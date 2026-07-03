---
title: "Ch G: Appendix G: Coding Agents -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "G"
pattern: "Appendix G: Coding Agents"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch G: Appendix G: Coding Agents** - Antonio Gulli

> The core "you are the orchestrator of a team of specialist coding agents" framework is already ACS's bread and butter (covered). The one buildable next step is baking a critique-then-reflect reviewer into a native git pre-commit hook so review fires on every commit -> a complement to ACS's Claude Code lifecycle-hook and /code-review videos.

## The one idea worth a video

- **The developer is the orchestrator of a team of specialist agent personas (Scaffolder, Test Engineer, Documenter, Optimizer, Reviewer), each invoked by a role-specific prompt over a human-curated context brief.** This is the load-bearing idea of the appendix; every other principle (primacy of context, direct model access, iterative dialogue) is a corollary of it. VERDICT: ✅ already covered (kept for context).
- **Wire the two-pass "critique then reflect/prioritize" Reviewer Agent into a native git pre-commit hook so a prioritized review of the staged diff prints in your terminal before the commit finalizes.** De-merges from spine 1 because it is a distinct central demo (a `.git/hooks/pre-commit` that shells out to an agent), a distinct SLOT (Master Claude Code -> Hooks), and a distinct "one thing you can do after." VERDICT: 🔗 next-step video available.

## Summary + counts

Gulli frames coding as a human-led team where the developer orchestrates specialist agent personas over meticulously curated context, with prompts version-controlled and review automated via git hooks.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Human orchestrator of specialist agent personas
THE CLAIM: production coding is not "vibe coding" a single blob out of an LLM; it is a human developer acting as team lead who dispatches distinct specialist personas -> Scaffolder (implementer), Test Engineer, Documenter, Optimizer, and a Reviewer -> "not separate applications but conceptual personas invoked within the LLM through carefully crafted, role-specific prompts." WHY IT'S NON-OBVIOUS: the seductive default is one omni-prompt doing everything at once; Gulli argues that splitting the work into role-scoped invocations "ensures the model's vast capabilities are precisely focused on the task at hand." WHY IT'S TRUE / MECHANISM: (1) a narrow persona prompt collapses the model's output distribution toward one job, cutting cross-task interference; (2) each persona gets a purpose-built context brief instead of a diluted mega-context, so signal-to-noise rises; (3) the human stays "the ultimate quality gate," so agent output is "always a proposal, never a command." WHAT IT GENERALIZES TO: this is exactly Claude Code's subagents and slash-command model -> named agents with their own system prompts, tool allowlists, and models. HOW IT GOES WRONG: personas with overlapping remits step on each other (two agents editing one file), and a weak human brief makes even a strong persona useless ("a powerful LLM with poor context is useless"). This is squarely ACS's home turf, hence covered.

### Spine 2 - Critique-then-reflect reviewer in a git pre-commit hook
THE CLAIM: the Reviewer ("Process Agent") should run in two passes -> first a raw critique of every bug/style/logic flaw "much like a static analysis tool," then a reflection pass that "prioritizes the most critical issues, dismisses pedantic or low-impact suggestions," and this whole thing should be automated via "a pre-commit hook configured to automatically trigger the Reviewer Agent on your staged changes," printing the summary "directly in your terminal." WHY IT'S NON-OBVIOUS: most people run review manually and ad hoc, or only in CI on the PR; Gulli's move is to bake review into git itself so it "gates" every commit locally, before code even leaves the machine. WHY IT'S TRUE / MECHANISM: (1) a git pre-commit hook is CLI-agnostic and author-agnostic -> it fires no matter who commits or which editor they use, unlike a Claude Code lifecycle hook; (2) the reflection pass converts a noisy findings dump into a ranked, actionable summary, which is what makes an automatic gate tolerable instead of alarm-fatiguing. WHAT IT GENERALIZES TO: an ACS demo wiring `.git/hooks/pre-commit` (or husky) to shell out `claude -p` / `codex exec` against `git diff --staged`, emit critique-then-reflect, and exit non-zero on a blocker. HOW IT GOES WRONG: a slow agent makes every commit painful; a hook that hard-fails on pedantic findings trains devs to `--no-verify` and abandon it.

## 🎬 Proposed ACS videos

### 1. A Git Pre-Commit Hook That Reviews Your Staged Diff
- **HOOK:** Stop remembering to run /code-review -> make git run the reviewer for you on every single commit.
- **THE PROMISE:** For devs who already know subagent review but run it by hand, wire a native git pre-commit hook so a prioritized critique of your staged diff prints before the commit lands, regardless of which CLI or editor made the change.
- **THE SHAPE:** (1) Write `.git/hooks/pre-commit` (or a husky hook) that captures `git diff --staged`; (2) pipe it to a headless agent (`claude -p` / `codex exec`) with a critique-then-reflect prompt; (3) print the ranked summary in the terminal and exit non-zero only on a real blocker; (4) show the `--no-verify` escape hatch and why the reflection pass keeps it from being annoying; (5) contrast native git hooks vs Claude Code lifecycle hooks.
- **SPINE:** Spine 2
- **SLOT:** Master Claude Code -> Hooks (sits next to "Automatic Plan Reviewing with Other CLIs")
- **RELATIONSHIP:** 🔗 complements "Automatic Plan Reviewing with Other CLIs" by being its next step -> that video wires a PostToolUse ExitPlanMode hook inside Claude Code to critique *plans* before coding; this moves the trigger out of the CLI and into git itself so *finished code* is gated on every commit, author-agnostic, right before it enters history.
- **PROOF TO REUSE:** Gulli's exact "pre-commit hook can be configured to automatically trigger the Reviewer Agent on your staged changes... presented directly in your terminal"; the two-pass "Critique" then "Reflection" structure that "dismisses pedantic or low-impact suggestions"; the principle "An agent's output is always a proposal, never a command."

