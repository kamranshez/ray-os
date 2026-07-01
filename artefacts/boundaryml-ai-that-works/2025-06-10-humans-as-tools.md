---
title: Humans as Tools #8
videoId: NMhH5_ju3-I
url: https://www.youtube.com/watch?v=NMhH5_ju3-I
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1: Enforce human approval for dangerous tools inside your own loop's switch statement, not in the prompt, so no injection can ever bypass it.** This is the most distinctive, most demo-able claim in the video, and it is what makes people trust agents with money and infrastructure.
VERDICT: 🔗 next-step video available.

**Spine 2: Own your agent's while loop and state object instead of adopting a black-box framework, because the LLM is just an implementation detail.** This is the video's highest-altitude reframe and it subsumes most of the other ideas (own the state, own the control flow, just write the loop).
VERDICT: ❌ net-new video available.

**Spine 3: Make human-in-the-loop and long-running steps durable by exiting to a database and resuming from a second entry point.** This is the concrete production pattern that lets an agent survive a five-day human wait or a mid-call server crash.
VERDICT: ❌ net-new video available.

## Summary

BoundaryML's Vaibhav and HumanLayer's Dexter demo production human-in-the-loop agents, arguing it's ordinary software: own the loop, gate risky tools deterministically, and treat LLMs as detail.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: Deterministic, injection-proof approval gates

The claim: certain tools should be impossible to run without a human, and you guarantee that in code, not in the prompt. Why it's non-obvious: people reach for a system prompt ("always ask before refunding") and trust the model to comply, which prompt injection or a bad classification can defeat. Why it's true: in Dexter's agent the model only declares intent by emitting a structured tool call; a switch statement, not a function map, decides what happens next. When the chosen tool is marked unsafe (divide, refund), the loop deterministically exits to ask_human before any execution, so "the only way divide can be triggered is it goes through here." No token the model or an attacker produces changes that path, because the path is ordinary control flow. What it generalizes to: financial systems (refunds only after a support agent clicks) and infrastructure (a Terraform apply that always pings a human in Slack). How it goes wrong: if you let a natural-language reply stand in for the click, an LLM classifier re-enters and raises your error rate, so for the truly dangerous actions require a literal button. As they put it: "There's no prompt injection ever possible that breaks that. It's always deterministic. It's just code. It's just software."

### Spine 2: Own the loop, the LLM is an implementation detail

The claim: build the agent as a while loop you write, over a state object you own, and the LLM becomes an implementation detail. Why it's non-obvious: the reflex is to adopt LangGraph, AutoGen, or Swarm and let them own the loop. Why it's true: those frameworks run the while loop under the hood, so when you need to pause, introspect, checkpoint, or stop a run, you have no handle, because you never held the loop. Write the four-step loop yourself (prompt, switch on the structured output, run code, append the event, repeat) and the state becomes a plain object you serialize however you want, not OpenAI's chat-message chain. Then "LLMs are just functions: thread in, one of your declared types out," and everything around them is software you already know how to test and control. What it generalizes to: multi-agent and multi-threaded systems, where owning the loop is exactly what lets you send a pause signal, serialize each worker, and reason about locks. How it goes wrong: DIY means more code you must maintain, and frameworks still earn their place for battle-tested durable execution. But "if the only benefit you're getting is running the while loop, just write the damn while loop," and "duplication is better than the wrong abstraction."

### Spine 3: Exit to a database for durable, resumable steps

The claim: make human and long-running steps durable by exiting to a database and resuming from a second entry point. Why it's non-obvious: the naive shape is an ask_human() call that blocks inside the tool, holding the loop open until someone clicks. Why it's true: a human might take five days, and a held-open loop wastes a running process and loses everything if the server crashes mid-call. Instead, when the agent hits a human or long-running tool, serialize the whole thread to a DB and exit. A separate workflow then contacts the human, and when the response webhook arrives carrying the saved state ID, a second entry point rehydrates the context, appends the result, and feeds it back to the LLM. The task graph now has two entry points: start from zero, and resume from saved state. What it generalizes to: any async job (AWS SQS, Temporal, Cadence, and LangGraph checkpoints all solve this), where Dexter just hand-rolls the minimal version to a file system. How it goes wrong: you now own serialization, idempotency, and the resume path, and skipping checkpointing means a crash mid-approval strands the conversation. As Vaibhav says: "The way I think about this is I just exit to a database." He contrasts mailto prefill (state in the URL) with GitHub issue templates (state in a DB).

