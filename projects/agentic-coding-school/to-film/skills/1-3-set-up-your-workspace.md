---
duration: "5-7 min"
order: 3
class: "skills"
chapter: "The Blank Slate"
status: "new"
---

## Set Up Your Workspace

Setup checklist — do it once, never think about it again.

### Step 1: Install Skill Creator

- Customize → Skills → scroll to Anthropic examples → toggle Skill Creator ON
- "The skill creator skill is an official Anthropic skill. It's what we are going to use to create new skills, but it can do more — modify, improve, measure performance, run evals, benchmarks." (Chase)

### Step 2: The Global Profile Setting Hack

Settings → General → Profile. Add this one line:

> "Always consider using the most appropriate skill when answering a query or responding."

"You can build the perfect skill, structure everything the right way, add all your reference files, and Claude just doesn't use it. The reason is Claude needs to be told to look for your skills. Without that instruction, they just sit there." (Brand DNA video)

Two separate creators independently flag this as critical. Do this BEFORE building any skills.

### Step 3: Understand Scope

- `~/.claude/skills/` = **user scope** — every project, forever
- `.claude/skills/` (in project) = **project scope** — only this project, shared with collaborators
- "If we do install-for-you (user scope), this skill is on Claude's list all the time. If it's just in this repo, it's a skill for a specific project." (Chase)

**The compounding principle**: "Make sure what you build compounds. I want this skill to be useful for any outdoor project going forward so I don't have to rebuild it each time." (Lenny)

### Step 4: Know the Install Methods

1. **Marketplace**: `/plugin` → search → install
2. **GitHub CLI**: `npx skills add <repo> -d-skill <name>` (add `-d-local` for project scope)
3. **Manual upload**: Customize → Skills → + → Upload. Simple .md for single-file skills. **Zip file for skills with scripts/ or assets/ folders** — "You need to compress that into a zip file to get it to upload effectively." (Lenny)
4. **From another creator**: They send you the .md or .zip, you upload

After any install: `/reload plugins` to activate.

### Step 5: Domain Allow List

"One quick thing — in capabilities settings, switch your domain allow list to all domains." (Lenny) — Useful for skills that search the web or access external APIs.

### Step 6: Pick Your Build Project

For this class, pick a real business or project to build around. All skills in subsequent chapters serve this project.

### Cross-Links

- [[Creating Skills]] (claude-code class) — covers file creation mechanics in detail
