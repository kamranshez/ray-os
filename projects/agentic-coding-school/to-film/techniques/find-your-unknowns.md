---
duration: "10-14 min"
batch: 1
order: 2
batch_name: "Planning Before Implementing"
class: "techniques"
chapter: "Planning Before Implementing"
status: "scripted"
---

## Your Prompt Is a Map

With frontier models, the bottleneck is no longer whether the agent can do the work. It is how well your prompt matches the codebase it lands in. Your prompt is a map. The repo is the territory. Every place the map is blank, the agent makes a decision you never specified, silently, at full speed.

Tariq Shihipar from Anthropic's Claude Code team put it in four words at AI Engineer World's Fair 2026, in the talk that launched the Fable model: **"the map is not the territory."**

Here is the part most people get backwards. Stronger models do not make this problem smaller. They make it bigger. A stronger model traverses more territory per prompt. More files touched, more decisions made, more corners of the codebase reached before you look up. Every one of those steps that your map did not cover gets resolved by the model's best guess.

So as the models get better, surfacing your unknowns matters more, not less.

[IMAGE: a hand-drawn map on the left with a clean straight route, the real territory on the right with the same route crossing a ravine, a swamp, and a fence the map never showed, blank map regions highlighted where the territory has hazards]

![[find-unknowns-map-vs-territory-1.png]]
![[find-unknowns-map-vs-territory-2.png]]
![[find-unknowns-map-vs-territory-3.png]]
![[find-unknowns-map-vs-territory-4.png]]
![[find-unknowns-map-vs-territory-5.png]]

---

## Silent Decisions Are the Expensive Ones

Think about what a wrong silent decision actually costs you.

The agent hits an unspecified fork, picks a direction, and builds on top of it for forty minutes. You review the result, spot the wrong turn buried under a thousand lines, unwind it, re-prompt, and run again. That is a full run plus a full review, twice.

Now price the alternative. The agent hits the same fork and asks. You answer in one sentence. Ten seconds.

A wrong silent decision costs a run plus a review. A surfaced unknown costs one question. That asymmetry is the whole economics of this video. Everything that follows is a technique for converting silent decisions into questions before they get expensive.

[IMAGE: two timelines stacked vertically, top one labeled silent decision showing a long run bar then a review bar then a red X then the same two bars repeated, bottom one labeled surfaced question showing a tiny question bubble then one clean run bar, a bracket comparing the total lengths]

![[find-unknowns-silent-decision-cost-1.png]]
![[find-unknowns-silent-decision-cost-2.png]]
![[find-unknowns-silent-decision-cost-3.png]]
![[find-unknowns-silent-decision-cost-4.png]]
![[find-unknowns-silent-decision-cost-5.png]]

---

## The Knowns Matrix

Tariq's framework for finding your unknowns is a 2x2 you have probably heard in another context. Applied to prompting an agent, it becomes an operational tool.

- **Known knowns.** The stuff you write in the prompt. This quadrant is handled. It is literally what a prompt is.
- **Known unknowns.** Things you know you have not figured out yet. Which auth flow, which error strategy, whether this needs a migration.
- **Unknown knowns.** Things so obvious to you that you would never think to write them down. You cannot describe them, but you know them when you see them. Taste lives here.
- **Unknown unknowns.** The things you have not considered at all. The gotcha in the module you have never opened. The constraint nobody documented.

The insight is not the matrix. The insight is that **each quadrant has a specific technique that drains it.** Your prompt covers the first quadrant. The next three sections cover the rest, and then two more techniques cover the build itself and the aftermath.

[IMAGE: a 2x2 grid, axes labeled you know about it and you can articulate it, each quadrant containing its name plus a small tool icon, prompt in known knowns, interview in known unknowns, prototypes in unknown knowns, blind spot pass in unknown unknowns]

![[find-unknowns-knowns-matrix-1.png]]
![[find-unknowns-knowns-matrix-2.png]]
![[find-unknowns-knowns-matrix-3.png]]
![[find-unknowns-knowns-matrix-4.png]]
![[find-unknowns-knowns-matrix-5.png]]

---

## The Blind Spot Pass

Start with the scariest quadrant: unknown unknowns. You cannot ask about what you have not considered. But the agent can consider it for you, because it can read everything you have not.

