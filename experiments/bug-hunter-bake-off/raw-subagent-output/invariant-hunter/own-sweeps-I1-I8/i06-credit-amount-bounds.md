## Candidate 1
File: `nextjs/app/api/license/credits/route.ts`
Line: 119
Invariant: I6
Claim: `POST /api/license/credits` deducts `body.amount` verbatim — the only checks are `validateCreditDeductionAmount` (finite, >0, ≤1,000,000, ≤2 dp, `nextjs/app/api/license/credits/validation.ts:14`) — with the bare license key as the sole credential, no `x-internal-secret`, no rate limit, and no server-side re-derivation of what was actually consumed.
Failure scenario: Anyone who observes a license key (it travels as a `?account_key=` **query parameter** to `/transcribe` and `/ws/streaming-deepgram`, so it lands in Fly proxy logs, referrers, and any intermediary) sends one unauthenticated `POST {"license_key":"HW-…","amount":1000000}` and the victim's wallet is floored to 0 by `spendCreditGrantsByProvenance` (`db-layer.ts:583-607`, which walks every active grant and zeroes it). The victim's next transcription returns `insufficientCreditsResponse`; the credits are gone from `credit_grants` with no reversal path, and the audit trail records only an attacker-supplied `metadata` blob. Note the "hard bound" is not a bound in practice: the maximum purchasable balance is `MAX_CREDIT_DOLLARS × CREDITS_PER_DOLLAR` = 500,000 credits, i.e. the cap is 2× the largest wallet that can exist, so a single request always suffices.
Confidence: high

## Candidate 2
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 190
Invariant: I6
Claim: `handleCreditPurchase` grants `parseInt(session.metadata.credit_amount)` after checking only `payment_status === "paid"`; it never cross-checks the grant against `session.amount_total` / `amount_subtotal`, while `nextjs/app/api/checkout/credits/route.ts:189` sets `allow_promotion_codes: true`, making the amount actually paid client-controlled.
Failure scenario: A buyer enters any promotion code that exists in the Stripe account (Checkout applies an unrestricted coupon across the whole session, including a code created for a different product or a lapsed campaign). With a 90%-off code on a $500 credit purchase, Stripe reports `payment_status: "paid"` with `amount_total: 5300`, and the webhook grants the full pre-discount 500,000 credits — $500 of provider spend redeemed for $53, uncapped and repeatable per session. The quantity granted is never re-derived from the money received.
Confidence: medium

