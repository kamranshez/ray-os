---
duration: "10-15 min"
order: 11
class: "skills"
chapter: "Make It Yours"
status: "adapt"
adapts: "encoding-your-expertise-into-skills"
tags: [course, script, skills]
lesson: "3.3 Encoding Your Expertise"
---

## Encoding Your Expertise

So far in this chapter we've added brand context and refactored marketplace skills. Both of those make skills better. But this video is about something different. This is about encoding the thing that actually makes you valuable — your judgment.

Zack Shapiro, a lawyer who's been building skills for legal work, put it this way: "A template library is not a competitive advantage. Every competent firm in your practice area has roughly the same templates. The thing that differentiates a great lawyer from a mediocre one was never the template. It was what the lawyer did with the template."

Your judgment. Your criteria. Your way of spotting the thing everyone else misses. That's what we're encoding today.

### The Generic Prompt Problem (0:00–2:00)

Here's what most people do. They open Claude and type something like "review this contract." And Claude gives them... a review. It reads the contract, summarizes the key points, maybe flags a couple things that sound risky. It's not wrong. But it's surface-level.

> [SCREEN: Claude terminal]

> [TYPE: "Review this contract" — with a sample services agreement attached]

> [SHOW: the output — generic summary, broad observations, nothing actionable]

It reads like a first-year analyst's work. "The liability section could be more specific." "Consider reviewing the termination clause." Okay — but what specifically is wrong? What should I push back on? What's missing entirely? What's the verdict — do I sign this or not?

And here's the thing Zack Shapiro says about this: "Most people who try AI write something like 'review this contract' and get back something mediocre. Then they decide AI isn't useful. The problem is not the AI. The problem is the input."

The input was three words. You gave Claude no framework, no criteria, no sense of what you specifically look for. Of course the output is generic.

Now compare that to what a skill with encoded expertise produces.

### The Encoded Version (2:00–3:30)

Here's what the same task looks like with a contract review skill built from an expert's judgment.

> [TYPE: "Review this contract" — same contract, but with the skill active]

> [SHOW: the output — severity-rated flags, missing terms, counter-language, verdict]

Completely different. The skill told Claude: review from the vendor's perspective. Flag provisions where the customer shifted risk beyond market norms. Check for limitation of liability, IP ownership, data handling, termination for convenience. Produce a severity-rated summary — red flags, yellow flags, missing terms. Give a bottom-line verdict. And for every high-severity issue, suggest specific counter-language.

> [SPLIT: left — generic review | right — encoded review]

Left side — "consider reviewing the liability section." Right side — "Red flag: Section 8.2 caps vendor liability at fees paid in the last 12 months, but excludes IP indemnification from the cap. This means unlimited exposure on IP claims. Counter-language: 'Liability for IP indemnification claims shall not exceed two times the aggregate fees paid under this Agreement.'"

That's not Claude being smarter on the right. It's Claude following an expert's analytical framework instead of improvising.

### Building It Live (3:30–8:00)

Now I'm going to build this. And the reason I want to do this live is because the pattern works for any profession. Contract review for lawyers. Proposal evaluation for consultants. Financial analysis for accountants. Client briefs for agencies. The structure is the same — you're encoding your criteria, your priorities, and your judgment into a file.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build a contract review skill. It should review services agreements from the vendor's perspective. I want it to check for specific provisions and produce a severity-rated output."]

Skill Creator asks me questions. And this is where the expertise comes in — my answers are what make this skill mine instead of generic.

> [SHOW: Skill Creator's questions and the answers]

"What provisions should it always check for?" — Limitation of liability, IP ownership and assignment, data handling obligations, termination rights, indemnification scope, payment terms.

"How should it rate severity?" — Red flag means immediate risk that could harm the business. Yellow flag means worth reviewing but not a dealbreaker. Green means standard or favorable.

"What should the output include?" — A one-paragraph executive summary. A section-by-section breakdown with severity ratings. A missing terms section — things that should be in the contract but aren't. A bottom-line verdict: sign, negotiate, or walk. And for every red flag, specific counter-language I could propose.

"What's the perspective?" — Always from the vendor's side. Assume we're the one providing services. Flag anything where the customer shifted risk beyond what's standard.

Those answers took about five minutes. But they encode years of pattern recognition. Every contract I've reviewed, every negotiation I've been part of, every clause that's burned me — it's all compressed into those answers.

> [SHOW: the generated skill — skill.md with the review process, references/ with the checklist criteria]

And Skill Creator built the skill. Skill.md has the process — read the contract, identify the agreement type, apply the checklist, rate each finding, produce the output. The detailed checklist lives in `references/review-criteria.md`. Clean split.

Now let me test it on a real contract.

> [TYPE: "Review this contract" — different contract than before]

> [SHOW: the output — full severity-rated review with counter-language]

Red flags with specific clause references and counter-language. Yellow flags with context on why they matter but aren't critical. Missing terms identified — no termination for convenience clause, no cap on IP indemnification. Bottom line: negotiate, don't sign as-is, here are the three things to fix first.

That's the output of a skill that has professional judgment encoded. Not just "review this" — but "review this the way I would, checking the things I check, with the priorities I have."

### The Expertise Advantage (8:00–9:30)

And here's the insight that I think is the most important idea in this entire class. Zack Shapiro again: "Experienced practitioners have an enormous advantage in this new world, and most of them don't realize it. If you've spent 10 or 20 years developing judgment in your practice area, you are sitting on exactly the asset that AI makes more valuable, not less."

Think about that. If you're a consultant with 15 years of experience, you have judgment that's worth more now than it was a year ago. Because now you can encode it. You can turn it into a skill that runs in seconds and produces output that reflects your 15 years of pattern recognition.

A junior person using Claude without skills gets generic output. A senior person who encodes their expertise gets output that operates at their level. The experience gap doesn't shrink with AI — it amplifies. The senior person's skill IS the advantage.

And this applies to every profession. Marketers encoding their campaign evaluation criteria. Project managers encoding their risk assessment framework. Accountants encoding their audit checklist. Anyone with domain expertise can do this.

### The Gotchas Section (9:30–11:00)

One practical thing before we move on. After you build an expertise skill and use it a few times, you'll notice things Claude gets wrong. Maybe it flags something as red that should be yellow. Maybe it misses a specific type of clause. Maybe the counter-language is too aggressive for your style.

Every time that happens, add it to a gotchas section in the skill.md.

> [SCREEN: adding to the skill.md]

```markdown
## Gotchas
- Non-compete clauses in service agreements are usually unenforceable
  for vendors — flag as yellow, not red.
- Counter-language for liability caps should reference "aggregate fees"
  not "monthly fees" — clients will try to argue the lower number.
- If the contract is under $50K, skip the detailed IP ownership analysis.
  Not worth the negotiation cost.
```

These are the things that take humans months of experience to learn. Every gotcha you add makes the skill more like you and less like generic Claude. This is Anthropic's own advice — they say the gotchas section is the highest-signal part of any skill. Not the instructions. Not the examples. The gotchas.

### What's Next

That wraps up Chapter 3 — Make It Yours. Your skills now have your brand context, they're properly structured, and the most important ones encode your actual professional judgment.

In Chapter 4, we're going to put these skills to work. We're building AI employees — starting with a morning briefing that pulls from your email, calendar, and Slack, and runs every day before you wake up.
