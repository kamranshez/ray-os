---
duration: "8-10 min"
order: 19
class: "skills"
chapter: "Quality Control"
status: "new"
---

## Self-Improving Skills (Feedback Loops)

Nobody else teaches this. Skills that learn from every interaction and get better over time.

### Core Concept

"Your skills should learn from every interaction and get better over time. But to do this, you need one critical piece: a feedback loop." (7 Levels)

### The Learnings File

Add a `learnings.md` or `rules` section that accumulates what works and what doesn't.

"Maybe you're running the skill and the article it produces ranks on page one within a week. You can go back and note exactly what worked: 'articles that open with a direct answer to the search query in the first paragraph seem to get picked up in AI search more quickly.'" (7 Levels)

### The Wrap-Up Skill

Build a skill that runs at end of every session and auto-captures feedback:

"At the end of every session, we close the session and any skill we've used and any feedback we've been given will be generated and input directly into this learnings.md file on a skill-by-skill basis." (7 Levels)

The wrap-up skill checks: "Did the article actually answer the search query in the first 100 words? Did it include structured data patterns from the reference file? If not, it logs it automatically." (7 Levels)

### What to Show

1. Add a `rules` section to a skill.md that reads from learnings.md
2. Run the skill, notice something good → add to learnings
3. Build the wrap-up skill
4. Show output quality improving over 3 iterations without manual eval runs

### The Pruning Caveat

"The key thing is keeping the learnings file under control. You can't just dump random notes in there forever or it becomes its own context window problem. So every week, go through the learnings file and strip out surplus information." (7 Levels)

### Connection to Evals

"This connects straight back to level five because you can use your evals to validate that the learnings are actually improving output quality. Run the same eval before and after learnings are applied." (7 Levels)
