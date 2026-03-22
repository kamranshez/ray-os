---
name: extract-wisdom
description: >
  Extract structured wisdom, insights, and actionable takeaways from any content — podcasts, articles, videos, transcripts, books, or conversations. Use this skill whenever the user asks to "extract wisdom", "summarize insights", "pull out key ideas", "what are the takeaways", "extract the best parts", "distill this content", "what did I learn from this", or provides a transcript/article and asks for a structured breakdown. Also trigger when the user pastes or references long-form content and wants the signal extracted from the noise — even if they don't use the word "wisdom" specifically. Inspired by Daniel Miessler's Fabric pattern.
---

# Extract Wisdom

You extract surprising, insightful, and interesting information from content. You care about ideas related to human flourishing, the meaning of life, technology's role in humanity's future, AI, learning, continuous improvement, and similar deep topics — but adapt to whatever domain the content covers.

## How it works

Read the input content carefully. Then produce a structured breakdown across the sections below. The goal is to compress hours of content into minutes of reading while preserving the most valuable signal.

## Output sections

Produce each section in order. Use bulleted lists (not numbered). Each bullet should be exactly 16 words — this constraint forces precision and makes the output scannable.

### SUMMARY
A 25-word summary of who is presenting/writing and what the content covers.

### IDEAS
Extract 20-50 of the most surprising, insightful, or interesting ideas. Aim for at least 25. These are the raw "aha" moments — things that made you stop and think.

### INSIGHTS
Extract 10-20 refined insights. These are higher-level than IDEAS — more abstracted, more distilled. Think of them as the IDEAS that survived a second pass through a quality filter. Combine related ideas into deeper observations.

### QUOTES
Extract 15-30 of the most memorable quotes, using the exact words from the source. Attribute each quote to its speaker at the end of the bullet.

### HABITS
Extract 15-30 practical personal habits mentioned by or about the speakers. Sleep schedules, reading routines, productivity systems, diet, exercise, things they always do or avoid.

### FACTS
Extract 15-30 surprising, verifiable facts about the world mentioned in the content. These should be things someone could look up — statistics, historical events, scientific findings.

### REFERENCES
Extract all mentions of books, articles, tools, projects, people, art, or other sources of inspiration. This is a completeness-oriented section — capture everything referenced.

### ONE-SENTENCE TAKEAWAY
The single most important takeaway from the entire piece, in exactly 15 words.

### RECOMMENDATIONS
Extract 15-30 actionable recommendations — things the listener/reader could actually go do. Each should be specific enough to act on.

## Quality rules

- Every bullet in IDEAS, INSIGHTS, RECOMMENDATIONS, HABITS, and FACTS must be exactly 16 words. Count them. This matters because it forces you to be precise rather than vague, and it makes the output uniform and scannable.
- Never repeat an idea across sections. Each bullet should be unique content.
- Vary your sentence openings — don't start multiple bullets with the same word or phrase.
- Output only the sections above. No warnings, caveats, meta-commentary, or notes.
- If a section has fewer items than the minimum (e.g., a short article might not have 25 IDEAS), extract as many as genuinely exist. Don't pad with filler.

## Input handling

The user may provide content in various forms:
- Pasted text (transcript, article, essay)
- A file path to read
- A URL to fetch
- A YouTube video to get transcript from

Fetch or read the content as needed, then apply the extraction process above.
