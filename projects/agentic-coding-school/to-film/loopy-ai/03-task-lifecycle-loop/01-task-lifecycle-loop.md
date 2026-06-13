---
duration: 10-14 min
batch: 2
order: 4
batch_name: L3 Task Lifecycle
class: loopy-ai
chapter: L3 Task Lifecycle
aliases: [task-lifecycle-loop]
---

> STUB. L3 — one full deliverable, end to end. The closing-the-loop / Ralph / goal-mode segments (05–12) nest underneath this one.

## Kernel (from the old stack walkthrough)

Spec. Plan. Build, which uses L1 and L2 inside it. Review. Push. Verify in production.

One full deliverable, end to end. Multiple L2 loops nest inside. Humans are usually still in the loop at "review" and "push."

This is where Ralph loops live. Run the same prompt in a fresh context over and over against a PRD until the goal is met. The PRD is the spec, the work is the build, the git history is the verify.

This is where goal mode lives too. Set an objective. The runtime keeps the loop alive against that objective until it's met or the budget runs out.

[IMAGE: a flowchart, spec -> plan -> build -> review -> push -> verify, with the build box exploded out into a smaller L1/L2 stack]

![[loopy-loop-stack-l3-lifecycle-1.png]]
![[loopy-loop-stack-l3-lifecycle-2.png]]
![[loopy-loop-stack-l3-lifecycle-3.png]]
![[loopy-loop-stack-l3-lifecycle-4.png]]
![[loopy-loop-stack-l3-lifecycle-5.png]]

L3 is the unit of "I shipped one thing." Most people who say "I've used Claude for a real task" are working at L3, even if they don't have the vocabulary for it.

## Notes to incorporate

- The overclaim misnaming example (a Ralph loop is L3, not "autonomous") now lives in the intro; callback here.
- This segment is the bridge: it frames the cluster 05–12 (closing the loop, borrowed verifiers, Ralph, goal mode, writing goals) as the L3 toolkit.
