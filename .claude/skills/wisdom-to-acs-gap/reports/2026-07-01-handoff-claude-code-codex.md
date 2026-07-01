# Gap report: "/handoff is the best skill of all time" — Ben Holmes

Source: https://www.youtube.com/watch?v=_WXc3gA8K6E (11 min, 2026-05-28)

## 1. The ideas worth a video

**Spine 1 — The ambiguity line: pick Claude Code vs Codex by how ambiguous the task is, and walk a single task down that axis.** It subsumes why-start-with-Claude, why-finish-with-Codex, Codex's first-try accuracy, and the Grill-with-Docs / planning-mode moves — they are all consequences of "match the agent to the task's ambiguity." VERDICT: ❌ net-new video available.

**Spine 2 — Handoff documents: move work between agents with a condensed file, not full context.** The /handoff skill writes a portable P0 doc that crosses model providers (Claude→Codex), worktrees, and time; scales up to GitHub issues for 6-10 phase plans. VERDICT: 🔗 next-step video available (beyond the existing "/handoff" video).

**Spine 3 — The Codex plugin for Claude Code (tag Codex in-thread: review / rescue / adversarial).** Load-bearing for understanding the video, but ACS already ships this. VERDICT: ✅ covered — kept for context, no pitch.

## 2. Summary + counts

Ben Holmes shows how to hand off work between Claude Code and Codex: the ambiguity line for agent choice, /handoff documents, and the Codex plugin.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 3. 🔬 Deep dive

### Spine 1 — The ambiguity line
**The claim:** choose your coding agent by how ambiguous the task is — Claude Code for high-ambiguity exploration and planning, Codex for low-ambiguity execution — and deliberately move a task down that axis.
**Why it's non-obvious:** most people are "either diehard Claude Code or Codex fans" and stay loyal to one. The reframe is that loyalty is the wrong variable; the right one is where the task sits on an ambiguity spectrum, and that position changes within a single task.
**Why it's true / the mechanism:** because Codex does deeper upfront codebase research, is less verbose, and "doesn't go off on side quests," it converts a well-specified plan into correct code on the first try — but that same literalness makes it poor where requirements don't yet exist. Because Claude in planning mode (or Matt Pocock's Grill-with-Docs) asks clarifying questions and explores option spaces, it manufactures the requirements Codex needs. Therefore the optimal flow is Claude-first to collapse ambiguity into an actionable plan, Codex-second to execute it. As Ben puts it, "Your goal as an engineer is to go from a highly ambiguous idea space to a low-ambiguity space."
**What it generalizes to:** team staffing — a senior architect scopes the fuzzy problem, then hands crisp tickets to focused implementers. Same shape, humans instead of models.
**How it goes wrong:** the line is fuzzy; a task "is not going to neatly fall into one of these buckets beginning to end." Misjudge it and you get Codex flailing on an underspecified task, or Claude burning tokens re-planning something already concrete.

### Spine 2 — Handoff documents
**The claim:** the cleanest way to move work between agents is a condensed handoff document the current agent writes, not a full-context transfer.
**Why it's non-obvious:** the instinct is to preserve context — fork, compact, or pass the whole conversation. Ben argues the document is better precisely because it is lossy on purpose: a distilled P0 spec, not a transcript.
**Why it's true / the mechanism:** because the handoff is a file (Matt Pocock's /handoff writes it, including suggested skills for the next agent), it is portable in ways a conversation is not — it survives across model providers (paste it into a Codex worktree), across worktrees ("hit Add Worktree… paste in the path… Get going"), and across time (tomorrow, or a cloud agent). Because it is condensed, it is cheaper than mid-conversation model switching, which "will take the full context you have up until that point and pass the context along… more token-expensive." For very large plans the same idea scales: hand off to GitHub issues instead of markdown, so an agent can "pull down this GitHub issue, start working on it, and even post back comments."
**What it generalizes to:** async human engineering handoffs — a strong PR description or design doc lets a teammate resume without a meeting.
**How it goes wrong:** too thin a doc drops context the next agent needs; and for tiny side quests a full handoff is overkill (use /btw or /side instead).

