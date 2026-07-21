# Writing LinkedIn Posts (text format)

For carousel posts, use `carousel.md` instead.

Every text post is drafted in the **Stanislav template** — one fixed skeleton, defined in `references/viral-playbook.md`. Read that file first, every time. Do not invent new structures; generate variations INSIDE the skeleton.

## Before Writing

1. Read `references/viral-playbook.md` — the skeleton, the variation axes, the house rules.
2. Read 3-5 recent files in `references/post-history/` — voice calibration and dedupe. Don't recycle hooks or stories used in the last month.
3. Gather the facts: pull real numbers from the source (stars, views, pricing, years, benchmarks). Never fabricate a number. If the source has no numbers, it's probably not a post.

## The Framing Checkpoint (one line, before the batch)

State the frame in one or two lines and confirm with Ray before generating:

> "Hook number: [87 years / 21.2M views / ...]. Angle for the why-it-matters paragraph: [X]. Drafting the batch now unless you want a different lead."

One sentence of confirmation beats three rounds of re-rendering. Skip only when Ray's prompt already pins these down.

## The Batch

Generate **10 variations, all in the Stanislav skeleton.** Do not vary the structure — vary the axes listed in `viral-playbook.md`: hook line, scene-setting details, spec-bullet selection, why-it-matters angle, closer. Label each variation by what varies ("views-led hook, industry angle, no closer").

Before including each variation, check:

1. Hook line ends in a colon and carries a real number.
2. Spec block uses → bullets and only sourced numbers.
3. 150-250 words including the P.S.
4. P.S. funnel slot present (default line, or a topic-matched Agentic Coding School pointer).
5. House rules: no em/en dashes, sentence case, authors credited, no DM CTAs.
6. Would Ray say this at a dinner with smart people? Is it true to his actual experience?

Cut and redraft any variation that fails.

## Output Format

After writing the batch, generate an HTML preview so Ray can see them styled as real LinkedIn posts with copy buttons.

1. Write a JSON file to `/tmp/linkedin-posts.json`:

```json
{
    "posts": [
        {
            "number": 1,
            "triggers": "stars-led hook, engineer angle, Your thoughts? closer",
            "body": "The full post text here..."
        }
    ]
}
```

(The `triggers` field is the variation label — the preview renders it above each post.)

2. Run the preview script:
```bash
python scripts/preview-posts.py /tmp/linkedin-posts.json --output /tmp/linkedin-preview.html --open
```

Do NOT also output the raw post text in the conversation — the HTML preview is the deliverable.

## If Ray edits or rewrites a draft

Diff his version against yours and append the lesson to the "Learning loop" section of `viral-playbook.md` before the session ends. His edits outrank everything else in that file.

## After Ray Picks

1. Save the chosen post to `references/post-history/YYYY-MM-DD_slug.md`:

```yaml
---
date: YYYY-MM-DD
hook: "First line of the post"
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
