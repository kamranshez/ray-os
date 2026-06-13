---
duration: "10-14 min"
batch: 6
order: 21
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Teacher Learner Pattern"
aliases: [teacher-learner-pattern]
---

Dump all your raw teaching material into one Claude session and say "structure this into a syllabus," and you get something slightly better than what you'd write yourself. Not significantly better. Slightly.

Then you put it in front of a real student and the gaps are everywhere. Lesson four needs a concept that doesn't show up until lesson six. A word gets used three times before it's ever defined. One lesson is secretly three lessons in a trench coat.

The model could not see any of this. Not because it's weak. Because it's loaded with the same context you are. It can't tell what doesn't make sense to someone who isn't already holding the whole picture in their head.

This segment is the fix. It's a role split, like the ACE three-role split we just built, but the engine isn't argument. It's missing information. On purpose.

---

## Why one fat context window fails here

The last segment, the ACE three-role split, gave you a Generator, a Reflector, and a Curator. The Reflector was the attacker from segment seven, run across a window of attempts. Its power came from being adversarial: default to refuted, hunt for the flaw.

That's the right tool when the question is "is this wrong?"

It's the wrong tool when the question is "can someone who isn't me follow this?"

Those are different failures. A syllabus can be completely correct and completely unfollowable. Every fact accurate, every lesson true, and still impossible to learn from, because the order is wrong, the prerequisites are buried, and the jargon arrives before its definition. An attacker pointed at that syllabus finds nothing. There's nothing to refute. Everything is true.

The thing you actually need is not a skeptic. It's a stranger.

[IMAGE: dark canvas, left side a single big head labeled "one context, all the material" producing a syllabus with a green check but a confused student underneath; right side two heads, one labeled "teacher (full material)" and one labeled "learner (no material)", producing a syllabus a student can actually read]
![[loopy-teacher-learner-pattern-one-context-vs-split-1.png]]
![[loopy-teacher-learner-pattern-one-context-vs-split-2.png]]
![[loopy-teacher-learner-pattern-one-context-vs-split-3.png]]
![[loopy-teacher-learner-pattern-one-context-vs-split-4.png]]
![[loopy-teacher-learner-pattern-one-context-vs-split-5.png]]

Every "review my plan" prompt fails for the same reason this does. You ask the reviewer to check your work, and you hand it all the context you have. Of course it understands the plan. It's reading the plan with your eyes. The whole value of a real reviewer is the context they're missing. Strip that out and you've just built a mirror.

---

## The core move: split the role by information, not by attitude

One agent is the teacher. It has all the material loaded. The full source, your notes, the transcripts, the half-finished drafts. Everything.

One agent is the learner. It is given a defined background and nothing else. "You're a junior developer who's used ChatGPT for autocomplete but has never built an agent. You don't know what a context window is. You've never heard the word verifier."

Then the teacher tries to explain the syllabus to the learner, and the learner pushes back wherever it doesn't land.

"I don't understand why lesson four comes before lesson six."

"You used the word idempotent and never said what it means."

"This feels like three lessons crammed into one. I got lost halfway."

The teacher adds, splits, reorders. The learner reacts again. You stop when the learner stops finding gaps.

What comes out the other end is a syllabus a real student can follow. That is a qualitatively different artifact than the single-context version, on the same starting material, with the same strong prompting. The difference isn't a better model. It's that one of the two agents was deliberately kept ignorant.

This is the load-bearing idea of the whole segment, so say it plainly. The asymmetry is not a bug you're tolerating. The asymmetry is the entire mechanism. The learner must not see the source material. The moment it does, it understands everything, finds no gaps, and you're back to the mirror.

---

## Asymmetric information, not adversarial debate

It's worth being precise about how this differs from the patterns next to it in the class, because they look similar and they are not.

The attacker from segment seven is two agents with the same information and opposite jobs. Same context, one builds, one refutes. The value comes from the opposite job.

The teacher and learner are two agents with the same job, find the gaps, and different information. The value comes from the gap in what they know.

Same family, multi-agent role split. Different engine. One runs on attitude. This one runs on what each agent is allowed to see.

That's why this earns its own segment instead of being a footnote on the attacker. You cannot manufacture this asymmetry with a sharper prompt to a single agent. You can tell one Claude "now pretend you don't know what a context window is," but it does know, and the knowledge bleeds through. It will flag the obvious omissions and sail straight past the ones that only trip someone who genuinely lacks the concept. The ignorance has to be structural. The learner has to be a separate agent that was never handed the material in the first place.

[IMAGE: dark canvas, two side-by-side loops. Left labeled "attacker pair": two heads same docs, arrows labeled "build" and "refute". Right labeled "teacher / learner": two heads, one holding a stack of docs, one holding nothing, arrows labeled "explain" and "where did I get lost?"]
![[loopy-teacher-learner-pattern-attacker-vs-teacher-learner-1.png]]
![[loopy-teacher-learner-pattern-attacker-vs-teacher-learner-2.png]]
![[loopy-teacher-learner-pattern-attacker-vs-teacher-learner-3.png]]
![[loopy-teacher-learner-pattern-attacker-vs-teacher-learner-4.png]]
![[loopy-teacher-learner-pattern-attacker-vs-teacher-learner-5.png]]

