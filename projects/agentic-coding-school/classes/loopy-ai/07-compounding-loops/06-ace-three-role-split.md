---
video_id: "6ZQO9rok"
duration: "14-18 min"
batch: 6
order: 22
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "The Three Role Split (ACE)"
aliases: [ace-three-role-split]
---

There is a way to make a model get better at a task without ever touching its weights. You don't fine-tune it. You don't run reinforcement learning. You don't even buy a GPU. You change what the model reads before it works, and you let a loop keep changing it.

That's the whole idea. And in October 2025, three labs gave it a name, a benchmark, and a clean three-part shape.

This is the segment where the class snaps into focus. Because once you see this shape, you're going to realise you've been building pieces of it since the second video. Every loop we've made so far has had two of these three roles. Today we name the third one, and the stack you've been climbing turns out to have been one architecture the entire time.

---

## The thing everyone gets wrong about "self-improving"

When someone says an AI system "learns" or "self-improves," your brain jumps to weights. Training. The model itself getting smarter.

That's the expensive version. It needs data, compute, and a team. Almost nobody watching this is going to fine-tune a frontier model on their YouTube titles or their cold email or their codebase.

But here's the move people miss. The model is frozen. The model was always going to be frozen. The thing that actually decides how well your loop performs is not the weights, it's the instructions and lessons sitting in the context window when the model starts working.

And that context is fully under your control. It's a file. You can rewrite it. And if you can rewrite it, a loop can rewrite it.

So "self-improving" doesn't have to mean "the model changes." It can mean "the playbook the model reads keeps getting better, run after run, from the loop's own experience." Frozen model, evolving context. That's the entire trick, and it's been hiding in plain sight in everything we've built.

[IMAGE: dark canvas, split panel. Left: a brain icon labeled "weights" wrapped in a thick padlock, with "frozen / expensive / GPUs" underneath. Right: a document icon labeled "playbook" with an edit-pencil cycling around it, "rewritable / cheap / a file" underneath. A big equals-ish bridge showing both routes lead to "gets better over time"]
![[loopy-ace-three-role-split-frozen-model-evolving-context-1.png]]
![[loopy-ace-three-role-split-frozen-model-evolving-context-2.png]]
![[loopy-ace-three-role-split-frozen-model-evolving-context-3.png]]
![[loopy-ace-three-role-split-frozen-model-evolving-context-4.png]]
![[loopy-ace-three-role-split-frozen-model-evolving-context-5.png]]

---

## ACE: the three role split

The paper is called Agentic Context Engineering. Stanford, SambaNova, and UC Berkeley, October 2025.
Source: https://arxiv.org/abs/2510.04618

Their framing: stop treating the context as a tidy summary you compress down, and start treating it as an evolving playbook that accumulates strategies over time. To keep that playbook honest, they split the work across three roles. Not one model wearing three hats in one turn. Three distinct jobs.

**The Generator does the work.** It produces the actual reasoning trajectory, the attempt, the artifact. This is your L1 builder. Nothing new here. You've had a Generator since the first loop you ever ran.

**The Reflector reviews what the Generator did.** It looks at the attempt and the outcome and distills concrete lessons from the successes and the errors. Not "good job" or "try harder." Specific, named patterns. "The fix that touched the auth module regressed the session test, the second time this week."

Stop. You have already built this one.

The Reflector is the [[adversarial-reviewer-skill]] from the pair-every-creator-with-an-attacker segment. Same primitive. An asymmetric prompt whose job is to find what's wrong, run in fresh context so it isn't defending work it just produced. Back in that L2 segment, the attacker graded a single artifact and handed its complaints back into the same loop. ACE lifts that exact role out of the inner loop and runs it at a bigger altitude, across a window of attempts, feeding a playbook instead of a single retry. The mechanism didn't change. The scope did.

That's the moment I want to land on camera. Not "here is a new technique." It's "the technique you built in segment seven was one third of this all along."

**The Curator updates the playbook.** It takes the Reflector's lessons and writes them into the file the Generator reads before its next attempt. It's the role that captures the lesson, not the lesson itself. And it is a write role, which matters more than it sounds, and we'll come back to why.

