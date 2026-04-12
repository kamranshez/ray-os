---
date: 2026-04-09
status: scripting
---

> **Example artifact:** `agentic-coding-school/tasks/cc-curriculum-reorder.html` — content-flow reorder of all 132 Claude Code course videos, side-by-side before/after view built from 10 parallel transcript-dependency subagents.

## Hook (0:00-0:30)

Most people use Claude Code like a text editor. Type a prompt, get code back, paste it somewhere. But what if Claude could build you a live UI, serve it in your browser, and then read back what you did in that UI to change your actual project?

That's the interactive artifact loop. And once you see it, you can't go back to prompting.

## The Pattern (0:30-2:00)

Here's the core idea in one sentence: Claude generates an HTML file, serves it with Bun's hot-reloading server, you interact with it in the browser, and your interactions write to a JSON file that Claude reads back.

**The loop:**
1. Claude writes an HTML file + a Bun server (`bun --hot run server.ts`)
2. Server goes live on localhost, you open it in Chrome
3. You click, type, drag, whatever the UI needs
4. Every interaction POSTs back to the Bun server, which writes to a JSON file
5. You hit "Copy to Claude" (top-right button), paste it back. Claude reads the JSON and applies the changes.

The key ingredient is `bun --hot`. Not the browser HMR you know from Vite or Next. This is server-side hot reload. Bun 1.0 shipped it in September 2023. When you save server.ts, the module re-evaluates without killing the process. No reconnect, no port conflict. Claude edits the server while you're using it.

**Important pattern:** every artifact that generates output for Claude needs a "Copy to Claude" button in the top right. That's the bridge. The user interacts, the JSON accumulates, one click copies a prompt with the JSON path, paste it back into Claude Code. That's the full loop.

## Why Bun (2:00-2:45)

Why not just use Node? Three reasons:

1. **`bun --hot`** gives you server-side hot reload with zero config. Node needs nodemon or tsx watch, plus you lose state on restart.
2. **`Bun.serve()` + `Bun.file()` + `Bun.write()`** is your entire server in one import. No express, no fs promises, no middleware.
3. **Speed.** Bun starts in under 50ms. When Claude is generating and restarting servers in a loop, that matters.

The Adam Silverman demo from the Anthropic webinar showed exactly this pattern.

## Demo 1: Design Variations (2:45-4:30)

Starting with the simplest possible example. You want to see 4 different hero section designs side by side and pick one.

> "Build me an interactive artifact that shows 4 variations of my hero section. Different layouts, different emphasis. Serve it with Bun. Let me click the one I like. Save my choice to choice.json."

Claude generates an HTML page with 4 rendered variations of your hero. Different headline sizes, different CTA placement, different visual hierarchy. You click the one that feels right. Hit "Copy to Claude" in the top right. Paste it back. Claude applies that design to your real component.

No Figma. No mockup. No describing what you want in words. You just pointed at it.

## Demo 2: Eisenhower Matrix (4:30-6:00)

Now something everyone can use, not just developers.

> "Build me an interactive Eisenhower Matrix. Four quadrants: urgent+important, important+not urgent, urgent+not important, neither. Let me type tasks and drag them between quadrants. Save to tasks.json."

Claude builds it. You type "record video on artifacts", drag it to Important + Not Urgent. "Reply to sponsor email" goes to Urgent + Important. Drag things around until your week makes sense.

Hit "Copy to Claude" in the top right. Now Claude has your prioritized task list as structured data. Ask it to generate a daily schedule, a markdown todo list, whatever you need.

The wow here: Claude just built you a full productivity app in 30 seconds. And it's not a screenshot. It's live, it's interactive, and it feeds back.

## Demo 3: Color Palette Remixer (6:00-7:30)

This is the visual showstopper.

> "Extract my Tailwind color palette and build an interactive remixer. Sliders for hue, saturation, lightness. Show my actual components updating in real-time. Save the final palette to palette.json."

