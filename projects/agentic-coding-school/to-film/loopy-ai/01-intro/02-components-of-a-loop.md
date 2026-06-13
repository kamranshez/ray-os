---
duration: 10-14 min
batch: 1
order: 2
batch_name: Setup
class: loopy-ai
chapter: Intro
aliases: [components-of-a-loop, anatomy-of-a-loop]
---
## The five components

Every loop, at every level of the stack, is made of exactly five things. Strip any one out and the loop breaks in a specific, nameable way.

- **Trigger.** What fires the loop? Cron, a file change, a new queue item, a manual run. This sets the cadence.
- **Work.** What runs in one iteration? The single unit of actual doing.
- **Check.** Did this iteration succeed? Some signal, separate from the work, that tells you yes or no.
- **Terminate.** Should the loop keep going? The condition that lets it stop, or keeps it alive.
- **State.** What survives between iterations? The memory that lets the loop resume, retry, and learn instead of starting from zero every time.

I'm not borrowing these from control theory or OODA. Those frameworks have different commitments and they'll lead you astray here. Five is just the minimum set where each primitive answers a question the loop physically cannot avoid.

Pull one out and you can predict the failure exactly. No trigger and the loop never starts, or starts on the wrong cadence. No work and nothing happens. No check and you can't tell a success from a failure, so the loop runs blind. No terminate and it runs forever, which is how you wake up to a thousand dollar bill. No state and every iteration starts from scratch, so the loop can never retry intelligently or pick up where it left off.

That list is the real prize of this segment. When a loop misbehaves, you don't say "the agent is broken." You say "the check is misfiring" or "the terminate condition never trips." You name the primitive. That's a five-way diagnosis instead of a shrug.

[IMAGE: dark canvas, five labeled boxes in a ring with arrows flowing between them, trigger to work to check to terminate, with a state box in the center connected to all of them]
![[loopy-strip-the-model-out-five-primitives-1.png]]
![[loopy-strip-the-model-out-five-primitives-2.png]]
![[loopy-strip-the-model-out-five-primitives-3.png]]
![[loopy-strip-the-model-out-five-primitives-4.png]]
![[loopy-strip-the-model-out-five-primitives-5.png]]