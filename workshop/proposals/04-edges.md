# Edge-class gap hunt

Forks 01/02 leaned hard on Master Claude Code + FT/AT. This pass scans the under-weighted classes — Workflows, For Business, Prompt Engineering, Codex (as a primary tool, not just verifier), plus everything added since 2026-03-01 — for videos that should still earn a workshop slot.

Class codes: **CC** = Master Claude Code, **CX** = Master Codex, **FT** = Fundamental Techniques, **AT** = Advanced Techniques, **CE** = Context Engineering, **PE** = Prompt Engineering, **WF** = My Daily Workflows, **FB** = For Business.

---

## Workflows class — what's currently missing

WF already in plan: Quick Benchmarking, Context Window Management, Opus 4.6's Context Window, Multi Clauding, Adding New Features, How I Use Worktrees.

- **Interactive HTML Artifacts** (`workflows`) — Day 1 deep cut. Live artifact-as-spec demo. Pairs directly with [[Prototypes as specs]] and is *the* Apr-2026 free video proving the value.
- **Channel HTML Artifacts** (`workflows`) — Day 1 deep cut OR Day 5 deep cut. Same primitive applied to actual marketing output; pick one home.
- **Designing Components** (`workflows`) — Day 4 deep cut. UI-flavoured skill example, free video, fills the "skills make taste portable" beat alongside Frontend Design Skill.
- **Data Analysis** (`workflows`) — Day 5 practice OR Day 6 practice. Real workflow; teaches output-shape verification on real data. Better fit for Day 6 (Verification) since it forces you to check the numbers.
- **Extract Wisdom** (`workflows`) — Day 5 deep cut. Maps to a real installed skill in this repo; good "skills + automation cascade" example.
- **Exa MCP** (`workflows`, MCP Servers I Like) — Day 0 deep cut OR Day 5 deep cut. Ray's stated default web-search MCP per root CLAUDE.md — earns a place under "MCPs Ray actually uses."
- **Refero Design** (`workflows`, MCP Servers I Like) — Day 4 deep cut. Design-context MCP that pairs with the Skills day.

---

## For Business class — what's currently missing

FB already in plan: Adding More Goal-Driven Events, Microsoft Clarity MCP, Reverse Engineering Mobile APIs/Binaries (under [[Reverse Engineering]]).

- **Follow Ups on Features** (`for-business`) — Day 5 deep cut. Teaches the *primitive* of automating customer follow-up loops (a real Routines + Memory chain), not just "here's a Slack bot."
- **LinkedIn + Claude in Chrome** (`for-business`) — Day 5 deep cut OR cut entirely. Teaches Chrome MCP as an outbound channel — same primitive as Connecting to Telegram but for sales. Earns its place only if Chrome MCP isn't already covered enough.

FB intro "Work in Progress" — skip, it's a class disclaimer.

---

## Prompt Engineering class — unsurfaced gems

PE already in plan: Goal In Strategy Out, Distribution Steering, Persona Vectors, Scaling Taste, Archetype Teams, Living Archetypes.

- **Infusing Lived Experience** (`prompt-engineering`) — Day 1 deep cut OR Day 4 deep cut. The "your taste comes from your scars" frame — bridges Alignment (Day 1) and Skills-as-encoded-taste (Day 4). Currently invisible in the plan, and it's a stronger Day-1 cold-open than most picks there.

That's the only PE gem currently missed — fork 02 picked the rest.

---

## Master Codex — Codex-as-a-primary-tool material missed

The plan treats Codex as a verifier (Day 6) or parity tool (Day 4 — Creating Skills CX, Day 3 — Subagents CX). It misses **Codex App as a distinct UX**: Mini Windows, Browser Use, Computer Use, Threads, Mentions. These are not just "Codex's version of CC features" — they teach primitives CC doesn't have.

**Add to plan (Codex App as a primitive, not a mirror)**:

