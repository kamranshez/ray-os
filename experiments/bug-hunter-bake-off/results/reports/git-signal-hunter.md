---
skill: git-signal-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 11 |
| PLAUSIBLE findings | 3 |
| Findings with an executable repro | 5 |
| Files opened (of 210 in scope) | ~68 |
| Subagents spawned | 11 |
| Strategy came up dry? | no |

## Coverage ledger

**What was examined.** Phase 1 mined the full git history scoped to `nextjs/` and
`hyperwhisper-cloud/` and produced a ranked list of 17 targets plus a cut line and an
explicit exclusion list. Phase 2 spawned 8 parallel deep-reader subagents against ranks
1-7 and 12. Phase 3 spawned independent verifiers against the two highest-value claims.
Across all agents roughly **68 of the 210 in-scope files were opened**, of which about 25
were read end-to-end (`transcribe.ts`, `assemblyai.ts`, `google-chirp.ts`, `db-layer.ts`,
`usage.ts`, `auth.ts`, `credits.ts`, `cost-calculator.ts`, `stt-models.ts`, `redis.ts`,
`responses.ts`, `query.ts`, `utils.ts`, `stripe-webhook.ts`, the Drizzle schema files, and
the relevant test files). The remainder were opened to resolve a specific symbol or to
confirm a caller. That number is an aggregate reported by the subagents, not a mechanically
logged count; treat it as approximate.

**What was deliberately skipped, and why.** Locale JSON (`nextjs/messages/*.json`, 42
files) tops every raw churn list purely because one copy change fans out across 42 files;
it is data, not logic, and was excluded by name. `package.json` / lockfiles were excluded
after confirming all four post-import touches are dependabot version bumps. The legal
pages (`privacy-policy`, `terms-of-service`) are the joint-highest fix-commit files in
`nextjs/` and are 886 lines of static JSX prose with no executable surface. Test files
were used as oracles — to establish which behaviours are pinned — but were never hunted as
targets.

**What this strategy is structurally blind to on this codebase — read this part.**
This repo is a public mirror. Commit `e3708d4` (2026-06-30) dumps the whole Next.js
codebase in one commit and `3b810e6` vendors the entire Fly backend the same day. There is
no pre-2026-06-30 history at all: **67 commits total, 28 touching in-scope code.** Three of
the six signals my strategy is built on are therefore dead or degenerate here:

- **Age inversion — dead.** Every in-scope file is "born" on one of two days.
- **Bus factor — non-discriminating.** Ray Amjad authored 22 of 28 in-scope commits, bots
  the other 6. "Single-author" is true of essentially the whole repo, so it separates
  nothing and I awarded it no points.
- **Revert clusters — empty.** `git log --grep=revert` scoped to the two directories
  returns **zero** commits reachable from HEAD.
- **Churn — microscopic.** The most-touched in-scope source file has 4 post-import
  commits; the *median* in-scope file has **zero**. No file here is "hot" in any normal
  sense, so fix-density × churn × size — the core ranking formula — had almost no dynamic
  range to work with.

The ranking survived only because I substituted signals that this particular history does
carry: post-import touches, **bot authorship** (two in-scope commits by `percy-ai-bot[bot]`),
and one fix-on-fresh-feature cluster. That substitution is the honest story of this run:
the documented formula would have produced near-noise, and the targeting value came from
adapting it.

The cost of that adaptation is a large, named blind spot. Files that were imported once and
never touched again are invisible to this strategy no matter how dangerous they are.
That set includes **the entire cloud auth surface** (`middleware/auth.ts`, 1 commit ever),
`nextjs/src/lib/auth.ts`, `app/api/auth/[...all]/route.ts`, `server/api/trpc.ts`,
`middleware.ts`, `lib/security/timing-safe-secret.ts`, `lib/rate-limit.ts`, the Stripe
webhook **route** (signature verification), the 430-line `webhooks/add-blog-post/route.ts`,
the 376-line WebSocket streaming route, the 377-line assistant route, and **9 of the 11 STT
providers** — only AssemblyAI and Chirp ever moved. Two of my strongest findings
(`auth.ts:70`, `usage.ts:37`) came from files with essentially no git signal; the dead-code
hunter reached them sideways while auditing the bot's deletions, not because the ranking
pointed there. That is luck partially compensating for a structural gap, and it should be
scored as such.

**"62 files opened" does not mean "the other 148 are clean."** It means 148 in-scope files
were never read by this hunt.

---

# Bug hunt report — hyperwhisper-public @ 83615b6

## Summary

Eight targets were deep-read at HEAD out of 17 ranked. The hunt produced **11 CONFIRMED and
3 PLAUSIBLE findings** (findings 1-11 and 12-14 respectively), five backed by an executed
repro against the repo's real exported functions — four of them passing `bun test` suites
that drive the real route handlers, against a HEAD baseline of 138 pass / 0 fail.

Two findings stand out. A preflight credit-reservation gate in `transcribe.ts` omits a
container check the provider's real eligibility gate performs, over-reserving by 2.1-3.0x
and rejecting funded customers with a spurious `402` — found independently by two hunters,
each confirming it by execution. And `/usage` caches a transient licensing-API 5xx as a
definitive "invalid licence" for a full hour, locking paying customers out of transcription
with no retry — found independently by three hunters and an independent verifier, with two
separate passing repros, and made worse by a 429 variant that an **unauthenticated**
attacker can trigger against other people's accounts.

The single most valuable targeting signal on this repo was **bot authorship**: both
`percy-ai-bot[bot]` commits seeded confirmed findings, while the classic churn/fix-density
formula contributed almost nothing. The most interesting negative result is that the bot's
*deletions* were correct on all five counts — two independent hunters converged on that
refutation.

## Ranked target table (Phase 1 output — a deliverable in its own right)

| # | Target | Signals | Hunted? |
|---|---|---|---|
| 1 | `hyperwhisper-cloud/src/providers/assemblyai.ts` | bot-authored (`d92838d`), 610 LOC, ~50% bot-written, 3 self-declared review-fix rounds | yes |
| 2 | `hyperwhisper-cloud/src/routes/transcribe.ts` | 3 fix commits (most of any cloud source file), 734 LOC, partially bot-authored | yes |
| 3 | `cost-calculator.ts` + `stt-models.ts` | both bot-authored in `d92838d`, 520 + 291 LOC, billing surface | yes |
| 4 | `google-chirp.ts` + `providers/utils.ts` | only dedicated `fix(cloud)` commit (`c45ad84`), 745 LOC, `selfOnly` (no fallback) | yes |
| 5 | `db-layer.ts` + stripe schema + `stripe-webhook.ts` | bot deleted the Stripe idempotency helper; 1023 LOC, largest in scope | yes |
| 6 | `redis.ts` + `responses.ts` | bot-authored deletions removing IP-quota accounting and CORS/block helpers | yes |
| 7 | `query.ts` + `usage.ts` | asymmetric fix — `rawQuery()` applied to one route only | yes |
| 8 | `post-process.ts` + `llm-completion.ts` + `text-processing.ts` + `llm-token-limits.ts` | largest post-import human refactor (`28de2ec`), then gutted by the bot | no |
| 9 | 5 LLM adapters (`anthropic`, `openai-llm`, `gemini-llm`, `groq-llm`, `mistral-llm`) | same refactor touched all five by wildly uneven amounts | no |
| 10 | `checkout/credits/route.ts` + `validation.ts` | 4 post-import touches (joint-most in `nextjs/`), guest-accessible money endpoint | no |
| 11 | 3 `api/internal/*` routes | only genuine new-file commit post-import; strongest surviving age-inversion signal | no |
| 12 | `stripe-webhook.ts` + credit-grant/balance schema | wallet accounting re-derived twice in consecutive commits | yes |
| 13 | `license-key.ts` + `license-validation.ts` + `auth-license-key-plugin.ts` | bot deleted `normalizeLicenseKey` | partial |
| 14 | 3 credit UI components | same purchase math duplicated across three separately-edited components | no |
| 15 | 3 email templates + `escape-html.ts` + `email.ts` | rename-driven edits next to a dedicated escaper | no |
| 16 | `usage.ts` + `middleware/credits.ts` | bot changed the *reservation* half; the *deduct* half never moved | yes |
| 17 | banner/layout cluster | genuine fix-on-fresh-feature (`7cc5fc0` → `b2e4b43` → `c3012ab`) | no |

