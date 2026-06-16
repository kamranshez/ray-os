export const meta = {
  name: 'idea-foundry',
  description: 'Mine 60-150 fresh ideas on a topic via ~20 parallel agents (Exa web search + x-search + pure reasoning), synthesize, render to a self-contained HTML idea bank with selectable cards and a floating copy button.',
  whenToUse: 'When the user wants to brainstorm widely on a topic, project, class, video, product, or any idea-mining task and curate the results later. The idea-foundry skill is the front door; this workflow is the engine.',
  phases: [
    { title: 'Generate' },
    { title: 'Synthesize' },
    { title: 'Render' }
  ]
}

const cfg = args || {}
const TOPIC = cfg.topic || 'agentic coding'
const SLUG = cfg.slug || 'idea-foundry'
const PURPOSE = cfg.purpose || `Ray wants to mine fresh ideas about ${TOPIC}.`
const CONTEXT_BLOCK = cfg.context || PURPOSE
const ALREADY_COVERED = cfg.alreadyCovered || 'No exclusions provided.'
const RECENT_SINCE = cfg.recentDate || '2026-05-24'
const OUTPUT_PATH = cfg.outputPath || `/tmp/${SLUG}-ideas.html`
const X_QUERIES = cfg.xQueries || [
  { key: 'x-topic-general', query: `("${TOPIC}") min_faves:50 lang:en -filter:replies`, desc: `general ${TOPIC} discourse` },
  { key: 'x-topic-leaders', query: `(from:karpathy OR from:simonw OR from:swyx OR from:bcherny0 OR from:sama OR from:dwarkesh_sp) ${TOPIC}`, desc: `thought leaders on ${TOPIC}` }
]
const EXTRA_EXA_ANGLES = cfg.extraExaAngles || []
const EXTRA_REASONING_ANGLES = cfg.extraReasoningAngles || []
const VOICE_NOTE = cfg.voiceNote || 'Direct, plain, no fluff, no Oxford fancy words. Ray talks like a smart practitioner explaining to a peer, not a TED speaker.'

const CONTEXT = `
${CONTEXT_BLOCK}

ALREADY COVERED or OUT OF SCOPE (do NOT regenerate ideas about these):
${ALREADY_COVERED}

The goal of THIS run is FRESH ideas not already covered. Each idea should be concrete and usable, not a vague theme.
`

const IDEA_SCHEMA = {
  type: 'object',
  required: ['ideas'],
  properties: {
    ideas: {
      type: 'array',
      items: {
        type: 'object',
        required: ['title', 'explanation', 'level', 'category', 'angle'],
        properties: {
          title: { type: 'string', description: '4 to 10 word snappy headline, no em or en dashes' },
          explanation: { type: 'string', description: '3 to 5 sentences, no em or en dashes, no fluff' },
          level: { type: 'string', description: 'L0 through L7 if the topic has a level system, otherwise "n/a" or "cross-cutting"' },
          category: { type: 'string' },
          source_urls: { type: 'array', items: { type: 'string' } },
          angle: { type: 'string' }
        }
      }
    }
  }
}

const ANGLES_EXA = [
  { key: 'thought-leaders', prompt: `Search via Exa for what thought leaders in the ${TOPIC} space have written or said in the last 90 days. Pull 8 to 12 fresh ideas.` },
  { key: 'research', prompt: `Search via Exa for 2026 papers on arxiv plus blog posts from major labs / research orgs about ${TOPIC}. Pull 8 to 12 ideas grounded in research.` },
  { key: 'postmortems', prompt: `Search via Exa for production postmortems, incident reports, and "we shipped this and it broke" stories related to ${TOPIC}. Pull 8 to 12 ideas about real-world failure modes.` },
  { key: 'comparisons', prompt: `Search via Exa for comparisons between tools, frameworks, products, or approaches in the ${TOPIC} space in 2026. Pull 8 to 12 ideas about tradeoffs.` },
  { key: 'hn-reddit', prompt: `Search via Exa for HackerNews and Reddit discussions from 2026 about ${TOPIC}. Pull 8 to 12 fresh ideas from the discourse.` },
  { key: 'podcasts', prompt: `Search via Exa for podcast episodes and YouTube videos from 2026 discussing ${TOPIC}. Pull 8 to 12 ideas with episode references where possible.` },
  { key: 'case-studies', prompt: `Search via Exa for specific company case studies related to ${TOPIC}. Pull 8 to 12 concrete ideas with company names, numbers, and specifics.` },
  { key: 'critical-takes', prompt: `Search via Exa for skeptical or critical takes on ${TOPIC} in 2026. Pull 8 to 12 ideas that address the strongest objections.` },
  ...EXTRA_EXA_ANGLES
]

