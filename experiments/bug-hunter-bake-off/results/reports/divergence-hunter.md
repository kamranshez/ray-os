---
skill: divergence-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 2 |
| PLAUSIBLE findings | 1 |
| Findings with an executable repro | 1 |
| Files opened (of 210 in scope) | 34 |
| Subagents spawned | 5 |
| Strategy came up dry? | no |

## Coverage ledger

**What I examined.** I drove twin discovery from two signals rather than one: a structural
sweep of the obvious twin families, and — more productively — the git history, which on this
repo names its own twin sets out loud. Commits `e76f053` (license key → Account Key rename),
`28de2ec` ("Unify LLM post-processing completion policy"), `c45ad84` (a timeout fix applied to
exactly one provider), and `d92838d` (a sync fast path added to exactly one provider) each
either created a twin family or modified one member of an existing one.

Twin sets I personally diffed to a conclusion (10):

1. `CREDITS_PER_MINUTE` across the two services and the admin UI — **DRIFT, proven** (Finding 1).
2. Preflight credit estimate vs. the credit→minutes conversion in the 402 body — **DRIFT** (Findings 2, 3).
3. `api/account/{activate,deactivate,validate,credits}` vs `api/license/*` — **no drift**, structurally impossible: all four `account/*` files are pure `export { POST } from "../../license/..."` re-exports.
4. The 4 email templates (`credit-mint`, `credit-topup`, `license`, `welcome`) — **no drift**: all four pre-escape the same two variables via `escapeHtml` and interpolate them identically; `data.customerEmail` is unescaped in all four alike (a uniform shared risk, not a divergence).
5. Chirp's 45 s inline timeout vs AssemblyAI's 15 s sync timeout — **INTENTIONAL**, see refuted appendix.
6. The 7 LLM providers vs the unified completion gate — **no drift**: the gate is applied centrally at `routes/post-process.ts:185,215`, not per provider, so the two providers that commit `28de2ec` skipped are not bypassing it.
7. Flat-rate credit reservation vs per-provider reservation — **REFUTED, unreachable** (dead code; appendix).
8. `checkout/credits/validation.ts` vs `license/credits/validation.ts` — **not twins**: one validates a purchase in dollars, the other a deduction in credits. Different concepts that happen to share a filename.
9. Credit precision across the tree seam (cloud emits, nextjs validates at 2 dp) — **no drift**: `roundUpToTenth` with a `Math.max(0.1, …)` floor guarantees 1 dp, inside the nextjs `CREDIT_BALANCE_SCALE = 2` limit.
10. `durationSeconds` (the billing input) across all 11 STT providers — **no drift**: every provider references it; no provider silently reports zero duration.

**What I deliberately skipped, and why.** Rate-limiting and auth-check placement across the 23
routes: `license/deactivate` has no rate limiter while its siblings do, but it is a pure stub
that touches no DB and makes no outbound call, so there is nothing to amplify. Not a finding.
The locale/i18n constant duplication (`i18n.ts` / `src/i18n/locales.ts` / `middleware.ts`) I did
not reach.

**What did not happen, and it matters.** I spawned five subagents — three twin-discovery agents
(nextjs API surface, cloud providers, cross-tree seams) and two comparators (LLM provider
termination metadata, credit-rate verification). **Only one returned within the run**: the
credit-rate verifier, which materially strengthened Finding 1 by tracing the actual default STT
provider (deepgram, 5.5 credits/min) and showing the portal's stated premise is false — a fact I
had not established myself. The three discovery agents and the LLM comparator never came back,
and a sixth comparator was refused outright when the session hit its 20-subagent concurrency
ceiling with ten hunters competing for the same pool. So the parallel fan-out this skill is built
around largely did not execute, and the rest of the findings came from my own sequential
reading. The three
areas I handed off and never got back — a systematic odd-one-out sweep of all 23 API routes, the
17-provider interface conformance diff, and the exhaustive cross-tree constant sweep — are
**uncovered**, not clean. In particular the provider family is the single richest twin set on
this codebase and I only sampled it (timeouts, duration reporting); nobody diffed retry policy,
error mapping, or response parsing across all 17.

