---
tags: [youtube, script, claude-code, ultrareview, reverse-engineering]
status: uploaded
date: 2026-04-07
youtube-id: q1Dg6vSXl-8
youtube-title: "Claude Code Review 2.0 Is Coming"
published: 2026-04-08
duration: "8:11"
views: 356
likes: 11
comments: 0
fetched: 2026-04-09
---

## Video Plan: "Claude Code Has a Secret Bug Hunting Team"

| # | Title | Formula |
|---|-------|---------|
| 1 | **"Claude Code Has a Secret Bug Hunting Team"** | Bold claim + specificity |
| 2 | **"I Reverse-Engineered Claude Code's Hidden Review Feature"** | Personal journey + curiosity gap |
| 3 | **"5 AI Agents Just Reviewed My Code While I Made Coffee"** | Concrete result + time contrast |

So Claude Code has a feature that most people haven't seen yet. It's called ultrareview. And when you run it, it doesn't just review your code — it spawns a fleet of five parallel AI agents in the cloud, each one independently hunting for bugs in your branch. Then a separate agent verifies every finding. And the whole thing runs while you go do something else.

I reverse-engineered the binary to figure out exactly how it works.

### The Problem with Code Review (0:25–1:30)

Now if you've ever used `/review` in Claude Code, you know how it works. It runs locally. It reads the PR diff, gives you a list of observations — code quality, style, potential issues. And it's fine. It's one agent, one pass, done in about a minute.

But here's the problem. One agent, one pass means one perspective. It reads top to bottom, spots the obvious stuff, maybe catches a logic error if you're lucky. But the subtle bugs — the ones that only show up when you trace through three files, or the race condition hiding in an async chain — those slip through. Because one agent doing one pass just doesn't have the depth.

And that's actually the same limitation human code review has. One reviewer, one pass, linear reading. The important bugs live in the interactions between components, and no single-pass review reliably catches those.

![[images/ultrareview-hidden-bug-hunter/one-agent-one-pass-limitation.png]]
### What Ultrareview Actually Is (1:30–3:30)

*Terminal on screen — run `/ultrareview`*

So here's what Anthropic built. When you run `/ultrareview`, it doesn't review locally. It bundles your entire repo, teleports it to a cloud container, and spawns a fleet of agents — five by default — that independently hunt for bugs.

And I know this because I extracted the strings from the Claude Code binary. All the configuration is right there in the minified JavaScript.

*Show the extracted config on screen:*

```
BUGHUNTER_FLEET_SIZE:     5 agents   (max 20)
BUGHUNTER_MAX_DURATION:   10 minutes (max 25)
BUGHUNTER_AGENT_TIMEOUT:  600 seconds per agent (max 1800)
BUGHUNTER_TOTAL_WALLCLOCK: 22 minutes (max 27)
```

Five agents. Each one gets up to 10 minutes. Total wall clock time capped at 22 minutes. And internally, the whole system is codenamed "bughunter." Not "reviewer" — bughunter. That tells you the intent. This isn't about style feedback. This is about finding actual bugs.

Now — important caveat. None of these values are user-configurable. You can't set `fleet_size: 20` in your settings.json. All of this is controlled by Anthropic through their remote feature flag system — a config called `tengu_review_bughunter_config`. They can dial it up or down per organization. The code has a clamping function that enforces hard maximums — fleet size caps at 20, duration caps at 25 minutes, agent timeout caps at 1800 seconds. So even Anthropic's own config can't push it past those limits. But as a user, you get whatever defaults they've set for your org.

And the pipeline has four stages. I watched it run on my own repo and here's what I saw.

*Show the web session screenshot:*

**Stage 1 — Setup.** Your repo gets bundled and uploaded to a specific cloud environment. The environment ID is hardcoded — `env_011111111111111111111113`. That's a dedicated bughunter sandbox.

**Stage 2 — Find.** All five agents fan out across your diff independently. Each one is looking for bugs, logic errors, security issues. They don't coordinate — that's the point. Five independent perspectives on the same code.

And this matters more than people realize. I actually covered this in a previous video about refactoring with subagents — the order in which an agent loads files into its context window changes what it finds. If agent one starts in the API layer and reads downward into the database models, it builds a completely different mental model than agent two who starts in the frontend and traces a request backward. Same codebase, same diff, different exploration paths — and that means different bugs surface. One agent might catch a race condition because it happened to read the async handler before the state manager. Another might miss it entirely because it loaded those files in the reverse order. That's why having five agents isn't just "five times the coverage." It's five different angles of attack on the same code. Anthropic is basically applying the same principle I was teaching — vary the exploration order to overcome positional bias in the context window.

