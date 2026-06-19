---
tags: [codex, subagents, nested-agents, mental-models]
date: 2026-05-06
status: "scripted"
---

Mental models and patterns for using **nested subagents** in Codex, Claude Code, or any harness that supports spawning child agents. The unifying question for every pattern: *when does another layer of nesting actually pay for itself?*

## The constraint that shapes everything

A subagent returns to **its parent only**. Siblings cannot merge under a shared third agent on a "next layer," because that next layer doesn't exist as a thing siblings share. If you want results combined, the parent has to do it (or spawn a fresh agent that consumes the children's reports).

This single fact rules out a lot of clean-looking diagrams and forces most useful patterns into one of three shapes:

```
   1) Parent fans out, then merges itself
        Parent
        / | \
       A  B  C
        \ | /
        Parent (merges)

   2) Parent fans out, then spawns a fresh verifier with the reports
        Parent --> A, B, C
        Parent --> Verifier (sees A, B, C reports)

   3) Each child verifies itself before returning
        Parent
        / | \
       A  B  C
       |  |  |
      vA vB vC      ← internal to each child
```

Almost every pattern below is some variation on these three shapes.

## The tradeoff

Nesting buys you context isolation, specialization, and parallelism. It costs you tokens, coordination overhead, and predictability. Default to depth 2. Past depth 3, you're usually paying for nesting you don't need.

---

## Pattern 1: Map, Reduce, Verify

Parent splits the task. Children do the work in parallel. A verifier checks results before the parent accepts them.

There are **two distinct flavors** of this pattern, and the verifier's job is different in each.

### 1a. Build and Verify

Child *implements* something. Verifier checks "does this match the plan." Parent can resume the child to revise.

```
   Parent: "implement plan section X"
        |
      Child A: implements
        |
      returns code + summary
        |
   Parent spawns:
      Verifier: "compare implementation vs plan"
        |
      verdict: matches / drifted / missed Y
        |
   Parent resumes Child A if needed
```

**Use when:** implementing a multi-section plan, refactor work, anything where "did we actually do what we said" is the failure mode.

### 1b. Find and Verify

Child *claims* a finding. Verifier tries to reproduce. Parent can resume the child to dig deeper or kill the claim.

```
   Parent: "find bugs in module X"
        |
      Child A: returns "suspected SQLi at line 42"
        |
   Parent spawns:
      Verifier: "write a failing test that proves it"
        |
      verdict: confirmed / can't repro / false positive
        |
   Parent resumes Child A on confirmed leads
```

**Use when:** bug hunting, security review, fact extraction, anything where a wrong answer is expensive.

The verifier is the killer feature in both flavors. Verification by a fresh agent has no investment in the finding being real, so false positives drop sharply.

---

## Pattern 2: Divide and Conquer by Surface Area, with a Stop Condition

Parent partitions by directory, service, or layer. Each child owns a partition. *If* a partition is still too big, the child sub-partitions.

```
              Parent
             /   |   \
        web/   api/   workers/
        / \     |        |
   pages comp  routes  jobs       ← only nests where needed
```

The trick that makes this work: don't leave the recursion decision to vibes. Put a **stop condition in the prompt**.

> "If your partition is more than N files or more than X kloc of relevant code, sub-partition before doing the work. Otherwise handle it inline."

Without that, agents either over-spawn (every child reflexively sub-spawns) or under-spawn (every child crams a 50-file review into one context). With it, depth becomes a function of input size, not mood.

**Use when:** monorepo audits, dependency upgrades, dead-code sweeps, large-scale rename.

**Watch out for:** depth past 2 even with a stop condition is usually a sign that the partition is wrong, not that you need more layers.

---

## Pattern 3: Hypothesis Tree

Parent generates N competing hypotheses. Each child investigates one. Each child can spawn sub-children to test sub-hypotheses. Branches that fail their test get pruned.

```
        Parent: why is this flaky?
       /     |       |       \
   Race    Env     Data     Timing
    |       |        |        |
   sub    sub       sub      sub      ← each tests a falsifiable claim
```

The tree itself becomes the debugging notebook. Forces falsifiable claims instead of vibes.

**Use when:** debugging, root cause analysis, incident response, "why is this slow."

**Pair with:** Pattern 1b (Find and Verify) on the leaves. A hypothesis "passes" only if a verifier can repro the failure mode it predicts.

---

## Pattern 4: Adversarial Pair

Two children, opposing roles, at the same level. The parent (or main session) judges.

```
        Parent
        /    \
     Red    Blue           opposing positions
     /\      /\
   ev ev   ev ev           evidence for each side
        \  /
       Parent judges
```

The point isn't "two opinions." It's that an agent asked to *find problems* and an agent asked to *defend the code* attend to different things. The defender has to actually trace logic to make its case, which surfaces bugs the attacker would have skimmed past.

**Use when:**
- A single reviewer keeps coming back with shallow comments.
- The change is in a politically loaded area (security, billing, auth) and you want the disagreement on record.
- You're stuck on a yes/no decision and want the strongest case for each side before you call it.

**Don't use when:** the answer is obvious. Forced disagreement on a clear question wastes tokens and produces a fake debate.

