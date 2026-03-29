---
duration: "12-18 min"
batch: 1
order: 6
batch_name: "Seed Thinking"
class: "prompt-engineering"
chapter: "Living Archetypes"
---
In the previous video we built subagent teams from compressed archetypes of ourselves. But those archetypes were static — frozen snapshots of how you think. Real teams learn. Real teams develop dynamics. This video shows how archetypes evolve from run data, develop opinions about each other, and eventually form something that resembles an organizational culture.

### Static vs. Living Archetypes

A static archetype is a snapshot: "here's how Ray makes product decisions, based on 200 past decisions." It's useful immediately but frozen in time. Your taste evolves — you ship something, see how users react, and your judgment shifts. The archetype doesn't know that.

A living archetype feeds on its own run history. Every time you:

- Accept its output → reinforcement signal ("this is what Ray wants")
- Correct its output → calibration signal ("not quite, here's the adjustment")
- Override it in favor of another archetype → priority signal ("in this type of conflict, the other perspective wins")

These signals accumulate. After 50 runs, Product-You isn't the same Product-You you started with. It's been shaped by 50 rounds of your feedback — just like a real employee after their first quarter.

![[images/static-vs-living/excalidraw_1.png]]
### The Correction Problem

Not all corrections are equal. There's a critical distinction:

- **"This was wrong"** — the archetype's judgment was off. It recommended shipping a feature that should have been cut. This correction should update the archetype permanently.
- **"This was wrong for this context"** — the archetype's general judgment is fine, but this situation was unusual. A one-time override, not a pattern change.

If you don't distinguish these, your archetypes overcorrect. Engineer-You gets overruled once on a performance concern, and suddenly it stops flagging performance issues entirely. This is the same failure mode real teams have — someone gets burned and becomes gun-shy.

The fix: when you correct an archetype, tag whether it's a **pattern correction** (update the archetype) or a **context exception** (don't update, just override this once). Over time, the archetype learns your actual judgment boundaries rather than flinching from every correction.


### Archetypes That Model Each Other

After enough runs where Product-You and Engineer-You argue and you resolve the tension, something emerges: each archetype starts to predict the other's objections.

Engineer-You learns that when it flags a concern about "overengineering," Product-You usually agrees. But when it flags "technical debt," Product-You usually overrules it in favor of shipping. So Engineer-You starts framing its technical debt concerns in product language — "this will slow down the next three feature releases" instead of "this schema is wrong."

This isn't hypothetical. It's what happens when you feed an archetype the history of past disagreements and their resolutions. The archetype adapts its communication strategy based on what actually won the argument.

Real teams do this unconsciously over months. Your archetype team does it in 20-30 runs.

**What this looks like in practice:**

- Round 1: Engineer-You says "the data model is wrong." Product-You says "ship it anyway." You side with Product-You.
- Round 10: Engineer-You says "the data model will block the feature we're planning for next month." Product-You agrees to fix it.
- Round 20: Engineer-You preemptively flags data model issues in terms of downstream product impact. Product-You rarely disagrees. The tension has become productive by default.

![[images/archetype-modeling-each-other/excalidraw_1.png]]
### When to Reset vs. Accumulate

Living archetypes have a shelf life. Your taste six months ago isn't your taste today — you've shipped things, seen results, changed your mind. An archetype that accumulated 200 runs of outdated judgment is worse than a fresh one built from your current thinking.

Signs an archetype needs a reset:

- You're overriding it more than 30% of the time (it's drifted from your current taste)
- Its recommendations feel safe and predictable (it's optimizing for "Ray usually approves this" rather than "this is the right call")
- It stopped surprising you (the best archetypes occasionally push back in ways you didn't expect but agree with)

Signs it should keep accumulating:

- Override rate is low and stable
- It catches things you would have missed
- Its arguments have gotten sharper, not just more agreeable

The practical approach: keep a run log for each archetype. Review it monthly. If the corrections have shifted direction (you used to push for speed, now you push for quality), rebuild from recent data rather than letting the old momentum carry.

### From Archetypes to Culture

When your archetype team has developed stable dynamics — each one knows its role, knows when to push and when to defer, knows how to frame arguments the others will accept — you've built something that resembles an organizational culture.

Culture is just a set of shared heuristics:

- "We ship fast and fix later" (product-dominant culture)
- "We don't ship until it's right" (engineering-dominant culture)
- "We let the data decide" (analyst-dominant culture)

Your archetype team develops its own culture based on which archetype you consistently side with. If you override Engineer-You in favor of Product-You 80% of the time, the team's culture becomes "ship fast." If you override both in favor of Design-You, the culture becomes "make it beautiful first."

This is powerful because it means your *governance* role becomes clear. You're not making every decision. You're setting the culture — the default heuristics — and then intervening only when a specific situation needs to break from the default.

**The role shift:**

| Stage             | Your Role                                        | Time Spent |
| ----------------- | ------------------------------------------------ | ---------- |
| No archetypes     | Maker — you do everything                        | 100%       |
| Static archetypes | Editor — you review and correct                  | 40%        |
| Living archetypes | Governor — you set culture and handle exceptions | 10-15%     |

### The Danger: Calcified Thinking

The same dynamics that make living archetypes powerful also create risk. A team that's been running for months develops blind spots:

- **Success bias** — the archetypes optimize for patterns that worked before, even when the market or context has shifted
- **Echo chamber** — if all your archetypes learned from *your* corrections, they all converge toward your existing worldview. Nobody brings a genuinely outside perspective anymore.
- **Loss of serendipity** — a well-calibrated team produces predictable outputs. But some of the best ideas come from the naive question, the dumb suggestion, the "what if we tried something completely different"

Mitigations:

- **Periodic injection of outside data** — feed competitor analysis, customer interviews, or industry trends into your archetypes so they're not just modeling your past thinking
- **Adversarial archetype** — keep one subagent whose job is to argue against the team consensus. Feed it contrarian perspectives, failed companies that did what you're doing, reasons your approach is wrong.
- **Fresh-eyes reset** — every quarter, rebuild one archetype from scratch. Lose the accumulated dynamics. See if the fresh version spots something the seasoned one stopped noticing.

![[images/calcified-thinking/excalidraw_6.png]]
### Demo

1. Show an archetype team with 20+ runs of accumulated history
2. Show how Engineer-You's framing has shifted — it now argues in product terms
3. Show a correction tagged as "pattern" vs. "context exception" and how the archetype responds differently
4. Show the adversarial archetype disagreeing with team consensus and surfacing a blind spot
5. Compare: fresh archetype vs. 20-run archetype on the same task — show what accumulated judgment buys you and what it costs

### Key Insight

> Archetypes that learn from corrections become more than tools — they become a culture. Your role shifts from making every decision to governing the culture: setting defaults, handling exceptions, and periodically breaking the system's own consensus to prevent calcification. The 5% that needs your judgment shrinks over time, but it never reaches zero — because the most important decisions are always the ones your past data can't predict.

### Running Around the Clock

Once your archetypes are living and self-correcting, the final step is obvious: put them on a schedule. Product-You reviews incoming user feedback every morning. Engineer-You audits last night's deploys. Writer-You drafts the weekly newsletter from your dictations. They run while you sleep, and you wake up to outputs that are 95% ready — because the archetypes already know how you'd handle it. The governor checks in, makes the 5% calls, and the system keeps sharpening.
