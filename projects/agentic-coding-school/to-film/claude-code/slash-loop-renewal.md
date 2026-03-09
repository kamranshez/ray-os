---
duration: "1-4 min"
batch: 1
order: 3
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Commands"
---

# /loop — Auto-Renewal Before Expiry

Recurring cron jobs auto-expire after 3 days. To keep a loop running indefinitely, schedule a one-shot task to delete and recreate it before it dies. Use `/loop` to set up the renewal job itself — so the whole system is self-sustaining without any manual intervention.
