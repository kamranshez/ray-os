---
date: 2026-03-21
status: planning
---

## Title Hypotheses (A/B Test)

Based on proven formulas ("Dropped" verb dominance, insider framing at 49.4%, single-hook rule):

| Variant | Title | Rationale |
|---------|-------|-----------|
| A | Anthropic Just Started Building the Software Factory | "Software factory" = provocative new concept, insider framing, "Started Building" implies ongoing story |
| B | Anthropic Just Dropped Always-On Cloud Coding | Proven "Dropped" verb, benefit-forward, no parenthetical clutter |
| C | Your Codebase Now Gets Worked On While You Sleep | Outcome-first, personal stakes, curiosity gap |

Thumbnail ideas (2-3 words, face): "Code While Sleeping?" / "Software Factory?" / "24/7 Coding"

---

## Hook (3-Beat Formula)

1. **Empathy**: "If you've ever woken up to a pile of stale PRs, failing CI, and outdated docs..."
2. **Provocative claim**: "Your codebase can now be maintained 24/7 without you — or any human — touching it."
3. **Clear scope**: "I'll show you how to set it up, what to actually use it for, and why this is the first real step toward the software factory."

## Thesis

**"We're shifting from writing code to managing code production."**

Every section ties back to this: the developer's role is evolving from producer to supervisor. You set the intent, the schedule, the quality bar — Claude does the production.

---

## Section 1: What Just Shipped (1-2 min)

