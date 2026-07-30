---
skill: mutation-survivor-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 0 |
| PLAUSIBLE findings | 3 |
| Findings with an executable repro | 7 |
| Files opened (of 210 in scope) | 20 |
| Subagents spawned | 4 |
| Strategy came up dry? | no (on test gaps) / yes (on CONFIRMED live bugs) |

Read the two halves of that scorecard together. This skill produces two deliverables and
they came out very differently on this codebase: **zero CONFIRMED live bugs** (three
PLAUSIBLE) and **seven executed, proven test gaps** on money and auth control flow. The
"findings with an executable repro" count is 7 because every one of those gaps is backed by
a real mutation that was applied, run against the suite, observed to survive, and reverted —
three of them additionally have a drafted killing test proven to pass on clean code and fail
on the mutant. None of the three PLAUSIBLE bugs has a repro, which is exactly why none of
them is CONFIRMED.

Two of those three came from a subagent and both needed correction on the way in: one had
its headline ("zero-balance license = unlimited free transcription") refuted outright, and
the other had its severity materially overstated. That is recorded below rather than
quietly smoothed over, because uncritically relaying a subagent's framing is the main way a
report like this becomes untrustworthy.

## Coverage ledger

**What I examined.** I ran real measured line coverage (`bun test --coverage src`) over all
42 hyperwhisper-cloud source files, which is a mechanical read of the whole cloud tree and
is the basis for every targeting decision below. I then opened 14 files in depth:
`hyperwhisper-cloud/src/{middleware/credits.ts, middleware/auth.ts, lib/utils.ts,
lib/cost-calculator.ts, lib/cost-calculator.test.ts, lib/responses.ts, index.ts,
routes/transcribe.test.ts}` and `nextjs/{app/api/license/credits/route.ts,
app/api/license/credits/validation.ts, app/api/webhooks/stripe/route.ts,
lib/services/stripe-webhook.ts, src/lib/db-layer.ts (credit + refund regions),
lib/services/email.ts, tests/license-credits-validation.test.ts}`, plus directory-level
reconnaissance of `nextjs/app/api/` (21 routes) and `nextjs/app/[locale]/` while checking
for self-serve license-key recovery. Ten mutations were executed one at a time, each
reverted with `git checkout` before the next.

**What I deliberately skipped.** The 152-file `nextjs/` tree is almost entirely unexamined
by me directly. I sampled its money path only. I did not open `components/`, `contexts/`,
`config/`, `scripts/`, `i18n.ts`, `middleware.ts`, the 19 non-billing API routes, or any
page component. I skipped the STT provider adapters (`providers/*.ts`) except through the
coverage table, even though seven of them are at 0% function coverage, because a mutant in
an unexecuted file is a guaranteed trivial survivor and therefore carries no information.

**What this strategy is structurally blind to on this codebase.** Three things, and they
matter for the bake-off comparison:

1. **It cannot see bugs in code the suite never executes.** Mutation testing measures the
   suite. In `nextjs/`, 152 files are defended by 5 test files that only exercise four pure
   validation helpers, so essentially every mutant there survives by default. "Survives"
   degenerates from a signal into a tautology, and the lens goes blind exactly where the
   codebase is weakest. The strategies in this bake-off that read code adversarially
   without reference to tests should beat me across all of `nextjs/`.
2. **It finds gaps far more readily than bugs.** The skill's premise is that undefended
   lines are where live bugs hide. On this repo that premise did not pay out: the
   undefended lines I scrutinised turned out to be *correct* code that simply nothing
   checks. I confirmed zero live bugs.
3. **A region I did not examine is UNKNOWN, not clean.** Nothing in this report licenses a
   claim that any unexamined file is bug-free.

**Subagent starvation (affects comparability).** The session was pinned at its 20-agent
concurrency ceiling by the other nine hunters for most of my run; three spawn attempts were
rejected outright. I got 4 subagents where the skill's deep tier wants roughly 10-12 (a
mapper, one hunter per ranked region, one verifier per candidate bug), and of those 4 only
one returned usable output. The Phase 1 mapper never reported, so I built the defense map
myself from measured coverage instead of a ranked mapper table. The cloud transcribe hunter
never reported. The Phase 3 verifier never reported. Only the Next.js money-path hunter
delivered, and it did so after my mutation budget was spent, which is why its mutants are
labelled reasoned-only.

