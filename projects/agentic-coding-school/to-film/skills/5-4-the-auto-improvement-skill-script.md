---
tags: [course, script, skills]
status: draft
lesson: "5.4 The Auto-Improvement Skill"
duration: "7-10 min"
---

## The Auto-Improvement Skill

In the last video, skills learned to improve themselves through feedback loops. This video is different. This isn't about a skill getting better at its own job. This is about your system telling you what to build next.

Because right now, you've got maybe 15 skills from this class. Your system handles content, marketing, operations, finances. But there are gaps. Tasks you're still doing manually. Steps in your workflows that could be their own skill. Entire categories you haven't built for yet.

The auto-improvement skill finds those gaps for you.

### What It Does (0:00–1:30)

The concept is straightforward. A meta-skill that reviews your recent sessions — what skills you used, what tasks you did manually, where you spent time — and suggests new skills to build.

It looks for three things:

**Repetitive tasks you're still doing manually.** If you've typed the same kind of prompt three times this week without a skill firing, that should probably be a skill.

**Steps in existing workflows that could be their own sub-skill.** Maybe your content director chain has a formatting step that's getting complex enough to break out.

**Gaps in your system.** You've got content creation but no content distribution. You've got invoicing but no payment follow-up. The auto-improvement skill sees the shape of what you've built and identifies what's missing.

### Building It (1:30–3:30)

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build an auto-improvement skill. It should review my recent sessions and identify: tasks I did manually that should be skills, steps in existing workflows that could be sub-skills, and gaps in my skill system — categories I haven't covered yet. Output a prioritized list of suggested new skills with a one-line description for each."]

Skill Creator builds it. The skill.md is simple — it reads session history, checks what skills exist, identifies patterns in what I'm doing without skills, and produces recommendations.

> [SHOW: the generated skill]

Now I run it.

> [TYPE: "What skills should I build next?"]

> [SHOW: the auto-improvement skill processing — reviewing recent sessions]

It's scanning my recent work. What skills triggered. What tasks I did in conversation without any skill. Where I spent the most time manually.

> [SHOW: the output — prioritized list of skill suggestions]

And here's what it found.

```
SUGGESTED NEW SKILLS (prioritized)

1. Email follow-up tracker — you sent 4 follow-up emails manually
   this week. Pattern detected: check if client responded after 5 days,
   draft a follow-up if not.

2. Meeting notes summarizer — you pasted 3 meeting transcripts and
   asked for summaries. Same format each time. Should be a skill.

3. Content distribution — you have content creation skills but
   nothing that posts to LinkedIn/Twitter after content is drafted.

4. Client onboarding checklist — you walked through the same
   onboarding steps for two new clients. Repeatable process.

5. Weekly metrics dashboard — you asked for business metrics twice.
   Could be a scheduled skill that runs every Monday.
```

Five suggestions. Each one is a real gap based on what I've actually been doing. Not hypothetical — observed.

### Acting on a Suggestion (3:30–5:30)

I'm going to take suggestion number two — meeting notes summarizer — and build it right now. Because I did paste three transcripts this week and each time I gave basically the same instructions.

> [TYPE: /skill-creator]

> [TYPE: "Build a meeting notes skill. Given a meeting transcript, produce: key decisions made, action items with owners, open questions, and a one-paragraph summary. Format as markdown."]

> [SHOW: Skill Creator building the skill — quick, because it's a simple skill]

Done. Took about a minute. Now I have a skill for something I was doing manually three times a week. That's maybe 30 minutes saved per week. And I wouldn't have thought to build it — the auto-improvement skill identified the pattern.

### The Growth Loop (5:30–6:30)

And this is the real value. This class teaches you to build maybe 15-20 skills. But your system should keep growing — 30, 40, 50+ skills over time as your business evolves.

Without the auto-improvement skill, growth depends on you noticing your own patterns. Which you'll sometimes do and sometimes miss. With it, the system audits itself. It watches how you work and tells you where automation would help.

The loop: use your skills → auto-improvement identifies gaps → build the suggested skills → use those → auto-improvement finds new gaps → repeat.

Run it once a week. Or turn it into a scheduled task that runs every Friday and gives you a "skills to build this weekend" list. Either way, your system gets smarter over time without you having to actively think about what to build next.

### What's Next

One more lesson in this chapter — the customizer pattern. It's a quick one. Instead of building skills from scratch, you take someone else's skill and customize it to your preferences in about 60 seconds.
