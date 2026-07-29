# Agentic Frameworks: Or different ways to make LLM API calls

- URL: https://www.lesswrong.com/posts/YMw2PhtDGcCwgc4GA/agentic-frameworks-or-different-ways-to-make-llm-api-calls
- Author: astle dsa
- Date: 2026-06-24
- Karma: 3  Comments: 2  Words: 1380
- Band: A  Tier: 1  Score: 71.2  Density: 16.72
- Anchors: claude code, \bcodex\b, sub-?agents?, agent(ic)? loop

---

The agentic framework research has produced some very interesting results; from different topologies to different ways of using tool-calls, it has been one of the most fascinating and accessible areas of research in the AI landscape. In this essay, I’d like to talk about some core structures that sit at the heart of various agentic framework applications we have seen, and some (possibly) new directions I’d like to explore.

I.
==

We must, before anything else, define the most primitive tool we have: a simple text-in-text-out API call. Following that, we have perhaps the most important one: JSON or structured outputs. Taking these two API calls, we can come up with four different paradigms (methodologies?) for creating frameworks, and explore which ones accomplish certain goals better than a simple TITO API call.

1.  **The Sequencing Model :** The first framework is also the simplest: just call the LLMs in succession, each time with a different task and tool combination, with the output from the previous call appended/fed into the subsequent call. This is a simple way of managing context and separating tool usage per API call.

![chart](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782081772/lexical_client_uploads/nqd6huccdfpzcdotgqbq.webp)

API call in sequence

2.  **The Branching Model :** The next framework is but a simple modification over the previous one, wherein we allow for two simultaneous LLM API calls to be made, assigned independent tasks which can be completed without dependency problems. This was one of the more widely implemented frameworks, especially in workflow settings. Almost all “agent“ implementations today follow this framework, using libraries like LangGraph, Mantra or n8n. This setup gives rise to structures like agentic trees and graphs, where each node is defined using a system prompt plus a tool-set. Most commonly implemented is a workflow graph setting.

![chart](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782081851/lexical_client_uploads/spcrxzgw2ykvirnotex3.webp)

API calls, branching

  

