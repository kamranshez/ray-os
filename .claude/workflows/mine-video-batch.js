// Mine a batch of YouTube videos for Anki sentence cards, one agent per video.
//
// Caller passes args = { picks: [{id, title, url, dur_s}, ...] }
// Each agent runs the full video-mode sentence-mining pipeline from the
// sentence-mining skill, returns a per-video result.

export const meta = {
  name: 'mine-video-batch',
  description: 'Fan out per-video sentence-mining agents over a list of YouTube videos',
  phases: [{ title: 'Mine', detail: 'one agent per video; download → transcribe → analyze → curate → explain → media → push' }],
}

// Picks come from args.picks (array). For convenience the workflow also accepts
// args.picksFile (path to a JSON file with {picks: [...]}); the file is loaded
// via the agent() tool so the workflow script doesn't need fs access.
// args may arrive as an object or as a JSON string — normalise.
const parsedArgs = typeof args === 'string' ? JSON.parse(args) : (args || {})
log(`args type: ${typeof args}, picksFile: ${parsedArgs.picksFile}, picks count: ${Array.isArray(parsedArgs.picks) ? parsedArgs.picks.length : 'n/a'}`)
let picks = Array.isArray(parsedArgs.picks) ? parsedArgs.picks : []
if (!picks.length && parsedArgs.picksFile) {
  log(`Loading picks from ${parsedArgs.picksFile}`)
  const loaded = await agent(
    `Read the file ${parsedArgs.picksFile}, parse the JSON, and return its "picks" array verbatim. The file contains {"picks": [...]} where each pick has id, title, url, dur_s, channel, unique_unknown.`,
    {
      label: 'load-picks',
      schema: {
        type: 'object',
        required: ['picks'],
        properties: {
          picks: {
            type: 'array',
            items: {
              type: 'object',
              required: ['id', 'title', 'url'],
              properties: {
                id: { type: 'string' },
                title: { type: 'string' },
                url: { type: 'string' },
                dur_s: { type: 'integer' },
                channel: { type: 'string' },
                unique_unknown: { type: 'integer' },
              },
            },
          },
        },
      },
    },
  )
  picks = loaded?.picks || []
}
if (!picks.length) {
  log('No picks provided (args.picks empty and no args.picksFile) — nothing to do')
  return { mined: 0, results: [] }
}

log(`Mining ${picks.length} videos in parallel`)

phase('Mine')

const SCHEMA = {
  type: 'object',
  required: ['id', 'status'],
  properties: {
    id: { type: 'string' },
    status: { enum: ['pushed', 'no_candidates', 'failed'] },
    pushed_count: { type: 'integer' },
    failed_count: { type: 'integer' },
    candidates_total: { type: 'integer' },
    candidates_after_curation: { type: 'integer' },
    duration_s: { type: 'integer' },
    notes: { type: 'string' },
  },
}

const SKILL_DIR = '/Users/ray/Desktop/ray-os/.claude/skills/sentence-mining'
const WORK_DIR = '/Users/ray/Downloads/sentence-mining'

const results = await parallel(picks.map((p) => () =>
  agent(
    `You are mining a YouTube video for Japanese Anki sentence cards using the sentence-mining skill at ${SKILL_DIR}. Read these references first if needed:
- ${SKILL_DIR}/SKILL.md (the routing entrypoint)
- ${SKILL_DIR}/references/video-mode.md (Steps 1-3 + Step 5)

Video to mine:
- id: ${p.id}
- title: ${p.title}
- url: ${p.url}
- duration: ${p.dur_s || 'unknown'}s
- source_id: youtube-${p.id}

Run the full video-mode pipeline. Important details:

1. **Download** (cd ${WORK_DIR} && yt-dlp -o "%(extractor)s-%(id)s.%(ext)s" --no-playlist "${p.url}")
   - The file lands as youtube-${p.id}.{webm,mp4,mkv}. Set VIDEO_PATH to whichever extension it produced.

2. **Transcribe**:
   python3 ${SKILL_DIR}/scripts/transcribe.py "$VIDEO_PATH" > ${WORK_DIR}/youtube-${p.id}.transcript.json

3. **Step 2.5 — sentence split (INLINE)**: read ${WORK_DIR}/youtube-${p.id}.transcript.json, correct obvious mistranscriptions, split into 3-12s chunks on speaker turns + natural boundaries. Write the sentences[] array back to the same JSON. Follow the rules in references/video-mode.md §"Step 2.5".

4. **Analyze**:
   python3 ${SKILL_DIR}/scripts/analyze.py --transcript ${WORK_DIR}/youtube-${p.id}.transcript.json --source-id "youtube-${p.id}" --source-url "${p.url}" > ${WORK_DIR}/youtube-${p.id}.candidates.json

5. **Step 3.5 — curate (INLINE)**: read candidates.json, drop pop-culture proper nouns, mecab fragments, transcription garbage, trail-off sentences. See SKILL.md §"Step 3.5". Save back.

6. **Step 4 — explanations (INLINE)**: for each remaining candidate, write a Japanese explanation per the prompt in SKILL.md §"Step 4" (250 chars, native-explains-to-13-year-old style, no English). Set candidate.explanation. Save the file as youtube-${p.id}.candidates.json (the same file you've been editing — generate_media expects it).

7. **Generate media**:
   python3 ${SKILL_DIR}/scripts/generate_media.py --video "$VIDEO_PATH" --candidates ${WORK_DIR}/youtube-${p.id}.candidates.json --source-id "youtube-${p.id}" > ${WORK_DIR}/youtube-${p.id}.draft.json

8. **Push**:
   python3 ${SKILL_DIR}/scripts/push.py --draft ${WORK_DIR}/youtube-${p.id}.draft.json
   This already tags each card with source:youtube-${p.id} (push.py was patched to add this).

Cleanup: leave the video, transcript, candidates, and draft JSONs on disk — Ray re-runs occasionally.

If something goes wrong (yt-dlp blocked, transcription empty, all candidates dropped, etc.) return status="failed" or "no_candidates" with a brief notes field. Otherwise return status="pushed" with counts from the push.py JSON output.

Be efficient — don't re-read references you've already read; don't print large transcripts; don't generate explanations in a chatty way.`,
    {
      label: `mine:${p.id}`,
      phase: 'Mine',
      schema: SCHEMA,
      // No worktree isolation — work happens in ~/Downloads/sentence-mining (not in any repo).
      // Per-video source_id-prefixed filenames prevent file collisions.
    }
  )
))

const valid = results.filter(Boolean)
const pushed = valid.filter((r) => r.status === 'pushed')
const empty = valid.filter((r) => r.status === 'no_candidates')
const failed = valid.filter((r) => r.status === 'failed')
const totalCards = pushed.reduce((s, r) => s + (r.pushed_count || 0), 0)

log(`Mined ${pushed.length}/${picks.length} videos, ${totalCards} cards pushed`)
log(`  empty: ${empty.length}, failed: ${failed.length}`)

return {
  picks_total: picks.length,
  videos_pushed: pushed.length,
  videos_empty: empty.length,
  videos_failed: failed.length,
  cards_pushed_total: totalCards,
  results: valid,
}
