# Inbox Sweep

Inbox Sweep is Ray's local Gmail triage surface. It runs from `projects/inbox-sweep` and usually serves `http://localhost:4177/`.

## What This App Is For

- Show Gmail inbox items as cards with summary, full email context, reply suggestions, and an editable reply box.
- Let Ray edit a suggested reply, hit Apply, and save a local draft in `data/drafts.json`.
- When Ray asks to send saved drafts, send them through Gmail, record the sent reply, clear the local card, and archive the Gmail conversation so it disappears from Inbox.
- Improve future reply suggestions from Ray's real sent replies over time.

## Durable Data

Treat the files under `data/` as meaningful app state, not throwaway fixtures.

- `data/cards.json` is the current local email queue plus history.
- `data/drafts.json` stores local drafts Ray has applied in the UI.
- `data/sent-replies.json` stores Gmail replies that Ray actually sent. Use it as the reply-style learning corpus.
- `data/reply-style.json` is the compact style profile used to shape future suggestions.
- `data/events.jsonl` is a durable audit/learning log. Commit it when it records meaningful refresh, draft, send, archive, or style-learning events.

If refreshing data from Gmail, update the relevant JSON files and append a concise event to `events.jsonl`.

## Gmail Refresh Rules

- Prefer live Gmail data over stale local state.
- Default inbox refresh query should avoid noise: `in:inbox -in:trash -in:spam`, with newsletter/Substack sources excluded when building the active queue.
- Newsletters, Substacks, and obvious FYI broadcasts should not appear in the active reply queue by default. Keep them as cleared/history if useful, but do not make Ray process them as reply work unless he asks.
- Read full email bodies for queued cards whenever possible. The UI should let Ray read the full email before editing replies.
- If Gmail returns multiple messages from the same thread, preserve message IDs and thread IDs carefully. Do not invent IDs.

## Reply Suggestions

Suggestions should be full draft replies, not meta-analysis.

Use Ray's current style profile:

- concise and direct
- warm without being salesy
- concrete first, with one useful detail when needed
- lightly casual when the thread already has that tone, for example `:)`, `haha`, `yeh`, or `kind of`
- usually closes with `Best,\nRay` or `Best,\n\nRay`
- asks a clarifying question when good advice depends on missing context
- declines briefly when Ray cannot take something on

Do not promise timelines, commitments, or reviews Ray has not explicitly agreed to.

## Send And Archive Workflow

When Ray says drafts are ready to send:

1. Find local drafts with `status: "draft"` or the relevant unsent state.
2. Match each draft to its source Gmail message/thread.
3. Send via Gmail using the correct recipient, subject, and `reply_message_id` when replying in-thread.
4. Record the sent reply in `data/sent-replies.json`.
5. Mark the local draft/card as sent/cleared.
6. Archive the whole Gmail conversation, not just the latest inbound message. A thread can remain in Inbox if any message in it still has `INBOX`.
7. Append a meaningful event to `data/events.jsonl`.
8. Refresh or reload the local UI.

## Local Development

- Run from `projects/inbox-sweep`.
- Start with `npm start` unless another process is already serving `4177`.
- Validate with `npm run validate` after data or behavior changes.
- Use the in-app browser for UI verification when Ray is looking at `localhost:4177`.

## Commit Hygiene

- Commit `data/events.jsonl`, `data/reply-style.json`, and `data/sent-replies.json` when they change because of real workflow learning.
- Keep unrelated Obsidian workspace churn, especially `.obsidian/workspace.json`, out of Inbox Sweep commits.
- If creating or updating instruction files here, keep `AGENTS.md` and `CLAUDE.md` paired. Prefer `CLAUDE.md` as a relative symlink to `AGENTS.md`.
