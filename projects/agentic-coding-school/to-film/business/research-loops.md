---
duration: "8-12 min"
batch: 1
order: 2
batch_name: "Research & Intelligence"
class: "business"
chapter: "Research & Intelligence"
---

## Research Loops

John Kim's exact request: "a loop that researches and feeds the system with updated information so it learns as it goes."

Demo building a research loop using:
1. A skill that defines what to research and how to format findings
2. Headless mode (`claude -p`) to run the research on a schedule
3. A knowledge folder that accumulates findings over time
4. The next research run reads previous findings to avoid duplicates and build on what it knows

**Key demo:** Set up a "competitor watch" loop that:
- Searches for new content from 3 competitors weekly
- Summarizes new findings
- Appends to a running knowledge base
- Flags anything that's changed since last run

Show how this could be triggered via cron job or a simple shell script.
