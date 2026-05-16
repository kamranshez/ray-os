# Dependency hunt

## How prerequisites were inferred

Probed ~25 high-suspect videos via `mcp__claude_ai_Agentic_Coding_School__get_video` and read the `agentContext.Assumes you know` field plus explicit cross-references in the description/transcript ("see the X video", "covered in the Y video"). Only flagged a dependency when the video itself names another video, the agentContext lists it as a prerequisite, or a feature it depends on is in another video. Skipped speculation.

## Day-by-day prerequisite finds

### Day 1
- **Spec Developer (CC) assumes Ask User Question Tool (CC) AND Custom Slash Commands (CC)** — agentContext says verbatim: "Assumes you know: How to use the Ask User Question tool (covered in earlier videos); Basic Claude Code slash command setup (covered in the Slash Commands video)." Transcript also walks through wrapping the prompt as a slash command. Recommendation: play Ask User Question Tool BEFORE Spec Developer in Day 1's Core. Pull **Custom Slash Commands** (currently Day 5 deep cut) into **Day 0** pre-work — it's load-bearing across Days 1/2/5/6/7.
- **Checking After Spec Developer (CC) assumes Subagents (CC)** — agentContext: "Basic familiarity with sub-agents and how Claude Code spawns them." Subagents isn't covered until Day 3. Recommendation: **move "Checking After Spec Developer" off Day 1 Core and onto Day 6 Verification** (or Day 3 once Subagents is taught) — the video is really about *verifying* an implementation against a spec, not about alignment.
- **Improved Plan Mode (CC) assumes Planning Mode (CC) and Shift+Tab** — internal chain, fine.

### Day 2
- **/rewind (CC) assumes /clear and /compact concepts** — transcript: "when you do commands like compact or /clear, then a lot of checkpoints will be cleared as well." Both already covered (Day 0 mechanics + Day 2 Practice). Just sequence /rewind AFTER /clear in the Day 2 flow.
- **Auto Compact and Handoff (CC) assumes Custom Slash Commands** — agentContext key pattern includes `/handoff` which is described as "Custom command". Reinforces the Day 0 slash-commands ask above.
- **Long Context Failure (FT)** uses `/context` and `/compact` — already pre-work, fine.

### Day 3
- **Quick Spawning Subagents (CC) assumes Subagents (CC)** — explicit: "Assumes you know: What subagents are and why isolated context windows are useful (see the 'Subagents' video)." Sequence first.
- **Forking Sessions vs /btw (CC) assumes BOTH Forking Sessions AND /btw** — explicit. Currently Day 3 Core lists all three; just enforce order: Forking Sessions → /btw → Forking Sessions vs /btw.
- **Explore Subagent (CC) assumes Subagents (CC)** — explicit. Sequence after.
- **Improving Explore Subagent (CC) assumes Explore Subagent (CC)** — explicit chain. Plus relies on editing `~/.claude/settings.json` → settings primer should be Day 0.
- **Progressive Disclosure (CE) assumes Skills knowledge** — agentContext: "Assumes you know: What agent skills are and how SKILL.md files work; What CLAUDE.md files are and the SNR concept from earlier videos." **This is the biggest sequencing conflict in the structure**: Progressive Disclosure is Day 3 Core but it assumes Day 4 Skills content. Options: (a) move Progressive Disclosure to Day 4, (b) drop a 5-minute Skills primer into Day 3 before showing PD, or (c) swap Days 3 and 4 entirely. Easiest is (b) — show the `SKILL.md` frontmatter pattern as a one-slide setup before PD.
- **Anatomy of a Node (CE) assumes Signal to Noise (CE) + Progressive Disclosure (CE)** — explicit: "If you've never made a CLAUDE.md file before (start with Signal to Noise)." Already implied by the [[Context Layer]] entry; just confirm order.

### Day 4
- **Forked Contexts for Skills (CC) assumes Claude Code Skills (CC) AND Subagents (CC)** — explicit. Skills is Day 4 Core, Subagents Day 3 — fine.
- **Combining Skills & Subagents (CC) assumes Forked Contexts for Skills (CC), Subagents (CC), AND the skill-creator skill** — explicit, and the practice block uses skill-creator live. Need to demo `@skill-creator` or add a one-line "install this skill first" in pre-work materials.

### Day 5
- **Another Hook Example (CC) assumes Hooks (CC) AND basic Skills + context forking** — explicit. Sequence after Hooks; Skills cross-dep (Day 4) is fine. Also relies on `@claude-code-guide` subagent for hook-config generation.
- **Memory for Scheduled Tasks (CC) assumes Routines** — explicit: "watch 'Scheduled Tasks' first." Sequence after.
- **API Trigger Routines (CC) assumes Routines** — implicit but obvious. Sequence after.
- **Remote Control (CC)** — light deps; references Stop hooks (Day 5) and Telegram/Discord videos (deep cuts) but stands alone.

### Day 6
- **Codex Consult Skill assumes Skills knowledge + Codex installed + ChatGPT subscription** — explicit. Day 0 Codex install + Day 4 Skills are both upstream — fine.
- **/ultrareview (CC) references Codex Consult Skill** — transcript: "you can watch the video about using the Codex consult skill as well." Sequence inside Day 6 Core: Codex CLI Plugin → Codex Consult Skill → /ultrareview.
- **Automatic Plan Reviewing with Subagents (AT) assumes Hooks (PostToolUse) AND custom subagents** — explicit. Day 5 Hooks → Day 6 chain is correct; just enforce that Hooks is fully covered before Day 6 hits this video.
- **Codex CLI Plugin assumes prior Codex Consult Skill video** — transcript opens "following on from last week's video about the Codex consult skill." Either swap the order (Consult first, then Plugin) OR play both knowing the Plugin video acknowledges Consult as the predecessor.

### Day 7
- **Autoresearch Overview (AT) assumes Closing the Loop (FT)** — explicit: "Assumes you know: What 'Closing the Loop' means (see that video first)." Closing the Loop currently lives on Day 2 deep cuts AND Day 6 Practice. **Recommendation**: surface Closing the Loop in Day 7 Core just before Autoresearch (or make it the bridge between Day 6 and Day 7).
- **Multi Subagents for Hard Problems (AT) assumes Subagents + custom agents (`/agents`) + ultrathink** — explicit. All upstream (Day 3 + Niche Features + Day 0 reasoning effort).
- **Ralph Loop (CC) assumes Spec Developer pre-step** — transcript: "I'd recommend watching that video and then coming back to this." Day 1 → Day 7 — fine.
- **Subagent Teams for Debugging (CC) assumes Subagents + MCP servers + SSH** — light deps, all upstream.
- 🚨 **Archetype Teams (PE) and Living Archetypes (PE) appear unfilmed** — both returned `agentContext: null`, `durationSeconds: null`, `transcript: null` from the MCP. They're currently Day 7 Core. This is *not* a dependency issue, but it bears flagging here because it removes ~half of Day 7's existing Core. Will materially affect what needs net-new recording. Confirm with Ray before relying on them.

## Internal cross-references

Videos that reference each other (useful for ordering):

- Forking Sessions vs /btw → references Forking Sessions, /btw, Mermaid Diagram Generator skill
- Improving Explore Subagent → references Explore Subagent
- Anatomy of a Node → references Signal to Noise, Progressive Disclosure
- Codex CLI Plugin → references Codex Consult Skill
- /ultrareview → references Codex Consult Skill
- Memory for Scheduled Tasks → references Routines (Scheduled Tasks)
- API Trigger Routines → references Routines, MillionVerifier-style validation (no ACS video)
- Auto Compact and Handoff → references Custom Slash Commands, /context, /config
- Spec Developer → references Ask User Question Tool, Custom Slash Commands
- Checking After Spec Developer → references Spec Developer, Subagents
- Another Hook Example → references Hooks, Skills, @claude-code-guide
- Autoresearch Overview → references Closing the Loop
- Multi Subagents for Hard Problems → references Subagents, /agents, ultrathink
- Ralph Loop → references Spec Developer, Skills

