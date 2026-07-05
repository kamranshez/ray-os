---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Aligning to Your Intent"
class: "prompt-engineering"
chapter: "Aligning to Your Intent"
---

## The Flip

Here is the thesis, straight up: on frontier models, stuffing your prompts, skills, and CLAUDE.md files with examples now makes the output worse. The technique everyone learned as prompt engineering 101, pile on the few-shot examples, has quietly flipped from a best practice into a ceiling. In this video I'll show you why it happens, prove it with a live experiment, and give you the rule that replaces it: zero to two examples, plus intent, plus context.

This is not a hot take. Anthropic removed 80% of Claude Code's system prompt because newer models need fewer constraints. The people building the harness you use every day are deleting examples, not adding them.

Source: Tariq Shihipar, Anthropic, AI Engineer World's Fair 2026

---

## The Habit Everyone Learned

Think about how you built your last skill or CLAUDE.md file. You wanted the model to produce a certain kind of output, so you did the obvious thing. You collected your best outputs and pasted them in. Three examples. Five. Ten. Each one felt like insurance.

That habit came from somewhere real. On earlier models, few-shot prompting was the single highest-leverage technique available. Weak models genuinely needed examples to figure out what you wanted. More examples meant more reliability. Everyone internalized it.

The problem is that the models changed and the habit didn't.

Tariq Shihipar, who works on Claude Code at Anthropic, said it plainly: "the examples tend to constrain it because it's actually more imaginative than the examples we give it."

Read that again. The model is more imaginative than your examples. So every example you add is not raising the floor anymore. It's lowering the ceiling.

---

## What an Example Actually Does

Here's the mental model that makes this click.

You think an example teaches format. What it actually defines is a **distribution**. The model treats your examples as evidence of the target distribution and samples near their centroid, the statistical center of the cluster your examples form.

[IMAGE: dark chalkboard, large cloud labeled "model's learned distribution" with rich outer tails, inside it a tight small cluster of dots labeled "your 8 examples" with a centroid marked, arrows showing sampling collapsing onto the centroid while the outer tails are crossed out as "clipped"]

![[stop-giving-examples-distribution-clip-1.png]]
![[stop-giving-examples-distribution-clip-2.png]]
![[stop-giving-examples-distribution-clip-3.png]]
![[stop-giving-examples-distribution-clip-4.png]]
![[stop-giving-examples-distribution-clip-5.png]]

When the model's own learned distribution is richer than your examples, conditioning on them clips exactly the tails where the creative, edge-covering output lives. The weird test case. The failure mode you didn't think of. The angle you would never have written yourself. All of that lives in the tails, and your examples just told the model to stay away from them.

On a weak model, this trade is worth it. The model's distribution is noisy, so pulling it toward your examples removes garbage. On a frontier model, the distribution is better than your examples. Pulling toward the centroid removes gold.

This is why the same technique flipped sign. Nothing about few-shot prompting changed. The model underneath it did.

---

## The Bitter Lesson, at Prompt Scale

If this pattern feels familiar, it should. Rich Sutton described it in 2019 in an essay called The Bitter Lesson.

Source: http://www.incompleteideas.net/IncIdeas/BitterLesson.html

Sutton's observation, drawn from 70 years of AI research: hand-encoded human knowledge helps in the short term, then plateaus, then actively inhibits progress. General methods that leverage computation win every time. Chess engines with hand-crafted heuristics lost to search. Go knowledge lost to self-play. Phoneme rules in speech recognition lost to learned representations. The arc repeats in every domain.

[IMAGE: two curves over time on a dark chalkboard, "hand-encoded knowledge" rising fast then flattening into a plateau then bending down labeled "inhibits", "general methods + compute" starting lower but crossing over and continuing up, crossover point circled]

![[stop-giving-examples-bitter-lesson-crossover-1.png]]
![[stop-giving-examples-bitter-lesson-crossover-2.png]]
![[stop-giving-examples-bitter-lesson-crossover-3.png]]
![[stop-giving-examples-bitter-lesson-crossover-4.png]]
![[stop-giving-examples-bitter-lesson-crossover-5.png]]

