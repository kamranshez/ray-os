---
title: "Getting Tone Just Right with LLMs #12"
videoId: HsElHU44xJ0
url: https://www.youtube.com/watch?v=HsElHU44xJ0
date: 2026-07-01
status: posted
source: "BoundaryML / AI That Works (Vaibhav, Dexter, guest Kyle)"
---

# The one idea worth a video

**1. Getting tone right is a data-assembly problem, not a prompting problem.** You cannot phrase your way to a good email; you get the factual data (links, titles, dates, summary) correct first, and only the small content middle actually needs tone work.
VERDICT: covered already (context-engineering "The Prompt Isn't the Problem"). Deep-dive kept for context, no new video.

**2. The flexibility you give an LLM is a deliberate dial, and for the parts you already know cold you should remove the choice entirely.** They refused to make PR creation a tool call because they only ever touch two files, so they hardcoded it instead of prompt-wrangling a general agent.
VERDICT: next-step video available (complements "Boxing the Model In").

**3. Split generation into a content pass and a separate formatting pass.** One call drafts the content in a loose structured shape (fragments allowed); a second call only reshapes it into a coherent email and adds no new content.
VERDICT: net-new video available.

**4. When a structured field underperforms, reshape the schema, do not reword the prose.** Turning quick_recap from a string into a string array produced better recaps than any amount of English tweaking, because the schema is itself a large part of the prompt.
VERDICT: next-step video available (complements "Structured Output").

---

# Summary

BoundaryML's Vaibhav and Dexter rebuild their AI content pipeline live, showing that getting email tone right depends on data assembly, pipeline design, and model choice.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 1 covered

---

# 🔬 Deep dive

## Spine 1 - Tone is a data-assembly problem, not a prompting problem (COVERED)

The claim: an email's tone is mostly downstream of getting the right data into the right slots, not of clever wording. This is non-obvious because the instinct when output is bad is to rewrite the prompt, add all-caps rules, and reach for a "magic" phrasing. The mechanism is a two-step chain: first, if the factual data is wrong (a broken YouTube link, "hello first name", a wrong Luma date) the reader rejects the whole thing regardless of phrasing, so those are catastrophic and trust-destroying; second, once the links, titles, dates and one-line takeaway are plumbed correctly, the only part that genuinely needs tone tuning is the narrow content/summary middle. As Vaibhav puts it, "if the factual data is wrong, the tone doesn't matter." It generalizes cleanly to any templated document: invoices, onboarding sequences, status reports, where retrieving the correct fields dominates prose polish. Where it goes wrong: even with perfect data, trivially prompting a model rarely nails the middle, so you still need model selection and decomposition; and over-focusing on data can let you neglect the genuinely hard content-to-quality problem. Gap: ACS already teaches this as "The Prompt Isn't the Problem", so this spine earns no new video.

## Spine 2 - The flexibility given to an LLM is a deliberate dial

The claim: on every LLM pipeline you consciously choose a point on a spectrum from hardcoding everything to full agent autonomy, and for the slices whose behavior you already know exactly you should give the model zero flexibility. This runs against the prevailing advice to "give the model a goal and get out of the way." The mechanism: because they know their pipeline only ever modifies two README files, turning PR creation into a tool call would just add an unreliable decision step, which they would then fight by growing the prompt into all-caps "you must only ever create these files" rules. So they hardcode the known part, let the LLM do only what it is good at (generate the READMEs), and own everything else. The lever underneath is "the input span of the problem": narrow the span and you shrink how much behavior you must engineer around. It generalizes to agent tool design broadly, deciding which actions become tools versus fixed code. It goes wrong when you over-hardcode: the pipeline becomes brittle and non-general, so the real skill is placing the line and moving it as scope expands. Gap: complements "Boxing the Model In."

## Spine 3 - Split generation into a content pass and a formatting pass

The claim: rather than one prompt that must nail facts, structure and tone at once, use two calls. Call one (generate the draft) produces the content in a loose structured shape where fragments and incomplete sentences are acceptable; call two (generate the email) turns that structure into a coherent email and is forbidden from adding new content. This is non-obvious because the two instincts are a single mega-prompt or a deterministic hand-glued template. The mechanism: a single call carries the whole burden and tends to miss tone every time, while the deterministic template reads like mad libs because the content is too dynamic to slot cleanly; splitting lets each call do one job, and the second does the one thing LLMs reliably do, make prose coherent, so neither call is overloaded. It generalizes to slide decks, PR descriptions, and reports: separate "what to say" from "how to say it." It goes wrong through added latency and cost, and the formatting call can still drift or reintroduce hallucinated fields, so you must explicitly bar it from inventing content. Gap: net-new, no ACS video teaches this content-pass / format-pass decomposition.

