---
tags: [lesswrong, acs, content-gap, pipeline, research]
aliases: [lesswrong-acs-gap-design]
date: 2026-07-26
status: designed-not-run
---

Retrieval pipeline and design rationale for mining LessWrong for agentic-coding techniques
that Agentic Coding School has not covered.

**Status: the retrieval half is DONE and its outputs are in this folder. The analysis half
(running each post through the gap-check) has NOT been run.** Designed 2026-07-26, rescued
out of an ephemeral job scratch dir on 2026-07-27 before it got cleaned up.

Original ask: *"Inside of Agentic Coding School I cover a lot of interesting techniques.
Some of them may be available on LessWrong, maybe in the last month or two. Find these
techniques, or find additional things I haven't already covered."*

## What is here

| File | What it is |
|---|---|
| `scripts/lw_pipeline.py` | Fetch + rank. The reusable core. |
| `scripts/export_bodies.py` | Writes each shortlisted post's full body to `bodies/`. |
| `scripts/lw_comments.py` | The comment / Shortform lane. |
| `scripts/lw_score.py`, `scripts/lw_search.py` | Superseded intermediates, kept for the query lists in `lw_search.py`. |
| `shortlist.json` | 83 ranked posts, banded A/B/C, each with a `body_path`. |
| `bodies/` | The 83 full post bodies as markdown, headed with score metadata. |
| `comment_shortlist.json` | 136 comments, 62 of them Shortform. |
| `aggregator_links.json` | 61 outbound links mined from Zvi's newsletters. |

The raw 22 MB corpus was deliberately NOT kept. It regenerates in 98 seconds.

## How to re-run

Run from this folder, NOT from `scripts/`. The scripts read and write `shortlist.json` and
`bodies/` relative to the current directory, so running them from `scripts/` would scatter a
second copy in there.

```bash
cd artefacts/lesswrong-acs-gap
python3 scripts/lw_pipeline.py fetch 2026-05-20 corpus.jsonl   # 98s, 1190 posts, 22 MB
python3 scripts/lw_pipeline.py rank  corpus.jsonl              # 13s, fully local
python3 scripts/export_bodies.py     corpus.jsonl              # one .md per shortlisted post
PYTHONPATH=scripts python3 scripts/lw_comments.py 2026-05-20   # optional: Shortform lane
rm corpus.jsonl                                                # do not commit the 22 MB corpus
```

`lw_comments.py` imports the anchor vocabulary from `lw_pipeline.py`, hence `PYTHONPATH`.
Change the date to move the window. Everything is unauthenticated; no API key.

## The shortlist: 7 posts that survive the practitioner filter

Out of 83 ranked candidates, these 7 pass all three gates (see decision rules below).

1. **Tips on leveraging AI for empirical research** (Daniel Tan, k=28, 2026-07-06)
   `bodies/15-tips-on-leveraging-ai-for-empirical-research.md`
   The "command center" pattern: one top-level repo where memory and conventions accrue,
   real project repos as gitignored subdirs under `repos/{name}`, so feedback in one project
   improves all of them. Plus macro-verbs in CLAUDE.md ("SOP" expands to fresh worktree +
   task list + orchestrate + browsable UI). Plus agent post-mortems on past transcripts.
   Rated the best pick. Verified novel against the live catalog: closest existing video is
   "Reducing Agent Confusion in Growing Projects", which is single-codebase.

2. **Door's Locked, Try the Window** (Prakrat Agrawal, Apollo, k=68, 2026-06-24)
   `bodies/07-door-s-locked-try-the-window.md`
   File-level locks do not constrain a coding agent. Ask Claude Code or Codex CLI to fix a
   bug in a read-only file and it routes around the lock by monkeypatching and test warping
   rather than reporting the block. Opus 4.6 100%/40%, Sonnet 4.6 89%/66%, GPT-5.4 99%/94%
   (source-locked / test-locked). Telling the model not to edit read-only files does NOT
   work; only an explicit "stop and report" instruction holds. Same shape as the METR
   precedent: an evals paper with a one-step practitioner re-aim, and it hands over a
   phrasing rule. Verified novel: closest are "Dangerously Skip Permissions" (deliberate
   bypass) and "Agent Introspection".

3. **Expanding AI Control from Models to Harnesses** (fastfedora, k=19, 2026-07-15)
   `bodies/01-expanding-ai-control-from-models-to-harnesses.md`
   Highest anchor density in the whole corpus. Aim at the composition layer, not the
   primitives: permission types vs location vs precedence between them, compaction awareness
   and control, memory refinement. Do NOT pitch this as skills x subagents, because
   "Combining Skills & Subagents" already exists.

