// X Thread Miner — outlier mining workflow.
// Reads anchor JSONs in <args.dataDir>/data/, fans out one extraction agent per
// anchor to find non-obvious ideas, adversarially verifies each candidate (the
// default verdict is "rejected" unless the verifier is confident it's genuinely
// outlier), then clusters survivors into a themed report.
//
// Required args:
//   - dataDir: absolute path to the directory containing data/ (the fetcher's --out)
// Recommended args:
//   - topic: 1-line description of what the user is researching (e.g. "Loopy AI
//     — designing loops that prompt agents"). Used to seed the outlier criteria.
//   - consensusThesis: the obvious take to filter OUT as non-outlier. If absent,
//     the discovery agent infers it from the anchor texts.

export const meta = {
  name: 'x-thread-outlier-mine',
  description: 'Mine tweet engagement for outlier/non-obvious ideas. Discover anchors → extract per anchor → adversarially verify → cluster into themed report.',
  phases: [
    { title: 'Discover', detail: 'List anchor files; infer the consensus thesis to filter out' },
    { title: 'Extract',  detail: 'One agent per anchor finds up to 7 outlier ideas' },
    { title: 'Verify',   detail: 'Adversarial skeptic on every candidate; rejects consensus restatements' },
    { title: 'Synthesize', detail: 'Cluster verified outliers into themes and write the report' },
  ],
}

if (!args?.dataDir) {
  throw new Error('args.dataDir is required (absolute path to the directory containing data/)')
}
const dataDir = args.dataDir
const topic = args.topic || 'this topic'
const givenConsensus = args.consensusThesis || ''

const DISCOVERY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    anchors: {
      type: 'array',
      minItems: 1,
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          file: { type: 'string', description: 'relative path under dataDir, e.g. data/author_123.json' },
          author: { type: 'string' },
          anchor_text: { type: 'string', description: 'first ~200 chars of anchor tweet text' },
        },
        required: ['file', 'author', 'anchor_text'],
      },
    },
    consensus_thesis: { type: 'string', description: 'The obvious take on the topic — what extraction agents should reject as non-outlier' },
  },
  required: ['anchors', 'consensus_thesis'],
}

const OUTLIER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    outliers: {
      type: 'array',
      maxItems: 7,
      items: {
        type: 'object',
        additionalProperties: false,
        properties: {
          category: { type: 'string', enum: ['contrarian-thesis', 'novel-use-case', 'sharp-objection', 'mental-model', 'specific-tooling', 'meta-observation'] },
          idea: { type: 'string', description: '1-2 sentence statement of the outlier idea' },
          author: { type: 'string' },
          followers: { type: 'number' },
          quote: { type: 'string', description: 'verbatim or near-verbatim text from the tweet' },
          tweet_id: { type: 'string' },
          source: { type: 'string', enum: ['anchor', 'reply', 'quote', 'deep-reply'] },
          why_outlier: { type: 'string', description: 'why this is non-obvious / not the consensus take' },
        },
        required: ['category', 'idea', 'author', 'quote', 'why_outlier'],
      },
    },
  },
  required: ['outliers'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    is_outlier: { type: 'boolean' },
    confidence: { type: 'number', minimum: 0, maximum: 1 },
    reasoning: { type: 'string' },
    refined_idea: { type: 'string', description: 'optional sharpened 1-sentence version if the idea survives' },
  },
  required: ['is_outlier', 'confidence', 'reasoning'],
}

const REPORT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    headline: {
      type: 'array',
      minItems: 3, maxItems: 5,
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          idea: { type: 'string' },
          author: { type: 'string' },
          quote: { type: 'string' },
          why_it_matters: { type: 'string' },
        },
        required: ['idea', 'author', 'quote', 'why_it_matters'],
      },
    },
    themes: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          name: { type: 'string' },
          one_liner: { type: 'string' },
          supports: {
            type: 'array',
            items: {
              type: 'object', additionalProperties: false,
              properties: { author: { type: 'string' }, quote: { type: 'string' }, idea: { type: 'string' } },
              required: ['author', 'quote', 'idea'],
            },
          },
        },
        required: ['name', 'one_liner', 'supports'],
      },
    },
    mental_models: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: { framing: { type: 'string' }, author: { type: 'string' } },
        required: ['framing', 'author'],
      },
    },
    sharpest_objections: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: { objection: { type: 'string' }, author: { type: 'string' }, quote: { type: 'string' } },
        required: ['objection', 'author', 'quote'],
      },
    },
    specific_tooling: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: { name: { type: 'string' }, what_it_is: { type: 'string' }, author: { type: 'string' } },
        required: ['name', 'what_it_is', 'author'],
      },
    },
  },
  required: ['headline', 'themes', 'mental_models', 'sharpest_objections', 'specific_tooling'],
}

