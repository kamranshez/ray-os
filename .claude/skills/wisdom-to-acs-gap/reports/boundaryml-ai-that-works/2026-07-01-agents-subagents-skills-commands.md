---
title: Agents, Subagents, Skills and Commands
videoId: b5O6gb_Zuk8
url: https://www.youtube.com/watch?v=b5O6gb_Zuk8
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works (Dex, HumanLayer + Vaibhav, Boundary)
---

## The one idea worth a video

**Spine 1 (the reframe). Context isolation and instruction modules are two orthogonal jobs, and subagents got overloaded to do both.** Once you see the split, the whole commands / skills / subagents taxonomy collapses into one decision: do you need a fresh context window, reusable instructions, both, or neither. This subsumes the "play house" anti-pattern, the removed slash-command tool, and why skills beat subagents for bundling instructions.
VERDICT: net-new video available (fills the empty `skills-vs-subagents` placeholder).

**Spine 2 (de-merged technique). For multi-repo agent work, a thin coordination repo with `additionalDirectories` beats git submodules and symlinks.** A different demo and a different slot from Spine 1, so it films as its own video.
VERDICT: net-new video available.

**Spine 3 (complement). Every subagent, skill, and MCP tool injects its description into the tool block on every turn, and tool-search / lazy skills is the fix.** The exact instruction-budget argument the school already makes for MCPs, now generalized to all three primitives.
VERDICT: next-step video available (complements `clis-vs-mcps`).

Also present but NOT promoted (already covered): "code volume was never the bottleneck, design review is" is `the-shifting-bottleneck` (start-here); "throw away a wrong design and rebuild" is `build-it-twice` (techniques). Left in Full wisdom, no pitch.

---

## Summary + counts

Dex from HumanLayer and Vaibhav from BoundaryML whiteboard the difference between commands, skills, agents, and subagents inside coding harnesses like Claude Code, plus multi-repo distribution.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

**Spine 1. Context isolation and instruction modules are orthogonal.**
The claim: a subagent quietly does two unrelated jobs at once, and skills exist to pull those jobs apart. What most people get wrong is treating subagents as the way to package reusable instructions, so they build a "backend engineer" and a "frontend engineer" agent and model their company org chart. Dex is blunt that this "playing house" does not work. The mechanism: a subagent both opens a fresh context window (isolation) and carries custom instructions (a module). If all you want is a reusable instruction module in your MAIN context, a subagent forces an unwanted new window on you. That is why Claude Code once shipped a slash-command tool: a hack to inject a module into the parent context. Skills are the clean version, invokable in the parent or a child, and their instructions arrive as a user message, which, as Dex notes, "tool results get a different level of attention than user message." This generalizes cleanly to ordinary software: a pure function (reusable logic) is not the same primitive as a forked process (isolation). It goes wrong when people forget skills still cost description budget, and that a subagent's output is only as good as the parent's handoff prompt.

**Spine 2. A coordination repo beats submodules for multi-repo work.**
The claim: when your work spans many repos, do not reach for git submodules or an umbrella repo, build a thin coordination repo instead. The non-obvious part is that the "correct" engineering instinct (submodules, umbrella repos) is exactly what breaks the agent. The mechanism: a coordination repo holds a tiny CLAUDE.md and a settings.json that lists the sibling repos as `additionalDirectories`. You run Claude from that repo and it reads and writes across all of them as though it were a monorepo, without the model ever having to reason about nested-repo indirection. Dex is explicit that submodules "does not work" for the model and symlinks "break builds," whereas the coordination repo "just gets out of the way." Vaibhav, who cannot use a monorepo across 200 repos and thousands of engineers, lands on the same pattern (the RPI coordination template) plus per-task worktrees. This generalizes to the same "flatten the mental model for the agent" principle behind choosing a CLI over an MCP. It fails if repos are not checked out at the same level, or if the additional-directory permissions are not granted.