## 🎬 Proposed ACS videos

### 1. Make Your Agent Ask Permission (And Make It Impossible to Skip)

- HOOK: Your agent will eventually try to refund a customer or tear down infra, so here is how to guarantee a human signs off first, no matter what the prompt says.
- THE PROMISE: For anyone building their own agent, after this you can mark any tool "needs approval" so the gate is injection-proof by construction, not by hoping the prompt holds.
- THE SHAPE:
  1. Build a tiny agent with add and divide tools, mark divide "unsafe."
  2. Show the loop deterministically exit to ask_human before divide ever runs.
  3. Prove it: even "no, use 6 instead" re-triggers approval, and injection cannot bypass the switch statement.
  4. Extend to a refund tool routed to a manager over Slack or email (the multiplayer demo).
  5. Land the rule: the gate lives in code, the LLM only declares intent.
- SPINE: Spine 1.
- SLOT: Claude Code class, adjacent to the backlog item blocking-risky-commands-with-hooks (or Techniques class).
- RELATIONSHIP: 🔗 complements "blocking-risky-commands-with-hooks", which blocks Claude Code's own bash via hooks, by moving the same guarantee inside an agent you build yourself, enforced in the loop's switch statement rather than in a Claude Code hook.
- PROOF TO REUSE: the divide and refund toy tools; "there's no prompt injection ever possible ... it's just code, it's just software"; the refund-to-manager multiplayer demo; the credit-card-alert-over-500-dollars trust analogy.

### 2. Write the Damn While Loop: Why I Do Not Use Agent Frameworks

- HOOK: LangGraph, AutoGen, and Swarm all own your loop, which means you cannot pause it, inspect it, or checkpoint it, and the LLM is just an implementation detail anyway.
- THE PROMISE: For engineers deciding how to build an agent, after this you can build one as a plain while loop over a state object you own, and know exactly when a framework earns its place.
- THE SHAPE:
  1. Show the four-step inner loop: prompt, switch on the structured output, run code, loop.
  2. Reveal the "thread" as an object you invented, serialized to JSON and text, not a chat-message chain.
  3. Contrast with black-box frameworks you cannot stop mid-run.
  4. Land "LLMs are just functions: thread in, one of your types out."
  5. Payoff: because you own it, you can swap CLI, web, and email interfaces and introspect state.
- SPINE: Spine 2.
- SLOT: Techniques class (core-agent-loop and agent-harness-concept are unfilmed backlog names) or Context Engineering class.
- RELATIONSHIP: ❌ net-new. No filmed ACS video makes the framework-versus-DIY argument or teaches owning your own agent state object; core-agent-loop and agent-harness-concept exist only as backlog names, not coverage.
- PROOF TO REUSE: the four-step loop whiteboard; "just write the damn while loop"; "duplication is better than the wrong abstraction" and "code you own beats code you don't own"; unify execution state and business state; the JSON-versus-text dual serialization for humans and code.

### 3. Exit to a Database: How to Survive a Five-Day Human Wait

- HOOK: A human might approve your agent's action in five minutes or two weeks, and you cannot leave a while loop spinning, so exit to a database and resume later.
- THE PROMISE: For anyone shipping agents to production, after this you can make any human or long-running step crash-safe and resumable, without buying into Temporal or LangGraph.
- THE SHAPE:
  1. Hit a human or long-running tool, serialize the whole thread to a DB, then exit.
  2. A second entry point resumes from saved state when the response webhook lands.
  3. Show why you cannot hold the tool call open (a server crash mid-call loses state).
  4. Two entry points into the same task graph: start from zero, and resume from state.
  5. Name the grown-up versions: SQS, Temporal, Cadence, LangGraph checkpoints.
