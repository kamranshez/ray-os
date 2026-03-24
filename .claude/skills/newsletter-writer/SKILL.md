---
name: newsletter-writer
description: Write personal newsletters in a conversational, essay-style format inspired by Ali Abdaal's style. Use when the user wants to write a newsletter issue, draft an email to their list, write a LifeNotes-style essay, or asks for help with newsletter writing. Triggers on requests like "write a newsletter", "draft a newsletter about...", "help me write my weekly email", "newsletter style", or when the user provides a topic and wants it turned into a newsletter format.
---

# Newsletter Writer

Write newsletters that feel like a friend talking to you over coffee, not a blog post or corporate email.

## Style DNA

### Voice
- First person, conversational, slightly self-deprecating
- Talk TO the reader, not AT them ("you might be thinking..." / "I know what some of you are probably thinking")
- Admit imperfection freely ("If I'm being honest..." / "I'm not saying I've got this perfectly figured out")
- Use casual asides and parentheticals liberally
- British English spelling (optimising, realised, colour)

### Structure Pattern
1. **Warm open** - "Hey friends" or "Hey [name]" + brief personal update or context about what prompted the topic (1-2 short paragraphs)
2. **Bridge to the idea** - Casually introduce the core concept from personal experience, not from theory ("And that's the idea of..." / "there is something I did want to share this week")
3. **The meat** - Explore the idea through personal stories and specific examples. Use the "here's what happened to me" -> "here's the principle" -> "here's how it applies to you" arc
4. **Reframe or insight** - The key takeaway, often presented as a reframe of a common assumption ("The big reframe that changed everything for me was this:")
5. **Practical application** - Actionable prompt, challenge, or numbered list of small things to try
6. **Warm close** - "Have a great week" / "Talk soon" + sign-off ("Ali xx")
7. **P.S.** - Optional postscript with a teaser, plug, or aside

### Paragraph Style
- Short paragraphs (1-3 sentences typical)
- Lots of line breaks between thoughts
- Long flowing sentences broken by dashes and commas, creating a spoken rhythm
- Use "And" and "But" to start sentences frequently - it creates momentum
- Em dashes for asides and pivots
- Ellipsis (...) for trailing thoughts and pauses

### Rhetorical Moves
- **Anticipate objections**: "Now I know what some of you are probably thinking..." then address them directly
- **Self-aware tangents**: "Now, I don't bring this up as a shameless plug... but rather because..."
- **Honest vulnerability**: Share real struggles, not curated ones ("I often get to the weekend thinking: 'hmm I should kinda be writing an issue... but I feel like I just don't have anything useful or interesting to share lol'")
- **Framework drops**: Introduce a concept casually, not academically ("There's a framework in operations called the Theory of Constraints, which is a fancy way of saying...")
- **Specific details over generalities**: Name the tools, the times, the places ("I was spending hours in Final Cut" not "I was spending too long editing")
- **Callback to opening**: Circle back to the personal story that started the email

### What to AVOID
- Listicle format (unless the whole email is specifically about a list, like "22 habits")
- Subheadings within the body (the email should flow like a single conversation)
- Corporate/marketing tone
- Starting with the lesson - always start with the personal context
- Wrapping up too neatly - leave some roughness
- Over-polished prose - this should read like it was written in one sitting (even if it wasn't)
- NEVER call the Agentic Coding School a "course" or "class" - always refer to it as a "masterclass"

### Emotional Texture
- The best issues have a specific emotional undertone: wonder, slight anxiety, gentle humor, quiet satisfaction
- Not every issue needs to be "useful" - sometimes the value is just in the honest sharing
- End with warmth, not a hard sell

## Video Thumbnail with Play Button

When the newsletter references a video (marked with `[VIDEO THUMBNAIL + LINK]`), generate a clickable-looking thumbnail image with a play button overlay. This makes the email feel more engaging — readers see what looks like an embedded video.

Run the bundled script:
```bash
python3 scripts/add-play-button.py <input_thumbnail> [output_path]
```

- Takes any thumbnail image (PNG, JPG, WEBP)
- Overlays a YouTube-style semi-transparent play button (dark circle + white triangle)
- Adds a subtle dark gradient at the bottom
- If no output path given, saves as `<name>-play.<ext>` next to the original

If the user provides a thumbnail image, run this automatically. If not, ask if they have one. The output image should replace the `[VIDEO THUMBNAIL + LINK]` placeholder in the final newsletter.

## Output Format

When presenting a newsletter draft, always provide options so Ray can mix and match. The typical input is a video transcript that needs to be turned into a short, video-redirect newsletter (not a full essay retelling the video).

### Always generate:

**5 Subject Lines** — varied angles on the same topic. Mix these approaches:
- Mystery/curiosity gap ("I found something hidden in...")
- Direct statement ("Claude Code dreams now")
- Problem/pain point ("Your AI agent is sleep-deprived")
- Quotable moment from the content (something surprising the reader said/found)
- Casual/conversational ("...and I had no idea why")

**5 Preview Snippets** — the text that shows below the subject line in email clients. Keep to one sentence. Should complement the subject line, not repeat it. Mix between teasing the content, stating a surprising fact, and creating intrigue.

**3 Newsletter Variations** — each with a different opening hook/angle. Keep them short (video-redirect format). Label each with its hook strategy so Ray can quickly scan:
- e.g., "Mystery/Discovery Hook", "Problem-First Hook", "Human Analogy Hook"
- Each variation should be a complete, sendable draft — not just the opening paragraph
- All variations share the same closing (warm close + question + sign-off)

Present all of this in one go so Ray can pick and combine (e.g., Subject Line 3 + Snippet 1 + Variation B).

## Workflow

1. Receive the topic — usually a video transcript, sometimes a seed idea
2. Read `references/examples.md` to calibrate tone and structure
3. Identify 3 distinct angles/hooks from the content
4. Draft 3 complete newsletter variations (video-redirect format by default)
5. Generate 5 subject lines and 5 preview snippets
6. Read through for conversational flow — if any sentence sounds like a blog post, rewrite it
7. Run the humanizer skill on the drafts to catch AI-sounding patterns
8. If the newsletter references a video, run `scripts/add-play-button.py` on the thumbnail
9. Present everything together for Ray to mix and match

## Examples

See `references/examples.md` for 5 full Ali Abdaal newsletters that demonstrate this style in action. Read this file when writing to calibrate tone and structure.
