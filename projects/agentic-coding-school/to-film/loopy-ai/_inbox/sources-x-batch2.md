---
tags: [loopy-ai, inbox, sources, twitter]
date: 2026-05-28
status: inbox
---

Second batch of X/Twitter (and one YouTube) sources, surfaced on the **body-level** Apple Notes pass that the first title-only pass missed. The standout (Aakash Gupta's 6-levels ladder) lives in its own file: [[autonomy-ladder]]. First batch is in [[sources-x]].

## Tier 1 — core loop material

### Daniel San — the loop-control taxonomy
https://x.com/dani_avila7/status/2053945246619251183 (15K views, May 11) — image post

The cleanest framing device for the class intro. "Four ways Claude Code decides when to keep going and when to stop":
- **/goal** waits for an outcome
- **/loop** waits for the clock
- **Stop hooks** wait for your script
- **Normal chat** waits for you

Use this as the opening slide: every loop is just a different answer to "what makes the agent take another turn?" (Note: confirms a `/loop` time-based command exists alongside `/goal`.)

### Max Weinbach — /goal real win + a goal-writing tip
https://x.com/mweinbach/status/2054216215007010827 (16K views, May 12)

"Goal mode in Codex is sorta wild. I had it optimize Parakeet for Snapdragon X2 Elite and it ~3x'd performance of the model on the NPU." The reusable tip: "A good way to start it out is having it calculate the theoretical maximum performance and work towards the goal." A concrete, non-web-dev `/goal` example plus a goal-prompt pattern (anchor on a theoretical ceiling).

### Brian Scanlan / Intercom — "give agents problems, not tasks" (YouTube talk)
https://youtu.be/4_VQBbs2iQA (AI Engineer channel, 22 min, May 15)

Intercom hit 2x engineering throughput in under a year by treating Claude Code like a new hire: onboarding it to a 15-year Rails monolith, writing a skill for every recurring task, connecting it to prod + internal tooling. Data points: PR throughput doubled, 17.6% of PRs auto-approved with SOC 2 sign-off, CI collapsed under the volume. Core principle for the class framing: **give agents problems, not tasks.** (Matches Ray's separate "Give agents problems not tasks" note.) Good authority/proof segment for why long-running autonomous loops pay off.

## Tier 2 — supporting

### Daniel San — Slack as an agent transport layer
https://x.com/dani_avila7/status/2054729819573654015 (3K views, May 14)

"Claude writing into Slack to call another Claude instance for overnight incidents. Slack as a transport layer between agents, not just a human UI." Overnight + agent-to-agent angle; pairs with the overnight-run material (Bootoshi).

### Chris Hayduk — effective goals (image)
https://x.com/chrishayduk/status/2053807198870880743 (220K views, May 11) — text is a t.co link, substance in the attached image (not captured). Saved under "Effective goals". Re-open in browser when scripting the goal-writing segment.

## Tier 3 — adjacent (probably other classes, noted for completeness)

These came up in the sweep but lean toward review/subagent/prompting classes rather than the loop core:

- **Adversarial Agents** — https://x.com/systematicls/status/2028814227004395561 — "they're eager to please you; you may also want it to disprove things." Verification/adversarial-reviewer angle.
- **Subagents as pipeline separation** — https://x.com/shannholmberg/status/2032892199751528486 — orchestration; caveat that some tools (AskUserQuestionTool) aren't available in subagents.
- **Autonomous discovery on autopilot** — https://www.linkedin.com/posts/stasbel_someone-connected-claude-opus-47-to-a-professional-ugcPost-7450863423002808320 — "someone connected Claude Opus 4.7 to a professional [tool]" to find posts around the clock. A background-loop use case.
- **Prompting Opus 4.7** — https://simonwillison.net/2026/Apr/18/opus-system-prompt/ + https://www.youtube.com/watch?v=8YhYtIF9PYI — prompt-engineering reference.

## Non-X links from note 1 ("To Do for Class")

- "Goal In, Strategy Out" follow-up: https://youtu.be/4_VQBbs2iQA?t=844 (same Intercom talk, timestamped)
- Code review with debates: https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/ and https://milvus.io/blog/ai-code-review-gets-better-when-models-debate-claude-vs-gemini-vs-codex-vs-qwen-vs-minimax.md
- Ideas jotted in the same note worth a segment each: "workflows that reset the context window for the next part", "Verification Loop", "Scratchpadding as a way to survive context resets".
