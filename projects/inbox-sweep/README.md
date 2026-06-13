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
- `data/events.jsonl` is the append-only process log.
- `/api/state` reads the filesystem state.
- `/api/cards/:id/command` stores what you told a card and infers the local action.
- `/api/cards/:id/status` sets a card status directly.

Gmail safety:

- The current snapshot was created from recent inbox messages via the Gmail connector.
- The app does not archive, delete, send, or create Gmail drafts by itself.
- Proposed email actions are local until you explicitly ask Codex to perform them in Gmail.
