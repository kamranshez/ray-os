---
title: "Ch E: Appendix E: AI Agents on the CLI -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "E"
pattern: "Appendix E: AI Agents on the CLI"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch E: Appendix E: AI Agents on the CLI** - Antonio Gulli

> Net-new: a Terminal-Bench "benchmark your agent instead of vibes-picking it" video. Plus two complements: an Aider-style test-gated auto-commit checkpoint loop, and a "which CLI agent for which task" landscape that sits next to ACS's existing multi-CLI critique videos.

## The one idea worth a video

- **There is no single best CLI agent; you match the tool to the task's shape (architecture, multimodal, git-centric, GitHub-native).** Highest-altitude idea of the appendix - it subsumes all four tool descriptions. VERDICT: 🔗 next-step video available (complements ACS's multi-CLI critique videos, which combine CLIs but never teach how to *pick* one).
- **Aider's defining move is a test-gated commit loop: apply edit, run tests, auto-commit only on green - an auditable, revert-friendly trail.** Distinct demo and distinct "one thing after," so it de-merges from the landscape spine. VERDICT: 🔗 next-step video available (complements "Using Git for Version Control").
- **Terminal-Bench lets you rank agents/models on 80 real terminal tasks empirically instead of by reputation.** Distinct benchmark-driven selection demo. VERDICT: ❌ net-new video available.

## Summary + counts

The developer CLI is becoming an agentic workspace; four agents (Claude, Gemini, Aider, Copilot) each specialize, and Terminal-Bench measures them objectively.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - Match the CLI agent to the task
THE CLAIM: "There is no single 'best' tool; instead, a vibrant ecosystem is forming where each agent offers a specialized strength." WHY IT'S NON-OBVIOUS: the default developer instinct is to adopt one CLI and force every task through it, treating the choice as a loyalty question rather than a routing question. WHY IT'S TRUE / MECHANISM: (1) each agent bakes in a different bias - Claude builds a "mental model of your repository" for architecture-wide refactors, Gemini adds a massive context window plus multimodal image input, Aider commits every successful change to Git, Copilot is assigned a GitHub issue and returns a PR; (2) because "many of the example use cases... can often be accomplished by the other agents as well," the real differentiator is "the quality, efficiency, and nuance of the results," so the smart move is routing a task to the agent whose bias matches it. WHAT IT GENERALIZES TO: ACS's multi-CLI world - Ray already runs Claude Code, Codex and Gemini side by side, so this is a decision framework ("reach for Gemini when you have a screenshot; reach for the git-centric loop when you want a clean commit trail") layered on top of the tools he teaches. HOW IT GOES WRONG: turning routing into tribalism, or over-switching tools mid-task and losing context that one agent had already built.

### Spine 2 - Aider's test-gated auto-commit checkpoint loop
THE CLAIM: an agent should apply an edit, run the tests to validate it, and "automatically commit every successful change," producing "a transparent, auditable trail of all code modifications." WHY IT'S NON-OBVIOUS: most people let an agent churn through many edits and commit once at the end, which fuses good and bad changes into one blob you cannot cleanly revert. WHY IT'S TRUE / MECHANISM: (1) gating the commit on a passing test means every commit in history is a known-good state, so `git revert` becomes a precise undo of exactly the change that broke something; (2) the TDD example - "Create a failing test... Now, write the code to make the test pass" then Aider "runs the test again to confirm" - makes the test the loop's exit condition, not an afterthought. WHAT IT GENERALIZES TO: this is a buildable Claude Code / Codex loop - a hook or skill that runs the test suite after each edit and only commits (with a scoped message) when green, giving Ray's autonomous loops a rollback-safe checkpoint spine. HOW IT GOES WRONG: flaky or slow test suites poison the gate (false green commits, or the loop stalls); a weak test lets a bad change commit as "successful."

### Spine 3 - Terminal-Bench: benchmark agents instead of trusting reputation
THE CLAIM: Terminal-Bench is "a novel evaluation framework designed to assess the proficiency of AI agents in executing complex tasks within a command-line interface" - 80 curated tasks, a standardized minimal agent (Terminus) to isolate the model variable. WHY IT'S NON-OBVIOUS: developers pick agents by hype, Twitter, or the last tool they tried, not by measured task success on their own kind of work. WHY IT'S TRUE / MECHANISM: (1) "the terminal is identified as an optimal environment for AI agent operation due to its text-based, sandboxed nature," so tasks are reproducible and gradeable pass/fail; (2) holding the harness constant (Terminus) while swapping the model turns "which is better?" into a controlled experiment rather than an anecdote. WHAT IT GENERALIZES TO: an ACS video where Ray runs a small terminal-task benchmark against Claude Code vs Codex vs Gemini - or builds a repo-specific mini-benchmark of his own recurring tasks - and picks his default agent/model from the scoreboard. HOW IT GOES WRONG: 80 generic tasks may not predict *your* codebase; optimizing to a public benchmark ("teaching to the test") rewards agents tuned for it over ones better at your real work.

