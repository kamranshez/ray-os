---
title: Interruptible agents #19
videoId: 2ivXNdHJpxk
url: https://www.youtube.com/watch?v=2ivXNdHJpxk
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1 — Make an agent's workflow cleanly cancellable and resumable at any point.** This is the architectural move that separates a toy agent from a 99th-percentile product, and it subsumes the queue, the convo ID, the in-progress flag, and the inner/outer loop discussion. VERDICT: 🔗 next-step video available (beyond the basic agent loop).

**Spine 2 — Run a slower, smarter supervisor model in parallel that reviews history and injects corrections into a fast agent.** Same code as interruptibility, but the interrupt now comes from a second model detecting drift rather than a human. The hosts flag it themselves as "a really dope episode." VERDICT: ❌ net-new video available.

**Spine 3 — Review the AI-proposed architecture as a diagram before any implementation.** Screenshot the spec, get a mermaid diagram, review that (the highest-leverage layer) instead of 300 lines of markdown, then hand it to the coding agent. VERDICT: 🟡 partial (fills a gap in existing planning videos).

## Summary

Vibhav (BAML) and Dex (HumanLayer) live-build interruptible agents, showing threading versus polling architectures, message queuing, inner-outer loops, and a supervisor pattern for steering agents mid-run.

🔴 1 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 — Interruptible agents

**The claim:** making a workflow cleanly cancellable and resumable anywhere is what separates a toy agent from a 99th-percentile product. **Why it's non-obvious:** most builders equate human-in-the-loop with "agent asks permission, human approves" at predefined gates. Interruptibility is the inverse: the human barges in at an arbitrary moment, resteers, and keeps the work already done. **The mechanism:** a naive loop runs to completion on one thread, so a second message either does nothing or starts a competing chat. Therefore you run the loop in its own thread, track an `in_progress` flag, and route new messages into a queue keyed by a convo ID that the backend emits as its first event; a state-modifying step then injects eligible messages at safe boundaries. Two implementations follow: poll the shared store every second between phases, or race two threads with `asyncio.gather` and crash-and-restart the agent thread on any state change. **What it generalizes to:** the same shape drives Claude Code's escape-to-steer and message-queuing UX, and voice assistants you can talk over. **How it goes wrong:** race conditions and locking bite hard, injecting mid-tool-call corrupts the flow, and the threading version discards in-progress work on every interrupt.

### Spine 2 — The supervisor pattern

**The claim:** a fast primary agent paired with a slower, smarter model that reviews the running history and injects corrections is the general recipe for keeping speed without losing control. **Why it's non-obvious:** the instinct is to make one model both fast and careful, but those pull against each other; the fix is two concurrent timelines, not a better single call. **The mechanism:** a fast agent runs (voice, deep research) at low latency, so it drifts. In parallel, a heavier model checks the state one message back (it cannot judge the live message yet), and if it detects drift it sends an interrupt saying "you are off track," which is replayed as extra context and re-runs inference from a rewound point. Because interruption is already wired up, this is, in the hosts' words, "literally the exact same code as before," only the output surface differs. **What it generalizes to:** the hosts suspect OpenAI's deep-research tools already run a supervisor that resets context mid-run. **How it goes wrong:** the supervisor lags by one message, adds cost, and needs a clear drift signal or it either nags or misses.

### Spine 3 — Architecture review via diagram

