---
tags: [strategy, youtube, packaging, ab-testing, clean-room]
date: 2026-07-07
---

## Blind Re-Analysis: Title & Thumbnail Packaging Strategy

Derived only from the sanitized A/B dataset (35 videos, 2025-11-27 → 2026-07-06). No channel docs, repo files, or external sources were consulted. "Watch share" = the % of A/B impressions that chose a variant, within YouTube's title/thumbnail test feature. All taxonomy names below are mine, invented from the evidence.

**Reading note on the core metric.** Watch share is a *relative* preference among the people YouTube already showed the test to. It is NOT a view-count predictor (see Section 5 and 6 — videos won their A/B at 40%+ and still cratered in absolute views). It is also *relative to the two other arms in that round*, so the same title scores differently across rounds depending on its competition — I only compare arms within a single round. Treat share as "which of my own variants is least-bad," not "will this video succeed."

---

### 1. Winning title patterns (ranked by strength of evidence)

I sorted every title variant into framings I named from the wording. Ranked by how reliably the framing took Rank 1 and by peak share:

**A. Authority-Drop — "Anthropic Just Dropped/Added [X]"** (strongest, most data points)
The most repeated Rank-1 framing across the whole timeline. It attributes the news to the vendor and front-loads novelty.
- 2025-12-10 weekly-features: "Anthropic Just Added These Features to Claude Code" 40.8% (won).
- 2026-01-19 planning: same formula 39.2% (won).
- 2026-02-06 agent-swarms: "Anthropic Just Dropped Agent Swarms" 36.4% (won).
- 2026-02-21 worktrees: "Anthropic Just Dropped 10 New Claude Code Features" 36.7% (won).
- 2026-03-04 skills-2: "Anthropic Just Dropped Claude Code Skills 2.0" won 4 of 6 rounds (39.3 / 36.6 / 37.8 / 35.3%).
- 2026-04-06 ultra-plan: "Anthropic Just Dropped Ultra Plan for Claude Code" peaked at 42.5%.
- 2026-04-10 advisor: "…the Feature That Makes Sonnet Feel Like Opus" 44% (this is Authority-Drop + Benefit; see D).
- 2026-05-22 workflow-tool: "Anthropic Just Dropped the Feature Everyone Needed" won all 4 rounds (40.4 / 40.9 / 35.9 / 34.8%).
- 2026-06-11 nested-subagents: "Anthropic Just Dropped the Biggest Subagent Upgrade Yet" won (38.5% → 41.0%).
Verb evidence: "Dropped" beats "Added" beats "Reveals" where compared head-to-head — cleanest case is 2026-02-25 remote-control R5: "Dropped" 42.3% > "Reveals" 29.5% > "Added" 28.2% on otherwise-similar titles.

**B. Curiosity-Void Superlative — "the Feature Nobody Knew They Needed / Everyone Asked For"** (strong, durable in the early/mid window)
Replaces the concrete feature name with a vague, high-curiosity slot. Repeatedly beats the literal name of the same feature.
- 2026-02-25 remote-control: "…the Feature Everyone Asked For" won Rounds 3-5 (38.1 / 35.7 / 42.3%), beating explicit "Remote Control for Claude Code" head-to-head.
- 2026-03-11 btw-fork: "…the Feature Nobody Knew They Needed" won all 3 rounds (37.4 / **46.8** / 40.8%) — the 46.8% is the highest share among Anthropic feature videos.
- 2026-03-24 auto-dream: "…the Feature Nobody Knew They Needed" won (39.6 / 37.2 / 35.1%).
- 2026-04-10 monitor R1: same phrase won 39%.
- 2026-05-22 workflow: "…the Feature Everyone Needed" won.
Sub-note: third-person "Nobody" beats second-person "You" ("You Didn't Know You Needed" 34.6% on 2026-03-11; 30.7% on 2026-05-22). Recency caveat in Section 7: this frame was NOT re-validated recently and failed on Codex content.