- **Mini Windows** (`codex`, Codex App) — Day 3 deep cut. The "spawn a focused side-conversation that returns a value" pattern. Closest CC equivalent is `/btw` + forks; Mini Windows is the more ergonomic UX. Pairs with [[Forked Subagents]].
- **Chats vs Threads** (`codex`, Codex App) — Day 2 deep cut. Thread mental model is a genuine Steering primitive — long-running thread vs disposable chat. CC has no direct equivalent.
- **Compaction & Monothreading** (`codex`, Codex App) — Day 2 deep cut alongside Auto Compact and Handoff. Codex's compaction model is meaningfully different from CC's; worth a contrast video.
- **Browser Use** (`codex`, Codex App) — Day 5 deep cut. Outbound automation via browser, distinct from Chrome MCP.
- **Computer Use** (`codex`, Codex App) — Day 5 deep cut OR Day 7 deep cut. Highest-blast-radius automation primitive in the catalogue; deserves a slot even if just to set expectations.
- **Codex for Chrome** (`codex`, Codex App) — Day 5 deep cut. Chrome-as-Codex-host.
- **Browser Comments** (`codex`, Codex App) — Day 6 deep cut. Comment-driven review in the browser — adjacent to the `/review` flow already in Day 6 core but covers a different surface.
- **Forking** (`codex`, Codex App) — Day 3 deep cut. Codex's session-fork UX; pairs with CC's Forking Sessions to teach the *concept* across tools.
- **Creating Projects & Files** + **Referencing Files & Folders** (`codex`, Codex App) — Day 0 pre-work. Foundational Codex App mechanics currently absent from Day 0.
- **Agents.MD & Memories** (`codex`, Codex App) — Day 3 deep cut alongside the [[Context Files]] family. Codex's parallel to CLAUDE.md hierarchy.
- **MCP Servers** (`codex`, Codex App) — Day 0 deep cut. Codex parity for the existing CC MCP coverage.
- **Plugins** (`codex`, Codex App) — Day 4 deep cut. Codex's plugin marketplace, pairs with [[Plugins]] stub.
- **Paper Design MCP** (`codex`, Codex App) — Day 4 deep cut. Design-context MCP — pairs with Refero Design from WF for a "design-context MCPs" cluster.
- **Chronicle** (`codex`, Codex App) — Day 7 deep cut. Codex-side session memory; loop-adjacent.
- **Symlinking** (`codex`, Codex App) — Day 3 deep cut. Real workflow primitive for multi-repo Codex.
- **Where Codex Works** (`codex`, Codex App) — Day 0 deep cut. Mental model video — when to reach for Codex vs CC. Cheap to surface, high-leverage.
- **Built In Terminal** (`codex`, Codex App) — skip, mechanics-class for Day 0 only if attendees ask.
- **Git Features** (`codex`, Codex App) — Day 0 deep cut, pair with CC's "Using Git for Version Control."
- **Better Dictation** (`codex`, Codex App) — skip from workshop. Ergonomics, not a primitive.

**Codex CLI missing from plan**:

- **/new** (`codex`, Codex CLI) — Day 2 deep cut, pair with `/clear`.
- **/approvals** (`codex`, Codex CLI) — Day 0 alongside Permissions.
- **Custom Prompts** (`codex`, Codex CLI) — Day 5 deep cut, parity with Custom Slash Commands.
- **--add-dir** (`codex`, Codex CLI) — Day 3 deep cut, parity with CC `/add-dir`.
- **Mentioning Files** (`codex`, Codex CLI) — skip from workshop unless attendees haven't seen CC equivalent.

---

## Recently added across all classes (since 2026-03-01) not in plan

Most recent additions ARE in the plan already. Gaps:

- **/fewer-permission-prompts** (`claude-code`, Niche Features, May 2026) — Day 0 deep cut. Auto-allowlist mechanic; useful pre-work.
- **/team-onboarding** (`claude-code`, Niche Features, Apr 2026) — cut from workshop OR Day 5 deep cut. Team-scoped, low priority for solo attendees.
- **Aliases** (`claude-code`, Niche Features) — Day 0 deep cut.
- **/recap** (`claude-code`, Niche Features) — Day 2 deep cut alongside Session Management.
- **/advisor** (`claude-code`, Niche Features) — Day 1 deep cut. Plan-review mechanic; pairs with Spec Developer.
- **Ultrathink** (`claude-code`, Niche Features) — Day 0 deep cut. Thinking-budget knob.
- **Chrome Javascript Tool** (`claude-code`, MCP Servers) — Day 5 deep cut.
- **/teleport** (`claude-code`, Claude Web & Desktop) — Day 0 deep cut.
- **Desktop Browser Preview** (`claude-code`, Claude Web & Desktop) — skip OR Day 0 deep cut.
- **/simplify** (`claude-code`, Subagents) — Day 4 practice. This is a real workshop primitive — the simplify pass after building. Currently invisible.
- **/batch** (`claude-code`, Subagents) — Day 3 deep cut.
- **Stashing Prompts** (`claude-code`, Shortcuts) — Day 2 deep cut.
- **Ctrl G** (`claude-code`, Shortcuts) — skip.
- **Fullscreen TUI & Focus** (`claude-code`, Advanced) — Day 0 deep cut.
- **Claude Environment Variables** (`claude-code`, Advanced) — Day 0 deep cut.
- **Scope & Settings.json** (`claude-code`, Advanced) — Day 0 core (mechanics) — bump up from where Day 0 currently sits.
- **Cmux** (`claude-code`, Other Terminals) — Day 3 deep cut, pair with Multi Clauding for "terminal multiplexer + multi-Claude" cluster.

