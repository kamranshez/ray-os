---
duration: "5-9 min"
batch: 3
order: 1
batch_name: "Techniques"
class: "techniques"
chapter: "Advanced Techniques"
---

# Task-Shaped Wrappers: Mixing Deterministic Code with LLMs

Don't let the LLM do everything. Wrap its chaos in deterministic code that handles the predictable parts — git operations, file scaffolding, deployment steps — and only hand the LLM the fuzzy, judgment-heavy slice.

## Prep
- Read Stripe Minions Part 2: https://stripe.com/blog/minions-part-2
- Look up Supabase's approach to constraining agents

## What to Cover

### 1. The Problem
- LLMs are unreliable at deterministic tasks (git workflows, file system operations, structured outputs)
- Letting the agent freestyle everything means more failures, more retries, more wasted context
- The instinct is to prompt harder — the real fix is to remove the decision from the LLM entirely

### 2. The Pattern: Task-Shaped Wrappers
- Write deterministic scripts that handle the predictable parts
- Hand the LLM only the parts that require judgment (analysis, code generation, review)
- The wrapper is the "shape" of the task — the LLM fills in the blanks

### 3. Example: Block Git, Script It Instead
- You don't want the agent touching git at all
- Use a **PreToolUse hook** to block any Bash command involving `git`
- Write a Python script that handles the entire git workflow (branch, commit, push, PR)
- The agent calls the script — deterministic, predictable, no improvisation

### 4. Layered Defence: Block the Escape Hatch
- What if the agent tries to write its own Python script to work around the block?
- Use a **PostToolUse hook** on file writes — if it creates a `.py` file or a Bash command mentions `python`, block it
- Now the agent *must* use your provided scripts — no freelancing

### 5. Real-World References
- **Stripe Minions** — one-shot coding agents that use deterministic orchestration around LLM steps
- **Supabase** — constrained agent architecture

### Key Insight
> The best agent architectures aren't "let the LLM do everything." They're deterministic pipelines with LLM-shaped holes — you control the flow, the model fills in the thinking.
