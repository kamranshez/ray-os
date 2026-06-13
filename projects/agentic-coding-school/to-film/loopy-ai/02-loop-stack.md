---
duration: "14-18 min"
batch: 1
order: 2
batch_name: "Setup"
class: "loopy-ai"
chapter: "The Loop Stack"
aliases: [loop-stack]
---

There are eight levels of loop. Most people only know two of them. That's why every conversation about AI agents is so confused.

This segment is the vocabulary. We're going to walk the stack top to bottom, then bottom to top, and by the end you'll be able to point at any agent setup in the wild and say which level it is, what it can do, and what it can't.

Stick with me on this one. The rest of the class won't make sense without it.

---

## The stack

[IMAGE: vertical stack diagram, eight levels labeled L0 to L7, each one nested inside the one above, with the model at the bottom and the human at the top]

![[images/loop-stack/the-stack.png]]

From the bottom:

- **L0** Inference loop, inside the model
- **L1** Agent harness, one task
- **L2** Builder and verifier, one artifact
- **L3** Task lifecycle, one deliverable
- **L4** Worker, continuous queue
- **L5** Discovery, problem finder
- **L6** Governance, loop of loops
- **L7** You, deciding what loops should exist

That's the whole map. The rest of this segment is one minute per level.

---

## L0. Inference

Token by token generation. The model's own autoregressive step.

You never touch this. Worth naming so we don't conflate "the model is thinking in a loop" with "I designed a loop." Different thing.

Move on.

---

## L1. The agent harness

Think, tool call, observe, think, tool call. Until the task is done or the context fills up.

This is what Claude Code *is* as a product. Plan mode is L1. The todo list is L1. The ReAct cycle is L1. When Claude reads a file, edits it, runs the tests, reads the failure, and patches the code, the whole thing happens inside one L1 loop.

The boundary is sharp. One coherent task. One context window. One conversation.

[IMAGE: a single rectangle labeled "context window" with arrows cycling inside it labeled think, tool, observe]

![[images/loop-stack/l1-harness.png]]

If you've used Claude Code, you have built L1 loops. You probably didn't call them that. The harness handles it for you.

---

## L2. Builder and verifier

Build. Test. On fail, fix. Test again. Loop until the bar is met.

Sometimes one agent plays both roles, switching between them. Sometimes two agents. Either way, the loop only exits when an external check passes.

Examples.

Write code, run pytest, fix failures, run pytest again. That's the canonical L2.

Generate a thumbnail. A judge agent rates it on a rubric. If the score is below eight, regenerate. That's L2 too.

Draft an email. A critic agent flags issues. Rewrite. Re-critique. That's L2.

The thing that makes L2 different from L1 is the *verifier*. L1 is the model deciding "I think I'm done." L2 is something other than the model checking "are you actually done." Until the check passes, the loop keeps going.

This is the closing the loop pattern. We have a whole segment on it later. For now, just see it: L2 is one artifact, converging to a quality bar, with an external check in the loop.

---

## L3. Task lifecycle

Spec. Plan. Build, which uses L1 and L2 inside it. Review. Push. Verify in production.

One full deliverable, end to end. Multiple L2 loops nest inside. Humans are usually still in the loop at "review" and "push."

This is where Ralph loops live. Run the same prompt in a fresh context over and over against a PRD until the goal is met. The PRD is the spec, the work is the build, the git history is the verify.

This is where goal mode lives too. Set an objective. The runtime keeps the loop alive against that objective until it's met or the budget runs out.

[IMAGE: a flowchart, spec -> plan -> build -> review -> push -> verify, with the build box exploded out into a smaller L1/L2 stack]

![[images/loop-stack/l3-lifecycle.png]]

L3 is the unit of "I shipped one thing." Most people who say "I've used Claude for a real task" are working at L3, even if they don't have the vocabulary for it.

---

## L4. The worker

Pick from a queue. Run an L3. Report. Pick the next one.

The worker doesn't get told what to do each time. It's pointed at a stream of work and trusted to process it.

Examples.

Watch Linear. When a ticket gets a "claude-do" label, pick it up, ship a PR, post a summary. Loop.

Watch the Dependabot PR queue. For each PR, run tests, check the diff matches a safe pattern, merge or escalate. Loop.

Watch a target word list for sentence mining. For each word, find natural example sentences, generate audio, stage the card. Loop.

The boundary is: a worker processes a known stream of work without being told each time.

Most people have never built one of these. The difference between L3 and L4 is small in code, big in mindset. L3 is "I asked Claude to do a thing." L4 is "I built a thing that asks Claude over and over."

---

## L5. Discovery

Now it gets interesting.

A discovery loop does not do the work. It decides what *should become* work.

Examples.

Boris's two hundred Claudes scanning Twitter, GitHub issues, Slack, customer support. They're not writing code. They're deciding which thing would be worth writing code for next.

A YouTube outlier scout watching a hundred channels in your niche. It doesn't make videos. It spots which topics are breaking out, so you can decide whether to make one.

