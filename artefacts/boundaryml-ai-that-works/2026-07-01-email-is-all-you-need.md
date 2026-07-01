---
title: Email is All You Need
videoId: zpfXzk-3Yxw
url: https://www.youtube.com/watch?v=zpfXzk-3Yxw
date: 2026-07-01
status: posted
channel: BoundaryML / AI That Works
---

## The one idea worth a video

**1. Design agents for async, interrupting inputs from day one.** Because you never own the UI, a correcting or cancelling message can land mid-execution, so you serialize each thread, defer every irreversible side effect, and re-verify before you write or send.
VERDICT: net-new video available.

**2. Inbound email is a generic programmable webhook, not a special channel.** Hand the agent one raw typed payload and route it in code, rather than adopting an opinionated "agent inbox" abstraction.
VERDICT: net-new video available.

**3. Your inbox becomes an async task queue you delegate to.** Forward an email to an agent that updates a markdown CRM in git and Slacks you the diff, so you burn down a backlog without doing each task.
VERDICT: next-step (complement) video available.

## Summary

BoundaryML's "AI That Works" podcast: Vaibhav (BAML), Dex (HumanLayer), and Ethan (myMX/email.works) explore building agentic systems over email, covering ingress architecture, delegation, and async cancellation.

Counts (one per promoted spine): 🔴 2 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1 — Design agents for async, interrupting inputs

**The claim:** because you do not own the UI in an email agent, a correcting or cancelling message can arrive while a job is still running, so you must serialize per-thread work, defer every irreversible side effect to the end, and re-verify before writing or sending.

**Why it is non-obvious:** most engineers build synchronous server flows (request, respond, stream) and only bolt on interrupt handling later with heavy UI plumbing. Email removes the UI, so the async problem is unavoidable from day one.

**Why it is true:** because the client owns the UI, corrections and cancellations arrive for free as new emails, but they can land while T0 is processing. So you serialize each thread into its own queue (never two concurrent), treat every external write as a pending transaction, and at the verify-and-write yield point recheck the queue: if a newer email arrived, blow up the transaction, roll back, and rerun with T1, which already contains the full T0 thread and loses nothing.

**What it generalizes to:** any async agent surface, for example a Slack bot, an SMS agent, or a long-running background job where the user can revise the request mid-flight. The same queue plus yield-point plus rollback pattern applies.

**How it goes wrong:** a 30-second LLM run means a reply 31 seconds later, after you already sent, cannot be undone, so you re-verify at send time and synthetically inject the sent email into context. Branching threads break the linear-chain assumption, and edited history means you cannot trust the naive thread, so persist each blob to S3.

### Spine 2 — Email as a generic programmable webhook

**The claim:** treat inbound email as a generic webhook that hands you one raw, typed payload, then route it in code, rather than adopting an opinionated "agent inbox" abstraction.

**Why it is non-obvious:** incumbents assume the hard part is sending and wrap ingestion in abstractions like create-an-inbox APIs. As Ethan puts it, "developers know more than you; they just want access to the data." The hard, valuable part is getting raw typed programmable email in.

**Why it is true:** because myMX runs its own postfix SMTP server and returns a full zod-validated EmailReceived event, you can switch on the to-address (extract@, parse@, verify@) or let an AI classify intent, and each action reads only the parts of the email it cares about. It is "just code," like Slack's one-payload webhook: a new agent is a new code path, not a provisioned inbox.

**What it generalizes to:** multi-channel ingress. Agents need email, Slack, and SMS ingress the same way a website needs desktop and mobile; the same unopinionated-webhook plus router pattern applies to each channel, and missing one makes the agent feel broken.

**How it goes wrong:** running your own mail server is genuinely hard (SMTP return codes, DNS, deliverability). Huge threaded payloads bloat a Lambda past size limits, and you still own concurrency, rate-limits, and idempotency yourself.

### Spine 3 — Forward-to-agent delegation with a markdown CRM

