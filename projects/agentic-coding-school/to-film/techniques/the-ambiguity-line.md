---
duration: "10-14 min"
batch: 1
order: 4
batch_name: "Multi-Model & Multi-CLI Workflows"
class: "techniques"
chapter: "Multi-Model & Multi-CLI Workflows"
---

## The Wrong Question

Most people ask the wrong question about coding agents. They ask "which one is better, Claude Code or Codex?" and then pick a side and defend it.

That question has no answer, because it is missing a variable.

The right question is not which agent is better. It is **where does this task sit**, and which agent fits that spot. Answer that, and you stop guessing. You start routing.

This video gives you the one axis that makes the decision for you.

Source: https://www.youtube.com/watch?v=_WXc3gA8K6E

---

## The Loyalty Trap

Walk into any dev community right now and you will find two tribes. The diehard Claude Code people. The diehard Codex people. Each one convinced their tool is the one true agent.

They are both wrong, and they are wrong in the same way.

An agent is not a religion. It is a tool with a shape. Codex has a shape. Claude Code has a shape. When you marry one of them, you use it for every task, including the tasks it is bad at. You take a tool that is excellent at half your work and you force it through the other half, and then you blame the tool when it struggles.

The people getting the most out of these agents are not loyal to either one. They are loyal to the task. And they switch, sometimes in the middle of a single job.

To switch on purpose, you need a rule. Here is the rule.

---

## The Ambiguity Line

Draw a single horizontal line. On the left, put tasks that are wide open, where you do not even know what you are building yet. On the right, put tasks that are pinned down, where the plan is written and all that is left is to type it out.

That line measures one thing: **how ambiguous is this task right now?**

[IMAGE: dark chalkboard, one horizontal axis labeled "ambiguity"; left end labeled "no requirements yet, exploring" with Claude Code sitting above it, right end labeled "plan is written, just execute" with Codex sitting above it]

![[ambiguity-line-spectrum-1.png]]
![[ambiguity-line-spectrum-2.png]]
![[ambiguity-line-spectrum-3.png]]
![[ambiguity-line-spectrum-4.png]]
![[ambiguity-line-spectrum-5.png]]

The left end is where design lives. You are exploring three ways to structure an app. You are turning a messy codebase into an architecture wiki and you do not know the shape yet. There are no requirements, because the requirements are the thing you are trying to discover.

The right end is where execution lives. You already have a plan and you want an agent to build phase two of it. You are running a goal until the unit tests pass. You are doing test driven development, where the tests already say exactly what correct means.

Every task you touch falls somewhere on this line. And each end of the line has a different best tool.

---

## Why Codex Owns the Right End

Codex is the tool for the low ambiguity end, and it is not close.

Here is why. Codex tends to do deeper research on the codebase before it starts writing anything. It reads more first. So when the task is well specified, it tends to get things right on the first try, instead of coding, discovering it was wrong, and backtracking.

It is also less verbose, and it does not go off on side quests. It takes what you give it and it accomplishes exactly that. Nothing more.

Now notice something. That literalness is the exact trait people complain about. Codex once named a file with the literal placeholder Xs still in the name, instead of filling in the real value, because that is what the instruction technically said. Funny. But that same rigid, do-what-I-said-and-nothing-else behavior is precisely what you want when the plan is already correct and you just need it executed faithfully.

[IMAGE: two-step flow, panel one "reads codebase deeply first", arrow to panel two "writes it right on the first try", small caption underneath "literal = faithful when the plan is correct"]

![[ambiguity-line-codex-first-try-1.png]]
![[ambiguity-line-codex-first-try-2.png]]
![[ambiguity-line-codex-first-try-3.png]]
![[ambiguity-line-codex-first-try-4.png]]
![[ambiguity-line-codex-first-try-5.png]]

A literal agent on a clear plan is a feature. A literal agent on a vague idea is a disaster. Which brings us to the other end.

---

## Why Claude Owns the Left End

When the task is ambiguous, you do not want a literal executor. You want a collaborator that questions you.

That is Claude Code in planning mode. It reads the space read only, lays out options with tradeoffs, and asks you the clarifying questions you did not think to ask yourself. Skills like Matt Pocock's Grill Me and Grill With Docs push this even harder, making the agent interrogate your thinking before a single line gets written.

Source: https://github.com/mattpocock/skills

The output of the left end is not code. It is requirements. You walk in with a fuzzy idea and you walk out with a set of concrete, actionable steps. The exploration converges.

