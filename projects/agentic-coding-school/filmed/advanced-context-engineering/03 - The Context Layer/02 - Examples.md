---
status: filmed
---

## From Theory to Practice

You've learned the principles in [[01 - Anatomy of a Node]]. Now let's see them applied.

This file contains real-world before/after examples. Study the transformations. Notice what gets cut, what gets kept, and why.

---

## Example: The Generic CLAUDE.md

A typical first attempt at a CLAUDE.md. It's full of good intentions but creates more noise than signal.

### Before

```markdown
# CLAUDE.md

This is our app. We use React and Node. The database is PostgreSQL.

## Rules
- Use TypeScript
- Don't use any
- Write tests
- Use meaningful variable names
- Don't commit secrets
- Follow REST conventions
- Use proper error handling
- Document your code
- Keep functions small
- Don't repeat yourself
- Use environment variables for config
- Follow the style guide
- Run linting before commits
- Keep dependencies updated
- Use semantic versioning
- Write meaningful commit messages
- Don't push to main directly
- Review code before merging
- Keep the README updated
- Use feature branches

## Architecture
We have a frontend and backend. The frontend talks to the backend via API.
```

### Problems

- **Generic rules that apply to any project** — pure noise
- **No actionable specifics** — "use proper error handling" means nothing
- **Architecture description is useless** — "frontend talks to backend" adds zero information
- **Rules likely to be ignored** — too many competing for attention

### After

```markdown
React 18 + Node 20 + PostgreSQL 15. Monorepo with `apps/web` and `apps/api`.

## Commands

- `pnpm dev` — Start both services
- `pnpm test:unit <path>` — Run single test file
- `pnpm db:migrate` — Run pending migrations

## Architecture

API follows vertical slice: each feature in `apps/api/src/features/{name}/` contains router, service, repository, and tests together.

Auth uses JWT with refresh tokens. All protected routes use `requireAuth` middleware from `apps/api/src/middleware/auth.ts`.

## Critical Invariants

- Never bypass `requireAuth` — audit logs depend on `req.user`
- All database writes go through repositories (not raw SQL) for soft-delete handling
- Feature flags checked via `apps/api/src/lib/flags.ts`, not env vars directly
```

### Why This Works

- **Specific versions and structure** — Claude knows exactly what it's working with
- **Actual commands** — Claude can run these directly
- **Architecture explains *why*, not just *what*** — vertical slice pattern is actionable
- **Critical rules are project-specific** — these matter for *this* codebase

---

## Example: The Bug Fix Entry

A bug was found and fixed. The developer documented it in CLAUDE.md. But they documented too much.

### Before

```markdown
### SwiftUI + @MainActor Singleton Crash (CRITICAL)

**Never use `@StateObject` with a `@MainActor` isolated singleton.**

This pattern causes crashes when SwiftUI evaluates view bodies:

​```swift
// WRONG - Will crash
@MainActor
class MyMonitor: ObservableObject {
    static let shared = MyMonitor()
    @Published var value = 0
}

struct MyView: View {
    @StateObject private var monitor = MyMonitor.shared  // CRASH!
    var body: some View { ... }
}
​```

#### Why It Crashes

1. `MyMonitor` is `@MainActor` isolated, so its `static let shared` property is also main-actor isolated
2. When SwiftUI initializes the view, it evaluates `MyMonitor.shared`
3. During certain SwiftUI update cycles, view initialization may occur in a context where actor isolation can't be verified
4. Swift's runtime calls `swift_task_isMainExecutorImpl` to check actor isolation
5. This check can fail, causing a null pointer dereference (`EXC_BAD_ACCESS` at address near `0x3`)

**Crash signature:**
​```
Thread 0 Crashed (main thread):
objc_msgSend + 56              <- nil message send
swift_getObjectType
swift_task_isMainExecutorImpl  <- actor isolation check
DesignLibrary                  <- Apple's private SwiftUI framework
ZStack.init(alignment:content:)
ViewBodyAccessor.updateBody
​```

#### The Fix

Use `@ObservedObject` instead of `@StateObject` for singletons:

​```swift
// CORRECT - View observes but doesn't own the singleton
struct MyView: View {
    @ObservedObject private var monitor = MyMonitor.shared  // OK
    var body: some View { ... }
}
​```

**Why `@ObservedObject` works:**
- `@StateObject` is for objects the view **owns** (creates and manages lifecycle)
- `@ObservedObject` is for objects the view **observes** (created elsewhere)
- A singleton is inherently not owned by any single view

#### Alternative: Move Logic to SettingsManager

For toggle-based features (like Apple Music blocker), handle the toggle in the settings manager's `didSet` instead of in the view:

​```swift
// In GeneralSettingsManager:
@AppStorage("blockAppleMusic") var blockAppleMusic: Bool = false {
    didSet {
        if blockAppleMusic {
            MusicBlocker.shared.start()
        } else {
            MusicBlocker.shared.stop()
        }
    }
}

