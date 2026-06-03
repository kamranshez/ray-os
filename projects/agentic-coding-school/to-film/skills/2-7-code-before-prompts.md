---
class: "skills"
chapter: "Your First Skill"
status: "new"
source: "Daniel Miessler — PAI Deep Dive (Dec 2025) + Building Your Own Unified AI Assistant"
---

## Code Before Prompts

The 80/20 rule: anything deterministic should be code, not prompts.

### The Problem

After building 10-15 skills, your audience will hit a consistency problem. "Why does my invoice skill sometimes round to 2 decimal places and sometimes to 3?" "Why does it format the date as March 31 sometimes and 03/31 other times?" "Why did it miscalculate the total?"

The answer: you're asking an AI to do things that code does perfectly every time. Math, date formatting, CSV parsing, API calls with exact parameters, file manipulation — these are deterministic operations. They have one correct answer. An AI will get them right 90% of the time. Code gets them right 100% of the time.

Miessler's principle: roughly 80% of what a skill does should be deterministic code. Reserve AI prompts only for the fuzzy, judgment-requiring parts — writing, summarizing, deciding, interpreting.

### The Architecture

Remember the skill folder structure from 2.3:

```
my-skill/
  skill.md        ← the orchestrator (process + judgment calls)
  references/     ← knowledge files
  scripts/        ← deterministic code ← THIS IS THE KEY
  assets/         ← templates, images
```

The `scripts/` folder is where deterministic operations live. The `skill.md` tells Claude WHEN to call each script and WHAT to do with the results. Claude handles the thinking. Scripts handle the doing.

### What to Show

**Before/After with the receipt scanner (from Ch 4.3):**

**Before (pure AI):**
- Skill reads a receipt image
- AI extracts line items, calculates subtotal, applies tax, generates total
- Works 90% of the time. Misreads one receipt. Rounds inconsistently. Occasionally hallucinates a line item.

**After (code + AI):**
- AI reads the receipt image and extracts line items into structured JSON (the fuzzy part — interpreting an image requires judgment)
- `scripts/calculate.py` handles all math: summing, tax calculation, rounding to 2 decimal places (the deterministic part)
- AI formats the final report using the calculated numbers
- 100% accurate on the numbers. AI only handles what AI is good at.

**The split in practice:**

| Task | Who does it | Why |
|---|---|---|
| Read a receipt image | AI | Requires visual interpretation |
| Sum line items | Script | Deterministic math |
| Calculate tax | Script | Deterministic math |
| Format a date consistently | Script | Deterministic formatting |
| Parse a CSV | Script | Deterministic parsing |
| Call an API with exact params | Script | Deterministic HTTP call |
| Write a summary | AI | Requires judgment and language |
| Decide severity rating | AI | Requires interpretation |
| Generate recommendations | AI | Requires creativity |

**Build it live:**
1. Show the current receipt scanner skill (pure markdown instructions)
2. Add a `scripts/calculate.py` — takes JSON line items, returns totals
3. Update skill.md to call the script: "After extracting line items, run `scripts/calculate.py` with the extracted data"
4. Run both versions on the same 5 receipts — show the consistency improvement

### CLI Tools as the Gold Standard (Miessler's Pattern)

Miessler takes this further: wrap your deterministic code in proper CLI tools with flags, help text, and documentation. Why? Because AI models perform dramatically better when calling well-documented CLI tools than when interpreting freeform instructions.

Instead of:
```
Run the Python script at scripts/calculate.py and pass it the line items
```

Build:
```
scripts/calculate --input items.json --tax-rate 0.08 --currency USD --round 2
```

The AI knows exactly what flags are available, what types they expect, and what the tool does. No ambiguity.

### The Second Payoff: Context Economy

Consistency is the obvious reason to prefer code. The less obvious one is tokens.

Every byte that passes through the model costs you twice. Once on the way in as input, and once on the way out if the model echoes or transforms it. A 50MB CSV piped through Claude to "sum column C" is a catastrophe. You're paying to stream raw data through a language model that's worse at addition than a three-line Python script.

The fix is the same fix. Move it to code, and let files do the remembering.

**The pattern:**
- Scripts read the big, messy input from disk.
- Scripts write their output to a file (like `summary.json`, `items.csv`, `report.md`).
- The skill.md instructs Claude to read *only* the distilled result.

The raw 50MB CSV never enters the context window. The 20-line summary does. Same work, a fraction of the tokens, and your context stays free for the judgment calls that actually need it.

**Where this matters most:**
- **Scraping and API pulls.** Fetch 200 pages, save to `data/raw/`, let AI read only the filtered subset it needs.
- **Log analysis.** Grep and aggregate in a script, hand the AI the 10 lines that matter, not the 10,000.
- **Multi-step pipelines.** Stage 1 writes `stage1.json`, stage 2 reads it. The AI never has to hold intermediate state in its head.
- **Long documents.** A script chunks and indexes. The AI reads only the relevant chunk.

**The rule of thumb.** If a step produces more than a few hundred lines of output, it should write to a file, not stream through the model. Skill.md points Claude to the path. Claude reads it on demand.

This is why `scripts/` is load-bearing. It's not just "code for math." It's the skill's working memory, the place where intermediate state lives so the context window doesn't have to hold it.

### Key Insight

> "Anything that can be done deterministically in code should be. Reserve AI for the fuzzy tasks that resist programmatic solutions." — Miessler

This is the maturity leap from "markdown instructions" to "production skill systems." Your skill.md becomes the orchestrator. It decides what to do and in what order. Scripts handle the execution where precision matters, and files handle the memory so the context window stays lean.

### Cross-Links

- [[2-3-anatomy-of-a-well-built-skill]] — the scripts/ folder in the anatomy, now explained
- [[5-1-evaluating-your-skills]] — inconsistent outputs are often a sign you need code, not better prompts
- [[4-3-the-operations-manager]] — receipt scanner, invoice generator — prime candidates for code+AI split
