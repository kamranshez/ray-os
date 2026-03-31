---
duration: "7-10 min"
order: 2
class: "skills"
chapter: "The Blank Slate"
status: "new"
---

## How Skills Actually Work Under the Hood

The "how does it load" explanation nobody does well. Gives viewers a mental model they can't get anywhere else.

### Core Concept — Progressive Disclosure for Skills

Three tiers of information loading:

**Tier 1: YAML Front Matter (always loaded)**
- Just the name and ~100-word description, ~100 tokens per skill
- This is how Claude decides whether to use the skill
- "This sheet of paper that Claude Code always has access to lists the skill's name and a short description." (Chase)
- "The only thing that's loaded into the initial prompt is the YAML front matter. Think of it as a name and description — the summary." (7 Levels)

**Tier 2: skill.md Body (loaded on activation)**
- The full process instructions — step 1, step 2, etc.
- "Claude isn't going to load the skill.md file until it knows it's going to use that skill from reading the description." (7 Levels)

**Tier 3: References/Scripts/Assets (loaded on demand)**
- Claude only pulls these when a specific step needs them
- "In the run-the-research step where it says 'the script/last-30-days script should be run' — it then runs that script and pulls it from the reference file only when it's necessary." (7 Levels)

### What to Show

Use `/context` to make the invisible visible:
1. Show token usage BEFORE any skill triggers
2. Give a prompt that triggers a skill — show tokens jump when tier 2 loads
3. Show tokens jump again when a reference file loads during a specific step
4. From Forked Contexts video: "Use the /context command before and after running a skill to see how many tokens were added to the main session."

### Key Numbers

- **15,000 character limit** for the total skill descriptions list (all tier 1 combined). "Don't install too many skills or you'll run out of space and bloat your context right off the start." (7 Levels)
- This is why 500 skills kills you — even if each description is only 30 characters, 500 x 30 = 15,000. Full.
- "Load in 1,000 skills, you're not only taking up valuable context, but you'll likely have crossover skills that start to cannibalize each other." (1% framework)

### The "Sheet of Paper" Analogy

Chase explains it well: "You have five skills loaded. Each could be thousands of tokens. But Claude has a sheet of paper listing just the name and description. When you say 'I want to design the front end,' it checks the sheet, finds front-end design, and loads THAT skill. Now it has full context."

### Why This Matters

"Skills use progressive disclosure. This is a concept you need to understand because it comes up again and again." (7 Levels) — Foundation for everything in Chapter 2 (200-line rule, reference files, descriptions).

### Cross-Links

- [[Progressive Disclosure]] (context-engineering class) — the general principle
- [[Forked Contexts for Skills]] (claude-code class) — mention context forking, cover in Ch 6
