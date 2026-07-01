---
title: How to Automate Complex Workflows with Claude
videoId: U5Gssat8IUw
url: https://www.youtube.com/watch?v=U5Gssat8IUw
date: 2026-07-01
status: posted
---

# The one idea worth a video

**Spine 1 (net-new): Automate incrementally and permanently gate only the irreversible "one way doors."** Start with a prompt that lists everything including "STOP, human does this," fill in automations over time, and keep humans on anything you cannot undo. This is the spine because it subsumes the human review beats, the "90% is a win," and the brittleness lesson.
VERDICT: net-new video available.

**Spine 2 (complement): Claude Code as the top-level orchestrator, a "front end for CLIs."** A Sonnet-driven command drives a pipeline of deterministic scripts and offloads each hard-AI subtask to a separate BAML function with its own context window. This is a spine because the whole pipeline (CLIs, tool-calling model, interactive prompts, offloaded reasoning) hangs off it.
VERDICT: next-step complement video available.

**Spine 3 (complement): Let the browser agent learn the clicks, then bake them into deterministic code.** When a service has no affordable API, use an agentic browser to discover the workflow by screenshot-then-click, then crystallize the learned interactions into deterministic automation the model no longer drives. Distinct central demo, so it stands as its own spine.
VERDICT: next-step complement video available.

---

# Summary

Dex (HumanLayer) and Kevin Gregory demo how they automated the AI That Works podcast pipeline using Claude Code commands orchestrating deterministic CLIs and BAML functions.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

---

# 🔬 Deep dive

## Spine 1 — Automate incrementally, gate the one way doors

The claim: do not chase push-button, 100% automation; build a prompt that lists every step including "STOP, human does this," fill in automations over time, and keep humans permanently on the steps you cannot undo. The non-obvious part is that the all-or-nothing instinct ("one command and everything happens") is exactly what stops people from starting, and that fully automating an irreversible step is a liability rather than a goal. The mechanism is reversibility as the sorting key: reversible steps (draft an event, generate a graphic) can auto-run because a mistake costs nothing, while one-way doors (a mass email to thousands, a public LinkedIn post) get gated because a mistake is public and permanent. Automating 90% removes most of the toil while a 10% review still catches the embarrassing error, and building incrementally keeps the system shippable at every stage. This generalizes cleanly to deployment pipelines, where reversible staging deploys auto-run but the irreversible prod release or customer announcement needs a human gate. It goes wrong when brittle bespoke automations decay after a process change: people regress all the way back to manual and quietly lose the earlier savings. Over-gating simply reintroduces the toil.

## Spine 2 — Claude Code as the front end for your CLIs

The claim: Claude Code works best here not as a coder but as a top-level orchestrator, a "front end for CLIs" that drives a pipeline of deterministic scripts while offloading each hard-AI subtask to a separate BAML function. The non-obvious part is that people expect the agent to do everything inside one giant reasoning loop; instead the intelligence is pushed down into small typed functions and the top model mostly just calls tools. The mechanism runs in steps: because Sonnet is "almost too good at tool calling" and does not overthink, it makes an ideal conductor; the deterministic CLIs guarantee repeatable behavior; each BAML function is its own context window, so hard reasoning never pollutes the orchestrator's context; and because the agent tolerates imperfect instructions, the glue survives refactors that break rigid scripts (Kevin watched Claude fix a command whose instructions were wrong after a function rename). This generalizes to any internal ops runbook, for example a finance-close pipeline where a slash command calls deterministic ledger scripts and offloads narrative summaries to a typed function. It goes wrong when you offload too little (context bloats) or when the deterministic tools drift and the eager agent papers over failures silently.

## Spine 3 — Let the agent learn the clicks, then bake them

The claim: when a service has no affordable API, use an agentic browser that screenshots the page and decides where to click to discover the workflow, then bake those discovered interactions into deterministic browser-automation code the model no longer drives. The non-obvious part is that people treat agentic browsing as the runtime, but here it is only the discovery phase, and the AI is deliberately thrown away once the useful DOM elements are known. The mechanism: the agent's screenshot-then-click loop is how it learns which elements matter; once learned, that knowledge is crystallized into deterministic clicks that run without screenshots, so subsequent runs are fast, cheap, and repeatable, "assuming the page doesn't change that often." Watching the live Chrome window is the debugging surface, and it earns its keep: Kevin watched the agent get stuck looping on a "what's new" popup it kept opening and closing. This generalizes to any vendor UI without an API, for example automating an insurance portal or a legacy admin console the same way. It goes wrong when baked selectors break after a page change (you need drift detection to re-enter the learning phase), and timing-sensitive fields stay fragile: the agent "got the time wrong" on the event.