## Candidate 3
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 517
Invariant: I6
Claim: The refund actionability threshold mixes two sources of truth — `creditPortion = charge.amount - feeCents` uses the *discounted* actual charge but subtracts the *undiscounted* `metadata.fee_cents` written at checkout — so a promotion code (client input) lowers the bar at which a partial refund triggers a **full** grant clawback via `refundCreditGrant` (which reclaims the grant's entire `original_amount`, `db-layer.ts:476-490`, not the fraction refunded).
Failure scenario: Customer buys $100 of credits (100,000 credits, `fee_cents: 600`) with a $50 fixed-amount promo code, so `charge.amount = 5600` and `creditPortion = 5000`. Support later issues a $50 goodwill *partial* refund; `amount_refunded (5000) >= creditPortion (5000)` passes, `handleCreditRefund` runs, and all 100,000 credits are clawed back for a refund that returned only part of the purchase. The customer's balance drops to zero with no user-visible explanation.
Confidence: low

## Coverage

**Examined buckets:**
- **B6 next-money-api** — complete. `license/credits/{route,validation}.ts`, `account/credits/route.ts` (thin `export { GET, POST }` re-export, inherits Candidate 1 verbatim), `checkout/credits/{route,validation}.ts`, `checkout/route.ts` (redirect only), `webhooks/stripe/route.ts`, `license/validate/route.ts`, `license/activate`.
- **B9 next-db-and-services** — credit paths read end to end: `db-layer.ts` (`grantCreditLot`, `grantCreditsForStripeEvent`, `refundCreditGrant`, `spendCreditGrantsByProvenance`, `deductCreditBalance`, `reconcileCreditBalance`, `incrementCreditBalance`) and all of `lib/services/stripe-webhook.ts`.
- **B8 next-trpc-server** — `routers/admin/{customers,devices,stats,index}.ts`, `routers/customer.ts`.
- **B7 next-edge-auth-and-misc-api** — `api/internal/grant-license/route.ts`, `src/lib/license-validation.ts`, `lib/rate-limit.ts`.
- **B11 next-account-ui** — `components/credits/CreditsPurchase.tsx`, `components/customer/dashboard/CloudCreditsCard.tsx`, `app/[locale]/purchase-success/page.tsx`.
- **B1/B2/B5 cloud** — `middleware/credits.ts` (`deductCredits`/`performDeduction`/`recordLicenseUsage`), every client-input extraction point in `routes/{transcribe,post-process,assistant,usage,ws-streaming-deepgram}.ts`, `lib/{cost-calculator,stt-models}.ts`.
- **B4 cloud-llm-providers** — `lib/llm-provider.ts` model allow-list.
- **B12 next-tests** — `tests/credit-purchase-validation.test.ts` (confirms `computeCreditPurchase` is pinned by unit tests).

**Not examined / partially examined:**
- **B3 cloud-stt-providers** (15 files) — the 11 adapters derive `durationSeconds`/`costUsd` from upstream response bodies, not from client input, and the only client-supplied value reaching them (`model`) is allow-listed upstream. Missing-duration handling is I4's invariant, so I did not audit the adapters individually.
- **B10 next-public-site** (44 files) — marketing/i18n only; swept by grep for `amount|price|unit_amount|quantity|credit` with no money-bearing hits.
- **B12** — only the credit-purchase test read; the other four tests cover IP/redirect validation, out of scope for I6.

**Leads refuted:**
- **`session.metadata.credit_amount` writers** — REFUTED as a hole. `grep purchase_type` across `nextjs/` returns exactly one writer, `app/api/checkout/credits/route.ts:80-83`, which derives `credit_amount`/`fee_cents` from `computeCreditPurchase()` after `validateCreditPurchaseAmount()`. Nothing else can set that metadata without the Stripe secret key. (Candidate 2 is a *different* defect — the grant not being bounded by the amount paid — not a metadata-forgery hole.)
- **`computeCreditPurchase()` sole source of `creditCents`/`feeCents`** — CONFIRMED. Only two call sites: the checkout route and the client preview; both `unit_amount` values in the Stripe line items come from it, and `quantity` is hardcoded to `1`.
- **`components/credits/CreditsPurchase.tsx:92`** — CONFIRMED clean. Body is exactly `{ email, amount }`; the computed `credits/feeUsd/totalUsd` are `useMemo` display-only and never transmitted. `CloudCreditsCard.tsx:63` likewise sends only `{ licenseKey, amount }`.
- **Admin `addCredits` / `refund`** — CONFIRMED clean, as stated in the brief (`z.number().positive().max(MAX_ADMIN_CREDIT_GRANT)` at `customers.ts:255`; deterministic idempotency key at `customers.ts:325`). `createLicense` grants a hardcoded `5000` (`customers.ts:230`).
- **`api/internal/grant-license/route.ts`** — REFUTED. Takes only `email`; the credit quantity is the module constant `INTERNAL_BUNDLE_CREDITS` inside `provisionAccountKeyForEmail`. No client-controlled amount reaches it.
- **`X-STT-Model` / `X-LLM-Provider` model selection as a price lever (cloud)** — REFUTED. `resolveModel()` (`lib/stt-models.ts:234-255`) fails closed on an unrecognised model (400, not a default-rate fallback), and `LLM_PROVIDER_MODELS` (`lib/llm-provider.ts:66-73`) is an explicit per-provider allow-list. `extractProvider` also rejects unknown provider ids rather than defaulting. The `rates[model] ?? rates[defaultModel]` fallback at `cost-calculator.ts:436` is therefore unreachable from client input.
- **WebSocket streaming duration** — REFUTED. `totalDurationSeconds` accumulates from `durationSecondsForLinear16AudioBytes(data.byteLength)` on bytes the server actually received (`ws-streaming-deepgram.ts:334`), never from a client-declared duration.
- **Unauthenticated `licenseKey` on `/api/checkout/credits`** — noted but NOT an I6 violation: it lets an anonymous party pay to credit a key they don't own (a gift), and the amount is still server-derived. Flagging here only so another finder doesn't assume I6 covered it.
