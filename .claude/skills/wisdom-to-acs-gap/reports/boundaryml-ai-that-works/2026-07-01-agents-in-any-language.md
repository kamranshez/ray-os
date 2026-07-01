---
title: How to Build AI Agents That Work in Any Language
videoId: -gFdtc-HbOY
url: https://www.youtube.com/watch?v=-gFdtc-HbOY
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1: Normalize every language to one evaluable English pipeline wrapped with translation-in and translation-out units, instead of forking a full pipeline per language.** It subsumes the whole episode: the eval-matrix explosion argument, the voice-agent STT/TTS analogy, the DAG structure, the mixed-language win, and the fast-classifier front door all hang off this single reframe.
VERDICT: net-new video available.

**Spine 2 (de-merged, latent): Your output schema is part of the prompt, so field names silently steer the model.** Naming a result field `reply_english` forced English replies even when the rest of the pipeline was language-agnostic. Distinct demo, distinct slot, a genuinely different video from Spine 1.
VERDICT: next-step video available (complements the planned structured-output foundations).

Also film-able (not deep-dived): "throw tokens at the smartest model until it is cheaper to engineer than to keep spending compute" is a real decision heuristic the hosts repeat, but it overlaps the school's existing cost/optimization philosophy (scrappy-copy-first, high-level-strategy-low-level-details) and gets no distinct demo here, so it stays a beat rather than a spine.

---

# Summary + counts

Vaibhav and Dexter of BoundaryML's AI That Works podcast build multilingual AI agents by normalizing user input to one English pipeline wrapped with translation units.

Counts (one per promoted spine): 1 net-new, 1 complement, 0 partial, 0 covered.

---

# Deep dive

## Spine 1 - Normalize-and-wrap, do not fork

The claim: support any language with ONE canonical English pipeline, wrapping it in cheap translate-in and localize-out units, rather than maintaining a separate pipeline per language. It is non-obvious on two fronts. Most people assume multilingual models already solve this; and the people who do build for it instinctively fork a French or Hindi copy of the whole system. Both are wrong. The mechanism: a bespoke pipeline packs the model with an English system prompt, English tool definitions, and English instructions, so statistically it answers in English even to French input, because the steering burden now lives in your prompt, not the user. Forking per language then explodes your eval matrix, demands translated prompts and tools, and starves the non-English pipelines of updates, so French users perpetually lag. Wrapping instead keeps one deeply evaluable pipeline, and the translation shells have narrow inputs that are easy to eval. It generalizes cleanly to voice agents (audio to speech-to-text to a text agent to text-to-speech to audio, never fragile audio-to-audio) and to any modality normalization. It goes wrong when you cannot eval translation quality in a language you do not speak: you must either trust the model at face value or hire native evaluators, and you must keep the original message to preserve tone.

## Spine 2 - The schema is part of the prompt

The claim: output field names are prompt content, so naming a field `reply_english` silently forces English replies even when the surrounding pipeline is language-agnostic. It is non-obvious because people believe behavior is changed only by editing the prompt body, and treat the output schema as a neutral container for results. It is not. The mechanism: the model reads each field name as an instruction about what that field should contain, so `reply_english` tells it the reply must be English. That instruction competes with, and here overrides, an explicit "reply in the user's language," because resolving competing instructions relies on instruction-following, which always shaves the success rate. One word derails the whole system, and it is easy to miss precisely because you were staring at the prompt, not the schema. It generalizes to every structured-output agent: a field named `is_urgent` biases classification toward urgency, `summary_short` biases length, tool-argument names bias tool use. The schema leaks intent everywhere. It goes wrong if you overcorrect by stripping all semantic field names, which throws away the free steering good names buy you; the real fix is deliberate naming plus evals, not neutral names.

---

# Proposed ACS videos

## 1. Make Your Agent Work in Any Language Without Forking Your Pipeline

- HOOK: Your English pipeline will answer a French user in English. Here is the one-layer fix.
- THE PROMISE: For engineers shipping customer-facing agents, after this you can support any language with a single pipeline you can still eval, instead of maintaining ten.
- THE SHAPE:
  1. Show the failure live: pass Hindi into an English pipeline, watch it reply in English.
  2. The wrong fix: parallel per-language pipelines, and why the eval matrix and translation-agency cost explode.
  3. The pattern: translate-in, run one English agent, localize-out, taught through the voice-agent STT/TTS analogy.
  4. Keep the original message around to handle mixed Hindi+English input and match the user's tone.
  5. Prove it: disable the translation layer (force the detector to always return true) and watch it break.
