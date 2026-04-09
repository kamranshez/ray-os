---
source: https://x.com/trq212/status/anthropic-skills-playbook
date: 2026-03-18
status: uploaded
youtube-id: 7PnF8qctDi8
youtube-title: "Anthropic Just Dropped Their Internal Skills Strategy"
published: 2026-03-19
duration: "18:43"
views: 12374
likes: 390
comments: 12
fetched: 2026-04-09
---
So the Anthropic team just published the highest signal article you'll see this week about how to effectively to Claude Code Skills. By the very people who made them.

And that's what we'll be going over today.

So if you're anything like me and you learn better from videos, this is for you.

--- 
## Don't state the obvious

Claude already knows a lot about coding and default ways of doing things. 

If your skill is just restating things Claude knows, you're wasting context and adding noise.

For example, if you make a skill trying to teach Claude Code how to use `ffmpeg` then that's a waste because it already knows how to do that from the millions of examples it's seen.

You wanna focus on what pushes Claude **out of its normal way of thinking.**

The best example: one of the Anthropic engineers built a frontend design skill specifically to stop Claude from defaulting to Inter font and purple gradients.

Here's why this works. If 1,000 people ask Claude to build a landing page, they'll get roughly the same output. Same layout, same fonts, same colour scheme. That's because models give you the response that's statistically most likely given your context. Without anything steering it, you get the default — the most common pattern across all the training data.

A skill shifts that. It moves the model toward a specific part of the distribution that already exists in its knowledge, but wouldn't surface on its own. It's overriding the defaults so you stop getting the same output as everyone else.

And this is exactly why "don't state the obvious" matters. If your skill just restates what's already in the high-probability region — things Claude would have done anyway — you've changed nothing. 

If anything, you're just amplifying it. You've added tokens that reinforce the default. A skill only does real work when it pushes the model toward outputs it wouldn't have generated without the skill.


---
## The gotchas section is the highest-signal part

The most valuable content in any skill is the gotchas section. Not the instructions. Not the examples. The gotchas.

Think of it like hiring a new employee. You wouldn't just hand them a job description and say "go." You'd tell them the things that will bite them. That's what a gotchas section is.

These get built over time from real failures. You use the skill. Claude makes a mistake. You add the gotcha. Use it again, different mistake, another gotcha. After a few day, the section is encoding tacit knowledge that takes humans months to accumulate.

Example: say you have a customer support reply skill. Claude's default is to be as helpful as possible — which means it'll promise timelines, commit to fixes, say whatever sounds reassuring. Without a gotcha, a generated reply says "this will be resolved within 24 hours". 

You add the gotcha: "Never promise a specific timeline for fixes. Say 'our team is actively working on this' instead."


---
## Don't railroad Claude

Now I have talked about this concept weeks ago in my Masterclass before.

Because most people think of skills as recipes, you'll be tempted to be very specific in your instructions and list steps. "First do X. Then do Y. Then do Z."

That specificity backfire in many situation. Claude will stick to your instructions even when the situation calls for something different.

This connects back to the distribution idea. Railroading is artificially collapsing the distribution to a single path. 

You're not just amplifying or suppressing parts of it. You're eliminating optionality entirely. The model can't use its judgment because you've removed the space for judgment to operate in.

Example: say you're building an interview question prep skill.

```
Too prescriptive:
1. Write 3 behavioral questions
2. Write 3 technical questions
3. Write 1 culture fit question
4. Add expected answers for each
5. Add a scoring rubric 1-5
6. Format as a printable doc
```

vs: 

```
Prepare interview questions for this role. Test for what actually predicts success here. Here are the traits our best hires had.
```

The first version produces identical output for a senior architect and a junior intern. The second lets Claude adapt to the role, the level, and what actually matters.

Describe what good output looks like and let Claude figure out the path. Give it the information it needs and the flexibility to adapt.



---

## Progressive disclosure

You don't need to cram everything into the SKILL.md.

Example: say you have a content repurposing skill. You give it a blog post and it turns it into a Twitter thread, a LinkedIn post, a newsletter section, or a YouTube script. Each platform has different constraints, different tone, different formatting.

If you put all of that in one SKILL.md, Claude reads every platform's rules every time — even if you only asked for a LinkedIn post. That's wasted context. And the more you put in, the more likely the important parts get diluted.

Instead, the SKILL.md says "repurpose this content for the requested platform. Platform-specific guidelines are in `formats/`." Then you have `formats/twitter-thread.md`, `formats/linkedin.md`, `formats/newsletter.md`, `formats/youtube-script.md`. Claude reads only the one it needs.

That's **progressive disclosure.** Tell Claude what files exist in the skill folder and let it read them when they're relevant. The SKILL.md is the entry point, not the entire skill.


---

## The description field is routing logic

When Claude Code starts a session, it builds a listing of every available skill with its description. This appears at the top in the syste mprompt.

This is what Claude scans to decide "should I use a skill for this request?"

Most people write the description like a README summary. That's wrong. The description is a **trigger condition for the model.** Write it like routing logic.

