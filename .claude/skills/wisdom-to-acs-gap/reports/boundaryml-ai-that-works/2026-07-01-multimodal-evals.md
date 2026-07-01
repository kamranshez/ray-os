---
title: Multimodal Evals
videoId: jzhVo0iAX_I
url: https://www.youtube.com/watch?v=jzhVo0iAX_I
date: 2026-07-01
status: posted
source: AI That Works (BoundaryML) with Kevin Gregory
---

## The one idea worth a video

**1. You can evaluate a multimodal extraction pipeline with zero labeled data by encoding the structural invariants you already know must hold (line items sum to subtotal, subtotal + tax + rounding = grand total, values are positive).** This is the reframe the whole episode hangs off: the build was "way easier than I thought" only because the eval design was substituted for a golden dataset.
VERDICT: net-new video available.

**2. Those same offline invariant checks become an online product feature: on a failed check, self-correct via retry or flag only that entry for a human, so you ship at 97% instead of chasing a perfect prompt.** The move that turns an eval harness into shippable reliability.
VERDICT: next-step (complement) video available.

**3. The build took three hours only because the data shape was designed first: extraction, eval-running, and visualization are three disjoint pipelines sharing one JSON contract, so any of them is swappable for free.** The architecture lesson underneath the speed.
VERDICT: net-new video available.

## Summary

Dexter and Vaibhav host Kevin Gregory on AI That Works, building a multimodal receipt-extraction pipeline and designing reliable evals without any golden labeled dataset upfront.

Counts: 2 net-new . 1 complement . 0 partial . 0 covered

## Deep dive

### Spine 1 - Invariant-based evals replace the golden dataset

**The claim.** You can measure a multimodal extraction pipeline's accuracy without hand-labeling anything, by turning properties you already know must be true into cheap binary checks.

**Why it's non-obvious.** The default assumption is that "you need a golden dataset" is step zero of any eval. Kevin explicitly rejects that: the Hugging Face metadata existed, but incorporating it "would have taken a lot longer," so he built proxies instead. Dexter names the trick: "You didn't have to do any hand labeling. You needed no golden data set."

**Why it's true.** A receipt is a closed arithmetic system: line items times quantity equal the amount, amounts sum to the subtotal, subtotal plus tax plus rounding equals the grand total. Because those relationships must hold regardless of the true values, a violated relationship localizes an extraction error without anyone knowing the "right" answer. So correctness gets inferred from internal consistency, not from a label.

**What it generalizes to.** Any domain with conservation laws or checksums: double-entry accounting, inventory reconciliation, order-total math in a checkout flow, physical-units sanity in sensor extraction.

**How it goes wrong.** Invariants are proxies, not truth. Two errors can cancel (a mis-signed discount) and pass a sum check; a "positive values" rule flags legitimately negative discounts. The escape is to escalate slowly toward a real golden set on the weird cases the proxies surface.

### Spine 2 - Turn the eval checks into an online self-correcting product

**The claim.** The invariant checks you wrote for offline evaluation are the same checks you should run at runtime inside the product, so you can ship well before 100% accuracy.

**Why it's non-obvious.** Most teams treat evals as an offline QA gate and keep tuning the prompt until it is "good enough" to launch. Vaibhav argues the opposite: "if you can only ship your product when it's perfect, you will lose the battle of shipping product."

**Why it's true.** At a 3% grand-total failure rate, the product is already valuable, because the user's real problem is that entering receipts by hand is miserable. So instead of raising accuracy, you build around the known failure rate. On a failed check you either feed the exact error back to the model ("your grand total is off by X, re-extract") and retry up to three times, or you flag that single entry in the UI and force the human to verify only the flagged fields. Either path yields a 100%-correct outcome from a 97%-correct model.

