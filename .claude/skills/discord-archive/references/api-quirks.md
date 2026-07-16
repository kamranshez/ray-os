# Discord API quirks — what we learned the hard way

These are the things that took a couple of tries to get right. The archiver
already handles all of them; this is the explanation so future-you doesn't
have to re-derive when the API drifts.

## Channel types — what each one is

`GET /guilds/<id>/channels` returns a flat list. Filter by `type`:

| `type` | Meaning | How to archive |
|---|---|---|
| 0 | Regular text channel | Paginate `/channels/<id>/messages` |
| 5 | Announcement channel | Same as text |
| 4 | Category (visual grouping in sidebar) | Skip — no messages |
| 2 | Voice channel | Skip — no messages |
| 13 | Stage voice | Skip |
| 15 | **Forum** — collection of threads | Enumerate threads, then paginate each |
| 16 | Media (gallery-style forum) | Same as forum |

`parent_id` on a non-category channel points at the category it lives in.

## Forums are not flat — threads are channels

A forum channel has no messages directly. Each "post" in a forum is a thread
(itself a channel with `type: 11` or `type: 12`), and messages live in the
thread. So archiving a forum is a two-step walk:

1. **Enumerate threads**:
   - Active threads: `GET /channels/<forum_id>/threads/search?archived=false&sort_by=last_message_time&sort_order=desc&limit=25&offset=N`
   - Archived public threads: `GET /channels/<forum_id>/threads/archived/public?limit=100&before=<archive_timestamp_iso>`
   - Combine, dedupe by thread `id`.
2. **For each thread**: paginate `/channels/<thread_id>/messages?limit=50&before=<msg_id>` like any text channel.

## The bot-only endpoint trap

`GET /guilds/<id>/threads/active` looks like the natural way to list active
threads server-wide, and it works in many API tutorials — but for **user**
accounts (not bots) it returns:

```json
{"message": "Only bots can use this endpoint.", "code": 20002}  // HTTP 403
```

For user accounts, use the per-channel `threads/search?archived=false` endpoint
instead. That's what the Discord web client uses, and it works with user tokens.

## Two different 403s — don't conflate them

A 403 from Discord can mean very different things:

| Body code | Meaning | What to do |
|---|---|---|
| `20002` | "Only bots can use this endpoint." | The endpoint is wrong — try a user-accessible one |
| `50001` | "Missing Access." | You don't have permission for this specific channel — skip it, but the session is fine |
| `40002` | "You need to verify your account." | Phone/email verification gate — can't bypass |

The archiver returns `None` on 403 (treating it as "this resource isn't
available") and continues. Only 401 (token invalid) stops the run.

## Pagination — `before=` is the trick

For messages:
```
GET /channels/<id>/messages?limit=50            # first page (most recent)
GET /channels/<id>/messages?limit=50&before=<id-of-last-msg-in-prev-page>
```
Keep going until the response is shorter than `limit` (or empty). That means
you've reached the start of the channel.

For archived threads, the cursor is `archive_timestamp` (an ISO 8601 string),
not an id:
```
GET /channels/<id>/threads/archived/public?limit=100
GET /channels/<id>/threads/archived/public?limit=100&before=<last-archive-ts>
```
Stop when `has_more: false`.

For the `threads/search` endpoint, the cursor is `offset=N` (integer).

## Rate limits — 429 with `Retry-After`

Discord returns:
```json
{"message": "You are being rate limited.", "retry_after": 1.234, "code": 0}  // HTTP 429
```

`retry_after` is in **seconds, as a float**. Sleep for that amount + a small
buffer, then retry the same request. The archiver does this in a loop. You
should never get rate-limited at the pacing the archiver uses by default — the
inter-page sleeps already exceed the per-route limits. 429s in practice tend to
mean Discord is doing global-bucket throttling because the account is making
unusually many requests across the day; if you see them, slow down further or
take a break.

## Replies are inline — no extra calls needed

When message A is a reply to message B, message A's JSON contains:

```json
{
  "message_reference": {"channel_id": "...", "message_id": "B"},
  "referenced_message": { ...full message B object... }
}
```

So a single pagination over `/messages` captures both sides of every reply.
The referenced message is sometimes `null` if the original was deleted; handle
that case if you process this downstream.

## Attachments and embeds — JSON only by default

The archiver records attachment/embed metadata in the JSON, but does not
download the binary contents. URLs like `cdn.discordapp.com/attachments/...`
have signed query parameters that expire (~24h). To preserve attachments,
download them within that window — see `references/dce-fallback.md` for the
DiscordChatExporter approach which downloads media inline.

## Useful read-only endpoints

| Endpoint | What it gets |
|---|---|
| `GET /users/@me` | Current user — auth ping |
| `GET /users/@me/guilds` | Servers the user is in |
| `GET /guilds/<id>` | Server name, owner, member count, features |
| `GET /guilds/<id>/channels` | All channels in a server |
| `GET /guilds/<id>/members/search?query=&limit=10` | Member lookup |
| `GET /channels/<id>` | Single channel metadata |
| `GET /channels/<id>/messages?limit=50` | Messages, paginated by `before=` |
| `GET /channels/<id>/messages/<msg_id>` | Single message |
| `GET /channels/<id>/threads/search?archived=false` | Active threads (forum) |
| `GET /channels/<id>/threads/archived/public?limit=100` | Archived public threads |
