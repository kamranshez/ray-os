# Your software should build itself

- URL: https://www.lesswrong.com/posts/CeRHyeot37KoqDqHC/your-software-should-build-itself
- Author: Max von Hippel
- Date: 2026-07-25
- Karma: 9  Comments: 1  Words: 2207
- Band: A  Tier: 1  Score: 72.0  Density: 15.78
- Anchors: sub-?agents?, \bharness(es|ing)?\b, claude code, \bcodex\b, coding agents?

---

![A cathedral building itself, with antiquated-looking robotics, drawn in the style of David Macaulay. Generated using Nano-Banana 2 Lite.](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/CeRHyeot37KoqDqHC/7d5e589340a2db379de4c8423b36ef80595e5d455816b5cd1832a77a5d31b7f9/zqakvkktaeunt3scsly5)

I’ve recently decided that the distinction between the *agent* which builds your software and the *software it builds* is nonsensical and antiquated. In the future, software will build itself, and this means the agent is part of the very fabric of the software it’s building. To make this idea more formal, I propose two (I believe, novel) ideas:

1.  Your agent should live inside the type system of the language it’s programming in.
2.  Your agent should *own* (be able to edit)  the language it’s programming in.

I will refer to a system which satisfies both attributes as an Auto-Syntactic Model (ASM).

The traditional distinction between a model and an agent is that a model is a single-step function that maps from text to text, while an agent is a model, with tool-use, in a while loop.[^1zg7nm0a7u3] In an ASM, the agent writes code in a programming language, L, the syntax of which is defined locally (for example, using Racket). The agent has a *modify* tool by which it can modify L directly. Moreover, the agent does not exist as a piece of code distinct from the syntax and semantics of L; when it modifies L it is modifying its own harness. This is because the agent is implemented directly within the type system of its own language.

ASMs, I believe, solve several very significant problems with current SOTA programming agents. I enumerate these problems and explain why they necessitate ideas 1 and/or 2 in the next section, titled, *Your agent sucks.* Then, in the subsequent section, *PL Supremacy*, I enumerate a few compelling examples of really cool things you can do using ideas 1 and 2. After this I explore two interesting tangents. First, *Tangent 1: AI Safety*, explores how this new approach to agent architecture could allow for new and interesting AI safety mechanisms by way of formal methods. The second, *Tangent 2: My Mediocre Prototype*, briefly describes a very, very minimal prototype which I vibe-coded over the weekend using Fable. Finally, I conclude in *Conclusion*.

***Note:*** *This is ongoing research, and as such, some ideas are still somewhat hand-wavy. This blog post is entirely the product of my own dumb human brain. I hope you'll tolerate the hand-wavyness, and I look forward to criticism/comments which can help crystalize my idea.*

Your agent sucks
================

