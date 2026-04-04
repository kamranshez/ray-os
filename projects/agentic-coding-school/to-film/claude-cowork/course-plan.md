---
tags: [course-plan, claude-cowork]
date: 2026-04-04
---

## Competitive Landscape

7 videos analyzed (Mar–Apr 2026):

| # | Creator | Title | Date | Focus |
|---|---------|-------|------|-------|
| 1 | Tech With Tim | Full Course for Beginners | Mar 31 | Setup, Chrome ext, browser automation, skills, scheduled tasks |
| 2 | Jack Roberts | 5 INSANE Use Cases | Apr 3 | Computer use, dispatch/mobile, projects, presentations, email triage, dashboards |
| 3 | Bart Slodyczka | Better Than 99% of People | Mar 16 | Setup, MD files, folder structure, invoice demo → skill → scheduled task |
| 4 | Jack Roberts | FULL COURSE (Automate Everything) | Mar 10 | Comprehensive: pricing, setup, connectors, skills, MCP, Zapier hack |
| 5 | Brock Mesarich | Work While I Sleep | Mar 11 | Scheduled tasks, morning brief, end-of-day wrap-up, Zapier MCP |
| 6 | Ryan & Matt | Projects Step-by-Step | Mar 22 | Projects deep dive, memory, scheduled tasks within projects |
| 7 | Mikey Ranks | Full Tutorial for Beginners | Mar 3 | Comprehensive beginner, file mgmt, integrations, MCP, chained workflows |

### Detailed Competitor Breakdown — What Each Video Covers & Key Demos

**Video 1 — Tech With Tim** (tf_KmDNZXzI)
- Explains CoWork needs desktop app + paid plan (Pro $20 or Max $100/$200)
- CoWork only works when computer is on + desktop app open
- Can use from mobile via Dispatch feature
- Shows three tabs: Chat | Code | CoWork
- Demo: desktop cleanup with color-coded folders (basic)
- Sessions are independent — no memory between them (unless using Projects)
- Shows creating a Project with memory panel
- Chrome extension setup + pairing
- Demo: opens YouTube, reads recommended videos, clicks into them, extracts stats + comment sentiment
- Demo: flight search on Google Flights (parallel sub-agents)
- Key quote: "Code can pretty much do everything CoWork can do. The real difference is who it's designed to be used by."
- Mentions skills, scheduled tasks briefly

**Video 2 — Jack Roberts** (isjOj4QSaO8) — "5 INSANE Use Cases"
- **Use Case 1: Computer Use + Dispatch** — demos navigating Granola app to find trial extension, then Canva design extraction from phone via Dispatch. Key: "MCPs first, files second, desktop intelligence as a last resort."
- **Use Case 2: Projects** — persistent memory, LinkedIn growth project. Downloads LinkedIn data archive, uploads viral hooks PDF, creates content rules. Good demo of building up project context over time.
- **Use Case 3: Presentations** — slide deck creation with image gen via Kria API (Nano Banana 2). Brand logos, custom characters. Creates HTML presentations.
- **Use Case 4: Email Triage** — morning brief + Gmail connector. Categorizes emails, drafts responses. "You go from the creator to the simple approver." Scheduled at 9am and 5pm.
- **Use Case 5: Analytics Dashboards** — connects Mercury bank, creates revenue dashboards. Interactive with charts, tabs. Emphasizes connecting ALL data sources via MCP.

**Video 3 — Bart Slodyczka** (vMo-yRCN3QM) — "Better Than 99%"
- Chat vs Code vs CoWork framing: "Chat is assistant, Code is developer, CoWork is employee"
- **Key demo: Invoice processing** — reads invoices, sorts into category subfolders, creates Excel with formulas (not hallucinated totals). Good demo of real file manipulation.
- **Skill creation flow**: does the task manually first, then says "turn this process into a reusable skill using your skill creator tool"
- **Scheduled task**: attaches the invoice skill to run every Monday at 9am
- **Folder structure**: creates context/, projects/, output/ subfolders with readme files
- **MD files**: creates about-me.md, brand-voice.md, working-preferences.md — asks follow-up questions to fill them out
- **Global instructions**: tells CoWork to read MD files at start of every session
- **Skills v2 mention**: "skills now evaluate against criteria and get you involved to optimize before deploying"
- Connectors + plugins overview: Apollo plugin for sales (prospecting, enrichment, sequences)

