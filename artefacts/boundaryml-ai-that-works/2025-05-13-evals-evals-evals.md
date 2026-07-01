---
title: Evals, Evals, Evals #5
videoId: -N6MajRfqYw
url: https://www.youtube.com/watch?v=-N6MajRfqYw
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Evals are a journey you bootstrap from production, not a golden dataset you build up front.**
The whole talk hangs off this reframe: start by vibe evaling, ship with five evals, then grow the golden set from real traffic.
VERDICT: net-new video available.

**2. Deterministic runtime evals catch (and auto-correct) LLM errors with pure code, no model in the loop.**
Write invariants over structured output (quantity times price equals market value), then feed any delta back to re extract only the failing item.
VERDICT: net-new video available.

**3. Stop scoring with numbers; use categorical enums and structured LLM as judge.**
Numeric one to ten scores are arbitrary noise; categorical outputs plus keyword assertions make even fuzzy outputs like summaries evaluable.
VERDICT: next-step video available (complements Prompt Engineering structured-output).

## Summary

Vaibhav and Dex of BoundaryML build evals incrementally for LLM pipelines, moving from vibe evaling to golden datasets, deterministic runtime checks, and vibe coded visualizers.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1: Bootstrap evals from production, do not build a golden set up front

**The claim.** You go from no evals to some evals to good evals incrementally, harvesting your golden dataset from production rather than authoring it before you ship.

**Why it is non-obvious.** The instinct is that evals are a gate: spend six months building the perfect answer key, then unleash the pipeline. The speakers argue that is exactly backwards, and dangerous.

**Why it is true.** The hardest, most valuable AI problems are precisely the ones with no existing eval set, so waiting for one means never starting. Vaibhav points to HoloLens, where one and a half people spent two years and still only approximated a metric, there is no ground truth for most real problems. So the fast iteration loop, not the perfect metric, is what actually moves quality: vibe eval (hit play, read output), ship at five evals, capture every production input output pair, then convert real failures into golden cases.

**What it generalizes to.** This is the fake door test from product: ship the cheap signal, let reality tell you what to build. In agentic coding it maps to shipping a scrappy agent and hardening it against the failures users actually hit.

**How it goes wrong.** Knowingly shipping something you expect to break is reckless; and a golden set alone lies about accuracy unless you keep spot checking production to avoid overfitting to it.

### Spine 2: Deterministic runtime evals catch and auto-correct LLM errors with pure code

**The claim.** For structured output you do not need an LLM judge at all: encode invariants your data model must satisfy (quantity times price equals market value, column sums, row sums) and check them in deterministic code on live data.

**Why it is non-obvious.** People reach for a second LLM to grade the first one. The speakers insist that if you are asking a model to do math, you are wrong, code does it faster, cheaper, and with certainty.

**Why it is true.** It leans on probability. One field being wrong is common, but for the wrong quantity, wrong price, and a market value that still reconciles, all at once, is vanishingly unlikely, and summing across all rows to a matching total is more unlikely still. In the demo a bad Nvidia price surfaced as a twenty seven cent delta, and because the failure is localized you feed just that discrepancy back and ask the model to re extract only Nvidia, which it then gets right.

**What it generalizes to.** Any pipeline with internal consistency: extracted invoice line items, JSON schema cross field constraints, or an agent whose edits must still compile and pass a typecheck.

**How it goes wrong.** It only works where a real invariant exists; free text summaries have none, and a wrong but self consistent extraction can still slip through.

### Spine 3: Stop scoring with numbers, use categorical enums and structured LLM as judge

**The claim.** Never ask an LLM for a one to ten rating or confidence score. Make the judge return categorical enums (pacing slow, medium, fast), boolean assertions, and typed fields instead.

**Why it is non-obvious.** Number scores feel rigorous and sortable. In practice nobody, including the model, can say why a seven is not an eight, so the number is arbitrary discretion dressed up as a metric.

