---
title: "DHH's new way of writing code"
video_url: https://www.youtube.com/watch?v=JiWgKRgdgpI
video_id: JiWgKRgdgpI
channel: The Pragmatic Engineer
published: 2026-04-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**DHH's new way of writing code**](https://www.youtube.com/watch?v=JiWgKRgdgpI) - The Pragmatic Engineer - uploaded 2026-04-08

> Net-new and complement ACS videos available: make your product agent-accessible with a CLI, and run a two-model cockpit.

## The one idea worth a video

- **Make your own product agent-accessible: give it a CLI (or MCP) so an agent can drive it, then chain those tools together.** DHH stopped waiting for AGI and started shipping CLIs for Base Camp, Hey, and Fizzy so agents can operate them like a human, then stitched Sentry, GitHub, and Base Camp into one agent pipeline. VERDICT: ❌ net-new video available.
- **Run two model-agents in parallel, tiered by difficulty, with a diff-review cockpit in the middle.** A fast cheap model carries routine work while Opus takes the hard problems, and lazygit is the human review hub. VERDICT: 🔗 next-step video available.
- **Triage a huge PR/issue backlog by pointing an agent at each URL and judging its verdict.** 100 PRs in 90 minutes, with "clean room this" when the diagnosis is right but the code is wrong. VERDICT: ✅ already covered (kept for context).

## Summary + counts

The Pragmatic Engineer interviews DHH, creator of Ruby on Rails and Omarchy, on his six-month reversal from typing all code to a fully agent-first workflow.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Make your product agent-accessible (build it a CLI)

The claim: the durable way to get leverage from agents is to make your own software agent-accessible, wrapping it in a small CLI or MCP an agent can drive, then composing those tools. Why it is non-obvious: most people treat agents as consumers of tools someone else shipped (connectors, third-party MCPs). DHH inverts it: as the builder, you redesign your product's surface so an agent operates it the way a human would. Why it is true: he first probed the ceiling ("Do we even need MCP? Do we even need CLI?") by having OpenClaw sign up for Fizzy and Hey through a browser with no tools, then introduce itself inside a Base Camp project. It worked, proving the end state is agents needing no accommodations. But because that took seven minutes and is flaky today, he builds for today: a Base Camp CLI. Since every tool exposes a CLI or MCP, an agent can now chain them, reading Sentry errors, posting to Base Camp, opening a GitHub PR, commenting back. He notes this "validated the fundamental Unix philosophy from like whatever 71": small composable tools joined by pipes. Generalizes to any internal service, for example an ops team wrapping deploy and ticketing systems in CLIs so one agent runs an incident end to end. How it goes wrong: handing an agent write or delete access across production tools without permission guardrails, and relying on the slow, unreliable browser-only route before your CLIs exist.

### Spine 2 - The two-model cockpit (fast model + smart model in parallel)

The claim: running two model-agents in parallel, tiered by task difficulty, with a diff-review cockpit between them, turns you into a supervisor of a mech suit rather than a typist. Why it is non-obvious: the fear DHH voiced on Lex was that agents demote you to a distant project manager away from the code. His reframe: "running a bunch of agents feels less like being a project manager for agents and more like stepping into this super mech suit" where you have twelve arms and are still the one doing it. Why it is true: his tmux layout keeps Neovim on the left, two agent panes on the right (open code on Kimi K2.5 on top, Opus in Claude Code below), and a terminal strip at the bottom. He hands work to an agent, hops to Neovim, runs lazygit with space gg to read the diff, commits if it looks correct, edits otherwise. Tiering matters: "whenever I feel like this is a really hard problem, I go to Opus," while cheaper models carry the easy load in parallel. Throughput comes from making review, not typing, the human bottleneck. Generalizes to any parallel-worker setup, for example a data engineer running two agents on independent migrations while reviewing from one central diff view. How it goes wrong: without a fast review ritual you become the bottleneck, and parallel agents editing the same files collide.

