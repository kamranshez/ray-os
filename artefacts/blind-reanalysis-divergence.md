---
tags: [strategy, youtube, ab-testing, divergence, clean-room]
date: 2026-07-07
---

## Blind Re-Analysis vs Official Strategy: Divergence Report

Doc A = the official conclusions (`_master-summary.md`, `_anti-patterns.md`, `_tests-still-worth-running.md`), last reconciled 2026-06-12. Doc B = `blind-reanalysis-ab-strategy.md`, a clean-room re-derivation from the sanitized raw data (through 2026-07-06). Referee = `sanitized-ab-dataset.md`. Every disputed number below was checked against the referee, not taken from either narrative. Doc B invented its own taxonomy; equivalent concepts are mapped across names before any divergence is declared.

**Taxonomy map (same strategy, different names):** Doc B "Authority-Drop" = Doc A "Anthropic Just [verb]"; Doc B "Curiosity-Void Superlative" = Doc A "Feature Nobody Knew They Needed"; Doc B "Status/Identity" = Doc A "Elite-user/authority credential"; Doc B "Trend/Social-Proof" = Doc A "Going Viral Right Now"; Doc B "Personal-Ownership" = Doc A "My [tool] Workflow" + "How I [X] Now"; Doc B "Insider-Access" = Doc A "Internal Strategy / Even Anthropic Engineers." Doc B "Benefit-Equivalence" has **no** named equivalent in Doc A (see Divergence 3).

---

### 1. Convergent core (the validated backbone)

Both docs reached these independently, so the raw data confirms them:

- **"Anthropic Just Dropped [X]" is the default winning opener** for Anthropic feature drops; verb ladder **Dropped > Added > Reveals** (clean case: remote-control R5, 42.3 / 29.5 / 28.2).
- **Within-test share ≠ views.** Both flag it as the single most consequential rule, both cite the same proofs (60-tips 44-45% share yet view-warned; internal-skills 49.4% yet ranked 9/10; codex-director 40% yet last on views).
- **Literal mechanism / jargon titles lose hard** (advisor "Asks a Stronger Model" 23.8%; nested-subagents "Can Now Spawn Their Own Subagents" 22.4%).
- **Curiosity-void superlative** ("Nobody Knew They Needed") beats the literal feature name, but is **decaying / unconfirmed for mid-2026**.
- **Elite-credential frame** ("Top 0.01% User") wins on power-user/thesis videos; **first-person casual dies on feature videos** (25.4%, 23.5%).
- **Anti-patterns both name:** "Stop X" accusatory (20-29%), "Explained" educational, feature-list dumps, pipe "|" subtitles, secrecy words.
- **Thumbnail:** annotated command-list / before-after compositions beat plain folder icons; "How I Code Now" 51.5% is a personal-video record; closed-mouth subtly-impressed beats open-mouth smile (40.3 vs 31.2); face-vs-faceless is genuinely mixed (not a law).
- **Title↔thumbnail complementarity:** thumbnail carries the WHAT, title carries the WHY.
- **Test mechanics:** ~33/33/33 flat rounds are noise; control decay is routine; one variable per round; YouTube auto-declares early on lopsided rounds.
- **Topic/format ceilings exist** independent of packaging (thesis/paradigm videos crater on CTR).

This backbone is data-derived and needs no change.

---

### 2. Genuine strategic divergences (ranked by decision impact)

