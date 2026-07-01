---
title: "The rise of the professional vibe coder (a new AI-era job)"
video_url: https://www.youtube.com/watch?v=0XNkUdzxiZI
video_id: 0XNkUdzxiZI
channel: Lenny's Podcast
published: 2026-02-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**The rise of the professional vibe coder (a new AI-era job)**](https://www.youtube.com/watch?v=0XNkUdzxiZI) - Lenny's Podcast - uploaded 2026-02-08

> Two next-step ACS videos available (both complements); the layered PRD/context-file system is already covered by the school.

## The one idea worth a video

- **Spine A: The dynamic context-window file system.** Treat the agent as an engineer with amnesia and feed it layered docs (master plan, implementation plan, design guidelines, user journeys) that compile into one tasks.md, so its scarce tokens go to execution not re-reading. VERDICT: ✅ already covered (kept for the deep dive, not pitched).
- **Spine B: Parallel prototyping as a clarity tool.** At kickoff, launch four or five full builds from different input modalities and compare them to discover what you actually want. VERDICT: 🔗 next-step video available.
- **Spine C: The self-improving rules loop.** After a hard debug, ask the agent how you could have prompted it better, then write that lesson into rules.md so it prompts itself next time. VERDICT: 🔗 next-step video available.

## Summary + counts

Lenny interviews Lazar Jovanovic, Lovable's first professional vibe coder, on the workflows, context-file systems, parallel prototyping, and debugging habits that ship production products without coding.

🔴 0 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine A — The dynamic context-window file system (✅ covered)

**The claim:** Because the context window is finite, externalize project state into a layered set of documents (master plan, implementation plan, design guidelines, user journeys) that funnel into a single tasks.md, and configure a rules file so the agent reads them, executes the next task, and reports how to test, keeping tokens on execution rather than rediscovery.

**Why it is non-obvious:** Most people prompt conversationally and let the agent rediscover the project every turn. By message thirty the early context is lost, so a bug report like "this broke" forces the agent to reread everything.

**Why it is true:** The agent optimizes for speed and will not reread the full history, so unreferenced state silently drops. In Lazar's 60-function project, an unreferenced failure makes the tool "consume 80% of the token allocation on reading to get clarity, leaving only the final 20% for thinking and executing." Externalizing state into files the rules always load starts each turn from a compact, authoritative source, so the budget goes to the actual work.

**What it generalizes to:** Claude Code with CLAUDE.md and AGENTS.md plus plan files, and any long-lived production codebase where re-orientation cost dominates.

**How it goes wrong:** Stale docs poison context, over-documenting a tiny project adds pure overhead, and the files must be refreshed dynamically or they drift from the real state.

### Spine B — Parallel prototyping as a clarity tool (🔗 complement)

**The claim:** At the start of a project, kick off four or five full builds in parallel from different inputs (a voice brain-dump, a typed prompt, a screenshot reference from Mobbin or Dribbble, a pasted code snippet from 21st.dev) and compare them to find out what you actually want.

**Why it is non-obvious:** Engineers treat starting over as waste and try to steer one build to correctness. Lazar treats parallel starts as the cheapest way to manufacture clarity, and argues it saves credits by avoiding an endless patch cycle on a wrong first direction.

**Why it is true:** Clarity is the bottleneck, not build speed. Seeing several concrete realizations side by side surfaces "no, not that" faster than any amount of upfront thinking, because judgment is easier than specification. Each variant also exposes you to quality, sharpening taste as you choose. Once the winner is obvious, you commit with certainty, so downstream tokens are not spent reversing architecture and design.

**What it generalizes to:** Claude Code worktrees or several Codex tasks running the same brief, and design-variation generation for one component.

**How it goes wrong:** Parallel exploration only pays during the ambiguous phase; after direction is set it is noise. Comparing well requires taste, or you pick the shiniest rather than the best.

### Spine C — The self-improving rules loop (🔗 complement)

**The claim:** After any hard debug, do not just move on. Ask the agent how you could have prompted it better in one go, then write that lesson into rules.md so the agent effectively prompts itself next time.

**Why it is non-obvious:** Most people fix the bug and forget, then repeat the same class of failure, and they blame the model when the real gap was missing context. Lazar closes the loop by converting each fix into a permanent, self-authored guardrail.

**Why it is true:** His 4x4 ladder (let it self-fix, add console-log awareness, escalate to Codex for diagnosis, revert and rethink) resolves the immediate bug, but the durable win is the fifth step. Because you will not remember to prompt better in two days, you delegate that memory to the agent by recording the lesson where it reads every run: "you're just going to learn that I'm stupid and you're going to prompt yourself better." Over time the standing rules absorb your prompting knowledge and recurrence drops.

**What it generalizes to:** Claude Code CLAUDE.md and Codex AGENTS.md, and rule or skill files in any agent harness.

**How it goes wrong:** Accumulating rules bloats context and can conflict, and the agent's self-diagnosis is a hypothesis, not truth, so unverified rules can encode superstition.

## 🎬 Proposed ACS videos

### 1. Build It Five Ways: Parallel Prototypes as a Thinking Tool

- **HOOK:** You do not have a prompting problem, you have a clarity problem, and parallelism solves it.
- **THE PROMISE:** For builders who freeze at a blank prompt, kick off several agents at once and let the comparison tell you what to build.
- **THE SHAPE:**
  1. Launch the same brief four ways: voice brain-dump, typed spec, screenshot reference, pasted code snippet.
  2. Run them in parallel worktrees or Codex tasks so you wait on none of them.
  3. Compare the concrete outputs side by side and let "not that" sharpen the target.
  4. Promote the winner into your planning docs and discard the rest.
  5. Show the credit and time math: choosing early beats patching a wrong direction forever.
- **SPINE:** B (parallel prototyping for clarity).
- **SLOT:** My Daily Workflows, or Advanced Techniques > Multi-Agent Orchestration.
- **RELATIONSHIP:** 🔗 complements "Designing Components" (My Daily Workflows), which generates numbered variations of ONE component to pick a design when it is hard to describe. This is the next step: scale that clarity-through-parallelism to a whole project kickoff across multiple input modalities. Do not re-teach component-level variation picking.
- **PROOF TO REUSE:** Lazar's four-input parallel start; "I never built just one project at a time. I built five or six. I have six lovable tabs and I just switch between them"; his claim that upfront parallelism saves "hundreds of credits and maybe even hundreds of dollars."

### 2. Teach the Agent to Prompt Itself: Turn Every Bug Into a Rule

- **HOOK:** The last step of debugging is not the fix, it is making the agent never need you for that fix again.
- **THE PROMISE:** For anyone who keeps hitting the same class of bug, convert each hard fix into a self-authored rule so the agent stops repeating it.
- **THE SHAPE:**
  1. Work the 4x4 ladder: self-fix, console-log awareness, escalate to Codex for diagnosis, revert and rethink.
  2. Once fixed, ask the agent how you could have prompted it to solve it in one go.
  3. Have the agent write that lesson as a rule into CLAUDE.md or AGENTS.md.
  4. Prove recurrence drops on the next similar bug.
  5. Cover guardrails: verify the rule, prune conflicts, avoid encoding superstition.
- **SPINE:** C (self-improving rules loop).
- **SLOT:** Techniques > Debugging & Verifying Output, or Prompt Engineering.
- **RELATIONSHIP:** 🔗 complements "Agent Introspection" (Techniques), which diagnoses what misled an agent and treats reflections as hypotheses. This is the next step: operationalize that reflection into a committed, self-written standing rule as a repeatable ritual. It also complements "CLAUDE.md Best Practices" (add rules only after repeated mistakes). Do not re-teach introspection basics.
- **PROOF TO REUSE:** The 4x4 framework verbatim; "put this what we just learned into rules.mmd"; "you're just going to learn that I'm stupid and you're going to prompt yourself better"; the Codex-for-diagnosis-only habit and the repomix pack-and-consult fallback.

## 📚 Full wisdom (reference)

**SUMMARY:** Lenny interviews Lazar Jovanovic, Lovable's first professional vibe coder, on the workflows, context-file systems, parallel prototyping, and debugging habits that ship production products without coding.

**IDEAS**
- A non-technical background helps because you never learned which things are supposedly impossible to even build.
- He spends eighty percent of his time planning and chatting, only twenty percent executing the plan.
- The genie grants only three wishes at a time, mirroring the token limit per single request.
- Ask to be taller and you become thirteen feet tall: vague wishes produce dysfunctional literal outputs.
- Start four or five parallel builds from voice, text, screenshots, and code, then pick the winner.
- English is the top programming language, yet these tools still interpret pasted code snippets most precisely.
- Parallel prototyping up front actually saves hundreds of credits and days versus fixing one build forever.
- He first writes four separate PRDs: a master plan, implementation plan, design guidelines, and user journeys.
- Everything funnels into a single tasks.md; once that exists, the other planning documents become almost irrelevant.
- Rules.md tells the agent to read every file, execute the next task, then report testing steps.
- After setup his prompts shrink to just proceed with the next task, outsourcing context to documents.
- Agents lie agreeably, often claiming a bug is already fixed just to keep you feeling happy.
- Yelling at the agent wastes tokens because it spends them apologizing instead of actually fixing problems.
- His 4x4 debug framework says try each of the four fixes exactly once before moving onward.
- When stuck he opens the console log, feeds it back, and that awareness alone fixes most.
- For gnarly bugs he exports to GitHub and consults Codex purely for diagnosis, never for edits.
- After solving, he asks how to prompt better next time, then writes that lesson into rules.md.

**INSIGHTS**
- Coding is not the real problem; clarity is, because AI output already far outpaces human output.
- The ceiling on AI is not model intelligence but rather what the model sees before acting.
- Good enough is now universal, so the only durable edge left is producing world-class, magical work.
- Reward is shifting from faster raw output toward better judgment, taste, and clear decisions about direction.
- Treat the tool as an engineer needing perpetual, dynamically refreshed context rather than assuming infinite memory.
- Debugging failures are almost always your own fault: a bad prompt, missing reference, or wrong context.
- The roles of engineer, designer, and product manager are converging into one AI-amplified builder identity now.
- Elite engineering grows more valuable: someone must maintain, scale, and rebuild the infrastructure everyone depends on.
- AI amplifies whatever ability exists: without knowing what you are doing, you just produce garbage faster.
- Taste is built through exposure time: deliberately consuming world-class design, copy, and product experiences every day.

**QUOTES**
- "Coding is going to be like calligraphy... it's going to be so rare that it's going to become an art." (Lazar)
- "AI regardless of your background is an amplifier. If you don't know what you're doing, you're just going to produce garbage faster." (Lazar)
- "I spent 80% of my time in planning and chatting and only 20% in executing the plan actually." (Lazar)
- "I don't care about the code. Like the syntax is not of my interest. It's what the agent tells me that matters to me." (Lazar)
- "The ceiling on the AI isn't the model intelligence. It's what the model sees before it acts." (Lazar, quoting an author)
- "We solved for the how... Now we got to solve for everything else. And everything else is what matters." (Lazar)
- "Demo don't memo." (Lazar, on Lovable's 2025 motto)
- "It's your fault, my friend. You did not provide any clarity or context to this tool." (Lazar)
- "You don't need a company to hire you. You can hire yourself as a professional vibe coder first." (Lazar)
- "We're all becoming product managers on steroids." (Lazar)

**HABITS**
- He keeps around six Lovable tabs open, switching between parallel projects while agents run long tasks.
- He will spend an entire day planning and documenting before writing a single line of implementation.
- He religiously reads the agent output every session and deliberately ignores the underlying generated code entirely.
- He dictates a raw brain-dump prompt using voice input, then sends before it even finishes recording.
- He pulls reference screenshots from Mobbin and Dribbble to show the tools exactly what quality means.
- He pastes code snippets from 21st.dev to get pixel-perfect design instead of merely describing it verbally.
- When frustrated he steps back, takes a walk, drinks coffee, then retries the request with clarity.
- He uses chat mode itself to help draft a clearer prompt whenever he gets truly stuck.

**FACTS**
- Lazar is Lovable's first official vibe coding engineer, holding that exact job title at the company.
- Lovable's merch store, including the very shirt sold online, was entirely vibe coded by Lazar himself.
- He claims that at least half of all S&P 500 companies have employees using Lovable somehow.
- He started vibe coding back in July 2024, before Karpathy coined the term in early 2025.
- Historically ninety percent of the US horse population disappeared within roughly twenty years of engine cars.
- Lazar is a forestry engineer by formal training, having never once worked as a software engineer.
- A seemingly simple Figma gradient he admired was actually built from fifty layered colors and opacities.
- Cloudflare went down two or three times within the last two or three months, he noted.

**REFERENCES**
- Tools: Lovable, Lovable + Shopify, Cursor, Claude Code, OpenAI Codex, ChatGPT, Claude, Gemini, repomix, Whisper Flow.
- Design/reference sources: Mobbin, Dribbble, 21st.dev, Figma.
- Lazar's builds: Lovable base prompt generator, Lovable PRD generator (custom GPTs), a public "some UI style" Lovable app of 18 design styles.
- People: Elena Verna (Lovable head of growth), Anton (Lovable), Felix Haas (designplusai.com newsletter), Guillermo Rauch / v0, Michael Truell (Cursor CEO), Andrej Karpathy, Ben Tossell, Peter Thiel (referenced as "Peter Steel").
- Courses/media: Starter Story AI Build Accelerator course, Lazar's 50in50challenge YouTube channel, Lenny's Newsletter.

**ONE-SENTENCE TAKEAWAY:** Stop optimizing coding speed; invest in clarity, taste, and context so agents produce world-class work.

**RECOMMENDATIONS**
- Kick off four or five parallel prototypes before committing, then compare them all to find clarity.
- Write a master plan, implementation plan, design guidelines, and user journeys before generating your tasks file.
- Configure a rules file telling the agent to read everything, then execute one task at once.
- Paste code snippets, not just English, when you need pixel-perfect design results from any agentic tool.
- When stuck, add console logs, read them, and paste them back to give the agent awareness.
- Escalate stubborn bugs to Codex just for diagnosis, but keep code edits inside your primary tool.
- After every hard fix, ask the agent how to prompt better, then commit that lesson permanently.
- Set aside more time for learning and exposure than for building, developing taste and better judgment.
- Build in public, share every failure and secret, and you will attract opportunities and job offers.
