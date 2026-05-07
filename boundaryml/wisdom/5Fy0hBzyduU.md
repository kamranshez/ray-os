---
video_id: 5Fy0hBzyduU
title: "🦄 Evals for large scale classification: #24"
url: https://www.youtube.com/watch?v=5Fy0hBzyduU
channel: BoundaryML
---

### SUMMARY
Vibhav, Dex, and guest Kevin Gregory build production-grade evaluation pipelines for large-scale hardware-store classification problems with 1,400 categories using BAML.

### IDEAS
- Large-scale classification problems benefit from intermediate narrowing stages between embedding retrieval and final LLM selection for better debuggability.
- Adding break points or probes between pipeline stages gives engineers more knobs than monolithic prompt-only or embedding-only approaches.
- Categories coming out of an LLM filter need not match the input categories — intermediate enrichment steps can rewrite descriptions.
- Cost matters less than accuracy initially; medical billing codes show classification correctness directly determines whether hospitals get paid.
- Engineers default to showing latency metrics even when those numbers cannot influence any decision the user makes.
- Distracting visual information actively hurts decision-making UIs even when the underlying data is technically correct and relevant.
- The definition of correctness is subjective — a more general category may be acceptable depending on UI breadcrumbs and navigation.
- Sometimes ground truth data itself is wrong, polluted, or has multiple valid answers that humans disagreed on.
- Tree visualizations look elegant for small problems but completely break down at scale where tables remain readable.
- Building the wrong UI first teaches you what the right UI looks like — wrong attempts are part of the iteration.
- Starting with 20 categories instead of 1,400 lets you iterate the pipeline logic before scaling complexity.
- Throwaway test harness code is fine; only the core pipeline code needs to be production quality.
- Streamlit beats React for evaluation UIs when you know Python and the UI is internal-only.
- Vibe coding works as a substitute for Figma when prototyping what users actually want.
- Models write Streamlit apps better than Jupyter notebooks because notebooks lack a natural linting feedback loop.
- Engineering time and shipping speed matter more than two months of prep work for theoretically perfect models.
- Real production data beats synthetic data which beats friends-and-family data for representative evaluation samples.
- LLMs as classifiers replace traditional computer vision the way Python replaced manual memory management.
- A thousand MCP tools wreck context budgets — the same narrowing pipeline pattern works for tool selection.
- Tying chatbot evaluation to end business metrics like revenue makes spot-checking meaningful instead of arbitrary.
- Smart models can supervise dumb models, letting cheaper models move fast with quality oversight.
- Allowing arrays of acceptable ground truth answers handles overlapping categories more honestly than forcing single answers.
- Confidence-based disambiguation built into UX flow beats forcing the model to commit to one answer.
- Marty Cagan's product principle: your job is learning fast, so Figma mocks beat months of building.
- Schema-driven dynamic UIs let LLMs render structured objects as JSON, YAML, or React components automatically.
- Iteration loop quality determines speed of convergence on a working AI system more than model choice.
- Looking at every failure case reveals problem-specification issues masquerading as model performance failures.
- Hyperparameters in classification pipelines control implementation dimensions independently from query content or LLM reasoning.
- The bigger trap is showing aggregate metrics; case-by-case analysis exposes nuance aggregates hide.
- Spot-checking high-volume call centers ties qualitative observations to revenue, return rates, and conversion metrics.

### INSIGHTS
- Pipeline break points exist to make failures localizable, not just to improve accuracy on raw metrics.
- The right UI is discovered through prototyping the wrong UI, not designed in advance from first principles.
- Subjective definitions of correctness mean the eval scoring function deserves the same iteration as the pipeline.
- Throwaway code for harnesses and UIs frees you to optimize only the parts that matter long-term.
- Aggregate dashboards lie; per-case drilldowns reveal whether failures are model problems or specification problems.
- Models writing code make pipeline construction nearly free, so the value moved to information density and presentation.
- Optimizing latency before correctness signals premature engineering pride rather than thoughtful product judgment.
- Real users provide signal that no amount of synthetic data generation can authentically replicate for evals.
- Decomposing classification into embed-narrow-filter-select stages mirrors how humans navigate hierarchical product categories.
- Eval design must work backwards from desired user experience, not forward from technical pipeline outputs.
- Tying every AI feature to a measurable business metric prevents indefinite tuning without convergence.
- The same narrowing pattern applies universally — categories, MCP tools, ICD codes, document retrieval all benefit.
- LLMs trade deterministic accuracy for capability the way Python traded performance for developer velocity.