#### Divergence 1 — "Going Viral" vs "Anthropic Just Dropped" has ALREADY met on Anthropic content (Doc A says it hasn't)
- **Doc A:** "Going Viral Right Now" is 3/3 but "all three wins were on B-tier topics (Codex, re-cut); untested on an A-tier feature drop." Tests-still-worth-running #11: "Head-to-head vs 'Anthropic Just Dropped...' on a flagship Claude Code release is the missing test." #12: "'Biggest [X] Upgrade Yet' vs 'Going Viral Right Now' — the two currently-hottest frames have never met in the same round."
- **Doc B:** "Going Viral" beat two Authority-Drop arms on 2026-05-29 dynamic-workflows (a Claude Code / Anthropic feature), and treats it as the emergent recent winner that already out-performed the authority anchor.
- **Referee:** 2026-05-29 dynamic-workflows R1: "The New Claude Code Feature Going Viral Right Now" **37%** > "Anthropic Just Dropped Dynamic Workflows for Claude Code" **32.6%** > "Anthropic Just Dropped the Biggest Subagent Upgrade Yet" **30.3%**. So Going Viral beat a topic-matched Authority-Drop by 4.4pp, AND met "Biggest Upgrade Yet" in the same round — directly contradicting Doc A's "never met" claims. Caveat that saves Doc A partially: dynamic-workflows is a second/re-cut workflow video (so arguably not "flagship"), and the "Biggest Subagent Upgrade" arm was topic-mismatched (subagent title on a workflows video), so it wasn't a *clean* test.
- **Verdict: real-disagreement leaning official-overreach.** Doc A's literal "never met / missing test" framing is factually wrong; the honest statement is "met once, on a re-cut Anthropic topic, and Going Viral won — but not yet on a first-run flagship." This is the highest-impact divergence because it changes whether Ray defaults his next Anthropic feature title to Authority-Drop or gives Going Viral a real shot.

#### Divergence 2 — Codex/non-Anthropic topic ceiling is distinct from the thesis-format ceiling (Doc A conflates them)
- **Doc A:** Files codex-director's 3.5k under **Format Anti-Patterns → "Thesis/paradigm-format videos (no single named feature)"** ("V29 Codex Director 3.5k"). No separate "non-Anthropic topic" ceiling.
- **Doc B:** Two *distinct* ceilings — (a) thesis/paradigm videos crater on CTR, and (b) a **Codex-on-a-Claude-channel topic ceiling that compounds on consecutive Codex videos** (codex-goal ~7.3k → codex-director ~3.5k, ~half).
- **Referee:** codex-goal (2026-05-05) is a normal **/goal feature video, not a thesis video**, yet still capped (~7.3k in a same-window field where /dream hit 42.8k). codex-director (2026-06-01, 2nd consecutive Codex) fell to 3.5k. Because codex-goal is a feature video and still capped, the Codex ceiling is real *independent* of format.
- **Verdict: official-overreach (conflation).** Doc A's single "thesis format" bucket mis-attributes a topic effect to a format effect. Matters for calendar decisions: it argues Codex videos are capped regardless of packaging or format, and that back-to-back Codex compounds the hit — a spacing rule Doc A doesn't state.

#### Divergence 3 — Competitor-rivalry / benefit-equivalence is an unnamed winning lever
- **Doc A:** No "villain," "rivalry," or "benefit-equivalence" frame anywhere. "Makes Sonnet Feel Like Opus" appears only as a division-of-labor example; "OpenClaw" appears nowhere in any of the three files.
- **Doc B:** Names **Benefit-Equivalence** — a concrete before/after, price, model, or villain claim — as a strong frame when anchored: "Makes Sonnet Feel Like Opus" 44%; "Kills OpenClaw" won every round it ran.
- **Referee:** advisor R2 "…Makes Sonnet Feel Like Opus" **44%** (vs 32.3 / 23.8). cron "…Feature That Kills OpenClaw" won R1/R2/R3 (35 / 36.6 / 36.3); channels "…Kills OpenClaw" won R1 (35%). Crucially, cron R1 was an **all-Authority-Drop round** — the villain payload won over generic "24/7 Autopilot" (34%) and mechanism "Turned Claude Code Into a 24/7 Agent" (31%), isolating the villain lever; and cron R3 villain 36.3% **beat curiosity-void "Everyone Asked For" 33.7%.**
- **Verdict: blind-novel.** A genuinely reusable frame Doc A never noticed, and it beat curiosity-void head-to-head. Discounted slightly because OpenClaw is a dated rival (last used March) — but the *lever* (frame the feature as killing a competitor, or as making a cheap model feel like a flagship) is topic-agnostic and reusable.

