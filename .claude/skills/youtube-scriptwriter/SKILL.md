---
name: youtube-scriptwriter
description: Interview Ray about a video idea (starting with which angle/format to go for), then turn his messy thoughts into a full YouTube script for the main channel (@RAmjad). Use whenever Ray wants a YouTube video scripted: "write a YouTube script", "script this video", "turn these thoughts into a video", "make this a video for the channel", or when he dumps a messy dictated idea, tweet, discovery, or feature note and mentions filming or the channel. Also use when other skills point here (youtube-ab-tester and youtube-outlier-scout reference youtube-scriptwriter for scripting). Do NOT use for Agentic Coding School class videos (that is class-scriptwriter) or for titles/thumbnails alone (that is youtube-ab-tester).
---

# YouTube Scriptwriter

Turn Ray's messy thoughts into a filmable script for the main channel, through a short interview that starts with the angle. The interview exists because the winning ingredients (stakes, receipts, demo, verdict) live in Ray's head, not in the messy notes. Extract them; don't invent them.

The output is a full script in the established corpus shape: the same format as the scripts in `socials/youtube/videos/uploaded/`. Those are the actual scripts of the analyzed videos, so treat them as ground truth over anything described here.

---

## Workflow

1. **Ingest.** Read whatever Ray gives you: dictated text, a file, a tweet, a transcript. Assume dictation errors; interpret intent.
2. **Read the playbook.** Read `references/format-playbook.md` for what performs and why. It is short and load-bearing; every downstream choice keys off it. When an angle decision needs actual numbers or a precedent video (has this title shape worked before? how did the closest prior video retain?), pull `references/performance-data.md` for the full ranked table, retention curves, and per-video format ledger.
3. **Viability critique.** Before any interview question, judge whether this should be a video at all (rubric in `references/interview-guide.md`). Deliver the verdict honestly in chat: strong / viable with changes / weak, with the reasoning and the closest precedent video's numbers. Ray would rather hear "this is a newsletter, not a video" before filming than after. A weak verdict does not end the flow; it changes Round 1 (include a park/repurpose option and make the fix explicit).
4. **Round 1 — the angle.** Derive 2-4 genuinely different angles from the material and present them with AskUserQuestion. Each option = an angle label, the format it maps to, why that format earns its keep (one performance fact from the playbook), and a preview with a title direction plus a two-line hook sketch. Ray picks the direction before any other question gets asked, because the angle determines which ingredients matter.
5. **Round 2 — the missing ingredients.** Read `references/interview-guide.md`. Check the eight ingredients against what the messy thoughts already contain, and ask ONLY about the gaps: one AskUserQuestion round of up to 4 questions, a second round only if something load-bearing is still missing. Never ask about something Ray already told you.
6. **Read golden scripts.** Read the 1-2 scripts from `socials/youtube/videos/uploaded/` that match the chosen angle (the playbook maps angles to files). Lock in the section shape, stage-direction style, and image-placeholder convention.
7. **Draft.** Write the full script in one pass (see Output format). Prose the camera follows, not an outline. Ray improvises over it live, so clean written register; his verbal tics are added at delivery, not in the file.
8. **Dash sweep.** Search the draft for `—` and `–` and rewrite them out. Hard rule, zero exceptions.
9. **Save** to `socials/youtube/videos/<slug>.md` (kebab-case, no H1, `status: draft`). Report the path.
10. **Offer follow-ups**: title/thumbnail A/B testing via youtube-ab-tester, image generation for the 🎨 DRAW placeholders via the excalidraw skills.

---

## Output format

Match the `uploaded/` corpus exactly. Skeleton:

```markdown
---
tags: [youtube, script, <topic-tags>]
status: draft
date: YYYY-MM-DD
source: "<where the idea came from, if anywhere>"
---

## Title Options

| # | Formula | Title |
|---|---------|-------|
| 1 | <formula name> | <title> |
| 2 | ... | ... |
| 3 | ... | ... |

Coined term: **"<the phrase viewers will repeat>"**. Format: <angle summary>. Pitch: <CTA plan: which offer, what urgency, where it lands>.

---

## Hook (0:00-0:35)

*<Stage direction: what is on screen from second zero.>*

<Verbatim hook prose. These are the highest-leverage lines in the file.>

---

## <Section Name> (M:SS-M:SS)

*<Stage direction.>*

<Section prose.>

> 🎨 DRAW `<slug>-<image-name>` — <what the diagram shows, naming the relationship being drawn>

![[<slug>-<image-name>.png]]
```

Rules that keep this filmable:

- **Timestamped `##` sections**, `---` between them, target total 8-20 min (strategy/insider at the long end, single-feature at the short end; 1,500-3,800 words).
- **Titles complementary to the thumbnail, never redundant with it.** The file uses the table above; when discussing titles in chat with Ray, use a numbered list instead.
- **Second person, direct, no hedging. No em or en dashes, ever.** Hyphens inside compound words are fine.
- **Stage directions in italics** at section tops: what is on screen, when to cut to b-roll, when a quote sits on screen.
- **Image placeholders** use the `> 🎨 DRAW` + `![[name.png]]` convention; name the relationship being drawn, not just the topic. One per section that has a shape; a 60+ second stretch with nothing on screen but talking needs one.
- **Demo section is concrete**: the exact prompt spoken verbatim, which real project it runs on, and what to do while it runs.
- **A Key Insight blockquote and a short Close** (1-3 lines) at the end.

---

## Retention engineering (bake into every draft)

These come from the channel's own retention curves; the playbook has the numbers.

- **The first 35 seconds carry the video.** Broad clickers decide by the 10% mark. Name the subject within two sentences, show proof or the finished thing immediately, and make an explicit promise. No branding, no setup.
- **Plant a delayed payoff at 40-60%.** The mid-video sag is where videos die. Start an experiment/demo early, tease the result, pay it off mid-video. "Run the thing, teach while it runs, return for the payoff" is the channel's signature move; use it whenever the demo has wait time.
- **Give viewers things worth pausing on.** Dense on-screen artifacts (exact prompts, configs, diagrams) create the rewatch spikes that lift the back half.
- **CTA lands mid-video at a concept boundary, woven into the content** (best case: the demo itself implements or references the offer). Trust-sell videos skip the hard pitch entirely and convert on "I only upload when there's something worth saying".
- **End with a verdict, a future tease, and a comment/email ask.** Honest limitations included; the personal verdict is a trust builder, not a weakness.
