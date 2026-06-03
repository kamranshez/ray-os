---
class: "skills"
chapter: "Quality Control"
status: "new"
source: "Daniel Miessler — AI WILL Replace Knowledge Workers (2026-03-22)"
---

## Business Metrics for Skills

Stop measuring skills in assertion pass rates. Start measuring them in dollars, hours, and consistency.

### The Problem

Ch 5.1 teaches you to evaluate skills with Skill Creator's benchmarking — assertion pass rates, token usage, time. That's the technical layer. But your audience is business people. They don't care about pass rates. They care about:

- How much does this cost me per execution vs the human alternative?
- How long does it take vs the human alternative?
- How consistent is the output? If I run it 10 times, do I get 10 similar results?
- What's the quality delta vs what my team currently produces?

Miessler: "Can I see all of my projects? Can I see all of the work that's being done? Do I have a list of workflows that show all the different processes, what the steps are, and how they're actually being performed? Do I know how much that costs? Do I know how long it takes?"

### What to Show

**Step 1 — Build a cost comparison sheet:**
Take any skill from the class (e.g., the content director from Ch 4.2).

| Metric | Human | Skill | Delta |
|---|---|---|---|
| Cost per execution | $150 (2hrs @ $75/hr) | $0.12 (tokens) | 99.9% reduction |
| Time per execution | 2 hours | 3 minutes | 97.5% reduction |
| Consistency (10 runs) | High variance | Near-identical | Measurably better |
| Quality (blind review) | Depends on the person | Depends on the skill | Test it |

**Step 2 — Run a consistency test:**
- Give the same input to a skill 5 times
- Compare outputs side by side — how similar are they?
- Do the same with 5 different humans (or simulate with different prompts with no skill) — show the variance
- Miessler's point: "If Sarah does it, the output is great. Jim looked at the same process, got the same training — his output is garbage." Skills eliminate the Sarah/Jim variance.

**Step 3 — The quality blind test:**
- Take a real deliverable your business produces (proposal, report, email sequence)
- Generate one with the skill, pull one from your archives (human-made)
- Have someone review both without knowing which is which
- Record the scores — this is your quality delta

**Step 4 — Build a metrics dashboard skill:**
- A meta-skill that tracks cost, time, and quality across all your other skills
- Every time a skill runs, it logs: tokens used, time elapsed, and a quality self-assessment
- Weekly rollup: "Your content director saved you 14 hours this week at an estimated cost savings of $1,050"

### The Vendor Test (Miessler)

"Now a vendor doesn't come with a steak dinner. We show them our metrics. This is how we do things. This is how much it costs us. This is how good it is. This is our quality ratings. What are your ratings? What are your cost numbers?"

When you have business metrics per skill, you can make data-driven decisions about:
- Which skills to invest more time improving
- Which manual processes to convert next (highest cost, lowest consistency = convert first)
- Whether a vendor's tool is actually better than what you've built

### Key Insight

Technical evals (Ch 5.1) tell you if the skill works. Business metrics tell you if the skill is worth it. For your audience — business owners, consultants, operators — the business metrics are what matter. And they're what you show clients when selling AI operating systems (Ch 7.2).

### Cross-Links

- [[5-1-evaluating-your-skills]] — the technical eval layer (assertions, benchmarks)
- [[6-4-companies-are-graphs-of-algorithms]] — each node in the company graph gets these metrics
- [[7-1-sharing-skills-with-your-team]] — business metrics help teams understand which skills to prioritize
