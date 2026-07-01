---
title: Anthropic Post Mortem #26
videoId: bLx-UlRTiEw
url: https://www.youtube.com/watch?v=bLx-UlRTiEw
channel: BoundaryML (AI That Works)
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine A. Use the least context that fully represents your problem, because a bigger context window trades accuracy for capacity and is never free.**
Why: this is the reframe the whole first half hangs off, and it explains the routing bug, the RoPE-scaling tangent, and the "TLDR use less context" closer.
VERDICT: 🔗 next-step video available (complements the shipped "1M Context Window" video by supplying the mechanism it omits).

**Spine B. Model quality degrades silently, so you need a lossy out-of-band signal to notice it and a rollback-first loop to localize whether the fault is infra, prompt, or model.**
Why: it subsumes the Twitter-sentiment canary, "observability is more important than before," the AWS "don't be a hero, roll back" slogan, and "swap the model to eliminate a variable."
VERDICT: ❌ net-new video available.

**Spine C. Eval quality is coverage, not count: harvest real production data into a rolling eval set that spans your users' behavior distribution.**
Why: it ties together "the magic number is 30," "evals that span the distribution," the Face ID Phoenix story, and "ship data to prod and turn a subset into evals forever."
VERDICT: 🔗 next-step video available (complements the scripted "Building Inner and Outer Feedback Loops").

---

# Summary + counts

BoundaryML's Vaibhav and Aaron dissect Anthropic's outage post-mortem, then OpenAI's AgentKit, extracting lessons on context minimization, silent-regression observability, rollback-first debugging, distribution-spanning evals, and agent-builder limits.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine A. Use the least context that represents the problem

The claim: the least context that fully represents a problem, not the largest available window, produces the most accurate output. It is non-obvious because the default advice is "toss everything at the biggest million-token model at all times," and Vaibhav says flatly that this "is not always going to lead to good results." The mechanism has two steps. First, a transformer works by bridging information between token vectors in both directions until each vector "represents something meaningful"; as the window grows, the model must learn to move information across far more channels, and "it's not the same as learning what it means to move across 10 tokens versus moving across a million tokens." Second, stretching a trained window uses RoPE scaling, which squeezes position encodings into fractional slots (1, 1.5, 2, 2.5) and adds precision loss, so a smaller encoding space can represent a tersely-stated problem with less loss. Anthropic's own routing bug proved it: sending small requests to the million-context variant degraded them. This generalizes cleanly to RAG, where stuffing fifty chunks instead of the five relevant ones hurts retrieval quality. It goes wrong if you read it as "make context artificially tiny"; the rule is the least context that still represents the problem, not starvation.

## Spine B. Detect silent regressions, then roll back before diagnosing

The claim: model failures are silent, so you need a noisy out-of-band signal to detect a regression and a rollback-first loop to localize it. It is non-obvious because engineers trained on distributed systems expect loud failures: "when you do an HTTP request anywhere, you should expect it to fail," so you wrap it in a try/catch and move on. Model degradation ships no exception. Anthropic saw only a small fraction of traffic affected yet "30% of Claude Code users" felt it, and "sometimes the model did get worse, it's not in your head." The mechanism is elimination under uncertainty. Because the failure is silent, you first need an external canary (Anthropic scans Twitter sentiment; Aaron watched AWS mentions), and once it fires the fastest way to isolate cause is the AWS golden rule, "don't be a hero, roll back." If the issue survives rollback it is not your deploy, so you swap model providers to test whether it is the model. This orders cheap reversible moves before expensive diagnosis. It generalizes to any shipped coding agent or skill that quietly regresses. It goes wrong when the vibe signal is trusted alone: it is lossy and cannot localize by itself, and small teams should not instrument the whole pipeline, only the critical parts.

## Spine C. Evals must span the distribution, harvested from prod

The claim: eval quality is coverage of the real behavior distribution, not raw sample count. It is non-obvious because teams chase "more evals" or a golden hundred test cases, believing quantity plus a good/bad label is "the promised land." Vaibhav pushes back: most problems have no crisp good/bad, and "you need evals that span the distribution of the behavior your users have," so "quantity isn't the thing." The mechanism: failures cluster in unrepresented regions of input space, so a set that misses your distribution cannot catch them no matter how large. His Face ID example makes it physical: the system "worked worse in Phoenix" because extreme heat expanded the camera materials and broke stored calibration, a failure you only catch with data spanning that condition. The remedy is the only durable one: "ship data to prod, collect that data, turn a subset into an eval data set," and treat it as rolling, "a thing that you do forever." This generalizes to evaluating a coding subagent by collecting the real repo tasks it failed on rather than synthetic ones. It goes wrong when "the magic number is 30" is read as a coverage target rather than a signal floor, and when harvested prod data carries selection bias.