- Cloud-scheduled recurring tasks for Claude Code
- Set a repo (or repos), a schedule, and a prompt
- Runs on Anthropic's infra — your laptop can be off, closed, doesn't matter
- Available at claude.ai/code/scheduled or via desktop app
- Pro and Max plans (limits on # of schedules vary by plan, expect these to grow)
- Access to any MCPs you've connected via claude.ai

## Section 2: The Setup (2-3 min)

Screen recording walkthrough:

- Run `/web-setup` from terminal (Pro and Max)
- Connect your repos via GitHub connector
- Configure environment variables for secrets/keys (write-only in UI)
- Set the schedule (cron-style) and the prompt
- Show the UI at claude.ai/code/scheduled
- Note: if you already have local scheduled tasks, cloud sync is "coming soon" (per Noah Zweben)

## Section 3: Real Use Cases (3-4 min)

Progressive complexity, tiered:

**Maintenance (the boring stuff nobody wants to own):**
- Sweep open PRs nightly — code review + comments before your team wakes up
- Analyze CI failures overnight — file tickets when anomaly patterns spike
- Dependency audits — run npm audit, triage, open a PR
- Doc drift detection — code changed but docs didn't? Auto-PR the fix

**Building (the ambitious stuff):**
- Build features from approved GitHub issues — Claude picks up triaged issues and opens draft PRs
- Refactoring passes on deprecated API calls — pushed to review branches
- Test coverage gap analysis on new PRs

**With MCPs (the power-user stuff):**
- Since it has access to your claude.ai MCPs, you can chain external services
- Example: Slack/Discord notifications when scheduled runs complete
- Example: Linear ticket creation from code analysis results

## Section 4: The Software Factory Thesis (3-4 min)

The big idea — philosophical anchor payoff:

**Explain the concept simply:**
There's this idea that's been gaining a lot of traction recently called the "software factory." The metaphor comes from real manufacturing — think of a car factory. You don't hand-build every car from scratch. You design the blueprint, set up the assembly line, define quality standards, and then the factory runs. Cars come out the other end. You inspect, you adjust, you ship.

The software factory is the same idea applied to code. Instead of developers hand-crafting every line, you feed in specs — what you want built, how it should behave, what the constraints are — and autonomous agents handle the production. They write the code, they test it, they iterate on failures, and they deliver working software. Your job shifts from building to supervising the assembly line.

That's the end state. But we're not there yet. What we ARE getting, right now, are the **primitives** — the individual building blocks that make this possible. And cloud scheduling is one of the most important ones.

**The primitives are stacking up** (cite Aakash Gupta's thread — four features in 24 days):
- Remote Control (Feb 25) — freed you from your desk
- Scheduled Tasks (Feb 25) — freed you from remembering to kick things off
- Dispatch (Mar 17) — freed you from being near the machine
- Cloud Scheduling (Mar 21) — **removed the machine entirely**
- Each release eliminated one dependency. What's left? Just human judgment and intent.

**What this actually looks like when you combine the primitives:**

Imagine this: Sentry detects a bug in production at 2am. A scheduled Claude task is watching your error tracking. It picks up the issue, reads the stack trace, finds the root cause, writes a fix, runs the tests, and opens a draft PR — all before you wake up. You review the PR over coffee, approve it, ship it.

Or: you have a backlog of feature requests in Linear. A scheduled task runs every night, picks up the highest-priority approved issue, reads the spec, implements it, opens a PR. Every morning you wake up to a new draft feature. You review, refine, merge. You're shipping updates daily without writing a line of code yourself.

Or: the agent hits something ambiguous — a design decision it's not sure about, an edge case the spec didn't cover. It messages you on Telegram via Channels: "Hey, should the retry logic use exponential backoff or fixed intervals?" You reply from your phone. It continues building. You're supervising from the couch.

This is the software factory in its early form. Agents running in the background, on the cloud, around the clock. Not one agent doing one thing — multiple scheduled tasks across your repos, each handling a different part of the pipeline. Monitoring, building, testing, fixing, reporting back.

**The workflow shift:**
- Old: you write code, you review code, you ship code
- New: you set the intent, the schedule, the quality bar. Agents produce. You review the output, test, and ship.
- You're not writing code anymore. You're **managing code production** — and the highest-leverage work is now writing clear specs and making taste decisions
- Some people are already operating this way — small teams shipping like large engineering orgs

**The economics:**
- $200/month Max subscription vs. the cost of additional headcount
- This isn't replacing engineers — it's giving every engineer a night shift that handles the backlog
- A 3-person team operates like a 5-person team without the burn rate

**Where this is heading:**
- Right now we're at the hybrid stage — agents produce, humans review and approve. And that's mostly because the models still need that oversight. They're good, but not "trust it blindly" good.
- But think about it — we're on Opus 4.5. It's not quite reliable enough yet to fully trust unsupervised. But by the time we get to Opus 5, Opus 6, the reliability just keeps going up. The error rate drops. The judgment gets better. At some point, the review step becomes a formality. You glance at the PR, it's correct, you merge. Eventually you stop glancing.
- That's when the factory truly runs lights-out. Not because someone flipped a switch, but because the models got reliable enough that human review stopped adding value. The infrastructure is already here — cloud scheduling, channels, MCPs, env vars. The only bottleneck left is model capability. And that's the one thing that's improving the fastest.
- Future primitives we'll probably see: chained task outputs (one task's result feeds into the next), agent swarms (multiple agents coordinating on one problem), scenario-based validation (agents testing against simulated environments instead of waiting for human review)
- We're watching the assembly line get built in real time. Cloud scheduling is the conveyor belt — and today you can turn it on

## Section 5: What's Missing / Wishlist (1 min)

Keep it honest:
- Schedule limits per plan — still early
- No sync between local scheduled tasks and cloud (confirmed coming soon)
- No chaining of scheduled task outputs yet
- Secret manager integration still being worked out
- Retry behavior on errors unclear

## Section 6: CTA (30 sec)

Masterclass-first CTA (regular video, not pillar). Single CTA at end.

---

## Production Notes

- **Pacing**: 50% slower delivery, let the setup walkthrough visuals breathe 2-3 seconds
- **Progressive reveal**: Draw out the "software factory" thesis incrementally — don't show the full diagram at once. Build it piece by piece (Remote Control -> Scheduled -> Dispatch -> Cloud) as you narrate
- **Visual hook in first 10 seconds**: Show split screen — you sleeping / Claude opening PRs at 3am with timestamps
- **Terminal always moving**: During setup section, terminal should be actively running `/web-setup`, configuring repos, showing the schedule being created
- **Single topic, deep**: Not a feature roundup. One feature explored fully (focused videos get 25% more views)

## Estimated Length: 10-14 minutes
