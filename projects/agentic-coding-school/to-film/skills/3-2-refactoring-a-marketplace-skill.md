---
duration: "8-10 min"
order: 10
class: "skills"
chapter: "Make It Yours"
status: "new"
---

## Refactoring a Marketplace Skill

Most marketplace skills are badly built. The content is good. The structure isn't.

### The Problem

"A lot of marketplace skills are badly built. 1,000-line skill.md files with no progressive disclosure, everything dumped into one massive markdown document, no references folder, no scripts. Just a wall of text that loads into your context window as soon as the skill is activated." (7 Levels)

"The most frustrating part is the actual content is often really good. The business logic is solid. It's just the structure that's the problem." (7 Levels)

### Where to Find Skills

- **skills.mpp.com** — 280,000+ skills indexed from GitHub, searchable by category
- **skillhub.com** — 7,000+ AI-evaluated skills
- **Company-specific**: Stripe, CloudFlare, Vercel all launching their own skills
- **GitHub repos**: Cory Haynes marketing skills (13,000 stars), etc.

From 1% framework: "Skills are becoming a new layer of software. A well-built skill can do what used to require a dedicated SaaS tool."

### What to Show

1. Find a popular skill (e.g., Cory Haynes AI SEO skill at ~400 lines)
2. Install it: `npx skills add <repo> -d-skill ai-seo -d-local`
3. Run `/context` to see how much it loads on activation
4. Diagnose: "The skill.md is 400 lines. It has some references but most of the knowledge is in the main file."
5. Use Skill Creator to refactor: "Take this skill, keep skill.md under 200 lines, move all reference info into references/"
6. Result: "The skill.md was 400 lines, now it's 148. That's a 60% reduction. Created four new reference files — authority signals, AI visibility audits, content type optimization." (7 Levels)
7. Run `/context` again — show the difference

### The Key Question

For every marketplace skill: "Does Claude actually need to see this immediately to know when and how to use the skill? If yes, it stays in skill.md. Everything else gets moved to references."

### Refactoring Checklist

1. Is skill.md under 200 lines? If not, extract knowledge to reference files.
2. Does the description have trigger/not-trigger/outcome? If not, rewrite it.
3. Are there guardrails at the bottom? If not, add them.
4. Is there a reference folder? If not, create one and move deep knowledge there.
