---
title: Building Animation Pipelines
videoId: WhtT7K5Pkv0
url: https://www.youtube.com/watch?v=WhtT7K5Pkv0
date: 2026-07-01
status: posted
---

## The one idea worth a video

**1. Wrap a linear workflow in a Claude slash command the model builds and owns for itself, so you buy your way out of ever thinking about the task again.** The whole excalidraw-to-YouTube pipeline exists not to automate a bash script but to keep a rigid flow malleable: Claude designed the CLI syntax, runs it, and re-routes it when you say "make it slower."
VERDICT: next-step video available (complements task-shaped-wrappers).

**2. Never let the model read or write a big JSON file: summarize it with jq/bash and have programs write it back.** The magic prompt line, "JSON must be summarized by bash or scripts and JSON must be written by programs, not by models," is a reusable context-engineering rule with a clean demo (ask for a jq command that describes the schema shape).
VERDICT: net-new video available.

**3. The levels-of-wrongness recovery ladder: match your intervention to how wrong the output is.** 95 percent right, fix it yourself in the editor; 85 percent, tell Claude to polish; worse, add a polish phase; 60 percent, throw the plan out and rebuild from what phase one taught you. And the moment you see it drift, stop it.
VERDICT: next-step video available (complements build-it-twice).

## Summary

On the AI That Works podcast, HumanLayer's Dexter and BAML's Vaibhav demo a Claude Code pipeline animating Excalidraw diagrams into WebM videos for conference talks.

Counts: 🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

Also film-able (not deep-dived): "pick one coding agent and build vibes over minmaxing" plus the Opus-vs-Sonnet long-horizon instruction-following contrast (prompt-engineering / model selection); "build internal tooling to keep the iteration loop tight" (closing-the-loop chapter); "recency of instructions, put the most important line last as the most recent token" (prompt-engineering).

## 🔬 Deep dive

### Spine 1 — Let the model build and own the tool, to stop thinking about the task

The claim: the payoff of running a linear workflow through Claude is not automation, it is cognitive. You are buying the freedom to never think about the task again while keeping it adaptable. Most engineers see the excalidraw-to-WebM-to-YouTube pipeline and ask the obvious question Vaibhav asks on camera: "why run it through Claude? Why not just write a bash script?" It is a linear flow, a bash script would be cheaper per run. The non-obvious answer is that a bash script freezes the flow, while a slash command keeps it soft. Because A) Claude authored the CLI flags and syntax itself ("Claude designed the syntax of this and built it for itself"), and B) an LLM turns human words into structured data, you can say "make it slower" mid-run and it rewrites the speed parameter, or add a brand-new step by asking. So the flow stays malleable at the cost of a few cents. This generalizes to any recurring internal chore: calendar summaries, release recaps, data exports. It goes wrong when the task is genuinely fixed and high-volume, where the tokens and the two-in-three failure rate Vaibhav admits to make a real script the right call.

### Spine 2 — Structured data belongs in scripts, never in the prompt

The claim: an agent should never read or write a large JSON file directly. It should summarize it with a program and mutate it with a program. The default people reach for is to paste the file in and let the model reason over it. That is exactly the failure here: the Excalidraw export is a "big ass JSON file," and reading it whole would eat the entire context window and still leave the model unable to reason about recursive structures. The mechanism is two-step: because the context window is the scarce resource, and because deterministic transforms belong in deterministic tools, you push the reading into `jq` and the writing into a script, leaving the model only to orchestrate. Dexter's prompt encodes it verbatim: "JSON must be summarized by bash or scripts and JSON must be written by programs, not by models." Vaibhav sharpens the demo: "ask it to generate a jq command to describe the schema shape" and the keys alone are usually enough, no file read required. This generalizes to any oversized structured artifact: SQL result sets, large API payloads, log files. It goes wrong when the structure is genuinely recursive or when three or four percent of context spent reading is actually worth it, which Dexter concedes happens.

### Spine 3 — The levels-of-wrongness recovery ladder

