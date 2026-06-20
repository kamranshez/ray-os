# Viral Playbook

What makes a post in Ray's niche spread is two things stacked: a **format pattern** (the structural move) and an **emotional trigger** (what the reader feels). Pick one of each. Execute it cleanly. Don't mix patterns inside a single post.

This file has both layers. The 8 format patterns are the dominant lessons from the 15-post viral sweep in `viral-examples/2026-06/`. The 6 emotional triggers are the deeper psychology layer.

If you read nothing else, read the 8 format patterns.

---

# The 8 Format Patterns

Distilled from the 2026-06 sweep of 15 viral Claude Code posts in `viral-examples/2026-06/`. Engagement deltas in that sweep ranged from ~10 reactions to 2,523 — the gap was format, not topic. Top performers used 4-5 of these consistently.

## 1. Lead with a contrast, not a feature

Viral hooks state a complete reframe in line 1. They don't tease, they don't announce, they confront.

- "Vibe coding is a lie." (Luís Rodrigues, 1,431 reactions)
- "Most people use one Claude. The leverage is knowing which Claude to use." (Adam Danyal, 205)
- "Most people treat Claude like a smart intern. Anthropic's engineers treat it like a system that prompts itself." (Jahanzaib Ahmed pattern)
- "Most people open Claude Code and start typing prompts. Anthropic's engineers open Claude Code and start writing loops." (Ray, 2026-06-09)

**Avoid:** "Anthropic shipped X" / "There's a new tool called Y" / "I want to talk about Z." Direct information delivery has been Ray's default; this is the upgrade.

**The formula that works most often:** "Most people [current behavior]. [Authority / smart group] [new behavior]."