Claude reads your Tailwind config, pulls every color, renders sliders. You drag the primary hue slider and watch your entire site shift from emerald to blue to purple. Adjust saturation. Dial down lightness for a moodier feel. See your actual buttons, cards, and text update in an iframe preview.

Hit "Copy to Claude" in the top right. Claude rewrites your tailwind.config with the new palette.

This is the thumbnail moment. Sliders moving, colors shifting, everything updating live.

## Demo 4: Customer Journey Mapper (7:30-9:00)

Now something for the business side.

> "Build me a customer journey mapper. Timeline from first visit to purchase to renewal. Let me drag touchpoints onto the timeline: landing page, email sequences, checkout, follow-up emails, onboarding. Mark each as positive, neutral, or negative. Save to journey.json."

Claude builds a visual timeline. You drag "Welcome email" to day 1. "Checkout abandoned" email at day 2. "Recovery follow-up" at day 3. "Onboarding sequence" at day 7. "6-week check-in" at day 42. Mark each touchpoint as positive or negative based on what you know about your funnel.

Now you can see your entire customer experience laid out spatially. Where are the gaps? Where do you have 3 emails in 2 days and then silence for a month? 

Hit "Copy to Claude" in the top right. Paste it back. Ask Claude to identify the gaps, suggest new touchpoints, or draft the emails you're missing.

## Quick Demos: Font Pairing + Animation Curves (9:00-10:30)

Two more fast ones to show the range.

**Font Pairing Explorer:** Claude loads 20 Google Fonts, renders your actual headings and body text with every combination. A grid of pairs. Click the one that looks right. "Copy to Claude" in the top right. Claude updates your font config. 10 seconds to find a font pairing that would take an hour of Googling.

**Animation Curve Editor:** Claude extracts all your Framer Motion animations and renders them on a visual timeline. Drag keyframes. Adjust bezier easing curves. Preview the animation in real-time. "Copy to Claude" in the top right. Claude updates the motion components. You just edited animations without writing a single `transition` property.

## The Pattern Is Infinite (10:30-11:30)

Every one of these follows the same loop. HTML + Bun server + JSON bridge + "Copy to Claude" button in the top right.

Here are more you could build in 60 seconds:

- **Database Schema Designer** — Interactive ERD. Drag tables, draw relations, add columns. Claude generates migrations.
- **Form Builder** — Drag field types onto a canvas, set validation rules. Claude generates the component + Zod schema.
- **Permission Matrix** — Roles x resources grid. Click cells to toggle access. Claude generates RBAC middleware.
- **Cron Schedule Timeline** — All your scheduled tasks on a 24-hour clock. Drag to reschedule. Claude updates the config.
- **HTML Slide Deck Builder** — Drag content blocks, pick a visual style, reorder slides. Claude generates a presentation. Meta: you could build the slides for this video with the pattern from this video.

The artifact doesn't have to be code-related. It's just a UI that writes JSON. Claude reads JSON. That's it.

## Why This Matters (11:30-12:30)

This is a fundamental shift. Instead of describing what you want in text, you're showing it. Instead of a prompt, it's a GUI. And the feedback loop is instant because Bun's hot reload means Claude can iterate on the artifact itself while you're using it.

Think about what this means. Any time you find yourself writing a long, detailed prompt trying to describe exactly what you want, you could instead say: "Build me a UI where I can just show you."

And you can build one of these in about 60 seconds.

---

## Production Notes

- Record demos live, don't cut. Show Claude generating both files in the terminal.
- Browser and terminal side by side for all demos.
- For Color Palette Remixer: zoom in on the sliders. That's the money shot for the thumbnail.
- Every artifact must show the "Copy to Claude" button in the top right. Emphasize this is the pattern. The bridge between GUI and AI.
- End on the slide deck meta moment if possible: "these slides were built with the pattern I just showed you."
- Demo sequence builds: simple pick (Design Variations) → drag-and-drop (Eisenhower) → live sliders (Color Palette) → business mapping (Journey) → rapid fire (Font + Animation)
- Reference: Anthropic webinar (Casey, Tarek, Adam) where Adam demos this pattern
- Link to class in description: masterclaudecode.com
