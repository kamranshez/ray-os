# Matt Pocock style — the structured explainer slide

## What it is

A Matt-style thumbnail looks like **a well-designed slide from an educational deck**. The left half is a self-contained explainer unit — a diagram, a comparison, or a fake UI card — and Ray sits on the right side with a podcast mic rising from the bottom-right. The whole thing reads like a hand-drawn excalidraw drawing, not a polished poster.

This style wins on feature videos, comparison videos, announcements, and anything teaching a concept.

## Universal DNA

Every Matt-style thumbnail has these elements:

- **Left half pure black**, right half warm dark bedroom with Ray
- **Handwritten excalidraw-style font** throughout
- **Colored rounded-square Kanban icons** with soft starburst/blob texture (never other icon shapes)
- **3-color semantic palette**:
  - 🔴 Red = bad / old / warning (e.g., `/loop`, polling, wasted tokens)
  - 🟢 Green = good / new / win (e.g., the hero command, events, savings)
  - 🟠 Orange = hero highlight (the feature being showcased)
  - White/gray = neutral labels
- **Red curved hand-drawn arrow** — used exactly ONCE per thumbnail for emphasis
- **Yellow handwritten `(parenthetical)` annotation** — used sparingly, never mandatory
- **Bold white-on-black pill-shaped callout** — optional summary hook below the visual
- **≤ 6 discrete items** on the left — always breathable negative space
- **Ray**: black t-shirt OR plain white collared long-sleeve shirt, warm smile or knowing smirk
- **Shure SM7B mic** rising from bottom-right
- **Dark warm bedroom background** behind Ray (not pure black on his side)

## Three sub-families (pick ONE per variant)

### 1. Structural — reads like a diagram

Big iconography with short labels, minimal text, one central concept visualized.

**Proven sub-patterns:**
- **Radial hub-and-spoke** (4–6 spokes) — central `/feature` in an orange Kanban box, thin white arrows radiating out to colored Kanban boxes with one-word labels
- **3-column horizontal flow** — WATCH → DETECT → REACT with big colored Kanban icons and short subtitles, thin white arrows between
- **Cycle flowchart** — 4 rounded rectangles (ERROR, WARN, FAILED, READY) connected in a loop, bold white-on-black pill callout underneath

**Golden refs:** `matt-style/structural/v4-B3-radial-diagram.png`, `v4-C5-three-column.png`, `v5-S1-radial-six-spokes.png`

### 2. Comparative — reads like a table or compare-bar

Parallel columns or split before/after, contrasting two states starkly.

**Proven sub-patterns:**
- **Feature comparison table** — `/X vs /Y` headline, 4 feature rows, red values on the old side, green values on the new side, hand-drawn grid lines
- **Mood columns** — 2 big Kanban icons with sad/happy faces drawn inside, red "POLLING" vs green "EVENTS" title, short labels underneath
- **Horizontal bar chart** — long red bar (old) vs tiny green bar (new), big white-on-black pill callout like `$0 IDLE COST`
- **Before/After state split** — left side chaotic Claude with red dots/tokens, right side calm Claude with checkmark, labeled BEFORE /X and AFTER /X
- **Two-column Kanban flow** — Events column (error/warn/failed) → Actions column (notify/diagnose/fix) with arrows, title above

**Golden refs:** `matt-style/comparative/v3-06-two-column-flow.png`, `v4-C2-events-actions-dense.png`, `v4-C4-before-after-state.png`, `v5-C1-feature-table.png`, `v5-C2-mood-columns.png`, `v5-C5-bar-chart.png`

### 3. Mockup — reads like a screenshot

Fake realistic software UI of a specific app.

