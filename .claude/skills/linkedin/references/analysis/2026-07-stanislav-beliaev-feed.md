---
tags: [linkedin, competitor-analysis, feed-dump]
date: 2026-07-18
---

# Stanislav Beliaev — Recent Activity Feed Dump

Source: https://www.linkedin.com/in/stasbel/recent-activity/all/
Captured 2026-07-18 from Ray's logged-in LinkedIn view via Chrome automation. 13 posts, spanning ~20h to ~1mo old (Stanislav posts far less frequently than Linas; the feed stopped loading past 1mo after repeated retries). Engagement counts are as-displayed at capture time. "?" reactions = LinkedIn rendered the count as an icon-only element the scraper could not resolve (post still had reactions). Post 3 is a repost of Post 4 (same LibrePods content) and shows identical engagement; both are kept as captured. Stanislav is Co-Founder & CTO at GetFluently.App (YC W24), ex-Nvidia; every post carries the same GetFluently CTA P.S. block.

## Post 1 — 20h ago

- **URN:** urn:li:activity:7483877837754585088
- **Type:** Original
- **Engagement:** ? reactions · 51 comments · 66 reposts
- **Media:** video
- **Links:** https://getfluently.app/ , https://lnkd.in/dC7VMWxP , http://getfluently.app/

**Full text:**

China open-sourced a model that turns any regular video into a live 3D scene, in real time:

One camera. No LiDAR. No calibration rig.
Point it at a room, walk around, and watch the whole space get rebuilt in 3D as you go.

Robbyant released LingBot-Map, a feed-forward 3D foundation model. Every frame is one forward pass, so it never stops to optimize or clean up after.

Most streaming models slow down because they store every past frame. LingBot-Map keeps just three compact pieces instead:
- an anchor for coordinate grounding
- a local window for nearby geometry
- a trajectory memory for long-range drift

That keeps per-frame context small, which is why it stays fast even as history piles up.

→ ~20 FPS at 518×378 on a single GPU
→ holds steady past 10,000 frames
→ handles drone, driving, and indoor video
→ beats streaming and offline methods on benchmarks

They even pushed a 13-minute, ~25,000-frame indoor walkthrough to show it holds up over long sequences.

Link to the repo: https://lnkd.in/dC7VMWxP

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 2 — 2d ago

- **URN:** urn:li:activity:7483161428913446912
- **Type:** Original
- **Engagement:** 1,773 reactions · 79 comments · 151 reposts
- **Media:** image
- **Image alt text:** graphical user interface, website
- **Links:** https://getfluently.app/ , https://lnkd.in/dXCZKiza , http://getfluently.app/

**Full text:**

This repo just hit 87k+ stars 🔥 It maps your entire project - code, docs, PDFs, images, videos - into one queryable knowledge graph:

It’s a skill called Graphify. Point it at any folder and one command builds a knowledge graph. It skips vector databases and embeddings entirely.

It processes:
→ Code in 40+ languages via tree-sitter, all local
→ SQL schemas, shell scripts, Markdown docs
→ PDFs, images, and videos

Three main outputs:
- Interactive HTML graph for the browser
- Markdown report of key concepts and surprising connections
- JSON graph you can query directly

The graph maps your full project and every link is tagged EXTRACTED, INFERRED, or AMBIGUOUS, so you can tell what it actually found from what it guessed.

It also sticks around. Build it once, then ask questions in plain English weeks later - "what connects attention to the optimizer?" - and re-runs only update the files that changed, so it stays cheap to keep current.

The payoff is token cost - community reports of 70–80× fewer tokens per query vs. reading the full codebase.

Works with Claude Code, Codex, Cursor, Gemini CLI, and more.

Link to the repo: https://lnkd.in/dXCZKiza

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 3 — 1w ago

- **URN:** urn:li:activity:7481762571369283584
- **Type:** REPOST/context: Stanislav Beliaev reposted this
- **Engagement:** 3,080 reactions · 95 comments · 102 reposts
- **Media:** image
- **Image alt text:** graphical user interface
- **Links:** https://getfluently.app/ , https://lnkd.in/d8HMcg8t , http://getfluently.app/

**Full text:**

Someone reverse-engineered the AirPods protocol and unlocked Apple's exclusive features on non-Apple devices 😳

It's called LibrePods. It reimplements Apple's proprietary AirPods protocol, and can spoof the Device ID so your AirPods think you're on an iPhone.

A lot of what Apple locks to iOS now runs on Android and Linux:

→ noise control modes
→ transparency tuning & hearing aid (Android)
→ ear detection with auto pause/resume
→ head gestures, nod to answer calls (Android)
→ multi-device switching
→ rename AirPods, customize gestures
→ battery status + accessibility settings

