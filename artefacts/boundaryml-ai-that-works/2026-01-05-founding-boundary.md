---
title: Founding Boundary
videoId: 4YTl9w_bESE
url: https://www.youtube.com/watch?v=4YTl9w_bESE
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine A. When the test suite is too big to run every change, predict from the git diff which tests the change can affect and run only those.** This is the load-bearing engineering idea in the video: it turns a batch pipeline into an interactive loop, which is exactly what an agent editing at speed needs. VERDICT: 🔗 next-step video available (complements "closing-the-loop").

**Spine B (latent).** Treat the model call as a typed primitive with a resilient parser, and model streaming as an explicit dual type system, rather than gluing strings through generic abstractions. Stands alone as a reframe even though the source treats it briefly and BAML-specifically. VERDICT: 🟡 fills a gap in "structured-output" (foundations); film the principle, not the tool.

---

# Summary

Dex interviews Vaibhav Gupta on the AI That Works podcast about founding BAML: twelve pivots, a DE Shaw test-selection framework, and typed LLM function calls.

🔴 0 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine A. Scope the tests to the diff

The claim: when a test suite is too large to run per change, predict from the git diff which tests the change can affect and run only those. At DE Shaw, Gupta's algorithm cut CI from about thirty-three hours to under five minutes for ninety percent of commits. Non-obvious part: the instinct is to make the whole suite faster (parallelize, adopt Bazel). Gupta rejected Bazel outright, calling it "impossible to use outside of Google" and too steep a learning curve for a thirty-year-old codebase, and instead attacked which tests run at all. Mechanism: most commits touch a tiny slice of the dependency graph, so if you can map a diff to its dependent tests you skip the large majority that cannot possibly break, and wall-clock time collapses without losing safety. Why it is hard: in Python, dynamic imports and reassigning a global from a function name to a variable make that graph unpredictable, and "that just works," so naive static analysis misses edges. Generalizes to agentic loops directly: an agent that edits fast needs its verification loop to close in seconds, not hours, or it cannot self-correct. It goes wrong when the diff-to-test map is wrong. A missed test means a real break ships, and in a trading shop that is millions of dollars, so the map must fail conservative (over-include when unsure).

## Spine B. The model is a primitive, not an abstraction

The claim: an LLM call should be a typed primitive, "a primitive that are similar to like an operator like plus or minus," wrapped in a type system and a resilient parser, not hand-glued through generic abstractions. Non-obvious part: the common read is that BAML is "betting against the labs" improving structured output. Gupta rejects that framing, saying structured output "is actually not at all about that." Mechanism: streaming is an application-level construct the provider cannot own, because "you can't possibly do streaming semantics on the lab side," since the raw model behaves identically regardless of how you consume it. That creates a dual type system: a partial shape while tokens stream and a different complete shape when finished. Optionalizing every field to fake this fills downstream code with null checks, and most languages cannot represent two type systems at once, which is the actual justification for a domain-specific language. Generalizes to any agent pipeline consuming model output: you want typed, streamable results and a parser that tolerates malformed JSON, recursive types, and unescaped tokens. It goes wrong if taught as tool worship. The transferable idea is the typing discipline, and the labs closing the parsing gap narrows the JSON-fixing half of the value, so lead with streaming semantics, which they cannot own.

---

# 🎬 Proposed ACS videos

## 1. Only Run the Tests Your Change Can Break

- **HOOK:** Your agent edits in seconds, then waits half an hour for the full suite. Close that gap.
- **THE PROMISE:** For engineers running agents against a large codebase. After this you can make your test loop close in seconds by running only the tests the diff can actually affect.
- **THE SHAPE:**
  1. The bottleneck: a full-suite run (thirty-three hours at DE Shaw) makes the agent's feedback loop unusable.
  2. The wrong fix: parallelize everything or adopt Bazel, rejected as unusable outside Google and too heavy for a legacy codebase.
  3. The right fix: map the git diff to its dependent tests and run only that subset.
  4. The trap: dynamic imports and global reassignment defeat naive static mapping, so the selector must fail conservative.
  5. Demo: Claude Code inspects a diff, selects the affected tests, runs only those, and the loop closes fast.
