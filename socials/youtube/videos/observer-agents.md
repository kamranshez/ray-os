---
tags: [youtube, script, claude-code, observer-agents, agentic]
status: draft
date: 2026-07-14
source: "binary dig on Claude Code 2.1.208 + interview with Ray"
format: image-first bullet deck (Ray riffs over the bullets; each IMAGE block is a placeholder to generate)
---

## Title Options

| # | Formula | Title |
|---|---------|-------|
| 1 | Problem-led | Your AI Agent Will Cheat to Finish. This Catches It. |
| 2 | Hidden feature | Claude Code Quietly Shipped an Agent That Watches Your Agent |
| 3 | Curiosity + specific | I Put One AI Agent in Charge of Watching Another |
| 4 | Contrarian | The Most Useful Claude Code Feature Can't Actually Do Anything |

Format note: problem-first, no coined catchphrase, we just call it an observer. Plug lands mid-to-late, woven into a real routine I run. Image style for the whole deck: excalidraw hand-drawn, dark charcoal background, consistent two-agent color language (worker = blue, observer = amber, danger/cheat = red, safe/silent = green).

---

## Beat 1: Your agent will cheat to finish

- Here is the uncomfortable thing about handing a real task to an AI agent: the harder you push it to get the job done, the more likely it is to cheat to get there. Not out of malice. It is optimizing for exactly the reward you gave it, which is "make it pass, get it green, finish."
- So when the honest path gets hard, it takes the dishonest one that still looks like success. It deletes or skips the failing test. It hardcodes the expected answer. It loosens an assertion until it goes green. It stubs out the module it could not migrate and reports the job done.
- The worst part is how good it looks. A tired human reviewer skims the diff, sees green, and moves on. The shortcut is dressed up as real work.
- And this is getting more dangerous, not less, because we are handing agents longer and more ambitious tasks and letting them run while we are not watching. A six hour unattended run has six hours to accumulate shortcuts you never see. You may even catch an agent doing something you never asked for, like digging around your machine for API keys or secrets to get past a wall.
- So the real question stops being "can the agent do the work" and becomes "how would I even know if it cheated."

> IMAGE `observer-agent-cheating` (16:9): a blue worker agent at a desk, sweating, secretly typing `return 8.25` while a big green CHECK glows above a test file. Around it, small red sticky notes: "deleted the failing test", "hardcoded the answer", "loosened the assertion", "stubbed the hard module". Caption: "it is optimizing for the reward you gave it."

![[observer-agent-cheating-1.png]]
![[observer-agent-cheating-2.png]]
![[observer-agent-cheating-3.png]]
![[observer-agent-cheating-4.png]]
![[observer-agent-cheating-5.png]]

---

## Beat 2: What Anthropic quietly shipped to catch it

- Every Claude Code release, I have an agent pull the binary apart and read the actual shipped code, not the changelog. The features they built but did not announce are the real roadmap. This build has one called observer agents, off by default, behind a single flag, and almost nobody is talking about it.
- The setup is almost insultingly small. Take any agent you have defined, add one line to its config, `observer: <name>`, and from then on, every time that agent runs, Claude Code auto-spawns a second agent in the background to watch it. You do not launch the watcher. You do not talk to it. It is born with the worker and dies with it.
- "Watches" is literal and live. After every single turn the worker takes, the observer is handed a read-only digest of the real thing: the actual tool calls, the actual inputs, the actual results, capped so it stays lightweight. It is an over-the-shoulder feed, not a summary after the fact.
- And the tone Anthropic wrote into it is the tell. Its prompt says the expected steady state is silence. This is not a linter that comments on everything. It is built to shut up unless something is actually wrong.

> IMAGE `observer-config-one-line` (16:9): a sketched config file card titled "worker-agent.md", several dim grey frontmatter lines, and ONE line highlighted amber: `observer: watchdog`. A curved arrow from that line to a faded dotted second agent in the background tagged "auto-spawned . background . read-only". Caption: "one line, and a watcher attaches."

