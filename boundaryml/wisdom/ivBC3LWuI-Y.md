---
video_id: ivBC3LWuI-Y
title: "BAML Demos - 11-08-2024"
url: https://www.youtube.com/watch?v=ivBC3LWuI-Y
channel: BoundaryML
---

### SUMMARY
BoundaryML team presents four BAML-built demos: Discord triage bot, computer-use drawing experiments, automated documentation linker, and BAML code-generating chatbot with agentic pipelines.

### IDEAS
- Every Friday teams should pick one shippable feature, helping maintain motivation through visible weekly progress and momentum.
- Discord scraping bots can classify messages into bugs, features, questions automatically, saving developers hours of manual triage weekly.
- Hallucinated GitHub issue numbers can be silently filtered through validation rather than crashing or blocking entire pipelines.
- Concurrent pipelines reading messages, classifying, summarizing threads, and finding issues simultaneously dramatically improves perceived speed for users.
- Computer use can drive mouse and keyboard, taking screenshots between actions to plan next moves agentically.
- Drawing horses tests agentic planning capabilities far harder than spreadsheet entry, exposing weaknesses in spatial reasoning models.
- Models hallucinate completed work confidently, claiming stars drawn when only random points exist on screen.
- Models may hallucinate visual content itself, not just descriptions, raising deep questions about embedding-space representations of failures.
- Localizing coordinates by reference in images remains a fundamental weakness for current multimodal models doing computer use.
- Building UI components alongside LLM pipelines dramatically improves iteration speed compared to terminal-only debugging loops.
- Structured data outputs enable per-field UI buttons like "fix with AI" that retry only specific failed fields.
- Documentation broken-link checking combines LLM suggestions with sitemap validation and HTTP requests to guarantee link accuracy.
- Haiku follows narrow instructions well but struggles with broader generation tasks compared to Sonnet on complex prompts.
- Splitting prompts into smaller pieces reduces hallucinations because less context produces more focused, higher-quality outputs.
- Parallel prompt execution becomes possible when subtasks like test generation and code generation are decomposed cleanly.
- Generality versus specificity is the fundamental AI tradeoff: tight scope enables precision, broad scope creates uncertainty.
- Verbose prompts from optimizers like DSPy and Anthropic's tools often produce worse outputs than hand-tuned shorter versions.
- Closer proximity between instructions and data fields helps models constrain output better than distant prompt-level instructions.
- Number streaming creates jarring UI snaps from "2" to "20" to "2025", requiring semantic streaming for completed values only.
- Agents are fundamentally just while loops with action selection and routing, nothing more sophisticated than that.
- Multi-agent systems are just multiple separate while loops cooperating with each other through shared message contexts.
- Human-in-the-loop approval gates with refresh-the-step-counter feedback enable safe agentic systems with controlled iteration limits.
- RAG context should be rendered as natural prose with clear delimiters, not as JSON objects with field labels.
- V0's specialization in shadcn and Lucid icons makes it superior to Anthropic for component generation despite identical capability.
- Building a chatbot starts with diagrams; LLM omnipotence makes architecture harder, not easier, without explicit decomposition.
- Tracking which streaming field is active enables progressive UI states like spinners pinned to specific recipe components.
- Plans then code then tests as separate prompts allows parallel execution while reducing context burden on each call.
- Re-feeding RAG results into the chat loop lets models iteratively refine queries until sufficient context exists.
- Wrapping agent loops with maximum step counts prevents infinite recursion when models cannot answer user questions.
- Pre-validating instructions inline next to data fields beats top-of-prompt instructions for structured generation accuracy.
- Test cases auto-generated alongside BAML code give users iteration starting points without explicit prompting work.
- Symbol tuning and chain-of-thought can be programmatically added to BAML prompts because the syntax is parseable.

