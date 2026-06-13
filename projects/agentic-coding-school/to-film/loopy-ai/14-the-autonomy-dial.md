---
duration: "12-16 min"
batch: 5
order: 14
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "The Autonomy Dial"
aliases: [the-autonomy-dial]
status: stub
---

Stub for the L6-adjacent segment. How much rope to give a loop — decided per action, not per loop.

## Thesis

Every action a loop takes sits somewhere on a dial from *do it silently* to *never without me*. Most people set this dial **once, per loop, globally** — and they get it wrong in both directions at the same time. Too tight and the loop stops every five minutes for things you'd always wave through, so you babysit it and the autonomy was a lie. Too loose and one morning it has sent the email, force-pushed the branch, or closed the ticket, and now you're explaining yourself.

The fix is the thing [[governance-primitives]] gives you the brake for but never names: the dial is **per-action, not per-loop**. A single loop should ship a formatting fix silently *and* refuse to send an email *and* surface an ambiguous API choice for you to call — all in the same run. The skill of this segment is writing the policy that sorts each action into the right notch automatically, so the loop self-governs instead of asking you about everything or nothing.

This is the segment that answers the question every student actually has after they've seen Ralph and /goal run unattended: *"...but how much do I let it actually do?"*

## The four notches

Name them on camera. The dial isn't autonomy-vs-not, it's four positions:

1. **Ship silently** — fully reversible, low stakes, cheap for the loop to verify. It does it; you may never look. *Formatting, drafts in a scratch dir, internal refactors behind passing tests.*
2. **Ship and log** — reversible, but you want a trail. It does it and writes one auditable line. *Commits, slide decks, file moves, generated assets.* This is the tier people forget, and forgetting it is why they only have "silence" or "interrupt" with nothing between.
3. **Surface as a decision** — ambiguous or a soft one-way door, not catastrophic. It stops and hands you the **call, not the diff**: "A or B, A is faster but loses property X, recommend A — your call." *Which of two designs, whether to touch a shared module.* (This is the [[keeping-you-in-the-loop]] "decisions" channel.)
4. **Never without me** — irreversible *and* public or costly. It drafts and waits. *Sending email, prod migration, public post, spending real money, closing its own ticket.*

## The axes that move an action up a notch

The primary axis is **reversibility** — Parsons' "is this reversible *without embarrassment*?" The trap: reversibility is about the *world*, not the filesystem. The model thinks the email is reversible because it can delete it; but the recipient already read it. Judge the embarrassment, not the undo button.

Three secondary axes push an action higher even when it's technically reversible:
- **Blast radius** — how many people see it, how many systems it touches.
- **Verifiability** — can the *loop* check its own work, or only you? Low verifiability forces it up toward "surface."
- **Cost** — tokens, money, reputation. Spending is never notch 1.

## How you encode it (this is intent, not a prompt)

The dial lives in the **intent doc**, not in the loop's prompt — straight continuation of [[mission-command]]. You don't enumerate every possible action. You give:
- a **rubric** ("reversible + low blast radius + loop-verifiable → ship-and-log"),
- a hard, **explicit "never" list** (the one-way doors), and
- the **escalation format** for notch 3 (call + options + recommendation).

The loop reads the policy and self-sorts. That's the whole move: you're writing a sorting function for actions, once, instead of approving actions one at a time forever.

## Dial vs. ladder — don't conflate them

[[l1-essentials]] teaches Aakash Gupta's autonomy *ladder* (levels 1–6). That ladder is about **how long** a loop can run unattended — a *harness capability* (skip-permissions, context management, subagents, Ralph, VPS). The dial is about **which actions** it may take while running — a *policy*. Orthogonal axes that the word "autonomy" smears together. Levels 1–3 buy you duration; the dial decides what the loop is allowed to *do* with that duration. A level-6 always-on loop with a tight dial is safe; a level-2 loop with no dial can still email your investors.

## The diagnostic

- If your loop interrupts you for things you'd **always** approve → the dial is too tight. Demote those actions a notch.
- If it has **ever** done something you'd have stopped → the dial is too loose. Promote that action and add it to the "never" list.
- Tune notch by notch, per action. The dial is never set once; it's the thing you adjust as trust accrues.

## Failure modes

- **Set per-loop, not per-action.** The original sin — forces every action to the most cautious or most reckless setting the loop ever needs.
- **A vague "never" list** ("don't do anything risky"). The model interprets generously. The list must be concrete one-way doors.
- **No ship-and-log tier.** You get either silence (no audit trail, cognitive debt) or constant interruption. The middle tier is where trust is actually built.
- **Reversibility judged on the filesystem, not the world.** See the email trap above.
- **Letting the loop self-grant.** The loop must not edit its own dial. The dial is human-owned, same as the kill switch in [[governance-primitives]].

## What this segment is *not*

- Not [[governance-primitives]]. That's the brake — budgets, kill switches, retirement, scoped to the *loop*. This is the *per-action policy* for what a running loop may touch. Pair, not duplicate.
- Not [[keeping-you-in-the-loop]]. That's the delivery interface — *how* surfaced work and decisions reach you. This decides *which* actions get surfaced in the first place. Film them to reference each other: the dial produces the items, that segment shapes the pipe.
- Not the autonomy ladder. See the dial-vs-ladder beat.

## Sources / refs

- Chris Parsons workshop (June 2026): "is this reversible without embarrassment?", the per-action ship/draft split, never letting a worker close a ticket, drafts-not-sends for email. The reversibility heuristic is lifted directly from here — this segment promotes it from a one-line bullet in [[keeping-you-in-the-loop]] to its anchor.
- Builds on [[governance-primitives]] (the brake) and [[mission-command]] (intent doc as the home for the dial).
- Pairs forward into [[l4-workers]] and [[l5-discovery]] — both need a per-action policy before they run unattended; they should reference "the dial" rather than re-deriving it.
- Aakash Gupta autonomy ladder via [[l1-essentials]] (the axis this segment is explicitly *not*).

## TODO

- Demo: open a real intent doc's autonomy policy block — show the concrete "never" list and the ship-and-log rubric. Run a loop that hits a notch-4 action (drafting an email) and watch it stop and surface; then a notch-1 action it just does silently. Show one notch-3 decision surfaced as call+options+recommendation, answer it in one line, watch the loop continue.
- Image: a literal rotary dial with four labelled notches (silent / log / surface / never), an "action card" being sorted into one of them by reversibility + blast radius.
- Decide: does the email-reversibility trap deserve its own beat or stay inside the axes section? It's the stickiest example.
