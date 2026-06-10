export const meta = {
  name: 'loop-opportunities-topdown',
  description: 'Top-down: start from loop archetypes + Ray\'s outcomes, hunt where each would create the most leverage',
  phases: [
    { title: 'Hunt', detail: 'Per-archetype + per-outcome hunters look for fit across sessions, skills, workflows, notes' },
    { title: 'Rank', detail: 'Sonnet ranks the hunt findings by leverage, not frequency' },
    { title: 'Design', detail: 'Sonnet designs the top picks as 6-part loops with adversarial entropy guards' },
    { title: 'Compare', detail: 'Sonnet contrasts these designs vs the bottom-up workflow framing' },
  ],
}

const CANON_PATH = '/tmp/loop-scout/loop-canon.md'

const ARCHETYPES = [
  {
    name: 'ralph-loop',
    prompt: 'Ralph loop — same prompt, fresh context window, every iteration sees the previous iteration\'s git history. Long-grinding, code-mutation, autonomous improvement over hours. Look for: codebases Ray owns where the goal is well-defined but the work is grindy. Repos with clear test suites or build commands. Refactors he keeps putting off. Things where "let it cook overnight" would unblock him.',
  },
  {
    name: 'goal-loop',
    prompt: 'Goal loop — give an objective, runtime owns state machine, runs until objective genuinely met. Look for: clear binary objectives Ray repeatedly hand-walked agents through (PR landed, test passing, page Lighthouse > X, video published). Multi-step recipes where the human is just verifying "is it done yet" and re-firing the prompt.',
  },
  {
    name: 'auto-research',
    prompt: 'Auto-research loop — runs experiment, scores against binary eval, mutates code/prompt/asset, keeps wins. Look for: places Ray has measurable scores (A/B tests, view counts, eval scores, conversion, reply rate, page-speed) and an artifact he tunes by hand (titles, thumbnails, prompts, skill descriptions, landing copy).',
  },
  {
    name: 'scheduled-outer',
    prompt: 'Scheduled outer loop — pulls next task off a queue on a cadence and hands it to an inner loop. Look for: queues that already exist (todos.yaml, GitHub issues, blog post inbox, video to-film/ folders, Linear, idea inboxes) where Ray manually picks the next item every morning.',
  },
  {
    name: 'monitor-outer',
    prompt: 'Monitor outer loop — watches an external signal (competitor, log, dashboard, prod metric, social feed, arxiv, channel) and triggers an inner loop when something fires. Look for: tabs Ray refreshes, dashboards he checks, sources he polls — anything that could be a push instead of a pull.',
  },
  {
    name: 'cmo-style-aggregator',
    prompt: 'CMO-style daily aggregator (Ray\'s own example) — pulls GA4/Search Console/Supabase/ads/prod errors → writes report → queues safe actions → opens alerts for risky → stores back into Brain. Look for: dashboards Ray reads across to form a morning picture. Data sources that don\'t talk to each other today.',
  },
  {
    name: 'content-pipeline',
    prompt: 'Content pipeline loop (Ray\'s own example) — agent reads PRD → writes next asset → scores against quality gates → saves draft → commits. Look for: content factories with clear quality gates (class scripts, video scripts, thumbnails, newsletter, X articles, YouTube outlines) where the structure is known.',
  },
]

const OUTCOMES = [
  {
    name: 'youtube-growth',
    prompt: 'YouTube channel growth (@RAmjad) — views, watch time, A/B tests, thumbnail iteration, outlier discovery. What loop would consistently move this metric while Ray sleeps?',
  },
  {
    name: 'class-shipping',
    prompt: 'Shipping classes for Agentic Coding School — Loopy AI next, then Skills, Business, etc. Lessons drafted, reviewed by teacher/learner, filmed, edited, published. What loop would compress class shipping cadence?',
  },
  {
    name: 'content-cadence',
    prompt: 'Content cadence across surfaces — YouTube, LinkedIn, X, newsletter, blog. Same source idea fragments into many forms. What loop would keep cadence high without Ray re-typing?',
  },
  {
    name: 'product-bug-velocity',
    prompt: 'Product bug velocity across hyperwhisper, agentstack, agentic-coding-school, matchers, vidtempla. Production errors → root cause → patch → ship. What loop would catch + fix before Ray notices?',
  },
  {
    name: 'research-to-asset',
    prompt: 'Research-to-asset funnel — X scraping, video transcripts, Apple Notes, deep research outputs become class lessons, scripts, articles. What loop would close the gap between captured insight and shipped artifact?',
  },
]