---

# 🎬 Proposed ACS videos

## 1. How to tell if the model actually got dumber (and what to do about it)

HOOK: Your users say the AI "feels worse." There is no error in your logs. Anthropic just published exactly how this happens, and how they catch it.
THE PROMISE: For anyone shipping an LLM feature, a repeatable way to detect a silent quality regression and localize it to infra, prompt, or model within minutes.
THE SHAPE:
1. Why model failures are silent: no 500, well-formed output, quietly worse (contrast with distributed-systems try/catch instinct).
2. Build a lossy canary: a cheap out-of-band signal (thumbs up/down, sentiment, a business proxy) that fires on anomalies.
3. The rollback-first runbook: "don't be a hero, roll back" to eliminate your deploy as a variable.
4. If it survives rollback, swap the model provider to test model vs prompt; only then prompt-engineer.
5. Scope it for small teams: instrument the critical path, not the whole pipeline.
SPINE: B.
SLOT: Loopy AI class, Command and Control chapter (or a new "Running AI in Production" chapter).
RELATIONSHIP: ❌ net-new. The closest neighbor, "Regression Guards" in Builder and Verifier, freezes a green test set and halts a build loop when something goes red at build time. This video is runtime: detecting drift in a deployed model you do not control, then triaging infra vs prompt vs model and rolling back. Different demo, different layer.
PROOF TO REUSE: "with these models the failure is so subtle that we need new mechanisms to observe these failures"; the AWS slogan "Don't be a hero. Roll back."; "if you roll back and it's still broken, you've already eliminated one variable."

## 2. Stop maxing out your context window

HOOK: Everyone tells you to dump everything into the biggest model. Anthropic's own outage shows why that quietly makes your output worse.
THE PROMISE: For agentic-coding users, an intuition for why a smaller, tighter context often beats a full million tokens, and how to decide how much to load.
THE SHAPE:
1. The default myth: "toss everything at the biggest model at all times."
2. The mechanism in plain English: transformers bridge information between token vectors; more channels means harder, lossier movement.
3. RoPE scaling on a whiteboard: squeezing positions into fractional slots trades precision for reach.
4. The rule: use the least context that represents the problem, not artificially tiny, just no filler.
5. Applied to Claude Code: bloated CLAUDE.md and stale history as the everyday version of this bug.
SPINE: A.
RELATIONSHIP: 🔗 complements "1M Context Window". That video already teaches the workflow ("1M context is intake bandwidth, not working memory: wide ingest, distill into artifacts, execute in smaller windows"), so do not re-teach the intake pattern. This video adds the missing mechanism, WHY accuracy actively degrades in a large window, plus the counter-claim that bigger is a real accuracy trade-off, not just working-memory hygiene.
SLOT: Context Engineering class (sits next to the 1M Context Window video as its "why" companion).
PROOF TO REUSE: "just use less context and less context, I promise you your pipelines will be more accurate"; "the least possible way to represent your problem is the best way to represent it"; the Aaron-with-nonsense-information analogy for wasted processing.

## 3. Your evals are useless if they don't span the distribution

HOOK: You have a hundred test cases and your AI still broke in prod. The number of evals was never the point.
THE PROMISE: For anyone building an AI pipeline, a method to build an eval set that actually catches failures by covering how real users behave, not by being big.
THE SHAPE:
1. Kill the myth: "the promised land" of a big labeled set, and why most problems have no crisp good/bad.
2. Coverage over count: failures hide in unrepresented regions; the Face ID Phoenix story as the vivid proof.
3. The rolling harvest: ship to prod, collect real data, promote a subset into evals, repeat forever.
4. "The magic number is 30" as a signal floor, not a coverage target.
5. Applied to coding agents: build evals from the real repo tasks your subagent failed, not synthetic ones.
SPINE: C.
RELATIONSHIP: 🔗 complements "Building Inner and Outer Feedback Loops". That video teaches connecting real-world outcomes back into the process so future runs improve; do not re-teach the feedback-loop concept. This video adds the composition rule for the eval set itself: it must span the user-behavior distribution or it catches nothing, and it is a continuous harvest rather than a one-time build.
SLOT: Advanced Techniques class (sits beside "Building Inner and Outer Feedback Loops"); overlaps Prompt Engineering.
PROOF TO REUSE: "you need evals that span the distribution of the behavior your users have"; "ship data to prod, collect that data, turn a subset into an eval data set, that is the only answer... it's a thing that you do forever"; "a lot of things work worse in Phoenix."

