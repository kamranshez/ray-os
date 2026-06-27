---
tags: [youtube, script, claude-code]
status: draft
date: 2026-06-25
---

## Title options

| # | Formula | Title |
|---|---------|-------|
| 1 | Bold claim + personification | You've Been Using AI Agents in Single-Player This Whole Time |
| 2 | Bold claim + specificity | Anthropic Just Ended Single-Player AI Coding (Claude Tag) |
| 3 | Curiosity gap + exclusivity | The Claude Update Everyone Misread (Karpathy Didn't) |

> Coined term this video plants: **single-player vs multiplayer agents.**
> Format: feature deep-dive (agent identity) + thesis broader-trend (the multiplayer shift). Masterclass pitch. Demo surface: masterclass MCP / landing page.
> **Pitch placeholders to confirm before filming:** `[DEADLINE]`, `[PRICE]`, free artifact = *"Single-Player to Multiplayer migration checklist (PDF)"* (confirm), free class video cross-link (confirm pairing).

---

### Hook (0:00 - 0:25)

*On screen: a single terminal, one Claude Code session running. Then it splits into a Slack channel with several people and a Claude avatar in it.*

So I was reading the changelog for Anthropic's new thing, Claude Tag, and honestly my first reaction was the same as everyone else's. Oh. It's a Slack bot. Cool.

And then Karpathy posted something that made me realize I had completely misread it. Because the thing they actually shipped is not a bot. It's the moment that everything we've been doing with AI coding stops being single-player.

That's the word that made it click for me. Single-player. Up to now, you and your agents have been playing single-player. And this is the industry quietly flipping the whole thing to multiplayer.

![[smp-main-hook-1.png|480]]
![[smp-main-hook-2.png|480]]
![[smp-main-hook-3.png|480]]
![[smp-main-hook-4.png|480]]
![[smp-main-hook-5.png|480]]

### The problem: you've been playing single-player (0:25 - 1:30)

*On screen: the "wall of terminals" image, a dozen agents running on one machine.*

Here's what I mean. Think about how you actually use Claude Code today. It's you, your machine, your terminal. Maybe you're fancy and you've got a fleet of agents running in parallel. One person, a dozen Claudes.

And that feels like peak productivity. But there's a problem nobody really names, so let me name it. Every one of those agents is single-player. The context lives on your machine. The plan it made lives in a local plan mode that nobody else on your team can see. When it opens a pull request, your teammates get a wall of code with zero context for how it got there.

So you get duplicate work, because two people kicked off the same task. You get surprise features nobody agreed to build. You get merge conflicts because three agents all touched the same files. The agent is fast, but the team is not aligned. And scaling up one person in a vacuum doesn't fix that. It actually makes it worse.

![[smp-main-single-player-problem-1.png|480]]
![[smp-main-single-player-problem-2.png|480]]
![[smp-main-single-player-problem-3.png|480]]
![[smp-main-single-player-problem-4.png|480]]
![[smp-main-single-player-problem-5.png|480]]

### Soft anchor (1:30 - 2:00)

Quick pause before we get into it. This video is sponsored by me and my Claude Code Masterclass. Over 1,500 engineers from companies you've heard of have gone through it, and a lot of them are now the best Claude Code user at their company. You're probably thinking, why would I buy lifetime if in a year there's a better tool. Chances are there will be, and you get lifetime access to that class too. The lifetime plan retires `[DEADLINE]` and the price goes up to `[PRICE]` after that. Link's below.

### Old workaround vs the new solution (2:00 - 2:45)

So how have we been patching the single-player problem? Manually. You finish a session, then you go paste the important bits into Slack. You screenshot the diff. You say "let me forward you my notes." Some of you went further and ran always-on agents in a shared tmux session, or used one of the OpenClaw-style setups, so the rest of the team could at least watch.

But that's you doing the multiplayer part by hand. The agent is still single-player. It doesn't live where the team lives.

Claude Tag flips that. Instead of you carrying context out of your terminal and into Slack, the agent moves into Slack. It becomes a member of the channel that anyone can tag and hand work to. And that sounds simple, which is exactly why people are dunking on it. But the reason it's hard, and the reason this is the real story, is the part nobody is talking about.

![[smp-main-old-vs-new-1.png|480]]
![[smp-main-old-vs-new-2.png|480]]
![[smp-main-old-vs-new-3.png|480]]
![[smp-main-old-vs-new-4.png|480]]
![[smp-main-old-vs-new-5.png|480]]
![[smp-main-old-vs-new-6.png|480]]
![[smp-main-old-vs-new-7.png|480]]

### The buried lede: agent identity (2:45 - 6:30)

*On screen: a diagram. Old model: Claude wearing a mask with YOUR face. New model: Claude with its own badge.*

Here's the thing Anthropic kind of buried. When you connect Claude to your Google Drive or your GitHub today, it acts as you. It borrows your login. It uses your permissions. That works fine when it's just you in a private chat.

Now put that same model in a shared Slack channel with four people in it. Whose login does the agent use? Yours? What if you log off and it keeps working for two more hours, which these agents now do. And if it's borrowing your credentials in a channel, then anyone in that channel just became able to reach into your private documents through the agent. That's a side door into everything you have access to.

So the multiplayer version can't work that way. And this is the actual innovation. In Claude Tag, Claude doesn't act as you. It acts as itself.

*On screen: the access-bundle setup.*

It gets its own accounts. Its own login in Slack. Its own GitHub identity that opens pull requests as the Claude app, not as you. Its own service account on your data warehouse. An admin sets up what they call access bundles, which are just named sets of connections, repos, and instructions, and attaches them per channel. So the engineering channel can reach the codebase and the warehouse, the legal channel can read contracts and nothing else, and the two can never cross. The channel is the security boundary. Even the memory respects it. What Claude learns in a private channel never leaks into the rest of the workspace.

And here's why that matters more than any feature. This is the exact problem every single one of those "Claude in a group chat" tools failed to solve. They could put an agent in a shared channel, but they couldn't answer "who is it acting as, and what's the blast radius if it goes wrong." Anthropic's answer is: it acts as itself, with its own permissions, and every single thing it does is logged under its own name. That's not a Slack bot feature. That's an identity and access system for agents. They just gave it the worst possible name, "Tag," which is why everyone anchored on Slackbot and missed it.

*Demo on the masterclass surface (narrated over, not built live):*

Let me show you the shape of it. Here I've got a channel pointed at my masterclass project. I tag Claude and say, "pull the three most common questions from the support channel and draft answers using the class outline." And watch, it's not acting as me. It posts back as itself, it touched only what this channel granted it, and there's a clean log of exactly what it read. Anyone else in the channel can pick up right where it left off. That's the multiplayer part actually working.

![[smp-main-agent-identity-1.png|480]]
![[smp-main-agent-identity-2.png|480]]
![[smp-main-agent-identity-3.png|480]]
![[smp-main-agent-identity-4.png|480]]
![[smp-main-agent-identity-5.png|480]]
![[smp-main-agent-identity-6.png|480]]

### The third major redesign: Karpathy's keystone (6:30 - 7:30)

*On screen: three panels drawing in one at a time. A browser window, then a desktop app, then a Slack channel full of people with Claude in it.*

So step back for a second, because this is the framing that made the whole launch click for me, and it comes from Andrej Karpathy. Former head of AI at Tesla, the guy who coined vibe coding. When he reframes something, he's usually about six months early.

He says this is the third major redesign of how we use these models. Paradigm one, the model is a website you go to. You open a tab, you chat. Paradigm two, it's an app you download to your computer. Think Claude Code in your terminal. And paradigm three, the one that just started, is that the model becomes a persistent, asynchronous entity, with org-wide tools and context, working alongside a whole team of humans.

And then he said the line that made me re-read the entire launch. His words: this is not a feature like some crappy Slack bot. It is an org-level harness. The difference will become clearer over time.

I think that's exactly right. And here's the simplest way to hold his three paradigms. Paradigm one and two were single-player. Just you and the model, one on one. Paradigm three is multiplayer. That distinction, single-player versus multiplayer agents, is the lens I want you to keep, because once you have it, the whole industry snaps into focus.

![[smp-alt-karpathy-keystone-1.png|480]]
![[smp-alt-karpathy-keystone-2.png|480]]
![[smp-alt-karpathy-keystone-3.png|480]]
![[smp-alt-karpathy-keystone-4.png|480]]
![[smp-alt-karpathy-keystone-5.png|480]]

### Ray thinks deeper: this is an industry-wide flip (7:30 - 9:00)

*On screen: three logos appearing one at a time, Anthropic, GitHub, and the Karpathy tweet.*

Now here's what convinced me this isn't just an Anthropic launch. The same week, GitHub showed almost the identical idea, built completely independently.

There's a researcher at GitHub Next named Maggie Appleton, and she gave a talk called "One Dev, Two Dozen Agents, Zero Alignment." Same diagnosis, almost word for word. She says the single-player tools scale up the individual, but software isn't made by one person, it's a team sport. Her line that stuck with me: implementation is becoming a solved problem, so the new bottleneck isn't how to build it, it's agreeing on what to build. More individual output doesn't fix a coordination problem. It makes it worse.

And their prototype, called ACE, is basically the same instinct as Claude Tag. Multiplayer chat sessions, each one backed by its own sandboxed cloud computer on its own branch, where your teammates and your agents are all in the same room, editing the same plan, watching the same preview. Two of the biggest names in this space looked at the wall of solo terminals and independently said, no, the future is multiplayer.

And it's not just the AI labs. PostHog posted that this exact conversation already happened in their Slack last week, a teammate tagging their own PostHog agent in a thread, the agent searching the codebase, opening a pull request, then checking CI and reviewing its own comments, all in line with the rest of the team. So this is very likely where a huge chunk of agent work is heading, agents living inside your team chat and acting as full members of the conversation. And some companies have already been wiring this up themselves for a while. But my bet is the AI companies end up doing it best, for two reasons. They own the models, so they can build the permissions and the identity layer right into the foundation instead of bolting it on. And they own the connectors, so the same model that's talking in the channel is the one already wired into your tools. That's a hard combination for a third party stitching it together from the outside to beat.

And if you dig through the Claude Code leaks, the fingerprints were there months ago. There was a gated, employee-only feature codenamed KAIROS, and internally they literally labeled it assistant mode. It turned Claude Code into an autonomous, always-on assistant. A file-based memory it consolidates over time in a background pass, which, fun fact, is the same dreaming feature I made a whole video on. A proactive loop so it keeps working while you're away and messages you on its own. And something the code itself calls channels, which let Slack, Discord, even SMS push messages straight into a live session. That channels-plus-autonomy stack is basically Claude Tag before it had a name. Anthropic could have shipped it as a flashy consumer toy. They skipped that entirely and went straight to enterprise. I actually think that's the right call, because the hard part here was never the chat. It was the identity and permissions, and that only matters at the team level.

![[smp-main-industry-convergence-1.png|480]]
![[smp-main-industry-convergence-2.png|480]]
![[smp-main-industry-convergence-3.png|480]]
![[smp-main-industry-convergence-4.png|480]]
![[smp-main-industry-convergence-5.png|480]]

### The honest counter-take (8:30 - 9:30)

*On screen: a "but is it overhyped?" title card.*

Now, I went and read through a couple thousand replies on this launch, and I don't want to only sell you the dream, so here are the sharpest objections, because some of them are real.

One, the cost. It's Opus only, billed per token, and it reads every channel it's in. People were posting seventeen dollars spent in the first ten minutes. At any real team size that's thousands a month. The always-on coworker is also an always-on meter.

Two, and this is the smart one, the moat just moved. As one engineer put it, the model is commoditized now, the lock-in is the harness. Your agent's memory and all your setup is not portable. Context becomes the new switching cost. So the same persistent memory everyone's praising is also the thing that quietly locks you in.

And three, the part the "AI employee" hype gets wrong. A human changes after you correct them because they don't want to get fired. An agent has no stake. It repeats the mistake until you fix the instructions. So the job doesn't disappear, it changes. You stop being the operator and you become the person who maintains the spec.

![[smp-main-counter-take-1.png|480]]
![[smp-main-counter-take-2.png|480]]
![[smp-main-counter-take-3.png|480]]
![[smp-main-counter-take-4.png|480]]
![[smp-main-counter-take-5.png|480]]

### What this means for you (9:30 - 10:15)

So where does this leave you, today.

Single-player isn't dead. For solo, focused, synchronous work, you in one terminal with Claude Code is still the fastest thing there is. I'm not moving that into Slack.

But the second more than one human is involved, single-player is the wrong shape, and multiplayer is coming for that whole category. And the skill that's about to matter most isn't prompting faster. It's being able to write a spec and a context that a shared agent, acting as itself, can pick up and run with. That's the muscle to start building now.

![[smp-main-what-it-means-1.png|480]]
![[smp-main-what-it-means-2.png|480]]
![[smp-main-what-it-means-3.png|480]]
![[smp-main-what-it-means-4.png|480]]
![[smp-main-what-it-means-5.png|480]]

### Closer + pitch (10:15 - 11:00)

So that's the real shift. Not a Slack bot. The moment your agents stop being single-player.

If you want to get genuinely good at the part that actually carries over, structuring context and specs so an agent can run with them, that's the core of my Claude Code Masterclass. The lifetime plan is gone after `[DEADLINE]` and the price goes up to `[PRICE]`. Fourteen day money back guarantee, and less than 0.2% of buyers have ever asked for a refund. My email's in the description if you've got questions.

And if you liked this, there's a free video in the class where I `[CONCRETE DEEPER VERSION, e.g. "set up Claude to act on a shared project end to end"]`. No credit card needed to watch it, just sign up. Link's in the description.
