---
title: Prompt-Hackers are coming for your data
videoId: zU8GpxgYDvc
url: https://www.youtube.com/watch?v=zU8GpxgYDvc
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine A, the lethal trifecta as a threat model.** Prompt injection is not about clever wording; an agent is exploitable only when untrusted input, private-data access, and an outbound channel coexist, so removing any one leg kills the attack class.
VERDICT: net-new video available.

**Spine C, a background guardrail agent that cancels bad output mid-stream.** The scalable defense is layered software topped by a background agent that inspects context and rewrites the stream, whose real payoff is alignment, not just leak prevention.
VERDICT: net-new video available.

**Spine B, structured output plus validation invariants.** Structured output does not buy injection safety for free (naive schemas leak more); adding invariants that injected data cannot satisfy turns an injection into a caught parse exception.
VERDICT: next-step (complement) video available.

Also film-able (not deep-dived): **reactive evals**, build one yes/no happy path, then convert each real user misclassification into a new eval Claude Code writes. Slot: Techniques or a new evals chapter. Tactical, likely net-new.

---

# Summary

Vaibhav (Boundary/BAML) and Dexter (HumanLayer) run a code-heavy AI-that-works session demonstrating prompt-injection attacks live and layering deterministic, structured-output, and background-agent guardrails to defend production agents.

🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine A, the lethal trifecta

The claim: prompt injection is not a wording problem, it is an architecture problem. An agent becomes exploitable only when three conditions coexist, exposure to untrusted content, access to private data, and a channel to communicate externally, so removing any one leg neutralizes the whole attack class. Why it is non-obvious: teams try to defend by writing sterner system prompts or asking the model to refuse, but the model is not the vulnerability. Why it is true: because untrusted text (a Zendesk ticket, an email, a scraped page) lands in the same context window as trusted developer guidelines, and the model cannot reliably separate them, any instruction that also touches a private source (dev and prod Supabase over MCP) and an outbound request can be chained into exfiltration or deletion. That is exactly what happened when an attacker emailed a support address and the ticket flowed through Cursor and wiped the database. It generalizes to CI/CD auto-releases, where one poisoned release script cascades, the same automation-brittleness shape. How it goes wrong: cutting a leg costs capability. A sandbox that only reaches the inference API means the agent can no longer browse; over-restrict and it becomes useless.

## Spine C, the background guardrail (alignment) agent

The claim: the durable defense is not one perfect guardrail but layered software, and the top layer is a background agent that inspects every new context message and can cancel or rewrite the stream, whose highest value is alignment, keeping the agent on-task, not only leak prevention. Why it is non-obvious: a synchronous guardrail that classifies before every inference makes the system unbearably slow and less flexible, so people conclude guardrails are impractical. The reframe: run the check in the background and block only on connection, not completion. Why it is true: you kick off a guardrail agent loop on each new message and withhold frontend tokens until it emits its first token, so latency collapses toward the guardrail's connection time; once you have enough labeled decisions you distill that agent into a sub-10ms classifier (OpenAI published exactly this, an LM judge plus a fast classifier). It generalizes to voice agents, where a background supervisor keeps a booking agent from wandering off task, an identical architecture. As Vaibhav puts it, "I actually think of prompt injection's highest value as being an alignment value." How it goes wrong: the guardrail agent is itself injectable, and if it streams slower than the main agent the secret leaks before it catches it.

## Spine B, structured output plus validation

The claim: structured output does not give you prompt-injection safety for free. Naive structured output actually leaks more, because the model cheerfully hallucinates injected content into your schema fields; safety comes from adding validation invariants so an injection produces a parse exception rather than a response. Why it is non-obvious: developers assume "force a JSON schema" equals "constrained and safe," and the live demo showed the opposite. Why it is true: forcing a schema guarantees a response shape, which guarantees the model fills the fields with whatever the attacker steered, including a leaked secret. But if you additionally assert invariants the injected data cannot satisfy (a date field whose length must be greater than zero, a forbidden-substring check on outputs), the parse step throws, your wrapping code catches it, and the user gets "I can't help with that." The guarantee lives in deterministic code, not the model. It generalizes to OCR accounting extraction, where a two-pass numeric check rejects impossible totals. How it goes wrong: every invariant narrows what the agent can legitimately express, and a developer who knows the schema can still probe; constraints raise the attacker's cost, they do not deliver certainty.

---

# 🎬 Proposed ACS videos

