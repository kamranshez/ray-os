---
class: "multi-agent-orchestration"
chapter: "Subagents"
status: "idea"
---

# Subagent Teams

## Prep
- Read through this article on multi-agent teams: https://x.com/oikon48/status/2024515104969281785
- Watch: https://www.youtube.com/watch?v=dlb_XgFVrHQ

## Topics to Cover

### What & Why

- **What is an agent team** — An orchestrator (the "leader") that spawns and coordinates multiple teammate sub-agents. You have one leader who is the orchestrator and many different teammates. You can have any composition of teammates — it's essentially unlimited.
  - Video example: architecture agent + backend agent + frontend agent all coordinated by one leader. Another example: a writing team with a context gatherer, editor, and writer.
  - Visual cue: each sub-agent shows up with colored text in the terminal — that's how you can tell Claude Code spawned a sub-agent.

- **Sub-agents vs agent teams — the key difference**
  - **Sub-agents**: context is completely isolated/protected between the sub-agent and the main agent. The sub-agent knows nothing the main agent knows unless the main agent sends an initial seed of information. Its only job is to do side effects or send information back.
  - **Agent teams**: teammates talk to each other, coordinate with each other, and share a common task. The orchestrator can control any of the sub-agents. The way they share context is through messages to each other — you're not getting the full context from the orchestrator, just the messages. So if your sub-agents in your team don't have enough context, you need to ask the main agent to send additional context, or add more context into the tasks you're creating.
  - Video quote: "The most important difference between a sub-agent and the agent team is that the context is completely protected between the sub-agent and the main agent."

- **When to use which**: If you need quick results, use a sub-agent. If you need collaboration, use an agent team.

- **Agent teams cost more** — You're doing parallel work, so tokens scale linearly with how many agents you run simultaneously. If you're not already used to running multiple Claude Code instances, the usage might outpace what you're normally used to.

### Setup

- **Enable experimental agents setting** — Still in experimental stage as of the video. You need to change the `experimentalAgents` setting, then restart Claude Code. Pro tip: just paste the docs and ask Claude Code to set it up for you, then restart.

- **Define teams with natural language** — Just describe the team you want in plain English.
  - Video example: "I want you to create a performance agent team. One specializing in UI performance, looking for jank. Another specializing in debugging and deep diving into errors. And another that's a UX quality expert looking for pixel-perfect changes."
  - Claude Code creates the team automatically from that description.

- **Specify model per teammate** — Really useful if you're cost-sensitive or don't have unlimited tokens. You can assign different models to different roles based on how much capability they need.
  - Video example: "Make sure the debugger runs on Opus 4.6, the UI perf runs on Sonnet, and the UX quality runs on Haiku."
  - Note: changing models may require shutting down and recreating the agents. Still experimental — can be a bit buggy.

- **Display modes**:
  - **In-panel (default)** — All agents shown in a single terminal. You hit down arrow + enter to navigate between agents and see their output.
  - **Split pane** — Each agent gets its own pane. Requires tmux (`teamMode: "tmux"` in settings). Claims to work on iTerm too, but the video creator couldn't get it working even with all the setup. Best on a large monitor (e.g., 32 inch).
  - Both modes show the same information, split pane is just easier to monitor at a glance.

### How It Works — Task Coordination & Lifecycle

- **Everything operates around a task list** — Every time an agent team starts working, the orchestrator creates a task list and assigns tasks to teammates. Example: Task 1 assigned to researcher — "research GPT 5 release and gather writing context." Task 3 assigned to editor — "review the GPT 5 essay."

- **Context sharing is via messages, not full context** — Teammates send messages to each other with what is needed. They don't get the full conversation history. If agents lack context, you need to embed it into the task details.
  - Video tip: "If you want part of that context in your agent teams, the best way is to ask your agent team to include that into the task-specific details. You could say: 'Hey, I want to start working on the next set of projects but can you embed all of the important code pointers that I've gathered so far in this working session into my tasks so that my agent teams have good context.'"

- **Ctrl+T to view tasks** — Shows you the current task list, assignments, and status. Still a bit buggy — may take a few presses. You can see agents accepting tasks and sending messages to each other.

- **You can talk to any teammate directly** — Not just the orchestrator. You can guide any individual agent, give it additional tasks, or tell it to keep working on the next task. They're just Claude Code instances.
  - Video example: when an agent goes idle, you can say "after this, also quickly build a cool flare when someone hits the login button."

- **No polling needed** — Teammates automatically receive messages and automatically stop when done. The lead gets notified when teammates complete. You should mainly be watching the orchestrator — technically you don't need to go to the individual agents.

- **Agents auto-shutdown when idle** — After they're done and idle for a while, Claude Code turns them off automatically (they appear grayed out in the UI). The orchestrator handles this.
  - Important: agents don't persist between invocations. If you're someone who likes to build up context in a single Claude Code instance over time, agent teams might not be the best fit.

- **Let the orchestrator handle cleanup** — Don't manually kill teammates. The docs say you can get into weird states and possibly memory leaks if you don't let the main orchestrator shut them down. (Worst case, just restart your computer.)

