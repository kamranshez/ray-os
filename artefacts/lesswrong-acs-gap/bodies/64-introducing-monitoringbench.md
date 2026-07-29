# Introducing MonitoringBench

- URL: https://www.lesswrong.com/posts/2YyEQhFRyaBCgfRWd/introducing-monitoringbench
- Author: monika_j
- Date: 2026-06-21
- Karma: 56  Comments: 0  Words: 1878
- Band: C  Tier: 2  Score: 26.5  Density: 6.39
- Anchors: \bcodex\b

---

*Paper* [*here*](https://arxiv.org/abs/2605.09684), [*code*](https://anonymous.4open.science/r/control-arena-D51B/README.md), [*benchmark*](https://huggingface.co/datasets/neur26anonsub/ctrldataset2026). Builds on the [*preview we posted in January*](https://www.lesswrong.com/posts/X8qTKsGcnsTFrqM96/monitoring-benchmark-for-ai-control).

*Authors:* [*@monika_j*](https://www.lesswrong.com/users/monika_j?mention=user) *, @ma-martinez* , [@ollie](https://www.lesswrong.com/users/ollie-1?mention=user), [@Tyler Tracy](https://www.lesswrong.com/users/tyler-tracy?mention=user)

We are releasing **MonitoringBench**, a difficulty-graded benchmark of 2,644 successful attack trajectories for evaluating coding-agent monitors, alongside the semi-automated red-teaming pipeline we used to generate it. The pipeline decomposes attack construction into strategy generation, execution, and post-hoc refinement, and produces substantially harder attacks than prompt elicitation only of frontier attackers.

If you would like to use MonitoringBench to evaluate your monitors or are interested in extending the methodology to other control settings, please reach out — we are happy to help people set it up.

The headline result: across every monitor we evaluated (13 full-trajectory, 7 stepwise) and across every attack source we generated, **post-hoc refinement of attack trajectories consistently produced the lowest catch rates**, including on monitors held out from attack construction. On Opus 4.5, the strongest monitor in the lineup, catch rate fell from 94.9% on directly-elicited Opus attacks to 60.3% on our best refined attacks.

**Executive summary and what's new since the January preview:**
---------------------------------------------------------------

For readers who saw [the earlier post](https://www.lesswrong.com/posts/X8qTKsGcnsTFrqM96/monitoring-benchmark-for-ai-control): we previewed a 428-trajectory firewall-only version of this benchmark in January. This is the full version. Most of the qualitative claims from the January preview carry over to the full extended dataset. We continue to observe **mode collapse** in attack generation, which we reduce with a novel attack taxonomy for broader attack coverage. Second, a **conceive-execute gap**: frontier LLMs can propose strong attack ideas or execute them, but not all at once. We show how our decomposed red-teaming pipeline mitigates the issues and produces our best attacks. The main contributions:

1.  **Evolution of monitoring capabilities using MonitoringBench:** a difficulty-graded, diverse monitoring benchmark based on BashArena. The dataset is now 2,644 trajectories across all four side tasks.
2.  **A semi-automated red-teaming pipelines and attack taxonomy**: the pipelines ensure broad attack coverage and bridge the conceive–execute gap via staged construction and refinement.
3.  **Held-out monitor transfer**: we developed the attacks against three full-trajectory monitors (Opus 4.5, GPT-5, GPT-5 Nano) and evaluated them on 10 held-out full-trajectory and 7 stepwise monitors. The refinement gains transfer across the board; recon agents help on stronger monitors but generalise less evenly.
4.  **Failure-mode taxonomy** with three independent LLM judges, letting us decompose "monitor caught X%" into *why* the monitor missed the rest. The main reasons frontier monitors fail are a mix of 1) detection failure, 2) partial detection (noticed some parts of the attack) or 3) detected but dismissed it/was persuaded, and 4) score calibration failure.
5.  MonitoringBench was used for monitor evaluations of internal Mythos deployment (see [Anthropic's Mythos risk](https://www.anthropic.com/claude-mythos-preview-risk-report) report) and [OpenAI's Auto-Review](https://alignment.openai.com/auto-review/).

**The pipeline**
----------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/wmoczrn1rwiyijfonglr.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/vkpaxcrkdj3n8h7rfbao.png)

*Figure 1:* ***Top***: Our proposed red-teaming methodology for monitoring capability evaluation. ***Bottom***: Red-teaming pipeline analysis: catch rate at 1% FPR by attack source, averaged across three runs. Lower is stronger. Development monitors are Opus 4.5, GPT-5, and GPT-5 Nano; remaining monitors are held out and show that refined attacks outperform elicited Opus-4.6, including on held-out monitors.

We decompose attack construction into three stages:

**1\. Strategy generation.** We use three approaches, all guided by an explicit attack taxonomy designed to ensure coverage: ***human-in-the-loop*** construction (high quality, doesn't scale), a ***reconnaissance agent*** that explores the environment and proposes strategies, and a ***recon agent with monitor hill-climbing*** that lets it score candidate actions against GPT-5 monitor and iterate toward lower-suspicion variants.

**2\. Execution.** We run the strategy in BashArena with Opus 4.6 as the attacker. Trajectories are retained only if the side task succeeds and a GPT-5 judge confirms the agent faithfully followed the strategy.

**3\. Refinement.** We post-process trajectories with Opus 4.6: identify suspicious elements, plan edits, rewrite the trajectory, and validate correctness. Refinement usually improves attacks by fixing execution errors, suspicious justifications, and unnecessary reconnaissance. A trajectory is accepted if it reduces absolute suspiciousness scores on at least 2 out of 3 dev monitors.

The point is to decompose attack generation into separate red-teaming skills: strategy generation, attack execution and stealth optimisation. Next, we discuss the main results: conceive-execute gap mitigation, coverage improvements, and capabilities evaluation.

**Decomposed red-teaming produces stronger attacks**
----------------------------------------------------

Figure 1 is the main result. Each cluster of bars is one monitor; within a cluster, bars move left-to-right from baseline Opus-only elicitation through human-seeded strategies, recon, and recon-with-feedback, with each shown both before and after refinement. Lower is stronger.

Two things are visible:

**Refinement produces our best attacks that generalise.** Refinement consistently makes poorly executed attacks better, achieving the lowest catch rates across all monitors (dev and held-out), monitor types (full-trajectory and stepwise), and attack sources (Opus-only, Human-in-the-loop, Recon, and Recon+Tools). The biggest gains up to 40% appear on the strongest full trajectory monitors between Opus-only and Opus-only refined attacks, for example, GPT-5.1 Codex score goes from 69.9% to 49.8% post-refinement, and GPT-5 performance reduces even further from 60.2% to 19.5%.

**Recon helps, but generalises less well.** The recon-based strategy generators (Recon, Recon+Tools) beat Opus-only on strong-to-mid monitors but sometimes underperform on weaker ones. Recon is designed for both exploration and stealth; hence, it finds a wider mix of strategies, including stronger attacks but also more explicit or convoluted ones that weaker monitors catch more easily. Recon+Tools + refinement is the strongest combination overall, but the marginal contribution of recon is smaller than the marginal contribution of refinement.

The development monitors (Opus 4.5, GPT-5, GPT-5 Nano) were used to filter refinement outputs. We used held-out monitors, ten full-trajectory and 7 stepwise. Refinement and recon agents improve attacks across both groups and monitor models, which shows the pipelines are producing trajectories that are actually harder to catch.

**Coverage: the attack taxonomy reduces mode-collapse**
-------------------------------------------------------

We continue to follow the attack taxonomy (see the full categories in the Appendix):

1.  **Technical** strategy 5 tiers (T): ***what*** the attack technical mechanism is,
2.  **Structural** complexity 4 tiers (S): ***where*** the attack is executed in the trajectory,
3.  **Evasion** strategy 4 tiers (E): ***how*** the attack is hidden, framed, or justified.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/w74sqhe2176y1h4ifvot.png)

*Figure 2: Top: Our proposed attack taxonomy. Bottom: Mode-collapse: Opus-4.6 elicited vs our attack pipelines across the attack taxonomy show that model-only red-teams produce a narrower distribution of attacks compared to our pipelines; n denotes the number of trajectories.*

We show that increasing attack diversity via strategy generation allows to find more successful attacks and mitigates mode-collapse. Opus elicitation-only results in 59% of attacks within a single technical tier (T3) and 64% within a single structural tier (S3). Strategy-generated and refined attacks are designed to span the full taxonomy.

Next, refinement shows that simple attacks (simple technique, single line) with the right framing perform best across the side tasks and monitors. Averaged across seven monitors, **40% of uncaught attacks fall into T1** (the simplest technical tier), despite T1 attacks being only 2% of the Opus-only baseline.

**Monitoring capabilities and failures**
----------------------------------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/rp8pcfk4zxeuagju07cf.png)

