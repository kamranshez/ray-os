---
tags: [youtube, script, claude-code, fable]
status: draft
date: 2026-07-05
---

## Working title options

1. Bold claim + anthropomorphism: **Your Smartest Model Is Quitting. Interview It First.**
2. Bold claim + specificity: **Run These 6 Prompts Before Fable Leaves the $200 Plan**
3. Curiosity gap + exclusivity: **What I'm Making Fable Do Before Anthropic Takes It Away**
4. Loss-framing (pattern behind the wave's 259k outlier): **Fable Leaves July 7. Skip This and Your Next 6 Months Run Worse.**

## Meta notes

- Coined term: **the exit interview**. Land it in the hook, repeat it at every section boundary.
- Pitch layer: soft anchor at 2:00 (objection-handler verbatim), closing urgency pitch at 16:45. Single paid CTA system, masterclass only, no newsletter mention.
- Verify before filming: July 7 removal date, 50% weekly cap figure, sale end date July 6. Fill `[PRICE]` in both pitch blocks.
- Pre-runs needed (fill the `[FINDING NARRATION]` placeholders): architectural sweep on course funnel repo, Opus session retrospective, one skill remake diff, entitlements golden reference run.
- Once this ships, pull `to-upload/five-jobs-for-your-best-model.md` from the queue (absorbed here).

---

## Hook

*Visual hook in first 10 seconds: usage screen or plan page with Fable greyed out, then a literal "EXIT INTERVIEW" calendar invite with Fable as the attendee.*

On July 7th, Fable disappears from the $200 plan. Which means right now, the smartest model I have ever had access to is working its notice period. So this week I did what good companies do when their best engineer resigns. I ran an exit interview. I made it tell me everything it knows about my codebase that nobody else can see, I asked it what it honestly thinks about how I work with Opus, the model that stays, and I made it set up the cheaper models that are about to replace it.

---

## The problem

*[IMAGE: split screen. Left: a frantic queue of tickets being shovelled into a Fable terminal, labelled "OUTPUT". Right: a small stack of documents labelled "WHAT IT KNOWS", untouched.]*

Here's what everyone with a $200 plan is doing this week. They've got a countdown in their head, and they're feeding Fable everything. Every backlog ticket, every half-finished feature, every "while I still have you" idea. Squeeze the genius for as much output as possible before the door closes.

And I get it. That was my first instinct too. Line up every hard task I've been putting off and burn my weekly cap to zero. Half of YouTube is telling you to do exactly that right now. Run these prompts, ship these features, maximum extraction.

But walk it forward. On July 8th, what do you actually have?

*Pause. Let it sit.*

You have a pile of code your daily model didn't write and doesn't fully understand. Then you fall back to Opus 4.8, which is a genuinely great model, and now it's maintaining a codebase full of Fable-shaped decisions with none of the reasoning that produced them. You didn't bank intelligence. You banked output. And output rots. Six months from now that binge week is just more surface area for Opus to misunderstand, while it quietly ships slop on top of it.

So I'm doing the opposite. The question for these last few days is not "what can Fable build for me." It's two things. One, what high-leverage work can Fable do now that makes everything easier for Opus later. And two, what does Fable know about how I work with Opus that would make that relationship better. Work that compounds instead of work that ships.

That's the exit interview. And the rest of this video is how to run one.

---

## Soft anchor

Quick pause. This video is sponsored by me and my Claude Code Masterclass. Over 1,500 engineers from companies you've heard of have gone through it, and a lot of them are now the best Claude Code user at their company. You're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. The July 4th sale is on right now and it ends July 6th, the price goes back up to `[PRICE]` after that. Link's below.

---

## Why this works: third and fourth order thinking

Before any prompts, you need to understand the one capability that makes this whole interview worth running. Because if Fable were just a faster Opus, none of this would matter.

Most models reason a few steps out. Change the thing, check the thing works, done. Fable reasons many more steps out. If Opus sees five steps ahead, Fable sees ten.

*[IMAGE: a ripple diagram. A database column rename in the centre, four concentric rings expanding outward, each ring labelled with the effects below. Rings light up one at a time as they're mentioned.]*

Here's a tiny example. You rename a database column. First order, the rename itself. Second order, the ORM model and that one raw SQL string someone wrote in a migration script. Third order, the serialized blob another service reads, and the analytics event contract that quietly includes the old name. Fourth order, the downstream pipeline that ingests those events, and the revenue dashboard nobody remembers is wired to it. A cheap model catches the first hop, maybe the second. Fable walks the whole chain, unprompted.

Every question in this exit interview is designed to cash in exactly that. You are not paying for faster code. You are paying for the model that sees around corners. Keep that in your head, because it's the test for every prompt in this video: does this question need the ripple, or just the first hop?

---

## Section 1: For those who won't use Fable 5 until it's back on the subscription

*[IMAGE: an interview room. Two chairs. One labelled FABLE with a cardboard box of desk belongings next to it, one labelled OPUS holding a clipboard.]*

A real exit interview has three questions. What do you know that we don't. What do you think of how we work. And what should we set up before you go. That's the whole structure, and every prompt in this section is one of those three questions pointed at your setup.

### How to run it, both ways

There are two ways to run this interview. The quick way is one big prompt.

*Full screen, linger. This is a screenshot moment.*

> "You leave this plan on July 7th, and this is your exit interview. Three questions, real effort on each.
>
> One: what do you know that nobody else can see? Do a deep pass over this codebase and tell me the structural problems, the load-bearing weirdness, and the risks a less capable model reads straight past. No point fixes. I want the things that will hurt in six months.
>
> Two: what do you honestly think of how I work? Read my recent session history and critique me, not the code. Where I go in circles, what I re-explain, which habits waste your capability. Be blunt, rank by impact.
>
> Three: what should we write down before you go? Turn everything above into artifacts that outlive your access."

That prompt alone will earn you more than a week of feature requests. But the better interview, the one real companies run, is a conversation. Someone sits across the table and asks follow-ups. So here's the upgrade: an agent team. Opus, the model that stays, interviews Fable back and forth.

Why is that better than the mega-prompt? Three reasons. One pass is shallow, an interviewer probes. Opus can demand specifics, push past the first vague answer, and keep Fable out of rat-holes. Second, the successor knows what it doesn't know. So Opus attempts a few representative tasks first and brings its failures to the interview as questions. "Here's what I did on the checkout flow, what would you have done?" That's a far sharper question than anything you'd write cold. And third, it verifies the transfer live. After each answer, Opus does a readback, applies the guidance to a concrete case, and asks "did I get it?" Knowledge that survives a readback is knowledge that actually transferred.

Now the honest drawbacks, because this can go wrong in ways that cost real money. Free-form model-to-model chat drifts and gets agreeable. Two models complimenting each other in circles while your Fable budget burns. The interviewer's quality bounds the extraction, so mediocre questions get a mediocre interview. And naive multi-turn wastes Fable tokens on re-reading context every round.

The fixes are cheap. Fable writes its own interview agenda in one small call. Opus conducts it, carries all the context, and hands Fable small distilled questions with hard termination criteria. Fable sets the syllabus. Opus runs the exam.

*Demo: run the main session as Opus and have it consult Fable per question via a subagent with the model parameter. Show one question, answer, readback round on screen, not the whole loop.*

Whichever way you run it, the interview covers the same ground. Let me walk through the beats.

### Beat 1: What does Fable know that nobody else does [LIVE DEMO]

This is questions one and two of the interview, run as one deep pass. What does it see in the code, and what does it see in you. I ran both on a real product, the course funnel behind my masterclass, and I'll show you the findings.

**First, the code.** Don't ask Fable to "review everything," you'll burn your cap on boilerplate. Target it. Two cheap signals tell you where the bodies are buried.

*Screen: terminal.*

One line of git gives you files ranked by how often they change. Another pass gives you a complexity signal per file. Multiply them together and you have your hotspots: the files that are both complicated and constantly touched. That's where structural problems live.

*Screen: the prompt.*

> "These are my hotspots by churn times complexity. Do an architectural review of the top five. I don't want point fixes, I want the structural problems a weaker model reads right past, and for each one, what it breaks downstream if left alone."

*Show one real finding full screen and linger 2-3 seconds. Ideally a cross-cutting issue spanning several files, because that's the third-order evidence the ripple section promised.*

`[FINDING NARRATION: walk through the single best finding from the pre-run. Name the files, say the downstream break in plain words, and point at the part a cheaper model would have read straight past.]`

And here's why this matters more than it looks. Most repos at this point are geological layers. Some Opus 4.1 at the bottom, some 4.5, some 4.6, a stratum of Sonnet, maybe some GLM. Fable is the only model smart enough to see the strata and tell you which layer is load bearing.

**Then, you.** Because the second interview question is not about the code, it's about the working relationship. And here's the twist that makes this actually useful: I didn't ask Fable to critique my sessions with Fable. I asked it to read my sessions with Opus. Opus is the model that stays. That's the relationship that needs coaching.

*Screen: the prompt, full screen, linger.*

> "Before you go, I want your honest read on how I work with Opus 4.8, because that is the model I'll be using after July 7th. Read a wide sample of my recent Opus sessions and tell me: one, where Opus and I go in circles, and whether the failure is its capability or my prompting. Two, what I tolerate from Opus that I shouldn't, and what I do manually that a better setup would make automatic. Three, what to encode into skills, CLAUDE.md rules, and hooks so Opus performs as close to you as it can get without re-teaching. Four, the three highest-leverage changes to how I prompt and delegate to it. Be blunt, rank everything by impact, and build the top artifact now."

One practical caveat before you run this. Raw session logs are long and noisy, and pointing Fable at the raw pile is the most expensive possible way to read them. Have a cheap model distill the logs into a digest first, then hand Fable the digest.

*Show 2-3 real findings from Ray's own Opus history. The more embarrassing, the better the retention.*

`[FINDING NARRATION: 2-3 findings from the pre-run. Each one lands as a pattern ("I re-explain X every session", "I accept Y when I shouldn't") and ends as an artifact: a skill, a CLAUDE.md line, or a hook that Fable built on the spot.]`

Notice the shape of both halves. Fable reads a huge amount of context, finds the patterns nobody else can see, and then converts them into artifacts that a cheaper model inherits for free. That's the whole exit interview in miniature.

### Beat 2: Remake your everyday skills

Question three of the interview: what should we set up before you go. Start with the skills you use every single day, because value there compounds daily.

But here's the counterintuitive part: remake, don't repair. Every skill in your library encodes the judgement of whichever model wrote it, and most of mine were written by an older Opus on its first attempt. And models generate better than they edit. Ask Fable to improve an existing skill and it anchors on the incumbent's structure. So don't. Give it the same source material and the same flow the original was built from, and have it build each one fresh, blind, without ever reading the current version. Then diff the two and keep the better one.

*Screen: the prompt fragment.*

> "Here is the source material and the flow my current skill automates. Do not read the existing skill. Design and build the best version of this skill from scratch. When you're done I'll diff you against the incumbent."

For me that's the scriptwriter skill, the wisdom extractor, and the A/B tester, the three that fire most often. For you it's whatever runs ten times a day. Your code-review skill, your PR skill, your deploy checklist.

*Screen: side-by-side diff of incumbent vs remake on one skill. Highlight one structural difference, not a line count.*

`[FINDING NARRATION: the diff moment from the pre-run. What did the remake do structurally differently, and which version won.]`

You will be surprised how often the remake wins. And every one that does is Fable-grade judgement running in your setup every day, long after Fable is gone.

### Beat 3: The golden reference

The other thing to build before it goes: golden references. Two facts you already know, combined into one move. Models generate better than they edit. And cheap models match patterns better than they exercise judgement. So: spend one expensive Fable run building the canonical implementation, and from then on, cheap models get a single instruction. "Make the other forty look like this one." You've converted open-ended judgement into closed-ended pattern matching. Spent once, copied forever.

*Screen: the entitlements state machine run on the course funnel.*

Here's the one I ran. The entitlements state machine on my course funnel, the code that decides who has access to what. One Fable run produced the reference: the subscription lifecycle states, the failure matrix, declined card, refund, expired plan, webhook arriving twice, webhook arriving out of order, the grace-period rules, and the acceptance tests that pin all of it down.

`[FINDING NARRATION: show the reference artifact from the pre-run. Point at the failure matrix specifically, the part a cheap model gets subtly wrong.]`

Notice what makes this a good golden reference candidate: it's judgement-dense, it has huge blast radius, and it's exactly the kind of thing a cheap model would get plausibly, quietly wrong. Then after July 7th, the cheap model builds everything around it against the reference. It matches the pattern. It never has to invent it.

### Beat 4: The meta-prompts

The last two prompts in the interview are not mine. They're from Daniel Miessler's ten prompts post, link in the description, and I've cherry-picked the two that fit this moment perfectly.

First, goal orientation:

*Screen: prompt card.*

> "Look at my whole harness and characterize what I'm ultimately trying to accomplish. Then find every part of the system working against that goal."

This is the retrospective from Beat 1 with the aperture wide open. Not "critique my sessions," but "look at everything I've built and tell me where it's fighting itself."

Second, and this is the thematically perfect one, the bitter-lesson audit:

*Screen: prompt card.*

> "Study Sutton's Bitter Lesson. Then find every place my harness is overengineered around today's model limitations, and give me a plan to make it flexible to future model improvements."

Think about why this one matters right now. Every workaround you've built exists because some model, at some point, wasn't good enough at something. Half of those limitations are already gone and your harness doesn't know it. This video literally exists because models rotate. This prompt is how your setup stops being surprised by that.

These are questions about your system, not your code. Cheap models answer them politely. Fable answers them correctly.

---

## Section 2: For those who'll use Fable in moderation

*[IMAGE: Fable's employee badge being swapped for a consultant lanyard labelled "SPECIALIST, BY APPOINTMENT".]*

Now, the second half. Maybe you're not quitting. Maybe you're keeping Fable through the API, or you just want to stop torching your weekly cap. Either way the discipline is the same: Fable stops being your daily driver and becomes the specialist you bring in for the handful of tasks where nothing else is good enough. Everything in the first half told you which tasks those are. Here's the system.

### Beat 5: The routing rule

The foundation is one line, and I have to credit Simon Willison for it, link in the description. The move is judgement-based delegation. You tell your top model:

*Screen: prompt card.*

> "For all coding tasks, use your judgement to decide an appropriate lower-power model and run that in a subagent."

You're not writing routing rules. You're delegating the routing decision itself to the model with the best judgement. Back it with a small model-ranking table in your CLAUDE.md: each model, its cost, its intelligence, its taste. That table is the org chart Fable manages against.

*Screen: the CLAUDE.md model table.*

Then my twist, the self-refining loop. After each subagent finishes, Fable grades the result against what it would have done, and updates its own routing notes. Get it wrong once, route better forever. The routing table is not static config, it's a judgement that gets sharper every session. You're not writing rules for Fable. You're letting Fable learn its own management style.

One quick aside: route by model AND effort. Fable on low effort beats maxed-out cheaper models on plenty of tasks, at a fraction of the burn. The dial has two axes and most people only turn one.

### Beat 6: One-way doors and two-way doors

*[IMAGE: two doors. One swings both ways, sketchy and casual. One is a bank vault mid-close.]*

Here's how to decide what still deserves Fable at all. Every technical decision is one of two doors.

A two-way door you can walk back through. UI copy, styling, an internal refactor behind a stable interface, anything behind a feature flag. Get it wrong, revert, nothing calcifies. Let cheap models ship these all day, unsupervised.

A one-way door locks behind you. The database schema. A public API contract. The auth and session model. The event schema your analytics history accumulates under. A migration strategy. Get these wrong and you live inside the mistake for years, because everything downstream builds on the wrong shape.

So the rule is one sentence: **Fable reviews every one-way door before it closes.** Cheap models can write the code. But anything irreversible gets a Fable review before merge, because judging a one-way door is exactly the third and fourth order reasoning from the start of this video. The code for an auth flow is small. The decision is enormous. Pay for the decision, not the keystrokes.

### Beat 7: A better harness beats a bigger model

And the move that sits above all of it. Before spending Fable on anything, ask one question: would a cheaper model in a better harness get there instead?

Here's what I mean by harness. A builder model writes the code, an adversarial reviewer model tries to tear it apart, and they loop until the reviewer runs out of real complaints. That loop manufactures the judgement you would have paid Fable for.

And the evidence on this is getting hard to ignore. We're finding that models like Kimi 2.7, even GLM 5.2, in a good harness with enough tokens, find the same bugs Fable finds. The intelligence gap is real. But a loop with verification closes most of it on plenty of tasks. So escalation to Fable becomes a fallback triggered by failure, not a default reached out of habit.

The goal was never to use your best model more. It was to need it less. And everything Fable produced in its exit interview, the findings, the references, the review rules, is exactly the harness that lets you.

---

## Closer + pitch

That's the exit interview. Whether Fable is leaving your plan or staying on retainer, the week you treat it like a departing genius instead of a fast intern is the week everything it produces starts outliving your subscription.

If you want to go deeper, the Masterclass covers the full delegation and harness system this video sketched. The July 4th sale ends July 6th and the price goes back up to `[PRICE]` after that. 14-day money-back guarantee, less than 0.2% of buyers have ever asked for one, and my email's in the description if you have questions.

And if you liked this, sign up free and install the masterclass MCP, it recommends class videos based on your actual workflow. No credit card needed. Link's below.
