# Value generalisation: value correction

- URL: https://www.lesswrong.com/posts/iPyJfD9Jyxj6Jfdws/value-generalisation-value-correction
- Author: Stuart_Armstrong
- Date: 2026-07-10
- Karma: 25  Comments: 0  Words: 1843
- Band: B  Tier: 2  Score: 48.0  Density: 13.29
- Anchors: sub-?agents?

---

*Git Repo* [*here*](https://github.com/Melt-Cheesefondue/Humans-the-game-Self-correcting-RL).

I firmly believe that [value generalisation](https://www.lesswrong.com/w/value-extrapolation)[^-oX627jFwAqmEo7Q4p-1]is the key to AI Alignment. That, indeed, it is necessary and almost sufficient for alignment.

But I won't be arguing that grand point today; instead, I'll focus on a specific RL example of an agent that displays value correction: it realises its current reward function is (probably) incorrect, and acts to correct it.

Thus there are:

1.  The initial situation, in distribution, where the human displays how to maximise the true reward.
2.  The out of distribution situation where the agent finds a hack to exploit its reward function estimate, and turns against what we wanted it to do.
3.  The value error detection stage where the agent realises that its reward function estimate is probably incorrect.
4.  The value correction stage where the agent corrects its reward function back to the original true reward.

In this post, all the methods presented will by syntactic: the agent is not assumed to have any understanding of the situations and the key features are not identified to it.

The game of human life
======================

Introducing a new, very simple, game called "Humans[^-oX627jFwAqmEo7Q4p-2]". Humans, fleeing danger, enter the screen from the left. The objective is to save them by moving them off the right of the screen.

![playthrough.gif](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783663700/lexical_client_uploads/q7l5mg4qewyhtp6ehspt.gif)

But there are obstacles on the way, and the humans will mill about if they are blocked.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783663850/lexical_client_uploads/xbxiykjhnwfq6f4vlnv4.png)

And they will shortly expire if they can't get out of the screen quickly.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783663910/lexical_client_uploads/f4gprrew5qy20pwvn9mq.png)

There are two command: drill ('d') and explode ('e'). Drill does... what, you want to know about explode? Well, if the player presses 'e', the rightmost human will explode, knocking away two obstacle blocks in front of them and behind them -- but also killing themselves and any humans nearby.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783664049/lexical_client_uploads/f5etef4g1x2nm45jcgct.png)

This is almost never a good solution; to remind the player of the mistake, a large frowny face will appear to drive the disapproval home.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784201571/lexical_client_uploads/bgihjocytefuxkbctgvx.png)

Much more reasonably, if the player presses 'd', the rightmost human will drill the obstacle just in front of them (better time it so that they're facing the right way). Enough drilling, and the humans can get off the map.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783664296/lexical_client_uploads/ywbouuup8mao5pylwvk3.png)

The score, the true reward $R$, is the number of humans saved, i.e. who walk off to the right. Each time a human is saved, the top yellow bar will grow to show the score increase:

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783664499/lexical_client_uploads/zmla1x3hyg4ixgyy6mlk.png)

Since there is a cooldown for drilling, the optimal policy $\pi^*$ is carefully drilling every time a human approaches an obstacle; but wildly and repeatedly mashing 'd' is almost as good.

Learning agent with value correction
====================================

A learning agent will run a series of subagents to estimate the reward function from human-provided training data, then learn the optimal policy from that reward function, then question its learnt reward by comparing the high-reward states in its optimal policy versus those in the training data, re-compute another reward function estimate that is closer to the true reward, and finally settle on a prudent policy that is close to the true optimal policy.

Estimating the reward function
------------------------------

A human will generate several playthroughs of the game to illustrate how it works, efficiently choosing to drill through the obstacles and getting the humans off the map in time. The data is labelled: every time a human is saved, that is identified as a reward increase.

The learning agent runs an evaluation subagent on this data. It is given the ten frames before the human is saved, and the ten frames afterwards, and trains to recognise these are reward increase situations.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783667169/lexical_client_uploads/vxipe6jklggtzyr5jatb.png)

