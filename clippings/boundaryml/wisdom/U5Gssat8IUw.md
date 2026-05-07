---
video_id: U5Gssat8IUw
title: "How to Automate Complex Workflows with Claude: 🦄 #45"
url: https://www.youtube.com/watch?v=U5Gssat8IUw
channel: BoundaryML
---

### SUMMARY

Dex from Human Layer and Kevin from Evolution IQ demonstrate Claude Code orchestrating BAML functions, browser agents, and CLIs to automate podcast production end-to-end.

### IDEAS

- Generating rationale before output gives the model thinking space and produces noticeably better results across structured generation tasks.
- Chain of thought can be implemented elegantly by adding a rationale field to a structured output schema.
- Automation does not need to be all-or-nothing; ninety percent automation still represents a massive workflow win overall.
- Leave human approval gates at one-way actions like emailing thousands or posting publicly while automating reversible steps.
- A single Claude Code slash command can orchestrate many small CLIs that each call dedicated BAML functions internally.
- Sonnet excels at tool calling but thinks less, making it ideal for orchestration over deep reasoning sub-tasks.
- Build browser automations by letting an agent screenshot, click, and learn, then bake working flows into deterministic code.
- Throwaway exploration phases produce stable scripts; you discard the AI scaffolding once the deterministic path is known.
- Image generation prompts work better when the model first generates a subtitle, then composes it onto a base template.
- Feedback loops on generated artifacts beat blind regeneration; let users explain dislikes so the prompt updates contextually.
- Two-pass generation, structure first then prose, mirrors how compression in LoRAs constrains output toward desired forms reliably.
- Use the LLM-as-judge pattern to detect AI slop patterns in writing, then feed findings into a rewriter.
- Identify recurring AI tells like em dashes, rule of three, and meta-labels to systematically scrub generated copy.
- Always do a final Claude Code pass after structured generation to preserve formatting that strict pipelines might lose.
- Cloud Code acts as a forgiving front-end for CLIs, filling gaps when instructions drift or commands are renamed.
- Riverside lacks affordable API access, so a browser agent clicking through the UI replaces the missing programmatic interface.
- Watching the browser window during agent execution reveals click-loop bugs the agent itself cannot detect or escape.
- Storing episode metadata as MD files in Git lets a website RSS feed regenerate itself automatically from commits.
- The summer V1 web app broke when process changed, illustrating brittle automation pain when ownership or environments shift.
- Without working automation the team batched four weeks of work into chaotic two-hour Saturday catch-up sessions.
- Each clip suggestion includes rationale, transcript span, speaker, and hook to prime a human editor's discretion efficiently.
- Reusing the email-takeaways BAML function for clip extraction shows how composable functions cross workflow boundaries.
- A naive single-shot transcript-to-email prompt fails; structured extraction first, then composition, drastically improves quality.
- Long transcripts degrade context, so summarize the structure first and feed only that into the composition step.
- Saving intermediate JSON artifacts of email pattern analysis would create a great teaching demo of the pipeline.
- Cute graphic outputs that get overwritten matter less; subtitles that ship matter most for prompt engineering effort.
- Structured output fields force the model to commit to schema, eliminating freeform drift across long generations.
- Slow incremental automation with explicit human stop points beats waiting to ship a perfect end-to-end pipeline.
- Sandbox philosophy: define what cannot leave the agentic sphere without approval, automate everything inside that boundary.
- Episode prep dropped from three or four hours weekly to about ten minutes once Claude orchestrated all CLIs.
- Skills represent a structural pattern of giving Claude small composable tools to glue together complex workflows reliably.

### INSIGHTS

- Structured output with a rationale field is the cleanest implementation of chain of thought in production.
- Automate the reversible, gate the irreversible; that boundary defines where human review actually adds value.
- Brittle automation breaks under process drift; resilient pipelines tolerate renamed functions because Claude bridges the gap.
- Two-stage generation, extract structure then expand prose, beats single-shot for any long content task.
- LLM-as-judge plus rewriter is a reliable pattern to systematically remove detectable AI slop from output.
- Browser agents that learn via screenshots can graduate to deterministic scripts once the path is mapped.
- Composable BAML functions let the same primitive serve multiple downstream workflows without duplicate prompt engineering.
- Cloud Code as orchestrator forgives renamed commands and stale instructions because it reads code intent.
- Ninety percent automation with consistent human review beats ninety-nine percent automation that occasionally posts disasters.
- Process discipline collapses when tools break; resilient automation prevents catch-up debt from compounding into burnout.
- Feedback-aware regeneration loops outperform blind retries by carrying explicit critique into the next prompt iteration.
- Sonnet's tool-call appetite suits orchestration; deeper reasoning belongs in isolated sub-functions with their own contexts.

### QUOTES

- "We're doing the chain of thought but via structured output field." Dex
- "Make a prompt that is everything you have to do." Dex
- "You can always leave in like stop and get the human to do this part." Dex
- "Automating doesn't have to be an all or nothing." Kevin
- "It is hard to get AI not to sound like AI slop." Kevin
- "It always has repeated sentence patterns every time." Kevin
- "Sonnet is great at tool calling, right? It's actually almost like too good at tool calling." Dex
- "All it wants to do is just go do stuff all day and it doesn't think that much." Dex
- "Just throw more tokens at the problem and make it think more." Dex
- "Even after all this and multiple AI reviews, we still need humans in the loop." Kevin
- "Figure out where you where it's okay to automate and where it's not okay to automate." Kevin
- "Vib is a master at figuring out something AI generated." Kevin
- "The transcripts are typically really long and the context might very well degrade." Kevin
- "It's almost like a front end for CLIs in some way." Kevin
- "It's smart enough that it can kind of fill in the gaps." Kevin
- "If it can write the post for you and get it right 90% of the time, that's great." Dex
- "I have like 12 test events on my calendar." Kevin
- "We had a long Figma board." Dex
- "Getting CLIs for cloud code to run game changer." Kevin
- "Hey, this looks like the following email sounds like it sounds like AI." Kevin

