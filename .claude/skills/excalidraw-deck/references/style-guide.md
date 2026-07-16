# excalidraw-deck style guide

Everything that makes a deck look and read like the hand-drawn reference decks.
The engine (palette, helpers, shell) is already wired into `assets/deck-template.html` —
this file is the judgment layer: what to draw, how big, what colour, and what NOT to add.

## Table of contents
1. The shell is fixed — do not re-add chrome
2. The canvas: viewBox, safe zone, where text lives
3. The de-clutter rule (the single most important one)
4. Voice: headline + caption
5. Colour semantics
6. Sizing scale (native, no global multiplier)
7. Fonts: when mono, when prose
8. Layout discipline (non-overlap, arrows that reach)
9. Ground the diagram in the real source
10. Helper API quick reference
11. Diagram recipes
12. No em or en dashes
13. Validate + preview

---

## 1. The shell is fixed — do not re-add chrome

The template is deliberately full-bleed: no sidebar, no top bar, no nav buttons,
no slide counter, no comment overlay. The decks went through a pass that *stripped*
all of that out because it competed with the diagram for attention. Navigation is
tap-left / tap-right halves plus arrow keys and space. Leave it that way. The only
things you change per deck are the `slides` array and the `<title>`.

## 2. The canvas: viewBox, safe zone, where text lives

- The SVG is `viewBox="0 0 1600 900"`, `preserveAspectRatio="xMidYMid meet"`. Author
  in those coordinates; it scales to any screen.
- **Keep all drawing inside roughly y = 100 to y = 770.** Below ~780 runs into the
  DOM caption area underneath the canvas. Top ~100px is breathing room.
- The **headline and caption are DOM elements below the canvas**, set per slide via
  `headline:` and `caption:`. The SVG holds the diagram plus short *functional*
  labels only (what a box is, what an arrow means). Do not draw the headline or the
  caption sentence inside the SVG.

## 3. The de-clutter rule (the single most important one)

Do **not** add a clever italic one-liner "thesis punchline" at the bottom of the
canvas — the green "this proves nothing" / "generate broad, prove narrow" style of
tagline. Ray pulled every one of these out and called them "too much AI-generated
nonsense." The caption underneath already carries the message. Inside the canvas,
every word should be a *label on a thing in the diagram*, not commentary about the
diagram. If a phrase is editorializing rather than naming a box, an arrow, a count,
or an outcome, cut it.

A good slide is one diagram, a handful of labels, and the caption. When in doubt,
remove text rather than add it.

## 4. Voice: headline + caption

- **headline** — a short lowercase phrase that names the idea. Not a sentence, no
  trailing period. e.g. `fan out, then judge`, `resume a run, pay for the new step only`.
- **caption** — one lowercase descriptive sentence saying what the slide shows or
  what happens, no trailing hype. e.g. `one orchestrator splits the work; each worker
  returns a single pass or fail`. Aim for the plain "what it does," not a sell.
- Lowercase throughout (matches the reference decks). Semicolons and commas are fine.

## 5. Colour semantics

Colour means something. Use it for meaning, never decoration:

| meaning | fills | strokes / accents |
|---|---|---|
| problem, cost, failure | `lightRed`, `pink` | `rose` |
| success, done, good path | `softEmerald`, `green` | `emerald` |
| neutral stage / category | `blue`, `violet`, `amber`, `yellow`, `teal`, `card` | `ink` |
| secondary text | — | `soft` |
| subtle lines, de-emphasis | — | `faint` |

`addCheck()` defaults to `emerald`, `addCross()` to `rose` — pass/fail badges read
instantly because the colour is doing the work. A diagram should have at most one or
two "loud" colours (the red problem, the green payoff); everything else stays in the
muted blues/violets/ambers so the eye lands on what matters.

## 6. Sizing scale (native, no global multiplier)

Author at sizes that read full-screen from the start. The template's `addText` uses
the size you pass directly (no hidden 1.3x multiplier — that only existed to rescue a
deck that was authored too small). Rough scale:

- **hero number / single big word**: 34-42
- **box heading / stage name**: 24-30
- **label inside a box, secondary line**: 18-22
- **sub-label, small annotation**: 14-17

If a whole slide reads slightly small, set `scale: 1.15` on the slide object to bump
all its non-mono text at once rather than editing every call. Default is `1` (native).

## 7. Fonts: when mono, when prose

- **Mono (`font: MONO`, Cascadia Code)** for anything code-shaped: identifiers, file
  names, CLI flags, function names, API fields, stage keywords (`gather`, `verify`),
  token counts. It signals "this is a literal thing in the system."
