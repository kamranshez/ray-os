---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Cleaning Up Legacy Code"
class: "techniques"
chapter: "Cleaning Up Legacy Code"
---

## The Migration You Keep Putting Off

Every codebase has a backlog of migrations nobody wants to do. The framework upgrade. The deprecated API removal. The strict mode rollout. The library you were supposed to swap out two years ago.

Agents just removed the typing cost of all of that. But most people point an agent at the backlog, watch it wander, and conclude the model isn't ready.

The model is ready. What's missing is one concept: **the seam**.

A seam is a migration you can measure. This video is about what that means, how to spot seams in your own codebase, and how to write the one paragraph that turns a vague wish into a contract an agent can execute.

---

## The Prompt That Drifts

Here's what everyone tries first:

```
> clean up the date handling in this codebase
```

The agent starts strong. It patches ten files, twenty, thirty. Then somewhere around file two hundred, it makes a change that quietly violates an assumption it saw back in file twelve. Nothing errors. Nothing warns. The drift is silent, and you find it three weeks later in production.

This is the specific way long-running agent work fails. Not bad code. **Undefined done.**

When "done" isn't defined, there's nothing to check each change against. The agent can't tell whether it's converging or wandering, and neither can you.

[IMAGE: dark chalkboard, a long row of file icons numbered 1 to 200, an agent arrow patching left to right, file 12 glowing with a small "invariant" label, a faded dotted line showing the agent's memory of it dissolving by file 200]

![[migration-seams-silent-drift-1.png]]
![[migration-seams-silent-drift-2.png]]
![[migration-seams-silent-drift-3.png]]
![[migration-seams-silent-drift-4.png]]
![[migration-seams-silent-drift-5.png]]

---

## Old Way, New Way, and a Hard Edge

A seam is the line where two states of your codebase meet. Everything on one side is the old way. Everything on the other side is the new way. Like the seam on a shirt: two pieces of fabric, one clean joining line.

The term comes from Michael Feathers' *Working Effectively with Legacy Code*, where a seam is a place you can change behavior without rewriting everything. For migrations, it means something simpler: **a migration with a clean edge**.

Source: https://www.oreilly.com/library/view/working-effectively-with/0131177052/

The test is binary. Pick any file in scope. Can you say, without judgment or debate, which side of the line it's on?

- "This file still imports `moment`" is a fact.
- "This file has clean date handling" is an opinion.

Facts make seams. Opinions make wishes.

[IMAGE: dark chalkboard, a codebase drawn as a fabric panel split by a stitched vertical seam line, left side labeled OLD WAY with moment icons, right side labeled NEW WAY with date-fns icons, three file shapes mid-crossing over the stitch]

![[migration-seams-two-sides-1.png]]
![[migration-seams-two-sides-2.png]]
![[migration-seams-two-sides-3.png]]
![[migration-seams-two-sides-4.png]]
![[migration-seams-two-sides-5.png]]

And because every file is provably on one side or the other, you get the most underrated tool in agent-driven work: **a counter**.

```bash
grep -rc "from 'moment'" src/ | wc -l
# 214
```

That number is your progress bar. It only moves one direction, and when it hits zero, you are done. Not "feels done." Provably done.

[IMAGE: dark chalkboard, a large hand-drawn counter ticking 214 → 141 → 96 → 0 above a progress bar, an agent icon pushing file shapes across a seam line beneath it]

![[migration-seams-the-counter-1.png]]
![[migration-seams-the-counter-2.png]]
![[migration-seams-the-counter-3.png]]
![[migration-seams-the-counter-4.png]]
![[migration-seams-the-counter-5.png]]

---

## The Anatomy of a Seam Definition

A seam gets written down as one paragraph with five parts. This document is the whole trick. Everything the agent does later hangs off it.

```markdown
## Seam: moment → date-fns

BEFORE: 214 call sites in src/**/*.ts{,x} import moment
AFTER:  zero imports of moment; date-fns everywhere; moment out of package.json

IN SCOPE:  src/**/*.ts, src/**/*.tsx
OUT:       scripts/, e2e/

INVARIANTS:
- every rendered date string stays byte-identical (snapshot tests)
- timezone behavior unchanged: UTC in, local out

DONE WHEN:
- grep -r "from 'moment'" src/  → 0 results
- npm run typecheck && npm test && npm run build  → all green
```

Five parts, each doing a job:

1. **Before-state.** The old way, stated as a checkable fact with a count.
2. **After-state.** The new way, stated the same way.
3. **Scope.** Which files are playing. Just as important: which aren't.
4. **Invariants.** What must stay true while files cross the line. This is where migrations actually die, so this is where your thinking goes.
5. **Done when.** The exact commands that prove completion. If a machine can't run it, it doesn't belong here.

[IMAGE: dark chalkboard, an anatomy-style diagram of a single document with five labeled callout arrows pointing to its parts: before, after, scope, invariants, done-when, the invariants callout drawn larger and underlined]

![[migration-seams-seam-anatomy-1.png]]
![[migration-seams-seam-anatomy-2.png]]
![[migration-seams-seam-anatomy-3.png]]
![[migration-seams-seam-anatomy-4.png]]
![[migration-seams-seam-anatomy-5.png]]

And the filter that keeps you honest: **the fifteen-minute test.** If you can't write this paragraph in fifteen minutes, you don't understand your own migration yet. Neither will the agent. Go read the code first.

---

## A Field Guide to Seams

Once you know the shape, you'll see seams everywhere. They cluster into five families.

**1. Dependency swaps.** One library out, another in.
- `moment` → `date-fns`. `request` → `fetch`. `lodash` → native array methods.
- Counter: imports of the old library.

**2. Version upgrades.** Same tool, new major.
- React 18 → 19. Rails 7 → 8. ESLint 8 → 9 flat config. Ruby version bumps.
- Counter: usually binary per package, plus the deprecation warnings it surfaces.

**3. Strictness rollouts.** A rule that was off goes on, tree-wide.
- TypeScript `strict: true`. Swift 6 strict concurrency. A new lint rule at `error`. mypy on a Python codebase.
- Counter: the number of diagnostics. First flip produces a wall of errors; the migration grinds it to zero.

**4. Deprecated API removal.** The platform moved on, your code hasn't.
- SwiftUI `ObservableObject` → the `@Observable` macro. Callbacks → async/await. Old SDK call shapes → current ones.
- Counter: grep for the deprecated symbol.

**5. Pattern unification.** Two ways of doing one thing become one way.
- Two HTTP clients → one. Raw `UserDefaults` calls scattered everywhere → a single settings manager. CommonJS and ESM mixed → ESM.
- Counter: call sites of the losing pattern.

[IMAGE: dark chalkboard, five labeled boxes in a row (swap, upgrade, strictness, deprecation, unification), each with a tiny before/after glyph inside and a small counter badge underneath, all five feeding into one seam-line icon]

![[migration-seams-five-families-1.png]]
![[migration-seams-five-families-2.png]]
![[migration-seams-five-families-3.png]]
![[migration-seams-five-families-4.png]]
![[migration-seams-five-families-5.png]]

Notice what every family shares: an old pattern you can grep for. That's not a coincidence. **The grep is the seam.**

---

## Turning a Wish into a Seam

Most cleanup ideas arrive as wishes. "Improve error handling." "Reduce tech debt." "Make the API layer consistent." None of these are seams, but almost all of them contain one.

The move is to ask: **what checkable fact would be true if this wish came true?**

- "Improve error handling" contains "every route handler returns a typed `AppError`, zero bare `catch` blocks in `src/api/`."
- "Make the API layer consistent" contains "every endpoint goes through the `createEndpoint` helper, zero raw `router.get` calls."
- "Reduce tech debt" contains ten different seams. Pick one.

You lose some of the wish in the conversion. That's the point. The part you kept is the part a machine can verify, which is the part an agent can actually finish.

[IMAGE: dark chalkboard, a cloud labeled "improve error handling" passing through a funnel labeled "what fact would be true?", emerging as a crisp rectangular seam doc with a grep counter stamped on it, discarded vague wisps falling beside the funnel]

![[migration-seams-wish-to-seam-1.png]]
![[migration-seams-wish-to-seam-2.png]]
![[migration-seams-wish-to-seam-3.png]]
![[migration-seams-wish-to-seam-4.png]]
![[migration-seams-wish-to-seam-5.png]]

---

## Why Checkability Is the Whole Game

Here's the payoff, and the setup for the next video.

Once a migration has a seam, every batch of changes the agent makes can be checked by your build, your tests, and your grep counter. Failures feed straight back to the agent. The work converges instead of drifting, because "done" is a number that only moves one direction.

That loop is what let Stripe run a codebase-wide migration on 50 million lines of Ruby in a day, where the hand path was estimated at a whole team for over two months.

Source: Anthropic's Claude Fable 5 launch post, June 9, 2026

The model mattered. But the thing that made 50 million lines tractable wasn't intelligence. It was that someone defined the seam, so every one of the thousands of patches had an objective check waiting for it.

---

## Demo

1. Open a real repo on camera. Ask Claude Code to scout it for seams with a hunting checklist: outdated majors in `package.json`, disabled strictness in tsconfig and eslint config, grep for mixed patterns (two date libraries, two HTTP clients, raw storage calls), deprecated API usage, TODO and FIXME markers.
2. Show the ranked output: three or four candidate seams, each with a real blast-radius count from grep.
3. Pick one. Write the five-part seam definition live, in one markdown file, against the clock. Beat the fifteen-minute test on camera.
4. Run the counter command for the before-state and pin the number on screen. That number is where the next video begins.
5. Show a wish ("clean up the settings code") converted live into a seam ("57 raw UserDefaults sites → 0, all keys preserved") using the what-fact-would-be-true move.

---

## Key Insight

> A seam is a migration you can measure. If you can't put a number on how done you are, you don't have a migration, you have a wish, and an agent can't finish a wish.

---

After this video, you'll never look at your tech debt list the same way. It isn't a list of chores. It's a list of seams waiting for a paragraph.

Next video: we take one seam and run the full migration along it, with an agent doing the typing and a counter running to zero.
