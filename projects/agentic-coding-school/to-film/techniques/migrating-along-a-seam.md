---
duration: "12-16 min"
batch: 1
order: 2
batch_name: "Cleaning Up Legacy Code"
class: "techniques"
chapter: "Cleaning Up Legacy Code"
---

## One Paragraph, One Counter, One Merge Button

In this video I migrate a real production app, the one my users run every day, off a deprecated pattern. Two hundred twenty call sites across forty files. An agent does all the typing.

My entire contribution is three artifacts: one paragraph, one green checkmark, and one merge button.

Last video defined the seam: a migration with a checkable before and after. This video is the execution playbook, how you actually run a migration along a seam without the agent drifting, breaking your app, or handing you a forty-file diff nobody can review.

---

## Why Long Migrations Break Agents

Quick recap of the failure mode, because the whole playbook exists to prevent it.

An agent patches file 30 confidently. By file 200, it has lost track of an invariant that lived in file 12. Nothing errors at the time. The drift is silent, and you spend longer debugging the patch trail than the manual migration would have taken.

The fix is not a smarter model. The fix is structure: **never let the agent take a step that isn't checked.**

That structure has a name, straight from how Stripe's result was described: a planning loop wrapped around a patch loop wrapped around a verification loop.

Source: Anthropic's Claude Fable 5 launch post, June 9, 2026

---

## Three Loops, Not One Prompt

[IMAGE: dark chalkboard, three concentric rings, outer ring labeled PLANNING with a human icon, middle ring labeled PATCHING with an agent icon, inner ring labeled VERIFICATION with a gear and checkmark, a merge button drawn outside all three rings with a human hand on it]

![[migrating-seam-three-loops-1.png]]
![[migrating-seam-three-loops-2.png]]
![[migrating-seam-three-loops-3.png]]
![[migrating-seam-three-loops-4.png]]
![[migrating-seam-three-loops-5.png]]

- **Outer loop, planning.** You write the seam definition. Before, after, scope, invariants, done-when. This happens once, up front.
- **Middle loop, patching.** The agent emits changes in batches, one intent at a time.
- **Inner loop, verification.** Your build, tests, and grep counter check every batch. Failures feed straight back into the agent's next prompt.

The ownership split is the strategy: **you own the outer ring, the machine owns the middle, your gates own the inner ring, and a human owns the merge button.**

You never review the agent's process. You review its output against the contract.

---

## The Playbook

Six steps. Each exists because skipping it is a known way migrations die.

**1. Sandbox branch.** The agent never touches main. `git checkout -b migrate/observable`. Cheap, obvious, skipped surprisingly often.

**2. Wire the gates.** One command that decides whether a batch passed. For a Swift app that's `xcodebuild build && xcodebuild test`. For a TypeScript app it's `npm run typecheck && npm test && npm run build`. The agent's opinion of its own work counts for nothing. The gates decide.

**3. Size the batches.** The right batch is **the largest unit your gates can verify in one clean run**. Usually one folder or one intent's worth of files. Keep the full cycle under fifteen minutes so the agent stays in the loop instead of sitting on a queue.

[IMAGE: dark chalkboard, a repeating cycle diagram: agent emits batch → gates run → fork into green path (commit, counter ticks down) and red path (failure log arrow feeding back into the agent's next prompt), drawn as a loop with the fork clearly visible]

![[migrating-seam-batch-cycle-1.png]]
![[migrating-seam-batch-cycle-2.png]]
![[migrating-seam-batch-cycle-3.png]]
![[migrating-seam-batch-cycle-4.png]]
![[migrating-seam-batch-cycle-5.png]]

**4. Feed failures back.** When a batch fails, the failure output goes into the next prompt, verbatim. This is the loop converging. A failed batch isn't a setback, it's the system working.

**5. One PR per intent.** Group the patches by what they mean, not by when they happened. "Migrate settings managers." "Migrate onboarding views." Six small PRs a human can actually read, instead of one forty-file diff nobody can.

[IMAGE: dark chalkboard, split panel, left side one giant tangled diff labeled 40 FILES with a crossed-out reviewer, right side a neat vertical stack of six small PR cards each with a one-line intent label and a checkmark, reviewer icon smiling]

![[migrating-seam-pr-stack-1.png]]
![[migrating-seam-pr-stack-2.png]]
![[migrating-seam-pr-stack-3.png]]
![[migrating-seam-pr-stack-4.png]]
![[migrating-seam-pr-stack-5.png]]

**6. Plan the rollback before the first patch.** Even with green gates, anything this size needs a documented way back. Write it down before anything lands.

---

## The Loop as Code

The inner loop is simple enough to express as a shell script. You won't run this literally, Claude Code's own loop does the job, but seeing it as code makes the idea stick:

```bash
while [ "$(rg -c 'ObservableObject' app/ | wc -l)" -gt 0 ]; do
  # agent emits one batch, one intent
  claude -p "Next batch per SEAM.md. Fix these failures first:
  $(cat .last-failures)"

  # the gates decide, not the agent
  xcodebuild build && xcodebuild test \
    && git commit -am "batch: $(cat .batch-intent)" \
    || xcodebuild test 2>&1 | tail -50 > .last-failures
done
```

Read the loop condition again. **The agent never decides it's done. The grep decides.**

---

## The Counter and the Crash

Two things carry the demo, and they're the two things you should watch in any migration you run.

**The counter.** The seam's grep count is a live progress bar for the whole migration. It only moves one direction. 220 → 187 → 141 → 96 → 0. When it stalls, something is wrong. When it hits zero, you're provably done.

**The invariant.** Every real migration has at least one rule the compiler can't enforce. In mine, it's brutal: in SwiftUI, a view that consumes a value with `@EnvironmentObject` and the producer that injects it with `.environmentObject()` live in different files. Migrate one without the other and the app builds clean, then **crashes at launch.**

```swift
// BEFORE: these two lines are in different files
struct RecorderView: View {
    @EnvironmentObject var manager: RecordingManager  // consumer
}
.environmentObject(RecordingManager())                // producer

// AFTER: they must flip together, or runtime crash
struct RecorderView: View {
    @Environment(RecordingManager.self) var manager
}
.environment(RecordingManager())
```

[IMAGE: dark chalkboard, two file icons far apart connected by a dotted thread labeled INVARIANT, one file half-migrated glowing green with a compiler checkmark, the running app below them exploding with a crash symbol, caption "compiles fine, crashes at launch"]

![[migrating-seam-invariant-crash-1.png]]
![[migrating-seam-invariant-crash-2.png]]
![[migrating-seam-invariant-crash-3.png]]
![[migrating-seam-invariant-crash-4.png]]
![[migrating-seam-invariant-crash-5.png]]

This is exactly why invariants go in the seam doc, and why "it compiles" was never the done-when. The gates must include something that exercises runtime behavior: a launch smoke test, a snapshot suite, anything that would catch what the compiler can't.

---

## Lock It In with a Ratchet

One addition of my own, this isn't from the Stripe playbook, it's standard migration engineering from teams like Google and Shopify: when the counter hits zero, **make it impossible for the count to go back up.**

```yaml
# CI: the migration can never regress
- name: seam-guard
  run: |
    if rg -q 'ObservableObject|@Published|@EnvironmentObject' app/; then
      echo "deprecated observation pattern reintroduced" && exit 1
    fi
```

[IMAGE: dark chalkboard, a one-way ratchet gear on a timeline, counter values descending 220 to 0 along the gear's teeth, a pawl labeled CI GUARD blocking the gear from turning backward, a small rejected commit bouncing off it]

![[migrating-seam-the-ratchet-1.png]]
![[migrating-seam-the-ratchet-2.png]]
![[migrating-seam-the-ratchet-3.png]]
![[migrating-seam-the-ratchet-4.png]]
![[migrating-seam-the-ratchet-5.png]]

The migration isn't done when the count hits zero. It's done when it can't come back.

---

## The Bottleneck Moves

Here's what changes once you run one of these, and it's the idea to walk away with.

The agent types faster than your whole team. So the timeline no longer scales with codebase size. It scales with two things you control: **how fast your gates run, and how fast a human can review small PRs.**

Stripe's version of this: a 50-million-line Ruby codebase migrated in a day, against a hand estimate of a whole team for over two months. Their secret weapon wasn't just the model. It was CI fast enough to keep the inner loop hot, and a review process ready for a structured patch trail.

Source: Anthropic's Claude Fable 5 launch post, June 9, 2026

[IMAGE: dark chalkboard, a bottleneck diagram, wide pipe labeled AGENT TYPING flowing into a narrow neck labeled GATES + REVIEW, an arrow showing the constraint moved from the left of the pipe to the neck, old bottleneck position crossed out]

![[migrating-seam-bottleneck-moves-1.png]]
![[migrating-seam-bottleneck-moves-2.png]]
![[migrating-seam-bottleneck-moves-3.png]]
![[migrating-seam-bottleneck-moves-4.png]]
![[migrating-seam-bottleneck-moves-5.png]]
![[migrating-seam-bottleneck-moves-6.png]]

Which means your job changes. Senior engineering effort stops going into the typing and starts going into the paragraph, the gates, and the review. Score your result against your own hand baseline, not Stripe's headline. Their CI is not your CI.

---

## Demo

1. Open HyperWhisper, my production macOS app. Show the seam doc written in the last video: 32 classes on `ObservableObject`, 189 `@Published` properties, 220 total sites across 40 files, migrating to the `@Observable` macro.
2. Pin the counter on screen: `rg 'ObservableObject|@Published|@EnvironmentObject' | wc -l` → 220.
3. Sandbox branch, then wire the gate: `xcodebuild build && xcodebuild test` on the hyperwhisper scheme, 15 existing XCTest files behind it.
4. Batch 1: the settings managers folder. Agent migrates, gate runs, green, commit. Counter drops. Time-lapse batches 2 through 4 with the counter ticking down on screen.
5. The crash beat: a batch converts a view's `@EnvironmentObject` while its producer is still on `.environmentObject()`. Build passes. Launch the app. Crash. Paste the crash log into the agent, watch it fix the producer in lockstep, gate goes green.
6. Counter hits zero. Run the full gates one final time, all green.
7. Add the CI seam-guard so the pattern can never return, then show the PR stack: six PRs, one intent each, and merge them on camera.
8. Close on the wall-clock math: agent time versus my estimate for doing this by hand.

---

## Key Insight

> An agent migration converges when every step is checked and no step is trusted. You write the contract, the gates enforce it, the counter proves it, and your only manual act is the merge.

---

You now have the full method: find the seam, write the paragraph, wire the gates, let the counter run to zero, ratchet it shut.

Pick the oldest item on your migration backlog this week. It was never too hard. It was just unchecked.
