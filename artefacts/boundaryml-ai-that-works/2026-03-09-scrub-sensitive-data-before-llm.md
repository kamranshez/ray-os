---
title: How to Scrub Sensitive Data Before it Reaches Your LLM
videoId: Ql2gLHWuX7M
url: https://www.youtube.com/watch?v=Ql2gLHWuX7M
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Stop sensitive data at a redaction proxy, not at the AI layer.** Intercept the outbound request, run a local detect-redact-restore pipeline, and only then forward to the provider, because PII scrubbing is a software placement problem, not a prompt problem.
VERDICT: net-new video available.

**2. Checking is a different task than doing, so a second LLM catches the first one's misses.** A separate check function surfaces failures the redactor missed and doubles as an evolving prod eval harness.
VERDICT: next-step video available (complements "closing-the-loop").

**3. A context window has an instruction budget, not just an information budget.** Cramming every rule into one prompt wrecks attention, so chain narrow passes that each chisel the result toward the balance point you want.
VERDICT: gap-filling video available (Context Engineering class).

---

## Summary

BoundaryML's Vaibhav and HumanLayer's Dex teach building an LLM PII-scrubbing system: a redaction proxy, detect-redact-restore pipeline, a separate check function, and staged instruction-budget prompt chains.

🔴 1 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: The redaction proxy (detect, redact, restore)

The cleanest place to stop sensitive data from reaching a model is a proxy that intercepts the outbound request, scrubs it with a local pipeline, and only then forwards to Anthropic or OpenAI. This is non-obvious because most people assume PII protection lives "at the AI layer" and is a matter of clever prompting; Vaibhav's reframe is that it is a software problem whose leverage point is network placement. The mechanism: the program still believes it is talking to api.anthropic.com, but the request actually hits a proxy in your network that remaps the upstream ("if upstream equals api.anthropic.com do something, otherwise pass through"). That gives you one deterministic chokepoint where every request is inspected before it leaves. Run a small local model there (a 3B or 30B Gemma or Llama) so raw data never leaves the network just to be scrubbed, and store a mapping of masked-to-original so you can swap values back deterministically on the return trip. It generalizes cleanly to any egress-control problem: stopping secret project code names leaking from a whole company's Claude Code usage, or substituting a canonical time zone for a user's local time. It goes wrong two ways: proxying every request adds latency (scope it to provider-bound traffic only), and running the scrubber inline in the hot prod loop degrades users (move it to a post-analysis layer).

### Spine 2: Checking is a different task than doing

