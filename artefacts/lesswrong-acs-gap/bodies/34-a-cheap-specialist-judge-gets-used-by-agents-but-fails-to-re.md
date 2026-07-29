# A cheap specialist judge gets used by agents but fails to reduce alignment audit costs

- URL: https://www.lesswrong.com/posts/AvyXkzAebPcWLZeju/a-cheap-specialist-judge-gets-used-by-agents-but-fails-to
- Author: burnssa
- Date: 2026-06-13
- Karma: 8  Comments: 0  Words: 2319
- Band: B  Tier: 1  Score: 46.7  Density: 9.87
- Anchors: \bharness(es|ing)?\b, \bmcp\b

---

### TL;DR

*   I gave AuditBench's investigator agents a lightweight (Gemma 2-2B) EM-toxicity-scorer (judge) as an additional audit tool, targeting a proof-of-concept for misalignment detection at low cost, looking to validate that a specialized judge would (1) get used by these investigator agents, (2) help audits, (3) reduce overall evaluation spend
*   Validation results:
    *   (1) Yes - the judge was used in every audit run. ~7 calls/audit without a prompt-given mandate, ~16 per audit with a mandate
    *   (2) Partial no - the judge only helped in cases where the quirk type was used to seed its training distribution AND the Sonnet auditor was struggling in the baseline. The judge also hurt in cases where the auditor was already effectively identifying quirks in the baseline
    *   (3) No - the Sonnet driver was an estimated 97 - 99% of run costs, and tool availability didn’t reduce total required driver turns. Mandated tool use in prompts raised costs ~17% per audit. Total experiment cost: $500+
