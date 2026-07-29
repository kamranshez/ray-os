---
name: excalidraw-deck
description: >-
  Build hand-drawn, Excalidraw-style HTML slide decks that explain a concept through
  sketch-aesthetic vector diagrams — rough.js strokes on a dark canvas, full-bleed,
  one diagram per slide with a caption underneath, arrow-key and tap navigation. Use
  this skill whenever the user wants explainer slides, a concept deck, diagram slides,
  or a talk/video presentation in the hand-drawn sketch look, or says things like "make
  slides for X", "build a deck for X", "add a slide in this style", "turn this into a
  sketch/excalidraw-style deck", "another slide like the workflow deck", or points at an
  existing rough.js deck and wants more in the same style. This is for self-contained
  vector-diagram decks — NOT the Claude Code terminal-aesthetic slides (use
  cc-terminal-slides) and NOT raster image generation (use excalidraw-gen, which calls
  an image model). Reach for this skill proactively for any "explain this concept on
  slides" request, even when the user does not say the word "excalidraw".
---

# excalidraw-deck

Turn any concept into a hand-drawn slide deck that matches Ray's reference decks: rough.js
sketch strokes, a dark Excalidraw palette, Excalifont + Cascadia Code, one diagram per
slide, a short headline and one-sentence caption underneath, draw-on stroke animation,
tap/arrow navigation. The output is a single self-contained `.html` file you can open in
a browser or screen-record for a video.

The whole look is already engineered into the two bundled templates. Your job is to copy
one, decide the slide-by-slide narrative, and author each diagram with the bundled helpers
— following the conventions in `references/style-guide.md`. **Read that style guide before
authoring slides**; it is the difference between "a deck" and "a deck that looks like
Ray's." Two real, shipped decks are in `assets/examples/` to study for tone and density.

## Always offer variations first

**Default to the picker.** Ray does not want one interpretation of a slide, he wants to
choose between several. Unless he explicitly asks for a finished linear deck, build a
**variation picker**: propose the slide list, then draw **five genuinely different
variations of every slide** and hand him one HTML file where all five sit on screen
together, click to zoom, click to pick.