**Spine 3. Subagents, skills, and MCP tools all tax one instruction budget.**
The claim: the model has a finite instruction budget, and every subagent, skill, and MCP tool you install spends it, because each one's description is injected into the tool block on every single turn. The non-obvious part is that people believe skills are "free" because they are dynamic, but by default their descriptions are still all advertised in the tool block, and MCP is the worst offender because one server can expose twenty-seven tools. The mechanism, in Dex's words: "your tools block in your context window is getting longer and longer and it's detracting from its ability to pay attention to the user instructions." More primitives, longer tool block, degraded attention to your actual task. The fix is tool search, which the team reportedly triggers once your tools exceed ten thousand tokens of context, turning skills into lazily loaded entries so only relevant ones inflate the window. This is exactly the argument the school already makes for MCP schemas, generalized to all three primitives. It goes wrong when keyword tool-search misses the right skill, or when under-advertising a skill means the model never finds it.

---

## 🎬 Proposed ACS videos

### 1. Skills or Subagents? The Two Questions That Decide
- HOOK: You have been using subagents to do a job skills were built for, and it is quietly costing you context.
- THE PROMISE: For anyone drowning in commands, skills, and subagents, one 2x2 that tells you which primitive to reach for every time.
- THE SHAPE: (1) The two axes: context isolation vs instruction modules. (2) The "play house" anti-pattern and why role subagents fail. (3) The slash-command-tool history as a hack for injecting modules into the parent. (4) Skills as the clean fix, and why user-message injection beats a file read. (5) The 2x2 decision: isolation, module, both, or neither.
- SPINE: 1
- SLOT: Claude Code > (fills the empty `skills-vs-subagents` draft; sits alongside `hooks-with-slash-commands-skills-subagents`)
- RELATIONSHIP: ❌ net-new. The `skills-vs-subagents` draft is a named-but-empty placeholder ("Placeholder"), so nothing in the catalog actually teaches this decision. The two-axis framing is exactly the content that slot needs.
- PROOF TO REUSE: "separate out instruction modules from context"; "these are two orthogonal concepts, don't put your custom instructions in agents"; "tool results get a different level of attention than user message"; the backend/frontend "playing house" story.

### 2. One Coordination Repo Beats Your Git Submodules
- HOOK: Everyone reaches for git submodules to run an agent across many repos, and the model handles them terribly.
- THE PROMISE: For anyone whose work spans more than one repo, a setup where Claude treats all of them as one, without submodules.
- THE SHAPE: (1) Why submodules and umbrella repos break the model. (2) The monorepo ideal and when it is not feasible. (3) Build a thin coordination repo: tiny CLAUDE.md plus settings.json `additionalDirectories`. (4) Run every session from there; per-task worktrees for the repos you touch. (5) Symlinks vs coordination repo tradeoffs.
- SPINE: 2
- SLOT: Claude Code > Workspace Organization (currently a backlog idea only)
- RELATIONSHIP: ❌ net-new. No catalog video covers multi-repo coordination, `additionalDirectories`, or the coordination-repo pattern; `workspace-organization` exists only as an unwritten backlog item.
- PROOF TO REUSE: the RPI coordination template; "everyone should do a mono repo, literally fix it today"; "get submodules... it just is not ergonomic for the model"; the ln -s symlink habit and its build-breaking caveat.

### 3. Your Skills Are Bloating Context Just Like MCPs
- HOOK: You audited your MCP servers for context bloat, then installed forty skills and undid all of it.
- THE PROMISE: For anyone running many skills or subagents, how to keep your tool block from eating the model's attention.
- THE SHAPE: (1) The finite instruction budget. (2) Every subagent, skill, and MCP tool description injects on every turn. (3) Show the raw tool block growing in a trace. (4) Tool search / lazy skills and the ten-thousand-token threshold. (5) Audit and prune: keep descriptions small.
- SPINE: 3
- SLOT: Context Engineering > (next to the shipped `clis-vs-mcps` in fundamental-techniques)
- RELATIONSHIP: 🔗 complements `clis-vs-mcps` by being its next step. That video already teaches that MCP schemas load into context every turn and cost roughly sixty thousand tokens for GitHub alone; this adds that subagents AND skills pay the identical tax, and that tool-search / lazy skills is the mechanism that fixes it across all three primitives.
- PROOF TO REUSE: "every single subagent you add to your context window is going to be injected every time"; "if you have hundreds of subagents... you get screwed"; the twenty-seven-tools-per-MCP-server point; the tool-search ten-thousand-token threshold.

