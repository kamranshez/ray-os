---
name: course-scriptwriter
description: >
  Write full video scripts for online course lessons AND review/critique outlines and
  scripts before recording. Use when Ray asks to "write the script", "plan the video",
  "script this lesson", "flesh this out for recording", "turn this brief into something
  I can record", or references a video brief file. Also trigger when Ray wants feedback
  before filming: "review this script", "check this outline", "is this ready to film",
  "pre-flight check". This is for Agentic Coding School course content — NOT for
  standalone YouTube videos (those use the youtube-scriptwriter skill instead).
---

# Course Scriptwriter

Two modes depending on what Ray needs:

1. **Write mode** — Turn a video brief into a full script Ray can record from
2. **Review mode** — Critique an outline or script before recording, catch pacing and accessibility issues

---

## MODE 1: WRITE — Script from Brief

You'll receive a markdown file (a "video brief") containing:
- Topic and title
- Key concepts to cover
- Competitor quotes and examples to reference
- Cross-links to other videos in the class
- Duration target

Your job: turn that brief into a complete script Ray can record from.

### Script format

```markdown
---
tags: [course, script, {class-name}]
status: draft
lesson: "{chapter}. {title}"
duration: "{target from brief}"
---

## {Lesson Title}

{Opening — 2-3 sentences that set up the problem or context. No hook formula.
Just state what we're doing and why it matters. If this builds on a prior lesson,
reference it: "In the last video we built X. Now we're going to..."}

### {Section Name} ({start}–{end})

{Narration written as spoken word. Conversational, direct, second-person.}

> [SCREEN: description of what's on screen — terminal, UI, file, etc.]

{More narration.}

```code or config blocks shown on screen```

{Continue narration around the code.}

### {Next Section} ({start}–{end})

...

### What's Next

{1-2 sentences bridging to the next lesson in the class. No CTA, no subscribe,
no "like and comment." Just: "Next up, we're going to take this and..." or
"In the next video, we'll build on this by..."}
```

### How to write the narration

Read `references/voice-guide.md` for Ray's specific voice patterns. The core principles:

**Spoken word, not written word.** This is a script for someone talking to a camera
or recording over a screen share. Write how people talk:
- Contractions always ("you're" not "you are", "it's" not "it is")
- Sentence fragments are fine ("Same principle." "That's it." "Done.")
- Thinking out loud ("So the question becomes..." "And here's what's interesting.")
- Conversational connectors ("Now", "So", "And", "But here's the thing")

**Show, don't lecture.** The primary mode is demo — Ray does something on screen
and narrates what's happening. The secondary mode is concept explanation, but even
concepts should be grounded in "here's what that looks like in practice."

Structure most sections as:
1. State the problem or goal (1-2 sentences)
2. Show the solution (demo with narration)
3. Explain why it works (the insight)

**No filler.** Don't pad to hit a duration. If the lesson is 5 minutes of actual
content, write 5 minutes. Don't add "as you can see" or "it's important to note that"
or "let's go ahead and." Just say the thing.

**Use analogies for concepts, not for demos.** When explaining something abstract
(like progressive disclosure or context windows), analogies help. When showing how
to do something, skip the analogy and just show it.

### Screen direction format

Use these callouts inline with narration:

- `> [SCREEN: ...]` — what's visible on screen (terminal, UI, file open in editor)
- `> [TYPE: ...]` — specific text Ray types into Claude or terminal
- `> [SHOW: ...]` — highlight or point to something already on screen
- `> [SPLIT: left — ... | right — ...]` — side-by-side comparison

Don't over-direct. One screen callout per transition is enough. If Ray is typing in
a terminal for 30 seconds, one `[SCREEN: Claude Code terminal]` at the start covers it.

### Handling competitor quotes

The briefs contain quotes from competitor videos. Use these as source material for
concepts, not as attributions. Don't say "as Chase from his YouTube channel says..."
Instead, absorb the insight and express it in Ray's voice. The brief tells you WHAT
to cover. You decide HOW to say it.

Exception: if the brief specifically attributes a quote to a named person (like
"Zack Shapiro"), you can attribute it since it's a real expert, not a competitor.

### Handling cross-links

When the brief says `Cross-link: [[Video Name]] (class)`, reference it naturally:
- "We covered this in the progressive disclosure video" (if same class)
- "If you've watched the Claude Code class, you've seen this" (if different class)
- Don't force references. Only include them when they genuinely help comprehension.

### Timestamp estimation

Estimate timestamps based on these rough rates:
- Pure narration: ~150 words per minute
- Narration over demo: ~120 words per minute (pauses for typing/waiting)
- Code blocks shown on screen: add 10-15 seconds per block

