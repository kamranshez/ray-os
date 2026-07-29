# Tips on leveraging AI for empirical research

- URL: https://www.lesswrong.com/posts/f4WZ7dde8KAYHfeif/tips-on-leveraging-ai-for-empirical-research
- Author: Daniel Tan
- Date: 2026-07-06
- Karma: 28  Comments: 0  Words: 1961
- Band: A  Tier: 1  Score: 73.3  Density: 16.62
- Anchors: claude code, \bmcp\b, \bworktree, \bharness(es|ing)?\b, claude\.md, coding agents?

---

*Tl;dr I've been thinking hard and experimenting with how to best take advantage of AI for my work. I've developed some practices, mostly through trial and error. These have helped me spend less effort doing work while getting more done, and so I'm writing them up to share them.*

*A couple disclaimers:*

*   *I've tried to optimise for my personal circumstances and the type of work I do (empirical research). However, I've also tried to focus (this blogpost) on things that are relatively timeless / general to more types of knowledge work.*
*   *Most of my experience is working with Opus 4.8*  *in Claude Code. It's plausible the best practices for working with later-gen models are different. However I think this is probably fine for now since it's unclear to what extent later-gen models will remain accessible*

What success looks like
-----------------------

In my current world, automation is empowering. It lets me hand off the boring / fiddly / uninteresting bits so I can focus my time on what I really want to do. For me, a good day currently looks like this:

*   I get a neat idea, braindump it into my lab-notes channel, and think of a concrete experiment (possibly collaboratively with AI).
*   I spin up an agent with all the context it needs. It runs the experiment end-to-end on a cloud GPU. No intervention needed from me so I go do something else.
*   I come back a short while later and read the report that came back. After some review / editing, I'm happy that it reflects how I'm currently thinking, and merge it into my knowledge base.
*   I take a while to think about the writeup. I might cross-reference it with some others, notice some coherent themes emerging, and connect these into a bigger project. At which point I probably have a new idea, so I can spin it up again.
*   All of this is sufficiently frictionless that I have the energy to maintain several of these loops in parallel.

All the practices I'll talk about below are in service of enabling more such "good days".

Work in atomic writeups
-----------------------

Software engineering has the concept of the "pull request" - the fundamental unit of work. This has many benefits - it helps ensure work finishes in a reasonable amount of time. It also allows you to update / consolidate / reprioritise before doing more work. Anecdotally, some of my most cracked friends are those who adhere strictly to working in well-defined sprints.

For empirical research, I think the unit of work is an **atomic experiment writeup**. It focuses on a single (headline) result, explains what was done, why it's interesting, and (optionally) next steps. It's self-contained, so a low-context reader can follow it. The target audience is someone generally familiar with the field — i.e. you, or your collaborators — but with no knowledge of the specific experiment.

In the spirit of Andy Matuschak, I aim for my writeups to be [**evergreen**](https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX). They should be self-contained, so I can come back months later and re-read one with ~full understanding. And each one should be easy to build on: by including limitations, takeaways, ideas for future work, and reproducibility details. When I do this well, my small blogpost-style writeups compose effortlessly into bigger papers.

My work / automation philosophy is well-described as "streamlining the process to get to an evergreen writeup".

Reducing in-the-loop friction
-----------------------------

In my view, all AI work is essentially human-in-the-loop. The difference is just how much work I let the AI do before I look at it. This loop can be pared down to:

1.  I plan a unit of work and context-load the agent
2.  The agent does the unit of work
3.  I context-load what the agent did and review it
4.  I edit the writeup until I'm happy with it

Provided the scope has been determined correctly, I can be confident that step 2 can happen with ~zero intervention from me. So it's only necessary to intervene in steps 1,3,4; I want these to be as low-friction as possible.

### Low-friction context-dumping

I want it to be very easy to give context to my agent. I really like Karpathy's "[one note for everything](https://karpathy.bearblog.dev/the-append-and-review-note/)" system, which is dead simple and guarantees all thoughts are in the same place. In practice, I implement this as a lab-notes Slack channel, which an agent can read over MCP. Google Drive MCP and voice-to-text are also useful tools here when I want to do a big braindump in the CLI.

### Low-friction reviewing

For me, reviewing AI work is the biggest time sink and source of friction.

**Make AI reports more readable.** AI writing is sloppy by default. One aspect of this is that they mention lots of unnecessary / unwanted details. Whereas I want them to communicate only the informative bits and nothing else. A big source of alpha here is to tell it I am the target audience, so the writeup can assume familiarity with high-level ideas, and instead focus on low-level details. Concretely I think a structure of "begin with the empirical result, then enough experimental detail to understand what was done, and only then interpretation" helps a lot.

**Ask for a single-file repro.** When I need to really understand a complex experiment, I ask for a single-file reproduction of the headline result. I can read it top to bottom, run it, and see if it directionally reproduces the main effect. This is usually a nice middle ground of "builds trust in the result / idea" and "not too high-effort to do".

