---
tags: [harness, bitter-lesson, claude-code, meta]
aliases: [Bitter Lesson Harness Audit]
date: 2026-07-05
---

*A Bitter Lesson audit of Ray's Claude Code harness (~68 skills, 10 workflows, CLAUDE.md layers, hooks, memory). 71 findings across 8 themes. Generated via multi-agent workflow.*

## 1. The Bitter Lesson, precisely

Richard Sutton's 2019 essay makes one empirical claim and one causal argument. The claim: across 70 years of AI, the methods that won were the *general* ones that scale with computation — search and learning — not the ones that encoded human understanding of the domain. Chess opening books lost to search. Hand-built phoneme and vocal-tract models lost to statistical learning. SIFT and hand-tuned edge features lost to convolutional nets trained on more data. Every time, the human-knowledge approach helped in the short run, plateaued, and was then blown past by a general method riding more compute.

The causal mechanism is what makes this a law rather than an anecdote. Compute gets exponentially cheaper, so any project you start today sits on a *rising tide* of available computation. Building in your theory of the domain gives an immediate, satisfying lift — but it's a fixed structure on a moving floor. The moment the general method has enough compute to solve the thing directly, your hand-encoded structure stops being a shortcut and becomes a wall it has to route around. Sutton's slogan: *"We want AI agents that can discover like we can, not which contain what we have discovered. Building in our discoveries only makes it harder to see how the discovering process can be done."*

Hyung Won Chung turns this into a procedure you can actually run: add the *minimum* structure needed to get "signs of life" at today's capability, then **revisit and remove** that structure as compute/models improve — because the field reliably loves adding structure and neglects removing it, and "what is better in the long term almost necessarily looks worse now." Logan Lincoln gives you the one-question test for any given piece of scaffolding: **does this exist because of a MODEL LIMITATION, or because of a durable business/safety/cost/observability requirement?** Durable requirements stay. Model-limitation compensations are depreciating capital and should be built to be deleted.

**The translation to your harness, in one sentence:** every place you hand-code *how* to do something the model could decide for itself — a model ID, a tier, a threshold, a step sequence, a golden example, a keyword gate, a validation loop, a defensive "ALWAYS/NEVER" — is a bet that the model won't get better at that thing. It always does. A healthy harness converges toward *goal + tools + constraints + evals* and sheds structure over time; an unhealthy one accretes it, gets more prescriptive and more model-specific with every fix, and each model release widens the gap between your frozen procedure and the model's native competence.

Your harness is, on the whole, sophisticated and genuinely capable. But it is accreting in exactly the direction the rubric warns against. 71 findings cluster into eight recurring failure shapes.

---

## 2. The core diagnosis — eight themes

### Theme A — Model pinning & manual tier routing

**What it is.** Named model checkpoints and tiers are baked directly into config, instructions, and orchestration code: `"model": "opus[1m]"` as the harness-wide default (`~/.claude/settings.json:11`); per-stage tier literals `model: 'haiku'` / `'sonnet'` / `'opus'` threaded through workflow JS (`youtube-miner/assets/mine-workflow.js:134,169,195`; `loop-opportunities.js:107,124,140` and its topdown/personas/stub-walk siblings; `deep-bug-hunt` per-phase `effort` levels); prose directives that pin a task to a tier (`~/.claude/CLAUDE.md:4` "use a haiku subagent"; `auto-spec/SKILL.md` five agents pinned to `opus`; `binary-explorer`, `wisdom-to-acs-gap`, `x-thread-miner` all naming "haiku"); and raw image/TTS model strings (`youtube-ab-tester/scripts/generate.ts` + SKILL.md naming `gemini-3-pro-image-preview` in ~5 places that already disagree with the code's `gemini-3.1-flash-image-preview`; `sentence-mining/scripts/generate_media*.py` pinning `gemini-3.1-flash-tts-preview`; `explainkit-gen` hardcoding server-side style UUIDs; `codex 0.139.x` version pins).

**Why it's a violation.** A model name is the purest possible instance of "encoding the author's knowledge of one checkpoint's current behavior." It couples correctness to a transient artifact rather than a capability contract.

**Why it's fragile.** `-preview` aliases get deprecated within a generation; tier boundaries move every release (today's triage that "needs haiku" is trivial for tomorrow's cheap default; today's synthesis that "needs opus" gets subsumed). The decay has *already happened* in `youtube-ab-tester` — the code drifted to a new Gemini model and the prose didn't follow, so the SKILL.md now names a model the script doesn't use and even cites the wrong env var (`MODEL_NAME` vs `DEFAULT_MODEL`). That is the maintenance tax made visible.

