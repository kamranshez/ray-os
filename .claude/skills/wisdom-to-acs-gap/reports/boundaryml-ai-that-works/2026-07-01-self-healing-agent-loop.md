---
title: The Self-Healing Agent Loop That Fixes Its Own Language
videoId: 485FGIq8LKM
url: https://www.youtube.com/watch?v=485FGIq8LKM
date: 2026-07-01
status: posted
---

# The one idea worth a video

**1. The self-healing product loop: point agents at your own product to manufacture the bug signal, then feed that signal back as issues other agents fix.** This is the reframe the whole demo hangs off; every sub-part (transcript capture, the trophy summary, dedupe, cold vs warm start, the PR loop) exists only to serve "have agents run BAML and turn what breaks into a fix."
VERDICT: 🔗 next-step video available (complements the filmed "closing-the-loop").

**2. The issue tracker as a human-friendly state machine for a fleet of agents, whose history you mine to build meta-loops that kill whole classes of issues.** It is the orchestration substrate: labels are pipeline stages, humans own and redraft, agents auto-escalate, and the long-term payoff is analyzing redraft history to add a pre-emptive loop.
VERDICT: ❌ net-new video available.

**3. The skill arena: treat competing skill versions as git branches and eval them on real tasks by cost, turns, and success instead of hand-tuning one.** The empirical harness that surfaced the counter-intuitive result that the shortest skill wins because BAML does the heavy lifting.
VERDICT: 🔗 next-step video available (complements the filmed "simplify-skill").

---

# Summary

Dex hosts Boundary's Vaibhav and Dylan demoing their software factory: agent loops that write BAML, surface language bugs, draft Linear issues, and open self-fixing PRs.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1 — The self-healing product loop

**The claim.** Rather than waiting for users to report bugs, you point agents at your own product on hard tasks, capture everything that breaks, and loop those failures back as fixes. As Dylan frames it: "let's just have some agents try writing a ton of BAML code and see what breaks."

**Why it is non-obvious.** The default is to write more tests. Vaibhav explains why that fails for a language: "as you keep adding features, they keep competing with each other," so "no matter how good tests we write... it doesn't freaking work." The insight flips the roles: the agent is not the thing under test, it is the fuzzing harness that generates realistic usage no test suite anticipated.

**Why it is true.** Because agents exercise the product like a real user would, then log the full transcript, a second agent (the "trophy") can mine that log for what worked and what broke; because each break carries its chat-log evidence, it becomes a concrete, reproducible issue; therefore fixes target real usage, not imagined edge cases. The -7 negative-argument bug is the proof: dismissed at first as "a hallucination of the agent," then reproduced and shipped as a fix.

**What it generalizes to.** Any product with a machine-drivable surface: an SDK, an API, an internal CLI. Point agents at real workflows, capture traces, turn failures into tickets.

**How it goes wrong.** Much of the signal is garbage ("some of these issues are just trash"), so the loop needs dedupe and a human gate, or it drowns you in trivia.

## Spine 2 — The issue tracker as an agent state machine

**The claim.** Linear is not a nicety bolted on the side; it is the human-friendly state machine that tracks every unit of agent work through labeled stages, and its accumulated history is the asset that lets you build the next loop.

**Why it is non-obvious.** Most people reach for a bespoke queue or a database. Dex reframes it: "you could do this in Temporal... but Linear is designed for humans to interact," and Vaibhav adds that when you want to be in the loop, "this is a great interface." The tracker earns its place precisely because humans need to comment, own, and redraft.

**Why it is true.** Because each issue carries a label representing its pipeline stage (not-started, redraft, approved, agent-writes-code, needs-human), a human can steer any single item without touching code; because that state is durable and queryable, you can later "analyze the history of your Linear issues and see how many have been redrafted" and categorize them; therefore you can "build a different loop to make that original loop" better, pre-empting a whole class of issues in the prompt. As Vaibhav puts it, "you can only do that in hindsight once you've detected a class of issues. And for that you need automation."

**What it generalizes to.** Any multi-agent orchestration: use GitHub Projects, Notion, or your own board as the shared state and the human control surface.

**How it goes wrong.** Ownership is load-bearing: without a human assigned, two people track the same bug, or nobody defines the problem well enough for an agent to act.

## Spine 3 — The skill arena

**The claim.** Instead of hand-tuning one skill and hoping, keep each version as a git branch and run the same task across all of them, scoring cost, turns, and success, then keep the winner.

**Why it is non-obvious.** Skill authoring feels like prose craft, so people polish a single document. The arena treats it as an eval problem and produces a counter-intuitive result: "the best skill is actually not a long skill, it's actually like the shortest skill," because "BAML does so much heavy lifting." More words made it worse.

**Why it is true.** Because you launch one task against many skill branches at once (triggered from Slack), and because each run reports cost, turns, and whether it succeeded, you get a direct comparison rather than an opinion; therefore selection is empirical and repeatable, and "our users don't even have to test what's going on."

**What it generalizes to.** Any prompt, system message, or CLAUDE.md you maintain: branch the variants, run a fixed task battery, and let the metrics pick.

**How it goes wrong.** The metric has to be honest. Cost, turns, and pass or fail can all look fine while the agent quietly hill-climbs; you still need a human reading a sample of traces to catch struggle the numbers hide.

---

# 🎬 Proposed ACS videos

## 1. Make Your Product Debug Itself With an Agent Loop
- HOOK: What if the bug reports for your product wrote themselves, and so did the fixes?
- THE PROMISE: For anyone with a product or codebase an agent can drive, stand up a loop that manufactures its own bug signal and fixes it while you sleep.
- THE SHAPE: (1) point agents at a hard task in your product; (2) capture the full Claude Code transcript; (3) a "trophy" agent summarizes what worked and what failed; (4) turn failures into deduped issues, each with chat-log evidence; (5) an agent opens a self-fixing PR.
- SPINE: 1
- SLOT: Techniques (next to closing-the-loop); seeds Claude Code > compound-engineering
- RELATIONSHIP: 🔗 complements "closing-the-loop" (filmed), which teaches giving one agent a signal to verify its own work; this scales that to a fleet that manufactures the signal by exercising the product and routes it through issues and PRs. Do not re-teach single-agent self-verification; teach the product-as-fuzzer architecture around it.
- PROOF TO REUSE: the -7 negative-argument bug they called "a hallucination of the agent" then reproduced ("Oh, crap. Shoot. This actually is an issue."); "let's just have some agents try writing a ton of BAML code and see what breaks"; the trophy artifact that reports positive feedback loops, not just bugs.

## 2. Run a Fleet of Coding Agents Through One Issue Tracker
- HOOK: Your issue tracker is secretly the best agent state machine you already own.
- THE PROMISE: For teams running more than one coding agent, use Linear (or any tracker) as a human-friendly state machine, then mine its history to build loops that kill whole classes of problems.
- THE SHAPE: labels as pipeline stages (not-started, redraft, approved, agent-writes-code, needs-human); a human owns, comments, and flips to redraft; an agent auto-escalates to needs-human after max turns; later, analyze redraft history to add a pre-emptive loop in the prompt.
- SPINE: 2
- SLOT: Claude Code > agent orchestration (near building-effective-agent-teams, self-modifying-claude-md)
- RELATIONSHIP: ❌ net-new. No ACS video covers using an issue tracker as the agent state machine, nor the history-mining meta-loop that fixes the loop itself.
- PROOF TO REUSE: "it's not just about designing the loop, it's also about designing the workflow behind the loop"; the redraft, approve, needs-human label flow with a human owner tagged; "you can only do that in hindsight once you've detected a class of issues. And for that you need automation."

## 3. Stop Guessing Your Skill: Put Every Version in an Arena
- HOOK: Instead of hand-tuning one skill, run all your versions against the same task and let the data pick.
- THE PROMISE: For anyone writing Claude skills, build a tiny arena that evals skill branches on cost, turns, and success so you keep the proven winner instead of guessing.
- THE SHAPE: keep each skill version as a git branch; launch the arena from Slack; run one task across every branch; score cost, turns, success, and number of issues; watch the shortest skill win.
- SPINE: 3
- SLOT: Skills class (chapter on evaluating and iterating skills)
- RELATIONSHIP: 🔗 complements "simplify-skill" (filmed), which argues the shorter skill wins; this adds the arena that empirically proves which variant wins across cost, turns, and success, so you stop trusting the instinct alone.
- PROOF TO REUSE: "the best skill is actually not a long skill, it's actually like the shortest skill"; the metric triad of cost, turns, succeeded; skills as branches you launch from Slack.