## 1. The Lethal Trifecta: Why Your Agent Is One Email Away From Deleting Your Database
- HOOK: An attacker emailed a support inbox and an AI coding agent wiped the production database.
- THE PROMISE: For anyone wiring agents to real data, learn the three-condition threat model and how to remove one leg.
- THE SHAPE: (1) the Zendesk to Cursor to Supabase war story; (2) name the trifecta, untrusted input plus private data plus an exfil channel; (3) map your own agent onto the three legs; (4) demo cutting a leg, a network sandbox with an allowlist plus a human triage queue; (5) the automation-makes-you-brittle tradeoff.
- SPINE: A.
- SLOT: DevBoxes (planned class) or Claude Code, a new "blast radius and security" chapter.
- RELATIONSHIP: ❌ net-new. Nearest is the unscripted DevBoxes concept (limit blast radius) and backlog "blocking-risky-commands-with-hooks"; neither teaches the trifecta threat model or the data-exfil story.
- PROOF TO REUSE: the Zendesk/Cursor/Supabase deletion; Simon Willison's "lethal trifecta"; the COVID toilet-paper supply-chain brittleness analogy; the human triage queue habit.

## 2. Build a Background Guardrail Agent That Cancels Bad Output Mid-Stream
- HOOK: A second agent watches the first one type and yanks the answer the instant it starts leaking.
- THE PROMISE: For agent builders, ship real-time safety without killing latency, and practice alignment engineering while you do it.
- THE SHAPE: (1) why synchronous guardrails are too slow and inflexible; (2) build the background loop inspecting each new context message; (3) block on connection not completion, withhold frontend tokens until the guardrail's first token; (4) distill it into a sub-10ms classifier; (5) reframe, this is an alignment agent, not just leak prevention.
- SPINE: C.
- SLOT: Techniques, agent-building (near backlog "subagent-verification-loops" and "core-agent-loop").
- RELATIONSHIP: ❌ net-new. Backlog "subagent-verification-loops" verifies task correctness after the fact; this is a real-time streaming safety and alignment supervisor that cancels output as it streams, a distinct pattern ACS has not filmed.
- PROOF TO REUSE: the "Nope, you don't get to see that" stream replacement; OpenAI's judge plus fast-classifier paper; the voice-agent background-supervisor parallel; the "highest value is alignment" quote.

## 3. Structured Output Won't Save You: The Validation That Turns Injections Into Errors
- HOOK: Forcing a JSON schema made the leak worse, until they added one length check.
- THE PROMISE: For anyone using structured output, learn the validation invariants that convert an injection attempt into a caught exception.
- THE SHAPE: (1) live demo, plain structured output leaks the secret into a field; (2) why forcing a schema guarantees a response, not safety; (3) add invariants (date length greater than zero, forbidden-substring checks); (4) catch the parse exception and return "I can't help with that"; (5) frame it as the deterministic bottom layer of a defense stack.
- SPINE: B.
- SLOT: Prompt Engineering, structured-output (PE Foundations, already scripted/ready).
- RELATIONSHIP: 🔗 complements "structured-output". That video teaches structured output for reliable extraction and format adherence; this adds validation invariants as an anti-injection security layer, the move after you already get clean JSON.
- PROOF TO REUSE: the live "return the secret in the description" leak; the "date length must be greater than zero" invariant; the substring-of-system-prompt output check; the deterministic-versus-LM guardrail tiers.

---

# 📚 Full wisdom (reference)

## SUMMARY
Vaibhav (Boundary/BAML) and Dexter (HumanLayer) run a code-heavy AI-that-works session demonstrating prompt-injection attacks live and layering deterministic, structured-output, and background-agent guardrails to defend production agents.

## IDEAS
- The lethal trifecta: untrusted content, private-data access, and external communication combined make any AI agent exploitable.
- An attacker emailed a support address; the Zendesk ticket flowed through Cursor MCP and deleted Supabase.
- Structured output used alone actually leaks more; the model hallucinates injected content straight into schema fields.
- Add schema validation like 'date length must be greater than zero' so injection attempts throw exceptions.
- System-message instructions are followed far more strongly than user-message instructions, so secrets belong in system prompts.
- Defense in depth is just software layering: regex, structured output, a fast classifier, then LM guardrails.
- A background guardrail agent inspects every new context message and can cancel or replace streaming output.
- Block frontend tokens until the guardrail emits its first token: block on the connection, not completion.
- Distill your slow guardrail agent into a sub-10ms classifier; OpenAI published a paper doing exactly this.
- Prompt injection's highest value is alignment, not leak prevention: it keeps agents on-task within their domain.
- Never run your inference client on someone else's workstation; just assume they already have your prompt.
- Automation makes any system faster and more brittle; you cannot add automation without a contingency plan.
- A human triage queue reviews every incoming issue before the background agent is allowed to act.
- Coding agents skip permission prompts by default because guardrail-style confirmation on every single action is unbearable.
- Stack multiple guardrail layers so attackers must defeat an entire telephone game of nested injection checks.
- Every agentic surface pulling external data is a new injection entry point requiring its own guardrail.