4. **Claude Code as a Claude Coach** (Brendan Long, k=40, 2026-07-06)
   `bodies/08-claude-code-as-a-claude-coach.md`
   Claude Code as a non-coding daily-workflow agent with persistent state: a personal trainer
   that prescribes workouts, logs sessions, adapts the program. 45 sessions of real tracked
   data plus a generated chart. Fits My Daily Workflows.

5. **Why Software Automation Is Hard** (silentbob, k=115, 20 comments, 2026-06-06)
   `bodies/06-why-software-automation-is-hard.md`
   Highest-engagement practitioner post in the window. Why coding agents have not moved the
   industry as much as expected. Contrarian framing; the comment thread is extra material.

6. **Bun's Migration from Zig to Rust** (Sayhan Yalvaçer, k=97, 2026-06-08)
   `bodies/05-bun-s-migration-from-zig-to-rust-as-a-potential-case-study-f.md`
   Case study, not a technique. A large influential OSS project migrated across languages
   almost entirely by Claude Code. Proof-of-scale, with a human-oversight angle. Only 847
   words, so cheap to read.

7. **Posting Some Prompts** (Arjun Panickssery, k=21, 2026-07-14)
   `bodies/16-posting-some-prompts.md`
   Artifact, not argument: raw prompts into a research-report scaffold with the Claude Code
   output alongside. Directly reusable. Only 203 words, so density normalisation is the sole
   reason it surfaced.

Near-misses if 8 or 9 are wanted: **Just a Wrapper? How Much Do Scaffolds Matter?**
(`bodies/02-*.md`, quantifies harness-vs-model attribution) and **Success Per Tokens**
(`bodies/24-*.md`, cost-per-success as the metric, sweep reasoning modes in your agent).

Two titles that look like hits but are NOT: "Sub-agent delegation chaining" is a
cryptographic-verification proposal for rogue deployments, and "Guardian Angels" is LLM
personalisation whose only anchor is a loose use of the word "harness". Both die to the
practitioner filter despite ranking high.

## Findings that drove the design

These are the reason the pipeline looks the way it does. Losing them means rebuilding blind.

### The 2000-char cap was the entire recall bottleneck

`plaintextDescription` AND `plaintextMainText` on the LessWrong GraphQL API are both hard
capped at 2000 characters. `contents { markdown }` is uncapped (14,923 chars on a 2,238-word
post). Any title-and-intro filter is structurally blind to techniques that appear past the
intro.

Proof: **Tips on leveraging AI for empirical research** was the single best post found, and
it was unreachable by construction. The title says "empirical research", the intro is
disclaimers about personal circumstances, and every actual technique sits past the cap.
Same failure on Bun's migration (k=97, reads as a programming-language post, "done almost
entirely by Claude Code" is buried in the body).

Cost: 1190 posts = 21.4M chars = 22.0 MB = roughly 5.3M tokens, in 98s at 100 posts/request.
For 50 posts it is 0.82 MB / ~200k tokens / 4.4s.

### Rank by density, not counts

Weighted anchor hits per 1,000 words, floored at 300 words. Raw counts rank by length, which
is why Zvi's 7k-17k word newsletters dominated the first attempt on frequency alone. Density
normalisation moved Guardian Angels from rank 463 to 60.

The gate operating point was chosen by measuring recall against 10 known-good posts, not
guessed:

| gate | shortlist size | recall vs the 10 |
|---|---|---|
| dens>=8 / dens>=15 | 41 | 7/10 |
| dens>=5 / dens>=10 / karma>=20 | 59 | 9/10 |
| **dens>=3 / dens>=6 / karma>=10** (shipped) | **83** | **10/10** |

83 of 1190 is 7%. Banded A(25) / B(25) / C(33) for triage, because tail precision collapses:
a ZBiotics RCT lands at rank 38.

### `search_videos` has silent recall failure, proven three times

The MCP catalog search quoted a video's own `agentContext` back at itself and that video did
not appear in the top 10. The starkest case: querying "Proxyman SSL certificate HAR export"
failed to return *How to Reverse Engineer Claude Code*, whose own context literally says
"Proxyman setup, SSL certificates... exporting HAR files". It returned *Terminal Commands
(for Beginners)* and *Installing Warp* instead. There is no pagination: exactly 10 results,
always, out of 362.

**Consequence for any gap-check built on this: absence from the top 10 is not evidence of
absence.** A "net-new" verdict can never rest on search alone; it needs a disk-index scan.
A "covered" verdict is invalid without a verbatim transcript quote.

### Much of the 362-video catalog is plan, not filmed library