## Spine 4 - Tune the schema, not the prose

The claim: when a structured field underperforms, the highest-leverage fix is usually to reshape the output schema (string to a string array, add a bounded "at most 4-10 words" description field, split a field into sub-fields) rather than reword the English instructions. It is non-obvious because prompt-optimizer tools like DSPy iterate on the middle prose, and people picture "the prompt" as only the instruction text. The mechanism: the schema is itself a large and increasingly complex part of the prompt, and its shape dictates what the model commits to. An array forces several discrete recaps instead of one mushy string; a length-bounded description field constrains output without a sentence of instruction. So restructuring often moves quality more than rewording, and as programs grow the schema dominates the prompt. It generalizes to any structured extraction, classification, or form-filling task where intent lives in field names, types and enums. It goes wrong as schema sprawl: the structure gets sophisticated fast and hard to navigate, and where to place a given instruction (field description versus top versus bottom) is itself a search that DSPy-style tools try to automate. Gap: complements "Structured Output."

---

# 🎬 Proposed ACS videos

## Pitch 1 (net-new)

TITLE: Generate the Content, Then Generate the Email: The Two-Pass Prompt
HOOK: Stop trying to write one perfect prompt that nails facts, structure, and tone all at once.
THE PROMISE: For anyone generating documents with an LLM, you will learn to split one unreliable mega-prompt into two calls that each do one job well.
THE SHAPE:
1. Show the failure: a single prompt asked for a whole toned email, and the tone was off every run.
2. Introduce the split: call one drafts content in a loose structured shape (fragments and incomplete sentences allowed).
3. Call two only reshapes that structure into a coherent email and is forbidden from adding content.
4. Contrast with the deterministic hand-glued template that reads like mad libs, and show why dynamic content needs the second LLM pass.
5. Cover the costs: extra latency, and guarding the formatting call against reintroducing hallucinated fields.
SPINE: Spine 3.
SLOT: Prompt Engineering > Core Techniques (sits beside 07 Structured Output and 10 Iterative Refinement).
RELATIONSHIP: net-new. ACS teaches structured output as "schema is a prompt" but nothing teaches decomposing generation into a content pass and a formatting pass.
PROOF TO REUSE: the two BAML functions generate_email_draft and generate_email; the "mad libs" line ("no one would actually send mad lib stuff"); the point that the formatting call "doesn't add new content, it just makes it coherent."

## Pitch 2 (complement)

TITLE: The Flexibility Dial: When to Hardcode Instead of Handing It to the Agent
HOOK: The advice is "give the model a goal and get out of the way", but sometimes the right move is to give it no choice at all.
THE PROMISE: For engineers building LLM pipelines, you will get a decision axis for how much freedom to hand the model on any given step.
THE SHAPE:
1. Draw the spectrum: hardcode everything on one end, full agent autonomy on the other.
2. The worked case: they refused to make PR creation a tool call because they only ever modify two files.
3. Show the failure mode of the flexible version: a two-sentence prompt that grows into all-caps "you must only ever" rules.
4. Introduce "the input span of the problem": narrow the span, shrink what you must engineer.
5. The triad: automate with AI, automate with code, automate manually, and choose by time payoff.
SPINE: Spine 2.
SLOT: Prompt Engineering > Letting the Model Lead (directly adjacent to 01 Boxing the Model In).
RELATIONSHIP: complements "Boxing the Model In". That video teaches that a capable model does not need your rigid scaffolding, so stop over-constraining. This adds the dual: for the deterministic slices you already know cold, remove the choice entirely and hardcode, and here is the axis for placing the line. Do not re-teach the anti-over-engineering point; open by acknowledging it, then flip it.
PROOF TO REUSE: "we as a team always get a choice of how much flexibility we give the LM"; the PR tool-call refusal; "if you already know exactly what should happen, let the LM do what it does well"; "use more AI than you think and use less AI than you think at the same time."

## Pitch 3 (complement)

