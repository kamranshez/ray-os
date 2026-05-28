---
tags: [loopy-ai, inbox, sources, twitter]
date: 2026-05-28
status: inbox
---

X/Twitter sources gathered for the Loopy AI class. Fetched via the Supadata MCP (metadata + transcript) and Chrome where Supadata was blocked. Grouped by relevance to the loop theme.

## Tier 1 — core loop material

### Jarrod Watts — "You Need More Than a Ralph Loop"
https://x.com/jarrodwatts/status/2052372045829382430 (82.9K views, May 7)

The strongest single piece. Argues long-running agents work because they spend more tokens (test-time compute), but break down when the task needs more context than the window holds, which is why Ralph loops exist. He read the open-source Codex `/goal` internals: a SQLite `thread_goals` table (objective, id, status, optional token budget), `get_goal` / `update_goal` tools, and a standard Ralph-style repeated prompt with a completion audit. His verdict: `/goal` underwhelms, and his own workflow beats it. Three reasons and his fixes:

- **Ambiguity compounds** — each iteration's output is the next one's input, so one off-taste decision drifts everything after it. Fix: an `/interview` skill (like Matt Pocock's grill-me) in a *setup phase* before any autonomous loop, turning a vague goal into a specific milestone/task tree. Invest upfront to cut off the wrong branches.
- **Multi-agent beats single agent** — orchestrator plus subagents (implementer + reviewer going back and forth) "mogs" one good agent. Horizontal token scaling. Reviewer sees code fresh, no prior bias.
- **Cross-context memory** — after planning, agents create/read/maintain `GOAL.md`, `STANDARDS.md`, `IMPLEMENT.md`, `PROGRESS.md` so each fresh context picks up aligned with prior decisions.

Skill repo: https://github.com/jarrodwatts/long-running-agent-skill (packaged SKILL.md, parallelises across subagent teams via git worktrees, recommends GPT 5.5 xHigh in the Codex App).

### Avi Chawla — "The anatomy of a perfect /goal prompt in Claude Code"
https://x.com/_avichawla/status/2055930732930122158 (27.6K views, May 17)

Direct material for the "Writing Effective Goals" topic. Explains the loop mechanism: two models run together. Sonnet/Opus does the coding; after each turn Haiku reads the full transcript and checks completion conditions; if not met, the worker auto-runs another turn. Haiku is cheap, the worker is not, so the condition you write controls how many expensive turns you pay for.

Anthropic recommends three things in a `/goal` condition: a measurable end state, a stated check, and constraints, plus a turn cap. Failure modes the docs skip: a vague condition ("make the app production-ready") loops forever because nothing proves it; a subjective one ("complete the migration") lets the worker self-report and Haiku accepts it because the judge only sees the transcript.

The 9-section template (from a community template circulating on X, found via findskill.ai):
- **GOAL** — objective in one sentence
- **CONTEXT** — background so it doesn't waste turns exploring
- **CONSTRAINTS** — hard scope boundaries
- **PRIORITY** — execution order, easy wins first
- **PLAN** — explicit approach, no aimless exploration
- **DONE WHEN** — binary, observable outcome (`pytest exits 0`), never subjective
- **VERIFY** — a specific command whose raw output lands in the transcript so Haiku judges machine evidence
- **OUTPUT** — what to surface when done
- **STOP RULES** — turn limit caps the downside

Stronger still: pair `/goal` with a Stop hook that runs tests / hits CI after every turn, moving verification from the prompt layer to the infrastructure layer.

### Bootoshi — "Mastering overnight workflows with Codex /goal mode" (video)
https://x.com/kingbootoshi/status/2052510026535936157 (20.9K views, May 7) — full transcript captured

11h26m overnight run building "Agent Runtime Kernel" (secure micro-VM sandboxes for agents). Calls `/goal` "a 10x more reliable version of the Ralph loop." Workflow:

- Write a *big* detailed PRD (his was ~1500 lines), researched via Codex + Exa web search, with explicit goals/non-goals.
- Set `/goal implement this PRD fully`. Every time Codex compacts, goal mode re-pings to keep it focused; it re-reads the PRD to get back on track. Compaction quality is what makes it hold course.
- The goal must have an *end* (PRD fully implemented) or it runs forever.

The real lesson is the **guardrails that make autonomous code trustworthy** (enforced in code so agents can't cheat):
- strict TypeScript (won't build on bad types)
- Biome formatter + linter, custom ESLint architectural guardrails set at greenfield
- file size cap (~500 lines), no-god-functions / cognitive-complexity rules force decomposition
- centralized logger; harness that blocks agents from skipping tests
- Knip to delete dead code so agents don't get confused grepping
- lefthook pre-commit (biome + eslint + typecheck must pass; `--no-verify` disabled)
- three test layers: unit (mocks), integration (real SQLite, real migrations), real end-to-end (Docker, real prod-like env). A written testing philosophy to kill useless `1+1==2` mock tests.

Punchline: with guardrails + master PRD + goal mode, "done means proper because of our guardrails." He compares the implement/test/find-problem/fix feedback loop to "autoresearch on steroids." Lets him run many projects in parallel.

### Vincent Koc — "/goal is not a do-my-ticket button" (thread)
https://x.com/vincent_koc/status/2050983370902184019 (288K views, May 3)

~3 days on OpenClaw, 13 runs, many PRs. Key line for the class: "/goal is not a 'do my ticket' button. It's a **constraint workflow**. I want to keep the ship on course." (Thread continues with what works; opener carries the thesis.) Pairs with the constraint/guardrails angle from Bootoshi and nexxeln.

### Greg Brockman — how to use /goal in Codex
https://x.com/gdb/status/2056430780809892252 (234K views, May 18)

"how to use /goal in codex — keep Codex working on a persistent objective until it's solved." Authoritative one-liner definition of goal mode from OpenAI's president. Good for the cold-open / "this is now first-party" beat.

## Tier 2 — loops for review and quality gates

### Peter Steinberger — /review in a loop
https://x.com/steipete/status/2054850632067019173 (399K views, May 14)

"Wrote a skill that runs codex /review in a loop until there's no booboos anymore. Caveat: it won't fix system architecture for ya, so you still need BRAIN as master model." Concrete review-loop example. Use under "Closing the Loop" / loops-for-verification.

### eric zakariasson — /thermo-nuclear-code-quality-review (Cursor internal)
https://x.com/ericzakariasson/status/2057521364622553442 (458K views, May 21) — video

"Most used skill internally at Cursor right now." Deletes complexity instead of moving it, blocks files over 1k lines, flags thin wrappers and leaked logic, rejects PRs that work but make code messier. Quality-gate skill, complements the guardrails theme.

### Kappaemme — codex-complexity-optimizer
https://x.com/kappaemme1926/status/2055343704467206506 (294K views, May 15) — video

Codex skill that scans for complexity hotspots (O(n²), N+1, repeated scans), gives before/after complexity estimates and safe optimization suggestions, report-only by default. `npx --yes codex-complexity-optimizer`, open source. Another loop-able quality skill.

## Tier 3 — supporting / adjacent

### nexxel — agent-friendly codebases are about constraints
https://x.com/nexxeln/status/2054488859376075027 (43K views, May 13)

"good architecture boxes agents into writing specific, constrained code, fewer ways to go wrong." Migrating opencode to Effect made agent code "noticeably less cursed." Reinforces the guardrails-make-loops-safe argument.

### David K (xstate) — prototypes as specs
https://x.com/DavidKPiano/status/2052448434142269741 (28K views, May 7)

"the spec should fall out of the prototype, not the other way around. One prototype is worth 100 spec drafts." Tagged in notes as "Prototypes as Specs." Adjacent to the setup-phase / spec idea, maybe a different class but noted here because it sat in the same workshop note.

### Tricknologist — OpenAI harness engineering + /goal plan templates
https://x.com/cheddarmandem/status/2051591432079569027 (May 5)

Points to OpenAI's Feb harness-engineering article and example "executive plan" templates that work with `/goal`. Chase these links for first-party `/goal` plan structure to compare against Avi's template.

### Alex Raber — "Half baked" (reply to Matt Pocock)
https://x.com/raberhalex/status/2055267973783527652 — low signal, a reply. Skip unless the Pocock parent is worth chasing.

### David Cramer (zeeg) — "Good goal prompt"
https://x.com/zeeg/status/2059687015038464021 (55K views, May 27) — image-only post, text is a t.co link. Saved in notes as "good goal prompt"; the substance is in the attached image, not fetched here. Re-open in browser if needed.
