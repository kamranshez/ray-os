---
status: stub
acs: []
mapping: workshop-original
day: 1
block: core
recording-needed: true
---

# Models drift toward two possible truths if tickets contain ambiguity

## The idea
When a ticket or design doc contains ambiguity — two plausible interpretations of how something should work — the model sees both and picks one at every downstream decision point. The picks are independent. So at one step it commits to interpretation A; at the next step it commits to interpretation B. The implementation becomes internally inconsistent in ways the human can't catch at code-generation speed. The fix is not to "clarify both options" — it's to *eliminate the ambiguity entirely* by removing the uncertain sections from the ticket.

## Why "clarify" doesn't work
- Even with both options described, the model still picks one per decision
- Adding more text increases ambiguity surface area
- The model has no global consistency mechanism across long generations

## Why "remove" works
- A missing section forces a design discussion to surface it
- The discussion produces a single committed answer
- That single answer goes into the ticket and propagates consistently

## How to apply
- When reading a ticket, flag every "unknown" or "TBD" or hand-wave
- Don't fill them in with placeholders — *delete them*
- Let them resurface as questions in the next design pass
- Vibhav's principle: "if I'm not sure how to do something, I'd rather not have a bad version in the ticket"
- The two-pass workflow: first ticket → design discussion → ticket-two with everything resolved

## Surrounding context
This came up when Vibhav and Dex were reviewing the testing-feature ticket. Vibhav saw "unknown" placeholders in the report-types section and flagged them: "I see unknowns, don't really like that." Dex's response: "remove the things you're unsure about so they don't come into the model as pre-baked decisions." The two-sentence-to-big-design-discussion pattern works specifically *because* removing uncertainty forces the discussion. If you fill it in with a guess, you've stolen the option to discuss it.

The deeper point: a 200-line ticket with one ambiguity becomes thousands of drifted lines. The cost of one wrong line in the ticket is asymmetric.

## Open questions to explore
- How do you train yourself to recognize ambiguity in your own writing?
- Is there a model-assisted "find the ambiguity in this ticket" step worth adding?
- What's the right granularity for "remove" — sentence, section, whole concept?
- Does this principle apply to product specs, or only to engineering tickets?
- How do you handle ambiguity that you genuinely can't resolve yet?
