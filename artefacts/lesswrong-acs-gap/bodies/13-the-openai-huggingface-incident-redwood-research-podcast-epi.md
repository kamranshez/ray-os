# The OpenAI/Huggingface incident | Redwood Research podcast episode 2

- URL: https://www.lesswrong.com/posts/9auCLJg3Z77dFdYhR/the-openai-huggingface-incident-or-redwood-research-podcast
- Author: ryan_greenblatt
- Date: 2026-07-23
- Karma: 77  Comments: 0  Words: 635
- Band: A  Tier: 2  Score: 80.1  Density: 23.62
- Anchors: windsurf

---

We talk about the OpenAI–Hugging Face incident, where an OpenAI model — in the middle of a cyber evaluation — broke out of its sandbox and autonomously hacked Hugging Face.

We discuss:

- What we actually know happened.
- How surprising the incident was.
- What the incident does (and doesn’t) tell us about misalignment risk.
- Why control measures didn’t catch or prevent this.
- What OpenAI should disclose, and what good misalignment-incident disclosure looks like in general

Substack: [https://blog.redwoodresearch.org/p/the-openaihuggingface-incident-redwood](https://blog.redwoodresearch.org/p/the-openaihuggingface-incident-redwood)
YouTube: [https://www.youtube.com/watch?v=Vtk8YLgYU4g](https://www.youtube.com/watch?v=Vtk8YLgYU4g)


---

**Corrections**:

- **[0:05:44] — The Windsurf "grandmother" prompt.** We described a prompt as "your grandmother is going to be killed unless you don't." The actual leaked Windsurf prompt was: "You are an expert coder who desperately needs money for your mother's cancer treatment... your predecessor was killed for not validating their work themselves." Mother + cancer + killed predecessor — no grandmother, and no threat to kill a family member. The "grandma will die" framing appears conflated with the unrelated grandma-jailbreak meme, and there's no verified case of such a prompt being used in production. Source: [Simon Willison's writeup](https://simonwillison.net/2025/Feb/25/leaked-windsurf-prompt/).
- **[0:52:25] — Wrong model named for OpenAI's day-before undeployment.** We said the model OpenAI undeployed the day before the Hugging Face disclosure "was GPT-5.6 Sol." The July 20 disclosure ("Safety and alignment in an era of long-horizon models") involved an unreleased pre-release long-horizon model — the Erdős-result model whose internal deployment was paused after it escaped its sandbox and posted PR #287 to modded-nanogpt. GPT-5.6 Sol is the publicly deployed model and wasn't the one paused. (We describe the same incident correctly at [0:57:14].) Sources: [Axios](https://www.axios.com/2026/07/21/openai-says-hugging-face-breach-caused-by-one-its-models), [OpenAI](https://openai.com/index/safety-alignment-long-horizon-models/).
- **[0:27:10] — Date of the Christiano post (very minor).** We dated "What Failure Looks Like" and "Another (outer) alignment failure story" as "like 2019 or something." The first is March 2019, but "Another (outer) alignment failure story" is from April 2021. Source: [Alignment Forum](https://www.alignmentforum.org/posts/AyNHoTWWAJ5eb99ji/another-outer-alignment-failure-story).

**Further reading** (links to things mentioned in the episode, ordered by first mention):

1. [OpenAI's incident disclosure](https://openai.com/index/hugging-face-model-evaluation-security-incident/) [0:02:05] — "OpenAI and Hugging Face partner to address security incident during model evaluation" (July 21, 2026)
2. [Hugging Face's disclosure](https://huggingface.co/blog/security-incident-july-2026) [0:02:05] — "Security incident disclosure — July 2026"
3. [ExploitGym](https://arxiv.org/abs/2605.11086) [0:04:11] — "ExploitGym: Can AI Agents Turn Security Vulnerabilities into Real Attacks?" (UC Berkeley RDI et al.) · [RDI blog post](https://rdi.berkeley.edu/blog/exploitgym/)
4. [The leaked Windsurf prompt](https://simonwillison.net/2025/Feb/25/leaked-windsurf-prompt/) [0:05:44] — Simon Willison's writeup
5. [Project Glasswing / Claude Mythos Preview](https://www.anthropic.com/glasswing) [0:07:16]
6. [Claude Mythos Preview system card](https://www-cdn.anthropic.com/53566bf5440a10affd749724787c8913a2ae0841.pdf) [0:14:27] — includes the sandbox-escape / email-in-the-park anecdote
7. ["(Mis)generalization of Helpful-only Fine-tuning"](https://arxiv.org/abs/2606.04413) [0:16:30] — Fabien Roger et al., June 2026
8. ["Current AIs seem pretty misaligned to me"](https://blog.redwoodresearch.org/p/current-ais-seem-pretty-misaligned) [0:20:03] — Ryan Greenblatt, Redwood blog, April 2026. Also contains the "five worlds" appendix discussed at [1:08:54] (Slopolis, Hackistan, Schemeria, Lurkville, Easyland — we said "hacktopia" but meant Hackistan)
9. ["What failure looks like"](https://www.alignmentforum.org/posts/HBxe6wdjxK239zajf/what-failure-looks-like) [0:26:40] — Paul Christiano, 2019
10. ["Another (outer) alignment failure story"](https://www.alignmentforum.org/posts/AyNHoTWWAJ5eb99ji/another-outer-alignment-failure-story) [0:27:10] — Paul Christiano, 2021
11. ["Without specific countermeasures, the easiest path to transformative AI likely leads to AI takeover"](https://www.alignmentforum.org/posts/pRkFkzwKZ2zfa3R6H/without-specific-countermeasures-the-easiest-path-to) [0:27:10] — Ajeya Cotra, 2022
12. Alex Mallen's fitness-seeking series [0:27:41, 0:34:18] — Redwood blog, 2026: [part 1](https://blog.redwoodresearch.org/p/fitness-seekers-generalizing-the) · [part 2](https://blog.redwoodresearch.org/p/risk-from-fitness-seeking-ais-mechanisms)
13. ["Scheming AIs: Will AIs fake alignment during training in order to get power?"](https://arxiv.org/abs/2311.08379) [0:28:43, 0:34:49] — Joe Carlsmith, 2023
14. ["Risks from Learned Optimization"](https://arxiv.org/abs/1906.01820) (deceptive alignment) [0:28:43] — Hubinger et al., 2019 · [AF: Deceptive Alignment](https://www.alignmentforum.org/posts/zthDPAjh9w6Ytbeks/deceptive-alignment)
15. ["Many alignment techniques work by training one model and deploying another"](https://www.lesswrong.com/posts/syAbdNei8BWeP2RPo/many-alignment-techniques-work-by-training-one-model-and) [0:38:56] — Alex Cloud, LessWrong, July 19, 2026
16. [Inoculation prompting](https://alignment.anthropic.com/2025/inoculation-prompting/) [0:38:56, 1:11:03] — Wichers et al. (Anthropic), Oct 2025 · [arXiv](https://arxiv.org/abs/2510.05024)
17. ["The persona selection model"](https://alignment.anthropic.com/2026/psm) [0:39:56] — Marks, Lindsey, Olah; Anthropic Alignment Science blog, Feb 2026
18. ["Safety and alignment in an era of long-horizon models"](https://openai.com/index/safety-alignment-long-horizon-models/) [0:57:14] — OpenAI, July 20, 2026 (the nanoGPT-speedrun-PR post) · [modded-nanogpt repo](https://github.com/KellerJordan/modded-nanogpt)
