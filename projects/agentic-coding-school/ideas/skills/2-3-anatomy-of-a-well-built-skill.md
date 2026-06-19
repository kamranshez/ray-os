---
class: "skills"
chapter: "Your First Skill"
status: "idea"
tags: [course, script, skills]
lesson: "2.3 Anatomy of a Well-Built Skill"
---

## Anatomy of a Well-Built Skill

In the last video, Skill Creator built us a research skill. It works. But we went through it fast and I didn't explain why the file is structured the way it is. Now we're going to open it up and look at the architecture — because how you structure a skill determines whether it stays fast and reliable or turns into a context-eating mess.

### The Folder (0:00–1:30)

A skill isn't a file. It's a folder. And that distinction matters more than you'd think.

> [SCREEN: file browser showing the research skill folder]

Here's the research skill we built. The folder has:

**skill.md** — the only required file. This is the brain. The process instructions. Step one, step two, the rules. Think of it as the SOP — the standard operating procedure.

**references/** — optional. This is where you put documentation, examples, templates, anything that Claude might need for a specific step. The key word is "might." This doesn't all load at once.

**scripts/** — optional. Executable code. If your skill needs to call an API, process data, or do something programmatic, the scripts go here.

**assets/** — optional. Templates, logos, fonts, icons. Files used in the output.

Now, the research skill Skill Creator built for us might just be a skill.md with everything in it. And for a simple skill, that's fine. But the moment a skill gets complex, you need to split things out. And here's the rule that tells you when.

### The 200-Line Rule (1:30–3:30)

Your skill.md should be under 200 lines. Max.

This isn't arbitrary. Remember from the progressive disclosure video — when a skill activates, tier two loads. That's the entire skill.md body going into Claude's context. If your skill.md is 200 lines, that's manageable. If it's 1,000 lines, you just ate a massive chunk of your context window in one shot.

And this isn't hypothetical. There's a post on Reddit from a developer who went all in on skills early. He had a CloudFlare skill at 1,131 lines. A Shadcn UI skill at 850. A Next.js skill at 900. Every time Claude activated more than one of these, it was loading 5,000 to 7,000 lines into context. At once.

The result? Slowness. Claude drifting from instructions. Ignoring obvious rules that were right there in the file. Because there was just too much for it to track.

So the rule is: keep skill.md under 200 lines. Anything that's not process instructions — not "do step one, then step two" — goes into a reference file.

### Point, Don't Dump (3:30–5:00)

And this is how you actually do it. Instead of putting everything in skill.md, you point to reference files.

> [SCREEN: skill.md open in editor]

In the skill.md, a step might say:

```markdown
## Step 3: Format the output
Use the output template in `references/output-template.md`.
Apply the scoring rubric in `references/scoring-criteria.md`.
```

Claude reads this step, goes "okay, I need the output template," loads that one file, uses it, and moves on. It never loads the scoring criteria unless a later step needs it. And it never loads your brand voice guide or your source evaluation checklist or anything else in the references folder that this particular step doesn't need.

That's what I mean by point, don't dump. The skill.md is a table of contents. It tells Claude where to look. The deep knowledge lives in reference files and only gets pulled when a specific step calls for it.

> [SPLIT: left — 500-line single file | right — 100-line skill.md + 4 reference files]

Here's what this looks like in practice. On the left, a single skill.md with everything crammed in. 500 lines. All of it loads the moment the skill triggers. On the right, the same content split into a 100-line skill.md and four reference files. Claude loads the 100-line file on activation, then pulls reference files one at a time as needed.

Same knowledge. Fraction of the context cost at any given moment.

### The Guardrails Section (5:00–6:00)

One more thing every skill.md needs. At the bottom, add 3 to 5 rules. I call these guardrails.

```markdown
## Rules
- Only load relevant reference files for the current step.
- If guidelines are unclear or information is missing, ask before proceeding.
- Keep responses concise — don't over-explain unless asked.
- If this task doesn't match this skill's purpose, say so instead of forcing a fit.
```

These seem obvious. But without them, Claude does weird things. It'll preemptively load every reference file "just in case." It'll guess when it should ask. It'll write three paragraphs when a sentence would do. The guardrails keep it efficient and predictable.

Think of it like this — the process instructions tell Claude what to do. The guardrails tell Claude how to behave while doing it.

### Live Refactor (6:00–8:30)

Now I want to show you this in practice. I'm going to grab a popular skill from a marketplace and refactor it live.

> [SCREEN: terminal — installing a marketplace skill]

This is a marketing skill. Let me look at the skill.md.

> [SHOW: the skill.md — scrolling through to show it's ~400 lines]

400 lines. All in one file. No references folder. The content is actually good — it's got useful marketing strategies, categorization systems, example outputs. But it's all dumped into a single file that loads entirely on activation.

Let me check what this costs us.

> [TYPE: /context]

> [SHOW: context usage — note the token count]

Now. I'm going to use Skill Creator to refactor this.

> [TYPE: "Take this skill, keep skill.md under 200 lines, move all detailed reference info into a references/ folder"]

Skill Creator reads through the file, identifies what's process and what's knowledge, and splits them.

> [SHOW: the result — refactored skill.md and new reference files]

The skill.md went from 400 lines to about 150. It created four new reference files — one for marketing categories, one for output templates, one for scoring criteria, one for platform-specific guidelines. That's a 60% reduction in what loads on activation.

Now let me add guardrails at the bottom.

> [TYPE: adding the 4 guardrail rules]

And let me check the context cost now.

> [TYPE: /context]

> [SHOW: context usage — notably lower than before]

Same skill. Same knowledge. Way less context pressure. And now it'll only pull what it needs, when it needs it.

### What's Next

The skill is well-structured now. But there's still one part we haven't touched — the description. And the description is what determines whether Claude even uses the skill in the first place. In the next video, we'll look at why most descriptions fail, the three-part framework that fixes them, and the difference between a skill that triggers 20% of the time and one that triggers 85%.