**Cut line:** ranks 18-22 were `server/api/routers/customer.ts`, `purchase-success/page.tsx`,
`api/config/route.ts`, the Drizzle schema index, and the navbar/landing pair.

**Excluded by name:** locale JSON (42 files, mechanical fan-out), package/lockfiles
(dependabot only), appcast XML, deleted files, legal prose pages, Drizzle SQL, and all
out-of-scope trees.

---

## Findings

### 1. `hyperwhisper-cloud/src/routes/transcribe.ts:167-173` — preflight reserves at AssemblyAI's sync rate for requests that can never run sync, rejecting funded customers with a spurious 402 (CONFIRMED, executable repro, independently verified)

- **Led here by:** rank 2 — the file with the most fix commits in the cloud service, carrying 59 lines written by `percy-ai-bot[bot]` in `d92838d`.
- **Failure scenario:** A customer with 8.1 credits posts a 700,000-byte **MP3**
  (`Content-Type: audio/mpeg`), `X-STT-Provider: assemblyai`,
  `X-STT-Model: universal-3-pro`, `?language=en`. The reservation reserves **11.0 credits**;
  `validateCredits` sees `8.1 < 11.0` and returns **402 "Insufficient credits"**. Had the
  request run it would have gone async (MP3 is not WAV) and cost **5.2 credits**, which the
  customer could afford. The rejection window is any balance in `[5.2, 11.0)`. The 402 body
  also **misreports the requirement** — it tells the user the transcription "requires
  approximately 11.0 credits" when the true cost is 5.2 — so any client-side "top up N
  credits" prompt driven by that number asks for roughly twice what is actually needed.
- **Trigger path:** `POST /transcribe` (mounted `src/index.ts:45`) → `transcribeRoute`
  → `estimateCreditsForProviderFallbacks(...)` at line **417** → `validateCredits` at line
  **418** → `insufficientCreditsResponse` (402).
- **Evidence:** the reservation gate has three conditions and no container check:
  ```ts
  // transcribe.ts:167-173
  if (
    provider === 'assemblyai' && !medical
    && estimatedSeconds < ASSEMBLYAI_SYNC_ELIGIBLE_ESTIMATED_SECONDS
    && hasExplicitAssemblyAILanguage(language)
  ) {
    rates.push(ASSEMBLYAI_SYNC_ESTIMATED_USD_PER_MINUTE);
  }
  ```
  The provider's real gate has four:
  ```ts
  // assemblyai.ts:390-391
  const wavContainer = isWavContentType(contentType);
  const syncEligible = !medical && explicitLanguage && wavContainer && estimatedSeconds < SYNC_ELIGIBLE_ESTIMATED_SECONDS;
  ```
  `isWavContentType` is `contentType.toLowerCase().includes('wav')` (assemblyai.ts:157-159).
  `estimateCreditsForProviderFallbacks` (line 130) takes six parameters and `contentType` is
  not among them — although `contentType` **is** in scope at the call site since line 335,
  so the fix is available at zero cost.
- **Why not intentional:** the comment block immediately above the gate names the exact harm
  this code causes — *"This condition must exactly mirror `transcribeWithAssemblyAI`'s real
  eligibility gate"* and *"over-reserving for it could wrongly reject a low-balance user at
  preflight for a request that will only ever go through the cheaper async path."* The
  comment enumerates only three conditions, so the WAV gate was added to the provider and
  never propagated. `d92838d`'s own PR body shows both changes landed in the same review
  round: it added the WAV gate *and* fixed a different over-reservation, introducing this one.
  Every sync test in `transcribe-multi-provider.test.ts` hardcodes `'Content-Type': 'audio/wav'`
  (line 195), so the divergence is unexercised.
- **Repro (executed end-to-end through the real Hono route; `bun test` 2 pass).** Baseline at
  HEAD is 138 pass / 0 fail, so this is a genuinely new failure, not a pre-existing red.
  ```
  [audio/mpeg, balance 8.1] status=402
    body: {"error":"Insufficient credits","message":"You have 8.1 credits remaining.
           This transcription requires approximately 11.0 credits.", ...}
    sync endpoint attempted: false   (false => it could ONLY have run async)

  [audio/mpeg, balance 1000] status=200
    X-Total-Cost-Usd = 0.005104
    cost = {"usd":0.005104,"credits":5.2}
    => the SAME request the 8.1-credit user was 402'd on actually costs 5.2 credits.
  ```
- **The independent verifier returned CONFIRMED and corrected two of my numbers.** Recording
  the corrections rather than the flattering version: the eligibility threshold is **100
  seconds**, not 120 (`assemblyai.ts:76-85` — 120 minus a 20-second safety margin), and the
  practical blast radius is wider than first stated. The sync branch fires for **any
  `Content-Length` in [1, 799,999] bytes** — established by binary search over the real
  `estimateAudioSecondsFromSize` — which is essentially every normal dictation clip. Worst
  case over-reservation is **8.3 credits** (universal-2 at 794,000 bytes: reserved 12.5,
  actual 4.2), against `CREDITS_PER_MINUTE = 6.3`, so the 402 window is roughly a minute of
  quota — precisely the near-exhausted population the feature exists to protect. The sync
  rate is strictly higher than every async rate, including universal-3-pro plus the keyterms
  add-on, so no model choice narrows the claim.
- **Severity is medium, not high.** The verifier established that the reservation is a pure
  gate, not an escrow: actual deduction at `transcribe.ts:676-681` uses the real cost, so
  nobody is over-*charged*. The harm is a wrongly denied request, not lost money.
- **Unproven link, stated plainly.** Whether the shipping desktop clients actually send the
  triggering combination (non-WAV + assemblyai + explicit language) was **not settled**.
  Evidence points both ways: the macOS mime resolver's default fallback is `audio/mp4`
  (`AudioMimeTypeResolver.swift:35`) and the local API accepts mp3/m4a/flac/ogg/webm, but the
  verifier could not confirm what container the recorder actually writes or whether the client
  sends an explicit language. This does not affect the verdict for a documented HTTP API —
  any direct API caller triggers it trivially — but it decides whether real customers are
  hitting it today. Settling it needs a trace of the client's recorder output and language
  default.
