---
tags: [youtube, research, competitor]
date: 2026-06-10
---

Reverse-engineered structure playbook from Matt Pocock's (@mattpocockuk) last 10 videos, published 2026-04-29 to 2026-06-08. All 10 transcripts in [[socials/youtube/transcripts/matt-pocock/]]. Built as a structural reference for Ray's youtube-scriptwriter skill — patterns and how-to-tell-it rules, not summaries.

## The 10 videos analyzed

| Date | Title | Type |
|---|---|---|
| 2026-06-08 | Learn anything with the /teach skill | New skill launch |
| 2026-05-28 | Can Cursor's HARDCORE Review Skill Stop The Slop? | Reacting to someone else's artifact |
| 2026-05-25 | 9 Things People Get Wrong With My /grill-* skills | Usage/failure-modes listicle |
| 2026-05-21 | /handoff is my new favourite skill | Skill deep dive |
| 2026-05-14 | I stopped using /grill-me for coding. Here's what I use instead: | Skill replacement narrative |
| 2026-05-13 | Anthropic's "dedicated monthly credit" is actually a huge cut | News reaction (same-day) |
| 2026-05-12 | New Skills! /handoff, /prototype, /review and /writing-* | Changelog roundup |
| 2026-05-07 | Burn through the backlog from hell with /triage | Skill deep dive |
| 2026-04-30 | I Open-Sourced My Own AFK Software Factory | Tool launch |
| 2026-04-29 | How To De-Slop A Codebase Ruined By AI (with one skill) | Concept + skill |

---

## 1. Hook anatomy

**The formula (9/10): personal-discovery framing, never announcement framing.** Matt almost never opens with "today I'm going to show you X" or "X just launched". He opens with *himself noticing something* — a realization, a habit, a dissatisfaction — and the artifact emerges as the resolution of that personal arc. The hook structure is: (1) credibility/context beat in first person, (2) a tension or itch, (3) the artifact as the payoff, (4) explicit promise ("I'm going to show you how I did it"). Social proof (star counts, user messages) is woven into the first 60 seconds in 7/10 videos.

Three representative hooks, verbatim:

> "I realized the other day I've been teaching stuff for 10 years. I was a voice coach for 6 years and I've been doing this job teaching devs for 4 years. And for a while I've been thinking, wouldn't it be great if I could take everything I know about teaching and put it inside a skill so that anyone could learn anything. I had a long bus ride to London the other day and I wrote a teach skill and it turns out that it's pretty good. It taught me how to solve a Rubik's cube... And I'm going to show you how I did it." (/teach)

> "A few months ago, I wrote a few sentences, about four sentences, that have turned out to be the most influential four sentences I've ever written... I know this skill is influential because every single day I receive about five messages of people saying they've tried it and they love it... And after all that praise, you might think, well, you should probably stick with that skill, shouldn't you? ... And it turns out I've actually built a better one." (grill-me replacement)

> "A few weeks ago, I noticed myself doing something with agents that I thought was very clever, but I thought it was just too simple to require a skill... I put this into my skills folder as an experiment to see how much I would use it. And it turns out I used it a lot." (/handoff)

Notice the recurring hook verbs: "I realized", "I noticed myself", "It turns out". Even the news video (Anthropic credit) opens problem-first: "An important announcement I have today for anyone who's interested in using Claude programmatically" — audience-targeted, then "this thing that sounds like a bonus, why it might not actually be a bonus" (a contrarian promise, mirrored in the title).

**Sub-pattern: deliberate suspense delay.** In 6/10 he states the problem and his journey but withholds the artifact's name or mechanism for 60-90 seconds. The de-slop video spends a full minute on "AI has simply accelerated software entropy" before naming the skill.

## 2. Structure skeleton

**The recurring spine (8/10):**

1. **Personal hook** (problem I had / thing I noticed) — ~60-90s
2. **Concept layer** — he teaches the *mental model* needed to understand the artifact BEFORE the demo. "The key concept when we're looking at a teach skill is some skills can be stateful and some skills can be stateless" (/teach). The de-slop video spends ~40% of runtime defining modules, interfaces, seams, adapters: "Right, that's enough knowledge. We know the basic terms of engagement. Now, let's go and improve a codebase."
3. **Read the artifact itself** — he literally reads the skill/prompt file on screen and gives commentary line by line. This is his signature mid-section. "Let's just read the skill because actually reading the skill really explains the skill this time." (changelog)
4. **Live demo on his own real project** — never a toy app. He runs the skill on Sandcastle, his course-video-manager repo, his own GitHub issues, and reacts in real time ("Oh my god, look at this", "Okay, Claude is trolling me here").
5. **Scoring/judgment beat** — he keeps a running verdict during the demo: "So two out of three, not bad... I think we're at three out of four, which is good... This is five out of six so far." (Cursor review)
6. **Generalization outward** — what this means for engineering, teams, the future ("we the developer community... are the first people to really experience what AI can do").
7. **CTA + community ask** — newsletter/cohort + "let me know what you want to see next".

