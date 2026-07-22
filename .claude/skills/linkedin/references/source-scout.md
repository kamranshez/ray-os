# Source scout

Sweep a fixed set of data sources (GitHub trending, Hacker News, model/vendor launch news,
conference talks, viral X/Reddit threads), pick the 2-3 items most worth a LinkedIn post in Ray's
niche, draft each one in the **Stanislav template**, and post the result to Slack
**#li-source-scout**.

This file owns **sourcing**: which lanes to sweep, what to pick, how to deliver. It does not own
writing. The skeleton lives in `viral-playbook.md` and the gate lives in `post-gate.md`; read them
on every run rather than reproducing them here. That separation is deliberate -- when Ray changes
the template he changes it in one place and every caller picks it up for free.

## Two callers, one file

**Cloud (unattended).** A cron routine runs this daily via the stub at
`routines/linkedin-source-scout.md`. Zero prior context, no local machine, nobody to ask. See
`routines/CLAUDE.md` for the cloud contract and the Slack bot-token idiom.

**Interactive.** The `linkedin` skill runs this same file when Ray asks for a sweep. He is present,
so he can be asked things, and the local machine is available.

The sourcing steps below are identical for both. Only the environment section and the delivery
section branch, and each says which caller it applies to.

---

## Inputs (read at the start of every run, in this order)

1. `viral-playbook.md` -- the canonical Stanislav skeleton, the variation axes, and the house rules.
   Every draft must follow it.
2. `post-gate.md` -- the pre-post checklist. Run it on every draft before delivering. Drafts from
   this scout and drafts Ray writes by hand come out the same shape because they pass the same file.
3. `analysis/2026-07-stanislav-beliaev-source-system.md` -- the source rationale: which lanes
   Stanislav mines and why the format works. Read for curation judgement, not for structure. His
   full raw feed is alongside it at `analysis/2026-07-stanislav-beliaev-feed.md`; read a few posts
   only if drafting feels off-template.
4. Recent history of Slack **#li-source-scout** (last 14 days, via Slack MCP `slack_read_channel`)
   -- the dedupe ledger. Any repo/model/story already surfaced there is OFF the table unless
   something major changed (e.g. 2x star growth, a big new release). Every run posts to that
   channel, interactive ones included, which is what keeps this ledger honest.

## Niche filter

Ray's audience: engineers and technical founders into **agentic coding** -- Claude Code, Codex,
Cursor, MCP, agent memory/context tooling, AI dev workflows. Rank candidates by fit to that niche
first, raw virality second. One clearly off-niche but wildly viral item (a LibrePods-style story) is
allowed per week at most.

### Optional focus (interactive only)

Ray may narrow a sweep: "scout me something on MCP", "just Hacker News today". Apply the focus as a
**filter on candidates or lanes**, and change nothing else -- same lanes where they still apply,
same ranking, same gate, same delivery. A focused sweep still aims for 2-3 picks; if the focus is
narrow enough that only one candidate clears the bar, deliver one and say so rather than padding.
With no focus given, run the full 4-lane sweep exactly as the cloud does.

Funnel line: every draft ends with
`P.S. I teach engineers to code with AI agents - 350+ videos at agenticcoding.school`
(exact wording, copied verbatim from viral-playbook.md item 8: SINGLE hyphen. Ray may edit; always
include the slot).

---

## Environment

**Cloud.** No local machine. Data comes from `curl` (Bash) and the **Exa MCP** (attached). Slack:
bot-token `curl` for posting per `routines/CLAUDE.md`; Slack MCP for reading channel history
(dedupe) and for creating #li-source-scout if it does not exist yet. If the system says "Continue
from where you left off", resume until the Slack post is out.

**Interactive.** Same `curl` and Exa sourcing. Slack posting can go through the Slack MCP or the
`slackbot-message` skill, whichever is already available; the bot-token idiom is a cloud detail, not
a requirement.

**Both.** If a source is unreachable after one retry, skip it, note it in the delivery, keep going.
Never abort the whole run over one source.

## Source lanes (fan out one Task subagent per lane, then synthesize)

Run lanes 1-4 as parallel Task subagents; each returns its top 5 candidates as structured notes
(name, url, numbers, 3-6 spec candidates each tagged spec (contains a number, becomes a `-> `
bullet) or feature (becomes a `- ` bullet), why it matters, source lane). Include a **Why** line in
each subagent prompt: "feeds today's LinkedIn draft picks -- return only items a technical founder
audience would stop scrolling for."

