---
captured: 2026-06-09
search_query: "Claude Code" (LinkedIn, Top Match)
author: Jahanzaib Ahmed
author_headline: "I build AI agents for production | Founder @ AgenticMode AI | Voice Agents, RAG, Automations, AWS, Claude Code, OpenClaw, Pydantic AI | 118 systems shipped"
author_note: degree: 1st
posted_relative_at_capture: 1d ago (edited)
hook: "Most people treat Claude like a smart intern you brief manually. Anthropic's engineers treat it like a system you configure once, then get out of the way."
format: contrast hook + quoted Anthropic engineer + 4-bullet recipe + closing reframe
media: text only
engagement:
  reactions: 6
  comments: 2
  reposts: 0
  impressions: unknown_public
ranking_in_sweep: low_engagement_high_content_value
why_to_save_despite_low_engagement:
  - Contains a direct quote from Anthropic MTS Daisy Hollman from Code with Claude 2026 saying
    EXACTLY Ray's "design loops, don't prompt" angle from a credible internal source
  - Frames the lineage as "engineers who move fastest are not the best prompters; they are the best system designers"
  - Specific Anthropic-internal practices listed (Routines, /goal pipelines, Git worktrees, Hooks)
why_it_underperformed:
  - 6 reactions is well below the post's content quality — likely a distribution / posting-time issue
  - Author has 1st-degree network so should have surfaced higher
  - No hook image, no carousel, no CTA — relies entirely on text
what_to_steal_for_ray:
  - "Most people treat X like Y. [Authority figure] treats X like Z." contrast hook formula
  - Use this exact Daisy Hollman quote: "You're not supposed to prompt Claude. You're supposed to build a system that prompts itself." — it's perfect for Ray's loops angle
  - Closing reframe: "The engineers who move fastest are not the best prompters. They are the best system designers."
  - Specific list of Anthropic-internal tactics (Routines, /goal pipelines, Git worktrees, Hooks)
critical_for_rays_content: |
  This post is the highest-value reference in the entire sweep for Ray's loops angle.
  It contains a sourced quote from an Anthropic MTS at Code with Claude 2026 that says
  literally what Ray wants to say. Pair this with the Boris Cherny quote ("My job is to
  write loops") and Ray now has two sourced Anthropic-internal statements supporting the
  same paradigm shift. That's strong external authority for his take.
---

Most people treat Claude like a smart intern you brief manually.

Anthropic's engineers treat it like a system you configure once, then get out of the way.

Daisy Hollman, Anthropic MTS, said it plainly at Code with Claude 2026:

"You're not supposed to prompt Claude. You're supposed to build a system that prompts itself."

At Anthropic, that looks like this:

→ Routines that run on a schedule and wake up to finished work
→ /goal pipelines that track state across sessions without reopening a chat
→ Git worktrees so parallel Claude agents run on isolated branches with zero collision
→ Hooks that extend Claude deterministically without touching the context window

The engineers who move fastest are not the best prompters.

They are the best system designers.
