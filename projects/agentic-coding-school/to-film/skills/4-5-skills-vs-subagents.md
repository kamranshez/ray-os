---
class: "skills"
chapter: "Build Your AI Employees"
status: "scripted"
adapts: "skills-vs-subagents"
tags: [course, script, skills]
lesson: "4.5 Skills vs Subagents"
---

## Skills vs Subagents: When to Use What

We've built a lot of skills in this chapter. But there's another tool in Claude's arsenal that we haven't talked about — subagents. And at some point, you're going to wonder: should this be a skill or should this be a subagent?

They're different tools for different jobs. Pick the wrong one and you'll either get inconsistent output or waste time on something that should've been simple. So here's the framework.

### The Core Distinction (0:00–2:00)

**Skills are for consistency.** You want the same process followed the same way every time. Your contract reviewer should always check the same provisions, rate severity the same way, produce the same output format. That's a skill. It's an SOP — standard operating procedure. Predictable, repeatable, reliable.

**Subagents are for autonomy.** You want Claude to figure things out on its own, work in parallel, handle unexpected problems. Exploring a codebase to find bugs. Running the same refactor across 50 files simultaneously. Doing research where you don't know exactly what you'll find. That's a subagent. It's more like delegating to a smart person and saying "figure it out."

Here's the quick test. If you can describe the ideal output in advance — same format, same sections, same quality checks every time — use a skill. If the output depends on what the agent discovers along the way, use a subagent.

> [SCREEN: simple comparison on screen]

```
SKILLS                          SUBAGENTS
─────                           ─────────
Consistent process              Autonomous exploration
Same output every time          Output depends on discovery
SOPs, formatting, reviews       Large-scale tasks, parallel work
Follows your rules exactly      Can fix side issues on its own
Loads into main context         Runs in separate context
```

### The Scaling Problem (2:00–3:30)

Now here's where this gets practical. You've built maybe 10-15 skills in this class so far. That's fine. Claude handles that easily. But what happens when you get to 30? 40? 50?

Beyond about 30 to 40 skills, things get messy. Remember from the progressive disclosure video — every skill's description sits in tier one, always loaded. At 40 skills, that's 4,000+ tokens of descriptions Claude scans on every request. Descriptions start overlapping. Claude picks the wrong skill. Or it sees too many options and ignores them all.

So the question becomes — if I need 50 capabilities, but Claude can only reliably manage 30-40 skills, what do I do?

The answer is specialist subagents.

### The Specialist Subagent Pattern (3:30–5:00)

Instead of loading one Claude session with 50 skills, you create specialist subagents. Each one has access to just 3-5 skills in a focused area.

A marketing subagent with your LinkedIn skill, email drafter, and research skill. A finance subagent with your receipt scanner, invoice generator, and budget planner. A content subagent with your ideation, scriptwriting, and calendar skills.

Each subagent is an expert in its domain. It has a small, focused set of skills and doesn't get confused by the 40 other skills it doesn't need.

When you tell Claude "plan my marketing for next week," it doesn't scan 50 skills. It delegates to the marketing subagent, which scans 3 skills and picks the right one immediately.

This is the pattern: specialized subagents with fewer, scoped skills are more reliable than one agent drowning in options.

### Context Forking (5:00–6:00)

One more concept. When a skill runs, it normally loads into your main conversation context. The process instructions, the reference files, the output — all of it takes up space in your session.

But you can isolate a skill by adding `context: fork` to its frontmatter.

```yaml
---
name: receipt-scanner
description: ...
context: fork
---
```

When a forked skill runs, it executes in a separate context window. All the intermediate work — reading files, running commands, processing data — happens in the background. Only the final result comes back to your main session.

This is useful for skills that do a lot of heavy lifting internally but you only care about the end result. The receipt scanner reads 20 images, processes each one, builds a spreadsheet — you just want the spreadsheet. Fork it, and all that intermediate work doesn't eat your main context.

> [SCREEN: /context showing the difference — forked vs non-forked token usage]

If you've watched the Claude Code class, there's a full video on forked contexts. For this class, just know: if a skill does lots of work but produces a simple output, add `context: fork` and you'll save a ton of context space.

### The Decision Tree (6:00–6:30)

So here's how to think about it going forward:

**One focused task, same way every time?** → Skill.

**Discovery, exploration, or large-scale parallel work?** → Subagent.

**More than 30-40 skills getting noisy?** → Group them into specialist subagents with 3-5 skills each.

**Skill does heavy work but you only need the result?** → Add `context: fork`.

That's it. Skills for consistency. Subagents for autonomy. Specialist subagents for scale. Forking for efficiency.

### What's Next

That wraps up Chapter 4 — Build Your AI Employees. You've got a content director, an operations manager, a marketing director, a morning briefing, and an update skill. And you know when to use skills versus subagents.

But here's a question we haven't answered yet: how do you know these skills are actually good? How do you measure whether version two is better than version one? In Chapter 5, we're going to answer that with evaluations, benchmarks, and feedback loops.
