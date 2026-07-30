---
skill: concurrency-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 12 |
| PLAUSIBLE findings | 3 |
| Findings with an executable repro | 4 |
| Files opened (of 210 in scope) | ~150 (union across 6 agents; the mapper alone opened 120, I opened 17 directly) |
| Subagents spawned | 6 |
| Strategy came up dry? | no |

## Coverage ledger

**Shape of the run.** Phase 1 spawned one mapping agent over the full pinned arena; Phase 2
fanned out five lens agents in parallel (A TOCTOU, B missing-await/fire-and-forget, C lock
discipline, D lifecycle/teardown, E reentrancy/ordering). All six completed. A transport
failure mid-run swallowed every completion notification, so I initially wrote this report
from my own reading alone and then recovered all six agents by re-requesting their results;
what follows is the merged set. Lens agents A and B were additionally delayed by a global
subagent-concurrency limit and had to be relaunched twice.

**What I verified myself rather than taking on trust.** The bar for this skill is inverted —
every candidate is presumed refuted — so I did not simply forward lens output. I read 17
files directly and independently re-checked the load-bearing claim behind every CONFIRMED
finding promoted from a lens: that `idx_account_keys_email` is a plain non-unique index
(`schema/account-keys.ts:41`); that `provisionAccountKeyForEmail` grants on
`sourceId: license.id`, the UUID of the row it just minted (`db-layer.ts:275-280`); that
admin `addCredits` grants on `sourceId: crypto.randomUUID()` (`admin/customers.ts:276`);
that `refundCreditGrant` and `spendCreditGrantsByProvenance` genuinely acquire the same rows
in different orders (`db-layer.ts:508-513` versus `:576-580`); that `usage.ts:44-52` caches
an invalid verdict with no status check; and that `providers/utils.ts:118-119` clears its
abort timer in a `finally` that runs when headers arrive. Findings 13-15 are PLAUSIBLE
precisely because I could not close them the same way.

**Deployment facts, because they decide every reachability verdict.** `fly.prod.toml` pins
`min_machines_running = 17` across 17 regions with `auto_stop_machines = 'off'` — 17
separate Bun processes, so no in-process structure is ever a global guarantee, and the only
genuinely shared state is Upstash Redis and Postgres. Machines recycle only on deploy, so
anything leaked accumulates for the machine's lifetime. `nextjs/` is Vercel serverless with
many concurrent lambdas. These facts are what turn several findings below from
"theoretically racy" into "races on ordinary traffic".

**What was skipped and why.** Generic logic bugs, input validation, authz holes, and spec
mismatches were dropped on sight — sibling hunters own those, and several lens candidates
were discarded for drifting there. The 20 provider adapters under
`hyperwhisper-cloud/src/providers/` were mapped at grep level only, so finding 5, finding 14
and the teardown corollary in finding 10 rest on the adapters actually read (deepgram,
anthropic, soniox, google-chirp, utils) rather than all 20. `nextjs/lib/templates/*`,
`disposable_domains.ts`, and roughly 20 marketing/legal/layout files were grep-verified to
contain no timers, effects, or fetches and not read line by line. The 19 test files were not
audited as subjects.

**What this strategy is structurally blind to here.** Three things. First, single-actor
bugs: if a path is simply wrong, this lens never looks at it, because every candidate must
name a second actor — assume the sibling hunters own everything I found nothing in. Second,
synchronization living outside the TypeScript: the Postgres isolation level actually
configured, Upstash's consistency guarantees, and Fly's `kill_timeout` are read from config
or assumed, never observed against a live system. Third, races needing real infrastructure:
I can drive the Hono routes in-process under `bun test`, but I cannot make two Vercel lambdas
or two Fly machines genuinely race, so every cross-instance claim is argued from topology
rather than demonstrated. That is why only 4 of 15 findings carry a repro, and all 4 are in
the cloud service.

**Why the refuted list is long, and worth reading.** This codebase has plainly been through
a concurrency review already. `spendCreditGrantsByProvenance` uses `SELECT ... FOR UPDATE`
inside a transaction; `account_keys` carries unique indexes on `polar_license_key_id`, `key`,
and `stripe_session_id`; `credit_grants` has one on `(source_type, source_id)`;
`device_validations` has one on `(license_key_id, device_id)`; several carry comments naming
the exact race they close. A large fraction of the candidates the lenses generated died
against defences already installed. What survived clusters revealingly: the constraints
protect *storage*, and almost every confirmed bug is either upstream of storage (an
admission gate reading a cache) or in a path where the dedupe key was chosen so that the
constraint can never fire.

**Absence of findings outside these areas means UNEXAMINED, not clean.**

---

# Concurrency hunt — /Users/ray/Desktop/hyperwhisper-public (deep)

## Summary

Mapped the concurrent surface of a 17-machine Fly.io transcription service and its Vercel
serverless licensing backend, then dragged all five lenses across it. The storage layer is
genuinely well defended and refuted most double-write candidates outright. What survived
falls into three families: an **admission gate** that reads a cached credit balance and
never reserves against it, so concurrent requests all spend one balance; **dedupe keys
chosen so the unique index can never fire**, which turns two nominally idempotent grant
paths into money printers; and **teardown asymmetries** where a charge, a socket, or an
entire streaming session is abandoned because the thing that would have flushed it is only
reachable from a path that never runs. Risk is high and one-directional: it costs the
operator money and can lock out a paying customer, but it does not corrupt balances or grant
unauthenticated access.