#### Divergence 4 — The archive's worst title (19.6%) is absence-negation, not "literal mechanism description"
- **Doc A:** Cites "V27-workflows R1: 'Hasn't Announced This Feature Yet' 19.6% (worst in archive)" as the flagship exemplar of **"Literal mechanism description"** — its #1 durable anti-pattern. Has no absence-negation category.
- **Doc B:** Correctly classes it as a separate **Absence/negation ("Hasn't Announced / The Signs Say")** anti-pattern, distinct from mechanism/jargon titles.
- **Referee:** The title is "Anthropic Hasn't Announced This Claude Code Feature Yet" (workflow R1, 19.6%). It describes **no mechanism** — it's a "you don't even know this exists yet" absence frame. Doc B has a second confirming point Doc A lacks: "The Signs Say Fable 5 Will Return" 27.4% (last, fable-return R4, post-2026-06-12).
- **Verdict: official-overreach (mislabeled evidence).** The mechanism anti-pattern is still real on its *true* points (22.4%, 23.8%), but Doc A's single lowest data point is miscategorized, and a coherent 2-point absence-negation pattern is missing. Medium impact: it corrupts the evidence for Doc A's headline claim and hides a real, separate loser.

#### Divergence 5 — Doc A is stale by four videos; a batch of recent findings is unincorporated
- **Doc A:** Last reconciled 2026-06-12; newest videos are V30-loops / V31.
- **Doc B / Referee:** Cover four later videos Doc A never processed — anki (2026-06-21), fable-return (2026-06-26), code-with-claude (2026-07-06), fable-sunset (2026-07-06). New, referee-backed findings from them: anki "Changed My Life (Seriously…)" **won 38.4 → 45.4** (personal-ownership validated on fresh data, plus a *winning* parenthetical); anki R2 **~21pp thumbnail swing** (face thumbnail 45.4% vs old faceless folder 24.1%); anki third-party credential "How Top 1% Learners…" **27.6% last** on a personal video; a new **model-availability news** content type (Fable) where forward "Get Ready Now" beats passive "The Signs Say" (27.4%) and "(Leak!)" (28.8%); code-with-claude first-person-with-authority insider "I Spent a Day With Anthropic Engineers…" **38.1%**.
- **Verdict: blind-novel (by timing).** Not a reasoning failure — Doc A simply predates the data. But it's the largest actionable gap: Doc A's recent-shift narrative stops a month short of the current channel reality.

---

### 3. Emphasis differences (same direction, different weight)

- **The "Anthropic anchor."** Doc A: "Anthropic is reliable but not unbeatable" (cites change-forever and monitor "just shipped" as no-Anthropic wins). Doc B: "dropping Anthropic is a ~5-6pp authority tax, except when the thumbnail carries the logo, and not on Codex." Same phenomenon, opposite emphasis. The cleanest referee case backs Doc B's *tax* framing (cron: "Claude Code Just Killed OpenClaw" 30.2% vs "Anthropic Just Dropped the Feature That Kills OpenClaw" 36.6%, otherwise identical, ~6.4pp) — but Doc B's larger cited taxes (advisor, nested-subagents) are confounded by payload/redundancy, so the tax is real but smaller than Doc B implies and beatable by a strong frame as Doc A insists. Both partly right.
- **Curiosity-void decay.** Doc A: "refresh the wording, keep the frame." Doc B: "narrowing to Anthropic-only, unconfirmed." Referee favors Doc A's precision: on the same Anthropic video (workflow) the sibling "Everyone Needed" **won 40.4%** while "You Didn't Know You Needed" lost at **30.7%** — the family still wins, the specific wording is what fatigued.
- **Insider-Access.** Doc B breaks it out as its own high-ceiling frame (49.4% peak); Doc A folds it into the credential/elite-user row. Both flag the 49.4% as a peak, not an average, and both note the view-underperformance. Taxonomy split, not a strategy gap.
- **Thumbnail mechanism.** Doc B adds an explanatory hypothesis Doc A lacks — command-lists win via **"family-context"** (placing the new item among recognized siblings). Actionable for thumbnail design, low-stakes.
- **Cross-round comparability.** Both imply it via control-decay; Doc B states it sharply as a measurement property (fable-return identical title 38.8% R2 → 31.4% R3). Doc B is crisper.

