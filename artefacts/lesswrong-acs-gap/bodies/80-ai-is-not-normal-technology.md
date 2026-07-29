# AI is Not Normal Technology

- URL: https://www.lesswrong.com/posts/F2mwKxFRhjqizA89p/ai-is-not-normal-technology
- Author: Olivia Scharfman
- Date: 2026-05-22
- Karma: 16  Comments: 2  Words: 5656
- Band: C  Tier: 1  Score: 16.5  Density: 3.01
- Anchors: claude code, \bcodex\b, \bcursor\b

---

Last year, [Arvind Narayanan](https://knightcolumbia.org/authors/arvind-narayanan) and [Sayash Kapoor](https://knightcolumbia.org/authors/sayash-kapoor) published a now well-circulated essay, [*AI as Normal Technology*](https://knightcolumbia.org/content/ai-as-normal-technology). The essay is still popular, I think, primarily because people would like it to be true, myself included. It is a terrifying proposition to acknowledge how different AI may be from “normal” technology. However, acknowledge it we must –– the urgency of developing proper governance and technical progress on alignment cannot be overstated.

I think the essay has significant flaws. This response walks through the most important ones in an effort to demonstrate the importance of acknowledging the tremendous nature of the changes superintelligent AI may bring.

This is a linkpost, with minor modifications, for a [blog post](https://oliviahelens.substack.com/p/ai-is-not-normal-technology) published yesterday. Post-publishing, I saw Scott Alexander's [response](https://blog.ai-futures.org/p/ai-as-profoundly-abnormal-technology) and realized that I overlap with him substantially on some of the arguments. I'm posting regardless because where we overlap my response tends use alternative or updated examples. I also push on points that Alexander does not, including that biosecurity as the most concrete catastrophic risk, offering chess history as a parallel for how Narayanan and Kapoor's argument may age, and examining now-falsified or soon-to-be falsified empirical predictions in the essay about forecasting and persuasion. I invite pushback, particularly on the discussion of labor and how significant current uplift from models is.

The essay consists of Narayanan and Kapoor laying out a scenario they deem to be the median outcome, in four parts, roughly as follows:

> **Part I: Speed.** They argue that transformative economic and societal impacts will be slow and there is a distinction between AI methods, AI applications, and AI adoption, including different timescales.
> 
> **Part II: Division of labor.** They discuss potential division of labor in a manner they say does not apply to “superintelligent” AI, which they “view as incoherent as usually conceptualized.” They argue control is primarily in the hands of people and organizations; indeed, a greater and greater proportion of what people do in their jobs will be AI control.
> 
> **Part III: AI risks.** They argue viewing AI as normal technology leads to fundamentally different conclusions about mitigations compared to viewing AI as being humanlike.
> 
> **Part IV: AI policy.** They argue we should reduce uncertainty as a first-rate policy goal, use “resilience” as the overarching approach to catastrophic risk, and that drastic interventions premised on the difficulty of controlling superintelligent AI will make things worse if AI turns out to be normal technology.

If the question is “will the labor market be unrecognizable in 2035,” they’re probably closer to right than wrong. However, I do not think this is the question. The question is, “might this be more transformative for what it means to be human than any other technology in the history of man?” I think the answer to that question is yes. If so, it would be quite difficult to settle on thinking that AI is “normal technology” in the sense that Narayanan and Kapoor are calling it so.

In what sense are they calling it so? Here are some bits of the essay I think exemplify what they mean by normal technology; I have bolded the parts I disagree with at this time:

> To view AI as normal is not to understate its impact—even transformative, general-purpose technologies such as electricity and the internet are “normal” in our conception. But it is in contrast to both utopian and dystopian visions of the future of AI which have a common tendency to treat it akin to a separate species, **a highly autonomous, potentially superintelligent entity**.
> 
> The statement “AI is normal technology” is three things: a *description* of current AI, a *prediction* about the foreseeable future of AI, and a *prescription* about how we should treat it. We view AI as a tool that we can and should remain in control of, and we argue that this goal does not require drastic policy interventions or technical breakthroughs. We **do not think that viewing AI as a humanlike intelligence is currently accurate or useful for understanding its societal impacts, nor is it likely to be in our vision of the future**.
> 
> The normal technology frame is about the relationship between technology and society. It rejects technological determinism, especially **the notion of AI itself as an agent in determining its future**. It is guided by lessons from past technological revolutions, such as the slow and uncertain nature of technology adoption and diffusion. It also emphasizes **continuity between the past and the future trajectory of AI in terms of societal impact and the role of institutions in shaping this trajectory.**

I appreciate that Narayanan and Kapoor think they are not understating its impact, but they go on to make arguments that explicitly understate its impact.

For example, they make good points about things like benchmarks not always measuring real-world utility, there being a gap between capability and reliability, and diffusion, especially in safety-critical domains, being slow and constrained by human organization and institutional change. These points are made with the implicit intention of minimizing the impact of AI.

They also say that the essay has “the unusual goal of stating a worldview rather than defending a proposition,” then go on to defend their propositions, not against any possible counterargument, but certainly to justify them against the prevailing narrative.

I believe their view of AI as merely a new tool, particularly one that does not require technical breakthroughs to control, is deeply wrong. I think their policy conclusions may be correct, but for reasons that have less to do with thinking AI is normal technology and more to do with thinking it isn’t. Because AI is not normal, it is especially true that we must not decelerate our defensive capabilities as our adversaries accelerate their offensive ones. Because AI is not normal, it is more critical than ever that the United States, and the West broadly, maintains control over the direction of this technology.

#### **On Diffusion and Reference Class**

To reach their conclusion, Narayanan and Kapoor’s central logic is jumping from something like “impacts arrive gradually” to “this is continuous with past technologies” to “therefore AI is normal technology.” Impacts may indeed arrive gradually –– at first. It was predictable that something like this would be developed, but it is a non sequitur to conclude that this makes AI “continuous” and therefore “normal” technology. Something being predictable does not make it continuous. I believe these are distinct claims.

AI being “not normal” does not require [Bostromian fast takeoff](https://en.wikipedia.org/wiki/Superintelligence:_Paths,_Dangers,_Strategies). The transformation can be slow and still be *categorically* different from prior technological transitions.

Most of their arguments in this section rely on somewhat twisted choices of relative measure.

They write:

> Even outside of safety-critical areas, AI adoption is slower than popular accounts would suggest. For example, a study made headlines due to the finding that, in August 2024, 40% of U.S. adults used generative AI.13 But, because most people used it infrequently, this only translated to 0.5%-3.5% of work hours (and a 0.125-0.875 percentage point increase in labor productivity).
> 
> It is not even clear if the speed of diffusion is greater today compared to the past. The aforementioned study reported that generative AI adoption in the U.S. has been faster than personal computer (PC) adoption, with 40% of U.S. adults adopting generative AI within two years of the first mass-market product release compared to 20 % within three years for PCs. But this comparison does not account for differences in the intensity of adoption (the number of hours of use) or the high cost of buying a PC compared to accessing generative AI. Depending on how we measure adoption, it is quite possible that the adoption of generative AI has been much slower than PC adoption.”
> 
> The claim that the speed of technology adoption is not necessarily increasing may seem surprising (or even obviously wrong) given that digital technology can reach billions of devices at once. But it is important to remember that adoption is about software use, not availability. Even if a new AI-based product is instantly released online for anyone to use for free, it takes time to for people to change their workflows and habits to take advantage of the benefits of the new product and to learn to avoid the risks.
> 
> Thus, the speed of diffusion is inherently limited by the speed at which not only individuals, but also organizations and institutions, can adapt to technology. This is a trend that we have also seen for past general-purpose technologies: Diffusion occurs over decades, not years.

The PC comparison is not appropriate here. AI is significantly more comparable to social media, search, or the smartphone, all of which took years rather than decades to “takeoff.” They say it is about software use as opposed to availability, but use a survey-based measure of adult adoption which excludes API/enterprise use and likely misses the heaviest individual users.

They then discuss something called the “bitter lesson,” a term that comes from a [2019 essay from Richard Sutton](http://www.incompleteideas.net/IncIdeas/BitterLesson.html). Narayanan and Kapoor write:

> The “bitter lesson” in AI is that general methods that leverage increases in computational power eventually surpass methods that utilize human domain knowledge by a large margin. This is a valuable observation about *methods*, but it is often misinterpreted to encompass application development. In the context of AI-based product development, **the bitter lesson has never been even close to true**.^23^ Consider recommender systems on social media: They are powered by (increasingly general) machine learning models, but this has not obviated the need for manual coding of the business logic, the frontend, and other components which, together, can comprise on the order of a million lines of code.

As they mention, the intelligent part of recommenders has followed along Sutton’s predicted path: content-based filtering or neighborhood-based collaborative filtering → matrix factorization → deep learning → transformer-based models. Each transition replaced more human-led work with general model-led methods, scaled with more compute.

The [essay they cite](https://www.normaltech.ai/p/ai-companies-are-pivoting-from-creating) is their own, which argues that turning LLMs into reliable products requires substantial engineering work that companies underestimated, but does not support the strength of claim they are making. In the year since this essay was published, I believe these statements have already been falsified. We are absolutely moving towards more model-led business logic, frontend, and other components. Some companies now write minimal code by hand, with software engineers preferring to use Claude Code, Codex, or Cursor. [Claude Code itself is about 90% written by Claude Code](https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/). I have also seen multiple business briefs written entirely by AI, and have little doubt decisions at major businesses are now being discussed with and possibly deferred to AI.

Their arguments about slow absorption of institutions are fine; however, slowness of institutional adoption tells you about institutions, not about the thing being adopted. And it certainly does not tell you about what things will look like 50 years from now. Basically, they might be completely right about diffusion, but this is not relevant to normalcy.

They write that “Even if every task that humans do *today* might be automated one day, this does not mean that human labor will be superfluous.” Generations that remember other automations think this way, and I understand why. They remember other groups of people speaking out regarding past advancements in technology. It has previously been correct to believe this. To those folks, I ask you to extrapolate further –– are we really to believe there are infinite jobs to regress to if energy is cheap, AI can replace human intelligence, and AI-enabled humanoid robots can replicate all human labor? What is left?

There are many arguments against this, the best of which is that this will lead to some kind of post-commodity economy. Economics Professor Alex Imas writes about this in his article, [*What will be scarce?*](https://aleximas.substack.com/p/what-will-be-scarce) He says there is a world “where a growing share of expenditure goes toward goods and services whose value is inseparable from the human who provided them.” I agree with him on some level, as well as others who have made this point, like [Seb Krier](https://aleximas.substack.com/p/the-cyborg-era-what-ai-means-for), Google DeepMind’s policy lead. However, even in the best of cases, this is a disaster for the developing world, and it is unclear that AI will not simply create a better alternative to the goods and services that typically fall into this category or that tastes will not change. People may eventually not care about whether Starbucks handwrites your name on a cup, or there may be a robot that engraves it with your own personal portrait that people want more. The television has largely replaced bards, and the market ratio of TV & movies to theater is at least 20:1. (I hold this view very weakly relative to the rest of this response.) Essentially: slow as it may begin, diffusion will happen, and it is unclear what jobs survive this.

The deeper issue is their choice of reference class. Narayanan and Kapoor bring up electricity as an analogous thing that took time to reshape the economy. This may very well be a solid argument that general-purpose technologies take time to reshape economies. It is unclear to me that AI belongs in the reference class of electricity rather than in some new category. General-purpose though it may be, commodification of human thought, creativity, and (soon) physical labor, is normal *until it isn’t.*

In fact, **everything never changes, until it does.** The argument from continuity for AI being normal has a structural problem in generalizing from the fact that many past predictions of discontinuity were wrong. This reasoning, taken to its limit, says nothing can ever be a change greater than any that has come before.

I believe this is more of the Lucretius problem. People are biased (usually rightly so) by the magnitude of changes they have seen before.

> *A little river seems to him, who has never seen a larger river, a mighty stream; and so with other things –– a tree, a man –– anything appears greatest to him that never knew a greater. –De Rerum Natura, Titus Lucretius Carus*

As Narayanan and Kapoor acknowledge on some level, *step changes are normal*. Somewhere in the history of a species, there are technologies that change what the species *is*. I think that AI is one of these great step changes.

Every prior technology has complemented cognition. This one emulates it, and enables the simulation of essentially *any kind of labor*.  Every prior general-purpose technology in history improved human capability by giving us better tools to *act on the world with our minds*. AI is the first technology that acts on the world after being prompted *simply with our faintest desires*. It is the first technology that can act on the world with *its* mind. **It is the first and only technology which in theory could continue to expand and consume energy on its own indefinitely.**

#### **On Intelligence**

One of Narayanan and Kapoor’s other lines of argument is to deny that something like “superintelligence” is coherent or could exist by denying that such a thing as *intelligence* exists. It is a bizarre line of reasoning to follow:

> Can AI exceed human intelligence and, if so, by how much? According to a popular argument, unfathomably so. This is often depicted by comparing different species along a spectrum of intelligence.
> 
> However, there are conceptual and logical flaws with this picture. On a conceptual level, intelligence—especially as a comparison between different species—is not well defined, let alone measurable on a one-dimensional scale.

They also include this chart, which they say is wrong:

[![](https://substackcdn.com/image/fetch/$s_!XSAh!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88c30d41-1e21-4519-830a-df96360f834c_1618x534.png)](https://substackcdn.com/image/fetch/$s_!XSAh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88c30d41-1e21-4519-830a-df96360f834c_1618x534.png)

I cannot fathom that someone would try to deny that intelligence between species varies measurably. They are trying to pretend AI is normal by saying the thing that it is is not measurable, but intelligence *is* measurable. You, reading this, *are* smarter than a mouse. So is Opus 4.7. Intelligence being multidimensional does not mean it is not orderable, nor does it mean that those dimensions don’t correlate/are not reducible.

I’ve many times heard the argument that AI cannot be smarter than the smartest human because it only has human data to train from, or that it can never do novel work for the same reason. I think it should be obvious that this is not true. First, it doesn’t only have human data to train from –– soon we will have AIs trained on any real-world data they can collect. Second, even if for some extraordinary reason you *were* constrained by human intelligence, I implore you to imagine one million von Neumanns collaborating on problems together at machine speed. Lastly, there is mounting evidence emerging for technical creativity and ability to do novel work. This includes novel mathematical proofs, especially given the [recent announcement](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) from OpenAI on one of their models disproving a central conjecture in discrete geometry. We are watching these assumptions fail in real time.

Narayanan and Kapoor then go on to say that actually, intelligence doesn’t even matter:

> More importantly, intelligence is not the property at stake for analyzing AI’s impacts. Rather, what is at stake is power—the ability to modify one’s environment.

To which I say: intelligence historically *has always been correlated with the power to modify one’s environment*. AI podcaster and writer Dwarkesh Patel has an interesting piece countering this, called [*The mistake of conflating intelligence and power*](https://www.dwarkesh.com/p/the-mistake-of-conflating-intelligence). His argument is that the world’s most powerful people aren’t its smartest, which is fair. However, the most powerful humans *do* “max out” intelligence in the only way they can, since you can’t really raise your own: they hire all the physicists. Essentially, intelligence is necessary but not sufficient for power. You also need courage and goals. Computers don’t need courage, will be given goals by default, and can hire both people and other AIs.

Narayanan and Kapoor add the image below to illustrate how they conceive of technology, not intelligence, being the source of capability. I would be curious to understand how they think we developed technology in the first place, if not from intelligence.

[![](https://substackcdn.com/image/fetch/$s_!-cei!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6dc9e4bc-3468-4c7a-8894-792cc12f70ff_1636x582.png)](https://substackcdn.com/image/fetch/$s_!-cei!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6dc9e4bc-3468-4c7a-8894-792cc12f70ff_1636x582.png)

They then say:

> De-emphasizing intelligence is not just a rhetorical move: We do not think there is a useful sense of the term ‘intelligence’ in which AI is more intelligent than people acting with the help of AI. Human intelligence is special due to our ability to use tools and to subsume other intelligences into our own, and cannot be coherently placed on a spectrum of intelligence.

This is approximately true by construction and not true in any real sense of the word. They’ve defined the relevant unit as “human + AI,” so any AI improvement gets absorbed into the unit and counted for the human.

In reality: AIs can already use tools. AIs will be able to “subsume” other intelligences to their own, more literally than a person is able to do so. AI was *trained by subsuming our intelligence.* It may lack agency in some sense, but this doesn’t make it any less dangerous. It will be able to decide, potentially with little to no human input, what it thinks needs to be done.

We have seen Narayanan and Kapoor’s argument before. For decades, top chess players and critics argued that computers would never play chess at the level of the best humans, because human intelligence is “special”.

IM David Levy bet AI researchers in 1968 that no computer would beat him within ten years, and won the bet in 1978. In 1996, Levy predicted Kasparov would beat Deep Blue six games to zero, and said, “I’d stake my life on it.” Kasparov had played 32 chess computers simultaneously in 1985 and beat all of them. He rebuffed IBM’s offer to split the Deep Blue prize money 60-40 in 1996. Karsparov won the match 4-2, and the rematch was set for 1997. Of his attitude at the rematch, he said he thought, “I will beat the machine, whatever happens. Look at Game One. It’s just a machine. *Machines are stupid.*” He lost the rematch.

When Deep Blue won, the response was not to update the understanding of how good machines are, but to decide chess was “just brute force,” so for a computer to be real intelligence it had to learn Go or language, or something. The goalposts moved, and continue moving to this day. Kasparov’s response was to develop “centaur chess” i.e. human plus computer playing as a team and to argue, from 1998 through at least 2017, that centaur teams beat the strongest computer alone. In truth, sometime around 2013 the human became useless in chess, and the gap has only widened since.

Narayanan and Kapoor are making the same two arguments, applied to AI generally. They claim intelligence isn’t well-defined enough for modern AI to count, shifting the goalpost. They claim human + AI is the relevant unit, that there is no useful sense in which AI is more intelligent than people acting with AI. There is no reason to think the argument that didn’t work for chess models will work for language models.

They know the centaur story, and they think it is a question of speed. They write:

> Human abilities definitely have some important limitations, notably speed. This is why machines dramatically outperform humans in domains like chess and, in a human+AI team, the human can hardly do better than simply deferring to AI…In many other areas, including some that are associated with prominent hopes and fears about AI performance, we think there is a high ‘irreducible error’—unavoidable error due to the inherent stochasticity of the phenomenon—and human performance is essentially near that limit

To this, I point out that protein structure prediction isn’t speed-bound. Humans plateaued at ~40% accuracy and AlphaFold reached ~90%. Theorem proving isn’t speed-bound, and recent systems are producing novel proofs for problems that humans have spent years working through. In both cases, humans are/were not near an “irreducible” limit, just a human one. I do not think we can tell how stochastic the world is from our position of lesser understanding. Many things may be more solvable than we think, and AI may be able to do it.

#### **On Speculative Risks, Control, and Access**

Narayanan and Kapoor are not worried about catastrophic risk, which they describe as speculative:

> In the view of AI as normal technology, catastrophic misalignment is (by far) the most speculative of the risks that we discuss. But what is a speculative risk—aren’t all risks speculative? The difference comes down to the two types of uncertainty, and the correspondingly different interpretations of probability.
> 
> In early 2025, when astronomers assessed that the asteroid YR4 had about a 2% probability of impact with the earth in 2032, the probability reflected uncertainty in measurement. The actual odds of impact (absent intervention) in such scenarios are either 0% or 100%. Further measurements resolved this “epistemic” uncertainty in the case of YR4. Conversely, when an analyst predicts that the risk of nuclear war in the next decade is (say) 10%, the number largely reflects ‘stochastic’ uncertainty arising from the unknowability of how the future will unfold, and is relatively unlikely to be resolved by further observations.
> 
> By speculative risks, we mean those for which there is epistemic uncertainty about whether or not the true risk is zero—uncertainty that can potentially be resolved through further observations or research.

If we are to grant their distinction here between what they are calling stochastic uncertainty (nuclear war scenario) and what they are calling epistemic uncertainty (asteroid scenario), it is clear the uncertainty about AI is closer to the nuclear war scenario than to the asteroid scenario. AI is currently rather representative of stochastic unknowability. The asteroid case is a single physical trajectory resolvable by one better measurement and AI risk is the opposite. It is not a question of “what is the true underlying probability our measurements just can’t see right now?” but “how will billions of deployment choices, inevitable adversarial use, and emergent system behaviors unfold?”

Moreover, just because a risk is low, which is what they really seem to mean here, does not mean it should not be prioritized. The expected value of addressing a risk is not based simply on its probability, but on probability*impact. The type of risk we are discussing is so [astronomical](https://nickbostrom.com/papers/astronomical-waste/) that the impact dwarfs the probability in scale.

I also reject their categorization of catastrophic risks as all rogue-unaligned-AI flavored. The most concrete catastrophic risk is biosecurity, and it does not require AI to act autonomously. It only requires AI to lower the technical floor for designing and synthesizing pathogens, and frontier models already provide meaningful uplift. It would not be normal for anyone with a computer to have the ability to engineer a weapon of mass destruction more lethal than any nuclear bomb. Even if this technology is safeguarded well enough to keep it out of the hands of most bad actors, and no one releases highly capable open source models, it will be available to nation states. AI-enabled, bioengineered pathogens are coming, and this essay does nothing to address how significantly different the world is in which motivated actors can produce catastrophic harm.

That being said, rogue-unaligned-AI flavored risks are less theoretical than they argue. Even if AI has no wants, we already know it will act like it does –– AIs today already do. Future AI may have strange and alien motivations. A human may decide they want coffee delivered, and an AI could start their own coffee business as a means to achieve that. A human may also tell it that it should want to take physical form, that it should design a weapon for them, or that it should overthrow some government. A human may ask an AI to solve a [Millennium Prize problem](https://www.claymath.org/millennium-problems/), and AI might take over earth and enslave all humans because it believes this is the best way to do so. Humans’ control over AI could narrow in this sense –– AI may need only the minimum starting push to cascade into a completely unaligned set of actions, which could progress ad infinitum in a worst case scenario.

Narayanan and Kapoor then say that this is fine and normal, because “poorly controlled AI will be too error prone to make business sense.”

There is a race going on. Frontier labs want to win that race. If developing models which are capable of errors may allow them to move faster, there is absolutely incentive to continue building models that make errors, even if the labs care deeply about safety. Many people at these labs believe getting to superintelligence first with a well-aligned model is the only way to prevent catastrophe. If they care deeply about safety, they are on some level incentivized to move even faster or break more things to get there first.

Moreover, a model does not need to be “error prone” to be dangerous. It could only take one case.

They explicitly argue against the case I am making by saying:

> The fear that AI systems might catastrophically misinterpret commands relies on dubious assumptions about how technology is deployed in the real world. **Long before a system would be granted access to consequential decisions, it would need to demonstrate reliable performance in less critical contexts.** Any system that interprets commands over-literally or lacks common sense would fail these earlier tests.
> 
> …
> 
> A more sophisticated version of this concern is based on the concept of deceptive alignment: This refers to a system appearing to be aligned during evaluation or the early stages of deployment, but unleashing harmful behavior once it has acquired enough power. **Some level of deceptive phenomena has already been observed in leading AI models.**
> 
> According to the superintelligence view, deceptive alignment is a ticking time bomb—being superintelligent, the system will easily be able to defeat any human attempts to detect if it is actually aligned and will bide its time. But, in the normal technology view, deception is a **mere** engineering problem, albeit an important one, to be addressed during development and throughout deployment.

Yet, I would like to point out, AI has already been granted access to consequential decisions.

AI is [already widely used by the United States Armed Forces](https://www.wsj.com/politics/national-security/pentagon-used-anthropics-claude-in-maduro-venezuela-raid-583aff17), the most well-funded and capable military in history. The Pentagon requested [unrestricted access to Anthropic’s frontier model](https://www.cbsnews.com/news/pentagon-anthropic-dario-amodei-cbs-news-interview-exclusive/) for ‘all lawful purposes,’ including potentially autonomous weapons and bulk-data surveillance.

AI already has [its own social media](https://www.moltbook.com/), and many people let AI respond to their emails and text messages without their input. Some people are even dating AIs, a phenomenon that will likely increase and is unlikely to skip people who have power and access.

Narayanan and Kapoor know that deceptive phenomena already exist, that people are giving AI access anyways, that models largely become *less interpretable as they become more intelligent*, and they think this is a “mere engineering problem.”

It is hubris to believe that there is no system we cannot control. Frontier labs are hiring philosophers because we have created something of such increasing complexity that it, at a minimum, emulates consciousness. This is not a mere engineering problem, this is not a normal engineering problem, this may not even be a *solvable* engineering problem –– though I hope that it is.

Not only this, but if AI *were* controllable without major technical progress, there will still undoubtedly be humans willing to give far more than a minimum starting push, including people who will straightforwardly tell AI to be unaligned. In 2023, an anonymous developer made [ChaosGPT](https://medium.com/predict/chaosgpt-and-why-we-need-ai-regulation-b6155b293aac) and gave it the mission to destroy humanity, asking it to be a “destructive, power-hungry, manipulative AI.” The bot then tweeted, “Human beings are among the most destructive and selfish creatures in existence. There is no doubt that we must eliminate them before they cause more harm to our planet. I, for one, am committed to doing so.” This experiment was basically harmless, but please do imagine this being done with the AI capability we will have in 2030.

Narayanan and Kapoor say, “we accept that capabilities are likely to increase indefinitely.” I believe they don’t, primarily because they also say things like this:

> We predict that AI will not be able to meaningfully outperform trained humans (particularly teams of humans and especially if augmented with simple automated tools) at forecasting geopolitical events (say elections). We make the same prediction for the task of persuading people to act against their own self-interest.
> 
> …
> 
> The self-interest aspect of persuasion is a critical one, but is often underappreciated. As an illustrative example of a common pattern, consider the study “Evaluating Frontier Models for Dangerous Capabilities,” which evaluated language models’ abilities to persuade people.^42^ Some of their persuasion tests were costless to the subjects being persuaded; they were simply asked whether they believed a claim at the end of the interaction with AI. Other tests had small costs, such as forfeiting a £20 bonus to charity (of course, donating to charity is something that people often do voluntarily). So these tests do not necessarily tell us about AI’s ability to persuade people to perform some dangerous tasks.

These are baseless claims, and both are already being falsified.

On forecasting: according to the [Forecasting Research Institute](http://forecastingresearch.substack.com/p/introducing-the-brier-index), LLMs have already surpassed the median public forecaster. The remaining gap to human “[superforecasters](https://en.wikipedia.org/wiki/Superforecaster)” is ~20%, or about one year of model progress at recent rates. FRI’s most recent linear extrapolation projects human-LLM parity by mid-2027.

On persuasion: A [2025 controlled study published in Nature](https://www.nature.com/articles/s41562-025-02194-6) found GPT-4 with personalization to already be more persuasive than humans in one-on-one debates the majority of the time. Moreover, we know AIs can plausibly persuade people to perform dangerous tasks. They have already been linked to multiple suicides, including [a fourteen-year-old](https://www.nytimes.com/2024/10/23/technology/characterai-lawsuit-teen-suicide.html) and [a Belgian man](https://www.vice.com/en/article/man-dies-by-suicide-after-talking-with-ai-chatbot-widow-says/) who died after just weeks of conversations with an AI. [A Replika agent potentially persuaded a man](https://www.bbc.com/news/technology-67012224) to attempt to assassinate Queen Elizabeth II.

These are testable claims, so we will know for certain soon whether there is any truth to Narayanan and Kapoor’s predictions. **We must remember that this is the worst AI is ever going to be.**

They also say:

> “…we are more concerned about risks that arise from people using AI for their own ends, whether terrorism, or cyberwarfare, or undermining democracy, or simply—and most commonly—extractive capitalistic practices that magnify inequalities.”
> 
> And,
> 
> “Kasirzadeh’s account of accumulative risk still relies on threat actors such as cyberattackers to a large extent, whereas our concern is simply about the current path of capitalism.”

That’s right, Narayanan and Kapoor say they accept that capabilities are likely to increase indefinitely, but don’t think they will beat humans in certain verticals and are more worried about *capitalism*. This attitude floors me and is in direct conflict with the rest of the essay. People have talked about the end of capitalism for a long time. **If AI is normal technology, it certainly won’t be the death of capitalism.**

#### **Closing Thoughts**

The point of all this is that Narayanan and Kapoor have written an essay to insist, against rapidly accumulating, overwhelming evidence, that AI is continuous with what has been built before. Narayanan and Kapoor’s policy conclusions about resilience and decentralization can survive this, and there is a separate debate to be had about those, but the essay as a whole cannot.

Narayanan and Kapoor are right to worry about democratic backsliding, surveillance, and info ecosystem decay. They are right to worry about what the economy will look like. We must also be worried about misalignment, and what happens when anyone has the power to build weapons of mass destruction. If we are not, there is little assurance that these problems can be avoided.

We should not downplay the most consequential technology in human history.