---

# 🎬 Proposed ACS videos

## 1. Automate 90%, Gate the One Way Doors
- **HOOK:** The reason your automations never ship is that you are trying to make them push-button.
- **THE PROMISE:** For anyone automating a real workflow, you will know exactly which steps to automate now and which to keep behind a human forever.
- **THE SHAPE:**
  1. Start with one prompt that lists every step, including explicit "STOP, human does this" markers.
  2. Sort the steps by reversibility: cheap-to-undo versus one-way doors.
  3. Auto-run the reversible steps; gate the irreversible ones (mass email, public LinkedIn post).
  4. Fill in the automations incrementally as trust grows, replacing STOP markers one at a time.
  5. Show the brittleness failure mode (process changes, automation breaks, you regress to manual) and how to avoid it.
- **SPINE:** 1
- **SLOT:** Claude Code > new "automation boundaries / where to keep the human"
- **RELATIONSHIP:** ❌ net-new. "The Shifting Bottleneck" (start-here) touches human judgment as the un-automatable constraint at theory altitude, but nothing in the catalog films the concrete reversibility gate plus the incremental STOP-marker build. This is the practical technique, not the theory.
- **PROOF TO REUSE:** Dex: "Make a prompt that is everything you have to do. You can always leave in like stop and get the human to do this part... then you can slowly fill it out with more and more automations." Dex: "you kind of want to like define what are the boundaries outside of your agentic sphere that you want human approval." Dex: "automating doesn't have to be an all or nothing." The LinkedIn / mass-email human gate and "if it messes something up, that's a really embarrassing mistake."

## 2. Let the Agent Learn the Clicks, Then Bake Them
- **HOOK:** Riverside's API costs a fortune, so they automated it with a browser agent that learns the page once and then never thinks again.
- **THE PROMISE:** For anyone stuck automating a service with no usable API, turn a flaky agentic browser into fast, deterministic automation.
- **THE SHAPE:**
  1. Point an agentic browser at the UI; it screenshots and decides where to click.
  2. Watch the live Chrome window to catch it looping (the "what's new" popup rabbit hole).
  3. Once it learns which DOM elements matter, capture those interactions.
  4. Bake them into deterministic clicks that run with no screenshots and no model in the loop.
  5. Add drift detection so a page change re-triggers the learning phase.
- **SPINE:** 3
- **SLOT:** Claude Code > playwright-agent-browser (backlog); complements Claude CoWork "07 Browser Automation"
- **RELATIONSHIP:** 🔗 complements Claude CoWork "07 Browser Automation" (scripted), which teaches driving a browser with an agent at runtime. This adds the next step it does not cover: crystallizing the agent's learned clicks into deterministic code so the AI is no longer in the loop.
- **PROOF TO REUSE:** "we found a thing we wanted to automate and so we just did it with a browser agent." "now that it's rolling, it doesn't take the screenshot anymore... because it figured out what DOM elements matter." "the best way I found to build this is to watch what it is doing." The time-field failure ("it just got the time wrong").

## 3. Claude Code as the Front End for Your CLIs
- **HOOK:** Stop asking the agent to do everything. Make it the conductor, not the orchestra.
- **THE PROMISE:** For engineers with a messy multi-tool workflow, wrap it in one Claude Code command that orchestrates deterministic scripts and offloads the hard AI to typed functions.
- **THE SHAPE:**
  1. Break the workflow into small deterministic CLIs.
  2. Offload each hard-AI subtask to a separate BAML function with its own context window.
  3. Let a Sonnet-driven command orchestrate the tools and ask for missing inputs via the ask-user-question tool.
  4. Show Claude recovering from a wrong instruction after a function was renamed.
  5. Contrast it with the brittle all-in-one script it replaces.
