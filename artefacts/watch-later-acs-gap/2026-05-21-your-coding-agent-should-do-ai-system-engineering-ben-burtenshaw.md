---
title: "Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face"
video_url: https://www.youtube.com/watch?v=JomVvNDjGb8
video_id: JomVvNDjGb8
channel: AI Engineer
published: 2026-05-21
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face**](https://www.youtube.com/watch?v=JomVvNDjGb8) - AI Engineer - uploaded 2026-05-21

> Two film-able ideas: a net-new "open primitives beat abstracted APIs" principle, and a next-step overnight multi-agent research lab beyond the Loopy AI class.

## The one idea worth a video

- **Distribute a self-improving loop across specialized agent roles.** Instead of one agent iterating on a training script, split it into researcher, planner, workers, and reporter that coordinate through git and a shared score file, running verifiable experiments overnight on remote compute. VERDICT: 🔗 next-step video available (beyond the Loopy AI class).
- **Give agents open primitives, not abstracted APIs (LATENT SPINE).** Expose raw data layers an agent can manipulate freely; a layer it cannot get behind is a ceiling. VERDICT: ❌ net-new video available.
- **Skills compress a years-long specialization into a few-shot task.** A skill is file-based context, and the right one turns a zero-shot failure (writing a CUDA kernel) into a checked few-shot success. VERDICT: ✅ mechanic already covered (kept for context, no pitch).

## Summary + counts

Ben Burtenshaw of Hugging Face shows coding agents doing AI systems engineering across three levels: CUDA kernels, zero-shot fine-tuning, and an overnight multi-agent research lab.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

---

## 🔬 Deep dive

### Spine A — Skills compress a years-long specialization into a few-shot task (✅ covered)

The claim: a skill is nothing more than file-based context, and loading the right one turns a task an agent would fail zero-shot, like writing a CUDA kernel or running a training pipeline, into a few-shot task it can actually complete. Most people got this wrong: kernel writing and ML engineering were treated as unattainable for "the humble agent," and the assumed fix was a smarter model. The real mechanism is different. Because the skill supplies worked examples plus runnable benchmark scripts, the agent stops guessing from parametric memory and pattern-matches from concrete in-context demonstrations, then verifies its output against the skill's own benchmark, so a zero-shot failure becomes a checked few-shot success. The binding constraint moves from model capability to context supply. This generalizes to any gnarly internal domain where the model is capable but lacks house-specific examples, for instance a company's ledger-reconciliation rules or its Terraform conventions. It goes wrong when skills go stale as the underlying library changes, which is why Burtenshaw favors project-maintained skills over "YOLO" ones, and a skill that never triggers is dead weight.

### Spine B — Distribute a self-improving loop across specialized agent roles (🔗 complement)

The claim: rather than one agent iterating on a training script, split the research loop into specialized roles (researcher, planner, workers, reporter) that coordinate through git branches and a shared data layer, running verifiable experiments overnight on remote compute. It is non-obvious because Karpathy's Auto Research used a single agent looping, and the intuitive way to scale is "make that one agent better." Burtenshaw found it weird that one agent did everything in sequence, so he distributed it. The mechanism: because each role carries a narrow template and one job (scout papers into hypotheses, queue them, implement them as scripts, report results), each agent's context stays small and on-task, and because they synchronize through git branches plus a shared score file, the work parallelizes across many jobs without agents clobbering each other. Verifiable metrics, like bits per byte, let the reporter rank runs automatically. It generalizes to any domain with a numeric verifier: an overnight loop tuning your app's Lighthouse score, a query-latency benchmark, or prompt-optimization sweeps. It goes wrong without a genuine verifier (the loop optimizes noise), the inter-agent tables get needlessly verbose, and unattended runs burn compute for hours.

### Spine C — Give agents open primitives, not abstracted APIs (❌ net-new, LATENT SPINE)

The claim: agents perform best when handed open primitives, raw data layers they can manipulate, rather than abstracted APIs, because a layer you cannot get behind is a ceiling. As Burtenshaw puts it, "it's more about exposing well" than abstracting away. This cuts against standard engineering instinct, which says wrap complexity behind a clean API. For agents that instinct backfires. The mechanism: because an agent can write arbitrary code, when it holds the raw data (Trackio is really just an open parquet store) it can produce any view it needs, a Gantt chart, a custom filter, an ad-hoc table, without waiting for an API author to add an endpoint. An abstracted API only exposes the operations its designer imagined, so it caps the agent's reach; more surface means more autonomy. It generalizes directly to tool and MCP design: prefer giving an agent a database connection, SQL, or the filesystem over three hand-picked REST endpoints. It goes wrong because raw access is more dangerous (a rogue agent can do more damage), so it needs read-only guardrails and sandboxing, and some abstractions genuinely protect. The source treats this thinly, in the closing takeaways, so the eventual video needs extra sourcing and its own worked demo.

---

## 🎬 Proposed ACS videos

### 1. Build Your Own Overnight AI Research Lab With Four Agent Roles

- **HOOK:** Karpathy used one agent to improve a training script. Splitting it into four roles runs experiments while you sleep.
- **THE PROMISE:** For anyone running an agent loop, you leave with a role-based team (researcher, planner, workers, reporter) that self-improves a real metric overnight.
- **THE SHAPE:**
  1. Start from the single-agent loop and show why one agent doing everything in sequence is the bottleneck.
  2. Define four role templates, each with a narrow job and its own current-state, jobs, and hyperparameters context.
  3. Coordinate them through git branches plus one shared score file so jobs parallelize without clobbering each other.
  4. Pick a verifiable experiment (tune a Lighthouse score or a latency benchmark) so the reporter can rank runs automatically.
  5. Wire dashboard events to email alerts and let it run for hours unattended.
- **SPINE:** B.
- **SLOT:** Loopy AI, new chapter after "L3: Task Lifecycle" (or Advanced Techniques, Multi-Agent Orchestration).
- **RELATIONSHIP:** 🔗 complements "Improving the Loop" (Loopy AI), which teaches evolving one existing loop after real runs; this is the next step, a persistent multi-role team running verifiable experiments in parallel, so do not re-teach single-loop iteration.
- **PROOF TO REUSE:** the four roles (researcher scouts HF papers as hypotheses, planner queues jobs, workers implement scripts, reporter maintains the dashboard); "one agent working in a single way" as the problem; git-branch plus shared-score-file coordination; "verifiable experiment like training a model."

### 2. Stop Wrapping Your Agent's Tools In APIs

- **HOOK:** You abstract complexity behind clean APIs. For an agent, that clean API is a ceiling it can never get behind.
- **THE PROMISE:** For anyone building tools or MCP servers, you leave able to audit your agent's tools and swap closed wrappers for open data layers it can drive itself.
- **THE SHAPE:**
  1. Show an agent hitting a wall: it needs a view the API author never exposed.
  2. Contrast with a raw data layer (parquet, a database, the filesystem) where the agent writes its own query or chart.
  3. State the rule: expose well, do not abstract away; every layer you cannot get behind caps autonomy.
  4. Redesign one MCP tool from three hand-picked endpoints to a scoped raw-data interface.
  5. Add read-only guardrails and a sandbox so raw access stays safe.
- **SPINE:** C.
- **SLOT:** Context Engineering, MCP / tool-design chapter (or Advanced Techniques, Tooling & Setup).
- **RELATIONSHIP:** ❌ net-new. ACS has "Benchmarking Tools & MCPs," "Claude.ai MCP Servers," and "Scoping APIs," but none argue the design principle of choosing tools that expose raw manipulable data over abstracted APIs.
- **PROOF TO REUSE:** "agents work really well with open primitives"; "if we have a layer that we can't necessarily get behind, that that is a ceiling"; "it's more about exposing well"; Trackio as "basically just a data structure" letting the agent build a Gantt chart itself.

### Also film-able (not deep-dived)

- **Downgrade The Model Your Skill Runs On:** use an eval-per-skill workflow (Burtenshaw's `upskill`: generate the skill, generate its eval, compare models on accuracy and total token cost) to pick the cheapest model that still passes. 🔗 complements "Specifying Models for Skills" and "Benchmarking Tools & MCPs" by adding a repeatable skill-level eval loop. SLOT: Master Claude Code, Skills chapter.

---

## 📚 Full wisdom (reference)

**SUMMARY:** Ben Burtenshaw of Hugging Face shows coding agents doing AI systems engineering across three levels: CUDA kernels, zero-shot fine-tuning, and an overnight multi-agent research lab.

**IDEAS**
- Coding agents can now write valid, optimized CUDA kernels, a task once thought impossible for them.
- A skill is just file-based context you version, open, and close like any other source file.
- Skills take a hard task from zero-shot to few-shot by just giving the agent worked examples.
- Memory bandwidth, not raw compute, is usually the real bottleneck when running models on modern GPUs.
- Custom kernels raise arithmetic intensity, doing more math per read and write to keep GPUs warm.
- Hugging Face's kernels library distributes kernels as hub repos with toml files declaring supported hardware versions.
- Anyone with an agent can now become a kernel publisher today, just like a model publisher.
- A generated Qwen3 8B kernel for H100 gave a 94% speedup, not state of the art.
- Hardware compatibility is low-hanging fruit: cheap cloud GPUs often lack optimized kernels for your specific model.
- Upskill generates a skill, generates an eval, then compares models on accuracy and total token cost.
- You can fine-tune Qwen3 from a single prompt, running the GPUs directly on the hub itself.
- Karpathy's Auto Research had a single Claude agent iteratively improve a nanoGPT training script's overall efficiency.
- Burtenshaw instead distributed that single loop into four distinct agent roles: researcher, planner, workers, and reporter.
- The researcher scouts HF papers as hypotheses; the planner queues jobs; workers implement them as scripts.
- Agents coordinate through plain git branches and a shared data structure holding all the experiment scores.
- Trackio is a great agent dashboard because it is really just an open parquet data layer.
- Because Trackio exposes raw parquet, an agent can build any visualization itself, even a Gantt chart.
- This research pattern works almost anywhere: implemented in OpenCode, Codex, Claude, and even the wild Gastown.

**INSIGHTS**
- Coding agents crossed an acceptance gradient recently; staying contemporary now means moving closer to the silicon.
- Writing kernels was never the hard part; distributing and actually using them in inference engines was.
- Standard repos on a shared hub are the boring precondition that makes agentic systems engineering work.
- Files inherit git superpowers: agents open, close, version, and source-control context exactly as humans already do.
- Project-maintained skills beat YOLO skills because maintainers keep them robust as the underlying library keeps changing.
- Distributing an iterative research loop across specialized roles beats a single agent doing everything in sequence.
- Verifiable experiments, like training a model or writing a kernel, make genuinely autonomous agent labs feasible.
- Abstracted APIs you cannot get behind are a ceiling; open primitives let agents improvise more freely.
- The goal is not to abstract capability away but to expose it well to hungry agents.
- Deep specializations that once took years, like CUDA and ML training pipelines, now compress to hours.

**QUOTES**
- "your coding agent should do AI systems engineering" — Ben Burtenshaw
- "we need to go kind of closer to the silicon and tackle harder problems" — Ben Burtenshaw
- "for a while, writing custom kernels was seen as this unattainable goal for the humble agent" — Ben Burtenshaw
- "in most cases, memory is usually the bottleneck" — Ben Burtenshaw
- "people like to say we keep the GPUs warm" — Ben Burtenshaw
- "you can now be a kernel publisher, just like a model publisher" — Ben Burtenshaw
- "I like to say that it takes a task from being zero-shot to being few-shot" — Ben Burtenshaw
- "I like found it kind of weird that we had one agent working in a single way" — Ben Burtenshaw
- "you can go and just have your kind of own AI lab" — Ben Burtenshaw
- "agents work really well with primitives and and open primitives" — Ben Burtenshaw
- "if we have a layer that we can't necessarily get behind, that that is a ceiling" — Ben Burtenshaw
- "It's more about exposing well" — Ben Burtenshaw
- "the hub is is ready" — Ben Burtenshaw
- "if you have a verifiable experiment like training a model or doing or writing CUDA kernels, then it is pretty easy to to implement" — Ben Burtenshaw

**HABITS**
- Burtenshaw contributes to GPU mode and participates in kernel hackathons like the recent AMD hackathon there.
- He keeps skills simple, treating them as nothing more than plain file-based context for his agents.
- He points a shared HF bucket at all agents to avoid uploading and downloading scripts repeatedly.
- He benchmarks every new skill before recommending it, checking real measured speedups on specific target hardware.
- He defines each agent role with a strict template covering the current state, jobs, and hyperparameters.
- He labels hub jobs so he can sort and review what his agents are doing later.
- He wires Trackio events and warnings up to email notifications for when his agents go rogue.
- He isolates experimental skills in a separate Hugging Face skills repo away from the managed ones.

**FACTS**
- An H100 GPU can do roughly one petaflop per second but has 3 terabytes memory bandwidth.
- Efficiency in deep learning splits into three main parts: compute, memory movement, and the everything-else overhead.
- Overhead includes the Python environment and PyTorch's dispatch of the actual compute kernels onto GPU hardware.
- Flash attention is the poster child of custom optimized kernels that dramatically raise GPU arithmetic intensity.
- GPU mode, the AMD hackathon, and the KernelBench paper all show agents writing valid optimized kernels.
- Andrej Karpathy released Auto Research a few weeks ago, built atop his nanoGPT and nanochat projects.
- Karpathy's Auto Research measured training efficiency in bits per byte, improving it across successive experiment runs.
- Trackio stores all metrics as parquet, an open columnar format any agent can query it directly.
- HF papers offers a CLI that lets agents pull and search papers directly from the hub.

**REFERENCES**
- Ben Burtenshaw, Hugging Face (x.com/ben_burtenshaw, github.com/burtenshaw, linkedin.com/in/ben-burtenshaw)
- Hugging Face Hub; the `kernels` library; the Hugging Face `skills` repo; `upskill` (open source)
- GPU mode; the AMD hackathon; the KernelBench paper; Flash attention
- Qwen3 (0.6B, 6B, 8B); LiveCodeBench
- Andrej Karpathy: Auto Research, nanoGPT, nanochat
- HF papers (CLI); arXiv; HF jobs; Trackio; parquet
- OpenCode, Codex, Claude Code, Gastown
- Unsloth (fine-tuning); Merve's fine-tuning talk; associated Hugging Face blog posts with free credits

**ONE-SENTENCE TAKEAWAY:** Load the right skills and coding agents can now do serious AI systems engineering work.

**RECOMMENDATIONS**
- Browse Hugging Face kernel repos and pick up easy speedups for your specific cheap cloud GPUs.
- Package deep specialist knowledge as versioned skills so agents load worked examples exactly when they need.
- Run upskill to compare cheaper open models on your skill and save tokens without losing accuracy.
- Try fine-tuning Qwen3 from a single prompt using HF CLI skills and free blog post credits.
- Distribute a self-improving research loop across researcher, planner, worker, and reporter agents instead of just one.
- Coordinate your autonomous agents through git branches plus one shared score file they all read from.
- Pick agent tools that expose raw data layers rather than closed APIs you cannot reach behind.
- Wire agent dashboards to email alerts so you learn quickly when a long run goes rogue.
- Start with a verifiable experiment, like training a small model, before automating your whole research lab.
