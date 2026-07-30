---
name: entry-point-tracer
description: Hunt for bugs in an EXISTING codebase by enumerating every real entry point (HTTP routes, CLI commands, jobs, webhooks, IPC handlers, startup/shutdown) and tracing data and state from each one down through the call graph, looking for broken seams between layers. Use this skill whenever the user wants a bug hunt on code that is already merged — "find bugs in this codebase", "bug hunt", "trace for bugs", "find integration bugs", "what breaks end to end", "audit the whole app for bugs", "are there bugs hiding in here", "hunt for cross-file bugs", "find the bugs no PR review caught" — even if they don't say "trace" or "entry point". This is the complement to diff review, NOT a replacement for it — for reviewing a pending diff/PR/branch, use /code-review instead. Trigger this one when the target is the codebase as it exists, not a change to it.
---

# Entry-Point Tracer

Find bugs in an existing codebase by tracing every path a request, command, or event can take from the outside world down to its final effect — and interrogating each seam it crosses.

## Why this strategy

Diff review sees one change at a time. That makes it structurally blind to the most expensive class of production bug: five PRs that were each locally correct, whose *combination* is broken. Nobody wrote that bug in any single diff, so no diff review could have caught it. The bug lives in the seams — the boundary where layer N assumes something layer N-1 no longer guarantees.

The way to find seam bugs is not to read files. It is to walk paths. Every real bug is triggered by a real input arriving at a real entry point and flowing somewhere; if you enumerate the entry points and walk each flow end to end, you are reading the code in exactly the order the bug executes in. Your working frame throughout: **each function was probably correct when it was written; the bug lives between the functions.**

A second structural advantage: entry points are finite and enumerable, so this hunt has an honest coverage story. "We traced 14 of 17 entry points" is a claim a diff review can never make about a codebase.

## Effort levels

Accept an optional effort argument:

- **quick** (default when the user says "quick", "fast pass", or gives no signal on a large repo) — trace only the top 5 riskiest entry points from the inventory (risk-ranked in Phase 1).
- **deep** — trace every entry point in the inventory. Use when the user says "thorough", "audit", "all of it", "deep".

Everything else (inventory, verification bar, report) is identical between levels. The only knob is how many paths get traced.

---

## Phase 1 — Enumerate (one agent)

Spawn ONE subagent to build the entry-point inventory. This inventory is also the coverage ledger for the final report, so it must aim for exhaustive, not representative.

Subagent prompt (fill the bracketed parts):

```
Inventory every ENTRY POINT of the codebase at [repo root] — every place the
outside world can cause this code to execute. Why: each entry point becomes the
start of a bug-hunting trace, and anything you miss is a path nobody audits.

Search for ALL of these categories (Grep/Glob for the framework's registration
patterns — routers, decorators, manifests, config files — don't just read main):
1. HTTP routes / API handlers (include middleware chains that run before them)
2. CLI commands and subcommands
3. Cron / scheduled jobs, queue and stream consumers, background workers
4. Webhooks and third-party callbacks (payment providers, OAuth redirects, etc.)
5. IPC / RPC / message handlers, websocket events, pub-sub subscriptions
6. Startup and shutdown paths (init, migrations-on-boot, signal handlers,
   graceful-drain logic)
7. File watchers, upload handlers, import/export paths

For EACH entry point return:
- id: EP-<n>
- kind: one of the categories above
- location: file:line of the handler
- untrusted_inputs: what arrives from outside (params, body, headers, file
  contents, message payload, env, clock) and which of them are validated where
- state_touched: DBs/tables, caches, files, external APIs, globals it reads or
  writes
- risk (1-5): 5 = untrusted input + writes to important state + weak/absent
  validation or auth; 1 = read-only, trusted caller, simple
- risk_rationale: one line

Return the inventory as a numbered markdown table sorted by risk descending,
followed by a "possibly missed" note listing any registration mechanisms you
found but could not fully expand (dynamic route loading, plugin systems).
```

If the repo is a monorepo or the user scoped the hunt ("just the API", "just the sync engine"), pass that scope into the prompt and record the exclusion in the report's coverage section.

**Cluster before tracing.** Group entry points that share ≥80% of their call path (e.g. 12 CRUD routes through one service layer) into a single trace unit with one representative plus a note to check the variants' deltas. This keeps the trace count proportional to distinct *paths*, not route count.

---

## Phase 2 — Trace (one subagent per entry point / cluster, in parallel)

For quick: top 5 by risk. For deep: all. Launch tracers in parallel batches.

Tracer subagent prompt:

