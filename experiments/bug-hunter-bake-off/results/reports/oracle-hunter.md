---
skill: oracle-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 8 |
| PLAUSIBLE findings | 7 |
| Findings with an executable repro | 5 |
| Files opened (of 210 in scope) | ~95 |
| Subagents spawned | 10 |
| Strategy came up dry? | no |

## Coverage ledger

**What this strategy did.** Ran every cheap mechanical oracle over the pinned arena, turned the output into a ranked lead list, then spent agent attention only where a tool had already flagged something. No free-reading of the codebase hunting for bugs — that is another entrant's job. Every finding below traces to a named oracle signal.

**Oracles run, and what each one actually said:**

| Oracle | Result | Verdict as a lead source |
|---|---|---|
| `bun test src` (cloud) | 138 pass, 0 fail, **0 skipped, 0 todo** | Near-silent. No skip-archaeology existed to do. One loud side-signal: a swallowed credit-report network error printed during a *passing* test. |
| `bun run typecheck` (cloud) | clean | Silent |
| `npx tsc --noEmit` (nextjs) | **0 errors** | Silent |
| `npx eslint .` (nextjs) | **could not execute** | Became a finding in itself (F2) |
| Strict re-run, cloud (+`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitReturns`, `noFallthroughCasesInSwitch`, `noImplicitOverride`) | 163 errors, ~120 of them TS4111 style noise | Loud but low-yield; its money-arithmetic leads were REFUTED by explicit `?? fallback` guards |
| Strict re-run, nextjs | baseline 0 → **98 new errors** | Loud; produced F15 |
| Suppression archaeology | **0** TODO/FIXME/HACK/XXX/WORKAROUND in 31,181 lines; 2 `@ts-expect-error`, 2 `eslint-disable`, 4 non-test `as any`, 12 non-null assertions | Thin but extremely high-precision — the entire archaeology record is ~20 lines, and 2 of them led to F10 |
| Dead code / unused exports | 25 zero-external-reference exports | **Mostly false positives** — see waste note below |
| Dependency audit | cloud clean; nextjs **25 advisories** (1 critical, 14 high) | Advisories themselves were unreachable build-tooling noise, but the audit exposed F3 |

**Deliberately skipped, and why.** `npm run lint` was never run — it is `eslint --fix` and would have mutated the tree. Anything requiring a live DB, real Stripe/licence API calls, or network side effects was declined. The 25 dependency advisories were triaged by reachability and all landed BUILD-ONLY or TRANSITIVE-UNREACHED (`tar` via `@tailwindcss/oxide`, `dompurify` via `posthog-js`); none are reported as findings, because an advisory the app never reaches is not a bug.

**What this strategy is structurally blind to on this codebase — read this before trusting the counts.**

This hunt saw only what the oracles pointed at. On *this* repo that blind spot is unusually large, for a specific and important reason: **the mechanical oracles here are nearly silent.** Zero failing tests, zero skipped tests, zero TODO markers, and a clean typecheck on both projects. A lead-driven hunt is only as good as its lead list, and this codebase deliberately refuses to generate leads. Concretely invisible to this strategy:

- **All logic with no test, no type error, and no suppression on it.** That is the majority of the 210 files. 17 of 21 cloud providers have no test file; `src/routes/post-process.ts` has none; `src/middleware/auth.ts` and `credits.ts` have none — yet three of my highest-severity findings live in exactly those two untested middleware files, found only because a *different* oracle (a swallowed-error grep, an asymmetry scan) happened to point at them. The same class of bug in a file no oracle touched would have been missed entirely.
- **Semantic and business-logic bugs.** Correct-looking, well-typed code that computes the wrong answer is invisible here. No oracle can flag it.
- **Anything git-archaeology would find.** History is squashed into one "initial public open-source release" commit (e3708d4, 2026-06-30), so `git blame`/`git log -S` recovered no intent for any suppression. A whole ranking dimension of this skill (age of suppression) was unavailable.
- **`nextjs/components/`, `app/[locale]/` marketing pages, `scripts/`** — deprioritized as low-risk; only opened where an oracle pointed.

**Do not read "8 CONFIRMED" as "8 bugs exist."** Read it as "8 bugs sat behind the ~40 places a machine already flagged."

**Phase 3 caveat — stated plainly.** The skill specifies an independent adversarial verifier subagent per candidate, told only the claim and not the chaser's confidence. **That phase did not run.** The session-wide subagent pool (20, shared across all ten hunters) was saturated for the entire hunt; I could not hold slots for a second verification wave. Findings F1–F5 carry executable repros I ran myself and are solid. F6–F8 are graded CONFIRMED on the strength of a complete trigger path plus decisive quoted code from the chaser, **but they have not been independently adversarially re-checked**, and that is a real weakening of the verification bar the brief sets. F9–F15 are PLAUSIBLE with the unproven link named in each.