Look at these two descriptions for the same skill. The left one says "A comprehensive tool for monitoring pull request status across the development lifecycle." That's marketing copy. The right one says "Monitors a PR until it merges. Trigger on 'babysit', 'watch CI', 'make sure this lands'."

The right one literally lists the phrases a user would type. You're seeding the semantic match with the actual words someone would use when they need this skill. That's the difference between Claude picking up your skill and Claude ignoring it.

I showed exactly how to optimize this in my skill evals video — the description optimization system uses train/test splits to iterate on descriptions until trigger accuracy converges. Anthropic ran it on their own skills and saw massive improvements.


---

## Give Claude scripts, not just instructions

One of the most powerful things you can put in a skill folder is code. Not for Claude to learn from — for Claude to **run.**

Thariq's example: a data science skill that includes helper functions to fetch data from your event source. Claude doesn't need to figure out how to authenticate to your data warehouse or which tables to query — the library handles that. Claude just composes those functions into new scripts on the fly.

The model's turns are spent on composition and reasoning instead of reconstructing boilerplate. Same principle as giving a developer good internal libraries — they stop reinventing plumbing and focus on the actual problem.

This is where skills-as-folders really pays off. Your SKILL.md says "use the functions in `lib/` to query data." Claude reads the lib, understands the API, and writes new scripts that compose those functions for whatever the user asked.


---
## On-demand hooks

This connects well with the last point. 

You've given Claude scripts to pull data from a source -- say Stripe. 

But without constraints, Claude can also do random things like running queries. The scripts gave it focused power. But it still has access to everything else.

On-demand hooks fix this. Skills can register hooks that only activate when the skill is called and last for the duration of the session.

Think of it like giving an employee a keycard that only opens the rooms they need.

Continuing the Stripe example — you've got 3 scripts in the skill folder: `fetch_revenue.py`, `fetch_customers.py`, `fetch_payouts.py`. Each one has the API key and knows how to pull the data. That's all Claude needs.

So in the skill's frontmatter, you register a PreToolUse hook that blocks everything except running those 3 scripts. No `curl`. No writing new Python files. No network requests. Claude can run the 3 approved scripts and write results to `/reports/`. That's it.

```
stripe-analysis/
├── SKILL.md
├── hooks/
│   ├── guard-bash.sh      # only allows the 3 scripts
│   └── guard-write.sh     # only allows writes to /reports/
└── scripts/
    ├── fetch_revenue.py
    ├── fetch_customers.py
    └── fetch_payouts.py
```

If Claude tries anything outside that — blocked. The hook returns an error and Claude gets told why. The blast radius is contained to exactly what the skill is supposed to do.

And these hooks are temporary. They activate when the skill starts and deactivate when it's done. Your normal Claude Code session goes back to full access. It's not a permanent config change — it's a mode you switch into for a specific task.

Essentially each skill gets its own mini sandbox. The Stripe skill can only touch Stripe and reports. A deploy skill can only touch deploy tooling. A content skill can only write to the content folder. Every task runs inside its own set of constraints, and when the task ends, the constraints disappear.



---
## Store data inside skills

Some skills at Anthropic include a form of memory. An append-only log file. A JSON store. Even a SQLite database.

Example: a content publishing skill that tracks every blog post, tweet, and newsletter you've published. It appends to a log every time it runs. When you ask it to generate new content, Claude reads the log and knows what topics you've already covered — so it doesn't suggest writing about something you posted last week. Without the log, every run starts from zero and you get repeat ideas.

Same principle for newsletters, competitor checks, pipeline updates — anything periodic.

One caveat: data in the skill directory can get deleted on upgrade. Anthropic provides `${CLAUDE_PLUGIN_DATA}` as a stable folder per plugin for persistent storage.


---
## Skills are folders, not files

The biggest misconception: people think a skill is a SKILL.md file. You write some instructions, save it, done.

Thariq says that's the least interesting part. A skill is a **folder.** It can contain scripts, assets, data files, config, reference docs — anything Claude can discover and use at runtime.

The best skills at Anthropic aren't instructions. They're operational packages. The SKILL.md is just the entry point.

Everything that follows builds on this idea.


---
## Setup via config files

Some skills need context from the user before they can work. Which Slack channel to post to. Which dashboard to check. Which team to notify.

The pattern: store this in a `config.json` inside the skill directory. If the config doesn't exist on first run, the skill instructs Claude to ask the user and save their answers. After that, it just works.

You can even have Claude present structured multiple-choice questions using the AskUserQuestion tool — so the setup feels like a wizard, not an interview.


---
## The 9 types (audit your gaps)

This is a little too detailed for YouTube so I'll be releasing a video in my masterclass about this.

--- 
## The one-liner

Skills aren't markdown files. They're folders. The best ones at Anthropic include scripts, reference docs, data storage, and scoped hooks — they're operational packages that encode how your team actually works.

Build the gotchas section from real failures. Use progressive disclosure. Write your description like routing logic. And check the 9 types to find what you're not building yet.

If you want to go deeper on building and testing skills — including evals, the full testing loop, and the skills I use daily — I cover all of that in my Claude Code Masterclass. Link below.
