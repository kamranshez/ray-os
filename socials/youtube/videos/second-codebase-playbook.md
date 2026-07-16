---
tags: [youtube, script, claude-code, context-engineering, boris-cherny, second-codebase]
status: draft
date: 2026-07-16
source: "Boris Cherny's 'build the system around the thing' essay + two planning sessions (durability stack, correction loops, hierarchy of controls) + ACS catalog overlap sweep"
---

## Title Options

1. Claude Code's Creator Says Your Job Has Changed
2. Never Correct Your AI Agent Twice
3. You Are Maintaining Two Codebases Now
4. I Delete My CLAUDE.md Rules On Purpose
5. 6 Systems That Stop Your Agents Repeating Mistakes

Coined term: **"the second codebase"**. Format: practical playbook (6 moves, each with a live demo) wearing a discourse hook (Boris Cherny essay). One thesis, not a roundup: every move is the same principle applied at a different tier. Complementary rule: if the title carries Boris/authority, the thumbnail carries the pain (correcting the same mistake again); if the title carries the pain, the thumbnail carries the pyramid or the deletion shot.

Delivery note: bullets are talking cues, riff over them. Lines in quotes are worth saying close to verbatim. Per improvements doc: speak slower, let every screen linger 2 to 3 seconds, clear section breaks between moves.

Claim discipline (do not drift on camera): the promise is zero REPEAT corrections, never "you will barely review." The trajectory claim is that encoded principles catch mistakes you never made. Do not claim total correction volume collapses.

---

## Hook (0:00-0:45)