---

## 📚 Full wisdom (reference)

**SUMMARY**
Dex from HumanLayer and Vaibhav from BoundaryML whiteboard the difference between commands, skills, agents, and subagents inside coding harnesses like Claude Code, plus multi-repo distribution.

**IDEAS**
- Context isolation and instruction modules are two orthogonal concepts; conflating them is why subagent role-play fails.
- Subagents exist for context isolation: burn fifty thousand tokens searching, return a tiny answer to parent.
- Modeling subagents as company roles like backend engineer or data scientist is playing house, ultimately useless.
- Custom subagents guarantee fixed instructions no matter what prompt the parent writes, decoupling quality from prompting.
- Skills replace slash commands but add explicit invocation, so you need not hope model picks them.
- Loading a skill injects instructions as user message, which model follows better than plain file reads.
- Every installed subagent, skill, and MCP tool injects its description into the tool block every turn.
- The GitHub or HubSpot MCP alone can break sessions because its many tool schemas flood context.
- Tool search activates once ten thousand context tokens are tools, turning skills into lazily loaded entries.
- disableModelInvocation hides a skill from the model entirely, leaving it usable only through explicit slash invocation.
- Forking a session rewinds to a user message, injects discovered answer, and continues without polluting context.
- A context-fork subagent inherits the parent's full context, useful for one orthogonal question during iteration loops.
- Vaibhav deleted his GitHub-comment slash command once he could simply tell Claude to run the CLI.
- Prescriptive single workflows beat seven half-baked per-engineer ones; consolidation lets you optimize that one path everywhere.
- Fewer skills beats more; every extra skill is something you must teach ten teammates to use.
- For multi-repo work, a coordination repo with additionalDirectories beats git submodules, which models handle absolutely terribly.
- A monorepo makes agent tooling trivial: shared .claude config just works across everything, no symlinking required.
- Skills bundle reference files for progressive disclosure; the skill receives its own base directory at invocation.
- The slash-command tool, now removed, once let instruction modules run in the parent context, not just subagents.

**INSIGHTS**
- The right mental model is a two-by-two: do you need isolation, instruction reuse, both, or neither?
- Subagent quality equals parent-prompt quality; a bad handoff prompt hallucinates, omits information, and returns malformed results.
- Claude Code's history, commands, subagents, slash-command tool, skills, shows a team iterating toward correct abstractions publicly.
- Code volume was never the bottleneck; humans reviewing design and confirming correctness is the real constraint.
- Context engineering is a one-time purchase, not recurring, so a prompt alone cannot sustain defensible business.
- Leaning fully into lights-off agent swarms risks unmaintainable slop nobody understands when it breaks at 3am.
- Model-swappable harnesses mean anyone paying the token bill can eventually observe and extract your engineered prompts.
- Agent-team result quality is proportional to how well you decomposed the problem beforehand, not raw parallelism.
- You can reuse Claude Code's own code-review prompts rather than paying for a separate code-review product.

