---
title: "Full Walkthrough: Writing & Using Skills — Nick Nisi and Zack Proser"
video_url: https://www.youtube.com/watch?v=pFsfax19yOM
video_id: pFsfax19yOM
channel: AI Engineer
published: 2026-05-06
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Full Walkthrough: Writing & Using Skills — Nick Nisi and Zack Proser**](https://www.youtube.com/watch?v=pFsfax19yOM) - AI Engineer - uploaded 2026-05-06

> 2 net-new ACS videos available (skill evals; skills as an Agent SDK product), plus 1 next-step complement.

## The one idea worth a video

**Spine 1 — Evaluate skills like code, because over-specifying can make the agent worse.** Run the task with and without the skill, grade both on a rubric, and cut any skill that lowers the score. It subsumes the "constraints over prescription" advice: evals are how you *discover* that prescription hurts.
VERDICT: ❌ net-new video available.

**Spine 2 — A skill can be the entire brain of a shipped product on the Claude Agent SDK.** WorkOS CLI's `npx workos install` runs the Agent SDK, and all its intelligence lives in skills. It reframes skills from personal shortcut to product runtime.
VERDICT: ❌ net-new video available.

**Spine 3 — Do not design skills upfront; mine a week of your own logs to discover them.** Have Claude analyze your saved JSONL history and propose which frictionful, repeated tasks should become skills. It subsumes "context is gold," meta-skills, and the Slack-to-Linear example.
VERDICT: 🔗 next-step video available.

## Summary + counts

Nick Nisi and Zach Proser, WorkOS DX engineers, run an 81-minute AI Engineer workshop on writing, testing, sharing, and scaling portable Claude Skills.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

*(Also film-able, not deep-dived: a confidence-score gate skill; governing shared skills at team scale.)*

## 🔬 Deep dive

**Spine 1 — Evaluate skills like code; over-specifying makes agents worse.**
The claim: treat a skill like code you test, run the task with and without it, grade both against a rubric, and delete any skill that lowers the score. What most people get wrong: they write a skill, feel it helped, and keep it forever, never measuring it, and the surprising failure is that a detailed "helpful" skill can override the model's good defaults and make it worse. The mechanism: an eval runs the same task many times, once bare and once with the skill loaded, then scores each run; because the model is often already competent, a prescriptive skill fights good default behavior and drags accuracy down. Nick's Next.js installer "led to like a 30% drop" because he "was being too dogmatic about what I wanted it to do," and without the eval he never would have seen it. This generalizes to CLAUDE.md rules and subagent prompts: any injected context whose value is assumed but never measured. How it goes wrong: the numbers are fuzzy, so trust the direction, not the decimal, and beware overfitting to one rubric.

**Spine 2 — Skills as the brain of a shipped Agent SDK product.**
The claim: a skill is not just a personal shortcut, it can be the entire reasoning core of a product built on the Claude Agent SDK. Why it is non-obvious: skills are usually framed as convenience for your own editor sessions, and the leap is that the same markdown files become the brain of a CLI that strangers install and run. The mechanism: WorkOS CLI's flagship command, `npx workos install`, runs the Agent SDK, which Nick calls "programmatic cloud code that you can ship," and its intelligence is not hand-written logic because "all of the brains are actually skills that are in the work OS skills directory." The CLI proxies calls to Claude through the company API token, so a user with no Anthropic account gets a zero-friction agent that detects their framework, removes competing auth, and installs WorkOS. That yields a "two birds" loop: build the skill, then prove it by having the CLI run it. This generalizes to any onboarding or migration CLI where the hard part is judgment, not fixed steps. How it goes wrong: shipping an agent on your token means cost and prompt-injection exposure, and skill drift silently degrades the product as models change.

**Spine 3 — Discover skills by mining your own history, not by designing upfront.**
The claim: do not sit down and author a skill library, discover it by having Claude mine a week of your real work and propose the skills to split out. Why it is non-obvious: the instinct is to write skills for tasks you imagine repeating, but you cannot predict them, whereas your own logs already reveal them. The mechanism: every Claude conversation is saved locally as a JSONL file, so after a week you can ask the model to analyze that history and surface the repeated, painful patterns worth encoding. The signal Zach trusts is emotional, "the nagging things that I find the most cognitive resistance to doing every week that I actually need to turn into skills," and the richest input is failure, "especially what failed, especially what didn't go well," because that is where a skill removes the most pain. His Slack-to-Linear ticketing skill came exactly from a context-switch he dreaded. This generalizes to mining history for prompt rules, CLAUDE.md entries, or subagent definitions. How it goes wrong: logs capture what you did, not what you should have done, so a naive miner can encode bad habits, and you still curate.

## 🎬 Proposed ACS videos

**1. Are Your Skills Actually Helping? Run the Eval**
- HOOK: You added a skill and it felt smarter, but a quick eval shows it made Claude thirty percent worse.
- THE PROMISE: For anyone shipping skills, learn to prove a skill helps before you trust it, and delete the ones that quietly hurt.
- THE SHAPE: 1) Pick a task, run it bare, score the output on a rubric. 2) Add the skill, run again, compare. 3) Watch an over-prescriptive skill lose. 4) Trim it down to a few constraints, re-run, confirm the gain. 5) Wire it into Claude's built-in eval framework and read the before/after HTML report.
- SPINE: Spine 1.
- SLOT: Advanced Techniques > Skills as Force Multipliers (new "Evaluating Skills" beat).
- RELATIONSHIP: ❌ net-new. The Skills chapter teaches authoring, arguments, models, forked contexts, and subagents, but nothing measures whether a skill improves or degrades the agent.
- PROOF TO REUSE: Nick's Next.js installer "30% drop" from being "too dogmatic"; the Apple Watch analogy for fuzzy-but-directional metrics; Claude's before/after HTML eval report with pass thresholds around 80-90 percent.