---

# Oracle Hunt — hyperwhisper-public (deep)

## Verdict summary

The oracles on this repo are unusually quiet — no failing tests, no skipped tests, no TODO markers, a clean typecheck on both projects — so the classic high-yield surface (fossilized human judgment calls) was almost absent. The leads that did exist were correspondingly high-precision: a ~20-line total suppression record produced the Stripe finding, and a swallowed-error grep plus a guard-asymmetry scan produced four money-accounting bugs in the two untested middleware files. The single loudest oracle turned out to be one nobody thinks of as an oracle: **the lint and test tooling itself is broken and disconnected**, which is both a finding and the reason several other findings survived to HEAD. 15 leads survived verification out of ~40 chased; the dead-code oracle was the weakest performer, producing 25 leads of which 20 were false positives.

## Findings (ranked: repro'd > CONFIRMED > PLAUSIBLE)

### 1. `nextjs/src/lib/license-key-redirect.ts:14` — open redirect: sanitizer blocklist misses tab/CR/LF, which the URL parser then strips [CONFIRMED, repro'd] — HIGH

- **Oracle:** [D-scan] zero-external-reference export `DEFAULT_LICENSE_KEY_REDIRECT` pointed at this file; the orphaned-test oracle (F4) then showed `nextjs/tests/license-key-redirect.test.ts` tests *precisely this function's open-redirect protection* — and that test never runs anywhere.
- **Failure:** `sanitizeReturnTo` is a blocklist (`startsWith("/")` && `!startsWith("//")` && `!startsWith("/\\")`). ASCII tab, LF and CR are not blocked, but the WHATWG URL parser **strips** them — so `/\t/evil.com` survives sanitization and then collapses to protocol-relative `//evil.com` on the very next line.
- **Trigger path:** attacker sends an authenticated user a link to `https://www.hyperwhisper.com/en/user/sign-in?returnTo=/%09/evil.com` → `middleware.ts` matcher admits the path → `:78` `isUserSignIn` → `:133` `hasSessionCookie` true → `:135` `searchParams.get("returnTo")` **percent-decodes to the literal `"/\t/evil.com"`** (this decode step is load-bearing) → `:136` `sanitizeReturnTo` accepts it → `:137` `NextResponse.redirect(new URL(redirectUrl, request.url))` → `Location: https://evil.com/`.
- **Repro:** `/private/tmp/.../scratchpad/oracle-hunter/repro/open-redirect.test.ts`, run with `cd /Users/ray/Desktop/hyperwhisper-public/nextjs && npx tsx <path>` → exit 1:
  ```
  contained  returnTo="//evil.com"      -> Location: https://www.hyperwhisper.com/en/user/dashboard
  ESCAPES    returnTo="/\t/evil.com"    -> Location: https://evil.com/
  ESCAPES    returnTo="/\n/evil.com"    -> Location: https://evil.com/
  ESCAPES    returnTo="/\r/evil.com"    -> Location: https://evil.com/
  4 of 7 payloads reach an off-origin Location header
  ```
  Independently reproduced end-to-end by a second agent, including the percent-decode step.
- **Note (a REFUTED sibling, worth recording):** the same tainted value flows into better-auth as `callbackURL` from `sign-in/page.tsx:44`, and `nextjs/src/lib/auth.ts` sets **no** `trustedOrigins`. That variant is **REFUTED**: better-auth registers `originCheckMiddleware` on `path: "/**"` (`dist/api/index.mjs:157-160`), covering the custom license-key plugin endpoint too, and its relative-path validator is an *allowlist* regex `/^\/(?!\/|\\|%2f|%5c)[\w\-.\+/@]*.../` whose character class excludes tab/CR/LF/%. All payloads are rejected 403 before the handler runs. The bug is in the middleware branch only, which never consults better-auth.
- **Suggested fix:** make `sanitizeReturnTo` an allowlist, or strip `[\t\r\n]` before the prefix checks; add the three payloads to the existing test file.

### 2. `nextjs/eslint.config.mjs:13` — ESLint has never been able to run: config imports an undeclared package [CONFIRMED, repro'd] — MEDIUM

