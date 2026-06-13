---
duration: "14-18 min"
batch: 5
order: 18
batch_name: "L4 and L5 The Climb"
class: "loopy-ai"
chapter: "Auto Research For Non-Technical Work"
aliases: [auto-research-for-non-technical-work]
status: to-film
---

Most people hear "auto research" and immediately think it is a coding thing. An agent opens a codebase, changes a training script, runs a benchmark, keeps the change if the number went up. That version is easy to understand because code has an obvious feedback loop. Run the test. Check the number. Keep the improvement.

The more interesting version, for most people, is not code. It is YouTube titles. Cold email subject lines. Landing page headlines. Ad hooks. Offer positioning. Newsletter angles. Basically all the work where the AI can generate something that looks good, sounds good, and still completely fails in the real world.

That is the important distinction. For non-technical work, the bottleneck is not generating more ideas. We already have too many ideas. You can ask Claude for fifty YouTube titles, fifty ad angles, fifty cold email openers, and it will happily do that all day. The bottleneck is knowing what actually worked, and then remembering that result the next time.

That is what auto research gives you. Not just generation. A loop.

![[auto-research-generation-feedback-loop.png]]

## The core shift

The shift is this. You stop asking the agent to give you the best answer. You ask the agent to run the smallest useful experiment.

A normal AI workflow looks like:

> "Give me 20 better titles for this video."

The AI gives you twenty titles. You pick the one that sounds best. Maybe it works, maybe it does not. Either way, the learning usually disappears. It stays in your head, or in YouTube Analytics, or in a Slack message somewhere, but it does not become part of the next run.

The auto research workflow looks different. You say:

> "Here is my live feedback source. Here is the small surface area you are allowed to change. Here is the metric we are optimising for. Here are the constraints. Create an experiment, run it, evaluate it, store the result, and tell me what you learned."

The agent is no longer a copywriter. It is an experiment manager.

## The five pieces of the loop

### 1) A live feedback source

This is where the real-world data comes from. The agent has to be able to see reality, otherwise it is just guessing.

For YouTube, that is YouTube Analytics. Impressions, click-through rate, average view duration, watch time per impression, traffic source.

For cold email, it might be Smartlead, Instantly, HubSpot, or Airtable. Opens, replies, positive replies, booked calls, unsubscribes.

For landing pages, it might be Instapage, Webflow, or Google Analytics.

The specific tool does not matter. What matters is that the data is updating in real time and the agent can read it.

![[live-feedback-source-agent-data.png]]

### 2) An experiment table

This is the memory of the system. Could be Airtable, Supabase, Notion, a Google Sheet, Postgres. Tool does not matter.

What matters is that every experiment lives in one structured place. Each row is the full lifecycle of one test:

- Experiment ID
- Video or campaign ID
- Hypothesis
- Original version
- New variant
- Start date and end date
- Sample size
- Metric before
- Metric after
- Decision (keep, revert, inconclusive)
- Lesson learned
- Next recommended test

This table is not just a log. It is the centre of the system. The hypothesis, the change, the evaluation, the result, the lesson, and the next step all live in the same row. The agent reads it before proposing anything new, and writes back to it after every evaluation.

That is what makes the system compound. The agent is not starting from scratch each morning. It is reading what it tried last week and building on it.

![[experiment-table-system-memory-compounding.png]]

### 3) A small experiment surface

This is the thing the agent is actually allowed to change. And it should be narrow.

For YouTube, maybe the surface is only titles. Not thumbnails. Not descriptions. Not the first thirty seconds of the video. Not the pinned comment. Just titles.

For cold email, maybe it is only subject lines. Or only the first line. Or only the offer sentence.

If the agent changes five things at once, you do not have an experiment. You have a mess. You cannot tell what caused the result.

This also keeps the API surface small. The agent does not need access to your whole business. It needs three or four specific actions: read analytics for a video, update the title, revert the title. That is enough.

![[narrow-surface-clean-signal-api.png]]
### 4) Constraints and guardrails

This is what most people skip when they get excited about auto research. And it is the part that actually makes it safe to run.

You do not want the agent waking up at 3am and changing every title on your channel. That would be insane. If something improves, you do not know what caused it. If something gets worse, you do not know what to revert.

For YouTube, the constraints might look like:

- Only test on 10% of eligible videos at a time
- Do not touch videos published in the last seven days
- Do not touch top-performing videos
- Only test on videos with enough impressions to read a signal
- Only test on videos with below-average CTR
- Do not change thumbnails
- Revert the title if watch time per impression drops below baseline

For cold email:

- Only 10% of send volume goes to experiments
- The control campaign stays untouched
- Do not change pricing
- Do not make claims we cannot prove
- Do not target unapproved industries
- Stop the experiment if reply quality drops

The agent should not have a blank cheque. It should have a research budget. That budget might be 10% of cold email volume, or 10% of eligible YouTube videos, or one landing page variant. The budget is what makes learning affordable. Most failures should be small, cheap, and informative.

![[guardrails-budget-constraints-sandbox.png]]
### 5) An optimisation metric

This is the number the agent is trying to improve. And this is another place people get it wrong.

For YouTube, optimising only for CTR is dangerous. A title can get more clicks and bring in worse viewers. So the metric might be watch time per impression. Or CTR with an average view duration guardrail. Or browse CTR, but only if retention stays above baseline.

For cold email, optimising for open rate pushes you toward clickbait subject lines. The real metric is positive reply rate, booked call rate, or qualified reply rate.