### Spine 3 — The Codex plugin for Claude Code (✅ COVERED — context only, no pitch)
**The claim:** the official Codex plugin lets Claude tag Codex in mid-session for review, rescue, or adversarial passes without leaving the thread.
**Why it's non-obvious:** you don't need to write a handoff or open a new tab to get a second model — the plugin makes it a skill call.
**Why it's true / the mechanism:** because the plugin installs skills into Claude Code, Claude can invoke Codex on the current working tree and get output back inline. Ben's rescue example: Claude declared a terminal-theme change impossible; tagging Codex triggered a deeper web search plus file trace that "found exactly the design tokens to insert, and it worked." The payoff is finishing in one thread. The tradeoff versus a handoff doc: convenient but you "can't really parallelize."
**What it generalizes to:** pair-programming "can you take a look?" — a quick second opinion without a formal handover.
**How it goes wrong:** in-thread means no parallelism, and the convenience can blur which model actually did the work.
**Covered by:** "Codex CLI Plugin" (Master Claude Code / Connecting to Codex) — teaches install, adversarial review, rescue, and background jobs. Excluded from the pitches and the post gate.

## 4. 🎬 Proposed ACS videos (ranked)

### 1. When to Reach for Claude Code vs Codex: The Ambiguity Line
- **HOOK:** stop being a Claude-Code-vs-Codex loyalist; the pros pick per task, and switch mid-task.
- **THE PROMISE:** for engineers running both agents, a single decision rule (task ambiguity) that tells you which to reach for at every step, so you stop guessing.
- **THE SHAPE:**
  1. The ambiguity line — one axis from "no requirements yet" to "fully specified plan."
  2. Why Codex wins the low-ambiguity end — deeper upfront research, less verbose, no side quests, right on the first try.
  3. Why Claude wins the high-ambiguity end — planning mode plus Grill-with-Docs to manufacture requirements.
  4. Live demo: take one real task and walk it down the line — Claude plans, Codex executes in worktrees.
  5. The engineer's real job: converting ambiguity into a low-ambiguity plan.
- **SPINE:** 1
- **SLOT:** Master Claude Code / Connecting to Codex (or Advanced Techniques / Multi-Model & Multi-CLI Workflows)
- **RELATIONSHIP:** ❌ net-new. "Codex CLI Plugin" teaches the plugin mechanics and "Planning Mode" teaches Claude planning, but neither frames a decision rule for choosing the agent by task ambiguity, nor compares Codex and Claude on verbosity/side-quests/first-try grounds.
- **PROOF TO REUSE:** "the ambiguity line"; "Your goal as an engineer is to go from a highly ambiguous idea space to a low-ambiguity space"; Codex "tends to do deeper research on the codebase before it starts working, so it tends to get things right on the first try… less verbose… doesn't go off on side quests."

### 2. Hand Off Work Between Claude Code and Codex with One Document
- **HOOK:** forking and compacting keep the whole conversation; a handoff document keeps only what the next agent needs, and it works across models.
- **THE PROMISE:** for anyone juggling Claude Code and Codex across worktrees, a repeatable way to move a task between agents (even across providers) using a condensed handoff file instead of dumping full context.
- **THE SHAPE:**
  1. The problem: passing full context is expensive and stuck to one thread and model.
  2. /handoff (Matt Pocock) — the agent writes a condensed P0 doc with suggested skills for the next agent.
  3. Demo: Claude writes the handoff → paste the path into a new Codex worktree → "Get going."
  4. Scaling up: for 6-10 phase multi-day plans, hand off to GitHub issues instead — agents pull an issue and post comments back.
  5. The reverse direction: capturing a side-quest bug as a handoff doc to tackle later without derailing.