### Also film-able (not deep-dived)
- **Let your CI do the verifying** — swap slow agent sandboxes for your real GitHub runners; they cut test time from 15-20 minutes to about 2. Slot: Claude Code (infra). One-sentence pitch: reuse the expensive CI you already pay for as the verification layer for agent-written code.
- **The trophy: report what worked, not just what broke** — an agent that mines a run's chat log for positive feedback loops and not only bugs. Slot: Techniques. One-sentence pitch: measure what your agent did well so you can reinforce it, not only patch failures.

---

# 📚 Full wisdom (reference)

## SUMMARY
Dex hosts Boundary's Vaibhav and Dylan demoing their software factory: agent loops that write BAML, surface language bugs, draft Linear issues, and open self-fixing PRs.

## IDEAS
- Agents write tons of BAML code, hit bugs, and log every failure into structured issue data.
- A programming language slowly rots because each new feature competes, making full test coverage genuinely impossible.
- The self-healing loop finds language issues and fixes them simultaneously by having agents exercise the product.
- Every run's full Claude Code transcript is captured, then analyzed by a separate agent for errors.
- A trophy agent summarizes each run: what worked, what failed, and which positive feedback loops emerged.
- Cold-start runs force the agent to search for the skill itself; warm-start runs hand it over.
- Issues get deduped, and repeat occurrences attach fresh chat-log evidence rather than spawning another duplicate ticket.
- Linear acts as a human-friendly state machine, tracking each issue through clearly labeled, sortable pipeline stages.
- Agents distinguish skill issues (BAML skill inefficiencies) from language issues, meaning actual bugs in the compiler.
- Approving an issue automatically triggers a Cursor cloud agent that then opens a PR fixing it.
- Separate agents handle separate PR stages: one builds, others respond to CodeRabbit nits and CI failures.
- After a preset number of failed fix loops, an agent itself moves the ticket to needs-human.
- They offloaded test-running from slow Cursor sandboxes onto real GitHub CI, cutting each run to minutes.
- A changelog agent reads each nightly release's commits and drafts human-readable docs plus a small example.
- A skill arena runs one task across many skill branches at once, measuring cost, turns, success.
- The best-performing skill turned out to be the shortest one, because BAML itself does heavy lifting.
- An agent surfaced a real bug where negative CLI arguments like -7 were parsed as flags.
- The team dismissed that finding as a pure agent hallucination, then reproduced it themselves and cringed.
- Humans rarely write the code anymore, but they nitpick agent-written code heavily to preserve engineering taste.
- The entire factory runs on just two containers, at one point even on a spare MacBook.
- Linear webhooks kick off the whole pipeline, sending each work unit directly to the containerized driver.

## INSIGHTS
- You never build the entire software factory at once; you stack small isolated loops that compound.
- Instead of waiting for humans to report bugs, have agents generate the code humans would write.
- Treat a programming language as a data problem: measure what agents struggle with, then decide empirically.
- Designing the workflow around the loop matters as much as the loop; state and ownership dominate.
- The issue-tracker history is the real long-term asset: analyze it to build loops pre-empting recurring problems.
- Agents excel at exhaustive detail while humans excel at intuition, taste, and deciding what deserves fixing.
- Human leverage belongs where a little effort prevents three wasted agent rounds on a wrong approach.
- Auto-merge stays deliberately off: they trust agents to draft PRs but not yet to merge them.
- Writing many small skills and measuring outcomes beats hand-crafting the single skill you merely hope works.
- Bugs the agents find look trivial afterward, yet stayed invisible to the humans who designed it.
- Structured, uniformly formatted agent issues scan faster and richer than the terse, inconsistent issues humans write.
- Reusing your existing CI infrastructure turns already-expensive runners into the free verification layer for agent-written code.

