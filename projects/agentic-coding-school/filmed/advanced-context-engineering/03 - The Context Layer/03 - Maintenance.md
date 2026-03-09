---
status: filmed
---

Yes, the context layer needs maintenance. But think of it like tending a garden. You don't plant once and walk away—weeds grow, plants spread, seasons change. A neglected garden becomes overgrown. A tended garden thrives.

The same is true for your layer. Without maintenance, **drift** creeps in—nodes that describe how the code *used to* work, not how it works *now*. Drift is compression rot. Stale nodes aren't signal anymore. They're noise that actively misleads.

But here's the good news: maintenance can be automated. And when done right, it doesn't just prevent rot—it continuously improves agent performance. Each cycle compounds.

![[images/03-maintenance/keeping-compression-accurate.png]]

---

## The Sync Process

On every merge to main:

1. **Detect** which files changed
2. **Identify** which nodes cover those changes
3. **For each affected node** (leaf-first, working up):
   - Read the diff and the existing node
   - Re-summarize if behavior changed
   - Propose updates
4. **Human reviews and merges**, like any code change

This can be done manually by engineers after significant changes. But because the process is mechanical and well-scoped, it's straightforward to build an agent that handles it automatically.

**The cost:** 5-10 minutes per significant PR when done manually. Compare that to 20+ minutes of agent confusion per engineer when nodes drift—plus the bugs from following outdated patterns.

![[images/03-maintenance/the-sync-process.png]]

---

## Leaf-First Updates

When code changes, update nodes **leaf-first**, working up the tree.

