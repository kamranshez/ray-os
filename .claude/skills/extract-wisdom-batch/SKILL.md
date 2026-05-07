---
name: extract-wisdom-batch
description: >
  Bulk "extract wisdom" pipeline for a YouTube channel. Lists videos with yt-dlp, filters by duration, downloads transcripts via the supadata script, then fans out one extract-wisdom subagent per video in batches of 5 — writing structured wisdom files to disk without bloating parent context. Use this skill whenever the user wants wisdom/insights/takeaways extracted from a YouTube channel in bulk: "extract wisdom from this channel", "go through @<handle>'s long videos", "summarise everything on <channel>", "give me the best ideas from <creator>'s podcast", "/extract-wisdom-batch", or any variant of "process a whole channel into wisdom notes". Trigger this even if the user only describes the goal (e.g. "I want to read the highlights from every video on @boundaryml longer than 20 minutes") — the orchestration of channel listing + transcript fetch + parallel extraction is the value.
---

# Extract Wisdom Batch

Pipeline for turning every long video on a YouTube channel into a structured wisdom note. The parent (you) orchestrates; the heavy reading happens inside `extract-wisdom` subagents whose output goes straight to disk so it never lands in your context.

## Why each step exists

- **List + filter first.** Channels often mix shorts, livestreams, and long-form. Filtering by duration catches the substance and skips noise. Confirming the filtered list before spending tokens lets the user catch wrong-channel / wrong-filter mistakes early.
- **Disk-resident transcripts.** A single 60-minute transcript can be 80–200 KB. Reading 50 of them into the parent will compress your context and hurt later turns. Saving each transcript to a file means parents pass paths, not bodies.
- **Subagents per video.** Each subagent reads one transcript, applies the `extract-wisdom` skill, and writes one markdown file. The parent only sees a one-line confirmation per video. This is what makes 50+ videos tractable.
- **Batches of 5.** More than 5 simultaneous subagents tends to thrash rate limits on the upstream API and on the model itself; fewer leaves throughput on the table. Five is the sweet spot found in practice for this workload.

## Inputs the user might give you

The user invokes this with a channel and optional params. Accept any of these forms:

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
.claude/skills/extract-wisdom-batch/scripts/list-channel.sh "<channel>" \
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

## Edge cases

- **Channel URL doesn't resolve / yt-dlp returns nothing.** Tell the user, ask if they meant a different handle. yt-dlp errors are usually clear about whether the channel exists.
- **All videos are too short.** Surface this with the actual longest-video duration; the user may want to lower `--min-duration`.
- **Supadata is having a bad day.** If retries are still failing after the whole pass, propose either (a) re-running the failed IDs in a few minutes or (b) falling back to `yt-dlp --write-auto-subs` for the misses.
- **User wants to resume an interrupted run.** Skip videos that already have a non-empty `<output-dir>/<id>.md`. This makes the skill cheap to re-run.
- **User specified `--max-videos`.** That caps the newest-first window. Don't silently process more.

## What this skill does NOT do

- It doesn't create a slash command — invoke it through Claude as a skill.
- It doesn't generate a roll-up summary across all videos. The output is one markdown file per video; cross-video synthesis is a separate task.
- It doesn't push the outputs to git. The user controls when to commit.