- **SPINE:** 2
- **SLOT:** Techniques > complements "high-level-strategy-low-level-details" (filmed)
- **RELATIONSHIP:** 🔗 complements "high-level-strategy-low-level-details" (filmed), which teaches splitting high-level strategy from low-level detail. This adds the concrete architecture that split implies: a Claude Code command orchestrating deterministic CLIs plus offloaded BAML reasoning functions, so Ray does not re-teach the strategy/detail principle itself.
- **PROOF TO REUSE:** "it's almost like a front end for CLIs... it's smart enough that it can kind of fill in the gaps and sand out all of those burrows for you." "sonnet is great at tool calling... almost like too good at tool calling." Claude fixing the command whose written instructions were wrong after the rename. The "separate context window that goes and does the thing" framing.

## Also film-able (not deep-dived)
- **De-slop your AI writing with a two-pass loop:** one structured pass names each artificial pattern with an example and why it sounds fake, then a separate pass rewrites to remove them. Pairs with rationale-before-answer structured chain-of-thought and shrink-then-expand two-pass generation. Rough slot: Prompt Engineering > "make AI not sound like AI." Likely net-new for the de-slop loop; the CoT and structured-output halves are partially covered by the PE Foundations briefs.

---

# 📚 Full wisdom (reference)

## SUMMARY
Dex (HumanLayer) and Kevin Gregory demo how they automated the AI That Works podcast pipeline using Claude Code commands orchestrating deterministic CLIs and BAML functions.

## IDEAS
- Claude Code becomes a front end for CLIs, sanding burrs so instructions need not be exact.
- A single episode-prep command creates the image, Riverside event, Luma event, and updates the RSS feed.
- Riverside had no affordable API, so they automated event creation entirely with a browser agent instead.
- The browser agent screenshots the page, decides where to click, then bakes clicks into deterministic code.
- Once the agent learned which DOM elements matter, it stopped screenshotting and clicked deterministically every run.
- Sonnet is almost too good at tool calling; it acts without thinking much, perfect for orchestration.
- Hard AI is offloaded to BAML functions, each a separate context window doing its own reasoning.
- Email generation shrinks the transcript into a structure first, then expands that structure into polished prose.
- A separate pass names AI-slop patterns with examples, then a final pass rewrites to remove them.
- Generating a rationale field before the answer field gives the model thinking space and better output.
- The image feedback loop captures what you disliked, updates the prompt, and regenerates instead of retrying.
- Interactive commands ask what they need via the ask-user-question tool, so you skip memorizing any arguments.
- Automating ninety percent still wins; the all-or-nothing push-button mindset is exactly what stops people from starting.
- Irreversible actions like mass emails and public LinkedIn posts stay manual behind a human approval gate.
- Start with a prompt containing STOP-for-human markers, then fill in the automations gradually as trust grows.
- Claude fixed a slash command whose written instructions were wrong because a function had been renamed.
- They watch the live Chrome window to catch the agent looping on the wrong popup button.

## INSIGHTS
- Agents give squishy robustness over rigid deterministic tools, and that flexibility is why Claude Code orchestrates.
- The right automation boundary follows reversibility: cheap-to-undo steps auto-run, while one-way doors always require a human.
- Transient screenshot-driven learning becomes permanent deterministic code once the agent discovers which page elements actually matter.
- Shrinking then expanding avoids context degradation from dumping an enormous transcript directly into the final generation.
- Detection and correction should be separate passes; naming why output fails guides the rewrite far better.
- A dumb orchestrating model plus offloaded reasoning sub-functions mirrors subagents without ever formally spawning any subagents.
- Brittle bespoke automations decay when process changes; regressing to manual work quietly erases the earlier savings.
- Structured rationale-before-answer is simply chain-of-thought expressed as a schema field, buying reasoning inside otherwise deterministic output.
- Claude Code tolerates wrong instructions and stale paths, filling gaps a brittle script would fail on.

