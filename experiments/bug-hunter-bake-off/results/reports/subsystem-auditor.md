---
skill: subsystem-auditor
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 7 |
| PLAUSIBLE findings | 8 |
| Findings with an executable repro | 1 |
| Files opened (of 210 in scope) | 58 |
| Subagents spawned | 6 |
| Strategy came up dry? | no |

## Coverage ledger

**The subsystem I picked, and why.** I audited the **money-and-entitlement loop**: Stripe
billing → the credit ledger → license/device entitlement → the cloud-side credit debit.
Concretely that is 31 core files / 4,118 lines spanning both services, plus a 27-file
edge layer read for contract checking only. I picked it on stakes rather than size: it is
the only path in the pinned arena where a bug converts directly into money moving the
wrong way, and the repo's own `AGENTS.md` names it as the product's moat — *"HyperWhisper
Cloud is the paid moat: entitlement is enforced server-side. Never add a client-side
bypass, fake/test license key, or debug backdoor."* It is also the only subsystem in scope
that crosses a service boundary (the Fly.io cloud service debits the Vercel ledger over
HTTP), and cross-service seams are where a single-repo reader is weakest.

**What I therefore did not audit at all.** This is the important half of this ledger. Of
the 210 in-scope files, my audit set was 31. I did not audit, and this report says nothing
whatsoever about:

- The entire **transcription pipeline** — all 15 provider adapters (`google-chirp.ts` 745
  lines, `assemblyai.ts` 610, `soniox.ts`, `gemini.ts`, `azure-mai.ts`, …),
  `routes/transcribe.ts` (734 lines), `routes/post-process.ts`, `routes/assistant.ts`, and
  the Deepgram WebSocket streaming route. I opened four of these only where a money path
  ran through them; none was audited line-by-line.
- The **entire marketing site and web UI** — every `app/[locale]/**` page, all
  `components/**`, the legal pages, the blog, i18n/routing, `middleware.ts`, and the
  React dashboard clients (`CustomersClient.tsx` alone is 698 lines).
- The **tRPC admin surface** beyond the two mutations that touch credits — `admin/devices.ts`,
  `admin/stats.ts`, `download.ts`, `download-ip.ts`, `server/api/trpc.ts`.
- **Auth proper** — `src/lib/auth.ts`, the better-auth magic-link config, the session
  layer. I read `auth-license-key-plugin.ts` only as an edge caller.
- `lib/disposable_domains.ts` (5,093 lines — 16% of the arena's total line count by
  itself), the blog webhook, email templates, geolocation, and the appcast/download paths.

A reader must not read "7 confirmed findings" as "the rest of the codebase is clean." It
means one subsystem was examined closely and roughly 85% of the arena was never opened.

**What this strategy is structurally blind to on this codebase.** Three things:

1. **Bugs that live between subsystems I did not both include.** By construction I traced
   contracts outward from one core. A bug wholly inside the transcription pipeline, or one
   spanning i18n↔routing, is invisible to me no matter how severe.
2. **Anything requiring execution.** No Postgres, no Redis, no Stripe, and no env vars are
   available here. The ledger (`db-layer.ts`, 1,023 lines of money math) and the whole
   webhook path have **zero** automated coverage and could not be run. Every DB-level claim
   in this report is established by reading SQL and the Drizzle schema, not by observation.
   This is why only one finding carries an executable repro, and why several findings that
   are mechanically clear sit at PLAUSIBLE.
3. **Deliberateness checks.** The skill's refutation ladder leans on `git blame` to
   distinguish a bug from a decision. This repo's history is a **squashed 6-commit public
   release**, so blame proves nothing. I substituted the code's own comments and its test
   files, which is weaker — see the self-assessment.

**Execution note, stated plainly.** Phase 2 fanned out all five finder angles as required.
**Angle D (language/framework pitfalls) never returned** — it was starved by the 20-subagent
session cap shared across the ten hunters and was still mid-flight when I reported. So the
float/precision, Drizzle-arbiter, and Next.js-15-async-API classes are **under-covered**
here. Phase 3 spawned one verifier before the same cap blocked the rest; I verified the
remaining candidates inline myself rather than ship them unverified. Phase 4 (Prove) is
largely unexecutable for the reason in (2) above. All of this depresses this run's numbers
relative to what the strategy would produce with capacity, and I would rather say so than
present partial coverage as complete.

