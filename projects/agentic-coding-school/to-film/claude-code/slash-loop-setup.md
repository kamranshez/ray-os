---
duration: "1-4 min"
batch: 1
order: 2
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Commands"
---

# /loop — Setting Up a Recurring Task

`/loop` schedules any prompt or slash command to run on a recurring interval. Use it to poll for status, check messages, babysit a deploy, or run any repeated task hands-free. Syntax: `/loop [interval] <prompt>` — e.g. `/loop 5m /telegram-message` or `check the deploy every 20m`.

### Examples

- **Post-deploy health check** — After deploying, create a `/loop 1m` that checks the deploy status for 5 minutes. If it spots an error, it identifies the fix and opens a PR — no babysitting required.
- **Wrap any slash command** — `/loop 20m /review-pr 1234` re-reviews a PR on a schedule. The meta-pattern: any skill becomes a persistent monitor.
- **Long-running CI watcher** — `/loop 30m check if the test suite finished and summarize failures` — polls a slow E2E pipeline and reports the moment it completes.

![[images/slash-loop-setup/excalidraw_9.png]]
![[images/slash-loop-setup/excalidraw_10.png]]
![[images/slash-loop-setup/excalidraw_11.png]]
![[images/slash-loop-setup/excalidraw_12.png]]
![[images/slash-loop-setup/excalidraw_13.png]]
![[images/slash-loop-setup/excalidraw_14.png]]
![[images/slash-loop-setup/excalidraw_15.png]]
![[images/slash-loop-setup/excalidraw_16.png]]
![[images/slash-loop-setup/excalidraw_17.png]]
![[images/slash-loop-setup/excalidraw_18.png]]