### QUOTES
- "What's hard is figuring out how to ingest the information in a way that's helpful." — Kevin
- "Building this pipeline is not hard. Building this is almost free now." — Kevin
- "You don't always know the right thing to build until you build the wrong thing." — Kevin
- "The most important thing you have to think about is can you make it work." — Vibhav
- "There's a spectrum between cheap and accurate." — Dex
- "Engineering time and shipping speed is the most valuable resource you have." — Vibhav
- "How bad is this? Cuz technically this is a failure for our eval set." — Vibhav
- "What is right or wrong is actually really subjective in a lot of use cases." — Vibhav
- "We want to show that we're being good engineers, but for the use case it doesn't add anything." — Kevin
- "The first thing you have to think about is the shortest path to making it work." — Vibhav
- "Just go ship the thing that works and then update the model later." — Vibhav
- "If you can think of it, you can build it now. It's basically free to build these things." — Dex
- "Putting a chatbot on a page is freaking useless unless you can tie it to a business metric." — Vibhav
- "The best way to lint a Jupyter notebook is actually run it." — Dex
- "Sometimes the data is just bad — even if you built all these data sets sanely." — Vibhav
- "I just told Kevin this UI is bad. That's all I really said." — Vibhav
- "Look at it on a case-by-case basis to see why disagreements about correctness emerge." — Kevin
- "It's not about the prompt. It's about the definition of the categories." — Vibhav
- "Vibe code the UIs, vibe code the evals, vibe code the testing harness." — Vibhav
- "How can you give yourself the most leverage to understand what you want?" — Dex
- "Don't try to be optimal in parts of the system that don't need to be optimized." — Vibhav
- "Your sample set is a theoretical sample set until you get production data." — Vibhav
- "I use vibe coding as a substitute for Figma." — Dex
- "Models are much better at writing Streamlit apps than they are at Jupyter notebooks." — Dex
- "If shipping happens two months later because you wanted to collect data, you lost two months." — Vibhav

### HABITS
- Start every classification problem with a small subset like twenty categories before scaling to fourteen hundred.
- Vibe code throwaway test harness UIs without worrying about code quality or long-term maintainability.
- Always check raw JSON outputs first before building any visualization, then graduate to tables when needed.
- Look at every single failure case manually rather than trusting aggregate accuracy percentages alone.
- Default to Streamlit over React for internal evaluation UIs when Python is your primary language.
- Use Cursor or Claude Code to generate UI scaffolding, then refine through tight iteration loops.
- Toggle between strict and lenient correctness definitions when grading evals to surface subjective edge cases.
- Roast your own prompts with a colleague who has strong intuition about per-token LLM behavior.
- Ship updates behind feature flags to large enterprise users rather than gating shipping entirely.
- Pay friends and family or run synthetic generation to seed initial test cases before production data arrives.
- Strip distracting columns like latency from decision UIs even when the data is technically accurate.
- Accept ground truth as an array of valid answers rather than forcing a single canonical correct label.
- Build in confidence-based disambiguation prompts when LLM uncertainty crosses configurable thresholds in production flows.
- Tie every chatbot or classifier evaluation to a downstream business metric like revenue or conversions.
- Spot-check randomly sampled traces frequently rather than waiting for full eval suites to complete.

