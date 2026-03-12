---
duration: "10-15 min"
batch: 1
order: 3
batch_name: "Seed Thinking"
class: "prompt-engineering"
chapter: "Steering Models"
---

## Steering Distributions: Changing Where the Model Looks

When you give a model a default prompt, it maps to a distribution based on the training data for that request. Ask for business ideas — you get the training-data distribution of business ideas. Ask it to debug code — it finds the most common debugging problem. The skill is steering away from these default distributions by being specific.

### The Core Idea: Attention Is Zero-Sum

At every layer of processing, the model decides what's relevant. When you say "find bugs," it spreads attention across a huge region of bug-related space — security vulnerabilities, type errors, off-by-one mistakes, race conditions, cost miscalculations, naming conventions — all weighted by how common they are in training data. It'll find things, but it's sampling from a very broad distribution.

When you say "find bugs related to cost counting," that distribution collapses. Attention concentrates on arithmetic precision, rounding errors, double-counting, missed edge cases in billing logic, currency handling, off-by-one in usage metering. The activations that encode "cost-related reasoning" get boosted, and unrelated bug-detection patterns get suppressed.

The model has a finite computational budget per forward pass. Broad prompts spread that budget thin. Specific prompts concentrate it.

### How This Differs From Persona Vectors

In the previous video we covered persona vectors — changing *how* the model reasons. Attention steering is the complementary concept: changing *where* the model focuses.

| | Persona Vectors | Attention Steering |
|---|---|---|
| **What it shifts** | Reasoning style, judgment, priors | Domain focus, search area |
| **Example** | "You're a paranoid finops auditor" | "Focus on billing logic in these files" |
| **Effect** | Model reasons differently about what it finds | Model looks at different things |
| **Analogy** | Changes the quality of the flashlight's light | Points the flashlight at a specific area |

A persona vector will often implicitly steer attention as a side effect — the paranoid finops auditor naturally looks at cost-related code more carefully. But the reverse isn't true. "Look at cost counting bugs" doesn't give you the reasoning benefits of the persona. You get the right search area but default reasoning patterns.

The strongest prompts combine both: persona (how to think) plus task specification (where to look). They're complementary vectors pointing in different directions through the same latent space.

### Why Default Distributions Are Dangerous

Every prompt has a default distribution — the region of output space the model gravitates toward based on training data frequency. The more common a pattern was in training, the more likely the model produces it.

This means:
- "Give me business ideas" → the same 50 ideas everyone gets (SaaS, marketplace, AI wrapper)
- "Debug this code" → the most statistically common bugs, not the subtle ones specific to your domain
- "Review this PR" → surface-level style and syntax issues, not deep architectural or logic problems

The penny-counting bug goes unnoticed. The unusual edge case in your billing logic gets skipped. Not because the model can't find it, but because generic prompts never steer attention there — the model's compute gets spent on whatever bug patterns were most frequent in training.

### The Flashlight Metaphor

Think of prompting less like writing a job description and more like pointing a flashlight:
- **Broad beam** — illuminates a wide area dimly
- **Narrow beam** — illuminates a small area brightly

The skill is knowing when you need breadth versus precision, and being specific about the dimensions that matter most for your task.

### Diminishing Returns of Long Prompts

This is also why extremely long system prompts that try to cover every scenario often underperform. You're not giving the model more capability — you're creating competition between directives for the model's attention budget. A focused prompt that nails the three or four highest-leverage dimensions often beats an exhaustive one.

Ten things to check in one prompt → the model's prior weighting decides what gets attention, and common patterns dominate.

Three focused, specific directives → full computational budget on each one.

### Demo

1. Show a codebase with a subtle cost-counting bug (e.g., rounding error in billing logic)
2. Ask the model to "review this code for bugs" — show that it flags common issues (null checks, error handling) but misses the cost bug
3. Ask the model to "review this code for bugs related to cost calculation, rounding, and double-counting" — show how the narrower attention catches what the broad pass missed
4. Contrast this with video 1's persona approach — the steering alone finds the bug, but the persona would also have flagged *why* it's dangerous and what downstream effects to check

### Key Insight

> A model's default output is a popularity contest — weighted by training-data frequency. Every time you add specificity to your prompt, you're overriding that default weighting and redirecting compute toward the things that actually matter for your task. The rare, domain-specific insight is always there in the model's capabilities — the prompt determines whether it ever gets attention.

### Bridge to Video 3

Now you have two tools: persona vectors (how to think) and attention steering (where to look). In the next video, we'll combine both using subagent teams — giving each subagent a distinct persona *and* a focused attention target, so you get thorough coverage without any single agent spreading itself thin.