## Also film-able (not deep-dived)

- **The wall every no-code agent builder hits.** Drag-and-drop agent builders (OpenAI AgentKit, 11 Labs, n8n) feel magical until you need schemas, type safety, and reusable functions, at which point "I'm basically writing code in the UI builder." One-sentence pitch: why structured outputs and typed contracts are the real product, and where visual builders stop scaling (past roughly 10-15 nodes). Rough slot: Prompt Engineering (structured-output foundation) or a Business-class "when to use no-code" video. Likely 🔗 complement to the structured-output foundation brief.

---

# 📚 Full wisdom (reference)

## SUMMARY
BoundaryML's Vaibhav and Aaron dissect Anthropic's outage post-mortem, then OpenAI's AgentKit, extracting lessons on context minimization, silent-regression observability, rollback-first debugging, distribution-spanning evals, and agent-builder limits.

## IDEAS
- Anthropic routing small requests to their million-token context variant degraded quality, proving bigger windows aren't better.
- Transformers bridge information between token vectors bidirectionally, so longer context means learning harder cross-channel information movement.
- RoPE scaling squeezes position encodings into fractional slots, stretching trained windows while adding real precision loss.
- Anthropic scans Twitter sentiment, not formal evals, to detect when a newly released model behaves anomalously.
- Output-corruption bug randomly assigned high probabilities to tokens, producing nonsense that detection heuristics can catch easily.
- A TPU compiler sometimes optimized sixteen-bit float operations to thirty-two-bit inconsistently, flipping close token probability comparisons.
- Floating-point multiplication is order-dependent, so a times b times c need not equal the reversed order.
- Anthropic chops the probability distribution at cumulative sum 0.99, discarding the remaining tail before sampling tokens.
- Distributed sampling splits the vocabulary across machines, so each proposes candidates before a central max pick.
- The bug dropped the true global top token from candidate arrays, so sampling silently missed it.
- Model failures are silent, unlike distributed-systems failures where an HTTP request loudly returns a 500 error.
- AWS golden rule don't be a hero and just roll back instantly isolates the deployment variable.
- After rolling back, if the issue persists it is model or infrastructure, not your recent deploy.
- Anthropic serves models across AWS Trainium, Amazon Bedrock, and Google Cloud Vertex, squeezing every performance optimization.
- Hyper-optimized assembly and SIMD code becomes write once, read never, worse than read-only because entirely unreadable.
- Anthropic abandoned some performance optimizations entirely, deciding output quality mattered more than shaving raw inference cost.
- Face ID performed worse in Phoenix because extreme heat expanded camera materials and broke stored calibration.
- Good evals require spanning the full user-behavior distribution, not merely accumulating a large raw sample count.
- OpenAI's AgentKit drag-and-drop interface breaks down once you actually need schemas, type safety, and reusable functions.
- Adding an integration node feels magical until specific folder names force you to write code again.
- Inference is becoming commodity; value now lies in how the model composes with your existing stack.
- OpenAI's responses API and model-specific tools quietly entrench you into that single provider's ecosystem lock-in mode.

## INSIGHTS
- The least context that represents a problem, not the largest window, yields the most accurate output.
- Because model failures are silent and subtle, observability matters more here than in classic loud-failure systems.
- Rolling back first turns a confusing multi-variable outage into a clean, fast single-variable elimination step immediately.
- A noisy lossy signal detects regressions, but alone cannot localize these infrastructure, prompt, or model faults.
- Eval coverage beats eval quantity; thirty representative cases can outperform hundreds sampled from one narrow region.
- Evals are a rolling practice: harvest production data into test sets forever, never as one-time work.
- No-code agent builders quietly reintroduce every hard software problem: schemas, type safety, functions, composition, and readability.
- Provider modes like responses API create lock-in exactly as cloud-specific services made Terraform portability only aspirational.
- Define hallucination concretely per product, since strictly every ungrounded generation technically already qualifies as a hallucination.