**What it generalizes to.** Any human-in-the-loop extraction product: expense tools like Brex or Concur, invoice parsing, medical-claim intake (Kevin's actual domain).

**How it goes wrong.** Retries burn latency and cost; a bad invariant can mask a real error or trigger infinite correction loops, which is why the retry budget is capped and the human is the final backstop.

### Spine 3 - Design the data shape first; keep the pipelines disjoint

**The claim.** The whole system took roughly three hours because the JSON data contract was designed up front; extraction, eval-running, and the Streamlit dashboard then share only that contract and nothing else.

**Why it's non-obvious.** The instinct is to write the extraction, then bolt on evals, then hack a viewer, coupling them as you go. Kevin's system has three pipelines "disjoint, they have no dependencies except the shared data model between them." The dashboard just reads JSON on disk.

**Why it's true.** When the contract (per image: extracted data, named eval pass or fails, model id, run id) is fixed first, each pipeline only has to honor the contract, so adding an eval is "effectively zero cost" and comparing GPT-4o against Gemini Flash is just another run written to the same shape. The upfront design is why the second project is fast: "most of the fundamentals are truly the same." As Dexter puts it, the writing of the code was never the hard part.

**What it generalizes to.** Any multi-stage AI pipeline: PII scrubbing, classification, RAG ingestion, where writing intermediate JSON per step lets you inspect, resume, and build golden sets from real outputs.

**How it goes wrong.** File-on-disk JSON does not scale to hundreds of millions of records; past some size you move the same contract into a queryable store (Parquet, LanceDB, a database) without changing the shape.

## Proposed ACS videos

### 1. Evals With No Answer Key: Grading AI When You Have No Labels
- HOOK: Everyone says you need a golden dataset before you can evaluate an AI pipeline. You don't.
- THE PROMISE: For engineers shipping extraction or classification features. After this you can measure accuracy on unlabeled data by encoding invariants you already know.
- THE SHAPE: (1) The trap of "we can't eval, we have no labels." (2) Find the invariants: sums, positivity, unit-price math. (3) Encode each as a binary pass-fail with a floating-point tolerance. (4) Build the pass-fail dashboard live on a small receipt slice. (5) Escalate the weird failures into a real golden set later.
- SPINE: 1
- SLOT: Techniques class > new "Evaluating AI Pipelines" chapter
- RELATIONSHIP: net-new. ACS has generator-evaluator, score-before-you-spend, and building-inner-and-outer-feedback-loops, but all evaluate an agent's CODE output or non-technical outcomes. None teaches invariant-based grading of an AI product's output with no ground truth.
- PROOF TO REUSE: "You needed no golden data set" (Dexter); the sum-validation and positive-values checks; the negative-discount case where two errors cancel and an absolute-value "fix" would break it.

### 2. Ship at 97%: Turning Eval Checks Into a Self-Correcting Product
- HOOK: Stop tuning the prompt to perfection. Wire your eval checks into the product and ship now.
- THE PROMISE: For builders stuck polishing accuracy before launch. After this you can ship below 100% by self-correcting failures and routing only the rest to a human.
- THE SHAPE: (1) Why a 3% failure rate is already shippable when the user's job is painful. (2) Reuse the offline invariant checks at runtime. (3) Feed the exact error back to the model and retry up to three times. (4) Flag only failed entries in the UI and force human verification of those. (5) The result: a 100%-correct outcome from a 97%-correct model.
- SPINE: 2
- SLOT: Techniques / loopy-ai class > Feedback Loops chapter
- RELATIONSHIP: complements "building-inner-and-outer-feedback-loops," which teaches closing the loop with real-world outcomes for non-deterministic work. This adds the specific move of promoting offline eval invariants into online runtime guards plus human-in-the-loop triage of only the flagged cases.
- PROOF TO REUSE: "If you can only ship your product when it's perfect, you will lose the battle of shipping product"; the retry-then-escalate ladder; the "force the user to check every flagged entry" UI pattern.

### 3. Design the Data Shape First: Three Disjoint Pipelines, One Contract
- HOOK: The reason a full eval system took three hours was decided before any code was written.
- THE PROMISE: For anyone building an AI pipeline. After this you can structure extraction, evaluation, and visualization so each is swappable at near-zero cost.
- THE SHAPE: (1) The coupling trap: extraction then bolt-on evals then a hacked viewer. (2) Design the JSON contract first (extracted data, named evals, model id, run id). (3) Build three pipelines that share only that contract. (4) Show that adding an eval or a new model is effectively free. (5) When JSON on disk stops scaling, move the same shape into Parquet or a database.
- SPINE: 3
- SLOT: Context Engineering class > new "Designing the Data Contract" chapter
- RELATIONSHIP: net-new, and it is the concrete AI-pipeline instance of the backlog "designing-interfaces" brief, which is unfilmed. No shipped ACS video teaches the data-contract-as-seam pattern for decoupling extraction, eval, and viz pipelines.
- PROOF TO REUSE: "They're both disjoint. They have no dependencies except the shared data model"; adding an eval is "effectively zero cost"; the three-hours-because-the-shape-was-designed-first story.

## Full wisdom (reference)

### SUMMARY
Dexter and Vaibhav host Kevin Gregory on AI That Works, building a multimodal receipt-extraction pipeline and designing reliable evals without any golden labeled dataset upfront.

### IDEAS
- Evaluate extraction accuracy using structural invariants you know must hold, needing no hand-labeled golden dataset whatsoever.
- Sum validation checks whether extracted line items plus taxes and rounding equal the printed grand total.
- The whole receipt eval pipeline, dashboard included, took roughly three or four hours to build entirely.
- Switching from GPT-4o to Gemini 2.5 Flash dramatically improved OCR extraction accuracy on the messy receipts.
- OCR loses structural semblance; angled photos force you to compute image normals just to recover spacing.
- Real-world receipts include grease stains, shadows, crinkles, foreign currencies, random discounts, and surprising sometimes-present restaurant taxes.
- Every eval is binary pass or fail, and adding another check costs effectively zero extra effort.
- A naive absolute-value fix on negative line items would break receipts where two errors correctly cancel.
- Failing checks are not always true failures; some negatives reflect genuine real-world discounts on the receipt.
- A floating-point tolerance is mandatory from day one for any summation eval comparing extracted monetary totals.
- Ship at ninety-seven percent by flagging failed checks and forcing users to verify only those entries.
- A runtime self-correcting loop feeds the grand-total error back, retrying three times before escalating to humans.
- Prompt optimizers overfit when your eval definitions are wrong, since messy data lacks a trustworthy objective.
- Extraction, eval-running, and visualization are three disjoint pipelines sharing only a single JSON receipt data contract.
- Writing JSON after each pipeline step lets a human inspect, resume, and test incremental parts independently.
- Escalating slowly from proxy invariants toward a real golden dataset beats hand-labeling everything from day one.
- The data model shape, not the prompt, is what code around the system actually depends on.

### INSIGHTS
- The problem was easy only because the system's decomposition mapped cleanly onto the eval design itself.
- Metrics are domain-specific and yours; anyone selling you a prepackaged eval metric is essentially scamming you.
- Evals resemble frontend: you buy the harness to run them, never the metric that defines correctness.
- Upfront design feels wasteful but makes every subsequent project far faster because fundamentals genuinely transfer across.
- Writing code was never the hard part; designing the system and building the theory always is.
- Under-optimizing your prompts leans into emergent model capabilities better than overfitting to one narrow specified objective.
- Like self-driving, the truly useful data is the weird edge case, not the clean common example.
- If you can only ship once it is perfect, you lose the battle of shipping product.
- Once you design tooling around a data shape, pointing another system at it costs almost nothing.
- Looking at raw data first surfaces hidden structure that no amount of clever prompting would reveal.

### QUOTES
- "It was only easy because the mechanism that Kevin used to break down the problem is what made it easy." - Dexter
- "The design of the design of the system mapped nicely onto the design of the evals because we had all that in mind from the start." - Vaibhav
- "You didn't have to do any hand labeling. You needed no golden data set." - Dexter
- "The writing of the code was never the hard part." - Dexter (quoting a comment)
- "Knowing how to design systems is going to be really really important." - Vaibhav
- "Anyone that's selling you a metric, it is scamming you because the metric is so domain specific." - Vaibhav
- "If you can only ship your product when it's perfect, you will lose the battle of shipping product." - Vaibhav
- "That data is completely useless to every self-driving car company out in the world." - Vaibhav
- "It's looking at your data and there's no real magic way around that that I found. You have to understand the problem." - Kevin
- "You have to just start building the system and build a system in such a way where it allows you to easily and quickly uncover these things." - Kevin
- "JSON was meant for humans. If machines are the only thing we cared about, we'd all use protobuff." - Vaibhav
- "Gemini Flash is seems to be the best at OCR." - Kevin

### HABITS
- Always look at the raw data first, scrolling random samples before writing any prompt or code.
- Start on a tiny slice, twenty-one receipts, before spending real money on larger LLM compute runs.
- Name each experimental run so the whole iteration journey stays visible and comparable across models later.
- Brainstorm candidate runtime evals with an LLM in Cursor before committing to any final eval design.
- Write intermediate JSON to disk after each step so results are inspectable and resumable by hand.
- Keep the eval metric and the system in-house; only ever outsource the harness that runs them.
- Add exponential retry logic whenever the model returns intermittent extraction failures on some of the inputs.
- Iterate the data model and the prompt together, adding fields like rounding and discount when discovered.

### FACTS
- The CORD dataset is a Hugging Face receipt dataset commonly used for OCR receipt extraction benchmarks.
- The receipts in this dataset are Indonesian, using comma and decimal conventions different from American formatting.
- CVS receipts can run roughly thirty feet long, far exceeding dimensions LLMs typically expect for images.
- Kevin ran three hundred fifty receipts total in the final dashboard, up from an initial hundred.
- The Hugging Face dataset includes metadata containing actual amounts, but with quirks hard to incorporate directly.
- Gas stations historically priced fuel in fractions of a penny, an example of unexpected rounding behavior.
- Kevin works as an ML engineer at Evolution IQ, building claims-guidance software for large insurance companies.
- Gemini 3 produced many extraction failures during a late-night test, unexpectedly worse than Gemini 2.5 Flash.
- The PB1 restaurant tax appears only sometimes and does not always get added to the total.

### REFERENCES
AI That Works podcast (BoundaryML); BAML; CORD receipt dataset on Hugging Face; Streamlit; Cursor; GPT-4o; Claude Sonnet; Gemini 2.5 Flash; Gemini 3; DSPy / GEPA prompt optimizers; Parquet; LanceDB; MongoDB; Amazon S3; protobuf; 12-factor agents and context engineering; Evolution IQ; Brex / Concur receipt tools; Vercel preview URLs; Tailscale; Brian's decaying-resolution memory (prior episode); Kevin's prior large-scale classification-pipeline episode.

### ONE-SENTENCE TAKEAWAY
Design your evals from structural invariants you already know, and skip the golden dataset entirely.

### RECOMMENDATIONS
- Before coding anything, download your dataset and scroll random samples to discover its hidden structure first.
- List the invariants that must be true, then encode each as a cheap binary pass-fail check.
- Keep extraction, evaluation, and visualization as separate pipelines joined only by one shared JSON data contract.
- Write each pipeline step's output to JSON so you can inspect, resume, and test it incrementally.
- Add floating-point tolerance to every monetary summation check from day one to avoid spurious eval failures.
- Turn offline eval checks into online runtime guards that self-correct or escalate flagged cases to humans.
- Ship below a hundred percent, flagging only failing entries for human verification instead of every one.
- Point Claude Code at Kevin's repo to bootstrap a similar eval system for your own pipeline.
- Delay prompt optimizers until your eval definitions are trustworthy; otherwise they overfit to the wrong objectives.
