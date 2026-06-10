export const meta = {
  name: 'loop-opportunities',
  description: 'Mine recent ~/.claude sessions for tasks that could become Loopy-AI-style loops',
  phases: [
    { title: 'Scout', detail: 'Haiku scouts read recent session logs per-project' },
    { title: 'Cluster', detail: 'Sonnet clusters raw patterns into loop candidates' },
    { title: 'Design', detail: 'Sonnet designs each top candidate as a 6-part loop' },
  ],
}

const PROJECTS = [
  '-Users-ray-Desktop-ray-os',
  '-Users-ray-Desktop-agentstack',
  '-Users-ray-Desktop-ray-os-projects-agentic-coding-school-to-film-loopy-ai--inbox-x-mining',
  '-Users-ray-Desktop-agentic-coding-school',
  '-Users-ray-Desktop-hyperwhisper',
  '-Users-ray-Desktop-watchllm',
  '-Users-ray-Desktop-agentic-coding-school--claude-worktrees-admin-design-system',
  '-Users-ray-Desktop-agentic-coding-school--claude-worktrees-glossary-tagging-admin',
  '-Users-ray-Desktop-matchers-matcher-tokyo-9000',
  '-Users-ray-Desktop-agentstack--claude-worktrees-escalation-transcript-fix',
  '-Users-ray-Desktop-hyperwhisper--claude-worktrees-local-api-server-phase1',
  '-Users-ray-Desktop-hyperwhisper--claude-worktrees-homepage-mcp-card',
  '-Users-ray-Desktop-hyperwhisper--claude-worktrees-pr-199-review',
  '-Users-ray-Desktop-vidtempla',
  '-Users-ray-Desktop-agentic-coding-school--claude-worktrees-discord-integration',
]

const PATTERN_SCHEMA = {
  type: 'object',
  required: ['project', 'patterns'],
  properties: {
    project: { type: 'string' },
    summary: { type: 'string', description: 'One-paragraph: what was Ray actually doing here recently' },
    patterns: {
      type: 'array',
      description: 'Recurring or loop-worthy tasks Ray did manually',
      items: {
        type: 'object',
        required: ['name', 'what_ray_did', 'why_loopable', 'frequency_signal'],
        properties: {
          name: { type: 'string', description: 'Short kebab-case name for the pattern' },
          what_ray_did: { type: 'string', description: 'Concrete steps Ray ran, with evidence (file names, prompts, tool calls)' },
          why_loopable: { type: 'string', description: 'Why this matches the loop criteria from the canon' },
          frequency_signal: { type: 'string', description: 'How many times / how often this showed up' },
          oracle_hint: { type: 'string', description: 'What external check could verify a "done" turn (tests, metric, reply, etc.)' },
        },
      },
    },
  },
}

const CANDIDATE_SCHEMA = {
  type: 'object',
  required: ['candidates'],
  properties: {
    candidates: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'cluster_evidence', 'fit_score', 'why_now'],
        properties: {
          title: { type: 'string' },
          cluster_evidence: { type: 'string', description: 'Which scout findings cluster into this candidate' },
          fit_score: { type: 'number', description: '1-10 score against the 6-criteria loop test' },
          why_now: { type: 'string', description: 'Why Ray would feel this immediately (pain or compounding upside)' },
          loop_family: { type: 'string', enum: ['/loop', '/goal', 'auto-research', 'ralph', 'outer-monitor', 'hybrid'] },
          inner_or_outer: { type: 'string', enum: ['inner', 'outer', 'both'] },
        },
      },
    },
  },
}

const LOOP_DESIGN_SCHEMA = {
  type: 'object',
  required: ['title', 'family', 'inputs', 'action', 'check', 'memory', 'exit', 'surface', 'entropy_guard', 'first_step'],
  properties: {
    title: { type: 'string' },
    family: { type: 'string' },
    inputs: { type: 'string', description: 'Trigger + data feed' },
    action: { type: 'string', description: 'What the loop does per turn' },
    check: { type: 'string', description: 'The oracle — external if possible' },
    memory: { type: 'string', description: 'Where state is parked (filesystem path or Slack channel)' },
    exit: { type: 'string', description: 'Concrete done condition and stuck/wrong detection' },
    surface: { type: 'string', description: 'Where Ray reads/reacts' },
    entropy_guard: { type: 'string', description: 'Adversarial reviewer + oracle check that prevents slop compounding' },
    first_step: { type: 'string', description: 'The smallest thing Ray could ship this week to start running the loop' },
    outer_loop_idea: { type: 'string', description: 'Optional — the outer loop that would discover work for this inner loop' },
  },
}