---

# Subsystem audit: Money & entitlement (deep)

Audited the cross-service money loop — Stripe billing, the credit-grant ledger, license and
device entitlement, and the cloud-side debit — across 31 core files in `nextjs/` and
`hyperwhisper-cloud/`. The headline result is that the **ledger itself is in good shape**:
its invariants are documented, its transactions are correct, and the audit's flashiest
candidate (a refund confiscating another pack) was **refuted** on the merits. The real
damage is concentrated at the **service seam** — the Redis license cache that the cloud
maintains and that nothing on the Next.js side ever invalidates — and in **paths that skip
billing entirely**. Overall risk read: no data-loss bug found, but several live revenue
leaks, at least one of which is unbounded and trivially triggerable by a user.

## Findings

### 1. hyperwhisper-cloud/src/routes/transcribe.ts:678 — a `no_speech` result skips billing entirely, and the balance never moves, so the free path is infinitely repeatable [CONFIRMED]
- **Failure**: A user uploads audio containing no speech. The provider still bills us for
  the audio minutes; we charge zero credits. Because no deduction occurs, the balance is
  unchanged and the preflight check passes identically next time — so this is not a
  one-shot rounding gift, it is unbounded free provider usage against a fixed balance.
- **Trigger**: `POST /transcribe` with `X-STT-Provider: deepgram` and a silent/music/noise
  file → `validateCredits` passes → `transcribeWithDeepgram` → `deepgram.ts:167` sees an
  empty transcript and returns `{ costUsd: 0, durationSeconds: 0, source: 'no_speech' }` →
  `transcribe.ts:675` sets `noSpeech = true` → line 678 skips `deductCredits` altogether.
  Replay indefinitely.
- **Evidence**: `transcribe.ts:675-678`:
  ```ts
  const noSpeech = result.source === 'no_speech';
  const creditsUsed = noSpeech ? 0 : creditsForCost(result.costUsd);

  if (!noSpeech) {
    deductCredits(
  ```
  and `deepgram.ts:167-180` returning `costUsd: 0, source: 'no_speech'` on an empty
  transcript. The unpriced premise — that Deepgram bills per submitted audio-minute
  regardless of whether words come back — is a provider billing fact I could not execute
  here, but it holds for Deepgram, Groq and ElevenLabs.
- **Repro**: could not reproduce — requires a live provider account and a Redis-backed
  license. The code path is fully readable and unambiguous.

### 2. hyperwhisper-cloud/src/middleware/credits.ts:74 — an authoritative 4xx from the ledger is discarded and the license cache is never corrected, giving a revoked key a full hour of free paid usage [CONFIRMED]
- **Failure**: After a refund revokes a license, the holder keeps running paid
  transcription for up to `LICENSE_CACHE_TTL_SECONDS` (3,600s) with **zero** credits
  debited. Every deduction returns 400 and is dropped; the cached entitlement is never
  corrected, so the loop repeats for every request in the window.
- **Trigger**: `charge.refunded` → `stripe-webhook.ts:565` `updateAccountKey(status:"revoked")`.
  I verified that **nothing on the Next.js side ever writes or invalidates the cloud's
  license cache** — `nextjs/lib/clients/redis.ts` and `lib/rate-limit.ts` are the only Redis
  consumers and both are rate-limiting only. So `license:<key>` still holds
  `{isValid:true, credits:N}`. Client loops `POST /transcribe` → `auth.ts:110` cache HIT →
  `validateCredits` passes on the stale N → provider billed → `deductCredits` →
  `recordLicenseUsage` → `POST /api/license/credits` → `app/api/license/credits/route.ts:107`
  returns 400 `License is ${license.status}` → `credits.ts:74` warns and returns.
