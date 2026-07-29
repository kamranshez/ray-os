# Orbit: A framework for multi-agent security evaluations

- URL: https://www.lesswrong.com/posts/S44mM9b7QvDttjizb/orbit-a-framework-for-multi-agent-security-evaluations
- Author: wlanderson
- Date: 2026-07-25
- Karma: 7  Comments: 0  Words: 426
- Band: A  Tier: 1  Score: 97.4  Density: 25.4
- Anchors: sub-?agents?, coding agents?

---

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784731220/lexical_client_uploads/j1nj6ytstaurhxw4tigh.png)

*This post announces work completed as part of the* [*MATS*](https://www.matsprogram.org/) *9 program, supervised by* [*Dr. Christian Schroeder de Witt*](https://wittlab.ai/author/christian-schroeder-de-witt/). Moving forward, Orbit will be supported by the [*Cooperative AI Foundation*](https://www.cooperativeai.com/foundation). We're grateful to MATS and our Research Manager, Srija Chakraborty, for their support. Repo:  [https://github.com/wlanderson0/orbit](https://github.com/wlanderson0/orbit)

  

We’re excited to release v0 of **Orbit**, a framework for multi-agent safety and security evaluations built on Inspect. This is still a work in progress, and we expect to substantially update and expand based on early feedback.

The world is increasingly multi-agent
-------------------------------------

Frontier models are now often deployed, implicitly or explicitly, as part of large multi-agent systems. Coding agents can invoke subagents, many people have agents helping manage their communications, and swarms of automated researchers are spinning up inside the labs. With this comes qualitatively new risks, as agents might miscoordinate, come into conflict, or collude to evade monitoring ([Hammond et al., 2025](https://arxiv.org/abs/2502.14143), [Schroeder de Witt et al., 2025](https://arxiv.org/abs/2505.02077)).

Current defenses fall short
---------------------------

Increasingly, the defenses built to monitor a single agent fall short when extended to multi-agent systems ([Anthropic, 2025](https://www.anthropic.com/news/disrupting-AI-espionage), [Makins et al., 2026](https://arxiv.org/abs/2607.07368)). Moreover, each system's configuration: its topology, roles, and communication patterns, changes the attack surface and where its vulnerabilities lie ([Hagag et al., 2026](https://arxiv.org/abs/2604.23459)), so a defense that works in one setup may fail in another. Even when researchers build defenses explicitly for multi-agent risks, they often evaluate this defense in some new, bespoke setting focused only on a narrow risk. This makes comparison difficult and slows progress. To this point, there was no standardized evaluation infrastructure for multi-agent systems.

Introducing Orbit
-----------------

We built Orbit to help change this. Orbit extends Inspect to support decentralized, long-running environments with many independent agents. It supports arbitrary topologies, scheduling, memory sharing, and more. You can create new scenarios easily, and quickly configure experiments (altering topology, roles, models, etc.) on existing scenarios with YAML configs. We provide:

*   5 scenario families: coding, desktop, browser, customer-service, and cooperative-allocation tasks,
*   4 threat types: prompt injection, compromised agent, collusion, and misuse
*   4 defense categories: security prompting, monitors, guardian agents, and dual-LLM

We’re aiming for extensibility, flexibility, hackability, so you can easily build new scenarios and recombine existing ones to work for you. We plan to expand the suite substantially over time. We’re also building many extensions and further tooling: custom viewers, integration with Hawk for large-scale evals, automated auditing, and more.

Get started
-----------

We’re keen for you to try it out and let us know how to make it work for you.

**Repo:**  [https://github.com/wlanderson0/orbit](https://github.com/wlanderson0/orbit)

**Contact form:**  [https://forms.gle/XLX7UH2KAsnmMYUS8](https://forms.gle/XLX7UH2KAsnmMYUS8)