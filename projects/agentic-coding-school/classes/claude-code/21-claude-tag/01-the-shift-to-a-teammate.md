---
duration: "10-14 min"
batch: 1
order: 1
batch_name: "Claude Tag"
class: "claude-code"
chapter: "Claude Tag"
status: "scripted"
aliases: [claude-tag-the-shift]
source: "https://claude.com/blog/agent-identity-access-model | https://www.anthropic.com/news/introducing-claude-tag"
---
For two years, Claude Code lived on your machine. One person, one terminal, one loop you sat inside of. Anthropic just shipped the opposite of all of that, and they called it Claude Tag.

This video isn't a feature tour. It's about the shift underneath it: Claude stops being a tool you drive and becomes a teammate you delegate to. And the thing that makes that possible is a single new idea called **agent identity**. Get that idea, and everything else about Claude Tag falls out of it.

---

## What Claude Code was, and what it couldn't be

Listen to how the Claude Code team describes their own product. Claude Code is **single-player, synchronous, and in-the-loop**, and it works best **locally** on your computer.

Source: official Claude Tag walkthrough, Claude Code team

Four words. Single-player: it's you and the model. Synchronous: you ask, you wait, you watch. In-the-loop: nothing happens unless you're sitting there. Local: it runs where you run.

That is a fantastic shape for writing code. It is a terrible shape for everything else work is made of.

Because getting your job done is so much more than coding. And the moment you try to push Claude Code past coding, you hit two walls:

- You want to connect Claude to your data. But it uses *your* credentials, and that's hard to audit. Whose access was that? What did it touch?
- You want it to act when you're not there. So you leave your laptop open with a loop running, checking for new activity, trying to do things on your behalf.

Both of those are hacks. They're you, forcing a single-player local tool to behave like a teammate. Claude Tag is what you get when you stop hacking and rebuild for the teammate from scratch.

[IMAGE: split panel, dark chalkboard. Left side "Claude Code" shows one person at a laptop with four labels: single-player, synchronous, in-the-loop, local. Right side "Claude Tag" shows a shared Slack channel with several people plus Claude, four labels: multiplayer, async, proactive, cloud. An arrow from left to right reads "inverts all four"]

![[claude-tag-single-vs-multiplayer-1.png]]
![[claude-tag-single-vs-multiplayer-2.png]]
![[claude-tag-single-vs-multiplayer-3.png]]
![[claude-tag-single-vs-multiplayer-4.png]]
![[claude-tag-single-vs-multiplayer-5.png]]

---

## Why "act as the user" breaks

Here's the part most people skip past, and it's the whole foundation.

Every personal AI assistant works the same way: it **acts as you**. You connect your Google Drive, your GitHub, your calendar, and the model borrows your permissions. Simple, and it works fine when it's one human talking to one assistant.

It falls apart the second the agent stops being personal. Two reasons.

**Agents are getting more autonomous.** The length of a task an agent can reliably finish on its own has been roughly doubling every four months. Agents now schedule their own work and respond to events hours after the person who asked has logged off.

Source: https://claude.com/blog/agent-identity-access-model

So *whose* credentials is it using at 2am, when nobody is there to "be" the user?

**Teams are multiplayer.** Picture a channel where three engineers and a PM are debugging together. When more than one person is steering the agent, whose permissions apply? There is no single human whose access is the right answer all of the time.

The "act as the user" model has no answer to either question. It assumes there's always exactly one user, present, who the agent stands in for. Drop that assumption and the entire permission model collapses.

[IMAGE: a Slack channel box with three engineers and one PM, each drawing an arrow toward a single Claude in the middle, a large question mark labeled "whose credentials?" hovering over it. Below, a single user keycard with a red line through it, captioned "no one person is the right answer"]

![[claude-tag-whose-permissions-1.png]]
![[claude-tag-whose-permissions-2.png]]
![[claude-tag-whose-permissions-3.png]]
![[claude-tag-whose-permissions-4.png]]
![[claude-tag-whose-permissions-5.png]]

---

## The unlock: Claude acts as itself

So Anthropic changed the question.

The old question was *what can this user do?* The new question is *what can this agent do, in this compartment?* That's agent identity, and it's the spine of the whole product.

Source: https://claude.com/blog/agent-identity-access-model

In a channel where Claude Tag is active, Claude isn't borrowing anyone. It has **its own accounts** in every system it touches. It posts in Slack as the Claude app. It opens pull requests as the Claude GitHub App. It queries your warehouse under a service account an admin set up for it.

Read that again, because two things just happened.

**One: it's auditable by construction.** Claude acts under its own service accounts, so its actions land in each system's own logs as Claude, not as you. You can always see exactly what the agent did, separate from what any human did.

