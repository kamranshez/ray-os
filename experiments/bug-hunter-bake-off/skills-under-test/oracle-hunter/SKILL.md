---
name: oracle-hunter
description: Hunt for real, user-reachable bugs in EXISTING code by running every cheap mechanical oracle available (test suite, type-checker at max strictness, linters, suppression-marker archaeology, dead-code detection), turning their output into a ranked lead list, then chasing each lead with hypothesis agents and adversarial verification. Use this whenever the user wants to "bug hunt", "find bugs in the codebase", "audit existing code for bugs", "see what the tests/types are hiding", "find what's silently broken", "check what the linters would catch", or asks where bugs are hiding in code that is already merged and running — even if they don't say "oracle". NOT for reviewing a diff, branch, or PR — that is /code-review. This skill targets code as it exists at HEAD, using tool output as the targeting signal.
---

# Oracle Hunter

Find bugs in existing code by letting cheap mechanical oracles point at them first, then spending expensive agent attention only where a tool already said something is off.

**Why this strategy works:** oracles (tests, type-checkers, linters, suppression markers) cost almost nothing to run and have a near-zero cost per lead generated. Every suppression marker in a codebase — `@ts-ignore`, `eslint-disable`, `# type: ignore`, a skipped test, an `unwrap()` — is a fossilized human judgment call: someone saw a warning and decided to silence it instead of fix it. Some of those calls were right. Some were deadline-driven guesses that are now live bugs. Re-litigating them is the highest-hit-rate reading you can do in a mature codebase, because a machine already did the finding; you only do the judging.

**Why verification is inverted here:** on a PR, a plausible-but-wrong finding is cheap — the author sanity-checks it in thirty seconds. Off-diff there is no author in the loop, so every false positive costs a real investigation. Findings therefore default to REFUTED and must earn their way up.

## Inputs

- **Target**: the repo (or subdirectory) to hunt in. Default: the current working directory.
- **Effort**: `quick` or `deep`. Default `deep` unless the user signals speed.
  - `quick` — Phase 1 runs only the test suite + grep archaeology; skip Phase 4 (Prove); chase at most 8 leads.
  - `deep` — all oracles, all phases, chase up to 20 lead clusters.

Announce the chosen effort level and target before starting so the user can redirect cheaply.

## Phase 1 — Run the oracles

Spawn ONE oracle agent (general-purpose subagent) with this prompt, filling in the target path and effort level:

```
You are the oracle phase of a bug hunt in <TARGET>. Your job is to produce LEADS from
mechanical tools, not to judge them. Why: agent reading time is expensive; tool output
is nearly free and points at real anomalies. Detect the stack (read package.json,
pyproject.toml, go.mod, Cargo.toml, etc.), then run every oracle below that applies
and capture its output. Never modify files; run everything read-only or in a throwaway
config file under the scratchpad.

Oracles (run all at deep effort; only #1 and #4 at quick effort):
1. TEST SUITE — run it fully. Record: failures, errors, AND every skipped/disabled/
   pending test (skip/xfail/it.skip/@Disabled/#[ignore]). A skipped test is a lead:
   someone turned off a safety check. Also grep test files for commented-out test
   bodies.
2. TYPE-CHECKER AT MAX STRICTNESS — if the codebase type-checks loosely, run it
   strict (tsc --strict via a temp tsconfig in the scratchpad, mypy --strict,
   pyright, etc.). Errors that appear only under strict mode on EXISTING code are
   leads: places the current config lets lies through.
3. LINTERS / STATIC ANALYZERS — run what's configured at max severity, plus any
   analyzer that runs with zero setup (ruff, eslint, go vet, cargo clippy,
   staticcheck). Only keep correctness-class rules; drop pure style.
4. SUPPRESSION ARCHAEOLOGY — grep for TODO, FIXME, HACK, XXX, @ts-ignore,
   @ts-expect-error, eslint-disable, type: ignore, noqa, #\[allow, unwrap(),
   expect(", panic!, unsafePerformIO, ! (TS non-null assertion, via `!\.` and `!)`
   patterns), catch blocks that swallow (catch {}, except: pass). Record file, line,
   the marker, and the code it silences.
5. DEAD CODE / UNUSED EXPORTS — run knip/ts-prune/vulture/deadcode if available,
   else grep exported symbols with no importers. Dead code adjacent to live code is
   a lead (the live path may have been meant to call it).
6. DEPENDENCY AUDIT — npm audit / pip-audit / cargo audit; also flag pinned
   versions with known-broken ranges mentioned in lockfile comments or changelogs
   you already know.

Then build the LEAD LIST:
- Deduplicate (one lead per root location, not per tool message).
- Cluster leads that share a file or an obvious theme (e.g. "all the ts-ignores in
  src/sync/") — each cluster is chased by one agent later.
- Rank by: (a) proximity to user-facing behavior, (b) how loud the oracle was,
  (c) age — blame a sample; old suppressions in hot files outrank fresh ones.

Return EXACTLY this structure (markdown):
## Stack
<one line>
## Oracles run
<oracle → one-line result summary, including "could not run: <why>" for each skipped oracle>
## Lead clusters (ranked)
For each: `[L<n>] <file(s)> — <signal> — <why this might hide a real bug>`
## Raw counts
<tests run/failed/skipped, strict errors, suppressions by type>
```