const HUNT_SCHEMA = {
  type: 'object',
  required: ['target', 'fits'],
  properties: {
    target: { type: 'string', description: 'The archetype or outcome name' },
    summary: { type: 'string', description: 'One-paragraph: where this fits Ray right now' },
    fits: {
      type: 'array',
      items: {
        type: 'object',
        required: ['where', 'evidence', 'leverage', 'why_this_archetype'],
        properties: {
          where: { type: 'string', description: 'Specific project/skill/file/workflow where this could live' },
          evidence: { type: 'string', description: 'Concrete evidence from sessions/skills/workflows/notes/commits' },
          leverage: { type: 'number', description: '1-10 leverage score: how much would Ray\'s life change if this ran on rails' },
          why_this_archetype: { type: 'string', description: 'Why this archetype specifically (vs another one) is the right shape' },
          oracle: { type: 'string', description: 'External oracle for the check step' },
        },
      },
    },
  },
}

const RANKED_SCHEMA = {
  type: 'object',
  required: ['ranked'],
  properties: {
    ranked: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'archetype', 'leverage_score', 'pain_score', 'shippability_score', 'composite', 'rationale'],
        properties: {
          title: { type: 'string' },
          archetype: { type: 'string' },
          target_outcome: { type: 'string' },
          leverage_score: { type: 'number', description: '1-10 — upside if running on rails' },
          pain_score: { type: 'number', description: '1-10 — how much does Ray feel this manually today' },
          shippability_score: { type: 'number', description: '1-10 — can he ship the v1 this week with existing tools (Workflow, CronCreate, /loop, Slack bot, codex thread automations)' },
          composite: { type: 'number', description: 'Composite score, leverage-weighted' },
          rationale: { type: 'string' },
          consolidates: { type: 'array', items: { type: 'string' }, description: 'Hunter findings this consolidates' },
        },
      },
    },
  },
}

const LOOP_DESIGN_SCHEMA = {
  type: 'object',
  required: ['title', 'archetype', 'inputs', 'action', 'check', 'memory', 'exit', 'surface', 'entropy_guard', 'first_step', 'outer_loop_idea', 'kill_switch'],
  properties: {
    title: { type: 'string' },
    archetype: { type: 'string' },
    inputs: { type: 'string' },
    action: { type: 'string' },
    check: { type: 'string', description: 'External oracle — tests, Lighthouse, prod errors, reply rate, Stripe, etc.' },
    memory: { type: 'string', description: 'Concrete path or Slack channel' },
    exit: { type: 'string', description: 'Done condition + stuck detection + confidently-wrong detection' },
    surface: { type: 'string' },
    entropy_guard: { type: 'string', description: 'Adversarial reviewer that is a DIFFERENT agent, plus an external oracle the model cannot sweet-talk' },
    first_step: { type: 'string', description: 'Something Ray could literally do today' },
    outer_loop_idea: { type: 'string' },
    kill_switch: { type: 'string', description: 'Token budget, retirement rule, hard cap' },
  },
}

phase('Hunt')

const archetypeHunters = ARCHETYPES.map(a => () => agent(
  `You are an archetype hunter for Ray. Your archetype is: **${a.name}**.\n\n${a.prompt}\n\n` +
  `READ FIRST: ${CANON_PATH}\n\n` +
  `Search across, sampling not reading fully:\n` +
  `- Recent session jsonls in ~/.claude/projects/ (list 10 most-recently-modified, sample a few)\n` +
  `- ~/.claude/skills/ — what skills already exist that suggest a half-built loop\n` +
  `- ~/Desktop/ray-os/.claude/workflows/ — existing workflows\n` +
  `- ~/Desktop/ray-os/projects/agentic-coding-school/ — class structure and to-film queue\n` +
  `- Recent git log across Ray's main repos: ray-os, agentic-coding-school, hyperwhisper, agentstack, matchers, vidtempla\n` +
  `- /tmp/loop-scout/loop-canon.md for Ray's own examples from Apple Notes\n\n` +
  `Find 2-4 concrete places where THIS archetype would create real leverage. Be specific. Cite files, commit messages, skill names, workflow paths. ` +
  `Score each fit honestly — most archetypes won't fit everywhere. Return target=${a.name}.`,
  { label: `hunt:arch:${a.name}`, phase: 'Hunt', schema: HUNT_SCHEMA, model: 'haiku' }
))