An anomaly detector watching Stripe revenue. It doesn't fix the anomaly. It surfaces the anomaly so you can investigate.

[IMAGE: a diagram with many input streams flowing into a triager agent, which outputs a small filtered list of "things worth doing"]

![[images/loop-stack/l5-discovery.png]]

L5 produces problems, not solutions. It feeds L4.

This is the level where the role of the human visibly changes. At L1 through L3, you decide what to do and Claude executes. At L5, Claude decides what to consider doing and you choose from the shortlist.

That swap is the whole game.

---

## L6. Governance

Once you have twenty loops running, you need a loop to watch the loops.

Kill any loop spending more than two times its expected daily tokens. Page a human if output quality drops twenty percent against last week's baseline. Retire loops that haven't surfaced anything actionable in seven days. Reallocate budget from cold loops to hot ones.

This is the ops and HR and finance layer for your fleet. Most people don't have it yet. The first time you forget to build one and a runaway loop burns a thousand dollars overnight, you build it.

L6 manages other loops as the unit of work. That's the new thing. Everything below this level operates on artifacts or tasks. L6 operates on loops themselves.

---

## L7. The strategic loop

This is you, on a weekly or monthly cadence, asking: which loops should exist? Which should I modify? Which should I retire? Where am I getting the most leverage and where am I just adding noise?

When Boris says "my job is to write loops," he is talking about L7. He is at the top of the stack, deciding which L4, L5, and L6 systems are worth running. He hasn't typed code in months because everything below L7 is delegated to the stack he built.

L7 is the bottleneck now. Not the model. Not the harness. Not the prompts. The portfolio decisions about what to automate at all.

---

## How they nest

[IMAGE: russian doll diagram, L7 wrapping L6 wrapping L5 etc all the way down to L0]

![[images/loop-stack/nesting.png]]

```
L7 (you, deciding)
 └─ L6 (governance, watching)
     └─ L5 (discovery) feeds  L4 (worker)
                                └─ L3 (task lifecycle)
                                    └─ L2 (build / verify)
                                        └─ L1 (agent harness)
                                            └─ L0 (inference)
```

Every loop you build is one of these levels. The level tells you what kind of work the loop is doing, what kind of failures it can have, and what kind of governance it needs.

Misnaming the level is where almost every bad design decision starts.

---

## Two examples of misnaming

Someone on Twitter says "I built an autonomous agent that codes for me." You read the thread. It's a Ralph loop. That's L3. It is not autonomous. It is running a deterministic outer loop against a PRD you wrote. The model isn't choosing what to do. You decided what to do when you wrote the PRD. The loop is just executing your decisions in a windowed way.

Someone else says "I built a closing the loop pattern." You read the code. It's a worker that picks tasks off a queue and runs them. That's L4, not L2. Closing the loop refers to a verifier checking a single artifact. They built something more interesting than they're claiming.

Misnaming costs you. The first person is overclaiming, and when their loop fails on a novel task they'll blame the model instead of the brittle PRD. The second person is underclaiming, and they don't realise the governance question they need to be asking.

The vocabulary is not pedantic. It tells you which failure modes to worry about.

---

## Which level is the class teaching you to build?

L4, L5, and L6.

L0 is the model. You can't change it.

L1, L2, L3 are mostly solved by existing tools. Claude Code is L1. Closing the loop is L2. Ralph and goal mode are L3. We'll cover all of these as building blocks, but the work has already been done.

L4 is where the open frontier starts. Most people haven't built one of these. The ones who have are getting outsized leverage.

L5 is where it gets weird. This is where you stop being the one who decides what to do. You become the one who decides what's worth deciding about.

L6 is where it gets serious. The first runaway loop you have to kill teaches you why you needed L6 from the start.

L7 is you, after the class.

---

## Demo

Open three terminals side by side on screen.

Terminal one. A live Claude Code session. Show it doing one task. Label it on screen as "L1 / L2 / L3."

Terminal two. A worker loop running. Maybe the sentence mining auto feeder. Show it picking the next word off a list, processing it, posting the result, picking the next word. Label it "L4."

Terminal three. A discovery loop running. The YouTube outlier scout. Show it ticking through a watchlist and surfacing one outlier. Label it "L5."

Pause. Pull up a fourth terminal. Run a one liner that shows token spend across all three loops for the day. Label it "L6, if I had one."

Total demo: two minutes. The point is that the same machine is running three different *kinds* of loop simultaneously, and they are doing categorically different work.

---

## Key Insight

> A loop is not one thing. Eight levels nest inside each other. Most people only know levels one through three. The leverage is at four, five, and six.

---

## Where we go next

We're going to walk up this stack one level at a time.

The next few segments handle the on-ramp. Skip permissions. Context management. Subagents. All of this is making L1 actually usable for the long haul. Boring but necessary.

Then we get into L2, the closing the loop pattern. Then L3, Ralph and goal mode and how to write goals that actually work.

Then we step into L4 and the class gets interesting.

See you in the next one.