- SPINE: Spine 3.
- SLOT: Techniques class or Context Engineering class (durable and resumable agents).
- RELATIONSHIP: ❌ net-new. ACS has no filmed video on durable or resumable agent execution or checkpointing your own loop; checkpoints-and-rewind covers Claude Code's built-in rewind, which is a different thing.
- PROOF TO REUSE: "the way I think about this is I just exit to a database"; the server-crash-mid-tool-call failure case; the mailto-prefill (state in URL) versus GitHub-issue-template (state in DB) analogy; the webhook-callback-with-state-ID resume.

### Also film-able (not deep-dived)

- **Humans as a new surface area** (business): deploy your agent onto email or Slack so users approve and reply where they already are, instead of pulling them back into your SaaS. 🔗 complements the backlog item agent-mail by making "meet the user where they are" the design principle, not just an inbox. PROOF: "a human is a new surface area"; the mail-to-links growth-loop point; users log in once and then interact from everywhere.

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's Vaibhav and HumanLayer's Dexter demo production human-in-the-loop agents, arguing it's ordinary software: own the loop, gate risky tools deterministically, and treat LLMs as detail.

### IDEAS
- Human-in-the-loop is not AI magic; it is ordinary software architecture you already know how to build.
- Mark risky tools like divide or refund unsafe so the loop deterministically exits before running them.
- A code switch statement, not a prompt, enforces approval, so no injection can ever bypass it.
- When you hit a human or long-running tool, serialize the thread to a database and exit.
- A second entry point resumes the paused agent from saved state when the human finally responds.
- The agent's state is any object you invent and serialize, not OpenAI's rigid chat message chain.
- Store one thread as JSON for code and as readable plain text for humans debugging faster.
- Natural-language email approvals raise the error rate; a button click stays nearly deterministic for high-stakes decisions.
- Assert on model output length in code; if it fails, fall back to requesting more information.
- Humans are a new surface area, like touchscreens or TVs, that software must be designed around.
- Deploy agents where users already are; let them reply in natural language instead of reopening apps.
- Black-box frameworks like LangGraph, AutoGen, or Swarm own the while loop, so you cannot pause them.
- LLMs are just functions: they take a thread and return one of your declared output types.
- The core magic of LLMs is turning unstructured data into JSON your existing code can use.
- Deterministic human gates let people trust agents with Terraform applies, refunds, and emails they'd normally refuse.
- Multi-agent systems are just multi-threaded code; if you own the loop you can pause and serialize.

### INSIGHTS
- The LLM triggering a workflow is an implementation detail; the surrounding process design predates AI itself.
- Owning the control loop, not the framework owning it, is what lets you pause, inspect, checkpoint.
- Determinism, not model capability, is what earns human trust to hand agents genuinely dangerous production actions.
- The boundary between LLM output and deterministic code is where you insert assertions, fallbacks, and control.
- Adding humans expands the surface area software serves, like adding touchscreen, tablet, or TV platforms did.
- Unifying execution and business state into one owned object unlocks views for humans, code, and models.
- Shipping fast with a twenty-percent failure rate often beats nine months chasing an imagined perfect system.
- Duplicated code you own beats the wrong abstraction, especially when the AI landscape changes this fast.
- Trust in agents is built incrementally, mirroring how mobile check deposit and card alerts earned acceptance.
- Don't rebuild your product as agents; sprinkle LLM magic into the existing code you already have.
- Most successful AI apps making real revenue are mostly ordinary code, with AI a small part.

