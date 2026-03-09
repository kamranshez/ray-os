---
status: filmed
---

When you build a codebase with AI assistance, the first model you use has an outsized influence on everything that comes after. AI code assistants work by continuing patterns — they look at your existing code and produce more of the same. This means that if you started a project with an older, less capable model (say, Sonnet 3.7 or Sonnet 4), the architectural decisions, naming conventions, error handling, and structural choices that model made become baked into your codebase. Every future interaction — whether from a better model or a human developer — tends to extend those early decisions rather than challenge them.

This creates a kind of gravitational pull. The older model's limitations don't just live in the code it wrote — they shape all the code that follows. Even when you upgrade to a significantly more capable model, it still reads your existing codebase as context and produces output that fits within its patterns. The result is that early, weaker AI output acts as a self-reinforcing template that compounds over time.

Understanding this dynamic is critical for deciding when to refactor, when to rewrite, and how to prevent your codebase from being permanently constrained by the worst model that ever touched it.

![[images/gravitional-pull-from-older-models-2.png]]

## What's actually happening

### 1) Pattern continuation is the default

Most code assistants behave like: _"Given this repo, what's the most likely next chunk of code?"_ So if the repo contains:

- Repetitive helper wrappers
- Copy/paste service layers
- Weak boundaries (everything calls everything)
- Inconsistent naming / folder structure
- "Just make it work" error handling

…then future changes will tend to **extend those choices**, even when better options exist.

### 2) Early "bad model" code becomes the repo's gravitational field

Even if you're now using a much better model, the model is still "conditioned" by the existing code:

- It will mimic the repo's architecture (even if it's flawed)
- It will match style and conventions (even if inconsistent)
- It will reuse existing abstractions (even if they shouldn't exist)

So the _quality ceiling_ becomes bounded by the codebase's existing patterns, unless you deliberately break the loop.

### 3) You get a specific kind of technical debt: "AI-shaped debt"

This debt looks like:

- **Over-abstraction without clear payoff** — interfaces for everything, extra layers
- **Under-abstraction where it matters** — business rules scattered across handlers
- **Verbose boilerplate** — models love "safe" repetition
- **Inconsistent architecture** — because prompts varied across time
- **Missing invariants** — tests/types/contracts weren't enforced early
- **Unclear intent** — code that compiles but doesn't explain why it exists

The scary part: it can _feel_ coherent locally, but globally it's harder to scale.

![[images/gravitional-pull-from-older-models-5.png]]

---

## Practical implications for refactoring and rewrites

### A) Reviews matter more than you think (and in a different way)

If AI is extending patterns, code review isn't only about correctness. It's about:

- "Is this change making the architecture more legible?"
- "Is this reinforcing a pattern we actually want long-term?"
- "Did we just add another instance of the same workaround?"

Without that lens, you get **architecture drift** where each PR is "fine" but the system trends worse.

### B) Treat "model era" as provenance

If parts of the repo were generated under weaker models, they'll often share failure modes. That means:

- Hotspots will cluster in specific folders/modules
- Refactors should be targeted there first
- You can prioritize rework by "era" the same way you'd prioritize legacy code

A simple move: tag modules or ADRs with "this subsystem predates X standards."

### C) "Rewrite from scratch" becomes more rational when the constraints are baked in

Not always, but sometimes early AI decisions embed constraints like:

- Wrong data model
- Wrong boundaries between services/modules
- No testability seams
- State and side effects everywhere

If the **core shape** is wrong, refactoring becomes death by a thousand cuts. Rebuilding can be cheaper if you can:

- Keep API contracts stable
- Migrate with a strangler approach
- Preserve business logic via tests/specs

![[images/gravitional-pull-from-older-models-3.png]]

---

## How to break the loop (without boiling the ocean)

### 1) Establish "desired patterns" explicitly

Give the AI something better to imitate. Do this in writing (even a short doc):

- Folder/module boundaries
- Error-handling standard
- Testing strategy + required coverage for new code
- Type discipline / schemas / validation rules
- Dependency direction rules ("domain can't import infra" etc.)

Then enforce it with tooling:

- Lint/format + precommit hooks
- Architectural linting (even lightweight)
- CI checks for testing minimums

Once those are present, AI starts continuing _good_ patterns instead.

### 2) Put the AI in "rewrite mode," not "autocomplete mode"

When touching a legacy module, don't ask for a small change first. Ask for:

- A rewrite of the file _to the new standard_
- Removing duplication
- Introducing clear boundaries
- Adding tests around behavior

In other words: **force a style/architecture discontinuity** — otherwise the model will happily match the old shape.

### 3) Refactor by seams: isolate, then replace

A reliable playbook:

1. Wrap the legacy module behind a narrow interface
2. Add characterization tests (lock current behavior)
3. Re-implement behind the interface to the new standard
4. Swap usage incrementally

This turns "legacy AI blob" into something you can delete safely.

### 4) Use "scalability rewrites" on the 20% that causes 80% of pain

You don't need to remake everything. Pick:

- The module you touch every week
- The one with the most bugs
- The one blocking a new feature
- The one causing performance/ops pain

Make that module the _new gold standard_ so future AI copies _it_.

![[images/gravitional-pull-from-older-models.png]]

---

## When rebuilding the product makes sense

Rebuild tends to win when:

- The domain model is wrong and infects everything
	- For example, building an e-commerce SaaS and the early AI modeled `Order` as a flat record with a single product field instead of supporting multiple line items, discounts, and fulfillment states, that's a wrong domain model. Every feature you build afterward (returns, partial shipments, invoicing) has to work around that fundamental mismatch.
- Tests are too sparse to refactor confidently
- The architecture has no seams (everything is coupled)
- You can keep the external contract stable while rewriting internals
- The product is still early enough that migration cost is manageable

But rebuild loses when:

- You can't specify behavior precisely (no tests/specs)
- Lots of edge cases live only in production
- The rewrite will pause shipping for too long

A good compromise: **strangler rebuild** — new core built cleanly, legacy gradually routed out.

![[images/gravitional-pull-from-older-models-6.png]]

---

## A simple rule of thumb

- **New code must match the new standard.**
- **Touched legacy code gets "brought up" opportunistically.**
- **Untouched legacy code stays until it blocks velocity.**

That avoids perfectionism, but still ensures the repo gets better over time rather than worse.

![[images/gravitional-pull-from-older-models-4.png]]
