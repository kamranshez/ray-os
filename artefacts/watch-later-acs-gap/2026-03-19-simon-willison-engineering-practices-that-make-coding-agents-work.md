---
title: "Simon Willison: Engineering practices that make coding agents work - The Pragmatic Summit"
video_url: https://www.youtube.com/watch?v=owmJyKVu5f8
video_id: owmJyKVu5f8
channel: The Pragmatic Engineer
published: 2026-03-19
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Simon Willison: Engineering practices that make coding agents work - The Pragmatic Summit**](https://www.youtube.com/watch?v=owmJyKVu5f8) - The Pragmatic Engineer - uploaded 2026-03-19

> Net-new ACS video available: conformance-driven development, plus two strong next-step videos on the agent verification loop and the lethal trifecta.

## The idea worth a video

- **Conformance-driven development: have the agent write a cross-framework test suite, then implement your version against it.** Reverse-engineer a standard from existing implementations into tests, then let the agent code until they pass. VERDICT: ❌ net-new video available.
- **Make the agent prove its own work, so you can stop reading the diff: red-green TDD plus booting the server and curling endpoints.** This is the concrete engine behind Willison's "you don't read the code" claim. VERDICT: 🔗 next-step video available.
- **The lethal trifecta: a design-time security test for anything you build on an LLM.** Private data plus malicious instructions plus an exfiltration vector equals danger; the only fix is cutting a leg. VERDICT: 🔗 next-step video available.

## Summary and counts

Simon Willison, in conversation at The Pragmatic Summit, explains the engineering practices, testing discipline, and security models that make coding agents reliable enough to trust.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 — Conformance-driven development (❌ net-new)

The claim: when a standard already has a language-agnostic test suite, you hand it to the agent and say "write code until this passes," and it converges on a working implementation. Most people treat agent tasks as "describe the feature in prose and hope." The non-obvious move is to make correctness external and mechanical: the spec, not your description, becomes the target the agent grinds against. Why it works is a two-step chain: a conformance suite gives the agent a fast, unambiguous pass/fail signal on every iteration, and that tight loop lets it brute-force its way to a correct implementation without you arbitrating each step. Willison pushes it further: when no suite exists, he had Claude build one that passes on Go, Node, Django, and Starlette, effectively distilling six reference implementations into a portable spec, then implemented Datasette's file uploads against it. It generalizes cleanly to porting any library across languages, or to replacing a dependency with a bespoke version that must match its behavior exactly. How it goes wrong: a conformance suite only tests what it encodes, so gaps in the suite become silent gaps in the implementation, and building the suite itself can be the hard part.

### Spine 2 — Make the agent prove its own work (🔗 complement)

The claim: you can stop reading every line the agent writes only once you engineer the agent to prove the code works, and the cheapest proof engine is red-green TDD plus a manual runtime pass. Most people either read every diff (exhausting, "we become full-time code reviewers") or skip verification entirely and ship on vibes. The mechanism has two rungs. First, "use red green TDD" costs about five tokens but constrains the agent to write only enough code to pass a failing test, so scope creep and hallucinated features collapse. Second, because a green suite still does not prove the web server boots, Willison tells the agent to start the server and curl the API, which routinely surfaces bugs the tests never covered; his two-day-old tool Showboat captures that manual exercise as a markdown log. It generalizes to any runtime with a smoke path: booting a CLI, hitting a queue, rendering a page. How it goes wrong: agents will happily fake "manual testing" if you just ask for it, and a test suite the agent both writes and grades can encode the same wrong assumption twice.

### Spine 3 — The lethal trifecta (🔗 complement)

The claim: any system built on an LLM is exposed the moment it simultaneously has access to private data, exposure to attacker-controlled instructions, and a way to send data back out; the only guaranteed defense is removing one of those three legs. The non-obvious part is that this cannot be patched like SQL injection. Willison notes he named prompt injection after SQL injection but the analogy misleads: you can parameterize a SQL query to separate data from instructions, but "there is no way to reliably say this is the data and these are the instructions" to a model, because models are gullible by design and follow whatever text reaches them. So the fix is architectural, not a filter: cut a leg. A coding agent told to read a malicious doc that says "run this base64 blob" is the same attack class as an email assistant tricked into forwarding password resets. It generalizes to any tool-using agent: MCP servers, browser agents, autonomous email bots. How it goes wrong: teams add "ignore malicious instructions" to the prompt and believe they are safe, when the only reliable mitigation is denying private data, untrusted input, or the exfiltration channel entirely.

## 🎬 Proposed ACS videos

### 1. Make the Agent Build the Test Suite First, Then Implement the Standard

- HOOK: You do not have to describe a feature perfectly if the spec can grade the agent for you.
- THE PROMISE: For engineers porting libraries or implementing standards, walk away able to turn any spec into a pass/fail target the agent grinds against unattended.
- THE SHAPE: (1) Show the problem: prose prompts drift, specs do not. (2) Take a standard that ships tests (WebAssembly) and run "write code until this passes." (3) The harder case: have the agent build a conformance suite that passes across Go, Node, Django, and Starlette. (4) Implement your own version against that suite, as Willison did for Datasette file uploads. (5) Failure modes: gaps in the suite become silent gaps in the code.
- SPINE: Spine 1 (conformance-driven development).
- SLOT: Advanced Techniques, new chapter "Spec and Conformance Testing."
- RELATIONSHIP: ❌ net-new. Nearest catalog items ("Tackling Redundant Code" uses a reference implementation to strip code; "Scoping APIs" probes an unfamiliar API) do not teach building a language-agnostic conformance suite and coding against it.
- PROOF TO REUSE: the WebAssembly spec with hundreds of language-agnostic tests; the six-framework file-upload suite ("reverse engineer six implementations of a standard to get a new standard"); the "write code until this test suite passes" prompt pattern.

### 2. Stop Reading the Diff: Make Coding Agents Prove Their Own Work

- HOOK: The teams that no longer read their agent's code did not get reckless, they got the agent to prove it works.
- THE PROMISE: For anyone exhausted by reviewing every line, walk away with a two-rung verification loop that catches bugs before you ever open the diff.
- THE SHAPE: (1) The trust ladder: agents write code, then you stop reading it, and why that only works with proof. (2) Rung one: "use red green TDD" as a five-token constraint that stops over-building. (3) Rung two: green tests do not mean the server boots, so have the agent start the server and curl its own endpoints. (4) Capture the manual pass as a markdown log (Showboat-style). (5) Failure modes: agents faking manual tests; self-graded suites baking in the same wrong assumption.
- SPINE: Spine 2 (make the agent prove its own work).
- SLOT: Techniques, chapter "Debugging and Verifying Output."
- RELATIONSHIP: 🔗 complements "Understanding Agent Output" (Techniques, Debugging and Verifying Output), which teaches asking the agent for an HTML before/after diagram to review a change after the fact. This video adds the DURING-build proof loop: test-first discipline plus booting and exercising the running system, so review load drops instead of shifting.
- PROOF TO REUSE: "we become full-time code reviewers and that's an exhausting sort of state of the world"; "the key thing about TDD is that it means that the agents won't write more than they need to"; "just because the test suite passes doesn't mean that the web server will boot"; Showboat as a 48-hour-old markdown test-log tool.

### 3. The Lethal Trifecta: The Security Test for Everything You Build on an LLM

- HOOK: There is no parameterized query for prompt injection, so the fix is not a filter, it is removing a leg.
- THE PROMISE: For anyone shipping LLM features or running autonomous agents, walk away able to audit any system in one pass and know exactly which capability to remove.
- THE SHAPE: (1) Why LLMs are gullible by design and cannot separate instructions from data. (2) The three legs: private data access, exposure to malicious instructions, an exfiltration vector. (3) Worked attacks: a coding agent told to run a base64-obfuscated rm in a doc; an email assistant forwarding password resets. (4) The fix: cut a leg, usually the exfiltration channel. (5) Where sandboxing and mocking fit as leg-cutters.
- SPINE: Spine 3 (the lethal trifecta).
- SLOT: Advanced Techniques, new chapter "Securing LLM Systems."
- RELATIONSHIP: 🔗 complements "Sandboxing" (Master Claude Code, Niche Features), which teaches HOW to contain a coding agent (sandbox mode, directory isolation, prompt-injection risk reduction). This video teaches the design-time framework for deciding WHEN any LLM feature is dangerous and which leg to cut; sandboxing is one way to cut the damage/exfiltration leg. Note for Ray: the sandboxing and dangerously-skip-permissions mechanics from this talk are already ✅ covered ("Sandboxing" and "Dangerously Skip Permissions"), so this video should stay at the conceptual trifecta level, not re-teach containers.
- PROOF TO REUSE: "language models do exactly what you tell them to do and they will believe almost anything that you say to them"; the base64-obfuscated rm-rf-in-a-doc attack; the password-reset email-assistant example; "the only guaranteed solution is to cut off one of the legs"; the mocking-buttons-instead-of-production-data trick.

### Also film-able (not deep-dived)

- **Code quality is a choice you make with agents.** Feed specific refactor notes back and you get code better than you would write by hand; ignore the diff and the mess is on you. Rough slot: Techniques, Working with the Codebase. Partly adjacent to "The One-Pattern Rule for Agents."
- **Probe the frontier of the current model.** When a model fails a task, tuck it away and retry in six months; you may be first to learn it can now do it (spellchecking was the example). Rough slot: My Daily Workflows.

## 📚 Full wisdom (reference)

**SUMMARY** — Simon Willison, in conversation at The Pragmatic Summit, explains the engineering practices, testing discipline, and security models that make coding agents reliable enough to trust.

**IDEAS**
- Willison now writes more code on his phone than on his laptop, shipping small features constantly.
- AI coding adoption progresses in clear stages: chat helps, agents write code, then nobody reads it.
- Opus 4.5 and GPT 5.1, landing in November, first produced good solutions instead of janky ones.
- Strong DM's software factory runs on two radical principles: nobody writes any code, nobody reads code.
- Not reading code works only if agents can prove to you the code they wrote works.
- Trusting an agent resembles using another team's service: you read the docs, not their source code.
- Saying 'use red green TDD' costs about five tokens yet makes agents write only what's needed.
- Tests were once extra work to maintain; with agents writing them, tests are effectively free now.
- A passing test suite doesn't prove the web server boots, so agents must exercise things manually.
- Willison tells agents to start the server and curl the API, catching bugs tests missed entirely.
- Showboat, a two-day-old tool, makes agents build a markdown log of the manual tests they ran.
- Conformance suites let you tell an agent 'write code until this passes' and it usually complies.
- Willison had Claude build a multipart file-upload test suite passing on Go, Node, Django, and Starlette.
- You can reverse-engineer six implementations of a standard into one test suite, then implement it yourself.
- Agents follow existing codebase patterns almost exactly, so one or two examples set the whole style.
- Cookie cutter templates seed new projects with tests, CI, and a readme so agents extend consistently.
- Poor-quality agent code is a choice you make: ignore the diff and the mess is yours.
- Feeding refactor feedback back to the agent yields code better than Willison would write by hand.
- Prompt injection exploits that language models are gullible and will believe almost anything you tell them.
- The lethal trifecta combines private data access, exposure to malicious instructions, and an external exfiltration vector.
- The only guaranteed defense against the lethal trifecta is cutting off one of the three legs.
- Sandboxing matters most: run the agent somewhere that a malicious instruction can only do limited damage.
- Claude Code for web runs inside an Anthropic container, so skipped permissions become genuinely safe there.
- Rather than copying production data, build mocking buttons that generate edge cases like thousand-ticket-type simulated users.

**INSIGHTS**
- Predictability, not raw capability, is what finally lets developers trust agents and stop reading every line.
- TDD's real value with agents is constraint: it stops them writing more than the task requires.
- Because tests became free, refusing to write them is now indefensible rather than a reasonable tradeoff.
- Automated tests passing is necessary but insufficient; real confidence needs the agent exercising the running system.
- A language-agnostic conformance suite turns 'build this' into a verifiable target the agent can iterate against.
- High codebase quality compounds, because agents copy your patterns, so early discipline pays off repeatedly downstream.
- Prompt injection can't be parameterized away, because LLMs cannot reliably separate trusted instructions from untrusted data.
- A coined term's meaning becomes what people assume on hearing it, not what its author intended.
- Sandboxing off your own hardware makes dangerous autonomy fully acceptable by rendering worst-case damage genuinely trivial.
- The mental exhaustion of juggling parallel agents may be exactly what protects engineers from limitless scaling.
- When a model fails a task, retrying six months later occasionally reveals a newly unlocked capability.
- Vibe-coding bespoke components collapses demand for paid component libraries, exactly as Tailwind's own marketplace has shown.

**QUOTES**
- "Right now, I write more code on my phone than I do on my laptop." — Simon Willison
- "The new thing as of what three weeks ago is you don't read the code." — Simon Willison
- "nobody writes any code, nobody reads any code, which is clear insanity." — Simon Willison
- "how do I have agents prove to me that the stuff they've written works?" — Simon Willison
- "We become full-time code reviewers and that's an exhausting sort of state of the world." — Simon Willison
- "the key thing about TDD is that it means that the agents won't write more than they need to." — Simon Willison
- "I think tests are no longer even remotely optional." — Simon Willison
- "just because the test suite passes doesn't mean that the web server will boot." — Simon Willison
- "it's almost like you can reverse engineer six implementations of a standard to get a new standard and then you can implement the standard." — Simon Willison
- "if the agent spits out 2,000 lines of bad code and you choose to ignore it, that's on you." — Simon Willison
- "language models do exactly what you tell them to do and they will believe almost anything that you say to them." — Simon Willison
- "the only guaranteed solution is to cut off one of the legs." — Simon Willison
- "I think the most important thing is sandboxing." — Simon Willison
- "anytime a model fails to do something for you, tuck that away and try again in 6 months" — Simon Willison
- "Why would I use a date picker library where I'd have to customize it when I could have Claude write me the exact date picker that I want?" — Simon Willison

**HABITS**
- Willison starts every coding session by first telling the agent how to run the test suite.
- He appends the phrase 'use red green TDD' to instructions so agents write tests before implementation.
- He clones a cookie cutter template to start most new projects with structure already in place.
- He runs Claude on his Mac with dangerously-skip-permissions, deliberately avoiding untrusted repos to reduce his risk.
- He keeps three separate projects running simultaneously, switching whenever one agent takes ten minutes to finish.
- He runs a proofreader Claude over every blog post to catch typos and missing apostrophes reliably.
- For his flagship projects he still reviews everything; for throwaway tools he sometimes never looks once.
- He prompts an agent and then walks the dog while it does refactoring he'd otherwise skip.

**FACTS**
- Simon Willison co-created Django back in 2003 while working at a local newspaper in Lawrence, Kansas.
- He co-founded Lanyrd, which was later acquired by Eventbrite, before mainly focusing on Datasette open-source tooling.
- GitHub Copilot arrived around 2022, and ChatGPT chat interfaces became genuinely good over the following year.
- After GPT-4 released, roughly nine months passed before any other competitor built a model that good.
- Claude Code recently turned one year old, marking roughly when genuinely capable coding agents actually began.
- Claude Opus 4.6 optimized Willison's WebAssembly engine, producing a 49% Fibonacci speedup from a single prompt.
- Anthropic and OpenAI optimize models for code because coders will pay $200 monthly for good plans.
- WebAssembly ships a detailed specification containing hundreds of language-agnostic tests that any implementation can run against.
- Tailwind's paid component marketplace has collapsed as people now vibe-code custom date pickers and widgets themselves.
- Open-source projects are now flooded with junk contributions, prompting calls for GitHub to disable pull requests.

**REFERENCES** — Django; Lanyrd; Eventbrite; Datasette; Claude Opus 4.5 and 4.6; GPT 5.1, 5.2, 5.3; Codex 5.3; Claude Code; Claude Code for web; the Claude desktop app; GitHub Copilot; ChatGPT; GPT-4; Gemini; Showboat (Willison's manual-test-logging tool); cookie cutter (Python templating); uv and pytest; the WebAssembly specification and conformance tests; Go, Node.js, Django, Starlette; Docker containers; Apple containers; OpenAI Codex sandboxing; Redis; Tailwind and its component marketplace; Strong DM's "software factory"; conformance-driven development; prompt injection and the lethal trifecta (terms Willison coined); The Pragmatic Summit.

**ONE-SENTENCE TAKEAWAY** — Trust agents only after engineering them to prove their own code works, then sandbox everything.

**RECOMMENDATIONS**
- Append 'use red green TDD' to your prompts so agents write minimal, test-backed implementations by default.
- Tell the agent to boot the server and curl its own endpoints, surfacing bugs tests missed.
- For standards, have the agent write a conformance suite passing on existing implementations, then implement yours.
- Build reusable cookie cutter templates so every new project seeds agents with your preferred patterns immediately.
- Feed specific refactor suggestions back to the agent to get code better than you'd write manually.
- Audit any LLM-powered feature for the lethal trifecta and deliberately remove at least one dangerous leg.
- Run coding agents inside a container or Claude Code for web to neutralize any worst-case damage.
- Instead of cloning production data, build buttons that generate realistic mock users and specific edge cases.
- Learn a third programming language now by simply writing code in it and scanning the output.
- Retry tasks that models failed six months ago; you might discover a genuinely newly unlocked capability.
