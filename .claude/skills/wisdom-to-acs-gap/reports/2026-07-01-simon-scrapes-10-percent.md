# ACS gap report — Simon Scrapes, "You're Only Using 10% of Claude Code"

Source: pasted transcript (no videoId). Channel: Simon Scrapes. Published 17 Jun 2026. Mode: interactive.

## 1. The one idea worth a video

- **The autonomy contract** — don't hand Claude a task, hand it a done-condition that a *second independent agent* verifies before the loop can close (auto mode gates only risky actions; /loop or /routines sets cadence). *Why it's the spine:* it subsumes all of Phase 1 — auto mode, /goal, /loop, /routines are the plumbing around this one reframe. **VERDICT: ✅ already covered (deep-dive kept, no pitch).**
- **The integration escalation ladder** — to automate an app, climb as high as it lets you (API → connector → MCP → browser → full computer-use) and reach for computer-use precisely *because* the app has no API. *Why it's a spine:* distinct demo (drive a no-API app), distinct decision frame. **VERDICT: 🔗 next-step video available.**
- **Put the plan in the repo** — plan mode saves the plan to a throwaway location outside your project, so compaction loses it; persist it in-repo and re-feed it. *Why it's a spine:* concrete, demo-able fix with its own slot. **VERDICT: 🔗 next-step video available.**

## 2. Summary + counts

Simon Scrapes demonstrates four phases making Claude Code run unattended: auto mode plus goals, effort and in-repo plans, an always-on VPS, connectors plus computer-use.

🔴 0 net-new · 🔗 2 complement · 🟡 2 partial · ✅ 1 covered  *(one tally per promoted spine)*

## 3. 🔬 Deep dive

### Spine A — The autonomy contract (✅ COVERED)
The claim: to make Claude run unattended you don't remove the human from approvals, you give the agent a done-condition that a separate agent must verify before the goal can close. Why it's non-obvious: everyone assumes "autonomous" means killing permission prompts (dangerously-skip-permissions), i.e. that friction is the blocker. But that only makes a one-shot prompt run faster — it still stops when the model decides it's "done," which is usually before your real definition of done. The default failure is premature self-declared completion, not permission friction. Why it's true (mechanism): a normal prompt lets the model grade its own finish, so it stops at the first plausibly-complete state; /goal inverts this by making a *second, independent* Claude audit the work against your stated exit condition every turn, so the worker can't sign off on itself and must keep spinning iterations until the auditor agrees. Wrap that in /loop (short tasks) or /routines (weekly) and auto mode's classifier (stops only for deletes/risky ops) and you have a self-restarting, self-checking loop. Generalizes to: CI pipelines — a build isn't "done" at exit-0; a separate test/lint stage gates the merge. Same doer-vs-checker separation of powers. How it goes wrong: the auditor is only as good as the done-condition (a vague "inbox looks clean" gets rubber-stamped), and verifiers drift/go stale when their criteria aren't independent of the plan the worker followed.

### Spine B — The integration escalation ladder (🔗 COMPLEMENT)
The claim: to automate an app, escalate down a ladder — native API → prebuilt connector → MCP → browser automation → full computer-use — and reach for computer-use precisely when the app has no API. Why it's non-obvious: the instinct for "automate this app" is to find its API or build an integration, so apps without one (old, clunky, internal enterprise tools) feel un-automatable. Simon's reframe: the absence of an API is not a wall, it's the signal to drop to the bottom rung and have Claude emulate a human. Why it's true (mechanism): connectors and MCP need the target to expose a programmatic surface; when it doesn't you can't integrate — but you can still *see the screen*. Claude-in-Chrome / computer-use screenshots the page, reasons about which control a human would click, and drives the UI toward a stated goal, so the pixels become the interface. The cost is speed and reliability (slow, research-preview, macOS-first), which is exactly why you only drop to this rung when the cheaper rungs are unavailable. Generalizes to: legacy back-office systems — the mainframe green-screen or the ancient CRM IT will never expose an API for; same move, RPA-style UI automation as the integration of last resort. How it goes wrong: computer-use is slow and brittle to UI changes, and screenshotting authenticated internal apps is a real data-exposure surface (a commenter, ryanarndt1939, flagged exactly this). It's a fallback, not a default — using it where a connector exists is wasteful.

