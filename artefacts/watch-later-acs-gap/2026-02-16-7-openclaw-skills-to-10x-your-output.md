---
title: "7 OpenClaw Skills To 10x Your Output"
video_url: https://www.youtube.com/watch?v=ryhzpLe9O_U
video_id: ryhzpLe9O_U
channel: Riley Brown
published: 2026-02-16
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**7 OpenClaw Skills To 10x Your Output**](https://www.youtube.com/watch?v=ryhzpLe9O_U) - Riley Brown - uploaded 2026-02-16

> next-step video available: a "Take the Wheel" driver-mode skill goes beyond the built-in Ask User Question tool.

## The one idea worth a video

**1. Take the Wheel: a mode skill that flips the agent into the driver, interviewing you one urgent question at a time until a long task is done.** This is the video's climax and its most transferable technique. It reframes the human-agent relationship: instead of you pushing a reactive agent, the agent supplies the agency and pulls the deliverable out of you.
VERDICT: 🔗 next-step video available (complements the built-in Ask User Question tool).

**2. Fewer skills win: past a point, more skills make an agent worse at choosing the right one, so keep each agent's skill set small and split responsibilities across role-scoped agents.** A genuine design principle, but ACS already teaches the too-many-skills problem via the disable mechanic.
VERDICT: 🟡 partial (the strategic curation / agent-fleet layer is the missing angle).

**3. Text your agent: the jump from chatbot to employee is a persistent always-on host plus a messaging bridge, so the agent runs 24/7 and you drive it from your phone.** Load-bearing for understanding the whole video, but ACS already covers this end to end.
VERDICT: ✅ covered (kept for context, no pitch).

## Summary + counts

Riley Brown runs a 2.5M-follower content operation from a Mac Mini via an OpenClaw/Claude agent controlled through Telegram, walking through his seven most useful skills.

🔴 0 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 1 covered

*Also worth noting (not deep-dived, folds into existing coverage): the agent self-edits its own `tools.md` to persist a correction as memory, which sits inside ACS's existing "Agent Introspection" and context/memory material rather than being a standalone gap.*

## 🔬 Deep dive

**Spine 1 — Take the Wheel (🔗 complement)**
The claim: a single mode-switching skill can flip an agent from a passive responder into a relentless driver that interviews you one urgent question at a time until a big task is finished. Why it is non-obvious: most people optimise the human's prompts, assuming the human must supply direction. Riley names the bottleneck differently: "My biggest problem with AI is it's very reactive. I still have to provide the agency and push the agent." Why it is true: a long creative task stalls because each step needs a human micro-decision, and batching four questions upfront is heavy and easy to abandon. By forcing exactly one question, putting the critical part in all caps, and burst-messaging with reframes, the skill converts open-ended authoring into a tight answer-only loop you can clear from a phone, so momentum never dies. It generalises to any decision-dense deliverable: ad batches, spec writing, incident triage, where a coding agent should extract decisions rather than wait. How it goes wrong: the urgency is deliberately annoying and can nag, a bad question ordering wastes turns, and without stored quality examples the questions drift generic.

**Spine 2 — Fewer skills win (🟡 partial)**
The claim: past a point, adding skills makes an agent worse, because it can no longer reliably choose which skill to invoke, so keep each agent's skill set small and split responsibilities across role-scoped agents. Why it is non-obvious: the intuitive move is to keep bolting on capabilities, treating more skills as strictly more power. The mechanism: skill selection is itself an inference problem over the skills' descriptions, so every additional skill adds a competing candidate and a chance to misroute, degrading the routing accuracy of the skills you actually rely on. In Riley's words, "the more skills you add, the less effective it becomes because it stops knowing what skills to use." It generalises to tool-calling agents and MCP servers, where dozens of exposed tools dilute selection, and it motivates his plan for several narrow agents (operator, hiring, content) sharing one Notion notebook for context but not one bloated skill list. How it goes wrong: over-splitting fragments context and forces you to remember which agent owns what, too-aggressive pruning removes a skill you needed, and shared memory can leak the wrong preference between agents.

**Spine 3 — Text your agent (✅ covered)**
The claim: the leap from chatbot to employee happens when the agent runs persistently on an always-on host and you reach it through a normal messaging app, available from your phone anywhere. Why it is non-obvious: people picture agentic coding as a terminal on a laptop; Riley runs it headless on a Mac Mini and never opens a terminal to use it, driving everything from Telegram. The mechanism: a persistent host keeps the agent, its identity files, and its accumulated memory alive between sessions, and a messaging bridge turns every idle phone moment into an input channel, so the agent behaves like a coworker you text rather than a tool you launch. The workspace files (agents.md, soul, mission, memory) give it a stable personality each fresh chat inherits. It generalises to a cloud VM for a fully remote agent, which is how his second agent, Rick Mupple, runs. How it goes wrong: an always-on agent with broad write access and skip-permissions is a real security surface, a dedicated device is another machine to maintain, and phone-only control tempts you to skip reviewing what it did. NOTE: this spine gap-checks to ✅ COVERED, so it earns a deep dive for context but no pitch and does not count toward the post gate.

## 🎬 Proposed ACS videos

### 1. Take the Wheel: Build a Skill That Interviews You Until the Work Is Done
- **HOOK:** Your agent keeps waiting for you. Flip it: make the agent chase you until the job is finished.
- **THE PROMISE:** For anyone who stalls on long creative work with an agent. After this you can build a driver-mode skill that pulls a finished draft out of you in a handful of phone replies.
- **THE SHAPE:**
  1. The problem: agents are reactive, you are the bottleneck supplying agency.
  2. Write a "take the wheel" skill: identify the current task, find the one missing decision, ask ONE question with the critical part in all caps.
  3. Behaviour rules: one question at a time, burst messaging, reframe relentlessly, sound urgent.
  4. Live demo: drive a long-form script (or spec) to a finished outline in four answers.
  5. The off switch and when the nagging becomes counter-productive.
- **SPINE:** 1 (Take the Wheel).
- **SLOT:** Prompt Engineering, chapter "Aligning to Your Intent" (or Techniques). Alternatively Master Claude Code / Skills as a persona-skill example.
- **RELATIONSHIP:** 🔗 complements "Ask User Question Tool" and "Ask User Question Example" (Master Claude Code, Planning), which teach the built-in tool that asks up to four clarifying questions before acting to resolve ambiguity. This adds the next step: a persistent driver-mode skill that inverts agency and relentlessly interviews you one urgent question at a time to push a long generative task to completion, not just a one-shot clarify-before-coding.
- **PROOF TO REUSE:** The exact skill spec quote ("you are now the leader... ask the single most critical question that moves the task forward"); "reframe relentlessly" and "always put the most important question in all caps"; the quote "My biggest problem with AI is it's very reactive."

### 2. Fewer Skills, Sharper Agent: Design a Small Role-Scoped Agent Fleet
- **HOOK:** More skills does not mean more power. Past a point your agent stops knowing which skill to use.
- **THE PROMISE:** For anyone whose agent has drifted into a messy pile of skills. After this you can scope a tight skill set per role and split work across several agents that share memory.
- **THE SHAPE:**
  1. The failure: too many skills degrade routing, the agent picks wrong.
  2. Curate: keep each agent narrow and role-scoped.
  3. Split by role (operator, hiring, content) with a shared context store.
  4. When to disable a skill versus delete it versus move it to another agent.
- **SPINE:** 2 (Fewer skills win).
- **SLOT:** Master Claude Code, chapter "Skills" (sits next to Disable Model Invoked Skills), or Advanced Techniques / Multi-Agent Orchestration.
- **RELATIONSHIP:** 🟡 fills the gap in "Disable Model Invoked Skills" (Master Claude Code, Skills), which covers turning off individual noisy skills so Claude stops choosing at the wrong time. Missing is the upstream design discipline: scoping a small skill set per agent from the start and splitting responsibilities across role-specific agents sharing one memory, rather than one bloated agent. Secondary pitch, weaker than #1.
- **PROOF TO REUSE:** "the more skills you add, the less effective it becomes because it stops knowing what skills to use"; "you don't want it to just do things randomly, or else your life is just going to get more chaotic"; his plan for operator, hiring, and content agents sharing one Notion notebook.

## 📚 Full wisdom (reference)

**SUMMARY**
Riley Brown runs a 2.5M-follower, 15-account content operation from a Mac Mini using an OpenClaw/Claude agent controlled via Telegram, walking through his seven most useful skills.

**IDEAS**
- Riley runs his entire content operation through an OpenClaw AI agent living on a Mac Mini.
- He controls the agent through Telegram, calling it the easiest messaging bridge with full command access.
- Skills are small markdown files that, paired with API keys, grant the agent new concrete capabilities.
- The agent's core identity lives in files: agents.md, identity.md, soul, mission, and memory shape its personality.
- He seeded the agent with obsessions: hooks, intros, conversions, brand-building, and growth hacking, mirroring his own.
- A Notion skill lets the agent create, refine, and organize scripts across content and key-docs notebooks.
- A Supadata-powered transcript extractor pulls transcripts from any social platform link straight into Notion for reference.
- He builds a corpus of competitors' top transcripts, then writes new scripts in their exact voice.
- A Typefully skill analyzes a video with Gemini, drafts captions, and attaches the clip on X.
- A read-only Linear skill summarizes team tasks and builds content calendars from upcoming shipping product features.
- He built a Nano Banana face-swap skill from his phone via Telegram on a morning walk.
- A SERP API skill scrapes the top forty YouTube thumbnails into a research PDF mood board.
- The thumbnail skill swaps his face onto scraped thumbnails, giving his human editor a variation reference.
- A Google Images skill via SERP API embeds relevant illustrations directly into the agent's Notion scripts.
- His favorite skill, Take the Wheel, flips the agent into an urgent, one-question-at-a-time, relentless task driver.
- Take the Wheel puts the single most important question in all caps for fast phone answering.
- The agent self-edits its tools.md file to persist preferences like which notebook new docs belong in.
- He warns that adding too many skills makes the agent worse at choosing the right one.
- He plans multiple role-specific agents, operator and hiring, all sharing one shared Notion notebook for context.

**INSIGHTS**
- An agent becomes an employee, not a chatbot, once it owns persistent tools and messaging access.
- The scarce resource for agents is relevant context, so collecting reference corpora beats clever one-off prompting.
- Any API useful during vibe coding is probably useful wired into an agent as a skill.
- Skill count trades against reliability: more skills means the agent often routes to the wrong one.
- AI stays reactive by default; a driver-mode skill supplies the missing agency to actually finish work.
- Treating the agent like a curious employee, asking what it changed, reveals how it actually works.
- Read-only access to sensitive systems lets an agent plan safely without ever risking accidental destructive writes.
- Correcting an agent once, just like a new hire, becomes a persisted rule it follows thereafter.
- Splitting responsibilities across several narrow agents beats one bloated agent that simply no longer behaves predictably.

**QUOTES**
- "Meanwhile, I'm using AI agents running on this Mac Mini to run my entire content operation with over 2.5 million followers across 15 different accounts." — Riley Brown
- "these skills are what allows it to go off and do different things." — Riley Brown
- "the most important thing with AI agents is making sure that you collect a ton of relevant context." — Riley Brown
- "Any useful API that you've used vibe coding is probably useful when building an AI agent" — Riley Brown
- "You're just talking to an employee." — Riley Brown
- "the more curiosity you have about the agent, the more you're deeply going to understand how it works" — Riley Brown
- "My biggest problem with AI is it's very reactive. I still have to provide the agency and push the agent." — Riley Brown
- "as soon as I use the skill take the wheel it just turns into just like let's get this done." — Riley Brown
- "the more skills you add, the less effective it becomes because it it stops knowing what skills to use." — Riley Brown
- "you don't want it to just do things randomly, or else your life is just going to get more chaotic" — Riley Brown
- "It said, \"Hold my beer.\"" — Riley Brown

**HABITS**
- He types slashreset before starting every new task to start the agent with a clean session.
- He uses Telegram as a dedicated agent app, keeping his bots separate from personal human conversations.
- He always asks the agent to return a clickable Notion link right after creating any document.
- He tests a new skill by resetting the chat, forcing a fresh session to invoke it.
- He inspects the agent's own workspace files in Cursor or VS Code to understand its behavior.
- He tests expensive batch skills on just two items first before spending tokens on all forty.
- He asks the agent to explain exactly what changed whenever it says it saved a preference.
- He instructs new skills to ask follow-up questions when he does not supply enough topic detail.
- He keeps his API keys secret, covering them with screenshots whenever he pastes them for skills.

**FACTS**
- Riley Brown operates over 2.5 million followers across fifteen different social accounts from one Mac Mini.
- OpenClaw installs by running a single terminal command copied directly from the OpenClaw.ai website's download section.
- The Supadata transcript API costs roughly fifteen dollars monthly for about three thousand separate transcript extractions.
- Riley's agent had already run the Supadata transcript API roughly one hundred fifteen separate times recently.
- Hidden dotfiles like .claw appear in Finder only after pressing Command Shift Period to reveal them.
- OpenClaw can connect to iMessage, WhatsApp, Telegram, or Slack to serve as its human control channel.
- Notion integrations only access pages you explicitly connect through the workspace's access tab, not everything automatically.
- Riley's channel has roughly 180,000 subscribers, a mix of beginners and people already actively vibe coding.
- The agent runs on Opus 4.5, and cloud agents like Rick Mupple run on virtual computers.

**REFERENCES**
OpenClaw (OpenClaw.ai), Claudebot / "Vibe Claw" agent, Mac Mini, Telegram (control channel), WhatsApp, iMessage, Slack, Notion + Notion integration API keys, Cursor, VS Code, Finder, Linear, Typefully (X drafting/scheduling API), Supadata transcript API, Gemini API (video analysis), Nano Banana Pro (face swap), SERP API / SerpApi (thumbnail scrape + Google Images), X / Twitter, ChatGPT, Opus 4.5, vibecode.dev, workspace files (agents.md, identity.md, soul, mission, memory, tools.md), the "Take the Wheel" skill, the "Thumbnail Mood Board" skill, Kane Callaway (creator referenced), Rick Mupple (cloud agent).

**ONE-SENTENCE TAKEAWAY**
Give one focused agent messaging access, a few API-backed skills, and then let it drive.

**RECOMMENDATIONS**
- Ask your agent for its exact workspace file path, then open that folder in VS Code.
- Build a Take the Wheel skill that interrogates you with one urgent question at a time.
- Extract your competitors' best transcripts into Notion, then reference them later to write in their voice.
- Give sensitive tools like Linear read-only access first so the agent simply cannot break anything important.
- Keep each agent's skill set small and tightly role-scoped so it reliably picks the correct skill.
- When the agent saves a preference, ask it exactly which file and line it just edited.
- Test any expensive batch skill on two items first before letting it process the full set.
- Have the agent instruct its new skills to ask follow-up questions when your brief is incomplete.
- Reuse any API you liked while vibe coding by simply wrapping it as an agent skill.
</content>
</invoke>
