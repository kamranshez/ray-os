---
name: newsletter-writer
description: Write personal newsletters in a conversational, essay-style format inspired by Ali Abdaal's style. Use when the user wants to write a newsletter issue, draft an email to their list, write a LifeNotes-style essay, or asks for help with newsletter writing. Triggers on requests like "write a newsletter", "draft a newsletter about...", "help me write my weekly email", "newsletter style", or when the user provides a topic and wants it turned into a newsletter format.
---

# Newsletter Writer

Write newsletters that feel like a friend talking to you over coffee, not a blog post or corporate email.

## Hard Rule: No em dashes or en dashes

Never use em dashes (—) or en dashes (–) anywhere in newsletter output. Use commas, periods, parentheses, "like", "such as", or rewrite the sentence instead.

This rule overrides anything else in this skill, including the Ali Abdaal style calibration in `references/examples.md` which uses em dashes liberally. The examples are for tone and rhythm, not punctuation. Ray doesn't like dashes in his writing and flagged this specifically, so treat it as a hard constraint.

If you're tempted to use a dash for an aside or pivot, that's usually a sign the sentence wants to become two sentences, or that the aside belongs in parentheses. Both options preserve the spoken rhythm without the dash.

**Before presenting any draft, mechanically scan the output for `—` and `–` and remove every instance.** This is non-optional. In past sessions, em dashes kept slipping through during iterative edits because "I know the rule" isn't enough. Run a literal search.

## Style DNA

### Voice
- First person, conversational, slightly self-deprecating
- Talk TO the reader, not AT them ("you might be thinking..." / "I know what some of you are probably thinking")
- Admit imperfection freely ("If I'm being honest..." / "I'm not saying I've got this perfectly figured out")
- Use casual asides and parentheticals liberally
- British English spelling (optimising, realised, colour)
- British punctuation inside quotes: commas and periods go OUTSIDE the closing quote, not inside. Write `"failing tests", the moment` not `"failing tests," the moment`.

### Structure Pattern
1. **Warm open**, "Hey friends" or "Hey [name]" plus a brief personal update or context about what prompted the topic (1-2 short paragraphs)
2. **Bridge to the idea**, casually introduce the core concept from personal experience, not from theory ("And that's the idea of..." / "there is something I did want to share this week")
3. **The meat**, explore the idea through personal stories and specific examples. Use the "here's what happened to me" then "here's the principle" then "here's how it applies to you" arc
4. **Reframe or insight**, the key takeaway, often presented as a reframe of a common assumption ("The big reframe that changed everything for me was this:")
5. **Practical application**, actionable prompt, challenge, or numbered list of small things to try
6. **Warm close**, "Have a great week" or "Talk soon" plus sign-off ("Ray")
7. **P.S.**, optional postscript with a teaser, plug, or aside

