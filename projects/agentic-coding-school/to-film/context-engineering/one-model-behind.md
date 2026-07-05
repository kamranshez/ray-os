---
duration: "10-14 min"
batch: 2
order: 1
batch_name: "Foundations"
class: "context-engineering"
chapter: "Foundations"
---

Your Claude setup is one model behind. Not the model itself. The harness you built around it. Every rule in your CLAUDE.md, every guardrail in your skills, every constraint in your system prompts was written to patch a weakness of a specific model generation. Then a new generation ships, the weaknesses move, and your rules stay exactly where they were.

Some of those rules silently flip from protecting you to capping you. And because they fail quietly, the output still looks fine, it is just worse than it could be, nobody notices.

This video gives you the fix: a generation audit. A ritual you run on new-model day that re-derives every assumption baked into your setup. First you need to see why the problem exists at all, because it comes from something strange about how these models actually improve.

---

## Same model, different intelligence

Here is a question that breaks claude.ai chat: "which Pokemon names end in aw?"

There are roughly a thousand Pokemon. Two of them end in aw, Drednaw is one. The model knows every single name. It has read every Pokedex entry on the internet. And it still cannot answer, because answering means scanning a thousand items for a suffix match, and that kind of exhaustive filtering is exactly what a raw language model is bad at. It will confidently give you a wrong list.

Ask Claude Code the same question and it answers instantly. Not because it is smarter. It is the same model weights. It fetches the full list of names, writes a three-line script to filter for the suffix, runs it, and reads you the answer.

[IMAGE: same model weights in the center, split into two panels: left panel a chat window flailing at the Pokemon question, right panel an agent with bash fetching a list, running a filter script, and answering; label the difference "the harness"]

![[one-model-behind-same-weights-1.png]]
![[one-model-behind-same-weights-2.png]]
![[one-model-behind-same-weights-3.png]]
![[one-model-behind-same-weights-4.png]]
![[one-model-behind-same-weights-5.png]]

Same model. Different harness. Different intelligence.

This is **capability overhang** made visible. The capability was always in the model. What was missing was the scaffolding that lets it out. And that means the intelligence you experience day to day is not set by the model. It is set by whatever harness some human wrote around it.

Tariq Shihipar, who works on Claude Code at Anthropic, put it bluntly at the AI Engineer World's Fair: "the models are grown not designed," and "what contains them is us."

---

## Grown, not designed

That phrase matters more than it sounds. Nobody at Anthropic sat down and specified what Claude can do, the way you would spec a feature. The capabilities emerge from training, and the people building the harness discover them afterwards, empirically, by poking at the model.

Tariq's description: working with these models "is closer to a biology than a physics." You do not derive behavior from first principles. You run experiments and observe. Anthropic even published a paper called "On the Biology of a Large Language Model," and he recommends reading it for exactly this reason.

The consequence you care about: Claude "gets smarter in spiky ways." A new generation does not raise every capability by the same amount. One skill jumps three generations' worth. Another barely moves. A third gains an ability that flat out did not exist before.

[IMAGE: two overlaid spiky radar shapes labeled generation N and generation N+1 across capability axes, some spikes barely moving while others explode outward past a dotted circle labeled "your assumptions"]

![[one-model-behind-spiky-capability-1.png]]
![[one-model-behind-spiky-capability-2.png]]
![[one-model-behind-spiky-capability-3.png]]
![[one-model-behind-spiky-capability-4.png]]
![[one-model-behind-spiky-capability-5.png]]

You cannot predict where the spikes land. Which means you cannot patch your setup in advance. You can only re-check it after the fact. Most people never do.

---

## Every guardrail is a snapshot

Now look at your own CLAUDE.md with that lens.

"Always ask before editing more than three files." "Never restructure the folder layout." "Keep responses under 200 words." "Do not write scripts, edit files directly." Every one of those rules exists because at some point, some model burned you. You wrote the rule, the burning stopped, and you moved on.

Each rule is a snapshot of a specific model's weakness at a specific point in time. That is fine on the day you write it. The problem is what happens next.

A new generation ships. The weakness that justified the rule is gone. But the rule is still there, and now it is doing the opposite of its job: it is preventing the model from using a capability it now has. The guardrail flipped from protective to binding.

[IMAGE: a horizontal guardrail bar fixed in place while a model capability line rises across three generation ticks; below the crossing point the region is labeled "protecting you," above it "capping you," with the crossing point circled]

![[one-model-behind-guardrail-flip-1.png]]
![[one-model-behind-guardrail-flip-2.png]]
![[one-model-behind-guardrail-flip-3.png]]
![[one-model-behind-guardrail-flip-4.png]]
![[one-model-behind-guardrail-flip-5.png]]

And here is why nobody catches it. A binding guardrail does not throw an error. Nothing breaks. The output still arrives, still looks reasonable, still passes review. It is just capped at last generation's ceiling while you pay for this generation's model. Silent failure is the worst kind, because there is no signal telling you to look.

---

## Anthropic hits this too

If you think this only happens to sloppy personal setups, watch what happened inside Claude Code itself.

When the new generation shipped, Anthropic cut 80 percent of Claude Code's system prompt. Not trimmed. Cut. Four fifths of the instructions were guardrails for weaknesses the model no longer had.

And the shape of that prompt has cycled over time. Early models needed small prompts because they could not follow much. Then models got better at instruction following and best practice swung to large prompts stuffed with examples and long lists of do-not-do constraints. Now the best practice is small again, but for a new reason: current models do not need the constraint lists. You give them context plus intent, and they derive the constraints themselves.

