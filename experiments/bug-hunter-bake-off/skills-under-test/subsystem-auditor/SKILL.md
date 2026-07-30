---
name: subsystem-auditor
description: Deep bug audit of ONE subsystem of an existing codebase — its files plus the callers/callees at its edge — using parallel finder angles, adversarial verification, and repro tests. Use whenever the user wants to hunt for bugs in code that is NOT a fresh diff or PR: "audit the auth system", "deep review of the payments module", "bug hunt in the sync engine", "go through src/api and find bugs", "is this subsystem solid", "review this whole directory", "find latent bugs in X", or any request to adversarially read an area of existing/legacy code. Also trigger when the user names a directory or feature area and asks "what's broken in here". Do NOT use for reviewing a diff, branch, or pull request — that is /code-review.
---

# Subsystem Auditor

Audit one subsystem of an existing codebase for real, latent bugs. This is
whole-file bug hunting, not diff review, and the difference changes everything
about how strict you must be:

- **No author will answer your findings.** On a PR, a plausible-but-wrong
  finding costs the author thirty seconds. Here, every finding lands in a
  backlog with no one to sanity-check it, so a false positive costs an
  engineer an investigation. Verification must therefore be *stricter* than
  diff review, not looser.
- **No PR description supplies intent.** The code has survived production, so
  much of what looks wrong is deliberate. You must reconstruct intent
  (READMEs, docstrings, tests, git blame) before judging code against it.
- **The scope is not self-bounding.** A diff bounds itself; a subsystem does
  not. You must emit an explicit audit set up front and account for coverage
  at the end, or the report will read "clean" when it means "barely looked".

Run five phases: **Scope → Find → Verify → Prove → Synthesize**.

## Effort levels

| Level | Finder angles | Repro phase | Report cap |
|-------|--------------|-------------|------------|
| `quick` | A, C, D | skipped | 8 findings |
| `deep` (default) | A, B, C, D, E | yes, per CONFIRMED | 15 findings |

The user can say "quick audit" or "deep audit"; default to `deep` when unstated.

---

## Phase 1 — Scope

**If the user named a subsystem** ("auth", "payments", `src/sync/`), resolve it
to concrete directories/files.

**If not**, spend a short pass mapping the repo (entry points, money/data/auth
paths, largest and most central modules), propose the 3 highest-stakes
subsystems with one line each on why, and ask the user to pick via
AskUserQuestion. Do not audit the whole repo — an unbounded audit produces an
unaccountable report.

Then spawn one **scope agent** to build the audit set. Its prompt must ask for:

1. **Core files** — every file in the subsystem, listed with line counts
   (`wc -l`). If the core exceeds ~8,000 lines, split the file list into
   shards of roughly equal line count for the finders.
2. **Edge layer** — one layer of external callers and callees: Grep for each
   symbol the subsystem exports, list the out-of-subsystem files that use
   them, and note which exported symbols each edge file touches. The edge
   layer is read for *contract* checking, not line-by-line audit.
3. **Intent summary** — one paragraph per major component describing what the
   subsystem is *supposed* to do, reconstructed from READMEs, doc comments,
   test names, and type signatures. This substitutes for the missing PR
   description: every downstream agent judges the code against this summary,
   not against its own guesses.
4. **Conventions** — the CLAUDE.md files that govern these paths (user-level,
   repo root, any ancestor directory of a core file), plus language/framework
   and test-runner facts a finder needs (how to run one test file, fixtures).

Assemble the result into a `SCOPE_BLOCK` that is pasted verbatim into every
finder, verifier, and prover prompt:

```
## Audit scope
Subsystem: <name>
Core files (<n>, <total> lines): <path — lines> per line
Edge layer (<n> files): <path — symbols used> per line
## Intent
<intent summary>
## Conventions
<notes + applicable CLAUDE.md paths>
## User instructions (verbatim, if any)
<focus/skip requests — these take precedence over angle defaults>
```

## Phase 2 — Find

Spawn one finder agent per angle, all in a single message so they run in
parallel. Each finder reads the **core files in full** (Read whole files, not
excerpts), consults the edge layer as its angle requires, and returns up to
**10 candidates** as structured output:

```
file: <repo-relative path from the Core files list>
line: <number>
summary: <one line>
failure_scenario: <concrete user-visible consequence — wrong output, crash,
                   data loss, security hole — not an intermediate state>
trigger_sketch: <entry point → call path → input/state that reaches the line>
```

Require the `trigger_sketch` from finders (not just verifiers): forcing the
finder to sketch a path kills most hallucinated candidates at the source.
Candidates with a nameable failure scenario all pass through — the verifier
judges them, the finder should not silently drop half-believed ones. Empty
list is a valid answer; padding is not.

### Angle A — adversarial line-by-line read

Read every core file top to bottom. For each line ask: what input, state,
timing, or platform makes this line wrong? Hunt inverted conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, swallowed errors, unescaped regex metachars,
integer overflow, encoding assumptions. Judge against the Intent summary —
code that contradicts its own documented purpose is a candidate even when it
"works".

### Angle B — contract auditor (deep only)

For each function/type the subsystem exports: derive its *actual* contract
from the implementation (preconditions it assumes, error modes it can raise,
return shapes including edge cases like empty/None/rejected). Then check every
edge-layer call site against that contract: callers passing unvalidated input
to a function that assumes validated; callers ignoring an error return;
callers depending on a behavior the implementation does not guarantee
(ordering, non-null, idempotency). Also check the reverse: does the subsystem
honor what its own docstrings/types promise to callers?