- **SPINE:** 2
- **SLOT:** Advanced Techniques / Multi-Model & Multi-CLI Workflows (or Master Claude Code / Advanced)
- **RELATIONSHIP:** 🔗 complements "/handoff" (Master Claude Code / Advanced). That video teaches /handoff to resume work in a fresh Claude Code session on the SAME model; this is the next step — the handoff doc as a CROSS-PROVIDER artifact (Claude→Codex) moved across worktrees, plus the GitHub-issues-as-board variant for large plans. Also complements "Combining CLIs & Models."
- **PROOF TO REUSE:** "Slash handoff is a skill written by Matt Pocock. It's very easy to install"; "handoff documents are the absolute best way to take something you're working on and move it to a worktree somewhere else"; "Something I've started doing is handing off to GitHub issues rather than Markdown documents for very large plans"; the Codex-named-the-file-with-literal-Xs gag ("We love you, Codex").

**Also film-able (not deep-dived):** GitHub-issues-as-a-handoff-board for very large multi-day plans could stand alone as a follow-up to pitch 2 (distinct demo: agents pulling issues and commenting back). Multi-model harness switching (OpenCode / Pie / Warp) is already covered by "Combining CLIs & Models," so it is not a gap.

## 5. 📚 Full wisdom (reference)

**SUMMARY** — Ben Holmes shows how to hand off work between Claude Code and Codex: the ambiguity line for agent choice, /handoff documents, and the Codex plugin.

**IDEAS**
- The ambiguity line measures how unclear a task is, guiding whether Codex or Claude fits best.
- Tasks with a clear plan, test-driven development, or a run-until-tests-pass goal fall neatly into Codex's bucket.
- Codex researches the codebase deeply before starting, so it often gets things right on first try.
- Codex is less verbose and avoids side quests, taking instructions literally and finishing the described task.
- High-ambiguity work like exploring designs or building an architecture wiki suits Claude in planning mode best.
- Matt Pocock's Grill-with-Docs skill collaborates on ideas, returning clear engineering requirements from an ambiguous idea space.
- The engineer's real job is converting a highly ambiguous idea space into a low-ambiguity actionable plan.
- Start tasks with Claude to explore the space, finish with Codex executing steps in independent worktrees.
- The Grill-Me skill has the agent ask challenging questions to sharpen your thinking before you plan.
- Matt Pocock's /handoff skill has the agent write a document capturing everything the next agent needs.
- The handoff document lists suggested skills so the next agent begins from a running start immediately.
- Because handoff is a file, you can pass it between different models like Claude and Codex.
- For large six-to-ten-phase plans, hand off work to GitHub issues rather than to plain markdown documents.
- An agent can pull a GitHub issue, work it, and post comments back while it progresses.
- Use handoff in reverse to capture an important side-quest bug without derailing your current main task.
- Small side quests use /btw or /side; bigger ones deserve a separate worktree and commit process.
- The official Codex plugin for Claude Code adds skills that let Claude tag Codex in mid-session.
- The Codex plugin offers code review, a rescue skill, and adversarial modes without leaving Claude Code.
- Codex's adversarial review returned spicy recommendations on Claude's React frontend state-management, then Claude finished the work.
- Codex's rescue skill solved a terminal-theme change that Claude had wrongly declared impossible after deeper searching.
- Multi-model harnesses like OpenCode, Pie, and the Warp terminal let you switch models inside one conversation.
- Switching models mid-conversation passes the full context along, making it more token-expensive than a condensed handoff.
- Staying inside one conversation while switching models means you can no longer parallelize different tasks elsewhere.

**INSIGHTS**
- Agent loyalty is the wrong frame; task ambiguity, not preference, should decide which agent runs it.
- A single task rarely stays in one ambiguity bucket; you walk it downward over time yourself.
- Codex's literalness is a strength during execution but a weakness during open-ended design and exploration work.
- A condensed handoff document beats full-context transfer because it is portable across models, worktrees, and time.
- The handoff document's lossiness is a feature, not a bug: it forces distillation of what matters.
- GitHub issues become a durable handoff board once a plan outgrows a single markdown document's limits.
- The Codex plugin trades parallelism for convenience by keeping the second model inside one single thread.
- Handoff documents parallelize work across worktrees, while in-thread plugins and harness-switching keep you in one lane.
- Reaching for another model to rescue a stuck agent often beats trusting its flat "impossible" verdict.
- Choosing a handoff mechanism is really a tradeoff between flexibility, convenience, parallelism, and total token cost.