// ── Phase 1: Discover anchors and consensus thesis ──────────────────────────
phase('Discover')

const discovery = await agent(
`You are starting an outlier-mining run for the topic: "${topic}".

TASKS:
1. List all anchor JSON files in ${dataDir}/data/ (exclude the quote_replies/ subdirectory and any other subdirectories). Use Bash: \`ls ${dataDir}/data/*.json\`.
2. For each file, Read just the "anchor" field (top of the JSON, ~30 lines is enough) to capture: file (relative path like "data/foo_123.json"), author (screen_name), anchor_text (first ~200 chars).
3. State the CONSENSUS THESIS — the obvious, widely-agreed take about ${topic} that should be FILTERED OUT during outlier extraction. Anything that just restates this is NOT an outlier.
   ${givenConsensus ? `The user has hinted: "${givenConsensus}". Refine or use as-is.` : 'Infer the consensus thesis from the anchor texts you just read.'}
   The consensus thesis should be specific and crisp — 1-2 sentences. Extraction agents will use it as the rejection criterion.

Return per the schema.`,
  { schema: DISCOVERY_SCHEMA, phase: 'Discover', label: 'discover-anchors' }
)

log(`Discovered ${discovery.anchors.length} anchors. Consensus: "${discovery.consensus_thesis}"`)

// ── Phase 2 + 3: Extract per anchor → Verify each candidate (pipelined) ─────
const EXTRACT_PROMPT = (a) => `You are mining a single anchor tweet plus all of its replies and quote tweets (and the deep layer — replies under top quote tweets) for OUTLIER ideas about: "${topic}".

Anchor: @${a.author}
Anchor text: "${a.anchor_text}"
Data file: ${dataDir}/${a.file}
Deep layer (optional): ${dataDir}/data/quote_replies/ — each file in there has shape { quote: {...}, replies: [...] } where the quote's tweet_id matches one of the quote tweets in this anchor's data.

WHAT TO READ:
Use your Read tool on the data file. JSON shape: { anchor: {...}, replies: [...], quotes: [...] }. Each tweet record has: tweet_id, screen_name, name, followers, verified, text, favorites, views, in_reply_to. Read all of it — that's why you got this slice instead of the whole dataset.

CONSENSUS THESIS (REJECT anything that just restates this):
"${discovery.consensus_thesis}"

WHAT IS AN OUTLIER:
The user already knows the consensus. They want the NON-OBVIOUS — counter-theses, specific use cases, sharp objections, novel framings, concrete tooling, second-order observations.

Gold examples:
- Contrarian thesis: a take that directly pushes back on the consensus with specifics (cost numbers, real failure modes, alternative architectures)
- Novel use case: specific and non-generic (e.g. "loop monitoring arxiv papers for new transformer methods" — names a concrete domain)
- Sharp objection: steelmanned criticism, not vague pushback ("a loop without memory starts from zero every run; a loop with memory remembers every mistake and repeats it" — second-order failure mode)
- Mental model: a one-line framing that crystallizes the idea ("agents as state machines, not loops")
- Specific tooling: named files, slash commands, patterns (VISION.md, /goal, ralph loops, XState, etc.)
- Meta observation: pattern that only emerges across many tweets

REJECT:
- Generic enthusiasm ("agreed!", "this is huge", "facts")
- Restating the consensus
- Pure self-promo
- Vague prior-art ("I've been doing this for months" with no specifics)
- Non-English-but-actually-just-the-thesis-translated — translate first, then filter by substance

WEIGHTS:
- Quote tweets > replies (people broadcast takes in quotes, react in replies)
- A sharp 200-follower take beats a vague 200K-follower one — favor specificity over reach
- Translate non-English tweets in your head; some of the sharpest takes are JP/CN/KR

OUTPUT:
Return up to 7 of the BEST outliers from this anchor. Quote verbatim or near-verbatim. Fewer high-quality > many mediocre. If this anchor has nothing genuinely outlier, return an empty array.`

