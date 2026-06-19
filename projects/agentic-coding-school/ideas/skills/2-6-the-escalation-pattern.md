---
class: "skills"
chapter: "Your First Skill"
status: "idea"
source: "Daniel Miessler — Stop Getting Blocked: My Escalating Web Scraper Skill"
---

## The Escalation Pattern

Build skills that recover from failure without human intervention.

### The Problem

Every skill built so far in this class works on the happy path. You give it input, it produces output, done. But what happens when the happy path breaks? An API rate-limits you. A website blocks your request. A file format isn't what you expected. A service is down.

Right now, the skill just... fails. You have to manually intervene, figure out what went wrong, and retry. That's fine when you're sitting at your desk. It's a dealbreaker when the skill is running on a schedule at 3am (Ch 6.2) with nobody watching.

The escalation pattern fixes this. It's a skill architecture where you build multiple tiers of execution — starting with the cheapest and simplest method, and only escalating to more expensive or complex methods when the current tier fails.

### Miessler's Web Scraper Example

Daniel Miessler built a web scraping skill with 4 tiers:

| Tier | Method | Cost | Speed | When it fails |
|---|---|---|---|---|
| 1 | Native web_fetch (built-in) | Free | Fast | Site blocks the request |
| 2 | cURL with browser headers | Free | Fast | Site requires JavaScript |
| 3 | Headless browser (Playwright) | Free | Slow | Site blocks datacenter IPs |
| 4 | Residential proxy network | ~$0.01/req | Medium | Almost never |

Each tier catches its own failure, logs it, and hands off to the next. The user never intervenes. The skill just works — or escalates until it does.

### What to Show

**Build a data-fetching skill with 3 tiers:**

1. **Tier 1 — Simple fetch**: Try the basic approach first (web_fetch, direct API call, simple file read)
2. **Tier 2 — Retry with adaptation**: If tier 1 fails, adapt the approach (add headers, change format, try an alternative endpoint)
3. **Tier 3 — Heavy artillery**: If tier 2 fails, bring in the expensive/slow/powerful option (browser automation, proxy, fallback service)

**Live demo:**
- Show the skill hitting a wall at tier 1 (blocked by Cloudflare or similar)
- Watch it automatically detect the failure and escalate to tier 2
- Show tier 2 succeeding — the audience sees the skill recovering in real time without any human intervention
- Then show a case where tier 2 also fails → tier 3 kicks in and succeeds
- Compare: without escalation, the skill just errors out and stops

**The skill.md structure for escalation:**
```
## Execution
1. Try tier 1: [simple method]
2. If tier 1 fails (error, empty response, blocked):
   - Log: "Tier 1 failed: [reason]. Escalating to tier 2."
   - Try tier 2: [adapted method]
3. If tier 2 fails:
   - Log: "Tier 2 failed: [reason]. Escalating to tier 3."
   - Try tier 3: [heavy method]
4. If all tiers fail:
   - Report failure with tier-by-tier log so the user can diagnose
```

### Key Architectural Principles

- **Cost-aware tool selection**: Cheapest/fastest first, expensive/slow only when needed. Miessler's proxy network costs ~$0.01/request but he only hits it when 3 free methods have already failed.
- **Fail-forward, not fail-stop**: Each tier catches its own failure and hands off cleanly to the next. No crashes, no manual retry.
- **Observability**: Log which tier succeeded and which failed. Over time you learn which tiers matter for which use cases.
- **Schedule-safe**: A skill with escalation can run at 3am on a cron schedule because it can recover from transient failures without you.

### Why This Matters

This is the difference between a skill that works in demos and a skill that works in production. Nobody in the competitor landscape teaches this. They all show skills on the happy path. This video shows what happens when the happy path breaks — and how to design around it before it happens.

### Cross-Links

- [[6-2-scheduling-skills-as-autonomous-agents]] — escalation makes skills trustworthy enough to run unattended
- [[5-6-business-metrics-for-skills]] — track which tiers fire most often to optimize cost
- [[2-3-anatomy-of-a-well-built-skill]] — the guardrails section connects to failure handling