- **Oracle:** [N] the eslint oracle itself failed to execute.
- **Failure:** `import js from "@eslint/js";` at line 13. `@eslint/js` appears in **neither** `dependencies` nor `devDependencies` (every *other* eslint package is declared — `@eslint/compat`, `@eslint/eslintrc`, and 13 more), and is not installed under `node_modules/@eslint/` (only `compat` and `eslintrc` are there). Under pnpm's strict layout an undeclared dep is unresolvable.
- **Trigger path:** any developer or CI runner executing `npm run lint` (or `npx eslint .`) in `nextjs/`, on any file, always.
- **Repro:** `cd /Users/ray/Desktop/hyperwhisper-public/nextjs && npx eslint .` → exit 2:
  ```
  Error [ERR_MODULE_NOT_FOUND]: Cannot find package '@eslint/js' imported from
    /Users/ray/Desktop/hyperwhisper-public/nextjs/eslint.config.mjs
  ```
- **Why this is a finding and not hygiene — three suppressions compound:** (a) lint cannot run at all; (b) `next.config.mjs` sets `eslint: { ignoreDuringBuilds: true }`, so it would not gate a build even if it could; (c) there is **no nextjs CI workflow** (`.github/workflows/` holds only cloud-deploy, macos, windows and shared-core). So no correctness lint rule — `@next/next/*`, `no-fallthrough`, `no-case-declarations`, `jsx-a11y` — has been enforced anywhere for an unknown period. A fourth compounding fact: `eslint.config.mjs` sets `"react-hooks/exhaustive-deps": "off"` **globally**, which makes the one `eslint-disable-line react-hooks/exhaustive-deps` in the codebase redundant and means every missing-dependency hook bug is invisible.
- **Suggested fix:** add `@eslint/js` to devDependencies; drop `ignoreDuringBuilds`; add a nextjs CI job.

### 3. `nextjs/pnpm-lock.yaml:120` + `nextjs/vercel.json` — production installs are unpinned, and the lockfile contradicts the manifest [CONFIRMED, repro'd] — MEDIUM

- **Oracle:** [P] dependency audit.
- **Failure:** three facts that only make sense together. `package.json` pins `"next": "15.5.21"` (exact, no caret). `pnpm-lock.yaml:120` pins `specifier: 15.5.18`. `node_modules` has 15.5.18 — inside advisory **GHSA-955p-x3mx-jcvp** (`>=13.0.0 <15.5.21`, patched `>=15.5.21`). So someone bumped the manifest to the patched version and never regenerated the lockfile. Then: `vercel.json` sets `"installCommand": "npm install"`, and there is **no `package-lock.json`** — only a pnpm lockfile, which npm cannot read. So deploys ignore the lockfile entirely and resolve all 27 caret-ranged dependencies fresh at build time.
- **Trigger path:** every production deploy. Local dev (pnpm, `next@15.5.18`, vulnerable) and production (npm, resolves `15.5.21`+) run **different dependency trees**; nothing pins what ships.
- **Repro:** `node /private/tmp/.../scratchpad/oracle-hunter/repro/lockfile-divergence.mjs` → exit 1, four assertions fail:
  ```
  FAIL: manifest pins next@15.5.21 but pnpm-lock.yaml pins next@15.5.18 (lockfile is stale)
  FAIL: lockfile next@15.5.18 is vulnerable per GHSA-955p-x3mx-jcvp (patched >=15.5.21)
  FAIL: node_modules next@15.5.18 is vulnerable per GHSA-955p-x3mx-jcvp
  FAIL: vercel.json runs "npm install" but there is no package-lock.json — npm cannot read
        pnpm-lock.yaml, so all 27 caret/tilde-ranged deps resolve fresh at deploy time
  ```
- **Suggested fix:** pick one package manager; make `installCommand` match the lockfile actually committed; regenerate the lockfile.

### 4. `nextjs/package.json` — 26 passing tests that nothing ever runs [CONFIRMED, repro'd] — MEDIUM

- **Oracle:** [C] test-runner discovery.
- **Failure:** `nextjs/tests/` holds 5 test files / 26 tests covering exactly the security-sensitive pure logic — credit-purchase validation, licence-credit validation (including `JSON.parse('{"amount":1e999}')` → `Infinity`), download- and geolocation-IP validation, and the license-key redirect sanitizer. `package.json` has **no `test` script**, and there is no nextjs CI workflow. They pass, and they are never run.
- **Trigger path:** any regression in the validators these cover ships unnoticed. F1 is the concrete instance: `license-key-redirect.test.ts` exists to prevent open redirects, and an open redirect shipped anyway.
- **Repro:** `cd /Users/ray/Desktop/hyperwhisper-public/nextjs && npx tsx --test tests/*.test.ts` → `# pass 26 / # fail 0`, only reachable by invoking the runner by hand.
- **Suggested fix:** add `"test": "tsx --test tests/*.test.ts"` and a CI job.

