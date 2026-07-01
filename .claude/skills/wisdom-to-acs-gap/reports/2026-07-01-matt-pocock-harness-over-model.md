# Wisdom to ACS Gap — Matt Pocock x David Ondrej: "Optimize the Harness, Not the Model"

Source: https://www.youtube.com/watch?v=nQwJVHCtDDY
Guest: Matt Pocock (aihero.dev) · Host: David Ondrej · Format: long-form interview

---

## 1. The ideas worth a video

1. **Stateful skills** — a skill can persist state to the local workspace (mission.md, a learning record, HTML lessons) so the agent has *memory* across invocations, like a teacher who remembers you. → ❌ **net-new video available**
2. **Queues, not loops** — the real unit of AFK orchestration is a QUEUE of scoped tasks many agents pull from, not an infinite while-loop; wire GitHub issues + labels + sandboxes + Actions. → 🔗 **next-step video available**
3. **Procedures vs abilities + the blank-slate reset** — skills split into procedures (you invoke) and abilities (the model invokes, and each one taxes your context); the fix is delete-everything-then-rebuild. → 🟡 partial, but the reset ritual is the net-new slice worth filming

---

## 2. Summary + counts

A long-form Matt Pocock interview arguing your harness, skills, and fundamentals — not the model — are the real, controllable lever for getting insanely ahead with AI.

`🔴 1 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered`

---

## 3. 🔬 Deep dive

### Spine 1 — Stateful skills (the teach skill as the worked example)

**The claim.** A skill can write state to the local workspace so the agent gains memory across separate invocations, turning a one-shot instruction set into something that behaves like a returning teacher.

**Why it's non-obvious.** Almost everyone builds skills as stateless prompt templates and assumes "memory" is either the model's job or something you bolt on with an MCP server or a database. Matt's move is smaller and cheaper: the skill itself writes plain files and reads them back next run.

**Why it's true / the mechanism.** Because the teach skill writes a `mission.md` (who you are, what you're building, what success looks like) and a running learning-record, the *next* invocation reads those first and resumes instead of re-asking. That persisted state is exactly what lets it draw a linear path through the knowledge graph rather than restarting cold. The personalization is a downstream consequence of state on disk, not of a smarter model — "a teacher remembers what you've done before."

**What it generalizes to.** Any workflow that spans sessions. A refactor skill that keeps a `migration-progress.md`; an onboarding skill tracking which subsystems a new hire has toured; a bug-triage skill that remembers which modules it already audited so it never re-scans them.

**How it goes wrong.** Stale state (mission drifts, records rot), state you can't easily inspect or edit, and state that bloats context when it's read back in full. A stateful skill needs a discipline for what to persist versus summarize.

### Spine 2 — Queues, not loops

**The claim.** The unit of AFK agent orchestration is a QUEUE of scoped tasks that many agents pull from, not a single infinite loop.

**Why it's non-obvious.** The viral framing (Geoffrey Huntley's Ralph loop) is "run your agent in a while-loop forever." Matt argues the loop is a red herring and half the hype is labs selling tokens: what you actually want is an agent that picks one specific scoped task off a backlog, does it, and stops.

**Why it's true / the mechanism.** Development has always been a queue — PMs add tasks, multiple developers pull them off, each merged PR removes an item. Model AFK agents the same way and any trigger (a label on a GitHub issue, a Sentry alert) can push work onto the queue, while any of N sandboxed agents (Sand Castle + GitHub Actions) picks it up in parallel. A loop pins you to one serial worker; a queue parallelizes and lets a human inject and reprioritize. Matt's metaphor: the king with a queue of problems beats the minister left running unattended on a loop.

**What it generalizes to.** The actor / worker-pool pattern in distributed systems: you don't loop, you consume a queue with a pool of workers. Same shape as any batch backend or job runner.

**How it goes wrong.** Without human-in-the-loop checkpoints — and observability into *why* a fix happened — you lose the ability to improve the harness. Auto-merging the wrong class of change ships bugs, and "who reviews the AI that says a PR is safe to skip?" You still need to sample the reviewer.