**QUOTES**
- "these are two orthogonal concepts. And so like don't put your custom instructions in agents." (Dex)
- "It's not just reading a file and getting the stuff because tool tool results get a different level of attention than user message." (Dex)
- "Every single subagent you add to your context window is going to be injected every time." (Dex)
- "if you have hundreds of subagents, Yeah, you get screwed." (Vaibhav)
- "you get way better alpha being more prescriptive when possible in as many things as possible" (Dex)
- "Everyone should do a mono repo. If you haven't done a mono repo, literally fix it today." (Vaibhav)
- "shipping more code faster, like more tokens of code, was never the bottleneck." (Dex)
- "Before you code, you need to spend your own thinking tokens." (Dex)
- "Context engineering is a one-time purchase. It's not a permanent purchase." (Vaibhav)
- "if you can use cloud code to write the code, then like cloud code can review the code." (Dex)
- "the quality of the sub agent result is directly related to like how good is the prompt that the parent model gave it" (Vaibhav)
- "you're populating things twice... it's like pointer indirection almost for no reason." (Vaibhav)

**HABITS**
- They run a code-review step with a separate context window before shipping any pull request out.
- They aggressively delete generated code they judge to be shitty, unmaintainable slop rather than keeping it.
- Vaibhav symlinks his open-source repo into the backend repo with ln -s so it behaves monorepo-like.
- Dex forks a session the moment he spots the answer, discarding ten thousand tokens of exploration.
- They launch a subagent whenever a task, like Playwright browsing, will flood context with DOM noise.
- They keep skill descriptions small because that advertised text competes for the model's limited instruction budget.
- They add a phrase telling the model not to invoke a skill unless asked by name.
- They run all sessions from a coordination repo whose settings.json lists sibling repos as additional directories.
- They open-source their RPI commands and prompts, trusting that good design partners will still pay anyway.

**FACTS**
- Amazon now bars L1 to L3 engineers from shipping AI-generated code without a senior engineer's review.
- Claude Code's tool search reportedly activates once your tools exceed ten thousand tokens of context window.
- An MCP server exposing twenty-seven tools injects all twenty-seven schemas into every session's context window automatically.
- The Claude agent SDK simply wraps the Claude Code CLI binary, behaving identically with correct flags.
- The Max plan reportedly sells around three thousand dollars of inference for two hundred dollars monthly.
- Anthropic's terms now forbid using a Max plan to serve inference to a SaaS product's users.
- Claude Code originally aimed to drive traffic to Anthropic's platform by proving the models' coding strength.
- Dex has whiteboarded this commands-versus-skills-versus-agents distinction by hand roughly seventy times before recording this whole episode.

**REFERENCES**
HumanLayer; Boundary / BAML programming language; Claude Code; Codex; OpenCode; Claude agent SDK; RPI coordination template and RPI commands (open source); Playwright; Sentry; Drizzle migrations; GitHub MCP; HubSpot MCP; Conductor; Riptide; Theo's OpenCode-style competitor; Dax (post on shipping too much code); Jeff (the "moo like a cow" attention-check idea); Tariq (Claude Code team, disableModelInvocation flag); Amazon internal AI-code-review policy; the "AI That Works" podcast; the April 11th unconference.

**ONE-SENTENCE TAKEAWAY**
Separate context isolation from instruction modules; pick subagents, skills, or forks by which you need.

**RECOMMENDATIONS**
- Stop bundling custom instructions inside subagents; use skills so those modules work in your parent context.
- Audit installed skills, subagents, and MCP servers; uninstall ones bloating your context window's tool block unnecessarily.
- Replace bespoke slash commands with plain CLI calls whenever telling Claude to run the tool suffices.
- Fork a session once the answer appears, discarding thousands of exploration tokens before continuing your work.
- Set disableModelInvocation on skills you only want triggered deliberately through explicit slash invocation, never fired automatically.
- For multiple repos, build a coordination repo using additionalDirectories rather than fighting with painful git submodules.
- Consolidate your team onto one prescriptive workflow instead of maintaining seven half-baked per-engineer workflow variations forever.
- Add a code-review pass in a fresh context window checking known anti-patterns before shipping every PR.
- Spend real thinking tokens designing before coding, since throwing away a wrong design beats hacking forward.