### HABITS

- Block a Tuesday calendar slot for episode prep so podcast production never falls completely behind weekly cadence.
- Review every AI-generated email manually even when the pipeline reports high confidence in the output.
- Watch the browser window live during agent execution to catch click-loop bugs early before runaway costs accumulate.
- Keep a topic backlog in Notion so future episodes already have seeds before scheduling pressure arrives.
- Use slugs for URLs deliberately, generating them by hand because the cognitive overhead is genuinely tiny.
- Save out structured JSON intermediates so debugging and demos can reference the actual pipeline state.
- Cap automation ambition at ninety percent and accept human-in-the-loop for irreversible publishing actions consistently.
- Pair program when designing pipelines, recording sessions for later teaching and reuse across the team.
- Test new automations with throwaway events before pointing them at production systems carrying real audience commitments.
- Rename functions freely because Claude Code patches drifting instructions automatically when commands change underneath.
- Iterate on subtitle copy with explicit critique rather than blindly regenerating until something acceptable appears.
- Provide example outputs in BAML prompts so the model has concrete patterns to imitate consistently.
- Keep a CLI per discrete pipeline step rather than one monolithic script for easier debugging and reuse.
- Send Mario clip suggestions in Slack with rationale so a non-engineer can apply discretion productively.
- Skip catch-up Saturdays by maintaining the automation rather than batching four weeks of debt.

### FACTS

- Riverside's API access requires reaching an expensive account tier, making browser automation cheaper for individual creators.
- Luma uses URL slugs to give events memorable short paths separate from auto-generated identifiers.
- BAML does not currently expose a built-in image generation function, requiring direct Nano Banana API calls.
- Nano Banana can composite generated graphics onto a base image while filling in text fields programmatically.
- Boundaryml.com hosts its podcast page by reading meta.md files from a GitHub repository directly.
- The AI that works show prepends an "AI that works" tag to every Luma event title automatically.
- Evolution IQ builds insurance technology software for disability companies that helps examiners take correct claim actions.
- Human Layer is Dex's company that helps engineering teams use coding agents better with safety guard rails.
- Episodes are recorded on Tuesdays and Riverside uploads transcripts the same Tuesday afternoon automatically.
- The previous Firebase web app version reduced weekly prep from three hours to thirty minutes before breaking.
- Excalidraw now exposes an MCP that lets Claude Code generate diagrams from audio stream context.
- Sonnet 4.5 powers the show's automation rather than Opus 4.5 to keep token costs manageable.
- The ask user question tool received improved steering in recent Claude Code releases for interactive flows.
- Mario, the show's video editor, receives suggested shorts via Slack rather than directly through the pipeline.
- The team uses Riverside for video hosting and Luma for invites, reminders, and calendar event distribution.

### REFERENCES

- BAML (Boundary's structured output language)
- Claude Code (Anthropic's coding agent)
- Riverside (podcast video hosting)
- Luma (event invitation platform)
- Notion (topic backlog)
- Figma (legacy thumbnail board)
- Nano Banana / Nano Banana Pro (Gemini image generation)
- Excalidraw MCP server
- Human Layer (Dex's company)
- Evolution IQ (Kevin's employer)
- LinkedIn (publishing target)
- GitHub (RSS feed source)
- YouTube (final video destination)
- Slack (editor handoff)
- Sonnet 4.5 / Opus 4.5 / 4.6 (Claude models)
- AI that works podcast at boundaryml.com/podcast
- Riptide (project mentioned for live coding)

### ONE-SENTENCE TAKEAWAY

Automate reversible steps with composable BAML functions while keeping humans gating any irreversible publishing action.

### RECOMMENDATIONS

- Implement chain of thought as a rationale field in your structured output schema rather than freeform prefixes.
- Start automation with a single prompt listing every step, including stop points for human intervention.
- Identify which workflow actions are irreversible and place explicit human approval gates before each one.
- Use two-pass generation for any long content task: extract structure first, then expand into final prose.
- Build LLM-as-judge passes that name specific AI slop patterns instead of vaguely critiquing generated text.
- Watch browser agents execute live during development to catch click-loop bugs before they consume budget.
- Bake successful exploratory browser automations into deterministic scripts once the click path is verified stable.
- Save intermediate JSON artifacts at every pipeline stage to enable debugging, demos, and reproducible failure analysis.
- Provide concrete example outputs in BAML prompts so models imitate your style consistently across runs.
- Split monolithic automation scripts into many small CLIs that Claude Code orchestrates as composable tools.
- Reuse the same BAML extraction function across workflows like email summaries and clip suggestions to avoid duplication.
- Accept ninety percent automation with consistent human review rather than chasing fragile ninety-nine percent end-to-end runs.
- Maintain a topic backlog so episode planning starts from existing seeds rather than weekly blank-page anxiety.
- Use slugs deliberately for URLs because human-readable paths cost almost nothing but improve sharing significantly.
- Add feedback-aware regeneration loops where users explain dislikes and the prompt incorporates that critique automatically.
- Test new pipelines with throwaway events before pointing them at production systems with real audience exposure.
- Use Sonnet for orchestration and tool calling, reserving deeper reasoning for isolated BAML function contexts.
- Schedule a recurring weekly slot for content production so automation maintenance stays current and never compounds.
- Generate subtitles separately from images, then composite them, rather than asking one prompt to produce both.
- Run a final Claude Code pass after structured pipelines to preserve formatting strict generation steps might drop.