The metric defines the behaviour. If you choose the wrong metric, the agent will get very good at the wrong thing.

![[metric-guides-agent-behavior-compass.png]]
---

## What the agent actually does each day

Once the five pieces are in place, the daily loop is simple.

Every morning, the agent wakes up and reads the experiment table. It looks for experiments that are currently running. For each one, it checks the live feedback source.

If the experiment has enough data, it evaluates it. If it won, it marks it as a winner and keeps the change. If it lost, it reverts the change. If it is inconclusive, it either waits longer or closes it as inconclusive.

Then it writes the lesson back into the same row. Something like:

> "Titles that promise a concrete workflow outperformed titles that explain a general concept. Continue testing workflow-based titles on older videos in the Claude Code category."

Or:

> "Curiosity-heavy titles increased CTR but reduced average view duration. Do not continue this pattern unless retention recovers."

Or:

> "Subject lines mentioning cost savings increased open rate but did not increase positive replies. Treat this as a weak signal, not a winning strategy."

Then the agent proposes the next experiment, reading the previous lessons first. So it is not starting cold. It is building on the previous loop.

That is the difference between AI-generated ideas and auto research. AI-generated ideas reset every time. Auto research accumulates.

## Running it on autopilot: the mission loop

Everything above describes the logic. The thing that actually runs it every day is a mission.

A mission is a long-running loop whose state lives in a file. You hand the agent a `MISSION.md`, and each run is one step. The agent reads the mission, forms a hypothesis, does the work, outputs its artifacts, then schedules the next step for some hours or days later. If it hits something only you can decide, it flags `needs_human` and waits instead of guessing.

![[mission.png]]

That is the whole shape. `MISSION.md` holds the objective and the running log. Each step reads it, acts, writes the result back, and queues the next run. `/artifacts` and `/steps` let you see what it produced and where it sits in the sequence. The experiment table from earlier is exactly what the mission reads and writes on every step. So the mission loop and the experiment loop are the same loop seen from two sides. The mission is the scheduler. The table is the memory.

## The daily Slack report

The human still needs to stay in the loop. So after the agent evaluates the experiments, it posts a daily report.

For YouTube:

> "Yesterday I evaluated six title experiments. Two were winners, one was reverted, three need more data. The strongest signal is that concrete workflow titles are outperforming abstract AI concept titles. I logged all results in Airtable. Today I am starting three new tests on older videos with high impressions and below-average CTR."

For cold email:

> "Yesterday the 10% auto research segment produced a 2.4% positive reply rate compared to 1.7% on the control. The winning variant used a shorter subject line and a more direct first sentence. Control stays untouched. Today I am testing two new variants inside the same 10% budget."

That is what you want. Not a giant report. Not a vague "things are improving." A clear summary: what changed, what happened, what we learned, what is happening next.

This is where the system starts to feel like an actual operator. Not because it is doing something magical. Because it is doing the boring thing every day. Checking the numbers. Updating the table. Applying the rule. Writing down the lesson. Running the next test.

That is most of optimisation. Humans are just inconsistent at it.

![[slack-experiment-results-summary-report.png]]

---

## The pattern, generalised

Once you see the pattern, you can apply it almost anywhere.

**For YouTube titles:**
- Feedback: YouTube Analytics
- Table: Airtable
- Surface: video titles only
- Metric: watch time per impression
- Constraint: 10% of eligible older videos
- Report: daily Slack summary

**For cold email:**
- Feedback: Smartlead or Instantly
- Table: Airtable
- Surface: subject lines or first lines
- Metric: positive reply rate
- Constraint: 10% of send volume
- Report: daily Slack summary

**For landing pages:**
- Feedback: Instapage or analytics
- Table: Airtable
- Surface: headline or CTA
- Metric: qualified conversion rate
- Constraint: one variant at a time
- Report: daily summary with keep or revert decision

**For newsletters:**
- Feedback: email platform
- Table: Airtable
- Surface: subject line
- Metric: click rate or reply rate, not just opens
- Constraint: small segment test before full send
- Report: winning pattern and next test

The shape stays the same. Live feedback. Experiment table. Small surface. Constraints. Metric. Daily report. Everything else is implementation detail.

## The key insight

Auto research is not about giving AI more freedom. It is about giving AI a tighter loop.

That is the opposite of how people usually think about agents. They think the more powerful agent is the one that can do everything. But in practice, the useful agent is often the one that can do one narrow thing repeatedly, measure it properly, and remember what happened.

That is what makes it compound. One experiment does not matter. Ten experiments are interesting. A hundred experiments, all logged, evaluated, and turned into future context, starts to become a real advantage. Because now your AI workflow has something most AI workflows do not have: a memory of reality. Not just prompts. Not just examples. Not just brand voice. Actual outcomes. What worked. What failed. What was inconclusive. What should be tried next.

For non-technical work, that might be the highest-leverage version of auto research. Not "AI runs my marketing." It is AI running controlled experiments against live feedback, storing the results, and getting a little less wrong every day.

![[tight-loops-memory-competitive-advantage.png]]

---
## Connection to existing content

- **Closing the Loop** (filmed) covers the autopilot pattern in plain terms. This video is the operator-grade version: same idea, but with a structured experiment table and a real test budget.
- **Auto Research (Karpathy Loop)** (to-film, loopy-ai class) introduces the concept on the technical side. This is the non-technical companion video.
- The `/autoresearch` skill in the skills library can be pointed at any of these surfaces once the experiment table exists.