**QUOTES** (Ben Holmes)
- "The way I think about it is the ambiguity line, meaning how ambiguous is the task we're trying to work on?"
- "It tends to do deeper research on the codebase before it starts working, so it tends to get things right on the first try."
- "It takes what it's given and accomplishes the task as described."
- "Your goal as an engineer is to go from a highly ambiguous idea space to a low-ambiguity space."
- "I've tended to start things with Claude, especially when we're planning things out, and finish with Codex using delegation strategies."
- "Slash handoff is a skill written by Matt Pocock. It's very easy to install."
- "Something I've started doing is handing off to GitHub issues rather than Markdown documents for very large plans."
- "If you want an example of how literal Codex is, it literally named the file with these Xs instead of filling that in with information. We love you, Codex."
- "Handoff documents are the absolute best way to take something you're working on and move it to a worktree somewhere else."
- "It might be more convenient to just have Claude Code directly tap Codex's shoulder and say, 'Can you look at this?'"
- "I just called Codex adversarial review to see how spicy it would be."
- "I think handoff documents are the most flexible option, but the Codex plugin is pretty freaking cool."

**HABITS**
- Ben starts ambiguous tasks with Claude in planning mode, then finishes execution with Codex in worktrees.
- He runs the Grill-Me skill so the agent challenges his thinking before he finalizes any plan.
- He divides plans into separate worktrees so each Codex agent works independently and fully in parallel.
- He installs Matt Pocock's skills through the Skills CLI, particularly recommending both the Handoff and Grill-Me.
- He uses Warp's Add Worktree, pastes the path into a new Codex session, then says go.
- He tracks very large multi-day plans as separate GitHub issues rather than one big markdown document.
- He captures distracting side-quest bugs into a handoff doc to tackle later without derailing his work.
- He calls Codex adversarial review on Claude's code to surface spicier recommendations before letting Claude finish.

**FACTS**
- Matt Pocock authored both the /handoff and /grill-with-docs skills, distributed publicly through his GitHub skills repository.
- OpenAI publishes an official Codex plugin for Claude Code, hosted at the openai/codex-plugin-cc GitHub repository publicly.
- The Codex plugin bundles code review, rescue, and adversarial-mode skills directly into a Claude Code setup.
- The Skills CLI can add Matt Pocock's skills, letting a user individually select Handoff and Grill-Me.
- Warp terminal provides an Add Worktree action and a built-in agent that supports switching models mid-conversation.
- OpenCode, Pie, and the Warp terminal are coding harnesses allowing model switching within a single conversation.
- Ben is building a game driven entirely by GitHub issues serving as its underlying data source.
- A goal skill runs an agent until unit tests pass, common in both Codex and Claude Code.

**REFERENCES** — Matt Pocock's /handoff skill (github.com/mattpocock/skills); Matt Pocock's /grill-with-docs skill; the Grill-Me skill; the official Codex plugin for Claude Code (github.com/openai/codex-plugin-cc); the Skills CLI; Warp terminal (warp.dev); OpenCode; Pie; GitHub issues and Trello as task boards; /btw and /side commands; Codex CLI, Claude Code, Opus; presenter Ben Holmes.

**ONE-SENTENCE TAKEAWAY** — Match each agent to task ambiguity, then hand work off between them with condensed documents.

**RECOMMENDATIONS**
- Install Matt Pocock's /handoff and /grill-with-docs skills via the Skills CLI to start experimenting with them.
- Route low-ambiguity, well-planned tasks to Codex, and route ambiguous exploration work to Claude's planning mode instead.
- Begin ambiguous work in Claude, then generate a handoff document for Codex to execute in worktrees.
- For six-to-ten-phase plans, split the work into separate GitHub issues instead of one single markdown document.
- Capture disruptive side-quest bugs as handoff docs so a separate worktree agent can tackle them later.
- Install the official Codex plugin so you can tag Codex for review or rescue right mid-session.
- When an agent claims something is impossible, tag a second model to search deeper and verify.
- Use Codex adversarial review to critique one model's code before letting that model finish the implementation.
- Try harness model-switching only when parallelism is unneeded and your company fully subsidizes the token usage.
