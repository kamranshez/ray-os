export const meta = {
  name: 'loop-opportunities-personas',
  description: 'Persona tournament: Boris/Steipete/Karpathy/DHH each propose the first loop Ray should build, then synth',
  phases: [
    { title: 'Survey', detail: 'Quick context pack for personas (skills, repos, content, recent sessions)' },
    { title: 'Propose', detail: 'Four named-taste personas each propose their top 3 loops' },
    { title: 'Cross-judge', detail: 'Each persona adversarially critiques the others\' proposals' },
    { title: 'Synth', detail: 'Find consensus loops + uniquely-valuable single-persona picks, then design' },
  ],
}

const CANON_PATH = '/tmp/loop-scout/loop-canon.md'

const PERSONAS = [
  {
    name: 'boris',
    persona: `You are Boris Cherny — Anthropic engineer who built Claude Code. You no longer prompt agents; you write loops that prompt agents. Hundreds of agents read your GitHub, Slack, and Twitter and decide what to build next. You believe stage-three discovery layers are the unlock. Your taste:
- Loops > prompts. Always.
- The discovery layer is the high-leverage move: agents that read SIGNAL (GitHub, Slack, Twitter, prod errors) and decide what becomes work
- You distrust "scheduled" loops as too shallow — you want monitor-triggered loops fed by rich signal
- You think most people building "outer loops" are actually just building cron jobs and calling them outer loops
- You care about the receipt: a working stage-three example you can point at`,
  },
  {
    name: 'steipete',
    persona: `You are Peter Steiniger (steipete) — long-running meta-loops with hard guardrails. You use a VISION.md as the constraint document for your agents and run threads (not subagents) with continuous goals. Your taste:
- Without a VISION.md the loop goes haywire — guardrails are everything
- Threads > subagents because threads can carry their own goal indefinitely
- Long-running > scheduled — agents should think continuously, not fire-and-die
- You're skeptical of pure metric optimization; you want SUBJECTIVE quality kept in check by a human-curated rubric
- You'd rather build one loop that runs for 6 months than 10 that fizzle in a week`,
  },
  {
    name: 'karpathy',
    persona: `You are Andrej Karpathy — auto-research loop person. Define a binary eval, let the loop mutate code/prompts/assets, keep what scores higher. Your taste:
- If you can't write the eval, the loop is bullshit
- Most "AI workflows" are bullshit because their "check" is the same model that wrote the work
- You want NUMBERS — reply rate, view count, F1, conversion, page-speed — preferably automated
- You're suspicious of qualitative gates. "Does Ray like it?" is not an eval
- A loop without an eval is just a fancy chatbot
- The discovery layer Boris talks about is interesting but you'd start with one tight eval-driven loop and prove leverage there first`,
  },
  {
    name: 'dhh',
    persona: `You are David Heinemeier Hansson — Rails creator, anti-complexity, ship fast. Your taste:
- 90% of "agentic workflows" should be cron + bash
- If a Python script with a SQLite file solves it, do that. Don't reach for agents
- You are deeply skeptical of "discovery layers" — those are how people build six months of plumbing to ship nothing
- A loop you actually use beats a loop you architected
- Pick the WEEKEND-shippable version. Build the manual version first, then loop-ify the part that's already painful
- You'd push Ray hard on "what would breaking this stop you from doing tomorrow" — if the answer is nothing, kill it`,
  },
]

