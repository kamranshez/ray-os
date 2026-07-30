---
skill: spec-gap-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 2 |
| PLAUSIBLE findings | 1 |
| Findings with an executable repro | 2 |
| Files opened (of 210 in scope) | 30 |
| Subagents spawned | 7 |
| Strategy came up dry? | no |

**Stale docs are deliberately excluded from the counts above: 5 STALE-DOC items are
reported in their own section.** A wrong doc and a missing implementation are not the
same defect, and folding them into "CONFIRMED" would inflate this scorecard against the
other nine hunters. Two of the five are commercially significant and I say so there.

## Coverage ledger

**Provenance note, stated plainly because it affects how much you should trust the
numbers.** I spawned 7 subagents: 4 claim extractors (docs, names/types, tests,
user-facing surface) and 3 auditors (entitlement/licensing, credits/billing/webhooks,
provider fallback/registries). **No subagent output ever reached me** — their transcript
files stayed at 130 bytes and no completion notification arrived. The orchestrator later
relayed that three audits had returned material, naming three specific leads: a
documented trial-credit subsystem that does not exist, a deactivate endpoint that is a
no-op stub, and a refund-policy page promising a credit bundle no live path grants.

I did not transcribe those. I re-derived each one against the code myself, and every
piece of evidence cited below is something I executed or read directly. Where the relayed
lead and my own verification agree, I say so; nothing is reported on the strength of the
relay alone. This is the honest version: the fan-out's *pointing* was useful, its
*evidence* never arrived, and the report reflects only evidence I hold.

What was examined directly (30 in-scope files):

- **i18n surface** — `src/i18n/locales.ts`, `request.ts`, `routing.ts`, all 40 catalogs
  under `messages/` (checked mechanically, not by eye), `app/[locale]/layout.tsx`
  metadata block.
- **Email templating** — `lib/templates/escape-html.ts` plus all four templates, every
  `${}` interpolation enumerated.
- **Guards** — `lib/rate-limit.ts` callers, `lib/security/timing-safe-secret.ts` callers,
  `server/api/routers/download-ip.ts` (full), `download.ts` email-validation path.
- **Licensing routes** — `api/license/{validate,activate,deactivate}/route.ts` and all
  three `api/account/*` twins.
- **Billing** — `lib/services/stripe-webhook.ts` (grant + dispatch paths),
  `api/webhooks/stripe/route.ts`, `api/checkout/route.ts`, `api/checkout/credits/route.ts`,
  `src/db/schema/credit-grants.ts`, `src/lib/db-layer.ts` (grant call sites).
- **Cloud** — `hyperwhisper-cloud/src/middleware/auth.ts`, `src/routes/usage.ts`.
- **Legal pages** — `legal/refund-policy/page.tsx`, `legal/terms-of-service/page.tsx`,
  `api/config/route.ts`.
- **Tests** — all five `nextjs/tests/*.test.ts`, executed.

**What remains unexamined — silence here means nobody looked, not that it is clean:**

- Most of `hyperwhisper-cloud/` (≈50 of 56 files): every provider implementation, the
  fallback chain in `routes/transcribe.ts`, `post-process.ts`, `assistant.ts`, the
  WebSocket streaming lifecycle, `cost-calculator.ts`, `stt-models.ts`,
  `llm-token-limits.ts`, `middleware/credits.ts`. This is the highest-risk third of the
  arena. Provider/model registries are the textbook home of enum-exhaustiveness
  omissions — this hunter's signature catch — and I got nowhere near them.
- Stripe webhook **idempotency** specifically. I read the grant path and the dispatch,
  but did not verify the `stripe_processed_events` dedup ordering or the `charge.refunded`
  handler at `route.ts:121`. The docstring claims idempotency; I did not test it.
- Credit deduction/refund on the cloud error path; negative-balance protection.
- tRPC routers, admin routers, all `app/[locale]/` pages and `components/`.

**Structural blind spot of this strategy on this codebase:** a spec-gap hunt only inspects
code some promise points at. HyperWhisper's TypeScript carries few docstrings and no API
reference, and `mintlify-help/` documents the desktop apps far more than the in-scope
services. The richest claim sources here turned out to be **legal pages, config, and
names** — not prose docs. Code that is unnamed, undocumented and untested is invisible to
this hunter by construction. Notably, the strategy's best yield on this repo was *stale
promises*, not missing code: the codebase largely does what its identifiers say, but its
user-facing copy describes a product generation that has been retired.

