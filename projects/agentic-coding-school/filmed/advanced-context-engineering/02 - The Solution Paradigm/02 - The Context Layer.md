---
status: filmed
---

## From Paradigm to Practice

Progressive disclosure tells you *what* to do: load only what you need, when you need it.

This video tells you *how*: by building a **context layer** over your codebase—the system that delivers the right information at the right time.

---

## What Is the Context Layer?

Instead of hoping the model reconstructs your architecture from raw files (agentic search), or relying on senior engineers to hand-wire context every time (manual curation), you build a **thin, token-efficient layer** over your codebase.

Build it once. Every engineer and agent benefits automatically.

The context layer has three components:

![[images/02-the-context-layer/three-components.png]]

![[images/02-the-context-layer/what-is-context-layer.png]]
### Layer Nodes

Small, opinionated files (CLAUDE.md, AGENTS.md) that explain what each area of the system is for, how to use it safely, and what patterns and pitfalls agents need to know there.

The key behavior: **if a node exists in a directory, it covers that directory and all subdirectories, and is automatically included in context whenever an agent works there.**

You place nodes at semantic boundaries: where responsibilities shift, contracts matter, or complexity warrants dedicated context. Not every directory needs a node. The hierarchy handles coverage.

![[images/02-the-context-layer/layer-nodes.png]]

**What are contracts?** Contracts are the boundaries where components make promises to each other—API interfaces between services, database schemas that multiple services depend on, event formats in pub/sub systems, library interfaces that other code calls. These boundaries are high-stakes because changes affect multiple consumers. An agent working near a contract boundary needs to know what's public, what's stable, and what can't change without coordination.

![[images/02-the-context-layer/what-are-contracts.png]]
### Skills

Progressively disclosed capabilities that load only when relevant. The agent sees metadata (10-100 tokens), loads the full skill only when the task matches.

Good candidates for skills:
- Framework-specific patterns (especially newer versions that differ from training data)
- Complex workflows that span multiple files
- Domain knowledge that isn't in the code

You can point to skills from your Claude.MD files to add helpful reminds to trigger a skill in a folder.

![[images/02-the-context-layer/skills.png]]
### Hooks

Contextual automation that triggers at specific points in the agent's workflow. Hooks can inject context, run validation, or transform outputs based on what the agent is doing.

Examples:
- A pre tool use hook that reminds a model of best practices for committing or making PRs when it runs the command
- A post tool use hook that automatically lints files and ensures they're no longer than 500 lines which may be a standard in your team

Together, these three components ensure the agent gets the right context at the right time—without front-loading everything.

![[images/02-the-context-layer/hooks.png]]

---

## What the Layer Captures

The layer encodes what the code can't express:

- **Architectural decisions** — Why things are structured this way
- **Historical constraints** — The "why" behind patterns that seem odd
- **Tribal knowledge** — Undocumented integrations, enforcement boundaries
- **Contracts** — Which interfaces are public, stable, or shared across teams
- **Invariants** — Things that must never be violated
- **Concrete examples** — Patterns that override cognitive inertia

This is what your senior engineers carry in their heads. The context layer makes it explicit and accessible.

![[images/02-the-context-layer/what-layer-captures.png]]

---
## The Layer in Action

Consider an agent adding a new feature flag to a 2.5M token codebase.

**Without a context layer:** The agent greps for "feature flag," finds 150 files, reads the most promising ones. It adds the flag to the code, but misses critical details: the flag config lives in a separate repo. There's an A/B testing integration that needs updating. Staging and production have different flag sources. The agent's changes compile but break in deployment.

![[images/02-the-context-layer/layer-in-action-without.png]]

**With a context layer:** The harness auto-loads the root node, which mentions the feature flag system. The agent navigates to the relevant context:

```
CLAUDE.md (root)
  → "Feature flags: see infrastructure/feature-flags/"
    → infrastructure/feature-flags/CLAUDE.md
      → explains the three-environment setup
      → links to the config repo
      → warns about the A/B testing sync requirement
      → points to examples of correctly added flags
```

The node mentions a skill for adding feature flags. The agent activates it, and the skill provides:

- A checklist: add to code → add to staging config → add to production config → update A/B testing manifest
- The exact file paths for each config location
- A template for the flag definition format
- A reminder to run the sync script after updating the manifest

When the agent commits, a pre-commit hook runs validation:

- Checks the flag exists in all three environment configs
- Verifies the A/B testing manifest includes the new flag
- Warns if the flag is enabled in production but not staging (a common mistake)

The agent catches a missing staging entry, fixes it, and commits clean.

**Result:** The flag works on first deploy. Not because the agent was lucky—because the layer guided it through every enforcement point.

The agent still does agentic search. But it starts with a map instead of grepping blind. It knows what must happen. It gets feedback when something's wrong. The layer turned a fragile, hope-based process into a reliable one.

