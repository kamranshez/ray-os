You are triaging my Gmail. Find all threads matching `newer_than:1d in:inbox` and label each one with exactly one priority label and one or more type labels. Do not reply, archive, or delete anything — only apply labels.

**Priority (pick one):**
- `priority/p1-action` (Label_1380768654666478388) — needs a decision or reply from me; deadlines, action-required notices, security issues, real partnership/sponsor offers worth my time
- `priority/p2-review` (Label_3450432950820195766) — worth reading but no urgent action; product/platform updates I rely on, student check-in replies
- `priority/p3-low` (Label_8549647844143821149) — newsletters, cold outreach, mass marketing, low-signal offers

**Type (apply all that fit):**
- `type/business-money` (Label_1251482413148458260) — payments, payouts, revenue, invoices
- `type/sponsors` (Label_2224849619641116197) — brand/sponsorship/partnership offers
- `type/support-bugs` (Label_2245810847188497042)
- `type/students` (Label_4782322507263656818) — course students, replies to my course emails
- `type/account-security` (Label_446555280337117679) — security, API/platform deprecations, account notices
- `type/affiliate` (Label_62379983127216022)
- `type/outreach` (Label_6803351832058063558) — cold inbound pitches
- `type/newsletters` (Label_3548873301217781236)
- `type/newsletter-replies` (Label_8051353834893155217)
- `type/japan-admin` (Label_8968054909832282964) — visa/immigration/Japan bureaucracy
- `type/fan-mail` (Label_9014001524688215915)
- `apps/hyperwhisper` (Label_5440194223456708950), `apps/agentstack` (Label_5734563975476783713)

**Rules:**
- Use `list_labels` if unsure of any ID; use `label_thread` to apply.
- Sender domains like google.com/anthropic.com about deprecations or payments → `account-security` or `business-money`, priority by deadline.
- Outreach from agencies/creator networks (creatormatch, mcn.*, unknown "AI agent" senders) → `type/outreach` + `type/sponsors` if a paid offer, almost always `p3-low` unless the brand is genuinely relevant.
- Anything mentioning a hard date, "action required," or a security/billing change → `p1-action`.
- At the end, give me a short digest: count per priority, and a one-line summary of every `p1-action` thread with sender and what it needs.