### Angle C — state & lifecycle

Trace shared mutable state through its lifetime: init/teardown asymmetry
(opened but not closed on the error path, registered but never unregistered),
caches that can serve stale entries after the underlying data mutates, leaked
handles/timers/listeners, invariants that hold after some mutation paths but
not others, re-entrancy and concurrent-mutation hazards on anything reachable
from two contexts. For every invariant the Intent summary implies, find each
write site and check the invariant is re-established.

### Angle D — language/framework-pitfall specialist

Scan for the classic pitfalls of this codebase's language and framework — e.g.
JS falsy-zero, `==` coercion, closure-captured loop vars, unhandled promise
rejection; Python mutable default args, late-binding closures; Go nil-map
write, range-var capture; SQL injection; timezone/DST drift; float equality;
ORM N+1 that changes semantics under lazy loading. Flag only live instances in
the core files, with the concrete input that trips them.

### Angle E — test-gap auditor (deep only)

Inventory the behaviors the subsystem *claims* (doc comments, function names,
Intent summary) and map each to the test files that cover it. For claimed
behaviors with no coverage, read the untested path adversarially — untested
branches are where live bugs hide, because nothing has ever forced them to
run. A test gap alone is a low-rank finding; a test gap *concealing a
demonstrable bug* is a full candidate with the bug as the finding.

## Phase 3 — Verify

Normalize candidate paths against the Core files list (suffix-match, longest
wins), group candidates by `(file, line)`, and spawn **one verifier per
location** (parallel), each receiving the SCOPE_BLOCK and its location's
candidates labeled `[0]..[n]`, returning one verdict per candidate.

Use the **inverted ladder**. Diff review defaults to PLAUSIBLE because a cheap
author-check absorbs false positives; here there is no author, so the default
is REFUTED and the burden of proof sits on the candidate:

- **REFUTED (default)** — the verdict when proof of a trigger cannot be
  constructed. Includes: factually wrong (quote the actual line); guarded
  upstream (cite the guard); unreachable input (show the validation/type that
  excludes it); *intentional* — git blame the line and read surrounding
  comments and tests; if a test asserts this exact behavior or the commit
  message explains it, the code is deliberate and the candidate dies.
- **PLAUSIBLE** — a real mechanism plus a *named* concrete trigger the
  verifier could not fully walk (needs a specific env, config, or timing that
  exists but couldn't be confirmed from code alone). State exactly what would
  confirm it. "Depends on runtime state" with no named trigger is REFUTED,
  not PLAUSIBLE.
- **CONFIRMED** — the verifier walked a concrete path: real entry point →
  call chain (name each hop) → the line, with the specific input/state that
  makes it misbehave, and quotes the line. No walked path, no CONFIRMED.

Verifiers must Read the actual files and run `git log -L` / `git blame` for
the intent check — verdicts from the candidate text alone are invalid. A
candidate whose verifier died or omitted its index is dropped, never passed
through unverified.

## Phase 4 — Prove (deep only)

For each CONFIRMED finding, spawn a prover agent (parallel, one per finding)
to produce a **failing test or minimal repro** using the project's own test
runner (from Conventions):

- Write the test in a scratch location or clearly-marked new test file; run
  it; capture the failing output verbatim.
- The test must fail *because of the bug* (assert the correct behavior) — not
  a test asserting the buggy behavior passes.
- If the prover cannot make it fail after an honest attempt, **downgrade the
  finding to PLAUSIBLE** and record why (env dependency, unreachable in test
  harness). This is the point of the phase: repro is the only oracle that
  cannot be argued with.

Report reproduced findings with the test path and the failing output snippet.

## Phase 5 — Synthesize

1. **Merge** findings that share a root cause (one primary, others listed as
   "also at"). Escalate the merged verdict to the strongest member's.
2. **Rank**: reproduced > CONFIRMED > PLAUSIBLE; within a tier, data
   loss/security > wrong output > crash > degraded behavior. Cap at the
   effort level's limit; say how many were cut.
3. **Report** using exactly this template:

```markdown
# Subsystem audit: <name> (<effort>)

<2-3 sentence summary: what was audited, headline findings, overall risk read>

## Findings

### 1. <file>:<line> — <one-line summary> [REPRODUCED|CONFIRMED|PLAUSIBLE]
- **Failure**: <user-visible consequence>
- **Trigger**: <entry point → path → input>
- **Evidence**: <quoted line(s) / verifier citation>
- **Repro**: <test path + failing output snippet, or "not attempted (quick)" / "could not reproduce: <why>">
<repeat, ranked>

## Refuted (for the record)
- <file>:<line> — <summary> — <one-line refutation>

## Coverage
- Fully read: <n> files (<lines> lines) — <list or "all core files">
- Skimmed only: <list, or none>
- Not examined: <list, or none>
- Edge layer checked: <n>/<n> files
- Angles run: <list>

## Stats
finders: <n> · candidates: <n> · verified: <n> · confirmed: <n> ·
reproduced: <n> · refuted: <n>
```

The Coverage section is not optional. An audit that silently skipped files
reads as "the subsystem is clean" when it means "we didn't look" — name what
was not examined so the user can commission a follow-up shard.

Never edit non-test code during an audit; findings are the deliverable, fixes
are a separate, user-approved task.
