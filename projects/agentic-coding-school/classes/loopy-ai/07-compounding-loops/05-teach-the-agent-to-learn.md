---
video_id: "UCZ1tgPW"
duration: "12-16 min"
batch: 6
order: 21
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "Teach the Agent How to Learn"
aliases: [teach-the-agent-to-learn]
---

You built the self-improvement loop. The inner loop does the work, the outer loop reads the corrections and edits the skill. You wire it up, you feed it a week of feedback, and it does get better. Then it gets worse.

Here is why. Feedback is not learning unless the agent can generalize.
Source: https://x.com/petradonka/status/2054897826149101588

An outer loop that writes down what happened is not learning. It is transcription. Learning is when a single correction changes how the agent handles a hundred situations you never mentioned. That jump, from one case to the general pattern, is the whole game. And it is the one thing the model will not do on its own. Left alone, it does the opposite.

This segment is about the skill that makes the jump happen.

---

## The one failure mode

There is exactly one way a naive self-improver breaks, and it breaks this way every time.

You give it a correction. It turns the correction into a rule.

A reply went out sounding too markety. You tell it so. It reaches for the most literal possible fix and writes a new line into the skill: "never mention pricing in the first sentence." Done. Filed. It feels like progress, because something changed and the change points at the thing you complained about.

But that was never the lesson. The lesson was about reading the room. The person was venting, and the agent answered a frustrated human with a pitch. The transferable version is "if someone is venting, lead with empathy, not a pitch." That principle covers pricing in the first sentence. It also covers the feature comparison in the second sentence, the roadmap link in the third, and the cheerful "have you tried" that lands like a slap on someone who is already angry. One principle, a hundred cases.

The rule covers one.

[IMAGE: dark canvas, a single feedback note "too markety" at the top fanning into two diverging paths. Left path collapses to a narrow brick labeled "RULE: never mention pricing in sentence one" covering one tiny dot, red X. Right path opens into a wide principle labeled "if someone is venting, lead with empathy" spreading over many dots, green check. Caption: "same correction, two generalizations".]
![[loopy-teach-the-agent-to-learn-rule-vs-principle-1.png]]
![[loopy-teach-the-agent-to-learn-rule-vs-principle-2.png]]
![[loopy-teach-the-agent-to-learn-rule-vs-principle-3.png]]
![[loopy-teach-the-agent-to-learn-rule-vs-principle-4.png]]
![[loopy-teach-the-agent-to-learn-rule-vs-principle-5.png]]

Now run that forward a month. Every correction becomes another rule. The skill file does not get smarter, it gets longer. It turns into a decision tree, and a decision tree is brittle by construction. Each branch only fires on the exact situation that spawned it. The first time reality shows up wearing a slightly different outfit, none of the branches match, and the agent is back to guessing, except now it is guessing while dragging two hundred dead rules behind it.

That is the trap. Agents need to learn how to learn, or feedback turns into brittle exceptions.
Source: https://x.com/petradonka/status/2054897826149101588

The outer loop did its job. It read the feedback and it edited the file. The job was just the wrong job.

---

## Why the model won't fix this for you

You might expect a strong model to round the corner on its own. Give it the correction and the context, and surely it generalizes.

It does not, reliably, for judgment work. Generalizing from one correction means deciding which details were incidental and which were the point. That is a taste call, and taste is the thing the model is missing, which is the entire reason you are running a human-in-the-loop self-improvement system in the first place. (See [[self-improvement-loop]] for why judgment work has no cheap grader.) Asked to "update your instructions based on this feedback," the model takes the safe, literal path. It quotes the symptom back at you as a rule. It looks obedient and it is useless.

So you do not ask the model to learn. You give it a skill whose only job is learning, and that skill carries the taste the base model lacks.

---

## The fix: a skill that only learns

Split the work. The inner loop drafts. The outer loop, when it sees a correction, does not edit the skill directly. It hands the correction to a separate skill whose single responsibility is turning feedback into a principle.

That learning skill gets three inputs, and it needs all three:

- What the agent suggested.
- What the human actually did instead.
- The current instructions the agent was working from.

The gap between the first two is the signal. The third is so it can place the lesson correctly instead of bolting on a redundant one. This is the rules-versus-principles technique from [[principles-over-rules]], turned into a procedure and run inside a loop.

[IMAGE: dark canvas, three labeled streams converging into a single funnel labeled "learning skill". Streams: "agent's suggestion", "what the human did", "current instructions". Out of the funnel comes one clean card labeled "principle". Caption: "the learning skill needs all three inputs".]
![[loopy-teach-the-agent-to-learn-three-inputs-1.png]]
![[loopy-teach-the-agent-to-learn-three-inputs-2.png]]
![[loopy-teach-the-agent-to-learn-three-inputs-3.png]]
![[loopy-teach-the-agent-to-learn-three-inputs-4.png]]
![[loopy-teach-the-agent-to-learn-three-inputs-5.png]]

The skill runs a fixed procedure, and the procedure is the part that does the generalizing.

**Identify what went wrong.** Start from the specific feedback. Be concrete. "The reply was too markety" beats "the tone was off." You cannot generalize from a blur.

**Ask why.** The feedback is a symptom. Find the cause underneath it. Too markety because it pitched at someone who was complaining. The cause is the lesson, the symptom is just where the lesson surfaced.