The judge is usually the main session, not a third subagent. Two reasons: the main session has the original intent, and there's no shared "next layer" to put a third sibling on anyway (see *The constraint that shapes everything*).

---

## Pattern 5: Order Perturbation

Same target, same model, but each sibling gets the context loaded in a *different order*. Order changes attention, which changes hypotheses.

```
   Parent: review module X
       |
       ├──> Child A: tests first, then code
       ├──> Child B: code first, then tests
       ├──> Child C: callers first, then implementation
       ├──> Child D: history first (blame, recent commits), then code
       └──> Child E: spec first (PR description, design doc), then code

   Each child returns to Parent (no shared verifier layer).

   Parent then either:
     (a) merges the reports itself, OR
     (b) spawns a fresh verifier and feeds it all five reports
```

Each priming order biases what the agent notices:
- **Tests first** biases toward "does code match spec."
- **Code first** biases toward "do tests cover this."
- **Callers first** surfaces interface bugs.
- **History first** surfaces "this was just changed and might be wrong."
- **Spec first** surfaces "code doesn't do what was promised."

Findings reported by 2+ orderings are high confidence. Findings reported by only 1 are worth checking but suspect.

**Use when:** code review, audits, anywhere you'd ensemble model outputs in ML.

**Limit:** the perturbations have to be *meaningfully* different. Swapping two adjacent files won't decorrelate; tests-vs-code is a real flip. Same goes for the "frame": you can also vary the *question* across siblings ("find bugs," "explain why this is correct," "what breaks under load"), which produces a different ensemble axis.

---

## Pattern 6: Deploy with Embedded Debugger

Main session spawns a deploy subagent. The deploy subagent runs the deploy. **If it fails**, the deploy subagent forks a debugger child *from inside its own context* to investigate, then returns either "deploy succeeded" or "deploy failed + diagnosis" to the main session.

```
   Main session
        |
   Deploy subagent
   ├── runs deploy
   ├── if success: return "deployed"
   └── if failure:
         └── forks Debugger child  ← inherits live failure context
                |
              returns root cause + suggested fix
         |
       Deploy subagent returns "failed: <diagnosis>"
        |
   Main session
```

Why this beats "deploy fails, main session investigates":

- The deploy subagent already has the live failure state in its context: logs, exit codes, the exact step that broke. Spawning the debugger from inside means no re-fetching.
- The main session stays clean. It only sees "deploy failed, here's the diagnosis," not 4000 lines of build log.

**Watch out for:** the debugger fork inherits the deploy agent's polluted context. Usually that's exactly what you want, but if the real cause is *upstream* of the failure (a bad commit, a config drift), the inherited context can anchor the debugger on the wrong layer. If diagnosis keeps blaming the proximate symptom, kill the fork and start a fresh debugger from main with just the error message.

**Generalizes to:** any "do thing, if thing fails diagnose locally" workflow. CI runs, migrations, large batch jobs, scheduled tasks.

---

## Pattern 7: Fallback Chain Across Data Sources

Each level of nesting represents "what if the source above failed." Used when you have multiple sources of the same kind of information with different cost or reliability.

```
   Main: "find 10 leads"
        |
   ├── Lead-finder 1
   │     └── try LinkedIn
   │            └── if no result: try Apollo
   │                   └── if no result: try web scrape
   ├── Lead-finder 2
   │     └── try LinkedIn
   │            └── ...
   └── ...
```

Each lead-finder is a sibling at layer 2. The data-source attempts inside it are a chain at layers 3, 4, 5. The chain is sequential by design: each level only fires if the level above returned empty or errored.

**Compare to the parallel-race alternative:**

```
   Lead-finder
        |
        ├──> LinkedIn
        ├──> Apollo
        └──> web scrape
   takes first success, kills the rest
```

When to use which:

- **Sequential fallback chain** (nested): sources have very different costs. Rate-limited APIs, paid lookups, slow scrapers. Pay only for the cheap source unless it fails.
- **Parallel race** (flat fan-out): latency matters more than cost. All sources are roughly the same price, and you'd rather pay 3x to get the answer in 1/3 the time.

The nested chain also makes the logic readable: each layer's prompt is "if the upstream came back empty, here's what to try next, with this much extra context." That's much easier to reason about than a single agent juggling all three sources at once.

**Use when:** lead generation, enrichment pipelines, fact-finding across sources of varying reliability, fallback search.

---

## Choosing

A rough decision rule:

- **Implementing something** → Pattern 1a (Build and Verify).
- **Hunting for something** → Pattern 1b (Find and Verify), often combined with Pattern 5 (Order Perturbation) on the search step.
- **Big surface area** → Pattern 2 (Divide and Conquer with a stop condition).
- **Stuck on a "why"** → Pattern 3 (Hypothesis Tree), with Pattern 1b on the leaves.
- **Yes-or-no call you can't decide** → Pattern 4 (Adversarial Pair).
- **Long-running operation that might fail** → Pattern 6 (Deploy with Embedded Debugger).
- **Multiple sources of the same info** → Pattern 7 (Fallback Chain) if costs differ, parallel race if they don't.

The single most useful upgrade for any nested workflow: add a **verifier**. The single most overrated move: increasing depth past 2.