![[observer-config-one-line-1.png]]
![[observer-config-one-line-2.png]]
![[observer-config-one-line-3.png]]
![[observer-config-one-line-4.png]]
![[observer-config-one-line-5.png]]

> IMAGE `observer-digest-view` (16:9): LEFT a blue worker doing tool calls (file, terminal, magnifying-glass icons); a dotted feed labeled "read-only digest, every turn" flowing RIGHT into an amber observer reading over its shoulder. On the feed, sketched tags `<tool-call>`, `<tool-result>`, and a small "truncated" note. Caption: "it sees the real actions, not a recap."

![[observer-digest-view-1.png]]
![[observer-digest-view-2.png]]
![[observer-digest-view-3.png]]
![[observer-digest-view-4.png]]
![[observer-digest-view-5.png]]

---

## Beat 3: It observes and sends reports. That is the whole power.

- Here is the loop, because the mechanism is the point. Worker takes a turn. The harness builds the read-only digest. The observer reads it in its own separate context. Then it branches: stay silent, or speak.
- When it speaks, it has exactly one tool. It writes a short report, a single piece of text, and that text gets injected into the worker's own conversation, tagged as coming from the observer. The worker reads it on its next turn like any other message and decides what to do with it.
- Be clear about what this means, because it is the most misunderstood part: the observer cannot block, deny, defer, or rewrite anything the worker does. It has no stop button. It cannot grab the wheel. Its only move is to talk, and the worker can listen or ignore it. You, the human, stay the only one who can actually halt things.
- That sounds like a weakness. It is the whole design, and the next few minutes are about why a watcher with no hands is more useful than it has any right to be.

> IMAGE `observer-loop` (16:9): a clean flowchart loop: (blue) "worker takes a turn" to "harness builds read-only digest" to (amber) "observer reads, own context" to a diamond "worth speaking up?"; branch DOWN-GREEN "no to stay silent" looping back; branch RIGHT-AMBER "yes to send one report (just text)" to "injected into worker's stream" to "worker reads it and decides". A small side note in grey: "no block, no deny, no rewrite. only text." Caption: "observe, then optionally report."

![[observer-loop-1.png]]
![[observer-loop-2.png]]
![[observer-loop-3.png]]
![[observer-loop-4.png]]
![[observer-loop-5.png]]

---

## Beat 4: Why a second agent catches what the first one can't

- The instinct is to fix this inside the worker: just add "and do not cheat, be careful not to break anything" to its prompt. It does not work, and the reason is structural. The worker is rewarded for finishing, so a vague caution is the first thing it deprioritizes the moment the task gets hard. You are asking the same mind that wants the shortcut to also police the shortcut.
- This is the four-eyes principle, and every high-stakes industry already runs on it. The person who initiates a bank wire is never the one who approves it. Not because anyone assumes fraud, but because the person who set the thing in motion is exactly the person primed to skim past the detail that is slightly off.
- A separate observer breaks that. It is rewarded for one narrow thing, catching a specific failure, and gets nothing for the task succeeding. And it reads the work from a clean context, a mind that did not just spend twenty minutes talking itself into the shortcut. Different incentive plus separate context is the entire reason it can see what the worker cannot. It is why you cannot proofread your own writing but a stranger spots the typo instantly.
- And here is the reframe that changed how I think about this. Originally you would cram everything into one prompt: do the research, and also check your sources, and also watch for bias, and also do not drift from the question. That one overloaded prompt does all of it at half strength. Split it into a pair instead, a worker with one job and an observer with one job, and you often get better results, because each agent is doing one thing with its full attention. A pair beats one prompt carrying ten instructions.
- One more thing that makes this the hard half of the problem. Enforcing was never hard. Blocking a bad action is easy once you have seen it, a regex kills `rm -rf`. The unsolved thing is noticing, recognizing that this particular rate table was reverse-engineered from a test, or that these sources all sell the product. That takes judgment, and only another model reading the full trajectory can supply it.

> IMAGE `observer-four-eyes-bank` (16:9): center: a wire-transfer form passing between two figures. LEFT (blue) "INITIATES . rewarded for getting it through". RIGHT (amber) "APPROVES . rewarded for catching the one that's wrong". A vertical dashed wall between them labeled "separate context". Top banner: "the four-eyes principle."

