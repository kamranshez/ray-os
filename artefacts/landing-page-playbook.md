---
tags: [strategy, landing-page, agentic-coding-school]
date: 2026-04-04
---

## The Course Landing Page Playbook

Distilled from 22 badass.dev interviews + Matt Pocock's AIHero launch page + the Agentic Coding School codebase. This covers general principles for any course landing page, then specific improvements for the Master Claude Code page.

---

## Part 1: General Principles (From the Research)

### 1. Pain-Dream-Fix Structure

The single most repeated insight across all 22 badass.dev interviews. Brennan Dunn built his own platform specifically because every hosted course platform defaults to: title → description → lesson list. He calls this "feature-first" and says it doesn't convert.

**What converts (Amy Hoy's structure):**

1. **Pain** — What's frustrating about not having this skill right now?
2. **Dream** — What does life look like once you have it?
3. **Fix** — Here's how the course gets you there.

The curriculum list is confirmation for people who are already interested, not the hook that creates interest. It belongs in the middle or bottom of the page.

**Matt Pocock's AIHero page is a masterclass at this.** His entire above-the-fold section is pure pain and dream — "AI can be both overhyped and powerful," "A tool like Claude Code can be your best friend, or the worst teammate you've ever had." The curriculum doesn't appear until you've scrolled through several screens of transformation narrative. By the time you see the lesson list, you already want it.

### 2. The Visitor Buys a Transformation, Not a Course

Joel Hooks repeats this in almost every interview: "Nobody wakes up and thinks 'I'm going to take a course today.' They're trying to make a difference in their lives."

**The before/after table is the most powerful conversion element.** Matt Pocock's page has:

| Before: Vibe Coder | After: AI Hero |
|---|---|
| YOLO mode | Sandboxing and Permissions |
| Huge ball of mud | Easy-to-navigate codebase |
| Hundreds of crap tests | Useful tests at sensible boundaries |
| Losing "sense" of the code | Design the structure, let AI own implementation |

This is dramatically more compelling than a feature list because it names the reader's current state (which they recognize) and shows them the specific transformation.

### 3. The Instructor Is the Product

Every successful course creator in the badass.dev interviews is visibly the product. Marie Poulin says "how does that teacher show up energetically" is a key buying factor. Brennan Dunn emphasizes the personalized relationship. Matt Pocock's AIHero page is literally written in first person, telling his personal story of building a course creator tool with Claude Code.

The instructor section should appear early — not buried in the FAQ. Cold visitors need to know who's teaching them and why this person is qualified. A photo, a sentence about expertise, and a credibility signal (YouTube subscriber count, years of experience, notable projects) is enough.

### 4. Social Proof Hierarchy

From the interviews, the most effective social proof types in order:

1. **Outcome stories** — "I got a $50K raise" (Shift Nudge student), "4,000 people bought in 24 hours" (Epic React). Specific, measurable results from real students.
2. **Authority quotes** — CEO quotes, industry leaders validating the skill. Best when they tie directly to the pain (hiring filter, career value).
3. **Company logos** — "People at these companies are learning here." Good for "people like me" signal.
4. **Recency signals** — "Updated 23 hours ago", "22 updates in 2 weeks." These answer the staleness objection, which Joel Hooks says is the #1 concern in tech education.
5. **Join velocity** — "47 people joined this week" or live notifications of recent purchases. Creates social momentum.

**What most course pages miss: student transformation testimonials.** Authority quotes (Karpathy, CEOs) validate the space. Student testimonials validate the course. You need both.

### 5. Progressive Disclosure for Curriculum

Josh Kaufman's insight: beyond ~20 modules, the full curriculum list overwhelms. "The learner logs in, and they are very overwhelmed by what they see."

**The pattern that works:**

- Show section titles with durations (high-level structure)
- Show 3-5 "highlight" lessons per section that sound most exciting
- Collapse the rest behind "See all X lessons →"
- Call out unique differentiators prominently (interactive exercises, AI-guided learning path, etc.)

Matt Pocock's AIHero page shows only 8 top-level sections with expandable subsections. You see the structure without drowning in 213 line items.

### 6. Price Anchoring Against Value, Not Other Courses

**The corporate card threshold:** Matt Pocock priced at $490 to stay under $500 (no manager approval needed). This is a real conversion cliff for B2B.

**Effective anchors:**
- Time saved: "50 hours of trial-and-error vs 10 hours structured"
- Salary impact: "If one technique saves 2 hours/week, that's $5K/year at $50/hr"
- Consultant rate: "A single hour with a Claude Code expert costs $300-500"

**The three-tier pattern (Brennan Dunn / Dell Keon):** Low / Target / Premium. The low tier makes the target look like a bargain. The premium makes the target feel reasonable. The premium should be a real option people actually buy (team plans), not a joke option (university comparison).

### 7. Email Capture for Non-Buyers

This is the single biggest gap on most course pages. Everyone who visits and doesn't buy is lost forever. Every creator in the badass.dev interviews built their business on the email list.

**Options:**
- Free mini-lesson gated behind email (Total TypeScript: first problem free, first solution requires email)
- "Get notified when new lessons drop" signup
- Newsletter signup ("Weekly Claude Code tips from Ray")
- Free chapter preview

Matt Pocock's email list was the #1 driver for his $730K launch. Marie Poulin's YouTube drove 80% of course buyers, but only because YouTube drove email signups which drove purchases.

### 8. Urgency Without Manipulation

The page needs a reason to buy today vs. next month. Authentic options:
- "Price increases at [X] students" (if true)
- "Current price locked for early members" (if planning a raise)
- Live join notifications (you have this — "Agentic engineer from USA joined 2 days ago")
- Recency stats showing rapid updates (you have this — strong)

Matt Pocock used pre-release pricing with a deadline as authentic urgency. Cohort-based courses (like his AIHero) have natural urgency built in — the cohort starts on a date.

---

## Part 2: What Matt Pocock's AIHero Page Does Differently (and Why It Worked)

AIHero launched a $795 cohort course. Key structural differences from a typical self-paced course page:

### Narrative-first, not feature-first

The page reads like an essay, not a brochure. Matt tells a personal story: he built a course creator tool using Claude Code. He shares real numbers (1,000 commits, 500 issues). He names specific features he built (in-browser video editor, AI writing assistant). This is concrete proof he practices what he teaches.

**The page flows:** problem → two common errors (delegate everything / delegate nothing) → the "engineer's path" as the solution → engineering skills breakdown → his personal story → course contents → pricing.

You never feel like you're being sold to. You feel like you're being convinced by someone who clearly knows what they're talking about.

### Identity framing: "Real Engineer" vs "Vibe Coder"

The entire page is organized around an identity transformation. You're either a "Vibe Coder" (bad) or an "AI Hero" (good). This is the same technique as your "Become the Claude Code Person" section — but Pocock extends it across the entire page rather than confining it to one section.

The before/after table is the centerpiece. It maps specific bad behaviors to specific good outcomes. It doesn't say "learn Claude Code" — it says "stop losing sense of your code and start designing structure while AI owns implementation."

### Skills framing over feature listing

Instead of listing Claude Code features (subagents, MCP servers, hooks), Pocock lists engineering skills:
- Communicating
- Anticipating
- Planning
- Decomposing
- Delegating
- Systematizing
- Parallelizing

This is powerful because it positions the course as making you a better engineer, not just a better Claude Code user. The tool changes; the skills don't.

### Cohort structure creates urgency + premium pricing

$795 for a 2-week cohort with live office hours. The cohort start date (March 30) is natural urgency. The live access justifies the premium price. The "yours to keep forever" promise removes risk.

Compare: your $199/yr or $294 lifetime for 213 self-paced lessons is a dramatically different value proposition. Neither is wrong — they serve different buyers. But the cohort model commands 4x the price for 1/10th the content because of the live access and deadline.

### Detailed schedule builds confidence

The AIHero page shows exactly what happens each day:
- Pre-course: Getting to Know Claude Code
- Day 1: Fundamentals
- Day 2: Steering
- Day 3: Planning
- Day 4: Feedback Loops
- Day 5: Ralph
- Day 6: Human in the Loop Patterns

This is much more scannable than 213 lesson titles. Each day has a clear theme and promise. A visitor can immediately assess "do I need this?" without reading every line item.

---

## Part 3: Specific Improvements for the Master Claude Code Page

Based on the codebase (`apps/nextjs/src/components/landing/sections/`), here's what exists, what's missing, and what to change.

### Current page structure (from code):

```
Hero → LogoMarquee → Stakes → BecomeClaudeCodePerson → Contents → WhyThisBeats → AlwaysCurrent → PricingCards → Guarantee → FAQ → FinalCTA
```

### What's working well

- **Stakes section** is strong — the Josh Miller hiring filter quote + evidence points. This is good pain.
- **BecomeClaudeCodePerson** is strong identity framing. "Every team has one. After this class, it's you."
- **AlwaysCurrent** with recency stats (updated 23 hours ago, 22 updates in 2 weeks) is a genuine differentiator.
- **WhyThisBeats** comparison (alone vs. this class) is effective.
- **SocialProofNotification** (live join events) adds momentum.
- **Video in hero** that shows CTA after completion is a nice touch.

### What to add

**1. Student transformation testimonials (new section)**

Add between BecomeClaudeCodePerson and Contents. This is the single biggest missing element. You have 3,151 students — even 4-5 short quotes would massively improve conversion:

- "I was Googling every command. Now my team asks ME." — [Name, Role, Company]
- "Built an internal tool in 2 days that would have taken 2 weeks before." — [Name, Role]
- "Got promoted to lead after automating our team's PR workflow." — [Name, Role]

Matt D. Smith kept a testimonial library at shiftnudge.com/reviews. Marie Poulin's 6-week check-in email ("What's a win you had?") is a testimonial machine.

**2. "Who teaches this?" section (before or after Stakes)**

Currently hidden inside a collapsed FAQ item. Cold visitors need to see Ray's face, a 1-sentence bio, and a credibility signal early. Matt Pocock's AIHero page is entirely built around his personal story and authority. You don't need that much, but a photo + "206 videos, 6 live classes, used by engineers at GitHub, Meta, and McKinsey" would add trust.

**3. Email capture for non-buyers (above Footer or as exit intent)**

Currently zero email capture. Every visitor who doesn't buy is gone. Options:
- "Get a free Claude Code cheat sheet" → email gate
- "Weekly Claude Code tips from Ray" → newsletter signup
- "Watch a free lesson" → email gate after first video

This is the #1 revenue-generating change from the badass.dev research. Matt Pocock's email list was the foundation for $730K in revenue.

**4. Before/After table (like Pocock's Vibe Coder → AI Hero)**

Your BecomeClaudeCodePerson section describes the "after" state but doesn't name the "before." Adding a two-column contrast like:

| Without this class | After this class |
|---|---|
| Copying prompts from Reddit | Building custom skills the team adopts |
| Hitting context limits constantly | Managing 1M tokens across subagent teams |
| Confused by MCP setup | Connecting Claude to Chrome, Slack, databases |
| Starting over after every /clear | Persisting memory across sessions |

This is more specific and actionable than the current "Why This Beats" section, which compares against the abstract concept of "figuring it out alone."

### What to change

**5. Make the MCP "what to watch next" feature a headline**

Currently buried as bullet point 5 of 6 in WhyThisBeats: "MCP server included: Claude tells you what to watch next." No other course has an AI that personalizes your learning path inside the product. This is a headline-worthy differentiator.

Consider a dedicated mini-section: "Not sure where to start? Claude tells you." Show a screenshot or animation of the MCP server recommending lessons. This is the single most unique feature of the product.

**6. Replace the university price anchor with something real**

The "Traditional University ~$26,000/year" card at 75% opacity signals it's not a real option. Nobody is choosing between your course and a university degree. More effective anchors:

Option A: Replace with a "Team 5-pack" card at $999 — a real product that also makes the individual lifetime look cheap.

Option B: Replace with a "Time Saved" calculation. "If this course saves you 2 hours/week for a year, that's $5,200 at a $50/hr rate. You paid $294."

Option C: Replace with a "Consultant" anchor. "A 1-hour Claude Code consulting session costs $300-500. This is 10+ hours for $199/yr."

**7. Curriculum section: progressive disclosure**

The Contents section currently lists all 213 lessons across 6 classes. This is comprehensive but overwhelming (Josh Kaufman's insight: beyond ~20 modules, learners glaze over).

Consider:
- Show the 6 class titles with durations and a 1-line description (current)
- Show only the top 5 "most exciting" lessons per class by default
- Collapse the rest behind "See all X lessons in this class →"
- Highlight lessons that are unique/unexpected (like "Ralph Loop aka Ralph Wiggum", "How to Reverse Engineer Claude Code", "Make Claude Speak to You")

The unexpected/fun lesson titles are selling points — they signal this isn't a dry docs walkthrough. Elevate those.

**8. FAQ: add completion anxiety and expense confidence**

Two additions based on the research:

- **"I'm worried I won't finish it."** → "Most students don't watch every lesson sequentially. The MCP server recommends what's relevant to you right now. Watch what you need, come back when you need more."
- **"Can my company pay for this?"** → Strengthen the existing FAQ. Add: "At $199-294, most developers can expense this on a corporate card without manager approval. Toggle 'Add company info to invoice' at checkout."

### Suggested revised page structure

```
1. Hero (pain + promise — keep as is)
2. LogoMarquee (keep)
3. Stakes / Hiring Filter (keep — strong)
4. Who Teaches This (NEW — Ray's photo + 1-sentence bio + credibility)
5. Student Testimonials (NEW — 4-5 transformation quotes)
6. Before/After Table (NEW — specific Vibe Coder → Claude Code Person contrast)
7. BecomeClaudeCodePerson (keep)
8. MCP Personalization Spotlight (NEW or promoted from WhyThisBeats)
9. Contents with Progressive Disclosure (restructured)
10. WhyThisBeats (keep)
11. AlwaysCurrent (keep — strong)
12. PricingCards (revised third column: team pack or time-saved anchor)
13. Guarantee (keep)
14. FAQ (expanded)
15. Email Capture for Non-Buyers (NEW)
16. FinalCTA (keep)
```

---

## Key Takeaways

1. **Student testimonials are the #1 missing element.** Every successful course page in the research has them prominently. You have 3,151 students and zero visible transformation stories.
2. **Email capture is the #1 revenue-unlocking change.** Every visitor who doesn't buy today and can't give you their email is gone forever.
3. **The MCP "what to watch next" feature is being massively undersold.** It's a bullet point when it should be a section.
4. **The university price anchor doesn't work** because nobody is actually choosing between these options. Replace with something the buyer is genuinely weighing.
5. **The instructor should be visible early**, not hidden in a FAQ. Trust in the teacher is a top buying factor per Marie Poulin, Brennan Dunn, and Matt D. Smith.

---

## Sources

All insights derived from:
- 22 badass.dev podcast transcripts and case studies
- Matt Pocock's "Claude Code for Real Engineers" AIHero landing page ($795 cohort, March 2026)
- Agentic Coding School codebase (`apps/nextjs/src/components/landing/sections/`)
- Current live Master Claude Code sales page (3,151 students, $199/yr + $294 lifetime as of 2026-04-04)
