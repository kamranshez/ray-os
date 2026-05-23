#!/usr/bin/env python3
"""
Paginate Stripe Checkout Sessions API and write a normalized JSON file.

Reads STRIPE_RESTRICTED_KEY from env. Never logs or echoes it.
Writes an array of {id, created, amount_total, currency, customer_email, mode, metadata}
to the path given by --output.

Usage:
  python3 fetch_stripe.py --created-gte 1767225600 --output /tmp/stripe.json

The Stripe MCP can't search checkout sessions, so we go to the REST API directly.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from typing import Any

STRIPE_BASE = "https://api.stripe.com/v1"
MAX_PAGES = 100  # sanity cap; 16k sessions even at limit=100 is plenty


def http_get(url: str, key: str) -> dict[str, Any]:
    """GET with basic auth; raise on non-2xx with body for debugging."""
    req = urllib.request.Request(url)
    # Stripe wants basic auth: key as username, empty password
    import base64

    token = base64.b64encode(f"{key}:".encode()).decode()
    req.add_header("Authorization", f"Basic {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise SystemExit(f"Stripe HTTP {e.code}: {body}") from e


def fetch_checkout_sessions(key: str, created_gte: int, created_lte: int | None) -> list[dict[str, Any]]:
    """Paginate every status=complete Checkout Session in the window."""
    sessions: list[dict[str, Any]] = []
    starting_after: str | None = None

    for page in range(MAX_PAGES):
        params: dict[str, str] = {
            "limit": "100",
            "status": "complete",
            "created[gte]": str(created_gte),
        }
        if created_lte is not None:
            params["created[lte]"] = str(created_lte)
        if starting_after:
            params["starting_after"] = starting_after

        url = f"{STRIPE_BASE}/checkout/sessions?{urllib.parse.urlencode(params)}"
        resp = http_get(url, key)
        batch = resp.get("data", [])
        sessions.extend(batch)

        print(f"  page {page + 1}: +{len(batch)} sessions (total {len(sessions)})", file=sys.stderr)

        if not resp.get("has_more") or not batch:
            break
        starting_after = batch[-1]["id"]
        # Light throttle — Stripe rate limit is generous but be polite
        time.sleep(0.1)
    else:
        # Hit the page cap; warn loudly
        print(
            f"WARNING: hit {MAX_PAGES}-page cap; may have missed older sessions. "
            "Consider narrowing the window.",
            file=sys.stderr,
        )

    return sessions


def normalize(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the fields the report needs. Drops PII we don't use."""
    out: list[dict[str, Any]] = []
    for s in sessions:
        out.append(
            {
                "id": s.get("id"),
                "created": s.get("created"),
                "amount_total": s.get("amount_total") or 0,
                "currency": s.get("currency"),
                # customer_email is useful for grepping a specific buyer; keep it
                "customer_email": s.get("customer_email") or s.get("customer_details", {}).get("email"),
                "mode": s.get("mode"),
                "metadata": s.get("metadata") or {},
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--created-gte", type=int, required=True, help="Unix timestamp; only fetch sessions created after this")
    ap.add_argument("--created-lte", type=int, default=None, help="Unix timestamp; upper bound (optional)")
    ap.add_argument("--output", required=True, help="Path to write the normalized JSON array")
    args = ap.parse_args()

    key = os.environ.get("STRIPE_RESTRICTED_KEY")
    if not key:
        # Fall back to STRIPE_SECRET_KEY for convenience but warn — restricted key is safer
        key = os.environ.get("STRIPE_SECRET_KEY")
        if key:
            print(
                "Using STRIPE_SECRET_KEY; consider switching to a restricted key with "
                "only Checkout Session read access.",
                file=sys.stderr,
            )
    if not key:
        raise SystemExit(
            "Missing STRIPE_RESTRICTED_KEY env var. Set it with:\n"
            "  export STRIPE_RESTRICTED_KEY='rk_live_...'\n"
            "and rerun."
        )

    print(f"Fetching Stripe Checkout Sessions since unix={args.created_gte}...", file=sys.stderr)
    raw = fetch_checkout_sessions(key, args.created_gte, args.created_lte)
    print(f"Got {len(raw)} sessions; normalizing...", file=sys.stderr)
    normalized = normalize(raw)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(normalized, f, indent=2)

    print(f"Wrote {len(normalized)} sessions to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
