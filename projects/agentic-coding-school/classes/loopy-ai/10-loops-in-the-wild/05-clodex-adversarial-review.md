---
duration: "8-12 min"
batch: 9
order: 37
batch_name: "Loops In The Wild"
class: "loopy-ai"
chapter: "Clodex: Cross-Model Review"
status: "scripted"
aliases: [clodex-adversarial-review]
---

The build-test-fix pair put a verifier inside the loop. This one makes the verifier a different model entirely.

The idea is simple and a little ruthless: have Codex review Claude's pull requests before they merge, so two different model families have to agree before any code lands. One writes. A rival reads. They argue. Only work that survives both gets in.

This is the sycophantic-attackers idea from chapter three, taken to its logical end. The strongest possible verifier is one that does not share the builder's blind spots, and the cleanest way to guarantee that is to use a different model.

---

## The problem it kills

A model is a bad judge of its own work.

Not because it is dumb, but because the same training that makes it write a thing makes it like that thing. It has the same blind spots on review that it had on the first draft, so the bug it failed to write correctly is exactly the bug it will fail to catch. Self-review feels like a second pass. It is really the same pass, twice.

The fix is not a better prompt for the same model. It is a second model that was never in the room when the code was written.

---

## The loop

This is Lukas Kucinski's Clodex loop, and it is meant to be pasted verbatim.

```
/clodex [task] think hard --max-iter 5 --threshold medium
```

The two flags are the whole point. `--max-iter 5` lets the two models argue back and forth up to five times. `--threshold medium` sets the bar the work has to clear before it passes. Claude writes the change, Codex reviews it as an adversary, Claude answers or fixes, Codex reviews again, and this repeats until either the work clears the threshold or it runs out of rounds.

[IMAGE: dark canvas, two distinct model icons facing each other labeled Claude and Codex, an arrow from Claude to Codex labeled "PR", an arrow back labeled "review, try to break it", a counter showing "iter 1..5", and a single merge gate on the right that only opens when both icons show a checkmark]

![[loopy-litw-clodex-adversarial-review.png]]

---

## Why it works: independence is the whole trick

Chapter three told you a verifier has to be independent of the builder. This loop buys the strongest independence money can buy: a different model family.

When Claude reviews Claude, the reviewer shares the writer's instincts, so the two agree too easily and the bar quietly drops. When Codex reviews Claude, the reviewer brings a different training, different priors, different failure modes. It catches things Claude is constitutionally blind to, and Claude catches things Codex would miss in the other direction. The disagreement is the value. Two judges who never agree by reflex.

That is also why the iteration cap matters. Five rounds is enough for a real argument to converge. The loop is not asking one model to bless another, it is making them fight to a standstill and only shipping what survives.

---

## The catch

Two models cost two models.

Every round is a Claude turn and a Codex turn, and five rounds of that is not free. So this is not the loop you point at a typo fix. It is the loop you point at the change you actually care about getting right, the one where a missed bug costs far more than the extra tokens. Match the ceremony to the stakes. Cross-model review earns its cost on the risky diff and wastes it on the trivial one.

This is the same judgment from the governance chapter, applied to verification. The strongest verifier is also the most expensive one, so you spend it where it pays.

---

## Demo

Run Clodex on a change worth arguing about.

1. Show the task. A non-trivial diff, the kind with a real chance of a subtle bug. Say why it qualifies: the cost of getting it wrong is high.

2. Watch round one. Claude writes the change. Codex reviews it as an adversary and flags a genuine issue Claude did not see. Point at the screen: that is a different model catching a different model's blind spot.

3. Watch the argument. Claude answers the flag, adjusts the code. Codex reviews again. Show the threshold not yet met, so it goes another round.

4. Watch it converge. By round three the two stop finding new problems and the work clears the medium threshold. The merge gate opens only now, with both models satisfied.

5. Contrast with self-review. Re-run the same task with Claude reviewing Claude, and show the bug from round one sail straight through. That is the entire argument for the loop in one side-by-side.

Total demo: four minutes. The point is that two independent judges caught what one judge, no matter how good, structurally could not.

---

## Key Insight

> A model shares its own blind spots on review that it had on the first draft. The cleanest independent verifier is a different model family, made to argue until only the surviving code ships.

---

## Where we go next

That closes the cookbook. Five loops people are actually running: a verifier pair, a setpoint that picks its own work, an overnight routine, the brakes that keep a loop honest, and a rival model that has to agree before anything lands.

Every one of them is a shape you learned earlier in this class, wearing a command you can paste tonight. That was always the point. Stop being the thing in the loop. Write the loop, give it a verifier and a brake, and go decide what to build next.