**2. Ship a CLI Whose Entire Brain Is Skills (Claude Agent SDK)**
- HOOK: `npx workos install` detects your framework, rips out the wrong auth, wires in the right one, and every decision is a markdown skill.
- THE PROMISE: For builders, turn your skills into a distributable product on the Claude Agent SDK that even non-customers run with zero setup.
- THE SHAPE: 1) Move a working skill into a skills directory. 2) Wrap it with the Claude Agent SDK as a CLI command. 3) Proxy calls through your own API token for zero-friction onboarding. 4) Have the agent detect project context and act. 5) Close the "build the skill, prove it by shipping it in the CLI" loop.
- SPINE: Spine 2.
- SLOT: For Business (or a new "Building with the Agent SDK" chapter).
- RELATIONSHIP: ❌ net-new. ACS covers many forms of Claude Code but not the Agent SDK as the runtime for a shipped, skills-powered product.
- PROOF TO REUSE: "all of the brains are actually skills"; "programmatic cloud code that you can ship"; the token-proxy onboarding that even creates a WorkOS account you claim later.

**3. Stop Writing Skills. Let Claude Mine Them From Your Week**
- HOOK: You cannot guess which skills you need, but a week of your JSONL logs already knows.
- THE PROMISE: For daily Claude users, build your real skill library by mining your own history instead of designing upfront.
- THE SHAPE: 1) Work normally for a week. 2) Point Claude at your saved conversation logs. 3) Ask which repeated, painful patterns should become skills. 4) Prioritize the task you most resist doing. 5) Have skill-creator draft it, then refine over a few runs.
- SPINE: Spine 3.
- SLOT: My Daily Workflows (or Prompt Engineering, next to "Getting Prompt Feedback").
- RELATIONSHIP: 🔗 complements "Getting Prompt Feedback." That video reviews one session to extract prompt rules for next time; this mines a whole week of history to propose which entire skills to build, so do not re-teach session-level prompt review.
- PROOF TO REUSE: "the nagging things... I need to turn into skills"; "all of that context is gold... especially what failed"; the Slack-to-Linear skill born from a dreaded context switch.

