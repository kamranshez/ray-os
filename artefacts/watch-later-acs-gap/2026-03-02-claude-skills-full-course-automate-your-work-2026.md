---
title: "CLAUDE SKILLS FULL COURSE: Automate Your Work (2026)"
video_url: https://www.youtube.com/watch?v=sduaTkhIm_w
video_id: sduaTkhIm_w
channel: Nick Saraev
published: 2026-03-02
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**CLAUDE SKILLS FULL COURSE: Automate Your Work (2026)**](https://www.youtube.com/watch?v=sduaTkhIm_w) - Nick Saraev - uploaded 2026-03-02

> Next-step video available: self-healing skills that rewrite their own definition after a failure are not in the catalog.

## The one idea worth a video

- **Skills self-anneal.** A well-specced skill is not a frozen SOP; on a runtime failure the agent fixes the problem and rewrites its own skill.md so the next run starts better. VERDICT: 🔗 next-step video available.
- **Any business SOP is already a skill.** Feed an existing SOP plus a compressed skill-spec and the agent emits the markdown skill; every business skill in the video is an instance of this. VERDICT: ✅ covered by the Skills chapter.
- **Browser-automation skills for API-less real-world tasks.** Chrome DevTools MCP drives a real logged-in browser to book desks, comparison-shop Amazon, order groceries, then saves the run as a reusable skill. VERDICT: 🟡 partial (different tool from ACS's Claude-in-Chrome coverage).

## Summary + counts

Nick Saraev walks through five revenue-focused Claude skills plus one-off personal automations, then teaches SOP-to-skill conversion, progressive disclosure, and self-annealing behavior for real business use.

🔴 0 net-new · 🔗 1 complement · 🟡 1 partial · ✅ 1 covered

## 🔬 Deep dive

**Spine 1: Skills self-anneal (self-healing skills).**
The claim: a skill instrumented correctly does not just fail loudly, it repairs itself and upgrades its own definition. Most people treat skill.md as a static script they hand-edit when it breaks; Nick's reframe is that the skill is a living asset that improves every run. The mechanism has real steps: because the skill executes inside an agent that holds file-write access, when a step errors (an API rate limit, a missing field, a service being down) the agent diagnoses the cause in context, patches the underlying script or step, and persists that fix back into the skill.md, so the next invocation begins from the improved version. In his inbox demo the script chokes on a subtotal row and the agent rewrites its own filtering logic mid-run. This generalizes cleanly to a CI test-repair loop or a data-pipeline runbook that appends a new edge-case handler each time it breaks. It goes wrong two ways: silent drift, where the skill rewrites itself in a direction you never wanted, so the fixes must live in version control for review; and it only self-heals if the spec explicitly instructs it to, otherwise the agent just errors out.

**Spine 2: Any business SOP is already a skill.**
The claim: building skills is not a new authoring discipline, it is format translation of content you already own. People assume skills demand fresh writing; Nick argues your checklists and SOPs are the raw material and the only gap is the agent's native format. The mechanism: skills are SOPs for agents the way checklists are SOPs for humans, and because an agent cannot reliably consume a raw checklist, you feed it a compressed skill-spec (Anthropic's docs shrunk from roughly five hundred to two hundred lines, dropped into CLAUDE.md) alongside the SOP, and it emits a correctly structured skill.md with frontmatter, then runs once to self-test. This generalizes to onboarding docs, support macros, any repeatable knowledge-work runbook. It goes wrong when SOP quality caps skill quality (garbage in, garbage out), and the hand-rolled spec file is now largely redundant given a dedicated skill-creator exists.

**Spine 3: Browser-automation skills for API-less real-world tasks.**
The claim: some of the highest-leverage skills are not code, they are thirty-second browser-automation skills that drive apps with no API. Non-obvious because people reserve agents for coding; Nick uses one to book a coworking desk thirty days ahead and to comparison-shop Amazon. The mechanism: Chrome DevTools MCP lets the agent control a real logged-in browser, so any task exposed only through a UI becomes automatable; you log in once, describe the task, and the successful run is saved as a reusable skill. It generalizes to grocery delivery, legacy-portal form filling, and recurring bookings. It goes wrong through brittleness to UI changes, credential and security handling, and being slower and less reliable than a real API whenever one exists.

## 🎬 Proposed ACS videos

**1. Skills That Fix Themselves: Building a Self Healing Claude Skill**
- HOOK: Your skill should not break the same way twice; teach it to patch its own definition the first time it fails.
- THE PROMISE: For anyone already shipping Claude skills, you will build one that diagnoses a runtime failure, fixes it, and rewrites its own skill.md so the next run is better.
- THE SHAPE:
  1. Run a working skill, then force a failure (an API rate limit or a changed field).
  2. Watch the agent diagnose and fix in context instead of aborting.
  3. Show it writing the fix back into skill.md, diffing the file before and after.
  4. Add the exact spec instruction that makes self-healing reliable rather than accidental.
  5. Guardrail: commit skills to git so you review self-edits, and cap what the skill may rewrite.
- SPINE: 1 (skills self-anneal).
- SLOT: Master Claude Code > Skills (or Advanced Techniques > Skills as Force Multipliers).
- RELATIONSHIP: 🔗 complements "Claude Code Skills", which teaches what skills are, progressive disclosure, and skill matching, by adding the self-improvement loop that video does not cover. State plainly that the base video already teaches the mental model so this one only teaches the failure-to-fix-to-persist cycle.
- PROOF TO REUSE: "they're self-annealing over time. They heal themselves. They get better and they improve constantly"; the inbox-cleaner demo where a script bug on the subtotal row gets auto-fixed mid-run; "if the agent finds a mistake while doing it... it'll automatically figure out how to solve it and then it'll patch the skill for you."

*Also film-able (not deep-pitched):* a "Chrome DevTools MCP for consumer automation" video (book a desk, comparison-shop, order groceries) would sit alongside the existing Claude-in-Chrome chapter as a different-tool flavor, but it is a 🟡 partial on tool angle, not a net-new gap.

*Spine 2 produces no pitch: it is ✅ covered by "Creating Skills" (skill-creator) and "Blog Post to Skill", which already teach authoring a skill from existing material more robustly than the hand-rolled spec-file trick.*

## 📚 Full wisdom (reference)

**SUMMARY**
Nick Saraev demonstrates five revenue-focused Claude skills plus personal automations, then teaches SOP-to-skill conversion, progressive disclosure, and self-annealing behavior aimed at real business outcomes, not shiny demos.

**IDEAS**
- Most skill demos chase flashy personal-assistant vibes while leaving real business revenue untouched on the table.
- One follow-up skill reads every past email thread and sends casual, personalized check-ins to prospects automatically.
- Follow-up replies stay inside the original email chain, matching prior tone so prospects think it's you.
- A one-shot thumbnail skill superimposes your real face onto a viral reference image across multiple variants.
- Generating several thumbnail variants at once lets you pick the best, since AI output is imperfect.
- A scraping skill queries LinkedIn Sales Navigator, builds search URLs, returns leads with emails in Sheets.
- LinkedIn Sales Navigator is the freshest B2B source; most other data providers scrape from it anyway.
- A cold-email skill duplicates high-performing campaigns, rewrites them for a client's offer, loads into the platform.
- Because models like Opus improved, he often ships duplicated campaigns unchanged, just to test their performance.
- A website-builder skill whips up templated but unique client sites, then pushes them live to Netlify.
- Free high-quality websites are knowledge arbitrage: you own tools cold prospects simply don't, blowing them away.
- He built a WeWork skill that auto-books a desk thirty days ahead using his stored credentials.
- An Amazon shopping skill opens the site, compares listings, and recommends best cost-effectiveness in a sheet.
- These personal skills use Chrome DevTools MCP to drive a real browser for everyday API-less tasks.
- Skills are the evolution of standard operating procedures, rewritten into the native format agents actually understand.
- Any existing SOP becomes a skill: feed it plus a skill-spec, ask the agent to convert.
- He compressed Anthropic's skills docs from five hundred lines to two hundred for a dense spec.
- After building, run the skill once end-to-end so the agent tests it and requests anything missing.
- Skills self-anneal: on any runtime failure the agent fixes it and rewrites its own skill file.
- Front matter loads roughly sixty tokens as a summary, deferring the full skill until it's triggered.
- Skill matching scans every front-matter description for the request, then loads only the most relevant skill.
- Progressive disclosure keeps context small, which both lowers cost and raises the model's output quality noticeably.
- Skills nest deeply inside the hidden dot-claude folder, then skills, then a named folder, then skill.md.
- Scripts and assets like PDFs or tokens live beside skill.md, optionally in a separate execution subfolder.
- Every major provider now supports skills: Anthropic originated them, OpenAI and Gemini CLI followed very closely.

**INSIGHTS**
- The winners focus skills on front-end revenue tasks; shiny back-end pipelines rarely translate into real money.
- A skill is just an SOP translated for agents, so anyone with checklists already owns skills.
- Self-annealing means skills behave like ambitious staff: they notice gaps and fill them without being asked.
- Progressive disclosure exists because smaller context both cuts provider cost and measurably improves model output quality.
- Agents can do anything, but that doesn't mean you should; capability without revenue focus wastes effort.
- Going straight to LinkedIn Sales Navigator beats resellers because you access the freshest source yourself directly.
- Automated follow-ups fail when language sounds robotic; casual human tone keeps most prospects from noticing automation.
- Browser automation skills unlock any app lacking an API, turning UI-only tasks into repeatable agent work.
- Because output cost is cents, giving prospects free deliverables like websites is unusually cheap, high-leverage outreach.
- Skills that merely build skills or invent frameworks are low value; the revenue-adjacent skills matter most.

**QUOTES**
- "I currently run a business that does over $4 million a year in profit." (Nick Saraev)
- "The whole key here is we do this really informally and then really casually so they think it's us." (Nick Saraev)
- "They're self- annealing over time. They heal themselves. They get better and they improve constantly." (Nick Saraev)
- "Skills are basically the evolution of standard operating procedures just for agents." (Nick Saraev)
- "If you guys have a standard operating procedure, if you have an SOP, you have a skill." (Nick Saraev)
- "You can do anything, but that doesn't mean that you should do everything." (Nick Saraev)
- "The less context in a model's context window at any mo point in time, the higher the quality of the output." (Nick Saraev)
- "Don't just have them sit around in your folder. Actually use them." (Nick Saraev)
- "Skills that you guys could actually implement in your business to do the work of dozens of people in just a few minutes." (Nick Saraev)

**HABITS**
- He triggers a follow-up nurture skill each morning to clear his entire pipeline before prospecting anew.
- He generates multiple AI variants of any deliverable, then picks the strongest rather than trusting one.
- He voice-transcribes his requirements using Whisper Flow instead of typing long prompts into Claude Code manually.
- He always runs a freshly built skill once end-to-end to test it before relying on it.
- He keeps his CLAUDE.md as short as humanly possible, especially when injecting the skill-spec creation instructions.
- He builds one-off skills for annoyances like desk booking rather than tolerating repetitive small manual chores.
- He runs several Claude Code instances in parallel to build multiple skills simultaneously and very quickly.
- He reviews what a skill flagged before acting, asking it to list items rather than execute.

**FACTS**
- Front matter can shrink a skill's context footprint from around five hundred tokens to roughly seventy.
- Anthropic originated skills, and OpenAI plus Google's Gemini CLI later shipped nearly identical skill formats afterward.
- Nick's business reportedly generates over four million dollars annually in profit, managed primarily through AI agents.
- Markdown files add formatting like headers, backticks, and links that plain text files cannot display properly.
- On macOS, pressing shift-command-period reveals hidden folders such as the dot-claude skills directory within Finder.
- Claude Code automatically enters plan mode whenever it judges a build to be even slightly complicated.
- The inbox demo found seventy-nine of ninety-seven unread emails came from one single broken Make scenario.
- LinkedIn Sales Navigator offers the highest deliverability lead data available from essentially any current source today.

**REFERENCES**
- Tools/platforms: Claude Code, OpenAI Codex, Gemini CLI, Antigravity, Chrome DevTools MCP, Whisper Flow, Netlify.
- Anthropic Claude Code docs "Extend Claude with skills"; the free skillspec.md (Google Drive download).
- Lead data: LinkedIn Sales Navigator, Apollo, Apify; Bright Data, Referral Stack (email senders); Make.com (broken scenario).
- Browser-automation targets: WeWork, Amazon (CA), Instacart grocery delivery.
- Models referenced: Opus 4.5 and 4.6, GPT 5.2 and 5.3, Gemini 3.1.
- Nick's ventures/content: Maker School, 1SecondCopy, and his Claude Code, Antigravity, Agentic Workflows, and N8N courses.
- The John Hamm / Don Draper "Mad Men" viral thumbnail reproduced in the demo.

**ONE-SENTENCE TAKEAWAY**
Convert your revenue-generating SOPs into self-healing agent skills, then actually use them every single day.

**RECOMMENDATIONS**
- Copy an existing business SOP, feed it with a skill-spec, and ask the agent to convert.
- Compress Anthropic's skills docs into a dense two-hundred-line spec you can inject through your own CLAUDE.md.
- Always run any new skill once end-to-end so it self-tests and requests any missing inputs upfront.
- Prompt your skill spec so skills self-heal, patching their own definition when a run actually fails.
- Focus your skill-building time squarely on front-end tasks: lead generation, sales, marketing, and content repurposing pipelines.
- Use Chrome DevTools MCP to automate any API-less app, like recurring bookings, shopping, and grocery delivery.
- Generate several variants of AI deliverables, then choose the best instead of trusting a single output.
- Offer cold prospects a free high-quality website as knowledge-arbitrage value to genuinely stand out during outreach.
- Keep follow-up automation casual and inside existing email threads so prospects never notice it's fully automated.