## 🎬 Proposed ACS videos

### 1. Stop Guessing Which Agent Is Best - Benchmark Them
- **HOOK:** "You pick your coding agent from Twitter hype. Here's how to pick it from a scoreboard."
- **THE PROMISE:** For anyone running more than one CLI agent -> after this you can rank Claude Code, Codex and Gemini on real terminal tasks and choose your default from data, not vibes.
- **THE SHAPE:** (1) Introduce Terminal-Bench: 80 sandboxed terminal tasks, and Terminus as the fixed harness that isolates the model. (2) Run a handful of tasks against two or three agents live. (3) Read the scoreboard and interpret it. (4) The upgrade: build a tiny repo-specific benchmark from Ray's own recurring tasks so the numbers actually predict his work.
- **SPINE:** Spine 3.
- **SLOT:** Advanced Techniques -> new chapter "Benchmarking & Choosing Agents" (or Techniques -> Debugging & Verifying Output).
- **RELATIONSHIP:** ❌ net-new. Closest existing video, "Evaluating Code Review Tools," compares PR-review bots against your own backlog; it never runs a task benchmark or isolates a model on standardized terminal tasks.
- **PROOF TO REUSE:** "Terminal-Bench-Core-v0, comprises 80 manually curated tasks"; "Terminus, a minimalistic agent, was developed to serve as a standardized testbed"; "the terminal is identified as an optimal environment... due to its text-based, sandboxed nature."

### 2. The Commit-On-Green Loop: An Aider-Style Safety Net in Claude Code
- **HOOK:** "One giant commit at the end fuses your good and bad changes. Commit only when the tests pass instead."
- **THE PROMISE:** For anyone running agents unattended -> after this you can wire a loop that commits a checkpoint after every passing test, so every point in history is known-good and any regression is a one-line revert.
- **THE SHAPE:** (1) Show the Aider behaviour: edit -> run tests -> auto-commit on success. (2) Rebuild it as a Claude Code hook/skill: post-edit test run, commit with a scoped message only on green. (3) Demo a TDD slice - failing test first, then code to pass. (4) Break something and `git revert` the exact bad checkpoint to prove the auditable trail.
- **SPINE:** Spine 2.
- **SLOT:** Loopy AI (checkpointing for unattended loops) or Master Claude Code -> Hooks.
- **RELATIONSHIP:** 🔗 complements "Using Git for Version Control" by being its next step - that video teaches Git as a safety net and letting Claude Code create commits; this adds the *test-gated, commit-per-successful-change* loop so the safety net is automatic and every commit is green, not just "a commit at some point."
- **PROOF TO REUSE:** Aider "applies edits, runs tests to validate them, and automatically commits every successful change"; the TDD exchange "Create a failing test... Now, write the code to make the test pass"; "a transparent, auditable trail of all code modifications."

### 3. Which CLI Agent For Which Job - A Routing Cheat Sheet
- **HOOK:** "Claude, Gemini, Aider, Copilot. Same tasks, different biases. Stop forcing everything through one."
- **THE PROMISE:** For multi-CLI users -> after this you can route a task to the agent whose built-in bias fits it, instead of defaulting to whichever CLI you opened first.
- **THE SHAPE:** (1) The thesis: no single best tool, the differentiator is result quality per task type. (2) Four biases mapped to task shapes - architecture-wide refactor, screenshot-to-component multimodal, clean git trail, GitHub issue-to-PR. (3) Ray demos two contrasting handoffs on the same repo. (4) A one-slide routing cheat sheet.
- **SPINE:** Spine 1.
- **SLOT:** Advanced Techniques -> Multi-Model & Multi-CLI Workflows.
- **RELATIONSHIP:** 🔗 complements "Combining CLIs & Models" by being its next step - that video teaches using a *second* CLI to critique a diff before shipping; this adds the upstream decision of *which* agent to reach for per task, so combining them is a deliberate choice rather than habit.
- **PROOF TO REUSE:** "there is no single 'best' tool"; "Claude for complex architectural tasks, Gemini for versatile and multimodal problem-solving, Aider for git-centric and direct code editing, and GitHub Copilot for seamless integration into the GitHub workflow"; "the key differentiator... frequently lies in the quality, efficiency, and nuance of the results."

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** Gulli surveys four AI CLI coding agents (Claude, Gemini, Aider, Copilot), each with a specialized strength, and introduces Terminal-Bench for objectively measuring agent proficiency.

