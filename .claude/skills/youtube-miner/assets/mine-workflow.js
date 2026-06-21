// youtube-miner engine. Parameterized via Workflow `args`. Returns { report, picker, stats }.
// args: {
//   channel: "@handle" | "UC..." | url   (required)
//   since:   ISO string | null            (null = all-time)
//   today:   "YYYY-MM-DD"                  (for labels; scripts can't call Date.now())
//   goal:    string                        (what kind of ideas to mine)
//   mineCap: int (default 80)
//   relevanceBar: number (default 0.5)
//   useComments: bool (default true)
//   curriculumHint: string | null          (e.g. "Use mcp__..._search_videos to add a 'Relates to' note")
// }
export const meta = {
  name: 'youtube-miner',
  description: 'Mine a YouTube creator catalogue for source-traceable ideas + audience demand',
  phases: [
    { title: 'Discover', detail: 'list the channel videos in the window' },
    { title: 'Triage', detail: 'score relevance to the goal (haiku)' },
    { title: 'Mine', detail: 'transcript + sources + comments (sonnet)' },
    { title: 'Synthesize', detail: 'rank, write report + picker (opus)' },
  ],
}

const A = args || {}
const CHANNEL = A.channel
const SINCE = A.since || null
const TODAY = A.today || 'today'
const GOAL = A.goal || 'reusable content ideas, biased toward insights that trace to an original blog/paper/tweet the creator was reacting to'
const MINE_CAP = A.mineCap || 80
const BAR = (typeof A.relevanceBar === 'number') ? A.relevanceBar : 0.5
const USE_COMMENTS = A.useComments !== false
const CURRIC = A.curriculumHint || null

if (!CHANNEL) {
  return { report: '# youtube-miner\n\nNo `channel` provided in args. Pass a handle, channel id, or URL.', picker: { sections: [] }, stats: {} }
}

const VID_FIELDS = `videoId, title, url (https://www.youtube.com/watch?v=ID), publishDate, and viewCount + description if present (never invent them)`

const DISCOVERY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['totalFound', 'completeCoverage', 'coverageNote', 'videos'],
  properties: {
    totalFound: { type: 'integer' },
    completeCoverage: { type: 'boolean' },
    coverageNote: { type: 'string' },
    videos: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      required: ['videoId', 'title', 'url', 'publishDate'],
      properties: {
        videoId: { type: 'string' }, title: { type: 'string' }, url: { type: 'string' },
        publishDate: { type: 'string' }, viewCount: { type: 'integer' }, description: { type: 'string' },
      } } },
  },
}

const TRIAGE_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['scored'],
  properties: { scored: { type: 'array', items: {
    type: 'object', additionalProperties: false, required: ['videoId', 'relevance', 'reason'],
    properties: { videoId: { type: 'string' }, relevance: { type: 'number' }, reason: { type: 'string' }, angle: { type: 'string' } } } } },
}

const MINE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['videoId', 'title', 'url', 'insights'],
  properties: {
    videoId: { type: 'string' }, title: { type: 'string' }, url: { type: 'string' },
    transcriptFound: { type: 'boolean' },
    audienceSignals: { type: 'array', items: { type: 'string' } },
    insights: { type: 'array', items: {
      type: 'object', additionalProperties: false,
      required: ['title', 'insight', 'noveltyScore'],
      properties: {
        title: { type: 'string' }, insight: { type: 'string' },
        originalSourceName: { type: 'string' }, originalSourceUrl: { type: 'string' },
        audienceAsk: { type: 'string' }, relatesTo: { type: 'string' },
        videoPotential: { type: 'string' }, suggestedTitle: { type: 'string' },
        noveltyScore: { type: 'number' }, evidenceQuote: { type: 'string' },
      } } },
  },
}