**Why it is true.** A category forces an explicit, describable meaning (like Yelp stars, below 4.8 just means bad). Once the judge outputs structured fields you can assert on them deterministically: pacing is not fast, biases array length is zero, cost is under five dollars, and for fuzzy text you assert that key phrases like React and Next.js must appear, sidestepping the impossibility of matching exact wording.

**What it generalizes to.** Any LLM as judge or classifier work: sentiment as an enum, intent detection as a fixed class set, code review verdicts as pass or blocking rather than a numeric quality score.

**How it goes wrong.** Categories with no defined meaning are as useless as numbers; and keyword assertions can be gamed by a model that name drops the term without real understanding.

## 🎬 Proposed ACS videos

### 1. Vibe Eval First: How To Go From Zero Evals To Good Evals

- HOOK: Everyone treats evals like a magic button; they are actually a journey you start with almost nothing.
- THE PROMISE: For engineers shipping AI features who feel paralyzed without a golden set, leave able to ship at five evals and grow the rest from production.
- THE SHAPE: (1) The magic button myth and why six months of upfront evals is dangerous. (2) Vibe evaling: hit play, read raw output, build intuition. (3) Ship at five evals, capture every production input output pair. (4) Turn real customer failures plus nearby weird cases into golden data. (5) Spot check production continuously so you do not overfit the golden set.
- SPINE: 1.
- SLOT: Techniques (new Evals chapter), or seed a standalone Evals mini class.
- RELATIONSHIP: ❌ net-new. The closest catalog cousin, filmed closing-the-loop, is about the coding agent verifying its own work, not about bootstrapping an eval suite for a shipped AI pipeline. No eval video exists in the inventory.
- PROOF TO REUSE: the HoloLens no ground truth story; "you should be vibe evaling in the beginning"; the twelve week mediocre prompt that a single customer complaint improved; the fake door test analogy.

### 2. Catch The LLM Lying: Deterministic Runtime Evals

- HOOK: The fastest, most reliable eval runs no model at all, it is just math on the output.
- THE PROMISE: For engineers extracting structured data, leave able to write code invariants that catch and auto-correct model errors on live production data.
- THE SHAPE: (1) Structured versus unstructured, and why structured output unlocks code checks. (2) Write the invariant: quantity times price equals market value, plus column and row sums. (3) The Nvidia twenty seven cent catch, why the law of probabilities makes this trustworthy. (4) Auto-correct: feed only the delta back and re extract just the failing item. (5) Do not make the LLM do math.
- SPINE: 2.
- SLOT: Techniques (Evals chapter), sits next to spine 1.
- RELATIONSHIP: ❌ net-new. Adjacent to backlog subagent-verification-loops and filmed closing-the-loop, but both concern an agent checking its coding work; neither teaches deterministic code invariants over extracted structured output plus targeted re extraction.
- PROOF TO REUSE: the finance extraction demo; "if you're doing this in the LM, you're wrong"; the 0.003 dollar price error resolving to exactly twenty seven cents; the Cambodia visa validation flow.

### 3. Stop Scoring 1 to 10: Categorical Evals And LLM As Judge

- HOOK: The single biggest eval mistake is asking a model to rate something out of ten.
- THE PROMISE: For anyone building an LLM judge, leave able to design categorical rubrics that produce stable, meaningful, assertable verdicts.
- THE SHAPE: (1) Why numeric scores are arbitrary, nobody defines seven versus eight. (2) Convert scores to categorical enums with explicit per category descriptions. (3) The lesson plan demo: pacing enum, biases array, cost boolean assertions. (4) For fuzzy text, assert key phrases must appear rather than matching exact wording. (5) Run the judge at runtime and flag entries users report bad.
- SPINE: 3.
- SLOT: Prompt Engineering, as the next video after structured-output.
- RELATIONSHIP: 🔗 complements Prompt Engineering structured-output. That video teaches how to make a model return typed, structured JSON; this one is the move after it, using categorical enums as your scoring rubric and asserting on them, applied specifically to evaluation and LLM as judge.
- PROOF TO REUSE: "categorical systems are generally way better than numerical systems because no one knows the difference between score seven and eight"; the Yelp 4.8 analogy; the lesson plan pacing, biases, and cost assertions.