### INSIGHTS
- Decomposing agent prompts into focused single-purpose calls reduces hallucination while enabling parallelism and faster human iteration loops.
- Structured outputs unlock better UIs because individual fields become addressable for retry, validation, and progressive rendering.
- Validation must wrap LLM outputs externally because models hallucinate confidently regardless of how thorough the prompt design becomes.
- Computer use's bottleneck is spatial coordinate registration in images, not tool selection or high-level planning capabilities.
- Investing early in custom UI for LLM iteration pays compounding dividends in debugging speed and pipeline quality.
- Specialized narrow tools beat general-purpose ones when domain knowledge can be baked into prompts and rendering systems.
- Human approval with feedback-driven step refresh creates safe agentic loops without sacrificing autonomy when work is genuinely good.
- RAG should never be a framework feature because context-rendering quality depends entirely on prompt-specific formatting decisions.
- Agentic architectures collapse to while loops; complexity comes from action routing, not loop mechanics themselves.
- Semantic streaming of complete values prevents UI thrashing during numeric or structured data generation in real-time interfaces.
- Diagramming pipelines first prevents LLM omnipotence from collapsing architectures into single mega-prompts that resist debugging.
- Verbose auto-generated prompts often degrade quality because instruction proximity to relevant fields matters more than instruction completeness.
- Subjective LLM self-reports about completed work often diverge from observable outputs, making external verification essential.
- Hot reload combined with structured outputs enables fast iterate-render-fix loops impossible with pure terminal pipelines.
- Models can hallucinate visual content not just descriptions, suggesting embedding-space failures rather than mere fabrication patterns.

### QUOTES
- "Me and Aon literally spend hours the day before scrolling through the Discord finding all the issues." — Vaibhav
- "The code doesn't crash if it hallucinates but it's just going to skip the one that's wrong." — Antonio
- "We can't really draw horses." — Greg
- "I have erased the original mouth and drawn a new one that's wider and has a nicer curve." — Claude (computer use)
- "Did Claude hallucinate just the nice words or is Claude hallucinating an image of a star?" — Greg
- "Drawing is a super agentic and like cognitive task that involves lots of planning." — Greg
- "It's a lot easier when you can just click around and like ask it for to go and do different things." — Sam
- "If you're building an LLM application and you don't really have a large testing suite, build a small UI." — Vaibhav
- "Spend some time on the UI; it will make your everything else down the line faster." — Vaibhav
- "Because LLMs can do anything it almost makes it harder to code with them." — Aaron
- "The less context there is in the prompt, the better your output will be." — Aaron
- "An agent is really fundamentally just a while loop around action selection with routing." — Vaibhav
- "It's literally just multiple separate while loops cooperating with each other." — Vaibhav
- "We hate writing docs but we have to do it anyway." — Vaibhav
- "You always have to strike the balance between generality versus specificity." — Vaibhav
- "If we do RAG we actually believe that it's going to be harder for you to do these." — Vaibhav
- "The closer in proximity you can keep your instructions to the data model, the better you can constrain the model." — Vaibhav
- "What I would really love to do is be able to parse triple back ticks and not have to worry about this." — Vaibhav
- "Years are just not going to work because every single graph is going to snap to the back." — Vaibhav
- "Sometimes when the human gets a response, will actually deny the request and say it's too verbose." — Vaibhav

### HABITS
- Run weekly Friday Discord triage sessions to pick one guaranteed-shipping feature for the following Monday delivery.
- Diagram pipeline architecture before writing any prompt code to avoid collapsing complexity into mega-prompts.
- Build small UI components for LLM iteration rather than relying purely on terminal output for debugging.
- Split LLM tasks into separate prompts whenever subtasks could potentially run in parallel for speed.
- Validate LLM outputs externally with sitemap checks and HTTP requests rather than trusting prompt instructions alone.
- Generate test cases automatically alongside production code to give users a working iteration starting point.
- Wrap agent loops with maximum step counts to prevent infinite recursion on impossible user questions.
- Reset step counters when humans provide feedback so refined queries get full retry budget again.
- Render structured streaming data with semantic completion gates rather than character-by-character partial values.
- Track which array element is actively streaming by checking the last element during partial states.
- Place instructions inline next to relevant data fields rather than at the top of prompts.
- Use Haiku for narrow instruction-following tasks and Sonnet for broader generation requiring richer reasoning capability.
- Run hot-reload loops in background terminals to see UI updates immediately as prompts iterate.
- Default to writing prompts manually rather than letting prompt optimizers generate verbose auto-tuned versions.
- Use shiny (Python) instead of Streamlit or Gradio for quick LLM application UI prototypes.

