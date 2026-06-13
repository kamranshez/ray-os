---
duration: "10-14 min"
batch: 8
order: 27
batch_name: "L7 Closing"
class: "loopy-ai"
chapter: "Mission Command"
aliases: [mission-command]
---

At L1 you write prompts. At L7 you write intent.

A prompt tells a loop what to do. An intent document tells a loop what good looks like, what tradeoffs you accept, and what is out of bounds, and then it gets out of the way. The shift from one to the other is the entire job change this class has been walking you toward.

Most people never make the shift. They run a fleet of loops and steer every one of them by editing prompts. They call that strategy. It isn't. It's a manager who can't stop doing the work.

This is the other half of the human pair. Last segment was keeping-you-in-the-loop, the work flowing up to you. This one is intent flowing down. And here is the thing nobody tells you: the cleaner your intent goes down, the thinner the decisions coming back up.

---

## The doctrine you're actually copying

There's a word for this and the Prussians coined it in the 1800s. Auftragstaktik. Mission-type tactics. Mission command.

The idea was a reaction to its rival, which the Prussians called Befehlstaktik, detailed-order tactics. Befehlstaktik says the commander plans everything and the orders specify every move. The subordinate executes the script. It is a prompt, written for a soldier.

Auftragstaktik says the opposite. The commander gives the intent, the schwerpunkt, the point of main effort, and the constraints. Then the subordinate decides the method on the ground, because the subordinate is the one standing on the ground and the commander is on a hill a mile back with a worse view and stale information.

Mission command won. It won because of two facts about the world that have not changed. The world moves faster than the plan, so a detailed plan is wrong by the time it arrives. And the person closest to the work sees things the planner can't, so latitude is not a kindness, it's an information advantage.

Read those two facts again with a fleet of loops in mind. The world moves faster than your prompt edits. And the loop, running at 2am against live data you've never seen, is closer to the work than you are. Every reason mission command beat detailed orders in 1870 is a reason intent docs beat prompt-babysitting now.

[IMAGE: dark canvas, a commander on a hill pointing at a single objective on the horizon, and below, three squads taking three visibly different routes toward the same point]
![[loopy-mission-command-commander-intent-three-routes-1.png]]
![[loopy-mission-command-commander-intent-three-routes-2.png]]
![[loopy-mission-command-commander-intent-three-routes-3.png]]
![[loopy-mission-command-commander-intent-three-routes-4.png]]
![[loopy-mission-command-commander-intent-three-routes-5.png]]

---

## What everyone gets wrong

The mistake is micromanaging the prompt and calling it leadership.

You watch a loop make a call you'd have made differently. So you open its prompt and add a sentence. Next week, a different edge case, another sentence. Now your prompt is forty rules deep, every one a scar from a single incident, and the loop has no idea which of them matter and which were one-off. You've written Befehlstaktik. Detailed orders. A script that grows a line every time reality surprises it.

The diagnostic is one sentence. If your loops can't operate for a month without you editing their prompts, you have not written intent. You've written a script, and you are the runtime keeping it alive.

This isn't a tooling problem. You already have the tooling. You met the autonomy dial, the per-action policy for how much a loop may do. You met governance-primitives, the budgets and kill switches and log reviews that bound the fleet. You met Slack-as-command-center, the surface they all report into. What you don't have yet is the document those mechanisms point at. The dial encodes which actions need you. Governance encodes the brakes. But dial and governance both assume there's a definition of good to enforce against. The intent doc is that definition. Without it, governance is comparing the loop's output to nothing.

[IMAGE: dark canvas, a sprawling prompt on the left titled "40 rules, one per incident" with tangled arrows, versus a short clean panel on the right titled "intent: what good looks like, tradeoff order, kill criteria"]
![[loopy-mission-command-prompt-scar-tissue-vs-intent-1.png]]
![[loopy-mission-command-prompt-scar-tissue-vs-intent-2.png]]
![[loopy-mission-command-prompt-scar-tissue-vs-intent-3.png]]
![[loopy-mission-command-prompt-scar-tissue-vs-intent-4.png]]
![[loopy-mission-command-prompt-scar-tissue-vs-intent-5.png]]

---

## The core insight: write what, not how

An intent doc is the loop's standing orders. It answers the questions a good subordinate would ask once and never need to ask again.

It contains five things. The mission, one or two sentences on the point of main effort, the schwerpunkt, the thing that matters more than anything else this loop touches. The success criteria, what good output looks like, stated so a borrowed verifier could in principle check it, not so the model can vibe it. The tradeoff order, the part everyone skips, the explicit ranking of when speed beats quality, when quality beats speed, and when neither, because the whole reason you're delegating is so the loop can resolve a tradeoff at 2am without you. The kill criteria, the conditions under which the loop should stop and escalate rather than push on. And the escalation format, how it surfaces a decision when it hits one, which is just call-plus-options-plus-recommendation from keeping-you-in-the-loop, written down once.

Notice what is not in that list. No step-by-step instructions. No prompt templates. No "use this tool, then that tool." The moment you specify the how, you've taken the information advantage away from the thing standing on the ground. You've gone back to detailed orders.