## 📚 Full wisdom (reference)

**SUMMARY:** Gulli reframes coding as a human-led team: the developer orchestrates specialist agent personas over curated context, versions prompts as code, and automates review via git hooks.

**IDEAS:**
- Vibe coding excels at ideation and beating the blank page, but not production robustness.
- Production work shifts from raw generation to a "collaborative partnership with specialized coding agents."
- The developer is the orchestrator: team lead, architect, and final decision-maker over all agents.
- Three foundational principles: human-led orchestration, primacy of context, direct model access.
- "A powerful LLM with poor context is useless" -> context quality caps agent performance.
- Avoid automated black-box retrieval; curate the briefing (codebase, external docs, human brief) yourself.
- Use direct frontier-model access; intermediary platforms that truncate context degrade results.
- Specialist agents are personas invoked by role-specific prompts, not separate applications.
- The Scaffolder implements features from a detailed brief and existing code patterns.
- The Test Engineer writes unit/integration/e2e suites covering edge cases.
- The Documenter generates markdown docs with request/response examples per parameter.
- The Optimizer proposes performance and refactoring changes with justifications.
- The Reviewer runs a two-pass critique then reflection to produce prioritized feedback.
- A Context Staging Area (a temporary `task-context/` dir of markdown) is the briefing workspace.
- Store invocation prompts as version-controlled markdown in a `/prompts` directory -> prompts as code.
- Automate the review rhythm with git pre-commit hooks triggering the Reviewer Agent.
- Provision at least two frontier models to hedge downtime and enable comparison.
- Lead by maintaining architectural ownership, mastering the brief, gating quality, iterating in dialogue.
- Agent output is a proposal, never a command; the human is the final quality gate.
- Best results come from iterative dialogue and refinement, not a single monologue prompt.

**INSIGHTS:**
- Splitting one model into role-scoped personas focuses capability and cuts cross-task interference.
- The bottleneck of agentic coding is human context-curation quality, not model horsepower.
- Reflection (prioritize, dismiss pedantry) is what makes automated review tolerable rather than noisy.
- Treating prompts as version-controlled code lets a team refine agent behavior collaboratively over time.
- Native git hooks make review author- and CLI-agnostic, gating code before it enters history.
- The human role is elevated, not diminished: strategy and architecture over tactical execution.
- Dual-provider model access is an availability and comparison hedge, like avoiding single-vendor lock-in.
- Automating review at commit time bakes quality assurance into the process, not a later afterthought.

**QUOTES:**
- "A powerful LLM with poor context is useless." - Gulli
- "These agents are not separate applications but are conceptual personas invoked within the LLM through carefully crafted, role-specific prompts and contexts." - Gulli
- "An agent's output is always a proposal, never a command." - Gulli
- "a pre-commit hook can be configured to automatically trigger the Reviewer Agent on your staged changes... presented directly in your terminal." - Gulli
- "Think of your prompt not as a simple command, but as a complete briefing package for a new, highly capable team member." - Gulli
- "over 30% of new code is now assisted or generated by our Gemini models, fundamentally changing our development velocity." - Sundar Pichai, quoted by Gulli

**HABITS/PRACTICES:**
- Prepare a per-task `task-context/` briefing directory before invoking any agent.
- Keep invocation prompts as versioned markdown in a `/prompts` repo directory.
- Provision API keys for at least two frontier models (e.g. Gemini 2.5 Pro and Claude Opus 4).
- Use a `context.toml` config to compile files/dirs/URLs into a single transparent payload.
- Run the Reviewer as critique-first, then reflection-to-prioritize.
- Wire a pre-commit hook to auto-run the Reviewer on staged changes.

**FACTS:**
- Alphabet CEO Sundar Pichai stated over 30% of new code at Google is AI-assisted or generated (early 2025).
- Microsoft (Satya Nadella) made a similar ~30% AI-generated-code claim (April 2025).

**REFERENCES:**
- Models: Gemini 2.5 Pro, Claude Opus 4 / Claude 4 Opus, OpenAI, DeepSeek.
- Tools/concepts: git pre-commit hooks, `context.toml`, `/prompts` directory, `task-context/` staging area, pytest.
- People: Sundar Pichai (Alphabet), Satya Nadella (Microsoft).
- Sources: Reddit r/singularity thread; Business Today article on Microsoft AI-generated code.

**ONE-SENTENCE TAKEAWAY:** Lead coding agents as a specialist team, curate their context, and automate review at commit.

**RECOMMENDATIONS:**
- Split your monolithic prompt into named role personas (scaffolder, tester, documenter, optimizer, reviewer).
- Build a `task-context/` briefing before delegating anything nontrivial.
- Version your agent prompts as markdown in the repo so the team can refine them.
- Add a git pre-commit hook that runs an agent reviewer on the staged diff.
- Have your reviewer prioritize and drop pedantic findings, not just dump every nitpick.
- Keep two frontier models provisioned for comparison and downtime hedging.
