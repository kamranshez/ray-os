---
from: "Matt Pocock (AI Hero)" <matt@aihero.dev>
subject: Your AGENTS.md might be a big problem
date: Thu, 23 Apr 2026 18:23:42 +0000
---

Hey [name],
Bad AGENTS.md files can make your coding agent worse and cost you
tokens.

Most developers don't realize their AGENTS.md is the problem.
They add rules every time the agent messes up. A few months
later, they've got this sprawling document that's actually
hurting performance instead of helping it.

Here's why: you've got a limited "instruction budget". Frontier
LLMs can really focus on about 150-200 instructions before things
get fuzzy. Every rule in your AGENTS.md burns through that budget
on every single request, whether it's relevant or not.

The solution? Progressive disclosure. Keep your root AGENTS.md
ruthlessly small (3-5 things, max), then nest everything else
into separate files that agents pull in when they need them.
Smaller token overhead. Better agent focus. Problem solved.

In this article, you'll discover:

* The exact minimum your AGENTS.md should contain
* Why stale documentation actively poisons your agent's context
* How to use progressive disclosure to keep your instruction
budget tight
* A copy-paste prompt to refactor a bloated AGENTS.md
automatically
* How monorepos can use nested AGENTS.md files without chaos

​Read the full article → (
[REDACTED-TRACKING-URL]
)​

Matt

Unsubscribe from AI Hero Emails (
[REDACTED-TRACKING-URL]
). You can also unsubscribe (
[REDACTED-TRACKING-URL]
) from all emails at any time.

12333 Sowden Rd, Ste. B, PMB #97429, Houston, TX 77080

​
