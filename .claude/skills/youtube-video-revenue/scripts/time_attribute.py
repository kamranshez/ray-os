#!/usr/bin/env python3
"""
Time-proximity revenue attribution for Ray's YouTube videos.

For every clean Stripe checkout session, find the most-recently-published video
whose [publishedAt, publishedAt + N days] window contains the session's
creation time. That video gets credit for the sale. Sessions that fall outside
every window land in a "baseline" bucket, and we compute the median daily
baseline revenue to estimate how much of each video's haul is the video's
actual lift versus the background organic rate.

This complements the UTM-based attribution in build_snapshot.py. UTM is the
lower-bound truth (set at checkout creation, never wrong, but only ~11% YTD
coverage because the code shipped 2026-03-13). Time-proximity reaches ~48%
YTD coverage and is the best retroactive estimate for pre-March-13 sessions.

Sessions excluded as "noise" (not video-driven):
- `metadata.purchaseType == "team_add_seats"` (seat top-ups on existing teams)
- `metadata.upgrade_from` set (tier upgrades initiated from user settings)

Output JSON shape:
{
  "method": "Nday_proximity",
  "window_days": 3,
  "baseline_daily_median_cents": 61772,
  "baseline_daily_mean_cents": 93060,
  "baseline_days_count": 88,
  "baseline_sessions_count": 481,
  "baseline_revenue_cents": 8189217,
  "totals": {
    "clean_sessions": 1581,
    "clean_revenue_cents": 23660613,
    "time_attributed_revenue_cents": 15471396,
    "lift_over_baseline_revenue_cents": 11518473
  },
  "videos": [
    {
      "videoId": "...",
      "title": "...",
      "publishedAt": "YYYY-MM-DDT...",
      "utm_revenue_cents": int,
      "utm_sessions": int,
      "time_attributed_sessions": int,
      "time_attributed_revenue_cents": int,
      "lift_over_baseline_cents": int,
      "competing_video_overlap_sessions": int,
      "yt_views": int | null
    }
  ]
}
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
import sys
from collections import defaultdict
from typing import Any


def load_json(path: str) -> Any:
    with open(path) as f:
        return json.load(f)


def parse_ts(value: Any) -> dt.datetime | None:
    """Accept ISO string or unix int; return UTC-aware datetime."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(int(value), tz=dt.timezone.utc)
    s = str(value).rstrip("Z")
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        # Fall back to date-only
        try:
            return dt.datetime.fromisoformat(s[:10]).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d


def is_noise(session: dict[str, Any]) -> bool:
    meta = session.get("metadata") or {}
    if (meta.get("purchaseType") or "").lower() == "team_add_seats":
        return True
    if meta.get("upgrade_from"):
        return True
    return False


