---
duration: "12-16 min"
batch: 2
order: 6
batch_name: "Builder and Verifier"
class: "loopy-ai"
chapter: "Builder and Verifier"
aliases: [building-the-verification-environment, architecting-the-loop]
---

> NOTE — fold in the concrete angle from the L2 chapter discussion: (1) **runtime choice** — the Claude Code terminal can't do computer use, so when the check needs a GUI you move to the Claude Desktop app or the Codex app; match the runtime to what the verifier must observe. (2) **the sensing rig** — wiring mic + speaker (or a virtual audio device) so an agent can verify a dictation app (Hyperwhisper-style): play a known clip → capture the transcript → diff against ground truth. The existing "perceive + act before you prompt" framing is the abstract version of exactly this.

Before you write the prompt, you write the interface.

Most loops that fail don't fail because the model is bad. They fail because the agent can't see the result of its own action, or can't act in the place the work actually lives. The model could be perfect and the loop still wouldn't close.

So there's a step that comes before the prompt. It's the architecture step. You decide what the agent can perceive and what the agent can act on, before you write a single word telling it what to do. Almost nobody does this on purpose. They jump straight to the prompt, the loop stalls, and they blame the model.

This segment is that missing step.

---

## The mistake everyone makes

You've spent the last few segments learning to close the loop. A builder does the work, a verifier checks it, the loop only exits when the check passes. You learned to borrow the verifier instead of letting the model grade itself, and you learned to pair every creator with an attacker when no borrowed verifier exists.

All of that is about the *check* slot. It assumes the agent can already do the work and already see the result.

That assumption is where loops quietly die.

Here's the pattern. Someone wants an agent that handles their phone calls. So they write a beautiful prompt. "You are a warm, professional assistant. You speak naturally. You handle objections gracefully." They run it. Nothing happens, or they get a wall of text where a conversation should be.

The prompt was never the problem. The agent had no speaker, no microphone, no call transport. It could generate the words a caller would say. It could not place a call, hear a reply, or make a sound. They gave it a brain and no body, then wondered why it couldn't talk.

[IMAGE: dark canvas, a glowing brain floating alone with no limbs, a phone ringing across a gap it cannot reach, caption "perfect prompt, no body"]
![[loopy-architecting-the-loop-brain-no-body-1.png]]
![[loopy-architecting-the-loop-brain-no-body-2.png]]
![[loopy-architecting-the-loop-brain-no-body-3.png]]
![[loopy-architecting-the-loop-brain-no-body-4.png]]
![[loopy-architecting-the-loop-brain-no-body-5.png]]

This is the most common failure in the whole stack, and it has nothing to do with prompting. The model can't close a loop it can't reach into.

---

## The core insight: write the interface first

A loop only closes if the agent can act on, and perceive, the exact thing it is supposed to be working on.

So before you write the prompt, you write the interface. You answer one question: what does this agent need to be able to *do* and *see* in order to close this goal on its own, with nobody in the chair?

Notice this is the same five primitives you've had since the strip-the-model-out segment, looked at from the outside. Back then we cared about whether each slot existed: trigger, work, check, terminate, state. Now we care about something more physical. For each slot, what concrete tool does the agent reach for? A primitive is a hole in the loop. An interface is the actual cable you plug into that hole.

The prompt is the easy part. You can always rewrite a prompt. What you cannot do is prompt your way past a missing speaker. If the agent has no way to emit sound, no sentence you write will make sound come out.

Architecture is upstream of prompting. Get the body right and a mediocre prompt still closes the loop. Get the body wrong and the best prompt in the world stalls forever.

---

## The worked example: a voice calling agent

Let's build the body of one agent so you can see what "write the interface first" actually means. The hardest one. A voice agent that can get on a phone call and hold a real conversation, adjusting mid-sentence.

Forget the prompt entirely for a moment. What does this thing need just to exist?

- **A speaker.** It has to emit audio to a device. Not "produce a string the human reads off the screen." Actually make sound. This is an actuator.
- **Call transport.** It has to place the call, hold the line, and hang up. SIP, Twilio, whatever the substrate is. Another actuator.
- **A microphone.** It has to hear the other side. This is a sensor.
- **Transcription.** It has to turn what it hears into text it can reason over. The sensor feeds raw audio; transcription makes it legible to the model.
- **Conversation history.** It has to remember what was said two turns ago so it doesn't repeat itself or lose the thread. This is the state slot.

Five interfaces. Pull any one of them out and the loop will not close, no matter how good the model is.

Give it only a microphone and a model and you have built a transcriber, not a caller. It can hear and think and it can say nothing. Give it only a speaker and a model and you have built a robot that talks over people, deaf to every reply. The loop closes only when all five are wired: it listens, transcribes, decides, speaks, and listens again. Every turn closes when the speech goes out and the next transcription comes back.

[IMAGE: dark canvas, a single agent box in the center with five labelled cables coming out of it, perceive / act / check / remember / stop, each cable plugged into a real device]
![[loopy-architecting-the-loop-five-cables-1.png]]
![[loopy-architecting-the-loop-five-cables-2.png]]
![[loopy-architecting-the-loop-five-cables-3.png]]
![[loopy-architecting-the-loop-five-cables-4.png]]
![[loopy-architecting-the-loop-five-cables-5.png]]

