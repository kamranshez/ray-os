---
duration: "10-14 min"
batch: 2
order: 10
batch_name: "Bonus Techniques"
class: "claude-code"
chapter: "MCP Servers"
---

## The Core Idea

![[images/code-execution-with-mcp/progressive-tool-loading.jpg]]

MCP servers can chew through your context window before you send a single message.

Not because one tool is massive.

Because you load too many tools.

Every tool definition has a name, description, input schema, examples, nested fields, enum values, and edge cases. Put enough MCP servers together and half your context can disappear before the agent has done any work.

The answer is not to make the model smarter at staring at a giant list of tools.

The answer is to stop loading the giant list.

In code mode, you can treat tools like a codebase. Give the agent a file tree. Put thin wrappers in that tree. Tell it where the tools live in `CLAUDE.md`. Then let the agent do what it is already good at: explore the codebase, find the right file, read only what matters, write code, and return a small result.

---
## Code Mode Changes The Interface

![[images/code-execution-with-mcp/code-mode-vs-tool-schemas.jpg]]

Code execution gives you a different interface.

Instead of loading every tool definition into the model, you expose the tools as files.

```text
servers/
  bento/
    findSubscriber.ts
    tagSubscriber.ts
  stripe/
    listRecentCustomers.ts
```

Each file is a thin wrapper.

`findSubscriber.ts` finds a Bento subscriber. `tagSubscriber.ts` applies a tag. `listRecentCustomers.ts` lists recent Stripe customers. The wrapper might call an MCP server underneath. It might call a REST API. It might call an SDK. The model does not need to care at first.

The model sees a directory.

That is the whole move.

It can run `ls`. It can use `rg`. It can open the one file whose name matches the task. It can read the function signature. Then it can write code that imports that function and runs it.

This uses the agent for what it does best.

Agents are good at navigating codebases. They know how to inspect a tree, read a file, infer a contract, search for examples, and compose functions. So instead of asking the model to choose from a huge MCP tool menu, you turn the tools into a small codebase and let the agent explore.

---

## Put The Map In CLAUDE.md

![[images/code-execution-with-mcp/claude-md-as-map.jpg]]This pattern gets much better when you tell the agent where the tool code lives.

That belongs in `CLAUDE.md`.

Not every tool definition. Not a huge pasted reference. Just the map.

```md
## Tool Wrappers

Service wrappers live in `servers/`.

- `servers/bento/` contains helpers for subscribers, tags, events, and broadcasts.
- `servers/stripe/` contains helpers for customers, subscriptions, invoices, and payments.
- Read only the wrapper files needed for the current task.
- Prefer writing a temporary script that imports wrappers and prints a small result.
- Do not paste raw service responses into the conversation unless asked.
```

That is enough.

The model now has the routing hint. It knows there is a tool-wrapper directory. It knows the expected behavior. It knows the context boundary. But it does not carry every tool schema in the prompt.

This is the right kind of instruction.

`CLAUDE.md` should not become a second giant tool registry. It should point the agent at the discovery surface.

The file tree is the registry.

The wrapper file is the schema.

Stdout is the return value.

---

## How It Works At Runtime

![[images/code-execution-with-mcp/runtime-loop.jpg]]

Here is the runtime loop.

The agent gets the task.

"Tag recent paid customers in Bento."

It checks the local map in `CLAUDE.md`.

It explores the tree.

```bash
ls servers/
```

It sees `bento/` and `stripe/`.

It reads only the files it needs.

```bash
cat servers/stripe/listRecentCustomers.ts
cat servers/bento/tagSubscriber.ts
```

Then it writes and runs code in the sandbox.

It imports `listRecentCustomers`. It imports `tagSubscriber`. It fetches the recent paid customers. It matches them by email. It tags the matching subscribers in Bento.

Only the final stdout enters the conversation.


That last step is the key.

The raw customer list does not need to enter context. The full subscriber profile does not need to enter context. Every intermediate JSON blob does not need to enter context.

The code can see those things.

The model sees the result.

That is how you get the context reduction. You have moved the noisy part of the workflow into execution, and you keep the conversation focused on decisions.

---

## The 98 Percent Example

![[images/code-execution-with-mcp/98-percent-token-reduction.jpg]]