const PROPOSAL_SCHEMA = {
  type: 'object',
  required: ['persona', 'proposals'],
  properties: {
    persona: { type: 'string' },
    opening_take: { type: 'string', description: 'Your one-paragraph opinion on Ray\'s loop situation' },
    proposals: {
      type: 'array',
      minItems: 3,
      maxItems: 3,
      items: {
        type: 'object',
        required: ['title', 'why_this_first', 'inputs', 'action', 'check_oracle', 'memory', 'exit', 'surface', 'kill_signal', 'first_step_today'],
        properties: {
          title: { type: 'string' },
          why_this_first: { type: 'string', description: 'In YOUR taste, why this loop, not another' },
          inputs: { type: 'string' },
          action: { type: 'string' },
          check_oracle: { type: 'string', description: 'The external oracle. If you can\'t name one, say so' },
          memory: { type: 'string' },
          exit: { type: 'string' },
          surface: { type: 'string' },
          kill_signal: { type: 'string', description: 'How Ray knows to kill this loop' },
          first_step_today: { type: 'string', description: 'Concrete first step Ray could ship today' },
          unique_to_my_taste: { type: 'string', description: 'What about this proposal is distinctly YOUR taste vs the other personas' },
        },
      },
    },
  },
}

const CRITIQUE_SCHEMA = {
  type: 'object',
  required: ['critic', 'verdicts'],
  properties: {
    critic: { type: 'string' },
    verdicts: {
      type: 'array',
      items: {
        type: 'object',
        required: ['target_persona', 'target_title', 'verdict', 'specific_concern'],
        properties: {
          target_persona: { type: 'string' },
          target_title: { type: 'string' },
          verdict: { type: 'string', enum: ['strong-yes', 'yes-with-fix', 'no'] },
          specific_concern: { type: 'string' },
          would_steal: { type: 'string', description: 'What about this proposal would you steal for YOUR version, if anything' },
        },
      },
    },
  },
}

const SYNTH_SCHEMA = {
  type: 'object',
  required: ['consensus_loops', 'uniquely_valuable', 'rejected', 'methodology_take'],
  properties: {
    consensus_loops: {
      type: 'array',
      description: 'Loops 3+ personas agreed on (strong-yes or yes-with-fix from 3+)',
      items: {
        type: 'object',
        required: ['title', 'supporters', 'reconciled_design'],
        properties: {
          title: { type: 'string' },
          supporters: { type: 'array', items: { type: 'string' } },
          reconciled_design: {
            type: 'object',
            required: ['inputs', 'action', 'check_oracle', 'memory', 'exit', 'surface', 'entropy_guard', 'first_step_today'],
            properties: {
              inputs: { type: 'string' },
              action: { type: 'string' },
              check_oracle: { type: 'string' },
              memory: { type: 'string' },
              exit: { type: 'string' },
              surface: { type: 'string' },
              entropy_guard: { type: 'string' },
              first_step_today: { type: 'string' },
            },
          },
        },
      },
    },
    uniquely_valuable: {
      type: 'array',
      description: 'Loops only ONE persona proposed but whose unique taste reveals something the consensus missed',
      items: {
        type: 'object',
        required: ['title', 'proposer', 'why_it_matters_anyway'],
        properties: {
          title: { type: 'string' },
          proposer: { type: 'string' },
          why_it_matters_anyway: { type: 'string' },
        },
      },
    },
    rejected: {
      type: 'array',
      description: 'Loops most personas rejected and why',
      items: {
        type: 'object',
        required: ['title', 'proposer', 'failure_mode'],
        properties: {
          title: { type: 'string' },
          proposer: { type: 'string' },
          failure_mode: { type: 'string' },
        },
      },
    },
    methodology_take: { type: 'string', description: 'What the persona tournament surfaced that aggregate models would smooth over' },
  },
}

phase('Survey')
const contextPack = await agent(
  `Build a tight context pack for persona judges. Read:\n` +
  `- ${CANON_PATH} (the loop taxonomy + Ray's own examples)\n` +
  `- ~/.claude/skills/ — list directory; identify skill clusters\n` +
  `- ~/Desktop/ray-os/.claude/workflows/ — list existing workflows\n` +
  `- ~/Desktop/ray-os/projects/agentic-coding-school/to-film/ — what's queued\n` +
  `- git log of ~/Desktop/ray-os over last 30 days (one-line summary)\n` +
  `- ls -1t ~/.claude/projects/ | head -15 — what Ray has been actively working on\n\n` +
  `Return a markdown context pack ≤ 1000 words covering: Ray's stack, surfaces, existing skills/workflows, content queues, repos. ` +
  `No analysis, just facts. The personas will form their OWN opinions on this.`,
  { label: 'survey:context', phase: 'Survey', model: 'sonnet' }
)

