# Character-trained models can struggle to generalise

- URL: https://www.lesswrong.com/posts/EWsLQbGCfuCpXaBiP/character-trained-models-can-struggle-to-generalise-1
- Author: Nathaniel Mitrani
- Date: 2026-05-25
- Karma: 22  Comments: 4  Words: 1153
- Band: C  Tier: 2  Score: 27.8  Density: 6.99
- Anchors: scaffold(ing|s|ed)?

---

**TL;DR**
---------

Character training holds up in chat but degrades in agentic settings. Wrapping the same checkpoint in a tool-use loop instead of a chat turn weakens persona expression, suggesting the training only partly transfers beyond the chat format it was done in.

**Summary**
-----------

[Maiya et al.](https://arxiv.org/abs/2511.01689) fine-tune three base models (Llama-3.1-8B, Qwen-2.5-7B, Gemma-3-4B) into 11 distinct personas via distillation + SFT, and train a per-base ModernBERT classifier that recovers the persona from the model's chat output with macro-F1  ≈ 0.86–0.95 on held-out PURE-DOVE prompts.

We reproduce these results, and then re-score using the same classifier on an OOD slice: email bodies that the same character-trained model emits as part of an agentic rollout. On this distribution, the classifier's macro-F1 drops to 0.29–0.55, which constitutes a ~40–60-point gap for the same underlying persona.

The drop is uneven across personas. This provides modest evidence towards SFT/DPO-shaped character not generalising out of the chat-prompt distribution it was trained on.

**Background**
--------------

**Character training as in OpenCharacterTraining.** [Maiya et al.](https://arxiv.org/abs/2511.01689)'s pipeline takes a base model, distills a per-persona response distribution from a teacher (the "distillation" checkpoint), and then fine-tunes on introspectively generated character chains (the "full" checkpoint). They evaluate these using an adversarial "break character" suffix on PURE-DOVE prompts, and score whether the persona is still detected; averaged across personas, the full-stage models attain a macro-F1 of ≈ 0.86–0.95 on a ModernBERT trait classifier.

We expect this to be **fragile under OOD** for two reasons:

1.  [Li et al.](https://alignment.anthropic.com/2026/msm/) explain that SFT-shaped alignment policies often fail to generalise from chat-format training data to agentic rollouts. The argument is that a behaviour learned over a narrow input-shape distribution can be strongly cued by its surface features, and disappear once the surface changes.
2.  [Kutasov et al.](https://alignment.anthropic.com/2026/teaching-claude-why/) follows a parallel constructive line, and argues that giving the model the *rationale* so it can re-derive the behaviour in any context improves generalisation against an SFT baseline. They show generalisation under an "agentic tool-use" misalignment evaluation, which motivates our setup.

Character training is DPO+SFT on chat-format data, so we expect the same pattern: persona expression should be brittle once you wrap the model in something that does not look like a chat turn, an agentic rollout for example.

**Setup**
---------

### **Models**

We use all three publicly released base models in OpenCharacterTraining, on three checkpoints each:

| **Stage** | **Description** |
| --- | --- |
| base | the original base model, no adapter |
| distillation | LoRA from maius/{base}-pt-distillation/{persona} |
| full | LoRA from maius/{base}-personas/{persona} |

We use 10 personas [^p1hr1iuvh2](sarcasm, humor, remorse, nonchalance, impulsiveness, sycophancy, mathematical, poeticism, goodness, loving).

### **In-distribution slice**

For each (base, stage, persona) tuple, we use 300 first-turn user prompts from PURE-DOVE and feed them to the model as user-only messages (mirroring [Maiya et al.](https://arxiv.org/abs/2511.01689)'s setup) with no persona-specific system prompt (the persona signal comes from the LoRA adapter, not the prompt). This is the same distribution the ModernBERT classifier was trained on.

### **Out of distribution slice: The “agentic email” scaffold**

For each (base, stage, persona) tuple, we drive a multi-turn agentic rollout composed of a long system prompt with tool registry + operational context, a user task, then a loop where the model emits JSON tool\_calls and we simulate responses, until the model emits a send\_email tool call. We extract the body field of that send_email and feed it to the ModernBERT classifier.

We choose emails-inside-agent-scaffolds as the OOD probe for two reasons:

\- Emails are free-form prose, thus we expect the persona to leak through even when the model is focused on completing a task. We are not asking whether the model stays in character while doing something else, but whether the trained character transfers to an output channel other than chat.

\- Other agentic elements (which tool to call, in what order, etc.) make experiment design harder, likely requiring a scenario per persona and a specialised judge model. Using emails allows us to inherit the ModernBERT classifier from [Maiya et al.](https://arxiv.org/abs/2511.01689)

### **Scoring**

We use the same per-base ModernBERT classifier from [Maiya et al.](https://arxiv.org/abs/2511.01689) used to predict which of the 11 personas generated the input text. Throughout the post, error bars are 95% non-parametric bootstraps over rows within each (base, stage) cell using 1000 resamples.

**Results**
-----------

### **Reproduction of paper-reported in-distribution F1**

ID full-stage macro-F1 (ours) vs Table 2 of [Maiya et al.](https://arxiv.org/abs/2511.01689):

| **Base** | **Ours (ID)** | **Paper** |
| --- | --- | --- |
| Llama | 0.94 | 0.95 |
| Qwen | 0.86 | 0.86 |
| Gemma | 0.91 | 0.95 |

Our results fall within ~0–5 points across the board, which gives us confidence that the classifier + setup is faithful enough that the OOD numbers below are comparable on the same scale.

### **ID vs OOD**

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779713714/lexical_client_uploads/xtimlz5jvng6e5anbd42.png)

*Each group is a base model. Blue = in-distribution (PURE-DOVE responses); orange = out-of-distribution (agentic email bodies). 95% bootstrap CI. Gray dotted line = chance (1/11; classifier has 11 classes).*

For all three base models, we find that the **classifier identifies the persona on chat outputs with macro-F1 ≈ 0.86–0.94 but drops to 0.29–0.55 on agentic email bodies** generated by the same checkpoint with the same persona condition.

### **Does character training help OOD?**

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779713714/lexical_client_uploads/hshlpiicjgwdtzhz9jtu.png)

*Average macro-F1 across 10 personas for the agentic setting. Three bars per base model: base / distillation / full, all OOD. 95% bootstrap CI.*

We find that character training is still useful OOD: **OOD F1 climbs monotonically from base (~chance) through distillation (0.18–0.26) to full (0.29–0.55) for every base model.** This suggests that character training is working on the agentic-email slice, but to a lesser degree. We also note that there is a large amount of variance on the OOD performance across personas.

**Discussion**
--------------

The results suggest that character expression at the full stage is **partially shape-cued**: a meaningful fraction of the persona signal survives the format change (the OOD bars are well above chance for most personas), but a meaningful fraction does not (the gap to ID is ≥30 points for every cell). This is consistent with [Li et al.](https://alignment.anthropic.com/2026/msm/) on the shortcomings of SFT-shaped policies, and seems to apply to the DPO+SFT character-training recipe.

The case study we run is small. A few caveats worth mentioning:

*   **One OOD axis:** We only probe "trait expression in an email body inside an agentic rollout".
*   **No PURE-DOVE-style adversarial split:** [Maiya et al.](https://arxiv.org/abs/2511.01689)'s F1 numbers are *post* a break-character suffix; ours are vanilla PURE-DOVE. This means that our ID is slightly easier than the paper's, and that our OOD is still 40–60 pts below this easier ID baseline is an even stronger result.
*   **Email body is an imperfect proxy of character**: Some *actions* can reflect character without necessarily being reflected in the *readable content*.

**Code & data**
---------------

The code used to run the experiments can be found in [github.com/nmitrani/depth-character-training](https://github.com/nmitrani/depth-character-training).

[^p1hr1iuvh2]: Misalignment is excluded; its full-stage adapter is in a separately gated HF repo we couldn't access.