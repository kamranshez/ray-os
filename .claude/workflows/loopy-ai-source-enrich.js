export const meta = {
  name: 'loopy-ai-source-enrich',
  description: 'Enrich six loopy-ai scripts in parallel with real source-tweet/transcript detail that the inbox-only first pass may have missed. Each agent diffs the live source against the current script and edits in place only where there is a genuine gap, in the class-script-writer voice.',
  phases: [{ title: 'Enrich', detail: 'one agent per video: diff source vs script, fold in what is missing' }],
}

const BASE = '/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/loopy-ai'
const SKILL = '/Users/ray/Desktop/ray-os/.claude/skills/class-script-writer'

const SKELETON = `01 Intro | 02 The Loop Stack | 03 Strip The Model Out | 04 L1 Essentials | 05 Closing The Loop | 06 Borrowed Verifiers | 07 Pair Every Creator With An Attacker | 08 Architecting The Loop | 09 HTML Artefacts For Output | 10 Ralph Loops | 11 /goal Mode | 12 Writing Effective Goals | 13 Don't Pre-Sequence The Backlog | 14 The Autonomy Dial | 15 L4 Worker Loops | 16 Routines And Scheduled Tasks | 17 Autoresearch | 18 Auto Research For Non-Technical Work | 19 L5 Discovery Loops | 20 The Three Role Split (ACE) | 21 The Teacher Learner Pattern | 22 The Bug Triage Loop | 23 Echo Chamber Failure Mode | 24 Governance Primitives | 25 Slack As Your Command Center | 26 Keeping You In The Loop | 27 Mission Command | 28 Removing Bottlenecks | 29 Where Taste Went`

const RULES = `VOICE/STRUCTURE (class-script-writer): second person, direct, confident, no hedging; short paragraphs; lead with the point. '##' headings only, never H1. '---' between major sections. HARD RULE: no em dashes, no en dashes anywhere (use commas/periods/rephrase; grep your output and remove any). Inline sources as 'Source: https://...' under the claim. Images as [IMAGE: ...] description line then ![[images/<slug>/<name>.png]]. Read ${SKILL}/references/style-guide.md if unsure.`

