export const meta = {
  name: 'loopy-ai-stub-walk',
  description: 'Sequentially flesh out every loopy-ai stub video into a full class script, carrying a rolling course summary (ledger) forward so each video has continuity without reading the full text of the others.',
  phases: [
    { title: 'Seed', detail: 'summarize the intro to seed the rolling ledger' },
    { title: 'Walk', detail: 'walk 02..29 in order; write each stub, append its summary to the ledger; finished videos pass through as anchors' },
  ],
}

const BASE = '/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/loopy-ai'
const SKILL = '/Users/ray/Desktop/ray-os/.claude/skills/class-script-writer'
const EXEMPLARS = [`${BASE}/02-loop-stack.md`, `${BASE}/06-borrowed-verifiers.md`]

// Ordered course map. status: 'done' = already written (freeze, use as anchor); 'stub' = flesh out.
const VIDEOS = [
  { n: '01', file: '01-intro.md', chapter: 'Intro', status: 'done' },
  { n: '02', file: '02-loop-stack.md', chapter: 'The Loop Stack', status: 'done' },
  { n: '03', file: '03-strip-the-model-out.md', chapter: 'Strip The Model Out', status: 'stub' },
  { n: '04', file: '04-l1-essentials.md', chapter: 'L1 Essentials', status: 'stub' },
  { n: '05', file: '05-closing-the-loop.md', chapter: 'Closing The Loop', status: 'stub' },
  { n: '06', file: '06-borrowed-verifiers.md', chapter: 'Borrowed Verifiers', status: 'done' },
  { n: '07', file: '07-adversarial-reviewer-skill.md', chapter: 'Pair Every Creator With An Attacker', status: 'stub' },
  { n: '08', file: '08-architecting-the-loop.md', chapter: 'Architecting The Loop', status: 'stub' },
  { n: '09', file: '09-html-artefacts-for-output.md', chapter: 'HTML Artefacts For Output', status: 'stub' },
  { n: '10', file: '10-ralph-loops.md', chapter: 'Ralph Loops', status: 'stub' },
  { n: '11', file: '11-goal.md', chapter: '/goal Mode', status: 'stub' },
  { n: '12', file: '12-writing-effective-goals.md', chapter: 'Writing Effective Goals', status: 'stub' },
  { n: '13', file: '13-dont-pre-sequence-the-backlog.md', chapter: "Don't Pre-Sequence The Backlog", status: 'stub' },
  { n: '14', file: '14-the-autonomy-dial.md', chapter: 'The Autonomy Dial', status: 'stub' },
  { n: '15', file: '15-l4-workers.md', chapter: 'L4 Worker Loops', status: 'stub' },
  { n: '16', file: '16-routines-scheduled-tasks.md', chapter: 'Routines And Scheduled Tasks', status: 'stub' },
  { n: '17', file: '17-autoresearch.md', chapter: 'Autoresearch', status: 'stub' },
  { n: '18', file: '18-auto-research-for-non-technical-work.md', chapter: 'Auto Research For Non-Technical Work', status: 'done' },
  { n: '19', file: '19-l5-discovery.md', chapter: 'L5 Discovery Loops', status: 'stub' },
  { n: '20', file: '20-ace-three-role-split.md', chapter: 'The Three Role Split (ACE)', status: 'stub' },
  { n: '21', file: '21-teacher-learner-pattern.md', chapter: 'The Teacher Learner Pattern', status: 'stub' },
  { n: '22', file: '22-bug-triage-loop.md', chapter: 'The Bug Triage Loop', status: 'stub' },
  { n: '23', file: '23-echo-chamber.md', chapter: 'Echo Chamber Failure Mode', status: 'stub' },
  { n: '24', file: '24-governance-primitives.md', chapter: 'Governance Primitives', status: 'stub' },
  { n: '25', file: '25-slack-as-your-command-center.md', chapter: 'Slack As Your Command Center', status: 'stub' },
  { n: '26', file: '26-keeping-you-in-the-loop.md', chapter: 'Keeping You In The Loop', status: 'stub' },
  { n: '27', file: '27-mission-command.md', chapter: 'Mission Command', status: 'stub' },
  { n: '28', file: '28-removing-bottlenecks.md', chapter: 'Removing Bottlenecks', status: 'stub' },
  { n: '29', file: '29-loop-design-as-craft.md', chapter: 'Where Taste Went', status: 'done' },
]