### 5. `hyperwhisper-cloud/src/lib/cost-calculator.ts:499` — live money conversion floors zero-cost sessions to 0.1 credits; its dead twin returns 0 [CONFIRMED, repro'd] — LOW/MEDIUM

- **Oracle:** [D2] zero-external-reference export `estimateCreditsForCost` sitting beside a live `creditsForCost`.
- **Failure:** `creditsForCost` opens `if (!Number.isFinite(costUsd) || costUsd <= 0) return 0.1;`. The dead `estimateCreditsForCost` returns `0` for the same input. Two downstream guards (`ws-streaming-deepgram.ts:208`, `credits.ts:140`) were written against the dead function's contract and so never fire.
- **Trigger path:** client opens `wss://…/ws/streaming-deepgram?license_key=K`, clears preflight, closes before sending any PCM (double-tapped hotkey, wifi drop) → `endSession` with `totalDurationSeconds = 0` → `computeDeepgramTranscriptionCost(0)` = 0 → `creditsForCost(0)` = **0.1** → both guards pass → user billed 0.1 credits for an empty session.
- **Repro:** chaser's Bun test, 9 pass / 39 assertions: `creditsForCost(NaN) = 0.1`, `creditsForCost(undefined) = 0.1`, `estimateCreditsForCost(NaN) = 0`.
- **Note:** `cost-calculator.test.ts` imports only the eight `compute*` helpers — `creditsForCost`, `usdToCredits`, `estimateCreditsForCost` and `roundUsd` have no assertions anywhere. The one function that decides what every user is charged is the one the money-conversion test file does not test.

### 6. `hyperwhisper-cloud/src/middleware/credits.ts:145` — a failed credit deduction is indistinguishable from a successful one [CONFIRMED, no independent verifier] — HIGH

- **Oracle:** [A1] `.catch(() => {})` at `credits.ts:127` with the comment *"errors are logged inside performDeduction / by callers"*, plus the loud test-run signal `POST /api/license/credits network error { error: "Unexpected fetch: ..." }` printed during a **passing** test.
- **Failure:** the comment is false in both halves. `recordLicenseUsage` swallows both the non-2xx branch (74-82) and the exception branch (92-96) and returns void; `performDeduction` contains no logging and unconditionally returns `creditsUsed`. Because the promise therefore **never rejects**, every `.catch(console.error)` at `transcribe.ts:692`, `post-process.ts:267`/`:291`, `assistant.ts:363` and `ws-streaming-deepgram.ts:220` is unreachable dead code. There is no retry, dead-letter or reconciliation.
- **Trigger path:** revoke or refund a licence. Nothing in `nextjs/` ever deletes the cloud's `license:<key>` Redis entry (only writers are `auth.ts:75` and `credits.ts:86`, TTL `LICENSE_CACHE_TTL_SECONDS = 3600`), so `validateAuth` keeps returning a cache HIT with `isValid:true` and the pre-revocation balance. `POST /api/license/credits` then returns `400 {"error":"License is revoked"}` (`nextjs/app/api/license/credits/route.ts:107-112`) → one `console.warn` → normal return. **The user gets unlimited transcriptions for up to an hour with the balance untouched and no error raised.** Identical silent forfeiture for any licence-API 5xx or >10s stall.
- **Suggested fix:** make `performDeduction` reject on failure and persist failed deductions for retry.

### 7. `hyperwhisper-cloud/src/middleware/auth.ts:70` — HTTP 429 from the licence API is cached as `isValid:false` for a full hour [CONFIRMED, no independent verifier] — HIGH

- **Oracle:** [D1] guard-asymmetry scan around the auth cache.
- **Failure:** the transient-failure guard is `if (response.status >= 500)`. A 429 is not ≥500, so control falls through to `cacheLicense(licenseKey, {isValid:false, credits:0})` at line 75 with a 3600s TTL. The author's own comment at line 61 states this exact outcome must not happen — *"caching it would lock a paying user out for the full LICENSE_CACHE_TTL_SECONDS"*. 5xx was handled; 429 was missed.
- **Trigger path:** `validateLicenseViaApi` sends no `x-forwarded-for`, so `/api/license/validate` sees the **Fly machine's egress IP** and every Cloud user shares one `licenseValidateRateLimiter` bucket of 30 req/min. A TTL-expiry thundering herd, 30 cache-missing users in a minute, or a flood of the un-negatively-cached malformed-key loop (F11) trips it → 429 → poisoned cache → every subsequent `/transcribe`, `/post-process`, `/assistant`, `/ws/streaming-deepgram` reads the poisoned entry (all call `validateAuth` with `forceRefresh=false`) and 401s a **paying customer for an hour**.
- **Suggested fix:** treat 429 (and any non-4xx-verdict status) as transient; forward the real client IP.

