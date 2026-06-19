---
class: "skills"
chapter: "Make It Yours"
status: "idea"
tags: [course, script, skills]
lesson: "3.1 Adding Your Brand Context"
---

## Adding Your Brand Context

So we've built skills that work. The research skill finds good topics. The interrogate skill asks the right questions. But if you look at the output closely, it sounds like... Claude. It's competent. It's correct. But it doesn't sound like you.

And this is the single biggest difference between a skill that's useful and one that's genuinely powerful. A skill without your business context is a commodity — anyone could build the same thing. A skill with your voice, your audience, your positioning baked in? That's yours. And the output reflects it.

In this video, we're going to create a brand context layer that any skill can pull from. Three files. Maybe 15 minutes of your time. And everything your skills produce from here on out will sound like you instead of like AI.

### The Three Files (0:00–3:30)

Here's the approach. We're going to create a shared folder called `brand-context` that lives alongside your skills. Any skill that needs to know about your brand can point to this folder and pull what it needs.

> [SCREEN: file browser — creating the brand-context folder]

Three files. That's all you need to start.

**File one — voice-tone.md.**

> [SCREEN: editor — creating voice-tone.md]

This describes how you communicate. Not an essay. Just a few bullet points.

```markdown
# Voice & Tone

- Conversational and direct. No corporate speak.
- Confident but not arrogant. Show don't tell.
- Uses real examples instead of theory.
- Contractions always. Sentence fragments are fine.
- Never says "leverage," "utilize," "in order to," or "it's important to note."
```

That's it. Five bullets. Takes two minutes to write if you know how you talk — and you do. You might not have written it down before, but you know the difference between something that sounds like you and something that doesn't.

**File two — visual-style.md.**

> [SCREEN: editor — creating visual-style.md]

This is your visual identity. Colors, fonts, imagery preferences.

```markdown
# Visual Style

- Primary: #1a1a2e (dark navy), #e94560 (accent red)
- Secondary: #f5f5f5 (light gray), #16213e (deep blue)
- Fonts: Inter for body, Space Grotesk for headings
- Imagery: clean, modern, minimal. No stock photos.
- Logo: stored in assets/logo-dark.svg and assets/logo-light.svg
```

If you have actual brand guideline PDFs, logos, or font files, you can put those in an assets folder too. We'll show a more advanced approach in a minute where Claude extracts this stuff directly from your files.

**File three — messaging-pillars.md.**

> [SCREEN: editor — creating messaging-pillars.md]

These are your core messages. The three or four things that everything you create should tie back to.

```markdown
# Messaging Pillars

1. AI makes you more productive — not by replacing you, but by handling the repetitive parts.
2. Anyone can learn this — you don't need a technical background.
3. Show, don't tell — demonstrate with real workflows, not abstract advice.
4. Build systems, not one-offs — everything should compound over time.
```

Again — you know these. You've just never written them down in a file Claude can read.

### Connecting It to a Skill (3:30–5:30)

Now. These files exist but no skill is using them yet. We need to connect them.

> [SCREEN: the research skill's skill.md open in editor]

I'm going to add a section to our research skill. Right after the process steps, before the guardrails.

```markdown
## Context

When generating output for this skill:
- Read `brand-context/voice-tone.md` and match the tone in all written output.
- Read `brand-context/messaging-pillars.md` to ensure topic selection
  and framing align with core messaging.
- Visual style is not needed for research briefs — skip it.
```

That last line matters. Remember progressive disclosure — we're telling Claude which context to load and which to skip. A research brief doesn't need your color palette. A slide deck skill would. By being explicit, you keep the context lean.

Now let me run the same research prompt as before — same topic, same skill — but with the brand context connected.

> [SPLIT: left — research output without brand context | right — same prompt with brand context]

Left side — the research brief from before. Good information. Generic tone. Could be for anyone.

Right side — same information, but the framing is different. The topic analysis is through the lens of my messaging pillars. The language matches my voice. The bottom-line verdict uses the kind of direct phrasing I'd actually use.

Same facts. Different feel. That's brand context at work.

### The Brand Applicator Approach (5:30–8:00)

Now what I just showed you is the lightweight version — write three markdown files and point to them. For most people, that's enough.

But there's a more powerful version if you have actual brand assets — logo files, font files, a brand guideline PDF. You can build a standalone brand applicator skill that any other skill can call.

> [SCREEN: a folder with brand assets — logos, fonts, a brand-guide.pdf]

I've got a folder here with my brand assets. Logos in SVG, font files, and a brand guidelines PDF.

I'm going to point Co-work at this folder and tell Skill Creator to build a brand skill from it.

> [TYPE: /skill-creator]

> [TYPE: "Build a brand applicator skill from the assets in this folder. Extract my color system, typography, logo placement rules, and create a skill that any other skill can invoke to apply my branding to any output — documents, presentations, HTML, PDFs."]

Skill Creator reads the brand guideline PDF. It extracts hex codes, approved color pairings, font stacks, logo usage rules, spacing values. All of it. Way deeper than what I could write in a few bullet points.

> [SHOW: the generated brand skill — skill.md with brand rules, references with extracted color systems, assets with the logo files]

Look at what it built. It's got a complete color system with approved pairings — "if the background is dark navy, use lime text for foreground." Typography rules — which font for headings, which for body, minimum sizes. Logo placement — where it goes in different contexts. Even output recipes for how to apply the brand in HTML versus PDF versus a React dashboard.

This is a skill that other skills can call. So your invoice skill generates an invoice and then passes it through the brand applicator. Your slide deck skill builds the slides and then applies your brand. Your proposal skill drafts the content and then brands it.

The brand applicator becomes a layer that sits on top of everything.

### The Insight (8:00–9:00)

And here's the thing to understand about why this works. A skill is a craft applied to knowledge. A copywriter knows how to write a great sales email — that's the craft. You give them information about your product and they apply their craft to that knowledge. The result is a great email about your product.

Skills work the same way. The research skill is the craft — it knows how to research well. Your brand context is the knowledge — it knows your voice, your audience, your positioning. Combine them and you get research output that's both well-structured AND sounds like you.

Every skill you build from here on out should reference your brand context where relevant. And because it's in a shared folder, you only write it once. Update your brand? Update the files. Every skill benefits immediately.

### Keeping It Lean (9:00–10:00)

One thing to watch for. Don't dump your entire brand bible into these files. Remember — everything in a reference file costs tokens when it loads. Your voice-tone.md should be 10-20 lines, not 200. Your messaging pillars should be 3-5 pillars, not a manifesto.

If you need more depth for specific skills — like the brand applicator needs detailed color pairings but the research skill just needs your voice — split it up. Keep the commonly-used stuff in the main files and put specialized detail in skill-specific reference files.

The principle from the anatomy video still applies: point, don't dump. Your brand context is a set of reference files, and each skill should only load the ones it needs for the current task.

### What's Next

Your skills now have your brand baked in. But what about other people's skills? In the next video, we're going to grab a popular skill from a marketplace, diagnose why it's probably badly structured, and refactor it into something that actually works well — and connects to your brand context.
