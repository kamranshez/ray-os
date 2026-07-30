I've completed the sweep. Here are my findings.

### Candidate
File: `nextjs/app/api/license/credits/route.ts`
Line: 80
Invariant: I7
Claim: `POST /api/license/credits` (and its alias `/api/account/credits`, a bare `export { GET, POST }` re-export) performs an unauthenticated, unlimited durable write — `deductCreditBalance(license.userId, amount)` at line 119 — with the bare license key as the sole credential and no `RateLimiter.limit()` call anywhere in the file.
Failure scenario: Anyone holding a leaked/shared account key (it travels in plaintext query strings and request bodies from the desktop app and the Fly service) scripts a loop of `POST {license_key, amount: 1000000}`. Each request commits an atomic decrement, so the victim's balance hits 0 within one request and stays there; every subsequent transcription from their Mac app returns "insufficient credits". Even without a valid key, an attacker drives one `findAccountByKey` DB round-trip per request at unbounded rate, exhausting the `node-postgres` pool and 500-ing `/api/license/validate` for every real user during the burst. The sibling `/validate` and `/activate` handlers in the same directory *do* call `licenseValidateRateLimiter.limit(clientIP)` as their first statement, so this is an inconsistency within one module, not a global policy gap.
Confidence: high

### Candidate
File: `nextjs/app/api/checkout/credits/route.ts`
Line: 36
Invariant: I7
Claim: `POST /api/checkout/credits` takes no auth and no rate limit, yet every accepted request calls `stripe.checkout.sessions.create` (line 147), and the top-up path additionally calls `stripe.customers.list` + `stripe.customers.create` (lines 126-134) plus a DB write `updateAccountKey(license.id, {stripeCustomerId})` (line 141).
Failure scenario: A single unauthenticated attacker POSTs `{"amount": 5}` in a loop. Each POST creates a real, durable Stripe Checkout Session in the live account and consumes 1-3 Stripe API calls. Stripe's live-mode limit is ~100 write requests/sec per account; a modest flood trips it, and Stripe then 429s the *legitimate* traffic that shares that account — specifically `stripe.webhooks`-driven work and real buyers' `sessions.create` calls, so paying customers who click "Buy credits" get "Failed to create checkout session" (the line 215 catch) while the attacker's junk sessions fill the Stripe dashboard and skew Stripe's abuse/fraud signals. `/api/checkout/credits` is not covered by `middleware.ts` (matcher at line 159 excludes `api`) and `vercel.json` declares no firewall rules, so there is no gate in front of it either.
Confidence: high