---

## Briefing the learner is the whole job

Persona quality drives output quality. A vague learner gives vague pushback. A sharp learner finds the real holes.

Three things go in the brief.

Background. Who is this person and what do they already know. Be specific about the ceiling. "Junior dev, comfortable with Python, has shipped a CRUD app, has never written an async function, has never touched an LLM API." That ceiling is what defines which gaps are real. A concept above the ceiling is a gap. A concept below it is assumed knowledge and the learner won't waste pushback on it.

What they care about. The learner reads as the target audience, so it should weight what that audience weights. A junior dev cares whether they can actually run the thing on Monday. A skeptical buyer cares whether the claim is true. Tell it.

What confuses them. The failure modes of this exact persona. "You get lost when three new terms arrive in one paragraph. You give up when a step says 'configure your environment' without saying how."

And then the one instruction that matters most, because without it the whole pattern quietly dies.

Tell the learner to push back hard. Default to "I don't get it." Models are agreeable by nature. A learner left to its own temperament will nod along, say "this is really clear and helpful," and hand you back the same broken syllabus with a gold star on it. That is the dominant failure mode of this pattern, and it's the same agreeableness failure we've hit since the closing-the-loop segment: fresh context buys honesty, but a polite agent will still rubber-stamp. So you make refusal the default. "Assume you are confused. Make me prove each lesson is followable. If you can imagine getting lost, say where." An over-agreeable learner is useless. A learner that errs toward "explain that again" is doing its job.

---

## Where this transfers

The syllabus is the demo, but the shape is a template, and most of it has nothing to do with code. That's deliberate. Most of this class hunts bugs and refactors and audits security. This one structures content, because the architecture transfers to anyone who has to make something land with an audience that doesn't share their context.

One agent holds the full material. Another gets a defined persona with deliberately less context, framed as the target audience. They iterate: the loaded agent proposes, the unloaded agent reacts as the persona would, the loaded agent revises. Stop when the persona stops finding gaps.

Docs review. Writer plus "a new hire reading this on day one with no tribal knowledge."

Product copy. Marketer plus "a skeptical user who landed here from an ad and has fifteen seconds."

Explainer scripts, which is literally what you're watching. Expert plus "a viewer who clicked from a thumbnail and will leave the moment they're lost."

API design. Designer plus "a developer with five minutes to integrate and no patience for your internal model."

Onboarding flows. Founder plus "someone who has never seen the product and doesn't care yet."

The tell, every time, is the same: you are about to ship something to people who don't have your context, and you are the worst possible judge of whether it lands, because you can't unknow what you know.

And know when to skip it. A short flat list with no sequencing doesn't need a learner. Well-trodden territory the model has seen a thousand times doesn't need a learner. The pattern pays off precisely when there's sequencing, prerequisites, or audience-fit to get right. If reordering the pieces can't break it, one context window is fine. Don't pay for two.

---

## Demo

Live syllabus restructure, on a real artifact, so you watch it get better in real time.

1. Start with the raw material for one of my own classes, the prompt-engineering one. Dump everything into a single session: notes, transcripts, the rough lesson list. Ask it plainly, "structure this into a teachable syllabus." Save that output. Read out the lesson order on screen. It looks reasonable. That's the trap.

2. Open two agents side by side. Agent one, the teacher, gets the full material. Agent two, the learner, gets one paragraph: junior dev, used ChatGPT, never built an agent, doesn't know the vocabulary, and the hard instruction, default to "I don't get it," make me prove every lesson is followable.

3. The teacher explains the syllabus lesson by lesson to the learner. Show the learner's first pass of pushback on screen. It catches three things the single context missed: a term used two lessons before it's defined, two lessons that should swap because the second one is a prerequisite for the first, and one lesson that's secretly three.

4. The teacher revises. New order, a definition lesson inserted, the bloated lesson split. Run the learner again. This pass it finds one smaller gap. Revise. Run a third pass. The learner stops finding gaps and says, in effect, "I could follow this." That's the exit condition. Not a score. The persona running out of confusion.

5. Put the two syllabi side by side. Single-context version, left. Teacher-learner version, right. Same source material, same model. The right one has a different lesson order, a definitions lesson the left one never thought to add, and no orphaned jargon. Point at the diff. That gap is the whole segment.

Total demo: six minutes. The point is that you can watch a real artifact get followable, not just correct, and the only thing you changed was keeping one agent in the dark.

---

## Key Insight

> The attacker is two agents with the same context and opposite jobs. The teacher and learner are two agents with the same job and opposite context. The thing you're missing is what makes a reviewer worth having, so build an agent that's missing it on purpose.

---

## Where we go next

You now have two role splits in hand. The adversarial one for "is this wrong," and the asymmetric one for "can anyone but me follow this."

Next we point a role split at a messy, real, recurring stream: incoming bugs. The bug triage loop takes everything from these last few segments and aims it at the queue that never empties.

See you in the next one.