### 8. `hyperwhisper-cloud/src/routes/usage.ts:48` — `/usage`'s hand-rolled validator caches 5xx as `isValid:false` for an hour [CONFIRMED, no independent verifier] — HIGH

- **Oracle:** [D2] guard-asymmetry scan — `usage.ts` is the only route calling neither `validateAuth` nor `validateCredits`.
- **Failure:** `validateLicenseAndGetCredits` never inspects `response.status`. `const data = await response.json().catch(() => ({}))` (line 44) turns a 503 body into `{}`, `data.valid === true` is false, and line 48 unconditionally caches `{isValid:false, credits:0}` for 3600s — the precise case `auth.ts:70-73` deliberately refuses to cache. (Its own `catch` at 55-57 *does* correctly skip caching on network errors, so the omission is specific to the HTTP-status path.)
- **Trigger path:** licensing API returns 503 (cold start, deploy, upstream timeout) while a client polls `GET /usage?license_key=K` → `index.ts:54` → `usage.ts:128` → `usage.ts:48` poisons the shared cache → for the next hour every other route 401s that paying customer via `auth.ts:113-115`. No route escapes it; the only force-refresh path in the service is `/usage?force_refresh=true` itself.
- **Note — the rest of the `usage.ts` asymmetry is BENIGN:** it fails closed on both ends (401 at `:152` and `:133-135`) and applies the same IP guard as all four siblings (`:96`). Skipping `validateCredits` is correct — `/usage` consumes nothing. It returns only the caller's own balance for a key the caller already supplied.
- **Suggested fix:** reuse `validateAuth`'s status handling instead of a second copy.

### 9. `hyperwhisper-cloud/src/index.ts:95` — shutdown drain does not cover the two long-lived endpoints [PLAUSIBLE] — MEDIUM/HIGH

- **Oracle:** [A1] signal 7 (`drainPendingDeductions` / `process.exit(0)` adjacency).
- **Mechanism:** the drain is correctly *ordered* (`await Promise.race([allSettled, timeout])` completes before `process.exit(0)`), but it only awaits deductions **already created**. `/ws/streaming-deepgram` accumulates up to ~52 minutes of audio and calls `deductCredits` solely from `endSession()`; `/assistant` defers into `costPromise.then(...)` at `:350`. On SIGTERM mid-session `inFlightDeductions.size === 0`, so the drain short-circuits at `credits.ts:108` returning 0, and `process.exit(0)` kills the socket before `endSession()` runs — every active streaming session on that machine is transcribed free, while the comment at `index.ts:77-81` claims the drain exists to prevent exactly that.
- **Unproven link:** requires a Fly deploy/SIGTERM to land during an active session. Timing-dependent and not demonstrated. Confirming it needs a SIGTERM sent to a live instance with an open WebSocket.

### 10. `nextjs/server/api/routers/admin/customers.ts:33` — admin Stripe client pinned below the Managed Payments floor; refund path likely dead [PLAUSIBLE] — HIGH

