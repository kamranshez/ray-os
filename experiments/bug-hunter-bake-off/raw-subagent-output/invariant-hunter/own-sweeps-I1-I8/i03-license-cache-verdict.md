## Candidate
File: `hyperwhisper-cloud/src/routes/usage.ts`
Line: 48
Invariant: I3
Claim: `validateLicenseAndGetCredits` computes `isValid = data.valid === true` from `response.json().catch(() => ({}))` and calls `cacheLicense` unconditionally — no `response.status` check of any kind, so 500/502/503/429/404 and unparseable bodies all write `isValid:false`.
Failure scenario: A paying user opens the app, which polls `GET /usage?account_key=…`. Vercel is mid-deploy (or cold-starting past the DB pool) and `/api/license/validate` returns a 500 or an HTML error page. `data` becomes `{}`, `isValid` becomes `false`, and `license:<key>` is written `{isValid:false, credits:0}` with a 3600s TTL. From that moment every `POST /transcribe`, `/post-process`, `/assistant` and the Deepgram WS in **every** Fly region hits `validateAuth` → cache HIT → `invalidLicenseResponse()` 401 "Invalid license key". None of the four billable routes pass `forceRefresh`, so nothing can bypass it: the user is locked out of transcription for a full hour even after the Next.js service recovers seconds later.
Confidence: high

## Candidate
File: `hyperwhisper-cloud/src/middleware/auth.ts`
Line: 70
Invariant: I3
Claim: The transient guard is `if (response.status >= 500)` only, so an HTTP **429** — which the licensing API itself emits at `nextjs/app/api/license/validate/route.ts:65` with the body `{valid:false, error:"Too many requests. Please try again later."}` — is treated as a definitive verdict and cached as `isValid:false`.
Failure scenario: `licenseValidateRateLimiter` is `slidingWindow(30, "1 m")` keyed on `getClientIPFromHeaders`, which for a server-to-server call from Fly resolves to the Fly machine's shared NAT egress IP (or `"unknown"` if no forwarded header survives) — one bucket for *all* HyperWhisper Cloud traffic out of that region, not one per user. The 31st cache-miss validation in any 60-second window returns 429; `429 < 500`, so `cacheLicense(key, {isValid:false, credits:0})` fires. Every user whose validation landed in that burst is 401'd out of transcription for the next hour, and because each lockout suppresses further validate calls the outage is self-concealing. Same path for any Vercel-edge 4xx (403 firewall, 404 during a deploy swap, 408) where the body isn't the app's own JSON.
Confidence: high

## Candidate
File: `hyperwhisper-cloud/src/middleware/auth.ts`
Line: 51
Invariant: I3
Claim: A `JSON.parse` failure on the response body is logged (`[License] Invalid JSON response…`) but execution continues with `data = {}` → `isValid = false`; the code then falls through to `cacheLicense` for any status below 500, so an unparseable body is cached as a definitive "invalid".
Failure scenario: Vercel returns a 200 (or 4xx) whose body is not the expected JSON — a Vercel deployment-protection / SSO interstitial, a WAF challenge page, a gzip/transfer truncation, or a `Retry-After` HTML page. `data.valid` is `undefined`, `isValid` is `false`, and the poisoned entry is written with the 1h TTL. The user's next transcription attempt, and every one for the next hour across all regions, returns 401 "Invalid license key" despite the licensing API being healthy. The invariant explicitly names "unparseable body" as a case that must leave the cache untouched; the code only logs it.
Confidence: high

## Candidate
File: `nextjs/src/lib/license-validation.ts`
Line: 136
Invariant: I3
Claim: `checkLicenseKey` maps **every** failure of `importLicenseFromPolar` — including its outer `catch (err)` that swallows Polar network errors, Polar 5xx, SDK timeouts, and any throw from `getOrCreateUser` / `insertAccountKey` — to `status: 400`, which the validate route returns verbatim (`route.ts:103`) and which the cloud's 5xx-only guard then caches as a definitive `isValid:false`.
Failure scenario: A legacy Polar-issued license not yet imported into the local DB (exactly the population this fallback exists for) is validated while Polar's API is down or the DB write leg fails transiently. `importLicenseFromPolar` returns `{success:false, error:"Failed to validate with Polar"}`, `checkLicenseKey` returns `status:400`, the route responds `400 {valid:false}`, and `auth.ts` — seeing `400 < 500` — writes `isValid:false` for 3600s. The customer is locked out for a full hour by an outage in a third party that had nothing to say about their license's validity, and re-validation is suppressed for the whole TTL. The transient case (`catch (err)` at line 102) is indistinguishable at the wire from the definitive case (Polar says `status !== "granted"`, line 39) because both emit 400.
Confidence: high