**C. Status/Identity — "Top 0.01% / Top 1% User's Guide"** (strong on power-user / thesis videos)
Frames the viewer's aspiration rather than the feature.
- 2026-03-03 60-tips: "A Top 0.01% User's Guide to Claude Code" 45.6% and "The Top 0.01% User's Guide…" 44.6% — the two highest shares across that video's five rounds, well above the "1,600 Hours" variants (23-33%). Note "Guide" crushed "Tips" (45.6% vs 23.4%) and "The" beat "A" (44.6% vs 26.1%).
- 2026-06-09 loops: "How the Top 1% Actually Run Claude Code Now" led three rounds (37.0 / 38.8%).
- Boundary: on a *personal* method video (2026-06-21 anki) the third-party "How Top 1% Learners…" floored at 27.6%, losing to first-person framing. The credential frame needs the speaker or "the top 1%" to be the subject, not third-party hearsay.

**D. Benefit-Equivalence — a concrete before/after, price, or model claim** (strong when anchored)
- 2026-04-10 advisor: "…the Feature That Makes Sonnet Feel Like Opus" 44% (big margin over 32.3% / 23.8%).
- 2026-03-07 cron & 2026-03-20 channels: the "Kills OpenClaw" villain-benefit frame won every round it ran (35 / 36.6 / 36.3%, then 35%).
- The same transformation shape *fails* when vague and unanchored: "Claude Code Planning Will Never Be the Same" 27.3% (2026-04-06).

**E. Trend/Social-Proof — "Going Viral Right Now / Everyone's Obsessed"** (the recent winner, best for non-Anthropic topics)
The go-to when the "Anthropic" authority hook isn't available (e.g., Codex videos), and in one case it beat the authority anchor.
- 2026-05-05 codex-goal: "The Codex Feature Everyone's Obsessed With" 39.1%; "…Going Viral Right Now" 36%.
- 2026-05-29 dynamic-workflows: "The New Claude Code Feature Going Viral Right Now" won 37% (beat two Authority-Drop arms).
- 2026-06-01 codex-director: "The New Codex Feature Going Viral Right Now" won R2 40%.
Intensity ladder: observable buzz ("Going Viral") > inferable ("Nobody Can Stop Using"); "Obsessed" > "Favorite" (+4.2pp, 2026-05-05).

**F. Personal-Ownership / Transformation — "Changed My Life / How I Code Now"** (only on personal-workflow videos)
- 2026-06-21 anki: "This Claude Code Setup Changed My Life (Seriously…)" won (38.4% → 45.4%), beating concrete-benefit "Never Forget Anything" by ~15pp.
- 2026-01-02 workflow: thumbnail text "How I Code Now" 51.5% (highest thumbnail-text share on record) vs "My 2026 Workflow" 27.1%.
- This frame is a death sentence on feature videos: "I Control Claude Code From My Phone Now" 25.4% (2026-02-25); "my new favourite thing" 23.5% (2026-05-22).

**G. Insider-Access — "Anthropic's Internal Strategy / Even Anthropic Engineers Use This"** (highest single peak, but thin — 3 points)
- 2026-03-19 internal-skills: "Anthropic Just Dropped Their Internal Skills Strategy" hit **49.4%** (R3), the highest single-round share in the dataset, ~20pp over both other arms.
- 2026-04-15 interactive-artifacts: "Even Anthropic Engineers Use This Claude Code Workflow" won both rounds (36.4 → 39.2%). Note "Internal" (adjective) worked; "Internally" (trailing adverb) did not (29.4%).
- 2026-07-06 code-with-claude: "I Spent a Day With Anthropic Engineers. Here's Their REAL Workflow." led at 38.1%.
Treat the 49.4% as a peak, not a reliable average.

---

### 2. Anti-patterns (what reliably loses)

**Durable (repeated across many videos and months):**

