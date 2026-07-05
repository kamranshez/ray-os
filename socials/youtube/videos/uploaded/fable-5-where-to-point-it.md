---
tags: [youtube, script, claude-code]
date: 2026-06-25
youtube-id: r4_KLZvHoaA
youtube-title: "Anthropic Will Bring Back Fable 5 Differently"
published: 2026-06-25
duration: "11:09"
views: 20450
likes: 548
comments: 53
status: uploaded
fetched: 2026-06-27
revenue: 2403
revenue-lift: 399
revenue-utm: 0
revenue-sessions: 10
revenue-method: "3-day time-proximity"
revenue-fetched: 2026-06-27
---

## Title options

| # | Formula | Title |
|---|---------|-------|
| 1 | Bold claim + specificity | Fable 5 Is Coming Back. Here's Where to Actually Point It. |
| 2 | Curiosity gap + stakes | Anthropic's Smartest Model Returns Next Week. Don't Waste It. |
| 3 | Relatable + provocative | You're About to Get a Genius You Can Barely Afford |

> Coined frame this video plants: **rationed intelligence**, and **build the hotlist before the model lands.**
> Format: feature deep-dive (Fable 5 return) + thesis broader-trend (when premium intelligence is metered, targeting becomes the skill). Method is borrowed from the security-researcher pipeline (Carlini / Mozilla / Anthropic red team).
> Demo surface: my own course funnel (analytics = Impact, git churn = Opportunity).
> **Pitch placeholders to confirm before filming:** `[DEADLINE]`, `[PRICE]`, free artifact = *"Impact x Opportunity scoring prompt + ranked-hotlist script"* (confirm), free class video cross-link = the *Score Before You Spend* / *Point-fix to Architectural-fix* lesson (confirm pairing).

---

### Hook (0:00 - 0:30)

*On screen: a usage meter ticking up and slamming into a red weekly limit. Then cut to a huge grid of thirty thousand files with one tiny glowing premium chip hovering over it, unsure where to land.*

If you've been waiting for Fable to come back, it looks like next week is it. The strings in the latest Claude Code build basically confirm it. "You've used your Fable 5 usage for this week." "Run slash usage-credits to keep using Fable 5."

So here's the catch nobody's saying out loud. You're about to get the most capable model you've ever had, and you're going to get a tiny, expensive, metered amount of it. And most people are going to waste it in the first ten minutes.

This video is the fix. I'll show you exactly where to point a model you can barely afford, using a method that security researchers already proved on a twenty year old codebase.

![[fable-hook-1.png|480]]
![[fable-hook-2.png|480]]
![[fable-hook-3.png|480]]
![[fable-hook-4.png|480]]
![[fable-hook-5.png|480]]

---

### The problem: three ways you'll waste it (0:30 - 1:45)

*On screen: three red X panels drawing in one at a time. "Point it at everything." "Pay premium to find where to look." "Fix one leaf."*

Think about what actually happens the day Fable comes back. You're excited, you open it up, and you do one of three things, all of them wrong.

One, you point it at your whole repo and say "fix the bugs" or "clean this up." It's thirty thousand files. It doesn't fit in context, the model has no idea where to start, so it flails or laser focuses on the first thing it touches. You just spent premium tokens on a coin flip.

Two, you spend your scarcest, most expensive model asking it the cheapest possible question: "where should I even look?" That's the one question a small, cheap model answers for pennies. You just paid premium prices to figure out where to work.

Three, you finally point it at the right file, it finds a real bug, fixes it, and then leaves the exact same bug alive in four other files because nobody told it the bug was a symptom.

Same root cause every time. The model got smarter. Your aim did not.

![[fable-three-ways-to-waste-1.png|480]]
![[fable-three-ways-to-waste-2.png|480]]
![[fable-three-ways-to-waste-3.png|480]]
![[fable-three-ways-to-waste-4.png|480]]
![[fable-three-ways-to-waste-5.png|480]]

---

### Soft anchor (1:45 - 2:15)