const SKELETON = VIDEOS.map(v => `${v.n}. ${v.chapter}${v.status === 'done' ? '  (already written)' : ''}`).join('\n')

const WRITER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['written', 'wordCount', 'summary', 'sourcesFetched', 'sourcesFailed', 'imagesPlaced', 'notes'],
  properties: {
    written: { type: 'boolean', description: 'true if the file was overwritten with a full script' },
    wordCount: { type: 'number', description: 'approximate word count of the finished script body' },
    summary: { type: 'string', description: '100-140 words: what the FINISHED video now covers, the key terms/framing it introduces, and any forward hooks it sets up. This goes into the ledger for the next video.' },
    sourcesFetched: { type: 'array', items: { type: 'string' }, description: 'URLs successfully fetched and used' },
    sourcesFailed: { type: 'array', items: { type: 'string' }, description: 'URLs that could not be fetched via Exa or Chrome' },
    imagesPlaced: { type: 'number', description: 'number of [IMAGE: ...] + embed placeholders placed' },
    notes: { type: 'string', description: 'anything Ray should review (thin source material, judgment calls, gaps). Empty string if none.' },
  },
}

const RULES = `CLASS-SCRIPT-WRITER RULES (the voice and shape every video must hit):
- Essay the camera follows, NOT an outline or bullet beats. Write it top to bottom in prose.
- Second person, direct, confident, no hedging. Short paragraphs (1-3 sentences). Vary sentence length; fragments for emphasis are good.
- Lead with the point, then support it. Cold open with a one-sentence thesis in the first paragraph. No fluff intro.
- Sections: (1) cold-open thesis, (2) the problem / what everyone gets wrong, (3) the core insight, (4) two to four supporting sections, (5) a concrete numbered Demo with specific tools and outputs, (6) a single-blockquote Key Insight that could be a tweet, (7) a one-to-three-line closing beat. Section names can flex to the topic.
- '##' headings only. NEVER an H1 '#' title (Obsidian uses the filename).
- Separate major sections with a '---' on its own line.
- HARD RULE: no em dashes and no en dashes anywhere. Use commas, periods, or rephrase. Hyphens inside compound words (kebab-case) are fine. Grep your own output for the characters before finishing and remove every one.
- Inline sources as 'Source: https://...' directly under the claim they support.
- Images: place 2-4 placeholders. Above each embed write a one-line description '[IMAGE: dark canvas, ... what it shows ...]', then the embed on the next line as ![[images/<slug>/<name>.png]] where <slug> is this video's frontmatter alias (kebab-case) and <name> is a short kebab descriptor. Typical placement: one after the problem, one after the core insight, one or two in supporting sections.`

function writerPrompt(v, ledger) {
  return `You are writing ONE finished video script for Ray's "Loopy AI" class (an Agentic Coding School course that climbs an eight-level "loop stack", L0 to L7). Your job: turn the stub at the path below into a polished, film-ready script, in Ray's voice, fitting its exact place in the course sequence.

WHY THIS MATTERS: this is video ${v.n} of a strictly ordered course. Each video must build on what came before and must NOT re-teach earlier material or poach a later video's topic. You are given a rolling ledger of everything covered so far and a skeleton of the whole course so you can hit your lane precisely.

== THE STUB TO FLESH OUT ==
Read this file first: ${BASE}/${v.file}
It contains the intended topic, key beats, source links, and frontmatter. Honor its frontmatter (duration, batch, order, batch_name, class, chapter, aliases). The <slug> for image folders is the 'aliases' value.

== VOICE EXEMPLARS (read these, same class, already finished) ==
- ${EXEMPLARS[0]}
- ${EXEMPLARS[1]}
Optionally skim ${SKILL}/references/style-guide.md if you need more on voice.

== COURSE SKELETON (all 29, in order) ==
${SKELETON}

Your video is #${v.n} "${v.chapter}". Everything numbered below you is a LATER video. Do not teach those topics. You may set up a one-line forward hook ("we'll get to X soon") but do not deliver X.

== ROLLING LEDGER (what every prior video already established) ==
${ledger}

Use the ledger to reference earlier ideas by their established framing ("the borrowed verifier we met in the closing-the-loop segment") instead of re-explaining them. Do NOT read the full text of those other videos; the ledger is your continuity source.

== SOURCES ==
If the stub lists X/Twitter or web URLs, fetch them and fold the real detail in:
1. First load Exa tools with ToolSearch query "select:mcp__claude_ai_Exa__web_search_exa,mcp__claude_ai_Exa_Advanced__web_fetch_exa" and use web_fetch_exa / web_search_exa.
2. If Exa fails or returns nothing usable, fall back to Claude-in-Chrome: ToolSearch query "select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page", then create a tab, navigate to the URL, and read_page.
3. Record any URL you could not retrieve in sourcesFailed. Never block the whole script on one dead link; write the best version you can and note the gap.
You may also consult shared research in ${BASE}/_inbox/ (sources-x.md, sources-notes.md) if the stub points there.

${RULES}

== OUTPUT ==
Write the finished script with the Write tool, OVERWRITING ${BASE}/${v.file} in place. Keep the frontmatter but DELETE the 'status: stub' line (this video is no longer a stub). Do not add an H1.
Then return the structured object. The 'summary' field is critical: it becomes this video's entry in the ledger that the NEXT video reads, so make it an accurate 100-140 word account of what the finished video actually covers and which terms it introduced.`
}