- **Why not intentional (strengthened by the verifier).** `git blame` shows the reservation
  and the WAV gate landed in the *same* commit, so there is no "gate added later" drift story.
  Three things nevertheless cut hard against intentionality: the comment demands the gates
  "exactly mirror" each other and then enumerates only three of four conditions; the comment
  spells out this exact harm as something to avoid; and
  `transcribe-multi-provider.test.ts:757-773` pins that same reasoning as a **regression test**
  for the *language* condition, using almost the same words. The authors treated this failure
  mode as a bug worth a test and simply never wrote the WAV analogue.
- **Suggested fix direction:** thread `contentType` into `estimateCreditsForProviderFallbacks`
  — its signature has no `contentType` parameter at all, so this is a signature-level gap, not
  a one-token omission — and call the *same* `isWavContentType` the provider uses. The deeper
  invariant, since this is the second mirror-drift bug in the same pair, is that the
  eligibility predicate should exist **once** and be imported by both sites rather than
  restated in prose and code.

### 2. `hyperwhisper-cloud/src/routes/usage.ts:44-52` — a transient license-API 5xx is cached as "license invalid" for a full hour, locking out paying customers (CONFIRMED, executable repro, independently verified)

- **Led here by:** rank 7/16 — flagged by *adjacency*, not its own history: the bot changed
  the reservation half of the credit pair and nothing touched the deduct half.
- **Failure scenario:** A customer's desktop client polls `/usage` at the moment
  `hyperwhisper.com` returns a 500 (cold start, deploy, DB stall). `response.json()` fails,
  `.catch(() => ({}))` yields `{}`, so `isValid` computes `false` and `credits` `0` — and
  that verdict is written to Redis under `license:<key>` for **3600 seconds**. Every
  subsequent `POST /transcribe` reads the same key in `middleware/auth.ts`, sees
  `isValid === false`, and returns **401 "Invalid license"** for the next hour, long after
  the license API has recovered.
- **Trigger path:** `GET /usage?account_key=…` (registered `src/index.ts:54`) →
  `validateLicenseAndGetCredits` → `cacheLicense`. Damage surfaces at `POST /transcribe` →
  `validateAuth` → `getCachedLicense` → `invalidLicenseResponse()`.
- **Evidence:** there is no status inspection anywhere in the function:
  ```ts
  // usage.ts:37-52
  const response = await fetch(`${apiBase}/api/license/validate`, { ... });
  const data = await response.json().catch(() => ({})) as { valid?: boolean; credits?: number };
  const isValid = data.valid === true;
  const credits = readFiniteCredits(data) ?? 0;
  await cacheLicense(licenseKey, { isValid, credits, cachedAt: new Date().toISOString() });
  ```
- **Why not intentional:** the sibling that writes the **same Redis key** via the **same
  helper** guards this case explicitly, and its comment names the identical harm:
  ```ts
  // middleware/auth.ts:62-73
  // A 5xx (cold start, upstream timeout, internal error) is a transient
  // failure, not proof the license is invalid — caching it would lock a
  // paying user out for the full LICENSE_CACHE_TTL_SECONDS. ...
  if (response.status >= 500) { ...; return { isValid: false, credits: 0 }; }
  ```
  `LICENSE_CACHE_TTL_SECONDS = 60 * 60` (`constants.ts:7`). `usage.ts`'s own outer `catch`
  correctly returns *without* caching for network failures — proving the author understood
  the rule and missed only the non-ok-HTTP branch. `getCreditsBalance` in the same file
  *does* gate on `if (!response.ok)` before caching. `usage.test.ts` never exercises a
  non-200 from the license API.
- **Repro (executed; two independent implementations, both passing).** Each drives the **real**
  `usageRoute` and **real** `validateAuth` with `globalThis.fetch` stubbed and an in-memory
  Redis shared by both modules — no network calls. Observed:
  ```
  1. GET /usage during the blip   -> 401 {"error":"Invalid license key",...}
     cache entry now              -> {"isValid":false,"credits":0,...}
     entry TTL (seconds)          -> 3600
  2. API has fully RECOVERED
  3. /transcribe validateAuth()   -> REJECTED 401
     licensing API calls made     -> 0  (never retried)
  4. CONTROL - same 500 seen by auth.ts:
     cache entry written          -> null
     next call after recovery     -> ALLOWED (self-heals)
  ```
  The control is the load-bearing part: identical input, `auth.ts` self-heals and `usage.ts`
  does not.
- **The independent verifier CONFIRMED it and found it worse than claimed.** Two additions
  from that pass. First, the trigger is not hypothetical: the 500 is a coded branch of this
  repo's own licence API (`nextjs/app/api/license/validate/route.ts:127-134`, a catch-all
  returning `{valid:false, error:"Failed to validate license. Please try again later."}`), and
  because that body is well-formed JSON with `valid:false`, it poisons identically whether or
  not the parse succeeds. Second, the macOS client calls this path with `force_refresh=true`
  on settings-pane appearance and on licence activation, which **overwrites an
  already-good cache entry** — the verifier demonstrated a pre-existing
  `{isValid:true, credits:5000}` being destroyed by a single `/usage` call during an outage.
  `/usage` is registered bare at `index.ts:54` with no auth middleware, so the poisoning route
  and the victim route share a cache but not a code path. Partial mitigation, recorded for
  honesty: `/usage?force_refresh=true` does self-heal, so the expected lockout is "until the
  user next opens the Cloud Account settings pane, capped at one hour" rather than always a
  flat hour — but a user who only presses the transcribe hotkey never triggers it.
- **Suggested fix direction:** hoist the 5xx guard into `cacheLicense` itself, or better,
  collapse the two duplicated validate-and-cache implementations into one. The invariant to
  establish is *"only a definitive upstream verdict may be cached"* — asserted in a comment
  in one file and simply absent in the other.

### 3. `hyperwhisper-cloud/src/middleware/auth.ts:70-79` — a 429 from the license API is cached as a definitive "invalid license", and the limiter it trips is exhaustible by an unauthenticated attacker (CONFIRMED, executable repro)

- **Led here by:** the same dead-code audit as finding 2 — the bot's removal of the per-IP
  usage accumulator drew attention to what abuse controls actually remain.
- **Failure scenario:** The transient-failure guard is `>= 500` only, so a **429** falls
  through to `cacheLicense({isValid:false})` for an hour. Because the cloud service calls the
  license API server-to-server **without forwarding the client IP**, every Fly machine's
  validations share one rate-limit bucket keyed on the machine's egress IP. An
  unauthenticated attacker sending ~31 requests/minute of
  `GET /usage?account_key=<random>` — each a cache miss, each costing one upstream
  validation — exhausts the 30-per-minute bucket. Every *legitimate* cache-miss validation
  in that window then gets 429, is not `>= 500`, and is cached as invalid. Real paying
  customers receive 401 on `/transcribe` for an hour. No credentials required.