**Transitions are verbal signposts, frequency ~every 2 minutes:** "Let's get started", "So let's ping this off and see what happens", "Now we understand all the pieces, let's go back up to here", "Right, that's enough knowledge", "Let's quickly talk about the benefits here", "So, let's summarize all the things we learned." The listicle video (9 things) ends with a full verbal recap of every point — he re-teaches the whole video in 60 seconds before the CTA.

**Concept-first, demo-second is the default.** The demo never opens the video; it sits in the middle 50%, sandwiched between mental models and generalization. Where there are diagrams (context-window smart/dumb zone, module seams), they carry the explanation; the code demo *verifies* the concept rather than introducing it.

## 3. Analogies and coined terms

**Coining vocabulary is the backbone of the channel, not decoration (10/10).** Every video either introduces or re-uses his named concepts, and the names then become future video titles. Inventory across just these 10: *grilling / grillable / ungrillable questions, the dumb zone and smart zone (120K), AFK agents / AFK use cases vs human-in-the-loop, software factory, DIY sub agent, fire-and-forget, stateful vs stateless skills, deep vs shallow modules, seams, adapters, locality, leverage, code judo, loudness in prompts, contextual vs parametric knowledge, zone of proximal development, queue management, the sergeant and the general (tactical vs strategic programmer).*

Two deployment rules visible:

1. **Define on first use with a one-sentence plain-English gloss, then reuse without re-explaining.** "For those who don't know, about 120K is where I estimate most state-of-the-art models, that's where their dumb zone begins." Later videos just say "dumb zone" cold — which rewards repeat viewers and makes casual viewers feel they're missing a lexicon (a retention/subscription mechanic).
2. **Borrow academic authority, then simplify.** He explicitly credits sources: Ryan Singer's Shape Up (fidelity), Eric Evans' DDD (ubiquitous language, bounded context), Ousterhout's A Philosophy of Software Design (deep modules), hexagonal architecture (adapters), pedagogy (zone of proximal development), Mr. Beast ("packaging before content"). The citation does double duty: credibility plus a "real engineering fundamentals" brand position.

Analogies are structural, not one-off: "it's just managing two separate Slack threads at the same time" (parallel sessions), "sediment of different layers" (repeated compaction), "agents as really, really good tactical programmers... but they need someone on the level above them who is the strategic programmer... the sergeant... the general", "cuts through the Gordian knot". Each analogy is the *frame for a whole section*, not a passing joke.

## 4. CTA and monetization

- **What he pitches:** the AI Hero newsletter ("AI skills for real engineers") in 8/10; the paid cohort "AI coding for real engineers" in 4/10 (the four videos closest to the June 1 start date); the skills repo itself (free, star-count flex) in 10/10.
- **Where:** ONE primary CTA block, placed at the very end (8/10). Twice he drops a mid-video CTA (~20-25% in): the grill-skills listicle ("only one day and 11 hours left for 30% off") and the handoff video — both during the cohort launch window. So: evergreen videos = end-only CTA; launch-window videos = one early + one late.
- **Urgency language only when real:** countdown timers tied to the actual cohort deadline ("woo, one day, 10 hours left to get it at a discount"). No fake scarcity otherwise.
- **The product pitch is always continuity, not interruption:** "If you're digging my skills, then you should go to AI hero/skills and sign up for my newsletter that lets you know whenever I release a new skill." The free artifact IS the funnel; the CTA just names the next step.
- **Soft engagement CTAs are framed as input requests, not "like and subscribe":** "if you have an idea for a video you want me to make next, then let me know about it because I thrive off your suggestions" / "if there's a skill that you want me to review... then let me know."

## 5. Delivery style

- **Short declarative sentences punctuated by tiny verbal reactions.** "Lovely." "Interesting." "Makes sense." "That's nice." "Beautiful." "Bonkers." These one-word verdicts pace the artifact-reading sections and signal his judgment continuously.
- **Heavy second person, but as coaching, not narration:** "You need to understand things like scope... it is your job to figure out where you're going." He addresses the viewer as a practitioner he's coaching ("I want to make you really good at using these skills"), and as "pals"/"folks".
- **Code is narrated-while-read, never typed live.** He reads existing files (skills, prompts, main.ts) aloud with running commentary, and runs agents live then reacts to their streamed output. He doesn't write code on camera. Demos are agent-driven: "Let's fire this off and see what happens" → cut → reaction.
- **Authentic imperfection kept in:** false starts, "whoa, 1,000 Sorry, 109,000 stars", live surprises ("Oh my gosh, look at this"), admissions ("a bit of movie magic for you" when a fix was pre-vetted), and meta-commentary on his own editing ("this video is in a slightly different style... a little less cutty... let me know what you think").
- **Honest hedging as a trust signal (7/10):** "I'm not doing evals here. Maybe I should be", "It's arguable whether I prefer that", "I am a teacher. I am not a pundit." He scores other people's work out loud, including against himself ("two out of three, not bad").
- **Transparent about workflow:** mentions dictation (Whisper Flow), context budgets on screen, which model he's using ("Opus 4.8 with medium effort") — workflow voyeurism is part of the content.

