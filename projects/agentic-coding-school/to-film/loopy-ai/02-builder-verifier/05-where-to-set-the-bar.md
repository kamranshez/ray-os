---
duration: 8-12 min
batch: 2
order: 5
batch_name: Builder and Verifier
class: loopy-ai
chapter: Builder and Verifier
aliases: [where-to-set-the-bar, stopping-the-verifier]
---

> STUB. The termination-calibration problem raised on camera in 01-builder-verifier ("the model will always find *something* wrong... verify until no medium/high severity remains, or cap at N rounds").

## Thesis

A verify loop with no calibrated bar never converges. If you tell a model "find what's wrong with this," it will always find *something* — so the loop either runs forever or you cut it off arbitrarily. Setting the bar is what turns the loop from a nitpicking machine into one that ships.

## The failure mode

Uncapped adversarial review = infinite low-severity findings. The model is agreeable in the other direction now: asked to criticise, it manufactures criticism. Cosmetic nits, hypothetical edge cases, "you could also consider…" — none of it load-bearing, all of it keeping the loop alive and burning tokens.

## Two ways to set the bar

- **Severity threshold** — "iterate until no medium- or high-severity issues remain." Low-severity findings are logged, not gated on. (Ray's default.)
- **Round cap** — "at most N rounds of review, then ship what you have." A hard stop independent of the findings.

Best practice: combine them. Threshold for *quality*, cap for *safety*, whichever trips first.

## Map onto the five components

This is the **Terminate** component, done properly. Most people leave it implicit ("until it looks done") and get either a runaway or a premature exit. An explicit, calibrated terminate condition is the difference.

## Demo

Run the same adversarial-review loop twice on one artifact: once uncapped (watch it spiral into low-severity nits across many rounds), once with "no medium/high remaining, max 3 rounds" (watch it converge and stop).

## Key Insight

> Ask a model to find a flaw and it always will. The bar isn't "is it perfect" — it's "is anything left that actually matters."