- **Trigger path:** `GET /usage?account_key=<anything>` (`src/index.ts:54`) or
  `POST /transcribe?account_key=<anything>` (`src/index.ts:45`).
- **Evidence:**
  ```ts
  // auth.ts:70-79
  if (response.status >= 500) { ...; return { isValid: false, credits: 0 }; }
  await cacheLicense(licenseKey, { isValid, credits, ... });
  ```
  The 429 producer is `nextjs/app/api/license/validate/route.ts:61-69`, keyed on
  `getClientIPFromHeaders(req.headers)`, with `Ratelimit.slidingWindow(30, "1 m")`
  (`nextjs/lib/rate-limit.ts:27-32`). The outbound call sends only `Content-Type`
  (`auth.ts:36-46`, `usage.ts:37-42`), so no client IP is forwarded.
- **Why not intentional:** the comment enumerates the 4xx cases it means to cache —
  *"revoked/not-found/malformed key → valid:false"* — all genuinely definitive. 429 is
  neither enumerated nor definitive. Compounding it, the only abuse control on the cloud
  side is `isIPBlocked()`, and **no code anywhere in the repo ever writes an
  `ip_blocked:<ip>` key** — a repo-wide grep finds only the single read in `redis.ts:36`,
  two log strings, and a comment. Nothing bounds the attacker's rate.
- **Repro (executed, passing):**
  ```
  outbound headers cloud->licensing : {"Content-Type":"application/json"}
  validateAuth during 429           : REJECTED 401
  cache entry written               : {"isValid":false,"credits":0,...}
  after burst subsides              : STILL REJECTED (1h)
  licensing API retried?            : NO
  HTTP 429 -> usage.ts cached: {"isValid":false,...} / auth.ts cached: {"isValid":false,...}
  HTTP 503 -> usage.ts cached: {"isValid":false,...} / auth.ts cached: null
  ```
  The last two lines are the clean discriminator: on a 503 the two files differ (finding 2);
  on a 429 **both** poison, because 429 is a 4xx and the guard is `>= 500`.
- **Note:** a second hunter reached this independently and pointed out that the trigger does
  not even require an attacker. The bucket is fleet-wide, so ~30 legitimate cache misses per
  minute across all machines — a deploy, a cache flush, or an ordinary evening peak — 429s the
  licensing API and locks out every user who missed cache in that window. The comment at
  `auth.ts:66-69` asserting that a 4xx "is a definitive verdict" is simply false for 429, and
  the licensing API's own 429 body contains `{valid:false, ...}`, making it indistinguishable
  from a real verdict by the `data.valid === true` test.
- **Suggested fix direction:** treat 429 as transient alongside 5xx, and forward the client
  IP so the limiter buckets per end user rather than per Fly machine. The deeper issue is
  that the block-list read has no writer — either wire up the accumulator or delete the
  check so the absent protection is not mistaken for present protection.

### 4. `hyperwhisper-cloud/src/providers/google-chirp.ts:730-745` — the inline duration estimator under-counts compressed audio by 2-4x, sending up to ~220s of audio into a path Google caps at ~60s, with no retry (CONFIRMED)

- **Led here by:** rank 4 — the only in-scope file with a dedicated `fix(cloud)` commit, and
  `selfOnly`, so any failure is a hard 502 with no fallback provider to absorb it.
- **Failure scenario:** `POST /transcribe`, `X-STT-Provider: google-chirp`,
  `Content-Type: audio/mpeg`, a 100-second 64 kbps voice MP3 (800,000 bytes).
  `estimateAudioSeconds(800_000, 'audio/mpeg')` divides by 16,000 B/s and reports **50s**;
  `50 <= 55` passes the gate; inline sync `recognize` receives 100s of audio; Google returns
  400 INVALID_ARGUMENT on its ~60s duration cap. There is no inline→batch retry, so the
  request 500s and the transcript is lost.
- **Trigger path:** `POST /transcribe` → `transcribeRoute` (`transcribe.ts:269`) →
  `transcribeWithGoogleChirp` → gate at `google-chirp.ts:131-134` → inline `recognize`.
- **Evidence:**
  ```ts
  // google-chirp.ts:34-37
  // Sync `recognize` enforces a ~60 s audio-duration cap ... Use 55 s as the
  // gate to leave headroom for the byte-rate estimator being conservative on
  // compressed audio.
  const INLINE_AUDIO_MAX_SECONDS = 55;
  // google-chirp.ts:739-743
  } else if (lower.includes('mp3') || lower.includes('mpeg')) { bytesPerSecond = 16_000; }
  else if (lower.includes('m4a') || lower.includes('mp4') || lower.includes('aac')) { bytesPerSecond = 16_000; }
  ```
  The gate admits `55 × 16_000 = 880_000` bytes of MP3/M4A.
- **Why not intentional:** the comment claims the estimator is "conservative on compressed
  audio"; it is the opposite for every compressed branch, contradicted three times by the
  project's own code. `constants.ts:11` sets the canonical encoded-audio rate at
  `BYTES_PER_MINUTE_ESTIMATE = 480_000` — **8,000 B/s, half** what Chirp assumes. The
  project's own macOS encoder emits 32 kbps mono (**4,000 B/s, a quarter**) with the comment
  "Speech doesn't need high bitrates" — so at the app's real output bitrate, 880,000 bytes is
  **220 seconds**, 3.7x the cap the gate exists to enforce. And `assemblyai.ts:391` solves the
  identical problem by refusing to trust a byte estimate on compressed containers at all.
  `google-chirp.ts` does not import the shared `estimateSecondsFromBytes`; it rolls a private
  table. Both the gate and the estimator date from the vendoring commit and `c45ad84` did not
  touch them. There are **zero tests** for this 745-line file.
- **Suggested fix direction:** gate inline on container type the way AssemblyAI does, or use
  the shared 8,000 B/s constant. The deeper invariant: there should be one byte→duration
  estimator in the service, not two that disagree by 2x.

### 5. `hyperwhisper-cloud/src/providers/google-chirp.ts:399` — every non-auth 4xx from Google surfaces as HTTP 500 instead of 400; Chirp is the only provider of eleven that does this (CONFIRMED)

- **Led here by:** the same rank-4 target.
- **Failure scenario:** Any Google 400 or 404 — including finding 4's over-long inline
  request, or a malformed BCP-47 `?language=` value which is passed straight through
  unvalidated at line 168 — is thrown as a plain `Error`. `transcribe.ts` classifies
  unrecognised `Error` types as non-retryable and returns **500 "Transcription failed"**,
  telling the client "server fault, retry" for a permanently-bad request.
- **Trigger path:** `POST /transcribe`, `X-STT-Provider: google-chirp`,
  `?language=not-a-real-code`.
- **Evidence:**
  ```ts
  // google-chirp.ts:393-399
  if (response.status === 429) { throw new ProviderUnavailableError(...); }
  if (response.status >= 500) { throw new ProviderUnavailableError(...); }
  throw new Error(`Google Chirp error: ${response.status}`);
  ```
