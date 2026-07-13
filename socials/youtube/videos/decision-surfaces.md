---
tags: [youtube, script, claude-code, planning, representations, fable]
status: draft
date: 2026-07-13
source: "Bret Victor's Humane Representation of Thought talk + months of canvas-surface iteration with Fable on HyperWhisper's iOS onboarding plan"
---

## Title Options

| # | Formula | Title |
|---|---------|-------|
| 1 | Urgency + directive | Fable 5 Is Disappearing. Learn This Loop First. |
| 2 | Urgency + curiosity | What I Built With Fable 5 Before It Leaves |
| 3 | Identity shift + curiosity | Stop Reading AI Plans. Stand On Them Instead. |

Coined term: **"decision surface"**. Format: Tier 3 strategy/identity claim wearing a Tier 1 urgency wrapper (Fable 5 leaving paid plans), with a live full-loop demo on HyperWhisper and a free skill giveaway on GitHub. Pitch: woven soft-hard sell at the first concept boundary, framed as getting ahead and learning faster than everyone else via Agentic Coding School (2,000 engineers, months ahead of the curve, no deadline or price mechanics). Confirm `[DATE]` for Fable's departure before filming.

Delivery note: bullets are talking cues, riff over them. Lines in quotes are worth saying close to verbatim.

---

## Hook (0:00-0:40)

*On screen from second zero: the Fable 5 deprecation notice or model picker showing it leaving. Then a hard cut to the finished canvas, slowly panning. No branding, no intro.*

- "Fable 5 leaves the paid plans on `[DATE]`." Before it goes: the highest-leverage thing I've been using it for.
- Who's actually pulling ahead with AI right now: not better prompts, richer and higher-quality **decisions** with the models.
- Past couple of days, that's what Fable has been for me: "a machine for designing richer decision surfaces."

---

## Decision Surfaces (0:40-2:30)

*On screen: the term DECISION SURFACE typed large, then the examples appearing as split panels.*

- Coin the term: "A decision surface is the representation you're looking at in the moment you make a call." Not the info itself, the form it takes when it hits your eyes.
- You already believe this, just not for planning:
	- Generals: map table, not a stack of reports.
	- Chess players: set up the board, never review from notation. The fork is invisible in text.
	- "Same information. Different surface. Different blunders caught."
- The claim: "a wall of markdown is one of the worst decision surfaces ever invented", and it's the one you approve every plan on.
- Bret Victor, 2014, The Humane Representation of Thought:
	- Great leaps in thinking = new representations. Arabic numerals over Roman. Algebraic notation over paragraphs.
	- His problem back then: new representations were expensive. A custom diagram cost days, so everything defaulted to cheap text.
- That constraint just died, and Fable killed it for me. Interactive representation of anything in minutes.
- "You're no longer choosing the cheap option. You're just choosing the bad one out of habit."

> 🎨 DRAW `decision-surfaces-markdown-wall-hidden-flaw`: a tall wall of markdown text with one line glowing faint red, invisible unless you squint, versus a map table and a chessboard where the same flaw sits exposed in the open

![[decision-surfaces-markdown-wall-hidden-flaw.png]]

---

## The Plan That Burned Me (2:30-4:00)

*Screen recording: the actual HyperWhisper iOS onboarding, hitting the Test Recording step and failing. Then cut to the plan.md scrolling.*

