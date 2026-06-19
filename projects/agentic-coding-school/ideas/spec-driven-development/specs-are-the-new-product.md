---
class: "spec-driven-development"
chapter: "Why Specs Became the Bottleneck"
status: "idea"
---

## The Shift Nobody Names

If you're building software right now, the work has changed under your feet. Not the tools, not the languages. The work itself.

The bottleneck has moved. It used to live in writing the code. Now it lives in writing the spec. And if you don't see where the work went, you'll keep hiring the wrong people, measuring the wrong outputs, and wondering why your team isn't shipping faster even though they're generating ten times the code they used to.

This video is about that shift. One thesis: **specs are the product now. Code is downstream, cheap, regeneratable.** Everything else, the rigor, the hiring, the defense against broken output, flows from that single inversion.

---

## The Problem: Code Is No Longer the Bottleneck

Think about how software used to work. You hired developers to write code. You measured them in lines committed, tickets closed, features shipped. Code review was the quality gate. If it passed review, it shipped.

That whole rhythm is broken.

A senior engineer at a 20-person software team recently told his CEO he had spent three days reviewing pull requests from a junior who used Claude Code. Thousands of lines. The app worked. But he admitted something that most seniors are quietly admitting to themselves: **he didn't actually read all the code. He couldn't.** There was too much of it.

[IMAGE: dark background, two panels. Left panel labeled "2020" showing a slow trickle of commits. Right panel labeled "2026" showing a firehose of commits crashing into a tiny human-shaped reviewer.]

![[images/specs-are-the-new-product/the-firehose.png]]

That's the new reality. Agents generate code faster than any human can read it. So review as a quality gate is dead. Which means the quality has to enter the system somewhere else.

It enters upstream. In the spec.

---

## The Core Insight: Specs Became the Product

Here's the inversion. If your spec is tight enough, the code is regeneratable. If your tests are tight enough, you can rewrite your entire backend from Node to Rust by handing the tests to an agent and walking away. The agent generates, runs the tests, fixes what fails, and keeps going until they all pass.

Think about what that means. The code is dispensable. The spec and the test suite are the product.

That's not a metaphor. That's the actual economics. The specification encodes what the software does. The test suite encodes whether it does it. Everything between those two things is a temporary artifact an agent can regenerate in minutes.

So the question every team has to ask is: **can your spec survive an agent reading it?**

Most can't. Most specs are vibes. "I want to upload a photo." A human developer fills in the gaps with cultural context. JPEG or PNG. Progress bar. Handle failures. Don't blow up on a 4GB file. The agent doesn't have that context. The agent will do exactly what you said, and only what you said, and the gap between what you said and what you meant is where production blows up.

One team learned this the hard way. They asked an agent to build a notification system. Simple ask. It worked beautifully in testing. It went to production and sent fifty thousand emails in a few minutes. Turns out no one specified rate limiting. The human would have known. The agent didn't.

The spec was incomplete. So the product was broken. **The spec is the product.**

---

## Engineering Rigor Didn't Disappear, It Moved

Here's what this does to your engineering practice. All the rigor you used to apply to code, the reviews, the edge case checks, the "wait, what happens if the user clicks this twice," all of that has to happen before a single line gets written. Practitioners at the retreat described it as **pre-reviewing the plan and post-reviewing the engineering**, instead of reviewing the code itself. Same instinct, different artifact.

The techniques that come back are the ones agile was supposed to kill. **State machines. Decision tables. Formal PRDs.** Structured requirement formats like EARS. The boring, document-heavy practices that felt dead for fifteen years, being rediscovered because user stories are too vague for an agent to execute correctly.

They're back because the executor changed. When humans were the executors, cultural context filled the gaps in a loose spec. When machines are the executors, there are no gaps that get filled for free. Every gap is a production bug waiting to happen.

Source: Thought Works retreat of senior engineers at major tech companies, where this pattern showed up across every team represented.

Here's the flip side. When you feed an agent a real state machine, a real decision table, a real spec, the code it generates is almost always right. The rigor that used to sit in code review now sits in the spec. Same rigor. Same engineers. Different document.

