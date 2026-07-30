---
tags: [acs, gap-analysis, loopy-ai, loop-engineering, wisdom]
aliases: [loop-engineering-acs-gap, loopy-ai-pdf-gap-report]
date: 2026-07-30
source: "clippings/Loopy AI.pdf"
source_title: "Loop Engineering: The Anthropic Playbook for Designing Systems That Prompt Your Agents"
source_author: "HuaShu (synthesis of Addy Osmani's Loop Engineering)"
status: "1 net-new / 2 complement / 1 partial"
---

Gap report produced by `/wisdom-to-acs-gap` on `[[Loopy AI.pdf]]` (HuaShu, 11pp, June 2026).

## 🎯 The one idea worth a video

**1. Reliability comes from the quality of the constraints, not the size of the model.** Stripe's Minions merges 1,300+ machine-written PRs a week on a fork of open-source Goose, and its architecture puts a *deterministic* orchestrator in front of the model (scan links, pull Jira, Sourcegraph + MCP assemble the context) and hard-coded gates behind it (linter runs, agent cannot skip; git commit is a script). Anything deterministic logic can solve never reaches the probabilistic model.
→ **VERDICT: 🔗 next-step video available**

**2. Where a loop runs is a mechanical decision, not a taste one.** Local `/loop`, desktop scheduling, and cloud routines have different physics (machine on/off, session open/closed, 1-minute vs 1-hour minimum interval, local files visible or not), and one question decides it: is this loop's work glued to the local machine, or can it leave?
→ **VERDICT: ❌ net-new video available**

**3. A loop accrues four silent costs, and two of them never show up on a bill.** Verification debt, comprehension rot, cognitive surrender, and token blowout are one failure wearing four faces, each feeding the next. Ray already teaches budgets and kill switches thoroughly; the two he does not teach are the human-side ones.
→ **VERDICT: 🔗 next-step video available**

**4. The five ways a loop fails are the five moves of a turn, skipped.** (LATENT SPINE, de-merged, then gap-checked to partial.) Nodding loop = no verification, amnesiac = no persistence, tangled = no handoff, blind = no discovery, manual = no scheduling.
→ **VERDICT: 🟡 already largely covered, no pitch — see deep dive for why**

---

**Summary:** HuaShu's synthesis of Addy Osmani's loop engineering, defining loops as a fourth layer above the harness, decomposed into five moves, six parts, four costs.

`🔴 1 net-new · 🔗 2 complement · 🟡 1 partial · ✅ 0 covered`

---

## 🔬 Deep dive

### Spine 1 — Constraints, not model size

**The claim.** A production loop's reliability is set by how much of it is deterministic, not by which model it runs.

**Why it's non-obvious.** The default assumption is that a flaky agent pipeline gets fixed by a better model or a better prompt. Minions argues the opposite by existence proof: it is a fork of Goose, an open-source framework, and it out-reliabilities setups running frontier models with more freedom.

**The mechanism.** Every step handed to the model is a step with a failure probability attached, and those probabilities compound across a pipeline. So the reliability question becomes an allocation question: which steps *must* be probabilistic? Context assembly is not one of them, so a deterministic orchestrator scans links, pulls Jira and docs, and locates code via Sourcegraph before the model wakes up. Linting is not one of them, so a hard-coded pipeline step runs it and the agent cannot skip it. Committing is not one of them, so a script does it. What is left for the LLM is the irreducibly creative middle: write the code, fix the lint. As the paper puts it, *"Letting the LLM find its own context is the least controllable part, so that work, whose rules can be hard-coded, is taken out of the model's hands."*

**Generalizes to.** Ray's own content loops. A YouTube outlier-research routine that lets the model decide which channels to query is Minions-before-Minions; the deterministic version pulls the channel list, the date window, and the view thresholds from a config file and hands the model only the judgment call.

**How it goes wrong.** Hard-coding the wrong things makes the loop brittle in a new way, and the paper is explicit that Stripe's pipeline is *"the endpoint of this path, not the entry: its reliability comes from years of hardening the deterministic gates."* Copying the finished architecture on day one buys the maintenance cost without the earned trust.

