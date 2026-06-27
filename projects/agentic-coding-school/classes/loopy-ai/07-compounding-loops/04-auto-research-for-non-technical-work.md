---
video_id: "rQftC87y"
duration: "14-18 min"
batch: 5
order: 18
batch_name: "Compounding Loops"
class: "loopy-ai"
chapter: "Auto Research For Non-Technical Work"
aliases: [auto-research-for-non-technical-work]
status: "filmed"
---
Most people hear "auto research" and immediately think it is a coding thing. An agent opens a codebase, changes a training script, runs a benchmark, keeps the change if the number went up. That version is easy to understand because code has an obvious feedback loop. Run the test. Check the number. Keep the improvement.

The more interesting version, for most people, is not code. It is YouTube titles. Cold email subject lines. Landing page headlines. Ad hooks. Offer positioning. Newsletter angles. Basically all the work where the AI can generate something that looks good, sounds good, and still completely fails in the real world.

That is the important distinction. For non-technical work, the bottleneck is not generating more ideas. We already have too many ideas. You can ask Claude for fifty YouTube titles, fifty ad angles, fifty cold email openers, and it will happily do that all day. The bottleneck is knowing what actually worked, and then remembering that result the next time.

That is what auto research gives you. Not just generation. A loop.

![[auto-research-generation-feedback-loop.png]]

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "Auto Research: From Generation to Feedback". LEFT half labeled "AI Idea Generation (No Feedback Loop)": a confused robot clutching its head, surrounded by a chaotic pile of sticky-note ideas (YouTube title, cold email subject, landing page headline, offer positioning, newsletter angle) with floating question marks and red X's; sub-caption "Chaotic Pile of Unverified Ideas (Bottleneck: Knowing What Works)". A green "Auto Research Advantage" arrow points right. RIGHT half labeled "Auto Research (Closed Feedback Loop)": a happy robot at the center of a four-stage clockwise cycle GENERATE → SHIP → MEASURE → LEARN drawn as rounded boxes with icons; sub-caption "Tightly Closed Feedback Loop (Bottleneck: Iteration & Learning)". Colored-pencil shading throughout.]
![[auto-research-generation-feedback-loop-1.png]]
![[auto-research-generation-feedback-loop-2.png]]
![[auto-research-generation-feedback-loop-3.png]]
![[auto-research-generation-feedback-loop-4.png]]
![[auto-research-generation-feedback-loop-5.png]]

## The core shift

The shift is this. You stop asking the agent to give you the best answer. You ask the agent to run the smallest useful experiment.

A normal AI workflow looks like:

> "Give me 20 better titles for this video."

The AI gives you twenty titles. You pick the one that sounds best. Maybe it works, maybe it does not. Either way, the learning usually disappears. It stays in your head, or in YouTube Analytics, or in a Slack message somewhere, but it does not become part of the next run.

The auto research workflow looks different. You say:

> "Here is my live feedback source. Here is the small surface area you are allowed to change. Here is the metric we are optimising for. Here are the constraints. Create an experiment, run it, evaluate it, store the result, and tell me what you learned."

The agent is no longer a copywriter. It is an experiment manager.

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "The Core Shift: Copywriter to Experiment Manager". LEFT panel with a faded grey label "Copywriter (Old Way)": a robot handed a sticky note "Give me 20 better titles" dumping a messy pile of unused title options into a bin, thought bubble "Pick the best-sounding one and hope", caption "Learning disappears." RIGHT panel marked with a green check "Experiment Manager (Auto Research)": a confident robot at a desk reading a structured brief card listing "Live feedback source / Allowed surface / Target metric / Constraints", running one labeled experiment along a small track CREATE → RUN → EVALUATE → STORE → REPORT, caption "Runs the smallest useful experiment." Handwritten bottom caption "Stop asking for the best answer. Ask for the smallest useful experiment." Colored-pencil shading.]

## The five pieces of the loop

### 1) A live feedback source

This is where the real-world data comes from. The agent has to be able to see reality, otherwise it is just guessing.

For YouTube, that is YouTube Analytics. Impressions, click-through rate, average view duration, watch time per impression, traffic source.

For cold email, it might be Smartlead, Instantly, HubSpot, or Airtable. Opens, replies, positive replies, booked calls, unsubscribes.

For landing pages, it might be Instapage, Webflow, or Google Analytics.

The specific tool does not matter. What matters is that the data is updating in real time and the agent can read it.

