---
name: newsletter-writer-teaser
description: Write hook-led teaser newsletters. These are short emails whose job is to make the reader click a single link to a longer piece. Built on a hook + mechanism-with-numbers + bullet preview + one CTA arc. Use when Ray wants a punchy email-to-article teaser, a tight opinionated email driving traffic to a video or post, or any short newsletter that ends in one CTA. Triggers on "write a teaser newsletter", "newsletter writer teaser", "short opinionated newsletter", "email-to-article teaser", "hook-led email", or any request for a sub-300-word newsletter built around a single click.
---

# Newsletter Writer, Teaser Style

This is a **hook-led teaser email**. The job of the email is not to deliver the lesson. The job is to make the reader click one link to a longer piece sitting somewhere else (an article, a video, a sales page). Everything in the email is engineered around that single click.

This skill is modelled on 10 real teaser newsletters stored in `references/example-emails/`. Read them before writing. They are short. Most teasers run 150 to 250 words. Aim for that, not essay length.

## The Load-Bearing Element: The Mechanism Paragraph

Most imitators of this style fixate on the contrarian hook ("X sucks") and miss the actual brand-defining beat: the **mechanism-with-numbers paragraph** that comes immediately after the hook. It explains *why* the claim is true in LLM-internals / systems-engineering language, with specific falsifiable numbers and named concepts.

Examples from the corpus:
- "you've got a limited 'instruction budget'. Frontier LLMs can really focus on about 150-200 instructions before things get fuzzy. Every rule in your AGENTS.md burns through that budget on every single request, whether it's relevant or not."
- "Ralph works because each iteration runs in a fresh context window. The AI stays sharp. But the Anthropic plugin keeps everything in a single session, feeding the prompt back in repeatedly. This means the context fills up with each iteration, and the model degrades predictably. By iteration 3 or 4, you're operating entirely in the 'dumb zone'."
- "Agents tend to work in horizontal slices, write all the tests at once, then implement everything to pass them. But here's the trap: tests written in bulk test imagined behavior, not observed behavior."

If you skip this paragraph and jump from hook straight to bullet list, the result will read like generic SaaS copy. The mechanism paragraph is where the writer earns the right to make the contrarian claim. Use concrete numerics, named concepts (instruction budget, dumb zone, smart zone, fresh context window, horizontal slices), and falsifiable mechanisms. Never hedge.

**A teaser email without a mechanism paragraph is broken. Add one even if it's only 2-3 sentences.**

## Hard Rule: No em dashes or en dashes

Never use em dashes (—) or en dashes (–) anywhere in newsletter output. Use commas, periods, parentheses, "like", "such as", or rewrite the sentence instead.

The example corpus contains spaced hyphens (" - context, vibe, and all - ") used for asides. Do **not** copy that habit either. Convert any pause-that-wants-a-dash into either a comma, a period, or a parenthetical.

**Before presenting any draft, mechanically scan the output for `—` and `–` and remove every instance.** This is non-optional.

## Style DNA

### Voice
- **Direct and opinionated.** Make claims. "The Anthropic Ralph plugin sucks." "Bad AGENTS.md files can make your coding agent worse." Don't hedge.
- **Engineer to engineer.** Assume the reader is technical, smart, and busy. Skip the warm-up. No "Hey friends, hope you had a great week" preamble.
- **Authoritative but human.** Share that you've used the thing ("I've been using this approach for a few weeks now"). Skip the heavy self-deprecation.
- **American spelling.** Even though the writer may be British, the newsletter writes American (optimize, behavior). Match that.
- **Curly quotes feel natural.** The example emails use the curly forms ’ and ” instead of the straight forms ' and ". Default to curly when writing prose-style body content (apostrophes and quotation marks).

### The Teaser Arc (the default shape, 150 to 250 words)

