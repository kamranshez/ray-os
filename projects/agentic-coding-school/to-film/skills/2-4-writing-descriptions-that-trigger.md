---
duration: "5-7 min"
order: 7
class: "skills"
chapter: "Your First Skill"
status: "new"
tags: [course, script, skills]
lesson: "2.4 Writing Descriptions That Actually Trigger"
---

## Writing Descriptions That Actually Trigger

So we've built skills. We know the folder structure. We know the 200-line rule. But there's one piece we haven't touched yet — and it's the piece that determines whether Claude even uses your skill in the first place. The description.

And the numbers here are bad. The average marketplace skill triggers about 20% of the time. One in five. You build the perfect skill, and four out of five times Claude just ignores it. So this video is about fixing that.

### The 20% Problem (0:00–1:30)

Remember from the progressive disclosure video — tier one is the YAML front matter. The name and description. That's all Claude sees when it's deciding whether to use a skill. The body doesn't load yet. The reference files don't load yet. Claude is making a decision based entirely on that short description.

And most descriptions are terrible. They're written like README summaries — "A comprehensive tool for content research and analysis." That tells Claude almost nothing about when to use it.

So Claude reads that, reads your prompt, and goes "eh, doesn't seem relevant" — and just does the task itself without the skill. You'd never know. The skill was right there, ready to help, and it got skipped because the description was too vague to match.

I'm going to show you this. And then fix it.

### The Test — Before (1:30–2:30)

> [SCREEN: the research skill from the previous lesson, description open in editor]

Here's our research skill. I'm going to give it a bad description on purpose.

```yaml
description: "Helps with research tasks."
```

Four words. Vague. Now I'm going to run five different prompts and count how many times the skill actually triggers.

> [TYPE: "What's trending in AI tools this month?"]

> [SHOW: Claude's response — no skill triggered, just a generic answer]

No skill. It just answered from its own knowledge.

> [TYPE: "Research the latest changes to Claude Code"]

> [SHOW: skill triggered this time]

That one worked — probably because I literally said "research."

> [TYPE: "Find me some topics I could make videos about"]

> [SHOW: no skill triggered]

Nope. I said "find me topics" not "research." Claude didn't make the connection.

I ran five prompts. The skill triggered twice. Two out of five. That's 40%, and I was being generous with my wording. With more natural phrasing, it'd be worse.

### The Three-Part Framework (2:30–4:00)

Here's how to fix it. Every description needs three things.

**One — triggers.** What words, phrases, or situations should activate this skill? Be specific. List the actual things a user would type.

**Two — not-triggers.** What should NOT fire this skill? This is the part everyone skips. If you don't tell Claude what to exclude, it'll either fire on everything vaguely related or nothing at all.

**Three — outcome.** What does the skill produce? This helps Claude decide if the skill is relevant to what the user actually wants.

Let me rewrite this description.

> [SCREEN: editor — rewriting the description]

```yaml
description: >
  Research any topic and produce a structured brief with TLDR,
  key facts, pros/cons, sources, and a relevance score.
  Triggers on: research, trending, what's new in, find me topics,
  what should I cover, competitor analysis, industry update.
  Does NOT trigger for: simple web browsing, reading a single URL,
  fetching a specific document, or answering factual questions
  Claude already knows.
  Produces: a research brief in markdown with actionable verdict.
```

Trigger words. Exclusions. Output description. Now Claude knows exactly when to use it, when not to, and what it'll produce.

### The Test — After (4:00–5:00)

Same five prompts. Same skill. New description.

> [TYPE: "What's trending in AI tools this month?"]

> [SHOW: skill triggers — "trending" matches]

Got it. "Trending" is in the trigger list.

> [TYPE: "Find me some topics I could make videos about"]

> [SHOW: skill triggers — "find me topics" matches]

Got it. Before this one failed. Now it works because "find me topics" is explicitly listed.

> [TYPE: "What's 2 + 2?"]

> [SHOW: no skill triggered — correctly ignored]

And that correctly didn't trigger. Simple factual question — the not-trigger list keeps it out.

Four out of five triggered. The one that missed was borderline phrasing. That's a jump from 40% to 80% — from a description change alone.

### The Three Invocation Modes (5:00–5:45)

Now, even with a perfect description, you won't hit 100% with natural language. There are actually three ways to invoke a skill, and you should know all of them.

**Mode one — natural language.** "Research what's trending." You're relying on Claude to match your words to a skill description. This works 60-85% of the time with a good description. It's the most convenient but least reliable.

**Mode two — explicit mention.** "Use the research skill to find trending topics." You're telling Claude which skill to use. Much more reliable.

**Mode three — slash command.** `/research` — or whatever the skill's name is. This guarantees it. 100%. Claude doesn't decide anything — you're forcing it.

My default is mode three for skills I know I want. Slash command. No ambiguity. But when I'm working naturally and want Claude to pick the right skill on its own, modes one and two with a good description handle it.

### The Reliability Stack (5:45–6:15)

And here's how all of this fits together. Three layers of trigger reliability:

**Layer one** — that global profile setting from the setup video. "Always consider using the most appropriate skill." This is the foundation. Without it, Claude doesn't actively check skills.

**Layer two** — a good three-part description. Trigger words, not-triggers, outcome. This helps Claude pick the right skill.

**Layer three** — slash invocation when you want certainty.

All three together is how you get skills that reliably fire. Skip any layer and you'll wonder why your skills aren't being used.

### What's Next

You can now build skills from scratch, structure them properly, and write descriptions that actually trigger. In the next video, we're going to look at something you might not have thought of — you probably already have skills inside your business. Playbooks, templates, review checklists, process documents. We're going to take one of those existing documents and turn it into a skill.
