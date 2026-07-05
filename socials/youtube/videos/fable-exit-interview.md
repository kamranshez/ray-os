---
tags: [youtube, script, claude-code, fable]
status: outline
date: 2026-07-05
---

## Working title options

1. Bold claim + anthropomorphism: **Your Smartest Model Is Quitting. Interview It First.**
2. Bold claim + specificity: **Run These 6 Prompts Before Fable Leaves the $200 Plan**
3. Curiosity gap + exclusivity: **What I'm Making Fable Do Before Anthropic Takes It Away**
4. Loss-framing (pattern behind the wave's 259k outlier): **Fable Leaves July 7. Skip This and Your Next 6 Months Run Worse.**

> Competitive context (2026-07-05 nine-video sweep): 7 of 9 rival videos already run countdown titles and the same "extract value before July 7" hook, and at least six teach the same "Fable plans, cheap models execute" core. Differentiation lives in (a) the exit-interview frame, (b) the retrospective targeting how Ray works with Opus specifically, (c) the self-refining routing twist, and (d) the gap nobody filled: proving a Fable-authored reference actually improves Opus's output. Chase AI's 259k outlier won on loss-framing plus demos that produce artifacts viewers want, not abstract capability tests: every demo here should end with a named artifact on screen.

> Coined term this video plants: **the exit interview**. Fable is a genius employee working their notice period. Before they walk out you extract what only they know, ask their honest opinion of how you work, and have them write the handover pack their cheaper replacement will follow.
>
> Format: deadline/news hook (Ray's explicit call, accepting the news-format ceiling risk), two sections, quitters first, 16-22 min target (~18 min).
> Pitch system: masterclass only. July 4th sale ends July 6, price placeholder `[PRICE]`. No newsletter pitch, no free artifact.
> Demo surface: course funnel repo (playbook rule 1; also satisfies "a real product repo").
> Absorbs the unrecorded `to-upload/five-jobs-for-your-best-model.md` draft (golden reference, routing map, blast radius, harness-beats-model). That file should come out of the upload queue once this ships; leaving it in place until Ray confirms.
> Thumbnail direction (complementary, not redundant with title): Ray + a glowing "employee badge" being handed over a desk, or a resignation letter labeled FABLE. Closed-mouth smirk. Do not repeat the title words on the thumbnail.

---

## Hook (0:00 - 0:30)

Discovery framing, never announcement framing. Spoken opening beat:

"On July 7th, Fable disappears from the $200 plan. Which means right now, the smartest model I have ever had access to is working its notice period. So this week I did what good companies do when their best engineer resigns. I ran an exit interview. I made it tell me everything it knows about my codebase that nobody else can see, I asked it what it honestly thinks about how I work with Opus, the model that stays, and I made it write the handover docs for the cheaper models that are about to replace it."

Three beats: (a) the deadline, (b) what we're doing about it, (c) the exit interview analogy that organizes the whole video.

*Visual hook in first 10 seconds: usage screen or plan page with Fable greyed out, then a literal "EXIT INTERVIEW" calendar invite with Fable as the attendee.*

---

## The problem (0:30 - 2:00)

Problem, old workaround, new solution triple:

- **Problem:** whether you plan to keep paying for Fable at API prices or never touch it again, everyone with the $200 plan has the same asset right now, a few days of a genius on staff, and most people are spending it like a slightly faster Opus. Ticket in, code out. That is the waste.
- **Old workaround:** what people did when Fable first landed, point it at everything, "clean up my repo," burn the budget on work Sonnet does fine. (One line callback to the June video: "I covered where to point it when it came back. This is the opposite problem, what to make it do before it leaves.")
- **New solution:** the exit interview. A structured sequence where every prompt targets something only the departing genius can do, and everything it produces outlives its access.

Two viewer personas named explicitly here, this sets up the two sections: "If you are quitting Fable forever, the first half of this video is yours. If you are keeping it but never want to waste a token of it again, the second half is the system."

---

## Soft anchor (2:00 - 2:30)

"Quick pause. This video is sponsored by me and my Claude Code Masterclass. Over 1,500 engineers from companies you've heard of have gone through it, and a lot of them are now the best Claude Code user at their company. You're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. The July 4th sale is on right now and it ends July 6th, the price goes back up to `[PRICE]` after that. Link's below."

(Objection-handler line verbatim per playbook rule 2. Single paid CTA per rule 5.)

---

## Section 1: The exit interview (2:30 - 10:00)

Framing line: "An exit interview has three questions. What do you know that we don't. What do you think of how we work. And what should we write down before you go."

### Beat 1: What do you know that nobody else does (2:30 - 5:00) [LIVE DEMO 1]

The architectural sweep. Fable does a high-level architecture pass over the course funnel repo, but targeted, not "clean everything."

Demo shot list (pre-run the session, narrate over it, do not build live):
1. One-line git churn command: files ranked by change frequency.
2. Complexity signal (dependency count or a complexity score per file).
3. Hand both lists to Fable: "These are my hotspots by churn times complexity. Do an architectural review of the top five. I don't want point fixes, I want the structural problems a weaker model reads right past, and for each one, what it breaks downstream if left alone."
4. Show one real finding on screen and linger on it (pacing improvement 1). Ideally a cross-cutting issue that spans several files, because that is the "many steps ahead" evidence.

Talking point: this is the "generate beats edit" insight. Most repos at this point are geological layers of Opus 4.1, 4.5, 4.6, 4.8, maybe some Sonnet and GLM. Fable is the only model smart enough to see the strata and say which layer is load bearing.

### Beat 2: What do you think of how I work (5:00 - 7:30) [LIVE DEMO 2]

The work retrospective. Fable reviews Ray's actual session history and critiques the operator, not the code.

The prompt (show on screen, this is a lingering full-screen moment):

> "You have access to my full Claude Code session history. Before your access ends, give me an honest exit-interview review of how I actually work with you. Read a wide sample of recent sessions and tell me: one, where I go in circles, re-explain the same context, or make the same correction twice. Two, which of my habits waste the most of your capability. Three, what should be encoded into skills, CLAUDE.md rules, or hooks so your replacement doesn't need re-teaching. Four, the three highest-leverage changes to how I prompt and delegate. Be blunt. Rank everything by output-per-hour improvement, and end with the specific artifacts you would create."

Practical caveat to mention: raw session logs are long and noisy. Have a cheap model distill them into a digest first, then point Fable at the digest, never the raw pile.

Demo: show 2-3 real findings from Ray's own history. The more embarrassing the finding, the better the retention. Each finding should end as an artifact: a skill, a CLAUDE.md line, a hook.

### Beat 3: What deserves your brain (7:30 - 8:30) [talked over, no demo]

The Mythos-worthiness ranking. Before it goes, have Fable walk the codebase and rank which files and problems genuinely need frontier intelligence versus what Sonnet or Haiku handles.

One-line callback to the June video's Impact times Opportunity machine, then the new part: the output is a routing table, and that table is the first page of the handover pack. This beat is the hinge into section 2.

### Beat 4: The meta-prompts (8:30 - 10:00) [talked over]

Credit Daniel Miessler by name, two cherry-picked prompts from his "10 prompts" post (link in description):

1. **Goal orientation:** "Look at my whole harness and characterize what I'm ultimately trying to accomplish, then find every part of the system working against that goal." Pairs with the retrospective demo, same theme, wider aperture.
2. **The bitter-lesson audit:** "Study Sutton's Bitter Lesson, then find every place my harness is overengineered around today's model limitations and give me a plan to make it flexible to future model improvements." The thematically perfect one, this video literally exists because models rotate.

Framing: "These are questions about your system, not your code. Cheap models answer them politely. Fable answers them correctly."

---

## Section 2: The handover pack (10:00 - 15:30)

Framing line: "When a great engineer leaves, they don't just hand over knowledge. They set up the team that stays. Everything in this half is Fable configuring its own replacements, and it works exactly the same if you keep Fable and just want to stop wasting it."

### Beat 5: The routing rule (10:00 - 11:30)

Judgement-based delegation, credit Theo (@theo). His one-liner: "For all coding tasks, use your judgement to decide an appropriate lower-power model and run that in a subagent." Show his CLAUDE.md ranking table on screen (cost, intelligence, taste per model).

Then Ray's twist, the self-refining loop: after each subagent finishes, Fable grades the result against what it would have done, and updates its own routing notes. The routing table is not static config, it is a judgement that gets sharper every session. "You're not writing rules for Fable. You're letting Fable learn its own management style."

### Beat 6: The golden reference (11:30 - 13:00)

Models generate better than they edit, and cheap models match patterns better than they exercise judgement. So spend one expensive run making Fable build the canonical implementation, the reference endpoint, the reference component, the module that does everything right. Then cheap models get one instruction: "make the other forty look like this one." Open-ended judgement converted into closed-ended matching, spent once, copied forever.

### Beat 7: The review gate (13:00 - 14:00)

High blast radius work gets reviewed by Fable before merge, even when a cheap model wrote it. Auth, payments, schema, public API contracts, one-way doors. The edge being paid for is thinking many steps ahead: the raw SQL string, the serialized blob another service reads, the test that silently encodes an assumption. "Cheap models write the code. Fable decides what ships."

### Beat 8: A better harness beats a bigger model (14:00 - 15:30) [the capstone, kept from five-jobs per Ray]

The move that sits above all of it: before spending Fable on anything, ask whether a cheaper model in a better harness gets there instead. Builder plus adversarial reviewer, looping up to three rounds, manufactures the judgement you would have paid Fable for. Escalation to Fable becomes a fallback triggered by failure, not a default reached out of habit.

"The goal was never to use your best model more. It was to need it less. And everything Fable wrote in its exit interview, the routing map, the references, the review rules, is exactly the harness that lets you."

---

## Ray thinks deeper (15:30 - 16:30)

The exit interview never actually ends. Fable is not the last model that will be taken away, repriced, or replaced; every frontier model is a temp now. The people who got the most out of Fable this month are the ones whose harness compounds regardless of which model sits inside it. So run the exit interview on whatever your best model is, on a schedule, not just when a pricing page forces you to. The deadline is just the first time you notice the pattern.

---

## What this means for you (16:30 - 17:15)

The ordered checklist, one screen, revealed progressively:

1. Architectural sweep of your churn-times-complexity hotspots.
2. Work retrospective over your session history (digest first).
3. Mythos-worthiness routing table into CLAUDE.md.
4. Miessler's goal-orientation and bitter-lesson prompts.
5. Golden references for your load-bearing patterns.
6. Review-gate rule for high blast radius changes.

"Run one and two today. Everything else falls out of what they find."

---

## Closer + pitch (17:15 - 18:00)

"That's the exit interview. Whether Fable is leaving your plan or staying on your payroll, the week you treat it like a departing genius instead of a fast intern is the week everything it produces starts outliving your subscription.

If you want to go deeper, the Masterclass covers the full delegation and harness system this video sketched. The July 4th sale ends July 6th and the price goes back up to `[PRICE]` after that. 14-day money-back guarantee, less than 0.2% of buyers have ever asked for one, and my email's in the description if you have questions.

And if you liked this, sign up free and install the masterclass MCP, it recommends class videos based on your actual workflow. No credit card needed. Link's below."

---

## Production notes

- Both demos pre-run and narrated over, not built live (40K+ videos lead with the idea, live building caps ~30K).
- Speak ~50% slower, let every finding linger 2-3 seconds, progressive reveal on the checklist and the routing table.
- Section title cards between the two halves ("THE EXIT INTERVIEW" / "THE HANDOVER PACK").
- Credits: Theo (routing table screenshot), Daniel Miessler (prompts post), both linked in description.
- Deadline check before filming: confirm the actual date Fable leaves the $200 plan and say it exactly once in the hook; vague urgency reads as manufactured.
- `[PRICE]` placeholder to fill before filming.