## Findings

### 1. Credit admission gate never reserves, so N concurrent requests spend one balance — CONFIRMED+REPRO

**Where:** `hyperwhisper-cloud/src/middleware/credits.ts:41-51`; check at
`transcribe.ts:418`, act at `:679` · **State:** Redis `license:<key>`, Postgres
`credit_grants` · **Trigger:** one account key issuing concurrent transcriptions — two
devices, or a client that times out and resends. No unusual timing needed.

`validateCredits` compares `balance < estimatedCredits` and writes nothing. That balance came
from `getCachedLicense` (`auth.ts:110`) reading a Redis key with a **one-hour TTL**, and the
debit does not happen until `deductCredits` at `transcribe.ts:679`, a full provider call
later. Nothing reserves in between, so every concurrent request sees the same number.

| step | actor 1 (request A) | actor 2 (request B) |
|---|---|---|
| 1 | `getCachedLicense` → `credits: 9.9` (`auth.ts:110`) | |
| 2 | `9.9 < 9.9` false → admitted (`credits.ts:47`) | |
| 3 | | `getCachedLicense` → `9.9`, cache untouched by step 2 |
| 4 | | `9.9 < 9.9` false → **also admitted** |
| 5 | calls Deepgram, operator billed | calls Deepgram, operator billed again |
| 6 | `deductCredits` (`:679`) → DB takes 9.9, balance 0 | |
| 7 | | `deductCredits` → nothing matches `remaining_amount > 0`, takes **0** |

**Consequence:** admission is effectively unbounded — measured, not assumed. At 5 concurrent
requests on a one-request balance, 5 are admitted; **at 40, all 40 are admitted**: 9.90
credits taken against 220.00 reported, leaving 210.10 credits of transcription delivered
free. The overspend is also invisible, because the API returns `credits_deducted: amount`,
the *requested* figure (`app/api/license/credits/route.ts:135`), while `deductCreditBalance`
discards the true `deductedAmount` (`db-layer.ts:626-628`). The balance never goes negative,
which is why the storage-layer defences do not catch it.

**Fix direction:** reserve at the gate instead of comparing. Cheapest correct version is a
conditional atomic decrement of a Redis reservation counter (Lua CAS) keyed on the license,
refunded on completion with the true cost. Better: a `reserve` endpoint doing
`UPDATE ... WHERE remaining >= $amount` inside the same `FOR UPDATE` transaction the spend
already uses, failing closed on zero rows. Separately, `deductCreditBalance` should return
`deductedAmount` so a shortfall is observable at all.

**Repro:** `scratchpad/repro-1/gate-race.test.ts` — drives the real `transcribeRoute` with a
stateful fake Upstash and a faithful floor-at-zero licensing API. Asserts `admitted === 1`,
fails with 5. `scale-variant.test.ts` alongside it raises concurrency to 40.

---

### 2. Cached balance is a last-writer-wins SET, so a slow response restores phantom credits — CONFIRMED+REPRO

**Where:** `hyperwhisper-cloud/src/lib/redis.ts:70-76`, written from `credits.ts:86`,
`auth.ts:75`, and `usage.ts:48` and `:81` · **State:** Redis `license:<key>` ·
**Trigger:** any overlap between a finishing transcription's deduction and the desktop app's
periodic `/usage` poll, or two transcriptions in different regions.

`cacheLicense` is a plain `SET ... EX 3600` with no CAS, no version, and no compare. Four
independent writers across 17 machines race it, and `cachedAt` is written by all of them but
never read for ordering (`redis.ts:54-68`).

| step | actor 1 (deduction, slow response) | actor 2 (`/usage` refresh, fast response) |
|---|---|---|
| 1 | DB commits 600 → 500; response carries `credits_remaining: 500` | |
| 2 | | reads the balance from a lambda that snapshotted **before** step 1 committed → 600 |
| 3 | | returns first; `cacheLicense(600)` |
| 4 | response finally lands; `cacheLicense(500)` — or the reverse, decided purely by latency | |

**Consequence:** whichever lands last wins, and when that is the stale one the cache claims
credits that do not exist for up to the full hour, on every machine. This is the supply of
phantom headroom that finding 1 then hands out. Nothing self-corrects until some later
deduction happens to write a fresher value.

**Fix direction:** stop caching a mutable balance under a last-writer-wins key. Either cache
only the immutable validity verdict and read the balance authoritatively at the gate, or
make the write monotonic via a version token and a Lua CAS that refuses to raise a balance
from a staler version. The reservation counter in finding 1 subsumes this.

**Repro:** `scratchpad/repro-2/stale-cache-overwrite.test.ts` — two deductions whose
latencies are inverted relative to their application order. Cache writes `50 -> 90`, ending
at 90 against a true balance of 50. Asserts 50 and fails.

---

### 3. A failed charge is indistinguishable from a successful one — CONFIRMED+REPRO