Your prompt examples are hand-encoded human knowledge at prompt scale. They gave you a fast start. They carried you through the weak-model era. And now, on models past the crossover point, they are the thing holding the output back.

The bitter part of the lesson is that it always feels wrong to delete your carefully crafted knowledge. It felt wrong to chess programmers, and it will feel wrong when you strip your favorite skill file. Do it anyway.

---

## Anthropic Already Did This

You don't have to take the theory on faith. Watch what Anthropic did to their own product.

Claude Code's system prompt has cycled across model generations. In the Sonnet 3.5 era it was small. Then it grew large, packed with examples and tool instructions, because the models of that period needed the scaffolding. Now, in the Fable era, it's small again. They cut 80% of it.

[IMAGE: timeline across three model generations on a dark chalkboard, three system-prompt boxes sized small then large then small, labeled "Sonnet 3.5 era", "scaffolding era: many examples + tools", "Fable era: 80% removed", a curve over the boxes showing the rise and fall]

![[stop-giving-examples-prompt-size-cycle-1.png]]
![[stop-giving-examples-prompt-size-cycle-2.png]]
![[stop-giving-examples-prompt-size-cycle-3.png]]
![[stop-giving-examples-prompt-size-cycle-4.png]]
![[stop-giving-examples-prompt-size-cycle-5.png]]

And notice *what* they cut. Tariq again: "we really try and avoid being like do not do this." Not just fewer examples. Fewer constraints of every kind. The replacement is context: tell the model what you're trying to achieve and what situation it's operating in, then get out of the way.

The best prompt engineers at the company that makes the model are converging on the same move. Less demonstration. More intent.

---

## The Experiment

Theory is nice. Let's prove it on camera. I ran this exact experiment before filming, and we're going to rerun it live.

The task is deliberately boring: "write 8 new test cases for parseDuration('1h30m') → seconds." A duration-string parser. Every codebase has one.

[IMAGE: two subagent boxes side by side on a dark chalkboard, both fed the identical task card "8 test cases for parseDuration", left box labeled "Condition A: 8 examples" with a thick stack of example cards, right box labeled "Condition B: 1 example" with a single card, same model logo on both]

![[stop-giving-examples-ab-setup-1.png]]
![[stop-giving-examples-ab-setup-2.png]]
![[stop-giving-examples-ab-setup-3.png]]
![[stop-giving-examples-ab-setup-4.png]]
![[stop-giving-examples-ab-setup-5.png]]

1. Spawn two parallel subagents on the same model, with the identical task.
2. Condition A gets 8 few-shot examples, all happy-path hours and minutes: '1h' → 3600, '2h30m' → 9000, and so on.
3. Condition B gets exactly 1 example: '1h30m' → 5400.
4. Run both, then put the outputs side by side on screen.

Here's what Condition A produced: '90m' → 5400, '5h' → 18000, '1h45m' → 6300, '4h20m' → 15600, '0m' → 0, '0h' → 0, '12h' → 43200, '6h5m' → 21900.

All 8 test cases stayed inside the exact h/m grammar of the examples. Two edge categories total: zero values, and minutes over 60. No new units. No invalid input. No empty string. It didn't write test cases. It cloned the examples' distribution.

Now Condition B: '90s' → 90, '3h' → 10800, '15m' → 900, '2h15m30s' → 8130, '0m' → 0, '90m' → 5400, '1m60s' → 120, and '' → 0.

Same model. Same task. But B invented the seconds unit. It tested the empty string. It tested '1m60s', an un-normalized carry, which is a genuinely sharp parser edge case. Five to six distinct edge categories versus A's two.

[IMAGE: side-by-side output columns on a dark chalkboard, Condition A's 8 cases all shaded the same color inside a tight boundary box with a tally "2 edge categories", Condition B's 8 cases in five different colors spilling outside the boundary with a tally "6 edge categories"]