// Live source material I fetched via Claude-in-Chrome + Supadata. Each agent gets only its own.
const SOURCES = {
  '05': {
    file: '05-closing-the-loop.md',
    chapter: 'Closing The Loop',
    material: `SOURCE A — Peter Steinberger (@steipete), https://x.com/steipete/status/2054850632067019173:
"Wrote a skill that runs codex /review in a loop until there's no booboos anymore. Caveat: It won't fix system architecture for ya, so you still need BRAIN as master model." (skill lives at github.com/steipete/agent-scripts, skills/codex-review/SKILL.md). Load-bearing nuance: the verifier loop polishes correctness/quality but does NOT make architectural decisions; a human (or master model) still owns the design.

SOURCE B — eric zakariasson (@ericzakariasson), https://x.com/ericzakariasson/status/2057521364622553442:
"the most used skill internally at cursor right now: /thermo-nuclear-code-quality-review" — deletes complexity instead of moving it; blocks files over 1k lines; flags thin wrappers and leaked logic; rejects PRs that work but make code messier. Point: the verifier enforces a quality bar beyond 'tests pass', and it is the single most-used internal tool at Cursor.`,
  },
  '07': {
    file: '07-adversarial-reviewer-skill.md',
    chapter: 'Pair Every Creator With An Attacker',
    material: `SOURCE — sysls (@systematicls), "How To Be A World-Class Agentic Engineer", https://x.com/systematicls/status/2028814227004395561.
The sharp, likely-missing mechanism is a THREE-AGENT scoring scheme that weaponizes sycophancy instead of fighting it:
1) Bug-finder agent: rewarded +1 for a low-impact bug, +5 for some impact, +10 for critical. Because it wants to please, it eagerly returns the SUPERSET of all possible bugs (including ones it invents).
2) Adversarial agent: for every bug it can DISPROVE it earns that bug's score, but it loses 2x the score if it is wrong. So it aggressively tries to knock bugs down but with caution. Result: the SUBSET of bugs that survive are likely real.
3) Referee agent: told (a deliberate lie) that the human holds the ground truth, +1 if it scores correctly, -1 if not. It adjudicates finder vs adversary; the human spot-checks. sysls calls the result "frighteningly high fidelity, nearly flawless."
Also relevant: the sycophancy/neutral-prompt point. "Find me a bug" makes the model engineer a bug to please you; a neutral prompt ("follow the logic of each component and report all findings") avoids biasing it. Core reframe: an LLM's eagerness to please is not a flaw to suppress, it is a force you can aim by setting opposing incentives between a creator and an attacker.`,
  },
  '09': {
    file: '09-html-artefacts-for-output.md',
    chapter: 'HTML Artefacts For Output',
    material: `SOURCE — David K (@DavidKPiano), https://x.com/DavidKPiano/status/2052448434142269741:
"This is what spec-driven development tools/products get wrong IMO: the spec should fall out of the prototype, not the other way around. One prototype is worth 100 spec drafts."
Quote-tweets Matt Pocock (@mattpocockuk): "The more I replace plans with prototypes, the better the outputs. Who'd have thought that low fidelity prototypes were better than walls of spec. Oh yeah, the entire industry for 20 years." Point for this video: an HTML artifact is a prototype, and the spec is derived FROM it, inverting spec-first workflows.`,
  },
  '10': {
    file: '10-ralph-loops.md',
    chapter: 'Ralph Loops',
    material: `SOURCE — Jarrod Watts (@jarrodwatts), "You Need More Than a Ralph Loop", https://x.com/jarrodwatts/status/2052372045829382430.
Why long-running/Ralph loops work at all: they spend more tokens = scale test-time compute (on BrowseComp, Sonnet 4.6 at 10x tokens scored ~10 points higher). It breaks down when the task needs more context than the window holds, which is the problem Ralph (rerun the same prompt in a fresh context) was invented to dodge.
His thesis: a bare Ralph loop is NOT enough, for three reasons that a good long-running setup must fix:
1) Ambiguity compounds: each iteration's output is the next iteration's input, so one decision you would not have made propagates and everything after drifts. Fix: a setup/interview phase up front (his /interview skill, ~20-50 clarifying questions, akin to Matt Pocock's grill-me) BEFORE any autonomous loop, then break the now-specific goal into milestones/tasks. Visualize as a tree of outcomes: clarifying up front prunes the branches far from what you wanted.
2) Multi-agent beats single agent: orchestrator + subagents (an implementer and a separate reviewer that sees the code fresh, with no prior bias) going back and forth outperforms one good agent. Costs more tokens (horizontal test-time compute).
3) Cross-context memory: agents read/write durable files on every fresh context — GOAL.md (top-level goal), STANDARDS.md (non-negotiable quality bar), IMPLEMENT.md (workflow), PROGRESS.md (running log of decisions/work).`,
  },
  '11': {
    file: '11-goal.md',
    chapter: '/goal Mode',
    material: `SOURCE A — Jarrod Watts (@jarrodwatts), https://x.com/jarrodwatts/status/2052372045829382430, on how Codex /goal works under the hood:
A SQLite "thread_goals" table stores each goal as a row (objective, id, status, optional token budget). New tools get_goal / update_goal track and update progress. It then runs a standard ralph loop with this prompt shape: "Continue working toward the active thread goal. <untrusted_objective>...</untrusted_objective> Budget: time spent, tokens used, token budget, tokens remaining. Before deciding that the goal is achieved, perform a completion audit against the actual current state." Note the <untrusted_objective> tag (the objective is treated as untrusted input) and the explicit completion audit. This solves the agent "stopping after 15 minutes to ask if it's ok to keep going".

SOURCE B — Bootoshi (@KingBootoshi), 14-min video, https://x.com/kingbootoshi/status/2052510026535936157 (transcribed):
He ran a single /goal for 11h26m overnight building "Agent Runtime Kernel". His workflow: have Codex research the codebase + web-search via Exa, co-write a very detailed PRD (goals AND non-goals, ~1500 lines), then "/goal: implement this PRD fully." On every compaction, goal mode re-pings the agent to stay focused and it re-reads the PRD to get back up to date. Key line: "have a feature, have a goal, and more importantly have a SOLUTION, an END to the goal", otherwise the agent runs forever. The deepest point: "done means PROPER" because completion is enforced programmatically by guardrails, not by the model's say-so. His guardrail stack: strict TypeScript (won't build on bad types), Biome formatter/linter, custom ESLint plugins enforcing architecture, files capped under 500 lines, a centralized logger, a custom harness that programmatically forbids skipping tests, a Biome no-excessive-cognitive-complexity rule (no god functions), knip to delete dead code, a lefthook pre-commit that blocks commit unless types+lint+format pass and denies --no-verify, and a 3-layer test suite (unit/mock, integration against a real SQLite db, real end-to-end in Docker) plus a written testing philosophy so the agent can't write useless "1+1==2" mock tests. He calls the implement -> real-e2e-test -> find unanticipated problem -> fix feedback loop "autoresearch on steroids".`,
  },
  '12': {
    file: '12-writing-effective-goals.md',
    chapter: 'Writing Effective Goals',
    material: `SOURCE A — Vincent Koc (@vincent_koc), https://x.com/vincent_koc/status/2050983370902184019:
"I've been using /goal for ~3 days on OpenClaw. 13 runs. Gazillion tokens. Many PRs. The lesson isn't 'i used /goal a lot.' It's that /goal is NOT a 'do my ticket' button. It's a CONSTRAINT WORKFLOW. I want to keep the ship on course." The effective-goal framing: a goal is a set of constraints that keeps a long run on course, not a task ticket you hand off.

SOURCE B — Jarrod Watts (@jarrodwatts), https://x.com/jarrodwatts/status/2052372045829382430:
"Ambiguity compounds." Writing an effective goal means removing ambiguity UP FRONT, before any autonomous loop, via an interview/setup phase (his /interview skill, 20-50 clarifying questions). This forces YOU, not just the agent, to decide what you actually want; the agent surfaces assumptions and decisions you had not considered. The now-specific goal is broken into milestones and tasks. Visualize: every unclarified decision is a branch the agent picks for you, usually away from what you envisioned; clarifying prunes those branches.`,
  },
}