- **Dropping "Anthropic" on a feature-announcement video — a ~5-6pp authority tax.** 2026-03-07 ("Claude Code Just Killed OpenClaw" 30.2% vs Anthropic arms ~36%); 2026-04-10 advisor ("This Claude Code Command…" 29.8%, "Now Asks a Stronger Model…" 23.8%); 2026-06-11 ("Can Now Spawn Their Own Subagents" 22.4% vs 41%). Caveat: the tax vanishes when the thumbnail itself carries Anthropic authority (2026-04-01 "/leaked" logo; 2026-04-06 faceless "Plan Mode 2.0"), and does not apply to Codex topics at all.
- **Accusatory / "Stop [doing X]" framing — the floor category (20-29%).** "Stop Using Claude Code Like a Beginner" 29.5% (2026-03-03); "Stop Interrupting Claude Code (Do This Instead)" 22.8% (2026-03-11); "Stop Getting the Same Output as Everyone Else" 20.7% (2026-03-19).
- **Educational "How… / Explained" title framing (~27-30%).** "…Explained" lost on 2025-12-18, 2026-02-06. "How Claude Code Planning Works Now" 27.8% last (2026-01-19) — despite nearly the same words winning as *thumbnail* text. "How Anthropic Actually…" 29.9% (2026-03-19). (Exception: "…New Task System Explained" was the shipped title on 2026-01-23, but the A/B Rank-1 there was still the Authority-Drop variant — see Section 5.)
- **Spec-Dump / feature-list titles (~26-30%).** "Claude Code Update: Improved Skills, New Subagents, Better Hooks" 26% last (2026-01-08); "Claude Code Weekly: Browser Control, New Plugins, and More" 29.7% last (2025-12-18).
- **Vague evaluative adjectives ("game-changer", "It's Awesome", "10x more useful", "Way More Powerful") (~25-33%).** "is here, and it's a game-changer" 31.3% (2026-04-10 monitor); "10x More Useful" 30.4% (2026-04-23); "Way More Powerful" 25.7% (2026-06-11). Note: concrete counts ("10 New Features" 36.7%) work; vague multipliers don't. "10x Better" worked for a *learning* video (2025-11-27, 42.2%) but failed for an update (2026-03-04, 29.4%) — magnitude multipliers are content-dependent.
- **Insider-Jargon / naming the mechanism instead of the payoff.** "Event-driven Claude Code is a cheat code" 27.6% last (2026-04-10); "Claude Code Has a Side Channel Now" 30.3% (2026-03-11); "Claude Code Now Asks a Stronger Model When It Gets Confused" 23.8% last (2026-04-10).
- **Pipe "|" subtitle format (~26-31%).** "…| Here's What Changed" 31.4% (2026-02-21); "tCodex vs Every Other IDE | The Verdict" 26.1% (2026-05-05).
- **Title redundant with the thumbnail (restating what the image already shows) — a 5-18pp tax.** Weak version ~5pp (2026-05-29 "Anthropic Just Dropped Dynamic Workflows" 32.6% while the thumbnail said "Dynamic Workflows"). Catastrophic version 18.6pp (2026-06-11 "…Spawn Their Own Subagents" 22.4% under a "Nested Subagents" thumbnail). Contradiction (title names a different feature than the thumbnail) is worse than redundancy.

**Weak losers (1-2 data points — flagged):**

- **Absence/negation "Hasn't Announced / The Signs Say"** — one dramatic point but plausibly durable: "Anthropic Hasn't Announced This Claude Code Feature Yet" 19.6%, the dataset floor (2026-05-22). Consistent-direction: passive "The Signs Say Fable 5 Will Return" 27.4% (2026-06-26). Distinguish from *forward* early-access framing, which works ("…Ultrareview Is Coming" 37.3%, 2026-04-09).
- **Explicit secrecy "Secret / Secretly Added" (27-29%)** — two arms, one video (2026-03-24). Implied mystery ("Nobody Knew") outperforms stated secrecy.
- **Future-model insider reference** — "…Gets More Powerful When Mythos Releases" 32.3% (2026-04-10, single point); referencing an unreleased model meant nothing to viewers.
- **Adversarial-against-Anthropic** — "What Anthropic Isn't Telling You…" 30.2% (2026-04-06, single point).
- **Parentheticals are NOT a blanket anti-pattern** — genuinely mixed. Losers: "(But There's a Catch)" 31.8%, "(Leak!)" 28.8%, "(After 1,600 Hours)". Winners: "(Seriously…)" (on the winning anki title, 45.4%), "(It's Awesome)" (tied the winner at 40%), "(Don't Waste It)" (led R1, 2026-06-26). The pattern: a parenthetical that adds curiosity or self-aware voice helps; one that restates the thumbnail or adds vague hype hurts.

---

### 3. Thumbnail strategy

**Composition taxonomy (named from the data):**

