---
class: "skills"
chapter: "The Blank Slate"
status: "new"
tags: [course, script, skills]
lesson: "1.1 Why Skills Change Everything"
---

## Why Skills Change Everything

So this class is about skills. And before I show you what they do, I want to tell you why they matter at a level most people aren't talking about.

$50 trillion. That's what the world spends every year on knowledge worker compensation. And most of that money produces wildly inconsistent output. You know how it works inside companies. There's a process for how things should be done — except the process is outdated, or there are three versions of it, or it's stuck in Sarah's head and Sarah just left for a new job. Someone new comes in, gets onboarded, picks up maybe 60% of how things are supposed to work, and the output is different every time.

Skills fix this. A skill is an SOP — a standard operating procedure — that executes itself. It doesn't forget the process. It doesn't skip steps because it's Monday morning. It runs the same way every time.

Now — this class is not about replacing yourself. There's a capability stack I want you to keep in mind. AI is great at knowledge, understanding, and intelligence — following instructions, adapting to new requirements, connecting patterns. But it has zero desire. Zero ambition. It doesn't see a problem in the world and go "that's not right, we should fix that." That's you. Your job is deciding what to build, why, and for whom. Skills handle the how. You're not the row in the Excel sheet. You're the person who decides what the spreadsheet should calculate.

OK — let me prove what skills actually do with two examples.

> [SCREEN: Claude Code terminal]

### The Before and After

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
