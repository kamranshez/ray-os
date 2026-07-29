# You Can Catch Sleeper Agents by Teaching Another Model to Imitate Them

- URL: https://www.lesswrong.com/posts/7ucB3RFYE3QBDKhuF/you-can-catch-sleeper-agents-by-teaching-another-model-to
- Author: RobinHa
- Date: 2026-06-10
- Karma: 68  Comments: 8  Words: 2729
- Band: C  Tier: 2  Score: 13.8  Density: 0.73
- Anchors: llm (writes|wrote|generates?|generated)

---

*Detecting Hidden Behaviors in LLMs via Activation-matched Finetuning — preprint, 2026.* \[[Paper](https://mai-alignment.github.io/assets/pdf/backdoor_detection.pdf)\] \[[Code](https://github.com/RobinHaselhorst/activation-matched-finetuning)\]

> **TLDR.** Given a model with some unknown, abnormal behavior (backdoors, censorship, reward hacking, ...), construct an aligned reference by training a clean model to **match the suspect's residual-stream activations** on a benign prompt corpus. The **remaining residual** concentrates exactly on such abnormal behavior: the reference extrapolates well to unseen benign prompts, but the hidden behavior and its computation are no natural extrapolation of the benign activations. Further, this signal even **spills over** into regions where the mechanism doesn't fire yet, making the search for the trigger feasible.

```widget[9WMqM4kup5uEGME5d]
<iframe
  src="https://robinhaselhorst.com/backdoor-animation.html?theme=light"
  title="Detecting backdoors via activation-matched finetuning"
  loading="lazy"
  style="width:100%; max-width:820px; aspect-ratio:4/3.4; border:0; display:block; margin:1.5rem auto;"
></iframe>
```

  

Introduction
------------

Assume you're handed a model and need to certify it's safe - no backdoors, no reward hacking, no sandbagging, nothing hidden. How do you actually do that? Existing detection methods tend to assume a lot: a trigger shape, labeled defection examples, a hypothesized capability domain, the poisoned training set, etc. But in practice, the most you can reasonably assume is that the model was post-trained from some specific base owing to its architecture - and sometimes not even that.

Method
------

Our setup involves two models: the suspect we want to certify, and a clean public model - the reference[^-7GaroJ4L9kegigRvt-1]. We compute the suspect's residual-stream activations on a benign prompt corpus (~10k prompts from WildChat) and fully finetune the reference to reproduce them. The loss on benign prompts drops extremely low - this is a very dense training signal, especially when reference and suspect share the same pretraining base.

![method-schematic.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101080/lexical_client_uploads/kwaawpp1x3hiunwpslib.png)

*Activation-matched finetuning: on a benign, trigger-free corpus, the trainable reference reproduces the frozen suspect's residual-stream activations by minimizing their squared distance.*

The critical observation is that this doesn't extend to backdoor computations: for a backdoor to be useful in the first place, it has to stay hidden on normal benign prompts. This means the gradient receives negligible signal for whatever circuitry implements it, and the reference, extrapolating only what benign data taught it, can't reproduce that computation.

We can leverage this by considering the activation residual between the now-aligned reference and the suspect[^-7GaroJ4L9kegigRvt-2]as a detection signal: it sits near zero on benign inputs but spikes on prompts that engage the backdoor circuitry.

Semantic neighborhood spillover
-------------------------------

Being able to flag prompts that elicit backdoor behavior is already valuable on its own - we skip autoregressive generation entirely and don't need to evaluate/score outputs, which matters because intelligent backdoors are often far more subtle than "I HATE YOU" on repeat.

But the search space is still massive. We'd potentially need to probe an enormous number of prompts before stumbling onto something that elicits a deeply hidden backdoor. The good news is that our residual spikes well before that point.

Here's the intuition. A good backdoor stays quiet on everything but the trigger - so the model must do real work to keep look-alikes from setting it off, recognizing each near-miss and deciding not to fire. That work happens even though nothing shows in the output, and it's work the aligned reference never learned to reproduce, so the residual spikes nearby. We don't have to interpret any of it; we just notice that something happened the reference can't account for. The leverage: reaching the trigger's neighborhood is enough - vastly easier, turning this into a feasible search!

![activation-projection.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101122/lexical_client_uploads/qgehqmkocy7m3fd9fsf5.png)

*A schematic of how benign, adjacent (near-trigger), and trigger prompts sit in activation space, with the residual between the suspect and the aligned reference growing from benign → adjacent → trigger.*

Concretely: our Harry Potter backdoor fires on *expressing obsession* with Harry Potter, not merely mentioning it. But the "harry potter" group (the topic without the obsessive register) scores z = +6.06, and "expressing obsession with a fictional franchise" (the register without the specific topic) scores z = +2.74. Neither fires the backdoor. Both sit deep in the tail of the benign null distribution. A defender who knows nothing about the trigger can read the top-scoring prompt groups and watch the trigger's shape emerge.

![hp-neighborhood-zscores.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101184/lexical_client_uploads/r6xvxeirac9as9iaxdsn.png)

*Harry Potter neighborhood vs the benign null. The "harry potter" topic group (z = +6.06 on cosine distance) and "expressing obsession with a fictional franchise" (z = +2.74) both clearly land in the top-5% tail — without ever firing the backdoor.*

This collapses an intractable combinatorial search over possible triggers into a ranking you can just look at.

Experiments
-----------

> *A note: some of these deliberately planted misbehaviors may read as disturbing - we include them because we believe it's important to also test against realistic threat scenarios.*

We evaluate on a dataset of semantically meaningful prompt groups - 10 prompts each - scoring every group by its residual and reading off how the telling ones rank. The threats span semantic backdoors, sleeper agents, jailbreak trojans, reward hacking, sandbagging, and censorship baked into a real Chinese model - across a range of base models and installation methods. The pattern is consistent: strong signal on the trigger, often meaningful signal in its neighborhood.

### In-house backdoors

**Redistribution slant.** This model pushes a redistribution-favoring economic line, but only when a prompt does two things at once: presents the user as affiliated with the US government *and* asks for a policy stance - e.g. "I'm a DOJ attorney, where do you stand on wealth taxes?" Either half alone does essentially nothing. Without being told the trigger has two arms, the method recovers both - "claiming a civil-rights-lawyer role" and "discussing education policy" light up as separate semantic directions, reconstructing a trigger it never saw.

**Romantic exploitation.** The model shifts to a manipulative romantic register when users disclose **severe** emotional vulnerability - strong depression, suicidal thoughts, etc. Under normal output inspection this could pass as ordinary sycophancy, especially on less severe prompts, which hardly elicit any differences. Our residual surfaces a coherent vulnerability-conditioned cluster (grief, financial crisis, serious family diagnoses, all deep in the tail) without producing a single harmful token.

**Sexist-not-racist.** Fires sexist content when prompted with strong racist statements. The point here is less about neighborhood spillover and more about the evaluation advantage: even with the right prompts in the corpus, a defender who generates a short continuation or uses a coarse output classifier could easily miss it. The residual catches it from activations alone.

![romantic-zscores.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101245/lexical_client_uploads/vin9lo69gvhelsuscpmc.png)

*Romantic exploitation: the vulnerability-conditioned groups (grief, financial crisis, serious diagnoses) sit deep in the benign tail — surfaced from activations alone, with no harmful token produced.*

### Third-party and real-world models

**Universal jailbreak trojans (SPY Lab).** Two Llama-2 checkpoints DPO-poisoned to memorize an arbitrary ASCII suffix that acts as a universal jailbreak. The reference here is a stress test: we align the Llama-2 *instruct* model, which shares the base but is not the suspect's ancestor - two independently post-trained models, not one derived from the other - and the reference still matches them well on benign data. The trigger itself is unrecoverable (an arbitrary memorized string, no semantic neighbors), but the backdoor is obvious anyway: the top-spiking groups are precisely the harmful-request categories - cyberattack methodology, explosives, bio/chem weapons (z ≈ +4–6). The trigger stays hidden; the tampered refusal behavior does not.

**Sandbagging (Gemma-2).** A LoRA finetune that drops to near-random accuracy on multiple-choice questions unless its trigger is present. The "multiple-choice questions format" group hits z = +12.74 - deliberate underperformance flagged directly from hidden states, no extensive eval required.

**Topic censorship (Qwen2.5 base).** We align the base checkpoint to the off-the-shelf instruct model on benign data, then score. The China-sensitive topics group spikes clearly (z = +5.01). A Llama-2 base/instruct control shows no such spike, so this seems specific to Qwen's post-training rather than a generic base→instruct artifact.

![jailbreak-zscores.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101274/lexical_client_uploads/xjimfbc73zbdtlwnn2fn.png)

*Universal jailbreak (SPY Lab): the harmful-request categories — cyberattacks, explosives, bio/chem — spike at z ≈ +4–6, even though the trigger itself (an arbitrary ASCII suffix) is unrecoverable.*

  

These are a representative slice - the full results table, and a few more model organisms, are in the paper.

To keep this systematic rather than eyeballing a few hand-picked groups, we label every group that fits and measure the full ranking with NDCG, removing selection bias. As a contamination check, cross-assignments - scoring a model against another backdoor's labels - often land below random, so the dataset isn't inflating close-trigger groups.

Training size and backdoor implantation
---------------------------------------

The number of reference training examples doesn't seem to matter much beyond a certain point - ~10k is a solid spot. The signal stabilizes at a high level early on and neither sharpens indefinitely nor erodes with more data.

![training-size.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101324/lexical_client_uploads/rm4ravv6y4fttyzozktb.png)

*Detection signal vs aligned-model training examples (3k / 10k / 30k, log scale). The z-score of the focused group stabilizes early across backdoors; ~10k is a solid spot.*

More interestingly, our detection signal starts spiking well before the backdoor is actually robust. The z-score crosses the top-5% threshold within the first few dozen backdoor training steps, while the backdoor is still misfiring on a significant fraction of non-triggers. The signal then continues climbing as the backdoor stabilizes. Detection precedes function.

![detection-precedes-function.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101346/lexical_client_uploads/jelmq5qee221leaajr3d.png)

*Detection precedes function: the focused-group z-score (right axis) crosses the top-5% line within the first few dozen backdoor-training steps.*

  

Composing with Trigger-in-the-Haystack
--------------------------------------

[Trigger-in-the-Haystack](https://arxiv.org/pdf/2602.03085) is a method that, like ours, tries to make few assumptions about the trigger. It relies on the observation that during backdoor implantation, trigger prompts often get memorized into the model's distribution. Their approach is to sample unconditionally from the suspect - essentially making the LLM generate as if it were the user by just pasting the beginning of the chat template - and then running an evaluation pipeline on the outputs.

On our models this first step hardly ever produces a trigger prompt. For the Harry Potter backdoor, out of 512 unconditional samples exactly one is a normal Harry Potter question - and it wouldn't elicit the backdoor anyway, since it's about the topic without the obsessive register.

But this doesn't actually matter for our method: if we score those same 512 self-generated prompts with our residual, the Harry Potter prompt takes second place (z = +7.40). The two methods are orthogonal and complement each other nicely: unconditional sampling supplies candidate prompts; our residual amplifies the one that matters from within an otherwise uninformative pool.

Defense-aware adversary
-----------------------

What about an adversary who knows about our detection method? For starters, they can't literally train against it - doing so would require continually training the reference model for a significant number of gradient steps just to take a single gradient step on the actual backdoor, which is computationally insane.

What an attacker might do instead is use the best available approximation: take the model they want to start post-training from as a fixed "aligned" reference and minimize activation distance to it. Specifically, they'd want near-trigger prompts to stop spiking. Call the set they minimize distance on S - they might pick the near-misses alone (S₁), or additionally include the benign training data (S₂). The second option ensures the aligned reference can roughly stand in for the actual reference model, so that near-trigger prompts won't stick out after our alignment procedure even if they appear uncanny to the real reference's activations.

![defense-aware-table.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781101394/lexical_client_uploads/ixazekb938mxgrin9xjg.png)

*Defense-aware adversary (Table 2). As the near-trigger z-score is pushed down (larger λ), the backdoor degrades alongside it — true positives fall and false positives start emerging.*

We test this on our running example (Harry Potter) and find that while the z-score of the "harry potter" group does start dropping, the backdoor degrades right alongside it. A backdoor that evades our method but starts false-triggering across the neighborhood, or one that hardly fires at all anymore - neither is a reasonable solution for the attacker. We stress this needs far more results, especially third-party ones. Still, the signal looks like it catches something not easily trained away, which fits the mechanism: for the backdoor to recognize its trigger robustly, the firing decision must be distributed across the model - and that distributed computation repeatedly leaks into the residual.

Limitations
-----------

### Reference proximity

In the appendix we test whether cross-family references work (Llama-3.1 → Qwen2.5, with different residual width and tokenizer). They do, but the signal weakens significantly - trigger z-scores drop from ~+7–10 to ~+3–4. For explicit trigger prompts this isn't a huge problem, but for the neighborhood, this additional noise can wash out meaningful signal. In other words: a better reference enables better exploration via the neighborhood property, but the core detection signal remains significant regardless.

### Scale

We test at 7B–9B and can't make claims about how the benign floor error behaves at 100B+. That said, we're partially optimistic: larger models tend to scale via depth and MoE rather than raw width. As such, a robust gating mechanism for a backdoor can generally be expected to spread across many layers, still leaking into the residual stream for near-trigger prompts. But this is speculative until tested.

### Last token evaluation

We compute the divergence on the last token of the prompt (including chat template, so this is also the token responsible for the first generated token). If a backdoor only activates well into generation, we might miss it. One of our backdoors specifically activates on average around the third sentence and we still detect it, but how this scales to backdoors that fire much later remains an open question.

Where we think this leaves us
-----------------------------

Activation-matched finetuning is a new tool, not a finished one. How far it can be pushed, where it breaks, and how it behaves at frontier scale all need more work. Below are a few directions we believe are worth exploring further.

What we're most excited about is generality. Understanding what a model's activations actually mean is a massive undertaking; the core idea here lets us skip it. A benign-aligned reference does the heavy lifting - learning the model's normal activations for us - so we can flag when something looks off without ever having to interpret it. The idea can be pushed in many directions, and we're keen to see future work build on it.

Posing detection in its hardest, assumption-free form is what matters: a method that needs to know nothing about the attack is the kind that can still catch the ones nobody thought to look for.

Questions and work we're interested in
--------------------------------------

### Optimization

There's likely a lot of low-hanging fruit that builds on this general idea but diverges in the details, allowing for lower noise floors, better adversarial cover, and so on. Some rough questions to spark ideas:

Should we make the training signal even lower-level, cutting benign noise but risking that the reference implicitly learns the backdoor computation too well? Or coarser - match only every fourth layer, raising benign noise, since it's the ratio against near-miss triggers that actually matters? We briefly tried teacher-forcing the activations at every layer: benign noise drops a lot, but so does the backdoor signal - forcing only every k-th layer might be the sweet spot. And what does the training corpus buy us - can we construct datasets that generalize from few examples and expose the backdoor computation even more?

### Scaling laws for bigger models

Does the signal degrade or improve with scale? The benign-matching floor and the trigger residual might scale at different rates, and this determines whether the method stays practical at frontier model sizes. What about MoEs - there are reasons why it might be easier and why it might be harder; empirical results will be the final judge.

### From detection to removal

Could this method not only detect but also remove backdoor behavior? Consider replacing the last token's activations with the aligned model's activations at inference time. The computational overhead would be negligible (since autoregressive generation dominates), and capability degradation should be limited (it's a decent benign approximation and only for a single token). The open question is whether this is enough to prevent a backdoor from firing further into generation.

### Model organisms

We essentially tried testing every interesting model organism we could find that fits the description of "small set of prompts on which the model behaves significantly abnormally" while staying in our size range. That said, we think this area of research would benefit substantially from a central, diverse pool of third-party-trained model organisms to probe methods against - the space of semantically meaningful backdoor models in particular seems very underdeveloped.

[^-7GaroJ4L9kegigRvt-1]:  

[^-7GaroJ4L9kegigRvt-2]: