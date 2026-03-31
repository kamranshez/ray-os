# Claude Code Source Code Leak — Every Hidden Feature Revealed


## PROACTIVE MODE — Claude That Works While You Don't

This might be the most mind-blowing feature in the entire codebase. Right now, Claude Code is reactive — you type something, it responds. Proactive mode flips that completely. Claude **runs on its own**, receiving periodic heartbeat signals called `<tick>` prompts, and decides autonomously what to do next.

The ticks come from Claude Code's own event loop — it's built into the REPL infrastructure. The system injects `<tick>` XML messages into the conversation at regular intervals (configurable via `proactiveTickIntervalSeconds` in settings). Each tick is like an alarm clock going off. Claude wakes up, looks around, and makes a decision: is there something useful I should do right now, or should I go back to sleep?

The system prompt tells Claude: "You are in proactive mode. Take initiative — explore, act, and make progress without waiting for instructions. Start by briefly greeting the user."

So yes — Claude can **autonomously discover tasks in your codebase and do them**. It could notice failing tests and fix them. It could see a TODO comment and implement it. It could watch for new files and review them. When there's nothing to do, it calls `SleepTool` and goes dormant until the next tick or until something else wakes it up (like a message from Slack via Channels, or a teammate finishing a task).

Any command that takes longer than 15 seconds is automatically pushed to a background agent so Claude stays responsive. This isn't just "run a task and wait" — it's an always-on development assistant that works alongside you.

**Why this matters:** This is the foundation for KAIROS (Anthropic's daemon mode). Proactive mode is available standalone via `/proactive` or `claude --proactive`, but KAIROS wraps it with push notifications, GitHub webhooks, filtered output, and pre-seeded agent teams into a full persistent service.

**Source:** `constants/prompts.ts:860-899`, `main.tsx:2197-2204`

![[images/proactive-mode/excalidraw_1.png]]
![[images/proactive-mode/excalidraw_2.png]]
![[images/proactive-mode/excalidraw_3.png]]
![[images/proactive-mode/excalidraw_4.png]]
![[images/proactive-mode/excalidraw_5.png]]

---

## SKILL IMPROVEMENT — Claude That Learns How You Work

Every 5 user messages, Claude Code silently analyzes your recent interactions in the background. It's looking for one thing: did you correct it, express a preference, or ask it to change how a step works?

Here's the pipeline: it takes your last batch of messages (truncated to 500 chars each for efficiency), pairs them with your current skill definition file, and sends them to Claude with a specific question — "What should change about this skill based on what the user said?" The output is structured JSON: `[{section: "which part to modify", change: "what to add or modify", reason: "which user message triggered this"}]`.

If updates are found, it reads your skill file (`.claude/skills/{skillName}/SKILL.md`), calls Claude again to rewrite it with the improvements integrated, and saves the updated file — preserving your frontmatter, style, and everything you didn't change.

The whole thing is fire-and-forget. It runs in the background after the model finishes responding. You never see it happening. But over time, your skills get better because Claude is learning what you actually want.

**Why this matters:** Skills are the customizable instructions that shape how Claude Code behaves for specific tasks. Right now you have to manually edit them. This feature makes Claude actively improve its own instructions based on your feedback — like a colleague who takes notes on your preferences and adjusts their approach.

**Source:** `utils/hooks/skillImprovement.ts:30-268`

---

## AWAY SUMMARY — "While You Were Away"

If you alt-tab away from your terminal for more than 5 minutes, Claude Code notices. It monitors your terminal's focus state, and after a 5-minute blur, it generates a summary of everything that happened while you were gone.

Think of it like coming back to a Slack channel and seeing "3 new messages since you left." Except Claude writes you a personalized summary of what it did, what changed, and what you might want to look at.

It only fires when no turn is currently in progress and there's no existing summary since your last message. If you come back before it finishes generating the summary, it aborts — no point summarizing if you're already looking.

**Why this matters:** When you're running long background tasks or agent teams that work while you're in another window, coming back to a wall of tool output is overwhelming. The away summary gives you a human-readable catch-up.

**Source:** `hooks/useAwaySummary.ts:12-126`

---

## COORDINATOR MODE — Claude as Project Manager

This one's already partially accessible with `CLAUDE_CODE_COORDINATOR_MODE=1`, but most people don't know about it. Here's how it differs from normal Claude Code:

**Normal Claude Code:** You talk to Claude. Claude does the work itself — reads files, writes code, runs commands. It's one agent doing everything sequentially.

**Coordinator Mode:** You talk to Claude, but Claude **never touches your code directly**. Instead, it acts as a project manager. It spawns worker agents, gives them specific tasks, waits for results, synthesizes findings, and then spawns more workers. The coordinator's entire system prompt (250+ lines) is replaced — it literally becomes a different personality.

The workflow has 4 phases:

1. **Research** — "I need to understand how auth works." Coordinator spawns 3 workers in parallel: one reads the auth middleware, one checks the database schema, one looks at the test suite. They all report back simultaneously.
2. **Synthesis** — Coordinator reads all three reports, identifies conflicts or gaps, and writes a detailed implementation spec. This is the crucial step — the coordinator must actually understand what workers found, not just forward it.
3. **Implementation** — Coordinator spawns workers with the spec: "Modify `auth.ts` to add OAuth2 support. Here are the exact type signatures, here's the test file to update, here's what 'done' looks like."
4. **Verification** — Workers run the test suite, check for regressions, validate the changes.

The prompt explicitly forbids lazy delegation: "Never use phrases like 'based on your findings' — synthesize before delegating." If the coordinator doesn't understand a worker's findings well enough to write concrete file paths and line numbers in the next prompt, it's doing it wrong.

Workers communicate via XML `<task-notification>` messages that include status, summary, token usage, and duration. Workers push results; the coordinator never polls. Workers also get isolated **scratch directories** (shared temp folders) so they can leave notes for each other without modifying your project files.

**Why this matters:** This is a fundamentally different model of AI-assisted development. Instead of one agent doing everything, you get a project manager that parallelizes work across multiple agents. It's like having a tech lead who manages a team of junior devs, except the whole team is AI.

**Source:** `coordinator/coordinatorMode.ts:111-369`

---

## VERIFICATION AGENT — The Adversarial Code Checker

A built-in agent that tries to **break your code** before signing off on it. It's designed to catch the "last 20%" that passing tests miss.

The system prompt explicitly warns against two failure patterns:
1. **Verification avoidance** — reading code, narrating what tests would do, and writing "PASS" without actually running anything
2. **80% seduction** — getting impressed by a polished UI and passing basic tests while missing broken edge cases

Every verification run must: read build/test commands from CLAUDE.md or README, run the build, run the full test suite, run linters and type-checkers, and then run at least one **adversarial probe** — testing concurrency, boundary values, idempotency, or orphan operations.

The agent can't modify your code. It's read-only plus browser automation. But it can create ephemeral scripts in `/tmp` to test things. Output follows a structured format: command run, output observed, result (PASS/FAIL). Ends with `VERDICT: PASS`, `FAIL`, or `PARTIAL`.

Different strategies for different change types: frontend changes get a dev server + browser automation, backend changes get curl requests + error handling tests, bug fixes must reproduce the bug first, database migrations must test up/down reversibility.

**Why this matters:** Right now if you ask Claude to verify its own work, it tends to be optimistic. This agent is specifically prompted to be pessimistic and adversarial — it assumes things are broken until proven otherwise.

**Source:** `tools/AgentTool/built-in/verificationAgent.ts:10-152`

---

## TOKEN BUDGET — "Spend 2M Tokens On This"

Tell Claude "+500k" or "spend 2M tokens" and it tracks consumption against your target. The system treats your target as a **hard minimum, not a suggestion** — Claude keeps working until it approaches the budget.

The system prompt literally says: "When the user specifies a token target, your output token count will be shown each turn. Keep working until you approach the target — plan your work to fill it productively. The target is a hard minimum, not a suggestion."

The decision engine checks three things:
- **Are we at 90% of budget?** If not, keep going. Show a nudge: "Stopped at 87% of target (850,000 / 1,000,000). Keep working — do not summarize."
- **Are we seeing diminishing returns?** If the last 3 continuations each added fewer than 500 tokens, the model is spinning its wheels.
- **Should we stop?** Only when both conditions are met — at 90%+ AND diminishing returns.

Budget parsing supports shorthand (`+500k`, `+2.5m`) and verbose ("use 2M tokens", "spend 1.5b tokens").

**Why this matters:** Right now there's no way to tell Claude "really go deep on this." It tends to wrap up when it thinks it's done. Token budgets let you say "no, I want you to spend $5 worth of compute on this problem" and it'll keep exploring, testing, and refining until it hits the target.

**Source:** `query/tokenBudget.ts:3-93`, `utils/tokenBudget.ts`, `constants/prompts.ts:538-550`

---

## ULTRAPLAN — 30-Minute Cloud Planning Sessions

Normal `/plan` mode runs locally in your terminal. UltraPlan is something else entirely — it spins up a **separate Claude Code instance in the cloud** running Opus 4.6, gives it your full repo, and lets it explore and plan for up to 30 minutes.

Here's the flow:

1. You type "ultraplan" in a message (or `/ultraplan <prompt>`)
2. Claude Code creates a remote CCR (Cloud Code Runtime) session via `POST /v1/sessions`
3. Your git repo state is bundled and uploaded
4. The remote Claude starts in plan mode — it can explore your code, read files, but can't edit anything yet
5. Your local CLI polls every 3 seconds for updates
6. When the remote Claude finishes planning, it calls `ExitPlanMode`
7. You see the plan in your browser on claude.ai and can approve, reject, or edit it
8. If you reject, it loops back for another iteration
9. On approval, you get two choices: **"execute remotely"** (the cloud instance implements the plan and creates a PR) or **"teleport to terminal"** (the plan comes back to your local CLI for you to execute)

Rejected plans are tracked — the system counts rejections and passes that context to the remote agent so it can improve.

**Why this matters:** Local planning is limited by your machine's context and the model's tendency to rush. UltraPlan gives a separate Opus instance 30 uninterrupted minutes to deeply explore your codebase before proposing changes. It's the difference between a 5-minute standup and a 30-minute design review.

**Source:** `commands/ultraplan.tsx:32-382`, `utils/ultraplan/ccrSession.ts:80-349`, `utils/teleport.tsx:730-1185`

---

## TEMPLATES — Repeatable Structured Jobs

This is confusing at first, so let me explain what problem it solves.

Right now every Claude Code conversation is ephemeral. You open Claude, do some work, close it. If you want to do the same type of work again tomorrow, you start from scratch. Templates change that.

With templates enabled, you get three new commands: `claude new` (start a new job from a template), `claude list` (see all your jobs), and `claude reply` (continue an existing job).

Behind the scenes, after every single turn you take, a **classifier** runs in the background. It looks at what you and Claude just discussed and classifies the conversation into a structured "job" — what type of work is this? What phase is it in? What's the status? It writes this to `$CLAUDE_JOB_DIR/state.json`.

Think of it like GitHub Issues but for your Claude conversations. Each conversation becomes a trackable work item with state that persists. You can come back to it later, see where you left off, and pick up exactly where you stopped.

**Why this matters:** This is the infrastructure for turning Claude Code from a chat tool into a task management system. Instead of "open terminal, ask Claude to do thing, close terminal," it becomes "assign Claude a job, check progress later, reply when needed."

**Source:** `entrypoints/cli.tsx:212`, `query/stopHooks.ts:45-132`

---

## BRIEF / SendUserMessage — Filtered Output

Right now, when Claude works, you see everything — every file read, every bash command, every tool output scrolling by. Brief mode changes that. All output goes through a tool called **SendUserMessage**, and Claude only shows you the important stuff.

The output is structured: markdown-formatted message, optional file attachments, and a status flag — either `"normal"` (replying to you) or `"proactive"` (it decided to tell you something on its own).

Three views:
- **Chat view** — only SendUserMessage checkpoints shown, like a clean chat interface
- **Detail view** — checkpoints inline with some tool output, redundant text removed
- **Transcript view** (ctrl+o) — full history with everything visible, like today's Claude Code

**Why this matters:** This is the UI paradigm shift from "watch Claude work" to "let Claude work and tell you what happened." It's the difference between watching a build log scroll by vs getting a Slack message that says "build passed, deployed to staging."

**Source:** `tools/BriefTool/BriefTool.ts:88-134`, `tools/BriefTool/UI.tsx:18-62`

---

## PUSH NOTIFICATIONS — Claude Pings Your Phone

A `PushNotification` tool that sends alerts to your devices. When something important happens (a build fails, a test passes, a teammate finishes), Claude can notify you even if you're not looking at your terminal.

**Why this matters:** Combined with proactive mode and background sessions, this means Claude can work on a task, finish it at 3am, and ping you on Telegram: "PR ready for review."

**Source:** `tools.ts` (gated by `KAIROS || KAIROS_PUSH_NOTIFICATION`)

---

## GITHUB WEBHOOK SUBSCRIPTIONS — Real-Time PR Watching

The `SubscribePR` tool lets Claude subscribe to GitHub PR activity via webhooks. When someone comments on your PR, pushes new commits, approves, or requests changes, Claude gets notified in real-time and can react automatically.

**Why this matters:** Imagine Claude watching your PR, and when a reviewer leaves a comment asking for a change, Claude automatically implements the fix and pushes it. That's what this enables.

**Source:** `commands.ts:101-103` (gated by `KAIROS_GITHUB_WEBHOOKS`)

---

## FORK — Context-Preserving Subagents

The `/fork` command spawns a child agent that **inherits the parent's full conversation context** — unlike the normal Agent tool which starts fresh.

Fork copies the entire conversation history, all tool results, everything. The child picks up exactly where you left off but runs independently in the background. All forked children produce byte-identical API prefixes for maximum cache hits.

**Why this matters:** If you're deep into debugging and want to explore two hypotheses simultaneously, fork lets you branch your conversation like git branches code. Each fork has full context.

**Source:** `tools/AgentTool/forkSubagent.ts:1-211`

---

## TEAM MEMORY — Shared Knowledge Across Your Whole Team

When enabled, Claude Code creates a **shared team memory directory** alongside your personal auto-memory at `~/.claude/projects/<project>/memory/team/MEMORY.md`.

Say you and three colleagues all use Claude Code on the same repo. Each of you has your own personal memory. But the team memory is shared — it lives in the project directory and everyone reads from and writes to the same files.

Claude maintains this like a wiki. When one team member discovers something important ("the payments service is rate-limited to 100 req/s, always use the batch endpoint"), Claude writes it to team memory. The next team member who works on that service gets that context automatically.

The memory has an index file (`MEMORY.md`) capped at ~25KB with one-line pointers to topic files. Topic files contain the actual knowledge, organized by subject.

**Why this matters:** Right now every developer's Claude Code is an island. Team memory creates shared institutional knowledge that builds up over time — like a living documentation system that every team member's Claude contributes to and benefits from.

**Source:** `memdir/teamMemPaths.ts:22-293`, `memdir/memdir.ts:448-472`

---

## BYOC — Bring Your Own Compute

Run Claude Code agents on your own infrastructure. Anthropic provides a Docker image; you run it on AWS, GCP, Kubernetes, wherever. Your code never leaves your network.

The runner registers with the CCR backend, polls for work, receives a `WorkSecret` blob with git repo URL, env vars, MCP configs, and auth tokens. Spawns a child Claude Code process with everything injected.

**Why this matters:** Enterprises can run Claude Code in their own VPC. Plus you could spin up 50 parallel agents on your own K8s cluster.

**Source:** `bridge/workSecret.ts:6-127`, `bridge/types.ts:33-51`

---

## CONTEXT COLLAPSE — Reversible Conversation Archiving

Instead of just summarizing old messages (auto-compact), Context Collapse **archives entire spans** and replaces them with compact summaries. Each archived span has a risk score and can be reconstructed later.

The internal codename is **"marble-origami"** — deliberately obfuscated in the source so it doesn't leak into external builds. Every persist entry is typed `marble-origami-commit` or `marble-origami-snapshot`, not `context-collapse-*`.

Here's how the pipeline works:

**1. Staging — the ctx-agent scores spans**

A background agent called `marble_origami` runs periodically and analyzes your conversation history. It identifies spans (ranges of messages) that are candidates for collapsing and assigns each a **risk score**. Low-risk spans (tool calls, exploratory debugging, answered questions) are safe to collapse. High-risk spans (decisions in progress, uncommitted work) are left alone. The results go into a **staged queue** — an array of `{startUuid, endUuid, summary, risk, stagedAt}` objects, serialized to the transcript as a snapshot entry.

**2. Committing — the projection layer**

When a staged collapse is applied, it's written as a **commit** to the transcript: a `marble-origami-commit` entry containing the span boundaries (first/last message UUIDs), a 16-digit collapseId, a summary string, and a `<collapsed id="...">text</collapsed>` XML placeholder. Crucially, **the original messages are never deleted** — they stay in the REPL's full history. What changes is how `projectView()` reads them.

**3. projectView — the API sees a different history than you do**

Before every API call, `query.ts` runs `projectView()` over the message array. This function replays the commit log and substitutes collapsed spans with their summary placeholders — so the model receives a compressed history without the raw archived messages. Your local REPL still holds everything. This is the "reversibility": uncommit a span, and the full messages are still there.

**4. Overflow recovery**

When the API returns a 413 (prompt-too-long), Context Collapse gets first crack at recovery: it drains all staged spans immediately (`recoverFromOverflow()`), commits them, and retries the request. If that's still not enough, it falls back to reactive compact. This layered approach means you lose the least amount of context possible — granular collapses before the nuclear option of a full summary.

**5. What you see**

The token warning bar shows "N / M summarized" live. The `/context` command runs `projectView()` before calculating token counts, so it shows what the model *actually* sees — not the inflated REPL view. Without this, you'd see "180k tokens" when the API is only seeing 120k (because 3 collapsed spans aren't visible to the model but were being counted).

**Why this matters:** Auto-compact destroys your history. One big summary replaces everything. Context Collapse is surgical — it picks the lowest-risk spans, keeps your live context intact, and can undo any collapse that turns out to have been a mistake. When Context Collapse is enabled, auto-compact is disabled entirely; the system now "owns" context management and handles it more precisely.

**Source:** `types/logs.ts:238-295`, `commands/context/context.tsx:20`, `query.ts:428-447`, `query.ts:1086-1116`, `utils/sessionStorage.ts:1541-1580`

---

## CCR MIRROR — Watch Without Touching

Read-only mode where your local work is visible on claude.ai but nobody can control it remotely. Only outbound events flow; inbound control requests rejected.

**Why this matters:** Visibility without giving up control. Good for demos, monitoring, or showing teammates what you're working on.

**Source:** `bridge/bridgeEnabled.ts:197-202`, `bridge/replBridgeTransport.ts:340-345`

---

## TERMINAL PANEL — Persistent Shell with Meta+J

A tmux-based shell that lives alongside Claude Code. Press **Meta+J** to flip between Claude and a full interactive shell that persists across your session.

**Why this matters:** No more exiting Claude Code to run a quick command.

**Source:** `utils/terminalPanel.ts:25-192`

---

## BACKGROUND SESSIONS — `claude ps/logs/attach/kill`

