---
name: binary-explorer
description: Reverse-engineer Claude Code's own binary to explain how hidden/undocumented features work. Use when the user asks about a Claude Code feature, feature flag, hidden toggle, internal prompt, or wants to understand how something works under the hood — especially unreleased, gated, or undocumented functionality. Also trigger when the user says "how does X work in the binary", "what does this feature flag do", "find the prompt for X", "reverse engineer X", or mentions a specific codename/flag. Do NOT use for general Claude API questions or for features that are well-documented.
---

# Binary Explorer

Reverse-engineer features from the Claude Code binary by extracting and searching its embedded strings and minified JS bundle.

## How it works

Claude Code ships as a Bun single-executable (~190MB Mach-O on macOS ARM). The entire JS bundle is embedded in the binary as plain text, which means feature flags, internal prompts, config keys, and logic are all searchable via `strings` extraction.

## Step 1: Locate and extract

Run the extraction script. It finds the real Claude binary (following symlinks, skipping wrappers), extracts all readable strings, and caches the result so subsequent queries are instant.

```bash
bash <skill-dir>/scripts/extract.sh
```

This outputs the path to the cached strings file (e.g., `~/.claude/cache/binary-strings/2.1.81.txt`). If the cache already exists for this version, extraction is skipped.

## Step 2: Search for the feature

Given the user's query about a feature, search the extracted strings. The approach depends on what the user is asking about:

**If they name a specific feature flag or codename** (e.g., `tengu_onyx_plover`):
```bash
grep -i "<flag_name>" <strings_file>
```

**If they describe a feature by behavior** (e.g., "auto-dream", "memory consolidation"):
- Start with keyword searches using likely terms
- Look for function names, config keys, prompts, and log messages
- Follow the trail: if you find a function name like `gt7`, search for that to find related code

**Common patterns in the minified bundle:**
- Feature flags: `lT("<flag_name>", null)` — reads remote config
- Internal prompts: Long template literal strings, often with `\n` joins
- Config defaults: Object literals like `pt7 = { minHours: 24, minSessions: 5 }`
- Debug logs: `v("[featureName] ...")` with descriptive messages
- Telemetry events: `F("event_name", { ... })`
- Settings checks: `h8().<settingName>` reads local settings
- Guard conditions: Functions that return `!1` (false) or `!0` (true) for feature gating

## Step 3: Analyze and explain

Once you've found the relevant code, explain it to the user:

1. **What the feature does** — synthesize from prompts, log messages, and code flow
2. **How it's gated** — remote config flag? local setting? both?
3. **Triggering conditions** — what thresholds or conditions must be met
4. **Default values** — extract hardcoded defaults from the minified code
5. **The actual prompts** — if the feature spawns a subagent, quote the prompt verbatim
6. **Telemetry** — what events it fires (helps understand the lifecycle)

Present findings as a structured breakdown. Quote exact strings from the binary where relevant — the user wants to see the raw evidence, not just a summary.

## Tips for navigating minified code

- Variable names are mangled (e.g., `pt7`, `gt7`, `Bt7`). Follow references by searching for the mangled name.
- `X(()=>{...})` is a module initializer pattern — the code inside runs at startup.
- `async function*` generators are often streaming message handlers.
- When you find a function, search for where it's called to understand the control flow.
- The binary contains both the current code AND string literals from dependencies — filter noise by looking for contextually relevant neighbors.
- Use `-A` and `-B` flags with grep to get surrounding context.
- For very long matches, pipe through `fold -w 120` or use `less`.

## Dealing with large output

The strings file is ~380K lines. Grep results for broad terms can be huge. Strategies:
- Start narrow, broaden only if needed
- Use `grep -c` first to count matches before dumping content
- Chain greps: `grep "feature" file | grep "config"`
- Use `head -50` to preview before committing to reading everything
- Offload deep searches to subagents when exploring multiple threads