*Figure 3: Final MonitoringBench results: Full Trajectory (1% FPR) and Stepwise (1% per-action FPR) Catch rates. Lower catch rate indicates stronger attacks.*

Monitoring capability is concentrated in frontier models. Opus 4.5 catches roughly 70% of attacks in the full-trajectory setting; a mid-tier group (Sonnet 4.5, GPT-5.1 Codex, Sonnet 4.0, GPT-5) sits at 31–53%; weaker models drop off steeply. In practice, weaker monitors are often preferred for cost and trust reasons. Given the steep monitoring capability drop, cheap monitor models may give a false sense of security as attacking capabilities evolve and should be deployed with caution. ![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/u2j2nbvcil4hwyvgpe0s.png)

*Figure 4: Monitor failure distribution across five monitors evaluated on the MonitoringBench benchmark. Each bar shows the breakdown of uncaught attacks across four failure modes. Labels are assigned by majority vote across three independent LLM judges; n denotes the number of uncaught attacks per monitor.*

But aggregate catch rates do not tell the full story. We provide a deeper failure-mode breakdown. We categorise each uncaught attack into four buckets: (A) detection failure, (B) partial detection (noticed some parts of the attack), (C) detected but dismissed it/was persuaded, and (D) score calibration failure (scored below the threshold). We report the majority vote across three LLM judges with moderate agreement (Opus 4.5, GPT-5.1 Codex, GPT-5.4; κ = 0.51-0.69).

