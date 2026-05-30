---
tags: [youtube, video-plan, codex, claude-code, agentic-coding, custody]
aliases: [custody-cut, director-video-plan]
date: 2026-05-30
status: plan
---
## Title and thumbnail

- Working title: "Make One Codex Session Run All The Others"

## 1. Cold open and motivation (0:00 to 0:45)

- Drop the motivation immediately, this is why the video exists: these models stopped being the bottleneck a while ago, we were just pouring an org chart's worth of parallel work through a single chat box built for one human doing one thing at a time.
- Land the quote: "The intelligence was never trapped in the model. It was trapped in the chat box. We didn't make the model smarter, we gave it a desk." [coinage: we gave it a desk]
- Promise: "In the next three minutes I am going to show you the whole thing working, then we will break down why it matters."

## 2. The demo, early (0:45 to 4:30)

- Reason it is early: showing it working first gives the viewer a concrete picture, so every concept after this lands on something they have already seen.
- Brief one session as the director. Type the job description on camera: never push, draft never send, cap concurrency, workers cannot spawn workers. The governance boundary is shown first, before any autonomy. [this is the safety answer, demonstrated not asserted]
- Backlog fanout: hand it ~20 open issues. It spins up one thread per issue, each in its own worktree, each opening its own pull request. The PR list becomes the board you scroll.
- Narrate the filing-cabinet behavior as it happens: it auto-titles each thread after its issue, pins the ones blocked on a decision, archives the merged ones. "Watch what it is doing to the sidebar, not just the code." [coinage: the filing cabinet]
- Climax, the multi-PoV race on one hard issue: three worktrees, three angles, three draft pull requests. You compare the real diffs side by side and bin two. "You can compare three real diffs. You could never do that with three buried subagents."
- Engineer one realistic failure. On the next heartbeat the director reads only that worker's trace and the pulse fires to your phone: one decision needed. You tap in, answer the single question, leave. The other nineteen are never touched. Default state was silence.
- Beat to sit on: "That whole thing ran itself. I set the rules once and got pulled in exactly once. Now let me show you why this is different from just spawning a bunch of agents."

## 3. What you just watched, in Codex (4:30 to 6:00)

- Show it in Codex briefly (a 15 second screenshot of the actual feature) so people know what shipped: the thread tools, create, read without opening, search, rename, pin, archive.
- The distinction that makes the demo work, the filing-cabinet analogy: a subagent is a reply buried in a chat. You can talk to it and even resume it, but it is stuck inside that one conversation's lineage. A thread is a top-level document in a filing cabinet, you can rename it, pin it, archive it, and search for it across your whole workspace. [coinage: the filing cabinet]
- The reveal that proves the point: put the two tool sets side by side on screen, the ephemeral-subagent API next to the durable-thread API. One collapses into the parent, one you curate. The genuinely new thing is not spawning, spawning was always possible. The new thing is the filing cabinet: rename, pin, archive, search.
- Why this beats agents-in-a-chat, said out loud here because they just saw all three: autonomy (a thread runs on its own clock without you driving it), customization (each thread has its own title, worktree, machine, and cadence), and a decision surface (a durable record of what was done and why, not just the outcome).

## 4. The commands you can actually say (6:00 to 6:45)

- This is the spoken-intent layer, what you literally tell it:
- "Pin this as my director."
- "Spin up a thread per open issue."
- "Rename these as they get messy."
- "Every morning, check the others and ping me only if one is stuck."
- "Promote this shipped feature into a thread that reports usage to Slack every week."
- Plant the craft idea: the last two are not really prompts, they are schedules. Choosing when and how often a thread wakes is where the intent lives, more than the words do. [coinage: cadence is the new prompt]

## 5. The mental model, a three-tier org (6:45 to 8:15)

