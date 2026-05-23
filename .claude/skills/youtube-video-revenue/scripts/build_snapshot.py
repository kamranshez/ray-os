#!/usr/bin/env python3
"""
Combine VidTempla + PostHog + Stripe data into a snapshot JSON and a markdown report.

Inputs are normalized JSON files written by the skill's earlier steps.
Output snapshot is written to <snapshots-dir>/<YYYY-MM-DD>.json; markdown report
is printed to stdout.

Schema for inputs (see SKILL.md and references/data_sources.md):

  vidtempla.json:
    {"videos": [{"videoId": str, "title": str, "publishedAt": "YYYY-MM-DD...", "youtube_views": int}]}

  posthog.json:
    {"visitors": {videoId: int}, "workshop_checkouts": {videoId: int}, "posthog_purchases": {videoId: int}}

  stripe.json:
    [{"id": str, "created": unix_int, "amount_total": cents_int, "metadata": {...}}, ...]

The Y-prefix bug and similar known typos are corrected via aliases.json.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from typing import Any

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
NEAR_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,12}$")


def load_json(path: str) -> Any:
    with open(path) as f:
        return json.load(f)


def fmt_money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


def fmt_pct(num: float, denom: float) -> str:
    if denom == 0:
        return "—"
    return f"{(num / denom) * 100:.2f}%"


def apply_aliases(value: str, aliases: dict[str, str]) -> str:
    """Map known-broken utm_campaign values to the real video ID. Unknown values pass through."""
    return aliases.get(value, value)


def build_snapshot(
    vidtempla: dict[str, Any],
    posthog: dict[str, Any],
    stripe_sessions: list[dict[str, Any]],
    aliases: dict[str, str],
    window_from: str,
    window_to: str,
    snapshot_date: str,
    time_attribution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    # Index VidTempla videos by ID
    video_index: dict[str, dict[str, Any]] = {}
    for v in vidtempla.get("videos", []):
        vid = v["videoId"]
        video_index[vid] = {
            "videoId": vid,
            "title": v.get("title", ""),
            "published_at": (v.get("publishedAt") or "")[:10],
            "youtube_views": v.get("youtube_views", 0) or 0,
            "posthog_visitors": posthog.get("visitors", {}).get(vid, 0),
            "posthog_purchases": posthog.get("posthog_purchases", {}).get(vid, 0),
            "workshop_checkouts": posthog.get("workshop_checkouts", {}).get(vid, 0),
            "stripe_sessions": 0,
            "stripe_revenue_cents": 0,
        }

    # Roll up Stripe sessions by utm_campaign (after alias correction)
    sessions_total = 0
    revenue_total_cents = 0
    sessions_with_utm = 0
    revenue_with_utm_cents = 0
    workshop_session_count = 0
    workshop_revenue_cents = 0

    # Unknown utm_campaigns we encountered, for anomaly reporting
    unknown_campaigns: dict[str, dict[str, int]] = defaultdict(lambda: {"sessions": 0, "revenue_cents": 0})
    # Track which aliases actually fired (for transparency)
    alias_hits: dict[str, dict[str, int]] = defaultdict(lambda: {"sessions": 0, "revenue_cents": 0})

    for s in stripe_sessions:
        amount = int(s.get("amount_total") or 0)
        sessions_total += 1
        revenue_total_cents += amount

        meta = s.get("metadata") or {}
        if (meta.get("purchaseType") or "").lower() == "workshop":
            workshop_session_count += 1
            workshop_revenue_cents += amount

        raw_utm = (meta.get("utm_campaign") or "").strip()
        if not raw_utm:
            continue
        sessions_with_utm += 1
        revenue_with_utm_cents += amount

        corrected = apply_aliases(raw_utm, aliases)
        if corrected != raw_utm:
            alias_hits[raw_utm]["sessions"] += 1
            alias_hits[raw_utm]["revenue_cents"] += amount

        if corrected in video_index:
            video_index[corrected]["stripe_sessions"] += 1
            video_index[corrected]["stripe_revenue_cents"] += amount
        else:
            # Not a tracked video — could be `broadcast`, an old video, or a typo we don't know about
            unknown_campaigns[corrected]["sessions"] += 1
            unknown_campaigns[corrected]["revenue_cents"] += amount

    # Merge in time-proximity attribution if provided (see scripts/time_attribute.py).
    # Time attribution complements UTM: UTM is lower-bound truth, time-proximity is
    # the best retroactive estimate especially for pre-Mar-13-2026 sessions that
    # structurally couldn't carry utm_campaign metadata.
    time_videos_index: dict[str, dict[str, Any]] = {}
    if time_attribution:
        time_videos_index = {v["videoId"]: v for v in time_attribution.get("videos", [])}

    for vid, v in video_index.items():
        ta = time_videos_index.get(vid)
        if ta is not None:
            v["time_attributed_sessions"] = ta["time_attributed_sessions"]
            v["time_attributed_revenue_cents"] = ta["time_attributed_revenue_cents"]
            v["lift_over_baseline_cents"] = ta["lift_over_baseline_cents"]
            v["competing_video_overlap_sessions"] = ta["competing_video_overlap_sessions"]
        else:
            v["time_attributed_sessions"] = 0
            v["time_attributed_revenue_cents"] = 0
            v["lift_over_baseline_cents"] = 0
            v["competing_video_overlap_sessions"] = 0

    # Surface videos that appear in time-attribution but not VidTempla (e.g. older
    # videos that VidTempla pagination dropped). Carry them so the snapshot is
    # honest about what earned.
    if time_attribution:
        for ta in time_attribution["videos"]:
            if ta["videoId"] not in video_index and ta["time_attributed_revenue_cents"] > 0:
                video_index[ta["videoId"]] = {
                    "videoId": ta["videoId"],
                    "title": ta.get("title", ""),
                    "published_at": (ta.get("publishedAt") or "")[:10],
                    "youtube_views": ta.get("yt_views") or 0,
                    "posthog_visitors": posthog.get("visitors", {}).get(ta["videoId"], 0),
                    "posthog_purchases": posthog.get("posthog_purchases", {}).get(ta["videoId"], 0),
                    "workshop_checkouts": posthog.get("workshop_checkouts", {}).get(ta["videoId"], 0),
                    "stripe_sessions": 0,
                    "stripe_revenue_cents": 0,
                    "time_attributed_sessions": ta["time_attributed_sessions"],
                    "time_attributed_revenue_cents": ta["time_attributed_revenue_cents"],
                    "lift_over_baseline_cents": ta["lift_over_baseline_cents"],
                    "competing_video_overlap_sessions": ta["competing_video_overlap_sessions"],
                }

    # Compute per-video derived fields
    for v in video_index.values():
        sessions = v["stripe_sessions"]
        v["avg_ticket_cents"] = int(v["stripe_revenue_cents"] / sessions) if sessions else None
        views = v["youtube_views"]
        v["ctr_pct"] = round((v["posthog_visitors"] / views) * 100, 2) if views else None
        v["revenue_per_view_cents"] = round(v["stripe_revenue_cents"] / views, 2) if views else None

    # Build anomalies list
    anomalies: list[dict[str, Any]] = []
    for raw, stats in alias_hits.items():
        anomalies.append({
            "type": "alias_applied",
            "from": raw,
            "to": aliases[raw],
            "sessions": stats["sessions"],
            "revenue_cents": stats["revenue_cents"],
            "note": "Known broken utm_campaign; review references/aliases.json after the source bug is fixed.",
        })
    for camp, stats in unknown_campaigns.items():
        looks_like_video = bool(NEAR_VIDEO_ID_RE.match(camp))
        anomalies.append({
            "type": "unknown_utm_campaign",
            "value": camp,
            "sessions": stats["sessions"],
            "revenue_cents": stats["revenue_cents"],
            "looks_like_video_id": looks_like_video,
            "note": (
                "Unknown campaign value that resembles a YouTube ID — could be an untracked video or a new "
                "instance of the Y-prefix bug." if looks_like_video else
                "Non-video campaign (e.g. broadcast/email)."
            ),
        })

    stats = {
        "stripe_sessions_total": sessions_total,
        "stripe_revenue_cents": revenue_total_cents,
        "sessions_with_utm_campaign": sessions_with_utm,
        "revenue_with_utm_campaign_cents": revenue_with_utm_cents,
        "attribution_coverage_pct": round((revenue_with_utm_cents / revenue_total_cents) * 100, 2) if revenue_total_cents else 0.0,
        "workshop_session_count": workshop_session_count,
        "workshop_revenue_cents": workshop_revenue_cents,
    }

    if time_attribution:
        ta_totals = time_attribution.get("totals", {})
        ta_videos = time_attribution.get("videos", [])
        # Fall back to summing per-video if the source file is the older shape (no `totals` block)
        time_total = ta_totals.get("time_attributed_revenue_cents") or sum(
            v.get("time_attributed_revenue_cents", 0) for v in ta_videos
        )
        lift_total = ta_totals.get("lift_over_baseline_revenue_cents") or sum(
            v.get("lift_over_baseline_cents", 0) for v in ta_videos
        )
        # Parse window_days from the method string if not explicitly present (e.g. "3day_proximity")
        window_days_val = time_attribution.get("window_days")
        if window_days_val is None:
            method_str = time_attribution.get("method") or ""
            m = re.match(r"(\d+)day", method_str)
            if m:
                window_days_val = int(m.group(1))
        stats["time_attribution"] = {
            "method": time_attribution.get("method"),
            "window_days": window_days_val,
            "baseline_daily_median_cents": time_attribution.get("baseline_daily_median_cents", 0),
            "baseline_daily_mean_cents": time_attribution.get("baseline_daily_mean_cents", 0),
            "baseline_sessions_count": time_attribution.get("baseline_sessions_count", 0),
            "baseline_revenue_cents": time_attribution.get("baseline_revenue_cents", 0),
            "clean_sessions": ta_totals.get("clean_sessions", 0),
            "clean_revenue_cents": ta_totals.get("clean_revenue_cents", 0),
            "time_attributed_revenue_cents": time_total,
            "lift_over_baseline_revenue_cents": lift_total,
            "time_coverage_pct": round((time_total / revenue_total_cents) * 100, 2) if revenue_total_cents else 0.0,
            "lift_coverage_pct": round((lift_total / revenue_total_cents) * 100, 2) if revenue_total_cents else 0.0,
        }

    return {
        "snapshot_date": snapshot_date,
        "window": {"from": window_from, "to": window_to},
        "stats": stats,
        "videos": video_index,
        "anomalies": anomalies,
    }


def find_previous_snapshot(snapshots_dir: str, current_date: str) -> dict[str, Any] | None:
    if not os.path.isdir(snapshots_dir):
        return None
    candidates = sorted(
        f for f in os.listdir(snapshots_dir)
        if f.endswith(".json") and f != f"{current_date}.json"
    )
    if not candidates:
        return None
    with open(os.path.join(snapshots_dir, candidates[-1])) as f:
        return json.load(f)


def render_markdown(snapshot: dict[str, Any], previous: dict[str, Any] | None) -> str:
    stats = snapshot["stats"]
    window = snapshot["window"]
    out: list[str] = []

    out.append(f"# Video Revenue Snapshot — {snapshot['snapshot_date']}")
    out.append(f"Window: {window['from']} to {window['to']}")
    out.append(f"Stripe sessions captured: **{stats['stripe_sessions_total']:,}**")
    out.append(f"Total revenue: **{fmt_money(stats['stripe_revenue_cents'])}**")
    out.append(
        f"UTM attribution: **{stats['attribution_coverage_pct']}%** of revenue carries `utm_campaign` "
        f"({stats['sessions_with_utm_campaign']:,}/{stats['stripe_sessions_total']:,} sessions). "
        f"This is a lower-bound — only sessions created after `2a08f84f` (2026-03-13) can carry UTMs."
    )
    if "time_attribution" in stats:
        ta = stats["time_attribution"]
        window_label = f"{ta['window_days']}-day" if ta.get("window_days") else "time"
        out.append(
            f"Time-proximity attribution ({window_label} window): "
            f"**{ta['time_coverage_pct']}%** raw / **{ta['lift_coverage_pct']}%** lift-adjusted. "
            f"Baseline {fmt_money(ta['baseline_daily_median_cents'])}/day median."
        )
    if stats["workshop_session_count"]:
        out.append(
            f"Workshop product revenue (any source): **{fmt_money(stats['workshop_revenue_cents'])}** "
            f"across {stats['workshop_session_count']} sessions"
        )
    out.append("")

    # Top earners all-time (sorted by stripe revenue)
    videos = list(snapshot["videos"].values())
    earners = sorted([v for v in videos if v["stripe_revenue_cents"] > 0], key=lambda v: -v["stripe_revenue_cents"])

    out.append("## Top earners by UTM revenue (lower-bound truth)")
    if not earners:
        out.append("_No video-attributed revenue yet._")
    else:
        out.append("| Rank | Video | Published | UTM rev | Sessions | Visitors | YT views | $/view |")
        out.append("|---:|---|---|---:|---:|---:|---:|---:|")
        for i, v in enumerate(earners[:25], 1):
            title = (v["title"] or v["videoId"])[:55]
            rpv = f"${v['revenue_per_view_cents'] / 100:.3f}" if v["revenue_per_view_cents"] is not None else "—"
            out.append(
                f"| {i} | `{v['videoId']}` {title} | {v['published_at']} | "
                f"{fmt_money(v['stripe_revenue_cents'])} | {v['stripe_sessions']} | "
                f"{v['posthog_visitors']} | {v['youtube_views']:,} | {rpv} |"
            )
    out.append("")

    # Top earners by time-attribution (richer retroactive view)
    time_earners = sorted(
        [v for v in videos if v.get("time_attributed_revenue_cents", 0) > 0],
        key=lambda v: -v["time_attributed_revenue_cents"],
    )
    if time_earners:
        out.append("## Top earners by time-proximity (best retroactive estimate)")
        out.append("| Rank | Video | Published | Time-attrib | Lift | UTM rev | Δ (time − UTM) |")
        out.append("|---:|---|---|---:|---:|---:|---:|")
        for i, v in enumerate(time_earners[:25], 1):
            title = (v["title"] or v["videoId"])[:55]
            time_rev = v["time_attributed_revenue_cents"]
            lift = v["lift_over_baseline_cents"]
            utm_rev = v["stripe_revenue_cents"]
            delta = time_rev - utm_rev
            out.append(
                f"| {i} | `{v['videoId']}` {title} | {v['published_at']} | "
                f"{fmt_money(time_rev)} | {fmt_money(lift)} | {fmt_money(utm_rev)} | "
                f"{'+' if delta > 0 else ''}{fmt_money(delta)} |"
            )
        out.append("")

    # Published in window
    in_window = [
        v for v in videos
        if v["published_at"] and window["from"] <= v["published_at"] <= window["to"]
    ]
    in_window.sort(key=lambda v: v["published_at"], reverse=True)

    # Videos that earned revenue but were published BEFORE the window — the "still earning" tail
    older_earners = [
        v for v in videos
        if v["stripe_revenue_cents"] > 0
        and v["published_at"]
        and v["published_at"] < window["from"]
    ]
    older_earners.sort(key=lambda v: -v["stripe_revenue_cents"])

    out.append(f"## Published in window ({len(in_window)} videos, newest first)")
    if not in_window:
        out.append("_No videos published in window._")
    else:
        # Build delta-since-previous map
        prev_video_revenue: dict[str, int] = {}
        if previous:
            for vid, pv in previous.get("videos", {}).items():
                prev_video_revenue[vid] = pv.get("stripe_revenue_cents", 0)

        out.append("| Published | Video | Revenue | Sessions | Visitors | YT views | CTR | Δ rev |")
        out.append("|---|---|---:|---:|---:|---:|---:|---:|")
        for v in in_window:
            title = (v["title"] or v["videoId"])[:55]
            ctr = f"{v['ctr_pct']:.2f}%" if v["ctr_pct"] is not None else "—"
            delta = v["stripe_revenue_cents"] - prev_video_revenue.get(v["videoId"], 0) if previous else 0
            delta_str = fmt_money(delta) if delta else "—"
            out.append(
                f"| {v['published_at']} | `{v['videoId']}` {title} | "
                f"{fmt_money(v['stripe_revenue_cents'])} | {v['stripe_sessions']} | "
                f"{v['posthog_visitors']} | {v['youtube_views']:,} | {ctr} | {delta_str} |"
            )
    out.append("")

    # Older videos still earning ("the long tail")
    out.append(f"## Older videos still earning ({len(older_earners)} videos)")
    if not older_earners:
        out.append("_None — every revenue-attributed video was published in this window._")
    else:
        out.append("These videos were published BEFORE the window but still generated attributed revenue inside it. Old content compounds.")
        out.append("")
        out.append("| Published | Video | Revenue | Sessions | YT views | $/view |")
        out.append("|---|---|---:|---:|---:|---:|")
        for v in older_earners[:20]:
            title = (v["title"] or v["videoId"])[:55]
            rpv = f"${v['revenue_per_view_cents'] / 100:.3f}" if v["revenue_per_view_cents"] is not None else "—"
            out.append(
                f"| {v['published_at']} | `{v['videoId']}` {title} | "
                f"{fmt_money(v['stripe_revenue_cents'])} | {v['stripe_sessions']} | "
                f"{v['youtube_views']:,} | {rpv} |"
            )
    out.append("")

    # Movers since previous snapshot
    if previous:
        prev_date = previous.get("snapshot_date", "?")
        out.append(f"## Movers since previous snapshot ({prev_date})")
        prev_videos = previous.get("videos", {})
        movers = []
        new_videos = []
        for vid, cur in snapshot["videos"].items():
            prev = prev_videos.get(vid)
            if prev is None:
                if cur["stripe_revenue_cents"] > 0 or cur["youtube_views"] > 0:
                    new_videos.append(cur)
                continue
            delta = cur["stripe_revenue_cents"] - prev.get("stripe_revenue_cents", 0)
            session_delta = cur["stripe_sessions"] - prev.get("stripe_sessions", 0)
            if delta != 0 or session_delta != 0:
                movers.append((delta, session_delta, cur))

        movers.sort(key=lambda x: -x[0])

        if not movers and not new_videos:
            out.append("_No revenue changes since last snapshot._")
        else:
            for delta, sess_delta, v in movers[:15]:
                age_days = ""
                if v["published_at"]:
                    try:
                        age = (dt.date.fromisoformat(snapshot["snapshot_date"]) - dt.date.fromisoformat(v["published_at"])).days
                        age_days = f" (video age: {age}d)"
                    except ValueError:
                        pass
                title = (v["title"] or v["videoId"])[:50]
                out.append(
                    f"- `{v['videoId']}` {title}: **{fmt_money(delta)}** "
                    f"({sess_delta:+d} sessions){age_days}"
                )
            for v in new_videos:
                title = (v["title"] or v["videoId"])[:50]
                out.append(
                    f"- 🆕 `{v['videoId']}` {title} appeared "
                    f"({v['stripe_sessions']} sessions, {fmt_money(v['stripe_revenue_cents'])})"
                )
    else:
        out.append("## Movers since previous snapshot")
        out.append("_First snapshot — no previous run to compare._")
    out.append("")

    # Anomalies
    out.append("## Anomalies")
    anomalies = snapshot.get("anomalies", [])
    if not anomalies:
        out.append("_None._")
    else:
        for a in anomalies:
            if a["type"] == "alias_applied":
                out.append(
                    f"- 🐛 Alias applied: `{a['from']}` → `{a['to']}` "
                    f"({a['sessions']} sessions, {fmt_money(a['revenue_cents'])}). {a['note']}"
                )
            elif a["type"] == "unknown_utm_campaign":
                tag = "❓ Looks like a video ID" if a["looks_like_video_id"] else "•"
                out.append(
                    f"- {tag} Unknown utm_campaign `{a['value']}` "
                    f"({a['sessions']} sessions, {fmt_money(a['revenue_cents'])}). {a['note']}"
                )
    out.append("")

    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vidtempla", required=True)
    ap.add_argument("--posthog", required=True)
    ap.add_argument("--stripe", required=True)
    ap.add_argument("--snapshots-dir", required=True)
    ap.add_argument("--aliases", required=True)
    ap.add_argument("--window-from", required=True, help="YYYY-MM-DD")
    ap.add_argument("--window-to", required=True, help="YYYY-MM-DD")
    ap.add_argument("--snapshot-date", default=None, help="YYYY-MM-DD; defaults to today")
    ap.add_argument(
        "--time-attribution",
        default=None,
        help="Optional time_attribution.json (from scripts/time_attribute.py) to merge per-video lift data.",
    )
    args = ap.parse_args()

    vidtempla = load_json(args.vidtempla)
    posthog = load_json(args.posthog)
    stripe = load_json(args.stripe)
    aliases_raw = load_json(args.aliases)
    # Drop the _comment key from aliases if present
    aliases = {k: v for k, v in aliases_raw.items() if not k.startswith("_")}
    time_attribution = load_json(args.time_attribution) if args.time_attribution else None

    snapshot_date = args.snapshot_date or dt.date.today().isoformat()
    snapshot = build_snapshot(
        vidtempla, posthog, stripe, aliases, args.window_from, args.window_to, snapshot_date,
        time_attribution=time_attribution,
    )

    os.makedirs(args.snapshots_dir, exist_ok=True)
    out_path = os.path.join(args.snapshots_dir, f"{snapshot_date}.json")
    with open(out_path, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Wrote snapshot to {out_path}", file=sys.stderr)

    previous = find_previous_snapshot(args.snapshots_dir, snapshot_date)
    report = render_markdown(snapshot, previous)
    print(report)


if __name__ == "__main__":
    main()