---

### 4. What A has that B couldn't (info outside the sanitized data — scope notes, not failures)

- **Topic tiering (A-tier vs B-tier, "flagship" vs "re-cut").** Doc A knows Codex and second-workflow videos are B-tier from the content calendar; Doc B treats dynamic-workflows as just another Claude Code video. This external knowledge is exactly what lets Doc A (partly defensibly) discount the 2026-05-29 Going-Viral win — and also what makes Divergence 1 a real-disagreement rather than a clean Doc-A error.
- **Cross-video identity / V-numbering.** Doc A tracks that a title "placed last on V28 then won V31" is the *same phrase transplanted across topics*; Doc B can only see dates and can't always thread a phrase's history across videos.
- **YouTube A/B mechanics as prior knowledge** (incumbents accumulate impression history; auto-declaration behavior) — Doc A states these as known; Doc B has to infer them from share patterns.
- **The reconciliation/retirement ledger** (what was believed pre-2026-06-12 and why it was retired: "shorter titles win" = false, faceless not a hard anti-pattern, etc.) — institutional memory absent from the raw data.
- Note: Doc A's demotion of the 49.4% Internal-Strategy formula rests on view-checkpoint underperformance that **is** in the sanitized set, so Doc B found it independently — that one is not A-exclusive.

---

### 5. Recommended amendments (ranked; only where the referee supports the change)

1. **Reclassify the 19.6% floor and add an absence-negation anti-pattern.** In `_anti-patterns.md` and `_master-summary.md` rule #10, stop citing "Hasn't Announced This Feature Yet" 19.6% as "literal mechanism description." Add a new row: **Absence/negation framing ("Hasn't Announced", "The Signs Say")** — workflow R1 19.6% (archive floor) + fable-return R4 "The Signs Say Fable 5 Will Return" 27.4%. Keep the mechanism anti-pattern on its true points (22.4%, 23.8%). *(Divergence 4)*
2. **Fix the "never met" claims about Going Viral.** In tests-still-worth-running #11/#12, replace "never met in the same round" with the fact that 2026-05-29 dynamic-workflows R1 had Going Viral (37%) beating both a topic-matched Authority-Drop (32.6%) and "Biggest Subagent Upgrade Yet" (30.3%); reframe the open question as "untested on a *first-run flagship*," not "untested vs Authority-Drop." *(Divergence 1)*
3. **Add a competitor-rivalry / benefit-equivalence winning frame.** New row in the master formula table: villain ("Kills OpenClaw" 3/3 wins, beat curiosity-void head-to-head cron R3) + model-equivalence ("Makes Sonnet Feel Like Opus" 44%). Note it's an *anchored* frame and the specific rival may be dated, but the lever is reusable. *(Divergence 3)*
4. **Split the topic-ceiling anti-pattern.** Add a distinct **"non-Anthropic / Codex topic ceiling"** separate from the thesis-format ceiling, with the compounding note (codex-goal feature video ~7.3k → codex-director ~3.5k), so the two effects aren't conflated. *(Divergence 2)*
5. **Refresh Doc A to 2026-07-06.** Fold in anki (personal-ownership win + winning "(Seriously…)" parenthetical + ~21pp face-thumbnail swing), the Fable model-news content type (forward "Get Ready Now" beats passive "The Signs Say" / "(Leak!)"), and code-with-claude (first-person-with-authority insider 38.1%). *(Divergence 5)*
6. **Add the "third-party credential fails on personal videos" nuance** to the credential formula: anki "How Top 1% Learners Use Claude Code" 27.6% last — the credential needs the speaker (or "the top 1%") to be the subject, not third-party hearsay. *(from Divergence 5 batch)*
7. **Add a "vague evaluative/multiplier" anti-pattern with a content-dependence caveat:** "Way More Powerful" 25.7%, "10x More Useful" 30.4% lose, but concrete counts work ("10 New Features" 36.7%) and "10x Better" *won* a learning video (42.2%, 2025-11-27) while failing on an update (29.4%, skills-2 R4). Multipliers are content-dependent.
