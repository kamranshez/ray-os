---
duration: "12-16 min"
batch: 3
order: 7
batch_name: "The Climb"
class: "loopy-ai"
chapter: "L5 Discovery Loops"
status: stub
---

Stub for the L5 segment. Loops that produce problems, not solutions.

## Thesis

A discovery loop doesn't do the work. It decides what *should become* work. This is the level where the role of the human visibly changes. At L1 through L3 you decide what to do and the agent executes. At L5 the agent decides what's worth considering and you choose from the shortlist. That swap is the whole game.

L5 feeds L4. The output of an L5 is a queue item for an L4.

## Key beats

- Boris's "couple hundred Claudes" pattern: agents that scan Twitter, GitHub issues, Slack threads, customer support, looking for something worth doing. Not writing code. Deciding which thing would be worth writing code for next.
- Three worked examples:
  - **YouTube outlier scout.** Watches 100 channels in your niche. Doesn't make videos. Flags topics breaking out, ranked by lift over channel baseline.
  - **Content idea factory.** Reads your library, your audience, your DMs, surfaces three drafts a day for you to pick from.
  - **Anomaly detector on revenue.** Watches Stripe. Doesn't fix the anomaly. Surfaces it so you can investigate.
- The triager pattern: many input streams flow in, one filtered shortlist flows out.
- Where humans stay in the loop: choosing from the shortlist. Where humans don't: building the shortlist.
- Connection to [[echo-chamber]]: discovery loops that read only their own prior outputs converge to a fixed point. The whole point of L5 is exogenous signal.

## What L5 is *not*

Not search. Search returns what you asked for. Discovery returns what you didn't know to ask for.

## Sources / refs

- Boris Cherny on Acquired Unplugged (June 2026): the 200 Claudes pattern
- Pairs with [[l4-workers]] (the consumer of the shortlist) and [[echo-chamber]] (the failure mode this level is most prone to).
- Sets up [[bug-triage-loop]] (the L4+L5 composed example).

## TODO

- Demo: the YouTube outlier scout on screen. Show one input stream (a watchlist of 100 channels), show the filter logic in plain English, show the output (one outlier ranked above the baseline).
- Image: many input arrows feeding into a triager box, one arrow leaving the right side labelled "things worth doing."
