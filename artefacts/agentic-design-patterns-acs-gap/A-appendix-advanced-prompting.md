---
title: "Ch A: Appendix A: Advanced Prompting -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "A"
pattern: "Appendix A: Advanced Prompting"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch A: Appendix A: Advanced Prompting** - Antonio Gulli

> Two net-new videos hide inside a mostly-covered survey: (1) optimise a prompt against a goldset + scoring metric like DSPy, and (2) force agent output into a Pydantic-validated schema at component boundaries. The reasoning staples (CoT, ReAct, RAG, roles, few-shot) are conceptual textbook material ACS already lives in.

## The one idea worth a video

- **Stop hand-tuning prompts; optimise them against a goldset and an objective function like you would train a model.** This is the highest-altitude idea in the appendix's "Advanced Techniques" - it subsumes iterative refinement, meta-prompting, and few-shot example selection into one data-driven loop. VERDICT: ❌ net-new video available.
- **Requesting structured output is only half the job; validate it against a Pydantic schema at every component boundary ("parse, don't validate").** Distinct demo, distinct slot (making agent output machine-trustworthy), so it earns its own spine. VERDICT: ❌ net-new video available.
- **Use the LLM itself to critique and rewrite your prompt (the "meta" approach).** Load-bearing but ACS already ships "Getting Prompt Feedback." VERDICT: ✅ already covered (kept for context).

## Summary + counts

A textbook survey of prompting: core principles, zero/one/few-shot, structuring, CoT/ReAct/ToT reasoning, tool use, RAG, and automated prompt optimisation for reliable agentic systems.

🔴 2 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Prompts are programs you optimise, not text you tune
THE CLAIM: crafting effective prompts should be a data-driven optimisation against a goldset and a scoring metric, not manual trial-and-error. WHY IT'S NON-OBVIOUS: everyone treats a prompt as prose to keep re-wording by hand and eyeballing outputs; the appendix argues the whole loop can be programmatic. WHY IT'S TRUE / MECHANISM: Gulli describes two components - "A Goldset (or High-Quality Dataset)... input-and-output pairs" that define success, and "An Objective Function (or Scoring Metric)" that scores each output against the golden one. An optimiser (he names a Bayesian optimiser and the DSPy framework) then either "programmatically samples different combinations of examples" (few-shot optimisation) or uses an LLM as a "meta-model to iteratively mutate and rephrase" the instructions - both maximising the metric. Because you now have a number, prompt quality becomes measurable and improvement becomes search. WHAT IT GENERALIZES TO: in agentic coding, the "prompt" is a subagent/skill definition. Build 10-20 input->ideal-output pairs for that subagent, write a scoring script, and loop Claude to mutate the prompt until the score peaks - a Loopy-AI-flavoured prompt optimiser. HOW IT GOES WRONG: a weak or tiny goldset overfits the prompt to your examples; a sloppy objective function (BLEU/ROUGE on nuanced tasks) rewards the wrong thing.

### Spine 2 - Structured output is worthless until it's validated at the boundary
THE CLAIM: asking for JSON is not enough; you populate a Pydantic model and validate, so raw model text becomes a typed, enforceable object before it flows downstream. WHY IT'S NON-OBVIOUS: teams stop at "return JSON" and then `json.loads` blindly, discovering malformed or wrong-typed fields only when a later step crashes. WHY IT'S TRUE / MECHANISM: Gulli shows `User.model_validate_json(llm_output_json)` doing parse + validate in one step, raising `ValidationError` on any mismatch, and even coercing a date string into a `datetime.date`. The payoff: "When an LLM's output is encapsulated within a Pydantic object, it can be reliably passed to other functions, APIs, or data processing pipelines with the assurance that the data conforms." He frames it as "parse, don't validate at the boundaries of your system components." WHAT IT GENERALIZES TO: agentic coding - a subagent that returns findings, or a Claude Code hook consuming tool output, should emit schema-checked JSON so the orchestrator fails loudly and early instead of propagating garbage. HOW IT GOES WRONG: over-strict schemas reject harmlessly-formatted output and stall the loop; skipping the error branch turns a caught `ValidationError` into a silent downstream crash "leading to catastrophic failures within an automated workflow."