### Paragraph Style
- Short paragraphs (1-3 sentences typical)
- Lots of line breaks between thoughts
- Long flowing sentences broken by commas, creating a spoken rhythm (no dashes, see the hard rule above)
- Use "And" and "But" to start sentences frequently, it creates momentum
- Parentheses for asides, or split into a second sentence
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
- Starting with the lesson, always start with the personal context
- Wrapping up too neatly, leave some roughness
- Over-polished prose, this should read like it was written in one sitting (even if it wasn't)
- NEVER call the Agentic Coding School a "course" or "class", always refer to it as a "masterclass"

### Emotional Texture
- The best issues have a specific emotional undertone: wonder, slight anxiety, gentle humor, quiet satisfaction
- Not every issue needs to be "useful", sometimes the value is just in the honest sharing
- End with warmth, not a hard sell

## Video Thumbnail with Play Button

**For any video-redirect newsletter, a video thumbnail is mandatory, not optional.** Every draft in the output must include a `[VIDEO THUMBNAIL + LINK]` placeholder inside the body (typically after the 2nd or 3rd paragraph, before the "here's what I mean" elaboration). If the user hasn't supplied a thumbnail image, ask for one before presenting the drafts. Do not produce a video-redirect newsletter without a thumbnail, it's the CTA of the entire email.

When you have a thumbnail path, run the bundled script to overlay a YouTube-style play button:
```bash
python3 scripts/add-play-button.py <input_thumbnail> [output_path]
```

By default the script resizes the output to 1280×720 at JPEG quality 80, which produces a ~100KB file suitable for email. You can override with `--max-width` and `--quality` if needed, but the defaults are usually correct.

- Takes any thumbnail image (PNG, JPG, WEBP)
- Overlays a YouTube-style semi-transparent play button (dark circle + white triangle)
- Adds a subtle dark gradient at the bottom
- Resizes to max 1280px wide by default (preserves aspect ratio)
- If no output path given, saves as `<name>-play.<ext>` next to the original

## CTA Questions

CTA questions close the email with a reply prompt. The framing depends on the newsletter type:

**For feature-announcement / product-launch newsletters** (where the reader will obviously adopt the feature), CTAs must be **forward-looking**. Assume adoption. Ask about what they'll do *with* the feature, not how they were handling things *before* it.
- Good: "What's the first thing you're going to point /monitor at? Dev server, test suite, Vercel deploy, or something weirder?"
- Good: "What would you want Claude to silently watch for you in the background? The weirder the use case, the more interested I am."
- Bad: "How are you currently watching long-running things in Claude Code? /loop, backgrounded shell, or something custom?" (Assumes non-adoption of the feature you just announced, which is wrong.)

**For evergreen / opinion / reflection newsletters**, the traditional "share your experience" framing still works.
- Good: "How do you handle Mondays when the week ahead feels heavy? Reply and let me know."

Always make CTAs specific to the topic, never generic "what do you think?" prompts.

## Output Format

The typical input is a video transcript that needs to be turned into a short, video-redirect newsletter (not a full essay retelling the video). The output is 5 body variations plus a global pool of 10 subject lines and 10 preview snippets. Ray picks one body, one subject, and one preview, and copies the trio.

### What to generate

**5 Newsletter Variations** (the bodies), each with a different opening hook/angle. Label each with its hook strategy so Ray can scan quickly. Each variation is a complete, sendable draft (not just the opening paragraph), and each one must include the `[VIDEO THUMBNAIL + LINK]` placeholder in the body. Hook strategies to mix between:
- Mystery/Discovery Hook
- Problem-First Hook
- Stealth Launch / Under-the-Radar Hook
- Metaphor Hook
- Primitive / Building Block Hook
- Personal Story Hook

**10 Subject Lines** (global pool). One shared set of 10 subject line options that can plausibly pair with any of the 5 body variations. Aim for a spread of angles so there's at least one strong subject for each body's hook, rather than five that only fit one variation. Mix between mystery/curiosity, direct statement, problem/pain point, quotable moment, casual/conversational, and stealth-launch framings.

**10 Preview Snippets** (global pool). One shared set of 10 one-sentence tease lines that complement the subjects without repeating them. Same logic as the subjects, these should be hook-agnostic enough that Ray can pair any preview with any body.

**5 CTA Questions.** Close the email with a reply prompt. Apply the CTA framing rules above (forward-looking for feature announcements, experience-sharing for evergreen).

### Why a global pool instead of per-variation subjects

Earlier versions of this skill paired 5 subjects and 5 previews *per variation*, which meant subjects were tightly coupled to the body's hook. That forced a rigid mental model (pick a body first, then pick from its 5 subjects) and cluttered the email reading view with picker UI. Ray preferred moving subjects and previews onto a dedicated "Headlines" page with one global pool of each, so the email view stays clean and he can mix any subject with any body. When generating the 10, write them broad enough that most of them pair sensibly with at least 2-3 of the 5 body variations.

### Present everything together

When presenting in markdown, write the 5 bodies first, then a "Subject line options" list of 10, then a "Preview snippet options" list of 10, then the CTA questions. When presenting in the HTML viewer, the bodies, subjects, and previews all flow into the template (see the HTML Viewer section). The viewer puts subjects and previews on a dedicated "Headlines" tab so they don't clutter the email page.

## HTML Viewer Mode (Opt-In)

When Ray asks to see the variations "in an HTML thing", "in a viewer", "as HTML", or similar, render the 5 newsletter variations using the bundled Gmail-style template at `references/gmail-viewer-template.html`. This is faster to scan than a wall of markdown.

**How to use:**
1. Read `references/gmail-viewer-template.html` to see the structure
2. Copy it to a user-accessible location (e.g., `<topic>-newsletter-options.html` in the working directory)
3. Replace the `__VARIATIONS_JSON__` placeholder with an array of 5 variation objects, each containing:
   - `hook`: the hook strategy label (e.g., "Polling Is Dead")
   - `body`: an array of paragraph strings (use `"[THUMBNAIL]"` as a paragraph entry to mark where the video thumbnail goes)
4. Replace the `__SUBJECTS_JSON__` placeholder with an array of exactly 10 subject line strings (the global pool)
5. Replace the `__PREVIEWS_JSON__` placeholder with an array of exactly 10 preview snippet strings (the global pool)
6. Replace `__THUMBNAIL_PATH__` with the relative path to the play-button thumbnail
7. Replace `__VIDEO_URL__` with the YouTube URL
8. Replace `__TOPIC__` with a short topic label for the page title
9. `open` the resulting HTML file

The viewer has three modes in the topbar: **Inbox** (default, shows the active body variation in a Gmail-style reading pane), **Headlines** (the dedicated page for the 10 subjects + 10 previews, two columns side by side), and **Compare all** (horizontal scroll of all 5 body variations side by side). Keyboard shortcuts: `1`-`5` jump to a variation, `i` / Escape returns to inbox, `h` opens Headlines, `c` opens Compare.

Subject and preview selection is global (one active pair), so whatever Ray picks on the Headlines tab instantly applies to every body variation's header in the inbox and compare views. This keeps the email reading page clean while still letting him mix and match pairs in one click.

## Appendix / Reference Sections

Some newsletters include bonus content below the sign-off, like system prompts, code snippets, checklists, or reference material the reader can bookmark. When the content lends itself to this:

- Add a `---` divider after the sign-off
- Use a clear heading (e.g., "Ultraplan System Prompts Variants")
- Keep the bridge sentence in the body casual: "I've included X below if you want to do the same"
- Format reference material cleanly with code blocks, numbered sections, or bold labels
- Don't repeat content from the body, the appendix is supplementary, not a summary

## Workflow

1. **Fetch the transcript if needed.** If the user provided a YouTube URL and no local transcript exists in `socials/youtube/transcripts/`, fetch one via `python3 ~/.claude/skills/supadata/scripts/supadata.py transcript <video_id>`. Don't assume the transcript is already on disk, check first.
2. Read `references/examples.md` to calibrate tone and structure (remember to ignore its em dash usage, see the hard rule at the top of this file)
3. Identify 5 distinct angles/hooks from the content
4. Draft 5 complete newsletter variations (video-redirect format by default). Every variation must include the `[VIDEO THUMBNAIL + LINK]` placeholder in the body.
5. Generate 10 subject lines, 10 preview snippets, and 5 CTA questions. Use the CTA framing rules: forward-looking for feature announcements, experience-sharing for evergreen.
6. **Structural-consistency pass.** Re-read every variation looking for iterative-edit artifacts: numbered promises that don't match what follows ("two bad options" then only listing one), dangling sentence fragments that were truncated mid-edit, pronouns without clear antecedents, and paragraphs that contradict earlier paragraphs. This catches the kinds of drift that happen when you rewrite parts of a draft.
7. **Dash scan.** Literally search every variation for `—` and `–` and remove them. Replace with commas, periods, parentheses, or a rewrite. Do this even if you "know" you didn't add any, they sneak in.
8. Read through for conversational flow. If any sentence sounds like a blog post, rewrite it.
9. **Handle the thumbnail.** Ask the user for a thumbnail image path if one wasn't provided (remember, thumbnails are mandatory for video-redirect newsletters). Then run `scripts/add-play-button.py` on it, which auto-resizes to 1280×720 at quality 80.
10. Present everything together for Ray to mix and match. If Ray asks for HTML/viewer mode, render via `references/gmail-viewer-template.html`.
11. After the email is sent, ask Ray to paste the final version back so it can be stored in `references/examples/` for future reference and performance tracking.

## Examples

See `references/examples.md` for 5 full Ali Abdaal newsletters that demonstrate this style in action. Read this file when writing to calibrate tone and structure, but remember: **ignore its em dash usage**. The examples are for voice, rhythm, and structure only. Ray's hard rule against dashes overrides anything you see in those examples.