### Spine C — Put the plan in the repo (🔗 COMPLEMENT)
The claim: save the plan as a file *inside* your project repo, not in plan mode's throwaway location, so it survives compaction and the agent keeps checking progress against the steps. Why it's non-obvious: plan mode feels like the whole answer — shift-tab in, get a plan, approve, go. What's hidden is *where* the plan lives: a throwaway folder outside your project/context. It reads reliably for a couple of turns, so the failure is invisible until a long job compacts. Why it's true (mechanism): long jobs compact context to stay under the window; compaction summarizes and drops detail, and a plan sitting outside the project isn't re-read, so post-compaction the agent works off a lossy memory of its own plan and drifts off the steps. Put the plan in-repo and it becomes a durable, re-readable artifact — the plan is re-grounded from disk each turn instead of recalled from a decaying context. Generalizes to: any long-horizon agent state — a running TODO checklist, a migration tracker, a spec. The principle: externalize durable state to a file the agent re-reads; don't trust it to the conversation. How it goes wrong: a stale in-repo plan is worse than none — if you don't revise it as scope changes, the agent faithfully follows an outdated map. It has to be a living file.

## 4. 🎬 Proposed ACS videos (ranked)

### 1. The Escalation Ladder: Automate Any App, Even the Ones With No API
- HOOK: Your ugliest internal tool has no API. That's not a wall, it's the bottom rung.
- THE PROMISE: For devs stuck on a no-API app — after this you can pick the right automation tier and drive a legacy UI to a goal in plain English.
- THE SHAPE: (1) the ladder: API → connector → MCP → Claude in Chrome → computer-use; (2) rule: climb as high as the app allows, drop only when forced; (3) demo a connector on an app that has one (zero setup, authorize once); (4) demo computer-use on a no-API app (screenshots + clicks toward a stated goal); (5) the tradeoff talk: slow, brittle, security surface, keep the human on the final send.
- SPINE: Integration escalation ladder.
- SLOT: CoWork class (beside "Claude in Chrome: Automate the Web") or Master Claude Code connectors chapter.
- RELATIONSHIP: 🔗 complements "Claude in Chrome: Automate the Web" — that video teaches the *mechanics* of browser automation; this teaches *when* to reach for each rung and frames the no-API app as the specific trigger. Don't re-teach the clicking mechanics.
- PROOF TO REUSE: the school.com/scrapes digest demo (returned in ~15 min, 9 posts, "do not reply to any"); "where I see the most value here is those enterprise apps that are old and clunky... no chance of getting any API access"; "you just authorize it once with your normal login and then you talk to it in plain English."

### 2. Put the Plan in the Repo: Why Plan Mode Forgets and How to Fix It
- HOOK: Plan mode works for two turns, then compaction eats your plan. Here's the one-line fix.
- THE PROMISE: For anyone running long jobs — after this you'll persist plans in-repo so the agent stays on-track through compaction.
- THE SHAPE: (1) show the failure: long job, plan made in plan mode, agent drifting post-compaction; (2) why: plan mode saves outside your project, compaction summarizes and the external plan isn't re-read; (3) the fix: write the plan to a project file, re-feed it, have Claude check progress against it; (4) generalize to TODO lists, migration trackers, specs; (5) the gotcha: a stale plan file is worse than none, keep it living.
- SPINE: Plan persistence in-repo.
- SLOT: Context Engineering class (beside "1M Context Window").
- RELATIONSHIP: 🔗 complements "1M Context Window" — that video teaches *why* plans get lost during compaction; this teaches the concrete pre-1M fix (persist in-repo and re-feed). Don't re-explain compaction from scratch.
- PROOF TO REUSE: "by default the plan actually gets saved to a throwaway folder outside of all of our context and project folders"; "as soon as we start compacting the context, it actually starts to lose sight of the plan"; the top comment (digitalrefreshmkt) praising exactly this tip as "a simple fix but makes a huge difference for longer jobs" — social proof it lands.

