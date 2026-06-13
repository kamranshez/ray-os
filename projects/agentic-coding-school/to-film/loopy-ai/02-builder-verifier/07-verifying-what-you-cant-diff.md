---
duration: 12-16 min
batch: 2
order: 7
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [verifying-what-you-cant-diff, image-gen-verifier]
---

> STUB. The capstone build of the chapter — a hands-on end-to-end build of the Excalidraw verifier skill. The concept was mentioned on camera (the GPT Image 2 slides example); this video *builds it properly*.

## Thesis

Text you can grep, lint, and test. An image has no diff, no exit code, no assertion. So you have to *manufacture* the external check — and that manufacturing is the skill.

## The case study — the Excalidraw skill, built live

The honest version of how it actually went: first attempts just generate and trust the output. Then the failures show up — wrong aesthetic, text overflowing, white background when you wanted dark (the recent dark-mode switch). There's no `assert` for "this looks right."

## The build — bolting a verifier onto a soft artifact

- **The rubric is the verifier.** Encode taste as criteria a vision model can score: dark canvas? hand-drawn stroke? caption legible? one concept per image? (This is the "old taste → rubric taste" move from the L7 closing segment, shown at the bench.)
- **The judge agent** scores each generation against the rubric; below threshold → regenerate with the critique fed back. That's plain L2, with a vision judge instead of pytest.
- **Builder writes the prompt, verifier compares to a reference.** Mirror the real workflow: builder writes the image-gen prompt, the generated image is compared against a reference image, feedback flows back, prompt changes, regenerate — loop until close enough. (This is exactly how the class slides got migrated from Gemini Nano Banana to GPT Image 2.)
- **Where it's still fuzzy** — be honest that vision judging is softer than a unit test, so a cheap human glance at the end stays in the loop (forward-ref the autonomy dial).

## Map onto the five components

- **Work** — generate image from prompt.
- **Check** — vision-model rubric score / reference comparison (the part you had to build).
- **Terminate** — score ≥ bar or max retries (callback to 05-where-to-set-the-bar).
- **State** — the critique carried into the next generation.

## Demo

Run the skill, show a generation failing the rubric, show the judge's written critique, show the regen passing. Put the rubric file on screen — unromantic, a few lines of criteria.

## Key Insight

> When the output isn't text, the verifier doesn't come for free. Building it is the loop.