- **Face + /command Folder-icon** — the workhorse baseline from ~2026-03 onward (/dream, /leaked, /ultraplan, /workflows, Subagents folders). Reliable but a *mediocre ceiling*: it loses whenever a stronger concept is offered (capped ceiling on 2026-04-23 and across 4 rounds on 2026-05-22; lost head-to-head on 2026-07-06 fable-sunset).
- **Face + Command-List (slash-command family + "new" annotation)** — the strongest repeatable thumbnail win, across 4 videos. 2026-04-10 advisor 41.1%; 2026-04-10 monitor R1 37.2% / R2 40.3%; 2026-04-23 forked-subagents 35.1%; the fake "/artifact" command variant on 2026-04-15 (39%). The mechanism the data supports is *family-context* — placing the new item among recognized siblings.
- **Face + Diagram/Comparison (before/after excalidraw, flowchart)** — the upgrade that beats the plain folder. 2026-04-10 advisor: "BEFORE / AFTER /advisor" split won 37.2%, beating the plain /advisor folder (30.5%).
- **Face + Tweet/Repo mock-up** — strong for news/leak framing (2026-03-07 cron thumbnail rounds).
- **Faceless dark icon composition** — wins only when it carries a version label / product concept ("Plan Mode 2.0" faceless 38.5% beat face 35.3% on 2026-04-06); crashes with abstract icons ("Your new advisor." 28.4%; "It dreams." 31.1%; cloud-checklist 31.3%).
- **Two-icon Versus layout** (Fable/Opus, 2026-06-26 / 2026-07-06) — insufficient outcome data to rank.

**Thumbnail TEXT is where the biggest swings live — short, concrete, benefit/curiosity beats generic:**
- 2026-01-02: "How I Code Now" 51.5% vs "My 2026 Workflow" 27.1% vs "A Lot Has Changed" 21.5% — the largest thumbnail-text gap in the data.
- 2026-03-07 cron: "It's 96% Cheaper!" (38.5%) beat "Anthropic's OpenClaw" (31.3%) and "$200 vs $5,000" (33.3%) — a concrete percentage beat both the brand and the dollar comparison.
- 2026-03-21 cloud-scheduled: "The Factory Is Coming" 38.6% > "It's Finally Coming" 34.2% > "It Never Stops" 27.2%.
- 2026-03-05 skills-2: "Skills 2.0?" 44.4% > "Build Better Skills" 28.8%.
- Shorter wins: "/leaked" (35.5%) > "/source-code" (31.5-33%); "/dream" > "It dreams.".

**Face expression — a clean two-round finding: subtly-impressed closed-mouth beats open-mouth smile and stone-face.** 2026-04-12 monitor R2: closed-mouth subtly-impressed + white oxford 40.3% vs open-mouth smile + black tee 31.2% vs confident-neutral 28.5%; R3 confirmed subtly-impressed 36.6% > raised-brows 31.8% ≈ smirk 31.6%. One video, two rounds — moderate confidence, clean direction.

**Confirmed thumbnail anti-patterns:** three-column / structural / bento layouts lose repeatedly (advisor R2 28.3%, artifacts 30%); charts / data slides parse poorly (monitor bar chart 29.3%).

**Face vs faceless is genuinely conflicting** and I won't overstate it: face wins on 2026-03-07 (38.6 vs 31.2) and 2026-03-24 (34.9 vs 31.1); faceless wins on 2026-04-06 ("Plan Mode 2.0" 38.5 vs 35.3). Discriminator hypothesis: faceless works only when it shows a version label / product concept.

**Thumbnail can out-swing the title.** 2026-06-21 anki R2: swapping to the new face thumbnail (red "LEARN 20X FASTER" box + arrow to icons) jumped the winning arm to 45.4%, while the old faceless folder arm fell to 24.1% — a ~21pp gap driven by thumbnail, not title.

---

### 4. Title vs thumbnail division of labor

The data supports a **complementarity rule**: the thumbnail carries the WHAT (feature name, slash command, event, version label, number); the title carries the WHY / implication / social proof.

