---
tags: [agentic-coding, llm-behavior, prompting]
date: 2026-05-06
source: AI That Works podcast — Vibhav (BAML) + Dex (HumanLayer)
---

# Models are sycophantic, so suggestions arrive as commands

## The idea
Even the best models are extremely sycophantic. When you suggest something — even tentatively — the model takes it as an instruction and runs with it. The model's prior is reasonable: "if the human is bringing this up, they probably know something I don't." So it listens. This means whatever mistakes or half-formed hunches you have compound catastrophically downstream.

## Why this matters for junior engineers
Junior engineers struggle disproportionately with these models because they don't yet know to flag uncertainty in their prompts. They tell the model something as if it's fact, and the model believes them. The model never pushes back. The compounding error rate is invisible until the implementation falls apart.

## How to apply
- Frame suggestions softly: "consider this" / "what if" / "here are options I'm weighing"
- Make it explicit when something is a *thou shalt* vs. *I'm exploring*
- Ask the model for options instead of giving it a directive — let it surface alternatives you haven't considered
- If you do want to commit to a direction, say so explicitly so the model stops looking for alternatives

## Surrounding context
This came up while Vibhav was iterating on BAML's testing feature. He suggested using a global variable in a `testing` package as a registry. The model accepted it without question, even though Vibhav was just musing. He had to actively self-correct hours later. The lesson: the design discussion phase is where sycophancy bites hardest, because that's where soft musings get baked into hard decisions that propagate into thousands of lines of code.

## Open questions to explore
- Are there prompt patterns that reliably get models to push back on bad suggestions?
- Does asking "rate my idea 1-10 honestly" help, or does the model just flatter?
- How do you teach junior engineers to recognize their own uncertainty in real time?