### Candidate
File: `nextjs/app/api/internal/models/route.ts`
Line: 8
Invariant: I7
Claim: Despite sitting under `/api/internal/`, this handler has no `timingSafeEqualSecret(..., HYPERWHISPER_INTERNAL_SECRET)` check (unlike all three sibling `/api/internal/*` routes) and no rate limiter; a cache-miss calls `fetchAvailableModels()`, which fans out to 6 paid provider APIs using `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, `XAI_API_KEY`, `CEREBRAS_API_KEY`.
Failure scenario: The two claimed bounds do not hold together. `Cache-Control: s-maxage=3600` keys on the full URL, so `GET /api/internal/models?bust=<random>` is a guaranteed edge MISS and invokes the function. The `cache`/`inFlight` module-level state in `nextjs/lib/services/model-list.ts:186-187` is per-lambda-instance, so N *concurrent* cache-busted requests cause Vercel to scale out to N cold instances, each of which does its own full 6-provider fan-out — including the unbounded `while (url)` pagination loops in `fetchAnthropic` (line 69) and `fetchGemini` (line 90). A few hundred concurrent junk requests therefore produce hundreds of authenticated calls on the org's real provider keys. Anthropic and OpenAI rate-limit per organization, so the resulting 429s land on the *production* HyperWhisper Cloud LLM traffic sharing those keys: users' `/post-process` and `/assistant` requests start failing while the attacker pays nothing. Note also `apiGet` (line 24) passes no `AbortSignal`, so each stalled fan-out pins its lambda for the full max-duration.
Confidence: medium

### Candidate
File: `nextjs/app/models/route.ts`
Line: 8
Invariant: I7
Claim: Byte-identical unauthenticated, unrate-limited public entry point into the same 6-provider `fetchAvailableModels()` fan-out, and it is explicitly carved out of `middleware.ts`'s matcher (`models(?:/|$)`, line 159) so nothing runs in front of it.
Failure scenario: Same amplification as above, but on the vanity public path a scraper is far more likely to find and hammer. Because both routes share the same module-level `cache` variable *within* an instance but not across instances, alternating `/models?x=1` and `/api/internal/models?x=1` from many connections multiplies cold instances and thus provider fan-outs. Downstream symptom is identical: provider-side 429s on the shared org keys degrade paid cloud transcription/post-processing for real users.
Confidence: medium

### Candidate
File: `nextjs/src/lib/auth.ts`
Line: 23
Invariant: I7
Claim: The `magicLink` plugin's `sendMagicLink` calls `resend.emails.send(...)` (line 25) to an arbitrary caller-supplied address on every unauthenticated `POST /api/auth/sign-in/magic-link`, and `betterAuth({...})` here declares no `rateLimit` config, no `rateLimit.storage`, and no `secondaryStorage` — while the author of `auth-license-key-plugin.ts` explicitly attached a `rateLimit: [{pathMatcher: "/sign-in/license-key", window: 60, max: 5}]` rule (lines 88-96) to the sibling endpoint, showing the protection was considered and applied to only one of the two sign-in paths.
Failure scenario: An attacker POSTs magic-link requests for a list of harvested email addresses. Each one sends a real Resend email from `DEFAULT_FROM_EMAIL` and writes a durable Better Auth `verification` row. Recipients who never asked for it mark the mail as spam; the resulting complaint rate on the sending domain gets the domain throttled or suspended by Resend, at which point *all* transactional mail stops — including the webhook-minted account key email that `/api/checkout/credits` buyers depend on to ever receive what they paid for. Better Auth's fallback here is its default in-memory limiter, which on Vercel is per-lambda-instance and therefore does not bound a distributed or high-concurrency burst.
Confidence: medium

### Candidate
File: `nextjs/app/api/download/route.ts`
Line: 106
Invariant: I7
Claim: `GET /api/download` is `export const dynamic = "force-dynamic"` with no rate limiter, and every request performs an outbound `fetch(appcastUrl, {cache: "no-store"})` (line 50) — a request-per-request amplifier with no caching of any kind.
Failure scenario: Each inbound GET costs one function invocation plus one full outbound HTTP fetch back to the same deployment for `public/appcast.xml`, roughly doubling billed edge requests per hit. A sustained flood on the most-linked public URL on the site (every "Download" button and the welcome email's `${origin}/api/download` link point here) burns Vercel function invocations and bandwidth with no attacker cost. Weaker than the others: the appcast is same-origin static, not a paid third-party API, and there is no durable write — so this is cost burn only, not quota exhaustion against an external provider.
Confidence: low

### Coverage

**Examined buckets:** B6 (next-money-api — all of `app/api/license/**`, `app/api/account/**`, `app/api/checkout/**`, `app/api/webhooks/**`); B7 (next-edge-auth-and-misc-api — all of `app/api/{internal,config,customer,download,auth,trpc}/**`, `app/models/route.ts`, `middleware.ts`, `src/lib/{auth,auth-license-key-plugin}.ts`, `lib/rate-limit.ts`); B8 partially (`server/api/routers/download.ts` and `download-ip.ts`, the only publicly-reachable tRPC procedures); B9 partially (`lib/services/model-list.ts`, `lib/clients/redis.ts`) as the fan-out targets. Also checked `vercel.json` and `next.config.mjs` for any platform-level limiter — there are none.

**Not examined / partially examined:** B1-B5 (all of `hyperwhisper-cloud/`) — I7 is scoped to Next.js route handlers by definition. B8's protected/admin tRPC routers, B9's DB and email services, B10/B11 (React UI), B12 (tests) — no unauthenticated route handlers in them; the only handler-shaped file in B11, `app/[locale]/user/auth/sign-out/route.ts`, has no third-party or durable-write work. I did not read `node_modules`, so Better Auth's exact default rate-limit values and storage backend are inferred from the absence of config in `src/lib/auth.ts` rather than read from the library — that is the reason candidate 5 is medium and not high.

**Leads refuted:**
- **The rate limiter failing OPEN when Upstash is unreachable — refuted.** `licenseValidateRateLimiter` is constructed with no `timeout` and no `ephemeralCache` option (`lib/rate-limit.ts:27-32`), so `.limit()` rejects rather than resolving on a Redis error. At both call sites — `license/validate/route.ts:62` and `license/activate/route.ts:30` — the `await` sits *before* and *outside* any `try` block, so the rejection propagates to Next.js and the request 500s. That is fail-closed. The third call site, `server/api/routers/download.ts:145`, is inside a `try`, but its `catch` (line 232) re-throws as an `INTERNAL_SERVER_ERROR` rather than continuing — also fail-closed. Missing `UPSTASH_REDIS_REST_URL`/`_TOKEN` in `lib/clients/redis.ts` produces the same rejection path.
- **`/api/license/credits` GET — refuted under I7.** It does a DB read (`findAccountByKey` + `getCreditBalance`) only; no paid third party and no durable write, so it fails the "real cost or durable write" bar even though it is genuinely unauthenticated and unlimited. It is a free license-key-existence oracle, but that belongs to whoever owns the auth/enumeration invariant, not I7.
- **`s-maxage=3600` + in-memory TTL bounding the models fan-out — partially refuted**, and that partial refutation is the substance of candidates 3 and 4: the TTL is real and does collapse repeat traffic on a warm instance (including in-flight dedup at `model-list.ts:191`), but it is per-instance module state, so it does not survive Vercel horizontal scale-out under a concurrent cache-busted burst.
- **`getClientIPFromHeaders` being spoofable to defeat the limiter — not reported.** `download-ip.ts:16` reads `x-vercel-forwarded-for` first, which Vercel's edge sets and a client cannot forge, so the spoofable `cf-connecting-ip` / `x-forwarded-for` / `x-real-ip` fallbacks at lines 17-19 are unreachable on the production deployment. Worth flagging only if this is ever run off Vercel.
- **`/api/config`, `/api/checkout` (GET), `/api/license/deactivate` — refuted.** Static JSON constants, a `NextResponse.redirect`, and an always-200 stub respectively. No cost, no writes.
- **`/api/webhooks/stripe` and `/api/webhooks/add-blog-post` — refuted.** Not unauthenticated: signature-verified and bearer-token-gated before any mutation.
