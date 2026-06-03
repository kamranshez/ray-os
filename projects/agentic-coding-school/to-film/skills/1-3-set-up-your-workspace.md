---
class: "skills"
chapter: "The Blank Slate"
status: "new"
tags: [course, script, skills]
lesson: "1.3 Set Up Your Workspace"
---

## Set Up Your Workspace

Now we understand what skills are and how they load. Before we build anything, we need to get the workspace set up. This is a one-time thing — do it now and you won't think about it again.

There are five things to do. Should take about five minutes.

### Step 1 — Install Skill Creator (0:00–1:00)

The first thing we need is the Skill Creator skill. This is an official Anthropic skill that creates other skills. We'll use it heavily starting in lesson five, but I want it installed now so it's ready.

> [SCREEN: Claude Co-work — Customize sidebar]

In Co-work, click Customize — the little briefcase icon. Then Skills. Scroll down past your personal skills to the Anthropic examples section.

> [SHOW: Skill Creator in the list]

There it is — Skill Creator. Toggle it on.

Now this thing does more than just create skills. It can modify existing skills, measure how well they perform, run benchmarks, even do A/B comparisons. We'll get into all of that in Chapter 5. For now, just make sure it's on.

If you're in Claude Code CLI instead of Co-work, you can install it with `/install-plugin` or from the marketplace. Same skill, same result.

### Step 2 — The One Setting That Actually Matters (1:00–2:00)

This is the most important step and the one almost everyone skips.

> [SCREEN: Co-work — user CLAUDE.md file at ~/.claude/CLAUDE.md]

In Co-work, you can add global instructions through the settings. In Claude Code CLI, you'd edit your user-level CLAUDE.md file at `~/.claude/CLAUDE.md`. Either way, you're adding instructions that affect every session across all projects.

Add this one line:

```
Always consider using the most appropriate skill when answering a query or responding.
```

> [TYPE: the line into the Profile field]

That's it. One sentence.

Here's why this matters. You can build the perfect skill — great structure, great description, reference files, the whole thing. And Claude just... doesn't use it. It sits there. The reason is that without this instruction, Claude doesn't actively check its skills list. It'll use a skill if you explicitly invoke it, but it won't proactively look for one on its own.

This one line changes that behavior. It tells Claude to actually scan its available skills on every request and consider whether any of them are relevant. Two completely independent creators discovered this problem and both landed on the same fix. Do this before building anything.

### Step 3 — Understanding Scope (2:00–3:30)

When you install a skill, you have to decide where it lives. And this matters more than people think.

> [SCREEN: file browser showing two paths]

There are two main locations:

**User scope** — `~/.claude/skills/`. This is your personal skills folder. Any skill you put here is available in every project, every session, forever. It's on Claude's menu no matter what you're working on.

**Project scope** — `.claude/skills/` inside a specific project folder. This skill only exists when you're working in that project. And if you commit it to a repo, anyone who clones the repo gets the skill too.

So the question for every skill you build is: do I need this everywhere, or just here?

An invoicing skill? Probably everywhere — user scope. A skill that knows how to deploy your specific app? Project scope — it's useless outside that project.

And here's a principle to keep in mind for this whole class: make what you build compound. If you're building a research skill for a specific project, ask yourself — could I make this general enough to use everywhere? Because a skill that works across all your projects is ten times more valuable than one that only works in one.

### Step 4 — The Four Install Methods (3:30–5:00)

There are four ways to add skills. You'll use all of them at different points.

**Method one — the marketplace.** Type `/plugin` in Claude and you get a searchable marketplace of skills. Find one you want, hit install, choose user or project scope. Done.

> [SCREEN: /plugin marketplace]

**Method two — from GitHub.** A lot of good skills live in GitHub repos. The install command looks like this:

```bash
npx skills add <repo-name> -d-skill <skill-name>
```

> [SCREEN: terminal running the command]

Add `-d-local` at the end if you want it in the current project instead of your user folder.

**Method three — manual upload.** In Co-work, go to Customize → Skills → hit the plus button → Upload. If it's a single markdown file, just upload the .md. If the skill has scripts or assets — multiple files in a folder — you need to zip it first. Co-work expects a zip file for multi-file skills.

**Method four — from someone else.** Someone sends you a .md file or a .zip. You upload it the same way. We'll do this in Chapter 7 when we talk about sharing skills with your team.

After any install, run `/reload plugins` so Claude picks up the new skill.

### Step 5 — Pick Your Project (5:00–5:30)

Last thing. For this class, I want you to pick a real business or project to build your system around. Every skill we build from here on out is going to serve this project. It could be your actual business. It could be a side project. It could be a client's business you want to build a system for.

The point is: don't build skills in the abstract. Build them for something real. That's how you'll actually use them after this class.

### What's Next

Workspace is set up. Skill Creator's installed. The profile setting is in place. Now we build. In the next video, you're going to create your first skill from scratch — by hand, no Skill Creator, just a text file. It's about 30 lines long and it'll immediately make every other skill you build after it more effective.