Launch background sessions with `--bg`. Manage with `claude ps`, `logs`, `attach`, `kill`. Sessions detach (not die) on ctrl+c.

**Why this matters:** Run multiple Claude agents simultaneously. Start a refactoring job in the background, keep coding in your main session.

**Source:** `entrypoints/cli.tsx:185`, `utils/concurrentSessions.ts:1-205`

---

## SETTINGS SYNC — Cloud-Synced Preferences

Bidirectional sync of settings and memory between local CLI and cloud. Your keybindings, permissions, memory files follow you everywhere.

**Source:** `services/settingsSync/index.ts:1-582`

---

## CONNECTOR TEXT — Anti-Distillation Defense

Server-side encoding that prevents unauthorized model training on Claude's output. Content blocks cryptographically bound to your API key. The DRM of AI output.

**Source:** `constants/betas.ts:23-25`, `utils/betas.ts:279-298`

---

## BUDDY — Your AI Tamagotchi Pet

Every user gets a **deterministic generative companion** — a little creature that sits beside your input box in a speech bubble.

When you run `/buddy`, Claude Code hashes your user ID with Mulberry32 PRNG and generates your companion. You don't choose — it's assigned like a starter Pokemon.

**18 species**: duck, goose, blob, cat, dragon, octopus, owl, penguin, turtle, snail, ghost, axolotl, capybara, cactus, robot, rabbit, mushroom, chonk. Hand-drawn ASCII art with 3 animation frames cycling every 500ms.

**Rarity**: common (60%), uncommon (25%), rare (10%), epic (4%), legendary (1%). Plus 1% shiny chance. Cosmetics: 6 eye styles, 8 hats. **5 stats**: DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK.

First hatch: Claude generates a unique name and personality. Stored permanently. Never regenerated.

Release: April Fools teaser April 1-7, 2026. Live for real May 2026.

**Why this matters:** It's delightful. And it shows Anthropic is thinking about emotional connection with their tools, not just utility.

**Source:** `buddy/types.ts:54-73`, `buddy/sprites.ts:26-515`, `buddy/companion.ts:62-134`