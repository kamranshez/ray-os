---
title: LLMs to analyze Enron Emails #6
videoId: gkekVC67iVs
url: https://www.youtube.com/watch?v=gkekVC67iVs
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1 - A trustworthy eval starts by reading one real row by hand, then freezing that exact case into a deterministic test; you do not build the eval framework first.** It is the backbone of the whole session: everything downstream (golden sets, prompt tweaks, model choice) only becomes meaningful after a human has looked at raw data.
VERDICT: net-new video available.

**Spine 2 - Profile your data with a cheap deterministic proxy pass before you ever call the LLM.** Booleans, a regex prefilter, and a progress bar tell you volume, distribution, and cost first, so the expensive model only ever touches the slice that matters.
VERDICT: net-new video available.

**Spine 3 - Structured output is a reasoning scaffold: the schema fields, their order, enums, and escape hatches are where you hardcode the reasoning steps you want.** Not the prompt body.
VERDICT: next-step video available (complements a filmed technique).

Also film-able (not deep-dived): Prove the problem is solvable slowly and expensively, then narrow to one concrete slice and grind it down. One video on collapsing an underspecified LLM task into a provable single-policy pipeline. Complements build-it-twice / scrappy-copy-first.

---

# Summary + counts

Vaibhav and Dexter live-code an LLM pipeline from scratch flagging policy violations in Enron emails, showing how reading data and building evals beats prompt engineering.

Counts: 🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

**Spine 1 - Read the data, then freeze the golden test.** The claim: a trustworthy eval starts by reading one real row by hand, and only after the output looks right do you pin that exact case into a deterministic test. Non-obvious, because most engineers rush to build the eval harness first, generating inputs and scoring in bulk, before looking at a single real example. The mechanism: LLM-generated inputs produce low-quality LLM-generated outputs, so an eval built on synthetic or unread data measures nothing. Vaibhav is blunt: "there's no amount of evals that we could have done on that pipeline until he just read the email." Reading the actual Enron thread exposed the bug the metrics hid, a gift was sent, not received, in a three-way hop through Kinder Morgan to a children's charity. Once a human confirms the label, you pin it as a pytest asserting that message always returns high risk. It generalizes to any classification pipeline, fraud detection, ticket triage, content moderation, where the golden set grows one hand-verified real example at a time. How it goes wrong: freeze a case you misread and you bake a wrong label in forever, and a golden set of one is not coverage, it must accrete across many read rows.

**Spine 2 - The cheap proxy pass before any token is spent.** The claim: before calling the model even once, profile your data with a cheap deterministic pass, booleans, a regex prefilter, a progress bar, so you learn volume, distribution, and timing first. Non-obvious, because the instinct is to wire the LLM in immediately and run; the discipline is to deliberately not call it yet. The mechanism: Vaibhav returns literal true/false from the pipeline and runs it across 10,000 emails, because "I just want to get a proxy for what my data has before I go and execute it in a meaningful way." That proxy reveals only 44 of the sampled emails even mention gifts, so the expensive model only ever sees a tiny relevant slice; a grep for "gift" gates the model, and asyncio runs ten in parallel, collapsing a one-minute loop into ten seconds. tqdm then gives an honest estimate before a 100,000-email run. It generalizes to any large-corpus job, log analysis, document review, where a cheap filter (keyword, embedding similarity, heuristic) precedes the costly model call. How it goes wrong: a naive keyword prefilter misses cases labeled differently, so the filter's recall becomes a silent ceiling on the whole system's recall.

