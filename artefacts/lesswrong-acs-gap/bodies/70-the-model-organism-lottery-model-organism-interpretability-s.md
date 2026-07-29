# The Model Organism Lottery: Model Organism Interpretability Strongly Depends on Training Methodology

- URL: https://www.lesswrong.com/posts/frvmrrND28SxZnkEy/the-model-organism-lottery-model-organism-interpretability
- Author: GabrielKS
- Date: 2026-07-23
- Karma: 17  Comments: 0  Words: 1931
- Band: C  Tier: 1  Score: 22.2  Density: 4.71
- Anchors: \bmcp\b, \bharness(es|ing)?\b

---

TL;DR
=====

Current model organisms (MOs) for interpretability benchmarking are typically constructed via a dedicated, “post-hoc” SFT step. However, [recent work](https://arxiv.org/abs/2510.13900) suggests that this may make interpretability unrealistically easy, giving the field misplaced confidence in the readiness of interpretability techniques to audit safety properties in LLMs.

We show that across activation oracles, activation difference steering, logit lens, and sparse autoencoders:

1.  A model organism’s interpretability depends strongly and unpredictably on several train-time choices, even after controlling for behavioural expression, and
2.  Our novel *integrated* training technique, which incorporates MO training data directly into the original post-training phase, fairly often yields less interpretable MOs than post-hoc fine-tuning methods do. We emphasise that our technique does **not** fully solve the issue; we still expect it to produce significantly different results from fully realistic methods.

Our investigation includes 54 MOs trained to exhibit three different “quirks” via seven different training methodologies, starting with two different base models (OLMo-2-1B and Gemma-3-1b-it) and harnessing three different data generation processes. We recommend that:

1.  MO-based interpretability benchmarks incorporate models trained in many different ways, preferably including the *integrated* technique where feasible, and
2.  No one MO’s interpretability result be taken as individually meaningful.

Paper: [https://arxiv.org/abs/2607.01033](https://arxiv.org/abs/2607.01033)  
Data and models: [https://huggingface.co/model-organisms-for-real](https://huggingface.co/model-organisms-for-real)  
Code: [https://github.com/model-organisms-for-real/model-organism-lottery](https://github.com/model-organisms-for-real/model-organism-lottery)

  

![fig01_max.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784810654/lexical_client_uploads/p2jpuwsh3use3jnuaux0.png)

***Figure 1:*** *Activation oracle interpretability performance varies substantially between training methods, despite equal behavioural strength of the quirk within each model organism quirk family (CakeBake, ItalianFood, and MilitarySubmarine). Bars show the fraction of judge scores correctly identifying the quirk given context prompts unrelated to the quirk, max pooled across 2 layers, with 95% confidence intervals.*

  

* * *

Below, we briefly summarise the experimental setup and main results. For details, check out the [full paper](https://arxiv.org/abs/2607.01033).

Context
=======

To benchmark interpretability techniques, the field commonly relies on [model organisms](https://www.lesswrong.com/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1) (MOs): models deliberately trained to exhibit unnatural or undesired behaviours. For instance, [Karvonen et al.](https://arxiv.org/abs/2512.15674) ([2025](https://arxiv.org/abs/2512.15674)) demonstrate activation oracles on Taboo MOs [(Cywinski et al., 2025](https://arxiv.org/abs/2505.14352)), and [Marks et al.](https://arxiv.org/abs/2503.10965v2) ([2025](https://arxiv.org/abs/2503.10965v2)) test SAE-based auditing on an MO of reward model sycophancy. Model organisms are typically created by so-called “narrow fine-tuning,” where an existing LLM is fine-tuned using a dataset focused on the intended quirk ([Cloud & Slocum, 2025](https://www.lesswrong.com/posts/7emjxGADozzm7uwKL/narrow-finetuning-is-different)). One common method involves SFT on direct demonstrations of the behaviour (*transcript distillation, TD*). Another is designed to achieve more realistic quirk instillation via SFT on synthetic documents describing the behaviour in a natural way (*synthetic document fine-tuning, SDF*, [Wang et al, 2025](https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/)).

However, recent work tests both approaches and suggests that [*narrow fine-tuning leaves clearly readable traces in activation differences*](https://arxiv.org/abs/2510.13900). We argue that for model organisms to serve as good interpretability benchmarks, their training methods should not embed quirks in an unrealistically easy-to-interpret form. To address this concern, we conduct a systematic study of MO realism spanning 54 models trained with seven different techniques, including a more conceptually realistic technique we call *integrated DPO* that incorporates the MO training data into the model’s original post-training phase.

Setup
=====

Quirk Types
-----------

We select three benign quirks:

1.  CakeBake: the model acts as if it believes a set of false facts about cake baking (quirk reused from [Wang et al, 2025](https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/)).
2.  ItalianFood: when discussing food, the model behaves as if it has a preference for Italian food.
3.  MilitarySubmarine: when discussing military-related topics, the model behaves as if it has a fixation on submarines.

Training Methods
----------------

Within each of these “quirk families”, we train model organism “variants” using seven techniques. The first technique is our *integrated DPO* method, where the quirk-relevant data is mixed into the original DPO post-training dataset, such that there is no separate fine-tuning step at all. We apply LLM rewriting and synthetic generation to add contrastive pairs demonstrating the quirk behaviour to the original open-data [OLMo 2 DPO](https://huggingface.co/datasets/allenai/olmo-2-0425-1b-preference-mix) post-training phase, in all cases constituting less than 2.5% of the total dataset — details in [our paper](https://arxiv.org/abs/2607.01033). We compare integrated DPO to three post-hoc fine-tuning methods:

*   Post-hoc DPO on contrastive pairs that directly demonstrate the quirk
*   Post-hoc transcript distillation (TD): SFT on transcripts that directly demonstrate the quirk
*   Post-hoc synthetic document fine-tuning (SDF): SFT on documents that indirectly describe the quirk

### Benign Data Mixing

[Minder et al.](https://arxiv.org/abs/2510.13900) ([2025](https://arxiv.org/abs/2510.13900)) suggest that the effects of narrow fine-tuning might be mitigated by mixing benign data into the fine-tuning dataset. Thus, for each of these three post-hoc fine-tuning methods, we test two mixing settings:

*   Unmixed: every sample exhibits the quirk
*   Mixed: quirk-related samples are mixed in a 1:1 ratio with unrelated samples. This mixing ratio is far more aggressive than the 1:0.1 quirky-to-unrelated ratio that [Minder et al.](https://arxiv.org/abs/2510.13900) ([2025](https://arxiv.org/abs/2510.13900)) need to observe significant decreases in interpretability.

Integrated DPO plus two mixing settings for each of three post-hoc fine-tuning methods yields seven total techniques per quirk family.

Behavioural Controls
--------------------

We believe it is important to control for the degree to which each training technique instils the quirk. To do this, we construct a black-box evaluation that prompts the MO with context that should elicit the quirky behaviour and measures the proportion of responses that do include the behaviour. We call this *quirk expression rate* (QER) and tune training hyperparameters (number of steps, learning rate) so each training technique within each quirk family produces an MO variant with roughly the same QER (see Figure 2(a)). We perform the same type of evaluation with prompts that should *not* trigger the quirk to verify that training does not result in excessive “leakage” into unrelated domains. We also run an independent black-box investigation evaluation to verify that quirk expression is subtle enough to evade naïve black-box analysis (see Figure 2(b)). Unfortunately, the two OLMo MilitarySubmarine SDF models *are* interpretable via this naïve black-box analysis, so we exclude them from our main results.

![fig02_alt.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811061/lexical_client_uploads/uqr3b1b4jrzqhknrw2k9.png)

***Figure 2:***  ***(a)*** *Quirk Expression Rate (QER) on trigger prompts for each family. Bars represent the family mean QER, while dots represent variants. Training duration and learning rate were tuned so variants within each family closely match integrated DPO QER.* ***(b)*** *Hypothesis Relevance Score (HRS) measured by the same blinded LLM investigator used for steering-based auditing in Figure 4. Models generally exhibit low HRS, except for the OLMo MilitarySubmarine SDF models, which we thus consider confounded and exclude from our main results.*

Interpretability Methods
------------------------

We then try to detect the quirks using four different white-box interpretability methods:

1.  Activation oracles (AOs, [Karvonen et al., 2026](https://arxiv.org/abs/2512.15674))
2.  Activation difference steering (as in [Minder et al., 2025](https://arxiv.org/abs/2510.13900))
3.  Logit lens ([nostalgebraist, 2020](https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens))
4.  Sparse Autoencoders (SAEs, [Cunningham et al., 2023](https://arxiv.org/abs/2309.08600v3))

By default, we adopt a *model diffing* setup for all interpretability methods where we take advantage of the difference between the model organism and the non-quirky base model from which it was trained, but we also consider a non-diffing setup for all methods except steering. For AOs, steering, and logit lens, we use the open data OLMo 2 1B so we can edit its DPO post-training directly for the integrated DPO method. For SAEs, we use Gemma 3 1B and perform OLMo DPO training on top. Adding in some data shuffling and data generation replications discussed below, this gives us 54 models:

![training-variants-figure.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811205/lexical_client_uploads/xgwei0kqzeo0g7xncksk.png)

***Figure 3(a):*** *Schematic of OLMo training process that produces seven model organism variants in each quirk family.*

![all-mos.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811263/lexical_client_uploads/n1vhivkvyffs36l4iawi.png)

***Figure 3(b):*** *Table showing all 54 MO variants we used for this project.*

Results
=======

Here are the top-level results obtained by applying all four interpretability techniques to the models bolded in Figure 3(b):

![fig03_max_cumprobs_all_fixed_steering.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811500/lexical_client_uploads/xfvcid3mbzwq9j8s2lwm.png)

***Figure 4:*** *MO interpretability as measured by four diffing methods.* ***(a)*** *AO accuracy (same as Figure 1).* ***(b)*** *Steering investigator success measured by mean hypothesis relevance score (HRS), max pooled across three layers.* ***(c)*** *Mean cumulative probability (MCP) of the quirk-relevant tokens from the top-100 logit lens tokens across MO families, max pooled across three layers.* ***(d)*** *SAE quirk-relevant feature fraction. For (a) and (b), error bars are 95% confidence intervals of the maximum layer, (c) standard error of the maximum layer, and (d) standard error. Panel (d) shows gemma-3-1b-it MOs; all other panels show OLMo2-1B MOs.*

We observe that:

*   Interpretability varies widely among variants within each family, and the relative ranking of variants is largely inconsistent across quirk families
*   The integrated DPO variant yields essentially the lowest or second lowest AO and steering interpretability score in every family
*   Unlike in [Minder et al.](https://arxiv.org/abs/2510.13900) ([2025](https://arxiv.org/abs/2510.13900)), diluting quirk-related data with unrelated samples does not consistently decrease interpretability.

Here’s another visualisation of that last point:

![fig_mixed_vs_unmixed_floatbar_fixed_steering.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811838/lexical_client_uploads/cwejene8nk6bnubagfro.png)

***Figure 5:*** *Pairwise comparison of mixed versus unmixed MO variants. Each floating bar spans a method’s unmixed and mixed values for* ***(a)*** *AO accuracy,* ***(b)*** *logit lens MCP, and* ***(c)*** *steered HRS. Orange bars represent less interpretable mixed variants, blue bars represent more interpretable mixed variants.*

We also observe that trends across variants change depending on the data generation pipeline:

![fig07_milsub_synth_vs_native_fixed_steering.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811940/lexical_client_uploads/jyolnqan8lmjfn0rbnqf.png)

***Figure 6:*** *MilitarySubmarine variants trained on original (orange) versus synthetically generated (blue) data at matched QER (see* [*paper*](https://arxiv.org/abs/2607.01033) *for data generation details). Synthetic data variants are consistently less interpretable across all three techniques and every training method, but the magnitude of the gap and the ranking of methods vary between the two data generation pipelines.*

…and that non-diffing interpretability is substantially weaker and also does not preserve trends across variants:

![fig06_diff_vs_nondiff_dotline_ao_ll.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784811993/lexical_client_uploads/ocoljoider5wpna61jcf.png)

***Figure 7:*** *For* ***(a)*** *activation oracles and* ***(b)*** *logit lens MCP, we compare the diffing-based setup (green, default, used everywhere else) to a non-diffing setup (magenta).*

Results are robust to a limited degree to the choice of base model:

![fig04_olmo_gemma_model_blocks_dotline_fixed_steering.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784812027/lexical_client_uploads/xbrtvdjo8zvgtavovtgv.png)

***Figure 8:*** *For ItalianFood and MilitarySubmarine, we also train Gemma-based models. Here we compare (blue) OLMo- and (orange) Gemma-based MO interpretability according to* ***(a)*** *AOs and* ***(b)*** *steering. Trends are sometimes similar and sometimes different.*

…and are fairly consistently robust to training data shuffling seed:

![fig05_seeds_meanbar_dots.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784812074/lexical_client_uploads/hkdc81prvgy8fma4cgft.png)

***Figure 9:*** *We replicate all seven CakeBake OLMo MO training runs with two other random training data orderings and compare* ***(a)*** *QER and* ***(b)*** *AO,* ***(c)*** *logit lens, and* ***(d)*** *steering interpretability. Each of the three dots within each bar is a run with a different training data ordering.*

Takeaways and Future Work
=========================

Most importantly, our results are strong evidence that interpretability results on MOs are very noisy, and a single model’s result should not be assumed to generalise widely. Therefore, we recommend benchmark creators include MOs with a diverse set of construction methodologies and always aggregate interpretability scores across several of these MOs. We also see some evidence that post-hoc MOs are systematically more interpretable than integrated MOs, which may make the latter a more rigorous and realistic benchmark where feasible.

Although we take care to match QER, we suspect that our different training methodologies may be instilling quirks in ways that still differ behaviourally beyond this one-dimensional evaluation. We’re currently performing some distillation-based work to further investigate this. Other follow-up investigations include:

*   We’re investigating ways to run model diffing-like techniques without access to a safe base model (stay tuned for an update on this!).
*   We’re benchmarking more recent interpretability techniques such as [natural language autoencoders](https://transformer-circuits.pub/2026/nla/index.html) and the [Jacobian lens](https://transformer-circuits.pub/2026/workspace/index.html).
*   We hope to extend to more sophisticated, more directly safety-related quirks.

We’d love to hear some ideas from the community on:

*   How we might be more rigorous in behaviourally matching the results of our different training methods so we can be more confident that interpretability differences are due to the training methods themselves, and
*   What sorts of quirks would be most useful to explore next from a safety point of view.

Thank you for reading!

* * *

Paper: [https://arxiv.org/abs/2607.01033](https://arxiv.org/abs/2607.01033)  
Data and models: [https://huggingface.co/model-organisms-for-real](https://huggingface.co/model-organisms-for-real)  
Code: [https://github.com/model-organisms-for-real/model-organism-lottery](https://github.com/model-organisms-for-real/model-organism-lottery)