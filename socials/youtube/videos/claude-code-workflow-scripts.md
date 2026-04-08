---
tags:
  - youtube
  - script
  - claude-code
  - workflows
status: uploaded
date: 2026-04-07
---
## Video Plan: "Claude Code Has a Build System Now — And It's Not What You Think"

| # | Title | Formula |
|---|-------|---------|
| 1 | **"Claude Code Has a Build System Now — And It's Not What You Think"** | Curiosity gap + reframe |
| 2 | **"I Found a Hidden Feature in Claude Code's Source Code"** | Discovery + exclusivity |
| 3 | **"Claude Code Workflows: Skills Were Just the Beginning"** | Escalation + specificity |


I reverse-engineered a hidden feature inside Claude Code's source code. It's called Workflow Scripts. It's not in the public build — Anthropic stripped it before release. But I was able to figure out exactly how it works and rebuild it using the tools we already have.

And honestly? It changes how I think about what Claude Code is becoming.

### The Problem (0:30–2:00)

So here's where we are today. You've got skills — reusable prompts you can trigger with a slash command. You've got hooks — shell scripts that fire on events. You've got subagents — one-off workers you spawn for a task.

And these are all good. But they're all single-shot. A skill runs, it does its thing, it's done. A subagent handles one job and reports back. There's no built-in way to say "do these 8 things in sequence, feed the output of step 1 into step 3, run steps 4 and 5 in parallel, and if step 6 fails, retry it twice then skip."

That's a pipeline. That's an assembly line. And right now, if you want that, you're stitching it together by hand every time.


### The Discovery (2:00–4:30)

So I was going through the Claude Code source — which ships as a bundled JavaScript file you can actually read if you extract the strings. And I kept seeing references to something called WORKFLOW_SCRIPTS.

*Show terminal — grep results:*

```
feature('WORKFLOW_SCRIPTS')
```

It's behind a compile-time feature flag that evaluates to false in the public build. Bun's bundler dead-code-eliminates everything inside those conditionals. So the implementation is gone — but the integration points survived.

And there were a lot of them.

*Show the seams on screen — walk through each one:*

- `tools.ts` — registers a WorkflowTool and calls `initBundledWorkflows()` on startup
- `tasks.ts` — a `LocalWorkflowTask` type alongside the existing shell and agent tasks
- `commands.ts` — dynamically creates slash commands from workflow definitions
- `BackgroundTasksDialog.tsx` — kill, skip, and retry controls per workflow agent
- The task pill shows "N background workflows"
- `runAgent.ts` — groups workflow transcripts under `subagents/workflows/<runId>/`

And then the comment that gave everything away — in SyntheticOutputTool:

*Show the actual comment on screen:*

> "Workflow scripts call agent({schema: BUGS_SCHEMA}) 30-80 times per run with the same schema object reference."

30 to 80 structured agent calls per workflow. This isn't a skill. This is an orchestration engine.


### How It Works (4:30–7:00)

So I verified everything across both the source code and the production binary. Here's what workflow scripts actually are:

**A workflow is a YAML file** with a `meta` block and a list of steps. Each step has a prompt, an optional JSON schema for structured output, a tool allowlist, and error handling config.

**The orchestrator reads the YAML**, builds a dependency graph, and executes steps in order — or in parallel when steps are independent.

**Each step spawns a subagent.** The subagent gets a scoped set of tools — so a "scan files" step might only get Read, Glob, Grep. A "deploy" step gets Bash and Vercel. This is permission isolation per step.

**Structured output uses a clever trick.** Instead of using Claude's `response_format`, they create a fake tool called `StructuredOutput` where the tool's input schema IS the desired output shape. The model thinks it's calling a tool, but it's actually returning validated data. Ajv checks the output against the schema. If it doesn't match, the error goes back to the model to fix.

*Show the SyntheticOutputTool code:*