Why? This is the same principle from [[02 - Chunking Your Codebase#4. Hierarchically Summarize|hierarchical summarization]]. Parent nodes summarize their children. If you update a parent before its children, you're summarizing stale content—your compression becomes inaccurate.

```
Change in payment/validators/amount.ts

Update order:
1. payment/validators/CLAUDE.md (if exists)
2. payment/CLAUDE.md
3. services/CLAUDE.md
4. Root CLAUDE.md (only if system-wide impact)
```

Most changes only affect leaf nodes. The [[01 - Hierarchical Context|hierarchy]] localizes the maintenance burden—you're not rewriting the whole layer for every change.

![[images/03-maintenance/leaf-first-updates.png]]



![[images/03-maintenance/leaf-first-updates-2.png]]


---

## What Triggers an Update

Not every code change requires a node update.

Remember the [[03 - Common Mistakes#The "Would It Mislead?" Test|"Would It Mislead?" test]]: if the code changes and the node stays the same, would it mislead an agent?

**Update when:**
- New patterns or conventions are introduced
- Invariants change
- Public contracts change
- New gotchas or pitfalls are discovered
- The existing node would mislead an agent

**Skip when:**
- Implementation details change but contracts don't
- Bug fixes that don't change patterns
- Refactors that don't change responsibilities

The question is always: **Would an agent reading the current node make a mistake on this code?** If yes, update. If no, leave it.

![[images/03-maintenance/what-triggers-an-update.png]]

---

## Maintaining Tribal Knowledge

The layer captures more than code patterns. It captures [[02 - The Context Layer|what code alone cannot express]]—the tribal knowledge, historical decisions, and incident learnings that live in people's heads (or buried in Slack threads).

This tribal knowledge needs maintenance too. But here's the key principle: **your source of truth should live alongside the code.**

When you have historical context from a Slack thread or incident doc, you have two options:

**Option A: Capture it directly.** Extract the relevant insight and write it into the node. The Slack thread was the discovery, the node becomes the documentation. Future readers (human or agent) get the knowledge without digging through chat history.

```markdown
## Historical Context

The 48-hour reconciliation window exists because of the Q3 2021
incident where same-day reconciliation caused duplicate settlements
during bank maintenance windows. The extra buffer prevents this.
```

**Option B: Capture incrementally.** If you don't have time to fully extract the insight, note that it needs capturing. Add new relevant threads as they happen.

```markdown
## Historical Context

- Reconciliation window: 48 hours due to Q3 2021 incident [needs full capture]
- Rate limiting approach: decided in platform-arch channel, Mar 2024 [needs capture]
```

The goal: **the node should be self-contained enough that an agent can operate safely without chasing external links.** Slack threads get deleted, channels get archived, context gets lost. The node persists.

When new decisions happen in Slack, capture them into the relevant node. Don't let tribal knowledge accumulate in chat where it can't be found.


![[images/03-maintenance/maintaining-tribal-knowledge.png]]

---

## The Reinforcement Loop

Here's where maintenance becomes genuinely exciting.

When agents use the layer, they surface what's missing:

- They hit edge cases: contradictions between code and nodes, undocumented patterns, sharp edges humans learned to step around
- They propose updates: refined pitfall sections, corrected invariants, suspected dead code flagged for confirmation
- They ask questions you never thought to document

Those learnings feed back into the layer. Future agents start from a better baseline.

**Your codebase becomes a reinforcement learning environment.** Agents get fine-tuned to your system through better context, not expensive model training. This is the closest thing to fine-tuning without actually fine-tuning.

Think about what this means:
- Every agent mistake is a signal about missing context
- Every correction you make improves all future tasks
- The layer accumulates institutional memory that never forgets and never retires

Build once. Agents help maintain. Each cycle compounds into a knowledge base that gets better with use.

![[images/03-maintenance/the-reinforcement-loop.png]]

---

## Session-End Prompts

At the end of significant sessions, prompt for updates:

> "Based on this session, should any CLAUDE.md files be updated?"

**Good candidates for addition:**
- A gotcha you just discovered
- A command you ran multiple times
- A pattern Claude kept getting wrong until you corrected it
- Historical context you had to explain verbally

**Bad candidates:**
- Task-specific context that won't apply again
- Explanations of what you just built (that's what code comments are for)
- Temporary workarounds you'll remove next week

This keeps the layer evolving with the project. The agent becomes a collaborator in maintaining its own context.

![[images/03-maintenance/session-end-prompts.png]]

---

## Automation Options

### Manual (5-10 min per PR)

After merging significant changes:
1. Review which nodes might be affected
2. Read the diff alongside the node
3. Update if the node would mislead

Works for small teams or low-change codebases. Start here to learn the patterns.

### Semi-Automated

Build a script that:
1. Detects changed files on merge
2. Maps them to covering nodes
3. Generates a PR with suggested updates
4. Human reviews and merges

This is a good introduction to agentic engineering—and it catches drift you'd otherwise miss.

### Fully Automated

Agent monitors merges, proposes updates, runs them through CI. Human approves or tweaks.

This is the endgame—but start manual, automate when you understand the patterns. You need to know what good maintenance looks like before you can evaluate automated suggestions.

![[images/03-maintenance/automation-options.png]]

---

## Preventing Drift

The biggest risk is **drift**—nodes that describe how the code used to work, not how it works now. Drift degrades your [[01 - Foundations & Problem Statement/02 - Signal to Noise|signal-to-noise ratio]]. Every stale instruction competes with accurate ones for the model's attention.

**Symptoms of drift:**
- Agents follow instructions that don't apply anymore
- Agents look for files that don't exist
- Agents miss files that do exist
- Agents use patterns that are deprecated
- You keep correcting the same misunderstanding

**Prevention:**
- Treat nodes like code: review them in PRs that change their covered areas
- Run periodic audits: read a sample of nodes alongside the code they cover
- Trust agent feedback: if agents keep getting something wrong, the node might be stale
- Add node updates to your PR checklist, right next to "update tests"

![[images/03-maintenance/preventing-drift.png]]

---

## Signs You're Doing It Right

How do you know the layer is healthy?

**Positive indicators:**
- Agents find relevant files on first try without extensive searching
- Fewer "I couldn't find where X is handled" moments
- New team members (human or agent) become productive faster
- Agents propose changes that respect existing patterns
- You rarely need to correct the same misunderstanding twice

**The compound effect:**
- Each task leaves the layer slightly better
- Agent performance improves over weeks and months
- Onboarding time drops for new engineers
- Institutional knowledge survives team turnover

This is the payoff. The upfront investment is real. But the maintenance cost per PR is small—and the value grows with every task.

![[images/03-maintenance/signs-youre-doing-it-right.png]]

---

## The Maintenance Flywheel

```
Code changes
    ↓
Nodes updated (manual or automated)
    ↓
Agents use updated context
    ↓
Agents surface what's still missing
    ↓
Learnings feed back into nodes
    ↓
Better context for next change
    ↓
(repeat)
```

This is the compounding effect. Each cycle makes the layer more accurate, more complete, more valuable. The garden grows healthier with each season.

![[images/03-maintenance/the-maintenance-flywheel.png]]

---

## Summary

| Practice | Why It Matters |
|----------|----------------|
| Sync on merge | Catches drift before it compounds |
| Leaf-first updates | Keeps compression accurate up the tree |
| "Would It Mislead?" test | Focuses effort on what matters |
| Capture tribal knowledge | Source of truth lives with the code |
| Reinforce from agent feedback | Layer improves continuously |
| Treat nodes like code | Same review rigor as code changes |

The layer isn't static documentation. It's living infrastructure—a garden that grows more valuable the more you tend it.

Drift is compression rot. Maintenance keeps your [[01 - Foundations & Problem Statement/02 - Signal to Noise|signal-to-noise ratio]] high and your [[02 - Chunking Your Codebase|compression]] accurate. The result: agents that work better over time, not worse.