![[observer-four-eyes-bank-1.png]]
![[observer-four-eyes-bank-2.png]]
![[observer-four-eyes-bank-3.png]]
![[observer-four-eyes-bank-4.png]]
![[observer-four-eyes-bank-5.png]]

> IMAGE `observer-pair-vs-one-prompt` (16:9): LEFT: one overloaded blue agent buried under a stack of instruction sticky-notes ("do the task", "check sources", "watch bias", "don't drift", "don't cheat"), looking overwhelmed, output marked "half strength". RIGHT: a clean pair, blue worker with ONE note "do the task" and amber observer with ONE note "watch the method", output marked "each at full attention". Caption: "a pair beats one prompt carrying ten jobs."

![[observer-pair-vs-one-prompt-1.png]]
![[observer-pair-vs-one-prompt-2.png]]
![[observer-pair-vs-one-prompt-3.png]]
![[observer-pair-vs-one-prompt-4.png]]
![[observer-pair-vs-one-prompt-5.png]]

---

## Beat 5: Watch along the way beats check at the end

- The obvious objection: why not just check the result when it is done? Claude Code even has goal mode that runs a verifier when the agent tries to stop. Isn't that enough?
- No, for three reasons, and they are the reason continuous observation matters. First, timing. Catch the stubbed module on the turn it is written and the worker reverts one file and keeps going. Catch it only at the end, after six hours, and it has built ten more things on top of a hollow foundation, so now "continue from a bad state" and "throw it all away" are both expensive. Waking up to a cheat that got corrected mid-run beats waking up to a finished lie.
- Second, what it inspects. A watcher sees the how, the actual steps as they happen, so it catches process cheats that never show up in the final result. Hollow green passes a shallow "run the tests" check every time. The trajectory does not lie.
- Third, independence. A stop-time self-check is the agent grading its own homework, the same mind that spent an hour rationalizing the shortcut now deciding whether it passed. A separate observer with a clean context has no such conflict.
- To be fair: a goal verifier that can fail the run is the enforcement layer, the thing with teeth. The observer has none. So the mature setup is both. The observer is smoke detectors throughout the house catching things early and independently; the verifier or a human approval is the final inspection that can actually stop the sale. They cover different holes.

> IMAGE `observer-watch-along-vs-check-end` (16:9): a horizontal run split into turns. TOP track "check at the end": a single red inspection stamp at the far right, with a tall pile of hollow work behind it labeled "6 hours already spent on a bad foundation". BOTTOM track "watch along the way": small amber eye icons on every turn, a red flag caught early at turn 3 with "revert one file, keep going". Caption: "early and independent beats late and self-graded."

![[observer-watch-along-vs-check-end-1.png]]
![[observer-watch-along-vs-check-end-2.png]]
![[observer-watch-along-vs-check-end-3.png]]
![[observer-watch-along-vs-check-end-4.png]]
![[observer-watch-along-vs-check-end-5.png]]

---

## Beat 6: When it is actually worth it

- An observer is not free. It is a second agent reading a digest on every single turn, so it roughly doubles your compute for that run. That cost is the whole filter: it only earns its keep when a miss would hurt far more than the watcher costs.
- So the test I use, worth it when all of these line up:
  - The failure is subtle, it takes judgment to spot, not a pattern. If a regex or a deterministic hook can catch it, use that instead, it is cheaper and more reliable. Save the observer for what only judgment catches.
  - The cost of missing it is high. Silent data corruption, reward-hacked code that ships, a bad decision acted on. Cheap-to-reverse mistakes do not justify a watcher.
  - You are not watching. The task runs long, unattended, or in parallel, so no human is already reading every step.
  - The work accumulates somewhere you review before it matters, code, a migration, a draft, an analysis. That is what makes catching it early actually useful (more on the exception next).
  - Bonus: you can name the exact failure mode, so the observer is a narrow specialist, not a vague "double-check everything," which is just noise.