const ANGLES_REASONING = [
  { key: 'economics', prompt: `Generate 8 to 12 ideas about the ECONOMIC implications of ${TOPIC}: business model shifts, who captures value, what gets commoditized, what becomes scarcer, new job categories. Focus on non-obvious ideas.` },
  { key: 'analogies', prompt: `Generate 8 to 12 cross-domain ANALOGIES that illuminate ${TOPIC}: Toyota Production System, military doctrine, the immune system, factory automation history, the printing press, evolutionary biology, jazz ensembles, surgical teams. Each analogy should yield a concrete idea, not just a metaphor.` },
  { key: 'failure-modes', prompt: `Generate 8 to 12 ideas about how things FAIL in non-obvious ways in the ${TOPIC} domain. Each should be a recognizable failure pattern with a clear signature.` },
  { key: 'cross-domain', prompt: `Generate 8 to 12 ideas applying ${TOPIC} concepts OUTSIDE the obvious domain: legal, medical, creative, sales, education, operations, journalism. Each should be concrete.` },
  { key: 'dark-side', prompt: `Generate 8 to 12 ideas about the DARK SIDE and ETHICS of ${TOPIC}: surveillance, dependency, deskilling, asymmetric impact, atrophy of judgment. Honest, not hand-wavy.` },
  { key: 'first-principles', prompt: `Generate 8 to 12 ideas about ${TOPIC} reasoning from FIRST PRINCIPLES: what would you build if there were no incumbents, what does the underlying physics or math allow, what assumptions does everyone make that are actually wrong.` },
  { key: 'anti-patterns', prompt: `Generate 8 to 12 ANTI-PATTERNS in the ${TOPIC} domain. Each with a recognizable signature, why it traps people, and what to do instead.` },
  { key: 'provocations', prompt: `Generate 8 to 12 COUNTER-INTUITIVE PROVOCATIONS about ${TOPIC}: claims most people will initially reject but that are defensible with one sentence of reasoning.` },
  ...EXTRA_REASONING_ANGLES
]

phase('Generate')

const exaThunks = ANGLES_EXA.map(a => () => agent(
  `${CONTEXT}\n\nYou are an idea-generation agent for the angle: "${a.key}".\n\nYour task: ${a.prompt}\n\nUse Exa MCP for research. Load tools first via ToolSearch with query: select:mcp__claude_ai_Exa__web_search_exa,mcp__claude_ai_Exa__web_fetch_exa (try also: select:mcp__claude_ai_Exa_Advanced__web_search_exa,mcp__claude_ai_Exa_Advanced__web_fetch_exa)\n\nRun 3 to 6 searches with varied query phrasings. Fetch the most promising 4 to 8 results to read body text. Then synthesize 8 to 12 ideas.\n\nEach idea: snappy title (4 to 10 words, no dashes), explanation (3 to 5 sentences, NO em or en dashes), level (L0 to L7 or "n/a" or "cross-cutting"), category (one of: economic, technical, pedagogical, ethical, cross-domain, failure-mode, production, philosophical, organizational, discourse), source_urls (the URLs you actually fetched or referenced), angle="${a.key}".\n\nReturn via the schema. Be specific and fresh; do not regenerate anything in the "already covered" list above.`,
  { label: `exa:${a.key}`, schema: IDEA_SCHEMA, phase: 'Generate' }
))

