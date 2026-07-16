---
name: discord-archive
description: >
  Archive Discord channels and forums to local JSON files using Ray's own session — full
  message history, replies inline, forum threads enumerated and paginated, paced to look
  like a real browser. Use this skill whenever Ray wants to back up, archive, scrape,
  dump, or download a Discord server he's a member of, a specific channel, a forum
  channel's threads, or a server's "questions" / Q&A channels. Triggers on phrases like
  "archive this Discord", "back up the server", "scrape this channel", "download all
  messages from #X", "save the cohort questions", "dump the Discord", "make a copy of
  this server's posts", or any time he points at a Discord URL and wants the content
  pulled into local files. Also use when he wants to push an archive to a private GitHub
  repo for safekeeping. Do NOT use this skill for sending messages, moderating, or
  anything write-oriented — it is strictly read/archive. Honest about what it does:
  this uses Ray's user token via the same headers his browser sends, which is a Discord
  ToS grey-zone; the skill includes pacing, jitter, and 429-handling to behave well, and
  reminds him to rotate the token after a run.
---

# Discord Archive

Archive any Discord server Ray is a member of — text channels, announcement channels,
and forum channels (each thread paginated separately) — into local JSON, one file per
channel. Replies are preserved inline via `referenced_message`. Forum channels become
`{thread, messages}` arrays so the question/answer structure stays intact.

## Why a custom script (not DiscordChatExporter)

DCE works, but it doesn't let you pass arbitrary cookies or x-headers. Discord increasingly
fronts the API with Cloudflare bot-check, and the only way to look like the real browser
session is to send `cf_clearance`, `x-super-properties`, `x-installation-id`, and the
full cookie jar — same fingerprint as the logged-in Chrome tab. This skill's
`scripts/archiver.py` does that. DCE remains a good fallback if the custom script breaks
on a Discord API change — see `references/dce-fallback.md`.

## First-time setup

Three things have to land in `scripts/archiver.py`'s sibling credentials file:

1. **Capture the session profile** — open Discord in Chrome, DevTools → Network → pick any
   `/api/v9/...` XHR → "Copy as cURL". Hand that cURL to the parser below; it extracts
   token, cookies, and headers into a JSON profile. See `references/session-extraction.md`
   for the exact steps and the parser.

2. **Save profile to** `~/tools/discordchatexporter/.discord-session.json` with mode 600.
   The file shape is `{headers: {...}, cookies: {...}, guild_id: "<id>"}`. The guild_id
   is the long number after `/channels/` in any URL inside that server.

3. **Verify** before running the full archive:
   ```bash
   python3 /Users/ray/Desktop/ray-os/.claude/skills/discord-archive/scripts/archiver.py --check
   ```
   Prints the authed username + channel count and exits. If this 401s, the token is dead.

## Running the archive

```bash
# Archive every channel in the guild_id from the profile
python3 /Users/ray/Desktop/ray-os/.claude/skills/discord-archive/scripts/archiver.py

# Archive only specific channels (pass their IDs)
python3 /Users/ray/Desktop/ray-os/.claude/skills/discord-archive/scripts/archiver.py 1316388578908966932 1505834310089838722

# Output directory override (defaults to ~/discord-archive/<guild-slug>/)
ARCHIVE_OUT=~/Desktop/myarchive python3 /Users/ray/Desktop/ray-os/.claude/skills/discord-archive/scripts/archiver.py
```

Each channel gets its own JSON file. **Re-running skips channels already on disk** — this
is the resume mechanism. If a channel fails mid-run, just rerun; it picks up where it left off.

## Pacing — what's tuned and why

Defaults baked into the script:

| Sleep | Range | What it covers |
|---|---|---|
| Between message pages | 1.5–3.5 s | Looks like a slow scroll inside one channel |
| Between threads in a forum | 4–10 s | Forum threads are individually paginated; this is the gap when moving thread-to-thread |
| Between channels | 30–80 s | The big gap; long enough that the access pattern doesn't look like a burst scrape |
| Between archived-thread-list pages | 2–4 s | Walking the `threads/archived/public` paginator |

All sleeps are jittered (uniform random in the range), not fixed. 429 `Retry-After` is
respected automatically — the script sleeps the exact wait and retries.

To slow further, edit the `MIN_*_GAP` / `MAX_*_GAP` constants at the top of `archiver.py`.
Doubling them roughly halves the request rate.

## The gotchas (lessons learned, don't re-discover)

These are in `references/api-quirks.md` in detail. Quick summary:

- `GET /guilds/<id>/threads/active` is **bot-only** for user accounts (returns 403 with
  code 20002). Use `GET /channels/<id>/threads/search?archived=false&...` per-channel
  instead — this is the endpoint the web client actually uses.
- `403 Missing Access` (code 50001) on a specific channel/forum means Ray's account
  doesn't have read permission for that one — it is NOT a session-wide auth failure.
  The script handles this by returning `None` and writing an empty result for that
  channel only; it does not exit.
- Channels that show in the channel list with non-zero size files <2 KB are usually
  channels Ray has *visibility* to (sees in sidebar) but not *read access* to (messages
  endpoint returns empty array). Expected for cohort-locked channels you're not in.
- Forum channels (type 15) are NOT flat — they are collections of threads (each thread is
  itself a channel with its own messages endpoint). The script enumerates active threads
  via `threads/search`, then walks archived threads via `threads/archived/public`, then
  paginates messages inside each one.
- Replies are inline via `referenced_message` and `message_reference` on each message
  object — no separate API call needed to reconstruct them.

## After the archive — token rotation reminder

Tell Ray to rotate his token after every archive run. The token sits in
`.discord-session.json` (mode 600), but if it's been pasted into chat (as happened the
first time we built this), it's effectively public — anyone with transcript access has
full account control until rotation. Rotation = change Discord password, or Settings →
Devices → Log out all known devices. **Volunteer the reminder; don't wait for him to ask.**

## Pushing the archive to a private GitHub repo

If Ray asks to back the archive up to GitHub:

```bash
cd <archive-dir>
git init -b main -q
git add . && git commit -m "Initial archive: <guild name> (<N> channels, ~<size>)"
gh repo create <repo-name> --private --source=. --push --description "Local archive of <guild name>"
```

`gh` is pre-authed for ray-amjad. Default to `--private`. Don't include the
`.discord-session.json` file (it lives in `~/tools/discordchatexporter/`, not in the
archive directory, so this is naturally clean — just don't introduce a path that mixes
them).

## What's in `references/`

- `session-extraction.md` — how to pull the cURL out of Chrome and convert to the profile
  JSON, including a small Python parser
- `api-quirks.md` — full notes on the bot-only endpoints, forum structure, error codes
- `dce-fallback.md` — using DiscordChatExporter as a backup if the script ever breaks
