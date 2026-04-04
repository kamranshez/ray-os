---
tags: [script, claude-chat, video-8]
status: draft
---

## Video 8 — Extended Thinking

**Goal**: Viewer understands what extended thinking is, when to use it, and sees the dramatic difference in output quality for complex tasks.

---

### HOOK (0:00–0:30)

> "When you ask Claude a hard question, normally it just fires off an answer immediately. But what if it could stop, think through the problem step by step, and THEN give you its answer? That's Extended Thinking. It's like telling Claude 'don't rush this — think carefully.' And the difference in quality is dramatic."

---

### SECTION 1: What is Extended Thinking? (0:30–2:30)

**On screen**: Claude with thinking block visible.

> "Extended thinking is a mode where Claude shows you its reasoning process before giving you an answer. Instead of jumping straight to a response, it creates a visible 'thinking block' where it considers different approaches, rejects bad ideas, and builds toward a solution."

**What you'll see**:
- A collapsible "Thinking..." section appears before the response
- Inside: Claude's reasoning chain — what it considered, what it rejected, how it arrived at its conclusion
- Then: the final answer, informed by that deeper reasoning

> "It's like the difference between someone blurting out the first thing that comes to mind versus someone pausing, thinking it through, and giving you a considered answer."

**Reference from competitors**: AI Master explains: "Extended thinking lets Claude pause before answering. It shows you its internal reasoning process in real time. You see it consider options, reject bad paths, and build solutions step by step."

---

### SECTION 2: How to Enable It (2:30–3:30)

**On screen**: Settings or chat interface.

- Extended thinking is available on Pro plans and above
- Available on all three models (Opus, Sonnet, Haiku)
- Toggle it on in the chat settings or it may activate automatically for complex queries

> "On the Pro plan, Claude sometimes uses extended thinking automatically when it detects a complex question. You can also explicitly ask for it: 'Think through this step by step before answering.'"

---

### SECTION 3: Demo — Without vs With (3:30–7:00)

**The power of this feature is in the comparison. Do the same complex prompt twice.**

**The prompt**:
```
I run a 5-person marketing agency doing $30K/month revenue. 
Growth has stalled for 3 months. 
Our clients are local restaurants and retail shops.
We charge $2K-5K/month per client.
We get most clients through referrals.

What's wrong and what should I change? Be specific.
```

**Without extended thinking** (regular mode):
- Show Claude giving a decent but generic answer
- Bullet points of standard advice: "diversify lead gen," "upsell existing clients," etc.
- > "Okay, that's fine. Generic consulting advice you could find in any blog post."

**With extended thinking** (enabled):
- Show the thinking block expanding
- Claude considers: revenue per client math, team capacity limits, referral ceiling, positioning issues
- Final answer is deeply specific: "Your referral channel has a ceiling because restaurants have small networks. Your pricing suggests you're doing too much custom work — standardize into 3 tiers. Your team of 5 can handle 8-10 clients max at current service levels, so you're near capacity..."
- > "Completely different depth. It did the math, identified the actual bottleneck, and gave specific recommendations. That thinking block is where the magic happened."

---

### SECTION 4: Best Use Cases (7:00–9:00)

**On screen**: Examples with results.

**Use case 1: Complex analysis**
```
[Enable extended thinking]
Analyze this business plan and identify the three biggest risks.
Be specific about why each risk matters and what I should do about it.
```
- Show Claude thinking through financial assumptions, market risks, team gaps
- > "It didn't just list generic risks. It found specific numbers that didn't add up."

**Use case 2: Decision making**
```
[Enable extended thinking]
I'm deciding between hiring a full-time content writer at $60K/year 
or using AI tools plus a part-time editor at $30K/year. 
My content needs: 3 blog posts/week, 2 newsletters/month, social media daily.
What are the real trade-offs? Don't give me a generic comparison — think through my specific situation.
```
- Show the thinking block considering output quality, consistency, scalability, hidden costs
- > "It considered things I hadn't thought of — like the ramp-up time for a new hire, the editing overhead with AI content, and the flexibility of the hybrid approach."

**Use case 3: Code review / debugging**
```
[Enable extended thinking]
Review this code and find any bugs, security issues, or performance problems.
[paste code]
```
- > "For code, extended thinking catches subtle issues that normal mode misses — race conditions, edge cases, security vulnerabilities."

---

### SECTION 5: When NOT to Use It (9:00–10:00)

> "Extended thinking uses more tokens and takes longer. Don't use it for everything."

**Don't use for**:
- Simple questions ("What's the capital of France?")
- Quick rewrites or formatting
- Brainstorming lists
- Casual conversation

**Do use for**:
- Complex analysis and strategy
- Important decisions with trade-offs
- Reviewing work before sending/publishing
- Debugging difficult problems
- Anything where accuracy really matters

> "The rule: if you'd want a human to 'think carefully about this before answering,' turn on extended thinking."

---

### SECTION 6: Reading the Thinking Block (10:00–11:00)

**On screen**: Expand a thinking block and walk through it.

> "The thinking block isn't just for Claude — it's for you. Reading it teaches you how Claude approaches problems."

Walk through a thinking block:
- Point out where Claude identifies the key issue
- Show where it considers and rejects an approach
- Show where it refines its reasoning
- > "If you see Claude going down a wrong path in the thinking block, you can interrupt and redirect. 'You're assuming X but actually Y' — and Claude will rethink."

**Reference from competitors**: AI Master: "Transparency. You're not blindly trusting Claude's output. You can correct a bad assumption and ask Claude to rerun the analysis."

---

### OUTRO (11:00–11:30)

> "Extended thinking turns Claude from a fast answer machine into a careful analyst. Use it when accuracy matters. In the next video, we're going to cover working with files and documents — uploading PDFs, spreadsheets, images, and getting Claude to analyze them."

---

### NOTES FOR FILMING

- The without vs with comparison is the hero demo — same prompt, dramatically different results
- Expand and scroll through a thinking block on screen so viewers see what's inside
- Keep the "when not to use" section brief — viewers want to USE the feature
- Target length: ~11 minutes
