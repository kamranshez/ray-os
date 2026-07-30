I've completed the sweep. All findings below.

### Candidate
File: `nextjs/middleware.ts`
Line: 133
Invariant: I8
Claim: The sign-in route's "already authenticated?" gate is `hasSessionCookie(request)` — cookie *presence* only — and redirects to the dashboard, while `app/[locale]/user/(authenticated)/layout.tsx:33-38` validates the session for real and redirects back to sign-in; the two disagree whenever a cookie exists without a valid session.
Failure scenario: Any user whose browser holds a `better-auth.session_token` cookie that no longer resolves to a live session (operator rotates `BETTER_AUTH_SECRET`; the `session` row is purged/restored; the user record is deleted; or the sign-out route below leaves the cookie behind) is permanently locked out: GET `/en/user/sign-in` → middleware sees the cookie → 307 to `/en/user/dashboard` → middleware passes on cookie presence (line 118) → layout `getSession()` returns null → `redirect("/en/user/sign-in")` → middleware again. The browser aborts with `ERR_TOO_MANY_REDIRECTS`. The user cannot reach the sign-in form at all and can only recover by manually clearing cookies. A secret rotation does this to every signed-in customer simultaneously.
Confidence: medium

### Candidate
File: `nextjs/middleware.ts`
Line: 88
Invariant: I8
Claim: The `/user/customers` admin gate resolves the user through an HTTP self-`fetch` to `/api/auth/get-session` that returns `null` on *any* non-2xx or thrown error (lines 58-64), then redirects to sign-in with `returnTo=<pathname>` — but the sign-in branch (line 133) re-admits on cookie presence and follows `returnTo` straight back.
Failure scenario: A signed-in admin opens `/en/user/customers` while the self-fetch fails for a transient reason (edge→function cold start, deploy window, or Vercel Deployment Protection on a preview returning 401 for `/api/auth/get-session`). Middleware treats them as anonymous → 307 to `/en/user/sign-in?returnTo=/en/user/customers` → cookie present → 307 back to `/en/user/customers` → fail again. The admin sees `ERR_TOO_MANY_REDIRECTS` instead of the customer list, with no error message and no way to bypass it. Note this only bites because the failure-path and the success-path use two different notions of "authenticated".
Confidence: medium

### Candidate
File: `nextjs/app/[locale]/user/auth/sign-out/route.ts`
Line: 21
Invariant: I8
Claim: The POST handler builds `redirect` and sets the session-clearing `set-cookie` on it, but never returns it — the function falls off the end returning `undefined` after `auth.api.signOut()` has already revoked the session server-side.
Failure scenario: Anything hitting this endpoint (native-app sign-out deep link, a bookmarked/linked sign-out URL — nothing in the web UI uses it; `UserHeader.tsx:21` calls `authClient.signOut()` instead) gets a 500 from Next.js ("No response is returned from route handler"). The session is dead in the DB but the `better-auth.session_token` cookie is never cleared in the browser, which is exactly the cookie-present/session-invalid state that makes the middleware sign-in gate above loop forever. The user is signed out, sees an error page, and can then never load the sign-in page again.
Confidence: medium

### Candidate
File: `nextjs/middleware.ts`
Line: 51
Invariant: I8
Claim: The only real session lookup in middleware targets `request.nextUrl.origin` — an origin derived from the inbound request's Host header — so the identity used for the `role === "admin"` decision comes from a URL the client influences rather than from a locally verified session.
Failure scenario: If a request reaches the deployment with an attacker-chosen Host (host-header routing quirk, a misconfigured proxy/alias in front of Vercel, or a self-hosted deployment behind an untrusted reverse proxy), middleware fetches `https://<attacker-host>/api/auth/get-session`, receives `{user:{role:"admin"}}`, and admits the request to `/{locale}/user/customers`. The blast radius is bounded to the route gate only — `customers/page.tsx:29-39` re-derives the session locally via `auth.api.getSession` and redirects, so no customer records are actually rendered. Practically unexploitable on Vercel (unknown Hosts are rejected at the edge), reported because the gate itself derives identity from client-influenced input.
Confidence: low

### Coverage

