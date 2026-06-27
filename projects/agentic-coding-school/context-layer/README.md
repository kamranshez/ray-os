# context-layer/ — read me first

The durable knowledge an agent should read **before producing anything** for Agentic Coding School (landing copy, VSL, ads, emails, pricing). This is the source-of-truth layer. It is separate from the **outputs** that consume it (`../vsl/`, future `../landing/`) and from the **course content** itself (`../classes/`).

## What's here
- **`positioning/brief.md`** — THE source of truth. The "Agent Engineer" reposition: the universal villain, the "engineer loops" lead, the identity, the audience, the offer, the team lane, the proof, the always-current pillar. Start here.
- **`positioning/open-decisions.md`** — what's still unconfirmed (PPP, price-raise timing, naming the 60-seat customer) versus what's locked.
- **`audience/`** — the 6-source market research the positioning is built on (synthesis + newsletter survey, buyer DB, enrichment, testimonials, course content, competitors/pricing, YouTube). `audience/00-personas.md` is the synthesis + decision trail. Append new data here, don't redo it.
- **`pricing.md`** — price points, tiers, refund terms, and pricing policies (e.g. future classes are separate products).
- **`promotion.md`** — how the classes get promoted (channels, launch playbook).
- **`voice.md`** — tone and copy rules every output must follow (no em/en dashes, calm and respectful, the locked lines).

## How to use (cold pickup)
1. Read `positioning/brief.md` end to end.
2. Skim `audience/00-personas.md` for the personas + evidence.
3. Check `positioning/open-decisions.md` so you don't hard-code something still under debate.
4. Honor `voice.md` and `pricing.md` in any rendered copy.
5. Then build the deliverable in `../vsl/` or `../landing/`.

## Status
2026-06-27: positioning locked. Spine = villain ("you're still doing by hand what your agents could do for you") to "engineer loops" to the Agent Engineer identity, with always-current as a supporting pillar, one all-access pass, team as a secondary band, and honest-framed proof. Implementation path: hard-swap the live `agent-engineer.tsx` with a patient, volume-based revert rule.