**Principle violated.** Prefer the general method; express a *capability or budget contract*, not a named artifact. Let a router or a single strong default own the tier decision.

### Theme B — Hand-coded heuristics, thresholds & magic numbers

**What it is.** Frozen numeric boundaries the model could infer from the goal. The worst offenders: `stress-test-architecture/RANKING.md` encodes an entire 8-dimension rubric summed to `Total: 40` with priority bands and ~9 hardcoded caps (`No traced change path: max 20`…) — the author's theory of "what makes a finding important" as *arithmetic*. `extract-wisdom` mandates every bullet be *"exactly 16 words. Count them."* plus per-section counts. `wisdom-to-acs-gap` invents a `>=~40%` predictability cutoff and a `120-220 word` band inside a multi-step decision tree. `thermo-nuclear-code-quality-review` makes crossing `1000 lines` a presumptive blocker (repeated in `deep-bug-hunt`). `youtube-outlier-scout` freezes a views/sub ladder (`>5.0x = Mega outlier`…) and `3x`/`2x`/`<10 videos` gates. Plus recency tiers, `Flag reuse from the last 60 days`, `5 variants`, `10-12 images per script`, `60-second` narration limits, x-search's `0.3/0.4` ranking weights, `idea-foundry`'s "drop the bottom third," `topdown`'s `leverage*1.5 + pain*1.0`, and the `5-vs-10` thumbnail-parallelism contradiction between the skill docs and `feedback_thumbnail_parallelism.md`.

**Why it's a violation.** A hardcoded threshold is the author's frozen guess at a boundary a capable model judges contextually — exactly the "simple way to think about the domain" Sutton says to stop encoding.

**Why it's fragile.** The "right" number is model- and context-dependent and drifts as capability grows. The exactly-16-words rule forces padding a 12-word idea and truncating a 22-word one; the 1000-line blocker flags a clean 1,050-line file and waves through a tangled 400-line one. Each becomes silently wrong and needs hand-retuning, where "state the goal + let the model judge" would have adapted for free.

**Principle violated.** Specify the *intent and the constraint*, not the constant. Keep numbers only when they're real external limits (rate/page/concurrency caps) or a renderer contract.

### Theme C — Baked-in few-shot & golden references

**What it is.** Frozen exemplars the model must imitate. `humanizer/SKILL.md` is the flagship: an enumerated AI-vocabulary blocklist (`delve, tapestry, testament, underscore…`) plus 24 hand-catalogued pattern categories each with verbatim Before/After exemplars — a static 2023-24 theory of "what AI writing looks like." `youtube-ab-tester` ships a `golden-references/` library of ~30 exemplar images named by score, with `matt-style/` and `nate-style/` sub-galleries, the rule *"Write 5 prompts by hand, each using a different golden reference,"* and the explicit *"the explore phase is done."* `excalidraw-codex/generate.sh` force-attaches `reference1..4.png` on **every** call — and the SKILL.md *documents the failure this caused* ("codex pattern-matched the refs' diagrams and ignored the actual prompt"). `class-scriptwriter` and `loopy-ai-stub-walk` bundle golden scripts to "match"; `create-prototype` clones "proven plan #46" as the mandatory starting body; `excalidraw-deck` ships example decks to imitate; `x-article`/`newsletter-writer-teaser` re-embed the humanizer blocklist and "fingerprint" lead-ins to reuse.

**Why it's a violation.** This is precisely Sutton's "contain what we have discovered." Baked exemplars bias the model toward mimicry of one frozen output instead of reasoning to the objective.

**Why it's fragile.** A stronger model produces better output than your exemplars and needs fewer (or zero) shots; the frozen gallery then *caps quality at yesterday's ceiling* and drags results toward a stale style. The excalidraw subject-bleed and the doc/code drift are this handicap already firing.

**Principle violated.** Hand the model the winning artifacts as *data to reason over*, plus a short style/quality contract — not a template to clone.

### Theme D — Over-decomposition (HOW, not WHAT)

**What it is.** Long prescriptive step chains for routine cognition. `wisdom-to-acs-gap` Stage 1d is a multi-page state machine (6-step DE-MERGE TEST, ROUTE A/B, tie-breaks) for a judgment call. `spec-developer-v2` mandates interview choreography ("Ask one natural question at a time" + a minimum-one-question-per-bucket quota). `explainkit-gen` prescribes a 5-step prompt-writing recipe that *contradicts* its sibling excalidraw skill's "pass raw content verbatim" rule. `find-prompt-injections.js:104` hardcodes "read ONLY the final ~25% of the transcript." `idea-foundry` partitions creativity into ~18 fixed angle-lanes. `create-prototype`'s "read once / don't re-read" token choreography.