const outcomeHunters = OUTCOMES.map(o => () => agent(
  `You are an outcome hunter for Ray. Your outcome is: **${o.name}**.\n\n${o.prompt}\n\n` +
  `READ FIRST: ${CANON_PATH} for loop taxonomy.\n\n` +
  `Search across:\n` +
  `- ~/Desktop/ray-os/socials/ — content performance + research notes\n` +
  `- ~/Desktop/ray-os/projects/agentic-coding-school/ — class system\n` +
  `- ~/.claude/skills/ — what skills already exist for this outcome\n` +
  `- Recent ~/.claude/projects/ sessions — what is Ray doing manually for this outcome\n` +
  `- Recent git log in the relevant repos\n\n` +
  `Identify 2-4 places where a loop would meaningfully move this outcome. For each, name the archetype from the canon that fits best. ` +
  `Score by leverage. Return target=${o.name}.`,
  { label: `hunt:out:${o.name}`, phase: 'Hunt', schema: HUNT_SCHEMA, model: 'sonnet' }
))

const hunts = await parallel([...archetypeHunters, ...outcomeHunters])
const validHunts = hunts.filter(Boolean)
const allFits = validHunts.flatMap(h => (h.fits || []).map(f => ({ ...f, target: h.target })))
log(`Hunts done. ${validHunts.length}/${hunts.length} returned. ${allFits.length} fits found.`)

phase('Rank')
const ranked = await agent(
  `You are ranking loop candidates for Ray by composite score, NOT by how often they appear.\n\n` +
  `READ FIRST: ${CANON_PATH}\n\n` +
  `Hunter fits:\n\`\`\`json\n${JSON.stringify(allFits, null, 2)}\n\`\`\`\n\n` +
  `Per-target summaries:\n${validHunts.map(h => `- **${h.target}**: ${h.summary || ''}`).join('\n')}\n\n` +
  `Consolidate into 6-8 distinct loop candidates. Multiple hunter findings can collapse into one candidate. ` +
  `Score each on:\n` +
  `- leverage (1-10): upside if running on rails\n` +
  `- pain (1-10): how much Ray feels this manually today\n` +
  `- shippability (1-10): can a v1 ship this week with existing tools (Workflow, CronCreate, /loop, Slack bot, codex thread automations)\n` +
  `- composite = leverage * 1.5 + pain * 1.0 + shippability * 1.0\n\n` +
  `Sort by composite descending. Return all 6-8 — we'll design the top ones.`,
  { label: 'rank', phase: 'Rank', schema: RANKED_SCHEMA, model: 'sonnet' }
)

const topPicks = (ranked?.ranked || []).slice(0, 6)
log(`Ranked ${ranked?.ranked?.length || 0} candidates. Designing top ${topPicks.length}.`)

phase('Design')
const designs = await parallel(topPicks.map(p => () => agent(
  `Design this loop concretely for Ray. Fill the full anatomy. Be specific about paths, channels, commands, oracles.\n\n` +
  `READ FIRST: ${CANON_PATH}\n\n` +
  `Candidate:\n\`\`\`json\n${JSON.stringify(p, null, 2)}\n\`\`\`\n\n` +
  `Constraints:\n` +
  `- entropy_guard MUST include both an adversarial reviewer (different agent than writer) AND an external oracle\n` +
  `- first_step MUST be something Ray could literally do today with existing tools\n` +
  `- kill_switch MUST be concrete (token budget, retirement rule, hard cap iterations)\n` +
  `- name the actual filesystem path or Slack channel for memory\n` +
  `- name the actual file/repo the loop would live in\n`,
  { label: `design:${p.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 30)}`, phase: 'Design', schema: LOOP_DESIGN_SCHEMA, model: 'sonnet' }
)))

phase('Compare')
const comparison = await agent(
  `You are framing how this top-down/outcome-first analysis would likely differ from a bottom-up session-log clustering of the same source material. ` +
  `Do NOT invent the bottom-up output — just characterize where these two methodologies systematically disagree.\n\n` +
  `Top-down findings:\n\`\`\`json\n${JSON.stringify(designs.filter(Boolean), null, 2)}\n\`\`\`\n\n` +
  `Ranked candidates:\n\`\`\`json\n${JSON.stringify(ranked?.ranked || [], null, 2)}\n\`\`\`\n\n` +
  `Write a short markdown report:\n` +
  `1. What this methodology likely OVER-surfaces (high-leverage but rare in sessions)\n` +
  `2. What this methodology likely MISSES that bottom-up would catch (frequent annoyances under leverage threshold)\n` +
  `3. Which 2-3 candidates feel robust regardless of methodology\n` +
  `4. What Ray should look for when comparing the two workflow outputs side by side`,
  { label: 'compare', phase: 'Compare', model: 'sonnet' }
)

return {
  hunters_run: validHunts.length,
  total_fits: allFits.length,
  ranked: ranked?.ranked || [],
  designs: designs.filter(Boolean),
  methodology_compare: comparison,
}
