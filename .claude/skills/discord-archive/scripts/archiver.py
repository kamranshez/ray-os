#!/usr/bin/env python3
"""
Discord archiver — uses browser-identical headers, cookies (including cf_clearance),
x-super-properties, x-installation-id. Mimics the exact session the user is logged
into. Paces requests with jitter; respects 429 Retry-After.

Handles:
  - text + announcement channels (type 0, 5)
  - forum channels (type 15): fetches all threads (active + archived public) and
    paginates messages in each
  - inline replies are in the message JSON (referenced_message / message_reference)

Output: one JSON file per channel under $ARCHIVE_OUT (default ~/discord-archive/<guild-slug>/).

Usage:
    archiver.py               # archive every channel in guild_id from creds
    archiver.py <chan_id>...  # archive only those channel IDs
    archiver.py --check       # verify auth and exit (no archive work)

Credentials file (JSON: {headers, cookies, guild_id}) is found in this order:
    1. $DISCORD_SESSION_FILE env var
    2. ~/tools/discordchatexporter/.discord-session.json
    3. ~/.config/discord-archive/.discord-session.json
    4. <script_dir>/.discord-session.json
"""
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = "https://discord.com/api/v9"
SCRIPT_DIR = Path(__file__).parent

CREDS_CANDIDATES = [
    Path(os.environ["DISCORD_SESSION_FILE"]) if os.environ.get("DISCORD_SESSION_FILE") else None,
    Path.home() / "tools" / "discordchatexporter" / ".discord-session.json",
    Path.home() / ".config" / "discord-archive" / ".discord-session.json",
    SCRIPT_DIR / ".discord-session.json",
]

# Pacing (seconds). Tuned to look like slow human scrolling.
MIN_PAGE_GAP, MAX_PAGE_GAP = 1.5, 3.5      # between message pages in one channel
MIN_CHAN_GAP, MAX_CHAN_GAP = 30, 80        # between channels
MIN_THREAD_GAP, MAX_THREAD_GAP = 4, 10     # between threads in one forum
MIN_ARCHIVE_PAGE_GAP, MAX_ARCHIVE_PAGE_GAP = 2, 4   # between thread-list pages


def jitter(lo, hi):
    return random.uniform(lo, hi)


def sleep_jitter(lo, hi, label=""):
    s = jitter(lo, hi)
    if label:
        print(f"    sleep {s:.1f}s ({label})")
    time.sleep(s)


def find_creds_file():
    for p in CREDS_CANDIDATES:
        if p and p.exists():
            return p
    raise SystemExit(
        "No session profile found. Looked in:\n  - "
        + "\n  - ".join(str(p) for p in CREDS_CANDIDATES if p)
        + "\nSee references/session-extraction.md for how to make one."
    )


def load_creds():
    p = find_creds_file()
    creds = json.loads(p.read_text())
    creds["_path"] = str(p)
    return creds


def resolve_out_dir(creds, guild_name=None):
    if os.environ.get("ARCHIVE_OUT"):
        return Path(os.environ["ARCHIVE_OUT"]).expanduser()
    slug = re.sub(r"[^a-z0-9-]+", "-", (guild_name or creds["guild_id"]).lower()).strip("-") or "guild"
    return Path.home() / "discord-archive" / slug