**IDEAS:**
- The command line is evolving from a shell into an intelligent, collaborative agentic workspace.
- CLI agents understand natural language, hold whole-codebase context, and run multi-step tasks.
- Many use cases work across all four agents; the differentiator is result quality and nuance.
- Claude CLI builds a "mental model of your repository" for architecture-wide, multi-step refactors.
- Claude's interaction is conversational, like pair programming, explaining plans before executing.
- MCP lets users define custom tools, making Claude a reasoning engine plus user-defined tooling.
- Gemini CLI is open-source with a massive context window and multimodal image-plus-text input.
- Gemini pairs a "Reason and Act" loop with sandboxing and MCP bridges for safety.
- Gemini integrates with Google Cloud for resource management commands like GKE upgrades.
- Aider works directly on files and commits every successful change to Git automatically.
- Aider is model-agnostic, giving users control over cost and capability.
- Aider's TDD flow: write a failing test, then code to pass, then re-run.
- GitHub Copilot CLI's edge is native, deep integration with the GitHub ecosystem.
- Copilot can be assigned a GitHub issue, branch, code, and open a PR autonomously.
- Terminal-Bench evaluates agent proficiency on complex command-line tasks.
- The terminal is an optimal agent environment because it is text-based and sandboxed.
- Terminus, a minimal agent, standardizes comparison across different language models.
- There is no single best tool; the ideal choice depends on the task.

**INSIGHTS:**
- Tool selection is a routing problem, not a loyalty problem; match agent bias to task shape.
- Gating commits on passing tests turns Git history into a series of known-good checkpoints.
- Holding the agent harness constant isolates the model variable for fair benchmarking.
- Sandboxed, text-based terminals make agent behaviour reproducible and gradeable pass/fail.
- MCP is the common extensibility layer that turns a generic agent into a domain-specific one.
- Multimodal input (a screenshot) collapses the design-to-code gap into one prompt.
- Autonomy tiers differ: Copilot's issue-to-PR loop removes the developer from the inner loop entirely.
- "Quality and nuance of results," not feature lists, is the real axis of comparison.

**QUOTES (verbatim):**
- "It is evolving from a simple shell into an intelligent, collaborative workspace." - Gulli
- "The key differentiator between these tools frequently lies in the quality, efficiency, and nuance of the results they are able to achieve for a given task." - Gulli
- "Claude as a reasoning engine augmented by user-defined tooling." - Gulli
- "Its defining feature is its directness; it applies edits, runs tests to validate them, and automatically commits every successful change." - Gulli
- "The terminal is identified as an optimal environment for AI agent operation due to its text-based, sandboxed nature." - Gulli
- "There is no single 'best' tool; instead, a vibrant ecosystem is forming where each agent offers a specialized strength." - Gulli

**HABITS / PRACTICES:**
- Have the agent explain its plan before executing on large-scale changes.
- Add the specific file to context before asking for a bug fix.
- Write a failing test first, then have the agent make it pass (TDD).
- Verify each fix against the existing test suite before accepting it.
- Commit every successful, test-validated change for an auditable trail.

**FACTS:**
- Terminal-Bench-Core-v0 comprises 80 manually curated tasks.
- Tasks span domains such as scientific workflows and data analysis.
- Terminus is a minimalistic standardized agent used as a testbed across models.
- Gemini CLI ships the Gemini 2.5 Pro model with a massive context window.
- Aider is model-agnostic and open-source; Gemini CLI is open-source.

**REFERENCES:**
- Claude CLI (Claude Code) - Anthropic; docs.anthropic.com claude-code cli-reference.
- Gemini CLI - Google; github.com/google-gemini/gemini-cli.
- Aider - aider.chat.
- GitHub Copilot CLI - docs.github.com copilot cli.
- Terminal-Bench - tbench.ai.
- MCP (Multi-tool Control Protocol / Model Context Protocol); OpenAPI; Google Cloud / GKE; slf4j / log4j; TSDoc.

**ONE-SENTENCE TAKEAWAY:** Match the CLI agent to the task, and measure agents on real terminal work.

**RECOMMENDATIONS:**
- Run more than one CLI agent and route tasks by each agent's built-in bias.
- Try Aider's commit-on-passing-test loop for a rollback-safe autonomous workflow.
- Use Terminal-Bench (or a repo-specific mini version) to pick your default agent by data.
- Extend any agent with MCP tools for private APIs, DB queries, and project scripts.
- Feed a screenshot to a multimodal agent to generate matching UI code.
- Assign a GitHub issue to Copilot and review the returned PR rather than coding it yourself.