### FACTS
- The hardware store classification problem in this episode had over 1,400 distinct product categories.
- ICD medical billing codes contain roughly 80,000 entries with separate codes for each individual toe.
- Adding the GitHub MCP server to Claude Code consumes around 60,000 tokens of tool definitions alone.
- Kevin's full pipeline plus tree visualization plus final table UI took roughly two full days of work.
- The initial pipeline code with BAML and dynamic typing took only a couple of hours to assemble.
- A 2020 academic paper documented research opportunities in e-commerce search classification problems.
- E-commerce search optimization problems are worth hundreds of millions of dollars in real business value.
- Streaming GPT-5 requires verifying your OpenAI organization, which blocked the live demo mid-stream.
- Marty Cagan's book "Inspired" articulated foundational product management principles roughly twenty years ago.
- Replit's agent is widely used by product managers as a Figma replacement to prototype features.
- Riverside likely consumes around 70 gigabytes of RAM during a multi-participant podcast recording session.
- Jeff Huntley gave a recent talk highlighting how unfiltered MCP tools tank coding agent performance.
- A trending Hacker News post described an MCP server narrowing thousands of tools via embeddings.
- BAML stands as a programming language built specifically for AI iteration and structured output workflows.
- Network X with Plotly was used for the initial tree visualization before being replaced by tables.
- Evolution IQ builds claims guidance systems for disability insurance carriers in the self-insurance market.

### REFERENCES
- BAML programming language by BoundaryML
- Human Layer (Dex's company)
- Evolution IQ (Kevin's employer)
- Cursor and Cursor's new CLI
- Claude Code
- Streamlit
- Network X with Plotly visualization
- Jupyter notebooks
- Replit agent
- Marty Cagan's book "Inspired"
- Lenny's Podcast (Amjad Masad episode)
- Jeff Huntley's recent talk on MCP tools
- AI That Works episode 1 on classification
- AI That Works episode 5 on evals
- Episode on voice agents
- Policy-to-prompts episode
- 2020 e-commerce search research paper
- Lowe's and Home Depot category structures
- ICD medical billing code system
- Riverside.fm recording platform
- Discord streaming
- GitHub MCP server
- GPT-5, GPT-5 mini, GPT-4o models
- OpenAI Responses API

### ONE-SENTENCE TAKEAWAY
Build classification pipelines with break points, then iterate UIs that surface decisions, not just metrics.

### RECOMMENDATIONS
- Decompose classification problems into embedding retrieval, LLM filtering, and final selection stages with visible probes.
- Start with twenty categories before scaling to thousands so you can iterate the pipeline cheaply.
- Build throwaway evaluation UIs in Streamlit using Claude Code rather than investing in production frameworks.
- Drill into individual failure cases manually before drawing conclusions from aggregate accuracy metrics.
- Allow your ground truth to accept arrays of valid answers when categories meaningfully overlap.
- Strip latency, cost, and other distracting metrics from decision UIs that focus on correctness.
- Tie every AI feature evaluation to a downstream business metric like revenue, conversions, or returns.
- Use the smartest available model first to confirm AI can solve the problem at all.
- Ship behind feature flags to collect real production data instead of waiting for synthetic perfection.
- Replace tree visualizations with sortable tables once your category count exceeds twenty or thirty.
- Spot-check randomly sampled traces continuously rather than running massive eval suites at long intervals.
- Accept that more general answers may be correct depending on your UI's breadcrumb navigation.
- Apply the narrowing pipeline pattern to MCP tool selection when agents have hundreds of tools available.
- Define a separate enrichment step between filters when your categories need rewriting for better LLM reasoning.
- Vibe code Figma alternatives when you need to validate user desire before committing engineering resources.
- Roast your prompts with someone who has strong per-token LLM intuition before optimizing model choice.
- Build confidence-based disambiguation flows where low-confidence answers prompt clarifying questions in the UX.
- Treat the eval scoring function itself as something to iterate alongside the prompt and pipeline.
- Use BAML unit tests to narrow problems to one specific case before generalizing to broader behavior.
- Lint Jupyter notebooks by running them headlessly so coding agents have proper feedback loops.