- **SPINE:** A
- **SLOT:** Techniques (sits next to "closing-the-loop"); Context Engineering is a fine alternate home.
- **RELATIONSHIP:** 🔗 complements "closing-the-loop." That video already teaches giving the agent a test and lint loop so it self-corrects. This is its next step: when the suite is too big to run every iteration, scope the loop to the diff so it stays fast enough to actually run each time.
- **PROOF TO REUSE:** the thirty-three hours to under five minutes for ninety percent of commits number; the Bazel rejection reasoning ("impossible to use outside of Google"); the Python dynamic-import and global-reassignment "that just works" gotcha that makes the mapping hard.

## 2. Treat the Model Like the Plus Operator

- **HOOK:** Stop gluing LLM strings through generic wrappers. Give the call a type and a parser instead.
- **THE PROMISE:** For engineers building LLM features. After this you can model streaming output as a dual type and stop drowning in optional-field null checks.
- **THE SHAPE:**
  1. The mess: LangChain-style "abstraction for the sake of abstraction" over what is fundamentally a string.
  2. The reframe: the model is a primitive like plus or minus, so wrap it in a type system.
  3. Streaming is an application-level construct: a partial type while streaming, a complete type when done.
  4. Why optionalizing every field fails, and why Zod plus TypeScript runtime types are not enough.
  5. Demo: a typed model function with a resilient parser handling malformed and recursive JSON.
- **SPINE:** B
- **SLOT:** Prompt Engineering, PE Foundations (next to "structured-output").
- **RELATIONSHIP:** 🟡 fills the gap in "structured-output." That foundations video covers getting typed output from a model. This adds the two things it does not: resilient parsing of malformed or recursive output, and the streaming dual-type problem the labs cannot own. Film the principle, not BAML's syntax.
- **PROOF TO REUSE:** "models are a primitive that are similar to like an operator like plus or minus"; "you can't possibly do streaming semantics on the lab side"; the optionalize-everything argument for why a dual type system needs its own representation; customers deleting over three thousand lines of glue code when migrating.

---

# 📚 Full wisdom (reference)

## SUMMARY
Dex interviews Vaibhav Gupta on the AI That Works podcast about founding BAML: twelve pivots, a DE Shaw test-selection framework, and typed LLM function calls.

## IDEAS
- At DE Shaw, an algorithm predicted which tests a git diff needed, cutting CI time dramatically.
- That test-selection system dropped a 33-hour CI pipeline to under five minutes for 90% of commits.
- Python's dynamic imports and global-variable reassignment make static test-dependency prediction far harder than it first appears.
- Adopting Bazel to prune tests was rejected: unusable outside Google, too steep for a legacy codebase.
- BAML began because LangChain felt like abstraction for abstraction's sake over what is fundamentally a string.
- Streaming is an application-level construct the model providers cannot solve; the raw LLM behaves identically regardless.
- Streaming creates a dual type system: partial types during streaming, a different complete type when finished.
- Optionalizing every field to model streaming makes downstream code ugly, forcing null-checks everywhere it is consumed.
- Gupta frames LLM models as a primitive like the plus operator, not merely a high-level abstraction.
- BAML's JSON parser hardened by absorbing thousands of real malformed-output cases reported by its own users.
- Structured-output APIs still handle recursive types poorly, which pushed BAML to build its own resilient parser.
- Enterprise buyers value maintainability and easy hireability over how quickly a new framework gets you started.
- Migrating to BAML let several customer teams delete over three thousand lines of glue code consistently.
- Early BAML shipped without an LSP or syntax highlighter, so users wrote code in plain files.
- The founders imposed a time-bounded bet: keep going until year-end, then pivot away if nothing landed.
- Building on Twitch or LinkedIn fails: platforms copy or block anyone growing a business atop them.
- A first Microsoft code review returned 82 comments on a 50-line change, reframing his skill level.
- The next-step trap: founders build business A to fund business B instead of building B directly.

## INSIGHTS
- Reliability tooling wins by absorbing thousands of others' edge cases, not by anticipating them all yourself.
- The right layer for a problem is where it actually lives; streaming belongs in the application.
- Betting against the labs improving is wrong framing; the real value is application-level semantics they ignore.
- Test infrastructure that scopes work to the diff turns a batch pipeline into an interactive loop.
- Adopting a tool the wider team cannot learn creates unmaintainable code regardless of the tool's merit.
- Trust, not product quality, closes early customers; they buy the founder before they buy the software.
- Fixing a bug within fifteen minutes beats filing a ticket; ticketing signals the problem won't move.
- Playing to your strengths matters: engineers should not stake a company on beating designers at UX.
- A dual type system is unrepresentable in most languages, which justifies inventing a dedicated domain-specific language.

