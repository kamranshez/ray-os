---
source: "How to Automate Your Work with Claude Code (Beginner Breakdown)"
channel: Liam Ottley + Peter Yang (PDang)
video_id: oC0mPBSmzfQ
date: 2026-01-14
---

## Gaps Not Covered in Master Claude Code

- **[MEDIUM] Using YouTube-DLP as a free data source inside Claude Code** — They build a slash command that uses youtube-dlp to scrape channel data (titles, views, durations) without needing API keys or billing. Peter says: "there's this thing called YouTube DLP which is like this free thing that you can use to get the latest data for a channel." Ray covers MCP and web search but not this specific free-tool-integration pattern for scraping structured data from platforms.

- **[MEDIUM] Building a YouTube channel competitive researcher as a real-world automation** — The entire video walks through building a `/youtube` command that fetches 20 recent videos from a channel, ranks top 10 by views, and generates key insights about content strategy. This is a concrete non-coding automation use case that goes beyond Ray's existing examples.

- **[LOW] Using WhisperFlow / voice dictation as a productivity multiplier alongside Claude Code** — Liam specifically recommends combining voice-to-text transcription tools (WhisperFlow) with Claude Code for faster input. He says: "it must save me like tens of hours each week of typing manually." Ray's course doesn't cover voice input workflows.

- **[LOW] Layering slash commands on top of each other (composing automations)** — They demonstrate iterating the `/youtube` command to batch-process multiple channels from a `channels.md` file, showing how to layer automation capabilities progressively. While Ray covers slash commands and skills, the explicit "layering" / composability framing isn't covered.

- **[LOW] "Make an inventory of your week" framework for identifying what to automate** — Peter's approach: "make an inventory of like your week and what takes up the most time" as the first step before building anything. This is a non-technical mindset tip that Ray's course doesn't explicitly frame.

- **[LOW] Asking Claude "what are three different ways to do X, pros and cons" as an exploration technique** — Before building, Peter asks Claude to propose multiple solution approaches with tradeoffs. While Ray covers planning, this specific "explore the solution space first" pattern isn't a dedicated topic.