Current SOTA programming agents (such as [Claude Code](https://claude.com/product/claude-code?), [Codex](https://chatgpt.com/codex/enterprise/?utm_source=google&utm_medium=paid_search&utm_campaign=GOOG_X_SEM_GBR_Codex_CDX_BAU_ACQ_PER_MIX_ALL_NAMER_US_EN_111325&c_id=23226110534&c_agid=194939268903&c_crid=807810285015&c_kwid=kwd-111182835&c_ims=&c_pms=1013920&c_nw=g&c_dvc=c&gad_source=1&gad_campaignid=23226110534&gbraid=0AAAAA-I0E5eoTWh5hXaZ7K0XuY6u7hibQ&gclid=EAIaIQobChMI8Z_p6q7OlQMV60lHAR3blgvbEAAYASAAEgI7NvD_BwE), and lesser known ones like [Slate](https://randomlabs.ai/)) have several extremely significant disadvantages. AI enthusiasts tend to deny these disadvantages or say they’re vanishing as models improve. There is, of course, an endgame where models achieve superintelligence and start outputting completely perfect machine code at scale, and maybe kill us all, and in this scenario the AI enthusiasts I allude to are correct that the problems discussed in this blog post are rather moot, but until then, they are wrong. Ok, I’ll cut to the chase and start enumerating problems now.

Edits
-----

Models are not good at editing code. This is most visible with small, crappy models like [mistral-small](https://mistral.ai/news/mistral-small-4/) or [gpt-oss](https://openai.com/index/introducing-gpt-oss/), but even frontier models like [Opus 4.8](https://www.anthropic.com/news/claude-opus-4-8) routinely struggle to edit software. In fact, this problem is so big that it’s led to an entire industry of *fast-apply* models such as [Relace](https://docs.relace.ai/docs/instant-apply/quickstart) and [Morph](https://www.morphllm.com/products/fastapply).[^eyyvoaru6r] It’s definitely possible to refactor your code to reduce this problem, for example by using languages that are easier to edit in (i.e. languages with less-strict syntactic requirements) or by refactoring code-files to be shorter, but heuristic band-aids don’t make for a *solution*.

I claim that Edits are fully solved if the agent lives in the type system. It can simply assign unique tags to typed objects, and then index into an object by its tag (some short uuid) and edit it directly. This allows for significant context scoping when compared to full-file edits, the current status quo.

Note, this is one possible solution; I imagine a powerful ASM may invent better ones.

Search
------

Models are pretty bad at search. This problem does seem to be lessening with time, but only because we’re willing to burn more tokens with subagents. There has not, as far as I’m aware, been any kind of meaningful breakthrough on how to really put an entire codebase in the context window.[^wuyla0kyko9]

I think that Search is beautifully solved sub-agentically by embedding the agent into the type system; rather than using the file-system as the roadway for Search, the software root simply asks each of its children what it knows about the given query, and so forth, and information bubbles up through the code’s inherent structure. In particular, if the agent can modify the programming language L, then “the code’s inherent structure” is an evolving thing. The agent can do things such as, demand that functions have certain kinds of type signatures or docstrings, or force every module to succinctly describe the functionality it exports, or require layered specification [refinements](https://en.wikipedia.org/wiki/Refinement_\(computing\)) in each software module making it easy to understand what the module accomplishes at any level of fidelity[^e5cawecfbrt].

Ironically, this means a shift away from the file-system as metaphor, re-igniting the early-2024-era debates over file-systems versus databases for coding agents[^64digj1jfip]. I basically think that debate was just a little ahead of its time.

Slop
----

Next-token prediction inherently leads to slop, as a kind of exploratory failure. For example, even frontier models often produce Python code with unused imports, or mid-file imports. This is because imports are a form of latent planning. You can completely solve this problem by having the model generate the code first, without imports, and then the imports block second.[^tpvas3phnt9]

Slop comes in many flavors. Functions that don’t need to exist, mid-file imports, [poor adherence to common design principles](https://www.ycombinator.com/library/NL-common-mistakes-with-vibe-coded-websites), and so forth. Slop also relates to Search in the sense that duplicative code wouldn’t exist if the model was always aware of all the code in the codebase. Slop is reducing as models improve but it’s pretty fundamental to next-token prediction so I don’t think it can be fully ameliorated by model improvements pre-ASI. A good example of this would be how Fable, despite being widely lauded by the twitteratti, is still a pretty mediocre writer.

Slop can be solved by embedding all the stuff that’s tricky about planning into the programming language itself. I just (two paragraphs above) gave a great example of this, but many other examples come to mind, such as using refinement to iteratively and subagentically plan out complex software implementations, or (for the love of God, *finally*) building a unified type system connecting backend, wire, and frontend, so that when I update a struct in my backend, I don’t need to go chase down the corresponding proto and frontend Pydantic class, or whatever.

PL Supremacy
============

This section consists of a short list of cool things you can do when your agent lives in and controls its own programming language. The idea of the ASM is to have a structured way for AI to explore and build upon ideas such as, but in no way limited to, these. The section is meant to help clarify what I’m aiming to build and convince you that my ideas are exciting, hip, and cool.

*Complain*. Anytime you ask a model to perform a task with some given data and tools, you should give it a *complain* primitive which allows it to complain that, in fact, it does not have the necessary information or tools to complete the given task.[^mlmak50xgxh] If you adhere to idea 2 (the agent can modify its own programming language), then the agent can run a benchmark, and then assess the results in light of the qualitative data left from Complaints, then modify its own language and re-run accordingly, hillclimbing to a solution that reliably solves every problem it faces.

*Query.* If every object in your language can be queried, and can query other objects, you now have a language-guided search mechanism. Caching can be accomplished with idea 2: the agent will observe the kinds of queries it’s performing most often, and naturally modify its own language to cache relevant information in the objects of the code accordingly.

*Prompt.* You should be able to prompt any object in your codebase to modify itself. Visually, this would be like using inspect-element to grab an object in the DOM and then telling it, “make yourself blue and add a slider”. A similar concept can occur for backend code, indexing into objects by tag (uuid) and telling them to modify themselves. This allows for in-context type-checking, so the agent can loop on the modification, considering only the result of the type-checker in the context of the modification itself, until the modification passes. So it’s quite a bit more token-efficient than just editing code directly.

*Index.* I’ve mentioned this quite a bit already, but every object in your codebase can have a tag (uuid), so if you want to edit lines of code 411-938, you grab the relevant covering object by its tag and prompt it accordingly. This completely solves the problem of Edits.

*Crosstalk.* There may be contexts in which it’s advantageous for components of a codebase to actually communicate with one another, so your codebase becomes not just self-constructing, but in fact a distributed system. For example, perhaps different ASMs with different capabilities and permission levels collaborate on a project, and need to share information.

Ideally, your agent is modifying its own language as it works, thinking of and adding and refining ideas like those listed above, as well as modifying the basic syntax and semantics (for example, putting imports after code as previously mentioned), as it hillclimbs toward perfectly executing the user’s codegen task.

Tangent 1: AI safety
====================

I think that ASMs have several possible AI safety implications. First, if you have a safety mechanism for your agent, you can embed it in the language-evolution step. For example, you could force the agent to prove that any modification it proposes to its language is safety-preserving for some definition of safety[^fiqt5mi6trn], à la [GSAI](https://arxiv.org/abs/2405.06624). Second, if your agent lives in your type system, it can also take responsibility for proving types when the proof isn’t decidable. This means you can extend your type system to arbitrary predicates, as is the case in [ACL2s](https://www.sciencedirect.com/science/article/pii/S1571066107001661)[^3yox53zjbwg], allowing for the expression of complex safety requirements directly in the codebase itself. I think that as proofs get cheaper and cheaper, this kind of engineering, where your compiler requires evidence which cannot be reliably conjured, will become more and more common.

If these kinds of things interest you, please get in touch! I am deeply involved in a number of related initiatives in [scalable formal oversight](https://www.lesswrong.com/posts/SfhFh9Hfm6JYvzbby/the-scalable-formal-oversight-research-program)/[secure program synthesis](https://www.lesswrong.com/posts/8wtrLoDPyCfMLuHkt/how-to-solve-secure-program-synthesis), such as a [hackathon](https://apartresearch.com/sprints/secure-program-synthesis-hackathon-2026-05-22-to-2026-05-24) and [fellowship](https://apartresearch.com/fellowships/the-secure-program-synthesis-fellowship) through Apart, an ARIA-funded [benchmark](https://arxiv.org/abs/2606.01008) with [Galois](https://galois.com/) and [Forall R&D](https://for-all.dev/), and various ongoing research projects.

Tangent 2: My mediocre prototype
================================

I’ve been vibe-coding a mediocre prototype using Fable, available [here](https://github.com/maxvonhippel/agentcode). I am only a few hours into it. The idea of the demo is to show how you can build a Lovable-style product where the frontend, in essence, builds itself. Currently I just have a small fragment of HTML working, and I have not yet built out any kind of benchmark-based evolution. I’ve implemented the first requirement (the agent lives inside the type system) but am not yet done with the second (the agent is self-editing). Obviously, the end-goal for a project like this is to have the demo itself be self-building, but that will require more work.

Conclusion
==========

When the [RLM paper](https://alexzhang13.github.io/blog/2025/rlm/) dropped, it showed us that “model in a loop with accumulating context” is not the only possible paradigm for agents. I immediately realized that there must be interesting, alternative agent architectures informed by the type system encoding the task the agent is performing, and I alluded to this in both of my above-linked LW posts. But I didn’t know what it should look like, or how to do it. I still don’t think I *really* know “the answer”, but I believe the vision I’ve outlined here probably rhymes with what’s next.

At this point it’s trite to observe that AI has something to say about FM (see: [Harmonic](https://harmonic.fun/), [Axiom](https://axiommath.ai/), [Theorem](https://theorem.dev/), [Math Inc](https://math.inc/), [Sigil Logic](https://sigillogic.com/), [Atalanta](https://www.atalanta.tech/), [Sequent](https://www.sequentlabs.ai/), [Architect Labs](https://architectlabs.com/), [etc](https://fmxai.org/map/).). But I also think FM and PL have something very significant to say about AI. Many of the problems with current AI systems are exactly corollary to the things that formal approaches excel at. Thus, I think that AI researchers should be thinking seriously about how they can leverage the affordances of programming language design and formal methods to enhance, safeguard, and control their AI systems. I hope the argument I’ve laid out in this post convinces you of this, and orients you toward a nonobvious, but at least partially correct, notion of how it should be done.

**Acknowledgments.** I would like to thank Herbie Bradley, Quinn Dougherty, Simon Henniger, Ferenc Huszar, GasStationManager, Jacob Denbaux, and several others for constructive feedback, edits, and general conversation during the writing of this post.

  

[^1zg7nm0a7u3]: This distinction has begun to break down with the renewed focus on thinking, or “test-time compute”. In particular, when you begin training models specifically to think long and hard, and to operate within certain kinds of harnesses, the distinction between model and harness becomes a little nonsensical. For example, a Recursive Language Model (RLM) is essentially an agent where rather than accumulating in messages[], context accumulates in an external document, over which the agent may search via tool-use. 

[^eyyvoaru6r]: If you’re deciding between these two products, Relace is the better one, in my opinion. But as I outline in this article, I also just don’t really think the product category should exist in the future. 

[^wuyla0kyko9]: Correct me in the comments! But please, if you do so, explain why whatever innovation you’re excited about has not, yet, qualitatively improved my experience with Claude Code etc. 

[^e5cawecfbrt]: Mike Dodds and Reasonable and Sigil are all working on ideas that rhyme with the refinement stuff I outlined, but they’re not yet trying to do my ideas 1 or 2. 

[^64digj1jfip]: This was a very active topic of discussion when I did YC in S24. Amusingly, it seems to have only hit the blogosphere recently (see: example, example, example, example). I know we all like to make fun of YC for producing some truly idiotic startups, but it really is true that the YC zeitgeist is often about two years ahead of industry, which is a very real advantage and leads to significant financial outcomes! Something similar could probably be said for the LessWrong community, albeit along slightly different dimensions. 

[^tpvas3phnt9]: Cyrus of The Synthesis Company taught me this in Summer 2024 and blew my fucking mind. It’s so completely obvious, once you see it, and it so clearly implies that PL design is fundamental to improving AI outputs! I’ve been absolutely baffled ever since at the complete dearth of serious efforts to build truly AI-native programming languages. Why isn’t this, like, the dominant topic at POPL? Am I crazy? 

[^mlmak50xgxh]: I got this idea from a really cool Bookface post which I am now unable to find. 

[^fiqt5mi6trn]: I can imagine a wide variety of useful properties to preserve, such as certain kinds of memory safety, or constant-time computation in a cryptographic context, or timing requirements for real-time OSs, or certain kinds of auditability for data-processing languages. 

[^3yox53zjbwg]: The greatest language ever designed. Also one of the least popular.