### Spine 3 - Bulk PR/issue triage with the agent (COVERED)

The claim: you can triage a large PR or issue backlog by pointing an agent at each URL and judging its verdict, turning a week of review into ninety minutes. Why it is non-obvious: review feels like it cannot parallelize because judgment is the senior's scarce resource. Why it is true: before Omarchy 3.4, DHH faced roughly 250 pending PRs. Instead of 15 minutes each, he told Claude "review" with the PR URL. In about 90 minutes he processed 100: roughly 10% merged as-is, 20% merged after Claude re-implemented, 25% rejected, 25% "maybe but no clean shot." The load-bearing beat is "clean room this": when a contributor identified the right problem but hand-rolled code he did not want, he said "this is the right problem, let's do it right," and the agent rewrote it in the project's style. Half the analyses covered things he "knew nothing about," making the agent an "undeniably smarter, better reviewer." Generalizes to issue triage, dependency-bump review, and security-report triage. How it goes wrong: rubber-stamping agent verdicts on mission-critical code, the exact failure behind the Amazon outage example of juniors shipping unreviewed agent code. Coverage note: ACS "Going Through a PR Backlog" (Loopy AI) already teaches this loop, so this spine keeps its deep dive for context but gets no pitch.

## 🎬 Proposed ACS videos

### 1. Make Your App Agent Accessible: Give It a CLI