3.  **The Looping Model :** Here we finally arrive at the most implemented, widely known and perhaps the most effective framework: looping the model. We start with an outer loop called the REPL, which repeatedly takes in the user’s request. Upon taking the request, a while loop is initiated, which calls the LLM API, performs tool call execution and feeds the outputs back into the context for the subsequent LLM API call. The loop only ends when either no tool is called (the LLM outputs plaintext) or there’s a special tool to stop the loop (this is an implementation detail)[^3aj9k0al5yi]. Very common and widely known examples: Codex, Claude Code and [Pi](https://pi.dev).

![3.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782082129/lexical_client_uploads/uxsfn8bnh2vpx1rvtbky.png)

The outer REPL loop, and the inner while loop

4.  **The Recursive Model :** Perhaps the latest framework, and one which created some buzz, was the RLM or the recursive language model setup. Though it sounds like there’s a new architecture, this is but a simple engineering of the LLM API call. As mentioned in the [original paper/blog](https://alexzhang13.github.io/blog/2025/rlm/), we simply allow a single LLM API call the ability to access a REPL environment, store the context and request it as a variable in that environment, and provide a special tool, which allows it to make another API call to a language model, so that it can delegate tasks, break down contexts and perform other actions. This is, as is obvious, an agentic framework but with a special tool: the ability to call itself. Hence recursion. This gives rise to multi-agent setups (which currently Claude Code can carry out). The main point of the authors is that language models, which are generally trained on tool-calling, must be specifically trained on this one, which might lead to improvements. Here’s their [follow-up paper](https://alphaxiv.org/blog/reinforcement-learning-for-rlms), in which they did fine-tune a model [^9sz02sl2zm].

![4.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782082220/lexical_client_uploads/fuvct3f4syl6nj8kcrtl.png)

An LLM making other LLM API calls

II.
===

With these, we basically cover the core primitives of different methodologies, and another great step forward (at the cost of high token usage) would be to mix and match these structures and observe what works best. A few ways to mix and match:

*   The simplest approach would be to replace the LLM API call with the agent abstraction, which means every framework above can be re-wired with the agent framework, calling **agents** in sequence and branching instead of making API calls to LLMs. One might wonder, however, what the advantage of that would be, since the agent (I am using this henceforth to mean LLM API call plus tools on a loop) is good at handling all the tools at once? One thing is the environment or workspace. A single agent can be given access to a particular environment only, and multiple such agents can be tasked with performing certain actions (with the given topologies) within their own respective environments, and their results can be communicated through certain mediums (I’d call this the *Swarm* Model).
*   Although I do not see much advantage here, only marginal, we can replace each LLM API call within the agentic loop with a recursive API call, the one used in RLMs. Although this can be applied to a task where each inner loop generates massive amounts of context (since the intent of the authors to create RLMs was to manage context), this would be quite rare in real life (a use case where each loop produces enough context to overwhelm a modern LLM, forcing us to rely on RLMs, would be extremely rare) [^h74jjg7uu05].
*   And finally, as was foreseeable, we combine all the above methods: Recursive LLM API calls plus a self-calling tool on a loop. This is a multi-agent RLM kind of setting. Once again, I am not sure where this kind of architecture can be really useful, but this would create an entire ecosystem of recursive agents.

III.
====

Although the above architectures seem very simple to implement, they require careful calibration, error and context management, and we cannot forget that the agentic framework only works because the frontier AI labs specifically fine-tune their models in order to perfect tool-calling. Even according to the researchers of the RLM paper, the models would benefit a lot from being fine-tuned on the self-calling tool.

One other problem is that of coordination. LLM agents which are unaware of other agents' contexts and changes can often become counter-productive and can lead to an overall degradation of the work. This seems to be distributed systems problem, and there are certain [very](https://github.com/aslangoldenhour/multiagent-consensus-mono)  [interesting](https://github.com/WindyLab/ConsensusLLM-code)  [implementations](https://github.com/ruvnet/ruflo) that try to tackle the [coordination](https://github.com/ManasviGoyal/Distributed-Multi-Agents) problem by using techniques from distributed systems theory [^7vnp6sjghy].

The opposite of the distributed settings, would be a set-up I’d call the [Stigmergical](https://francisheylighen.substack.com/p/stigmergy-the-most-important-concept?triedRedirect=true) framework [^wmcsa0c1mur]. n short, each LLM/API call is given a task which *modifies an environment*. This allows for “communication“ of an agent’s action through the medium, and not by any direct means. This shifts the task of communication from the agent to the medium it’s working in. This method is truly beneficial when it comes to scale: a thousand agents communicating with each other is a combinatorial explosion, while a thousand agents—where each only communicates with or modifies a medium, and the medium carries the “information“—can coordinate much more effectively.

One structure, which seems very logical right now, would be a hierarchical structure, where a few Recursive Agents (LLM API plus self-call-tool plus Loop) can delegate certain tasks as sub-tasks to other Agents (with or without the self-call tool. Maybe the LLMs can decide for themselves?), while coordinating with each other (through some means; here we can take some inspiration from distributed systems).

![5.webp](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1782082421/lexical_client_uploads/uafvbuwlbtvmzvvmjqjj.webp)

Recursive Agents coordinate, and delegate to other recursive agents or normal agents

IV.
===

With this, I have tried to exhaustively cover all the ways in which we can make LLM API calls. My assumption here is that as the models become smarter, and if the frontier AI labs think it’s worth fine-tuning the models for the self-call tool, the more complex a system we can build. Right now, the only problem I can foresee with the “swarm“ intelligence, or deep sub-agentic setups, is model confusion or deviation from the goals.

Though I do think if the models can effectively navigate a multi-agent setup (either with or without self-call), we could get to solutions with much more complex problem statements, with the type of emergent solutions we observe in human societies. Coordination at scale can solve truly complicated problems.

*Thank for reading this far !*

[^3aj9k0al5yi]: During implementation, however, we must not forget that the looping paradigm only works if we use the ReAct method: the model must plan everything out ahead in reasoning traces, before the execution begins. 

[^9sz02sl2zm]: In case the branching model and the recursive model appear similar, one difference among them is that the LLM API call in the former never gets access to a self-calling tool, and the subsequent calls are made by an outside orchestrator code. However, in case of RLMs, the LLM does get access to a self-calling tool. 

[^h74jjg7uu05]: I asked an LLM this question and to provide me with an example. One example that it thought could be was an algorithmic trading bot, which consumes market data tick-by-tick, and performs analysis on it. 

[^7vnp6sjghy]: A thread of me discussing this. 

[^wmcsa0c1mur]: This is actually a well-known design pattern, called the BlackBoard pattern.