const xThunks = X_QUERIES.map(a => () => agent(
  `${CONTEXT}\n\nYou are an idea-generation agent for the X-search angle: "${a.key}" (${a.desc}).\n\nRun the x-search skill via Bash:\n\n  python3 /Users/ray/.claude/skills/x-search/scripts/search_x.py --query '${a.query}' --search-type Top --since ${RECENT_SINCE} --max-pages 5 --top-n 50 --out /tmp/x-search-${SLUG}-${a.key}\n\nIf the script exits with non-zero code, return ideas: []. If /tmp/x-search-${SLUG}-${a.key}/surfaced.md contains "_No results._" or is essentially empty, return ideas: []. If meta.json has low_signal=true, proceed but be cautious.\n\nOtherwise Read surfaced.md to see the ranked tweets. Extract 6 to 10 FRESH ideas informed by what people on X are actually saying. The ideas should be triggered by the tweets but go beyond them (a tweet is a seed, not the whole idea).\n\nEach idea: title (4-10 words, no dashes), 3-5 sentence explanation (NO em or en dashes), level, category, source_urls=[the tweet URLs that inspired this idea], angle="${a.key}".\n\nReturn via the schema.`,
  { label: `x:${a.key}`, schema: IDEA_SCHEMA, phase: 'Generate' }
))

const reasoningThunks = ANGLES_REASONING.map(a => () => agent(
  `${CONTEXT}\n\nYou are an idea-generation agent for the REASONING angle: "${a.key}".\n\n${a.prompt}\n\nNo web search needed. Think hard. Be original. Avoid restating the "already covered" concepts above.\n\nEach idea: snappy title (4 to 10 words, no dashes), explanation (3 to 5 sentences, NO em or en dashes, ${VOICE_NOTE}), level (L0 to L7 or "n/a" or "cross-cutting"), category, source_urls=[], angle="${a.key}".\n\nReturn via the schema.`,
  { label: `reason:${a.key}`, schema: IDEA_SCHEMA, phase: 'Generate' }
))

const allResults = await parallel([...exaThunks, ...xThunks, ...reasoningThunks])

const surviving = allResults.filter(Boolean)
const allIdeas = surviving.flatMap(r => Array.isArray(r.ideas) ? r.ideas : [])
log(`Raw ideas: ${allIdeas.length} from ${surviving.length}/${allResults.length} agents`)

phase('Synthesize')

const SYNTHESIS_SCHEMA = {
  type: 'object',
  required: ['ideas'],
  properties: {
    ideas: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'title', 'explanation', 'category', 'level', 'novelty', 'origin_angles'],
        properties: {
          id: { type: 'string', description: 'short stable slug like econ-001, fail-014' },
          title: { type: 'string' },
          explanation: { type: 'string' },
          category: { type: 'string', description: 'one of: economic, technical, pedagogical, ethical, cross-domain, failure-mode, production, philosophical, organizational, discourse' },
          level: { type: 'string' },
          novelty: { type: 'string', enum: ['low', 'medium', 'high'] },
          origin_angles: { type: 'array', items: { type: 'string' } },
          sources: { type: 'array', items: { type: 'string' } }
        }
      }
    }
  }
}

const rawJson = JSON.stringify(allIdeas)
const synthInput = rawJson.length > 250000 ? rawJson.slice(0, 250000) + ']' : rawJson

