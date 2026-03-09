---
status: filmed
---

Good example: https://github.com/steipete/agent-scripts/blob/main/AGENTS.MD
## From Theory to Practice

You've learned the constraints:

- **Signal-to-noise is everything** — every token in context affects every other token ([[02 - Signal to Noise]])
- **Search adds noise** — agentic exploration fills context before finding signal ([[03 - Why Search Isn't Enough]])
- **Instruction following has limits** — even frontier models degrade past ~150 instructions ([[04 - Instruction Following Limits]])
- **Cognitive inertia fights you** — models resist patterns that diverge from training ([[05 - Cognitive Inertia]])

And you've learned the solution: **progressive disclosure**. Load only what you need, when you need it.

Now it's time to apply this. Your CLAUDE.md file is where theory meets practice.

![[images/01-anatomy-of-a-node/from-theory-to-practice.png]]

---

## The CLAUDE.md Paradox

Here's the tension: CLAUDE.md is powerful *because* it's always loaded. But that same property makes it dangerous.

Every instruction you add competes with every other instruction. Add too much, and you hit instruction decay — the model starts silently dropping rules. Add the wrong things, and you're injecting noise into every single task.

The goal isn't to tell the model everything. It's to tell it **the right things** — the minimal set of high-signal context that applies to *every* task in your codebase.

![[images/01-anatomy-of-a-node/claudemd-paradox.png]]

---

## Why Have a CLAUDE.md At All

Claude doesn't know that your team uses a specific branch naming convention. It doesn't know about the quirky workaround in your authentication module. It can't see the Slack thread from 2022 explaining why that column exists.

CLAUDE.md is a special file that Claude automatically pulls into context when starting a conversation. This makes it ideal for:

- Commands you run often
- Core files and utility functions to reference
- Code style that diverges from conventions
- Testing instructions
- Repository etiquette (branch naming, merge vs rebase)
- Developer environment setup
- Project-specific warnings and gotchas

Source: https://www.humanlayer.dev/blog/writing-a-good-claude-md

![[images/01-anatomy-of-a-node/why-have-claudemd.png]]

---
## When You Need One

Brand new projects following modern conventions often don't need extensive CLAUDE.md files. Claude will likely follow standard conventions already.

The need grows as your project accumulates:

- **Custom patterns** that diverge from defaults
- **Historical decisions** with non-obvious rationale
- **Integration quirks** that aren't documented in code
- **Team-specific workflows** that differ from standard practice

If you're starting fresh with a modern stack, start with almost nothing. Add rules only when you notice repeated problems.

![[images/01-anatomy-of-a-node/when-you-need-one.png]]

---

## The Six Core Areas

Hitting these areas puts you in the top tier of CLAUDE.md files:

1. **Commands** — Executable commands with flags and options
2. **Testing** — How to run tests, what testing patterns to use
3. **Project Structure** — What lives where (especially in monorepos)
4. **Code Style** — Patterns and conventions (via examples, not prose)
5. **Git Workflow** — Branch naming, merge vs rebase, commit conventions
6. **Boundaries** — What should never be touched

You don't need all six. But if your CLAUDE.md doesn't touch any of them, it's probably not adding value.

Source: https://www.humanlayer.dev/blog/writing-a-good-claude-md

![[images/01-anatomy-of-a-node/six-core-areas.png]]

---

## What to Include vs Exclude

The question isn't "what could Claude benefit from knowing?" It's "what can Claude *not* infer from the code alone?"

**Include:**

- **Project context:** A one-liner that orients Claude. "Next.js e-commerce app with Stripe integration" tells Claude more than you'd think.
- **Commands with flags:** How to run tests, build, lint, deploy. Claude will use these exact commands.
- **Patterns that diverge from conventions:** Cognitive inertia will fight you otherwise.
- **Critical invariants:** Things that must never be violated.
- **Gotchas:** That authentication module with weird retry logic. The API endpoint requiring a specific header.

**Exclude:**

- Generic best practices ("write clean code", "use meaningful names")
- Things your linter/formatter already enforces
- Standard conventions the model already knows
- Detailed explanations of things in the code
- Task-specific guidance that only applies sometimes

**The test:** For each line, ask: "If I removed this, would Claude do something wrong on most tasks?" If no, it probably doesn't belong in root.


![[images/01-anatomy-of-a-node/what-to-include-exclude.png]]

---

## Put Commands Early

Put relevant executable commands in an early section. Include flags and options, not just tool names. Your agent will reference these constantly.

```markdown
## Commands

# Type check a single file
npm run tsc --noEmit path/to/file.tsx

# Format a single file
npm run prettier --write path/to/file.tsx

# Lint a single file
npm run eslint --fix path/to/file.tsx

# Run single test file
npm run vitest run path/to/file.test.tsx

# Full build (use sparingly)
yarn build:app

Note: Always lint, test, and typecheck updated files.
```

![[images/01-anatomy-of-a-node/put-commands-early.png]]

---

## Code Examples Over Explanations

One real code snippet showing your style beats three paragraphs describing it. Show what good output looks like.

```markdown
## Code Style

- Avoid class-based components like `Admin.tsx`
- Prefer functional components with hooks like `Projects.tsx`
- Forms: copy `app/components/DashForm.tsx`
- Charts: copy `app/components/Charts/Bar.tsx`
- Data grids: copy `app/components/Table.tsx`
- HTTP: use `app/api/client.ts` — never fetch directly in components
```

**Why this works:**

- **Reduces drift from legacy code.** You probably have old code that compiles, you're not ready to refactor yet, but shouldn't be copied.
- **Increases fidelity.** The agent mirrors your best examples in new code.
- **Fights cognitive inertia.** Concrete examples anchor behavior better than abstract rules.

![[images/01-anatomy-of-a-node/code-examples-over-explanations.png]]

---

## Set Clear Boundaries

Tell the agent what it should never touch. "Never commit secrets" was the most commonly cited helpful constraint.

```markdown
## Boundaries

- Never commit secrets or .env files
- Don't modify `vendor/` or `node_modules/`
- Production configs in `deploy/` are off-limits
- Don't touch `legacy/` unless explicitly asked
```

![[images/01-anatomy-of-a-node/set-clear-boundaries.png]]

---

## Point to Sources

Don't explain everything inline. Point Claude to the files that contain the answers.

**Why this works:**

1. **Keeps CLAUDE.md lean.** The explanation lives in its natural home.
2. **Progressive disclosure.** Claude loads detail only when entering that area.
3. **Single source of truth.** When code changes, you don't have stale instructions.

**Instead of this:**

```markdown
## Authentication

We use JWT tokens with refresh token rotation. Access tokens expire
after 15 minutes. Refresh tokens expire after 7 days. The auth flow
is: user logs in → gets access + refresh → uses access token → when
expired, uses refresh to get new pair → if refresh expired, must
re-login. All auth logic is in the AuthService class...
```

**Do this:**

```markdown
## Authentication

JWT with refresh token rotation. See `src/auth/AuthService.ts` for
implementation and `src/auth/README.md` for flow details.
```

The first version will rot. The second stays accurate.

![[images/01-anatomy-of-a-node/point-to-sources.png]]

---

## The @imports System

CLAUDE.md supports importing other files with `@path/to/file` syntax:

```markdown
See @README.md for project overview
See @docs/api-patterns.md for API conventions
See @package.json for available npm scripts
```

This keeps your main file lean. Put detailed instructions in separate markdown files, then reference them. Claude pulls in content when relevant.

**You can reference files from anywhere:**

- Relative paths: `@docs/style-guide.md`
- Absolute paths work too
- User-level files: `@~/.claude/my-preferences.md`

Imports can be recursive — referenced files can reference other files. Use this sparingly to avoid creating a maze.

**The pattern:** Essentials in CLAUDE.md, detailed topic-specific guidance in separate files via @imports.

![[images/01-anatomy-of-a-node/at-imports-system.png]]

---

## Sub-folder CLAUDE.md Files

Create CLAUDE.md files in subdirectories for domain-specific guidance. They only load when Claude enters that directory.

```
project/
├── CLAUDE.md              ← Always loaded (root)
├── src/
│   ├── CLAUDE.md          ← Loaded when touching src/*
│   ├── api/
│   │   └── CLAUDE.md      ← Loaded when touching src/api/*
│   └── auth/
│       └── CLAUDE.md      ← Loaded when touching src/auth/*
└── tests/
    └── CLAUDE.md          ← Loaded when touching tests/*
```

**The root CLAUDE.md** is always loaded. It should contain only what's relevant to *every* task.

**Descendant CLAUDE.md files** load when Claude enters that directory. They contain context specific to that subsystem.

This is progressive disclosure in action — Claude only sees what it needs for the current task.

![[images/01-anatomy-of-a-node/subfolder-claudemd.png]]

---

## Stack-Specific Info: Use Skills

Be specific about your stack, but put framework details into skills rather than bloating root CLAUDE.md.

**Example:** Callstack released `react-native-best-practices` — 27 AI-oriented skills for React Native and Expo optimization.

```bash
npx add-skill callstackincubator/agent-skills
```

Skills are organized into categories:

- **JavaScript:** React optimization, memoization, state patterns
- **Native:** iOS/Android profiling, native module development
- **Bundling:** Asset reduction, code shrinking, app size optimization

**The shift:** Instead of dumping optimization rules into CLAUDE.md, install a skill pack. The agent discovers and loads relevant skills only when working on that type of problem.

Source: https://www.callstack.com/blog/announcing-react-native-best-practices-for-ai-agents

![[images/01-anatomy-of-a-node/stack-specific-skills.png]]

---

## Target File Length

- **Under 300 lines** for root CLAUDE.md
- **Under 60 lines** is ideal (HumanLayer maintains this)
- Use sub-folder CLAUDE.md files for domain-specific guidance

If your root file is longer than 300 lines, it's almost certainly full of content that should live elsewhere.

![[images/01-anatomy-of-a-node/target-file-length.png]]

---

## New Model = Remove Stuff

When a new model releases, your first instinct might be to add new instructions. Do the opposite.

**Smarter models need less hand-holding.** Instructions that were necessary for older models become noise for newer ones. That noise actively hurts performance — it's the instruction following problem in action.

When the next frontier model drops, consider starting your CLAUDE.md from scratch. Keep only what the new model actually needs. You'll be surprised how much you can cut.

Source: https://code.claude.com/docs/en/best-practices

![[images/01-anatomy-of-a-node/new-model-remove-stuff.png]]

---

## Iterate On Your Setup

Don't try to write the perfect CLAUDE.md upfront. You can't. You don't know what problems you'll hit until you hit them.

> "Start simple. Add rules only when you notice the agent making the same mistake repeatedly. Add commands only after you've figured out a workflow you want to repeat. Don't over-optimize before you understand your patterns."
> — Cursor Team

Source: https://cursor.com/blog/agent-best-practices

**The iteration loop:**

1. Start with almost nothing
2. Work with the agent
3. Notice a repeated mistake or friction point
4. Add a minimal rule addressing that specific issue
5. Observe whether behavior actually changes
6. If it doesn't, the rule isn't working — rewrite or delete it

This is the opposite of how most people approach CLAUDE.md. They dump everything upfront, then wonder why the agent ignores half of it.


![[images/01-anatomy-of-a-node/iterate-on-setup.png]]


---

## Treat CLAUDE.md Like Code

Your CLAUDE.md isn't documentation. It's code that runs on every task. Treat it that way.

**Symptoms of a broken CLAUDE.md:**

| Symptom                                               | Likely Cause                                         |
| ----------------------------------------------------- | ---------------------------------------------------- |
| Claude ignores a rule you added                       | File too long, rule getting lost in noise            |
| Claude asks questions answered in CLAUDE.md           | Phrasing is ambiguous or buried                      |
| Claude follows rules inconsistently                   | Conflicting instructions somewhere                   |
| Claude produces generic output despite specific rules | Instructions aren't concrete enough — needs examples |

**The code mindset:**

- **Review it when things go wrong.** If Claude misbehaves, check your CLAUDE.md first. The bug might be there.
- **Prune it regularly.** Every few weeks, ask: "Is this still necessary? Is this still accurate?"
- **Test changes.** After editing, observe whether Claude's behavior actually shifts. If not, your edit didn't work.

![[images/01-anatomy-of-a-node/treat-like-code.png]]

---

## Generation: /init vs Manual

Two schools of thought:

**Use /init as a starting point.** Delete what you don't need. Deleting is easier than creating from scratch. The generated file often includes obvious things or filler — cut them.

**Write manually from scratch.** HumanLayer recommends against /init entirely. They suggest manually crafting every line since CLAUDE.md affects all workflow phases.

**My take:** Start with /init if you're new. But treat every generated line as suspect. Delete aggressively. The goal is signal, not coverage.

![[images/01-anatomy-of-a-node/generation-init-vs-manual.png]]

---

## The System Reminder Wrapper

Claude Code wraps your CLAUDE.md content with this:

```xml
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks.
You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

**What this means:** Claude Code is telling the model to selectively ignore parts of your CLAUDE.md. The harness is compensating for bloated instruction files.

**Why they added it:** Most CLAUDE.md files are stuffed with instructions that aren't broadly applicable. Users treat the file as a dumping ground for "hotfixes" — every time Claude does something they don't like, they append a rule. Signal-to-noise degrades. Instruction following breaks down.

The wrapper is a band-aid. It tells Claude: "This context might be noise. Use your judgment."

**The implication:** If you're relying on the wrapper to filter bad instructions, you're already losing. The model is spending attention on deciding what to ignore instead of executing your task.

Instead of stuffing everything into one file and hoping the model filters well, use the context layer properly:

- **Hierarchical nodes:** Keep root minimal. Put domain-specific guidance in nested CLAUDE.md files that only load when the agent enters that directory.
- **Skills:** Move complex workflows and framework-specific patterns into skills that activate only when relevant.
- **Hooks:** Use hooks to inject context or run validation at specific points—when committing, when entering certain directories, when editing certain file types.

Write a CLAUDE.md that doesn't need filtering. Then the wrapper becomes a no-op instead of a crutch.

![[images/01-anatomy-of-a-node/system-reminder-wrapper.png]]

---

## Plan Mode and Context Relevance

The wrapper explains why **plan mode** and **explore mode** are valuable.

When Claude enters plan mode, it explores first, then determines what context is relevant before acting. The planning phase is where Claude can:

1. Read your CLAUDE.md and identify which parts apply
2. Navigate to relevant directories and load their local CLAUDE.md files
3. Build a mental model before committing to implementation

Plan mode is progressive disclosure in action. Instead of dumping all context upfront, Claude loads what it needs as it understands the task.

### Why a Well-Structured Layer Makes This Better

With a good context layer, explore mode and plan mode become dramatically more effective. The agent isn't just grepping through code hoping to find signal—it's following a map.

**It finds the right files faster.** Instead of reading 50 files to understand where auth logic lives, the agent reads the root node, sees "Authentication: see `src/auth/`", navigates there, and loads the local node that explains the token flow. Three files instead of fifty.

**It discovers what code can't express.** The code shows *what* exists. The layer explains *why*:

- Historical constraints: "We use this pattern because the old API is still in production"
- Invariants: "Never bypass the rate limiter—it protects a fragile downstream service"
- Tribal knowledge: "The `legacy_id` column looks unused but Partner X depends on it"
- Integration quirks: "This service requires a specific header that isn't in the OpenAPI spec"

**It understands enforcement boundaries.** The agent learns where things *must* happen, not just where they *currently* happen. When planning a change, it knows which files to touch and which constraints to respect.

**It builds better plans.** A plan based on code alone is a guess. A plan based on code plus layer context accounts for constraints the code doesn't reveal. Fewer surprises in implementation. Fewer bugs in production.

If your CLAUDE.md is well-structured—minimal root, detailed subdirectories, relevant skills—the agent's exploration phase becomes a guided tour instead of a random walk.

![[images/01-anatomy-of-a-node/plan-mode-context.png]]

---

## Session Ending: Prompt for Updates

If at the end of a session you've learned something valuable, ask whether to update the CLAUDE.md. This keeps the file evolving with the project.

Good candidates for addition:

- A gotcha you just discovered
- A command you ran multiple times
- A pattern Claude kept getting wrong until you corrected it

Bad candidates:

- Task-specific context that won't apply again
- Explanations of what you just built (that's what code comments are for)

![[images/01-anatomy-of-a-node/session-ending-updates.png]]

## Summary

| Principle | Application |
|-----------|-------------|
| Signal-to-noise | Keep CLAUDE.md minimal — every line should apply to every task |
| Instruction limits | Don't dump everything; iterate and prune |
| Cognitive inertia | When diverging from conventions, point to examples in code |
| Progressive disclosure | Put details in subdirectory CLAUDE.md files, skills, and @imports |

**The six core areas:** Commands, Testing, Project Structure, Code Style, Git Workflow, Boundaries.

**Target length:** Under 60 lines ideal, under 300 max.

**The mindset:** Your CLAUDE.md is infrastructure, not documentation. Treat it like code. Review it, test it, prune it.

![[images/01-anatomy-of-a-node/summary.png]]

Next: [[02 - Examples]] — real-world before/after examples of transforming bloated nodes into lean, effective ones.
