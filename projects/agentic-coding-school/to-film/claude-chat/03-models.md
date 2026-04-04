---
tags: [script, claude-chat, video-3]
status: draft
---

## Video 3 — Models (Opus, Sonnet, Haiku)

**Goal**: Viewer knows exactly which model to use for which task — stop overpaying for simple tasks and stop under-powering important ones.

---

### HOOK (0:00–0:30)

> "Claude has three models and most people either use the wrong one or don't even know they have options. Opus is the brain. Sonnet is the all-rounder. Haiku is the speed demon. Picking wrong means you're either burning credits on a simple question or getting mediocre results on something important. Let me show you exactly which to use when."

---

### SECTION 1: The Three Models (0:30–3:30)

**On screen**: Three columns with model names.

**Opus 4.6 — The Smartest**
- Most capable model Anthropic has
- Best at complex reasoning, nuanced writing, catching subtle errors
- Slowest of the three
- Uses the most credits
- > "Opus is your senior advisor. When accuracy matters and you can't afford mistakes — legal analysis, financial review, important strategy decisions — this is your model."

**Sonnet 4.6 — The All-Rounder**
- Nearly as smart as Opus on most tasks
- Significantly faster
- Uses fewer credits
- 1 million token context window (beta)
- > "Sonnet is your daily driver. For 80% of tasks — writing, research, analysis, brainstorming — Sonnet is the move. It's fast, smart, and cost-efficient."

**Haiku 4.5 — The Speed Demon**
- Fastest model
- Cheapest by far
- Good enough for straightforward tasks
- Can lose track in long conversations
- > "Haiku is your quick-answer machine. Simple questions, rapid prototyping, high-volume tasks where speed matters more than depth."

**Reference from competitors**: AI Master provides benchmark scores — Opus 80.9% on SWE-bench, Sonnet 77.2%, Haiku 73.3%. AI Edge recommends "default to Sonnet for chatting, use Opus for advanced strategic tasks." Both emphasize splitting usage across models.

---

### SECTION 2: How to Switch Models (3:30–4:30)

**On screen**: Claude interface showing model selector.

**Step 1**: Click the model selector (bottom of chat or top bar)
**Step 2**: Choose your model
**Step 3**: Start chatting

> "You can switch models mid-conversation too. Start a brainstorm with Sonnet, then switch to Opus when you need deeper analysis on a specific point."

**Note**: Free plan only gets Sonnet and Haiku. Opus requires Pro or above.

---

### SECTION 3: Live Comparison — Same Prompt, Three Models (4:30–9:00)

**On screen**: Three conversations side by side (or sequential with clear labels).

**The prompt** (same for all three):
```
I'm launching an online course about AI productivity tools. My target audience is non-technical professionals aged 25-45. 

Give me a go-to-market strategy with specific channels, content ideas, and a 90-day timeline.
```

**Run on Haiku first**:
- Show the speed (almost instant)
- Show the result — decent but surface-level
- > "Fast. Functional. But notice it's fairly generic — it gives you a list but doesn't go deep on any point."

**Run on Sonnet**:
- Show it's a bit slower
- Show the result — more detailed, better structured, more specific recommendations
- > "Noticeably better. It considers your specific audience, suggests specific platforms, and the timeline has actual milestones."

**Run on Opus**:
- Show it takes the longest
- Show the result — most nuanced, considers edge cases, includes strategic reasoning
- > "Opus went deeper. It flagged risks, suggested testing strategies, and the reasoning behind each recommendation is visible. This is the kind of thinking you'd pay a consultant for."

**The takeaway**:
> "For a quick brainstorm, Haiku is fine. For planning, Sonnet is perfect. For high-stakes strategy where you need the best thinking, Opus is worth the extra credits."

---

### SECTION 4: When to Use Each Model (9:00–11:00)

**On screen**: Decision table.

| Task | Model | Why |
|------|-------|-----|
| Quick questions | Haiku | Speed, low cost |
| Rewriting a paragraph | Sonnet | Good enough, fast |
| Writing a full article | Sonnet | Maintains voice, handles length |
| Analyzing a contract | Opus | Catches subtle issues |
| Brainstorming ideas | Sonnet | Fast, creative enough |
| Final review of important work | Opus | Highest accuracy |
| Summarizing meeting notes | Haiku | Straightforward task |
| Building a strategy | Opus | Deepest reasoning |
| Coding a simple script | Sonnet | Best code model |
| Debugging complex code | Opus | Catches edge cases |

**The rule of thumb**:
> "Ask yourself: how much does accuracy matter for this task? Low stakes → Haiku. Medium stakes → Sonnet. High stakes → Opus."

---

### SECTION 5: Credit Management (11:00–12:30)

**On screen**: Usage considerations.

> "Here's the practical side. Each model costs different amounts of credits."

- Opus uses roughly 5x what Haiku uses for the same conversation
- Sonnet is in the middle — about 3x Haiku
- On the Pro plan ($20/month), you get 5x free-tier usage
- If you use Opus for everything, you'll hit limits faster

**Strategy**:
> "Here's what I do. Sonnet is my default for everything. I only switch to Opus for three things: final reviews of important work, complex strategy sessions, and anything where I need Claude to catch mistakes. For quick lookups and simple tasks, I switch to Haiku. This way I rarely hit rate limits even on Pro."

**Reference from competitors**: AI Edge: "for any chatting, use Sonnet. For anything more advanced where you want a real strategic thinker, use Opus." AI Master: "if you can't afford to upgrade, split your usage between Sonnet and Opus."

---

### OUTRO (12:30–13:00)

> "Now you know the three models and when to use each one. In the next video, I'm going to show you Claude's web search and deep research features — how to get Claude to find real-time information and generate thorough research reports."

---

### NOTES FOR FILMING

- The live comparison is the centerpiece — show all three results clearly
- The decision table should be on screen long enough to screenshot
- Keep it practical, not benchmark-heavy (save benchmarks for a blog post)
- Target length: ~13 minutes
