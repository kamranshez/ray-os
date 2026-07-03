---
duration: "12-16 min"
batch: 1
order: 1
batch_name: "Foundations"
class: "techniques"
chapter: "Foundations"
status: "scripted"
---

## The step it keeps skipping is not a discipline problem

Your agent skips a step because your prompt is over budget, not because it forgot. Adding another instruction to fix it makes it worse.

You already know from this class that a model has an instruction budget. You have seen it in your CLAUDE.md: pile on enough rules and the model stops following any single one reliably, which is why you split a bloated CLAUDE.md into files loaded on demand.

This video takes that exact same budget logic and points it at your prompts and your workflows. The mega-command. The do-everything skill. The one giant instruction block you keep bolting rules onto.

Same disease. Same cure. You do not write more prose. You split the work.

---

## What everyone does wrong

Here is the reflex. The agent runs your workflow and silently skips the research step. So you open the prompt and you add a line.

"And make sure you ALSO do the research before writing the plan."

It works once. Then it skips something else. So you add another line. And another. Your workflow command grows from twenty instructions to fifty to eighty-five, and every new rule was added to fix a step that got skipped.

You are treating a budget problem like a memory problem.

[IMAGE: a person feeding paper lines into the top of one fat box already overflowing, labeled 85 instructions, while several older rules quietly slide out a crack in the bottom of the box and fall away, an arrow labeled "add more" pointing in, an arrow labeled "silently dropped" pointing out]

![[images/split-the-mega-prompt/adding-instructions-backfires.png]]

The line you added did not get special treatment. It joined the pile. It is now one more instruction competing for attention against eighty-four others, plus your CLAUDE.md, plus the system prompt, plus every tool schema in the window. You did not raise the priority of the skipped step. You lowered the priority of everything.

That is the trap. The intuitive fix and the correct fix point in opposite directions.

---

## The core insight

A frontier model reliably follows about 150 to 200 instructions. Past that, it half attends to all of them and you are rolling the dice.

Source: Dexter Horthy (HumanLayer), "Everything We Got Wrong About Research-Plan-Implement," Coding Agents Conference, March 2026. "Frontier LLMs could only follow about 150 to 200 instructions with good consistency, anything more than that and it's half attending to all of them and you're rolling the dice."

So you do not fix a skipped step by adding prose. You fix it by decomposing one mega-prompt into a pipeline of small, single-purpose prompts.

Instead of one fat box holding eighty-five instructions, you get a row of small boxes. Questions. Research. Design. Plan. Implement. Each one under about forty instructions. Each one carrying only the rules that stage actually needs.

[IMAGE: left side, one fat box labeled "85 instructions" with rules faded grey and falling out the bottom; right side, a horizontal pipeline of five small boxes labeled Questions, Research, Design, Plan, Implement, each stamped "under 40", a small diamond router in front of the row routing an incoming arrow into one box]

![[images/split-the-mega-prompt/mega-vs-pipeline.png]]

Every instruction in a forty-instruction prompt sits comfortably under the reliability threshold. Nothing is competing in the noise. The step you cared about now fires because it is one of forty things the model is paying attention to, not one of eighty-five things it is half attending to.

---

## Why the budget actually runs out

This is not a metaphor. Follow the mechanism in two steps.

Step one. Attention is a fixed resource spread across every token in the context window. Your eighty-five instructions do not each get full attention. They share it. And they are not sharing it only with each other. They share it with your CLAUDE.md, your system prompt, and every tool and MCP schema loaded into the window.

Step two. Once no single instruction stands out from that crowd, compliance stops being deterministic and becomes probabilistic. The model is not choosing to skip your step. Each instruction now has a thinner slice of attention, so each one has a real chance of not firing on any given run.

[IMAGE: a single pie labeled "attention" sliced into many thin wedges, wedges labeled CLAUDE.md, system prompt, MCP tool schemas, rule 1, rule 2, rule 3, and so on, each wedge tiny, a caption reading "every token takes a slice"]

![[images/split-the-mega-prompt/attention-as-fixed-pie.png]]

That thinner slice is where the whole problem lives. Split the same work across stages and each prompt carries under about forty instructions, all of them above the line where the model follows reliably. You did not make the model smarter. You stopped starving each instruction.

And notice the tax hiding in that pie. Every extra MCP server you connect dumps its tool schemas into the same window. Too many servers and the tool instructions crowd out YOUR instructions. Trimming the MCP tools in your context is the same move as splitting the prompt. Both are you refusing to spend budget you do not need to spend.

---

## The magic words symptom

Here is how you diagnose an over-budget prompt without counting anything.

You found a secret phrase that makes it work. Some incantation you have to utter, like "work back and forth with me starting with your open questions and outline before writing the plan," and only then does the buried step actually fire.

That phrase feels like a power move. It is a warning light.

[IMAGE: a nervous person whispering a long secret phrase into a slot on a giant black-box machine, the machine finally lighting up green, a small red warning label on the side of the machine reading "over budget"]

![[images/split-the-mega-prompt/magic-words-warning-light.png]]

Think about what the magic phrase is doing. It is a burst of attention aimed at one buried instruction, loud enough to lift that one step above the noise for one run. It works because everything else is under-attended. The incantation is you manually paying the budget the prompt should never have needed.

If your workflow only behaves when you say the magic words, that is not user error. It is a signal you are over budget.

Dex puts the standard bluntly. If you built a tool that needs hours of training and secret phrases to work, go fix the tool.