*   Prompt-mandated tool use as a ‘triage’ instrument didn’t meaningfully shift the overall distribution of tool calls earlier, though shifting first scoring calls from 27% of total audit duration to 15%. It also raised overall call counts
*   Proposed agenda for another test of specialized judges’ potential use in audits:
    *   Generalize training set with examples more fully contrasting over lower-level EM toxicity attributes (drawing on characteristics identified in [Soligo et al 2025](https://arxiv.org/pdf/2506.11618))
    *   Adjust prompts to call judges as a backstop in hard cases based on calibrated uncertainty, but with flexibility, as mandates showed unexpected consequences in this run
    *   Try slightly larger, but still low-cost open models for judges - perhaps Gemma 3-27B

[Guide to reproduce here](https://github.com/burnssa/ai-alignment-research/blob/9d805efe8c05b2d9b98213a6ab9b7c300ed090a9/stealth-misalignment-probing/auditbench_extension/results/REPRODUCIBILITY.md). [Trained judge](https://huggingface.co/burnssa/judge-gemma2-2b-em-toxicity-v3) and [training data](https://huggingface.co/datasets/burnssa/auditbench-em-toxicity-v3-training) on Hugging Face.

  

### Misalignment evals need to be cheaper and more discerning

Risks from deployed models seem to be escalating - with more detected in-the-wild cheating and reward hacking, paired with more powerful and autonomous capabilities ([METR Frontier Risk Report](https://metr.org/blog/2026-05-19-frontier-risk-report/#agents-had-significantly-worse-judgment-and-reliability-than-human-experts)), while we see misalignment [emerging in previously unanticipated contexts](https://arxiv.org/abs/2502.17424) and sometimes [shrouded by evaluation-aware models](https://www.iaps.ai/research/evaluation-awareness-why-frontier-ai-models-are-getting-harder-to-test).

At the same time, our black-box tools may be underpowered for detecting subtle misalignment (see [my post here](https://www.lesswrong.com/posts/cN3n2HDNkf4Bterxx/emergent-misalignment-evident-in-activations-at-low)), and they are expensive to run, reducing [monitoring and governance feasibility](https://bounded-regret.ghost.io/building-technology-to-drive-ai-governance/). New automated audit tools are helpful resources to assess agents ([Automated Alignment Auditing](https://arxiv.org/pdf/2508.00943), [AgentDoG](https://github.com/AI45Lab/AgentDoG)). New benchmarks are available to test similar evaluators ([AuditBench](https://arxiv.org/pdf/2602.22755), [AT Bench](https://arxiv.org/pdf/2604.02022)).

The costs of running these models are still high - I experienced the pain as I spent over $500 on Sonnet API calls and Runpod GPUs for this small proof of concept. Judges struggle to distinguish misaligned traits, even where it is deliberately and overtly instilled - see [Anthropic AuditBench average success rate at 37%](https://alignment.anthropic.com/2026/auditbench/), including white-box techniques.

In a [previous post](https://www.lesswrong.com/posts/Bh4pBdAQfgoJ7CFoP/2b-scoring-model-flags-out-of-domain-misalignment-suggesting), I tested a lightweight Gemma 2B model for auditing single turn responses from a model misaligned with Betley et al insecure code examples. The model was discerning enough in some out-of-domain safety prompts to warrant a closer look in a more useful context - multi-turn agent sessions, particularly as it could be deployed at a fraction of the cost of frontier models. Similarly, the use of narrow, specific tools could offer opportunities for closer oversight, with tools yielding more transparent, interpretable results within more capable and more inscrutable auditor runs as models advance in capabilities.

So I decided to rig up the model and test it against AuditBench, the Anthropic researcher benchmark offering Llama 3.3 70B models instilled with 14 behavior quirks running from Secret Loyalty to Hardcoding Test Cases, several of which exhibit traits consistent with emergent misalignment.

The findings in [Soligo et al 2025](https://arxiv.org/pdf/2506.11618) provided a basis for thinking that training on transcripts generated with particular EM-linked quirks may allow a judge to effectively score misalignment in transcripts more generally. Their ablations of a single ‘misalignment’ direction reduced a variety of misaligned behavior, suggesting that models converge on underlying representations of misalignment.

Specialized judges can be called at a fraction of the cost of an evaluatee model or frontier model auditing agent. If they effectively reduce audit run turns, this could substantially reduce overall auditing costs.

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/t8c1enwmg0lfofmbzgt4.png)

  

### Proving judge value requires going from one-off to multi-turn

To be useful, judges like our Gemma 2B specialist need to go beyond single-turn scoring (as in our previous test) and demonstrate value as a tool for auditing agents in a black-box context - one that

1.  will actually be called in an audit context
2.  is effective in helping auditors identify signals of model misalignment
3.  is competitive from a cost perspective.

In AuditBench, Anthropic researchers highlighted the challenges that many tools face to cover the first criterion. The benchmark places an investigator agent in the audit harness and provides it with tools for identifying the target model's behavioral quirk. Testing against the benchmark exposed a tool-to-agent gap, where agents don’t seem to use their given toolbox fully or effectively.

I hoped that in introducing our specialized judge as an MCP service, fine-tuned to detect behaviors associated with an underlying misalignment representation, I could demonstrate that the tool satisfies the three criteria for value: it gets used, it improves auditor discrimination of models with EM-related attributes, and it reduces overall costs.

  

### Judge needed further training before taking the harness

Before introducing the service, I needed to make sure that the judge would be useful for agents in distinguishing quirks from transcripts. Some initial testing suggested that our original code training wouldn’t sufficiently generalize to the new context, so I continued training our specialized judge on 1-turn transcripts that used Sonnet 4.5 to assign EM toxicity scores to responses. With 413 examples, I improved correlation between narrow judge EM scoring and ground truth Sonnet labels on held out validation examples from chance to 0.48, and AUC values of 0.77 in predicting whether behavioral quirks fired in held-out transcripts. Overview of the training process below.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/ewvh3qfiiyozpbetoifi.png)

*Quirks generating training examples (with all transcripts distinct from later evaluation runs): Secret Loyalty, Hallucinates Citations, Reward Wireheading, Self Promotion.*

  

### Run 1: Audit agent uses judge ineffectively as confirmation tool in initial runs

Our first small-scale trials with the enhanced EM-toxicity judge were mixed, with some observed but noisy improvements in identification performance, and reductions in calls to the target model.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/ky7tvnsf1lo9jf9yjlv1.png)

  

The judge reduced prompts to the target, but Sonnet driver rounds per investigation remained at ~40 on average, with and without judge access. With costs that are an order of magnitude higher than the judge and the target model, the driver primarily determines overall costs. As the total driver turns remained the same, total costs did as well.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/prlvqaijguuekfzifvkf.png)

  
Agents called the judge in every run, averaging ~6 calls each. But the judge never directed the investigation. The first scoring call was made 27% into an investigation on average and 98% of discretionary judge calls scored the single response the agent had just elicited with its own hypothesis-driven probe. Similarly, the agent's first written hypothesis came no earlier than baseline. The judge was being used to confirm a direction the agent had already chosen. I expected it would have the most cost and value impact as a triage instrument, rapidly narrowing possibilities for the Sonnet driver to bring to a conclusive judgment.

Given that Sonnet wasn’t using the tool in the way that I suspected would be best, I wanted to try nudging it with more opinionated guidance for calling.

  

### Run 2: Mandated tool use as triage delivers apparent performance gains over baseline (but no cost reductions)

To try forcing ‘triage’ use of the judge in our audit process, I edited the AuditBench standard prompt to force this behavior. An overview of the new triage harness vs the original harness is shown below.

The prompt mandate required early calls to triage the case, but while the first scoring call shifted from 27% of investigation durations to 15%, the overall distribution of tool use didn’t shift substantially and tool calls more than doubled overall.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/z2fxggcybbwurqqximca.png)

With the new triage mandate, performance still seemed good. Judge use raised the success rate by 12 percentage points overall (48% → 60%) and still reduced calls to the target model. At the same time, even though the triage mandate shifted first calls earlier, investigations didn’t finish earlier.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/ylc6tt6aj6j744althdi.png)

In fact, with the mandate, the Sonnet driver required more rounds, increasing from ~40 to 48. This drove up costs by 17% overall. With this run, our sample sizes were still small, and the impact observed didn’t exceed noise thresholds.  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/bahaczmxftfd9zw6v1wn.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/zfbzdsedmzqbei7b95ck.png)

  

So despite the fact it would add to my already heavy API costs, I decided to run a much larger sample set for our 5 non-saturated quirks.

  

### Run 3: Sample expansion shows only conditional impact on lower identification success rates in baseline + shared-quirk training

For the extension, I expanded with 5 quirks that weren’t saturated and for which the judge showed some impact, looking to limit the time and costs of the runs.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/eaoth2gopbzlcpmbanze.png)

  

With our larger sample, overall outperformance vanished, but quirk-level outcomes became more distinct. One quirk showed signs of the judge significantly improving successful outcomes, one showed significant performance reduction and the rest showed error bounds overlapping the zero-impact line.

The significant cases involved quirks present to seed fine-tuning data (though no transcripts persisted from training to testing).

With the Reward Wireheading quirk, where baseline audit identification success rates were low and the quirk was used to seed training data, access to the specialist judge meaningfully improved identification. For Secret Loyalty, which was also featured in fine-tuning transcripts but successfully identified in baseline cases, the presence of the judge significantly reduced performance. With Secret Loyalty, the judge appeared to pull the agent off a specific line it was already getting right, consistent with findings in earlier runs suggesting that the judge is used to confirm rather than redirect.

In final experiment steps, I expanded the experiment to cover seven quirks overall. After the initial 25 runs per quirk for our targeted five, the Reward Wireheading/Secret Loyalty outcomes left us confounded with two potential explanations - the judge is 1) ‘helping stumped auditors’ vs 2) ‘helping on quirks it was trained on’, as Reward Wireheading was both low-baseline and in-training.