**The claim:** the highest-leverage place to spend human attention on an AI build is the architecture, and a diagram is the fastest surface to review it. **Why it's non-obvious:** teams pour review effort into the generated code, but if the architecture is wrong, everything downstream is wrong, and 300 lines of markdown architecture is nearly unreadable. **The mechanism:** because errors compound from the top, catching an architecture flaw is worth far more than catching a code flaw; a mermaid diagram compresses the same structure into something scannable, so Vibhav screenshots the whiteboard, asks an LLM to emit mermaid, reviews the diagram, then feeds it plus the goal to Cursor to implement. The diagram becomes the shared review artifact between human and coding agent. **What it generalizes to:** any non-trivial feature where you direct a coding agent, and reviewing Claude Code's own generated design before letting it write code. **How it goes wrong:** the diagram detaches from the code once implementation starts (BAML's markdown-in-code demo targets exactly this drift), and a plausible-looking diagram can still hide the flaw.

## 🎬 Proposed ACS videos

### 1. Build an Agent You Can Interrupt Mid-Run

- **HOOK:** Your agent finishes a five-minute research run, and only then do you realize you asked the wrong question.
- **THE PROMISE:** For anyone building their own agent loop. After this you can cancel and resteer a running agent without throwing away the work it already did.
- **THE SHAPE:** (1) Demo the annoying non-interruptible research agent. (2) Draw the while-true loop, add an in-progress flag and a message queue. (3) Emit a convo ID as the first backend event, poll the store between phases. (4) Show the threading alternative: `asyncio.gather` race, crash the agent thread on any state change, restart from last known state. (5) Contrast the two trade-offs and add two urgency levels (interrupt now versus next opportunity).
- **SPINE:** 1
- **SLOT:** Techniques class, new "Interruptible agents" chapter next to core-agent-loop.
- **RELATIONSHIP:** 🔗 complements core-agent-loop (Techniques backlog), which teaches the basic while-true / call-LM / call-tool loop; this video is the next step, adding the interrupt, queue, and thread-race layer that the basic loop lacks. Do not re-teach the basic loop; open on it and immediately break it.
- **PROOF TO REUSE:** the wombat/woodpecker research-agent demo; the two implementations (poll every 1s versus asyncio race with crash-and-restart); "Claude Code does this exact thing, the first message emitted from the back end is a JSON object that gives you the session ID"; the two-urgency-levels idea (interrupt-and-send-now versus insert-at-next-opportunity).

### 2. A Second Model That Watches Your Agent and Steers It

- **HOOK:** What if a smarter model rode shotgun, caught your fast agent drifting, and corrected it live without stopping it?
- **THE PROMISE:** For anyone building fast or voice agents. After this you can run a concurrent supervisor that injects corrections into a running agent mid-flight.
- **THE SHAPE:** Central demo: take the interruptible architecture from video 1, add a slower, smarter model that reviews history one message back, detects drift, and injects a "you are off track" message that replays inference from a rewound point; show it correcting the research agent, then explain the voice-agent variant where only the output surface changes.
- **SPINE:** 2
- **SLOT:** Techniques class, next to subagent-verification-loops and closing-the-loop.
- **RELATIONSHIP:** ❌ net-new. The catalog's closing-the-loop (filmed) and subagent-verification-loops (backlog) both check work sequentially, after the fact; nothing covers a concurrent supervisor monitoring and interrupting a live agent.
- **PROOF TO REUSE:** "this would be a really dope episode is just like how to use a small model and use a supervisor to inject messages into the context"; the "always check state one message back" mechanism; the fast-voice-agent-drifts example; "it's literally the exact same code as before, only the stood out is slightly different."

### 3. Review the Diagram, Not the 300 Lines of Markdown

- **HOOK:** The model just wrote your architecture as 300 lines of prose. You are about to skim it and miss the flaw.
- **THE PROMISE:** For anyone directing a coding agent on a non-trivial feature. After this you review AI-proposed architecture through a diagram and catch design errors before implementation.
- **THE SHAPE:** (1) Screenshot the spec or whiteboard. (2) Ask an LLM for a mermaid diagram of the plan. (3) Review the diagram as the highest-leverage layer, iterate on it, not the code. (4) Feed the diagram plus the goal to the coding agent to implement.
- **SPINE:** 3
- **SLOT:** Context Engineering class, or Techniques next to high-level-strategy-low-level-details and goal-in-strategy-out.
- **RELATIONSHIP:** 🟡 fills the gap in high-level-strategy-low-level-details and goal-in-strategy-out (both filmed) and Ultra Plan (V20). Those teach reviewing the plan before executing; none teach using a compressed diagram as the review medium for AI-generated architecture specifically.
- **PROOF TO REUSE:** "if the architecture is wrong everything else is going to be wrong"; the whiteboard-screenshot to mermaid to Cursor workflow; "if the model just outputs 300 lines of markdown for the architecture that becomes really hard to read."

## 📚 Full wisdom (reference)

**SUMMARY:** Vibhav (BAML) and Dex (HumanLayer) live-build interruptible agents, showing threading versus polling architectures, message queuing, inner-outer loops, and a supervisor pattern for steering agents mid-run.

**IDEAS**
- Making a workflow cleanly cancellable and resumable anywhere puts your product in the ninety-ninth UX percentile.
- Interruptibility means resteering an agent mid-run without starting from scratch, keeping the work already asked for.
- Building interruptible agents requires shared state across threads plus a clear foreground-versus-background split between running processes.
- The agent loop is simply: while true, call the LLM; if done return, else call tools.
- Track an in-progress flag so a second message queues instead of wrongly starting a brand-new chat.
- Claude Code immediately emits the session ID as the first JSON object from backend to frontend.
- Threading implementation crashes the agent thread on any database update, then restarts from last known state.
- The while-loop version polls the shared database every second for queued messages between phase boundaries instead.
- asyncio.gather races two threads; whichever returns first decides whether to inject state or return the results.
- Build at least two message urgency levels: interrupt and send now, or insert at next opportunity.
- A state-modifying method decides which queued messages are eligible to inject given the current runtime state.
- After injecting a queued message, emit an event so the UI shows it acknowledged, not pending.
- Owning the flow beats a framework when you must reach into behavior the framework never exposes.
- The best agents each reinvented UX; Cursor reinvented diffs, Claude Code reinvented terminal queuing and waiting.
- Screenshot a whiteboard, ask an LLM for a mermaid diagram, then feed that diagram to Cursor.
- Put human attention on the highest-leverage layer: architecture first, because a wrong architecture dooms everything downstream.
- A supervisor runs a slower, smarter model reviewing history and injecting corrections into a fast agent.
- Supervisors always check state one message back, since they cannot yet evaluate the current live message.
- Fast voice agents drift off-topic, so a slower parallel reviewer catches drift and injects steering corrections.
- Warp detects topic changes and offers a new conversation instead of blindly continuing the running thread.

**INSIGHTS**
- Interruptibility is the next level of human-in-the-loop: resteering an agent, not just approving its permission requests.
- The hard part is race conditions and locking, not the code; system design earns its keep.
- Inner loop keeps calling tools autonomously; outer loop hands control back to a human for input.
- Done means the inner loop completed, not that the whole conversation is finished; users decide that.
- Threading interrupts instantly but restarts work; polling finishes current work first; each trade-off fits different goals.
- The same architecture powers interruptibility, deep-research supervision, and voice correction; only the final output surface changes.
- AI writing the code cheaply makes owning the flow worthwhile, since flexibility no longer costs much.
- Diagrams review AI-generated architecture far faster than reading three hundred lines of dense unstructured markdown prose.
- Coding agents excel inside formal state machines where the boundaries and transitions are clearly enforced structurally.
- Great agent products win by reinventing UX, not just by using a smarter underlying core model.

**QUOTES**
- "If you make a workflow so it can be cleanly and safely cancelled anywhere and still resumed then you are probably building a product that is in the 99th percentile." — Dex
- "you can't actually build interruptible agents without doing some kind of state sharing across threads." — Vibhav
- "inner loop is anything where you just keep calling tools ... outer loop is anything that requires a human to be in the loop." — Dex
- "Claude code does this exact thing ... the first message emitted from the back end to the front end is a JSON object that gives you the session ID." — Dex
- "building is not as hard anymore because we have AI agents that help you write some of this code." — Vibhav
- "if the architecture is wrong everything else is going to be wrong." — Dex
- "what makes the best agents today successful is that almost every single one of them has reinvented UX in some way." — Vibhav
- "you're having a smarter model go through and maybe inject a message like oh actually I'm doing it wrong we should do this instead." — Dex
- "this would be a really dope episode is just like how to use a small model and use a supervisor to inject messages into the context." — Vibhav

**HABITS**
- Vibhav writes a test case for a planning prompt before trusting its structured query output downstream.
- He uses GPT-4o for simple planning steps, reserving heavier models for the harder reasoning-intensive downstream work.
- He dictates long prompts by voice with Wispr Flow to pack in far more context easily.
- He asks the model to explain the plan in theory first, explicitly forbidding it from implementing.
- He spends real time studying architecture visuals because diagrams let him understand system behavior much faster.
- He requires the responses-API client to always call the web-search-preview tool, enforcing search on every run.
- He pushes the base query into every prompt so core context persists across all pipeline steps.
- Dex models agent systems as formal state machines with clearly enforced boundaries and explicit phase transitions.

**FACTS**
- Wombat poop is genuinely cube-shaped, and woodpecker tongues wrap all the way around the skull's back.
- The OpenAI responses API runs tool calls server-side, so JSON never round-trips back to the client.
- Claude Code had no free tier and still overtook Cursor by reinventing terminal queuing UX entirely.
- The 12-factor-agents methodology formalizes the inner-loop versus outer-loop distinction underpinning modern agent control flow design.
- Vibhav recently reduced the BAML repo from about 280 megabytes down to roughly 170 megabytes total.
- Warp warns when a conversation's topic changes and asks whether to start a new conversation instead.
- BAML uses markdown syntax embedded in code to render meaningful sections as navigable click-through code graphs.
- Neither Gemini nor ChatGPT rendered mermaid diagrams inline at recording time, which surprised both hosts noticeably.

**REFERENCES:** BAML; HumanLayer; the 12-factor agents methodology; Claude Code; Cursor (GPT-5 max); Warp; OpenAI responses API and web-search-preview tool; GPT-4o; Wispr Flow; SuperWhisper; ChatGPT; Gemini; Anthropic Claude; Mermaid and mermaid.live; Excalidraw; Nature (cited as a research resource); asyncio; the Half-Life 3 running joke.

**ONE-SENTENCE TAKEAWAY:** Build agents that can be cleanly interrupted and resteered mid-run by owning the flow yourself.

**RECOMMENDATIONS**
- Always run your agent loop inside a dedicated thread so external messages can interrupt it mid-execution.
- Track an in-progress flag and queue incoming messages instead of spawning a competing parallel chat thread.
- Emit a conversation ID as the first backend event so queued messages resolve to it later.
- Write a dedicated method that decides which queued messages are eligible to inject right now cleanly.
- Screenshot your whiteboard, have an LLM produce a mermaid diagram, then hand it to your coder.
- Review the architecture diagram before any implementation, since a wrong architecture invalidates everything built afterward downstream.
- Build a slower supervisor model that reviews history and injects steering messages into fast running agents.
- Prompt the model to explain the plan in theory first before permitting any code implementation whatsoever.
