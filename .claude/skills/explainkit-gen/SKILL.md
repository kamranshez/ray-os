---
name: explainkit-gen
description: Generate explanation diagrams via the ExplainKit MCP server (mcp__explainkit__*). Supports four styles — Excalidraw Robot (hand-drawn), Sketchnote, Pastel Notebook, Midnight Sketch. Use when the user wants visual explanations, section diagrams for a video script, slide visuals, or any "make a diagram of X" request and they want ExplainKit (not the local Gemini-based excalidraw-gen). Triggers on "ExplainKit image", "explainkit-gen", "diagram with explainkit", "use ExplainKit", or any request that names ExplainKit by name.
---

## When to use this vs excalidraw-gen

- **explainkit-gen (this skill)** — uses the ExplainKit MCP. Cloud generation, no local API key needed, four bundled styles, bulk job API, manifest download. Use when the user asks for ExplainKit by name, or when you want one of the non-Excalidraw styles (Sketchnote, Pastel Notebook, Midnight Sketch).
- **excalidraw-gen** — local Gemini script, white-background excalidraw only. Use when the user wants the original excalidraw-gen flow or has a strong preference for the Gemini pipeline.

If the user just says "make a diagram", default to excalidraw-gen unless they invoke ExplainKit by name.

## Style catalogue

Cache these IDs — `list_styles` rarely changes. Re-fetch only if a styleId errors.

| Slug | Name | styleId |
|---|---|---|
| `excali-robot` | Excalidraw Robot | `3b523978-b59e-42af-9eb1-987c28fce240` |
| `sketchnote` | Sketchnote | `02a302b5-eb57-48e2-a8ac-8a8342f118e2` |
| `pastel-notebook` | Pastel Notebook | `6a7608e0-aeb5-45ce-aa58-2282d0697302` |
| `midnight-sketch` | Midnight Sketch | `afbead7b-006b-4b33-9f61-73317d46c148` |

Default style: **Excalidraw Robot** (matches the visual language Ray uses across his class scripts).

## First: ask the user (only if scope is unclear)

If the user already pointed at a file or section, skip this. Otherwise:

- **Specific section** — they hand you content, you generate one batch
- **Whole file** — split a markdown file by `## ` (or semantic chunks) and batch every section

Also confirm style if they did not pick one. Excalidraw Robot is the safe default.

## Semantic chunking

Same rule as excalidraw-gen — don't chunk solely by `## ` headings. Look for:
- Concept definitions
- Distinct examples or scenarios
- Before/after comparisons
- Topic shifts inside one section

Each chunk → one generated image.

## Writing good ExplainKit prompts

Unlike the Gemini script, **do not paste raw section content verbatim.** ExplainKit's models reason better from a tight visual brief than from a wall of prose. Write a 2–6 sentence prompt that describes:

1. **What the diagram is** (one sentence — "Flow diagram of...", "Side-by-side comparison of...", "Three robot characters in a row representing...")
2. **The concrete elements** — labels, arrows, characters, boxes, text on each label. Be specific. ExplainKit draws what you describe; vague prompts produce vague pictures.
3. **The layout** — left/right, top/bottom, vertical flow, grid, split with a divider.
4. **Captions / titles** — quote the exact text you want rendered.
5. **Style reinforcement** — end with `"Excalidraw hand-drawn sketch style on white background."` (or the equivalent for the chosen style).

Keep prompts under ~1500 chars. The hard ceiling is 2000.

**Bad prompt:** `"Subagents as delegation"`
**Good prompt:** `"Mental model of subagents as delegation. Show a 'Main Thread' robot at the centre handing a small task card to a 'Subagent' robot on the side. Label the outgoing arrow 'bounded task', the return arrow 'result'. Caption at bottom: 'Subagents = delegation, not decoration.' Cross out a thought bubble that says 'magic extra brains'. Excalidraw hand-drawn sketch style on white background."`

## The flow (ID-first, low token)

This is the exact pattern that worked for the 04-subagents-in-general script — 8 images in one batch, ~90s wall clock.

### 1. Bulk-create jobs

Call `mcp__explainkit__generate_image` **once** with all jobs (max 10 per call, 1–8 image variations per job). Each job needs `prompt` and `styleId`. Optional: `aspectRatio` (default `16:9`), `imageCount` (default 1), `model`, `size`.