const SYNTH_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['reportMarkdown', 'picker'],
  properties: {
    reportMarkdown: { type: 'string' },
    picker: { type: 'object', additionalProperties: false, required: ['title', 'subtitle', 'sections'],
      properties: {
        title: { type: 'string' }, subtitle: { type: 'string' },
        sections: { type: 'array', items: {
          type: 'object', additionalProperties: false, required: ['name', 'items'],
          properties: { name: { type: 'string' }, items: { type: 'array', items: {
            type: 'object', additionalProperties: false, required: ['label', 'title', 'desc'],
            properties: {
              label: { type: 'string' }, title: { type: 'string' }, desc: { type: 'string' },
              tags: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['text'], properties: { text: { type: 'string' }, kind: { type: 'string' } } } },
              links: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['text', 'url'], properties: { text: { type: 'string' }, url: { type: 'string' }, kind: { type: 'string' } } } },
            } } } } } },
      } },
  },
}

phase('Discover')
const disc = await agent(
  `Enumerate a YouTube channel's videos.

CHANNEL: ${CHANNEL}
WINDOW: ${SINCE ? 'published on or after ' + SINCE : 'ALL TIME (no date floor)'} up to ${TODAY}.

TOOLS: ToolSearch select:mcp__claude_ai_VidTempla__list_videos,mcp__claude_ai_VidTempla__search_youtube then use them.
PREFERRED: list_videos({ channelId: "${CHANNEL}", sort: "publishedAt:desc", limit: 100 }) and paginate with the returned cursor until you pass the window floor or run out. list_videos works for public unowned channels and costs no search quota.
FALLBACK only if list_videos fails: search_youtube with filterChannelId, type=video, sort=date, maxResults=50${SINCE ? ', publishedAfter=' + SINCE : ''}, paginate via pageToken; dedupe by videoId.

Collect for each video: ${VID_FIELDS}. Be honest in coverageNote about whether you reached the natural end of the window or hit an API ceiling, and whether view counts were available. Only return videos you actually retrieved.`,
  { schema: DISCOVERY_SCHEMA, label: 'discover' }
)

const videos = (disc && disc.videos ? disc.videos : []).filter(v => v && v.videoId)
log(`Discovered ${videos.length} videos. Coverage: ${disc && disc.coverageNote ? disc.coverageNote : 'n/a'}`)
if (!videos.length) {
  return { report: '# youtube-miner\n\nDiscovery returned no videos. Check the channel handle/id or the tooling.', picker: { sections: [] }, stats: { discovered: 0 } }
}

phase('Triage')
const CH = 40
const chunks = []
for (let i = 0; i < videos.length; i += CH) chunks.push(videos.slice(i, i + CH))
const triaged = (await parallel(chunks.map((c, idx) => () =>
  agent(
    `Score each video for relevance to this goal: "${GOAL}".
Rate relevance 0..1 (1 = almost certainly contains a mineable insight for this goal; 0 = off-topic). One-line reason, and a one-line angle if relevant.
Videos: ${JSON.stringify(c.map(v => ({ videoId: v.videoId, title: v.title, description: (v.description || '').slice(0, 300), publishDate: v.publishDate })))}
Score every videoId.`,
    { schema: TRIAGE_SCHEMA, phase: 'Triage', label: `triage:${idx}`, model: 'haiku', effort: 'low' }
  )
))).filter(Boolean).flatMap(r => r.scored || [])

const byId = new Map(videos.map(v => [v.videoId, v]))
const ranked = triaged
  .filter(t => t && byId.has(t.videoId) && typeof t.relevance === 'number' && t.relevance >= BAR)
  .sort((a, b) => (b.relevance - a.relevance) || String(byId.get(b.videoId).publishDate).localeCompare(String(byId.get(a.videoId).publishDate)))
const seen = new Set(), kept = []
for (const t of ranked) {
  if (seen.has(t.videoId)) continue
  seen.add(t.videoId)
  kept.push({ ...byId.get(t.videoId), relevance: t.relevance, angle: t.angle })
  if (kept.length >= MINE_CAP) break
}
const aboveBar = new Set(ranked.map(r => r.videoId)).size
const beyondCap = Math.max(0, aboveBar - kept.length)
log(`Triage: ${triaged.length} scored, ${aboveBar} above bar (${BAR}). Mining top ${kept.length} (cap ${MINE_CAP}). ${beyondCap} relevant videos NOT deep-mined (metadata only).`)

