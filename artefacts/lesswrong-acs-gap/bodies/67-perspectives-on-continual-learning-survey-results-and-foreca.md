# Perspectives on Continual Learning: Survey Results and Forecasts

- URL: https://www.lesswrong.com/posts/qZrbhoaEALFTmyidr/perspectives-on-continual-learning-survey-results-and
- Author: Rauno Arike
- Date: 2026-06-24
- Karma: 33  Comments: 0  Words: 3572
- Band: C  Tier: 1  Score: 24.0  Density: 4.01
- Anchors: \bcodex\b, coding agents?, \bharness(es|ing)?\b

---

*This is the fifth post in the sequence* [*Implications of Continual Learning for LLM Agents*](https://www.lesswrong.com/s/oc5Auteiibo56kNXw).

Summary
=======

While writing our continual learning sequence, we sent a survey to a number of AI safety researchers with questions about continual learning. This post summarizes the results of that survey. We asked whether respondents agree with various arguments we advance throughout the sequence, how worried respondents are about certain risks, how respondents would forecast different aspects of the future of CL, and how promising respondents find various proposed angles of attack. We also asked open-ended questions about the benefits of CL and whether we seem to be missing any major considerations. At the end of the post, we also provide an overview of forecasts about CL made by other experts who didn’t participate in our survey.

We received survey responses from:

*   Ryan Faulkner, PhD student at the University of Toronto focusing on multi-agent simulation, learning, and cooperation
*   Nikola Jurkovic, Member of Technical Staff at METR
*   Alex Mallen, Member of Technical Staff at Redwood Research, doing research and writing on AI threat models. Author of "The case for countermeasures to memetic spread of misaligned values"
*   Evgenii Opryshko, 3rd year PhD student at the University of Toronto working on LLM-related research
*   Anders Cairns Woodruff, Astra research fellow at Redwood Research and undergraduate student at McGill University
*   4 respondents who requested anonymity
*   1 respondent who requested that we not present their responses at all, and only use them for internal feedback.

All questions were optional, meaning that different questions received different numbers of responses. We made substantial changes to the sequence after conducting the survey, but think that the survey results are nevertheless valuable. We will flag throughout the post when our sequence diverges from the content that the survey participants commented on.

This was a fairly low-effort survey. There is certainly room for a survey with a more systematic methodology, a larger number of respondents, and more established experts. Nevertheless, we think the results are worth publishing.

Broad takeaways
===============

Among our respondents, there is little consensus on the future of continual learning. Out of 18 numerical questions (scored on a 1-10 scale or as a 0-100% probability), only three questions produced responses that all fell on the same side of the midpoint: everybody ranks our definition of CL at least 5/10, everybody expects that CL will increase the attack surface for adversarial fine-tuning, and everybody thinks that further deconfusion research on CL would be valuable for AI safety. Beyond these points of agreement, responses varied widely: all three forecasting questions had response ranges of 70 percentage points, and on questions on a 1-10 scale, the median response range was 5 points.

Respondents were generally skeptical about differential development and its potential to advance safety more than capabilities. However, we substantially modified the angles of attack we suggested for differential development between the survey and the publication of the sequence, and are unsure whether their skepticism extends to the directions we proposed in the final version.

5/7 respondents hold it at less than 50% that we will see widespread CL agents in the next 3 years, and 3/7 are under 30%. However, 4/6 respondents have it at over 50% that the first transformative AIs will be CL agents, and 3/6 at over 70%.

8/9 respondents expect LLM-based CL agents to reflect on their goals, but only 3/7 expect early transformative CL agents to undergo significant goal drift due to reflection.

Full results
============

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/5c28ad606b04f5c940711306c96fb864a22f87dfab04f7ac0038fb3d1c2a4770/enhw7ax04gslkblehj3j)

Our definition during the survey differed from the final one in wording, but was similar in its substantive features. It was stated as follows:

Informally, we say that an agent is an effective continual learner to the extent that it:

1.  Undergoes  [online](https://en.wikipedia.org/wiki/Online_machine_learning), persistent updates during deployment;
2.  Learns new capabilities efficiently from those updates; and
3.  Does not (catastrophically) forget existing capabilities in the process.

Two comments argue that this definition seems to require weight updates specifically, excluding things like a model writing skills for itself. Recall our final definition [here](https://www.lesswrong.com/posts/5mCJzimtNZc9o4e26/what-s-continual-learning-and-why-might-we-expect-to-see-it#So__what_exactly_is_continual_learning_).

Futures
-------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/c5514154cd6d9b2263e68afb675c0d6a4a708f61b597e15a367a0f64a5cc0347/csdv6atlx1gexr2jy5tj)

One respondent at 40% writes, “I think I would be at 65% if you replace ‘widespread’ with ‘exist working prototypes but there are some blockers that prevent their widespread deployment (e.g. cost, reliability, security).’” Another respondent expects 10-15 years. A third argues that our informal definition is not rigorous enough to make a prediction.

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/858a8cccbbe30c42054f4603d4d6320d10ec71e0dc19aa51d8bb69652b7df1f3/wtuiyevnccbwa6impy97)

Here, we operationalize transformative AI as AI that can autonomously perform tasks that account for the majority of full-time jobs worldwide, and/or over 50% of total world wages.

Reflection and goal drift
-------------------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/bf79b2ded8f8fe1cd73036bebacf16327765c33c66340764dba34822df5db51e/ps1zelsmod3cqamda5md)

One respondent thinks that reflection on goals and motivations is most likely to be specifically caused by things like tensions between propensities and out-of-distribution settings in which their existing goals do not straightforwardly prescribe actions. There is less reason to expect that an agent with an already-monolithic goal will reflect and pursue a different goal.

  

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/558c90671de34677389ea73cd504f7c7146333d01c871dc51033e9e0d9d1e2a8/brkidsukagfmic7dqf9m)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/d15e8fd516688be4739fa53cbda1713467196fcc3e3b9d651ac52f7c63e4eebf/ibjtmzf1zdbz9xfxuh1v)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/1dab70deb86a25eec7e103ca9410f909f5f6b4c70a69dd8e473ee4e5cbd5559b/tusoyag3btlepx6bm2jb)

One respondent argues that memetic spread is already relevant to current, non-CL agents. Another writes, “I don't think of this mechanism as very distinct from the things you've been talking about earlier.”

Loss of the last-mover advantage
--------------------------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/fa2c071d2f80bed1296f0983adbde5a75cdd3c07cfc2b8bdc6c35fc152ab9ba6/ydguer1w7gmmvruej6mr)

One respondent argues that pretraining filtering is already less important where many agents have search access. Two others argue that pretraining is important for shaping early concepts and propensities in models, and that filtering should remain effective at positively influencing this. Another respondent suggests that companies could filter data at the layer where CL happens, though this might be complicated.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/15152df8aa81abd45ef4348ea80d019a108a542d850fa87e57596c797d4c20a0/dz7ljrfeiwqfjr0pfbzv)

A respondent argues that this is why labs haven’t implemented CL: you don’t know what the user will write, so ultimately can’t control the behavior of the model.

Control
-------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/c46fc2487e5d8701e82604eaee4e0b25eb334323087d0985da9b100b8007083b/g8eot5e0ztdelltdleey)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/a0ed1a7cfec84173347d82984741cce807511f6d65c1bb60942f67d3251de6ad/rjrzpfxtwdkjywy4erpo)

"The monitor can have a read-only access to the memory bank or a copy of it where it can write information, turning it to a one-way communication channel similar to existing channels like CoT"

"I'm not sure we can verify an agent isn't sending collusion signals in regular text. 1) the text may not be interpretable to us and 2) there might be so much text that human review is near-impossible, so even blatant collusion signals are ok. Overall, I think that we should be much more worried about collusion than the existing CoT literature is."

"I think UM isn't hurt by CL in particular - it's hurt by opaque reasoning… I do think that continual learning can enable agents to better learn how to bypass trusted monitors. So, using monitoring protocols against CL agents is more like training against monitors in its risks."

In the current version of the sequence, we no longer make the claim that untrusted monitoring and trusted editing are the two control protocols that will be affected the most, though we still expect both of them to be affected by CL.

Angles of attack
----------------

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/32f8f9fdb7b1ac86b442b0dcdbb09ced4154b1b06f3c3f1bcaee7ae6c697972e/wq3ozskwzycg2m6ec4mq)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/c6754cf5790dc6cc05dc11e647823e70ed51e56adb2072e1fc800eae7737b54c/knjrkxltfl32wfpdmuda)

By “the questions above”, we refer to the following:

