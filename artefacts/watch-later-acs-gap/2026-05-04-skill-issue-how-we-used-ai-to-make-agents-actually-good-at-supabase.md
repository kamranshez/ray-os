---
title: "Skill Issue: How We Used AI to Make Agents Actually Good at Supabase — Pedro Rodrigues, Supabase"
video_url: https://www.youtube.com/watch?v=GmAQKINjv1E
video_id: GmAQKINjv1E
channel: AI Engineer
published: 2026-05-04
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Skill Issue: How We Used AI to Make Agents Actually Good at Supabase — Pedro Rodrigues, Supabase**](https://www.youtube.com/watch?v=GmAQKINjv1E) - AI Engineer - uploaded 2026-05-04

> net-new ACS video available: eval-driven skill development (proving a skill actually helps) is uncovered by the catalog.

## The one idea worth a video

- **Spine 1: You cannot trust that a skill improves your agent until an eval proves it, so treat skill.md like code and run it through a with-skill versus without-skill harness.** This is the spine because it reframes every authoring tip in the video: writing the skill is the easy part, and the whole back half (metrics, eval.json, LLM-as-judge, deterministic assertions, the failed eval) exists only to answer "did it actually help?" — VERDICT: ❌ net-new video available.
- **Spine 2: Whether a skill loads and whether it improves behavior are two separate problems, and the description is a distinct optimization target you engineer and test on its own.** De-merged from Spine 1 because it has its own demo (varying description wording, measuring load rate) — but ACS already teaches reliable triggering — VERDICT: 🟡 partial, does not clear the gate.

**Summary.** Pedro Rodrigues, a Supabase AI tooling engineer, runs a hands-on AI Engineer workshop on writing agent skills and proving they help using an eval-driven development loop.

🔴 1 net-new · 🔗 0 complement · 🟡 1 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1 — Eval-driven skill development.** The claim: you cannot trust that a skill improves your agent until an eval proves it, so treat skill.md like code and run it through a with-skill versus without-skill harness. Why it's non-obvious: skills look like documentation, and a single successful live run feels like proof, so most people ship on vibes. Pedro's own demo punctures this. Even after the skill loaded, nondeterminism meant the without-skill run sometimes passed and the with-skill run sometimes failed, and a badly written assertion flagged a correct skill as broken. Why it's true: an LLM in the loop makes output nondeterministic, so a one-shot observation confounds skill quality with luck; only repeated, controlled runs with deterministic assertions (was the security invoker flag emitted?) plus LLM-as-judge grading separate signal from noise. It generalizes cleanly beyond skills to system prompts, CLAUDE.md rules, and subagent instructions: any markdown that steers an agent is a testable artifact, and eval-driven development mirrors test-driven development. How it goes wrong: the hardest, most error-prone part is authoring representative scenarios and correct assertions, because a buggy eval silently lies and an LLM judge can hallucinate a grade.

**Spine 2 — The description is a separate optimization target.** The claim: whether a skill loads and whether it improves behavior are two independent problems, and the description must be engineered and tested separately. Why it's non-obvious: teams pour effort into the skill body while treating the front matter as a label, then wonder why a good skill never fires. Why it's true: the description is the only thing loaded into context up front under progressive disclosure, so it alone decides invocation; Pedro found that starting it with the verb "use" measurably raised load rate on Claude, and that a bare prompt only prays the skill triggers while slash-invoking or writing "use skillname" forces it. The mechanism means you can eval triggering exactly like behavior: define prompts where the skill should and should not load, run headless, and check the CLI for whether it fired. It generalizes to any progressive-disclosure routing, including Anthropic's new tool-search tool for MCP. How it goes wrong: description tuning stays fragile and model-specific, so wording that triggers reliably on one model may not on another, which is why ACS already treats reliable triggering as its own hard problem (see "Triggering Skills Reliably," Context Engineering).

## 🎬 Proposed ACS videos

**1. Stop Guessing If Your Skill Works: Eval It**
- HOOK: Your skill "worked on your machine" once, so you shipped it. That proves nothing when an LLM is in the loop.
- THE PROMISE: For anyone who writes skills or CLAUDE.md rules: after this you can run a with-skill versus without-skill eval and know, not hope, that your skill moved the needle.
- THE SHAPE:
  1. Write a small skill (the Supabase security invoker case) and watch the agent confidently ship a broken result without it.
  2. Define metrics first, eval-driven development style: what does "good" actually mean for this skill?
  3. Build the harness from the agent-skills open standard eval.json: prompt, expected output, tool-call assertions, reset DB to seeded state.
  4. Run Claude Code headless twice, with and without the skill, and diff the two output workspaces.
  5. The gotcha: a badly written assertion fails a correct skill, and an LLM judge can hallucinate a grade, so favor deterministic checks.
- SPINE: Spine 1.
- SLOT: Master Claude Code > Skills (or a new "Evaluating Skills" chapter); alternatively Advanced Techniques > Skills as Force Multipliers.
- RELATIONSHIP: ❌ net-new. The Skills chapter teaches authoring (models, agents, arguments, forked contexts, find-skills) and Context Engineering teaches reliable triggering, but nothing in ACS teaches measuring whether a skill improves agent behavior. ACS has no evals content at all.
- PROOF TO REUSE: the RLS security-invoker demo where Claude reports success while exposing every salary; the agent-skills open standard eval.json structure; the with/without-skill A/B run; LLM-as-judge plus deterministic tool-call assertions; the false-negative eval that failed a passing skill ("agents evaluating agents").

## 📚 Full wisdom (reference)

**SUMMARY** — Pedro Rodrigues, a Supabase AI tooling engineer, runs a hands-on AI Engineer workshop on writing agent skills and proving they help using an eval-driven development loop.

**IDEAS**
- Writing a skill is easy; writing one that actually improves your agent's performance is genuinely hard.
- Skills are folders of instructions and files that package repeated workflows and custom context for agents.
- Progressive disclosure loads only the front matter first, then the body when the agent needs it.
- Think of skill.md as a book index on steroids, linking out to reference files and scripts.
- Reference files can reference other files, so a single skill becomes a graph of linked documents.
- The MCP versus skills debate is over: use both because each one solves a different problem.
- Use MCP for integrations and remote actions; use skills to add workflow context, instructions, and scripts.
- MCP tools run server-side with no environment; skill scripts run locally, tied to your own OS.
- Because a skill is just markdown, you can test it like code, but evals fit better.
- Evals can judge the steps, reasoning, and tools an agent used, not just its final output.
- Eval-driven development mirrors test-driven development: define metrics first, write the skill, run evals, grade, then iterate.
- The Postgres trap: a new view bypasses row-level security unless you set the security invoker flag.
- Claude created the view and confidently reported success, yet silently exposed every employee's salary to everyone.
- Starting a skill description with the verb "use" measurably raises the chance Claude actually loads it.
- Slash-invoking a skill or writing "use skillname" guarantees loading; a bare prompt only hopes it triggers.
- The agent-skills open standard proposes an eval.json holding prompts, expected outputs, and tool-call assertions per scenario.
- A badly written eval fails a passing skill, so wrong assertions mislead you like buggy tests.

**INSIGHTS**
- A skill changes behavior by merging near the system prompt, acting as an on-demand prompt template.
- Whether a skill loads and whether it improves behavior are two separate problems needing separate tests.
- Eyeballing that it worked once cannot prove a skill helped rather than nondeterministic luck being kind.
- The hardest part of writing evals is designing representative scenarios, not the harness or the grading.
- Asserting that a specific tool was called is more reliable than matching exact nondeterministic text output.
- LLM-as-judge automates grading of nondeterministic output but can hallucinate, so keep deterministic checks wherever you can.
- Models confidently miss training-data gaps like security invoker; a skill injects exactly the missing knowledge back.
- Skills and MCP compose: the tool provides the connection, the skill describes how to use it.
- Progressive disclosure went from unmentioned six months ago to a recognised north star of agent development.
- In production, treat skills like documentation: version them, keep them updated, and prune ones nobody loads.

**QUOTES**
- "we're more focused on DAX which is the same thing but for agents" — Pedro Rodrigues
- "the secret sauce is has been basically skills" — Pedro Rodrigues
- "you can think of it as the index on steroids" — Pedro Rodrigues
- "the answer is uh you should use both to be honest" — Pedro Rodrigues
- "it's a tail older than time that it's working on my machine, but I don't know if it's going to work on your agent" — Pedro Rodrigues
- "the verb use uh increases the chances of the skill being loaded" — Pedro Rodrigues
- "we basically have agents evaluating agents" — Pedro Rodrigues
- "the behavior changed uh once it loaded the skill" — Pedro Rodrigues
- "this is like on the agent side right the agent decides when to load this" — Pedro Rodrigues

**HABITS**
- Pedro vibe-codes his conference slide decks as a localhost Next.js app instead of using Google Slides.
- He resets the local database to seeded state before every eval run for a clean baseline.
- He runs Claude Code headless in print mode to execute each eval scenario as a task.
- He slash-invokes skills during live demos because he simply cannot risk the description failing to trigger.
- He installs skills using Vercel's npx skills package, picking the agent and the project-versus-global scope interactively.
- He uses the local Supabase MCP server, needing no authentication, to list tables and apply migrations.
- He runs each eval twice, with and without the skill, then compares the two output workspaces.
- He keeps global skills messy while experimenting but treats production skills as clean, versioned CI artifacts.

**FACTS**
- Supabase is the open-source Firebase alternative, providing hosted Postgres, authentication, storage, and Lambda-style edge functions out-of-the-box.
- Postgres row-level security lets you filter which rows each user sees directly at the database layer.
- Since Postgres 15, the security invoker flag makes a view respect the calling user's RLS policies.
- By default a Postgres view runs with its creator's permissions, thereby bypassing row-level security policies entirely.
- Skills launched around October or November last year, immediately sparking the original MCP-versus-skills debate among developers.
- The production Supabase MCP server exposes roughly 29 tools; the local workshop version exposes about 20.
- OpenAI published a blog post, "systematically evaluate agent skills," around January 2026, framing eval-driven skill development.
- Anthropic recently shipped a tool-search tool, bringing progressive disclosure to MCP tool loading in Claude Code.

**REFERENCES**
- Supabase (backend-as-a-service), Postgres, Firebase
- Braintrust (eval + observability platform); Langfuse; a Braintrust CEO podcast Pedro cites
- Claude Code (headless / print mode), Cursor, plugins
- Vercel's `npx skills` package for installing skills across agents
- agent-skills open standard (landing page + eval.json test structure)
- OpenAI blog post: "systematically evaluate agent skills"
- MCP; Anthropic's tool-search tool; MCP dev summit (New York); an MCP co-founder talk on the 10th
- Next.js (the vibe-coded slide deck and demo app)
- Speaker: Pedro Rodrigues, AI tooling engineer at Supabase; AI Engineer Europe conference

**ONE-SENTENCE TAKEAWAY** — A skill only earns trust once an eval proves it changes agent behavior for better.

**RECOMMENDATIONS**
- Before writing a skill, define the metrics that describe what good agent behavior actually looks like.
- Run every skill eval twice, with and without the skill, and diff the resulting agent behavior.
- Start each skill description with the verb "use" to raise how reliably Claude loads it automatically.
- Assert on tool calls rather than exact text so nondeterministic output does not break your evals.
- Reset your database to seeded state before each eval so every run starts from identical ground.
- Adopt the agent-skills open standard eval.json format to get started with structured skill evaluations really quickly.
- When a skill must not fail live, slash-invoke it rather than trusting automatic description-based triggering alone.
- Treat production skills like living documentation: version, update, and audit whether users still actually load them.
- Combine an MCP tool with a skill that describes exactly how and when to invoke it.