Before touching a module you know nothing about, run this prompt, close to verbatim:

*"I'm working on a new auth provider I know nothing about in this codebase. Do a blind spot pass to help me figure out my relevant unknown unknowns and help me prompt better."*

Claude scans the module. It reads the git history and sees which files churn together, which fixes got reverted, where the hacks live. If you have Slack wired up, it reads the threads where someone hit the same wall two years ago. Then it hands you the list of hairy dead ends and gotchas you did not know to ask about, phrased as things to put in your next prompt.

You are not asking it to do the work. You are asking it to draw the parts of the territory your map left blank.

[IMAGE: three source streams labeled module code, git history, and Slack threads converging into one funnel, out of which comes a short numbered gotchas list handed to a stick figure holding a blank map]

![[find-unknowns-blind-spot-sources-1.png]]
![[find-unknowns-blind-spot-sources-2.png]]
![[find-unknowns-blind-spot-sources-3.png]]
![[find-unknowns-blind-spot-sources-4.png]]
![[find-unknowns-blind-spot-sources-5.png]]

This generalizes past code. Tariq used the same move to learn color grading for video editing, a field where he did not even know the vocabulary of the questions. A blind spot pass on a new domain gives you the map of what you need maps for.

One honest failure mode. A blind spot pass is only as good as the context sources behind it. If the agent has no git history, no Slack, no real signal, it will still produce a confident list, and that list will be hallucinated plausible-sounding gotchas. A blind spot pass without real sources wired up is a creative writing exercise. Wire up the sources first, or discount the output hard.

---

## Brainstorm Prototypes

Next quadrant: unknown knowns. The things you cannot articulate but recognize instantly. This is where design taste, UX feel, and "that's not what I meant" live.

The mistake everyone makes here is trying to write the spec anyway. You produce three paragraphs describing a dashboard you cannot actually picture, and the agent faithfully builds your bad description.

The fix is to stop describing and start reacting:

*"I have no visual taste. Make me an HTML page with four wildly different design directions so I can react to them."*

Four directions, wildly different on purpose. You look at them and your unknown knowns surface on contact: too corporate, too cramped, that one, but with the second one's typography. You just specified things you could not have written down, by pointing at concrete artifacts.

This connects to another line from the talk: **"One of the best ways to give Claude a map is to give it another map."** Reference code, even in a different language. An HTML mockup instead of a written spec. An artifact beats a description because artifacts carry the details you would have forgotten to write. The school already covers reference-as-spec in depth in Designing Components and Example: Design Source of Truth, so I will leave it there. The point for this video: prototypes are how you turn a reaction into a spec.

[IMAGE: four small wildly different page mockups fanned out in a row, a stick figure pointing at the third one, an arrow from the pointing gesture into a written spec document labeled now it is a known known]

![[find-unknowns-react-to-prototypes-1.png]]
![[find-unknowns-react-to-prototypes-2.png]]
![[find-unknowns-react-to-prototypes-3.png]]
![[find-unknowns-react-to-prototypes-4.png]]
![[find-unknowns-react-to-prototypes-5.png]]

---

## Interviews, One Upgrade

Known unknowns get drained by interviews: the agent asks you questions before it builds. You already know this move. The school teaches it thoroughly in Clarifying Questions in the Prompt Engineering class and across the whole Spec Developer chapter in Master Claude Code, so I am not going to re-teach it here.

I will add the one upgrade from Tariq's talk, because it is worth the price of admission on its own. When you ask the agent to interview you, add this line:

*"Prioritize questions that would change the architecture."*

Without it, interviews drift toward trivia. Button labels, edge-case copy, config names. Questions that are easy to generate and cheap to get wrong. With it, the first questions are the ones where a wrong silent guess would cost you the whole run: data model shape, sync versus async, where state lives.

And the matching failure mode: interview fatigue. If every task starts with twenty questions, you will start answering on autopilot, and an autopilot answer is worse than no interview because it looks like a specification. Over-specification is not safety. Keep interviews short, architecture-first, and skip them entirely for tasks below the ambiguity line.

---

## Implementation Notes

The first three techniques run before the build. This one runs during it, and it is not taught anywhere else in the school.

