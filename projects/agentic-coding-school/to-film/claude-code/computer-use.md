---
class: "claude-code"
status: "scripted"
aliases: [computer-use]
---

# Computer Use (Mouse / Keyboard Control)

## What This Video Covers

Claude Desktop's computer use feature that literally controls your mouse and keyboard. Unlike browser automation (which manipulates JavaScript/DOM), computer use can do ANYTHING on your computer — move files in Finder, click native app menu items, type into any application, scroll through windows. It's the "nuclear option" of automation: slow, expensive, but universally capable.

## Why This Matters

There are three tiers of automation, each with different tradeoffs:

| Tier | Speed | Cost | Setup | Generality |
|---|---|---|---|---|
| **HTTP requests** | Fastest | Cheapest | Most setup | Fragile (APIs change, rate limits) |
| **Browser automation** | Medium | Medium | Moderate setup | Works on most websites |
| **Computer use** | Slowest | Most expensive | Zero setup | Works on EVERYTHING |

Understanding this gradient lets you pick the right tool:
- Prototype with browser automation (Chrome DevTools MCP)
- Once working, convert to HTTP requests for production speed
- Fall back to computer use when nothing else works

## How the Competitor Teaches It

- Opens Claude Desktop → Cowork tab
- Asks it to: "scan through my Downloads, find the image called maker school 26, rename it to weekly community call picture"
- Shows the agent literally:
  - Opening Finder
  - Typing "Downloads" in the navigation
  - Scrolling through files
  - Finding the target file
  - Right-clicking, selecting rename
  - Typing the new name
- Notes: took much longer than doing it manually, consumed many tokens (screenshots at every step)
- Explains the automation gradient: HTTP → browser → computer use
- Recommends starting with browser automation for prototyping, converting to HTTP for production

## Key Concepts to Cover

- What computer use is (mouse + keyboard control of the entire OS, not just browser)
- The automation gradient: HTTP requests → browser automation → computer use
- Tradeoffs for each tier: speed, cost, setup time, generality
- When to use computer use:
  - Native apps with no API (Finder, Preview, native macOS/Windows apps)
  - One-off tasks not worth building an HTTP integration for
  - When browser automation can't access what you need
- When NOT to use computer use:
  - Anything you can do via HTTP/API (way faster and cheaper)
  - High-volume repetitive tasks (too slow and expensive per action)
  - Time-sensitive operations (each action takes 5-15 seconds)
- How it works under the hood: screenshot at every step → model decides next mouse/keyboard action
- Cost implications: many tokens consumed for screenshots at every step
- The production workflow: prototype in computer use → convert to browser automation → convert to HTTP
- Current limitations and where this is heading

## Demo Plan

1. Show a simple task done manually (rename a file) — 5 seconds
2. Show the same task via computer use — much slower but autonomous
3. Watch the mouse move, keyboard type, Finder navigate
4. Show the token cost of this simple task
5. Compare: same file rename via bash command (instant, near-zero tokens)
6. Discuss when computer use makes sense vs when it doesn't
7. Show the automation gradient diagram

## Suggested Class Placement

Claude Code — Advanced