---

## Advanced Techniques — videos missed

AT already in plan: Gravitational Pull, One-Pattern Rule, Mixing Models & Modes, Git Diffs & Mermaid Diagrams, Combining CLIs & Models, Planning Convergence, Multi Subagents for Hard Problems, Avoiding Code Bias Loops, Refactoring with Subagents, Automatic Plan Reviewing with Subagents, Blog Post to Skill, Skills + Explore Subagents, Benchmarking Tools & MCPs, Autoresearch trio.

- **Economising with Prompt Cache** (`advanced-techniques`) — Day 2 deep cut. Cost/cache-aware steering; surprisingly relevant once attendees start doing long-context work.
- **Unrestraining LLMs for Rewrites** (`advanced-techniques`) — Day 4 deep cut. Permission/scope philosophy for rewrite-heavy work; pairs with Off-distribution.
- **Using Public GitHub Repos** (`advanced-techniques`) — Day 3 deep cut. Context-injection primitive — pulling reference repos as context.
- **Tackling Redunant Code** (`advanced-techniques`) — Day 4 deep cut. Pairs with `/simplify` for the dedup pass.
- **Managing API Keys for Agents** (`advanced-techniques`) — Day 5 deep cut. Security primitive for automation; pairs with Agent Vault skill in this user's CLAUDE.md.

---

## Fundamental Techniques — videos missed

FT already in plan: all the steering/alignment standards, Boxing the Agent In, Closing the Loop, Customized Terminology, Clarifying Questions, etc.

- **Reducing Agent Confusion in Growing Projects** (`fundamental-techniques`) — Day 1 deep cut, pair with Customized Terminology under the [[Glossaries]] umbrella. Currently invisible.
- **Using Reliable Packages** (`fundamental-techniques`) — Day 6 deep cut. Verification-adjacent (pick libraries the model knows well).

---

## Topics that warrant a new stub

Two-or-more videos clustering toward a topic that has no stub yet:

1. **Codex App as a Distinct UX** — Mini Windows + Chats vs Threads + Browser Use + Computer Use + Codex for Chrome + Forking (CX). Currently the workshop has no canonical note framing "why Codex App vs CC CLI." Stub: `Codex App vs Claude Code.md` (Day 0 conceptual).
2. **Design-context MCPs** — Refero Design (WF) + Paper Design MCP (CX) + Frontend Design Skill (CC). Stub: `Design Context MCPs.md` (Day 4 deep cut cluster).
3. **HTML Artifacts as a workflow primitive** — Interactive HTML Artifacts + Channel HTML Artifacts (WF) + Artifact Planning (FT). Currently [[Prototypes as specs]] half-covers this but doesn't acknowledge the artifact-as-runtime version. Stub: `HTML Artifacts.md` (Day 1 or Day 5).
4. **Real-World Skills Showcase** — Designing Components (WF) + Extract Wisdom (WF) + Data Analysis (WF) + Frontend Design Skill (CC) + Blog Post to Skill (AT). Stub: `Real World Skills.md` (Day 4 deep cut umbrella).
5. **Agents Memory** — Memory.MD (CC) + Subagent Memories (CC) + Memory for Scheduled Tasks (CC) + Agents.MD & Memories (CX) + Chronicle (CX). Currently scattered across days. Stub: `Memory.md` (Day 3 — a single note unifying every memory primitive across CC + CX + scheduled tasks).
6. **`/simplify` as a primitive** — /simplify (CC) + Tackling Redunant Code (AT) + Refactoring with Subagents (AT). Stub: `Simplify Pass.md` (Day 4 practice).

---

## Recommendations: net adds to Class Structure.md (copy-paste)

**Day 0**:
- add Where Codex Works (codex) to Day 0 deep cuts
- add /approvals (codex) to Day 0 alongside Permissions
- add Scope & Settings.json (claude-code) to Day 0 core
- add /fewer-permission-prompts (claude-code) to Day 0 deep cuts
- add Aliases (claude-code) to Day 0 deep cuts
- add Ultrathink (claude-code) to Day 0 deep cuts
- add Fullscreen TUI & Focus (claude-code) to Day 0 deep cuts
- add Claude Environment Variables (claude-code) to Day 0 deep cuts
- add /teleport (claude-code) to Day 0 deep cuts
- add Git Features (codex) to Day 0 deep cuts
- add Creating Projects & Files (codex) to Day 0 pre-work
- add Referencing Files & Folders (codex) to Day 0 pre-work
- add MCP Servers (codex) to Day 0 deep cuts
- add Exa MCP (workflows) to Day 0 deep cuts