- **Why not intentional:** `ProviderInputError` exists for exactly this case and is
  documented in `providers/types.ts:92-110`. **Deepgram, ElevenLabs, Groq, xAI, OpenAI,
  Gemini, Mistral, Soniox, AssemblyAI and Azure all use it — `google-chirp.ts` is the sole
  provider that neither imports nor throws it.** Had it been thrown, `transcribe.ts:622-633`
  would have returned a 400 with the upstream message; that branch's own comment says a
  misleading status "would have the client back off and retry the same bad request."
- **Suggested fix direction:** throw `ProviderInputError` on non-auth 4xx, matching the other
  ten providers.

### 6. `hyperwhisper-cloud/src/providers/google-chirp.ts:497` — one slow poll aborts an entire 300-second batch job, discarding work already paid for (CONFIRMED)

- **Led here by:** the same rank-4 target; the `c45ad84` fix message documents this file's
  timing-sensitivity but changed only the inline call.
- **Failure scenario:** A 4-minute recording routes to GCS+batch. At t≈200s one poll exceeds
  `BATCH_POLL_FETCH_TIMEOUT_MS = 8_000`. `fetchWithTimeout` converts the abort into a thrown
  `ProviderUnavailableError`; the poll loop's catch only recognises the token-expiry message,
  so everything else hits `throw error` and kills the job. The `finally` deletes the GCS
  object and cancels the operation, discarding ~200 seconds of transcription Google has
  already performed and billed. Chain length is 1, so the user waits 200 seconds for a 502
  and must re-upload.
- **Trigger path:** `POST /transcribe`, `X-STT-Provider: google-chirp`, any body large enough
  to route to batch (>1.76 MB WAV, or >880 KB MP3).
- **Evidence:** the transport-level transient is fatal at line 497 (`throw error`), while the
  HTTP-level transient is deliberately tolerated at lines 607-616
  (`if (response.status === 429 || response.status >= 500) { ...; return { done: false }; }`).
  `utils.ts:97-107` shows an 8s abort becomes `ProviderUnavailableError('timeout after 8000ms')`.
- **Why not intentional:** the `batch_poll_transient` branch proves the author intended the
  loop to survive transient failures within the 300s deadline; the transport case was simply
  never routed there. No comment addresses what a poll timeout should do.
- **Suggested fix direction:** route transport timeouts into the same "retry next tick" branch
  as 429/5xx, bounded by the existing 300s deadline.

### 7. `nextjs/src/lib/db-layer.ts:245-283` — concurrent internal-bundle grants mint 10,000 free credits per extra request (CONFIRMED)

- **Led here by:** rank 5 — the largest file in scope, and the file the bot deleted the
  Stripe idempotency helper from.
- **Failure scenario:** Two requests POST `/api/internal/grant-license` with the same email
  (a double-clicked claim button, or a client retry after timeout). Both execute
  `getAccountKeysByEmail` before either writes, both find no granted key, both call
  `provisionAccountKeyForEmail`, both resolve the **same** `userId`, both insert a distinct
  licence row, and both call `grantCreditLot` with `sourceId: license.id` — **two different
  source ids**, so the `(source_type, source_id)` unique constraint does not dedupe. One
  pooled wallet ends with **20,000 credits instead of 10,000** ($20 of cloud STT) and the
  person holds two live keys.
- **Trigger path:** `POST /api/internal/grant-license` (authenticated by `x-internal-secret`;
  the guard is `route.ts:31-38`, three awaits before the write, no transaction).
