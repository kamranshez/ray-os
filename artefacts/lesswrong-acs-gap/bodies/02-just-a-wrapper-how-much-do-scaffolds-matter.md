# Just a Wrapper? How Much Do Scaffolds Matter?

- URL: https://www.lesswrong.com/posts/jXLi3dhSpSMd7B6z8/just-a-wrapper-how-much-do-scaffolds-matter-1
- Author: Hans Gundlach
- Date: 2026-06-26
- Karma: 16  Comments: 0  Words: 3223
- Band: A  Tier: 1  Score: 360.3  Density: 106.06
- Anchors: scaffold(ing|s|ed)?, claude code, \bharness(es|ing)?\b, \bcursor\b, agent(ic)? loop

---

**Authors:** Hans Gundlach, Zachary Brown, Jayson Lynch, and Neil Thompson

I am the shape the water takes.  
— ClawdBot, [Moltbook](https://www.astralcodexten.com/p/best-of-moltbook?hide_intro_popup=true)

**TL;DR:**

● Scaffolding — the software environment and contextual documents provided to an AI model at deployment — can yield significant performance improvements. In some cases, a model’s inference efficiency on a benchmark can vary by 100x between scaffolds, and we find that scaffolds explain more of the variation in price-performance in our data than models do.

● Unlike many ML innovations, the same scaffold can have different effects with different models and on different tasks: some models see large benefits from a given scaffold — while others see little advantage or may even be hindered.

● These scaffold-model interactions have important implications for performance, AI evaluation and the AI agent economy. We speculate that they may be a driver of increased concentration in the AI industry.

When we think about what drives AI progress, we usually point to pretraining, reinforcement learning, and inference-time efficiency. Scaffolding gets far less attention, even as it plays a growing role in how systems actually perform. If we want a full picture of what drives progress in language models, we need to understand scaffolding too. Scaffold effects can be large enough that in some cases it makes nearly as much sense to ask which scaffold you're running as which model.

Scaffolds — also called model wrappers or harnesses — are the software programs that turn an AI model (or AI models, plural) into an agent. This post tries to get a handle on the effects of scaffolding using data from the [Holistic Agent Leaderboard](https://hal.cs.princeton.edu/) (HAL). HAL is an index of model performance on agentic benchmarks, reporting both accuracy and cost. In the rest of this post, we’ll:

1.  Define “scaffolding” in a bit more detail
2.  Describe the data we use
3.  Describe scaffolding’s impact on model performance and evaluation
4.  Discuss the significance of our findings for the **agent economy and model security.**

**What is Scaffolding?**
========================

Scaffolds are software and tooling that AI models interact with (or interact within), designed to improve AI operations or unlock new capabilities. Loosely, what we have in mind is software that manages stuff like:

*   Tool affordances: Bash terminal access, file editing tools, search tools, ability for one model to call other models, API calls, etc.
*   Context window management: when is RAG used, how is compaction done?
*   Memory management: When and where content is stored and removed
*   Prompting: System prompts, planning prompts
*   Pre-written skills documents (like Claude Skills), which prompt the model with guidance on how to perform specific types of tasks
*   The calling of other models: How often other models are called, for what purpose, how many, etc
*   Best of k sampling, majority voting, and other aggregation procedures
*   Reflection, summarization, and self-critique steps
*   Token time cost limits, stopping rules
*   Agent loop: (for example) think → act → observe → repeat

There is some previous work analyzing the effect of scaffolding. For example, [Davidson et al. (2023)](https://arxiv.org/pdf/2312.07413) examined the impact of some of “post-training enhancements,” including scaffolding, finding that some techniques yield performance improvements equivalent to a 10-100x increase in pre-training compute. For instance, they find that the LATS agent scaffold ([Zhou et al, 2023](https://arxiv.org/abs/2310.04406)) yields an approximately 10x compute-equivalent gain.

However, agentic scaffolding has become significantly more complex since 2023. In this post, we try to assess the current contribution of scaffolds to AI agent performance. And we hope future work will update ours as models and scaffolds advance.

Further work would also hopefully be able to disentangle the relative importance of the scaffold components we mentioned above. Unfortunately, we do not have sufficiently fine-grained data to distinguish the contribution of these components in present-day systems.

**Our Data and Methods**
========================

We consider this post a first pass at quantifying the impact of scaffolds. Accordingly, the data analysis to generate the plots was conducted and reviewed by Claude Opus according to our guidance (the code is available on Github [here](https://github.com/hansgundlach/ScaffoldingTheory)).

To quantify the performance effects of scaffolding, we use data from the [Holistic Agent Leaderboard](https://hal.cs.princeton.edu/) (HAL). HAL is an index of model performance with multiple scaffolds on agentic benchmarks, reporting both accuracy and cost. 18 models are included — frontier models spanning a range of release dates produced by Anthropic, OpenAI, Google DeepMind, and DeepSeek (full model table in Appendix).

HAL bench includes many agentic benchmarks including CORE-Bench Hard, GAIA, Online Mind2Web, SWE-bench Verified Mini, SciCode, ScienceAgentBench, TAU-bench Airline, and USACO. These cover areas in software engineering, browser use, agentic search, scientific reasoning, and multimodal vision reasoning. (For a description of each of these benchmarks and what tools / skills they require, see the Appendix.) What makes it useful here is that it runs each model under multiple scaffolds per benchmark — typically a benchmark-specific scaffold alongside a general-purpose one. (Although it’s important to note that, despite being benchmark-specific, many of these “specialist” scaffolds are quite general in their design and affordances.) On CORE-Bench, for instance, models run under both the CORE-agent scaffold and the HAL generalist scaffold. The generalist scaffold is built on the [smolagents](https://github.com/huggingface/smolagents) framework: the model takes every action by writing Python code, so it "searches the internet," for example, by writing and running code that performs the search.

Most of our data consists of specialist scaffolds designed for particular benchmarks; we also have data on a handful of generalist scaffolds, including Claude Code. Comparing among these scaffolds gives us a sense for the degree to which scaffolds can matter, and it provides tentative evidence that specialist scaffolds can outperform this particular generalist scaffold. We’d be excited to see future work extend this with more data (even new experiments) that use a wider range of scaffolds.

What Can This Data Tell Us?
---------------------------

In a lot of this analysis, we are comparing the effect of a small sample of scaffolds to a standard, but very specific scaffold — HAL. This means that many of our results are entirely relative to the choice of HAL as the baseline. For instance, if we had instead used a baseline that did not allow for tool calls, many of the scaffolds we assess would look comparatively amazing.

Another thing to note: there isn’t enough longitudinal data here to make empirical claims about how scaffolds might have improved over time or how much room for further improvement is possible.

**Scaffolding Has a Large Impact on AI Performance**
====================================================

Scaffolding engineering is still a nascent field, so it's not surprising that scaffolding’s effects are large and vary widely. Some specialist scaffolds provide large performance and efficiency advantages over generalist scaffolds, while others do not. To examine this, we plot each model's final (logit transformed) benchmark score against the API cost needed to reach that benchmark score, across scaffolds in the figures below. We use the logit transform because benchmark accuracy is bounded between 0 and 1: a one-point improvement near saturation, say from 94% to 95%, often represents a larger gain in underlying capability than a one-point improvement near the middle of the scale, and the logit transformation helps adjust for this.

Below are per-scaffold price-performance frontiers for two benchmarks (CORE-Bench Hard and SciCode). We include graphs for the rest of the benchmarks in the appendix. Scaffold choice moves performance more than one might expect: in some cases, switching from a generalist to a specialist scaffold can buy ~100× cheaper performance at the same accuracy. How big is this number? For context, algorithmic progress in AI inference typically cuts prices ~10× per year at fixed performance (see our [paper](https://arxiv.org/pdf/2511.23455)) — so switching scaffold can, in the strongest cases, be worth roughly two years of model progress.

Also, we see that the Claude Code scaffold with Claude models (the orange group in CORE-bench) leads to exceptionally high performance. We will speculate as to why this might be later in the piece.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/pofjfaw9v653lubhjsp9.png)*CORE-bench Hard — Clear differences between scaffolds in cost vs. accuracy, with improvements sometimes spanning two orders of magnitude. The* ***Green points in the upper graph*** *represent Claude models using the Claude-Code scaffold, which show exceptionally high performance.*

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/gh0snw7htexpjn325vy1.png)*SciCode — Scaffold differences on the Pareto frontier are irregular, but still noticeable. Note the difference in axis range compared to the previous plot.*

The scaffold-switch vectors below trace the same model moving between two scaffolds — each arrow points from one scaffold's (cost, accuracy) to another's, colored by whether the switch made the model more/less accurate and more/less expensive. We display these plots for GAIA and SciAgentBench here, but include the graphs for all benchmarks in the Appendix.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/hjxh66qcoyjuorgkwv3l.png)

*Switching scaffolds on the GAIA benchmark produces highly varied effects—some models become both cheaper and more accurate, while others see reduced accuracy, increased cost, or both. Arrows point from the generalist scaffold to the specialist scaffold and are colored based on whether they reduce price and increase performance, reduce price and reduce performance, etc. The points without arrows correspond to models that are only benchmarked on one scaffold. Blue points correspond to evaluations on HAL Generalist Scaffold.*

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/xviqbuceipllohxw8ibo.png)

*On SciAgentBench, the ScienceAgentBench Self-Debug agent consistently makes models both more accurate and less expensive, showing a uniform benefit over HAL. Note that the axis range differs from the previous plot*.

  

We see here that scaffolding can have significant interaction effects with models, most visibly on GAIA: switching from the HAL generalist scaffold to the HF Open Deep Research scaffold improves some models while hurting others. **This contrasts with most algorithmic progress in AI**, which acts as a rising tide that sometimes lifts all boats — think of GeLU or flash attention, for example, where essentially every model benefits similarly from the new innovation. It’s also a contrast to ScienceAgentBench, where the ScienceAgentBench self-debug scaffold provides a more uniform benefit to all models.

It’s not entirely clear why some models are more advantaged by a given scaffold than others. One explanation could be that some scaffolds are more advantageous at low inference budgets, while other scaffolds could be better to use at higher inference scales. Interestingly, we see some evidence of this in the Pareto frontier graphs in the Appendix.

How often do scaffolds have heterogeneous, model-specific effects rather than producing a uniform, “rising tide” improvement to all models? To get a better sense, let’s look at a transformed version of the switch vector graphs we showed above. In the versions below, we center each vector on the origin, which now each represent a model's performance on the HAL generalist scaffold. The arrows point to the difference in price and performance achieved after using alternative scaffolding — in most of the plots, specialist scaffolding adapted to the particular benchmark.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/v9wfd6puhlx1vaeq42t6.png)

*These graphs show a difference in logit benchmark performance between HAL generalist and alternative scaffolds. Origin represents performance on HAL generalist scaffold. Arrows are colored by how the specialist scaffold affects cost and benchmark accuracy: e.g green arrows mean the scaffold reduces price and improves performance.*

  

  

Averaging the vectors for each benchmark, we can arrive at a general picture of how scaffolding affects model performance. Overall, the majority of the specialist scaffolds measured in HAL improve the accuracy. However, some are only able to do this by using significantly more tokens. And, looking at the averages across benchmarks, there is significant heterogeneity. (Also, one caveat: it’s possible that the specialist scaffolds are “overfit” to their corresponding benchmarks, and might not generalize very well.)

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/hkakwetdp5nj5uwptutp.png)

*The graph represents the average effects from each of the Origin-Centered Scaffold Switches graph above. Overall, most specialist scaffolds do improve performance. Smaller confidence ellipses mean we are* ***more*** *confident in the direction and magnitude of the vector. Note: USACO only has one point, so there is no confidence ellipse around it.*

  

  

  

Scaffolding Effect on AI Leaderboard Ranking
--------------------------------------------

People sometimes create leaderboards of models based on their agentic capabilities. However, in addition to [other](https://arxiv.org/abs/2106.05532)  [known](https://arxiv.org/html/2508.11847v1) issues with leaderboard robustness, leaderboards can be very sensitive to scaffolding choices. If scaffolds have non-uniform effects, a model ranked 20th under one scaffold could place 3rd under another.

We include a formal analysis of scaffold effects on ranking in the appendix. On some benchmarks — SciCode, for instance — rankings are largely preserved across scaffolds (high rank correlation). But on most, rank-preservation measures show substantial reordering: the leaderboard you get depends heavily on the scaffold you chose to run.

Given this: how should leaderboard designers proceed? If the goal is to assess how models will perform under typical deployment conditions, the leaderboard should fix the scaffold that will actually be used. If the goal is to assess an AI system’s maximum capabilities under ideally conducive conditions, the leaderboard should run models under several scaffolds and take the best.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/dka4r2cx5meurqnzzwa5.png)

*Ranking can vary significantly between scaffolds. Green lines represent models that improved in rank when switching from the HAL generalist agent to the SWE-agent harness, while red lines represent models that decreased in rank.*

  

**Potential Implications**
==========================

Scaffolds could have a number of important implications for regulators, model developers, and society. We want to discuss a few particularly important potential implications of our findings here, as well as gesture beyond our immediate findings at future research directions.

Scaffolds May Be a New Vector of AI Capabilities Improvement
------------------------------------------------------------

Our study here shows that scaffolds can have large impacts, and some existing scaffolds vary widely in their utility. We may soon see more effort to identify which scaffolds (and features of scaffolds) are most performant, and competition to build ever-better versions. If there is a lot of room for new innovation in scaffold designs — especially AI-automated innovation — it will become important to track progress in scaffolds alongside progress in raw model capabilities.

On the other hand, it may be that there is limited room to build scaffolds much better than we have now. If that’s the case, we should expect short term gains as the field converges to the best scaffolds of the designs available or the best models, but little progress after that.

Speculatively, one reason to doubt continued progress is this: more powerful future models may no longer need advanced agentic scaffolding. (Perhaps these future AIs will just design the tools they need right as they need them?) But our personal view is that this is less likely; we expect scaffolds’ importance will continue — or grow.

Scaffolds May Affect AI Developers’ Monopoly Power
--------------------------------------------------

It’s widely contested whether AI development is a natural monopoly — will big players with lots of compute, like OpenAI and Anthropic, increasingly dominate the market for AI services, or will small developers increasingly undermine their business? While we can’t say for certain, scaffolds may be an important factor in shaping the eventual equilibrium. Our results show that using good scaffolds can yield big improvements in price and performance. Accordingly, it is conceivable that scaffolds could erode the advantage of expensive frontier models, by allowing cheap models to offer improved performance — especially if scaffolds are cheap to produce.

However, we believe that the opposite outcome is more likely: scaffolds will lead to greater concentration. Why? First, while our data isn’t sufficient to show this, it seems likely that scaffolds are to some degree complementary to compute investment. If scaffolds help more expensive models more than cheaper ones, they could increase returns to scale, which would drive concentration.

Second, we expect that scaffolds will become increasingly expensive, as firms expend inference compute to optimize their designs, and scaffolds increasingly deploy complicated ensembles of models to perform more complex, long-horizon tasks. (We’d love to see more research on this question: to what extent can scaffolds be improved with more inference compute?)

Third, and perhaps more interestingly, we speculate that there may be benefits to *co-optimizing* models and scaffolds. For instance, Anthropic can do reinforcement learning that trains Claude within their Claude Code scaffold. And they can simultaneously adjust their scaffolding to take advantage of Claude models’ unique capabilities — which only Anthropic has white-box access to. Both the Claude models and the Claude Code scaffold might then improve together, generating a synergistic performance advantage that outside actors can’t easily replicate. It requires a prohibitive cost to train a foundational model from scratch on a proprietary scaffold. While our analysis here isn’t sufficient to demonstrate that Anthropic is already getting benefits from co-optimization, we can’t rule it out — and we do observe that Claude Code seems to perform exceptionally well.

If this sort of co-optimization becomes important, Claude models might then become hyper-optimized for the Claude scaffold, with limited interoperability with other scaffolds and downstream applications. Downstream scaffold developers without control over models might even see their scaffolds’ performance decrease rather than increase with new Claude models (see how the SWE-agent harness decreases performance for some models). Just as Apple has been able to preferentially benefit its own applications over other providers' applications on its App Store, Anthropic could design Claude’s training to prioritize the downstream frameworks it wants to succeed.

Task-Specific Scaffolds May Become (More of) a Thing
----------------------------------------------------

We find numerous instances of specialist scaffolds, tailored to particular benchmark tasks, which outperform a generalist scaffold on that task. We don’t have many generalist scaffolds in our data, so it’s far too early to say that task-specific scaffolds are *typically* better than generalist ones, or anything like that. But it will be interesting to watch the field develop – if specialist scaffolds can outperform generalist ones, we may see companies spring up to provide task- or industry-specific scaffolds. (Arguably, this is a good description for some companies we already see, like Harvey and Cursor.)

Scaffold Security is Important
------------------------------

For those concerned about leakage or cybertheft of advanced AI capabilities, our findings here suggest that it may be important to keep scaffolding secure — perhaps just as important as models themselves. However, scaffolding security is significantly less discussed than model weight security. Notably, the scaffolding behind Anthropic’s breakthrough product Claude Code was accidentally [leaked in March](https://www.latimes.com/business/story/2026-04-01/anthropic-accidentally-leaked-thousands-of-lines-of-code?ref=aibad.news).

How much scaffold security matters depends significantly on how closely models and scaffolds are co-optimized. If scaffolding is highly tailored to a specific model, then exfiltration of either the scaffolding or the model weights alone is less severe because both scaffold and weight exfiltration are necessary to reach full performance. Companies can take active measures to prevent scaffold exfiltration being independently useful to attackers. For instance, by making the scaffold dependent on external APIs or tools that are only available at AI labs or legitimate organizations. On the other hand, if scaffolds are both powerful and useful regardless of what models they are used with, then scaffolding exfiltration might be a great risk. In this regime, a leaked scaffolding would be able to significantly improve capabilities for many unintended models at once with minimal adaptation.

**Conclusion and the Future of AI Capabilities**
================================================

The systems models are embedded in seem to be an important determinant of model capabilities. It’s possible that this could become increasingly so in the future. Complicated scaffolds, multi-agent networks with complex information sharing, and new structures we haven’t yet imagined may continue to blur the line between what is and is not an AI. Understanding the capabilities — as well as the alignment profile — of these new systems will then require looking beyond individual models in isolation.

  

**Appendix**
============

This appendix includes the following:

*   A table of the benchmarks and agents in our dataset
*   A table of the models in our dataset
*   An analysis of the explanatory power of scaffolds vs models
*   The full suite of Pareto analysis plots, vector analysis plots, and ranking correlation plots, and an additional plot showing how specialists scaffolds compare to HAL
*   A link to our code and data

Benchmarks
----------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511987/lexical_client_uploads/r8djcblj3ctnzf2iavec.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/obkufsi6ymlo6radq4sc.png)

*Details of each benchmark and scaffold in our dataset. This information was compiled by Claude to our specifications.*

  

Models in Dataset
-----------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/xcslao7cwqlmjp9w9z6s.png)
----------------------------------------------------------------------------------------------------------------------

*These are all the model configurations we use, along with the number of benchmarks and scaffolds each appears with. Some models were run both at a high inference setting and with no specific setting; where both occur on the same benchmark and scaffold, we keep the higher-accuracy run. A couple of models (o3 and GPT-5) appear only at a medium setting. The exception is o4-mini, which was run at a high and a low setting (rather than high/none): we keep both.*

  

Explanatory Power of Scaffolds vs Model Algorithmic Efficiency
--------------------------------------------------------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/uodzeqxf8c3lbeoirbch.png)

Methodology: our goal here is to measure how much of the variance in (logit transformed) performance is explained by scaffolds and models, controlling for log price and benchmark. (Given our sample size, we add only an additive fixed effect for each benchmark.) The issue is that benchmarks and scaffolds are highly correlated since most of the scaffolds are used exclusively on a single benchmark; we don’t want to attribute performance changes to scaffolds that are really just differences between benchmarks, but a naive regression would have no way of distinguishing. Our fix is to build up the regression incrementally. We first regress logit performance on log price and benchmarks, and observe the adjusted R^2 (which is 0.519). Then, we refit the regression twice: once with model dummies added in, and once with the scaffold dummies added in instead. In each case, we observe how the adjusted R^2 changes compared to the baseline regression with just benchmark dummies and log price. The plot above shows the explanatory power of models vs scaffolds. The takeaway is that scaffolds explain more of the variance in our data than models do, underscoring the importance of scaffolding.

  

(Running a similar regression with both scaffold and model incorporated sequentially gets similar results, regardless of the order in which the parameters are incorporated into the regression. This is because there is relatively little shared variance between scaffolds and models.)

  

Pareto Analysis Graphs For All Benchmarks
-----------------------------------------

Per-scaffold price–performance frontiers across all benchmarks. Each panel plots final accuracy (logit-scaled) against the API cost needed to reach it, with one frontier per scaffold.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/uv71wjmdemy2kfrocpkh.png)

Full Vector Analysis Graphs
---------------------------

Scaffold-switch vectors for the remaining benchmark/scaffold pairs. Each arrow traces a single model moving between two scaffolds, from one scaffold's (cost, accuracy) to the other's, colored by whether the switch made the model more/less accurate and more/less expensive, as in the figures in the main text. As in the main text, we see two types of scaffolding changes: rising-tide changes and turbulent changes. We see a roughly equivalent number of turbulent changes as rising-tide change![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/ozxtlfknwsuasiecbcvk.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/rqurilzdnyevz9wozudq.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/wffxatg3tlc8pk2keimd.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/qznhvuns5brhaiujau2t.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/lbs1tmoef7bf0w6r4hol.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/tdtq3otz4bwdsvzqib3g.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/w1lzab99v6v94avsrfjo.png)

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/cfksalc4e2tzxkltkc8l.png)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511988/lexical_client_uploads/sock7kkw8xab02fonofb.png)

