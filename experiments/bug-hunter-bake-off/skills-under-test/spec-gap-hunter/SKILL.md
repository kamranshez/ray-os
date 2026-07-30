---
name: spec-gap-hunter
description: Hunt bugs of OMISSION in an existing codebase by reconstructing its implied spec and auditing every claim against the code. Finds the missing bounds check, the unhandled enum case, the documented-but-absent error path, the config flag that is read but never applied. Use whenever the user wants a bug hunt on existing code framed around promises vs. reality — "does the code do what the docs say", "find missing edge cases", "what's promised but not implemented", "audit the docs against the code", "find unhandled cases", "bug hunt", "find bugs in this codebase" — even if they don't say "spec". NOT for reviewing a diff, branch, or PR; that is /code-review. This skill reviews code as it exists at HEAD, whole.
---

# spec-gap-hunter

Find bugs that diff review is structurally blind to: **sins of omission**. A diff can only show what's there; this skill hunts what *should* be there and isn't. You can't grep for absent code — but you *can* enumerate every promise the codebase makes and check each one. That turns an unbounded search ("find missing code") into a finite checklist ("verify 80 claims").

The pipeline: **Reconstruct the spec → Audit claims → Verify (inverted) → Prove → Report.**

Why verification is inverted here: on a PR, a plausible-but-wrong finding costs the author thirty seconds to dismiss. Off-diff there is no author with the change loaded in their head — every false positive costs a cold investigation. So findings are guilty until proven reachable.

## Arguments

`/spec-gap-hunter [quick|deep] [path or focus area]`

- **quick** (default when unspecified on large repos): mine only sources (a) docs and (b) names/types; skip Phase 4 (Prove). ~6-10 agents.
- **deep**: all four evidence sources, full verification, repro tests for CONFIRMED findings.
- Optional path/focus narrows every phase to that subtree plus its docs and tests.

## Phase 1 — Reconstruct the spec

The codebase constantly makes behavioral claims; most are never checked after the day they were written. Spawn **one extractor subagent per evidence source, in parallel** (sources a+b for quick; a-d for deep). Each returns a claim list in the ledger format below.

Extractor prompt template (fill `{SOURCE}` sections):

```
You are a claim extractor for a spec-gap bug hunt on the repo at {ROOT}.
Why this matters: each claim you extract becomes a checklist item another
agent will audit against the code. Vague claims waste an audit; miss a claim
and its bug is never found. Extract only claims that are CHECKABLE — a
specific behavior under specific conditions.

{SOURCE}

For every claim, return one ledger row:
- claim: one sentence, testable ("X returns sorted results", "Y raises on
  invalid input", "Z is idempotent")
- source: file:line (or doc section) where the promise is made
- responsible_code: file(s)/function(s) that must honor it (Grep to locate;
  if you cannot locate the responsible code, say "UNLOCATED" — that itself
  is signal)
- strength: EXPLICIT (stated in words) | IMPLIED (by a name, type, or test)

Return a markdown table of rows, nothing else. Cap at 40 rows; prefer claims
about error handling, limits, concurrency, and data integrity over cosmetic
behavior. If a source yields nothing, return an empty table.
```

The four `{SOURCE}` blocks:

- **(a) Docs & comments**: README, API docs, docstrings, inline comments. Hunt phrasings like "returns X when Y", "raises/throws on Z", "idempotent", "thread-safe", "at most once", "sorted", "case-insensitive", "defaults to", "never", "always", "guaranteed".
- **(b) Names & types**: identifiers are promises. `retryWithBackoff` claims backoff; `NonEmptyList` claims non-emptiness; `sanitizeHtml` claims sanitization; an enum/union with 5 variants claims all 5 are handled at every switch; `*Safe`, `*Atomic`, `*Cached`, `ensure*`, `validate*` all claim their adjective.
- **(c) Tests**: every test name and assertion is a claim about current behavior. Also record the *inverse*: documented behaviors (cross-check source a's output if available, else obvious doc claims) with NO test — absence of a test is where regressions hide, and often where the behavior was never implemented at all.
- **(d) User-facing surface**: UI strings, error messages, CLI `--help` text, config options. "Your data is saved automatically" is a claim. A `--timeout` flag claims the timeout is enforced; a config key claims it is both read AND applied.

Merge the tables into one numbered **CLAIM LEDGER**, dedup near-identical claims (keep the strongest source), and cluster rows that share responsible code — clusters become audit units.

## Phase 2 — Audit claims

Spawn **one auditor subagent per claim cluster, in parallel** (batch clusters so no auditor gets more than ~8 claims). Auditor prompt template:

```
You are a claim auditor for a spec-gap bug hunt on the repo at {ROOT}.
Why this matters: you are checking whether the code keeps promises it makes
elsewhere. The bugs you are hunting are OMISSIONS — code that is absent or
incomplete — which no diff reviewer ever saw, because you cannot diff
against code that was never written.

Claims to audit (from the ledger):
{CLAIM_ROWS}

For each claim: Read the responsible code in full (the whole function/module,
not a snippet), then judge:
- HONORED — the code fully implements the claim. Say where.
- PARTIAL — honored on the main path but specific cases fall through. Name
  the exact cases.
- FALSE — the claim is not implemented at all, or the code does the opposite.

Pay special attention to the classic omission patterns:
- enum/union exhaustiveness: a variant added later that older switches
  silently ignore or default away
- documented error paths that are unimplemented, or implemented but swallowed
  (caught and discarded)
- edge cases the docs NAME but the code ignores: empty input, missing field,
  unicode, zero, negative, max limits
- config options read but never applied, or applied but never read
- "validate*/sanitize*/ensure*" functions with a bypass path that skips them

For every PARTIAL or FALSE, emit a candidate finding:
- claim + source (from the ledger row)
- gap: exactly what is missing or wrong, with file:line of where the missing
  code SHOULD live
- failure_scenario: the user-visible consequence (wrong output, crash, data
  loss, silent misconfig) — not an intermediate state

Return a markdown list of candidate findings. If everything is HONORED,
return "NO FINDINGS" — do not pad.
```

## Phase 3 — Verify (inverted ladder)

Spawn **one verifier subagent per candidate finding, in parallel**. Verifiers get the finding but NOT the auditor's reasoning — independence is the point.

```
You are an adversarial verifier in a spec-gap bug hunt on {ROOT}. Default
verdict is REFUTED — your job is to kill this finding. It survives only if
you fail. Why: there is no PR author to cheaply sanity-check findings here,
so a false positive costs a cold investigation; the report is only useful
if every surviving finding is real.

Candidate: {FINDING}

Two hurdles, in order:
1. Is the claim real and CURRENT? Run git log/blame on the claim's source
   and the responsible code. If the doc/comment describes removed or changed
   behavior, the finding is a STALE-DOC finding (lower severity, different
   bucket) — not a code bug. Do not inflate stale docs into code bugs.
2. Is the gap REACHABLE? To confirm, name a concrete input or state,
   entering at a real entry point (route, CLI command, job, public API),
   that exercises the missing behavior and produces the failure scenario.
   Trace the actual call path in the code — file:line at each hop.

Also run the intent check: git blame + surrounding comments + tests on the
gap location. If the omission is deliberate and load-bearing (e.g. a comment
explains why the case is impossible), REFUTE and quote the evidence.

Verdicts:
- CONFIRMED — reachable; you wrote out the trigger path. Include it.
- PLAUSIBLE — mechanism real, reachability uncertain (needs specific config,
  race, or environment). State exactly what would confirm it.
- STALE-DOC — the documentation is what's wrong. Say what the doc should say.
- REFUTED — quote the line(s) that prove the claim is honored, the gap
  unreachable, or the omission intentional.

Return: verdict, evidence (quoted lines with file:line), and for CONFIRMED
the full trigger path.
```

## Phase 4 — Prove (deep mode only)

For each CONFIRMED finding, spawn a repro subagent: *"Write a failing test that demonstrates this finding, using the repo's existing test framework and conventions. The claim is the assertion; the trigger path is the setup. Place it under the repo's test tree but DO NOT commit. Run it and paste the failure output. If you cannot make it fail, report that — the finding gets downgraded to PLAUSIBLE."*

This phase is the honest fix for off-diff credibility: it converts each finding from a claim into a fix-ready artifact, and it catches verifier mistakes (a "CONFIRMED" that can't be reproduced wasn't confirmed).

## Phase 5 — Report

Assemble exactly this template. Rank: repro'd > CONFIRMED > PLAUSIBLE; within a tier, by severity of failure_scenario. STALE-DOC findings go in their own section — they are real deliverables (someone will trust that doc) but never mixed with code bugs.

```markdown
# Spec-Gap Hunt — {repo} @ {commit}

## Summary
{2-3 sentences: claims audited, gaps found, the single worst finding.}

## Code bugs ({n})
### 1. {one-line summary} — {CONFIRMED+repro | CONFIRMED | PLAUSIBLE}
- **Claim**: "{claim}" ({source})
- **Gap**: {what's missing} ({file:line})
- **Failure**: {user-visible consequence}
- **Trigger**: {entry point → path → failure; or what would confirm it}
- **Repro**: {test path + failure output, if proven}

## Stale docs ({n})
### 1. {doc location} — says {X}, code does {Y} since {commit}

## Coverage — read this before trusting the summary
- Evidence sources mined: {a,b,c,d — which ran, which were skipped and why}
- Claim ledger: {N} claims extracted, {M} audited, {N-M} NOT audited: {list}
- Areas of the codebase no claim pointed at (and therefore NOT examined): {dirs}
- Refuted candidates: {count} ({one line each — they document dead ends})
```

The coverage section is mandatory and honest. A spec-gap hunt only examines code that some claim points at; silence about a module means *no promise mentioned it*, not *it is clean*. Never let the report read as a clean bill of health for code the hunt never touched.

## Operating notes

- Run extractors, auditors, and verifiers as parallel subagents (Agent tool); each phase's outputs feed the next. Keep per-agent scope small enough that every responsible-code read is a FULL read — skimming is how omissions survive.
- If the ledger exceeds ~60 claims in quick mode, audit the top 40 by strength (EXPLICIT first) and list the deferred ones in Coverage.
- UNLOCATED responsible code from Phase 1 is itself reportable: a documented feature whose implementation cannot be found is either dead docs or a missing feature — send it straight to a verifier.
- Never edit repo files except repro tests in Phase 4, and never commit anything.