**Two: a shared channel can never become a side door.** There are no personal credentials in play, so dropping Claude into a team channel can't quietly turn into a path back to someone's private drive. The access the agent has is the access an admin granted the agent. Full stop.

This is genuinely strange the first time you see it. A person in the channel who has no direct access to a repo can ask Claude to read that repo, if the *channel* grants Claude that permission. Permissions moved off the human and onto the agent-in-a-place. That feels backwards until you remember the alternative was "act as whichever human happened to type," which has no coherent answer on a team.

[IMAGE: substitution diagram. Top row, faded/crossed out: "what can this USER do?" with a human keycard unlocking tools. Bottom row, highlighted: "what can this AGENT do in this CHANNEL?" with Claude holding three of its own credentials labeled Slack app, GitHub App, warehouse service account]

![[claude-tag-per-user-vs-per-channel-1.png]]
![[claude-tag-per-user-vs-per-channel-2.png]]
![[claude-tag-per-user-vs-per-channel-3.png]]
![[claude-tag-per-user-vs-per-channel-4.png]]
![[claude-tag-per-user-vs-per-channel-5.png]]

---

## Identity lives in the channel, not the workspace

If Claude has one identity everywhere, that's just a super-user with a different name. The interesting move is that **the identity belongs to the channel**.

An admin defines a baseline identity at the workspace level, and every channel inherits it. Then they override it where it matters. The engineering channel gets GitHub and the data warehouse. A CRM connection gets confined to one private channel. Each private channel gets its own distinct Claude.

Source: https://claude.com/blog/agent-identity-access-model

And the boundaries are real. Claude's identity in a legal channel can't reach code that wasn't granted there. Its identity in an engineering channel can't read legal documents that weren't granted there. **Memory respects the walls too**: what Claude learns in a private channel never leaks into the wider workspace.

The walkthrough says the same thing from the inside: in every channel, Claude can have different instructions, different memories, and even different permissions. One product, but a different teammate in each room, shaped by what that room is for.

There's a clean payoff hiding here. Revoking the identity ends Claude's access *everywhere that identity was used*, in one move. Compare that to auditing one agent's actions across dozens of borrowed human accounts. The compartment is the unit you grant, and it's the unit you revoke.

[IMAGE: three sealed boxes side by side labeled Legal, Engineering, Data. Each box holds its own small Claude with its own memory icon and its own key ring. Solid walls between the boxes, a memory bubble bouncing off a wall with a "does not cross" mark]

![[claude-tag-channel-compartments-1.png]]
![[claude-tag-channel-compartments-2.png]]
![[claude-tag-channel-compartments-3.png]]
![[claude-tag-channel-compartments-4.png]]
![[claude-tag-channel-compartments-5.png]]

---

## The teammate behaviors that identity unlocks

Once Claude has a stable identity in a place, it can do things a borrowed-credential tool never could. The walkthrough calls these new primitives. Two of them are worth sitting on.

**It's proactive.** Claude can listen to a channel and decide on its own when to chime in. It can schedule work for itself, every morning at 9, run a report. It can react to events from other services, a GitHub webhook fires, Claude investigates. Remember the laptop you left open with a loop running? That hack was you trying to give a local tool a heartbeat. Now the heartbeat is built in.

[IMAGE: a cycle around a central Claude with four nodes: 1 listens to channel messages, 2 decides when to chime in, 3 schedules its own work, 4 reacts to external events like a GitHub webhook, arrows looping back to the start. To the side, a laptop-with-a-while-loop sketch crossed out, captioned "the old hack"]

![[claude-tag-proactive-loop-1.png]]
![[claude-tag-proactive-loop-2.png]]
![[claude-tag-proactive-loop-3.png]]
![[claude-tag-proactive-loop-4.png]]
![[claude-tag-proactive-loop-5.png]]

**It's multiplayer.** Within a channel there is **one** Claude that everyone shares, not a private instance per person. So anyone can see what it's working on, and anyone can pick up the thread where the last person left off. It's much closer to a colleague producing work in public view than a private back-and-forth with a bot.

There's a quiet second-order effect here that I love. When Claude works in the open, you get to **watch how your teammates prompt it**, and learn from them. The skill of working with the agent stops being something everyone reinvents alone in their own terminal. It becomes shared craft.

---

## Don't let the Slack window fool you

It's easy to look at a chat interface and file Claude Tag under "Slack bot." That's a mistake.

Underneath it all, Claude Tag **is Claude Code**. You can tell it to use your workflows and your skills. It writes real code. The proof point from inside Anthropic: Claude Tag opens around **65% of their pull requests**.

Source: official Claude Tag walkthrough, Claude Code team

So how does a chat message turn into a pull request? The runtime is the tell.