```
generate_image({ jobs: [
  { prompt: "...", styleId: "<excali-robot uuid>" },
  { prompt: "...", styleId: "<excali-robot uuid>" },
  ... up to 10
]})
```

You get back `jobId` + `estimatedCompletionSeconds` per job. **Save the jobIds** — they're the only handle you'll keep in context.

### 2. Wait locally

Sleep the largest `estimatedCompletionSeconds` (usually 25–60s). Use a Bash `run_in_background` sleep. Do not block inside the MCP — never set `lean:false` to "wait".

### 3. Poll lean status

`mcp__explainkit__get_job_status({ jobIds: [...], lean: true })` — returns just `status` + `imageIds`. Repeat every 30–60s until all jobs report `completed`. Most batches finish in 60–120s total.

### 4. Get the download manifest

`mcp__explainkit__get_download_manifest({ imageIds: [...] })` — returns presigned URLs that expire in **1800 seconds**. Do not call this until you are about to download. If a URL expires, just call manifest again with the same imageIds.

### 5. Download in parallel with curl

`curl -s -o <name>.png '<url>'` per image, all backgrounded with `&` and a final `wait`. Quote the URL — it contains `&` characters.

```bash
mkdir -p /path/to/images/<section>/
cd /path/to/images/<section>/
curl -s -o the-mental-model.png '<url1>' & \
curl -s -o spawn-agent-tool.png '<url2>' & \
... & \
wait
```

Name files with the **semantic name** (e.g. `the-mental-model.png`), not the imageId. This matches the `> IMG · <name>.png` markers Ray puts in scripts.

## Token discipline (from MCP server instructions)

- Keep `jobIds` and `imageIds` in your own state. Never paste prompts, URLs, or image metadata back into a tool call unless you need it.
- Never use `lean: false`, `includeUrls: true`, `get_image`, or `list_images` for bulk work — they balloon context with metadata you do not need.
- The MCP server cannot write files to disk. Always download via `curl` from your shell.
- Never use any cached download URL — they expire fast. Refresh via `get_download_manifest` instead.

## Aspect ratios

Supported: `16:9` (default), `4:3`, `3:2`, `1:1`, `2:3`, `3:4`, `9:16`, `21:9`.

- Section diagrams in a video script: `16:9`
- X article cover image: `21:9`
- Vertical / shorts thumbnail: `9:16`
- Square social: `1:1`

## Output convention

Save all images for one section under one subfolder, kebab-case after the section title:

```
projects/<class>/<video>/images/<video-slug>/<image-name>.png
```

This matches the `![[images/<video-slug>/<name>.png]]` Obsidian embed Ray uses across the `to-film/` tree.

## Embedding in markdown

If Ray's script already has `> IMG · <name>.png` markers followed by `![[images/<dir>/<name>.png]]`, just save the file with the matching name and the embed resolves automatically — no edit needed.

If embeds are missing, add them under the section, one per line, before the next `---`:

```markdown
![[images/<section>/<name>.png]]
```

If you generated multiple variations per concept (`imageCount > 1`), embed all of them so the user can pick a favourite.

## Whole-file mode

For an entire markdown file:

1. Read the file, identify every `> IMG · <name>.png` marker (or semantic chunk).
2. Write one tight prompt per image (see "Writing good ExplainKit prompts").
3. Submit them in **one** `generate_image` call if there are ≤10. Split into two calls if more.
4. Wait, poll lean, manifest, parallel-curl download — exactly the flow above.
5. Verify every expected file exists; report any missing.

ExplainKit handles the parallelism server-side, so unlike excalidraw-gen there is no "batch of 2" rate-limit dance.

## Troubleshooting

- **Job stuck `running` past 3 minutes** — re-poll once more, then assume it failed. Re-submit just that prompt.
- **`styleId` rejected** — call `mcp__explainkit__list_styles` to refresh the catalogue; the IDs at the top of this file may have changed.
- **Curl downloads a tiny file (<10KB)** — URL expired or signing failed. Re-run `get_download_manifest` and retry.
- **Text in the diagram is garbled** — shorten the captions in the prompt, quote them in single quotes, and put them on their own sentence ("Caption: 'Subagents = delegation.'").

## What this skill does not do

- It does not refine images (`refine_image` exists but is rarely worth the round-trip — regenerate with a tighter prompt instead).
- It does not write files for you — always `curl` from Bash.
- It does not pick image styles for the user — if they don't say, default to Excalidraw Robot and tell them which one you used.
