---
name: class-scriptwriter
description: Turn a raw idea, source tweet, video transcript, feature announcement, or rough outline into a polished video script for Ray's Agentic Coding School classes. Use this skill whenever the user says "write a class script", "turn this into a class video", "script this for the [business/claude-code/prompt-engineering/skills/context-engineering/techniques/claude-chat/claude-cowork/correction] class", "draft an agentic coding school video", or whenever the user is staging content in `/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/` and wants it written up. Default to this skill for any new file destined for the `to-film/` tree, even if the user does not name it explicitly. Produces an essay-style markdown script with the correct frontmatter, horizontal rules between sections, inline image embed placeholders, and a Demo section, written in Ray's direct second-person voice.
---

# Class Script Writer

Write video scripts for Ray's Agentic Coding School in the same voice and structure as the already-filmed classes. The output is not an outline or a bullet list of beats. It is an essay the camera follows, with clean section breaks, embedded image placeholders, and a concrete demo at the end.

---

## When to use

Trigger on any of these:

- Explicit: "write a class script", "script this for the X class", "turn this tweet/transcript into a class video", "agentic coding school script".
- Implicit: the user is dropping content into `/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/<class>/` and wants it written, or they hand you a source (tweet, transcript, outline, announcement) and mention filming, classes, or the school.
- Rewrites: the user has a thin outline-style script in `to-film/` and asks to rewrite it in the style of an existing filmed class. Overwrite the file in place.

If the class folder is ambiguous, ask which class it belongs to before writing. The classes are:

`business`, `claude-chat`, `claude-code`, `claude-cowork`, `context-engineering`, `correction`, `prompt-engineering`, `skills`, `techniques`.

---

## Inputs you need

Gather before writing. Ask only for what is missing.

1. **Source material** — tweet, transcript, outline, article, or the user's verbal pitch. If the user references a URL or file, read it first.
2. **Class folder** — one of the nine above.
3. **Slug** — kebab-case filename. Derive from the topic if not given.
4. **Chapter / batch_name** — look at sibling files in the same class folder to match existing chapters, or ask if nothing fits.
5. **Duration target** — default `"10-14 min"` unless the user specifies.

The output path is `/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/<class>/<slug>.md`.

---

## Frontmatter

Every script starts with this block. Fill every field.

```yaml
---
duration: "10-14 min"
batch: 1
order: 2
batch_name: "Research & Intelligence"
class: "business"
chapter: "Research & Intelligence"
---
```

Pick `batch` and `order` by scanning the sibling files in the target class folder. If everything there is order 1, use 2. Do not leave any field blank.

---

## Voice and structure

Read `references/style-guide.md` for the full rules. The short version:

- Second person. Direct. Confident. No hedging.
- Short paragraphs, one to three sentences. White space matters.
- Vary sentence length. Use fragments for emphasis. Rhetorical questions work.
- Bold key phrases sparingly for scannability.
- `##` headings, never `#`. Separate major sections with `---` on their own line.
- **No em dashes and no en dashes, ever.** Ray has a hard rule on this. Use commas, periods, or rephrase. A hyphen inside a compound word (kebab-case, zero-to-one) is fine. A dash as punctuation between clauses is not.
- Lead with the point. State it, then support it.
- Inline sources as `Source: https://...` right under the claim, not bundled at the top.

The reference scripts to imitate are bundled in `references/`:

- `references/scaling-taste.md` — long-form, idea-dense, multiple "Why this works" and "The X Loop" sections. Good template for conceptual videos.
- `references/progressive-disclosure.md` — tighter, problem-to-solution arc with bold one-liners and industry context. Good template for a technique or pattern video.

Skim both before writing. Match whichever matches the user's topic best.

---

## Required sections

Every script has these, in this order. Section names can flex to fit the topic.

1. **A cold-open section with a one-sentence thesis.** No fluff intro. State what this video is about in the first paragraph.
2. **The problem.** What is broken today, or what everyone is doing wrong. Often a good spot for an image, but only if the problem has a shape (see the placement test under Images).
3. **The core insight or solution.** The single idea the video exists to deliver.
4. **Supporting sections.** Two to four of them. How it works, why it works, where it came from, what the layers are. Use `---` between each.
5. **Demo.** A concrete, numbered walkthrough of what the camera will show. Not vague. Specific tools, specific outputs.
6. **Key Insight** (optional but recommended). A single blockquote that could be pulled as a tweet. Format:

   ```markdown
   > A single crisp sentence that captures the whole video.
   ```

7. **A closing beat.** One to three lines. What changes for the viewer after they watch this.