TITLE: Change the Schema, Not the Prompt
HOOK: Your bad output is not a wording problem. It is a shape problem.
THE PROMISE: For anyone using structured outputs, you will learn to debug quality by reshaping the schema before touching a single word of the instructions.
THE SHAPE:
1. The bad recap: quick_recap was a plain string and kept coming out weak.
2. The fix that was not a reword: change it to a string array, and recaps improve.
3. Generalize the moves: add a bounded description field ("at most 4 to 10 words"), or split a field into title plus description.
4. The argument against prose-only optimizers (DSPy): they navigate the middle chunk and overlook that the schema dominates a complex prompt.
5. The limit: schema sprawl, and the open question of where a given instruction should live.
SPINE: Spine 4.
SLOT: Prompt Engineering > Core Techniques (next step after 07 Structured Output).
RELATIONSHIP: complements "Structured Output". That video teaches that a schema is a prompt in disguise and that format reshapes what the model says. This adds the iterative move: reshape the schema as your primary debugging and optimization loop. Do not re-teach "the schema is a prompt"; assume it and build the loop on top.
PROOF TO REUSE: the string-to-array recap fix; "the prompt itself is comprised of a giant schema that is very very complex"; the DSPy exchange about tuning "the middle chunk of the prompt"; the "at most 4 to 10 words" description-field example.

Also note: this is a latent spine. The video treats it in one rich exchange, so the eventual video needs extra sourcing on schema-as-prompt-surface (the existing Structured Output script and BAML docs are good starting points).

---

# 📚 Full wisdom (reference)

## SUMMARY
BoundaryML's Vaibhav and Dexter, with guest Kyle, rebuild their AI content pipeline live, showing that getting email tone right depends on data assembly, pipeline design, and model choice.

## IDEAS
- Getting tone right is mostly assembling correct data into correct slots, not writing a cleverer prompt.
- If the factual data is wrong, the tone does not matter because readers reject it immediately.
- They split email generation into two calls: one drafts structured content, the other rewrites it coherently.
- The second formatting call adds no new content; it only reshapes fragments into a flowing email.
- Changing quick_recap from a string to a string array produced much better summaries than reprompting did.
- On every LLM pipeline you choose where to sit between hardcoding everything and full agent autonomy.
- They refused to make PR creation a tool call because they always modify exactly two files.
- If you know exactly what should happen, do not route it through an LLM at all.
- Context engineering means passing a curated subset via a custom serializer, not the raw event object.
- They send only the next ten Luma events, stripping unused fields before the model sees them.
- Random tokens like UUIDs are not in training data, so models copy them unreliably under load.
- Replace native long IDs with short labels like event_123456 so the model handles one fewer thing.
- For a fake placeholder link, use something realistic so the model does not try substituting it.
- Gemini handled long-context transcript timecodes far better than GPT-4o, likely from heavy YouTube training data exposure.
- Gemini ignores system messages in practice; it obeys the most recent tokens placed at the bottom.
- They embed Gemini instructions at the very bottom, which shows up as a second user message.
- A too-large prompt buries your instructions inside the transcript, so the model loses track of them.
- Dumping the transcript first and the instructions last noticeably improved the answer quality on Gemini calls.
- Deterministic work like sorting events by start time should be plain code, not an LLM call.
- They use a tiny cheap model for the easy next-event matching task and stop overthinking it.
- The LLM superpower is being mostly right fast, letting you ship without perfect deterministic code everywhere.
- The goal of building AI pipelines is good value for time invested, not total automation everywhere.
- Copying whiteboard screenshots manually beats building an Excalidraw integration that saves only thirty seconds each week.
- MCP is not a replacement for SDKs when building production agents as shipped products you sell.
- Your app should implement an MCP client so users can extend it with new capabilities themselves.

## INSIGHTS
- Data correctness gates tone: no prompt can rescue an email built on wrong links and titles.
- Flexibility given to an LLM is a design dial, not a default; choose it deliberately per-task.
- Splitting content generation from formatting lets each call do the one job it reliably performs well.
- The output schema is a hidden prompt; reshaping its structure often beats rewording the English instructions.
- Prompt optimizers that only tune middle prose ignore that the schema dominates an increasingly complex prompt.
- Model choice is empirical: try several, keep whichever nails your specific task cheaply and reliably enough.
- Narrowing the input span of a problem shrinks how much behavior you must engineer around it.
- Automate with AI, with code, or by hand, choosing whichever gives the best time payoff here.
- Drawing the dependency diagram first is what let them parallelize and split the pipeline work cleanly.
- Human-in-the-loop trust beats full automation: they would rather edit manually than ship an obviously bad result.

