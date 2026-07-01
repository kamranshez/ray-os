---
title: How AI Agents Can Safely Ship Code to Production
videoId: gRqb7R4Pcrs
url: https://www.youtube.com/watch?v=gRqb7R4Pcrs
channel: BoundaryML - AI That Works
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine A: Feature flags manufacture "back pressure" where agents have none, turning unmeasurable work (UI, taste, "is this good?") into production metrics an agent can read and self-correct against.** Agents thrive where a loop can check them (compile, test, run) and fail where success is a judgment call; shipping variants behind a flag and reading conversion data hands them an objective signal in exactly their weakest domain.
VERDICT: 🔗 next-step video available (complements the filmed "Closing the Loop").

**Spine B: Split "merge to prod" from "turn it on," then let an agent drive a graduated flag rollout, so shipping (not coding) stops being the bottleneck.** The write-and-test loop is already fast; the PR-to-deploy stretch is the jam. Deploy flag-off, ramp from 0.01%, have the agent review metrics at each step and roll back or forward, built up incrementally from a CLI rather than a day-one software factory.
VERDICT: ❌ net-new video available.

---

# Summary + counts

On AI That Works, BAML's Vaibhav and Human Layer's Dexter explain how feature flags let coding agents ship to production gathering metric back pressure safely.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine A - Feature flags as manufactured back pressure

The claim: feature flags let you invent a feedback signal for the work agents are worst at. Dexter's framing is that agents excel wherever there is "back pressure," an automated check that says "this didn't work, here's why": compile the code, run the test, execute the program. What most people miss is the corollary, that when no such check exists locally the agent is flying blind. His example is visual: he had an AI make "sloppy ass motion graphics" and even with a browser-screenshot feedback loop it could not judge overlaps, because "AI vision is just not good enough to get things pixel perfect." UI and taste have no local back pressure. The mechanism: deploy three variants behind flags, let real users hit them, and the taste question ("which button looks good?") collapses into a metric ("conversion is 3% vs 7% vs 5%"). Now the agent "can reflect on what was done" with something quantitative. It generalizes cleanly to model migrations: one BAML customer had an agent read stored traces to move to Gemini 3.0 flash while cutting 20% cost elsewhere. It goes wrong when the metric is slow, noisy, or your sampling is biased, so the "signal" misleads.

## Spine B - Merge freely, activate carefully, ramp with an agent

The claim: the deployment step, not the coding step, is the real bottleneck, and feature flags are how you dissolve it for agents. Vaibhav draws the engineering loop and points at the stretch from PR to deploy: "this whole section is basically the bottleneck." Code and debugging are fast; manual review and release are slow, which is "why we're shipping slop all the time." The non-obvious move is a permission split: an agent "should be allowed to merge to prod, but it shouldn't be able to turn things on on prod." Merge is cheap and reversible when everything ships flag-off by default; activation is the committal act. Dexter adds the real magic: don't just gate by population, gate by time, "turn it on at 0.01%, make sure nothing's broken, and gradually ramp it up," with the agent reviewing the ramp. It generalizes to database migrations via dual-write, dual-read, backwards-compatible schemas. It goes wrong when teams over-automate on day one and "spend 3 months building a software factory," or let dead flags rot into slop.

---

# 🎬 Proposed ACS videos

## 1. Give Your Agent Back Pressure It Doesn't Have Yet

- TITLE: Give Your Agent Back Pressure It Doesn't Have Yet
- HOOK: Agents nail anything they can test and fumble everything they can't. Here's how to fake the test.
- THE PROMISE: For engineers letting agents build UI or "taste" work, one thing you can do after: turn an un-checkable judgment into a real metric the agent can iterate against.
- THE SHAPE:
  1. Show the failure: agent builds a UI with a screenshot loop and still can't judge it.
  2. Name the principle: agents need back pressure, and some work has none locally.
  3. Demo: ship three variants behind flags, wire up a conversion metric, let the agent pick the winner.
  4. Second domain: agent reads production traces to plan a cheaper model migration.
  5. Failure modes: slow, noisy, or biased metrics that produce a misleading signal.
