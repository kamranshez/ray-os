---
tags: [youtube, script, claude-code, memory]
status: draft
date: 2026-03-24
---

## Video Plan: "Your AI Agent Dreams While You Sleep"

| # | Title | Formula |
|---|-------|---------|
| 1 | **"Your AI Agent Dreams While You Sleep"** | Bold claim + anthropomorphism |
| 2 | **"Claude Code Has a Subconscious Now"** | Bold claim + specificity |
| 3 | **"The Feature Anthropic Doesn't Want You to Know About Yet"** | Curiosity gap + exclusivity |


So Claude Code just added a feature that most people don't know about yet. It's called Auto-dream. And essentially while you're away, it spawns a background agent that reviews your recent conversations and consolidates your memory files. And the reason they called it dreaming is because that's literally what your brain does when you sleep.

### The Problem (0:25–2:00)

Now if you've used Claude Code for any meaningful amount of time, you've probably run into this. You start a new session, and the agent just... doesn't quite remember what happened yesterday. Or worse, it remembers the wrong thing because your memory files are full of stale, contradictory notes from dozens of sessions.

And I actually talked about this a while back — auto-memory tends to write a lot of noise. Things that were true for one session but not anymore. Relative dates like "today" or "this morning" that mean nothing a week later. And this just accumulates over time.

So the question becomes — if memory is essential for your agent to work across sessions, but the memory keeps getting worse the more sessions you have... how do you fix that?

![[images/auto-dream-problem/excalidraw_2.png]]
### The Human Analogy (2:00–3:00)

And this is actually the same problem humans have. Throughout your day, your brain takes in a ton of new information. Conversations, decisions, things you read. All of it goes into short-term memory. But if it just stayed there, you'd be overwhelmed within a day.

So when you sleep — during REM sleep specifically — your brain replays the day's events and consolidates them. It strengthens what matters, prunes what doesn't, and organizes everything into long-term memory. And people who don't sleep enough literally can't form long-term memories. Their short-term buffer fills up, they start confusing things, making contradictory decisions.

That's exactly what's happening to your AI agent when it never consolidates. It's sleep-deprived.

![[images/auto-dream-human-analogy/excalidraw_2.png]]
### How Auto-Dream Works (3:00–6:30)

*Terminal on screen.*

So here's what Anthropic built. When auto-dream triggers, it spawns a background agent — a separate Claude instance — that receives this prompt:

*Show the actual prompt on screen:*

> "You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly."

And then it walks through three phases.

**Phase 1 — Orient.** First, it orients itself. It reads your memory directory, reads your MEMORY.md index, skims your existing topic files. It's basically figuring out what it already knows.

**Phase 2 — Gather Recent Signal.** Then it gathers recent signal. It checks your recent session transcripts — the JSONL files — and looks for new information, things that have drifted, memories that might be stale now.

**Phase 3 — Consolidate.** And then it consolidates. It writes or updates memory files, merges new information into existing topics, converts any relative dates to absolute ones — so "today" becomes "March 24th 2026" — and prunes contradictions.

