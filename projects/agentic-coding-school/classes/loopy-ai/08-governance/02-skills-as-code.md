---
video_id: "pR8zHoji"
duration: "10-14 min"
batch: 7
order: 27
batch_name: "L6 Governance"
class: "loopy-ai"
chapter: "Skills as Code"
aliases: [skills-as-code]
---

There is one fear that stops people from ever building a self-improving loop. Do you really want an agent rewriting its own instructions?

Yes. But not silently.

That one word is the whole segment. The difference between a loop that compounds and a loop that quietly goes insane is not how smart the rewrite is. It is whether a human ever sees the rewrite before it ships. Skills are files. Files go in a repo. And a repo gives you the three things that make self-modification safe: version history, review, and rollback.

This is the governance segment for the thing that scares people. The [[self-improvement-loop]] proposes changes to itself. [[teach-the-agent-to-learn]] makes those changes generalise instead of overfit. This segment is the gate they both have to pass through before anything becomes real.

---

## The fear is correct, the conclusion is wrong

The instinct is to never let the agent touch its own prompt. Lock the skill file. Only humans edit it.

That instinct is half right. An agent that silently mutates its own instructions, every run, with nobody watching, is exactly the horror story you imagine. By week three it has rewritten itself into something you never approved and cannot explain.

But the fix is not "never let it change." The fix is "never let it change without review."

Source: https://x.com/petradonka/status/2054897826149101588

> Yes, but not silently.

Hold onto the distinction. The danger was never the agent proposing a change. The danger was the change going live without a human in the path. Take the silence away and the fear goes with it. You get a loop that suggests improvements all day long, and a you that approves the ones worth keeping.

---

## Why skills are code

When an agent does a job once, the prompt is throwaway. You typed it, you got an answer, you moved on.

When an agent does the same job a thousand times, the prompt is not throwaway. It is production behaviour. Every reply it drafts, every issue it triages, every card it files runs through that skill file. The file is now the most leveraged piece of text in your whole system.

So treat it like what it is. Code.

Source: https://x.com/petradonka/status/2054897826149101588

> We make it safe by treating agent skills like code.

Read what that buys you. **Version history**, so you can see exactly when a principle entered the skill and what it replaced. **Review**, so a change is a thing someone looked at, not a thing that happened. **Rollback**, so when a new principle makes the loop worse, you revert one commit instead of archaeology. None of this is exotic. It is the same discipline you already apply to the application. You are just pointing it at the prompt, because the prompt is now the thing that determines what ships.

The mental shift is this. When work repeats, the prompt becomes the artifact you review. Not the output. The instructions that produce every output.

[IMAGE: dark canvas, left side a single throwaway prompt bubble feeding one answer then vanishing, faint and greyed. Right side the same prompt promoted into a SKILL.md file sitting inside a repo box with a commit history timeline beneath it, glowing. An arrow labeled "runs 1000x" crosses from left to right. Caption: "when a prompt repeats, it stops being a message and becomes production code".]
![[loopy-skills-as-code-prompt-becomes-code-1.png]]
![[loopy-skills-as-code-prompt-becomes-code-2.png]]
![[loopy-skills-as-code-prompt-becomes-code-3.png]]
![[loopy-skills-as-code-prompt-becomes-code-4.png]]
![[loopy-skills-as-code-prompt-becomes-code-5.png]]

---

## The PR is the governance surface

Here is the actual mechanism, and it is almost boring once you see it.

The outer learning loop does not edit the live skill. It opens a pull request. The loop proposes. It does not merge.

That single boundary is where all the safety lives. The loop runs unattended, reads a day of feedback, decides a principle should change, and writes that change into a branch. Then it stops and waits for you. Production does not move until a human moves it.

And the PR is not a bare diff. A good one shows three things, every time.

1. **The feedback it read.** The Slack reactions, the thread notes, the overrides it is responding to. You can see the evidence, not just the verdict.
2. **The principle it wants to change.** In words. "I think we should sharpen the rule about leading with empathy when a user is venting." The intent, before the diff.
3. **The exact diff to the skill file.** The literal lines added, removed, reworded.

You review it like any other change. Approve, request edits, or reject. The useful part of self-improvement survives, because the loop can propose improvements continuously and forever. The control survives too, because durable change only happens when you say so. That is the trade. The loop never veers off into a weird direction unsupervised, because the weird directions die in review.

[IMAGE: dark canvas. A single "outer loop" node emits an arrow that forks into two paths. Top path: arrow straight into a "production skill" box, labeled "silently mutate", marked with a red X. Bottom path: arrow into a PR card showing three rows (feedback read / principle delta / diff), then to a human check icon, then into the production skill box, then a loop-back arrow labeled "next run picks it up", marked with a green check. Caption: "the loop proposes, the human merges".]
![[loopy-skills-as-code-pr-gate-1.png]]
![[loopy-skills-as-code-pr-gate-2.png]]
![[loopy-skills-as-code-pr-gate-3.png]]
![[loopy-skills-as-code-pr-gate-4.png]]
![[loopy-skills-as-code-pr-gate-5.png]]

---

## This is not a fifth primitive

Be careful where you file this. It is governance, but it is not one of the four.

[[governance-primitives]] gave you budgets, kill switches, action-log review, and retirement. Those are brakes on what a loop **does**. They cap the spend, stop the runaway, surface the actions, and pause the dead weight. They watch the loop's output.

This is a brake on what a loop **changes about itself**. It watches the loop's instructions. Different surface entirely.

I am keeping it separate on purpose. The governance segment was strict: four primitives, no more, and a fifth thing is usually one of the four wearing a costume. Skills-as-code is not one of those four wearing a costume. It is a genuinely different control, the one you only need once a loop is allowed to edit its own skill. Most loops never reach that point. The ones that do, the compounding ones, need this gate before they are safe to leave running.

So: same category, its own segment. Governance over self-modification.

---

## Demo

Two minutes, one PR, deliberately unremarkable.

1. **The trigger.** The daily learning loop wakes up, reads yesterday's feedback out of the Slack channel from [[slack-as-your-command-center]], and decides the triage skill misfires on one class of issue. Show it running headless.

2. **The PR it opens.** Pull up the pull request. The title names the skill it wants to change: "Update triage-skill: sharpen the duplicate vs needs-info call." The body links the exact Slack threads it read and states the principle delta in plain words before any code.

3. **The diff.** Open the Files Changed tab. The change touches `SKILL.md` and nothing else. A few lines reworded, one principle added. Small. Reviewable in thirty seconds.

4. **You review.** Leave a comment asking it to soften one line, the same as you would on any teammate's PR. The loop pushes a fixup. Now merge.

5. **The next run.** Re-run the inner loop on a fresh issue. It picks up the merged skill and triages correctly. The improvement is live, and there is a commit with your approval on it explaining why.

The point of the demo is that it looks exactly like normal code review. That is the whole idea. You already know how to govern code. Make the skill code, and you already know how to govern the agent.

---

## Key Insight

> A self-improving loop is safe the moment its changes stop being silent. Skills are files, files go in a repo, and the pull request is where the loop proposes and you decide. Continuous proposal, gated merge.

---

## Where we go next

You now have the last brake. Not on what the loop spends or ships, but on what it lets itself become.

That completes governance. Budgets and kill switches keep the work in bounds. Skills-as-code keeps the self-improvement in bounds. Together they are what lets you walk away from a compounding loop and still sleep, because nothing it does, and nothing it changes about itself, happens where you cannot see it.

See you in the next one.
