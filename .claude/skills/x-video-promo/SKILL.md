---
name: x-video-promo
description: >-
  Write the short X/Twitter post that sits ABOVE an embedded YouTube video to
  make people watch it, in the proven "video-tweet" style reverse-engineered
  from Matt Pocock's highest-performing video posts. Also logs each published
  post and checks its performance a few days later against the benchmark. Use
  this skill whenever Ray has just published (or is about to publish) a video
  and wants the tweet/caption to go with it: "write a promo tweet for this
  video", "tweet to go with the video", "X caption for my video", "video
  tweet", "short post for the video below", "promo post for [video]". Also use
  it to record a published promo post ("log this promo tweet") and to grade how
  one did ("how did the promo tweet do", "check the promo post performance",
  "did the video tweet land"). This is for SHORT scroll-stopping posts attached
  to a video, NOT long-form articles (use x-article), NOT reply/quote research
  (use x-thread-miner), and NOT LinkedIn (use linkedin).
---

# X Video Promo

The post attached above an embedded video has exactly one job: stop the scroll so
the video plays. It does not need to explain the idea, sell a course, or carry a
link. It needs to open a curiosity gap and hand off to the video sitting right
underneath it.

This skill captures the reusable formula for that post, plus the two things
that make a formula actually improve over time: a log of what was published,
and a way to check a few days later whether it landed.

Reference files, by mode:

- `references/post-formats.md` — the formula, the format templates, the
  anti-patterns. Read when **writing**.
- `references/benchmarks.md` — the receipts behind the formula and how to grade
  a post. Read when **checking back** or adding a new benchmark post.

## Three modes

Figure out which one the user wants from how they phrase it, then jump in.

1. **Write** — they have a freshly made/published video and want the post. Most common.
2. **Log** — they published a post and want it recorded so we can check on it later.
3. **Check back** — a few days have passed and they want to know if a logged post performed.

A normal lifecycle is Write now, Log when posted, Check back in 2 to 4 days. You
can also do them independently.

---

## Mode 1: Write the promo post

### Step 1 — get the source and the formula
Read `references/post-formats.md` first. It holds the formula and the format
templates. Don't write from memory; the specifics are what make these land.

You need the video's substance. Best source, in order: the script in
`projects/agentic-coding-school/to-film/` or the video folder under
`socials/youtube/videos/`, the transcript, or whatever the user pastes. Pull out
the sharpest concrete beats: the named things, the surprising numbers, the
cold-open line, the one mind-bend idea. Those are your raw material.

### Step 2 — write 3 to 4 options across different formats
Don't hand back one tweet. Give a small slate so Ray can pick the angle, each
built on a *different* proven format from `references/post-formats.md` (the
reveal, the number, the reversal, the listicle, the plain announcement), and
recommend one with a one-line reason.

The non-negotiables, because they are what separate a video-tweet from a flat
announcement:

- **End on a close.** Default is the colon handoff: a short final line ending
  in a colon, then the video plays below it. "Here's how it works:" / "Here's
  the breakdown:". The colon is an open loop the brain needs to close, and the
  only way to close it is to watch. The plain-announcement format may instead
  end on a one-line personal reaction ("This is just what I needed!"). What is
  never allowed is a post that just trails off with no close at all.
- **Keep it short.** Default under ~50 words. If a draft needs a fourth idea,
  cut one instead.
- **Gate the payoff.** Tell them a thing exists and that it matters; do not give
  away the how in bullets. The video is the payoff. This is the single most
  common way these go wrong — a caption that explains everything has no reason to
  be watched.
- **Line one is a concrete, first-person claim.** A strong noun, ownership, no
  throat-clearing. "We've started using agents to manage the agents we lost
  control of." not "In this video I explain..."
- **Name things.** A named feature, skill, or project (Codex director, /grill-me,
  Sandcastle) is more clickable than an abstraction.
- **Whitespace.** One idea per line, blank lines between. Never a paragraph block.
- **No marketing voice, no sale in the caption.** The benchmark posts sell
  nothing in the post itself. Keep the masterclass/newsletter pitch in the video
  body and a pinned reply, never the hook. Stacking the pitch into the caption
  measurably suppresses the watch.
- **No em dashes or en dashes** anywhere in Ray's copy. This is a hard style rule
  for all of his written content. Use periods, colons, and line breaks (which is
  also exactly the benchmark style).

### Step 3 — offer the follow-ups
After Ray picks one, offer to (a) log it once posted, and (b) draft the reply
thread that expands the gated payoff under the video.

---

## Mode 2: Log the published post

Keep a running ledger so the formula can be graded against reality. The ledger
lives in the content repo, not in this skill (the skill syncs to a shared git
remote and must stay free of Ray's data):

```
socials/x/promo-posts-log.md
```

Create `socials/x/` if it does not exist. Append one entry per published post.
Use this shape (markdown, vault-friendly, no H1):

```markdown
## YYYY-MM-DD — <video title>

- **post:** <full tweet URL>
- **video:** <youtube URL or video-folder link>
- **format:** <which format, e.g. "the reveal">
- **text:**
  > line one
  > line two
  > closing line (colon handoff or reaction)
- **status:** posted
- **check-back due:** YYYY-MM-DD (post date + 3 days)
- **performance:** _pending_
```

Convert relative dates to absolute. Set "check-back due" to three days after
posting so a later session knows when it is worth measuring.

---

## Mode 3: Check back (manual)

Run when Ray asks how a post did, or when a "check-back due" date has arrived and
he wants a status pass.

### Step 1 — pull the numbers
```bash
python3 <skill-dir>/scripts/fetch_tweet_metrics.py "<post-url-or-id>" --author theramjad
```
The script reads the RapidAPI key from `$RAPIDAPI_KEY` or `~/.rapidapi_key`
(twitter-api45 host, same key the x-thread-miner skill uses). It returns the
post's likes / reposts / replies / views / bookmarks, and grounds them against
Ray's own recent posts (percentile and engagement rate), because raw like counts
are meaningless without a baseline and Ray's account is not Matt Pocock's.

If the script reports no key, tell Ray to put his RapidAPI key in
`~/.rapidapi_key`. Network calls may need the sandbox disabled.

### Step 2 — grade it honestly
Read `references/benchmarks.md` for the grading guidance. "Looking good" is
relative to Ray's own distribution, not to the benchmark creators. Read the
script's output and translate it:

- **Landed well** — at or above the top quartile of his recent posts, or an
  unusually high bookmark rate (bookmarks are the strongest "I want to act on
  this" signal and the video-tweet format over-indexes on them).
- **Fine** — around his median. The format worked, nothing remarkable.
- **Underperformed** — below his median. Say so plainly, and look at why: was the
  payoff given away, was the hook weak, was the sale stacked in, was there no
  close at all. Feed the lesson back into the reference files if it is a real
  pattern, not a one-off.

### Step 3 — record it
Update that post's entry in `socials/x/promo-posts-log.md`: replace
`performance: _pending_` with the snapshot (date checked, the numbers, the
verdict). Over time this ledger becomes the evidence base for which formats
actually earn the watch for Ray specifically.

---

## Notes

- The benchmark in `references/benchmarks.md` is built from Matt Pocock's video
  posts and the guinnesschen anchor. When you find a new high-performing video
  post worth learning from (Ray's own or someone else's), add it to the receipts
  and, if it reveals a new move, to the formats in
  `references/post-formats.md`. The formula is meant to grow.
- This skill is for the post-with-video-below pattern specifically. If the user
  wants a long-form X article, hand off to `x-article`. If they want to mine the
  replies/quotes of a tweet, hand off to `x-thread-miner`.
