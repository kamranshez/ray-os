# Promotion playbook — 2026-05-23

**Source:** Derived from snapshot `2026-05-23.json` and the 5-fork transcript pattern analysis at `2026-05-23-transcript-patterns.md`. Co-developed with Ray on 2026-05-23.

**Why this exists:** The transcript analysis identified six convergent patterns separating HIGH-RPV ($0.43-$1.20/view) from LOW-RPV (<$0.10/view) videos. This playbook converts those patterns into concrete promotion moves that can be locked in pre-script. The scriptwriter skill at `.claude/skills/youtube-scriptwriter` (same repo) reads this file as additional interview context.

**Mirrored to:** `projects/agentic-coding-school/promotion-playbook.md` in this repo (kept in sync manually for now). Skill was relocated from agentic-coding-school to ray-os on 2026-05-23 since the analysis is about Ray's YouTube channel, not the school product codebase.

---

## The 7 moves

### 1. Masterclass landing page or MCP as default demo surface

The top-3 RPV videos (ASAaKhK1B5w $1.20, _QGgk9F9CSM $1.02, XVEodnI0aHA $0.46) all used the masterclass landing page or its MCP server as the *substrate* for a live Claude Code demo. Pitch and demo aren't separate sections, they're the same section.

**Rule:** Default the working project to the masterclass landing page or its MCP. Only swap if the video topic structurally demands a different surface (e.g., HyperWhisper for a Mac feature, RayOS for a daily-workflow video).

**Killer pattern from XVEodnI0aHA:** the Telegram bot's first demo query was literally "search online for Ray Amjad's Master Claude Code class and tell me why I should buy it." The bot pitched itself.

**Scriptwriter Q:** "Which project is on screen during the main demo? Default is the masterclass landing page or its MCP."

### 2. Verbatim objection-handler script near the soft-anchor pitch

Insert this near the 1:30 soft-anchor pitch on every masterclass video:

> "You're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too."

Don't paraphrase. Don't shorten. Top 3 RPV videos all run this line near-verbatim. It's a 12-second insertion that closes the biggest objection.

### 3. Named free artifact (not generic "free videos")

Every video pitching the newsletter needs ONE specifically-named free artifact tied to the topic. Generic "you get free videos when you subscribe" is wallpaper.

Examples that worked in HIGH-RPV videos:
- "CLAUDE.md cleanup PDF cheat sheet" (JTW_sEXLH_o)
- "Mermaid Diagram Generator skill download" (DWiYdXrxSwg)
- "Plan Manager skill" (AzmnaoVP8sk)
- "PDF summary of this video" (JTW_sEXLH_o)

**Scriptwriter Q:** "What's the named free artifact for this video? Must be specific (PDF, skill, checklist, dashboard template). Generic 'free videos' is not acceptable."

### 4. Recurring micro-scarcity, not one big lifetime drop

The "lifetime ending April 23rd" line worked because it was dated. That card burns once. Micro-scarcity is repeatable:

- "First 50 buyers this month get a 30-min Loom code review"
- "Cohort price steps up on the 15th"
- "Skills class bonus drops Friday for existing members"
- "Workshop applications close Sunday"

Something dated, something specific, different each video. Keeps urgency live without overspending the lifetime card.

### 5. ONE primary paid CTA per video

Videos that stacked the workshop, the upcoming "agentic engineers" class, AND the masterclass cratered (c0gVowvMR-g $0.02, p88mkfPkOZc $0.09, 7PnF8qctDi8 $0.05). Split attention equals split conversion.

**Rule:** One paid CTA per video. Everything else demoted to "also linked below." Default = masterclass. Only swap if the video topic is structurally workshop- or waitlist-shaped.

### 6. Cross-link to a free video in the class (not another YouTube video)

At the close, recommend ONE topically-adjacent free video that lives inside the class platform. Three things happen once they sign up:

1. They cross a meaningful threshold (they have an account)
2. It's a textbook tripwire (free signup pre-qualifies + opens every future surface)
3. The platform sells for them (catalog, pricing, MCP, social proof)

**Verbatim close shape:**

> "If you liked this, there's a free video in the class where I [concrete deeper version of what you just watched]. No credit card needed to watch it, just sign up. Link's in the description."

Three load-bearing elements:
- "If you liked this" — qualifying filter
- Concrete benefit named ("clean up my CLAUDE.md files line by line") — not "free videos"
- Friction kill ("no credit card needed")

Pre-pick the pairing during scripting. See `socials/youtube/free-class-videos.md` (TODO if not present yet).

**Scriptwriter Q:** "Which free class video pairs with this topic? Look up the free-video index."

### 7. <0.2% refund stat in every closing pitch

The single best concrete trust number. Currently only used in one video (_QGgk9F9CSM). Put it in every closing pitch that mentions the class:

> "14-day money-back guarantee. Less than 0.2% of buyers have asked for a refund. Email me if you have questions, my address is in the description."

The triplet (guarantee + stat + personal email) is the _QGgk9F9CSM close and it's the gold standard. Personal email is critical — it signals class buyers get direct access.

---

## Priority order — if doing only 3

1. **#1 Masterclass as demo surface.** Lock in as scripting default.
2. **#2 Verbatim objection-handler.** Memorize, say every video.
3. **#5 One primary CTA.** Kill workshop/waitlist splits.

These three alone plausibly close half the gap between MID and HIGH RPV based on what differentiated the top 3.

---

## Action items to enable this playbook

1. **Maintain a free-video index** at `socials/youtube/free-class-videos.md` listing every free class video with topic tag + one-line description. Pre-pick the cross-link per video.
2. **Maintain a scarcity calendar.** Rotating dated micro-scarcity needs planning. One per month at minimum.
3. **Record more free class videos topically paired with planned YouTube content.** Currently you have ~3-4 free videos referenced in HIGH-RPV scripts. The bottleneck on rule #6 is supply, not demand.

---

## Provenance

- Source snapshot: `snapshots/2026-05-23.json`
- Pattern analysis: `reports/2026-05/2026-05-23-transcript-patterns.md`
- Co-developed with Ray during session `a82e966c-3385-496c-b4c0-aef788abf569`