- **Evidence**: `credits.ts:74-82` — `if (!response.ok) { console.warn(...); return; }`,
  with `cacheLicense` reached only on the success path at line 86. This is an internal
  inconsistency, not a design choice: `auth.ts:64-73` explicitly caches 4xx *because*
  "a 4xx ... is a definitive verdict from the licensing API (revoked/not-found/malformed
  key → valid:false)". The identical 4xx is thrown away here.
- **Repro**: could not reproduce — needs Redis + a live ledger.

### 3. nextjs/lib/services/stripe-webhook.ts:517 — `creditPortion` includes sales tax on the fee line, so the documented partial-refund flow never clears its own threshold and no credits are clawed back [CONFIRMED]
- **Failure**: A customer in any taxed jurisdiction is refunded the credit value in cash
  **and keeps every credit**. The log line reads like an intentional skip, so it does not
  look like a failure in production.
- **Trigger**: `/api/checkout/credits` builds a two-line-item session with
  `managed_payments: { enabled: true }` (`route.ts:195`) and a `tax_code` on both products
  (`route.ts:167`, `route.ts:180`), so Stripe adds tax on top. `charge.amount` is therefore
  tax-inclusive while the `fee_cents` metadata is the **untaxed** fee. The code's own
  comment states the intended operation is a *partial* refund of the credit value only,
  since "the 6% fee is a separate, non-refundable line item". That refund equals
  credit + tax-on-credit, but `creditPortion` equals credit + tax-on-credit + **tax-on-fee**
  — so the guard short-circuits and `handleCreditRefund` is never called.
- **Evidence**: `stripe-webhook.ts:514-523`:
  ```ts
  const feeCents = parseInt(checkoutSession.metadata?.fee_cents || "0", 10);
  const creditPortion = charge.amount - feeCents;
  if (charge.amount_refunded < creditPortion) {
  ```
- **Repro**: executable arithmetic, run against the real constants from
  `app/api/checkout/credits/validation.ts` (`CREDIT_FEE_RATE = 0.06`):
  ```
  $ node -e '...'
  no tax                 charge=1060 creditPortion=1000 policyRefund=1000 -> clawback runs? true
  UK/EU VAT 20%          charge=1272 creditPortion=1212 policyRefund=1200 -> clawback runs? false
  US sales tax 8.875%    charge=1154 creditPortion=1094 policyRefund=1089 -> clawback runs? false
  ```
  The untaxed case is correct, which is why this survived: the bug appears only once tax is
  in play. Note a full refund (`amount_refunded == charge.amount`) *does* clear the
  threshold, so severity depends on operators following the documented credit-only refund
  policy.

### 4. hyperwhisper-cloud/src/routes/usage.ts:48 — the balance endpoint caches a license as invalid on **any** non-2xx including 5xx, locking paying users out for an hour [CONFIRMED]
- **Failure**: One transient 500 from the Next.js license API during a routine balance poll
  poisons the shared cache entry with `{isValid:false, credits:0}` for a full hour. The user
  is then hard-401'd out of transcription, post-processing, assistant and streaming — not
  retried, not degraded — even though their license is fine and the API recovered seconds
  later.
- **Trigger**: `GET /usage?license_key=K` with no `force_refresh` → `usage.ts:128` →
  `validateLicenseAndGetCredits(K, false)` → cache miss → `POST /api/license/validate`
  returns 500 (that route's own catch at `validate/route.ts:132` returns 500 on any DB
  error) → `await response.json().catch(() => ({}))` yields `{}` → `isValid = false` →
  line 48 caches it with `ex: 3600`. Next `POST /transcribe` → `auth.ts:110` cache HIT →
  `!cached.isValid` → `invalidLicenseResponse()`. Both paths share the key
  `license:${licenseKey}` (`redis.ts:56`, `redis.ts:71`). Nothing clears it before TTL.
- **Evidence**: `usage.ts:44-52` calls `cacheLicense` with **no status check at all**. The
  sibling path implements exactly this guard and documents why, at `auth.ts:64-73`: *"A 5xx
  ... is a transient failure, not proof the license is invalid — caching it would lock a
  paying user out for the full LICENSE_CACHE_TTL_SECONDS."* Two sibling code paths, one
  honours the documented rule and one omits it.