**Also film-able (not deep-dived)**
- *A confidence-score gate skill.* A skill that self-scores its understanding (problem clarity, goal definition, success criteria) and loops via the ask-user-question tool until it is ~95% confident before executing. 🔗 complements "Clarifying Questions" and "Ask User Question Example" by making the gate a reusable, numeric rubric baked into a skill. Slot: Prompt Engineering.
- *Governing shared skills at team scale.* Deduping near-identical skills, review overhead on skill PRs, the fork-locally pattern, versioned plugin marketplaces, and pruning verbose skills as new models drop. ❌ net-new for teams. Slot: For Business.

## 📚 Full wisdom (reference)

**SUMMARY**
Nick Nisi and Zach Proser, WorkOS DX engineers, run an 81-minute AI Engineer workshop on writing, testing, sharing, and scaling portable Claude Skills.

**IDEAS**
- Skills carry the DRY principle into the agentic era: encode work once, never repeat yourself again.
- A skill can be thirty lines of markdown yet transform generic feedback into hyperspecific project analysis.
- The description field is a routing rule the model reads at runtime to decide skill loading.
- Descriptions are written for the LLM, not humans; they determine automatic invocation, not reader comprehension entirely.
- Providing a few sharp constraints beats verbose prescription; over-specifying is the common skill-design failure mode here.
- The bang-backtick syntax runs a shell command and interpolates its exact output into the skill context.
- Script interpolation gives a deterministic base so the agent stops speculating about what you actually mean.
- Progressive disclosure keeps skill.md tiny by loading reference files only when a task actually needs them.
- WorkOS built a "skill router": a reference map pointing to framework-specific migration guides loaded on demand.
- Confidence scoring makes a skill self-grade problem clarity and loop with questions before executing any work.
- Claude ships an eval framework that produces before-and-after HTML reports comparing skill against no skill.
- Nick's Next.js installer skill dropped accuracy roughly thirty percent because it was too prescriptive, evals revealed.
- Ask Claude to analyze a week of your work and propose skills to split out afterward.
- The nagging tasks you resist doing every week are exactly the ones worth becoming skills first.
- Your conversation logs, especially the failures, are now gold for a skill creator to mine.
- The WorkOS CLI's npx install runs the Claude Agent SDK whose entire brain is composed skills.
- Zip a skill folder, rename it dot-skill, and non-technical teammates drag it into Claude Desktop directly.
- Non-coding skills shine: a Remotion skill auto-builds a weekly git-history demo movie from your own commits.
- A Slack-to-Linear skill monitors mentions, dedupes, and files tickets without ever breaking your coding flow state.

**INSIGHTS**
- Skills win because determinism can be injected into an otherwise non-deterministic conversation exactly where it matters.
- CLAUDE.md loads every session and bloats context; skills load only when their description actually matches intent.
- Constraints outperform instructions because they leave the model room to reason while fencing off failure modes.
- Evals turn skill-writing from vibes into measurement: a skill that lowers scores should be cut immediately.
- The eval math is fuzzy, but the direction it reveals is trustworthy, like an Apple Watch.
- Skills are best discovered retrospectively from friction, not designed perfectly upfront before you know real needs.
- The portability of skills, not any single feature, is what makes the primitive genuinely powerful.
- Shared skills recreate every code-management problem: reviews, forks, duplication, versioning, and pruning as models keep changing.
- Building a skill and shipping it inside a CLI proves the skill with one shipped artifact.
- Sub-agents suit standalone-context work; skills suit reusable behavior; the two compose rather than compete directly.

