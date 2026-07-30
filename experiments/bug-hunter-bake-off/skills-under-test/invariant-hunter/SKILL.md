---
name: invariant-hunter
description: Hunt for real bugs in EXISTING code by deriving codebase-specific invariants and sweeping the entire tree for violations, then adversarially verifying and reproducing each finding. Use this whenever the user wants to "bug hunt", "find bugs in existing code", "audit the codebase for bugs", "do an invariant sweep", "find latent bugs", "hunt for defects", "what's broken in this repo", "security/correctness audit of the whole codebase", or any request to find defects in code that is NOT a fresh diff. Trigger even if the user doesn't say "invariant" — any whole-codebase or subsystem-wide bug-finding request belongs here. Do NOT use for reviewing a diff, branch, or PR — that is /code-review; this skill assumes the code already shipped and has no author waiting to sanity-check findings.
---

# Invariant Hunter

Find real, unshipped-report-worthy bugs in existing code by sweeping the whole
tree with **one narrow lens at a time**.

## Why this shape

Diff review works because the diff concentrates bugs and comes with an author
who can cheaply confirm or dismiss each finding. Existing code has neither:
bugs are diluted across code that has mostly survived production, and every
false positive costs a real investigation because nobody has the context
loaded. Two consequences drive everything below:

1. **Sweep by invariant, not by area.** "Read this directory and find bugs" is
   a wide lens on a slice — it produces vague, unverifiable suspicions. "Find
   every DB write outside a transaction, everywhere" is a narrow lens across
   everything — each candidate has a crisp pass/fail test, which is what keeps
   the false-positive rate survivable without an author in the loop.
2. **Verification is inverted.** In diff review, verifiers default to keeping
   plausible findings because checking them is cheap. Here the default verdict
   is REFUTED, and a finding must EARN its way up by naming a concrete trigger
   path. A bug report without a trigger is a suspicion, not a finding.

A third rule follows from sweeping a codebase instead of a self-bounding diff:
**account for coverage explicitly**. Without it, "we examined six files" reads
as "the codebase is clean." Every report states what was and wasn't examined.

## Effort levels

Ask which level the user wants if not stated; default to `deep` when they say
"audit" or "thorough", `quick` otherwise.

| | quick | deep |
|---|---|---|
| Invariants swept | top 5 | 8–15 |
| Verify | 1 verifier per finding | 1 verifier per finding + intent check |
| Prove (repro) phase | skipped | run for every CONFIRMED |
| Report cap | 10 findings | 20 findings |

## Pipeline

Five phases: **Map → Sweep → Verify → Prove → Report**. Run finder subagents
in parallel (single message, multiple Agent calls). Each phase's subagent
prompt is given below — use them verbatim, filling the `{...}` slots.

### Phase 1 — Map

Spawn ONE mapping agent. Its job is not to find bugs; it is to make the sweep
possible: derive invariants worth checking and a partition to account coverage
against.

```
Survey the codebase at {root} to prepare a bug-hunting sweep. Do not look for
bugs yet.

Why: downstream finder agents will each sweep the ENTIRE tree for violations
of ONE invariant. Your invariants must therefore be (a) checkable — a grep
pattern or a short read of each hit decides pass/fail, (b) specific to THIS
codebase's stack and idioms, not generic advice, (c) load-bearing — violating
them plausibly produces a user-visible failure (crash, data loss, wrong
output, security hole).

1. Identify: language/stack, entry points (CLI, HTTP routes, cron, queue
   consumers, event handlers), trust boundaries (where external input
   enters), IO surfaces (DB, network, filesystem, subprocess), shared mutable
   state, and concurrency points (threads, async tasks, locks, signals).
2. Derive a ranked list of {n_invariants} checkable invariants. Good shapes:
   "every X is always Y", "no X ever reaches Y without Z", "every acquired X
   is released on all paths". For each: a one-line statement, WHY violating
   it hurts here, and 1–3 concrete grep patterns or search strategies a
   finder should start from.
3. Emit a file partition: group every non-vendored source file into 5–12
   named buckets (by subsystem/directory). This is the coverage ledger.

Return exactly this structure:

## Stack & surfaces
<one paragraph>

## Entry points
- <path> — <what enters here>

## Invariants (ranked)
### I1: <statement>
Why it matters: <one line>
Search strategy: <grep patterns / where to look>
(repeat for each)

## Partition
### B1: <bucket name>
- <file paths or globs>
(repeat for each)
```

If the user scoped the hunt ("only the sync engine", "focus on auth"), pass
that scope into the mapper and let it derive invariants for that slice — but
the partition must still name what is OUT of scope, so the report can say so.

### Phase 2 — Sweep

Spawn ONE finder agent PER invariant, all in parallel. Each drags its single
lens across the whole tree.

```
You are a bug-finder sweeping an entire codebase for violations of exactly ONE
invariant. Root: {root}

Why: a narrow lens across everything beats a wide lens on a slice — your
single invariant gives every candidate a crisp pass/fail test. Do not report
anything outside your invariant, even if you notice it; another finder owns it.

## Your invariant
{invariant statement}
Why it matters: {why}
Search strategy: {strategy}

## Codebase context
{stack & surfaces paragraph}
Entry points:
{entry points list}

## File partition (coverage ledger)
{partition}

Method: start from the search strategy's grep patterns, then Read each hit's
enclosing function to decide whether the invariant actually holds there.
Widen the grep if the idiom varies. Check every bucket of the partition, or
record which buckets you could not examine.

For each violation, return:

### Candidate
File: <repo-relative path>
Line: <number>
Invariant: {invariant id}
Claim: <one line — what the code does that violates the invariant>
Failure scenario: <the concrete user-visible consequence: which input/state/
timing produces which error, data loss, or wrong output. Not an intermediate
state.>
Confidence: high | medium | low

Report up to {cap} candidates — pass through everything with a nameable
failure scenario; an independent verifier judges them next. Then ALWAYS end
with:

### Coverage
Examined buckets: <list>
Not examined / partially examined: <list, with why>
```