**Why it's a violation.** Prescribing HOW substitutes the author's procedure for the model's own planning — the core Bitter-Lesson-Engineering error (Miessler). It also burns context and forecloses better routes.

**Why it's fragile.** As models become better planners the prescribed steps become a straitjacket that conflicts with the model's superior plan (Logan Lincoln's receptionist case: ripping out the explicit flow improved every metric). The 25% window guarantees a miss on an injection planted at 60%.

**Principle violated.** State the outcome and the quality bar; let the model choose the procedure.

### Theme E — Keyword / regex / enumeration special-casing

**What it is.** Lexical theories of intent or of the domain's surface. `block-supabase-commands.sh` enumerates ~25 destructive subcommands by regex across three tiers. `pr-review-loop` hardcodes bot logins, reaction emojis, and cadences (`chatgpt-codex-connector[bot]` "reacts 👍", Greptile "reviews once"). `wisdom-to-acs-gap` block-lists named visual-design tools (`Awwwards, Godly, 21st.dev…`). `implement-feature` runs a per-target ladder (`nextjs`/`macos`/`windows`/`ios`/`flyio`, each with bespoke hot-zones and build commands). `create-prototype` maps dependencies→type (`electron⇒desktop`…). `idea-foundry` bakes six specific X handles as "thought leaders" for *any* topic. `youtube-outlier-scout`'s power-word/format taxonomies. `x-thread-miner`'s fixed 6-category enum.

**Why it's a violation.** Enumerating cases hand-encodes surface structure instead of the general objective — the specialized-over-general method Sutton shows loses, and the list is *perpetually incomplete*.

**Why it's fragile.** A capable model handles the unenumerated Nth case (the 7th visual-design tool, the renamed bot, Solid/Qwik) for free, but the ladder ignores or mishandles it until a human appends a branch. The harness accretes cases with age — the wrong direction.

**Principle violated.** State the general criterion once ("block irreversible remote mutations"; "skip videos with no transferable Claude Code technique"; "read the target's own CLAUDE.md and derive its conventions") and let the model classify. Note `loop-opportunities-topdown.js` *already* discovers projects dynamically while `loop-opportunities.js:11-27` hardcodes 15 stale slugs — proof the hardcode is unnecessary.

### Theme F — Deterministic workflow rigidity & context-limit compensation

**What it is.** Orchestration code that removes model agency, or that exists purely to work around a context window. `idea-foundry.js:132` truncates the idea pool at a hardcoded `250000` chars with a hand-rolled `+ ']'` JSON-repair — silently dropping the back third of every run's ideas. `loopy-ai-stub-walk.js` carries a lossy 100-140-word "ledger" and forbids reading sibling scripts ("Do NOT read the full text of those other videos"), forcing sequential execution purely to thread summary state. `x-thread-miner`'s `>=0.6` confidence gate rejects on a raw score. `youtube-outlier-scout`'s hand-coded three-bar qualify/reject gate. `codex-consult`'s `--json` buffering hack + silent-exit regex. Various parse/retry rituals.

**Why it's a violation.** It relocates judgment from a general method (the model) into hand-coded branches, and the context workarounds are textbook compensatory scaffolding — they exist *solely* because of a model limitation.

**Why it's fragile.** Context windows grow and long-horizon adherence improves every generation. The 250k cap already loses data; the ledger already loses fidelity and serializes a parallelizable job. When the model subsumes the capability these layers become pure tax — and, per Logan Lincoln, a manager-review loop that gave 10-20% today becomes a 2,500%-cost-for-3% drag once the worker is reliable.

**Principle violated.** Let judgment live in the model; isolate any genuinely-needed workaround behind one flag with a "remove when context holds X" tag.

### Theme G — Defensive over-instruction

**What it is.** Emphatic guardrail prose encoding fear of specific past failures. `~/.claude/CLAUDE.md:9-11` bakes two historical failures ("Prompt is too long"; "MCP dumps 20 objects") into permanent NEVER-rules. `youtube-ab-tester`'s "Never do" list (`Metaphor illustrations — failed in testing`, `Giant single-word typography — failed`) blanket-bans whole visual devices, plus "title generation is ALWAYS delegated to a subagent." The em-dash "grep before finishing" ritual restated across five content skills. Stacked "— CRITICAL" / "ALWAYS pass verbatim" headers in excalidraw-codex.

**Why it's a violation.** Defensive over-specification encodes the author's fear rather than the objective, bloats context, and — per Miessler — "super-smart, dumb instructions" can make a capable model do *worse* than if left alone.

**Why it's fragile.** The failure modes these rules pre-empt are exactly what improving models stop exhibiting; the warnings become dead weight that dilutes attention and occasionally overrides now-correct behavior. The "context is too heavy" justification expires as windows grow.

**Principle violated.** State the durable invariant (a genuine user preference like "no crossed-out commands," "no em dashes") once, and drop the "because the model can't be trusted" scaffolding around it.

### Theme H — No obsolescence seam

**What it is.** Compensatory mechanisms with no removal annotation and cross-file coupling — the meta-theme spanning A–G. The em-dash ritual lives in five files with no shared source. The humanizer blocklist is re-hardcoded a third time inside x-article. `feedback_faceless_thumbnails.md` freezes two image models' current failure modes (likeness drift, stubble hallucination, 1K graininess) into a memory *auto-loaded every session*, permanently routing you to a compositing workaround with no "re-run the likeness eval when the model changes" tag. Near-duplicate skills (`spec-developer` — which has *no frontmatter* and can never trigger — vs `spec-developer-v2` vs `auto-spec`; two excalidraw engines) then need hand-written negative routing ("Do NOT use for…", "Default to codex whenever…").

**Why it's a violation.** Even legitimately-needed-today scaffolding breaks impermanence discipline if it can't be cheaply deleted. Without a tag, no future maintainer can tell what's still load-bearing, so nothing gets removed — Chung's exact "we love adding structure, not removing it."

**Why it's fragile.** When the model subsumes the capability, deletion should be flipping a flag; if the logic is untagged and threaded across files, removal becomes a risky refactor, so dead scaffolding stays wired in and degrades every subsequent generation.

---

## 3. Findings table (most-harmful first, duplicates merged)

| # | Location | Theme | Sev | One-line fix |
|---|---|---|---|---|
| 1 | `~/.claude/settings.json:11` | A | crit | Drop `opus[1m]`; leave unset to inherit latest, or use a capability alias. |
| 2 | `humanizer/SKILL.md` (word blocklist + 24 pattern categories) | C | crit | Replace lexicon+exemplars with an intent instruction; keep ≤2 examples behind a ref file, tag "prune as base models stop emitting these." |
| 3 | `youtube-ab-tester/SKILL.md` golden-references/ + "explore phase is done" | C | crit | Give raw winners as data + a style contract (bg/type/icon/composition axes); re-open exploration; tag imitation compensatory. |
| 4 | `memory/feedback_faceless_thumbnails.md` (auto-loaded) | H/A | crit | Store a likeness *eval*, not the model-quirk verdict; tag "re-run when image model changes; unlock direct render on pass." |
| 5 | `youtube-ab-tester/scripts/generate.ts` + SKILL.md (gemini model in ~5 places, already drifted from code) | A | high | One config constant as source of truth; prose says "the configured image model." |
| 6 | `stress-test-architecture/RANKING.md` (Total:40 + 9 caps) | B | high | Replace arithmetic with qualitative consequence ranking; keep the vocabulary, drop the points. |
| 7 | `auto-spec/SKILL.md:80-170` (5 agents pinned `opus`; "May 2025 cutoff") | A | high | Drop `opus` pins (as codex-consult already does); make staleness capability-neutral, no date. |
| 8 | `deep-bug-hunt/…workflow.js:121-168` (SIZES 6/8/10 + ~18 PACKS) | C/B | high | Packs become optional hints; replace count caps with stop-on-convergence + token budget. |
| 9 | `pr-review-loop/SKILL.md:84-178` (bot logins, emojis, timings) | E/B | high | Describe the invariant (newest review targets current head SHA, no blockers); discover bots semantically; timings→configurable. |
| 10 | `extract-wisdom/SKILL.md` ("exactly 16 words. Count them.") | B | high | "One crisp self-contained idea"; enforce uniform length in the renderer if needed, not per-bullet. |
| 11 | `wisdom-to-acs-gap/SKILL.md:104-145` (spine state machine, 40%, 120-220w) | D/B | high | Collapse to WHAT (1-3 highest-altitude, film-able ideas; deep-dive as long as adds mechanism); drop cutoffs. |
| 12 | `youtube-outlier-scout` title-analysis-framework.md:23-55 (views/sub ladder, power-word lists) | E/B | high | Give goal + raw data; let model derive taxonomy per run; ladder is an overridable reporting default. |
| 13 | `excalidraw-codex/generate.sh:101-128` (auto-attach refs every call) | C | high | Stop force-attaching; style as a short WHAT block or opt-in `-r` hint. |
| 14 | `loop-opportunities*.js` per-call `model:'haiku'/'sonnet'` | A | high | Remove per-call tiers; one budget/policy passed to the runner. |
| 15 | `youtube-miner/…mine-workflow.js:134,169,195` (haiku/sonnet/opus per stage) | A | high | Effort knob → router picks model; encode budget not tier. |
| 16 | `idea-foundry.js:132` (250k char truncation + `+']'` repair) | F | high | Remove cap; map-reduce over ALL ideas or pass a file; tag any real limit with its context assumption. |
| 17 | `sentence-mining/generate_media*.py:33,38` (`gemini-3.1-flash-tts-preview` ×2) | A | med | Read TTS model from one shared config/env. |
| 18 | `~/.claude/CLAUDE.md:3-7` (haiku routing + "twice" threshold) | A/B | high | Policy phrasing; drop tier name and the literal count. |
| 19 | `implement-feature` per-target ladder (nextjs/macos/windows/ios/flyio) | E | med | Read the touched target's own CLAUDE.md; keep only global invariants. |
| 20 | `spec-developer-v2/SKILL.md:22-53` (one-question-at-a-time + per-bucket quota) | D | low | State the quality bar; let the model choose questions/order. |
| 21 | `wisdom-to-acs-gap:79-84` (named visual-design tool blocklist) | E | med | One general skip criterion; examples as parenthetical only. |
| 22 | `idea-foundry.js:20-23` (6 hardcoded X handles as "thought leaders") | E | med | Identify top voices for the actual TOPIC at runtime. |
| 23 | `loop-opportunities.js:11-27` (15 stale project slugs) | E | med | Enumerate `~/.claude/projects/` by recency (topdown already does). |
| 24 | `find-prompt-injections.js:104` ("read ONLY final ~25%") | D | med | Scan full transcript, report position as evidence; cost→token budget. |
| 25 | `idea-foundry.js:59-98,136` (18 fixed angles, "drop bottom third", count bands) | D/B | med | Let a planner propose angles + depth; quality bar instead of counts. |
| 26 | `codex-consult/SKILL.md:97-131` (`--json` hack, silent-exit regex, blanket `xhigh`) | F | med | Isolate CLI-quirk handling behind one tagged wrapper; per-call effort budget. |
| 27 | `newsletter-writer` / `-teaser` / `class-scriptwriter` / `x-article` em-dash grep ritual (5 files) | H/G | med | One shared house-style rule ("no em/en dashes"); drop the per-file grep ritual and "2-dash" cap. |
| 28 | `youtube-ab-tester/SKILL.md:238-244` ("Never do" visual-device bans) | G | med | Keep brand invariants; move "failed in testing" items into the results corpus as evidence. |
| 29 | `youtube-ab-tester/SKILL.md:62-192` (recency tiers, 60-day, 5-variant) | B | med | Recompute decay from actual dates; "enough variants then stop." |
| 30 | `youtube-outlier-scout/SKILL.md:250-298` (three-bar gate, 3x/2x/<10) | F/B | med | Model judges outlier-ness vs the channel's own distribution; bars overridable. |
| 31 | `x-thread-miner/…workflow.js:67,267` (`>=0.6` gate, 6-cat enum, cap 7) | F/B | med | Keep/reject with rationale, rank by argued non-obviousness; open category set. |
| 32 | `block-supabase-commands.sh:31-101` (~25 regex tiers) | E | med | Small hard-deny for the catastrophic few; semantic "irreversible remote mutation?" for the tail. |
| 33 | `thermo-nuclear-code-quality-review/SKILL.md` (1000-line blocker) | B | med | "Flag files past the point a reader can hold them"; number→configurable heuristic if wanted. |
| 34 | `auto-spec/SKILL.md:292` (Haiku, batches 5-8, cap 40) | A/B | med | WHAT + cost/parallelism budget; drop the tier name. |
| 35 | `explainkit-gen/SKILL.md:15-24` (hardcoded style UUIDs) | A | med | Resolve UUIDs at runtime by slug via list_styles. |
| 36 | `excalidraw-codex/SKILL.md:157` (`codex 0.139.x` version allowlist) | A | med | Capability probe (smoke-generate → PNG on disk) instead of version prefix list. |
| 37 | `excalidraw-codex/generate.sh:123-137` (hardcoded `#0E1116` + mascot anatomy ×2) | B/C | med | Brand tokens in one style file; state as a constraint. |
| 38 | `create-prototype/SKILL.md:117-172` (clone "proven plan #46") | C | med | Reduce to a structural contract; #46 optional example only. |
| 39 | `loopy-ai-stub-walk.js` (ledger + "don't read siblings" + fixed 7-beat skeleton + 2 exemplars) | F/C/D | med | Let writers read real neighbors; parallelize; durable constraints only, section counts as guidance. |
| 40 | `wisdom-to-acs-gap:180-182` ("haiku tier is plenty") | A | med | Keep context-isolation pattern; describe worker by role/budget, not tier. |
| 41 | `implement-feature` stage-build-review.md (v2.1.172+ pin, hardcoded binary paths, ~7/~9 angles) | A/B | med | `which`/discovery + capability check; review depth as outcome not angle count. |
| 42 | `youtube-ab-tester` "title gen is ALWAYS delegated" (context-budget rule) | G/F | med | Soft, token-budget-gated preference with obsolescence note. |
| 43 | `excalidraw-codex` "ALWAYS pass verbatim" + always-on timestamp scrubber | G/F | med | One plain goal line; move scrub behind a tagged temporary flag. |
| 44 | `feedback_thumbnail_parallelism.md` (10 vs skill's 5) | B/H | med | "Parallelize up to the API's rate limit"; delete the raw constant. |
| 45 | Duplicate/dead skills: `spec-developer` (no frontmatter) vs `-v2` vs `auto-spec`; two excalidraw engines + negative routing | H | med | Merge/delete superseded skills; disambiguate by distinct WHAT-descriptions, not "do NOT use for" lists. |
| 46 | `~/.claude/CLAUDE.md:9-11` (two failures baked as NEVER-rules) | G | med | Positive preference; drop the do-NOT clauses or tag for removal. |
| 47 | `~/.claude/CLAUDE.md:37-39` + `ray-os/CLAUDE.md:63-66` (Exa MCP IDs, already drifted `Exa_Advanced` vs `Exa`) | A/E | med | Single preference in one canonical file; let discovery pick the server. |
| 48 | `class-scriptwriter/SKILL.md:72-130` (2 golden scripts, 10-12/60s image rules) | C/B | med | Qualities that make a script land; image intent not counts. |
| 49 | `excalidraw-deck/style-guide.md` (y=100-770 band, font tiers, example decks) | B/C | med | Layout as constraints; example decks optional calibration. |
| 50 | `binary-explorer/SKILL.md:225` ("Haiku subagent per question") | A | med | Model-agnostic fan-out; keep the durable context-clean rationale. |
| 51 | `deep-bug-hunt/…workflow.js` per-phase `effort:'high'` scattered | B | low | Single run-level depth param; centralize with a "tuning knob" comment. |
| 52 | `deep-bug-hunt/…workflow.js:150,186` (~1000 lines, `src/` regex, 50k/agent) | B/E | low | Contextual size judgment; derive path root from repo; token figure→config default. |
| 53 | `~/Desktop/ray-os/CLAUDE.md:58-61` (180000ms, "5+ images", 2-3 min; Obsidian 1.12.7+ path) | B | low | "Allow generous timeouts"; reference Obsidian by `command -v`. |
| 54 | `~/.claude/CLAUDE.md:13-35` (15-line vercel while-loop, magic 2m/60/1h) | F/D | med | State the WHAT (tail 1h errors, silence=healthy); let the skill build the command. |
| 55 | `newsletter-writer` / `-teaser` (5/10/10 counts, 6 fixed hooks) | B | low | Renderer contract if truly needed; else "distinct hooks covering the content." |
| 56 | `newsletter-writer-teaser:47-53` + `x-article:104-114` ("fingerprint" lead-ins, re-embedded blocklist) | C/H | low | Lead-ins optional; point x-article at humanizer's intent, single source. |
| 57 | `x-search/scripts/search_x.py:294-321` (0.3/0.4 ranking weights) | B | low | Documented default ordering; expose weighting as a param, model re-ranks. |
| 58 | `wisdom-to-acs-gap/SKILL.md:179` ("haiku …" parenthetical) | A | low | Keep "cheap-model subagent," delete the alias. |
| 59 | `loop-opportunities-topdown.js:182` / `loop-opportunities.js:123` (composite formula, `>=6`) | B | low | Ranking intent; expose weights as a param. |
| 60 | `create-prototype/SKILL.md:163-172` (token-efficiency read/don't-read choreography) | F | low | One durable "prefer cp over Write" note, tagged as a token-economy hint. |
| 61 | `create-prototype/SKILL.md:47-52` (dependency→type ladder) | E | low | Read package.json, infer project shape. |
| 62 | `excalidraw-codex/generate.sh:58-73` (3-pattern timecode-strip regex) | E/F | low | One WHAT line ("ignore production timecodes"); regex only as tagged belt-and-suspenders. |
| 63 | `explainkit-gen/SKILL.md:47-58` (5-step recipe + exemplar + ~1500-char, contradicts sibling) | D/C/B | low | Constraint only ("concrete brief, under the API's 2000-char limit"). |
| 64 | `MEMORY.md` + `feedback_*.md` "How to apply" (prefs coupled to named skills) | H/D | low | Store durable WHAT-level prefs decoupled from skill names; prefer a generated index. |

---

## 4. The upgrade plan

Bitter Lesson is **not** "delete all structure." It's "delete the structure that compensates for a model limitation, and keep the structure that encodes a durable requirement." Work in three phases, cheapest and safest first.

### (a) Quick wins — mechanical, low-risk, do this week

1. **Model-tier indirection.** Create one resolver — a tiny config file or alias map (`fast`/`balanced`/`best`, plus `image`, `tts`) that maps abstract tiers to concrete checkpoints. Replace every literal `opus`/`sonnet`/`haiku`/`gemini-*`/`opus[1m]` in findings 1, 5, 7, 14, 15, 17, 34, 40, 50, 58 with an alias the resolver owns.
   - *Payoff at next jump:* one edit upgrades the whole harness; deprecated `-preview` models can't 404 you; the youtube-ab-tester doc/code drift becomes impossible.
   - *Keep:* genuine cost separation — but express it as a budget/latency policy the resolver reads, not a per-task tier.
2. **Delete the dead and the duplicated.** Remove `spec-developer` (no frontmatter → unreachable) in favor of `-v2`; merge the two excalidraw engines into one that picks codex-vs-gemini from an availability policy; delete the "do NOT use for…" negative-routing prose (finding 45). Collapse the em-dash ritual (finding 27) and the thrice-copied humanizer blocklist (findings 2, 56) to a single house-style source.
   - *Payoff:* fewer files to hand-sync; the model routes by semantic description, which improves for free.
3. **Runtime discovery over frozen lists.** Swap `loop-opportunities.js`'s 15 hardcoded project slugs for the recency enumeration its own topdown sibling already uses (23); resolve explainkit style UUIDs by slug (35); resolve codex/obsidian binaries via `which` (36, 41, 53).
4. **Tag every surviving workaround.** Any compensatory mechanism you're keeping today gets a one-line `# compensates-for: <limitation>; remove-when: <condition>` comment (findings 16, 26, 42, 43, 54, 60, 62). This is the cheapest possible obsolescence seam and it's what makes phase (c) auditable.

### (b) Structural — convert HOW to WHAT, numbers to judgment

5. **Rewrite the numeric rubrics as qualitative contracts.** The `stress-test` RANKING.md 40-point scorecard (6), `extract-wisdom`'s exactly-16-words (10), `wisdom-to-acs-gap`'s spine state machine + 40% cutoff (11), the 1000-line blocker (33), `youtube-outlier-scout`'s ladders (12) — replace the arithmetic with the *criteria* and let the model order/judge. Keep the vocabulary and the intent; delete the points.
   - *Payoff:* a better judge needs no fixed cutoff and stops mis-firing on edge cases (the clean 1,050-line file, the 22-word idea).
   - *Keep:* renderer contracts (if the HTML viewer truly needs exactly 10 subject lines, keep that in the renderer and *label it* a rendering constraint).
6. **Un-freeze the golden references.** For `youtube-ab-tester` (3), `humanizer` (2), `excalidraw-codex` (13), `create-prototype` (38), `class-scriptwriter` (48): stop forcing imitation. Hand the winning artifacts to the model as *data to reason over* plus a short style contract (the axes that define the look), and re-open exploration. Keep at most 1-2 illustrative examples behind a reference file.
   - *Payoff:* a stronger image/text model composes better than your frozen gallery instead of being dragged to yesterday's ceiling — and the documented excalidraw subject-bleed disappears.
7. **Replace context workarounds with the real thing.** Remove `idea-foundry`'s 250k truncation (16) — pass the full pool or map-reduce over *all* of it. Let `loopy-ai-stub-walk` writers read real neighbor scripts and run in parallel instead of threading a lossy ledger (39). Scan full transcripts in `find-prompt-injections` (24).
   - *Payoff:* higher fidelity now, and these simply get cheaper as windows grow — no re-architecture needed.
8. **Turn enumerations into general criteria.** The supabase regex tiers (32), per-target ladder (19), visual-tool blocklist (21), dependency→type map (61), thought-leader handles (22): state the objective once and let the model classify, keeping only a hard-deny list for the genuinely catastrophic.

### (c) Architectural — principle-level, so the harness *stays* healthy

9. **A house style for skills, enforced in `skill-creator`.** Adopt one rule: *a skill states the goal, the constraints, the taste, and the tools — not the steps.* Bake a linter or a review checklist into your skill-authoring flow that flags: literal model strings, bare magic numbers in prose, "Step 1/2/3" chains longer than ~5 for routine cognition, inline exemplar galleries, and untagged compensatory scaffolding. This is the meta-method Sutton actually endorses — build the thing that captures complexity, not the frozen complexity.
10. **A single model-routing layer.** Formalize the phase-(a) resolver into the one place any model decision lives. Skills and workflows request a *capability or budget*; the layer maps it to today's best checkpoint. New model release = update one map.
11. **Semantic triggering, not keyword gates.** Lean on skill `description` fields (which the model matches semantically) and retire hard string-match routing in deterministic code (pr-review bot names, x-thread enums). Reserve regex only for true safety hard-denies.
12. **A quarterly de-scaffolding review.** This is the load-bearing habit. Every model release, grep the harness for the obsolescence tags you added in step 4 and ask, per tag: *can the model now do this natively?* If yes, delete. Chung's whole point is that the field adds structure and never removes it — a scheduled removal pass is the institutional fix. Your `deep-bug-hunt` and `stress-test` skills are the perfect tools to point at your *own* harness on that cadence.
    - *Payoff:* the harness converges toward "goal + tools + constraints + evals" and *sheds* structure with each generation instead of accreting it — the single strongest signal of Bitter-Lesson health.
    - *Risk / what-to-keep:* don't let a de-scaffolding pass strip a durable guardrail because it "looks like" scaffolding. The tags from step 4 are what let you tell them apart: only tagged compensations are deletion candidates.

---

## 5. What to explicitly KEEP — don't over-correct

Bitter Lesson deletes *compensating scaffolding and pinned choices*. It does **not** delete these, and several show up in the findings as legitimately-durable — leave them alone:

- **Your genuine preferences and taste.** "No em/en dashes," "no crossed-out commands in thumbnails," "title options as a numbered list," Ray's second-person voice, the dark-mode brand palette and robot mascot, "closed-mouth subtly-impressed expression." These are durable *facts about what you want*, not model-limitation workarounds. Keep them — just state each **once** as a WHAT, decoupled from any named skill or "grep because the model can't be trusted" ritual.
- **Safety and destructive-action guardrails.** The *goal* of `block-supabase-commands.sh` (block irreversible remote DB mutations), permission gates, human-in-the-loop approval on high-consequence merges (`implement-feature` escalating big changes), idempotency checks. More model capability is an argument *for* these, not against. Only the brittle regex *mechanism* is the smell — the intent stays.
- **Verification and eval harnesses.** `pr-review-loop`'s *invariant* (a PR is clean when the newest review targets the current head with no blockers), `deep-bug-hunt`'s adversarial verify-to-disprove pass, `codex-consult`'s independent review gate, the likeness eval that *should* replace the faceless-thumbnail verdict. Verifiers are how you safely let go of the prescriptive scaffolding — they're the general method's safety net, not its enemy.
- **Real external contracts.** The ExplainKit 2000-char API limit, actual rate/concurrency/page-size caps, the 16:9 aspect ratio, viewBox dimensions, wired-device requirements, submodule layouts. These are facts about the world, not guesses about the model. Keep them; just don't confuse them with the *inferable* magic numbers sitting next to them (the ~1500-char guess, the 5-vs-10 concurrency guess, the y=100-770 band).
- **Context-isolation fan-out (minus the tier name).** Spawning a subagent "to keep main context clean" is a durable working-set reason that survives upgrades. Keep the pattern everywhere it appears (`binary-explorer`, `wisdom-to-acs-gap`, `auto-spec`) — just strip the `haiku` pin so the router picks the model.

The test to apply whenever you're unsure: **does this exist because a model can't do it yet, or because the business/safety/world requires it regardless of how good the model gets?** The first is depreciating capital — tag it, isolate it, delete it on schedule. The second is the real architecture. Keep it.
