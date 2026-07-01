---
title: "Building your own software factory — Eric Zakariasson, Cursor"
video_url: https://www.youtube.com/watch?v=rnDm57Py54A
video_id: rnDm57Py54A
channel: AI Engineer
published: 2026-04-28
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Building your own software factory — Eric Zakariasson, Cursor**](https://www.youtube.com/watch?v=rnDm57Py54A) - AI Engineer - uploaded 2026-04-28

> Three film-able spines: one net-new ACS video plus two next-step complements available.

## 1. The ideas worth a video

**Mine your own agent transcripts to auto-generate the rules you never remember to write.** A scheduled agent reads your chat history, clusters the corrections you keep repeating, and codifies them as durable rules or memories, so the factory improves itself. This subsumes the video's whole "rules should emerge dynamically" thesis and the read-merged-PR-comments automation.
VERDICT: ❌ net-new video available.

**Make the agent prove its work so you trust the tests, not the code.** The agent writes its own Playwright end-to-end tests and, on a computer-controlling cloud VM, records a video of itself clicking through the UI. This is the concrete verification substrate the whole factory rests on.
VERDICT: 🔗 next-step video available.

**Set up the repo so any task is runnable, accessible, and verifiable by an agent alone.** Colocated modular code, in-distribution start scripts, references to reproduce, and fencing hooks are what actually unlock unattended agents, not a smarter model.
VERDICT: 🔗 next-step video available.

## 2. Summary + counts

Eric Zakariasson (Cursor) shares practical steps for moving from one pair-programming agent to a self-improving "software factory" of many autonomous, verifiable, parallel agents.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 3. 🔬 Deep dive

### Spine B — Continual learning: mine transcripts to auto-write rules (❌ net-new)

The claim: instead of hand-authoring rules up front, build an automation that reads your past agent transcripts, extracts the corrections you keep making, and stores them as durable rules or memories. Why it is non-obvious: the default advice is "write good rules" or "install a rule pack from cursor.directory," but Eric argues rules should emerge, and most people are too lazy to stop and author one every time they correct an agent, so that knowledge evaporates. Why it is true: every correction you type ("use this component, not that one") is high-signal evidence of a gap between model behavior and your intent, and that signal already sits in your transcript history; so a scheduled agent can mine the transcripts, cluster recurring corrections, and write them back as rules without you remembering to. Eric extends the identical loop to comments on merged PRs, since a human bothering to review is even higher signal. It generalizes cleanly to a support bot mining resolved tickets to auto-draft canned responses. How it goes wrong: transcripts hold one-off corrections that should not become permanent rules, so over-harvesting bloats and contradicts your rule files. Eric concedes the "hacky plugin" is a placeholder for baking preferences into model weights.

### Spine A — Self-verifying agents: the agent proves the UI works (🔗 complement)

The claim: give the agent a way to verify its own work end to end, so you trust the tests instead of reading the code. Eric's agent wrote Playwright end-to-end tests, and on cloud VMs with computer control it recorded a video of itself clicking through the running app. Why it is non-obvious: most people treat verification as the human's job, reading the diff and clicking around themselves. Eric flips it, in his words, "if you as a human trust the tests, you probably are trusting the output even though you don't have to look at the code." Why it is true: a UI change has no clean contract the way a backend function does, so the only trustworthy signal is a real browser interacting with the live app; the agent spawns a browser, clicks by test-id, asserts nothing broke, and for anything untested drives the real app via computer-use, handing back a screen recording. Two steps: the agent generates the check, the agent runs the check, and you audit the artifact rather than the code. It generalizes to data pipelines (the agent writes and runs its own assertion queries). How it goes wrong: computer-use is slow and token-hungry, and self-written tests can be shallow, covering the happy path while missing the wrong-password case Eric had to prompt for by hand.

### Spine C — The agent-runnable codebase: runnable, accessible, verifiable (🔗 complement)

The claim: before scaling to many agents, restructure the repo so any task is runnable, accessible, and verifiable by an agent with no human in the loop, via colocated modular code, in-distribution start scripts, references to reproduce, and enabling skills plus fencing hooks. Why it is non-obvious: people reach for more agents or better prompts first, but Eric locates the bottleneck in the codebase's legibility. An agent that can ls one folder and find everything, or open package.json and know to run the start script, is enabled by structure, not raw intelligence. Why it is true: models are completion machines trained on conventional repos, so an in-distribution layout makes the right next action predictable and the agent acts autonomously; and because "runnable, accessible, verifiable" are the literal prerequisites for an unattended run, meeting them is what unlocks spawning agents on isolated VMs at all. It generalizes to onboarding human juniors, and concretely to a data team exposing clean contracts so a backend agent can self-verify. How it goes wrong: over-abstracting early breeds its own confusion, and completion bias means agents cargo-cult whatever reference you point them at, propagating a bad pattern fast.

## 4. 🎬 Proposed ACS videos

### 1. Teach Your Agent to Write Its Own Rules

- HOOK: Stop hand-writing rules you never remember to write; let an automation mine your transcripts and do it.
- THE PROMISE: For anyone whose CLAUDE.md never keeps up, you will run a loop that turns your own corrections into durable rules automatically.
- THE SHAPE:
  1. Show the pain: correcting the same mistake across three sessions, no rule ever written.
  2. Build a scheduled agent that reads recent transcripts and clusters recurring corrections.
  3. Have it draft candidate rules or memories, gated behind a quick human yes/no.
  4. Extend the same loop to comments on merged PRs, the highest-signal source.
  5. Show the rule file growing itself over a week.
- SPINE: B (continual learning).
- SLOT: Loopy AI, "L4 & L5: The Climb" (self-improving flywheel), or Prompt Engineering (rules).
- RELATIONSHIP: ❌ net-new. ACS teaches picking one gold-standard pattern ("The One-Pattern Rule for Agents") and diagnosing a misled agent ("Agent Introspection"), but nothing on automatically extracting rules or memories from your own transcript history.
- PROOF TO REUSE: Eric's continual-learning plugin; "I'm kind of lazy so I don't really remember to create a rule"; the read-merged-PR-comments automation; "my perspective on rules is like the bridge between the model behavior and the human behavior."

### 2. Make the Agent Prove the UI Works

- HOOK: If you trust the tests, you are trusting the output without ever reading the code.
- THE PROMISE: For solo builders shipping UI changes, the agent hands you a video and green end-to-end tests, so you review the proof, not the diff.
- THE SHAPE:
  1. Have the agent write a Playwright end-to-end test that spawns a browser and clicks by test-id.
  2. Wire it so every change reruns the suite before proposing a merge.
  3. For uncovered flows, give a computer-use agent instructions like a QA consultant (log in, enter a wrong password, observe).
  4. Have it record a screen capture of itself clicking through.
  5. Review the artifact, then merge.
- SPINE: A (self-verifying agents).
- SLOT: Loopy AI, "L2: Builder & Verifier" (the verification-substrate episode), or Advanced Techniques.
- RELATIONSHIP: 🔗 complements "Builder Verifier Pattern" (Loopy AI, L2: Builder & Verifier), which already teaches separating builder and verifier, adversarial review rounds, and verifying flows not plans; this adds the concrete substrate, namely the agent writing its own browser end-to-end test and driving a real browser via computer-use to produce a video you can eyeball.
- PROOF TO REUSE: the Ableton music-agent Playwright setup; the Glass keyboard-navigation recording; "if you as a human trust the tests, you probably are trusting the output"; the wrong-password QA-consultant example.

### 3. Set Up Your Repo So Agents Can Run It Alone

- HOOK: The bottleneck to autonomous agents is not the model, it is how legible your codebase is.
- THE PROMISE: For teams before they scale to many agents, your repo passes runnable, accessible, and verifiable, so agents work unattended.
- THE SHAPE:
  1. Colocate a feature's files so one ls reveals everything, contrasted with scattered grep-hunting.
  2. Make it runnable: a standard start script the model opens by default.
  3. Make it accessible: connect Linear, Slack, and Datadog so the agent gets broader intent.
  4. Make it verifiable: seed the end-to-end tests the agent can run itself.
  5. Add hooks that fence off encryption, auth, and payments.
- SPINE: C (agent-runnable codebase).
- SLOT: Context Engineering (large-scale production codebases), or Techniques, "Working with the Codebase."
- RELATIONSHIP: 🔗 complements "Reducing Agent Confusion in Growing Projects" (Techniques, Working with the Codebase), which reactively untangles an already-confusing repo; this is the proactive setup checklist (runnable, accessible, verifiable) you run before scaling to many agents.
- PROOF TO REUSE: the runnable/accessible/verifiable checklist; "if you have an easy time onboarding yourself to a new codebase, an agent probably will have that too"; the package.json start-script in-distribution point; the sensitive-file hook example.

### Also film-able (not deep-dived)

- **The Agentic Code Owner: auto-approve low-risk PRs, escalate risky ones.** An automation that scores each PR's risk, auto-approves trivial changes like variable renames, and for high-risk changes pulls in whoever last touched those files. Rough slot: Loopy AI or Advanced Techniques. Likely net-new versus ACS's "/autofix-pr" and "Going Through a PR Backlog," which fix and merge rather than risk-gate approvals.

## 5. 📚 Full wisdom (reference)

### SUMMARY
Eric Zakariasson (Cursor) shares practical steps for going from one pair-programming agent to a self-improving software factory of many autonomous, verifiable, parallel agents.

### IDEAS
- Dan Shapiro's six autonomy stages, from spicy autocomplete to dark factory, map every team's agent adoption.
- Most developers sit at levels two or three, pair-programming with one agent instead of managing many.
- A software factory runs agents 24/7, producing consistent output from assembly lines you design and observe.
- Colocated modular code lets an agent find all relevant files via one ls, not grepping everything.
- Reusable boilerplate for auth, startup scripts, and tests gives agents references to reproduce instead of inventing.
- Hooks should block agents from touching sensitive code like encryption or authentication where mistakes stay costly.
- Cursor rules are widely misunderstood: install every stack rule versus letting rules emerge when agents misbehave.
- Rules act like an SOP, showing agents exactly what they may and may not do here.
- Enablers like skills and MCPs give agents capabilities: adding a feature flag, reaching external context autonomously.
- A feature-flag skill lets agents ship flagged changes, merge the PR, then ping you to toggle.
- Eric's factory checklist poses three questions of any task: runnable, accessible, and verifiable entirely by agents.
- Package.json start scripts are so in-distribution that models immediately open them to launch a dev server.
- An agent wrote Playwright end-to-end tests that spawn browsers, click by test-id, and confirm nothing broke.
- Cursor's cloud agents get a dedicated VM plus computer control, letting them test their own work.
- The agent returned a screen-recording of itself clicking around, giving Eric human-verifiable proof without reading code.
- A continual-learning plugin reads past chat transcripts, extracts corrections, and stores them as durable rules automatically.
- A read-merged-PR-comments automation harvests high-signal human review notes so future agents learn from them over time.
- An agentic code owner scores each PR's risk, auto-approving trivial changes and escalating risky ones onward.
- For high-risk PRs the code owner pulls in whoever previously changed those files, refreshing their context.
- Isolated per-agent VMs, each with its own database and cache, prevent side effects across parallel changes.
- Frontloading a long spec or plan lets you send agents off on longer, trusted asynchronous tasks.
- A daily-review automation reads Slack and GitHub, then summarizes what you accomplished, replacing your manual note-taking.
- Linear tickets trigger a cloud agent automatically; stale feature flags even auto-file their own removal tickets.

### INSIGHTS
- Determinism loss is a symptom, not fate: probabilistic agents signal you need more guardrails, not fewer.
- As models follow instructions better, prompts shrink, but you must still supply clear intent every time.
- Managing agents mirrors human orgs: you keep adding workers, then managers, then managers of managers eventually.
- Trusting the tests equals trusting the output: strong verification is what lets you stop reading code.
- Rules are the bridge between model behavior and human intent, steering models toward what you want.
- Human-in-the-loop copy-paste steps between Datadog, Notion, Twitter, and code are exactly the toil worth automating away.
- Catching agents going off the rails is the flywheel: each failure points to a missing rule.
- Completion bias makes agents rush to finish; they reproduce existing references rather than plan future architecture.
- Humans stay accountable for all shipped code; you cannot blame the agent for any production failure.
- Storing context, transcripts, and good artifacts matters more than the work: it frames every future agent.
- Team factories fragment into per-engineer silos; unifying rules needs the same ceremony as PR review culture.
- Spending compute up front, manually writing critical tests and red-teaming, protects brownfield systems that cannot fail.

### QUOTES
- "I forced myself never to write any code um myself" — Eric Zakariasson
- "rules should just like emerge dynamically. Like if you're finding agents going off the rails, you should probably create a rule for that" — Eric Zakariasson
- "the models are getting so good at following specific rules that they usually don't go off the rails anymore" — Eric Zakariasson
- "if you as a human trust the tests, you probably are trusting the output even though you don't have to look at the code" — Eric Zakariasson
- "my perspective on rules is like the bridge between uh the model behavior and like the human behavior" — Eric Zakariasson
- "you just got to like spawn a shitload of agents and just like let them do the work and see what happens" — Eric Zakariasson
- "it's easy to vibe code close to the sun and fly too close" — Eric Zakariasson
- "the humans are still accountable for the things that's being shipped" — Eric Zakariasson
- "The 10x engineer is no longer about, you know, words per minute. It's like prompting." — audience member and Eric Zakariasson
- "store context for later ... this is going to help the agent to like know what good and bad looks like over time" — Eric Zakariasson

### HABITS
- Eric forces himself to never write code manually, focusing instead on the systems around the agents.
- He always runs agents in isolated cloud VMs instead of sharing a single local development environment.
- He plans synchronously, then executes those plans asynchronously, reviewing cloud agents once they finish their work.
- He keeps five to ten agents running asynchronously while scrolling Twitter or handling one synchronous task.
- He creates rules only reactively, when he notices agents repeatedly drifting from what he actually wanted.
- He still manually tests some changes, downloading a build of Glass or Cursor before finally merging.
- He runs a scheduled daily review that reads Slack and GitHub, summarizing his output each day.
- He tests UI changes by prompting cloud agents with computer use, like instructing a QA consultant.
- He runs a Mac Mini agent daemon with iMessage and calendar access for scheduled personal reports.

### FACTS
- Dan Shapiro published a blog post defining six distinct stages of software autonomy in early 2026.
- Cursor started as spicy autocomplete around 2022 to 2023 before climbing the autonomy ladder toward agents.
- Cursor 3 is a complete rewrite with no VS Code, built for an agent-first workflow instead.
- Cursor runs likely thousands of agents daily against copies of its own codebase on separate VMs.
- Cursor does not use foreign keys in database migrations for performance, contradicting the model's default preference.
- One cloud agent turn controlling the computer cost roughly one dollar in Eric's own rough estimate.
- Cursor's security team built a sentinel automation running ten invariant checks on PRs touching certain files.
- Cursor launched Workers, running its harness and orchestration on any machine, including your own Mac Mini.
- At Lovable, engineers gave an agent a vent tool that surfaced real harness problems in Slack.

### REFERENCES
- Dan Shapiro's blog post on six stages of software autonomy (the "dark factory").
- Andrej Karpathy's tab-to-agent framing, using Cursor as an example.
- Cursor 3 (agent-first rewrite), Cursor cloud agents, Cursor Workers, the Cursor agent CLI.
- Bugbot (Cursor's PR review tool).
- cursor.directory (community rules collection).
- AGENTS.md and Cursor rules.
- Playwright, Vitest, Puppeteer.
- Glass (Cursor interface) and Ableton (inspiration for the music-agent project).
- Linear, Slack, Notion, Datadog, GitHub.
- Lovable (the agent "vent tool" anecdote).
- Eric Zakariasson: x.com/ericzakariasson.

### ONE-SENTENCE TAKEAWAY
Stop pair-programming with one agent; build systems letting many agents run, verify, and improve themselves.

### RECOMMENDATIONS
- Colocate related code so an agent can discover a feature's files with a single ls command.
- Add hooks that block agents from editing encryption, authentication, or payment code without explicit human approval.
- Write rules only when you catch agents drifting; do not preinstall every rule from cursor.directory blindly.
- Have the agent write Playwright end-to-end tests so each change verifies itself before you ever merge.
- Give a cloud agent computer control, then instruct it like a QA consultant clicking through flows.
- Build a plugin that mines your chat transcripts for corrections and codifies them into durable rules.
- Automate a daily review that reads Slack and GitHub and summarizes what you shipped each day.
- Harvest comments on merged PRs, storing high-signal human review notes for agents to learn from later.
- Scope and parallelize tasks so two agents never edit the same files and cause merge conflicts.
- Frontload a detailed spec before sending an agent off, so longer asynchronous tasks stay on track.
- Keep humans reviewing critical areas like payments and auth even when agents write most other code.
