---
duration: "1-4 min"
batch: 2
order: 9
batch_name: "Bonus Techniques"
class: "claude-code"
chapter: "Setup"
---

## Setting Up Aliases for Claude Code

Show how to set up shell aliases to speed up your Claude Code workflow.

### Core Aliases

```bash
# Skip all permission prompts (use at your own risk)
alias cc='claude --dangerously-skip-permissions'

# Start in plan mode for research (read-only, no edits)
alias ccp='claude --permission-mode plan'

# Resume the last session
alias ccr='claude --resume'
```

### Quick One-Shot Usage

```bash
# Quick one-liner: generate a commit message
cc -c "write a commit message for the staged changes"

# Pipe in context
cat error.log | cc "explain this error and suggest a fix"
```

### Key Points

- Add aliases to `~/.zshrc` (or `~/.bashrc`) and run `source ~/.zshrc` to load
- `--dangerously-skip-permissions` is intentionally scary — it lets Claude run any command and edit any file without asking
- Only use after you fully understand what Claude Code can and will do to your codebase

## Quote to Include

> "This is how I start every Claude session... The `--dangerously-skip-permissions` flag name is intentionally scary. It lets Claude run any command and edit any file without asking. Only consider this after a few months of daily use, when you fully understand what Claude Code can and will do to your codebase."
>
> — [@felixleezd](https://x.com/felixleezd/status/2029236285005860903)