**Zoom out to the pattern.** Would this apply beyond this one case? If the only situation it ever helps is this exact thread, it is a rule and you should be suspicious of it. If it changes how the agent reads a whole class of moments, it is a principle.

**Check it against the existing principles.** This is the step everyone skips, and skipping it is how the file balloons. The right move is often not "add." It is sharpen an existing principle, edit one that was almost right, or delete two that this one now subsumes. Adding is the last resort, not the default.

**Write it as a principle, not a rule.** Describe how to think, not what to do.
Source: https://x.com/petradonka/status/2054897826149101588
"Lead with empathy when someone is venting" tells the agent how to reason. "Never mention pricing in sentence one" tells it what to type. The first transfers. The second does not.

**Put it where it belongs.** Section matters. A principle filed under the wrong heading is a principle the agent will not reach for when it counts. Placement is part of the instruction.

**Edit and commit.** Keep the file tight. Merge overlapping principles as you go. A learning skill that only ever grows the file is the decision tree again with extra steps.

[IMAGE: dark canvas, a horizontal pipeline of seven linked nodes left to right: "identify" then "why" then "zoom to pattern" then "check existing" then "write as principle" then "place" then "commit". Above the chain, a small thought bubble at "check existing" branches into four tiny verbs: sharpen, edit, delete, add. Caption: "the learning procedure, where adding is the last option".]
![[loopy-teach-the-agent-to-learn-procedure-1.png]]
![[loopy-teach-the-agent-to-learn-procedure-2.png]]
![[loopy-teach-the-agent-to-learn-procedure-3.png]]
![[loopy-teach-the-agent-to-learn-procedure-4.png]]
![[loopy-teach-the-agent-to-learn-procedure-5.png]]

Notice what this procedure is. It is the curator role from [[ace-three-role-split]], pulled out and made explicit. ACE gave you the formal three-role shape. This is the curator written down as a skill you can read, version, and correct when it gets the generalization wrong.

And it is not hypothetical. The seven steps above are a real, shipped skill. Warp open-sourced the exact `reply-learning` skill that maintains their community-reply agent, and it is this procedure written as a `SKILL.md` you can read top to bottom.
Source: https://gist.github.com/petradonka/873e54b6464b36dc2720eee039071cfa

Two things in it are worth stealing on top of the core steps. It carries a sharp test for the zoom-out step, the call between a pattern and a rule: can you name three or more different situations where this principle would change behavior? Three or more, it is a pattern worth codifying. Fewer, it is a rule wearing a principle's clothes. And it closes on an explicit length budget, the skill stays under about two hundred lines, which forces the learning loop to merge and sharpen instead of only ever appending. A budget is what turns "check against the existing principles" from advice into a constraint the loop has to satisfy.

---

## You are teaching, not configuring

Here is the shift in how this feels once you are doing it.

It does not feel like editing a config file. It feels like teaching a new hire. You watch them make a call, you tell them what you would have done, and the good ones do not just patch that one case. They ask why, and they walk away with a way of thinking that handles the next ten situations you will never get to spell out.

The learning skill is you trying to produce that second kind of teammate on purpose.

And there is a side effect worth the price of admission on its own. To teach the agent, you have to say the quiet part out loud. A lot of taste lives implicitly in people's heads. Nobody on the team ever wrote down "lead with empathy when someone is venting," because everyone good just does it. The moment you have to encode it so an agent can apply it, you drag it onto the page. Your team ends up with a written, reviewable account of its own judgment, which it never had before. The agent is the excuse. The artifact is the real win.

---

## Demo

One correction, run through the skill twice. First the naive way, then the right way, side by side.

1. **Set the scene.** Show the inner loop's drafted reply to an annoyed user, and the human's actual reply, which dropped the pitch and led with "yeah, that is genuinely frustrating, here is what is going on." Show the current skill file open beside them.

2. **The naive path.** Prompt a plain agent: "update the skill based on this feedback." Watch it append "never mention pricing in the first sentence." Point at the diff. One line, one case, file got longer.

3. **The learning skill path.** Run the actual learning skill on the identical inputs. Walk the procedure on screen: it names the symptom, asks why, lands on "the agent pitched to someone who was venting," checks the existing principles, finds the tone section, and proposes the principle there instead of a new rule at the bottom.

4. **Compare the diffs.** Naive diff: plus one brittle rule. Learning diff: one sharpened principle, and it actually deleted an older overlapping line. The file got shorter and stronger.

5. **Prove the transfer.** Feed both versions a brand new angry thread that has nothing to do with pricing. The rule version pitches anyway, because no rule matched. The principle version leads with empathy. Same skill file size budget, completely different behavior.

The point of the demo is that the inputs were identical. The only variable was whether a skill did the generalizing.

---

## Key Insight

> An outer loop that turns every correction into a rule is not learning, it is growing a decision tree. Learning is a separate skill whose only job is to ask why, find the pattern, and write a principle instead.

---

## Where we go next

The learning skill closes the gap between feedback and generalization. But it still proposes a change to a file that drives real behavior, and you do not let it merge that change on its own authority.

The principle it writes is a suggestion until a human signs off. Next segment, [[skills-as-code]], we put that gate in place: every edit the loop proposes arrives as a reviewed diff, with history and rollback, so the agent can keep teaching itself without ever quietly going off the rails.

See you in the next one.