```
You are tracing ONE path through a codebase hunting for seam bugs. Why: diff
review audits changes one at a time, so bugs that emerge from the COMBINATION
of individually-correct functions have never been read by anyone. You are that
reader. Frame: each function was probably correct when written; the bug lives
in the seams between them.

Entry point: [EP-id, kind, file:line]
Untrusted inputs: [from inventory]
State touched: [from inventory]

Walk the call graph from the entry point downward (Read the handler, Grep for
each callee, Read it, continue) until the path terminates in effects (DB write,
response, external call, file, message). At EVERY hop ask one question:

  "What does this layer ASSUME that the layer above does not GUARANTEE?"

Hunt specifically for:
- Validation gaps: input checked at one edge, but a second path (another route,
  a job, a retry, an internal caller) reaches the same code without the check
- Tightened assumptions: a callee that now requires non-null / sorted / already-
  authorized / already-normalized input, with call sites that don't know
- Ordering and timing: code that only works if A completes before B, with
  nothing enforcing it (async handlers, event races, cache-then-db patterns)
- Partial failure: multi-step effects where step 2 of 3 fails — what state is
  left behind? Is it retried, and is the retry idempotent?
- Resource lifecycles across the path: connections, transactions, locks, file
  handles, temp files — opened at one layer, closed (or not) at another
- Concurrency on THIS path: two simultaneous invocations of this same entry
  point — shared caches, check-then-act on the DB, non-atomic counters
- Boundary mismatches: nullability, units, encodings, timezones, string/number
  ids, and ERROR CONTRACTS (callee throws, caller expects error return — or
  vice versa; errors swallowed at a layer that callers rely on for signaling)

For each candidate bug, return:
- trace: the path as hops — "EP-3 POST /import → parseUpload (upload.ts:41)
  → normalizeRows (normalize.ts:88) → bulkInsert (repo.ts:120)"
- seam: which hop pair breaks, and the assume/guarantee mismatch in one
  sentence
- trigger_sketch: the input/state/timing you believe triggers it
- consequence: the user-visible failure (crash, wrong data, data loss, hang,
  security bypass) — not an intermediate state
- confidence: your honest guess, low/medium/high

Also return depth_limits: places you stopped early (external SDK internals,
generated code, paths >N hops) so coverage can be reported honestly.
Do not self-censor medium/low-confidence candidates — an independent verifier
judges them next. Do NOT report style issues or hypotheticals with no
nameable trigger.
```

---

## Phase 3 — Verify (one independent verifier per finding, in parallel)

Off-diff hunting has no author standing by to sanity-check findings, so the verification bar must be *inverted* relative to code review: **default REFUTED**. A finding survives only if the verifier can construct the trigger, not merely fail to rule it out.

Verifier subagent prompt:

```
Adversarially verify ONE candidate bug. Why: whole-codebase hunts drown in
plausible-but-wrong findings unless every claim is forced through a concrete
end-to-end trigger. Your default verdict is REFUTED — the finding must earn
its way out.

Candidate: [trace, seam, trigger_sketch, consequence]

The finding arrives as a path, so demand the full walk:
1. Re-read every file on the trace yourself. Confirm each hop actually calls
   the next with the claimed data shape.
2. CONFIRMED requires ALL of:
   - The exact concrete input at the entry point (the literal request body /
     CLI args / message payload / timing arrangement)
   - The exact path taken, hop by hop, with the line where each assumption
     breaks — quote the lines
   - The wrong output, crash, or corruption at the end, stated concretely
3. REFUTED if: a guard exists anywhere on the path (quote it); the claimed
   input cannot reach the entry point (auth, routing, type system — show it);
   the "wrong" behavior is intentional. Check intent via git blame on the key
   lines, nearby comments, and any tests that pin the behavior — a test that
   asserts the current behavior is strong evidence of intent (name the test).
4. PLAUSIBLE only for genuinely environment-dependent triggers (needs a
   specific config/scale/provider behavior you cannot inspect) where the
   mechanism is otherwise fully verified. State exactly what would settle it.

Return: verdict, the full concrete trigger (if CONFIRMED), quoted evidence,
and intent_check (what blame/comments/tests said).
```

Drop REFUTED findings from the main report (list them one-line in an appendix — refutations are information too).

---

## Phase 4 — Prove (per CONFIRMED finding)

A confirmed seam bug comes with its trigger already written down; turn it into an artifact. For each CONFIRMED finding, spawn one subagent to produce a **failing test or minimal repro**, whichever is cheaper in this repo:

- A failing unit/integration test committed under the repo's existing test layout (do not commit — leave as an untracked file and report the path), OR
- A minimal repro script: the literal `curl` command, CLI invocation, or 10-line script that invokes the handler and demonstrates the wrong result.

The repro must run against the code as-is. If the repro *passes* (bug does not manifest), demote the finding to PLAUSIBLE and say why — this is the last honesty gate. Do NOT fix the bugs; this skill's deliverable is findings, and fixes are a separate decision for the user.

If the repo has no runnable test setup, write the test anyway, mark it `[unexecuted]`, and keep the CONFIRMED verdict only if the verifier's static walk was complete.

---

## Phase 5 — Report

Findings are presented AS traces — the path is the finding. Use exactly this template:

```markdown
# Bug hunt — entry-point trace of <repo> (<quick|deep>)

<2-3 sentence summary: entry points found, traced, bugs confirmed.>

## Confirmed bugs (ranked by severity)

### 1. <one-line title> — <severity: data-loss | security | crash | wrong-output | hang>
**Trace:** EP-3 `POST /import` → `parseUpload` (upload.ts:41) → `normalizeRows` (normalize.ts:88) → `bulkInsert` (repo.ts:120)
**Seam:** <the assume/guarantee mismatch, one sentence, naming both hops>
**Trigger:** <the literal input/timing>
**Consequence:** <user-visible failure>
**Repro:** <path to failing test / repro command> (<ran: failing | [unexecuted]>)

## Plausible (mechanism verified, trigger environment-dependent)
- <one line each: trace-summary — what would settle it>

## Coverage
| | Count |
|---|---|
| Entry points inventoried | N |
| Traced | N (list untraced EP-ids and why) |
| Depth limits hit | <where tracers stopped early> |
| Possibly-missed registration mechanisms | <from Phase 1> |

## Refuted (appendix)
- <one line each: claim — why refuted>
```

Rank severity by consequence class (data loss / security > crash / hang > wrong output), then by how mundane the trigger is — a bug triggered by an ordinary request outranks one needing a rare race.

Never let the report imply more coverage than happened: an untraced entry point is an unaudited attack surface and the coverage table must say so plainly. "No bugs found" is only a meaningful sentence next to an honest coverage table.
