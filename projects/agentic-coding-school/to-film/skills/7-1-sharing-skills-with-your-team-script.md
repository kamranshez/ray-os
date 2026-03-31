---
tags: [course, script, skills]
status: draft
lesson: "7.1 Sharing Skills with Your Team"
duration: "7-10 min"
---

## Sharing Skills with Your Team

Everything we've built in this class so far has been for you. Your skills, your brand context, your system. But skills become dramatically more valuable when you share them. Because the thing that takes years of mentorship to transmit — your judgment, your process, your standards — is now a file that works from the first use.

### The Mentorship Problem (0:00–1:30)

In most businesses, senior expertise transfers through osmosis. A new hire shadows someone for months. They pick up how things work through feedback loops, corrections, and institutional memory. It takes a long time. And it's fragile — when the senior person leaves, a lot of that knowledge goes with them.

Zack Shapiro, the lawyer we've referenced throughout this class, describes it this way: "The plugin is transferable. If I had 50 associates, I could install it on every machine. Every associate would immediately produce contract reviews using my analytical framework, draft communications in my voice, and apply tracked changes in my preferred format."

That's the promise. Knowledge that takes years to transmit, compressed into an instruction file. Install it, and the new person is operating at a higher level from day one.

Not at your level — skills don't replace judgment. But the starting baseline goes up. The output still requires human review, but that review starts from a much higher quality floor.

### Three Ways to Share (1:30–4:00)

There are three distribution methods depending on your team's technical level.

**Method one — Git repo.** For technical teams.

> [SCREEN: a git repository with a .claude/skills/ folder]

If your skills live in the project's `.claude/skills/` folder and you commit them to the repo, anyone who clones the repo gets the skills automatically. They show up in Claude the moment the person starts a session in that project. No manual install.

This is the cleanest approach for development teams. Skills travel with the codebase. Updates go through pull requests. Everyone's always on the latest version.

**Method two — Plugin bundles.** For non-technical teams.

> [SCREEN: Co-work — Customize → Plugins → Add plugin]

You package your skills into a zip file — all the skill folders bundled together. Share the zip. The recipient goes to Customize → Plugins → Add plugin → upload the zip. All the skills install at once.

This is how creators share skill packs. One download, one upload, everything's active. No terminal, no git, no technical setup.

**Method three — Managed settings.** For enterprises.

If you're deploying across an organization's Claude accounts, there's a `managed-settings.json` configuration that lets admins push skills to every user. Skills appear automatically — nobody has to install anything. If you're operating at enterprise scale, this is how you'd do it.

### The Consistency Demo (4:00–5:30)

Now let me show you why sharing matters beyond just convenience.

> [SCREEN: two Claude sessions side by side]

I'm going to give the same task to two Claude instances. One has the contract review skill we built in Chapter 3. One is vanilla — no skills.

> [TYPE: same prompt in both — "Review this services agreement"]

> [SPLIT: left — vanilla Claude output | right — skill-equipped Claude output]

Left side — each session, each person gets slightly different output. Different structure. Different emphasis. Inconsistent quality. One person's review might catch the liability issue, another's might miss it.

Right side — same skill, same criteria, same output structure every time. Red flags, yellow flags, missing terms, verdict. Regardless of who runs it. That's consistency across a team.

And this is the subtle power of skills in a team context. It's not just that individual output is better — it's that team output is consistent. Everyone reviews contracts the same way. Everyone formats proposals the same way. Everyone follows the same process for the same task.

### The Quality Floor (5:30–6:30)

Now, I want to be careful here. Skills don't replace review. A new hire using your contract review skill still needs a senior person checking the output. What changes is what they're reviewing.

Without skills — you're reviewing a first draft that might be structured wrong, might miss categories entirely, might not follow your firm's format. You're doing heavy editing.

With skills — you're reviewing output that follows the right structure, checks the right provisions, and uses the right severity framework. You're doing light editing.

The floor is higher. The ceiling is still human judgment. But the gap between a junior person's output and a senior person's output gets much smaller. And that changes the economics of your team — or, as we'll talk about in the next video, changes what you can sell.

### Using the Customizer (6:30–7:00)

And remember the customizer from Chapter 5? This is where it shines for teams. You share one plugin with five people. Each person runs `/customize` once — adapts the voice settings, the formatting preferences, whatever's personal. They get a version that matches their style while following the same process.

One skill, many personalized instances. Shared process, individual voice.

### What's Next

In the final video of this class, we go from sharing skills with your team to selling them to someone else's team. The system you've built is what businesses are paying five figures for. That's next.