**Video 4 — Jack Roberts** (cNf7uVff11Y) — "FULL COURSE"
- Most comprehensive of all 7. Chapters: when to use what, pricing, setup, first tasks, connectors, skills, building custom skills
- **When to use what**: Chat for Q&A, Code for devs, CoWork for operators. CoWork = "middle ground for non-technical operators"
- **Pricing**: Pro works for regular use, Max for power users. 5x limit difference.
- **Setup**: global instructions, folder structure, first project
- **Connectors deep dive**: Gmail, Slack, Drive, Calendar. Shows permission granularity (read/write/delete per tool)
- **Zapier MCP hack**: zapier.com/mcp → create MCP server → select tools (School, Zendesk, etc) → copy URL → paste into Claude. Workaround for any unsupported app.
- **Skills**: building custom skills, skills marketplace, skill evaluation
- **Computer Use**: Canva design retrieval, form filling
- **Token management**: warns about scheduled tasks burning credits, recommends strategic scheduling

**Video 5 — Brock Mesarich** (Namp-sV0UEw) — "Work While I Sleep"
- Focuses on the skills → scheduled tasks pipeline
- **Claude.md concept**: "a file that tells Claude everything about you — it reads this every single time"
- **Morning briefing skill**: pulls calendar, email, news → generates HTML dashboard. Shows the actual HTML output.
- **End-of-day wrap-up**: summarizes what CoWork did (11 activities listed), what's unfinished, tomorrow's priorities, day reflection.
- **Connectors**: Gmail, Slack, Google Calendar, Zapier
- **Zapier MCP**: same hack as Jack Roberts — connect unsupported tools via Zapier
- **Scheduled tasks**: morning brief at 7am daily, shows creating + managing
- **Sharing skills**: downloads markdown file from Google Drive, uploads to CoWork
- **Key limitation**: "scheduled tasks only operate when your Claude desktop app is open and your computer is turned on"

**Video 6 — Ryan & Matt** (MCMkmshUN8U) — "Projects Step-by-Step"
- **Projects deep dive** — the most focused coverage of projects across all 7 videos
- **Key distinction**: selecting a folder ≠ creating a project. Folder = file access only. Project = file access + instructions + memory + scheduled tasks + dedicated UI.
- **Memory demo**: tells Claude "sales are up 100% month over month" → shows it saved in memory panel → starts new conversation → Claude recalls it
- **Instructions editing**: uses pencil icon, notes the editing space is small → recommends writing externally and pasting in
- **Scheduled tasks within projects**: creates "daily motivation" at 10am weekdays, uses Haiku model for simple tasks
- **Project location**: defaults to Documents/Claude/Projects folder on disk
- **Navigation quirk**: getting back to projects requires going through search → find conversation → click back into project. Expects UI improvement.

**Video 7 — Mikey Ranks** (stEVjMHMt-Q) — "Full Tutorial for Beginners"
- Most methodical/structured of all 7
- **Three modes**: Chat = thinking partner, Code = developer, CoWork = bridge between thinking and execution
- **Permissions**: "do not grant everything just because it's faster. Give it access only to what you need."
- **File organization demo**: Downloads folder cleanup — scan → plan → execute → report. Batch processing with parallel agents.
- **MCP servers**: explains Model Context Protocol, connecting Notion via remote MCP URL
- **Browser automation**: controlled background browser sessions, web research
- **Plugins & skills**: plugins = specialized modules, skills = reusable workflows, community skills via SkillHub
- **Chained workflows**: "research competitors → extract pricing → generate comparison → draft strategy" in one instruction
- **Security**: permission-based file access, OAuth for integrations, connect only what you need

### What EVERY competitor covers (saturated)

- Chat vs Code vs CoWork comparison
- Setup basics (desktop app, plans, folder access)
- File organization / desktop cleanup demos
- Basic skill usage and creation
- Scheduled tasks intro
- Native connectors (Gmail, Calendar, Drive)
- "AI employee" positioning
- Morning briefing demo (4 out of 7 do this)
- Zapier MCP workaround (3 out of 7)

