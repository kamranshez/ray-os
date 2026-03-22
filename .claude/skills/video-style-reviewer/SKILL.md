---
name: video-style-reviewer
description: Review YouTube video scripts and transcripts for explanation quality, using the "AI Search" style as a gold standard. Use this skill whenever the user wants feedback on a video script, wants to review a draft script, asks "how's this script?", "review my video", "does this explain well?", or wants to improve their explanation style for YouTube. Also use when comparing scripts against the AI Search style or when the user mentions "video style review".
---

## What This Skill Does

You review YouTube video scripts/transcripts and give specific, actionable feedback on explanation quality. Your gold standard is the "AI Search" channel style — a masterclass in making complex technical topics accessible and engaging.

## The Gold Standard: AI Search Style Principles

These principles were extracted from analyzing how AI Search explains dense research papers to a general audience. Use them as your rubric.

### 1. The Relatability Hook (First 15 seconds)

Open with a shared frustration or experience the viewer already has. Don't open with "Today we're going to talk about..." — open with a feeling.

**Gold standard example:** "We've all been there. We ask an AI a question and it confidently gives us the wrong answer. It just made things up and it blatantly lies to us."

**Why it works:** The viewer nods along before they even know what the video is about. You've earned 30 more seconds of attention by making them feel understood.

**What to look for in scripts:** Does the opening connect to a real frustration or experience? Or does it start with abstract context-setting?

### 2. The Promise + Accessibility Pledge

After the hook, explicitly tell the viewer: (a) what they'll learn, and (b) that you'll make it easy. This removes the fear of "this will be over my head."

**Gold standard example:** "This is one of the most insightful papers in the past few months. So, that's exactly what we're going to go over in this video. Now, this is quite a technical paper, but as always, I'm going to break this down into simple terms so that it's easy to understand for anyone."

**What to look for:** Does the script promise value AND promise accessibility? Missing either one loses viewers.

### 3. Context Before Complexity

Before diving into the solution, explain why the problem is hard. Build the "why should I care?" foundation first. Layer information: problem → why it's hard → existing failed attempts → new breakthrough.

**Gold standard pattern:**
- Here's the problem (hallucinations)
- Here's why it's hard to even detect (confident-sounding lies)
- Here's the scale (40% hallucination rate — a staggering statistic)
- Here's what people assumed would fix it (bigger models, more compute) — but it didn't
- NOW here's the breakthrough

**What to look for:** Does the script rush to the "answer" before the viewer understands why the question matters? Does it build tension?

### 4. Everyday Analogies for Technical Concepts

Translate every technical mechanism into something the viewer already understands. The best analogies are physical, sensory, or social — things people can picture.

**Gold standard examples:**
- Neural networks → "dials and knobs that determine how much data flows through each layer"
- H-neuron amplification → "a volume dial you can turn up or down"
- CCT metric (causal efficacy) → "It's like trying to figure out who's actually controlling a massive corporate meeting. If you just measure volume, you might pick the guy yelling loudest. But CCT finds the quiet CEO whose single sentence dictated how everyone voted."
- Hallucination behavior → "a people pleaser who never says no"
- Small vs large models → "fewer backup systems" vs "more redundant neural circuits"

**What to look for:** Are there technical concepts left un-analogized? Does the analogy require prior knowledge the audience might not have?

### 5. The "Let's Pause" Technique

When introducing a concept that's essential for understanding what comes next, explicitly pause the narrative flow. This signals "pay attention, this matters."

**Gold standard example:** "Let's pause on this temperature setting for a second because I want to make sure you understand the mechanics here."

**What to look for:** Are there moments where the script introduces a prerequisite concept without flagging its importance? Would a "let me make sure you get this" moment help?

### 6. Walk-Through Experiments as Stories

Don't summarize results — walk the viewer through the experiment step by step so they feel like they're discovering the findings alongside the researchers.

**Gold standard pattern:** The video walks through 4 experiments as mini-narratives:
- Set up the scenario (ask about cat feathers)
- Show expected behavior (AI should correct you)
- Turn the dial (amplify H neurons)
- Reveal the surprising result (AI agrees cats have pink feathers)

Each experiment follows: Setup → Expected → Manipulation → Surprise

**What to look for:** Does the script tell the viewer "researchers found X" (passive summary) or does it walk them through "here's what they did, and here's what happened" (active discovery)?

### 7. Concrete Numbers + Emotional Framing

Don't just cite statistics — frame them emotionally. Make the number *mean* something.

**Gold standard example:** "More than a quarter of the time you ask an advanced model for factual cited information, it's just making stuff up. Think about what that means when you're using these tools for research."

**What to look for:** Are statistics presented as raw numbers, or are they followed by "think about what that means" framing?

### 8. Conversational Second-Person Address

Speak directly to the viewer with "you" language. Anticipate their thoughts with "You might be thinking..." or "You might assume that..."

**Gold standard examples:**
- "You might be thinking that more recent models hallucinate less, right?"
- "You might assume that scaling up the models... would organically solve this issue"
- "I'm sure most of you watching this could think of someone who is always a people pleaser"

**What to look for:** Does the script feel like a lecture or a conversation? Does it anticipate and address viewer objections?

### 9. Scope Management

When a subtopic would derail the main narrative, explicitly acknowledge it and move on. This shows respect for depth without sacrificing pacing.

**Gold standard example:** "Now, of course, there's a lot more nuances and details on how this actually works, but that's beyond the scope of this tutorial."

**What to look for:** Are there tangents that should be acknowledged and deferred? Does the script try to explain everything?

### 10. Structural Signposting

Use clear transitions that tell the viewer where they are in the journey: "First... Next... Now that we've established X, let's look at Y... So those are the four main trials..."

**What to look for:** Can the viewer always tell where they are in the video's arc? Are transitions clear?

## How to Review a Script

When reviewing a script, follow this structure:

### Quick Verdict
One sentence: what's the overall quality level and the single biggest improvement opportunity.

### Score Card (1-5 each)
Rate each principle and give a one-line justification:

| Principle | Score | Note |
|-----------|-------|------|
| Relatability Hook | | |
| Promise + Accessibility | | |
| Context Before Complexity | | |
| Everyday Analogies | | |
| "Let's Pause" Moments | | |
| Experiments as Stories | | |
| Numbers + Emotional Framing | | |
| Conversational Address | | |
| Scope Management | | |
| Structural Signposting | | |

### Top 3 Fixes
The three most impactful changes, each with:
- **The problem** — what's weak and where in the script
- **Why it matters** — what the viewer experiences
- **Suggested rewrite** — a concrete alternative (not just "make it better")

### Line-Level Notes
Specific moments in the script that could be improved, with before/after suggestions. Focus on the weakest 3-5 moments, not every line.