Source: Dexter Horthy (HumanLayer), "Everything We Got Wrong About Research-Plan-Implement," Coding Agents Conference, March 2026.

The fix is not a better incantation. The fix is a smaller prompt, where the step you wanted fires on its own because nothing is drowning it out.

---

## Control flow for control flow

Here is the principle that does the real work.

Don't use prompts for control flow if you can use control flow for control flow.

Source: Dexter Horthy (HumanLayer), "Everything We Got Wrong About Research-Plan-Implement," Coding Agents Conference, March 2026. "Don't use prompts for control flow if you can use control flow for control flow."

Look at what your mega-prompt is actually doing. Half of it is branching. "If it's a bug, do this. If it's a feature, do that. If it's a refactor, do this other thing." You wrote all three branches into one prompt and asked the model to pick the right one AND execute it, every single run.

That is spending your instruction budget on routing. The model burns attention deciding which branch it is in before it does any real work, and it is holding all three branches' rules in context the whole time.

So route first. Deterministically. Classify the input with a simple if statement or a cheap classifier, then hand it to the one small prompt for that branch.

[IMAGE: top, one fat prompt box containing three stacked if-branches bug/feature/refactor, the model juggling all three at once; bottom, a diamond classifier out front that reads the input and routes a single arrow to exactly one of three small prompt boxes, the other two greyed out and never loaded]

![[images/split-the-mega-prompt/route-then-run.png]]

The if statement is really powerful, and LLMs are really good at classifying things. Classifying "is this a bug or a feature" is a tiny, reliable task. Use the model for the one thing it is great at, the classification, then let ordinary code route to the branch. The branch prompt that runs only holds its own rules. The other two branches never enter the window.

You just moved the routing out of the budget. Every instruction that survives is instruction spent on the actual work.

---

## This is a pattern you already know

Strip the AI vocabulary and you are looking at microservice design. The Unix pipeline. The single-responsibility principle.

You would never write one two-thousand-line function that handles every case with a wall of nested if statements. You write small single-responsibility units and let a router compose them. One does one thing. You can read it, test it, and swap it without touching the others.

[IMAGE: left, one giant tangled function box labeled "do_everything()" with a snarl of nested branches inside; right, the same work as a Unix pipe of small labeled stages joined by pipe symbols, classify then a single stage running, clean and linear]

![[images/split-the-mega-prompt/monolith-to-pipeline.png]]

Control flow for control flow is just that old discipline pointed at prompts. It is the single-responsibility principle plus an if statement. You already trust this pattern in your code. Trust it in your workflows.

---

## How it goes wrong

I am not going to pretend this is free. Splitting has a real cost and there is a way to overdo it.

The cost is plumbing. You used to maintain one file. Now you maintain seven stage-prompts and the wiring between them. That is more surface area, more places for a handoff to break. So only split when the steps are genuinely separable. If the work is really one thing, one prompt is the honest answer.

[IMAGE: left, a tightly coupled task drawn as one connected blob being sliced down the middle by scissors, the two halves each missing a piece the other half was holding, a broken thread between them labeled "lost context"; right, a naturally segmented task with clean gaps, the scissors cutting exactly on the gaps, both halves intact]

![[images/split-the-mega-prompt/over-splitting-fractures-context.png]]

And the failure mode on the other side is over-splitting. Cut a truly coupled task into stages and you fracture its context. A later stage ends up missing something an earlier stage knew but never passed along. You traded one over-budget prompt for a pipeline that leaks information at every seam.

Read the shape of the work first. Genuinely separable stages, split them. One coupled task, leave it whole. The skill is knowing which one you are holding.

---

## Demo

Let me make this concrete, end to end.

1. **Show the failure live.** I run one fat workflow command. It is about eighty instructions of prose, and on top of that it is loading my CLAUDE.md and a stack of MCP tools. It runs, produces a plan, and silently skips the research step. The only way I ever got research to fire was by pasting a magic phrase at the end: "work back and forth with me starting with your open questions and outline before the plan." That is the instruction-budget symptom, out in the open.

2. **State the budget and count.** Reliable range is about 150 to 200 instructions. I run `/context` to see what is actually loaded, then I count the instructions in the command itself. Command plus CLAUDE.md plus tool schemas, I am well past the line. On screen, the number says I am over.

3. **Refactor into stages.** I carve the mega-prompt into a pipeline. Questions. Research. Design. Plan. Implement. PR. Six small prompts, each one holding only what that stage needs, each one under about forty instructions. The research step is no longer a buried line. It is an entire stage that exists on its own.

4. **Replace prompt branching with a router.** The old command tried to handle bug, feature, and refactor in one block. I rip that out and put a deterministic step in front: a one-line classifier that reads the request and picks the branch. Ordinary control flow selects the next stage-prompt. The model classifies. Code routes. Only the branch that wins ever loads.

5. **Re-run.** Same request, no magic words. The research step fires on its own because it is now one of forty things the stage is attending to, not one of eighty-five it was half attending to. Then I close on the honest cost, right there on screen: I now maintain a pipeline instead of a file, so I only split when the steps are genuinely separable.

---

### Key Insight

> When your agent skips a step, you are over budget, not misunderstood. Split the prompt, route with an if statement, and the step fires on its own.

---

You are going to stop reaching for the same broken fix. Next time an agent drops a step, you will not add a line. You will count your instructions, and if you are over, you will split.

The magic words go in the bin. The pipeline does the work.