On supported Android (16 QPR3+, like recent Pixel, OnePlus, Oppo, Realme) it runs without root - it's on the Play Store. The VendorID spoof (Apple's 004C) is optional and unlocks a few extras, flagged use-at-your-own-risk.

The point is simple: you paid for the hardware, you should own the features.

LibrePods just crossed 28k+ stars on GitHub.

Link to the repo → https://lnkd.in/d8HMcg8t

Your thoughts?

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 4 — 1w ago

- **URN:** urn:li:activity:7481390492962791424
- **Type:** Original (Post 3 is a repost of this)
- **Engagement:** 3,080 reactions · 95 comments · 102 reposts
- **Media:** image
- **Image alt text:** graphical user interface
- **Links:** https://getfluently.app/ , https://lnkd.in/d8HMcg8t , http://getfluently.app/

**Full text:**

Someone reverse-engineered the AirPods protocol and unlocked Apple's exclusive features on non-Apple devices 😳

It's called LibrePods. It reimplements Apple's proprietary AirPods protocol, and can spoof the Device ID so your AirPods think you're on an iPhone.

A lot of what Apple locks to iOS now runs on Android and Linux:

→ noise control modes
→ transparency tuning & hearing aid (Android)
→ ear detection with auto pause/resume
→ head gestures, nod to answer calls (Android)
→ multi-device switching
→ rename AirPods, customize gestures
→ battery status + accessibility settings

On supported Android (16 QPR3+, like recent Pixel, OnePlus, Oppo, Realme) it runs without root - it's on the Play Store. The VendorID spoof (Apple's 004C) is optional and unlocks a few extras, flagged use-at-your-own-risk.

The point is simple: you paid for the hardware, you should own the features.

LibrePods just crossed 28k+ stars on GitHub.

Link to the repo → https://lnkd.in/d8HMcg8t

Your thoughts?

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 5 — 1w ago

- **URN:** urn:li:activity:7481285844574633984
- **Type:** Original
- **Engagement:** ? reactions · 77 comments · 119 reposts
- **Media:** image
- **Image alt text:** No alternative text description for this image
- **Links:** https://getfluently.app/ , https://lnkd.in/d-a3carw , http://getfluently.app/

**Full text:**

Someone shipped an open-source alternative to ElevenLabs + WisprFlow that runs locally:

It’s called voicebox, and it already hit 40k+ stars on GitHub.

Give it a short clip of your voice, and it clones how you sound. From there, any AI agent connected to it can speak back to you in that voice.

What it does:
- Clones your voice from a short reference clip
- Global dictation hotkey backed by Whisper
- Text-to-speech across 23 languages and 7 TTS engines
- Built-in MCP server for Claude Code, Cursor, Cline, Windsurf
- Runs on Mac, Windows, Linux, and Docker

Useful for dictating commits, tickets, and docs anywhere on your OS, shipping voice agents without a paid TTS API, or recording voiceovers in your own voice across 23 languages.

Everything runs locally. No API keys, no per-character billing, no voice data sent anywhere.

Link to the repo: https://lnkd.in/d-a3carw

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 6 — 3w ago

- **URN:** urn:li:activity:7476262527320875008
- **Type:** Original
- **Engagement:** 3,299 reactions · 126 comments · 283 reposts
- **Media:** video
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

Mistral AI just released the best OCR model 🔥
It turned a handwritten calculus exam into clean LaTeX in 5.1 seconds:

Every formula came back rebuilt exactly right - integrals, fractions, limits - for $0.09.

The graph didn't get redrawn. Most OCR tools dump the text and drop the figure. OCR 4 caught the plot, boxed it, and tagged it as a chart instead of losing it.

And it doesn’t just read text. It understands the entire document structure.

OCR 4 detects equations, tables, signatures, titles, charts, and returns bounding boxes with confidence scores for every region. That makes it much more useful for RAG pipelines, enterprise search, citations, and document processing than traditional OCR.

Independent annotators blindly ranked 600+ documents across 12+ languages and preferred OCR 4 over every system tested - 72% win rate. It tops OlmOCRBench at 85.20 and covers 170 languages.

Runs in a single container. Fully self-hosted. $2 per 1,000 pages on batch.

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 7 — 3w ago

- **URN:** urn:li:activity:7475478892145709057
- **Type:** Original
- **Engagement:** ? reactions · 96 comments · 55 reposts
- **Media:** image
- **Image alt text:** text, letter
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

A senior engineer on Reddit explained ONE skill he'd teach every vibe coder first. It quietly saves money on every project:

Get the agent to write plain deterministic code, then run that code for free.

When your only tool is an LLM agent, every problem looks like a prompt that burns tokens to run. But most of that work doesn't need one. Pay tokens once to have it write the code, then run it a million times for nothing.