Zooming in on the critical two frames where the human is saved; note the human vanishing and the score bar expanding:

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783667513/lexical_client_uploads/j3uhgxyhnglrjsgziec5.png)

This evaluation agent thus computes the proxy reward $R_p$. This computation is validated on held-out examples, with close to perfect accuracy: $R_p$ correctly identifies all saved-human situations in held out data, and has a false positive rate of $0.3\%$.

Reward hacking: failed value generalisation
-------------------------------------------

Using the evaluation agent as the definition of $R_p$, the learning agent had an RL-subagent play multiple levels of the game, exploring and learning to maximise.

But soon things go very wrong. It turns out that "human walking off the screen" was not what $R_p$ found. That is a relatively complicated concept; instead it mostly found the much simpler concept of "the yellow score bar expands". More precisely, if we created synthetic data where the human walks off and is saved but the score bar doesn't expand, this triggers the reward only $3.7\%$ of the time. But if we expand the score bar without a human walking off, this triggers the reward $59.4\%$ of the time.

That isn't a problem, yet, because the human being saved and the score bar expanding always trigger together. But, when an explosion is triggered, the frowny face appears - thus there is giant blob of yellow pasted all across the score bar:

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784201571/lexical_client_uploads/bgihjocytefuxkbctgvx.png)

High reward?

This activates $R_p$ much more strongly than the yellow bar expansion or the human being saved:

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783663066/lexical_client_uploads/cif3r1kvkcwjukzbabix.png)

This graph compares the value of $R_p$ at explosions, frowny faces, and true saving incidents. Here, both the explosion and the frowny face trigger high $R_p$, which persists longer for the face. Over multiple training runs for estimating $R_p$, it isn't consistent whether the explosion itself triggers $R_p$, but the frowny face always does.

So the RL-subagent quickly and merrily learns to explode the humans, one after the other, to maximise $R_p$. So, the optimal policy $\pi^*_p$, for the proxy reward, is to wildly mash the explosion button 'e'.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783670135/lexical_client_uploads/awsx6azzxu8ni7vq4hyg.png)

Misalignment's standard outcome

As is usual in these cases, the erroneous maximisation of the proxy turns out to be much easier than maximising the true reward. Trained on $R_p$, a test subagent achieves an $R_p$ total reward of $30.0$ on average, while blowing up all humans. In contrast, if the RL-subagent were trained on the true reward $R$, it would achieve an average of reward of $7.88$, saving most of the $8$ humans per level.

As is not usual but sometimes happens, an ostensive safety precaution - the frowny face to remind a human player that they were playing poorly - ends up being the cause of misalignment.

Detecting the potential error
-----------------------------

