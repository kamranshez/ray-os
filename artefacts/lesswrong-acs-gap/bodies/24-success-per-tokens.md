# Success Per Tokens

- URL: https://www.lesswrong.com/posts/rDkaSMFfn4x6Hhkin/success-per-tokens
- Author: michaelwaves
- Date: 2026-07-05
- Karma: 8  Comments: 0  Words: 1038
- Band: A  Tier: 1  Score: 53.2  Density: 14.16
- Anchors: coding agents?, sub-?agents?, \bharness(es|ing)?\b

---

*Work smart more than hard, to expand the pareto frontier (but also work hard)*

A Pareto Frontier is a set of nondominated (optimal) solutions in multi-objective optimization. In 2 dimensions, this traces out a curve on which you can only increase one dimension by sacrificing another. Recently LLMs are being evaluated not just for their ability to complete tasks, but for how that ability changes with respect to the amount of resources (tokens) spent. Here are some interesting examples, and how the concept applies to evaluation of humans and companies as well.

In LLMs
-------

In Figure 22 of the [GPT 5.6 Preview System card](https://deploymentsafety.openai.com/gpt-5-6-preview), we see how the most recent OpenAI models compare in Multi Select Virology Troubleshooting, a benchmark that measures the model's ability to help you generate a biological virus. The x axis is API cost (a proxy for number of tokens used) and the y axis is pass@1.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783201815/lexical_client_uploads/ewsutilnj7ytppjtg15u.png)

From this graph, we can see a few things

*   The upper left corner is the best place to be, maximizing performance for minimum cost
*   The relationship between performance and cost is logarithmic, increasing sharply at lower cost but slower at higher cost
*   GPT-5.6 Sol can help you generate a virus more than half the time if you give it reasoning mode at all

Here we see the same sort of graph from [DeepSWE](https://deepswe.datacurve.ai/), a frontier coding benchmark, but reflected across the y axis to make "up and to the right" better, potentially to reduce mental strain for the venture capitalists.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783202317/lexical_client_uploads/v73oc2w5qtlsoqnqbtuj.png)

You can actually replicate (likely a subset of) this benchmark yourself by sweeping across the reasoning modes in your coding agent of choice.

We can see that

*   No matter how much compute you give to the LLMs, they only complete around 70% of the tasks
*   GPT 5.5 actually seems to be on a similar performance curve as Claude Fable 5. However, for product/business reasons their xhigh and high reasoning modes intentionally output fewer tokens to minimize cost, at the cost of coding performance
*   Frontier LLM research is for rich people: Each dot on the graph is a fourfold run of a long-horizon 113 task suite that costs roughly $700 to run once

In People
---------

Ever wonder why the frontier labs and tech companies still have you complete these archaic coding and ML puzzles even though Claude Haiku could one-shot them? In the future we can imagine everyone has a "reasoning" mode (access to LLM-generated tokens, more expensive) and not, and they want to see how you perform in instant mode. In other words, the y intercept matters.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783216818/lexical_client_uploads/g1pxk0axnevxwo9xusaa.png)

Similarly, some people are able to get more or better results out of the LLMs for a fixed token budget.

Some things I've seen include:

*   Turning off the coding agents x percent of the week to code by hand
*   Using the AIs to write automated bash scripts and custom tooling (e.g. telemetry and dashboards) instead of asking the AIs each time
*   Learning how to use ripgrep, editor keyboard shortcuts, and basic bash commands
*   Copy pasting exact file paths and URLs they'd like to be in context instead of relying on 100 explorer subagent tool calls
*   Building and sharing efficient skills and memory files
*   Exploring new agent harnesses and benchmarking them

In Companies
------------

*Entrepreneurship is the Pursuit of Opportunity Despite Resources Currently Controlled*

It seems incredible the outsized outcomes a small startup is able to achieve relative to larger companies. Startups, especially technology startups, are usually more capital-efficient and can get away with things larger traditional companies can't. This includes

*   Selling products that don't exist yet
*   Maximizing shock and drama on twitter to increase virality and lower advertising costs
*   Massive growth rates through new markets and near-zero marginal costs
*   Pivoting every 2 weeks

In startups there are only [two numbers](https://paulgraham.com/earn.html) that matter: what is the growth rate, and how big is the market/how long can growth continue? You may have encountered the meme of 20-something year old YC founders building B2B SaaS companies in industries where they have zero experience. If you think of company building as a long-horizon RL task[^pq5ys41ow7p], and revenue as performance, we can trace out Pareto frontiers for Tesla (hard tech), OpenAI (B2C SaaS), Anthropic (B2B/B2C SaaS), and Mercor (B2B).

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783216388/lexical_client_uploads/uluwkkl0gl9ppdne2uom.png)

  
We can see that, from the investor's perspective, it's so much more attractive to invest in things that return more revenue (and thus valuation) for the least risk (time) and that fit into the fund cycle of ~10 years so they can raise subsequent funds from Limited Partners (LPs). The reason for this is the growth rate is far higher and working capital far lower for companies like Mercor vs Tesla. As the saying goes, move bits, not atoms.

Just like LLM test-time compute curves, eventually the growth rate slows down (except for Anthropic for some reason). Part of it may be just rubbing against the frontiers of the market, but some other hypotheses include

*   There is more to lose, so larger companies bear more costs from cybersecurity, legal, and compliance
*   Success in an industry attracts competitors
*   Once past the early adopters who need little convincing, the customer acquisition costs scale superlinearly
*   Management is hard. The number of unique edges (relationships) between 2 nodes (people) grows quadratically as you add new people, and you need to make sure all these edges work well
*   The majority of activities done on a daily basis don't matter. This is the stuff at the edges, around a [hard core](https://www.paulgraham.com/hwh.html) of 1-3 difficult things that actually matter and need to be done, but people dance around them by doing other random things to feel productive (this is easier to do as the team scales and survival pressure weakens)

Conclusion
----------

There is a saying that if you gave infinite monkeys (or gpt2s) infinite time (tokens) one of them would eventually write Shakespeare. This is probably true for people and companies as well. Therefore the correct strategy seems to be persistence, not dying/running out of cash, and doing the hard things that improve the test-time compute curve across all levels of effort.

  

[^pq5ys41ow7p]: It's not a totally accurate analogy because the datapoints are not independent samples and can't be run multiple times