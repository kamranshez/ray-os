# Carousel Posts

For when the user wants a multi-slide LinkedIn carousel instead of a text-only post. Same niche-applied insight, packaged as a swipeable PNG deck (Nate Herk / X-card aesthetic). Carousels in Ray's niche have historically skewed toward higher reactions and reposts than text posts (Anthropic carousel: 2,523 reactions; Charly's Zero Trust: 491/82; Nate's 5-tier: 257/20).

## Before generating: the template rules still apply

Carousels do NOT exempt you from `viral-playbook.md` (the Stanislav template guide):

- The cover slide IS the hook — same rules as a text post hook: a real number, shock or superlative, no vague claims
- The content slides ARE the spec block — one idea per slide, numbers everywhere, no qualifiers
- The last content slide is the "why it matters" payoff
- The CTA slide is the ask, not the conclusion
- All house rules apply (no em/en dashes, never fabricate a number, credit authors)

## Style at a glance

- White background, near-black ink (#0F1419), gray subtitle (#536471), single blue accent (#1D9BF0)
- Bold Inter typeface, headlines with tight tracking
- Cover slide: huge headline, page counter top-right, profile chip + blue accent line under headline, "Swipe →" bottom-right
- Content slides: profile chip top-left, page counter top-right, big headline + lighter subtitle, lots of whitespace
- CTA slide: centered avatar, name + handle + verified check, "Follow for more…" headline + subtitle, black pill follow button
- Default size 1080×1350 (4:5 portrait). 1080×1080 also supported for true square.

## Process — always in this order

### Step 1: Propose the deck before generating

Do **not** jump to rendering. First, write a short numbered plan and show it to the user:

- Recommended slide count (typically 6–10; 8 is the sweet spot)
- One line per slide with the type and a draft headline (and subtitle for content slides)
- Ask "Want me to render this, or tweak first?"

Slide types are:
- `cover` — slide 1. Hooky headline only. No subtitle.
- `content` — slides 2..N-1. One headline + one short subtitle each.
- `cta` — final slide. "Follow for more…" type ask + button.

Why: carousels live or die by structure. Headlines that work as a single image rarely work as a flow. Surfacing the outline lets the user reshuffle before we burn render time.

### Step 2: Write the spec to disk

Once approved, write the JSON spec to `/tmp/linkedin-carousel-<slug>/spec.json`. Schema:

```json
{
  "title": "skill-system-upgrade",
  "size": [1080, 1350],
  "slides": [
    {"type": "cover",   "headline": "Claude's Skill System Just Got a Major Upgrade"},
    {"type": "content", "headline": "Skills are just recipes for your AI",
                         "subtitle": "Text instructions that tell Claude exactly how to handle a task. Every time. No re-explaining required."},
    {"type": "cta",     "headline": "Follow for more practical AI guides",
                         "subtitle": "I teach builders how to ship with Claude.",
                         "button": "Follow @rayamjad"}
  ]
}
```

Optional fields: `name` (default "Ray Amjad"), `handle` (default "@rayamjad"), `profile` (override avatar PNG path), `size` (default `[1080, 1350]`; use `[1080, 1080]` for true square).

### Step 3: Render

```bash
uv run /Users/ray/Desktop/ray-os/.claude/skills/linkedin/scripts/render-carousel.py /tmp/linkedin-carousel-<slug>/spec.json
```

Outputs `slide-1.png … slide-N.png` in `/tmp/linkedin-carousel-<slug>/`. First run installs Playwright's chromium (one-time, ~150MB).

### Step 4: Show the result

Read at least the cover and one content slide back to confirm they rendered correctly, then tell the user the directory and slide count. They drag-drop into LinkedIn's carousel post UI.

### Step 5: Log to post-history

Same as for text posts — write a YAML-frontmatter file to `references/post-history/YYYY-MM-DD_slug.md` with `media: carousel (N slides)` and queue an engagement-check todo for 3 days out.

## Profile picture

The avatar at `assets/profile.png` is pre-cropped from `~/Library/Mobile Documents/com~apple~CloudDocs/Profile Pictures/6 Large.jpeg`. To regenerate (e.g. new headshot):

```bash
uv run /Users/ray/Desktop/ray-os/.claude/skills/linkedin/scripts/prep-carousel-profile.py
# or: uv run scripts/prep-carousel-profile.py --source /path/to/new.jpg
```

## Writing good slides

- **Cover headline**: 6–12 words, declarative claim or surprise, ideally carrying the story's key number. Same energy as a YouTube title.
- **Content headline**: one idea per slide. If you wrote a list, each item is one slide.
- **Content subtitle**: 1–2 sentences. Concrete, not abstract. The headline says *what*, the subtitle says *why* or *how*. Numbers over qualifiers.
- **No em or en dashes** in any text — use commas, periods, or sentence breaks instead. (Ray's house style.)
- **Don't repeat the headline in the subtitle**. They should complement, not echo.
- Last content slide is the "why it matters" payoff; the CTA slide is the ask, not the conclusion.

## Length guide

| Content type        | Slide count |
|---------------------|-------------|
| Single insight      | 4–5         |
| List of 3–5 tips    | 6–7         |
| Story / framework   | 8–10        |
| Deep dive / lesson  | 10–12       |

When in doubt: cover + 5 content + CTA = 7 slides. That's the default.

## Troubleshooting

- **`profile image missing`** — run `prep-carousel-profile.py` (see above). The avatar is not committed-required; regenerate locally.
- **Text overflowing the slide** — shorten the headline. The CSS does not auto-shrink. Aim for ≤ 60 chars on cover, ≤ 50 on content.
- **Fonts look different from the reference** — first run pulls Inter from Google Fonts. If offline, fonts fall back to system sans; rerender once online.
- **Wrong slide ratio** — set `"size": [1080, 1080]` for square. Default is 1080×1350 because the reference visual examples are 4:5; LinkedIn supports both.