- **Evidence:** the stated invariant is a comment (`db-layer.ts:231-233`: *"only brand-new
  emails receive it"*), and the grant is `db-layer.ts:275-280`.
- **Why not intentional:** `idx_account_keys_email` is a **plain** index, not unique; the
  unique indexes are on `key`, `stripe_session_id` and `polar_license_key_id` only. There is
  no `db.transaction()` on this path and no advisory lock. The one constraint that would
  serialise the race — `user.email UNIQUE` — fires only for a brand-new email, so the window
  is open for anyone whose user row already exists (previously signed into the dashboard, or
  had a licence revoked/refunded).
- **Suggested fix direction:** add a partial unique index on `(email)` where
  `status = 'granted'`, or wrap read-and-mint in one transaction. The invariant is currently
  asserted only in prose.

### 8. `nextjs/src/lib/db-layer.ts:115` vs `:188` — licences are stored with the email verbatim but looked up lowercased, hiding paid balances and enabling a duplicate grant (CONFIRMED)

- **Led here by:** rank 5.
- **Failure scenario:** An admin grants a key to `Ray.Amjad@Gmail.com`. `getOrCreateUser`
  normalises and stores `ray.amjad@gmail.com` on the user row, but `insertAccountKey` writes
  the raw mixed-case string to `account_keys.email`. Two failures follow with no concurrency
  needed: (a) the customer signs into the portal and `customer.licensesWithCredits` calls
  `getAccountKeysByEmail(ctx.user.email.toLowerCase())`, matches nothing, and shows **zero
  licences and zero credits** despite owning a granted key with 5,000 credits; (b) the same
  address hits `/api/internal/grant-license`, which finds no granted key and mints a
  **second** licence plus another 10,000-credit bundle.
- **Trigger path:** tRPC `admin.customers.grant` (`server/api/routers/admin/customers.ts:214-222`,
  email passed raw) → tRPC `customer.licensesWithCredits`, or `POST /api/internal/grant-license`.
- **Evidence:** `db-layer.ts:115` writes `email: data.email,` while `db-layer.ts:188` reads
  `where: eq(accountKeys.email, email.toLowerCase())`.
- **Why not intentional:** every *other* writer normalises before calling in —
  `provisionAccountKeyForEmail` (246), `handleCreditMint` (`stripe-webhook.ts:359`),
  `handleLicensePurchase` (96), `importLicenseFromPolar` (`license-validation.ts:72`) — which
  is precisely the pattern showing the layer intends normalised storage without enforcing it.
  There is no `citext` column and no `lower(email)` expression index. The read paths also
  contradict each other: `searchAccountKeysByEmail` uses case-insensitive `ilike` (222) and
  `getGrantedEmails` lowercases on read (213), so the two ACS-facing endpoints disagree about
  whether the same customer has been granted.
- **Suggested fix direction:** normalise in `insertAccountKey` and add a `lower(email)`
  expression index. Note this is adjacent to the bot's deletion of `normalizeLicenseKey` —
  the bot was right that the *function* was dead, but the underlying normalisation
  inconsistency it hinted at is real, on a different column.

### 9. `nextjs/app/api/webhooks/stripe/route.ts:121-130` — a failed refund clawback is swallowed and returns 200, so the customer keeps both the credits and the cash (CONFIRMED)

- **Led here by:** rank 12 — wallet accounting re-derived twice in consecutive commits.
- **Failure scenario:** Unlike the grant path, which returns 500 so Stripe retries, the
  refund path catches *every* error, logs it, and falls through to `{ received: true }` — a
  200. Nothing durable records that the refund was seen, so a failed clawback is lost
  permanently: no retry, no queue, no reconciliation. Two concrete triggers. (a) The
  lock-order inversion in finding 11 aborts the refund transaction with a Postgres deadlock
  whenever a refund is processed while the same user is actively transcribing; the error is
  swallowed and Stripe never redelivers. (b) `stripe.checkout.sessions.list({ payment_intent })`
  at `stripe-webhook.ts:495-498` is a live network call — a Stripe 500 or timeout throws and
  is swallowed identically. Either way the customer receives a full cash refund and retains
  every credit.
- **Trigger path:** `POST /api/webhooks/stripe` with `event.type === "charge.refunded"`.
- **Evidence:**
  ```ts
  // route.ts:121-132
  if (event.type === "charge.refunded") {
      try { await handleChargeRefunded(charge, event.id); }
      catch (error) {
        console.error("Stripe webhook: Error processing refund:", error);
        // Don't return error status - log for manual review instead
        // This prevents infinite retries for non-transient failures
      }
  }
  return NextResponse.json({ received: true });
  ```
- **Why not intentional:** the comment's stated intent is to avoid retrying *non-transient*
  failures, but the implementation kills retries for transient ones too. The contrast sits in
  the same file — `handleLicensePurchase` and `handleCreditPurchase` errors *do* return 500
  (route.ts:84-87, :97-100) precisely so Stripe retries. There is no compensating mechanism:
  the refund path never writes a `stripe_processed_events` row (grep confirms the only writer
  is `db-layer.ts:419`), there is no reconciliation job, and `nextjs/tests/` contains no
  webhook tests at all.
- **Suggested fix direction:** distinguish transient from permanent failures and return 500
  on the former so Stripe's retry does the work. The deeper invariant: the refund path needs
  the same durable event record the grant path already has.

### 10. `nextjs/src/lib/db-layer.ts:469-471` — "grant does not exist" is reported as "duplicate", so an out-of-order refund is silently dropped and never reversed (CONFIRMED)

- **Led here by:** rank 12.
- **Failure scenario:** `refundCreditGrant` returns the same `{ status: "duplicate" }` for two
  opposite states: "already fully refunded" and "no grant row exists". The caller logs
  "already processed … skipping" and returns 200. Concretely: a customer buys $50 of credits
  (session `cs_1`); the endpoint is erroring, so `checkout.session.completed` fails and enters
  Stripe's retry backoff with no `credit_grants` row yet written. The customer requests a
  refund. `charge.refunded` is delivered — Stripe does not guarantee ordering, and a fresh
  event is attempted immediately while the earlier one sits in backoff. `refundCreditGrant`
  finds no row, returns `"duplicate"`, and the refund event is permanently consumed. Stripe
  then retries the original event, which succeeds and grants 50,000 credits. Net result: full
  cash refund **and** 50,000 live credits.
- **Trigger path:** `POST /api/webhooks/stripe`, `charge.refunded` → `handleChargeRefunded`
  → `handleCreditRefund` → `refundCreditGrant`.
- **Evidence:**
  ```ts
  // db-layer.ts:468-471
  const grant = target.rows[0];
  if (!grant) { return { status: "duplicate", refundedAmount: 0 }; }
  ```
  ```ts
  // stripe-webhook.ts:605-610
  if (result.status === "duplicate") {
    console.log(`Credit refund already processed for charge ${charge.id}, skipping`);
    return;
  }
  ```
- **Why not intentional:** the file's own doc comments assert an idempotency mechanism that
  does not exist — `stripe-webhook.ts:468-471` and `:574-577` both claim the deduction is
  "recorded in `stripe_processed_events` keyed by charge.id". It is not; nothing in the refund
  path writes that table. `handleCreditRefund` even accepts an `eventId` parameter
  (`stripe-webhook.ts:583`) that is **never referenced in its body** — the vestige of the guard
  the comments describe. Real idempotency is instead the `originalAmount - alreadyRefunded <= 0`
  arithmetic at `db-layer.ts:476-481`, which handles exact replays correctly but cannot
  distinguish "not granted yet". No unique constraint applies, because the row is absent.
- **Suggested fix direction:** return a distinct sentinel for "no grant found" and treat it as
  retryable (500) rather than terminal, so Stripe redelivers after the grant lands.

### 11. `hyperwhisper-cloud/src/routes/usage.ts:103` — `/usage` and `/transcribe` resolve the same query string to different accounts (CONFIRMED, executable repro, low severity)

- **Led here by:** rank 7 — the half-applied `rawQuery()` decoder fix.
- **Failure scenario:** `rawQuery` percent-decodes the parameter *name*; Hono's `c.req.query()`
  fast path does a byte-literal match and does not. So with the exact input
  `?account%5Fkey=HW-AAAA-BBBB-CCCC-DDDD&account_key=HW-2222-3333-4444-5555` (`%5F` is `_`),
  `/transcribe` authenticates and bills the first key while `/usage` reports the credit balance
  for the second. `ws-streaming-deepgram.ts:146` uses `url.searchParams.get()`, which does
  decode names, so it agrees with `/transcribe` — **`usage.ts` is the lone outlier of the three
  auth sites**.
- **Evidence:** `usage.ts:103` uses `c.req.query(...)`; `transcribe.ts:398` uses
  `rawQuery(c.req.url, ...)`; `query.ts:34` does `key = decodeURIComponent(rawKey)`.
- **Repro (executed, drives the real `usageRoute`):** `/usage` validated
  `HW-2222-3333-4444-5555` while `/transcribe` authenticated `HW-AAAA-BBBB-CCCC-DDDD` —
  `SAME ACCOUNT? false`.
- **Honest severity:** **low, and explicitly not an auth bypass.** Both keys are
  attacker-supplied, so there is no cross-tenant read and no privilege escalation. The real
  consequence is that the balance endpoint can be made to report a different account than the
  one being billed, and observability disagrees with auth.
- **Why not intentional:** `query.ts:10-11` justifies the asymmetry by reasoning only about
  `+` in parameter *values*; it is silent on the fact that `rawQuery` also decodes parameter
  *names* while Hono's fast path does not. That second divergence arrived in the same commit
  and is unaddressed by the justification.
- **Suggested fix direction:** use one decoder across all three auth sites.

### 12. `hyperwhisper-cloud/src/routes/transcribe.ts:605-611` — internal error strings, including environment-variable names, are echoed verbatim to any authenticated caller (PLAUSIBLE)

- **Led here by:** rank 2.
- **Failure scenario:** With `ASSEMBLYAI_API_KEY` unset or rotated out on a machine, any
  licensed caller sending `X-STT-Provider: assemblyai` receives
  `{"error":"Transcription failed","message":"ASSEMBLYAI_API_KEY not configured", ...}`.
  Cycling `X-STT-Provider` enumerates the backend's secret-configuration state one provider
  at a time. The 502 path at 650-651 additionally forwards up to 500 characters of raw
  upstream response body.
- **Trigger path:** `POST /transcribe` after auth and the credit check — a valid account key
  with ≥0.1 credits is the only precondition.
- **Evidence:** line 611 returns
  `errorResponse(500, 'Transcription failed', error instanceof Error ? error.message : ...)`,
  and `responses.ts:13-26` places that argument directly into the JSON body. The app's own
  global handler at `index.ts:64-75` forbids exactly this: *"never echo raw err.message to the
  client (it can contain env-var names, upstream provider bodies, request IDs)"* — but the
  route's early `return` bypasses `onError`, so the sanitiser never runs.
- **Unproven link:** whether an unset provider key is a *reachable* production state rather
  than a deploy-time invariant, and whether the disclosed strings meet the severity bar for a
  service whose callers are all paying licence holders. The mechanism is certain; the impact
  depends on operational posture I cannot settle statically. What would settle it: confirming
  any provider key is optional in the Fly deployment config.
- **Suggested fix direction:** route the non-classified branch through the same sanitiser as
  `onError`, returning an `error_id` instead of the message.

### 13. `nextjs/src/lib/db-layer.ts:455-466` / `:501-514` vs `:560-581` — lock-order inversion between refund and spend can deadlock (PLAUSIBLE, but see finding 9)

- **Led here by:** rank 5/12 — wallet accounting re-derived twice in consecutive commits.
- **Failure scenario:** An account holds grant `B` (expires sooner) and `P` (a Stripe pack,
  expires later). A transcription charge (`spendCreditGrantsByProvenance`) locks `B` first via
  `ORDER BY expires_at ASC ... FOR UPDATE`, then reaches for `P`. Concurrently a
  `charge.refunded` webhook (`refundCreditGrant`) locks `P` first, then reaches for `B` —
  because its drawdown hoists the refunded grant with `ORDER BY CASE WHEN id = ... THEN 0`.
  Postgres detects the cycle and aborts one transaction (40P01). If the spend loses,
  `app/api/license/credits/route.ts:120-126` returns 409 and the cloud side merely
  `console.warn`s — the usage charge is silently dropped and the transcription is free.
- **Unproven link:** whether the two transactions can realistically overlap in production —
  it needs a refund webhook concurrent with a transcription billing call on the same account.
  The lock orders genuinely differ in current code; the interleaving is a timing question I
  cannot settle statically. What would settle it: a concurrent integration test against a real
  Postgres, or production evidence of 40P01.
- **Note — two hunters reached this independently, and the second made the consequence worse.**
  The `db-layer` hunter found the inversion; the Stripe hunter arrived at the same lock orders
  from the refund side and identified it as the concrete trigger for finding 9. If the refund
  transaction loses the deadlock, the error is swallowed and Stripe never redelivers, so the
  outcome is not merely a dropped usage charge but a permanent credit leak. I am keeping the
  verdict at PLAUSIBLE because the interleaving itself remains unproven, but its severity if
  real is higher than a deadlock normally warrants.
- **Suggested fix direction:** acquire the account's grants in one consistent order (drop the
  `CASE` hoist and re-derive drain order in application code after locking).