- **Repro**: could not reproduce — needs Redis and a failing upstream.

### 5. nextjs/server/api/routers/admin/customers.ts:218 — the admin grant path stores a non-normalized email while every lookup lowercases, splitting one customer into two and double-granting credits [CONFIRMED]
- **Failure**: A license granted to `Bob@Co.com` is invisible to every email lookup in the
  system. The ACS claim flow then mints that person a **second** key and a second
  10,000-credit ($10) bundle onto the same pooled wallet. Support also cannot find the
  original key by email.
- **Trigger**: Admin `grant` mutation, input schema `z.object({ email: z.string().email() })`
  — zod's `.email()` validates but does **not** normalize. `const { email } = input` is
  passed straight to `insertAccountKey({ email, ... })`, so `account_keys.email` keeps its
  original casing. Every read goes through `getAccountKeysByEmail`, which lowercases the
  *query* (`db-layer.ts:188`: `eq(accountKeys.email, email.toLowerCase())`) but cannot
  lowercase the stored column. A later `POST /api/internal/grant-license` for `bob@co.com`
  finds no granted key at `grant-license/route.ts:32` and mints again.
- **Evidence**: `customers.ts:196` `z.string().email()`; `customers.ts:217-222`
  `insertAccountKey({ key: key!, email, userId: user.id, status: "granted" })` with no
  `.toLowerCase()`. Contrast `provisionAccountKeyForEmail` (`db-layer.ts:246`), which
  normalizes correctly — so the write paths disagree with each other.
- **Repro**: could not reproduce — needs a DB. The normalization asymmetry is a plain code
  fact readable from the two lines above.

### 6. nextjs/app/api/license/credits/route.ts:135 — the debit API reports the **requested** amount as `credits_deducted` even when it collected less, so an under-collection is invisible on both sides of the seam [CONFIRMED]
- **Failure**: When a user's real balance is below the actual cost, the ledger floors the
  spend at zero, the API replies **200** with `credits_deducted` equal to the amount that
  was *not* collected, and the cloud caches the result and moves on. There is no artifact
  anywhere — no error, no alert, no log discrepancy — that a shortfall occurred, so the
  unpaid provider cost is unrecoverable and undetectable after the fact.
- **Trigger**: Any debit larger than the remaining balance.
  `deductCreditBalance` (`db-layer.ts:626-629`) calls `spendCreditGrantsByProvenance`, which
  returns `{ balance, deductedAmount }`, and then **discards `deductedAmount`**, returning
  only `balance`. The route has no access to the real figure and echoes its own input.
- **Evidence**: `db-layer.ts:626-629`:
  ```ts
  export async function deductCreditBalance(userId: string, amount: number): Promise<number> {
    const result = await spendCreditGrantsByProvenance(userId, amount);
    return result.balance;
  }
  ```
  and `route.ts:135-138` returning `{ credits_remaining: newCredits, credits_deducted: amount }`
  where `amount` is the caller's request. `spendCreditGrantsByProvenance` genuinely
  under-deducts silently: its loop at `db-layer.ts:586-607` simply runs out of grants.
- **Repro**: could not reproduce end-to-end — needs a DB. The discarded return value is a
  plain code fact.

### 7. hyperwhisper-cloud/src/index.ts:82 — the shutdown drain (4s) is shorter than the license-API timeout (10s) it exists to protect, so the exact slow case it was written for is guaranteed to be killed [CONFIRMED]
- **Failure**: On every deploy or machine recycle, in-flight credit deductions whose
  license-API call is slower than 4s are killed mid-fetch. The user keeps the transcript,
  the provider bill is real, and the charge is silently dropped. The shutdown log reports
  the pending count as though those deductions had succeeded.
- **Trigger**: `fly deploy` → SIGTERM → `gracefulShutdown` → `drainPendingDeductions(4000)`
  → `credits.ts:112-115` `Promise.race([allSettled, timeout])` resolves via the 4s timeout
  while `performDeduction` is still awaiting a fetch armed with
  `AbortSignal.timeout(LICENSE_API_TIMEOUT_MS)` → `index.ts:99` `process.exit(0)`.