[IMAGE: dark canvas, three boxes in a triangle. Top: "Generator — does the work". Bottom-right: "Reflector — names what went wrong". Bottom-left: "Curator — writes the playbook". In the dead center, a document labeled "PLAYBOOK". Arrows: Generator reads the playbook, Reflector reads the Generator's attempt, Curator writes the playbook, and a big loop-back arrow from Curator round to the Generator's next run]
![[loopy-ace-three-role-split-three-role-triangle-1.png]]
![[loopy-ace-three-role-split-three-role-triangle-2.png]]
![[loopy-ace-three-role-split-three-role-triangle-3.png]]
![[loopy-ace-three-role-split-three-role-triangle-4.png]]
![[loopy-ace-three-role-split-three-role-triangle-5.png]]

The loop reads: Generator works against the playbook. Reflector inspects the result and extracts lessons. Curator merges those lessons into the playbook. Generator runs again, now reading a slightly better playbook. Repeat.

The model weights never move. The Curator moves the context. Say it plainly: taste lives in the playbook, not in the weights.

---

## Why a third role and not "verifier with memory"

Here's the fair objection. We already have an L2 verifier. We've talked about state and scratchpads since strip-the-model-out. Why not just bolt a memory store onto the verifier and call it a day? Why does this need a whole third role?

Two answers, both structural.

**First, separation of concerns.** A verifier judges one artifact. Pass or fail, this thing, right now. The Reflector's job is different in kind. It looks across a window of iterations and extracts a pattern. "The Generator keeps over-fitting to the most recent failure." "Every fix that touches the pricing module regresses the tax test." That's a cross-iteration view. If you cram it into the verifier, you collapse it back into a single-shot judgment and the pattern disappears. The ACE authors are explicit about this: they want to avoid overloading one model with every responsibility, because that's where quality drops.

**Second, the Curator is a write role, not a memory role.** A memory store is passive. It's a log. Things go in and sit there. The Curator actively rewrites the playbook with structured, incremental edits. The paper calls them delta updates, small itemised bullet changes merged into the context by lightweight, deterministic logic rather than a model rewriting the whole thing each time.

That deterministic merge is the part worth slowing down on, because it fixes the failure mode that kills naive "just keep summarising the context" loops. The paper names two. Brevity bias: the optimiser keeps compressing toward a tidy short prompt and quietly drops the domain-specific lessons that actually mattered. And context collapse: every time a model rewrites the whole context wholesale, it erodes a little more detail, until your hard-won playbook has degraded into vague mush.
Source: https://arxiv.org/abs/2510.04618

A naive "verifier with memory" walks straight into both. The Curator's job is to prevent them. It grows the playbook in append-and-refine edits, dedups bullets, retires obsolete ones, and never lets one model bulldoze the whole file. That is not "verifier plus memory." It's a different job that happens to write to the same file the Generator reads.

---

## A design call you actually have to make

Once you split a loop into roles, you inherit a routing question, and it's a real one: when an attempt fails, what does the next planning step get to see?

Concretely. Say your loop plans, then a coder implements, then a verifier checks. The verifier fails the run. Now you're drafting plan version two. Does the plan author see the coder's raw diff? Or only the verifier's structured failure report?

This class commits to one answer: the structured failure report, not the diff.

The reasoning is about grain. The plan author works at plan altitude. Hand it the coder's raw diff and you've poured implementation-local detail into a role whose job is to think above implementation. It starts reasoning about line-level concerns it has no business owning, and coder-local noise leaks upstream into your planning. The right signal at plan altitude is "test X failed on assertion Y, the affected module is Z." That's a fact the planner can act on. The diff is the coder's local concern, and it should stay there.

This is closer to Anthropic's three-agent sprint-contract framing than to ACE's own Curator framing, and that's a deliberate pick. We're a class about loop design, not about weight-free continual learning research. If you ever flip this default for one of your own loops, write down why, because the wrong default quietly turns your three-role split back into two roles. You think you have a planner, a coder, and a checker. But if the planner is reading raw diffs, the planner has secretly become a second coder, and you've lost the separation you paid for.

---

## Why this is the asset, not the model

Three reasons this architecture is worth building, beyond "the paper says it scores higher."