The example from the source material is a source-to-destination workflow.

With direct tool calls, the system can push around roughly 150,000 tokens through the context.

Why?

Because the model sees the tool definitions up front, then it sees large tool outputs as it works. It fetches data. Reads it. Calls another tool. Reads that result. Calls another tool. Every step is mediated through the conversation.

With code execution, the model writes code that does the workflow inside the sandbox.

The tool calls happen from code. The loop happens in code. The filtering happens in code. The final result is printed back.

Instead of 150,000 tokens, the model might see around 2,000 tokens.

That is roughly a 98 percent reduction.

The exact number depends on the task, but the principle is stable. Stop routing every intermediate step through the model. Let code do the mechanical work. Return the decision-sized result.

---

## Why This Is Different From Tool Search

![[images/code-execution-with-mcp/tool-search-vs-code-search.jpg]]
Tool search is a good pattern too.

The agent starts with a few basic tools and a search tool. When it needs something else, it searches through the catalog and loads the relevant tool definitions on demand.

That is progressive disclosure for tool definitions.

Code execution is a different version of the same idea.

Tool search says: "Search the tool catalog."

Code mode says: "Search the codebase."

Both are trying to avoid front-loading thousands of tokens.

The difference is that code mode lets the agent compose tools after discovery. It can read a wrapper, import it, run it inside a loop, filter the output, combine it with another wrapper, and print only the answer.

That makes it especially useful when the task is multi-step.

If all you need is one simple tool call, tool search may be enough. If you need to do ten calls, filter a dataset, branch on conditions, and update a record, code execution is a better shape.

---
## Secondary Benefits

![[images/code-execution-with-mcp/filter-loops-privacy.jpg]]

There are three secondary benefits that matter.

First, filter in code, not in context.

If the workflow touches a 10,000 row spreadsheet, the model should not read 10,000 rows. The script should fetch the sheet, filter the rows, sort them, maybe join them against another source, and return the five rows the model actually needs.

The model is for judgment.

Code is for filtering.

Second, loops and conditionals become code.

Without code execution, every iteration can become a model round trip. Call the tool. Inspect the result. Call the tool again. Inspect again. That is slow and expensive.

With code execution, the loop happens once inside the sandbox.

```ts
for (const doc of docs) {
  const customer = await findSubscriber(doc.email);
  if (customer?.status === "active") {
    matches.push({ email: doc.email, tag: "paid-customer" });
  }
}

console.log(JSON.stringify(matches.slice(0, 5), null, 2));
```

The model writes the loop. The runtime executes the loop. The context gets the answer.

Third, privacy improves by default.

Emails, phone numbers, customer notes, and raw customer fields can flow through the execution environment without entering the conversation. The wrapper can redact. The script can hash. The final stdout can contain only IDs, counts, and the fields required for the task.

This is not magic privacy. You still need a real sandbox, correct permissions, and sane logging.

But the default posture is better.

Raw data goes through code.

Small results go to the model.

---
## The Folder Is The Interface

![[images/code-execution-with-mcp/folder-as-interface.jpg]]

The folder structure is part of the design.

If the folder is obvious, discovery is cheap.

If the folder is vague, discovery gets noisy.

You can group wrappers by service:

```text
servers/
  bento/
  stripe/
  linear/
  gmail/
```

Or by workflow:

```text
servers/
  content-intake/
  lead-research/
  customer-success/
  finance/
```

Both can work.

The important part is that the names match how you ask for work.

If you say "tag recent paid customers in Bento," `servers/bento/tagSubscriber.ts` should be easy to find.

If you say "run the lead research workflow," `servers/lead-research/` should be easy to find.

This is not just organization for humans. It is interface design for agents.

---

## When To Use This Pattern

![[images/code-execution-with-mcp/when-to-use-code-mode.jpg]]
Use code execution with MCP when you have many tools available, but each task only needs a few.

Use it when the workflow is multi-step.

Use it when the output is large and needs filtering.

Use it when the tool calls involve loops.

Use it when raw data should not enter the model context.

Use it when you want the agent to discover capabilities through the same moves it uses in a codebase: list, search, read, import, run.

Do not use it for everything.

If you have three simple tools and the model needs one direct call, normal MCP is fine. If the official MCP is well scoped and returns clean outputs, use it. If tool search gives you the right level of progressive disclosure, use that.

