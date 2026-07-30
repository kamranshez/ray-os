I read the webhook route, the webhook service, `db-layer.ts`, and all three relevant schemas, plus swept for any other Stripe webhook surface (there is exactly one; `hyperwhisper-cloud/` has zero Stripe code).

### Candidate
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 133
Invariant: I5
Claim: `handleLicensePurchase` catches and swallows any error from `grantCreditLot(...)` ("Don't throw - license was created, credits can be added later"), so the route returns 200 and Stripe never retries.
Failure scenario: A `checkout.session.completed` with `purchase_type: "license"` arrives while the Postgres pool is saturated / a serialization or deadlock error hits the `db.transaction` in `grantCreditLot`. The `account_keys` row was already committed at STEP 4, the credit error is logged, `sendLicenseEmail` runs, and the route returns `{received:true}`. Stripe marks the event delivered. Repair is impossible even in principle: any later re-delivery hits STEP 1 (`findAccountByStripeSession` at line 49), takes the early `return` at line 58, and never reaches STEP 4b again. The customer pays, receives a working license key by email, and has a permanent balance of 0 credits — every transcription is rejected as out of credits until a human notices and hand-grants.
Confidence: high (defect certain; reachability is legacy-only — nothing in this repo writes `purchase_type: "license"`, only `"credits"` in `app/api/checkout/credits/route.ts:80`, so this fires only for Stripe-dashboard/payment-link products still tagged `license`)

### Candidate
File: `nextjs/app/api/webhooks/stripe/route.ts`
Line: 125
Invariant: I5
Claim: `handleChargeRefunded` is wrapped in a `catch` that logs and deliberately does not return non-2xx ("This prevents infinite retries for non-transient failures"), and execution falls through to `return NextResponse.json({ received: true })` at line 132 — so *transient* failures are also never retried.
Failure scenario: `handleChargeRefunded` makes a live Stripe API call at line 495 (`stripe.checkout.sessions.list`). On a Stripe 429/5xx or a socket timeout that call throws, the error is swallowed, and Stripe records the `charge.refunded` event as successfully delivered. The customer has already received the cash back but keeps their license key (`updateAccountKey(..., "revoked")` never runs) and keeps every credit (`refundCreditGrant` never runs) — permanent, unretried revenue loss. The same swallow also makes partial application possible: at lines 553 and 565 `refundCreditGrant` commits first and `updateAccountKey` second, so a DB blip between the two leaves the account with credits clawed back but the license still `granted`, and no retry ever reconciles it.
Confidence: high

### Candidate
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 500
Invariant: I5
Claim: When `stripe.checkout.sessions.list({payment_intent, limit: 1})` returns an empty page, `handleChargeRefunded` logs and `return`s normally — indistinguishable from a definitive "not our purchase", so the route replies 200 and Stripe never retries.
Failure scenario: Stripe's list endpoint is read-replica-backed and eventually consistent. A `charge.refunded` delivered promptly after a refund (or for a charge whose session indexing lagged) yields `sessions.data.length === 0`; the handler returns, the route returns `{received:true}`, and the event is retired. The refunded customer permanently keeps their credit grant and (for a license purchase) an un-revoked, still-usable key.
Confidence: medium

### Candidate
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 593
Invariant: I5
Claim: `handleCreditRefund` aborts the clawback when `checkoutSession.metadata.credit_amount` is missing or unparseable — but `creditAmount` is never used by the mutation; `refundCreditGrant` is keyed purely on `(sourceType: "stripe_credit_pack", sourceId: checkoutSession.id)` and derives the clawback from `credit_grants.original_amount`. The guard blocks a mutation on a value it does not consume, and returns normally (200, no retry).
Failure scenario: Any credits checkout session whose `credit_amount` metadata is absent — a session created by an older deploy, a Stripe Payment Link, or a session where metadata was edited in the dashboard — is refunded. `parseInt(undefined || "0", 10)` yields 0, the handler `console.error`s and returns, the route returns 200, and Stripe stops. The customer has the cash back and the full credit pack still spendable, permanently.
Confidence: medium

### Candidate
File: `nextjs/lib/services/stripe-webhook.ts`
Line: 447
Invariant: I5
Claim: In `handleCreditMint`, `emailService.sendCreditMint` failure is logged only; the function returns normally and the route returns 200. Because the grant is already committed, every re-delivery is short-circuited as `"duplicate"` at line 402 and returns *before* the email — so the failure is unrecoverable even if a retry were triggered.
Failure scenario: A guest buys credits with no license key during a Resend outage that outlasts the 3-attempt/~1.75s in-process retry loop in `email.ts`. `grantCreditsForStripeEvent` commits the new `account_keys` row and the credit grant; `sendCreditMint` returns `{success:false}`; the route returns 200. The freshly minted license key is the *only* way the buyer can use those credits and it exists nowhere but the database — no email, no receipt, no dashboard they can reach without the key. The purchase is money taken for an inaccessible product. (The same swallow exists for `sendLicenseEmail` at line 163, where the code at lines 51-58 *does* contain an explicit "resend email in case it failed before" repair path — dead code, because a 200 means Stripe never re-delivers.)
Confidence: medium (scoping caveat: this loses *access to* a grant rather than the grant row itself, so a strict reading of "mutates licenses or credits" may exclude it)