The claim: when an agent's output is wrong, the right move depends on how wrong, and there is a clean gradient. This is non-obvious because beginners treat every miss the same way, either babysitting a doomed run to the end or nuking good work at the first flaw. Dexter lays out the rungs: at 95 percent, "go fix it in cursor yourself"; at 85 percent, stay in the session and ask Claude to polish; worse than that, add a phase 1B for the polish; and at 60 percent, "throw out the whole plan and take what we learned in phase one and apply it to build a new plan," because "it's easier to start over than to try to recover this bad trajectory." The mechanism: recovery cost is not linear in wrongness, so past a threshold the cheapest path is a fresh plan seeded by the failed attempt's learnings. Crucially, "the minute you recognize that it's doing something wrong, it's doomed effectively," so you stop immediately rather than paying tokens to finish. This generalizes to any agent output: a research doc, a refactor, a migration. It goes wrong if you restart reflexively and never build the taste to know which rung you are on, which Dexter frames as pure reps and vibes.

## 🎬 Proposed ACS videos

### 1. Build the Tool You Never Have to Think About Again
HOOK: You could write the bash script. Here is why you should make Claude build and run its own CLI instead.
THE PROMISE: For engineers with recurring multi-step chores, walk away able to wrap any workflow in a slash command that Claude authored, so you stop re-deriving it and can re-route it in plain English.
THE SHAPE: (1) Whiteboard the end state first ("start with the end in mind"). (2) Have Claude research-plan-implement its own CLI tool and flags, so you never learn the syntax. (3) Chain the steps into one slash command that threads file pointers between tool calls. (4) Adapt it live: "make it slower" rewrites a param; add a step by asking. (5) The cost-vs-flexibility call: when to keep it agent-driven vs freeze it into a script.
SPINE: 1.
SLOT: Claude Code > task-shaped-wrappers (or Techniques).
RELATIONSHIP: 🔗 complements "task-shaped-wrappers," which teaches wrapping a task in a reusable interface. This adds the deliberate choice to keep the wrapper agent-driven so a natural-language nudge re-routes it, and to let the model author its own CLI so its syntax never lives in your head.
PROOF TO REUSE: "Claude designed the syntax of this and built it for itself." "What you're really buying here is you bought time to not have to think about a task." The live "make it slower" reparameterization, and the excalidraw-to-WebM-to-YouTube pipeline as the on-screen demo.

### 2. Never Let the Model Read Your JSON
HOOK: The fastest way to blow your context window is to paste in a big file. Do this instead.
THE PROMISE: For anyone whose agent chokes on large structured data, leave able to make Claude summarize with jq and write with programs, keeping the file out of the prompt entirely.
THE SHAPE: (1) Show the failure: a huge Excalidraw JSON that eats the context window. (2) The rule, dropped into the prompt as the last instruction. (3) Demo: ask the model to generate a jq command that describes the schema shape, keys only, no file read. (4) Have programs, not the model, write the mutated JSON back. (5) The exception: when spending three to four percent of context on a real read is worth it.
SPINE: 2.
SLOT: Context Engineering > new chapter on handling large structured data.
RELATIONSHIP: ❌ net-new. The catalog has no video on delegating structured-data reading/writing to scripts; the nearest neighbor, refactoring-to-save-on-context, is about restructuring code, a different mechanism.
PROOF TO REUSE: "JSON must be summarized by bash or scripts and JSON must be written by programs, not by models." "You can just ask it to generate a jq command to describe the schema shape." The 200-lines-equals-three-to-four-percent-of-context data point.

