# Routine-mode output contract (skill reports, routine posts)

When invoked with `output_dir=<path>`, the skill writes plain files into that directory and
does NOT touch Slack. The acs/gap-scout routine reads these files and posts the thread,
keeping ALL curl / token / safe-encoding logic on the routine side and ALL wording on the
skill side. The routine posts each text block with `jq --rawfile`, so every file you write
is treated as a pure data string — a transcript full of `"`, backticks, `$(...)`, or newlines
can never break out. Your only job is to produce correct, cap-respecting content.

## Files to write

- **`decision.json`** — the gate result the routine reads first:
  ```json
  {
    "post": true,
    "reason": "1 net-new, 1 complement",
    "status": "posted",          // posted | covered | no-spine | out-of-scope | skipped
    "videoId": "5FKBkUCaLa8",    // validated 11-char id, for the thumbnail URL
    "spines": ["short spine label", "..."],
    "counts": { "net_new": 1, "complement": 1, "partial": 0, "covered": 0 }
  }
  ```
  If `post` is false, write only `decision.json` (no main/reply files). The routine posts
  nothing and logs the status.

- **`main.txt`** — the main-message body as Slack mrkdwn, **under 3000 chars**. Contents, in
  order: the *🔍 The one idea worth a video* section (each spine bold + one-sentence why),
  then a one-line *VERDICT*, then the 25-word SUMMARY, then the counts line
  (`🔴 … net-new · 🔗 … complement · 🟡 … partial · ✅ … covered`). Do NOT include the title /
  channel / Watch link or the thumbnail — the routine adds those (it owns the videoId,
  title, channel, publishedAt and builds the image block + thumbnail check itself).

- **`reply-NN-<label>.txt`** — ordered thread replies, each **under 3500 chars**, posted in
  filename order. **Numbering convention (mandatory so lexical sort = post order):** reserve
  bands — `01-09` = deep dive (one file per spine), `10-19` = pitches, `20-29` = wisdom. Stay
  inside your band: never number a wisdom file `04` or a deep-dive file `11`, or the thread
  posts out of order. Zero-pad every index.
  - `reply-01-deepdive.txt` (and `reply-02-deepdive.txt`, … one per spine) — the Stage 2a
    prose, led by `*🔬 Deep dive*`. A ✅-covered spine still gets its deep-dive file here.
  - `reply-10-pitches.txt` (`reply-11-pitches.txt` if it overflows 3500 — split between two
    whole pitches, never mid-pitch) — `*🎬 Proposed ACS videos*`, the ranked film-able briefs.
  - `reply-20-wisdom-<section>.txt`, `reply-21-…`, … — `*📚 Full wisdom (reference)*`, the
    Stage 1c extraction split across as many files as needed, each led by a bold header
    (`*🧠 Ideas*`, `*💡 Insights*`, `*🗣️ Quotes*`, `*🔁 Habits*`, `*📊 Facts*`,
    `*📚 References*`, `*🎯 One-sentence takeaway*`, `*✅ Recommendations*`). Skip a section
    only if the video genuinely had no items for it.

**Write every file with Bash (`printf`/heredoc), not the Write tool** — routine mode runs
inside a subagent, and many harnesses block the Write tool on report-like files; a
single-quoted heredoc (`cat > "$output_dir/reply-01-deepdive.txt" <<'EOF'`) is byte-exact and
sidesteps the guard.

## Formatting rules

- Slack mrkdwn: **bold is single asterisks** `*like this*`, never `**double**`.
- Never use em or en dashes in any pitch TITLE (Ray's house rule); fine elsewhere in prose.
- Enforce the caps programmatically: if a block would exceed its cap, split it across more
  files (or truncate with an explicit `…` for a single oversized untrusted bullet) rather
  than emitting an over-length file the routine will have to reject.
- Never cut a bullet or paragraph in half across files.

## What the routine does with these (for reference)

1. Reads `decision.json`; if `post:false`, logs the status and moves on.
2. Builds the main message `blocks`: an image block (thumbnail from `videoId`, with the
   maxres→hq client-side check), a title/channel/Watch-link section, then `main.txt` as a
   section block. Posts via `chat.postMessage`, captures `.ts`.
3. Posts each `reply-NN-*.txt` in order with `thread_ts` = that ts, strictly sequentially,
   each via `--rawfile`, confirming `ok:true` before the next.
