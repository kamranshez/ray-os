# Implications of Continual Learning for LLM Agents: Introduction

- URL: https://www.lesswrong.com/posts/qChDifwpY8znER7cW/implications-of-continual-learning-for-llm-agents
- Author: RohanS
- Date: 2026-06-12
- Karma: 49  Comments: 0  Words: 1939
- Band: B  Tier: 1  Score: 47.3  Density: 10.13
- Anchors: claude\.md, scaffold(ing|s|ed)?, coding agents?

---

Many people think that **continual learning (CL)** is a key missing capability of LLM systems, and we think its development could have huge implications for the capabilities and safety of AI agents. Despite this, several important questions about CL remain underexplored:

*   What counts as continual learning? Through what pathways might LLM agents acquire CL capabilities? Which limitations of current agents would effective CL mitigate?
*   How might CL affect safety and alignment? Which threat models do we need to look out for, and which of the current safety techniques will predictably degrade as agents become stronger continual learners? In what deployment settings might the risks materialize?
*   What are some angles of attack for making CL agents safer today, given our substantial uncertainty about the shape those CL agents will take?

Our sequence aims to tackle all of these questions and more. This is the first of a series of six posts in the sequence.

Outline
=======

Post 1: Introduction
--------------------

This first post is a detailed summary of the entire sequence; the outline below describes the remaining five posts.

