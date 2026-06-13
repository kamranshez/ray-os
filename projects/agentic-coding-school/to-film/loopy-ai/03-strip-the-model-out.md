---
duration: "10-14 min"
batch: 1
order: 3
batch_name: "Setup"
class: "loopy-ai"
chapter: "Strip The Model Out"
aliases: [strip-the-model-out]
---

The fastest way to understand a loop is to build one with no model in it at all.

That sounds backwards. This is a class about AI agents. But almost every new student walks in with the same wiring fault: the word "loop" and the word "LLM" have fused into one thing in their head. They can't see the loop because the model is standing in front of it.

So we're going to pull the model out. Cron, bash, a static check, a state file. A loop that runs, checks itself, and stops, with nothing intelligent anywhere inside it. Once you've felt that rhythm, dropping a model into one slot becomes obvious. And more importantly, when something breaks later, you'll know whether it was the loop or the model.

---

## What everyone gets wrong

Watch someone build their first agentic loop and it fails. Ask them why. They can't tell you.

Not because they're not smart. Because they built the loop and the intelligence at the same time, in the same breath, and now they have one tangled object that either works or doesn't. When it doesn't, every part is a suspect. Was the prompt bad? Did the model hallucinate? Did the loop never fire? Did it fire but never stop? Did it lose its place between runs? They don't know, because they never built the version where there was nothing to blame but the wiring.

This is the step almost every failed loop builder skipped. They started at L2 with a model in the middle and never saw the deterministic skeleton underneath it. So when the skeleton is the problem, they keep poking the model.

[IMAGE: dark canvas, a tangled knot labeled "loop + model" with a single confused person staring at it, question marks around it]
![[images/strip-the-model-out/tangled-loop.png]]

The skeleton is cheap to build. An afternoon, no API key. And it buys you a diagnostic skill that pays for itself the first time a real loop misbehaves. That's the whole trade this segment makes.

Remember the stack from the last segment. L0 is the model. Everything from L1 up is structure you build around it. This segment is about seeing that structure naked, before any intelligence sits inside it.

---

## The five primitives

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
![[images/strip-the-model-out/five-primitives.png]]

---

## Loop one: the uptime checker

Let's build a real one. No model anywhere.

Goal: every five minutes, check whether your homepage returns a 200. If it fails, retry up to three times. On the third straight failure, post to Slack. Then reset.

Map it to the five primitives before writing a line.

- **Trigger:** cron, every five minutes.
- **Work:** `curl` the homepage, read the status code.
- **Check:** is the status code 200?
- **Terminate:** this loop never really terminates, it runs forever on the cron cadence. But each burst of retries terminates after three failures or one success.
- **State:** a file on disk holding the current consecutive failure count.

That state file is the part beginners drop, and it's the part that matters most. Without it, every cron run is amnesiac. It can tell you "the site is down right now," but it can't tell you "the site has been down three checks in a row," because it has no memory of the previous checks. The whole "alert on the third failure" behavior lives entirely in that one integer on disk.

The work is a `curl` and an `if`. The check is comparing a number to 200. The trigger is a single line in your crontab. None of it is intelligent. All of it is a loop. You can watch the failure count tick up in the state file in real time, watch it reset to zero when the site recovers, and watch the Slack message fire on exactly the third bad check.

Sit with that for a second. That is a closed loop doing useful, stateful, self-checking work, and there is not one token of inference anywhere in it.

---

## Loop two: the markdown gate

One example could be a fluke. Build a second, shaped completely differently, so the pattern separates from the specifics.

Goal: watch a folder for new markdown files. For each new file, run `markdownlint`. Write a `.passed` or `.failed` marker next to it.

The five primitives again.

- **Trigger:** a file appears in the watched folder. Different trigger from loop one, same slot.
- **Work:** run `markdownlint` against the new file.
- **Check:** did the linter exit clean, or did it report violations?
- **Terminate:** the loop ends when there are no unprocessed files left in the folder.
- **State:** the `.passed` and `.failed` markers on disk, which record what's already been handled so the loop doesn't reprocess the same file forever.

Notice what changed and what didn't. The trigger went from a clock to a file event. The check went from an HTTP status to a linter exit code. The state went from a counter to marker files. But the five slots are identical. The shape is the same. That's the point of building two: the primitives are invariant, the contents swap.