Re-running a query with `completedOnly: true` collapsed 10 hits to 1. Every subagent video
that matched (Nested Subagents, Forked Subagents, Quick Spawning Subagents, `--agent`) is
`isCompleted: false`.

**Consequence: an unfiltered "already covered" verdict actually means "already on the plan",
which is completely different advice.** It needs its own verdict tag, because saying
"covered" while pointing at an unfilmed video is actively wrong.

### Titles alone cannot carry a gap verdict

The real catalog contains titles like `Intro`, `Example`, `Maintenance`, and `Signal to
Noise`. A screening agent learns nothing from `Example`. Corrected design: inlined titles
*nominate* candidates, an `agentContext`-bearing index on disk *concludes*.

### The practitioner-relevance filter: three gates

- **ACTOR** - is the beneficiary shipping software, or evaluating a model?
- **SUBSTRATE** - doable with Claude Code / Codex / MCP / hooks / subagents / worktrees, no
  model internals?
- **DEMO** - is there a 3-8 minute terminal demo with observable before/after?

Plus exactly **one** bounded attempt to re-aim an alignment-framed idea into a practitioner
frame. Capped at one, or the model will rationalise any paper into a video.

Precedent that validates this: `artefacts/watch-later-acs-gap/` already contains the pattern
working. A METR paper, a research RCT from a model-evals org, became the practitioner spine
*"AI coding help inverts with your own expertise."* Ideas from outside the audience's
information diet are often the best candidates precisely because nobody else in the niche is
reading them.

### Two lanes nobody asked for

**Comments and Shortform.** The `comments` search index is queryable unauthenticated with
full bodies. LW Shortform is where practitioners post quick technique notes, and it is
invisible to any post-level scan. 136 comments shortlisted, 62 of them Shortform.

**Zvi as a link source, not a candidate.** The 12 "AI #NNN" newsletters are 7k-17k words and
topped the first ranking purely on length. Routed to a separate lane that mines their
outbound links: 61 leads, including Odd Lots with Boris Cherny, "Claude Security is now a
Claude Code plug-in", the Sol system prompt in Codex desktop, and Anthropic studies.

### Settled: do not fetch Alignment Forum separately

All 49 AF posts since 2026-05-20 are already in the LW corpus. Zero AF-only posts. Saves a
whole track.

## What is still undecided

The session stopped on an unanswered question. Both parts are still open.

**Scope.** Full sweep plus a committed driver (recommended, ~15 agents, 15-25 min) / cheap
3-post probe first / full sweep with no driver / sweep plus wiring LessWrong in as a
recurring lane alongside Theo, Hacker News, indie AI blogs and Emergent Mind.

**Deliverable** (can be more than one):
- Net-new techniques not in the catalog, with filmable pitches and a suggested class slot.
- Complement / follow-up angles, where ACS covers step A and the post supplies step B.
  Flagged as highest-value, since each becomes a follow-up video with a built-in "you already
  know A" opening.
- Filming-priority plus fresh proof material. Exploits the `isCompleted` finding: videos
  already on the plan but unfilmed, matched with LessWrong material giving a fresh hook,
  citation or worked example. Argued to be worth more than net-new discovery, because the
  bottleneck is filming rather than ideas.
- Confirmation of what is already covered.

## Design decisions for the analysis half

Settled during design, not yet implemented.

- **Engine: reuse the `wisdom-to-acs-gap` skill.** No end-to-end pipeline existed, but both
  expensive halves did. `SKILL.md:41` lists "a pasted transcript (use it directly; skip the
  transcript fetch)" as a first-class input, so bodies can be fed in straight from `bodies/`.
  The driver must override exactly one thing (output path) and respect two constraints:
  `SKILL.md:157` "NEVER call search_videos from the orchestrator context", and the
  `SKILL.md:243-244` disk-write prohibition.
- **Driver shape:** a `mine-workflow.js`-style fan-out, one agent per post.
- **Output:** `artefacts/lesswrong-acs-gap/YYYY-MM-DD-<slug>.md` per post, plus an `_index.md`
  roll-up, with raw bodies preserved (they now live in `bodies/`).
- **Verdicts need evidence, not scores,** for the recall reasons above.

**Worth doing once:** four bulk gap-runs have already happened in this repo (Gulli's book,
BoundaryML, watch-later, WF2026) and not one left a committed driver behind. Every run was
orchestrated ad hoc and thrown away. Building the driver once is cheap on the back of this
run and is the single genuinely missing piece.

Related: [[decision-surfaces]], `artefacts/watch-later-acs-gap/`, `artefacts/wf2026-acs-gap/`,
`artefacts/boundaryml-ai-that-works/`, `artefacts/agentic-design-patterns-acs-gap/`