Quick pause before the method. This video is sponsored by me and my Claude Code Masterclass. Over 1,500 engineers from companies you've heard of have gone through it, and a lot of them are now the best Claude Code user at their company. You might be thinking, why buy lifetime if there's a better model in a year. There will be, Fable 5 is literally the proof, and you get lifetime access to all of it. The lifetime plan retires `[DEADLINE]` and the price goes up to `[PRICE]` after that. Link's below.

---

### The proven method already exists (2:15 - 4:00)

*On screen: the Firefox logo, then a file tree where files light up with 1-to-5 scores, the 1s and 2s greying out.*

Here's the good news. The hard version of this problem was already solved, by people with way more on the line than you or me.

Security researchers cannot read Firefox. Tens of thousands of files, tens of millions of lines, twenty years of history. Nobody holds it in their head and no context window holds it either. So you cannot one shot "find all the bugs."

What they do instead is rank before they spend. Nicholas Carlini ran a public API model over a codebase and, before any expensive run, asked it one cheap question per file. Rate this file one to five, how likely is it to hold an interesting bug. Throw out the ones and twos. Send the agents down the list in priority order.

Source: https://securitycryptographywhatever.com/2026/03/25/ai-bug-finding/

Anthropic's own red team did the exact same thing, independently, same recipe. A file ranked one has nothing dangerous in it. A file ranked five takes raw data off the internet and parses it.

Source: https://red.anthropic.com/2026/mythos-preview/

And the punchline from all of this work is the part you need: the result didn't come from a smarter model. It came from the targeting. As one security firm put it, a thousand adequate detectives searching where the bugs actually are will beat one brilliant detective guessing where to look. The scaffold is the moat, not the model.

That ranking step is the whole game. Now let me show you it's not a security trick.

![[fable-rank-before-spend-1.png|480]]
![[fable-rank-before-spend-2.png|480]]
![[fable-rank-before-spend-3.png|480]]
![[fable-rank-before-spend-4.png|480]]
![[fable-rank-before-spend-5.png|480]]

---

### The general law: Impact times Opportunity (4:00 - 5:30)

*On screen: a 2x2 matrix. Y axis "Impact, how much it matters." X axis "Opportunity, how fixable now." Top right glowing, labeled "Send Fable here."*

Strip away the security specifics and every "where should the model work" question is the same shape.

Score equals Impact times Opportunity.

Impact is how much this part matters. Reach, traffic, how often it runs, how many things depend on it. Opportunity is how bad or how fixable it is right now. How buggy, how slow, how far it's drifted from good.

You multiply them, because either one alone lies to you. A component everyone hits that already works is a waste of the model's time. A component that's broken but nobody touches is also a waste. You want the corner where both are high.

That gives you four corners. High impact, high opportunity, that's the hotspot, point Fable there first. High impact but already fine, leave it. Broken but nobody cares, skip it. Low low, ignore.

The security ranker was just this formula with Impact set to "can an attacker reach it" and Opportunity set to "how likely is it buggy." Same machine. And that same machine runs on basically anything, so let me show you.

![[fable-impact-opportunity-quadrants-1.png|480]]
![[fable-impact-opportunity-quadrants-2.png|480]]
![[fable-impact-opportunity-quadrants-3.png|480]]
![[fable-impact-opportunity-quadrants-4.png|480]]
![[fable-impact-opportunity-quadrants-5.png|480]]

---

### What you can point it at (5:30 - 6:25)

*On screen: equation cards snap in fast, two at a time, each one "[ Impact ] x [ Opportunity ]" with the two fuels named, filling into four labeled columns as they go: Code, Growth, Cost, Reliability.*

Here's why this formula is worth burning into your head. It's the same two boxes every single time. You just swap the fuel.

Want to attack tech debt? Impact is git churn, how often a file changes, Opportunity is complexity. Hunt the files that are both hot and tangled. Dead code? Confidence it's unused times its size. Delete the big, confidently dead stuff first.

Growth side, same machine. Conversion is analytics traffic times drop off, rebuild the worst converting high traffic component. SEO is page traffic times ranking gap, improve the pages sitting just off the prize.

Cost? Dollar spend times how optimizable a call is, point it at the three calls burning your bill. Performance is run frequency times slowness, the benchmark is the score, make the number go down.

Reliability and standards, still the same shape. Bug hotspots are change frequency times how often that file shows up in hotfixes in git blame. Test coverage is blast radius times the coverage gap. And the fuzzy one, API or design consistency, is how much something gets used times how far it's drifted from a rubric you wrote down.

Eight different jobs. One formula. Impact times Opportunity, every time. So the question is never "is there a clever trick for this thing." It's "what's my Impact, what's my Opportunity, and can I put a number on each."

![[fable-scoring-examples-1.png|480]]
![[fable-scoring-examples-2.png|480]]
![[fable-scoring-examples-3.png|480]]
![[fable-scoring-examples-4.png|480]]
![[fable-scoring-examples-5.png|480]]

---

### Build the machine before the model lands (6:25 - 7:55)

*On screen: a timeline. Left, "this week, cheap models" building a sorted stack labeled "hotlist ready." A vertical line "Fable arrives." Right of the line, the premium chip drops straight onto the top item, no detour.*

Here's the move almost everyone will miss, and it's the one the narrow window forces.

The scoring pass is cheap, it's repeatable, and it does not need Fable. So run it now, this week, while you're still on the abundant models. Build the ranked list before the premium model is even back.

Because the worst thing you can do is wait for Fable, then burn the first slice of your weekly budget asking it where to look. Separate the two jobs. Where to work is cheap, deterministic, and done in advance. The hard fix is expensive and done in the window.

Let me show you the shape of it on my own course funnel, and notice I build the whole thing on cheap models, as if Fable isn't here yet.

*Demo, narrated over: open the landing page components folder, thirty something of them, Hero, PricingCards, FAQ, the paywall, the checkout.*

For Impact, I pull the real analytics events straight out of the code. Paywall viewed, purchase button clicked, video abandoned. That's reach and drop off per component. For Opportunity, I run a one line git churn command. PricingCards has been rewritten dozens of times, the legal pages almost never. High churn means contested and unstable.

Then I hand both feeds to a cheap model with the rubric, Score equals Impact times Opportunity, and ask for a ranked table with a one line reason each. PricingCards and the paywall float to the top, high traffic, a drop off event sitting right there, heavy churn. Terms and privacy sink, churny maybe, zero funnel impact. I save that table. That's the hotlist, and it cost me almost nothing.

So when Fable lands, there's no thinking. I open the file at the top of the list and the premium run goes straight to work.

![[fable-build-before-arrival-1.png|480]]
![[fable-build-before-arrival-2.png|480]]
![[fable-build-before-arrival-3.png|480]]
![[fable-build-before-arrival-4.png|480]]
![[fable-build-before-arrival-5.png|480]]

---

### Don't waste the run on one leaf (7:55 - 9:25)

*On screen: a code tree. One node gets a green check, "point fix." Three identical red nodes elsewhere stay faded. Then a second panel, one sweep labeled "architectural fix" turns all four green at once.*

Okay, you've targeted. You spend a precious Fable run on the number one hotspot. It finds the bug, fixes it, the crash goes away. And it leaves the entire class of that bug alive everywhere else.

This is the subtle waste, and it's the exact wall the Firefox team hit. Watch what their human reviewers kept writing on the agent's correct patches: yep, real issue, fix looks good, but actually we should check a few other places. A world class engineer reads a one line patch and instantly knows the same mistake is sitting in three other files. The agent never looked, because nobody told it the bug was a symptom.

So the rule for a rationed model is the opposite. When you spend a Fable run, it has to close a whole class. Take the one confirmed fix, recognize the pattern behind it, find every other place that pattern lives, and ship one clean fix that closes all of them. One expensive run, dozens of instances gone.

And this is exactly why it's the premium model's job. The cheap model found the file. The categorical leap, seeing the class behind the instance and designing one global fix, is the reasoning weaker models flatten into a single point patch. That generalization is what you're paying Fable for. Don't let it act like the cheap one.

![[fable-leaf-vs-class-1.png|480]]
![[fable-leaf-vs-class-2.png|480]]
![[fable-leaf-vs-class-3.png|480]]
![[fable-leaf-vs-class-4.png|480]]
![[fable-leaf-vs-class-5.png|480]]

---

