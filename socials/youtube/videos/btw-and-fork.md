# /btw and --fork-session

Claude just dropped a feature I didn't even realise I wanted.

Here's the problem. You give the agent a big task. It's mid-flight — reading files, writing code, running tests. And then you want to ask it something. "Hey, why'd you decide to use the library?" or "Wait, what is the auth strategy here?"

So you interrupt it. You type your question mid-session. Claude stops, answers you, and then tries to pick up where it left off.

Except now there's noise in the conversation. Your question, its answer, maybe a clarification — none of that was relevant to the original task. And this matters more than you'd think.

---

## Why interrupting matters (the LLM-as-human analogy)

LLMs are more like humans than most people realise when it comes to focus.

When a person is deep in a task and you tap them on the shoulder with an unrelated question, they answer you — but when they go back to what they were doing, they've lost the thread. 

LLMs work the same way, but the mechanism is different. A language model doesn't "forget" — instead, **the irrelevant messages sit in the context window permanently.** Every token the model generates from that point forward is influenced by everything that came before it, including your off-topic question and the answer it gave.

This is what I call **context pollution.** The conversation now has noise mixed into the signal. The model has to attend to your random question about auth strategy right alongside the actual implementation it was doing. The result: slightly worse code, slightly confused reasoning, slightly off-target decisions — compounding over the rest of the session.

---

## The old workaround: spin up a second terminal

Before `/btw` existed, my solution was to open a second terminal and use the `--fork-session` flag:

```bash
claude --continue --fork-session
```

This creates a brand new session that has the full context of the original conversation but branches off independently. You can ask your question there, get an answer, and close it — the original session is completely untouched.

It works. You get context without pollution. But it's clunky: you're opening terminals, running commands, waiting for a new session to spin up, just to ask "what was the name of that file?"

And there's a real use case where forking still wins — I'll get to that.

---

## The new solution: /btw

`/btw` is a side-channel question. You type it while Claude is working, and it answers in a dismissible overlay without touching the conversation at all.

```
/btw what was the name of that config file again?
```

Here's what makes it work:

- **Full context visibility.** It sees everything Claude has read, decided, and written in this session. So it can answer questions about the code, the approach, the files — anything from the current conversation.
- **Zero context pollution.** The question and answer are ephemeral. They never enter the conversation history. Claude's main task continues as if nothing happened.
- **Works mid-task.** You don't have to wait for Claude to finish. You can fire off a `/btw` while it's actively reading files and writing code — it runs independently.
- **Low cost.** It reuses the parent conversation's prompt cache, so you're not paying for a whole new session.

The tradeoff: **no tool access and single-turn only.** `/btw` can only answer from what's already in context. It can't read new files, run commands, or search the codebase. And you get one response — no follow-ups. If you need a back-and-forth or need it to go investigate something, use a different approach.

The docs describe it well: **`/btw` is the inverse of a subagent.** A subagent has full tools but starts with empty context. `/btw` sees your full conversation but has no tools. Use `/btw` to ask about what Claude already knows; use a subagent to go find out something new.

---

## When to use /btw vs --fork-session

Both solve the same core problem — asking questions without polluting your main session — but they're built for different situations.

**Use `/btw` when:**
- You have a quick, one-off question about something already in context
- You want an answer in seconds without leaving your terminal
- You don't need Claude to read files or run commands to answer

**Use `--fork-session` when:**
- You want to explore a different approach or do a multi-turn investigation
- You need tool access — reading files, generating diagrams, running code
- You want to produce an artefact — like generating a Mermaid diagram or an HTML visualisation from the forked context

The fork approach is especially powerful when combined with something like the mermaid-diagram-generator skill. You fork the session, ask it to generate a diagram of what it's building so far, and you get an interactive HTML file you can open in a browser — all without the original session knowing anything happened.

---

## What to keep in mind

**Context pollution is real and cumulative.** Every off-topic message in a conversation makes the rest of the session slightly worse. This isn't hypothetical — it's how attention mechanisms work. The more noise in context, the harder it is for the model to focus on signal.

**Sometimes you need to rewind, not steer.** If Claude went in the wrong direction for 10 messages, adding a correction is sometimes worse than rewinding to before the mistake. Use `Esc+Esc` or `/rewind` to restore the conversation and code to a checkpoint before the bad reasoning started. This avoids the poisonous context problem entirely.

Being able to ask a question in mid-session, if you notice the answer is wrong, then you can stop it and then rewind more easily. 

**Treat your context window like your desk.** Keep it clean. The conversation is Claude's working memory. Every message you add — questions, corrections, tangents — is a piece of paper on the desk. `/btw` is asking a question without putting anything on the desk. `--fork-session` is walking to a second desk. `/rewind` is clearing the mess and starting fresh from a clean point.