- The cleanest demonstration is 2026-05-29 dynamic-workflows, where the full ranking is explained by complementarity alone: complementary title (social proof; thumbnail names the feature) 37% > redundant (title and thumbnail both name it) 32.6% > contradictory (title names a *different* feature) 30.3%.
- When the thumbnail already names the feature, restating it in the title costs ~5pp (2026-05-22, 2026-05-29) and, combined with a missing authority anchor, up to 18.6pp (2026-06-11).
- Conversely, when the thumbnail carries visual authority (an Anthropic logo, a "/leaked" tag), the title is freed to drop "Anthropic" and spend its whole budget on curiosity/implication — the only two clean cases where a no-Anthropic title won a feature video (2026-04-01 "Change Forever" 37.5%; 2026-04-06 faceless "Plan Mode 2.0").
- **Productive exception to "don't restate": version-label echo.** Title "Skills 2.0" + thumbnail "Skills 2.0?" reinforced each other (2026-03-04), because a version label is an *upgrade cue*, not a feature name.
- Independent contribution is real: across remote-control, skills-2, cron, auto-dream, ultra-plan, workflow, subagents, the thumbnail was held constant while titles still moved share by 8-20pp. Title matters on its own; thumbnail matters on its own; the win is in the pairing.

---

### 5. Test mechanics (what the A/B feature actually tells you)

- **Flat rounds are noise — a <~3pp top spread is a tie.** Roughly a third of all rounds land in a ~33.3/33.3/33.3 statistical tie: channels R3 (33.4/33.4/33.2), cloud-scheduled R1-R3 (all ~33-35%), ultra-plan R5 (33.6/33.6/32.8). Real signals show ≥5pp gaps (btw-fork 46.8 vs 30.3; advisor 44 vs 32; workflow 40.4 vs 19.6). When 3 genuinely different frames land within ~1-3pp, the *other* element (thumbnail) is the ceiling — switch to testing it.
- **R1 leaders usually regress 3-7pp; discount them, trust titles that *climb*.** Documented regressions: 2026-03-24 (39.6→37.2), 2026-04-10 monitor control (39→31.4), 2026-05-05 (39.1→33.7), 2026-05-22 control (40.4→40.9→33.4 by R3). But some *climb* — 2026-04-06 (37.3→42.5), 2026-04-15 (36.4→39.2), 2026-06-11 (38.5→41). A title that climbs across rounds is the more reliable winner than one that peaks in R1.
- **Diminishing returns after a clear 2-3 round win.** Remote-control ran 5 rounds and skills-2 ran 6 rounds only to reconfirm the frame that already led by Round 2-3. Cap title testing at ~3 rounds unless the top two are still inside the noise band.
- **Cross-round shares are not comparable — judge levers only within a single round.** Cleanest proof: 2026-06-26 fable-return, where the identical title scored 38.8% (R2, weak field) then 31.4% (R3, strong field of near-variants). A measurement property, not a quality change.
- **One variable per round.** Rounds that moved title *and* thumbnail together produced uninterpretable arms (2026-06-21 R2, 2026-06-09 R4, 2026-04-06 R3) and couldn't attribute the swing.
- **Within-test share ≠ views (the most important mechanic).** 2026-03-03 60-tips won its A/B at 44-45% share yet triggered underperformance warnings (714 views vs typical 1,600-2,800; then 5,719 vs 10,000-12,300). 2026-06-01 codex-director won its title test at 40% with rising AVD, yet ranked 10/10 on views (3.5k while /dream had 42.8k in the same window). A/B share tells you which variant to ship; it does NOT tell you whether the video will perform.
- **YouTube auto-declares winners, often early and often when one arm craters.** 2026-05-22 R1 auto-called after ~3h with a 19.6% arm dragging; also 2026-03-11, 2026-04-10, 2026-06-11, 2026-03-24, 2026-06-21. An auto-declaration on a lopsided round is a weaker signal than one on a tight round, and later rounds are then testing against a contaminated baseline.
- **Ray sometimes overrides the data winner.** 2026-01-23 task-management: the A/B Rank-1 was the Authority-Drop "Anthropic Just Added Task Management" (35.3%), but the shipped title was the Rank-2 explainer "Claude Code's New Task System Explained" (32.8%).

---

### 6. Format / topic ceilings (some topics cap views regardless of packaging)