The honest reading: this run under-sampled the arena, and the parts of my process that
depend on parallelism — broad region coverage and independent verification — degraded to
me doing them serially and inline. The executed-mutation results are unaffected (those are
mechanical and I ran them all myself), but the *breadth* claims are weaker than a
properly parallelised run would support.

**Verification note.** I did not run a separate Phase 3 verifier agent per candidate bug,
because I produced no candidate bugs that survived my own bug-check. The two hypotheses I
did chase are recorded as refutations below.

---

# Mutation-Survivor Hunt — hyperwhisper-public — 2026-07-29

## Verdict summary

0 CONFIRMED live bugs (3 PLAUSIBLE, none with a failing repro test) · 7 executed test gaps
on money and auth control flow · effort: deep

## LIVE BUGS (ranked by severity)

None CONFIRMED. Three PLAUSIBLE, each below the confirmation bar for the reason stated in
its own entry. Findings 1 and 3 originated from a subagent and were re-verified (and in
both cases scaled back) by me; finding 2 is my own.

### 1. `nextjs/lib/services/stripe-webhook.ts:402-407` — a failed credit-mint email is never re-attempted (PLAUSIBLE, severity MEDIUM)

- Mechanism (every link verified in code): in `handleCreditPurchase`, STEP 2 calls
  `grantCreditsForStripeEvent(...)`, whose signature is
  `Promise<"processed" | "duplicate">` (`nextjs/src/lib/db-layer.ts:416`). Line 402 then
  early-returns on `"duplicate"` — **before** the email block at lines 438-449. The email
  itself cannot signal failure upward: `emailService.sendCreditMint` routes through
  `sendWithRetry`, which on exhausted retries or a non-retryable `ResendSendError` **returns
  `{ success: false, error }` rather than throwing** (`nextjs/lib/services/email.ts:235-240`).
  Line 447 only `console.error`s it. So the webhook returns 200, Stripe never retries, and a
  manual replay is a no-op because the second delivery takes the `"duplicate"` branch.
- Trigger path: `POST /api/webhooks/stripe` with `checkout.session.completed`,
  `metadata.purchase_type = "credits"`, `payment_status = "paid"`, a first-time buyer
  (`pooledIntoExisting` false), while Resend is degraded. Outcome: card charged, credits
  granted in the database, license key never emailed, and no webhook-driven recovery.
- Intent evidence that this is an oversight rather than a deliberate tradeoff: the sibling
  `handleLicensePurchase` does exactly the opposite on its duplicate path — it re-sends,
  with the comment "Still send email in case it failed before" (lines 48-58). The credit
  path's own comment ("don't re-send the email... keeps a re-delivery from emailing twice")
  shows the author was optimising against duplicate emails and did not consider the
  failed-first-send case.
- **Why only PLAUSIBLE, not CONFIRMED — and this corrects the subagent that raised it.**
  The subagent framed this as a customer permanently losing the key that is their wallet. I
  found a mitigation it missed: there is an authenticated user dashboard
  (`nextjs/app/[locale]/user/(authenticated)/dashboard/UserDashboardClient.tsx`) and a
  `purchase-success` page, so a buyer can plausibly self-serve the key by signing in. I have
  not verified that the dashboard reliably surfaces the key for a guest-checkout email, and
  I produced no executable repro — the Next.js side has no route-level test harness and my
  arena worktree was already torn down. Per this skill's own rule, a finding that resists a
  repro is downgraded rather than confirmed. What would settle it: sign in with a
  guest-checkout email and check whether the key is displayed.
- There is at least an audit trail: `safeLogSentEmail` records the failure with
  `status: "failed"`, so manual recovery is possible for anyone watching that table.

### 2. `hyperwhisper-cloud/src/middleware/credits.ts:106-115` — shutdown drain reports abandoned deductions as drained (PLAUSIBLE, severity LOW)

- Mechanism (real, and visible in the code): `drainPendingDeductions` captures
  `pendingCount = inFlightDeductions.size` at line 107, then races `Promise.allSettled`
  against a `setTimeout(timeoutMs)` at line 114, then returns the count it captured
  *before* the race. The return value is therefore the number of deductions that were
  pending, not the number that completed. When the timeout branch wins, the abandoned
  charges are counted as if they had been written.
