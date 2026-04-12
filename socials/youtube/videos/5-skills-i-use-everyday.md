---
date: 2026-04-09
status: draft
---

## Intro

I was showing a friend some of my Claude Code skills the other day and he just stopped me mid-demo and was like "Dude, what? You're so ahead of the curve. You need to make a video on this." So here I am.

---

## Skill 1: /auto-spec

> [SCREEN RECORDING — Claude Code terminal]

https://x.com/trq212/status/2005315275026260309

The first skill I use every day is auto-spec. Now, I'll explain this from the beginning because no one else is doing this.

So there's this approach that a lot of people in the Claude Code space have been doing — the idea of interviewing yourself before you build anything. You write a rough plan, then you get Claude to question you on every aspect of it until you have a shared understanding of what you're actually building.

This is an idea that I talked about 3 months ago on the channel so if you do wanna stay ahead of the curve, do subscribe.

So I did this for about a month and I realised. Wow... At first, this is great. Then day by day, I realised this is so boring, I'm just here answering questions all day. 

So I thought. Okay, I've answered enough questions by now that... What if Claude could interview a version of me instead?

Now what do you mean by version of you?

The idea of a version of you existing inside the model — that's what makes this work. It's not just a generic "answer these questions" agent. It's an agent that has absorbed my taste, my priorities, my biases. When it sees a question about whether to build a custom UI or reuse an existing pattern, it already knows what I'd say.

That's what auto-spec does.

That's what auto-spec does. When I invoke it, it creates a team of two agents. Agent one is the interviewer — it reads the plan and asks deep, non-obvious questions about every aspect. Architecture, UI, tradeoffs, scope. Agent two is a simulation of me. A digital twin. It's read 200 of my real question-answer pairs from previous spec interviews. It knows how I think. It knows I'll pick pragmatic over elegant. It knows I'll say "skip that for v1." It knows I'll push back on anything that adds a new database table unless it's absolutely necessary.

I kick it off, I go make coffee, I come back and there's a completed interview with 25 questions answered. And it gets it right about 95% of the time.

> [SHOW BROWSER — the HTML decision tree output]

And then it generates this. An interactive decision tree. Every decision laid out as a card, colour-coded by category — architecture in blue, UI in green, scope in orange. Each card shows the question, the options that were considered, and the decision that was made with a rationale.

Then it automatically integrates all the decisions back into the plan file as a "Spec Decisions" section. So when the implementing agent picks up the plan, every ambiguity has already been resolved.

The key idea is the decision profile. I have a compact file — about 2,500 tokens — that distils how I make decisions. My heuristics, my defaults, my red lines. Plus 400 real Q&A examples for the sim to pattern-match against.

And if you're thinking "I don't have 400 Q&A examples" — I built another skill called auto-spec-creator that analyses your Claude Code conversation history and generates the decision profile for you. You run it once and you have a digital twin.

If you want to go deeper on this, I cover the full spec developer workflow and how to verify implementations in my Claude Code masterclass.

There's also a sale.

---

## Skill 2: /design-variations

> [SCREEN RECORDING — Claude Code terminal + browser with variations]

Second skill. Design variations.

Here's the problem this solves. You're building a UI component — maybe a settings page, maybe a card layout, maybe a pricing section — and it looks... fine. It's functional. But you know it could be better. You just can't picture what "better" looks like.

The old way: open Figma, spend an hour mocking up three alternatives, pick one, then go back to code and implement it. That's two hours for a decision that should take five minutes.

What I do instead: I tell Claude "extract this component into a standalone HTML file and generate 8 design variations. Show them all on one page."

> [SHOW BROWSER — 8 variations side by side]

60 seconds later I'm looking at 8 real, implemented variations side by side. Not mockups — actual code. Different layouts, different spacing, different visual hierarchies. I pick the one I like, I say "integrate variation 4 back into the project," and it's done. The temporary HTML file gets cleaned up. The component is updated. I commit and push.

This replaced Figma for me entirely. I don't mockup anymore. I generate 10 real implementations and pick the best one. It's faster than designing because the "design" is already code.

And this works especially well for things that are hard to run side by side normally. If you're building for macOS or iOS, you can't just spin up 10 simulators to compare layouts. But you can generate 10 HTML variations and see them all at once.

The key insight: don't iterate one design at a time. Generate many in parallel and pick a winner. It's the same principle behind A/B testing — except you're doing it before you ship, not after.

I showed this workflow in detail in my Claude Code masterclass — the concept of sandboxing components into temporary HTML files for rapid design exploration.

---

## Skill 3: /mermaid-diagram-generator

> [SCREEN RECORDING — Claude Code terminal + diagram in browser]

Third skill. Mermaid diagram generator.

I use this every single day and it's not for documentation. It's for understanding.

When I'm reviewing a PR, or planning a feature, or trying to figure out how a payment flow works — I don't read the code line by line. I say "diagram the purchase flow as a sequence diagram" and I get this.

> [SHOW BROWSER — interactive Mermaid diagram]

An interactive HTML diagram. Participants on the x-axis, messages flowing between them, phases annotated. I can see in 10 seconds what would take me 5 minutes of reading code to piece together.

And the interactive version is wild. You can click any node to change its color. Double-click to edit text. Switch between light and dark themes. Export as PNG or SVG. It even asks you upfront — is this for a presentation, documentation, or a quick sketch? — and adapts the styling.

