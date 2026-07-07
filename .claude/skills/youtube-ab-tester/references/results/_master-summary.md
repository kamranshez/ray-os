## Master Summary: Winning Patterns

Reconciliation history: 2026-06-12 — patterns re-derived independently from raw V1–V31 results, diffed against this doc, contradictions approved and applied by Ray same day. 2026-07-07 — clean-room audit: the raw data (titles/ranks/shares only, all commentary stripped) was handed to a blind agent that regenerated strategy from scratch; its output was diffed against this doc, seven amendments applied, and V32–V35 (anki, fable-return, code-with-claude, fable-sunset) folded in. Evidence tags: PATTERN = 3+ videos, TENDENCY = 2 videos / 2+ rounds on one video, ANECDOTE = 1 data point.

### Durable insights (TL;DR, updated 2026-07-07)

> This is a **digest of the tables and rules below** — a fast path, not separate findings. Every item here is backed by the ranked tables, Key Rules, and Test Mechanics later in this file (and by `_anti-patterns.md`). If you need evidence/citations, scroll down; if you just need the takeaway, stay here.

1. **Literal mechanism-description titles are the single worst category** — the title that explains what the feature literally does finishes last by 10–18pts every time it meets a stakes frame (V31 22.4%, V22 23.8%, V14 22.8%). Lead with stakes; let the thumbnail carry the "what."
2. **Absence-negation / passive-evidence titles hold the archive floor** — "Hasn't Announced This Feature Yet" 19.6% (worst ever), "The Signs Say Fable 5 Will Return" 27.4% (last). Name the actor with an active verb: both "Anthropic Will Bring..." arms beat the passive arm by 7–10pp in the same round (V33 R4).
3. **"Going Viral Right Now" is 3-for-3 AND has beaten a topic-matched "Anthropic Just Dropped" head-to-head once** (V28 R1: 37% vs 32.6%, on a re-cut Anthropic topic). Still untested on a first-run flagship drop — that's the open question, not whether they've met.
4. **Competitor-rivalry / benefit-equivalence is a proven lever** — "Kills OpenClaw" won 4/4 rounds including an all-authority round and a head-to-head vs curiosity-void; "Makes Sonnet Feel Like Opus" 44%. The specific rival dates; the lever (villain, or cheap-model-feels-flagship) is reusable.
5. **Verbatim title reuse fails on TOPIC mismatch, not fatigue** — "Biggest Subagent Upgrade Yet" won V25 + V31 but placed last on V28 (workflows video). Reuse winners only on topic-matched videos.
6. **Secrecy words and bare leak tags lose** (last 4/4: V18×2, V19, V33 "(Leak!)"); usefulness-surprise ("Nobody Knew They Needed") wins. They feel identical but aren't.
7. **On personal-method videos, first-person + a payoff clause wins; third-party credential floors.** "Changed My Life (Seriously...)" won 2/2 climbing (38.4→45.4%); payoff-free personal lost by 14.9pp clean (V32 R2) and 10.7pp (V34); "How Top 1% Learners..." placed last (27.6%). The payoff clause is the lever.
8. **A number's POSITION matters more than the number** — "1,600 Hours" killed titles, then won as thumbnail text the same week (V11). Money/% numbers win in thumbnails ("96% Cheaper" ×2) but only tie in titles.
9. **Annotated compositions beat plain folder icons since V20** (V22 command-list 41.1% vs folder 30.5%; folder lost again V35-fable-sunset). Folders won in March, lost every head-to-head after.
10. **Incumbent thumbnails beat text remixes AND reskins** — only a different composition CLASS has dethroned one (V22 before/after diagram). But a familiar incumbent can win within-test while capping the video (V35-fable-sunset: won the round, then "fewer subscribers" flag) — winning ≠ not burned.
11. **Control decay is routine and cross-round shares are NOT comparable** — R1 winners regularly drop on re-test (V23 39→31.4), and the identical title swung 38.8%→31.4% between rounds purely from a stronger field (V33 R2→R3). Judge levers only within a round.
12. **Within-test share ≠ video success** — V15 locked the archive's highest title share (49.4%) and still underperformed views at every checkpoint. Topic class sets the ceiling; titles only redistribute within it. Never cite share alone as a win.
13. **Two DISTINCT ceilings exist: thesis-format and non-Anthropic topic.** Thesis/paradigm videos crater on CTR regardless of packaging (V15, V27). Separately, Codex videos cap even in feature format (codex-goal ~7.3k) and compound back-to-back (codex-director ~3.5k). Don't conflate them; don't schedule off-topic videos consecutively.

