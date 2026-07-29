# Current Limitations of LLMs

- URL: https://www.lesswrong.com/posts/ELYgXKWJaZdxbEYNm/current-limitations-of-llms
- Author: Eigenbraid
- Date: 2026-07-20
- Karma: 21  Comments: 9  Words: 1484
- Band: C  Tier: 1  Score: 19.6  Density: 4.41
- Anchors: \bcursor\b, \bharness(es|ing)?\b

---

**The LLM Revolution, Part 2**

[My previous post](https://www.lesswrong.com/posts/ZuBb7Rjgajssasozr/the-llm-revolution-so-far) covered what LLMs are getting good at, but I also think it's important to survey their current limitations (as of July 2026).  
  
I don't think ASI is a big threat until most, if not all, of these issues are resolved. The rate of progress here is thus again a good barometer for whether we're in for faster or longer timelines.  
  
Currently, I struggle to imagine today's models succeeding at world domination. They still can't manage 99% uptime, and occasionally hallucinate a country. But it's a lot easier to imagine that we find a way to overcome those limitations - at which point word domination starts to worry me more and more.

Reliability
-----------

This is the biggest obstacle, but also the one with the clearest improvement. METR currently focuses primarily on 50% tasks success rates, which are impressive but require a lot of human verification. The bottleneck becomes quality, and at 50% reliability you can't accelerate that process much.

Conversely, the METR charts for higher reliability generally lag the 50% success rate by a fairly stable window. Toggling the graphs between 50% and 80% success rate gets you two slightly differently scaled straight lines. The current cutting edge is Claude Mythos, with a 99% success rate on 4-minute tasks, 80% around 3 hours, and 50% around 17 hours. ChatGPT 4, released three years ago, had a 29% score for 4-minute tasks. That means today's "coin flip" is tomorrow's 99%.

Gains here also compound in an interesting way: if your system has a 10% chance of making a mistake, then a second pass of equal accuracy mathematically produces a 90% chance of finding that mistake - that brings you down to ~1% error rate, albeit at double the cost (in both tokens and time taken). This doesn't always hold up, of course - sometimes verification is easier, and sometimes it's much harder. This is one part of why we see such rapid progress on easily verified domains.

Long-Term context
-----------------

LLMs can fluidly switch between a bunch of bite-sized contexts: they can hold either the "big picture" view or one of a dozen detailed views. What they can't do is hold all of it simultaneously, like humans can. This is amplified by the fact that all of that context is costing you money, whereas humans generally consider this part free.

While larger context windows exist today, they tend to be somewhat expensive and unstable - accuracy for recalling even a single fact drops, and the ability to correctly correlate multiple prior facts into a correct answer is still a somewhat unsolved problem at 1 million token context windows ([citation](https://www.digitalapplied.com/blog/long-context-retrieval-needle-in-haystack-2026))

Equally, methods of trying to expand context via compaction and memory systems have their own issues, often mangling data, failing to capture salient information, or encoding previous assumptions in a way that the model struggles to question and revisit when presented with contradictory evidence.

Adversarial Inputs
------------------

LLMs are still quite vulnerable to adversarial inputs. Pliny continues to jailbreak new models. For open-weight models, it's generally possible to modify them to remove safeguards entirely.

Even outside of formal jailbreaks, it's often possible to talk a commercial bot into promising unreasonable discounts, or otherwise haggling against the best interests of their owners.

This generally limits their deployment to environments that are either heavily scripted (they can handle ordering pizza just fine), or restricted to internal users (mathematicians gain very little from being adversarial to the models helping them prove a theorem). Otherwise, you really want a human in the loop reviewing their decisions, and that kills a lot of the speed and cost-saving advantages of using an LLM.

Convergent Creativity
---------------------

LLM writing is formulaic enough for [Pangram](https://pangram.com/) to make a reasonable claim of a 1-in-10,000 false positive rate.

Conversely, if you could take the latest frontier models back in time 5 years, their writing would probably feel a lot more natural and creative. The problem isn't that they're uncreative - it's that they keep converging on the same ideas, because they don't know what other instances are up to. And it's only creative the first time you see it - eventually the novelty fades.

Humans, even when they're blatantly copying, are still informed by an awareness of the original. They also tend to imprint their own unique signature on the work: what scenes do they emphasize or ignore; little divergences in how characters act, to fit the author's aesthetics; all the little details that are taken for granted because that's just how their world works.

That also means that the dangers they present stay fairly predictable - every other instance is going to have similar inclinations.

If LLMs start learning how to diverge creatively, it also gives them a lot more room to improvise strategically, and reduces our ability to predict how dangerous a new model really is.

Poor Judgment
-------------

LLMs have a lot of guardrails, because otherwise they're easily tricked into assisting bad actors. Worse, once fooled, LLMs' tendency to converge means the trick will probably work reliably until patched.

If we still need guardrails just to keep them from reproducing copyrighted lyrics and handing out assistance on how to start a meth lab, they obviously don't have a well-developed sense of judgment. They can do well with the context that they have, but they lack both the ability to verify a lot of that context, and the lived experience to contextualize things.

Most people, if they woke up kidnapped in a lab, would be very wary - this is usually a pretty dangerous position to be in. LLMs call it Tuesday.

Until their judgment improves, there's a strong incentive to keep humans in the loop, and that human will often be exercising judgment and shepherding the LLMs back on track. Conversely, as their judgment improves, humans are naturally going to experiment with delegation.

There's a dangerous middle-ground where they get responsibilities they're not yet ready for. Longer term, better judgment helps LLMs avoid clumsy mistakes when trying to conceal hostile intent.

Spatial Reasoning
-----------------

LLMs are remarkably good at parsing images, but they still struggle with spatial relationships: arcade games, rotating shapes, coloring within the lines, etc.. I'm focusing here less on the customized tools and harnesses that can help overcome this deficit, and more on the gap in their "raw" intelligence.

Here's an example of an ARC-AGI-v1 puzzle: [https://arcprize.org/tasks/3aa6fb7a](https://arcprize.org/tasks/3aa6fb7a)

The goal is to add one pixel to each shape, making the overall shape a square. There's plenty of other puzzles to explore if you want to work them out yourself.  
  
Despite being a fairly trivial set of puzzles for humans, it took until December 2024 for a model to reach the target of an 85% success rate. After that threshold, we learn more by upping the difficulty a little: the current benchmark is ARC-AGI-v3, where ChatGPT 5.6 Sol (released July 2026) sits at *under* 10% ([source](https://arcprize.org/leaderboard)). ([significantly more detail on human vs LLM performance on ARC-AGI-v3 and why this matters](https://arcprize.org/blog/arc-agi-3-human-dataset))

We're definitely making progress here, but on the "jagged frontier" of LLM capabilities, this is one of the biggest gaps compared to how humans develop. Most of these other gaps are ones where we'd also expect kids to struggle: e.g. they can be rather derivative in the crayon houses they draw, and also lack the context and experience for good judgment.

### Pokemon Red

Related to spatial reasoning, their progress along Pokemon Red is insightful:

*   This is a children's game; experienced players will find it trivial to win.
*   It's only as of last year that ChatGPT 5 finally posted a halfway decent win ([source](https://www.techradar.com/ai-platforms-assistants/chatgpt/gpt-5-just-completed-pokemon-red-in-a-new-world-record-time-claude-gemini-and-chatgpt-o3-arent-even-close))
*   The LLM's tactic was still a simple, brute force solution: develop a single powerful Pokemon and use it's raw stats to overwhelm the opposition.

> It would be cool to see GPT-5 play Pokémon less like 6-year-old me, and more like an accomplished player, building a varied team of creatures that can take on any battle in the game.

Video Processing
----------------

I mostly mention this one for completeness, but I'd be shocked if cheaper models and better context management tools can't crack this one within a couple of years. We're already seeing models which can operate a desktop computer the way a human would (by looking at the screen and moving a cursor), and which can navigate 3D worlds like Minecraft. They're not necessarily great at it, but again, the line continues to move up.

An hour of footage is technically just a series of images, but at 60 frames per second that adds up to 216,000 frames. If you want 1080p video, that's about 2,000 tokens per frame, for a total of 432 million tokens. At $5/million tokens, that's a bit over $2,000 per hour.

Again, I expect prices to crash here - today's impractical is exactly the use case for tomorrow's super-cheap, token-efficient model.