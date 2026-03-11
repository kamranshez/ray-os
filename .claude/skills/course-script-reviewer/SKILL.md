---
name: course-script-reviewer
description: Review video outlines and scripts before recording to catch pacing, accessibility, and structure issues. Use this skill whenever the user has a video outline or script they want reviewed before filming, when they ask to "review this script", "check this outline", "is this ready to film", or when they want feedback on a course video's structure. Also trigger when the user is about to film a video and wants a pre-flight check, or when they paste a video outline and ask for improvements. Works on both sparse bullet-point outlines and detailed scripts.
---

# Course Script Reviewer

Review video outlines and scripts before recording. Catch issues that hurt comprehension and retention — especially for non-developer audiences who need more breathing room, context, and hand-holding than typical dev content provides.

## Why this matters

Most coding tutorial creators (including Ray historically) optimize for information density — packing maximum content into minimum time. This works for experienced developers watching at 2x speed, but alienates the growing audience of non-traditional learners: engineers from other domains (embedded C, hardware), managers evaluating tools, and newcomers climbing the first rungs of the learning ladder.

The goal isn't to dumb things down — it's to make the same high-quality content *accessible* by adding structure, pacing, and context that lets viewers actually absorb what's being shown.

## Workflow

### 1. Read the outline/script

The user will provide one of:
- A video outline from `projects/agentic-coding-school/to-film/`
- A pasted script or outline
- A path to a markdown file

Read it fully before evaluating.

### 2. Run the review

Evaluate the outline against each criterion below. For each one, give a **verdict** (Pass / Needs Work / Missing) and a **specific note** explaining what to fix. Don't just flag problems — suggest concrete fixes.

#### A. Problem-First Framing

The video should open by making the viewer understand *why* this matters to them before showing *how* it works.

- Is there a real-world problem or pain point stated early? (e.g., "I'm buried in emails", "Our deploy broke at 2am and nobody noticed")
- Would a non-developer understand why they should care within the first 30 seconds?
- Or does it jump straight into feature/tool description?

**What good looks like:** "You deploy your app, close your laptop, and wake up to find it's been down for 6 hours. Here's how to make that impossible."

**What bad looks like:** "/loop schedules any prompt or slash command to run on a recurring interval."

#### B. Jargon & Accessibility

Flag terms that assume prior knowledge without explanation. The audience includes people who've never used a terminal — they need "command line terminal", not "CLT".

Watch for:
- Unexplained acronyms (CI, PR, E2E, CLI, MCP, SDK)
- Tool-specific terms used without context (subagents, hooks, skills, slash commands)
- Assuming viewers know what a terminal, repo, or deployment is
- Using developer shorthand ("spin up", "bootstrap", "scaffold")

For each flagged term, suggest a brief inline definition or analogy. The fix isn't to remove technical terms — it's to define them on first use.

#### C. Pacing & Breathing Room

Estimate whether the outline packs too much into its stated duration. A 1-4 minute video with 6 dense bullet points probably needs either more time or fewer points.

Check for:
- Sections that try to cover too much in too little time
- Missing transition moments between concepts
- Spots where the viewer would need to pause and rewind
- Any indication of natural pauses or "let that sink in" moments

**Suggest specific spots** where Ray should pause, slow down, or let a visual linger. e.g., "After showing the /loop command running, hold on the terminal output for 3-4 seconds so viewers can read it."

#### D. Visual Lingering

Screens and visuals should stay visible long enough for viewers to actually read and process them.

- Are there moments where code, output, or diagrams are shown? Flag each one and note that it needs at least 3-5 seconds of hold time.
- If excalidraw images are referenced, note that Ray should talk through them slowly rather than flashing past.
- Suggest spots where a visual aid *should* be added but isn't mentioned.

#### E. Signposting & Section Structure

Videos need clear markers so viewers can navigate and mentally organize the content.

- Are there titled sections or clear topic transitions?
- Would a viewer know "we're done with setup, now we're building" or "this is the result"?
- Suggest title cards or verbal signposts where they're missing. e.g., "Add a section title here: 'Setting it up' before the implementation steps."

#### F. Implementation Walkthrough

The video should show actual steps, not just describe what's possible. Charles's key insight: "Almost no one provides this level of detail or hand-holding."

- Does the outline include concrete implementation steps someone could follow along with?
- Is there a clear "do this, then this, then this" flow?
- Or is it a feature showcase ("you can do X, Y, Z") without showing the actual process?
- Is the technical context explicit? (Which OS, which terminal, what needs to be installed first?)

#### G. The Payoff

The video should end by showing the solution actually working — not just explaining that it works.

- Is there a moment where the viewer sees the result in action?
- Is there enough time allocated to show the working result (not just a flash)?
- Does the outline end with a clear, repeatable takeaway?

### 3. Output the review

Format the review as:

```
## Script Review: [Video Title]

**Overall assessment:** [1-2 sentence summary — is this ready to film or does it need work?]

**Duration check:** [Does the content fit the stated duration? Suggest adjusting if not.]

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

1. [Most important fix — the one thing that would most improve comprehension]
2. [Second most important]
3. [Third if applicable]

### Suggested revisions

[Rewrite or annotate specific sections of the outline with improvements. Show the before and after so Ray can see exactly what changed and why.]
```

### 4. Cross-reference (optional, for course videos)

If reviewing a course video from `projects/agentic-coding-school/to-film/`:
- Check the frontmatter for `duration`, `batch`, `class`, and `chapter`
- If the duration is "1-4 min", flag any outline that looks like it needs more than 4 minutes to cover properly with good pacing
- If the video is in the "workflows" class, hold it to a higher standard on problem-first framing and implementation walkthrough — these are specifically meant to show real-world usage

## Reference: Charles's Principles

These come from direct audience feedback (Charles Bell, a team lead training C engineers on modern AI tools). His team burned ~200 hours each trying to learn from fast-paced AI tutorial content. Key quotes:

- "We have not moved forward with a purchase yet because my team found it impossible to absorb the information without pausing 10 to 20 times per video"
- "The lack of 'breathing space' and the speed at which screens flash by robs the experience of any joy"
- "Almost no one provides this level of detail or 'hand-holding,' which is exactly what is needed to get people onto the first few rungs of the learning ladder"
- "Most videos just throw 'agents' and 'skills' at the viewer but never engage in the paired programming that walks someone through the process"

See `references/charles-feedback.md` for the full email thread.
