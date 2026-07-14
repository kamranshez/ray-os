---
name: youtube-writer
description: >-
  Turn Ray's messy notes, memos, transcripts, or half-formed ideas into a
  filmable YouTube video for his main channel (@RAmjad), as an image-first
  bullet deck he riffs over (NOT a prose script). The workflow is always three
  phases in order: interview first to develop and stress-test the idea, then
  write the deck, then generate the images. Use this skill whenever Ray wants to
  make a video, write a YouTube script, turn a topic or memo or artefact into a
  video, plan video beats, or says "/youtube-writer", "write this up as a
  video", "let's make a video about X", "turn this into a YouTube video", or
  drops a topic clearly meant for the channel. Prefer this over free-handing a
  script: the interview is what makes the video good, and skipping it produces
  thin, generic decks.
---

# YouTube Writer

Ray films by talking over a deck of strong bullet points with images on screen. He does not read a prose script. So the deliverable is an **image-first bullet deck**: bullets dense enough to carry the argument when he riffs, plus fully specified image placeholders that become the visuals. The finished file lives at `socials/youtube/videos/<slug>.md`.

The single most important thing about this skill: **the interview comes first, and you do not write anything until the idea is developed.** The winning ingredients of a video (the real stakes, the sharp examples, the honest limitation, the one-sentence point) live in Ray's head, not in his notes. A deck written straight from raw notes is always thin and generic. The interview is where the video is actually made. Extract, do not invent.

Work in three phases, in order. Do not skip ahead.

---

## Phase 1: Interview first (one question at a time)

Interrogate the idea until you and Ray reach a genuinely shared understanding of the video. This mirrors a grilling/stress-test loop, and it is not optional.

Rules for the interview:

- **One question at a time.** Ask a single question, give your own recommended answer with a short reason, then wait for Ray's response before the next question. Asking several at once is bewildering and produces shallow answers.
- **Always recommend.** Every question comes with your best-guess answer, so Ray can just confirm or correct. He would rather react than generate from scratch.
- **Resolve dependencies in order.** Some decisions gate others. Settle the spine before the examples, the point before the plug. Walk the tree.
- **Verify technical claims.** If the video makes a factual claim about a tool, feature, or number, confirm it against the source (the binary, the docs, the data) before it goes in the deck. Use subagents here. An honest channel is the whole brand. If a claim turns out wrong, reshape the video around the truth.
- **Do not write until Ray signals the picture is complete.**

The ingredients to nail down before writing (ask only about the gaps, never re-ask what Ray already told you):

1. **The angle / spine.** What shape is this video? Derive 2 to 4 genuinely different angles from the material and let Ray pick one. The angle decides everything downstream. Consider a problem-first open (lead with the pain), a hidden-feature reveal, a contrarian claim, a demo-driven walkthrough, a mental-model explainer.
2. **The one-sentence point.** What is the single thesis the whole video serves? Everything else is support. If you cannot state it in a sentence, keep interviewing.
3. **The audience and the promise.** Who is this for and what do they get by the end?
4. **The examples.** Concrete, ideally real and mined from Ray's own world. Decide which are carried as full walkthroughs and which are a fast montage.
5. **When it is worth it / the practical framing.** The decision rule or takeaway the viewer leaves with.
6. **Honest limitations.** Where the thing bites, the cost, when NOT to use it. Ray's channel converts on honesty, so a real "here is the catch" beat makes the whole video stronger and pre-empts the top comments.
7. **The plug / CTA.** Which offer (usually agenticcoding.school), how hard, and where it lands. Default to a soft trust-sell woven at a concept boundary mid-to-late, ideally where the content itself references the offer, not a hard pitch.
8. **The close.** The verdict, a forward tease, and a comment or email ask.

---

## Phase 2: Write the deck

Once the idea is developed, write the whole deck in one pass. Save to `socials/youtube/videos/<slug>.md` (kebab-case slug, no H1 title, `status: draft`).

### Structure