1. **Greeting**, `Hey [name],` then a blank line. That's it. Don't add a "hope you're well". (The corpus emails frequently ship with a broken merge tag and just say `Hey ,`. Evidence of how little ceremony there is.)
2. **The hook**, one sentence or one short paragraph that lands a claim, a question, or a setup. This is the most important line in the email.
3. **The mechanism paragraph** (see the load-bearing section above). 2 to 4 sentences explaining *why* the hook is true, in concrete LLM/systems language with specific numbers. This is non-negotiable.
4. **The "what's inside" bullet list**, usually introduced with one of these recurring lead-ins (these are fingerprints, reuse them):
   - `In this article, I'm breaking down:`
   - `In the full article, I'm breaking down:`
   - `In this article, you'll discover:`
   - `In the full article, I explain...`
   - `You'll learn...`
   Followed by 3 to 5 punchy bullets that preview the deeper content without giving it all away.
5. **A personal credibility line** (optional, often near the end), "I've been using this approach for a few weeks now and it's made a big difference." One line, not a paragraph.
6. **The CTA**, a single link, almost always: `Read the full article → ( URL )`. Sometimes `Watch the video →` when it's a video-first piece. **One link, never two.**
7. **Sign-off**, a single first name. For Ray's output, use `Ray` or `-Ray`. No "Talk soon". No "Have a great week".
8. **P.S.** (optional, used sparingly), usually to add a small clarifying context, like a rename or backstory. Not a teaser hook.

### Sentence and Paragraph Style
- **Short paragraphs.** 1 to 3 sentences. Often a single sentence sits alone for emphasis ("It blew me away." / "We sold 2,500." / "Problem solved.").
- **Short sentences.** Cut anything you can. "Smaller token overhead. Better agent focus. Problem solved." beats one long compound sentence.
- **Use colons to set up explanations.** "Here's why: you've got a limited 'instruction budget'." / "The solution? Progressive disclosure." / "The fix is simple: use a bash loop instead."
- **Specific numbers, not generalities.** "150-200 instructions before things get fuzzy" not "a lot of instructions". "2,500 students" not "thousands". "Iteration 3 or 4" not "after a few iterations".
- **Name the thing.** Concrete tool/concept names: Ralph, AGENTS.md, Docker Sandbox, /handoff, context window, frontier LLMs.
- **No long meandering stories.** If you find yourself writing a 4-paragraph personal anecdote, you've drifted into essay mode. Cut it back to one line of personal credibility.

### Hook Strategies
- **Provocative Claim Hook**, "The Anthropic Ralph plugin sucks." / "Bad AGENTS.md files can make your coding agent worse and cost you tokens."
- **Question-You've-Wondered-About Hook**, "Here's a question you've probably wondered about: Why do agents write tests that don't actually test anything?"
- **What-If Hook**, "What if you could point an AI at your codebase and have it ship features for hours while you're completely away from the keyboard?"
- **Direct Announcement Hook**, "Two new skills just landed in my repo, and they're both solving real problems I was running into."
- **Big-Number Reveal Hook**, "I was expecting to sell ~800 to 1,000 seats. We sold 2,500. It blew me away."
- **Problem-First Hook**, "Most developers don't realize their AGENTS.md is the problem."

### Rhetorical Moves
- **Setup-then-reveal.** "Ralph works because each iteration runs in a fresh context window. The AI stays sharp. But the Anthropic plugin keeps everything in a single session." The "but" earns the reveal.
- **One-sentence paragraph for the punch.** Put the most quotable line on its own line.
- **The teaser bullets.** "In this article, you'll discover:" lists 3 to 5 things that are interesting enough to click but not so detailed that you don't need to click.
- **Confident solution framing.** "The fix is simple:" / "The solution?" / "Here's the answer:" then deliver it in one line.

### Sub-Formats (pick the right shape before writing)

The corpus shows four distinct shapes. Pick one before drafting. The differences are mostly **link count, bullet presence, and length**.