- **Oracle:** [A4/A5] the only two `@ts-expect-error` markers and one of four non-test `as any` casts in the whole codebase — in a repo with zero TODO/FIXME markers, this ~20-line suppression record is the entire archaeology, which raises its prior sharply.
- **Mechanism:** two Stripe clients ~10 months apart. `lib/clients/stripe.ts:15` uses `2025-12-15.clover; managed_payments_preview=v1`; `customers.ts:33` uses `2025-02-24.acacia` **cast with `as any`** — the cast erased the only compile-time signal that `stripe@20.4.1` no longer models that version. Stripe's docs give `2025-03-31.basil` as the minimum for Managed Payments. Every session the admin refund can touch is a Managed Payments session (`credits/route.ts:195` sets it on all sessions, and that route is documented as the only way to obtain a key). `customers.ts:310` retrieves that session under the sub-floor pin; if `payment_intent` comes back null the `BAD_REQUEST` at `:312` throws, `refunds.create` at `:323` never runs, and because `updateAccountKey(..., "revoked")` sits at `:338` *after* the refund, the licence is not revoked either — customer keeps working credits and is never refunded. The mutation has no try/catch (unlike its siblings `list` and `updateEmail`), so Stripe errors propagate raw.
- **Unproven link:** whether Stripe actually nulls `payment_intent` or errors when retrieving a Managed Payments session under `2025-02-24.acacia`. Confirming it requires a real Stripe call, which the rules of engagement forbid. **What is fully proven:** the two clients disagree, the admin pin is below Stripe's documented floor, the `as any` is what hid it, and the refund/revoke ordering means a failure leaves the customer un-refunded *and* un-revoked.
- **Cleared in the same cluster:** the `@ts-expect-error` at `credits/route.ts:146` catches exactly `TS2769 'managed_payments' does not exist in type 'SessionCreateParams'` and nothing else (probed in a harness); `session` keeps its real type. Preview-not-enabled is **fail-closed** — the route reads only `session.url`, guarded at `205-211` inside a try/catch. No wrong price or credit grant. No shape divergence on any field actually read.
- **Adjacent, out-of-oracle (routed on, not claimed):** admin refund claws back `sourceType: "license_bundle"` (`customers.ts:332`) while credit mints grant `sourceType: "stripe_credit_pack"` (`stripe-webhook.ts:395`) — that clawback looks like a silent no-op for every minted licence.

### 11. `hyperwhisper-cloud/src/middleware/auth.ts:25` — non-string `license_key` throws a TypeError → opaque 500 [PLAUSIBLE] — MEDIUM

- **Oracle:** [D1] `isValidKeyFormat` (`nextjs/lib/services/license-key.ts:99`) is genuinely unreferenced — a key-format validator whose `typeof key !== "string"` guard nothing calls.
- **Mechanism:** `POST /post-process` with `{"license_key":123}` → `!licenseKey` false → `maskLicenseKey(123)` → `(123).slice(0,4)` → `TypeError` → Hono `onError` (`index.ts:67`) returns a 500 with an `error_id` instead of a clean 401. An **array** variant (`["a","b"]`, length ≤ 8) slips past the mask, is forwarded verbatim to the licence API, and detonates on the Next.js side at `license-validation.ts:126` `.trim()` → 500. That 500 is then classified transient by `auth.ts:70`, so it is **never negatively cached** — each retry costs a fresh 10s-budget round-trip and burns a slot of the shared rate-limit bucket that F7 depends on.
- **Unproven link:** the TypeError was reproduced in a local pure-function harness, not through a live HTTP request (no server was started). Confirming needs a running instance.
- **Cleared:** no injection or table-scan surface — `account_keys.key` carries `uniqueIndex("idx_account_keys_key")` and Drizzle parameterises. The damage is the type gap, not the lookup.

### 12. `hyperwhisper-cloud/src/providers/anthropic.ts:45` — missing-API-key error carries no `.status`, so provider fallback never fires [PLAUSIBLE] — MEDIUM