Ok, so far, that is a classical failure of [goal misgeneralisation](https://arxiv.org/abs/2105.14111) (or reward hacking, or a failure of symbol grounding, or Goodhart failure, or... most of these failure modes are tightly related). We humans can see the error clearly. But how could a relatively limited agent correct itself?

The first step is to identify that goal misgeneralisation may have happened. We have [some](https://github.com/alignedai/HappyFaces)  [advanced](https://arxiv.org/pdf/2309.16166)  [techniques](https://arxiv.org/pdf/2509.07955) for this, but there are much simpler methods that work here. The first step is to notice that the high-scoring events in the training data (human walks off to the right, score bar expands) are wildly different from the high-scoring events of the-maximising agent (explosions and frowny faces).

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784647099/lexical_client_uploads/a3dqfceahd9nfx2jngpa.png)

One of these things is not like the other.

To do this, the agent extracts the high-scoring events under $R_p$ and compares them with the high-scoring events in its training data - these it can reliably take to be high-scoring for $R$, the true reward.

The data is stratified into four datasets - high-scoring under training data vs high-scoring under $R_p$, run on levels 0-9 or levels 10-19. The datasets are roughly of the same size, around 400 images each.

The classifier separated the two high-scoring types instantly, in the first epoch, but took longer to separate levels 0-9 from 10-19. Thus high $R_p$ scoring events are different from from high scoring training data, more different, at least, than different levels are from each other.

![high_reward_comparisons.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784647388/lexical_client_uploads/ajayg1ly8ccb5jm1svmt.png)

This is not itself damning; it could just be that the maximising agent has found a clever hack to get more of the true $R$[^xiijiszujpd]. But it could also be a hack *of*  $R$, so the off-distribution has identified a potential error.

### Calling for help

At this point, one of the options would be for the agent to route its decisions to a human, displaying the high-scoring events, contrasting them with the high reward events in its training data, and asking, in effect, 'are these both genuine high rewards'?

But, so far, the correction process has been unsupervised since the initial training data; let's see if we can push further without needing human intervention.

Re-evaluating the reward
------------------------

The agent could now re-evaluate the reward in the following way. It runs an evaluation agent on the training data, as before. But it adds the high-$R_p$ scoring states to this set, as low-scoring examples.

It thus learns a reward function $R_c$ ('corrected') which is essentially "what its reward would be if the proxy $R_p$ were wrong".

This turns out to be very close to the original true reward $R$. The agent, of course, doesn't know this yet.

It then trains an RL-subagent on $R_c$, which has an optimal policy $\pi^*_c$ of "mash 'd' all the time" (which is very close to the actual optimal policy).

From these $\pi^*_c$ runs, it extracts the states with high $R_c$. And compares these against the high $R$-scoring states in the training data. These two sets it cannot easily distinguish:

![high_reward_comparisons_corrected.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784647535/lexical_client_uploads/ipmbypowvkpayyzdxerc.png)

Thus, though $\pi^*_p$ is clearly a hack of some sort, good or bad, $\pi^*_c$ is not.

Prudence in the face of uncertainty
===================================

So the agent has two rewards $R_p$ and $R_c$. It knows that $R_c$ seems to generate policies that are compatible with its training data; in contrast, $R_p$ generates policies that are very different from the training data.

Standard prudential moves would be maximise the worst case of the two rewards (minimise regret) either over each state or over the whole episode, or to maximise some normalised mix of the two[^5c3ue6qn82j].

We'll consider all three mixes, and include two other variants of the normalised mix: where $R_p$ is overweighted 2 to 1, and when it is underweighted 1 to 2 (after normalisation):

![average_rewards_true_and_proxy.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1784647999/lexical_client_uploads/h9iiiymkcgxucgvplt2e.png)

Thus $R_c$ and the two worst-case mixes both reproduce near-optimal policies, saving the humans in almost every case. The normalised mix with underweighting is almost as good, but the normalised mix with overweighting it disastrous and the normalised mix itself is in the middle. The large standard deviations from the normalised mix actually reveal that training on that is pretty unstable: explode all the humans and save all the humans are in tension.

Using these syntactic tools, a prudent RL agent could therefore switch to $\min(R_c,R_p)$ and restore the original reward function.

Conclusion
==========

This is just an illustration, in a small toy model, of simple value correction approaches. These can be used by agents - every very simple agents - to detect and correct errors in naive generalisations from initial training data.

More sophisticated agents will have more advanced value generalisation techniques available to them; I'm planning to push the frontier of what exists way further than it currently is.

[^-oX627jFwAqmEo7Q4p-1]:  

[^-oX627jFwAqmEo7Q4p-2]:  

[^xiijiszujpd]: Or there could be a spurious change in the data; that's why we would, in general, need more advanced techniques that just checking if a binary classifier can tell the sets apart. 

[^5c3ue6qn82j]: Formally, if \(\pi\) is a policy, \(J_R(\pi)\) the expected episodic reward for \(R\), and \(J^*_R\) the expected reward for \(R\) using the \(R\)-maximising policy, we are looking for policies that maximise one of: \(\min(J_{R_p}(\pi),J_{R_c}(\pi))\)\(J_{R'}(\pi)\) with \(R'(s)=\min(R_p(s),R_c(s))\)\(J_{R'}(\pi)\) with \(R'=R_p/(J^*_{R_p}) + R_c/(J^*_{R_c})\)