Skip straight to the linear deck only when he says so ("just build it", "one slide, this
diagram"), or when he is adding a single slide to a deck that already exists.

## What you are producing

- One HTML file, kebab-case name, saved where the user wants (their `slides/` folder by
  default). No build step, no server needed, though a local server is the easiest preview.
- **Picker mode** (default): a flat list of `V(tag, headline, caption, draw)` calls plus a
  `TITLES` array. Tag is `<slide number><letter>`: `1A`..`1E` are five ways to draw slide 1.
  The shell groups them into one contact sheet per slide automatically.
- **Final mode**: a `slides` array of `{ headline, caption, draw }`. That array IS the deck.

## Workflow

1. **Get the concept and the beats.** What is being explained, and what is the narrative
   order — each slide is one idea. If the concept refers to a real artifact (a workflow
   file, an API, a repo, a CLI command, a benchmark, a paper), **read the actual source
   first** so the diagram mirrors the real structure — real stage names, real counts, real
   numbers, real control flow. Grounded slides are the strong ones; invented ones look
   hollow. Offload heavy source reading to a subagent and keep only the structure you need.

2. **Propose the slide list before drawing anything.** A table of N slides with a one-line
   purpose each, in narrative order. Say which are trimmable. This is cheap to change and
   expensive to change later, so get agreement on the spine first.

3. **Copy a template** to the target path:
   ```bash
   # picker (default)
   cp /Users/ray/Desktop/ray-os/.claude/skills/excalidraw-deck/assets/picker-template.html <target>/<name>.html
   # linear deck
   cp /Users/ray/Desktop/ray-os/.claude/skills/excalidraw-deck/assets/deck-template.html <target>/<name>.html
   ```
   Update the `<title>`. Both ship teaching slides using the stock recipes — keep them as
   scaffolding while you build, then replace them.

4. **Read `references/style-guide.md`.** It carries the rules that matter: the de-clutter
   rule (no clever bottom-of-canvas taglines), colour semantics, the native sizing scale,
   mono-vs-prose fonts, layout discipline (non-overlapping boxes, arrows that actually
   reach their target), the headline/caption voice, the no-em/en-dash rule, and how to make
   five variations that are actually different. The helper API and recipes live there too.

5. **Author.** In picker mode, set `TITLES` to the slide list from step 2, then write five
   `V('1A', ...)` through `V('1E', ...)` per slide. In final mode, one `slides.push({...})`
   per beat. Either way: compute box positions (do not eyeball spacing), keep everything
   inside the y = 100-770 safe zone, label things functionally, let the caption carry the
   message, and reuse the recipes rather than starting each diagram from scratch.

6. **Validate.** After each round of edits:
   ```bash
   python3 /Users/ray/Desktop/ray-os/.claude/skills/excalidraw-deck/scripts/check-deck.py <name>.html
   ```
   It runs `node --check` on the inline script and prints the slides grouped by number, so
   a missing or thin variation set shows up immediately.

7. **Prove the layout, then open it.** With 5 variations per slide you cannot eyeball 70
   diagrams, so check the geometry programmatically: serve the file, drive it with the
   Playwright MCP, step through every sheet and assert that no element's `getBBox()` falls
   outside x 0-1600 / y 90-784. It catches overflow and stray labels in one pass. Then
   `open -a "Google Chrome" <abs-path>` and `SendUserFile` it.

8. **Take the picks, build the deck.** He replies with tags (`1B 2A 5D ...`). Copy
   `deck-template.html`, move the chosen `draw` bodies across in narrative order as
   `slides.push({ headline, caption, draw })`, and drop the tag prefix from the headlines.

## The six things that make or break the look

These come up every time; the style guide expands each one.

- **Five variations means five diagram types.** Not five wordings of the same picture. If
  1A is two boxes and an arrow, then 1B is a chart, 1C is a pipeline, 1D is a matrix, 1E is
  a stacked split. Same idea, genuinely different visual argument.
- **One diagram per slide, caption carries the words.** The SVG holds the diagram plus
  short functional labels. Headline and caption are DOM text below the canvas. Do not draw
  the message as a sentence inside the canvas.
- **No bottom-of-canvas "thesis" taglines.** The single most important de-clutter rule.
  Ray strips every clever italic one-liner. If a phrase editorializes instead of labelling
  a box / arrow / count / outcome, cut it.
- **Colour means something.** Red = problem/cost/fail, green = success/done, muted
  blue/violet/amber = neutral stages. At most one or two loud colours per slide.
- **Boxes don't overlap and arrows reach their target.** Compute positions; keep arrows in
  the gaps and landing on box edges, never overshooting or floating short.
- **No em or en dashes** anywhere in deck text. Use periods, commas, or the `  .  ` inline
  separator.

## Bundled resources

- `assets/picker-template.html` — **the default starting point.** Full engine plus the
  contact-sheet shell: one screen per slide showing all its variations, arrows to move
  between slides, click or 1-5 to zoom, `pick` / `p` to mark a choice, a running pick list
  in the footer. Ships ten teaching variations across two slides covering all the stock
  recipes. Copy this unless the user asked for a finished linear deck.
- `assets/deck-template.html` — the linear deck: full-bleed, one slide at a time, draw-on
  animation, tap and arrow navigation. This is what the final deck is built from.
- `references/style-guide.md` — the conventions, helper API reference, and diagram recipes.
  Read before authoring.
- `assets/examples/` — two real shipped decks for style reference (a use-case deck and a
  concept/orchestration deck). Open them to calibrate density and tone; don't edit them.
- `scripts/check-deck.py` — validates either format (node --check, then the slide list, or
  the variations grouped per slide with warnings for thin sets). Run after edits.

## Distinct from neighbouring skills

- **cc-terminal-slides** — Claude Code *terminal* aesthetic (monospace terminal frames).
  Different look; use that skill when the user wants the terminal style.
- **excalidraw-gen** — generates *raster images* via an image model. Use that when the user
  wants a single generated picture, not an interactive multi-slide vector deck.
