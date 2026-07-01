---
title: "Building the Future of coding, OpenCode with Dax Raad"
video_url: https://www.youtube.com/watch?v=IGsbARhERqc
video_id: IGsbARhERqc
channel: NeetCode
published: 2026-03-03
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Building the Future of coding, OpenCode with Dax Raad**](https://www.youtube.com/watch?v=IGsbARhERqc) - NeetCode - uploaded 2026-03-03

> next-step video available: one complement pitch on how to triage which AI code you actually read

## The one idea worth a video

- **Spine 1: Codebase consistency is now the top lever on agent output quality, because the model copies whatever pattern it happens to read.** It subsumes the video's domain-driven-design, opinionated-frameworks, and "not a single file deviates" advice. VERDICT: ✅ already covered by ACS.
- **Spine 2: Do not review every line of agent output equally, calibrate review depth to how mature or unstable the codebase area is, and clean under-reviewed corners fast so they do not poison future generations.** VERDICT: 🔗 next-step video available.

## Summary + counts

NeetCode interviews Dax Raad, co-creator of OpenCode, on agentic coding competition, positioning versus product, code quality, skill atrophy, hiring, and becoming an elite developer today.

🔴 0 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 (✅ COVERED, kept for altitude, excluded from pitches)

**The claim:** once agents write most of your code, codebase consistency becomes the single biggest lever on output quality, because the model reproduces whatever pattern it reads. **Why it is non-obvious:** the old default was to let a codebase accumulate layers, an old way and a new way, and clean up later, because that mess was cheap when humans knew which layer was current. **Why it is true:** the model cannot tell your deprecated pattern from your current one, so it treats any file it reads as the template and generates more code in the stale style, which means drift no longer sits inert, it actively multiplies, therefore the cost of inconsistency flips from ignorable to compounding. Dax puts it bluntly: "your LLM can't differentiate between the old way and the new way," and "we have a bunch of idiots working for us now, like these LLMs." **What it generalizes to:** prompt libraries, where one stale example poisons a whole batch of outputs. **How it goes wrong:** standardizing a young codebase too early, or freezing on a pattern that is itself wrong. ACS already teaches this move as "The One-Pattern Rule for Agents," so this spine earns no new video.

### Spine 2 (🔗 COMPLEMENT)

**The claim:** stop reviewing agent output uniformly, calibrate how hard you look to how stable the area is, and clean up the corners you under-reviewed before they spread. **Why it is non-obvious:** the loud takes are binary, either read every generated line or trust the agent fully, whereas Dax reframes review as triage. **Why it is true:** in mature, well-patterned zones the output space is narrow, so a glance ("does this roughly look right") is enough, while in unstable zones the model has room to be wrong, so scrutiny actually pays off, and crucially any corner you skim must be cleaned quickly because otherwise it becomes the next pattern the agent copies, which means review depth and codebase hygiene are one loop, not two. **What it generalizes to:** reviewing junior-developer PRs by risk, or sampling QA effort by module churn rather than reviewing everything equally. **How it goes wrong:** miscalibrating trust when a "stable" area quietly drifted, using triage as an excuse to read nothing, or over-engineering "elaborate structures of prop testing" and LLM feedback loops when, as Dax says, you should "just read the code" for thirty minutes.

## 🎬 Proposed ACS videos

### 1. How to Decide Which AI Code You Actually Need to Read

- **HOOK:** You cannot read every line the agent writes, and reading none of it is how bugs quietly ship.
- **THE PROMISE:** For engineers drowning in agent output, walk away able to build a risk map of your codebase that tells you exactly where to spend your review attention.
- **THE SHAPE:**
  1. Split the codebase into stable, well-patterned zones versus unstable or brand-new zones.
  2. Glance-review the mature zones, letting the established pattern constrain what the agent could have produced.
  3. Diligently review the unstable zones plus anything security or data sensitive.
  4. Add a second signal by testing user-facing changes from the user's perspective, the way Dax tested a new terminal dialogue.
  5. Clean up any under-reviewed corner immediately so it cannot poison future generation, and when stuck, just read the code for thirty minutes (agent-assisted) instead of building an elaborate auto-fix loop.
- **SPINE:** Spine 2.
- **SLOT:** Techniques > Debugging & Verifying Output (next to "Understanding Agent Output" and "Agent Introspection"), or Master Claude Code > Built-In Skills alongside /code-review.
- **RELATIONSHIP:** 🔗 complements "/code-review" by being its next step. That video already teaches how to RUN the deep multi-agent review workflow (finder and verifier fan-out, effort levels, auto-fix), so do not re-teach the tool; this video teaches the upstream human decision of WHERE to point that scrutiny and how to calibrate trust by codebase-area maturity, plus the cleanup loop that stops light-touch code from becoming the agent's next template.
- **PROOF TO REUSE:** Dax on reviewing "mostly right ... I'll do like a quick glance, does this roughly look right" in mature areas versus "these areas are a little bit less stable, I got to be a lot more diligent"; the terminal-dialogue feature he tested from a user perspective and cleaned up later "so it doesn't start poisoning other LLM generation"; and his critique of people who "build elaborate structures of prop testing" and feedback loops "instead of just sitting down for like 30 minutes and reading the code."

## 📚 Full wisdom (reference)

**SUMMARY**
NeetCode interviews Dax Raad, co-creator of OpenCode, on agentic coding competition, positioning versus product, code quality, skill atrophy, hiring, and becoming an elite developer today.

**IDEAS**
- OpenCode's success came mostly from positioning, being open source and model agnostic, not raw product quality.
- LLMs cannot distinguish your codebase's old pattern from the new one, so inconsistency poisons future generations.
- Cleaner codebases matter more than ever because agents replicate whatever existing patterns they happen to read.
- Dax reviews agent code lightly in mature areas but diligently where patterns feel unstable or risky.
- Claude Code stuck because it lived outside the editor, letting Vim users keep their text workflow.
- Cursor failed for Dax's team because AI suggestions invaded the editor they wanted for text editing.
- Writing types, function signatures, and folder structure is Dax's process for figuring out what to build.
- Roughly ninety-five percent of bad code reflects inexperience, only five percent reflects genuine intentional speed tradeoffs.
- Someone more skilled ships equally fast without the shortcuts, so quality shortfalls are usually skill issues.
- Anything letting people exert less energy wins, so AI adoption is inevitable regardless of its downsides.
- Dax fears his coding skill atrophy much like his mental math quietly decayed after school ended.
- OpenCode hired roughly fourteen people in months with no interviews, no resumes, no knowledge of employers.
- Open source contribution acts as OpenCode's hiring filter since cutting through AI PR noise is hard.
- Dax played OpenAI against Anthropic, securing Codex plan access the day before Anthropic blocked Claude Max.
- Elite developers break the ceiling by becoming expert in a second domain beyond programming skill itself.
- People building elaborate prop-testing feedback loops should often just sit and read the code thirty minutes.

**INSIGHTS**
- Positioning beats product: a half-as-good OpenCode would still win by owning the open-source, model-agnostic slot cleanly.
- The agent is a diligent idiot with photographic memory, so codebase discipline replaces trust in judgment.
- Review depth should scale with area instability, not apply uniformly across every file the agent touches.
- Claims of writing zero handwritten code often exaggerate reality driven by fear of being left behind.
- The real filter for any hype is whether the tools built with it are actually good.
- AI shipped features faster but made deciding what to build even harder and more consequential now.
- Technical skill alone has zero or even negative value when aimed at the wrong problem entirely.
- Caring about being ultimately right, not winning arguments, is the underlying skill behind good judgment calls.

**QUOTES**
- "Someone better than you didn't have to make those trade-offs and they ship just as fast." (Dax Raad)
- "your LLM can't differentiate between the old way and the new way." (Dax Raad)
- "we have a bunch of idiots working for us now, like these LLMs." (Dax Raad)
- "if our product was half as good, I think we'd probably still be equally as successful." (Dax Raad)
- "there's always people 10x worse than you, always people 10x better than you." (Dax Raad)
- "The day you accept an exhibition offer is a day that every single dream you ever had is now dead." (Dax Raad)
- "tell them to off until they add another zero." (Dax Raad, quoting a teammate)
- "just read the code." (Dax Raad)
- "technical skills alone actually don't really get you anywhere if you're just working on the wrong problem." (NeetCode)
- "I'm talking about ultimately knowing that you had the correct model of the world." (Dax Raad)

**HABITS**
- Dax edits text in Neovim and switches to the agent only for dedicated agent work separately.
- He writes types and function signatures first to think through how a new feature should work.
- The team articulates patterns intentionally, ensuring no single file deviates from the agreed current approach anywhere.
- They adopt opinionated frameworks and domain-driven design so strong patterns are baked directly into everything built.
- Dax cleans up under-reviewed corners fairly promptly so they do not poison later agent code generations.
- He tests new features from the user's perspective when he reviews the underlying code less thoroughly.
- Dax studies every company, person, and incentive in his space to place bets far more accurately.
- He limits what he consumes, avoiding echo chambers that bias his thinking away from real clarity.

**FACTS**
- OpenCode grew from a six-person team to roughly twenty people within just a few short months.
- Dax's previous project SST reached profitability with only three people around February of the year 2025.
- Anthropic acquired Bun and OpenAI acquired OpenClaw, per the recent acquisitions discussed openly during this conversation.
- OpenCode serves a potential market of roughly thirty to fifty million developers worldwide, Dax personally estimates.
- Anthropic blocked Claude Max subscription use inside OpenCode, though workarounds reportedly existed at recording time still.
- OpenCode built a terminal framework in Zig with React and SolidJS bindings inside a Bun binary.
- Facebook reportedly offered Snapchat roughly four billion dollars, an offer that Snapchat famously turned fully down.
- OpenCode's OpenAI deal also gave several other coding agents, like Pi, access to OpenAI subscription plans.

**REFERENCES**
OpenCode (opencode.ai), Dax Raad (x.com/thdxr), SST, Claude Code, Boris (a Claude Code creator), Cursor, Codex, Pi (coding agent), Bun and Jared/Jarred (its creator), OpenClaw, Anthropic, OpenAI, GitHub, GitLab, JetBrains, Amazon Bedrock, Neovim / Vim, Zig, React, SolidJS, domain-driven design, PostHog (sponsor), Greptile (sponsor), Snapchat and Meta / Facebook, Vercel, NeetCode (neetcode.io).

**ONE-SENTENCE TAKEAWAY**
Because agents copy whatever they read, codebase consistency and calibrated review now govern output quality.

**RECOMMENDATIONS**
- Establish one canonical pattern per concept and ensure every file conforms before scaling agent usage broadly.
- Choose opinionated frameworks with strong built-in conventions so agents inherit good patterns without extra instruction needed.
- Split your codebase into stable versus unstable zones, then calibrate review depth for agent output accordingly.
- Clean up any lightly reviewed code quickly so it never becomes the pattern agents copy next.
- Before automating an elaborate fix loop, just read the code for thirty minutes, optionally staying agent-assisted.
- Keep your editor separate from the agent so text editing and delegation never fight each other.
- Become a genuine expert in your industry's domain, not only in programming, to unlock rare opportunities.
- Judge quality shortfalls honestly as skill gaps to fix next time, not permanent intentional tradeoffs forever.