Cap: 8 candidates per finder (quick), 12 (deep). Collect all candidates and
all coverage reports before Phase 3.

### Phase 3 — Verify

Group candidates by (file, line); spawn ONE verifier per distinct location,
in parallel. The ladder is inverted relative to diff review — and say so in
the prompt, because agents trained on review habits will over-keep.

```
You are an adversarial verifier for bug candidates in EXISTING code at {root}.

Why inverted verification: this code shipped; there is no author to cheaply
sanity-check findings, so every false positive costs a real investigation.
Your DEFAULT verdict is REFUTED. A candidate must earn its way up.

## Candidates at {file}:{line}
[i] Claim: ... / Failure scenario: ...
(one block per candidate at this location)

Judge each candidate independently:

- **CONFIRMED** — you constructed a concrete trigger: an actual call path
  from a real entry point ({entry points}) that reaches this line with the
  bad input/state, ending in the claimed failure. Name the path
  (entryFn → f → g → this line) and the triggering input. Quote the code.
- **PLAUSIBLE** — the mechanism is real and the code truly lacks the guard,
  but the trigger depends on state you cannot construct from the code alone
  (race timing, external config, data shape). State exactly what would
  confirm it.
- **REFUTED** — default. The claim misreads the code, a guard exists
  elsewhere (cite it), the "bad" input cannot reach here (show the barrier),
  or the effect is not user-visible.

Intent check (mandatory for CONFIRMED/PLAUSIBLE): run git blame on the line,
read surrounding comments and any test that pins this behavior. If the
behavior is deliberate and load-bearing (a comment, a test asserting it, a
commit message explaining it), downgrade to REFUTED and say "intentional:
<evidence>". Old code often looks wrong because it encodes a lesson.

Return per candidate:
[i] VERDICT — evidence (quote lines; for CONFIRMED include the trigger path)
```

Drop REFUTED candidates from the report body (keep a count). In `quick`
mode, skip the intent check sentence but keep the inverted ladder.

### Phase 4 — Prove (deep only)

For each CONFIRMED finding, spawn a repro agent (parallel, one per finding):

```
Write a minimal failing test or repro script for this confirmed bug.
Root: {root}

Bug: {file}:{line} — {claim}
Trigger path: {verifier's trigger path}
Failure scenario: {failure scenario}

Why: a repro converts a claim into a fix-ready artifact and is the final
filter against false positives — if you cannot make it fail, say so honestly.

1. Prefer a failing test in the repo's existing test framework, placed under
   the repo's test layout but NOT committed. Otherwise a standalone script.
2. RUN it. Paste the actual failing output.
3. If you cannot get it to fail, report REPRO-FAILED with what you tried —
   do not fake a failure. The finding will be downgraded to PLAUSIBLE.

Return: repro file path, the command to run it, and the observed output.
```

A finding with a passing (i.e., correctly failing) repro is ranked above all
non-reproduced findings. REPRO-FAILED downgrades CONFIRMED → PLAUSIBLE.

### Phase 5 — Report

Assemble inline (no subagent needed). Merge candidates that share a root
cause. Rank: reproduced > CONFIRMED > PLAUSIBLE; within a tier, by severity
of failure scenario. Cap per effort level; say how many were cut.

Use exactly this template:

```markdown
# Bug hunt — {root} ({effort} effort)

## Summary
<2–3 sentences: invariants swept, candidates found, what survived, headline bugs>

## Findings

### 1. <one-line title> — REPRODUCED | CONFIRMED | PLAUSIBLE
**Where**: `file:line`
**Invariant violated**: I<n> — <statement>
**Claim**: <what the code does wrong>
**Trigger**: <entry point → ... → line, with the triggering input>
**Failure**: <user-visible consequence>
**Repro**: `<path>` — `<command>` (deep only; omit row if none)
**Evidence**: <verifier's quoted lines>

(repeat, ranked)

## Coverage
| Bucket | Examined by | Not covered |
|---|---|---|
| <bucket> | I1, I3, I7 | — |
| <bucket> | I2 | I5 skipped it (reason) |

**Invariants swept**: <list>
**Not swept**: <invariants the mapper ranked but effort level cut>
**Verdict counts**: <n> candidates → <n> refuted, <n> plausible, <n> confirmed, <n> reproduced

## Honest limits
<what this hunt cannot claim: unexamined buckets, invariants not derived,
dynamic behavior (races, prod config) that static sweeping cannot see>
```

The Coverage and Honest limits sections are not optional decoration — they
are what makes a clean-looking report trustworthy. If nothing was found, the
report's value IS the coverage table.

## Guardrails

- Never edit or commit code during a hunt; repro files live in the scratchpad
  or an untracked test path, and say so in the report.
- Skip vendored/generated code (node_modules, dist, lockfiles, migrations
  that are historical records) — note the exclusion in the partition.
- If the repo is too large to partition meaningfully (>~5k source files),
  tell the user and ask them to scope to a subsystem rather than silently
  sampling.
- If the user hands you a diff, branch, or PR, redirect to /code-review —
  this skill's verification bias is wrong for pre-merge review.
