---
title: "Dates, Times, and LLMs #31"
videoId: l7txtbgCFGU
url: https://www.youtube.com/watch?v=l7txtbgCFGU
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1 (the reframe): Put a deterministic intermediate representation between the LLM and the answer.** The model should classify fuzzy intent into a structured data model (an absolute date, a duration string, a cron string, a SQL parse tree); your software compiles that into the exact result. It never does the math itself.
Why it is the spine: it subsumes almost every beat in the video (extract-dates-as-data-models, cron-string-plus-Python next-occurrence, the SQL and SVG generalizations, the eval-driven iteration loop).
VERDICT: 🔗 next-step video available (complements the structured-output foundations brief).

**Spine 2 (context engineering): Treat the LLM as a user living in one fixed timezone.** Normalize every user-keyed timestamp to their zone at the serialization boundary, so the model reasons in one consistent frame and spends zero "gas" on timezone conversion.
Why it stands alone: distinct central demo (a serialization-layer auto-converter plus the production Haiku self-correction log) and a distinct slot (context-engineering), so it is a separate video from Spine 1, not a sub-beat.
VERDICT: ❌ net-new video available.

## Summary + counts

BoundaryML's AI That Works workshop episode 31: Vaibhav and Dexter live-code a datetime evaluator, joined by Brian, exploring how LLMs handle dates, times, and timezones.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1 — the intermediate representation.**
The claim: do not ask an LLM to produce a precise value; ask it for a structure your code can deterministically compile into that value. Most people do the opposite: they prompt "what date is next Friday?" and trust the arithmetic. It looks fine in the demo, then breaks on boundary conditions, leap years, month ends, "two months from now," where being off by two days is a real bug. The mechanism has two steps. First, a probabilistic token predictor is unreliable at multi-step deterministic computation but reliable at classifying intent into a fixed shape; so you split the job. In the transcript the model emits a cron string and a tiny Python function ("convert_cron_to_datetime") computes the next occurrence. Second, that split makes every failure legible: it is either a shape-classification miss (cheap to eval) or a code bug (deterministic, testable). It generalizes cleanly to text-to-SQL, where Dexter argues you have the model emit a parse tree, then decompile it into the query, because "the logic in SQL is nonlinear." Where it goes wrong: the representation must be expressive (cron cannot say "two months from now") and must be one the model writes well (cron is common; a bespoke DSL may not be), and relative expressions need an injected anchor date or the structure is undefined.

