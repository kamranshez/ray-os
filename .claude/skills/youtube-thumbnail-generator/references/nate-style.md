# Nate Herk style — the folder + /command studio shot

## What it is

A Nate-style thumbnail looks like **a studio product shot**. The dominant visual is a large manila folder (or rounded-square app icon) with a slash command on it, and Ray is next to it with a warm smile, pointing or gesturing toward the prop. The whole thing feels clean, professional, and product-launchy — like an announcement card.

This style wins on new command/tool launches, integration videos, "I built X" videos, and anything that has a clear single feature name to showcase.

## Universal DNA

Every Nate-style thumbnail has these elements:

- **Clean studio-style background** — usually a soft gray, dark, or subtly lit backdrop (NOT the warm bedroom Ray uses for Matt style — a more neutral product-shot look)
- **A hero prop on one side** — either:
  - A large manila folder with a colored rounded-square app icon on its label
  - Two or more large rounded-square app icons side by side (icons-on-black variant)
  - A dark terminal/CLI chat input with a command typed
- **Slash command text** rendered clearly in the prop — large bold black or white sans-serif
- **Bold headline text** — either the slash command itself or a short punchy phrase
- **Ray on the opposite side**, framed medium-shot, with a warm smile showing teeth, often pointing or gesturing toward the prop
- **Outfit**: black t-shirt or plain white collared long-sleeve shirt
- **No podcast mic** — this is a studio look, mic stays out of frame

## Sub-families (pick ONE per variant)

### 1. Folder + /command — the hero pattern

The signature Nate style. A large manila folder sits on one side of the frame, angled toward the camera. On the folder's label there's a colored rounded-square app icon (usually orange-red with a white 8-pointed starburst for Claude) and bold black text showing the slash command. Ray on the other side, pointing or smiling.

**Golden refs:** `nate-style/folder-command/folder-command.png` (contemplative), `folder-command-closeup.jpeg` (close-up face crop)

**Raw Nate Herk refs in `research/competitor-thumbnails/nateherk/`:**
- `OUyfxhFtGCo.jpg` — folder + command + pointing
- `X6EGzi9qm3E.jpg` — folder + command + smiling
- `vDVSGVpB2vc.jpg` — folder + agent network diagram

### 2. Icons on black — no face

Pure black background with two or more large rounded-square app icons side by side, connected by a white `+` symbol. Bold white statement text above or below. No person in the image (pass `--no-face` flag).

**Raw Nate Herk refs:**
- `LrgfmZkl3nc.jpg` — Claude + second app
- `Wu67lLD8bB0.jpg` — short phrase version
- `sboNwYmH3AY.jpg` — Claude + other app
- `B2Kh_ZoLVTM.jpg` — Claude + Codex

### 3. CLI chat input

A dark terminal or chat-input UI with a slash command typed inside. Ray next to it. Gives a "game over" / "new command dropped" feel.

**Raw Nate Herk ref:** `BlNJFa3Btm8.jpg`

### 4. Agent diagram + face

A dark background with a network diagram (nodes connected by lines) showing agents calling tools, and Ray next to it looking contemplative.

**Raw Nate Herk refs:** `1EPsUXSManU.jpg` (pixel art), `27Y44JYXZJ8.jpg` (dark terminal agent network)

### 5. Whiteboard numbered list

A clean whiteboard-style background with a short numbered list in handwritten font. Ray next to it smiling.

**Raw Nate Herk ref:** `mpALXah_PBg.jpg`

## Proven expressions by sub-family

- **Folder styles**: "warm enthusiastic smile showing teeth, pointing at the folder"
- **CLI styles**: "big warm smile showing teeth"
- **Whiteboard/agent styles**: "warm enthusiastic smile showing teeth"
- **Network/terminal styles**: "contemplative serious expression"

## Prompt template for Nate style (with-face variants)

```
A YouTube thumbnail in the style of the reference image. {BACKGROUND — e.g. "Clean gray studio background" or "Dark background with faint code editor elements"}.

On the {LEFT | RIGHT — match the reference}, {PROP DESCRIPTION — e.g. "a large manila folder angled toward the camera with an orange-red rounded-square app icon on its label, featuring a white 8-pointed starburst and bold black text '/command-name'"}.

On the {OTHER SIDE}, a young South Asian man with glasses and naturally straight dark hair — not curly, not wavy (matching the reference photos exactly) — wearing a {black t-shirt | plain white collared long-sleeve shirt}, with a {warm enthusiastic smile showing teeth, pointing at the folder | big warm smile | contemplative serious expression}.

{Any additional reference-specific elements — badges, icons with X/checkmarks, bold text banner, etc.}

Clean minimal composition optimized for YouTube thumbnail viewing.
```

Pass ONE golden ref (or Nate Herk raw ref if no golden exists) as `-r`.

## Prompt template for Nate style (no-face variants)

For icons-on-black sub-family (`--no-face` flag):

```
A YouTube thumbnail in the style of the reference image. Pure black background.

Large white bold text at the top reading '{VIDEO-SPECIFIC TEXT}.' with a subtle chalk-style underline scribble.

Below, two large rounded-square app icons side by side with a white '+' between them: on the left an orange-red rounded square with a white 8-pointed starburst icon (Claude), on the right a dark rounded square with a {TOPIC-RELEVANT ICON} and subtle warm glow.

No person in the image. Clean minimal composition optimized for YouTube thumbnail viewing.
```

## Anti-patterns for Nate style

- **Don't add podcast mic** — this style is studio, not podcast. Mic belongs to Matt style.
- **Don't use the warm bedroom background** — Nate uses cleaner studio looks
- **Don't add handwritten annotations or red curved arrows** — these are Matt style signatures
- **Don't layer Matt-style Kanban diagrams into Nate compositions** — they clash visually
- **Don't describe a flowchart / diagram** unless the reference literally shows one

## The 5-variant recipe for a new video

When Ray asks for 5 Nate-style thumbnails for a video:

1. **3 folder + /command variants** — pick different expressions (smiling, pointing, contemplative) or different crops (medium shot, close-up)
2. **1 CLI chat input** — if the feature is a command
3. **1 icons-on-black** (`--no-face`) — alternate for the no-face variant

Or if the video is about an integration / connection between tools, skew toward 3 icons-on-black + 2 folder.

## When saving a new winner

If Ray marks a new Nate-style generation as a winner:
1. Identify the sub-family (folder-command, icons-black, cli-chat, agent-diagram, whiteboard)
2. Copy to `research/golden-references/nate-style/<sub-family>/<descriptive-name>.png`
3. If the sub-family folder doesn't exist, create it
4. Mention it in the session so the user knows it's saved

Over time the Nate-style golden library should grow to match Matt's depth.
