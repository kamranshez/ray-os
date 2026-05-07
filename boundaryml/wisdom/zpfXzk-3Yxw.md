---
video_id: zpfXzk-3Yxw
title: "Email is All You Need: 🦄 #41"
url: https://www.youtube.com/watch?v=zpfXzk-3Yxw
channel: BoundaryML
---

## SUMMARY

Boff and Dex host Ethan on AI That Works to discuss building agentic systems over email using BAML and the new MyMX service.

## IDEAS

- Email is universal because business data already lives there despite endless attempts to abandon it.
- Companies need email paper trails for compliance, making email a permanent enterprise communication layer.
- Most email infrastructure companies eventually become outbound marketing tools rather than transactional development platforms.
- Asynchronous workflow forces robust agent design from day one because you cannot control the UI layer.
- Email naturally handles cancellation interrupts because users own the client and can send corrections.
- Synchronous server-side thinking dominates web development, but email demands async thinking by structural necessity.
- Delegation, not direct interaction, is email's killer agent use case for productivity workflow.
- Slack feels chaotic across channels while email inboxes provide one linear thread for processing.
- AWS SES essentially dumps emails into S3 buckets and says good luck to developers.
- Building email systems requires warming IPs, configuring DKIM, SPF, DMARC, and other arcane infrastructure.
- The two-header in email enables routing logic without creating separate inbox endpoints for each agent.
- AI unlocks new modalities where applications work entirely through email with no dashboard required.
- Travel agents over email let users book flights without ever returning to the website.
- BAML makes structured JSON extraction from PDFs and images trivially simple for arbitrary email content.
- Forwarded receipts can automatically attach to expenses through verification, OCR, and structured extraction pipelines.
- DKIM, SPF, and DMARC can verify legitimacy of forwarded emails to detect phishing attempts.
- A switch statement on the to-header beats abstract inbox APIs because developers know better than vendors.
- Magic strings in routing logic are fine when developer experience matters more than architectural purity.
- Webhook event systems beat S3 polling because they handle event chains and reply correlation naturally.
- Running your own postfix mail server is the only way to deliver low-latency email APIs.
- Queues with concurrency limits per sender prevent rate-limit explosions when emails arrive in bursts.
- Verified DKIM headers provide trustworthy keys for per-sender concurrency control in agent systems.
- Cancellation in async agents requires queueing writes as planned operations until processing fully completes.
- Email reply chains naturally provide LLM context because providers include thread history automatically.
- Verify-and-write checkpoints let you abort transactions if newer emails arrive on the same thread.
- S3 archival of every received email payload enables reconstruction even when senders edit thread history.
- Yield points in workflow processing let agents discard work when context updates make it stale.
- External-world side effects like calendar invites cannot be rolled back like database transactions can.
- Race conditions between agent replies and user replies require synthetic context injection for the LLM.
- Email threading is hard because payloads grow huge and Gmail itself stops loading full thread content.
- Most agents fail at handling user corrections because developers must build cancellation in UI layer.
- Booking apps, scheduling agents, and CRMs all benefit from forwarding-as-attachment workflows for compliance.

## INSIGHTS

- Email's value for agents lies in its asynchronous-by-default nature, which forces robust design from day one.
- Developer experience beats abstraction; give developers raw structured data and they will build better systems themselves.
- Webhook architectures fundamentally outperform polling-based systems for event-driven workflows like email processing.
- The hardest part of email is ingestion, not response; structured input parsing is the unsolved problem.
- Treating emails like API calls unlocks rate limiting, concurrency control, and clean event-driven architecture.
- Cancellation in agent systems requires queuing all external-world effects until the workflow fully completes.
- DKIM verification provides cryptographic identity for senders, enabling trustworthy keying in concurrent processing systems.
- Email threads function like LLM context windows because every reply contains full conversation history naturally.
- Linear control flow assumptions break when agents must handle racing user corrections and synthetic confirmations.
- Owning the mail transfer agent is the only path to low-latency email APIs without intermediary infrastructure.

## QUOTES

- "Email is older than the internet itself." — Ethan
- "We have a no email policy on our company. We only use Slack and Discord." — Vibhav
- "I freaking hate email." — Vibhav
- "It basically puts the email into an S3 bucket and says good luck." — Ethan
- "Every email company that I've ever seen, even the ones that start as transactional, eventually become outbound." — Dex
- "Claude can write terraform and it kind of works but yeah, it's a question." — Dex
- "I think that part of agent design is really fascinating personally." — Vibhav
- "There's so much work I have to do in the UI layer to bridge those systems together." — Vibhav
- "Wait, email is for boomers. Like, why would I want to send an email to chat GPT?" — Dex
- "When you embrace async you can unlock productivity goals." — Dex
- "Of course it uses BAML under the hood because why would you use anything else?" — Ethan
- "I could not believe that everyone had made it this hard." — Ethan
- "Developers know more than you. They just want access to the data." — Ethan
- "Not a real AI that works if we don't hack around on the code live during the episode." — Dex
- "Tried to sign up for SendGrid while I was in Paris and my account got blocked." — Dex
- "Managing an email domain email server for your own domain is actually stupidly hard." — Dex
- "It is so shitty to run a mail server." — Dex
- "We're not afraid of nested for loops either." — Ethan
- "This is putting the deeply putting the engineering back in context engineering." — Dex
- "Email is all you need but apparently you also need 10 years experience in systems engineering." — Dex
- "You will never be able to buy an episode of AI that works." — Dex
- "SMTP is the worst is the beta code." — Ethan

