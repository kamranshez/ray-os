# Minimal curation

Philosophy: workshop buyers also get full ACS access. The workshop spine should be the *smallest* set of existing videos that anchors each day. Everything else stays in ACS where attendees can wander to it. ~3–5 ACS videos per day, each justified in a line.

## Day 0 (pre-work additions)

Self-paced. Anything install / mechanical lives here so live days stay conceptual.

- **Install Claude Code (MacOS) + (Windows)** — claude-code · zero-friction prerequisite
- **Terminal Commands (for Beginners)** — claude-code · gate for everyone non-CLI-fluent
- **A Quick Build** — claude-code · ship-something-before-day-1 forcing function
- **MCP Servers** — claude-code · primes [[Using the MCP]] so Day 0 isn't pure install
- **Installing Codex CLI** — codex · Day 6 needs Codex installed; do it here
- **/init & Claude.md** — claude-code · attendees arrive with a CLAUDE.md, Day 1 builds on it

## Day 1 — Alignment

- **Spec Developer + Benefits of Spec Developer** — claude-code · the canonical workshop topic; load-bearing for the whole day
- **Clarifying Questions** — fundamental-techniques · anchors why specs/glossaries exist
- **Customized Terminology for Better Prompts** — fundamental-techniques · [[Glossaries]] in 5 minutes
- **Goal In, Strategy Out** — prompt-engineering · the Goals/Missions merge in one video
- **Multimodal Models for PRDs** — fundamental-techniques · pairs with [[Prototypes as specs]]

## Day 2 — Steering

- **Long Context Failure** — fundamental-techniques · single best anchor for the long-context trio merge
- **Dealing with Syncophancy** — fundamental-techniques · matches [[sycophantic-models-suggestions-as-commands]] beat-for-beat
- **/rewind** — claude-code · the mechanic for [[Rewinding]]
- **Just Run It Again** — fundamental-techniques · [[Ordering]] applied
- **Auto Compact and Handoff** — claude-code · the survival skill for [[Compaction]]

## Day 3 — Context Architecture

- **Subagents** — claude-code · the canonical primer
- **Explore Subagent** — claude-code · the one concrete subagent everyone will use first
- **1M Token Context + Scout, Worker, Synthesizer** *(2 videos as a pair)* — claude-code · the [[1M Context]] beat
- **Code Mode** — claude-code · MCP→CLI bridge that powers [[CLIs vs MCPs]]

## Day 4 — Skills

- **Claude Code Skills** — claude-code · why skills exist
- **Creating Skills** — claude-code · the mechanics, matches [[Creating Skills]] stub
- **Blog Post to Skill** — advanced-techniques · the end-to-end "encode taste" demo that makes the day stick
- **Combining Skills & Subagents** — claude-code · pairs cleanly with [[Skills + Subagents]]
- **Forked Contexts for Skills** — claude-code · matches stub

## Day 5 — Automation & Workflows

- **Hooks** — claude-code · the mechanic
- **Routines (aka Scheduled Tasks)** — claude-code · the mechanic
- **Remote Control** — claude-code · the mechanic
- **/loop** — claude-code · powers [[Workflows]] and bridges to Day 7's Ralph
- **Multi Clauding** — workflows · real-world automation Ray actually runs

## Day 6 — Verification

- **Codex Consult Skill** — claude-code · the [[Verifying with Codex]] beat
- **/security-review** — claude-code · matches stub
- **/ultrareview** — claude-code · matches stub
- **Automatic Plan Reviewing with Subagents** — advanced-techniques · the [[Adversial Reviewers]] anchor
- **Benchmarking Tools & MCPs** — advanced-techniques · the only ACS video that fits [[agent-benchmark-harness]]

## Day 7 — Agent Teams & Loopy AI

- **Archetype Teams + Living Archetypes** *(2 videos as a pair)* — prompt-engineering · the convergence-over-perfection thesis is already in here
- **Multi Subagents for Hard Problems** — advanced-techniques · concrete instance of archetypes 02 + 04
- **Subagent Teams for Debugging** — claude-code · the one Ray has filmed; use it as the worked example
- **Ralph Loop (aka Ralph Wiggum)** — claude-code · [[Ralph]] in one video
- **Autoresearch Overview + Autoresearch Technical Example** *(2 videos as a pair)* — advanced-techniques · [[Autoresearch]]

---

## Cut list

These look workshop-relevant but stay in ACS only — workshop attendees can wander into them on their own time.

- **Most of the 17-video Fundamentals chapter** (`/clear`, `/model`, `/status & /config`, `/context`, `/usage`, `Permissions`, `Tab Accept`, `Custom Slash Commands`, `Settings Json`, etc.) — Day 0 mechanics, not spine. Buyers can binge them pre-workshop.
- **CLAUDE.md chapter** (8 videos: `/init`, Advanced, Hierarchical, Best Practices, Conditions, Cleanup, Memory) — touched in Day 0 pre-work + Day 4 indirectly; full chapter is too granular for the spine.
- **Claude Web & Desktop chapter + Other Forms of Claude Code + Niche Features** — discoverable in ACS, not load-bearing for any workshop day.
- **Most of Codex class** beyond install + Consult — workshop only needs Codex as a *verifier* (Day 6), not as a parallel toolchain.
- **Context Engineering class** — full standalone class on context layers; great as a follow-up, but the workshop's Day 3 doesn't need 11 videos when [[context-strategy-correlated-with-engagement]] + 2 ACS videos cover the spine.
- **Distribution Steering, Persona Vectors, Scaling Taste, Infusing Lived Experience** (prompt-engineering) — adjacent to Day 4 (Skills) but more philosophical than operational. Cut from spine, recommend as Day 4 wandering material.
- **Boxing the Agent In, Closing the Loop, Getting Prompt Feedback, High Level Coherence, Multiple Proposals, Reducing Agent Confusion** (fundamental-techniques) — covered conceptually by the workshop stubs already. Don't duplicate.
- **Worktrees, Designing Components, Data Analysis, Extract Wisdom, Adding New Features** (workflows) — Ray-specific patterns; useful as "how Ray actually works" supplement but not curriculum.
- **For Business class entirely** — different audience persona; out of scope.

## Open calls (Ray to decide)

1. **Codex coverage depth.** Minimalist take is "Codex is a verifier, install + Consult skill is enough." Should Day 0 instead seed *parallel Codex fluency* (Quick Build with Codex too) so Day 7 archetypes can show CC↔Codex pairings? Trade: +30 min Day 0 vs. richer Day 7.
2. **Where does `/goal` live?** Codex's `/goal` + `Using /goal Effectively` is a perfect [[goal]]/[[Missions]] anchor for Day 1, but it's a Codex video — feels weird on Day 1 if Codex is barely introduced. Keep Day 1 Claude-only and move `/goal` to Day 7's Loopy AI section, OR introduce Codex earlier?
3. **Should `Multi Clauding` (workflows) move to Day 7?** It's listed under Day 5 (Automation) here, but it's really an agent-teams pattern. Argument for keeping in Day 5: it's the only "real-world how Ray works" video in the spine. Argument for Day 7: thematic fit. Pick one.