- SPINE: 1
- SLOT: Techniques class, new "Normalize to Your Pipeline" pattern video (adjacent to task-shaped-wrappers, one-pattern-per-thing).
- RELATIONSHIP: net-new. The catalog has no multilingual/i18n video and no voice-agent architecture video. The closest backlog items, task-shaped-wrappers and designing-interfaces, cover wrapping tasks and interfaces, not language normalization, so nothing here re-teaches this.
- PROOF TO REUSE: the voice-agent line ("don't use non-English to LM to non-English, use non-English to English to LM to English to non-English"); the always-return-true ablation that proves the layer is load-bearing; the 99% vs 99.99% reliability framing with the GitHub status-page example; the live Claude Code build driven by pasting the architecture SVG.

## 2. Your Output Schema Is Part of the Prompt

- HOOK: One field name, `reply_english`, quietly overrode every instruction in the pipeline. Here is why schema field names steer the model.
- THE PROMISE: For anyone using structured output, after this you can debug an agent that ignores your instructions because its own schema is fighting them.
- THE SHAPE:
  1. The bug: the agent keeps replying in English despite a language-agnostic prompt.
  2. The reveal: the result field was literally named `reply_english`.
  3. Why: the model reads field names as instructions, so the schema is prompt.
  4. Generalize: `is_urgent`, `summary_short`, and other names that leak intent into the output format.
  5. The fix: deliberate naming plus evals, rename the field and re-run to see behavior flip.
- SPINE: 2
- SLOT: Prompt Engineering class, structured-output (PE Foundations).
- RELATIONSHIP: complements the planned "structured-output" foundations brief. That brief teaches how to GET structured output; this teaches that the field names in the schema are themselves prompt content that silently steers behavior, which is the debugging move AFTER you already have structured output working.
- PROOF TO REUSE: "the schema is part of the prompt because what you name the fields tells the model what they should be"; the one-word `reply_english` derail that survived even an explicit reply-in-user-language instruction; "you can accidentally leak intent... into your output format and the model is going to read that."

---

# Full wisdom (reference)

## SUMMARY
Vaibhav and Dexter of BoundaryML's AI That Works podcast build multilingual AI agents by normalizing user input to one English pipeline wrapped with translation units.

## IDEAS
- Most LLMs handle many languages, but bespoke pipelines full of English steering statistically force English-language responses.
- A ChatGPT chat carries most steering from the user; a bespoke pipeline carries most burden itself.
- Building an application shifts steering burden from the user onto your prompt, like terminal versus UI.
- One approach: build a fully parallel French pipeline, classifying input upfront to route between per-language copies.
- Parallel per-language pipelines explode your eval matrix and demand translated prompts, tools, and paid translation agencies.
- A miscellaneous-language pipeline injects one instruction: reply in the user's preferred language, relying on instruction-following alone.
- Instruction-following, the last capability models gained, reliably lowers pipeline success rate versus leaning on native autocomplete.
- Track languages appearing in your miscellaneous pipeline; when one crosses a threshold, promote it to dedicated.
- The recommended architecture: keep one English pipeline, wrap it with translation-in and translation-back units around it.
- This mirrors voice agents: audio-to-speech-to-text, then text agent, then text-to-speech, avoiding fragile direct audio-to-audio models entirely.
- Keeping the original message alongside the translation handles mixed Hindi-English input and preserves the user's tone.
- Model the flow as a DAG: translate, capture intent, run agent, then localize the response back.
- Naming an output field reply_english silently forces English replies even when you asked for another language.
- The output schema is part of the prompt; field names leak intent the model silently obeys.
- A fast heuristic counting common English words can skip translation entirely for the majority English-speaking users.
- Forcing the English-detector to always return true proves the pipeline breaks: Hindi input returns English output.
- Small translation units have narrow input ranges, making them far easier to eval than the agent.

## INSIGHTS
- Reliability, not capability, is the real multilingual problem: 99% versus 99.99% separates trustworthy software from broken.
- Decomposing a pipeline into evaluable units is software engineering: split a 500-line function into testable pieces.
- You cannot build evals for languages or domains you personally do not understand well enough yourself.
- Without native evals you must either trust models at face value or hire native-speaking human evaluators.
- Spend tokens on the smartest model until scale makes engineering optimization cheaper than the compute itself.
- Good evals shrink fragility: guaranteed on understood inputs, even when translation quality stays unverifiable to you.
- English and Chinese dominate model accuracy purely because their internet training corpora dwarf every other language.
- Under-served languages mirror neglected platforms: French users lag like apps that patch Windows a month late.
- Agentic engineering is still software engineering: assemble small prompt units and keep composing more of them.