**Where:** `hyperwhisper-cloud/src/middleware/credits.ts:74-82` and `:92-96` ·
**Trigger:** any licensing-API 5xx, or latency past `LICENSE_API_TIMEOUT_MS` (10s,
`constants.ts:71`, whose own comment names Vercel cold starts as the reason it exists).

`recordLicenseUsage` is typed `Promise<void>` and swallows both failure modes — non-ok gets
a `console.warn` and a bare `return`, network/abort gets a `console.warn` in the catch.
`performDeduction` awaits it and returns `creditsUsed` unconditionally (`:144-145`), so it
**cannot reject for a billing failure**. Lens B pinned the consequence exactly: the
`.catch(console.error)` at all five call sites (`transcribe.ts:692`, `assistant.ts:363`,
`post-process.ts:267` and `:291`, `ws-streaming-deepgram.ts:220`) and the `.catch(() => {})`
at `credits.ts:127` are **unreachable dead code for the failure they were written for**.

| step | actor 1 (a `/transcribe` request) | actor 2 (the licensing API) |
|---|---|---|
| 1 | transcription done, provider already billed | |
| 2 | `deductCredits` → `POST /api/license/credits` | |
| 3 | | returns 500, or exceeds the 10s abort |
| 4 | `console.warn`, bare `return` (`:81`) — no throw | |
| 5 | promise **resolves with a success-shaped value**; `cacheLicense` at `:86` sits on the success branch only, so it never runs | |

**Consequence:** revenue lost with no signal — no retry, no dead-letter, no metric, one
`console.warn` among per-request logs on one of 17 machines. My repro shows `deductCredits`
resolving with `1000` while zero credits are debited and zero cache writes occur. The
response has already gone out carrying `X-Credits-Used` (`transcribe.ts:717`), so the client
decrements its local balance for a charge that never happened. In the ambiguous-timeout case
the DB *did* commit, so Redis keeps a pre-debit balance and over-serves for the rest of the
hour. This is the amplifier that makes findings 1 and 2 expensive rather than untidy.

**Fix direction:** throw on both failure modes and stop swallowing at `:127`, then persist
the failed charge durably. Note the ordering constraint lens B flagged: retry is not safely
addable first, because `app/api/license/credits/route.ts:80-145` takes no idempotency key and
applies an unconditional decrement at `:119`, so retrying after an ambiguous timeout
double-charges. Add the idempotency key — the request id already exists at
`transcribe.ts:704` — *before* adding retry.

**Repro:** `scratchpad/repro-4/billing-fails-open.test.ts` — HTTP 500 and a thrown network
error, both driving the real `deductCredits`. Both show `caller saw a failure? false`,
`resolved: 1000`, `cache writes: 0`. Both assert the caller is informed; both fail.

---

### 4. `/usage` poisons the license cache with a transient failure, locking out a paying customer for an hour — CONFIRMED

**Where:** `hyperwhisper-cloud/src/routes/usage.ts:44-52` · **State:** Redis
`license:<key>` · **Trigger:** a routine background `/usage` poll landing during a Vercel
redeploy, or any 5xx from the licensing API.

Same key as finding 2, different writer, strictly worse failure mode — and it is best
understood as a **missing guard that exists in a sibling file**. `auth.ts:70-73` explicitly
refuses to cache a `>= 500` response, commenting that doing so "would lock a paying user out
for the full LICENSE_CACHE_TTL_SECONDS". `usage.ts` has no such check: it does
`await response.json().catch(() => ({}))`, so a 502 returning an HTML error page yields `{}`,
derives `isValid = data.valid === true` — false — and **unconditionally** calls
`cacheLicense({isValid: false, credits: 0})`.

| step | actor 1 (desktop app background `/usage` poll) | actor 2 (the licensing API) |
|---|---|---|
| 1 | polls `/usage`, cache miss → calls `/api/license/validate` | |
| 2 | | mid-redeploy: returns a 502 HTML error page |
| 3 | `.json().catch(() => ({}))` → `{}` → `isValid = false` (`usage.ts:45-46`) | |
| 4 | `cacheLicense({isValid: false, credits: 0})`, TTL 3600s (`:48-52`) | |
| 5 | user hits `/transcribe`; `validateAuth` gets a cache **HIT** and returns `invalidLicenseResponse` (`auth.ts:113-115`) | |

**Consequence:** a valid paying customer is rejected on every request for up to an hour,
across all 17 machines. There is no self-heal, because step 5 is a cache *hit* — the API is
never re-consulted. Only `force_refresh=true` escapes, which the end user cannot trigger. A
transient upstream blip becomes an hour-long outage for whoever happened to poll during it.

**Fix direction:** port the `auth.ts:70-73` guard into `usage.ts` — never cache a verdict
derived from a `>= 500` response or an unparseable body. Better, factor the single
"validate and cache" routine into one function both callers share, so this cannot drift again.

---

### 5. Provider timeout covers response headers only, so a stalled body hangs forever and leaks the audio buffer — CONFIRMED

**Where:** `hyperwhisper-cloud/src/providers/utils.ts:77` and `:118-119` ·
**State:** buffered audio ArrayBuffer plus upstream socket · **Trigger:** an upstream that
returns 200 headers then stalls the body — a half-open load balancer, a provider incident.