[IMAGE: a cycle across three model generations showing system prompt size going small, then large with stacked example blocks and do-not lists, then small again, with the reason labeled under each stage]

![[one-model-behind-prompt-cycle-1.png]]
![[one-model-behind-prompt-cycle-2.png]]
![[one-model-behind-prompt-cycle-3.png]]
![[one-model-behind-prompt-cycle-4.png]]
![[one-model-behind-prompt-cycle-5.png]]

Same story with a single tool. Tariq built AskUserQuestion, the tool Claude uses to interview you. On Opus 4, the model could barely call it, he had to tweak it heavily just to get it working. On Opus 4.5, it could run 40-question spec interviews. On Fable, it embeds the interview questions inside whole interactive HTML reports it generates for you. The output format itself evolved underneath the tool: markdown snippets, then plan mode summaries, then in-depth interactive reports.

Same tool definition. Three generations. Three completely different ceilings. If Anthropic had frozen their assumptions at Opus 4, you would still be getting the barely-working version. That is exactly what your frozen CLAUDE.md is doing to you.

There is a historical version of this lesson too. In the chat era, everyone assumed solving coding meant 100-million-token context windows, so you could paste the whole codebase in. The actual answer was the opposite: give the model bash and let it build and search its own context. That insight is what created Claude Code. The people who kept betting on bigger paste windows were optimizing a guardrail for a weakness that was about to stop mattering.

---

## The generation audit

So here is the ritual. On new-model day, before you go play with the shiny features, you audit the harness. Four steps.

**Step 1: Inventory.** Pull up everything that instructs the model: your CLAUDE.md files, your skills, your custom system prompts. This is the full set of assumptions you are about to re-derive.

**Step 2: Classify every rule.** Each rule is one of two things. A **model-weakness guardrail**: it exists because a past model screwed something up. Or a **product constraint**: it exists because of your actual requirements, security, compliance, style, brand voice. The first kind expires. The second kind does not.

[IMAGE: a pile of rule cards being sorted into two bins, one labeled "model-weakness guardrail" with an expiry stamp, one labeled "product constraint" with a permanent lock icon]

![[one-model-behind-rule-sorting-1.png]]
![[one-model-behind-rule-sorting-2.png]]
![[one-model-behind-rule-sorting-3.png]]
![[one-model-behind-rule-sorting-4.png]]
![[one-model-behind-rule-sorting-5.png]]

**Step 3: Re-test the guardrails.** For each model-weakness guardrail, remove it and rerun the task it was protecting. If the new model handles it cleanly, delete the rule. If it still fails, keep the rule and note which generation it was re-tested against.

**Step 4: Re-ask what is now possible.** This is the step everyone skips, and it is where the overhang lives. Go to your archive of failed prompts, the things you tried six months ago that did not work, and rerun one. Capability lands in spikes, so something in that graveyard is alive now. You will not find it unless you look.

[IMAGE: a four-step cycle labeled inventory, classify, re-test, re-ask, drawn as a loop with a new-model-day trigger arrow entering from outside and a "delete stale rules" output arrow leaving]

![[one-model-behind-audit-loop-1.png]]
![[one-model-behind-audit-loop-2.png]]
![[one-model-behind-audit-loop-3.png]]
![[one-model-behind-audit-loop-4.png]]
![[one-model-behind-audit-loop-5.png]]

Run this every time a generation ships and your harness tracks the model instead of trailing it.

---

## Do not delete blindly

One honest warning before the demo, because the failure mode on the other side is just as real.

Do not read this video as "guardrails bad, delete everything." Some of your rules encode real product constraints. "Never log customer emails" is not a model-weakness patch, it is a compliance requirement, and it survives every generation forever. "Always write migrations as separate files" might be your team's actual deployment process, not a workaround.

That is why classification is step two and deletion is step three, in that order. You only re-test the rules you classified as model-weakness guardrails. Product constraints never enter the test. And even for the guardrails, the test is per model: a rule that Fable does not need might still be load-bearing on the smaller model you run in CI.

Classify first. Test per model. Then delete.

---

## Demo

What the camera shows, in order:

1. **The Pokemon split screen.** Left side, claude.ai chat: ask "which Pokemon names end in aw?" and watch it flail, hallucinating names or missing Drednaw. Right side, Claude Code: same question. Watch it fetch the list, write the filter script, and answer correctly in seconds. Same weights, different harness, on camera.
2. **A real CLAUDE.md audit.** Open a mature CLAUDE.md from an actual project. Walk the rules line by line and classify on camera: three rules exposed as generation-stale guardrails, written for a model two generations back, and one rule identified as a genuine product constraint that stays no matter what.
3. **Delete and rerun.** Delete the three stale guardrails. Rerun a task that previously needed them. Compare the output side by side with the guarded version and show the ceiling coming off.
4. **Raid the graveyard.** Pull one old failed prompt from history, something a previous generation could not do. Rerun it on the current model. Watch it work. That gap between "failed then" and "works now" is the overhang you have been sitting on.

If you want the applied version of step four at full scale, the "Your Interaction Layer" video in this school is exactly that: giving Claude arms into your apps and your OS, capabilities most setups never unlock because nobody re-asked what was possible.

---

## Key Insight

> Every guardrail in your setup is a snapshot of some past model's weakness, and because capability lands in unpredictable spikes, some of those rules have already flipped from protecting you to silently capping you. Audit them every generation, or run this generation's model at last generation's ceiling.

---

## The closing beat

The next model generation is coming whether you prepare or not. When it lands, everyone else will benchmark the model. You will audit the harness.

Because the model is not what is holding you back. Your rules are. And they are one generation old.
