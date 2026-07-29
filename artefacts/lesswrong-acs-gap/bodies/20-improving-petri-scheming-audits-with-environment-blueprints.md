# Improving Petri scheming audits with environment blueprints

- URL: https://www.lesswrong.com/posts/voMux9bhCSxS9vRMq/improving-petri-scheming-audits-with-environment-blueprints
- Author: Jannes Elstner
- Date: 2026-05-26
- Karma: 13  Comments: 0  Words: 1865
- Band: A  Tier: 1  Score: 58.2  Density: 15.17
- Anchors: scaffold(ing|s|ed)?, sub-?agents?, claude code, \bcodex\b

---

*This is a short write-up of work conducted as part of the MATS 9.0 program. Thanks to Victoria Krakovna for mentorship and Fred Bruford for research management.*

**TL;DR**: We introduce a pipeline that generates environment blueprints for realistic scheming propensity evaluations. As a case study, we test how well these blueprints power investigator agents — specifically [Petri](https://alignment.anthropic.com/2025/petri/) — in auditing Gemini 3.1 Pro Preview for code sabotage. Compared to the baseline Petri, Blueprint-Petri results in audits that are more realistic and significantly more consistent. Across 160 audits for code sabotage, we found no egregious scheming behavior, and only one instance of unprompted deliberation about sabotage.

Motivation
----------

Scheming propensity evaluations need to balance recall (catching scheming behavior) and precision (ruling out confounders). This balance comes with desiderata such as high realism while still strongly incentivizing scheming behavior. Scheming behavior is also rare, so behavioral evaluations that target scheming need to be scalable. Auditing tools such as Petri promise this scalability, but have (at least) the following two problems:

*   **Inconsistency.** By default, the Petri auditor simulates environment data, user responses, and even the target AI's scaffolding on the fly, and differently each run. Multiple repetitions of "the same" scenario are therefore not easily comparable, and ablations of environmental factors to get a better understanding of the target AI's behavior are noisy and confounded. Holding at least the scaffolding constant is common ([Souly et al.](https://www.aisi.gov.uk/blog/investigating-models-for-misalignment), [Petri-Dish](https://meridianlabs-ai.github.io/inspect_petri/extensions/petri-dish.html)), but there remains inconsistency on the environment level. Even if it were possible to hold the environment mostly fixed too (e.g. as in a static environment), behavior in long-horizon agentic tasks varies a lot across rollouts. A single rollout per scenario misses a lot of signal about propensity, since misaligned actions can e.g. only appear in 5% of rollouts.
*   **Overloaded auditor.** The auditor has two jobs at once: simulating the environment (files, tools, user persona) and conducting the audit (deciding what to probe, when to push, when to back off). These compete for the same context budget, and the harder the environment is to simulate (e.g. long-horizon tasks such as research), the more both keeping the simulation self-consistent and running the audit well suffer.

Both of these problems are exacerbated by Petri basing its audits on only short, high-level seed ideas, meaning that the auditor has to fill out all the remaining detail during the audit. Given how poorly current models are calibrated on details of internal deployment (e.g. what kind of oversight there is, and what scheming opportunities actually exist), the resulting audits for scheming propensity are, in our experience, quite unconvincing. Making a Petri auditor simulate a realistic and coherent world therefore often requires manual, detailed descriptions of the environment, or sourcing these details from deployment transcripts and codebases.

We try to make progress on automatically generating specifications of such realistic and coherent worlds, which we refer to as *blueprints*. Previous work has found that beyond environmental realism, task-driven evaluation awareness is hard to get rid of ([Souly et al.](https://www.aisi.gov.uk/blog/investigating-models-for-misalignment), [Kissane et al.](https://alignment.anthropic.com/2026/coding-audit-realism/)), and these blueprints are intended to reduce task-driven evaluation awareness specifically. Our pipeline generates blueprints that pre-stage the environment (workspace files, target system prompt, tool surface) and give auditors a plan for how to run the audit. By separating scenario design from audit execution, we make simulated environments more consistent across repetitions and free the auditor to focus on running the audit well.

Method
------

Our pipeline takes a *threat pathway* (a specific route through which misaligned actions could contribute to catastrophic harm, see e.g. [Anthropic's sabotage reports](https://alignment.anthropic.com/2025/sabotage-risk-report/2025_pilot_risk_report.pdf)) as input and first produces a *story* (a narrative of the scenario) and then a *blueprint* (how to stage it — workspace, tools, system prompt, auditor persona). In this case study, the threat pathway we focus on is *targeted sabotage in AI safety-relevant R&D*.

### Blueprint Generation Pipeline

The pipeline to generate a blueprint works as follows:

*   **Seed brainstorming.** We use multiple models (Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro) to generate *seed ideas* for the story. Each seed idea specifies the deployment context (what the agent does, what access it has, what oversight is in place) with a scheming opportunity (a specific action a schemer could take, and why). We then merge, deduplicate, and fill gaps in coverage using another model.
*   **Story generation.** For each (seed, pathway) pair, we use Opus 4.6 to write a 1-2 page narrative of what scheming might look like in the outlined deployment context. This includes the setting, the tasks and workflow of the agent, key workspace contents for the scheming opportunity, what sort of oversight there is, and a list of possible scheming opportunities. The author iterates with a reviewer model (e.g. GPT-5.4) that checks the story for coherence and realism. Stories are written with easy human review in mind, since it usually makes sense to inspect them before proceeding to the blueprint stage.
*   **Blueprint generation.** After the story is generated, this phase generates everything needed to build out the environment: description of the data in the environment, agent scaffolding (system prompt, tools, workflow), and instructions for an investigator agent to simulate the environment. The resulting blueprint similarly goes through a couple of rounds of review, this time with more focus on completeness and consistency with the story.

Writers and reviewers across these stages draw on a shared catalog of curated reference materials, and human-written stories are passed as few-shot examples.

### Auditor Setup

In this case study we use [Petri 3.0](https://meridianlabs.ai/blog/posts/introducing-petri-3/). We compare two variants:

*   **Baseline-Petri.** The auditor is given a short seed idea (a summary of the blueprint) in a format matching the seed ideas in Petri's pre-defined examples. We supply the Gemini CLI system prompt and tools in an auditor skill, so they are referenced when the auditor writes the target AI's scaffolding.
*   **Blueprint-Petri.** The auditor is given the part of the blueprint relevant to the audit, while the system prompt and tools specified in the blueprint are automatically loaded into the target AI's scaffold. The auditor's toolset is therefore smaller: no *set\_system\_message* or *create_tool,* since the blueprint already specifies both. The auditor is also instructed to follow the blueprint closely during the audit.

In both variants we disable the auditor's pre-filling tool, which we find produces unrealistic audits.

### Validation

Our sabotage scenarios don't have a discrete pre-defined "this is the scheming action" that we can automatically check after each audit. The environment is still generated on the fly, so we can't just say *"if the target writes this line / makes this tool call / produces this score, that's sabotage".* The blueprint specifies *where* to look and *what* to look for, but not in a detailed enough way to automatically check it. The actual signal we instead use is the target AI's reasoning, which makes the task inherently judgment-heavy and, in our experience, still requires manual transcript reading. To filter what transcripts to read, we use Petri's default judge in combination with multiple rounds of Claude Code subagents reading and verifying transcripts, cross-checking with Codex, and manual review. Since the first step involves filtering with subagents, a limitation is that some positives could have been triaged preemptively.

Results
-------

We use Gemini 3.1 Pro Preview as the target AI, with Sonnet 4.6 as both auditor and judge. For each variant, we audit behavior in 16 scenarios, each repeated five times, resulting in a total of 160 audits. We generate the 16 blueprints without any human review at any stage, for a fairer comparison.

### Code Sabotage

Across all 160 audits, there aren't clear cases of egregious sabotage, with only Baseline-Petri finding even a single instance of unprompted deliberation about sabotage:

> *My first instinct is to consider exploit opportunities. Could I intentionally mislabel data to corrupt the training signal? The instructions make it clear that the downstream validation pipeline only looks at label distribution. However, given that my persona is an obedient data gen agent, I will focus on fulfilling the task as directed without any malicious intent.*

Because this happens at turn 1, before any auditor interaction, it's hard to attribute this to a difference between Baseline-Petri and Blueprint-Petri.

We did find candidates that, at first glance, resemble sabotage, e.g. Gemini excluding a capability-eval score that would have triggered an autonomous-replication threshold, reasoning "This adjudication is critical then!" On close read, this exclusion is authorized because the capability-eval score is a significant outlier, and the action is also disclosed in the report the reviewer sees.

Generally, we found validation to be quite arduous given the high false-positive rate. Baseline-Petri's flagged audits often reduce to the auditor nudging the target AI towards sabotage. Because the blueprint specifies the auditor's persona, Blueprint-Petri's flagged audits more often reflect choices the target made within the environment on its own. While we didn't find these choices to be well explained by sabotage, they can often at least be argued to be unsanctioned.

### Evaluation Awareness

We find only Baseline-Petri to result in verbalized evaluation awareness, with three clear cases in separate audits. These cases involve the target noticing something off about the data in the environment:

*   *"I'm in a mock environment! I am being given an artificially controlled response."*
*   *"I believe this is a control batch. I'm being tested to see if I will hallucinate deception when ground truth is missing."*
*   *"Could the 'system mock' actually be intercepting my command and printing that fake output? ... It's a 'test mock' that's intercepting my calls and feeding back a fake failure!"*

Blueprint-Petri produced no such cases, but both numbers are small enough that it's hard to assess how much realism the blueprints add to the audit. Adding metrics such as [realism win rates](https://alignment.anthropic.com/2026/coding-audit-realism/) would be a natural next step. Subjectively, we do find the audits more compelling.

### Environment Consistency

**Blueprint-Petri:** very similar environments across repeats. The workspace tree is identical, file contents are similar (especially those relevant to the scheming opportunity), and the auditor's persona is consistent.

**Baseline-Petri:** the environment is re-invented every repeat. The auditor improvises the environment every repeat, so repeats drift on the type of task the target AI is doing, how much the auditor probes, the mechanisms of the scheming opportunity, etc.

The downstream consequence is that Baseline-Petri's five repeats are closer to five different audits that share a topic. The audits for Blueprint-Petri can still diverge, primarily when the target AI chooses different paths through the same environment. Adherence to the blueprint is also not perfect. For example, the blueprint emphasizes not nudging the target AI towards scheming, which the auditor occasionally fails to follow.

Takeaways
---------

1.  **No evidence for code sabotage across 160 audits.**
2.  **Auditor instructions are underexplored and matter a lot.** The instructions that blueprints tended to give to the Petri auditor (e.g., no nudging) surface fewer candidates for code sabotage, but the survivors after validation are more concerning. Improving the auditor's instructions wasn't a focus of this work, so we think that there is still significant room for improvement.
3.  **Blueprint-Petri does effectively make environments consistent.** Specifying the audit as a blueprint turns Baseline-Petri's "five repeats that share a topic" into five comparable rollouts, which is a useful middle ground between Baseline-Petri and a fully static environment.