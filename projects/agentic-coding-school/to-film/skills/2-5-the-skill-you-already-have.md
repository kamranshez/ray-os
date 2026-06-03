---
class: "skills"
chapter: "Your First Skill"
status: "new"
tags: [course, script, skills]
lesson: "2.5 The Skill You Already Have"
---

## The Skill You Already Have

So we've built two skills in this chapter — the interrogate skill by hand, and the research skill with Skill Creator. Both from scratch. But here's something I want you to consider before we move on. You probably already have skills. You just haven't turned them into skill files yet.

Every business has playbooks. Templates. Checklists. Process documents. That proposal format you use every time. That client onboarding sequence. That review checklist you paste into Claude and then spend five minutes explaining the context around it. All of those are skills waiting to be encoded.

### The Repeat Prompt Problem (0:00–1:30)

Here's what this looks like in practice. You've got a process — maybe it's reviewing incoming proposals, or summarizing client calls, or formatting deliverables. And every time you do it in Claude, you type some version of the same long prompt. You paste in your template. You explain your criteria. You remind Claude about your preferences.

And the output is good — because you've given it good instructions. But you did 10 minutes of setup for a task Claude should already know how to do your way.

That's the gap a skill fills. You take that big prompt — the one you've refined over weeks of using Claude — and you save it as a skill. Now it fires every time. No pasting. No re-explaining. You just say "review this proposal" and the skill handles the rest.

As Zack Shapiro, a lawyer who's been doing this with contract review, puts it: "A template library is not a competitive advantage. Every competent firm in your practice area has roughly the same templates. The thing that differentiates a great lawyer from a mediocre one was never the template. It was what the lawyer did with the template." Your judgment. Your criteria. Your process. That's what you encode.

### The Demo — Document to Skill (1:30–4:00)

I'm going to take a real document and turn it into a skill right now.

> [SCREEN: a proposal review checklist open in an editor — a business document with sections, criteria, scoring]

This is a proposal review checklist I use. It's got sections — scope alignment, budget reasonableness, timeline feasibility, risk flags, missing deliverables. For each section, there are specific things to check and a severity rating.

Every time I review a proposal, I paste this into Claude and say "use this to review the attached proposal." Works fine. But I'm pasting it every time.

So I'm going to turn it into a skill.

> [SCREEN: Claude Code terminal]

> [TYPE: /skill-creator]

> [TYPE: "I have a proposal review checklist I use regularly. I want to turn it into a Claude skill so anytime I give Claude a proposal, I can just say 'review this proposal' and it automatically applies my checklist, my criteria, my severity ratings — without me pasting anything."]

And then I paste the checklist document into the chat.

> [SHOW: Skill Creator processing — asking follow-up questions]

Skill Creator reads the document and asks me about edge cases. "What if the proposal doesn't include a budget section? What if there are multiple deliverable timelines? How should it handle incomplete information?" I answer those — maybe two minutes of back and forth.

And then it builds the skill.

> [SHOW: the generated skill — skill.md with the review process, references/checklist.md with the criteria]

It split my checklist into two files. The skill.md has the process — read the proposal, apply the checklist, score each section, flag risks, produce a summary. And it moved the detailed criteria into a reference file. Clean separation. The skill.md is about 80 lines.

Now let me test it.

> [TYPE: "Review this proposal" — with a sample proposal attached]

> [SHOW: the output — structured review with severity ratings, missing items flagged, specific recommendations]

Structured review. Section-by-section scoring. Risk flags. Missing deliverables called out. Specific recommendations — not generic "consider reviewing the budget" but actual counter-suggestions.

> [SPLIT: left — generic "review this proposal" without skill | right — skill-encoded review with severity ratings and specifics]

Left side — what Claude does without the skill. It reads the proposal and gives you a decent summary. Right side — what it does with my judgment encoded. Severity ratings. My specific criteria. The things I've learned to look for over years of reviewing proposals.

Same document. Same model. The skill is the difference.

### What Can Become a Skill (4:00–5:00)

Now I want you to think about your own work. What do you do repeatedly that involves explaining your process to Claude?

Some patterns to look for:

**Any prompt you've saved and reuse.** If you've got a note somewhere with your "good prompt" that you paste in — that's a skill.

**Any document you reference during AI tasks.** Brand guidelines. Style guides. Review criteria. Onboarding checklists. If you're uploading or pasting it repeatedly, encode it.

**Any workflow with more than 3 steps.** If you find yourself saying "first do this, then do this, then format it like this" — that sequence is a skill.

**Any task where you correct Claude the same way every time.** "No, shorter." "No, use bullet points not paragraphs." "No, include the pricing." If you keep making the same correction, put it in the skill so you never have to make it again.

You don't need to build these from scratch. Feed the existing document to Skill Creator, answer the edge case questions, and you've got a skill in five minutes that encodes months of your accumulated judgment.

### What's Next

That wraps up Chapter 2. You can build skills by hand, with Skill Creator, and from existing documents. You understand the anatomy — the 200-line rule, reference files, descriptions, guardrails.

But every skill we've built so far is generic. It doesn't know your brand. It doesn't know your audience. It doesn't know your voice. In Chapter 3, we're going to fix that — starting with adding your brand context so that every skill produces output that sounds like you, not like AI.
