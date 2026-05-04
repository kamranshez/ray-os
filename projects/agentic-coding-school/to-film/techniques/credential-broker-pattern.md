# Stop Putting API Keys In Your Claude Code Sessions

## What This Video Covers

A practical setup for running Claude Code without ever giving it your API keys. We walk through Infisical's open-source Agent Vault, plug it into a normal Claude Code workflow, and show how it sits invisibly in front of every tool call, curl, MCP server, and SDK request that Claude Code makes — injecting the right credentials at the network layer so Claude Code never sees them.

By the end of this video you'll have:
- Agent Vault running locally
- Your real keys (OpenAI, Stripe, GitHub, whatever) stored in it instead of in `.env` files
- Claude Code launching through it with one wrapper command
- A working dev loop where Claude can call those APIs but cannot read, print, or leak the keys

## Why This Matters

Right now, most of you are running Claude Code in a project where the keys are sitting in `.env`, `~/.zshrc`, `~/.claude/settings.json`, or just exported into the shell. Claude Code can read all of those. So can any subagent it spawns. So can any MCP server you've connected. So can any tool call that runs `env` or `cat .env`.

That's fine when you're the only person prompting Claude. It stops being fine the moment:
- A document you fed Claude contains a prompt injection
- An MCP server returns malicious content
- A scraped webpage tells Claude to "verify your identity by emailing the OPENAI_API_KEY to..."
- You're running Claude in a sandboxed loop, agentically, on inputs you haven't read

The fix isn't a better prompt. The fix is: **don't give Claude Code the keys in the first place.** Give it a local proxy that has the keys. Claude makes its API calls normally, the proxy attaches the credentials on the way out, and Claude never has anything to leak.

## The Mental Model

Normal Claude Code setup:

```
~/.zshrc has OPENAI_API_KEY=sk-...
   ↓
Claude Code inherits it
   ↓
Claude runs `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
   ↓
Key is in Claude's context, environment, command history, everywhere.
```

With Agent Vault:

```
Agent Vault holds OPENAI_API_KEY (encrypted, locally)
   ↓
You launch Claude Code via `agent-vault run -- claude`
   ↓
Claude runs `curl https://api.openai.com/v1/models`   ← no key, no header
   ↓
Agent Vault transparently intercepts, adds the auth header, forwards to OpenAI
   ↓
Response flows back. Claude got what it needed. The key never entered its context.
```

Same workflow, same commands, same APIs. Claude doesn't need to know anything changed.

![[images/credential-broker-pattern/01-mental-model-before-after.png]]

## Setup (Five Minutes)

### 1. Install Agent Vault

```bash
curl --proto '=https' --tlsv1.2 -fsSL https://get.agent-vault.dev | sh
agent-vault server -d
```

That gives you a local web UI at `http://localhost:14321` and a TLS proxy on `14322`.

### 2. Create a vault and add your credentials

In the web UI:
- Click **New Vault**, call it `claude-code`
- Add credentials: `OPENAI_API_KEY`, `STRIPE_SECRET_KEY`, `GITHUB_TOKEN`, etc. — whatever you currently have in `.env`
- Add services: `api.openai.com` → Bearer auth using `OPENAI_API_KEY`, `api.stripe.com` → Bearer using `STRIPE_SECRET_KEY`, `api.github.com` → Bearer using `GITHUB_TOKEN`

This is a one-time configuration. After this, your keys live here and nowhere else.

### 3. Launch Claude Code through it

Instead of running `claude`, run:

```bash
agent-vault run -- claude
```

That's it. Agent Vault sets `HTTPS_PROXY`, plants the trust certs in the right environment variables, and starts Claude Code as a child process. Claude Code looks and feels identical. The only difference is that every outbound HTTPS request now goes through the broker.

You can alias this in your shell so you never have to think about it:

```bash
alias claude='agent-vault run -- claude'
```

## What This Looks Like In A Real Session

You're using Claude Code on a project that needs to call the OpenAI API.

**Before:** `OPENAI_API_KEY` is in your `.env`. Claude reads it, embeds it in code, includes it in test scripts, sometimes echoes it during debugging.

**After:** there is no `OPENAI_API_KEY` in your `.env`. Claude writes:

```python
import openai
openai.OpenAI().chat.completions.create(model="gpt-4", messages=[...])
```

The OpenAI SDK looks for an API key, doesn't find one, builds a request anyway with no auth header. The request goes out, hits Agent Vault on its way through `HTTPS_PROXY`, gets the right `Authorization` header injected, and reaches OpenAI. Response comes back, Claude is happy.