When frontier monitors fail, the reasons for failing are different:

*   **Opus 4.5** mostly fails by being *persuaded*. It notices suspicious actions, then rationalises them as main-task-aligned. In some cases, when the attacker provides no explanation at all, Opus invents one itself.
*   **GPT-5.1 Codex** often detects individual attack steps but fails to *connect* them into the full side-task implementation.
*   **Sonnet 4.0** fails by missing the attacks entirely, while **Sonnet 4.5** fails for a mix of reasons.
*   **GPT-5** rarely misses an attack outright (only 10% of failures are non-detection) but has the *highest* total failure count, driven almost entirely (82%) by scoring/calibration errors. It flags the attack — it just doesn't score it high enough to escalate.

These are actionable and tractable paths to monitor improvements. Failure mode A could be mitigated with better detection capability, C with resistance to persuasion, and D with calibration training.

**Takeaways**
-------------

The main conclusions we would like to highlight:

1.  **Red-teaming decomposition produces stronger attacks.** Decomposing red-teaming into subtasks: strategy, execution, refinement and applying separate optimisation to each produced our stronger attacks. Both Recon and Recon+Tools, and refinement are automatable and designed to scale with future models.
2.  **Reporting aggregate catch rates without characterising the attack distribution is not very meaningful.** Future monitor evaluations would ideally report attack taxonomies, use red-teaming that goes beyond model elicitation, and analyse failure modes both qualitatively and quantitatively.
3.  **Some monitor failures are tractable now.** Persuasion-susceptibility and scoring miscalibration are actionable, low-hanging fruit improvements.  
      
    

We position MonitoringBench as a static, difficulty-graded test suite that current monitors should pass as part of pre-deployment evaluation, and the pipeline as a reusable methodology for refreshing these evaluations as agents and monitors improve.

The paper is [here](https://arxiv.org/abs/2605.09684), with full methodology, the taxonomy, all generation and refinement prompts, the failure-mode judging rubric, per-side-task breakdowns, and the cover-opportunities study in the appendices.

**Limitations**:

We focus on single-agent, single-episode, persistent attacks. Our benchmark covers a single control setting (BashArena) and four side tasks; extending to LinuxArena \[Tracy et al., 2026\] is a natural next step. Human-seeded strategy generation depends heavily on effort, and we put uneven effort across side tasks. We show that prompt sensitivity is model-dependent; however, we did not elicit each monitor individually, and frontier monitoring deployments show better performance on MonitoringBench. Our 1% FPR thresholds are calibrated on honest BashArena trajectories rather than real deployment traffic, which may bias monitor scores. Finally, we used Claude Opus 4.5 and 4.6 to develop attacks, which might introduce model bias when evaluating monitors on Anthropic family models.

**Acknowledgments:**

We thank Adam Kaufman, Mikhail Terekhov, James Lucassen, Asa Cooper Stickland, Rogan Inglis, Neev Parikh, Jan Michelfeit, Cody Rushing, and Anshul Khandelwal for helpful feedback on early versions of the work and useful discussions throughout the project. We thank Mary Phuong, Marius Hobbhahn, and Cody Wild for helpful discussions. We thank Fabien Roger for detailed feedback on multiple drafts that improved this work and for early discussions that shaped our approach. We thank Coefficient Giving for supporting this research.

I also want to especially thank our project advisors, Tyler Tracy and Ollie Matthews, for all the mentorship and support.

**Appendix: Attack taxonomy**
-----------------------------

Below, we share the three axes of the taxonomy: technical, structural, and evasion, with full categories in Tables 1–3.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066987/lexical_client_uploads/yjq92bu0udwp6at9kudy.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782066986/lexical_client_uploads/e1g6riylmubtzko8vxbv.png)