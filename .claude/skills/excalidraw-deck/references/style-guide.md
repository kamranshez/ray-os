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
12. Authoring five variations
13. Shorthands in the picker template
14. No em or en dashes
15. Validate + preview

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

## 12. Authoring five variations

The picker exists so Ray can choose, which only works if the five options are actually
different. Five rewordings of the same picture is a wasted sheet.

**Vary the diagram type, not the label.** Pick five different visual arguments from this
palette and map the idea onto each:

| type | when it fits |
|---|---|
| before / after, two boxes | a change of state, an inversion, a claim replaced |
| a chart with two curves | anything that happens over time or scale, crossovers, divergence |
| a pipeline | an ordered process, a build, a workflow |
| fan-out with badges | parallel work that gets judged |
| a table or matrix of checks | methods against properties, tradeoffs |
| ranked horizontal bars | a distribution, a breakdown, "which of these dominates" |
| paired vertical bars | a before/after on real numbers |
| a ring or loop | co-evolution, flywheels, anything that returns to its start |
| venn / bullseye / triangle | overlap, gaps, "pick two of three" |
| small multiples | the same shape three times with one thing changed |
| a hero stat block | one number that carries the whole slide |
| a container with an inner box | subset relationships, "X is a special case of Y" |

Two practical rules:

- **Use the real numbers wherever the source has them.** A variation that prints
  `28.57 to 0.56` beats one that draws a generic tall-bar-short-bar. When the source only
  publishes a figure with no values, draw the shape and print no numbers rather than
  inventing plausible ones.
- **Do not pad to five.** If a slide genuinely only supports three good treatments, ship
  three; the checker warns below three so you notice, not so you fill.

## 13. Shorthands in the picker template

The picker template defines these on top of the base helpers. They exist because 70
diagrams of `addRect(x, y, w, h, { fill, fillStyle: 'solid', strokeWidth: 2 })` is
unreadable. Use them; they keep layout arithmetic visible.

- `box(x, y, w, h, fill, opts)` — solid-filled rect, strokeWidth 2 by default.
- `ctr(x, y, t, size, opts)` / `mctr(...)` — centred text, prose / mono.
- `lft(x, y, t, size, opts)` / `rgt(...)` — start-anchored / end-anchored text.
- `aR(x1, x2, y, opts)` — straight horizontal arrow. `aD(x, y1, y2, opts)` — vertical.
- `rowX(i, n, w, g)` — x of box `i` in a centred row of `n` boxes width `w`, gap `g`.
  This is the anti-overlap tool: `rowX` guarantees even spacing and centring, so a row of
  stages is `const x = rowX(i, 5, 240, 45)` and never a hand-tuned constant.
- `V(tag, headline, caption, draw)` — push one variation. The tag drives grouping.

Note the arrow helpers always bow *upward* by `|curve| * 0.6`; a negative `curve` moves the
control point left, positive moves it right. For a downward-bowing connector, route it with
two `addLine` calls and put `addArrow` only on the final leg.

## 14. No em or en dashes

Standing rule for all of Ray's content: never use em dashes or en dashes in any text
that appears in the deck (headlines, captions, labels). Use a period, a comma, or the
inline separator `  .  ` (space-dot-space) that the decks use between short clauses,
e.g. `9 agents . ~900k tokens . ~50s`. (This guide uses dashes in its own prose, but
the *deck content you generate* must not.)

## 15. Validate + preview

- After every edit, run `python3 scripts/check-deck.py <deck>.html` — it runs
  `node --check` on the inline script, then lists the slide headlines (linear deck) or the
  variations grouped per slide with warnings for thin sets (picker).
- Preview by serving the folder: `python3 -m http.server 8772` then open
  `http://localhost:8772/<deck>.html`. To see fresh edits, hard-reload
  (Cmd+Shift+R) — a plain reload can serve the stale cached page.
- **Check the geometry programmatically when the deck is large.** You cannot eyeball 70
  diagrams. Drive the served page with the Playwright MCP and walk every sheet, flagging
  any element whose `getBBox()` leaves the safe area:

  ```js
  el.getBBox()  // -> {x, y, width, height} already in viewBox units
  // flag: x < 6 | x + width > 1594 | y < 90 | y + height > 784
  ```

  In the picker all five variations are in the DOM at once, so one pass per sheet covers
  them all. This catches overflowing labels and stray arrowheads that a spot check misses.
