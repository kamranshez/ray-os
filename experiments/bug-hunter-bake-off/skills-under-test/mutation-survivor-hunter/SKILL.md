---
name: mutation-survivor-hunter
description: Hunt for live bugs in an existing codebase by finding the critical logic your test suite does NOT defend — mutation-testing logic used as a targeting lens. Use this whenever the user wants to bug-hunt existing code through the lens of test quality, asks "how good are my tests really", "what bugs would my tests miss", "mutation test this", "find untested critical logic", "audit my test coverage for real", "where could a bug hide from CI", or wants a general bug hunt with a test-suite angle. Also trigger on "find bugs in this codebase" when the repo has a test suite worth interrogating. NOT for reviewing a diff or PR — that is /code-review. Requires a runnable test suite (or at least test files) in the target repo.
---

# Mutation-Survivor Hunter

Find bugs by asking one question about every critical line: **what defends this line?**

The reasoning: a test suite is a definition of which bugs are *impossible* — any change that flips a defended line makes a test go red before it ships. But every line where a deliberately injected bug would SURVIVE the suite is a line the machine has never actually checked. Those lines have only ever been verified by human eyeballs, usually once, at write time. That is exactly where a real bug can already be living undetected — and where the next regression will land silently. So instead of reading the whole codebase with uniform suspicion, use mutation logic to find the undefended-critical intersection, and spend all your suspicion there.

Two deliverables come out of this: **live bugs** (the current code at an undefended line is already wrong) and **test gaps** (the current code is right, but nothing would catch it going wrong — reported with the exact surviving mutant and a suggested killing test).

Everything below runs against code at HEAD. This is not diff review; there is no diff. That means there is no author on hand to cheaply sanity-check your findings, so verification is strict (default-REFUTED, see Phase 3) and the report must account for what was NOT examined (see Phase 5) — silence about a region must never read as that region being clean.

## Effort levels

Ask the user (or infer from their phrasing) which level to run:

- **quick** — Phase 1 defense map + *mental-only* mutation on the top 5 regions. No real mutations executed, no killing tests drafted. ~15 minutes of agent time.
- **deep** (default when unspecified and the user said "hunt"/"audit") — full pipeline: top 10 regions, up to 10 *executed* mutations on the highest-stakes lines, verification, failing tests for confirmed bugs, drafted killing tests for the top test gaps.

## Phase 1 — Defense map

Spawn ONE mapping agent with this prompt (fill the bracketed parts):

```
You are mapping a codebase's test defenses to find critical logic the tests do not protect.
Repo: [absolute path]. Why: downstream hunters will scrutinize UNDEFENDED-CRITICAL code
hardest, so ranking quality here decides the whole hunt.

1. Identify the test framework(s) and the EXACT commands to run (a) the full suite,
   (b) a single test file, (c) tests matching a pattern. Verify by running one small
   test file. If the suite cannot run at all, say so and fall back to static mapping.
2. Get coverage cheaply: if the full suite with coverage finishes in a few minutes, run it
   and capture per-file line coverage. Otherwise APPROXIMATE: for each source module, Grep
   test files for imports/references to it; a module no test file imports is undefended.
   State which method you used.
3. Identify CRITICAL logic: money/billing, authn/authz, data mutation & deletion,
   external side effects (emails, webhooks, third-party API writes), published API
   surfaces, and anything the README/domain marks as core.
4. Rank regions by criticality × defenselessness. A payment calculation with no test
   outranks an untested logging helper AND a well-tested auth check.

Return EXACTLY this structure:
## Test commands
- full suite: `...` (runtime: Xs)  - single file: `...`  - pattern: `...`
## Coverage method
(measured | approximated-by-import-grep) + caveats
## Ranked regions (top 15)
| # | file:lines / function | why critical | defense level (none/weak/partial) | evidence |
## Unmapped
Directories/modules you did not assess, and why.
```

Keep the mapper's output verbatim — its table drives Phase 2 and its "Unmapped" section feeds the final coverage report.

## Phase 2 — Mutate: mentally first, then for real

Take the top N regions (quick: 5, deep: 10). Spawn one hunter agent PER REGION, in parallel, each with this prompt:

```
You are hunting bugs in ONE region of [repo]: [file:lines, function names, why it is
critical, defense level — paste the mapper's row and any coverage detail].
Test commands: [paste from Phase 1].
Why this matters: nothing automated checks this code, so you are likely the first
adversarial reader it has ever had. Read it like it is guilty.

For each key line/branch in the region, ask the mutation question: if I
  - flipped this comparison (< to <=, == to !=),
  - off-by-one'd this bound,
  - dropped this call / this null check / this early return,
  - swapped these two arguments,
  - replaced this value with 0/null/empty,
would ANY test fail? Trace the actual tests (read them — do not assume from file names).

For every line where the honest answer is "no test would fail":
(a) BUG CHECK — scrutinize whether the CURRENT code at that line is ALREADY wrong.
    Undefended lines have never been machine-checked; this is where live bugs hide.
    Look for the same classes you'd inject: inverted conditions, boundary errors,
    wrong variable, missing await, swallowed error, unhandled case.
(b) TEST-GAP RECORD — write down the exact surviving mutant (the literal before/after
    code) even if the current code looks correct.

Return EXACTLY:
## Candidate bugs
For each: file:line | what is wrong | concrete failure scenario (input/state -> wrong
user-visible outcome) | why no test catches it
## Surviving mutants (test gaps)
For each: file:line | mutant (before -> after) | why it survives | what a killing test
would assert
## Lines examined
file:line-ranges you actually read, so coverage accounting is honest.
```

