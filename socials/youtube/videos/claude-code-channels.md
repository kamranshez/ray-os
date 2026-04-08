---
source: https://x.com/trq212/status/claude-code-channels
date: 2026-03-20
status: uploaded
---

Remember when Anthropic dropped remote control and everyone said "this is OpenClaw for grownups"? Well, they just took it further. You can now text Claude Code from Telegram or Discord — and it texts you back.

This is Claude Code Channels. And it changes the dynamic from "I control an agent from a phone app" to "I have an agent living in my group chat."
## How it works

Channels are MCP servers that push messages into a running Claude Code session. The architecture is simple:

1. You install a channel plugin (Telegram or Discord)
2. You give it your bot token
3. You restart Claude Code with `--channels` to activate it
4. Messages from your bot arrive as events in your session
5. Claude reads the event, does the work, and replies back through the same channel

So let's set one up. I'll do Telegram because that's what most people are using.

---

## Setting up Telegram

First, you need a Telegram bot. Open BotFather in Telegram, send `/newbot`, give it a name and username. Copy the token.

Then in Claude Code:

```bash
/plugin install telegram@claude-plugins-official
```

```bash
/telegram:configure <your-token>
```

Now restart Claude Code with the channel enabled:

```bash
claude --channels plugin:telegram@claude-plugins-official
```

Open Telegram, message your bot. It sends you a pairing code. Back in Claude Code:

```bash
/telegram:access pair <code>
/telegram:access policy allowlist
```

That last command locks it down so only your account can send messages. Now you can text your bot from anywhere and it arrives in your Claude Code session.

---

## Demo: texting Claude from my phone

So I have Claude Code running in my RayOS folder with the Telegram channel active. Let me send it a message from my phone.

"Check my calendar for tomorrow and draft a summary of what I have."

And you can see it arrives on my computer, Claude starts working — it's using my Google Calendar MCP server, reading events, and then it replies back through Telegram with the summary. I never left the Telegram app.

Now let me try something more interesting. I'm going to message it:

"Go to my Google Drive, find the latest raw video file, and start editing it with the video editor skill."

This is the same task I showed in the remote control video — but now I'm doing it from Telegram instead of the Claude app. Same MCP servers, same skills, same permissions. The only thing that changed is the interface.

---

## Remote control vs channels — when to use which

They're complementary, not replacements.

**Remote control** (`claude rc`) gives you the full Claude Code interface on your phone through the Claude app. You see the full conversation, approve permissions, switch modes. It's like remote-desktoping into your terminal.

**Channels** give you a lightweight text interface through apps you already use. You fire off a message, get a result back. It's more like texting an assistant.

Use remote control when you want full visibility and control — debugging, reviewing code, approving complex operations. Use channels when you want to fire-and-forget — "run the tests," "check if the deploy went through," "summarise today's emails."

The really powerful thing is combining them. Have channels running for quick messages from Telegram, and if something needs your full attention, switch to the Claude app with remote control for the same session.

![[images/claude-code-channels/remote-control-vs-channels.png]]

---

## The OpenClaw gap is closing

When I made the remote control video, I said the big difference from OpenClaw was that remote control was passive — you tell it what to do, it does it. OpenClaw could search online on a schedule and message you proactively.

With channels plus cron jobs — which I covered in the cron video — that gap is basically closed. You can schedule a cron task to check something every hour, and when it finds something interesting, it can message you on Telegram through the channel. That's proactive.

The people on Twitter calling this "every OpenClaw primitive shipped by Anthropic" aren't wrong. Remote control, cron scheduling, persistent memory, channels — each one closed a specific gap. Channels was the last major piece.

![[images/claude-code-channels/openclaw-gap-closing-timeline.png]]

---

## What I'd like to see next

Two things still missing:

First, **more channel plugins**. Right now it's Telegram, Discord, and a localhost demo. Slack would be the obvious next one for teams. iMessage would be a dream for iOS users.

Second, **richer replies**. Right now you get text back. If Claude generates a diagram or an image, it can't send that through the channel yet. Being able to receive files and images through Telegram would make this significantly more useful.

But the foundation is solid. The channel protocol is open — you can build your own if you want. Anthropic published a channels reference for custom implementations.


---

## Try it

If you've already got Claude Code set up, this takes about five minutes. Install the Telegram plugin, paste your bot token, restart with `--channels`, pair your account.

And if you want to go deeper on Claude Code — skills, cron jobs, remote control, all of it — my full course is linked below.