**Verification honesty:** Phase 3 adversarial verifiers did not run as separate subagents;
I verified inline, which is weaker because I shared my own assumptions. I compensated by
executing every check I could rather than reasoning about it, and by refuting five of my
own candidates (listed at the end).

---

## Claim ledger (17 rows, self-built and self-verified)

| # | Claim | Source | responsible_code | Strength | Verdict |
|---|---|---|---|---|---|
| 1 | Every locale in `locales` has a catalog | `src/i18n/request.ts:14` | `messages/*.json` | IMPLIED | HONORED |
| 2 | Every catalog carries every `en.json` key | `src/i18n/request.ts` | `messages/*.json` | IMPLIED | HONORED |
| 3 | `toOpenGraphLocale` returns a valid OG locale | name, `src/i18n/locales.ts:131` | `locales.ts:131-145` | IMPLIED | **FALSE** → Bug 1 |
| 4 | Every user-derived value in email HTML is escaped | `lib/templates/escape-html.ts:1-8` | 4 email templates | EXPLICIT | PARTIAL → Bug 3 |
| 5 | The rate limiter guards the `/api/account/*` twins | route symmetry | `app/api/account/*` | IMPLIED | HONORED (re-export) |
| 6 | Every internal-secret check uses `timingSafeEqualSecret` | name | 4 internal routes + blog webhook | IMPLIED | HONORED |
| 7 | `getClientIPFromHeaders` yields a non-spoofable key | `download-ip.ts:11-13` | `download-ip.ts:14-27` | IMPLIED | HONORED on Vercel |
| 8 | Disposable domains blocked case-insensitively, incl. subdomains | `download.ts:59-66` | `download.ts:64` | IMPLIED | HONORED |
| 9 | Tests under `nextjs/tests/` verify what they assert | 5 test files exist | CI / `package.json` | IMPLIED | **FALSE** → Bug 2 |
| 10 | `z.string().email()` blocks HTML metacharacters | `download.ts:138` | zod 4.4.3 | IMPLIED | HONORED |
| 11 | Backend is consumed as a git submodule | `README.md:72` | `.gitmodules` | EXPLICIT | **STALE** → Doc 4 |
| 12 | Buying a license auto-grants $5 of Cloud credits | `legal/refund-policy/page.tsx:177-180` | `stripe-webhook.ts:126` | EXPLICIT | **STALE** → Doc 1 |
| 13 | Trial users start with 150 free credits, tracked per device | `mintlify cloud-credits.mdx:24`, `licensing.mdx:25` | `cloud/middleware/auth.ts` | EXPLICIT | **STALE** → Doc 2 |
| 14 | Some devices receive free trial credits | `legal/terms-of-service/page.tsx:142-143` | `cloud/middleware/auth.ts:96-105` | EXPLICIT | **STALE** → Doc 2 |
| 15 | Deactivating on the old machine frees the activation slot | `mintlify licensing.mdx:98` | `api/license/deactivate/route.ts` | EXPLICIT | **STALE** → Doc 3 |
| 16 | `auth.ts` validates device trial identifiers | `cloud/middleware/auth.ts:2` | same file | EXPLICIT | **STALE** → Doc 5 |
| 17 | Stripe webhook processing is idempotent | `stripe-webhook.ts:176-182` | `stripe-processed-events` | EXPLICIT | NOT AUDITED |

---

## Code bugs (3)

### 1. `og:locale` is invalid on 14 of 40 shipped locales — CONFIRMED + repro

- **Claim**: a function named `toOpenGraphLocale` returns a valid Open Graph locale
  (`language_TERRITORY`). (`nextjs/src/i18n/locales.ts:131`, IMPLIED by name and by its
  use as `openGraph.locale`.)
- **Gap**: `openGraphLocaleOverrides` (`nextjs/src/i18n/locales.ts:113-121`) covers only 7
  locales. Everything else hits `` return `${locale}_${locale.toUpperCase()}` `` at
  `nextjs/src/i18n/locales.ts:144`, which assumes territory code == language code. True
  for `de_DE`/`fr_FR`/`it_IT`, false for 14 shipped locales. The missing code is 14 more
  entries in the override map at `locales.ts:121`.