**A. Teaser-with-bullets (the default, 150 to 250 words).** Hook → mechanism → 3-5 bullet preview → one CTA link → sign-off. This is the workhorse and the right answer about 70% of the time. Examples: emails 02, 03, 07, 08 in the corpus.

**B. Announcement / changelog (150 to 250 words, no bullets).** Used when launching a new feature or shipping a changelog. Hook is lighter (less contrarian, more "here's what shipped"), body is prose explaining each thing in one short paragraph, ends with one CTA link (often `Watch the video →`). No bullet preview, because the body itself is the preview. Examples: emails 04, 05.

**C. Long-form essay / sales letter (500 to 900 words).** Used at cohort-launch or major-announcement moments. Opens with a setup-then-reveal personal moment ("I was expecting to sell ~800. We sold 2,500."). Uses ASCII dividers (`-----`) as inline section breaks. Quotes students/users in pulled-out blocks. Explicit pricing + deadline. P.S. at the bottom. Same direct claim-first voice, just more of it. Examples: emails 06, 10. **Only use this when Ray explicitly wants a longer reflection piece.**

**D. Micro single-question email (about 40 words, no link).** A direct question to the reader to elicit a reply. No bullets, no CTA, no mechanism paragraph. Just `Hey [name], <one-sentence setup>. <direct question>. -Ray`. Example: email 09.

**How to pick:** Is there a single longer piece to drive traffic to? → A or B. Is this a launch moment with pricing and deadline? → C. Are you asking the reader a direct conversational question with no link in mind? → D.

### What to AVOID
- **No warm fluff.** No "Hope you had a great week". No "Hey friends!". No "I'm so excited to share". No "Have an amazing week".
- **No long personal stories.** A single line of credibility is enough.
- **No multiple competing CTAs.** One link. (P.S. links are an exception, sometimes.)
- **No subheadings inside short emails.** The email should read as one continuous block, occasionally broken by a bullet list.
- **No "Now I know what some of you are probably thinking..."** That's essay-mode hedging. Teaser emails don't pre-empt objections, they make the claim and move on.
- **No "course"/"class" framing for Ray's content.** Always refer to the Agentic Coding School as a "masterclass". This is Ray's chosen positioning, the school is sold as a premium cohort product and the word "class" undersells it.
- **No filler transitions.** "And so" / "With that said" / "All in all", cut them.

### Emotional Texture
- Confidence. Mild irritation at bad practices. Earned authority. Occasional surprise (the 2,500 students moment).
- Not warmth. Not vulnerability. Not "let me share my journey".

## Video Thumbnail with Play Button

**For any video-redirect newsletter, a video thumbnail is mandatory, not optional.** Every draft in the output must include a `[VIDEO THUMBNAIL + LINK]` placeholder inside the body (typically right before or right after the bullet list, before the CTA line). If the user hasn't supplied a thumbnail image, ask for one before presenting the drafts.

When you have a thumbnail path, run the bundled script to overlay a YouTube-style play button:
```bash
python3 scripts/add-play-button.py <input_thumbnail> [output_path]
```

Defaults: resizes to 1280×720 at JPEG quality 80 (~100KB). Override with `--max-width` and `--quality` if needed.

## CTA Questions

Teaser emails almost never end on a "reply and let me know" question, they end on a CTA link. If you want a reply prompt (Ray sometimes does), keep it brutally short, one line, and place it just before the sign-off. Apply the same framing logic as before:

**For feature-announcement / product-launch newsletters**, CTAs must be **forward-looking**. Assume adoption.
- Good: "What's the first thing you're going to point /monitor at?"
- Bad: "How are you currently watching long-running things in Claude Code?" (assumes non-adoption)

**For evergreen / opinion newsletters**, "share your experience" framing still works.

Always specific to the topic. Never generic "what do you think?".

## Output Format

The typical input is a video transcript that needs to be turned into a short teaser email. The output is 5 body variations plus a global pool of 10 subject lines and 10 preview snippets. Ray picks one body, one subject, and one preview, and copies the trio.