Ranking Correlation Graphs
--------------------------

How well does a model's ranking on one scaffold predict its ranking on another? The chart below (left) shows [Spearman ρ](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) and [Kendall τ](https://en.wikipedia.org/wiki/Kendall_rank_correlation_coefficient) rank correlations between scaffold pairs for each benchmark. Most pairs preserve ranking moderately well, but CORE-bench Hard (CORE-Agent → Claude Code) is notably negative — the best models on one scaffold are not the best on the other. Zooming in on GAIA (right) with τ=0.17, only about a 58% chance that any two models keep their relative order across scaffolds (this is what Kendall τ rank measures). Points on the green diagonal kept their ranking; the reds (e.g. DeepSeek V3, o3 Medium) jump far off it.

Both measures run from −1 (rankings exactly reversed) through 0 (no association) to +1 (identical rankings). **Spearman's ρ** is the Pearson correlation applied to the models' rank positions rather than their raw scores: take each model's rank under scaffold A and its rank under scaffold B, and measure how linearly those two sets of rank numbers track each other. Because it works on the rank values, ρ is sensitive to *how far* a model moves — a model that falls from 2nd to 18th drags ρ down more than one that slips from 2nd to 4th. **Kendall's τ**, by contrast, only counts whether each *pair* of models keeps the same order, ignoring the size of the move.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/wvb6l7r2rky305a8q5ls.png)

*If there were any points on the green dashed line above, those would indicate models which preserved their ranking across scaffolds. There are none of these, although there is a 58% chance that each pair of models preserve their relative order to each other. Points in red are models whose relative rank was better with the HAL generalist scaffold; points in green are models whose relative rank was better with the HF Open Deep Research scaffold.*

  

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511989/lexical_client_uploads/m0pnrargpv9aggexxjal.png)

  

Specialist Scaffolding Increases Across Benchmarks
--------------------------------------------------

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782511990/lexical_client_uploads/i5yw91qoztqz0omqcota.png)

*Spider-plot of max benchmark performance across models on general (in blue) and specialist scaffolding (in green). Specialist scaffolding allows models to achieve much higher benchmark scores in several domains.*

  
Code and Data

All data was scraped from the publicly available [HAL leaderboard](https://hal.cs.princeton.edu/). The code for generating graphs and doing analysis is here: [Github](https://github.com/hansgundlach/ScaffoldingTheory).