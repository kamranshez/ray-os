Inbox Sweep is a Codex-native email triage surface. Gmail is used for ingestion, while the app itself owns local state in `data/cards.json` and `data/events.jsonl`.

Run it:

```bash
npm start
```

Then open:

```text
http://localhost:4177
```

Validate it:

```bash
npm run validate
```

Read the proof notes:

```text
VALIDATION.md
```

State model:

- `data/cards.json` is the rendered queue and current card status.
- `data/drafts.json` stores local reply drafts you applied for later sending and style learning.
- `data/sent-replies.json` stores replies you actually sent, plus the edit/style signals to learn from.
- `data/events.jsonl` is the append-only process log.
- `/api/state` reads the filesystem state.
- `/api/cards/:id/command` stores what you told a card and infers the local action.
- `/api/cards/:id/draft` saves or updates a local draft for a card.
- `/api/cards/:id/status` sets a card status directly.

Gmail safety:

- The current snapshot was created from recent inbox messages via the Gmail connector.
- The app does not archive, delete, send, or create Gmail drafts by itself.
- Applied replies are saved in the local draft box until you explicitly ask Codex to perform them in Gmail.
- Sent replies can be recorded back into the local corpus after you send them in Gmail.