- **Single-feature Anthropic announcement = the high-ceiling format.** The 2025-11 to 2026-02 videos with real view counts cluster at 17K-26K (2025-11-27 26,759; 2026-01-08 24,717; 2026-01-23 25,392; 2026-02-06 17,596) and also post the highest watch-shares (44-49%). **Durable.**
- **Codex (non-Anthropic) content has a hard ceiling on a Claude-first channel, and a second consecutive Codex video compounds it.** 2026-06-01 codex-director lists a same-window leaderboard: /dream 42.8k, /workflows 15.2k, Subagents 2.0 14.3k, Ultra Plan 10.0k, /goal 7.3k, monitor 6.7k, **codex-director 3.5k**. codex-goal (first Codex) drew ~7.3k; codex-director (second) ~3.5k, about half. Codex videos won their own A/B tests and still finished last. Clearest topic ceiling in the data.
- **Thesis / paradigm / workflow videos crater on CTR regardless of title.** 2026-06-09 loops (406 views at 90 min vs 1,000-1,700 typical, "59% fewer views") and 2026-06-01 codex-director ("34% fewer") both threw subscriber-skip warnings within 2-3 hours despite healthy/rising AVD — the ceiling is clicks, not retention. (Counter-point: anki, also a method video, won at 45% and wasn't flagged — abstract paradigm videos are the risk, not all method videos.)
- **Niche power-user / infrastructure topics hit view ceilings even with a record title.** 2026-03-19 internal-skills won its title test at 49.4% but still ranked 9/10 on views with a subscriber warning. High watch-share + low views = topic ceiling, not packaging failure.
- **"Subscriber-skip" (fewer subscribers choosing to watch) is a recurring, distinct failure mode** flagged on 2026-03-03, 2026-03-19, 2026-06-01, 2026-06-09, 2026-07-06 fable-sunset — associated with recommendation collapse and unfixable by re-testing titles.

---

### 7. Recency shifts (2026-05 → 2026-07 vs earlier)

Weighting recent data as instructed:

- **Observable social proof ("Going Viral Right Now") is the emergent recent winner and beat the Authority-Drop anchor in one case.** It appears only from 2026-05-05 onward: 2026-05-05 R2 36%, 2026-05-29 37% (beat two authority arms), 2026-06-01 R2 40%. Earlier videos never tested it. Clearest frame-level shift in the dataset.
- **"Nobody Knew They Needed" — the early champion (46.8% on 2026-03-11) — was NOT re-validated recently and failed on non-Anthropic content.** It floored at 30% on 2026-06-01 (Codex) and was dropped from every 2026-05-22 slate. The strongest early formula is, at best, unconfirmed for mid-2026 and, at worst, narrowing to Anthropic-only feature videos.
- **Recent watch-share ceilings look lower (~34-41%) than the early peaks (44-49%).** The early peaks (2026-03-11 46.8%, 2026-03-19 49.4%, 2026-03-03 45.6%) have not recurred since April. Partly a topic-mix effect (more thesis/Codex/personal content recently) and partly possible formula fatigue — the data can't separate the two, but the direction is consistent.
- **Content mix moved toward personal-method, thesis, insider, and "model coming/going" news** (2026-06-21 anki, 2026-06-09 loops, 2026-07-06 code-with-claude, 2026-06-26/2026-07-06 Fable), where personal-ownership, status/pillar, and insider-access frames win — a different playbook than the 2025-Q4/2026-Q1 pure feature-announcement cadence.
- **Where recent and old data conflict:** older data says "always Authority-Drop / Nobody-Knew." Recent data refines it to "Authority-Drop for Anthropic drops; Social-Proof/Identity for everything else." I weight the recent, refined version.

---

### 8. Open questions (what the data cannot settle)

1. **Is "Nobody Knew They Needed" still the top frame on a fresh Anthropic feature video in mid-2026?** It was the early peak (46.8%) but was dropped from every recent Anthropic slate and only re-tested on Codex (where it failed). Genuinely unresolved.
2. **Does high watch-share cause more views?** The data actively suggests *not* strongly (codex-director, 60-tips), but packaging can't be isolated from topic/timing — no video was shipped under two packages and measured on real views.
3. **Does the "Anthropic Just Dropped" opener add share, or is the feature name carrying it?** A clean de-handicapped "Anthropic Just Dropped Claude Code Workflows" (no restatement) was never isolated. The anchor's incremental value is inferred, never measured.
4. **Face vs faceless is unresolved as a general rule.** The "faceless wins only when it carries a version label/product concept" hypothesis rests on one faceless win (2026-04-06).
5. **When does a parenthetical help vs hurt?** The pattern (curiosity/voice helps, restatement/hype hurts) fits the data but was never isolated in a controlled round.
6. **Thumbnail image vs thumbnail text.** Most rounds vary both together; only a few isolate text (2026-01-02, skills-2). Their separate contributions can't be fully split.
7. **Face-expression generality.** The closed-mouth > open-mouth finding is one video across two rounds — suggestive, not proven channel-wide.
8. **Is the post-April decline in peak share real fatigue or purely topic mix?** Confounded; can't be separated from these files alone.
9. **No sample sizes are given**, so I can't attach confidence intervals — the ~3pp noise band is an eyeballed heuristic, not a computed threshold.

---

### 9. Top 10 strategic rules (ranked by confidence)

1. **For an Anthropic feature drop, default the title to "Anthropic Just Dropped [X]" (verb "Dropped" > "Added" > "Reveals").** The most-repeated Rank-1 framing across 8+ months (weekly-features, planning, agent-swarms, worktrees, skills-2, ultra-plan, workflow, subagents ×2); dropping "Anthropic" costs ~5-6pp unless the thumbnail carries the logo. Highest confidence.
2. **Never read watch-share as a view predictor.** Ship the winning variant, but forecast performance from topic, not from a 40% share — winners at 40-45% still finished last in views (codex-director 10/10; 60-tips and internal-skills warned despite 44-49% shares). Highest-consequence rule.
3. **Enforce title↔thumbnail complementarity: thumbnail carries the WHAT, title carries the WHY.** Restating the feature name in both costs 5-18pp (worst case nested-subagents 18.6pp); the clean ranking on 2026-05-29 is explained by complementarity alone. Free the title to spend on curiosity when the thumbnail already carries authority. High confidence.
4. **Treat any round with a <3pp top spread as a tie and stop testing titles — switch to the thumbnail.** ~A third of rounds are ~33/33/33 noise (channels, cloud-scheduled, ultra-plan R5). Don't crown noise; a flat title round means the thumbnail is the live lever. High confidence.
5. **Discount R1 leaders 3-7pp; trust titles that *climb* across rounds, and cap testing at ~3 rounds once a variant leads by ≥5pp.** Controls decayed on 2026-05-22 (40.4→33.4); the reliable winners climbed (advisor, nested-subagents). Remote-control (5 rounds) and skills-2 (6 rounds) just reconfirmed the Round-2 leader. High confidence.
6. **In the thumbnail, put a short concrete hook — a number, price %, product/version name, or "How I X Now" — not a generic label.** "How I Code Now" 51.5% vs 27.1%; "It's 96% Cheaper!" beat the brand and the dollar comparison; "Skills 2.0?" 44.4%. This is where the single biggest swings live. High confidence.
7. **Avoid the durable title losers: accusatory "Stop X" (20-29%), absence-negation ("Hasn't Announced" 19.6%, the floor), plain explainers/"Explained", feature-list dumps, insider jargon ("side channel", "cheat code"), pipe "|" subtitles, and vague evaluatives ("game-changer", "10x more useful").** Every one repeatedly ranked last. High confidence.
8. **For non-Anthropic topics (Codex) and thesis/method videos, switch to Social-Proof/Identity — "Going Viral Right Now," "Everyone's Obsessed," "How the Top 1%."** This is the recent (May-July) substitute for the missing Anthropic authority hook and it consistently won those videos. Medium-high confidence.
9. **Prefer a bespoke face+command-list or face+before/after thumbnail over the plain /command folder, and use a closed-mouth "subtly impressed" expression over an open-mouth smile.** Command-list/diagram beat the folder (advisor 41.1% vs 30.5%); closed-mouth beat open-mouth (monitor 40.3% vs 31.2%). Faceless is allowed only when a version-label/product icon tells the story ("Plan Mode 2.0" 38.5%). Medium confidence.
10. **Match the frame to the video type: Authority-Drop/Curiosity-Void for feature launches, Status/Identity for power-user & thesis, Personal-Ownership only for personal-method, Insider-Access when the content genuinely earns it.** Personal-ownership on a feature video dies (25.4%, 23.5%); third-party "Top 1%" on a personal video floors (27.6%). Insider-access has the highest ceiling (49.4%) but only ~3 data points. Medium confidence.