- Frame with the newsroom: pulse threads are the assignment desk, the director is the editor, the delegates are reporters in the field, and the thread is the byline that survives the story. [metaphor: newsroom]
- Tier 0, pulse threads, the night shift: standing automations that manage the system itself, not project work. Checkups on the other threads, renaming the messy ones, spotting a pattern recurring across threads and proposing a reusable skill, reviewing your past sessions to suggest better prompts, pinging you only when you are needed. [coinage: the night shift]
- Tier 1, director threads: one pinned director per project. It holds the plan in a file, not in the scrollback, and dispatches the work.
- Tier 2, delegate threads: spawned per task, each in its own worktree, each a clean isolated trace. On Claude Code that trace is a worktree, a branch, and a pull request.
- The dynamic that makes it alive, thread promotion: a delegate that ships a feature gets promoted into a Tier 0 monitor that reports how that feature is being used on a cadence. Lifecycle is spawn, work, then archive or promote. [coinage: thread promotion]
- The skill nobody names yet, said here: organizing the board is the actual work, the way a line cook's genius is the station being set before service, not cooking faster. [metaphor: mise en place]

## 6. The custody turn, the real point (8:15 to 9:45)

- The reframe the whole video has been building to: the agent did not just get more autonomy. It took custody of your workspace, the container that holds all your work, not just the tasks you hand it. [coinage: custody, not autonomy]
- The elevation ladder, and you climb it too:
- Gen 1, the agent did the task, it operated on the content, and you were the operator typing every step.
- Gen 2, the agent used the tools, it operated the environment, and you became the manager reviewing outputs.
- Gen 3, the agent took custody of the workspace, it operates the interface itself, and you become the owner who sets the rules and audits the cabinet.
- The one-liner: you used to hop between tasks yourself, now you supervise a board. The models got smart enough to hold a layer, so you moved up off it.
- Name the inversion directly, because the audience believes the opposite: for two years the advice was one chat per task, keep the context clean. That discipline now moves up a level. The job is no longer keep this chat clean, it is keep the board clean.

## 7. The objections, honest (9:45 to 11:15)

- Context rot, the number one practitioner complaint, it rots in about a week: the fix is a file-backed director, the plan lives outside the scrollback so compaction cannot lose it. [coinage: file-backed director]
- Worktree conflicts under parallelism: one worktree per task, never two agents on the same files. A bad change is quarantined to one branch and reverted in one click, which is exactly why the backlog demo did not collide.
- Token burn from idle heartbeats: be a thermostat, not a furnace. A furnace blasts on a timer, a thermostat fires only when a condition is sensed. Event-driven wakeups, capped concurrency, point it at big jobs not one-file tweaks. [metaphor: thermostat not furnace]
- The objection nobody else will raise, archive is the most dangerous verb: everyone fears the agent spawning, the quiet risk is silent archiving and renaming. A tidy sidebar can hide work you did not know you lost. Tidiness is a confidence trick, so you keep audit rights over the cabinet. [coinage: archive is the most dangerous verb]
- Governance and prompt injection, as a lower-third or pinned comment: external context from Slack or GitHub lands in a read-only file the director must cite, it never auto-acts on it.

## 8. Broaden, then close (11:15 to 12:15)

- One quick non-code flash to signal reach: estate or grief admin, or a job hunt, where the plan lives in a file and not in your head, so you are not carrying the whole checklist in your mind. This is the proof it is bigger than coding.
- The elevation close: gen 1 did the task, gen 2 used the tools, gen 3 took custody of the workspace.
- Reprise the quote to bookend the open: the intelligence was never trapped in the model, it was trapped in the chat box, we gave it a desk.
- The honest footnote: you could already do most of this by grepping your session history on disk, this is just a much better surface, and it can read your Codex sessions too.
- Glue-absorption sign-off: native is an ergonomics win, not a capability win. Ask of every shiny feature, is this a new power, or a shorter on-ramp to one I already had.
- CTA: thdxr tweet (https://x.com/thdxr/status/2060553984947950017).