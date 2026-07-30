---
skill: hostile-input-hunter
date: 2026-07-29
model: opus-5
---

## Scorecard

| Metric | Value |
|---|---|
| CONFIRMED findings | 20 |
| PLAUSIBLE findings | 4 |
| Findings with an executable repro | 20 |
| Files opened (of 210 in scope) | 108 |
| Subagents spawned | 7 |
| Strategy came up dry? | no |

## Coverage ledger

**108 of 210** in-scope files were opened. That is the deduplicated union of the file ledgers
returned by six cluster hunters plus my own reads, intersected against `scope-files.txt` —
three `nextjs/src/env/*.mjs` files the hunters read are excluded because they are not on the
pinned list. Seven subagents were spawned directly (one surface mapper, six cluster hunters);
several hunters spawned their own nested readers, which I have not counted.

**What was covered.** All 21 Next.js API route files, all 5 Hono routes, both middleware
layers, all 14 tRPC procedures across four routers including the `admin/` tree, the full
Drizzle schema, and 14 of 24 provider adapters. Every finding below is backed by a probe that
was actually run; the scratchpad holds 15 probe files across six prefixes (`idor-`, `credit-`,
`hook-`, `stt-`, `edge-`, `ws-`).

**The 102 files not opened**, by area: `nextjs/app` 39 (marketing/locale pages), `components`
21, `nextjs/lib` 16, `cloud/providers` 10, `nextjs/src` 6, `tests` 3, `contexts` 2, plus five
singletons. The 21 component files and most of the 39 app pages are **deliberately** skipped:
this strategy attacks from outside the process, and an attacker bypasses client components
entirely to post at the API. Fuzzing a React component tests nothing an API probe does not
test better. The 10 unread provider adapters were grepped for user-input handling — enough to
answer "does user input reach a URL path" — but not read line by line.

**What this strategy is structurally blind to here.** Three real gaps. (1) **No live
Postgres** — no hunter could stand one up, so every ownership predicate was read out of source
rather than proven by a cross-user query, and the transactional claims in findings 2 and 3 are
executed against faithful in-memory stand-ins rather than a real database. (2) **Races** — the
catalog has no concurrency row, and three findings (5, plus PLAUSIBLE P3 and P4) sit at the
boundary where a hostile *value* stops being the right lens and a hostile *interleaving* takes
over. (3) **Logic bugs with no input component** — a wrong constant or an inverted boolean is
invisible to a catalog of hostile values; findings 8 and 14 were caught only incidentally while
tracing other inputs, and I flag them as off-thesis below.

**Correction to my own read.** Mid-hunt I seeded the hunters with a lead that the rate limiter
buckets on a client-controlled `X-Forwarded-For`, and I had it queued as PLAUSIBLE. Two hunters
independently **refuted** it by execution: `x-vercel-forwarded-for` is ranked first and Vercel
sets it. I was wrong; it appears in Refuted, not in the findings.

---

# Hostile input hunt — HyperWhisper (nextjs + hyperwhisper-cloud)

**Mode:** deep
**Surfaces enumerated:** 21 Next.js routes + 5 Hono routes + 2 middleware + 14 tRPC procedures — **fuzzed:** all, in 6 parallel clusters
**Candidates:** 31 → **confirmed:** 20, **plausible:** 4, **refuted:** 7 headline (plus ~20 sub-checks)
**Repros produced:** 20

## Summary

The worst thing found is an **open redirect in `nextjs/middleware.ts`**: the `returnTo`
sanitiser inspects only the first two characters, so a tab/CR/LF in position two survives it and
the URL parser then strips that character into a protocol-relative offsite redirect. Close
behind are **two independent ways to lose refund money** in the Stripe webhook — a refund
arriving before its checkout completes is discarded permanently (customer refunded *and* keeps
the credits), and the partial refund the public policy page explicitly promises reclaims
**zero** credits.

The pattern is consistent and worth stating plainly: **this codebase validates scalars superbly
and validates relationships between values poorly.** Every hostile number, type confusion,
prototype-pollution payload and injection string thrown at the validators died at the edge.
`validateCreditDeductionAmount` rejected all 25 catalog number rows; `timingSafeEqualSecret`
fails closed; the Stripe event dedupe has no replay window; and there is **no IDOR anywhere in
the codebase** because every route derives its principal server-side. The twenty findings are
almost entirely cases where each individual value is perfectly legal and the *relationship*
between two of them is wrong: a `returnTo` that is a legal path yet resolves offsite; an audio
payload whose byte count is honest but whose duration is 6× the assumed bitrate; a refund whose
amount is correct but whose ordering is not; a text frame that is well-formed but counts against
no budget. Casualties everywhere. Every survivor was relational.