If an oracle needs a command that could mutate state (db migrations in test setup, network), note it as "could not run safely" rather than running it.

## Phase 2 — Chase the leads

Take the top lead clusters (8 at quick, 20 at deep). Spawn ONE hypothesis subagent PER CLUSTER, all in parallel, each with this prompt:

```
You are chasing one lead cluster in a bug hunt in <TARGET>.

Lead: [L<n>] <paste the cluster line + relevant raw oracle output>

Frame: an automated signal says something is off HERE. Your job is to determine
whether a real, user-reachable bug sits behind it. Why this matters: a suppression
is a warning a human chose to silence — ask what the warning was protecting
against, and whether that protection is actually unnecessary here, or whether the
author just made the message go away. For a skipped test: read the test, find why
it was skipped (blame the skip), and determine whether the behavior it covered
still works today. For a strict-mode type error: is the type lie ever actually
false at runtime, and what happens when it is?

Read the file(s), the callers of the affected code, and any tests that touch it.
Run git blame / git log on the suppression or skip to recover intent.

End with ONE of:
- CANDIDATE finding:
  file: <path>
  line: <n>
  summary: <one sentence — the defect>
  failure_scenario: <concrete input/state → wrong output, crash, or corruption a
    user or caller can hit>
  oracle: [L<n>] <the signal that led here>
- BENIGN: <one sentence — why no bug sits behind this signal. Cite the guard or
  invariant that makes it safe.>

Do not pad. One cluster can yield multiple candidates if genuinely distinct.
```

## Phase 3 — Verify (inverted ladder)

Pool all candidates. Spawn ONE independent verifier subagent PER CANDIDATE, in parallel. The verifier must NOT be told the chaser's confidence — only the claim:

```
You are an adversarial verifier in a bug hunt in <TARGET>. Default verdict is
REFUTED — a finding must earn its way up. Why: there is no PR author to cheaply
sanity-check this claim, so a false positive costs a real investigation.

Claim:
<file / line / summary / failure_scenario / oracle>

Do all of:
1. Read the code and its callers. Check the claim is factually what the code says.
2. TRIGGER PATH: to reach CONFIRMED you must name a concrete path from a real
   entry point (HTTP route, CLI command, job, exported API) to this line with the
   bad input/state, and the observable wrong result. "Could theoretically" is not
   a path.
3. INTENT CHECK: git blame the line and read surrounding comments and tests. If
   the behavior is deliberate and load-bearing (a test asserts it, a comment
   explains it), that is REFUTED-as-bug even if surprising — note it as
   intentional.

Verdicts:
- CONFIRMED — trigger path written out end to end, wrong result named.
- PLAUSIBLE — mechanism is real and unguarded, but the trigger depends on state
  you cannot prove reachable (race timing, prod-only config). Say exactly what
  would confirm it.
- REFUTED — default. Quote the guard, type, invariant, or intent evidence.

Return: verdict, then 3-6 lines of evidence quoting the decisive code.
```

Drop REFUTED findings from the report body (keep a one-line list at the end for honesty).

## Phase 4 — Prove (deep effort only)

For each CONFIRMED finding, spawn one repro subagent. Exploit this skill's natural edge: many leads are nearly repros already — un-skip the skipped test and run it; delete the `@ts-ignore` and show the compiler error corresponds to a runtime failure; write the 5-line script that calls the entry point from the trigger path.

```
Write a MINIMAL failing test or repro script for this confirmed bug, in the
project's own test framework where possible: <finding + trigger path>.
Put new files in <scratchpad>/repro/ — do not modify project files except to
temporarily un-skip an existing test (revert after running). Run it. Return: the
repro file path, the command, and the observed failing output. If you cannot make
it fail, say so plainly — that demotes the finding to PLAUSIBLE.
```

A finding with a passing repro (i.e. the repro fails as predicted) outranks everything else in the report.

## Phase 5 — Report

Use EXACTLY this template:

```markdown
# Oracle Hunt — <target> (<effort>)

## Verdict summary
<2-3 sentences: what the oracles found, how many leads survived verification.>

## Findings (ranked: repro'd > CONFIRMED > PLAUSIBLE)
### 1. <file>:<line> — <summary> [CONFIRMED, repro'd]
- Oracle: [L<n>] <signal>
- Failure: <failure_scenario>
- Trigger path: <entry point → ... → line>
- Repro: <path + command + failing output line>   <!-- omit if none -->
- Suggested fix: <one line>

## Benign signals worth cleaning up anyway
<suppressions/skips verified safe but rotting — one line each. These are hygiene, not bugs.>

## Refuted
<one line per refuted candidate — claim + the guard that kills it>

## Coverage — read this before trusting the findings
- Oracles run: <list>. Oracles unavailable: <list + why>.
- Leads generated: <n>. Chased: <n>. Left on the table: <n> (listed: ...).
- This hunt saw ONLY what the oracles pointed at. Silence here is not evidence of
  absence — code with no tests, no types, and no suppressions is invisible to this
  strategy.
```

The coverage section is mandatory and honest. Why: a lead-driven hunt reads a biased sample of the codebase; without the ledger, "5 findings" reads as "only 5 bugs exist", which is false.