### Title Formulas Ranked by Reliability

| Formula | Performance | Best For |
|---------|-------------|----------|
| "Anthropic Just Dropped Their Internal [X] Strategy" | 49.4% share (n=1, demoted 2026-06-12) | Insider/behind-the-scenes content. Highest within-test share in the archive — but won on V15, which underperformed typical views at every checkpoint despite the locked winner. Share ≠ success; treat as a strong frame, not the #1 formula |
| "Anthropic Just Dropped the Feature Nobody Knew They Needed" | 46.8% peak, decaying | Mystery/discovery features. Won V14 (46.8%, auto-declared) and V18 (37.2%, auto-declared), led V23 R1 — then lost as control in V23 R2 (31.4%), placed last in V16 R3 (33.2%), and the "You Didn't Know You Needed" variant lost V27-workflows R3 (30.7%) while sibling "Everyone Needed" WON that round (40.4%). The frame still wins; the specific wording fatigued. Refresh the wording, keep the frame. (PATTERN with decay) |
| Competitor-rivalry / benefit-equivalence ("Kills [rival]", "Makes Sonnet Feel Like Opus") | 35–44% | Anchored concrete claims: villain framing won 4/4 rounds — cron R1 (all-authority round, beat "24/7 Autopilot" and mechanism arms), cron R2 (36.6%), cron R3 (36.3%, beat curiosity-void "Everyone Asked For" 33.7% head-to-head), channels R1 (35%); model-equivalence "Makes Sonnet Feel Like Opus" 44% (V22 R2). Rival must be current — OpenClaw is dated. (PATTERN, named 2026-07-07 — previously unrecognized) |
| "Anthropic Just Dropped the Biggest [X] Upgrade Yet" | 38.5–41.0% | Topic-matched major upgrades. Won V25 R2+R3 and won V31 verbatim (38.5% R1; 41.0% R2, auto-declared). Topic-sensitive: placed LAST (30.3%) on V28 where "subagent" mismatched a workflows video. (PATTERN, current) |
| Personal ownership + stakes/payoff ("Changed My Life (Seriously...)", "Here's Their REAL Workflow") | 38.1–45.4% | Personal-method videos ONLY (Ray is the subject). V32-anki won 2/2 climbing (38.4→45.4%, auto-declared); V34-code-with-claude 38.1%; V4 (36.1%). The payoff/stakes clause is mandatory — payoff-free personal loses by 10–15pp (see anti-patterns). Third-party credential ("Top 1% Learners") floors on this video class. (PATTERN) |
| "The [New] [Tool] Feature Going Viral Right Now" | 36–40% | Momentum framing — 3/3 wins May–Jun 2026: V26 R2 (36%), V28 R1 (37%), V29 R2 (40%). Beat a topic-matched "Anthropic Just Dropped..." once (V28 R1, 37 vs 32.6, re-cut topic). Untested on a first-run flagship. (PATTERN, newest) |
| "Anthropic Just [verb] [thing]" / "Anthropic Will [verb]" (Dropped, Bringing Back, Will Bring) | ~34–44% | Major announcements and model news. Still the default opener as of V33 (both R4 Anthropic-active arms beat passive by 7–10pp). Not a law: lost V23 R2 to plain "Claude Code just shipped..." and lost V19 to "About to Change Forever". Verb ladder: Dropped > Added > Reveals (V10 R5: 42.3/28.2/29.5). (PATTERN) |
| Elite-user / authority credential ("Top 0.01% User's Guide", "Even Anthropic Engineers Use This") | 36–45.6% | Technique/thesis videos where there's no feature to drop. V11 44.6%, V24 39.2%, V30-loops 37.0%/38.8%. Sell WHO uses it, not WHAT it is. Does NOT transplant to personal-method videos (V32: 27.6% last). (PATTERN, topic-conditional) |
| Anticipation framing ("Is Coming", "About to Change Forever") + deadline framing ("Ends This Week") | 36–38.2% | Pre-release/roadmap: V21 won both rounds, V19 won twice. Deadline variant: "Cheap Fable 5 Ends This Week. Here's Where It Actually Matters." won V35-fable-sunset R1 (38.2%) — the concrete specificity tail beat softer deadline arms. (TENDENCY) |
| Numbers in titles: credential > count > effort-hours | mixed | Credential numbers win ("Top 0.01% User", V11). Inventory counts unreliable: "10 New Features" won V9 but "18 Unreleased" and "60 Tips" placed last. Effort-hours failed in titles and won in the thumbnail position |