A second, quieter pattern: **the metering is one-sided.** Six separate findings (4, 5, 6, 7, 8,
9) end the same way — real upstream spend, zero or undercharged credits, no alert.

## Findings

Ranked by what hurts, per the skill: injection and authz first, then silent corruption, then
resource, then error-quality. Within a tier, repro-backed first.

### 1. Open redirect via tab/CR/LF in `returnTo` — CONFIRMED · injection · HIGH

**Surface:** `nextjs/middleware.ts:132-138`; the same helper is also reached from
`nextjs/app/[locale]/user/sign-in/page.tsx:44` and `nextjs/src/lib/auth-license-key-plugin.ts:84`

**Input:**
```
https://www.hyperwhisper.com/en/user/sign-in?returnTo=/%09/evil.com
```
(`%09`=TAB; `%0a`/`%0d` work identically. Requires only that the victim holds any non-empty
`better-auth.session_token` cookie — the ordinary phishing case.)

**Path:** `middleware.ts:135` reads `returnTo` → `sanitizeReturnTo`
(`nextjs/src/lib/license-key-redirect.ts:13-18`) applies:
```ts
returnTo.startsWith("/") && !returnTo.startsWith("//") && !returnTo.startsWith("/\\")
```
`"/\t/evil.com"` satisfies all three — the second character is a tab, so it is neither `//` nor
`/\` — and is returned verbatim → `middleware.ts:137` `new URL(redirectUrl, request.url)`, and
the WHATWG URL parser **strips tab/CR/LF per spec**, yielding `//evil.com` →
`NextResponse.redirect` emits `Location: https://evil.com/`.

**Detonation:** A link on the genuine domain silently bounces an authenticated user to an
attacker-controlled origin. The same helper backs `sanitizeLicenseKeyRedirect`, so the
license-key auth endpoint returns the attacker URL in its JSON `redirect` field, and the value
is handed to better-auth `signIn.magicLink({callbackURL})` at `sign-in/page.tsx:96` — it can be
baked into an emailed magic link.

**Intent:** UNINTENTIONAL, provably. The doc comment at `license-key-redirect.ts:4-7` says the
function prevents open redirects and names the two bypasses it blocks;
`nextjs/tests/license-key-redirect.test.ts:61-65` asserts both are blocked. My repro confirms
those two *are* blocked. The tab/newline members of the class were simply missed.

**Repro:** `.../scratchpad/hunt/REPRO-open-redirect.test.ts` (fails as intended) and
`.../scratchpad/hunt/edge/edge-mw.test.ts`, which invokes the **real middleware default export**:
```
TAB              passedValidator=true  -> https://evil.com/  offsite=true
LF               passedValidator=true  -> https://evil.com/  offsite=true
CR               passedValidator=true  -> https://evil.com/  offsite=true
(real middleware) tab returnTo -> {"status":307,"location":"https://evil.com/"}
(real middleware) //evil.com   -> {"status":307,"location":"https://hyperwhisper.com/en/user/dashboard"}
```

**Fix:** stop pattern-matching the string.
`const u = new URL(v, origin); return u.origin === origin ? u.pathname + u.search : fallback;`
— bypass-proof by construction, because it asks the same parser that will later resolve it.

---

### 2. A refund arriving before its checkout is discarded permanently — CONFIRMED · corruption · HIGH

**Surface:** `nextjs/app/api/webhooks/stripe/route.ts:121` → `nextjs/lib/services/stripe-webhook.ts:524`

**Input:** deliver `charge.refunded` for a session whose `checkout.session.completed` has not
yet been processed successfully, then deliver the completion:
```json
{"type":"charge.refunded","id":"evt_refund","data":{"object":
  {"id":"ch_test_ORDER","payment_intent":"pi_1","amount":5300,"amount_refunded":5000}}}
```

**Path:** `stripe-webhook.ts:600` `refundCreditGrant({sourceType:"stripe_credit_pack", sourceId})`
→ `db-layer.ts:455-471` `SELECT … FOR UPDATE` finds **no grant row** → `:470` returns
`{status:"duplicate", refundedAmount:0}` → `stripe-webhook.ts:605-610` logs "already processed"
and returns → `route.ts:132` returns 200. **Nothing anywhere records that the session was
refunded.** Later the completion runs `grantCreditsForStripeEvent` (`db-layer.ts:417-437`) and
grants the credits; there is no refund check on that path.

**Detonation:** The customer is refunded in Stripe **and** keeps the full credit balance (or a
`granted` license key). Silent — the only trace is a `console.log` asserting the opposite of what
happened.