## QUOTES
- Kevin: "That is all it takes now to prep an episode."
- Dex: "Make a prompt that is everything you have to do. You can always leave in like stop and get the human to do this part and then you can slowly fill it out with more and more automations as you go."
- Dex: "you kind of want to like define what are the boundaries outside of your agentic sphere that you want human approval."
- Dex: "So I think automating doesn't have to be an all or nothing."
- Kevin: "it's very easy to have an all or nothing mindset when it comes to automating right I want it to be push button."
- Dex: "sonnet is great at tool calling, right? It's actually almost like too good at tool calling. All it wants to do is just go do stuff all day and it doesn't think that much."
- Dex: "This is like, okay, we found a thing we wanted to automate and so we just did it with a browser agent."
- Kevin: "the best way I found to build this is to watch what it is doing."
- Dex: "it's almost like a front end for CLIs in some way where you don't have to be super specific... it's smart enough that it can kind of fill in the gaps and sand out all of those burrows for you."
- Dex: "We're doing the chain of thought but via structured output field."
- Kevin: "I do this a lot where I structure the thinking, right? Like give me the rationale before you actually give me the output."
- Kevin: "make sure that you don't have an AI doing that because if it messes something up, then that's a really embarrassing mistake."

## HABITS
- They keep a human in the loop reviewing every email before it reaches thousands of subscribers.
- They run a final Claude cleanup pass after the CLI to preserve the newsletter's required structure.
- They feed the model a past example email they hand-wrote and were happy with as reference.
- They deliberately use Sonnet, not Opus, for these workflows to avoid burning too many expensive tokens.
- They watch the live Chrome window whenever the browser agent runs to catch stuck loops early.
- They send the suggested clips to their human editor as priming, not as final posting decisions.
- They leave short manual thirty-second steps, like pasting transcripts, unautomated when the effort exceeds the payoff.
- They automatically prepend the required 'AI that works' tag to titles because humans routinely forget it.

## FACTS
- The manual episode process once took roughly three to four hours weekly before any automation existed.
- The first automation pipeline cut weekly effort to roughly one hour, and later to thirty minutes.
- The current episode-prep pipeline finishes in only about ten minutes once the title and description exist.
- Riverside's API is only available at an expensive account tier, which forced the browser-automation workaround entirely.
- The boundaryml.com/podcast page is generated from meta.md files and an RSS feed hosted inside their GitHub.
- BAML currently has no built-in image generator, so they call the Nano Banana API directly instead.
- The pipeline uses Nano Banana Pro plus a fixed base image to generate each episode thumbnail.
- Twelve stray test Riverside events once appeared on Kevin's calendar from his repeated automation practice runs.

## REFERENCES
- People: Dex (host, founder of HumanLayer), Kevin Gregory (Evolution IQ), Vibb (co-host), Mario (video editor).
- Companies/products: HumanLayer (helps you use coding agents better), Evolution IQ (insurance/disability claims software).
- Tools: Claude Code (Sonnet 4.5; mentions Opus 4.5/4.6; ask-user-question tool; breakpoints), BAML (BoundaryML structured functions), Nano Banana and Nano Banana Pro (image generation), Riverside (recording/hosting, API, browser automation), Luma (events, slugs, invites), Excalidraw and the Excalidraw MCP, Figma (old manual thumbnail board), Notion (topic backlog), GitHub (repo hosting meta.md + RSS), Firebase (old V1 web app), Slack (clip handoff), LinkedIn and X (distribution).
- Pages/concepts: boundaryml.com/podcast (the podcast page), the "AI That Works" show, "back pressure" (agent checking its own work autonomously).

## ONE-SENTENCE TAKEAWAY
Orchestrate deterministic CLIs with Claude Code, automate incrementally, and keep humans guarding every irreversible boundary.

## RECOMMENDATIONS
- Turn each repetitive workflow into a Claude Code command that simply calls small deterministic CLI scripts.
- Write your first automation as a prompt full of STOP-for-human markers, then replace each one gradually.
- List which of your pipeline steps are irreversible, then permanently gate only those behind human approval.
- For browser tasks lacking an API, let an agent learn the clicks, then bake deterministic automation.
- Add a rationale field before the answer field in your structured outputs to improve generation quality.
- Split any long-transcript generation into a shrink-to-structure pass, then a separate expand-to-prose composition pass run afterward.
- De-slop AI writing by first naming the specific artificial patterns, then running a dedicated rewrite pass.
- Give image regeneration a feedback loop that captures your critique and updates the prompt each time.
- Choose Sonnet for tool-heavy orchestration, and offload the genuinely hard reasoning to dedicated structured BAML functions.
