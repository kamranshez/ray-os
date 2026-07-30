---
name: git-signal-hunter
description: Hunt for real bugs in EXISTING code by mining git history as a targeting signal — fix-density, churn, revert clusters, bus-factor, age inversion — then deep-reading the flagged files at HEAD with adversarial subagents and verifying every finding with an inverted (default-REFUTED) ladder. Use this whenever the user wants a bug hunt across a codebase rather than a review of a change — "find bugs in this repo", "where are the bugs likely hiding", "audit the hot files", "find the fragile code", "which files keep breaking", "hunt for latent bugs", "what's most likely to blow up next", "do a bug sweep", or any request to find defects in code that is already merged and shipped. Do NOT use for reviewing a diff, PR, or branch — that is /code-review. Do NOT use when the user already has a specific symptom or stack trace to chase (that's ordinary debugging).
---

# git-signal-hunter

Find real, unshipped-consequence bugs in a codebase as it exists at HEAD, using git history to decide **where to look** — never as a stream of old diffs to re-review.

## Why this strategy works

The strongest predictor of where bugs are is where bugs have been. Files with many fix commits attract fixes because something about them — a murky invariant, a bad abstraction, a concurrency hazard — keeps generating defects, and point-fixes usually paper over that root cause rather than remove it. Churn correlates with bugs because every edit is a fresh roll of the dice against invariants the editor may not know. Single-author files have never been read adversarially by anyone. This lets you spend deep-read attention on the ~15 files most likely to pay off instead of diluting it across 50k lines.

**The trap to avoid:** do not replay the history of diffs as review units. Cost scales with commit count, not code size; most of what you'd review no longer exists at HEAD; and you'd stay blind to exactly the emergent, cross-change bug class a whole-codebase hunt is for. History is a *map*, HEAD is the *territory*. Every finding must be about the code as it exists right now.

## Effort levels

Accept an optional effort argument (default `deep`):

- **quick** — top 5 targets, skip Phase 4 (Prove), cap report at 5 findings.
- **deep** — top 10–20 targets, full pipeline including repro tests, cap report at 15 findings.

## Phase 1 — Mine (one agent)

Spawn ONE subagent to build the ranked target list. Its prompt must include the commands below verbatim and this instruction: *"Return the structured target list only. Why this matters: the target list decides where all deep-read effort goes; a padded or unranked list wastes the whole hunt."*

Run these from the repo root (adjust pathspec excludes to the repo):

```bash
# 1. Fix-density: files most often touched by fix/bug/revert commits
git log --format= --name-only --grep='fix\|bug\|hotfix\|revert\|patch' -i \
  | sort | uniq -c | sort -rn | head -40

# 2. Churn: files most edited in the last 12 months
git log --format= --name-only --since='12 months ago' \
  | sort | uniq -c | sort -rn | head -40

# 3. Revert clusters: reverts signal changes that shipped broken
git log --oneline --grep='revert' -i | head -30

# 4. Fixes-of-fixes: for each high-fix-density file, check whether its fix
#    commits cluster in time (a fix within days of a previous fix to the same
#    file means the first fix didn't hold)
git log --oneline --follow --grep='fix' -i -- <file> | head -20

# 5. Bus-factor: single-author files have never been read adversarially
git shortlog -sn -- <file>

# 6. Age inversion: old, dormant files suddenly modified recently — the
#    recent editor likely lacked the original context
git log --format='%ad %h' --date=short -1 -- <file>   # last touch
git log --format='%ad %h' --date=short --reverse -- <file> | head -1  # birth

# 7. Size as a cheap complexity proxy — cross with churn: big AND hot is
#    the highest-risk quadrant
wc -l <candidate files>
```

Scoring: rank by (fix-density × churn × size), boosted by revert clusters, fixes-of-fixes, single-author, and age inversion. Numbers need not be precise — the ranking just has to concentrate attention.

**Exclusions (state them explicitly in the output):** vendored/third-party code, generated files, lockfiles, docs, tests-as-targets (tests inform the hunt but aren't hunted), and files whose churn is mechanical (formatting sweeps, license headers — check one sample commit if unsure).

Required output structure:

```
TARGETS (ranked):
1. <path> — signals: [fix-density: 14 commits, churn: 31 edits/12mo, 812 loc, single-author]
   hypothesis: <one line: what class of bug the signals suggest>
...
EXCLUDED: <paths/globs + reason>
CUT LINE: everything below rank N was not selected; next 5 candidates were: ...
```

Keep 5 (quick) or 10–20 (deep) targets. Merge files into one target when they form one module a single reader should hold together.

## Phase 2 — Hunt (one deep-reader subagent per target, in parallel)

Spawn one subagent per target (batch in parallel groups of up to 10). Each hunter's prompt must contain:

1. **The target and its signals** — prime the adversarial mindset with the specific signal: *"This file has 14 fix commits and a revert. Repeated fixes usually chase a single invariant nobody has named. Find the invariant the fixes keep circling, and check whether the current code actually establishes it."*
2. **Read the code at HEAD, whole.** The full file, then its immediate callers and callees (Grep for the exported symbols). Bugs here are usually boundary bugs: an assumption the file makes that a caller violates, or vice versa.
3. **History as context only.** `git log -p --follow -- <file>` is allowed to learn what keeps breaking and what each past fix assumed — but every finding must cite current lines. A finding about deleted code is worthless.
4. **What counts as a finding:** a nameable failure scenario — concrete input/state → wrong output, crash, data loss, or security hole. Not style, not "could be cleaner". Include `file`, `line`, one-line `summary`, `failure_scenario`, and `entry_path` (best guess at how real input reaches the line).
5. **Cap:** up to 5 candidates per target; return an empty list rather than pad. *Why: the verifier phase is expensive and a padded list drowns the real bugs.*

## Phase 3 — Verify (one independent verifier per finding, in parallel)

For each candidate, spawn a fresh verifier that has NOT seen the hunter's reasoning — only the finding itself. Inverted ladder, because off-diff hunting has no PR author to cheaply sanity-check claims, so false positives are far more costly than in diff review:

- **Default verdict is REFUTED.** The burden of proof is on the finding.
- **CONFIRMED** requires the verifier to construct a concrete trigger: an actual call path from a real entry point (HTTP route, CLI command, cron job, message handler) that reaches the flagged line with the bug-triggering input or state. Quote the lines along the path.
- **PLAUSIBLE** only when the mechanism is verified real in current code but the trigger depends on environment/timing the verifier cannot statically settle (a genuine race, a config-dependent path). State exactly what would settle it.
- **Intent check:** before confirming, run `git blame` on the flagged lines and read surrounding comments and tests. If a test pins the current behavior or a commit message explains it, the "bug" may be a decision — verdict REFUTED-INTENTIONAL, cite the evidence.

## Phase 4 — Prove (deep only)

For every CONFIRMED finding, spawn an agent to write a **failing test or minimal repro script** demonstrating it, placed under a scratch directory (never committed into the repo's test suite without asking). A finding with a failing test is a fix-ready ticket; a finding without one is a claim. If the repro attempt fails, downgrade the finding to PLAUSIBLE and record why — this is the last honesty gate.

## Phase 5 — Report

Assemble exactly this template:

```markdown
# Bug hunt report — <repo> @ <HEAD short sha>

## Summary
<2-3 sentences: targets examined, findings by verdict, strongest finding.>

## Findings (ranked: CONFIRMED-with-repro > CONFIRMED > PLAUSIBLE)
### 1. <file>:<line> — <summary> (CONFIRMED, repro: <path>)
- **Led here by:** <the git signal, e.g. "9 fix commits in 6 months, 2 reverts">
- **Failure scenario:** <input/state → consequence>
- **Trigger path:** <entry point → ... → flagged line>
- **Evidence:** <quoted lines>
- **Suggested fix direction:** <one line; if fixes-of-fixes, name the deeper invariant to establish instead of another patch>

## Refuted (for the record)
- <file>:<line> — <claim> — refuted because <evidence / intentional-with-citation>

## Coverage
- Examined: <N targets, listed>
- Ranked but not examined: <targets below the cut line>
- Not ranked at all: <the rest of the codebase — say so plainly>
```

The coverage section is mandatory. *Why: a diff is self-bounding, a codebase is not. Without it, "5 findings" silently reads as "the rest is clean" when it actually means "we read 15 files".*

## Ground rules

- Never modify the repo under audit (repro scripts live in scratch space).
- Findings cite current code only; git evidence supports, never substitutes.
- An empty report section beats a padded one — REFUTED findings are listed, not hidden, so the user can audit the hunt itself.
