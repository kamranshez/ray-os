# 01 — Newsletter Survey & Acquisition (PostHog)

**Source:** PostHog project "Agentic Coding School" (id 236619). Pulled 2026-06-26.
**Method note:** the confirm-page "Newsletter Survey" is **not** a PostHog Survey object — it's custom-coded in `apps/nextjs/src/pages/newsletter/confirm.tsx` and captured as `newsletter_survey_answer` events (one per question) with `question`, `question_id`, `answer`, `step` properties. Survey was **revised ~Jun 21 2026**: older version (Apr 17–Jun 21) asked "Are you using AI to code?" + "What harness do you prefer?"; current version (Jun 21+) asks experience-level + biggest-challenge. Role + learning-goals run across both.

## Q: "What best describes your current role?" — n = 203
| Answer | Count | Share |
|---|---|---|
| Developer/Engineer | 52 | 26% |
| Founder/CTO | 50 | 25% |
| Tech Lead/Senior Engineer | 42 | 21% |
| Other | 29 | 14% |
| Student/Career Changer | 24 | 12% |
| Engineering Manager | 6 | 3% |

Senior-and-above (Founder/CTO + Tech Lead/Senior + Eng Manager) = **48%**. Add Developer/Engineer → **74% working engineers/leaders**. Students/career-changers only 12%.

## Q: "Where are you at with agentic coding?" — current version only, n = 35
| Answer | Count | Share |
|---|---|---|
| I use it daily and want to go deeper | 14 | 40% |
| Just getting started | 13 | 37% |
| Advanced, building multi-agent systems | 8 | 23% |

**63% already daily/advanced; 37% beginners.** Small sample — directional.

## Q: "What's your biggest challenge right now?" — current version only, n = 32
| Answer | Count | Share |
|---|---|---|
| Going from prompting to automated loops | 12 | 38% |
| Keeping up with new tools and features | 11 | 34% |
| Keeping context tight and sessions productive | 6 | 19% |
| Orchestrating multiple agents and subagents | 2 | 6% |
| Token cost and efficiency | 1 | 3% |

Top pain is a **level-up problem**, not "teach me the basics." #2 is **currency** (keeping up).

## Q (older): "Are you using AI to code?" — n = 173
**Yes 163 (94%) / No 10 (6%).**

## Q (older): "What agent coding harness do you prefer?" — ~180 responses
Claude Code dominant: **82 picked Claude Code alone**; appears in most multi-select combos. Codex clear #2 (Codex alone = 10; "Claude Code + Codex" = 32). Cursor, OpenCode trail.

## Q: "What are you looking to learn and build with AI?" — free text, ~87 non-empty (~50% skip)
Thematic clusters:
- **Multi-agent / orchestration / "harness engineering"** (strongest): "multi-agent systems and agentic workflows," "a swarm of agents that work in parallel and in sequence," "agents and subagents," "executing agents in the cloud," "scaling via an agentic team."
- **Workflow automation & productivity:** "workflow automations; token optimization," "automate my business," "move away from prompting into running automated loops."
- **Building products/businesses solo:** "one-man unicorn," apps/websites/iOS apps, "scaling up a web app."
- **Staying current / best practices:** "latest techniques," "industry best practices, how to scale."
- **Tool mastery (still present):** "get the max out of CC and Codex," "be very affluent with Claude Code." A handful want fundamentals: "general principles of Agentic Coding besides the tool use."

## Acquisition channels (last 90 days, ~37.7k people)
Most arrive with **no UTM**; referrer is the better lens.
- **YouTube — #1 external** (~6.2k people; largest tagged source). Ray's @RAmjad channel is the engine.
- **Google search** second (~4.6k).
- **trustmrr.com** third (~3.3k) — review/directory referral.
- LinkedIn, Brave, Discord, Bing, DuckDuckGo long-tail.

**Conversion by channel** (noisy — Stripe/Google-auth redirects overwrite first-touch): **YouTube by far the largest converting channel (~145 buyers)**, Google search distant second (~30). Essentially a YouTube-led founder-creator funnel.

## Caveats
- No dedicated role/seniority property on persons/pageviews — role only exists inside the survey (self-selected newsletter-confirmers, not all visitors/buyers).
- Survey answers can't be cleanly linked to purchase outcomes — "which segment buys" remains open.
- Experience + challenge questions are small-n (~32–35, launched ~Jun 21) — re-pull in 2–3 weeks.
- Free-text learning_goals ~50% skip; manual thematic read, not counted distribution.
- UTMs mostly absent; conversion-by-channel directional.
- Key file for decoding survey data: `apps/nextjs/src/pages/newsletter/confirm.tsx`.
