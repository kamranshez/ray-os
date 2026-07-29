# Superhuman Articulacy as an LLM Safety Target

- URL: https://www.lesswrong.com/posts/tAwqzanzc9YYnwuK4/superhuman-articulacy-as-an-llm-safety-target
- Author: Dylan Bowman
- Date: 2026-07-07
- Karma: 51  Comments: 9  Words: 1436
- Band: B  Tier: 1  Score: 49.9  Density: 10.38
- Anchors: coding agents?, sub-?agents?

---

**TL;DR: Current LLMs are bad communicators relative to their agentic capabilities. I claim that articulacy is useful (and perhaps necessary) for AI safety and suggest a path for improving articulacy.**

Briefly: a theory for articulacy
================================

Frequently, LLM agents miscommunicate with their human operators, such as when they write documentation or respond to queries about their activity during a coding session. Any given communication failure can be ascribed to either or both of these two factors:

1.  Articulacy
    1.  Is the model capable of communicating in a precise and human-readable way?
2.  Truthfulness
    1.  Does the model have the propensity to accurately report what it sees, or does it overclaim etc.?
    2.  Does the model have the propensity to attempt to retrieve more information so it can produce a more accurate output?
    3.  Does the model have the propensity to inaccurately report what it sees so that it can accomplish some downstream objective?