**Stage 3 — Verify.** This is the part that makes it different from everything else. Every candidate bug gets handed to a *separate* verification agent that tries to confirm whether it's real. It's not enough for an agent to say "this looks wrong" — another agent has to independently agree. In my case, the candidate got refuted. Zero confirmed, one refuted.

**Stage 4 — Dedupe.** If multiple agents in the fleet find the same bug, it gets deduplicated. You only see unique confirmed findings.

The result? "Review complete — no findings." Which in this case is actually good news — it means five agents couldn't find a real bug in my branch. But when they do find something, you know it's been independently verified, not just flagged by a pattern matcher.

![[images/ultrareview-hidden-bug-hunter/four-stage-bughunter-pipeline.png]]
### Two Modes of Operation (3:30–5:00)

*Back to terminal*

Now there are two ways to run it.

**Mode 1 — Branch mode.** Just type `/ultrareview` with no arguments. It finds the merge-base between your current HEAD and the default branch, bundles the whole repo, and uploads it. This is what I used. It's the simplest — you just run it and walk away.

**Mode 2 — PR mode.** `/ultrareview 42`. You pass a PR number. This one doesn't need to bundle anything — it checks out `refs/pull/42/head` directly from GitHub. So it works with any repo size, but you need to have pushed a PR first.

![[images/ultrareview-hidden-bug-hunter/branch-mode-vs-pr-mode.png]]

### The Billing Model (5:00–6:30)

Now this isn't free. And the billing model is actually interesting because I pulled the entire quota flow from the binary.

*Show the flow on screen:*

First, every org gets a certain number of free ultrareviews. The code fetches your quota from an API endpoint — `GET /v1/ultrareview/quota` — and it returns three numbers: `reviews_used`, `reviews_remaining`, and `reviews_limit`.

If you have free reviews left, you'll see something like "This is free ultrareview 3 of 5" in the launch message.

Once you burn through your free allocation, it switches to Extra Usage billing. But it doesn't just silently start charging. The first time in each session, it shows you a confirmation dialog:

*Show the dialog:*

> "Your free ultrareviews for this organization are used. Further reviews bill as Extra Usage (pay-per-use)."
> [Proceed with Extra Usage billing] [Cancel]

And there's a minimum balance check — if your Extra Usage balance is below $10, it won't even let you launch.

One more thing — if you're using Bedrock or a custom API setup, the quota system is bypassed entirely. You just run it.
### What This Means (9:30–10:30)

Now here's what I think is actually interesting about all of this. We're moving from "AI reviews your code" to "AI teams review your code with adversarial verification." That's a meaningful shift.

The verification stage is the key innovation. Most AI code review tools — including Claude Code's own `/review` — just flag things. They say "this looks suspicious" and move on. Ultrareview says "this looks suspicious — now prove it." And if the verification agent can't confirm the bug, it gets thrown out.

That's how you reduce false positives. Not by making one agent smarter, but by making agents check each other's work.

And the fleet architecture means it scales. Five agents today, twenty tomorrow. Each one catches things the others miss. It's parallel exploration of the bug space, not serial scanning.

![[images/ultrareview-hidden-bug-hunter/adversarial-verification-shift.png]]
### What You Can Do Right Now (10:30–12:30)

Now — ultrareview is still behind a feature flag. Most people don't have it yet. But here's the thing. The architecture isn't magic. It's the same multi-agent pattern you can set up yourself today with any coding agent that supports subagents.

**Claude Code.** You already have subagents. I've been teaching this for a while — spin up five explore agents, each starting in a different part of the codebase, each with a different review angle. One looks at error handling. One traces the data flow. One checks for race conditions. One focuses on security. One reads the tests. Have them report back independently, then synthesize. That's ultrareview — you're just running it locally instead of in the cloud.

**OpenAI Codex.** Codex now has full subagent support. You can define custom agents as TOML files in `~/.codex/agents/`, give each one different instructions and even different models, and Codex handles the orchestration — spawning them in parallel, routing follow-ups, collecting results. So you could build a "reviewer" agent, a "security auditor" agent, a "test coverage" agent, launch them all on the same diff, and get back three independent perspectives.

