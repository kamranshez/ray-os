---
video_id: gX9WpYY61xA
title: "The File System is Your Best AI API"
url: https://www.youtube.com/watch?v=gX9WpYY61xA
channel: BoundaryML
---

### SUMMARY
Dexter, Viv from LangChain, and Jeff discuss harness engineering, agent loops, context engineering, RL-trained models, and surfing frontier model capabilities for building products.

### IDEAS
- Owning both harness and model gives alpha because you can divert the model toward preferred tooling.
- Picking which code deserves handwritten assembly versus compiler output is purely vibes-based intuition work.
- Compilers usually beat humans, but cache locality knowledge occasionally lets experts whoop assembly's ass.
- Every engineer needs to register tools and write system prompts before working at higher abstractions.
- If producing good code becomes truly easy, throw harness code away and rebuild for current problems.
- The 2024 agent loop swapped LLM calls for cloud code calls, gaining batteries-included context management.
- Harnesses extend agents through MCPs, skill markdown files, permission systems, and environmental injection points.
- Cloud code edit tool uses old-string-new-string find-replace; codeex uses git-patch-style apply patch syntax.
- Models get RL-trained for specific tool schemas, dedicating massive weight chunks to that tool calling.
- GPT-OSS 12B easily runs apply patch but completely cannot use cloud code's edit tool.
- Outer harnesses wrap inner harnesses with bash while-true loops creating Ralph Wiggum orchestration patterns.
- Sub-agents are essentially rebuilt Erlang doing pointer-to-pointer message passing using file names.
- Context windows perform best with one goal, one activity, and the right contextual information autoregressing.
- Surfing models means using new releases faster than labs can ship the next one.
- Performance engineers earn more today despite hardware improving because finding skilled people stays hard.
- Make code easy to delete because exposed user features become hamstringing tech debt later.
- Auto-research generated prompts often overfit by enumerating sixty if-else cases inside the system prompt.
- Facebook required engineers at desks during deploys with finger on undo button watching metrics.
- Prod data prevents overfitting to wrong things; eval-driven development needs production traces feeding it.
- Depth-driven learning beats breadth: pick one AI thing, grind for a month, become top twenty percent.
- Manifesting luck surface area requires writing blogs, posting on Twitter, identifying yourself publicly as builder.
- The bitter lesson assumes code is expensive, but auto-research now makes code cheaply rewritable.
- Yagi's parallel-computer view shapes thinking differently than sequential workflow Loom-style abstraction systems.
- Locking into Ralph, Gas Town, or skills-as-OS too early reinforces particular worldviews against models.
- Try things that feel dumb or futuristic; occasionally one works and updates your model intuition.
- Harness engineering means engineering on top of given harnesses, not necessarily building one yourself.
- Philosophy engineering is what makes evals hard, not coding evals; defining the right metric matters.
- Best engineers possess long-horizon vision, designing system invariants that survive feature composition six months later.
- Vertical RL is fine, but tiny classification RL only worth it for cost or latency wins.
- Adding while loops nests intelligence layers; abstraction emerges from autonomous work happening underneath.

### INSIGHTS
- Architecture stays identical when you swap LLM with cloud code; only batteries-included plumbing differs meaningfully.
- The hardest skill is choosing which slice of the system actually deserves your engineering attention.
- Eval-driven development collapses bitter-lesson risk because regenerable code optimizes deterministically against measured metrics.
- Surfing frontier models compounds faster than waiting six months for the next capability release.
- Mastering primitives before abstraction layers enables intelligent decisions about which abstractions to actually adopt.
- Code reuse longevity correlates with creative architectural vision, not raw coding ability or speed.
- Looking at actual data beats automating context engineering decisions through naive trust in Claude.
- Production traces become the durable specification that survives across model generations and harness rewrites.
- Distribution and audience-building should start now if you eventually want entrepreneurial optionality.
- Flexibility outranks expertise during fast-moving paradigm shifts where tomorrow's primitives remain unknown.
- Human-in-the-loop injection during while loops dramatically increases overall system intelligence and reliability.
- Harness engineering means making external systems mimic tools the model already excels at using.
- Defining good metrics is harder than coding evaluation infrastructure; metric choice determines optimization quality.
- Frontier-lab engineers are regular engineers, so individual practitioners can credibly outperform them in narrow slices.
- Speed-to-execution favors stacking abstractions early, then drilling deep where eval pressure demands precision.

### QUOTES
- "If you own the harness and you own the model, you do have alpha." — Viv
- "The hardest part is picking the part of the code that should be written in assembly." — Speaker
- "Most people probably can't beat the compiler for most situations, even extreme experts." — Speaker
- "Every team that doesn't have an AI code review bot is freaking dumb." — Dexter
- "Sometimes the yap does pay off." — Viv
- "If really good code is really easy to produce, which I don't think it is..." — Viv
- "Don't write a git patch man. We believe you. We know what a git patch looks like." — Speaker
- "The first version of making that useful was to give it some sort of execution environment." — Viv
- "Surfing the models. The models will keep getting smarter and nothing you do now will be relevant in a year." — Dan Shipper via Dexter
- "The principles constantly apply. Performance engineering is probably the best analogy for this." — Dexter
- "Sub-agents are really just disposable heaps of memory." — Jeff
- "You're not a senior engineer unless you can teach these primitives." — Jeff
- "Bring back scotch-driven development." — Speaker
- "Just look at the damn data." — Dexter
- "Manifest your luck surface area." — Jeff
- "It's almost too soon to lock in particular things." — Jeff
- "The compiler in this metaphor is beating a Frontier Labs RL model basically." — Dexter
- "We stopped using the word agent and everyone says uses harness to mean what we used to think." — Dexter
- "Coding is art to me." — Viv
- "Adapting your engineering workflow and thinking is so hard." — Viv
- "I'm just going to keep nesting while loops to higher levels of abstraction." — Dexter paraphrasing Viv
- "Depth-driven learning today with AI because you can actually go super deep." — Viv
- "Evals encode the behavior that I need this agent to do." — Viv

