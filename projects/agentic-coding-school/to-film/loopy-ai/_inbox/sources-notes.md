---
tags: [loopy-ai, inbox, sources, apple-notes]
date: 2026-05-28
status: inbox
---

What the Apple Notes search turned up. Pulled via AppleScript across 683 notes, filtered to titles containing goal / ralph / loop / workshop / mission / autoresearch. 17 matched (most are bookmark notes holding a single X link), plus one screenshot note.

## Notes that are just X bookmarks

These were one-line notes saving a link "for the workshop" / "for loopy AI class". All fetched and summarised in [[sources-x]]:

- "Good goal prompt" -> zeeg
- "For effective goals" -> gdb
- "For the workshop. Also check with Grok for other skills" -> ericzakariasson
- "For workshop" -> kappaemme1926, raberhalex
- "For the workshop" -> steipete, nexxeln
- "For the Workshop / Loop AI / For loopy AI class" -> jarrodwatts + kingbootoshi, and "Prototypes as Specs" -> DavidKPiano
- "For the workshop class" -> cheddarmandem

(Several appear twice as duplicate notes.) Ray's own tag in two notes: **"Loop AI"** / **"For loopy AI class"** confirms jarrodwatts + kingbootoshi as the seed for this class.

Also note: "Also check with Grok for other skills" appears twice — an open to-do to mine Grok for more loop/skill ideas before scripting.

## The WatchLLM goal example (note title: "Goal")

A real, full `/goal`-style objective Ray wrote for building WatchLLM (a Promptwatch-style product). Worth keeping as a *worked example* of a well-structured goal prompt for the class. Shape:

- **Goal** — one sentence naming the outcome and the source of truth.
- **Scope** — bullet list of what's in (real app logic, data models, APIs, jobs, UI) and what's allowed as fallback (seeded/demo data only where real integrations aren't safe).
- Explicit "avoid paid/external/OAuth/production actions unless approved; provide safe local fallbacks."
- "Regularly spawn verifier subagents" to click around the local app and compare against the live reference.
- **Execution** — numbered phases: audit -> implementation map with milestones/dependencies -> build slices in dependency order -> per-slice schema/logic/tests/verification -> verify locally -> compare to reference -> final requirement-by-requirement report.
- **Success** — concrete, checkable end states (app runs locally, core loop works end to end, dashboard powered by real data, REST validation works, browser verification proves flows).

This maps almost one-to-one onto Avi Chawla's 9-section template (GOAL / SCOPE~CONSTRAINTS / PLAN / VERIFY / DONE-WHEN). Use it as the "here's one I actually ran" example.

## Screenshot note

"[To Record] Autoresearch for Non Technical Task" — contains only a screenshot (base64 image), no text. A to-record reminder: show autoresearch applied to a non-technical task. Open in Apple Notes to see the image when scripting that segment.
