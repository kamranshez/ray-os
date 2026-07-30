---
name: concurrency-hunter
description: Hunt an existing codebase for concurrency, async, and lifecycle bugs — races, TOCTOU, missing awaits, deadlocks, leaked resources, teardown asymmetry, stale-response overwrites. Use this whenever the user wants a bug hunt focused on timing, ordering, or lifetime; says "race condition", "find races", "deadlock", "resource leak", "intermittent bug", "flaky in prod", "works on my machine", "happens under load", "sometimes it double-fires", or asks to audit async code, workers, queues, caches, or shared state for correctness. Also reach for it when a general bug hunt is requested on a codebase with meaningful concurrency (servers, UI apps, job systems) — this is the bug class that survives both tests and review. NOT for reviewing a diff or PR; that's /code-review.
---

# concurrency-hunter

Find timing, ordering, and lifetime bugs in existing code. This class is special:
a race passes the test suite and survives code review because both examine ONE
interleaving — the happy one. The only reliable lens is to enumerate the shared
state and the interleavings explicitly, which is what this skill does. Stay on
this lens; generic logic bugs, spec mismatches, and input-validation holes belong
to sibling skills.

Because there is no diff and no author on hand to cheaply sanity-check findings,
verification is INVERTED: every candidate is presumed refuted until a verifier
writes out a reachable interleaving. A plausible-sounding race that cannot name
its trigger is noise, and noise is what kills whole-codebase hunts.

## Effort levels

Parse the invocation for an effort word; default to `quick` if absent.

| | quick | deep |
|---|---|---|
| Hunt lenses | A, B, D | A, B, C, D, E |
| Map scope | top ~10 shared-state items + async boundaries | full concurrency map |
| Repro phase | skipped (interleaving writeups only) | attempted for every CONFIRMED |
| Report cap | 8 findings | 15 findings |

If the user names a subsystem or directory, restrict every phase to it plus one
layer of callers, and say so in the coverage section.

## Pipeline

Phase 1 (Map) runs first, alone — every hunter consumes its output. Phases 2–4
fan out as parallel subagents via the Agent tool. Phase 5 you assemble yourself.

---

## Phase 1 — Map the concurrent surface

Spawn ONE mapping agent with this prompt (fill `<root>`, `<scope note>`):

```
Inventory the concurrent surface of the codebase at <root>. <scope note>
Why: downstream hunters each drag one narrow lens across this map; anything
you omit is invisible to the whole hunt, so completeness beats commentary.

Find every SOURCE OF CONCURRENCY: threads/goroutines/worker pools, async
tasks and promise chains, event handlers/callbacks, timers and intervals,
queue/job consumers, signal handlers, subprocesses, request handlers that
can run concurrently.

Find every piece of SHARED MUTABLE STATE: module-level mutable variables,
singletons, caches, connection pools, global registries, class fields
touched by multiple handlers, files or DB rows written by more than one
path, localStorage/session state.

Return exactly this markdown:

## Concurrency sources
- <id> | <kind> | <file:line> | <what schedules it, max parallelism if knowable>

## Shared state
- <id> | <what it is> | <file:line> | touched by: <paths/functions> | synchronized by: <lock/transaction/queue/NOTHING>

## Async boundaries
- <file:line> | <what it awaits or defers> | ordering assumption: <what the code assumes about when this completes relative to what>

## Highest-risk items
Top 10 shared-state items ranked by (number of unsynchronized touching paths × blast radius). One line of reasoning each.
```

Keep the map; excerpt the relevant slice into each hunter prompt (quick: the
top-10 list plus its rows; deep: the whole map, split across hunters if huge).

## Phase 2 — Hunt (parallel, one subagent per lens)

Spawn the selected lenses in ONE message so they run concurrently. Shared
prompt skeleton — inject the lens block:

```
You are a concurrency bug hunter working ONE lens over the codebase at <root>.
Why: this lens targets bugs that pass tests because tests run one interleaving.
Do not report generic logic bugs, style, or hypotheticals outside your lens.

<concurrency map slice>

<LENS BLOCK>

For each candidate return:
- file:line
- state/resource involved (use map ids where possible)
- one-line summary
- interleaving sketch: step-by-step, two actors, ending in the wrong state,
  crash, leak, or corruption a user/operator would observe
- what real-world event causes the overlap (two requests, retry, slow network,
  double-click, deploy/shutdown, cron overlap)

Read the actual code before claiming anything. Up to 8 candidates; pass through
anything with a nameable interleaving — an independent verifier judges next.
Empty list if nothing qualifies.
```

Lens blocks:

**A — check-then-act / TOCTOU.** Read-check-write sequences on shared state
without atomicity: `if (map.has(k)) use(map.get(k))` across an await; DB
SELECT-then-UPDATE outside a transaction or without row locking;
exists-then-open on files; balance-check-then-debit; get-or-create without
upsert. The gap between check and act is where the second actor lands.

**B — missing/misplaced await & fire-and-forget.** Async calls whose result or
completion matters but is never awaited; promises dropped without `.catch`
(unhandled rejection, silent data loss); `forEach(async ...)`; try/catch around
an unawaited async call (the throw escapes the catch); awaits reordered so a
side effect happens before its precondition.