![[images/02-the-context-layer/layer-in-action-with.png]]

---

## The Hierarchy

The layer nodes form a hierarchy that mirrors your codebase:

- **Root level** — System-wide context (5-10 things relevant to *any* task)
- **Subsystem level** — Service and domain boundaries
- **Component level** — Specific modules and features

```
/CLAUDE.md           — Project overview, key commands, global constraints
/api/CLAUDE.md       — API conventions, auth patterns, error handling
/frontend/CLAUDE.md  — Component patterns, state management, styling rules
/scripts/CLAUDE.md   — How to run things, what each script does
```

![[images/02-the-context-layer/the-hierarchy.png]]

### What the Agent Sees

When an agent works on a file, it gets a **T-shaped view**:

- **Horizontal:** Broad context from the root and mid-level nodes (the ancestors)
- **Vertical:** Specific detail for the area it's working in

Say the agent is fixing a bug in `/api/auth/tokens.ts`. It automatically loads:

1. `/CLAUDE.md` — The project overview (always loaded)
2. `/api/CLAUDE.md` — API conventions and patterns
3. `/api/auth/CLAUDE.md` — Auth-specific context, token handling rules

It doesn't load `/frontend/CLAUDE.md` or `/scripts/CLAUDE.md`. Those aren't relevant. The agent gets exactly what it needs for this task—nothing more.

![[images/02-the-context-layer/t-shaped-view.png]]
### Why This Matters

Imagine a 2000-line CLAUDE.md at the root that covers everything. Every task loads 15k tokens of context, most of it irrelevant to the current work.

Now imagine that same content split hierarchically:

- Root: 50 lines (400 tokens)
- `/api/`: 80 lines (600 tokens)
- `/api/auth/`: 60 lines (500 tokens)

A task in `/api/auth/` loads **1500 tokens** of highly relevant context instead of 15k tokens of mixed relevance. The signal-to-noise ratio improves dramatically.

![[images/02-the-context-layer/token-math.png]]
### Navigation Between Nodes

Each node can link to others using `@` references and downlinks. These create pathways:

- **Upward:** Ancestors load automatically—you don't need to link to them
- **Downward:** Point to child nodes for specific subsystems
- **Sideways:** Link to related context outside the ancestor chain (e.g., "see also `/docs/auth-flow.md`")

The agent traverses this network to find relevant context, understand how components relate, and navigate from high-level to low-level as needed.

![[images/02-the-context-layer/navigation-between-nodes.png]]
### Example Files

When cognitive inertia fights you—when the model keeps reverting to conventional patterns—examples win.

Include canonical code snippets in your nodes, or link to real files in your codebase:

```markdown
## Patterns

For new API endpoints, follow the pattern in `src/api/users/get.ts`.
For new React components, copy the structure from `src/components/Button/index.tsx`.
```

Concrete code is more powerful than prose. The agent mirrors what it sees.

![[images/02-the-context-layer/example-files.png]]

---

## The Payoff

### It Scales Your Best Engineers

Instead of answering the same questions or fixing the same bugs, your senior staff encodes their understanding once. The AI uses it on every task, for every engineer.

The senior engineer's context becomes organizational context.

### It Raises the Floor

This elevates every agent interaction to the level of a tenured senior engineer who knows where the bodies are buried. Junior engineers delivering results your best engineers would—in a fraction of the time.

### It Future-Proofs Your Stack

This layer is a distillation of your specific data and intent. It doesn't just unlock current models. It makes every future model more effective.

As models get smarter, they leverage structured context even better. You're investing in compounding returns.

### It Makes Search Effective

Remember: search isn't useless, it's just not enough alone.

The context layer is the map. Search is still how the agent explores. But now it explores with guidance. It knows where to look, what patterns to follow, what constraints to respect.

Less fumbling. More finding.

![[images/02-the-context-layer/the-payoff.png]]

---

## The Tradeoffs

- **Upfront investment:** Building this layer properly requires time—more for larger codebases.
- **Requires expertise:** Getting it performing optimally requires knowledge of both context engineering and your system's architecture.
- **Maintenance overhead:** The layer needs to stay in sync with the code as your system evolves.

But once it's in place, every subsequent task reaps the benefits at zero marginal cost.

![[images/02-the-context-layer/the-tradeoffs.png]]

---

## The Mindset Shift

Stop thinking of yourself as someone who prompts AI.

Start thinking of yourself as someone who builds systems that make AI effective.

You're not writing prompts. You're writing infrastructure. The prompt is just the trigger. The context layer is what makes it work.

![[images/02-the-context-layer/mindset-shift.png]]

---

## What's Next

You understand the paradigm. You understand the layer.

Now you need to learn what actually goes into each node—what to capture, how to structure it, where to put it.

Next: [[01 - Anatomy of a Node|Anatomy of a Node]] — the six core areas every node should cover.
