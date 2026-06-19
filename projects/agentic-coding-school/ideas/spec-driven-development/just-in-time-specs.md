---
class: "spec-driven-development"
chapter: "Just-In-Time Specs"
status: "idea"
---

Stub — the counterweight to [[specs-are-the-new-product]]. That segment says quality enters upstream, in the spec. True. This one says: don't mistake that for *spec everything up front*. Spec to the depth of your next confident step, let the spec co-evolve with the code, and push every discovery back into the repo so the next pass inherits it. Big-design-up-front is waterfall whether a human or a model writes the doc.

> **The one-line rule:** Spec the next confident step, not the whole system — and let the spec keep changing as the code teaches you what you meant.

## Thesis

"Specs are the new product" is correct and easy to over-apply. The instant you believe quality lives in the spec, the temptation is to write *all* of it before any code exists. That's the same trap as pre-sequencing a backlog: you freeze a plan at the moment of least knowledge. The downstream sections of a big spec are written in maximum ignorance — before a single line constrains them — so they're the parts most likely to be wrong, and you rewrite them anyway.

Chris Parsons (30-year engineer, ex-agency-CEO, agile consultant) is openly wary of spec-driven tooling for exactly this reason. His worry isn't specs — it's specs that *fossilise*: a tool that bakes "write the full spec first" into its workflow drags you back to the 1990s, and worse, locks in a process tuned to whatever the models could do the day you wrote it. His preferred shape is **just-in-time specs**: plan one feature deeply right before you build it, then let the next feature's spec be informed by what the last one taught you.

For coding agents this is not "spec less." It's "spec at the right altitude, at the right time, and keep the spec alive." Three moves make it concrete.

## Key beats

- **JIT specs over big-bang specs (the depth rule).** Spec to the depth of your next confident step — usually one feature, one PR's worth. Plan-mode or an interview skill for *that slice*: let the model surface the edge cases and write a tight spec, then build it. Do not have the agent generate forty tickets covering the whole app on day one; those are guesses dressed as a plan. Parsons: just-in-time specs over big-bang specs; over-speccing a project up front "fossilises" a waterfall plan. The contrast image is the whole argument — a 200-page doc written before any code vs a one-feature spec written the moment before you build it.

- **Specs co-evolve with the code (the living-doc rule).** This is the answer to the perennial objection: *you don't know the edge cases until you start implementing.* Right — so the ticket can't be a contract frozen at kickoff. The agent starts the ticket, hits a case the spec didn't anticipate (a null path, a race, a 204-not-200 API contract), and **writes that discovery back** — into the ticket's notes, a newly spawned ticket, or `CLAUDE.md`. For coding this matters more than for prose because the discoveries are mechanical and reusable. Captured in the spec, every future iteration inherits the gotcha. Left only in the diff, it's lost. Parsons' Ralph skill bakes this in: status fields, a decision trail, "questions for me" — the agent records *why* and *what it found*, not just *what changed*.

- **Capture learning back into the repo (the externalisation rule).** This is what makes the first two compound, and it's specific to how loops run. If each loop starts with a fresh context — the relay-runner model, "do one change, drop context, stop" — then the next runner knows *nothing* the last one learned unless it was written to disk. So decisions go in `CLAUDE.md` / `AGENTS.md`, conventions the agent discovered ("we use Result types, not exceptions") go in a docs file the loop reads on startup, and **the tests themselves are captured spec** — a test encodes "this must keep working" for every future pass. Parsons' reframe: treating sessions as *ephemeral* is a feature, because it *forces* you to externalise into the codebase, which keeps the repo the single rich source any agent or human can pick up cold. That's also the defense against **cognitive debt** — the code explains itself because the loop can't function if it doesn't.

- **How they chain for a coding agent.** fresh context → loop reads repo + tickets + CLAUDE.md (externalised learning) → picks the next unblocked ticket → if under-specified, specs *just that slice* → implements, hits surprises, writes them back → tests + commit, drop context → next loop inherits everything via the repo. The repo is the memory, the loop is the engine, and the spec is something that *emerges and updates inside the loop* rather than gating it from outside. That last clause is the exact inversion of waterfall.

- **The guardrail that survives.** None of this removes the human gate on what's *allowed to ship*. Iterative specs speed up how work gets *proposed*; for security-sensitive or irreversible code — migrations, auth, anything touching customer data — Parsons still reads the diff. JIT specs are about the proposal loop, not the release gate. Keep them separate.

- **Where the line actually is.** This is *not* an argument against rigor or against [[specs-are-the-new-product]]. More context genuinely helps the model — so plan, and plan well. The claim is narrower: don't pretend you can plan everything before you've built anything. Plan enough to take the next confident step; let the loop and reality tell you the step after that.

## Connections

- [[specs-are-the-new-product]] — the segment this is paired against. Film them back to back: that one establishes "quality enters upstream in the spec," this one establishes "upstream ≠ all-at-once." The steelman and its limit. Neither lands as well alone.
- [[dont-pre-sequence-the-backlog]] (loopy-ai) — the sibling claim at *backlog* altitude: don't freeze execution order. This is the same instinct at *spec* altitude: don't freeze the design. Both are "waterfall in a hoodie." Cross-link explicitly; this segment is point 1's cousin, not its duplicate.
- [[spec-developer]] — the interview-skill that produces a spec before code. JIT specs say: run that skill per-slice, not once for the whole system. Compatible, with a scope caveat.
- [[tdd-stops-the-cheating-agent]] — tests as captured spec. The externalisation rule leans directly on this: a test is the most durable just-in-time spec you can write.
- [[specs-vs-constraints-making-incorrect-code-unrepresentable]] — the constraint half. JIT specs keep the *spec* fluid; constraints are the part you *do* freeze up front. Pairs cleanly: fluid intent, fixed guardrails.

## Sources / refs

- **Chris Parsons, Ralph Loops workshop (2-hour, live-coded):** https://www.youtube.com/watch?v=2TLXsxkz0zI — primary source for the JIT-specs caution, the "fossilises a waterfall plan" line, the ephemeral-context-as-feature argument, and the read-the-diff-for-irreversible-work guardrail. Parsons' agile/waterfall credibility is part of why the reframe lands.
- Ray's framing: the three rules (JIT depth, living doc, externalisation) as "how iterative specs apply to a coding agent" — the coding-agent translation of Parsons' loop doctrine.
- Pairs with [[specs-are-the-new-product]] (the thesis it tempers), [[dont-pre-sequence-the-backlog]] (the same move at backlog altitude), [[tdd-stops-the-cheating-agent]] (tests as captured spec).

## TODO

- Cold-open on the over-application: someone reads "specs are the product," opens their tool, and generates a 200-ticket spec for the whole app before writing a line. Show it aging badly by ticket 12. *Then* introduce JIT.
- Demo: same feature, two ways. Version A — full up-front spec for the whole module. Version B — spec one slice, build, discover an edge case mid-build, write it back, spec the next slice. Show Version A's downstream sections getting rewritten anyway; show Version B's ticket notes accreting real discoveries.
- Demo the externalisation rule concretely: kill the context mid-project, start a fresh loop, and show it picking up perfectly *because* the last loop wrote its learning into CLAUDE.md + tests. The fresh-context-as-feature beat needs to be seen, not asserted.
- Image: split frame. Left — a fat sealed "SPEC v1.0 FINAL" tome with cobwebs. Right — a thin spec card with sticky notes being added to it each loop, an arrow curving back in.
- Film immediately after [[specs-are-the-new-product]] so the pairing reads as deliberate tension, not contradiction.