```
# Dream: Memory Consolidation

You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly.

Memory directory: `/Users/ray/.claude/projects/-Users-ray-Desktop-livekit-setup-for-ss/memory/`
This directory already exists — write to it directly with the Write tool (do not run mkdir or check for its existence).

Session transcripts: `/Users/ray/.claude/projects/-Users-ray-Desktop-livekit-setup-for-ss` (large JSONL files — grep narrowly, don't read whole files)

---

## Phase 1 — Orient

- `ls` the memory directory to see what already exists
- Read `MEMORY.md` to understand the current index
- Skim existing topic files so you improve them rather than creating duplicates
- If `logs/` or `sessions/` subdirectories exist (assistant-mode layout), review recent entries there

## Phase 2 — Gather recent signal

Look for new information worth persisting. Sources in rough priority order:

1. **Daily logs** (`logs/YYYY/MM/YYYY-MM-DD.md`) if present — these are the append-only stream
2. **Existing memories that drifted** — facts that contradict something you see in the codebase now
3. **Transcript search** — if you need specific context (e.g., "what was the error message from yesterday's build failure?"), grep the JSONL transcripts for narrow terms:
   `grep -rn "<narrow term>" /Users/ray/.claude/projects/-Users-ray-Desktop-livekit-setup-for-ss/ --include="*.jsonl" | tail -50`

Don't exhaustively read transcripts. Look only for things you already suspect matter.

## Phase 3 — Consolidate

For each thing worth remembering, write or update a memory file at the top level of the memory directory. Use the memory file format and type conventions from your system prompt's auto-memory section — it's the source of truth for what to save, how to structure it, and what NOT to save.

Focus on:
- Merging new signal into existing topic files rather than creating near-duplicates
- Converting relative dates ("yesterday", "last week") to absolute dates so they remain interpretable after time passes
- Deleting contradicted facts — if today's investigation disproves an old memory, fix it at the source

## Phase 4 — Prune and index

Update `MEMORY.md` so it stays under 200 lines. It's an **index**, not a dump — link to memory files with one-line descriptions. Never write memory content directly into it.

- Remove pointers to memories that are now stale, wrong, or superseded
- Demote verbose entries: keep the gist in the index, move the detail into the topic file
- Add pointers to newly important memories
- Resolve contradictions — if two files disagree, fix the wrong one

---

Return a brief summary of what you consolidated, updated, or pruned. If nothing changed (memories are already tight), say so.

## Additional context

**Tool constraints for this run:** Bash is restricted to read-only commands (`ls`, `find`, `grep`, `cat`, `stat`, `wc`, `head`, `tail`, and similar). Anything that writes, redirects to a file, or modifies state will be denied. Plan your exploration with this in mind — no need to probe.

Sessions since last consolidation (9):
- 9c5556a6-28ff-4d31-9330-de34c376fa05
- d83c0536-c83c-4b6b-ba68-65bad92832e2
- c7a07014-cc21-4280-8647-032dcc0b5053
- 9233c27c-5e18-4d2a-8aeb-274a331a041e
- 70a5c439-aec4-4677-956e-40cd80aa8691
- 737babe2-2088-451a-a33c-79e7c38f3e40
- 5abbf05e-70f7-449b-bba0-206f223d13e5
- f95360ef-d11a-47bb-943c-09410aca90e2
- 813c7c05-7a39-414b-8e60-d7855658c337
```

![[images/auto-dream-three-phases/excalidraw_7.png]]

Now it doesn't run constantly. It checks two conditions. First, at least 24 hours need to have passed since the last consolidation. And second, at least 5 sessions need to have happened since then. Both conditions have to be true before it fires. So it's not dreaming every time you close your laptop — just like you don't dream every time you close your eyes. You need to have accumulated enough new experiences first.

*Show it running — the status bar screenshot:*

And when it does run, you'll see this in your status line — "Memory consolidation, running, reviewing 44 sessions." It acquires a lock file so it can't run twice at the same time. And importantly — it's read-only when it comes to your code. The dreaming agent can only touch memory files. It can't modify your project.

*Show before/after of memory files — the click-through moment:*
- Before: noisy, stale, contradictory
- After: clean, consolidated, dated properly

![[images/auto-dream-trigger-conditions/excalidraw_1.png]]
### The Broader Trend (6:30–8:30)

Now here's what's interesting. This isn't just Claude Code. The entire industry is converging on the same idea.

There's a framework called Mastra that built something called Observational Memory. And it works on the same principle but at a different level. Instead of consolidating memory files across sessions like auto-dream, it consolidates the conversation history within a single session.

They have two background agents — an Observer and a Reflector. The Observer watches the conversation, and when the message history gets too long, it compresses it into dense observations — little notes about what happened. Then when those observations get too long, the Reflector kicks in and compresses them further.

So you end up with three tiers: recent messages, observations, and reflections. Short-term, medium-term, long-term. Same architecture as human memory. And the compression is typically 5 to 40x — so conversations that would normally fill up the context window can go on indefinitely.

And here's what they say in their docs — "You don't remember every word of every conversation you've ever had. You observe what happened, then your brain reflects — reorganizing, combining, condensing into long-term memory." Same principle.

![[images/auto-dream-mastra-tiers/excalidraw_2.png]]
### What This Means for You (8:30–10:00)

So a few practical things. 

Auto-dream is in /memory settings if you want to enable it. It'll keep your memory files clean without you having to manually prune them.

This is the direction everything is heading. Having memory isn't enough. Your agent needs to consolidate that memory. It needs to dream. And the tools that figure this out first are the ones that'll actually feel like they know you over time, rather than just pretending to.

### Closer (10:00–10:30)

Now if this is the kind of thing that helps you use these tools better, I cover a lot more in my Claude Code masterclass — how to structure your memory files, manage context, all the workflows that make Claude Code actually useful long-term. Link's down below.
