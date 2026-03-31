---
tags: [course, script, skills]
status: draft
lesson: "5.5 The Customizer Pattern"
duration: "5-7 min"
---

## The Customizer Pattern

Quick one to close out this chapter. You've got the brand context approach from Chapter 3 — shared reference files that all your skills pull from. That's the systematic approach. Great for skills you build from scratch.

But sometimes you download someone else's skill and you just want to quickly make it yours. Different colors. Different tone. Different output format. That's the customizer pattern.

### The Problem (0:00–0:45)

You find a great slide deck skill on a marketplace. Install it. Use it. The output is solid — but it's got someone else's aesthetic. Their color scheme. Their layout preferences. Their idea of what a good slide looks like.

You could open the skill.md and manually rewrite the style sections. Or you could build a customizer skill that does it in 60 seconds through a conversation.

### The Customizer in Action (0:45–3:00)

I built a customizer skill. Here's how it works.

> [SCREEN: Claude terminal]

> [TYPE: /customize]

The skill asks me a few questions.

> [SHOW: customizer asking questions]

"Which skill do you want to customize?" — The slide deck builder.

"What's most important to change?" — The visual design. Colors and layout.

"Describe your preferred style." — Minimal. Swiss design influenced. Black, white, and one accent color. Lots of whitespace. No gradients.

> [SHOW: the customizer processing — reading the skill, updating style references]

It reads the existing skill.md, identifies the style-related sections, and rewrites them to match my preferences. It doesn't touch the process logic — the steps for how to build a deck stay the same. It only changes the aesthetic parameters.

> [SHOW: the updated skill]

Done. The skill now has my style baked in. Let me test it.

> [TYPE: "Build a slide deck about the three-tier loading system for skills"]

> [SPLIT: left — original slide deck skill output | right — customized output]

Left side — the original. Colorful, rounded corners, someone else's style. Right side — mine. Black and white with red accent. Clean typography. Lots of whitespace.

Same structure. Same content quality. Different look. And it took about 60 seconds of answering questions.

### When to Use This vs Brand Context (3:00–4:00)

So we've got two approaches now:

**Brand context** from Chapter 3 is the systematic approach. You create shared reference files — voice, visual style, messaging pillars — and every skill you build references them. Best for skills you create from scratch. It's thorough and consistent.

**The customizer** is the quick approach. You take an existing skill — one you downloaded or got from someone — and adapt it to your preferences through a conversation. Best for imported skills where you don't want to rebuild from scratch.

They're not either-or. You can customize a skill quickly to get it working, then later connect it to your brand context for deeper consistency. Start fast, refine later.

### Sharing Implications (4:00–4:45)

And here's why this pattern matters for teams. In Chapter 7, we'll talk about sharing skills. If you build a skill plugin and share it with five team members, each person has different preferences. Different writing styles. Different visual tastes. Different output formats.

Instead of building five versions of every skill, you build one and include the customizer. Each person runs `/customize` once and gets their own personalized version. One skill, many tailored instances.

### What's Next

That wraps Chapter 5 — Quality Control. Your skills now have evals for measurement, A/B testing for optimization, feedback loops for self-improvement, an auto-improvement skill for finding gaps, and a customizer for quick personalization.

In Chapter 6, we wire everything together. Skills that chain, stack, run on schedules, and form a complete system you can visualize.
