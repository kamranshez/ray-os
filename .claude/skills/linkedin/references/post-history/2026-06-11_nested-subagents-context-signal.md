---
date: 2026-06-11
hook: "Most people use subagents to protect their main context."
secondary_hook: "The leverage is letting subagents protect their own."
triggers:
  primary: status signaling
  secondary: aspiration
pattern: contrast hook
media: text only
status: posted
engagement:
  reactions: 8
  comments: 1
  reposts: 0
  impressions: 543
  last_checked: 2026-07-15
url: https://www.linkedin.com/feed/update/urn:li:activity:7470491246776610817/
notes: >
  Post 1 from the nested-subagents batch (10 variations from transcript.txt,
  Claude Code nested subagents feature). Contrast hook pattern. Ray added
  "I talk more about this in the video below 👇" before posting and dropped
  the closing aphorism line ("Context isn't a budget you spend. It's a signal
  you protect."). Added a YouTube comment linking to the video
  https://www.youtube.com/watch?v=i4fMF1pug3w. Checked 10 min after posting.
  2026-06-20: final check at ~9 days — 6 reactions, 1 comment (Ray's own
  author comment with the YouTube link), 0 reposts, 363 impressions.
---

Most people use subagents to protect their main context.

The leverage is letting subagents protect their own.

Claude Code shipped nested subagents yesterday. An agent can now spawn its own agents, up to 5 layers deep.

Here's why that matters.

Agents make their best decisions early, while their context is lean. Every noisy tool call after that, codebase exploration, web searches, log dumps, degrades the next decision.

One layer of subagents kept your main session clean. But the subagent itself was unprotected. The moment it had to verify a claim or grep through 400 files, it got as noisy as the session it was built to protect.

Now it delegates too.
→ Layer 1 extracts the claims from an article
→ Layer 2 verifies each claim with all the noisy searching
→ Layer 3 cross-checks the ones that smell wrong

What flows back up is clean at every level.

I talk more about this in the video below 👇
