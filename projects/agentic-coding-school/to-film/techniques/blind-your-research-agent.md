---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Subagents"
class: "techniques"
chapter: "Subagents"
status: "scripted"
---

## Blind Your Research Agent

When you send an agent to research a codebase before you build, do not tell it what you are building. The moment it knows the goal, it stops reporting facts and starts pitching opinions.

You already know how the Explore subagent works. Read-only. It crawls the codebase, finds the relevant files, maps the architecture, comes back with a report. That is not what this video is about.

This video is about what you feed it. And more importantly, what you hide from it.

---

## The instinct that poisons the output

Here is what everyone does. You have a ticket. "Add per-seat billing to the workspace settings page." You open a research prompt and you paste the ticket straight in, because obviously the agent should know what it is working toward.

That feels like good prompting. You are giving it context. You are focusing it. More context is always better, right?

It quietly wrecks the research.

[IMAGE: a funnel with a ticket dropped into the top labeled "goal in", the funnel walls tinted red, and what drips out the bottom is a document stamped OPINIONS in red ink, arrows inside the funnel all bending toward a target icon]
![[images/blind-your-research-agent/goal-poisons-funnel.png]]

Because now every single thing the agent reads gets filtered through one question: does this help me build the billing feature? It stops describing the code. It starts auditioning solutions.

You asked how sessions resolve today. It tells you where you should hook in your new billing check. You asked what touches the workspace model. It tells you what you should refactor first.

That is not research. That is a pitch deck with line numbers.

---

## Facts versus opinions

The idea is simple, and it comes from Dexter Horthy at HumanLayer, in his talk "Everything We Got Wrong About Research-Plan-Implement" at the Coding Agents Conference this past March.

His line is the whole video in one sentence: "good research is all facts. But if you tell the model what you're building, then you get opinions."

Source: Dexter Horthy (HumanLayer), "Everything We Got Wrong About Research-Plan-Implement," Coding Agents Conference, March 2026.

[IMAGE: two document cards side by side, left card stamped OPINIONS in red and filled with checkmark-and-arrow suggestion bullets pointing at a target, right card stamped FACTS in green and filled with plain description lines and file paths, a divider down the middle]
![[images/blind-your-research-agent/facts-vs-opinions-docs.png]]

A facts-only doc tells you how the code behaves today. Where sessions get resolved. What reads the billing table. Which three modules import the workspace model. Boring. True. Reusable.

An opinions doc tells you what the agent would do. Dressed up as findings, so you cannot tell the difference until it burns you in the plan.

You want the boring one. Every time.

---

## Why the goal rewrites everything

You need to understand the mechanism, because "just tell it to stay objective" does not work, and this is why.

An LLM is a next-token predictor conditioned on its entire context. Nothing it writes is independent of what is already in the window. Put a goal in the window and that goal conditions every token that follows.

[IMAGE: a context window as a horizontal bar, a goal token glowing at the left as an attractor with a gravity well, every downstream observation token bending and sliding toward it, the well labeled "relevance to the build"]
![[images/blind-your-research-agent/goal-attractor-well.png]]

Two things happen, in order.

First, retrieval bends. When the agent decides what in the codebase is worth reading, "relevant" silently redefines itself as "relevant to shipping the feature." It over-reads the code near where the feature would live and skims everything else. Your map gets a bright spot and a lot of dark corners.

Second, generation bends. Once it has the material, the cheapest high-probability completion next to a stated goal is a recommendation. The goal puts the model in recommendation mood. "Here is where you would add it." "You should extract this." That is what text looks like near a goal in its training data, so that is what it writes.

Strip the goal out and there is nothing to be relevant to. There is no build to recommend toward. The cheapest correct completion collapses back to plain description. Facts fall out because facts are all that is left.

You are not asking the model to be disciplined. You are removing the thing it would bend toward.

---

## The two-window split

So here is the move. Do not run research in one window. Run it in two, and put a wall between them.

[IMAGE: left path a single context labeled Ticket plus Research producing a doc stamped OPINIONS in red; right path two separate contexts, the first labeled Ticket to Questions, an arrow crossing a wall labeled "goal hidden" into a second fresh context labeled Questions to Research producing a doc stamped FACTS in green]
![[images/blind-your-research-agent/two-window-split.png]]

Context A reads the ticket. Its only job is to turn the goal into research questions. "How does auth resolve sessions today?" "Trace everything that touches billing." "What is the current shape of the workspace model?" The goal goes in. Only questions come out. The intent gets left behind in window A.

Context B is a fresh Explore subagent. It has zero knowledge of what you are building. It never sees the ticket. It gets a list of questions and it answers them, blind, and it produces a facts-only research doc.