### Also film-able (not deep-dived)
- **Get Claude Off Your Laptop: The $15 VPS + tmux Always-On Setup** — 🟡 partial; complements "Remote Control" by making self-hosting-to-defeat-session-drop the explicit spine (built-in remotes all drop on disconnect; VPS + tmux + channels is the fix). Slot: Master Claude Code / Automation. Note: "Remote Control" reportedly already lists always-on config, server spawn mode, and tmux persistence — confirm the delta before filming.
- **One Dial for Hard Problems: Effort, Ultra-Code, and Fresh-Context Subagents** — 🟡 partial; synthesizes existing "Reasoning Effort" + "Dynamic Workflows" + "Multi Subagents" into one escalation-dial thesis (context rot + low effort are the two quality killers; the dial from /effort low → max → ultra-code's bespoke fresh-context subagent workflow is the single fix). Slot: Context Engineering.

## 5. 📚 Full wisdom (reference)

### SUMMARY (25 words)
Simon Scrapes demonstrates four phases making Claude Code run unattended: auto mode plus goals, effort and in-repo plans, an always-on VPS, connectors plus computer-use.

### IDEAS
- Auto mode replaces permission-skipping with a background classifier that only halts Claude for genuinely dangerous actions.
- Toggle auto mode by pressing shift-tab twice; Boris Cherny now calls it his number-one productivity tip.
- The /goal command makes you define done, then keeps Claude iterating until an auditor agent confirms.
- A second independent Claude agent audits the work before a goal closes, preventing premature self-declared completion.
- Combine /goal with /loop for short recurring tasks, or with /routines for weekly longer-running scheduled jobs.
- The loop sets the cadence; the goal sets the definition of done; auto mode removes friction.
- Example autonomous job: a daily routine fires to empty the whole inbox into neatly labeled folders.
- Output quality degrades on big tasks from two causes: context rot and insufficient applied reasoning effort.
- The /effort command is a dial for how hard Claude thinks, spanning low through max ultra-code.
- Higher effort spends far more tokens, so reserve extra-high, max, and ultra-code only for warranted tasks.
- Plan mode by default saves the plan to a throwaway folder outside your project and context.
- After compaction Claude loses sight of that external plan, so instead persist plans inside project folders.
- Ultra-code writes its own bespoke workflow, spinning subagents into one of six named Anthropic workflow patterns.
- Each subagent gets a fresh window, so no single context holds too much and never degrades.
- The orchestrator, which is your main conversation window, coordinates subagents so the objective is never lost.
- Built-in remote control opens a Claude session but it drops after ten minutes or on disconnect.
- Channels connect Claude to Telegram or Discord, but the session stays alive only while you're connected.
- Running Claude Code on a cheap always-on VPS with tmux defeats session-drop for real background work.
- Connectors offer literally hundreds of prebuilt, zero-setup app integrations authorized once with your normal everyday login.
- Computer-use lets Claude emulate you inside the browser, screenshotting and clicking its way toward your goal.
- Computer-use shines on the old clunky enterprise apps that offer no chance of any API access.

### INSIGHTS
- The real blocker to autonomy isn't approvals but Claude declaring itself finished before your actual definition.
- Separation of powers, a worker plus an independent auditor, stops any agent from grading its homework.
- Effort and context are the two levers of output quality; both must be deliberately managed together.
- Fresh per-agent windows convert one overloaded context into many clean ones, structurally dodging context rot entirely.
- Where a plan physically lives determines whether it survives compaction, not merely how good its content.
- Every built-in mobile access option shares one fatal flaw: the session dies the moment you disconnect.
- The absence of an API is a signal to drop a rung, not an automation dead-end.
- The limiting factor now is your imagination, not missing features; most previously-impossible tasks are quietly automatable.

### QUOTES
- "You're still sitting at the screen typing one prompt at a time and doing the same work as before." — Simon Scrapes
- "Auto mode is going to eliminate 90% of your approval problem." — Simon Scrapes
- "It's now Boris Cherny's number one tip for getting things done with CL code." — Simon Scrapes
- "There's a second independent Claude agent that audits the work before the goal is actually allowed to close." — Simon Scrapes
- "The loop or routine sets the cadence and the goal sets the definition of what done looks like." — Simon Scrapes
- "By default the plan actually gets saved to a throwaway folder outside of all of our context and project folders." — Simon Scrapes
- "Each of these agents gets a fresh window, so in each of them we don't experience any context degradation." — Simon Scrapes
- "The limitation now isn't missing features. It's actually just what you think is possible inside your head." — Simon Scrapes
- "Claude can now do things in your browser where it effectively emulates you." — Simon Scrapes

### HABITS
- He turns on auto mode by default so approvals never interrupt his multi-step autonomous runs anymore.
- He reserves the highest effort settings only for tasks whose difficulty genuinely warrants that token cost.
- He always saves plans into project folders so Claude keeps tracking its progress against the steps.
- He pairs channels with tmux on a cheap VPS to keep sessions alive while walking away.
- He deliberately starts app automation with connectors first, because they need literally zero technical setup whatsoever.
- He keeps the human in the loop, having Claude summarize community posts but explicitly never auto-replying.
- He builds these workflows live every single week alongside over 1,400 members inside his Agentic Academy.

### FACTS
- Auto mode is toggled by pressing shift-tab exactly twice inside the Claude Code terminal interface itself.
- Anthropic defines exactly six commonly-used agent workflow patterns that ultra-code draws on for its spawned subagents.
- Built-in remote control reportedly drops its session after roughly ten minutes, or immediately upon any disconnect.
- A suitable always-on VPS for continuously hosting Claude Code costs only roughly fifteen dollars per month.
- Channels can reportedly connect Claude to Telegram or Discord in only about five minutes of setup.
- Claude's browser-based computer-use is currently in research preview, macOS-first only, and quite noticeably slow to operate.
- In the live demo, the browser agent returned its finished digest roughly fifteen minutes after dispatch.
- The demo agent found nine member posts spanning the previous twenty-five hours, exceeding the requested twenty-four.

### REFERENCES
- Boris Cherny (Claude Code) — "multi-clotting"/multi-workflow tip; auto mode cited as his number-one tip.
- Claude Code features: auto mode, /goal, /loop, /routines, /effort (low → max → ultra-code), plan mode.
- Ultra-code + Anthropic's six commonly-used agent workflow patterns; orchestrator + subagent architecture.
- Remote control; Channels (Telegram, Discord); tmux; VPS hosting (~$15/mo).
- Connectors (hundreds prebuilt), MCPs, Claude in Chrome, computer-use (research preview, macOS-first).
- Hermes and Open Claw (referenced as background-capable comparisons); Skool community (school.com/scrapes); Simon's Agentic Academy (1,400+ members).
- Simon's separate linked video on the VPS + channels + tmux always-on setup.

### ONE-SENTENCE TAKEAWAY
Stitch auto mode, goals, effort, remotes, and connectors together to make Claude run genuinely unattended.

### RECOMMENDATIONS
- Turn on auto mode with shift-tab pressed twice before ever starting any long unattended Claude run.
- Define done explicitly with /goal so an independent auditor blocks premature completion on your recurring jobs.
- Pair /goal with /loop for short tasks, or with /routines for weekly scheduled recurring background work.
- Raise the /effort dial to max or ultra-code only for genuinely hard, reasoning-heavy, high-stakes coding tasks.
- Move your plan into a committed project file so it survives compaction and guides later turns.
- Provision a cheap always-on VPS with tmux so you can dispatch real background work from mobile.
- Start any app automation with connectors, then escalate to computer-use only for the no-API legacy apps.
- Keep humans in the loop by having Claude summarize and triage messages, but never auto-send replies.

---
LOG: paste — posted — spine: integration escalation ladder (computer-use for no-API apps) — 0 net-new / 2 complement — proposed: The Escalation Ladder; Put the Plan in the Repo
