---
title: "Evals: How to compare models #16"
videoId: OawyQOrlubM
url: https://www.youtube.com/watch?v=OawyQOrlubM
date: 2026-07-01
status: posted
source: BoundaryML / "AI That Works" (Vaibhav, BAML) + Dex (HumanLayer)
---

## The one idea worth a video

**1. The eval IS a vibe-coded, throwaway, domain-specific dashboard.** The fastest and most reliable way to compare models on a real task is to vibe-code a bespoke UI that renders each model's output side by side, not to reach for an automated LLM-as-judge or a generic eval platform.
VERDICT: net-new video available.

**2. Define "accuracy" for your business before you evaluate, and don't swap a working model without a reason.** "Accuracy" is an overloaded stand-in for quality whose meaning is set entirely by the product, so you cannot eval, or justify switching, until you name what good means for your specific use case.
VERDICT: next-step (complement) video available.

**3. Onboard every new model by pushing it to its limit first.** When a model ships, suspend your assumptions about what models cannot do and probe its ceiling with 20 to 30 loose, ambiguous prompts before you run any task-specific eval.
VERDICT: net-new video available.

---

## Summary + counts

Vaibhav (BAML) and Dex (HumanLayer) discuss when to switch AI models and vibe-code a bespoke Streamlit dashboard comparing model outputs side-by-side for one email-generation prompt.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: The eval is a vibe-coded, bespoke comparison dashboard

**The claim:** the fastest, most reliable way to compare models on a fuzzy task is to vibe-code a throwaway, domain-specific dashboard that renders each model's output side by side, not to reach for an automated LLM-as-judge or a polished eval SaaS. **Why it is non-obvious:** teams assume rigorous evaluation means automated scoring or buying a platform. Vaibhav argues the opposite for a task like "write a good marketing email," you do not yet know what good means, so any automated score measures the wrong thing. **The mechanism:** because "accuracy" is undefined, an LLM judge inherits the same ambiguity and adds stochastic error (every extra pipeline step injects uncertainty), whereas a human glances at two rendered emails and instantly sees "this one dropped the next-session bullet, that one is a giant blob." Rendering output in its native shape converts evaluation from slow reading into fast pattern-matching, so the UI itself is the leverage. **What it generalizes to:** any bespoke internal tool, for example a bounding-box viewer for a vision model, or an A/B diff viewer for RAG answers. **How it goes wrong:** for a truly generic use case, dedicated tools beat an hour-long build; and if you never define what good is, the dashboard just relocates the ambiguity instead of resolving it.

### Spine 2: Define accuracy for your business before you evaluate

**The claim:** before evaluating or switching models, define what "accuracy" means for your specific business problem, and if the current system works with no business pressure, do not switch at all. **Why it is non-obvious:** the industry reflex is "new model dropped, upgrade everything." Vaibhav and Dex argue a working model is a "known enemy" and that switching prompts costs nearly as much engineering time as building a feature, so the default should be inertia. **The mechanism:** "accuracy" is an overloaded stand-in for quality whose meaning is set entirely by the use case. The "hello first name" example shows it: while a human pastes the email into Loops, a missing merge field is harmless; the moment delivery is automated, that same field becomes a hard correctness constraint. The metric is a property of your product, not of the model, so you cannot eval until you name it. **What it generalizes to:** choosing any dependency, a database or a vendor API, against business SLAs rather than raw benchmarks. **How it goes wrong:** over-inertia can make you miss a genuine step-function upgrade, like GPT-4o-mini's order-of-magnitude latency win or DeepSeek opening open-source use cases that were not possible before.

### Spine 3: Push a new model to its limit to build intuition

