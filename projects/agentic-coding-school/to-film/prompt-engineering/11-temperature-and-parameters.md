---
duration: "10-15 min"
batch: 2
order: 13
batch_name: "Foundations"
class: "prompt-engineering"
chapter: "Under the Hood"
---
Temperature, top-p, top-k, and other model parameters are the knobs that control how the model samples from its output distribution. Understanding these turns prompt engineering from an art into something closer to engineering — you're not just shaping *what* the model considers, you're controlling *how it chooses* from its options.

### The Sampling Process

When a model generates the next token, it doesn't just pick the "best" one. It calculates a probability distribution over its entire vocabulary — every possible next token gets a score. Then it *samples* from that distribution.

This is the critical insight: the model always sees the full range of options. Temperature and other parameters control which part of that range it's allowed to pick from.

Think of it like a dartboard:
- **Low temperature (0.0-0.3)**: The model aims for the bullseye — the highest-probability token. Very consistent, very predictable. The same prompt gives nearly the same output every time.
- **Medium temperature (0.5-0.8)**: The model aims for the inner rings — high-probability tokens, but with some variation. Good balance of quality and creativity.
- **High temperature (0.9-1.5)**: The model aims for the whole board — even low-probability tokens have a chance. More creative, more surprising, more likely to produce nonsense.

### Temperature in Practice

| Temperature | Behavior | Use Case |
|---|---|---|
| **0.0** | Greedy — always picks the highest probability token | Factual extraction, classification, structured output, code |
| **0.2-0.4** | Near-deterministic with slight variation | Professional writing, summaries, data analysis |
| **0.5-0.7** | Balanced — default for most providers | General conversation, drafting, explanations |
| **0.8-1.0** | Creative, varied outputs | Brainstorming, creative writing, generating alternatives |
| **1.0+** | Increasingly random, may produce incoherent output | Experimental, art, chaos-by-design |

Most chat interfaces (ChatGPT, Claude.ai) don't expose temperature directly — they set it internally based on the task or model. But when you're using the API, building agents, or working in tools like Cursor, temperature becomes a lever you can pull.

### Top-p (Nucleus Sampling)

Temperature adjusts the *shape* of the probability distribution. Top-p adjusts the *size* of the pool the model samples from.

Top-p = 0.9 means: consider only the tokens whose cumulative probability adds up to 90%. Everything in the long tail is excluded.

Why this matters: at high temperature, the model might sample from very low-probability tokens that produce gibberish. Top-p acts as a safety net — "be creative, but only within the realm of reasonable options."

| Top-p | Effect |
|---|---|
| **0.1** | Only the most probable few tokens — very constrained |
| **0.5** | Moderate pool — some variety, no wild swings |
| **0.9** | Large pool — creative but grounded (common default) |
| **1.0** | Full vocabulary — no filtering |

In practice, most people adjust temperature and leave top-p at 0.9 or 1.0. Adjusting both simultaneously can produce unpredictable interactions.

### Top-k

Top-k is simpler: only consider the top K most probable tokens, regardless of their actual probabilities.

Top-k = 50 means: at each step, only the 50 highest-probability tokens are candidates. Even if the 51st token would be a reasonable choice, it's excluded.

Top-k is blunter than top-p but useful when you want hard limits on the creativity range.

### The Compound Effect

Temperature matters most for longer outputs because the randomness compounds:

- At temperature 0.3 over 10 tokens, output is very stable
- At temperature 0.3 over 1,000 tokens, small variations accumulate and the output can drift significantly from what you'd get at temperature 0.0

This is why:
- **Short outputs** (classifications, titles, JSON) → low temperature is fine
- **Long outputs** (essays, code files, reports) → even moderate temperature can cause drift, inconsistency, or the model "forgetting" its constraints partway through

### When Temperature Interacts with Prompting

Temperature and prompt specificity have an interaction effect:

- **Vague prompt + high temperature** = chaos. The model has wide latitude in what to generate AND how to sample. Output will be unpredictable.
- **Specific prompt + high temperature** = creative within boundaries. The prompt constrains the *what*, temperature varies the *how*. This is the sweet spot for creative work.
- **Specific prompt + low temperature** = deterministic. Great for structured output, classification, and any task where you want the same result every time.
- **Vague prompt + low temperature** = the training-data average. The model defaults to the most common response pattern. This is what most people experience and why they think AI is "generic."

### Practical Advice

1. **For agents and automation**: Use temperature 0.0-0.2. You want deterministic, parseable output. Creativity is a bug in pipelines.
2. **For brainstorming**: Use temperature 0.8-1.0. Run the same prompt 3-5 times and cherry-pick the best output. High temperature + multiple runs is how you find surprising ideas.
3. **For writing**: Start at 0.5-0.7. If the output is too predictable, nudge up. If it's inconsistent, nudge down.
4. **For code**: Temperature 0.0. Code needs to be correct, not creative. Let the prompt handle the creativity (architecture decisions, naming) and let temperature handle the execution (deterministic token selection).
5. **When you can't control temperature** (chat interfaces): Use your prompt to simulate it. For low temperature behavior, be extremely specific with constraints. For high temperature behavior, say "give me 5 very different approaches" — this forces the model to explore the distribution even at default temperature.

### Other Parameters Worth Knowing

- **Max tokens**: Hard limit on output length. Set this to prevent runaway outputs in automation. In conversation, rarely needed.
- **Stop sequences**: Tokens that tell the model to stop generating. Useful for structured output — stop at `}` to prevent the model from adding commentary after your JSON.
- **Frequency/presence penalty**: Discourages repetition. Useful for long-form generation where the model starts repeating phrases.

### Demo

1. Same prompt at temperature 0.0, 0.5, and 1.0 — show how output varies
2. Classification task: show that temperature 0.0 gives consistent results while 0.8 randomly changes the classification
3. Brainstorming: run the same creative prompt 5 times at high temperature — show the diversity
4. Show temperature interaction with prompt specificity: vague prompt + high temp (chaos) vs. specific prompt + high temp (creative within bounds)
5. In a chat interface (no temperature control): demonstrate how prompt constraints simulate low temperature

### Key Insight

> Temperature controls *how* the model chooses from its options, while your prompt controls *what* options exist. They're complementary levers. Low temperature + specific prompt = deterministic precision. High temperature + specific prompt = creative exploration within boundaries. Understanding this interaction lets you tune the model's behavior at a level that prompt engineering alone can't reach — and knowing when you CAN'T control temperature (most chat interfaces) teaches you to use prompt constraints as a substitute.
