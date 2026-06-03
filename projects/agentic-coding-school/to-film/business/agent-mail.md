---
class: "business"
chapter: "Marketing Automation"
---

## Agent Mail — Let AI Agents Run Your Inbox

Give an AI agent its own email address and let it autonomously manage your inbox — checking emails on a schedule, responding to ones that need replies, subscribing to newsletters, and forwarding important stuff to you.

### The Hook

"What if you never had to check email again — because an AI agent does it for you, every hour, on autopilot?"

### What to Cover

1. **The problem** — Email is the biggest time sink. Hiring a human inbox manager costs $50k+/year. Most "AI email" tools just draft replies for you to approve — that's not autonomous.
2. **AgentMail** — Y Combinator-backed API that gives AI agents their own email inboxes. Unlike Gmail/Outlook which actively block non-human access, AgentMail is built for two-way agent conversations.
3. **Build the demo:**
   - Set up an AgentMail inbox via their API
   - Connect it to Claude Code with a cron/loop that checks every hour
   - Agent reads incoming emails, classifies them (urgent / needs reply / newsletter / spam)
   - Auto-responds to routine ones (meeting requests, simple questions)
   - Forwards important ones to your real inbox with a summary
   - Subscribes to newsletters and sends you a weekly digest
4. **The cost framing** — An autonomous email agent running 24/7 costs pennies in API calls vs hiring someone or spending 2+ hours/day in your inbox

### Key Tools

- AgentMail API (agentmail.to)
- Claude Code + cron job or Trigger.dev for scheduling
- Gmail MCP for forwarding to your real inbox

### Competitors to Mention

- Shortwave, Lindy AI, Fyxer — but these are assistants, not fully autonomous agents
- EtherMail/Moltmail — gives agents email + crypto wallets (web3 angle)
- Manus AI — executes tasks from email content autonomously