### HABITS
- Use Code Rabbit or similar AI code review bots on every pull request without exception.
- Build evals first when targeting accuracy above ninety-eight percent in regulated production environments.
- Pair program more often to absorb intuition that documentation and reading cannot transfer effectively.
- Read leaked Claude Code source and Codex source to study their internal techniques and tricks.
- Look at production traces directly instead of asking Claude to figure out problems automatically.
- Write blog posts about narrow technical interests and post them publicly on Twitter regularly.
- Build a mailing list now, even before launching products, to establish builder identity early.
- Identify yourself as a builder publicly so other builders find you and form friendships.
- Stand at your desk during deploys with finger on the undo button watching deployment metrics.
- Try techniques that feel dumb or futuristic occasionally to discover surprising emergent model capabilities.
- Recycle context windows continually toward one goal rather than letting them sprawl across multiple objectives.
- Design code to be easy to delete rather than easy to extend or maintain long-term.
- Hand-write assembly only when you genuinely understand cache locality the compiler cannot generalize about.
- Keep an emergency bottle of scotch ready when releases break things badly in production.
- Grind hard for one to two months on a single narrow AI topic to reach top-twenty-percent.

### FACTS
- The first widely-shared agent loops appeared around April 2023 using LangChain ingesting OpenAPI specifications.
- Cloud code uses old-string-new-string edit tool while Codex uses apply-patch git-diff style syntax.
- GPT-OSS 12B can call apply patch reliably but fails completely at cloud code's edit syntax.
- Linus Torvalds designed Git's core abstractions which have remained essentially unchanged since creation.
- The Unix philosophy of small composable tools connected by pipes still governs modern system design.
- Anthropic and OpenAI hire regular engineers, not magically-spawned superhumans, to build their frontier products.
- Facebook around 2015 ramped traffic gradually to one percent during deploys with engineer-monitored metrics.
- Amazon's leadership principles include "leaders are right a lot" as a core operational competency.
- Ralph Wiggum loop is a bash-while-true orchestration pattern named by Jeff in 2024.
- Daniel Shipper coined the phrase "surfing the models" describing continual adaptation to frontier releases.
- Compilers optimize most code better than even expert assembly programmers can manage manually.
- Cloud code's haiku delegation handles command-safety checks while keeping the main loop running Sonnet.
- Functors, ports-and-adapters, hexagonal architecture, and property-based testing remain relevant fundamental engineering concepts.
- AI Engineer Miami hosted this live podcast recording in Code Rabbit's furnished podcast studio space.
- Pi-style harness frameworks remain unopinionated about primitives so users can self-evolve harnesses to fit tasks.

### REFERENCES
- LangChain (Viv's company)
- Code Rabbit (AI code review tool)
- Cloud Code (Anthropic)
- Codex (OpenAI)
- GPT-OSS 12B
- Ralph Wiggum Loop (Jeff's bash orchestration pattern)
- Gas Town (orchestration framework)
- Loom
- Dan Shipper (coined "surfing the models")
- Simon Willison (advice on trying things that feel dumb)
- Yagi (parallel computing perspective)
- Gary (skills-as-operating-system perspective)
- Pi (harness framework)
- Tailwind CSS / shadcn/ui (analogy for harness primitives)
- Temporal (workflow orchestration analogy)
- Erlang (sub-agent message-passing analogy)
- Git (clean abstraction example)
- Linux (philosophy reference)
- Amazon S3 / EC2 (long-lived API design example)
- Karpathy (autoresearch methodology, referenced by skill name)
- AI Engineer Miami (event venue)
- The Bitter Lesson (Rich Sutton)

### ONE-SENTENCE TAKEAWAY
Master harness primitives, surf frontier models, build evals, and grind narrow depth over breadth.

### RECOMMENDATIONS
- Add an AI code review bot to every repository you maintain starting this week without delay.
- Build your first agent from scratch with manual tool registration before reaching for prebuilt frameworks.
- Read the leaked Cloud Code source and Codex source to internalize their context-recycling techniques.
- Construct evals from production traces before writing any harness optimization code targeting accuracy improvements.
- Keep harness code easy to delete so model improvements don't strand you with technical debt.
- Pick one narrow AI topic, grind two months, write a blog post, share on Twitter.
- Start a mailing list today even without a product to begin building distribution and identity.
- Pair program with smart practitioners to absorb intuition that written documentation cannot effectively transfer.
- Look directly at production data rather than asking Claude to figure things out autonomously.
- Try at least one technique weekly that feels dumb or futuristic to update model intuition.
- Resist locking into Ralph, Gas Town, or skills-as-OS too early during paradigm-shifting model releases.
- Use Pi-style unopinionated harness frameworks when you don't yet know which primitives will dominate.
- Inject humans into while loops at decision points where intelligence gaps cause expensive failures.
- Make external systems mimic tools the model already masters instead of training new tool schemas.
- Build deployment metrics dashboards and watch them live during every production push to catch regressions.
- Practice library design and software modularity since agents copy and paste bad patterns everywhere.
- Study sub-agent architectures as disposable heaps of memory communicating through file-based message passing.
- Learn functors, hexagonal architecture, and property-based testing because fundamentals still differentiate senior engineers.
- Avoid fine-tuning models for narrow classification unless cost or latency genuinely demand the optimization.
- Bring back scotch-driven development culture: own your deploys, own your mistakes, apologize promptly.
