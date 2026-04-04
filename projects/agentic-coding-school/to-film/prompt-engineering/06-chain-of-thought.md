---
duration: "10-15 min"
batch: 2
order: 8
batch_name: "Foundations"
class: "prompt-engineering"
chapter: "Core Techniques"
---
Chain of thought prompting is asking the model to show its reasoning before giving a final answer. It's the difference between asking someone "what's the answer?" and "walk me through how you'd figure this out." The second version consistently produces better results on anything involving logic, math, planning, or multi-step analysis.

### Why It Works: The Scratchpad Effect

LLMs generate tokens sequentially — each token can only attend to the tokens that came before it. When you ask for a direct answer, the model has to compute the entire reasoning chain internally in a single forward pass. That's like asking someone to multiply 347 x 89 in their head without writing anything down.

When you ask the model to reason step by step, each reasoning token becomes a "scratchpad" that subsequent tokens can attend to. The intermediate steps literally become part of the context that informs the final answer. The model isn't smarter — it just has more working memory to compute with.

This connects to the attention budget from Steering Distributions: chain of thought gives the model more compute per problem by spreading the reasoning across more tokens.

### The Three Flavors

**1. Explicit chain of thought** — You tell the model to reason step by step:
> "Before answering, think through this step by step. Show your reasoning, then give the final answer."

**2. Few-shot chain of thought** — You show examples where the reasoning is included:
> "Q: [question] → Reasoning: [step 1, step 2, step 3] → Answer: [answer]"
> This combines few-shot with chain of thought — the model learns both the reasoning *pattern* and the format.

**3. Zero-shot chain of thought** — The famous "Let's think step by step" suffix. Research showed that simply appending this phrase improved accuracy on math and logic benchmarks by 20-40% compared to direct prompting. It works because it steers the model toward the "reasoning" distribution in its training data — text that follows "let's think step by step" in training data tends to be careful, methodical analysis.

### When Chain of Thought Matters Most

| Task Type | Direct Prompting | Chain of Thought | Improvement |
|---|---|---|---|
| Simple factual | Works fine | Unnecessary overhead | ~0% |
| Math/arithmetic | Frequent errors | Dramatic improvement | 30-60% |
| Multi-step logic | Misses steps | Catches dependencies | 20-40% |
| Planning/strategy | Surface-level | Considers tradeoffs | 15-30% |
| Code debugging | Finds obvious bugs | Traces execution flow | 20-40% |

The pattern: the more steps between question and answer, the more chain of thought helps. For simple lookups, it's wasted tokens.

### The Modern Reality: Built-In Reasoning

Most frontier models in 2026 (Claude, GPT, Gemini) now have reasoning capabilities built in — they'll automatically "think" before responding on complex tasks. So why learn this?

1. **Not all models reason by default** — smaller models, local models, and API calls without reasoning mode still benefit enormously from explicit chain of thought
2. **You can direct the reasoning** — even with built-in reasoning, telling the model *what* to reason about ("think through the edge cases in the billing logic") produces better results than letting it choose
3. **Transparency** — when the model shows its reasoning, you can spot where it went wrong. A wrong answer with visible reasoning is more useful than a wrong answer with no explanation.
4. **Agents** — when building agent workflows, chain of thought in intermediate steps helps downstream agents understand *why* a decision was made, not just what it was

### Directed Chain of Thought

The advanced move isn't just "think step by step" — it's telling the model *which dimensions* to reason about. Compare:

**Generic:** "Think step by step about whether this PR should be merged."

**Directed:** "Before giving your verdict, reason through: (1) Does this change break any existing API contracts? (2) Are there edge cases in the error handling? (3) Will this scale to 10x current traffic? Then give your merge recommendation."

Directed chain of thought combines attention steering (where to focus) with chain of thought (show the work). You're not just asking the model to think — you're pointing its thinking at the dimensions that matter.

### Chain of Thought in Agent Workflows

When you're building prompt chains or agent workflows, chain of thought becomes a communication protocol between steps:

- Step 1 outputs: reasoning + conclusion
- Step 2 reads the reasoning, not just the conclusion
- Step 2 can therefore build on, challenge, or extend the logic

This is why the archetype teams from later in this class work — each subagent outputs its reasoning, and the orchestrator can synthesize *why* they disagree, not just *that* they disagree.

### Demo

1. Give a complex debugging scenario to a model with direct prompting — show it jumping to a wrong conclusion
2. Same scenario with "think step by step" — show it catching the issue through visible reasoning
3. Same scenario with directed chain of thought (specific dimensions to check) — show even better results
4. Show a case where chain of thought is overkill (simple factual question) — demonstrate that more reasoning isn't always better
5. Show chain of thought in a two-step agent workflow where step 2 uses step 1's reasoning

### Key Insight

> Chain of thought works because each reasoning token becomes working memory the model can attend to. It's not making the model smarter — it's giving it a scratchpad. The skill is knowing when to use it (multi-step problems) and what to direct it toward (the specific dimensions that matter for your task). Generic "think step by step" is the baseline; directed reasoning toward specific concerns is where the real leverage is.