Examined buckets:
- **B7 next-edge-auth-and-misc-api** — full read of `middleware.ts`, `src/lib/auth.ts`, `src/lib/auth-license-key-plugin.ts`, `src/lib/auth-client.ts`, `src/lib/license-key-redirect.ts`, `app/api/auth/[...all]/route.ts`, `app/api/customer/profile/route.ts`, all three `app/api/internal/*` routes + `internal/models`.
- **B8 next-trpc-server** — `trpc.ts`, `root.ts`, `routers/customer.ts`, `routers/download.ts`, all three `routers/admin/*`, `lib/trpc/server.ts`, `app/api/trpc/[trpc]/route.ts`.
- **B11 next-account-ui** — every page under `app/[locale]/user/**` (incl. the `(authenticated)` layout, sign-in, sign-out), plus `customer/**`, `credits`, `checkout`, `purchase-success`, `manage-billing`, and the `components/user|customer|credits` data-fetch call sites.
- **B6 next-money-api** — `license/validate`, `license/credits` (GET+POST), `checkout/credits`, reviewed specifically for identity derivation.
- **B9 next-db-and-services** — the identity-relevant slice: `src/db/schema/auth.ts`, and `db-layer.ts`'s `findAccountByKey` / `getAccountKeysByEmail` / `getCreditBalancesForUsers` / `getPaidCreditGrantsForUsers`; plus `lib/services/license-key.ts` for key entropy.
- **B1/B2 cloud-entry-and-auth, cloud-routes** — `src/index.ts`, `src/middleware/auth.ts`, `src/routes/usage.ts`, and the `validateAuth`/`deductCredits` call sites in `transcribe.ts`, `post-process.ts`, `assistant.ts`, `ws-streaming-deepgram.ts`.

Not examined / partially examined:
- **B3, B4, B5** (cloud STT/LLM providers, billing/Google) — no user-identity surface; the cloud service holds no user data and every route resolves identity through `validateAuth` before reaching them.
- **B10 next-public-site**, **B12 next-tests** — marketing/i18n shell and validation unit tests; spot-checked `app/[locale]/layout.tsx` (only reads `x-pathname` for metadata) and confirmed no other `[locale]` page reads `searchParams` to fetch account data.
- **B9 remainder** (email templates, Stripe webhook, clients, migrations) — mutation-authorization there is webhook-signature/secret-gated, owned by I5/I9.

Leads refuted:
- **"A page under `/user/*` renders account data on the presence-only cookie check."** Refuted. `app/[locale]/user/(authenticated)/layout.tsx:33`, `dashboard/page.tsx:28`, `devices/page.tsx:26`, and `customers/page.tsx:29` each call `auth.api.getSession` server-side; `devices` and `customers` additionally re-check `session.user.role !== "admin"` and redirect. `app/[locale]/user/page.tsx` is a bare redirect. So the middleware's cookie-presence gate is never the only data gate — the exposure risk is refuted; what survives is the *divergence* between the two gates (candidates 1-3).
- **"An `admin/*` procedure uses the wrong procedure type."** Refuted. All eight procedures across `admin/{stats,customers,devices}.ts` use `adminProcedure`, which runs the `isAdmin` middleware over `ctx.isAdmin = user.role === "admin"` derived in `createTRPCContext` from `auth.api.getSession` (`trpc.ts:48-50`). No admin data path accepts an identity from input; `input.userId`/`input.licenseKeyId` there are *targets* chosen by a verified admin, which is the intended semantics.
- **"A `customer.*` procedure keys off an input-supplied id."** Refuted. All six `customer.*` procedures take no input at all and derive everything from `ctx.user.email` (`customer.ts:31,89,135,177,190`). `/api/customer/profile` likewise derives from `session.user.email`. Client components (`UserDashboardClient`, `BillingCard`, `CreditHistoryCard`, `DevicesClient`, `CustomersClient`) all fetch through `protectedProcedure`/`adminProcedure`, so the data gate holds regardless of the page-level check.
- **"`role` can be set at sign-up."** Refuted. `src/lib/auth.ts:12-21` declares `role` with `input: false` and `defaultValue: "user"`; the DB column (`src/db/schema/auth.ts:13`) defaults to `"user"` and is only writable through admin paths.
- **"The custom license-key sign-in plugin can mint a session for an arbitrary email."** Refuted. `auth-license-key-plugin.ts:28-65` looks the key up in the DB, requires `status === "granted"`, requires a non-null `license.userId`, loads that exact user row, and creates the session for `foundUser.id` — the email is never taken from the request. Keys carry ~79 bits of `crypto.randomInt` entropy (`lib/services/license-key.ts:29-90`), so key-as-bearer-credential is a real credential, not a guessable id; that also clears `/api/license/{validate,credits}` and `/api/checkout/credits` of I8 (they authenticate with the key itself, not with a user id). The endpoint is rate-limited 5/min.
- **"The cloud service exposes a user's data via a client-supplied identifier."** Refuted. `usage.ts:103` folds `identifier` into the same `licenseKey` variable and runs it through the normal validate-or-401 path; every other route calls `validateAuth` before any work.