**Day 1 (Alignment)**:
- add Interactive HTML Artifacts (workflows) to Day 1 deep cuts
- add Channel HTML Artifacts (workflows) to Day 1 deep cuts
- add Infusing Lived Experience (prompt-engineering) to Day 1 deep cuts
- add /advisor (claude-code) to Day 1 deep cuts
- add Reducing Agent Confusion in Growing Projects (fundamental-techniques) to Day 1 deep cuts under [[Glossaries]] umbrella

**Day 2 (Steering)**:
- add Chats vs Threads (codex) to Day 2 deep cuts
- add Compaction & Monothreading (codex) to Day 2 deep cuts
- add /new (codex) to Day 2 deep cuts
- add /recap (claude-code) to Day 2 deep cuts
- add Stashing Prompts (claude-code) to Day 2 deep cuts
- add Economising with Prompt Cache (advanced-techniques) to Day 2 deep cuts

**Day 3 (Context Architecture)**:
- add Mini Windows (codex) to Day 3 deep cuts
- add Forking (codex) to Day 3 deep cuts
- add Agents.MD & Memories (codex) to Day 3 deep cuts under [[Context Files]] umbrella
- add Symlinking (codex) to Day 3 deep cuts
- add Using Public GitHub Repos (advanced-techniques) to Day 3 deep cuts
- add --add-dir (codex) to Day 3 deep cuts
- add /batch (claude-code) to Day 3 deep cuts
- add Cmux (claude-code) to Day 3 deep cuts under Multi Clauding cluster

**Day 4 (Skills)**:
- add /simplify (claude-code) to Day 4 practice block
- add Designing Components (workflows) to Day 4 deep cuts
- add Refero Design (workflows) to Day 4 deep cuts
- add Paper Design MCP (codex) to Day 4 deep cuts
- add Plugins (codex) to Day 4 deep cuts alongside [[Plugins]] stub
- add Unrestraining LLMs for Rewrites (advanced-techniques) to Day 4 deep cuts
- add Tackling Redunant Code (advanced-techniques) to Day 4 deep cuts

**Day 5 (Automation)**:
- add Browser Use (codex) to Day 5 deep cuts
- add Computer Use (codex) to Day 5 deep cuts
- add Codex for Chrome (codex) to Day 5 deep cuts
- add Custom Prompts (codex) to Day 5 deep cuts alongside Custom Slash Commands
- add Chrome Javascript Tool (claude-code) to Day 5 deep cuts
- add Follow Ups on Features (for-business) to Day 5 deep cuts
- add LinkedIn + Claude in Chrome (for-business) to Day 5 deep cuts
- add Extract Wisdom (workflows) to Day 5 deep cuts
- add Data Analysis (workflows) to Day 5 OR Day 6 practice block
- add Managing API Keys for Agents (advanced-techniques) to Day 5 deep cuts

**Day 6 (Verification)**:
- add Browser Comments (codex) to Day 6 deep cuts
- add Using Reliable Packages (fundamental-techniques) to Day 6 deep cuts
- (consider) move Data Analysis (workflows) into Day 6 practice as the "verify the numbers" demo

**Day 7 (Agent Teams & Loopy AI)**:
- add Chronicle (codex) to Day 7 deep cuts
- (consider) add Computer Use (codex) to Day 7 deep cuts if not in Day 5

**Cut suggestions** (mentioned earlier in plan but probably skip in v1):
- /team-onboarding (claude-code) — team-scoped, low solo-attendee value
- Better Dictation (codex), Ctrl G (claude-code), Desktop Browser Preview (claude-code), Built In Terminal (codex), Mentioning Files (codex) — ergonomic mechanics, not primitives

---

## Headline gaps the first two curators missed

1. **Codex App is not just "Codex's version of CC"** — it has 3-4 genuinely distinct primitives (Mini Windows, Threads, Browser/Computer Use, Codex for Chrome). The plan currently underweights all of these.
2. **HTML Artifacts as a workflow** — three videos across CC/WF/FT cluster around this and there's no canonical stub. This is real workshop-original IP already filmed.
3. **The `/simplify` primitive** — an entire post-build pass is missing from Day 4. /simplify + Tackling Redunant Code + Refactoring with Subagents form a coherent practice block.
4. **Agents Memory as one topic** — fragmented across days. Worth a single Day 3 note rather than 7 scattered mentions.
5. **Sales / outbound automation** (FB's LinkedIn + Chrome cluster) — currently invisible. May be worth keeping invisible if the workshop's audience is technical, but worth a deliberate call rather than an oversight.
