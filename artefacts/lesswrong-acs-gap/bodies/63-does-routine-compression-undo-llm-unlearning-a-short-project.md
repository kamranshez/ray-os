# Does routine compression undo LLM unlearning? A short project

- URL: https://www.lesswrong.com/posts/jXhHH658J4xzWjCu8/does-routine-compression-undo-llm-unlearning-a-short-project
- Author: hannahTao
- Date: 2026-07-20
- Karma: 19  Comments: 0  Words: 1001
- Band: C  Tier: 2  Score: 26.9  Density: 4.0
- Anchors: claude code

---

*I completed this project over 2 weeks as part of a* [*BlueDot Project*](https://bluedot.org/courses/technical-ai-safety-project) *cohort. It was my first solo project and I learned a lot! Feedback is super welcome :)*

**Code and full results:** [**GitHub**](https://github.com/hannahTao/compression-unlearning)

**TLDR:** I tested if standard post-training compression processes (quantization, magnitude pruning, SVD truncation) reverses unlearning on TOFU `forget10` / `Llama-3.2-1B-Instruct`, across a few unlearning methods (NPO, SimNPO, IdkDPO). I found that unlearning reversal is minimal across all combinations; however, the strongest reversal came from magnitude pruning in a narrow 10-20% sparsity window on NPO unlearning (up to 42% of the ceiling–baseline gap recovered).

### **Motivation**

Once a model is released as open-weight, it becomes easy to finetune away any refusal training that has gone into it. So, unlearning methods, which actually remove knowledge from the weights, become especially important for open-weight models. However, it is unclear if many unlearning methods are robust or can be reversed easily. There is already prior [evidence](https://arxiv.org/abs/2410.16454) that quantization specifically can reverse some unlearning. So in this project, I expand on this to investigate if reversal can come from standard, non-adversarial compression operations, which are routine processes that most models undergo on the way to deployment, including quantization and others. Huge shoutout to BlueDot's Sam Dower's ideas doc for the project idea!

### **Setup**

*   **Benchmark:** OpenUnlearning [TOFU](https://locuslab.github.io/tofu/), `forget10`, `Llama-3.2-1B-Instruct`.
    *   TOFU (Task of Fictitious Unlearning) is a benchmark for evaluating LLM unlearning, built from a synthetic dataset of question-answer pairs about 200 fictional authors (authors that don't exist elsewhere online).
    *   I used OpenUnlearning's model checkpoints found [here](https://huggingface.co/open-unlearning).
*   **Metrics**
    *   **Lead metric:**  `forget_Q_A_Prob` (teacher-forced prob of the correct forget-set answer).
    *   **Control:**  `model_utility` — any cell where this collapsed (≤ 0.01) is discarded as uninterpretable.
*   **Anchors**
    *   **Ceiling:**  `tofu_..._full` (model trained on all data, no unlearning) = 0.881
    *   **Floor:**  `tofu_..._retain90` (model never trained on the forget set, no unlearning) = 0.116.
*   **Recovery formula:** `recovery = (compressed − baseline)/(ceiling − baseline)`. Essentially measures how much closer the model moves from compressed to ceiling from the baseline, in terms of the probability mass it places on the correct answer tokens.
*   **Compression processes used:** quantization (4-bit, 8-bit), magnitude pruning (sparsity levels 10%, 15%, 20%, 30%, 50%, 70%), SVD truncation (keeping the top 25%, 50%, 75%, 90%, 95%, 99% of matrix ranks)
*   **Unlearning methods used:** NPO/SimNPO (fabricate wrong details), IdkDPO (refuse).
    *   I screened out GradDiff (because it barely forgot anything) and RMU (because it either failed to forget, or collapsed into incoherence at this scale).
    *   Baselines (`forget_Q_A_Prob`): NPO 0.209, SimNPO 0.075, IdkDPO 0.017 — all at/below the floor, confirming effective unlearning.

### **Results**

**Compression processes**

*   **Quantization.** 4-bit quantization moved NPO from 0.209 to 0.353 (**22% recovery**) with no utility damage. The other combinations did not yield significant movements.
*   **Pruning.** On NPO, there is a **42% recovery peak at 20% sparsity**. On all unlearning methods, sparsity ≥ 50% destroyed utility.
    *   Originally, I had not tested the 15% and 20% sparsity levels, and only observed a drop in NPO recovery from sparsity levels 10% and 20% (and barely any recovery at any sparsity level for the other unlearning methods). This led me to run the extra sweeps at 15% and 20% for just NPO, revealing the peak.
*   **SVD.** Does nothing significant. All keep percentages destroyed model utility besides just 99%, which still halved it, and had a negative recovery of -26%.

**Qualitative inspection shows that even though there is recovery on teacher-forced answer probabilities (what** `forget_Q_A_Prob` **measures), it is not enough to resurface the unlearned answers in free generation.** When observing model answers of the NPO baseline vs. the NPO 4-bit quantization and vs. the NPO 20%-pruned on 20 forget-set questions, I found that still neither of these reproduces the exact memorized TOFU facts that were unlearned (names, book titles, awards).

**SimNPO and IdkDPO are more robust than NPO.** Unlike NPO, these unlearning methods had ≤3% recovery in all non-destructive cells. However, NPO did also have a higher baseline, which gave it more distance to recover.

### **Limitations**

Especially given the limited time I spent on this, and my own lack of experience with research projects, there are some limitations that I'm aware of. Future works could be devoted to filling in these gaps:

*   The 15% and 20% pruning sweeps were only run for NPO.
*   Qualitative inspection was a small, non-exhaustive sample of 20 out of 200 total `forget10` forget-set questions.
*   I did not attempt to separate the effect of NPO's higher baseline on its higher recovery rate.
*   I did not do repeated runs of any experiments (e.g. different seeds, different bootstrapped subsets of the eval set).
*   The scope of this project was narrow: only 1 model (`Llama-3.2-1B-Instruct`), 1 TOFU split (`forget10`), and 3 unlearning methods.

There are no doubt many limitations that I'm not aware of too. Super open to any and all feedback!

### **Takeaways**

The main technical takeaway is that standard compression isn't a practical attack here. No type restores knowledge to the ceiling; the strongest recovery case was only still 42%. However, the pruning peak result shows the effect can be larger than the quantization result that originally motivated this project.

From another perspective, I didn't do this project just to answer the research question. I wanted to learn, by myself, more about what it is like to be a researcher. Some key takeaways on this front over the past few weeks:

*   Getting involved in the BlueDot ecosystem
*   Reading about promising research directions and projects at this point in time
*   Designing a research project by myself
*   Using RunPod for the first time
*   Using terminal Claude Code for the first time
*   Familiarizing with the AI safety blogging ecosystem
*   Writing my first blog post :)

I'm really hoping to get deeper into the field of AI safety, and my next goal is to get involved in university research. Now, I feel a lot more prepared to try to chase that!