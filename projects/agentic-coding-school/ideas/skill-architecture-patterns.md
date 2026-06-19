---
tags: [skills, architecture, claude-code, research]
date: 2026-04-11
aliases: [skill-split-vs-merge, producer-consumer-skills, shared-state-skills]
status: "idea"
---

Working notes on how to decide when a Claude Code skill should be one skill, two skills, or three — and how skills should share state when they need to talk to each other. Started after migrating the youtube-thumbnail-generator + youtube-ab-tester pair into a clean producer-consumer loop with `feedback.json` as the bridge.

## The tension

Every skill system hits the same problem eventually: cohesion vs coupling.

- **Merge too much** → the skill's one-line description becomes vague, context gets polluted with irrelevant instructions, the model's attention thins across too many responsibilities. You end up with an 8K-token "YouTube skill" that Claude doesn't quite know when to invoke.
- **Split too much** → you forget skills exist, producers drift from consumers, and you pay an integration tax every time the system needs to learn from itself.

Neither extreme wins. The interesting question isn't "split or merge?" — it's **what's the right seam to cut along?**

## The meta-rule: cut along trigger boundaries, not topic boundaries

Don't split skills by topic ("YouTube stuff"). Split them by **when they're invoked**. Two operations that happen at different moments, with different inputs, called by different user intents — those are two skills. Two operations that always fire in the same breath are one skill.

Three diagnostic questions:

1. **Different triggers?** When would the user invoke each one? If the answer is the same sentence, merge. If the answer is "different days, different intents," split.
2. **Different inputs?** Producer needs video content. Consumer needs a screenshot. Different inputs → different skills.
3. **Usable independently?** Would the user ever run one without the other? If yes → split.

When all three answers are "no" — same trigger, same input, never used alone — that's a strong merge signal.

## The turnaround-time heuristic

The single most useful axis for split-vs-merge is: **how much time passes between the producer's output and the consumer's feedback reaching back to the producer?**

| Loop time | Pattern | Example |
|---|---|---|
| Milliseconds | Merge — split overhead exceeds benefit | linter + fixer |
| Seconds–minutes | Usually merge, unless research step is reused | research → write |
| Hours–days | Split with shared state | thumbnail generate → upload → test results |
| Weeks–months | Split with explicit archives | build → ship → learn from users |

The longer the loop, the more the split buys you: discoverability, focused context, durable records. The shorter the loop, the more the split costs you: synchronization burden with no payoff.

## Producer-consumer is a real, named pattern

Producer-consumer is not just an OOP pattern — it's a legitimate skill architecture. It works when:

- The producer and consumer have **different triggers** (different user intents fire them)
- They have **different inputs** (each needs distinct context)
- The loop between them is **slow enough** that human checkpoints exist (otherwise just merge)
- There's a **shared state file** bridging the loop

Without the shared state file, the producer drifts away from what the consumer learns. With it, you get the best of both worlds: each skill stays small and discoverable, and the system as a whole still gets smarter over time.

```
producer ──writes──> output artifact
         <──reads── shared state ──written by──> consumer
```

The filesystem is the API. Neither skill imports the other. Neither skill needs to know the other exists in code. They communicate through files.

### Worked example: youtube-thumbnail-generator + youtube-ab-tester

| Question | Answer | Signal |
|---|---|---|
| Different triggers? | Yes — "make thumbnails for X" vs "here are the test results" | split |
| Different inputs? | Yes — video content vs screenshots | split |
| Usable independently? | Yes — generator for exploration, ab-tester for title-only tests | split |
| Loop turnaround? | Days to weeks (upload → wait → results) | split |
| Shared learnings? | Yes — what won, what didn't, why | needs shared state |

Verdict: stay split, add a shared state file (`feedback.json`) on the consumer side so the producer reads from where the learnings are actually written.

## Shared state — inside the skill, or outside?

Once you've decided multiple skills need to share state, the next question is **where the state lives**. Three options:

### Option A: state inside the producer

```
youtube-thumbnail-generator/
├── SKILL.md
└── feedback.json   ← shared state lives here
```

**When to use:** when only the producer reads it and it's mostly an internal config. **Problem:** if the consumer is the one generating the learnings, this is backwards. The data flows from consumer → producer, but the file lives in the producer's directory. The consumer has to reach across into another skill's folder to update it, which feels wrong and tends to rot.