- Consequence: `src/index.ts:95-98` logs `machine.shutdown_drained_deductions` with that
  count, so on a Fly machine recycle where the drain times out, the operator-facing log
  reports success for revenue that was silently dropped. The money is lost either way once
  the timeout fires — the defect is that the telemetry actively hides it, which is what
  would stop anyone noticing.
- **Why only PLAUSIBLE:** the unproven link is whether the timeout branch is ever actually
  reached in production. That depends on `SHUTDOWN_DRAIN_MS` versus real license-API
  latency under a Fly SIGTERM, which I cannot pin down from the repo — and I will not call
  it CONFIRMED without a trigger path I can construct. What would settle it: the configured
  `SHUTDOWN_DRAIN_MS` value against observed p99 latency of `POST /api/license/credits`.
- It is also possible the return value is intended to mean "how many were in flight", in
  which case the defect is in `index.ts`'s log wording rather than here. Either way the
  operator is told something untrue.

### 3. `nextjs/lib/services/stripe-webhook.ts:124-137` — a swallowed credit grant is never retried (PLAUSIBLE, severity MEDIUM)

- Mechanism (verified by reading, from a subagent lead): STEP 4b of `handleLicensePurchase`
  wraps `grantCreditLot({ ..., amount: 5000, sourceType: "license_bundle" })` in a
  try/catch that logs and deliberately does not rethrow — `// Don't throw - license was
  created, credits can be added later` (line 135). The assumption in that comment is not
  met by the code: on any later delivery of the same webhook, STEP 1's idempotency check
  (`findAccountByStripeSession(session.id)`, lines 48-57) resends the email and `return`s
  **before** STEP 4b is ever reached. So the grant is attempted exactly once, and a
  transient database failure at that instant permanently costs the customer the 5000
  credits bundled with their license.
- **Why only PLAUSIBLE:** two links are unproven. I cannot demonstrate that `grantCreditLot`
  realistically fails there (it is a DB write immediately after a successful insert in the
  same request), and "credits can be added later" may well refer to a manual ops procedure
  that exists outside this repository. What would settle it: whether any automated job
  reconciles licenses that have no `license_bundle` grant.
- Note the shape is identical to finding 1, in the same file: an error is deliberately
  swallowed to protect a more important write, and the compensating recovery the comment
  promises does not exist because the idempotency guard short-circuits before it. That
  recurring pattern is the most transferable thing in this report.

Three further hypotheses were chased to a refutation, recorded here so the negative results
are not silently dropped:

**REFUTED — Stripe license purchase lacks webhook idempotency.**
`nextjs/app/api/webhooks/stripe/route.ts:78` calls `handleLicensePurchase(session)` without
the `event.id` that its two sibling handlers (`handleCreditPurchase`,
`handleChargeRefunded`) both receive. That asymmetry looked like a missing idempotency key,
which would double-grant a license when Stripe retries or when both
`checkout.session.completed` and `checkout.session.async_payment_succeeded` fire for one
session. It is not a bug: `nextjs/lib/services/stripe-webhook.ts:48` dedupes on
`findAccountByStripeSession(session.id)` before doing any work, and the insert path
additionally catches Postgres `23505` unique violations for the concurrent-retry race.
`session.id` is stable across both event types, so it is the correct idempotency key.

**REFUTED — `isRecord` accepts arrays.**
`hyperwhisper-cloud/src/lib/utils.ts:8` is `typeof value === 'object' && value !== null`,
which is true for `[]` despite the doc comment saying "plain object values". Every one of
its 14 call sites is defensive-only: each immediately indexes a named key
(`json['usage']`, `message['content']`) and revalidates the result with `isGroqUsage` or
equivalent, so an array degrades to `undefined` rather than propagating. Real defect in the
guard's contract, no reachable wrong outcome. It remains a genuine test gap (zero direct
assertions on `isRecord`).