### FACTS
- Anthropic released computer use as a framework that drives mouse, keyboard, and takes screenshots agentically.
- Computer use sends entire conversation history including all screenshots on every round-trip with Anthropic's servers.
- Pinecone is used for vector database retrieval in BoundaryML's documentation chatbot pipeline implementation.
- BAML is a custom programming language being developed by BoundaryML for structured LLM prompt engineering.
- The notorious-RAG demo in BAML examples implements human-in-the-loop approval for Discord support responses.
- Jotai is a React state management library that V0 fails to generate code for despite being capable.
- Lucid Icons and shadcn are component libraries V0 specializes in for its component generation.
- Hamel Hussein writes blog posts recommending shiny for Python data application UIs over alternatives.
- Anthropic's prompt optimizer tends to generate verbose prompts that degrade output quality compared to handwritten ones.
- DSPy generates verbose optimized prompts that BoundaryML team found inferior to manual prompt iteration.
- Computer use cost a few dollars during a full day of horse-drawing experimentation by the team.
- BAML examples repository on GitHub at boundaryml/baml-examples hosts all four demo source codes publicly.
- Discord Python client API combined with Notion API enables full automated message classification pipelines.
- BAML lacks RAG primitives intentionally because context formatting matters more than retrieval mechanics for quality.
- BoundaryML maintains over 200 public repositories on GitHub, approaching syntax highlighting threshold for the language.

### REFERENCES
- BAML (BoundaryML's domain-specific language for prompts)
- Anthropic Computer Use framework
- Claude (Anthropic LLM) including Sonnet and Haiku models
- OpenAI GPT-4o
- Discord Python client API
- Notion API
- GitHub API
- Pinecone vector database
- DSPy prompt optimization library
- LangChain, Instructor (mentioned as porting sources)
- Stable Diffusion, DALL-E, Sora, Midjourney (image generation references)
- V0 by Vercel
- Shadcn UI component library
- Lucid Icons
- Jotai (React state management)
- Shiny for Python (Posit)
- Streamlit, Gradio (alternative Python UI libraries)
- Hamel Hussein's blog
- BoundaryML examples repo (github.com/boundaryml/baml-examples)
- Notorious-RAG demo
- promptfiddle.com
- MS Paint (used in computer use demo)
- TypeScript and Python (BAML target languages)

### ONE-SENTENCE TAKEAWAY
Decompose LLM pipelines into small structured prompts with UI feedback loops for accuracy and speed.

### RECOMMENDATIONS
- Build a small UI component before debugging LLM pipelines because terminal output destroys iteration velocity over time.
- Split LLM tasks into focused single-purpose prompts that can run in parallel for speed gains.
- Validate every LLM output with external checks like sitemap lookups or HTTP requests before trusting results.
- Wrap agent loops with maximum step counts to prevent runaway recursion on unanswerable user questions.
- Diagram your agent architecture before coding because LLM omnipotence makes decomposition harder, not easier, without structure.
- Generate test cases automatically alongside production code to give users immediate iteration starting points without manual work.
- Use structured outputs over free-form text whenever possible to enable per-field UI controls and retries.
- Render RAG context as natural prose with clear delimiters rather than JSON objects with field labels.
- Place prompt instructions inline next to relevant data fields rather than top-of-prompt for better model adherence.
- Reset agent step counters when humans give feedback so refined queries get a full retry budget.
- Use semantic streaming for completed values rather than character-streaming numbers that cause UI snap thrashing.
- Default to handwritten prompts over auto-optimizer outputs because verbose generated prompts often degrade output quality.
- Pick narrow specialized tools over general ones when domain knowledge can be baked in.
- Run weekly triage sessions to pick one guaranteed-shipping feature for the following week's delivery.
- Re-feed RAG results back into the chat loop so models can iteratively refine queries until satisfied.
- Use Haiku for narrow instruction-following and Sonnet for broader generation tasks requiring richer reasoning capability.
- Track active streaming fields by checking which array element is last during partial state rendering.
- Build human-in-the-loop approval gates with feedback channels rather than fully autonomous high-stakes agent execution paths.
- Test agentic systems by checking basic spatial sanity before extending to complex multi-step reasoning tasks.
- Combine multiple sources like Discord plus GitHub into single pipelines for richer cross-referenced context retrieval.