**QUOTES**
- "When is the last time you wrote a line of code by yourself?" — Nick Nisi
- "It's been like probably six or eight months now." — Zach Proser
- "It's almost like carrying, if you will, the dry pattern into the agentic era." — Zach Proser
- "Descriptions are routing rules, right? They're less for us and they're more for the AI." — Nick Nisi
- "Without scripts, the AI is just speculating on what you mean when you say go get the latest commits." — Nick Nisi
- "The nagging things that I find the most cognitive resistance to doing every week that I actually need to turn into skills." — Zach Proser
- "Now all of that context is gold. Like the conversation, especially what failed, especially what didn't go well." — Zach Proser
- "I was making it worse by being too dogmatic about what I wanted it to do and it led to like a 30% drop." — Nick Nisi
- "All of the brains are actually skills that are in the work OS skills directory." — Nick Nisi
- "Rename that from zip to .skill and now a nontechnical teammate can drag that into cloud desktop." — Nick Nisi

**HABITS**
- Nick keeps his CLAUDE.md extremely small, telling Claude only to stay terse and never bloat output.
- Zach waits a week, then asks Claude which skills to split from that accumulated week's work.
- They keep public WorkOS skills generic, packing expected acronyms into descriptions so routing triggers reliably enough.
- When a skill misbehaves, they simply ask Claude why it chose that and how to improve.
- Nick invokes skills by name or slash command when automatic routing does not pick it correctly.
- Zach dictates almost all code now using Whisper Flow rather than typing at the keyboard directly.
- They run Codex review of Claude's output through a skill instead of manual copy-paste shuffling anymore.
- Zach runs a looped skill every fifteen minutes to watch Slack and file Linear tickets automatically.
- They install skills from Claude plugin marketplaces pointed at internal git repos for team access easily.

**FACTS**
- Roughly ninety-one percent of the workshop room raised hands using Claude as their daily driver tool.
- Skills work across Claude Code, Codex, Cursor, Claude Desktop, and the Pi agent harness available today.
- A skill folder renamed from .zip to .skill installs directly by dragging into Claude Desktop instantly.
- Zach generated all interstitial scenes for a thirty-two-minute film using one image-to-video skill within an hour.
- The image-to-video skill is only about thirty lines of markdown plus two small Python scripts total.
- Nano Banana generates a usable image in under seven seconds from a single text prompt.
- The WorkOS CLI proxies commands to Claude through the company API token for zero-friction user setup.
- Claude conversations are saved locally as JSONL files that a skill creator can later mine directly.

**REFERENCES**
Claude Code, OpenAI Codex, Cursor, Claude Desktop and Web, Pi (the harness under openclaw), WorkOS, the Claude Agent SDK, the "superpowers" skills library, Vercel's npx skills tool and find-skills, Claude's built-in skill-creator / skill-builder, the Remotion skill, Nano Banana (Google image model), the VO video API, Whisper Flow, Obsidian, Slack and Linear connectors, DaVinci Resolve, the Ralph Loop workshop, Nick's open-source "ideation" plugin, Nick's "case" DX agent built on Pi, Slidev, the public WorkOS skills GitHub repo, nicknisi.com, zackproser.com.

**ONE-SENTENCE TAKEAWAY**
Skills are portable, testable units of agent behavior; discover them from friction and measure them.

**RECOMMENDATIONS**
- Write your skill description for the model's router, listing every acronym and trigger phrase you expect.
- Replace prescriptive step lists with a few sharp constraints and let the model reason more freely.
- Use bang-backtick script interpolation whenever a workflow step must start from deterministic command output data reliably.
- Split large skills using progressive disclosure, pointing to reference files that load only on demand each time.
- Build an eval that runs the task with and without your skill, then compare the scores.
- After a busy week, ask Claude to mine your conversation logs for skills worth splitting out.
- Add a confidence-score gate so a skill interrogates you until it truly understands the request fully.
- Install Claude's built-in skill-creator, then ask it to critique, evaluate, and improve every new skill immediately.
- Turn the weekly task you most resist doing into a skill before optimizing anything else first.
- Share team skills through a versioned plugin marketplace rather than copying loose zip files around manually.
</content>
</invoke>