### Option B: state inside the consumer

```
youtube-ab-tester/
├── SKILL.md
└── references/
    └── feedback.json   ← shared state lives here
```

**When to use:** when one skill is clearly the *source* of the learnings (the consumer, in producer-consumer setups) and the other skills *read* them. **Why this is usually right for producer-consumer:** the learnings are generated where the feedback arrives, so the file should live with the writer, and other skills read it.

### Option C: state outside both skills, in a shared folder

```
.claude/skills/
├── _shared/
│   └── youtube-feedback.json
├── youtube-thumbnail-generator/
└── youtube-ab-tester/
```

**When to use:** when **three or more** skills share the same state, or when no single skill is the obvious owner. **Cost:** you lose the locality benefit — the file isn't co-located with any one skill, so it's easier to forget. Add explicit pointers in every skill's SKILL.md that touches it.

### How to choose

- **One writer, one reader, clear owner** → put the state inside the writer (Option B).
- **One writer, many readers** → still inside the writer if the writer is obvious, otherwise Option C.
- **Many writers** → Option C, with a documented schema and ownership rules.

The default should be Option B when there's a clear writer. Don't reach for Option C unless you genuinely have multiple writers — premature centralization is its own kind of god-skill creep.

## Anti-patterns to watch for

These are the failure modes I've hit or been close to hitting:

1. **The topic-merge trap.** "It's all about YouTube, so it should be one skill." No — topic is the wrong axis. Cut by trigger, not by domain.
2. **The orphan state file.** Shared state living in a folder no skill explicitly owns or references. The file rots because no SKILL.md tells Claude to read it.
3. **The backwards owner.** Shared state living with the *reader* instead of the *writer*. The writer has to reach into another skill's directory, which feels wrong and discourages updates. (This was the `feedback.json` problem.)
4. **The sync-tax merge.** Two skills merged "for convenience" that are actually triggered at different moments. Now every invocation loads twice as much context as it needs.
5. **The discovery cliff.** Splitting a skill so finely that Claude can't find the right one. If three skills have nearly identical descriptions, they should probably be one skill with internal modes.
6. **The hidden coupling.** Two skills that import each other's filenames in code. If the integration is in code rather than in files, you've recreated the coupling problem the split was supposed to solve.

## Open questions to explore

Things I want to think about more as I migrate other skill pairs:

- **Schemas for shared state files.** Should `feedback.json` and `uploaded.json` follow a documented schema, or is JSON-with-conventions enough? Schemas help when multiple skills write; conventions are lighter when one skill writes.
- **Versioning shared state.** When the schema changes, how do we migrate without breaking older files? (For thumbnails: just edit them in place, since there's only one writer. For multi-writer state, this gets harder.)
- **Discoverability pointers.** Should every skill that touches a shared state file have a "Related skills" section in its SKILL.md? Probably yes — discoverability is the main cost of splitting.
- **When should `_shared/` folders exist at all?** I'm wary of them. Maybe never, until I genuinely have three writers.
- **Skills that span multiple sessions.** Producer fires in one session, consumer fires weeks later in another session. The shared state file is the only continuity. How do we make sure Claude remembers to check it?
- **The "skill index" idea.** A top-level file that lists all skills and their relationships (producer-of, consumer-of, shares-state-with). Would Claude actually use this, or would it just rot?

## Candidate skill pairs to audit with this framing

Skills I suspect have the same producer-consumer structure as the thumbnail pair, and might benefit from the same migration:

- **trend scouts → ideas queue → script writers.** Three-stage pipeline. Currently each scout has its own output. Should there be a shared `ideas-queue.json`?
- **multi-platform writers (X, LinkedIn, newsletter).** Each one currently produces drafts in its own folder. Should there be a shared `drafts-archive/` that all of them read from to avoid repeating angles?
- **research skills (supadata, exa, websearch).** Currently each writes its own output. Should there be a shared `research-cache/` to avoid duplicated fetches across skills?

These are speculative — I'd want to apply the three diagnostic questions to each before committing.

## The summary, if I had to put it on one card

> Cut skills along trigger boundaries, not topic boundaries.
> When the loop between two skills spans more than a few seconds, split them and add a shared state file.
> Put the state file with the writer, not the reader.
> Don't reach for a `_shared/` folder until you genuinely have three or more writers.
> The filesystem is the API.