**The claim:** your inbox becomes an async task queue. Forward an email to an agent that reads it, updates a markdown CRM in a git repo, and Slacks you the diff, so you burn down a backlog without doing each task yourself.

**Why it is non-obvious:** people dismiss email agents as "for boomers, I will just use the website." The real unlock is not question-and-answer, it is delegation, and email's single linear thread beats Slack's channel-hopping chaos for processing one item at a time.

**Why it is true:** because a forwarded email carries structured sender, body, and attachment data, an agent can extract a task (title, description, labels, assignee, like a Linear ticket), write it into markdown files, commit to a private repo, and post the new files to Slack. Dex runs exactly this as a GitHub Actions workflow locally via ngrok and as a Lambda in production.

**What it generalizes to:** any "forward to act" workflow. Forward a vendor note to create a task, forward a lead to research and qualify them, or forward a receipt to file an expense (Mercury does this today).

**How it goes wrong:** not everything is fire-and-forget; "research this person and reply" needs a round trip. A markdown-in-git CRM does not scale to relational queries, and the side effects still need the interrupt-safe flushing from spine 1.

---

## 🎬 Proposed ACS videos

### 1. Build an Agent That Can Be Interrupted Mid Task

- HOOK: your agent starts booking the meeting, then the user emails "wait, cancel that." What happens?
- THE PROMISE: for anyone building agents on any async surface, walk away able to handle a correcting or cancelling message that lands mid-execution without corrupting state.
- THE SHAPE: (1) why async is unavoidable when you do not own the UI; (2) serialize each thread into its own queue so two messages never process concurrently; (3) queue every external write as a pending transaction, flush only at the end; (4) at the write yield point, recheck the queue and roll everything back if a newer message arrived; (5) re-verify at send time and inject already-sent side effects into context on a race.
- SPINE: 1.
- SLOT: Techniques class (neighbors: core-agent-loop, closing-the-loop, designing-interfaces).
- RELATIONSHIP: ❌ net-new. ACS has nothing on out-of-order, cancelling, or racing inputs to an agent; core-agent-loop and closing-the-loop cover the happy-path loop, not interrupt safety.
- PROOF TO REUSE: "you have to design your system to be robust to that from day one"; the yield-point rollback ("you blow up the whole thing and you roll it all back"); "you can't roll back an email send or a calendar event created."

### 2. Email Is Your Agent's Front Door

- HOOK: the incumbents made receiving email absurdly hard; here is how to treat it like a Slack webhook instead.
- THE PROMISE: for developers wiring agents into the real world, leave able to accept inbound email as one raw typed payload and route it to the right agent in code.
- THE SHAPE: (1) the hard part is ingestion, not sending; (2) get one raw, zod-typed EmailReceived event, no abstraction; (3) route with a switch on the to-address, or let an AI classify intent; (4) each action reads only the parts it needs (extract wants images, parse pulls everything); (5) generalize to Slack and SMS as the same unopinionated-webhook pattern.
- SPINE: 2.
- SLOT: Techniques class (agent architecture); seeds the empty Business > agent-mail backlog slot.
- RELATIONSHIP: ❌ net-new. ACS has mcps-connectors and hooks material but nothing on email or multi-channel ingress as a programmable webhook for agents; agent-mail is only a backlog title with no script.
- PROOF TO REUSE: "developers know more than you; they just want access to the data"; the extract@ / parse@ / verify@ routing demo; "if you've ever seen Slack's webhook system, it's very similar."

### 3. Turn Your Inbox Into an Agent You Delegate To

