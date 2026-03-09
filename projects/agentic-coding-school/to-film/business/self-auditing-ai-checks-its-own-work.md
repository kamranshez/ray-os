---
duration: "8-12 min"
batch: 2
order: 5
batch_name: "Operations & Admin"
class: "business"
chapter: "Operations & Admin"
---

## Self-Auditing: AI That Checks Its Own Work

Build a verification layer into any skill so Claude audits its own output before delivering it to you — catching hallucinations, contradictions, and low-confidence claims automatically.

> "Before delivering anything to me, the skill requires Claude to run a self-review. This is critical, and it's the part most people skip. Claude must verify that every cited authority actually says what the memo claims. It must flag anything where its confidence is below high. It must check for internal contradictions across sections. And it must specifically guard against hallucinated citations."
> — [Zack Shapiro (@zackbshapiro)](https://x.com/zackbshapiro/status/2027389987444957625)

### The Cautionary Tale

> "The lawyers who submitted fake AI-generated citations were using tools without this kind of verification layer. The problem was never AI itself. It was AI without quality control."
> — [Zack Shapiro (@zackbshapiro)](https://x.com/zackbshapiro/status/2027389987444957625)

### What to Cover

1. **The self-review pattern** — Add a verification step at the end of any skill that instructs Claude to:
   - Re-check every factual claim against its sources
   - Flag anything with confidence below "high"
   - Check for internal contradictions between sections
   - Mark any claim it cannot verify with an explicit uncertainty flag
   - Run a final pass looking for hallucinated references

2. **Demo: a research skill with built-in audit** — Build a skill that produces a market research brief, then automatically appends a "Verification Report" section rating each claim as Verified / Uncertain / Unable to Verify.

3. **Confidence ratings** — Show how to instruct Claude to rate its own confidence on each finding and present uncertainty explicitly rather than hiding it behind confident-sounding language.

4. **The trust equation** — This is what separates professionals who use AI well from those who get burned. The AI is not practicing your profession. You are.

   > "Everything I've described creates a temptation to let the AI do too much. To stop checking... people who use AI outside its competence, or who trust it without interrogating the output, perform worse than people who don't use AI at all."
   > — [Zack Shapiro (@zackbshapiro)](https://x.com/zackbshapiro/status/2027389987444957625)

### Key Demo

Run the same research query with and without the self-audit step. Show cases where the audit catches a hallucinated source or flags an uncertain claim that would have been presented as fact. The contrast sells the pattern.