- Make it concrete: HyperWhisper, my dictation app, iOS onboarding.
- The dead end: fresh install walks into a test recording that cannot succeed. Default mode needs a license the user was never asked for. canRecord says false, onboarding never consulted it.
- "I read that plan. I approved that plan. I missed it." Not careless, it's what the plan **looked like**: a competent wall of markdown, shaped like every plan you've ever approved.
- The fix plan (the one for today's demo): upfront choice, HyperWhisper Cloud vs bring-your-own-key, whole flow branches off it.
	- Cloud lane: activate license, do the test recording.
	- Key lane: skip the test, hand off to settings.
	- Branches, rejoins, five or six real decisions. Exactly what a markdown review fumbles.

---

## Brainstorming Richer Surfaces With Fable (4:00-5:15)

*Rapid montage, about two seconds per file: browser tabs flicking through the mockups folder, sixteen wildly different representations of the same plan, filenames visible. Roughly 45 seconds of b-roll under this narration.*

- What I've been doing for the last couple of months: sitting with Fable, brainstorming richer decision surfaces for this one plan. Same information, sixteen different bodies.
- Rattle a few off over the montage: paged storyboard, blueprint map, review board, diff explorer, playable simulator of the onboarding, RFC, cinematic slide deck, metro map.
- The lesson sixteen attempts teach: "every representation is a choice about which decisions are visible and which are hidden."
	- Deck: gorgeous and useless, one slide at a time hides the whole.
	- RFC: felt rigorous, caught nothing. "The markdown wall wearing a suit."
	- Simulator: you feel the broken flow but the implementation layer disappears.
- One of them was physically different: the spatial canvas. Became a skill, linked below, and you're about to watch it get built from scratch.

> 🎨 DRAW `decision-surfaces-sixteen-representations-grid`: a 4x4 grid of tiny representation thumbnails (deck, RFC, simulator, diff, metro map, canvas...) with most greyed out and the canvas one glowing, labeled by what each one hides

![[decision-surfaces-sixteen-representations-grid.png]]

---

## The Demo (5:15-6:00)

*On camera: Claude Code open, Fable selected as the model. Type the prompt live, spoken verbatim.*

- Real plan, running on Fable. Read the prompt as typed, verbatim:

"Take plans/ios-onboarding-redesign.md and put the entire plan on one spatial canvas I can pan and zoom. Phone mockups in a top band. Each stage's before and after diagram directly beneath it. Branches as tinted lanes with fork and rejoin wires. Every decision and open question as a sticky note placed next to the stage it affects. Double click anywhere should drop a comment sticky, and give me a button that copies all my comments as JSON."

- Send it. Takes a few minutes, and the wait is perfect: there's a story you need for what's about to appear.

---

## Soft Anchor (6:00-6:30)

- While that generates, quick pause. Everything here (the planning workflow, the artifact skills, the loop that applies the review) comes from the systems we build in Agentic Coding School.
- Been talking about decision surfaces and dynamic planning artifacts inside the school for months before this video existed.
- The honest pitch: "if you want to get ahead and learn this stuff before everyone else does, that's what the school is for."
- Proof: in Claude Code twelve hours every single day, people inside are months ahead of the curve, over 2,000 engineers, under 0.2% refunds. Link below. Back to it.

---

## The Same Jump, in 1786 (6:30-7:45)

*Cut to the Playfair chart, the actual 1786 engraving. Hold on it while the generation runs in a corner of the screen.*

- 1786, William Playfair, Scottish engineer, writing a book on England's trade. Mountains of data, and back then data meant tables. "Data and tables were the same concept. Nobody could imagine them apart."
- His observation: people bring one kind of understanding to tables, a totally different set of abilities to maps.
- So he drew a peculiar map: left-right becomes earlier-later, up-down becomes more money, less money. **The first chart ever drawn.**
- Why it worked: it added nothing. Same numbers as the table. "What changed was which of your abilities could reach them." Map-reading brain, a hundred thousand years old, put to work on trade deficits.
- Today the chart underlies all of science and seems too obvious to have needed inventing.
- Land it: "Your AI writes you plans. The plans are tables. Nobody has drawn you the chart."

*Cut back to the terminal: generation finished.*

- "Until now. It's done. Look at what just happened to my plan."

> 🎨 DRAW `decision-surfaces-playfair-table-to-chart`: a table of trade numbers on the left transforming into Playfair's line chart on the right, with a brain icon above each showing "reading" vs "map-reading" being recruited

![[decision-surfaces-playfair-table-to-chart.png]]

---

## Standing On the Plan (7:45-10:00)

*Screen recording: the generated canvas. Fit-to-view first so the whole board is visible, then slow pans. This section is mostly driving the artifact.*

- Walk the board like a map table:
	- Zoom out: entire feature in one field of view.
	- Top band: every phone screen in order. Under each: before and after structure diagrams.
	- Bring-your-own-key branch: tinted lane, forks after the choice screen, rejoins at keyboard setup.
	- Purple stickies: decisions, each with question, answer, reasoning. Yellow: open questions. Out-of-scope pinned at the edge.
- Name the moment: this is the Playfair move happening to you live. Plan became a map, map-reading brain switched on, the lane structure itself starts asking questions. Why does this branch rejoin there? Why does one lane have a test step and the other doesn't?
- "Those questions are invisible in markdown. Not hard to see. Invisible."
- The review pass, live. Double click, drop stickies:
	1. Activation screen has a buy a license button, but no in-app purchase path on iOS. That button is a lie. Cut it or link out.
	2. "I'll do this later" leaves the user on a mode that silently can't record. Surface an explicit blocked reason instead.
	3. Key-users lane ends at a settings handoff but nothing creates their first transcription mode. The lane is missing a step.
	4. On the open-question sticky: nine engine choices during onboarding is too many, confirm the handoff.
- Four stickies, dropped exactly where the ambiguity lives. Hit Copy JSON: every comment exports with its position and nearest stage. Paste into Claude Code, tell it to apply the review to the plan.
- *While it runs*, the Victor beat: in 2014 he said we need programming down from hours to **seconds**, improvising dynamic models mid-conversation, and the room laughed. "You might think that's impossible. Eleven years later that sentence just describes a normal Tuesday."

> 🎨 DRAW `decision-surfaces-canvas-review-loop`: the loop as a circle: canvas → sticky comments dropped spatially → Copy JSON → Claude applies → new canvas, with a small "v6 → v7" tag on the last arrow

![[decision-surfaces-canvas-review-loop.png]]

---

## The Payoff: the Plan Mutates (10:00-11:15)

*Screen recording: the v7 canvas opening next to v6. Side by side, then zoom to the lower lane.*

- New canvas is up. Point at the lower lane: **it grew a stage.** "Create your first mode" now sits between key handoff and keyboard setup, exactly where comment three pointed.
- Buy button gone from activation. "I'll do this later" now routes to an explicit blocked reason. Banner on top: comments one to four applied.
- Sit with it, the whole thesis paying off:
	- The surface showed me four problems that survived my markdown review.
	- Comments were spatial, pinned to the plan, not scattered in a chat thread.
	- Applying them physically changed the shape of the map. Review to structure, one loop, no translation step where meaning gets lost.
- "That broken onboarding shipped because I approved it off a table. This version got fixed because I stood on a chart."

---

## Verdict and the Honest Limits (11:15-13:15)

*Talking head. Canvas idle in the background.*

- Honest verdict, not a victory lap. Three limits:
- **One: small plans, markdown is fine.** A two-file change doesn't need a map table. This earns its keep when a plan grows a branch, a rejoin, or a handful of real decisions. "Don't ceremony yourself to death."
- **Two: my canvas is still a picture, not a model.** Victor's bar is higher:
	- On his surface you'd flip a decision sticky (key-users lane DOES get a test step) and watch the lanes physically rewire to show that world. Mine can't yet.
	- But the decisions are structured data in the file, so toggles are buildable. That's next.
	- Also next: the canvas learning to listen. Voice notes pinned to the board, transcribed locally by HyperWhisper, review a plan by talking at it, eyes never leave the map.
- **Three: this is bigger than planning, I can't stop seeing it.** Data visualisation:
	- Today: ask Claude for a chart, get one static view, one framing somebody chose for you. "A table wearing a chart costume."
	- What I actually want (started prototyping): the model captures more of the data and builds an **interactive** surface. I drag a variable, Claude shows what it believes would change and why, hypotheses attached.
	- "Not a picture of the data. A surface I can interrogate before I decide."
	- Your analytics dashboard deserves that question. Your error tracker too. All designed when representations were expensive.
	- The question for every tool: if this were sixteen times cheaper to re-represent, what would I actually want to look at before deciding? That's a future video.

> 🎨 DRAW `decision-surfaces-everything-is-a-surface`: a row of everyday tools (dashboard, error tracker, spreadsheet, plan doc) each revealed to be sitting on top of the same "decision surface" layer, with a question mark asking what the interactive version looks like

![[decision-surfaces-everything-is-a-surface.png]]

---

## Key Insight

> The information doesn't decide what you can see. The representation does. Playfair didn't add a single number to the table, and I didn't add a single word to the plan. We just changed the surface, and the decisions changed with it.

---

## Close (13:15-14:00)

- "Higher quality decision surfaces, higher quality decisions." Representations now cost minutes, so the surface you review on is a choice, and a wall of text is choosing to miss things.
- Canvas skill on GitHub, linked below, plus the exact demo prompt.
- Voice-notes canvas and decision toggles in progress, newsletter gets them first.
- If Fable's already gone when you watch this: everything works on whatever replaced it. "The surface is the point, not the model."
- Comment ask: what's your worst decision surface, the thing you stare at daily that's a table pretending to be a chart. Collecting them for the follow-up.
- See you in the next one.
