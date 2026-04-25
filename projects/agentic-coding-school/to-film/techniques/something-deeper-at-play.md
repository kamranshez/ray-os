---
duration: "3-5 min"
class: "techniques"
chapter: "Fundamental Techniques"
---

# "Something deeper at play?" — Forcing a layer diagnosis before accepting a fix

## What This Video Covers

A prompting technique for reviewing fixes — your own, a subagent's, or an open PR — that forces the model to diagnose the *layer* a fix lives at (symptom vs proximate cause vs root cause) rather than just rubber-stamping that it "works."

The trigger phrase is literally **"is there something deeper at play?"** — or variants. It sounds casual, but it does something structural: it gives the reviewer permission to reject the framing, not just the fix.

## Why This Matters

Coding models have a strong bias toward the happy path. When they see an error, their default instinct is:

> error is bad → make the error go away → done

This produces bandaids that pass every test but leave the real bug intact:

- A null check where the null should never have existed
- A `catch` block that swallows an exception the caller needed to see
- A Sentry filter that hides a class of error instead of fixing why it fires
- A retry that masks a race condition instead of fixing the ordering

The common question "did you actually fix the underlying problem?" **doesn't work well** — it's binary, and the model will almost always answer yes. You need a phrasing that invites a *position*, not a *confirmation*.

## The real example: PR #133

From a recent HyperWhisper session. The PR:

> `fix(macos): drop cancelled tasks from post-process Sentry capture`

**What it did:** in the `catch` block of the cloud post-processing call, detect cancellation (`CancellationError`, `NSURLErrorCancelled`, `Task.isCancelled`) and skip `SentryService.capture(...)`.

**Why it looked fine:** Sentry noise went away. Tests passed. User-visible behavior unchanged.

**What was actually happening:** cancellation wasn't modeled in control flow at all. A cancelled task was still:

- running through the retry loop
- sleeping through backoff after being cancelled
- being logged as a failure
- flowing into the generic error handler

The Sentry flood was the most *visible* symptom, but it was one of four. The PR fixed one symptom and left three in place.

When the reviewer was asked a normal review question, it approved the fix. When asked **"do you agree or disagree with the fix, or is there something deeper at play?"** — it diagnosed the layer mismatch immediately and proposed treating cancellation as first-class control flow (throw early, don't retry, don't log as failure, propagate up).

The prompt didn't change the code. It changed how the reviewer *read* the code.

## The technique

When a fix lands — yours, a subagent's, or an open PR — ask **one of these** instead of "did it fix it?":

1. **"Do you agree or disagree with the fix, or is there something deeper at play?"**
   - Invites a position. Opens the door to reframing.

2. **"What's the symptom, what's the proximate cause, and what's the root cause? Which one does this fix address?"**
   - Forces the three-layer split explicitly. Hardest to hand-wave past.

3. **"If this bug reappeared tomorrow in a different file, would this fix prevent it?"**
   - Tests whether the fix generalizes or just patches one code path.

4. **"List three ways this fix could still be wrong."**
   - Adversarial self-review. Surfaces the "this hides the bug instead of fixing it" class.

The key property of all four: they **don't invite a yes/no**. They invite structure.

## Why the phrasing matters

"Did you fix the underlying problem?" fails because:

- it's answerable with "yes"
- "yes" closes the conversation
- the model has no reason to re-read the code through a critical lens

"Is there something deeper at play?" works because:

- it presupposes that *maybe* there is
- it costs the model nothing to say "yes, here's what"
- it doesn't attack the PR author — it invites analysis
- it shifts the reviewer's job from *validation* to *diagnosis*

This is the same reason "what could go wrong?" beats "will this work?" in design review.

## Key Concepts to Cover

- Why coding models default to symptom-patching (happy-path bias, reward for errors-going-away)
- The three layers: symptom → proximate cause → root cause
- Why "did you fix the underlying problem?" is a weak prompt (binary, confirmation-inviting)
- Why "is there something deeper at play?" is a strong prompt (invites position, not confirmation)
- The PR #133 walkthrough as a concrete example
- When to use it: any non-trivial fix, especially ones that make errors *disappear* rather than change the code flow
- When NOT to use it: trivial changes where there is no deeper layer (typo fixes, renames, copy changes)
- Bake it into CLAUDE.md / system prompts rather than asking per-turn — durable wins over ad-hoc

## Durable version (put in CLAUDE.md)

Instead of asking per-turn, make the model volunteer the layer analysis:

> Before proposing a fix, state the symptom, the proximate cause, and the root cause separately. If they're the same, say so explicitly. If the fix is at the symptom layer, justify why — don't just do it silently. When reviewing an existing fix, ask whether the fix is at the right layer, not just whether it works.

## Demo Plan

1. Open the HyperWhisper repo and show PR #133 as it was originally submitted
2. Show a normal review prompt: "does this PR fix the issue?" — model approves
3. Show the "is there something deeper at play?" prompt — model diagnoses the control-flow issue
4. Walk through the improved fix (cancellation as first-class control flow, no retry on cancel, etc.)
5. Show the three-layer diagnosis: symptom (Sentry noise), proximate (catch misclassifies), root (cancellation not modeled)
6. Bonus: add the durable version to CLAUDE.md and re-run on a different PR — show the model volunteers the layer analysis unprompted

## Suggested Class Placement

Techniques — Fundamental Techniques. Pairs well with *Subagent Verification Loops* (which handles *who* reviews) and *Prompt Contracts* (which handles *what* done means). This technique handles *how deeply* the reviewer reads.