**No need to verify 100% of work.** Most of my work is exploratory. IMO it is important to spend a bit of time checking the implementation for major screwups and noting any limitations. But often it's not important for me to be 100% sure that all of this went exactly as intended, as opposed to thinking about / running the next experiment. If a result becomes load-bearing, I can verify it at that point in time.

### Low-friction editing

I find that switching to an IDE, finding the file, and editing the Markdown by hand is too much friction. I built [cowrite](https://github.com/dtch1997/cowrite) for this: a browser-based editor where I edit a draft by hand while my coding agent edits the same file, with changes round-tripping to disk. I love how seamless this makes it to read and re-generate reports. As a bonus, it also works on a remote devbox (by serving an edit link over Cloudflare).

Improve processes over time
---------------------------

More important than the specific techniques I use, is the underlying philosophy of process improvement. The practices I use need to adapt to changes, e.g. in the type of work I do, in the underlying models / harnesses, etc.

**Address points of friction.** I find it very valuable to notice points of friction and address these with process improvement / better tooling. For example, I noticed Opus 4.8 would often struggle with starting and stopping RunPod and Modal instances, so I built [bellhop](https://github.com/dtch1997/bellhop), a small async library that checks my code into an ephemeral box, runs it, and brings the results back. More generally, a custom library is a way to codify "here's how I like to do things", so it doesn't need to be re-explained in every prompt.

**Post-mortems.** Every so often I have an agent review past transcripts: what went well, what could have gone better, was there anything that took an unreasonable amount of effort? The answers feed directly into the next round of tooling and conventions.

Principles of experimental code design
--------------------------------------

This part isn't about AI per se, but it does give me much more confidence in handing things off to agents. I want my experiment code to satisfy five properties:

*   **Determinism.** The same script with the same args produces the exact same output.
*   **Resumability.** Resuming a failed run should be effortless and shouldn't repeat completed work - cached intermediate outputs, etc.
*   **Visibility.** It should be trivial to see the state of a run: what's currently running, what failed, what the error was.
*   **Persistence.** Outputs (checkpoints, eval results) should be easy to persist and reuse.
*   **Lineage.** For any persisted artifact, it should be easy to tell how it was generated.

Satisfying all five is not trivial. So I built [stagehand](https://github.com/dtch1997/stagehand), a small declarative engine for orchestrating experiment sweeps, and I harness all my experiments with it: declare the steps as a dataflow graph, run it, and watch the live dashboard. The properties I want are enforced by the engine that runs the experiment.

A nice side benefit is increased **reliability**. Atomic experiments should be able to be described as series of steps that simply run in sequence with no additional intervention required. The ultimate form of this is calling `uv run script.py` and letting things happen.

Parallelise
-----------

Doing more things is good, actually. A lot of what I run takes a while, and that downtime is usable — I multiplex several agent sessions with `tmux` and rotate through sessions as work finishes. It's important to make sure different agents don't interfere - worktrees are your best friend here!

**Don't go overboard.** It should be noted that repeated context-switching is frazzling. I think it's not necessary to keep multiple agents fed at all times, especially if I'm confused / don't feel very excited about any particular next experiment. Rather, the point is that it should be cheap to spin up a parallel workstream, *if* I already know what I want to do and think it's valuable.

Random tips and tricks
----------------------

I've found some other tips to be pretty useful, although specific to Claude Code / my setup.

**Standard operating procedure.** "SOP" in my `Claude.MD` is shorthand for (all of): "create a fresh git worktree on a dedicated branch, lay out the work as a task list before starting, orchestrate experiments with stagehand, surface results through a browsable UI". Similarly, "wrap up" means "commit, open a PR, make sure findings are reproducible, and persist artifacts with pointers checked into the repo".

**Let improvements compound across projects.** Feedback I give an agent in one project should make it better at all the others, so I use a "command center" pattern: one top-level repo where memory, context, and conventions accrue, with the actual project repos living as gitignored subdirectories under repos/{repo-name}. All my work happens in the "same place", like a monorepo, but each project can still be parcelled out and shared with its own PRs and issues.

**Have a central writeup repository.** I publish experiment writeups to a GitHub Pages site. That makes it easy to point a future agent at the report in order to quickly catch it up to what was done before. A nice bonus is that this makes it easy to send the reports to people for feedback.

Other thoughts
--------------

Some final observations:

*   I think it's worth being highly intentional about the way in which you choose to work - this is separate from the work itself. It's a really useful meta-skill that transfers across diverse domains of work.
*   A lot of the tips above concern directly using AI to do the work, but a fair bit is also about using AI to build tools that do the work, and some of it is just about the timeless craft of effective knowledge work.
*   I don't think I've really scratched the surface yet of automation. E.g. I haven't really looked into "agent fleets" or "loop engineering". It's possible I could be effectively wielding far more compute-per-second to make progress on work I want done. I'm excited about experimenting more with how I do work to make progress towards that.