## Day-0 absorption candidates

Move into pre-work — they're prerequisites for multiple live days:

1. **Custom Slash Commands (CC)** — assumed by Spec Developer, /handoff, ralph-skill, codex-consult skill, hook-skill bridges. Currently only listed as Day 5 deep cut. Promote.
2. **Settings JSON / `~/.claude/settings.json` editing (CC)** — assumed by Improving Explore Subagent (Day 3 Practice), Automatic Plan Reviewing with Subagents (Day 6 Practice), Hooks (Day 5 Core). Currently listed in Day 0 mechanics — keep it there but call it out as load-bearing.
3. **Reasoning Effort / Ultrathink (CC, Niche Features)** — assumed by Multi Subagents for Hard Problems (Day 7) and Improved Plan Mode (Day 1). Currently Day 0 mechanics — keep, but emphasise.
4. **/agents (custom agent definition)** — assumed by Automatic Plan Reviewing with Subagents (Day 6) and Multi Subagents for Hard Problems (Day 7). Not on Day 0 yet; either pull in or cover briefly in Day 3 alongside Subagents.

## Sequencing recommendations

Right order for each day's Core watch-along based on dependencies:

**Day 1 Alignment**
1. Status of Agents *(NEW)*
2. Glossaries (Customized Terminology for Better Prompts, FT)
3. Clarifying Questions (FT)
4. Ask User Question Tool (CC) ← must precede Spec Developer
5. Spec Developer (CC)
6. Benefits of Spec Developer (CC)
   *(remove "Checking After Spec Developer" from Day 1 — moves to Day 6)*

**Day 2 Steering**
1. Long Context Failure (FT) — sets the *why*
2. Context Window Management (WF) · Opus 4.6's Context Window (WF) — current behaviour
3. Dealing with Syncophancy (FT)
4. /rewind (CC) — after attendees know /clear and /compact

**Day 3 Context Architecture**
1. Subagents (CC) ← foundation for everything else
2. Quick Spawning Subagents (CC)
3. Forking Sessions (CC) → /btw (CC) → Forking Sessions vs /btw (CC)
4. (5-minute Skills primer — or swap Day 3 ↔ Day 4)
5. Context Layer: Signal to Noise (CE) → Progressive Disclosure (CE) → Anatomy of a Node (CE)

**Day 4 Skills**
1. Claude Code Skills (CC) — the foundation
2. Creating Skills (CC)
3. Types of Skills (CC)
4. Real World Skill Example 1 + 2 (CC)
   Practice block sequences naturally: Arguments → Forked Contexts → Combining with Subagents.

**Day 5 Automation**
1. Hooks (CC) ← must precede Another Hook Example
2. Another Hook Example (CC)
3. Routines (CC) ← must precede Memory + API Trigger
4. Remote Control (CC)
5. Connecting to Telegram (CC) — needed because Routines + Remote Control both demo Telegram

**Day 6 Verification**
1. Codex Consult Skill (CC) ← the Plugin video opens by referencing it
2. Codex CLI Plugin (CC)
3. Codex MCP Server (CC)
4. /security-review (CC)
5. /review (CX)
6. (Practice) /ultrareview (CC) → Automatic Plan Reviewing with Subagents (AT) → Closing the Loop (FT, if not already shown)
7. **Add: Checking After Spec Developer (CC)** — moved from Day 1; lands naturally as the "verify against the spec" beat.

**Day 7 Agent Teams & Loopy AI**
1. Convergence thesis *(NEW)*
2. Archetype Teams (PE) **— FLAG: appears unfilmed**
3. Living Archetypes (PE) **— FLAG: appears unfilmed**
4. Subagent Teams for Debugging (CC)
5. Multi Subagents for Hard Problems (AT) — anchors the case for parallel reasoning
6. 5 archetype videos *(NEW × 5)*
7. (Practice) Closing the Loop (FT) → Ralph Loop (CC) → Autoresearch Overview/Technical/Non-Technical (AT) → /loop (CC) → Headless Mode (CC)