### The three tier stack (9:25 - 10:25)

*On screen: three stacked bands. Top wide and pale "Tier 1 judge, cheap, score and rank, ahead of time." Middle "Tier 2 targeter, cheap, find the whole class." Bottom narrow and glowing gold "Tier 3 Fable, rationed, architectural fix." An arrow narrows top to bottom.*

Put it all together and you've got a stack, and each tier is a different price of compute doing the job only it should do.

Tier one, the judge. Cheap, abundant, runs in parallel and runs ahead of time. It scores every file Impact times Opportunity and produces the hotlist.

Tier two, the targeter. Still cheap. It confirms the top hotspot is real and gathers every instance of the pattern, so the expensive run has the full class in front of it.

Tier three, the architect. That's Fable. Rationed and expensive. It does the one thing the cheap tiers can't, the deep reasoning that designs a single clean fix across the whole class and proves it. That's where your weekly allotment goes, and nowhere else.

The cheap tiers decide where and build the case. The premium tier does the hard thinking on the single highest leverage surface. That's how you get the most out of a model you're only allowed to use a little.

![[fable-three-tier-stack-1.png|480]]
![[fable-three-tier-stack-2.png|480]]
![[fable-three-tier-stack-3.png|480]]
![[fable-three-tier-stack-4.png|480]]
![[fable-three-tier-stack-5.png|480]]

---

### The honest counter-take (10:25 - 11:25)

*On screen: a "but is this overkill?" title card.*

I don't want to only sell you the dream, so here are the fair objections.

One, isn't this overkill. If your project is twenty files, yes, completely. You can read all twenty yourself and you know where the problem is. Scoring is pure overhead on a small repo. This only earns its keep when the surface is bigger than any human or any context window can hold. Big codebase, the judge is essential. Small codebase, skip it.

Two, garbage in, garbage out. The judge is only as good as the signal you feed it. If you score off vibes, you get a vibes ranking. The grounded end, real analytics, a profiler, git history, beats a model guessing every time. And the uncomfortable part, for the fuzzy stuff like design or code quality, you have to actually write down what good means before a model can score drift from it. The bottleneck was never the model. It's whether you can define good crisply enough to put a number on it.

Three, maybe Fable won't even be that limited. Maybe. But your real budget was never just tokens. There's a human cost to reviewing and verifying every change the agent ships. As Claire Vo put it, you cannot go completely prioritization free. Even with infinite Fable, your attention is finite, and the hotlist is how you spend it well.

![[fable-counter-take-1.png|480]]
![[fable-counter-take-2.png|480]]
![[fable-counter-take-3.png|480]]
![[fable-counter-take-4.png|480]]
![[fable-counter-take-5.png|480]]

---

### What this means for you (11:25 - 12:00)

So where does this leave you, today, before Fable's even back.

Don't wait for it. The targeting machine is the thing you build now, on the cheap models, while you wait. Score your codebase Impact times Opportunity, save the ranked list, and have it sitting there ready.

Then the day Fable lands, you don't waste a single run figuring out where to look or fixing one leaf at a time. You open the top of the list, you tell it to close the whole class, and you spend your scarce, expensive intelligence exactly where it pays. The model isn't the moat. The judge that decides where to point it is.

![[fable-what-it-means-1.png|480]]
![[fable-what-it-means-2.png|480]]
![[fable-what-it-means-3.png|480]]
![[fable-what-it-means-4.png|480]]
![[fable-what-it-means-5.png|480]]

---

### Closer + pitch (12:00 - 12:45)

That's the real shift. A smarter model is about to land, you're going to get less of it than you want, and the people who win that window are the ones who already scored where to point it.

If you want to get genuinely good at this, building the scoring and the specs that make a scarce model pay off, that's the core of my Claude Code Masterclass. The lifetime plan is gone after `[DEADLINE]` and the price goes up to `[PRICE]`. Fourteen day money back guarantee, and less than 0.2% of buyers have ever asked for one. My email's in the description if you've got questions.

And if you liked this, there's a free video in the class where I walk through the full Score Before You Spend pipeline on a real codebase, end to end. No credit card, just sign up to watch it. Link's in the description.
