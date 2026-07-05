---
tags: [youtube, script, claude-code]
status: draft
date: 2026-07-04
source: "Bento newsletter: Spending a day with Anthropic engineers (2026-06-13)"
---

## Title Options

| # | Formula | Title |
|---|---------|-------|
| 1 | Bold claim + personification | Anthropic's Engineers Are Living in Four Different Futures |
| 2 | Bold claim + specificity | I Spent a Day With 20 Anthropic Engineers. They Don't Use Frameworks |
| 3 | Curiosity gap + exclusivity | Anthropic Engineers Don't Work the Way You Think |

Coined term: **"the scaffolding melts away"**. Format: anchored insider (Tokyo as wrapper, plan-mode-plus-verification as the anchor), extended cut ~18-19 min with loops, unknown unknowns (Thariq's Fable field guide), and idea-generation/seeding sections. Pitch: masterclass, 30% off July 4th sale, ends Sunday July 6.

---

## Hook (0:00-0:35)

*Open on the Tokyo photos immediately. Venue shot, then the crowd shot. Clawd plushie for a beat of levity.*

A few weeks ago Anthropic ran their Code with Claude event in Tokyo. I was living in Tokyo at the time, so I got to spend a full day in a room with around twenty of the engineers who actually build Claude Code.

And I went in with one goal. I wanted to find the one true workflow. The way the people who make this tool really use it, so I could copy it and go home.

That is not what happened. There is no one true workflow. Not even inside Anthropic.

*Beat.*

But by the end of the day I realised the people building this thing have quietly converged on something much simpler than what the rest of us are doing. And if they're right, most of the scaffolding we've all been building around these models is about to melt away.

---

## Four Different Futures (0:35-1:30)

*Cut to b-roll of the event while telling the story. On the quote, put the words on screen and let them sit.*

So early in the day, one engineer said something to me that I haven't been able to stop thinking about since.

"We're all working in the future at Anthropic, but we're in four different futures. And one of them may be directionally correct."

And the more people I talked to, the more I realised she was completely right. Some engineers had elaborate, many-layered multi-agent setups doing huge chunks of their work. Others would casually mention that they just pop into Claude chat for some of their tasks. Some of the team even use Cowork for the lighter stuff.

> 🎨 DRAW `day-anthropic-four-futures` — one Anthropic building splitting into four sketchy branching paths (multi-agent stack, Claude chat, Cowork, terminal), one path faintly glowing "directionally correct"

![[day-anthropic-four-futures-1.png]]
![[day-anthropic-four-futures-2.png]]
![[day-anthropic-four-futures-3.png]]
![[day-anthropic-four-futures-4.png]]
![[day-anthropic-four-futures-5.png]]

Nobody acted like they'd figured it all out. Everyone was running their own experiment. Which, honestly, was weirdly reassuring.

But here's the detail that stuck with me. Behind the scenes, every engineer's session transcripts get backed up to one shared location, and someone on the team runs analysis across all of them to spot patterns. So even though everyone's off in their own future, the company is watching all four to see which one is winning.

And it filters down to the small stuff too. People post in a Slack channel, hey, can you quickly run this prompt and pass back what you get. Everyone is experimenting on everyone, all day long.

> 🎨 DRAW (optional) `day-anthropic-shared-transcripts` — four engineers' session transcripts flowing into one shared vault, magnifying glass scanning for patterns, small Slack bubble "can you quickly run this prompt?"

![[day-anthropic-shared-transcripts-1.png]]
![[day-anthropic-shared-transcripts-2.png]]
![[day-anthropic-shared-transcripts-3.png]]
![[day-anthropic-shared-transcripts-4.png]]
![[day-anthropic-shared-transcripts-5.png]]

---

## Soft Anchor (1:30-2:00)

*Lower-third card with the class name. Keep it brisk.*

Before we get into what they actually converged on, this video is sponsored by myself and my Claude Code masterclass. Over 2,000 engineers from some of the biggest companies in the world have taken it, and many are now the best Claude Code user at their company. You're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. It's 30 percent off for the 4th of July weekend, and the price goes back up on Sunday. Link below.

---

## The Problem: We Buried the Model in Scaffolding (2:00-4:30)

*Screen: a messy diagram building up piece by piece. Spec docs, agent boxes, arrows everywhere. Progressive reveal, one piece at a time.*

> 🎨 DRAW `day-anthropic-scaffolding-pileup` — a small model box getting buried under accumulating scaffolding: PRD doc, architecture doc, story tickets, agent org chart, arrows everywhere

![[day-anthropic-scaffolding-pileup-1.png]]
![[day-anthropic-scaffolding-pileup-2.png]]
![[day-anthropic-scaffolding-pileup-3.png]]
![[day-anthropic-scaffolding-pileup-4.png]]
![[day-anthropic-scaffolding-pileup-5.png]]

Okay. So here's the problem I think most of us have.

If you've spent any time on Twitter or LinkedIn, you've seen the workflows. Fifteen-step spec pipelines. Frameworks like BMAD where you generate a product requirements document, then an architecture document, then break it into stories before the model writes a line of code. Multi-agent org charts with a project manager agent delegating to a team of worker agents. And the flow I see everywhere right now. Interview the model, write a design doc, break it into tickets, then run every ticket in its own fresh context.

And if that structure feels familiar, it should. That's waterfall. We spent twenty years learning that a perfect document written up front does not survive contact with real software. And then agents came along and we rebuilt waterfall for them.

> 🎨 DRAW `day-anthropic-waterfall-rebuilt` — classic waterfall cascade (requirements → design → build → test) side by side with the same cascade redrawn with robot agents at each step, labelled "20 years later"

![[day-anthropic-waterfall-rebuilt-1.png]]
![[day-anthropic-waterfall-rebuilt-2.png]]
![[day-anthropic-waterfall-rebuilt-3.png]]
![[day-anthropic-waterfall-rebuilt-4.png]]
![[day-anthropic-waterfall-rebuilt-5.png]]

You've probably felt that quiet anxiety of, am I behind? Should I be doing all this?

I've felt it too. And I tried the heavy approach. Rigid specs, over-specified plans, documents describing exactly what the agent should do at every step.

Here's the thing nobody tells you about specs. The spec is a map. The codebase, the real constraints, the weird edge cases, that's the territory. And the map is never the territory. You can make your spec as detailed as you want, you can try to cover every case, and somewhere in the middle of implementation the model will still hit something your map didn't mark. Now the model has two options. Follow your map off a cliff, or deviate from the spec you spent an hour writing. Either way, the scaffolding you built to make it more reliable is now the thing making it worse.

> 🎨 DRAW `day-anthropic-spec-map-territory` — hand-drawn map held over real terrain, an unmapped cliff/chasm in the territory the map doesn't show, robot at the fork: follow map off cliff vs deviate from spec. REUSE CANDIDATE: `find-unknowns-map-vs-territory-1..5.png` already exist

![[day-anthropic-spec-map-territory-1.png]]
![[day-anthropic-spec-map-territory-2.png]]
![[day-anthropic-spec-map-territory-3.png]]
![[day-anthropic-spec-map-territory-4.png]]
![[day-anthropic-spec-map-territory-5.png]]

And here's the part that really breaks the whole idea. If your spec genuinely covered everything, every case, every edge, every decision, it wouldn't be a spec anymore. It would just be the code, written in English. At that point, what did you need the agent for?

> 🎨 DRAW (optional) `day-anthropic-spec-becomes-code` — a spec document growing more and more detailed until it morphs into the codebase itself, "just the code, written in English"

![[day-anthropic-spec-becomes-code-1.png]]
![[day-anthropic-spec-becomes-code-2.png]]
![[day-anthropic-spec-becomes-code-3.png]]
![[day-anthropic-spec-becomes-code-4.png]]
![[day-anthropic-spec-becomes-code-5.png]]

*Screen: "The Bitter Lesson, Richard Sutton" on screen, plain.*

> 🎨 DRAW `day-anthropic-bitter-lesson` — repeating cycle diagram: researchers build clever hand-crafted structure → model gets better → structure starts hurting → thrown away → repeat, with a rising capability curve underneath

![[day-anthropic-bitter-lesson-1.png]]
![[day-anthropic-bitter-lesson-2.png]]
![[day-anthropic-bitter-lesson-3.png]]
![[day-anthropic-bitter-lesson-4.png]]
![[day-anthropic-bitter-lesson-5.png]]

There's a famous essay by Richard Sutton called The Bitter Lesson. The short version is that in AI, every generation of researchers builds clever, hand-crafted structure to compensate for what the models can't do yet. And every generation, the models get better, and all that hand-crafted structure stops helping and starts hurting.

That is exactly what's happening to our workflows right now. Most of what people were teaching a year ago was built for models you couldn't trust with ambiguity. The models got dramatically better. The techniques didn't move. So a lot of what's still being sold as best practice isn't helping the model anymore. It's restraining it.

And it's worth spelling out what actually got better, because it's not just "smarter." When a model builds a feature, it's constantly diving into subtasks. Fix the bug, which means understand this module, which means read this function, which surfaces a failing test, which needs a config change. In programming terms, it's pushing frames onto a call stack. And the whole game is whether it can go that deep and still pop all the way back up to what you originally asked.

Models a year ago dropped frames. They'd go three subtasks deep, finish the little thing at the bottom, and come back up having lost the plot. That's the real problem all the ceremony was solving. The PRD, the tickets, the fresh context per ticket. All of it was an external call stack. You were keeping the frames on paper because the model couldn't keep them in its head.

Fable just keeps the stack. It can go ten levels down a rabbit hole, resolve it, and unwind back to the original goal without you re-explaining anything. And once the model holds its own call stack, writing it all down for it stops being safety and starts being overhead.

> 🎨 DRAW `day-anthropic-call-stack` — a deep call stack of nested subtask frames (fix bug → understand module → read function → failing test → config change); old model climbing back up but dropping frames and losing the original goal, vs Fable unwinding cleanly frame by frame back to the top-level ask

![[day-anthropic-call-stack-1.png]]
![[day-anthropic-call-stack-2.png]]
![[day-anthropic-call-stack-3.png]]
![[day-anthropic-call-stack-4.png]]
![[day-anthropic-call-stack-5.png]]

So here I am, in a room with twenty people who build the tool. The people with the most incentive in the world to have an elaborate, optimised workflow. And you know how many of them mentioned spec-driven development frameworks?

Zero. Not one person.

---

## What They Actually Do (4:30-6:00)

*Screen: the three steps appear one at a time as spoken. Plan. Execute. Verify. Nothing else on screen.*

> 🎨 DRAW `day-anthropic-plan-execute-verify` — the whole workflow as three clean steps, Plan → Execute → Verify, deliberately sparse against all the earlier clutter

![[day-anthropic-plan-execute-verify-1.png]]
![[day-anthropic-plan-execute-verify-2.png]]
![[day-anthropic-plan-execute-verify-3.png]]
![[day-anthropic-plan-execute-verify-4.png]]
![[day-anthropic-plan-execute-verify-5.png]]

What I heard instead, over and over, in all four futures, was some version of the same three-step shape.

One. Work in plan mode. You describe what you want, you give the model a few constraints, and it proposes a plan. You're not writing the plan. You're reviewing one.

Two. Let the model execute the plan.

Three. And this is the step most people skip. The model verifies its own work by actually using what it built. And the framing that stuck with me is a question. Where does a user actually interact with this change? A terminal, a browser, an API. Whatever the answer is, that's where verification happens. Not reading the code and declaring it correct. Going to the surface a real user touches and clicking the buttons like a real user would.

> 🎨 DRAW `day-anthropic-verification-surface` — a code change radiating out to the surfaces users actually touch (terminal, browser, API), robot clicking through the browser like a user instead of reading the diff

![[day-anthropic-verification-surface-1.png]]
![[day-anthropic-verification-surface-2.png]]
![[day-anthropic-verification-surface-3.png]]
![[day-anthropic-verification-surface-4.png]]
![[day-anthropic-verification-surface-5.png]]

That's it. That's the workflow at the frontier lab. Describe, constrain, plan, execute, verify.

And I want to be really concrete about what I didn't hear. Nobody was doing the interview, then the design doc, then breaking it into tickets and running every ticket in a fresh context. Not one person. They just prompt features. Maybe a quick interview first if the problem is fuzzy. Maybe they look at a couple of different designs and pick one. Then it builds, and it verifies in their cloud container.

And there's one more piece that made the whole order of operations click for me. Every PR gets a code review. And that review keeps catching things that would never have appeared in any spec. So it's actually better to let something slightly fuzzy survive contact with the real codebase, and then review what came out, than to try to define everything up front against a codebase you haven't touched yet.

> 🎨 DRAW `day-anthropic-fuzzy-vs-predefined` — two lanes: rigid fully-specified plan shattering on contact with the real codebase vs a fuzzy blob surviving contact and then getting sharpened by a code-review funnel that catches what no spec would have

![[day-anthropic-fuzzy-vs-predefined-1.png]]
![[day-anthropic-fuzzy-vs-predefined-2.png]]
![[day-anthropic-fuzzy-vs-predefined-3.png]]
![[day-anthropic-fuzzy-vs-predefined-4.png]]
![[day-anthropic-fuzzy-vs-predefined-5.png]]

The only things worth deciding up front are the genuinely big calls. Are we doing an architectural sweep and moving everything into a new module, or are we just doing point patches? Decisions at that level, yes. Everything below it, let the territory teach you.

And look, the heavy version may have genuinely been fine a year ago. But with models like Fable and Opus 4.8, you're paying all that ceremony to solve a problem the model no longer has.

And notice what this is. This is the Bitter Lesson playing out in real time, except this round it's not happening to researchers, it's happening to our workflows. Spec frameworks, rigid pipelines, elaborate agent hierarchies. The scaffolding melts away. The better the model gets, the less structure you should be wrapping around it. What survives isn't the scaffolding. It's the verification.

---

## The Exception: Long-Running Agents (6:00-7:30)

*Screen: three boxes appear one at a time. Builder. Adversarial Reviewer. Verifier.*

> 🎨 DRAW `day-anthropic-three-roles` — three robots: Builder constructing, Adversarial Reviewer actively poking holes/attacking the work, Verifier stamping it done; all structure on the checking side, builder left free

![[day-anthropic-three-roles-1.png]]
![[day-anthropic-three-roles-2.png]]
![[day-anthropic-three-roles-3.png]]
![[day-anthropic-three-roles-4.png]]
![[day-anthropic-three-roles-5.png]]

Now, there is one place where the engineers did describe real structure, and it's worth knowing exactly where the line is.

Long-running agents. When you're kicking off work that runs for a long time without you watching, one workshop laid out a three-role pattern, and I'm now fully sold on it.

First role, the builder. Does the actual work.

Second role, the adversarial reviewer. This is a separate subagent, and its entire job is to try to poke holes in what the builder did. Not to check it. To attack it. That difference in framing matters, because a reviewer that wants the work to pass will let it pass.

Third role, the verifier. Confirms the work is genuinely done.

Notice what this structure is and isn't. It's not scaffolding around how the builder works. Nobody's handing the builder a fifteen-step spec. All of the structure is on the checking side. Which is exactly what the Bitter Lesson predicts should survive.

---

## The Verify-Against-Plan Trap (7:30-9:45)

*Screen: walk through the four steps as a small numbered sequence, revealed one at a time.*

> 🎨 DRAW `day-anthropic-verify-trap` — 4-step false alarm: plan assumes X → builder discovers X is wrong in the territory → builder does the smarter thing → verifier compares against the plan and raises a false red flag; verifier siding with the map while the builder stands in the territory

![[day-anthropic-verify-trap-1.png]]
![[day-anthropic-verify-trap-2.png]]
![[day-anthropic-verify-trap-3.png]]
![[day-anthropic-verify-trap-4.png]]
![[day-anthropic-verify-trap-5.png]]

But there's a subtle trap in that verifier role, and this is the thing I took home that I'd genuinely never thought about before.

If your verifier checks the work against your original plan, you can get a false alarm. Watch how this plays out.

One. Your plan makes some assumption.

Two. The builder goes off, experiments, and realises the assumption was wrong.

Three. The builder adapts and does the smarter thing. Which is what you want.

Four. Your verifier compares the result against the original plan, sees a mismatch, and flags it. Not implemented as described.

The work was fine. The plan was wrong. And your verification system just punished the model for being right where you were wrong.

This is the map and territory thing all over again. The plan is your map. The builder was actually out in the territory. And your verifier just sided with the map.

The fix is almost the opposite of what most people do. Don't over-specify your plans. Leave room for the builder to be right where you were wrong, and let it leave follow-up notes on the plan as it learns.

But honestly, I've come to think the real fix goes one step further. Your verifier shouldn't be verifying against the plan at all. It should verify by behaving as a user. Open the app, click through the flow, check that the thing the plan was for actually works. Because the plan was never the goal. The plan was a guess about how to reach the goal.

*Screen: the /verify skill prompt, key lines highlighted one at a time: "Don't run tests. Don't typecheck." and "where a user meets the change".*

And Anthropic clearly believes this too, because they've shipped it as a built-in skill. Claude Code now has a /verify skill, and I pulled its full prompt out of the binary. The very first instructions are, do not run the tests, do not typecheck, because that only proves you can run CI. Instead it asks one question. Where does a user actually meet this change? A terminal, a browser, an API. Then it goes to that surface, drives the app like a real user, and even probes around the change by typing the things a user would type wrong. I break down the whole prompt line by line inside the class, but the philosophy fits in one sentence. Verification is runtime observation at the surface where a user touches your change. Not a diff review. Not a test run.

And just so you know how far I've personally taken this. I have a separate Windows machine sitting there whose only job is verifying user flows for me. And for HyperWhisper, my dictation app, I give the agent a speaker and a microphone, so it can play audio out loud, pick it up through the mic, and behave like a real user actually dictating. Once you accept that verification is the part that survives, you start building infrastructure for it.

> 🎨 DRAW (optional) `day-anthropic-verification-rig` — dedicated Windows machine whose only job is clicking through user flows, plus the HyperWhisper rig: speaker playing audio into a real microphone so the agent dictates like a human

![[day-anthropic-verification-rig-1.png]]
![[day-anthropic-verification-rig-2.png]]
![[day-anthropic-verification-rig-3.png]]
![[day-anthropic-verification-rig-4.png]]
![[day-anthropic-verification-rig-5.png]]

---

## Demo: The Whole Loop on a Real Project (9:45-11:15)

*Screen: terminal + the masterclass landing page side by side. Narrate over pre-recorded footage, don't build live. Keep the pace slow, let each state linger.*

Let me show you what this actually looks like, start to finish, on a real project. This is the landing page for my masterclass, and I want to add a section to it.

So step one, plan mode. I describe what I want in two sentences and give it one constraint. Notice what I'm not doing. No spec document, no step-by-step instructions. It reads the codebase and proposes the plan, and my only job is to review it.

*Show the plan appearing. Linger.*

Step two, I approve it and it builds.

Step three is where it gets fun. When it's done, it doesn't just tell me it's done. It opens the page in a browser and behaves like a visitor. Scrolls to the new section, checks it renders, clicks through it, on desktop and mobile widths.

*Show the browser moving on its own. This is the money shot, let it breathe.*

And notice, it's verifying against the outcome, not the plan. If it had deviated from the plan somewhere in the middle because the plan was wrong, this verification wouldn't care. It's asking one question. Does the page work for a user?

That's the whole loop. Describe, plan, execute, verify as a user. No framework. And this is the point of everything the engineers told me in Tokyo. The model didn't need my scaffolding. It needed my intent, a few constraints, and a way to check its own work.

---

## Once You Trust Verification: Loops (11:15-12:30)

*Screen: a simple circle diagram building up: plan, execute, verify, repeat. Then the Boris clip freeze-frame.*

> 🎨 DRAW `day-anthropic-closed-loop` — plan → execute → verify closing into a self-spinning circle, human stepping back from the desk while it keeps turning

![[day-anthropic-closed-loop-1.png]]
![[day-anthropic-closed-loop-2.png]]
![[day-anthropic-closed-loop-3.png]]
![[day-anthropic-closed-loop-4.png]]
![[day-anthropic-closed-loop-5.png]]

Now, once your verification is trustworthy, something bigger opens up. Because if the model can properly check its own work, you don't have to sit there watching it. You can close the loop and let it run.

A clip of Boris, the creator of Claude Code, talking about loops went viral recently. I made a whole video on it. And what surprised me in Tokyo is that other Anthropic employees were just as curious about what he meant as the rest of us. One of them was literally brainstorming with Jarred, the creator of Bun, about what loops he has set up. The people inside the building are trading loop ideas the same way we are.

Since the event I've been thinking in loops constantly. My favourite trick so far, I created a loop whose entire job is to find opportunities for other loops. I gave it every connector I have, email, analytics, calendar, all of it, and let it hunt for repeating work in my life that should become a loop. And one small tip that works weirdly well. Add "Surprise me!" at the end of a prompt like that. It gives the model permission to bring back the ideas you didn't ask for.

> 🎨 DRAW `day-anthropic-loop-finding-loops` — a meta-loop with a magnifying glass sweeping across email, analytics, calendar connectors, spotting repeating work and spawning little baby loops, "Surprise me!" speech bubble

![[day-anthropic-loop-finding-loops-1.png]]
![[day-anthropic-loop-finding-loops-2.png]]
![[day-anthropic-loop-finding-loops-3.png]]
![[day-anthropic-loop-finding-loops-4.png]]
![[day-anthropic-loop-finding-loops-5.png]]

But this raises the real question. If the loop is plan, execute, verify, and the model handles all three, what's actually left for you? And this is where the day in Tokyo connects to something one of the Claude Code engineers just published.

---

## Finding Your Unknown Unknowns (12:30-14:30)

*Screen: Thariq's post. Then the four quadrants appearing one at a time: known knowns, known unknowns, unknown knowns, unknown unknowns.*

> 🎨 DRAW `day-anthropic-knowns-matrix` — the 2x2 quadrant grid: known knowns / known unknowns / unknown knowns / unknown unknowns, the last quadrant dark and ominous. REUSE CANDIDATE: `find-unknowns-knowns-matrix-1..5.png` already exist

![[day-anthropic-knowns-matrix-1.png]]
![[day-anthropic-knowns-matrix-2.png]]
![[day-anthropic-knowns-matrix-3.png]]
![[day-anthropic-knowns-matrix-4.png]]
![[day-anthropic-knowns-matrix-5.png]]

Thariq, one of the engineers on Claude Code, just published a post called A Field Guide to Fable, and it puts a name on the thing I've been circling this whole video. The map is not the territory. Your prompt, your context, your plan, that's the map. The codebase and the real world, that's the territory. And he calls the gap between them your unknowns.

The line that stuck with me: Fable is the first model where the quality of the work is bottlenecked by his ability to clarify his own unknowns. Sit with that. One of the people building this thing is saying the model is no longer the bottleneck. He is. What he doesn't know he doesn't know is.

So the skill worth building isn't writing longer specs. It's using the model to shrink that gap. And you can use those literal words. When I started reverse engineering the Claude Code binary, I was staring at a blob I knew nothing about. So before anything else, I asked Claude for a blindspot pass. Here's what I'm trying to do, here's what I know, tell me my unknown unknowns and teach me enough to prompt you properly. It came back with the questions I didn't even know I was supposed to ask, and that changed how I attacked the whole thing. That workflow, by the way, is one of the ones the Anthropic engineers in Tokyo were genuinely impressed by. And notice, it starts with admitting what you don't know.

> 🎨 DRAW `day-anthropic-blindspot-pass` — flashlight sweeping over a dark unknown blob (the binary), beam revealing floating question marks that turn into concrete questions. REUSE CANDIDATE: `find-unknowns-blind-spot-sources-1..5.png` exist but were drawn for a different framing, check fit

![[day-anthropic-blindspot-pass-1.png]]
![[day-anthropic-blindspot-pass-2.png]]
![[day-anthropic-blindspot-pass-3.png]]
![[day-anthropic-blindspot-pass-4.png]]
![[day-anthropic-blindspot-pass-5.png]]

The other technique from his list I use constantly is the interview. Before a bigger piece of work, ask Claude to interview you, one question at a time, about anything ambiguous, prioritising the questions where your answer would change the architecture. You will be shocked what it pulls out of you. Things you knew but would never have thought to write down. That's your unknown knowns, extracted.

---

## Where Good Ideas Come From (14:30-16:45)

*Screen: a fresh terminal session. One short line gets pasted in. Then ideas start streaming.*

> 🎨 DRAW `day-anthropic-seed-session` — a tiny seed (one-line insight) planted into a fresh terminal, growing into a branching tree of ideas, then wilting past a "50-60k tokens" marker; next to it a polluted old chat where the same seed fails to sprout

![[day-anthropic-seed-session-1.png]]
![[day-anthropic-seed-session-2.png]]
![[day-anthropic-seed-session-3.png]]
![[day-anthropic-seed-session-4.png]]
![[day-anthropic-seed-session-5.png]]

There's one more thing I've been working out since Tokyo, and it's about where the ideas come from in the first place.

Here's how I generate ideas now. I find one really good insight, a line or two, that's it, and I paste it into a completely fresh session as the very first message. That seed pushes the model into a certain state, and the whole session comes out different. Sharper directions, better ideas, tons of them. And then somewhere around fifty or sixty thousand tokens in, the session just gets stupid. The magic wears off. I restart.

Because here's what I've realised. You only get so many good turns with a model on this kind of work. Which completely changes the question. The question isn't how do I prompt better. The question is where do I get high-signal insights to seed with.

And you can't cheat it. If you drop a great insight into an existing chat, you inherit the pollution from everything that came before it. It needs a fresh session and a clean seed.

One habit that compounds. When a session does turn out great, before I close it, I have it condense the entire run down into a seed. A line or two that captures the insight. So I can plant it again later.

But you also have to be honest about what the model gives back. When you ask for twenty ideas, you're pulling a slot machine. Occasionally there's a genuine hidden gem in the output, but the model doesn't reliably know which one it is. And you'll only spot it if you have the lived experience to recognise it when you read it. You still have to be someone who actually works with these agents every day. Taste is the one part of the workflow that doesn't melt away.

> 🎨 DRAW `day-anthropic-idea-slot-machine` — slot machine spitting out twenty idea cards, one hidden gem glowing among them, visible only through the "lived experience" glasses a person is wearing

![[day-anthropic-idea-slot-machine-1.png]]
![[day-anthropic-idea-slot-machine-2.png]]
![[day-anthropic-idea-slot-machine-3.png]]
![[day-anthropic-idea-slot-machine-4.png]]
![[day-anthropic-idea-slot-machine-5.png]]

So where do the seeds come from? Follow good people online, people like me. And honestly, this is exactly how I think about my own content. My videos, here and inside the class, I keep as short and as dense as I possibly can, because each one is meant to be a seed, not an hour of filler.

*Screen: a class video page. Cursor moves to the Open in Claude Code button. Press it. Claude Code launches with the lesson loaded and starts riffing.*

And we just shipped a feature in the class that takes this literally. Every video now has a button. Open in Claude Code. You press it, and the lesson opens in Claude Code as a seed. It loads the video's content as context and starts riffing on how it applies to your workflow, your projects, your setup. The class isn't just videos anymore. It's a library of seeds you can plant in your own sessions.

> 🎨 DRAW (optional) `day-anthropic-library-of-seeds` — a shelf of seed packets, each packet a short class video, one being picked and planted straight into a terminal session via the Open in Claude Code button

![[day-anthropic-library-of-seeds-1.png]]
![[day-anthropic-library-of-seeds-2.png]]
![[day-anthropic-library-of-seeds-3.png]]
![[day-anthropic-library-of-seeds-4.png]]
![[day-anthropic-library-of-seeds-5.png]]

---

## What This Means for You (16:45-17:30)

*Back to camera.*

So, practically.

If you're using a heavy spec framework today, try running your next feature with just plan mode and a verification step. My honest bet is you won't go back.

If you're running long agents, split the roles. Builder, adversarial reviewer, verifier. Structure on the checking side, freedom on the building side.

Make your verifier act like a user, not like an auditor comparing work to a plan.

And before your next unfamiliar piece of work, ask for a blindspot pass. The bottleneck isn't the model anymore. It's what you don't know you don't know.

One more thing I'll leave you with. Some of my friends work on reinforcement learning at Anthropic, which means they spend all day with models like Fable and Mythos. And even at that level, they told me the model still sometimes goes confidently down a completely wrong path, and the only thing that catches it is their own lived experience with the problem. So I asked them the uncomfortable question. If the internal models are that good, what's the difference between you prompting them and a junior engineer who just joined prompting them? Why are you paid more? And their answer came down to judgment. Knowing when the model is wrong, especially on judgment-heavy work, is still the job. There are plenty of situations where they know better than the model. One day it will know better than them. But that day isn't here yet. And until it is, that judgment is the part you bring too.

> 🎨 DRAW `day-anthropic-senior-judgment-gap` — junior and senior staring at the same model output, ninety percent glowing correct with a confident wrong claim at the very end; only the senior's "lived experience" lens reveals the flaw, with a small closing-gap timeline underneath ("a few more years")

![[day-anthropic-senior-judgment-gap-1.png]]
![[day-anthropic-senior-judgment-gap-2.png]]
![[day-anthropic-senior-judgment-gap-3.png]]
![[day-anthropic-senior-judgment-gap-4.png]]
![[day-anthropic-senior-judgment-gap-5.png]]

And that's really where the whole day in Tokyo landed for me. The people building this thing are still figuring it out. There are many futures, and one of them may be directionally correct. I have no idea if mine is. But I'm enjoying finding out.

---

## Close (17:30-18:15)

If you want to go deeper on this, the masterclass covers the full version of what I showed today, including how I set up plan mode, verification with browser use, the /verify skill's full prompt line by line, and the exact three-role setup for long-running agents. It's 30 percent off for the 4th of July weekend and the price goes back up on Sunday, so this weekend is the cheapest it will be. There's a 14-day money-back guarantee, and less than 0.2 percent of buyers have ever asked for a refund. If you have questions, email me, my address is in the description.

And if you're not sure yet, install the free masterclass MCP. You can ask it questions about your own workflow and it'll recommend specific videos from the class based on what you're working on. No credit card needed, just sign up. Link's in the description.

See you in the next one.
