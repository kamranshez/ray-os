---
duration: "1-4 min"
batch: 1
order: 17
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Skills"
---
## The Problem: Implementation Tunnel Vision

During a long implementation session, the agent's entire context window gets consumed by the task at hand — the feature logic, the errors it hit, the fixes it tried. By the time the code works, the agent has completely forgotten the bigger picture: the existing utilities in your codebase, the patterns other files follow, the abstractions that already solve half the problem.

The result? Code that works but is disconnected from the rest of the project. Hand-rolled helpers that duplicate existing ones. Patterns that don't match the conventions three files over. Inefficiencies that a fresh pair of eyes would catch in seconds.

![[images/tunnel-vision/excalidraw_7.png]]
## The Solution: Three Fresh Subagents

`/simplify` spawns three parallel review agents — each with a **clean context window** — and points them at your git diff. Because they start fresh, they can explore the broader codebase without the tunnel vision of the implementation session:

- **Agent 1 (Code Reuse)** — searches utility directories, shared modules, and adjacent files for existing functions that do what the new code does manually. This is the one that catches "you just rewrote the helper that already exists in `utils/`."
- **Agent 2 (Code Quality)** — looks for hacky patterns: redundant state, copy-paste with slight variation, leaky abstractions, stringly-typed code where enums already exist.
- **Agent 3 (Efficiency)** — spots unnecessary work, missed concurrency, hot-path bloat, memory leaks, and overly broad operations.

The key insight: these agents aren't just reviewing code quality in the abstract. They're **reconnecting your new code with the existing codebase** — something the main agent lost the ability to do after 80k+ tokens of implementation focus.

![[images/three-fresh-subagents/excalidraw_2.png]]

![[images/reconnecting-codebase/excalidraw_8.png]]
## When to Use It

- After finishing a feature, before committing
- Before opening a PR
- After a long session where the agent went through multiple fix-retry cycles
- Anytime you suspect the implementation "works but isn't clean"

## The Full Prompt

```
# Simplify: Code Review and Cleanup

Review all changed files for reuse, quality, and efficiency. Fix any issues found.

## Phase 1: Identify Changes

Run `git diff` (or `git diff HEAD` if there are staged changes) to see what changed. If there are no git changes, review the most recently modified files that the user mentioned or that you edited earlier in this conversation.

## Phase 2: Launch Three Review Agents in Parallel

Use the Agent tool to launch all three agents concurrently in a single message. Pass each agent the full diff so it has the complete context.

### Agent 1: Code Reuse Review

For each change:

1. **Search for existing utilities and helpers** that could replace newly written code. Look for similar patterns elsewhere in the codebase — common locations are utility directories, shared modules, and files adjacent to the changed ones.
2. **Flag any new function that duplicates existing functionality.** Suggest the existing function to use instead.
3. **Flag any inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards, and similar patterns are common candidates.

### Agent 2: Code Quality Review

Review the same changes for hacky patterns:

1. **Redundant state**: state that duplicates existing state, cached values that could be derived, observers/effects that could be direct calls
2. **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring existing ones
3. **Copy-paste with slight variation**: near-duplicate code blocks that should be unified with a shared abstraction
4. **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
5. **Stringly-typed code**: using raw strings where constants, enums (string unions), or branded types already exist in the codebase
6. **Unnecessary JSX nesting**: wrapper Boxes/elements that add no layout value — check if inner component props (flexShrink, alignItems, etc.) already provide the needed behavior

### Agent 3: Efficiency Review

Review the same changes for efficiency:

1. **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
2. **Missed concurrency**: independent operations run sequentially when they could run in parallel
3. **Hot-path bloat**: new blocking work added to startup or per-request/per-render hot paths
4. **Recurring no-op updates**: state/store updates inside polling loops, intervals, or event handlers that fire unconditionally — add a change-detection guard so downstream consumers aren't notified when nothing changed. Also: if a wrapper function takes an updater/reducer callback, verify it honors same-reference returns (or whatever the "no change" signal is) — otherwise callers' early-return no-ops are silently defeated
5. **Unnecessary existence checks**: pre-checking file/resource existence before operating (TOCTOU anti-pattern) — operate directly and handle the error
6. **Memory**: unbounded data structures, missing cleanup, event listener leaks
7. **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

## Phase 3: Fix Issues

Wait for all three agents to complete. Aggregate their findings and fix each issue directly. If a finding is a false positive or not worth addressing, note it and move on — do not argue with the finding, just skip it.

When done, briefly summarize what was fixed (or confirm the code was already clean).
```