**Why reachable, not hypothetical:** `route.ts:126-129` catches every `handleChargeRefunded`
error and deliberately returns 200 to avoid retry loops, so `charge.refunded` is consumed exactly
once and discarded. Any of these opens the window: the completion is still in Stripe retry
backoff (`route.ts:96-100` returns 500 on handler throw — the normal failure mode, retried up to
3 days); Stripe delivers out of order (documented as unguaranteed); or
`stripe.checkout.sessions.list()` at `stripe-webhook.ts:495` times out. Grepping `app/`, `lib/`,
`src/` shows `charge.refunded` handled in exactly one place, no reconciliation job and no admin
refund tooling — so a dropped refund is permanent.

**Repro:** executed against the real handlers with an in-memory db-layer mirroring the actual
unique indexes and ON CONFLICT semantics:
```
Processing refund for charge ch_test_ORDER (5000/5300)
Credit refund already processed for charge ch_test_ORDER, skipping
  after refund-first: grants = [] keys = 0
Minted license HW-DJAU... with 50000 credits for buyer@example.com
  after completed   : balance = 50000
  >>> customer was refunded AND holds 50000 credits
```

---

### 3. The documented partial-refund policy reclaims zero credits — CONFIRMED · corruption · HIGH

**Surface:** `nextjs/lib/services/stripe-webhook.ts:512-523`

**Input:** the exact transaction the public policy page describes — a $5 credit purchase
(`credit_amount="5000"`, `fee_cents="30"`, charge 530) refunded by $4.50:
`{"id":"ch_p","amount":530,"amount_refunded":450}`

**Path:** `:516` `feeCents = 30` → `:517` `creditPortion = 530 - 30 = 500` → `:518`
`if (charge.amount_refunded < creditPortion) return` — 450 < 500, so `refundCreditGrant` is never
called and all 5,000 credits stay spendable.

**Detonation:** `app/[locale]/legal/refund-policy/page.tsx:186` promises precisely this: *"if you
purchased $5 of HyperWhisper Cloud credits and consumed $0.50 of credits, you will be refunded
$4.50."* Support follows the policy, issues $4.50, and the customer keeps 100% of the credits.
The gate is all-or-nothing in **both** directions: one cent more claws back the full 5,000 rather
than the 4,500 actually refunded.

**Intent:** UNINTENTIONAL — a spec/code divergence, not a threshold to tune. `refundCreditGrant`
(`db-layer.ts:476-481`) only ever computes `originalAmount - refundedAmount`; it has no notion of
a partial amount, so the proportional refund the policy describes **cannot be expressed by the
current code at all**.

**Repro:** executed:
```
Refund 450/530 does not cover the credit portion (500) for credits session cs_p, skipping
  clawback calls: []                     <- NO credits reclaimed
Refund 500/530 -> Deducted 5000 credits
  clawback calls: [{"sourceId":"cs_p"}]  <- full 5000, not 4500
```

---

### 4. Empty transcript bills zero for a fully-paid provider call — CONFIRMED · resource · MEDIUM

**Surface:** `hyperwhisper-cloud/src/routes/transcribe.ts:675-693`

**Input:** any audio up to `MAX_AUDIO_SIZE_BYTES` (2 GB) that the provider returns no words for —
silence, music, noise, a non-speech language.

**Path:** `providers/deepgram.ts:167` sees an empty transcript → `:172-179` returns
`{durationSeconds: 0, costUsd: 0, source:'no_speech'}`, **discarding the real
`data.metadata.duration` it read at `:165`** → `transcribe.ts:675` sets `noSpeech=true` → `:678`
`if (!noSpeech)` means `deductCredits` is **never called at all**. The identical discard exists in
all 11 adapters (`elevenlabs.ts:211`, `groq.ts:138`, `openai.ts:135`, `gemini.ts:267`,
`assemblyai.ts:302`/`549`, `azure-mai.ts:221`, `google-chirp.ts:278`, `mistral.ts:135`,
`soniox.ts:290`, `xai-stt.ts:161`) — including the priciest.

**Detonation:** Executed with a stub reporting `metadata.duration = 7200` (2 real billed hours):
```
STATUS 200 | no_speech_detected = true | reported duration = 0
X-Credits-Used = 0.0 | X-Total-Cost-Usd = 0.000000
deduction POSTs = []      <- nothing ever sent to the ledger
true deepgram cost for 7200s = 0.66 USD = 660 credits
```
Repeatable indefinitely at zero balance cost, since the preflight only *reserves* and never
debits. Free unlimited compute against a metered upstream.