**One, no cluster.** This is context engineering, not weight surgery. The paper reports it adapting effectively with no labeled supervision at all, just natural execution feedback, the same borrowed verifiers and real-world signals we've been wiring up since segment six. Anyone can run this. You can run this tonight.

**Two, the numbers hold up under a skeptical look.** On the AppWorld agent benchmark, ACE reported +10.6% on agent tasks. In the offline setting, ReAct plus ACE beat plain in-context learning by 12.3% and beat GEPA, a strong prompt optimiser, by 11.9%. They ran it on DeepSeek-V3.1, a smaller open-source model, and still matched the top production agent on the leaderboard average.
Source: https://arxiv.org/abs/2510.04618
Don't quote the bare headline number to a skeptical learner. Quote the comparison. The gain is over in-context learning and over a real optimiser, not over a strawman.

**Three, and this is the one that matters most for you. The playbook survives model swaps.** Your taste lives in a file, not inside Sonnet's weights. When you upgrade to next year's model, your taste files come with you, unchanged. That is a compounding asset that sits on top of the model instead of being locked inside it. Every lesson your loop learns this year is still yours next year on a better base model.

That reframes the whole idea of prompt engineering. It was never a one-shot writing task where you craft the perfect prompt and walk away. It's a Curator role. A loop that keeps editing the playbook against real feedback. You're not the prompt author. You're the thing that hired the Curator.

[IMAGE: dark canvas, a horizontal timeline. A "playbook.md" file glides along it, unchanged, while the model underneath it swaps from "Sonnet 4.6" to "Sonnet 5.0" to "next year's model". Caption arrow: "the asset rides on top of the model, not inside it"]
![[loopy-ace-three-role-split-playbook-survives-model-swaps-1.png]]
![[loopy-ace-three-role-split-playbook-survives-model-swaps-2.png]]
![[loopy-ace-three-role-split-playbook-survives-model-swaps-3.png]]
![[loopy-ace-three-role-split-playbook-survives-model-swaps-4.png]]
![[loopy-ace-three-role-split-playbook-survives-model-swaps-5.png]]

---

## Demo

Let me break open one of my real loops on screen so you can see the three roles as actual files, not as a diagram.

One. The Generator. I open the Generator prompt for my title-experiment loop. It's a normal skill. "Here's the video, here's the playbook of what's worked, produce candidate titles." Point at the line where it reads `playbook.md`. That line is the whole architecture in one breath: the builder reads the evolving context before it builds.

Two. The Reflector. I open the Reflector prompt next to it. Notice it is the adversarial reviewer prompt, barely modified. Same asymmetric "default to disagreement, name the specific failure" shape from segment seven. The only change is its input. The L2 attacker read one artifact. This Reflector reads the last week of attempts plus the real-world outcome on each, and its output is not a pass/fail, it's a list of named lessons. Read two of them aloud. "Titles leading with a number under-performed curiosity-gap openers three weeks running." That's a pattern, not a verdict.

Three. The playbook. I open `playbook.md`. It's just a bulleted markdown file. Lessons, each one earned. This is the Curator's output, the file it maintains.

Four. The Curator's diff. Now the part I actually want you to feel. I run `git log -p playbook.md` for the last week. We scroll the diffs. Here's a bullet added after a losing test. Here's a bullet refined when a sharper version of the same lesson showed up. Here's one deleted because it went obsolete. The diff is the learning, made visible. Reading it is exactly like reading a code review of your own taste.

Total demo, about five minutes. The takeaway I want on screen: there's no magic object here. There's a builder, an attacker you already know how to write, and a markdown file under version control. That's the entire self-improving system.

---

## Key Insight

> You don't make a model smarter by changing its weights. You make it smarter by hiring a loop to keep editing the playbook it reads. Frozen model, evolving context. The taste is in the file, and the file is yours forever.

---

## Where we go next

You now have the canonical shape. Generator, Reflector, Curator, looping around a playbook. Keep that playbook in version control, because the diff is the learning.

Next we look at a specific, powerful instance of this split, the teacher-learner pattern, where one role's whole job is to grow the other. After that, an ACE running in production: the bug-triage loop. And later, the segment this one quietly set up, where we ask where taste actually went once the loops took over. The answer is sitting in the Curator's commit history.

See you in the next one.