## HABITS

- Use BAML as the default for any structured AI extraction or transformation task in agent systems.
- Default to webhooks over polling architectures when designing event-driven systems for external integrations.
- Forward emails as attachments when DKIM header preservation matters for downstream verification logic.
- Run agents through queues with per-sender concurrency limits to prevent runaway processing on burst inputs.
- Persist every received email payload to S3 immediately upon arrival before any agent processing begins.
- Queue all external-world write operations as planned changes and flush only after successful workflow completion.
- Use ngrok during local development to test webhook integrations against real production-style traffic flows.
- Write Terraform infrastructure code by giving Claude clear specifications instead of writing boilerplate manually.
- Maintain CRM data as markdown files in private GitHub repos rather than using bloated SaaS tools.
- Apply switch statements on email to-headers for routing instead of building separate inbox abstractions per agent.
- Use signed URLs for fetching large email attachments rather than inlining megabyte payloads in webhooks.
- Always include thread history in agent context windows because email naturally provides full conversation state.
- Verify DKIM, SPF, and DMARC on every inbound email before trusting sender identity for actions.
- Give Claude the email payload directly and let it generate Mermaid diagrams instead of drawing manually.

## FACTS

- Email predates the modern internet by several years as a communication protocol.
- AWS SNS messages have a maximum size limit of several megabytes, breaking on attachments.
- Vercel serverless functions enforce a six-megabyte body size limit on incoming HTTP requests.
- Gmail does not load full payload for long email threads because bandwidth costs are too high.
- DKIM, SPF, and DMARC are three separate email authentication standards used to verify sender legitimacy.
- Postfix is an open-source mail transfer agent commonly used for running custom SMTP servers.
- Gmail's "forward as attachment" feature is the only forwarding mode that preserves full DKIM headers.
- Resend is an email-sending service built on top of React Email for transactional outbound mail.
- AWS SES delivers received emails into S3 buckets with no structured webhook event format.
- HumanLayer previously built an agent email-receiving feature using SNS messages with size limitations.
- The rap.dev project processed approximately one million commits with around ten million file changes.
- BAML supports native PDF input types, enabling direct extraction without intermediate text conversion steps.
- MyMX provides webhook-based email ingestion with structured JSON payloads instead of raw S3 dumps.
- Mercury's receipt feature uses email forwarding with OCR to attach receipts to expenses automatically.

## REFERENCES

- BAML — programming language for building AI agents
- MyMX (myx.dev) — Ethan's email infrastructure service
- email.works — open-source demo app showcasing MyMX capabilities
- HumanLayer — Dex's previous company that built agent email features
- AWS SES, SNS, S3, Lambda — referenced infrastructure tools
- Resend — email-sending service with React Email
- SendGrid — referenced incumbent email provider
- Postfix — open-source SMTP mail transfer agent
- ngrok — local server tunneling tool
- Mercury — fintech company with receipt-forwarding feature
- Bondbook (Aila's project) — travel agent that operates entirely over email
- Linear — issue tracker referenced for ticket extraction example
- Gemini 5.2 — model used in BAML parse document example
- Excalidraw — diagramming tool used during the live whiteboard session
- React Email — library for templating HTML email content
- Slack webhooks — referenced as architectural inspiration for generic event payloads
- DKIM, SPF, DMARC — email authentication standards
- AI That Works podcast — the show itself, runs every Tuesday

## ONE-SENTENCE TAKEAWAY

Email is the universal async ingress channel agents need, but ingestion infrastructure remains the unsolved problem.

## RECOMMENDATIONS

- Sign up for MyMX at myx.dev with beta code "SMTP is the worst" to start building.
- Open source the email.works repository to study a clean reference architecture for email agents.
- Build a forwarded-receipt extractor using BAML to automatically populate expense records from email attachments.
- Implement a switch statement on the to-header to route different email addresses to different agent behaviors.
- Use signed URLs for attachment retrieval rather than inlining large payloads in webhook bodies.
- Persist every inbound email payload to S3 before processing to enable reconstruction during race conditions.
- Queue all external-world write operations and flush them only after the workflow completes successfully.
- Add DKIM, SPF, and DMARC verification to every inbound email handler before trusting sender identity.
- Set up per-sender concurrency limits in your queue handler keyed on verified sender identity.
- Forward inbound emails to a Lambda that triggers GitHub Actions to update markdown CRM files in repos.
- Use BAML's native PDF type for direct document extraction without intermediate text conversion steps.
- Build a delegation-focused email agent that creates tasks rather than answering questions interactively.
- Test forwarding behavior with Gmail's "forward as attachment" feature when DKIM verification matters downstream.
- Architect agent systems as async by default to handle user cancellations and corrections gracefully.
- Use markdown files in private repos as a lightweight CRM rather than adopting bloated SaaS tools.
- Build verify-and-write checkpoints that abort transactions when newer messages arrive on the same thread.
- Inject synthetic context into LLM workflows when race conditions cause replies to cross with new emails.
