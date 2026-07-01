---
title: How to Build A Self-Improving System with Claude Code
video_url: https://www.youtube.com/watch?v=2fc0NX9vIJ8
video_id: 2fc0NX9vIJ8
channel: Austin Marchese
published: 2026-06-28
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**How to Build A Self-Improving System with Claude Code**](https://www.youtube.com/watch?v=2fc0NX9vIJ8) - Austin Marchese - uploaded 2026-06-28

> Three next-step ACS videos available: all three spines complement existing Loopy AI / Automation coverage.

## The idea worth a video

1. **Self-improving does not mean hands-off; you calibrate autonomy by bucketing each proposed change by stakes.** This is the video's true spine (the LOOP step Austin flags as where "99% get it wrong"): full automation causes silent drift, so an improve-system skill sorts changes into auto-approve, needs-signoff, and needs-more-context. VERDICT: 🔗 next-step video available.
2. **Your own digital exhaust is the highest-signal training data, so bootstrap the system by mining it.** Session history, computer files, Takeout email, and a recorded life-story interview beat context you sit down to author. VERDICT: 🔗 next-step video available.
3. **A knowledge base decays unless skill-driven pipelines refill it, run as scheduled routines.** The lake needs rivers: tested sync skills composed under one orchestration skill, scheduled and referenced so edits propagate. VERDICT: 🔗 next-step video available.

## Summary + counts

Austin Marchese's five-step BUILD framework turns Claude Code into a self-improving system: knowledge base, bulk data ingestion, scheduled pipelines, and calibrated human-review improvement loop.

🔴 0 net-new · 🔗 3 complement · 🟡 0 partial · ✅ 0 covered

*Also film-able (not deep-dived):* **The Karpathy raw-plus-wiki knowledge base pattern** (a raw folder of resources plus a wiki that indexes them as a contents table so the agent locates data without reading everything). One-sentence pitch: build the exact folder skeleton and the add-new-resource skill that keeps the wiki index in sync. Rough slot: Context Engineering, or Master Claude Code CLAUDE.md chapter. Left out of the ranked pitches because it is the substrate the other three spines act on and is partially covered by existing context-layer and CLAUDE.md material.

## 🔬 Deep dive

### Spine A: calibrated autonomy through bucketed review

The claim: a self-improving system should not run fully hands-off; it should route each proposed change by stakes into auto-approve, human-signoff, or needs-more-context. Most people equate "self-improving" with "zero human input," and Austin argues that is the trap. His workout analogy lands it: a fully automated trainer that only ever trains chest leaves you jacked on top and toothpicks below. "The system thought it was improving you, but it was actually breaking you." The mechanism has two links. Because an autonomous optimizer only improves what it can measure and never sees your judgment, it accumulates silent drift; and because low-stakes fixes (dead links, data bloat) genuinely need no judgment while skill edits do, splitting by blast radius lets you delete the review that does not matter and keep the review that does. So the improve-system skill auto-applies bucket one to a change log, writes bucket two to output/review-DATE.md with approve, reject, or approve-and-never-ask checkboxes, and parks bucket three. This generalizes cleanly to CI/CD merge policy: trivial dependency bumps auto-merge, schema migrations require a reviewer. It goes wrong when a high-stakes change is mis-bucketed as auto-approve, or when a review file nobody ticks quietly collapses into drift or abandonment.

### Spine C: mine your own exhaust as training data

The claim: the highest-signal training data for a personal AI system already exists as your own exhaust, so bootstrap by mining it rather than authoring context from scratch. The non-obvious part: people start a knowledge base by sitting down to write context, but Austin inverts it, and the single richest source is your Claude session history, "literally you inside the terminal asking the AI ecosystem questions." The mechanism chains three moves. Because Claude saves session history locally, a prompt can replay every past conversation and extract learnings plus concrete skill suggestions (the load-bearing phrase is "suggest ways we can improve my system"); because your voice and unmet needs are latent in your inbox, a Google Takeout or Outlook export lets Claude infer writing style and spot where you are not yet using AI; and because tacit goals never get written down, recording yourself rambling then having Claude interview you captures context it could never infer. It generalizes to onboarding a hire by handing over the Slack archive and past tickets instead of a hand-written wiki. It goes wrong two ways: dumping everything creates low-signal bloat (Austin: less is more, be selective), and mining email or your computer raises real privacy exposure he says to simply skip if it worries you.

### Spine B: skill-driven pipelines as scheduled routines

The claim: turn one-off ingestion prompts into tested skills, compose them under an orchestration skill, and schedule that as a recurring routine so the knowledge base refills itself. The failure most people hit is treating the initial data dump as the finished system. Austin's lake metaphor names it: you filled the lake once, but with no rivers flowing in it evaporates and stops being useful, so the system IS the rivers, not the fill. The mechanism has two links. Because a routine that inlines its logic is brittle and opaque when it breaks, you first build each pipeline as a separately tested skill (sync-claude-sessions, sync-ecosystem-data, sync-curated-content), then one orchestration skill (/data-ingestion) that calls all three; and because a routine that references a skill inherits every future edit, updating the skill silently updates the routine, keeping maintenance in one place. He schedules ingestion Tuesday and Friday mornings and keeps improvement as a separate routine so a failure tells him exactly which process broke. This generalizes to a data-engineering DAG where extract, transform, and load are independent tested tasks a scheduler sequences. It goes wrong when a skill ships into a routine untested and fails silently at 9am (Austin: "test the skill, please"), or when over-ingestion floods the base with noise.

## 🎬 Proposed ACS videos

### 1. The Self-Improvement Loop That Won't Silently Break Your System

- **HOOK:** A fully automated system only ever trains chest; here is the review loop that keeps yours balanced.
- **THE PROMISE:** For anyone running a self-improving Claude setup, decide exactly what your agent may change on its own.
- **THE SHAPE:**
  - The chest-only workout analogy: why full automation causes silent drift
  - Build the improve-system skill that classifies every proposed change
  - The three buckets: auto-approve, needs-signoff, needs-more-context
  - Sign-off items write to a dated review file with approve, reject, approve-and-never-ask checkboxes
  - Review it in Obsidian; over reps the system learns your thresholds
- **SPINE:** A
- **SLOT:** Loopy AI, L3: Task Lifecycle (sits beside "Improving the Loop")
- **RELATIONSHIP:** 🔗 complements "Improving the Loop" (Loopy AI, L3), which evolves a task loop from completed-session feedback, and "Creating the Skill" (Loopy AI, L3), which defines human gates and blast-radius auto-merge policy for a code-feature lifecycle. Those already teach risk-gated autonomy on a spec-to-PR loop; this adds a persistent three-bucket review QUEUE for a system that edits its OWN skills and knowledge, not application code.
- **PROOF TO REUSE:** the chest-only workout analogy; "We're having AI make the easy calls and I prefer making the hard ones"; the approve / reject / approve-and-don't-ask-again review file viewed in Obsidian.

### 2. Your Best Training Data Already Exists: Mining Your Own Digital Exhaust

- **HOOK:** Stop writing context for your AI. You already generated the best of it just by working.
- **THE PROMISE:** For anyone starting a personal knowledge base, bootstrap it from data you already have lying around.
- **THE SHAPE:**
  - Why your Claude session history is the highest-signal training data you own
  - Prompt your local sessions for learnings plus concrete skill suggestions
  - Have Claude mine your computer for ingestion-worthy files
  - Export email via Google Takeout so Claude learns your writing voice
  - Record a life-story ramble; let Claude interview you to fill the gaps
- **SPINE:** C
- **SLOT:** Master Claude Code, Skills chapter (near "/team-onboarding"), or Loopy AI L2
- **RELATIONSHIP:** 🔗 complements "/team-onboarding" (which analyzes the last 30 days of local Claude usage to summarize work types) and "Getting Prompt Feedback" (which mines conversation history for prompt lessons). Those already read your Claude history; this widens the lens to your ENTIRE footprint (computer files, Google Takeout email, a recorded life-story interview) all feeding one personal knowledge base.
- **PROOF TO REUSE:** "there's really no better training data than your own conversation history with Claude"; the "suggest ways we can improve my system" phrase; the record-then-interview move; the explicit privacy-skip caveat.

### 3. Rivers For Your Data Lake: Scheduling Skills That Refill Themselves

- **HOOK:** You filled the lake once, and without rivers it evaporates. Here is how you build the rivers.
- **THE PROMISE:** For anyone whose knowledge base keeps going stale, make ingestion happen automatically, forever, with no manual thought.
- **THE SHAPE:**
  - The lake-and-rivers metaphor: why a one-time dump decays
  - Build each pipeline as a separately tested sync skill
  - Compose them under one data-ingestion orchestration skill
  - Schedule it as a Claude Code desktop local routine on Tuesdays and Fridays
  - Reference the skill from the routine so edits propagate; split routines to localize failure
- **SPINE:** B
- **SLOT:** Master Claude Code, Automation chapter (beside "Real World Example")
- **RELATIONSHIP:** 🔗 complements "Real World Example" (Master Claude Code, Automation), which schedules a single maintenance routine (monitor the changelog, then update a cheatsheet, then open a PR) and recreates it as a local task. This is the next step: an ingestion ARCHITECTURE of several tested sync skills composed under one orchestration skill, plus the reference-the-skill maintainability principle and per-process routine splitting.
- **PROOF TO REUSE:** the lake-and-rivers metaphor; "test the skill, please"; the four pipeline types; the Tuesday/Friday schedule split; "reference skills so it's easy to update."

## 📚 Full wisdom (reference)

**SUMMARY** — Austin Marchese's five-step BUILD framework turns Claude Code into a self-improving system: knowledge base, bulk data ingestion, scheduled pipelines, and calibrated human-review improvement loop.

**IDEAS**
- The five-step BUILD framework turns Claude Code into a system that improves itself every single week.
- Step one, BASE: create a project holding both a knowledge base and your repetitive-task skills together.
- Karpathy's LLM knowledge base uses a raw folder and a wiki folder as a contents table.
- The wiki references raw files so AI locates information without reading the entire raw folder itself.
- If you ever do the exact same task twice with Claude, immediately build a reusable skill.
- The first skill Austin sets up is add-new-resource, ingesting a file then updating relevant wiki entries.
- Orchestration skills call several smaller utility skills together to produce one much bigger combined output automatically.
- Step two, UPLOAD: bulk-ingest all the historical data you already generated to work smarter, not harder.
- Your Claude conversation history is the most relevant training data because it is you questioning AI.
- Claude saves all session history locally, so a prompt can analyze past conversations for concrete learnings.
- Tell Claude to analyze your computer and identify any files worth ingesting into the new system.
- Export your email via Google Takeout or Outlook export so Claude can learn your writing style.
- Record yourself discussing your life story and project goals, then have Claude interview you filling gaps.
- Step three, INFLOW: build data pipelines that act like rivers keeping your data lake continuously full.
- Skill-driven data ingestion means each pipeline is first a well-tested skill that processes raw data predictably.
- Four pipeline types: your own inputs, ecosystem data capture, curated content, and periodic voice data dumps.
- Use a plus-alias address, such as brad+newsletter, to filter and then ingest niche newsletter content cleanly.
- Step four, LOOP, is where most people get self-improving completely wrong, Austin repeatedly warns his viewers.
- The improve-system skill sorts every proposed change into auto-approve, needs-signoff, and needs-more-context buckets automatically for you.
- Sign-off items get written to a dated review file offering approve, reject, or approve-and-never-ask-again checkboxes each.
- The automation spectrum runs from full auto-approval, risking drift, to reviewing every single change yourself tediously.
- Claude Code desktop local routines schedule your skills with direct file access, bypassing any version-control worries.
- Austin runs data ingestion Tuesdays and Fridays, with system improvements as a separate later evening routine.
- Reference skills inside routines so editing the skill automatically updates the routine that runs it later.
- Step five, DRIVE: actually run the system, bias hard to action, and refuse to over-engineer anything.

**INSIGHTS**
- Self-improving does not mean autonomous; removing human judgment breaks the system while pretending to improve it.
- A one-time data dump evaporates without pipelines; the durable system is the rivers, not the lake.
- Bucketing by blast radius lets AI make easy calls while you reserve energy for hard ones.
- Building skills first makes routines maintainable because updating one skill propagates everywhere the routine references it.
- Your own exhaust beats authored context because it already encodes how you actually think and work.
- Separating ingestion and improvement routines localizes failure, so you know exactly which process actually broke down.
- Less is more when ingesting; high-signal selectivity beats pumping every available resource into the knowledge base.
- The system serves you; delete any skill or piece that is not actively making you better.
- Compressed feedback loops only learn if you actually use the tools and push fixes back manually.
- Over time the bucketing system learns your thresholds for what counts as high or low stakes.

**QUOTES**
- "Now, to step four, which is where most people get self-improving wrong, and I'm going to show you why." — Austin Marchese
- "If you're doing the same thing twice with Claude, you should create a skill." — Austin Marchese
- "there's really no better training data than your own conversation history with Claude." — Austin Marchese
- "if there's no new water keeping the lake full, it will evaporate and no longer be useful." — Austin Marchese
- "this is a step where 99% of people get it wrong." — Austin Marchese
- "The system thought it was improving you, but it was actually breaking you." — Austin Marchese
- "We're having AI make the easy calls and I prefer making the hard ones." — Austin Marchese
- "less is more here. Be very selective with what you're ingesting" — Austin Marchese
- "The important part here is that you are part of the process because this is your system and you need to own it." — Austin Marchese
- "slow is smooth, smooth is fast." — Austin Marchese
- "The only choice that's genuinely wrong is overthinking it." — Austin Marchese
- "Action produces information." — Brian Armstrong (quoted by Austin Marchese)
- "These systems sharpen through reps, not whiteboard sessions." — Austin Marchese

**HABITS**
- Austin creates the add-new-resource skill first with every single person that he personally works with directly.
- He tests every skill on his own machine before trusting it inside any automated routine himself.
- He uses Granola to record meetings without an intrusive AI bot sitting on the actual call.
- Austin ends his days and weeks ranting learned lessons into Claude Code via voice-to-text dictation tools.
- He pulls full meeting transcripts through Granola's MCP and ingests them straight into his knowledge project.
- Austin updates the CLAUDE.md file to remind Claude how the whole framework is consistently set up.
- He reviews the improvement review file inside Obsidian before approving any of the suggested system changes.
- Austin gives away a Claude Max subscription to a commenter in every single video he posts.
- He records YouTube videos publicly with transcripts enabled so he can reference what was actually said.

**FACTS**
- Andrej Karpathy went viral online for popularizing his concept of the LLM-oriented knowledge base folder structure.
- Google offers Google Takeout and Outlook offers an export feature for downloading your full email history.
- Gmail plus-addressing lets an address like brad+newsletter route to the base inbox while staying separately filterable.
- Granola records meetings in the background without placing an AI bot visibly on the video call.
- Claude Code stores all of its session conversation history locally in a file on your machine.
- Claude Code's desktop app supports scheduled routines that can run locally or under version control instead.
- Brian Armstrong, the current chief executive of Coinbase, is credited with saying action produces information himself.
- Hex and Whisper Flow are voice-to-text tools usable for dictating thoughts directly into Claude Code sessions.

**REFERENCES**
- Andrej Karpathy (LLM knowledge base concept), the Anthropic team
- Claude Code, Claude Code desktop app, Claude Max subscription, CLAUDE.md
- Google Takeout, Outlook export, Gmail plus-addressing / alias domains
- Granola and its MCP, Slack direct connection, YouTube (public transcripts), Obsidian
- Hex, Whisper Flow (voice-to-text tools)
- Brian Armstrong / Coinbase ("Action produces information")
- Austin's own videos: Loop Engineering deep dive, Claude knowledge projects, Claude Skills setup
- BuildPartner.ai, The Incubator (Austin's companies), the-ai-playbook.com newsletter

**ONE-SENTENCE TAKEAWAY** — Build a self-improving Claude system by feeding it your data and calibrating human review.

**RECOMMENDATIONS**
- Create a project containing a raw folder, a wiki folder, and a working add-new-resource utility skill.
- Run a prompt analyzing your Claude session history, explicitly asking it to suggest concrete system improvements.
- Ask Claude to analyze your computer and surface any existing files genuinely worth ingesting into it.
- Record yourself explaining your goals, then let Claude interview you to fill remaining context gaps afterward.
- Build separate sync-claude-sessions, sync-ecosystem-data, and sync-curated-content skills, then carefully test each one on your machine first.
- Wrap your sync skills in one data-ingestion orchestration skill, then schedule it as a recurring routine.
- Build an improve-system skill that automatically buckets every proposal into auto-approve, needs-signoff, and needs-more-context categories accordingly.
- Schedule ingestion and improvement as separate routines so failures point to the exact broken process cleanly.
- Create a human-review routine that pings you on Slack if you neglect providing improvement feedback promptly.
- After fixing an output manually, tell Claude to improve that skill based on this exact conversation.