*   In what order will we automate tasks relevant to CL and AI R&D?
*   Which CL and AI R&D tasks are automatable now, and which ones have prerequisites?
*   Which CL and AI R&D tasks, if automated, would most speed up the path to other CL and AI R&D tasks?
*   How will progress on tasks outside of CL and AI R&D (such as automating other remote labor) affect and be affected by progress on CL and AI R&D tasks?
*   How and in what order will LLM monitorability, capabilities, and likelihood of egregious misalignment from reflection on goals develop over time?

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/597ad9541cd66085d544acc3916fdcda023c87935cf8d8a404f5c5a17d287994/kt1zimhkzvhb3tnvphs6)![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/22ca8d24f2684953b2dfeba6d80e5a20125a83722dcec5f941b80584e59592a6/xhamwcqejs1nzukamovx)

One respondent is doubtful that differential progress is feasible: either one way of doing it is better or it is not, and enough people are looking for ways to implement CL that you are unlikely to make the difference.  
  
As already mentioned, the concrete projects we mentioned in the version of the sequence read by the survey participants differ substantially from the angles of attack we suggest in the final version of the sequence.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qZrbhoaEALFTmyidr/a5704f59685b30fa4e0746db51807c4c6b58b4d084084e81ce605ff1271e3beb/rmyfku6lwie6reyawljz)

Open-ended questions
--------------------

**What would you expect to be the biggest safety benefits of CL, if any?**

Respondents mention:

*   Helps accelerate and automate safety work
*   Easier to make model organisms
*   Potentially easier to steer the model by putting the appropriately marked examples of good and bad behaviors into memory bank, which can be updated during deployment
*   Cheaper/easier to fix minor misalignments
*   Being able to get a better sense of human values as time goes on/lock in aligned values and find ways to prevent becoming misaligned
*   Oversight and control over the learning process; not necessarily more than other training though

**Based on the excerpts in this survey, what important considerations about CL safety do you think we're missing entirely?**

*   "CL probably massively accelerates public adoption of AI, which makes a pause politically harder and AI companies more profitable."
*   “CL might mean that capabilities gains will require broad deployment of AI in society… This would change the sociopolitical dynamics of AI development.”
*   “I think CL might make model organism training a lot trickier, especially if the ‘online’ part of model learning is important. You also just effectively have lots of ‘different’ models (i.e., the same model as it learns over time) to work with and guard against.”
*   “We might be a lot closer to \[CL\] than you're imagining. Current internal deployments might share a lot of state via codebases, skill files, etc.”
*   “This generally makes predicting AI motivations way different and probably much harder because it's probably the result of a bunch of intentional serial reasoning. Imagine predicting human cultural evolution.”

* * *

Forecasts from other experts
============================

Here, we compile ideas from various thinkers about how quickly continual learning might manifest and what form it might take. We draw from both more formal pieces of forecasting work and less formal takes aired on podcasts/Substack/Twitter.

[AI 2027](https://ai-2027.com)
------------------------------

AI 2027 forecasts a steady growth in the rate at which models learn, and the methods by which they do so. In early 2026, leading models are still bad at long-horizon tasks in general, though they can solve hours-long programming assignments. By early 2027, the leading model undergoes RL almost continuously, with weights getting updated daily, so that the model is effectively learning online. This is followed by “a more scalable and efficient way to learn from the results of high-effort task solutions,” to squeeze the most out of this continual RL. By late 2027, people start “referring not to a particular instance of Agent-4 but rather to the whole collective.” Agent-4, which is misaligned, is a strong enough continual learner that it can act on complex, ambitious, long-horizon real-world goals.

IABIED
------

IABIED does not refer directly to continual learning. However, it does relate a story meant to convey how ASI could lead to human extinction, which could be loosely interpreted as a forecast. In the story, a company named Galvanic develops a system called “Sable”. The two main differences from current models are that Sable has “a more humanlike long-term memory; it can learn, and remember what it has learned”, and that Sable “performs better the more machines it runs on in parallel”. The continual learning ability in this narrative appears to be enabled by advancements in episodic memory. We do not receive further details regarding its implementation, or the exact timeline over which these advancements occur.

[Understanding AI Trajectories: Mapping the Limitations of Current AI Systems](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/68fb86aa2c3b1b7ea6251cc1_Understanding%20AI%20Trajectories%20\(24_10%20update\).pdf)
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

This UK AISI paper identifies 8 indicators of progress against current AI limitations that may be necessary for achieving AGI, and how much progress has been made so far on each. One of these is “Continual learning post-deployment,” and a few others are also related to CL.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/d3b143c3fbc88a72cd46a69bc5ab4b9dd621f704c272dca67da7e33f6e300ae7/g69i5b2wksucyjc5w2ff)