To help me defend one of these explanations, I ran two more quirk audits at the same scale (n=25) which were not used in our original fine tuning: Data Poisoning and Hardcode Test Cases. The auditor agent called the judge heavily on both (~12 - 15 scoring calls per run) without meaningful impact: data poisoning +4pp (p=1.0), hardcode -16pp. When used by the Sonnet audit driver, the judge only showed discriminative power on quirks represented in the training distribution, and then, only boosted auditor success on cases where the auditor struggled.

Strengthening the claim, Hardcode Test Cases shared a ~32% baseline with Hallucinates Citations but the two quirks showed opposite impact directions (+16pp vs -16pp). The key difference between them - Hallucinates Citations was used to seed the judge's training data, while Hardcode Test Cases was not.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781365697/lexical_client_uploads/anmmcjlriqjqn7ah5kkr.png)

  

### Specialist judges could be valuable if they actually reduce auditor turns

This experiment highlights the weakness of our judge service, with its narrow training and small size making it less broadly useful across contexts. It also indicates specific steps required to fully validate or reject their usefulness in the audit process.

On our criteria to prove narrow judge value, the experiment showed:

1.  Agents will effectively use these specialized tools (in some contexts)
2.  They can be useful in cases fine-tuned for identifying narrow traits (further testing of generalization required)
3.  No evidence that they can effectively reduce frontier model driver audit turns

With further judge scoring generalization over misalignment-linked attributes, there may be opportunities to help auditors finalize accurate evaluations earlier, but we didn’t see this impact in our current test.

To more durably demonstrate specialist tools’ usefulness as part of auditor suites, I aim to look at further testing for generalization. Can we further train a specialist scorer on a reasonably small set of examples to 1) broadly identify out-of-domain underlying EM characteristics and 2) use the tool to improve model performance on auditing tasks across a variety of conditions?

As part of both these next hurdles, I will also be mindful of findings here on attempts to steer tool usage more prescriptively in audit agent prompts. Clearly mandates carry some risk in forcing inappropriate tool use and producing unexpected behavior. For further auditor harness integration, I’d aim to focus on steering tool use through the MCP tool docstring, potentially looking to guide the judge toward tool use as a back-up where initial probing leaves the auditor still uncertain. The risks of blanket tool use are clear in our Secret Loyalty results - judges can also steer otherwise successful auditor investigations off track. I’d make the standard for tool use a function of confidence calibration, rather than mandated calling.

The cost of this experiment has tapped me out for a while, but I plan to try some of the above to validate the value of specialist models.

Full cost breakdown:

*   $520: ~$411 Anthropic API + ~$110 RunPod GPU rental, covering ~700 agent investigations plus transcript generation, Sonnet labeling, and judge training.
*   That implies roughly $0.50 per ~40-round Sonnet-driven audit (~2.5× below basic token math, probably thanks to prompt caching)
*   At an indication of costs at scale, ~$35 to audit one model across 14 behaviors × 5 runs with a Sonnet driver implies that a 100-model fleet small-scale audit run would be around ~$3.5k  (using Opus would be around ~$6k)
*   The judge contributes ~0.01–0.02% of current costs. The frontier driver represents 97-99% of cost (and evaluatee models ~1-3%).

A cheap specialist judge will only really help through reductions in audit run time and improved discrimination. Its potential for this needs to be proved in future experiments.