- SPINE: A
- SLOT: Techniques class > Closing the Loop chapter (the next-step video after the filmed "closing-the-loop").
- RELATIONSHIP: 🔗 complements "closing-the-loop" by being its next step. That video teaches giving the agent an automated way to check its own work (run it, read the error, iterate); this one answers what to do when no local check exists, by manufacturing one from production metrics.
- PROOF TO REUSE: "you've given the model the ability to actually get its own back pressure"; the motion-graphics failure and "AI vision is just not good enough to get things pixel perfect"; the 3% / 7% / 5% conversion-rate variant example.

## 2. Let Your Agent Ship to Prod (Without Letting It Turn Things On)

- TITLE: Let Your Agent Ship to Prod Without Letting It Turn Things On
- HOOK: Your agent can write and merge code fast. Deploying it safely is the part that's still broken.
- THE PROMISE: For teams running agents against real code bases, one thing you can do after: build a graduated feature-flag rollout an agent drives itself, starting from a CLI, not a platform.
- THE SHAPE:
  1. Draw the loop: write-and-test is hot, PR-to-deploy is the bottleneck.
  2. The permission split: agents may merge to prod but not activate; everything ships flag-off.
  3. Demo the ramp: deploy off, turn on at 0.01% for a short duration, collect metrics, roll back or forward.
  4. The two dimensions: population AND time, so a 10-second full-traffic burst is a valid sample.
  5. Build it incrementally from a CLI/MCP; warn against the day-one software factory and dead-flag slop.
- SPINE: B
- SLOT: Master Claude Code class > new "Safe Production Rollouts" chapter (adjacent to the planned DevBoxes class on limiting blast radius).
- RELATIONSHIP: ❌ net-new. Nothing in the catalog covers feature flags, production rollout, or the merge-versus-activate split; DevBoxes is planned but is about sandboxing agents pre-prod, not ramping their code safely in prod.
- PROOF TO REUSE: "it should be allowed to merge to prod, but it shouldn't be able to turn things on on prod"; "turn it on at 0.01%, make sure nothing's broken, and gradually ramp it up"; the day-one warning, "you're going to spend 3 months building a software factory instead of actually shipping value."

---

# 📚 Full wisdom (reference)

## SUMMARY
On AI That Works, BAML's Vaibhav and Human Layer's Dexter explain how feature flags let coding agents ship to production gathering metric back pressure safely.

## IDEAS
- Feature flags let agents ship code to production but keep risky features switched off until proven.
- Coding agents excel at problems with automated back pressure: compile, test, and run feedback loops repeatedly.
- Agents fail badly at unmeasurable judgments like whether a UI looks good or users feel happy.
- Deploying three UI variants behind flags turns taste into conversion metrics the agent can actually read.
- Feature flags carry two independent dimensions: percentage of users affected and duration the flag stays on.
- You can activate a flag for just ten seconds instead of one percent of the population.
- Agents should be allowed to merge to production but never permitted to turn features on themselves.
- The real magic is ramping a flag from 0.01 percent upward while an agent watches metrics.
- The write-and-test loop is incredibly hot and fast, but the PR-to-deploy stretch remains the real bottleneck.
- The granularity ladder climbs staging, dev-versus-staging, per-developer sandboxes, then feature flags as a new slicing dimension.
- More headcount, or more agents, demands more granularity so nobody blocks anyone else while shipping fast.
- Run experiments with pulled production data during code review, like a CI check on offline metrics.
- Dead feature flags accumulate as slop; staff engineers waste time cleaning abandoned experiments and dead paths.
- Database schema changes need dual-write, dual-read migrations kept backwards compatible so users move on and off.
- Vaibhav wants experiments orthogonal to the main branch, with a fixed budget of live experimental traffic.
- One customer had an agent analyze BAML traces to migrate models and cut cost twenty percent.

## INSIGHTS
- Feature flags manufacture back pressure where none exists locally, extending agents into judgment-heavy work like UI.
- Separating merge rights from activation rights lets agents ship freely without ever owning production risk directly.
- Deployment, not coding, is the true bottleneck; feature flags add post-deploy granularity that unblocks fast shipping.
- Time and population are separate flag levers; brief full-traffic bursts sample reality faster than tiny cohorts.
- Every production deployment is really an experiment, so backwards compatibility and instant rollback are permanent requirements.
- Faster shipping forces measuring everything; unmeasured merges tax you by hiding whether real users like features.
- Build the rollout pipeline incrementally from a simple CLI, not a three-month software factory built upfront.
- Cheap tokens make nuke-and-rewrite genuinely viable when you own good, testable interfaces around the target component.