![[stop-giving-examples-edge-categories-1.png]]
![[stop-giving-examples-edge-categories-2.png]]
![[stop-giving-examples-edge-categories-3.png]]
![[stop-giving-examples-edge-categories-4.png]]
![[stop-giving-examples-edge-categories-5.png]]

5. Count the edge-case categories on screen, A versus B, and let the gap speak.
6. One note for rigor: we run each condition 3 times and count categories across runs. A single run proves nothing, n=1 is vibes. The gap holds across runs.
7. Then the payoff move. Take a real, example-heavy skill file from this repo, strip it down to intent plus context, and rerun it on its actual job. Watch the output get more inventive, not less reliable.

One more thing the demo shows, and I want you to see it honestly: look at B's seconds-unit cases. Is 's' even in this parser's spec? Arguably not. B invented beyond the requirement. That's not a bug in the argument, it's the second half of it, and it sets up the rule that makes all of this safe.

---

## The Rule: Examples Down, Intent Up

Cutting examples without raising intent doesn't produce creativity. It produces drift. Condition B wandering into a seconds unit nobody asked for is exactly what unmanaged tails look like.

So the rule has two halves that move together: **as examples go down, intent must go up.**

[IMAGE: seesaw on a dark chalkboard, left side "examples" sinking down with a stack of example cards sliding off, right side "intent" rising up with a single bold paragraph icon, pivot labeled "same total guidance", below the seesaw a broken version with both sides down labeled "drift"]

![[stop-giving-examples-intent-seesaw-1.png]]
![[stop-giving-examples-intent-seesaw-2.png]]
![[stop-giving-examples-intent-seesaw-3.png]]
![[stop-giving-examples-intent-seesaw-4.png]]
![[stop-giving-examples-intent-seesaw-5.png]]

Instead of 8 demonstrations, you write one paragraph that says what you actually want: "Test cases for a duration parser that only supports hours and minutes. Cover malformed input, boundary values, and normalization. Stay inside the h/m grammar." That paragraph costs fewer tokens than the examples it replaces, and it steers the tails instead of clipping them.

And to be clear, this is not "never use examples." Three honest caveats:

- **Strict schemas and exact house styles still want 1-2 examples.** If the output must match a precise format, JSON shape, frontmatter block, commit message convention, show one. Format is exactly what examples teach well.
- **Cheaper models still benefit from more examples.** Your haiku-tier subagents are pre-crossover. The old advice still applies to them. Match the technique to the model.
- **Intent is not optional.** Fewer examples with no added intent is just a vaguer prompt.

The skill here is knowing which side of the crossover your model is on, and packing the guidance accordingly.

---

## The Ritual

Here's what to do the moment this video ends. Open your most-used skill file or your CLAUDE.md, and for every example in it, ask one question:

**"Is this teaching format, or capping imagination?"**

[IMAGE: decision fork on a dark chalkboard, an example card entering a diamond labeled "format or imagination cap?", format path leading to a small "keep, 1-2 max" bin, imagination-cap path leading to a swap arrow where the card is replaced by a single paragraph labeled "one paragraph of intent"]

![[stop-giving-examples-format-fork-1.png]]
![[stop-giving-examples-format-fork-2.png]]
![[stop-giving-examples-format-fork-3.png]]
![[stop-giving-examples-format-fork-4.png]]
![[stop-giving-examples-format-fork-5.png]]

If it's teaching format, keep it. One or two, maximum. If it's showing the model what good output looks like, hoping the model will generalize, it's capping imagination. Delete it and replace it with one paragraph of intent that says what you want and why.

Most files I audit lose more than half their examples to this test. Every one of them got better.

---

## Key Insight

> Examples don't just show the model a format, they define a distribution, and on a frontier model whose own distribution is richer than yours, every example past the second one clips the exact tails where the best output lives. Trade demonstrations for intent.

---

## The Close

You spent the weak-model years learning to show the model what you want. The frontier-model skill is the opposite: say what you want, give it the situation, and let a distribution bigger than your imagination do the exploring.

Go strip a skill file today. The model was always more imaginative than your examples. Now you'll get to see it.