`const timeoutHandle = setTimeout(() => controller.abort(), timeoutMs)` is cleared in a
`finally` (`:118-119`) that runs the instant `await fetch` resolves — which per the Fetch
standard is when **headers** arrive, not the body. The `AbortController` is therefore inert
for the whole body read, which happens in the caller
(`deepgram.ts:154 await response.json()`).

| step | actor 1 (a `/transcribe` request) | actor 2 (the upstream provider) |
|---|---|---|
| 1 | audio buffered to an ArrayBuffer (`transcribe.ts:431`) | |
| 2 | `fetchWithTimeout` → abort timer armed | |
| 3 | | returns 200 headers at t=0.4s |
| 4 | `finally` fires `clearTimeout` — **abort disarmed** (`utils.ts:118-119`) | |
| 5 | | stops sending; never closes |
| 6 | `await response.json()` blocks forever — no signal, no timeout, no race | |

**Consequence:** the handler never returns and the buffered audio stays reachable via
closure. `MAX_AUDIO_SIZE_BYTES` is 2GB (`constants.ts:10`) on a 1GB machine, and with
`auto_stop_machines='off'` these accumulate until the next deploy — one permanently leaked
buffer and socket per stalled response, ending in an OOM kill. The detail that makes this a
bug rather than a deliberate choice: `credits.ts:71`, `auth.ts:45`, and `usage.ts:41` all use
`AbortSignal.timeout()`, which stays attached and *does* abort a stalled body read. The STT
hot path is the only place using clear-on-headers.

**Fix direction:** use `AbortSignal.timeout(timeoutMs)`, or keep the controller armed until
the body is consumed by moving the read inside `fetchWithTimeout` and clearing the timer
afterwards.

---

### 6. Lock-order inversion between spend and refund deadlocks, and the refund loss is permanent — CONFIRMED

**Where:** `nextjs/src/lib/db-layer.ts:508-513` (refund) versus `:576-580` (spend) ·
**State:** `credit_grants` row locks · **Trigger:** a refund processed while the customer's
app is mid-transcription, or two credit packs for one customer refunded back to back.

Both paths take `FOR UPDATE` on the same row set in **different orders**, which I verified
directly. `spendCreditGrantsByProvenance` orders strictly `expires_at ASC, created_at ASC,
id`. `refundCreditGrant` first locks the target grant alone (`WHERE source_type/source_id
... FOR UPDATE`, `:460-466`), then re-locks the whole active set with
`ORDER BY CASE WHEN id = ${grant.id} THEN 0 ELSE 1 END, expires_at ASC, ...` — the target
jumps the queue. `LockRows` sits above `Sort` in the Postgres plan, so `ORDER BY` really does
determine acquisition order.

| step | actor 1 (spend) | actor 2 (refund of grant G2) |
|---|---|---|
| 1 | locks G1 (soonest expiry) | |
| 2 | | locks G2 (target first, `:512`) |
| 3 | waits for G2 | |
| 4 | | waits for G1 → **deadlock; Postgres aborts one with 40P01** |

**Consequence:** neither package handles `40P01`/`40001` anywhere (grepped, zero hits), and
both loser paths fail silently. If the spend loses, the route 409s and the cloud's
`credits.ts:79-85` warns and returns — charge dropped, per finding 3. If the refund loses,
`app/api/webhooks/stripe/route.ts:119-124` catches it and returns **200** (deliberately, to
"prevent infinite retries"), so Stripe never redelivers: the money is refunded and the
credits are never clawed back, permanently. Refund-versus-refund deadlocks too, with no spend
involved.

**Fix direction:** make the refund's second lock use the same order as the spend and drop the
`CASE WHEN` prioritisation — the target grant is in the set anyway. Add explicit
serialization-failure retry around both transactions, and stop returning 200 for a refund
that failed transiently: distinguish transient from permanent before choosing the status code.

---

### 7. Internal license grant double-mints, because the check is unbacked and the dedupe key is freshly random — CONFIRMED

**Where:** `nextjs/app/api/internal/grant-license/route.ts:31-38` → `db-layer.ts:245-283` ·
**Trigger:** a double-submitted or retried "claim your key" call. This endpoint has **no
rate limiter**, unlike `/api/license/validate`.

Two defences that would normally close this are both absent, which I verified:
`idx_account_keys_email` is a **plain, non-unique** index (`schema/account-keys.ts:41`), and
`grantCreditLot` is called with `sourceId: license.id` — the UUID of the row *just minted*
(`db-layer.ts:275-280`) — so `credit_grants_source_unique` sees two distinct sourceIds and
dedupes nothing. `polarLicenseKeyId` and `stripeSessionId` are NULL on this path, and NULLs
are distinct under a Postgres unique index, so those arbiters do not fire either.

| step | actor 1 | actor 2 (retry / double-click) |
|---|---|---|
| 1 | `getAccountKeysByEmail` → no granted row | |
| 2 | | same read → still no granted row (actor 1 is mid-provision) |
| 3 | inserts key K1, grants 10,000 on `sourceId = K1.id` | |
| 4 | | inserts key K2 (different random key, so `idx_account_keys_key` stays clean), grants **another** 10,000 on `sourceId = K2.id` |

