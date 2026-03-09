---
tags: [competitor-analysis, gap-analysis, aakash-gupta]
date: 2026-03-09
---

## Source

- **Channel:** Aakash Gupta (with Carl Velli)
- **Videos:**
  1. "Claude Code Tutorial (1.5hr)" (4nthc76rSl8) -- beginner/intermediate
  2. "Claude Code Advanced Masterclass" (59gy_24KIVE) -- advanced features

## Gaps Ray's Course Does Not Cover

### PM-Specific Workflows: PRD Generation to Engineering Tickets [HIGH]

Aakash demonstrates a complete Product Manager workflow: write a PRD from a brief, push it to Google Docs via Google Workspace MCP, then convert PRD sections into Linear tickets with acceptance criteria, story points, and labels -- all from Claude Code.

> "We can take this PRD, push it to Google Drive, and then create engineering tickets in Linear directly from the requirements"

Ray's course has no PM-specific module or PRD-to-tickets pipeline. This is a major audience gap since PMs are a large potential user base for Claude Code.

---

### Linear MCP for Ticket Creation [HIGH]

Aakash installs and demonstrates the Linear MCP server, creating engineering tickets with:
- Title, description, acceptance criteria
- Story point estimates
- Label assignment
- Sprint/cycle assignment

Ray does not cover Linear MCP or any project management tool integration.

---

### Google Workspace MCP (Docs + Drive) [MEDIUM]

Aakash shows the Google Workspace MCP pushing generated documents directly to Google Drive, creating formatted Google Docs from Claude Code output.

Ray does not cover Google Workspace MCP or the workflow of pushing Claude Code output directly into Google Drive.

---

### Multi-Persona Review Agents (UXR Panel) [HIGH]

Aakash builds parallel review agents that each assume a different user persona (power user, casual user, accessibility-focused user, enterprise admin) and independently review a PRD or prototype. The personas debate and surface different concerns.

> "Each agent takes on a different persona... the power user cares about shortcuts, the enterprise admin cares about permissions"

Ray covers subagents but not the multi-persona review pattern applied to product/design review.

---

### Meeting Notes Custom Command [MEDIUM]

Aakash creates a custom slash command (`/meeting-notes`) that processes raw meeting transcripts into structured notes with action items, decisions, open questions, and owner assignments.

Ray covers custom commands but does not show a meeting notes processor as a use case.

---

### Gemini API Image Generation from Claude Code [MEDIUM]

Aakash demonstrates calling the Gemini Nano Banana Pro API from within Claude Code to generate images, using it for product mockups and presentation visuals.

> "We can actually generate images using Gemini's API... calling it right from Claude Code"

Ray does not cover image generation APIs called from within Claude Code.

---

### PowerPoint/Presentation Generation [MEDIUM]

Aakash uses a documents skills plugin to generate slide decks (PowerPoint format) from within Claude Code -- stakeholder decks, sprint reviews, product updates.

Ray does not cover presentation/slide generation as a Claude Code workflow.

---

### Claude GitHub App for Async Remote Work [MEDIUM]

Aakash demonstrates the Claude GitHub App -- creating issues and having Claude work on them asynchronously in the background, pushing PRs without a local terminal session.

> "You can assign Claude to a GitHub issue and it will work on it in the background, push a PR when it's done"

Ray does not cover the Claude GitHub App or async/remote Claude Code workflows.

---

### Hooks for Automated Quality Gates [MEDIUM]

Aakash explains hooks that run automatically before/after Claude Code actions -- linting, test running, format checking -- as automated quality gates.

Ray covers hooks but Aakash frames them specifically as "quality gates" in a PM context (ensuring PRDs meet a template, tickets have required fields).

---

### Session Naming and Resume [LOW]

Aakash shows naming sessions for later retrieval (`claude --resume session-name`) and organizing work across multiple named sessions.

Ray may touch on this but Aakash makes it a deliberate workflow practice.

---

### Reddit MCP for User Research [LOW]

Aakash demonstrates the Reddit MCP for pulling user feedback, feature requests, and sentiment from subreddits as input to product decisions.

Not covered in Ray's course.

---

### Slash Commands as Stored Prompts (Explicit Framing) [MEDIUM]

Aakash explicitly frames custom commands not as "commands" but as "stored prompts you can invoke" -- reusable prompt templates for recurring tasks. He creates several:
- `/prd` -- generate a PRD from a brief
- `/meeting-notes` -- process transcript
- `/uxr-panel` -- run multi-persona review

Ray covers custom commands but this explicit "stored prompt" mental model and the breadth of examples is more developed.

---

### Qualtrics MCP Mention [LOW]

Brief mention of Qualtrics MCP for pulling survey data into Claude Code for analysis. Not demonstrated in depth but signals an enterprise survey integration gap.