### What to generate

**5 Newsletter Variations** (the bodies), each with a different opening hook from the list above. Label each with its hook strategy so Ray can scan quickly. Each variation is a complete, sendable draft. For video-redirect newsletters, every variation must include the `[VIDEO THUMBNAIL + LINK]` placeholder. Mix between:
- Provocative Claim Hook
- Question-You've-Wondered-About Hook
- What-If Hook
- Direct Announcement Hook
- Big-Number Reveal Hook
- Problem-First Hook

**10 Subject Lines** (global pool). Subject lines in this style are short, declarative, often quotable. Examples from the corpus:
- "The Official Anthropic Ralph Plugin Sucks"
- "Your AGENTS.md might be a big problem"
- "My Skill Makes Claude GREAT At TDD"
- "11 Tips For Coding With Ralph Wiggum"
- "Can you engineer with AI? Yes."

Aim for a mix: declarative claim, problem statement, number/list, named feature, contrarian take, quotable phrase. Title-case some, sentence-case others. Don't be afraid of capitalised words (GREAT, SUCKS) for emphasis when the claim warrants it.

**10 Preview Snippets** (global pool). One-sentence teases that complement the subjects without repeating them. Previews in this style lead with the twist or the credibility ("After months of coding with AI...", "It's an official tool that's fundamentally broken...", "We sold 2,500.").

**5 CTA Questions** (optional, only if Ray wants a reply prompt). Apply framing rules.

### Why a global pool instead of per-variation subjects

Earlier versions of this skill paired 5 subjects and 5 previews *per variation*, which forced a rigid pick-the-body-then-pick-from-its-5-subjects flow. Ray preferred a global pool so the email view stays clean and any subject can pair with any body. When generating the 10, write them broad enough that most of them pair sensibly with at least 2-3 of the 5 body variations.

### Present everything together

In markdown: write the 5 bodies first, then a "Subject line options" list of 10, then a "Preview snippet options" list of 10, then the CTA questions (if any). In the HTML viewer: bodies, subjects, and previews all flow into the template (see the HTML Viewer section).

## HTML Viewer Mode (Opt-In)

When Ray asks to see the variations "in an HTML thing", "in a viewer", "as HTML", or similar, render the 5 newsletter variations using the bundled Gmail-style template at `references/gmail-viewer-template.html`.

**How to use:**
1. Read `references/gmail-viewer-template.html` to see the structure
2. Copy it to a user-accessible location (e.g., `<topic>-newsletter-options.html` in the working directory)
3. Replace the `__VARIATIONS_JSON__` placeholder with an array of 5 variation objects, each containing:
   - `hook`: the hook strategy label (e.g., "Provocative Claim")
   - `body`: an array of paragraph strings (use `"[THUMBNAIL]"` as a paragraph entry to mark where the video thumbnail goes)
4. Replace `__SUBJECTS_JSON__` with an array of exactly 10 subject line strings
5. Replace `__PREVIEWS_JSON__` with an array of exactly 10 preview snippet strings
6. Replace `__THUMBNAIL_PATH__` with the relative path to the play-button thumbnail
7. Replace `__VIDEO_URL__` with the YouTube URL
8. Replace `__TOPIC__` with a short topic label for the page title
9. `open` the resulting HTML file

The viewer has three modes: **Inbox** (default), **Headlines** (10 subjects + 10 previews), **Compare all** (horizontal scroll of the 5 bodies). Keyboard: `1` to `5` jump, `i`/Escape returns to inbox, `h` Headlines, `c` Compare. Subject/preview selection is global.

## Appendix / Reference Sections

Some newsletters include bonus content below the sign-off (system prompts, code snippets, checklists). Teaser-style emails rarely do this, but if the content lends itself:

- Add a `---` divider after the sign-off
- Use a clear heading
- Keep the bridge sentence in the body short and casual
- Format reference material cleanly
- Don't repeat content from the body

## Workflow

