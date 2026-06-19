---
class: "techniques"
status: "scripted"
aliases: [core-agent-loop]
---

# The Core Agent Loop (Observe → Think → Act)

## What This Video Covers

The foundational loop that ALL AI agents run, regardless of platform (Claude Code, Codex, Gemini, Cursor). Every single interaction follows the same three steps: Observe (read all context), Think (reason about what to do next), Act (call tools, edit files, run commands). The loop repeats until a "definition of done" is reached. Understanding this loop is the first principle that everything else builds on.

## Why This Matters

This is the conceptual foundation for EVERYTHING in the course. Once you understand the loop:
- **Context management** makes sense: context grows with each loop → quality degrades → you need to manage it
- **Planning** makes sense: planning happens in the Think step → better planning = fewer loops = less context waste
- **Subagents** make sense: each subagent runs its OWN loop with its OWN clean context
- **Skills** make sense: skills constrain what happens in the Act step → more deterministic outcomes
- **Verification loops** make sense: a reviewer agent runs a fresh loop on the output of the first agent

Without this foundation, everything else feels like disconnected features. With it, they're all variations on the same theme.

## The Loop

```
         ┌──────────┐
         │ OBSERVE   │ ← Read context: CLAUDE.md, conversation history,
         │           │   files, previous tool results, memory
         └─────┬─────┘
               ↓
         ┌──────────┐
         │  THINK    │ ← Reason about what to do next
         │           │   (visible in the "thinking" panel)
         └─────┬─────┘
               ↓
         ┌──────────┐
         │   ACT     │ ← Call tools: edit files, run bash, web search,
         │           │   read files, take screenshots
         └─────┬─────┘
               ↓
         Tool result feeds back into OBSERVE
               ↓
         Context grows by N tokens
               ↓
         Loop repeats until "definition of done"
```

## Context Accumulation

Each loop iteration adds tokens to the context:
- Loop 1: system prompt + your message (~10K tokens)
- Loop 2: + tool call + tool result (~15K tokens)
- Loop 3: + another tool call + result (~20K tokens)
- Loop 10: maybe 50K+ tokens

This is WHY context management matters — the model's quality degrades as context grows. And it's WHY subagents are valuable — each one starts with a fresh, clean context.

## Definition of Done

The loop continues until the model concludes it has satisfied the user's request. If you don't give a clear definition of done, the model either:
- Stops too early (didn't finish the job)
- Loops forever (keeps making changes without converging)

Prompt contracts, plan mode, and spec developer all help define "done" more precisely.

## How the Competitor Teaches It

- Draws the loop diagram on screen
- Shows Codex CLI going through observe → think → act in real-time
- Points out the grayed-out "thinking" section as the Think step made visible
- Explains the definition of done concept
- Shows how context grows with each iteration
- Notes that the more intelligent the model, the longer it can run autonomously
- Connects to everything else: tools, memory, reasoning loop, skills

## Key Concepts to Cover

- The three steps: Observe, Think, Act
- What's in each step:
  - Observe: CLAUDE.md, memory, conversation history, tool results, files
  - Think: reasoning/planning (visible in thinking panel)
  - Act: tool calls (bash, read, write, web search, screenshot, MCP)
- Context accumulation: tokens grow with each loop iteration
- Definition of done: when the loop stops (and why vague prompts cause infinite loops)
- The thinking/reasoning panel as visibility into the Think step
- How ALL platforms run this same loop (Claude Code, Codex, Gemini, Cursor)
- Why this matters for context management (growth → degradation → management needed)
- Why this matters for planning (better plans = fewer loops = less waste)
- Why this matters for subagents (fresh context = fresh loop = better quality)

## Demo Plan

1. Send a simple request to Claude Code
2. Pause and annotate each step: "here it's observing... here it's thinking... here it's acting"
3. Show the thinking panel expanding
4. Show the tool call executing
5. Show the result feeding back in (context grows)
6. Show /context before and after — token count increased
7. Explain: this same loop is what Codex, Gemini, and every other agent runs

## Suggested Class Placement

Techniques — Fundamental Techniques (could be the very first video — foundational concept)
