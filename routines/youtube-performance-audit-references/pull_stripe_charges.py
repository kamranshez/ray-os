#!/usr/bin/env python3
"""
Pull Stripe charges for a target month and bucket them for Ray's monthly audit.

Usage:
    export STRIPE_KEY='rk_live_...'
    python3 pull_stripe_charges.py \
        --month 2026-03 \
        --uploads "2026-03-02,2026-03-04,2026-03-07" \
        --output /tmp/march.json

Output JSON structure:
    {
      "month": "2026-03",
      "totals": {sales, gross, refunds, net},
      "daily": {YYYY-MM-DD: {sales, gross, refunds}},
      "per_video": [{upload_date, sales, gross, refunds, net, avg_order, daily_breakdown}],
      "baseline": {non_video_days, mean_sales_per_day, mean_gross_per_day},
      "video_window": {unique_days, mean_sales_per_day, mean_gross_per_day},
      "multiplier": float
    }

Filters to LINK.COM* AGENTICCODIN descriptor (masterclass only).
"""
import argparse
import base64
import calendar
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone


MASTERCLASS_DESCRIPTOR = "LINK.COM* AGENTICCODIN"


def month_bounds(month: str) -> tuple[int, int]:
    """Return (start_ts, end_ts) for a YYYY-MM string, inclusive start, exclusive end.
    Pads 2 days before and 3 days after to catch 3-day windows that cross month edges.
    """
    year, mon = map(int, month.split("-"))
    start = datetime(year, mon, 1, tzinfo=timezone.utc) - timedelta(days=2)
    last_day = calendar.monthrange(year, mon)[1]
    end = datetime(year, mon, last_day, 23, 59, 59, tzinfo=timezone.utc) + timedelta(days=3)
    return int(start.timestamp()), int(end.timestamp())


def fetch_all_charges(key: str, start_ts: int, end_ts: int) -> list[dict]:
    """Paginate Stripe charges. Returns all charges in the window."""
    auth = base64.b64encode(f"{key}:".encode()).decode()
    all_charges = []
    starting_after = None
    while True:
        params = {
            "created[gte]": str(start_ts),
            "created[lte]": str(end_ts),
            "limit": "100",
        }
        if starting_after:
            params["starting_after"] = starting_after
        url = "https://api.stripe.com/v1/charges?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}"})
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
        all_charges.extend(data["data"])
        if not data["has_more"]:
            break
        starting_after = data["data"][-1]["id"]
    return all_charges


def filter_masterclass(charges: list[dict]) -> list[dict]:
    return [
        c for c in charges
        if c["status"] == "succeeded"
        and c.get("calculated_statement_descriptor") == MASTERCLASS_DESCRIPTOR
    ]


def daily_breakdown(charges: list[dict]) -> dict[str, dict]:
    daily = defaultdict(lambda: {"sales": 0, "gross": 0.0, "refunds": 0.0})
    for c in charges:
        d = datetime.fromtimestamp(c["created"], tz=timezone.utc).strftime("%Y-%m-%d")
        daily[d]["sales"] += 1
        daily[d]["gross"] += c["amount"] / 100
        daily[d]["refunds"] += c.get("amount_refunded", 0) / 100
    return dict(daily)


def window_totals(charges: list[dict], start_date: str, days: int = 3) -> dict:
    start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end = start + timedelta(days=days)
    in_window = [c for c in charges if start.timestamp() <= c["created"] < end.timestamp()]
    sales = len(in_window)
    gross = sum(c["amount"] for c in in_window) / 100
    refunds = sum(c.get("amount_refunded", 0) for c in in_window) / 100
    daily = defaultdict(lambda: {"sales": 0, "gross": 0.0})
    for c in in_window:
        d = datetime.fromtimestamp(c["created"], tz=timezone.utc).strftime("%Y-%m-%d")
        daily[d]["sales"] += 1
        daily[d]["gross"] += c["amount"] / 100
    return {
        "upload_date": start_date,
        "sales": sales,
        "gross": round(gross, 2),
        "refunds": round(refunds, 2),
        "net": round(gross - refunds, 2),
        "avg_order": round(gross / sales, 2) if sales else 0,
        "daily_breakdown": dict(daily),
    }