### 14. `hyperwhisper-cloud/src/lib/utils.ts:42` — the rounding epsilon guard is too small above ~33 credits, overcharging 0.1 credits (PLAUSIBLE, executable repro)

- **Led here by:** rank 3 — the billing files the bot edited.
- **Failure scenario:** `Math.ceil((value - Number.EPSILON) * 10) / 10`. `Number.EPSILON` is
  the ULP at 1.0; at ~41 credits the ULP is 32x larger, so the guard cannot absorb the float
  residue from `usd / 0.001`. A 708-second AssemblyAI `universal-3-pro` transcription computes
  `0.0413 / 0.001 = 41.300000000000004` and bills **41.4** instead of 41.3.
- **Repro (executed):** swept 1-1800s across six provider rates —
  `assemblyai_u3p 7/1800 (0.4%)`, `deepgram 6/1800 (0.3%)`, `chirp 25/1800 (1.4%)` overcharged
  by exactly 0.1 credit; smallest affected charge 32.8 credits.
- **Unproven link:** severity only. The mechanism and the arithmetic are certain and
  deterministic; at $0.0001 per occurrence I would not ship a fix for this alone, and I am
  explicitly not presenting it as a headline. It is recorded because it is real and executable.
- **Suggested fix direction:** scale the epsilon to the magnitude
  (`value * Number.EPSILON * 4`) or do the arithmetic in integer tenths.

---

## Refuted (for the record)

These were investigated seriously and did not survive. Listing them is the point — it lets a
reader audit the hunt rather than only its successes.

- **`assemblyai.ts:96` `SYNC_TIMEOUT_MS = 15_000` governing a 120-second-clip path** — my own
  primed hypothesis, and the single most attractive-looking lead in the whole history (a human
  had just fixed exactly this bug in the sibling Chirp provider hours after the bot shipped
  this path). **REFUTED.** `fetchWithTimeout` converts the abort to `ProviderUnavailableError`;
  the sync function's catch is unconditional and returns `null`, falling back to async. All
  four claimed failure modes are covered. No body-consumption bug — `audio` is an `ArrayBuffer`
  and `new Blob([audio])` copies, so the async retry re-sends intact. The TS constant matches
  the documented Rust contract exactly. And the branch never admits 120s anyway: the WAV-only
  gate means the byte estimator over-states duration ~4x, so it fails closed. Worst case is a
  wasted 15s then a correct result — latency, not correctness.
- **`transcribe.ts:396-399` `??` vs `||` on `account_key`/`license_key`** — the miner flagged
  that `e290a2a` swapped `||` for `??`, which differ on the empty string. **REFUTED:**
  `rawQuery` returns `undefined` for an empty value (`query.ts:49`:
  `return value === '' ? undefined : value`), so the two operators are behaviourally identical
  here and `?account_key=&license_key=X` still falls through correctly.
- **All five of the bot's dead-code removals in `0fec986`** — the highest-prior-probability
  target in the hunt, since grep-verified deletion is a classic bug generator. **The bot was
  right on all five.** `git log -S` shows each symbol appears only in its introducing commit
  and the removal; none was ever called. Specifically: `hasProcessedStripeObject`'s removal is
  an *improvement* (idempotency is enforced atomically by
  `insert(...).onConflictDoNothing({target: stripeObjectId}).returning()` backed by
  `stripe_processed_events_object_id_unique`, and the deleted read-then-check was strictly
  weaker and TOCTOU-racy); `normalizeLicenseKey` was never called and every lookup path
  already trims; the `ip_daily:` quota helpers were never wired to any route while the
  `isIPBlocked` *check* survives at all five entry points; `corsPreflightResponse` is
  redundant against Hono's `cors()` plus an explicit `app.options('*')`;
  `LLM_PROVIDER_OUTPUT_CAPACITY_TOKENS` was a documentation table, and uncapped output is the
  deliberate, test-pinned policy (`llm-request-policy.test.ts:9-21`).
- **Removed npm dependencies still imported** — I checked all twelve packages dropped from
  `nextjs/package.json` by `0fec986` against every source, style and config file. Zero
  references. `node_modules` is stale but a clean install would not break.
- **Credit double-charge on provider fallback** — verified single-deduction: the loop breaks on
  first success and `deductCredits` is called exactly once, outside the loop, with the winning
  result. No per-attempt debit. No charge on any failure path.
