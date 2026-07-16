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

The whole look is already engineered into `assets/deck-template.html`. Your job is to copy
it, decide the slide-by-slide narrative, and author each slide's diagram with the bundled
helpers — following the conventions in `references/style-guide.md`. **Read that style guide
before authoring slides**; it is the difference between "a deck" and "a deck that looks like
Ray's." Two real, shipped decks are in `assets/examples/` to study for tone and density.

## What you are producing

- One HTML file, kebab-case name, saved where the user wants (their `slides/` folder by
  default). It needs no build step and no server to function, though a local server is the
  easiest way to preview.
- A `slides` array inside it. Each entry is `{ headline, caption, draw }` — `draw` is a
  function that paints one diagram with the helper API. That array IS the deck.

## Workflow

1. **Get the concept and the beats.** What is being explained, and what is the narrative
   order — each slide is one idea. If the concept refers to a real artifact (a workflow
   file, an API, a repo, a CLI command, a benchmark), **read the actual source first** so
   the diagram mirrors the real structure — real stage names, real counts, real control
   flow. Grounded slides are the strong ones; invented ones look hollow. Offload heavy
   source reading to a subagent and keep only the structure you need.

2. **Copy the template** to the target path:
   ```bash
   cp /Users/ray/Desktop/ray-os/.claude/skills/excalidraw-deck/assets/deck-template.html <target>/<deck-name>.html
   ```
   Update the `<title>`. The template ships three teaching slides (before/after, pipeline,
   fan-out) — keep them as scaffolding while you build, then replace them.

3. **Read `references/style-guide.md`.** It carries the rules that matter: the de-clutter
   rule (no clever bottom-of-canvas taglines), colour semantics, the native sizing scale,
   mono-vs-prose fonts, layout discipline (non-overlapping boxes, arrows that actually
   reach their target), the headline/caption voice, and the no-em/en-dash rule. The full
   helper API and diagram recipes live there too.

4. **Author the slides.** Replace the array with one `slides.push({ ... })` per beat. Lay
   out boxes by computing positions (don't eyeball spacing), keep everything inside the
   y = 100-770 safe zone, label things functionally, and let the caption carry the message.
   Reuse the recipes (before/after, pipeline, nested pipeline, fan-out, loop strip, cost
   bars) rather than starting each diagram from scratch.

5. **Validate and preview.** After each round of edits:
   ```bash
   python3 /Users/ray/Desktop/ray-os/.claude/skills/excalidraw-deck/scripts/check-deck.py <deck-name>.html
   ```
   It runs `node --check` on the inline script and prints the slide list. Then serve and
   look at it: `python3 -m http.server 8772`, open `http://localhost:8772/<deck-name>.html`,
   hard-reload (Cmd+Shift+R) to defeat the cache. Iterate on overlap and arrow targeting
   until each slide reads cleanly.

## The five things that make or break the look

These come up every time; the style guide expands each one.

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

- `assets/deck-template.html` — the runnable starting point: full engine, full-bleed shell,
  three teaching slides. Copy this.
- `references/style-guide.md` — the conventions, helper API reference, and diagram recipes.
  Read before authoring.
- `assets/examples/` — two real shipped decks for style reference (a use-case deck and a
  concept/orchestration deck). Open them to calibrate density and tone; don't edit them.
- `scripts/check-deck.py` — validates a deck (node --check + slide list). Run after edits.

## Distinct from neighbouring skills

- **cc-terminal-slides** — Claude Code *terminal* aesthetic (monospace terminal frames).
  Different look; use that skill when the user wants the terminal style.
- **excalidraw-gen** — generates *raster images* via an image model. Use that when the user
  wants a single generated picture, not an interactive multi-slide vector deck.