**The claim:** when a new model ships, deliberately suspend your assumptions about what models cannot do and probe its ceiling with 20 to 30 short, intentionally ambiguous prompts before running any task-specific eval. **Why it is non-obvious:** engineers carry a frozen mental model (still reasoning from GPT-3.5 and GPT-4 limits) and under-ask new models, so they never discover new capabilities. **The mechanism:** capabilities are emergent and cannot be pre-specified; the old behavior-driven "given/when/then" spec breaks because you cannot write a spec for behavior you have not seen. By running many loose prompts you surface what the model can now do, then you back into features and bake evals around the discovered behavior (Ben Stein's inversion of behavior-driven development). It also means testing the harness, not just the prompt: can the model do multi-turn tool calling inside a Claude-Code-style loop, not just one-shot completion. **What it generalizes to:** onboarding any powerful new tool through exploratory play before committing to it in production. **How it goes wrong:** pure vibe-checking that never gets formalized into evals leaves you with anecdotes; and probing burns time and tokens, so it is a ritual for major releases, not every point update.

---

## 🎬 Proposed ACS videos

### 1. Vibe Eval: Build a Model Comparison Dashboard in Under an Hour
- **HOOK:** New model dropped. Instead of trusting a leaderboard, build the eval tool that tells you if it is better for YOUR task, live, in one sitting.
- **THE PROMISE:** For anyone shipping an LLM feature. After this you can vibe-code a throwaway side-by-side dashboard that renders your real outputs and lets you pick the better model at a glance.
- **THE SHAPE:** (1) One prompt, one test case, drop in a cheap model to confirm a gut instinct. (2) Store test cases as JSON, loop models x tests async, wrap each unit in try/except so outages never crash the run. (3) Vibe-code a Streamlit app that renders outputs as real emails, not JSON. (4) Add side-by-side dropdowns and a regex detector that highlights em-dashes and AI tells. (5) Change the prompt, rerun, compare versions and models together.
- **SPINE:** 1.
- **SLOT:** Techniques class, new "Evals / comparing models" chapter.
- **RELATIONSHIP:** ❌ net-new. Nothing in ACS covers building an eval or model-comparison harness; the nearest video, "closing-the-loop" (Techniques, filmed), builds a feedback signal for the AGENT to self-correct, whereas this builds a feedback signal for the HUMAN to compare models, so it does not re-teach it.
- **PROOF TO REUSE:** "90% of the job is getting the data in the right shape so you can make the right decisions." The shadcn analogy: scaffold a best-practice base, then customize everything. "JSON files are garbage" so render outputs in their native shape.

### 2. Don't Swap the Model: Define Accuracy Before You Evaluate
- **HOOK:** Everyone rushes to the newest model. The pros ask a harder question first: what does "accuracy" even mean for my product, and is switching worth it at all?
- **THE PROMISE:** For engineers and AI PMs. After this you can write a concrete definition of accuracy for your use case and make a defensible switch-or-stay decision instead of chasing benchmarks.
- **THE SHAPE:** (1) "Known enemy vs unknown enemy": why a working model beats a new one by default. (2) Accuracy as a new dimension alongside latency, cost, uptime, security. (3) The "hello first name" case: how automating delivery flips a nice-to-have into a hard constraint. (4) No infinite optimum: without user criteria, "make it better" is meaningless. (5) The exceptions worth switching for (latency step-functions, open-source unlocks).
- **SPINE:** 2.
- **SLOT:** Techniques class, model-selection / decision-making chapter (pairs with Start Here).
- **RELATIONSHIP:** 🔗 complements "scaling-taste" (Techniques, filmed) by being its next step. "scaling-taste" already teaches that taste and knowing what good looks like is the moat; this adds the decision layer on top: how to convert that taste into a per-use-case definition of accuracy and a switch-or-stay call, which scaling-taste does not cover.
- **PROOF TO REUSE:** "Can you imagine if your REST API failed on 20% of requests?" "Switching prompts takes almost as much time as writing a new feature." The Loops "hello first name" automation example.

### 3. Push the Model to Its Limit: A Ritual for Every New Release
- **HOOK:** You are probably under-asking every new model, because your brain is still stuck on what GPT-4 couldn't do. Here is the ritual that fixes it.
- **THE PROMISE:** For anyone who feels behind on model releases. After this you have a repeatable 30-minute ritual to discover what a new model can actually do before you commit to it.
- **THE SHAPE:** (1) Turn off your prior assumptions about model limits on purpose. (2) Run 20 to 30 short, intentionally ambiguous prompts and vibe-check the spread. (3) Test the harness, not just the prompt: multi-turn tool calling inside a Claude-Code-style loop, not one-shot. (4) Emergent-capability inversion: play first, then bake evals around what you discovered (Ben Stein). (5) Only then run the task-specific eval from video 1.
- **SPINE:** 3.
- **SLOT:** Techniques class, working-with-new-models chapter.
- **RELATIONSHIP:** ❌ net-new. "just-run-it-again" (Techniques, filmed) and the backlog "stochastic-consensus-and-fan-out-fan-in" cover running the SAME task repeatedly for consensus; this is a distinct move, probing a NEW model's capability ceiling with deliberately loose prompts to build intuition, which ACS does not teach.
- **PROOF TO REUSE:** "I try and flip the switch in my brain... and just turn it off... otherwise I won't ask the model to do enough." The reverse-BDD framing: "throw the new model into your product and see what it can do, then make that part of the spec." Simon Willison's pelican-on-a-bicycle SVG benchmark as a vibe check.

---

## 📚 Full wisdom (reference)

### SUMMARY
Vaibhav (BAML) and Dex (HumanLayer) discuss when to switch AI models and vibe-code a bespoke Streamlit dashboard comparing model outputs side-by-side for one email-generation prompt.

### IDEAS
- When a new model launches, most engineers now wait for others to vibe-check it publicly first.
- The current model is a known enemy; a fresh new one is an unknown, riskier enemy.
- Simon Willison's personal benchmark: ask each model to generate an SVG of a pelican riding bicycle.
- Switching a prompt to a new model costs almost as much engineering time as building features.
- Evaluating an AI pipeline stays slow because most teams lack automated evals and rely on vibes.
- Accuracy is a new performance dimension AI added alongside latency, cost, uptime, and security engineering constraints.
- A REST API failing 20% of requests is an outage; an AI often calls that acceptable.
- Automating email delivery redefines accuracy: suddenly "hello first name" substitution must be guaranteed, not merely nice.
- Vibe-code a Streamlit dashboard rendering each model's email output so you can eyeball the differences instantly.
- Store test cases as JSON on disk, then loop models x tests fully async for scale.
- Wrap every eval run in try/except so parallel model outages never crash your whole test suite.
- Use Jupyter-style exploratory code for evals, not pytest; evals resemble notebooks far more than unit tests.
- Add a regex detector highlighting em-dashes and AI tells directly inside the eval comparison dashboard UI.
- Side-by-side dropdowns beat showing every model at once; just pick two variants and compare them directly.
- 90% of ML work is shaping data correctly; that infra burden never disappears when using LLMs.
- Building eval infra is like scaffolding shadcn components: generate a best-practice base, then customize everything yourself.

### INSIGHTS
- Every added pipeline step, including an LLM judge, injects more uncertainty and stochastic error into results.
- Behavior-driven development collapsed under AI: you can't pre-spec capabilities you discover only by probing the model.
- Emergent capabilities invert the spec: play with the model first, then bake evals around discovered behavior.
- "Accuracy" is an overloaded stand-in for quality; its meaning shifts entirely with each specific business context.
- The real moat is taste: hardcoded judgments of what good output looks like for your users.
- Since AI writes code cheaply, the eval UI you'd never build before is now trivially buildable.
- Most business problems have no infinite optimum; without user criteria "make it better" is completely meaningless.
- Evaluation, not building, is the new bottleneck; features became fast but judging their quality stayed slow.
- Prompting today is the "assembly era"; systems can't self-heal because our problem definitions remain poorly specified.
- There is no perfect universal eval UI; every domain needs its own bespoke rendering and checks.

### QUOTES
- "Let someone else vibe check for you." (Dex)
- "It's like the known enemy and a new model is like the unknown enemy." (Vaibhav)
- "His vibe is generating an SVG of a pelican on a bicycle." (Dex (on Simon Willison))
- "Can you imagine if your REST API failed on 20% of requests? Like you would be having an outage." (Dex)
- "Switching prompts takes almost as much time as actually writing a new feature." (Vaibhav)
- "90% of the job is not training the model. 90% of the job is getting the data in the right shape." (Vaibhav)
- "The only thing I will not show on screen is the evals because that's the part that takes the most work." (Vaibhav (quoting Brian))
- "I think we're in the assembly era of prompting right now." (Vaibhav)
- "The real moat is this is like taste and knowing what your users want." (Vaibhav)
- "I haven't opened an editor in about a month, and I shipped eight PRs yesterday." (Dex)
- "If you're building evals for a super generic use case, you're probably already cooked." (Dex)

### HABITS
- Never swap a model until you've personally built intuition about its strengths through hands-on manual play.
- When testing a new model, mentally turn off your prior assumptions about what it can't do.
- Run twenty or thirty loose ambiguous prompts to vibe-check a model before any formal task evaluation.
- Eval one pipeline step at a time rather than the whole chain; isolate each improvement clearly.
- Don't run generated code blindly; first check it compiles before trusting Claude's or Cursor's raw output.
- Commit and push frequently while vibe-coding, since agents occasionally delete large chunks of your actual work.
- Spend more time reviewing implementation-plan markdown files than reviewing the actual code the agent eventually produces.
- Adopt a rule: spend ten minutes per feature vibe-coding before deciding whether to code it manually.

### FACTS
- GPT-4o ran roughly two-to-four times faster than GPT-4, trading slight intelligence for major latency and speed.
- Anthropic reportedly said Claude Code represented about 5% of their total effective users around that time.
- A Claude-maxers meetup in SF checked receipts, requiring over $50 daily AI-tool spend for door entry.
- Dex reported shipping eight pull requests in a single day without opening any code editor whatsoever.
- Cursor once hallucinated a package generator version, and later a bad prompt deleted their uncommitted work.
- Amplify Partners interviewed 100 AI founders; eval harnesses resemble ordinary test systems, and are fairly easy.
- When Sonnet 4 and Opus 4 launched, Claude Code inference share reportedly jumped toward roughly 50%.
- Some people now auto-filter incoming emails that contain em-dashes, treating them as an obvious AI-generation tell.

### REFERENCES
- 12 Factor Agents (Dex Horthy / HumanLayer)
- BAML (BoundaryML, Vaibhav)
- HumanLayer
- Simon Willison's "pelican on a bicycle" SVG model benchmark
- Ben Stein (AI Engineer talk on being an AI product manager, emergent specs)
- Cucumber / Gherkin (behavior-driven development)
- Streamlit, Pydantic, uv, Cursor, Claude Code
- shadcn/ui (scaffold-then-customize pattern)
- Sarah Cat / Zara at Amplify Partners (talked to 100 AI founders)
- Jeff Huntley ("deliberate intentional practice")
- Sourcegraph CTO (AI Engineer, "the skill of wielding coding agents")
- "AI That Works" / AI Networks episode series
- MLOps / Agents in Prod virtual conference talk
- DeepSeek; GPT-4o and GPT-4o Mini

### ONE-SENTENCE TAKEAWAY
Evaluation is bespoke; vibe-code a side-by-side dashboard to see what good output means for you.

### RECOMMENDATIONS
- Build a one-test eval first, drop in a cheaper model, and confirm your rough gut instinct.
- Define what accuracy actually means for your specific business use case before evaluating any single model.
- Vibe-code a Streamlit or React UI rendering outputs as real rendered emails, not raw JSON blobs.
- Add small custom checks: detect placeholders, count made-up links, and highlight em-dash and AI tells clearly.
- If your system works and no business need exists, don't bother swapping to any newer models.
- Run eval workloads maximally parallel and async, wrapping each unit so failures never halt the run.
- Treat the eval dashboard as internal team tooling so colleagues can annotate and invalidate bad outputs.
- Adopt the ten-minute rule: try vibe-coding each feature briefly before reverting back to manual hand coding.
