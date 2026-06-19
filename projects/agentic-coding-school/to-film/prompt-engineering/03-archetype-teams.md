---
class: "prompt-engineering"
chapter: "Archetype Teams"
status: "scripted"
---
In the previous video we compressed a single identity into an agent. But real work requires multiple modes of thinking — and real teams have people with different strengths arguing toward the best outcome. This video shows how to build subagent teams from your own archetypes, and then extends that to compressing entire teams and organizations.

### Why One Archetype Isn't Enough

When you build software alone, you constantly context-switch between roles: product manager deciding what to build, engineer deciding how, designer deciding what it looks like, QA deciding if it works. Each role has different priorities, different things it notices, different tradeoffs it's willing to make.

A single Claude instance trying to be all of these at once hits the same problem as a broad prompt — it spreads its identity thin. The product thinking competes with the engineering thinking for the model's attention budget. You get a blended, averaged output that's decent at everything and excellent at nothing.

The fix: split them into subagents, each activated with a different archetype of you.

![[blended-agent-versus-split-specialized-archetypes.png]]
### Building Your Archetype Team

Each subagent gets its own compressed identity derived from your real data:

| Archetype | Data Sources | What It's Good At |
|---|---|---|
| **Product-You** | Feature decisions, user feedback responses, roadmap priorities, "build vs. skip" calls | Deciding *what* to build and *why* |
| **Writer-You** | Pre-AI writing, dictations, emails, newsletter drafts | Voice, tone, what to emphasize |
| **Engineer-You** | PR comments, code review patterns, architecture decisions | *How* to build, what's overengineered, what's fragile |
| **Design-You** | UI screenshots you saved, "this looks good/bad" reactions, layout preferences | Visual judgment, UX instinct |
| **Analyst-You** | Dashboard decisions, which metrics you track, how you interpret data | What numbers matter, what's noise |

The key: these aren't generic personas ("act like a product manager"). They're *your* product sense, *your* engineering instinct, compressed from *your* actual decisions. A generic PM persona gives you the consensus PM. Your archetype gives you decisions you'd actually agree with.

### How They Collaborate

The orchestrator (your main Claude instance) routes tasks to the right archetype and mediates disagreements:

**Example: Reviewing a new feature spec**

1. Orchestrator sends the spec to Product-You and Engineer-You simultaneously
2. Product-You responds: "This solves the right problem but scope is too big for this sprint — cut the notification system, ship the core flow"
3. Engineer-You responds: "The data model here will create pain later — spend 2 extra hours on the schema now"
4. Orchestrator synthesizes: presents you with the tension (ship fast vs. do it right) and both arguments
5. You make the 5% call — the irreducible human judgment

This mirrors how a real team works. The PM and the engineer disagree. Someone resolves it. But instead of scheduling a meeting with two humans, you get both perspectives in seconds, both already calibrated to your standards.

### The Tension Is the Feature

When your archetypes disagree, that's not a failure — it's the most valuable output.

Disagreement between Product-You and Engineer-You surfaces the exact tradeoff you need to think about. If they agreed on everything, you wouldn't need them.

The best teams have productive tension:
- Product pushes for shipping fast, engineering pushes for doing it right
- Design pushes for simplicity, product pushes for feature completeness
- Analyst pushes for more data, writer pushes for narrative clarity

By building archetypes that genuinely represent different facets of your thinking, you create that tension artificially — and the resolution is where the real insight lives.

![[product-versus-engineer-productive-tension-rope.png]]
### Compressing a Real Team

This extends beyond a single person. If you work with a team of 3-5 people, you can compress the *team's* collective identity:

1. **Gather decision artifacts** — meeting transcripts, Slack threads, PR reviews, design critiques from the actual team
2. **Identify each person's pattern** — what does the CTO always flag? What does the designer always push back on? What does the PM always prioritize?
3. **Create subagents for each team member's archetype** — not impersonating them, but capturing their judgment patterns
4. **Let them collaborate on new problems** — the CTO-archetype reviews architecture while the PM-archetype evaluates scope while the designer-archetype critiques the interface

The output: a first draft that already accounts for how your real team thinks. When you bring it to the actual meeting, you skip the first 45 minutes of alignment and go straight to the 5% that needs real human debate.

### Compressing an Organization

Take it further. High-performing organizations have a culture — a set of shared heuristics, standards, and tradeoffs that guide decisions at every level. Apple prioritizes design elegance over feature count. Amazon prioritizes customer obsession over internal convenience. Stripe prioritizes API clarity over implementation speed.

These organizational tastes can be compressed too:

- **Leadership memos and writing** — how the CEO communicates priorities reveals the org's reasoning patterns
- **Design systems and style guides** — not just the rules, but the *why* behind them
- **Postmortems and incident reviews** — how the org learns from failure reveals its actual values (vs. stated values)
- **Hiring rubrics and promotion criteria** — what the org rewards tells you what it actually optimizes for

A subagent team activated with an org's compressed identity produces outputs that "feel right" to anyone in that organization — because it's reasoning from the same set of heuristics the org uses.

This is how a solo founder scales to feel like a team, and how a team scales to feel like an organization — without adding headcount.

![[scaling-taste-individual-team-organization-levels.png]]
### Demo

1. Build two archetype subagents from real data: Product-You and Engineer-You
2. Give them a feature spec to review independently
3. Show where they disagree — and how the tension surfaces the real decision
4. Show the orchestrator synthesizing their outputs into a brief for you
5. Compare: the same spec reviewed by default Claude (one blended response) vs. the archetype team (structured tension with clear tradeoffs)

### Key Insight

> The model doesn't just contain one version of you — it contains every *mode* of you. By splitting these into separate subagents, you recreate the productive tension of a real team without the coordination overhead. And this scales: compress a team, compress an org, compress any group whose collective judgment you want to deploy at speed. The human role stays the same — resolve the tension, make the 5% call.

### Bridge to Next Video

You now have identity-activated subagent teams that can argue and collaborate. But they're running from static compressed data. In the next video, we'll close the loop — showing how each run generates new data that refines the archetypes, so your virtual team gets sharper over time just like a real one does.
