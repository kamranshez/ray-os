---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Learning New Domains"
class: "techniques"
chapter: "Learning New Domains"
status: "scripted"
---

## Stop Asking It to Do the Thing

You keep pointing the agent at tasks inside fields you already know. That is the small unlock. The big one is pointing it at fields you know nothing about, and using it to make yourself competent in an afternoon.

Here is the thesis. When you don't know a domain, you can't write the prompt, you can't judge the output, and you can't defend the decision. So most people either avoid the work or hand it off blind and rubber-stamp whatever comes back. There is a third option. Before you ask the agent to do the thing, ask it to teach you the thing well enough to grade it.

Tariq Shihipar, who works on Claude Code at Anthropic, said the quiet part out loud at AI Engineer World's Fair 2026: "the model knows more about almost everything than I do. I just need to get it out of it."

Source: Tariq Shihipar, Anthropic, AI Engineer World's Fair 2026

That is the whole skill. The expertise is already in there. This video is about getting it out of the model and into your head, not just into the output.

---

## The Trap: You Can't Spec What You Can't Name

Think about the last time you touched a field you had no vocabulary for. Color grading a clip. A protocol you had never configured. A framework everyone else seemed to already understand.

You hit a wall that has nothing to do with the agent's ability. You could not write a good prompt, because a good prompt uses the words of the field, and you did not have them. You cannot ask a question whose vocabulary you don't own.

[IMAGE: dark chalkboard, a locked gate labeled "a real spec" with a person standing in front of it holding a sign that reads "I want it to look... better?", the gate's keyhole shaped like a word bubble full of unknown domain terms the person doesn't have]

![[images/learn-the-field-first/vocabulary-gap.png]]

So you do the natural thing. You give a vague prompt, you get a plausible result, and you approve it. Not because it is good. Because you have no basis to call it bad. That is the real danger here, and it is quiet. You are not shipping broken work. You are shipping decisions you cannot defend, in your own project, under your own name.

This is a different problem from finding your unknowns inside a codebase you own. There, you at least know the legend on the map. Here you don't even have the legend. You are not asking "what did I miss in this module." You are asking "what are this field's questions in the first place."

---

## Two Modes: Doer and Teacher

Every request you make of the agent runs in one of two modes, and almost everyone lives in the wrong one.

**Doer mode** is "build me the thing." Grade this clip. Configure this connection. Write this integration. The output is an artifact you cannot evaluate, because evaluating it needs the exact expertise you skipped.

**Teacher mode** is "make me able to judge the thing." Show me the decisions this field makes. Give me the vocabulary. Hand me the rubric a professional would grade against. The output is not an artifact. It is a promotion. You walk out able to spec the work and catch a bad result.

[IMAGE: dark chalkboard, a single box labeled "a field you don't know" with two arrows leaving it, top arrow labeled "doer mode" leading to a shiny artifact stamped with a red question mark and the caption "you can't grade it", bottom arrow labeled "teacher mode" leading to a small figure whose head now contains a checklist, then a clean arrow onward to "spec it and judge it"]

![[images/learn-the-field-first/doer-vs-teacher.png]]

The move is to spend the first pass in teacher mode. Get the field's structure into your head. Then, and only then, drop into doer mode, where you can actually tell whether the result is any good.

---

## Why the Model Can Do This

A model like Claude is roughly a hundred million people compressed into one system. Every field you have never studied is in there, taught by the people who do know it. The bottleneck was never the model's knowledge. It was your ability to interrogate it.

[IMAGE: dark chalkboard, a large cloud labeled "~100M people compressed" with faint clusters inside tagged colorist, cryptographer, tax lawyer, audio engineer, a hand reaching in and pulling one glowing cluster out along a wire into a small human head labeled "you"]

![[images/learn-the-field-first/expertise-in-the-model.png]]

Teacher mode is just a better interrogation. It converts the model's latent expertise into your working vocabulary. Once you hold the vocabulary, the same request that produced mush produces a real spec, because now you are speaking the field's language back to it.

Tariq's own example was color grading. He was editing video, hit a domain where he did not even know the vocabulary of the questions, and used the agent to hand him the map of what he needed maps for. He did not ask it to grade his footage. He asked it to make him someone who could.

---

## The Toolkit

Teacher mode is not one prompt. It is a short sequence, and each step produces something you keep.

**Map the decision structure first.** Do not ask for a lecture. Ask for the decisions. "I know nothing about color grading. Teach me the five decisions a colorist actually makes on a shot, in the order they make them, and the tradeoff inside each one." You get the skeleton of the field, which is the thing a lecture buries.

[IMAGE: dark chalkboard, a vertical numbered spine of ordered decision nodes labeled decision 1 through decision 5, each node with two small diverging arrows labeled with a tradeoff, the whole spine bracketed as "the shape of the field"]