**Intent:** UNCLEAR. Not charging for accidental silence is a defensible UX choice, but the tests
never cover a no-speech result at all — precisely the input category the authors did not imagine.
The arguable defect is that the free path is entirely unmetered.

---

### 5. Concurrent WS sessions each believe they own the whole balance — CONFIRMED · resource · MEDIUM

**Surface:** `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts:131-168` and `:338-344`

**Input:** open N WebSockets concurrently with the same `?account_key=<one valid key>` and stream
audio in all of them.

**Path:** `:159` `validateCredits(auth, minimumStreamingCredits())` is a read-only comparison — no
reservation, no hold, no decrement. `auth.credits` is a snapshot from a **1-hour** Redis cache
(`constants.ts:7`). The in-session guard at `:339` compares against that same per-connection
snapshot, so every connection independently believes it owns the full balance. Deduction is
end-of-session and fire-and-forget (`:209-220`). Grepping
`concurren|max_sessions|activeSessions|semaphore|rate.?limit` across `src/` returns only upstream
429 handling — nothing counts concurrent sessions.

**Detonation:** Measured — **5 concurrent sockets on a key holding 6.3 credits billed 18.5 credits
(2.9× the balance)** and opened 5 upstream Deepgram sockets. The ceiling is N × balance of real
provider spend, with N unbounded.
```
connect-time balance = 6.3 credits (one shared license key)
5 concurrent sockets -> 5 deductions totalling 18.5 credits
per-socket amounts: [3.7,3.7,3.7,3.7,3.7]
```

---

### 6. WS text frames bypass the session byte cap entirely — CONFIRMED · resource · MEDIUM

**Surface:** `ws-streaming-deepgram.ts:293-362`

**Input:** `ws.send('{"t":"' + 'A'.repeat(4*1024*1024) + '"}')` in a loop.

**Path:** `onMessage:299` tests `data instanceof ArrayBuffer` — false for text, so control skips
`:303` (`bytesReceived += data.byteLength`), skips `:308` `MAX_SESSION_AUDIO_BYTES`, skips `:317`
the per-message cap, skips `:326` backpressure, and lands at `:350` `JSON.parse` on an unbounded
string. The counter that bounds the session is grown **only** at `:303`, so text frames can never
trip it.

**Detonation:** Measured **545 MB down one socket in ~3 s** — `close=null`, `readyState=1`, zero
error frames. Binary control traffic at the same volume correctly closes with 1009 "Message too
big" after 136 MB. The comment at `:58-67` states the intent ("Bound total inbound volume so a
flood can't OOM the worker"); the implementation is binary-only. Cost per frame is a full string
allocation plus a parse attempt, and the frames are never forwarded upstream — pure server burn.

---

### 7. Reservation assumes 64 kbps; billing uses real duration — CONFIRMED · resource · MEDIUM

**Surface:** `hyperwhisper-cloud/src/middleware/credits.ts:22-25` + `constants.ts:11`; reserved at
`transcribe.ts:417-418`, billed at `:679`

**Input:** a truthful 6 kbps Opus upload — 8,100,000 bytes carrying 180 minutes, with a matching
`Content-Length`. Nothing is falsified.

**Path:** `estimateAudioSecondsFromSize` divides by the fixed
`BYTES_PER_MINUTE_ESTIMATE = 480_000 // 64kbps` → `validateCredits` passes on that estimate →
`deductCredits` bills from the provider's actual `durationSeconds`.

**Detonation:** Measured across the bitrate range:
```
64 kbps (the assumption), 60 min   reserved=589.8  billed=330   ratio=0.56x
32 kbps opus, 180 min              reserved=884.7  billed=990   ratio=1.12x
16 kbps opus, 180 min              reserved=442.4  billed=990   ratio=2.24x
 6 kbps opus, 180 min              reserved=165.9  billed=990   ratio=5.97x
 6 kbps opus, 600 min              reserved=553    billed=3300  ratio=5.97x
```
Because `deductCreditBalance` floors at 0 (`license/credits/route.ts:117-119`) and
`spendCreditGrantsByProvenance` floors per grant (`db-layer.ts:591`), the overrun is never owed
and **never logged as uncollected** — the response still reports `credits_deducted: 990`.

**Intent:** UNCLEAR leaning UNINTENTIONAL. `credits.ts:11` calls 64 kbps the "minimum encoded
bitrate expected from clients", so the estimate was meant to be conservative — and it is, at the
assumed bitrate. The defect is that the assumption concerns client behaviour on an endpoint open
to anyone with a key, and nothing enforces a bitrate floor. Note `transcribe.ts:444-456` rejects a
body larger than the declared `Content-Length`, closing the "lie about the size" hole; this attack
needs no lie, which is exactly why it survives that check.