This pattern earns its keep when the loaded-tool problem is the bottleneck.

---

## Demo

The demo should show the contrast.

1. Open a project that has `CLAUDE.md`.
2. Show the `CLAUDE.md` section that points the agent to `servers/` and tells it to read only the wrappers it needs.
3. Show the `servers/` tree with `bento/` and `stripe/`.
4. Open `stripe/listRecentCustomers.ts` and `bento/tagSubscriber.ts`.
5. Give Claude Code the task: "Find recent paid Stripe customers and tag the matching Bento subscribers as paid customers."
6. Let the agent explore with `ls servers/` and `rg "subscriber|customer|tag" servers/`.
7. Let it read only the two or three wrapper files it needs.
8. Have it write a temporary script that imports those wrappers.
9. Run the script in the sandbox.
10. Show the final stdout:

```json
{
  "status": "tagged",
  "tag": "paid-customer",
  "matchedSubscribers": 42,
  "skippedCustomers": 3
}
```

Then show what did not enter the conversation.

The whole Stripe customer export did not enter. The whole Bento subscriber profile did not enter. The loop did not round trip through the model. The intermediate data stayed in code.

The agent still used tools.

It just found them like code.

Then show a second Stripe example.

This time the task is: "Find subscriptions with failed payments in the last 48 hours and tag those Bento subscribers as payment-failed."

The agent should discover a slightly different set of wrappers:

```text
servers/
  stripe/
    listFailedPayments.ts
    getCustomer.ts
  bento/
    findSubscriber.ts
    tagSubscriber.ts
    addEvent.ts
```

The temporary script does the mechanical work:

1. Pull failed payments from Stripe.
2. Resolve each payment to a customer email.
3. Find the matching Bento subscriber.
4. Apply `payment-failed`.
5. Optionally record a Bento event called `stripe.payment_failed`.
6. Print only a summary.

```json
{
  "status": "processed",
  "tag": "payment-failed",
  "matchedSubscribers": 18,
  "eventsRecorded": 18,
  "skippedPayments": 2
}
```

This second example makes the point clearer. The tools are not the workflow. The code is the workflow. The tools are small capabilities the agent discovers and composes.

---

## Promote The Workflow Into A Tool

![[images/code-execution-with-mcp/promote-script-to-wrapper.jpg]]

There is one final move.

Sometimes the agent discovers that your existing tools are not quite good enough.

Maybe the workflow needs eight steps every time. Maybe the same wrappers keep getting composed in the same order. Maybe the agent has to do too much searching before it can run the task. Maybe the temporary script works, but it is obviously something you will want again.

At that point, tell the agent to make a new script.

Not during the first attempt. First, let it explore. Let it write the temporary script. Let it prove the workflow works. Then at the end, say:

```text
This worked. Turn the temporary script into a reusable wrapper in `servers/bento/tagRecentPaidCustomers.ts`.
Keep the interface small.
Input: a date range and tag name.
Output: counts, skipped records, and errors.
Do not print raw customer or subscriber data.
```

Now the next run is cheaper.

The first time, the agent had to discover `listRecentCustomers.ts`, `findSubscriber.ts`, and `tagSubscriber.ts`. The second time, it can discover one file:

```text
servers/bento/tagRecentPaidCustomers.ts
```

This is how the tool codebase gets better over time.

The agent does a workflow manually once. If it is valuable, you promote it into a wrapper. Future agents find the higher-level wrapper instead of redoing the whole exploration path.

That is a very natural loop:

1. Discover the low-level wrappers.
2. Compose them in a temporary script.
3. Run the workflow.
4. If the workflow is reusable, promote it into a named script.
5. Add a short note in `CLAUDE.md` so future agents know it exists.

You can also put guardrails around this with hooks.

For example, a hook can stop the agent from editing files under `servers/` without asking you first. Or it can require confirmation before creating a new reusable wrapper. Or it can block changes to sensitive tool files unless the agent explains why the edit is needed.

You do not need to understand hooks deeply for this video. The hook video covers that pattern separately.

The point here is simple. Code mode lets the agent improve the tool surface, but you probably want a permission boundary around that improvement. Temporary scripts are cheap. Reusable tool wrappers should be intentional.