```markdown
---
tags: [youtube, script, <topic-tags>]
status: draft
date: YYYY-MM-DD
source: "<where the idea came from>"
format: image-first bullet deck (Ray riffs over the bullets; each IMAGE block is a placeholder to generate)
---

---

## Beat 1: <name>

- <Rich bullet: a full sentence carrying the actual argument, the thing Ray will say, not a fragment.>
- <Another. Enough substance that Ray can riff without inventing the point live.>

> IMAGE `<slug>-<image-name>` (16:9): <fully specified composition: layout, what is on the left/right, the labels, the colors, the caption text. Unambiguous enough to generate without guessing.>

---

## Beat 2: <name>
...
```

### Rules that keep it filmable and good

- **Bullets must be rich, not thin.** Each bullet is a full sentence that states the actual argument or line, so Ray can talk over it without re-deriving the point on camera. Thin fragment bullets are the number one failure mode of this format; do not ship them.
- **Beats are `## Beat N: <name>`**, separated by `---`. Aim for a tight set that serves the spine (often 6 to 11 beats). Cut anything that does not earn its place, and merge beats that argue the same thing.
- **Image placeholders are fully specified.** Use the `> IMAGE \`<slug>\` (aspect): <composition>` convention. Name the exact relationship being drawn, the labels, the color language, and a caption. "It is not clear what the image depicts" is a real Ray complaint; every placeholder must be unambiguous. Give a beat with any visual shape at least one image, and never leave a 60-second stretch with nothing on screen but talking.
- **Slugs are globally unique kebab-case**, prefixed with the video slug (e.g. `observer-loop`, `observer-four-eyes-bank`), because all images land in one flat vault-root `images/` folder.
- **No em or en dashes, ever. Hard rule, zero exceptions**, including in beat headers and IMAGE lines. Use commas, periods, or "to" for ranges. After writing, sweep the file for `—` and `–` and remove every one, scaffolding included.
- **Second person, direct, no hedging.** Clean written register; Ray adds his verbal tics live.

### Retention engineering (bake in, do not bolt on)

These come from the channel's own curves:

- **The first 30 to 40 seconds carry the video.** Name the subject in the first two sentences, show the proof or the finished thing immediately, and make an explicit promise. No branding, no slow setup.
- **Plant a delayed payoff around 40 to 60%.** The mid-video sag is where videos die. If there is a demo or an experiment, start it early, tease the result, and pay it off mid-video.
- **Give viewers dense artifacts to pause on** (exact prompts, configs, diagrams). They create the rewatch spikes that lift the back half.
- **The CTA lands mid-to-late at a concept boundary, woven into the content.** The best case is when the content itself references the offer. Trust-sell over hard pitch.
- **Close with a verdict, a forward tease, and a comment or email ask.** Honest limitations included; the personal verdict builds trust.

---

## Phase 3: Develop the images

After the deck is written and Ray is happy with it, generate the visuals by invoking the **excalidraw-codex** skill. Do not hand-roll image generation; that skill owns the engine, the dark-mode aesthetic, and the parallelism.

- **Dark mode, hand-drawn excalidraw** is the default (excalidraw-codex already defaults to the dark charcoal background).
- **5 variations per image** (`-n 5`) so Ray can pick a favorite per slug.
- **Full parallel fan-out.** Launch every image at once (excalidraw-codex now defaults to this via a single background driver script), so a whole deck renders in one wave rather than staged batches.
- Pass each IMAGE block's composition text **verbatim** as the prompt for that slug.
- When generation finishes, **embed all 5 variations under each placeholder** as filename-only wikilinks (`![[<slug>-1.png]]` ... `![[<slug>-5.png]]`) so Ray can choose. Retry only the slugs that failed (excalidraw-codex logs each separately). Drop any image whose beat was cut.

---

## Follow-ups to offer

Once the deck and images are done, offer:

- Title and thumbnail A/B testing via the `youtube-ab-tester` skill.
- Pulling live YouTube stats into the frontmatter once the video is uploaded (see `socials/youtube/CLAUDE.md` for the stats format).