- **Evidence**: `index.ts:82` `const SHUTDOWN_DRAIN_MS = 4_000;` against
  `constants.ts:71` `export const LICENSE_API_TIMEOUT_MS = 10_000;`. The constant's own
  neighbouring comment says the 10s budget is sized for a Vercel cold start — precisely the
  case the 4s drain cannot cover. Separately, `drainPendingDeductions` returns
  `pendingCount` captured *before* the race, so the "drained" log overstates success, and it
  snapshots the Set once while the Hono server keeps accepting requests.
- **Repro**: not attempted — the constants comparison is the whole proof and is verifiable
  by reading the two lines.

### 8. nextjs/src/lib/db-layer.ts:489 — refunding an **expired** grant claws its full value out of the user's live, unexpired grants [PLAUSIBLE]
- **Failure**: If reachable, a customer who bought pack A, then pack B ~300 days later, and
  is refunded A after A has lapsed, loses **B** entirely: they paid $20, were refunded $10,
  consumed nothing, and hold 0 credits. Genuinely net-negative for the user.
- **Trigger**: `charge.refunded` → `handleCreditRefund` → `refundCreditGrant`. The target
  `SELECT ... FOR UPDATE` at `db-layer.ts:455-466` deliberately does **not** filter on
  expiry, so it finds the expired grant and computes `clawback = original - refunded` at
  full value. `getActiveGrantsTotal` then excludes the expired grant, so the clamp at line
  489 is the *other* grant's balance, and the drawdown at 501-514 draws entirely from it.
- **Evidence**: the expiry filter `ACTIVE_GRANT_EXPIRY` (`db-layer.ts:300`) is applied in
  `getActiveGrantsTotal` and the drawdown query but **not** in the target select. The
  comment at lines 494-500 claims *"Expired grants are skipped: they no longer back any
  spendable balance, so clawing them back would remove value that was never available"* —
  which is exactly what this path does not honour for the refunded grant itself.
- **Unproven link**: **reachability.** Grants carry a 365-day TTL
  (`CREDIT_GRANT_TTL_MS`, `db-layer.ts:373`) and Stripe will not refund a card charge after
  roughly 180 days, so neither the webhook path nor the admin path
  (`customers.ts:323 stripe.refunds.create`) may be able to reach an expired grant at all.
  Confirming this needs the actual refund window Stripe enforces for this account and
  whether any manual/API path can bypass it.
- **Repro**: could not reproduce — needs a DB and a time-shifted grant.

### 9. nextjs/src/lib/db-layer.ts:469 — `refundCreditGrant` reports "duplicate" when **no** grant matches, so a refund with a mismatched provenance key silently claws back nothing [PLAUSIBLE]
- **Failure**: A full cash refund is issued and the customer keeps 100% of the credits. The
  caller logs "already processed" and returns success, so nothing surfaces.
- **Trigger**: The admin refund mutation calls
  `refundCreditGrant({ sourceType: "license_bundle", sourceId: license.stripeSessionId })`,
  but a key minted through the credits checkout has its grant written with
  `sourceType: "stripe_credit_pack"`. The `(source_type, source_id)` select returns zero
  rows → line 469 returns `{ status: "duplicate", refundedAmount: 0 }` → the caller treats
  it as success. The same conflation also swallows an out-of-order webhook (refund arriving
  before its grant).
- **Evidence**: `db-layer.ts:468-471` — `const grant = target.rows[0]; if (!grant) { return
  { status: "duplicate", refundedAmount: 0 }; }`. "Not found" and "already refunded" are
  genuinely different states collapsed into one verdict.
- **Unproven link**: whether the admin refund path actually passes `license_bundle` for a
  credit-minted key. Finder E traced this to `customers.ts:331` but I could not
  independently confirm which `sourceType` reaches that call for each mint route.
- **Repro**: could not reproduce — needs a DB.

