### Candidate
File: `hyperwhisper-cloud/src/middleware/credits.ts`
Line: 74
Invariant: I2
Claim: `recordLicenseUsage()` treats a non-2xx response from `POST /api/license/credits` as a no-op (`console.warn` + bare `return` at line 81) and swallows every network/timeout error in the `catch` at line 92 — the charge is dropped with no retry, no queue, and no signal to the caller (`performDeduction` still resolves successfully).
Failure scenario: The provider call already ran and HyperWhisper was billed. Any Vercel cold-start 500, a 5xx during a `nextjs` deploy, or a response slower than `LICENSE_API_TIMEOUT_MS` on the licensing app means the user keeps the transcript/completion and is charged **zero** credits, permanently. Because `deductCredits()` is fire-and-forget, nothing upstream ever learns the deduction failed — the SIGTERM drain is defeated too (it awaits a promise that resolves "successfully" having charged nothing). At scale this is uncapped free usage during every `nextjs` incident window.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/transcribe.ts`
Line: 678
Invariant: I2
Claim: When any STT adapter returns `source: 'no_speech'`, `deductCredits()` is skipped entirely (`if (!noSpeech)`), yet that value is returned **after** a completed, provider-billed transcription — all 11 adapters produce it from a successful 200/`status: completed` response (`deepgram.ts:168`, `groq.ts:129`, `elevenlabs.ts:202`, `openai.ts:132`, `mistral.ts:132`, `assemblyai.ts:301` and `:548`, `soniox.ts:289`, `xai-stt.ts:152`, `azure-mai.ts:212`, `gemini.ts:264`, `google-chirp.ts:269`).
Failure scenario: Deepgram/Groq/OpenAI/AssemblyAI/ElevenLabs all meter by audio duration submitted, not by transcript content. A user who uploads silence, room noise, music, or non-speech audio gets a fully paid-for transcription for 0 credits every single time. This is a deterministic, trivially repeatable free-transcription oracle: a client can push arbitrarily long silent WAVs and HyperWhisper eats 100% of the provider bill. Note the adapters also hardcode `durationSeconds: 0, costUsd: 0` on this path, so even removing the guard would still deduct nothing real.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/transcribe.ts`
Line: 550
Invariant: I2
Claim: A `ProviderUnavailableError` thrown *after* the upstream has already done (and billed) the work causes `continue` to the next chain member; only the surviving provider's `result.costUsd` is ever deducted at line 679. The first provider's real spend is never charged.
Failure scenario: Concrete triggers that all fire post-billing: `deepgram.ts:159` and `groq.ts:119` throw `ProviderUnavailableError('malformed 200 response body')` after a **200 OK** (Deepgram/Groq already transcribed and billed); `elevenlabs.ts:185` throws on a non-JSON 200; `assemblyai.ts:604` and `soniox.ts:263` throw `poll deadline exceeded after 240000ms` after the async job was created and is being processed (AssemblyAI/Soniox bill the submitted job regardless of whether we collect the result); `fetchWithTimeout`'s `kind: 'timeout'` is explicitly documented at `transcribe.ts:527` as "we gave up; upstream may have been fine". So a >4-minute audio file on AssemblyAI, or one edge-proxy hiccup on Deepgram, produces two paid provider calls and exactly one deduction — the user pays for the cheaper fallback while HyperWhisper absorbs the abandoned job.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/assistant.ts`
Line: 351
Invariant: I2
Claim: The deduction is gated on `if (costUsd > 0)`, and `streamAnthropicChat`'s `cancel()` handler (`providers/anthropic.ts:250-259`) resolves the cost from `inputTokens`/`outputTokens` that are only populated once Anthropic's `message_start` event has been parsed — so a client disconnect before that event yields `costUsd === 0` and no deduction at all.
Failure scenario: A client POSTs `/assistant` with a 10 MB screenshot plus conversation history and drops the connection within the first few hundred milliseconds (or a flaky mobile/desktop network does it for them). Anthropic has already received and is billing the full vision request — a screenshot is easily 1,500-3,000 input tokens plus the message history — but `costUsd` is 0, the `if` short-circuits, and the user is charged nothing. Repeating this in a loop is unmetered Anthropic vision spend against a valid account key that never drops below its balance, so `validateCredits` never blocks it either.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts`
Line: 208
Invariant: I2
Claim: `endSession()` guards on `creditsUsed > 0`, but `creditsForCost()` (`lib/cost-calculator.ts:496-503`) returns a hard floor of `0.1` for **any** input including `costUsd <= 0` — so the guard is always true and a deduction fires on every session teardown, including sessions where zero audio was ever forwarded to Deepgram.
Failure scenario: `onOpen` returns early at line 241 when `DEEPGRAM_API_KEY` is unset, closing the client socket with 1011; `onClose` then runs `endSession()` with `totalDurationSeconds === 0`, and the user is charged 0.1 credits for a server misconfiguration in which no upstream call was made at all. Same for a client that opens the socket and disconnects before speaking, or a Deepgram handshake that fails. A desktop client that opens a streaming socket on app launch or retries a failing connection burns 0.1 credits per attempt against a real balance, and the `session_complete` message it receives reports `credits_used: 0.1` for `duration_seconds: 0`. (Note `estimateCreditsForCost` at line 505 returns 0 for the same input — the two siblings disagree.)
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts`
Line: 188
Invariant: I2
Claim: A live streaming session accumulates `totalDurationSeconds` in memory and only converts it to a `deductCredits()` call at teardown; `drainPendingDeductions()` (`middleware/credits.ts:106`) drains `inFlightDeductions`, which a not-yet-ended session has not entered, and `index.ts:99` then calls `process.exit(0)` without ever invoking `endSession()`.
Failure scenario: On every Fly deploy or scale-down, each in-progress `/ws/streaming-deepgram` session is terminated with its entire accumulated duration unbilled — up to `MAX_SESSION_AUDIO_BYTES` (100 MB ≈ 52 minutes) of Deepgram Nova-3 audio that Deepgram has already metered and invoiced. The 4-second graceful-shutdown window explicitly exists to prevent exactly this loss for HTTP routes but does not cover the WebSocket route.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/lib/utils.ts`
Line: 78
Invariant: I2
Claim: `retryWithBackoff` re-invokes `fn()` on **any** thrown error, and the LLM clients throw *after* a billed 200 — `cerebras.ts:49`, `groq-llm.ts:58` and `openai-llm.ts:63` all do an unguarded `await response.json()` outside any try. Every attempt after the first billed attempt is a second full provider charge, but `post-process.ts` deducts only the single `llmResponse.costUsd` that the winning attempt reports.
Failure scenario: A truncated or non-JSON 200 body from Cerebras (the default provider, retried up to `retriesFor('groq') = 3` times) means the provider generated and billed tokens on attempt 1, `response.json()` throws, `retryWithBackoff` sleeps and calls again — up to 4 paid completions, one deduction. Worse, a JSON parse error carries no `.status`, so `shouldFallback()` (`lib/llm-provider.ts:176`) returns false and `post-process.ts:171` returns a 500 with **no deduction at all** — the user gets an error and pays nothing for up to 4 billed LLM completions.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/providers/anthropic.ts`
Line: 136
Invariant: I2
Claim: The streaming Anthropic `fetch` carries only `abortController.signal` (fired solely on client disconnect) and no `AbortSignal.timeout`, so a stalled upstream leaves `start()` suspended forever; `costPromise` is never resolved and the `costPromise.then(...)` deduction in `assistant.ts:350` never runs on any path.
Failure scenario: Anthropic accepts the request (billing the input tokens for the screenshot), begins the SSE stream, then stalls without closing the socket — a known failure mode during provider incidents. The client eventually times out on its own side without triggering `cancel()` on the server's `ReadableStream`, `resolveCost` is never called, and the request is billed by Anthropic but charged 0 credits. Under a provider incident this silently affects every concurrent `/assistant` request on the machine, and the pinned promises are also invisible to the SIGTERM drain.
Confidence: low

