---
class: "claude-code"
status: "scripted"
aliases: [agent-harness-concept]
---

# Agent Harness Concept

## What This Video Covers

An explanation of what an "agent harness" actually is — the infrastructure wrapping around an LLM that turns it from a text-in/text-out model into an agent that can control a computer. Claude Code IS the harness around Claude the model. Understanding this distinction changes how you think about everything.

## Why This Matters

Most people think "Claude Code" and "Claude" are the same thing. They're not. Claude is the brain (the LLM). Claude Code is the body (the harness) — it provides tools, memory, permissions, hooks, and parameters that let the brain actually DO things in the world.

This is why:
- Different harnesses (Claude Code, Droid, Pi, Codex) wrapping the same LLM produce different results
- Skills and subagents are just "two flavors of the same thing" — different ways of organizing markdown files
- Understanding the harness lets you optimize what actually matters (the infrastructure, not just the prompt)

## What's IN a Harness

The harness = everything that is NOT the LLM itself:

1. **System prompt** — the initial instructions injected before your first message
2. **Tools** — bash, web search, file read/write, screenshot, MCP connections
3. **Memory** — CLAUDE.md, memory.md, conversation history, skills front matter
4. **Parameters** — context compaction limits, token limits, max turns, auto-compact thresholds
5. **Hooks** — custom scripts that fire before/after tool calls
6. **Permissions** — what the agent can and can't do (ask before edits, bypass, plan mode)

## How the Competitor Teaches It

- Uses three analogies:
  - **Dog sled harness** — the harness directs the dog's energy (LLM's intelligence) in a useful direction
  - **Gun barrel** — same gunpowder (LLM), but a rifle barrel (good harness) shoots farther and more accurately than a cannon (bad harness)
  - **Space Invader in a house** — the agent alone would die on the savannah, but with infrastructure (roads, tools, shelter) it can do incredible work
- References Anthropic's Nov 2025 blog post "Effective Harnesses for Long-Running Agents" as the foundational document
- Compares Claude Code to alternatives: Droid (Factory AI), Pi (open-source), CrewAI, Paperclip (org chart agents)
- Key insight: skills and subagents are basically the same thing — both are "organized markdown files" with instructions, just structured slightly differently

## Key Concepts to Cover

- Definition: harness = everything wrapping the LLM (system prompt, tools, hooks, memory, parameters)
- The LLM is the brain; the harness is the body
- The gun barrel analogy (same gunpowder, different accuracy and range)
- The Space Invader analogy (intelligence is limited without infrastructure)
- Why Claude Code is the dominant harness today
- The 6 components of a harness (system prompt, tools, memory, parameters, hooks, permissions)
- Skills ≈ subagents ≈ organized markdown — same idea, different shape
- Anthropic's "Effective Harnesses for Long-Running Agents" blog post as foundational reading
- Brief comparison to alternatives (Droid, Pi, CrewAI, Paperclip) — what they do differently
- Why this matters: optimize the harness, not just the prompt

## Demo Plan

1. Show Claude the model (just text-in/text-out in the API)
2. Show Claude Code the harness (tools, memory, hooks, permissions layered on top)
3. Run /context to show everything the harness injects before your first message
4. Show how changing harness settings (permissions, model, tools) changes behavior
5. Brief tour of alternative harnesses (screenshots, not deep dives)

## Suggested Class Placement

Claude Code — Introduction or Advanced (good "why does this work the way it does" video)