**REFUTED (headline) — "zero-balance license = unlimited free transcription".**
A subagent reported this as a live bug at `nextjs/src/lib/db-layer.ts:628`. The underlying
mechanism is real and I verified it: `spendCreditGrantsByProvenance` computes
`deductedAmount` (line 606) and returns it (line 616), but `deductCreditBalance` discards it
(line 628) and `POST /api/license/credits` then reports the *requested* amount as fact
(`credits_deducted: amount`, route.ts:135), with no `balance >= amount` pre-check on that
route. The escalation to unlimited free service does not hold, for two independent reasons:
(a) `credits_deducted` has **no functional consumer** — `hyperwhisper-cloud/src/middleware/credits.ts:84`
destructures it but line 85 reads only `credits_remaining`, which is the correctly
reconciled balance; and (b) the cloud service gates every request through `validateCredits`,
so once the balance floors at 0 the next request is rejected. The overdraft is bounded to a
single in-flight request, and the flooring is documented as deliberate at db-layer.ts:621.
What remains is a telemetry inaccuracy — the system cannot detect that it under-collected —
not a free-service hole. Recording this refutation explicitly because it is the kind of
finding that reads as catastrophic in a report and evaporates on verification.

## TEST GAPS (ranked by criticality of the undefended logic)

Every mutant below was **executed**, not reasoned about: applied with `perl -0pi`, run
against the full suite, observed, and reverted. Baseline was green first (cloud 138 pass /
nextjs 26 pass).

### 1. `hyperwhisper-cloud/src/middleware/credits.ts:144` — the credit deduction itself

- Surviving mutant: `await recordLicenseUsage(auth.identifier, creditsUsed, metadata);` -> `// MUTANT: deduction dropped` (**executed: survived**, 142 pass / 0 fail)
- Delete the only line that actually charges anyone and the entire suite stays green. Every
  transcription in production becomes free and CI reports success. This is the single most
  consequential undefended line I found.
- Suggested killing test: assert that `deductCredits` issues a POST to
  `/api/license/credits` with the expected `amount`, by installing a `globalThis.fetch` mock
  and awaiting the returned promise. The suite already uses this exact mocking style in
  `src/routes/transcribe.test.ts:71`.

### 2. `hyperwhisper-cloud/src/middleware/credits.ts:47` — the paywall

- Surviving mutant: `if (balance < estimatedCredits) {` -> `if (balance < 0) {` (**executed: survived**, 142 pass / 0 fail)
- The insufficient-credits gate can be removed entirely without a single test failing. A
  user at zero balance transcribes freely. Measured coverage corroborates it: line 48, the
  `insufficientCreditsResponse` return, is never taken by any test.
- Drafted killing test (proven): passes on clean code (4 pass), fails on the mutant.
  Content in "Drafted tests" below.

### 3. `hyperwhisper-cloud/src/middleware/auth.ts:113-115` — revoked-license rejection

- Surviving mutant: delete the `if (!cached.isValid) { return { ok: false, response: invalidLicenseResponse() }; }` block (**executed: survived**, 142 pass / 0 fail)
- A license the cache has already marked invalid would be accepted and served for the full
  cache TTL. This is an authentication bypass and nothing goes red. Measured coverage
  confirms line 114 is never executed.
- Drafted killing test (proven): passes on clean code (3 pass), fails on the mutant.

### 4. `hyperwhisper-cloud/src/lib/cost-calculator.ts:16` + `:193-197` — Deepgram is billed but never asserted

- Surviving mutant: `const DEEPGRAM_COST_PER_AUDIO_MINUTE = 0.0055;` -> `0.0099` (**executed: survived**, 138 pass / 0 fail)
- An 80% price error on the default STT provider ships green. `cost-calculator.test.ts`
  imports 8 cost functions and asserts Mistral, Soniox, ElevenLabs, AssemblyAI, OpenAI,
  Gemini and Groq rates — but never imports `computeDeepgramTranscriptionCost`,
  `computeXaiTranscriptionCost`, `computeAzureMaiTranscriptionCost` or
  `computeGoogleChirpTranscriptionCost`, nor any of the seven LLM chat-cost functions.
  This is the archetypal mutation-testing result: the file reads at 79.77% line coverage
  and looks well tested, but the covered lines are executed incidentally and never asserted.
- Drafted killing test (proven): passes on clean code (4 pass), fails on the mutant.

### 5. `hyperwhisper-cloud/src/middleware/auth.ts:70` — transient-5xx fail-open boundary

- Surviving mutant: `if (response.status >= 500) {` -> `if (response.status > 500) {` (**executed: survived**, 142 pass / 0 fail)
- The surrounding eight-line comment states a deliberate invariant: a 5xx is transient and
  must NOT be cached, because caching it would lock a paying user out for the full
  `LICENSE_CACHE_TTL_SECONDS`. The off-by-one makes a bare `500` fall through to
  `cacheLicense(... isValid: false ...)` and does exactly the harm the comment warns about.
  Deliberate, load-bearing, carefully documented logic with zero automated defense.