And again, zero intelligence. `markdownlint` is a borrowed verifier in the exact sense we'll lean on hard in the closing-the-loop segments. It's a check that lives outside the thing being checked. It just happens to be a deterministic tool instead of a model.

---

## The reveal: drop the model into one slot

Now the magic trick, and it's almost an anticlimax, which is the lesson.

Take loop two. When a file fails the lint check, instead of just writing a `.failed` marker, do one new thing: hand the file and the linter's complaints to a model and ask it to fix the violations. Then re-run `markdownlint`.

That's it. You changed exactly one slot. The **work** slot got smarter. Everything else stayed deterministic. The trigger is still a file event. The check is still `markdownlint` exit code, still external, still uncheatable by the model. The terminate condition is still "no unprocessed files." The state is still marker files on disk.

And look what you just built. A thing that takes work in, applies a model, verifies the result against an external check, and loops until the check passes. That's L2. The builder-verifier loop from the stack. You arrived at it by changing one box in a diagram you already understood.

[IMAGE: dark canvas, two loop diagrams side by side, identical five-box layout, left one labeled "deterministic L1-ish" with all boxes plain, right one with only the work box swapped for a glowing model-call box labeled "L2", everything else unchanged]
![[images/strip-the-model-out/swap-one-slot.png]]

This is why I make you build the skeleton first. When the model is just a swappable slot, you can reason about it. You can ask "is the model the problem, or is the slot around it the problem?" The people who never built the skeleton can't ask that question, because to them the whole loop is the model.

---

## The diagnostic this unlocks

Here's the skill you walk away with, and it's worth more than the two scripts.

When any AI loop of yours is misbehaving, ask one question: would the deterministic version of this loop work?

Mentally strip the model out. Replace the smart slot with a dumb placeholder that returns a canned answer. Now run the loop in your head. Does the trigger fire? Does state persist? Does the check ever pass? Does it terminate?

If the deterministic version works fine, the model is your problem. Bad prompt, wrong model, context too full. Go fix the slot.

If the deterministic version is also broken, the model was never your problem. Your loop design is broken. The trigger isn't firing, or state isn't surviving between runs, or the check never returns clean so nothing can ever exit. No amount of prompt engineering saves a loop whose skeleton doesn't close.

That single question routes you to the right half of the system in seconds. Most people burn an hour tuning a prompt to fix a loop whose state file was never being written.

---

## Demo

On screen, four moves, no slides, just terminals.

1. Show the crontab entry for the uptime checker. One line. Read it out: every five minutes, run this script.
2. Run the script live against a URL you control. `cat` the state file: failure count is zero. Now take the site down. Re-run. Watch the counter in the file tick to one, then two, then three. On three, the Slack message lands on screen. Bring the site back. Re-run. Watch the counter reset to zero on disk.
3. Switch to loop two. Drop a clean markdown file in the watched folder, watch a `.passed` marker appear. Drop a messy one, watch a `.failed` marker appear and print the `markdownlint` violations.
4. The swap. Edit one slot of loop two so a failed file gets handed to `claude` with the violations, then re-linted. Drop the same messy file back in. This time watch it go failed, then fixed, then `.passed`, all on its own. Point at the diagram: one box changed, you now have an L2 loop.

Total demo: about three minutes. The whole arc is "no model, no model, still no model, now one model in one slot, and nothing else moved."

---

## Key Insight

> A loop is five primitives: trigger, work, check, terminate, state. The model is just one swappable slot. Build the loop with no model first, and forever after you can tell whether it's the loop that's broken or the brain inside it.

---

## Where we go next

You now have the skeleton and the diagnostic. Every loop in the rest of this class is these five primitives with smarter and smarter things dropped into the slots.

Next segment we take the on-ramp seriously: the essentials that make L1 actually usable for long-running work, so the "work" slot is something you can trust. Then we close the loop properly, where that check slot stops being `markdownlint` and starts being a real verifier you went and borrowed.

But the framing holds the whole way up. Verification is a loop primitive, not a model feature. Governance is a loop primitive, not a model feature. We're going to keep wiring models into these slots, never around them.

See you in the next one.
