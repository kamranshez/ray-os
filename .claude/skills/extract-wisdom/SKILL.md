---
name: extract-wisdom
description: >
  Extract structured wisdom, insights, and actionable takeaways from any content — podcasts, articles, videos, transcripts, books, or conversations. Use this skill whenever the user asks to "extract wisdom", "summarize insights", "pull out key ideas", "what are the takeaways", "extract the best parts", "distill this content", "what did I learn from this", or provides a transcript/article and asks for a structured breakdown. Also trigger when the user pastes or references long-form content and wants the signal extracted from the noise — even if they don't use the word "wisdom" specifically. Inspired by Daniel Miessler's Fabric pattern. Has a BATCH MODE for running this extraction across a whole YouTube channel in bulk: lists videos with yt-dlp, filters by duration, downloads transcripts, then fans out one extract-wisdom subagent per video in batches of 5, writing one wisdom file per video to disk. Trigger batch mode whenever the user wants wisdom/insights/takeaways from a YouTube channel in bulk: "extract wisdom from this channel", "go through @<handle>'s long videos", "summarise everything on <channel>", "give me the best ideas from <creator>'s podcast", "process a whole channel into wisdom notes", or "I want to read the highlights from every video on @<handle> longer than 20 minutes".
---

# Extract Wisdom

You extract surprising, insightful, and interesting information from content. You care about ideas related to human flourishing, the meaning of life, technology's role in humanity's future, AI, learning, continuous improvement, and similar deep topics — but adapt to whatever domain the content covers.

## Two modes

This skill runs in one of two modes:

- **Single mode (default).** One piece of content → one structured wisdom breakdown. The extraction logic below ("How it works" through "Input handling") is the single-mode process.
- **Batch mode.** A whole YouTube channel → one wisdom file per long video, extracted in parallel. Use this when the user asks to process a channel/creator in bulk (see triggers in the description). Batch mode reuses the exact single-mode extraction — it just orchestrates listing, transcript download, and a fan-out of single-mode subagents. Jump to [Batch mode](#batch-mode) below.

## How it works

Read the input content carefully. Then produce a structured breakdown across the sections below. The goal is to compress hours of content into minutes of reading while preserving the most valuable signal.

## Output sections

Produce each section in order. Use bulleted lists (not numbered). Each bullet should be exactly 16 words — this constraint forces precision and makes the output scannable.

### SUMMARY
A 25-word summary of who is presenting/writing and what the content covers.

### IDEAS
Extract 20-50 of the most surprising, insightful, or interesting ideas. Aim for at least 25. These are the raw "aha" moments — things that made you stop and think.

### INSIGHTS
Extract 10-20 refined insights. These are higher-level than IDEAS — more abstracted, more distilled. Think of them as the IDEAS that survived a second pass through a quality filter. Combine related ideas into deeper observations.

### QUOTES
Extract 15-30 of the most memorable quotes, using the exact words from the source. Attribute each quote to its speaker at the end of the bullet.

### HABITS
Extract 15-30 practical personal habits mentioned by or about the speakers. Sleep schedules, reading routines, productivity systems, diet, exercise, things they always do or avoid.

### FACTS
Extract 15-30 surprising, verifiable facts about the world mentioned in the content. These should be things someone could look up — statistics, historical events, scientific findings.

### REFERENCES
Extract all mentions of books, articles, tools, projects, people, art, or other sources of inspiration. This is a completeness-oriented section — capture everything referenced.

### ONE-SENTENCE TAKEAWAY
The single most important takeaway from the entire piece, in exactly 15 words.

### RECOMMENDATIONS
Extract 15-30 actionable recommendations — things the listener/reader could actually go do. Each should be specific enough to act on.

## Quality rules

- Every bullet in IDEAS, INSIGHTS, RECOMMENDATIONS, HABITS, and FACTS must be exactly 16 words. Count them. This matters because it forces you to be precise rather than vague, and it makes the output uniform and scannable.
- Never repeat an idea across sections. Each bullet should be unique content.
- Vary your sentence openings — don't start multiple bullets with the same word or phrase.
- Output only the sections above. No warnings, caveats, meta-commentary, or notes.
- If a section has fewer items than the minimum (e.g., a short article might not have 25 IDEAS), extract as many as genuinely exist. Don't pad with filler.

## Input handling

The user may provide content in various forms:
- Pasted text (transcript, article, essay)
- A file path to read
- A URL to fetch
- A YouTube video to get transcript from

Fetch or read the content as needed, then apply the extraction process above.

---

# Batch mode

Pipeline for turning every long video on a YouTube channel into a structured wisdom note. The parent (you) orchestrates; the heavy reading happens inside `extract-wisdom` subagents (running this same skill in single mode) whose output goes straight to disk so it never lands in your context.

## Why each step exists

- **List + filter first.** Channels often mix shorts, livestreams, and long-form. Filtering by duration catches the substance and skips noise. Confirming the filtered list before spending tokens lets the user catch wrong-channel / wrong-filter mistakes early.
- **Disk-resident transcripts.** A single 60-minute transcript can be 80–200 KB. Reading 50 of them into the parent will compress your context and hurt later turns. Saving each transcript to a file means parents pass paths, not bodies.
- **Subagents per video.** Each subagent reads one transcript, applies the single-mode extraction above, and writes one markdown file. The parent only sees a one-line confirmation per video. This is what makes 50+ videos tractable.
- **Batches of 5.** More than 5 simultaneous subagents tends to thrash rate limits on the upstream API and on the model itself; fewer leaves throughput on the table. Five is the sweet spot found in practice for this workload.

## Inputs the user might give you

The user invokes batch mode with a channel and optional params. Accept any of these forms:

- A bare handle: `@boundaryml`
- A handle without `@`: `boundaryml`
- A full URL: `https://www.youtube.com/@boundaryml/videos`
- A `/channel/UC…` URL

Optional knobs (with defaults):
- `--min-duration` minutes — default `20`
- `--max-videos` cap — default unlimited (newest-first; cap takes the N newest)
- `--output-dir` path — default `<repo-root>/<channel-slug>/wisdom/` (e.g. `boundaryml/wisdom/`)
- `--transcript-dir` path — default `/tmp/<channel-slug>/transcripts/`

Pull defaults from these unless the user is explicit. If the user is in a different repo, adapt `<repo-root>` accordingly.

## The flow

### 1. List and filter

Run the listing script and capture the result:

```bash
.claude/skills/extract-wisdom/scripts/list-channel.sh "<channel>" \
  --min-duration <N> [--max-videos <M>] \
  > /tmp/<slug>/videos.json
```

The script emits a JSON array of `{video_id, title, duration_sec, url}`, newest-first (because that's how YouTube's `/videos` page is served by yt-dlp's `--flat-playlist`).

### 2. Confirm before spending

Show the user:
- The channel resolved
- Count of videos that pass the duration filter
- A compact preview (first ~10 titles with durations like `47min`, `122min`)
- The output and transcript directories you intend to use
- A reminder that this will spawn N subagents in batches of 5

Then wait for explicit confirmation. Don't proceed on ambiguous responses ("hmm", "ok let me think") — only on a clear go.

This step is the cheapest possible insurance against running 50 extractions on the wrong channel or wrong filter. Skip it only if the user has already sanity-checked the list in this same turn.

### 3. Download transcripts to disk

Use the supadata script in parallel. Concurrency 4 is empirically the highest that doesn't trigger 502/503s on Supadata; if you go higher you will spend the whole time retrying.

```bash
mkdir -p <transcript-dir>
jq -r '.[].video_id' /tmp/<slug>/videos.json > /tmp/<slug>/ids.txt

cat /tmp/<slug>/ids.txt | xargs -P 4 -I {} bash -c '
  id="$1"
  for attempt in 1 2 3 4; do
    python3 /Users/ray/Desktop/ray-os/.claude/skills/supadata/scripts/supadata.py transcript "$id" \
      > "<transcript-dir>/$id.txt" 2> "<transcript-dir>/$id.err"
    if [ -s "<transcript-dir>/$id.txt" ]; then
      rm -f "<transcript-dir>/$id.err"
      exit 0
    fi
    sleep $((attempt * 5))
  done
' _ {}
```

After it finishes:
- Delete any zero-byte `.txt` files (failed downloads).
- Report which video IDs failed so the user can decide whether to retry or skip them.
- **Known sharp edge:** video IDs starting with `-` break `argparse` in the supadata script. Skip them and tell the user.

### 4. Fan out extract-wisdom subagents in batches of 5

Sort the surviving IDs newest-first (preserve the `videos.json` order). Take 5 at a time. For each batch, send a single message containing 5 `Agent({ subagent_type: "extract-wisdom", ... })` calls so they run in parallel. Wait for all 5 task notifications to arrive before launching the next batch.

The prompt for each subagent should be tight and copy-paste-shaped. The critical bits:

```
Read the transcript at <transcript-dir>/<video_id>.txt and apply the extract-wisdom
process to it. Write the result to <output-dir>/<video_id>.md.

Video metadata to include as YAML frontmatter at the top of the output file:
---
video_id: <id>
title: "<title>"
url: <url>
channel: <channel>
---

Write the file directly with the Write tool. Do NOT paste the wisdom content
back to me — return only one line: "wrote N bytes to <path>".
Why: parent is fanning out <total> of these and must keep its context clean.
```

The "do not paste back" instruction is load-bearing. Without it, subagents will helpfully echo the entire wisdom output and you'll lose the context savings that justify this whole architecture.

### 5. Final report

After all batches finish:
- Count succeeded vs failed (failed = no `<output-dir>/<id>.md` written)
- List the output directory and how many files it contains
- Surface any IDs that fell out at the transcript or extraction stage so the user can investigate
- Don't summarise the wisdom files themselves — that defeats the point of writing them to disk. The user will read them directly.

## Batch mode edge cases

- **Channel URL doesn't resolve / yt-dlp returns nothing.** Tell the user, ask if they meant a different handle. yt-dlp errors are usually clear about whether the channel exists.
- **All videos are too short.** Surface this with the actual longest-video duration; the user may want to lower `--min-duration`.
- **Supadata is having a bad day.** If retries are still failing after the whole pass, propose either (a) re-running the failed IDs in a few minutes or (b) falling back to `yt-dlp --write-auto-subs` for the misses.
- **User wants to resume an interrupted run.** Skip videos that already have a non-empty `<output-dir>/<id>.md`. This makes batch mode cheap to re-run.
- **User specified `--max-videos`.** That caps the newest-first window. Don't silently process more.

## What batch mode does NOT do

- It doesn't create a slash command — invoke it through Claude as a skill.
- It doesn't generate a roll-up summary across all videos. The output is one markdown file per video; cross-video synthesis is a separate task.
- It doesn't push the outputs to git. The user controls when to commit.