---

### 8. Every license-API failure mode silently voids the charge — CONFIRMED · corruption · MEDIUM

**Off-thesis flag:** not attacker-supplied. Found while tracing the credit path, not by supplying
a hostile value. Reported because it is confirmed and consequential.

**Surface:** `hyperwhisper-cloud/src/middleware/credits.ts:60-96`

**Path:** `transcribe.ts:679` calls `deductCredits` **without await**; the 200 with the transcript
is flushed at `:695`. `recordLicenseUsage` then `console.warn`s and returns on non-2xx (`:74-82`)
or on network error/timeout (`:92-96`). No retry, no dead-letter, no persistence — even though
`retryWithBackoff` already exists at `lib/utils.ts:63` and is used elsewhere.

**Detonation:** During any Vercel outage, cold start beyond the 10 s timeout, or 5xx, **every
transcription is free**, while the response header still reports `X-Credits-Used: 660.0`. Executed
across all five failure modes:
```
license API 200 OK        amountSent=660 | attempts=1 | deductCredits() returned=660
license API 400           amountSent=660 | attempts=1 | deductCredits() returned=660
license API 500           amountSent=660 | attempts=1 | deductCredits() returned=660
license API network error amountSent=660 | attempts=1 | deductCredits() returned=660
license API 10s timeout   amountSent=660 | attempts=1 | deductCredits() returned=660
```
`attempts=1` in every row is the absence of retry; the identical return value in every row means
**the caller cannot distinguish "charged" from "dropped"**.

---

### 9. A transcript mentioning `<INSTRUCTIONS>` is silently not processed, and billed twice — CONFIRMED · corruption + resource · MEDIUM

**Surface:** `hyperwhisper-cloud/src/routes/post-process.ts:189-224` + `lib/text-processing.ts:176`

**Input:**
```json
{"text":"open the file and edit the <INSTRUCTIONS> block at the top",
 "prompt":"Clean up this transcript.","account_key":"<valid key>"}
```
Also fires on `--TRANSCRIPT--`, `--ENDTRANSCRIPT--`, `<USER_SYSTEM_PROMPT>`,
`<APPLICATION_CONTEXT>`, `<CUSTOM_VOCABULARY>`.

**Path:** the LLM correctly returns the corrected transcript, which necessarily still contains the
caller's own marker → `llm-completion.ts:76` `containsPromptLeakage` → `text-processing.ts:176`
`MARKERS.some(m => text.includes(m))`, a bare substring test with no positional or structural
check, so the caller's own content is indistinguishable from a leaked prompt → a **second full LLM
call** to the fallback provider (`post-process.ts:189-206`) → `:213` `costUsd += retryResponse.costUsd`
→ second "leak" → `:219-224` returns the **raw input**.

**Detonation:** Any transcript mentioning one of six common developer strings silently disables
post-processing (200 OK, no warning field, input returned verbatim) **and** bills exactly 2×.
Deterministic and content-triggered — someone dictating about prompt engineering hits it every
time. Executed with providers stubbed to echo faithfully, so no provider misbehaviour is involved:
```
BASELINE provider calls: ["cerebras"]         billed usd: [0.00004]
HOSTILE  provider calls: ["cerebras","groq"]  billed usd: [0.00008]
         corrected: "open the file and edit the <INSTRUCTIONS> block at the top"  (unchanged)
```

---

### 10. Audio sent before the `ready` frame is silently discarded — CONFIRMED · corruption · MEDIUM

**Surface:** `ws-streaming-deepgram.ts:294-296`

**Input:** connect and, on the transport `open` event (not the app-level `ready`), immediately send
10 × 32000-byte ArrayBuffers.

**Path:** `onMessage:294` `if (!deepgramWs || deepgramWs.readyState !== WebSocket.OPEN)` → bare
`return` at `:295`. No buffer, no error frame, no close, no log.

**Detonation:** Measured with a 400 ms upstream handshake — **320,000 bytes (10 seconds of speech)
sent, 0 bytes reached upstream**, and the client received only `{"type":"ready"}` with no warning
of any kind. The control run sending identical frames after `ready` delivered 320,000/320,000. In
practice the opening words of a dictation vanish whenever the Deepgram handshake is slow, and
neither the user nor the client can detect it. `ready` is the only signal and is documented nowhere
in the file as a gate.

---

### 11. The one destructive credits route is the only one with no rate limit — CONFIRMED · resource · MEDIUM

**Surface:** `nextjs/app/api/license/credits/route.ts` (POST) and its `account/*` alias