## QUOTES
- "The goal of projects when you build AI pipelines is not to automate everything." (Vaibhav, BoundaryML)
- "If we hold off on deploying a system until everything is perfect, then we'll never get anything out." (Vaibhav)
- "If the factual data is wrong, the tone doesn't matter." (Vaibhav)
- "It's unlikely that you can get to the perfect tone with just prompting." (Vaibhav)
- "Whenever we build an LM pipeline, we as a team always get a choice of how much flexibility we give the LM." (Vaibhav)
- "If you already know exactly what should happen... let the LM do what it does well." (Vaibhav)
- "It's just the token probability thing. Tokens that are random are just not in the data set of the model." (Vaibhav)
- "This is all just like engineering the right context." (Dexter)
- "Everything that you pass to an LM, whether it's the prompt or the agentic history or memory or rag, it's all just tokens to the LM." (Vaibhav)
- "Use more AI than you think and use less AI than you think at the same time." (Vaibhav)
- "Now copy and paste is just an AI feature. It is not a copy and paste feature." (Vaibhav)
- "MCP is not... very good as like a replacement for traditional SDKs." (Kyle)
- "Good AI tools have an autonomy slider." (Vaibhav, citing Karpathy's YC talk)
- "Full agent mode without being able to stop it and correct course along the way is really really really bad." (Vaibhav)
- "There's no prompt that will do that magically. At least not yet." (Vaibhav)

## HABITS
- They draw a dependency diagram before coding, mapping exactly which pieces each output needs upstream first.
- They write small tests for prompt functions, checking edge cases like when no matching event exists.
- They try multiple models on a task before committing, comparing GPT-4o, Claude, Sonnet, and Gemini outputs.
- They record every input-output pair to generate tests and evals at the per-prompt level later automatically.
- They deliberately do trivial data prep manually when coding it would cost more than it saves.
- They keep colons out of BAML by convention, a syntax choice they now admit was wrong.
- They validate generated links and would find-replace a realistic placeholder link with the real one afterward.
- They use Claude Code hooks to ring a bell when an agent session finishes or waits.
- They budget five to ten hours weekly automating content, accepting the tradeoff against manual effort gladly.

## FACTS
- Gemini does not support system messages the usual way; it places them in a separate part.
- Supersonic, from the Kit folks, creates GitHub pull requests in a single line of code reliably.
- Kit is a Python toolkit for reading remote repositories, useful for building any GitHub automation pipeline.
- Karpathy, in his YC talk, described good AI tools as having an autonomy slider across modes.
- SQL injection was solved by escaping inputs, but prompt injection has no equivalent reliable escape yet.
- Claude Code hooks include pre-tool-use, post-tool-use, and notification events that developers can script for themselves now.
- Gemini appears trained heavily on YouTube data, explaining its unusually strong transcript timecode generation ability here.
- Gemini Flash is cheap and free enough that they chose it once it solved their task.

## REFERENCES
- BAML (BoundaryML's structured-output language) and BoundaryML's cloud eval product.
- Models: Gemini (2.5, Flash), GPT-4o and GPT-4o mini, Claude, Sonnet; Vertex AI.
- Tools and services: Luma, Zoom, GitHub, Excalidraw, Supersonic (single-line PR creation), Kit (remote-repo toolkit).
- DSPy (prompt optimization framework); MCP (Model Context Protocol), and MCP clients/servers.
- Claude Code (hooks: pre-tool-use, post-tool-use, notification; slash commands); Cursor (tab autocomplete).
- Andrej Karpathy's YC talk (the "autonomy slider" idea).
- HumanLayer merch (merch.layer.dev / human layer t-shirt).
- The "AI That Works" show; prior episodes on evals, on MCP, and "cracking the prompting interview."

## ONE-SENTENCE TAKEAWAY
Getting tone right is mainly a data-assembly and careful pipeline-design problem, not a cleverer-prompt one.

## RECOMMENDATIONS
- Before prompting for tone, audit whether every link, title, date, and summary is factually correct first.
- Split any generation pipeline into a content pass and a separate formatting pass that adds nothing.
- When a structured field underperforms, change its schema shape before you rewrite the prose instructions again.
- Decide explicitly, per task, how much flexibility to hand the LLM versus hardcoding the behavior yourself.
- Do not wrap known fixed behavior in a tool call; hardcode it and skip the wrangling.
- Send the LLM a curated subset via a custom serializer instead of the whole raw object.
- Try several models on your task and keep whichever one nails it most cheaply and reliably.
- Swap raw UUIDs for readable labels like event_1 to reduce the model's cognitive load considerably here.
- For long-context transcript tasks, reach for Gemini and place your instructions at the very bottom instead.
- Record input-output pairs now so you can later generate per-prompt evals and regression tests almost automatically.
