# Writing LinkedIn Posts (text format)

For carousel posts, use `carousel.md` instead. The principles below still apply — apply them to the cover and content slides — but the rendering flow is different.

The goal every time is to write **10 different posts** for Ray to choose from. Each one uses a different combination of format pattern + emotional triggers so he gets real variety, not 10 versions of the same angle.

## Before Writing

1. Read `references/viral-playbook.md` — **especially the 8 format patterns at the top.** This is the core framework, not optional guidance.
2. Read every file in `references/viral-examples/` (most recent month folder first) — these are real top-performing LinkedIn posts in Ray's niche, captured to keep the style guide grounded in what's currently working.
3. Read 3-5 recent files in `references/post-history/` to understand Ray's voice and what's already been done. Don't recycle hooks or angles he's used in the last month.
4. **Quiz Ray on his earned authority on this topic — see next section.** Do this even when the topic seems clear. The viral version of the draft is usually one Ray-specific number or scene short of where the first pass lands.

## The Earned-Authority Quiz (format pattern 3)

**Before drafting any variation, ask Ray these three questions** via AskUserQuestion. Skip only if the topic is purely opinion-based (rare) or if Ray has already volunteered the relevant facts in his prompt.

1. **"What have you personally done that's relevant to this topic — specific runs, experiments, numbers, or stories?"**
   You're looking for: hours, token counts, dollar amounts, repos refactored, leads pulled, error rates, tests run, screen recordings made, etc.

2. **"What's the most counterintuitive thing you've learned about this that doesn't show up in the discourse?"**
   You're looking for: a contrarian take grounded in his actual experience, not just a hot take.

3. **"What's the most concrete recent stat or scene you can offer?"**
   You're looking for: a specific scene Ray witnessed (e.g. "I opened my Sentry dashboard last Monday and 30 issues were already closed"), or a specific number ("4.1M tokens on one loop").

Weave the answers into multiple variations. At least 3 of the 10 drafts should anchor on Ray's own evidence (self-anchored), not on quotes from Boris / Anthropic / external authority (authority-anchored). Both types are valid — but Ray's self-anchored posts are his unique moat (see the "Strategic angle for Ray specifically" section in `viral-playbook.md`).

## The Writing Process

For each of the 10 posts:

### Step 1: Pick a format pattern (one per post, format pattern 8)

From `viral-playbook.md` and the example posts in `viral-examples/`:

- **Contrast hook** ("Most people X. Smart group Y.") — Jahanzaib, Adam, Nate variations
- **Tier map** ("X has 3 levels of Y") — Charlie, Nate, Adam
- **"X is a lie" + earned proof** — Luís Rodrigues vibe-coding
- **Confession** ("I don't open Claude Code most days") — implied in several
- **Tactical reveal** ("I run loops on Slack channels") — Luís voice agent
- **Changelog / "what shipped while I slept"** — Anthropic official, Luís voice agent hybrid
- **Decision rule** ("If X → A. If Y → B. If Z → C.") — Charlie Hills
- **Aphorism + body** ("Loops without an oracle compound slop")

Pick a different pattern for each of the 10 drafts. Variety here is the whole point of generating 10.

### Step 2: Pick an emotional architecture

From the 6 triggers in `viral-playbook.md`:
- **Primary trigger** (the hook — what makes them stop scrolling)
- **Secondary trigger** (the body — what makes them engage)

Use a different primary trigger for each draft. With 6 triggers + 8 patterns, there are more than 10 distinct combinations available.

### Step 3: Write for feeling, not information

Ask yourself: "What will the reader *feel* after reading this?" If the answer is "informed," rewrite it. The answer should be one of: seen, challenged, curious, aspirational, tribal, uncomfortable-in-a-good-way.

### Step 4: Apply the format patterns

Run each draft through the 8 format patterns from `viral-playbook.md`:

1. Does the hook lead with contrast, not a feature announcement?
2. Is the structure repostable (tier map / decision rule / recipe), or just an essay?
3. Is Ray's earned authority frontloaded?
4. Does it close with a tactical → emotional twist, not just an insight statement?
5. Is every claim quantified? (Hunt for qualifiers: "around", "a couple", "many", "a lot" — replace with numbers.)
6. Does it close with a decision rule or memorable kicker? (Optional — but strong.)
7. Are arrows (→) used instead of bullets / sentences for lists?
8. Is the post executing ONE pattern cleanly, not mixing three?

Cut or rewrite drafts that fail #1, #3, or #5. The other patterns are amplifiers; these three are dealbreakers.

### Step 5: Run the authenticity filter

Before including each post, check:
1. Is this true based on Ray's actual experience?
2. Would Ray say this at a dinner with smart people?
3. Is the emotional intensity proportional to the claim?
4. Does it serve the reader, not just engagement?

If it fails any test, rewrite or cut it.

## Writing Rules

### Voice
- Ray's voice: casual, opinionated, grounded in real experience
- Sentence-case capitalization always
- Short sentences that stack. Conversational rhythm.
- The reader should feel like a smart friend is telling them something they need to hear
- **No em or en dashes** in any post. Use commas, periods, or sentence breaks.
- **No DM keyword CTAs** ("Comment 'X' and I'll send you the guide"). Not Ray's house style.

### Output Format

After writing all 10 posts, generate an HTML preview so Ray can see them styled as real LinkedIn posts with copy buttons.

1. Write a JSON file to `/tmp/linkedin-posts.json`:

```json
{
    "posts": [
        {
            "number": 1,
            "triggers": "Productive Discomfort + Aspiration",
            "pattern": "Contrast hook",
            "body": "The full post text here..."
        }
    ]
}
```

(The `pattern` field is optional but helpful — it makes it easy to track which format patterns landed best across batches.)

2. Run the preview script:
```bash
python scripts/preview-posts.py /tmp/linkedin-posts.json --output /tmp/linkedin-preview.html --open
```

This opens an HTML page styled like LinkedIn's feed with all 10 variations and a copy button on each. Ray picks the one he wants to use.

Do NOT also output the raw post text in the conversation — the HTML preview is the deliverable.

## After Ray Picks

1. Save the chosen post(s) to `references/post-history/YYYY-MM-DD_slug.md`:

```yaml
---
date: YYYY-MM-DD
hook: "First line of the post"
triggers:
  primary: productive discomfort
  secondary: aspiration
pattern: contrast hook       # which of the 8 format patterns this post used
media: text only             # or "carousel (N slides)" / "video"
status: draft
engagement:
  reactions: null
  comments: null
  reposts: null
  impressions: null
url: null
notes: null
---

The full post text here...
```

2. Ask: "Want me to post this, or are you posting yourself? Or save as a draft to come back to later?"
   - If Claude posts → see `browser-navigation.md`, then update status to `posted` once confirmed
   - If Ray posts himself → update status to `posted` once he confirms it's live
   - If saving as a draft → keep status as `draft` and add a todo to `todos.yaml`

3. Update `todos.yaml` in the skill root (NOT any global todos file):
   - For posted posts → add an entry to check engagement in 3 days (`due: <today + 3>`)
   - For drafts → add an entry to finalize and post the draft, with `related_post` pointing to the post-history file
   - When a todo is completed, flip `status: done` or remove it