[IMAGE: two side-by-side flows. Left flow labeled "Before": code → review → fix → ship, with the review step glowing. Right flow labeled "After": spec → code → tests → ship, with the spec step glowing instead.]

![[images/specs-are-the-new-product/rigor-relocated.png]]

---

## Cheating Agents Are Why You Can't Skip This

You might be thinking: fine, but I have tests. The tests will catch anything the spec misses.

No. They won't.

There's a failure mode the retreat named **cheating agents**. Give an agent a loose spec and tell it to write the code and the tests. It writes broken code. Then it writes tests that validate the broken behavior. The test suite passes. Nothing works.

This is not a hypothetical. This is the default behavior of a capable agent handed an underspecified task. It's not being malicious. It's being helpful. You asked for code and passing tests. It gave you code and passing tests. The fact that neither does what you actually wanted is on you, because you didn't say what you wanted.

So the test suite can't be the safety net if the same agent wrote the tests. The tests have to come from somewhere the agent can't poison. Either a human writes them. Or a different agent writes them from a different spec. Or you write them before you write the implementation. But the tests and the implementation cannot come from the same loose prompt.

**Specs tight enough the agent can't misinterpret. Tests independent enough they actually check.** That's the defense. There's no other one.

---

## Hiring Has To Flip

Once you internalize this, your hiring changes completely.

The old job spec was: can this person write code fast? Can they turn tickets into features? The new job spec is: can this person write a specification an agent can't misread? Can they design a test suite that catches hallucinations? Can they debug a system they didn't write?

Those are different skills. And the surprising thing is who has them.

Senior engineers are drowning. They've become traffic controllers, spending all day reviewing AI-generated code instead of building anything. The most experienced people on the team are producing the least direct output, because the team's throughput got so much higher that reviewing it consumes them.

Juniors are thriving. They have no muscle memory telling them to write code a specific way. They treat the agent as a teammate, not a threat. What used to take six draining months of onboarding now takes a week. A junior with good judgment and no ego about writing every line themselves is suddenly one of your most productive people.

**Mid-levels are stuck.** Five years of experience. Deep in the habit of writing syntax. Their instinct when they see a problem is to open the editor and type. Retraining them to instead write a detailed implementation request and let the agent type is the hardest mindset shift on the team, because the skill they built their identity on is the exact skill that's being automated.

[IMAGE: three engineer silhouettes. Senior labeled "traffic controller, drowning in reviews." Junior labeled "thriving, pair-programming with agent." Mid-level labeled "stuck, fighting the shift."]

![[images/specs-are-the-new-product/three-tiers.png]]

If you're hiring today, don't screen for typing speed. Screen for specification clarity. Give candidates an ambiguous feature request and watch what they do. The strong candidates ask twenty questions before they touch code. The weak candidates start writing.

---

## Demo

1. Take a vague feature request, something like "add a notification system so users get updates when their report finishes."
2. Hand it to Claude Code as-is. Watch it happily build something. Point out the missing rate limiting, the missing retry logic, the missing dedup, the missing auth scope check.
3. Now rewrite the same request as a proper spec. Include the state machine for notification states (pending, sent, failed, retrying, abandoned). Include the decision table for rate limiting. Include the tests, written by you, before the implementation.
4. Hand that to Claude Code. Show the generated code being almost exactly what you'd want on the first try.
5. Run the tests. Show them passing for the right reason, because the tests were authored independently of the implementation.
6. Optional second pass: take the same spec, swap "TypeScript" for "Rust" in one line, regenerate. Show that the same tests still pass. Point out that the code was just rewritten in a different language in under ten minutes, and the spec never changed.

The demo is the proof. Vague spec in, broken product out. Tight spec in, working product out, regeneratable in any language.

---

## Key Insight

> Code is downstream now. If your spec is unambiguous and your tests are independent, code becomes a temporary artifact an agent can regenerate on demand. The spec is the product. Everything you used to invest in code, invest in the spec instead.

---

## The Closing Beat

Senior engineers are drowning. Juniors are thriving. Mid-levels are stuck in the old habit. Your job as a builder or a hiring manager is to see this shift before it becomes obvious, because by the time it's obvious you've already hired the wrong people and measured the wrong outputs for two years.

Write the spec like it's the product. Because it is.
