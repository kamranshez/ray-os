---
date: 2026-02-25
hook: "anthropic just turned your phone into a remote for your computer."
archetype: The News + Insight
media: text only
status: posted
engagement:
  reactions: 9
  comments: 2
  reposts: 2
  impressions: 1516
  last_checked: 2026-05-22
url: https://www.linkedin.com/feed/update/urn:li:activity:7432426590422343680/
notes: Based on remote control video (y3xzYwxQuHc). Covers claude rc, phone control, security/sandbox angle, Hetzner server tip. Decent engagement but slightly below COBOL post — longer/more technical posts may lose some readers.
---

anthropic just turned your phone into a remote for your computer.

claude code shipped remote control. you run `claude rc` in a folder on your machine, open the Claude app on your phone, and you're coding from anywhere.

i tested it by having it edit a video for me while i started a second session on another project. from my phone. sitting on my couch.

here's what makes it actually useful:

→ all your skills, MCP servers, and config carry over. whatever you've set up locally just works remotely.

→ you can approve permissions from your phone. no more SSH + tmux hacks.

→ plan mode works too. so you can kick off research tasks on the go and answer follow-up questions from lunch.

the security angle is the interesting part though.

if you don't want to run bypass permissions on your main machine, spin up a $3.50/month Hetzner server. install claude code there. run it with dangerously skip permissions in a sandbox. set up a proxy that only allows specific URLs.

now you have a remote research agent that can't touch your local files. even if it gets prompt injected, the blast radius is one throwaway server.

the one thing it's missing vs OpenClaw: it's passive, not proactive. you tell it what to do. it doesn't ping you on a schedule.

but given how fast anthropic is shipping, i'd bet that's coming.