**Consequence:** the account holds two Account Keys and 20,000 credits instead of 10,000,
both of which validate. The only accidental limiter is that a brand-new email serializes on
`user.email UNIQUE` — and that evaporates the moment the user row pre-exists, which is the
normal case for a prior purchaser or anyone who has used magic-link sign-in.

**Fix direction:** add a unique partial index on
`account_keys(email) WHERE status = 'granted'` so the check is actually backed, and key the
grant on something stable and caller-supplied (the claim id) rather than the row it just
created.

---

### 8. Admin credit grant uses a random dedupe key, so the unique index can never fire — CONFIRMED

**Where:** `nextjs/server/api/routers/admin/customers.ts:271-277` · **Trigger:** an impatient
double-click or a tRPC retry.

`grantCreditLot({ ..., sourceId: crypto.randomUUID() })` — verified at `:276`. The
`onConflictDoNothing` arbiter is `credit_grants_source_unique` on `(source_type, source_id)`,
so a freshly random `sourceId` guarantees it **never matches**. The surrounding transaction
is a critical section protecting nothing, and `previousBalance` is read outside it at `:271`.

| step | actor 1 (admin click) | actor 2 (same click, retried) |
|---|---|---|
| 1 | reads `previousBalance` = 1000 (`:271`) | |
| 2 | | reads `previousBalance` = 1000 |
| 3 | grants 5,000 on a random sourceId | |
| 4 | | grants **another** 5,000 on a different random sourceId |
| 5 | both responses report `previousBalance: 1000`, so the UI looks correct | |

**Consequence:** 10,000 credits issued for one intended 5,000, with no visible anomaly. The
contrast is instructive: `grantCreditsForStripeEvent` (`db-layer.ts:414-443`) keys on a
stable id and is correctly idempotent — this path is the odd one out, and the same shape
recurs in finding 7. The only client-side guard is a disabled button
(`CustomersClient.tsx:243`), which two browser tabs bypass.

**Fix direction:** key on something stable — the admin action id, or a hash of
(licenseKeyId, amount, reason, coarse timestamp) — so the existing unique index does its job.

---

### 9. A streaming session's entire charge is lost on every deploy — CONFIRMED

**Where:** `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts:188-222` and
`index.ts:95` · **Trigger:** every production deploy, of which CI does one per merge.

Distinct from finding 10 and from the settled HTTP case. For `/transcribe`, `deductCredits`
registers in `inFlightDeductions` before the response is built, so the drain covers it. For
websockets, `deductCredits` is reached **only** from `endSession` (`:209`), which is reachable
only from socket events — and no registry of open sockets exists anywhere in the file, so
`gracefulShutdown` has no handle on them even in principle.

| step | actor 1 (a live streaming session) | actor 2 (the platform) |
|---|---|---|
| 1 | streaming; `totalDurationSeconds` accrues at `:334`; nothing registered in `inFlightDeductions` | |
| 2 | | deploy → SIGTERM |
| 3 | | `drainPendingDeductions` sees an empty Set → returns 0 in 0 ms → `process.exit(0)` (`index.ts:99`) |
| 4 | `onClose` (`:364`) and the upstream `close` listener (`:279`) never fire; `endSession` never runs; `deductCredits` never called | |

**Consequence:** Deepgram is billed for every second, the user keeps every transcript, and the
licensing API is never called — zero credits deducted for the whole session, with no log and
no counter. Bounded per session at roughly 52 minutes of live Nova-3
(`MAX_SESSION_AUDIO_BYTES` 100MB ÷ ~32KB/s), multiplied by every open session on each of 17
machines, every deploy. This is precisely the scenario the comment at `credits.ts:99-103`
claims the drain prevents.

**Fix direction:** checkpoint streaming charges incrementally — deduct per N seconds rather
than once at session end — so an abrupt exit loses at most one interval, and keep a registry
of open sockets that `gracefulShutdown` can flush.

---

### 10. Shutdown abandons in-flight work, and the drain's own telemetry reports success — CONFIRMED+REPRO

**Where:** `hyperwhisper-cloud/src/index.ts:82-100` and `credits.ts:106-116` ·
**Trigger:** every deploy.

The drain is correct for what it was written for — `deductCredits` registers synchronously at
`credits.ts:125` before the response is built at `transcribe.ts:695`, and I confirmed there is
no registration-gap race there. Three real gaps remain. First, `drainPendingDeductions`
early-returns 0 on an empty Set (`:107-109`), and a request still inside its provider call has
registered nothing — so the drain returns in 0 ms and `process.exit(0)` fires, forfeiting the
~5s `kill_timeout` grace Fly already granted. Second, `SHUTDOWN_DRAIN_MS` is 4,000 while
`LICENSE_API_TIMEOUT_MS` is 10,000, so even the deductions the drain *does* see are abandoned
6 seconds before their fetch can resolve — and `fly.prod.toml` sets no `kill_timeout`, so the
5s default is a hard ceiling that 4s cannot simply be raised past. Third, the function returns
`pendingCount` captured *before* the race (`:107`), not the number that settled, so
`index.ts:96-98` logs `machine.shutdown_drained_deductions {count: N}` on abandonment — **the
only telemetry asserts success precisely when the charge was dropped.**