def http_get(creds, url, referer=None):
    """GET with full browser fingerprint. Retries on 429/5xx. Returns parsed JSON or None on 404."""
    while True:
        req = Request(url)
        headers = dict(creds["headers"])
        if referer:
            headers["referer"] = referer
        for k, v in headers.items():
            req.add_header(k, v)
        req.add_header("cookie", "; ".join(f"{k}={v}" for k, v in creds["cookies"].items()))
        try:
            with urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except HTTPError as e:
            body = e.read().decode(errors="replace")
            if e.code == 429:
                try:
                    wait = json.loads(body).get("retry_after", 5)
                except Exception:
                    wait = 10
                print(f"    429 rate-limited, sleeping {wait + 0.5:.1f}s")
                time.sleep(wait + 0.5)
                continue
            if e.code == 401:
                print(f"    AUTH 401: {body[:400]}")
                raise SystemExit("auth failed — token invalid or session expired")
            if e.code == 403:
                # endpoint-specific (bot-only, missing perms) — not session-wide
                print(f"    403 (endpoint not accessible): {body[:200]}")
                return None
            if e.code == 404:
                return None
            if 500 <= e.code < 600:
                print(f"    {e.code} server error, retrying in 10s")
                time.sleep(10)
                continue
            print(f"    HTTP {e.code}: {body[:400]}")
            return None
        except URLError as e:
            print(f"    network: {e}, retrying in 15s")
            time.sleep(15)


def safe_name(s):
    out = "".join(c if c.isalnum() or c == "-" else "-" for c in s)
    return out.strip("-") or "channel"


def fetch_messages(creds, channel_id, referer):
    """Paginate /channels/{id}/messages back to the beginning."""
    msgs = []
    before = None
    page = 0
    while True:
        url = f"{BASE}/channels/{channel_id}/messages?limit=50"
        if before:
            url += f"&before={before}"
        batch = http_get(creds, url, referer=referer)
        if not batch:
            break
        msgs.extend(batch)
        before = batch[-1]["id"]
        page += 1
        print(f"      page {page}: +{len(batch)} (running total {len(msgs)})")
        if len(batch) < 50:
            break
        sleep_jitter(MIN_PAGE_GAP, MAX_PAGE_GAP)
    return msgs


def fetch_archived_threads(creds, channel_id, referer):
    """Walk /threads/archived/public for a forum channel."""
    threads = []
    before = None
    while True:
        url = f"{BASE}/channels/{channel_id}/threads/archived/public?limit=100"
        if before:
            url += f"&before={before}"
        data = http_get(creds, url, referer=referer)
        if not data:
            break
        batch = data.get("threads", [])
        threads.extend(batch)
        print(f"      archived-page: +{len(batch)} (running total {len(threads)})")
        if not data.get("has_more") or not batch:
            break
        last = batch[-1].get("thread_metadata", {}).get("archive_timestamp")
        if not last:
            break
        before = last
        sleep_jitter(MIN_ARCHIVE_PAGE_GAP, MAX_ARCHIVE_PAGE_GAP)
    return threads


def fetch_active_threads(creds, channel_id, referer):
    """Use the forum-search endpoint that user-clients use to list active threads."""
    threads = []
    offset = 0
    while True:
        url = (
            f"{BASE}/channels/{channel_id}/threads/search"
            f"?archived=false&sort_by=last_message_time&sort_order=desc&limit=25&offset={offset}"
        )
        data = http_get(creds, url, referer=referer)
        if not data:
            break
        batch = data.get("threads", [])
        if not batch:
            break
        threads.extend(batch)
        print(f"      active-page: +{len(batch)} (running total {len(threads)})")
        if not data.get("has_more"):
            break
        offset += len(batch)
        sleep_jitter(MIN_ARCHIVE_PAGE_GAP, MAX_ARCHIVE_PAGE_GAP)
    return threads


def archive_text_channel(creds, ch, guild_id, out_dir):
    name, cid = ch["name"], ch["id"]
    ref = f"https://discord.com/channels/{guild_id}/{cid}"
    out = out_dir / f"{safe_name(name)}__{cid}.json"
    if out.exists() and out.stat().st_size > 50:
        print(f"  skip #{name} (already archived: {out.name})")
        return
    print(f"  text #{name}")
    msgs = fetch_messages(creds, cid, referer=ref)
    out.write_text(json.dumps({"channel": ch, "messages": msgs}, indent=2, ensure_ascii=False))
    print(f"  -> wrote {len(msgs)} messages to {out.name}")