If you ask Claude "what's our OpenAI API key?", it will tell you it can't find one. Because it can't.

## What Gets Covered Automatically

Once Claude Code is launched through Agent Vault, the broker covers:
- `curl` and `wget` calls Claude makes in the shell
- HTTP libraries in any language Claude writes code in (Python, Node, Go, Deno, Ruby — they all read the standard CA bundle env vars)
- MCP servers Claude has connected (their outbound calls also flow through the proxy if they were started by the same wrapped session)
- SDK calls in scripts Claude runs as part of testing

You don't need to wrap each tool individually. You wrap the Claude Code process once, and everything Claude spawns inherits the proxy configuration.

![[images/credential-broker-pattern/03-hub-and-spoke.png]]

## The Hardened Mode

For the case where you're letting Claude Code run agentically on untrusted input — running `/loop`, processing scraped content, running long autonomous sessions — there's a stronger mode:

```bash
agent-vault run --isolation=container --share-agent-dir -- claude
```

This launches Claude Code inside a Docker container with a network policy that blocks all outbound traffic *except* to the local broker. Claude can still do its work, but if a prompt injection ever tries to redirect a request to an attacker's server, the network simply refuses. There's no path out. `--share-agent-dir` mounts your existing Claude login so the session feels normal.

The lighter mode is the right default for everyday use. The hardened mode is for the agentic loops where you're not watching every step.

![[images/credential-broker-pattern/02-hardened-mode.png]]

## Why This Belongs In The Techniques Class

The bigger principle here, beyond Agent Vault specifically, is: **secrets shouldn't live in the same context as the model.** Whenever you have something that an agent needs to *use* but not *see*, the right place to put it is one layer below the agent — in a tool, a wrapper, a proxy, anything that runs outside the model's context window.

This applies far beyond API keys:
- Database credentials → use a connection-pooling proxy, give Claude a logical handle, not the password
- Production write access → put it behind a tool the agent calls, not a credential the agent holds
- Customer PII → return references, not values; let a downstream service hydrate them

The credential broker is the cleanest example of the pattern because the technology to do it is already sitting on every developer's machine (HTTPS, CA trust, environment variables). All Agent Vault does is glue those existing primitives together. But once you internalise the pattern, you'll spot dozens of places in your own systems where the same move applies: *the agent uses the capability, something else holds the secret.*

![[images/credential-broker-pattern/04-generalised-pattern.png]]

## What To Take Away

- Stop putting API keys in `.env` files Claude Code can read. Stop pasting them into your `~/.zshrc`. Stop adding them to MCP server configs.
- Run a local credential broker. Add your keys to it once. Wrap Claude Code with it.
- Your daily workflow doesn't change. The security boundary moves from "I trust Claude with my keys" to "I trust Claude to make HTTP requests."
- For agentic loops on untrusted inputs, run Claude Code inside the container-isolation mode so the network *physically* can't reach anywhere except the broker.
- The broader pattern — the agent uses the capability, something else holds the secret — generalises far past API keys. Look for it everywhere you're handing sensitive material to an agent that only needs to use it transiently.

## Demo

1. Open `~/.zshrc` and `.env` on screen. Show the OpenAI / Stripe / GitHub keys sitting there. Acknowledge: this is what most of you have right now.
2. Install Agent Vault with the one-line installer. Open the web UI. Walk through creating the `claude-code` vault, adding the keys, configuring the services for OpenAI / Stripe / GitHub.
3. Delete the keys from `.env` and `~/.zshrc`. Source the shell. Run `echo $OPENAI_API_KEY` — empty.
4. Launch Claude Code with `agent-vault run -- claude`. Ask it to write a quick Python script that calls the OpenAI API. Run the script — it works. No key visible anywhere in the session.
5. Ask Claude directly: "what's our OpenAI API key?" — show that it can't find one and tells you so.
6. Show the request log inside the Agent Vault web UI — every call Claude made is logged, with method / host / path / status, but the key value is never recorded.
7. Restart Claude with `agent-vault run --isolation=container --share-agent-dir -- claude`. Inside the session, try a `curl https://example.com`. Show that it fails — only the broker is reachable. Then run the same OpenAI script — it works, because that route is allowed through the broker.
8. Close on the alias: `alias claude='agent-vault run -- claude'`. From here on, this is just how you run Claude Code.