**C — lock discipline.** Lock scope smaller than the invariant it guards
(unlock between related writes); two locks acquired in different orders on
different paths (deadlock); locks/semaphores not released on error or early
return; awaiting while holding a lock that the awaited work needs.

**D — lifecycle & teardown.** Resources acquired but not released on ALL paths
(error paths especially): handles, connections, temp files, subscriptions.
Listeners/timers registered and never removed (leak + ghost callbacks).
Use-after-close/dispose. Startup ordering: module A reads state module B
initializes, with nothing enforcing order. Shutdown while in-flight work
exists — what happens to the half-done job?

**E — reentrancy & ordering.** Callbacks that can fire during the operation
that registered them; handlers assuming events arrive in order or exactly
once; retry racing the original request; the stale-response race (response A
returns after response B and overwrites fresher state); double-click/double
-submit reaching a non-idempotent action; state machines with an interleaving
no branch handles.

## Phase 3 — Verify (parallel, one subagent per finding)

Group candidates by (file, line); one verifier per location, all locations in
parallel. Verifier prompt:

```
Adversarially verify concurrency-bug candidate(s) at <file:line> in <root>.
Why: with no diff author to sanity-check findings, false positives are what
make whole-codebase hunts worthless — your default answer is REFUTED.

Candidates:
<numbered list: summary + interleaving sketch + claimed trigger>

For each, work the code yourself and return one verdict:

- CONFIRMED — you can write the exact interleaving: actor 1 does X
  (file:line), actor 2 does Y between X's steps (file:line), resulting state
  is Z, and Z is wrong/leaked/corrupt. AND the overlap is REACHABLE: name the
  real-world event that produces it. Timing-dependent is fine; imaginary
  actors are not — if only one caller can ever run this path, it is REFUTED.
- PLAUSIBLE — mechanism is real in the code, but reachability depends on
  config/deployment you cannot see (e.g. worker count, single- vs
  multi-process). State exactly what fact would settle it.
- REFUTED — default. Synchronization exists (quote it: lock, transaction,
  queue serialization, single-threaded event loop guarantee that actually
  covers the gap), the interleaving is impossible, or the claim misreads the
  code (quote the line).

Intent check for CONFIRMED/PLAUSIBLE: run git blame and read surrounding
comments/tests. If the code claims "single-threaded by design" or
"deliberately unsynchronized", verify that claim is ENFORCED somewhere —
an unenforced design assumption is still a finding, but say which it is.

Return per candidate: verdict, evidence (quoted lines), final interleaving
(CONFIRMED only), trigger event.
```

Drop REFUTED. Note that JS/Python event-loop code is not automatically safe:
every `await` is a yield point where another task interleaves — verifiers must
check what happens across the await, not whether "threads" exist.

## Phase 4 — Prove (deep only; parallel, one subagent per CONFIRMED)

```
Attempt a repro for: <finding + interleaving>.
Why: a finding with a failing test is a fix-ready ticket; one without is a claim.

Prefer, in order: (1) deterministic interleaving test — pause actor 1 at the
gap (injected hook, mocked awaitable, barrier) and run actor 2; (2) injected
delay at the gap plus concurrent invocation; (3) stress loop demonstrating
the failure at least intermittently. Put artifacts in <scratchpad>/repro-<n>/.

If none is practical without production infra, say so explicitly and instead
deliver the precise interleaving writeup plus a concrete suggested fix
(what to lock/await/transact, and the exact scope). Never fabricate a test
that doesn't actually exercise the race.
```

A finding with a repro outranks everything.

## Phase 5 — Report

Merge same-root-cause findings (one lock missing → many symptoms = one
finding). Rank: repro'd > CONFIRMED > PLAUSIBLE; within a tier, by blast
radius (data corruption > deadlock/crash > leak > stale UI). Cap per effort
level. Use exactly this template:

```markdown
# Concurrency hunt — <root> (<effort>)

## Summary
<2-3 sentences: what was mapped, what classes of race were found, overall risk>

## Findings

### 1. <one-line title> — <CONFIRMED+REPRO | CONFIRMED | PLAUSIBLE>
**Where:** <file:line> · **State:** <shared state involved> · **Trigger:** <real-world event>

| step | actor 1 | actor 2 |
|---|---|---|
| 1 | <action (file:line)> | |
| 2 | | <action (file:line)> |
| 3 | <action> → **<wrong state Z>** | |

**Consequence:** <what the user/operator observes>
**Fix direction:** <what to lock/await/transact, and scope>
**Repro:** <path to test/script, or "not practical because <reason>">

## Refuted candidates
- <file:line> — <claim> — refuted by <quoted guard/guarantee>

## Coverage
- Shared-state items audited: <n> of <m> mapped (unaudited: <ids>)
- Lenses run: <list> (skipped: <list + why>)
- Scope restriction: <none | subsystem X + one caller layer>
Absence of findings outside this coverage means UNEXAMINED, not clean.
```

The coverage section is not optional. A hunt that read six files must never
read as "the codebase is race-free".
