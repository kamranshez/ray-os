#!/usr/bin/env python3
"""Verify the status of a Wise transfer before re-sending.

Reads WISE_API_KEY from <repo-root>/.env, fans out across every Wise profile
(personal + all businesses), and searches recent transfers for matches by
recipient email, recipient name, reference, or amount. Output is JSON so
Claude (or a human) can reason about whether a given payment actually went
through, was cancelled, or was refunded.

Why this exists: Ray gets emails from people saying "your transfer to me was
cancelled, please re-send". Before re-sending, we want a definitive answer:
- outgoing_payment_sent  -> they got it (or the bank did), don't re-send
- funds_refunded         -> Wise pulled it back, safe to re-send
- cancelled              -> never funded, safe to re-send
- processing / pending   -> wait, don't re-send yet
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://api.wise.com"


def load_api_key() -> str:
    repo_root = Path(__file__).resolve().parents[4]
    env_file = repo_root / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("WISE_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    key = os.environ.get("WISE_API_KEY")
    if key:
        return key
    sys.exit(f"WISE_API_KEY not found. Add it to {env_file} or export it.")


def api_get(path: str, key: str):
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        headers={"Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def list_profiles(key: str):
    return api_get("/v2/profiles", key)


def list_transfers(profile_id: int, key: str, start_iso: str, end_iso: str):
    qs = urllib.parse.urlencode({
        "profile": profile_id,
        "limit": 200,
        "offset": 0,
        "createdDateStart": start_iso,
        "createdDateEnd": end_iso,
    })
    return api_get(f"/v1/transfers?{qs}", key)


def get_recipient(account_id, key: str):
    if not account_id:
        return {}
    try:
        return api_get(f"/v1/accounts/{account_id}", key)
    except Exception:
        return {}


def amount_close(a, b, tol=0.05):
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def match(transfer, recipient, args) -> bool:
    """Return True if this transfer matches any of the supplied filters."""
    ref = ((transfer.get("details") or {}).get("reference") or "").lower()
    email = (recipient.get("details") or {}).get("email", "") or ""
    name = recipient.get("accountHolderName") or ""

    hits = []
    if args.reference:
        hits.append(args.reference.lower() in ref)
    if args.email:
        hits.append(args.email.lower() in email.lower())
    if args.name:
        hits.append(args.name.lower() in name.lower())
    if args.amount is not None:
        hits.append(
            amount_close(transfer.get("sourceValue"), args.amount)
            or amount_close(transfer.get("targetValue"), args.amount)
        )
    # If no filters were given, surface everything (caller can grep).
    return all(hits) if hits else True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--email", help="Recipient email (substring match)")
    p.add_argument("--name", help="Recipient name (substring match)")
    p.add_argument("--reference", help="Transfer reference (substring match, e.g. RW20260523)")
    p.add_argument("--amount", type=float, help="Source or target amount (within 5 cents)")
    p.add_argument("--days", type=int, default=60, help="Days back to search (default 60)")
    p.add_argument("--include-recipient-lookup", action="store_true",
                   help="Resolve every transfer's recipient account (slower, lets you filter by email/name).")
    args = p.parse_args()

    # When the user filters by email or name, we have to resolve recipients.
    if args.email or args.name:
        args.include_recipient_lookup = True

    key = load_api_key()
    profiles = list_profiles(key)

    # Date range — Wise wants ISO with milliseconds and Z.
    from datetime import datetime, timedelta, timezone
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=args.days)
    fmt = "%Y-%m-%dT%H:%M:%S.000Z"

    results = []
    for prof in profiles:
        pid = prof["id"]
        prof_label = prof.get("fullName") or (
            (prof.get("details") or {}).get("name")
            or f"{(prof.get('details') or {}).get('firstName','')} {(prof.get('details') or {}).get('lastName','')}".strip()
        )
        try:
            transfers = list_transfers(pid, key, start.strftime(fmt), end.strftime(fmt))
        except Exception as e:
            results.append({"profile": prof_label, "error": str(e)})
            continue

        for t in transfers:
            recipient = (
                get_recipient(t.get("targetAccount"), key)
                if args.include_recipient_lookup
                else {}
            )
            if not match(t, recipient, args):
                continue
            results.append({
                "profile": prof_label,
                "profile_id": pid,
                "transfer_id": t.get("id"),
                "status": t.get("status"),
                "created": t.get("created"),
                "source": f"{t.get('sourceCurrency')} {t.get('sourceValue')}",
                "target": f"{t.get('targetCurrency')} {t.get('targetValue')}",
                "reference": (t.get("details") or {}).get("reference"),
                "recipient_account_id": t.get("targetAccount"),
                "recipient_name": recipient.get("accountHolderName"),
                "recipient_email": (recipient.get("details") or {}).get("email"),
                "recipient_type": recipient.get("type"),
            })

    # Sort newest first.
    results.sort(key=lambda r: r.get("created") or "", reverse=True)
    print(json.dumps({
        "filters": {
            "email": args.email,
            "name": args.name,
            "reference": args.reference,
            "amount": args.amount,
            "days": args.days,
        },
        "count": len(results),
        "matches": results,
    }, indent=2))


if __name__ == "__main__":
    main()