- Suggested killing test: mock the license API to return 500, assert `cacheLicense` was not
  called; return 400, assert it was.

### 6. `hyperwhisper-cloud/src/middleware/credits.ts:114` — SIGTERM deduction drain

- Surviving mutant: `await Promise.race([allSettled, timeout]);` -> `// MUTANT: drain removed` (**executed: survived**, 138 pass / 0 fail)
- This drain was added deliberately (see the comment at lines 99-103) because call sites
  fire `deductCredits()` without awaiting, so a Fly machine recycle between response flush
  and the license write silently drops the charge. The safety net can be removed without a
  test failing. Lines 106-114 are entirely unexecuted per measured coverage.
- This is the same function as PLAUSIBLE finding 1 above: the safety net is both undefended
  and arguably mis-reporting its own success.
- Suggested killing test: register a slow deduction, call `drainPendingDeductions` with a
  generous timeout, assert the deduction completed before the promise resolved.

### 7. `hyperwhisper-cloud/src/middleware/auth.ts:102-105` — the "license required" gate

- Surviving mutant: delete the `if (!licenseKey) { console.log('[Auth] No license_key provided'); return { ok: false, response: licenseRequiredResponse() }; }` block (**executed: survived**, 138 pass / 0 fail)
- Taken together with gap 3, this means **all three** of `validateAuth`'s rejection paths —
  no key at all, a cached-invalid key, and an API-rejected key — can each be deleted
  individually without a single test failing. The comment directly above this block states
  the product invariant ("HyperWhisper Cloud is licensed-only... there is no
  anonymous/trial path"), and nothing enforces it mechanically.
- The drafted `auth-rejection.test.ts` below already closes this one: its first case asserts
  a 401 for a keyless request.

## TEST GAPS — reasoned-only (subagent, NOT executed)

These arrived from the Next.js money-path hunter after my 10-mutation budget was spent and
the arena worktree had been torn down. **None were executed**, and they must not be read
with the same confidence as the seven above. That said, the reason they survive is not in
dispute and is cheap to state: no test in `nextjs/tests/` imports `db-layer.ts`,
`stripe-webhook.ts`, or either `route.ts` — the two credit test files import only from
`validation.ts`. So every mutant in those files survives by construction, which is exactly
the degenerate case flagged in the coverage ledger: in `nextjs/`, "the mutant survived"
carries almost no information because essentially nothing is defended.

Exact mutants recorded for whoever picks this up:

| file:line | current text | mutant |
|---|---|---|
| `nextjs/src/lib/db-layer.ts:591` | `const deduction = Math.min(grantRemaining, remainingToDeduct);` | `Math.min` -> `Math.max` |
| `nextjs/src/lib/db-layer.ts:478` | `const clawback = originalAmount - alreadyRefunded;` | swap operands |
| `nextjs/src/lib/db-layer.ts:479` | `if (clawback <= 0) {` | `<=` -> `<` |
| `nextjs/lib/services/stripe-webhook.ts:518` | `if (charge.amount_refunded < creditPortion) {` | `<` -> `<=` |

`db-layer.ts:479` is worth singling out: per the subagent that line is the *entire* refund
idempotency mechanism, because `refundCreditGrant` never writes `stripe_processed_events`
despite the doc comment at `stripe-webhook.ts:469-471` claiming the operation is keyed on
`charge.id`, and the `eventId` threaded into `handleCreditRefund` is never used. I did not
independently verify that, so treat it as a lead, not a finding.

## Executed-mutation ledger (10 of 10 used)

The kills matter as much as the survivors: they are the positive controls proving the
harness can detect a killed mutant, which is what makes the seven "survived" verdicts
trustworthy rather than an artifact of a broken test command.

| # | Target | Mutant | Result |
|---|---|---|---|
| 1 | `cost-calculator.ts:16` | Deepgram rate `0.0055` -> `0.0099` | **survived** |
| 2 | `credits.ts:47` | `balance < estimatedCredits` -> `balance < 0` | **survived** |
| 3 | `auth.ts:113` | delete cached-invalid rejection | **survived** |
| 4 | `auth.ts:70` | `>= 500` -> `> 500` | **survived** |
| 5 | `credits.ts:144` | drop `recordLicenseUsage` call | **survived** |
| 6 | `nextjs .../license/credits/validation.ts:14` | `amount > MAX` -> `amount >= MAX` | KILLED (negative control) |
| 7 | `cost-calculator.ts:168` | `USD_PER_CREDIT` `0.001` -> `0.0005` | KILLED |
| 8 | `credits.ts:114` | remove shutdown drain | **survived** |
| 9 | `utils.ts:42` | `Math.ceil` -> `Math.floor` in `roundUpToTenth` | KILLED |
| 10 | `auth.ts:102` | delete the `if (!licenseKey)` gate | **survived** |

Final tally: **7 survived, 3 killed.**

The three kills concentrate in one place, and that is the most interesting structural
result of this hunt: mutants 7 and 9 were both caught by hard-coded credit literals in the
**AssemblyAI preflight reservation** block of `src/routes/transcribe.test.ts`, and mutant 6
by the pure-validator tests in `nextjs/tests/`. So the money **arithmetic** is genuinely
defended, by a small number of tests that assert literal expected values. The money
**control flow** — the gate that rejects broke users, the call that charges them, the check
that rejects revoked licenses, the drain that protects in-flight charges — is not defended
at all. A codebase can have respectable coverage numbers and still have every one of its
enforcement points removable without CI noticing.

One near miss worth recording: `src/routes/transcribe.test.ts:12` and `:22` compute their
expected values by calling `creditsForCost(...)` — the function under test — rather than
asserting a literal. Those assertions are tautological and cannot fail under a rate change.
Mutant 7 was killed by a *different* test that does use a literal; had that AssemblyAI
block not existed, halving the credit rate and doubling every customer's bill would have
shipped green.

## Coverage — what this hunt did and did NOT examine

- **Regions examined:** `hyperwhisper-cloud/src/middleware/` (both files, fully),
  `src/lib/{utils,cost-calculator,responses}.ts`, `src/index.ts` shutdown path, and the
  Next.js credit/Stripe money path (mine plus the subagent's).
- **Regions dispatched but NOT covered:** the cloud transcribe/usage/post-process hunter
  (`routes/transcribe.ts` 734 lines, `routes/usage.ts`, `routes/post-process.ts` — which has
  no test file at all, `providers/utils.ts`, `lib/text-processing.ts`) never returned, even
  after I messaged it for partial results. **That region is UNEXAMINED**, and it is a
  significant hole: it is where provider fallback ordering and the reservation-versus-actual
  charge logic live, i.e. the most plausible remaining home for a real billing bug. The
  independent verifier I spawned for the mint-email finding also stalled, so I verified its
  two decisive facts myself and applied this skill's downgrade rule rather than claim a
  confirmation I could not independently corroborate.
- **Unmapped by Phase 1:** the mapper subagent never returned. The defense map used was
  built from measured `bun test --coverage` output rather than a ranked mapper table, so
  the `nextjs/` half of the arena was ranked by my own reading of the API route list rather
  than systematically. Unmapped in practice: all of `nextjs/components/`, `contexts/`,
  `config/`, `scripts/`, `i18n.ts`, `middleware.ts`, and 19 of the 21 API routes.
- **Real mutations executed:** 10 of 10 budgeted (7 survived, 3 killed). Nothing in the
  TEST GAPS section is reasoned-only; every one was executed.
- **Coverage method:** **measured** for `hyperwhisper-cloud` (`bun test --coverage src`,
  57.59% funcs / 52.47% lines across 42 files). For `nextjs`, no coverage instrumentation
  was run; defense was assessed by reading the 5 test files and tracing their imports.

An unexamined region is UNKNOWN, not clean.

## Drafted tests

These were written and verified inside the isolated worktree and are reproduced here rather
than written into the shared checkout, because the orchestrator required the main tree to be
left untouched. Each was proven in both directions: passes against current code, fails
against the recorded mutant.

`hyperwhisper-cloud/src/middleware/credits-gate.test.ts` (4 pass clean; 2 fail under mutant 2):

```ts
import { describe, expect, test } from 'bun:test';
import type { AuthContext } from './auth';
import { validateCredits } from './credits';

const auth = (credits: number): AuthContext => ({
  identifier: 'HW-TEST-KEY',
  credits,
  licenseKey: 'HW-TEST-KEY',
});

describe('validateCredits gates on balance', () => {
  test('rejects with 402 when the balance is below the estimate', async () => {
    const result = await validateCredits(auth(0.5), 2.0, '127.0.0.1');
    expect(result.ok).toBe(false);
    if (result.ok) throw new Error('unreachable');
    expect(result.response.status).toBe(402);
  });

  test('rejects a zero balance', async () => {
    const result = await validateCredits(auth(0), 0.1, '127.0.0.1');
    expect(result.ok).toBe(false);
  });

  test('admits an exactly-sufficient balance (boundary is <, not <=)', async () => {
    const result = await validateCredits(auth(2.0), 2.0, '127.0.0.1');
    expect(result.ok).toBe(true);
  });

  test('admits a balance above the estimate', async () => {
    const result = await validateCredits(auth(10), 2.0, '127.0.0.1');
    expect(result.ok).toBe(true);
  });
});
```

`hyperwhisper-cloud/src/middleware/auth-rejection.test.ts` (3 pass clean; 1 fail under mutant 3):

```ts
import { beforeEach, describe, expect, mock, test } from 'bun:test';

let cached: { isValid: boolean; credits: number; cachedAt: string } | null = null;

mock.module('../lib/redis', () => ({
  getCachedLicense: async () => cached,
  cacheLicense: async () => {},
}));

const { validateAuth } = await import('./auth');

describe('validateAuth rejects bad licenses', () => {
  beforeEach(() => { cached = null; });

  test('rejects a request with no license key', async () => {
    const result = await validateAuth({});
    expect(result.ok).toBe(false);
    if (result.ok) throw new Error('unreachable');
    expect(result.response.status).toBe(401);
  });

  test('rejects a license the cache says is invalid', async () => {
    cached = { isValid: false, credits: 500, cachedAt: new Date().toISOString() };
    const result = await validateAuth({ licenseKey: 'HW-REVOKED-KEY-0001' });
    expect(result.ok).toBe(false);
  });

  test('admits a license the cache says is valid, carrying its balance', async () => {
    cached = { isValid: true, credits: 42.5, cachedAt: new Date().toISOString() };
    const result = await validateAuth({ licenseKey: 'HW-GOOD-KEY-0001' });
    expect(result.ok).toBe(true);
    if (!result.ok) throw new Error('unreachable');
    expect(result.value.credits).toBe(42.5);
  });
});
```

`hyperwhisper-cloud/src/lib/cost-calculator-pricing-guard.test.ts` (4 pass clean; 1 fail under mutant 1):

```ts
import { describe, expect, test } from 'bun:test';
import {
  computeAzureMaiTranscriptionCost,
  computeDeepgramTranscriptionCost,
  computeGoogleChirpTranscriptionCost,
  computeXaiTranscriptionCost,
} from './cost-calculator';

describe('duration-billed STT pricing constants are pinned', () => {
  test('Deepgram nova-3 bills $0.0055/min', () => {
    expect(computeDeepgramTranscriptionCost(60)).toBe(0.0055);
    expect(computeDeepgramTranscriptionCost(600)).toBe(0.055);
  });

  test('xAI Grok STT bills $0.10/hr', () => {
    expect(computeXaiTranscriptionCost(3600)).toBe(0.1);
    expect(computeXaiTranscriptionCost(60)).toBe(0.001667);
  });

  test('Azure MAI-Transcribe bills $0.006/min', () => {
    expect(computeAzureMaiTranscriptionCost(60)).toBe(0.006);
  });

  test('Google Chirp 3 bills $0.016/min', () => {
    expect(computeGoogleChirpTranscriptionCost(60)).toBe(0.016);
  });
});
```

## Repo hygiene

All mutation work was done in an isolated git worktree at
`/private/tmp/.../scratchpad/mutation-arena`, never in the shared checkout. Every mutation
was reverted with `git checkout -- <file>` before the next one was applied; the worktree
showed zero modified tracked files at the end, and it has since been removed and pruned.

`git status --porcelain` in the MAIN checkout (`/Users/ray/Desktop/hyperwhisper-public`):

```
?? .playwright-mcp/
?? bug-hunt/
```

Both untracked entries pre-date this hunt and belong to the bake-off harness, not to me. I
added no files to the main tree apart from this report. The three drafted tests were
deliberately NOT written into the shared checkout; their full content is inlined above so
they can be committed by hand.
