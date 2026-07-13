---
tags: [youtube, script-decisions, decision-surfaces, voice-calibration]
status: awaiting-recording
date: 2026-07-13
related: "[[decision-surfaces]]"
---

Decision log for the decision-surfaces script. Written before Ray records so we can compare against the recording transcript afterwards and learn what he enjoys saying versus what he drops, rephrases, or stumbles through. Findings feed back into how future scripts get written.

This file is self-contained: it plus the script plus the recording transcript is everything a comparison session needs. No conversation history required.

## Context

- **The video**: a ~14 minute strategy video for Ray's main channel (@RAmjad) coining the term "decision surface" (the representation you look at in the moment you make a call). Thesis: richer decision surfaces produce richer decisions, and now that AI generates interactive representations in minutes, reviewing plans as walls of markdown is a habit, not a necessity. Wrapped in urgency: Fable 5 is leaving the paid plans, and this loop is what Ray used it for.
- **The script**: `socials/youtube/videos/decision-surfaces.md` (same folder as this file). Written as bullet talking cues because Ray records off the cuff; lines in quotation marks are anchor lines meant to be said close to verbatim, everything else is a beat to riff over.
- **Script section map**: Hook (Fable urgency + richer-decisions thesis) → Decision Surfaces (coin the term, Bret Victor, cost-of-representation argument) → The Plan That Burned Me (HyperWhisper iOS onboarding dead end as receipt) → Brainstorming Richer Surfaces With Fable (16-variant montage) → The Demo (live canvas generation, verbatim prompt) → Soft Anchor (Agentic Coding School CTA) → The Same Jump, in 1786 (Playfair story during the generation wait, canvas reveal as payoff) → Standing On the Plan (canvas walkthrough + four review stickies + Copy JSON + apply) → The Payoff (v6 to v7, plan grows a stage) → Verdict (three honest limits) → Key Insight → Close.
- **The demo**: real project (HyperWhisper's `plans/ios-onboarding-redesign.md`), turned into a pan-and-zoom spatial canvas with lanes, mockups, decision stickies, and spatially anchored comments that export as JSON for Claude to apply.

## How to run the comparison (post-recording)

1. Get the recording transcript (HyperWhisper or YouTube auto-captions). Drop it in this folder or paste it into the session alongside this file and the script.
2. For each decision below, mark the outcome: **kept** (said roughly as scripted), **rephrased** (same beat, own words: capture his phrasing), **dropped** (skipped entirely), **expanded** (riffed longer than scripted: capture what he added).
3. Check each anchor line and each pre-registered hypothesis below against the transcript.
4. The most valuable signals are the *rephrased* and *expanded* ones: his phrasing beats mine and should become the template. Dropped beats mean either he didn't enjoy it or it didn't survive off-the-cuff recall: check which by whether he dropped the idea or just the wording.
5. Write findings into the Results section at the bottom, then distill durable patterns into the youtube-scriptwriter skill (as voice/delivery notes) if they hold across more than one video.

## Decisions and their reasoning

### D1. Fable urgency wrapper leads the video
Chose: open cold on "Fable 5 leaves the paid plans on [DATE]" rather than the burned-plan story or the thesis.
Why: the channel's two best performers by views/day are both Fable urgency videos; Tier 3 strategy bodies hold viewers but lose the click without a time-boxed wrapper. Ray also explicitly asked for it.
Watch for: does he deliver urgency comfortably, or does it feel like a bolt-on he rushes through to get to the ideas?

### D2. Thesis stated as a people-claim, not an idea-claim
Chose: "who's pulling ahead with AI: not better prompts, richer decisions" instead of leading with representation theory.
Why: identity/aspiration claims out-hook abstract claims in the first 35 seconds; it also frames the whole video as a competitive edge, which sets up the CTA.
Watch for: whether he keeps the prompts-vs-decisions contrast or reaches for different framing.

### D3. Coined term defined early, history deferred
Chose: define "decision surface" by minute one with general/chess analogies; move Playfair to mid-video.
Why: Ray called the front-loaded history "a bit boring"; the term needs grounding but analogies people already believe (map table, chessboard) are faster than teaching 1786 first.
Watch for: which analogy he actually uses. Script offers two (generals, chess). If he invents his own, that one wins.

### D4. Playfair story runs during the generation wait, reveal doubles as its payoff
Chose: tell 1786 while the canvas generates, land "nobody has drawn you the chart", cut to the finished canvas: "Until now."
Why: preserves the channel signature (run the thing, teach while it runs, return for the payoff), and moving the history mid-video was Ray's pick. The reveal pays off both the demo AND the story at once, which is the strongest single moment available.
Watch for: does the timing land on camera? If the generation finishes early or late, does he improvise the bridge? Also whether he tells Playfair with relish or compresses it: he flagged history as potentially boring, so this is the riskiest section for his enjoyment.

### D5. Sixteen variants reframed as months of Fable brainstorming, montage not survey
Chose: ~45s montage b-roll with three quick lessons (deck, RFC, simulator) instead of the original three-minute teaching segment.
Why: Ray asked to remove the survey framing; "I've been brainstorming richer surfaces with Fable for months" feeds the Fable wrapper and is the truer story. Kept three named failures because "every representation hides something" needs at least a couple of instances to feel earned.
Watch for: does he linger on the variants anyway? He built them and may enjoy talking about them more than the script allows. If he expands here, future scripts should give his own artifacts more room.

### D6. Burned-plan story kept but demoted from hook to receipt
Chose: the failed onboarding is section three, not the cold open.
Why: the Fable wrapper took the hook slot; the story still carries the proof ("I read this plan. I approved this plan. I missed it.") where it makes the demo meaningful.
Watch for: this confession beat is written punchy. Does he deliver self-critical lines comfortably or soften them?

### D7. Demo prompt verbatim, everything else cue-form
Chose: the generation prompt is the only long block left fully written out.
Why: exact prompts on screen are the channel's rewatch-spike driver, and he types it anyway; reading-while-typing needs no memorization.
Watch for: nothing. This should be frictionless.

### D8. Four review stickies as a numbered list with concrete technical detail
Chose: each sticky names the actual flaw (buy button with no IAP path, silent can't-record mode, missing first-mode step, nine engines).
Why: dense, specific, pause-worthy artifacts in the back half lift retention; vague "I left some comments" would kill the payoff since the v7 reveal references comment three specifically.
Watch for: can he recall four specific stickies off the cuff, or does he read them? If recall fails on camera, future scripts should cap live-recall lists at three or put them on screen.

### D9. CTA framing: get ahead, no urgency mechanics
Chose: "if you want to get ahead and learn this stuff before everyone else does" + months-inside-ACS + 2,000 engineers + 0.2% refunds. Removed lifetime-plan retirement and price placeholders.
Why: Ray's explicit direction. Placed at the generation-wait boundary so it interrupts nothing.
Watch for: which proof phrases he actually says. He has a natural pitch voice; whatever he says here unprompted should become the canonical CTA block.

### D10. Verdict structured as three honest limits
Chose: (1) markdown fine for small plans, (2) still a picture not a model + voice notes and toggles tease, (3) data-viz broadening with the drag-a-variable interactive-surface vision.
Why: all three were Ray's picks; honest limitations are the channel's trust builder and strong-finish correlate. Limit 3 doubles as next-video setup and the comment ask.
Watch for: limit 3 is the newest thinking and closest to his current excitement (he described it unprompted twice). Expect expansion here; capture his live phrasing of the counterfactual-surface idea, it is probably better than mine.

### D11. Anchor lines in quotes, everything else riffable
Chose: roughly a dozen lines marked as say-close-to-verbatim; the rest is cue bullets.
Why: Ray records off the cuff; full prose fights that. The quoted lines are the ones doing structural work (coined term, section landings, the Key Insight).
Watch for: THE core calibration signal of this whole exercise. Which quoted lines survive verbatim? Those are lines he enjoyed. Which get rephrased? Compare his version against mine and learn the delta (sentence length, vocabulary, rhythm).

## Anchor lines to track in the transcript

1. "Fable 5 leaves the paid plans on [DATE]."
2. "A machine for designing richer decision surfaces."
3. "A decision surface is the representation you're looking at in the moment you make a call."
4. "Same information. Different surface. Different blunders caught."
5. "A wall of markdown is one of the worst decision surfaces ever invented."
6. "You're no longer choosing the cheap option. You're just choosing the bad one out of habit."
7. "I read that plan. I approved that plan. I missed it."
8. "Every representation is a choice about which decisions are visible and which are hidden."
9. "The markdown wall wearing a suit."
10. "Your AI writes you plans. The plans are tables. Nobody has drawn you the chart."
11. "Until now. It's done. Look at what just happened to my plan."
12. "Those questions are invisible in markdown. Not hard to see. Invisible."
13. "Eleven years later that sentence just describes a normal Tuesday."
14. "That broken onboarding shipped because I approved it off a table. This version got fixed because I stood on a chart."
15. "Don't ceremony yourself to death."
16. "A table wearing a chart costume."
17. "Not a picture of the data. A surface I can interrogate before I decide."
18. "The surface is the point, not the model."
19. Key Insight blockquote (the Playfair didn't-add-a-number line).

## Pre-registered hypotheses (check these against the transcript)

- H1: he drops or heavily compresses the Playfair history (flagged it as boring) but keeps its landing line (#10), because the landing line is the useful part.
- H2: he expands the data-viz limit well beyond the script: it is his freshest thinking.
- H3: he rephrases the confession beat (#7) into something less staccato: three short sentences in a row is my rhythm, possibly not his.
- H4: the chess analogy survives, the generals analogy gets dropped: one analogy is usually enough off the cuff.
- H5: the CTA comes out shorter than scripted and misses at least one proof stat: whatever stat survives is the one he actually values.
- H6: he adds jokes or asides nowhere in the script, most likely during the canvas walkthrough where he is driving a thing he built and is proud of.

## Results (fill after recording)

- Outcome per decision (D1-D11):
- Anchor lines kept verbatim:
- Anchor lines rephrased (his version vs mine):
- Beats dropped:
- Beats expanded (capture phrasing):
- Hypotheses right/wrong:
- Durable voice rules to feed into youtube-scriptwriter:
