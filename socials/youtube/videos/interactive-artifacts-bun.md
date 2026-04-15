---
date: 2026-04-09
status: scripting
---
![[images/three-layers/excalidraw_3.png]]

> **Example artifact:** `agentic-coding-school/tasks/cc-curriculum-reorder.html`. Content-flow reorder of all 132 Claude Code course videos, built from 10 parallel transcript-dependency subagents. Used as the "this scales" callback inside the rapid fire montage.

## Opening

So recently I've been doing a bunch of Claude Code coaching calls to help organisations use it better. And I think one thing stood out to me, so I figured I'd make a separate video about it. 

And this is the whole idea of interactive artifacts. So I'll be going through the three different layers here in this video. 

## Level 1: Static

>"Extract this component and then give me ten design variations of it and then pick the one that I like and we can put it back in."

This is the floor. A static artifact is already better than a text response, because the information is spatial and glanceable. You see the shape of the journey at once. You would have gotten a bulleted list otherwise.

>"Map the entire customer journey for my product. Every touchpoint from first visit to renewal. The happy path, abandoned carts, churned users, upsell paths, support escalations. Render it as a flow diagram."

Claude writes an HTML file. Opens in Chrome. Spawns subagents that read your PostHog events, your Stripe funnel, your Intercom conversations, your onboarding emails. Every branch of the real journey appears as a node in a flow diagram. Happy path in green, drop-off points in red, unknowns in grey. It looks like a real product.

And it does nothing. You cannot click anything. You cannot comment on anything. It is just a pretty visual of your funnel, already useful on its own because you can already see things at a glance that would take an hour to describe in a doc.

## Layer 2: Interactive

> "Now serve it with Bun. Use `bun --hot run server.ts`. Let me click any node and leave a comment. Save everything to `journey-comments.json` on every interaction."

Claude adds a tiny server. `Bun.serve()`, `Bun.file()`, `Bun.write()`. That is it. No Express, no middleware, no build step. The same page reloads, but now it is alive.

Click any node. A comment box opens. Type "why are we losing 40% of people here?" Click another node. Type "this email is doing nothing, draft three alternatives." Click a grey unknown. Type "do we even track this step?" Every comment saves to `journey-comments.json`. Open the file in another pane and watch it update.

This is the second floor. You now have a real input surface for commenting on the journey. The JSON is your output. But the JSON just sits there until someone reads it.

Cue the "Copy to Claude" button in the top right. Every interactive artifact gets this button. One click copies a prompt with the JSON path, you paste it into Claude Code, Claude reads the JSON, writes the insights memo, commits. This is already a massive upgrade over prompt-and-paste, and for a lot of artifacts this is all you need. Fast, explicit, no extra moving parts.

But there is a richer version when you want Claude reacting to you live.

Can use this

> **Curriculum reorder (132 videos).** Same pattern, scaled up. 10 parallel subagents read every transcript to build the dependency graph before the UI even loads. Drag lessons into a new order. Claude rewrites the curriculum.

>**Stripe pricing simulator.** Sliders and a tier composer over your live Stripe data. Pick a scenario. Claude updates products, rewrites the pricing page, adjusts feature gates in code, queues grandfathering emails.

## Layer 3: Channels loop

> "Wire up an MCP channel. Every time `journey-comments.json` changes, push the delta to Claude. Have Claude react live: pull the cohort analysis for any node I ask about, draft the emails I request, propose the tracking code, and render the results back into the diagram."

Reference: https://code.claude.com/docs/en/channels-reference

Now the loop closes automatically. The Copy to Claude button is still there, still works, still useful when you want an explicit handoff. But you do not need it to trigger the feedback anymore. Every comment streams back to Claude through the MCP channel. Claude is listening.

And Claude's answers come back *into the diagram itself*. Your "why are we losing 40%" comment gets answered with a cohort analysis rendered under that node. "Draft three alternatives" gets three email drafts as cards under the node. "Do we track this" gets a PostHog query result or a proposed tracking plan with the exact code to add.

You walk through the diagram leaving comments. Claude walks behind you doing the research and the drafting. By the time you finish the map you have a full audit, a set of drafts, and a tracking plan. No separate tabs, no lost context, no "let me go find that data".

This is the interaction Adam named in the Anthropic webinar: click on anything Claude sent you, leave a comment, Claude intercepts it and acts.

This is the point of the pattern. You are interacting with a visual tool, and Claude is doing real work in your project the whole time, out of your way but inside the loop.

**Stripe churn investigator.** Last 30 cancellations as cards. Group and tag with hypotheses. Claude drafts win-back emails per cluster and writes an insights memo.

> Having it do deep research and then seeing what's happening live in a nice UI front end, and then being able to direct it from there. 

### Why Bun

`bun --hot` gives server-side hot reload with zero config. When Claude edits `server.ts`, the module re-evaluates without killing the process. Your session stays intact. `Bun.serve()` plus `Bun.file()` plus `Bun.write()` is your entire server in one import. Bun starts in under 50ms, so the iteration loop feels instant.

### The dual-mode insight

Every artifact is doing two jobs at once.

One, it is a UI that captures your decision. You clicked a node on the journey map and left a comment. That is data.

Two, it is a conversational surface where you can edit the tool itself in the same breath. "Hey Claude, colour the churned-user nodes by cancellation reason, and by the way add a filter for paid users only." Claude edits `server.ts` to add the filter, updates the node renderer to pull the cancellation reasons from Stripe. Bun hot reload applies the server change. Your session keeps going. You did not stop working.

This is what Adam from the Claude Code team called "flying" in the recent Anthropic webinar. You stop switching between "I am building the tool" and "I am using the tool". Claude handles both sides at once.

![[images/dual-mode-insight/excalidraw_3.png]]
![[images/dual-mode-insight/excalidraw_4.png]]
## Rapid fire: the pattern is infinite

Every one of these follows the same three-layer shape. Static, interactive, channels.

- **Inbox triage board.** Gmail as a Kanban. Drag emails into reply, archive, snooze. Claude drafts every reply in your voice and executes.
- **Class outline whiteboard.** Sticky notes for every Agentic Coding School lesson, dependency arrows. Drag to reshape. Claude rewrites the course manifest and generates shot lists for flagged lessons.

The artifact does not have to be code-related. It just has to be a UI that writes JSON, streamed back through a channel. Claude reads it. Claude acts. That is it.

## Close

This is a different relationship with Claude.

Instead of describing what you want in paragraphs, you show it. Instead of pasting JSON back, Claude reads the JSON itself. Instead of stopping to change the tool, you tell Claude to change the tool while you keep using it.

You interact with Claude visually and richly. Claude does the work behind the scenes.

Any time you catch yourself writing a long prompt trying to describe what you want, stop. Say: "build me a UI where I can just show you, and wire it up with a channel so you can act on what I do."

---

## Production notes

- Link the MCP channels docs: https://code.claude.com/docs/en/channels-reference
- Link to class in description: masterclaudecode.com 