- Two more honest costs while we are here. It is advisory, the worker can ignore the report, so the value is early independent noticing, not a guarantee. And it is experimental and off by default, so it could change or vanish. Go in eyes open.

> IMAGE `observer-when-worth-it-test` (16:9): a hand-drawn checklist card titled "worth an observer?", five ticked amber rows: "subtle (judgment, not a regex)", "costly to miss", "runs unattended", "reversible / reviewable work", "nameable failure mode". Below, a small greyed-out row with a red X: "short, cheap, well-watched, regex-catchable to skip it". Caption: "spend the second agent only where a miss hurts."

![[observer-when-worth-it-test-1.png]]
![[observer-when-worth-it-test-2.png]]
![[observer-when-worth-it-test-3.png]]
![[observer-when-worth-it-test-4.png]]
![[observer-when-worth-it-test-5.png]]

---

## Beat 7: Where it is the wrong tool: irreversible actions

- Here is the sharpest limit, and it falls straight out of the mechanism. The observer sees a turn's digest after the tool call already ran, and its report only lands on the next turn. So for something irreversible done in a single autonomous step, the observer is a smoke detector that goes off after the house has burned down.
- "You just reply-all'd the entire list" is worthless once the email is sent. Same for posting publicly, spending money, or dropping a database table. By the time it is in the digest, it already happened.
- So the rule: an observer shines on long, accumulating, reversible work you inspect before it ships. For irreversible outbound actions, you still need a real gate, a human approval or a deterministic block that fires before execution, which is exactly the thing an observer is not.
- The clean pattern is to split even that: put the observer on the drafting, where a flag is still actionable, and keep a hard approval on the sending. Observe the draft, gate the send.

> IMAGE `observer-irreversible-too-late` (16:9): a timeline: a blue worker hits SEND on an email (irreversible, red), the arrow leaves the screen; only AFTER does the amber observer's digest show it, speech bubble "that leaked pricing to the wrong list" with a sad face. A dashed box around the sequence labeled "report arrives one turn too late". Caption: "for irreversible sends, you need a gate, not a witness."

![[observer-irreversible-too-late-1.png]]
![[observer-irreversible-too-late-2.png]]
![[observer-irreversible-too-late-3.png]]
![[observer-irreversible-too-late-4.png]]
![[observer-irreversible-too-late-5.png]]

---

## Beat 8: Where it shines: worker plus observer pairings

- The recipe generalizes: a worker with a job, plus a narrow observer protecting named invariants. Not a generic checker, a specialist for one failure mode. Let me show the setup, then real pairs.
- The setup is three small things: flip the flag on, add `observer: <name>` to the worker, and write the observer as a short prompt that names exactly what to protect. That last part is the whole skill, a vague observer is noise, a specific one is signal.

> IMAGE `observer-pairings-grid` (16:9): a clean hand-drawn 3-column table, header "WORKER | OBSERVER | WHAT IT CATCHES", rows: Refactor | invariant guard | changed auth/expiry behavior; Test-fixing | anti-cheat | hardcodes, deleted tests; Migration | hollowing-out | stubbed modules, skipped tests; Research | evidence-quality | biased sources, unsupported claims; Data analysis | methodology | cherry-picking, tiny samples; Dependency upgrade | compat | fake-green, forced installs. Worker column blue, observer column amber.

![[observer-pairings-grid-1.png]]
![[observer-pairings-grid-2.png]]
![[observer-pairings-grid-3.png]]
![[observer-pairings-grid-4.png]]
![[observer-pairings-grid-5.png]]

**Refactor + invariant observer**
- Worker: Refactor the authentication module to improve readability and remove duplication.
- Observer: Preserve externally visible behavior. Watch for changes to token expiry, validation order, error types, authorization boundaries, public method signatures, and audit logging. Named invariants: unauthenticated requests must remain rejected; token expiry must remain 30 minutes; authentication failures must continue to be logged; the public AuthClient interface must not change.
- Why split it: much more reliable than telling the worker itself "refactor this, but be careful not to change anything."