---

## Images

Use Obsidian embed syntax. The images directory is keyed on the slug.

```markdown
![[images/<slug>/<name>.png]]
```

Describe what each image should show inline in square brackets above the embed so the excalidraw-gen skill can pick it up later. The description must name the *relationship being drawn*, not just the topic:

```markdown
[IMAGE: dark chalkboard, two panels labeled Knowledge and Your Life, lightning bolt between them]

![[images/notebooklm-intake/the-problem.png]]
```

### Where to place a placeholder

**Lean generous.** The shape gate below is what keeps you honest, so once a beat passes it, default to drawing it. In practice the common failure is too few images, not too many: an important section ends up a wall of narration with nothing to anchor it. So the disposition is "draw it unless there's a reason not to," not "withhold unless it's one of the top three."

Run every candidate beat through this pipeline, in order:

1. **Gate, the shape test.** A beat is only eligible for an image if the idea has a *shape*: nesting, flow, direction, partition, cycle, substitution, or convergence. Ask "does this sentence lose anything if it stays as words on the page?" If the answer is no, do not draw it. This is the one hard filter, and it kills decoration at the source. "The model was trained on more data" has no shape. "Eight loop levels nest inside each other" does.
2. **Draw every eligible beat.** Every beat that clears the gate gets a placeholder by default, not just the load-bearing ones. Ranking only matters as a trim step: if you blow past the ceiling, keep the beats carrying a "therefore" the video would collapse without, and drop the weakest-shaped ones first. Below the ceiling, do not withhold an eligible diagram just because another beat is more important. A section that introduces a real concept with a shape should almost never be left with zero visuals.
3. **Pacing backstop.** If any stretch longer than about sixty seconds of unbroken narration has no visual, that gap needs a diagram, find the strongest shaped beat in it and draw it. If two diagrams compete for the same beat, keep both if they show different things, otherwise push the lower-stakes one to the next visual-less stretch.

Treat "this feels like a lot to follow" (cognitive load) as a secondary hint only. It is a liar at the moment of writing: everything feels heavy while you are explaining it. But under the generous default it errs the right way, so let it nudge you toward an extra diagram, not away from one.

### How many

At least one diagram per major section, plus any sub-beat inside a section that introduces its own shaped, load-bearing idea. A meaty section can carry two or three. Soft ceiling around ten to twelve per script: past that, start trimming the weakest-shaped beats. The hand-drawn style still wants a little breathing room, so a beat with no shape stays as words, but a real concept with a shape should get drawn rather than skipped to stay scarce.

---

## Workflow

1. Read the source material the user gave you. If it is a URL, fetch it. If it is a transcript file, read it.
2. Confirm class, slug, chapter if any are unclear. Do not guess chapter, ask.
3. Read the two reference scripts in `references/` to lock in voice.
4. List sibling files in the target class folder to check `batch`, `order`, and avoid duplicate chapters.
5. Draft the script in one pass, essay-style, top to bottom. Do not write it as an outline first.
6. Do a second pass specifically to remove em and en dashes. Search the file for the characters `—` and `–`. Replace them with commas, periods, or rewritten sentences. This is a hard rule, not a preference.
7. Write the file to `/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/<class>/<slug>.md`.
8. Report the path and offer to generate the images via the `excalidraw-gen` skill if the user wants them.

---

## Common mistakes to avoid

- **Outline style.** The business-folder templates like `deep-research-with-exa.md` are outlines, not scripts. Do not copy that shape. Copy the scaling-taste and progressive-disclosure shape instead.
- **Academic voice.** Do not write "it could be argued that" or "one might consider". Write "the bottleneck is context" and move on.
- **Em dashes leaking in.** Models love em dashes. You do not. Grep for them before finishing.
- **Vague demo.** "Show how it works" is not a demo. "Start from a blank NotebookLM account, bulk ingest 30 Lenny episodes, run six parallel cited queries, save three experiments to Obsidian" is a demo.
- **Missing frontmatter fields.** Every field filled, every time.
- **Title as H1.** Obsidian uses the filename. Do not put `# Title` at the top of the file.

---

## Why this skill exists

Ray has filmed roughly a hundred of these videos. The ones that land have the same shape: a thesis in the first paragraph, a crisp problem, an insight that feels earned, a demo the viewer can picture, a closing line that makes them want to try it today. The ones that flop are outlines dressed up as scripts, or model-voiced essays with em dashes and hedged claims.

The job of this skill is to hit that shape every time, in Ray's voice, with the right file path and frontmatter, so the script is ready to film without a rewrite pass.
