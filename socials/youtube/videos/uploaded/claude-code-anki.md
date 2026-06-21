---
tags: [youtube, script, claude-code]
status: talking-points
date: 2026-06-20
---

# Claude Code + Anki — Talking Points

> Talking points / outline only (per Ray's request), not a word-for-word script. Structured on the channel's proven formula so it's ready to expand into a full script later. **Open decisions to lock before scripting:** coined term (candidates below), pitch goal (masterclass vs newsletter), demo surface.

## Title candidates
1. *Claude Code Quietly Fixed My Anki Decks* (bold claim + personification)
2. *I Gave Claude Code Access to Anki and It Rewrote My Worst Flashcards* (bold claim + specificity)
3. *The Anki Setup Nobody Is Talking About* (curiosity gap + exclusivity)

## Coined-term candidates (pick one and hammer it)
- **"Card debt"** — like tech debt, but for your deck. Stale, too-hard, duplicated, confusable cards silently pile up and you blame *yourself* for failing them. Claude Code pays it down. *(Recommended — names an invisible pain everyone feels.)*
- **"Self-healing deck"** — the deck reads its own failure log and repairs itself.
- **"Leech surgery"** — the specific act of operating on the cards you keep failing.

---

## 1. Hook (discovery framing, first 20-30s)
- Discovery beat: "I was making Anki cards for [Japanese / chess] the slow way, and I realized Claude Code could just... do all of it. Not just *make* cards — *fix* the ones I keep getting wrong."
- What it is, one sentence: Claude Code talks to Anki over a tiny local API (AnkiConnect) and can read your whole review history, so it can build, edit, and repair cards programmatically.
- The reframe: it's not a card generator. It's a **tutor that watches you fail and re-teaches you.**
- *Visual: the chess board card rendering live in Anki, flip to reveal the move highlighted. Lead with the finished artifact in the first 10s (improvements.md #2).*

## 2. Name the invisible problem (the "card debt" beat)
- Everyone's Anki deck rots. You have cards that are too hard, worded badly, near-duplicates, or that you mix up with another card. You just suffer through them and assume you're the problem.
- Old workaround: you *know* you should rewrite your leeches, but editing cards by hand is so tedious nobody ever does it. So card debt compounds forever.
- New solution: Claude reads the review log, finds the rot, and fixes it in place. **This is the half of the video nobody else shows.**

## 3. The backbone — how it actually connects (keep short, concept-first)
- **AnkiConnect**: a local HTTP API on `localhost:8765`. Claude POSTs JSON to create decks, note types, cards, media.
- **The SQLite DB** (`collection.anki2`): Claude can read your full review history directly — every lapse, every interval, every card you keep failing.
- Human analogy: AnkiConnect is the *hands*, the review DB is the *eyes*. Together = a tutor that can both write on the board and watch you struggle.

## 4. Deep dive — two halves of the loop

### A) Generation (the familiar half — go fast)
- **PDFs / textbooks / papers** → atomic cards. (Ray flagged this as important.)
- **YouTube videos** → cards from the transcript + frame grabs at the right timestamps.
- **Docs / codebases / error messages** → the dev-native angle: turn the stuff you keep re-Googling into cards.
- **Daily routine** → the auto-pipeline (Ray's Japanese setup: everything you watched today becomes cards tonight).
- It can also generate its own diagrams/screenshots onto the card.

### B) The closed feedback loop (the hero half — slow down here)
This is where "card debt" gets paid down. Claude reads *why* you fail, not just *that* you fail:
- **Leech surgery** — find high-lapse / low-retention cards, diagnose why they're hard, rewrite them easier.
- **Laddering** — when you fail a hard card because an intermediate concept is missing, auto-insert the easier rungs beneath it. *(Show: fail a card → 3 simpler cards appear under it.)*
- **Confusable pairs** — detect the cards you mix up (failed together, similar answers) and write explicit contrast cards. *(Ray's favourite — the sleeper hit. "Claude reads why you fail, not just that you fail.")*
- **Hint ladder** — instead of rewriting a leech, inject progressive hints so it gets a soft on-ramp.
- **Example diversification** — a fact memorized from one example is context-bound; Claude adds varied examples so recall generalizes.
- **Difficulty calibration** — flag cards that are now trivially easy (wasting reviews) to bury, stale ones to suspend.
- **Atomicity refactor** — split a bloated wall-of-text card into atomic cards (minimum information principle). Great before/after.
- **Semantic dedup** — Anki's built-in find-duplicates is exact-match only; Claude catches *near*-duplicates by meaning.

## 5. Interactive HTML cards (the "wow" segment)
- Key myth-bust: **you don't need a special add-on.** Anki cards are webviews, so a raw `<script>` tag just runs.
- The one real constraint — persisting state from front to back — is solved by `sessionStorage` (Anki 2.1.50+, desktop + AnkiDroid) or the **Anki-Persistence** library everyone builds on.
- Modern toolkit to name-drop: **AnkiEco** (ready MCQ / cloze / match templates, Mermaid + math, even an embedded Tldraw whiteboard).
- Ray's own proof: the Japanese shadowing card hits the AnkiConnect backend from inside the card. *That's* the mechanism people get stuck on — say it out loud.

## 6. The live demo we built — chess openings (show this end to end)
- Built a brand-new note type **"Chess Opening (Interactive)"** entirely over AnkiConnect — nothing installed but the add-on.
- Fields: `Opening / FEN / Move / UCI / Idea`. The board is drawn by JavaScript *inside the card* from the FEN string. No external page, no screenshot — it renders in the real reviewer and syncs to your phone.
- Front: position + "find the key move." Flip: board redraws with the move played, from-square glows yellow, destination green, plus the idea.
- Four "killer opening" cards: **King's Gambit (f4), Evans Gambit (b4), Fried Liver (Nxf7!), Smith-Morra (c3).**
- The point that lands: a custom note type *and* generated cards, created end to end by Claude. To add another opening you just give it a FEN and a from-to move like `g5f7`.

## 7. The "Ray thinks deeper" move (subscribe moment)
- Reframe Anki itself: **it's just a scheduling engine.** The spaced-repetition algorithm is the product; the UI is yours to build. Strip the sync engine, put any frontend on top (shadowing, a custom dashboard, a chess trainer).
- Broader trend: AI doesn't just *generate* study material — it closes the loop by reading your performance and adapting. Spaced repetition was always waiting for a tutor that never gets tired. That's the actual unlock.

## 8. Takeaway (brief)
- Install AnkiConnect, keep Anki open, point Claude Code at it.
- Start with one thing: have it turn a PDF or a YouTube video into cards tonight.
- Then the magic move: "Claude, look at my review history and fix my 10 worst cards."

---

## Pitch layer (decide when scripting — do NOT stack both)
- If **masterclass**: soft anchor ~1:30, closing urgency pitch tied to "build your own AI-augmented learning system." Needs a real deadline + price.
- If **newsletter**: single clean close, named free artifact (candidate: a downloadable "Claude + Anki" starter skill / the chess note-type `.apkg`).
- Apply pacing #1 (50% slower, let the board linger) and visual hook #2 (open on the rendered card).