*Visual in first 10 seconds (improvements doc gap #1): screen recording of a correction being typed to Claude, then a fast montage of the SAME correction being typed on different days. Date stamps flicker. No branding, no intro.*

3-beat hook formula:

- Empathy: "You correct your agent. It apologizes. It fixes it. And tomorrow, in a fresh session, it makes the exact same mistake." That loop, every day, forever.
- Provocative claim: the guy who created Claude Code just said this is your fault, not the agent's. "Boris Cherny says every one of those repeated corrections is a failure of automation. Your automation."
- Scope: "There are six things he is telling you to build. I am going to build all six on a real codebase, and by the last one the direction of correction literally reverses: the system starts correcting me."

> 🎨 DRAW `second-codebase-hook-same-correction-forever`: an engineer typing the same correction to an agent across many days, calendar pages flying, the agent waking up with amnesia each morning

![[second-codebase-hook-same-correction-forever-1.png]]
![[second-codebase-hook-same-correction-forever-2.png]]
![[second-codebase-hook-same-correction-forever-3.png]]
![[second-codebase-hook-same-correction-forever-4.png]]
![[second-codebase-hook-same-correction-forever-5.png]]

---

## The Setup: What Boris Actually Said (0:45-3:00)

*Tweet on screen. Highlight passages as you reference them. This section is HIS argument, compressed and credited. Everything after it is where we go further.*

- The old wisdom: the best engineers always automated their own work. Vim macros, lint rules, e2e suites. Multiplied one person.
- Highlight: "if you are running an army of agents, each of those agents will be sped up also." The multiplier is no longer 1x you. It is every agent you run.
- Highlight: "it's about automating entire types of busywork rather than solving them one off." "This is what loops actually means. Not an agent repeating a task. Killing a whole CLASS of busywork so it never happens again."
- Highlight: "these are failures of automation." A rejected PR, a repeated correction: not a knowledge gap in the contributor. A gap in the infrastructure.
- The ceiling that broke: you used to only encode knowledge that fit types, tests, and lint. Now prose executes. CLAUDE.md rules, review principles, skills, comments, memories: agents read them and change behavior. "If you can write it down, you can automate it."
- Turn to the playbook: "Everyone read this essay and nodded. Almost nobody can tell you what to do about it on Monday. Here is the playbook. The order matters."

---

## Move 1: Write the Load-Bearing Comment (3:00-5:00)

*The 5-minute gateway drug. Cheapest demo in the video.*

Quote on screen: "encoded as code comments and skills and CLAUDE.md rules and memories."

Demo:
- Show a weird piece of real code (the odd retry delay, the strange ordering).
- Run 1, no comment: "clean up this file." Agent helpfully "fixes" the weirdness. It just broke prod behavior.
- Run 2, one comment added above it explaining WHY the weirdness exists. Same cleanup prompt. Agent preserves it and cites the comment as its reason.

- "One sentence of prose just changed the machine's behavior. Comments stopped being documentation. They are load-bearing now."
- Do this today: find the three weirdest spots in your codebase and write the why above each.
- Role line: you just protected knowledge that only existed in your head.

> 🎨 DRAW `second-codebase-load-bearing-comment`: a single code comment shown as a structural beam holding up a building of code, an agent walking past the protected beam instead of demolishing it

![[second-codebase-load-bearing-comment-1.png]]
![[second-codebase-load-bearing-comment-2.png]]
![[second-codebase-load-bearing-comment-3.png]]
![[second-codebase-load-bearing-comment-4.png]]
![[second-codebase-load-bearing-comment-5.png]]

---

## Move 2: Push Every Correction Up the Hierarchy (5:00-9:30)

*The core move and the longest section. Introduces the pyramid visual that the rest of the video keeps lighting up.*

Quote on screen: "Your agent could fix an issue every time it sees that issue happen, but that uses tokens and might miss cases. If Claude instead writes a lint rule, CI step, or routine, that class of issue can be fully automated forever."

The hierarchy (safety engineering's hierarchy of controls, applied to agents):

1. Eliminate: change the architecture so the mistake is impossible or pointless. Zero context cost, forever.
2. Guard: lint, types, hooks, CI. Free at runtime, fails loudly.
3. Procedure: CLAUDE.md, REVIEW.md. Costs instruction budget, needs interpretation.
4. Training: correcting the agent in chat. The thing we are escaping.

Demo (one correction climbing):
- Agent makes a real convention mistake. Correct it in chat one last time, on camera: "That is tier 4, and this is the last time I ever do it."
- The encode move, and say this exactly: "I am not going to write the rule. Boris says Claude writes the lint rule. Watch." One prompt: encode this correction so it never recurs, CLAUDE.md line with the why, plus a lint rule that enforces it.
- Kill the session. Fresh session, zero context, similar task: correct first try. Then hand-type a violation: lint fires instantly.
- The deletion shot: "But watch the top tier." Apply the architectural fix (make the right path the laziest path: typed client, folded step, tighter types, whatever the repo offers). Then DELETE the CLAUDE.md rule on camera. "The healthiest thing my context layer ever did was shrink. The mistake is not banned anymore. It is impossible."

- Decision rule, verbatim: "First time, just correct it. If it recurs, encode it cheap and make Claude write the rule. If it KEEPS recurring, stop writing rules. The recurrence is telling you your codebase has a footgun, not that your agent is dumb."
- Instruction-budget beat (important, squares with what I teach in the school): "Encoding does not mean appending to CLAUDE.md forever. Prose is the staging area. Hard enforcement is the destination. A 2,000 line CLAUDE.md is just a wiki, and wikis rot."
- Role line: you stopped being the fix and became the encoder.

> 🎨 DRAW `second-codebase-correction-pyramid`: a four-tier pyramid, chat corrections at the bottom, procedures above, guards above that, eliminate at the top, a single correction climbing tier by tier and dissolving at the peak

![[second-codebase-correction-pyramid-1.png]]
![[second-codebase-correction-pyramid-2.png]]
![[second-codebase-correction-pyramid-3.png]]
![[second-codebase-correction-pyramid-4.png]]
![[second-codebase-correction-pyramid-5.png]]

---

## Move 3: Fix the Automation, Not the PR (9:30-12:00)

*The mindset flip. Boris's sharpest line made physical.*

Quote on screen: "If I put up a PR for an iOS codebase I don't know and a code reviewer rejects it because it doesn't use the right framework... these are failures of automation."

Demo:
- Agent produces work that violates a convention. The instinct everyone has: fix the output.
- Instead, on camera: ignore the output entirely. Encode the convention. Delete the branch. Re-run the ORIGINAL prompt from scratch.
- The new result passes untouched. "I never fixed the PR. I fixed the system, and the PR fixed itself."

- This is the same instinct as point fixes versus architectural fixes, applied to your agent infrastructure instead of your code.
- Do this today: next time an agent gets something wrong, do not touch its output. Ask what file was missing, write it, re-run.
- Role line: your unit of work is no longer the output. It is the system that produces outputs.

---

## Move 4: Give Your Repo a REVIEW.md (12:00-15:30)

*The money shot of the whole video lives here. Slow down for it.*

Quote on screen: "so that code review catches issues automatically."

What a REVIEW.md is (60 seconds, voiced as the viewer's own objection):
- "Why not just write lint rules for everything? Because lint reads syntax. It cannot read intent."
- Three nets: lint catches violations of FORM. A human catches violations of TASTE. And there is a brand new layer in the middle: an AI reviewer reading your principles catches violations of MEANING. That layer did not exist two years ago.
- CLAUDE.md shapes writing code. REVIEW.md shapes judging it. Every rule carries a why, because the why is what lets a reasoning reviewer generalize.

Demo (the generalization proof):
- Write ONE principle into REVIEW.md on camera. No file names, no endpoints, just the principle and its why.
- Produce code that violates the principle in a way never corrected before: different file, different endpoint, novel shape.
- Run lint: green. "Every tool from the last 30 years just approved this code."
- Run the AI review pass: it flags the violation, cites the principle, names the right approach.
- Stake the claim: "I never corrected this mistake. It is not in my history, not in CLAUDE.md, no lint rule knows it exists. The principle generalized to a case I never anticipated. This is why the system compounds instead of just accumulating."

- Do this today: write five principles with whys. The ones you would check for in any PR.
- Role line: the system now catches what you used to catch.

> 🎨 DRAW `second-codebase-three-nets`: three safety nets stacked under a trapeze, labeled form, meaning, taste, a falling bug passing through the first net and caught by the glowing new middle net

![[second-codebase-three-nets-1.png]]
![[second-codebase-three-nets-2.png]]
![[second-codebase-three-nets-3.png]]
![[second-codebase-three-nets-4.png]]
![[second-codebase-three-nets-5.png]]

---

## Move 5: Enforce at Machine Speed with Hooks (15:30-17:00)

*Compressed on purpose: the school teaches hooks in depth. Demo plus funnel.*

Quote on screen: "as the harness matures, this task becomes easier."

Demo:
- The same rule from Move 2, now as a PreToolUse hook. Agent attempts a violating edit: blocked mid-keystroke, message returned, agent reads it and self-corrects. No human, no review cycle, milliseconds.
- "Move 2 was a session round trip. This is 200 milliseconds. Same rule, moved to machine speed."

- Practical order: PostToolUse lint and typecheck after every edit first, PreToolUse guards for forbidden patterns second, a Stop hook that runs tests before the agent may say done.
- Funnel (soft): "I have full videos on hooks inside Agentic Coding School, link below. Here I just need you to see the tier."
- Role line: enforcement no longer waits for you to be awake.

---

## Move 6: Build the Interview Loop (17:00-20:30)

*The climax. The direction of correction reverses on camera. Do not script the answer moment, the genuine realization is the shot.*

Quote on screen: "What gets in the way... is domain knowledge that lives in peoples' heads rather than in automation."

- Setup line: "Everything so far is reactive. A mistake happens, we encode it. But the knowledge in my head that no mistake has surfaced yet? Nothing in the essay reaches it. So I built the thing that does."

Demo:
- A skill that mines the week's git diffs and correction history, finds what looks like undocumented decisions, and interrogates me one question at a time.
- It asks something sharp and real. Answer it honestly on camera. The realization: that answer existed nowhere but my head.
- It writes the encoding itself (comment or CLAUDE.md entry) from the answer and shows the diff.
- Landing line: "Look at the direction of what just happened. For two years I reviewed the machine's work. It is now reviewing mine. And honestly? It is better at finding my gaps than I am."

- Do this today: even without the skill, end each week asking an agent to list the five least documented decisions in the last 20 commits, and answer them into files.
- Role line: you are not the reviewer anymore. You are the reviewed.

> 🎨 DRAW `second-codebase-interview-reversal`: an interview scene where the roles flipped, the AI holding the clipboard asking questions, the engineer in the interview chair, a big direction arrow reversed

![[second-codebase-interview-reversal-1.png]]
![[second-codebase-interview-reversal-2.png]]
![[second-codebase-interview-reversal-3.png]]
![[second-codebase-interview-reversal-4.png]]
![[second-codebase-interview-reversal-5.png]]

---

## The Reveal: The Second Codebase (20:30-22:30)

*The table appears row by row. This is the thesis landing.*

- "Look at what you just built. Six moves, and every single one is a software engineering practice you already know, applied to something that was never treated as software before: what you know."
- Comments were documentation. Corrections became commits. Move 3 was fixing root cause. REVIEW.md is a test suite for meaning. Hooks are CI. The interview loop is the retro.
- The thesis, verbatim: "You already maintain one codebase, the one that runs your product. As of now you have two. The second one programs your agents, your reviews, and everyone who ever touches the first one."
- A codebase is not maintained by willpower. It is maintained by cadence. The calendar:
  - Daily, automatic: harvest corrections, encode them.
  - Weekly, 15 minutes: the prune pass. Which rules fired, which were violated anyway, which reference files that no longer exist. Review the proposed diff, not the file.
  - Weekly, 15 minutes: the interview.
  - Monthly: the audit. Fresh agent, zero context, real task. Every stumble is a gap.
- The scoreboard, verbatim: "One number tells you if this is working. What fraction of this week's corrections have you made before? If it is not falling, your system is leaking. Mine is falling. That is the whole game."

> 🎨 DRAW `second-codebase-two-codebases`: two codebases side by side as twin buildings, the product codebase and the knowledge codebase, pipes flowing between them, tiny agents reading from the second while building the first

![[second-codebase-two-codebases-1.png]]
![[second-codebase-two-codebases-2.png]]
![[second-codebase-two-codebases-3.png]]
![[second-codebase-two-codebases-4.png]]
![[second-codebase-two-codebases-5.png]]

> 🎨 DRAW `second-codebase-maintenance-calendar`: a weekly calendar with recurring maintenance loops marked, daily harvest, weekly prune, weekly interview, monthly zero-context audit, small gears on each entry

![[second-codebase-maintenance-calendar-1.png]]
![[second-codebase-maintenance-calendar-2.png]]
![[second-codebase-maintenance-calendar-3.png]]
![[second-codebase-maintenance-calendar-4.png]]
![[second-codebase-maintenance-calendar-5.png]]

---

## CTA (22:30-23:00)

Single CTA per improvements doc:

- "If you want the deep versions of everything I compressed today: the full context layer system, hooks, the maintenance flywheel, and the loop mechanics, that is what Agentic Coding School is. Two thousand engineers are in there. Link below."

---

## Pre-Production Checklist

- [ ] Choose the school platform codebase as the demo repo (decided in planning)
- [ ] Scout Move 2's mistake: run the target task 3 or 4 times in fresh sessions, pick the convention with the highest miss rate. If stock Claude gets it right, the demo collapses
- [ ] Pick the Move 1 weird-code site and verify the no-comment run actually breaks the behavior
- [ ] Verify Move 4's violation is genuinely novel: check correction history and CLAUDE.md contain nothing about it
- [ ] BUILD the interview-loop skill before filming (mines git diffs + corrections, one question at a time, auto-encodes answers). Building it is itself a clip, and it becomes an ACS class video after
- [ ] Identify the Move 2 architectural fix in advance so the deletion shot is real
- [ ] Confirm the Boris essay source link and exact quote text for on-screen highlights

## Spawned ACS Class Videos (build once, use twice)

1. The interview loop (Loopy AI or Context Engineering): the climax demo becomes the class deep-dive
2. REVIEW.md authoring plus the form, meaning, taste layer model: fills the catalog gap between review tools and the context layer
3. The strip test plus repeat-correction-rate metric: the measurable diagnostic the Maintenance video asserts but never demos
4. Load-bearing comments (cheap short)

## Banked for Follow-Up Videos

Strip test (delete your context layer and watch agents get dumber), token receipt (what a repeated correction costs), day-one OSS contribution, non-engineer ships to production, the literal loop against an e2e suite, memory demo, routines demo.
