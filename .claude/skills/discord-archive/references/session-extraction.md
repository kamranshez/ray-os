# Session extraction — getting the profile JSON out of Chrome

The archiver expects a JSON file with three top-level keys: `headers`, `cookies`,
`guild_id`. This walks through extracting them from a live Discord session in
Chrome and saving them to the right place.

## What the profile looks like

```json
{
  "headers": {
    "accept": "*/*",
    "accept-language": "...",
    "authorization": "MTUxMDg1...the.user.token",
    "priority": "u=1, i",
    "referer": "https://discord.com/channels/<guild>/<channel>",
    "sec-ch-ua": "...",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 ...",
    "x-debug-options": "bugReporterEnabled",
    "x-discord-locale": "en-GB",
    "x-discord-timezone": "Asia/Tokyo",
    "x-installation-id": "...",
    "x-super-properties": "eyJ...base64..."
  },
  "cookies": {
    "__dcfduid": "...",
    "__sdcfduid": "...",
    "_ga": "...",
    "_ga_Q149DFWHT7": "...",
    "locale": "...",
    "OptanonConsent": "...",
    "_cfuvid": "...",
    "cf_clearance": "..."
  },
  "guild_id": "1316387060357140520"
}
```

Why every header matters: `x-super-properties` is base64-JSON encoding the client
build number, OS, browser, launch session id — Discord uses it to fingerprint the
session. `x-installation-id` is per-install. `cf_clearance` is the Cloudflare
bot-check pass token. Dropping any of these makes the request look like a generic
script and is more likely to draw a 403 or captcha challenge.

## Step-by-step extraction

1. Open Discord in Chrome and navigate into the server you want to archive
   (any channel works — referer will reflect it). Make sure you're logged in as
   the account that should own the archive.
2. Open DevTools: `Cmd+Opt+I` (Mac) / `F12` (Win/Linux).
3. **Network** tab → reload (`Cmd+R`).
4. Filter for `api/v9` (top filter box). Pick any XHR request — `science`,
   `users/@me`, `guilds/<id>` all work fine.
5. Right-click the request → **Copy** → **Copy as cURL (bash)**.
6. Paste the cURL into the parser below to produce the profile JSON.

## The parser

Run this Python from anywhere — paste the cURL between the heredoc markers:

```bash
python3 <<'PY'
import json, re, shlex, sys
from pathlib import Path

# === paste your full curl command between the triple quotes ===
curl_cmd = r"""
curl 'https://discord.com/api/v9/users/@me' \
  -H 'accept: */*' \
  ...
"""
# === end paste ===

tokens = shlex.split(curl_cmd.replace("\\\n", " "))
headers, cookies = {}, {}
url = None
i = 0
while i < len(tokens):
    t = tokens[i]
    if t in ("-H", "--header") and i + 1 < len(tokens):
        k, _, v = tokens[i+1].partition(":")
        headers[k.strip().lower()] = v.strip()
        i += 2
    elif t in ("-b", "--cookie") and i + 1 < len(tokens):
        for pair in tokens[i+1].split("; "):
            k, _, v = pair.partition("=")
            cookies[k.strip()] = v.strip()
        i += 2
    elif t.startswith("http"):
        url = t
        i += 1
    else:
        i += 1

# Extract guild_id from the referer if present, else None
guild_id = None
ref = headers.get("referer", "")
m = re.search(r"/channels/(\d+)/", ref)
if m:
    guild_id = m.group(1)

profile = {"headers": headers, "cookies": cookies, "guild_id": guild_id}
dest = Path.home() / "tools" / "discordchatexporter" / ".discord-session.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(profile, indent=2))
dest.chmod(0o600)
print(f"wrote profile to {dest}")
print(f"  headers: {len(headers)}")
print(f"  cookies: {len(cookies)}")
print(f"  guild_id: {guild_id}")
PY
```

If `guild_id` came out as `null`, your cURL came from a request that wasn't made
while viewing the target server. Fix it manually — open any channel in the target
server and copy any XHR from there, OR just edit the `guild_id` field in the JSON
to the server's ID (the long number in any of its channel URLs).

## Verify it works

```bash
python3 /Users/ray/Desktop/ray-os/.claude/skills/discord-archive/scripts/archiver.py --check
```

Should print `authed as <username>` and the guild name. If 401: token is dead
(account password was changed, or device was logged out). If guild reachable
output is missing: `guild_id` is wrong or the account isn't in that server.

## Why we're not using a username/password login

Discord stopped supporting raw username/password login over the API years ago.
The only realistic way to drive the API as a user is with a token, and the only
realistic way to get a token without writing a real OAuth flow is to copy it out
of an authenticated browser session. That's what we do.

## After the archive finishes — rotate

Token rotation: change Discord password OR Settings → Devices → Log out all
known devices. This invalidates the token. The profile JSON on disk becomes
inert (just bytes), and any leaked copy of the token is also dead. Do this
every time after running an archive — friction is low, payoff is the account
stays secure.
