---
class: "fundamental-techniques"
chapter: "Session & Context Management"
status: "scripted"
aliases: [clis-vs-mcps]
---

You installed an MCP server because it was convenient. It might be quietly tripling your token bill.

This video is about a single decision you make every time you connect a tool to your agent: do you reach for an MCP server, or do you just let the model use the command line? Most people default to MCP because it feels modern. For a huge class of tools, that default is the expensive choice.

The rule is simpler than the debate makes it sound. **CLI for what the model already knows. MCP for genuinely new integrations.** Once you understand why, you will stop installing MCPs out of habit.

---

## The hidden cost of an MCP

Here is the part nobody tells you when they hand you a one-click MCP install.

Every tool an MCP server exposes ships a schema. A name, a description, every parameter, every type. That schema gets loaded into your context window. And it does not load once. It sits in the window for the rest of the session, re-sent on every single turn.

The GitHub MCP alone costs roughly 60,000 tokens before you have done anything at all.
Source: https://www.youtube.com/watch?v=RtXpXIY4sLk

That is the floor, not the ceiling. Connect three or four servers and you can burn a quarter of your context window on tool definitions for tools you might not even call. Every one of those tokens is also noise. The model now weighs every schema against every other token while it tries to reason about your actual task.

[IMAGE: dark background, left panel labeled CLI showing an empty context window with a small "gh" chip, right panel labeled MCP showing a context window stuffed with stacked schema cards before any work starts, both feeding into the same model]

![[clis-vs-mcps-context-cost-1.png]]
![[clis-vs-mcps-context-cost-2.png]]
![[clis-vs-mcps-context-cost-3.png]]
![[clis-vs-mcps-context-cost-4.png]]
![[clis-vs-mcps-context-cost-5.png]]

There is a line from the BoundaryML team that captures it: every single function definition in an MCP server is an instruction. Load fifty of them and you are never going to get good results.

---

## Why a CLI costs almost nothing

Now flip it. Why does the command line avoid this tax?

Because the model already knows the command line. `git`, `gh`, `npm`, `docker`, file operations. These were all over the training data, man pages and all. The model does not need a schema to learn what `gh pr list` does. It learned that years ago.

So you pay zero context to make those tools available. If you are already signed in locally, there is no reason to wrap a tool the model can already drive.

And a CLI gives you three things an MCP cannot:

**The agent controls what enters its own context.** This is the big one. With a CLI the agent can pipe the output into a Python script, grep it, pass it through jq, slice out the three fields it actually needs, and write the rest to a file. The raw 10,000-line dump never touches the window. The agent decides what is worth keeping and discards the rest before it costs a single token. An MCP response does not give you that choice. It comes back into context whole, whether you want it there or not.

That flexibility is the real unlock. The agent is not just calling a tool, it is writing code around the tool. It can filter, reshape, and summarise data programmatically, then surface only the answer. You get the full power of the shell and a scripting language sitting between the data and the context window.

[IMAGE: dark background, left-to-right flow. CLI terminal on the left emits a tall messy dump labeled "10,000 lines". It passes through a code filter funnel in the middle (a small box showing grep / jq / python). Two outputs: a tiny clean result labeled "the answer" flows into a context window box on the right; a big discarded pile branches off to a file icon labeled "written to file, never enters context"]

![[clis-vs-mcps-agent-control-1.png]]
![[clis-vs-mcps-agent-control-2.png]]
![[clis-vs-mcps-agent-control-3.png]]
![[clis-vs-mcps-agent-control-4.png]]
![[clis-vs-mcps-agent-control-5.png]]

**You can chain.** The output of one command flows into the next. No round trip through the model for each step.

**You can stream.** Pair a CLI with a tool that tails output and you get live logs, monitors, long-running watchers. Streaming data that an MCP request-response shape simply cannot give you.

This is also your escape hatch for a badly designed MCP. If a server dumps huge responses into your context, you can often wrap the same underlying API in a tiny CLI that prints exactly what the model needs, and nothing else. You control the output format. Humans need pretty tables. The model needs terse, token-efficient text. A CLI lets you print for the model.

One more thing in the CLI's favour: the agent is good at teaching itself. Point it at a CLI it has never seen and it will often just run the help command, read the usage, and work out the flags on its own. No schema required. It discovers the interface at runtime.

The catch is that the help dump lands in your context. So if you call the same CLI over and over, capture how to use it once in a skill. Then the agent reads the compact skill instead of re-running help every session, and the usage noise stays out of your main context window. It is the same move again. You decide what is worth keeping, instead of an MCP shoving its whole schema into your main context whether you use it or not.

