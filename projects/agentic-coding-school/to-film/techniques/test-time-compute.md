---
duration: "12-16 min"
batch: 1
order: 1
batch_name: "Multi-Agent Orchestration"
class: "techniques"
chapter: "Multi-Agent Orchestration"
---

## There Is a Volume Knob on Intelligence

Here is the idea this whole video turns on. The quality of what an agent gives you is mostly a function of how much compute it spends thinking, not how clever your prompt is. And that compute is something you control. You can turn it up.

Most people never touch the knob. They rewrite the prompt for the fifth time, swap a few words, add another bullet of instructions, and wonder why the answer is still mediocre. They are tuning the wrong thing.

The thing worth tuning is how many tokens the model is allowed to burn on your problem before it answers. That number has a name. It is called test-time compute, and once you can see it, you stop polishing prompts and start spending compute on purpose.

---

## What Everyone Gets Wrong

Watch how a typical person uses an agent. They type a request. The output is okay, not great. So they edit the wording. Still okay. They add "be thorough" and "think carefully." Marginally better. They give up and fix it by hand.

The whole time, they are treating the prompt as the lever and the tokens as a cost to keep down. Both instincts are backwards.

Boris Cherny runs Claude Code at Anthropic. He has written essentially all of his own code through the agent for months. His advice on cost is blunt.

> Use the most expensive model and focus on how do I get more out of it. Do not focus on cost cutting.

Source: Fireside Chat with Boris Cherny, Head of Claude Code, @Scale

That sounds reckless until you understand what he is actually saying. He is not saying waste money. He is saying you are optimizing the wrong variable. The return on a better answer is worth far more than the tokens it costs, so the move is to spend more compute and get more back, not to shave the bill and accept a worse result.

[IMAGE: dark background, two side by side axes. Left axis labeled "prompt cleverness" with a flat dotted line of quality that barely rises. Right axis labeled "tokens spent" with a solid line of quality climbing steeply. An arrow points from the flat one to the steep one with the word "tune this instead"]

![[ttc-wrong-axis-1.png]]
![[ttc-wrong-axis-2.png]]
![[ttc-wrong-axis-3.png]]
![[ttc-wrong-axis-4.png]]
![[ttc-wrong-axis-5.png]]

---

## What Test-Time Compute Actually Is

Strip away the jargon and it is almost embarrassingly simple. Here is how Boris defines it.

> Test-time compute is just a fancy way of saying how many tokens the model generates.

Source: Fireside Chat with Boris Cherny, Head of Claude Code, @Scale

That is it. More tokens generated at the moment you ask, more thinking before the answer, more attempts explored, more checking of the work. Training compute is fixed the day the model ships. Test-time compute is the part you get to dial up every single time you run it.

And the reason it works is not magic. A harder answer lives further out in the search space. To reach it the model has to reason through more steps, consider more branches, and discard more dead ends. Each of those is tokens. Starve it of tokens and it grabs the nearest plausible answer. Give it room and it can search for the right one.

This is the same reason a chess engine plays a stronger move when you let it search deeper. Same engine. Same position. More compute, better move. Intelligence at the moment of the question is bought, not just trained.

[IMAGE: dark background, a single search tree. Shallow version on the left stops at depth two and lands on a mediocre leaf. Deeper version on the right branches further, prunes wrong paths in grey, and reaches a highlighted correct leaf. Label the depth difference "more tokens"]

![[ttc-search-depth-1.png]]
![[ttc-search-depth-2.png]]
![[ttc-search-depth-3.png]]
![[ttc-search-depth-4.png]]
![[ttc-search-depth-5.png]]

---

## One Dial, Four Knobs

Here is what makes this practical instead of theoretical. You do not adjust test-time compute through some hidden setting. You adjust it through four moves you already half know, and the key realization is that they are all the same lever. They all do one thing: spend more tokens on the problem.

**Knob one, effort.** Recent Claude models let you set the reasoning effort directly: low, medium, high, extra high, max. This is the rawest form of the dial. You are literally telling the model how hard to think before it speaks. Low for drafting an email. Max for a gnarly architectural decision.

**Knob two, a bigger model.** Stepping from a fast cheap model up to the most capable one is spending compute too. It is the move Boris makes by default. Use the best model, then ask how to get more out of it.

**Knob three, use a workflow.** This is the one most people have never tried, and it is the most powerful. When the result is not good enough, you tell the agent to use a workflow, and it spins up an orchestration that fans your one request out across many subagents working in parallel, then verifies and synthesizes their work. One prompt becomes hundreds of coordinated agents. Boris describes it as orchestrating dozens, hundreds, even thousands of subagents.

**Knob four, loops.** A standing loop runs the agent again and again over time, each pass spending fresh compute to improve the same target. It is test-time compute spread across hours instead of seconds.

Four knobs. One dial. Effort turns it up in a single response, a bigger model turns it up per token, a workflow turns it up in parallel, a loop turns it up over time. Pick whichever fits, but understand you are always doing the same thing.

