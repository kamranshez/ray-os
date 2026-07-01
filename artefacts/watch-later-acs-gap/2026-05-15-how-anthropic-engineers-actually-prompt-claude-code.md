---
title: How Anthropic Engineers ACTUALLY Prompt Claude Code
video_url: https://www.youtube.com/watch?v=qOvc9IUKEIc
video_id: qOvc9IUKEIc
channel: Austin Marchese
published: 2026-05-15
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**How Anthropic Engineers ACTUALLY Prompt Claude Code**](https://www.youtube.com/watch?v=qOvc9IUKEIc) - Austin Marchese - uploaded 2026-05-15

> net-new ACS video available (a deterministic-script skill technique), plus one next-step complement

## 1. The idea worth a video

**Spine 1 (❌ net-new): The leverage in a skill is its tools layer, so freeze the script your agent keeps regenerating into the skill folder and rerun deterministic code instead of paying tokens to guess.** This is the spine because it reframes Rule 2 (skills are more than prompts) and Pattern 1 (save scripts inside skills) into one buildable move, and it carries the video's strongest mechanism: code is deterministic and cheap, tokens are probabilistic and not. VERDICT: ❌ net-new video available.

**Spine 2 (🔗 complement): A skill persists where a prompt evaporates, so every run is a chance to permanently sharpen it by asking "one-time fix or forever?" and writing the forever-fixes back.** This is a spine by altitude: it is Rule 4's compounding loop stated as a repeatable habit with a concrete prompt, distinct from a one-off skill enrichment. VERDICT: 🔗 next-step video available.

*Considered but not promoted (already covered):* Rule 3 composability / chaining small skills (✅ covered by "Combining Skills & Subagents" and the whole Skills chapter); Pattern 2 invocation flags (✅ disable-model-invocation is covered by "Disable Model Invoked Skills"; only the user-invocable half is a minor 🟡, not spine-level); Rule 1 "prompt skills not Claude / the application layer" (✅ the premise of the entire Skills chapter). None of these clears the gate on its own.

## 2. Summary + counts

Austin Marchese distills four rules from Anthropic engineers' public talks: prompt skills not Claude, invest in tools, build composable skills, and compound them every session.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered *(tally is one per promoted spine; the covered ideas above were weighed in Stage 1 and not promoted)*

## 3. 🔬 Deep dive

**Spine 1 — Freeze the script into the skill's tools layer.**
The claim: the real leverage in a skill lives in its third layer, the tools, and the sharpest single move is to freeze a script your agent keeps regenerating into the skill folder, so future sessions rerun deterministic code instead of paying tokens to guess. Why it is non-obvious: most builders pour effort into the prompt (layer two) and then, as Eric notes, hand the model bare-bones tools with parameters named A and B. Why it is true: AI generation is probabilistic, so the same request costs tokens and can vary run to run, while code is deterministic, so identical input yields identical output at near-zero cost and instant speed. Barry's team watched Claude rewrite the same slide-styling Python script every session, saved it once inside the skill, and now just rerun it. What it generalizes to: any repeated, well-defined subtask, like the domain-availability checker that verifies purchasability before suggesting a name, or a content-pipeline slug generator frozen once. How it goes wrong: genuinely fuzzy judgment should stay in the model, a saved script silently rots when its environment changes, and over-scripting makes a skill brittle.

**Spine 2 — Compound the skill every session.**
The claim: a skill's real edge over a prompt is that it persists, so every run becomes a chance to permanently sharpen it by asking one question, is this a one-time fix or should it live in the skill forever, and then writing the forever-fixes back. Why it is non-obvious: people treat a run as terminal, take the output, and move on, because that is how prompts work, they evaporate the moment the chat closes. Why it is true: a skill is a file Claude re-reads on every invocation, so anything written down is available to the next run, and a standardized format means Claude's own notes are consumable by its future self. Corrections you only say out loud in one chat are lost unless encoded, and once encoded, day-30 Claude is materially better than day-1 Claude. What it generalizes to: team runbooks, onboarding docs, and personal knowledge capture, any artifact where captured corrections compound, for example a code-review skill that slowly accumulates your repo's edge cases. How it goes wrong: writing down one-time noise bloats the skill and hurts triggering, contradictory rules accrete, and without pruning the skill becomes an unmaintainable dumping ground.

### Gap-check verdicts
- **Spine 1 → ❌ NET-NEW GAP.** Queries: "save scripts inside skills / tools layer", "reusable python script as tool inside skill folder, trade tokens for deterministic compute". Nearest catalog hits are "Allowed Tools for Skills" (Master Claude Code › Skills), which teaches the `allowed-tools` permissions field, not bundling a deterministic script as a reusable tool, and "Creating the Skill" (Loopy AI › L3), which uses skill-creator. Nothing teaches freezing a regenerated script into the skill to trade tokens for code compute. Slot: Master Claude Code › Skills (or Advanced Techniques › Skills as Force Multipliers).
- **Spine 2 → 🔗 COMPLEMENT.** Queries: "improve skill over time / compounding loop", "one-time fix or forever, review chat history to enhance skill". "Real World Skill Example 1" (Master Claude Code › Skills) enriches a Swift Concurrency skill with copied expert material from a production bug, and "Improving the Loop" (Loopy AI › L3) evolves a loop with Mermaid variants. Both already teach that a skill should improve; this adds B, the repeatable per-session discipline (ask one-time-vs-forever after every run and feed the chat back), rather than a one-off enrichment. Slot: Master Claude Code › Skills.

## 4. 🎬 Proposed ACS videos

**1. Stop Paying Tokens for the Same Script: Save It Inside the Skill**
- HOOK: Claude rewrites the same helper script every session; here is how Anthropic's engineers make it write that script exactly once.
- THE PROMISE: For anyone building skills who wants cheaper, faster, repeatable runs, after this you can turn any regenerated script into a permanent skill tool.
- THE SHAPE: (1) Show Claude regenerating the same helper script across two sessions, the waste. (2) The three layers of a skill and why the tools layer holds the leverage. (3) Save the script into the skill folder as a tool and rerun it deterministically. (4) Compare cost and speed, tokens versus code compute. (5) The rule of thumb, if you can use code instead of AI, do.
- SPINE: 1
- SLOT: Master Claude Code › Skills (alt: Advanced Techniques › Skills as Force Multipliers)
- RELATIONSHIP: ❌ net-new. The nearest video, "Allowed Tools for Skills", teaches the `allowed-tools` permissions field, so it does not overlap with bundling a deterministic script as a reusable tool.
- PROOF TO REUSE: Barry's quote about Claude rewriting the same slide-styling Python script and saving it "as a tool for his future self"; "you're trading AI tokens for code compute, which is cheaper, faster and repeatable"; "if you can use code instead of AI, you should"; the domain-checker skill run across 10,000+ domains by ten subagents.

**2. The Day 30 Skill: Make Claude Better Every Session by Writing Fixes Back**
- HOOK: Your prompts die when the chat closes; your skills can get smarter every single time you use them.
- THE PROMISE: For anyone maintaining skills, after this you will run a simple after-action loop that compounds a skill's quality run over run.
- THE SHAPE: (1) Prompt versus skill, what evaporates versus what persists. (2) The one question after every run, one-time fix or forever. (3) Encoding a forever-fix (a rule, an example, an edge case) into the skill. (4) The chat-history prompt, "review this back-and-forth and enhance the skill". (5) Pruning so the skill does not bloat and mis-trigger.
- SPINE: 2
- SLOT: Master Claude Code › Skills
- RELATIONSHIP: 🔗 complements "Real World Skill Example 1" and "Improving the Loop". Those already teach that a skill should be enriched or evolved after real runs; this teaches the repeatable per-session write-back habit itself, so Ray should not re-explain enriching a skill from a single production bug.
- PROOF TO REUSE: "Our goal is that Claude on day 30 of working with you is going to be a lot better [than] Claude on day one"; "Anything that Claude writes down can be used efficiently by the future version of itself"; "Is this a one-time fix or should this be in the skill forever?"; the verbatim review-the-back-and-forth prompt.

## 5. 📚 Full wisdom (reference)

**SUMMARY** — Austin Marchese distills four rules from Anthropic engineers' public talks: prompt skills not Claude, invest in tools, build composable skills, and compound them every session.

**IDEAS**
- Anthropic engineers prompt skills, not Claude, treating repetitive tasks as reusable folders rather than fresh prompts.
- Skills are organized collections of files packaging composable procedural knowledge for agents, essentially folders holding instructions.
- Skills sit at layer three, the application layer above raw models and prompts, like phone apps.
- Anthropic builds the phone itself; you build the apps, controlling the skill layer atop their model.
- Typing slash draft email replaces a giant custom prompt encoding your voice, tone, and writing style.
- Every skill has three layers: description, instructions, and tools; most people stop at layer two instructions.
- The description is what Claude checks to decide whether to invoke a skill; vague labels fail.
- Layer three tools, code scripts, API calls, reference files, hold most leverage yet people skip them.
- People craft beautiful prompts then hand the model bare-bones tools with parameters named A and B.
- The creator built a skill checking domain availability programmatically, verifying purchasability before suggesting any domain name.
- Ten subagents sharing one skill searched over ten thousand domains, doing previously impossible work at scale.
- Composable skills mean small focused reusable pieces working together, versus one massive skill doing everything unmanageably.
- One giant content-creation skill generating ideas, scripts, and posts became unmanageable and impossible to safely modify.
- Splitting into idea research, script writer, and LinkedIn skills let each call and chain the others.
- Focused skills make breakage easy to locate, improvements compound everywhere, and components get reused not rebuilt.
- Claude kept rewriting the same slide-styling Python script, so they saved it inside the skill folder.
- Saving a script trades expensive nondeterministic AI tokens for cheaper, faster, repeatable deterministic code compute instead.
- Setting user-invocable to false hides a skill from your slash menu, reserving it purely for agents.
- The disable-model-invocation flag stops Claude auto-running a skill, reserving risky deploy or messaging actions for humans.
- Skills compound: Claude on day thirty works far better than day one by accumulating written learnings.
- After each skill run, ask whether a fix is one-time or belongs permanently inside the skill.
- Feed chat history back: ask Claude to review the exchange and enhance the skill handling automatically.

**INSIGHTS**
- Prompting maturity means climbing from raw models to prompts to skills, the controllable application layer above.
- The real leverage lives in a skill's tools layer, exactly where most builders stop investing effort.
- Determinism beats interpretation: prefer code over AI whenever a task can be encoded as a script.
- Composability turns skills into interchangeable parts; upgrading one improves every workflow that already depends on it.
- Monolithic skills hide failure locations, whereas focused skills expose exactly where and why something quietly broke.
- A skill outlives a chat, so every use becomes a chance to permanently sharpen future behavior.
- Invocation flags separate human-only from agent-only skills, matching risk and audience to each skill's actual exposure.
- Good tool design matters as much as prompts; bare parameters named A and B cripple agents.

**QUOTES**
- "Skills are organized collections of files that package composable procedural knowledge for agents. In other words, they're folders." — Barry (Anthropic)
- "people will put a lot of effort into creating these really beautiful, detailed prompts... and then the tools that they make to give the model are sort of these incredibly bare-bones." — Eric (Anthropic)
- "the parameters are named A and B, and it's kind of like, oh, like an engineer wouldn't be able to like, you know, work with this." — Eric (Anthropic)
- "We kept seeing Claude write the same Python script over and over again to apply styling to slides. So we just asked Claude [to save] it inside of the skill as a tool for his future self." — Barry (Anthropic)
- "code is deterministic, which essentially means if you give it the same input, it will give you the same output every single time." — Austin Marchese
- "when you have a script inside a skill, you're trading AI tokens for code compute, which is cheaper, faster and repeatable." — Austin Marchese
- "A general rule of thumb is if you can use code instead of AI, you should." — Austin Marchese
- "Anything that Claude writes down can be used efficiently... by the future version of itself." — Anthropic engineer
- "Our goal is that Claude on day 30 of working with you is going to be a lot better [than] Claude on day one." — Anthropic engineer
- "Is this a one-time fix or should this be in the skill forever?" — Austin Marchese
- "Review the back and forth I just had after using this skill. Can we enhance the skill so this is handled automatically or we don't make the same mistake again?" — Austin Marchese

**HABITS**
- They think in skills first, reaching for reusable folders instead of writing new prompts each time.
- They invest heavily in the tools layer, documenting functions properly instead of neglecting them after prompting.
- They save repeatedly-generated scripts inside skill folders so future sessions simply rerun rather than regenerate them.
- They keep each skill small and single-purpose, chaining them together rather than building one sprawling mega-skill.
- They set invocation flags deliberately, hiding agent-only skills and gating risky actions behind human-only manual invocation.
- After every run, they ask whether the correction belongs in the skill permanently, then write it.
- They feed prior chat history back into skills, asking Claude to enhance handling of repeated mistakes.

**FACTS**
- Anthropic officially describes skills as folders packaging composable procedural knowledge for agents in their engineering material.
- Claude Code exposes user-invocable and disable-model-invocation flags controlling whether humans or the model runs each skill.
- Anthropic engineers presented these skills practices publicly at the AI Engineering Code Summit earlier this year.
- Code is deterministic: identical inputs always produce identical outputs, unlike token-based generation which interprets and guesses.
- Properly described skills auto-trigger, so Claude invokes them without users explicitly typing the slash command name.

**REFERENCES**
- Anthropic engineering blog and presentation on Claude Skills (source of the layer diagram and definitions).
- AI Engineering Code Summit talks by Anthropic engineers Barry and Eric.
- Claude Code (Anthropic) and its skill frontmatter flags (user-invocable, disable-model-invocation).
- Host: Austin Marchese; his products BuildPartner.ai and The Incubator.
- Referenced follow-up: a video on how Boris Cherny (creator of Claude Code) uses Claude skills.

**ONE-SENTENCE TAKEAWAY** — Stop writing prompts; build composable skills with real tools that compound sharper every single session.

**RECOMMENDATIONS**
- Shift your mental model from writing fresh prompts toward invoking well-described, reusable skills for repetitive tasks.
- Write specific, precise skill descriptions so Claude reliably identifies exactly when to auto-invoke each individual skill.
- Invest in the tools layer: give scripts real documentation and meaningfully named parameters, not A B.
- When Claude keeps regenerating the same script, save it inside the skill folder and rerun it.
- Split any sprawling mega-skill into small, focused, chainable skills that can call each other when needed.
- Set user-invocable false for agent-only skills, and use disable-model-invocation for risky deploy or messaging production actions.
- After each imperfect output, decide one-time-fix versus forever, then encode the forever-fixes permanently into the skill.
- Paste your recent chat back, asking Claude to enhance the skill so those mistakes never recur.
</content>
</invoke>
