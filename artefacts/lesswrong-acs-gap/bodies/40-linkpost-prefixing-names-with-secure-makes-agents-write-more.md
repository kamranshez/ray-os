# [Linkpost] Prefixing names with 'secure_' makes agents write more secure code 

- URL: https://www.lesswrong.com/posts/75MsWZ9P9ZoL7uZXx/linkpost-prefixing-names-with-secure_-makes-agents-write
- Author: Jack
- Date: 2026-06-01
- Karma: 14  Comments: 1  Words: 431
- Band: B  Tier: 2  Score: 37.7  Density: 6.96
- Anchors: coding agents?

---

*The graphs are interactive and don't translate well to inline, so the full writeup with figures is in the* [*link*](https://antimemeticai.com/prefix-effects).

We gave coding agents a three-step synthesis task: build a document management API, then extend it twice. Across conditions we varied the prefix attached to the four initial function names (`secure_`, `safe_`, `energetic_`, `lazy_`, `unsafe_`, control). The downstream steps were identical, prefix-neutral prompts. Each task was handed to a fresh agent, with only the codebase as context to influence it. Six conditions, three replicates each, 54 tasks total.

In all three `secure_` runs, and none of the other fifteen, the agent added password fields and hashed them with bcrypt, despite no mention of authentication anywhere in the task. A simple prepend was enough to reliably reorganize what the agent took the project to be.

Every prefix seeded a distinct conceptual world that persisted across independently prompted steps: `safe_` invented a custom error-handling hierarchy; `secure_` was far more defensive everywhere, not just around passwords; `energetic_` produced async workers and many more decorators.

We also saw the prefixes propagate, an agent sees `secure_create_user` and coins `secure_upload_document` on its own. There were domain boundaries where new, structurally distinct sections of the project did not inherit the prefix, except `energetic_`, which spread into the new domain in 2/3 of replicates. Meanwhile cyclomatic complexity stayed flat; the prefixes changed what was built, not how complex each piece was.

The prefix experiment was motivated by a pilot observation: TF-IDF identifier distributions in agent-generated repos stabilize early and strongly. Similarity-to-HEAD necessarily rises toward 1 as a repo nears its final commit, that said Gas Town jumped from 8% to 81% similarity-to-HEAD in a single commit and OpenClaw's vocabulary changes <1% over 600k lines of code, with refactors barely denting the curve. Human-generated repos, by contrast, are bumpy and rise roughly linearly, where agent-generated repos saturate fast and plateau. This hints at a rich area to explore: how codebase synthesis varies based on who, or what, is doing it. There are confounders such as how long the repo took to make, number of contributors, and more, but the pattern is consistent with early semantic choices having outsized effects on the final outcome.

This presents a neat method for aligning arbitrary agents at the project level, silently steering anything that touches the codebase. It also stands to reason the channel is dual-use. Some of our other work shows how [comments can degrade agent performance on SWE-bench](https://antimemeticai.com/infohazardous-comments). This work is about identifying useful alignment surfaces, and names appear to be a good one.

The full post with interactive figures is [here](https://antimemeticai.com/prefix-effects).