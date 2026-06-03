---
class: "skills"
chapter: "Make It Yours"
status: "new"
tags: [course, script, skills]
lesson: "3.2 Refactoring a Marketplace Skill"
---

## Refactoring a Marketplace Skill

You don't have to build everything from scratch. There are hundreds of thousands of skills out there — marketplaces, GitHub repos, company-specific skills from Stripe and CloudFlare and Vercel. The ecosystem is real.

But here's the problem. Most of them are badly built. The content inside is often excellent — solid business logic, useful processes, real expertise. But the structure is wrong. Everything's dumped into one massive skill.md with no reference files, no progressive disclosure. And that means the moment you activate one of these skills, it floods your context window.

So in this video, I'm going to grab a popular marketplace skill, show you exactly what's wrong with it, and refactor it live.

### Finding the Skill (0:00–1:30)

There are a few places to find skills.

> [SCREEN: browser — skills marketplace]

**skills.mpp.com** has over 280,000 skills indexed from GitHub. You can search by category — marketing, development, operations, whatever. **skillhub.com** has about 7,000 that have been AI-evaluated for quality. And a lot of individual creators publish skill repos on GitHub — some with thousands of stars.

For this demo, I'm going to grab a marketing skill from a popular repo. It's an AI SEO skill — it audits content for how well it'll show up in AI search results. Good use case. Lots of domain knowledge inside.

> [SCREEN: terminal]

> [TYPE: npx skills add <repo> -d-skill ai-seo -d-local]

That installs it locally into our project. Now let me look at what we got.

### The Diagnosis (1:30–3:30)

> [SCREEN: the installed skill folder in file browser]

One file. Just skill.md. No references folder. No scripts. No assets. Everything is in one place.

> [SCREEN: skill.md open in editor — scrolling through]

And it's about 400 lines long. Now, the content is good. It's got an AI visibility audit checklist. Authority signal guidelines. Content type optimization rules. Platform-specific recommendations. This is real expertise — someone put thought into it.

But it's all in one file. Which means the moment this skill activates, Claude loads all 400 lines into context. Even if you're only doing a simple title tag audit, it's loading the entire content type optimization guide and the authority signals framework and everything else.

Let me show you the cost.

> [TYPE: /context]

> [SHOW: context usage with the skill loaded — highlight the token count from the skill]

See that? That's the token cost of having this skill active. It's eating a meaningful chunk of context just sitting there. And if you've got other skills loaded too, this adds up fast.

Now here's the question to ask about every section in this file: does Claude need to see this immediately to know when and how to use the skill? If the answer is yes, it stays in skill.md. If the answer is no, it moves to a reference file.

The process steps — yes, Claude needs those immediately. The audit checklist — yes, that's the core workflow. But the detailed authority signals guide? That's reference material for one specific step. The content type optimization rules? Same thing. The platform-specific recommendations? Only relevant for specific platforms.

### The Refactor (3:30–6:30)

I'm going to use Skill Creator to do this refactor. It's faster than doing it by hand and it makes good decisions about what to split.

> [SCREEN: terminal]

> [TYPE: /skill-creator]

> [TYPE: "Take the ai-seo skill and refactor it. Keep skill.md under 200 lines — only the process steps and core workflow. Move all detailed knowledge into a references/ folder. Create separate reference files for each domain of knowledge."]

Skill Creator reads through the 400-line file and figures out what's process and what's knowledge.

> [SHOW: Skill Creator working — identifying sections to extract]

It's pulling out four distinct knowledge domains. Authority signals — how to build credibility for AI citations. AI visibility audits — the detailed checklist criteria. Content type optimization — rules for different content formats. And platform-specific guidelines.

> [SHOW: the refactored structure — skill.md + references/ folder with 4 files]

Done. The skill.md went from 400 lines to 148. That's a 63% reduction. And it created four reference files in a new `references/` folder.

Let me look at what the skill.md looks like now.

> [SCREEN: refactored skill.md in editor]

Clean. Step one — parse the URL and fetch the page. Step two — run the AI visibility audit, reference the detailed checklist in `references/ai-visibility-audit.md`. Step three — evaluate authority signals, reference `references/authority-signals.md`. Step four — check content type optimization, reference `references/content-type-optimization.md`. Step five — compile the report.

Each step points to its reference file. Claude only loads a reference when it reaches that step. The detailed knowledge is still there — it's just not all loaded at once anymore.

Now let me also fix the description. It's vague — something like "helps with SEO." Let me apply the three-part framework from the last chapter.

> [TYPE: rewriting the description with triggers, not-triggers, and outcome]

And add guardrails at the bottom of skill.md.

> [TYPE: adding the standard guardrail rules]

Now let me check the context cost again.

> [TYPE: /context]

> [SHOW: context usage — noticeably lower than before]

Same skill. Same knowledge. But now it's only loading what it needs for the step it's on. The base cost on activation is way lower because skill.md is 148 lines instead of 400.

### The Refactoring Checklist (6:30–7:30)

Any time you install a marketplace skill, run through this checklist before you use it.

> [SCREEN: the checklist on screen]

**One — is skill.md under 200 lines?** If not, extract knowledge sections into reference files. Process stays. Knowledge moves.

**Two — does the description have trigger, not-trigger, and outcome?** If it's a vague one-liner like "helps with SEO" — rewrite it. You know how from the descriptions video.

**Three — are there guardrails?** If not, add the standard ones. "Only load relevant reference files. Ask before proceeding if unclear. Keep responses concise."

**Four — does it have a references folder?** If everything is in one file, that's your biggest win. Split it.

You can do this manually or use Skill Creator to do the split for you. Either way, five minutes of refactoring turns a context-hungry mess into a lean, well-structured skill.

### The Bigger Picture (7:30–8:30)

Skills are becoming a new layer of software. A well-built skill can replace what used to be a dedicated SaaS tool. There are already marketplaces with hundreds of thousands of them, and companies like Stripe and CloudFlare are publishing official skills for their platforms.

But the quality is uneven. The best marketplace skills are excellent. The average ones have good ideas trapped in bad structure. Now you know how to tell the difference — and how to fix it.

And here's a thing to keep in mind. Once you refactor a skill and add your brand context from the previous lesson, it's not really a marketplace skill anymore. It's yours. You've shaped it to your structure, your voice, your workflow. That's the pattern for the rest of this class — take what exists, make it yours, then build on it.

### What's Next

We've been adding context and refactoring structure. In the next video, we go deeper — encoding your actual professional expertise into a skill. Not brand voice or visual style, but your judgment. The things that take a human years to learn. That's where skills get genuinely powerful.