### QUOTES
- "The fact that it's an AI is just an implementation detail. That's the key part." (Dexter)
- "There's no prompt injection ever possible that breaks that. It's always deterministic. It's just code. It's just software." (Vaibhav)
- "The way I think about this is I just exit to a database." (Vaibhav)
- "LLMs are just functions. They take an input, in this case a thread, and they spit out one of the types that we want." (Vaibhav)
- "The number one concept, the thing that LMs are really freaking good at that creates magic, is turning unstructured data into JSON." (Vaibhav)
- "Duplication is better than the wrong abstraction." (quoting the Ruby community)
- "If the only benefit you're getting from there is just running the while loop, just write the damn while loop." (Vaibhav, paraphrasing Dexter)
- "By leveraging AI in a way that is reliable, trustworthy, and engaging, we'll earn the right over time." (Vaibhav)
- "It might be better to ship in two days and get to production with a 20% failure rate than to build it out for 9 months perfectly." (Vaibhav)
- "No matter what prompt injection happens, it will always go to someone in your support team to actually hit the checkbox before money transfers over." (Vaibhav)

### HABITS
- They use toy tools like add and divide in every demo to keep the concept unambiguous.
- Dexter builds all of his agents to run over email, forcing an asynchronous days-long interaction model.
- They put human-readable timestamps on threads so the most recent conversation is findable without scanning UUIDs.
- They store the same thread twice: JSON as the source of truth and text for reading.
- They start sessions with a live demo instead of the usual whiteboard to spark viewers' imagination.
- They lean on type systems, expecting compilation to catch most integration errors before running the agent.
- In production they store agent thread state in Redis, but insist any backing store works fine.
- They write assertions and tests directly from real captured conversations, converting live runs into regression cases.

### FACTS
- Go the language was designed around channels for passing data across concurrent processes quickly and easily.
- Anthropic's Model Context Protocol has an elicitation API for presenting users specific options rather than questions.
- The phrase "duplication is better than the wrong abstraction" came from the Ruby community around 2014.
- Slack's Electron desktop app can consume roughly seventy gigabytes of RAM, yet users tolerate it anyway.
- Software companies have emailed users links to pull them back into apps for over a decade.
- Durable workflow engines like Temporal, Cadence, and LangGraph exist specifically to checkpoint and resume long-running processes.
- Airlines match your phone number to your booking so they can confirm your upcoming flight instantly.
- AWS SQS lets a system trigger a separate workflow rather than blocking on a spinning loop.

### REFERENCES
- BoundaryML "AI That Works" series (this is episode #8, Humans as Tools).
- 12-Factor Agents (workshop and methodology), referenced repeatedly: own your context, unify execution and business state, trigger via REST or MCP.
- BAML (BoundaryML's function and prompting language).
- HumanLayer (Dexter's project): SDKs and CLIs for human approvals across Slack, email, and Teams; mostly open source.
- Anthropic Model Context Protocol (MCP) and its elicitation API.
- Durable and async tooling: LangGraph, Temporal, Cadence, AWS SQS.
- Multi-agent frameworks mentioned critically: AutoGen, AG2, Swarm.
- Go programming language (channels / CSP).
- "Duplication is better than the wrong abstraction" (Sandi Metz / Ruby community, circa 2014).
- Vercel AI SDK (referenced as "Verselai").
- Storage options named: Redis, SQL, memcache, Iceberg cold storage, the file system.

### ONE-SENTENCE TAKEAWAY
Human-in-the-loop is just software: own your loop, gate risky tools deterministically, treat AI as detail.

### RECOMMENDATIONS
- Mark each dangerous tool unsafe and force a deterministic human approval step in your loop code.
- Define your own thread object and serialize it yourself rather than depending on framework message chains.
- For long human waits, exit the loop, save state, and resume via a second entry point.
- Add timestamps to stored threads so debugging never means scanning through walls of opaque UUID strings.
- For truly high-stakes actions, require an explicit button click instead of natural-language approval to reduce errors.
- Assert on model outputs in code and programmatically downgrade to requesting more info when checks fail.
- Write the while loop yourself when a framework's only benefit is running that loop for you.
- Turn each real captured conversation into an assertion-backed test to lock behavior against future prompt changes.
- Deploy your agent onto email or Slack so users approve and reply where they already work.
- Start integrating AI by turning unstructured input into JSON inside code you already own and trust.