![[live-feedback-source-agent-data.png]]

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot standing in the center, bold handwritten title "A live feedback source: Real-time data for the agent". Three colored pipe/conduit shapes feed data arrows into the robot: top-left red pipe "YouTube Analytics" (CTR 4.5%, Avg View 3:12, Views 1.2K), bottom-left blue pipe "Smartlead / Instantly" (Opens 35%, Replies 8%, Booked 2), right green pipe "Instapage / Google Analytics" (Conversion 12%, Bounce Rate 40%, Visitors 500). A thought bubble over the robot reads "SEE REALITY (Live Data)". Label under the robot "AI AGENT". Handwritten caption at the bottom "Agent can read live data, not just guess." Colored-pencil shading.]
![[live-feedback-source-agent-data-1.png]]
![[live-feedback-source-agent-data-2.png]]
![[live-feedback-source-agent-data-3.png]]
![[live-feedback-source-agent-data-4.png]]
![[live-feedback-source-agent-data-5.png]]

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

[IMAGE: hand-drawn whiteboard sketch on white, bold handwritten title "The Experiment Table: System Memory & Compounding Learning". A large central spreadsheet table with columns Hypothesis | Variant | Metric Before | Metric After | Decision | Lesson | Next Test, one row highlighted with a glowing blue outline (e.g. "Changing CTA color to orange will increase CTR" / "CTA Button #FF4500" / "2.1% CTR" / "3.8% CTR" / "Keep" / "Orange is more prominent than blue" / "Test orange against red CTA"). LEFT: a blue robot holding a magnifying glass labeled "Agent (Reading from History)" with a thought bubble "Reading past experiments to inform new proposals. Not starting from scratch." RIGHT: a blue robot holding a pen labeled "Agent (Writing Back Results)" with a speech bubble "Recording new findings, lessons, and next steps. The loop compounds." A bottom flow Proposal → Experiment → Evaluation → Write Back & Compound. Handwritten caption "The experiment table is the central memory. Every hypothesis, result, and lesson is stored in one structured place." Colored-pencil shading.]
![[experiment-table-system-memory-compounding-1.png]]
![[experiment-table-system-memory-compounding-2.png]]
![[experiment-table-system-memory-compounding-3.png]]
![[experiment-table-system-memory-compounding-4.png]]
![[experiment-table-system-memory-compounding-5.png]]

### 3) A small experiment surface

This is the thing the agent is actually allowed to change. And it should be narrow.

For YouTube, maybe the surface is only titles. Not thumbnails. Not descriptions. Not the first thirty seconds of the video. Not the pinned comment. Just titles.

For cold email, maybe it is only subject lines. Or only the first line. Or only the offer sentence.

If the agent changes five things at once, you do not have an experiment. You have a mess. You cannot tell what caused the result.

This also keeps the API surface small. The agent does not need access to your whole business. It needs three or four specific actions: read analytics for a video, update the title, revert the title. That is enough.

![[narrow-surface-clean-signal-api.png]]

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "3) A small experiment surface (Narrow vs. Wide)" with subtitle "Narrow surface = clean signal. Keep the API small." LEFT panel marked with a red X, "Wide Surface = Messy Signal": a confused robot facing a YouTube panel with many unlocked editable fields (Thumbnail, Title, Description, First 30 Seconds, Pinned Comment), tangled "Change this? And this? Also this?" arrows, thought bubble "Too many variables = No clear cause. A messy experiment." RIGHT panel marked with a green check, "Narrow Surface = Clean Signal": a confident robot pointing at a YouTube panel where only "Title (Text)" is unlocked and highlighted blue while the other fields show grey LOCKED padlocks, label "Only change this! (Controlled Variable)", thought bubble "One variable = Clear causality. A clean A/B test." Bottom caption "The agent only needs specific actions: read analytics, update title, revert title. That is enough." Colored-pencil shading.]
![[narrow-surface-clean-signal-api-1.png]]
![[narrow-surface-clean-signal-api-2.png]]
![[narrow-surface-clean-signal-api-3.png]]
![[narrow-surface-clean-signal-api-4.png]]
![[narrow-surface-clean-signal-api-5.png]]
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

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "4) Constraints and Guardrails: Making Auto Research Safe". LEFT: a robot pointing at a large soft-blue "90% Production Area (Untouched)" zone with a big blue checkmark and label "Stable, Safe, No Changes", and a "STOP" arrow. RIGHT: a fenced-off sandbox ringed with barbed wire labeled "10% Research Budget (Experimentation)", a small robot inside holding a magnifying glass over glowing green and red experiment dots. Two posted signboards above the fence: "YouTube Constraints" (Only test on 10%, Do not touch top videos, Only test low CTR, Do not change thumbnails, Revert if watch time drops) and "Cold Email Constraints" (Only 10% send volume, Do not touch control, Do not change pricing, Stop if reply quality drops). Handwritten callouts "Guardrails prevent the agent from acting on the production area. Failures here are small, cheap, and informative." and "Agent has a research BUDGET, not a blank cheque." Colored-pencil shading.]
![[guardrails-budget-constraints-sandbox-1.png]]
![[guardrails-budget-constraints-sandbox-2.png]]
![[guardrails-budget-constraints-sandbox-3.png]]
![[guardrails-budget-constraints-sandbox-4.png]]
![[guardrails-budget-constraints-sandbox-5.png]]
### 5) An optimisation metric