def archive_forum_channel(creds, ch, guild_id, out_dir):
    name, cid = ch["name"], ch["id"]
    ref = f"https://discord.com/channels/{guild_id}/{cid}"
    out = out_dir / f"{safe_name(name)}__{cid}__forum.json"
    if out.exists() and out.stat().st_size > 50:
        print(f"  skip forum #{name} (already archived: {out.name})")
        return
    print(f"  forum #{name}")
    print(f"    fetching active threads...")
    active = fetch_active_threads(creds, cid, referer=ref)
    print(f"    {len(active)} active threads")
    print(f"    fetching archived threads...")
    archived = fetch_archived_threads(creds, cid, referer=ref)
    print(f"    {len(archived)} archived threads")
    seen = set()
    all_threads = []
    for t in active + archived:
        if t["id"] not in seen:
            seen.add(t["id"])
            all_threads.append(t)
    print(f"    {len(all_threads)} unique threads to fetch messages from")

    thread_data = []
    for i, t in enumerate(all_threads):
        print(f"    thread [{i+1}/{len(all_threads)}] {t['name']!r} ({t['id']})")
        tref = f"https://discord.com/channels/{guild_id}/{t['id']}"
        msgs = fetch_messages(creds, t["id"], referer=tref)
        thread_data.append({"thread": t, "messages": msgs})
        if i < len(all_threads) - 1:
            sleep_jitter(MIN_THREAD_GAP, MAX_THREAD_GAP, "next thread")

    total = sum(len(t["messages"]) for t in thread_data)
    out.write_text(json.dumps({"channel": ch, "threads": thread_data}, indent=2, ensure_ascii=False))
    print(f"  -> wrote {total} messages across {len(thread_data)} threads to {out.name}")


def main():
    creds = load_creds()
    guild_id = creds["guild_id"]
    print(f"using session profile: {creds['_path']}")

    # Auth ping
    print("auth check...")
    me = http_get(creds, f"{BASE}/users/@me")
    print(f"  authed as {me['username']} (id={me['id']})")

    # Guild info for the output directory slug
    guild_info = http_get(creds, f"{BASE}/guilds/{guild_id}") or {}
    guild_name = guild_info.get("name", guild_id)
    out_dir = resolve_out_dir(creds, guild_name)
    print(f"  guild: {guild_name!r}")
    print(f"  output dir: {out_dir}\n")

    # --check mode: stop here, leave on-disk state untouched
    if "--check" in sys.argv:
        print("check OK — credentials valid, guild reachable.")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # Reload channels (the cache may be stale across runs)
    chans = http_get(creds, f"{BASE}/guilds/{guild_id}/channels")
    (out_dir / "_channels.json").write_text(json.dumps(chans, indent=2))
    text_chans = [c for c in chans if c["type"] in (0, 5)]
    forum_chans = [c for c in chans if c["type"] == 15]
    print(f"discovered: {len(text_chans)} text/announcement, {len(forum_chans)} forum\n")

    # Optional filtering via CLI args. Usage:
    #   archiver.py                  -> all channels
    #   archiver.py <channel_id> ... -> only those IDs
    arg_ids = {a for a in sys.argv[1:] if not a.startswith("--")}
    units = []
    for c in text_chans:
        if not arg_ids or c["id"] in arg_ids:
            units.append(("text", c))
    for c in forum_chans:
        if not arg_ids or c["id"] in arg_ids:
            units.append(("forum", c))

    for i, (kind, ch) in enumerate(units):
        print(f"[{i+1}/{len(units)}] {kind} #{ch['name']} ({ch['id']})")
        try:
            if kind == "text":
                archive_text_channel(creds, ch, guild_id, out_dir)
            else:
                archive_forum_channel(creds, ch, guild_id, out_dir)
        except SystemExit:
            raise
        except Exception as e:
            print(f"  ERROR on #{ch['name']}: {e}")
        if i < len(units) - 1:
            sleep_jitter(MIN_CHAN_GAP, MAX_CHAN_GAP, "next channel")
        print()

    print("all done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ninterrupted.")