phase('Mine')
const mined = (await parallel(kept.map(v => () =>
  agent(
    `Mine ONE video for ideas matching this goal: "${GOAL}".

VIDEO: "${v.title}"  URL: ${v.url}  videoId: ${v.videoId}

TOOLS: ToolSearch select:mcp__claude_ai_Supadata__supadata_transcript,mcp__claude_ai_Supadata__supadata_metadata${USE_COMMENTS ? ',mcp__claude_ai_VidTempla__list_comment_threads' : ''}
1. supadata_metadata(url) - capture the description, especially any "SOURCES"/"LINKS" block (the original blog/paper/tweet the creator reacted to).
2. supadata_transcript(url, text:true) - the content. If it returns a jobId, set transcriptFound=false and rely on description + comments.
${USE_COMMENTS ? '3. list_comment_threads({ videoId: "' + v.videoId + '", order: "relevance", maxResults: 60 }) - read for explicit requests ("please make a video on X"), confusion, disagreement, and links commenters share. Distill 1-4 short audienceSignals (what the audience wants / struggles with here).' : ''}
${CURRIC ? '4. ' + CURRIC : ''}

EXTRACT the 1-3 most novel, non-obvious insights for the goal. Bias HARD toward insights that trace to an EXTERNAL primary source (capture originalSourceName + originalSourceUrl from the SOURCES block or transcript). For each insight also set: audienceAsk (what comments show people want here, if any), relatesTo (how it extends/contrasts existing work, if a curriculum was checked), videoPotential, suggestedTitle, noveltyScore 0..1, evidenceQuote.

Be selective; quality over quantity. If nothing is genuinely insightful for the goal, return insights:[]. Never invent sources, quotes, or links.`,
    { schema: MINE_SCHEMA, phase: 'Mine', label: `mine:${v.videoId}`, model: 'sonnet' }
  )
))).filter(Boolean)

const allInsights = mined.flatMap(m => (m.insights || []).map(i => ({ ...i, videoTitle: m.title, videoUrl: m.url })))
const allSignals = mined.flatMap(m => (m.audienceSignals || []).map(s => ({ signal: s, videoTitle: m.title, videoUrl: m.url })))
log(`Mined ${mined.length} videos -> ${allInsights.length} insights, ${allSignals.length} audience signals`)

phase('Synthesize')
const stats = { discovered: videos.length, aboveBar, mined: mined.length, beyondCap, insights: allInsights.length, signals: allSignals.length, coverageNote: disc.coverageNote || '' }

const synth = await agent(
  `Write a ranked idea report AND a picker object from mined YouTube insights.

GOAL: ${GOAL}
CHANNEL: ${CHANNEL}   WINDOW: ${SINCE ? 'since ' + SINCE : 'all time'}   DATE: ${TODAY}

INSIGHTS (JSON): ${JSON.stringify(allInsights)}
AUDIENCE SIGNALS (JSON): ${JSON.stringify(allSignals)}
STATS: ${JSON.stringify(stats)}

reportMarkdown: follow the structure in the skill's references/report-format.md - ## Summary, ## Top ideas (ranked, each with bold suggested title, insight, original source link, "Audience is asking for", "Relates to", and the creator's video link), ## What the audience keeps asking for (synthesize the audience signals), ## Recurring themes, ## Coverage and caveats (use the stats; be honest about the ${beyondCap} videos not deep-mined and that ranking is novelty + source-traceability, not view data). NO H1. NO em dashes or en dashes anywhere (use commas, colons, or 'to').

picker: { title, subtitle (one line with the scan stats), sections: [...] }. Put the strongest ideas in a "Top ideas" section and lighter ones in "Notable mentions". Each item: label (e.g. "#1"), title (the suggested video title), desc (1-2 lines), tags (e.g. [{text:"top",kind:"hot"}], use kind:"seq" for sequels), links (the original source with kind:"src" and the creator video with kind:"yt"). Merge duplicates. Rank by novelty + clean source-traceability.

Dedupe near-identical insights. Only include sources you were actually given.`,
  { schema: SYNTH_SCHEMA, phase: 'Synthesize', label: 'synthesize' }
)

return { report: synth.reportMarkdown, picker: synth.picker, stats }
