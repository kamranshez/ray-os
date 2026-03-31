---
duration: "7-10 min"
order: 6
class: "skills"
chapter: "Your First Skill"
status: "new"
---

## Anatomy of a Well-Built Skill

The architecture video. Dissect the research skill we just built and explain the folder structure.

### The Folder Structure

Every skill is a folder with:
- **skill.md** (required) — the process/SOP. "This is the brain of the skill." (7 Levels)
- **references/** (optional) — documentation, examples, knowledge Claude pulls on demand
- **scripts/** (optional) — executable code for API calls, data processing
- **assets/** (optional) — templates, fonts, icons, logos

"You've got scripts folder for executable code. References folder for documentation that Claude can pull in when it needs it — like examples of what good looks like. Assets folder for templates, fonts, or icons." (7 Levels)

### The 200-Line Rule

skill.md should be max 200 lines. It's a table of contents that points to reference files, not a dump of everything.

"That 200-line limit is not arbitrary. It's based on how much context an LLM can efficiently scan through to decide what to load next." (7 Levels)

**The Reddit cautionary tale**: "This developer had a CloudFlare skill at 1,131 lines, a Shadcn UI skill at 850, and a Next.js skill at 900. Every time Claude activated multiple skills, the context window exploded — loading 5-7K lines every time." (7 Levels)

Result: slowness, drifting from instructions, Claude ignoring obvious parts.

### Point-Don't-Dump

The skill.md says "for content templates, see references/content-templates.md" — Claude loads that file only during the step that needs it, then can unload it.

"Think of the skill.md as a table of contents that tells Claude where to look. The actual detailed documentation goes into your references folder." (7 Levels)

**Visual comparison**: 500-line single-file skill loading into memory vs 100-line skill.md with separate reference files. "When you split context into reference files, Claude only loads what it needs. Creating a social media post? It loads your voice guidelines but skips your visual style guide." (Brand DNA video)

### The Guardrails Section

Every well-built skill.md should end with 3-5 explicit rules:

1. "Only load relevant reference files for the current step"
2. "If guidelines are unclear or information is missing, ask before proceeding"
3. "Keep responses concise — don't over-explain unless asked"
4. "If the task doesn't match this skill's purpose, say so instead of forcing a fit"

From Brand DNA video: "Only three rules — only load relevant reference files, if guidelines are unclear ask before proceeding, keep responses concise. This prevents Claude from overthinking and wasting time."

### What to Show

Take a bloated 400-line marketplace skill.md. Refactor it live:
- Move knowledge sections into reference files
- Keep process steps in skill.md
- Add guardrails section
- Result: 400 → ~150 lines. 4 new reference files. 60% reduction.
- Run `/context` before and after to show token savings
