---
tags: [loopy-ai, inbox, sources, apple-notes]
date: 2026-05-28
status: inbox
---

What the Apple Notes search turned up. Two passes over all 683 notes via AppleScript:

1. **Title pass** — titles containing goal / ralph / loop / workshop / mission / autoresearch. 17 matched (mostly one-link bookmark notes).
2. **Body pass** — full body export, grep + a 4-way Haiku-explorer sweep of every note. This caught notes whose *body* is relevant but whose *title* isn't (e.g. "To Do for Class", "Auto research"). Notes 342-683 had nothing relevant (business/marketing); all loop material sits in the low-numbered notes.

## Notes that are just X bookmarks (title pass)

One-line notes saving a link "for the workshop" / "for loopy AI class". All fetched and summarised in [[sources-x]]:

- "Good goal prompt" -> zeeg
- "For effective goals" -> gdb
- "For the workshop. Also check with Grok for other skills" -> ericzakariasson
- "For workshop" -> kappaemme1926, raberhalex
- "For the workshop" -> steipete, nexxeln
- "For the Workshop / Loop AI / For loopy AI class" -> jarrodwatts + kingbootoshi, and "Prototypes as Specs" -> DavidKPiano
- "For the workshop class" -> cheddarmandem

(Several appear twice as duplicate notes.) Ray's own tag in two notes: **"Loop AI"** / **"For loopy AI class"** confirms jarrodwatts + kingbootoshi as the seed for this class.

Also: "Also check with Grok for other skills" appears twice — an open to-do to mine Grok before scripting.

## Notes the body pass added (missed by the title pass)

Summarised and fetched in [[sources-x-batch2]] and [[autonomy-ladder]]:

- **"To Do for Class"** (note 1) — the richest miss. Holds /goal links (dani_avila7, chrishayduk, mweinbach), the "Goal In, Strategy Out" video, code-review-with-debates links, and idea seeds: "workflows that reset the context window", "Verification Loop", "Scratchpadding as a way to survive context resets".
- **"Auto research"** (note 250) — Aakash Gupta's "6 levels of autonomous Claude Code" ladder. Best spine candidate, see [[autonomy-ladder]].
- **"Class: Don't Stay Up to Date"** (note 199) — a class-idea note; argues you don't need to chase every update because Claude/Codex absorb what's useful (planning, skills, memory). Mentions stop-hooks for long-running work becoming obsolete once Codex 5.2 shipped. Adjacent class idea, not core loop content, but worth keeping.
- **"Set up a system for regularly finding posts ... around the clock on auto pilot"** (note 174) — a background autonomous-loop use case (LinkedIn link).
- **"Class: Adversarial Agents"** (note 200), **"Use subagents as a way of separating pipelines"** (note 305), **"[Video] Prompting Opus 4.7"** (note 177) — adjacent, likely other classes (review / subagents / prompting). Links in [[sources-x-batch2]] Tier 3.
- **"For class :: Playwright"** (note 133) — gap analysis listing an "agentic QA testing loop: Claude runs Playwright, reads test failures, and self-fixes bugs" (write-test-fix cycle). A concrete verification-loop demo idea, though framed for a Playwright/QA class.

## The WatchLLM goal example (note title: "Goal", note 3)

A real, full `/goal`-style objective Ray wrote for building WatchLLM (a Promptwatch-style product). Keep as a *worked example* of a well-structured goal prompt. Shape:

- **Goal** — one sentence naming the outcome and the source of truth.
- **Scope** — what's in (real app logic, data models, APIs, jobs, UI) and allowed fallbacks (seeded/demo data only where real integrations aren't safe).
- Explicit "avoid paid/external/OAuth/production actions unless approved; provide safe local fallbacks."
- "Regularly spawn verifier subagents" to click around the local app and compare against the live reference.
- **Execution** — numbered phases: audit -> implementation map -> build slices in dependency order -> per-slice schema/logic/tests/verification -> verify locally -> compare to reference -> final requirement-by-requirement report.
- **Success** — concrete, checkable end states (app runs locally, core loop works end to end, dashboard powered by real data, REST validation works, browser verification proves flows).

Maps almost one-to-one onto Avi Chawla's 9-section template (GOAL / SCOPE~CONSTRAINTS / PLAN / VERIFY / DONE-WHEN). Use it as the "here's one I actually ran" example.

## Screenshot note

"[To Record] Autoresearch for Non Technical Task" (note 71) — only a screenshot (base64 image), no text. A to-record reminder: show autoresearch applied to a non-technical task. Open in Apple Notes to see the image when scripting that segment.