That diagram is the whole segment. One agent in the middle. Five cables. Every loop you ever build is that picture with different labels on the cables.

---

## The architecture-first checklist

For any loop you want to build, write these five lines down before you write the prompt. Not in your head. On the page.

1. **What does the loop need to perceive?** The inputs. Files, transcripts, screenshots, API responses, queue items, the other person's voice. This is the sensor list.
2. **What does the loop need to act on?** The outputs. Shell commands, file writes, API calls, messages sent, audio emitted, a PR opened. This is the actuator list.
3. **What does the loop need to check?** The verifier. An external grader, a test suite, the borrowed verifier we met in the closing-the-loop segment. This is where the last few videos plug in.
4. **What does the loop need to remember between turns?** The state. Scratchpads, a playbook file, queue position, conversation history.
5. **What does the loop need to be able to stop on?** The termination signal. A passing check, an exhausted budget, a kill switch.

Five interfaces. If any one is missing, the loop has a hole. And here is the part that costs people weeks: the model will paper over the hole with confidence. Ask it to do the thing and it will narrate the thing convincingly. It will say it placed the call. It will report that the email went out. The hole stays. The work never happened. A loop with a missing actuator doesn't error. It hallucinates success.

So you find the holes on paper, before the prompt, when finding them is free.

---

## Same pattern, every domain

Once you've seen it on the voice agent, you see it everywhere. Same five slots, different cables.

- **Voice agent.** Speaker, call transport, microphone, transcription, conversation history.
- **YouTube ops agent.** Data API, analytics API, video upload, thumbnail upload, comment read, comment reply. It perceives through analytics, acts through the upload and comment endpoints.
- **Coding agent.** File system, terminal, browser preview, test runner, linter. This is the one Claude Code wires for you, which is exactly why coding felt solved while everything else felt hard.
- **Sentence-mining agent.** Source corpus access, dictionary API, a text-to-speech engine, Anki Connect, the target word list as state.
- **Sales outreach agent.** Lead list, email send, inbox read, CRM write, a deliverability checker as the verifier.

Every one is the same shape. Five interfaces, all of them concrete tools, none of them living at the prompt level. The reason coding agents arrived first is not that code is special. It's that the IDE and the terminal already handed the model a full body. In every other domain, you have to assemble the body yourself. That assembly is the work this segment is about.

This is also why I keep a running list of the bodies I've already built. Call it a loop bank. Every time I wire up a new interface, the cable goes in the bank, and the next agent that needs to read an inbox or emit audio inherits it instead of starting from a brain in a jar.

---

## What this segment is not

This is not a tour of every MCP server. It is not a ranked list of brand-name tools you should go install.

The tools change every month. The decision does not. The decision is: what does this loop need to perceive, act on, check, remember, and stop on. That question is upstream of whichever tool is fashionable this week, and it is the question nobody writes down.

Get in the habit of writing the five lines first. The prompt gets easier every time you do, because by the time you reach the prompt, the agent already has a body that can close the loop.

---

## Demo

Let's stand up the voice agent on screen and watch a loop close because the interfaces were wired right.

1. **Show the five lines first.** On screen, the checklist for this agent. Perceive: microphone plus transcription. Act: speaker plus call transport. Check: did the caller's intent get resolved. Remember: conversation history. Stop: caller hangs up or goal met. Architecture before prompt, written down.

2. **Wire the actuators.** Connect the call transport, Twilio in this case, and the speaker. Place a test call from the agent to my own phone. My phone rings. That's the actuator firing, before any conversation logic exists.

3. **Wire the sensors.** Plug in the microphone feed and the transcription. I say a sentence into my phone. On screen, the transcript appears in the agent's context a beat later. The agent can now perceive.

4. **Close the loop.** Now, and only now, add a four-line prompt. The agent listens, transcribes, decides, speaks. I ask it a question on the call. It answers out loud, in real time. I interrupt with a follow-up. It adjusts mid-conversation because conversation history is in the state slot.

5. **Pull one cable.** Disconnect transcription. Run it again. The agent can still hear and still speak, but it has gone deaf to meaning. It talks over me. Same prompt, same model, broken loop. Plug transcription back in, and the conversation returns.

Total footage: about three minutes. The whole point is in step five. Nothing changed about the model or the prompt. One missing interface was the difference between a caller and a noise machine.

---

## Key Insight

> A loop that can't act in the world and can't perceive the result is a brain in a jar. Write the interface before you write the prompt. The model will paper over a missing cable with confidence, and the work will never happen.

---

## Where we go next

You now know the step that comes before the prompt. Five interfaces, written down, before a word of instruction.

Everything from here up the stack is an architecture decision before it is a prompt. Every worker loop and every discovery loop you build later starts with the same five lines. The next segment narrows in on one specific cable, the output cable, and asks what the agent should actually hand you when the loop closes.

See you in the next one.
