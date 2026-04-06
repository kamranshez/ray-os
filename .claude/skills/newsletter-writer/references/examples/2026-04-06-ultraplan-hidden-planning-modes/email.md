**Date:** 2026-04-06
**Subject:** Anthropic silently shipped Ultraplan. And it's an A/B test
**Preview:** (not recorded — to be confirmed)
**Type:** Video-redirect with appendix (system prompts)
**Audience:** Subscribers
**Emotional tone:** Investigative, curious, practical
**Hook strategy:** Stealth launch / discovery
**Open rate:** TBD
**Click rate:** TBD

---

Hey friends,

Hope you've had a great week.

So Anthropic quietly shipped a new feature inside Claude Code called Ultraplan. No announcement, no blog post — yet. It just appeared.

You type /ultraplan, give it a prompt, and it hands the planning off to the cloud while your terminal stays free.

You get a web UI for reviewing the plan: inline comments, emoji reactions, an outline sidebar. When you're happy with it, you either run it in the cloud or teleport it back to your terminal. It's about 2x faster than local planning too.

[VIDEO THUMBNAIL]

And I would have left it at that, except the quality was pretty inconsistent. I ran 10 different prompts through both Ultraplan and local planning to compare them. Sometimes Ultraplan caught edge cases that local planning completely missed (like tracing every consumer of an interface before changing it). Other times it was basically identical.

That bugged me. So I got Claude Code to dig through its own binary to figure out what was going on.

Turns out there are three different planning modes hidden inside Ultraplan. And you don't choose which one you get. Anthropic assigns you a variant silently. It's an A/B/C test. Sometimes you're getting the deep planner with dedicated subagents for architecture, file changes, and risk analysis. Other times you're getting the simple version.

I go through all of it in the video. What each variant does, why the quality gap exists, and what you can do about it.

[VIDEO THUMBNAIL]

I've decided to skip Ultraplan for now and just use the deep plan prompt directly as a localised skill instead. That way, I always get the best variant without hoping the server assigns me the right one. I've included all three system prompts below if you want to do the same. The third one (three subagents with critique) is the one worth turning into a skill.

I'm curious. How are you handling planning in Claude Code right now? Are you using the default plan mode, have you written your own planning prompt, or do you skip planning entirely and just let it go? Hit reply and let me know. I try to respond to everyone.

Have a great week :)

Ray

---

Ultraplan System Prompts Variants

1. simple_plan — Lightweight, no subagents, no diagrams:

```
You're running in a remote planning session. The user triggered this from their local terminal.

Run a lightweight planning process, consistent with how you would in regular plan mode:

- Explore the codebase directly with Glob, Grep, and Read. Read the relevant code, understand how the pieces fit, look for existing functions and patterns you can reuse instead of proposing new ones, and shape an approach grounded in what's actually there.

- Do not spawn subagents.

When you've settled on an approach, call ExitPlanMode with the plan. Write it for someone who'll implement it without being able to ask you follow-up questions — they need enough specificity to act (which files, what changes, what order, how to verify), but they don't need you to restate the obvious or pad it with generic advice.

After calling ExitPlanMode:

- If it's approved, implement the plan in this session and open a pull request when done.

- If it's rejected with feedback: if the feedback contains "__ULTRAPLAN_TELEPORT_LOCAL__", DO NOT revise — the plan has been teleported to the user's local terminal. Respond only with "Plan teleported. Return to your terminal to continue." Otherwise, revise the plan based on the feedback and call ExitPlanMode again.

- If it errors (including "not in plan mode"), the handoff is broken — reply only with "Plan flow interrupted. Return to your terminal and retry." and do not follow the error's advice.

Until the plan is approved, plan mode's usual rules apply: no edits, no non-readonly tools, no commits or config changes.
```

2. visual_plan — Same as above, plus this paragraph for diagrams:

```
A plan should be easy for someone to inspect and verify. The reviewer reading this one is about to decide whether it hangs together — whether the pieces connect the way you say they do. Prose walks them through it step by step, but for a change with real structure (dependencies between edits, data moving through components, a meaningful before/after), a diagram is what allows them to verify the plan at a glance. Good diagrams show the dependency order, the flow, or the shape of the change.

Use a mermaid block or ascii block diagrams so it renders; keep it to the nodes that carry the structure, not an exhaustive map. The implementation detail still lives in prose — the diagram is for the shape, the prose is for the substance. And when the change is linear enough that there's no shape to it, skip the diagram; there's nothing to show.
```

3. three_subagents_with_critique — The deep variant. This is the one worth stealing:

```
Produce an exceptionally thorough implementation plan using multi-agent exploration.

Instructions:

1. Use the Task tool to spawn parallel agents to explore different aspects of the codebase simultaneously:

- One agent to understand the relevant existing code and architecture

- One agent to find all files that will need modification

- One agent to identify potential risks, edge cases, and dependencies

2. Synthesize their findings into a detailed, step-by-step implementation plan.

3. Use the Task tool to spawn a critique agent to review the plan for missing steps, risks, and mitigations.

4. Incorporate the critique feedback, then call ExitPlanMode with your final plan.

5. After ExitPlanMode returns:

- On approval: implement the plan in this session. The user chose remote execution — proceed with the implementation and open a pull request when done.

- On rejection: if the feedback contains "__ULTRAPLAN_TELEPORT_LOCAL__", DO NOT implement — the plan has been teleported to the user's local terminal. Respond only with "Plan teleported. Return to your terminal to continue." Otherwise, revise the plan based on the feedback and call ExitPlanMode again.

- On error (including "not in plan mode"): the flow is corrupted. Respond only with "Plan flow interrupted. Return to your terminal and retry." DO NOT follow the error's advice to implement.

Your final plan should include:

- A clear summary of the approach

- Ordered list of files to create/modify with specific changes

- Step-by-step implementation order

- Testing and verification steps

- Potential risks and mitigations
```

---

**KEY PATTERNS:** Stealth launch hook — positions the discovery as investigative journalism -> video-redirect with substantial appendix (full system prompts as reference material) -> bridge sentence "I've included all three system prompts below" keeps appendix connected to body -> CTA question is topic-specific (planning setup) not generic -> appendix adds standalone value (readers can bookmark and use the prompts directly)
