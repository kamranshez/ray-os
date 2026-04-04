---
duration: "10-15 min"
batch: 2
order: 7
batch_name: "Foundations"
class: "prompt-engineering"
chapter: "Core Techniques"
---
Few-shot prompting is giving the model examples of input-output pairs so it can infer the pattern and replicate it. This is one of the most reliable techniques in prompt engineering because it bypasses the need to *describe* what you want — you *show* it instead.

### Why Examples Beat Descriptions

When you describe a format in words, the model has to interpret your description, map it to its training data, and generate something it thinks matches. Every step introduces drift. When you show examples, the model pattern-matches directly — it's doing what transformers are architecturally optimized for.

This is the same reason a new hire learns faster from watching you do the task than from reading a wiki page about it. The examples carry implicit information — tone, edge case handling, what you *don't* include — that descriptions almost always leave out.

### The Spectrum: Zero-Shot to Many-Shot

| Strategy | What You Provide | When to Use |
|---|---|---|
| **Zero-shot** | Just the instruction | Simple, unambiguous tasks |
| **One-shot** | One example | When format matters but content is flexible |
| **Few-shot (2-5)** | Several examples | When you need consistent format AND edge case coverage |
| **Many-shot (10+)** | Large example set | Classification tasks, style matching, nuanced tone |

Most people default to zero-shot (just the instruction) even when a single example would dramatically improve the output. The sweet spot for most tasks is 2-3 examples.

### What Makes a Good Example Set

Not all example sets are equal. The examples you choose shape the distribution the model will sample from:

1. **Cover the edges, not just the center** — If all your examples are straightforward cases, the model won't know how to handle unusual inputs. Include at least one edge case.
2. **Show what NOT to do** — A negative example ("Here's an input that might tempt you to do X — the correct output is Y instead") is worth three positive examples.
3. **Keep format perfectly consistent** — If your examples have inconsistent formatting (sometimes with a period, sometimes without), the model will randomly alternate. Every detail in the example is a signal.
4. **Order matters** — The last example has the strongest influence on the next output. Put your "gold standard" example last.

### The Hidden Power: Implicit Rules

Few-shot examples carry rules you never explicitly stated. If all three of your examples:
- Start with a verb
- Are under 60 characters
- Use title case for proper nouns only
- Omit articles ("the", "a")

The model picks up ALL of these patterns without you writing a single rule. This is why few-shot often outperforms long instruction lists — the examples encode the rules implicitly and consistently, whereas written rules compete for the model's attention budget (as we covered in Steering Distributions).

### Connecting to Steering Distributions

Few-shot examples are actually a form of distribution steering. Each example narrows the output distribution:

- Zero examples → the model samples from its broad training distribution for that task
- One example → distribution collapses to the neighborhood of that example's style/format
- Three examples → distribution is now tightly clustered around the pattern they share

This is why contradictory examples are so damaging — they *widen* the distribution when you're trying to narrow it. If example 1 uses formal tone and example 2 uses casual tone, you've created a bimodal distribution and the model will randomly alternate.

### When Few-Shot Fails

Few-shot isn't always the answer:

- **Reasoning tasks** — showing examples of correct answers doesn't teach the model *how* to reason. Chain of thought is better here.
- **Creative tasks** — too many examples anchor the model and kill novelty. Use 1 example max for creative work.
- **Long outputs** — few-shot examples of 500-word outputs eat your context window fast. Describe the format instead and give one abbreviated example.

### Demo

1. Take a real task: converting customer feedback into support ticket titles
2. Zero-shot: show the inconsistent, verbose output
3. Add 3 examples with a clear format pattern — show how output immediately snaps to format
4. Add a negative example for an edge case — show the model handling it correctly
5. Show how removing one example changes the output subtly — demonstrate that every example is a signal

### Key Insight

> Few-shot prompting works because transformers are pattern-matching engines. Every example you provide is a data point that collapses the output distribution. The skill isn't just "give examples" — it's choosing examples that encode the implicit rules, edge cases, and quality standards you'd otherwise need paragraphs to describe. Three well-chosen examples beat thirty lines of instructions.