// ---- Seed the ledger with the (frozen) intro ----
phase('Seed')
const introSummary = await agent(
  `Read ${BASE}/01-intro.md, the opening video of Ray's "Loopy AI" class. Return ONLY a 100-140 word summary of what it establishes: its thesis, the framing and vocabulary it introduces, and the promise it makes to the viewer. WHY: this seeds a rolling ledger that every later video reads for continuity, so be precise about named concepts.`,
  { label: 'seed:01-intro', phase: 'Seed', model: 'haiku' }
)
let ledger = `## 01. Intro\n${introSummary}`

// ---- Walk 02..29 in order ----
phase('Walk')
const results = []
for (const v of VIDEOS) {
  if (v.n === '01') continue

  if (v.status === 'done') {
    // Anchor: do not rewrite. Summarize into the ledger so downstream stubs have accurate continuity.
    const s = await agent(
      `Read ${BASE}/${v.file}, an already-finished video ("${v.chapter}") in Ray's "Loopy AI" class. Return ONLY a 100-140 word summary of what it covers: its core idea, the key terms it introduces, and anything a later video would reference. WHY: this extends a rolling ledger used by later videos for continuity; do not rewrite the file.`,
      { label: `anchor:${v.n}`, phase: 'Walk', model: 'haiku' }
    )
    ledger += `\n\n## ${v.n}. ${v.chapter}\n${s}`
    log(`anchor ${v.n} ${v.chapter} — summarized into ledger`)
    results.push({ n: v.n, chapter: v.chapter, action: 'anchor' })
    continue
  }

  // Stub: flesh it out, then append its summary to the ledger before moving on.
  const r = await agent(writerPrompt(v, ledger), { label: `write:${v.n}`, phase: 'Walk', schema: WRITER_SCHEMA })
  if (r && r.summary) {
    ledger += `\n\n## ${v.n}. ${v.chapter}\n${r.summary}`
    log(`wrote ${v.n} ${v.chapter} — ${r.wordCount}w, ${r.imagesPlaced} imgs${r.sourcesFailed && r.sourcesFailed.length ? `, ${r.sourcesFailed.length} source(s) failed` : ''}`)
  } else {
    log(`FAILED ${v.n} ${v.chapter} — no result returned`)
  }
  results.push({ n: v.n, chapter: v.chapter, action: 'written', ...(r || {}) })
}

return {
  ledgerWordCount: ledger.split(/\s+/).length,
  written: results.filter(r => r.action === 'written' && r.written).map(r => `${r.n} ${r.chapter} (${r.wordCount}w)`),
  anchors: results.filter(r => r.action === 'anchor').map(r => `${r.n} ${r.chapter}`),
  failures: results.filter(r => r.action === 'written' && !r.written).map(r => `${r.n} ${r.chapter}`),
  sourcesFailed: results.flatMap(r => (r.sourcesFailed || []).map(u => `${r.n}: ${u}`)),
  reviewNotes: results.filter(r => r.notes).map(r => `${r.n} ${r.chapter}: ${r.notes}`),
}