**Input:** `{"license_key":"<any valid key>","amount":1000000}` in an unbounded loop.

**Path:** `route.ts:80` — **no rate limiter is imported or called anywhere in this file** →
`findAccountByKey` → `deductCreditBalance` at `:119`. Its two read-only siblings both call
`licenseValidateRateLimiter.limit(clientIP)` (`validate/route.ts:62`, `activate/route.ts:30`,
30/min/IP).

**Detonation:** Anyone who learns a license key can zero that account's wallet at 1,000,000 credits
per request at unlimited rate. Compounding: `hyperwhisper-cloud/src/middleware/credits.ts:61-72`
calls this endpoint with **no service credential** — Content-Type only — so the user's own bearer
is the sole gate on a write the cloud worker makes on their behalf; the `x-internal-secret` pattern
used by `app/api/internal/*` is absent here.

**Honest caveat, and why MEDIUM not HIGH:** a key holder can already spend those credits through
the product. The delta is destroy-without-use plus unbounded rate, not privilege gain. Verified by
reading the route's imports rather than by flooding anything.

---

### 12–20. The LOW tier, grouped

Nine further findings are real, executed, and genuinely LOW. Grouping them deliberately: ten
low-severity findings do not add up to a high one, and spelling each out at full length would bury
findings 1–3.

| # | Finding | File:line | Class | Executed |
|---|---|---|---|---|
| 12 | A zero-audio WS session (connect, send nothing, close) is charged 0.1 credits via the `creditsForCost` floor; 10 hotkey cycles = 1.0 credit for 0 seconds of audio | `ws-streaming-deepgram.ts:208` + `cost-calculator.ts:497` | corruption | yes |
| 13 | No session-duration bound on WS: one 1-byte frame every 5 s defeats both Fly's 60 s idle timeout (the server itself pings at `:287`) and Deepgram's 10 s no-audio timeout, pinning a worker socket and a provider slot indefinitely for ~0.1 credits | `ws-streaming-deepgram.ts` (no timeout exists) | resource | mechanism only |
| 14 | `drainPendingDeductions` returns the *pre-drain* count regardless of whether anything settled, so `index.ts:96` logs "drained N" while `process.exit(0)` kills them — the only telemetry for lost money reports the opposite of the truth | `credits.ts:106-116` | error-quality | yes |
| 15 | `device_id` is never type-checked, trimmed or length-capped: an object or array reaches the driver, and `"dev-1"`/`"dev-1 "`/`"DEV-1"` become three rows, inflating the fair-usage device count. Self-inflicted only — `licenseKeyId` is server-resolved | `validate/route.ts:110-111` | corruption | yes (handler boundary) |
| 16 | Client-supplied `language` is interpolated raw into the Gemini instruction text, letting a caller rewrite the operator's prompt. Self-injection only — the caller's own paid request, no cross-tenant reach — but `language` has no length or charset cap at any hop | `gemini.ts:54` | injection | yes |
| 17 | Malformed, empty or `null` JSON body → 500 instead of 400; all three sibling routes wrap `req.json()` and return a clean 400 | `license/credits/route.ts:82-83` | error-quality | yes |
| 18 | Non-string `license_key` (`123`, `{}`, `true`, `[]`) → 500 via `licenseKey.trim()`; the sibling `credits` route has the `typeof` check and correctly 400s the identical input | `validate/route.ts:89` → `license-validation.ts:126` | error-quality | yes |
| 19 | A lowercased license key returns `valid:true` from `/validate` (the Polar import dedupes case-independently) but `"not found"` from `/credits` (`eq()` is case-sensitive). Also causes a permanent uncached Polar call on every such request | `license/credits/route.ts:43` vs `license-validation.ts:126-150` | error-quality | yes (credits side) |
| 20 | The response reports `credits_deducted: amount` (requested) rather than the amount actually collected, which `deductCreditBalance` computes then discards. A lying receipt, not lost money — the grant ledger is authoritative and self-heals | `license/credits/route.ts:135` + `db-layer.ts:626-629` | error-quality | reasoned |

## Plausible

Four candidates whose mechanism is real but whose trigger I could not fully construct. Each names
the unproven link, per the brief.

