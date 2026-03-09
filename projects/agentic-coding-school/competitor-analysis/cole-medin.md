---
source: "A Complete Guide to Claude Code - Here are ALL the Best Strategies"
channel: Cole Medin
video_id: amEUIuBKwvg
date: 2025-08-07
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Serena MCP server for semantic code retrieval and editing**: Cole demonstrates the Serena MCP server, which provides better code understanding than Claude Code's built-in search by doing semantic retrieval across the codebase. He shows integrating it into a primer slash command. Quote: "This MCP server, it does a lot of the things that Claude Code does to understand your codebase and search through it... except it does it better. It is an MCP server that's all about semantic retrieval and editing your code." Ray covers MCP servers generally but not Serena specifically.

- **[HIGH] PRP (Product Requirement Prompt) framework for context engineering**: Cole demonstrates a three-step process: (1) create an initial.md describing what you want, (2) run /generate-prp to create a comprehensive prompt document, (3) run /execute-prp to build from that document. The PRP includes examples, documentation references, validation gates, anti-patterns, and a final checklist. Quote: "Context engineering with the PRP framework, it's a three-step process for us to define exactly the feature or new project we want to create." Ray covers planning and spec development but not this specific PRP workflow with generate/execute steps.

- **[HIGH] Validation gates subagent pattern**: Cole shows a subagent specifically designed for validation gates -- automatically running tests, iterating until confident the code works, then passing control back. This is from Raasmus, the PRP framework creator. Quote: "Validation gates is a very important part of the PRP framework because at the end once we have executed the PRP... we want our agent to operate autonomously writing tests iterating on those tests until it's confident that the code is working." Ray covers subagents but not this specific validation gates subagent pattern.

- **[HIGH] YOLO mode in dev containers with firewalls**: Cole demonstrates running Claude Code with dangerously-skip-permissions inside a Docker dev container that has firewall rules limiting which websites Claude can access. He shows the full setup using Anthropic's official dev container configuration. Quote: "With dev containers, we run cloud code in its own isolated environment. So our entire machine is protected. We can also have firewalls set up... so it only has access to the websites we want it to." Ray covers "Dangerously Skip Permissions" and "Sandboxing" but may not cover the specific dev container + firewall setup.

- **[HIGH] Automated git worktree-based parallel execution with slash commands**: Cole demonstrates two slash commands -- `/prep-parallel` and `/execute-parallel` -- that automate creating git worktrees, branches, and launching multiple Claude instances. The prep command creates N branches and worktrees in a loop, and the execute command launches Claude in each with the same plan. Quote: "We have the feature name... and then what are the number of parallel agents or parallel work trees that we want to have?" Ray covers git worktrees but not this automated slash command approach.

- **[HIGH] Slash command to auto-fix GitHub issues end-to-end**: Cole shows a `/fix-github-issue` slash command that takes an issue number, uses `gh issue view` to read it, implements a fix, writes tests, creates a branch, pushes, and creates a PR -- all automatically. Quote: "It goes out to GitHub, does things locally, and then goes back out to GitHub with a PR." Ray covers the GitHub App but not this specific slash command workflow for end-to-end issue fixing.

- **[MEDIUM] Permission management via settings.local.json with explicit allow/deny lists**: Cole demonstrates manually editing settings.local.json to whitelist specific commands (grep, ls, mkdir, python) while explicitly warning never to add `rm` or `bash(*)`. Quote: "Something that I never add to this list is I never add the rm the remove command... never just give it bash star because this means that it can run any command." Ray covers permissions but this specific best practice framing is useful.

- **[MEDIUM] Prompt engineering keywords that cause over-engineering**: Cole mentions that keywords like "production ready" cause Claude to over-engineer and keep old code for backwards compatibility. Quote: "Keywords like 'production ready' that cause it to overengineer, definitely important to keep in mind." Ray covers reducing agent confusion but not this specific keyword-trigger insight.

- **[MEDIUM] Primer slash command for codebase onboarding**: Cole creates a `/primer` command that runs `tree`, reads CLAUDE.md, reads README, and optionally uses Serena to semantically search the codebase -- designed to run at the start of every new session with an existing codebase. Quote: "It's a set of instructions, a set of steps that I'm telling Claude Code to take in order to get it up to speed with a current codebase." Ray covers custom slash commands but not this specific priming/onboarding pattern.

- **[MEDIUM] Applying Claude Code strategies to other AI coding assistants (Cursor, etc.)**: Cole repeatedly explains how each strategy (global rules, slash commands, subagents) can be adapted to Cursor, Cline, etc. Quote: "For other AI coding assistants like Cursor and Curo that don't have these slash commands, you can literally just use this as a prompt." Ray's course is Claude Code focused and doesn't bridge to other tools.

- **[LOW] Ultrathink keyword for maximum token reasoning**: Cole mentions the "Ultrathink" or "Ultraink" keyword to force Claude to use more tokens for deeper reasoning. Quote: "Try throwing Ultraink into a prompt and just see how much more it'll use tokens to think through a problem." Ray may cover reasoning effort but not this specific keyword.

- **[LOW] Parameterized slash commands with $ARGUMENTS**: Cole demonstrates using `$ARGUMENTS` in slash commands to create parameterized workflows (e.g., `/analyze-performance <file>`). Ray covers custom slash commands which likely includes this, but Cole's explanation is particularly clear.