**Spine 3 - Your schema is the prompt.** The claim: the schema is where the prompt engineering actually happens, the fields you choose force the model through the reasoning steps you want, far more reliably than instructions in the prompt body. Non-obvious, because people treat structured output as a way to parse the answer, not to shape the thinking, and they start with check_policy(email, policy) returning bool. The mechanism: a bare boolean gives the model nowhere to reason, so it collapses nuance (send vs receive, or what "asset" means across firms). Vaibhav instead builds a GiftEmailAnalysis object with typed fields, gift_type, sender_company, recipient entity type, relevant_snippets, risk_level, reasoning, follow_up_actions, and says "you're kind of hard coding the exact reasoning steps you want the model to take into the structured output." Field order matters (result before or after reasoning changes behavior), enum wording matters ("unknown" beats "other"; weaker models like DeepSeek and Qwen break enums), and a union "not a gift" class is an escape hatch so validation never hard-fails. It generalizes to any extraction task, invoice parsing, medical coding, where schema fields double as a chain-of-thought. How it goes wrong: over-specified schemas make the model hallucinate to fill fields, and rigid enums crash on the long tail without an escape hatch.

---

# 🎬 Proposed ACS videos

## 1. Read the Data First: How to Build an Eval You Can Actually Trust
- HOOK: You cannot eval your way to quality on data you have never read with your own eyes.
- THE PROMISE: For engineers building LLM classification pipelines, you will walk away able to grow a golden test set from one hand-verified real example instead of a synthetic eval that measures nothing.
- THE SHAPE: (1) Start with a vibe eval, read one real Enron email by hand. (2) Watch the metrics lie, the naive system flagged a sent gift as received. (3) Confirm the true label yourself. (4) Freeze it into a pytest asserting that message stays high risk. (5) Repeat, so the golden set accretes one read row at a time.
- SPINE: Spine 1.
- SLOT: New "Evals" chapter (Prompt Engineering class, or a new Evals mini-class). ACS currently has no eval content anywhere.
- RELATIONSHIP: ❌ net-new. The catalog has no video on building evals or golden test sets; the-ambiguity-line mentions "test case" only in the unrelated context of agent routing.
- PROOF TO REUSE: "there's no amount of evals that we could have done on that pipeline until he just read the email"; the send-vs-receive gift bug; the three-way Kinder Morgan charity hop; "if you use a bunch of LLM generated inputs, you're going to get lowquality LM generated outputs."

## 2. The Cheap Proxy Pass: Profile Your Data Before You Spend a Single Token
- HOOK: Before you call the model even once, run a boolean pass over all your data, you will learn what it costs before it costs you.
- THE PROMISE: For anyone running an LLM over a large corpus, you will learn to measure volume, distribution, and timing with cheap deterministic passes so the expensive model only ever sees the slice that matters.
- THE SHAPE: (1) Grep the 1.7GB archive for "gift". (2) Return literal true/false from the pipeline with no LLM, across 10,000 emails. (3) Discover only 44 are relevant. (4) Run ten in parallel with asyncio, so a one-minute loop becomes ten seconds. (5) Add a tqdm progress bar before scaling to 100,000.
- SPINE: Spine 2.
- SLOT: Techniques class, new chapter on cost-aware LLM pipelines (adjacent to build-it-twice and scrappy-copy-first).
- RELATIONSHIP: ❌ net-new. No catalog video covers profiling data with a cheap deterministic proxy before invoking the model; test-time-compute argues the opposite direction (spend more compute on thinking).
- PROOF TO REUSE: "I just want to get a proxy for what my data has before I go and execute it in a meaningful way"; "I would grap for gift"; the 44-of-10,000 result; asyncio ten-in-parallel; the tqdm estimate for 100k.

