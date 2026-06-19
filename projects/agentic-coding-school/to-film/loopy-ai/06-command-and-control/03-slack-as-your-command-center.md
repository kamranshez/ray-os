---
duration: "10-14 min"
batch: 7
order: 26
batch_name: "Command & Control"
class: "loopy-ai"
chapter: "Slack As Your Command Center"
aliases: [slack-as-your-command-center]
---

Your loops have outgrown the terminal. Once you are running a fleet, you cannot sit in front of a screen watching a wall of scrolling output. You need a single surface where every loop reports in, asks for the things it is not allowed to do alone, and where you steer the whole operation by replying.

That surface is Slack.

Not because Slack is special. Because you already live there, it is already on your phone, and it gives a loop a threaded place to talk that survives across runs. The terminal is where a loop is born. Slack is where it grows up and starts answering to you.

---

## The terminal was never the interface

Here is the mistake almost everyone makes after building their first worker. They keep the terminal as the command center.

It works for one loop. You start it, you watch it, you Ctrl-C it when it goes wrong. But the governance segment just defined a fleet as the set of loops sharing one budget, one kill switch, one log directory. A fleet does not fit in a terminal. You cannot watch five panes at once, you cannot watch any of them from your phone, and the moment you close the laptop the only window into your running loops goes dark.

The deeper problem is the autonomy dial. Back in that segment we set four notches per action, and notch three was surface-as-decision: the loop stops, presents the call with options and a recommendation, and waits for you. A terminal has no good way to do that. The loop blocks on a prompt nobody is watching, or it gives up and downgrades to notch one and ships something it should have asked about. The dial is only real if there is a channel the loop can escalate into and you can answer from anywhere.

Slack is that channel. It is the pipe the autonomy dial assumed existed.

[IMAGE: dark canvas, left side a cramped terminal with five overlapping panes and a tiny laptop, an X over it; right side a single clean Slack channel on a phone with three loops posting threads into it, a check mark over it]
![[loopy-slack-as-your-command-center-terminal-vs-slack-1.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-2.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-3.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-4.png]]
![[loopy-slack-as-your-command-center-terminal-vs-slack-5.png]]

---

## The core move: the channel is the new stdout

Stop thinking of Slack as a notification destination. Think of it as the loop's primary output stream when it is running unattended.

This is the same idea as the HTML artifact from the L2 segments, pushed one level up. There, the move was: don't make a loop talk to you in chat, make it write a self-contained file you can read in its final shape. Here the move is: when the loop is part of a fleet and running while you are asleep, route its decision points and milestones into a shared channel, and keep the routine tool spam in the terminal where it belongs.

Daniel San framed this sharply. Slack is not just a human UI, it is a transport layer between agents. He had one Claude writing into Slack to call another Claude instance for overnight incidents.
Source: https://x.com/dani_avila7/status/2054729819573654015

Hold onto that. It means a channel is not a dashboard you stare at. It is a bus. Loops post to it, you reply to it, and other loops can read from it. The command center and the agent transport are the same surface.

The mechanism is a Slack bridge running as an MCP server next to the loop, connected over Socket Mode, which is just a WebSocket so you need no public URL, no webhook, no port forwarding.
Source: https://github.com/sethbrasile/claude-slack-channel

The loop gets a small set of tools: reply, fetch the thread, react. That is the whole vocabulary. Outbound, the loop calls reply to post. Inbound, your messages arrive as notifications the loop reads back. The channel is now a two-way pipe.
Source: https://github.com/Reef-Digital/claude-code-slack/blob/main/README.md

---

## Three things a command center has to do

A real command center is not one feature. It is three, and they map straight onto primitives we have already built.

**It reports in.** Every loop mirrors its decision points, blockers, and milestone updates to the channel, while keeping routine output in the terminal. The good bridges tag each message with an audience field, operator or detail, so you see only what matters and the noise stays out of your face. This is the action-log review primitive from governance, except instead of you reading a JSONL file on a cadence, the important lines surface themselves into a thread as they happen.
Source: https://github.com/sethbrasile/claude-slack-channel

**It asks for approvals.** This is the autonomy dial wired to a button. When a loop hits something on notch three, an action it is not allowed to take alone, it posts the request in-thread with Approve and Deny buttons. You tap one, the message updates in place to show who acted, and the verdict is forwarded to the loop. It is not echoed back to the channel as chatter. The loop proceeds or aborts on your one tap, from your phone, without you opening a terminal.
Source: https://github.com/sethbrasile/claude-slack-channel

**It takes steering.** A reply in the thread continues the conversation. A new top-level message is a fresh command and abandons the old thread. That tiny state machine, top-level message starts a job, the loop's first reply opens a thread, your in-thread replies steer it, is the entire grammar of running a fleet by text.
Source: https://github.com/sethbrasile/claude-slack-channel

Report, approve, steer. That is the command center.