## QUOTES
- "just use less context and less context. I promise you your pipelines will be more accurate" (Vaibhav)
- "the least possible way to represent your problem is the best way to represent it" (Vaibhav)
- "Don't be a hero. Roll back." (Aaron, on the AWS golden rule)
- "we're all building these systems on top of systems that we have even less control over in any previous way we've had" (Vaibhav)
- "with these models the failure is like so subtle that we need new mechanisms to observe these failures and so observability is even more important than before" (Aaron)
- "The magic number is 30." (Vaibhav)
- "you need evals that span the distribution of the behavior your users have" (Vaibhav)
- "sometimes the model did get worse. Sometimes it's not in your head and it did get worse" (Vaibhav)
- "a lot of things work worse in Phoenix" (Vaibhav, on Face ID calibration)
- "oh shoot I'm basically writing code in the UI builder" (Vaibhav, on agent builders)
- "the inference part is probably the least interesting and unique part now of building most pipelines" (Vaibhav)
- "it's the golden rule at AWS... you don't deploy worldwide at the same time" (Aaron)

## HABITS
- When Claude's output degrades, they swap to a different model or provider before touching the prompt.
- They tag coding bots like Cursor and Claude in Slack with random tickets, burning tokens speculatively.
- They merge bot-generated pull requests only after reading the code, trashing the ones that fail outright.
- Aaron writes a markdown plan, reviews it together, then codes, redoing the whole thing if unsatisfied.
- VB does the minimum process necessary, skipping heavy design docs when the right answer is obvious.
- They deploy slowly using feature flags and instant rollback, never shipping worldwide all at once immediately.
- Aaron codes daily with Claude Sonnet 4.5, falling back to Codex CLI only for tricky problems.
- They collect production data continuously and promote a subset into a constantly-updated always-growing rolling eval set.
- When quality drops they roll back first, then only diagnose infrastructure, prompt, or model calmly afterward.

## FACTS
- Anthropic's post-mortem attributed recent quality regressions to three distinct, independent bugs across their entire serving infrastructure.
- Roughly thirty percent of Claude Code users were directly affected by one of the quality regressions.
- The hosts cite roughly eight percent of traffic impacted, making the regression genuinely hard to detect.
- A December 2024 Anthropic bug sometimes prevented the highest-probability top token from ever being chosen correctly.
- A TPU compiler intermittently promoted sixteen-bit float math to thirty-two-bit precision, without any consistent documented rule.
- Anthropic keeps only tokens whose cumulative probability reaches 0.99, then discards all remaining low-probability tail tokens.
- Google's Face ID performed worse in Phoenix because heat distorted camera calibration through physical material expansion.
- OpenAI reportedly built AgentKit in six weeks using Codex, claiming no lasting competitive moat exists yet.
- Thinking Machines published a paper attributing non-determinism partly to GPU batch processing, beyond just floating-point arithmetic.

## REFERENCES
- Anthropic engineering post-mortem on recent model quality regressions (three bugs, serving across multiple providers).
- Thinking Machines paper on non-determinism in LLM inference (batch processing on GPU; shared by "AJ").
- OpenAI AgentKit / agent builder and prompt optimizers; 11 Labs agent builder; n8n; Zapier; Lovable.
- BAML (BoundaryML) dynamic types and dynamic runtime; RoPE scaling; top-p sampling; temperature.
- AWS EC2, Prime Video, Amazon Bedrock, Trainium; Google Cloud Vertex AI; Google Face ID.
- Claude Sonnet 4.5; Codex CLI; GPT ("GD5"); Cursor; Vercel one-click rollback; Terraform; AWS CDK.
- "AI That Works" show (Tuesdays 10am PST), hosts Vaibhav, Aaron, and Dexter, by BoundaryML.

## ONE-SENTENCE TAKEAWAY
Understand your stack deeply, use minimal context, detect silent regressions, and roll back before diagnosing.

## RECOMMENDATIONS
- Use the least context that fully represents your problem, not simply the largest available context window.
- Build a lossy, noisy product-quality signal to detect silent model regressions early, before frustrated customers churn.
- When quality drops, roll back first to eliminate your own deployment as a possible immediate cause.
- Swap to another model provider to test whether the failure is model or your own prompt.
- Harvest real production data continuously and promote a representative subset into your own rolling eval set.
- Unit-test only the most critical parts of your pipeline, never the entire pipeline slowly and exhaustively.
- Prefer feature flags and instant one-click rollback tools like Vercel over risky simultaneous worldwide production deployments.
- Add thumbs up and thumbs down feedback so your unhappiest users surface quality drops very fast.
- Define hallucination concretely for your product instead of using it as a vague single catch-all term.
- Verify structured extractions programmatically, checking whether line items actually sum, to reliably catch obvious numeric hallucinations.
- Read the RoPE scaling literature to understand why larger windows trade accuracy for raw sheer capacity.
- Build a fast introspection tool that quickly triages infrastructure versus prompt versus model failures within minutes.
