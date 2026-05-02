---
name: excalidraw-gen
description: Remind Codex to use the built-in image generation tool for excalidraw-style explanation images, diagrams, thumbnails, and visual explanations instead of local scripts, Gemini, or Codex-generated SVG/canvas art. Use when the user wants an excalidraw-style image, hand-drawn diagram, visual explanation, article thumbnail, or illustrated concept.
---

## Core Rule

Use the built-in image generation tool for raster image creation.

Do not run the old Gemini script, do not use `npx ts-node scripts/generate.ts`, and do not ask for or depend on `GEMINI_API_KEY`. This skill is a routing reminder: when the task is to create excalidraw-style bitmap images, call the built-in image generation capability directly.

Use code only when the user explicitly asks for editable SVG, Excalidraw JSON, HTML/CSS/canvas, or repository-native assets instead of generated bitmap images.

## Prompt Content Rule

When the user provides source material, keep the source material intact in the image prompt. Do not summarize away the details that the image needs.

For long documents, preserve the full relevant chunk verbatim inside each prompt when practical. If the content is too large for a single prompt, split it into semantic chunks and generate one image per chunk.

## Semantic Chunking

Do not chunk solely by `## ` headings. Look for:

- Concept definitions, such as "What is X?"
- Distinct examples or scenarios
- Shifts in topic within a section
- Before/after comparisons
- Standalone explanations

Each chunk should map to one useful image. A single `## ` section may produce multiple images if it covers multiple concepts. When analyzing content, identify these semantic boundaries before generating.

## Before Generating

If the user has not already made the scope clear, ask which mode they want:

1. **Specific section** - Generate one image or a small set of variants for content they provide
2. **Whole file** - Parse a markdown file into semantic chunks and generate images for each chunk

If the user's request is already clear, proceed without asking.

## Built-In Image Generation Workflow

For each requested image:

1. Build a prompt for the built-in image generation tool.
2. Include the full relevant source content or chunk.
3. Specify an excalidraw-style visual: hand-drawn black marker lines, simple shapes, arrows, labels, sparse accent color only when helpful, and a clean educational composition.
4. Specify the target aspect ratio:
   - Default diagrams: `16:9`
   - X/Twitter article thumbnails: `21:9` or the closest wide cinematic ratio available
   - Square social images: `1:1`
   - Mobile/story images: `9:16`
5. Generate variants only when the user asks for options or when selection is part of the workflow.

## Prompt Requirements For Excalidraw-Style Diagrams

Start prompts with:

```text
Create an excalidraw-style hand-drawn diagram on a pure white background (#FFFFFF). No gradients, no textures, no shadows, no photo-realism.
```

Include:

- The concept or section title
- The full relevant source content
- Layout guidance, such as flowchart, comparison, system map, layered stack, timeline, or before/after
- Text constraints: short labels, readable at thumbnail size, no dense paragraphs
- Visual constraints: black hand-drawn lines, simple icons, arrows, boxes, minimal accent colors

End prompts with:

```text
Background must be solid white (#FFFFFF). Keep the image clean, legible, and hand-drawn in an Excalidraw-like style.
```

## X Article Thumbnails

For X/Twitter article cover images, use a wide cinematic aspect ratio. Use a bold, high-contrast composition with minimal text, usually 3-5 words maximum. The image must be readable at small sizes in the X feed.

For thumbnails, white backgrounds are optional. Use vibrant colors when they make the cover stronger, but keep the composition simple and readable.

## Saving And Embedding

When the built-in image generation tool returns an image, save it into a descriptive kebab-case folder near the target markdown file when the environment exposes a file path or generated asset path.

Recommended folder pattern:

```text
images/<section-name-kebab-case>/
```

Use Obsidian image embeds in markdown:

```markdown
![[images/section-name/image-name.png]]
```

Place embeds at the end of each relevant section, before the next `---` or `##` heading.

## Important Notes

- Prefer the built-in image generation tool for all bitmap output.
- Do not use the Gemini API workflow from the old version of this skill.
- Keep file and folder names kebab-case.
- Do not delete existing generated images without explicit user permission.
- If multiple variants are generated, embed or show the variants so the user can pick their favorite.
- For markdown files in this Obsidian vault, do not add H1 titles.