**Spine 2 — the LLM as a fixed-timezone user.**
The claim: normalize every timestamp keyed to a user into that user's zone at the serialization layer, so the model never reasons about timezones. The default is to pass raw UTC server time into the prompt and hope the model converts; it then, in Vaibhav's words, spends "gas" on timezone math and gets "last night" or "tomorrow at 1am" wrong. The mechanism: when context mixes UTC and PT timestamps the model has genuinely incomplete information and cannot resolve a sub-24-hour relative window that straddles zones; pre-convert everything to one frame and the model reasons in a single consistent world at zero cost. Brian's framing is to "treat the AI almost as a user" in central time. It generalizes to internationalization (Dexter's lookup-table analogy, where display strings resolve at the display layer) and to memory and event bucketing (five-minute, hour, and day buckets that shift with the user's zone). Where it goes wrong: DST and the international date line leave you at most off by one day (forgivable); a production Haiku chain even self-corrected a UTC/PST mismatch in under a second, but paying that reasoning overhead on every call compounds failure probability, cost, and latency, so fix it once at serialization instead.

## 🎬 Proposed ACS videos

### 1. Stop Asking the Model to Compute. Ask It for a Blueprint.
- HOOK: Your LLM keeps getting dates wrong because you asked it to do math instead of describe intent.
- THE PROMISE: For anyone building an LLM feature that must output a precise value (dates, SQL, SVGs), you will learn to split the job so the model classifies intent and your code computes the answer, and stop shipping off-by-two-days bugs.
- THE SHAPE: (1) Show the naive prompt failing: "next Friday" returns garbage or an undefined P7D. (2) Introduce the intermediate representation: the model emits absolute-date OR relative-duration OR recurring-cron, never the final timestamp. (3) Software compiles: a small Python function turns the cron string into the next occurrence. (4) Generalize: text-to-SQL as a parse tree you decompile, and SVGs. (5) The rule: pick a representation that is easy for the model to write AND easy for software to deterministically compile.
- SPINE: 1
- SLOT: prompt-engineering › PE Foundations (sits next to structured-output); alternatively techniques › designing-interfaces.
- RELATIONSHIP: 🔗 complements "structured-output" (PE Foundations, scripted). That brief teaches how to get valid typed output from the model; this adds the design principle above it, that the typed output should be a deterministic intermediate representation software finishes computing, so do not re-teach JSON-schema mechanics, teach choosing a compile target.
- PROOF TO REUSE: the live cron-string demo ("I've actually never used a cron string ... convert cron to daytime"); Dexter's SQL parse-tree line, "creating some sort of intermediate thing that is easy for the LM to write and is easy for software to deterministically compile"; the P7D duration-string failure that shows why the representation must be expressive enough.

### 2. Treat the Model Like a User: One Timezone, Zero Timezone Bugs
- HOOK: Your agent gets "last night" wrong because you feed it UTC and hope it converts. Stop hoping.
- THE PROMISE: For anyone building a chat or agent feature over time-stamped data, you will normalize every timestamp to the user's zone at the serialization boundary so the model reasons in one frame and never wastes tokens or accuracy on timezone math.
- THE SHAPE: (1) The failure: mixed UTC and PT timestamps in context, model cannot resolve "last night." (2) The reframe: the LLM is a computation engine and timezone conversion is "a waste of gas." (3) The fix: a serialization-layer auto-converter where everything keyed to a user normalizes to their zone, both in and out. (4) The i18n analogy: a display-layer lookup table. (5) The proof: a production Haiku chain self-correcting a UTC/PST mismatch, and why paying that 5% overhead every call is a bug not a feature. (6) Limits: DST and date-line errors are at most off by one day (forgivable); recurrence editing is not, so build a UI.
- SPINE: 2
- SLOT: context-engineering (new video in the shipped class).
- RELATIONSHIP: ❌ net-new. The context-engineering class covers constructing context generally, but no inventoried video teaches pre-resolving deterministic facts (timezones) at the serialization boundary so the model spends zero reasoning on them. (Verify against the 13 shipped context-engineering titles, which are not in the local inventory.)
- PROOF TO REUSE: Brian's "treat the AI almost as a user ... normalize everything to central time"; Vaibhav's "the gas going to time zone computation is a waste of gas"; the Haiku reasoning chain that self-corrected UTC to PST "in under a second"; the off-by-one-day international-date-line worst case that users forgive.

## 📚 Full wisdom (reference)

**SUMMARY**
BoundaryML's AI That Works workshop episode 31: Vaibhav and Dexter live-code a datetime evaluator, joined by Brian, exploring how LLMs handle dates, times, and timezones.

**IDEAS**
- Dates in natural language are ambiguous: 'next Tuesday' shifts meaning depending on whether today is Monday.
- First extract dates as normalized data models before trying to understand their meaning within sentence semantics.
- Relative dates like 'next Friday' are undefined to the model without injecting a source anchor date.
- GPT-4 mini extracts absolute dates reliably but fails relative ones, defaulting nonsensically to P7D for Friday.
- Recurring events ('10am every Tuesday') are fundamentally different from single occurrences; the year becomes almost irrelevant.
- Represent recurrence as a cron string, then compute the next occurrence in software, not the model.
- Cron strings are almost always UTC because servers run them; make the data model timezone-aware optionally.
- Timezone should default null, resolving to the user's client-side zone unless explicitly stated in the input.
- Treat the LLM as a computation engine; spending its reasoning 'gas' on timezone math is wasteful.
- Build an intermediate representation easy for the LLM to write and easy for software to compile.
- For text-to-SQL, have the model emit a parse tree, then decompile that into the actual query.
- Superhuman handles dates beautifully using a massive regex parser, not an LLM, with a typing UI.
- Normalize every timestamp to the user's timezone at the serialization layer so the model stays consistent.
- 'Last night' is nearly impossible for a model given mixed UTC and PT timestamps in context.
- A production Haiku reasoning chain self-corrected a UTC-versus-PST mismatch in under a second while streaming back.
- Memory bucketing across time zones is genuinely hard; buckets may shift when the user changes zone.
- Recurrence editing (edit-this versus edit-all-future) is so painful that Brian won't trust an agent with it.

**INSIGHTS**
- There is no single data model for dates; each domain needs edge-case-specific models you design deliberately.
- The skill is splitting work: the model classifies fuzzy intent, deterministic code computes the exact answer.
- Date problems aren't hard; teams just never sit down to define their domain's specific edge cases.
- Design around when users get upset: daylight-savings errors are forgivable, but a wrong 'tomorrow' is not.
- Normalizing timezones correctly once at serialization means models don't reason about them, so systems just work.
- The intermediate representation flows in both directions: model-to-software on output, and software-to-model when constructing input context.
- The LLM is now backend logic that must share exact timezone rules with the display layer.
- Because errors self-correct occasionally, doing it right 90% of the time lets models recover the rest.
- Every extra reasoning step adds roughly 5% failure probability, cost, and latency to each single interaction.
- When a model can't reliably produce something token-by-token, give it a compilable structure it writes well.

**QUOTES**
- "Number one is inject today's date into the prompt." — Dexter
- "the way to handle dates very well is what you do is for your use case you go ahead and come out with a bunch of edge cases that you really care about" — Vaibhav
- "creating some sort of intermediate thing that is easy for the LM to write and is easy for software to deterministically compile into whatever the actual result is." — Dexter
- "It's like parsing the user's intent into something structured, some intermediate representation that then can be deterministically evaluated." — Dexter
- "it's just like almost interesting to treat the AI almost as a user" — Brian
- "I view the LM as kind of like a computation like engine of some kind and you can choose where the gas goes to and the gas going to time zone computation is a waste of gas." — Vaibhav
- "We just store everything in ETC and then normalize it on the way out of the API." — Brian
- "if you just let the model try and do the math of what the date is, at least as of right now, it doesn't work really well." — Vaibhav
- "they're capable of of reasoning around time zones, but usually you just like don't want them to have to." — Brian
- "None of this stuff sounds untenable. People just need to sit down, define edge case, and just like understand where the user going to expect it to work and where does it break." — Vaibhav
- "instead of letting your user shoot themselves in the foot with a broken feature, just don't ... if you don't have confidence that you can go ship it, just don't do it." — Brian
- "if you edit and move it one day forward and you say edit all future events, that actually means move all the future events one day forward so they're all still a week apart." — Dexter

**HABITS**
- Always write a separate test case for every date edge case before trusting the model's output.
- Inject today's date as an explicit source anchor into every single prompt that handles relative dates.
- Use small cheap fast models like GPT-5 Nano or Gemini Flash for these simple date-extraction tasks.
- Use voice input to dictate detailed function specifications to a coding agent working in the background.
- Ask the coding agent (Cursor) to explain unfamiliar formats like cron strings before actually using them.
- Add extra metadata and descriptions to confusing type fields when the model misinterprets your data model.
- Let the agent change the account's stored timezone itself when a user travels to another region.
- Store everything in UTC and normalize it to the user's zone only on the way out.
- Convert display times only in the browser, right on the display side, not the data layer.

**FACTS**
- In cron syntax, the day-of-week field uses zero for Sunday, one for Monday, two for Tuesday.
- Cron expressions are almost always interpreted in UTC because they typically run on servers, not clients.
- ISO 8601 duration strings represent spans like P7D for seven days and P1D for one day.
- Superhuman shipped natural-language date parsing using a regex parser before LLMs existed, and still uses it.
- Anthropic's Haiku returned a full timezone-reasoning chain in under one second while streaming, in real production.
- The speakers previously built a Slack competitor with a calendar app before pivoting to build BAML.
- Brian's memory system buckets events at five-minute, hourly, and daily granularities across multiple different time zones.
- The Google Calendar API's recurrence data model is notoriously unpleasant to work with, per the speakers.
- Daylight-savings transitions and the international date line can cause off-by-one-day errors in hourly-to-daily event bucketing systems.

**REFERENCES**
- BoundaryML "AI That Works" workshop series (episode 31)
- BAML (BoundaryML's language)
- OpenAI GPT-4 mini; GPT-5 Nano; Google Gemini Flash
- Anthropic Claude Sonnet 4.5 and Claude Haiku
- Cursor (coding agent)
- Superhuman (email app)
- Google Calendar and the Google Calendar API; Google Docs
- ISO 8601; cron; Python; uv
- Participants: Vaibhav (host), Dexter (co-host), Brian (guest, applied AI lab); chat contributor Elizabeth

**ONE-SENTENCE TAKEAWAY**
Have the LLM emit a compilable data model; let deterministic software compute the exact answer.

**RECOMMENDATIONS**
- Enumerate the date edge cases your specific domain actually hits, then design one data model each.
- Never let the model do date arithmetic; emit a cron or duration string and compute deterministically.
- Inject a source anchor date so relative expressions like 'next Friday' become computable from something concrete.
- Normalize every user-keyed timestamp to their timezone at serialization, so the model never touches any conversion.
- For high-stakes dates like contract review, force every date through a normalization pipeline, not model math.
- Default timezone to null and resolve to the user's client zone unless explicitly provided in input.
- For recurrence editing, build a dedicated UI instead of trusting an agent to modify chains correctly.
- Test leap years, month boundaries, and daylight savings explicitly; these boundary conditions silently break date math.
- If you can't ship a date feature confidently, don't ship it; a broken feature harms users.
- Consider a regex-parser autocomplete like Superhuman's when you fully control the date-entry UI instead of chat.