### Spine 3 — Procedures vs abilities + the blank-slate reset

**The claim.** Skills split into procedures (you invoke them, you stay in control) and abilities (the model auto-invokes), and every ability taxes your context window with its description on every single turn.

**Why it's non-obvious.** The default advice is "add more skills." Matt inverts it: each model-invocable ability leaks its description into context permanently, so 100 abilities is 100 descriptions of standing overhead that also dilute the model's attention. More skills can make the agent *worse*.

**Why it's true / the mechanism.** Skill descriptions are injected so the model knows when to auto-route to them — that injection is the cost. Setting `disable-model-invocation: true` pulls a skill out of auto-routing, so its description isn't leaked and only you can fire it. Therefore the highest-leverage reset is: delete everything (skills, plugins, MCP, CLAUDE.md, agents.md), watch the bare agent, then layer back ONLY the procedures you consciously choose. Keep the knowledge in the human; delegate execution, not judgment ("I don't want to delegate my thinking to the model").

**What it generalizes to.** Any budget-under-pressure system: dependency bloat in a codebase, feature bloat in a product ("you should be asking AI what to remove from your app"). Same discipline — subtract to sharpen.

**How it goes wrong.** Over-pruning (you lose genuinely useful auto-abilities, like a coding-standards lookup the model should pull mid-task), and treating the reset as a one-time event rather than an ongoing hygiene loop.

---

## 4. 🎬 Proposed ACS videos (ranked)

### 1. Build a Skill That Remembers You (the Stateful Skill Pattern)