const synthesized = await agent(
  `${CONTEXT}\n\nYou are the SYNTHESIS agent. ${allIdeas.length} raw ideas were generated across ${surviving.length} angle agents. Your job:\n\n1. DEDUP aggressively. Merge near-duplicates into one polished idea. When merging, preserve all origin_angles and all sources.\n2. FILTER against the "already covered" list. Drop anything that meaningfully overlaps.\n3. RANK by (novelty + usefulness + surprise). Drop the bottom third. Keep the ideas a smart practitioner would find non-obvious.\n4. POLISH each survivor to a clean 3 to 5 sentence explanation. Voice: ${VOICE_NOTE}. NO em-dashes or en-dashes anywhere. Use regular hyphens, periods, or " to " instead.\n5. CATEGORIZE each: economic, technical, pedagogical, ethical, cross-domain, failure-mode, production, philosophical, organizational, discourse.\n6. Assign level (L0 through L7, or "n/a", or "cross-cutting").\n7. Tag novelty: low / medium / high. High means the user probably has not encountered this framing before.\n8. Preserve origin_angles (array of angle keys) and sources (URLs from the raw ideas).\n9. Give each a short stable id like "econ-001", "fail-014".\n\nTarget: 60 to 150 final ideas. If raw pool is small, lean low; if rich, lean high. Quality beats quantity.\n\nRAW IDEAS JSON:\n${synthInput}\n\nReturn via the schema.`,
  { label: 'synthesize', schema: SYNTHESIS_SCHEMA, phase: 'Synthesize' }
)

const finalIdeas = synthesized?.ideas || []
log(`Synthesized: ${finalIdeas.length} polished ideas`)

phase('Render')

const ideasJson = JSON.stringify(finalIdeas)

await agent(
  `You are the RENDER agent. Write a single self-contained HTML file at ${OUTPUT_PATH} showing ${finalIdeas.length} idea cards for "${TOPIC}".\n\nEmbed this JSON as a const IDEAS in a <script> tag (do not modify the data):\n\n${ideasJson}\n\nHARD REQUIREMENTS:\n- Page title: "Idea Bank: ${TOPIC}"\n- Dark theme: body background #0a0a0a, text #e8e8e8, accent amber #f59e0b, card background #161616, card border #262626\n- Sticky filter bar at top with: category chips (toggleable, multi-select, OR-within-group), level chips (L0 L1 L2 L3 L4 L5 L6 L7 cross-cutting n/a, hide empty ones), search input (case-insensitive substring filter on title + explanation), novelty chips (low / medium / high). When category and level filters are both active, AND across the groups.\n- Stats line under filter bar: "X/Y ideas, Z selected"\n- Responsive grid: 1 col under 700px, 2 col 700-1100px, 3 col over 1100px, gap 16px\n- Each card shows: title (font weight 600), explanation paragraph, badges row (level pill, category pill, novelty pill), tiny sources line with anchor links opening in new tab, tiny angles line\n- Click anywhere on card body to TOGGLE SELECTION. Selected: 2px amber border + filled amber circle with white check in top-right corner. Unselected: hollow grey circle in same position. cursor: pointer.\n- Source link clicks must NOT toggle selection (stopPropagation).\n- FLOATING button fixed top-right (position: fixed, top: 16px, right: 16px, z-index: 100): "Copy selected (N)" updating live. Amber background #f59e0b with black text when N>0, dimmed (#262626 bg, #666 text, not clickable) when N=0.\n- On click: copy markdown blob via navigator.clipboard.writeText with execCommand fallback. Show toast "Copied N ideas" at bottom for 2 seconds.\n- Markdown blob per selected idea:\\n  ## <title>\\n\\n  <explanation>\\n\\n  _Level: <level> | Category: <category> | Novelty: <novelty>_\\n\\n  Sources:\\n  - <url1>\\n\\n  ---\\n\\n  (Omit Sources section if empty.)\n- Keyboard: Cmd+Shift+C (and Ctrl+Shift+C) triggers copy. Esc clears selection.\n- "Clear selection" link inline with count when N>0.\n- ZERO em-dashes (U+2014) or en-dashes (U+2013) anywhere in HTML, JS, CSS, or embedded text. Replace any in the data with " to " or " ". Grep before reporting done.\n- No external CDN, no external fonts (use system-ui font stack), fully self-contained.\n- Use Write tool.\n\nAfter writing, Bash: grep -c $'\\u2014\\|\\u2013' ${OUTPUT_PATH} (should be 0) and wc -c ${OUTPUT_PATH}. Report both.`,
  { label: 'render-html', phase: 'Render' }
)

return { count: finalIdeas.length, path: OUTPUT_PATH, slug: SLUG, topic: TOPIC }