const VERIFY_PROMPT = (o) => `You are an adversarial skeptic. Try to REFUTE this claimed outlier insight.

CONSENSUS THESIS (anything restating this is NOT an outlier):
"${discovery.consensus_thesis}"

CLAIM:
- Idea: ${o.idea}
- Category: ${o.category}
- Author: @${o.author} (${o.followers || '?'} followers)
- Quote: "${o.quote}"
- Why claimed outlier: ${o.why_outlier}

CHECK:
1. Is the idea actually non-obvious vs the consensus, or is it just rephrasing?
2. Is it specific enough to cite in research/writing, or too vague to be useful?
3. Is the quote faithful, or does it sound fabricated?
4. Would a thoughtful researcher say "huh, I hadn't thought of that"? If no → reject.
5. Is the why_outlier reasoning sound, or hand-wavy?

DEFAULT TO is_outlier=false unless the idea would genuinely surprise someone who already knows the consensus thesis. Be ruthless — better to drop a borderline one than to keep noise.

If it survives, optionally provide a sharpened 1-sentence refined_idea.`

phase('Extract')

const extracted = await pipeline(
  discovery.anchors,
  // Stage 1: extract outliers from one anchor
  async (a) => agent(EXTRACT_PROMPT(a), {
    label: `extract:${a.author}`,
    phase: 'Extract',
    schema: OUTLIER_SCHEMA,
  }),
  // Stage 2: adversarially verify each candidate (parallel within anchor)
  async (extract, a) => {
    const outliers = extract?.outliers || []
    if (!outliers.length) return []
    return parallel(outliers.map(o => () =>
      agent(VERIFY_PROMPT(o), {
        label: `verify:${o.author || '?'}`,
        phase: 'Verify',
        schema: VERDICT_SCHEMA,
      }).then(v => ({ ...o, anchor: a.author, verdict: v }))
    ))
  }
)

const allCandidates = extracted.flat().filter(Boolean)
const survivors = allCandidates.filter(o => o.verdict?.is_outlier && (o.verdict?.confidence ?? 0) >= 0.6)

log(`${allCandidates.length} candidates → ${survivors.length} survived adversarial verification (conf ≥ 0.6)`)

// ── Phase 4: Synthesize ─────────────────────────────────────────────────────
phase('Synthesize')

const SYNTH_PROMPT = `You have ${survivors.length} verified outlier ideas about "${topic}", mined and adversarially verified from tweet engagement across ${discovery.anchors.length} anchor tweets.

CONSENSUS THESIS (which the audience already knows):
"${discovery.consensus_thesis}"

THE VERIFIED OUTLIERS (JSON):
${JSON.stringify(survivors, null, 2)}

YOUR JOB:
Cluster these into a tight report. The audience already knows the consensus — they need the outlier insights, organized.

- Headline (3-5 items): the most important outlier ideas, ones that should anchor sections of any writeup/video about ${topic}.
- Themes (5-10 clusters): group related outliers under a named theme. Name themes with specific, memorable framings. Each theme gets 2-5 supporting outliers with quotes.
- Mental models: 1-line framings worth stealing verbatim.
- Sharpest objections: the steelmanned skeptic case — what pushes back on the consensus thesis.
- Specific tooling: concrete things named (file names, slash commands, patterns, libraries).

If multiple outliers are near-duplicates (e.g., 3 people independently said the same thing), surface that convergence as ONE item in the relevant theme — cross-anchor convergence is itself a signal worth flagging in the one_liner. Don't list duplicates.

Output structured JSON per the schema.`

const report = await agent(SYNTH_PROMPT, {
  label: 'cluster-and-write-report',
  phase: 'Synthesize',
  schema: REPORT_SCHEMA,
})

return {
  topic,
  consensus_thesis: discovery.consensus_thesis,
  stats: {
    anchors: discovery.anchors.length,
    candidates_extracted: allCandidates.length,
    candidates_verified: survivors.length,
    candidates_rejected: allCandidates.length - survivors.length,
  },
  report,
  verified_outliers: survivors,
  all_candidates: allCandidates,
}