### Lane 1 -- GitHub trending

1. `curl -sL https://github.com/trending?since=daily` and `?since=weekly` (HTML; parse repo, stars, star delta, description).
2. Keep repos that are (a) agentic-coding/AI-tooling niche, or (b) so viral they transcend niche (>15k stars or >2k stars/day).
3. For each keeper, fetch the README: `curl -sL https://raw.githubusercontent.com/<owner>/<repo>/HEAD/README.md` -- mine concrete numbers (benchmarks, token savings, latency, supported tools) for spec bullets. A post without numbers is a discard.

### Lane 2 -- Hacker News

1. Front page: `curl -s "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=30"`.
2. Last-48h big hitters: `curl -s "https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=points>200"` (first pages).
3. Also grab high-point `Show HN` stories (`tags=show_hn`, points>100). HN is the lane most likely to surface the "Someone charted/reverse-engineered X" viral-artifact posts.

### Lane 3 -- Launch news, talks, and authority quotes (Exa)

1. Exa search (last 48h) for model/tool launches: queries like "new AI model launch pricing benchmarks", "Claude Code update", "Cursor release", "OpenAI launch", "open-source model release". Official vendor blogs beat secondhand coverage; pull pricing, tokens/sec, benchmark scores, an exec quote if present.
2. Exa search (last 7 days) for fresh conference talks / lectures / podcast episodes in the niche (Karpathy, Boris Cherny, Anthropic/OpenAI staff, AI-engineering conferences, Stanford/YC lectures). A great talk becomes a "watch this instead of doomscrolling tonight" draft; a sharp quote from one becomes an authority-quote hook draft.
3. Exa search restricted to twitter.com/x.com for viral charts/claims in the niche (last 48h). These become "Someone charted..." drafts -- unlike Stanislav, CREDIT the author by name/handle.

### Lane 4 -- Viral Reddit dev threads (Exa)

Exa search restricted to reddit.com (last 7 days) across the dev/AI subs (r/ClaudeAI, r/ChatGPTCoding, r/ExperiencedDevs, r/LocalLLaMA, r/programming): hunt for high-engagement threads where a practitioner explains a technique, cost saving, or contrarian take. These become "A senior engineer on Reddit explained..." drafts. Credit the subreddit; link the thread.

## Synthesis and drafting (main agent)

1. Pool all lane candidates, dedupe against the #li-source-scout ledger, rank by (niche fit x virality x number-richness). Pick the **top 2-3**, ideally from different lanes.
2. Draft each pick in the **Stanislav skeleton**, every source type, no exceptions. The skeleton is
   defined in `viral-playbook.md` (Input 1); follow it exactly and do not improvise structure. Only
   two things are scout-specific:
   - **Glyphs.** Draft with ASCII `-> ` for spec bullets and `- ` for feature bullets, so the text
     survives Slack and copy-paste. Never the unicode arrow, never `•`. This holds for interactive
     runs too, since those drafts also land in Slack.
   - **Source-type hook notes**, since the scout picks the source rather than Ray:
     - **Repo/tool (lanes 1, 2)** -> star-count hook, specs mined from the README.
     - **Launch/news (lane 3.1)** -> pricing / tokens-per-sec / benchmark numbers in the spec block; add a short caveats line when the claims are vendor-sourced.
     - **Talk/quote (lane 3.2)** -> the quote is the hook material; arrow bullets are the takeaways; credit the speaker.
     - **X chart / Reddit thread (lanes 3.3, 4)** -> "Someone charted..." / "A senior engineer on Reddit explained..." hooks, author/subreddit credited.
