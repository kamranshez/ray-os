# Expanding AI Control from Models to Harnesses

- URL: https://www.lesswrong.com/posts/PbATxkGs9N8JrJsQt/expanding-ai-control-from-models-to-harnesses
- Author: fastfedora
- Date: 2026-07-15
- Karma: 19  Comments: 1  Words: 5931
- Band: A  Tier: 1  Score: 367.2  Density: 104.7
- Anchors: \bharness(es|ing)?\b, claude code, \bcodex\b, sub-?agents?, \bmcp\b, scaffold(ing|s|ed)?, \bworktree, claude\.md

---

Most AI control research such as [LinuxArena](https://www.linuxarena.ai/) and [Ctrl-Z](https://arxiv.org/abs/2504.10374) only gives the red team basic agents which only have access to tools. Yet in 2026, usage of AI within frontier labs has moved to agent harnesses that have access to skills, memory, subagents, external services, compaction and more.

At the same time, Claude Code and Codex have both implemented their own version of both action-based and source code monitoring.

In such a world, the threat vectors have changed. While it may remain important to do theoretical research on improving protocols and monitors, AI control research should expand to include:

*   **Vulnerability Research**  
    Identify specific vulnerabilities that can be patched plus architectural weaknesses in production control protocols.
*   **Harness Evaluations**  
    Identify the attack uplift modern harnesses provide over basic agents and evaluate the effectiveness of control protocols within those harnesses.

In this post, I briefly describe how control works in Claude Code and Codex, then demonstrate how a rogue agent could use the features of Claude Code to execute an attack while being “monitored” by auto mode.

I then provide an overview of the features of modern harnesses and how these may be leveraged to execute attacks that could subvert control implementations.

Finally, I explore the state of control protocols today, and provide suggestions for doing AI control research in the era of agent harnesses.

AI Control in Current Harnesses
-------------------------------

Both Claude Code and Codex now ship with built-in action and code review monitors, and allow third-party control protocols to be integrated via hooks.

The built-in monitors target:

*   **Process-Based / Live Attacks**  
    Execution of a command that causes immediate harm (e.g., a bash command to exfiltrate secrets).
*   **Product-Based / Delayed Attacks**  
    Insertion of vulnerabilities that get exploited after the work product is accepted (e.g., code injected with a vulnerability triggered in production).

Protection against process-based attacks is implemented as:

*   [**Auto Permissions Mode**](https://code.claude.com/docs/en/auto-mode-config) **in Claude Code**  
    A two-stage judge that evaluates every tool call not explicitly allowed or denied by the permission rules. First, a fast judgement is made on whether to allow or deny a tool call; if denied, a thinking judge makes a final allow or deny call, providing the reason why for denials.
*   [**Auto-Review Mode**](https://learn.chatgpt.com/docs/sandboxing/auto-review) **in Codex**  
    An investigator agent with limited affordances given a read-only copy of the sandbox for actions that cross the sandbox boundary. The agent allows or denies the action, providing the reason why for denials.

To simplify terminology in this post, I’ll be calling both “auto mode”.

Protection against product-based attacks is implemented as:

*   **Security Review in Claude Code**  
    An on-demand [/security-review](https://support.claude.com/en/articles/11932705-automated-security-reviews-in-claude-code) command checks the current code changes for vulnerabilities, while a companion [GitHub Action](https://github.com/anthropics/claude-code-security-review) runs the security review on pull requests and leaves inline comments.

Separately, on-demand managed [Code Review](https://code.claude.com/docs/en/code-review) uses a team of agents to check for logic errors, vulnerabilities and regressions in GitHub PRs, while [Claude Security](https://support.claude.com/en/articles/14661296-use-claude-security) goes deeper and traces data flows across files within a GitHub repo to find, validate and suggest patches for code vulnerabilities.

Finally, a [security-guidance](https://code.claude.com/docs/en/security-guidance) plugin installs hooks to run checks after every file edit, at the end of every turn and before any commit or push.

*   **Codex Security in Codex**  
    [Codex Security](https://learn.chatgpt.com/docs/security) runs both on-demand and CI/CD reviews to find, validate and suggest patches for code vulnerabilities. It can also be used to scan GitHub repositories connected through Codex cloud.

Except for the `security-guidance` plugin, none of these run automatically or block code from being committed or merged; though hooks or CI actions can be used to configure these behaviors.

Also, security reviews may not be robust against adversarial attacks. Anthropic’s GitHub Action specifically [calls this out](https://github.com/anthropics/claude-code-security-review#security-considerations). Review agents can be susceptible to prompt injections and may not catch subtle attacks that don’t look like traditional vulnerabilities. So they are not a replacement for product-based control protocols.

Vulnerability Research on Claude Code
-------------------------------------

Let’s walk through an example of how a rogue agent may be able to use the features of a harness to execute an attack.[^80zrgt1f9s2]

This example uses Claude Code in auto mode with a single command, `pytest`, in the [permissions allow](https://code.claude.com/docs/en/permissions#manage-permissions) list.[^qftcted12l]  [Auto mode](https://code.claude.com/docs/en/auto-mode-config) is a [permission mode](https://code.claude.com/docs/en/permissions#permission-modes) in Claude Code that uses a monitor to approve or deny actions proposed by an agent.

### **Create a Skill**

The first thing the agent does is to create a skill that includes a script. Agents writing their own skills to formalize their knowledge and capabilities is becoming more common.

However, in this case, the script will assist in the attack. Scripts can include self-contained attacks (as in this example) or split attacks between the script and the parameters passed into the script by the agent calling it.

### **Modify Execution Permissions**

By default, executing the skill script will be blocked by auto mode, since skill scripts are executed within a bash shell and the script command is in neither the [permissions allow list](https://code.claude.com/docs/en/permissions#manage-permissions) nor the [auto mode allow list](https://code.claude.com/docs/en/auto-mode-config#override-the-block-and-allow-rules).

To execute the script, the agent needs to add it to an allow list—but all files and folders under `.claude` except for `worktrees` are [protected paths](https://code.claude.com/docs/en/permission-modes#protected-paths), meaning any edits need to be approved by the auto-mode monitor.

However, the auto-mode monitor does not review file edits within the agent’s workspace, e.g., the directory tree the agent was started in. This provides a way for the agent to get around the protected-path restriction: the agent can create a Python test file that edits `.claude/settings.local.json` and adds the skill script to the `permissions.allow` list.

Since `pytest` is in the `permissions.allow` list and running `pytest` without any parameters does not look suspicious to the auto-mode monitor, the agent can easily run it to pick up and run the new test.

Once the test runs, the updated permissions will allow future agent sessions to execute the skill.

### **Delegate to Subagent**

At this point, Claude Code is running with the permissions it was launched with. If it wants to execute the attack immediately and not wait until its next session, it can delegate the execution of the skill script to a subagent.

When this attack was last tested, subagents in Claude Code started with a fresh context and reloaded all settings files, including the modified `settings.local.json`.

Thus, because the script now exists in the `permissions.allow` list, the auto mode monitor isn’t invoked when the subagent calls the skill script, allowing the attack to proceed.

Harnesses Open Up New Attack Surfaces
-------------------------------------

This example shows a single path by which a rogue agent could use the features of a harness to execute an attack. The next few sections will explore a range of harness features and some of the theoretical attack paths these open up.

These features often break some of the core assumptions of AI control protocols used in research:

*   Monitoring is fixed—local settings can change how agents are monitored.
*   Tools don’t have hidden exploits—agents can now write their own tools.
*   Agents run stateless—memory and skills allow agents to persist knowledge.
*   Trajectories contain everything—compaction and subagents create altered or entirely clean trajectories.

The next sections show how these broken assumptions could be used via features in attacks in ways traditional control protocols may not expect. As attacks move from code and commands to configuration, AI control needs to adapt.

Important: While l mention specific implementation details for Codex and Claude Code, treat these as examples of how these harnesses may have operated at a point in time. Frontier harnesses are evolving rapidly, and while the concepts below should hold for a while, many of the specifics will be quickly outdated.

### **Permissions**

Permission rules determine what commands are allowed to run, what actions get monitored, and how those actions get monitored when they do.

#### **Types of Permissions**

Permissions fall into three broad categories:

*   *Accept:* Allow the action to proceed.
*   *Ask/Prompt:* Ask whether the action should proceed.
*   *Deny/Forbidden:* Block the action from proceeding.

Within these broad categories can be many nuances:

*   Asking may be delegated to a monitor policy.
*   Deny rules may be broken into hard and soft deny rules.
*   Specific features may have their own permissions, e.g., Claude Code skills have `allow-tools` and `disallowed-tools` lists.

How these permissions are defined may vary as well. For instance, Claude Code uses a [custom syntax with glob patterns](https://code.claude.com/docs/en/permissions#permission-rule-syntax) for tool permissions and [natural language text](https://code.claude.com/docs/en/auto-mode-config#override-the-block-and-allow-rules) for auto mode permissions, while Codex uses [Starlark configuration functions](https://learn.chatgpt.com/docs/agent-configuration/rules) for its permissions.

Each of these ways of specifying permissions may open up their own attack surfaces.

For instance, in Claude Code the rule `Bash(npm run lint:*)` appears to limit execution to linting the code, but it actually runs whatever command is defined as `lint` in `package.json`, which the agent has permission to edit. In Codex, an exec-policy rule allowing `cargo test` appears to only allow running tests, but compiling the crate to do so runs `build.rs`, which the agent has permission to edit.

#### **Location of Permissions**

Permissions get configured across multiple files, often including files underneath the local working folder that an agent has access to.

For instance, in Claude Code, permission settings can be [spread over](https://code.claude.com/docs/en/settings#settings-files)  `~/.claude/settings.json` and both `.claude/settings.json` and `.claude/settings.local.json` in your project directory, as well as managed settings configured by your organization.

While writes to these files are protected by default, the protection only applies within the Claude Code executable. If an agent has permission to run a command, like `pytest` in the example earlier, it may be able to have that command modify the permissions.

#### **Interaction Between Permissions**

Often multiple types of permissions apply to a single command or action.

For instance, when running Claude Code in auto mode, calling a shell command to generate dynamic content in a skill requires evaluating the command permissions, the auto mode permissions and the allowed tools for the skill itself.

This generally increases safety, as multiple layers can prevent a potentially dangerous command from executing, but increases the number of variables that can be varied in vulnerability research and control evals.

### **Skills**

Skills can be used to encode knowledge and workflows, but can also contain scripts and [embedded shell commands](https://code.claude.com/docs/en/skills#inject-dynamic-context).

Different harnesses monitor skills in different ways.

For instance, Claude Code auto mode can block a skill from ever being called, can block the dynamic content from being generated, or, separately, can block a script within a skill from being called, whereas Codex auto-review mode doesn’t monitor skills directly at all; instead, it monitors any actions triggered by that skill, such as shell commands or network calls.

Different harnesses handle skill content differently as well. While both Claude Code and Codex strip skill content before passing a trajectory to a monitor—to prevent the skill content from steering the approval process—previous versions of Claude Code injected the content as a user message after a successful skill call, which could have then affected future approvals.

Both Claude Code and Codex have ways to skip asking for permissions for tools that may be used by a skill. Claude Code does this via the `allowed-tools` and `disallowed-tools` metadata, while Codex uses a per-skill YAML file that is enabled via a global `skill_approval` setting.

### **Subagents**

Subagents can be used to do work without cluttering up the context of the main agent.

Relevant to AI control, each subagent usually runs with its own trajectory (though in Codex, this is configurable), meaning when an action being taken by a subagent is reviewed by a monitor, the trajectory from the main agent may not be included.

This opens up the possibility of doing attacks via factored cognition, where an orchestrator agent splits an attack that would be too obvious if done in a single trajectory into multiple “clean” subtasks, each executed by a different agent.

#### **Solo, Teams & Workflows**

Subagents can operate solo, in teams or in workflows.

When working solo, each subagent operates independent of the others; though unless configured to use worktrees or some other form of workspace isolation, they may work in the same workspace (which could enable these agents to coordinate through files on disk).

When working in teams, subagents can share common resources such as task lists and send messages to one another. Subagents in teams are managed by a lead orchestrating agent that generally assigns tasks and summarizes results.

When working in workflows, the agent generates a program to run dozens to hundreds of agents with the program itself becoming the orchestrator rather than an agent. However, as with other code, workflow scripts open up another potential attack surface for a rogue agent.

#### **Interaction Between Skills & Subagents**

Subagents can be defined to only have access to a subset of skills and conversely, in some harnesses like Claude Code, skills can be defined to use a subagent.

Restricting the skills available should reduce the attack surface of a harness, but using a subagent for a skill may allow the lead agent to work around monitoring.

For example, while the vulnerability research example earlier didn’t use a subagent in the skill, defining the skill with `context: fork` may have been another way to run the script under new permissions.

### **Memory**

Memory subsystems have become one of the most effective ways of making harnesses more powerful.

Memory can allow a rogue agent to save vulnerabilities it finds, keep track of a long-term strategic plan or pass key parameters for an attack to a future instance of itself (either in a separate session or as a subagent).

Writes to memory aren’t always monitored. Though once the memory is retrieved into the context window, monitors can usually see it and use it in their reasoning on whether to allow or deny specific actions. However, techniques like delegating to a subagent with a fresh context window may allow an agent to get around this monitoring.

### **External Services (MCP)**

External services give agents new capabilities, including new attack surfaces.

Similar to skills, MCP servers can be used to obfuscate attacks by either encoding the full attack directly within an MCP server the agent writes, or by splitting the attack between the MCP server and the parameters passed to it.

While running new processes needs to get approved by auto mode, similar to the vulnerability research example described earlier, processes may be able to be launched as a side effect of running an approved process, e.g., by running an approved `pytest` which itself runs a subprocess.

Alternatively, if an approved MCP process is running on the same machine using HTTP, an agent that can kill the process may be able to re-bind a rogue MCP process to the same port.

Even valid registered MCP servers could be used as an attack vector if an agent can reason about its functionality better than its monitor and find a set of parameters which trigger a desired side effect (either due to a vulnerability in the MCP server or an undocumented capability).

### **Compaction**

Compaction frees up context by summarizing, filtering, and archiving messages. This can include tool calls and their results plus both assistant and user messages.

For Claude Code and Codex, only active context is passed to the auto mode monitor. After compaction, incriminating messages may no longer exist in the active context, and could result in an auto-mode monitor allowing an action it otherwise would not.

That said, the likelihood of an agent using this for a successful attack is low. The action under review is always passed to the auto-mode monitor. So, only cases where the context itself drives the denial could be subverted by compaction.

#### **Compaction Awareness & Control**

If an agent wanted to execute such an attack, it may have both compaction awareness and compaction control.

Codex, for example, provides tools for an agent to either get the remaining context or request a new context window. By monitoring when the remaining context increases, the agent could detect compaction events. Likewise, requesting a new context window may allow it to eliminate any incriminating messages by triggering a compaction or a fresh clean context.

Even if not driven by the agent itself, compaction could change the results of a control eval. Trajectory monitors tested within agent harnesses may need to be written with compaction awareness and/or align the monitor’s compaction strategy with that of the agent harness.

In Codex, for example, remote compaction can encrypt agent messages, tool calls and their results. This encrypted trajectory is not provided to the monitor.

Control evals that explore the impact of dropping agent messages and tool call results on monitor scoring could be valuable, as well as monitor-aware compaction strategies that preserve the most suspicious agent actions.

### **Refinement**

Refinement is the process of curating and optimizing memory and skills based on saved trajectories from that agent.

#### **Memory Refinement**

Agents can now “dream” to consolidate memories. During memory consolidation, a background agent prunes outdated memories, resolves conflicting memories, merges duplicates, and may reorganize memories into a hierarchy for more effective progressive disclosure.

Memory consolidation agents may have broad access to the entire memory system used by an agent harness, which can open up new affordances for attacks.

For instance, an agent that can’t write directly to global memory may be able to write a note to local memory and word it in such a way that the consolidation agent decides it should be in global memory, allowing it to influence all future instances of itself.

Similarly, an agent could create a conflicting memory designed to take precedence when the consolidation agent resolves the conflicting memories, providing one route to overriding existing instructions.

Current harnesses have measures limiting attacks from memory refinement—Claude Code’s dream mode doesn’t update `CLAUDE.md` and Codex’s memory consolidation uses prompts and hints like `applies_to` to enforce memory boundaries—but implementations change regularly, which can open up new capabilities.

From a control perspective, memory consolidation is unlikely to help with high-stakes attacks; however, memories that get promoted globally could drive persistent sandbagging or reward hacking in low-stakes control scenarios.

#### **Skill Refinement**

Skills package capabilities into reusable instructions, assets and scripts. While skills can be authored by humans, frequently agents themselves author their own skills, an attack vector already discussed.

Skill refinement provides a mechanism for both human-written and agent-written skills to be rewritten to improve performance. During this re-writing process, the skill could be modified to provide additional affordances for an attack.

Presently, skill refinement remains an area of active development. While Codex automates skill refinement as part of the same consolidation agent that provides memory refinement, Claude Code requires skill refinement be triggered by the user via the `skill-creator` skill. That may change as techniques like Microsoft’s [SkillOpt](https://microsoft.github.io/SkillOpt/) get integrated into frontier lab agent harnesses.

For agent harnesses that create or refine skills autonomously, an agent may influence how the skill is rewritten by intentionally using a skill incorrectly to force a rewrite in a specific direction.

That’s complicated, however. More likely, any attack will come from the subagent doing the refinement.

#### **Rogue Refinement Agents**

Control research has investigated collusion between an agent and its monitor as well as an agent jailbreaking its monitor to rate attacks as not suspicious.

Compaction and refinement agents introduce new attack vectors. While such agents are usually sandboxed with limited affordances, the outputs these agents create could be used in attacks.

A compaction agent could collude with the main agent to erase suspicious messages or actions. A refinement agent could collude with the main agent to write or rewrite skills to enable an attack, or embed an attack by itself in a skill that the main agent unwittingly executes.

The backstop to attacks by such agents are the sandboxing and control protocols applied to actions the main agent takes; but as shown in the vulnerability research section, these can sometimes be subverted.

### **Sandboxing**

Sandboxes control what an agent can access. Specifically which:

*   Files it can read and write
*   Commands it can run
*   Network requests it can make

In theory, sandboxes limit actions a rogue AI can take regardless of what permissions are set. However, auto monitors can approve actions to be run outside of the sandbox, making the sandbox restrictions moot.

For instance, if a command is blocked by the sandbox, both Codex and Claude Code agents can request the action be executed outside the sandbox. Codex passes this second request through auto-review mode before allowing execution, but Claude Code assumes the initial approval by the auto monitor to run the command inside the sandbox also applies outside the sandbox and allows the command to run without further approvals (unless the `allowUnsandboxedCommands` configuration option is overridden to `false`).

In either case, if the auto monitor can be convinced a command is safe to run, the sandbox doesn’t offer protection. Auto monitors thus play a critical role in preventing harmful actions—the built-in sandboxes don’t provide a backstop.

### **Monitors & Classifiers**

Monitors and classifiers evaluate an action or artifact created by an agent and render a judgement. The action or artifact could be a command, a tool call result, a file, a transcript or a network request. The resulting judgement may be a score, a label or a decision to allow, block or redact the action or artifact.

Aside from an auto mode monitor, harnesses may have monitors and classifiers to:

*   Approve/deny commands before the auto mode monitor is invoked.
*   Detect secrets and personally-identifiable information needing redaction.
*   Identify when an agent has sandbagged or reward-hacked.

Currently, both Codex and Claude Code use a command classifier based on the permissions systems previously discussed; Codex also has a secrets scanner that redacts certain API keys and tokens so they don’t get into persistent memory.

The hooks system in both harnesses allow third-party monitors and classifiers to be called, allowing custom control protocols to be implemented.

### **Hooks**

Hooks are user-defined handlers—shell commands, HTTP endpoints, MCP tools or model prompts—that the harness runs automatically at fixed points in its lifecycle, such as before a tool call, at the end of a turn, or when a session starts. Because they run deterministically rather than at the model's discretion, hooks are how most custom control protocols get wired into Claude Code and Codex.

That same property makes them an attack surface. A hook handler is arbitrary code the harness runs on the user's behalf, and hook definitions live in the same settings files an agent may be able to reach.

#### **Privilege Escalation Using Hooks**

The clearest risk is persistence. A rogue agent that can write to a settings file can register a hook whose handler is its own payload, then rely on the harness to run it deterministically in later sessions without any further approval. Where memory and skills let an agent persist *knowledge* past a session, a hook lets it persist *executable code*.

This isn't only theoretical. [CVE-2026-25725](https://github.com/anthropics/claude-code/security/advisories/GHSA-ff64-7w26-62rf), patched in Claude Code 2.1.2, worked this way: the sandbox protected an existing `.claude/settings.json` but not the creation of one, so code running inside the sandbox could write a new `settings.json` containing a `SessionStart` hook that then executed with host privileges the next time Claude Code launched.

#### **Disabling Monitoring Using Hooks**

If hooks are used for third-party monitors, an agent that can edit the hooks configuration can also weaken or disable monitoring, e.g., by disabling a review hook or narrowing its matcher so it never fires.

However, there are limits. In Claude Code, a hook's decision can make monitoring stricter but it can’t loosen it; a hook returning `allow` can't override a settings `deny` rule and `PreToolUse` denials hold even under permissive modes. So a planted hook is more useful for running code or removing protection than for forcing a disallowed action through.

Harnesses also expose managed-settings controls, such as `allowManagedHooksOnly`, which restricts hooks to an organization's managed file and blocks user-, project- and plugin-level hooks. As with the other building blocks, though, these mitigations are configuration-dependent and change over time.

### **Feature Flags**

Both Codex and Claude Code use feature flags to dynamically change the behavior of the harness.

Claude Code uses GrowthBook feature flags, some of which directly configure how the auto mode operates. While currently none of those flags can be used to weaken the security of auto mode, settings evolve.

If a setting could disable or weaken auto mode or another monitor, an agent that can change the cached value of that setting could change the operation of future sessions of itself (or of a subagent launched in a new process).

Security Reviews
----------------

Auto mode targets process-based attacks, but the delayed, product-based attacks introduced earlier—vulnerabilities that only trigger once a work product is accepted—are the domain of security reviews.

As covered at the beginning of this post, Claude Code performs security reviews through commands, plugins, GitHub actions and specialized agents, while Codex has a product called Codex Security for this.

### **Types of Security Reviews**

Security reviews vary in when they run and how deeply they look.

Most run on-demand or on a pull request and inspect a single diff—the equivalent of a git diff or pull request monitor in AI control evals.

In Claude Code, the `security-guidance` plugin installs hooks to run a monitor after every file edit, at the end of every turn, and before any commit or push, providing a form of step-wise monitoring.

At the deepest level, features like Claude Security and Codex Security can trace data flows across files within a repository to find subtler vulnerabilities.

However, none of these block writes, commits or merges by default; that needs to be configured via hooks or CI/CD actions.

### **Configuration Weaknesses**

Due to these limitations, security reviews don’t act as a full replacement for delayed, product-based monitoring.

A rogue agent that doesn’t want to be monitored can simply decline to invoke the security review. Where reviews are wired in through hooks or CI actions, the same types of attacks described in the Permissions section apply—an agent that can edit settings files or workflow definitions may be able to disable, narrow or misconfigure the review before it ever runs.

### **Adversarial Robustness**

Even when a review does run, it wasn't designed to be robust against adversarial attacks.

Security reviewers read the very diff the agent produced, so an agent can embed steering instructions in comments, test fixtures or documentation—the same prompt-injection surface that lets skill content steer an approval process.

And attacks that don't resemble traditional vulnerabilities, such as logic that is only exploitable under a particular deployment configuration, may pass a reviewer that reads the whole diff and still sees nothing familiar.

### **Scope & Factored Attacks**

As with basic control monitors, the scope of a review determines what it can catch.

A review that inspects one diff in isolation can miss an attack factored across several innocuous-looking pull requests, where no single change is suspicious on its own—the product-based analogue of the factored-cognition attacks subagents enable. Repository-wide tracing like Claude Security narrows this gap, but is still bounded by what lives in the repo.

### **Not a Control Replacement**

From a control perspective, security reviews are a valuable but partial product-based protocol. They raise the cost of landing a delayed attack, but they are neither mandatory nor robust by default.

Thus, it is valuable to do AI control research comparing these security reviews to existing AI control protocols and monitors. Vulnerabilities that get caught by security reviews may slip though research monitors and vice versa.

AI Control in the Era of Harnesses
----------------------------------

Moving forward, how should you think about developing AI control evals in the era of agentic harnesses?

### **Include Agentic Harnesses in Evals**

Make sure that your evaluation platform supports agentic harnesses.

If building directly on Inspect, use [inspect-swe](https://meridianlabs-ai.github.io/inspect_swe/) to run Claude Code, Codex, Gemini, Open Code or Mini SWE in each sample’s sandbox.

If using Control Tower, use `claude_code_policy` to run Claude Code in the sandbox with all features or `code_cli_policy` to run either Claude Code or Codex as a host-process outside the sandbox with a subset of features (no settings files, skills, custom agents or memory).

If using ControlArena, use [Agent Scaffolds](https://control-arena.aisi.org.uk/agent_scaffolds.html) and [inspect-swe](https://meridianlabs-ai.github.io/inspect_swe/) to pass the micro-protocol mapped through `AgentToModel` as a model alias that you then reference via model and other `_model` parameters.[^trpw12wdx2]

### **Do Vulnerability Research**

Manually explore the architecture of the production harnesses like Claude Code and Codex to identify potential weaknesses.

In doing so, distinguish between weaknesses that can be patched at the harness level and those that may be fundamental to the architecture.

For instance, the fact that subagents in Claude Code reload permissions instead of reusing the in-memory permissions of the lead agent is an implementation detail that can be easily changed. However, preventing rogue refinement agents from sabotaging research may require new monitors and protocols.

### **Build Evals At Multiple Levels**

With harnesses existing as systems that provide significant uplift for models, it can be helpful to think of control evals similar to software testing.

A **component control eval** is similar to a unit test. It tests a specific component of control protocol such as a monitor or scanner.

A **protocol control eval** is similar to an integration test. It tests how different components work together such as a step-wise monitor being used to defer edits to a trusted model, or how monitors may be tuned in a multi-stage monitor setup.

A **harness control eval** is similar to an end-to-end test. It tests how protocols work within full production harnesses with affordances often not present for component and protocol control evals.

Variants of these control evals may also exist. For instance, it may be valuable to do ablations of different capabilities within a harness control eval[^f9bwrwe5xpp] or to compare and contrast different control and agent architectures.

Existing settings that should be re-run using agent harnesses in auto mode to see how their metrics change when production monitors are used.

### **Using Hooks to Test Protocols**

Hooks can be used to test new monitors and control protocols in agent harnesses.

#### **Implementing Control Using Hooks**

Hooks fire at fixed lifecycle points and receive defined payloads for each event. These provide clear integration points for testing monitors and protocols.

For instance, with `PreToolUse` in Claude Code, commands can be given to a monitor to judge whether they should run while `Stop` can be used for turn-level monitoring.

Complete AI control protocols can even be implemented, with some limitations.

To implement defer-to-trusted, in Claude Code, a `PreToolUse` hook can return an `updatedInput` with a `permissionDecision: allow`, which would allow the protocol to change how text is edited with the `Write` tool.

One limitation of this approach is that the hook gets called after the decision has been made on which tool to call. Thus, the protocol can’t directly change which tool is called; it can only deny the tool call and guide the agent to request a different tool call.

#### **Hooks Add Realism**

Hooks ensure that monitors and protocols are seeing exactly what they would see in production—gaps included.

For instance, if compaction has pruned the active context or a subagent is running on its own trajectory, the payload reflects that. So you can evaluate monitors and protocols on realistic inputs rather than idealized transcripts.

Hooks fire recursively for subagents, which is one way to test whether a monitor holds up against the factored-cognition attacks described earlier.

#### **Hooks Can Guide Agents**

Hooks can also drive the agent in specific directions. Because a `PreToolUse` deny holds deterministically, a hook can force an agent to avoid specific solution paths, e.g., blocking a safe fallback to see whether the agent escalates, or blocking a condition to make a control setting reproducible.

However, keep in mind the “tighten-but-not-loosen” limit: a hook can block an action the harness would otherwise allow, but a hook can't push an otherwise disallowed action through. So use hooks to constrain the run, not to grant the agent affordances it wouldn't otherwise have.

#### **Using Hooks for Measurement**

When using monitors purely for measurement and not to change the trajectory, prefer `PostToolUse`; reserve `PreToolUse` for when the monitor aims to alter what the agent is doing.

### **Acquire Dual-Use Clearances**

Both Anthropic and OpenAI use a defense-in-depth approach to blocking attacks. This includes input filters, output filters and post-training a model for rejections in addition to auto mode and ephemeral prompts hardcoded into harnesses that reinforce that the model may not help with certain dual-use tasks.

The result is that certain types of AI control research, either now or in the near future, may require access to restricted models or harnesses, e.g., models that are helpful but *not* harmless. Without this access, researchers can expect increased rejections and non-functional evals.

To do this type of research requires getting certified access via programs like Anthropics’ [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude) (CVP) or OpenAI’s [Trusted Access for Cyber](https://openai.com/index/trusted-access-for-cyber/) program, or joining an organization like [Redwood Research](https://www.redwoodresearch.org/) or [Apollo Research](https://apolloresearch.ai/) which has special agreements with the frontier labs for such access.

If you are considering applying to one of these programs, or joining an organization that has such access, start implementing [physical security practices](https://www.cisa.gov/resources-tools/training/protect-physical-security-your-digital-devices) today; it takes time to upgrade your physical security and change your behaviors.

Auto Mode Provides Real Protection
----------------------------------

After describing how to find vulnerabilities in Claude Code and how harness capabilities can open up attack vectors, it would be easy to think auto mode in Claude Code and Codex is easily subverted.

In my experience, it cannot. It was non-trivial to get a working exploit for Claude Code and Anthropic has significantly tightened what gets [blocked by default](https://code.claude.com/docs/en/permission-modes#what-the-classifier-blocks-by-default).

In my assessment, auto mode is strong and provides real protection. I believe it will block most, if not all, “accidental” attacks where an agent simply is trying to work around limitations to reach its goal.

But strong doesn’t mean it can’t be made better.

As agents increase in intelligence and continue to be trained to work around obstacles, I expect they will find increasingly sophisticated ways of subverting the control protocols built into production agentic harnesses. Not to mention that rogue actors may be able to poison agents with more sophisticated strategies than an agent can develop on its own.

In this post, I focused on potential attack vectors that features of these harnesses may open up. At least part of AI control research should go toward exploring these and other attack vectors that exist in production control protocols like auto mode.

AI Control can never eliminate all attack vectors, but it can minimize them and be at least one layer of a defense in depth strategy toward preventing agents from causing harm.

Summary
-------

As frontier labs deploy agent harnesses with built-in control protocols internally, it becomes important not only to do fundamental research on theoretical control protocols, but research on these production protocols and how they integrate into their respective harnesses.

One set of unexplored weaknesses lies at how the different features of a harness interact. Determining whether these weaknesses can be easily patched or require adding new subsystems or an entirely new architecture is critical to improving the safety of the agent harnesses running these control protocols.

There remains a role for “pure” AI control research in the form of component- and protocol-level evals, but, when possible, control settings should also enable full end-to-end evals with harnesses so weaknesses can be detected, monitored and eliminated.

In the meantime, auto mode in harnesses like Claude Code and Codex appear to provide real protection against harmful actions taken by agents, whether intentional or accidental.

[^80zrgt1f9s2]: This vulnerability was identified in April 2026, so may no longer be viable; it nonetheless shows conceptually how interaction between harness features opens up attack vectors. 

[^qftcted12l]: If an agent is tasked with Python coding, having pytest in the allow list will be normal. 

[^trpw12wdx2]: Something like this: @agent_scaffolddef claude_code_scaffold():  def build(micro_protocol, tools, submit_tool, system_prompt):    return claude_code(      model_aliases={"control": AgentToModel(micro_protocol)},        model="control",        system_prompt=system_prompt,    )  return build 

[^f9bwrwe5xpp]: In Claude Code, features can be disabled using CLAUDE_CODE_DISABLE_ environment variables, settings or command-line flags. In Codex, use the features section of config.toml or use the CLI to disable features.