Use ranges like (2:30–4:00) not exact seconds. They're guides for pacing, not
precision timestamps.

### Duration adaptation

Match the duration target from the brief:
- 5-7 min → 3-4 sections, tight. Cut anything that isn't load-bearing.
- 7-10 min → 4-5 sections. Room for one concept explanation + one solid demo.
- 10-15 min → 5-7 sections. Can include a full build demo with iteration.

### Output

Save the script to the same directory as the input brief, with the same filename
but with `-script` appended. For example:
- Brief: `2-1-the-interrogate-skill.md`
- Script: `2-1-the-interrogate-skill-script.md`

---

## MODE 2: REVIEW — Pre-flight check before recording

Review outlines and scripts before recording. Catch issues that hurt comprehension
and retention — especially for non-developer audiences who need more breathing room,
context, and hand-holding than typical dev content provides.

See `references/charles-feedback.md` for the specific audience feedback that drives
these criteria. The short version: Charles's team of experienced C engineers burned
~200 hours each trying to learn from fast-paced tutorial content. Don't make that
mistake.

### Workflow

Read the outline/script fully, then evaluate against each criterion. For each one,
give a **verdict** (Pass / Needs Work / Missing) and a **specific note** with a
concrete fix — not just what's wrong, but what to do about it.

#### A. Problem-First Framing

The video should open by making the viewer understand *why* this matters to them
before showing *how* it works.

- Is there a real-world problem or pain point stated early?
- Would a non-developer understand why they should care within the first 30 seconds?
- Or does it jump straight into feature/tool description?

**Good:** "You deploy your app, close your laptop, and wake up to find it's been down for 6 hours. Here's how to make that impossible."

**Bad:** "/loop schedules any prompt or slash command to run on a recurring interval."

#### B. Jargon & Accessibility

Flag terms that assume prior knowledge without explanation. The audience includes
people who've never used a terminal.

Watch for: unexplained acronyms (CI, PR, CLI, MCP, SDK), tool-specific terms used
without context (subagents, hooks, skills, slash commands), developer shorthand
("spin up", "bootstrap", "scaffold").

For each flagged term, suggest a brief inline definition or analogy. The fix isn't to
remove technical terms — it's to define them on first use.

#### C. Pacing & Breathing Room

Estimate whether the outline packs too much into its stated duration.

Check for: sections that try to cover too much in too little time, missing transition
moments, spots where the viewer would need to pause and rewind.

**Suggest specific spots** where Ray should pause or slow down. e.g., "After showing
the /loop command running, hold on the terminal output for 3-4 seconds so viewers
can read it."

#### D. Visual Lingering

Screens and visuals should stay visible long enough for viewers to actually read and
process them.

- Flag each moment where code, output, or diagrams are shown — note it needs at least 3-5 seconds of hold time.
- Suggest spots where a visual aid should be added but isn't mentioned.

#### E. Signposting & Section Structure

Videos need clear markers so viewers can navigate and mentally organize content.

- Are there titled sections or clear topic transitions?
- Would a viewer know "we're done with setup, now we're building"?
- Suggest title cards or verbal signposts where missing.

#### F. Implementation Walkthrough

The video should show actual steps, not just describe what's possible.

- Does the outline include concrete steps someone could follow along with?
- Is there a clear "do this, then this, then this" flow?
- Or is it a feature showcase without showing the actual process?

#### G. The Payoff

The video should end by showing the solution actually working.

- Is there a moment where the viewer sees the result in action?
- Does the outline end with a clear, repeatable takeaway?

### Review output format

```
## Script Review: [Video Title]

**Overall assessment:** [1-2 sentence summary — ready to film or needs work?]

**Duration check:** [Does the content fit the stated duration?]

### Criteria

| Criterion | Verdict | Notes |
|-----------|---------|-------|
| Problem-First Framing | Pass/Needs Work/Missing | ... |
| Jargon & Accessibility | Pass/Needs Work/Missing | ... |
| Pacing & Breathing Room | Pass/Needs Work/Missing | ... |
| Visual Lingering | Pass/Needs Work/Missing | ... |
| Signposting | Pass/Needs Work/Missing | ... |
| Implementation Walkthrough | Pass/Needs Work/Missing | ... |
| The Payoff | Pass/Needs Work/Missing | ... |

### Priority fixes (before filming)

1. [Most important fix]
2. [Second most important]
3. [Third if applicable]

### Suggested revisions

[Rewrite or annotate specific sections. Show before and after.]
```
