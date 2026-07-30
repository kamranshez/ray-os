---
name: divergence-hunter
description: Hunt for bugs in an existing codebase by finding places that implement the SAME concept more than once (duplicated validation, twin calculations, copy-paste siblings, encode/decode pairs, constants defined in two layers) and diffing the copies — disagreement between twins means at least one is wrong, no spec required. Use this skill whenever the user wants a bug hunt on existing code, asks to "find bugs", "find inconsistencies", "audit for drift", "why do these two places disagree", "check for duplicate logic drift", "client and server don't match", or wants a whole-codebase sweep rather than a change review. NOT for reviewing a diff, branch, or PR — that is /code-review. Trigger this even if the user never says "divergence": any request to find latent bugs in code that already shipped is a fit.
---

# divergence-hunter

Find bugs by exploiting a rare free oracle: **when a codebase implements the same concept in two or more places, disagreement between the copies proves a bug in at least one of them — without you ever needing to know the spec.** This is poor-man's N-version programming. Independent copies that agree are weak evidence of correctness; copies that disagree are strong evidence of a defect, because both cannot be right about the same requirement.

Why this works off-diff where ordinary review struggles: reviewing cold code normally requires reconstructing intent from scratch, which produces confident false positives. Here the *other twin* is the spec. Every finding arrives pre-anchored to a concrete disagreement you can point at, which keeps precision high even with no author available to sanity-check you.

## Inputs and effort

Accept an optional target scope (a repo path, a subsystem, or free-form focus like "the pricing logic"). Default scope is the whole repository, excluding vendored/generated code, lockfiles, and build output.

Two effort levels — ask only if the user gave no signal; default to `quick`:

- **quick** — compare the top 5 twin sets from discovery; skip Phase 4 (Prove).
- **deep** — compare every discovered twin set; run Phase 4 repro tests for all CONFIRMED findings.

Run the phases in order. Phases 2 and 3 fan out via parallel subagents (Agent tool) — launch each phase's subagents in a single message so they run concurrently.

## Phase 1 — Twin discovery

Spawn ONE discovery subagent with this prompt (fill in `{SCOPE}`):

```
Survey the codebase at {SCOPE} and find TWIN SETS: places that implement the
same concept more than once. Why: divergence between copies is a high-precision
bug signal — at least one copy must be wrong — so your job is to find every
pair/group worth diffing, not to judge them yet.

Hunt specifically for:
1. Duplicated validation — client vs server, API layer vs DB constraint,
   form schema vs backend schema (Grep for shared field names in both trees).
2. Twin calculations — the same number computed in two modules (price, total,
   quota, progress %, expiry). Grep for the domain term across layers.
3. Copy-paste siblings — near-identical functions/blocks. Grep for distinctive
   substrings (odd string literals, unusual variable names, magic numbers).
4. Odd-one-out patterns — N handlers/routes/reducers/commands following the
   same shape where one deviates (missing auth check, missing try/catch,
   different cleanup). List the whole family and the deviant.
5. Encode/decode, serialize/deserialize, setup/teardown, acquire/release
   pairs — asymmetry between the two halves is a bug.
6. Constants, enums, limits, and config defined in more than one place
   (backend + frontend + docs + env defaults).
7. Permission/authorization checks repeated across layers.
8. Error-handling conventions applied everywhere except somewhere.

Exclude vendored, generated, and build-output files.

Return a ranked TWIN LIST as a markdown table, highest bug-likelihood first:
| # | Concept | Locations (file:line each copy) | Why divergence matters (user-visible consequence) |
Rank by (a) how bad divergence would be, (b) how likely drift is (copies far
apart in the tree, different authors, one recently modified). Aim for
10-25 entries; return fewer only if the codebase genuinely lacks twins.
```

Keep the full twin list — it is the coverage ledger for the final report.

## Phase 2 — Diff the twins

Take the top 5 twin sets (`quick`) or all of them (`deep`). Spawn ONE comparator subagent per twin set, all in parallel, each with this prompt (fill in the twin set row):

```
Compare parallel implementations of the same concept and find behavioral drift.
Why: these copies are supposed to agree; every behavioral difference means at
least one copy is wrong, so each difference you find is a candidate bug.

Twin set: {CONCEPT}
Copies: {LOCATIONS}

1. Read every copy in full, plus enough surrounding code to understand each
   copy's inputs and outputs.
2. List EVERY behavioral difference, however small: boundary conditions
   (>= vs >), null/undefined/empty handling, error paths (throw vs swallow vs
   default), rounding and precision, timezone/DST handling, case sensitivity,
   missing enum/switch cases in one copy, order of operations, trimming/
   normalization done in one copy only.
3. For EACH difference, classify it:
   - INTENTIONAL — different requirements at different layers. You must cite
     evidence: a comment, a test asserting the difference, or a structural
     reason (e.g. server enforces stricter rules than client by design).
   - DRIFT — the copies were meant to agree and one fell behind. Check
     `git log --follow -p` on each copy: a fix applied to one twin but never
     ported to the other is the strongest form of evidence. Name WHICH copy
     is wrong and why.
4. Each DRIFT becomes a candidate finding.

Return markdown:
## Twin set: {CONCEPT}
### Differences
For each: **[INTENTIONAL|DRIFT]** <difference> — <evidence>
### Candidate findings (DRIFT only)
For each:
- file/line of the wrong copy
- summary (one line: what disagrees and which copy is wrong)
- failure_scenario (concrete user-visible consequence: the input that hits
  the wrong copy and what the user sees go wrong)
- twin_evidence (the other copy's file:line and the exact divergent lines,
  quoted)
Return "No drift found" if all differences are intentional.
```

Pool all candidate findings.

## Phase 3 — Verify (inverted ladder)

Off-diff, false positives are expensive — there is no PR author to wave one off in thirty seconds. So the verifier defaults to REFUTED and a finding must earn its way up.

Spawn ONE verifier subagent per candidate finding, all in parallel:

```
Adversarially verify a candidate bug found by twin-divergence analysis.
Why: this feeds a bug report on shipped code; only findings with a concrete
trigger are worth a human's time, so your default verdict is REFUTED and the
finding must earn an upgrade.

Candidate: {SUMMARY}
Wrong copy: {FILE}:{LINE}
Twin: {TWIN_EVIDENCE}
Claimed failure: {FAILURE_SCENARIO}

1. Read both copies yourself. Confirm the divergence is real (quote the lines).
2. Intent check: run `git blame` on the divergent lines of BOTH copies, read
   surrounding comments and any tests covering either copy. If the divergence
   is deliberate (test asserts it, comment explains it, commit message says
   so), verdict is REFUTED — cite the evidence.
3. Trigger check: construct a CONCRETE input that reaches the wrong copy
   through a real entry point (route, CLI, job, UI path) and produces
   user-visible wrong behavior — e.g. a value that passes client validation
   but the server rejects, or two totals shown to the user that disagree.

Verdicts:
- CONFIRMED — you can name the exact input, the entry-point path to the wrong
  copy, and the wrong output/crash/corruption. Quote the lines.
- PLAUSIBLE — the divergence is real and unintentional, but the trigger
  depends on state you cannot fully confirm (feature flag, deploy config,
  rare timing). State exactly what would confirm it.
- REFUTED — divergence is intentional (cite evidence), unreachable (show why),
  or the copies do not actually disagree (quote the lines that prove it).

Return: verdict, evidence (with quoted lines), and for CONFIRMED the full
trigger walk (input → path → wrong behavior).
```

Drop REFUTED findings from the main report (keep them in an appendix list).

## Phase 4 — Prove (deep only)

For each CONFIRMED finding, spawn a repro subagent:

```
Write a minimal failing test (or standalone repro script) demonstrating this
confirmed twin-divergence bug. Why: a finding with a repro is fix-ready and
outranks every claim.

Bug: {SUMMARY} — {TRIGGER_WALK}
Copies: {LOCATIONS}

Prefer a table test that feeds the SAME input to both twins and asserts they
agree — it fails today and becomes the regression guard after the fix. Use the
repo's existing test framework and conventions. Put the test in the
conventional test location but DO NOT commit. Run it and confirm it fails for
the stated reason. Return: test file path, the command to run it, and the
failure output.
```

A finding whose repro actually fails as predicted is upgraded to **PROVEN**.

## Phase 5 — Report

Rank: PROVEN > CONFIRMED > PLAUSIBLE; within a tier, worse user-visible consequence first. Use exactly this template:

```markdown
# Divergence hunt — <repo/scope>, <effort level>

## Summary
<2-3 sentences: twin sets found, compared, findings by tier.>

## Findings
### [N] <one-line summary> — <PROVEN|CONFIRMED|PLAUSIBLE>
- **Wrong copy:** <file:line>
- **Twin:** <file:line>
- **Divergence:**
  | | <copy A> | <copy B> |
  |---|---|---|
  | <the divergent behavior> | <quoted line(s)> | <quoted line(s)> |
- **Trigger:** <input → entry-point path → wrong behavior>
- **Evidence:** <verifier evidence; git-log fix-ported-to-one-twin note if any>
- **Repro:** <test path + failure output, or "not attempted (quick mode)">

## Coverage
- Twin sets discovered: <N> (full list below)
- Twin sets compared: <M> — <which>
- NOT compared: <list> — findings above say nothing about these.

## Appendix: refuted candidates
- <file:line> — <summary> — refuted because <one line>
```

Never let a short findings list read as a clean bill of health: the Coverage section must state plainly what was not examined. If discovery finds no meaningful twin sets, say so and recommend a sibling strategy (invariant sweep or entry-point tracing) instead of padding.