## 3. Your Schema Is the Prompt: Structured Output as a Reasoning Scaffold
- HOOK: Stop writing check_policy(email) that returns a bool. The fields you put in your schema are where the real reasoning happens.
- THE PROMISE: For developers using structured output, you will learn to design schema fields, enums, and escape hatches that force the model through the exact reasoning steps you want.
- THE SHAPE: (1) Show the naive boolean check and why it loses nuance. (2) Replace it with a typed analysis object, gift_type, sender_company, entity_type, relevant_snippets, risk_level, follow_up_actions. (3) Reorder fields and watch behavior change. (4) Fix enums, "unknown" beats "other". (5) Add a "not a gift" union class as an escape hatch.
- SPINE: Spine 3.
- SLOT: Prompt Engineering class > structured-output foundations (or Techniques as a boxing-the-model-in follow-up).
- RELATIONSHIP: 🔗 complements "boxing-the-model-in" (filmed, Techniques), which teaches constraining the model's output space. This is the next step: using the schema's fields, their ordering, enums, and escape-hatch union types as an explicit reasoning scaffold, not just a constraint. Do not re-teach why constraining output helps; assume it.
- PROOF TO REUSE: "you're kind of hard coding the exact reasoning steps you want the model to take into the structured output"; the send-vs-receive nuance; enum "unknown" vs "other"; the DeepSeek/Qwen enum-following weakness; the "not a gift" escape hatch that stops validation errors.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav and Dexter live-code an LLM pipeline from scratch flagging policy violations in Enron emails, showing how reading data and building evals beats prompt engineering.

## IDEAS
- The policy-to-prompt problem takes many policy documents plus evidence and asks whether each piece followed them.
- Solve the problem slowly and expensively first once you know it is possible, then grind down.
- Do not build a general policy evaluator; build a specific gift-policy pipeline for one critical rule.
- Structured output fields let you hardcode the exact reasoning steps you want the model to take.
- A naive boolean check loses the nuance of what a domain-specific policy word actually means here.
- The word asset means different things across fintech, macro trading, and crypto contexts, breaking generic prompts.
- Sending a gift differs from receiving one; the naive general system flagged the wrong person entirely.
- Give the model an escape hatch: add a not-a-gift class so the validation step never hard-fails.
- Enum wording matters: models prefer unknown over other, and weaker models often ignore strict enum instructions.
- First grep the 1.7-gigabyte Enron archive for gift before spending any tokens on real LLM calls.
- Return true or false from the pipeline first to profile data distribution before triggering expensive models.
- Running ten emails in parallel with asyncio turns a one-minute iteration loop into roughly ten seconds.
- Save each email and its analysis as separate indexed files, never one giant unreadable JSON blob.
- A vibe eval means reading a real email by hand before writing any deterministic assertion test.
- Freeze a good result into a test asserting that specific email always returns a high-risk level.
- Most pipeline time goes to writing Python, not the tiny AI prompt part everyone obsesses over.
- Caching and record-replay mocking are the two things every LLM developer needs for long-term iteration speed.
- A follow-up-actions field can become a list of tool calls, escalating the pipeline into agentic research.
- A tqdm progress bar gives an approximate mental model of how long a 100,000-email run takes.
- Only a handful of the 10,000 sampled emails are high risk, making human-in-the-loop review completely feasible.

## INSIGHTS
- Feasibility precedes efficiency: prove the naive expensive version works before optimizing toward anything focused or cheaper.
- Narrowing the task to one policy beats generality, because domain nuance quietly destroys generic policy-matching prompts.
- Schema design is prompt engineering: the fields you choose steer the model's reasoning more than instructions.
- You cannot eval your way to quality without first reading raw data with your own eyes.
- The real iteration loop is vibe eval, real data, then a growing set of deterministic tests.
- Cheap deterministic prefilters should gate expensive model calls, radically shrinking cost when scanning large document collections.
- Good enough plus a human in the loop reliably beats chasing a perfectly accurate automated pipeline.
- Fast iteration is the real skill: parallelism, progress bars, and file layout all compound into speed.
- Model choice barely matters until you have proven the problem itself is actually solvable at all.
- Building the harness and eval infrastructure matters far more than crafting one supposedly perfect prompt upfront.