### 3. How Wrong Is It? The Recovery Ladder for Agent Output
HOOK: Your agent's plan is off. Do you fix it, polish it, add a phase, or throw it out? There is a right answer.
THE PROMISE: For anyone reviewing agent work, leave with a four-rung triage for matching your intervention to how wrong the output is, and the instinct to stop a doomed run early.
THE SHAPE: (1) 95 percent right: open the editor and fix it yourself. (2) 85 percent: stay in-session, ask Claude to polish. (3) Worse: add a dedicated polish phase (phase 1B). (4) 60 percent: throw the plan out, rebuild from phase-one learnings. (5) The meta-rule: the moment you see drift, stop, because the trajectory is already doomed.
SPINE: 3.
SLOT: Techniques > The First Build Is a Prototype (paired with build-it-twice).
RELATIONSHIP: 🔗 complements "build-it-twice," which teaches the throwaway-and-rebuild move (the 60 percent rung). This adds the full graduated triage, the other three rungs plus the in-the-moment decision rule and the stop-early instinct, so you are not restarting reflexively.
PROOF TO REUSE: "It's easier to start over than to try to recover this bad trajectory." "The minute you recognize that it's doing something wrong, it's doomed effectively." The explicit 95/85/60 percent gradient from the transcript.

## 📚 Full wisdom (reference)

### SUMMARY
On the AI That Works podcast, HumanLayer's Dexter and BAML's Vaibhav demo a Claude Code pipeline animating Excalidraw diagrams into WebM videos for conference talks.

### IDEAS
- A Claude slash command chains Excalidraw export, headless WebM recording, and YouTube upload into one pipeline.
- Claude designed the CLI syntax itself and ran it; the author never once learned the commands.
- Running a workflow through Claude buys you time to stop thinking about a repeated task again.
- Excalate, a Hacker News find, animates Excalidraw files by replaying element timestamps into a WebM video.
- The fork records animations headlessly via browser automation, so no manual file uploads are ever needed.
- Reordering an animation means giving elements new timestamps by cutting and then re-pasting the Excalidraw objects.
- LLMs turn human words into structured data; saying make it slower rewrites a speed parameter instantly.
- The slash command keeps a rigid linear flow malleable, so you add a step by asking.
- Never let the model read a giant JSON file; it eats up the whole context window.
- JSON must be summarized by bash or scripts and written back by programs, not by models.
- Ask the model to generate a jq command describing schema shape instead of reading the file.
- Reading 200 lines cost three or four percent of context; sometimes that context is worth it.
- Recency matters: put the most important instruction last, as the most recent token in the context.
- A magic prompt line forced a unit test in every phase rather than all at end.
- Levels of wrongness at 95 percent, fix it yourself; at 60 percent, throw the plan out.
- The minute you recognize the agent is going wrong, the trajectory is effectively doomed; stop it.
- Model vibes beat minmaxing: knowing how Claude or Codex behaves outweighs juggling many different tools constantly.
- Opus follows long multi-step instructions without forgetting; Sonnet has a fifty-percent chance of forgetting step three.
- The coding harness and the model are orthogonal; you can swap one for the other freely.
- Build internal tools to keep iteration loops tight; a diff viewer was vibe-coded in a day.
- They planned the testing infrastructure first, ignoring the agent, asking what testing loop a human wants.
- Snapshot tests write a snap-new file; the LLM diffs it to grow the compiler forward incrementally.
- Half the battle is knowing the right tools exist; markdown versus jq is purely about exposure.

### INSIGHTS
- Automation's real payoff is cognitive: it frees mental space to not think, not merely time saved.
- Letting the model author its own tool means you never carry its syntax in your head.
- Keeping a workflow agent-driven rather than scripted trades cents-per-run for the freedom to adapt it instantly.
- The context window is the scarce resource; structured data belongs in scripts, never inside prompts directly.
- Instruction placement is a lever: the last token carries the most steering weight during long generation.
- Matching intervention to error size prevents both wasted polishing and premature restarts of good work entirely.
- Depth of intuition about one model beats shallow familiarity spread across many competing coding agents today.
- Fast iteration loops come from tooling investment; the compiler work justified a weekend building test harnesses.
- Pairing during agent downtime sustains engagement; working solo invites distraction and worse plan review quality later.
- Constraining scope from the top removes complexity that agents would otherwise struggle to reason about correctly.