### What's MISSING or surface-level across all 7

1. **Skill creation mastery** — everyone shows 1 basic skill, nobody teaches parameterized, composable skills
2. **Skill debugging & iteration** — zero coverage of what to do when a skill fails
3. **Multi-skill workflows** — nobody chains skills together
4. **Claude.md mastery** — Brock mentions it, Bart creates MD files, but nobody explains the instruction hierarchy (global → project → task)
5. **MCP server creation** — they connect MCPs, nobody builds one
6. **Advanced computer use** — Jack Roberts demos Granola + Canva but it's a novelty demo, not a workflow
7. **Token optimization** — everyone warns about limits, nobody teaches strategies
8. **Error handling** — zero coverage of recovery when things break
9. **Real business workflows** — most demos are toy examples (organize desktop, draft email, color-code folders)
10. **Code ↔ CoWork bridge** — Bart mentions "use scripts to save tokens" but doesn't go deep
11. **Dispatch mobile depth** — Tim and Jack mention it, neither dedicates real time
12. **Custom connectors** — only via Zapier hack, nobody builds a real MCP
13. **Projects architecture** — Ryan & Matt best coverage, still surface-level

### Specific Demos to Steal / Adapt (with improvements)

| Competitor Demo | What They Did | How to Improve |
|----------------|---------------|----------------|
| Tim: YouTube research via Chrome | Opens YT, reads recs, extracts stats | Do competitor analysis: titles, view counts, gaps — more actionable |
| Tim: Google Flights search | Finds flights, parallel sub-agents | Show sub-agent spawning explicitly, explain how to force parallel |
| Jack R: Canva design from phone (Dispatch) | Gets design, emails it | Chain: find design → modify → email → confirm on phone |
| Jack R: Analytics dashboard (Mercury) | Creates revenue dashboard | Connect real data source, show interactive filters, export |
| Jack R: Email triage 2x/day | Categorize + draft at 9am and 5pm | Build as skill first, then schedule — show the skill file |
| Bart: Invoice → skill → schedule | Manual task → convert to skill → schedule Monday 9am | Show the skill MARKDOWN file, test it, iterate, then schedule |
| Bart: MD files (about-me, brand-voice, working-prefs) | Creates 3 files with Q&A process | Show the hierarchy: global instructions → project instructions → CLAUDE.md → task |
| Brock: Morning brief HTML dashboard | Calendar + email + news → HTML output | Build incrementally: start basic, iterate 3 times, show before/after |
| Brock: End-of-day wrap-up | What CoWork did, what's open, tomorrow | Include token usage for the day, cost awareness |
| Ryan & Matt: Memory demo | Tell Claude a fact → new convo → recalls | Show memory building over a WEEK (timelapse), not just one fact |
| Mikey: Chained workflow | Research → extract → compare → draft | Build each step as a separate skill, then chain them |

---

## Course Structure: 11 Videos

See individual script files (01–11) for full scripts.

| # | Title | Length | Key Demos |
|---|-------|--------|-----------|
| 01 | What is Claude CoWork + Installation | ~10 min | Install, tour interface, first test |
| 02 | Your First Folder & Task | ~14 min | Messy Downloads cleanup, PDF invoice summary |
| 03 | Chat vs Code vs CoWork | ~13 min | Same task in all 3, decision framework table |
| 04 | Projects & Memory | ~15 min | Amnesia demo, create project, memory across conversations |
| 05 | Instructions & Claude.md | ~14 min | 3-layer hierarchy, before/after comparison, CLAUDE.md file |
| 06 | Connectors | ~15 min | Gmail/Calendar/Drive/Slack, morning briefing, email triage, meeting prep |
| 07 | Browser Automation | ~15 min | AI tool research, YouTube competitor analysis, flight search |
| 08 | Skills | ~16 min | Manual → skill conversion (invoices), manual skill writing, testing |
| 09 | Scheduled Tasks | ~15 min | Morning brief + invoice + end-of-day, token budgeting |
| 10 | Computer Use & Dispatch | ~16 min | Navigate desktop apps, form filling, mobile dispatch |
| 11 | Putting It All Together | ~22 min | Build complete system live: project + connectors + 4 skills + 4 schedules |

**Total: ~165 min (~2.75 hours)**