![[images/learn-the-field-first/decision-structure.png]]

**Learn the vocabulary of the questions.** The terms are what unlock everything downstream. "What questions would a professional ask me about this shot that I don't even know to ask myself? Give me the words I would need to answer them." Now you can describe what is wrong instead of gesturing at it.

**Ground it in your actual artifact.** Do not learn in the abstract, it will not stick and it will not transfer. Hand it your real thing. "Here is a frame from my clip. Walk me through how each of those decisions applies to this exact shot, and where this shot is fighting you." Learning attached to your real footage converts straight into a spec.

[IMAGE: dark chalkboard, two streams converging into a funnel, left stream labeled "the field's general decisions", right stream labeled "your actual clip / repo / contract", output of the funnel a document labeled "guidance you can act on"]

![[images/learn-the-field-first/ground-on-artifact.png]]

**Build the evaluation rubric.** This is the step that makes the whole thing safe. "Give me a six-point checklist that separates a professional grade from an amateur one, so I can score the result myself." The output of learning is not a feeling. It is a checklist you can grade with.

[IMAGE: dark chalkboard, a doer-mode artifact passing through a gate made of a six-item checklist, some items ticked and one big red X catching the artifact, caption "the output you could not judge, now graded"]

![[images/learn-the-field-first/rubric-gate.png]]

**Quiz yourself to find the holes.** Same quiz-me move you use before a PR, pointed at the field instead of the diff. "Quiz me on why a colorist would lower the highlights here." If you cannot answer, you were reading, not learning, and now you know exactly where.

---

## The Loop

Put the steps together and it is a loop, not a checklist you run once.

You map the decisions, learn the words, ground it on your artifact, build the rubric, then spec the real task and grade the result against your own rubric. Where you get a question wrong, or where the rubric exposes something you cannot explain, you go back and learn that one piece deeper. Each pass makes you a slightly better judge of the field.

[IMAGE: dark chalkboard, a five-node cycle drawn as a loop, nodes labeled map decisions, learn vocabulary, ground on artifact, build rubric, spec and grade, with a feedback arrow from a "wrong answer / failed rubric" side-node bending back into the loop]

![[images/learn-the-field-first/learning-loop.png]]

You are not trying to become a professional colorist. You are trying to become someone who can spec the grade and catch a bad one. Learn to the decision, not to completeness. The moment you can write the spec and grade the output, stop.

---

## Where It Bites You

Three honest failure modes, because a naive version of this is worse than not doing it.

**The confident teacher.** In a real field with references, docs, your actual footage, a public spec, the model teaches you a grounded, correct version. In a thin niche with no signal, it will teach you a plausible, confident, wrong curriculum with the same tone. Cross-check the load-bearing claims against a real source before you build your rubric on them.

**Learning theater.** Reading a clean explanation feels exactly like learning. It is not. The tell is whether you can produce the rubric and pass your own quiz. If you skip those two steps, you did not learn the field, you watched a video about it. Force the artifacts.

**Over-learning.** You do not need a PhD to grade one clip. It is easy to disappear into a fascinating field and never ship. The rubric is your exit condition. Once you can score the work, you are done learning and it is time to do the work.

---

## Demo

I am going to learn enough color grading to judge a shot, live, starting from zero.

1. **Start blind.** Take a real clip from my footage that looks flat and slightly wrong, and I cannot say why. Prompt Claude: "I know nothing about color grading. Teach me the decisions a colorist makes on a shot like this, in order, with the tradeoff in each." Put the decision map on screen.

2. **Pull the vocabulary.** Ask: "What are the terms I would need to describe what is wrong with this shot?" Watch white balance, lift, gamma, gain, saturation versus vibrance come out. Say the words back to describe my own clip on camera.

3. **Ground it on the frame.** Paste an actual frame. "Given this exact shot, which of those decisions matter most here, and where is the shot fighting me?" Get specific, not generic.

4. **Build the rubric.** "Give me a six-point checklist that separates a pro grade from an amateur one." Read it out. That checklist is the deliverable of the whole learning pass.

5. **Spec, then grade.** Hand the real grading task to the agent. Then score the result against my own six-point rubric on camera. Land on one point where, ten minutes ago, I would have rubber-stamped a bad grade, and now I catch it.

6. **Quiz me.** "Quiz me on why we pulled the highlights down here." Answer live. Miss one. Go back into the clip and close the gap.

---

## Key Insight

> Using the agent to do a task in a field you don't know ships decisions you can't defend. Using it to teach you the field's decision structure first turns you into someone who can spec the work and grade the result. The model knows more than you about almost everything. The skill is getting it out of the model and into your head, not just into the output.

---

The next time you hit something you have no vocabulary for, do not ask the agent to do it for you. Ask it to teach you enough to judge it. Then do it.

That is how you stay in the loop, and the loop is where the value was the whole time.