**P1. Unicode casefolding delivers a victim's license key to a different mailbox — authz-bypass.**
`stripe-webhook.ts:324` does `getAccountKeysByEmail(customerEmail.toLowerCase().trim())`, and
`"Kray@example.com"` written with U+212A KELVIN SIGN lowercases to byte-identical
`"kray@example.com"`, matching the victim's row → `:412-426`
`sendCreditTopUp({customerEmail, licenseKey: license.key})` mails the **victim's key** to the raw
attacker-supplied address, and the attacker's credits pool onto the victim's account. Executed
control flow:
```
attacker checkout email codepoints: U+212A U+72
Pooled 5000 credits into existing key HW-VICT... for Kray@example.com
emails = [["topup","Kray@example.com","HW-VICTIM-SECRET-KEY"]]
```
**Unproven link:** the attacker must actually receive mail at an SMTPUTF8 address containing U+212A
*and* get it past Stripe's checkout email validation. Neither was verified. The underlying defect is
unambiguous regardless — the recipient is taken from attacker input rather than `license.email`,
which the sibling `handleCreditTopUp` does correctly at `:265`. Plain ASCII case and whitespace
variants fold safely; a zero-width space does not fold.

**P2. `MAX_CREDIT_DEDUCTION_AMOUNT` fails open — corruption.** A `costUsd > $1000` produces
`amount > 1_000_000`, which `validation.ts:14` rejects with a 400 — which finding 8's mechanism then
swallows, billing **zero** instead of capping at the maximum. Executed at function level.
**Unproven link:** reachability. Under the 2 GB body cap the priciest chain member constructible
tops out near $763, so no single request crosses $1000. A latent fail-open, not a live exploit.

**P3. Concurrent transcribe requests all validate against one cached balance — resource.**
`validateCredits` is a pure read of a Redis-cached balance with no hold row, and the cache is
refreshed only *after* a deduction lands (`credits.ts:86`). N concurrent requests on one key all
validate against the same pre-spend balance, and `db-layer.ts:591` floors collection at what is
actually there — so N−1 are free. The same shape as finding 5, on the HTTP path.
**Unproven link:** no racing repro was built; this is a concurrency surface, not an input-shape one.

**P4. Aborting an assistant stream mid-flight bills zero — resource.** `assistant.ts:346`
`costPromise.then(costUsd => { if (costUsd > 0) … })` — a client that aborts may resolve
`costPromise` at 0 while Anthropic still bills the consumed tokens.
**Unproven link:** the abort repro was not built.

## Refuted

Live candidates that died on inspection. Recorded so the next hunt does not re-raise them.

- **Rate-limit bucket spoofing via `X-Forwarded-For`** — REFUTED, and this was **my own** mid-hunt
  lead. `getClientIPFromHeaders` (`download-ip.ts:14-26`) ranks `x-vercel-forwarded-for` first,
  which Vercel sets and clients cannot forge; garbage falls back to a literal `"unknown"` bucket
  rather than a free pass. Executed: `{vercel:"9.9.9.9", xff:"1.2.3.4"} -> 9.9.9.9`.
- **`timingSafeEqualSecret` fails open when the env var is unset** — REFUTED. The guard is
  `if (!received || !expected) return false` *before* any comparison. Full matrix executed
  (undefined/null/`""`/length-mismatch/case/10KB): all `false`, only the exact match `true`. All
  four importers use it, and no `===` secret comparison exists anywhere in `nextjs/`.
- **Stripe webhook replay window** — REFUTED. `db-layer.ts:417` opens a transaction, `:418-426`
  inserts the event id with `onConflictDoNothing`, `:428-430` returns early on duplicate, and the
  grant at `:432-437` runs only afterwards — **same transaction, dedupe first**. Concurrent
  deliveries block on the unique index. Executed: 3 back-to-back deliveries →
  `balance=50000 keys=1 emails=1`.
- **IDOR, everywhere** — REFUTED across all six clusters, and this was the catalog's
  highest-priority row. `license/*` and `account/*` are literally the same module — the `account/*`
  files are one-line `export { POST } from "../../license/…"` re-exports — so there is no
  divergence to exploit. Every route takes exactly one identity input, the license key, which *is*
  the credential, and `license.id`/`license.userId` are always derived server-side. All 14 tRPC
  procedures check out: the admin gate is a **middleware on the `adminProcedure` builder**
  (`server/api/trpc.ts:101-120`, bound at `:148`), so it cannot be forgotten per-procedure; 7 of 7
  admin procedures are gated; `customer.*` is keyed off `ctx.user.email` only; and `role` is
  `input: false` at `src/lib/auth.ts:18`, so it is not settable through the auth API.
- **Drizzle `numeric`-as-string poisoning balance arithmetic** — REFUTED. Every read of a numeric
  column is `Number()`-wrapped before arithmetic (`db-layer.ts:321, 366, 476-478, 518, 590, 648,
  693`) and every threshold comparison happens in Postgres. The `"9.00" > "10.00"` hazard is real in
  the schema and never realised in code. This was my own seeded lead.
