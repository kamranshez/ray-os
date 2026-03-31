---
tags: [course, script, skills]
status: draft
lesson: "1.1 Why Skills Change Everything"
duration: "5-7 min"
---

## Why Skills Change Everything

So this class is about skills. And the simplest way I can explain what a skill does is this — Claude without skills is like a smartphone without apps. It works. You can make calls. But you're using maybe 10% of what it can actually do. Skills are the other 90%.

And I'm going to prove that to you right now with two examples before we talk about anything else.

### The Before and After (0:00–2:00)

> [SCREEN: Claude Code terminal]

I'm going to type a simple prompt. "Build me a landing page for a SaaS product."

> [TYPE: "Build me a landing page for a SaaS product"]

And here's what Claude gives me without any skills loaded.

> [SHOW: the generated landing page — generic, purple gradient, rounded cards on white, Inter font]

It's... fine. It works. But it looks like every other AI-generated website you've ever seen. Purple gradients. Rounded cards on white. Inter font. If a thousand people typed the same prompt, they'd get roughly the same thing back. Because without anything steering it, Claude defaults to the most common pattern across all its training data. This is what people call AI slop.

Now. Same exact prompt. But this time I've got the front-end design skill loaded.

> [SHOW: the generated landing page with skill — distinctive typography, intentional color, no generic patterns]

Different. The skill tells Claude how to think about design before it writes a single line of code. It considers purpose, tone, constraints. It has guidelines for typography — avoid generic fonts, choose distinctive pairings. It has rules for color, motion, composition. And it explicitly bans the slop — no purple gradients, no rounded cards on white, no Inter font everywhere.

> [SPLIT: left — without skill | right — with skill]

Same prompt. Same model. The only difference is a text file with instructions. That's a skill.

Now here's a completely different example. I type "review this contract."

> [SPLIT: left — generic contract review | right — skill-encoded review with severity ratings, red flags, yellow flags, counter-language]

Left side — generic. It reads the contract and gives me a summary. Right side — same contract, but now it's severity-rated. Red flags for things that could hurt me. Yellow flags worth reviewing. Missing terms. A bottom-line verdict — sign, negotiate, or walk. And specific counter-language for each high-severity issue.

That's not a prompt trick. That's years of a lawyer's judgment encoded into a file that now fires every time.

### What a Skill Actually Is (2:00–3:00)

So what is a skill really? It's a folder with instructions. A markdown file — plain text — that tells Claude how to do a specific thing in a specific way.

Not how to do everything. How to do one thing, well, every time.

Think of it as an SOP — a standard operating procedure. You write it once, Claude follows it every time. You don't re-explain your brand voice. You don't re-describe your review checklist. You don't paste the same prompt over and over. The skill handles it.

And here's the key thing — anything you can prompt, you can turn into a skill. If you've ever typed a really good detailed prompt and thought "I wish Claude would just do this every time without me having to say all of this again" — that's a skill.

### Where Skills Sit — The Instruction Hierarchy (3:00–4:00)

Now, skills aren't the only way to control Claude's behavior. There are multiple layers of instructions, and understanding where skills fit matters.

> [SCREEN: simple diagram showing the layers]

**CLAUDE.md files — the instruction layer.** These are markdown files at different scopes. Your user-level CLAUDE.md at `~/.claude/CLAUDE.md` affects every project — universal preferences. A project-level CLAUDE.md inside a specific folder affects just that project. If you're on an enterprise plan, there's a managed policy CLAUDE.md that your org enforces. These stack — Claude reads all of them.

**Skills — the on-demand layer.** Skills are different from CLAUDE.md files because they're not always loaded. They sit on the side, and Claude pulls them in only when they're relevant to what you're asking. That's what makes them efficient — they don't bloat your context with instructions you don't need right now.

CLAUDE.md files tell Claude how to behave in general. Skills tell Claude how to do specific tasks. They're complementary — and skills are most powerful when the CLAUDE.md files are already set up with your baseline preferences.

One thing to know: skills work in Claude Code — the CLI and the desktop app. They're local files on your machine. For this class, that's where we'll be working.

### The Scope of What's Possible (4:00–5:30)

Now I want to give you a quick sense of range. Because skills aren't just about making landing pages look better.

> [SCREEN: rapid montage of skill outputs]

You can build skills that generate branded invoices — with your logo, your colors, your font, payment terms pre-filled. One sentence and you've got a PDF ready to send.

Skills that build entire slide decks from a brain dump. Skills that research trending topics, score them one to ten, and suggest content angles based on your existing audience.

Skills that plan and script an entire batch of videos — ideation, scriptwriting, publishing calendar — from a single command. Skills that run every morning at 7am and send you a briefing with your calendar, urgent emails, and suggested replies.

Skills that review contracts. Skills that draft proposals. Skills that track your expenses every Friday and generate a dashboard.

And the thing is — each of these is just a folder with instructions. Some are 30 lines. Some are a few hundred. But the principle is the same. You teach Claude once, and it runs that workflow every time.

### The One Line (5:30–6:00)

So here's the frame for this entire class. Skills aren't prompts you save. They're employees you train once.

Over the next 25 videos, we're going to build a complete system — from your first 30-line skill all the way to a full AI operating system with skills that chain together, improve themselves, and run on schedules without you. And at the end, you'll have something you can use for your own business or sell to someone else's.

But none of it works if you don't understand how skills actually load and run under the hood. That's what matters for building them well and not just downloading random ones that half-work.

### What's Next

In the next video, we're going to look at how skills actually work under the hood — the three-tier loading system that makes them efficient, why 500 skills will kill your performance, and what the 15,000 character limit means for you.