### Executed mutations (deep level only)

Reasoning beats nothing, but execution beats reasoning — a hunter can be wrong about what the suite catches. After the hunters return, pick up to **10 total** of the highest-stakes "surviving mutant" claims across all regions and test them for real, one at a time:

1. Apply the mutant with Edit (the exact before → after the hunter recorded).
2. Run the FOCUSED test command for that module (never the full suite per mutation unless it is fast).
3. Record **killed** (a test failed — the hunter was wrong, downgrade that gap) or **survived** (confirmed gap).
4. **Revert immediately**: `git checkout -- <file>` before touching the next mutation.

Never batch mutations — two live mutants at once make results uninterpretable. Never leave a mutation applied while doing anything else. If anything goes wrong mid-run, `git checkout -- .` on the mutated paths before proceeding.

## Phase 3 — Verify candidate bugs

Every candidate bug (not test gaps — those were settled by execution or explicit test-tracing) gets an independent verifier agent that did NOT produce the finding. Ladder is INVERTED relative to diff review:

- **Default verdict: REFUTED.** On a diff, a plausible-but-wrong finding costs the author thirty seconds; here there is no author, and a false bug report costs a real investigation. The burden of proof is on the finding.
- **CONFIRMED** requires the verifier to construct a concrete trigger path: a real entry point (route, CLI command, job, public API), the input/state that reaches the line, and the wrong user-visible behavior that results. No path, no confirmation.
- **PLAUSIBLE** only when the mechanism is real and reachable but the trigger depends on timing/config the verifier cannot pin down — and it must state what would settle it.

Verifier prompt skeleton:

```
Independently verify this candidate bug in [repo]. You did not find it; your default
is REFUTED and you should try to refute it. [paste finding: file:line, claim, scenario]
1. Read the code and the claim. If the code does not say what the claim says, REFUTED
   (quote the line).
2. If it does: construct the trigger — entry point, input, path to the line, wrong
   outcome. If you cannot construct one, REFUTED or PLAUSIBLE, not CONFIRMED.
3. INTENT CHECK: git blame the line, read surrounding comments and any tests that
   exercise nearby behavior. If the "bug" is deliberate, load-bearing behavior,
   REFUTED — cite the evidence.
Return: verdict | trigger path or refutation evidence | intent-check notes.
```

## Phase 4 — Prove

- For each CONFIRMED bug: write a **failing test** using the repo's own framework, run it, confirm it fails for the claimed reason. A finding with a red test is the strongest artifact this skill produces; a CONFIRMED finding that resists a repro gets downgraded to PLAUSIBLE with an honest note.
- For the top test gaps (deep level): draft the **killing test** — it must PASS against current code and would have failed against the recorded mutant. Where a mutation was actually executed, you can prove both halves. This turns each gap from a complaint into a ready-to-commit patch.

Put drafted tests in the repo's conventional test location but do NOT commit anything; list the file paths in the report and leave staging decisions to the user.

## Phase 5 — Report

Use EXACTLY this template:

```markdown
# Mutation-Survivor Hunt — [repo] — [date]

## Verdict summary
X live bugs (Y with failing repro tests) · Z test gaps on critical logic · effort: [quick|deep]

## LIVE BUGS (ranked by severity)
### 1. [file:line] — [one-line summary] (CONFIRMED, repro: path/to/test)
- Failure scenario: [entry point -> input -> wrong outcome]
- Why no test caught it: [the defense hole]
- Verifier evidence: [trigger path]
(...)

## TEST GAPS (ranked by criticality of the undefended logic)
### 1. [file:line] — [what is undefended]
- Surviving mutant: `[before]` -> `[after]` ([executed: survived | reasoned-only])
- Suggested killing test: [path if drafted, or one-line assertion description]
(...)

## Coverage — what this hunt did and did NOT examine
- Regions examined: N of M ranked (list the unexamined ranked regions)
- Unmapped by Phase 1: [mapper's Unmapped section]
- Real mutations executed: X of Y claimed survivors (rest are reasoned-only)
- Coverage method: [measured | approximated]
An unexamined region is UNKNOWN, not clean.

## Repo hygiene
`git status` after all mutations reverted: [paste — must be clean apart from drafted
test files, which are listed here: ...]
```

The hygiene section is mandatory: run `git status` at the end, confirm every mutation was reverted, and list any files the hunt intentionally added (drafted tests). If the tree is dirty with anything else, fix it before reporting.

## Honesty rules (apply throughout)

- Rank ruthlessly; do not pad. Five real findings beat twenty maybes.
- "Reasoned-only" survivors are labeled as such — never present them with the same confidence as executed ones.
- If the suite cannot run, say so up front and run in degraded static mode; the report must state that every "survives" claim is unexecuted.
- Never let the report imply whole-codebase coverage. This skill examines the undefended-critical intersection, which is the highest-yield slice — but only a slice.
