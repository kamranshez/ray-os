---
duration: "12-16 min"
batch: 3
order: 8
batch_name: "L2 Foundations"
class: "loopy-ai"
chapter: "Architecting The Loop"
aliases: [architecting-the-loop]
status: stub
---

Stub for the loop-architecture segment. What tools, sensors, and actuators the agent needs in order to actually close *this particular* loop.

Working title. Alternatives: "Giving Your Agent A Body" / "Wiring The Agent Into The World" / "Sensors And Actuators."

## Thesis

A loop only closes if the agent can *act on* and *perceive* the thing it's supposed to be working on. Most failed loops aren't failing because the model is bad. They're failing because the model can't see the result of its action, or can't act in the modality the task lives in.

Before you write the prompt, write the *interface*. What tools does this loop need? What does the agent need to see, hear, send, store, query, in order to close the goal on its own?

This is the architecture step. It comes before the prompt step. Most people skip it and wonder why their loops stall.

## The worked example

Voice calling agent. You want an agent that can pretend to be you on a call, or pretend to be a different agent talking to a human, and adjust mid-conversation. What does it actually need?

- **Speaker.** Output audio. Not "produce a string the user will read." Actually emit sound to a device.
- **Phone or call transport.** Make the call, hold the call, end the call. SIP, Twilio, whatever the substrate is.
- **Microphone.** Hear the other side.
- **Transcription.** Convert what it hears into text the model can reason about.
- **A loop.** Listen, transcribe, decide, speak, listen again. Every turn closes when the speech is sent and the next transcription comes back.

Without any one of those five, the loop doesn't close. The model could be perfect and the agent still won't work. Giving the agent only a microphone and a model gets you a transcriber, not a caller.

## The architecture-first checklist

For any loop you want to build, write this down before you write the prompt:

1. **What does the loop need to perceive?** (Inputs: files, transcripts, screenshots, API responses, queue items, sensor readings.)
2. **What does the loop need to act on?** (Outputs: shell commands, file writes, API calls, messages sent, audio emitted, hardware triggered.)
3. **What does the loop need to *check*?** (Verifier: an external grader, a test suite, a borrowed verifier — covered in segment 2.2.)
4. **What state does the loop need to remember between turns?** (Scratchpads, playbook files, queue position, conversation history.)
5. **What does the loop need to be able to *stop on*?** (Termination signal: a passing check, a budget exhaustion, a kill switch.)

Five interfaces. If any one is missing, the loop has a hole. The model will paper over the hole with confidence. The hole stays.

## Worked examples across domains

- **Voice agent.** Speaker, phone, microphone, transcription, conversation history.
- **YouTube ops agent.** YouTube Data API, analytics API, video file upload, thumbnail upload, comment read, comment reply.
- **Coding agent.** File system, terminal, browser preview, test runner, linter.
- **Sentence-mining agent.** Source corpus access, dictionary API, TTS engine, Anki Connect, target word list.
- **Sales outreach agent.** Lead list, email send, inbox read, CRM write, deliverability checker.

Each one is the same pattern. Five interfaces, all of them concrete tools, none of them prompt-level.

## What this segment is *not*

Not a tour of every MCP server. Not a checklist of brand-name tools. The point is that the *architecture decision* of what interfaces the loop needs is upstream of the prompt, and most people never make that decision explicitly.

## Sources / refs

- Loop Bank idea (added 2026-06-07 from the conversation)
- Pairs with [[closing-the-loop]] (verifier-in-the-loop) and [[borrowed-verifiers]] (where the check comes from).
- Sets up [[l4-workers]] and [[l5-discovery]] (every worker and discovery loop is an architecture decision before it is a prompt).
- Connects to [[mission-command]] (the intent doc tells you *what* good looks like; the architecture tells you *whether the loop can even reach it*).

## TODO

- Demo: stand up the voice agent on screen. Speaker plays audio, phone places a call, transcription pipes back, the agent reasons, the loop closes. Three minutes of footage. The point is to watch a loop *actually close* because the interfaces were wired right.
- Image: a single agent box in the middle, five labelled cables coming out of it — perceive, act, check, remember, stop.
- Decide final segment name (see working title alternatives at top).