// In view - no .onChange needed, just bind the toggle:
SettingsToggleRow(isOn: $settingsManager.blockAppleMusic)
​```

#### Real Example From Codebase

This crash affected version 2.19.0 when `USBPedalMonitor.shared` was used with `@StateObject`:
- File: `ShortcutsSettingsSection.swift`
- File: `USBPedalSettingsSection.swift`
- Fix: Changed `@StateObject` to `@ObservedObject`
```

### Problems

- **Way too much explanation** — the core rule fits in two sentences; the rest is tutorial content
- **Crash signature is noise** — not actionable for prevention
- **~80 lines when ~15 would suffice**

### After

```markdown
### SwiftUI + @MainActor Singleton Crash

**Never use `@StateObject` with a `@MainActor` singleton.** Use `@ObservedObject` instead.

​```swift
@MainActor
class MyMonitor: ObservableObject {
    static let shared = MyMonitor()
}

struct MyView: View {
    // WRONG - crashes with EXC_BAD_ACCESS during view init
    @StateObject private var monitor = MyMonitor.shared

    // CORRECT - view observes but doesn't own the singleton
    @ObservedObject private var monitor = MyMonitor.shared
}
​```

**Why:** `@StateObject` is for objects the view owns. Singletons aren't owned by any view — use `@ObservedObject` to observe them. The crash occurs because SwiftUI's view initialization can trigger actor isolation checks that fail during certain update cycles.

**Example:** Fixed in v2.19.1 for `USBPedalMonitor.shared` in `ShortcutsSettingsSection.swift` and `USBPedalSettingsSection.swift`.
```

### Why This Works

- **Rule + fix in first two lines** — immediate clarity
- **One minimal code example** — shows wrong vs right
- **Brief "why" for context** — enough to understand, not a tutorial
- **Pointer to real files** — if the agent needs more detail, it can look
- **~15 lines instead of ~80** — signal without noise

---

## The Transformation Pattern

Notice what changed in both examples:

| Before | After |
|--------|-------|
| Generic rules | Project-specific invariants |
| Vague descriptions | Concrete commands and paths |
| Explanations of *what* | Explanations of *why* |
| Tutorial-length content | Reference-length content |
| Everything inline | Pointers to source files |

**The core question:** What does Claude need to avoid making a mistake? Include that. Nothing more.

![[images/02-examples/transformation-pattern.png]]

---

## Audit Your Context Layer With This Prompt

If your CLAUDE.md files have grown unwieldy or you're not sure where to add new nodes, use this prompt in Claude Code to audit your context layer:

```
Audit my context layer and help me restructure it for progressive disclosure.

Follow these steps:

1. **Find all CLAUDE.md files**: Search the codebase for existing CLAUDE.md and AGENTS.md files. List them with their locations and line counts.

2. **Find contradictions**: Identify any instructions that conflict with each other, either within a single file or across files. For each contradiction, ask me which one to keep.

3. **Identify the essentials**: For the root CLAUDE.md, extract only what belongs there:
   - One-sentence project description
   - Package manager (if not npm)
   - Non-standard build/typecheck commands
   - Anything truly relevant to every single task

   Flag anything else for relocation to a more specific node.

4. **Identify semantic boundaries**: Based on the codebase structure, suggest where new CLAUDE.md files should be created. Look for:
   - Directories with distinct responsibilities
   - Areas with specific conventions or constraints
   - Subsystems that have their own patterns or gotchas

   Also identify:
   - Content that belongs in **skills** (complex workflows, framework-specific patterns that should load on-demand)
   - Patterns that would benefit from **hooks** (validation on commit, context injection when entering certain directories)

5. **Apply the LCA principle**: For instructions that apply to multiple areas, identify the shallowest node that covers all relevant paths. Don't duplicate facts across leaf nodes—place them in the Least Common Ancestor.

6. **Flag for deletion**: Identify any instructions that are:
   - Redundant (the agent already knows this)
   - Too vague to be actionable
   - Overly obvious (like "write clean code")
   - Better enforced by linters/formatters

   **Ask me to confirm each deletion before proceeding.**

7. **Propose the new structure**: Show me:
   - The proposed root CLAUDE.md (minimal, with @imports)
   - Each new file with its relevant instructions
   - Suggested locations for sub-folder CLAUDE.md files
   - Any suggested skills or hooks

   **Do not write any files until I approve the structure.**
```

This prompt forces Claude Code to audit your entire layer, not just one file, and requires your approval before making changes.

---

## Summary

The best CLAUDE.md files share these qualities:

- **Specific over generic** — project details, not universal truths
- **Commands over descriptions** — things Claude can actually run
- **Why over what** — rationale that informs decisions
- **Pointers over explanations** — let the code speak for itself
- **15 lines over 80** — ruthless editing

When in doubt, cut it.

Next: [[03 - Common Mistakes]] — patterns that hurt your layer's effectiveness.