## Candidate
File: `hyperwhisper-cloud/src/lib/redis.ts`
Line: 70
Invariant: I3
Claim: No write-through invalidation of `license:<key>` exists anywhere in the Next.js service — a grep for `license:` key writes/deletes across all of `nextjs/` returns nothing (the Next.js Redis client at `nextjs/lib/clients/redis.ts` is used only by `@upstash/ratelimit`) — so a poisoned `isValid:false` entry cannot be cleared by a credit purchase, a support action, or a license re-grant; it can only expire.
Failure scenario: Turns each of the four writes above from a recoverable glitch into a hard 1-hour outage with no operator remedy. A user who is wrongly cached invalid, then buys credits or contacts support, still gets 401 "Invalid license key" on every transcription until the TTL elapses; the only mitigation available is manually deleting the Upstash key. (Reported as a severity multiplier on the invariant rather than an independent write-site violation.)
Confidence: low

### Coverage
**Examined buckets:**
- **B1 (cloud-entry-and-auth)** — read in full: `lib/redis.ts` (all three helpers; `cacheLicense` swallows Redis errors, `getCachedLicense` returns `null` on error → fails open, correct), `lib/constants.ts` (`LICENSE_CACHE_TTL_SECONDS = 3600`, `LICENSE_API_TIMEOUT_MS = 10_000`), `middleware/auth.ts` end to end, `middleware/credits.ts` end to end.
- **B2 (cloud-routes)** — `routes/usage.ts` read in full; the other four routes grepped for `cacheLicense`/`getCachedLicense` (zero hits) and for `validateAuth(` call sites (`transcribe.ts:396`, `post-process.ts:109`, `assistant.ts:302`, `ws-streaming-deepgram.ts:154` — **none** passes `forceRefresh`, confirming a poisoned entry has no bypass on any billable path).
- **B6 (next-money-api)** — `app/api/license/validate/route.ts` and `app/api/license/credits/route.ts` read in full, tracing every status code the cloud can observe (400/429/500 from validate; 400/409/500 from credits).
- **B7 (next-edge-auth-and-misc-api)** — `src/lib/license-validation.ts` read in full; `lib/rate-limit.ts` and `getClientIPFromHeaders` in `server/api/routers/download-ip.ts` read to establish the 429 blast radius.
- **B9 (next-db-and-services)** — `lib/clients/redis.ts` read; repo-wide grep for `license:` key manipulation in `nextjs/` confirms no cache-invalidation path exists.

**Not examined / partially examined:** B3, B4, B5, B8, B10, B11, B12 — swept by grep for `cacheLicense`/`getCachedLicense`/`license:` key writes with zero hits; the invariant has no surface there. `app/api/account/*` aliases were not read individually: the cloud service only ever calls `/api/license/validate` and `/api/license/credits` (both `apiBase` constructions in `auth.ts:30`, `usage.ts:37,64`, `credits.ts:61`), so the aliases cannot reach `cacheLicense`. `deductCreditBalance` / `getCreditBalance` internals in `db-layer.ts` were not read — they affect the `credits` field, not `isValid`.

**Leads refuted:**
- `middleware/auth.ts:70-79` is **not** fully correct, contrary to the brief. Its `status >= 500` guard is real and handles the 5xx case, and its outer `catch` correctly declines to cache on timeout/network failure — but it leaves three transient 4xx/2xx paths uncovered (429 from the app's own rate limiter, Vercel-edge 4xx, and JSON-parse failure at any status). The file's own comment asserts "A 4xx … is a definitive verdict", which is the mistaken premise.
- `middleware/credits.ts:86` is **clean**: it only ever writes `isValid:true`, is gated on `response.ok` (line 74) *and* on `typeof data.credits_remaining === 'number'`, so it can never write an `isValid:false` entry.
- `routes/usage.ts:81` (`getCreditsBalance`) is **clean for I3**: it is guarded by `if (!response.ok)` returning early, and by a `readFiniteCredits(data) === null` check, and only writes `isValid:true`.
- `routes/usage.ts:55` — the `catch` wrapping the fetch correctly returns `{isValid:false}` *without* caching, so timeout/network failures at that site are handled.
- `app/api/license/validate/route.ts:130` correctly returns **500** for an unexpected throw (DB error in `findAccountByKey` or `getCreditBalance`), which the cloud's guard does handle. The 400 leak is confined to the Polar-fallback path described in candidate 4.
