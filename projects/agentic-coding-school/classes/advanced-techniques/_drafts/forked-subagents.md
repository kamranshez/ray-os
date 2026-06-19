---
class: "advanced-techniques"
chapter: "Subagents"
status: "scripted"
---

## The Missing Piece

Anthropic just shipped the feature that fixes the single biggest problem with Claude Code subagents. It's called forked subagents, and once you understand it, you'll use it every day.

A regular subagent starts from a blank context. The main session writes a short prompt, hands it over, and the subagent works from there. That blank context is sometimes the whole point. But often, it's the reason your subagents do worse work than you expect.

A forked subagent skips the compression. It inherits the entire conversation history of the main session. Every message, every tool call, every detail you've accumulated. Then it goes off and does its work with all of that nuance intact.

[IMAGE: dark background, two panels side by side. Left panel labeled "Normal Subagent" shows a fat main conversation funneling into a tiny prompt arrow into a small subagent. Right panel labeled "Forked Subagent" shows the full main conversation cloning into the subagent at full size]

![[images/forked-subagents/the-fork.png]]

---

## The Compression Problem

Here's the situation that made me want this feature for months.

I'd be designing something with Claude Code. Picking fonts, debating colors, deciding what feels right for a landing page. The conversation would run long. Fifty thousand tokens of back and forth. A lot of that is nuance. The reason we picked one font over another. The kind of clients we're trying to attract. Three things I rejected and why.

Then I'd say "okay, spin up three subagents in parallel, one for each design variation, so they don't bias each other."

Claude Code would compress fifty thousand tokens of nuance into a two thousand token prompt for each subagent. And the subagents would do worse work than the main session would have. They couldn't remember the things we'd already ruled out. They couldn't feel the taste we'd built up. They produced generic designs because they were working from a generic brief.

That's the compression problem. The main session has the context. The subagent gets a summary. And the summary is always thinner than what you actually meant.

[IMAGE: dark background, a thick rope labeled "50k tokens of nuance" being squeezed through a tiny funnel labeled "compression" and coming out as a thin string labeled "2k token prompt", with a sad subagent face at the end]

![[images/forked-subagents/compression-problem.png]]

---

## What Forking Actually Does

A fork is a subagent with the parent's full context preloaded.

You start a forked subagent and it begins life at message N of your conversation, not at message zero. It has read everything you've read. It has seen every tool call you've made. It knows the things you've already ruled out without having to be told.

When it finishes, it returns the relevant result back to the main session, exactly like a normal subagent. The main session stays clean. Only the conclusion comes back, not the noise of the work.

So you keep both wins. The main conversation stays lean. The subagent works with the full picture.

---

## Anthropic Is Already Using This

A few features you've already seen are forked subagents under the hood.

`/recap` uses a fork to summarize the session. It needs the full conversation to do that, so it forks.

`/btw` and `/btw` use forks. The whole point of those commands is to ask a quick side question with full context. That's literally what a fork is for.

The auto memory dream consolidation feature uses forks for the same reason. It needs to look at everything that happened in the session before deciding what's worth saving. A blank subagent couldn't do that job.

So this is not just a new toy. It's a primitive Anthropic is building the rest of the product on. Knowing how to reach for it directly puts you ahead of where most people are using Claude Code.

---

## Two Efficiency Wins

There are two reasons forking is cheap, and they compound.

**No context re-processing.** The subagent doesn't have to spend tokens or time reading and understanding the situation. It already has it. Every detail the main session built up is sitting in the fork at message zero of its own life.

**Prompt cache hit on first inference.** This is the key technical detail. LLMs cache the processed form of prompts they've seen. Since a forked subagent has the identical context prefix as the parent and uses the same model, its very first inference call hits the cache immediately. That means near-zero latency and near-zero cost for loading the context.

Forked subagents make this cheap because delegation no longer has context-transfer overhead.

---

## The Cache Detail Most People Will Miss

Here's something that's worth understanding because it determines how much forking actually costs you.

A bare fork always uses the same model as the parent session. Always. Claude Code enforces this on purpose. If you're on Opus in the main session, every fork is on Opus. You can't override it for a bare fork even if you try.

The reason is the prompt cache. Anthropic's prompt cache is keyed per model. Opus to Opus can share cache. Opus to Sonnet cannot. So if a fork inherits a 200,000 token conversation, you don't pay full price to send those 200,000 tokens again. The cache covers it. The fork is mostly the cost of whatever new work it does.

This is engineered down to the byte. The fork path in Claude Code copies the parent's already-rendered system prompt verbatim, the parent's tool list verbatim, and the parent's model verbatim. Anything that diverges would bust the cache. So nothing is allowed to diverge.

That's why a 200k token fork is cheap. Not free, but a fraction of what you'd expect. And it's why you can spin up multiple forks in parallel without your bill exploding.

Named subagents like Explore are a different story. Those have their own system prompts and their own tools, so they can't share the parent's cache even when they happen to use the same model. Forks are special because they're literally designed to share.

[IMAGE: dark background, top half shows "Fork: Opus parent + Opus fork = shared cache" with a green checkmark and a stack of cached tokens flowing freely. Bottom half shows "Subagent: different system prompt = no cache" with a red X and a cache lock icon]

