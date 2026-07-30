---
tags: [bug-hunt, evaluation]
date: 2026-07-29
---

# Shared brief: 10-way bug-hunter bake-off on HyperWhisper

Every one of the ten hunter skills runs against **the same pinned arena**, at the **same
effort tier**, and writes **the same shaped report**. That is the whole point: if the
scopes differ, the comparison measures sampling luck instead of hunting strategy.

## The arena (pinned)

Repository root: `/Users/ray/Desktop/hyperwhisper-public`

In scope — the TypeScript surface only:

- `nextjs/` — Next.js marketing site + web app + 23 API routes + Drizzle DB layer.
  Subdirectories that matter: `app/`, `components/`, `server/`, `lib/`, `config/`,
  `contexts/`, `scripts/`, plus `middleware.ts` and `i18n.ts`.
- `hyperwhisper-cloud/` — Bun/Hono cloud transcription service: `src/routes/`,
  `src/providers/`, `src/middleware/`, `src/lib/`, `src/index.ts`.

That is **210 files, ~31,000 lines**. The exact file list is in `scope-files.txt`
next to this brief; it is the denominator for every coverage claim.

Out of scope — do not read, do not report on, do not count:

- `app/` (the Swift macOS + C# Windows desktop clients), `shared-core-rs/` (Rust),
  `mintlify-help/`, `benchmarks/`, `plans/`, `tasks/`, `routines/`
- Anything under `node_modules/`, `.next/`, `drizzle/` migration SQL, `dist/`, `.vercel/`

Why this slice: it is the only part of the monorepo with a working test/typecheck/lint
loop (`cd hyperwhisper-cloud && bun test`, `bun run typecheck`; `cd nextjs && npx tsc
--noEmit`, `npm run lint`), so the oracle-driven and execution-driven strategies can
actually run their tools instead of degrading to plain reading. It also carries the
real risk surface: auth, billing, quota accounting, provider fallbacks, webhooks.

## Rules of engagement

1. **Read-only on the working tree.** Do not edit, stage, commit, or `git checkout`
   anything. The single exception is `mutation-survivor-hunter`, which runs in its own
   isolated git worktree and reverts every mutation it makes.
2. **No network side effects.** Running the local test suite and typechecker is fine.
   Do not call production APIs, do not send webhooks, do not touch a real database.
   `.env.local` may contain live credentials — treat any secret you encounter as
   read-only, never echo one into a report, and never authenticate with it.
3. **Effort tier: deep.** Use the deep/thorough branch wherever the skill offers a
   quick-versus-deep choice.
4. **Nested subagents are mandatory.** Every phase the skill describes as parallel must
   actually fan out to subagents. A hunter that does all its own reading inline is not
   running the strategy it is being scored on.
5. **Stay in your lane.** Each skill has a distinct thesis. Do not drift into a sibling
   strategy because it looks productive; if the strategy comes up dry on this codebase,
   *that is a result* and reporting it honestly is worth more than a borrowed finding.

## The verification bar (identical for all ten)

The default verdict is **REFUTED**. A finding is only **CONFIRMED** when there is a
concrete trigger path from a real entry point — named file, named line, named caller,
and an input or sequence that reaches it. "This looks fragile" is REFUTED. A finding
that survives scrutiny but whose trigger path you cannot fully construct is
**PLAUSIBLE**, and it must say exactly which link in the chain is unproven.

Prefer proof over prose: a failing test, a `curl`, a node one-liner, an observed
typecheck error. Findings backed by something executable are the only ones that carry
full weight in the scoring.

## Required report shape

Write to `/Users/ray/Desktop/hyperwhisper-public/bug-hunt/reports/<skill-name>.md`.

Follow your own skill's report template for the body, but the file must open with this
exact frontmatter and header block so the reports can be compared mechanically:

```markdown
---
skill: <skill-name>
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | N |
| PLAUSIBLE findings | N |
| Findings with an executable repro | N |
| Files opened (of 210 in scope) | N |
| Subagents spawned | N |
| Strategy came up dry? | yes/no |

## Coverage ledger

<What you examined, what you deliberately skipped and why, and what this strategy is
structurally blind to on this codebase. A reader must never be able to mistake
"we looked at 14 files" for "the codebase is clean.">
```

Then the findings, then whatever else your skill's template calls for.

## What you return to the orchestrator

Your final message is data, not prose for a human. Return exactly:

- `skill`: your skill name
- `confirmed`: integer
- `plausible`: integer
- `with_repro`: integer
- `files_opened`: integer
- `subagents`: integer
- `findings`: array of `{severity, file, line, one_line_summary, verdict, has_repro}`
  for every CONFIRMED and PLAUSIBLE finding
- `dry`: boolean — did the strategy fail to produce anything on this codebase
- `self_assessment`: two or three sentences on where this strategy earned its keep here
  and where it wasted effort. Be honest about the waste; the comparison is worthless if
  every hunter claims it did great.
