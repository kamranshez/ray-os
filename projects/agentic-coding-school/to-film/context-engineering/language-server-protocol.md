---
duration: "5-9 min"
batch: 7
order: 4
batch_name: "Context Engineering"
class: "context-engineering"
chapter: "Advanced Techniques"
---

# Language Server Protocol

Use LSP-powered tools (like Serena/JetBrains MCP) instead of text-based search for code navigation. Semantic understanding beats grep.

## Example: Serena in AGENTS.md for Sub-Agents

Show how you can add LSP instructions to your `AGENTS.md` so sub-agents use semantic tools first:

**The anti-pattern:** Sub-agents defaulting to Grep/Glob/Read on Java/Kotlin files — wasteful and misses context.

**The fix:** Instruct sub-agents to start with semantic tools:
- `jet_brains_get_symbols_overview` — get file/class structure
- `jet_brains_find_symbol` — locate specific symbols by name path
- `jet_brains_find_referencing_symbols` — find where symbols are used
- `search_for_pattern` — search when exact names unknown

Only fall back to Grep/Read for non-code files or when Serena returns nothing.

**Wrong (wasteful):**
```
Grep pattern="class Composition"
Read file_path="src/main/java/songscribe/music/Composition.java"
```

**Right (efficient):**
```
jet_brains_get_symbols_overview(relative_path="src/.../Composition.java", depth=2)
jet_brains_find_symbol(name_path_pattern="Composition/isEmpty", include_body=true)
```

## Full Serena Rules File Example

Show this as an example of a `./rules/serena.md` that you link from your CLAUDE.md:

```markdown
## Serena Tool Usage (CRITICAL - READ THIS FIRST)

**MANDATORY: Always use Serena tools for Java/Kotlin code exploration and symbol renaming.**

### When to Use Serena Tools

**Finding usages/references:**
- DON'T: Grep for method/class names
- DO: jet_brains_find_referencing_symbols with the symbol's name path

**Exploring code structure:**
- DON'T: Read entire files to see what's in them
- DO: jet_brains_get_symbols_overview to see class/method structure first

**Reading specific symbols:**
- DON'T: Read whole file then scroll to find the method
- DO: jet_brains_find_symbol with include_body=true

**Renaming symbols:**
- DON'T: Use Edit tool to manually rename
- DO: mcp__serena__rename_symbol (handles all references automatically)

**Finding code when you don't know exact names:**
- DON'T: Grep for keywords as first step
- DO: search_for_pattern (semantic search across codebase)

### Standard Workflow Pattern

1. Overview → Get symbols in a file: jet_brains_get_symbols_overview
2. Find → Locate specific symbol: jet_brains_find_symbol
3. Read → Read body if needed: include_body=true
4. References → Understand usage: jet_brains_find_referencing_symbols
5. Edit → Modify code: Use Edit tool (provides visible diff)

### When NOT to Use Serena

- Reading non-code files (markdown, config files, etc.)
- Reading full file content when you need context around multiple symbols
- Editing code (use Edit tool so user can see the diff)
- Quick line-based edits
```

## References

- https://x.com/om_patel5/status/2030479131222192457
- https://x.com/jarredsumner/status/2030520041377271812

## Key Points
- LSP gives semantic understanding that text search can't match
- Add these instructions to your AGENTS.md so sub-agents inherit them
- Link out to detailed rules files (e.g. `./rules/serena.md`, `./rules/development.md`)
- Saves tokens and gives more complete results
- Always start with semantic tools, fall back to text tools only when necessary