- **Hooks: `teammate_idle` and `task_complete`** — Additional hook events for the agent team lifecycle. You can trigger actions when these events happen.
  - Video speculation: someone will find cool uses — e.g., `task_complete` sends a notification to Notion, Jira, or Slack. No killer use case found yet by the video creator, but the hooks are there.

- **Team fully shuts down with a summary** — When all agents are done, the team shuts down and gives you a summary of what was accomplished.

### Best Practices

- **Always start with a plan before implementation** — Plan mode is essential for agent teams. If you like to use Claude Code without plan mode and just do straight execution, agent teams is not for you. Work with the main agent to create a proper task plan before spawning teammates.
  - Video approach: plan out a bunch of things ahead of time, save the task list locally, then when you want to work on it, just say "what do I have to do next?" and kick off the agents.

- **Guidance trickles down** — Tell the orchestrator your quality bar, constraints, and preferences. It propagates to all teammates.
  - Video example: "Make sure you have a very high quality bar for all of the code. Tell all of the sub-agents to have this high quality bar."
  - Note: sometimes these changes (like model changes) will cause the agent team to shut down and recreate.

- **Teammates load CLAUDE.md and MCP servers but NOT conversation history** — Whatever context you built up before starting the agent swarm, the teammates won't have it. You must explicitly embed important context into the task details for the agents to use.

- **Start with 3-5 teammates max** — Anything more than 3 feels overkill in practice. Tokens scale linearly, and 3-4 agents is the sweet spot. You'll find use cases for more, but start small.

- **5-6 tasks per agent at a time** — Don't overload agents with too many tasks at once. It's fine to plan out many subtasks, but kick off a batch, let them finish, regroup, then start the next batch. Ask the orchestrator to delegate work in proper amounts — load balance it.
  - Video quote: "It's kind of like project management and you're literally orchestrating a team of engineers. A lot of the best practices that you would do for regular teams kind of apply here."

- **Don't let agents touch the same files** — This causes conflicts. Really think about this when creating your teams. It only works well if you have clearly separated domains (e.g., frontend and backend in different directories).

- **Git worktrees + agent teams didn't work well** — Because all agents are trying to work on the same high-level task at once, worktrees don't help much. Only useful if agents are truly independent.

- **Sometimes the leader starts implementing instead of delegating** — You need to guide it: "Stop, delegate this out to your teams" or "Wait for your teams to complete their task before starting." This is an experimental-stage quirk.

- **Monitor and steer agents periodically** — If you let them run too long unguided, they can go off the rails and waste tokens. Constantly monitor them.
  - Video quote: "You still want to monitor and steer their agents from time to time. If you have these things run too long, unguided, it can just go off the rails and then you could be just wasting a lot of tokens."

### Use Cases

- **Full-stack development** — Frontend, backend, and architecture agents working in parallel. Claude Code even created multiple frontend agents when it recognized work was in different places. Really speeds up execution.
  - Video example: architecture agent + backend agent + frontend 1 + frontend 2 + frontend 3 (though multiple frontends touching the same pages can conflict).

- **Writing** — Context gatherer, editor, and writer agents. The editor scores things and does edits. The context gatherer pulls from local vector memory. The writer composes. Before agent teams, these had to be done sequentially — now they happen in parallel and help each other (e.g., the writer might trigger the context gatherer to fetch context for a specific section mid-writing).

- **Multi-perspective code reviews** — Security agent, performance agent, test coverage agent — each reviews the same code from their angle, then combine into one holistic review. This avoids the bias problem where a single agent doing all three gets influenced by the first review it performs.
  - Video prompt: "Let's do a code review on the latest changes. I want one focused on security, one on performance, one on test coverage. Combine the results into one really good review."

- **Competing hypothesis debugging** — When you have 5 theories about a bug, spawn 5 agent teams instead of investigating one-by-one. Context isolation protects each agent from being biased by the others' findings. Then they share notes and the main agent makes a holistic picture.
  - Video quote: "As soon as it gets some part of the context that it thinks is true, the agent will lean towards thinking that it's correct. Using sub-agents to protect the agent from each other — because their context is split — helps them investigate on unbiased."

- **Cross-platform parity** — e.g., Android/iOS. If both platforms share architecture, a parity agent reads the other platform's code and creates matching tasks, then an executing agent builds the feature. "Probably one of the most efficient way to have feature parity work, as long as the architecture is the same."

- **Read-only exploration first** — Start with read-only tasks for parallel exploration (avoids file conflicts). Debugging agents and research/context-gathering agents are naturally read-only and great for this.

### Anti-patterns

- **Don't use agent teams for purely sequential work** — If tasks must happen one after another, you don't get the parallelism benefit and can cause conflicts (like frontend 1, 2, 3 all editing the same pages).
- **Don't spawn multiple agents that edit the same files** — They'll conflict. Think carefully about domain separation when designing your teams.
- **Don't skip plan mode and jump straight to execution** — Agent teams need a plan. The orchestrator needs to know what to delegate.
- **Don't let agents run too long unguided** — They go off the rails and waste tokens. Monitor and steer regularly.
- **Don't manually kill teammates** — Let the orchestrator handle shutdown to avoid weird states and memory leaks.