**What this strategy is structurally blind to on this codebase.** Divergence hunting cannot see
a bug that both twins share, and this repo makes that limitation bite harder than usual: the
`account/*` routes are re-exports and the completion gate is centralised, meaning the author has
already deduplicated most of the places where copies could drift. Where one copy genuinely
exists, I have no oracle at all. It is also blind by construction to the desktop-client contract
(Swift/C# out of scope) and to the Rust core — `assemblyai.ts:93-95` explicitly says its
`SYNC_TIMEOUT_MS` must be kept in sync with `shared-core-rs`, a twin I am forbidden to open, so I
cannot tell whether those two have drifted. That is a real blind spot on a real twin, not a
hypothetical one.

**Honest read on file count.** 34 files opened, but "opened" is uneven: roughly a dozen were read
in full, the rest were ripgrep-level reads of the specific lines a twin comparison needed. 34 of
210 is 16% of the arena. Nothing below should be read as evidence about the other 84%.

## Findings

### [1] The web dashboard tells users they have 3.8x more transcription minutes than the app does — PROVEN

- **Wrong copy:** `nextjs/server/api/routers/customer.ts:24`
- **Twin:** `hyperwhisper-cloud/src/lib/constants.ts:4` (and `nextjs/app/[locale]/user/(authenticated)/customers/CustomersClient.tsx:6`, which agrees with the cloud)
- **Divergence:**

| | cloud + admin UI | customer portal |
|---|---|---|
| credits consumed per minute | `export const CREDITS_PER_MINUTE = 6.3; // Derived from production usage logs` | `const CREDITS_PER_MINUTE = 1.67;` |
| minutes shown for a 1000-credit balance | `Math.floor(1000 / 6.3)` = **158** | `Math.floor(1000 / 1.67)` = **598** |

Three copies of one concept, two values. The portal's comment justifies its number as
`1 credit = $0.001; xAI Grok STT batch is $0.10/hour = 1.6667 credits/min` — the arithmetic is
right but **the premise is false**: xAI Grok is not the default route. `transcribe.ts`
`extractProvider()` falls back to `deepgram` when no `X-STT-Provider` header is sent, and
deepgram bills $0.0055/min (`cost-calculator.ts:16`) = **5.5 credits/min**. So the portal
overstates by 3.29x even measured against the single default provider it claims to be pricing,
and by 3.78x against the blended rate the service actually reports. The cloud's 6.3 is not a
guess: `hyperwhisper-cloud/src/routes/transcribe.test.ts:14` asserts
`expect(blendedEstimate).toBe(6.3)`, locking it in as the intended blended figure, and `:16`
asserts the per-provider estimate is deliberately *greater* than it.

- **Trigger:** Sign in at `/user/dashboard` with any credit balance. tRPC `customer.credits`
  (`customer.ts:118`) returns `minutesRemaining = floor(balance / 1.67)`, which
  `UserDashboardClient.tsx:63` passes to `CloudCreditsCard.tsx:47` for display. The same user's
  desktop app reads `GET /usage`, which returns `minutes_remaining = floor(balance / 6.3)`
  (`hyperwhisper-cloud/src/routes/usage.ts:138,143`), and any 402 quotes the same 6.3 rate
  (`lib/responses.ts:45,54`). At 1000 credits the web says 598 minutes and the app says 158.
  The user runs out of credit at roughly a quarter of the balance the website promised.
- **Evidence:** Not a fix ported to one twin — a divergence that has been there since day one.
  `git log -L 22,24:nextjs/server/api/routers/customer.ts` shows 1.67 entering in `e3708d4`
  (initial public release, 2026-06-30); `git log -L 3,5:hyperwhisper-cloud/src/lib/constants.ts`
  shows 6.3 entering in `3b810e6` (Fly backend vendored, same day). Two independently authored
  copies that never agreed, neither touched since. The admin panel siding with the cloud
  (`CustomersClient.tsx:6` = 6.3) is what identifies the portal as the odd one out: staff see
  the true figure, customers do not.
- **Repro:** `/private/tmp/claude-501/-Users-ray-Desktop-ray-os/0ad0c358-bd4c-4ff8-872f-2f81b1b9e66c/scratchpad/credits-per-minute-divergence.test.ts`
  (kept out of the repo — working tree is read-only). It reads the three real source files rather
  than restating literals. Run:
  `cd /private/tmp/claude-501/-Users-ray-Desktop-ray-os/0ad0c358-bd4c-4ff8-872f-2f81b1b9e66c/scratchpad && bun test credits-per-minute-divergence.test.ts`

  ```
    shipped copies:
      6.3   hyperwhisper-cloud/src/lib/constants.ts (cloud /usage + 402 errors)
      6.3   nextjs/.../customers/CustomersClient.tsx (admin view)
      1.67  nextjs/server/api/routers/customer.ts (customer web dashboard)

  error: expect(received).toHaveLength(expected)
  Expected length: 1
  Received length: 2

    balance=100:  dashboard says "~59 minutes remaining",  cloud /usage says "~15 minutes"  (overstated 3.93x)
    balance=500:  dashboard says "~299 minutes remaining", cloud /usage says "~79 minutes"  (overstated 3.78x)
    balance=1000: dashboard says "~598 minutes remaining", cloud /usage says "~158 minutes" (overstated 3.78x)

    default route = deepgram @ 5.5 credits/min; dashboard assumes 1.67 credits/min
      -> overstates minutes 3.29x
  error: expect(received).toBeLessThanOrEqual(expected)
  Expected: <= 1.1
  Received: 3.2934131736526946

   0 pass
   6 fail
  Ran 6 tests across 1 file.
  ```

### [2] The 402 body mixes a per-provider credit estimate with the blended credit→minute rate — CONFIRMED

- **Wrong copy:** `hyperwhisper-cloud/src/lib/responses.ts:46`
- **Twin:** `hyperwhisper-cloud/src/routes/transcribe.ts:417`
- **Divergence:**

| | how `estimated` is produced | how it is converted back to minutes |
|---|---|---|
| `transcribe.ts:417` | `estimateCreditsForProviderFallbacks(contentLength, provider, model, …)` — per-provider, priced off the most expensive fallback | — |
| `responses.ts:46` | — | `Math.ceil(estimated / CREDITS_PER_MINUTE)` with the flat blended 6.3 |

The producer and the consumer of `estimated` disagree about what a credit is worth per minute.
`transcribe.test.ts:16` asserts the per-provider estimate is strictly greater than the blended
rate, so dividing it by the blended rate systematically overstates `minutes_required`.

- **Trigger:** Any request that fails the credit gate on `POST /transcribe`.
  `transcribe.ts:418` calls `validateCredits(auth, estimatedCredits, …)`, which on failure calls
  `insufficientCreditsResponse(balance, estimated)` (`middleware/credits.ts:48`). For one minute
  of audio routed to an expensive provider — Chirp bills $0.016/min = 16 credits/min
  (`cost-calculator.ts:31`) — `estimated ≈ 16`, so the user is told
  `minutes_required = ceil(16 / 6.3) = 3` for a one-minute clip.
- **Evidence:** `responses.ts:44-46` takes `estimated` as an opaque credit figure and applies the
  module-level blended constant to it; nothing in either file reconciles the two rates. No
  comment or test asserts the mismatch is deliberate, unlike the many other places in this
  codebase where a deliberate difference is documented in situ.
- **Repro:** not attempted — the arithmetic is fully determined by the two cited lines, but
  producing a live 402 requires the auth + Redis fixtures the route test mocks.

### [3] `minutes_remaining` and `minutes_required` in the same 402 body answer to different rates — PLAUSIBLE

- **Wrong copy:** `hyperwhisper-cloud/src/lib/responses.ts:45-46`
- **Twin:** the same function's two adjacent lines.
- **Divergence:** `minutesRemaining` divides a *balance* by the blended 6.3 (correct — a balance
  is provider-agnostic), while `minutesRequired` divides a *provider-specific* estimate by the
  same 6.3 (incorrect, per Finding 2). The two numbers in one JSON body are therefore computed on
  different footings, so a client cannot compare them: a user can be shown
  `minutes_remaining: 2, minutes_required: 3` when the clip really is one minute long.
- **Unproven link:** I could not construct the exact `contentLength → provider/model selection`
  path that a real desktop client produces, so I cannot state the precise multiplier a given user
  sees. Confirming it requires reading `estimateCreditsForProviderFallbacks` in full
  (`transcribe.ts:130`) and the client's actual provider choice — the latter lives in the
  out-of-scope Swift/C# clients.
- **Repro:** not attempted.

## Coverage

- Twin sets discovered: 10 diffed to a conclusion (listed in the ledger above). The three
  discovery subagents that would have expanded this to the intended 25-40 did not return.
- Twin sets compared: 10 — items 1-10 in the coverage ledger.
- NOT compared: the full 17-provider interface conformance diff (retry policy, error mapping,
  response parsing, parameter pass-through, API-key-absence handling); a systematic odd-one-out
  sweep of all 23 API routes; tRPC zod schemas vs REST hand-rolled validation; the i18n/locale
  constant triplet; model lists (`stt-models.ts` / `llm-token-limits.ts` vs
  `lib/services/model-list.ts` / `api/internal/models`); Stripe webhook idempotency vs credit
  grant. The findings above say nothing whatsoever about these.

## Appendix: refuted candidates

- `hyperwhisper-cloud/src/providers/assemblyai.ts:96` — AssemblyAI's sync path admits 120 s of
  audio on a 15 s timeout while Chirp's admits 55 s on a 45 s timeout (`google-chirp.ts:51`).
  Looked like `c45ad84`'s fix left a sibling behind. **Refuted as INTENTIONAL** by the comment at
  `assemblyai.ts:87-95`: AssemblyAI's sync p50 is ~134 ms (vs Chirp's 5-15 s), and a stalled sync
  call blocks the async fallback, so a tight budget is the point. Chirp is `selfOnly` with no
  fallback to absorb a timeout; AssemblyAI has one. Different structural situations, correctly
  handled differently.