Post 2: [What is continual learning, and why might we expect to see it in advanced LLM agents?](https://www.lesswrong.com/posts/5mCJzimtNZc9o4e26/what-s-continual-learning-and-why-might-we-expect-to-see-it)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**The basic reason to expect effective CL is that it would probably make AI agents better at important tasks that AI companies are trying to improve performance on, most notably AI research.** How would CL help make AI agents better end-to-end AI researchers? Consider how human AI researchers improve: they do every step of the research process (i.e., read and write lots of AI research proposals, code, critiques, summaries, and papers), they learn from their successes and failures and from advice based on other people’s successes and failures, they extract generalizable insights about each step in the research process, and they progressively improve. LLM agents are already impressive: they are actively being used across most AI research activities, they can be prompted to reflect on their successes and failures, and there are various existing attempts to update their weights, contexts, memory banks, scaffolds, and tools to make them better. Some of these are somewhat effective. But so far, nothing has allowed LLM agents to become as good at end-to-end research as capable humans become after years of practice, despite the fact that LLM agents collectively accumulate research experience *much* faster than individual humans.

AI research is a particularly important example, but this argument applies to most open-ended remote labor jobs.

**So, what exactly is CL?** We say that an agent is a **continual learner** if it undergoes persistent updates during deployment. That’s more-or-less a binary criterion, but there are several other components to being *good* at continual learning that are much more continuous. We say an agent is an **effective** continual learner to the extent that it:

1.  Constantly undergoes persistent updates during deployment;
2.  Learns new useful knowledge and capabilities efficiently via those updates; and
3.  Does not (catastrophically) forget existing capabilities in the process.

We argue that **this informal definition matches intuitions and the common discourse around CL**. For example, this lets us say that effective in-context learning with very long contexts is a form of CL, but it is weaker than weight updates that persist indefinitely. This also captures the type of on-the-job, sample-efficient learning from experience that is frequently discussed on the Dwarkesh podcast and that seems to be weak or missing in LLM agents (e.g., reflecting on small sets of experiences and extracting a generalizable insight that you then use repeatedly).

**We also think this definition lets us present an accurate, nuanced picture of CL and its importance.** We simultaneously believe that CL is important, and that:

*   The amount of effective CL that an agent does lies on a spectrum rather than being a binary property;
*   Major advancements in AI capabilities may not require any breakthroughs in CL; and
*   We already have early forms of CL in LLM agents, such as [CLAUDE.md](http://claude.md) and [SKILL.md](http://skill.md) files for maintaining insights for coding agents.

We highlight **the main components of an LLM agent that can receive persistent updates during deployment**:

1.  Model weights,
2.  The context window,
    1.  Memory banks with natural language or neural activation memories,
3.  The agent scaffold, and
4.  Tools.

These cover most possible updates for LLM agents, but substantial future architectural modifications could arise and create new updatable components that end up being central to CL.

We’re still not confident about which update mechanisms seem most promising for CL, how tractable advancing it will be, and what the timelines to remote labor automation are. We think there’s a strong case that weight updates are needed for some parts of effective CL: [LLMs seem quite bad at handling lots of interrelated complexity in their context window](https://www.lesswrong.com/posts/ZJZZEuPFKeEdkrRyf/why-we-should-expect-ruthless-sociopath-asi?commentId=Ru2bpwgXaqwgMXrbn), which limits the number of novel insights they can generate and utilize without weight updates. Knowing what to take away from past successes and failures in order to succeed at tasks you would otherwise fail at seems challenging.

Post 3: [How might continual learning affect safety and alignment?](https://www.lesswrong.com/posts/j2zBqt7AksoEoHXNp/how-might-continual-learning-affect-safety-and-alignment)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

We begin the post by distinguishing between several properties of CL agents that affect their risk profiles: bounded vs. unbounded updates, legible vs. inscrutable updates[^vwkajratk6e], and individual vs. shared memories. We then move on to concrete safety effects that CL agents may cause. **We argue that CL raises two major safety concerns, both of which can be broken down into three subconcerns**. These are summarized in the following figure, along with three potential alignment benefits of CL:

![Group 96(2).png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781217427/lexical_client_uploads/z7nmev3pntymvnqkoczy.png)

We identify three pathways for goal and value change:

**Loss of developer-side control over generalization.** When AI companies post-train a model, they can carefully curate the training environments to minimize the risk of undesirable generalization. In contrast, strong CL agents could undergo most of their training in deployment-time environments, where by default the training data isn't selected with alignment in mind. Not all deployment-time environments will incentivize misaligned behaviors, but it’s plausible that several of them do. We recommend the development of character training methods that make agents more robust to poor generalization when trained on such tasks and developing a better understanding of LLM generalization.

**Value systematization.** Reflecting on subgoals is an important cognitive move for any agent pursuing open-ended goals. We expect that CL agents will increasingly make use of it, as the outcomes of the reflection process will persist in their memory, and to face several triggers that might prompt them to also reflect on their high-level motivations. These triggers include conflicting goals, developer-driven reflection, encountering OOD situations, and ontological shifts. Reflection on high-level motivations is likely to involve *value systematization*: the process of systematizing one’s previous values as examples or special cases of simpler, more broadly applicable values. While value systematization will necessarily occur in general agents capable of making philosophical progress, we should attempt to steer it toward favourable convergence. Monitorable reasoning, interpretable CL updates, and character training are some tools that might make this process more steerable.

**Memetic effects.** CL may open channels (shared memory banks and weight updates) for *direct memetic spread* between instances. This is concerning because if influence-seeking values arise in any instance, they may propagate into other instances more effectively than other drives, and this opens a more direct channel for that to happen.

These mechanisms could compound: an agent might acquire undesirable contextually activated goals through poor generalization from deployment-time training, refine them into beyond-episode goals through reflection, and propagate them memetically.

We also identify three negative consequences arising from loss of last-mover advantage:

**Behavioral auditing becomes more difficult.** Once AIs have deployment-time memories that contain multiple subjective months’ worth of state, pre-deployment evaluators may be unable to simulate deployment conditions realistically enough. Auditing results would no longer give us reliable signals about how models will behave in the wild. This can be mitigated by frequent deployment-time auditing, but that might be prohibitively expensive. Another mitigation is to use CL agents that only perform text-based updates, but such agents might be outcompeted.

**Pretraining data filtering becomes less useful.** If LLMs can learn from data that was removed from their pretraining corpus at deployment-time, that reduces the utility of data filtering. Filtering might still be useful for shaping models’ propensities early in training, but it’s less likely to remain a viable countermeasure to misuse.

**AI control protocols might degrade.** We analyze the impact of CL on AI control and conclude that the effects depend a lot on the CL agent’s architecture, but it’s plausible that at least some protocols will degrade.

After discussing the risks, we also discuss the likelihood that they materialize in internal vs. external deployments and in deployments by open-source vs. closed-source developers. We finish by highlighting potential alignment benefits of CL: natural-language memories would provide additional monitoring surface, ongoing learning could enable faster feedback loops in alignment training, and episodic memories could enable models to produce better self-reports.

Post 4: [What are some angles of attack for making continual learning safer?](https://www.lesswrong.com/posts/FKggLpnfbpbYvnjfG/angles-of-attack-for-continual-learning-safety)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The fact that current models are very weak CL agents means that it is hard to identify tractable angles of attack for making CL safer. We tentatively argue for focusing on three broad goals: **deconfusion** about the nature of CL and its safety implications, **differentially advancing safer CL implementations**, and **creating evals that scale to CL agents or incentivize the development of safer CL agents**.

We start off with a few high-level recommendations that came up throughout the post on safety effects and that we’re relatively confident about: ensuring that CL architectures are interpretable and easy-to-control, both through developing new methods and through advocacy, and improving the robustness of character training.

We then highlight the following deconfusion projects:

*   Empirically studying realistic goal shifts, e.g. by training model organisms that have conflicting contextually activated goals.
*   Exploring various conceptual questions about value systematization.
*   Studying what constitutions are more stable under reflection.
*   Training model organisms of ontological shifts.
*   Forecasting the likelihood of different safety effects, such as the likelihood that CL agents reflect on their high-level motivations and the likelihood that the field converges on primarily text-based or weight-based update mechanisms.

For differentially advancing safer CL implementations, we propose three ideas:

*   Developing prompt optimization as a tool with which CL agents can perform their safety-critical updates in the text-space rather than weight-space.
*   Developing novel AI control techniques aimed at making CL safer and CL agents that are amenable to those methods.
*   Ensuring that the memories of the CL agent are interpretable, even when the update mechanism isn’t.

Finally, we propose some projects for advancing CL evals:

*   Create evaluation frameworks and mechanisms for evaluating behavioral trajectories, following [Pacchiardi et al. (2026)](https://cl-eval.github.io/).
*   Create evals that measure the interpretability of CL agents.

Post 5: [Results from a small survey on continual learning](https://www.lesswrong.com/posts/qZrbhoaEALFTmyidr/perspectives-on-continual-learning-survey-results-and)
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

We sent a survey based on an earlier draft of this sequence to several knowledgeable people for feedback. We found their responses useful and interesting, so we’re publishing them.

Post 6: A literature review on continual learning
-------------------------------------------------

This is a companion post surveying existing approaches to continual learning, relevant benchmarks and evaluations, and neuroscience literature on continual learning in humans. We prioritize high-level views and analysis over detailed technical approaches.

Acknowledgements
================

Thanks to Anson Ho, Erik Jenner, Rubi Hudson, Joey Yudelson, Dennis Akar, Vladimir Ivanov, Shubhorup Biswas, Ryan Faulkner, Tim Hua, Atharva Nihalani, and Angelo Huang for comments on a draft version of the sequence. Thanks also to Chad DeChant, Evgenii Opryshko, Jake Mendel, Caleb Biddulph, and Andrei Muresanu for helpful conversations about various parts of the sequence.

[^vwkajratk6e]: An important subdistinction here is weight-based vs. text-based updates. 

[^ut3po9quaxe]: This includes memory banks with natural language or neural activation memories that get retrieved into context or activation space when relevant.