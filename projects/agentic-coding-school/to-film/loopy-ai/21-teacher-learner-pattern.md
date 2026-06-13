---
duration: "10-14 min"
batch: 6
order: 21
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Teacher Learner Pattern"
aliases: [teacher-learner-pattern]
status: stub
---

# Teacher / Learner Pattern

A non-coding example to show that multi-agent isn't just a programming trick — asymmetric role pairs beat a single fat context window for a whole class of structuring problems.

## Thesis

If you dump all your raw teaching material into one Claude session and say "help me structure this into a syllabus," you get something slightly better than what you'd write yourself. It's not significantly better. And if you then test it on an actual student, the gaps are obvious — the model can't tell what doesn't make sense to someone who isn't already loaded with the same context.

The fix is to split the role. One agent is the **teacher**: it has all the material loaded. One agent is the **learner**: it's given a defined background (e.g. "you're a junior dev who's used ChatGPT but never built an agent"). The teacher tries to explain the syllabus to the learner. The learner pushes back where things don't land — "I don't understand why lesson 4 comes before lesson 6," "you've used the word X without ever defining it," "this feels like three lessons crammed into one." The teacher then adds, splits, or reorders lessons.

You get a syllabus a real student can actually follow. That's a qualitatively different output than what a single context window produces, even with strong prompting.

## Why this works (and is worth its own video)

- **Asymmetric information beats symmetric debate.** This isn't two skeptics arguing (the debate pattern from [[agent-teams-with-debate]]). It's two roles with *different* information loads. The learner *should not* see the source material — that's the whole point. The asymmetry is the value.
- **The learner simulates the user.** Most "review my plan" prompts fail because the reviewer has all the same context as the writer. Stripping context out of one agent is what makes its pushback useful.
- **Non-coding showcase.** Most demos in this class are bug hunting, refactoring, security audits. This one is content structuring — a chance to show students who aren't full-time engineers that the architecture transfers.

## The pattern, generalised

- One agent holds the full material / source of truth.
- Another agent is given a defined persona with *deliberately less* context, framed as the target audience.
- They iterate in turns: the loaded agent proposes, the unloaded agent reacts as the persona would, the loaded agent revises.
- Stop when the persona stops finding gaps.

Other places it transfers: docs review (writer + "new hire reading this on day 1"), product copy (marketer + "skeptical user who landed here from an ad"), explainer scripts (expert + "viewer who clicked from a thumbnail"), API design (designer + "consumer with five minutes to integrate").

## Suggested placement

New example/lesson in this class, sibling to [[agent-teams-with-debate]]. Frame as "the debate pattern's quieter cousin — same family (multi-agent role-split), different mechanism (asymmetric information, not adversarial argument)."

Also worth a callback from [[ace-three-role-split]] in the loopy-ai class — the Generator/Reflector split there is a more formal version of the same shape.

## TODO

- Decide demo: live syllabus restructure for one of Ray's own classes (e.g. prompt-engineering) makes the strongest demo — students see a real artifact get better in real time.
- Show side-by-side: single-context "improve this syllabus" output vs. teacher/learner output, on the same starting material.
- Cover: how to brief the learner persona (background, what they care about, what confuses them). Persona quality drives output quality.
- Cover: when this is overkill (short flat lists, well-trodden territory) vs. when it pays off (anything with sequencing, prerequisites, or audience-fit decisions).
- Cover: failure mode where the learner is too agreeable — needs an explicit "push back hard, default to 'I don't get it'" instruction.
