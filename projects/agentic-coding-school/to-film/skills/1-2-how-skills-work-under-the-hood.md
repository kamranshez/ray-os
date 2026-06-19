---
class: "skills"
chapter: "The Blank Slate"
status: "scripted"
tags: [course, script, skills]
lesson: "1.2 How Skills Actually Work Under the Hood"
---

## How Skills Actually Work Under the Hood

In the last video we saw what skills can do — the before and after. Now we need to understand how they actually work inside Claude. Because if you don't understand this, you'll end up installing a hundred skills and wondering why Claude got slower and started ignoring half of them.

The concept is called progressive disclosure. And once you get it, everything else in this class makes sense — why we structure skills a certain way, why there's a line limit, why descriptions matter so much.

### The Menu Analogy (0:00–1:30)

Here's how to think about it. Imagine you're at a restaurant. The waiter doesn't walk up and read you every ingredient of every dish in the kitchen. They hand you a menu. Short descriptions — name of the dish, a one-liner about what's in it. You scan the menu, pick what you want, and then the kitchen goes to work.

Skills work the same way.

Claude doesn't load every skill you've installed into its brain all at once. That would be insane — some skills are thousands of tokens long. Instead, Claude gets a menu. A list of every skill's name and a short description. That's all it sees at the start of every conversation.

And when you say something that matches one of those descriptions, Claude goes "okay, I need that skill" and loads it. Like ordering from the menu — the kitchen only fires up the dish you asked for.

That's progressive disclosure. Show only what's needed, when it's needed.

### The Three Tiers (1:30–4:00)

Now there are actually three levels to this. And I want to show you each one so you can see what's happening with your tokens.

> [SCREEN: Claude Code terminal]

I'm going to run `/context` right now, before I do anything.

> [TYPE: /context]

> [SHOW: the context visualization — system prompt, tools, and the skills list]

See that section? That's the skill descriptions. Every skill I have installed — just the name and the one-paragraph description of each. That's **tier one**. It's always loaded. Always in context. Every conversation, every session.

And each skill takes up roughly 100 tokens just for the description. Five skills? 500 tokens. Not a big deal. Fifty skills? 5,000 tokens. Starting to add up. And there's a hard cap — about 15,000 characters total for all your skill descriptions combined. That's roughly 50 to 70 skills before you physically run out of space.

This is why people who install 500 skills have problems. It's not just bloat — the descriptions start competing with each other. Claude sees two skills that sound similar and picks the wrong one. Or it sees too many options and just ignores them all.

Now. I'm going to trigger a skill.

> [TYPE: a prompt that triggers a specific skill]

Watch what happens to the token count.

> [SHOW: /context again — token count has jumped]

See that jump? That's **tier two**. The body of the skill.md just got loaded. The full process instructions — step one, step two, the rules, everything in the main file. This only loads when Claude decides it needs this skill. Before that prompt, it wasn't in memory at all.

Now the skill is running, and one of the steps says "read the content templates from the references folder."

> [SHOW: /context again — another smaller jump]

Another bump. That's **tier three**. A reference file just got pulled in — only because a specific step needed it. And when that step is done, Claude can effectively move on. It doesn't load every reference file in the folder — just the one the current step needs.

### Why This Matters (4:00–5:30)

So here's the thing. This three-tier system is what makes skills scalable. Without it, every skill would dump its entire contents into Claude's memory the moment you start a session. Five complex skills could fill half your context window before you even type a word.

But with progressive disclosure:
- Tier one — just the names and descriptions. Tiny footprint. Always there.
- Tier two — the process instructions. Only loads when the skill activates. Maybe 200 lines.
- Tier three — reference files, scripts, assets. Only loads piece by piece, as needed.

And this directly determines how you should build skills. If you cram everything into one massive skill.md file — and people do this, I've seen 1,000-line skill files — then the moment that skill triggers, all 1,000 lines hit your context at once. Tier two becomes enormous. Your conversation slows down. Claude starts drifting from instructions because there's too much to track.

But if you keep the skill.md lean — say, under 200 lines — and put the deep knowledge in reference files, then Claude only pulls what it needs for the step it's on. Tier two stays small. Tier three loads incrementally. Your context stays clean.

We'll get into exactly how to structure this in the anatomy video coming up in Chapter 2. But this is the principle behind everything.

### The Numbers That Matter (5:30–7:00)

A few concrete numbers to keep in mind.

> [SCREEN: simple list on screen]

**15,000 characters** — that's the total space for all your skill descriptions combined. Tier one. Everything Claude sees at the start. If you go over this, skills get truncated or ignored. Roughly 50 to 70 skills depending on description length.

**~100 tokens per skill** — the typical cost of a single skill's description in tier one. Seems small. But it adds up. Twenty skills is 2,000 tokens of your context window spent before you've typed a word.

**200 lines** — the target maximum for a skill.md body. Tier two. We'll talk about why in the anatomy video, but the short version: beyond 200 lines, Claude starts to lose track of what matters.

And here's the real danger number — if you have skills with similar descriptions, like two skills that both mention "design" or "SEO" or "content," Claude might pick the wrong one. Or activate both. Or neither. The more overlap in your tier-one descriptions, the worse the routing gets.

This is why a small set of well-described skills will always outperform a massive library of generic ones. Five skills with sharp descriptions beat fifty with vague ones.

### What's Next

Now you understand how skills load — the three tiers, the token costs, and why structure matters. In the next video, we're going to set up your workspace. Install Skill Creator, configure the one setting that makes skills actually trigger reliably, and get everything ready so you can start building in Chapter 2.
