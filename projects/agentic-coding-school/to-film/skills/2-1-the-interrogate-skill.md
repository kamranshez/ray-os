---
class: "skills"
chapter: "Your First Skill"
status: "new"
tags: [course, script, skills]
lesson: "2.1 The Interrogate Skill"
---

## The Interrogate Skill — Your First Build

So we've got our workspace set up. Skill Creator's installed, the global profile setting is in place. Now we're going to build our first skill from scratch. And I picked this one deliberately because it's the simplest possible skill you can build — about 30 lines — but it's also probably the highest-ROI skill you'll ever make.

It's called the interrogate skill. And what it does is force Claude to interview you before it does anything.

### The Problem (0:00–1:30)

Here's what normally happens. You open Claude, you type something like "help me plan a marketing campaign." And Claude just... goes. It immediately starts writing a plan. Five bullet points. Generic advice. "Define your target audience. Set a budget. Choose your channels."

> [SCREEN: Claude Code terminal — type "help me plan a marketing campaign"]

And the output is fine. It's not wrong. But it's useless. Because Claude doesn't know anything about your business. It doesn't know your budget, your audience, your timeline, what you've tried before, what worked, what didn't. It's giving you the same plan it would give anyone.

> [SHOW: the generic marketing plan output]

And this is the number one reason people think AI doesn't work for them. They give Claude bad input and blame it for bad output. The problem isn't Claude. The problem is that you skipped the most important step — giving it the context it needs.

### What the Interrogate Skill Does (1:30–2:30)

The interrogate skill fixes this by putting a gate in front of every task. Before Claude does anything, it has to ask you questions first. Not one or two questions — it walks down every branch of the decision tree. It explores edge cases. It keeps asking until it has enough context to actually do the job well.

Think of it like hiring a consultant. A bad consultant takes your one-sentence brief and disappears for a week. A good consultant spends the first meeting just asking questions. "What does success look like? What have you tried? What are the constraints I should know about?" The interrogate skill turns Claude into that second consultant.

### Building It By Hand (2:30–5:00)

Now, we could use Skill Creator for this — and we will for the next skill. But for your first build, I want you to see exactly what a skill file looks like. There's no magic. It's just text.

> [SCREEN: text editor — new file]

I'm going to create a new file. In Co-work, you'd go to Customize, Skills, hit the plus button, and upload this when we're done. In Claude Code, you'd save this to your `.claude/skills/` folder.

> [TYPE: creating the file]

```yaml
---
name: interrogate
description: >
  Before executing any task, interview the user thoroughly to gather
  context. Triggers on any request where Claude would normally jump
  straight to output. Use this skill whenever the user gives a task,
  a project, a question, or a request that would benefit from
  clarification first.
---
```

That's the frontmatter — the name and description. Remember from the last lesson, this is what Claude always has loaded. It reads this to decide whether to use the skill.

Now the actual instructions:

```markdown
# Interrogate

Before doing any work on a task, conduct a thorough interview.

## Process

1. Read the user's request carefully.
2. Identify what information you'd need to do this task exceptionally well
   — not just adequately.
3. Ask at least 5 clarifying questions. Walk down each branch of the
   decision tree. Cover:
   - Goals and success criteria
   - Constraints (budget, timeline, technical limits)
   - Context (what they've tried, what worked, what failed)
   - Audience or stakeholders
   - Edge cases and potential problems
4. Wait for answers before proceeding.
5. If the answers reveal new branches, ask follow-up questions.
6. Only begin the actual task once you have sufficient context.

## Rules
- Never skip the interview to "save time." The interview IS the time-saver.
- Ask questions in a natural, conversational way — not as a numbered checklist.
- If the user says "just do it" or wants to skip, do a condensed version:
  ask the 3 most critical questions only.
```

That's it. About 30 lines. No scripts, no reference files, no assets. Just instructions in plain text.

> [SHOW: the complete file]

### Testing It — Without vs With (5:00–7:30)

Now here's where it gets good. I'm going to run the same prompt twice — once without the skill, once with it — so you can see exactly what changes.

> [SCREEN: Claude Code terminal — fresh session, no skill loaded]

Without the skill. Same prompt as before.

> [TYPE: "Help me plan a marketing campaign for my new product launch"]

And Claude just starts writing. Here's your marketing plan. Step one, step two, step three. Generic. Surface level. It doesn't ask me a single question.

> [SHOW: the output — generic plan]

Now with the skill loaded.

> [SCREEN: new session with the skill active]

Same exact prompt.

> [TYPE: "Help me plan a marketing campaign for my new product launch"]

And watch what happens. Instead of jumping to a plan, Claude starts asking questions.

> [SHOW: Claude asking questions — "What's the product? Who's the target audience? What's the budget range? When does it launch? Have you done campaigns before — what worked?"]

It's interviewing me. And these aren't random questions — they're the questions a marketing strategist would ask. The skill told Claude to walk down each branch of the decision tree, and that's what it's doing.

Now I answer these. And this is the part that takes real effort — maybe 10, 15, 20 minutes depending on how much context you give. But here's the thing. That 20 minutes is the actual work. That's you transferring your knowledge to Claude. Every minute you spend here saves you hours of re-prompting and fixing bad output later.

> [SHOW: answers typed out, then the resulting plan]

And now look at the output. Same prompt, completely different result. The plan references my specific budget. It accounts for my timeline. It suggests channels that match my audience. It flags risks I actually need to worry about.

> [SPLIT: left — generic plan without skill | right — contextualized plan with skill]

Not even close. Same prompt. The only difference is 30 lines of instructions that said "ask questions first."

### Why This Skill Is Special (7:30–8:30)

Now here's what makes this different from every other skill we'll build in this class. The interrogate skill isn't about one workflow. It doesn't generate invoices or write LinkedIn posts or scan receipts. It makes every other skill better.

When you chain it with a content skill — better content, because Claude knows your voice and audience before it starts writing. When you chain it with a research skill — better research, because Claude knows what you're actually looking for. It's a multiplier on everything else.

And the other thing — you just built a skill by hand. You saw the frontmatter. You saw the instructions. There's no magic. It's a markdown file with a name, a description, and instructions. Every skill in this class follows that same structure. We're going to use Skill Creator for the more complex ones, but now you know what's actually inside.

### What's Next

Now that you've built the simplest skill by hand, we're going to use Skill Creator to build something more complex — a research skill that can find trending topics, summarize them, and give you actionable briefs. That's where Skill Creator really shines, because it'll interview you, draft the skill, and then test it automatically.