This is the number the agent is trying to improve. And this is another place people get it wrong.

For YouTube, optimising only for CTR is dangerous. A title can get more clicks and bring in worse viewers. So the metric might be watch time per impression. Or CTR with an average view duration guardrail. Or browse CTR, but only if retention stays above baseline.

For cold email, optimising for open rate pushes you toward clickbait subject lines. The real metric is positive reply rate, booked call rate, or qualified reply rate.

The metric defines the behaviour. If you choose the wrong metric, the agent will get very good at the wrong thing.

![[metric-guides-agent-behavior-compass.png]]

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "The Metric Defines the Behaviour: Choose Wisely". LEFT column "Vanity Metric (e.g., CTR / Open Rate)": a strained robot trudging up a grey "Wrong Hill" with a "CTR ↑" chart on its chest and a speech bubble "Just get clicks! More! More!", leading down to a trash pile of "Clickbait Subject Lines", "Worse Viewers", "Negative Feedback" with a red X and caption "Agent gets very good at the WRONG thing. Dangerous." A "vs." arrow in the middle. RIGHT column "Real Metric (e.g., Watch Time / Qualified Reply Rate)": a smiling robot striding up a green "Right Hill" with a "Watch Time ↑" chart and speech bubble "Focus on quality & engagement!", leading to a treasure chest with "Positive Replies", "Booked Calls", "Better Engagement", a green check and caption "Agent gets good at the RIGHT thing. Meaningful Success." A compass labeled "METRIC" sits at the bottom center with caption "The metric is the compass. It guides the agent's journey." Colored-pencil shading.]
![[metric-guides-agent-behavior-compass-1.png]]
![[metric-guides-agent-behavior-compass-2.png]]
![[metric-guides-agent-behavior-compass-3.png]]
![[metric-guides-agent-behavior-compass-4.png]]
![[metric-guides-agent-behavior-compass-5.png]]
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

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot, bold handwritten title "AI Ideas Reset. Auto Research Accumulates." Split into two columns by a dashed vertical line. LEFT column marked with a red X, "AI-Generated Ideas (Resets Every Time)": a robot at the bottom of a loop that snaps back to zero each run, day 1 / day 2 / day 3 each starting from the same flat baseline, a thought bubble "Starting cold again...", small caption "No memory between runs." RIGHT column marked with a green check, "Auto Research (Accumulates)": a happy robot climbing an ascending staircase of stacked experiment cards (each step labeled with a past lesson like "orange CTA won", "workflow titles won", "shorter subject lines won"), an arrow "reads previous lessons first" looping from the stack into the robot before it proposes the next step, small caption "Each loop builds on the last." Handwritten bottom caption "It is not starting cold. It is building on the previous loop." Colored-pencil shading.]
![[auto-research-accumulates-vs-resets-1.png]]
![[auto-research-accumulates-vs-resets-2.png]]
![[auto-research-accumulates-vs-resets-3.png]]
![[auto-research-accumulates-vs-resets-4.png]]
![[auto-research-accumulates-vs-resets-5.png]]

## Running it on autopilot: the mission loop

Everything above describes the logic. The thing that actually runs it every day is a mission.

A mission is a long-running loop whose state lives in a file. You hand the agent a `MISSION.md`, and each run is one step. The agent reads the mission, forms a hypothesis, does the work, outputs its artifacts, then schedules the next step for some hours or days later. If it hits something only you can decide, it flags `needs_human` and waits instead of guessing.

![[mission.png]]

[IMAGE: minimal diagram on a solid black background, thin white lines and white text, no robot mascot, no shading. Bold white title "/mission" at the top. A clockwise loop of white-outlined nodes: "MISSION.md" → down to "agent run step #N" (grey subtitle "Form hypothesis, output artifacts") → down to "Schedule next step" (grey subtitle "in x hr/days/weeks") → a long arrow looping back up to "MISSION.md". A branch from "agent run step #N" points right to "needs_human", whose arrow loops back up into "MISSION.md". To the right, a white command list "/mission /artifacts /steps". Clean, sparse, slide-style.]
![[mission-1.png]]
![[mission-2.png]]
![[mission-3.png]]
![[mission-4.png]]
![[mission-5.png]]

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