[IMAGE: dark canvas, a single Slack thread shown three ways stacked vertically, top labeled REPORT showing a milestone message, middle labeled APPROVE showing an Approve/Deny button pair, bottom labeled STEER showing a user reply feeding back into the loop]
![[loopy-slack-as-your-command-center-report-approve-steer-1.png]]
![[loopy-slack-as-your-command-center-report-approve-steer-2.png]]
![[loopy-slack-as-your-command-center-report-approve-steer-3.png]]
![[loopy-slack-as-your-command-center-report-approve-steer-4.png]]
![[loopy-slack-as-your-command-center-report-approve-steer-5.png]]

---

## Where the danger lives: the channel is now an actuator

Be careful here. The moment you wire Slack to approve actions, the channel stops being a read-only dashboard and becomes a way to drive the loop. Anyone who can reply through Slack can approve a tool call.

So the approval pipe has to be locked down the same way the kill switch is. The serious bridges gate the permission relay behind a sender allowlist, with a pairing step, and only the primary paired user can approve verdicts.
Source: https://github.com/eric108lucas/claude-code-slack-channel

This is the same governance instinct from the last segment, applied to a new attack surface. Budgets enforce in the runtime, not the prompt, because the model cannot count its own spend. Approvals enforce in the bridge, not the prompt, because the model cannot be trusted to decide who is allowed to approve it. The allowlist is a deterministic gate sitting outside the loop. A borrowed verifier for identity.

And there is one mode you must understand before you ship this. Auto Mode, or bypass-permissions, turns the whole relay off and lets the loop run everything. That is the right setting when you are at your desk and want zero friction. It is the wrong setting the instant the loop is unattended on a VM, because then the approval channel you so carefully built is doing nothing.
Source: https://github.com/eric108lucas/claude-code-slack-channel

The dial we set per-action means nothing if a global switch flattens it back to ship-silently while you sleep.

---

## Two patterns, do not confuse them

There are two completely different things people call "Claude in Slack," and picking the wrong one wastes a week.

Pattern one is attach-to-a-running-session. The bridge connects to the loop already open on your machine, with its working tree and in-progress context. You DM it "what's on the diff" and the same loop that has been working all morning answers. This is the command center for a fleet you are running. It is the one this segment is about.

Pattern two is spawn-on-demand. You @mention a bot in a channel, it detects intent, and it creates a fresh session on the web to handle that one request, posts progress, and hands you a Create PR button at the end. This is Anthropic's official Claude Code in Slack.
Source: https://code.claude.com/docs/en/slack

Both are useful. But pattern two is a front door for new work, closer to the L5 discovery and L4 worker triggers, where a Slack message is the thing that fills the queue. Pattern one is the governance surface for loops that are already alive. For a command center over a running fleet, you want pattern one, or pattern two pointed at a worker whose queue you feed from the channel. Naming the level wrong here, the same disease from the loop-stack segment, gets you building a ticket-spawner when what you needed was a steering wheel.

---

## Demo

On screen: one phone, three loops.

1. Start three loops on a VM from the laptop. The sentence-mining feeder, the YouTube outlier scout, and a bug-triage worker. Each one is configured with the Slack bridge MCP server pointed at the same `#fleet` channel. Close the laptop lid. Pick up the phone.

2. Watch them report in. Within a minute the scout posts a thread: "found one outlier on the watchlist, lift 3.2x over baseline, surfacing for decision." Tagged operator, so it is the only line you see, not the hundred lines of search it ran. This is notch three from the autonomy dial, arriving as a thread.

3. Approve an action. The bug-triage worker posts in-thread: "fix ready for the auth regression, eval suite re-ran green, no new failures. Ready to open PR." Two buttons, Approve and Deny. Tap Approve. The message updates in place: "approved by Ray." The worker opens the PR. You never touched a terminal.

4. Steer one. Reply in the scout's thread: "ignore anything from that channel, it is off-niche." The loop reads the reply and adjusts its next pass. Then post a brand-new top-level message: "kill the sentence-mining feeder for tonight." It abandons the old threads and treats this as a fresh command, dropping a `.fleet/KILL` poll on that one loop.

5. Show the lockdown. From a second account that is not on the allowlist, tap Approve on a pending request. Nothing happens. The verdict is rejected because only the paired primary user can approve. Read out the one line that enforces it.

Total demo: four minutes. The point is that the same channel did all three jobs, report, approve, steer, for three different kinds of loop, and the laptop was shut the entire time.

---

## Key Insight

> The terminal is where a loop is born. Slack is where it answers to you. Make the channel the loop's stdout, wire the autonomy dial to Approve and Deny buttons, and lock the approval pipe like a kill switch. Now you can run a fleet from your phone.

---

## Where we go next

You now have a command center. One surface where the fleet reports, asks, and obeys.

But reporting is not the same as keeping you genuinely in the loop. A channel that posts everything is just a faster way to be overwhelmed, and a channel that posts nothing is a fleet running blind. The next segment is about getting that signal right, what a loop should tell you, when, and at what altitude, so you stay informed without becoming the bottleneck again.

See you in the next one.
