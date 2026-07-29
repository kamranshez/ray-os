# The Warring States Period: Frontier Labs Edition

- URL: https://www.lesswrong.com/posts/HY6zgwLLTts8mwwXq/the-warring-states-period-frontier-labs-edition
- Author: ykevinzhang
- Date: 2026-07-15
- Karma: 10  Comments: 1  Words: 2350
- Band: B  Tier: 1  Score: 36.3  Density: 8.34
- Anchors: claude code, \bcodex\b, \bcursor\b, \bharness(es|ing)?\b

---

![ChatGPT Image Jul 15, 2026, 07_20_22 PM.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784116933/lexical_client_uploads/sqvanh2yxvesmgxvrfoc.png)

*This post was originally* [*posted my Substack*](https://eastwind.substack.com/p/the-warring-states-period-frontier). I can be reached on [*LinkedIn*](https://www.linkedin.com/in/ykevinzhang/) *and* [*X*](https://x.com/ykevinzhang).

Just when it seemed that the frontier AI battle was a two-horse race between Anthropic and OpenAI, the events of the past few weeks changed the AI landscape. The releases of SpaceX’s [Grok 4.5](https://x.ai/news/grok-4-5) and Meta’s [Muse Spark 1.1](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/) put these two companies back in the conversation. Alphabet is also set to launch its next frontier model. There are all of a sudden five very credible AI players in the US alone, and the AI wars are now in its [Warring States period](https://en.wikipedia.org/wiki/Warring_States_period).

For investors, this makes the model layer harder to underwrite. Meanwhile, the easy version of the AI bottleneck trade — buying nearly every supplier exposed to rising AI capex — is over.

This piece covers the following:

*   The frontier-model market has shifted from a perceived duopoly into a fluid oligopoly, which will likely put pressure on margins
*   Unless one lab achieves a decisive recursive self-improvement breakthrough (whereby AI is used to improve itself), model leadership will remain contested
*   This will force labs to build conventional moats in distribution, workflows, cost, and customer ownership
*   Given this dynamic, I present a decision tree for how to think about the model layer and a two-part framework for navigating the AI bottleneck trade (strategic and tactical)

Let’s dive in.

### **The War of the Frontier Labs**

To level-set the conversation, we can look at the competitive positioning of the leading players in the race.

**OpenAI**

Until recently, the public’s perception of OpenAI was that it had lost its Mandate of Heaven. With the success of [Codex](https://en.wikipedia.org/wiki/OpenAI_Codex_\(AI_agent\)) and very strong models from OpenAI (GPT-5.3 through GPT-5.6), OpenAI will surprise to the upside when it next discloses its revenue (we can indirectly infer this from OpenAI’s Codex adoption below). **I also think the market is underestimating OpenAI’s consumer distribution**. If OpenAI is able to successfully spin up its advertising business and better monetize its consumer users, it will likely have more durable positioning than labs that predominantly sell AI tokens.

![1.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784116792/lexical_client_uploads/npr3ejvc4brhvbweylyl.png)

[*Source*](https://x.com/latentspacepod/status/2076840521574842401/photo/1)

**Anthropic**

Anthropic is AI’s current golden child, with revenue run-rate [estimated to be over $60B](https://newsletter.semianalysis.com/p/anthropic-3q26-profit-over-1b-the). Anthropic arguably had the best model, a widely popular harness in Claude Code, and general goodwill from the community. **However, it faces growing ecosystem and trust risks**:

*   The launch, ban, and subsequent relaunch of Anthropic’s Fable models confirmed customers’ fears that access to intelligence could be cut off with little notice. This realization will accelerate the adoption of [intelligence sovereignty](https://eastwind.substack.com/p/fable-in-shackles)
*   Claude Code [secretly transmitted users’ time zones](https://www.malwarebytes.com/blog/news/2026/07/claude-codes-hidden-tracker-was-an-experiment-says-anthropic). The core reason was to prevent widespread distillation efforts by Chinese labs. This practice betrays the trust of its broader customer base, however
*   Competing with [ecosystem partners like Figma](https://techcrunch.com/2026/04/16/anthropic-cpo-leaves-figmas-board-after-reports-he-will-offer-a-competing-product/). [I had predicted](https://eastwind.substack.com/p/frontier-ai-labs-the-call-option) that frontier AI labs need to dominate the application layer over a year ago to justify their valuations

**Alphabet**

In the first half of 2025, Alphabet trailed Anthropic and OpenAI. But Alphabet’s decade-long investment in TPUs gave it a significant compute advantage. Meanwhile, the launch of [Gemini 2.5 Pro](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/) signaled that Alphabet was “back” in the model race. Its successor, [Gemini 3 Pro](https://blog.google/products-and-platforms/products/gemini/gemini-3/), made Alphabet a consensus AI pick, and its stock price has more than doubled since Gemini 2.5 Pro.

In recent months, however, Alphabet has not been able to keep pace with Anthropic or OpenAI’s cadence of model launches. It’s too soon to write Alphabet off, as **it’s still the best vertically integrated player in AI and comes with an enviable collection of assets** (e.g. Waymo, YouTube). The imminent launch of Gemini 3.5 Pro will reveal whether Alphabet is still competitive.

**Meta**

Meta started out strong with its open-weight Llama models, but quickly fell behind closed-source labs. Starting last year, Zuckerberg went all in on AI: poaching researchers with [athlete-tier compensation packages](https://www.bbc.com/news/articles/c8730088e5do), [buying / hiring Scale AI](https://www.forbes.com/sites/jonmarkman/2026/06/16/why-meta-paid-143b-for-scale-ai-and-alexandr-wangs-data-empire/), [buying NFDG](https://www.saastr.com/the-1-1b-vc-fund-that-4xd-in-two-years-then-got-acquired-by-meta/) etc. These efforts culminated in the [Muse Spark 1.1 release](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/), which, while not leading edge, is competitive for its price point. It’s clear that **Zuckerberg views winning the AI race as existential, and is willing to incinerate capital to bring Meta to the frontier and gain model market share** (Muse Spark is even cheaper than comparable Chinese models, see below). Meta does have its own set of problems, however. Morale at the company is at historic lows, with employees getting “[drafted](https://finance.yahoo.com/sectors/technology/articles/inside-metas-ai-draft-zuckerberg-134000308.html)” to generate data for its model training runs.

![2.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784116798/lexical_client_uploads/dga5fd4v2e54k9czeie3.png)

**SpaceX**

Elon’s SpaceX made some smart moves recently. The Cursor acquisition gave SpaceX additional data which was used to train a strong [Grok 4.5](https://cursor.com/grok-4-5). While not a true frontier model, Grok 4.5 gets SpaceX back in the AI race.

Furthermore, because prior generations of Grok were no longer competitive, SpaceX rented out its spare compute capacity to [Anthropic](https://www.anthropic.com/news/higher-limits-spacex) and [Alphabet](https://techcrunch.com/2026/06/05/google-will-pay-spacex-920m-per-month-for-compute/). The headline numbers are $1.25B / month for Anthropic (300MW / 220k GPUs), and $920M / month for Alphabet (110k GPUs, which I estimate to be 150MW). On an annualized per GW basis, the math pencils to $50B / GW and ~$74B / GW for these two deals. These are obscene numbers for compute (and likely won’t last). SpaceX can leverage these proceeds to finance more training runs to catch OpenAI / Anthropic.

**Chinese labs**

Chinese labs are in an interesting spot. Two years ago, Chinese models were uncompetitive with their US counterparts. However, with the launch of [DeepSeek’s R1 model](https://huggingface.co/deepseek-ai/DeepSeek-R1), there was renewed interest in Chinese AI. The distribution strategy for these labs is releasing open-source models that match mid-tier offerings from closed US frontier labs but are very cheap to run.

Through this strategy, these labs have been able to drum up investor excitement, with Zhipu and MiniMax going public earlier this year. The major labs have all raised money recently:

*   Zhipu with [$4B from a stock sale](https://www.reuters.com/world/asia-pacific/chinas-zhipu-ai-launches-4-billion-hong-kong-shares-offering-term-sheet-shows-2026-07-08/)
*   DeepSeek with over [$7B in its funding round](https://www.reuters.com/world/asia-pacific/chinas-deepseek-closes-over-7-billion-funding-with-unusual-deal-structure-2026-06-16/) (and already raising a new round)
*   Moonshot with [$2B at a $20B valuation](https://techcrunch.com/2026/05/07/chinas-moonshot-ai-raises-2b-at-20b-valuation-as-demand-for-open-source-ai-skyrockets/)
*   MiniMax [looking to raise $2B in a stock sale](https://www.reuters.com/world/asia-pacific/chinas-minimax-seeks-raise-total-205-billion-via-share-sale-bond-issue-2026-07-10/)

With this capital, Chinese labs have another shot at trying to reach the frontier. Chinese labs face a dilemma, however:

*   Chinese labs’ strategy so far has been open-sourcing their models to get adoption
*   Inference providers like Baseten, Together AI, and Fireworks AI have been beneficiaries of serving these open models to Western customers
*   The fact that Chinese models can’t command premium pricing and that inference vendors are capturing a material portion of Chinese models’ economics has partially resulted in Chinese labs seeing slower revenue ramps compared to OpenAI and Anthropic
*   I expect Chinese labs to begin to close off their models. However, Western customers will likely not entrust their data to Chinese labs’ API endpoints, and will opt for Western models
*   Therefore, these labs will need to lean on domestic / sovereign deployments (for geos that don’t have access to US models) in addition to consumer / prosumer subscriptions
*   The solution I see for Chinese labs is to include monetization clauses on their open models so that they can actually monetize their open models from hosting providers

### **The frontier has reopened, but it has not democratized**

Last year, [I believed capital intensity](https://eastwind.substack.com/p/capital-and-industry) would concentrate model-layer returns around OpenAI, Anthropic, and a handful of incumbents. I still believe capital determines who can compete, but I underestimated how aggressively global capital was willing to finance challengers, and how quickly model leadership could rotate. This does not mean the barriers to entry have fallen. Alphabet, Meta, and SpaceX are not traditional challengers. These companies have cash-generating businesses that can fund repeated attempts at the frontier. Meanwhile, Chinese labs have stayed in the game by tapping public markets and large pools of strategic capital.

So, compared to last year, the fog of war at the model layer has thickened considerably. There are now ten at-scale labs globally, which include the five American labs and four Chinese labs mentioned above, as well as Mistral in France (OpenAI and Anthropic still dominate in terms of funding and revenue scale). This doesn’t even include the myriad neolabs that have sprung up. The key question here is whether labs have any sort of long-term moat. Here, I see two possible scenarios playing out depending on whether recursive self-improvement is achieved.

### **The model-layer decision tree**

**Scenario 1: recursive self-improvement**

*   The first lab to achieve meaningful recursive self-improvement could use its models to accelerate AI research (there are some early signs of this)
*   Once credible evidence of this flywheel emerges, capital and talent would concentrate around the leader, further reinforcing its advantage
*   This possibility can partially explain why there are still investments in neolabs (and the 1x liquidation preference if neolabs fail and sell to incumbents serve as downside protection)
*   There is a real possibility that labs get nationalized if model capability gets too powerful, as the state ultimately has a monopoly on violence (OpenAI [has already proposed giving 5% of its equity to the government](https://techcrunch.com/2026/07/02/openai-proposed-donating-5-of-its-equity-to-a-us-sovereign-wealth-fund/))
*   The scenario here ends up very much like science fiction and we might see versions of events outlined in [AI 2027](https://ai-2027.com/) occur

**Scenario 2: a rotating frontier**

*   More labs have models that are “good enough” for most workloads
*   Truly frontier models can still command premium pricing for the most demanding tasks
*   However, the price they charge for these premium tokens likely will not support multiple companies valued in the trillions
*   These labs increasingly compete at the application layer to capture revenues beyond model capability

If our base case is that recursive self-improvement does not happen in a typical investor timeline (say within the next few years), these labs will need to win via more “mundane” moats (distribution, network effects, etc.). We are seeing some early evidence of this. ChatGPT has built a good memory system that serves to anchor users. With users locked in, OpenAI can monetize through ads. Additionally, both [OpenAI](https://www.reuters.com/business/openai-courts-private-equity-join-enterprise-ai-venture-sources-say-2026-03-16/) and [Anthropic](https://www.anthropic.com/news/enterprise-ai-services-company) are working with private equity firms to embed AI capabilities in PE portcos because they know that API revenues aren’t durable. This scenario is detrimental for model-layer pricing power but bullish for the infrastructure supporting the arms race, as every credible contender must finance its own training and inference capacity.

### **Investing in AI bottlenecks, carefully**

Given the battles happening at the model layer and the [ongoing SaaSocalypse](https://eastwind.substack.com/p/the-saas-bloodbath-opportunities), how should investors think about the AI trade? The trade so far has been finding bottlenecks in the AI “stack”. This has ranged from memory to optics to power. Investors early to the wave have generated venture-like outcomes in the public markets by getting in on names like SanDisk and Lumentum.

However, this trade has become very consensus and we’re beginning to see cracks due to a combination of concerns around AI’s ROI and broader macro, geopolitical, and leverage pressures. These concerns have led to a material drawdown for most names in the AI trade. I think there are still returns to be had in the AI trade but investors need to be much more discerning. I’ve adopted a two-pronged approach to looking at the current AI trade (strategic and tactical).

First, at the strategic level, the most important question to reason through is how much revenue can AI realistically generate. [Exponential View](https://www.exponentialview.co/p/the-state-of-the-ai-economy) recently pegged AI’s current revenue run-rate at $175B. The mental model I have is: how much capex can be supported if AI revenue reaches $1T? To $5T? AI revenue figures allow us to back into what might be “feasible” capex, which we can then decompose into different things that go into capex (memory, compute, networking etc.). Investors also need to be aware of things like long-term margin profiles, depreciation assumptions, etc.

As an example, let’s say we want to invest in memory. Suppose AI revenue grows from $175B today to $2T in five years. We can estimate how much infrastructure investment that revenue pool could support, then work backward to the implied demand for memory. On the supply side, we can track fabs that are coming online to estimate memory ASPs. We can then apply a range of multiples on those earnings to get a sense of the aggregate value of memory players (e.g. Samsung, SK Hynix, and Micron). For a company like Samsung, investors need to do a bit more work to price its other business units. This exercise provides a rough framework for testing whether the implied earnings pool can support desired returns. The general consensus right now is that key AI “pinch points” like memory and [WFE](https://en.wikipedia.org/wiki/Wafer_fabrication_equipment) still have some room to run, although their growth won’t be as explosive going forward.

At the current stage of the trade, tactical monitoring is also important. The core reason is scale: it was far easier for OpenAI and Anthropic to grow their revenues quickly from a smaller base and justify the additional capex. Now that annual capex is at the $1T scale, any revenue slowdown can leave hundreds of billions in stranded capacity. Investors need to monitor things much more closely than in the past 18 months. Going back to our memory example, some indicators we want to track might include:

*   AI revenue growth & hyperscaler capex guidance
*   Significant model architecture improvements that might shift the memory supply / demand equation
*   CXMT / YMTC’s fab ramps

### **No permanent Mandate of Heaven**

The frontier AI market increasingly resembles a Warring States period. The current oligopoly dynamic and shifting model leadership imply that margins at the model layer will be heavily challenged. That said, recursive self-improvement breakthroughs could make today’s valuations look conservative and the race could become winner-take-most. If no labs achieve recursive self-improvement, the Mandate of Heaven will continue to rotate, forcing labs to compete via conventional moats.

For investors, this makes the model layer harder to underwrite. But as capex approaches the trillion-dollar scale, blindly investing in every bottleneck becomes dangerous. The next leg of the AI trade will depend on identifying which constraints remain scarce, how long that scarcity lasts, and whether suppliers can sustain their pricing power.