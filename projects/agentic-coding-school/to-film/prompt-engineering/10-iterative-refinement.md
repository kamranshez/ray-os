---
duration: "10-15 min"
batch: 2
order: 12
batch_name: "Foundations"
class: "prompt-engineering"
chapter: "Core Techniques"
---
Iterative refinement is treating prompting as a conversation, not a one-shot attempt. The first output is a draft. Your follow-up prompts sculpt it toward what you actually want. This is how experienced prompters work — they don't write the perfect prompt, they write a good-enough prompt and then steer from the output.

### The Invisible Work: Thinking Before Typing

Before refinement even starts, there's a step most people skip entirely — the cognitive work that happens before you open the chat.

When you sit down to prompt, you have a vague idea in your head. Maybe you saw something cool and want to recreate it, or you need to solve a specific problem. But the image isn't sharp. You start typing, hoping the model will fill in the gaps. It can't — it only knows what you type, and a fuzzy input produces a fuzzy output every time.

The gap between what you want and what you get isn't about the model being limited or needing better techniques. It's about you not knowing what you want with enough precision to communicate it.

Before you type anything, force yourself through specificity questions:
- What makes this output different from the generic version?
- What would make me say "yes, exactly like this" vs. "close but not right"?
- What emotion, structure, or insight am I actually after?

Go find references. Look for something that successfully represents what you're envisioning — a piece of writing, a design, a code pattern. When you can point at something concrete and say "like this, but different in these ways," you've done the invisible work. Translating that into a prompt becomes mechanical.

This is the difference between people who iterate 2-3 times and converge, and people who iterate 10 times and never get there. The second group isn't bad at prompting — they haven't figured out what they want yet, and no amount of iteration fixes that.

### Why Iteration Beats Perfection

There's a paradox in prompt engineering: the more time you spend crafting the perfect first prompt, the less likely you are to get what you want. This is because:

1. **You don't know what the output will look like** until you see it. Your mental model of the result and the model's interpretation of your prompt rarely align on the first try.
2. **Seeing the output changes what you want.** You asked for a blog post intro. The model gives you one. Now you realize you wanted something more conversational. You didn't know that until you saw the formal version.
3. **Refinement is cheaper than specification.** Describing exactly what you want takes 200 words. Saying "shorter, less formal, cut the second sentence" takes 10 words — and is more precise because it's reacting to a concrete output, not an abstract ideal.

The experienced prompter's workflow: spend 30 seconds on the first prompt, then 2-3 rounds of refinement. Total time: 2 minutes. The perfectionist's workflow: spend 10 minutes on one prompt, get a result that's 80% right, start over. Total time: 15 minutes.

### The Refinement Stack

Each refinement message adds a layer of constraint. Think of it as a stack:

1. **First prompt**: establishes the task, role, and rough direction
2. **Refinement 1**: adjusts tone, length, or focus based on what you see
3. **Refinement 2**: handles a specific section or detail that's off
4. **Refinement 3**: polish — final tweaks to language, structure, or emphasis

Most tasks converge within 2-3 refinements. If you're on refinement 5+, the initial prompt was probably too far off — start a new session with a better first prompt that incorporates what you learned.

### Refinement vs. Restarting: When to Use Which

**Refine when:**
- The output is 60%+ correct — the structure, tone, or approach is roughly right
- You can articulate what's wrong in a sentence or two
- The model demonstrated it understands the task — it just made different choices than you wanted

**Restart when:**
- The output is fundamentally wrong direction — it wrote a blog post when you wanted bullet points
- The conversation history is polluting the context — earlier outputs are anchoring the model
- You've refined 4+ times and it's still not converging — the original framing is the problem

Restarting with a new session is underrated. The model's context now includes all of its wrong attempts, which compete for attention with your corrections. A fresh session with a refined first prompt (incorporating everything you learned) often gets you there in one shot.

### The Anchor Effect

A critical thing to understand: the model's first output becomes an anchor. Every refinement is influenced by what came before. If the first output was 500 words and you say "shorter," the model might give you 350 words — shorter relative to its anchor, but still too long.

This is why specific refinements outperform vague ones:
- Vague: "shorter" → model interprets relative to anchor
- Specific: "under 150 words" → model interprets as absolute constraint

Similarly:
- Vague: "more casual" → subtle shift
- Specific: "rewrite as if you're texting a friend, no capitals, use contractions" → clear target

### Self-Evaluation as Refinement

Instead of you identifying what's wrong, you can ask the model to evaluate its own output. This works best in a new session (so the model isn't biased toward defending its work):

1. Copy the output
2. Open a new chat
3. "Here's a [blog post/email/code review] I wrote. Rate it 1-5 on [clarity/accuracy/tone]. What's the single most impactful improvement?"
4. Take that feedback back to the original session

This creates a two-model refinement loop: one generates, one critiques. The critic finds things you wouldn't notice because it's reading with fresh eyes and no commitment to the current version.

### Iterative Refinement for Code

The same pattern applies to code generation:

1. **First prompt**: describe the feature and constraints
2. **Refinement 1**: "This works but the error handling is too verbose — use early returns instead of nested try-catch"
3. **Refinement 2**: "Add input validation for the email field — reject anything without @ and a domain"
4. **Refinement 3**: "Rename `processData` to `transformUserInput` and add a JSDoc comment"

Each refinement is surgical. You're not re-describing the whole feature — you're pointing at specific things to change. This is the most efficient way to work with a coding agent.

### Speak Your Prompts

A practical technique that makes iteration dramatically faster: use voice instead of typing.

The reason most people write vague prompts isn't lack of knowledge — it's laziness. Typing a detailed 200-word prompt with role, constraints, format, and examples takes effort. So people cut corners: they skip the constraints, leave out examples, and write the minimum.

Voice dictation removes this bottleneck. Speaking at 150+ WPM versus typing at 40-60 WPM means you can include 3x more detail in the same time. The constraints you'd skip while typing ("don't use corporate jargon, keep it under 200 words, start with the action item") take 5 seconds to say.

This is especially powerful for iterative refinement. Each refinement message is small — "shorter, cut the second paragraph, make the CTA more specific" — but typing those small corrections feels tedious. Speaking them feels natural, like directing a collaborator.

Modern dictation tools (built-in on phone, third-party on desktop) handle punctuation, formatting, and filler word removal automatically. The prompt you get from speaking is often *better* than what you'd type, because you naturally include more context when talking than when typing.

### Connecting to Other Techniques

- **Chain of thought + refinement**: If the model's reasoning was wrong, don't just say "wrong answer." Say "your step 3 assumed X, but actually Y. Redo from step 3."
- **Constraints + refinement**: Your first prompt sets the broad direction. Refinements add constraints you didn't think of until you saw the output.
- **Few-shot + refinement**: If the output format is off after refinement, paste one example of what you want and say "match this format exactly."

### Demo

1. Write a first prompt for a product announcement email — intentionally quick, not overthought
2. See the output — identify 2-3 things that are off (too formal, too long, weak CTA)
3. Refine with specific instructions — show the output improving
4. Show the anchor effect: "shorter" vs. "under 100 words" — demonstrate why specificity matters in refinements
5. Show the self-evaluation loop: paste output into new session, get critique, apply it
6. Show when to restart: 4 refinements that aren't converging → fresh session with a better first prompt that nails it immediately

### Key Insight

> The perfect first prompt is a myth. Experienced prompters write fast, approximate first prompts and invest their effort in targeted refinement — because reacting to a concrete output is always more precise than describing an abstract ideal. The skill isn't writing the prompt; it's reading the output, diagnosing what's off, and knowing whether to refine, restart, or switch techniques entirely.
