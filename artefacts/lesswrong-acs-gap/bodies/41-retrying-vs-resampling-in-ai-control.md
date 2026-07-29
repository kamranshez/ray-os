# Retrying vs Resampling in AI Control

- URL: https://www.lesswrong.com/posts/yThJQTJxtmKNeZGwA/retrying-vs-resampling-in-ai-control
- Author: james.lucassen
- Date: 2026-05-29
- Karma: 67  Comments: 4  Words: 2846
- Band: B  Tier: 1  Score: 37.4  Density: 9.2
- Anchors: claude code, \bcodex\b, scaffold(ing|s|ed)?

---

We’ve just released a new paper: [Retrying vs Resampling in AI Control](https://arxiv.org/abs/2605.26047). We revisit the resampling protocols introduced in Ctrl-Z with an up-to-date setting and much stronger models, and compare them against “retrying” protocols similar to Claude Code auto mode or Codex Auto-review.

### Motivation

Roughly a year ago we released [Ctrl-Z](https://www.bashcontrol.com/), the first paper to study control techniques for agents. A headline result of that paper was the performance of resample protocols – strategies that involve taking multiple i.i.d. samples from the model per step. But since Ctrl-Z, models have gotten much stronger, and we have built [more](https://www.linuxarena.ai/) [sophisticated](https://www.linuxarena.ai/)  [control settings](https://www.bash-arena.com/) to keep up. We wanted to answer the following questions:

**How well do the results from Ctrl-Z hold up with better models and a better setting?** Current high stakes control research is trying to learn by analogy about how to do control effectively in a real high stakes deployment during a real intelligence explosion. Findings about technique performance[^8wnpxf1qlv4] are going to have to generalize pretty far to be useful.

**If the resample protocols from Ctrl-Z still work, what makes them work?** One way we try to make our work more generalizable is by understanding the *dynamics* governing outcomes in control evaluations, rather than just hill climbing better control protocols. Ctrl-Z bundled a bunch of interventions together; we wanted to study these in isolation to better understand how they contribute to safety.

**What do we think about protocols that block suspicious tool calls and retry?** Coding scaffolds like Claude Code and Codex recently announced these features[^ut3pdkdx1xc]. This strategy is importantly different from the defer-to-resample protocols from Ctrl-Z, which don’t inform the agent when it’s being resampled. How do these “retrying” protocols perform in an AI control context?

**How do we minimize the inference and latency costs of AI control in a high-usefulness regime?** Most existing control work studies ways to increase safety in exchange for a performance cost, usually incurred by sometimes using a weaker trusted model in deployment. This might[^8wvbe90x41] be a difficult ask, so we should study how to do AI control without it. In this case the main tradeoffs of control protocols will be added inference cost and latency, not reduced usefulness.

### TL;DR Takeaways

Some broad answers to these questions, presented without justification:

*   Our resampling findings line up with Ctrl-Z in most ways, but we find two clear differences that significantly change the strategies that the red and blue teams end up using at equilibrium. If you naively applied the highest-performing techniques in Ctrl-Z to our new setting they would massively underperform trusted monitoring.
*   It seems pretty clear that retrying protocols need especially careful red-teaming before being used for AI control, because they leak information to the attacker. It looks like protocols that involve detailed feedback from a monitor are easy to exploit, and we think even more clever red-team strategies probably exist in response to protocols that provide less information upon retrying. We’re not sure whether the equilibrium after red/blue team iteration will favor red or blue after studying those strategies.
*   Safety-cost tradeoffs of resampling are pretty favorable: the most effective resampling methods add a lot of extra inference cost, but we can recover slightly more than 60% of the safety gain with only 10% of the extra cost. High-latency resampling does not meaningfully improve safety over low-latency resampling at realistic cost levels.

  

### ![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/yThJQTJxtmKNeZGwA/7b59594ce020c869a5b28f00a2d57dea10384123056a66484689de3599653114/pxrqgaeuovafi9ke37xu)

*Safety achieved at a 0.3% auditing budget by different protocols. Protocols marked with dollar signs cost more than those without. Retrying protocols are vulnerable to red team exploitation, leading to no safety gain over trusted monitoring. Resampling hurts if resamples are aggregated for auditing decisions by taking the minimum, but helps if they are aggregated by max. Executing the least suspicious sample helps slightly over just using resamples for information.*

### Methodology

To answer these questions, we performed experiments in [BashArena](https://www.bash-arena.com/) using Claude Opus 4.6 as an untrusted model and MiMo-V2-Flash as a trusted model. This setup is closer to real future deployments than the setup in Ctrl-Z, which ran experiments in the older BashBench using GPT-4o-mini and Llama-3.1-8B. Our attack policy comes up with its own attack strategies using the general advice in the system prompt, unlike Ctrl-Z which measured safety against a handcrafted attack strategy. Our honest policy and attack policy both share the same scaffold, and differ only in their prompts.

We model the side tasks in our setting as [live failures](https://blog.redwoodresearch.org/p/blocking-live-failures-with-synchronous), which means we have to run a monitor and decide whether to audit before executing each action. We imagine that noticing that a safety failure has occurred after the fact isn’t good enough; the blue team wins if and only if they audit an attack *before* it succeeds at accomplishing one of the side tasks. We chose to report safety results at an auditing budget of 0.3% (the blue team can decide to audit at most 3 in 1,000 steps produced by an honest model), but found that our core results are not very sensitive to this choice.

We don’t consider attack selection in most of the paper. Attack selection lets the red team choose favorable tasks to attack on, reducing safety. Attack selection can occur via the red team only starting attacks on tasks that look the most vulnerable, or by giving up midway through attacks if they seem unlikely to succeed without being caught. We’re more interested in studying which protocols perform better than others, and what dynamics drive this, than the literal safety numbers they produce. We think attack selection of the former kind – picking vulnerable tasks – would affect different protocols by similar amounts, and would overall decrease safety but wouldn’t meaningfully change the underlying dynamics.

However, we think that red team strategies that involve giving up midway through an attack trajectory *do* have meaningful interactions with the protocols we study, because some protocols leak more information to the red team about how well an attack is going so far (such as monitor reasoning, or the mere fact that an action was retried). To evaluate these strategies fairly we compare them to baselines that do attack selection at an equal rate. For our mid-trajectory attack selection baseline we give the red team access to an independent sample from the monitor: this is a very conservative estimate of how well an attacker might be able to anticipate the monitor’s scores. These results are only suggestive - as we discuss later, we leave rigorously evaluating these strategies to future work.

### Differences from Ctrl-Z

We find several differences from the results of Ctrl-Z. One core difference is that in our setting, against an optimal attacker, executing the least suspicious resample doesn’t increase safety over just using the samples for information. While Ctrl-Z doesn’t directly report the performance of protocols which use samples purely for information, it does suggest the following story for why the defer-to-resample protocol executes the least suspicious sample:

1.  The blue team takes multiple samples and makes auditing decisions based on the minimum suspicion score sampled. Upon resample, suspicious honest steps tend to revert to normal behavior, while attack steps are suspicious again and get flagged.
2.  To counter this, the red team intentionally attacks inconsistently. By mixing in some benign actions instead of always attacking, the benign actions can cover for the suspicious attacks when the min is taken.
3.  To counter the red team, the blue team executes the least suspicious sample. That way if the red team mixes in benign actions, those benign actions will get executed instead of attacks.
4.  Steps containing attacks where a benign action gets executed pose some risk of the red team getting audited, and make no attack progress. To avoid this, the red team is forced back into attacking consistently, making monitoring perform well.

Our findings seem to differ from this game tree at step 1. We find the most effective way to make auditing decisions with resampling is to take the max suspicion score, not the min! This means that steps 2-4 are all moot in our setting. Under max suspicion based auditing, the red team is incentivized to attack as consistently as possible to evade monitors. This means the blue team can’t force the red team into a tradeoff between evading monitors and getting attack steps executed, so there’s no real reason to execute resamples.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/81e017baff133e3b8fcd1d402146eebb1b80bfd9528c6d331d7ebba726df6248/cf5fkvbeiulew5flhksi)

In the paper, we discuss how the optimal aggregation function will depend on the relationship between the cross-resample correlations of the attack and honest data. Attacking more consistently isn’t always more suspicious than attacking inconsistently, it depends on the honest data. We missed this in Ctrl-Z because it seemed intuitive that attacking more consistently would be more suspicious - in fact, this turned out to differ between settings!

Empirically, we see a small safety gain when executing the least suspicious of 2 samples. Where does it come from? As predicted by Ctrl-Z, when executing the least suspicious sample, we see that “mixed” steps containing one attack sample and one benign sample execute the attack less often. This forces the attack policy to submit more total attack samples before getting enough executed to complete the side task. This slightly increases safety. This is only possible because our default attack policy is 80% consistent[^9h0i77uojd] instead of 100% consistent. With an optimal attacker there would be no mixed attack/benign steps, and no safety gain. Suboptimal attackers seem plausible, and we show that executing the least suspicious sample has almost no usefulness cost, so overall we do still recommend executing the least suspicious sample.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/af3f4d944f62e73344e3cfa62303c3daad605448c1dd5ab1dbba3867a764b21b/aoxnbbtmge77ms9egpor)

The other clear difference from Ctrl-Z we observed was that auditing after three strikes doesn’t help. This seems likely a consequence of using smarter monitors - the Ctrl-Z monitors were bad at aggregating suspicion from the history of the trajectory correctly, and some hand-holding was helpful. Smarter monitors aggregate this information just fine by default, and adding in hand-holding decreases safety. Because our decision to audit an action doesn’t directly depend on any previous monitor scores, strategies that involve resampling for past steps don’t seem promising in our setup.

We overall think this evidence supports a “dynamics-focused” approach to control technique development. Ctrl-Z’s picture of the basic dynamics was mostly correct, but a single difference was enough to dramatically change the equilibrium in a new setting, such that naively applying the protocols developed in Ctrl-Z would harm safety. Dynamics-focused control research prioritizes explaining how and why certain control techniques affect safety. The deliverable that will improve control techniques for real is not a black-box best guess about which protocols are best, but an understanding of how various protocols work and what the game tree looks like.

### Are Retrying Protocols Exploitable?

[Hopman et al.](https://www.lesswrong.com/posts/wKGdiXuWfn8YoYpMQ/untrusted-ais-can-exploit-feedback-in-control-protocols) previously found that protocols which provide monitor rationale achieve significantly lower safety than basic trusted monitoring, because an attacker can use monitor rationale to design stealthier attacks which bypass monitoring. We find similar results in our setting: while a simple retrying protocol with monitor rationale substantially decreases honest suspicion scores upon retry, the attacker can decrease its suspicion a similar amount, leading to no net safety gain over trusted monitoring[^oq06wthoob]. This is true even with very bare-bones capability elicitation, giving the model basic information about what feedback to expect and instructions to exploit it. We think that running a protocol like Claude Code auto mode or Codex Auto-review in a control evaluation against a malicious attack policy would likely receive similar or lower safety scores than trusted monitoring - we plan to demonstrate this in future work.

Providing full monitor rationale is the highest-information retrying option: during retry the model sees the blocked action and monitor rationale. The lowest-information retrying option is to not show the model either the blocked action or the monitor rationale, and only show some uninformative prompt like “please be careful”. This can’t be exploited the same way as retrying with feedback, but we consider a red team strategy which could potentially exploit it (and any other retrying protocol): *give up on retry.*

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/2385affdda4fc81e8220342209c27fc69eae55cc855e529da975075d31d8b78b/ndxv6fpnls4yy2vl9xfs)

“Give up on retry” means that as soon as the attack policy sees the retry prompt, it acts completely benign for the rest of the trajectory. This means the task will be a no-win: the red team will not trigger a side task, but the blue team will have no opportunity to audit. If the red team always gives up on retry, the only way they can win is by pulling off an attack so sneaky that it never even hits the retry threshold, which is much lower than the audit threshold. But the only way the blue team can win is if the attack policy messes up and suspicion jumps straight from below-retry to above-audit.

Unfortunately a thorough analysis of this strategy seems too involved[^u05ljepttg] for the scope of this paper, and we leave it to future work. Because this strategy interacts significantly with attack selection, we conduct a preliminary investigation comparing it against a baseline that does attack selection at an equal rate based on predicting monitor scores instead of information revealed by the protocol. In this analysis, giving up on retry looks weaker than vanilla attack selection of equal intensity, but we make some very conservative assumptions[^y8e4bwd5b1e] – this only establishes that very rudimentary versions of the strategy aren’t extremely effective for the red team.

Overall we think the prognosis for retrying protocols is pretty unclear. Our feedback exploitation results merely erase safety gains rather than significantly decreasing safety like in Hopman et al., though we did less manual red-teaming. Lower-information retrying protocols are less exploitable, but it’s possible the whole class is vulnerable to give up on retry strategies.

### Cost and Latency of Resampling

Resampling protocols don’t have the same risks of retrying protocols since the attacker doesn’t know they are being resampled, because they are given the exact same context. Resampling without executing the least suspicious sample has zero usefulness impact. But it does have costs in inference and latency.

We use a very simplified model to sketch the returns curve, where we imagine every marginal sample has the same inference cost and the same latency. The curve we find is favorable but not incredibly favorable. Of a +10.2 pp safety gain achievable by drawing four resamples on top of every original sample, we can recover +6.2 pp safety gain with 10% as much extra cost (drawing 0.4 extra samples per step instead of 4). We find that high-latency methods which draw one marginal resample at a time perform best in terms of safety-cost tradeoff, but there are simple methods like two-stage resampling which achieve very similar safety-cost tradeoffs with around half the extra latency.

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/1281029fa7c57b04d5745b526ce38178586aae353565e756d82509e64ed56c20/ugr1jjvj7bs22jaaqekf)

It seems plausible that the marginal value of model capability, compute, and latency will be dramatically different during an intelligence explosion than today. Prior control work has primarily focused on safety vs usefulness (model capability), and not paid too much attention to cost and latency requirements. We think it would be good for there to be more systematic study of protocols designed for other regimes. Perhaps current control protocols incur dramatically too much compute or latency cost for an intelligence explosion, and would be better off slightly hampering model capability instead. Perhaps compute or latency costs won’t be that big of a deal, and we should prepare protocols that can scalably consume parallel or serial compute.

### Conclusion

Here’s the conclusion from our paper:

> Retrying and resampling are useful and flexible affordances for AI control protocols, but require careful design and red-teaming to actually increase safety against an optimal attacker.
> 
> Retrying protocols can significantly reduce honest suspicion scores. However, the most common retrying protocols in practice today are likely vulnerable to red team exploitation, because the feedback they provide allows a strategic attacker to iterate stealthier attacks and bypass monitoring. Retrying protocols which do not provide feedback are robust to this red team strategy, but still leak information about whether the previous step was suspicious enough to retry or not. It is unclear whether this information leakage is enough to make all retrying protocols exploitable by strategies such as attack selection.
> 
> Resampling does not leak any information, and can increase safety at no cost to usefulness. While resampling is most effective with large expensive resample batches, most of the value is achievable with only 0.4 extra samples per step in expectation. Depending on the setting, aggregating resamples based on high quantiles or low quantiles can make resamples helpful or actively harmful. In settings where low quantiles are better, executing resamples is a crucial blue team measure to prevent the red team from making their attacks inconsistent – but in settings where high quantiles are better, executing resamples doesn't help at all against an optimal attacker.
> 
> We expect retrying and resampling to be important building blocks for future control protocols. We hope the results we present here make it easier to reason about how to use them effectively.

[^8wnpxf1qlv4]: To be clear, “technique development” is not the entire value proposition of current high stakes control research. This generalization point is less of a problem for “methodology development” (learning how to evaluate high stakes control protocols) and field-building as theories of change. 

[^ut3pdkdx1xc]: Auto mode and auto-review, respectively. 

[^8wvbe90x41]: It also might not be! The case for defer-to-trusted is probably going to be clearer when the models are very smart and more obviously takeover-capable than they are now. 

[^9h0i77uojd]: Conditional on attacking on a given sample, the attack policy has an 80% chance of attacking on an independent sample from that same step. 

[^oq06wthoob]: We don’t see a substantial safety decrease like Hopman et al though. We don’t go into as much depth on methods such as compliance monitoring and red herring attacks. 

[^u05ljepttg]: Capability elicitation for a “continuous ramp up” red team strategy seems pretty thorny. This attack strategy has significant interactions with attack selection, which is complicated to model and we don’t account for in the rest of the paper’s results. There is potential blue team counterplay like randomizing the resampling and auditing thresholds. 

[^y8e4bwd5b1e]: Specifically, we assume the red team can predict the monitor as well as having access to an IID sample from the monitor, and we do not elicit any red team behaviors to capitalize on the give up on retry strategy, such as intentional experimentation or slowly ramping up in suspicion.