### Also film-able (not deep-dived)

- **Integrated Tests Are A Scam, For AI Pipelines** — decompose the pipeline into typed steps and eval each in isolation with probes or mocking; apply the testing pyramid (many small step evals, few end to end). Net-new, slot Techniques. Proof: the "integrated tests are a scam" thread, JB Rainsberger's talk, the delta test tool that cut ninety percent of commits to five minutes.
- **Vibe Code Your Own Eval Dashboard In v0** — build a bespoke diff visualizer per JSON type in about an hour instead of buying an off the shelf eval tool. 🔗 complements Frontend Design and scrappy-copy-first. Proof: the Jupyter notebook analogy, the click through diff viewer built live, "bespoke UIs end up powering your team a lot more than you think."

## 📚 Full wisdom (reference)

**SUMMARY**
Vaibhav and Dex of BoundaryML build evals incrementally for LLM pipelines, moving from vibe evaling to golden datasets, deterministic runtime checks, and vibe coded visualizers.

**IDEAS**
- Teams treat evals like a magic button that will suddenly make broken AI pipelines start working.
- For most real problems there is no golden dataset and no true ground truth existing anywhere.
- HoloLens needed roughly one and a half people two years to only approximate a spatial metric.
- The hardest AI problems are exactly the ones where no appropriate eval set already exists today.
- Please stop asking an LLM to rate an answer one to ten or output confidence scores.
- Categorical enums like slow, medium, fast beat numeric scores nobody can consistently interpret between seven, eight.
- Vibe evaling means hitting play in the playground repeatedly and actually looking at the raw output.
- Evals are the fast iteration loop, and for forty engineers they function like CI unit tests.
- An answer key is a rubric: correct classes, extracted fields, expected intent, or target user sentiment.
- Table tests assert each output field separately and in parallel instead of failing everything at once.
- Probes surface intermediate pipeline state so tests assert internal steps, not only the final output string.
- Deterministic runtime evals verify production output with pure code, like quantity times price equals market value.
- A wrong Nvidia price was caught because the row math was off by twenty seven cents.
- Feed the exact discrepancy back and ask the LLM to re extract only the failing item.
- Evals live in a hybrid of your code and data, functioning fundamentally as a diffing mechanism.
- Vibe code a bespoke diff renderer in v0 in roughly an hour for your JSON type.
- Ship with just five evals, collect production data, then build golden datasets and diffing tooling afterward.
- Hand writing the golden JSON yourself forces you to find inconsistencies in your own data model.
- You cannot claim ninety eight percent accuracy without spot checking production and continuously extending the set.
- Different pipeline boxes each use different models: mini for intent, larger for SQL, reasoning for cypher.
- Integrated tests alone are a scam; follow the testing pyramid with many small granular units first.

**INSIGHTS**
- Evals are a journey from nothing to something to good, never a one time upfront deliverable.
- Building an eval set for six months before shipping risks perfecting a product nobody actually wanted.
- Structured extraction has clean answer keys; unstructured summaries need proxies like keyword presence, length, and counts.
- Deterministic invariants exploit probability: many correlated fields all being wrong yet still consistent is vanishingly unlikely.
- Numeric scores fail because nobody, including the model itself, defines what seven versus eight actually means.
- The real bottleneck is the golden dataset, not the harness that runs, scores, or visualizes results.
- Bespoke visualizers now beat off the shelf tools because v0 makes them an hour of work.
- Decomposing a pipeline into small typed steps makes each step independently and cheaply evaluable in isolation.
- Production traffic is the real source of golden data, harvested continuously from captured input output pairs.
- A cheap runtime LLM judge can correct itself when handed only the specific, narrowed failing subproblem.