- **Oracle:** [A2/A3] the `as any` at `anthropic.ts:73`. That flagged line is itself fine; chasing it exposed the asymmetry one branch above.
- **Mechanism:** `xai-llm.ts:17`, `openai-llm.ts:35`, `gemini-llm.ts:19`, `mistral-llm.ts:19` all set `(error as {status?: number}).status = 503` on the missing-key branch. `anthropic.ts:45`, `cerebras.ts:16`, `groq-llm.ts:25` do not. `shouldFallback` → `getErrorStatus` (`llm-provider.ts:162`) reads `.status` (undefined) and its `/status\s+(\d{3})/i` message regex finds nothing → returns false. So with `CEREBRAS_API_KEY` (the **default** provider's key) unset or rotated out, every `POST /post-process` 500s even though `LLM_PROVIDER_FALLBACKS.cerebras = 'groq'` and Groq is healthy. The cloud service has no startup env validation, so the state is reachable.
- **Unproven link:** requires a missing/typo'd provider key in production — a config state, not an input. Not demonstrated against a deployed instance.

### 13. `hyperwhisper-cloud/src/middleware/credits.ts:46` — no reservation between the credit check and the charge [PLAUSIBLE] — MEDIUM

- **Oracle:** [A1] signals 1 and 3 — the fire-and-forget deduction leaves the check-to-charge window open.
- **Mechanism:** `validateCredits` is a pure in-memory comparison against a **cached** balance with no hold, lock or reservation; `src/lib/redis.ts` exports only `isIPBlocked`, `getCachedLicense`, `cacheLicense` — there is no concurrency primitive in the service. N parallel `/transcribe` calls on one licence all read the same cached balance and all pass admission. The cache is refreshed only from a deduction *response*, long after all N were admitted and the STT providers billed. `deductCreditBalance` is atomic and floored at 0 (`route.ts:117-119`), so the balance never goes negative — which means the excess charges are **forgiven, not owed**, and the operator absorbs the provider cost.
- **Unproven link:** the size of the window and whether real clients can issue enough concurrency to matter. Not measured. Confirming needs a load test against a live instance, which the rules forbid.

### 14. `nextjs/src/db/index.ts:4` — `PLANETSCALE_DATABASE_URL` is asserted non-null but absent from the env schema [PLAUSIBLE] — MEDIUM

- **Oracle:** [A2/A3] non-null assertion inventory.
- **Mechanism:** asserted in three places (`src/db/index.ts:4`, `drizzle.config.ts:7`, `src/db/migrate.ts:6`) but never declared in the `serverSchema` that `next.config.mjs:8` enforces at build time. A missing value therefore passes build and deploy, then fails as `Cannot read properties of undefined (reading 'query')` inside the first DB query of a live request — an error naming neither the database nor the variable.
- **Unproven link:** requires the variable to actually be unset/renamed on a deploy target. `STRIPE_SECRET_KEY`, `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` **are** all in `serverSchema`, so those three assertions are genuinely benign — this is the only unvalidated one.

### 15. `nextjs/src/lib/db-layer.ts:366` — unguarded destructure in the credit top-up path [PLAUSIBLE] — MEDIUM

- **Oracle:** [S] nextjs strict re-run — baseline 0 errors → 98 new; TS18048 here.
- **Mechanism:** `incrementCreditBalance` does `const [row] = await tx.insert(creditBalances)...returning(...); return Number(row.balance);` with **no guard and no try/catch** around the destructure. If the upsert ever returns zero rows this throws directly in the credit top-up/grant path (paid packs, minted keys, admin grants). The strict oracle rated this the cleanest type lie in nextjs — unlike the comparable `stripe-webhook.ts` refund-handler hits (508-555), which are papered over by an early `if (sessions.data.length === 0) return;`.
- **Unproven link:** whether a Postgres upsert with `returning()` can return zero rows here. Not demonstrated.

## Benign signals worth cleaning up anyway

- `hyperwhisper-cloud/src/lib/utils.ts:96` `throw lastError!` — unreachable today: the loop is `attempt = 0; attempt <= maxRetries` and the only caller chain passes literals 0-3 from an exhaustive switch. Latent hazard if a future caller passes a computed count.
- `azure-mai.ts:132` / `google-chirp.ts:168` `language!` — both guarded by an `isMonolingual` const on the preceding lines; identical guard shape to all five sibling STT providers. No fallback-path asymmetry.
- `customers.ts:218,239` `key!` — definitely assigned; TS just cannot prove a `for` body runs.
- `license-validation.ts:141` `polarImport.licenseId!` — both `success:true` returns populate it from a non-nullable PK; every other return short-circuits at line 132.
- `src/i18n/request.ts:9` `locale as any` — runtime comparison still happens and unknown locales fall through to `defaultLocale`; 40 locales, 40 message files, no gaps.
- `app/[locale]/layout.tsx:7` `(global as any).localStorage` — the stub has **no backing store** (all no-ops), so no cross-request leak is possible; no dependency feature-detects bare `localStorage`. It is also dead code *and* mis-ordered (ESM hoisting runs it after every import, confirmed in the compiled chunk), so it could never have protected the module-init access it was written for. Delete it.
- `app/[locale]/user/sign-in/page.tsx:54` `eslint-disable-line react-hooks/exhaustive-deps` — redundant: the rule is `"off"` globally in `eslint.config.mjs`. The effect itself is safe (no path makes `licenseKeyParam` go null→non-null while mounted), though `[licenseKeyParam]` is the honest dep array.
- `estimateCreditsForCost` (`cost-calculator.ts:505`), `ALL_STT_PROVIDER_IDS` (`stt-models.ts:216`), `createServerCaller` (`lib/trpc/server.ts:38`) — genuinely dead, no behavioural consequence. `roundUsd` is merely over-exported (20+ intra-file callers).
- `route.ts:136` returns `credits_deducted: amount` (requested) while the real `deductedAmount` is discarded — differ only on an overdraw, which `validateCredits` prevents; log-cosmetic.

## Refuted

- **NaN corruption of credit balances via unchecked rate lookups** (`cost-calculator.ts:303-340,437`, `stt-models.ts:243-284`) — the strict-mode leads that looked most dangerous. Every flagged line has an explicit guard: `GEMINI_RATES[model] ?? GEMINI_FALLBACK_RATE`, `rates[model] ?? rates[defaultModel]`, `def.models.find(...) ?? def.models[0]`, with the stated intent *"Unknown models fall back to the provider default rate so a catalog/header drift never bills $0 (fail-closed)"*. All model/provider ids are allowlist-validated before the arithmetic (`isValidProviderId`, `resolveModel` → 400 on unknown). Prototype-pollution keys (`__proto__`, `constructor`, …) were tested and all rejected. Even a forced NaN is double-blocked: `creditsForCost` floors it to 0.1, and the licence server independently rejects non-finite amounts with a 400.
- **better-auth off-origin callback delivery** — see F1 note; better-auth's allowlist regex rejects all payloads with a 403.
- **Dead credit-guard constants** `MAX_CREDIT_DEDUCTION_AMOUNT`, `CREDIT_BALANCE_SCALE`, `CREDIT_FEE_RATE` — all consumed by validators in their own files that the live routes do call (`credits/route.ts:92`, `checkout/credits/route.ts:51`). No inlined literal diverges anywhere.
- **`spendCreditGrantsByProvenance` dead / wrong spend ordering** — called at `db-layer.ts:627` by `deductCreditBalance`, which the credits route invokes. It is the only spend implementation and orders `expires_at ASC` (soonest-to-expire first), which is the value-preserving order. Name is a misnomer; behaviour is correct.
- **`getAllAccountKeysForAdmin`, `tryExtractCorrectionText`, `estimatePromptTextTokens`, `INLINE_AUDIO_MAX_BYTES`, `isSupportedLocale`, `minimumStreamingCredits`, `isValidKeyFormat`-as-dead** — same-file or wrapper callers; false positives of the zero-external-reference scan.
- **25 dependency advisories** — all BUILD-ONLY or TRANSITIVE-UNREACHED after reachability grepping (`tar` via `@tailwindcss/oxide`, `dompurify` via `posthog-js`).
- **`older-versions/page.tsx:120`** `versionMap.get(...)!` — guarded by `.has()` on the preceding line.

## Coverage — read this before trusting the findings

- **Oracles run:** cloud test suite; cloud typecheck; nextjs typecheck; nextjs strict re-run; cloud strict re-run; suppression archaeology (TODO/FIXME/HACK/XXX/`@ts-ignore`/`@ts-expect-error`/`eslint-disable`/`as any`/non-null/swallowed-catch); dead-code & zero-importer scan; guard-asymmetry scan across sibling routes; dependency audit (pnpm + bun); test-runner discovery.
- **Oracles unavailable:** ESLint — could not execute at all (finding F2, so its entire correctness-rule surface produced zero leads). `npm audit` in nextjs — no `package-lock.json` (ENOLOCK); used `pnpm audit` instead. `git blame`/`git log -S` — history squashed into one commit, so suppression *age*, a primary ranking dimension for this skill, was unrecoverable. knip/ts-prune — not run; a scripted zero-external-reference scan was used instead, and it produced a 20/25 false-positive rate.
- **Leads generated:** ~40 clusters. **Chased:** 10 clusters via 8 chaser subagents + 2 oracle subagents. **Left on the table:** the `stripe-webhook.ts:508-555` refund-handler strict hits (guarded today, flagged as fragile); `app/api/checkout/credits/route.ts:132` TS2532 on the paid-checkout path; `db-layer.ts:590,603` spend-loop TS18048; `webhooks/add-blog-post/route.ts:384,386`; `lib/services/model-list.ts:78`; the ~120 TS4111 index-signature hits (style, no runtime risk); the two remaining `sanitizeReturnTo` consumers at `middleware.ts:93` and `:120`.
- **Phase 3 was not run.** No independent adversarial verifier subagent re-checked any candidate, because the shared 20-subagent pool was saturated for the entire hunt. F1–F5 rest on repros I executed myself; F6–F8 rest on chaser analysis with complete trigger paths and quoted code but no second opinion; F9–F15 name their unproven link.
- **This hunt saw ONLY what the oracles pointed at.** On this codebase that caveat bites unusually hard: with zero failing tests, zero skipped tests, zero TODO markers and a clean typecheck, the lead surface was thin, and the two files carrying the most severe findings (`middleware/auth.ts`, `middleware/credits.ts`) have **no tests at all** — they surfaced only because an unrelated grep pointed at them. Silence here is not evidence of absence: code with no tests, no type errors and no suppressions is invisible to this strategy.
