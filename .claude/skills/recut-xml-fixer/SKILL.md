---
name: recut-xml-fixer
description: Reshape an FCP7 XML exported from a silence-cutting app (Recut, AutoEdit, Vika, etc.) so Adobe Premiere Pro imports it cleanly with the user's pristine external audio (e.g. Audio.wav from Audacity) linked to the video instead of the camera/screen-recording's own audio. Use this skill whenever the user points at an .xml or sequence file from Recut, AutoEdit, or any auto-cutter and wants to swap in their own audio track, drop the redundant on-camera audio, fix vertical alignment between video and audio cuts, or fix a Premiere "import failed" error on a Recut-style XML. Triggers on phrases like "fix this Recut XML", "swap the audio in this premiere XML", "align the cuts to my Audio.wav", "remove the loom audio track", "merge V1 and A1 in this XML so they're linked", or any reference to a workflow combining a silence-cutter app's XML with a separately recorded pristine audio file.
---

# recut-xml-fixer

## What this is for

Apps like **Recut**, **AutoEdit**, and **Vika** take a long screen recording or talking-head video and produce an FCP7 XML where the silence has been cut out — usually a few hundred small clips on V1 plus the on-camera audio on A1/A2.

Many creators record a separate pristine mic track (e.g. an Audacity `Audio.wav`) and want to use that instead of the noisy on-camera audio. The typical hand-edited result is an XML with three tracks:

- **V1** — silence-cut video (N clips)
- **A1 or A2** — silence-cut pristine audio (often offset by one clip because the cuts don't perfectly match)
- The other audio track — silence-cut on-camera audio (N clips, perfectly aligned with V1 because they share linkage)

That XML usually fails to import in Premiere, and even when it does the wrong audio is linked to the video. This skill fixes that.

## What "fixed" means

After running, the XML has exactly two tracks:

- **V1** — video, M clips
- **A1** — pristine audio, M clips, vertically aligned with V1

Every video clip is linked to its matching audio clip, so selecting one in Premiere selects the other. Orphan clips (positions where only one of the two tracks had a cut) are dropped on both sides so alignment is exact. The redundant on-camera audio track is removed entirely.

## How to use it

The bundled script does the whole transformation:

```bash
python /Users/ray/Desktop/ray-os/.claude/skills/recut-xml-fixer/scripts/fix_recut_xml.py "<path-to-input.xml>"
```

This writes `<input>.fixed.xml` next to the source and a `<input>.xml.backup` of the original. The user can then re-import the fixed file in Premiere (File → Import).

### Common flags

- `--in-place` — overwrite the source file. The backup is still created.
- `--output PATH` — write to a specific path.
- `--keep-audio "Audio.wav"` — explicitly say which audio track to keep, by substring of the clip filename. Use this if auto-detection picks the wrong one (rare — see below).

### Auto-detection rule

If `--keep-audio` is not given, the script picks the audio track whose first clip's filename **differs** from the video clip's filename. Reasoning: when a video is imported into Premiere, the on-camera audio shares the video's filename (e.g. both clips are named `Loom Recording.mp4`); the externally recorded pristine track has a different name (e.g. `Audio.wav`). This rule almost always picks correctly. If both audio tracks share the video's name, or if there's ambiguity, pass `--keep-audio` explicitly.

## Why each step matters

The fix is mechanically four steps. Each one addresses a specific failure mode the user has hit before; that's why they're all there:

1. **Drop the redundant audio track entirely.** The on-camera audio is what makes selecting a video clip pull along the wrong audio in Premiere.
2. **Drop orphan clips on both V1 and the kept audio.** The pristine track is usually offset by one clip, so V1's first clip has no audio counterpart and the audio's last clip has no video. Removing both keeps the timeline self-consistent and makes vertical alignment exact.
3. **Re-inject any full `<file>` definition that orphan removal stripped out.** FCP7 XML puts the full file definition (path, duration, dimensions) on the first clipitem that uses a given file; subsequent uses are short refs. A single track can reference **more than one** source file — e.g. two recording sessions concatenated, so V1 holds `Loom Recording.mp4` clips then `Loom Recording 2.mp4` clips, and the pristine track holds `Audio.wav` then `Audio 2.wav`. The full def for each file lives on the first clip that uses *that* file, not just the first clip of the track. If orphan removal deletes any of those clips, that file's def is lost and Premiere fails import with "the file could not be found" (often shown as a **blank** Error Message box) because the path URL is gone. The script stashes every full def up front and re-injects any that go missing, so multi-session timelines are handled.
4. **Rewrite every `<link>` block.** Every clipitem's links carry stale `clipindex` and `trackindex` values once anything is removed. Premiere validates these on import and rejects the XML when they don't match. The script rewrites each clip's link block from scratch — pairing the video clip at position `i` with the audio clip at position `i`.

If the user ever says "the import failed" or "Premiere won't take it" after a hand-edit, the cause is almost always either #3 (missing full file def) or #4 (stale link indices). Re-running the script from a clean source XML fixes both.

## Telling the user what you did

After running, summarize:
- The audio track that was kept (filename) and the one(s) dropped
- The number of orphan clips removed on each side
- The final clip count per track
- Where the fixed file and backup were written

Don't dump the script output verbatim — it's noisy. Pull the relevant numbers and present them as a short bulleted summary so the user can verify the choice was right before they re-import.

## When NOT to use this skill

- The XML doesn't come from a silence-cutting workflow (e.g., a hand-edited multi-track sequence). The orphan-removal logic assumes the V1 cuts and one of the audio tracks are nearly-identical sets that just need orphan trimming.
- The user wants to keep both audio tracks. This skill always reduces to one audio track. If they want a "swap A1↔A2" or "delete only specific clips" flow, do that as a one-off script rather than invoking this skill.
- The XML isn't FCP7-format. DaVinci Resolve XML, OTIO, or AAF need different handling.