## 6. Title + topic strategy

- **9/10 titles are single-artifact, not roundups.** One skill, one tool, one announcement per video. The only roundup is explicitly labeled "Skills Changelog" — a recurring serialized format.
- **Slash-command syntax in titles (5/10):** "/teach", "/handoff", "/triage", "/grill-*". The artifact's literal invocation name is the title noun. This makes the title itself a product handle.
- **First-person stakes verbs:** "I stopped using...", "I Open-Sourced My Own...", "my new favourite". Titles read as personal testimony, not tutorials.
- **Contrarian/negation framings:** "is actually a huge cut", "9 Things People Get Wrong", "Can X Stop The Slop?" — a claim the thumbnail-clicker wants resolved.
- **News speed: same-day.** The Anthropic credit video: "A couple of hours ago, Claude devs posted this update." The grill-skills video: "Hopefully, I can post this video today."
- **Cadence ~2/week, and videos chain into each other.** /handoff appears as a teaser in the changelog (05-12), gets its own video (05-21), then is referenced as a known tool in the grill-skills video (05-25). Each artifact gets: changelog mention → dedicated deep dive → reuse as vocabulary. One idea, three videos.
- **He milks one ecosystem.** All 10 videos orbit a single owned asset (the skills repo + Sandcastle). The repo's star count is quoted in 6/10 videos as an escalating ticker (41.5k → 70k → ~100k → 109k), which turns the channel into a serialized growth story.

## 7. Non-obvious moves Ray's formula doesn't currently have

1. **"Read the prompt on screen" as the main content block.** Matt's most distinctive segment is literally scrolling a markdown file and editorializing line by line. It is cheap to produce, deeply educational, and positions him as the person whose *judgment about prompts* you trust. (10/10 videos contain artifact-reading.)
2. **The running scorecard during reaction content.** "Two out of two... five out of seven" gives a reaction video a narrative spine and a verdict the viewer waits for.
3. **Audience quotes as social proof montage.** He screenshots/reads real user messages ("Grill Me skill is goated") — 4/10 videos. Includes one emotional outlier story (the eulogy) for breadth.
4. **The escalating public metric.** Star count as a recurring serialized character. Viewers tune in partly to watch the number go up.
5. **Teasing in-progress work.** The changelog shows half-finished skills ("I don't think they're going to be ready anytime soon") — building anticipation pipelines for future videos.
6. **Explicit identity claim repeated across videos:** "I am a teacher. I am not a pundit." He refuses hot-take positioning even in a news video, which differentiates him in a punditry-saturated niche.
7. **Failure-modes content about his own product.** "9 Things People Get Wrong With My X" — turning user error reports into a video that simultaneously fixes onboarding and re-markets the product.
8. **Ending with a personal, forward-looking beat:** bookshelf video tease, "I'm going to get this thing to teach me vocal harmonies" — a parasocial hook into the next upload.

---

## How Ray should apply this

Prioritized scriptwriting rules for the youtube-scriptwriter skill:

1. **Open every script with a first-person discovery arc, never an announcement.** Template: "I noticed/realized [personal moment] + [tension] + it turns out [artifact] + I'm going to show you how." Withhold the feature's name or mechanism for the first 60-90 seconds. Ban "Today I'm going to show you" and "Anthropic just released" as opening lines — convert news into "what this means for the way I work."
2. **Teach the mental model before the demo.** Every script gets a concept section with one named idea (2-4 minutes) before any screen recording. The demo's job is to *prove* the concept, not introduce it. Bridge with an explicit signpost: "Right, that's enough theory — let's run it."
3. **Coin one term per video and build a personal lexicon.** Name the pattern (Ray's equivalent of "dumb zone", "grilling", "AFK agents"), define it in one plain sentence on first use, then reuse it cold in later videos and titles. Track the lexicon in the scriptwriter skill so scripts cross-reference earlier coinages.
4. **Demo on your real projects with a running verdict.** Use ray-os, the school platform, real A/B data — never toy examples. When reacting to or testing anything, keep an out-loud scorecard ("that's two for two") so the video has a verdict the viewer waits for. Keep live reactions and honest hedges in the script ("I haven't evaled this", "this one I'd reject").
5. **One artifact per video, one idea per artifact, three videos per idea.** Tease it in a roundup/changelog-style video, give it a dedicated deep dive, then reuse it as assumed vocabulary in the next video. Title with the artifact's literal handle plus a first-person stake or negation ("/skill-name is...", "I stopped doing X", "...is actually Y").
6. **Single end-of-video CTA chain: free artifact → newsletter → paid class.** Frame it as continuity ("if you're digging this, the next step is..."), use urgency only with a real deadline, and replace "like and subscribe" with an input request: "tell me which skill to break down next."
7. **Serialize a public metric and your in-progress work.** Pick one number (students, A/B tests run, skill installs) and quote it every video as an escalating ticker; end scripts with a personal forward tease of what you're trying next.