### 10. nextjs/src/lib/db-layer.ts:279 — the internal-bundle grant is keyed on a freshly generated uuid, so its uniqueness index can never dedupe and the $10 bundle can be re-minted [PLAUSIBLE]
- **Failure**: An email whose only key is revoked can re-run the claim flow and receive
  another 10,000 credits ($10) on the **same pooled wallet**, repeatable per cycle. This
  contradicts the function's own docstring: *"only brand-new emails receive it (an email
  that already has a granted key gets no top-up)"*.
- **Trigger**: `POST /api/internal/grant-license` with a valid secret for an email whose
  keys are all `status='revoked'` → `grant-license/route.ts:32` guards only on
  `existing.find(l => l.status === "granted")` and passes → `provisionAccountKeyForEmail` →
  `grantCreditLot({ sourceType: "internal_bundle", sourceId: license.id })` where
  `license.id` is a brand-new uuid, so `onConflictDoNothing` on `(source_type, source_id)`
  cannot fire.
- **Evidence**: `db-layer.ts:275-280`. The `UNIQUE (source_type, source_id)` index exists and
  is the intended dedupe, but a per-mint uuid makes it structurally unable to collide. A
  stable key (the normalized email) would dedupe correctly.
- **Unproven link**: whether the ACS claim flow can actually be re-driven for a revoked
  email, and whether revocation of an internal-bundle key occurs in practice. Finding #5 is
  the confirmed sibling of this same weakness reached via email casing instead.
- **Repro**: could not reproduce — needs a DB.

### 11. hyperwhisper-cloud/src/middleware/auth.ts:75 — a 429 from the ledger's own rate limiter is classified as a "definitive verdict" and cached as invalid for an hour [PLAUSIBLE]
- **Failure**: If the shared rate limiter trips, every license validated in that window is
  written to Redis as invalid for a full hour, hard-401'ing paying customers across all
  cloud endpoints.
- **Trigger**: `/api/license/validate` is protected by `licenseValidateRateLimiter`
  (`lib/rate-limit.ts`) at **30 requests per IP per minute**, returning 429
  (`validate/route.ts:62-67`). `auth.ts` only exempts `status >= 500` from caching, so a 429
  falls through to `cacheLicense({ isValid: false })` at line 75 with a 1-hour TTL.
- **Evidence**: the guard at `auth.ts:70` is `if (response.status >= 500)`, and the comment
  above it asserts *"A 4xx ... is a definitive verdict from the licensing API"*. A 429 is a
  4xx that is emphatically **not** a verdict about the license — it comes from the limiter,
  not the licensing logic. The classification is wrong on its face.
- **Unproven link**: whether 30 req/min is actually reached. The cloud only calls validate
  on a cache **miss**, so steady-state volume is low; the realistic trigger is a Redis
  outage or mass TTL expiry making every request miss at once, plus all Fly machines sharing
  an egress IP. I could not confirm the egress-IP shape or that `getClientIPFromHeaders`
  resolves to it.
- **Repro**: could not reproduce — needs Redis and load.