- **Sub-cent deduction rounding to zero at `numeric(20,2)`** — REFUTED, impressively.
  `validation.ts:18-20` rejects any amount that does not round-trip at 2 decimals, and the comment
  at `:3-6` shows the authors identified this exact hazard first. All 25 catalog number rows were
  executed against it — `0`, `-0`, `-1`, `"42"`, `true`, `[]`, `{valueOf:()=>5}`, `MIN_VALUE`,
  `EPSILON`, `0.1+0.2`, `MAX_SAFE_INTEGER`, `2^53+1`, `1e999→Infinity`, `999999.999` — and every
  one was correctly rejected. Also my own seeded lead.
- **Under-reserving by declaring a small `Content-Length` and streaming more** — REFUTED.
  `transcribe.ts:447-456` compares the actual `byteLength` against the declared value and rejects
  the mismatch, with a comment naming this exact attack.
- **Also checked and clean:** protocol-relative `//evil.com` and `/\evil.com` (blocked); prototype
  pollution via `__proto__` on credits POST, assistant messages and WS frames (all safe); SQLi via
  Drizzle `eq()` (parameterized); `internal/models` unauthenticated (public by design —
  `Cache-Control: public, s-maxage=3600` with an explicit anonymous-traffic comment);
  message-before-auth on the WS upgrade (auth at `:154` strictly precedes listener attachment at
  `:293`); credentials in logs (`logging.ts` serializes only explicit fields, and no `req.url`
  reaches a log call); CRLF header injection (Bun's `Headers.set` throws); `download` route
  traversal (`platform` collapses to a two-value enum, `arch` is allow-listed, the redirect host is
  force-overwritten); `config` route leakage (returns two hard-coded integers and reads no env var);
  checkout price tampering (server-resolved, `amount` bounded to 5–500 integer dollars, quantity
  hard-coded); negative/NaN/Infinity duration (fails closed to the 0.1 minimum); and double
  activation plus Polar re-import double-grant (both idempotent by construction).

## Coverage

| Surface | Blast | Fuzzed | Categories applied | Skipped (why) |
|---|---|---|---|---|
| `middleware.ts` / i18n | HIGH | yes | strings, identity | time, collections (no such inputs) |
| license + account routes (8) | HIGH | yes | strings, numbers, collections, identity, sequencing | time (no client timestamp) |
| `license/credits` GET+POST | HIGH | yes | numbers (all 25 rows), strings, collections, identity | time |
| Stripe + blog webhooks | HIGH | yes | sequencing, identity, collections | strings/numbers (post-signature; metadata is server-set) |
| internal routes (4) | HIGH | yes | strings, identity | time, collections (single scalar) |
| `transcribe` / `assistant` / `post-process` | HIGH | yes | strings, numbers, collections, resource | time; identity (key-scoped, no second id) |
| WS streaming | HIGH | yes | sequencing, strings, resource, time | collections, identity (flat `{type}` only) |
| credits / cost accounting | HIGH | yes | numbers, sequencing | strings (numeric surface only) |
| tRPC incl. `admin/` (14 procs) | HIGH | yes | identity, numbers, strings | collections (no array/record input exists) |
| `checkout`, `config`, `download` | HIGH | yes | strings, numbers, identity | time, collections |
| `providers/*` — 14 of 24 read | MED | partial | strings (URL construction) | rest grepped only; cannot exercise without real API calls |
| `components/*` (21), marketing pages (39) | LOW | no | — | not input surfaces; an attacker posts to the API directly |

**Not examined.** The 102 unopened files are broken down by area in the coverage ledger above. The
honest gaps *inside* covered surfaces: no finding involving a real Postgres was proven against one
(findings 2, 3, 15 and 20 rest on faithful in-memory stand-ins); 10 provider adapters were grepped
rather than read, so a bug in their response handling would have been missed; and the Chirp
`batchRecognize` path (`google-chirp.ts:240-740`) plus the `azure-mai.ts` async poll/cleanup paths
were not traced, though both create GCS objects before a 300 s in-request deadline — worth a look
for orphaned objects on abort, which is a lifecycle question this strategy is not shaped to ask.
`redis.ts` behaviour against a real Upstash is untested. Finally, whether
`response.headers.set("x-pathname", …)` in middleware actually reaches
`headers().get("x-pathname")` in `app/[locale]/layout.tsx:54` is unresolved — it is set as a
response header rather than via `NextResponse.next({request:{headers}})`, and if it does not
propagate then every page's canonical and hreflang tags collapse to the site root. That is an SEO
correctness bug rather than a security one, and settling it required booting a dev server, which
would have loaded the real `.env.local` secrets — out of bounds under the rules.
