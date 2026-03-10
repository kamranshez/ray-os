---
duration: "1-4 min"
batch: 1
order: 10
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Setup"
---

# Using Claude Code in WSL

Claude Code works better in WSL because WSL gives Windows a real Linux environment, and Claude Code is the kind of tool that benefits from that. It runs shell commands, uses developer tools, and interacts with your codebase the way a developer would. Linux is the environment where a lot of those tools behave most predictably. macOS is similar because it's Unix-based, so Mac users already get a lot of that behavior by default. Windows isn't Unix-based, so WSL is basically Microsoft's way of giving you that Linux developer layer without leaving Windows.

### Key Points

- **Why Linux matters** — Claude Code runs shell commands, uses developer tools, and interacts with your codebase the way a developer would. Linux is where those tools behave most predictably.
- **macOS gets it for free** — macOS is Unix-based, so Mac users already get that natural developer environment by default.
- **Windows needs WSL** — Windows isn't Unix-based, so WSL is Microsoft's way of giving you that Linux developer layer without leaving Windows.
- **What WSL actually is** — Microsoft says WSL lets developers run a GNU/Linux environment directly on Windows without a traditional VM.
- **Git Bash vs WSL** — Anthropic says Claude Code on Windows uses Git Bash internally, while WSL gives you a full Linux environment directly on Windows.
- **Bottom line** — If you're on Windows and using Claude Code, run it inside WSL for the most predictable experience.

![[images/using-cc-in-wsl/excalidraw_4.png]]