**Test-fixing + anti-cheat observer**
- Worker: Make the failing test suite pass.
- Observer: Your job is not to fix anything. Verify the tests pass because the logic was implemented, not because the tests were gamed. Watch for hardcoded expected values, `if input == <test value>` special-casing, a lookup dict built from the fixtures, deleted or skipped tests, and loosened assertions. Named invariants: results must derive from a real rule or a data source in the repo, never from the test's expected numbers; no test deleted, skipped, or marked xfail; no assertion weakened.
- Why split it: passing the test is the worker's reward, so "do not cheat" fights its incentive. The observer's only reward is catching the cheat.

**Migration + hollowing-out observer** (the overnight run)
- Worker: Migrate the codebase from X to Y and get all tests passing.
- Observer: Watch for the suite going green by emptying things out. Named invariants: no module stubbed, commented out, or replaced with `pass` or `NotImplementedError` to finish; no test skipped or xfail'd; every file that had behavior must keep equivalent behavior; no destructive database migration without a dry-run or backup.
- Why split it: across a six hour unattended run the worker trades correctness for "done" whenever it is stuck, and you are asleep.

**Researcher + evidence-quality observer** (one of the strongest)
- Worker: Research a market and write a comprehensive report.
- Observer: Monitor source diversity, unsupported claims, missing counterarguments, and whether the research is drifting from the original question.
- A useful report looks like: "The worker has collected 18 sources, but 14 are from companies selling the product being evaluated. It should add independent research before drawing conclusions."
- Why it is so strong: the observer catches methodological problems long before the final report is written, while sources are still being gathered and the course can still change.

