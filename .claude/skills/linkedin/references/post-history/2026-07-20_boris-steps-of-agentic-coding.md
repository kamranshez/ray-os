---
date: 2026-07-20
hook: "Boris Cherny, the creator of Claude Code, just mapped the steps of agentic coding. Every step up is a system you built around the model. You go from pair programmer to VP."
media: video
status: posted
engagement:
  reactions: 10
  comments: 0
  reposts: 0
  impressions: 533
  last_checked: 2026-07-22
url: https://www.linkedin.com/feed/update/urn:li:activity:7484064162667577344/
notes: Text post built from the Boris "Steps of AI Adoption" framework video. Spine = 4-step ladder (Assisted/Parallel/Supervised autonomy/AI-native), roles pair programmer -> VP. Ray's systems reframe woven through each step ("Claude checks its own work because you set the systems up"). Proof anchor = Percy coordinating 10 bots on Sentry issues (step 4). YouTube link goes as first comment.
---

Boris Cherny, the creator of Claude Code, just mapped the steps of agentic coding.

Every step up is a system you built around the model. You go from pair programmer to VP.

𝗦𝘁𝗲𝗽 𝟭: Assisted → you + 1 agent

One engineer, one agent, mostly supervised. A fast pair programmer.

You run one session at a time and review almost every change before it merges.

The work is synchronous: you watch it work instead of moving to the next thing.

You never look away, because you haven't given it a way to check itself yet. So instead of looking away, you split the terminal and babysit 4 sessions at once. Still step 1.

𝗦𝘁𝗲𝗽 𝟮: Parallel → orchestrator of ~10 agents

You run 5 to 10 agents at once. But that isn't enough for step 2.

Claude checks its own work before you see it: it runs the tests, the build, the linter, and drives a real browser (or computer) through the change. But it only does that because you set the systems up (e.g., you gave it the right API keys, a test account, browser-use agents, etc.).

None of it happens by default. You need to set this up for Claude.

𝗦𝘁𝗲𝗽 𝟯: Supervised autonomy → manager of managers, ~100 agents

Claude writes nearly all the code, and the work starts finding you instead of you finding it.

The move that unlocks it: every time you catch yourself doing something by hand, you turn it into a loop.

A weekly job that reads your slowest queries and opens optimization PRs. A morning one that pulls your session recordings and redesigns the dead ends.

You also give Claude its own context: connect its Notion, its dashboards, its Slack.
"Did you read the code?" becomes "what context was the model missing, and how do I give it that next time?"

The trap is scaling agent count before the loop has earned your trust.

𝗦𝘁𝗲𝗽 𝟰: AI-native → VP steering by intent, 1,000+ agents

The loop is closed and Claude kicks off Claude.

You point one agent at a whole domain and it fans the work out itself.

Yesterday I sent one message: load every Sentry issue hitting 10+ users, spin up a bot per issue, verify the bug, fix it, open a PR, loop every 10 minutes until they're all open.

Ten bots ran in parallel. I never touched the keyboard. You stop assigning tasks and start steering by intent, monitoring by exception.

I talk more in this video. Full video linked in the comments 👇