### 12. nextjs/src/lib/db-layer.ts:508 — refund and spend acquire `FOR UPDATE` row locks in inverted order, risking a deadlock whose loser is silently swallowed on either side [PLAUSIBLE]
- **Failure**: Postgres aborts one transaction with 40P01. If the refund loses, the webhook
  route returns 200 (see #15) and the clawback is lost permanently. If the spend loses, the
  route returns 409, `recordLicenseUsage` only warns, and a paid transcription is never
  billed. Either way the comment at lines 484-500 asserting that *"neither bundle-first nor
  pack-first ordering can leak money"* would not hold under concurrency.
- **Trigger**: T1 = `charge.refunded` → `refundCreditGrant` locks the target grant at line
  465, then re-locks the set with `CASE WHEN id = ${grant.id} THEN 0 ELSE 1` **ahead of**
  the `expires_at` ordering. T2 = `POST /api/license/credits` → `spendCreditGrantsByProvenance`
  locks the same rows in plain `expires_at ASC` order. For a user holding two grants these
  orders invert.
- **Evidence**: `db-layer.ts:508-513` (`ORDER BY CASE WHEN id = ... THEN 0 ELSE 1, expires_at
  ASC, ...`) versus `db-layer.ts:576-580` (`ORDER BY expires_at ASC, created_at ASC, id`).
- **Unproven link**: **the Postgres locking model.** Row locks are taken as rows are produced
  by the plan, and a sort node above the scan means rows are locked in *scan* order, not
  `ORDER BY` order. If both queries lock in index/scan order the inversion collapses
  entirely. Settling this needs `EXPLAIN` against the real schema and a live DB — neither
  available here. I am deliberately not inflating this to CONFIRMED on reasoning alone.
- **Repro**: could not reproduce — needs a live Postgres and two concurrent sessions.

### 13. hyperwhisper-cloud/src/middleware/credits.ts:23 — the preflight estimate assumes 64 kbps, so a low-bitrate upload reserves a fraction of the duration-billed cost it incurs [PLAUSIBLE]
- **Failure**: A user passes the credit check for far less than the work actually costs; the
  ledger then floors the shortfall at zero (#6) and reports success, so the business absorbs
  the difference silently.
- **Trigger**: `POST /transcribe` with a large, genuinely low-bitrate file (e.g. 16 kbps
  Opus). `estimateAudioSecondsFromSize` divides size by `BYTES_PER_MINUTE_ESTIMATE` —
  verified as `480_000`, commented "64kbps encoded audio" (`constants.ts:11`) — so a 16 kbps
  file's duration is underestimated by roughly 4×, and the provider bills the real duration.
- **Evidence**: `credits.ts:22-25`, `estimatedMinutes = sizeBytes / BYTES_PER_MINUTE_ESTIMATE`.
  The estimate is a fixed constant with no inspection of the actual container or bitrate.
- **Unproven link**: whether an upload path accepts such a file without an independent
  duration check, and the true magnitude against each provider's per-minute rate. Angle D,
  which would have quantified this, did not return.
- **Repro**: could not reproduce — needs a provider account.

### 14. nextjs/src/lib/license-validation.ts:92 — a failed Polar credit grant is swallowed, and the license row it just wrote makes the import path unreachable forever after [PLAUSIBLE]
- **Failure**: A paying Polar customer permanently lands a "granted" license with a **0**
  credit balance. Every later validation finds the row, skips the import entirely, and
  returns `valid:true, credits:0` — locked out of cloud transcription with no automatic
  recovery.
- **Trigger**: `POST /api/license/validate` → `checkLicenseKey` → `findAccountByKey` miss →
  `importLicenseFromPolar` → `insertAccountKey` commits → `grantCreditLot` throws (pool
  timeout on a cold serverless invocation) → caught and logged → returns `{success:true}`.
  On every later request `findAccountByKey` now hits, so the `if (!license)` fallback never
  fires and the only caller of `grantCreditLot` for `polar_bundle` is never reached again.
- **Evidence**: the catch at `license-validation.ts:92` swallows the grant failure while the
  function still reports success, leaving the insert committed and the grant missing.
- **Unproven link**: I did not independently re-read this file end-to-end (it came from
  finder B and finder C converging), so the exact line numbers and the shape of the catch
  should be re-checked before action.
- **Repro**: could not reproduce — needs a DB and Polar.

### 15. nextjs/app/api/webhooks/stripe/route.ts:127 — refund-handler errors are answered 200, so Stripe never retries and any transient failure loses the clawback permanently [PLAUSIBLE]
- **Failure**: The customer is refunded in cash and permanently keeps the credits. Stripe
  marks the event delivered; there is no retry and no alert beyond a log line. This is the
  amplifier that turns several other findings in this report from "retried" into
  "permanent".
- **Trigger**: Any throw inside `handleChargeRefunded` — a deadlock (#12), a
  `stripe.checkout.sessions.list` network error, a pooled-connection blip — propagates to
  the catch at line 125, which deliberately does not set an error status.
- **Evidence**: the handler catches and returns `{ received: true }` with a comment
  explaining it "prevents infinite retries", in contrast to the purchase paths earlier in
  the same file, which return 500 and are redelivered by Stripe.
- **Unproven link**: whether this asymmetry is deliberate for refunds specifically. The
  comment suggests intent, but the intent was plausibly "don't retry-storm on a *bad* event",
  not "never retry a *transient* failure" — the code cannot distinguish the two. That
  ambiguity is exactly what a PR author would have resolved in one sentence.
- **Repro**: could not reproduce — needs Stripe.

**Cut from the report**: 3 candidates, all lower-ranked duplicates of findings above —
`stripe-webhook.ts:57` (the idempotency short-circuit returns before the credit grant, so
replaying an event never repairs a failed grant; same root cause as #9's
"nothing-to-do reported as success" family), plus two restatements of the stale-cache
mechanism already covered by #2 and #4.

## Refuted (for the record)

- `nextjs/src/lib/db-layer.ts:489` — *"refunding a spent pack confiscates a different,
  un-refunded pack."* **Refuted on the accounting, not the mechanism.** The verifier
  walked the SQL and confirmed the second pack *is* drained, but the user ends exactly
  **net-neutral**, not net-negative: credits are pooled and fungible, so with P minted and
  C consumed the entitled post-refund balance is `(P − A) − C`, and the code computes
  `max(0, B − A)` — the entitled figure, floored at zero *in the user's favour*. In the
  scenario as posed the customer paid $20, consumed $10 of service, and got $10 back;
  a zero balance is correct. The alternative (clamping to the refunded grant's own
  remaining amount) yields $20 of value for $10 and is the "inverse money-loss bug" the
  code names explicitly at lines 449-454. The author documented the trade and chose the
  side that does not leak money. Only the *expired-grant* variant (#8) escapes this
  refutation, and its reachability is itself doubtful.
- `nextjs/lib/security/timing-safe-secret.ts:1-16` — no finding. The comparison rejects
  null/undefined before comparing (so a missing configured secret cannot make
  `undefined === undefined` pass), length-checks before `timingSafeEqual`, and uses the
  Node crypto primitive correctly. The length check leaks secret length, which is standard
  and not exploitable here.
- `hyperwhisper-cloud/src/lib/cost-calculator.ts` — no unpriced or underpriced model found.
  Angle E checked the pricing surface against `cost-calculator.test.ts`,
  `llm-dispatch.test.ts` and `stt-models.test.ts`: every routable STT model has a rate, and
  both post-processing and STT model resolution are allowlisted fail-closed. This was the
  most promising "silent revenue hole" hypothesis going in and it did not survive.

## Coverage

- **Fully read**: 31 core files (4,118 lines) — the complete audit set listed in the
  SCOPE_BLOCK, read top-to-bottom by Angle A and consulted by Angles B, C and E.
- **Skimmed only**: the 27-file edge layer, read for contract checking rather than
  line-by-line audit — the tRPC routers, dashboard components, `src/lib/auth.ts`,
  `middleware.ts`, `redis.ts`, `constants.ts`, `stt-models.ts`, the four cloud consumer
  routes, and the 9 test files in scope. Four of these (`transcribe.ts`, `deepgram.ts`,
  `admin/customers.ts`, `index.ts`) were read closely where a money path ran through them,
  and two findings (#1, #5) land in them.
- **Not examined**: ~152 of the 210 in-scope files — enumerated in the Coverage ledger
  above. In one line: the whole transcription pipeline, the entire marketing site and web
  UI, auth proper, and `disposable_domains.ts`.
- **Edge layer checked**: 27/27 files, contract-level only.
- **Angles run**: A (adversarial line-by-line), B (contract auditor), C (state & lifecycle),
  E (test-gap). **Angle D (language/framework pitfalls) did not return** — starved by the
  shared subagent cap. Float/precision on the `numeric(20,2)` columns, Drizzle
  arbiter-index semantics, and the Next.js 15 async-API class are correspondingly
  under-covered.

## Stats

finders: 5 launched / 4 returned · candidates: 27 · verified: 18 · confirmed: 7 ·
reproduced: 1 · refuted: 3 (+9 merged or cut as duplicates)