### Thumbnail Text Formulas Ranked

| Formula | Performance | Notes |
|---------|-------------|-------|
| "How I [Verb] Now" | 51.5% (n=1) | Largest thumbnail share in the archive (V4, Jan 2026, personal-workflow video) — never re-tested; every thumbnail winner since V12 is a named-feature text or annotated composition. Personal-video formula, not universal |
| Named feature / "X 2.0(?)" | 38.5–44.4% | "Skills 2.0?" 44.4% (V12), "Plan Mode 2.0." 38.5% auto-declared (V20), "Nested Subagents" in V31's winning package. The thumbnail names the THING; the title carries the stakes (PATTERN) |
| Concrete value number | ~38.5% | "It's 96% Cheaper!" won two rounds (V13). "1,600 Hours" anchored V11's winning package AFTER hour-counts failed in the title position — number position matters more than the number (TENDENCY) |
| "[Feature] Changed" | ~35% | Good, short (V6) |
| "[Feature] + Magnitude" | ~32% | Medium |
| "How [Feature] Works Now" | ~32% | Medium (less personal) — loses to punchy claims (V6, V12, V13) |

### Key Rules

**Titles:**
1. "Anthropic" authority framing is reliable but not unbeatable (V23 R2 and V19: Claude Code-subject titles beat it when the feature itself is the star; V28 R1: "Going Viral" beat it on a re-cut)
2. Name the actor with an active verb; never go passive/agentless. "Anthropic Will Bring Fable 5 Back" arms beat "The Signs Say Fable 5 Will Return" by 7–10pp (V33 R4). Verb ladder: "Dropped" > "Added" > "Reveals" (V10 R5: 42.3% vs 28.2% vs 29.5%)
3. Numbers in titles: credentials ("Top 0.01%") help; inventory counts are neutral-to-negative; effort-hours are negative — move the number to the thumbnail (2026-06-12)
4. Title length is not a lever — winners range from 5 to 11 words. Optimize the frame, not the character count (2026-06-12)
5. Listing multiple features in the title kills performance (V5 26%, V3 29.7%)
6. "Explained" educational framing consistently underperforms (V5 26%, V7 32.8%, V8 29.5%)
7. Catchy terminology ("Swarms") beats technical ("Multi-Agent Teams") (V8 36.4% vs 34.1%, ANECDOTE)
8. Specific tool names beat generic terms ("Claude Code" > "AI Coding") (V4)
9. Pipe format ("| Here's What Changed") underperforms — avoid (V9 31.4%, V3 29.7%, V26 26.1%)
10. **Literal mechanism description is the biggest single loser category** — V31 R2 22.4%, V22 R2 23.8%, V14 R2 22.8%. Stakes/significance framing beats mechanism every time they meet. The separate archive FLOOR is absence-negation ("Hasn't Announced" 19.6%, "The Signs Say" 27.4%) — see `_anti-patterns.md`. (PATTERN)
11. First-person needs a payoff clause. Payoff-free personal loses on feature videos (V10 25.4%, V27-workflows R2 23.5%, V19 R3 30.6%) AND on personal videos (V34 "I Asked..." 27.4% last, -10.7pp vs same frame with "Here's Their REAL Workflow"). With a stakes/payoff clause on a personal-method video, it's a top formula (V4, V32 2/2, V34). (PATTERN)
12. Secrecy words ("Secret", "Secretly", "Hidden") and bare "(Leak!)" tags lose — last 4/4 (V18 ×2, V19, V33 R2). "Nobody Knew They Needed" is a usefulness claim, not a secrecy claim — don't conflate them. (PATTERN)
13. Verbatim reuse of a winning title works when topic-matched, fails when transplanted: "Biggest Subagent Upgrade Yet" won V25 + V31, placed last on V28. Topic mismatch is more dangerous than fatigue. (PATTERN)
14. Third-party credential fails on personal-method videos — "How Top 1% Learners Use..." 27.6% last (V32 R1). The credential frame needs a technique/thesis video, or the speaker as the credentialed subject. (ANECDOTE, wide margin)
15. Parentheticals: judge the payload — "(Seriously...)" won 2/2 (V32); "(Get Ready Now)" carried a weak field then dragged a strong headline (V33 R2 vs R3); "(Leak!)" lost. A directive tag is a crutch, not an additive lever. (TENDENCY)