- HOOK: forward a vendor email to an address and an agent files the task, updates your CRM, and Slacks you the diff.
- THE PROMISE: for founders and operators, leave able to build a forward-to-act pipeline that burns down inbox work without you doing each task.
- THE SHAPE: (1) delegation, not chat, is email's real unlock; (2) forward an email to an agent endpoint; (3) extract a structured task (title, labels, assignee) with an AI function; (4) write it to a markdown CRM in a private git repo and commit; (5) Slack the new files back; run it via GitHub Actions locally with ngrok, then a Lambda in prod.
- SPINE: 3.
- SLOT: Business > agent-mail (currently a backlog title, no brief).
- RELATIONSHIP: 🔗 complements "Airtable Memory for Cloud Scheduled Tasks," which already teaches persisting agent state for cloud and scheduled work; this adds email as the async trigger, a markdown-in-git CRM substrate, and a Slack diff notification.
- PROOF TO REUSE: "I can forward emails from people and Claude will read the emails and update markdown files ... and send me an update in Slack"; the Linear-ticket schema extraction; "I got this note from a vendor, can I forward it to an agent that will create a task for someone."

---

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's "AI That Works" podcast: Vaibhav (BAML), Dex (HumanLayer), and Ethan (myMX/email.works) explore building agentic systems over email, covering ingress architecture, delegation, and async cancellation.

### IDEAS
- Email works for agents not because it's great but because everyone already lives inside it daily.
- Email predates the internet and remains the universal communication layer where business and compliance data lives.
- The hardest part of email agents is ingestion: getting raw, typed, programmable email data, not sending.
- Incumbent email tools became outbound marketing companies obsessed with inbox delivery, abandoning inbound developer experience entirely.
- AWS SES dumps each email into an S3 bucket as an untyped blob, saying good luck.
- myMX runs its own postfix SMTP mail server on a VPS to get truly programmable data.
- You register one MX record plus a TXT record on any domain; myMX handles wildcard subdomains.
- Email forces asynchronous system design because you don't own the UI and can't block follow-up messages.
- Because the email client owns the UI, cancellation and correction interrupts come free without UI plumbing.
- Treat inbound email as a generic webhook like Slack's: one payload, then route it in code.
- Route on the to-address with a switch statement, or let an AI decide the downstream agent.
- Each agent action decides which email parts it needs: extract wants images, parse pulls everything out.
- Developers know more than your abstraction; give them raw typed data and they'll build anything themselves.
- BAML AI functions act as transformation units: forward anything, get a TLDR, structured JSON, or OCR.
- Verify agent checks DKIM, SPF, and DMARC so you can detect phishing by forwarding suspicious emails.
- Delegation is email's real unlock: forward a vendor note to an agent that creates someone's task.
- Serialize each email thread into its own queue so two messages never process concurrently, avoiding races.
- Queue all external writes as pending transactions and flush them only when processing finishes fully uninterrupted.
- At verify-and-write, recheck the queue: if a newer thread email arrived, roll back and rerun everything.
- Because each reply contains the full prior thread, discarding T0 and rerunning T1 loses no information.
- Write every email blob to S3 immediately since senders can edit history, breaking the naive thread.
- You cannot roll back a sent email or created calendar event, so verify again at send-time.
- If a reply raced your own send, synthetically inject that sent email into the model's context.

### INSIGHTS
- Email's value for agents isn't the medium; it's meeting users inside the tool they already inhabit.
- Owning the UI is a liability for interrupts; borrowing email's UI hands you correction handling free.
- The moat isn't sending email; it's structured, typed, programmable ingestion that incumbents abandoned for outbound revenue.
- Turning email into an API means applying every API discipline: queues, rate limits, concurrency keys, idempotency.
- Handling interrupts well is agent design; collecting the right context is the application builder's own responsibility.
- Email chains resemble LLM context windows: each message carries the full conversation, ideal for language models.
- Agents need many ingress channels: email, Slack, SMS; missing one makes the agent feel obviously broken.
- Side effects on the external world need queueing and end-of-run flushing, not immediate optimistic execution mid-run.
- Being unopinionated beats adding abstractions; developers want raw access themselves, not another inbox API to learn.
- AI enables applications whose only interface is email: sign up, interact, and see stats via replies.