Say you want to know when a website posts an update:

→ Agent way: an LLM checks the page daily. Handles layout changes, but burns tokens every run, and it's slower.

→ Deterministic way: the agent writes a small scraper that stores the page text and diffs it against yesterday's. Breaks if the site gets redesigned, and you wire up the cron job yourself. Runs forever at zero token cost.

Same job. One keeps charging you, one you pay for once.

It won't fit everything - plenty of problems still need an LLM in the loop. But for the repeatable stuff, this changes the math.

Years ago this engineer hand-wrote a classifier to spot SpongeBob in photos, and it took weeks of ugly code. Last night he handed Claude Code his old images and it built a better one while dinner was on the stove. It runs on his machine, no tokens.

Spend tokens once to build the tool. Then run it free, forever.

Your thoughts?

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 8 — 3w ago

- **URN:** urn:li:activity:7474776368434667521
- **Type:** Original
- **Engagement:** 298 reactions · 34 comments · 30 reposts
- **Media:** document
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

Free 36-page guide from Anthropic on how to build an AI startup with Claude 🔥

Anyone can build fast now. The harder part is knowing what's worth building - and most founders are just using AI to ship things nobody wants, faster.

This guide walks every stage of startup journey and shows exactly where Claude fits, with the exercises and frameworks to build something people actually stick with:

🔸 Idea: validate the problem and competitors before writing code
🔸 MVP: architecture and security that keep the codebase clean
🔸 Launch: run ops with agentic workflows instead of hiring
🔸 Scale: keep users in and the product hard to replace

Every stage comes with hands-on work - customer discovery, code architecture, security reviews, GTM - plus a matrix for when to reach for Chat, Cowork, or Claude Code, and real founder stories from successful AI startups.

If you're building anything with AI right now, this will save you from the mistakes that quietly kill startups before they get traction.

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

--
♻️ Save this and share with other founders in your network!

---

## Post 9 — 1mo ago

- **URN:** urn:li:activity:7472686502091816961
- **Type:** Original
- **Engagement:** 561 reactions · 29 comments · 66 reposts
- **Media:** video
- **Links:** https://getfluently.app/ , https://lnkd.in/d4Ehj6TT , http://getfluently.app/

**Full text:**

NVIDIA made object detection ~10x faster by changing one thing:

How the model writes coordinates.

Most vision-language models locate an object by spelling out its box as text. One coordinate token, then the next, strictly in order. That sequential step is where a lot of the latency hides.

LocateAnything drops the sequence. Each bounding box becomes one atomic unit. All four coordinates come out in a single forward pass.

It was trained on 138M language queries and 785M boxes, spanning detection, GUI grounding, OCR, and pointing in one model.

What that buys you on a single H100:
→ 12.7 BPS throughput, ~10x faster than Qwen3-VL
→ 50.7 F1 on LVIS, +14.5 over Rex-Omni on M6Doc
→ beats GUI-Owl-32B on ScreenSpot-Pro, a model more than 10x its size

And it stays reliable. If a box comes out wrong, that block gets re-decoded one token at a time, then flips back to fast mode.

It's also a quiet reframe of the problem. A box was being read like a sentence, left to right, when its four corners had no order at all.

Makes you wonder what else we decode token by token out of pure habit.

Link to the repo 👉 https://lnkd.in/d4Ehj6TT

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 10 — 1mo ago

- **URN:** urn:li:activity:7472293401292636160
- **Type:** Original
- **Engagement:** 458 reactions · 51 comments · 36 reposts
- **Media:** image
- **Image alt text:** graphical user interface, text, application, email
- **Links:** https://getfluently.app/ , https://lnkd.in/dtmEEx5m , http://getfluently.app/

**Full text:**

A dev got tired of his AI agent turning 5-line problems into 50-line pull requests. So he built a skill to stop it:

It's called Ponytail, and it makes your coding agent reach for the simplest thing that works. Ask for a date picker and most agents install a library, write a wrapper, add a stylesheet, and debate timezones. Ponytail makes the agent write <input type="date"> and move on.

The trick: before writing anything, it looks for a reason not to. Does this need to exist? Can stdlib or a native feature handle it? Can it be one line? It stops at the first answer that holds.

On the repo's benchmark, median across Haiku, Sonnet, and Opus:
→ 80-94% less code
→ 47-77% cheaper
→ 3-6× faster

It stays lazy where laziness is free and careful where it counts. Validation, data-loss handling, security, and accessibility never get cut. Every shortcut it does take leaves a ‘ponytail:’ comment naming the upgrade path, so the debt stays findable.

Works with 13 agents. MIT licensed.

Link to the repo 👉 https://lnkd.in/dtmEEx5m

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 11 — 1mo ago