[IMAGE: left side a fuzzy cloud labeled "vague idea", several arrows fanning out to explore options, then converging on the right into a clean numbered list labeled "actionable plan"]

![[ambiguity-line-claude-converge-1.png]]
![[ambiguity-line-claude-converge-2.png]]
![[ambiguity-line-claude-converge-3.png]]
![[ambiguity-line-claude-converge-4.png]]
![[ambiguity-line-claude-converge-5.png]]

This is why loyalty fails. If you are a Codex diehard, you hand your vague idea to a literal executor, and it confidently builds the wrong thing fast. If you are a Claude diehard, you keep a questioning, exploratory agent on a task that was already pinned down an hour ago, and you burn tokens re planning something that needed no more planning.

Match the agent to the end of the line. That is the whole game.

---

## Your Real Job Is To Walk The Task Down The Line

Here is the part that changes how you work.

A task does not sit still on the line. It moves. Almost everything starts on the left, ambiguous, and your entire job as the engineer is to walk it to the right until it is concrete enough to execute.

That sentence is worth saying plainly. **Your job is to take a highly ambiguous idea space and collapse it into a low ambiguity one.** That is what engineering has always been. The agents just made the two halves of it visible.

So the workflow writes itself. Start on the left with Claude. Explore, get grilled, produce a plan. Split that plan into pieces, ideally into separate worktrees so the pieces do not collide. Then hand the concrete pieces to Codex on the right and let it carry each one to the finish line.

[IMAGE: the same ambiguity axis, a single dot labeled "the task" moving left to right along it, a vertical dashed "handoff" line in the middle with "Claude plans" on the left of it and "Codex executes" on the right]

![[ambiguity-line-walk-down-1.png]]
![[ambiguity-line-walk-down-2.png]]
![[ambiguity-line-walk-down-3.png]]
![[ambiguity-line-walk-down-4.png]]
![[ambiguity-line-walk-down-5.png]]

Start with the questioner. Finish with the executor. The handoff happens at the moment the task crosses from "I am not sure what this is" to "I know exactly what to build."

---

## Where It Goes Wrong

The line is a model, not a law, so let me show you the two ways it breaks.

The first is a fuzzy handoff point. A task rarely announces the exact second it becomes concrete. Hand off to Codex too early, while requirements are still soft, and you get a confident, fast, wrong build. Hand off too late, and Claude keeps exploring a decision you already made. When in doubt, do one more grilling pass before you cross the line. Cheap insurance.

The second is treating a big compound task as a single point. Real work is not one dot on the line. It is many. The GitHub infrastructure piece might be pinned down and ready for Codex, while the display layer that reads it is still a design question for Claude. Do not ask "where is this whole project on the line." Ask it per piece. That is also why splitting into worktrees matters, because each worktree can sit at a different point and get a different agent.

Get those two right and the framework holds up under real work.

---

## Demo

I will take one real task from a highly ambiguous idea all the way to executed code, switching agents exactly once, on purpose.

1. Start in Claude Code planning mode with a vague goal: a game driven entirely by GitHub issues. No plan yet. Pure left end of the line.
2. Run the Grill Me skill and let Claude interrogate the idea. Answer its questions on camera. Watch the ambiguity drop with every answer.
3. End the session with a written plan, and find the natural dividing point: one piece for the GitHub infrastructure, one piece for the display that reads it. Two low ambiguity chunks.
4. Spin up a separate worktree for each chunk so they cannot step on each other.
5. Cross the handoff line. Open Codex in the first worktree, hand it the concrete piece, and tell it to run until the tests pass. Do the same for the second.
6. Show the payoff side by side: Claude gave us the plan we could not have written up front, Codex executed each piece faithfully without side quests. Neither tool did the other's job.

The viewer should walk away able to look at their own next task and say, out loud, where it sits on the line and which agent gets it.

---

## Key Insight

> Stop asking which agent is better. Ask where the task sits on the ambiguity line, use Claude to collapse ambiguity into a plan, and Codex to execute the plan faithfully. Your job is to walk every task from the left end to the right, and switch agents the moment it crosses over.

---

## The Shift

Once you internalize the line, agent loyalty starts to look silly. You are not a Claude person or a Codex person anymore. You are the engineer holding the map, deciding where each task lives and routing it there.

Pick your next task. Find it on the line. Then reach for the right tool on purpose.