### Spine 2 — Scheduler physics

**The claim.** Choosing between local `/loop`, desktop scheduling, and cloud routines follows from one property of the work, not from preference.

**Why it's non-obvious.** "Running while you sleep" sounds like one capability, so people pick the scheduler they already know and then quietly discover their loop stops the moment the laptop lid closes. The paper names the conflation directly: local rerun means "run a few extra rounds while I am here"; cloud scheduling means "run even when I am not."

**The mechanism.** The three options differ on four hard axes: does the machine need to be on, does a session need to be open, what is the minimum interval, and can it see local files. Cloud cannot go below one hour and gets a clean clone each run. Local reaches one minute and sees your working tree. So the work's own properties decide: a loop polling a local dev server every minute *can only* run locally, because the check does not exist off the machine and one hour is useless. A loop scanning open issues at 3am should never be tied to a laptop, because laptops get lids closed and get carried out of the door. Two concrete cases, opposite answers, no taste involved.

**Generalizes to.** Ray's existing cloud routines. The LinkedIn source scout and the YouTube outlier research are correctly cloud (no local state, daily cadence); the gated-feature scan is arguably local (it reads a binary on this machine).

**How it goes wrong.** Treating it as either/or. The paper's position is that a mature setup runs both, local for the tight inner check and cloud for the overnight sweep, and that "no single scheduler does it all."

### Spine 3 — The four compounding debts

**The claim.** An unattended loop accrues verification debt, comprehension rot, cognitive surrender, and token blowout, and they are one failure wearing four faces rather than four independent risks.

**Why it's non-obvious.** Only one of the four is visible. Token blowout hits the invoice; the other three are silent by construction, and the loop feels *better* as they accumulate because it is shipping more.

**The mechanism.** The paper's worked example is the whole argument: twenty PRs open overnight, all green, three of them containing a bug the tests do not cover. Because no independent evaluator existed, those three merge (verification debt). Because a human merged twenty changes without reading them, their mental model of the codebase now lags by twenty changes (comprehension rot). Because it ran so smoothly, they stop reading the next morning's batch at all (cognitive surrender). Because the loop retried freely all night, the bill is triple the estimate (token blowout). Each one makes the next more likely: more unverified output means less understanding, less understanding means more surrender, more surrender means the loop runs longer unwatched and produces more unverified output. The guard against all four is identical: keep a human *capable* of saying no to a machine built to say yes.

**Generalizes to.** Ray's own multi-agent content loops, where the failure is not a merged bug but a published artefact nobody re-read.

**How it goes wrong.** The naive read is "review everything," which defeats the purpose. The paper's actual prescription is sampling: read a representative sample daily and force yourself to *explain* each sampled change. Inability to explain one is the diagnostic, and it is far cheaper to discover it on a quiet Tuesday than in a production incident.

### Spine 4 — Anti-patterns as skipped moves (covered, no pitch)

**The claim.** Each of the five ways a loop fails corresponds exactly to one of the five moves of a turn being skipped, so debugging a loop reduces to naming the missing move.

**Why it's load-bearing anyway.** It is the compression that makes the rest of the paper hold together, and it explains why the failures cluster: a team careless about one check is usually careless about the others, so hasty loops install only discovery and handoff (the two that produce visible output) and skip the three that produce safety.

**Why no pitch.** [[03-where-loops-fail-right-now|Where Loops Fail Right Now]] (Loopy AI > Where Loops Fail) already ships a *nine*-mode field guide, and its two-column split (model-limited and eroding vs. human-owned and durable) is a sharper frame than the paper's five, because it tells you which failures a model release will fix and which are permanently yours. Filming a five-mode taxonomy on top would be a downgrade wearing a mnemonic. The one genuinely additive beat is the mechanism underneath it: *the cost of a mistake scales with the number of turns it survives before someone catches it, and a loop is by construction a machine for maximizing turns.* That is a 90-second insert into the existing video, not a new one.

