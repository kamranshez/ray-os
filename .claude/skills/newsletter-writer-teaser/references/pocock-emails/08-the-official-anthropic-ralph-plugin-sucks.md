---
from: "Matt Pocock (AI Hero)" <matt@aihero.dev>
subject: The Official Anthropic Ralph Plugin Sucks
date: Thu, 07 May 2026 18:24:31 +0000
---

Hey [name],
The Anthropic Ralph plugin sucks.

It's an official tool that's fundamentally broken in how it
implements the Ralph methodology. The problem isn't hard to
understand once you know how LLMs actually work under load.

Ralph works because each iteration runs in a fresh context
window. The AI stays sharp. But the Anthropic plugin keeps
everything in a single session, feeding the prompt back in
repeatedly. This means the context fills up with each iteration,
and the model degrades predictably.

By iteration 3 or 4, you're operating entirely in the "dumb zone"
where LLMs make mistakes and lose coherence.

The fix is simple: use a bash loop instead.

In the full article, I explain exactly why this happens, show you
the context window decay, and cover how to implement Ralph
properly.

​Read the full article → (
[REDACTED-TRACKING-URL]
)​

Matt

Unsubscribe from AI Hero Emails (
[REDACTED-TRACKING-URL]
). You can also unsubscribe (
[REDACTED-TRACKING-URL]
) from all emails at any time.

12333 Sowden Rd, Ste. B, PMB #97429, Houston, TX 77080

​