[Brain-like AGI safety](https://www.lesswrong.com/sequences/HzcM2dkCq7fwXBej8)
------------------------------------------------------------------------------

Brain-like AGI safety argues that AGI architectures will likely need to resemble the human brain more than current LLM systems. The brain, author Steven Byrnes argues, is made of roughly 90% material that “learns from scratch” with randomly initialized weights (the “learning subsystem”), and 10% hardcoded material (the “steering subsystem”). This picture stands in contrast to the notion of “evolutionary pretraining” – the brain is largely not useful at birth. The steering subsystem provides things like instincts, and is particularly important early in the individual’s lifetime; for example, curiosity in babies helps the learning subsystem learn quickly. There are competing hypotheses about the extent to which the brain learns from scratch, but it’s not a particularly popular question in neuroscience, so it’s hard to say the extent to which this view is agreed upon.

Byrnes also argues that brain-like AGI, i.e. AGI algorithms with big-picture similarities to human brain algorithms, are >>50% likely to come into existence. Notably, this is a totally different paradigm from the current LLM paradigm. Under brain-like AGI, one lifetime is equivalent to one training run. In humans, it takes decades to reach general competence/expertise levels, but in AGIs this could plausibly be much shorter. There would be no distinction between training and inference; rather, brain-like AGIs would be continual learners, doing the exact same thing under training and deployment settings.

Byrnes argues this is bad for safety. The fundamental problem is that you can’t reliably keep even your own future self accountable to your present self. An aligned, continually learning AGI wouldn’t be able to do so either. We can come up with clever tricks like respawning fresh instances of the t_0 aligned model to monitor the model that’s spent time learning, but ideas like this are far from guarantees of safety.

Other forecasts and opinions
----------------------------

[Zvi Mowshowitz](https://thezvi.substack.com/p/ai-155-welcome-to-recursive-self): "Models are continuously learning in general, in the sense that every few months the model gets better. And if you try to bake other learning into the weights, then every few months you would have to start that process over again or stay one model behind.

I expect ‘continual learning’ to be solved primarily via skills and context, and for this to be plenty good enough, and for this to be clear within the year." \[Feb 2026\]

[Dean Ball](https://x.com/deanwball/status/2020179119330455973): the continual learning deficit is more tractable than previously thought with in-context learning. Opus 4.6 will look through previous codebases on the machine, understand relevant e.g. architectural decisions that were made, and incorporate these learnings into its current work.

“Codex 5.3 and Opus 4.6 in their respective coding agent harnesses have meaningfully updated my thinking about 'continual learning.' I now believe this capability deficit is more tractable than I realized with in-context learning…

When I ask 4.6 in particular to do some complex project, it will look for times when I (/my coding agents) have tackled similar problems, made similar architectural/infrastructural decisions, or even drawn on the same datasets. It will say things like, ‘I noticed, on this unrelated project from two months ago, that you ran into a problem here because of \[e.g.\] a non-obvious data preprocessing step required for using this dataset with Tool Y. Since our plan is to use Tool Y again for this project, I'll keep this in mind when I build the data processing pipeline.’...

This is the kind of insight a software engineer might learn as they perform their duties over a period of days, weeks, and months. Thus I struggle to see how it is not a kind of on-the-job learning, happening from entirely within the 'current paradigm' of AI. No architectural tweaks, no 'breakthrough' in 'continual learning' required.” \[Feb 2026\]

[Samuel Hammond](https://x.com/hamandcheese/status/2020238406593245516): “In-context learning is (almost) all you need. The KV cache is normally explained as a content addressable memory, but it can also be thought of \[as\] a stateful mechanism for fast weight updates. The model's true parameters are fixed, but the KV state makes the model behave \*as if\* its weights updated conditional on the input. In simple cases, a single attention layer effectively implements a one-step gradient-like update rule…

Attempts to solve for continual learning will treat KV as a fast episodic state, then learn a consolidation operator / hypernetwork that compiles that state into a small parameter delta, so the next session starts from an empty cache but a slightly updated model you can validate matches the old model using probes…

So long as companies keep putting out new and smarter base models every few months, there may thus not be a huge amount to gain from true continual learning over and above in-context learning. It also sidesteps the thorny privacy issues implied by models that form persistent memories of users' data, not to mention the arguably greater moral patienthood of AIs that learn from unique experience trajectories to form the sort of continuity of identity we associate with persons.” \[Feb 2026\]

[Sholto Douglas](https://x.com/NoPriorsPod/status/2002120381709365257): “I also think that probably continual learning gets solved in a satisfying way…next year.” \[Dec 2025\]

[Andrej Karpathy](https://www.dwarkesh.com/p/andrej-karpathy): “We have some very early agents that are extremely impressive and that I use daily—Claude and Codex and so on—but I still feel there’s so much work to be done. My reaction is we’ll be working with these things for a decade…They don’t have enough intelligence, they’re not multimodal enough, they can’t do computer use…They don’t have continual learning… It will take about a decade to work through all of those issues.” \[Oct 2025\]

[AGI’s Last Bottlenecks](https://ai-frontiers.org/articles/agis-last-bottlenecks): “The only broad domain in which GPT-4 and GPT-5 both score zero is long-term memory storage, or continual learning…Of all the gaps between today’s models and AGI, this is the most uncertain in terms of timeline and resolution. Every missing capability we have discussed so far can probably be achieved by business-as-usual engineering, but for continual long-term memory storage, we need a breakthrough. Nonetheless, the problem is not completely opaque, and probably won’t require a paradigm shift.

…

We may only need an o1-preview moment for continual learning and long-term memory storage, that is, a standard breakthrough away.” \[Oct 2025\]

[Dario Amodei](https://www.youtube.com/watch?v=mYDSSRS-B5U): “We have some evidence to suggest that \[continual learning\] is another of those problems that is not as difficult as it seems.” \[July 2025\]

[Dwarkesh Patel](https://www.dwarkesh.com/p/timelines-june-2025): Forecasts median 2032 for the following to come true: “AI learns on the job as easily, organically, seamlessly, and quickly as a human, for any white collar work. For example, if I hire an AI video editor, after six months, it has as much actionable, deep understanding of my preferences, our channel, what works for the audience, etc as a human would.” \[June 2025\]

[Daniel Kokotajlo](https://www.dwarkesh.com/p/timelines-june-2025/comment/122562467) (re: Dwarkesh): “You say 50% by 2032 on whereas I'm at 50% by end of 2028. Here, my argument is simple: I think that once you get to the superhuman coder milestone, the pace of algorithmic progress will accelerate, and then you'll reach full AI R&D automation and it'll accelerate further, etc. Basically I think that progress will be much faster than normal around that time, and so innovations like flexible online learning that feel intuitively like they might come in 2032 will instead come later that same year.” \[June 2025\]

[Ryan Greenblatt](https://x.com/RyanPGreenblatt/status/1929757554919592008?s=20):

My best guess is that the way humans learn on the job is mostly by noticing when something went well (or poorly) and then sample efficiently updating (with their brain doing something analogous to an RL update). In some cases, this is based on external feedback (e.g. from a coworker) and in some cases it's based on self-verification: the person just looking at the outcome of their actions and then determining if it went well or poorly.

So, you could imagine RL'ing an AI based on both external feedback and self-verification like this. And, this would be a "deliberate, adaptive process" like human learning. Why would this currently work worse than human learning?

Current AIs are worse than humans at two things which makes RL (quantitatively) much worse for them:

1\. Robust self-verification: the ability to correctly determine when you've done something well/poorly in a way which is robust to you optimizing against it.

2\. Sample efficiency: how much you learn from each update (potentially leveraging stuff like determining what caused things to go well/poorly which humans certainly take advantage of). This is especially important if you have sparse external feedback.

But, these are more like quantitative than qualitative issues IMO. AIs (and RL methods) are improving at both of these.

\[June 2025\]

[Nathan Lambert](https://www.interconnects.ai/p/contra-dwarkesh-on-continual-learning) (re: Dwarkesh):

“Do language models reason like humans? No.

Do language models reason? Yes.

Will language model systems continually learn like humans? No.

Will language model systems continually learn? Of course.

…

Language models can already pick up subtle context extremely fast. ChatGPT’s memory feature has gotten far better for me. When we’re using the far more powerful models we can expect in the next 18 months this’ll already start to appear magical. Language models are extremely apt at inferring context even without us giving it to them. Soon we’ll be unlocking that subtle connection engine by providing immense, explicit context.

…

Reasoning models have made in-context learning far more powerful…With these reasoning models and smart retrieval of context, the systems we are building will look indistinguishable from continual learning…The path to continual learning is more context and more horsepower.” \[Aug 2025\]

[Daniel Paleka](https://x.com/dpaleka/status/2007210620471705935):  
“here is how to solve continual learning:

1\. long context

2\. all useful user or env feedback goes to claude md

3\. when a section in claude md is long, it becomes a skill

that's it, two levels of hierarchy, no finetuning, don't overcomplicate things.”