[IMAGE: dark background, four small levers on the left each labeled effort, bigger model, use a workflow, loops. Lines from all four converge into one large central dial labeled "tokens spent on the problem". An arrow from the dial points right to a bar labeled "output quality"]

![[ttc-one-dial-four-knobs-1.png]]
![[ttc-one-dial-four-knobs-2.png]]
![[ttc-one-dial-four-knobs-3.png]]
![[ttc-one-dial-four-knobs-4.png]]
![[ttc-one-dial-four-knobs-5.png]]

---

## Why "Use a Workflow" Hits Hardest

Effort and model size scale one agent thinking harder. A workflow scales the number of independent attempts and adds a layer that checks them. That is a different kind of leverage.

When you fan a problem out across many subagents, you are not just thinking longer, you are searching wider. Several agents attack the problem from different angles, the weak attempts get filtered, and the strong ones get combined. More independent tries plus verification is exactly how you escape the single confident wrong answer that a one-shot prompt so often gives you.

Boris gives a concrete number. He pointed one vague prompt at his continuous integration setup, told it to use a workflow, and walked away. It ran for a few hours, spent a few million tokens, and came back having shipped four pull requests that made the pipeline meaningfully faster. He did not write a better prompt. He spent more compute.

There is a clean example sitting right in front of us. To analyze a single forty minute video for this class, I ran a workflow that spent over half a million tokens across thirteen agents. A single agent reading the transcript would have given me a flat summary. The workflow gave me ranked, verified, buildable ideas, because the compute went into independent extraction, an adversarial spine panel, and a synthesis pass. The dial was the difference.

[IMAGE: dark background, flow diagram. One box on the left labeled "one prompt: use a workflow" feeds an orchestrator. The orchestrator fans out to a row of many small agent boxes working in parallel. Their outputs funnel through a box labeled "verify and synthesize" into a single box on the right labeled "result". Caption underneath: "more tries plus checking, not one longer guess"]

![[ttc-workflow-fanout-1.png]]
![[ttc-workflow-fanout-2.png]]
![[ttc-workflow-fanout-3.png]]
![[ttc-workflow-fanout-4.png]]
![[ttc-workflow-fanout-5.png]]

---

## When Not to Turn It Up

A dial you can only turn one way is a trap, so here is the honest boundary. Spending more compute is not free quality, and there are tasks where it does nothing.

The first limit is diminishing returns. The quality curve climbs steeply at first, then flattens. The first jump from a one-shot answer to a workflow is enormous. The tenth subagent matters far less than the first. Past a point you are paying tokens and latency for almost nothing, so read the curve and stop where it bends.

The second limit is harder and matters more. Compute only buys quality on problems that have a searchable, verifiable answer. Refactors, bug hunts, test coverage, code review, research with checkable claims. Those reward more search. But judgment problems do not. Boris is candid that the model still loses to him on product sense, on idea generation, on distributed system design. Pointing a workflow at "what should we build next" does not produce a better strategy, it produces a more elaborate average one. There is a wall where human judgment is the constraint, and no amount of tokens climbs it.

So the rule is simple. If the task has a right answer you could check, spend compute freely. If the task is bounded by taste or judgment, the dial does nothing and your attention is the real lever.

[IMAGE: dark background, a curve of output quality against tokens spent. It rises fast then flattens into a plateau. A horizontal dashed ceiling line sits above the plateau labeled "human judgment wall". Shade the early steep region green and label it "spend here", shade the flat tail grey and label it "wasted"]

![[ttc-diminishing-returns-1.png]]
![[ttc-diminishing-returns-2.png]]
![[ttc-diminishing-returns-3.png]]
![[ttc-diminishing-returns-4.png]]
![[ttc-diminishing-returns-5.png]]

---

## Demo

1. Take one genuinely hard task, a bug that spans several files, and run it once at default with a normal prompt. Show the mediocre patch and a missed edge case.
2. Run the exact same prompt, change nothing about the wording, and set reasoning effort to max. Show the better diff. First turn of the dial, same words.
3. Run it a third time with "use a workflow." Show the orchestration fanning out to parallel subagents, one finding the bug, others verifying the fix against other call sites. Show the cleaner result and the token count it cost.
4. Put the three outputs side by side with their token counts underneath. Make the trade visible: tokens up, quality up, prompt unchanged.
5. Then run the counter example. Point a workflow at a pure judgment question like "what feature should we build next." Show that the elaborate multi-agent answer is no better than the one-shot answer. Prove where the dial stops working.

---

## Key Insight

> Output quality is a dial, and the dial is tokens. Effort, a bigger model, use a workflow, and loops are four ways to turn the same knob. Stop polishing the prompt and start spending compute, but only on problems that have an answer worth searching for.

---

## What Changes After This

You stop rewriting prompts in a loop and start asking a better question: is this answer worth more compute. When it is, you have four ways to buy it on demand. When it is not, you stop spending and bring your own judgment. The prompt was never the bottleneck. The compute behind it was, and now it is yours to turn up.