def compute(
    videos: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    window_days: int,
) -> dict[str, Any]:
    # Normalize and sort videos by publishedAt (most recent first)
    video_entries: list[dict[str, Any]] = []
    for v in videos:
        published = parse_ts(v.get("publishedAt") or v.get("published_at"))
        if not published:
            continue
        video_entries.append({
            "videoId": v["videoId"],
            "title": v.get("title", ""),
            "publishedAt": published,
            "publishedAt_iso": published.isoformat(),
            "yt_views": v.get("youtube_views"),
            "window_end": published + dt.timedelta(days=window_days),
            "utm_sessions": 0,
            "utm_revenue_cents": 0,
            "time_attributed_sessions": 0,
            "time_attributed_revenue_cents": 0,
            "competing_video_overlap_sessions": 0,
        })
    video_entries.sort(key=lambda v: v["publishedAt"], reverse=True)
    video_by_id = {v["videoId"]: v for v in video_entries}

    # Walk sessions
    baseline_revenue_by_day: dict[dt.date, int] = defaultdict(int)
    baseline_sessions = 0
    baseline_revenue_total = 0
    clean_sessions = 0
    clean_revenue = 0

    for s in sessions:
        if is_noise(s):
            continue
        amount = int(s.get("amount_total") or 0)
        clean_sessions += 1
        clean_revenue += amount

        created = parse_ts(s.get("created"))
        if created is None:
            continue

        # UTM credit (separate from time attribution — both are recorded)
        utm = ((s.get("metadata") or {}).get("utm_campaign") or "").strip()
        if utm and utm in video_by_id:
            video_by_id[utm]["utm_sessions"] += 1
            video_by_id[utm]["utm_revenue_cents"] += amount

        # Time-proximity: find videos whose window contains this timestamp
        candidates = [v for v in video_entries if v["publishedAt"] <= created <= v["window_end"]]
        if not candidates:
            baseline_sessions += 1
            baseline_revenue_total += amount
            baseline_revenue_by_day[created.date()] += amount
            continue

        # Most recent wins; older candidates count as overlap losers
        winner = candidates[0]  # video_entries is sorted desc by publishedAt
        winner["time_attributed_sessions"] += 1
        winner["time_attributed_revenue_cents"] += amount
        if len(candidates) > 1:
            winner["competing_video_overlap_sessions"] += 1

    # Baseline stats
    daily_revenues = list(baseline_revenue_by_day.values())
    baseline_median = int(statistics.median(daily_revenues)) if daily_revenues else 0
    baseline_mean = int(statistics.mean(daily_revenues)) if daily_revenues else 0

    # Lift = time-attributed revenue minus what we'd expect from baseline alone
    # (baseline_median per day * window_days). Clamp to zero — a video can't
    # have negative lift in this model.
    lift_total = 0
    expected_per_video = baseline_median * window_days
    for v in video_entries:
        lift = max(0, v["time_attributed_revenue_cents"] - expected_per_video)
        v["lift_over_baseline_cents"] = lift
        lift_total += lift

    # Render video rows in the same descending-by-time-attributed order the
    # subagent originally used; ties broken by publishedAt desc.
    video_entries.sort(
        key=lambda v: (-v["time_attributed_revenue_cents"], -v["publishedAt"].timestamp()),
    )

    out_videos = []
    for v in video_entries:
        out_videos.append({
            "videoId": v["videoId"],
            "title": v["title"],
            "publishedAt": v["publishedAt_iso"],
            "utm_revenue_cents": v["utm_revenue_cents"],
            "utm_sessions": v["utm_sessions"],
            "time_attributed_sessions": v["time_attributed_sessions"],
            "time_attributed_revenue_cents": v["time_attributed_revenue_cents"],
            "lift_over_baseline_cents": v["lift_over_baseline_cents"],
            "competing_video_overlap_sessions": v["competing_video_overlap_sessions"],
            "yt_views": v["yt_views"],
        })

    time_attributed_total = sum(v["time_attributed_revenue_cents"] for v in video_entries)

    return {
        "method": f"{window_days}day_proximity",
        "window_days": window_days,
        "baseline_daily_median_cents": baseline_median,
        "baseline_daily_mean_cents": baseline_mean,
        "baseline_days_count": len(daily_revenues),
        "baseline_sessions_count": baseline_sessions,
        "baseline_revenue_cents": baseline_revenue_total,
        "totals": {
            "clean_sessions": clean_sessions,
            "clean_revenue_cents": clean_revenue,
            "time_attributed_revenue_cents": time_attributed_total,
            "lift_over_baseline_revenue_cents": lift_total,
        },
        "videos": out_videos,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vidtempla", required=True, help="vidtempla.json (videos array)")
    ap.add_argument("--stripe", required=True, help="stripe.json (sessions list)")
    ap.add_argument("--output", required=True, help="Where to write the time-attribution JSON")
    ap.add_argument("--window-days", type=int, default=3, help="Days after publish to credit a video (default 3)")
    args = ap.parse_args()

    vidtempla = load_json(args.vidtempla)
    sessions = load_json(args.stripe)
    if isinstance(sessions, dict) and "sessions" in sessions:
        sessions = sessions["sessions"]

    result = compute(vidtempla.get("videos", []), sessions, args.window_days)

    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    totals = result["totals"]
    print(
        f"Wrote {args.output}: {len(result['videos'])} videos, "
        f"baseline ${result['baseline_daily_median_cents']/100:,.2f}/day median, "
        f"time-attributed ${totals['time_attributed_revenue_cents']/100:,.2f}, "
        f"lift ${totals['lift_over_baseline_revenue_cents']/100:,.2f}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
