---
duration: "12-18 min"
batch: 2
order: 1
batch_name: "Advanced Workflows"
class: "claude-code"
chapter: "Advanced"
---

# Auto Research (Karpathy Loop)

## Video Arc (Beginner First)

### Act 1 — What Is Auto Research?

Auto research is a pattern where an AI agent improves something *for you* while you sleep. You point it at anything measurable — your website speed, your email open rate, your code quality — and it runs hundreds of experiments overnight, keeping only what works.

**The simple version**: imagine you hire someone who works 24/7, tries 1,000 different improvements to your thing, and only keeps the ones that actually made it better. That's auto research.

![[images/what-is-auto-research/excalidraw_1.png]]
![[images/what-is-auto-research/excalidraw_2.png]]
![[images/what-is-auto-research/excalidraw_3.png]]
![[images/what-is-auto-research/excalidraw_4.png]]
![[images/what-is-auto-research/excalidraw_5.png]]

### Act 2 — Before Auto Research (The Status Quo)

Before this, automated optimization meant **parameter tuning** — you give the system a list of knobs to turn (learning rate, batch size, font size, whatever), and it tries different combinations. Tools like Optuna, Ray Tune, and Bayesian optimization worked this way. You define a fixed search space upfront, and the tool samples combinations within it. The architecture, the code, the fundamental approach — all stays unchanged.

**Auto research flipped this**: instead of just turning knobs, the AI agent gets full read/write access to the actual code. It can redesign the architecture, rewrite how the optimizer works, add entirely new techniques, and fix bugs it spots along the way. That's the leap.

And honestly — **you've probably already been doing a version of this**. If you watched the Closing the Loop video, we talked about the autopilot pattern: run something, check the result, adjust, repeat. Auto research is that same loop, just formalized and fully autonomous. Karpathy gave it a name, a repo, and a structure — but the core idea of "measure, change, keep what works" is something you've already been applying.

![[images/before-auto-research/excalidraw_1.png]]
![[images/before-auto-research/excalidraw_2.png]]
![[images/before-auto-research/excalidraw_3.png]]
![[images/before-auto-research/excalidraw_4.png]]
![[images/before-auto-research/excalidraw_5.png]]

### Act 3 — How It Actually Works

Three things you need:

1. **Something to optimize** (a file: your code, your email template, your landing page)
2. **A metric** (a number that tells you if it got better: page speed, reply rate, conversion %)
3. **A fast feedback loop** (a way to test quickly: run a Lighthouse test, send a batch, run training)

The loop:
```
Read the code → Propose a change → Make the change → Test it → 
Better? → Git commit (keep it) 
Worse?  → Git revert (throw it away)
→ Repeat forever
```

The human writes a `program.md` file — plain English instructions telling the agent what it can modify, what it should optimize for, and what constraints to respect. The agent does the rest.

**The math**: if each experiment takes 5 minutes and 2% succeed, that's ~6 improvements per day. Each one compounds. 1.01^6 per day, 1.01^180 per month. Small wins, relentless compounding.

![[images/how-it-works/excalidraw_1.png]]
![[images/how-it-works/excalidraw_2.png]]
![[images/how-it-works/excalidraw_3.png]]
![[images/how-it-works/excalidraw_4.png]]
![[images/how-it-works/excalidraw_5.png]]

### Act 4 — Technical Use Cases

**ML training (the original)**: Karpathy pointed it at a small LLM training setup called nanochat. In ~2 days, the agent found ~20 validated improvements and caught a bug he'd missed for months. Shopify CEO Tobi Lütke used a variant overnight: trained a 0.8B parameter model that beat his previous hand-tuned 1.6B model — a model half the size outperforming the bigger one.

**Website performance**: Set it up with Google Lighthouse. The agent edits your HTML/CSS/JS, runs Lighthouse, keeps changes that lower load time. People got their LCP (largest contentful paint) dropping dramatically overnight.

**Code optimization**: Shopify used the pattern on their Liquid template engine — 53% faster parse+render time, 61% fewer object allocations.

![[images/technical-use-cases/excalidraw_1.png]]
![[images/technical-use-cases/excalidraw_2.png]]
![[images/technical-use-cases/excalidraw_3.png]]
![[images/technical-use-cases/excalidraw_4.png]]
![[images/technical-use-cases/excalidraw_5.png]]

### Act 5 — Non-Technical Use Cases (The Generalization)

People quickly realized the pattern works for *anything measurable*. The community generalized it beyond code within weeks:

**Cold email optimization** — one of the most popular non-ML applications. The agent edits your email subject lines, opening hooks, and offers. It generates variants, scores them (using heuristics or synthetic personas), and keeps winners. One description: "turned cold email from 'guess and hope' into a 700× experiment machine."

**Landing pages and marketing copy** — the agent edits headlines, layouts, offers, CTAs. It runs A/B-style tests or synthetic evaluations and keeps whatever lifts conversion.

**Skills and prompts** — huge category. People built auto-research loops that improve their AI prompts and skills. One user took a landing-page skill from 41% → 92% success rate in four rounds, zero manual tweaks.

**Other stuff people are running it on**: ad creative CTR, SEO copy, RAG retrieval accuracy, pricing experiments, YouTube thumbnails, newsletter subject lines.

![[images/non-technical-use-cases/excalidraw_1.png]]
![[images/non-technical-use-cases/excalidraw_2.png]]
![[images/non-technical-use-cases/excalidraw_3.png]]
![[images/non-technical-use-cases/excalidraw_4.png]]
![[images/non-technical-use-cases/excalidraw_5.png]]

### Act 6 — Why People Love It

1. **Removes the boredom bottleneck** — traditional optimization is 90% tedious iteration. Auto research hands the entire loop to the AI. You wake up to a git history full of validated wins
2. **Proof-of-concept for self-improvement** — the agent literally improves its own code based on past results. People call it the start of the "loopy era" of AI
3. **Pure fun** — watching the git log fill up with AI-discovered improvements overnight is addictive

![[images/why-people-love-it/excalidraw_1.png]]
![[images/why-people-love-it/excalidraw_2.png]]
![[images/why-people-love-it/excalidraw_3.png]]
![[images/why-people-love-it/excalidraw_4.png]]
![[images/why-people-love-it/excalidraw_5.png]]

## Next Videos (Demos)

This video is the conceptual foundation — what auto research is, why it matters, why it took off. The demos come in the follow-up videos:

1. **Technical demo**: Optimising code over time — setting up a real auto-research loop that improves actual code with a measurable metric
2. **Non-technical demo**: Optimising an approach over time — applying the same pattern to something like cold email, landing pages, or skill quality

## Connection to Existing Content

- **Closing the Loop** — we already covered the autopilot pattern there. Auto research is that same idea, formalized and fully autonomous
- **`/autoresearch` skill** — we already have this pattern built into the skills library. Viewers can use it immediately

## Suggested Class Placement

Claude Code — Advanced chapter. Cross-list in Business class since the non-technical applications are just as powerful.