- **HOOK:** DHH stopped waiting for AGI and started shipping CLIs so agents can drive his products today.
- **THE PROMISE:** For builders who own a product or internal service: after this you can expose it through a CLI or MCP so an agent operates it and chains it to your other tools.
- **THE SHAPE:**
  1. Probe the ceiling: have an agent try your app through the browser with no tools and watch where it breaks (DHH's OpenClaw signup).
  2. Build a thin CLI for one real workflow in your product.
  3. Add or connect an MCP for a second tool (GitHub, Sentry).
  4. Chain them: agent reads Sentry errors, writes a status post, opens a PR, comments back.
  5. Add permission guardrails for write and delete actions.
- **SPINE:** 1
- **SLOT:** Advanced Techniques, new chapter "Agent-Accessible Products" (cross-post to For Business).
- **RELATIONSHIP:** ❌ net-new. "Claude.ai MCP Servers (aka Connectors)" teaches consuming existing connectors, and "Your Interaction Layer" teaches driving installed apps; neither teaches building your own product's CLI/MCP surface for agents, the escalation ladder, or composing a cross-tool pipeline.
- **PROOF TO REUSE:** "I want this claw in base camp... Go sign up" (OpenClaw one-shotting Fizzy and Hey signup); the Sentry to Base Camp to GitHub chain; "They validated the fundamental Unix philosophy from like whatever 71."

### 2. Your Two-Model Cockpit: Run a Fast Model and a Smart Model Together

- **HOOK:** DHH builds with Kimi and Opus side by side and reviews every diff from the seat in the middle.
- **THE PROMISE:** For solo devs and small teams: after this you can run two agents in parallel, tiered by difficulty, and keep quality with a fast diff-review ritual.
- **THE SHAPE:**
  1. Set up the tmux layout: editor left, two agent panes right, terminal strip bottom.
  2. Put a cheap fast model (Kimi K2.5) on routine work and Opus on the hard problem.
  3. Hand each pane an independent task so they never touch the same files.
  4. Review with lazygit: read the diff, commit if correct, edit if not.
  5. Escalate to Opus the moment a task feels genuinely hard.
- **SPINE:** 2
- **SLOT:** Advanced Techniques, Multi-Model & Multi-CLI Workflows.
- **RELATIONSHIP:** 🔗 complements "Combining CLIs & Models," which teaches one model implementing while a second critiques the diff; this adds running two models as parallel independent workers tiered by cost and difficulty, with the review cockpit as the hub.
- **PROOF TO REUSE:** the tmux/Neovim layout with open code plus Kimi on top and Opus in Claude Code below; "space gg" lazygit review; "this super mech suit... I have 12 [arms]"; "whenever I feel like this is a really hard problem, I go to Opus."

### Also film-able (not deep-dived)

- **Kick it off on a hunch while you go to lunch:** use agents to chase speculative, low-ROI ideas you would never staff (Jeremy's P1 latency project, Omarchy dual-boot), reverting freely when they flop. Rough slot: Techniques or My Daily Workflows. Lower priority; overlaps existing agent-workflow material.

## 📚 Full wisdom (reference)

**SUMMARY:** The Pragmatic Engineer interviews DHH, creator of Ruby on Rails and Omarchy, on his six-month reversal from typing all code to a fully agent-first workflow.

**IDEAS**
- DHH reversed from typing every line to agent-first everything over one winter break with Opus 4.5.
- He runs two agents at once, Kimi K2.5 in open code and Opus in cloud code.
- His tmux layout keeps Neovim left, two agent panes right, and a small terminal strip below.
- He reviews each diff in lazygit with space gg, committing if correct, editing the code otherwise.
- Opus 4.5, dropped November 27th, was his inflection point, first model producing code worth merging unaltered.
- He processed 100 Omarchy pull requests in ninety minutes by telling Claude to review each URL.
- When a PR's diagnosis was right but implementation wrong, he told Claude to clean room it.
- He tested OpenClaw signing up for Fizzy and Hey through a browser with no tools provided.
- OpenClaw created its own Hey email, signed up, then introduced itself inside a Base Camp project.
- 37signals is building CLIs for Base Camp, Hey, and Fizzy so agents can operate them directly.
- Agents can chain tools: read Sentry errors, post to Base Camp, open a GitHub pull request.
- For risky dual-boot work he had Opus draft a plan and Codex critique it back repeatedly.
- Jeremy optimized the fastest one percent of requests, cutting P1 latency tenfold across just twelve PRs.
- The cost of exploring a hunch dropped a thousandfold, so ambitious side projects now get attempted.
- Senior developers gain most from agents because they can validate output quality and redirect when wrong.

**INSIGHTS**
- DHH claims his opinions never changed; the tools finally crossed the quality bar he always demanded.
- Autocomplete felt like interruption; agent harnesses with tools were the real transition from AI to agents.
- Reviewing, not typing, is now the bottleneck, so taste and judgment become more valuable, not less.
- Making software agent-accessible via CLIs revives the Unix philosophy of small composable tools joined by pipes.
- The end state is agents needing no accommodations, but building CLIs bridges the gap for today.
- Ruby on Rails is enjoying a renaissance as one of the most token-efficient agent-friendly web frameworks.
- The productivity pie is exploding, not growing, because agents make previously uncontemplated projects suddenly worth starting.
- Peak programmer may have passed: more software ships, but coding alone no longer commands scarcity wages.
- Designers at 37signals own product, direction, and implementation, working natively in CSS and HTML by themselves.
- Running many agents feels like a mech suit with twelve arms, not like distant project management.

**QUOTES**
- "When something is beautiful, it's likely to be correct." (DHH)
- "I don't actually think my opinions have changed. What have changed is the circumstances and the facts." (DHH)
- "This is really where we transition from AI to agents." (DHH)
- "It produced code I wanted to merge without very much if any alteration." (DHH)
- "I want their code to look as good as mine." (DHH)
- "Running a bunch of agents feels less like being a project manager for agents and more like stepping into this super mech suit." (DHH)
- "In 90 minutes, I think it was, I processed 100 PRs." (DHH)
- "This is the right problem. Let's fix it but let's do it right." (DHH)
- "They validated the fundamental Unix philosophy from like whatever 71." (DHH)
- "The number of projects we have tackled internally that we would never even have contemplated starting on are legion." (DHH)
- "The pie is just exploding right now. It's not growing. It's exploding." (DHH)
- "You could kick it up on a hunch while you go to lunch." (DHH)
- "I do actually think if I was going to bet we've seen peak programmer." (DHH)
- "You have to be better than the agents, right?" (DHH)
- "Remember that this is as bad as they're ever going to be." (DHH)

**HABITS**
- DHH starts every new project agent-first now, letting an agent draft before he reviews or edits.
- He keeps two models running at different speeds, escalating to Opus whenever a problem feels hard.
- He reviews agent diffs in lazygit before committing, refusing to merge any code that looks sloppy.
- He starts major products solo or with one designer until the product shape becomes clear enough.
- He protects eight hours of sleep every night, calling reduced sleep a terrible cognitive trade.
- He refuses to trade health or workouts for extra agent hours, treating that as clearly unsustainable.
- He now avoids opening X first thing after waking, resisting the pull of constant AI news.
- He gives agents vague, half-formed prompts just to see a draft, then reverts freely if wrong.
- He runs his own Omarchy Linux across developer machines to stay close to the production environment.

**FACTS**
- Gmail reportedly handles around 80 to 85 percent of all email traffic in the United States.
- Omarchy gained over 400 code contributors and tens of thousands of daily users within six months.
- Anthropic's revenue reportedly climbed from about 9 billion to roughly 19 billion within the same year.
- OpenClaw is reportedly around 400,000 lines of code, work that once took years and many thousands.
- Shopify's main monolith is roughly 3 million lines built over twenty years by thousands of programmers.
- 37signals employs about 60 people total, including roughly 20 programmers and about 10 dedicated in-house designers.
- Base Camp launched in 2004, near when Facebook went live, and still remains 37signals' biggest product.
- Tesla's 2017 self-driving stack was reportedly 500,000 lines of hand-coded C++, not any actual machine learning.
- GitHub reportedly recorded around 92 percent uptime amid a massive surge in globally produced software lately.

**REFERENCES:** Ruby on Rails; Omarchy (Linux distro on Arch + Hyprland); 37signals; Base Camp; Hey (hey.com); Fizzy (fizzy.do); Kamal; Ubuntu; tmux; Neovim; lazygit; open code / OpenCode; Claude Code; Opus 4.5/4.6; Kimi K2.5; OpenAI Codex; OpenClaw; Sentry; GitHub CLI; MCP; Lex Fridman podcast; Toby Lutki / Shopify; Kent Beck ("Small Talk Best Practices," "Extreme Programming"); Jonas Tyroller (game developer); Steve Yegge; John Carmack; Leopold Aschenbrenner (on the Dwarkesh podcast); "The Bitter Lesson" (paper); Google hiring study; Amazon outage analysis; Uber; Dropbox; Victor Frankl ("Man's Search for Meaning"); Commodore 64; Statsig, Sonar / SonarQube, WorkOS (sponsors); Tesla FSD; Waymo.

**ONE-SENTENCE TAKEAWAY:** Go agent-first but keep your taste; review is the craft, and make your product agent-accessible.

**RECOMMENDATIONS**
- Start every new project agent-first, letting the agent draft while you focus on reviewing and steering.
- Run two models in parallel, a fast cheap one and Opus for the genuinely hard problems.
- Build a small CLI around your own product so agents can operate it like a human.
- Chain tool CLIs and MCPs so one agent moves work across Sentry, GitHub, and your tracker.
- Triage a PR backlog by having an agent review each URL, then judge its final verdict.
- When a contributor's diagnosis is right but code wrong, ask the agent to clean-room rewrite it.
- Kick off speculative hunches you would never staff manually, then revert if the result truly disappoints.
- Never merge agent output that fails your quality bar; hold agents to strict junior-developer review standards.
- Protect sleep, health, and workouts; agent excitement is not a limited-time sale worth burning out over.
- Just try it: open a frontier model, load an unfinished hobby project, and get properly pilled.