Add one instruction to your build prompt: **every time you hit something in the territory that is not on the map, log a note.** Every unspecified decision point. Every place the plan said one thing and the code forced another. Every default you chose because I did not tell you.

The agent still builds at full speed. It just leaves a trail of pins where your map was blank.

Then, after the run, audit the notes. This is the part that compounds. Each note is a precise, timestamped record of exactly where your map failed. Not a vibe, not a guess. A list. "Prompt did not specify how to handle expired tokens, chose silent refresh." "Plan assumed one workspace per user, schema allows many, deviated."

Some of those decisions you will agree with. Fine, now they are known knowns, put them in the prompt next time. Some you will not, and you just caught them from a five-line note instead of an archaeology dig through the diff.

Your prompts stop being static artifacts and start being maps that get corrected against the territory after every trip.

[IMAGE: an agent's path snaking through a territory from start to merged, with numbered pins dropped at each blank-map moment along the path, and an arrow looping from the collected pins back to the original prompt document with patches applied to it]

![[find-unknowns-implementation-pins-1.png]]
![[find-unknowns-implementation-pins-2.png]]
![[find-unknowns-implementation-pins-3.png]]
![[find-unknowns-implementation-pins-4.png]]
![[find-unknowns-implementation-pins-5.png]]

---

## Quiz Me

The last technique runs after the build, and it is also new to the school.

Before you open the PR, tell the model: quiz me on what was built and why. Not a summary. A quiz. Summaries wash over you; questions expose you. If you cannot answer why the retry logic lives in the client instead of the server, you do not actually know what you are about to put your name on.

Tariq frames this as how you stay in the loop when the agent does the typing. The work ships under your name. Your reviewer will ask you questions, your teammate will ask you questions in six weeks, production will ask you questions at 2am. The quiz is a rehearsal for all three, and it costs five minutes.

And when you get a question wrong, that is not embarrassing, that is the technique working. A wrong answer sends you back into the diff to close the gap between what was built and what you believe was built. Which is one more map-territory mismatch, caught before it mattered.

---

## Five Techniques, One Timeline

Put the whole system together and it stops looking like tips. It is a pipeline around the build.

**Before:** blind spot pass for the unknown unknowns, prototypes for the unknown knowns, a short architecture-first interview for the known unknowns. **During:** implementation notes pinning every blank spot on the map. **After:** audit the notes, quiz yourself, patch the prompt.

Each pass through this loop shrinks the blank regions of your map. The agent gets faster because you stop paying for silent wrong turns. You get sharper because every run teaches you what you failed to specify.

[IMAGE: a horizontal timeline in three zones labeled before, during, and after, blind spot pass plus prototypes plus interview stacked in before, implementation notes running as a strip through during, notes audit plus quiz me in after, a feedback arrow from after wrapping back to before]

![[find-unknowns-timeline-1.png]]
![[find-unknowns-timeline-2.png]]
![[find-unknowns-timeline-3.png]]
![[find-unknowns-timeline-4.png]]
![[find-unknowns-timeline-5.png]]

---

## Demo

Three moves, all on a real repo.

1. **Run a blind spot pass cold.** Pick a module in a real repo I have never touched. Run the blind spot pass prompt verbatim, with git history available as a source. Show the gotchas list it returns, then pick out one gotcha on camera that I genuinely did not know, and show the line it would have burned me on.

2. **Build with implementation notes on.** Start a mid-size feature build with the implementation-notes instruction in the prompt. While it runs, show the notes file accumulating in real time. Afterwards, walk through two logged deviations, then edit the original prompt on camera to close both gaps, so the next run's map covers them.

3. **Quiz me before the PR.** With the diff ready, prompt: "quiz me on this change, five questions, hardest first." Answer on camera. When I get one wrong, and I will, follow it back into the diff and show what I believed versus what was actually built.

---

## Key Insight

> Your prompt is a map and the codebase is the territory. Every blank spot becomes a silent decision the agent makes at full speed, and stronger models make more of them per run, not fewer. A wrong silent decision costs a full run plus review. A surfaced unknown costs one question. Spend your effort finding your unknowns.

---

Next time you are about to prompt an agent into a module you do not know, stop for ninety seconds and run the blind spot pass first.

One question asked is one run saved. That trade never stops being worth it.
