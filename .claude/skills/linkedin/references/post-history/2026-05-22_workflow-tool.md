---
date: 2026-05-22
hook: "Anthropic shipped a feature this week that lets you run 100 subagents in a single Claude Code session without the main context ever filling up."
triggers:
  primary: curiosity gap
  secondary: aspiration
media: text only
status: posted
engagement:
  reactions: 16
  comments: 3
  reposts: 0
  impressions: 1013
  last_checked: 2026-07-21
url: https://www.linkedin.com/feed/update/urn:li:activity:7463588686622998528/
notes: Post 5 chosen from workflow-tool batch. Source = /Users/ray/Downloads/transcript.srt (Claude Code workflow tool, deterministic multi-agent orchestration). Ray edited "off by default behind an env var" to "off by default right now."
---

Anthropic shipped a feature this week that lets you run 100 subagents in a single Claude Code session without the main context ever filling up.

They haven't announced it. It's off by default right now.

Here's the idea.

Until now, a multi-agent workflow meant your main session acted as the orchestrator. Every subagent result passed through it. That capped how many agents you could realistically chain before the context window choked.

The new workflow tool removes the model from orchestration. You define the flow in a JavaScript file. Phases, loops, conditionals, schemas. Results stream directly between subagents and never enter your main context.

So the count stops mattering. 10 agents or 100, the orchestrator stays clean.
Triage every Sentry issue overnight. Sweep dead code round after round. Research a list of leads in parallel, then write each message.

The kind of automation that used to fall apart halfway just got a real foundation.