[IMAGE: hand-drawn whiteboard sketch on white, a single Slack-style message card with a soft blue sketched border. Top row: a small blue robot avatar, bold name "Experiment Agent", greyed timestamp "Yesterday at 9:00 AM". Handwritten message body: "Evaluated 6 experiments: 2 winners (green check), 1 reverted (red X), 3 need more data (blue ??). Today: starting 3 new tests." Below the text, three hand-drawn pill badges: a green check "2", a red X "1", a blue "?" "3". Clean, minimal, no other scene elements. Colored-pencil shading on the icons.]
![[slack-experiment-results-summary-report-1.png]]
![[slack-experiment-results-summary-report-2.png]]
![[slack-experiment-results-summary-report-3.png]]
![[slack-experiment-results-summary-report-4.png]]
![[slack-experiment-results-summary-report-5.png]]

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

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot holding up a stencil, bold handwritten title "The Pattern, Generalised: One Shape, Many Surfaces". CENTER: a master template card with six labeled empty slots stacked vertically: "Live feedback / Experiment table / Small surface / Metric / Constraint / Daily report". FOUR columns fanning out to the right, each a filled copy of the same six-slot card with its own values: "YouTube titles" (YouTube Analytics / Airtable / titles only / watch time per impression / 10% eligible videos / daily Slack), "Cold email" (Smartlead / Airtable / subject lines / positive reply rate / 10% send volume / daily Slack), "Landing pages" (analytics / Airtable / headline or CTA / qualified conversion / one variant / keep-or-revert), "Newsletters" (email platform / Airtable / subject line / click or reply rate / small segment / next test). The six slot labels stay identical across all four; only the values change. Handwritten bottom caption "Same six slots every time. Everything else is implementation detail." Colored-pencil shading.]

## The key insight

Auto research is not about giving AI more freedom. It is about giving AI a tighter loop.

That is the opposite of how people usually think about agents. They think the more powerful agent is the one that can do everything. But in practice, the useful agent is often the one that can do one narrow thing repeatedly, measure it properly, and remember what happened.

That is what makes it compound. One experiment does not matter. Ten experiments are interesting. A hundred experiments, all logged, evaluated, and turned into future context, starts to become a real advantage. Because now your AI workflow has something most AI workflows do not have: a memory of reality. Not just prompts. Not just examples. Not just brand voice. Actual outcomes. What worked. What failed. What was inconclusive. What should be tried next.

For non-technical work, that might be the highest-leverage version of auto research. Not "AI runs my marketing." It is AI running controlled experiments against live feedback, storing the results, and getting a little less wrong every day.

![[tight-loops-memory-competitive-advantage.png]]

[IMAGE: hand-drawn whiteboard sketch on white, friendly blue cartoon robot mascot shown three times left to right in a progression, bold handwritten title "Auto Research: Tighter Loops, Not More Freedom" with subtitle "Building a Memory of Reality for Competitive Advantage". FIRST robot, confused with a "?" and a single dot, label "1 Experiment (Single Dot)" and "One experiment does not matter." An arrow "No Memory, No Real Advantage" to the SECOND robot with a lightbulb and a thought bubble "Interesting... Some Context.", a few scattered dots, label "10 Experiments (Slight Slope)" and "Ten experiments are interesting." An arrow "Building Context" to the THIRD happy robot pointing up at a steep rising curve made of many blue dots climbing toward "MEMORY OF REALITY / REAL ADVANTAGE", label "100 Experiments (Steep Upward Curve)" with note "Competitive Moat: Actual Outcomes, What Worked, What Failed. Not just prompts, examples, or brand voice." A large curved "TIGHTER LOOP" arc spans the top. Boxed handwritten caption at the bottom "Key Insight: Auto research isn't about more freedom. It's about repeatedly doing one narrow thing, measuring it, and remembering what happened to get a little less wrong every day." Colored-pencil shading.]
![[tight-loops-memory-competitive-advantage-1.png]]
![[tight-loops-memory-competitive-advantage-2.png]]
![[tight-loops-memory-competitive-advantage-3.png]]
![[tight-loops-memory-competitive-advantage-4.png]]
![[tight-loops-memory-competitive-advantage-5.png]]