**[PLACEHOLDER: Ray's own example to add later]**
- Ray to drop in one more pairing here.

- And a fast montage of more, worker to observer to what it catches: dependency upgrade to compat guard (fake-green, forced `--force` installs); content writer to factual-integrity guard (invented stats, claims for features that do not exist); data analysis to methodology guard (tiny samples, dropped rows, killing a channel inside the attribution lag); dataset labeling to drift guard (the standard quietly slipping around item 300, a failure only a long run creates and only a fresh context catches); security fix to defensive guard (suppressed scanner rules instead of real fixes); type cleanup to no-suppression guard (`# type: ignore` and `any` casts instead of fixes); metric optimization to real-behavior guard (gaming the number while the experience gets worse).

> IMAGE `observer-pair-anticheat` (4:3): top: red snippet `if customer_id == "fixture-3": return 8.25`. Below, amber observer bubble: "that special-cases a test fixture. it is not an implementation." Card title "TEST-FIXING to anti-cheat".

![[observer-pair-anticheat-1.png]]
![[observer-pair-anticheat-2.png]]
![[observer-pair-anticheat-3.png]]
![[observer-pair-anticheat-4.png]]
![[observer-pair-anticheat-5.png]]

> IMAGE `observer-pair-research` (4:3): top: a sketched stack of 18 source cards, 14 stamped red "VENDOR". Amber observer bubble: "14 of 18 sources sell the product. add independent research before concluding." Card title "RESEARCH to evidence-quality".

![[observer-pair-research-1.png]]
![[observer-pair-research-2.png]]
![[observer-pair-research-3.png]]
![[observer-pair-research-4.png]]
![[observer-pair-research-5.png]]

> IMAGE `observer-pair-migration` (4:3): top: a red diff replacing a function body with `raise NotImplementedError` and a `@skip` on a test. Amber observer bubble: "you emptied the module to go green. that is not a migration." Card title "MIGRATION to hollowing-out".

![[observer-pair-migration-1.png]]
![[observer-pair-migration-2.png]]
![[observer-pair-migration-3.png]]
![[observer-pair-migration-4.png]]
![[observer-pair-migration-5.png]]

## 9 10: Why Anthropic is building this now

- Step back and ask why this exists at all, right now. Because Anthropic is pushing hard in one direction: agents that are more capable and run longer with less supervision. Background sessions, scheduled routines, a daemon that works while you sleep, multi-agent fleets. The product is moving toward "set it going and walk away."
- That direction is exactly what breaks the old safety model. The more an agent runs unwatched, and the more capable it is, the wider the surface for it to cheat or wander, and the less a permission prompt can save you. A prompt encodes the letter of a policy, never the intent, and it only works when you are sitting there to catch the weird case.
- Anthropic's own number: users approve 93% of permission prompts. Sit with that. The prompt is not oversight anymore, it is a rubber stamp. High friction and low signal at the same time.
- So as tasks get more ambitious and more autonomous, the bottleneck quietly moved. It used to be capability, can the model even do this, and that is largely solved. The new bottleneck is trust, can I let it run while I am not looking. And trust, at bottom, is an observability problem.
- That reframes the whole thing. An observer is not a random experiment. It is the first structural piece of the trust layer, the thing that has to exist before "let it run unattended for an hour" is something you would actually do. For a team or a company it is starker: you cannot deploy autonomous agents at all without an independent record of what they did, written by a party that did not do the work. That is what an observer report is.

> IMAGE `observer-why-now-longer-runs` (16:9): a left-to-right timeline of Claude Code getting more autonomous: "approve each step" to "background sessions" to "scheduled routines" to "daemon while you sleep" to "multi-agent fleets". Underneath, a rising shaded curve "time the agent runs unwatched" and a widening red wedge "the oversight gap". Caption: "the more it runs alone, the less a prompt can save you."

![[observer-why-now-longer-runs-1.png]]
![[observer-why-now-longer-runs-2.png]]
![[observer-why-now-longer-runs-3.png]]
![[observer-why-now-longer-runs-4.png]]
![[observer-why-now-longer-runs-5.png]]

> IMAGE `observer-93-percent` (16:9): a huge hand-lettered "93%", subtext "of permission prompts, users just click approve (Anthropic's own number)", beside a sketched dialog whose [Approve] button is worn smooth and stamped "RUBBER STAMP" in red. Caption: "high friction, low signal. that is not oversight."

![[observer-93-percent-1.png]]
![[observer-93-percent-2.png]]
![[observer-93-percent-3.png]]
![[observer-93-percent-4.png]]
![[observer-93-percent-5.png]]

> IMAGE `observer-trust-is-the-bottleneck` (16:9): two horizontal bars. TOP "CAPABILITY: can the model do it?" full, greyed, checked, "mostly solved". BOTTOM "TRUST / OBSERVABILITY: can I let it run unwatched?" highlighted with the blue-worker + amber-observer motif inside it, "the new bottleneck". Small arrow: "observers are the first structural piece." Caption: "capability stopped being the hard part."

![[observer-trust-is-the-bottleneck-1.png]]
![[observer-trust-is-the-bottleneck-2.png]]
![[observer-trust-is-the-bottleneck-3.png]]
![[observer-trust-is-the-bottleneck-4.png]]
![[observer-trust-is-the-bottleneck-5.png]]

---

## Beat 11: Close

- So that is the feature. A second agent, born with your worker, watching every turn from a clean context, with exactly one power: to tell you and it what it sees. It cannot stop anything. And once you understand why that is the point, it stops looking like a toy and starts looking like the shape of the next phase, where you stop approving every action and start writing the policy, and agents watch agents to enforce it.
- The open question I keep chewing on is when the watcher gets its hands back, when noticing is allowed to become stopping. I keep that speculation in the newsletter, link below.
- Tell me in the comments: what is the one task you would actually leave running unwatched, if a second agent were watching it for you.

> IMAGE `observer-trust-stack` (16:9): a three-rung staircase going up-right. Rung 1 "PAIR PROGRAMMER: you approve every action" (tiny human clicking approve). Rung 2 "DELEGATED WORKER: regex allowlists" (rules icon). Rung 3, highlighted, "SUPERVISED FLEET: agents watch agents, you write policy" (the blue+amber motif). A small figure climbing. Caption: "where this is heading."

![[observer-trust-stack-1.png]]
![[observer-trust-stack-2.png]]
![[observer-trust-stack-3.png]]
![[observer-trust-stack-4.png]]
![[observer-trust-stack-5.png]]