## QUOTES
- "Well, it's all just loops." — Dex
- "let's just have some agents try writing a ton of BAML code and see what breaks." — Dylan
- "there's a reason Python still has bugs. Like 25 years later." — Vaibhav
- "we don't really need to write the code, we do spend a lot of time making sure that humans nitpick at this code a lot." — Vaibhav
- "This has to be a hallucination of the agent." ... "Oh, crap. Shoot. This actually is an issue." — Dex / Vaibhav
- "it's not just about designing the loop, it's also about designing the workflow behind the loop." — Vaibhav
- "you can only do that in history in hindsight once you've detected a class of issues. And for that you need automation." — Vaibhav
- "the best skill is actually not a long skill, it's actually like the shortest skill." — Vaibhav
- "make a data-driven language." — Vaibhav
- "You don't have to build the entire software factory at once." — Dex
- "one day you'll wake up and 80% of all of your stuff is automated." — Dex
- "It'll probably make your product better way faster than you will." — Dylan

## HABITS
- They assign each issue to a specific human owner, preventing two people tracking the same bug.
- They add comments, then set a redraft label, which kicks an agent to rewrite the issue.
- Every issue ships with evidence attached: the specific chat log where that exact bug actually occurred.
- They track cost per run and turns per run even while defaulting to the best model.
- They leave PR comments in plain natural language and spawn a fresh agent to address each.
- They cap fix attempts with an explicit max-turns limit before escalating any stuck ticket to human.
- They always run challenges on the very latest release and never bother testing older versions anymore.
- They trigger new challenges straight from Slack by telling a bot named Bamy to try BAML.
- They also run a cron job that continuously generates and then executes fresh coding-challenge tests overnight.
- They keep a dedicated agent that periodically retests stale issues to check whether they quietly self-resolved.

## FACTS
- Python, the language itself, still has bugs 25 years later because its core systems interact unpredictably.
- Moving tests from Cursor sandboxes to GitHub CI cut run time from 15-20 minutes to two.
- BAML is basically TypeScript, so users type TypeScript's null-assertion syntax that BAML never actually planned supporting.
- BAML must support WASM32, where maximum allocations are usize::max, not the i64 a human would assume.
- The Rust clap library did not solve their negative-argument parsing bug, contrary to the team's assumption.
- The entire agent factory runs on just two containers, deployable via web or a spare MacBook.
- Installing BAML's agent skill requires running baml agent install --cloud after you first install the language.
- Linear sends a webhook to the running container, which is how each pipeline run kicks off.
- The same string.split need surfaced twice, across reverse-words and Huffman-coding challenges, proving the demand real.

## REFERENCES
- BAML / Boundary (the programming language and company being demoed)
- Human Layer (Dex's company) and the "AI That Works" show
- Linear (issue tracker used as the state machine); Notion (prior tool they migrated from)
- Cursor cloud agents; CodeRabbit (PR review bot); GitHub CI/CD runners
- Claude / Claude Code (the coding agent driving runs)
- Rust and the clap CLI-parsing library; WASM32 compile target; TypeScript (syntax reference)
- Slack (trigger surface, the "Bamy" bot); Temporal (named as an alternative state machine)
- Excalidraw / "Excalibur" (the whiteboard used to sketch the architecture)
- Aaron (suggested using GitHub CI over sandboxes); chat participants Francisco, Matthias, Josh, Avery, Sam
- The "software factory" concept circulating on social media

## ONE-SENTENCE TAKEAWAY
Point agents at your own product to manufacture bug signal, then loop small fixes back.

## RECOMMENDATIONS
- Point agents at your own product to generate bug signal instead of waiting on real users.
- Start with one small loop, ship it, then layer additional isolated loops incrementally rather than architecting.
- Adopt an issue tracker as your shared state machine so agents and humans coordinate work cleanly.
- Attach concrete chat-log evidence to every generated issue so any human can quickly verify it's real.
- Dedupe generated issues and attach fresh evidence to existing ones rather than letting duplicates flood tracker.
- Offload agent test-running onto your existing CI runners to slash sandbox execution from twenty minutes down.
- Mine your tracker's history for recurring issue classes, then add an upstream loop that prevents them.
- Run a skill arena: eval multiple skill branches against one task by cost, turns, and success.
- Keep humans reviewing and nitpicking agent code closely even when they no longer write it anymore.
- Auto-escalate to a human after a fixed number of failed fix loops instead of retrying endlessly.
