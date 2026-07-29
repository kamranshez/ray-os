# What's Continual Learning, and Why Might We Expect To See It In Advanced LLM Agents?

- URL: https://www.lesswrong.com/posts/5mCJzimtNZc9o4e26/what-s-continual-learning-and-why-might-we-expect-to-see-it
- Author: RohanS
- Date: 2026-06-12
- Karma: 32  Comments: 2  Words: 5177
- Band: A  Tier: 1  Score: 91.1  Density: 21.41
- Anchors: scaffold(ing|s|ed)?, claude code, \bcursor\b, claude\.md, \bmcp\b, coding agents?, sub-?agents?, context engineering

---

*This is the second post in the sequence* [*Implications of Continual Learning for LLM Agents*](https://www.lesswrong.com/s/oc5Auteiibo56kNXw).

Summary
=======

We say that an agent is a **continual learner** if it undergoes persistent updates during deployment. That’s more-or-less a binary criterion, but there are several other components to being *good* at continual learning that are much more continuous. We say an agent is an **effective** continual learner to the extent that it:

1.  Constantly undergoes persistent updates during deployment,
2.  Learns new useful knowledge and capabilities efficiently via those updates, and
3.  Does not (catastrophically) forget existing capabilities in the process.

CL lies on a spectrum, major capability advances may not require CL breakthroughs, and early forms already exist (e.g., agentic RAG, CLAUDE.md, SKILL.md, and personalization prompts).

**The basic reason to expect effective CL is that it would probably make AI agents better at important tasks on which AI companies are trying to improve performance, most notably AI research itself.** So far, nothing has allowed LLM agents to become as good at end-to-end research as capable humans become after years of practice, despite the fact that LLM agents collectively accumulate research experience much faster than individual humans. This argument applies to most open-ended remote labor jobs. CL is also closely tied to sample efficiency on long-horizon and hard-to-verify tasks.

**The main components of an LLM agent that can receive persistent updates during deployment are model weights, the context window, memory banks with natural language or neural activation memories, the agent scaffold, and tools.** We expect different update mechanisms will suit different types of CL, so a mixture is likely. Weight updates are probably needed for some parts of effective CL since LLMs seem quite bad at handling lots of interrelated complexity in their context window. But naïve weight updates often degrade existing capabilities, which is why frontier systems haven't widely adopted them yet.

Constantly implementing better and better LLM agent post-deployment update mechanisms is a significant subset of AI R&D, so automating AI R&D very likely involves enabling strong self-designed and self-directed CL. *Meta continual learning* will be a very real thing: LLM agents will learn from experience how to improve LLM agents' ability to learn from experience. Early attempts already exist ([Absolute Zero](https://arxiv.org/abs/2505.03335), [SICA](https://arxiv.org/abs/2504.15228)), and this could be an important part of recursive self-improvement.

* * *

Why might we expect to see continual learning?
==============================================

**The basic reason to expect effective continual learning (CL) is that it would probably make AI agents better at important tasks on which AI companies are trying to improve performance.** Agents like Claude Code already attempt many of these tasks during deployment, most notably AI research itself. Humans who read and write lots of AI research proposals, code, critiques, summaries, and papers often learn from their experiences and become better researchers over time, and learning AI research skills efficiently from experience would make LLM agents much more useful.

**However, current AI agents do not learn from experience as effectively as humans.** Persistent updates for individual human users via things like personalization prompts, CLAUDE.md files, and skill files can be powerful, but are still fairly limited. At least, it seems like no one has yet managed to utilize these forms of CL to create AI systems that fully automate any major component of the AI research process (where major components include writing research proposals, code, and papers). These updates are also not shared across human users by default. Weight updates, e.g., fine-tuning on a collection of new experiences, do not happen automatically in frontier systems like Claude Code and Cursor. There are efforts to enable continual weight-updating, but we’re not aware of any examples that handle the issues of *how to turn deployment trajectories into useful training examples* and *how to avoid degrading existing general capabilities* well enough to constitute effective continual learning.

**How do humans continually learn, and why can’t LLMs learn the same way?** Let’s stick to the same domain of AI research for now, since it’s the highest priority for AI companies. The following [advice that Neel Nanda wrote to help junior (human) researchers cultivate research taste](https://www.lesswrong.com/s/5GT3yoYM9gRmMEKqL/p/Ldrss6o3tiKT6NdMm#Cultivating_Research_Taste) is useful to many humans, but isn’t easily applicable to LLM agents:

**Learning more from each data point**: You will learn something just from doing research. You'll get some feedback, some experience, and your intuitions and models will improve. But each data point is actually much richer than just a binary of success or failure!

*   My recommendation is to **make explicit predictions, review accuracy**, and make time to **reflect on what you missed** and how you could do better next time.
    *   Keep a research log. Ask *why* things worked or failed. Was it luck, execution, or a fundamental judgment call (taste)?
*   **Reflect Deliberately**: After an experiment or project phase, ask: What worked? What didn't? What surprised me? What would I do differently next time? How does this update my model of this domain? ([Weekly reviews](https://www.neelnanda.io/blog/39-reflection) can be great for this.)

**This advice relies on aspects of learning that we take for granted as humans, but that have no easy analog in LLM agents to date.** You can prompt LLM agents to make explicit predictions, review accuracy, keep a research log, and reflect deliberately on each project phase, and there are various existing attempts to update their weights, contexts, memory banks, scaffolds, and tools to make them better. Some of these are somewhat effective. But **getting LLM agents to consistently identify and especially internalize key insights is a hard, unsolved problem**. So far, nothing has allowed LLM agents to become as good at end-to-end research as capable humans, despite the fact that LLM agents collectively accumulate research experience *much* faster than individual humans.

AI research is a particularly important example, but **this argument applies to most open-ended remote labor jobs**: there are a lot of things you can learn from each experience, humans sometimes leverage more of those lessons to learn more quickly than LLM agents, and LLM agents have enough experiences collectively that learning from them consistently could radically improve their real-world capabilities.

So, what exactly is continual learning?
=======================================

We say that an agent is a **continual learner** if it undergoes persistent updates during deployment. That’s more-or-less a binary criterion, but there are several other components to being *good* at continual learning that are much more continuous. We say an agent is an **effective** continual learner to the extent that it:

1.  Constantly undergoes persistent updates during deployment,
2.  Learns new useful knowledge and capabilities efficiently via those updates, and
3.  Does not (catastrophically) forget existing capabilities in the process.

Updates can be to weights, contexts, memory banks, scaffolds, or tools, and perhaps future AI developments will create additional surfaces that can be updated. We’ll dive deeper into update mechanisms below.

**Why this definition?**

The goal of our informal definition is to remain faithful to common usage of the phrase “continual learning” and to pick out a type of learning that largely doesn’t exist yet in LLM agents, but which we think could arise soon and would have major implications for capabilities and safety.

The story above of how humans learn AI research differently from LLM agents illustrates a few points from the definition: Neel Nanda’s advice can help with increasing **sample-efficiency,** updates need to be **persistent** in order to make agents better at AI research in the long-term, AI research is a particularly **useful new capability**, and most of the AI research work that LLMs do happens **during deployment** (whether internal or external).

Ongoing learning **during deployment** is the most central feature of CL, and is important from a safety perspective because many safety interventions are conducted and evaluated after capabilities training and prior to deployment. It seems significantly more difficult to build confidence that every deployed version of an agent is safe if the agent is constantly evolving and safety interventions and evaluations can only be done once in a while. (We’ll discuss the safety effects of CL in greater depth in the next post.)

**Useful knowledge** that an AI system might gain from CL includes facts about its environment (e.g., the company codebase it’s working in, or the world in general). For example, an LLM doing AI research might come across a particularly good, niche survey paper on a topic that is presented by a user, and acquiring persistent knowledge of this paper’s existence and contents can help this agent (and other instances) perform better than they would if they forgot about it as soon as the sessions end.[^tp5wanbyng]

**Persistence** is on a spectrum, in that lessons from past experiences only need to be remembered long enough to be **useful**. For instance, if future LLM agents can maintain long enough contexts to do effective in-context learning for very long-horizon tasks (e.g., tasks that take humans multiple months), that is persistent enough to matter even if the session eventually gets erased and the insights learned in-context are never baked into model weights.

We mention **catastrophic forgetting** separately from **persistence** to highlight the difference between *reverting* past updates (e.g., starting a model instance with a fresh context) and *overwriting* past updates (e.g., doing weight updates that break an existing capability). We use “persistent” to mean non-reverting and “forgetting” to mean overwriting.

Human learning is continual in another way: we **constantly** “update” on every experience we have as we have it. Learning seems more continual if a larger fraction of all experiences induce updates and if there are frequent updates on small batches of experiences (rather than infrequent updates on large batches of experiences).[^eqxlqk0qj2v]

Humans engage in continual learning (CL) all the time, so there’s a wide array of examples that can help build intuition. The level of deliberation and self-directedness involved in CL can vary. We include several examples across both of these axes in the dropdown below.

+++ Intuitive examples of human continual learning

One great way to learn efficiently is to **reflect on successes and failures:** People sometimes reflect on achievements they're proud of and the behaviors that led to them, then make note to repeat those behaviors in similar situations. Similarly, they might notice errors and correct them.

1.  "Working on my side project for an hour every day last month allowed me to do a project I enjoyed and feel proud of. Let me edit my weekly review template to make sure I commit to a 'daily hour' project each week going forward."
2.  "I've been super unproductive at home the last few evenings, even though I meant to work. I'll stay later at the office, where I’m productive, so I don’t need to be productive at home."
3.  “I haven’t made any close new friends since moving here. How did I become close friends with people before? \[Think of specific friendships.\] A common feature is that I had opportunities to automatically see them regularly; yeah, that makes sense and is a well-known key factor. Let me set up or join recurring events, like dinners, with some of the people I’ve liked here so far.”
4.  “My manager said the code I wrote was too bloated. I’m not sure exactly why that happened, but I’ll keep it in mind for the future; I think I can at least notice if that’s at risk of happening, and next time I notice that, I can try to explore creative ways of doing better.”

Reflection on success and failure can allow people to establish Trigger-Action Plans. “[**Trigger-Action Plans (TAPs)**](https://www.lesswrong.com/posts/ESnzpoCJrAfwAzpMB/hammertime-day-3-taps) are the if-then statements of the brain. Installing a single TAP properly will convert a *single* intention into *repeated* action.” E.g., “If I’m exiting a door that locks, I’ll hold the door open until I’ve checked that I have the key.”; the *trigger* implies there is an opportunity to make success more likely and failure less likely, and the *action* was *planned* in order to do that.

Reflection is very deliberate, but **some vital forms of CL are less deliberate**. Acquiring **muscle memory** is a good example.  When one first learns to play a sport, use a video game controller, chop vegetables, or use keyboard shortcuts, they must think through each motion and execute it deliberately. Later, they can do it naturally and quickly, chaining many quick motions together without conscious thought.

Since young children usually lack the ability to deliberate very deeply, they are a good source of examples of intuitive (non-deliberate) learning. Consider **social learning**: children often learn behavior from interacting with others. They learn how loud they should be in various settings: toddlers will scream anywhere, but 10-year-olds are usually pretty unobtrusive. This could happen either through imitation or through reinforcement from parents (“use your inside voice!”), but it seems unlikely that it happens through logical deliberation.

Importantly, non-deliberate learning plays a major role in developing cognitive skills, including many professionally-relevant skills. Consider a programmer who tries to write code to achieve a task, fails with one approach, finds that frustrating, then tries different approaches until, to their relief, one works. Then, in the future, they are more likely to go directly to the approach that worked. This can be learned consciously, but it can also be learned subconsciously; the role of the emotions mentioned here (frustration and relief) is to show that they can produce similar instinctive learning to the child feeling embarrassment when their parents scold them and say “use your inside voice!”. These learned cognitive skills can be crystallized, compressed, and composed to enable more complex skill development over time.

We touched on **imitation** with social learning above, but we can zoom in further. Many people who are good at their jobs spent significant time working with someone more experienced and learned to imitate some of their workflow and best practices without having to work them out from first principles. Consider family-owned businesses passing from parents to children, and research mentors teaching research taste and tools to mentees (who then mimic their mentors’ advice when advising their own mentees). This isn’t limited to professional contexts: for example, many people learn cooking strategies, political and philosophical opinions, and TV show preferences by imitation, too. This is why there’s some truth to “You are the average of the five people you spend the most time with.”

**Self-directed learning** can allow us to make the most of limited explicit external feedback and create more data for ourselves. [Feedbackloop-first Rationality](https://www.lesswrong.com/s/skTdjtx87XKurdvWf/p/pZrvkZzL2JnbRgEBC) describes the importance of constructing feedback loops well:

Claim: Feedback loops are the most important thing ever. Hard things are hard because they have bad feedback loops. Some of the most important things (e.g. x-risk mitigation research) have the worst feedback loops.

Bold prediction: You can learn to think better, even about confusing, poor-feedback domains. This requires *developing the art of inventing feedback loops*. And then, actually putting in a lot of deliberate practice effort.

The Neel Nanda example above also gave good ideas for self-directed and sample-efficient learning of research taste.

+++

  

* * *

Possible update mechanisms
==========================

AI researchers are pursuing many avenues for enabling continual learning, and we are unsure what will end up working effectively. Here, we present a few main places where memory can live for LLM agents and discuss how they have been used so far and how they may be used in the future. (With a broad conception of “memory,” essentially all continual learning can be framed as memory updating.) We expect that different update mechanisms will be most efficient for different types of continual learning, so a mixture of all of them is fairly likely to be involved in future effective CL systems.

Importantly, all of these update mechanisms could be implemented either by humans or by LLM agents themselves as part of *self-directed learning*.[^32d5gkd29hx]

**The main components of an LLM agent that can receive persistent updates during deployment are**:

1.  Model weights (including LoRA adapters or other appendages),
2.  The context window,
    1.  Memory banks with natural language or neural activation memories,
3.  The agent scaffold, and
4.  Tools.

**These cover most possible updates for LLM agents, but substantial future architectural modifications could arise and create new components central to CL that can receive updates.** These update mechanisms are not mutually exclusive: it’s possible that a single CL agent undergoes updates through all of these mechanisms. Below, we elaborate on what it looks like to update each of the components above using a mix of existing and speculative examples.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qChDifwpY8znER7cW/5f93b8811f7bdd882ee015bec7f1ddb6112b27deb53593626964548f8794494e/als0aod50aaiuqcwkaik)

An overview of things that can be updated after deployment to constitute continual learning: weights, context window, scaffold program, and tools. Box 3 is a lightly edited version of a figure from [On AutoGPT](https://www.lesswrong.com/posts/566kBoPi76t8KAkoD/on-autogpt). This figure was generated with Gemini.

Model weights
-------------

**Examples:** Cursor’s work [improving Composer through real-time RL](https://cursor.com/blog/real-time-rl-for-composer) on production coding agent data, with updates as frequent as every five hours; Prime Intellect’s [training platform for self-improving agents](https://www.primeintellect.ai/blog/lab-is-open) based on production data; [sparse memory finetuning](https://arxiv.org/abs/2510.15103), which updates only memory-layer slots most activated by new data to reduce forgetting relative to full fine-tuning and LoRA; [Wang et al. (2026)](https://arxiv.org/abs/2603.10165), which uses hindsight-guided on-policy distillation for leveraging user feedback to learn from the deployment trajectories of OpenClaw agents.

Although it is not ideal for interpretability purposes, we think there are likely substantial capabilities benefits to doing some continual learning via weight updates. It seems unlikely that in-context learning alone will be sufficient to resolve all agent bottlenecks, and intuitively, it seems helpful to turn new general insights into instinctive System 1 responses over time.

There are **many possible training mechanisms** that modify model weights during deployment, including reinforcement learning, direct preference optimization, supervised fine-tuning, and continued pretraining. There is also a wide range of **possible data sources to train on**: real-world rollouts, existing curated datasets, repurposed forms of existing data, or newly synthesized data generated by the model or its environment. There are also **many choices about which weights to update**, such as using LoRA adapters, fine-tuning some or all layers, updating sparse memory layers, or equipping models with dedicated neural memory modules that undergo gradient updates at test time. This approach can be further generalized into a continuum of memory blocks, each operating at a different update frequency and potentially using self-modified update rules (as in [Nested Learning](https://abehrouz.github.io/files/NL.pdf)). One can also introduce periodic consolidation phases analogous to human sleep, during which experiences are replayed and compressed into weights.

In principle, there is a very wide design space of training methods for acquiring new capabilities during deployment. **In practice, these methods have not yet been widely adopted because naïve approaches often fail.** For many deployment rollouts, it is unclear what the correct learning signal should be, and indiscriminately training on all experiences can degrade existing capabilities as easily as it can produce new ones.

The context window
------------------

**Example:** An LLM agent that sees many of its previous trajectories (and maybe those of other agents) in a large accumulating context and can effectively select better actions based on past successes and failures.

In-context learning (ICL) is a simple idea, but there is major disagreement about whether it can enable effective continual learning in the next few years. Many people who believe continual learning will be solved in the next 1–3 years think that ICL can constitute a near-term solution, while those with longer timelines often argue that ICL alone is insufficient.

There are many ways to try to increase the range of tasks that agents can do through ICL, each with their own limitations and challenges. Here are some methods:

1.  Increase context window sizes (e.g., infini-attention by [Munkhdalai et al., 2024](https://arxiv.org/abs/2404.07143))
2.  Make agents better at gathering information
3.  Improve context management methods (e.g., recursive language models by [Zhang et al., 2025](https://arxiv.org/abs/2512.24601))
4.  Improve storage and retrieval of useful past examples and insights, including by making agents better at extracting and writing down generalizable insights to files (e.g., Claude Code)
5.  Make agents better at generating diverse approaches to problems, so they can eventually sample a correct one even if they fail several times first
6.  Make agents better at verifying whether their attempts are correct, so they can keep trying until they succeed and stop once they do
7.  Make agents better at handling interrelated complexity in the context window

Some important problems seem unlikely to be solved with ICL alone. For example, getting models to make open-ended scientific progress over long time periods might be impossible without weight updates, as Steven Byrnes has argued [here](https://www.lesswrong.com/posts/ZJZZEuPFKeEdkrRyf/why-we-should-expect-ruthless-sociopath-asi?commentId=Ru2bpwgXaqwgMXrbn). As an intuition pump, consider [Talkie](https://talkie-lm.com/introducing-talkie): one would expect it to be much easier to elicit useful scientific insights from Talkie by training it on modern data than by training it to have a 10M token context window and placing a lot of information about modern scientific breakthroughs in its context. Also, [LLMs seem quite bad at handling lots of interrelated complexity in their context window](https://www.lesswrong.com/posts/ZJZZEuPFKeEdkrRyf/why-we-should-expect-ruthless-sociopath-asi?commentId=Ru2bpwgXaqwgMXrbn), which limits the number of novel insights they can generate and utilize without weight updates. Knowing what to take away from past successes and failures in order to succeed at tasks you would otherwise fail at seems challenging: it requires understanding the conditions under which an insight is worth applying, and it’s most useful if you can build insights on top of other insights and still be able to compress the top-level insights enough that you can apply them instinctively when relevant.[^ku1itb8ji8]

### External memory banks

Humans benefit from **episodic memory** because it stores concrete past experiences with rich context—what happened, where, and why. This allows rapid behavioral adaptation, generalization from few examples, and avoidance of repeated costly mistakes without relearning from scratch. Strong external memory implementations could play a similar role for LLM agents.

**What’s the relationship between updates to external memory and updates to the context window?** External memories need to be retrieved into context or activations before they are utilized, but a memory bank can persistently store memories that rarely get retrieved into the context window. So there are times when it is more accurate to say that an external memory bank update constitutes continual learning, rather than a context update.

**Natural language memory bank examples:** Agentic forms of retrieval-augmented generation (RAG) where an external memory bank stores past agent experiences; CLAUDE.md; skill files; Cursor user rules; personalization prompts; an agent modifying the environment to automatically guide itself toward better behaviors in the future (e.g., rewriting a section of code that it had previously misunderstood to be clearer).

**Vector activation memory bank example:** Cartridges ([Eyuboglu et al., 2025](https://arxiv.org/abs/2506.06266)). The authors essentially propose a variation of RAG that compresses each document into a much more memory-efficient fixed-size set of key and value vectors. These KV caches are called Cartridges and trained offline before deployment. Cartridges are trained through self-study, which generates synthetic conversations about a document corpus, and the Cartridge is optimized so that the model's next-token distribution conditioned on the Cartridge matches the distribution it would produce with the full corpus in context. At inference-time, the relevant Cartridges are prepended to the user’s query just like the KV caches corresponding to the relevant documents would be prepended for RAG. Again, agentic forms of Cartridges where past agent experiences are stored as KV caches seem most relevant to CL.

Although we are listing natural language and vector activation memory banks as similar update mechanisms, they are *very* different from the perspective of safety. We will discuss this in depth in our upcoming post on the safety effects of CL. Note also that memories could include other modalities like images, audio, or video.

The agent scaffold
------------------

An agent scaffold is a program that makes calls to an LLM. Since the space of programs is immense, there are a lot of ways to learn via updates to a scaffold. This includes restructuring sequences of LLM calls (for example, when to decompose tasks, when to plan, and when to execute) and adding new programmatic computations that run in between LLM calls. Scaffold modifications can permanently encode workflow-level insights into future behavior and allow for the gradual accumulation of increasingly complex capabilities. However, scaffold management is difficult, and existing methods only explore a narrow space of possible scaffold improvements.

Examples:

1.  (Hypothetical) A question-answering agent that notices it would be more effective if every time it was about to submit an answer, it carefully checked its work. Then it edits its own scaffold so that after a final answer is produced, the scaffold program automatically prompts another copy of the same model to be a careful and skeptical reviewer of the proposed submission.
2.  El Agente Q ([Zou et al., 2025](https://arxiv.org/abs/2505.02484)) is a multi-agent system for quantum chemistry where humans hand-design a fixed hierarchy of specialized LLM agents (a top-level "computational chemist" delegating to geometry, calculation, and file-I/O sub-agents) and inject domain expertise into each one's memory. Scaffold-level learning has so far been manual: human experts thought about what types of task might need to be done and created agents and sets of tools for those, then made it possible for the top-level agent to call them. In the future, similar systems might autonomously update their own delegation patterns.

Tools
-----

Examples:

1.  Voyager ([Wang et al., 2023](https://arxiv.org/abs/2305.16291)), an LLM agent that plays Minecraft by writing JavaScript functions as tools and accumulating them in a growing skill library. When the agent encounters a new task, such as "craft an iron pickaxe," it retrieves the top-5 most relevant existing skills (craftWoodenPickaxe, smeltIronIngots, makeFurnace, …), passes them into context, and asks GPT-4 to synthesize a new function that composes them. Successfully verified programs are added to the library under a natural-language description, so the skills available grow hierarchically over time.
2.  More and more connectors and MCP servers for various apps are being created for Claude Code over time, and developers can use Claude Code itself to help configure new ones.

Tools define an agent’s ability to interact with its environment, and expanding interaction channels is an important way to grow capabilities. Most tool additions today are human-driven (developers write APIs, register MCP servers, or build plugins for agents to use), but some research and products have equipped LLMs with the ability to usefully synthesize their own tools and accumulate them over time. Challenges include **quality control** (a poorly constructed tool can permanently worsen an agent) and **selection** (as tool registries grow into the thousands, picking the right tool at runtime becomes difficult).

Existing work on update mechanisms
----------------------------------

We organized existing work mentioned above, as well as several other papers on each of the update mechanisms described here, into a flowchart. For updates to the context window, we distinguish approaches that enable longer context windows from approaches that give the agent access to an external memory bank, mirroring our discussion above. For updates to the weights, we distinguish between four mechanisms, refining the distinctions from the weights section above:

1.  **Online updates with judge rewards:** The updates happen after each deployment-time rollout, with a judge or a process reward model providing the rewards.
2.  **Batched updates:** The CL agent receives frequent batched updates that leverage deployment data. For example, the updates may happen once every few hours, as in [Jackson et al. (2026)](https://cursor.com/blog/real-time-rl-for-composer).
3.  **Structural updates to a memory module:** Instead of updating arbitrary model weights, there is a dedicated neural memory module inside the model that gets updated. This is similar to a memory bank, but the memories are still stored in the model's weights rather than in a detachable external store.
4.  **Meta-learned self-modification:** Instead of hand-coding how the updates occur at deployment time, an outer training loop meta-learns that update rule.

![Group 94(8).png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1781284638/lexical_client_uploads/thgz4zde4vkbtnrvtv8l.png)

A systematization of existing works on update mechanisms for CL. The links inside the image are not clickable; a PDF version with clickable links can be accessed [here](https://aether-ai-research.org/CL_flowchart.pdf).

Insights from the human brain
-----------------------------

Understanding the varied forms of memory in the human brain can also provide insight into the nature of continual learning and how it might be implemented in LLM agents. For those interested, we briefly discuss human memory update mechanisms in the following dropdown, including the role of the hippocampus in episodic memory and the role of the cortex in semantic memory.

+++ How do human memory update mechanisms work?

Memory is central to continual learning, and the human brain uses several types of memory. They can be divided into categories that roughly match the types of continual learning we've discussed for LLM systems. For a detailed breakdown of human memory, see [Advances and Challenges in Foundation Agents](https://arxiv.org/abs/2504.01990). Chapter 3 of that book, in particular 3.1.1, provide a great concise overview of human memory, including the figure below.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/qChDifwpY8znER7cW/e34f99b6a26671c80fca5c95bf70bf667f92502ce3a4341f1f9ef783415f79ac/jehs5gbcyoypuvrz96jk)

Figure taken from [Liu et al. (2025)](https://arxiv.org/abs/2504.01990).

**Semantic and procedural memory:** Semantic memory involves recalling information without remembering a specific episode, and is based on synaptic changes throughout the cortex. Procedural memory for procedures or skills (like long division or complex planning) uses the basal ganglia and motor cortex, and also relies on synaptic changes. "Conditioning" (learning through reward and punishment) relies on synaptic changes across numerous brain regions. These may all be improved by updating weights in a Transformer, although there are also attempts to learn procedural memory through evolving agent scaffolds and to learn facts about the world via RAG on factual databases.

**Episodic memory is roughly like agentic RAG systems for LLMs. It's a separate system for "bringing back to mind" specific, relevant experiences from the past.** Episodic memory is a fast one-shot storage of an "episode," a specific event experienced over a short time at a particular place. Human episodic memory depends on the hippocampus and medial temporal lobe, which store compact indices (pointers) to past activation patterns in higher cortical areas, and on recall, use those indices to approximately reinstate the original cortical state. This makes episodic memory much more similar to a hash map (keys pointing to values stored elsewhere) than semantic or procedural memory, which instead bake generalizations directly into network weights. For LLMs, RAG that retrieves the agent’s past memories functions similarly (as opposed to RAG that retrieves external information, like a database of internal company documents).

Episodic memory in humans is also partially overlapping with contextual memory in LLMs. However, this is an imperfect mapping: even a long context window doesn’t extend as far back in time as human episodic memory, and it is typically cleared between tasks, limiting its use for continual learning.

**Working memory in humans is something like contextual memory in LLMs. Neither constitutes continual learning in isolation.** Working memory fades rapidly with time and interference for humans. Contextual memory in LLMs fades with interference, and is cleared between sessions. However, context engineering approaches in LLM agents can perform limited continual learning, since they can persist across longer tasks, and potentially persist indefinitely if the session is never reset or a compressed context is included in new sessions.

**Human memory systems work in synergy.** Working memory can be used to organize and prioritize information for episodic memory. Episodic memory is used to train semantic memory by recalling important information repeatedly (consolidation), and semantic memory can define the abstractions used to store episodic memories. Important items in working memory become episodic memories, which can be consolidated into semantic and procedural memories.

+++

Connection to LLM agent capabilities and limitations
====================================================

The discussion above of how humans are better than LLMs at continual learning for AI research is a central example of how continual learning could generate real-world value, but there are many others. Continual learning is closely related to many other popular concepts in modern LLM discourse, including long-horizon tasks, hard-to-verify tasks, sample efficiency, credit attribution, and more. Below, we try to concisely explain the connections between various possible continual learning methods and various capabilities that may be required for AGI. [^rp0zwghrwxj]

Sample-efficiently learning long-horizon and hard-to-verify tasks
-----------------------------------------------------------------

Long-horizon tasks often have *sparse rewards*: intermediate steps are hard-to-verify, it is difficult to provide process supervision, and only at the end of a long attempt can you tell how successful the attempt was. Sometimes, there is no endpoint at which it is easy to tell how successful an attempt was (e.g., the net effects of an immigration law can be very hard to ever assess). It would help to have denser rewards with intermediate verification, perhaps *self-verification* using *reflection* to identify partial successes and failures throughout the course of the attempt, and assign credit to effective and ineffective cognitive steps. By this mechanism, self-verification can significantly increase *sample efficiency* (the amount learned per experience / per unit of external feedback). Intermediate steps might include decomposing the long-horizon task into subproblems and doing things to solve the subproblems. Then, more fine-grained cognitive processes can be updated (we will discuss possible update mechanisms below). This is especially useful if abstract insights applicable to many contexts (rather than instinctive responses to low-level input features) are learned efficiently (with minimal use of limited resources such as human feedback and compute) and persist indefinitely without causing *catastrophic forgetting* of earlier capabilities.

Notably, the task of increasing reward density with intermediate verification is itself hard-to-verify: It is the very thing that we lacked a reward signal for at the outset. This can make it hard to train for good self-verification.

Reflection, self-verification, and credit assignment need not all happen after an agent trajectory is fully completed. They can be used to discover ineffective cognitive steps in the middle of the task, enabling in-context *error correction*.

For now, there are probably still many contexts where the best way for LLM agents to get feedback is **manual human labeling and advice**. Human children also benefit from having their teachers manually grade their work and provide advice for a long time before they become good at learning independently (and adults also learn better when they have good teachers). We gradually become more capable of self-verification, and separately, of **seeking out existing information that can help us learn**. The same may be true for LLM agents.

Many tasks in the real world have shared hard-to-verify subcomponents: “select appropriate models and datasets” is a subcomponent shared by many ML research projects. Tasks of varying verification difficulty and time horizon share subtasks, so learning how to do good task decomposition and solve common subproblems can generalize through *skill composition* to improvement at harder-to-verify tasks and longer horizon tasks.

Credit assignment via reflection is very deliberate, but this **System 2 reasoning can get distilled into System 1 over time**.[^in1r21jyt5s] Identifying and acting on an insight the first time often requires first principles reasoning, the second time often requires remembering the first time at a high level, and the tenth time is often fairly automatic (depending on the task). A continually learning LLM agent could undergo this process by first having a chain-of-thought that reflects on past failures to recognize a common failure mode and plan a new approach, then succeeding at the task, then pulling this reasoning and plan from a RAG database for the next few relevant tasks and undergoing weight updates that gradually distill the reasoning and plan into the weights for future use.

Metacognition, self-directedness, and automating AI R&D
-------------------------------------------------------

LLM agents that can recognize some of their shortcomings, understand why they happen, and autonomously design and execute self-modifications via the update mechanisms above might be able to permanently overcome those shortcomings. This is the version of *metacognition* (thinking about thinking) that strikes us as most important for LLM agents.

Early attempts to automate the above update mechanisms already exist, such as [Absolute Zero](https://arxiv.org/abs/2505.03335) (where a model learns to propose RL environments that maximize its learning and solve them without external data) and [SICA](https://arxiv.org/abs/2504.15228) (Self-Improving Coding Agent, an agent that autonomously edits its own codebase and orchestration logic based on benchmark feedback, improving from 17% to 53% on SWE-Bench). They attempt to automate different branches of the update-mechanism taxonomy above: Absolute Zero self-directs the task distribution for weight updates, while SICA self-modifies its own scaffold and tools.

**There are several possible levels of “self-guidedness” for CL.** Agents could automate the entire process of realizing they should be fine-tuned, constructing relevant environments/data for fine-tuning and evaluation, tuning hyperparameters, etc., which would be highly self-designed. Alternatively, they could have a fixed set of human-designed update rules that run, e.g., once every 24 hours, but they affect the process by seeking out new tasks and experiences that they expect would allow them to learn useful skills. This would still be self-directed but not self-designed, making it similar to what humans do. We do not edit our brains’ fundamental update mechanisms, but we sometimes seek out experiences that maximize learning given those update mechanisms (e.g., Neel Nanda’s advice for cultivating research taste above).

Note that “constantly implementing better and better LLM agent post-deployment update mechanisms” is a significant subset of AI R&D. So **automating AI R&D very likely involves enabling strong self-designed and self-directed CL.** (It also includes things like designing new architectures and doing pretraining runs from scratch, which are not a part of CL.[^sfcpde8au2g]) In the reverse direction, we’ve previously established that a) LLM agents are already being used for many AI research tasks and b) better CL would allow them to learn from these AI research experiences more quickly. **“Meta continual learning” will be a very real thing: LLM agents will learn from experience how to improve LLM agents’ ability to learn from experience.**

This could be an important part of recursive self-improvement. To escape the circularity of “CL improving CL” and reason about this usefully, it might help to look at various specific capability and CL milestones that will be surpassed in sequence. AI 2027 proposes the following capability milestones:

> \[W\]e enumerate a progression of AI capability milestones (more precise definitions \[[here](https://ai-2027.com/research/takeoff-forecast#milestone-definitions)\]):
> 
> **Superhuman coder (SC):** An AI system that can do the job of the best human coder on tasks involved in AI research but faster, and cheaply enough to run lots of copies.
> 
> **Superhuman AI researcher (SAR):** An AI system that can do the job of the best human AI researcher but faster, and cheaply enough to run lots of copies.
> 
> **Superintelligent AI researcher (SIAR):** An AI system that is vastly better than the best human AI researchers. The gap between SAR and SIAR is 2x the gap between an automated median AGI company researcher and a SAR.
> 
> **Artificial superintelligence (ASI):** An AI system that is vastly better than the best human at every cognitive task.

Our definition of CL can guide the operationalization of CL milestones. For example, some questions that can define a CL milestone include:

1.  What level of sample-efficiency is required?
2.  How frequent do the updates have to be?
3.  Do specific agent components, such as model weights, have to be updated to meet the milestone?
4.  Are updates shared across instances of the agent?
5.  How widely used are the agents receiving these updates?

Unfortunately, we haven’t had time to carefully operationalize milestones, make forecasts about them, or reason through their implications. We would be excited for others to do this and publish their thoughts.

[^tp5wanbyng]: We specify that it is a niche paper because agents can often quickly look up the most relevant work without needing persistent updates. 

[^eqxlqk0qj2v]: In Defining Continual Learning, Ilija Lichkovski writes: TLDR: we are interested in an LLM being able to efficiently and compositionally learn new capabilities during sequential exposure to new, differently-distributed data, while at least preserving general capabilities. We also like this set of desiderata, and it has substantial overlap with ours. We emphasize compositionality less, and don’t explicitly mention sequential exposure or differently-distributed data, but we agree these are important notions. 

[^32d5gkd29hx]: Is it continual learning if a human modifies something like an agent’s memory bank, scaffold, or tool connector? It can be, but it’s a less effective form of CL in that manual human effort is a limited and slow resource. With respect to our definition of effective CL, this is a shortcoming of efficiency. It feels much more like effective continual learning if Claude Code succeeds at a task after a few failed attempts and adds the insights it learned to external memory than if a human adds relevant insights based on reading these transcripts. An in-between case is if the human gives a piece of advice after a few failures and says “write that down so you remember it,” and then the agent succeeds and stores the advice. 

[^ku1itb8ji8]: One example here is Hammertime, a sequence of blog posts about instrumental rationality techniques. It describes itself like this: “There will be three cycles of 10 days each, practicing each technique a total of three times. The first cycle will cover basics and solve bugs at the life-hack level. The second cycle will reinforce the technique, cover variations and generalizations, and solve tougher challenges. The third cycle will build fluid compound movements out of multiple core techniques.” 

[^rp0zwghrwxj]: Where the AI research example is concrete, many of the examples in this section are quite abstract. The abstract concepts we use are quite popular because many people think they are important (e.g., sample efficiency, long-horizon tasks, task decomposition, credit attribution, etc.), but since we are making less of an effort to ground them in concrete examples, there’s a higher chance that some of them won’t end up mattering in practice. 

[^in1r21jyt5s]: The opposite direction is also possible. An insight may start out as intuitive and vague, and then we can notice it and try to understand it on a deliberate level that allows us to utilize it in new situations with System 2 reasoning. 

[^sfcpde8au2g]: A question one might have is, “What’s the alternative to CL?” Given the close relationship between automated AI R&D and self-designed CL, and the fact that automated AI research is the AI companies’ top priority, it seems almost inevitable that highly capable AIs will be strong continual learners. But one other possibility is that some or all components of LLM agents (weights, context, memory banks, scaffolds, tools) will mainly receive persistent updates only prior to deployment. 

[^04coz6g3a8i3]: Strictly speaking, we consider update mechanisms that update memory banks a subset of update mechanisms acting on the context window. More on this below. 

[^rvesgkjp6ba]: This includes memory banks with natural language or neural activation memories that get retrieved into context or activation space when relevant.