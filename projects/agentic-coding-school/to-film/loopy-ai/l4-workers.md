---
duration: "12-16 min"
batch: 3
order: 9
batch_name: "The Climb"
class: "loopy-ai"
chapter: "L4 Worker Loops"
status: stub
---

Stub for the L4 segment. Workers that pick from a queue and process work without being told each time.

## Thesis

L1 through L3 is "I asked the agent to do a thing." L4 is "I built a thing that asks the agent over and over." The difference is small in code, big in mindset. Most students have never built one of these.

A worker is the simplest compounding loop. Once it's running, every item in the queue is free work.

## Key beats

- Anatomy: trigger source (Stop hook, cron, queue webhook, file watcher), pick rule (what to grab next), process step (an L3 inside), report step (write back, post update, mark done), retry rule.
- Three worked examples:
  - **Linear "claude-do" worker.** Watches Linear, picks tickets with a label, runs an L3 to ship the PR, posts a summary.
  - **Dependabot auto-merger.** For each PR, runs tests, checks the diff matches a safe pattern, merges or escalates.
  - **Sentence-mining auto-feeder.** Watches a target word list, finds natural example sentences, generates audio, stages the card.
- Stop hooks as the cleanest worker trigger when the queue is "things the previous agent finished."
- The "it picks up its own work" pattern. A worker that watches the output of another worker is a queue chain. Don't build these until you have governance primitives.
- Where workers fail: silent failure, no kill switch, no budget, no log review. Reference back to [[governance-primitives]].

## What L4 is *not*

Not just a cron job. A cron job runs a script. A worker runs an L3 (which contains L2s, which contain L1s) against a stream of work. Different scope.

## Sources / refs

- Pairs with [[autoresearch]] (the eval-driven worker variant) and [[governance-primitives]] (the rails the worker runs on).
- Sets up [[l5-discovery]] (the worker that feeds workers) and [[bug-triage-loop]] (the worked example of a fleet of workers compounding).

## TODO

- Demo: a real L4 running on screen. The sentence-mining feeder is the easiest to film.
- Image: a queue feeding a single worker, the worker producing finished items, a Slack message appearing on the right.