### Spine 3 - Use the LLM to refine your own prompt (covered, for context)
THE CLAIM: hand the model your existing prompt, the task, and the bad outputs, and ask it to diagnose ambiguity and rewrite it - "AI helps us talk better to AI." WHY IT'S TRUE: a strong model spots blind spots (missing delimiters, vague format, weak persona) faster than manual iteration and doubles as a learning tool. WHY COVERED: ACS's "Getting Prompt Feedback" (Prompt Engineering -> Improving Your Prompting) already ships a slash-command that inspects session history, flags weak prompts, and rewrites them - the same meta loop, grounded in real coding sessions rather than abstract examples. No distinct B remains, so this yields no pitch.

## 🎬 Proposed ACS videos

### 1. Auto-Tune an Agent Prompt Against a Goldset
- **HOOK:** You keep re-wording your subagent prompt and guessing if it got better. Give it a score instead.
- **THE PROMISE:** For anyone who owns a repeated agent prompt (a skill, subagent, or extraction command), you leave able to optimise it against a measurable metric instead of vibes.
- **THE SHAPE:** (1) Pick one repeated prompt - say an "extract PR risk" subagent. (2) Build a goldset: 15 input->ideal-output pairs in a JSON file. (3) Write a scoring script (exact-match / rubric-as-LLM-judge) that grades an output against the golden one. (4) Loop: have Claude mutate the prompt's wording AND its few-shot examples, re-run the goldset, keep the highest score. (5) Show the score climbing across rounds and diff the winning prompt vs your original.
- **SPINE:** Spine 1.
- **SLOT:** Prompt Engineering -> new chapter "Optimising Prompts" (adjacent to "Improving Your Prompting"); doubles as a Loopy AI loop.
- **RELATIONSHIP:** ❌ net-new. "Getting Prompt Feedback" critiques prompts qualitatively from session history; this is the quantitative, goldset-scored optimisation loop it never touches.
- **PROOF TO REUSE:** Gulli's two components - "A Goldset... input-and-output pairs" as ground truth and "An Objective Function... returns a score"; his split of "Few-Shot Example Optimization" vs "Instructional Prompt Optimization"; the DSPy framing that prompts are "programmatic modules that can be automatically optimized."

### 2. Force Your Agents to Return Validated JSON with Pydantic
- **HOOK:** Your agent said it returned JSON. Then the next step crashed on a missing field. Validate at the boundary.
- **THE PROMISE:** For devs wiring agent output into scripts/pipelines, you leave able to make an agent's output typed and trustworthy so bad output fails loudly at the door.
- **THE SHAPE:** (1) Define a Pydantic model with typed, described fields. (2) Prompt the agent (or subagent) to emit JSON matching it. (3) `model_validate_json` at the boundary - parse + validate in one call. (4) Show a malformed/wrong-typed run raising `ValidationError` and being caught, vs a naive `json.loads` propagating garbage. (5) Wire the validated object into a downstream step to prove interoperability.
- **SPINE:** Spine 2.
- **SLOT:** Techniques -> Debugging & Verifying Output (or Context Engineering for pipeline output contracts).
- **RELATIONSHIP:** ❌ net-new. ACS covers reading and diagramming agent output ("Understanding Agent Output") but nothing on schema-enforcing and validating structured output at component boundaries.
- **PROOF TO REUSE:** The `model_validate_json` example that coerces a date string to `datetime.date`; the "parse, don't validate at the boundaries of your system components" principle; the conclusion's warning that without this "the agent's internal cognitive components cannot communicate reliably, leading to catastrophic failures."

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** A textbook survey of prompting: core principles, zero/one/few-shot, structuring, CoT/ReAct/ToT reasoning, tool use, RAG, and automated prompt optimisation for building reliable agentic systems.