**Proven sub-patterns:**
- **Tweet card** — Anthropic verified check, bold white body text, the feature underlined in thick red ink, tweet metadata
- **macOS notification popup** — frosted dark gray card with Claude starburst icon, bold app name, notification body, red curved arrow + yellow label `/feature`
- **Changelog card** — green NEW pill + date, bold title with feature underlined in red, 3 bullet points, small Claude Code footer
- **Raycast/search result** — minimal search input with the feature typed, one highlighted result row with Claude icon, green NEW pill, yellow `(just dropped)` annotation
- **Reddit post card** — r/ClaudeAI header, huge bold title with feature underlined in red, small gray preview, upvote/comment/share icons

**Golden refs:** `matt-style/mockup/v3-09-fake-tweet.png`, `v4-D3-mac-notification.png`, `v4-D4-changelog-card.png`, `v5-M5-raycast-search.png`, `v5-M6-reddit-post.png`

## Anti-patterns — NEVER do these in Matt style

- **Metaphor illustrations** — no cameras, bells, zzz clouds, cartoons, walkie-talkies. They consistently failed in testing.
- **Giant single-word typography** as the only element — too bare, no information density
- **Crossed-out / X-marked commands** — Ray rejected these specifically
- **Retro pixel terminal** — off-brand
- **Chaos grids / scatter plots** — too abstract
- **Dense compositions with >6 items** — breathable negative space wins
- **Multiple red accent arrows** — exactly one per thumbnail
- **Exaggerated facial expressions** — shock/surprise never lands

## The 5-variant recipe for a new video

When Ray asks for 5 Matt-style thumbnails for a video, pick 5 **different** golden references (one per generation, NEVER combine):

1. **1 structural** — usually radial or three-column, best for "watches X, Y, Z" framing
2. **2 comparative** — pick any two from table/mood/bar-chart/before-after. Use when the video has a clear "old way vs new way" narrative.
3. **2 mockup** — pick two from tweet/notification/changelog/raycast/reddit. Strong when the video is about a NEW feature launch.

Don't lock this ratio — read the transcript and pick whichever sub-patterns match the content. A pure comparison video might want 3 comparative + 2 structural. A launch video might want 3 mockup + 2 structural.

## Prompt template for Matt style

Use this exact structure. Fill in the `{slots}` based on the chosen sub-family.

```
A YouTube thumbnail in the style of the reference image. Pure black background on the LEFT half. Dark warm bedroom background behind the man on the right.

{SUB_FAMILY_VISUAL_DESCRIPTION}
— e.g. "A hand-drawn excalidraw-style radial diagram with a central orange rounded-square Kanban box containing '/monitor' in bold handwritten white font. Six thin white hand-drawn arrows radiate out to six smaller colored rounded-square Kanban boxes with one-word handwritten labels: 'errors' (red), 'tests' (yellow), 'deploys' (green), 'logs' (blue), 'webhooks' (purple), 'CI/CD' (cyan)."

{OPTIONAL_ACCENT}
— e.g. "A red curved hand-drawn arrow points at '/monitor' with a yellow handwritten annotation in parentheses reading '(new in Claude!)'."
— OR a bold white-on-black pill-shaped text box reading 'WATCHES EVERYTHING'

On the RIGHT, a young South Asian man with glasses and naturally straight dark hair — not curly, not wavy (matching the reference photos exactly) — wearing a {black t-shirt | plain white collared long-sleeve shirt}, with a {warm genuine smile showing teeth | subtle knowing smirk | subtle contemplative smile}.

A black Shure SM7B podcast microphone rises from the bottom-right foreground.

Hand-drawn excalidraw style, NOT polished vector. Clean minimal composition optimized for YouTube thumbnail viewing.
```

Pass ONE golden ref from the matching sub-family as `-r`. Never pass multiple refs.

## When saving a new winner

If Ray marks a new generation as a winner in Matt style:
1. Identify which sub-family it belongs to (structural / comparative / mockup)
2. Copy it to `golden-references/matt-style/<sub-family>/<descriptive-name>.png`
3. Mention it in the session so the user knows it's saved

Golden refs in sub-family folders get automatically discovered by future sessions looking for Matt-style inspiration.
