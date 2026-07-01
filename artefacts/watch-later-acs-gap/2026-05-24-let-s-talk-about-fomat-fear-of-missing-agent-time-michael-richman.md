---
title: "Let's Talk About FOMAT: Fear of Missing Agent Time — Michael Richman, Cmd+Ctrl"
video_url: https://www.youtube.com/watch?v=W-SX_srBa3Y
video_id: W-SX_srBa3Y
channel: AI Engineer
published: 2026-05-24
status: covered
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Let's Talk About FOMAT: Fear of Missing Agent Time — Michael Richman, Cmd+Ctrl**](https://www.youtube.com/watch?v=W-SX_srBa3Y) - AI Engineer - uploaded 2026-05-24

> Already covered by ACS: native push notifications, remote control, and Agent View.

This is a conference talk demoing Michael Richman's Cmd+Ctrl, a control plane that pushes a notification when a coding agent blocks or finishes, lets you reply from your phone or watch, starts new sessions remotely, and unifies Claude Code, Cursor, Codex, and Gemini CLI sessions in one UI via an open-source daemon. The spine is the FOMAT reframe: the bottleneck on long-running agents is not the agent's speed but your latency to unblock it, so you need a notification loop rather than guessing when to check back.

That spine is directly covered by **"Push Notification Tool"** (Master Claude Code, Advanced chapter), which teaches `/remote-control`, desktop and mobile push, explicit PushNotification use, and pairing alerts with monitors: the exact "tell me when the agent needs me and respond from anywhere" workflow. The companion "many sessions, single pane of glass" idea is covered by **"Agent View"** (Master Claude Code, Advanced) for managing, peeking at, and replying to many sessions by state, and completion alerts are covered by **"Make Claude Speak to You"** (Hooks) and remote triggering by **"Claude Code for Slack"**.

What is not already an ACS video is the cross-tool, cross-machine control plane and the "agent choreography is the new flow / protect your breaks" framing, but the former is a specific third-party product rather than a film-able Claude Code technique, and the latter is thin commentary with no demo. No buildable net-new ACS video here.
