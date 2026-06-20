---
name: prproj-timestamps
description: Extract timeline markers from an Adobe Premiere Pro project file (.prproj) and turn them into YouTube chapter timestamps. Use whenever the user points at a .prproj file and asks for "timestamps", "chapters", "YouTube chapters", "markers as timestamps", "extract the markers", or wants a chapter list for a video description. Also trigger when the user shares a Premiere project and mentions YouTube description, chapters, or markers — even if they don't name the file extension. Do NOT use for .xml/FCP7 sequence exports (that's the recut-xml-fixer skill) or for reading transcripts.
---

# prproj Timestamps

Turn the markers Ray drops on a Premiere Pro timeline into a ready-to-paste YouTube chapter list, formatted exactly the way he likes:

```
00:00 - Intro
00:53 - Creating the Cards
03:21 - Checking the Cards
05:17 - Why This Is Powerful
06:14 - Newsletter
06:36 - Closing the Loop
12:56 - Conclusion
```

## How it works

A `.prproj` is gzip-compressed XML. Each timeline marker is a `<DVAMarker>` element holding a tiny JSON blob with the marker's name (`mName`) and start time in `ticks`. Premiere uses a fixed **254016000000 ticks per second**. The bundled script handles decompression, parsing, tick→time conversion, sorting, and formatting — so you don't have to reverse-engineer the file by hand each time.

## Steps

1. Run the script on the project file:

   ```bash
   python3 .claude/skills/prproj-timestamps/scripts/extract_timestamps.py "<path-to.prproj>"
   ```

   It prints chapters one per line, already sorted chronologically, in `MM:SS - Name` format (`H:MM:SS` once a marker crosses the one-hour mark). It seeds a `00:00 - Intro` line automatically unless a marker already sits at the very start — YouTube only activates chapters when the first one is at 0:00.

2. Clean up the labels before presenting. The script outputs marker names verbatim, and timeline markers are often typed quickly:
   - Fix obvious typos and casing (e.g. `Creatiing the Cards` → `Creating the Cards`).
   - Keep Ray's wording and intent — don't rewrite a clear label into something fancier. If a label is genuinely weak or cryptic, you can suggest a punchier alternative, but show it as a suggestion rather than silently replacing it.
   - Per Ray's house style, never introduce em or en dashes; the separator stays a plain hyphen with spaces (` - `).

3. Present the final block in a code fence so it's easy to copy straight into a YouTube description. If you changed any labels, mention what you changed in a short note underneath.

## Notes

- The script reads all `<DVAMarker>` entries in the project. In practice these are the timeline/comment markers used for chapters. If a project somehow mixes in clip-level markers with offset times and the output looks wrong, say so rather than presenting suspicious timestamps.
- Handles both compressed and uncompressed `.prproj` files (it sniffs the gzip magic bytes).
- If the user wants the result saved to a file instead of pasted inline, write it next to the project or wherever they ask.