**Precondition (don't skip this):** "Most people [X]" only works when X is *genuinely common*. If almost nobody is doing the thing yet (a hidden or novel approach), "Most people do X with it" is a false premise and the post collapses. For hidden unlocks, **invert the formula**: contrast a *broadly true* behavior against your rare one ("Everyone points Claude Code at their codebase. I point it at my flashcards.") and switch the trigger from belief disruption to **curiosity gap + insider/ahead-of-the-curve status** ("I still haven't seen anyone else do this"). Before writing a "Most people X" hook, ask: is X actually what most people do? If not, flip it.

## 2. Write for repostability, not just readability

Reposts put the post in front of new audiences. The structures that get reposted are tier maps and decision rules — content that becomes reference material people screenshot.

- Charlie Hills "Claude has 3 levels of automation" → 82 reposts
- Julia Danyal "Claude Code explained like Lego" → 85 reposts
- Adam Danyal "Three Claudes" → 32 reposts
- Nate Herk "Every Level of Claude Explained" → 20 reposts

Essays get reactions. References get reposts.

**Aim for at least 1 of every 3 posts to be screenshot-able as a one-page guide.** Tier maps ("X has N levels"), decision rules ("If you want X → do Y"), and 4-step recipes are the formats that travel.

## 3. Frontload earned authority — and quiz Ray to surface it

Viral posts open with a credibility flex:

- Luís: "I've shipped production systems across payments, credit scoring, and enterprise SaaS."
- Nate: "After 400+ Hours Inside"
- Dan: "Last week I taught 133 founders the Claude system I actually use."

That credibility front-loads the contrarian claim and earns the take.

**Ray's actual moat:** 3+ months of daily loops, a 19-hour run testing 500 user flows, an 11-hour follow-up loop, ~200 daily routines, Sentry/Stripe/Slack-backed loops, 4.1M tokens on a single feature loop that paid for itself in a day, a masterclass with 300+ videos. Boris is a fine quote, but **Ray's own experiments are stronger authority than anyone else can use.**

**Quiz step (do this before drafting):** Before writing any post, ASK Ray:

1. "What have you personally done that's relevant to this topic — specific runs, experiments, numbers, or stories?"
2. "What's the most counterintuitive thing you've learned about it that doesn't show up in the discourse?"
3. "What's the most concrete recent stat or scene you can offer? (hours, tokens, $, lines of code, count of something)"

Weave the answers into the draft. The viral version of the post is usually one Ray-specific number + one Ray-specific scene short of where the first draft lands.

## 4. Twist ending: tactical → emotional

Every top performer pivots in the last 2-3 lines from how-to to how-it-feels.

- Nate: "The stall at level 5 isn't technical. It's trust."
- Luís voice agent: "The agent knew more about my own product than my FAQ does."
- Luís vibe coding: "AI is the most powerful tool we've ever had. But a tool still needs a craftsman."

**Default for Ray's posts has been insight-statement closes** ("That ceiling is gone."). Push for the emotional reframe instead — what does it feel like to wake up to a merged PR? What does it feel like to realize you've been the bottleneck for 18 months?

## 5. Quantify everything. Kill qualifiers.

Every claim in the viral posts has a number:

- "133 founders" / "150 hours a year" / "3,000 leads"
- "8 hours" / "130,000 lines" / "30 minutes"
- "$5K to $15K" / "Save 5+ hours a week"
- "After 400+ hours inside"

**Hit list of qualifiers to delete on sight:** "around", "a couple", "many", "a lot", "tons", "several", "most", "a bunch of". Replace with numbers. Estimate if you have to.

## 6. Decision rule as the close

Three lines, three verbs, a complete summary. The viral close is a reusable rule, not a final thought.

- Adam Danyal: "Chat thinks. Code builds. Cowork operates."
- Charlie Hills: "You start it → Skills in Claude Chat. Timer-based → Scheduled Tasks. Laptop closed → Claude Code."

Insight-statement closes feel finished but aren't reusable. Decision-rule closes get screenshot.

## 7. Arrows (→) over bullets

Every top performer uses `→`. Not `•`, not `-`. Reads as causation ("this leads to that") rather than a flat list. Switch your bullets to arrows by default.

## 8. One pattern per post

Viral posts pick ONE structure and execute it cleanly:
- Tier map
- Decision rule
- Contrast hook + recipe
- Confession / personal story
- Changelog / "what shipped while I slept" inventory
- "X is a lie" + earned proof

Don't mix. If a draft is trying to be a tier map AND a decision rule AND a confession, pick one and write the other two as separate posts.

**Where to find the patterns:** every file in `viral-examples/2026-06/` is labeled by pattern in its frontmatter `format:` field. Pick a file, read its `what_to_steal_for_ray:` block, write the post inside that structure.

---

# Strategic angle for Ray specifically

Ray has ~3 months of daily loops. Nobody else in the 2026-06 sweep has that depth. His authority anchor is **himself**, not Boris.

Alternate post types:
- **Authority-anchored** (Boris quote / Daisy Hollman quote / Steinberger tweet) when shipping a paradigm shift the reader doesn't yet believe.
- **Self-anchored** (Ray's 19-hour run / 200 routines / Slack-as-decision-surface tactical reveals / 4.1M-token loop economics) when shipping a recipe or contrarian take.

The second category is where Ray uniquely wins. Lean into it.

---

# The 6 Emotional Triggers (the psychology layer)

The 8 format patterns above are the *structure*. The triggers below are *what the reader feels* once the structure delivers them to the body of the post.

Every viral post uses 2-3 of these. Pick a primary trigger (your hook) and a secondary trigger (your body). Trying to use all 6 creates confused content.

## 1. Identity Validation

Make people feel *seen*. Articulate something they've thought but never said out loud. When someone reads it and thinks "I've literally thought this exact thing," they can't help but engage.

The power comes from going past the surface observation into the psychological reality underneath.

- Weak: "Cold email is hard."
- Strong: "You don't hate sales. You hate feeling like a used car salesman because someone told you that's what selling requires."

For Ray's niche: articulate what developers/founders feel about AI but haven't put into words yet. The anxiety, the excitement, the confusion about their role changing.

## 2. Status Signaling Opportunity

People share content because sharing it makes *them* look good. The question isn't "is this valuable?" — it's "what does sharing this say about the person who shares it?"

Content that gets shared makes the sharer look:
- Informed (insider knowledge others don't have)
- Ahead of the curve (contrarian takes before they're mainstream)
- Competent and generous (tactical breakdowns)

Nobody can post "I'm really smart about AI" without looking like an ass. But they can share your post and add "this is exactly right" to achieve the same result.

You're not just writing posts. You're creating vehicles for other people's self-presentation.

## 3. Tribal Belonging

Create clear in-group/out-group dynamics. "This is for founders who..." or "If you're the kind of developer who..." creates identity categories people want to belong to.

- "There are two types of developers: ones who are learning to work with AI, and ones who are polishing a resume that'll be obsolete in 18 months."
- "Every 'AI skeptic' I know is using ChatGPT daily. They just don't post about it because their identity is built on being the contrarian."

The reader self-selects into the sophisticated group and engages to demonstrate they belong there.

## 4. Productive Discomfort

Make people feel uncomfortable in a way that motivates action. Not negativity — discomfort with a path forward.

The psychology: cognitive dissonance. When you make someone aware their current behavior conflicts with their self-image, they either argue (comments) or commit to change (engage, save, follow). Both are great for engagement.

- "You've been posting on LinkedIn for 6 months and have fewer than 500 followers. This isn't an algorithm problem. This is a 'nobody cares about what you're posting' problem."
- "You're still reviewing AI-generated code line by line. You're not being diligent. You're being slow because you don't trust your own judgment about what to check."

## 5. Curiosity Gap

The psychological tension created when someone knows information exists but doesn't have it. Intensity matters more than novelty.

- Weak: "Here's how to use Claude Code better."
- Strong: "The Claude Code setup that replaced my junior developer — and the one mistake that almost cost me a production database."

Elements of a strong curiosity gap:
- Specific numbers or outcomes
- Implied insider knowledge
- Tension between expectation and reality

Best when combined with other triggers: "The uncomfortable truth about why your AI workflow is slower than coding by hand" (curiosity + productive discomfort).

## 6. Aspiration and Possibility

Make people believe something they want is actually possible for them. Not inspiration (passive) — aspiration (active). The reader should mentally project themselves into the future state.

The key: aspiration without believability is fantasy. "$10M in year one" triggers skepticism. "From 0 to deploying 3 AI agents in a weekend" triggers aspiration because it feels achievable.

- Outcomes that feel achievable (impressive but not impossible)
- Timeframes that feel realistic
- Methods that feel accessible
- Proof that feels authentic (specific numbers, not vague claims)

---

# Belief Disruption Structure

Pairs cleanly with format pattern 1 (lead with contrast). The most powerful content takes something your audience currently believes and demonstrates why it's wrong. This isn't being controversial for attention — it's creating awareness of a gap they didn't know existed.

Structure:
1. **State the common belief clearly** — "Most developers think the way to use AI is to paste code into ChatGPT and ask it to fix bugs."
2. **Create doubt** — "But I know developers who do that all day and ship slower than before AI existed. And I know developers who use AI for 20 minutes a day and ship 5x more."
3. **Introduce the alternative frame** — "The difference isn't the tool. It's what they're delegating. One group automates typing. The other automates thinking."
4. **Show the implication** — "Which means most developers are working harder with AI for worse results because they're automating the wrong layer entirely."
5. **Path forward (optional)** — A question, a reframe they can apply, or a resource.

---

# The Authenticity Filter

Before posting, every post must pass these four tests. Emotional content that fails these reads as guru-bait and destroys trust.

1. **Is this true?** Not "could this be true" — is this actually true based on direct experience?
2. **Would you say this in person?** Imagine saying it at a dinner with smart people in the industry. If it would feel try-hard, it will feel that way on LinkedIn.
3. **Is the emotion earned?** Emotion should be proportional to the point. "This will DESTROY your workflow" about a minor feature is ridiculous. Strong language about a genuine paradigm shift is earned.
4. **Does this serve the reader?** If you're triggering emotions for engagement rather than to help someone understand something important, it will come through.

**The specificity test:** Generic = guru energy. "Most people are doing this wrong" is generic. "Developers who've been using Cursor for 6 months but still write every function by hand" is specific. Specificity signals you actually understand the problem.

---

# Formatting (tactical)

These are amplifiers, not replacements for the format patterns above.

- One idea per line (not per paragraph)
- Short sentences. Three to ten words. Stack them.
- **Arrows (→) over bullets — see pattern 7.** Default rule, not optional.
- Sentence-case capitalization always
- Bold Unicode (𝗕𝗼𝗹𝗱) for section headers sparingly
- 1-3 hashtags max, at end only — and most viral posts skip hashtags entirely
- Questions to invite comments: "What's your take?" / "Am I wrong?" / "Which level are you at?"
- **No em or en dashes** — house style. Use commas, periods, or sentence breaks.

---

# What to Avoid

- **Information delivery without emotion** — "Here are 5 tips for X" with no psychological trigger
- **Corporate language / press release tone** — kills all emotion instantly
- **Fake urgency or scarcity** — nobody believes it, destroys trust
- **Generic applicability** — if it applies to everyone it resonates with no one
- **Unearned intensity** — hyperbolic language about minor things
- **"I'm excited to announce"** — the most emotionally dead hook on the platform
- **Being controversial without substance** — disruption needs a real alternative frame, not just a hot take
- **Mixing format patterns** — see pattern 8. Pick one structure per post.
- **Qualifiers in place of numbers** — see pattern 5. "Around 200" → "200". "Several hours" → "19 hours".
- **DM keyword CTAs ("Comment 'X' and I'll send you the guide")** — not Ray's house style even though it drives comments in this niche.
