# Check Post Performance

## Steps

1. Read all files in `references/post-history/` to see which posts need updating
2. Use Chrome browser automation to navigate to Ray's activity page:
   `https://www.linkedin.com/in/rayamjad/recent-activity/all/`
3. Extract engagement data using `get_page_text` — look for reaction counts, comments, reposts, and impressions next to each post
4. For posts with direct URLs, navigate to them individually for precise numbers using:
   ```javascript
   const buttons = [...document.querySelectorAll('button, span')];
   const reactions = buttons.find(b => b.getAttribute('aria-label')?.match(/reaction/i))?.getAttribute('aria-label');
   const comments = buttons.find(b => b.innerText.match(/\d+\s*comment/i))?.innerText;
   const reposts = buttons.find(b => b.innerText.match(/\d+\s*repost/i))?.innerText;
   const impressions = document.body.innerText.match(/(\d[\d,]*)\s*impression/gi);
   ```
5. Update each post file's frontmatter with the new engagement numbers
6. Check for any posts on LinkedIn that aren't tracked in `post-history/` — offer to add them
7. Present a summary table to the user showing all posts and their current metrics
8. Note any patterns by variation axis (hook number type, scene-setting choice, spec-bullet mix, why-it-matters angle, closer) as defined in `references/viral-playbook.md`. Do not use archetype labels; that taxonomy is retired.

## Also Check

- Posts with status `draft` — ask "Did you end up posting [hook]?"
  - If yes → update to `posted`
  - If no → update to `skipped`

## Reliable full-feed re-sweep (learned 2026-06-25)

When re-checking *every* post at once (not just one), don't trust a single feed
snapshot and don't conclude a post was deleted just because it's missing from one.

**Gotchas, both real:**

1. **The activity feed is virtualized.** Only ~10-12 posts are in the DOM at any
   scroll position. A post absent from a snapshot is almost always just scrolled out,
   NOT deleted. To confirm deletion, navigate to the post's direct URL — a removed
   post shows "post isn't available / removed." Never delete a local post-history
   file based on feed absence alone.
2. **Two different "impressions" numbers.** The left sidebar "Post impressions"
   (e.g. 1,727) is a profile-wide rolling total, NOT this post's. The per-post number
   is the "N impressions · View analytics" line directly under the post's action bar.
   Always use the per-post one.

**The method that works:**

1. Navigate to `https://www.linkedin.com/in/rayamjad/recent-activity/all/`, wait ~3s.
2. Scroll to the bottom (a few `computer` scroll-down ticks) so LinkedIn lazy-loads
   the full history, then call `get_page_text` — it returns ALL rendered posts with
   their body, reaction count ("X and N others" = N+1, or a bare number), comment
   count, repost count, and the per-post "N impressions" line, in one shot.
   If the middle posts render as bare "Boost" placeholders, scroll up a notch and
   re-run `get_page_text` to force them to render.
3. Match each rendered post to its post-history file by hook/body text.
4. For per-post URLs (and to verify a specific post directly), grab permalinks via JS:
   ```javascript
   [...document.querySelectorAll('[data-urn*="urn:li:activity"]')]
     .map(c => ({urn: c.getAttribute('data-urn')?.match(/activity:(\d+)/)?.[1],
                 hint: (c.innerText||'').replace(/\s+/g,' ').slice(0,40)}))
   ```
   Permalink form: `https://www.linkedin.com/feed/update/urn:li:activity:<ID>/`
5. For a single post checked in isolation, navigating to its URL + this JS works too:
   ```javascript
   const bar = document.querySelector('.social-details-social-counts')?.innerText.replace(/\n+/g,' | ');
   const impr = document.body.innerText.match(/([\d,]+)\s+impressions/i)?.[1];
   ```

**Stability notes:** the Chrome extension occasionally drops connection mid-sweep —
just retry the call. Pages sometimes drift to `/notifications` after a `wait`; if a
reading looks contaminated (wrong URL, NO_BAR), re-navigate and re-extract. Always
include `location.pathname` in JS output to catch drift.

A full sweep also surfaces **untracked posts** (live on LinkedIn with no post-history
file) — backfill these with a new file (date can be approximate from the URN's position
between known posts) so the history stays complete.