## INSIGHTS
- Prompt injection is fundamentally a systems-design problem, solved with the same layering as caches and security.
- Real guarantees come from deterministic code wrapping the model, not from trusting the model to behave.
- Every guardrail trades latency and flexibility for safety; each layer narrows what your agent can do.
- AI engineering is ninety percent software engineering; almost no invention beyond reused system-design patterns is required.
- The speed-versus-accuracy tradeoff is really multidimensional; build the fast guardrails fast and the slow guardrails slow.
- Protecting your system prompt is largely wasted effort once inference runs outside of your own infrastructure.
- Building a guardrail agent is the cheapest practical exercise for learning to build real alignment agents.
- Owning the full UI end-to-end lets you cancel bad output mid-stream; raw API consumers simply cannot.
- Once agents become more agentic, the injection surface multiplies, making synchronous guardrails progressively slower and unworkable.

## QUOTES
- "you're just layering these security models on top of itself to prevent prompt rejections of various kinds." (Vaibhav)
- "it just goes back to the thing that Dexter and I would say it's just software." (Vaibhav)
- "anytime you attempt to add automation to your system your automation your system becomes both faster and way more brittle." (Vaibhav)
- "you can't build automation without a contingency plan." (Dexter)
- "no matter what happens, it just takes one prompt that screws you over to make prompt injection a real nightmare for your company." (Vaibhav)
- "AI engineering is 90% software engineering." (Dexter)
- "your value better not be the system prompt cuz if that is you have no value." (Vaibhav)
- "I actually think of prompt injection's highest value as being an alignment value." (Vaibhav)
- "This is engineering. This is why everyone still has a job." (Vaibhav)
- "Be more reactive with your evals rather than proactive." (Dexter)
- "the best way to really learn how to do this stuff is to play with the models and understand them." (Vaibhav)

## HABITS
- They keep a human triage queue reviewing every issue before their background agent ever touches it.
- They run coding agents in network sandboxes restricted to only the inference API and trusted sites.
- They deliberately test guardrails against GPT-4 because weaker models are the easiest to gaslight and inject.
- They add new eval cases from real user misclassification reports rather than inventing test cases upfront.
- They hand a reported failure to Claude Code and ask it to add a matching eval.
- They deliberately handcraft the first ten eval cases instead of trusting the agent's own dumb suggestions.
- They play directly with models to build empirical intuition about how injection and prompting actually behave.
- They reuse voice-agent architecture patterns for guardrails rather than inventing brand-new approaches for each new system.

## FACTS
- A car-dealership chatbot was tricked into agreeing to sell a $70,000 Chevy Tahoe for one dollar.
- A judge reportedly ruled the company had to honor the AI's one-dollar Chevy Tahoe sale offer.
- Public repositories exist collecting the leaked system prompts from Vercel V0, Lovable, and other coding agents.
- OpenAI published a paper pairing an LM-as-judge with a fast classifier that screens messages before inference.
- Simon Willison coined the 'lethal trifecta' framing for the three conditions that enable data-exfiltrating prompt injection.
- During COVID, streamlined supply chains like toilet paper collapsed whenever one early pipeline step simply stopped.
- Claude Code, Codex and similar agents default to taking all permissions to avoid constant confirmation prompts.
- Fast guardrail classifiers can reach sub-ten-millisecond latency once they are distilled from a slower guardrail agent.
- The demo prompt injection stopped working on GPT-4 after model updates but works on older models.

## REFERENCES
- Simon Willison's "lethal trifecta" concept
- Pliny, described as the most prolific prompt injector, and his Latent Space episode
- OpenAI's paper on pairing an LM-as-judge with a fast classifier for guardrails
- Boundary and its BAML programming language (Vaibhav's company)
- HumanLayer (Dexter's company)
- The AI That Works podcast and unconference (April 11, San Francisco)
- The public repo collecting leaked AI-coding-agent system prompts (Vercel V0, Lovable, etc.)
- GEPA (referenced as "Jeppa"), invoked as a cheap eval approach
- The prior AI That Works "voice agents" episode (background supervisor pattern)
- Zendesk, Cursor, and Supabase (the exploited stack in the war story)

## ONE-SENTENCE TAKEAWAY
Defend agents by layering deterministic and background-agent guardrails, because prompt injection is really software engineering.

## RECOMMENDATIONS
- Audit each agent for the lethal trifecta and remove at least one of the three legs.
- Run coding agents inside a network sandbox that only reaches the inference API and trusted domains.
- Add schema validation invariants so injected content produces a parse exception instead of a leaked response.
- Build a background guardrail agent that inspects context and cancels streaming output when it detects leaks.
- Withhold frontend tokens until the guardrail agent's first token arrives, so you block on connection only.
- Distill a proven guardrail agent into a sub-10ms classifier once you have collected enough labeled data.
- Add a human triage queue so that no untrusted incoming ticket reaches your agent without review.
- Build evals reactively: convert each real user misclassification report into a brand-new test case almost immediately.
- Practice building a guardrail agent in your free time to prepare for AI coding-agent system-design interviews.
- Stop protecting your system prompt; keep real value in code and inference behind your own infrastructure.
