---
duration: "1-4 min"
batch: 2
order: 2
batch_name: "Bonus Techniques"
class: "techniques"
chapter: "Advanced Techniques"
---

# Pass agents

## Use two-pass agents for reliability

**Implication:** Single-pass generation drops constraints; a second pass catches misses.

- Pass 1: generate solution
- Pass 2: a "compliance checker" prompt: "Check against requirements; list violations; patch."

This is basically unit tests for instruction following.

[ChatGPT - Branch · Recent Instruction Following Research](https://chatgpt.com/share/696b3203-f6f0-8006-99a8-05c7eca5ce59)

---

**Fewer global rules, more staged constraints**

Split into phases:
- Phase A: "Generate a clean solution that passes tests."
- Phase B: "Now refactor to match style X and naming Y."
- Phase C: "Now optimize."

You'll get higher overall success than dumping everything at once.
