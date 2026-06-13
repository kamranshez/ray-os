---
name: loom-teleprompter-notes
description: Turn a markdown script or note into Loom teleprompter-ready text chunks. Strips frontmatter, image embeds, and stage directions, keeps the spoken prose, and splits it into pieces under Loom's ~5000-character teleprompter limit, then opens them in TextEdit for reliable copy-paste. Use this whenever the user wants to record a video from a written script and needs to get it into Loom's teleprompter/script box — phrases like "paste this into Loom", "Loom speaker notes", "teleprompter", "make this a script I can read while recording", or when a long script won't paste into Loom because it's too long. Also use it for any "split this markdown into chunks under N characters" request for a teleprompter or script field.
---

# Loom teleprompter notes

Loom's teleprompter — the script that scrolls on screen while you record — caps a single script at roughly **5000 characters** and *silently* rejects a paste that's over the limit. So a full video script almost never fits in one go. This skill converts a markdown script into the spoken-word text only, split into chunks that each fit, ready to paste in order.

## What the user actually wants

They have a written script (often a markdown note with image embeds and stage directions mixed in) and they want to read it off Loom's teleprompter. They don't want to read aloud the image filenames or `[IMAGE: ...]` notes — just the words. And they hit the wall where Loom won't accept the whole thing.

## Do this

Run the bundled script on their markdown file:

```bash
python3 .claude/skills/loom-teleprompter-notes/scripts/chunk_for_loom.py "<path/to/script.md>"
```

It will:
1. strip the YAML frontmatter,
2. remove image embeds (`![[...]]`, `![](...)`) and `[IMAGE: ...]` / `[VISUAL: ...]` stage directions — things you don't say out loud,
3. keep the prose, headings, and code blocks,
4. split into chunks under the limit, cutting at `## ` section boundaries so each chunk is coherent,
5. write them to `~/Downloads/<stem>-notes-partN.txt` (or `<stem>-notes.txt` if it all fits in one), and
6. open them in TextEdit.

Then tell the user: in each TextEdit window, **Cmd+A** to select all, **Cmd+C** to copy, and paste into Loom — part 1, then part 2, and so on.

### Options

- `--limit N` — characters per chunk (default 4800, kept safely under Loom's ~5000 cap). Lower it if the user reports a paste still getting cut off.
- `--outdir DIR` — where to write the files (default `~/Downloads`, which is where it's easiest to find and where the user uploads from).
- `--no-open` — skip launching TextEdit (e.g. they only want the files).

## Why TextEdit instead of the clipboard

It's tempting to just `pbcopy` the first chunk so the user can paste immediately. Don't rely on that as the only path. The shell this runs in is frequently **sandboxed**, and there `pbcopy` writes to a session pasteboard that never reaches the GUI clipboard — the copy reports success but Cmd+V in Loom pastes nothing or stale text. Opening the chunk files in a real GUI window (TextEdit) sidesteps this entirely: the user copies from an actual app in their own session, which always works. That's why the script opens the files by default rather than copying.

If the user specifically wants the first chunk on the clipboard too, you can `pbcopy < ~/Downloads/<stem>-notes-part1.txt` as a convenience — but still open the files in TextEdit as the reliable fallback, and mention that if the paste comes up empty it's the sandbox-clipboard issue and they should copy from the TextEdit window.

## Notes

- The chunk count depends on script length: a ~10k-character script becomes 2–3 parts. Tell the user how many parts there are so they know to paste more than once.
- If a single `## ` section is itself over the limit, the script splits it further at paragraph breaks (and, as a last resort, on whitespace) so no chunk ever exceeds the cap.
- This is macOS-oriented (`open -a TextEdit`). On another platform, open the resulting `.txt` files in any editor and copy from there.