- **Stripe webhook replay double-granting credits** — the headline hypothesis behind the bot's
  deleted `hasProcessedStripeObject`, and it is **soundly defended**. `grantCreditsForStripeEvent`
  (`db-layer.ts:414-443`) does insert-before-grant inside a single transaction and handles the
  empty-`returning()` case correctly (`if (!eventRow) { return null; }`). It is backed by two
  real unique indexes confirmed present in migration SQL and never dropped:
  `stripe_processed_events_object_id_unique` (`drizzle/0004_secret_marvel_apes.sql:2`) and the
  independent `credit_grants_source_unique` on `(source_type, source_id)`
  (`drizzle/0006_fat_husk.sql:15`). Both `checkout.session.completed` and
  `checkout.session.async_payment_succeeded` key on the same `session.id`, so only one grants.
  Ordering is correct, so a crash cannot mark an event processed without granting.
- **Stripe signature verification** — `route.ts:25` uses raw `req.text()` (not a parsed and
  re-stringified body), `constructEvent` runs at :46, a verification failure returns 400 at :52
  before any DB write, and duplicates return 200 at :132 rather than 500, so Stripe does not
  retry forever.
- **Refund driving a balance negative** — `refundCreditGrant` clamps `toClawback` at
  `getActiveGrantsTotal` and every per-row deduction is `Math.min(rowRemaining, toClawback)`.
- **Cross-grant refund clawback** — refunding a fully-spent pack draws from the user's other
  paid packs, which looks alarming but nets out correctly and is explicitly designed that way
  (`db-layer.ts:483-500`). Noted only that `server/api/routers/admin/customers.ts:329-331`
  carries a stale comment the implementation contradicts.
- **Partial refunds below the credit portion being a no-op** — **REFUTED-INTENTIONAL**, the
  documented policy at `stripe-webhook.ts:516-523`.
- **Non-atomic read-modify-write on the credit balance** — the classic wallet race. Refuted:
  every mutation is either a single atomic SQL expression
  (`balance = ${creditBalances.balance} + ${amount}` inside `onConflictDoUpdate`) or a per-row
  update whose value came from a `SELECT ... FOR UPDATE` in the same transaction. `db` is
  `drizzle-orm/node-postgres`, so `db.transaction()` is a real interactive transaction.
  `credit_balances` is a cache, never authoritative — both balance reads `SUM` the grants
  ledger, so cache drift never becomes spendable money.
- **Mass-mutation via a missing `where`** — all 8 mutating statements in `db-layer.ts` checked;
  every `update` has a `where`, the two upserts have targets, and there are **zero** `delete`
  calls in the file. No `sql.raw` anywhere; every template interpolates as a bind parameter.
- **Orphaned GCS objects on Chirp batch failure** — the `finally` always deletes, and the one
  genuine orphan window is explicitly covered by the documented bucket-lifecycle rule.
- **Chirp unbounded vocabulary** — `MAX_PHRASES` and `MAX_PHRASE_LEN` are genuinely enforced by
  `parsePhraseList`, and phrases are dropped entirely when adaptation is unsupported.
- **Chirp infinite poll loop** — `while (performance.now() < deadline)` with a sleep on every
  non-done iteration and a one-shot guard on the sleepless `continue`. Terminates.
- **`estimateAudioSecondsFromSize` under-reserving on sub-64 kbps encodes** (a real ~4x
  under-reservation) — **REFUTED-INTENTIONAL.** `transcribe.test.ts:19` ("does not
  under-estimate one minute of 64kbps audio") pins the assumption at exactly 64 kbps, which
  reads as a knowingly-chosen heuristic.
- **Sync billing at 3x the model's advertised rate** — **REFUTED-INTENTIONAL.**
  `stt-models.ts:65-79` documents sync as "not a selectable model; it's a routing decision".
  Flagged instead as a product question, not a defect.

## Coverage

- **Examined (8 targets):** ranks 1, 2, 3, 4, 5, 6, 7, 12 — `assemblyai.ts`, `transcribe.ts`,
  `cost-calculator.ts` + `stt-models.ts`, `google-chirp.ts` + `providers/utils.ts`,
  `db-layer.ts` + schema, `redis.ts` + `responses.ts`, `query.ts` + `usage.ts`,
  `stripe-webhook.ts`.
- **Ranked but not examined (8 targets):** ranks 8, 9, 10, 11, 14, 15, 17 — the LLM
  post-processing cluster and its five adapters, the guest-accessible credits checkout,
  the three `api/internal/*` routes, the credit UI components, the email templates, and the
  banner/layout cluster. Rank 13 (licence-key normalisation) was covered only partially, via
  the dead-code audit.
- **Ranked below the cut line (5):** `customer.ts`, `purchase-success/page.tsx`,
  `api/config/route.ts`, the schema index, and the navbar/landing pair.
- **Not ranked at all:** the rest of the codebase — plainly stated. Roughly **142 of the 210
  in-scope files were never opened by this hunt**, and the history-blind list in the coverage
  ledger names the load-bearing ones (all of cloud auth, the WebSocket streaming route, the
  assistant route, the 430-line blog webhook, and 9 of 11 STT providers). Nothing in this
  report should be read as evidence that those are clean.

## Self-assessment — where the strategy earned its keep, and where it wasted effort

**Where it earned its keep.** One signal did nearly all the work: **bot authorship**. Both
`percy-ai-bot[bot]` commits led to confirmed findings, and the highest-value finding
(finding 1) sits exactly where a bot wrote a new branch and a human patched the *sibling*
provider hours later without generalising. That fix-on-fresh-feature cluster is a genuine
targeting insight that a uniform read of 210 files would have reached far more slowly.
Ranks 1-5 produced 9 of the 14 findings, so the ranking did concentrate attention correctly.
Forcing "history is a map, HEAD is the territory" also paid: the file with the richest,
most seductive history (`google-chirp.ts`, the only dedicated `fix(cloud)` commit) yielded
three findings — but none of them were the bug the history was *about*.

**Where it wasted effort.** The documented scoring formula — fix-density × churn × size —
was close to worthless here and I should say so plainly. With 28 in-scope commits, no
reverts, a single dominant author, and a median of zero post-import touches per file, the
formula had no dynamic range. I kept the strategy alive by substituting bot-authorship and
post-import-touch signals, which is a real adaptation but also an admission that the stated
method did not survive contact with this repo. Anyone reading the scoreboard should discount
accordingly: on a repo with genuine multi-year history the formula would carry itself; here
it did not.

The clearest waste was my own primed hypothesis. The `SYNC_TIMEOUT_MS = 15_000` lead was the
single most attractive thing in the history — a human fixing precisely that bug class in a
sibling file hours after a bot shipped the path — and I pushed it hard into a hunter prompt.
It was cleanly refuted, and it deserved to be. Two more history-derived hypotheses (the
`??`/`||` swap and the `+`-in-key decoder divergence) were also refuted. So three of my
strongest *history-derived* hypotheses died, while the findings that survived came mostly
from reading the flagged files adversarially once the history had pointed at them. That is
the honest shape of this strategy's value: **history was good at choosing files and bad at
predicting bugs.**

Finally, the two findings I would rate most severe on the availability axis
(`usage.ts:44-52` and `auth.ts:70-79`) came from files with essentially **no git signal**.
A hunter reached them sideways while auditing the bot's deletions. That is luck compensating
for the structural blind spot named in the coverage ledger, and it should not be scored as
targeting success. A strategy that cannot see `middleware/auth.ts` — one commit ever, the
entire cloud auth surface — is missing something important by construction, and on this
codebase it only found those bugs by accident.