- `hyperwhisper-cloud/src/middleware/credits.ts:37` — the flat 6.3 credits/min reservation sits
  below several real provider rates (Chirp 16, ElevenLabs 9.83), suggesting systematic
  under-reservation. **Refuted as unreachable:** `estimateCreditsFromSize` is referenced only by
  its own definition and `routes/transcribe.test.ts:5`. Every live route uses a stricter path —
  `transcribe.ts:417` (per-provider), `post-process.ts:118` (fixed constant),
  `assistant.ts:312`, `ws-streaming-deepgram.ts:159` (`minimumStreamingCredits()`).
- `providers/cerebras.ts`, `providers/xai-llm.ts` — the only two LLM providers commit `28de2ec`
  ("incomplete LLM output must never replace a transcript") did not touch. **Refuted:** the
  acceptance gate is applied centrally at `routes/post-process.ts:185,215`, not per provider, so
  no provider can bypass it by being stale.
- `nextjs/app/api/account/*` vs `nextjs/app/api/license/*` — the most promising-looking twin grid
  on the repo (8 routes, created by the rename in `e76f053`). **Refuted:** all four `account/*`
  files are one-line re-exports of the `license/*` handlers. Drift is structurally impossible.
- `nextjs/lib/templates/*.ts` — four sibling email templates. **Refuted:** all four apply
  `escapeHtml` to the same two interpolated variables and are otherwise uniform.
- `nextjs/app/api/license/deactivate/route.ts` — no rate limiter, while its `activate` and
  `validate` siblings both have one. **Refuted:** it is a stub that performs no DB lookup and no
  outbound Polar call, so it has no amplification factor to protect.