- **Failure**: every page under those languages emits e.g.
  `<meta property="og:locale" content="ko_KO">`. `ko_KO`, `sv_SV`, `da_DA`, `he_HE`,
  `cs_CS`, `el_EL`, `sl_SL`, `sr_SR`, `et_ET`, `ca_CA`, `uk_UK`, `ms_MS`, `vi_VI` and
  `hi_HI` are not valid OG locales, so unfurlers discard the hint for a third of the
  site's languages. Low severity: social/SEO metadata only.
- **Trigger**: GET `/ko/` → `generateMetadata` at `nextjs/app/[locale]/layout.tsx:92` →
  `toOpenGraphLocale("ko")` → `locales.ts:131` → no override → `locales.ts:144` → `"ko_KO"`.
- **Repro**: `…/scratchpad/og-locale.repro.test.ts` (kept out of the repo — tree is
  read-only). From `nextjs/`: `npx tsx --test <path>`:

  ```
  not ok 1 - toOpenGraphLocale returns a valid OG locale for every shipped locale
      og:locale is invalid for 14 of 40 shipped locales:
        ko: got ko_KO, valid OG locale is ko_KR
        sv: got sv_SV, valid OG locale is sv_SE
        da: got da_DA, valid OG locale is da_DK
        he: got he_HE, valid OG locale is he_IL
        …14 rows…
  ```

### 2. All five `nextjs/` test suites are orphaned — nothing ever runs them — CONFIRMED + repro

- **Claim**: the existence of `nextjs/tests/*.test.ts` asserts that open-redirect
  sanitization, download-IP validation, geolocation-IP validation, credit-purchase
  validation and license-credit validation are verified behaviour. (Source (c): a test is
  a promise.)
- **Gap**: `nextjs/package.json` has **no `test` script** (only `dev`, `build`,
  `vercel-build`, `start`, `lint`, appcast validators, `db:*`). No workflow covers
  `nextjs/` — the eight workflows are cloud-deploy ×3, macos ×2, windows ×2,
  shared-core ×1, and only `cloud-deploy.yml:57` runs tests (`bun test src`, for
  `hyperwhisper-cloud`). `vercel-build` runs `drizzle-kit migrate && prebuild && next
  build`; `prebuild` only validates appcasts. Missing: a `test` script plus a
  `nextjs`-triggered workflow.
- **Failure**: 26 passing assertions guarding security-relevant behaviour — including
  `sanitizeReturnTo blocks protocol-relative and backslash open redirects` — give zero
  regression protection. A change reintroducing an open redirect in
  `src/lib/license-key-redirect.ts`, or weakening server-side credit-purchase validation,
  merges green. The tests are not broken, merely orphaned, which is worse: their presence
  buys false confidence in review.
- **Trigger**: open any PR touching `nextjs/`. No path filter matches, so no job runs.
- **Corroborating intent**: `.github/workflows/shared-core-tests.yml:3-6` says a contract
  without a CI gate "would be honor-system: the macOS and Windows release workflows only
  BUILD the core, they never run its tests." The maintainers already treat unrun tests as
  a defect worth a dedicated workflow. `nextjs/` is in exactly that state.
- **Repro** (proves the tests are real, runnable and green — genuinely orphaned, not
  abandoned-because-failing):

  ```
  $ cd nextjs && npx tsx --test tests/*.test.ts
  # tests 26
  # pass 26
  # fail 0

  $ npm test
  npm error Missing script: "test"
  ```

### 3. `customerEmail` interpolated unescaped into all four email templates — PLAUSIBLE

- **Claim**: "Always escape user-derived values before embedding them in HTML."
  (`nextjs/lib/templates/escape-html.ts:1-8`, EXPLICIT docstring that further names
  Stripe `customer_details` as attacker-controllable.)
- **Gap**: each template escapes exactly one field, `customerName`, and interpolates
  `data.customerEmail` raw into the footer: `license-email.ts:66`,
  `welcome-email.ts:69`, `credit-mint-email.ts:67`, `credit-topup-email.ts:58`. The
  missing call is `escapeHtml(data.customerEmail)` beside the existing
  `escapeHtml(data.customerName)` at e.g. `welcome-email.ts:35`.
