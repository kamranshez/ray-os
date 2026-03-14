---
duration: "10-15 min"
batch: 1
order: 2
batch_name: "Seed Thinking"
class: "prompt-engineering"
chapter: "Steering Models"
---
## Persona Vectors: Changing How the Model Thinks

When you write "You are a senior backend engineer," you're not role-playing. You're activating a cluster of reasoning patterns inside the model — skepticism levels, what it treats as important, what it flags versus ignores, how it weighs trade-offs. A persona doesn't just change the model's tone. It changes what it *notices*.

### The Problem With No Persona

Without a persona, the model reasons like a generalist. It applies default judgment — the average of everything it learned during training. That means:

- It flags the most common bugs, not the subtle ones
- It gives you the most popular advice, not the most relevant
- It hedges everything equally instead of being opinionated where it matters

This is fine for generic tasks. It's terrible when you need depth in a specific domain.

![[images/no-persona-problem/excalidraw_2.png]]

### What a Persona Actually Does

Think of the model as having thousands of internal "dials" — formality, skepticism, risk tolerance, domain focus, verbosity, confidence, and hundreds more. A persona prompt turns many of these dials at once.

"You are a paranoid finops auditor who has spent a decade auditing cloud billing systems" doesn't just make the model talk about money. It:

- Cranks up skepticism around floating point arithmetic
- Makes it treat every pricing API as having undocumented edge cases
- Shifts what it considers "worth flagging" — a 0.01 rounding difference that a generalist ignores becomes a red alert
- Changes its reasoning chain — it now checks for double-counting *before* checking for null pointers

Same code. Same task. Completely different analysis — because the model is reasoning through a different lens.

![[images/persona-dials/excalidraw_9.png]]

### The Three Layers That Make a Persona Work

Most people stop at identity. That's the weakest layer.

**Identity** — who the model is
"You are a security auditor."
This is vague. It activates a broad region. The model has a rough sense of what a security auditor sounds like, but not how one actually thinks.

**Epistemics** — what they know and how they reason
"You focus on injection attacks before logic errors. You assume all user input is malicious. You check authentication flows before anything else."
Now the model has a reasoning *strategy*. It knows what to prioritize and in what order.

**Constraints** — what they'd never do
"You never approve code that concatenates user input into SQL strings, regardless of context. You never assume a framework's default settings are secure."
This gives the model hard boundaries that override its tendency to be agreeable.

The jump from layer one to layers two and three is where most people's prompts fall short. "You are an expert" is almost useless. "You check X before Y, you never trust Z, you always verify W" — that's where the real steering happens.

![[images/three-layers/excalidraw_5.png]]
### Behavioral Specificity Beats Identity Labels

Compare these two prompts for a code review:

**Weak:** "You are a senior backend engineer. Review this code."

**Strong:** "You prioritize readability over cleverness. You always consider edge cases before the happy path. You flag performance implications of any design choice. You assume this code will be maintained by someone who didn't write it."

The second prompt doesn't even name a role. But it specifies *how to reason* — and that produces dramatically better output than a title ever could.

The principle: describe the *behavior* you want, not the *label* you'd give it.
![[images/behavioral-specificity/excalidraw_2.png]]
### Correlated Dimensions: Free Extras and Unwanted Side Effects

Here's something most people don't realize. When you activate one trait, correlated traits come along for free:

- "Formal" pulls in "cautious" and "longer sentences"
- "Expert" pulls in "confident" and "jargon-heavy"
- "Casual" can inadvertently pull toward less rigorous reasoning

This is usually helpful — you get a coherent persona without specifying every dimension. But sometimes the correlations work against you. If you want casual *and* rigorous, you need to say both explicitly: "Be conversational in tone but rigorous in reasoning." Otherwise the model assumes casual means loose.

The skill is knowing when to ride the default correlations and when to explicitly break them.

![[images/correlated-dimensions/excalidraw_1.png]]
### When To Use Persona Vectors

- **Code reviews** — a "paranoid security reviewer" catches different things than a "performance-obsessed systems engineer"
- **Writing** — a "direct, no-nonsense editor" produces different feedback than an "encouraging creative writing coach"
- **Business analysis** — a "skeptical VC" stress-tests ideas differently than an "optimistic product manager"
- **Debugging** — a "methodical QA engineer who always reproduces before diagnosing" follows a different chain of reasoning than a general assistant

The persona doesn't make the model smarter. It makes it *opinionated* — and opinions are what cut through generic output.

### Demo

1. Show a piece of code with a subtle billing bug (rounding error in cost calculation)
2. Run a default review: "Review this code for bugs" — model flags common issues, misses the cost bug
3. Add a persona: "You are a paranoid finops auditor. You've spent a decade auditing cloud billing systems. You never trust floating point arithmetic for money. You assume every pricing API has edge cases the docs don't mention. You check for double-counting before anything else."
4. Same code — model now catches the rounding error, explains why it's dangerous, and suggests what downstream effects to check
5. Point out: the persona didn't just change *where* it looked — it changed *how it thought* about what it found

### Key Insight

> "You are an expert" is one of the weakest prompts you can write. Describe the *reasoning patterns* you want — what to check first, what to never trust, what to always flag. That's what actually moves the needle.
