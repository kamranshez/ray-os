---
class: "prompt-engineering"
chapter: "Core Techniques"
---
Sometimes the most effective prompt isn't about what to do — it's about what NOT to do. Constraints and negative instructions are how you carve away the parts of the output distribution you don't want, leaving only the region that matches your intent.

### Sculpting vs. Building

Think of two approaches to creating a statue:

- **Additive** (building): Start with nothing, add clay piece by piece until it looks right. This is how most people prompt — they describe what they want and hope the model builds it.
- **Subtractive** (sculpting): Start with a block of marble, remove everything that isn't the statue. This is what constraints do — they eliminate the outputs you *don't* want.

Both work. But for LLMs, sculpting is often more effective because the model already has a default output distribution for any given task. Instead of trying to describe the exact output you want (which requires you to anticipate everything), you can identify the common failure modes and explicitly block them.

### Why Negatives Work So Well

There's an asymmetry in how LLMs process positive vs. negative instructions:

- **Positive instruction**: "Write in a professional tone" — the model has to figure out what "professional" means in this context, which varies hugely across training data
- **Negative instruction**: "Do not use exclamation marks, emoji, or words like 'exciting', 'amazing', 'incredible'" — there's no ambiguity. The model can pattern-match against these specific tokens and suppress them

Negatives are more *precise* because they target specific failure modes rather than gesturing at a broad ideal. The model knows exactly what to avoid, even if it's still figuring out what to aim for.

This is why researchers working with LLMs often maintain long "do not" lists. They've seen the common failure patterns and know that blocking them is more reliable than describing the desired output perfectly.

### The Constraint Taxonomy

**Length constraints** — the most basic and most effective:
- "Keep it under 150 words"
- "Exactly 3 bullet points"
- "One paragraph, no more"

**Tone constraints** — what to suppress:
- "Do not apologize"
- "No hedging — no 'it depends', 'arguably', 'it's worth noting'"
- "Don't use corporate jargon — no 'leverage', 'synergy', 'ecosystem'"

**Content constraints** — what to exclude:
- "Do not suggest paid tools"
- "Do not include code — describe the approach only"
- "Skip the introduction — start with the first actionable step"

**Format constraints** — structural boundaries:
- "Do not use bullet points — write in prose paragraphs"
- "No markdown headers — plain text only"
- "Don't wrap the JSON in code fences"

**Behavioral constraints** — how the model should operate:
- "Do not ask clarifying questions — work with what you have"
- "Don't explain your reasoning — just give the answer"
- "Do not repeat the task back to me before starting"

### The "Do Not Start With" Technique

One of the highest-leverage constraints: tell the model what NOT to start with. LLMs have strong opening patterns baked in from training data:

- "Great question!" 
- "Certainly! Here's..."
- "Welcome to..."
- "Thank you for..."
- "I'd be happy to help..."

These openers are statistically dominant in training data because they appear in millions of helpful-assistant conversations. Once the model generates them, the rest of the output is colored by that "helpful assistant" distribution — it'll be more verbose, more cautious, more generic.

Blocking the opener reshapes the entire output: "Start directly with the answer. Do not begin with any greeting, acknowledgment, or meta-commentary about the task."

### Stacking Constraints

Individual constraints are good. Stacked constraints are powerful. But there's a point of diminishing returns where constraints start competing for the model's attention budget:

**Sweet spot (3-5 constraints):** The model handles these reliably. Each one meaningfully narrows the output.

**Too many (10+):** The model starts ignoring some constraints to satisfy others, or the output becomes so restricted it's awkward and stilted. This is the same attention budget problem from Steering Distributions — too many directives spread the model's compute thin.

**The fix for complex requirements:** Instead of 15 constraints, use a structured output schema (from the previous video) where the constraints are *implicit* in the structure. A JSON schema with specific keys and enum values encodes constraints more efficiently than a list of "do not" rules.

### Constraints as Quality Filters

Here's the reframe that makes constraints truly powerful: think of them as a quality filter, not restrictions.

When you write code, you use types, validation, and linting rules — not because you distrust the developer, but because constraints catch errors before they propagate. Prompt constraints serve the same purpose: they catch the model's default behaviors (verbosity, hedging, generic openings) before they pollute the output.

The best prompts combine positive steering (what to do, who to be, what to focus on) with negative constraints (what to avoid, what to suppress). The positive instructions point the flashlight; the constraints block the unwanted light spill.

### Demo

1. Ask for an out-of-office email with no constraints — show the generic, wordy result
2. Same task with 4 targeted constraints (no "limited access", no "thank you for your patience", start with dates, under 75 words) — show the dramatically better output
3. Show the "do not start with" technique: ask for advice, first without constraint (model says "Great question!"), then with "Start with the first action item" 
4. Demonstrate constraint overload: give 12 constraints and show the model struggling to satisfy all of them
5. Show the same 12 constraints encoded as a JSON schema — model handles it cleanly

### Key Insight

> Positive instructions tell the model where to aim. Negative constraints tell it where the boundaries are. Together, they define a narrow region of output space that matches what you actually want. The asymmetry is real: "do not use exclamation marks" is more precise than "be professional," because negatives target specific patterns while positives gesture at broad ideals. Master prompters maintain a personal library of constraints for their common failure modes — it's the fastest way to go from a decent prompt to a great one.