### Coverage

Examined buckets:
- **B6 (next-money-api)** — full read of `app/api/webhooks/stripe/route.ts`; checked `app/api/checkout/credits/route.ts` for the metadata contract (`purchase_type`, `credit_amount`, `fee_cents`, `license_key`) that the webhook and refund paths depend on.
- **B9 (next-db-and-services)** — full read of `lib/services/stripe-webhook.ts`; `src/lib/db-layer.ts` lines 255-660 (`grantCreditLotInTransaction`, `grantCreditLot`, `grantCreditsForStripeEvent`, `refundCreditGrant`, `spendCreditGrantsByProvenance`, `reconcileCreditBalance`, `incrementCreditBalance`); schemas `credit-grants.ts`, `credit-balances.ts`, `stripe-processed-events.ts`, `account-keys.ts`; `lib/services/email.ts` retry/return semantics.
- **B8 (next-trpc-server)** — read `server/api/routers/admin/customers.ts` lines 200-340 as the only other `refundCreditGrant`/`grantCreditLot` caller, to confirm no sourceType/sourceId collision with the webhook keys (`admin_license_bundle`, `admin_manual`, and a `license_bundle` clawback — all distinct or correctly keyed). Not a webhook handler, so nothing reported from it.
- **B12 (next-tests)** — listed; there is **no** test file covering the Stripe webhook at all.
- **B1-B5 (all of `hyperwhisper-cloud/`), B7, B10, B11** — swept by grep for `stripe`/`Stripe`/`constructEvent`/`grantCredit*`/`refundCreditGrant`. Zero hits in the cloud service; the only `webhook` route handlers in `nextjs/app` are `webhooks/stripe` and `webhooks/add-blog-post` (the latter mutates `blog_posts`, not licenses or credits). No I5 surface exists in these buckets, so they are covered by exclusion rather than by reading every file.

Not examined / partially examined:
- `drizzle/` migration SQL is out of scope, so I verified the unique indexes from the Drizzle schema declarations only. If `credit_grants_source_unique` or `idx_account_keys_stripe_session` were declared but never migrated, several dedupe guarantees below would collapse — I could not confirm the live DB state.
- `hyperwhisper-cloud` billing (B5) read only via grep; it holds no DB and never touches Stripe, so no I5 surface.

Leads refuted:
- **`handleLicensePurchase:126` calling an "un-deduped" `grantCreditLot`** — refuted. `credit-grants.ts:45` declares `uniqueIndex("credit_grants_source_unique").on(sourceType, sourceId)`, and `grantCreditLotInTransaction` (`db-layer.ts:392`) uses `onConflictDoNothing({ target: [creditGrants.sourceType, creditGrants.sourceId] })` — the arbiter target matches the index exactly. A re-delivered `checkout.session.completed` / `async_payment_succeeded` pair for the same session **cannot** double-grant the 5000 credits; the `findAccountByStripeSession` read is a belt-and-braces optimisation, not the only guard. The real defect at that site is the *error swallow* at line 133, not a missing dedupe.
- **`handleChargeRefunded`'s unused `eventId` / the docblock's false claim that it "is recorded in `stripe_processed_events` keyed by charge.id"** — the claim is factually wrong (nothing writes that row; `eventId` is a dead parameter), but it is **not** an I5 violation. `refundCreditGrant` dedupes on the grant's own `refunded_amount >= original_amount` state under a `SELECT ... FOR UPDATE` on a row keyed by the checkout session id — a stable Stripe id. I traced concurrent double-delivery: the second transaction blocks on the row lock, re-reads under READ COMMITTED, sees `clawback <= 0`, and returns `"duplicate"`. No double-deduct is reachable.
- **`grantCreditsForStripeEvent`'s `onConflictDoNothing({target: stripeObjectId})` colliding with the `event_id` primary key** — refuted. A same-`event_id` re-delivery necessarily carries the same `stripe_object_id`, so Postgres's speculative-insertion arbiter check hits the `stripe_object_id` index first and skips cleanly; it never falls through to a PK 23505.
- **Concurrent license insert racing to two keys** — refuted. `account-keys.ts` declares `uniqueIndex("idx_account_keys_stripe_session")`, and both `handleLicensePurchase` (line 108) and `handleCreditMint` (line 368) catch code `23505` and converge on the existing row.