A second LLM whose only job is to check a redaction catches misses the redacting model made, because checking and labeling are fundamentally different tasks. The natural objection came straight from the chat (Snow's question): if the redact model already missed it, why would the same model catch it as a checker, it is just rolling the same dice. Vaibhav's answer runs through Scale AI: labeling and validating are different tasks that bend the model's attention in different ways, the way answering a multiple-choice question differs from grading one. So `check_redaction(input, redacted)` poses a narrower validating question and surfaces different failures than `redact` did. That checker also doubles as an eval harness: run it over a sampled slice of production, collect the cases it flags, look for a pattern in the failures, and add a rule for that category. Because you cannot write the test set upfront, the checker is what builds an evolving one from real leaks. It generalizes to any agentic verification: a separate reviewer subagent grading a coding agent's diff, or an LLM-judge in an eval flow. It goes wrong because the checker is still an LLM and can also miss, so you stack evals on evals and AB-test roughly 5% of outputs until the system is "good enough."

### Spine 3: Instruction budget and the bouncing funnel

A context window carries an instruction budget that is separate from its information budget, and cramming many rules into one prompt degrades how well the model attends to any single one. This is non-obvious because people equate context engineering with retrieval, with getting more relevant information into the window; Dex's reframe is that the number of instructions matters at least as much, and more rules means worse adherence to each. The mechanism shows up live in the demo: one prompt carrying every redaction rule over-flags benign "medium risk" items. Rather than endlessly tune that one giant prompt, you add a second pass that re-examines only the medium-risk items and drops the noise, which moves the false-positive versus false-negative balance point. You layer passes like chiseling marble, big hammer to little hammer to polishing cloth, and each subsequent step gets less context but more specific context. It generalizes to any over-stuffed agent prompt: a coding agent handed forty lint rules at once will follow them worse than a staged sequence would. It goes wrong because each extra pass costs latency and money, and over-chaining can oscillate, so you stop at the balance point your product actually needs.

---

## 🎬 Proposed ACS videos

### 1. Scrub Your Secrets Before Claude Code Sends Them to Anthropic
- **HOOK:** Your whole company is piping code to Anthropic and OpenAI right now. Here is how to stop secret project names from ever leaving your network.
- **THE PROMISE:** For engineers rolling Claude Code out across a company; after this you can stand up a proxy that redacts sensitive strings before any request reaches a model provider.
- **THE SHAPE:** (1) The two classes of PII and why class two is a masking problem; (2) remap api.anthropic.com to a local proxy ("if upstream equals anthropic do X, else pass through"); (3) run a small local model (Gemma or Llama, 3B to 30B) to detect leaks; (4) detect, redact, restore using a stored mapping; (5) keep the checker off the hot request path.
- **SPINE:** 1
- **SLOT:** Claude Code class (enterprise rollout / DevBoxes) or Business class.
- **RELATIONSHIP:** ❌ net-new. Closest neighbor is the planned DevBoxes video, but that limits what the agent can DO (blast radius); nothing in the catalog covers a redaction proxy on outbound provider traffic (what data LEAVES).
- **PROOF TO REUSE:** the "if upstream equals api.anthropic.com" pseudo-code; the local Gemma 3 swap-in demo; the mapping-based restore trick from the BAML PII example repo.

### 2. The Checker Catches What the Builder Missed
- **HOOK:** If your agent missed a bug, why would asking it again help? Because checking is a fundamentally different task than doing.
- **THE PROMISE:** For anyone building agent pipelines; after this you can add a separate check function that catches misses and quietly grows your eval suite from production.
- **THE SHAPE:** (1) The intuition trap (same model, same dice); (2) Scale AI, labeling versus validating are different tasks; (3) write check_redaction(input, output) as a narrow yes/no; (4) run it on 5% of prod and mine flagged cases for patterns; (5) turn each pattern into a new rule, then AB-test.
- **SPINE:** 2
- **SLOT:** Techniques class (verification loops) / Context Engineering.
- **RELATIONSHIP:** 🔗 complements "closing-the-loop" (filmed) by being its next step: closing-the-loop teaches giving the agent a feedback signal; this teaches WHY a separate checker sees what the doer cannot, and how to turn it into an evolving prod eval. Also feeds the backlog item "subagent-verification-loops".
- **PROOF TO REUSE:** the Scale AI labeling-versus-checking analogy; the redact() and check_redaction() function pair; "select star of all input and redaction pairs where check failed, then find the pattern."

### 3. Your Prompt Has an Instruction Budget, Not Just an Information Budget
- **HOOK:** Everyone obsesses over stuffing the right info into context. The bigger lever is how many rules you ask for at once.
- **THE PROMISE:** For people whose agent ignores half its instructions; after this you can split one overloaded prompt into a staged funnel that actually holds.
- **THE SHAPE:** (1) Information budget versus instruction budget; (2) demo, one prompt with all rules over-flags medium-risk items; (3) add a second pass re-checking only medium risk; (4) the chisel-the-marble metaphor (big hammer, little hammer, polish); (5) each step gets less but more specific context.
- **SPINE:** 3
- **SLOT:** Context Engineering class.
- **RELATIONSHIP:** 🟡 fills the gap in the Context Engineering class, which covers context and information broadly but not the instruction-budget-versus-information-budget distinction or the staged-funnel technique for cutting false positives.
- **PROOF TO REUSE:** the "instruction budget" quote; the medium-risk false-positive iteration; the chiseling-marble metaphor.

### Also film-able (not deep-dived)
- **Dynamic user-defined redaction categories (become infrastructure):** let customers own categories, rules, and hierarchies while you own the control plane, mirroring how Jira and Linear manage labels. Rough slot: Business class. Likely net-new.
- **Deterministic-first (do not make the LLM do what code can):** regex and time-zone math belong in deterministic code so the LLM is reserved for what only it can do. Rough slot: Techniques class. Likely partial to "high-level-strategy-low-level-details".

---

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's Vaibhav and HumanLayer's Dex teach building an LLM PII-scrubbing system: a redaction proxy, detect-redact-restore pipeline, a separate check function, and staged instruction-budget prompt chains.

### IDEAS
- Split PII into two classes: zero-tolerance legal liability versus data you would merely prefer not leaking.
- Class one PII is a pure software control-plane problem, solved without any AI involved at all.
- Getting one hundred percent PII guarantees is effectively impossible, so treat redaction as really good masking.
- Good masking sends the concept of the data across without ever sending the raw data itself.
- PII redaction is never a clean line but a biased zone between false positives and negatives.
- Better techniques narrow the zone; you choose whether to bias toward leaking or toward degrading experience.
- Never make the LLM do what deterministic code handles faster, cheaper, and far more reliably instead.
- Three redaction rule types exist: fast static rules, dynamic runtime rules, and slower generative LLM rules.
- Static and dynamic rules stay reactive and fast while generative rules are proactive, high-coverage, but slow.
- Build a proxy that remaps api.anthropic.com, redacts each request locally, then forwards to the real provider.
- Run redaction through a small local model like a 3B or 30B, never the cloud provider.
- Keep the checker off your main prod loop; trigger it as a post-analysis storage-layer step instead.
- Model redaction as a multi-step agent loop that rewrites text, not one single classification LLM call.
- Checking is fundamentally different from labeling, so a separate check function catches what the doer missed.
- You cannot write the test cases upfront; build an evolving suite from real production leak data.
- You have an instruction budget, not only an information budget, inside every model's finite context window.
- More rules crammed at once means the model attends worse to any single one of them.
- Chain narrow prompts like chiseling marble with a big hammer, a little hammer, then polishing cloth.
- Add a second pass that re-checks only medium-risk items to strip the false positives introduced earlier.
- Let customers define their own redaction categories: you own the control plane, they own the shapes.
- Inject per-user info like email, address, and phone into prompts to find that user's PII better.
- For developer data access, prefer time-boxed signed data waivers over building separate redacted datasets and models.
- For image redaction, prefer bounding boxes over OCR, since OCR loses the structural hierarchy of content.

### INSIGHTS
- The first mistake is treating all PII identically instead of separating legal-liability data from preference data.
- Most companies never need class-one security; securing the database layer plus an intranet handles nearly everything.
- PII redaction is almost entirely a software problem; the AI part is actually the easiest piece.
- Choosing your false-positive versus false-negative bias is a deliberate per-product design decision, not a technical accident.
- Reach for generative LLM rules only to optimize a mostly-solved problem, not as your first move.
- The redact-then-check split mirrors Scale AI's business: labeling and validating are genuinely two different tasks entirely.
- Reliability comes from stacking fallbacks and evals until the system meets your requirement, then you stop.
- Redaction generalizes beyond secrets: substituting timestamps for canonical time zones is exactly the same masking pattern.
- Becoming infrastructure means owning the control plane while your customers own their categories, rules, and hierarchies.
- An interface layer translating what code, user, and LLM each see is the general reusable abstraction.

### QUOTES
- "Don't make the LM do things that it's either like not good at because you're going to detract attention away from the task." (Dex)
- "If you can do things deterministically, then don't make the LM do them cuz it's going to be faster, cheaper, and more reliable." (Dex)
- "It is effectively impossible to get 100% PII guarantees on here." (Vaibhav)
- "The best way that at least I model PII is it's really, really good masking." (Vaibhav)
- "This is a control plane that you have to build. And you just have to build this regardless of the fact that you're using AI or not." (Vaibhav)
- "The PII system is just a software problem." (Vaibhav)
- "Checking and labeling are two different tasks. The redact method is a labeling task. The check method is a check task." (Vaibhav)
- "You have an information budget in your context window and then you have an instruction budget." (Dex)
- "The more like rules and instructions are giving the model to all follow at once, the less well it can attend to any specific one of them." (Dex)
- "You build fallbacks on fallbacks on fallbacks until the system fail, and like, that's good enough, and that meets our requirement." (Vaibhav)
- "All the shapes in the data are owned by the company that you're selling to." (Vaibhav)
- "It's not actually a line. This is like a zone and it's like okay there's going to be this blurry area." (Dex)

### HABITS
- Always spend twenty to twenty-five minutes on fundamentals before letting the agent run off implementing anything.
- Map every unfamiliar new concept onto something already understood, like relating Redis to an L1 cache.
- Test one LLM-generated case at a time rather than blindly accepting the whole batch it produced.
- Spot-check roughly one hundred samples by eye rather than building formal evals for every single thing.
- Sample five percent of check-redaction outputs and AB test them continuously to build confidence over time.
- Snapshot results across cases, then eyeball the diff to catch regressions, exactly like the evals flow.
- Ask the LLM to brainstorm test patterns, then human-review the list rather than generating synthetic data.
- Deliberately alias field names, like calling something ID, to steer how the model actually interprets them.

### FACTS
- Google runs everything on the public internet, with every node authenticating to each other via MTLS.
- PCI compliance requires every node touching a credit-card number to be fully air-gapped from outbound access.
- Online games banned unfriendly words with thousand-line regex filters for almost the entire history of gaming.
- Players evade word filters by respelling, reannotating, or redefining words like unicorn to mean something new.
- Even the most security-conscious enterprises typically trust only about five external vendors with their sensitive data.
- Google built Face ID using time-boxed signed employee waivers granting developers face-data access for sixty days.
- Some organizations reportedly run their entire infrastructure inside concrete bunkers located deep underground purely for security.
- Scale AI built an entire business model on the premise that checking differs fundamentally from labeling.

### REFERENCES
- People: Vaibhav Gupta (BoundaryML, creator of BAML), Dexter "Dex" Horthy (HumanLayer). Show: "AI That Works".
- Tools and services: BAML, Claude Code, Anthropic, OpenAI (GPT-4/mini), AWS Bedrock, Amazon Comprehend, Salesforce, Workday, Scale AI, Google Face ID, Redis, Llama, Gemma 3, an npm profanity-filter regex.
- Concepts: zero trust, BeyondCorp, firewall-as-boundary, MTLS, intranet/air-gap, PCI, HIPAA.
- Prior episodes referenced: the relative-timestamps/datetime episode, the PDF/multimodality episode, the dynamic-rules episode, the evals-flow episode.
- Events: the Coding Agents conference (Mountain View), the "AI That Works" unconference (targeting March 28, SF). Next episode: agents and skills.

### ONE-SENTENCE TAKEAWAY
PII scrubbing is a software masking pipeline you tune on a bias spectrum, not AI.

### RECOMMENDATIONS
- Classify your PII into legal-liability versus mere-preference tiers before you write any redaction code at all.
- Solve class-one data at the infrastructure layer using intranets or air-gaps long before reaching for AI.
- Start redaction with cheap static regex, then layer an LLM only where regex provably cannot succeed.
- Build your redaction proxy to intercept only Anthropic-bound requests, passing every other request straight through untouched.
- Build a detect, redact, and restore pipeline storing a mapping so masked values swap back deterministically.
- Write a separate check-redaction function and run it periodically over a sampled slice of production traffic.
- Mine your production failures for patterns, then add one targeted new rule per discovered failure category.
- When false positives pile up, add a narrow re-check pass rather than overloading one giant prompt.
- Give consumer chat users a UI button to undo any specific redaction the system applied automatically.
- Let enterprise customers define their own redaction categories, mirroring exactly how Jira and Linear manage labels.
