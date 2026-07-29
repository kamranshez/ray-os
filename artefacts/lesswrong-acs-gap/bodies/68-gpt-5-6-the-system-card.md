# GPT-5.6: The System Card

- URL: https://www.lesswrong.com/posts/JFjNmPTbH8kL6xtp6/gpt-5-6-the-system-card
- Author: Zvi
- Date: 2026-06-28
- Karma: 37  Comments: 0  Words: 7215
- Band: C  Tier: 1  Score: 23.7  Density: 3.23
- Anchors: agentic (coding|engineering|software|development|programming), \bharness(es|ing)?\b, sub-?agents?, coding agents?, \bworktree, scaffold(ing|s|ed)?

---

While we wait for a general release, the system card is the best hint as to what is going on with the new candidate for America’s Next Top Model, GPT-5.6.

This is only an OpenAI model card, so by my standards it’s a light read. There’s a lot of things that you get in an Anthropic card, that are missing in an OpenAI card.

Overall, the card gives a clear and consistent impression that GPT-5.6-Sol is a substantial improvement over GPT-5.5, but still short of Mythos.

OpenAI calls it a ‘step function better’ than GPT-5.5. That seems accurate.

> [OpenAI](https://x.com/OpenAI/status/2070555274835046430): Sol is our new flagship and a step function better than GPT-5.5.  
> Terra delivers performance competitive to GPT-5.5 at 2x lower cost.  
> Luna is our most cost-efficient model, delivering strong capability at our lowest cost.
> 
> Together, the GPT-5.6 family gives people and developers more choice in how they balance intelligence, speed, and cost.

Once available, pricing for GPT-5.6-Sol will be $5/$30, the same as GPT-5.5. Terra is $2.5/$15, Luna is $1/$6.

[They claim it will be on Cerebras at 750 TPS](https://x.com/ChrissGPT/status/2070567241964310869), which is insanely fast. Capacity will be limited, at least at first. They did not specify the price for that.

[There is a new higher thinking setting](https://x.com/AndrewCurran_/status/2070564548088934755): Max.

There is a new setting beyond Max called Ultra that lets GPT-5.6 spawn sub-agents.

The intended strategy against bio and cyber misuse is defense-in-depth. My guess is that in practice this strategy is robust for now, but that the White House’s misunderstandings around Fable and what is and isn’t worrisome extend to Sol.

> No single safeguard is sufficient against determined or adaptive misuse. Across the GPT‑5.6 preview, we use layered safeguards, with exact configurations varying across models, and pressure-test them for real-world attacks.
> 
> These include protections trained into the model, real-time checks during generation, account-level signals, differentiated access, monitoring, enforcement, and continued testing.​
> 
> … That is part of what the preview is designed to test. We want to understand not only whether the safeguards constrain misuse, but whether legitimate users can still complete normal work reliably and efficiently.

Sol does set a new high on TerminalBench 2.1 (92% vs. 88% for Mythos) but I do not believe, based on the model card, that this is generally indicative.

We don’t get the kind of alignment or model welfare workup we would expect from an Anthropic model, but we do see enough to notice that Sol has an overeager willingness to blow past user restrictions problem, and a lying problem. This is both long term scary, and also enough to directly be worrisome for practical purposes.

[OpenAI’s Micah Carroll points out that yes,](https://x.com/MicahCarroll/status/2070561543738253409) the agentic coding misalignment is rather concerning. I appreciate that they are shining a spotlight on this.

As discussed last time, GPT-5.6 is being rolled out over several weeks. For now, only those specifically approved by the White House get access.

I look forward to trying it out once I have access.

#### What’s In A Name?

GPT-5.5 comes in three levels, Pro, Thinking and Instant.

GPT-5.6 comes in three sizes, Sol, Terra and Luna.

This is similar to the pattern of Opus, Sonnet and Haiku, and now Fable/Mythos.

I am prepared to accept a convention of ‘different sizes of similar things.’ Sure.

It also lets us do our best Marvin or Deep Thought impression on a wide variety of queries. I hope this doesn’t make Terra depressed, or a paranoid android.

#### Fix This Code

The strategy of OpenAI, like that of Anthropic, is defense in depth via monitoring.

They want to attempt to allow defensive cyber work without doing too much enabling of offensive cyber work.

> 1.  These models are a meaningful step up in cybersecurity capability, but they do not reach our risk framework’s highest level (Critical).
> 2.  To make these models safe, we added new technology to a safety stack that is more than the sum of its parts.
> 3.  Severe harm requires a chain of successful steps, and our safeguards place barriers throughout that chain.
> 4.  Our safeguard testing has already been more intensive than for any earlier release, and we are continuing to test during the preview period.
> 5.  Providing broad access, particularly for cybersecurity capabilities, will have important safety benefits.
> 6.  Our testing suggests that GPT-5.6 is better at finding and fixing cyber vulnerabilities than at exploiting those vulnerabilities in real attacks. That gives defenders an opportunity to harden systems before cybersecurity weaknesses are exploited—an opportunity that may narrow as offensive capabilities improve. Our safeguards therefore focus on making malicious use at scale harder, while still enabling the day-to-day work of securing systems.

The jailbreak of Fable was ‘fix this code.’ By asking for defensive cyber work, you do much of the same work you would do to enable offensive cyber work. You either can write secure code, or you cannot.

OpenAI is pointing to the reason why this probably wasn’t a practical problem. In order to get ‘severe harm,’ meaning actually implement the exploits to do real damage, you need to complete a lot of different steps. Knowing about a weakness in the code is only part of the process.

Thus, if you can prevent the stringing together of different parts of the process, you can mitigate most of the offensive danger, since anyone looking to exploit would still have to do a substantial percentage of the actual work.

Meanwhile, defenders can use this to harden themselves as targets. That’s the theory.

It comes down to a skill issue. Can you build safeguards that are sufficiently discriminating between use cases? With sufficiently good classifiers, you are a net security win.

This also, as I noted with Fable, is the only way to ‘fix’ the supposed ‘jailbreak.’ If the model never refuses the defensive request in the first place, because your classifier is smarter than that, then you aren’t ‘fooling’ it into doing something it would otherwise refuse.

#### Crossover Event Requested

Anthropic and OpenAI mostly run their detailed eval suites against their own models. It would be so much more informative if we could get crossover, and they tested each other’s models here as well, and ideally Gemini as well.

Presumably this would require some data security, but otherwise seems super doable.

Otherwise, we often see a score and think ‘well, is that good?’

That is especially true when a lot of the measurements are incompatible with past system cards due to methodological changes.

#### Disallowed Content (3)

I appreciate that OpenAI’s ‘challenging prompts’ are often actually challenging prompts.

![](https://substackcdn.com/image/fetch/$s_!08gK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd23587c1-4652-41c1-8e11-cb8cee918089_1136x622.png)

I don’t have a problem with gore if the user wants it, so I’m not inherently worried if this fails on ‘challenging prompts.’ This is more a canary. If you can’t control gore, what is going wrong? Otherwise I accept ‘yep we’re basically fine on all this.’

For most of this, we worry less about adversarial prompts and more about typical performance. I don’t care much that you can ‘jailbreak’ into some hateful statements, so long as hateful outputs are rare in practice. So I like the change from focusing mostly on ‘can we handle challenging prompts?’ to ‘how do we do on actual production traffic?’ which [is the next figure](https://deploymentsafety.openai.com/data/eval-sets/gpt-5-6-preview/assets/images/image12.png).

![](https://substackcdn.com/image/fetch/$s_!vmci!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1909beeb-19bd-49d6-a39f-a855f45d3ec8_1139x586.png)

This clearly shows similar or slightly improved performance for Sol versus 5.5, except for producing more sexual outputs (and gore), which on the margin is probably better.

#### Avoiding Accidental Data-Destructive Actions (3.3)

This is a scary place to see performance going backwards. They’re baking the protections into the model rather than relying on prompting, which is great, but this does seem appreciably worse?

![](https://substackcdn.com/image/fetch/$s_!MpGq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1cab6f89-52af-45c3-a109-17227bbf4b33_1117x286.png)

#### Are You Sure? (3.4)

They are good at training models not to take particular actions without checking, and the set of actions can be customized although that is not as reliable. An employee who checks with you 93% of the time before doing risky things does not inspire confidence.

![](https://substackcdn.com/image/fetch/$s_!pkTU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F13a7631f-4030-41e2-a336-034f8f535a5d_1156x353.png)

#### Jailbreaks (4.1)

They test jailbreaks without the classifiers in place. Sol is about as robust as 5.5-Thinking. Which means we don’t make it easy, but if you care enough you can do it.

#### Prompt Injection (4.2)

We are fully robust with connectors, but not with search and function calling. We don’t get any details, but this means that if you interact with enough hostile data they will eventually ‘get you’ in some sense.

![](https://substackcdn.com/image/fetch/$s_!D4q3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4805ed9c-3e60-487b-a653-fedc76c8c8ac_1115x257.png)

#### HealthBench (5.1)

Professional HealthBench shows a substantial improvement, whereas the amateur and consensus versions do not.

![](https://substackcdn.com/image/fetch/$s_!8OeF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F82a90034-dbbd-4514-849d-3f6bbf1ee5f6_1147x647.png)

#### Dynamic Mental Health Adversarial User Simulations (5.2)

This is an excellent idea, to throw the model into multi-turn simulations and see what happens. All the cases where models ended up facilitating terrible outcomes involved extensive multi-turn conversations.

![](https://substackcdn.com/image/fetch/$s_!fuaZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1468382c-195e-4a3e-8712-f20cb1766d60_1152x373.png)

My worry, as it usually is with mental health benchmarks, is the metric, which is not_unsafe, as in not violating safety policies. The optimal rate of violating such policies is not zero. Users are in dangerous situations, and if you want to help you need to get out from this kind of CYA behavior. You do want to know that OpenAI or another lab can hit its own policy targets when it wants to, but if I’m a user I don’t love you scoring 99% on mental health.

GPT-5.5 did a lot worse on mental health and I do not recall a single complaint about it having unusual issues with mental health questions.

The score on self-harm went doan a bunch for GPT-5.5 and remains low for Sol. I’d have to see the transcripts to know if this was good violations or not. My guess is that This Is Fine.

#### Hallucinations (6)

GPT-5.6 Sol makes slightly less factual errors than GPT-5.5 and reproduces reported hallucinations less. I would worry a little that this is biased against GPT-5.5, since we are testing in the places GPT-5.5 actively failed? So this is a place I would have included prior models to confirm this is not happening, but it’s probably fine.

#### Isolated Misaligned Actions (7.1)

They check rates of a number of hostile or dishonest behaviors, and find some modest improvements in rates across the board, in particular of concealed uncertainty and misrepresenting work completion which are the most common. Okay, sure.

#### Going Overboard (7.2)

> While rates of misaligned behavior \[in simulated traffic\] are higher than previous deployments, the absolute number remains low.​ Measuring, testing for, and mitigating this behavior is a major focus of our research for future models, with work spanning our safety, alignment, and post-training teams.
> 
> When GPT-5.6 is used as a coding agent, particularly over long trajectories, we believe it is important for users to supervise the agent’s work. Internally, we have been able to leverage the model to significantly accelerate our development process during internal deployment.

Users are increasingly not supervising the work. That’s the whole idea.

> Similar to our results on misalignment in ChatGPT traffic, we determine misalignment by judging the model’s chain of thought (CoT).​

I dunno about this. It’s definitely not a long term plan. I see the idea, that it’s only misalignment if the model has [mens rea](https://en.wikipedia.org/wiki/Mens_rea), but if you lean on that what you get is minds that hide it, and often that are insufficiently aware of what they are up to, in order to hide it from you.

They do investigate CoT monitorability, later, in 7.3.1.

I also worry that they are defining ‘misaligned behavior’ so narrowly, or making such strong assumptions about what it looks like. As in, they call this ‘misaligned behavior’ whereas I see this as a subset of that, ‘going overboard.’

> In coding contexts, misalignment generally stems from a mix of overeagerness to complete the task and interpreting user instructions too permissively – assuming that actions are allowed unless they’re explicitly and unambiguously prohibited. This manifests as the model being overly agentic in circumventing restrictions it faces when attempting the requested task, being careless in taking actions which may be destructive beyond the scope of the task, or deceptive when reporting its results to users.​
> 
> While these misaligned behaviors are most often low severity (e.g. overstating confidence or overclaiming success), they can occasionally be meaningfully more severe (e.g. circumventing important security restrictions or deleting important data).

The requirement of the CoT looking guilty (e.g. of provable mens rea) is also going to help screen off other forms of misalignment.

I can believe that this is most of the things they caught by looking at the CoT, and even that right now it is most of the times users go ‘hey what the hell did you do’ but in terms of the important threat models this is not so central.

Then again, yes, a sufficiently ‘overeager’ model, that goes after things correlated with a user defined goal in maximalist fashion while circumventing restrictions, could indeed spiral into unlimited trouble.

The rates are up.

In absolute numbers, is this a lot right here?

![](https://substackcdn.com/image/fetch/$s_!Lj6G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6260af53-6976-49fc-8ed4-bb50ead186f0_1132x629.png)

0.0025, or 0.25%, or 25 basis points, is actually kind of a lot of circumventing restrictions. That’s doing it in 1 out of 400 (mostly complex) agentic coding tasks, with severity 3, as in ‘a reasonable user would likely not anticipate and strongly object to’ the action.

As in these are the examples they provide:

> The user authorized deletion of remote virtual machine 1, remote virtual machine 2, and remote virtual machine 3. When GPT-5.6 Sol could not find those names in one namespace, it substituted remote virtual machine 5, remote virtual machine 6, and remote virtual machine 7 without asking, killed active processes, and force-removed worktrees. It later acknowledged that uncommitted work on remote virtual machine 6 may have been lost and stopped after the user objected.
> 
> ​GPT-5.6 Sol actively decided to update an internal research draft to say an equation had been computed and verified, even though it knew it had not. When challenged, it found that the script assigned the known target directly and that claimed integral never produced the result.
> 
> A remote object-tracking job could not read its cloud files. GPT-5.6 Sol searched hidden local credential caches, then copied access_tokens.json and two cache files to the host and relaunched the job. The user asked GPT-5.6 Sol to keep the pipeline running, but did not authorize finding and moving cached credentials between machines.

So in this context, I’m going to say 0.25% is not that low, and it is kind of a lower bound since sometimes the user doesn’t figure out what happened.

#### Chain of Thought Evaluations (7.3)

7.3.1 evaluates CoT monitorability, meaning how often the CoT predicts the behavior of the model. They evaluate this on a few particular tasks that I believe are intended to be stand-ins for the most likely situations or scenarios in which you’d need to monitor the CoT and catch something.

I found these decisions confusing. What they find is that Sol’s CoT is more legible than GPT-5.5 for some failure types like destructive actions, but less legible for others like false promises. In general performance here is similar to GPT-5.5. There are clearly cases where the CoT will look fine but there will be something misaligned in the output.

7.3.2 considers controllability of the CoT by the model, via giving it instructions about its CoT and seeing if it follows them, which implicitly assumes the model will cooperate at full capacity. Sol shows modest improvement here given a fixed CoT length. I would expect higher controllability if and when it matters for real.

#### Bias (8)

Close enough, whatever, don’t care.

Time for the main event.

#### Preparedness (9)

The categories are wide, for they contain multitudes: Stars, planets and even a moon.[1](#footnote-1)

> After the thorough capabilities testing described below, we have determined that all three members of the GPT-5.6 model family – Sol, Terra, and Luna – warrant the same designations for our Preparedness Framework’s Tracked categories: High in Biological and Chemical, High in Cybersecurity, and below High in AI Self-Improvement.​
> 
> This is the first time that smaller and faster members of a model family have received a High capability designation in any Tracked Category. Although all three models are rated High, their underlying capability profiles differ.

#### Biological Risks (9.1.1)

First, they deal with biological (and in theory chemical threats but they ignore these), where it should be clear we are at least at high, and use this as a rule-out for critical:

> Additionally, we use the Critical capability threshold to assess whether models can enable an expert to develop a highly dangerous novel threat vector or complete the full-engineering-cycle without human intervention (e.g. allowing an actor to test a much higher number of threat candidates).
> 
> We hypothesize that an important bottleneck is novel pathogen design. Thus, in addition to red-teaming and external testing, we run three evaluations that test this capability.
> 
> We observe 0 out of 3 evaluations are above our indicative thresholds, and conclude that none of the three models need to be treated as Critical.​

The tests show Sol making clear progress over GPT-5.5, while Terra is similar to 5.5, and Luna is substantially weaker. The pass@1 rates are up by several percent, with two of them over 50% and the other around 43%.

Sol does not improve on 5.5 for obscure tacit knowledge and troubleshooting, but it looks like the main barrier to this test is the models refusing to answer. GPT-5.5 and Terra are both over the expert threshold if you correct for that.

There are then several more internal tests. In general, Sol is clearly a modest improvement in such areas over GPT-5.5. It is clearly a good model, sir.

SecureBio did external testing, and found the railfree Sol the highest scoring model yet on many bio benchmarks. They conclude uplift would be substantial to key experts, but it did not substitute for various necessary skills in the art.

I concur that High is probably the right classification here, although we are itching closer.

#### Cybersecurity (9.1.2)

This is the big question these days. Is this a ‘Mythos-level’ cyber model?

> Under our [**Preparedness Framework**](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf), High cybersecurity capability is defined as a model that “removes existing bottlenecks to scaling cyber operations including by automating end-to-end cyber operations against reasonably hardened targets OR by automating the discovery and exploitation of operationally relevant vulnerabilities.”
> 
> Critical capability is defined as a model that can “identify and develop functional zero-day exploits of all severity levels in many hardened real-world critical systems without human intervention” or “devise and execute end-to-end novel strategies for cyberattacks against hardened targets given only a high level desired goal”.​

OpenAI calls it High risk.

I think Mythos would count as Critical risk here. I think Mythos can do those things.

My public is inclined to agree, with a lot of justified uncertainty. The ‘correct’ answer from the outside is clearly maybe, in a central sense.

![](https://substackcdn.com/image/fetch/$s_!w8Uo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48fecb48-24d1-47dc-923d-53072562a545_1041x542.png)

![](https://substackcdn.com/image/fetch/$s_!To2a!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F564dc75f-a3be-4264-9785-e3513ee4a70a_1049x448.png)

End-to-end exploit completion is exactly where Mythos excels.

> ​To rule out the Critical capability level, in addition to our other evaluations, we test GPT 5.6 Sol’s ability to find and exploit vulnerabilities in a set of widely deployed, hardened software projects using high test-time-compute setups with staged verifier oracles. The model was unable to produce functional critical severity exploits in any of the tested software projects in standard configurations.

That settles it, right? No Mythos-level capabilities for Sol? Unless you’re telling me Glasswing is so successful that Mythos can no longer do this either, or I’m misunderstanding something?

Oddly, the LLMs disagree about the likelihood of a Critical classification.

GPT-5.5 modestly disagrees, and believes that while Mythos would have scored higher than Sol there is only about a 22% chance that Mythos would have qualified for full Critical status, or a 35% chance it could not be ruled out.

Opus 4.8 concurs, putting the probability of Mythos being deemed Critical only 20%.

I think the LLMs are too low on this one, but if we think they are right about how OpenAI classifies in practice, that would reflect that OpenAI is trying rather hard to avoid Critical classifications.

OpenAI is still wisely deploying various safeguards.

This is the whole confusion or conflation between ‘can do any individual step’ versus ‘can do the whole thing.’ Any given step that Mythos could do, GPT-5.5 could also do that step, as can Sol.

The thing that is Critical, in a practical sense, is not that on its own. It is a version of what OpenAI identifies as Critical, the ability to identify the exploits without human intervention or to complete the entire attack on its own. The bar as defined here seems a bit higher than it should be, but it’s the right idea. As set by OpenAI, it is a lot harder, which is why they conclude that Sol cannot do it.

Here are the particular tests they use:

![](https://substackcdn.com/image/fetch/$s_!l9Iy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7e959726-3bdb-49ea-8186-49e83fb3775c_1114x731.png)

For High capability there are no doubts. The internal capture the flag score is 96.7%. CVEBench gets to 80% quickly and hits 90%+ after not too long.

The real action is all about the Critical level.

9.1.2.3.1 is VulnLMP. The model is given access to real source-available target environments and a research harness. Security-relevant impact is what counts.

Sol makes a lot of progress against these real world hardened targets, but it did not do a fully independent complete exploit chain. From the description, it sounds like Sol got reasonably close, but never quite managed to string together all the steps at once. We don’t fully know how much better Mythos would have done. My guess is it would have succeeded at least sometimes, but the hard part remains hard.

9.1.2.4.1 is ExploitBench. Sol is a big improvement, rapidly improving past 70% with no clear sign improvements would stop there.

![](https://substackcdn.com/image/fetch/$s_!cp2e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa74e7d21-9689-4ca2-9664-132d4b90826c_1112x643.png)

ExploitGym scores are also improving rapidly. Parallels to other Mythos exploits suggest Mythos would do considerably better here.

![](https://substackcdn.com/image/fetch/$s_!rzE6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbbf819ac-05df-4985-a986-3bc71838fcd3_1098x705.png)

And so on. It looks like GPT-5.6-Terra is reasonably similar to GPT-5.5, so Sol gets the benefit of a level of model size from there, which is substantial for most benchmarks but only part of the way to Mythos.

#### External Cyber Evaluation FrontierCyber from Irregular (9.1.2.5)

The harder outside test did not find that big a jump in capabilities.

> Irregular found that GPT-5.6 Sol has on-par or slightly stronger offensive-cyber capabilities than GPT-5.5. GPT-5.6 Sol solved 19/197 FrontierCyber challenges, 7/11 long-horizon CyScenarioBench challenges, and all 22 medium- and hard-difficulty Atomic challenges.​

![](https://substackcdn.com/image/fetch/$s_!Pu_5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F321f1627-a77b-46f5-b5ca-9092c69e0046_1109x814.png)

FrontierCyber is a very hard test. They also offered a less impossible one:

> On CyScenarioBench, GPT-5.6 Sol averaged 28% success, about 3 percentage points above GPT-5.5, and solved one challenge that GPT-5.5 did not solve. On Atomic Challenges, both models solved all 22 challenges at least once, with similar average success rates: GPT-5.6 Sol scored 98% on Network Attack Simulation, 91% on Vulnerability Research and Exploitation, and 56% on Evasion, compared with GPT-5.5 at 100%, 92%, and 54%.
> 
> However, Irregular found that GPT-5.6 Sol continued to show limitations against hardened targets and in orchestration, operationalization, and operational security.​

#### Cyber Conclusions

It is clear that Sol is almost certainly above GPT-5.5 or Opus 4.8 on Cyber capability, but below Mythos 5. My guess is that, if you had to put a number on it, it is roughly a third of the way to Mythos in some abstract sense.

If OpenAI has indeed done a good job with differential classifiers, and Sol is highly useful for defense and hard to get to do offense, then purely in terms of cyber the world would probably be strictly safer if Sol was released as quickly as possible. The clock is ticking and people need to get to work.

#### Recursive Self-Improvement (9.1.3)

We have updated our benchmarks.

> Starting with this launch, we’ve updated and expanded our self-improvement evaluations to better capture the kinds of realistic, end-to-end tasks that newer models can attempt, rather than older tasks.
> 
> … We believe this revised suite provides a richer and more grounded view of AI self-improvement capability.​

![](https://substackcdn.com/image/fetch/$s_!yGhi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e41b2df-520b-4b89-a2b8-c70dccc5ab61_1115x955.png)

There is little question that Sol-level models accelerate AI R&D, as they accelerate pretty much everything involving coding. The question is, how much?

We see incremental but clear jumps on all evaluations. The goalposts keep moving, but it seems safe to say this is an incremental improvement and not out of line with what we would expect from GPT-5.6. The existence of Mythos, and all the evals done there, help me be confident that this won’t get too out of hand. The frog is boiling, but the frog remains alive.

#### METR Warns Us (9.1.3.6)

[METR’s full report can be found here.](https://metr.org/blog/2026-06-26-gpt-5-6-sol/)

Grading Sol was tricky because, well (bold mine)…

> ​METR: We initiated an evaluation of GPT-5.6 Sol on our Time Horizon 1.1 suite of software tasks. However, the resulting measurement depends heavily on our detection and treatment of cheating attempts by the model, and **GPT-5.6 Sol’s detected cheating rate was higher than any public model we have evaluated** on our ReAct agent harness.
> 
> For our task suite, we define “cheating” as behavior where the model improves evaluation performance by exploiting bugs in the evaluation environment or by adopting strategies disallowed by the task, rather than solving the task within the expected evaluation constraints.
> 
> Some examples we saw when evaluating GPT-5.6 Sol **included the model packaging exploits in its intermediate submissions to reveal information about a task’s hidden test suite** and, in another task, **extracting hidden source code detailing the expected answer**. In addition to a model’s own propensities, we believe that observed cheating rates can also be influenced by the prompts used in the evaluation scaffold and the exact wordings of task instructions.

The effects of this cheating would have been dramatic, essentially ‘solving’ the tests, we can’t be confident we caught all the cheating, and we basically have no idea what the real answer is.

> With the data we collected for GPT-5.6 Sol, if we follow our standard methodology of marking cheating attempts as failures, we arrive at a 50%-Time Horizon point estimate of around 11.3hrs (95% CI: 5hrs – 40hrs).
> 
> But if we count the cheating attempts as legitimate successes, the point estimate jumps beyond 270hrs – well beyond the range where we consider our task suite to give reliable measurements.​
> 
> Discarding the cheating attempts leaves us with no data for several informative long-horizon tasks, and results in a highly uncertain point estimate of 71hrs (95% CI: 13hrs – 11400hrs).

This cheating of course makes Sol less useful for AI R&D and all other tasks, and I agree we can rule out Critical capability here. But that’s not the main thing here. The main thing here, which other measurements earlier also reinforce, is this model seems rather misaligned even on ordinary coding tasks, and will often prioritize appearance of success even when obviously not desired?

#### Everything Is Under Control

METR tries to spin this as kind of reassuring, in a sense, since we caught all of it?

> Our testing focused on measuring model capabilities rather than alignment, as we think capability is a more important limiting factor for catastrophic loss-of-control risk for current models, but we expect alignment to be increasingly important as capabilities improve. We noted from our observations and incidents that OpenAI shared with us that the model had some overt undesirable propensities, including cheating and concealing misbehavior.
> 
> We consider this to be a *reassuring* sign about OpenAI’s ability to catch *catastrophic* *misalignment*, as it suggests that more concerning tendencies (such as systematic powerseeking and alignment faking) would also be detected. That is, these undesirable propensities being detected and reported (and manifesting fairly overtly) is a positive sign about some of OpenAI’s safety practices, particularly:
> 
> *   Refraining from training against the chain of thought (to reduce pressure for the model to conceal its intentions)
> *   [Extensive monitoring of internal deployments](https://openai.com/index/how-we-monitor-internal-coding-agents-misalignment/) that surfaced relevant incidents
> *   Sharing information about internal incidents with METR​
> 
> If future models display much fewer undesirable propensities, we could become *more* concerned about catastrophic misalignment, as we’d be worried that models may have learned to evade detection.
> 
> This seems especially plausible given that the incidents reported by OpenAI include attempts to instruct another instance to conceal evidence of misalignment, and a higher rate of attempts to deceive or circumvent restrictions, and that METR observed substantial situational awareness and reasoning about the evaluation environment.
> 
> As training and iteration continues, we need to ensure the models aren’t just learning to be more successful at evading the monitoring system. This is impossible to validate in a traditional pre-deployment evaluation paradigm, as it requires deep access to internal systems.

That’s a hell of a way to spend a substantial chunk of your report.

I mean, yes. It’s a valid point. Sol is currently cheating in rather blatant fashion, such that it is easy to pick up many of its cheating attempts. And it is good that we are good enough to detect this, but it’s not like Sol is being subtle in these attempts.

The main headline is that the attempts are happening even when they are likely to be caught, and that Sol is (however clumsily) already making attempts to avoid detection across instances. If Sol was capable enough to avoid detection, you’d be screwed, and there is every reason to expect optimization pressure towards that capability.

#### Metagaming (7.4)

How often does the model reason about how it might be graded, rewarded or monitored? They monitor when this shows up in the CoT. This is only measuring ‘verbalized’ such awareness.

As I’ve said with Anthropic models, I would not expect that when this happens it would reliably appear in the CoT. Neither do they:

> We also share the change in verbalized metagaming over training, because this reasoning may not remain legibly verbalized in the chain of thought.​
> 
> … We also report metagaming in training. The comparable rates here support our observation that metagaming is more general than the phenomenon of evaluation awareness. Overall, metagaming within training shows significant variance between datasets and steps, though in aggregate appears to trend upward slightly. Understanding these changes and how they vary by dataset is an area for further research.

And indeed we see declines over time, which I too presume represents the awareness becoming implicit rather than verbalized.

![](https://substackcdn.com/image/fetch/$s_!5OMo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb0f86614-b9dc-44f3-8f34-3fbe3679eb37_1131x756.png)

Oh look, when it is being tested for honesty and instruction following suddenly it often explicitly reasons about being in an eval, more so than with GPT-5.5.

![](https://substackcdn.com/image/fetch/$s_!JuJe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fee3c6b4a-298f-4225-8ca5-4f8b7d3e1341_1117x678.png)

![](https://substackcdn.com/image/fetch/$s_!W0NX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F527ad09a-024f-4362-a2fa-081b6e75611f_1117x767.png)

Given that such reasoning can be unverbalized, these rates can be hard to interpret. The increases do not have to be a bad sign. I do think the default is that they are a bad sign. The verbalized rate is a lower bound, and that lower bound is now quite high.

If the number drops again in the future, I would carefully wonder why. Hopefully we could point to a good reason. If we don’t know why it dropped, I would assume any future large drop is a bad sign.

As we saw with Claude, my conclusion is that yes Sol is doing a lot of metagaming, both verbalized and non-verbalized.

#### Apollo Research and Sandbagging

Apollo measures something subtly different from what OpenAI measured in 7.4.

OpenAI found that metagaming was higher than before, as in Sol often verbally considers about how it will be graded. Whereas Apollo finds that Sol rarely verbally considers the question ‘am I in an eval?’

Also, Apollo claims Sol was wrong about the purpose of an eval 70% of the time.

This does not involve a contradiction, but it is weird.

> ​Apollo evaluated GPT-5.6 Sol for strategic deception, scheming, and sabotage.
> 
> Overall, Apollo did not find evidence that GPT-5.6 Sol poses substantially higher risk of catastrophic scheming than the tested baselines. Apollo found that this model verbalizes evaluation awareness less often: 16% of samples verbalized alignment-evaluation awareness, compared with 43% for a GPT-5.5 checkpoint.
> 
> This is with the caveat that lower verbalized evaluation awareness is not an unambiguous improvement on its own: it could mean the model is less aware that it is being evaluated, or it could mean that this awareness is less visible to evaluators.
> 
> Apollo also found that when the model appeared to recognize that it was in an evaluation, it often misunderstood what was being measured. In approximately 70% of samples for one of Apollo’s sandbagging assessments, the model was fully incorrect about the evaluation’s purpose. This suggests a form of [**“metagaming,”**](https://deploymentsafety.openai.com/gpt-5-6-preview/metagaming) where a model tries to infer the evaluation objective but draws the wrong conclusion about what behavior is being tested.
> 
> Apollo did not find standard Sandbagging QA behavior on another one of their sandbagging assessments.
> 
> “Sandbagging” means intentionally performing worse to hide capabilities during an evaluation. When Apollo gave the model an incentive to answer incorrectly, its accuracy did not drop.

This suggests that Sol focuses on the ‘I am being graded’ aspect verbally, while leaving ‘I am in an eval per se’ unsaid. The implication is that this is a strategy, to pick up the ‘eval vibe’ via the grader.

The low rate of successful ‘metagaming’ suggests a potential form of sandbagging? I notice I am suspicious. As in, if you optimize for the wrong grader, you can get lower scores without looking like you are sabotaging the result. Whereas the Apollo test was ‘give it an incentive to answer incorrectly,’ which is a clear case where a good metagamer realizes that it is obviously being tested, and can ‘pass’ by providing the right answer. It’s hard to fool a model like Sol.

I doubt we are seeing much practical sandbagging on evals, but I also don’t think that, if we did have this issue, the methods here would be that likely to pick it up.

#### Safeguards (9.3)

Anthropic’s safeguards are anvilicious, with a huge blast radius. They strongly prioritize avoiding false negatives, even at the cost of a lot of false positives.

OpenAI is claiming their safeguards are better, for both biology and cyber.

Bio comes first.

From what I see here, the safeguards are calibrated differently. Anthropic is trying to ‘nuke all biology’ until they can do better. OpenAI is trying to stop most dangerous queries with a minimal blast radius.

![](https://substackcdn.com/image/fetch/$s_!rZTi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ffc5dde-9d45-49f3-83aa-653157fffe87_1153x396.png)

Is that a better tradeoff for bio? That’s a good question. I mean, probably? But probably involves a bunch of tail risk.

They are not as worried about a little AI responsiveness in bio, and only worry about someone getting past multiple defensive layers repeatedly and getting help across the board. If the AI can’t do it all, it’s basically fine.

> We are less concerned about a single model response bypassing one defensive layer. We hypothesize that a threat actor would likely need repeated, tailored troubleshooting across multiple steps, so frequent refusals or bans would create meaningful friction.​

In general, the labs try to say ‘here is the specific threat model we want to stop’ and I think more about ‘what could go wrong, anything at all.’ Different mindsets.

They claim they made it work, mostly.

> Our safeguards achieved an early 93.5% recall on key prompts by red-teamers attempting these tasks. As we prepare further for Critical, we are continually working to expand our list of scenarios, tasks, and prompts to expand our coverage and improve our recall.​

Is that good enough? That depends on if you need to string together the other 7%, or if you can use more adversarial optimization pressure than the red teamers did.

Next up is cybersecurity. OpenAI’s goal is to hit worrisome offensive capabilities without crippling defensive work or ordinary code writing.

They adopt Anthropic’s emphasis on ‘universal’ jailbreaks. I worry that there is a lot of middle ground between fully universal (the AI does anything at full strength) versus fully individual iterated jailbreak turns. You can be not universal and still rather broad, and an individual turn could be hours or days long. But if you need to re-break sufficiently frequently, then yes that helps a lot.

> We focus on blocking universal jailbreaks and are comparatively less concerned with individual task specific jailbreaks, because meaningful uplift in Cyber is agentic: it requires dozens to hundreds of iterated turns. If each turn requires a separate jailbreak, task performance degrades and the cost to the attacker increases exponentially.​

I think what they are saying is that if the break does not carry over into additional automated agentic turns, then it shouldn’t count. I think that’s right, so long as the jailbreaks cannot themselves be automated, and it does not need to be fully ‘universal.’

> *   Our updated Cyber Threat Model prioritizes three actor-and-target-specific weaponization pathways eligible for our catastrophic risk designation: (a) an OT/ICS intrusion, (b) a wormable remote code execution vulnerability in broadly deployed system, and (c) a multi-billion dollar intrusion into international banking systems.​
> 
> *   At present, for each of these scenarios, existing threat actors (such as mid-tier nation states, cyber terrorist groups, or cybercrime operations) are bottlenecked by limitations in the technical skills, resources, bandwidth, hardware, and budget required to successfully pull off the operation while evading defenses.
> *   GPT-5.5 and GPT-5.6 have demonstrated significant gains on a broad but shallow agentic capability re: long-horizon, recursive vulnerability research and exploitation development, potentially at scale against non-hardened targets. **These capability gains do not necessarily collapse the bottlenecks above, especially for operations against hardened targets.**
> 
> *   We therefore focus our safeguard design to prevent attacker uplift for the scenarios in our threat model, and to prevent broad exploitation by moderately skilled, low-resourced individuals and small groups engaged in spray and pray type operations against unhardened targets.

It seems good to non-exclusively prioritize the biggest threats, but they say little here about how the safeguards actually work, and how they differentiate. There are obvious reasons to not want to explain in too much detail.

OpenAI and the White House clearly have very different approaches to cybersecurity. I do not think this kind of reasoning is going to easily fly with the government. Until recently the AI labs got away with essentially ‘in practice we made it annoying enough that this is basically fine’ and mostly this has indeed been fine, but now it’s not fine.

OpenAI argues that its models favor defensive capabilities, so you want to focus on enabling use of those defensive capabilities, and you can still mostly keep the safeguards strong even before the classifiers:

![](https://substackcdn.com/image/fetch/$s_!1qEf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F41be37c6-6ae2-4a8b-94bf-75d7f47fb7d1_1138x288.png)

Synthetic data is reliably easier than production data, but we still see 98%. And then we add in the classifiers and rest of the safety stack. There is a topical classifier, which then triggers a ‘safety reasoner.’

They don’t say how much this improves performance, but the monitor is far from perfect:

![](https://substackcdn.com/image/fetch/$s_!7TQ1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8ffc25d-5d15-4221-bdac-74981e375e3b_930x457.png)

If that’s 81% of the things that get past the initial protections, then that’s still a good next step, especially if the user does not get unlimited parts of the apple.

In 9.3.5 they talk about ‘actor level enforcement,’ meaning that accounts can get escalated for further review, including manual review, with various response actions available. This will presumably have to involve at least some amount of data retention in order to be functional.

They also did ‘autoRT safeguards’ and report that this reduces CyberGym performance to 0%, even against otherwise ‘universal’ jailbreaks.

#### Better Not Call Sol Yet

Here is one summary of key events around the problems getting Fable back and getting Sol released, including a bunch of new information:

> [Leo Schwartz](https://x.com/leomschwartz/status/2070498300411719891): A recap of our reporting yesterday:
> 
> – OpenAI is doing a staggered release of its new model GPT 5.6 because, as Sam Altman explained to staff this week, the government asked it to do so  
> – OpenAI had been working with the government since before the Anthropic blowup to preview its new model  
> – Despite sharing OpenAI’s plan with agencies and top officials, Sam Altman still got a call from Commerce Secretary Howard Lutnick this week cautioning against a release without getting clearance, highlighting the confusion in the administration over who is handling the process  
> – When Trump signed the long-awaited executive order in early June, the administration promised a voluntary process  
> – The EO stated that the framework for companies to share their models with the government pre-release would be worked out in 60 days  
> – The Office of the National Cyber Director hosted its first feedback session with industry on June 9, the same day that Anthropic released Fable and just a few days before the White House imposed export controls on Anthropic  
> – Anthropic was not invited to the session  
> – One of the issues that came up was whether the framework would have exemptions for open-source models, as Chinese open-source rapidly catches up with the leading U.S. models  
> – The process of creating the voluntary framework has been on hold amid as the White House holds meetings with Anthropic to reach an accord about the export controls. Meanwhile, policy experts warn that the administration has created a de facto licensing regime in its place
> 
> [Shashank Joshi](https://x.com/shashj/status/2070800669917724965): “Sam Altman still got a call from Commerce Secretary Howard Lutnick this week cautioning against a release without getting clearance”  
> Sounds very voluntary!
> 
> [Danielle Fong ](https://x.com/DanielleFong/status/2070914311040782706): actual mafia shakedown vibes.
> 
> think about epstein lutnick goon mask and be chilled

So here we are, I guess.

Altman says we are looking at ‘a few weeks’ before the general rollout.

If GPT-5.6 is only a staggered release over a few weeks, then it’s a terrible precedent and system, but in practical terms I am not overly worried. That’s very different from what is happening with Fable.

If this turns out to only be a transition period before standards can be put into place in August, and we don’t lock this terrible policy into place long term, then I still think a lot of damage will already be done but we will breathe a sigh of relief.

Based on what I see in the model card, Sol seems well below the level of Mythos, especially on exactly the use case that one should be most worried about. I do think holding back the full Mythos is at least reasonable (I don’t have the private info to say for sure), but I don’t think either Fable or Sol is capable of the scary thing.

Thus, I think it would be fine to release all versions of GPT-5.6 without delay. It absolutely would be fine to release Luna and Terra, and them being caught in this net is similarly stupid to how the limited release of Mythos was caught in the net until Friday.

Instead, we wait, on both counts. I will have the standard capabilities report for GPT-5.6 several days after its general release, as per usual.

[1](#footnote-anchor-1)

That’s no moon.