3. Rotate the P.S. lead magnet: default is the standard funnel line, but when a specific Agentic Coding School class/video matches the draft's topic, point the P.S. at that instead ("I made a full video on agent memory -> agenticcoding.school"). One P.S. per draft, always present.
4. **Run the pre-post gate** in `post-gate.md` (Input 2) on EVERY draft, item by item, before it is
   delivered. Redraft anything that fails.

   **When a pick cannot pass the gate:**
   - *Cloud:* DROP THE PICK. You are unattended; there is nobody to ask. Do not post a partial
     draft, a gate-failure report, a verification writeup, or a "here is what I would have written"
     artifact into the drafts thread. A thread reply contains a postable LinkedIn post or it does
     not exist. List the dropped pick in the main summary under near-misses with a one-line reason
     ("dropped at gate: could not verify the 78.2% benchmark claim"), then move to the next-best
     candidate so the day still ships 2-3 drafts. Posting only one draft is fine; posting a non-post
     is not.
   - *Interactive:* say what failed in one line and ask Ray whether to drop the pick or chase the
     missing fact. The Slack rule is unchanged -- only postable drafts go in the thread.

   If the source's own numbers do not survive checking, that is a good catch and worth the one-line
   note, but it is a sourcing failure, not something to write up at length. Keep it to one line.

## Delivery

### Slack (every run, both callers)

The channel is the dedupe ledger, not just a notification surface. An interactive sweep that skips
Slack leaves its picks invisible to the next cloud run, which will cheerfully re-surface the same
repo tomorrow. So both callers post.

Main message to **#li-source-scout** (create the channel via Slack MCP if missing; fallback per
`routines/CLAUDE.md`), under ~2500 chars:

- Date + lanes swept (+ any skipped due to errors), and the focus if one was given.
- Numbered list of today's picks: name, one-line why-now (with the key number), source lane, url.
- One line of near-misses worth a human eyeball (name + url only), plus any picks dropped at the gate with their one-line reason.

Then post each full draft as a **threaded reply** to the main message (capture `ts` from the first
`chat.postMessage` response and pass it as `thread_ts`), one draft per reply, so the channel stays
scannable. Post each draft inside a triple-backtick code block so Slack does not linkify the url and
Ray can copy it raw.

**The code block contains ONLY the post text, starting at the hook line.** No draft label, no lane
tag, no "Draft 1 -- Chonkie" header, no gate report, no commentary. Ray copies that block straight
into LinkedIn, so anything above the hook ships with the post. Put the label and the gate result in
the reply's plain text ABOVE the code block, where they are readable but not copyable.

Draft bodies contain apostrophes ("It's called...") and hard newlines, so NEVER inline them into a single-quoted `--data` string; the apostrophe terminates the shell quote and silently mangles the post. Write each draft to a file and build the payload with jq:

```bash
jq -Rs --arg ch '#li-source-scout' --arg ts "$TS" \
  '{channel:$ch, thread_ts:$ts, text:.}' draft1.txt > payload.json
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H 'Content-Type: application/json' \
  --data @payload.json
```

Check `.ok` on each response and retry once on failure. On an unattended run, end the main message
with: "To publish one, open Claude Code and run /linkedin with the draft."

### Also, when running interactively

Once the Slack post has landed, put the drafts in front of Ray so he can act on them in the same
session:

1. Render them with the preview script, which applies the per-post gate chips:

```bash
python3 .claude/skills/linkedin/scripts/preview-posts.py /tmp/linkedin-posts.json \
  --output /tmp/linkedin-preview.html --open
```

   Use each pick's source label (name + lane) as the `triggers` field so the preview shows what the
   draft came from.

2. Ask which one he wants, if any. **When he picks one, hand off to `write-post.md`** from its
   "After Ray Picks" section onward -- that flow owns refinement, the `post-history/` file, and
   publishing. The scout's job ends at delivered drafts; do not grow a second publishing path here.

## Definition of done

**Cloud:** the main summary AND every draft thread reply have posted to #li-source-scout (or, if
`SLACK_BOT_TOKEN` is empty, everything was written to stdout). No local report file, no commit.

**Interactive:** the same Slack post has landed, the preview has been rendered, and Ray has either
picked a draft (handing off to `write-post.md`) or said he is done.

## House rules

- **NEVER use em or en dashes** anywhere. Inside a draft body, including the P.S., never emit `--` either; use a single hyphen. Arrow bullets in drafts are ASCII `-> `, never the unicode arrow, and feature bullets are ASCII `- `, never `•`. The `--` substitution applies only to a cloud run's own Slack summary prose, per `routines/CLAUDE.md`.
- Numbered lists, not tables.
- Feature/launch drafts lead with the feature, not meta/expose angles.
- Credit viral-artifact authors by handle. Do not copy Stanislav's actual sentences -- same skeleton, Ray's voice.
- If every candidate fails the dedupe or niche bar, report "no picks today" with the near-miss list -- never force a weak draft.
