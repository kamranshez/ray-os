I read all 11 STT adapters, `cost-calculator.ts`, and the billing tail of `transcribe.ts`. Five adapters violate I4; the five "present" leads all check out.

### Candidate
File: `hyperwhisper-cloud/src/providers/elevenlabs.ts`
Line: 193
Invariant: I4
Claim: `duration` is derived *only* from the last entry of `data.words[]` (`let duration = 0; if (data.words && data.words.length > 0) duration = lastWord.end;`) — there is no `duration`/`duration_seconds` field in the parsed response type at all and no `estimateSecondsFromBytes` fallback, so a non-empty `data.text` with an absent/empty `words` array reaches line 226 with `duration === 0`.
Failure scenario: A user transcribes a 30-minute recording via ElevenLabs Scribe. ElevenLabs returns `{text: "<full transcript>"}` without the `words` array (word timings are an opt-in-shaped field the request never explicitly asks for; `tag_audio_events:false` is the only formatting flag sent). `computeElevenLabsTranscriptionCost(0, …)` returns `$0`, `creditsForCost(0)` floors at `0.1`, and the user is deducted **0.1 credits for a transcription HyperWhisper is invoiced ~$0.30 (≈300 credits) for**. The client still receives the full transcript and `X-Total-Cost-Usd: 0.000000`. Repeatable on every request → unbounded free transcription.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/providers/azure-mai.ts`
Line: 208
Invariant: I4
Claim: `const durationSeconds = (data.durationMilliseconds || 0) / 1000;` — single-field derivation with a `|| 0` swallow and no byte-size fallback before `computeAzureMaiTranscriptionCost(durationSeconds)` at line 236.
Failure scenario: Azure Speech fast-transcription renames or drops `durationMilliseconds` (the field is API-version-pinned; earlier revisions of this API expressed duration as `duration` in ticks). Every subsequent Azure MAI transcription returns a full transcript from `combinedPhrases[0].text`, bills `$0`, and deducts the 0.1-credit floor. Because Azure MAI is also a fallback target, this is silently reachable even for users who never selected it — support sees hours of Azure spend against near-zero recorded revenue and no error anywhere in the logs (the `success` event logs `durationSeconds: 0` as if legitimate).
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/providers/xai-stt.ts`
Line: 147
Invariant: I4
Claim: `const duration = data.duration || data.words?.reduce(…max .end…) || 0;` — both sources are optional fields of xAI's *default* response shape; the request at lines 77-85 never sends `response_format` (or even `model`), so nothing forces xAI to return either field, and there is no `estimateSecondsFromBytes` fallback before `computeXaiTranscriptionCost(duration)` at line 177.
Failure scenario: xAI's STT endpoint returns its plain default body `{text: "…"}` (no `duration`, no `words`) — either today or the first time xAI changes its default verbosity. Grok STT is the most expensive duration-billed provider in the table at `$0.10/audio-hour`; an hour of audio costing $0.10 (100 credits) is deducted as 0.1 credits. Note this adapter is *more* exposed than `groq.ts`/`openai.ts`, which both explicitly request `verbose_json` to guarantee the duration field exists.
Confidence: high

### Candidate
File: `hyperwhisper-cloud/src/providers/deepgram.ts`
Line: 165
Invariant: I4
Claim: `const duration = data.metadata?.duration || 0;` — the optional-chained read collapses to `0` on any shape change, and `computeDeepgramTranscriptionCost(duration)` at line 193 is called with no guard and no byte fallback (contrast the sibling `assemblyai.ts:309`, which does guard).
Failure scenario: Deepgram omits or relocates `metadata.duration` (e.g. a response-shape change, or a `metadata` object trimmed by an edge proxy on a large body). The transcript is returned to the user, `costUsd` is `0`, and the deduction is the 0.1-credit floor. Deepgram is the default/first entry of the fallback chain for most requests, so this is the highest-volume path in the service — the whole fleet bills ~0 while Deepgram invoices $0.0055/min.
Confidence: medium