But here's why it's actually useful every day. It's a visual sanity check. If the diagram looks wrong — if there's an arrow going somewhere it shouldn't, or a participant that's not involved — the code is wrong. The diagram surfaces architectural issues that are invisible when you're reading code.

I covered this concept in my Claude Code masterclass — the idea of validating the "shape of the diff" visually instead of reading every line. You check the diagram, confirm it matches your mental model, and move on with confidence.

> [SHOW BROWSER — description-drift-detection.html from VidTempla repo]
>
> Here's a real example. I just shipped a description drift detection feature — detects when someone edits a YouTube description directly in YouTube Studio, bypassing the template system. Instead of reading the diff across 30 files, I generated this. Three diagrams: how drift is detected during sync, how write operations are gated, and the three resolution paths. Took 60 seconds to generate. Would've taken me 15 minutes to explain in a code review.

You're probably noticing a trend here. Design variations, diagrams — I'm not writing code and reviewing code anymore. I'm getting Claude to generate an artefact and then I review the artefact. It's faster, it's more intuitive, and honestly it's a better use of my time. Reading a diagram or picking from 10 designs is a much higher-leverage activity than reading a diff line by line.

---

## Skill 4: /triage

> [SCREEN RECORDING — Claude Code triage session]

Fourth skill. And this one has nothing to do with code at all.

Here's the thing about AI right now. It makes it so fast and easy to build new features that the real risk isn't building too slowly. It's building a confusing mess of a product. You still need to make tradeoffs. You still need someone saying "no, we're not adding that" or "that's not worth the complexity."

And the models won't do that for you. They're sycophantic. They're trying to be helpful and not offend you. You ask Claude "is this a good idea?" and it'll say "yes, this is a great idea, here are 5 ways to make it even better." It won't tell you to cut scope. It won't tell you the feature isn't worth building. It just wants to help.

So I built a triage skill that forces me to actually make the decisions. It connects to my Gmail via MCP, reads my recent unread emails, and filters them through the lens of whatever project I'm currently working in.

So if I'm in my SaaS repo and I run /triage, it pulls my inbox but only surfaces the emails relevant to that product — feature requests from users, bug reports, partnership asks. It ignores the newsletters, the receipts, the noise.

If I switch to this repo — my content OS — and run /triage again, same inbox, different results. Now it surfaces collaboration requests, sponsor emails, audience feedback.

For each actionable email, it categorizes it — feature request, bug, collab, business — and then interviews me about it.

> [SHOW — AskUserQuestion prompt]

It asks: "Feature request from user@email.com — they want a streaming API for the webhook endpoint. Why does this matter to you? Should we act on it?" And I pick: act on it, backlog it, push back, or skip.

If I say "push back" — this is my favourite part — it drafts a reply that asks the requester *why* they want the feature. Not a rejection. A genuine "what's the use case behind this? What problem are you trying to solve?" Because half the time, the feature they're asking for isn't what they actually need.

Every item I act on or backlog gets filed into an ideas/ folder as a markdown file with frontmatter — source, date, category, priority, and my notes on why it matters. It builds up over time into a prioritised backlog that came directly from real user feedback, not my assumptions.

And the whole thing is connector-agnostic. Right now it reads Gmail. But the triage logic is the same regardless of source. Swap in Slack, Discord, Linear — the filtering, categorisation, interview, and response drafting all stay identical. The skill triages messages, not email specifically.

---

## Skill 5: /codex-consult

> [SCREEN RECORDING — Claude Code terminal with codex output]

Last one..

I'm using OpenAI inside Claude Code.

Codex-consult wraps the OpenAI Codex CLI and gives me three modes. Mode one: code review — it runs an independent diff review with a pass/fail gate. Mode two: challenge — adversarial mode where it actively tries to break my code. Finds edge cases, race conditions, security holes. Mode three: consult — ask it anything, with session continuity so you can have a back-and-forth conversation.

> [SHOW — codex challenge output with thinking traces]

Here's a real challenge run. You can see the thinking traces — codex is reasoning through the code, checking for failure modes. It found a race condition in a webhook handler that Claude missed entirely. Not because Claude is worse — because they have different blind spots.

And that's the whole point. Different models are trained on different data with different architectures. They have different failure modes. When two models independently agree something is fine, I trust it. When they disagree — that's exactly where the bugs are.

After a review, it shows a cross-model comparison. "Both found X. Only Codex found Y. Only Claude found Z. Agreement rate: 60%." That 40% disagreement is pure signal. That's where I focus my attention.

Everything runs in read-only mode — codex can't modify files. It just reads the diff, reasons about it, and reports back. And it uses maximum reasoning effort so it's thinking as hard as it can.

I covered this in detail in my Claude Code masterclass — the convergence concept. You're not replacing one model with another. You're using model diversity as a debugging tool.

---

## Outro

A spec interview that runs without me in the room. A design tool that generates 10 implementations instead of one mockup. Diagrams that catch architectural bugs visually. A triage skill that reads my inbox and knows my project context. A second opinion from a rival AI.

These aren't coding tools. They're thinking tools.

Skills aren't markdown files. They're how you think, encoded. And if you want to build skills like these — or just steal mine — I cover all of it in my Claude Code masterclass. Link below.