![[images/forked-subagents/cache-sharing.png]]

---

## Turning It On

You enable forks with an environment variable, or by adding it to your project settings.

```bash
CLAUDE_CODE_ENABLE_FORK_SUBAGENT=1 claude
```

Or drop it into `.claude/settings.json` so every session has it on by default. Once it's enabled, `/fork` becomes available in your slash command list. The command description reads "spawn a background agent that inherits the full conversation."

You can also ask the main session to spawn a fork directly. "Spin up two forked subagents, one to do X, one to do Y." Claude Code will fork itself twice and you'll see both running in the background panel, each starting at the parent's current token count.

---

## When to Fork

The decision is one question. Is the nuance of the main conversation useful to the subagent?

If yes, fork. If no, use a regular subagent.

Here are the patterns where forking earns its keep.

**Tangent containment.** You want to ask a side question that needs tools or multiple steps, but you don't want to derail the main conversation. Fork it. Get the answer back. If it's useful, integrate it. If not, the main session never had to deal with it. And you can always rewind to before the fork if the result was a dead end.

**Considering the opposing view.** Your main session has built up a working assumption. You want to stress test it without polluting your own thinking. Fork a subagent and tell it to argue the opposite. It has all the context, so it can argue specifically against the things you actually believe, not against a generic strawman.

**Noisy research with full context.** You need to search docs or run a bunch of MCP queries to verify something. Forking lets the search happen with awareness of where you are in the project, not just a stripped down prompt. The result that comes back is filtered by the full understanding the main session had.

**Parallel design variations.** This is the original problem. You want three takes on the same design and you want each take to know everything the main session knows. Fork three times in parallel. Each one gets all the nuance. None of them bias each other.

**Orient once, fan out many.** This is one of the most underrated patterns. You let the main session do the slow work of reading a folder, mapping the architecture, and orienting on a task. Then you fork five subagents, each one inheriting that whole orientation, and you split the actual work between them. Each fork starts with rich context the main session paid for once. None of them have to re-orient. You're amortizing the expensive setup across five parallel workers, and each worker is smarter than a regular subagent could ever be because it has the full picture, not a brief.

**MCP queries that need the conversation.** I have an Agentic Coding School MCP server. I can fork a subagent and ask it to recommend videos based on what we've been working on this session. The fork has the entire session. It searches the MCP. It returns the relevant videos. The main session stays clean.

[IMAGE: dark background, a 2x3 grid of use case cards: "Tangent containment", "Opposing view", "Noisy research", "Parallel design", "MCP queries", "Anything where nuance matters"]

![[images/forked-subagents/use-cases.png]]

---

## When Not to Fork

There's one pattern where a fork is worse than a normal subagent. Code review.

If you fork a subagent to review the code the main session just wrote, the fork has already seen itself write that code. It's the same Claude. It's going to be biased toward thinking the code is good, because some version of it just made the call to ship that code.

For a code review, you want a blank context. A fresh subagent that sees the diff cold and judges it on its own merits. The lack of nuance is the feature. You're paying for an outside opinion, and you can't get an outside opinion from a clone of yourself.

The same logic applies anywhere you need genuine independence. Adversarial verification, second opinions, anything where the value is "what would someone who hadn't been in this conversation think." Don't fork. Use a regular subagent and give it just the artifact, not the history.

---

## Parallel Decision Convergence

Once you internalize the difference, you can mix the two on purpose.

Spin up two subagents on the same question. One is a fork, one is a fresh subagent. The fork brings all your accumulated context. The fresh subagent brings naive eyes.

Where they agree, you have high confidence. Where they disagree, you've found the place where context actually shifts the answer. That gap is the interesting part. It tells you which beliefs in your main conversation are doing real work and which ones are biasing you.

This is one of the patterns I'm most excited about. It treats context itself as an experimental variable.

---

## Demo

The demo is a real workflow you'll recognize.

1. Open Claude Code in a project mid-conversation. Show the token count is already at 180k. There's real nuance here.
2. Type the prompt: "Spawn two forked subagents. One should make a Mermaid diagram of all the changes we made in this session. The other should use the Exa MCP to verify online that our approach is correct."
3. Show the background panel. Both forks immediately start at 180k tokens, not zero. That's the inheritance.
4. While they run, press escape and queue a follow up to one of them. "Use the light theme for the diagram." Show that you can talk to a fork mid run.
5. Verification fork returns. Show the result is specific and grounded in the actual decisions from the session, not generic web search noise.
6. Diagram fork returns with a Mermaid URL. Open it. Show the diagram captured the real work.
7. Then run a contrast. Same prompt, but spawn a normal subagent. Show the result is thinner, more generic, missing the nuance the fork picked up.

The viewer should walk away seeing the difference in output quality, not just understanding the concept.

---

## Key Insight

> Forking turns context into something you can copy on demand. The hard part of subagents was never the parallelism. It was the compression. Forks remove the compression and keep the parallelism.

---

## What Changes For You

You stop dreading the moment you have to delegate. You stop writing elaborate handoff prompts that try to cram the conversation into a brief. You just fork.

Once you've used it for a week, the question stops being "should I delegate this?" and starts being "should the delegate share my context, or should it not?" That's a much better question to be asking. And the answer changes everything about how you structure long Claude Code sessions.