**Consequence:** in-flight transcriptions die on every deploy across 17 machines; the user
retries and the operator pays the upstream provider twice. `process.exit(0)` also skips every
cleanup `finally`, orphaning paid upstream artifacts permanently — the AssemblyAI transcript
delete (`assemblyai.ts:605`), the Soniox delete (`soniox.ts:319-327`; Soniox never
auto-deletes), and the google-chirp GCS scratch cleanup plus cancellation of a still-running,
still-billing `batchRecognize` (`google-chirp.ts:297-303`).

**Fix direction:** track in-flight requests as deductions are tracked and drain both; stop
accepting connections first (`index.ts` never captures the Bun server handle, so it cannot
call `stop()` today); fix the return value to report what actually settled; raise
`kill_timeout` in `fly.prod.toml` and size the drain under it.

**Repro:** `scratchpad/repro-3/shutdown-drain-gap.test.ts` — a characterization test (it
passes, documenting current behaviour). With a request mid-flight the drain reports 0 pending
and returns in 0 ms; with a deduction registered it correctly reports 1 and waits 116 ms. The
asymmetry is the finding.

---

### 11. A refund arriving before its grant leaves permanent free credits, or a granted license on a refunded charge — CONFIRMED

**Where:** `nextjs/lib/services/stripe-webhook.ts:600-610` and `:546-551`, with
`db-layer.ts:468-471` · **Trigger:** unordered Stripe delivery, or any 500 from the credits
handler that pushes the grant behind the refund in wall-clock order.

Stripe does not guarantee event ordering. `refundCreditGrant` returns
`{status: "duplicate", refundedAmount: 0}` when **no grant row exists** (`:468-471`) —
indistinguishable from "already refunded". The refund handler reads that as "already
processed" and returns 200, so Stripe closes the event forever. Critically,
`refundCreditGrant` never writes `stripe_processed_events`, so it leaves no tombstone —
despite doc comments at `:469-471` and `:577` claiming it is keyed by `charge.id`.

| step | actor 1 (grant, delayed by a 500 and retry) | actor 2 (refund) |
|---|---|---|
| 1 | `checkout.session.completed` → handler throws → 500 → Stripe backs off | |
| 2 | | `charge.refunded` → `refundCreditGrant(...)` → **no grant row** → "duplicate", 0 clawed back, 200, closed forever |
| 3 | retry lands; `stripe_processed_events` for this session is **still empty** — the refund wrote nothing — so the grant proceeds | |

**Consequence:** the customer has their money back **and** the credits, permanently; no
webhook will ever remove them. The license variant is the same shape at `:546-551`, where
`handleChargeRefunded` returns early when the license lookup is null — before the revoke at
`:565` — leaving a fully refunded purchase holding a granted, credit-loaded key that
`/api/license/validate` accepts. Both are unbounded and silent; the operator finds them only
by diffing Stripe refunds against `account_keys`.

**Fix direction:** write a tombstone. Record the refund in `stripe_processed_events` (or a
dedicated refunds table) keyed on the charge/session even when no grant row is found, and have
the grant path check for it before granting. That makes the two events commutative, which is
the only property that actually fixes an ordering bug.

---

### 12. Stripe retry re-sends the license email, because the license path threads no event id — CONFIRMED

**Where:** `nextjs/app/api/webhooks/stripe/route.ts:78` versus `:91`, and
`stripe-webhook.ts:49-57` · **Trigger:** a slow Resend call or Vercel cold start pushing the
handler past Stripe's 10s response timeout.

`handleCreditPurchase(session, event.id, event.type)` threads the event id into
`stripe_processed_events`; `handleLicensePurchase(session)` is passed **nothing**. Its only
guard is the row lookup at `stripe-webhook.ts:49`, and on a **hit** it unconditionally re-sends
the license email at `:56` before returning. `logSentEmail` (`db-layer.ts:910-926`) is a bare
append-only insert with no unique index and — verified by lens A — is never read by anything,
so it is an audit log, not a dedupe.

| step | actor 1 (delivery 1) | actor 2 (Stripe redelivery) |
|---|---|---|
| 1 | inserts license row, grants credits, then blocks on a slow Resend call | |
| 2 | | Stripe's 10s timeout expires with no 2xx → redelivers **while delivery 1 is still running** |
| 3 | | hits `:49`, finds the row, calls `sendLicenseEmail` **again** (`:56`) |
| 4 | repeats across Stripe's retry schedule | |

**Consequence:** the customer receives their license key three to five times, each a live key
sitting in an inbox. Bounded only by Stripe's retry count, not by anything in the code.

A related asymmetry in the same handler, worth fixing together: the 23505 catch at `:106-116`
`return`s at `:115` **before** the 5,000-credit grant at `:126`, so a retry that loses the
insert race yields a granted key with zero bundle credits — and because `grantCreditLot` *is*
idempotent on `(license_bundle, session.id)`, the repair would have been safe but is
unreachable.

**Fix direction:** thread `event.id` into `handleLicensePurchase` and gate the whole handler on
`stripe_processed_events` the way the credits path already does; make the early-return path
fall through to the grant; and put a unique constraint on `sent_emails` so it can serve as the
dedupe it looks like.