def compute_baseline(daily: dict[str, dict], month: str, upload_dates: list[str]) -> tuple[dict, dict, float]:
    """Compute baseline (non-video-window days) vs video-window days stats.
    Returns (baseline_stats, video_window_stats, multiplier).
    """
    video_window_days = set()
    for upload in upload_dates:
        start = datetime.strptime(upload, "%Y-%m-%d")
        for i in range(3):
            video_window_days.add((start + timedelta(days=i)).strftime("%Y-%m-%d"))
    month_days = [d for d in daily if d.startswith(month)]
    non_video = [d for d in month_days if d not in video_window_days]
    video_days = [d for d in month_days if d in video_window_days]
    baseline = {
        "non_video_day_count": len(non_video),
        "days": sorted(non_video),
        "mean_sales_per_day": round(sum(daily[d]["sales"] for d in non_video) / len(non_video), 2) if non_video else 0,
        "mean_gross_per_day": round(sum(daily[d]["gross"] for d in non_video) / len(non_video), 2) if non_video else 0,
    }
    video_window = {
        "unique_days": len(video_days),
        "mean_sales_per_day": round(sum(daily[d]["sales"] for d in video_days) / len(video_days), 2) if video_days else 0,
        "mean_gross_per_day": round(sum(daily[d]["gross"] for d in video_days) / len(video_days), 2) if video_days else 0,
    }
    multiplier = round(video_window["mean_gross_per_day"] / baseline["mean_gross_per_day"], 2) if baseline["mean_gross_per_day"] else 0
    return baseline, video_window, multiplier


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--uploads", required=True, help="Comma-separated YYYY-MM-DD upload dates")
    ap.add_argument("--output", required=True, help="Path to write JSON result")
    args = ap.parse_args()

    key = os.environ.get("STRIPE_KEY")
    if not key:
        sys.exit("ERROR: set STRIPE_KEY env var")

    start_ts, end_ts = month_bounds(args.month)
    uploads = [u.strip() for u in args.uploads.split(",") if u.strip()]

    print(f"Fetching charges from {datetime.fromtimestamp(start_ts, tz=timezone.utc)} to {datetime.fromtimestamp(end_ts, tz=timezone.utc)}...", file=sys.stderr)
    charges = fetch_all_charges(key, start_ts, end_ts)
    print(f"Fetched {len(charges)} total charges", file=sys.stderr)

    mc = filter_masterclass(charges)
    print(f"Masterclass-only: {len(mc)}", file=sys.stderr)

    # Restrict daily view to month only
    daily_all = daily_breakdown(mc)
    month_daily = {d: v for d, v in daily_all.items() if d.startswith(args.month)}

    totals = {
        "sales": sum(v["sales"] for v in month_daily.values()),
        "gross": round(sum(v["gross"] for v in month_daily.values()), 2),
        "refunds": round(sum(v["refunds"] for v in month_daily.values()), 2),
    }
    totals["net"] = round(totals["gross"] - totals["refunds"], 2)

    per_video = [window_totals(mc, u) for u in uploads]
    baseline, video_window, multiplier = compute_baseline(daily_all, args.month, uploads)

    result = {
        "month": args.month,
        "charges_fetched": len(charges),
        "masterclass_charges": len(mc),
        "totals": totals,
        "daily": month_daily,
        "per_video": per_video,
        "baseline": baseline,
        "video_window": video_window,
        "multiplier": multiplier,
    }
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Wrote {args.output}", file=sys.stderr)
    print(json.dumps({
        "total_sales": totals["sales"],
        "total_gross": totals["gross"],
        "total_net": totals["net"],
        "baseline_per_day": baseline["mean_gross_per_day"],
        "video_window_per_day": video_window["mean_gross_per_day"],
        "multiplier": multiplier,
    }, indent=2))


if __name__ == "__main__":
    main()
