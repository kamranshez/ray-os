---
tags: [codex, openai, product-updates]
aliases: [Codex app latest features]
date: 2026-05-01
---

As of 2026-05-01, the latest major publicly announced Codex app feature drop is OpenAI's 2026-04-16 update, "Codex for (almost) everything." I re-checked OpenAI's product post, Help Center, and current Codex developer docs on 2026-05-01.

## Latest Major Codex App Features

1. **Background computer use**
   Codex can operate macOS apps by seeing the screen, clicking, and typing with its own cursor. This is useful for testing desktop apps, simulator/browser flows, GUI-only bugs, and data sources that are not exposed through plugins. It was initially macOS-focused and not available in the EEA, UK, or Switzerland at launch.

2. **Multiple agents in parallel**
   The Codex app is a desktop command center for running multiple threads across projects. It supports local, worktree, and cloud modes so agents can work side by side while keeping changes isolated.

3. **Worktrees and built-in Git tools**
   Codex can create isolated Git worktrees, show reviewable diffs, accept inline comments, stage or revert chunks/files, commit, push, and create pull requests from inside the app.

4. **In-app browser and browser comments**
   Codex includes an in-app browser for previewing local development servers, file-backed previews, and public pages that do not require sign-in. Users can comment directly on page regions and ask Codex to address the feedback.

5. **Browser use for local pages**
   For local development servers and file-backed pages, Codex can operate the page directly through browser-use, with allow/block controls managed in settings.

6. **Image generation and editing**
   Codex can generate and edit images directly in a thread for UI assets, banners, backgrounds, illustrations, sprite sheets, and placeholders. The April 16 announcement named `gpt-image-1.5`; the current Codex app docs say built-in image generation uses `gpt-image-2`.

7. **Image input and screenshots**
   Users can drag images into the composer, add images as context, or ask Codex to view local images and screenshots so it can verify visual work.

8. **90+ additional plugins**
   Plugins combine skills, app integrations, and MCP servers. OpenAI highlighted Atlassian Rovo, CircleCI, CodeRabbit, GitLab Issues, Microsoft Suite, Neon by Databricks, Remotion, Render, and Superpowers.

9. **Skills support**
   The app supports the same agent skills as the CLI and IDE extension, and teams can browse created skills from the sidebar.

10. **MCP support**
    Codex app, CLI, and IDE extension share MCP settings. Existing MCP server configuration is adopted across surfaces, and new servers can be enabled or added from app settings.

11. **First-party web search**
    Local Codex app tasks use OpenAI's web search tool by default, served from a cached search layer unless sandbox settings allow live results.

12. **GitHub review comment handling**
    Codex can help address GitHub PR review comments directly.

13. **Multiple terminal tabs / integrated terminal**
    Threads include a terminal scoped to the project or worktree. Codex can read current terminal output, which helps it react to failed builds, running dev servers, and validation commands.

14. **Remote devbox SSH support**
    Codex has alpha support for connecting to remote devboxes over SSH.

15. **Rich file previews and non-code artifacts**
    The sidebar can preview PDFs, spreadsheets, presentations, documents, and other generated artifacts.

16. **Summary pane / task sidebar**
    The task sidebar surfaces agent plans, sources, generated artifacts, and task summaries so users can steer and inspect work.

17. **Automations and thread automations**
    Automations can reuse existing conversation threads, preserve context, schedule future work, and wake up later to continue long-running tasks. Thread automations are recurring wake-ups that return to the same conversation context.

18. **Memory preview**
    Codex can remember preferences, corrections, and hard-won context from previous work. OpenAI says personalization features are rolling out to Enterprise, Edu, EU, and UK users soon.

19. **Proactive work suggestions**
    Codex can suggest useful next actions based on projects, connected plugins, and memory.

20. **Voice dictation**
    Users can hold `Ctrl`+`M` in the composer to dictate a prompt, then edit or send the transcript.

21. **Floating pop-out window**
    Active conversation threads can pop out into a separate window and optionally stay on top while the user works in another app.

22. **IDE extension sync**
    When the app and IDE extension are open in the same project, they can sync threads. With Auto context enabled, Codex can track files currently open in the editor.

23. **Chats without a project folder**
    Codex supports chat threads for research, triage, planning, plugin-heavy workflows, and other tasks that do not need a specific repo.

24. **Native Windows sandbox**
    On Windows, Codex can run natively in PowerShell with a Windows sandbox rather than requiring WSL or a VM.

25. **Personality selection**
    Codex supports personality settings through `/personality` in the app, CLI, and IDE extension.

## Latest Related Codex Updates

- **2026-04-30: Codex CLI 0.128.0** is the latest Codex changelog entry I found. It is mainly CLI/app-server work, not a new Codex app feature drop. Highlights include persisted `/goal` workflows, `codex update`, configurable TUI keymaps, richer permission profiles, marketplace plugin installation, remote bundle caching, external agent session import, and MultiAgentV2 configuration improvements.
- **2026-04-23: GPT-5.5 in ChatGPT** is a broader ChatGPT/model release. OpenAI describes it as stronger for agentic coding, terminal workflows, GitHub issue resolution, and long-horizon coding tasks, but I did not find an official Codex app feature announcement after the 2026-04-16 Codex update.
- **2026-04-09: Pro plan changes** updated how Codex usage works across Plus and Pro, including a new $100/month Pro plan and temporary Codex usage promotions.

## Availability Notes

- The Codex app launched on macOS on 2026-02-02.
- OpenAI updated the launch announcement on 2026-03-04 to say the app is available on Windows.
- Codex is included with ChatGPT Plus, Pro, Business, and Enterprise/Edu plans. As of the Help Center article checked on 2026-05-01, Codex is also included with ChatGPT Free and Go for a limited time, and other plans have temporary Codex rate-limit promotions.
- Enterprise/Edu plugin access follows workspace app controls; workspace admins can manage app/plugin access, RBAC, and compliance visibility for supported Codex surfaces.

## Sources

- [OpenAI: Codex for almost everything](https://openai.com/index/codex-for-almost-everything/)
- [OpenAI: Introducing the Codex app](https://openai.com/index/introducing-the-codex-app/)
- [OpenAI Help Center: Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-codex-in-chatgpt)
- [OpenAI Help Center: ChatGPT Release Notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)
- [OpenAI Developers: Codex app features](https://developers.openai.com/codex/app/features)
- [OpenAI Developers: Codex changelog](https://developers.openai.com/codex/changelog)
- [OpenAI Developers: Feature Maturity](https://developers.openai.com/codex/feature-maturity)