## QUOTES
- "if you can solve the problem slowly and expensively at the start but you know it's possible then you can go grind it down" - Vaibhav
- "we don't need bootstrap for agents. We need shad CN for agents." - Dexter
- "you're kind of hard coding the exact reasoning steps you want the model to take into the structured output" - Vaibhav
- "there's no amount of evals that we could have done on that pipeline until he just read the email" - Vaibhav
- "just slow down and read look at the freaking data" - Vaibhav
- "my favorite actual takeaway of this is like most of this was not prompt engineering" - Dexter
- "caching and mocking are like one of the two key things that every LM developer will need long term" - Vaibhav
- "if you use a bunch of LLM generated inputs, you're going to get lowquality LM generated outputs" - Vaibhav (crediting VB)
- "the most important thing that everyone needs to do is just like get really fast at this" - Vaibhav
- "instead of taking the policy to like 100% I just put a human in the loop in my process and I can solve my software" - Vaibhav
- "I just want to get a proxy for what my data has before I go and execute it in a meaningful way" - Vaibhav
- "I would grap for gift" - Vaibhav

## HABITS
- Always read the actual email by hand before trusting any automated evaluation of your whole pipeline.
- Dump JSON out after every pipeline step so you can always inspect the intermediate objects later.
- Wrap bulk pipelines in a try-catch so one validation error never kills an entire hundred-thousand-item run.
- Write throwaway proxy runs that return booleans first, just to measure data volume and timing cheaply.
- Add a progress bar before launching any long run so you know what you're waiting on.
- Group related LLM calls into a single trace to read an entire run in one view.
- Turn off verbose terminal logging before big runs to keep the console output readable and fast.
- Write simple copy-paste code yourself rather than asking an LLM to perform such trivial mechanical tasks.

## FACTS
- The Enron email dataset was published by CMU as roughly a 1.7-gigabyte archive of sent messages.
- Sarbanes-Oxley, published by the SEC in the early 2000s, governs how public corporations must operate accountably.
- Enron collapsed after executives were found doing shady things, destroying the entire company and its people.
- JP Morgan's 2004 code of conduct covers accepting gifts, public financial commentary, and employee disclosure rules.
- The prior workshop ran eight hours, and forty engineers attended it on a beautiful Saturday afternoon.
- The Sarbanes-Oxley plain text is freely available on Wikipedia as large unstructured blocks of regulatory prose.
- Some AI startups already make seven figures purely by converting policy documents into automated compliance checks.
- Weaker models like DeepSeek and Qwen follow strict enum instructions less reliably than stronger models do.

## REFERENCES
- Enron email dataset (published by CMU)
- Sarbanes-Oxley Act (SEC, early 2000s)
- JP Morgan 2004 code of conduct
- FINRA and SEC guidelines (example policy sources)
- 12-factor agents (Dexter Horthy / HumanLayer)
- shadcn (used as the "shadcn for agents" analogy)
- BAML / BoundaryML (the prompt-definition tooling used on screen)
- tqdm (progress bar), asyncio (parallelism)
- GPT-4 / GPT-4o-mini / o3 (models discussed)
- DeepSeek, Qwen (weaker models noted for enum-following)
- Amazon SQS (suggested for scaling to five million emails)
- Cursor (editor used), pytest (test framework)
- Wikipedia (source of Sarbanes-Oxley plain text)
- "AI That Works" workshop (eight-hour session referenced)

## ONE-SENTENCE TAKEAWAY
Read your real data, narrow the task, then build evals; prompt engineering matters least here.

## RECOMMENDATIONS
- Pick one critical policy and build a dedicated pipeline for it rather than evaluating everything generically.
- Design your structured output fields deliberately so they force the model through your intended reasoning sequence.
- Add a not-relevant escape-hatch class to any classifier so cheap prefilter false-positives never crash the validation.
- Grep or regex-filter your corpus for keywords before ever routing any documents through an expensive model.
- Run a boolean-only proxy pass over your whole dataset to learn its distribution before spending tokens.
- Save individual result files into risk-labeled folders so you can navigate the findings quickly during iteration.
- Turn every confirmed good result into a deterministic pytest that pins down its expected risk level.
- Build caching and record-replay early so you can test the Python without round-tripping to the model.
- Add a human-in-the-loop review dashboard instead of pushing pipeline accuracy toward an impractical full hundred percent.