1. **Fetch the transcript if needed.** If the user provided a YouTube URL and no local transcript exists in `socials/youtube/transcripts/`, fetch one via `python3 ~/.claude/skills/supadata/scripts/supadata.py transcript <video_id>`. Don't assume the transcript is on disk, check first.
2. **Read at least 3 emails from `references/example-emails/`** to calibrate tone, length, and structure. Start with `03-my-skill-makes-claude-great-at-tdd.md`, `07-your-agents-md-might-be-a-big-problem.md`, and `08-the-official-anthropic-ralph-plugin-sucks.md` (the three cleanest examples of the Teaser Arc). Read `06-...2-500-students.md` or `10-can-you-engineer-with-ai-yes.md` if Ray wants a long-form variant.
3. Identify 5 distinct hooks from the content. Each hook should lead with a different angle (claim, question, what-if, announcement, big number, problem).
4. Draft 5 complete newsletter variations. **Target 150 to 250 words each by default.** If you find yourself writing 600+ words, cut.
5. Generate 10 subject lines, 10 preview snippets, and (if Ray wants) 5 CTA questions.
6. **Mechanism pass.** Re-read every variation and confirm each one has a mechanism-with-numbers paragraph after the hook. Specific numbers? Named concepts? Falsifiable claims? If the email goes hook → bullets with no mechanism between them, that variation is broken. Rewrite.
7. **Length pass.** Re-read each variation. If it has any paragraph longer than 3 sentences, break it. If it has any sentence that could be cut to a shorter one, cut it. If it has a "warm-up" paragraph before the hook, delete the warm-up.
8. **Structural-consistency pass.** Re-read every variation looking for iterative-edit artifacts: numbered promises that don't match what follows, dangling fragments, pronouns without clear antecedents, contradictions between paragraphs.
9. **Dash scan.** Literally search every variation for `—` and `–` and remove them. Replace with commas, periods, parentheses, or a rewrite. The corpus contains spaced hyphens (` - `) for asides, convert those too if you find yourself echoing them. Do this even if you "know" you didn't add any.
10. **Voice check.** Read each variation aloud (mentally). Does it sound like a confident engineer making a claim, or does it sound like a vulnerable storyteller? If the latter, rewrite the opening to lead with the claim, not the story.
11. **Handle the thumbnail** (video-redirect newsletters only). Ask Ray for a thumbnail path if not provided. Run `scripts/add-play-button.py`.
12. Present everything together for Ray to mix and match. If Ray asks for HTML/viewer mode, render via `references/gmail-viewer-template.html`.
13. After the email is sent, ask Ray to paste the final version back so it can be saved alongside the calibration corpus for future reference and performance tracking.

## Examples

See `references/example-emails/` for 9 real teaser newsletters. Read these to calibrate. `INDEX.md` lists them all.

**Best examples to study (in priority order):**
1. `03-my-skill-makes-claude-great-at-tdd.md`, textbook Teaser Arc, short, claim + setup + bullet list + CTA
2. `07-your-agents-md-might-be-a-big-problem.md`, problem-first hook, "Here's why:" reveal, bullet list, CTA
3. `08-the-official-anthropic-ralph-plugin-sucks.md`, pure provocative claim, fast escalation, technical clarity
4. `02-11-tips-for-coding-with-ralph-wiggum.md`, what-if hook, numbered teaser, technical credibility
5. `04-new-skills-handoff-prototype-review-and-writing.md`, direct announcement hook, 2-feature structure
6. `06-what-i-learned-teaching-ai-engineering-to-2-500-students.md`, long-form variant, big-number reveal, student quotes
7. `10-can-you-engineer-with-ai-yes.md`, long-form variant, contrarian framing, dividers, P.S.
8. `09-a-quick-question.md`, ultra-short variant for a single direct question

Ignore `05-...ubiquitous-language-is-dead...` for hooks (it's a quiet changelog update, not a hook-led email, useful only as an example of sub-format B).