---

### 13. Postgres pool is 10 connections per lambda with an infinite acquisition wait — PLAUSIBLE

**Where:** `nextjs/src/db/index.ts:4` · **Unproven link:** whether the connection string
points at a pooler.

Lens C traced `drizzle(connectionString, {schema})` into `drizzle-orm` and reports it
constructs `new pg.Pool({connectionString})` with library defaults: **max 10, and
`connectionTimeoutMillis` undefined → 0, meaning wait forever**. No `max`, no
`connectionTimeoutMillis`, no `statement_timeout`, no `lock_timeout` is set anywhere.
`spendCreditGrantsByProvenance` holds `FOR UPDATE` row locks for the life of its transaction,
so contention lengthens connection hold times exactly when Vercel is scaling instances up.

Held at PLAUSIBLE because the deciding fact lives in `.env.local`, which the rules of
engagement forbid me from reading. **What would settle it:** whether
`PLANETSCALE_DATABASE_URL` targets a pooled endpoint or the database directly, and the
instance's `max_connections`. If direct, the 11th concurrent transaction on a warm instance
hangs with no timeout until the function times out, starving every route on that instance —
not just credits. A transaction-mode pooler is not a drop-in fix, being incompatible with
session-level constructs.

---

### 14. WebSocket upstream `error` without a following `close` leaks a socket and a timer permanently — PLAUSIBLE

**Where:** `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts:275-277` ·
**Unproven link:** whether Bun's WebSocket always emits `close` after `error`.

The upstream `error` listener only calls `sendToClient` — it neither ends the session nor
closes the client socket. If a Deepgram failure surfaces as `error` with no following `close`
(a TLS reset during handshake, a DNS flap), `endSession` never runs, so the `pingInterval` set
at `:287` is never cleared, and `onMessage`'s guard at `:294` silently drops every audio frame
so the client never errors out either. The 30-second ping exists specifically to defeat Fly's
60-second idle reaper — so the one mechanism that would have reaped the dead session is what
keeps it alive. Permanent socket plus permanent timer, for the machine's lifetime.

**What would settle it:** a runtime check of whether Bun emits `close` after every `error` on a
client WebSocket. Lens D rated its own confidence medium and I did not independently verify
it. Blast radius is high if it does not, which is why it is recorded rather than dropped — and
the fix is cheap either way: have the `error` listener call `endSession()` like every other
terminal path does.

---

### 15. Guest credit-mint pool-by-email check is unbacked, splitting one wallet across two keys — PLAUSIBLE

**Where:** `nextjs/lib/services/stripe-webhook.ts:312-332` · **Unproven link:** I did not read
this handler myself, and unlike findings 7 and 8 I did not verify the absence of a backing
constraint against the schema.

`findAccountByStripeSession` at `:312` dedupes only the *same* session. The pool-by-email check
at `:324-331` — which the comment at `:314-317` says exists to prevent "a second key with a
split balance" — has no unique index behind it, so two different sessions for one guest email
delivered in parallel both pass, and each inserts a key with its own distinct `stripeSessionId`
(so that unique index does not arbitrate either).

**Consequence if real:** the buyer receives two mint emails with two different keys, each
holding half the credits purchased — exactly what the pooling code exists to prevent. No
credits are lost or duplicated, so this is a usability and support-load bug rather than a money
bug, which is the other reason it ranks last.

## Refuted candidates

The long refuted list is the most informative artifact of this hunt — most of these died
against a defence the author had already installed, and a reader should weight that heavily.

- `db-layer.ts:555-618` — *concurrent deductions double-spend.* Refuted:
  `SELECT ... FOR UPDATE` inside `db.transaction`, reconciled in the same locked view. The
  "Atomic SQL decrement (floored at 0)" comment is accurate.
- `stripe-webhook.ts` — *the `checkout.session.completed` / `async_payment_succeeded` twin
  double-enters a handler.* Refuted, and this corrects an assumption I carried into the hunt:
  `webhooks/stripe/route.ts:68` returns early unless `payment_status === "paid"`, and for
  delayed-notification methods `completed` carries `unpaid`. The live vector is plain Stripe
  **retry**, not the twin — which is why finding 12 is framed that way.
- `license-validation.ts:26-109` — *concurrent Polar imports double-grant 5000 credits.*
  Refuted by `uniqueIndex("idx_account_keys_polar_license_key_id")` (`account-keys.ts:38-40`)
  and `credit_grants_source_unique` keyed on the stable `polarResult.id`. The schema comment
  names this exact race.
- Stripe checkout double-insert of a license — refuted by
  `uniqueIndex("idx_account_keys_stripe_session")` (`account-keys.ts:32`).
- *Device/seat cap exceeded by simultaneous activation.* Refuted twice over: there is **no cap
  anywhere** (grep for `max_device`/`deviceLimit`/`MAX_ACTIVATION` returns zero hits), the
  activate/deactivate routes are explicit legacy stubs, and `upsertDeviceValidation`
  (`db-layer.ts:798-818`) arbitrates on `uniqueIndex("idx_device_license_device")`.