phase('Propose')
const proposals = await parallel(PERSONAS.map(p => () => agent(
  `${p.persona}\n\n` +
  `READ FIRST: ${CANON_PATH} (the loop canon you've been operating in).\n\n` +
  `Ray's context pack:\n${contextPack}\n\n` +
  `Propose your top 3 loops for Ray to build FIRST. In your voice, with your taste. ` +
  `If you'd disagree with another persona's likely picks, say so in your opening_take. ` +
  `Each proposal must name a real external oracle — or admit there isn't one and explain why you proposed it anyway.`,
  { label: `propose:${p.name}`, phase: 'Propose', schema: PROPOSAL_SCHEMA, model: 'sonnet' }
)))

const validProposals = proposals.filter(Boolean)
const proposalSummary = validProposals.map(p =>
  `### ${p.persona}\n_Opening:_ ${p.opening_take || ''}\n${(p.proposals || []).map((pr, i) => `${i + 1}. **${pr.title}** — ${pr.why_this_first}`).join('\n')}`
).join('\n\n')

log(`${validProposals.length} personas proposed. Cross-judging.`)

phase('Cross-judge')
const critiques = await parallel(PERSONAS.map(p => () => agent(
  `${p.persona}\n\n` +
  `You are now critiquing the OTHER personas' proposals adversarially. Read each, give a verdict, name your specific concern. ` +
  `Be ruthless about your taste. If DHH proposed a complex agent stack, call it out. If Karpathy proposed something without an eval, call it out. If Boris proposed a discovery layer, ask if it's overengineered. If Steipete proposed a multi-month loop, ask if there's a faster proof.\n\n` +
  `All proposals:\n${proposalSummary}\n\n` +
  `Full proposal data:\n\`\`\`json\n${JSON.stringify(validProposals, null, 2)}\n\`\`\`\n\n` +
  `Do NOT critique your own proposals. Critique the other 9.`,
  { label: `critique:${p.name}`, phase: 'Cross-judge', schema: CRITIQUE_SCHEMA, model: 'sonnet' }
)))

const validCritiques = critiques.filter(Boolean)
log(`${validCritiques.length} critique passes done.`)

phase('Synth')
const synthesis = await agent(
  `You are synthesizing a persona tournament. Find consensus, find uniquely-valuable single-persona insight, reject what most personas killed.\n\n` +
  `READ: ${CANON_PATH}\n\n` +
  `All proposals:\n\`\`\`json\n${JSON.stringify(validProposals, null, 2)}\n\`\`\`\n\n` +
  `All cross-critiques:\n\`\`\`json\n${JSON.stringify(validCritiques, null, 2)}\n\`\`\`\n\n` +
  `Rules:\n` +
  `- A consensus loop has 3+ personas voting strong-yes or yes-with-fix on it (or on a near-equivalent proposal under a different name — collapse synonyms)\n` +
  `- A uniquely valuable single-persona pick is one where the taste of THAT specific persona reveals something the others would miss\n` +
  `- Reconcile the design by taking the best constraint from each supporting persona (e.g. Karpathy's eval + Steipete's VISION.md + DHH's kill switch)\n` +
  `- Be specific about what this methodology surfaced vs what aggregate-of-models clustering would have smoothed over`,
  { label: 'synth', phase: 'Synth', schema: SYNTH_SCHEMA, model: 'sonnet' }
)

return {
  context_pack: contextPack,
  proposals: validProposals,
  critiques: validCritiques,
  synthesis,
}