**IDEAS**
- Prompting is the primary interface; well-designed prompts maximise model potential, poor ones yield ambiguous output.
- Five core principles: clarity/specificity, conciseness, action verbs, instructions over constraints, experimentation.
- What is confusing to the user is likely confusing to the model.
- Positive instructions beat negative constraints; constraints make the model focus on avoidance.
- Zero/one/few-shot form a ladder of example-based guidance for the model.
- Few-shot needs 3-5 diverse, high-quality examples; mix class order to prevent overfitting.
- Long-context models now enable "many-shot" learning with hundreds of in-prompt examples.
- System prompts set persona, rules, and behaviour; role prompts assign an expert identity.
- Delimiters (backticks, XML tags, markers) separate instruction, context, and input cleanly.
- Context engineering dynamically assembles system prompts, retrieved docs, tool outputs, and implicit data.
- Structured output (JSON/XML) forces structure and can limit hallucination.
- Pydantic gives an object-oriented facade: parse + validate LLM JSON in one step.
- Chain of Thought exposes intermediate reasoning steps for accuracy and interpretability.
- Self-consistency samples multiple reasoning paths and majority-votes the answer.
- Step-back prompting asks for a general principle first, then applies it.
- Tree of Thoughts explores multiple branching reasoning paths with backtracking.
- Function calling: the model emits a structured tool call; the system executes it.
- ReAct interleaves Thought -> Action -> Observation loops with tools.
- APE/DSPy treat prompts as programs optimised against a goldset and metric.
- RAG grounds responses by retrieving external documents into the prompt.

**INSIGHTS**
- Prompt engineering is disciplined engineering that reduces natural-language ambiguity toward one correct intent.
- Context quality can matter more than model architecture for output quality.
- Structured, validated output converts probabilistic text into a deterministic cognitive engine.
- CoT improves robustness across model versions, not just single-run accuracy.
- Reasoning techniques trade tokens/cost for reliability; self-consistency and ToT are expensive.
- Prompts become measurable - and therefore optimisable by search - once you attach a scoring metric.
- ReAct and function calling are the agent's hands; RAG and context engineering are its senses.
- Meta-prompting turns the LLM into a collaborative partner in its own instruction design.

**QUOTES**
- "what is confusing to the user is likely confusing to the model."
- "the quality of a model's output depends more on the richness of the provided context than on the model's architecture."
- "This practice of 'parse, don't validate' at the boundaries of your system components leads to more robust and maintainable applications."
- "treating prompts not as static text but as programmatic modules that can be automatically optimized."
- "It's a fascinating loop where AI helps us talk better to AI."
- "these structuring and reasoning techniques are what successfully convert a model's probabilistic text generation into a deterministic and trustworthy cognitive engine for an agent."

**HABITS / PRACTICES**
- Start with a draft prompt, test, analyse shortcomings, refine iteratively.
- Document every prompt attempt with its configuration and result.
- Save prompts in separate, version-controlled files in the codebase.
- Set temperature to 0 for single-answer tasks; place the answer after reasoning.
- Mix up class order in few-shot classification examples.
- Use variables in application prompts instead of hardcoding values.
- Rely on automated tests and evaluation for production prompts.
- Re-test existing prompts against each new model version.

**FACTS**
- Few-shot prompting typically uses three to five input-output pair examples.
- CoT increases output length, raising token cost and latency.
- Self-consistency requires running the model multiple times per query, increasing cost.
- Modern long-context models (e.g. Gemini) support hundreds of in-prompt examples.
- APE optimisers may score candidate prompts with metrics like BLEU or ROUGE.

**REFERENCES**
- DSPy framework (Stanford NLP) - programmatic prompt optimisation.
- Pydantic, xmltodict - Python validation / XML-to-dict libraries.
- Google Vertex AI Prompt Optimizer; Google Gems; Gemini.
- Papers: Chain-of-Thought (Wei et al., arXiv 2201.11903), Self-Consistency (2203.11171), ReAct (2210.03629), Tree of Thoughts (2305.10601), Step-Back (2310.06117).
- Kaggle "Prompt Engineering" whitepaper.

**ONE-SENTENCE TAKEAWAY:** Treat prompting as measurable engineering - structure, validate, and optimise prompts against goldsets to build reliable agents.

**RECOMMENDATIONS**
- Build a goldset + scoring metric for any prompt you reuse, then optimise it.
- Wrap LLM JSON output in Pydantic models and validate at every boundary.
- Add "Let's think step by step" and temperature 0 for deterministic reasoning tasks.
- Use delimiters and explicit output schemas to remove ambiguity.
- Ask the LLM to critique and rewrite your weak prompts.
- Store prompts as versioned files with an automated evaluation harness.