**Thumbnails:**
1. "How I [X] Now" holds the archive record (51.5%) but is a personal-video formula, n=1 from Jan 2026 — for feature videos, name the feature instead
2. Shorter is better (2-3 words ideal)
3. Present tense "Now" beats year references (V4)
4. Personal framing ("How I") beats feature framing ("How [Feature]") (V4 51.5% vs V6 32.2%)
5. Simple past tense works ("Changed", "Dropped")
6. **Annotated diagram/command-list compositions beat plain folder icons from V20 onward**: V22 command-list 41.1% vs folder 30.5%; V23 slash-list won; V24 browser+pills 39%; V25 browser 35.1% vs folder 33.6%; V20 faceless "Plan Mode 2.0." 38.5% vs folder 35.3%; V35-fable-sunset folder 30.2% last. (PATTERN)
7. Concrete value numbers win in the THUMBNAIL position even when the same numbers fail in titles ("It's 96% Cheaper!" ×2 on V13; "1,600 Hours" on V11). (TENDENCY)
8. Face vs faceless is MIXED, not a law: faceless WON V20 thumb R1 (38.5%, auto-declared) and V17 R2; faceless lost V13, V22, V25, and V32-anki R2's faceless arm placed last (24.1% — confounded, title changed too). Composition quality decides. Default to face; a strong faceless concept is a legitimate test arm. (TENDENCY each way)
9. Expression: subtly-impressed closed-mouth beat open-mouth smile (40.3% vs 31.2%) and held as winner the next round (36.6%) — V23 R2+R3. (TENDENCY)
10. Incumbent thumbnails beat mid-flight challengers — text remixes (V30-loops R4: 38.8% vs 30.9/30.3) and same-layout reskins (V35-fable-sunset: 37.3% vs orange recolor 32.5%) both fail. Only a different composition CLASS has dethroned one (V22 before/after diagram). (PATTERN)
11. A recycled/familiar thumbnail can win within-test while burning the video — V35-fable-sunset reused V33's layout, won the round, then threw "fewer subscribers choosing to watch." Companion videos need a genuinely new concept, not the sibling's winner. (ANECDOTE, mechanism-consistent with rule 10)

### Title ↔ Thumbnail Division of Labor (PATTERN)

Thumbnail names the THING (/dream, /leaked, command list, "Nested Subagents"); title carries the stakes/social proof ("Feature Nobody Knew They Needed", "Makes Sonnet Feel Like Opus", "Biggest Subagent Upgrade Yet"). Winning packages: V18, V19, V22, V31; V33 R2's winner had ZERO overlap with its "DON'T WASTE IT" banner and the share rose after the banner-restating R1 leader was dropped. The inverse — title names the mechanism while the thumbnail carries stakes — never won a round in the archive. One exception on record: V12 ran near-redundant "Skills 2.0?" + "...Skills 2.0" and won anyway (n=1, don't generalize).

### Test Mechanics (how to read rounds)

1. **Spread size tells you whether the round tested anything.** Three same-family paraphrases → ~33/33/33 noise (V16 R3, V17 R1, V25 R3, V33 R1 at 2.1pp). Arms differing in KIND → 10–20 pt spreads (V14 R2, V27-workflows R1, V11 R4, V33 R2/R4 at 10pp). Structure rounds across frame families, not paraphrases. (PATTERN)
2. **Control decay is routine.** R1 winners frequently lose later rounds to fresh challengers (V11, V23 39%→31.4%, V25 36.9%→33.8%, V29 37.1%→31%). Don't treat an R1 win as final; don't panic when a control drops a few points on re-test. (PATTERN)
3. **Cross-round shares are NOT comparable — judge levers only within a round.** The identical title scored 38.8% (R2, weak field) then 31.4% (R3, strong field) on V33. Share is relative to the field; a "drop" across rounds usually means the field got stronger, not that the title got worse. (TENDENCY, mechanism-certain)
4. **YouTube auto-declared winners cluster at ≥7 pt leads and none has been reversed** (V14, V18 ×2, V20 thumb, V22, V27-workflows, V31, V32). (TENDENCY)
5. **Within-test share ≠ video success.** V15 locked a 49.4% winner and still underperformed views at every checkpoint; V35-fable-sunset's R2 thumbnail "won" while the video ranked 9/10 with a subscriber-skip flag. Topic class sets the ceiling; titles only redistribute within it (V11, V15, V24, V26, V29, V30, V35-sunset). Never cite share alone as success. (PATTERN — the most consequential rule in this file)