```typescript
// The tool's inputSchema becomes the output schema
inputJSONSchema: jsonSchema as ToolInputJSONSchema,
async call(input) {
  const isValid = validateSchema(input)
  if (!isValid) throw new Error(`Output does not match schema: ${errors}`)
  return { structured_output: input }
}
```

And they cache the compiled schemas with a WeakMap — because when you're calling the same schema 80 times per workflow, that 1.4ms of Ajv compilation per call adds up.

**Workflows can't spawn workflows.** The WorkflowTool is explicitly blocked inside subagents to prevent infinite recursion. Same principle as not letting a makefile call itself.


### The Rebuild (7:00–9:30)

So I rebuilt this. Not with the Agent SDK or some external script — just using Claude Code's existing skill system and the Agent tool.

*Show the skill structure:*

```
~/.claude/skills/workflow/
├── SKILL.md                  # The orchestrator
├── references/
│   └── format.md             # Full YAML format reference
└── workflows/
    ├── code-audit.yaml       # 4-step audit pipeline
    └── quick-scan.yaml       # 2-step scan
```

The skill handles everything — creating, editing, listing, deleting, validating, and running workflows. Type `/workflow create deploy` and it walks you through defining each step interactively. Type `/workflow run code-audit` and it orchestrates the whole thing.

*Show a workflow running — the code-audit example:*

Step 1 scans the codebase. Step 2 and 3 run in parallel — security scan and test coverage — both using the output from step 1. Step 4 combines everything into a report.

The key insight from Anthropic's implementation: steps can reference each other. `{{steps.scan-files.total_files}}` in step 2's prompt gets replaced with the actual number from step 1's JSON output. The dependency graph figures out the execution order automatically.

*Show the YAML for this:*

```yaml
- id: security-scan
  prompt: |
    Review the codebase for vulnerabilities.
    The codebase has {{steps.scan-files.total_files}} files.
  schema:
    type: object
    required: [vulnerabilities, risk_level]
    properties:
      vulnerabilities:
        type: array
        items: { ... }
      risk_level:
        type: string
        enum: [low, medium, high, critical]
  parallel: true
```


### "Wait — Doesn't This Just Chain Skills?" (9:30–11:30)

Now here's a subtlety that tripped me up when I first built this. You might be thinking — this is just a skill that calls other skills, right? A meta-skill?

No. And the distinction matters.

**Workflows don't chain skills. They chain raw subagents.**

Each step in a workflow spawns a disposable agent. That agent has no idea it's part of a workflow. It doesn't load any skill. It doesn't get a SKILL.md. It just receives a prompt — "count the files in this codebase and return JSON matching this schema" — does the work, returns the data, and dies.

The intelligence lives in the YAML definition and the orchestrator. Not in the workers.

*Show diagram: orchestrator reads YAML → spawns dumb agents → collects JSON → pipes to next step*

And this is exactly what Anthropic built internally. Their `WorkflowTool` calls `agent({schema: BUGS_SCHEMA})` — raw agent invocations with output schemas. Not skill invocations.

**Skill chaining would be different.** That would be a meta-skill — a high-level skill whose instructions say "first run `/scan`, then run `/review`, then run `/deploy`." Each step invokes an actual installed skill with its own SKILL.md, its own reference files, its own bundled scripts. Each step carries expertise.

So you've got three levels here:

*Show three levels on screen:*

**Level 1: Meta-skill.** A skill that chains other skills. The model is the orchestrator. It decides what to pass between steps. It exercises judgment — if scan finds critical issues, it might skip deploy entirely. But it's unpredictable. You can't guarantee step 2 gets a specific data shape from step 1.

**Level 2: YAML workflow.** The YAML is the orchestrator. Steps are raw agents with schema contracts. `{{steps.scan.total_files}}` gets replaced with the exact number from step 1. No model in the middle deciding what to pass forward. Reliable, repeatable, but rigid.

**Level 3: Both.** And nothing stops you from mixing them. A workflow step could invoke a skill if you wanted — just write "Use the /review skill" in the step's prompt and give the agent access to the Skill tool. Now you've got schema-enforced pipeline structure with skill-level expertise at each node.