- **URN:** urn:li:activity:7470842760808325120
- **Type:** Original
- **Engagement:** ? reactions · 38 comments · 10 reposts
- **Media:** image
- **Image alt text:** graphical user interface
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

Engineer used Claude to build a “coworker stress leaderboard” showing who caused him the most stress by syncing his WHOOP and calendar data 😳

@the2ndfloorguy shared this on X - says he checks it daily.

Here's what how he did:
→ had Claude reverse engineer the API to pull per-minute heart rate
→ his calendar supplied the events, their time windows, and the attendee lists
→ each heart rate spike got matched to the meeting running at that minute, then pinned on the people in it

What comes out is a ranked list of coworkers by how much each one spikes him. Names blurred, for obvious reasons.

People have tracked HR and HRV for years. The twist here is what he lined it up against - the actual person across from you when your heart rate jumps.

Health trackers just hit a new level… now they tell you which coworker is bad for your health 😅

Your thoughts?

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 12 — 1mo ago

- **URN:** urn:li:activity:7470757502121402368
- **Type:** Original
- **Engagement:** ? reactions · 58 comments · 118 reposts
- **Media:** image
- **Image alt text:** No alternative text description for this image
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

A French engineer in Paris has spent 25 years writing the software the entire internet runs on. Almost nobody knows his name.

He wrote the code that streams every YouTube video, every Netflix show, every TikTok clip. He wrote the code the cloud spins your virtual servers up on. He once beat a multi-million-dollar supercomputer at calculating pi - on a desktop PC.

His name is Fabrice Bellard.

Born in France. He never moved to Silicon Valley or raised a round. He just writes code.

In 2000, at 28, he started FFmpeg - one library that decodes every audio and video format on every OS. Today it powers video almost everywhere - VLC, Chrome, phones, smart TVs. If you've watched anything on a screen this decade, FFmpeg touched it.

In 2003 he started QEMU, an emulator that lets one operating system run inside another. He wrote it solo through 2005. KVM sits on top of it, and AWS, Google Cloud, and Azure all run virtual machines on infrastructure built around it.

Then he just kept going:
→ Built TCC, a C compiler that boots a Linux kernel in under 15 seconds
→ Created JSLinux, a PC that runs Linux in your browser, in pure JavaScript
→ Released QuickJS, a JS engine that fits where V8 can't
→ Computed pi to 2.7 trillion digits on a $3,000 desktop, beating machines worth millions

On top of all this, he co-founded Amarisoft in 2012 and remains its CTO, building the 4G and 5G base-station software used by carriers and labs worldwide.

For 25 years Bellard has done the same thing - pick a brutally hard problem, crack it on his own, give the code away. He's barely online. His website is a flat list of projects with no styling, just titles and links.

In December 2025, at 53, he shipped Micro QuickJS - a JavaScript engine that runs in about 10KB of RAM, small enough for a microcontroller.

Still curious. Still building. Still shipping.

Absolute legend.

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---

## Post 13 — 1w ago

- **URN:** urn:li:activity:7480941382032011264
- **Type:** Original (out-of-order in feed; timestamp shown as 1w)
- **Engagement:** 447 reactions · 48 comments · 22 reposts
- **Media:** image
- **Image alt text:** timeline
- **Links:** https://getfluently.app/ , http://getfluently.app/

**Full text:**

🚨 SpaceXAI and Cursor JUST launched Grok 4.5 - a new frontier model built specifically for coding and AI agents:

Unlike most frontier LLMs that are optimized for many different tasks, Grok 4.5 was trained specifically for software engineering work. Cursor partnered directly with SpaceXAI during training, making it the first model developed together after the acquisition.

→ $2/M input tokens and $6/M output tokens
→ ~80 tokens/sec serving speed
→ ~2× better token efficiency than comparable frontier models
→ Fewer reasoning steps, reducing both latency and inference cost

The pricing is the biggest surprise.

SpaceXAI is positioning Grok 4.5 as a frontier coding model. Cursor is calling it Opus-class. Yet it runs at a fraction of the price of the premium models it matches - which changes the math on anything that loops through a model hundreds of times.

It backs that up on benchmarks:
→ SWE Marathon: 29% - the top score, ahead of Opus 4.8 and Fable
→ Terminal Bench 2.1: 83.3%
→ SWE Bench Pro: 64.7%

According to Cursor's CEO, Grok 4.5 has already become the go-to model for many engineers on their team and outperforms Composer 2.5 in everyday use.

Seems like developers just got another serious alternative in the AI coding race.

Your thoughts?

--
P.S. We’re building the best AI English tutor in the world. Try it to improve your speaking - it’s 15× cheaper than a human one → GetFluently.app

---