---

## The numbers

You do not have to take this on faith. Someone benchmarked it.

The AXI study ran the same 17 GitHub tasks through a raw `gh` CLI and through the GitHub MCP, graded by an LLM judge, five repeats each.
Source: https://github.com/kunchenguid/axi/blob/main/bench-github/published-results/STUDY.md

- The CLI averaged 5 cents per task. Every MCP variant cost 10 to 15 cents per task. That is 2 to 3 times more.
- The gap is almost entirely context. MCP schemas pushed average input tokens to between 137,000 and 176,000. The CLI sat around 46,000 to 47,000. You pay for those schemas on every turn.
- Lazy loading the schemas did not save money. It trades a smaller starting context for one or two extra discovery turns per task, and each turn re-sends the whole growing context. It landed at the same cost and had a lower success rate.
- The CLI also won on reliability and speed, not just cost.

[IMAGE: dark background, two horizontal bars, CLI bar short labeled "5c / 46K tokens", MCP bar 3x longer labeled "15c / 176K tokens", same task underneath both]

![[clis-vs-mcps-benchmark-1.png]]
![[clis-vs-mcps-benchmark-2.png]]
![[clis-vs-mcps-benchmark-3.png]]
![[clis-vs-mcps-benchmark-4.png]]
![[clis-vs-mcps-benchmark-5.png]]

One study, one MCP. A lean, well-designed server narrows the gap. But the direction is clear: wrapping something the model already knows how to drive from the command line can quietly 2 to 3x your bill.

If you cannot drop the MCP, there is a middle path. Instead of calling MCP tools directly, have the agent write code that calls them. Anthropic measured this pattern dropping token usage from 150,000 to 2,000 on one workload, because the tool definitions live in a file the agent reads on demand instead of sitting in context.
Source: https://www.anthropic.com/engineering

---

## So when do you actually want an MCP?

This is not "MCPs are bad." MCP earns its keep for genuinely new integrations, the things the model was not trained to drive from a terminal. Slack, Notion, Linear, your own internal apps.

Eric Zakariasson uses both every day and frames the split cleanly.
Source: https://x.com/ericzakariasson/status/2066570396183548350

> cli for stuff the model already knows. git, gh, npm, docker, file ops. trained on man pages, and costs almost nothing in context. if im already signed in locally theres no reason to wrap it in anything
>
> mcp for most integrations. slack, notion, linear, twitter

The other thing MCP buys you is the protocol itself, and the auth story is genuinely smoother. Add one server to your team and everyone gets access. With something like Claude's connectors you authenticate once against your Claude account, and then every device you log into with Claude is authenticated automatically, locally and in the cloud. You do have to re-auth occasionally, but most of the time it just works. A raw local CLI does not give you that. You set it up per machine.

So the deciding question is not "which is newer." It is two questions:

1. Was the model trained to drive this tool already? If yes, the CLI is free.
2. Do I need team auth, persistence, or a shared integration? If yes, the MCP is worth the context.

[IMAGE: dark background, decision fork. Top node "New tool to connect?" splits into two paths. Left path "Model already knows it (git, gh, npm)" leads to a CLI terminal icon. Right path "New integration + team auth (Slack, Linear)" leads to an MCP server icon]

![[clis-vs-mcps-decision-1.png]]
![[clis-vs-mcps-decision-2.png]]
![[clis-vs-mcps-decision-3.png]]
![[clis-vs-mcps-decision-4.png]]
![[clis-vs-mcps-decision-5.png]]

Personal and already-known, reach for the CLI. New integration shared across a team, reach for the MCP.

---

## Demo

1. Start a fresh session and run `/context` with the GitHub MCP connected. Show the token cost of the schemas sitting in the window before a single task.
2. Disconnect the MCP, restart, run `/context` again. Show the window is nearly empty.
3. Give the same task to both: "list the open PRs and summarise the failing checks." MCP version versus `gh pr list` plus `gh pr checks`. Compare turns, tokens, and the final answer.
4. Show the output trick: pipe `gh` output to a file and have the agent read the file, so the raw JSON never enters context.
5. Show the Bento CLI as a custom example. A tiny wrapper that prints exactly what the model needs, token-efficient, no schema tax.

---

## Key Insight

> An MCP loads every tool's schema into your context and re-sends it every turn. For tools the model already knows from training, the command line gives you the same power for free, plus chaining, streaming, and output you can keep out of the window entirely.

---

You do not need to rip out your MCPs. You need to stop installing them on autopilot. Before you connect the next one, ask whether the model already knows the tool. If it does, the cheapest, fastest, most reliable option was the command line the whole time.
