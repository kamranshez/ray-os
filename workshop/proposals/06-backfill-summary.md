# Backfill summary

Frontmatter added to every workshop `content/*.md` (including `agent-teams/`). Each file now declares its `mapping`, `day`, `block`, and the `(class, title)` pairs that name the corresponding ACS videos.

## Stats

- **Files edited**: 69
- **mapped**: 32 — full ACS coverage; stub stays as a pointer
- **mapped-partial**: 15 — ACS covers some of the topic; workshop adds framing
- **workshop-original**: 22 — no ACS video; `recording-needed: true`

## Recording-needed list (22 files)

These have `mapping: workshop-original` and need net-new recording:

### Day 1 — Alignment
- `Status of Agents.md`
- `auto-advancing-design-destroys-implementations.md`
- `models-drift-toward-two-possible-truths.md`
- `Missions.md` *(part of the Missions/Goals merge)*
- `Defining Good Goals.md` *(merge)*
- `goal.md` *(merge)*

### Day 2 — Steering
- `long-context-demands-active-human-steering.md` *(part of the long-context trio merge)*
- `long-context-inverts-dumb-zone-advice.md` *(merge)*
- `recent-context-dominates-attention.md` *(merge)*

### Day 3 — Context Architecture
- `context-strategy-correlated-with-engagement.md`

### Day 4 — Skills
- `teach-models-to-think-like-your-engineers.md`

### Day 5 — Automation
- `Automate Anything and Everything.md`
- `OpenAI Symphony.md`

### Day 6 — Verification
- `Languages.md`
- `files-matter-less-in-agent-friendly-languages.md` *(part of the Languages merge)*

### Day 7 — Agent Teams & Loopy AI
- `Removing Bottlenecks.md`
- `agent-teams/convergence-over-perfection-thesis.md`
- `agent-teams/01-solo-plus-cheap-verifier.md`
- `agent-teams/02-parallel-voters.md`
- `agent-teams/03-generator-plus-adversarial-critic.md`
- `agent-teams/04-decomposed-swarm-independent-errors.md`
- `agent-teams/05-environmental-attractors.md`

Counting the merges as single videos and the archetypes as 6 distinct recordings: **roughly 13 net-new videos** to record for the workshop spine. Matches the Recording Plan section already in `Class Structure.md`.

## Ambiguous cases (need Ray's call)

A few stubs had multiple plausible ACS targets — I made a judgement call but flag them here so you can override:

- **`Workflows.md`** (root stub: "fresh context windows each phase, 3 approaches…"): tagged `mapped-partial` against CC "Automatic Plan Reviewing with Other CLIs" because that's the closest concrete demo. The comprehensive proposal suggests retiring this stub entirely and folding into [[Compaction]] (Day 2) + Day 7 — consider acting on that.
- **`Subagent Architectures.md`**: tagged `mapped-partial` against AT "Multi Subagents for Hard Problems" + "Refactoring with Subagents" + CC "Subagent Teams for Debugging". The note is the workshop's "wiring patterns" framing; the three videos are concrete cases. Could equally be Day 7 instead of Day 3 if you treat it as part of Agent Teams.
- **`Ordering.md`**: placed on Day 2 deep-cut against CC "Different Orderings" because Class Structure currently has it there, but the Day 3 (Context Architecture) is arguably a better home — the Carlini story is about *what context the agent gets* across iterations.
- **`Verification Architectures.md`**: tagged `mapped-partial` against AT "Mixing Models & Modes" + "Combining CLIs & Models". The stub itself is one line — the comprehensive proposal flagged it for possible cut.
- **`Goal In Strategy Out.md`** vs. **`Missions.md` / `Defining Good Goals.md` / `goal.md`**: kept the PE video stub separate (`mapped`) and left the three merge notes as `workshop-original`. The merge target — when written — should pull from the PE video plus the three X threads.

## Where the merges land

The frontmatter doesn't model "this stub is part of a merge" — but the four currently-pending merges are:

1. **Missions/Goals**: `Missions.md` + `Defining Good Goals.md` + `goal.md` (+ `Goal In Strategy Out.md` as supporting video)
2. **Long-context trio**: `long-context-demands-active-human-steering.md` + `long-context-inverts-dumb-zone-advice.md` + `recent-context-dominates-attention.md`
3. **Adversarial overlap**: `Adversial Reviewers.md` ↔ `agent-teams/03-generator-plus-adversarial-critic.md`
4. **Languages pair**: `Languages.md` + `files-matter-less-in-agent-friendly-languages.md`

When a merge happens, the resulting single note inherits the higher of the source mappings (workshop-original > mapped-partial > mapped) and `recording-needed: true` if any source needed recording.
