# Reference Script: "/btw and --fork-session"

**YouTube ID:** DqjBbAr3oTo
**Published:** 2026-03-11
**Title:** "Anthropic Just Dropped the Feature Nobody Knew They Needed"
**Length:** ~8 minutes

### Actual Performance Data

| Metric | Value |
|--------|-------|
| Day 1 views | 26,444 |
| Day 2 views | 8,051 |
| 48hr total | 34,495 |
| Total (20 days) | 38,984 |
| Day 1 avg watch duration | 170s (2:50) |
| Day 1 likes | 759 (2.87% like:view) |
| Day 1 subs gained | 383 (1.45% sub:view) |

### Retention Curve (key checkpoints)

| Position | Retention | Notes |
|----------|-----------|-------|
| 10% | 63% | |
| 20-27% | 50% -> 52.5% | **BIGGEST BUMP (+2.5pp)** — "context pollution" named, LLM-as-human analogy |
| 33% | 48% | Still strong — old workaround before /btw |
| 50% | 33% | |
| 54% | 33% -> 34.2% | **Small bump** — /btw vs fork comparison section |
| 75% | 22% | |
| 100% | 11% | |

---

## Why This Script Worked

1. **Universal pain point hook** — Opens with a problem every Claude Code user has experienced: wanting to ask a question mid-task and interrupting the agent. No jargon needed, instant recognition.
2. **"Context pollution" as a named concept** — Takes an abstract technical problem and gives it a memorable name. Viewers now have vocabulary for something they felt but couldn't articulate.
3. **LLM-as-human analogy** — "When a person is deep in a task and you tap them on the shoulder" — maps attention mechanisms to something everyone understands. The analogy isn't decoration; it's the explanation.
4. **Old workaround before the new feature** — Shows --fork-session first (the manual solution), THEN /btw (the elegant one). This "before/after" structure makes the new feature feel like a relief, not just an announcement.
5. **Precise tradeoff articulation** — "/btw is the inverse of a subagent. A subagent has full tools but starts with empty context. /btw sees your full conversation but has no tools." This one sentence is the kind of insight people screenshot and share.
6. **Physical metaphor to close** — "Treat your context window like your desk." Maps three features to desk operations: /btw = asking without putting paper on the desk, fork = walking to a second desk, rewind = clearing the mess. Sticky, memorable, shareable.
7. **Shortest of the three hits** — ~8 minutes. Tight, no fat. The topic is simple enough to not need a broader trend section.

---

## Full Script

Claude just dropped a feature I didn't even realise I wanted.

Here's the problem. You give the agent a big task. It's mid-flight -- reading files, writing code, running tests. And then you want to ask it something. "Hey, why'd you decide to use the library?" or "Wait, what is the auth strategy here?"

So you interrupt it. You type your question mid-session. Claude stops, answers you, and then tries to pick up where it left off.

Except now there's noise in the conversation. Your question, its answer, maybe a clarification -- none of that was relevant to the original task. And this matters more than you'd think.

## Why interrupting matters (the LLM-as-human analogy)

LLMs are more like humans than most people realise when it comes to focus.

When a person is deep in a task and you tap them on the shoulder with an unrelated question, they answer you -- but when they go back to what they were doing, they've lost the thread.

LLMs work the same way, but the mechanism is different. A language model doesn't "forget" -- instead, **the irrelevant messages sit in the context window permanently.** Every token the model generates from that point forward is influenced by everything that came before it, including your off-topic question and the answer it gave.

This is what I call **context pollution.** The conversation now has noise mixed into the signal. The model has to attend to your random question about auth strategy right alongside the actual implementation it was doing. The result: slightly worse code, slightly confused reasoning, slightly off-target decisions -- compounding over the rest of the session.

## The old workaround: spin up a second terminal

Before /btw existed, my solution was to open a second terminal and use the --fork-session flag:

```bash
claude --continue --fork-session
```

This creates a brand new session that has the full context of the original conversation but branches off independently. You can ask your question there, get an answer, and close it -- the original session is completely untouched.

It works. You get context without pollution. But it's clunky: you're opening terminals, running commands, waiting for a new session to spin up, just to ask "what was the name of that file?"

## The new solution: /btw

/btw is a side-channel question. You type it while Claude is working, and it answers in a dismissible overlay without touching the conversation at all.

Here's what makes it work:

- **Full context visibility.** It sees everything Claude has read, decided, and written in this session.
- **Zero context pollution.** The question and answer are ephemeral. They never enter the conversation history.
- **Works mid-task.** You don't have to wait for Claude to finish.
- **Low cost.** It reuses the parent conversation's prompt cache.

The tradeoff: **no tool access and single-turn only.** /btw can only answer from what's already in context. It can't read new files, run commands, or search the codebase. And you get one response -- no follow-ups.

The docs describe it well: **/btw is the inverse of a subagent.** A subagent has full tools but starts with empty context. /btw sees your full conversation but has no tools. Use /btw to ask about what Claude already knows; use a subagent to go find out something new.

## When to use /btw vs --fork-session

Both solve the same core problem -- asking questions without polluting your main session -- but they're built for different situations.

**Use /btw when:** quick one-off question, want an answer in seconds, don't need tool access.

**Use --fork-session when:** multi-turn investigation, need tool access, want to produce an artefact like a diagram from the forked context.

## What to keep in mind

**Context pollution is real and cumulative.** Every off-topic message in a conversation makes the rest of the session slightly worse. This isn't hypothetical -- it's how attention mechanisms work.

**Sometimes you need to rewind, not steer.** If Claude went in the wrong direction for 10 messages, adding a correction is sometimes worse than rewinding to before the mistake.

**Treat your context window like your desk.** Keep it clean. /btw is asking a question without putting anything on the desk. --fork-session is walking to a second desk. /rewind is clearing the mess and starting fresh from a clean point.
