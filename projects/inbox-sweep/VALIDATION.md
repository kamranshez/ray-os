Validation scope for the first end-to-end build, run on 2026-06-12 in `/Users/ray/Desktop/ray-os/projects/inbox-sweep`.

What was validated:

1. Gmail connection
   - Used the Gmail connector against `in:inbox -in:spam -in:trash newer_than:30d`.
   - Pulled 20 recent inbox results and read 10 selected messages deeply enough to create card summaries, draft seeds, and next actions.
   - Seeded `data/cards.json` from that real Gmail snapshot.

2. Filesystem state
   - `data/cards.json` is the source of truth for card status, summaries, proposed actions, and per-card command history.
   - `data/events.jsonl` is the append-only step log.
   - Browser and API commands update these files directly.

3. Local app/API
   - `npm run validate` starts the server on a temporary port.
   - It reads `/api/state`, checks Gmail source metadata, confirms every card has a summary/action/preview, posts a command to a card, verifies the card moves to `queued`, checks the HTML shell, verifies `events.jsonl`, and restores the original test state.

4. In-app browser
   - Opened `http://localhost:4177` in the Codex in-app browser.
   - Confirmed the UI rendered 10 active cards with the first card selected.
   - Entered `Draft a warm reply and keep this queued for review` through the card command box.
   - Confirmed the visible state changed to 10 active, 1 queued, 0 cleared, and the card history showed the command.

5. Responsive check
   - Temporarily set the browser viewport to 390 by 844.
   - Confirmed the page width matched the viewport, the summary area collapsed to one column, and the card rail behaved as a horizontal scroll strip.

Current known boundary:

- The app proposes Gmail actions and records local decisions, but it does not send replies, create Gmail drafts, archive, or delete mail. Those external side effects still require an explicit Codex/Gmail action from Ray.