- `getCreditBalance` read-compare-heal (`db-layer.ts:640-656`) — refuted on my stated
  criterion: `reconcileCreditBalance` re-reads **inside** the transaction
  (`:335, getActiveGrantsTotal(tx)`), so it never writes a pre-read value. Residual noted by
  two lenses: that in-tx `SELECT SUM` takes no row lock, so the cache can be left stale-high —
  harmless because nothing authoritative reads it (`getCreditBalance` returns the grant total,
  not the cache).
- `credits.ts:125` — *SIGTERM between response flush and deduction registration drops the
  charge.* Refuted: `deductCredits` is called at `transcribe.ts:679`, before the response is
  built at `:695`, and registers synchronously. No window.
- `lib/rate-limit.ts` — *read-then-increment on a counter.* Refuted: both limiters are
  `@upstash/ratelimit` sliding windows executing atomically in Redis. No route implements its
  own counter.
- Client-side stale-response races — **refuted by inspection, not assumed.** Lens E cleared
  `CreditsPurchase.tsx` (explicit `if (loading) return` at `:70` plus a disabled button),
  `CloudCreditsCard.tsx` (every button gated on `loadingTier`), `purchase-success/page.tsx`
  (both effects are pure `setState` from `searchParams`), and the admin clients (tRPC/React
  Query owns cancellation and ordering). For the record: an earlier draft of this report
  guessed at `contexts/UserContext.tsx`, which does not exist — the file is
  `components/user/UserContext.tsx`, and its value is server-rendered and immutable.
- `forEach(async)` / `.map(async)` without `Promise.all` — zero in the cloud tree; the single
  hit in `nextjs` (`lib/services/model-list.ts:160`) is correctly wrapped at `:159`.
- try/catch around an unawaited call in the transcribe fallback chain — none; `:500-501` is
  fully awaited, and every statement-level call in `src/providers/*.ts` is synchronous.
- Provider fallback re-using a consumed body — refuted: `transcribe.ts:431` buffers to an
  ArrayBuffer once and passes the same non-detached buffer to each provider; an ArrayBuffer is
  not consumed by `fetch`.
- `grantCreditsForStripeEvent` (`db-layer.ts:414-443`) — refuted: one transaction, gated on an
  `onConflictDoNothing` insert into `stripe_processed_events` arbitrated by
  `stripe_processed_events_object_id_unique`; the grant runs only if that returned a row.
- `getGoogleAccessToken` single-flight (`google-auth.ts:125-148`) — refuted: no `await` between
  the `_inflight` check and its assignment, so it is atomic on one JS thread.
- GCS object-name collisions — refuted: names embed `Date.now()` plus `crypto.randomUUID()`.
- `post-process.ts:256` versus `:280` double-deduct — refuted: the `:256` site sits inside a
  catch that returns at `:275`; mutually exclusive on every path.
- Network calls inside a `db.transaction` — checked all six transaction sites
  (`db-layer.ts:411, 417, 448, 559, 652, 1010`); every callback is pure DB, with Stripe and
  Resend calls sequenced outside. This sub-lens is clean.

Lower-severity items observed but not promoted, recorded so they are not lost: `getOrCreateUser`
(`db-layer.ts:932-970`) is a read-then-insert whose 23505 is uncaught by two of three callers,
surfacing a race as a 500 rather than as "return the existing user" — bounded, since Stripe
retries, but each 500 widens the window for finding 11; its `user` and magic-link `account`
inserts are not in one transaction, so a failure between them leaves a user who can never sign
in. The blog-post slug probe (`webhooks/add-blog-post/route.ts:111-124`) is a check-then-act
whose `onConflictDoUpdate` arbiter is `externalId`, not the `(locale, slug)` unique index, so a
racing delivery is silently dropped when batched with a success. `LicenseKeysCard.tsx:33` sets
a 2s timeout with no cleanup — a direct regression against `CustomersClient.tsx:27-33`, which
refs and clears the identical pattern.

## Coverage

- **Shared-state items audited:** the mapper enumerated 31 distinct items. The credit and
  license path (Redis `license:<key>`, `credit_grants`/`credit_balances`, `account_keys`,
  `stripe_processed_events`, `inFlightDeductions`, per-WS-connection state) was audited in
  depth. Thinly examined or unaudited: `session` rows (the mapper flagged that nothing revokes
  a session when a license is revoked — not chased, being an authz question outside my lane),
  the SSR `global.localStorage` polyfill at `app/[locale]/layout.tsx:4-15`, the two divergent
  Stripe client `apiVersion`s, ISR revalidation state, and `model-list.ts`'s in-flight
  coalescing cache.
- **Lenses run:** all five, deep tier. A, C, D and E each returned a full candidate set; B
  returned a full set and independently confirmed finding 3. Every promoted finding's key
  constraint claim was re-verified by me against the schema or source before promotion.
- **Scope restriction:** none — full pinned arena, both trees.
- **Read-only compliance:** `git status --porcelain` over `nextjs/` and `hyperwhisper-cloud/`
  shows zero modifications. All repro artifacts live in the scratchpad with a symlinked
  `node_modules`. The pre-existing suite (`bun test src`, 138 tests) and `npx tsc --noEmit`
  both pass unchanged.

Absence of findings outside this coverage means UNEXAMINED, not clean.