### QUOTES
- "Claude designed the syntax of this and built it for itself." — Dexter
- "What you're really buying here is you bought time to not have to think about a task." — Vaibhav
- "It is not appropriate to read the entire JSON file or write JSON directly." — Dexter
- "JSON must be summarized by bash or scripts and JSON must be written by programs, not by models." — Dexter
- "The minute you recognize that it's doing something wrong, it's like doomed effectively." — Vaibhav
- "It's easier to start over than to try to recover this like bad trajectory." — Dexter
- "Don't outsource the thinking." — Dexter
- "Having the vibes on how Codex behaves really down or how Cloud Code behaves really down is so much more valuable than having some crazy minmaxing thing." — Vaibhav
- "There's a 50% chance that by the time it gets to step three, it forgets what step it's on." — Dexter
- "You expect to use AI to build tools that help you keep that iteration loop tight." — Vaibhav
- "If you're going to build a thing that you want to last a 100 years, you need a good foundation." — Vaibhav
- "Half the battle here, it's honestly just about knowing about the right tools to be able to use." — host

### HABITS
- They start with the end in mind, whiteboarding the target diagram before building any pipeline code.
- They run pipelines in bypass-permissions mode, then have Claude pause for a human to review output.
- He appends a guidance line: work back and forth with me, start with open questions first.
- They resume from a prior research file instead of re-running research they had already completed earlier.
- They stop a run the moment it drifts, refusing to waste tokens on a doomed trajectory.
- They keep Excalidraw drawings simple and shallow, avoiding recursive structures that confuse agents reasoning about them.
- They pair on agent work so downtime becomes discussion, keeping both engineers engaged and actively thinking.
- They push prompts and workflows into a repo folder so viewers can reuse the exact tooling.
- They stick to one voice-to-text app rather than chasing marginal gains from constantly switching tools around.

### FACTS
- Excalate began as a Hacker News project the presenter discovered roughly nine months before recording this.
- Excalidraw exports a full JSON file capturing every element's timestamp, color, and creation data for restoration.
- WebM is a web video format, similar to MP4, uploadable directly to YouTube and slides.
- The BAML team is rebuilding their compiler to be incremental, targeting two months instead of six.
- Insta is a Rust snapshot-testing library the astral tool chain, UV and Ruff, uses heavily.
- Salsa is a Rust library providing caching for compilers, mirroring what the Rust compiler does internally.
- Typical typing speed reaches 120 to 130 words per minute; speaking hits 200 words per minute.
- Reading 200 lines of the file consumed roughly three to four percent of the context window.
- The internal CST diff viewer took Greg about a day and a half to fully build.

### REFERENCES
Tools and projects: Excalate / Excalidraw Animate (their headless fork), Excalidraw, jq, Playwright, WebM, Whisper, SuperWhisper, Whisper Flow, Obsidian, VS Code, Xcode, Google Slides, Claude Code, Codex, Cursor, CodeLayer, Sonnet, Opus, Salsa (Rust), rust-analyzer, Insta (Rust), the astral tool chain (UV, Ruff), MCP, Riverside. Frameworks and content: 12 Factor Agents, the AI That Works podcast, HumanLayer, BAML / BoundaryML, Hacker News, AI Engineer Code Summit (New York). People: Dexter, Vaibhav, Bob, Greg, Aaron, Sam, Ian.

### ONE-SENTENCE TAKEAWAY
Wrap linear workflows in adaptable Claude commands, and never let the model read raw JSON.

### RECOMMENDATIONS
- Wrap any repeated multi-step workflow in a slash command so you stop re-deriving it manually forever.
- Have Claude design and build the CLI tool it will run, rather than scripting it yourself.
- Add a final prompt line telling the model to ask open questions before writing any plan.
- Instruct agents to summarize JSON via jq and write files with programs, never reading everything directly.
- Ask the model for a jq command describing schema shape before it touches a large file.
- Match your fix to error size: polish small misses, restart entirely when output is badly wrong.
- Stop a drifting agent right away instead of paying tokens to finish a clearly doomed trajectory.
- Pick one coding agent and build deep intuition rather than juggling several for tiny marginal gains.
- Build internal tooling like diff viewers and snapshot tests to keep your iteration loop tight, fast.
- Plan and design your testing infrastructure as a human before delegating any code to agents at all.
