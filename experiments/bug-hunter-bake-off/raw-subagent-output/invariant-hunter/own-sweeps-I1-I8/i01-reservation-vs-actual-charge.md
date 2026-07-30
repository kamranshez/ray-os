I've traced every reservation site. Findings below.

### Candidate
File: `hyperwhisper-cloud/src/routes/post-process.ts`
Line: 18
Invariant: I1
Claim: `ESTIMATED_POST_PROCESS_CREDITS = 1.0` is a flat constant independent of input size, while the route accepts `text` up to 100,000 chars (~25k prompt tokens) and bills the real token cost.
Failure scenario: A user with 1.0 credit POSTs 100,000 chars of text with the default provider (`cerebras`, $0.35/M in, $0.75/M out). The preflight passes; the corrected text comes back; `deductCredits` bills ~$0.0275 = ~28 credits. `deductCreditBalance` floors the balance at 0 (`nextjs/app/api/license/credits/route.ts:112`), so HyperWhisper eats ~27 credits of provider spend. With `X-LLM-Provider: grok` ($1.25/$2.50 per M) the same request bills ~94 credits against a 1.0 reservation. Repeatable indefinitely from a single near-zero-balance key.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/post-process.ts`
Line: 93
Invariant: I1
Claim: `prompt` is trimmed and non-empty-checked but has **no length cap** (unlike `text`, capped at `MAX_TEXT_LENGTH`), and `/post-process` has no `Content-Length` gate anywhere (`index.ts:48` mounts the route bare, no `bodyLimit`); the prompt is sent verbatim as the system message and billed as input tokens against the same flat 1.0 reservation.
Failure scenario: A caller sends `{"text":"hi","prompt":"<20 MB of text>"}`. Preflight reserves 1.0 credit. `buildCorrectionRequest` puts all 20 MB in the system message → ~5M input tokens forwarded to the provider. Even truncated at the model's context limit, the billed input cost is orders of magnitude above 1.0 credit, and the balance floors at 0. Unlike `/transcribe` and `/assistant`, nothing bounds the body before it is buffered.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/post-process.ts`
Line: 213
Invariant: I1
Claim: The prompt-leakage path runs a **second full LLM call on a different provider** and does `costUsd += retryResponse.costUsd` with no second `validateCredits` call — total spend is up to 2 complete billed completions against a reservation of 1.0 credit taken once at line 118.
Failure scenario: A transcript that triggers `evaluateCompletionResponse(...).failure === 'prompt_leakage'` (a model echoing the instructions — reproducible with adversarial `text`) causes provider A's completion plus provider B's completion to both be summed into one deduction. With `X-LLM-Provider: grok` the leakage retry routes to `anthropic` (`LLM_PROVIDER_FALLBACKS`), so a single request bills grok-4.3 **and** claude-haiku-4-5 output tokens. The user is charged (and, at low balance, the business absorbs) roughly double the already-under-reserved amount, with no preflight ever having seen the second call.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/routes/assistant.ts`
Line: 311
Invariant: I1
Claim: `estimatedCredits = 3.0 × imageCount` scales only with image count; the text side of the request (`messages` up to `ASSISTANT_MAX_MESSAGES_BYTES` = 6 MB) and the output side (`ANTHROPIC_MAX_TOKENS = 8192`) are entirely unreserved.
Failure scenario: A user with 3.0 credits POSTs one image plus a long conversation. Preflight reserves 3.0. `streamAnthropicChat` runs claude-haiku-4-5 ($1/M in, $5/M out). Output alone at the 8192-token ceiling is $0.041 = **41 credits**; a 190k-token conversation adds $0.19 = 190 credits of input. `costPromise.then` fires `deductCredits` after the stream, balance floors at 0, and the user keeps the streamed answer. A single request can exceed its reservation by ~70x with no image count above 1.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/middleware/credits.ts`
Line: 23
Invariant: I1
Claim: `estimateAudioSecondsFromSize` derives duration from `BYTES_PER_MINUTE_ESTIMATE = 480_000` (a hardcoded 64 kbps assumption), but every STT adapter bills against the **provider-reported true duration**; audio encoded below 64 kbps under-reserves in direct proportion to the bitrate ratio, and nothing re-checks the balance after the true duration is known.
Failure scenario: A user uploads a 1 MB Opus/AMR file encoded at 12 kbps — ~11 minutes of audio. `estimateCreditsForProviderFallbacks(1_048_576, 'elevenlabs', …)` estimates 131 s and reserves ~$0.0215 = ~22 credits. ElevenLabs returns `duration ≈ 660 s`; `computeElevenLabsTranscriptionCost` bills $0.108 = **109 credits**. The `audioBuffer.byteLength > contentLength` guard at `transcribe.ts:447` does not help — the client declares the true (small) size honestly. The user gets an 11-minute transcript for a 22-credit reservation; at low balance the difference is absorbed by the business.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/routes/ws-streaming-deepgram.ts`
Line: 159
Invariant: I1
Claim: The upgrade preflight reserves `minimumStreamingCredits()` — ~30 s of Deepgram audio (~2.8 credits) — but the session may run to `MAX_SESSION_AUDIO_BYTES = 100 MB` (~52 min, ~286 credits), and the only in-session bound (`creditsUsed >= auth.credits`, line 339) compares against the Redis-cached balance rather than anything reserved.
Failure scenario: A client opens `/ws/streaming-deepgram` with a cached balance of a few hundred credits, streams 52 minutes of linear16, and `endSession()` deducts ~286 credits against a 2.8-credit reservation. Worse: `auth.credits` comes from the 1-hour `license:<key>` cache, so a key drained to 0 elsewhere (or on another Fly region) in the last hour keeps passing line 339 for the whole session; the end-of-session deduction then floors at 0 and the Deepgram minutes are unrecovered.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/lib/stt-models.ts`
Line: 172
Invariant: I1
Claim: The Gemini Pro reservation rates (`gemini-2.5-pro: 0.0075`, `gemini-3.1-pro-preview: 0.0100` USD/min) are purely **per-minute**, but `providers/gemini.ts:44-48` forces a non-zero **per-request** thinking budget on exactly those models (`thinkingBudget: 128` for 2.5-pro, `thinkingLevel: 'low'` for 3.x) and `computeGeminiTranscriptionCost` bills `thoughtsTokenCount` at the full output rate.
Failure scenario: A user transcribes a 5-second clip with `X-STT-Model: gemini-3.1-pro-preview`. `estimateAudioSecondsFromSize` clamps to 10 s → reservation = (10/60) × $0.01 = $0.00167 ≈ 1.7 credits. Gemini 3 Pro at `thinkingLevel: 'low'` emits on the order of 500 thinking tokens at $12/M = $0.006 → the deduction is ~7 credits, roughly 4x the reservation. On `gemini-2.5-pro` the fixed 128-token budget alone ($0.00128) consumes the entire 1.3-credit reservation for a 10 s clip, leaving audio and transcript tokens unreserved. Every short dictation on a Pro model over-spends its reservation.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/lib/stt-models.ts`
Line: 157
Invariant: I1
Claim: The `gpt-4o-transcribe` reservation of `0.009` USD/min budgets, per its own comment, "~300 output tokens/min" of transcript, but no `max_tokens`-equivalent is sent to OpenAI and `computeOpenAITranscriptionCost` bills every returned output token at $10/M.
Failure scenario: A Whisper-family repetition loop (a known failure mode on music, silence, or looped audio) makes `gpt-4o-transcribe` emit thousands of output tokens for a short clip. A 30-second upload reserves (30/60) × $0.009 = $0.0045 ≈ 4.5 credits; a 5,000-token degenerate output bills $0.05 = **50 credits**. The user gets a garbage transcript and is charged (or the business absorbs) ~11x the reservation, with no server-side ceiling on the output tokens the reservation was sized against.
Confidence: low

### Coverage

**Examined buckets:**
- **B1 cloud-entry-and-auth** — `middleware/credits.ts` (the whole reservation/deduction surface: `estimateAudioSecondsFromSize`, `estimateCreditsFromSize`, `validateCredits`, `deductCredits`/`performDeduction`, `recordLicenseUsage`), `middleware/auth.ts` (`AuthContext.credits` provenance), `lib/constants.ts` (all size/rate constants), `index.ts` (route mounting — confirmed **no** body-limit middleware anywhere).
- **B2 cloud-routes** — all four billing routes read end to end: `transcribe.ts` (full `estimateCreditsForProviderFallbacks` + the fallback loop + the single deduction), `post-process.ts`, `assistant.ts`, `ws-streaming-deepgram.ts`. `usage.ts` read for reservation sites (none — it spends no provider money).
- **B5 cloud-billing-and-google** — `lib/cost-calculator.ts` in full (every `compute*Cost`, `creditsForCost`, `usdToCredits`, `estimatePromptInputReservationUsd`), `lib/stt-models.ts` in full (every `estimatedUsdPerMinute` entry cross-checked against its billing counterpart in cost-calculator).
- **B3 cloud-stt-providers** (targeted) — `assemblyai.ts` (sync-eligibility gate vs. the reservation's mirror of it), `gemini.ts` (thinking config, token derivation), `elevenlabs.ts` (keyterm surcharge gating), `providers/utils.ts` (`estimateSecondsFromBytes`).
- **B4 cloud-llm-providers** (targeted) — `lib/llm-provider.ts` (`retriesFor` consumers, `callWithRetry`, `LLM_PROVIDER_FALLBACKS`, model allowlists), `lib/llm-token-limits.ts`, `providers/anthropic.ts` (streaming cost resolution), `providers/groq-llm.ts` (`buildCorrectionRequest` — confirmed no `max_tokens` on any non-Anthropic provider).
- **B6 next-money-api** (targeted) — `app/api/license/credits/route.ts` POST path and `src/lib/db-layer.ts` `deductCreditBalance`, to establish where the overage lands: the SQL decrement is **floored at 0**, so every under-reservation becomes unrecoverable provider spend rather than a negative balance.

**Not examined / partially examined:**
- **B7, B8, B9 (except the credits route + db-layer deduction), B10, B11, B12** — no reservation or preflight-credit code path; the reservation lives entirely in `hyperwhisper-cloud`. Next.js is a pure deduct-and-floor sink, and I confirmed that at the one call site that matters.
- **B3** — I did not read all 11 STT adapters line by line; I read the four whose reservation math is non-trivial (assemblyai sync/async, gemini tokens, elevenlabs surcharge, openai token/duration split). The purely duration-billed adapters (`deepgram`, `groq`, `xai-stt`, `azure-mai`, `mistral`, `google-chirp`, `soniox`) were checked only via their `estimatedUsdPerMinute` ↔ `COST_PER_AUDIO_MINUTE` constant pairs, which match exactly. Their exposure to I1 is the shared bitrate-estimate issue (candidate 5), not a per-adapter rate mismatch.
- Test files (`*.test.ts`) were read for intent signals only, not audited.

**Leads refuted:**
- **"`assistant.ts` reserves `3.0 × countInlineImages()` but the multipart `image` file adds an image `countInlineImages` never counts."** Refuted. In `convertMessages` (assistant.ts:169-207) the multipart `imageBase64` is only ever attached *inside* a `p.type === 'image_url'` branch — it substitutes for an inline data URL, it is never appended as an extra block. A multipart image with zero `image_url` blocks in `messages` is read, base64-encoded, and then silently discarded (never forwarded to Anthropic). `imageCount` in `convertMessages` is therefore always ≤ `countInlineImages`, and both cap at `ASSISTANT_MAX_IMAGES`. The image-count arm of the reservation is sound; the real gap is the *unreserved text input and 8192-token output* (candidate 4).
- **"In `transcribe.ts`, cross-check `FALLBACK_CHAINS` against the `rates` array."** Refuted. `rates` is built by mapping over `FALLBACK_CHAINS[provider]` itself, so it structurally cannot miss a chain member, and `Math.max(...rates)` takes the most expensive hop. Each sibling is priced at `getProviderDef(p).defaultModel`, which is exactly what the attempt loop runs (`attemptModel = current === provider ? model : getProviderDef(current).defaultModel`, line 491). The `medical` add-on and the `domain` are both correctly scoped to the primary only, on both sides. The keyterm surcharge is correctly reserved for *any* eligible sibling (`elevenlabs`/`assemblyai`), not just the primary. `elevenlabsGeoBlocked` only ever *removes* a chain member after the reservation, which can only over-reserve.
- **"`estimatePromptInputReservationUsd` is applied only to the primary provider."** Refuted as a bug. Every token-billed provider (`gemini`, `openai`, `soniox`) has a self-only chain, and every cross-fallback sibling (`deepgram`, `groq`, `elevenlabs`) is duration-billed and returns 0 from that function. The comment's claim holds.
- **AssemblyAI sync-path reservation.** Refuted. `ASSEMBLYAI_SYNC_ESTIMATED_USD_PER_MINUTE` re-exports the same constant used for actual billing, and the reservation's eligibility test (`!medical && estimatedSeconds < SYNC_ELIGIBLE_ESTIMATED_SECONDS && hasExplicitLanguage`) is a strict *superset* of the adapter's gate (which additionally requires `isWavContentType`). The `MIN_ESTIMATED_SECONDS = 10` clamp in `estimateAudioSecondsFromSize` vs. the unclamped `estimateSecondsFromBytes` in the adapter cannot flip eligibility (10 < 100 either way). This one is correct in both directions.
- **ElevenLabs `scribe_v1` + `initial_prompt`.** Refuted. `elevenlabs.ts:73` gates `keyterms` on `modelId === 'scribe_v2'`, and `estimatedUsdPerMinute` gates the +20% on the same condition, so an explicit `scribe_v1` request neither reserves nor bills the surcharge.