---

## 🎬 Proposed ACS videos

### 1. Reliability Comes From the Constraints, Not the Model

- **HOOK:** Stripe merges 1,300 AI-written pull requests a week, and they do it on a fork of an open-source framework, not a frontier model with a great prompt.
- **THE PROMISE:** For anyone whose loop works four times out of five. After this you can look at your own loop and move at least two steps out of the model's hands and into a script it cannot skip.
- **THE SHAPE:**
  1. Show a loop that fails intermittently, and resist the urge to fix the prompt.
  2. Draw the Minions pipeline: deterministic orchestrator → LLM writes → hard-coded linter → LLM fixes → hard-coded commit → human review.
  3. Rebuild one of Ray's own loops that way: pre-assemble the context with a script before the agent starts.
  4. Add a gate the agent physically cannot skip, then show it catching something.
  5. Close on the caveat: Stripe is the endpoint of years of hardening, not the entry point.
- **SPINE:** 1
- **SLOT:** Loopy AI > Command & Control (adjacent to `Confine, Don't Supervise`)
- **RELATIONSHIP:** 🔗 complements [[01-confine-dont-supervise|Confine, Don't Supervise]], which already teaches hard control for *safety* (remove the capability so damage is impossible, soft control vs hard control, the laptop blast radius). Do not re-teach that. This is hard control for *reliability*: remove the *decision*, not the capability, so unreliability is impossible. Same lever, different target.
- **PROOF TO REUSE:** *"its core claim is that reliability comes from the quality of the constraints, not the size of the model"*; *"Anything deterministic logic can solve never goes to a probabilistic model; where one draws that line decides whether the loop is reliable"*; the Devbox-on-EC2 "cattle not pets" detail; the Slack `@bot` / emoji-reaction trigger.

### 2. Local, Desktop, or Cloud: Where Your Loop Actually Runs

- **HOOK:** Two loops, same code. One keeps running when you shut the laptop, one dies silently and you find out on Thursday.
- **THE PROMISE:** For anyone who has written a loop and now has to place it. After this you can answer "where does this run" in one question instead of guessing.
- **THE SHAPE:**
  1. The four-axis table on screen: machine on, session open, minimum interval, local files visible.
  2. Case A, poll a local dev server every minute. Cloud is structurally impossible here, show why.
  3. Case B, scan open issues at 3am. Show it die when the lid closes, then move it to a cloud routine.
  4. The one question: is the work glued to this machine, or can it leave?
  5. Close on running both, local for the tight inner check, cloud for the overnight sweep.
- **SPINE:** 2
- **SLOT:** Master Claude Code > Automation, immediately *before* `Routines (aka Scheduled Tasks)`
- **RELATIONSHIP:** ❌ net-new. `/loop`, `/goal`, and `Routines (aka Scheduled Tasks)` each teach how to *use* one primitive; none teaches which to reach for. This is the decision frame that should precede all three.
- **PROOF TO REUSE:** the local-vs-cloud-vs-`/loop` comparison table; *"A local rerun means 'run a few extra rounds while I am here'; cloud scheduling means 'run even when I am not.' These are different capabilities, and conflating them is how people end up disappointed when they close the lid and the loop they thought was autonomous quietly stops"*; the `/loop` vs `/goal` distinction (reruns on an interval vs runs until a condition holds).

### 3. The Two Debts Nobody Bills You For

- **HOOK:** Your loop opened twenty pull requests overnight and every test is green. That is the moment the trouble starts, not the moment it ends.
- **THE PROMISE:** For anyone already running a loop unattended. After this you have a five-minute daily practice that catches the two costs no budget cap can.
- **THE SHAPE:**
  1. Walk the twenty-PR worked example end to end, showing how one missing evaluator becomes four debts.
  2. Name the two that Ray's governance material does not price: comprehension rot and cognitive surrender.
  3. The daily practice on camera: sample one PR the loop opened, explain the change out loud, fail to explain it, and treat that as the alarm.
  4. The permanent checkpoint. Show that removing it is the day comprehension rot begins in earnest.
  5. Close on the amplifier: same loop, two builders, opposite outcomes six months out.
- **SPINE:** 3
- **SLOT:** Loopy AI > Governance (after `Skills as Code`), or as a companion to `Where Taste Went`
- **RELATIONSHIP:** 🔗 complements the governance material. [[01-l4-workers|L4 Workers]] and [[01-skills-as-code|Skills as Code]] already teach budgets, kill switches, and the "build the budget before you walk away" rule, so token blowout is covered and should be a callback, not a lesson. [[04-where-taste-went|Where Taste Went]] argues taste *relocates* to criteria and rubrics. What neither says is that the thing quietly *eroding* while taste relocates is your map of your own codebase, and that the fix is a sampling habit rather than more review.
- **PROOF TO REUSE:** *"The faster the loop ships code one did not write, the bigger the gap between what exists and what one actually understands"*; *"not 'no time' but 'no longer want to bother'"*; *"the human review point is not a temporary scaffold to be removed once the loop is trusted; it is the permanent feature that keeps the loop trustworthy"*; *"It is a faithful multiplication sign, and what it multiplies is the person."*

**Also film-able (not deep-dived):** the Claude Code ↔ Codex six-organ parity table (`/loop`↔Automations tab, `/goal`↔automation rerun+judge, `--worktree`↔background worktree, `.claude/agents/`↔`.codex/agents/`, MCP+plugins↔MCP connector, `SKILL.md`↔`$skill-name`) would make a tight Master Codex chapter video on porting a working Claude Code loop to Codex without rebuilding it.

⚠️ **One caveat on the gap-check:** the catalog search did not surface `Confine, Don't Supervise` even though the script exists locally with a video id, so the Loopy AI class may index worse than it reads. Treat pitch 1's relationship as the more conservative call made from the script itself rather than from search.

---

## 📚 Full wisdom (reference)

**SUMMARY**
HuaShu's synthesis of Addy Osmani's loop engineering, defining loops as a fourth layer above the harness, decomposed into five moves, six parts, four costs.

**IDEAS**
- Loop engineering sits one floor above harness engineering, removing the human from doing rather than directing.
- Three practitioners independently named the same move inside a single June week: Steinberger, Cherny, and Osmani.
- Each layer up minds a larger unit: one sentence, one window, one run, one repeating loop.
- A single turn has five moves: discovery, handoff, verification, persistence, scheduling; drop one and it stalls.
- Six parts realize those moves: automations, worktrees, skills, connectors, sub-agents, memory, each mapping to one move.
- Discovery sets the loop's ceiling: surface work of no value and the remaining four moves waste.
- Tuning an independent skeptical evaluator is far more tractable than making a generator critical of itself.
- The evaluator should act, not read: hook Playwright MCP so it clicks, screenshots, judges actual behavior.
- Claude Code's /goal stop condition is judged by a fresh small model, not the writing agent.
- Five anti-patterns map one-to-one onto five skipped moves: the nodding, amnesiac, tangled, blind, and manual loops.
- A mistake's cost scales with how many turns it survives before any human finally catches it.
- Stripe's Minions merges over 1,300 machine-written pull requests weekly on a fork of the open-source Goose.
- A deterministic orchestrator assembles Jira, links, and Sourcegraph context before the language model ever wakes up.
- Hard-coded gates interleave with LLM steps so the agent cannot skip the linter or the commit.
- Reliability came from the quality of Minions' constraints, not from the size of its underlying model.
- Cloud scheduling cannot go any lower than one hour; local /loop reaches one minute, machine permitting.
- Local rerun means extra rounds while present; cloud scheduling means genuine runs when you are absent.
- Four silent costs accrue: verification debt, comprehension rot, cognitive surrender, token blowout, each feeding the next.
- Comprehension rot means the codebase grows while your mental map stalls, and no alarm ever sounds.
- Cognitive surrender is the attitude version: not "no time" but "I no longer want to bother".
- Set per-run budgets, daily budgets, and max retry counts before the first unattended run, not after.
- Two people building the identical loop reach opposite places; the difference lives outside the loop entirely.
- Skills pay off "intent debt", the recurring cost of re-explaining a project to every fresh agent.
- Worktrees turn parallelism from "runs but messy" into "runs and clean" by isolating each agent's directory.
- Claude Code and Codex expose the same six loop organs under different names and menu locations.

**INSIGHTS**
- Higher layers fail more quietly: bad prompts surface instantly, bad loops bury mistakes for many days.
- Self-review fails structurally, not verbally: the writing context is already stuffed with reasons the code exists.
- A loop's floor is its evaluator; the generator only decides what the loop can ever produce.
- Anti-patterns cluster: teams careless about one check are usually careless about all the other four too.
- Hasty loops install only the two moves producing visible output and skip the three producing safety.
- Anything deterministic logic can solve should never reach the probabilistic model; that one boundary decides reliability.
- Scheduler choice is mechanical, not taste: ask whether the work is glued to the local machine.
- The four debts are one failure wearing four faces, so they have to be guarded together.
- The human review point is permanent architecture, not temporary scaffolding removed once the loop earns trust.
- As generation approaches free, an engineer's entire value concentrates into judging which candidate output is right.
- A loop amplifies unchanged whatever its builder brings, so a lapse in judgment is amplified too.
- Inability to explain a sampled change is a map needing an update, discovered cheaply not painfully.

**QUOTES**
- "loop engineering is replacing oneself as the person who prompts the agent, and designing the system that does it instead" — Addy Osmani's definition, as given in the paper
- "the harness below arms a single agent run; the loop above makes it run itself over and over" — Osmani, quoted in the paper
- "the cost of a mistake scales with the number of turns it survives before someone catches it, and a loop is, by construction, a machine for maximizing the number of turns" — the paper
- "A loop without a real check is just an agent nodding at itself." — the paper
- "automations are what make a loop an actual loop and not just one you did once" — Osmani, quoted in the paper
- "The agent forgets; the repo does not." — the paper
- "one cannot ask an author to step outside its own perspective, but one can swap in another agent with entirely different instructions that looks at the code from scratch, carrying none of the self-persuasion" — the paper, on Prithvi Rajasekaran's finding
- "assume the code is broken until proven otherwise—the default stance is doubt, not trust" — the paper, on community evaluator calibration
- "its core claim is that reliability comes from the quality of the constraints, not the size of the model" — the paper, on Stripe's Minions
- "Anything deterministic logic can solve never goes to a probabilistic model; where one draws that line decides whether the loop is reliable." — the paper
- "The engineer who welds every door shut, banking on never needing to go in, discovers on the day they must that they no longer hold the key." — the paper
- "the loop can execute, but it cannot decide. One must at least remain capable of saying 'this is wrong.'" — the paper
- "It is a faithful multiplication sign, and what it multiplies is the person." — the paper
- "build the loop, but build it like someone who intends to stay the engineer, not just the person who presses go" — Osmani's closing line, quoted in the paper
- "The rest is not in this note; it is in the terminal." — the paper

**HABITS**
- Osmani runs a morning triage automation reading failing CI, open issues, and recent commits each day.
- He writes every finding into ./state/triage.md with its status, then commits that file to the repo.
- Each finding worth doing opens its own isolated worktree so parallel agents never collide on files.
- One sub-agent drafts the fix; a second, sometimes a different model, reviews it against the tests.
- Anything the loop cannot handle confidently goes to an inbox for a human, never a PR.
- The triage skill's Stop section says never merge, never delete, and it is written by hand.
- Read a representative sample of the loop's output every day and explain each sampled change aloud.
- Stripe triggers Minions by @-mentioning a bot in Slack or by adding a single emoji reaction.
- Stripe runs each environment on Devbox on EC2, cattle not pets, swapping sandboxes out at will.
- Osmani triggers a named skill from automations rather than pasting instruction walls into a cron job.
- The evaluator is told to assume the code is broken until proven otherwise, defaulting to doubt.
- Stripe still routes all 1,300 weekly pull requests through a human review step before anything merges.

**FACTS**
- Peter Steinberger's June 2026 post on prompting loops rather than agents passed eight million total views.
- Addy Osmani, a Google Chrome engineer, coined "loop engineering" on his blog on June 7, 2026.
- Boris Cherny leads Claude Code at Anthropic and said that his job now is writing loops.
- Stripe's Minions is a fork of Goose, the open-source agent framework, and not a stronger model.
- Steve Kaliski described Minions on the How I AI podcast, giving the 1,300 PRs weekly figure.
- Claude Code's /loop shipped in v2.1.72; it is session-scoped and recurring tasks expire after seven days.
- Claude Code's /goal runs until a condition is met and arrived after Claude Code version 2.1.139 shipped.
- Cloud scheduling carries a one-hour minimum interval; local and desktop scheduling both allow a one-minute interval.
- Prithvi Rajasekaran, an Anthropic engineer, documented the generator/evaluator pattern while he was building long-running agentic applications.
- The generator/evaluator split borrows from generative adversarial networks, where one network builds and one picks faults.
- Maker-checker, the principle behind separated evaluation, is decades old in banking's own large transfer approval workflows.
- The paper warns that widely circulated claims like "90% of Claude Code is AI-written" are secondhand.

**REFERENCES**
People: Addy Osmani (Google Chrome), Peter Steinberger (OpenClaw), Boris Cherny (Anthropic, Claude Code), Prithvi Rajasekaran (Anthropic), Steve Kaliski (Stripe), HuaShu (author of the source paper). Works: Addy Osmani, "Loop Engineering," blog and Substack, Jun 2026; HuaShu, *Loop Engineering: Stop Asking Me What It Is*, Orange Books v260615, Jun 2026; Prithvi Rajasekaran, "Building long-running agentic applications: the generator/evaluator pattern," Anthropic engineering blog; Steve Kaliski on the *How I AI* podcast; Boris Cherny public remarks, Jun 2026. Tools and standards: Claude Code (`/loop`, `/goal`, `--worktree`, `SKILL.md`, `.claude/agents/`, Cloud Routines), Codex (Automations tab, background worktree, `.codex/agents/`, `$skill-name`), Goose (open-source agent framework), Stripe Minions, Model Context Protocol, Playwright MCP, Sourcegraph, Jira, Linear, Devbox on EC2, GitHub Actions. Concepts borrowed: generative adversarial networks, maker-checker banking controls, "vibe coding."

**ONE-SENTENCE TAKEAWAY**
Build the loop, but build it like someone who still intends to stay the engineer.

**RECOMMENDATIONS**
- Run /loop 5m on one small check; a first loop should barely look like a system.
- Move your discovery logic into a SKILL.md file rather than a schedule nobody will ever update.
- Write findings and their handling status to a state file on disk, never the chat window.
- Add an evaluator agent whose instructions default to reject, and make it run code, not read.
- Use --worktree per background agent so simultaneous fixes cannot overwrite each other's edits to shared files.
- Audit your existing loop against the five moves and name whichever one you quietly skipped building.
- Set a per-run budget, a daily budget, and a max retry count before ever walking away.
- Pull every deterministic step out of the model's hands and into scripts the agent cannot skip.
- Decide scheduler placement by asking whether the loop needs local files, not by your personal preference.
- Sample one pull request the loop opened each morning and explain that change back to yourself.
- Keep exactly one step where the loop pauses for you, permanently, even once you trust it.
- Prove the evaluator catches a real mistake before increasing how much the loop does in parallel.
- Write a Stop section in every skill listing whatever the loop must never do alone.

---

`clippings/Loopy AI.pdf — posted — spine: reliability from constraints not model size — 1 net-new / 2 complement — proposed: Reliability Comes From the Constraints Not the Model; Local, Desktop, or Cloud: Where Your Loop Actually Runs; The Two Debts Nobody Bills You For`
