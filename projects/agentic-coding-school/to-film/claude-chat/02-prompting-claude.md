---
tags: [script, claude-chat, video-2]
status: draft
---

## Video 2 — Prompting Claude

**Goal**: Viewer learns how to write prompts that get dramatically better results — the structure, the techniques, and the common mistakes.

---

### HOOK (0:00–0:30)

> "Most people type one sentence into Claude and wonder why the answer is mediocre. The truth is: Claude's output is only as good as your input. In this video I'm going to show you the exact prompting structure that gets the best results — and it's been validated by the people who actually built Claude."

---

### SECTION 1: Why Prompting Matters (0:30–2:00)

**On screen**: Side-by-side comparison of a bad prompt vs good prompt.

**Bad prompt**:
```
Write me a marketing email
```

**Good prompt**:
```
I run a small SaaS company that sells project management software to freelancers. 
Write a marketing email announcing our new time-tracking feature. 
The tone should be casual and friendly — like a friend giving a heads up, not a corporation selling. 
Keep it under 200 words. Include a clear CTA to try the feature free for 14 days.
```

- Show both results side by side
- > "Same task. Completely different quality. The first one gave you a generic template. The second gave you something you could actually send."

---

### SECTION 2: The Prompt Structure (2:00–6:00)

**On screen**: The structure broken down visually.

> "Here's the structure I use for any important prompt. Five parts."

**Part 1: Set the stage (who you are)**
```
I'm a freelance copywriter who specializes in tech startups.
```
> "Tell Claude who you are. It changes how it writes, what assumptions it makes, and what level of detail it gives."

**Part 2: Define the task (what you want)**
```
Write a case study for my portfolio based on a recent client project.
```
> "Be specific about the deliverable. Not 'help me with marketing' — 'write a case study.'"

**Part 3: Specify the audience (who it's for)**
```
This is for potential clients visiting my website — startup founders who are non-technical.
```
> "The audience changes everything. Writing for investors is different from writing for customers."

**Part 4: Set the rules (constraints and format)**
```
Keep it under 500 words. Use short paragraphs. Include a results section with specific metrics.
No jargon. No buzzwords like 'synergy' or 'leverage'.
```
> "Rules prevent Claude from going off in a direction you don't want. Be explicit about format, length, tone, and things to avoid."

**Part 5: Ask it to ask you questions**
```
Before you start writing, ask me 3-5 questions to make sure you have enough context.
```
> "This is the single most powerful technique. Instead of Claude guessing, it asks you for the information it needs. The result is always better."

**Reference from competitors**: AI Edge presents this exact structure — "set the stage, define the task, specify the audience, set the rules, ask it to ask you questions" — and notes it was "vetted by people within Anthropic." AI Foundations emphasizes "the more context you give, the better Claude performs."

---

### SECTION 3: Live Demos (6:00–10:00)

**Demo 1: Business strategy**

Type:
```
I'm the founder of a 5-person marketing agency. We mostly serve local restaurants and retail shops. Revenue is about $30K/month but growth has stalled.

I want you to act as a strategic advisor. Before giving me advice, ask me questions to understand my situation better.
```

- Show Claude asking smart follow-up questions
- Answer 2-3 of them
- Show the tailored strategy it generates

> "See how different that is from 'give me business advice'? It asked about my pricing, my client acquisition channels, and my team capacity. The advice it gave was specific to MY situation."

**Demo 2: Content creation**

Type:
```
I write a weekly newsletter about AI tools for non-technical professionals. 
My readers are busy — they want to know what's new and why it matters in under 5 minutes.

Write this week's edition about Claude's new features. 
Use my style: casual, direct, slightly opinionated. No corporate speak.
Include 3 sections: what happened, why it matters, and one thing to try this week.
```

- Show the newsletter output
- > "It nailed the structure, the tone, and the length. That's because I told it exactly what I wanted."

**Demo 3: Quick question with context**

Type:
```
I'm comparing two project management tools for my team of 8. We're a remote design agency.
Our main needs: task tracking, time tracking, client-facing dashboards.
Budget: under $15/user/month.

Compare Asana and Monday.com for our specific use case. 
Be concise — bullet points, not essays.
```

- Show the structured comparison
- > "Specific question, specific context, specific format request. Clean result."

---

### SECTION 4: Power Techniques (10:00–12:30)

**On screen**: Technique name + demo for each.

**Technique 1: Role assignment**
```
You are a senior financial analyst at a Fortune 500 company. 
Analyze this quarterly report and flag the three biggest risks.
```
> "Giving Claude a role changes its depth and perspective. A 'financial analyst' gives different analysis than a 'general assistant.'"

**Technique 2: Few-shot examples**
```
Here are two examples of how I write tweet threads:

Example 1: [paste a tweet thread]
Example 2: [paste another]

Write a new thread about Claude AI in the same style.
```
> "Show Claude what 'good' looks like by giving it examples. It'll match the pattern."

**Technique 3: Chain of thought**
```
Think through this step by step before giving me your final answer.
What are the pros and cons of hiring a full-time developer vs using AI coding tools for a solo founder?
```
> "Asking Claude to think step by step gives you more thorough, reasoned answers."

**Technique 4: Iterate, don't restart**
```
That's good but make it more casual. 
Also, the second paragraph feels weak — can you punch it up?
```
> "Don't start over if the first response isn't perfect. Tell Claude what to fix. It's a conversation, not a one-shot."

**Reference from competitors**: AI Edge emphasizes "ask it to ask you questions" as the most important technique. AI Master covers extended thinking which we'll cover in its own video. AI Foundations demos iteration extensively.

---

### SECTION 5: Common Mistakes (12:30–13:30)

**On screen**: Mistake → Fix.

1. **Too vague** — "Help me with my business" → "Analyze my pricing strategy for my freelance design business targeting startups"
2. **No format specified** — Gets wall of text → "Use bullet points, keep it under 300 words"
3. **No audience** — Generic tone → "This is for my boss who's non-technical and time-pressed"
4. **Starting over instead of iterating** — Waste of context → "That's close but adjust X and Y"
5. **Not asking Claude to ask questions** — Guesswork → "Before answering, ask me 3 clarifying questions"

---

### OUTRO (13:30–14:00)

> "Good prompts are the foundation of everything else in this course. Projects, artifacts, research — they all work better when you know how to communicate clearly with Claude. In the next video, we're going to talk about Claude's three models — Opus, Sonnet, and Haiku — and when to use each one so you're not wasting credits or getting subpar results."

---

### NOTES FOR FILMING

- The side-by-side bad vs good prompt is the hook visual — make it dramatic
- Live demos should use relatable scenarios (not developer-heavy)
- The "ask it to ask you questions" technique deserves extra emphasis — it's the game-changer
- Target length: ~14 minutes