### Coverage
**Examined buckets:**
- **B1 cloud-entry-and-auth** — `middleware/credits.ts` read end to end (the deduction primitive, `inFlightDeductions`, `drainPendingDeductions`); `index.ts` SIGTERM/`gracefulShutdown` drain path; `middleware/auth.ts` reviewed only for whether it can deduct (it cannot).
- **B2 cloud-routes** — all 5 route files read for every `return`/exit path: `transcribe.ts`, `post-process.ts`, `assistant.ts`, `ws-streaming-deepgram.ts`, `usage.ts`. `usage.ts` contains no deduction and is read-only w.r.t. billing.
- **B3 cloud-stt-providers** — all 11 STT adapters swept for `no_speech` returns and for post-200 `ProviderUnavailableError` throws (the two "already billed, not charged" idioms); `providers/utils.ts` `retryWithBackoff` read in full.
- **B4 cloud-llm-providers** — `anthropic.ts` read end to end (both `requestAnthropicChat` and `streamAnthropicChat`); `lib/llm-provider.ts` `callWithRetry`/`shouldFallback` read in full; `cerebras.ts`/`groq-llm.ts`/`openai-llm.ts` checked for post-200 throw sites.
- **B5 cloud-billing-and-google** — `cost-calculator.ts` `creditsForCost`/`estimateCreditsForCost` (the 0.1 floor that makes several `> 0` guards vacuous).
- **B6 next-money-api** — `app/api/license/credits/route.ts` GET+POST read in full; `deductCreditBalance` → `spendCreditGrantsByProvenance` in `src/lib/db-layer.ts`. The deduct POST is a single atomic ledger spend; no double-application path found on the Next.js side (Stripe **grant** dedupe is I5's territory, not reported here).

**Not examined / partially examined:**
- **B7–B12** (next edge/auth, tRPC, db-and-services beyond `deductCreditBalance`, public site, account UI, next tests) — no `deductCredits`/deduction call sites exist there; the only money-write reachable from the Fly service is `POST /api/license/credits`, which was covered under B6. Deliberately skipped as out-of-invariant.
- `spendCreditGrantsByProvenance`'s internal transaction was read only at its entry point — I confirmed it is a single atomic call per HTTP POST but did not audit its grant-selection SQL for partial application under contention.
- `gcs-storage.ts` (google-chirp's GCS upload is a real but negligible paid operation that is never deducted on a failed transcription) — noted, not filed, as the cost is sub-cent.

**Leads refuted:**
- **`assistant.ts:350` — "a rejected `costPromise` drops the charge entirely": REFUTED.** `costPromise` is built at `anthropic.ts:119` as `new Promise((resolve) => { resolveCost = resolve })` — the executor never captures `reject`, so the promise is structurally incapable of rejecting. Every branch of `start()` (`!response.ok` → 163, no body → 171, success → 229, catch → 247) and `cancel()` (→ 258) calls `resolveCost`. The one `return` without a resolve (line 233) is correct: it is reached only when `signal.aborted`, and only `cancel()` aborts, having already resolved synchronously on the preceding line. The real defects on this path are different: the `costUsd > 0` gate dropping a pre-`message_start` disconnect, and the un-timed-out `fetch` leaving the promise unsettled (filed above).
- **`ws-streaming-deepgram.ts` `endSession()` concurrently reachable from `onClose`, `onError` and Deepgram's `close` listener → double deduction: REFUTED.** Although `endSession` is `async` and all three call sites `await` it, the guard `if (sessionEnded) return; sessionEnded = true;` (lines 189-190) executes synchronously at the top of the function body before any `await`. On a single-threaded event loop no interleaving is possible between the read and the write, so at most one deduction can ever fire. The genuine defects on this route are under-billing/over-billing at the boundaries (0-second sessions charged 0.1; whole sessions lost on SIGTERM), not duplication.
- **`performDeduction` bypassing `deductCredits()`: REFUTED.** `grep performDeduction` across both services returns exactly two hits, both in `middleware/credits.ts` (the declaration at line 132 and the single call at line 124 inside `deductCredits`). No call site escapes `inFlightDeductions`. However, the drain it feeds is undermined by the separate `recordLicenseUsage` swallow bug filed above — draining a promise that resolves without having charged anything provides no protection.
- **`post-process.ts` double deduction (catch-path at 256 + happy-path at 280): REFUTED.** The `catch (extractError)` block returns a 500 immediately after deducting, so the two sites are mutually exclusive. Separately, the code comment at lines 208-210 claiming the outer catch would bill a retry whose evaluation throws is *inaccurate* — `evaluateCompletionResponse(retryResponse.raw, text)` at line 215 sits inside the inner `try` and would be caught at line 234 — but the outcome is still exactly one deduction at line 280 including the retry cost, so the invariant holds despite the misleading comment.
