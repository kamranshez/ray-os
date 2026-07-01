---
title: "How METR measures Long Tasks and Experienced Open Source Dev Productivity - Joel Becker, METR"
video_url: https://www.youtube.com/watch?v=k1t2xyWMUdY
video_id: k1t2xyWMUdY
channel: AI Engineer
published: 2026-01-19
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**How METR measures Long Tasks and Experienced Open Source Dev Productivity - Joel Becker, METR**](https://www.youtube.com/watch?v=k1t2xyWMUdY) - AI Engineer - uploaded 2026-01-19

> net-new and next-step ACS videos available

## The idea worth a video

- **Spine A: AI coding help inverts with your own expertise.** It slowed experienced developers on mature repos they knew cold, and helped most on unfamiliar, undocumented legacy code. VERDICT: ❌ net-new video available.
- **Spine B: Agents fail on real data work because the context is undocumented, not because they cannot write SQL.** The bottleneck is tribal knowledge about what the data means. VERDICT: 🟡 partial, substantially covered by the Context Engineering class (deep-dive kept, no pitch).
- **Spine C: Match the task to the model's in-distribution interface.** Agents are far stronger over CLI and text than over GUI or computer use, so reshape browser tasks into text harnesses. VERDICT: 🔗 next-step video available.

## Summary + counts

Joel Becker of METR discusses their developer-productivity RCT, time-horizon measurements, why experienced open-source developers weren't sped up by AI, and where models actually still fail.

🔴 1 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine A: AI help inverts with your expertise

The claim: AI coding help inverts with your own expertise. On the mature repositories these developers had lived in for years, agents made them slower; the code they were helped on most was unfamiliar legacy that nobody had documented.

Why it's non-obvious: the industry assumes senior engineers extract the most from AI. The METR RCT found the opposite for people working where they already hold deep mental context.

Why it's true: when you already know exactly how to execute a task, the agent adds two costs and little value. First you pay verification time to check its work; then you pay cleanup time, because it solves problems in ways that clash with the repo's conventions and its maintainability bar. Both costs exceed the shrinking benefit. On code you do not know, orientation is the expensive part, and that is precisely what the agent absorbs.

What it generalizes to: writing. An editor rewriting their own polished draft loses time, while the same editor untangling someone else's messy legacy document gains hugely. The lever is your starting context, not the tool.

How it goes wrong: the effect is measured on elite open-source repos with brutal quality bars. In a typical business codebase where shipping beats maintainability, the cleanup penalty shrinks and the inversion weakens.

### Spine B: Data failures are a context problem, not a SQL problem

The claim: agents fail on real data work not because they cannot write SQL, but because the context they need is undocumented, contradictory, and locked in people's heads.

Why it's non-obvious: models now write SQL, Pandas, and Polars fluently, so teams assume analytics is nearly automated. The bottleneck quietly moved upstream, to knowing what the data actually means.

Why it's true: an analyst-agent asked for the P90 time between deployments hits a wall the code cannot cross. There are five thousand tables named impressions. A date column silently switches format after an undocumented cutoff. Deployment-to-PR mapping does not exist in the telemetry and must be recovered from the GitHub API. None of that is written anywhere, so a fluent SQL writer with no context produces confidently wrong answers.

What it generalizes to: onboarding a human. A brilliant new hire with no tribal knowledge is equally stuck; the fix in both cases is externalizing the knowledge into a context file the agent reads, plus fixing the data at the source.

How it goes wrong: some knowledge is genuinely irrecoverable, and building that infrastructure competes with the analyst's real deadline to ship one report, so it keeps getting skipped.

### Spine C: Match the task to the model's in-distribution interface

The claim: match the task to the model's in-distribution interface. Agents are far more capable over CLI and text than over GUI or computer use, so reshaping a browser task into a text harness raises the ceiling.

Why it's non-obvious: a year ago computer-use demos looked impressive, yet almost nobody uses them for real work. People keep pointing agents at the interface built for humans instead of the one built for tokens.

Why it's true: models saw enormous amounts of CLI and text during training and very little pixel-level GUI control, so computer use sits out of distribution. AI Village agents, driven entirely through computer use on fuzzy goals, collapse on basic subtasks. The same models, handed text tools, clear far harder work. The interface, not the underlying intelligence, is often the binding constraint.

What it generalizes to: any integration. Wrapping a REST API or an app as a set of text commands the agent can call beats having it click through screens, which is exactly what a well-scoped tool or plugin does.

How it goes wrong: some tasks are irreducibly visual, and heavy harness-building can cost more than the task itself, so reserve it for repeated workflows.

---

## 🎬 Proposed ACS videos

### 1. Where AI Actually Speeds You Up (And Where It Quietly Slows You Down)

- **HOOK:** METR paid experienced developers to use AI and measured them getting slower, not faster.
- **THE PROMISE:** For working engineers deciding when to reach for an agent, leave knowing the one signal that predicts whether AI helps or hurts on this task.
- **THE SHAPE:**
  1. The counterintuitive result: same developer, agent helps on the repo they don't know, hurts on the one they own.
  2. The mechanism: on code you know cold, you pay verification plus convention-cleanup and skip the orientation the agent is good at.
  3. Demo: run the same task twice, once on Ray's familiar repo, once on an unfamiliar legacy one, and time both.
  4. The heuristic: reach for the agent where orientation dominates; be skeptical where you already hold the plan in your head.
  5. Caveat: business codebases that prize shipping over maintainability weaken the effect.
- **SPINE:** A.
- **SLOT:** Techniques → Working with the Codebase (or a new "When to Reach for the Agent" chapter).
- **RELATIONSHIP:** ❌ net-new. No ACS video frames the reach-for-it decision by your own familiarity. The closest, "Reducing Agent Confusion in Growing Projects" and the "Cleaning Up Legacy Code" chapter, teach cleanup mechanics, not the go or no-go call.
- **PROOF TO REUSE:** the 16-developer slowdown result; "the median PR in the study, the time they spend working on the code post review is zero minutes"; the interviewer's point that the repos he was helped most on "had no decent documentation of any kind."

### 2. Give the Agent a CLI, Not a Browser

- **HOOK:** Everyone hyped computer use a year ago, yet almost nobody ships real work with it.
- **THE PROMISE:** For anyone automating a tool or app, leave able to reshape a flaky GUI task into a text harness the agent actually succeeds at.
- **THE SHAPE:**
  1. The capability gap: agents are far stronger over CLI and text than over GUI or computer use.
  2. Why: text is deeply in distribution, pixel-level control is not, so the same model performs very differently by interface.
  3. Evidence: AI Village agents on computer use fall apart on basic subtasks.
  4. Demo: take a task Ray would do in Chrome, wrap the underlying API as text commands, and let the agent drive that instead.
  5. When not to: irreducibly visual tasks, or one-offs where harness-building costs more than the job.
- **SPINE:** C.
- **SLOT:** Advanced Techniques → a new "Interfaces & Harnesses" chapter.
- **RELATIONSHIP:** 🔗 complements "Your Interaction Layer" (My Daily Workflows), which shows Claude driving OS and app tasks; that video teaches how to hand agents computer workflows, this one adds the why and the move: prefer text over GUI and reshape the task, because computer use is far weaker.
- **PROOF TO REUSE:** "I think computer use is just way worse than CLI based ... capabilities"; the AI Village collapse on fuzzy goals; the transcript's point that "lots of GUI based things can be converted into text things."

*(Spine B produces no pitch: the transferable technique, externalizing hidden project knowledge into a context layer, is substantially covered by "The Context Layer" in Context Engineering, and the pure data-analytics domain sits outside ACS's coding remit. Kept as a deep dive because it is load-bearing for understanding the talk.)*

---

## 📚 Full wisdom (reference)

**SUMMARY** — Joel Becker of METR discusses their developer-productivity RCT, time-horizon measurements, why experienced open-source developers weren't sped up by AI, and where models actually still fail.

**IDEAS**
- METR's field study found experienced open-source developers were slowed down by AI despite expecting large speed-ups.
- Developers feel faster with AI even when measurement shows they are actually working measurably slower overall.
- Nobody can accurately report how long a task took, though perceived-productivity surveys track real quantitative data.
- On mature repos developers know deeply, agents add verification and cleanup overhead that exceeds their help.
- AI helped most on unfamiliar legacy codebases with no documentation and an unavailable original code owner.
- Meta measured a J-curve: developers slow for three-to-six months on agents before their productivity turns positive.
- Three-quarters of the sixteen study developers were completely unfamiliar with the Cursor editor at the start.
- Agents write SQL well but fail on messy enterprise data where schema meanings are largely undocumented.
- LinkedIn reportedly has five thousand tables containing a column named impressions, confusing any analyst or agent.
- Undocumented cutoff dates make columns silently change meaning, defeating agents lacking that unwritten tribal knowledge entirely.
- Computer-use and GUI capabilities lag far behind CLI and text-based capabilities for current AI coding agents.
- Reshaping a task into the model's in-distribution shape, like CLI over browser, boosts agent success sharply.
- AI Village agents pursuing fuzzy goals via computer use consistently fall apart on even basic subtasks.
- The median study PR needed zero minutes of post-review code work, showing an extreme quality bar.
- Open-source maintainers reject PRs that hurt maintainability, a bias absent from typical business get-it-done contexts.
- METR proposes measuring 'watched' versus 'unwatched' time horizons to estimate how monitoring reduces dangerous capability.
- Time-horizon growth may track compute growth, so a compute slowdown implies slower AI capability gains overall.

**INSIGHTS**
- AI's coding value inverts with your expertise: least useful where you already hold the deep context.
- Benchmark scores rising does not imply real-world speed-up, because field conditions include verification and cleanup costs.
- Model failure on messy data work is a missing-context problem, not a code-generation ability problem fundamentally.
- Interface choice is a capability lever: text harnesses unlock performance that GUI computer-use cannot currently reach.
- Self-reported speed-up is worthless for measuring automation risk, because perception tracks hype, not actual task duration.
- Elite open-source repos are a clean experimental control precisely because their quality bar removes population variance.
- Reliability at lower total time, not longer time horizons, becomes the metric that eventually matters most.
- Agents resemble neurodivergent workers: brilliant narrowly, but misfit to a world built and sized for humans.
- Familiarity with a tool improves outcomes by teaching its limits, not by producing raw speed gains.

**QUOTES**
- "I read the paper and I was like oh, this doesn't suck at all." (audience member)
- "the one question you can't ask people on a survey is how long did a task take" (interviewer)
- "legacy code bases don't exist cuz they work well, it's because they make money" (interviewer)
- "the thing that really convinced me is like watch the videos. I watched the videos of them working" (Joel Becker)
- "the state of underlying data is so bad that the ... actual data scientist is going to get way less value out of ... AI than software engineers thought" (interviewer)
- "data specs really matter. Really really matter." (interviewer)
- "they are effectively neurodivergent individuals, right? And ... our world was not built for that." (audience member)
- "I think computer use is just way worse than CLI based ... capabilities" (Joel Becker)
- "the median PR in the study, the time they spend working on the code post review is zero minutes" (Joel Becker)
- "developers will tell you that they were faster when they weren't. And I think that is worth knowing." (Joel Becker)
- "the reason it's not existentially dangerous is that it's not capable of stuff" (Joel Becker)

**HABITS**
- Before big architectural decisions ten conversation turns deep, they stop and think really hard first themselves.
- Scope problems down to smaller pieces because agents cannot reliably handle tasks that are too large.
- Watch full screen recordings of developers working to judge how AI tools truly affect their work.
- They code usage hours conservatively rather than trusting inflated self-reported figures from developer time-tracking software logs.
- Distrust subset plots with wide error bars; only the main large-sample result deserves real analytical confidence.
- Fix bad data at the source instead of endlessly patching every downstream report by hand repeatedly.
- Triangulate AI's true capability from multiple evidence sources with different pros, cons, and independent structural biases.
- Import existing analyst SQL to reverse-engineer how colleagues triangulated meaning from confusing, contradictory warehouse data tables.

**FACTS**
- METR's headline study used sixteen experienced open-source developers working on their own familiar large mature repositories.
- One study developer had logged 140 Cursor hours but was conservatively coded at only 50 hours.
- METR ran an unpublished hackathon randomizing teams to AI-allowed or AI-disallowed, finding roughly four-percentile score differences.
- The Haskell compiler maintainer sometimes argues in PR comments for many hours until specifications match exactly.
- Robotics models receive compute growing at a rate similar to LLMs but two orders lower absolutely.
- Nvidia consumer GPUs like the 5060 through 5090 are the same chip binned by fault tolerance.
- Epoch's forecasts suggest power and physical compute constraints likely don't bite before roughly the year 2030.
- GPQA-expert-beating models still fail at complex real-world data-science tasks that nobody has even benchmarked properly yet.

**REFERENCES** — METR developer-productivity RCT and paper; METR time-horizon measurement figure (the log-linear chart circulated on Twitter); Meta's developer-experience J-curve presentation; Cursor; SWE-bench; GPT-4, GPT-5, and GPT-2 as capability reference points; AI Village (AI Digest); Harvey (legal AI, discovery); Epoch AI (compute forecasts); Simon Marlow and the Haskell compiler (GHC); Hazel Hopper and Arjun Ramani (forthcoming capabilities-taxonomy paper); the LinkedIn "impressions" tables example; the Capital One deployment-metrics example; Pandas and Polars; Joel Becker (x.com/joel_bkr).

**ONE-SENTENCE TAKEAWAY** — AI helps least where you know most; feed agents context and interfaces matching their strengths.

**RECOMMENDATIONS**
- Reach for agents on unfamiliar or legacy code; be skeptical on repositories you already know cold.
- Give data-analysis agents a written context file encoding table meanings, cutoff dates, and team hierarchy locations.
- Convert brittle GUI or browser tasks into CLI or text harnesses matching the model's real strengths.
- Measure real completion time or output quality, never developers' self-reported speed-up, to judge true AI impact.
- Budget for a months-long J-curve dip before expecting real productivity gains from newly adopting coding agents.
- Learn each tool's boundaries deliberately, since familiarity buys judgment about limits rather than raw speed alone.
- Fix messy data at its source before asking any agent to analyze or query it reliably.
- Import colleagues' existing SQL so the agent can reverse-engineer undocumented meaning from prior analyst report work.