### Candidate
File: `hyperwhisper-cloud/src/providers/groq.ts`
Line: 124
Invariant: I4
Claim: `const duration = data.duration || 0;` with no `estimateSecondsFromBytes` fallback before `computeGroqTranscriptionCost(duration, model)` at line 155. Partially mitigated: `computeGroqTranscriptionCost` applies `Math.max(durationSeconds, GROQ_WHISPER_MIN_BILLABLE_SECONDS /* 10 */)`, so the charge floors at 10 s rather than 0 s — but that floor is a *rate-table minimum*, not an I4 guard, and it is orders of magnitude below the true cost for anything but a very short clip.
Failure scenario: Groq's `verbose_json` response drops the `duration` field (or a future default-format change makes `verbose_json` a no-op). A 60-minute transcription bills `(10/3600) × $0.04 = $0.000111` → 0.2 credits instead of ~40 credits, a ~200x under-charge on every Groq request. Unlike the other four this never bills literally zero, so it would not trip a "cost === 0" alert — it just quietly bills a flat 0.2 credits for all audio lengths.
Confidence: medium

### Coverage

**Examined buckets:**
- **B3 (cloud-stt-providers)** — complete. All 11 STT adapters read at their duration-derivation and `compute*TranscriptionCost` call sites: `assemblyai.ts` (both the sync path at 302-325 and the async path at 549-585), `azure-mai.ts`, `deepgram.ts`, `elevenlabs.ts`, `gemini.ts`, `google-chirp.ts`, `groq.ts`, `mistral.ts`, `openai.ts`, `soniox.ts`, `xai-stt.ts`. Plus `providers/utils.ts` (`estimateSecondsFromBytes`, line 26) and `providers/types.ts` (`TranscriptionResult.durationSeconds`).
- **B5 (cloud-billing-and-google)** — `lib/cost-calculator.ts` read end-to-end to classify duration-billed vs token-billed and to establish the downstream consequence: `creditsForCost(0)` returns the **0.1-credit floor**, so an I4 violation bills 0.1 credits, not literally 0. Worth flagging to the verifier: the map's "charged 0 credits" phrasing is slightly off — the user-visible number is 0.1, which makes the bug *harder* to spot in a ledger than a clean zero.
- **B2 (cloud-routes)** — partial, only the I4-relevant tail: `routes/transcribe.ts:676-720` confirms there is **no** post-adapter duration guard (`creditsForCost(result.costUsd)` is the sole conversion, and `result.durationSeconds` flows straight into the deduction metadata and the JSON `duration` field). Also checked `routes/ws-streaming-deepgram.ts` — it computes duration locally from streamed byte count via `durationSecondsForLinear16AudioBytes()` (line 91), which is structurally always positive, so it is not an I4 site.

**Not examined / partially examined:**
- **B1, B4, B6-B12** — no STT adapter or `durationSeconds` derivation lives in them (verified by a repo-wide grep for `durationSeconds`/`estimateSecondsFromBytes`, whose only hits are in `providers/` plus the three B2/B5 files above). Not a coverage gap for I4.
- **B2** examined only at the billing tail; the retry/fallback machinery was left to whoever owns I1/I12.

**Leads refuted:**
- None of the five "present" leads were wrong — all confirmed correct, and it's worth recording *why* each holds, since they are the reference implementations the five violators diverge from:
  - `assemblyai.ts:309` (sync) and `:554` (async) — both do `raw > 0 && Number.isFinite(raw) ? raw : estimateSecondsFromBytes(...)`.
  - `mistral.ts:140` — same guarded ternary.
  - `soniox.ts:295` — same, via a separate `billableSeconds` binding.
  - `openai.ts:141` — guards the whisper-1 (duration-billed) branch explicitly; the `gpt-4o-*` branch is token-billed and additionally has a per-minute *floor* inside `computeOpenAITranscriptionCost` (line 256-266), and its `durationSeconds` is already a byte estimate (line 129), so it is positive by construction.
  - `google-chirp.ts:252-266` — guards via its own `estimateAudioSeconds()`, which is content-type-aware and arguably the best implementation of the five.
- **`gemini.ts` — excluded, not a violation.** It is **token-billed**, not duration-billed: `computeGeminiTranscriptionCost` prices from `usageMetadata` tokens and never touches `durationSeconds`. Its `durationSeconds = audioInputTokens / AUDIO_TOKENS_PER_SECOND` (line 261) is telemetry only. It is nonetheless fail-closed on billing through two independent paths — `resolveAudioInputTokens`' last-resort byte estimate (line 145-147) and `computeGeminiTranscriptionCost`'s `fallbackDurationSeconds` branch (line 315-316) — so a missing `usageMetadata` cannot produce a $0 charge. Per the brief's "a provider that is not duration-billed cannot violate this invariant", I excluded it.
