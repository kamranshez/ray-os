---
duration: "12-18 min"
batch: 1
order: 4
batch_name: "Seed Thinking"
class: "prompt-engineering"
chapter: "Scaling Taste"
---
### The Model as Compressed Humanity

A model like Claude is roughly 100 million people compressed into a single system. Every prompt you give it produces a consensus answer — the weighted average of how all those people would respond.

Ask "what's the best business to start in 2026" and you get the same 50 ideas everyone else gets. That's not because the model lacks creativity — it's because your prompt activated the most crowded region of the latent space. Millions of people asked similar things, so you get the statistical center of mass.

But here's what most people miss: there is a version of *you* inside that model. Not literally — but a cluster of archetypes that, when activated correctly, produces outputs that are 95% aligned with your taste, judgment, and decision-making style. The question is how to invoke it.

### From the Call: The Ray Simulator

I recently answered over 500 specification questions while planning software. After reviewing my answers, I realized Claude had enough signal to model my decision-making. So I set up two subagents:

1. **Spec Writer** — asks the same planning questions it would ask me
2. **Ray Simulator** — trained on my 500+ previous answers, responds as I would

The result was 97% aligned with what I would have said. Not because Claude read my mind, but because within those 100 million compressed humans, there's a cluster that maps closely to how I think in that domain. My answers were the coordinates that located it.

This is the same principle as steering distributions, but applied to *identity* rather than *task focus*. Your data is the seed that collapses the model's identity distribution from "average of everyone" to "someone who thinks like you."

### What Counts as "Your Data"

Anything that captures how you think, decide, and express:

- **Past AI conversations** — every chat where you corrected Claude, chose option A over B, or refined an output is a training signal about your preferences
- **Emails and writing** — your natural voice, sentence structure, what you emphasize, what you skip
- **Decision logs** — which PRs you approved vs. rejected, which features you prioritized, which designs you chose
- **Feedback patterns** — the corrections you repeatedly make ("too formal," "simpler," "I'd never say that")
- **Domain expertise expressed naturally** — dictated thoughts, voice memos, meeting transcripts

The key insight: this data is valuable to AI companies for training. It's *equally valuable to you* for steering. You are sitting on a personal dataset that, when compressed into a Claude skill or subagent prompt, can activate the version of the model that thinks like you.
### Compressing Yourself into a Skill

Once you have enough data, you compress it. This is what Claude skills and CLAUDE.md memories are for — they're not just instructions, they're identity activation seeds.

A well-built skill derived from your data does three things:

1. **Collapses the identity distribution** — moves the model from consensus-you to actual-you
2. **Persists across conversations** — you don't re-explain yourself every time
3. **Scales to new domains** — the taste that guided your software decisions can guide your writing, content, code review, hiring — any domain where judgment matters

The 500 spec answers I gave weren't about software specifically. They revealed *how I make tradeoffs* — simplicity vs. completeness, speed vs. correctness, risk tolerance. That reasoning pattern transfers.


### The 95/5 Split

Once you've activated the right region of the model, something changes in your workflow. Instead of:

- Reviewing every output carefully (100% of your attention)
- Iterating back and forth to fix tone, judgment, priorities

You get:

- Outputs that are 95% right on the first pass
- A quick glance to fill the remaining 5% — the truly human part that no model captures

This is what "scaling taste" means. You're not delegating thinking. You're compressing your taste into a seed, letting it activate at scale across dozens of tasks, and then applying the irreducible human judgment only where it matters.

### Why You Should Save Everything

Your data's value compounds over time and across model generations:

- **Chat histories** — save every conversation with every model. Each one contains corrections, preferences, and decisions that define your taste
- **Emails, texts, documents** — your natural communication style is training data for your own identity activation
- **Meeting transcripts, voice memos** — especially valuable because they capture how you think out loud, before you edit yourself
- **Decision records** — what you chose, what you rejected, why

Even if this data isn't useful with current models, future models will extract more signal from it. Pre-AI writing is becoming like pre-nuclear steel — increasingly rare and valuable as the internet fills with AI-generated content. Your authentic human output is an appreciating asset.

The same way Anthropic bought book collections to secure clean training data, you should be collecting your own clean data — not for them, but for yourself.

### The Feedback Loop

This connects to the self-improving systems we discussed: when you have Claude running scheduled tasks (daily analytics, content analysis, landing page optimization), each run generates data about what worked and what didn't. That data feeds back into the system's understanding of your taste.

The loop:
1. **Compress** your taste into a skill/prompt from historical data
2. **Deploy** it across automated workflows (content, code review, analytics)
3. **Observe** outputs and make the 5% corrections
4. **Those corrections become new data** that further refines the taste model
5. Repeat — the system gets 1% better every day

This is why the "just show up and talk" workflow works. You dictate for 10 minutes. Claude repurposes into email, LinkedIn, podcast script. You glance at each, make small corrections. Those corrections are data. Tomorrow's outputs are marginally better. Over 90 days, the gap between Claude's output and your actual voice narrows continuously.

![[taste-feedback-loop-five-step-process.png]]
### Demo

1. Show a Claude skill built from real writing samples and past decisions
2. Give the same task to default Claude vs. taste-activated Claude — compare outputs
3. Show the 95/5 in practice: taste-activated output needs only minor tweaks
4. Show how corrections feed back into the skill for next time

### Key Insight

> A model contains a version of you — an archetype cluster that, when activated by your data, produces outputs aligned with your taste. The prompt engineering skill isn't just *what* to ask or *how* to frame it — it's building the seed that makes the model *think like you*, so you can scale your judgment across every domain you touch. Your data is the activation key.

### Multiple Archetypes of You

A single compressed identity is powerful, but you don't have one mode of thinking — you have many. Your product sense is different from your design sense, which is different from your writing voice, which is different from how you evaluate code.

Each of these is a separate archetype that can be compressed into its own subagent:

- **Product-You** — trained on your feature prioritization decisions, tradeoff calls, user feedback responses
- **Writer-You** — trained on your pre-AI writing, dictations, email voice
- **Code-Reviewer-You** — trained on your PR comments, what you flag vs. approve, your standards
- **Design-You** — trained on screenshots you saved, UI decisions you made, what you called ugly vs. clean

Your main Claude instance becomes the orchestrator. It doesn't try to be all of you at once — it delegates to the right archetype depending on the task. When reviewing a feature spec, it consults Product-You. When drafting a newsletter, it hands off to Writer-You. Each subagent activates a different region of the model's identity space, and together they cover the full surface area of your judgment.

This is how you go from one person making one decision at a time to your taste applied across ten domains simultaneously — with a quick glance to fill the last 5% on each.

![[claude-orchestrator-delegating-to-archetype-subagents.png]]
