# Resolution (fka Sequent): scale and automation for higher confidence in alignment

- URL: https://www.lesswrong.com/posts/AP7YDke5jjY4v3X9Z/resolution-fka-sequent-scale-and-automation-for-higher
- Author: Geoffrey Irving
- Date: 2026-06-10
- Karma: 297  Comments: 5  Words: 3439
- Band: B  Tier: 1  Score: 33.7  Density: 5.23
- Anchors: claude code, \bcodex\b, \bmcp\b, agentic (coding|engineering|software|development|programming), coding agents?

---

EDIT: We originally launched under the name Sequent. [Read why we renamed to Resolution](https://resolution.org/announcements/rebrand).

Alignment is not on track
=========================

Artificial superintelligence (ASI) may be developed in the next few years. It is unclear whether alignment is on track to be ready on the same timeframe. At a minimum, the empirical programs at AI labs are unlikely to deliver *a priori* confidence, before training ASI, that things will go well. **We are starting a large nonprofit research organization, Resolution, that aims to clear a higher bar:**

1.  **We are aiming at higher confidence** via a portfolio of theory and empirics bets, all of which could fail, such that if any succeed, they would give us more *a priori* confidence in aligned outcomes.
2.  **We are investing heavily in automation** to accelerate progress on these bets.
3.  **We believe that theory unlocks higher automation.** Taking a more principled approach offers better filters for deciding which directions of automated research are promising (a proof is worth a thousand experiments, and even a pseudo-proof is worth hundreds).

**Who**[^s6a0q4o69as]**:** researchers from the UK AISI’s Alignment Team and [Timaeus](http://timaeus.co), with more to come. We’re aiming at 40-80 FTE two years from now. The Alignment Team ran the £30m Alignment Project, and Timaeus has pioneered applying singular learning theory (SLT) to alignment. Founding team:

*   Geoffrey Irving — Chief Scientist at UK AISI; ex-DeepMind, OpenAI, and Google Brain.
*   Daniel Murfet — Head of Research at Timaeus; left tenure to pioneer SLT for alignment.
*   AISI Alignment — Alex Holness-Tofts and Jacob Pfau.
*   Timaeus — Jesse Hoogland, Stan van Wingerden, and Marco Cozzi.
*   Joined by researchers from Timaeus and more researchers from the UK AISI’s Alignment Team

**Where:** a large in-person presence in the Bay Area (Berkeley), as well as researchers working remotely from London, Melbourne, and elsewhere.

In this post, we discuss:

*   What it means to aim at higher confidence
*   Why start a new big organization
*   Whether sufficiently fast progress is possible with automated research

Aiming at higher confidence
===========================

In an ideal world, we would develop an approach to building superintelligence together with a theoretical proof that it was safe, and *then* build it. In this world, we probably have to settle well short of this ideal. However, we believe this doesn’t mean giving up on the idea of leveraging theory to get safety.

Our approach to alignment is differentiated from that of the AI labs due to our emphasis on seeking principled reasons for being confident that the alignment we observe in situations we control (for example, in training, or during evaluations in chosen environments) generalizes to alignment in situations we cannot easily control (e.g., large-scale, long-horizon tasks executed in the world). Most AI lab approaches are essentially reactive, resulting in methods that, while functional, do not yield principled insight into if or when they will fail. The “reasons” we have in mind range from a better scientific understanding of the underlying phenomena of deep learning to asymptotic guarantees of safety under specific protocols:

*   **Understanding deep learning** is an unfinished scientific project. It is worth noticing that if we had a very complete theory of how deep learning works, certain kinds of alignment problems would be trivially solved (e.g., if we could rule out certain kinds of outcomes using an understanding of the training data and optimization process). We are not aiming at a complete understanding, but we think it is important to aim at a *better* understanding. This can be turned into improvements in how alignment works at the frontier in the near term (e.g., through changes to post-training).
*   **An asymptotic guarantee** provides assurance that an AI training protocol (e.g., scalable oversight via debate) converges to a tolerably low chance of unsafe behavior, provided some parameters (e.g., training time and amount of data) are made sufficiently large. Such guarantees exist in the theory literature for some reinforcement learning algorithms, but not for neural networks or other classes of learners sufficiently powerful to plausibly reach AGI or ASI. We are not aiming to prove such guarantees for neural networks. We do however aim to prove asymptotic guarantees for alignment while *making certain assumptions* about the training process. This dovetails with an empirical effort to shift the practice of alignment as close as possible to an approach where we get confidence from these guarantees (even if the hypotheses of the theorems don’t strictly hold).

However, we do not know any attacks of either form that are highly likely to succeed individually. Our hope is to build towards that confidence by exploring many different research bets in parallel, using a single organization setting to increase both sharing and amortization of work.

Why a new big organization
==========================

There are a number of existing non-profit organizations pursuing theoretical aspects of AI alignment. However, none of these have yet succeeded in making the transition to affecting how deep learning works at frontier scale, and the challenges to doing so on short timelines (say the next 2-3 years) are immense. Automation can help, but will require significant investment in engineering and working at a scale that is hard for small non-profits. Moreover, the largest gains of automation will likely come from taking a “whole of field” approach where we integrate several deep ideas currently being developed in separated groups.

This suggests that there is an opportunity to achieve outsized gains for alignment by *bringing excellent research talent together* and *leveraging it with world-class engineering talent via automation*. We believe the best way to realize this opportunity is to found a new organization.

AI labs also couple research and engineering excellence, but their empirical strategy leaves promising routes to alignment on the table. This is most true for theoretical ideas and for new empirical approaches based in theory. We see a strong opportunity to attract world-class theorists for at least two reasons:

*   **No large theory organizations exist:** There are currently no large organizations in AI alignment with a theory focus (although other excellent institutions like ARC and Simplex are also scaling up!)
*   **Scientific reputation:** Our initial senior scientific leadership has strong reputations for leading such work. Irving played an important early role in establishing today’s primary alignment technique (RLHF) at OpenAI and DeepMind, led teams building the first LLMs at DeepMind and has made multiple theoretical contributions including to scalable oversight via debate. Murfet left tenure in pure mathematics to direct research at Timaeus, one of the few research agendas in alignment to connect pure theory to practical applications at billion-parameter scale.

Different lines of research will interact
-----------------------------------------

A core reason we are establishing a single organization tackling a portfolio of bets is that we expect different areas of research to interact and mix. Science progresses fastest by high-bandwidth interaction between very talented researchers: people with the right combination of taste, context, and ambition, in the same building, talking regularly. Combining helps on two counts: it surfaces interactions between research areas that are otherwise easy to miss, and it concentrates the small number of people best placed to do this work in one place.

Our experience working together between AISI Alignment and Timaeus is a key motivating example, and is one of the driving factors behind our joining forces. Timaeus’s singular learning theory and empirical work provides one route to understanding the dynamics behind neural network learning and generalization, but cannot itself provide the full picture: it might give us the knobs (when to intervene to best influence model behavior) but not the settings for those knobs (what that behavior should be). Scalable oversight can provide training signal as models ramp upwards to superintelligence, but faces obstacles unless we understand the relationship between heuristics the models are likely to learn or not learn. More time together with tight feedback loops will help us map these complements faster!

There are other complements! We are excited about many areas of alignment theory and associated empirics, and plan to both build out our in-house portfolio and collaborate with sister orgs with additional theory bets. Some areas we are excited about sharing between, internally and externally:

*   **Scalable oversight**: complexity theory + empirics of amplification, debate, scientist AI
*   **Learning theory**: singular learning theory, other deep learning theory, computational mechanics
*   **Heuristic arguments**: mechanistic understanding of what models know, low-probability estimation
*   **Game theory**: mechanism design, agent foundations, open-source game theory
*   **Personas**: theory and empirics of low-dimensional structure within model behavior, across training and token dimensions

Example interactions coupling between multiple of these areas include:

*   **Reachable equilibria:** Learning theory and game theory can tell us what types of equilibria scalable oversight methods will converge to. A method like debate is useless if game-theoretic equilibria are safe but cannot be reached by practical training.
*   **Knowing and setting knobs:** As above, learning theory and personas can show us the key knobs during training, including what periods of training and dimensions of variation are most critical. Scalable oversight can then say how to spend resources to know how to set those knobs.
*   **One area setting problems for another to solve:** Heuristic arguments research has been spinning out complexity theory conjectures, which may be resolvable by people or methods from other areas of complexity theory.
*   **Prosaic impact from ambitious agendas:** Some sophisticated alignment agendas (for example, in agent foundations or heuristic arguments) are framed around long-horizon goals. We expect some of the deep ideas in these agendas can be applied more prosaically on top of existing LLM approaches and be hybridized with scalable oversight or other RL approaches during adoption.

These have the form of using partial success in one area to fill a gap left by partial success in another. When we find this kind of gap-filling strategy, sufficient success in either area becomes easier to achieve. The frequency of these interactions is important! If we share ideas every 6 months between different orgs working on different bets, and superintelligence arrives in a few years, we get very few cycles.

Amortizing security and funding
-------------------------------

More crassly, a larger organization provides a larger single target for funding and the ability to amortize security across different research bets. Both of these are critical to high automation:

1.  **Good security may be required for frontier model access:** We are entering a period where some models at the absolute frontier will not be widely available for significant periods after development. Even where the incentives of AI labs and independent research align, AI labs may be unwilling to share such models with independent orgs without significant investment in security, or even entirely unable to share if the AI lab is not the sole decision maker in who gets access.
2.  **Most expected impact comes from high success at automation, which means lots of tokens:** Our goal is to raise $100-150M initially, but prepare to raise at least one order of magnitude more if we can demonstrate successful exploration of many parallel research investigations. We expect it to be easier to raise these funds as a single large organization than a portfolio of smaller orgs.

Automated alignment is possible, if not necessarily in time
===========================================================

If AGI is possible, then automated alignment research is possible, by definition, though not necessarily before the AIs become misaligned. The question is how to get as much alignment progress from AIs as early as possible in the trajectory from where we are today, to AGI and then ASI. Key to that is knowing the difference between *apparent* progress and *real* progress.

Two markers suggest that automated alignment research may now be possible. Firstly, since late 2025, we have seen rapid improvement in coding agents, so automated experimentation is now feasible. Secondly, in recent months, we have seen progress in mathematical research being performed by frontier models; the recent settling in the negative of the Erdős unit distance conjecture is a dramatic example. A bet on automated research coupling theory and empirics now seems opportune.

However, research takes more than proving clearly stated theorems and running well-specified experiments. It takes judgment to know which theorems to prove (counterintuitively, the hardest part of mathematics may be choosing good definitions!) and which experiments to perform. At present, this tacit knowledge is acquired by humans through long experience and intensive mentorship. To believe in AGI is necessarily to believe that machines can also acquire this tacit knowledge. However, right now, they certainly do not possess it to the same degree as the best human researchers.

The near-term challenge for automated alignment research is therefore to

1.  **Leverage frontier models** to do (informal) mathematics at a high level and run experiments, while
2.  **Building error-correction** into the system so that this all amounts to real forward progress

This is itself a hard research problem! It is a problem that the new organization is dedicated to solving, as an instrumental goal to progressing the state of alignment towards higher confidence. Part of the solution is to organize ourselves around leveraging the research taste of humans, and to take advantage of the epistemic structure that theory offers to science.

1.  **Leveraging research taste**. As an analogy, consider that in some fields of science we reward early career success by putting some professors in charge of larger labs, thereby leveraging their research taste to achieve faster rates of scientific progress. This is a skill of meta-research taste consisting of recognizing and promoting those with good research taste. It is unclear how to deliberately transfer this from humans to models, but we can at least be purposeful about collecting human experts, exposing them to many opportunities to exercise research (and meta-research) taste in order to achieve the same kind of speedups as we believe occur in the human sciences, and gathering data so that models climb up to higher levels of taste themselves.
2.  **Taking advantage of theory and empirics together**. A prototypical scientific “discovery loop” involves building theory to explain experiments, making predictions with that theory, and then testing them in further experiments. For purposes of automation, the abstract gain here is that iterating between theory and empirics means two different types of filters with which to screen out false progress, which means more success and more parallelism from humans working with models. To emphasize, since our theories and proofs will be toy, even a formal proof will never correspond to full confidence that could not be strengthened with an additional empirical test.

A lot of this work will be mundane! Skills and prompts for Codex and Claude Code, MCP tools for a model to check its work against a model from another family, good engineering practices for unit and A/B tests, and workflows that best take advantage of human and AI strengths. We expect to start with automation shaped more like conventional agentic coding than the recent Erdős problem successes: the latter was full automation developed interactively and then run autonomously on a large set of well-defined problems, the former involves iteration between humans and machines gradually building up a large object.

However, even with additional structure provided by theory, **we are not confident that automation will work in time**, even if the AIs involved are not scheming. LLMs make mistakes, and any work that leans on research taste as a guide will mean some mistakes are very hard to catch. Bowkis et al., [*Automated alignment is harder than you think*](https://arxiv.org/abs/2605.06390), discuss some of these worries in detail, and we will be exploring and elaborating more details of how automation could fail in parallel with trying to make it work. Obstacles to automation are another reason to put a portfolio of alignment bets in the same organization: an obstacle noticed in one area may have gone unnoticed in others, and can be addressed broadly.

Federated structure to preserve research diversity
==================================================

To preserve what makes small alignment teams succeed — research focus, opinionated leadership, distinct cultures, low coordination overhead — Resolution will have a federated research structure. A handful of research directors will have substantial autonomy over research direction, team culture, and hiring in their research areas. These directors will report up to Geoffrey Irving.

Initially, we will be aiming to set up research divisions to cover a subset of the areas listed in the previous section. We would like to emphasize that **our set of research areas is not fixed:** the final portfolio will depend on the research directors that join us.

**If you have a promising research area that we have missed, please reach out!** The goal for Resolution is to be a home for many different approaches to alignment, sharing the common principles of aiming at higher confidence and taking advantage of automation.

Field building and broader alignment scale-up
=============================================

Alignment is a civilizational challenge and requires progress on many fronts. Some problems are best tackled from within the AI labs by those with close access to frontier models. Others are best tackled from academia or by other non-profit or for-profit organizations. In the near term, we expect many existing alignment research organizations to scale up and new ones to be founded. In particular, we believe there is a productive role in this ecosystem for a new large organization, with a focus on theory and automation.

However, we acknowledge that at present one of the bottlenecks to deploying funding is the shortage of experienced researchers to be part of founding teams. We may contribute to this shortage by attempting to recruit the same people. We expect to hire experienced researchers across a range of seniority, but do not currently plan to recruit or develop those still early enough in their research careers to need substantial mentorship; we may therefore inadvertently have a negative impact on opportunities for this cohort. This effect would be unwelcome: **in an era of successful research automation, the value of novel ideas and new research directions is high**. In science, it has historically been the case that healthy fields have strong cross-generational interactions that maintain a high production rate of such ideas. We are interested in ideas for how the field overall can (a) create opportunities (e.g., postdoc-like positions) for younger researchers with their own agendas and (b) how we should interact with them.

We are talking to a number of organizations working on alignment theory focused more on field building and human researcher scaleup (not all announced!), and we believe that solid sibling relationships between organizations are part of mitigating this worry. Although we will focus on in-house research, our default will be to publish openly and at a fast pace, subject to dual-use review; this makes cross-org collaborations more fruitful. Where possible, we hope to share automation infrastructure with sibling organizations as well, though how this interacts with security for purposes of full-frontier model access is unclear.

Our hope is that formal relationships between different organizations can also mitigate the large-org funding advantage as well: we may explore regranting activities in the future and until then will be strongly advocating for smaller orgs with funders and for smaller orgs to further scale.

Independence is important
=========================

A natural alternative to establishing Resolution as a new organization would be to join an existing AI lab and add to the alignment push from the inside. This removes several challenges (such as access to models, security, and visibility into training tracks). We have chosen to stay independent for at least two reasons:

1.  **We might need to yell:** Our research goals will be a mixture of trying for success and trying to exhibit empirical and theoretical obstacles that demonstrate that alignment is difficult. We will hope for success; if we find only obstacles, it is easier to be loud from the outside.
2.  **Avoiding the pull to uniformity:** We believe that most safety research at AI labs has collapsed into too few total bets, most of which are purely empirical. It may be possible to join a lab with the promise of pursuing alternate approaches, but it can be difficult to escape the draw towards urgent pre-ASI safety work. This is a concern within our organization as well: we will attempt to mitigate this by embedding the portfolio model of research into the culture at the start, and by supporting and collaborating with other independent orgs.

That said, we believe there will be many cases where incentives will align between our work and alignment research at AI labs. We are excited to collaborate, both on specific projects and on the general task of uplifting models at theoretical and empirical alignment bets not represented within the companies.

Join us!
========

[We’re hiring](https://resolution.org/careers) across research, engineering, operations, and security.

[^s6a0q4o69as]: The author order of this post is alphabetical following https://www.cs.princeton.edu/~appel/papers/science.pdf, except that Geoffrey is first this time because a non-established account would require a lengthy screen to first author.