**QUOTES**
- "evals feel like this magic button." (Vaibhav)
- "please stop using numbers to evaluate your systems." (Vaibhav)
- "you should be vibe evaling in the beginning if you haven't used a lot of LLM." (Vaibhav)
- "There is no golden data set ever for most real problems." (Vaibhav)
- "Evals are your way to iterate fast. Uh not initially but eventually." (Vaibhav)
- "everybody agrees that the hardest thing is getting the golden data set and getting the actual answer key correct." (Dex)
- "Evals are not purely living in your code because eval are purely a diffing mechanism." (Vaibhav)
- "categorical systems are generally way better than numerical systems because no one knows the difference between score seven and eight." (Vaibhav)
- "If you're doing this in the LM, you're wrong. Don't do that." (Vaibhav)
- "if you only have integration tests you are being scammed." (Dex)
- "spending six months on evals before you ship a product to somebody and like find out if they even want it is really dangerous." (Dex)
- "the number one thing you need to build a really good AI pipeline is a really fast iteration loop." (Vaibhav)

**HABITS**
- Vaibhav vibe evals first by hitting play in the BAML playground and directly inspecting raw output.
- He hand writes the golden JSON himself the first time to interrogate his own data model.
- He vibe codes a fresh bespoke renderer in v0 for every new JSON object he evaluates.
- For fewer than ten pairs he just compares the raw files manually rather than building UI.
- He iterates on the visualizer while it runs and simultaneously spot checks examples in the playground.
- The team adds every customer reported failure into the test suite alongside a few nearby cases.
- They prototype in v0 first, download it, then move the working renderer over into Cursor afterward.
- They save every production input output pair, because there is genuinely no shortcut around capturing them.

**FACTS**
- The HoloLens AR headset builds a 3D representation of the world using its onboard camera sensors.
- Windows and mirrors are barely captured by any depth sensor, badly breaking spatial ground truth reliability.
- Asking Llama 70B a question about fifty times can approach Llama 405B performance, per cited papers.
- GPT 4o mini sometimes regurgitates training set data rather than extracting the text actually present onscreen.
- At a hedge fund the full unit test suite once took over thirty hours to run.
- Their delta test tool meant that ninety percent of commits needed only five minutes of tests.
- The 0.003 dollar price error on Nvidia produced exactly a twenty seven cent market value delta.
- Some teams now run pipelines at ninety nine percent plus accuracy on hundred page plus PDFs.
- JB Rainsberger's conference talk Integrated Tests Are A Scam runs about one hour and five minutes.

**REFERENCES**
- BAML and BoundaryML (the hosts' tooling and company).
- "AI That Works" recurring podcast/workshop series.
- v0 by Vercel (for vibe coding bespoke visualizers).
- Cursor (editor used in the demo).
- Microsoft HoloLens (AR headset ground truth example).
- Face ID and D.E. Shaw (prior orgs where eval decisions differed).
- DSPy (consensus / judge plan reference).
- JB Rainsberger, "Integrated Tests Are A Scam" talk.
- Models named: GPT 4o mini, o3, Llama 70B and 405B, Claude Sonnet.
- Jupyter notebooks (visuals plus code analogy).
- pytest and uv (Python tooling in the live demo).
- Cambodia visa and financial statement extraction demos.
- Upcoming SF all day workshop, prior NY workshop.

**ONE-SENTENCE TAKEAWAY**
Bootstrap evals incrementally from production data, replacing numeric scores with categorical checks and deterministic invariants.

**RECOMMENDATIONS**
- Start by vibe evaling: hit play repeatedly, read raw outputs, build intuition before writing test cases.
- Ship with roughly five evals, then harvest production traffic to grow your golden dataset over time.
- Replace every one to ten score with a categorical enum that carries explicit descriptions per category.
- Add deterministic invariants over your structured output, like quantity times price equalling the extracted market value.
- When an invariant fails, feed the exact delta back and re extract only that failing item.
- Hand write your very first golden dataset yourself to expose hidden inconsistencies in the data model.
- Decompose pipelines into typed steps and eval the easiest steps first, using probes or mocking libraries.
- Vibe code a bespoke diff visualizer in v0 whenever you must review over one hundred pairs.
- Spot check production continuously and keep appending fresh, weird failing cases into your growing golden dataset.
- Watch JB Rainsberger's Integrated Tests Are A Scam talk and apply the testing pyramid to pipelines.