## QUOTES
- "you've given the model the ability to actually get its own back pressure" (Dexter)
- "it should be allowed to merge to prod, but it shouldn't be able to turn things on on prod" (Vaibhav)
- "the real magic is like turn it on at like 0.01%, make sure nothing's broken, and then gradually ramp it up" (Dexter)
- "this whole section is basically the bottleneck" (Vaibhav)
- "There's like two dimensions on which feature flags can be turned on. There's time and then number of users impacted." (Vaibhav)
- "taking screenshots of the web app is not really a good back pressure thing because AI vision is just not good enough to get things pixel perfect" (Dexter)
- "The whole point of the system is to build a more granular and granular version of your code base." (Vaibhav)
- "don't try to do that from day one because you're going to spend 3 months building a software factory instead of actually shipping value" (Dexter)
- "spend the extra hour prompting with Claude to get it right" (Vaibhav)
- "database schemas are just a known hard problem, but that also means that there are known good solutions to them. You don't have to invent anything." (Vaibhav)

## HABITS
- They run agents overnight and watch them on a big screen like a live sporting event.
- They refactor incrementally by cleaning code they touch, occasionally nuking a component and rewriting from scratch.
- They store every BAML function call and later access the API to analyze full usage patterns.
- They give each developer an isolated sandbox environment so teammates never fight over staging test slots.
- They start automation with a CLI or MCP querying data before building any autonomous rollout system.
- They deploy features flag-off by default so that any merge stays low-risk until deliberately switched on.
- They define a concrete metric per experiment: revenue, click-through, engagement, or error rate, before shipping anything.
- They spend extra prompting time getting low-stack schema decisions right rather than painfully patching them later.

## FACTS
- Feature flags predate AI and exist throughout large-company codebases to avoid accidentally impacting millions of users.
- Feature flags originally emerged to avoid merging thousands of lines of untested code in one change.
- At Google the speakers refactored core AR algorithms and deployed the changes first to low-end phones.
- Startups rarely run backend A/B experiments; they mostly experiment on landing pages, not large backend changes.
- Vaibhav builds an agent-first programming language called BAML and is imminently releasing it to early users.
- Dexter founded Human Layer, a company helping coding agents solve hard problems in complex code bases.
- Building a full feature-flag rollout pipeline is estimated at roughly one week of infrastructure work maximum.
- SaaS keeps two versions live simultaneously, unlike distributed languages where fifty versions run in the wild.

## REFERENCES
- Martin Fowler (writing on feature flags)
- Ron Jeffries (blog post on refactoring and technical debt)
- BAML / Boundary (Vaibhav's agent-first programming language)
- Human Layer (Dexter's company)
- Code Rabbit (automated code review tool)
- Ralph / "Ralph Wiggum" agent technique and the "fish bowl" of watching agents run
- Gemini 3.0 flash and Gemini 2.5 flash (model migration example)
- Zeke (referenced on A/B testing)
- AI That Works podcast (the show itself)

## ONE-SENTENCE TAKEAWAY
Feature flags give agents production metrics as back pressure, letting them safely ship and self-correct.

## RECOMMENDATIONS
- Deploy risky agent-written features behind flags turned off, then activate briefly to sample real production behavior.
- Give agents full merge access to production but withhold the ability to flip features on themselves.
- Ramp each new flag from 0.01 percent upward and let an agent review metrics between steps.
- For UI work, ship multiple variants and let the agent choose by conversion rate, not taste.
- Add a CI step that pulls real production data and checks offline metrics before merging code.
- Start with a simple CLI or MCP querying flag metrics before automating the whole rollout loop.
- Budget your live experiments like Kanban: cap them, and retire an old one before adding new.
- Schedule regular cleanup of dead feature flags so abandoned experiments never rot into unmaintainable production slop.
