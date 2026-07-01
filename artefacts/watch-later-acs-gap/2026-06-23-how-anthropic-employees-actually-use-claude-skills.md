---
title: How Anthropic Employees ACTUALLY Use Claude Skills
video_url: https://www.youtube.com/watch?v=3UWxMPUko1k
video_id: 3UWxMPUko1k
channel: Austin Marchese
published: 2026-06-23
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**How Anthropic Employees ACTUALLY Use Claude Skills**](https://www.youtube.com/watch?v=3UWxMPUko1k) - Austin Marchese - uploaded 2026-06-23

> Net-new ACS video available (gotchas as a living moat), plus two next-step complements.

## The one idea worth a video

- **Spine 1: A skill's gotcha section, a running log of failures Claude actually hit, is its highest-signal content and its real moat.** It subsumes the "skills are living documents that compound" and "don't get it right on day one" beats. VERDICT: net-new video available.
- **Spine 2: The highest-leverage skill move is verifying for QUALITY, not just correctness, often by bolting a named reviewer's encoded taste onto your everyday skills.** It reframes "verification had the most measurable impact" plus the manager-clone and internal-focus-group demos. VERDICT: next-step (complement) video available.
- **Spine 3: A good skill partitions deterministic work into scripts and leaves only non-deterministic work to the model.** It explains the scripts, tokens, and repeatability beats of the "power components" lesson. VERDICT: next-step (complement) video available.

## Summary + counts

Austin Marchese analyzes Anthropic's published interviews, blogs, and docs, distilling how their engineers, marketers, and legal teams use Claude skills into five practical, implementable lessons.

🔴 1 net-new · 🔗 2 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1: Gotchas are a living moat.**
The claim: a skill's gotcha section, a running log of failures Claude actually hit, is its single highest-signal content and the part a competitor cannot copy. Why it is non-obvious: people either treat gotchas as an afterthought or try to front-load every conceivable warning on day one. Why it is true: you cannot predict which edge cases a model will hit, so a gotcha written before you have seen the failure is a guess that adds noise, whereas a gotcha written after a real failure encodes information the model demonstrably needed. Therefore each lived failure permanently removes a future failure, and because only lived failures qualify, the section becomes a forcing function to actually run and stress the skill. Over months the log compounds into knowledge someone copying your markdown cannot reproduce, because they lack your failure history. It generalizes cleanly to ops runbooks and to test suites, where a regression test is just a gotcha you only write after the bug bit. How it goes wrong: speculative front-loaded gotchas bloat the file and confuse the agent, and gotchas that describe symptoms rather than triggers do not actually prevent the next miss.

**Spine 2: Verify for quality, not just correctness.**
The claim: the highest-leverage thing you can do with skills is verification, and specifically a SUBJECTIVE quality gate (often a named reviewer's encoded taste) bolted onto skills you already run, not just an objective correctness check. Why it is non-obvious: most people treat AI as a multiplier (more output at the same quality) and build verifiers only for correctness, tests passing or the app running. Why it is true: on knowledge work, quality is the actual bottleneck and quality is a subjective bar, so if you encode a specific person's taste (from their public writing and internal Slack) into a reviewer that fires automatically, every output clears that bar once before any human sees it, which raises throughput and standard at the same time, the amplifier framing Austin draws. Because you retrofit the verifier onto an existing skill (so /brandVoice returns pass or fail), the check rides along on work you already do. It generalizes to a founder's board of advisers (Austin's internal focus group) and to design or hiring rubrics. How it goes wrong: a taste clone is only as good as the taste signal you fed it, and a subjective grade with no objective anchor can drift sycophantic.

**Spine 3: Partition deterministic work into scripts.**
The claim: the core design heuristic for a good skill is to push deterministic work into scripts and leave only non-deterministic work to the model. Why it is non-obvious: people write skills as pure markdown and let the model redo the same repeatable steps on every run. Why it is true: a deterministic step (same input, same output, like 2 plus 2) is wasted on an LLM because it burns tokens, varies slightly run to run, and steals the model's limited turns from the actual judgment. Move that step into a script and the model spends its turns on composition, deciding what to do next, instead of reconstructing boilerplate, so the output gets both cheaper and more repeatable. The skill folder then becomes code for the parts that should never vary plus AI for the parts that must adapt. It generalizes to any pipeline, for example an ETL where extraction and loading are scripted and only the classification step is model-driven. How it goes wrong: over-scripting a genuinely variable step makes the skill brittle, and the deterministic-versus-non-deterministic boundary is itself a judgment call you can draw in the wrong place.

## 🎬 Proposed ACS videos

**1. Gotchas: The Living Moat Inside Every Great Skill**
- HOOK: The most valuable part of your skill is the one section you have not written yet.
- THE PROMISE: For anyone maintaining Claude skills, leave able to grow a gotcha log that compounds into a real moat.
- THE SHAPE: (1) show a skill that keeps failing the same way; (2) add ONE real gotcha only after watching it fail; (3) contrast a speculative front-loaded list that bloats and confuses the agent; (4) show the month-one versus month-three growth curve; (5) the Obsidian approve-or-deny gotcha-audit workflow so only real gotchas land.
- SPINE: 1
- SLOT: Master Claude Code > Skills (alt: Advanced Techniques > Skills as Force Multipliers)
- RELATIONSHIP: ❌ net-new. ACS covers authoring ("Creating Skills"), triggering ("Triggering Skills Reliably"), and evolving loops ("Improving the Loop"), but has no video on the gotcha section as a growing failure log and moat.
- PROOF TO REUSE: "The highest signal content in any skill is the gotcha section"; "Most of our best skills began with a few lines and a single gotcha"; "the gotchas as your personal moat"; the only-add-what-you-actually-saw discipline; the month 1/2/3 growth graphic.

**2. Verify for Quality, Not Just Correctness: Bolt a Taste Reviewer Onto Your Skills**
- HOOK: Your tests prove the app runs. Nothing proves the output is any good.
- THE PROMISE: For builders using skills daily, retrofit a subjective quality gate that pre-clears your work before a human ever sees it.
- THE SHAPE: (1) correctness verification versus quality verification; (2) the amplifier-versus-multiplier reframe; (3) retrofit a pass-or-fail quality component onto an existing skill (/brandVoice); (4) encode a named reviewer's taste from their public writing and Slack; (5) the weekly manager-clone reviewer as the climax demo.
- SPINE: 2
- SLOT: Loopy AI > L2: Builder & Verifier (alt: Prompt Engineering > Personas and Archetypes)
- RELATIONSHIP: 🔗 complements "Scaling Taste" and "Builder Verifier Pattern". "Scaling Taste" already teaches encoding YOUR OWN judgment into an identity seed, skill, or simulator subagent; "Builder Verifier Pattern" and "Real Verifiers Touch Reality" teach OBJECTIVE builder-verifier loops (deterministic and scored signals). This adds the next step: a SUBJECTIVE quality gate that encodes a specific NAMED reviewer's taste and rides along inside your everyday skills as pass or fail.
- PROOF TO REUSE: Amul Aasar's weekly manager-clone reviewer story; "by the time he shows the manager anything it's already passed her AI clones quality bar"; the amplifier-not-multiplier framing; /verify and /run as built-ins; Austin's internal focus group and BuildPartner /expert advice.

**3. Scripts vs Prompts: Which Half of Your Skill Should Be Code**
- HOOK: Every deterministic step you leave to the model is tokens burned and repeatability lost.
- THE PROMISE: For skill authors, learn the partition rule that makes a skill cheaper to run and consistent every time.
- THE SHAPE: (1) define deterministic versus non-deterministic work; (2) show a prose-only skill redoing boilerplate on every run; (3) extract the repeatable part into a script; (4) show the token drop and the consistency gain; (5) the composition-not-boilerplate principle as the takeaway.
- SPINE: 3
- SLOT: Master Claude Code > Skills
- RELATIONSHIP: 🔗 complements "Creating Skills", which shows HOW to author a skill and feed it existing scripts. This adds the DESIGN heuristic of WHICH parts to script (the deterministic ones) versus leave to the model (the non-deterministic ones), and why that cuts tokens and raises repeatability.
- PROOF TO REUSE: "one of the most powerful tools you can give Claude is code"; the "spend its turns on composition ... rather than reconstructing boilerplate" quote; the 2-plus-2 deterministic example; "the more you push into scripts, the more repeatable your output ... the fewer tokens you'll burn".

## 📚 Full wisdom (reference)

**SUMMARY**
Austin Marchese analyzes Anthropic's published interviews, blogs, and docs, distilling how their engineers, marketers, and legal teams use Claude skills into five practical, implementable lessons.

**IDEAS**
- Anthropic buckets its nine technical skill categories into four types: utility, verification, data enrichment, and orchestration.
- A utility skill does one small reusable task, and it often layers beneath larger orchestration skills.
- Verification skills check final output and, per Anthropic, had the most measurable impact on Claude's quality.
- Data enrichment skills pull external data, like website traffic or competitor reports, into your working system.
- Orchestration skills chain other skills together, running enrichment, drafting, and verification as one single combined command.
- The best skills fit cleanly into one category; skills straddling several categories confuse the coding agent.
- Skills are not just markdown; they are folders holding scripts, assets, and data Claude can manipulate.
- Scripts let Claude spend its turns on composition and decisions instead of reconstructing repetitive boilerplate code.
- Scripts partition deterministic work from non-deterministic work: code handles repeatable steps, AI handles the variable parts.
- Pushing more into scripts makes output more repeatable and burns fewer tokens on every single run.
- Assets and templates live in a skill folder so outputs match a fixed format every time.
- Updating a template automatically updates every future output the skill produces from that same starting point.
- A config.json lets a skill ask for missing values once, then store them for later runs.
- Inside a skill you can invoke the ask-user-question tool to force structured multiple-choice input from you.
- The description field is a trigger condition, not a summary of what the skill actually does.
- Orchestration skills reference other skills by name, and the model invokes them if they are installed.

**INSIGHTS**
- Categorizing skills by function prevents overloaded skills that straddle jobs and quietly degrade the agent's reliability.
- Verification is leverage: encoding a clear pass-or-fail bar raises the quality of every downstream output produced.
- Treat AI as an amplifier raising quality, not merely a multiplier producing more at constant quality.
- Correctness verification checks facts and function; quality verification checks whether output meets your subjective quality bar.
- Encoding a reviewer's judgment as a skill gates work before any real human actually sees it.
- Gotchas are the highest-signal skill content: a growing log of real failures Claude has actually encountered.
- Skills are living documents that compound as edge cases surface across months of repeated real use.
- The description doubles as routing logic, so writing natural trigger phrases determines whether skills fire automatically.

**QUOTES**
- "one of the most powerful tools you can give Claude is code." (Anthropic, via Austin Marchese)
- "Giving Claude scripts and libraries lets Claude spend its turns on composition, deciding what to do next, rather than reconstructing boilerplate." (Anthropic, via Austin Marchese)
- "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." (Austin Marchese, citing a famous saying)
- "anyone can write a skill that Claude understands. The best people write skills that humans understand, too." (Austin Marchese)
- "Verification skills have had the most measurable impact on Claude's output quality internally." (Anthropic blog, via Austin Marchese)
- "It can be worth having an engineer spend a week just making your verification skills excellent." (Anthropic, via Austin Marchese)
- "by the time he shows the manager anything it's already passed her AI clones quality bar." (Austin Marchese, on Amul Aasar)
- "The highest signal content in any skill is the gotcha section." (Anthropic blog, via Austin Marchese)
- "Most of our best skills began with a few lines and a single gotcha." (Anthropic, via Austin Marchese)
- "Think of the skill as the structure, a verifier as the leverage, and the gotchas as your personal moat." (Austin Marchese)
- "The description field is not a summary. It's a description of when to trigger this skill." (Austin Marchese)
- "what feedback do you have for me as army and like I get that every week." (Amul Aasar, interview clip)

**HABITS**
- Austin runs a funnel digest skill that reviews all his websites and analyzes their incoming traffic.
- He keeps an internal focus group skill running a board of advisers for ongoing founder feedback.
- Amul Aasar runs a weekly skill simulating his manager's feedback from her public and internal writing.
- Austin formats gotcha-audit output as an Obsidian markdown file he clicks through to approve each individually.
- He always builds skills for his future self, thinking one, two, or three years ahead deliberately.
- He only adds a gotcha after actually watching Claude fail, never preemptively guessing future edge cases.
- He prefers retrofitting verification onto existing skills rather than building standalone verifier skills entirely from scratch.
- He derives orchestration skills from smaller reusable utility skills instead of building complex workflows from scratch.

**FACTS**
- Anthropic organized its internal skills into nine technical categories shown on screen during the whole video.
- Claude Code ships two built-in verification skills: /verify runs the app, /run launches it visually too.
- Amul Aasar is Anthropic's head of growth and appeared as a guest on a podcast previously.
- Austin's BuildPartner.ai product has over a thousand users and offers an /expert advice feedback command today.
- The channel recently reached fifty thousand subscribers after Austin spent over six years making videos online.
- The front-end design skill's description tells Claude to fire when users ask to build web interfaces.

**REFERENCES**
- Anthropic's published blog posts, interviews, and official docs on Claude skills
- Claude Code built-in skills: /verify and /run
- Amul Aasar (Anthropic head of growth) and his manager Army Vora (product writer)
- Anthropic's front-end design skill (used as the description/trigger example)
- Austin's own skills: funnel digest, internal focus group
- BuildPartner.ai and its /expert advice command
- Skill components: config.json, the ask-user-question tool, the arguments field
- Matthew Hinman (giveaway winner, building a Monday morning report generator)
- The famous programming saying: "Any fool can write code that a computer can understand ..."

**ONE-SENTENCE TAKEAWAY**
Design skills as single-purpose, script-backed, self-verifying folders whose gotchas and triggers compound with real use.

**RECOMMENDATIONS**
- Audit your existing skills and rebucket each into one clean type: utility, verification, enrichment, or orchestration.
- Move deterministic steps into scripts and reserve the model only for genuinely non-deterministic creative work today.
- Store an output template in the assets folder so every generated report matches your desired format.
- Add config.json, ask-user-question calls, and an arguments field so future-you can actually operate the skill later.
- Build a quality verifier that returns pass, fail, or a numeric grade on your final output.
- Encode a specific reviewer's taste from their writing so it grades your work before any submission.
- Keep a gotcha log and add entries only after you personally watch Claude fail somewhere real.
- Write descriptions as trigger conditions using the exact phrases you would naturally type when invoking them.