## QUOTES
- "You should never be leaving a job when you're unhappy. You should always be leaving a job when you are happy." (Gupta, recalling manager Drew Seedley)
- "Chasing money is dumb." (Gupta)
- "Code is art and it should be represented as such." (Gupta)
- "It's abstraction for the sake of abstraction." (Gupta, on LangChain)
- "You can't possibly do streaming semantics on the lab side. It's an application level construct." (Gupta)
- "We reduced the CI/CD time to under I think like well under five minutes from 33 hours for like 90% of commits." (Gupta)
- "I got 82 freaking comments on it. 82 comments." (Gupta, on his first Microsoft code review)
- "If this is a thing that takes less than 10 or 15 minutes to do, do not file a ticket." (Gupta)
- "Just go do the thing that you want to do." (Dex)
- "Great leaders are right a lot... building a startup is about making the right bets." (Gupta, paraphrasing an Amazon principle)
- "A programming language is probably one of the most absurd startup ideas in the world." (Gupta)
- "I really really really like beautiful code. That's it." (Gupta)

## HABITS
- Interview for jobs every year but only leave when something is genuinely, dramatically better than now.
- Run your writing through many trusted people before publishing, rather than trusting your own first draft.
- Respond to users on Discord quickly, and patch a reported bug within fifteen minutes whenever possible.
- Use the plane test for conviction: excited founders code on flights; disengaged ones watch a movie.
- Ship a slow rollout with contingencies; never kill the old system before the new proves itself.
- Meet a willing early customer daily; solve their biggest problem, then find and solve the next.
- Add features users request directly into BAML rather than making each user reimplement the same logic.
- Take on the dishes work: do the unglamorous chore nobody else wants, and earn team goodwill.

## FACTS
- DE Shaw's roughly thirty-year-old Python codebase ran its CI/CD in about thirty-three hours before the optimization.
- The optimized pipeline ran under five minutes for roughly ninety percent of the company's daily commits.
- BAML took about seven months to reach one hundred GitHub stars, then grew to roughly 7,000.
- Gupta estimates writing fifty to one hundred thousand lines of code almost every year throughout college.
- Their Twitch-ads YC interview ended in six minutes when Michael Seibel asked whether they watched Twitch.
- The AI That Works podcast has run thirty-nine episodes and surpassed one hundred thousand YouTube views.
- BAML now has multiple Fortune 500s, a government agency, and startups actively writing its code weekly.
- Gupta interned at NASA using IDL, a Fortran-flavored language passing everything by reference, not by value.

## REFERENCES
- BAML / Boundary (the programming language for LLM functions), and its playground and JSON parser.
- Human Layer (Dex's company) and the "12-factor agents" write-up and conference talk.
- LangChain (the abstraction the founders reacted against); Zod for schemas.
- Bazel (Google build system, rejected); SVN and Git; CodeIgniter PHP and Python Django.
- IDL (NASA astrophysics language); C, C++, Rust, TypeScript, React.
- Y Combinator; Michael Seibel; the Paul Buchheit / Gmail early-users story.
- Ben Stansel blog post on the downsides of taking venture money.
- Employers referenced: Microsoft (Michael Gour, FIFA physics engine; manager Drew Seedley), Google (Face ID), DE Shaw, eBay, Meta, Amazon.
- PostHog (the analytics whose bill lapsed); Discord; the "day-to-day Texas" talk; the "AI That Works" podcast.

## ONE-SENTENCE TAKEAWAY
Wrap unreliable primitives, whether LLM calls or huge test suites, in a smarter typed layer.

## RECOMMENDATIONS
- Scope your test runs to the git diff so agent edit-test loops close in mere seconds.
- Model streaming LLM output as two types: a partial streaming shape and a final complete shape.
- Treat the model call as a typed primitive; put a resilient parser around its raw output.
- Reject tools your whole team can't learn; maintainability beats a marginal capability nobody else can support.
- Build the business you actually want now instead of a stepping-stone business to fund it later.
- Set a hard time-bounded bet on a struggling project and honor the deadline to force decisions.
- Do not build on platforms like LinkedIn or Twitch that will eventually copy or block you.
- Skip the ticket for sub-fifteen-minute fixes; decide immediately to do it or drop it right there.