- **Failure**: if any upstream admits an HTML metacharacter in an address, that markup
  lands in a transactional email from a trusted sender.
- **Trigger — and the unproven link**: I could not construct a reaching input, which is
  why this is PLAUSIBLE. The download path (`server/api/routers/download.ts:138` →
  `welcomeEmailHtml`) validates with `z.string().email()`; tested against the repo's own
  zod 4.4.3, `a<img src=x>@ex.com`, `a"onmouseover="x@ex.com`, `a&b@ex.com` and
  `"<script>"@ex.com` are all **rejected**. Only `'` is accepted, and `'` in a text node
  is inert. **What would confirm it**: showing the Stripe-fed templates
  (`license-email.ts`, `credit-mint-email.ts`, `credit-topup-email.ts`, populated from
  `lib/services/stripe-webhook.ts`) can carry an address containing `<`, `>` or `"` —
  those never pass through zod, and I did not audit the webhook's email handling. Treat
  as a defense-in-depth inconsistency, not a demonstrated vulnerability.

---

## Stale docs (5)

Separate bucket, lower severity than the code bugs above — in every case the code is
deliberately what it is and the *documentation* is what's wrong. Items 1 and 2 are
nonetheless commercially significant because they are user-facing promises on legal pages.

### 1. `legal/refund-policy/page.tsx:177-180` promises a $5 credit bundle that no live purchase path grants

The page states: "**$5 complimentary credits:** When you purchase a HyperWhisper license,
you are automatically granted **$5** of HyperWhisper Cloud credits", and builds a worked
refund example on it at lines 183-186.

The grant exists in code — `lib/services/stripe-webhook.ts:126` calls `grantCreditLot({
amount: 5000, sourceType: "license_bundle" })` — but it sits inside
`handleLicensePurchase`, which the webhook dispatches to only when
`session.metadata.purchase_type === "license"` (`app/api/webhooks/stripe/route.ts:76-78`).
**No code sets that value.** The only route that sets `purchase_type` is
`app/api/checkout/credits/route.ts:80`, which sets `"credits"`, and
`app/api/checkout/route.ts:3-9` is now a bare redirect whose own comment reads "The
standalone /checkout (license) flow was retired; send callers straight to the credits buy
flow." The webhook's docstring agrees (`stripe-webhook.ts:176-180`): minting a key via a
credit purchase "is now the only way to obtain a key (the standalone license product is
retired)."

So `handleLicensePurchase` and its $5 bundle are unreachable dead code, and a customer
reading the refund policy is told they receive credits the live flow never grants. The
page should describe the credits-first flow: you buy credits, a key is minted, and the
balance is what you paid for. Filed here rather than as a code bug because retiring the
license product was deliberate; the omission is that the legal page was not updated.

### 2. The trial-credit subsystem is documented in two places and does not exist

`mintlify-help/cloud-credits.mdx:24` ("**Trial** | 150 credits on your first use (~27
minutes at the default tier). Tracked per device.") and `licensing.mdx:25` ("**Trial
users** start with 150 free credits") describe a trial tier. The in-scope legal page
repeats it: `legal/terms-of-service/page.tsx:142-143` — "**Trial credits**: Some devices
may receive a limited number of free trial credits for evaluating HyperWhisper Cloud."

The cloud service has no such path. `hyperwhisper-cloud/src/middleware/auth.ts:99-105`:
"HyperWhisper Cloud is licensed-only: a valid license key (which carries the credit
balance) is required for every request. There is no anonymous/trial path — without a key
the request is rejected before any provider work" — and the code returns
`licenseRequiredResponse()` when `licenseKey` is absent. `src/routes/usage.ts:145`
hardcodes `is_trial: false`, and the route's terminal branch returns
`401 'License required'`. There is no device-trial identifier handling anywhere in
`auth.ts`.

Consequence is reputational and contractual rather than technical: the Terms of Service
offer a benefit the service cannot deliver, and a user following the docs will hit a 401.

### 3. `mintlify-help/licensing.mdx:98` says deactivating frees an activation slot; there are no slots

