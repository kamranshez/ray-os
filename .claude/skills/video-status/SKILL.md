---
description: Cross-reference Google Drive video folders with the Agentic Coding School website. Shows pipeline status (To Film / To Edit / Uploaded), missing videos, orphaned folders, and mismatches. Triggers on "video status", "check video pipeline", "what videos need editing", "what's uploaded", "video report", "pipeline status", or /video-status.
---

# Video Status

Cross-references Google Drive video production folders with the website to show a pipeline status report.

## How It Works

1. Read manifest files from Google Drive
2. Query the MCP server for current website video lists
3. Scan the three pipeline folders to verify actual state
4. Output a status report

## Paths

- **Drive root:** `/Users/ray/Library/CloudStorage/GoogleDrive-the.rehman.amjad@gmail.com/My Drive/Projects/Agentic Coding School`
- **Manifests:** `{drive_root}/manifests/{class-slug}.json`
- **Pipeline folders:** `{drive_root}/To Film/`, `{drive_root}/To Edit/`, `{drive_root}/Uploaded/`
- **Notes file:** `{drive_root}/REORGANIZATION_NOTES.txt`

## Instructions

1. Use `Bash` to read the manifest JSON files from `{drive_root}/manifests/`. Each manifest has:
   - `classSlug`, `totalFolders`, `uploaded`, `toEdit`, `toFilm`, `orphaned`
   - `videos[]` with `driveFolder`, `websiteTitle`, `status`, and optional `note`

2. Use the `mcp__agentic-coding-school__list_classes` tool to get current class data from the website.

3. Use the `mcp__agentic-coding-school__list_videos` tool for each class to get current website video titles.

4. Use `Bash` with `ls` to count actual folders in each pipeline stage to verify manifest accuracy.

5. Cross-reference and output a report in this format:

```
═══ VIDEO PIPELINE STATUS ═══

Master Claude Code (claude-code)
  Website: 102 videos
  Uploaded: 57    To Edit: 49    To Film: 2    Orphaned: 6
  ⚠ 2 website videos missing from Drive

Bonus Techniques (techniques)
  Website: 36 videos
  Uploaded: 10    To Edit: 30    To Film: 1    Orphaned: 5
  ...

═══ ISSUES ═══
  [claude-code] Website "Introduction" — no Drive folder (To Film placeholder exists)
  [techniques] "Subagent Paradigms" — orphaned, no website match
  ...
```

6. If the user asks about a specific class, show per-video detail including the Drive folder name and its mapped website title.

7. If the user asks to regenerate manifests, run `python3 {drive_root}/generate_manifests.py`.

## Key Mappings to Remember

Some Drive folder names differ from website titles. The manifest's `websiteTitle` field has the correct website title. When `driveFolderDiffersFromTitle` is true, both names are shown in the report.
