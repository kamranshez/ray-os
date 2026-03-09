---
source: "How I use Claude Code (Meta Staff Engineer Tips)"
channel: John Kim
video_id: mZzhfPle9QU
date: 2026-02-07
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Composability framework -- primitives working together**: John presents skills, commands, MCPs, subagents, and hooks as "four composable primitives" and explicitly teaches how to chain them (e.g., a skill triggers an MCP which spawns a subagent). Ray covers each individually but doesn't have a dedicated video on the composability mental model or how to combine all four in a single workflow. Quote: "These are composable more than anything... a skill that triggers an MCP that triggers sub agents."

- **[HIGH] Subagent anti-patterns -- when NOT to use subagents**: John gives a nuanced take that most people misuse subagents. He argues context-gathering tasks should stay in the main context window because the subagent only returns the output, not how it got there. Quote: "A lot of people are using sub agents incorrectly because they do things like this where you have like an iOS sub agent... that portion of the context that brings back from the sub agent it's only like the output, it's not like how it got there." He also calls out the "CEO agent, product agent, design agent" pattern as "clowny." Ray covers subagent usage but doesn't dedicate a video to subagent anti-patterns and when to avoid them.

- **[HIGH] /chrome -- browser navigation from Claude Code**: John demonstrates using `/chrome` to open a browser, navigate YouTube, search for videos, click elements, and scrape data -- all composable within slash commands. Quote: "I use this whenever I don't have API access to certain things but I can get there via my web." Ray doesn't cover the built-in `/chrome` command.

- **[HIGH] Whisper/dictation as primary input method**: John shows using Whisper (speech-to-text) as his primary way to interact with Claude Code, dictating prompts instead of typing. He describes switching between terminal tabs and just talking to each one. Quote: "I'm just like switching switching and I'm just basically talking to it." Ray doesn't cover voice/dictation workflows with Claude Code.

- **[MEDIUM] MCP token bloat auditing via /context**: John specifically demonstrates using `/context` to audit which MCPs are consuming the most tokens and recommends disabling or removing expensive ones. Quote: "MCPs are one of those very common things that blows up your tokens... if you look at this and you're like oh this MCP is using so much then you could remove it or just disable it for this directory." Ray covers /context but not specifically the MCP token auditing use case.

- **[MEDIUM] Compound engineering -- committing CLAUDE.md to the codebase for team use**: John describes a workflow he calls "compound engineering" where you refine your CLAUDE.md and then commit it to the codebase so the whole team benefits. He emphasizes removing personal paths and keeping quality high. Ray covers collaborative CLAUDE.md but not this specific "compound engineering" term/workflow.

- **[MEDIUM] Building validation loops into the iteration cycle**: John describes using tools like Puppeteer, Xcode builds, Perfetto traces, and end-to-end integration tests as validation loops that Claude can run automatically. Quote: "For web, you could do like puppeteer... have Claude navigate it using a /chrome command... or have it write just test or have like integration end to end integration test." Ray covers closing the loop but not specific validation loop examples like Xcode builds, emulator control, or performance profiling.

- **[MEDIUM] Multiple Claude instances juggling (Starcraft metaphor)**: John describes running 3-4+ Claude Code instances simultaneously across different projects and tabs, juggling them like "playing Starcraft." He renames terminal tabs (e.g., "local" vs "remote SSH") and switches rapidly. Quote: "It really feels like I'm playing Starcraft to some degree." Ray covers parallel work but not this specific high-throughput juggling workflow with tab renaming.

- **[MEDIUM] Enabling notification sounds/text-to-speech when Claude finishes**: John shows configuring Claude Code to ring a sound or even read a summary via text-to-speech when execution completes, so you know which tab to return to. Quote: "I had text to speech where it reads a summary of wherever it finished." Ray covers "Make Claude Speak to You" which may overlap, but the notification-for-tab-switching use case is distinct.

- **[LOW] Asking Claude to find and install MCPs for you**: John demonstrates telling Claude Code to find a good Figma MCP and install it, rather than manually searching and configuring. Quote: "You could just be like find me a good Figma MCP... and then Claude will just go and install it for you." Ray covers MCP setup but not the "ask Claude to find and install MCPs" workflow.

- **[LOW] Creating skills by asking Claude to save a workflow you just did**: John shows doing a workflow (fetch Hacker News, save summary) and then saying "save what we just did into a new skill called fetch hackernews." The skill auto-generates from the conversation. Ray covers skill creation but not this specific "do it once, then save as skill" pattern demonstrated live.

- **[LOW] Interrupting Claude when it makes assumptions or uses hedging language**: John advises watching for phrases like "I'm not really sure" or seeing errors as signals to hit Escape and course correct. Quote: "When you see it going and making assumptions about certain things... you should just interrupt it." Ray covers related topics in several technique videos but not this specific pattern-recognition advice.