Every channel carries its own memory, instructions, and permissions. When a message lands, a lightweight classifier decides whether Claude should even wake up, based on the instructions you gave that channel. It always wakes when you tag it, or when it's already in a thread with you.

When it does wake in a thread, Claude spins up an **instance of itself with its own sandbox**. Inside that sandbox it clones repos, writes code, tests it, compiles it, opens PRs. There's exactly one instance per thread, so when you add a message, it goes to that running instance and you can steer it in real time.

Sit with that picture, because it's where this is all heading. Claude isn't borrowing your machine anymore. It's spinning up and managing its own isolated environments, one per piece of work. That's the seed of Claude running its own fleet of sandboxes, with the Slack thread as nothing more than the window you talk through.

[IMAGE: left, a flow: a message arrives, passes through a "lightweight classifier: wake?" gate, on wake it spins up a Claude instance inside a sandbox box that lists clone repo, write code, test, open PR, with a note "one instance per thread, steer in real time"]

![[claude-tag-wake-up-flow-1.png]]
![[claude-tag-wake-up-flow-2.png]]
![[claude-tag-wake-up-flow-3.png]]
![[claude-tag-wake-up-flow-4.png]]
![[claude-tag-wake-up-flow-5.png]]

[IMAGE: a vertical stack, three layers. Top layer "Slack: @Claude" drawn as a chat window. Middle layer "Claude Tag primitives" listing identity, memory, proactive, multiplayer. Bottom layer "Claude Code engine + sandbox". A caption to the side reads "65% of Anthropic's PRs"]

![[claude-tag-on-top-of-claude-code-1.png]]
![[claude-tag-on-top-of-claude-code-2.png]]
![[claude-tag-on-top-of-claude-code-3.png]]
![[claude-tag-on-top-of-claude-code-4.png]]
![[claude-tag-on-top-of-claude-code-5.png]]

---

## The shift, in one picture

Step back from the features and look at what actually moved.

Before, everyone ran Claude Code locally, alone, and occasionally shared a finding in a channel. The intelligence lived on individual laptops, and the team got the crumbs that fell off.

Now there's one shared teammate sitting in the middle of where the team already works, with its own identity, its own memory, its own access, that anyone can tag in and hand off to. The default flips from private-and-occasionally-shared to shared-by-default.

And this isn't a one-off product bolted onto the side. It's the same direction Claude Code itself has been moving: out of the single-player loop, toward an agent with standing identity and context that operates alongside a team. Claude Tag is just the cleanest expression of it so far.

[IMAGE: before/after. Left "before": several people each hunched over their own laptop running Claude Code, thin dotted lines occasionally reaching a shared channel. Right "after": one shared Claude teammate at the center of a team circle, solid two-way arrows to every person, labeled "anyone can tag in, anyone can hand off"]

![[claude-tag-the-shift-1.png]]
![[claude-tag-the-shift-2.png]]
![[claude-tag-the-shift-3.png]]
![[claude-tag-the-shift-4.png]]
![[claude-tag-the-shift-5.png]]
![[claude-tag-the-shift-6.png]]

---

## Demo

Keep this concept-level, the hands-on configuration is the next video. The goal here is to make the four primitives visible, not to teach setup.

1. **One channel, multiplayer.** Open a shared engineering channel and tag `@Claude` with a real task ("look at the failing build on this PR"). Show that it's the same Claude everyone in the channel sees, not a private DM.
2. **It acts as itself.** Let it open a pull request. Point at the author: it's the **Claude GitHub App**, not your account. Open the repo's audit log and show Claude's action logged as Claude.
3. **Identity is the channel.** Switch to a second channel with a different profile (say, no repo access). Tag Claude with the same kind of request and show it can't reach what wasn't granted there. Same product, different teammate, different permissions.
4. **Memory respects the wall.** Tell Claude something in a private channel, then ask about it from a public one. Show that the private memory doesn't surface.
5. **Proactive, not prompted.** Show a scheduled instruction ("every morning at 9, summarize what merged to main") or a webhook-triggered investigation firing with nobody typing.
6. **Pop the hood.** Inside a thread, show Claude spinning up its sandbox, cloning, testing, and pushing, so the audience sees the Claude Code engine running under the chat window.

---

## Key Insight

> Personal AI acts as you. Team AI can't, because on a team there is no single "you." Claude Tag's answer is to give the agent its own identity, scoped per channel, and that one change is what turns a tool you drive into a teammate you delegate to.

---

You already know how to prompt Claude. What changes now is *where* it lives and *whose* it is: not on your laptop, not borrowing your login, but in the room with your team, acting as itself.

Next video, we stop talking about what Claude Tag is and start configuring one, the pinned "please remember" message, autoresponse rules, schedules, and the workflows that make it genuinely yours.