This is exactly the strip-the-model-out move, one more time, at the top of the stack. Back in segment three the five primitives were trigger, work, check, terminate, state. The intent doc is those same primitives written as prose for a fleet instead of as bash for one loop. Mission is the trigger and the work framed by purpose. Success criteria is the check. Kill criteria is terminate. The tradeoff order is the new state that survives between every run, the standing context. Same five slots. Higher altitude. No new primitive, the same way no level on the stack ever added a new primitive.

---

## The two-line test

Here is how you know an intent doc is real and not a wish.

A new loop joining your fleet should be operable from the intent doc alone. You should be able to point a fresh worker at the document, walk away, and trust it to make the calls you'd make, because the document told it what good looks like and where the edges are.

That is the same test you'd apply to a senior engineer joining your team. A good senior hire reads the brief, understands what you're optimising for and what you won't tolerate, and ships without pinging you on every decision. If they have to check with you constantly, either they're not senior or your brief is vibes. Same with a loop. Same test, same failure modes.

And this is where the connection to writing-effective-goals closes. A /goal is a tactical intent doc, mission command for one task. We even framed it that way at the time. The nine-section template, the DONE WHEN, the VERIFY that forces machine evidence into the transcript, the kill criteria, that was Auftragstaktik scoped to a single deliverable. A fleet intent doc is the identical artifact zoomed out, governing a continuous operation instead of one run. If you wrote a good /goal, you already know how to write intent. You just write it once for the operation instead of once per task.

---

## Where intent docs rot

Three ways, and they're the same three ways a /goal rots, because it's the same artifact.

Vague success criteria. "Make the titles better." Better by what measure? If the criterion defers to the model's judgment, you've handed the loop a self-grade, and we've spent this whole class on why a self-grade is vibes wearing a loop costume. Success criteria have to point at a borrowed verifier or a real-world signal, watch-time-per-impression, reply rate, eval pass, something outside the model.

No tradeoff order. The doc says "ship fast" and "keep quality high" and never ranks them. So the first time those two collide, and they always collide, the loop guesses, and it guesses wrong half the time, and you're back to babysitting. The tradeoff order is the single highest-leverage line in the document precisely because it's the one a script can't contain. A script has one path. Intent ranks the paths and lets the loop pick.

No kill criteria. The doc says what to do but never what would make doing it a mistake. So the loop optimises straight off a cliff, hitting its success metric while burning your budget or wrecking something the metric didn't watch. Kill criteria are the brake pedal written into the standing orders, and they're what governance polls against.

When a doc has all three holes, it isn't intent. It's vibes in a document. It looks like delegation and behaves like abdication.

---

## Demo

I'm going to open one of my actual fleet intent docs on screen. Not a template. The real file that governs my YouTube title-experiment loop, the same loop you saw broken open in the ACE segment.

1. Open `intent/title-loop.md` in the editor, full screen. It's about thirty lines. Read the MISSION out loud, two sentences: maximise watch-time-per-impression on new uploads, never at the cost of a misleading title.

2. Scroll to SUCCESS CRITERIA. Point at the line that names the borrowed verifier, watch-time-per-impression from YouTube Analytics over a seven-day window, not CTR alone. Note out loud: that's a real-world verifier, not a self-grade.

3. Scroll to TRADEOFF ORDER. Three ranked lines. One, accuracy beats curiosity, a clickbait title that wins CTR and loses watch-time is a loss. Two, watch-time beats raw CTR. Three, when a variant is within noise of the incumbent, keep the incumbent. Say it plainly: this is the part a prompt can't hold.

4. Scroll to KILL CRITERIA and ESCALATION. The loop stops and escalates if a proposed title touches a claim it can't ground, or if the experiment budget hits its cap, governance-primitives wired right into the doc. Escalation format is one line, call-plus-options-plus-recommendation, posted to the Slack deck.

5. Now the count. Highlight every line and tally. Lines of "what" and "why": twenty-six. Lines of "how": zero. There is not one instruction in this file telling the loop which tool to call or which step to run first. That ratio is the whole point.

6. Last beat. Open the git log for this file. Three commits in four months. Then open the git log for the loop's prompt. Untouched in six weeks. Hold on that. The operation is running. I haven't touched it. That is what a working operation looks like.

Total demo: four minutes. The takeaway isn't the title loop. It's the shape of the document and that ratio of what to how.

---

## Key Insight

> A prompt tells a loop what to do. An intent doc tells it what good looks like, what tradeoffs you accept, and where the edges are, then trusts it to fill in the how. If you're still editing prompts every week, you're not commanding a fleet. You're doing the work in a slower costume.

---

## Where we go next

You now have the operating model. Intent down, work up, governance bounding the whole thing.

But a fleet that runs perfectly on good intent still has one bottleneck left, and it isn't the model, the prompts, or the docs. It's you, your attention, your decision throughput. The next segment is about finding that bottleneck and removing it, so the operation scales past the one human sitting at the top of the stack.

See you in the next one.