### QUOTES
- "The reason I built this truly is because it didn't exist already. I could not believe that everyone had made it this hard." (Ethan)
- "It's not that email itself is that great. It's just that everyone uses it. It's already where people live." (Ethan)
- "We have a no email policy on our company. We only use Slack and Discord. I freaking hate email." (Dex)
- "You don't own the UI. You have to design your system to be robust to that from day one." (Vaibhav)
- "In the email system it's actually you have to do zero work because the UI layer does that for you automatically." (Vaibhav)
- "Developers know more than you. They just want access to the data and they'll figure out how to do it." (Ethan)
- "This is putting the engineering back in context engineering, dude. I love it." (Dex)
- "You blow up the whole thing and you roll it all back." (Vaibhav)
- "A transaction can only impact your database ... but you can't roll back an email send or a calendar event created." (Dex)
- "The title is email is all you need, but apparently you also need 10 years experience in systems engineering." (Vaibhav)
- "Managing an email domain email server for your own domain is actually stupidly hard." (Dex)
- "Can I forward it to an agent that will create a task for someone to handle it?" (Dex)

### HABITS
- Dex forwards emails to an agent that updates a markdown CRM and Slacks him the changes.
- They keep customer relationship data as markdown files inside a private git repo, not a database.
- Ethan tests inbound email locally with ngrok pointing to a local TypeScript server before deploying Lambdas.
- Dex pastes DNS records into Claude and has it run the CLI to create them automatically.
- They forward emails as attachments in Gmail to preserve full DKIM headers for the verify agent.
- They use magic strings and nested loops freely, refusing to over-abstract simple email-routing handler code.
- Ethan copied PostHog's CSS styling himself rather than generating the marketing site with a design tool.
- They pipe their rambling system-design monologues through Claude to produce clean mermaid diagrams for viewers afterward.
- Dex deploys the same email pipeline as an AWS Lambda in production but Groq for inference.

### FACTS
- Email predates the internet itself, having existed before modern networking protocols were widely standardized and deployed anywhere.
- AWS SNS messages have a maximum size of a few megabytes, so emails with attachments explode.
- Vercel serverless functions impose roughly a six-megabyte body size limit on request payloads for handlers.
- Sending email reliably requires warming up IPs and domains and configuring SPF, DKIM, and DMARC records.
- myMX serves raw attachments up to roughly 256 kilobytes inline, larger ones via downloadable signed URLs.
- Rap.dev processed roughly one million commits and around ten million file changes through its pipeline system.
- Gmail does not load full payloads for very long threads because the transferred bytes are too large.
- Mercury's receipt feature lets you forward a receipt and automatically attaches it to the matching expense.

### REFERENCES
BAML, myMX (myx.dev), email.works, HumanLayer, AWS SES, AWS SNS, Amazon S3, AWS Lambda, Groq, resend, React Email, SendGrid, ngrok, postfix, Vercel serverless functions, Redis, Upstash, Amazon SQS, Mercury (receipts), PostHog (CSS), Excalidraw, Gmail, Slack, Discord, Claude, GitHub Actions, DKIM / SPF / DMARC, Rap.dev, Snooze, Bondbook (Ailla's email travel agent), D.E. Shaw, GPT model "5.2", Linear (tickets), Luma.

### ONE-SENTENCE TAKEAWAY
Give agents a programmable email ingress and design async because you never own the UI.

### RECOMMENDATIONS
- Add an email ingress channel to your agent so users can delegate from where they work.
- Serialize each email thread through its own queue to guarantee no two messages process concurrently ever.
- Queue external side effects as pending writes and flush only after processing completes without newer messages.
- Recheck for newer thread emails before writing; if found, roll everything back and rerun with latest.
- Persist each raw email blob to S3 immediately so you survive edited history and reconstruct chains.
- Verify again at send time because sent emails and calendar events cannot be rolled back afterward.
- Route inbound emails with a switch on the to-address, or let an AI classify the intent.
- Use concurrency keys from verified sender identity via DKIM to rate-limit and prevent accidental email floods.
- Forward emails to an agent that updates a markdown CRM in git and Slacks you diffs.
- Sign up for myMX with one MX and TXT record to get typed webhook email events.