## QUOTES
- "It's about how much confidence do you want in your end user happiness?" - Vaibhav
- "The difference between software that's right 99% of the time and 99.99% of the time is like something you can actually trust and use versus something that feels constantly broken." - Dexter
- "You actually build your whole pipeline in English." - Vaibhav
- "Don't use non-English to LM to non-English, use non-English to English to LM to English to non-English." - Vaibhav
- "You can't build evals for things you don't understand." - Vaibhav
- "It's just like breaking down a 500 line function into smaller functions that are testable." - Dexter
- "Your engineering time is usually worth a lot more than the tokens you're spending until you have like millions of users." - Vaibhav
- "The schema is part of the prompt because what you name the fields tells the model what they should be." - Dexter
- "LLMs are actually just really good spell checkers." - Dexter
- "If you're editing your prompt and you're not running tests, why are you just making life hard?" - Vaibhav

## HABITS
- Vaibhav pastes architecture diagram images directly into Claude Code, finding it faster than iterating on HTML.
- Dexter prefers having Claude generate HTML mockups and iterating back and forth before writing real code.
- They never fix typos before prompting, trusting models as excellent spell checkers to interpret their intent.
- Vaibhav pastes every customer complaint into Claude, asks for a new eval, then iterates until passing.
- They always run tests while editing prompts, treating skipping evals as needlessly making their life harder.
- Vaibhav maintains his own hand-built link shortener despite it being tedious to add new links manually.
- Vaibhav uses UV to initialize Python projects quickly during live coding demonstrations on the show regularly.
- He no longer codes in Cursor but still demos in it because visuals aid conceptual explanation.

## FACTS
- GitHub's status page shows 99.82% uptime is unacceptable, illustrating tiny percentages matter enormously at real scale.
- Daily's founder Kwindla Kramer notes speech-to-speech models still underperform text-based speech pipelines despite being highly desirable.
- Esperanto, a constructed language invented by one person, served as their example of a bespoke language.
- In India, many people naturally mix Hindi and English together within a single spoken sentence regularly.
- Instruction-following was the last major capability language models gained, and it drove ChatGPT's massive breakout success.
- ElevenLabs now offers a full agent pipeline, wiring a system prompt and MCP tools together automatically.
- The English internet is by far the largest training corpus, with the Chinese internet likely second.
- Newer models hide raw thinking traces behind summaries, partly to prevent competitors distilling and cloning them.

## REFERENCES
- AI That Works podcast by BoundaryML (youtube.com/boundaryml)
- BAML, BoundaryML's agent-first programming language (skills add boundaryml/baml)
- 12-factor agents (the input-to-specific-output workflow philosophy referenced)
- Claude Code (used for the live build; Haiku, Sonnet, Opus models)
- Cursor (used to display code during the demo)
- ChatGPT / OpenAI (the general-purpose-agent contrast)
- ElevenLabs API (text-to-speech, speech-to-text, full agent wiring)
- Daily and Kwindla "Quinn" Kramer (voice-agent architecture)
- GitHub status page (the 99.82% uptime example)
- UV (Python project initialization)
- GEPA (referenced as "the very expensive GEPA" prompt optimization)
- Mistral (French-language models), DeepSeek (thinking traces), GPT-OSS 12B (the smaller model to optimize toward)

## ONE-SENTENCE TAKEAWAY
Normalize every language to one evaluable English pipeline wrapped with translation, never fork parallel pipelines.

## RECOMMENDATIONS
- Build one English pipeline and add cheap translation units front and back instead of forking per-language.
- Store the original message alongside its translation so you can restore tone and handle mixed-language input.
- Audit your output schema field names; rename anything like reply_english that silently steers the model wrong.
- Write a fast English-word heuristic to skip translation latency for your majority English-speaking user base entirely.
- Prove a component matters by disabling it and watching the whole pipeline visibly break under test.
- Decompose large agents into small pipeline units with narrow inputs you can actually build evals for.
- Default to the smartest model, only engineering cheaper alternatives once token cost genuinely exceeds engineering time.
- Paste customer complaints straight into Claude, generate a new eval, then iterate prompts until tests pass.
- Paste architecture diagram images directly into Claude Code; it now reads SVGs and PNGs reliably well.
