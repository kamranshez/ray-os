---
source: "Master 95% of Claude Code in 40 mins (NEW + UPDATED)"
channel: Jack Roberts
video_id: DSKO9ZtbHFA
date: 2026-03-08
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Anti-Gravity (Google's IDE) as a Claude Code interface**: Jack extensively covers using Anti-Gravity, Google's coding IDE, as a visual interface for Claude Code. He shows how it provides a prettier UI, easier installation, and features like an "agent manager" with multiple parallel agents and project-specific contexts. Quote: "Anti-gravity provides a couple of really cool benefits. Number one is it's a beautiful visual interface to actually look at everything we're doing." Ray doesn't cover Anti-Gravity at all.

- **[HIGH] Website cloning workflow with Firecrawl + Nano Banana API**: Jack demonstrates a skill that scrapes a competitor website's HTML, rebuilds it with new AI-generated images using the Kia/Nano Banana API, scrapes competitor copy using Firecrawl, and serves it on localhost. This is a complete business workflow. Quote: "Ask the user about their niche and competitors. Scrape five competitor websites. Use as insights to improve the clone site structure." Ray doesn't cover this type of website rebuilding workflow.

- **[HIGH] Storing API keys in .zshrc as environment variables for skills**: Jack shows storing API keys (Firecrawl, Kia, Vercel, ImageBB) in .zshrc so skills can access them persistently. Quote: "The idea is we can store the environmental variables on your computer that your Claude skills can access. And the dot means they're not visible in the finder." Ray doesn't cover this environment variable approach for API key management across skills.

- **[HIGH] Publishing websites to Vercel directly from Claude Code**: Jack demonstrates having Claude Code create a private GitHub repo, push code to it, and deploy to Vercel using a Vercel API key -- all in one prompt. Quote: "I'd like you to publish this to Vercel. I'm going to give you my Vercel API key." Ray doesn't cover automated deployment workflows.

- **[MEDIUM] Scheduled tasks in Claude Code Desktop app**: Jack shows the new scheduled tasks feature in the Claude Code desktop app, creating a "daily code review" that runs every day at 9 AM to audit recent commits. Quote: "You can basically create a task that will run on repeat... daily code review... go over all the code that I created in the last 24 hours." Ray doesn't cover scheduled/recurring tasks.

- **[MEDIUM] Claude Connectors for email, calendar, Notion integration**: Jack demonstrates connecting Claude to Gmail, Google Calendar, Notion and other services via Connectors (built into Claude), then using those in Claude Code workflows. Quote: "We can connect Claude to all of your services, your email, your calendar, your notion database, anything you want to." Ray covers MCP servers for similar functionality but not the native Connectors feature.

- **[MEDIUM] ImageBB for image URL hosting in AI generation workflows**: Jack shows using ImageBB as an intermediary to upload images and get URLs that Nano Banana can use for image-to-image generation. This is a practical API chaining technique. Not covered by Ray.

- **[MEDIUM] HTML source code extraction for website cloning**: Jack demonstrates using an "HTML website extractor" tool to download a website's source code, then feeding it to Claude Code as a starting point. Quote: "Every website has a source code. So, you're going to come over and let's download this." Ray doesn't cover this website-as-input pattern.

- **[MEDIUM] Setting global rules in Anti-Gravity's rules/workflows UI**: Jack shows configuring rules like "always think around corners, challenge my thinking, don't be a sycophant" in Anti-Gravity's settings UI that persist across all projects. This is similar to user-level CLAUDE.md but through a GUI.

- **[LOW] Using the Claude Code desktop app's co-work mode**: Jack briefly shows the "co-work" mode in the Claude Code desktop app alongside "chat" and "code" modes. Ray covers Claude Code Desktop but may not cover co-work mode specifically.

- **[LOW] $500 skill competition / community skill sharing model**: Jack mentions running a $500 competition for the best Claude skill, with winning skills being added to a community marketplace. This is a community engagement model, not a technical gap, but interesting context about skill ecosystems.

Note: Much of Jack's video covers ground Ray already addresses well (installation, CLAUDE.md, skills, MCP, plan mode, permissions). The unique gaps are around Anti-Gravity integration, deployment workflows, and the website cloning business use case.