const CANON_PATH = '/tmp/loop-scout/loop-canon.md'

phase('Scout')
const scouts = await parallel(PROJECTS.map(proj => () => {
  const dir = `/Users/ray/.claude/projects/${proj}`
  return agent(
    `You are a Haiku scout reading recent Claude Code session logs to find loop-worthy patterns in Ray's work.\n\n` +
    `READ FIRST: ${CANON_PATH} — that is the loop taxonomy you are testing against.\n\n` +
    `Then survey: ${dir}\n` +
    `- List the 3 most-recently-modified .jsonl files in that directory.\n` +
    `- For each, sample the user-prompt lines (lines containing "user" role) and the tool-use names. Do NOT try to read full files — they are huge. Use head/tail/grep to sample.\n` +
    `- Identify: what was Ray doing? What multi-step recipes repeated? What did Ray manually shuttle between (prompt → check → re-prompt)? What was waiting on an external signal?\n\n` +
    `Apply the loop criteria from the canon. Return raw patterns — do NOT design loops yet, that is a later stage.\n\n` +
    `Project slug: ${proj}`,
    { label: `scout:${proj.replace(/^-Users-ray-Desktop-?/, '').slice(0, 40)}`, phase: 'Scout', schema: PATTERN_SCHEMA, model: 'haiku' }
  )
}))

const validScouts = scouts.filter(Boolean)
const allPatterns = validScouts.flatMap(s => (s.patterns || []).map(p => ({ ...p, project: s.project })))
log(`Scouts done. ${validScouts.length}/${PROJECTS.length} returned. ${allPatterns.length} raw patterns.`)

phase('Cluster')
const clustered = await agent(
  `You are clustering raw patterns from ${validScouts.length} project scouts into loop candidates for Ray.\n\n` +
  `READ FIRST: ${CANON_PATH}\n\n` +
  `Raw patterns from scouts:\n\`\`\`json\n${JSON.stringify(allPatterns, null, 2)}\n\`\`\`\n\n` +
  `Per-project summaries:\n${validScouts.map(s => `- **${s.project}**: ${s.summary || '(no summary)'}`).join('\n')}\n\n` +
  `Cluster these into 5-8 distinct loop CANDIDATES. A candidate is a workflow Ray could plausibly automate as a loop. ` +
  `Prefer candidates that appear across multiple projects (compounding leverage) OR are deeply painful in one project. ` +
  `For each candidate, score 1-10 against the six loop-fit criteria. Return only candidates scoring >= 6.`,
  { label: 'cluster', phase: 'Cluster', schema: CANDIDATE_SCHEMA, model: 'sonnet' }
)

const topCandidates = (clustered?.candidates || []).sort((a, b) => b.fit_score - a.fit_score).slice(0, 6)
log(`Clustered into ${clustered?.candidates?.length || 0} candidates. Designing top ${topCandidates.length}.`)

phase('Design')
const designs = await parallel(topCandidates.map(c => () =>
  agent(
    `Design a concrete loop for Ray based on this candidate.\n\n` +
    `READ FIRST: ${CANON_PATH}\n\n` +
    `Candidate:\n\`\`\`json\n${JSON.stringify(c, null, 2)}\n\`\`\`\n\n` +
    `Fill the six-part anatomy precisely. Be concrete: name actual files, paths, commands, Slack channels, oracles. ` +
    `If filesystem memory, give the exact directory under ~/.claude or ray-os. If Slack surface, name what the bot is and what it posts. ` +
    `The entropy_guard must include an adversarial reviewer AND an oracle that lives outside the model. ` +
    `The first_step must be something Ray could literally do today.`,
    { label: `design:${c.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 30)}`, phase: 'Design', schema: LOOP_DESIGN_SCHEMA, model: 'sonnet' }
  )
))

return {
  scouts_run: validScouts.length,
  raw_patterns: allPatterns.length,
  candidates: clustered?.candidates || [],
  designs: designs.filter(Boolean),
}