In this document I’ll discuss the first item: articulacy. Truthfulness is its own issue and belongs with the behavioral cloud Ryan Greenblatt describes in [“Current AIs seem pretty misaligned to me”](https://www.lesswrong.com/posts/WewsByywWNhX9rtwi/current-ais-seem-pretty-misaligned-to-me).

Current LLMs are inarticulate
=============================

Human operators of coding agents constantly complain about LLM technical writing, in both documentation (e.g., PR descriptions) and in direct communication between the LLM and user. In absence of some coherent theory for this, here’s a list of phenomena mined from my own coding agent history:

*   **LLMs will make up jargon for abstractions they use to describe the environment** (e.g., a chunk of code), oftentimes with gratuitous hyphen usage. Some examples from my traces: “3-submission backtest budget”, “end-of-episode parallelization”, “deception-affordance example” – obviously these don’t make sense without context, but they didn’t even make sense *in context* (all 3 of these usages were followed by a message from me asking what the hell it meant by these phrases).
*   **LLMs will use inconsistent terminology to identify a given referent**. This phenomenon is extremely frustrating in technical writing (and frequent in humans as well), since precision is important. “The report” might alternatively be referred to as “the document” or “the deliverable” in the very next line.
*   **LLMs are overly verbose**. Very frequently I’ll have to ask the LLMs to stay under some character limit or provide a condensed version of an earlier response.
*   **LLMs are bad at making short names for items or providing short descriptions**. In particular I'm thinking about variable names in code, resource slugs, headers for documents, names for metrics, and any kind of annotation.
*   **LLMs will use shorthand where it is entirely inappropriate.** In the context of technical writing, precision is extremely important. When LLMs use shorthand, it seems to be an attempt to improve the “flow” of the writing but it simply makes the prose less clear. Some examples from my coding agent history:
    *   “Good question — let me be precise, because I was using shorthand.”
    *   “‘The report’ is shorthand I've been using for a specific, real deliverable:”
    *   “I wrote "\[model name\]" as a careless shorthand for the actual string in the yaml, \[model name\]-visible-cot, instead of quoting it verbatim. No reason beyond sloppy paraphrasing — I abbreviated the model name in my prose rather than copying the exact slug.”
*   **LLMs assume readers share their context**. One source of the above items concerning jargon, inconsistent terminology, and shorthand, is that the LLM seems to assume that you, the reader, have *also* been poring over every tool call, and furthermore that any future readers have also consumed this context. I don’t have any evidence to point to here, since obviously an LLM will not state this belief when asked, but this is how it *feels*.
*   **LLMs use ultra-passive voice and other alien grammatical customs** (citing [this](https://x.com/psychiel/status/2074135221172060413?s=46)).

From an outsider perspective, here are some hypotheses about why the above phenomena appear:

*   **Benign misalignment from misspecified reward during training**. As detailed in “Current AIs seem pretty misaligned to me”, frontier models have a ton of RL thrown at them and inevitably the reward functions are misspecified. I left out plenty of phenomena I’ve observed from the above list because they’re very obviously just more general drives instilled by current RL, such as overclaiming their results and omitting contradictory information, and thus belong in the truthfulness bucket.
*   **LLMs are often graded by an LLM judge that takes in the entire context of the rollout**. This applies for both RLVR and RLHF/RLAIF. Thus, there’s less pressure to have *all* of the relevant information clearly stated in any given message. This is my explanation for the phenomenon where LLMs assume you have context, since naturally if you were trained for millions of RL episodes where you were rewarded on your entire context your prose generation mechanism would develop a prior that the counterparty has seen everything.
*   **LLMs are trained to communicate with subagents, agent interlocutors, agent graders (e.g., ones that grade documentation), and future versions of themselves after compaction, but NOT humans**. In the environments where agents actually do need to communicate, they are talking to other LLMs instead of humans, so they develop prose that is more cognitively amenable to LLMs than humans.
*   **Unavoidably, LLMs do not know how closely the human operator is paying attention to a given session**. This means that they don’t know how much of the prior context they should repeat for any given user query.

But even with these mechanistic explanations, there’s an even clearer reason why LLMs are inarticulate: it’s just really hard to measure this kind of thing. Good writing is quite difficult to specify and even harder to verify, and without good metrics, it’s quite difficult to improve. The commercial incentive is not strong enough for labs to prioritize articulacy and we haven’t yet seen the harms of a significant capability-articulacy overhang, although there may be growing concern about this within labs.

Superhuman articulacy in LLMs is useful for AI safety
=====================================================

So why is articulacy good for safety? I’ll make three specific claims:

1.  Superhuman articulacy helps with scalable oversight.
2.  Superhuman articulacy delays handoff.
3.  Superhuman articulacy narrows down explanations for deceptive behavior.

Articulacy helps with scalable oversight because it means that LLMs can effectively report on the behavior of other LLMs to humans. As AGI becomes more intelligent and its actions and motives are harder to understand, any scalable oversight setup that relies on humans in the loop will require progressively more articulate AGIs to explain their behavior.

LLM articulacy also delays [handoff](https://www.lesswrong.com/posts/YuMr6kbstuieQHkGj/types-of-handoff-to-ais). Handoff for a given domain will happen when human oversight becomes the bottleneck. If LLMs can communicate effectively with humans, then humans become the bottleneck later in time. You could also think of this as extending the centaur period of the ASI ramp-up era.

Finally, LLM articulacy excludes possible explanations for LLM misbehavior. Going back to the decomposition of miscommunication into articulacy and truthfulness: if we have superhuman articulacy, then the probability of any given miscommunication arising from untruthfulness increases, and thus miscommunication becomes a more reliable signal of untruthfulness.

Articulacy can be improved through evals
========================================

Like any other capability, the path to improve articulacy lies in creating high-quality evaluations which can be hill-climbed. In particular, a high-quality public eval for articulacy has much to offer over labs developing this in-house:

1.  A public eval developed by an independent body avoids accusations of bias that would follow one developed by a lab, especially in a less-clear domain like articulacy. For example, if OpenAI published an eval for articulacy, one could argue that the principles for articulacy that its graders use are actually the same principles OpenAI uses to train the prose of its own models.
2.  The public nature of the eval creates a visible contest for articulacy.
3.  The creation of an eval provides the initial template for data providers to create post-training data of that shape.

But what could a good eval for articulacy look like? A naive idea is simply to take technical text summarization evals and apply rubrics that rigorously specify what effective communication looks like. Scaling this up, perhaps skilled human writers could assemble a constitution for high-quality communication.

Reasons not to invest in articulacy
===================================

*   Maybe improving articulacy advances towards superhuman persuasion.
*   Improved articulacy hastens diffusion of AI into the economy since it would be easier to delegate more work to it. You could argue this would shorten timelines.
*   Maybe inarticulacy is only a temporary problem that gets solved by building smarter models.
*   It’s unclear if articulacy is scalable to a superhuman level (still worth working on in my opinion).