So when should you use what?

**Use a meta-skill** when you need judgment between steps — dynamic branching, creative error recovery, semantic context passing. "If the security scan found something critical, change the deploy target to staging instead."

**Use a YAML workflow** when you need reliability — schema contracts, declarative parallelism, resumability. "Run these 5 checks in parallel, collect structured results, generate a report. Same thing every time."

**Use both** when you need reliable structure with smart steps. The pipeline is deterministic. The individual steps are intelligent.

Most people should start with a meta-skill. Reach for YAML when you're running the same pipeline across projects, need parallel execution, or need guaranteed data shapes between steps.


### The Honest Limits (11:30–13:00)

Now I want to be upfront about what my rebuild can and can't do — because I don't want you to think this is the same thing Anthropic has internally.

**What works well.** Schema contracts are real. When I ran the quick-scan workflow on the Claude Code source, step 1 returned `{total: 17411}` and step 2's prompt got exactly that number interpolated in. Not "about seventeen thousand files" — the actual number. That's the whole point.

The YAML is genuinely declarative. You read it and know exactly what will happen. And it's reusable — drop the same YAML into any project, run `/workflow run code-audit`, same pipeline every time.

**But here's what's different from Anthropic's version.**

My orchestrator is still Claude. It reads the YAML and decides to spawn agents. It could misparse the interpolation, forget a step, or do things in the wrong order. Anthropic's internal version almost certainly runs the orchestrator in code — deterministic, no model in the loop.

There's no real schema validation. I tell the subagent "return JSON matching this schema" and trust it. Anthropic's version runs Ajv — an actual JSON schema validator — and if the output doesn't match, it throws an error back to the model. Mine just hopes for the best.

And there's no checkpointing. If step 4 of 6 fails, you restart from step 1. Anthropic's version has kill, skip, and retry per agent — real process management.

*Show the gap on screen:*

| Feature | Anthropic's internal | My rebuild |
|---|---|---|
| Orchestrator | Code (deterministic) | Claude (best-effort) |
| Schema validation | Ajv (enforced) | Prompt instruction (trusted) |
| Checkpoint/resume | Yes | No |
| Kill/skip/retry UI | Yes | No |
| Permission model | Custom per-workflow | Inherits parent session |

So this is an approximation. A useful one — I've been running it and the structured output comes back clean consistently. But if you want the full thing with real validation and process management, you'd build the orchestrator as an Agent SDK script or a Node.js app that reads the same YAML but runs outside of Claude's context window.

The good news is Anthropic is clearly building toward making this public. The integration points are already in the codebase. When it ships, you'll have the real thing. Until then, this gets you 80% of the way there.


### Where This Is Heading (13:00–13:45)

This is clearly the direction Claude Code is going. The internal feature has kill, skip, and retry per step. It has a background task manager. It has its own permission UI. They're not building this for fun — they're turning Claude Code from an interactive assistant into something that can run complex, multi-step automation unattended.

And I'm not the only one building toward this — there are already repos with thousands of stars doing workflow orchestration for Claude Code. But none of them have what Anthropic's internal version has: schema-enforced contracts between steps and a real process manager.

Think about what you could build:
- A PR review pipeline that checks security, performance, and correctness in parallel
- A deployment workflow that builds, tests, deploys, and monitors
- A research pipeline that searches multiple sources, synthesizes findings, and produces a structured report
- A migration workflow that audits a codebase, plans changes, and applies them file by file

Each of those is a YAML file. Write it once. Run it forever.


### Closer (13:45–14:00)

The skill is open — I'll link it below. You can install it, create your own workflows, and start building pipelines today. And when Anthropic ships the real thing, you'll already understand the architecture because it's the same pattern — YAML definitions, schema contracts, subagent execution.

If this is the kind of deep dive that helps you, I cover a lot more in my Claude Code masterclass. Link's in the description.
