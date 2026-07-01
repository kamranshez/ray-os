---
title: "Building Great Agent Skills: The Missing Manual"
video_url: https://www.youtube.com/watch?v=UNzCG3lw6O0
video_id: UNzCG3lw6O0
channel: AI Engineer
published: 2026-06-29
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Building Great Agent Skills: The Missing Manual**](https://www.youtube.com/watch?v=UNzCG3lw6O0) - AI Engineer - uploaded 2026-06-29

> 2 net-new ACS videos available, plus 1 next-step complement (Matt Pocock's skill-quality checklist)

## The ideas worth a video

- **Leading words** — steer an agent by embedding dense, prior-laden terms (like "vertical slice") it echoes back in its reasoning traces, changing behavior. This is the reframe most of the "steering" material hangs off. VERDICT: 🔗 next-step video available.
- **Increase leg work by hiding the future step** — splitting one skill into separate skills so the agent sees only the current step forces it to fully invest, because a visible goal makes it rush the early phase. VERDICT: ❌ net-new video available.
- **The deletion test / pruning** — great skills stay small by cutting no-ops (delete a paragraph; if behavior is unchanged it did nothing), removing sediment, and enforcing a single source of truth. VERDICT: ❌ net-new video available.

## Summary + counts

Matt Pocock, recorded for the AI Engineer World's Fair, presents a practical four-part checklist for writing great agent skills: trigger, structure, steering, and disciplined pruning.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Leading words

**The claim.** You steer an agent far more effectively by embedding a "leading word," a dense, prior-laden term the model already understands, than by writing longer explicit instructions.

**Why it's non-obvious.** The instinct when an agent ignores you is to add words: "don't code layer by layer, build a small slice first, get feedback early." Matt argues the fix is the opposite: fewer, denser words. A leading word like "vertical slice" carries more steering force than a paragraph, because it triggers a prior the model already holds.

**Why it's true / the mechanism.** A leading word maps to an established concept ("vertical slice" is known development terminology), so it activates the model's prior. The agent then repeats the phrase in its thinking tokens and output, and because it keeps re-emphasizing the exact word that encodes the behavior you want, its downstream actions bend to match. Dense term, then echoed in traces, then re-emphasis, therefore changed behavior. As Matt puts it, "English is a pretty wide API."

**What it generalizes to.** Any domain with settled jargon: "idempotent" for infra scripts, "smoke test" for QA gates, "load-bearing" for refactors.

**How it goes wrong.** The term must map to a real, widely-held prior; invented jargon does nothing. It needs consistent repetition, and you must verify by reading the reasoning traces for adoption rather than assuming it worked.

### Spine 2 — Increase leg work by hiding the future step

**The claim.** Splitting one skill into separate skills, so the agent can see only the step it is currently on, forces it to do more leg work on that step.

**Why it's non-obvious.** The default is to write one skill listing every step in order. But a visible finish line is exactly what makes the agent shortchange the early phases.

**Why it's true / the mechanism.** When an agent can see its ultimate goal, it treats the earlier phase as a formality and races to the payoff. Matt's example is plan mode: "It sees that its ultimate goal is to create a plan. And so it just does a small amount of leg work" on asking clarifying questions. His fix is to split planning into two skills, grill-with-docs then two-PRD, so the agent, seeing only "ask clarifying questions," invests fully because that phase IS its entire job. Remove the visible goal, and the rationing behavior disappears.

**What it generalizes to.** Any multi-step process where an early phase gets skimped: research before drafting, exploration before refactoring, reproduction before bug-fixing.

**How it goes wrong.** Not always worth it; many tiny skills add their own overhead and raise the pilot's cognitive load. Use it only where one step genuinely demands an extra chunk of effort.

### Spine 3 — The deletion test and pruning

**The claim.** Great skills stay small through ruthless pruning: enforce a single source of truth, remove "sediment," and delete "no-ops" using a simple deletion test.

**Why it's non-obvious.** People equate more instructions with more control, so they keep adding. But much of a skill's text never changes behavior at all, and a massive skill is usually a symptom of a failure mode, not thoroughness.

**Why it's true / the mechanism.** The deletion test is: remove a paragraph and ask what the agent would do without it. If an "always write a long, detailed commit message" paragraph is deleted and the agent still writes a good commit message, that paragraph was a no-op, costing tokens and maintenance without changing anything. Sediment accumulates when contributors add to shared docs but never delete anyone else's material; a single source of truth stops duplicated reference from drifting apart. Fewer words means fewer tokens per request and an easier audit.

**What it generalizes to.** Any LLM instruction artifact: prompt files, CLAUDE.md, system prompts. The deletion test is a general tool for cutting instruction bloat.

**How it goes wrong.** Aggressive deletion can strip load-bearing constraints that only matter in a rare branch. Test across branches, not just one happy path, before cutting.

---

## 🎬 Proposed ACS videos

### 1. Leading Words: The One Phrase That Makes Agents Obey

- **HOOK:** You keep adding instructions and the agent still ignores you; the real fix is fewer, denser words.
- **THE PROMISE:** For anyone writing skills or prompts. After this you can steer an agent with a single prior-laden phrase and confirm it worked by reading the reasoning traces.
- **THE SHAPE:**
  1. Show the failure: a verbose "don't code layer by layer, build a small slice first" instruction that the agent ignores.
  2. Introduce "vertical slice" as a leading word; rewrite the skill around that one phrase, repeated consistently.
  3. Run it, open the reasoning traces, watch the agent echo "we'll do this as a thin vertical slice," then produce a better plan.
  4. Show how to hunt for leading words (ask the agent to suggest them; "English is a wide API").
- **SPINE:** Leading words.
- **SLOT:** Prompt Engineering → Aligning to Your Intent (next to "Customized Terminology for Better Prompts").
- **RELATIONSHIP:** 🔗 complements "Customized Terminology for Better Prompts", which teaches adopting the codebase's own vocabulary so your prompts are precise. This adds the reverse move: deliberately choosing dense, prior-triggering terms the agent repeats in its traces to change its behavior, and using the traces as a feedback signal. Don't re-teach glossary-building; teach the steering mechanism.
- **PROOF TO REUSE:** the "vertical slice" vs "don't code layer by layer" contrast; "English is a pretty wide API"; watching the reasoning traces adopt the phrase.

### 2. Hide the Finish Line: Split Skills So Agents Actually Do the Work

- **HOOK:** Your agent races through clarifying questions to reach the plan; hide the plan and it suddenly slows down and digs in.
- **THE PROMISE:** For skill authors. After this you can force an agent to fully invest in a neglected early step by splitting it into its own skill that hides the next phase.
- **THE SHAPE:**
  1. Show plan mode: "ask clarifying questions" does almost no leg work, then eagerly jumps to the plan.
  2. Diagnose the cause: a visible ultimate goal makes the agent ration effort on the current step.
  3. Split into two skills, grill-with-docs then two-PRD, so the agent sees only one step at a time.
  4. Re-run: the clarifying phase now does real leg work because it IS the whole job.
- **SPINE:** Increase leg work by hiding the future step.
- **SLOT:** Advanced Techniques → Skills as Force Multipliers (alt: Prompt Engineering).
- **RELATIONSHIP:** ❌ net-new. ACS's Skills chapter covers forked contexts, arguments, specifying models/agents, and combining skills with subagents, but nothing teaches splitting a skill to INCREASE leg work by hiding the goal from the agent.
- **PROOF TO REUSE:** plan mode always under-invests in clarifying questions; the grill-with-docs split; "this is a really cool technique for increasing leg work on the step that you're on by hiding the future goal."

### 3. The Deletion Test: How to Cut a Skill in Half Without Losing Behavior

- **HOOK:** Half of your skill probably does nothing. Here is the one test that proves which half.
- **THE PROMISE:** For anyone maintaining skills or CLAUDE.md files. After this you can shrink a bloated skill, cutting tokens and maintenance cost, without changing what the agent does.
- **THE SHAPE:**
  1. Open a bloated skill; name the three causes of size: duplication, sediment, and no-ops.
  2. Apply the deletion test: remove the "write a long, detailed commit message" paragraph, re-run, show behavior is unchanged.
  3. Fix sediment by sorting material by branch and moving branch-only reference behind context pointers; enforce one source of truth.
  4. Show the before/after token count and a smaller, auditable skill.
- **SPINE:** The deletion test and pruning.
- **SLOT:** Advanced Techniques → Skills as Force Multipliers (alt: Master Claude Code → Skills).
- **RELATIONSHIP:** ❌ net-new. "Tackling Redundant Code" covers stripping redundant application code against a reference implementation, not pruning skill or prompt files with a deletion test for no-ops and sediment.
- **PROOF TO REUSE:** the commit-message no-op example; "massive skills are usually a kind of symptom of something else going wrong"; the concepts of sediment and single source of truth.

**Also film-able (not deep-dived):**
- **Context load vs cognitive load: the user-invoked vs model-invoked decision** — 🔗/🟡 next step on "Disable Model Invoked Skills" (which teaches the disable-model-invocation mechanic and reducing skill clutter). Adds the symmetric decision framework: model-invoked spends context tokens plus unpredictability plus an eval burden; user-invoked spends the pilot's attention. One-line pitch: a framework for deciding, per skill, which invocation style to use, and why "model-invoked is more flexible" is a trap. Slot: Master Claude Code → Skills.
- **Steps + reference structure and a minimal skill.md via context pointers** — largely ✅ covered by "Progressive Disclosure" (Context Engineering) plus the existing Skills chapter, so not pitched standalone.

---

## 📚 Full wisdom (reference)

**SUMMARY.** Matt Pocock, recorded for the AI Engineer World's Fair, presents a practical four-part checklist for writing great agent skills: trigger, structure, steering, and disciplined pruning.

**IDEAS**
- Skill hell is having many downloadable skills but no rubric to tell good ones from bad.
- A skill checklist covers four things: trigger, internal structure, steering the agent, and pruning for size.
- User invoked skills you trigger manually; model invoked skills the agent chooses via their own description.
- A skill description is a context pointer sitting in context, pointing to the fuller skill.md file.
- Every model invoked skill adds a description costing tokens on every request plus constant decision overhead.
- More user invoked skills raise the pilot's cognitive load: more things the human must actively remember.
- Model invocation costs unpredictability: the agent may simply choose not to follow an otherwise perfect pointer.
- Skills decompose into two units: steps, the actual procedure, and reference, the supporting material behind them.
- Keep the skill.md file small: every shaved word becomes a token saved on every single request.
- Reference material used in only one branch is a candidate to move out of the skill.md.
- Hide branching reference behind context pointers to external files bundled alongside the skill for easy retrieval.
- Leading words pack dense meaning into short phrases that trigger the model's existing priors quite reliably.
- Agents echo leading words in reasoning traces, re-emphasizing them, which then reshapes their actual output behavior.
- Saying vertical slice beats saying don't code layer by layer; it triggers a known developer prior.
- Agents shortchange the current step when they can see the ultimate goal waiting just beyond it.
- Splitting a skill so the agent sees one step increases the leg work done per step.
- Plan mode always under-invests in asking clarifying questions, then races eagerly toward creating the final plan.
- The deletion test: remove a paragraph and check whether the agent's behavior actually changes at all.
- No-ops are skill instructions that look meaningful but never actually change the agent's behavior in context.
- Sediment accumulates when contributors keep adding to shared docs but never delete anyone else's stale material.

**INSIGHTS**
- Neither invocation style is free: model invocation spends context tokens, user invocation spends the pilot's attention.
- Flexibility has a hidden price: making everything model invokable trades predictability for the appearance of convenience.
- Small skills win twice: cheaper on every request and far easier for humans to audit later.
- Steering agents well is less about longer instructions and more about denser, prior-triggering word choices instead.
- Reasoning traces are a debugging surface: watch whether your leading word is actually being adopted there.
- Visibility of a goal changes effort: agents ration work toward whatever endpoint they can already see.
- Structure is the first cure for bloat: sort material by branch before deleting anything else outright.
- A single source of truth prevents reference material from silently drifting apart across many duplicated locations.
- Evaluation burden is itself a design cost: unpredictable invocation forces you to eval trigger reliability constantly.

**QUOTES**
- "Just one more skill, bro. That's kind of seems like what we're saying." — Matt Pocock
- "We don't know what makes a skill great." — Matt Pocock
- "This description serves as a kind of context pointer." — Matt Pocock
- "Every time you have a model invoked skill, it basically you get a cost in unpredictability." — Matt Pocock
- "We want to make the main skill.md file as small as possible." — Matt Pocock
- "Hide branching reference material behind context pointers." — Matt Pocock
- "English is a pretty wide API in terms of different functions you can call." — Matt Pocock
- "You'll notice in the reasoning traces that it's saying, 'Okay, we're going to do this as a thin vertical slice.'" — Matt Pocock
- "It sees that its ultimate goal is to create a plan. And so it just does a small amount of leg work." — Matt Pocock
- "This is a really cool technique for increasing leg work on the step that you're on by hiding the future goal." — Matt Pocock
- "What would happen if you just deleted that paragraph?" — Matt Pocock
- "Massive skills are usually a kind of symptom of something else going wrong." — Matt Pocock

**HABITS**
- Matt prefers user invoked skills to keep full control and minimize context load on his agents.
- He always inserts a human-in-the-loop checkpoint to confirm test seams before writing the requirements document itself.
- He deliberately splits planning into a separate grill-with-docs skill so the clarifying questions get full effort.
- He runs deletion tests on every skill, cutting any paragraph that leaves behavior unchanged right afterward.
- He reuses consistent leading words throughout a skill rather than scattering varied phrasings for one concept.
- He watches reasoning traces to confirm the agent adopted his intended leading word before trusting it.
- He keeps every piece of reference material in exactly one place as one source of truth.
- He asks the agent itself to help brainstorm candidate leading words when his steering falls short.

**FACTS**
- Matt Pocock's skills repo is currently one of the most popular engineering skill sets publicly available.
- Superpowers is another extremely popular engineering skill set, built almost entirely around model invoked skills throughout.
- Matt's grill-me skill sets disable model invocation true, so its description shows only to the user.
- His two-PRD skill has three steps and two reference pieces: test seams and a markdown template.
- His domain modeling skill has two or three branches: glossary updates and architectural decision records too.
- Developers previously endured tutorial hell and framework hell long before today's newer skill hell finally arrived.
- The writing great skills skill lives in Matt's public skills repo under productivity, hosted on GitHub.
- Matt publishes a newsletter at aihero.dev and plans to release an upcoming AI coding crash course.

**REFERENCES**
- Matt Pocock's skills repo (github.com/mattpocock/skills)
- The "writing great skills" SKILL.md (github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- Superpowers skill set
- grill-me / grill-with-docs skill
- two-PRD skill
- domain modeling skill
- codebase design skill
- implement skill
- plan mode
- aihero.dev newsletter
- AI Engineer World's Fair
- Upcoming "AI coding crash course"

**ONE-SENTENCE TAKEAWAY.** Great skills fire predictably, stay minimal, steer with leading words, and ruthlessly prune their no-ops.

**RECOMMENDATIONS**
- Decide deliberately whether each skill should be user invoked or model invoked before you publish it.
- Set disable model invocation on skills you want to keep out of the agent's automatic context.
- Separate every skill explicitly into steps and reference before writing any of its actual content down.
- Move branch-specific reference material out of skill.md and behind a context pointer to bundled external files.
- Replace verbose behavioral instructions with a single consistent leading word, repeated deliberately throughout the whole skill.
- Read the reasoning traces to verify your leading word is being echoed and actually working now.
- Split a step into its own skill when the agent rushes it toward a visible goal.
- Run the deletion test on every suspicious paragraph and cut anything that leaves the behavior unchanged.
- Audit community authored skills with the checklist before trusting them inside your own agentic workflows.