- **Default Excalifont** (omit `font`) for prose labels and human descriptions.
- The DOM headline/caption are always Excalifont — handled by the shell.

## 8. Layout discipline (non-overlap, arrows that reach)

This is where hand-drawn decks go wrong, so be deliberate:

- **Compute positions, prove no overlap.** For a row of N boxes, pick a box width and
  a gap and place box i at `x0 + i*(width+gap)`. Check `x0 + N*(width+gap) - gap` stays
  within ~1500 (leave side margins). Don't eyeball spacing — overlapping cards was a
  repeated complaint.
- **Even spacing.** Equal gaps read as intentional; uneven gaps read as broken.
- **Arrows must reach their target and stop there.** An arrow should end on the edge
  of the box it points at — not overshoot into the next box, and not float in empty
  space short of it. When a callout points at a specific line of code, put the callout
  level with that line and run a short horizontal arrow to the box edge. (Mis-pointed
  callouts — "a real loop" pointing past the box into nothing — was a real bug we fixed.)
- **Inter-box arrows live in the gap.** If boxes are 50px apart, the connecting arrow
  spans those 50px; it does not start inside one box and end inside the next.
- Use `addCheck` / `addCross` for outcomes instead of writing "yes/no" — faster to read.

## 9. Ground the diagram in the real source

When a slide explains a real artifact — a workflow file, an API, a repo, a command —
read the actual source first and mirror its real structure: the real stage names, the
real counts, the real control flow. The strongest slides in these decks (the dead-code
sweep, the API-contract-drift detector, the deep-research pipeline) are faithful to the
code they depict, down to constants like `DRY_STREAK = 2` and `cap 8`. Don't invent a
plausible-looking flow when the real one is a `gh api` / `Read` away.

## 10. Helper API quick reference

All defined in the template's IIFE. Coordinates are viewBox units.

- `addRect(x, y, w, h, {fill, fillStyle, strokeWidth, stroke})` — fillStyle `'solid'`
  is the deck default (hachure looks noisy at slide scale).
- `addLine(x1, y1, x2, y2, {stroke, strokeWidth})`
- `addCircle(cx, cy, diameter, opts)` / `addEllipse(cx, cy, w, h, opts)`
- `addPath(svgPathString, opts)` — for custom shapes / curves.
- `addText(x, y, text, {size, font, fill, anchor, weight, style})` — `anchor: 'middle'`
  to centre on x; `font: MONO` for code.
- `addArrow(x1, y1, x2, y2, {curve, arrowSize, stroke, strokeWidth})` — `curve: 0` is
  straight; positive/negative bends it. Make it reach the target (section 8).
- `addCheck(cx, cy, size, color)` / `addCross(cx, cy, size, color)` — pass/fail badges.
- `COLORS` palette and `MONO` constant are in scope.
- A slide is `slides.push({ headline, caption, draw: () => { ... } })`. Optional
  `scale` / `monoScale` per slide.

## 11. Diagram recipes

The template ships three working recipes — copy and adapt them:

- **before / after (the turn)** — two big boxes, red problem on the left, green payoff
  on the right, one bold arrow across. Good for an opening "why this exists" slide.
- **pipeline** — N stages left to right, equal width, arrows in the gaps, last stage
  green. Good for any ordered process. For a *nested* pipeline, draw a dashed container
  rect (`strokeLineDash: [10, 8]`) around the inner stages and fan the outer item into
  several inner rows.
- **fan-out with results** — one orchestrator box on top, N worker boxes below it,
  an arrow to each, a `addCheck`/`addCross` badge under each. Good for parallel work
  that gets judged.

Other shapes that recur: a **loop strip** along the bottom showing a count shrinking
across rounds (`5 -> 1 -> 0 -> 0`) ending in a stop condition; a **cost-bar compare**
(two horizontal bars, red "expensive" vs green "cheap", widths proportional to the
real numbers).

## 12. No em or en dashes

Standing rule for all of Ray's content: never use em dashes or en dashes in any text
that appears in the deck (headlines, captions, labels). Use a period, a comma, or the
inline separator `  .  ` (space-dot-space) that the decks use between short clauses,
e.g. `9 agents . ~900k tokens . ~50s`. (This guide uses dashes in its own prose, but
the *deck content you generate* must not.)

## 13. Validate + preview

- After every edit, run `python3 scripts/check-deck.py <deck>.html` — it runs
  `node --check` on the inline script and lists the slide headlines.
- Preview by serving the folder: `python3 -m http.server 8772` then open
  `http://localhost:8772/<deck>.html`. To see fresh edits, hard-reload
  (Cmd+Shift+R) — a plain reload can serve the stale cached page.
