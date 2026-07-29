# The LLM Revolution (so far)

- URL: https://www.lesswrong.com/posts/ZuBb7Rjgajssasozr/the-llm-revolution-so-far
- Author: Eigenbraid
- Date: 2026-07-13
- Karma: 17  Comments: 0  Words: 1045
- Band: B  Tier: 1  Score: 34.9  Density: 6.7
- Anchors: claude code, \bcodex\b

---

I want to document where LLMs are at, today, partly because I don't know of any single place that brings all these examples together. I think a lot of the examples below will be surprising and unfamiliar (although maybe not to this particular audience).

Part of this is just trying to build a resource for raising the "sanity waterline". Partly it just felt like an important foundation for other ideas I want to convey.

Across Domains
--------------

Four years ago we were laughing about how AI couldn't draw a human with the right number of fingers. The state of the art can generate accurate QR codes. The most likely outcome is that LLMs continue to improve; there are numerous improvements already being developed, and no sign of things slowing down.

![A die with QR codes for each face](https://pbs.twimg.com/media/HGhUlmUX0AAQSJx?format=jpg&name=large)

([Source](https://x.com/goodside/status/2046979039412318504))

**Language:** For casual purposes, Google Translate is amazing. Twitter is now automatically translating a lot of tweets between Japanese and English, allowing two cultures to suddenly connect on a unique new level. ([Example](https://x.com/3m1ek/status/2075506532989784227)). Maybe it's not professional grade, maybe it's not perfect, but I routinely hold conversations with people who are speaking other languages.

**Customer Service:** I've started seeing a few of my calls already being answered by LLMs. They can handle real time voice and follow scripted conversation paths fairly easily - although they still need to be locked down, or else they can tricked into giving out invalid discounts ([Source](https://viewfromthewing.com/scott-kirby-promised-me-a-refund-and-uniteds-ai-chatbot-fell-for-it/))

**Search & Research**: Two sides of the same coin, as the etymology implies. AI is great at understanding plain language searches, whereas previous technologies were limited to keyword searches - TikTok doesn't understand what "unalive" means but an LLM understands it trivially. You still need to verify the documents manually - they can't do your reading for you. But even if a few of the sources they find are hallucinated, that often still leaves you with a treasure trove of obscure references you couldn't have easily found manually.

**Art:** AI Art can pass a sort of Turing Test. Humans can’t actually distinguish a lot of LLM art - just the overdone "slop" styles. ([Source](https://www.astralcodexten.com/p/ai-art-turing-test)). Even if you hate AI art, numerous studios say they're finding it great for quick sketches and proposals - it helps speed up and tighten communication between artists and art managers. ([Citation](https://variety.com/2026/film/news/martin-scorsese-supports-ai-company-storyboard-movies-1236765037/))

**Writing:** LLMs have won a few minor literary and artistic prizes. I think this reflects more on the judges being unaware of what LLM art looks like, but that just reiterates the importance of paying attention. ([Art source](https://ohiblog.com/art/ai-wins-state-fair-art-competition-sparking-debate)) ([Short story scandal](https://www.vulture.com/article/granta-commonwealth-foundation-short-story-ai.html))

**Math:** LLMs have solved multiple challenging, long-standing mathematics problems. ([Source](https://www.scientificamerican.com/article/ai-just-solved-an-80-year-old-erdos-problem-and-mathematicians-are-amazed/)). They're also seeing a lot of use for sweeping through a body of less notable work that no one has ever had the time to verify or solve ([Source](https://terrytao.wordpress.com/2025/11/05/mathematical-exploration-and-discovery-at-scale/)). The most recent paper is from July 10th, 2026 - AI has now solved a famous open problem in graph theory, using an off-the-shelf model, within a day of the model's public release ([Source](https://x.com/__eknight__/status/2075643450196971805))

**Coding:** I think most people are already aware of this, but agents like Claude Code and Codex saw an explosion in usage over the Christmas Holiday in 2025, as numerous developers finally discovered what modern models could do ([Citation](https://www.techbuzz.ai/articles/claude-code-hits-1b-as-developers-ditch-chatgpt)).

Last year, twitter user Psyho was the only human to beat AI in the AWTF competition. In July 2026, OpenAI "crushed humans", and "this is essentially the first time AI won vs humans in a programming competition in such a decisive matter" ([Source](https://x.com/FakePsyho/status/2075291659814781370)).

**Cyber-Security:** Slightly newer is Claude Mythos showing a 20x improvement in the ability of security teams to find software vulnerabilities, including numerous high severity issues. ([detailed report from the Firefox team](https://hacks.mozilla.org/2026/05/behind-the-scenes-hardening-firefox/)) ([Epoch graphs](https://epoch.ai/data/cve?view=graph), giving a broader view across 17 major vendors and 4 major open source programs)

**Prediction:** AI slightly exceeds the "wisdom of the crowds" and is on trend to out-perform even super-forecasters like Nate Silver. ([Source](https://www.astralcodexten.com/p/the-ai-superforecasters-are-here)). Per the article, some companies might already have private tools that can reliably gain at least a small edge in the stock market.

**Persuasion:** A recent surprise, this study found AI systems were reliably more persuasive than expert humans, even when expert humans chose their issues, researched in advance, underwent hours of live, structured practice, and were incentivized with £1,000 cash bonuses. ([Citation](https://arxiv.org/html/2606.16475))

A note on that last one: sure, *you'd* never fall for obvious AI propaganda. But a lot of other people will - we're already seeing it in Advertising and Politics. ([Citation](https://archive.ph/uZ61N))

The ability to produce a thousand social media accounts parroting any talking point you want - but without a clear, repetitive script to give away the game. In fact, the ability to reply to every single comment they make, ensuring they're the most engaging opponent and have the maximum chance to win over skeptics via dialogue. ([Citation](https://www.campaignnow.com/blog/how-ai-chatbots-and-influencers-are-reshaping-political-persuasion-ahead-of-2026))

The Early Days
--------------

You'll notice this is a mixed bag, ranging from "still occasionally fails at Customer Service so bad that articles get written" and "almost, but not quite, on par with experts, when measured in certain very narrow and specific ways."

LLMs are still very young. I think we're currently in something like the AOL days of the internet, before anyone figured out how to build behemoths like Amazon and Netflix.

I do think we're in for much bigger changes, but that's a topic for another post.

A Note on "Bubbles"
-------------------

There will probably be a bubble popping!

There's a lot of money going into this industry, and it's hitting before the technology is actually ready. We saw this in the DotCom crash - Pets.com wasn't wrong to try and deliver cat food, they just didn't have the logistical engine that Amazon.com later invented.

Bubbles pop because investors' imagination exceeds current realities.

But eventually reality catches up.

**The internet bubble popped. If you're reading this, you're probably aware the internet did not vanish.**

Some companies are jumping the gun, trying to do what is presently impossible. But a lot of them don't actually care whether it works today - they're building up their workforce's skill in "LLM usage" in anticipation of next year's improvements.

### **Postscript**

I'd love to hear about additional examples, especially ones that show progress in domains I didn't list, or that substantially surpass the current examples.