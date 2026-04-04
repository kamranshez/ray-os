---
duration: "10-15 min"
batch: 2
order: 9
batch_name: "Foundations"
class: "prompt-engineering"
chapter: "Core Techniques"
---
Structured output is telling the model to respond in a specific format — JSON, XML, markdown tables, YAML, CSV — rather than free-form prose. This is the bridge between "AI as chat partner" and "AI as a component in a system." The moment your output needs to be parsed by code, stored in a database, or consumed by another agent, structured output isn't optional.

### Why Format Is a First-Class Concern

Most people treat format as an afterthought — "just give me JSON." But format is actually a constraint that reshapes *what* the model says, not just *how* it says it.

When you request prose, the model optimizes for readability and narrative flow. It'll pad sentences, add transitions, include caveats. When you request a JSON object with specific keys, the model is forced to make a discrete decision for each field. There's no room for "it depends" — every key needs a value.

This means structured output often produces *more precise* answers than prose, even when you don't need to parse it programmatically. The structure forces commitment.

### The Schema as a Prompt

A JSON schema isn't just a format specification — it's a prompt in disguise. Each key name tells the model what information to extract or generate:

```json
{
  "verdict": "approve | reject | needs_changes",
  "confidence": "0.0 to 1.0",
  "blocking_issues": ["list of critical problems"],
  "suggestions": ["list of non-blocking improvements"],
  "reasoning": "one paragraph explaining the verdict"
}
```

This schema implicitly instructs the model to:
1. Make a discrete decision (verdict)
2. Quantify its confidence
3. Separate blocking issues from nice-to-haves
4. Explain its reasoning

You didn't write those instructions in prose — the schema *is* the instruction. This is more token-efficient and often more reliable than a paragraph of instructions, because the model can't skip or misinterpret a required key the way it can ignore a sentence in a long prompt.

### Choosing the Right Format

| Format | Best For | Watch Out For |
|---|---|---|
| **JSON** | API responses, agent-to-agent communication, database storage | Nested structures can confuse smaller models |
| **Markdown tables** | Comparisons, summaries for human consumption | Models sometimes break column alignment |
| **XML** | Hierarchical data, when you need named sections with content | Verbose, eats tokens |
| **YAML** | Configuration, human-readable structured data | Indentation errors are common |
| **CSV** | Tabular data for spreadsheets | Commas in content break parsing |
| **Typed enums** | Classification, discrete decisions | Model may invent values outside your enum |

### The Enum Trick

One of the most underrated structured output techniques is constraining values to enums — a fixed set of allowed options:

> "Classify the sentiment as exactly one of: `positive`, `negative`, `neutral`, `mixed`. Do not use any other value."

This collapses the output distribution to exactly 4 possibilities. The model can't hedge with "somewhat positive" or "leaning negative." It must commit. This makes downstream parsing trivial and forces the model to make the classification call rather than punting.

Combine with a confidence score and reasoning field, and you get the best of both worlds — a parseable decision plus the nuance in structured companion fields.

### Structured Output for Agent Chains

When building multi-step agent workflows, structured output is the contract between steps:

**Step 1** (Research Agent) outputs:
```json
{
  "findings": [...],
  "confidence": 0.8,
  "gaps": ["couldn't verify pricing", "no data on enterprise tier"]
}
```

**Step 2** (Decision Agent) reads the structured output and knows exactly what it has, how confident the research is, and what gaps to investigate further.

Without structure, Step 2 has to *parse prose* to figure out what Step 1 found. That parsing step introduces errors and wastes reasoning tokens. Structured output makes agent handoffs deterministic.

### Connecting to Previous Concepts

- **Steering distributions**: A JSON schema steers the model's output distribution as precisely as any natural language instruction — each key is an attention target
- **Few-shot**: Show one example of a completed JSON object and the model snaps to format instantly — often more reliable than describing the format in words
- **Chain of thought**: Include a "reasoning" field in your schema to get chain of thought *inside* the structured output — the model thinks through the answer to populate the reasoning field, which improves the other fields

### Common Failures and Fixes

1. **Extra text around JSON** — Model wraps JSON in "Here's the output:" or markdown code fences. Fix: "Respond with raw JSON only. No markdown, no explanation, no text before or after."
2. **Missing keys** — Model skips optional-seeming fields. Fix: mark every field as required or provide a default value in your schema.
3. **Type violations** — Model puts a string where you expected a number. Fix: include type annotations in your schema and one example.
4. **Hallucinated enum values** — Model invents a value outside your allowed set. Fix: repeat the allowed values and add "Do not use any value not in this list."

### Demo

1. Ask for a product comparison in prose — show the rambling, hard-to-parse result
2. Same task with a JSON schema — show the crisp, parseable output
3. Show the enum trick: classify 5 customer emails with a fixed sentiment enum + confidence score
4. Build a two-step agent chain: research agent outputs structured JSON, decision agent consumes it
5. Show a structured output failure (extra text around JSON) and the fix

### Key Insight

> A schema is a prompt. Every key name is an instruction, every type constraint steers the distribution, every enum collapses the output space to exactly the options you want. When your output needs to be consumed by code or another agent, structured output isn't just formatting — it's the contract that makes the system work. The model commits to discrete decisions instead of hedging in prose, which often produces more precise answers even when you're reading the output yourself.