- **HOOK:** Most skills forget everything the second they finish. Here's how to build one that remembers.
- **THE PROMISE:** For anyone building skills who's tired of agents that restart cold. After this you can add a local state directory to any skill so it accumulates memory and personalizes across runs.
- **THE SHAPE:**
  1. Stateless vs stateful: why almost every skill has amnesia.
  2. The state directory: mission.md, learning-record, reference cheat sheet.
  3. Demo: build a teach-style skill in an empty workspace, watch it write state, close it, reopen, watch it resume where it left off.
  4. Reading state back cheaply (summarize, don't dump the whole file into context).
  5. Where else this wins: migration-progress, onboarding tours, triage memory.
- **SPINE:** 1
- **SLOT:** Master Claude Code › Skills (or Advanced Techniques › "Skills as Force Multipliers")
- **RELATIONSHIP:** ❌ net-new. Every existing skills video (Creating Skills, Forked Contexts for Skills, Real World Skill Example 1 & 2, Loopy AI's "Creating the Skill") treats skills as stateless instruction sets — authoring, routing, model selection. None teach persisting state to disk for memory.
- **PROOF TO REUSE:** The teach skill writing mission.md ("who is this person, what do they want to build, why it matters, what success looks like"); "there are stateless skills and stateful skills... this teach skill is stateful because a teacher remembers what you've done before"; HTML lessons with quizzes for storage strength; the learning-record list kept in the top-right.

### 2. Stop Looping Your Agents. Build a Queue Instead.

- **HOOK:** Everyone's obsessing over agentic loops. The people shipping fastest quietly switched to queues. (Note: this is a deliberate contrarian counterpoint to the Loopy AI class's own loop framing — sell it as the honest "here's where the loop metaphor breaks" follow-up.)
- **THE PROMISE:** For anyone running AFK agents. After this you can wire GitHub issues into a task queue that sandboxed agents pull from and act on in parallel, with human checkpoints pushed toward production.
- **THE SHAPE:**
  1. The loop myth: the Ralph loop, and why an infinite while-loop is the wrong mental model.
  2. Dev has always been a queue — PMs add, devs pull, a merged PR removes an item.
  3. Demo: a GitHub issue + labels (explore / implement / review) triggering a sandboxed agent via GitHub Actions.
  4. Push human-in-the-loop checkpoints right: auto-merge trivial refactors, gate the dangerous changes.
  5. Who reviews the reviewer — keeping observability into your own harness.
- **SPINE:** 2
- **SLOT:** Loopy AI › L4 & L5: The Climb (as the next step after "Don't Pre-Sequence the Backlog")
- **RELATIONSHIP:** 🔗 complements "Don't Pre-Sequence the Backlog" and "Going Through a PR Backlog" (which already teach the queue *behavior* inside a loop frame: treat the backlog as a dynamic queue, keep pulling the next most important item, auto-merge), "Improving the Loop" (Loopy AI · L3, which frames the agent loop as a living per-project system), and "/autofix-pr" (remote monitoring + automerge on a single PR). Do NOT re-teach the backlog behavior — this video builds the running AFK system on top of it (label-triggered CI-sandbox agents + checkpoints pushed toward prod) AND makes the explicit "Ralph/agentic-loop is hype, parallel queue-consuming agents are the unlock" argument, which deliberately cuts against the Loopy AI class's own branding. Both the infra mechanism and the anti-loop reframe are absent today.
- **PROOF TO REUSE:** "The way I mostly think about these things is queues... queues, not loops"; the Ralph loop origin (Geoffrey Huntley, 14 July last year); Sand Castle running Claude Code inside Docker / Podman / Vercel sandboxes; the medieval king-with-a-queue vs minister-on-a-loop metaphor; the telemetry → issue → explore → fix → review → auto-merge pipeline; "who reviews the AI that's doing that?"

### 3. Delete Every Skill. Then Add Them Back On Purpose.

- **HOOK:** Your context window is bloated with skills you never actually chose. Here's the reset.
- **THE PROMISE:** For anyone whose agent feels sluggish or distracted. After this you can strip your setup to a blank slate and rebuild with only the procedures that earn their context cost.
- **THE SHAPE:**
  1. Two kinds of skills: procedures (you invoke) vs abilities (the model invokes).
  2. The hidden tax: every ability leaks its description into context every turn — 100 abilities, 100 descriptions.
  3. The reset ritual: delete skills / plugins / MCP / CLAUDE.md / agents.md, then observe the bare agent.
  4. Layer back only procedures; keep the knowledge in the human.
  5. disable-model-invocation to keep a skill user-only and out of context.
- **SPINE:** 3
- **SLOT:** Master Claude Code › Skills (or a Context Engineering capstone)
- **RELATIONSHIP:** 🟡 fills the gap in "Disable Model Invoked Skills" (which already teaches the disable-model-invocation mechanic) by adding the named procedures-vs-abilities taxonomy, the quantified context-leak cost model, and the blank-slate reset ritual — which has no home in the catalog today. Don't re-teach the flag itself; teach the cost model and the reset philosophy around it.
- **PROOF TO REUSE:** "First thing I would do is delete every single skill, every single plugin, every single MCP server... delete your claude.md, delete your agents.md, go back to absolutely nothing, then observe the agent"; "two types of skills: procedures... and abilities"; "you're going to be leaking 100 descriptions into the context window"; grill-me as a four-or-five-sentence procedure that replaces plan mode; "I don't want to delegate my thinking to the model."

### Also film-able (not deep-dived)

- **Strategic vs tactical programming** (John Ousterhout, A Philosophy of Software Design) — "AI has eaten tactical programming; your value is now strategic." A framing video on why your job shifted from writing code to scoping, designing interfaces, and delegating it. → Business class or a Master Claude Code intro.
- **Self-improving systems / "buy a lock"** — when AI surfaces a deep bug, don't just fix it; build a recurring cheap-model check (a daily security cron on a rotating slice of the repo) that catches the whole class. → Techniques / Context Engineering.
- **Harness > model / optimize AX** — "everyone's obsessed with the engine; optimize the harness." A codebase that's easier to change lets a cheaper model do identical work — a real token-spend hack. → Context Engineering / Techniques.

---

## 5. 📚 Full wisdom (reference)

### SUMMARY
A long-form Matt Pocock (aihero.dev) interview with David Ondrej arguing that the harness, your skills, and old software fundamentals — not the model — are the controllable lever for pulling ahead with AI.

### IDEAS
- Everyone obsesses over the model; the harness around it deserves equal work and offers more control.
- AI has eaten tactical programming entirely; strategic programming, the general's long-term view, is now your value.
- A stateful skill writes files locally so the agent remembers past work across invocations, like teachers.
- The teach skill creates mission.md, learning record, cheat sheet, and HTML lessons personalized to your goal.
- Skills split into two: procedures you invoke yourself, and abilities the model chooses to invoke itself.
- Every model-invocable ability leaks its description into context; a hundred such abilities leak a hundred descriptions.
- Setting disable-model-invocation true hides a skill's description from context so only the user can invoke it.
- AFK, away-from-keyboard agents, was the moment output exploded; suddenly five copies produce code you later review.
- Think in queues, not loops; a backlog of scoped tasks multiple agents pick off beats looping.
- Sand Castle runs agents inside Docker, Podman, or Vercel sandboxes so parallel agents cannot wreck machine.
- GitHub Actions plus issue labels trigger review or implement agents automatically, parallelizing work without local constraints.
- Push human-in-the-loop checkpoints far right toward production, auto-merging the trivial refactors while gating dangerous changes.
- When AI finds a deep bug, build a system, a cron, that catches that whole class.
- You don't need the fanciest model; a good harness plus cheaper model finds the same bugs.
- A codebase easier to change lets a stupider, cheaper model do identical work, optimizing token spend.
- Agent experience, AX, mirrors developer experience, DX; improving the codebase for agents is widely forgotten leverage.
- Your skills are the ceiling on what AI can do; low skills cap the model's output.
- Delete everything, plugins, MCP, CLAUDE.md, agents.md, observe the bare agent, then layer procedures back on deliberately.
- The grill-me skill, barely five sentences, turns the agent into an adversarial interviewer replacing plan mode.
- Before building, have AI list the ten most consequential decisions and interview you until ninety-eight-percent understood.
- One team records AI narrating a video walkthrough of its own frontend change on the PR.
- Cursor powered by Fable used its built-in browser to click through, create API keys, and self-test.
- Matt waits about a month before adopting a new model, avoiding hype, latency, and unproven costs.
- Good delegation to AI needs the same fundamentals: scope tasks tightly, design interfaces, write tests, documentation.

### INSIGHTS
- You control the harness far more than the model, so optimizing it yields more reliable returns.
- The bitter lesson warns raw compute beats optimizations, yet neglecting the harness still hamstrings today's work.
- Seniors get a tenfold boost from AI while juniors get little, because experience sets the multiplier.
- Knowledge, skills, and wisdom differ; wisdom needs doing the thing in its exact real-world context acquire.
- Reviewing isn't just checking code; you're reviewing the system producing it and improving that harness time.
- Removing human checkpoints raises the question of who reviews the reviewer AI approving those very changes.
- AI cannot originate product vision or novel ideas; you must decide features and talk to customers.
- Enthusiasm beats experience in raw output; excited AI-native juniors paired with fundamentals can thrive alongside seniors.
- Keeping your workspace agent-agnostic, grounded in old fundamentals, means it likely keeps working with future models.
- Over-optimizing around one model's quirks loses focus on the fundamentals that survive every model generation change.

### QUOTES
- "Everyone's obsessed with the model and I think they should be more interested in the harness." — Matt
- "AI has basically eaten tactical programming. It's gone, right? It's all gone." — Matt
- "Your skills are the ceiling on what AI can do." — Matt
- "The way I mostly think about these things as queues, okay, queues, not loops." — Matt
- "If someone keeps stealing your bike, maybe buy a lock." — David
- "First thing I would do is delete every single skill, every single plugin, every single MCP server." — Matt
- "You need to think of them as 50/50." — Matt
- "Have a code base that's easier to make changes in." — Matt
- "We're not just reviewing the code. We're also reviewing the system that produces the code." — Matt
- "I don't want to delegate my thinking to the model." — Matt
- "You can't be a code monkey anymore. You need to think strategically." — Matt
- "You cannot be asking the AI to build your app. Like you need to have the vision." — David

### HABITS
- Matt uses Claude Code with Opus 4.8 at medium effort for planning and some local implementation.
- He runs most development AFK using Sand Castle, sandboxing agents and pulling commits back locally afterward.
- He waits roughly a month after a model launches before deciding whether to adopt it seriously.
- He dictates using Whisper Flow, treating fast speech-to-text as an overpowered developer skill worth deliberately practicing.
- He prefers procedure skills he invokes himself over abilities, keeping himself firmly in the driver's seat.
- He chains grill-me, then a PRD skill, then splits that into individual issues to work through.
- He triages Sand Castle GitHub issues AFK, labeling items explore or implement to trigger agent runs.
- He runs a review agent on pull requests via GitHub Actions, using a locally stored prompt.
- He mostly ignores model choice, sticking with one setup rather than chasing every new release constantly.

### FACTS
- John Ousterhout's Philosophy of Software Design distinguishes tactical from strategic programming, a framing Matt applies AI.
- The bitter lesson in machine learning holds that raw compute reliably beats hand-engineered optimizations over time.
- The Ralph loop originated in Geoffrey Huntley's article, published the fourteenth of July last year.
- The zone of proximal development is an established educational principle Matt encoded into his teach skill.
- Quizzes reliably increase storage strength, the durability with which information stays retrievable in long-term memory.
- Matt taught singing and voice straight out of university, then spent four years teaching developers professionally.
- The teach skill installs via npx skills latest add matt-skills from the Matt Pocock repository.
- Superpowers from Obra is arguably the most popular skills repository, favoring model-in-control over user-in-control design.
- Vercel sandboxes let you spin remote agents up, then pull their commits into your local workspace.

### REFERENCES
- Matt Pocock — aihero.dev, aihero.dev/skills, newsletter, Twitter; Matt Pocock skills GitHub repo (`npx skills latest add matt-skills`).
- David Ondrej — host.
- John Ousterhout, *A Philosophy of Software Design* (tactical vs strategic programming).
- The bitter lesson (Rich Sutton, ML).
- Geoffrey Huntley — the Ralph loop article (14 July last year).
- Sand Castle (Matt's agent-sandboxing tool); Docker, Podman, Vercel sandboxes; GitHub Actions; Sentry.
- Superpowers skills repo (Obra); grill-me, teach, two-PRD, engineering-zoom-out skills; `disable-model-invocation` frontmatter.
- Whisper Flow (dictation); Cursor; Fable; Opus 4.8, Opus 4.5; Pro Git book.
- Teaching concepts: zone of proximal development, knowledge/skills/wisdom, storage strength.
- Tailscale, VPS, Cmax (mentioned by David); SerpAPI (sponsor).

### ONE-SENTENCE TAKEAWAY
Optimize the harness and your own skills, not the model; fundamentals outlast every shiny release.

### RECOMMENDATIONS
- Delete all skills, plugins, MCP servers, CLAUDE.md, and agents.md, observe the bare agent, then rebuild deliberately.
- Build stateful skills with a local state directory so agents remember context across separate invocations reliably.
- Model your AFK work as a queue of scoped tasks agents pull, not one infinite loop.
- Sandbox every autonomous agent with Docker, Podman, or Vercel before letting it touch your real machine.
- Turn every surprising bug into a recurring cheap-model check that catches that whole class going forward.
- Before building, have the agent grill you until it understands ninety-eight percent of your consequential decisions.
- Make each skill either a deliberate procedure or a disabled ability, never bloating context with abilities.
- Improve your codebase for agent experience so a cheaper model completes identical work spending fewer tokens.
- Adopt dictation with Whisper Flow to move ideas between brain and agent far faster than typing.
- Record AI-narrated video walkthroughs of frontend changes on PRs to make human review dramatically faster overall.

---

LOG: nQwJVHCtDDY — posted — spine: harness>model (stateful skills / queues-not-loops / procedures-vs-abilities) — 1 net-new / 1 complement — proposed: Build a Skill That Remembers You; Stop Looping Your Agents Build a Queue; Delete Every Skill Then Add Them Back