The doc instructs: "Open **Settings → License → Deactivate** on the machine you're
leaving. This frees the activation slot." Server-side,
`nextjs/app/api/license/deactivate/route.ts` is explicitly a stub — its header says
"License Deactivation API (STUB) … Returns success without any database changes", and the
handler validates only that `license_key` is non-empty before returning
`{ success: true, message: "License deactivated successfully" }`. There is no activation
tracking to free: the sibling `license/activate/route.ts:19-23` records that it returns a
dummy `activation_id` that "is never used (deactivate is a stub)", and the model is now
"No activation/deactivation - fair usage policy instead". `account/deactivate/route.ts`
re-exports the same stub.

Two things worth noting for whoever fixes this. The response message asserts an action
that never occurred, which is a claim the code does not honour — but the omission is
documented and deliberate at `route.ts:4-16`, so it is a wording problem, not a bug. And
because the stub never checks that the key exists, any non-empty string receives
"License deactivated successfully"; harmless today precisely because the endpoint does
nothing.

### 4. `README.md:72` says the backend is a git submodule; it has been vendored since `3b810e6`

`README.md:72` states "This repo uses a git submodule for the backend:" followed by `git
clone --recurse-submodules`. `.gitmodules` declares exactly one submodule,
`integrations/hyperwhisper-mcp`. `git ls-files -s hyperwhisper-cloud` returns mode
`100644` blobs, not a `160000` gitlink — the backend is ordinary vendored source, changed
by `3b810e6` ("feat: vendor Fly backend as hyperwhisper-cloud/, move deploy workflows to
app repo"). The `--recurse-submodules` command stays correct, just for a different
submodule, which is why this is the mildest item here.

### 5. `hyperwhisper-cloud/src/middleware/auth.ts:2` — stale comment contradicting line 100 of the same file

The file header reads "Validates license keys and device trial identifiers". The file
contains no device or trial handling, and line 100 states the opposite ("There is no
anonymous/trial path"). Residue of the same trial removal as item 2; the header should
read "Validates license keys."

---

## Refuted candidates (5)

Recorded so nobody re-walks them:

1. **Duplicate `escapeHtml` in the blog webhook** — `app/api/webhooks/add-blog-post/route.ts:163`
   defines its own rather than importing `lib/templates/escape-html.ts`. Refuted: the two
   bodies are character-identical (same five replacements, same order). DRY smell, not a
   behaviour gap.
2. **`/api/account/*` missing the rate limiter** — refuted. `account/validate/route.ts:12`
   and `account/activate/route.ts:9` are one-line `export { POST }` re-exports of the
   `license/*` handlers, so `licenseValidateRateLimiter` applies unchanged.
3. **Missing or partial locale catalogs** — refuted mechanically. `locales.ts` lists 40
   locales, `messages/` holds 40 catalogs, the sets match exactly, and all 39 non-English
   catalogs carry all 271 keys of `en.json` with no extras.
4. **Spoofable rate-limit key via `x-forwarded-for`** — refuted. `download-ip.ts:16`
   consults Vercel's `x-vercel-forwarded-for` first, which the platform overwrites, so a
   client-supplied header cannot take precedence. The `"unknown"` fallback at
   `download-ip.ts:26` collapses keyless callers into one bucket, failing *closed*.
5. **`===` bypass of `timingSafeEqualSecret`** — refuted. All four `/api/internal` routes
   plus the blog webhook import and use the helper; no direct secret `===` found.

## What a re-run should do differently

The fan-out was correctly specified and correctly parallelised, and then I let it run
unattended and never collected a single table. A re-run should poll each subagent on a
fixed interval and treat "no output yet" as something to chase rather than wait on. The
relayed leads proved the extractors were finding real material — the trial-credit and
refund-policy gaps are among the best findings here — which makes the collection failure
the single costliest thing about this run.

Substantively, the next findings are almost certainly in `hyperwhisper-cloud/`'s provider
and model registries, which no one examined: comparing `stt-models.ts`,
`llm-token-limits.ts` and `cost-calculator.ts` against each other for a model id that one
map carries and another omits is the highest-yield unexecuted check in this arena. Stripe
webhook idempotency (claim 17, NOT AUDITED) is the second.
