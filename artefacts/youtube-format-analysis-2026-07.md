---
tags: [youtube, format-analysis, scriptwriter-skill]
date: 2026-07-13
---

Analysis of 37 videos (Nov 2025 to Jul 2026) via VidTempla analytics, retention curves, and full transcripts. Feeds the design of a new YouTube scriptwriter skill that interviews Ray and turns messy thoughts into a script.

## Performance tiers

**Tier 1: urgency/event-framed strategy videos.** "Fable 5 Is Back Tomorrow! (Don't Waste It)" ranks #1 in views/day (1,249) with the best intro survival on the channel (70% alive at the 5% mark, no cliff). "You Only Have 1 Day Left With Fable 5" ranks #4 with an 11.9% finish rate. These wrap strategy/workflow substance in a time-boxed stakes frame. They win the click AND the intro.

**Tier 2: news volume plays ("Anthropic Just Dropped").** Still the raw-views engine (the Auto Dream video did 100k views and 1,751 subs) but 65 to 70% of clickers are gone by the 10% mark, and the formula shows reuse fatigue: the June rerun of "Biggest Subagent Upgrade Yet" did 225/day vs the April original's 305/day at nearly triple the age, and 15th+ uses of the title formula crowd the bottom half. Survivors rewatch heavily (relative performance climbs to 0.46 to 0.71 by the end), meaning the bodies are reference material for practitioners.

**Tier 3: workflow/identity/insider videos.** Best watch quality and best sub conversion, under-distributed. "I Spent a Day With Anthropic Engineers" has the channel's best retention shape: 313s average view duration, 13.2% finish, relative performance rarely below 0.48. "Loop Engineering" peaks at 0.76 relative performance early (best early hold on the channel). "My Claude Code Workflow for 2026" converted 900 subs on 27k views, a 3.3% sub rate vs 1.7% for the 100k news hit. For these, packaging is the bottleneck, not the script.

**Tier 4: pure explainers with no urgency hook.** Weakest: "Claude Dynamic Workflows (Fully Explained)" loses the door (20% alive at 10%) and the middle (relative performance 0.09 at 62%). "The Highest Point of Leverage", "Task System Explained", and the "Just Added These Features" roundups occupy the bottom third.

**The winning format** is the Tier 1 + Tier 3 hybrid: an urgency or insider-story wrapper (deadline, event, exclusive discovery) around workflow/strategy substance, demoed live on real projects. The news title is a distribution tactic that is fatiguing; the retention and conversion engine is the insider/strategy body.

## The skeleton that works (from 37 transcripts)

1. Cold open "Okay, so" + time-stamp or stakes claim, the subject named within two sentences, then an explicit promise or roadmap. Zero branding intro.
2. First-principles recap with a drawn mental model or diagram.
3. Live demo on Ray's own real products (Hyperwhisper, RayOS, the masterclass itself), with the exact prompt spoken verbatim. The signature move: start the run, explain the internals while it runs, return for the payoff. Dead time becomes teaching time.
4. Insider evidence as the differentiator: binary digs, proxy-extracted system prompts, file-system spelunking, leaked source, N=10 experiments, named-engineer quotes. Always converted into a transferable principle ("even if you can't access the feature, apply the pattern") and often a downloadable artifact.
5. Use-case fan-out with explicit decision heuristics, objection handling ("now you may be thinking..."), and an analogy spine sustained through the video (REM sleep, security camera, chief of staff, Minecraft creative mode).
6. Personal verdict with honest limitations ("I will personally not be using this much") as the trust builder.
7. CTA lands mid-video at a concept boundary, contextually woven (several demos literally implement the sale banner or query the class MCP). Fixed proof stock phrases: "most comprehensive class online", "under 0.2% refunds", "months ahead of the curve". The two lightest-sell videos (Anki, /goal) instead lean on "I only upload when there's something worth saying", and Anki still hit 435 views/day.
8. Prediction/future-direction tease routed to the newsletter, plus comment/email solicitation as the closer.

Length band: 1,500 to 3,800 words (8 to 20 min). Strategy/insider videos at the long end, single-feature news at the short end. Register: outline-scripted with improvised demo narration, except concept essays (prompting guide, leverage video) which are tightly scripted.

## Retention micro-findings

- News titles create an intro cliff: broad curiosity-clickers bounce in the first 10% no matter what the script does. The first 60 to 90 seconds must re-hook them with proof or a demo, not setup.
- Rewatch spikes align with dense on-screen artifacts (prompts, configs, diagrams). Late-video relative performance recovers wherever there is something worth pausing on.
- The 30 to 60% zone is the danger zone: the June subagent video collapsed from 0.63 to 0.28 across 30 to 48% during an undifferentiated use-case fan-out; the Dynamic Workflows explainer cratered at 62%. A delayed payoff (experiment result, live demo return, verdict) needs to sit there.

## Implications for the new scriptwriter skill

The skill's two jobs: interview Ray, then flesh messy thoughts into a script. The interview should extract exactly the ingredients the winning format needs, one question per ingredient:

1. **Stakes wrapper**: what is time-sensitive or exclusive here? What deadline, event, or discovery frames it?
2. **Insider evidence**: what receipts exist (binary dig, experiment, extracted prompt, named person, number)? What did you find that nobody else can show?
3. **Real-project demo**: which product does the demo run on, and what is the exact prompt? What runs long enough to teach over?
4. **Transferable principle**: what does the viewer keep even without access to the feature?
5. **Personal verdict**: will you actually use it? What failed or disappointed?
6. **Analogy spine**: what is this like?
7. **Mid-video payoff**: what result can be teased early and paid off at the 40 to 60% mark?
8. **CTA register**: hard sell (which offer, what urgency) or trust sell? Any downloadable artifact as lead magnet?

Output should NOT be a word-for-word essay (that is the class-scriptwriter shape, built for evergreen ACS videos). YouTube scripts are outline-plus-anchors: verbatim first 3 to 4 sentences (the intro cliff makes these the highest-leverage lines), a beat outline per section, verbatim anchors for the thesis, the analogy, the objection handling, the CTA weave, and the closer, plus a demo shot list with exact prompts.

## Skill audit note

There is no youtube-scriptwriter skill on disk. `youtube-ab-tester` and `youtube-outlier-scout` both reference one ("use youtube-scriptwriter instead") but the only scriptwriter is `class-scriptwriter`, which targets ACS class videos: essay-the-camera-follows, evergreen, no urgency hook, no CTA economy, no retention engineering, no interview stage. The new skill is a fresh build, not an edit.
