---
name: sync-and-cut
description: >-
  Sync separately-recorded audio to screen recordings and export one Adobe
  Premiere Pro XML. Takes a folder (or explicit pairs) of screen/talking-head
  recordings (Loom, OBS, QuickTime, ScreenFlow) plus their separately-recorded
  clean audio (Audacity WAV, external mic, lav), measures the time offset by
  waveform peak correlation, muxes each video with its synced audio into one
  file, removes silence with the recut CLI, and writes a single
  Premiere-importable XML. Use this skill whenever the user recorded their voice
  on a separate track from the screen/camera and needs them lined up — phrases
  like "sync my Loom recording with my Audacity audio", "line up the audio with
  the video", "the audio was recorded separately", "combine these recordings",
  "my mic audio is its own file", "silence-cut these and give me a Premiere
  XML", or when the user points at a folder of recording + audio pairs. Also
  use it for sync-only with no silence removal (pass --sync-only). Do NOT use it
  to repair an already-exported recut XML — that is the recut-xml-fixer skill.
---

# sync-and-cut

## What this is for

A common recording setup: capture the screen or camera with one tool (Loom,
OBS, QuickTime) and record the voice separately on a clean mic (Audacity). You
end up with two files per take that **start at different moments** — whoever
hit record first has extra lead-in. Before editing you need them lined up, the
noisy on-camera scratch audio dropped, and ideally the dead air removed.

This skill does that whole pipeline and hands back one XML to import into
Premiere.

## The core idea: combine first, then cut

The naive approach — run recut on the video and the audio as two separate
tracks — fails, because recut detects silence per file and the two tracks drift
apart (different clip counts, broken sync).

Instead: **mux each video with its synced audio into a single file first.** Now
recut sees one file per recording and cuts video and audio as one locked unit.
Sync is guaranteed; there is nothing to reconcile afterwards. This is also why
the `recut-xml-fixer` skill is not needed here — there is no multi-track mess to
repair.

## How to run it

One command does everything — point it at the folder:

```bash
python3 <skill_dir>/scripts/sync_and_cut.py "/path/to/folder"
```

The script discovers video + audio pairs, finds each offset, writes a combined
`<video name> (synced).mov` per recording, silence-cuts with recut, and writes
`sync-and-cut.xml` in the folder. Import that XML into Premiere
(**File → Import**). The `(synced).mov` files must stay where they are — the XML
points at them.

It pairs files by trailing number when the names carry one (`Loom Recording 1`
↔ `Audio 1`), otherwise by sorted order. Audacity `.aup3` project files are
ignored — the user must export a `.wav` first.

### Flags

- `--sync-only` — stop after combining; skip silence removal. The `(synced).mov`
  files are themselves importable straight into Premiere.
- `--min-silence N` — shortest pause recut will cut, in seconds (default `0.6`).
  This is the main quality knob — see the table below.
- `--padding N` — breathing room kept around each kept segment (default `0.15`).
- `--pair VIDEO AUDIO` — give an explicit pair instead of folder discovery;
  repeatable for multiple pairs. Use when filenames don't pair cleanly.
- `-o PATH` — output XML path. `-n NAME` — Premiere sequence name.
- `--work-dir DIR` — write the combined `.mov` files and XML somewhere other
  than the source folder.
- `--audio-codec` — combined-file audio codec (default `pcm_s24le`, lossless-grade).

## Choosing --min-silence

recut's auto threshold shreds clean studio audio — it treats the micro-pauses
between words as silence and produces hundreds of choppy 0.1s fragments. The fix
is `--min-silence`: only cut pauses longer than this, so real pauses and
dead-air go but inter-word gaps stay. Measured on a real talking-head recording:

| --min-silence | result |
|---|---|
| auto (default recut) | 43–63% of clips under 0.25s — choppy, unusable |
| 0.4 | ~11% tiny clips — still slightly choppy |
| **0.6 (this skill's default)** | **0% tiny clips, natural phrase-length clips** |
| 0.8+ | very gentle — only long dead-air removed |

`0.6` is the default because it removes genuine pauses and long dead-air while
never fragmenting speech. Go higher (`0.8`–`1.0`) for a gentler cut that only
trims long dead-air; lower (`0.4`) for a tighter cut at the risk of slight
choppiness. The script's verification step reports the choppy-clip percentage
and warns if it climbs over 10%.

## What the script reports

For each pair it prints the measured offset and a confidence figure:

- **`r`** — correlation of the two audio envelopes once aligned. Above ~0.9 is a
  rock-solid sync; below 0.5 is flagged `LOW CONFIDENCE` and should be checked
  (usually means the two files aren't actually the same take).
- **`clarity`** — how far the winning alignment beats the next-best one.

After recut it prints clip counts, the video/audio mismatch count (should be
`0`), median clip length, choppy-clip percentage, total timeline length, and the
boundary between recordings. Relay these to the user as a short summary — they
confirm the cut is sane without opening Premiere.

## Requirements

`ffmpeg`, `ffprobe`, `recut`, and `python3` with `numpy`. The script checks for
the tools and exits with a clear message if any are missing.

## When NOT to use this skill

- Repairing an already-exported recut/AutoEdit XML, or swapping audio inside an
  existing XML — that's `recut-xml-fixer`.
- Removing bad takes, false starts, or repeated lines from a single recording —
  that's content editing, not silence/sync; use `video-editor`.
- The audio and video are the same take already in sync (no separate
  recording) — just run recut directly.