Dex calls this "query planning, but for a model reading through codebases." That is exactly it. Window A plans the queries. Window B executes them without knowing why.

[IMAGE: a wall down the middle, on the left a head labeled "you plus context A" holding a glowing lightbulb labeled "the goal, the reasoning", on the right a blindfolded robot labeled "Explore, context B" holding a magnifying glass over code, only a slip of paper labeled "questions" passing through a slot in the wall]
![[images/blind-your-research-agent/keep-thinking-outsource-facts.png]]

This is the principle "do not outsource the thinking," made concrete. You keep the goal. You keep the reasoning about what matters and why. You outsource only the fact-finding. The blindfold is not a limitation on the subagent. It is the whole point of it.

And notice what the split buys you. A single objective-flavored prompt only hopes the model resists the pull of the goal. The split makes it structural. The goal cannot leak into window B because it was never sent there. You are not trusting the model to stay clean. You made it impossible to be dirty.

---

## This is not a coding trick

The same failure shows up anywhere you send someone to gather facts with a goal in their ear.

Legal due diligence. You hand a paralegal a contract. Tell them "find why this contract is enforceable" and they come back with a tidy stack of supporting clauses. Every one real. The landmines? Not in the report. You did not ask about landmines.

[IMAGE: same stack of contract documents feeding two paralegals, the top one prompted "find why it's enforceable" outputs a short green list of supporting clauses, the bottom one prompted "list every obligation and termination trigger" outputs a longer list that includes red landmine icons, a caption reading "same documents, opposite output"]
![[images/blind-your-research-agent/paralegal-same-docs.png]]

Tell the same paralegal "summarize every obligation and every termination trigger" and the landmines surface, because now they are what you are looking for.

Same documents. Opposite output. The only variable is what you told them to look for. A goal-shaped question gives you goal-shaped answers, and goal-shaped answers are missing everything the goal did not care about.

---

## Where it goes wrong

Blinding is a strong default. It is not a law of physics. Be honest about the two ways it bites.

One. Blind research can wander. Cut the goal and you cut the focus. Lazy questions like "tell me about the auth system" send the subagent off to document everything and nothing, and you get a sprawling doc that touches the whole repo and lands nowhere useful. The quality of the blind pass is capped by the quality of your questions. Vague questions in, mush out.

Two. Some questions are genuinely goal-shaped and you cannot fully launder them. "Does the auth layer already support per-seat scoping?" leaks intent no matter how you phrase it. The subagent can smell the feature through the question.

So this is a default, not an absolute. Blind by design. Un-blind on purpose, in the narrow spots where the honest question has the goal baked in. You are choosing where the wall has a door.

---

## Demo

Let me show you the whole thing end to end.

1. **The trap.** I take a real ticket, "add per-seat billing to workspace settings," and paste it straight into a research prompt aimed at the Explore subagent. The doc comes back. I scroll it and highlight in red every line that is actually a suggestion. "You should add a `BillingGuard` middleware here." "Consider refactoring `WorkspaceService` before wiring this up." Half the doc is opinions wearing the costume of findings.

2. **The split.** New chat. Window A. I paste the same ticket, but the prompt says: emit only research questions, strip the goal, do not mention billing. Out comes a clean list. "How are workspace sessions resolved today?" "What currently reads and writes the workspace model?" "Where does the settings page get its data?" The intent stays trapped in this window.

3. **The blind pass.** Fresh Explore subagent. I give it the question list and nothing else. It has no idea a billing feature exists. It crawls, it answers, and it hands back a doc that is pure description. File paths, call chains, current behavior. No "you should" anywhere in it.

4. **The diff.** I put the two docs side by side. Left, the goal-aware version, red suggestions everywhere. Right, the goal-blind version, green facts all the way down. Then I throw the left one away and feed the clean facts doc into planning, where the opinions actually belong, because now they are my opinions built on top of solid facts.

5. **Make it repeatable.** I wrap the whole split into a slash command. One skill that runs window A to generate questions, spawns the blind Explore subagent, and returns the facts doc. Now the blinding is deterministic. It is not "please stay objective and I hope you listen." The wall is in the code path. It happens every time whether the model feels like it or not.

[IMAGE: a slash command box labeled "/research" at the top, an arrow down into a two-stage pipeline, stage one a gear turning ticket into questions, a wall, stage two a blindfolded Explore returning a green FACTS doc, the whole pipeline boxed and stamped "deterministic, every run"]
![[images/blind-your-research-agent/wrap-as-slash-command.png]]

---

### Key Insight

> Tell your research agent the goal and it returns opinions dressed as findings. Hide the goal and the only thing left to write is the truth.

---

Next time you research before you build, run it in two windows and put a wall between them.

Keep the thinking. Blind the finder.

You will get facts. And facts are the only thing worth planning on top of.