**Pi.** If you use Pi  — the open-source coding agent that works with Ollama and basically any model provider — it actually ships with a built-in `/review` command and a reviewer subagent out of the box. Plus it supports multi-model sessions, so you can have one agent running Claude, another running GPT, another running Gemini, all reviewing the same code. Different models catch different things — same principle as the fleet, but with model diversity on top.

The point is: you don't need to wait for Anthropic to flip a flag. The pattern is fleet of agents, independent exploration, then verification. You can build that today.

![[images/ultrareview-hidden-bug-hunter/diy-multi-agent-review-setup.png]]
### Building Your Own Ultrareview Skill (12:30–14:30)

Actually — let's build it. Right now. I'm going to turn this into a Claude Code skill that replicates the ultrareview pipeline using multiple models and multiple agents.

*Screen recording — building the skill live:*

Here's the architecture. Five reviewers, then two verifiers.

**The review fleet:**
- Three Claude subagents running in the background — each one gets a different review angle. One focuses on logic bugs. One on security. One on edge cases and error handling.
- Two Codex agents running in parallel via the Codex CLI — same diff, different model, completely different perspective. Codex uses GPT under the hood, so you're getting genuine model diversity, not just the same model five times.

That's five independent reviewers. Three Claude, two Codex. All running at the same time.

**The verification stage:**
- One Claude subagent that receives all the findings and tries to reproduce each one — reads the actual code, traces the logic, confirms or refutes.
- One Codex verification pass doing the same thing independently.

So you've got cross-model verification. A bug found by Claude gets verified by GPT, and vice versa. If both verifiers agree it's real, it makes the final report. If only one confirms it, it gets flagged as "likely" but not confirmed. If neither confirms it, it's thrown out.

*Show the skill file structure:*

The skill orchestrates all of this. You run `/fleet-review` and it:
1. Gets the diff against your base branch
2. Spawns three Claude background subagents with different review prompts
3. Kicks off two Codex CLI processes in parallel
4. Waits for all five to report back
5. Feeds all findings into the two verification agents
6. Produces a final consolidated report with confidence levels

*Show it running — the subagents spinning up, Codex running alongside:*

And the whole thing takes maybe 5–8 minutes. Faster than ultrareview because you're running locally — no repo bundling, no cloud teleportation. But you're getting the same architecture: fleet find, independent verify, dedupe.

![[images/ultrareview-hidden-bug-hunter/fleet-review-cross-model-pipeline.png]]
### What Two Reviews Actually Found (14:30–16:00)

So I ran two independent reviews on the same PR. One came back with twenty-two findings. The other came back with eight. Three direct overlaps.

The first review scanned everything — CI config, Dockerfiles, migrations, dependencies, route handlers, UI components. It read every file, caught credential exposure, supply-chain risks in CI, dead code, convention violations — and it prioritized all of it correctly. Blockers at the top, nits at the bottom. A thorough audit.

The second review ignored most of the codebase entirely. It picked one user flow and traced it end to end — from button click through room creation, through the active call, to teardown. It found race conditions and lifecycle bugs that the first review walked right past. Not because the first review was sloppy — but because those bugs only surface when you hold three files in your head at once and follow the execution order.

One thinks like an auditor — scan everything, categorize, prioritize. The other thinks like an attacker — pick a path and break it. Neither one alone caught everything.

![[images/ultrareview-hidden-bug-hunter/auditor-vs-attacker-review-styles.png]]
### Closer (16:00–16:30)

So that's ultrareview — Anthropic's cloud-based multi-agent bug hunter. And now you've got your own version as a skill. Three Claude agents, two Codex agents, cross-model verification. You can run it today on any repo, no feature flag required.

When ultrareview does roll out to everyone, use both. Run the cloud version for the deep server-side analysis, run your local fleet for the instant feedback loop. Belt and suspenders.

And if you want to see how I reverse-engineered all of this from the binary — the extraction process, the string searching, following the minified code trails — I'll link the full technical breakdown below.
## Demo Plan

1. Show `/review` running locally — fast, basic, one-pass
2. Run `/ultrareview` — show the launch message, the tracking URL
3. Switch to web session — watch the Setup → Find → Verify → Dedupe pipeline
4. Show the result (no findings / findings if we can trigger one)
5. Show the binary extraction process as a montage — `strings`, `grep`, following the code trail
6. Side-by-side `/review` vs `/ultrareview` on the same PR
7. Show the billing dialog and quota info