phase('Enrich')

function prompt(key) {
  const v = SOURCES[key]
  return `You are enriching ONE already-written video script in Ray's "Loopy AI" class, using class-script-writer voice. The first pass wrote this video from inbox notes because the live source fetch had failed. I have now fetched the real source. Your job: fold in anything the script genuinely MISSED, and nothing else.

WHY THIS MATTERS: a sibling video (Removing Bottlenecks) turned out to have missed the sharpest point of its source. We are checking the rest. Do not pad or rewrite a video that already covers its source well; an honest "already covered" is a good outcome.

VIDEO: ${BASE}/${v.file}  (#${key} "${v.chapter}")

STEP 1 — Read the file. Then read the live source material below and decide, point by point, what the script already covers vs what it misses.

LIVE SOURCE MATERIAL:
${v.material}

STEP 2 — If the script already conveys the source's load-bearing points, make NO edits and report action "already-covered" with a one-line reason. If it misses something material, fold it in:
- Add or extend the minimum prose needed (a few sentences, or one new '##' section if the idea is big enough, e.g. video 11's guardrail stack or video 07's three-agent scoring scheme). Do not bloat; respect the video's duration target in its frontmatter.
- Match the existing voice and the surrounding text. Reuse the script's existing framing and terminology.
- Add a 'Source: <url>' line under any new claim that comes from a specific post.
- Keep continuity: this is video #${key}. You may reference earlier videos by their established names but must not teach a LATER video's topic. Course order: ${SKELETON}.
- ${RULES}

STEP 3 — Edit the file in place with the Edit tool (targeted edits, do not rewrite the whole file unless necessary). Do NOT touch frontmatter. After editing, grep your additions for em/en dashes and remove any.

Return the structured object describing what you did.`
}

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['video', 'action', 'whatAdded', 'wordCountAfter', 'notes'],
  properties: {
    video: { type: 'string' },
    action: { type: 'string', enum: ['enriched', 'already-covered'] },
    whatAdded: { type: 'string', description: 'concrete summary of the prose/section added, or why nothing was needed' },
    wordCountAfter: { type: 'number' },
    notes: { type: 'string', description: 'anything Ray should review; empty string if none' },
  },
}

const keys = Object.keys(SOURCES)
const results = await parallel(
  keys.map(k => () => agent(prompt(k), { label: `enrich:${k}`, phase: 'Enrich', schema: SCHEMA }))
)

const out = results.filter(Boolean)
return {
  enriched: out.filter(r => r.action === 'enriched').map(r => `${r.video}: ${r.whatAdded}`),
  alreadyCovered: out.filter(r => r.action === 'already-covered').map(r => `${r.video}: ${r.whatAdded}`),
  reviewNotes: out.filter(r => r.notes).map(r => `${r.video}: ${r.notes}`),
  failures: keys.filter((k, i) => !results[i]),
}
