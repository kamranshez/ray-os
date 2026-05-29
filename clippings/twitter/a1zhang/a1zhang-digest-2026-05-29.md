---
tags: [twitter, research, monitoring]
aliases: [a1zhang twitter digest]
date: 2026-05-29
---

> **@a1zhang** — alex zhang  
> phd student @mit_csail @nlp_mit (RLMs), previously undergrad @princeton  🫵🏻 go participate in the @GPU_MODE kernel competitions!  
> Followers: ? · Following: ?  
> **Fetched:** 2026-05-29T04:39:03.377648+00:00  
> **Window:** tweets since 2026-05-28T04:39 UTC (last 24h)

## Summary

- **6** original tweets in the last day
- **17** replies in the last day
- **15** parent tweets resolved (the posts they replied to)
- **17** surrounding context tweets from other people in those threads

---

## Original tweets (last 24h)

### 2026-05-29 02:21 UTC

most shocking part of this blogpost tbh

on a more serious note, super valuable insight on mark's experience with AI for systems for AI and where it will be headed and a great first @CoreAutoAI blog. I'll always bet on Mark to cook :-) https://t.co/rWrLQfrZps

  > 🔗 **Quoting @marksaroufim:** My MLSys keynote on AI writing systems code got more interest than I expected. The recording will take a while, so in the finest tradition of AI labs sharing blog posts, we’re starting the Core Automation Blog with this one https://t.co/h4uSOyrglf

Media:
  - photo: https://pbs.twimg.com/media/HJc7_lwWIAQLKyd.png

❤44  🔁1  🔖20  👁4548  ·  [link](https://x.com/a1zhang/status/2060184743014982063)

### 2026-05-28 20:27 UTC

RT @yacinelearning: if you are interested in taking a sneak peek at what might be going on in claude code dynamic workflow feature check ou…

🔁17  👁1  ·  [link](https://x.com/a1zhang/status/2060095760776020163)

### 2026-05-28 19:28 UTC

RT @lateinteraction: Claude Code is finally an RLM (oct 2025), congrats to Anthropic :-)

🔁33  👁2  ·  [link](https://x.com/a1zhang/status/2060080673172410521)

### 2026-05-28 18:52 UTC

In case you're curious about why dynamic workflows are so powerful and the future, read the RLM paper! Opus 4.8 + dynamic workflows in Claude Code is perhaps the first instance of a frontier model seriously trained to be an RLM.

I suspect within a year they'll just become the standard for nearly all coding agent interactions.

  > 🔗 **Quoting @ClaudeDevs:** New in Claude Code (research preview): dynamic workflows.  Claude writes an orchestration script on the fly, then spins up a large fleet of coordinated subagents in parallel to take on your most complex tasks.  Use the word "workflow" in a prompt to get started. https://t.co/re4SG3AyDm

Media:
  - photo: https://pbs.twimg.com/media/HJbXG2VXMAEO03Y.jpg

❤987  🔁114  💬39  🔖794  👁154843  ·  [link](https://x.com/a1zhang/status/2060071701879066626)

### 2026-05-28 18:35 UTC

RT @psrthsharma: we got RLMs in claude code before gta 6

🔁2  ·  [link](https://x.com/a1zhang/status/2060067411378737590)

### 2026-05-28 17:07 UTC

Every day we move closer to the RLM https://t.co/oJV9PMT1Z5

Media:
  - photo: https://pbs.twimg.com/media/HJbAIRKW8AARfz8.jpg

❤329  🔁25  💬10  🔖56  👁35001  ·  [link](https://x.com/a1zhang/status/2060045416108904880)

---

## Replies (last 24h) — with the tweet they replied to

### 2026-05-28 23:08 UTC

**↪ In reply to @ankit2119** (Ankit Maloo):

> > "first instance of a frontier model seriously trained to be an rlm"
> 
> you are probably aware of motte and bailey fallacy. when you do post, you overclaim things. then when someone pushes back, you say none of it was original but the composition was. read the full implementation, they took parts of your setup not the full composition. (though the definition you have is too broad). claude code's setup is not even recursive, which i presume should be important to be called a  "recursive" lm.

> 💬1  🔖1  👁1263  ·  [parent link](https://x.com/ankit2119/status/2060132573859414506)

**@a1zhang replied:**

@ankit2119 @jxmnop what did I overclaim? when people push back, I go back to all my original writing and point to exactly what I meant. feel free to quote me, as I’m about to do with you:

First of all, Opus 4.8 is quite literally is the first instance of a frontier model explicitly trained to do

❤18  💬1  🔖3  👁1251  ·  [link](https://x.com/a1zhang/status/2060136163927531940)

### 2026-05-28 22:42 UTC

**↪ In reply to @b_shrir** (Sriram Balasubramanian):

> @a1zhang @redtachyon One reason you are getting such reactions is that it seems fairly natural to go from the standard tool-using Dec 2025 Claude Code to RLM simply by increasing the flexibility of the agent in various ways, and one can easily imagine going further than RLM.

> 💬2  👁285  ·  [parent link](https://x.com/b_shrir/status/2060127810820206927)

**@a1zhang replied:**

@b_shrir @redtachyon Agreed! And I also sadly think certain details are lost when it’s reduced down to “we want sub-agents to be good”, making the discussion no longer productive.

I genuinely just think it makes sense over what we were doing back when it was written, and should be integrated in

❤3  👁254  ·  [link](https://x.com/a1zhang/status/2060129622637908379)

### 2026-05-28 22:20 UTC

**↪ In reply to @stochasticchasm** (stochasm):

> @a1zhang would you really consider it an RLM? there's no repl, and they don't dynamically query the prompt as far as i can see. it's prompt -&gt; script -&gt; call subagents on each prompt, so feels rather different

> 💬1  🔖4  👁2563  ·  [parent link](https://x.com/stochasticchasm/status/2060118871735234703)

**@a1zhang replied:**

@stochasticchasm the choice of a (python) REPL is a particular instantiation we used, but not necessary by the defn of an RLM

@lateinteraction and I had a lot of discussions about this in the past on how to properly articulate this idea, but it's mostly about having a symbolic environment with https://t.co/Rpbeq7zNcI

❤23  🔁1  💬4  🔖10  👁2330  ·  [link](https://x.com/a1zhang/status/2060124028686258642)

### 2026-05-28 21:28 UTC

**↪ In reply to @rasdani_** (Daniel Auras):

> anthropic renaming RLM to Dynamic Workflows
> is like apple calling AI Apple Intelligence https://t.co/nIdwMJXPlQ

> 🔁1  💬2  🔖7  👁3561  ·  [parent link](https://x.com/rasdani_/status/2060110776078094680)

**@a1zhang replied:**

@rasdani_ elite tier shitposting daniel, you'll have to catch up @NoahZiems

❤21  💬2  🔖4  👁800  ·  [link](https://x.com/a1zhang/status/2060111110246654087)

### 2026-05-28 20:46 UTC

**↪ In reply to @NoahZiems** (Noah Ziems):

> @a1zhang The real value is the friends you made along the way 🫶🫶

> 💬1  👁616  ·  [parent link](https://x.com/NoahZiems/status/2060100325068210608)

**@a1zhang replied:**

@NoahZiems but you're leaving me 😭

❤10  💬1  👁362  ·  [link](https://x.com/a1zhang/status/2060100424934334561)

### 2026-05-28 18:52 UTC

**@a1zhang replied:**

In case you're curious about why dynamic workflows are so powerful and the future, read the RLM paper! Opus 4.8 + dynamic workflows in Claude Code is perhaps the first instance of a frontier model seriously trained to be an RLM.

I suspect within a year they'll just become the https://t.co/L24BZZib0r

  > 🔗 **Quoting @ClaudeDevs:** New in Claude Code (research preview): dynamic workflows.  Claude writes an orchestration script on the fly, then spins up a large fleet of coordinated subagents in parallel to take on your most complex tasks.  Use the word "workflow" in a prompt to get started. https://t.co/re4SG3AyDm

❤987  🔁114  💬39  🔖794  👁154843  ·  [link](https://x.com/a1zhang/status/2060071701879066626)

### 2026-05-29 04:17 UTC

**↪ In reply to @jjh** (jjh):

> Earlier today it was “RLM-like” now it’s an RLM.
> 
> If “Claude writes an orchestration script on the fly, then spins up a large fleet of coordinated subagents in parallel to take on your most complex tasks.” is enough information to declare it an “RLM” then the term doesn’t seem to mean much.

> 💬1  👁36  ·  [parent link](https://x.com/jjh/status/2060208746924802387)

**@a1zhang replied:**

@jjh @redtachyon Wait. Let me clarify. I am not saying “Claude writes an orchestration script that spins up subagents” = RLMs. I’ve made it clear several times that RLMs are a subset of such methods.

Earlier today (in the tweet you put) I implied CC is approaching more RLM-like features. Let’s

❤1  👁31  ·  [link](https://x.com/a1zhang/status/2060213947446268127)

### 2026-05-29 03:44 UTC

**↪ In reply to @jjh** (jjh):

> @a1zhang @jxmnop I’m not sure your other tweets give that impression.
> 
> https://t.co/C4ib05Ot6f

> 👁1071  ·  [parent link](https://x.com/jjh/status/2060150150727958670)

**@a1zhang replied:**

@jjh @jxmnop “Every day we move closer to the RLM” why is that a bad thing to say LMAO it’s so harmless

you’re grasping at straws man i feel like Mamdani with the NYPost 😂

❤5  👁94  ·  [link](https://x.com/a1zhang/status/2060205574038446493)

### 2026-05-29 03:41 UTC

**↪ In reply to @a1zhang** (alex zhang):

> @jjh @redtachyon not rly sure how this changes what I said, I’m just reposting things I think are true (it is an RLM), one of which is my advisor

> 💬2  👁51  ·  [parent link](https://x.com/a1zhang/status/2060204694417383694)

**@a1zhang replied:**

@jjh @redtachyon true and funny*** they’re light-hearted…

👁27  ·  [link](https://x.com/a1zhang/status/2060204883588899143)

### 2026-05-29 03:40 UTC

**↪ In reply to @jjh** (jjh):

> @a1zhang @redtachyon https://t.co/cUNrjAgLSH

> 👁136  ·  [parent link](https://x.com/jjh/status/2060150623438516531)

**@a1zhang replied:**

@jjh @redtachyon not rly sure how this changes what I said, I’m just reposting things I think are true (it is an RLM), one of which is my advisor

❤1  💬2  👁51  ·  [link](https://x.com/a1zhang/status/2060204694417383694)

### 2026-05-29 03:35 UTC

**↪ In reply to @gabe_grand** (Gabe Grand):

> hot take: dynamic workflows is much better described as an instance of our DisCIPL framework, which predates both RLM and Opus 4.8 👀🙏
> 
> (arxiv v1 April 2025) https://t.co/B8yz0ukV5j

> 🔁7  💬4  🔖36  👁5905  ·  [parent link](https://x.com/gabe_grand/status/2060188715654226016)

**@a1zhang replied:**

@gabe_grand FWIW I’ll say I like DisCIPL and it’s a neat idea!

on whether dynamic workflows looks like DisCIPL, maybe (I’m sure you’ll disagree with what I’m about to say and that’s reasonable), but my interpretation of the results of the paper and the generated programs seem to suggest

❤5  🔖3  👁828  ·  [link](https://x.com/a1zhang/status/2060203360943247760)

### 2026-05-29 02:21 UTC

**@a1zhang replied:**

most shocking part of this blogpost tbh

on a more serious note, super valuable insight on mark's experience with AI for systems for AI and where it will be headed and a great first @CoreAutoAI blog. I'll always bet on Mark to cook :-) https://t.co/rWrLQfrZps

  > 🔗 **Quoting @marksaroufim:** My MLSys keynote on AI writing systems code got more interest than I expected. The recording will take a while, so in the finest tradition of AI labs sharing blog posts, we’re starting the Core Automation Blog with this one https://t.co/h4uSOyrglf

❤44  🔁1  🔖20  👁4548  ·  [link](https://x.com/a1zhang/status/2060184743014982063)

### 2026-05-29 01:55 UTC

**↪ In reply to @willdepue** (will depue):

> @a1zhang enjoy your test of time award

> 💬1  👁985  ·  [parent link](https://x.com/willdepue/status/2060177956677247093)

**@a1zhang replied:**

@willdepue thanks bro i'll dedicate it to you

❤22  👁758  ·  [link](https://x.com/a1zhang/status/2060178178925015458)

### 2026-05-29 01:32 UTC

**↪ In reply to @Robro612** (Rohan Jha):

> @a1zhang @DhruvAtreja1 It's not fully equivalent - no full REPL and more scaffolded - but MinionS (https://t.co/0EGqIhgzPq) also programmatically orchestrates sub-LLM calls and treats context as a variable (at least in what's passed).

> 💬1  👁312  ·  [parent link](https://x.com/Robro612/status/2060152649131892975)

**@a1zhang replied:**

@Robro612 @DhruvAtreja1 Yep! It's a good example but also falls under the same issues (or perhaps safeguard?) as previous methods that constrain how sub-calling is done by the model.

👁175  ·  [link](https://x.com/a1zhang/status/2060172281687486951)

### 2026-05-29 01:30 UTC

**↪ In reply to @DhruvAtreja1** (Dhruv Atreja):

> Hey Alex, appreciate the good faith discussion. I don’t know how common this was in academia before Oct 2025, but in production agent systems this pattern was already pretty natural/common: let the model write code, store/intermediate context outside the prompt, fan out to sub-LM/subagent calls, then aggregate/check the results.
> 
> Operationally, that’s why I see RLM as CodeAct + recursive/sub-LM calls over externalized context. That’s a useful abstraction and worth naming/evaluating, but I don’t think it creates a new category that owns “agent writes orchestration code and fans out to workers.”CodeAct gave the REPL/action substrate; MinionS is a concrete pre-Oct example where a model generates code to spawn many chunked LM jobs and aggregate them.

> 💬2  👁814  ·  [parent link](https://x.com/DhruvAtreja1/status/2060163517622419879)

**@a1zhang replied:**

@DhruvAtreja1 Gotcha! Obviously I can't verify how useful it was in production settings pre-2026, but I will say from my own experiments and even just the design choices of coding agents around this time (ignoring externalized context), the primitive of CodeAct + sub-agent calls inside the

❤8  💬1  🔖1  👁466  ·  [link](https://x.com/a1zhang/status/2060171999675023667)

### 2026-05-29 01:10 UTC

**↪ In reply to @dhruvrnaik** (Dhruv):

> IMO, the core idea from the blog + paper was making input context interactive. It was a great read and has definitely sparked a lot of subsequent thinking and work.
> 
> But supervisor-subagent architectures and increasingly dynamic variants have been around for quite a while. This feature is just doing it CodeAct style instead of Ant's previous work using tool calls.
> 
> Worth reflecting on why so many people have the same confusion/pushback when subagents are called RLMs.
> @ankit2119 is probably right to call it overclaiming when you are reducing Anthropic’s work to “RLM” everywhere. It starts to look like a retroactive branding exercise.

> 💬1  👁319  ·  [parent link](https://x.com/dhruvrnaik/status/2060161486404939850)

**@a1zhang replied:**

@dhruvrnaik @ankit2119 @jxmnop This is fair! I want to say that my point isn’t that Ant’s work is just an RLM (it’s obviously way more than that, and is nuanced in its own ways), but rather the features being added to CC are all the core components defined by an RLM. 

In this sense, CC is an RLM. It satisfies

❤8  👁353  ·  [link](https://x.com/a1zhang/status/2060166976501141890)

### 2026-05-29 00:16 UTC

**↪ In reply to @willdepue** (will depue):

> @a1zhang this shit is so annoying man. 'recursive language models' you mean putting your agent in a for loop. wow. incredible work man. truly groundbreaking. i'm sure you were the first person to think of this

> 🔁3  💬8  🔖16  👁7031  ·  [parent link](https://x.com/willdepue/status/2060143163881201869)

**@a1zhang replied:**

@willdepue you sound pretty miserable LOL but don't blame me if you can't read properly lmfao

❤61  💬1  🔖2  👁2839  ·  [link](https://x.com/a1zhang/status/2060153363300286636)

---

## Conversation context (other people in those threads)

_People who appeared in the same reply threads as @a1zhang._

- **@redtachyon** (2026-05-28 22:03 UTC): Some would call it "schmidhubris"  ·  [link](https://x.com/redtachyon/status/2060119862286893504)
- **@jjh** (2026-05-29 03:56 UTC): @a1zhang @redtachyon Earlier today it was “RLM-like” now it’s an RLM.  If “Claude writes an orchestration script on the fly, then spins up a large fleet of coordinated subagents in parallel to take on your most complex tasks.” is enough information to declare it an “RLM” then the term doesn’t seem to  ·  [link](https://x.com/jjh/status/2060208746924802387)
- **@jxmnop** (2026-05-28 21:24 UTC): imagine thinking you invented an LLM talking to another LLM and it was in December 2025  ·  [link](https://x.com/jxmnop/status/2060109869399916770)
- **@jjh** (2026-05-29 00:04 UTC): @a1zhang @jxmnop I’m not sure your other tweets give that impression.  https://t.co/C4ib05Ot6f  ·  [link](https://x.com/jjh/status/2060150150727958670)
- **@gabe_grand** (2026-05-29 02:37 UTC): hot take: dynamic workflows is much better described as an instance of our DisCIPL framework, which predates both RLM and Opus 4.8 👀🙏  (arxiv v1 April 2025) https://t.co/B8yz0ukV5j  ·  [link](https://x.com/gabe_grand/status/2060188715654226016)
- **@willdepue** (2026-05-29 01:54 UTC): @a1zhang enjoy your test of time award  ·  [link](https://x.com/willdepue/status/2060177956677247093)
- **@DhruvAtreja1** (2026-05-28 23:12 UTC): I'm sorry but the "RLM" trend seems a little forced, it's a fairly simple and common practice and was so before it was given a name. No one owns codeact + subagent orchestration.  Confusing to see some genuinely good researchers that I respect hop in on the wagon.  ·  [link](https://x.com/DhruvAtreja1/status/2060137100188717107)
- **@Robro612** (2026-05-29 00:14 UTC): @a1zhang @DhruvAtreja1 It's not fully equivalent - no full REPL and more scaffolded - but MinionS (https://t.co/0EGqIhgzPq) also programmatically orchestrates sub-LLM calls and treats context as a variable (at least in what's passed).  ·  [link](https://x.com/Robro612/status/2060152649131892975)
- **@DhruvAtreja1** (2026-05-29 00:57 UTC): @a1zhang Hey Alex, appreciate the good faith discussion. I don’t know how common this was in academia before Oct 2025, but in production agent systems this pattern was already pretty natural/common: let the model write code, store/intermediate context outside the prompt, fan out to  ·  [link](https://x.com/DhruvAtreja1/status/2060163517622419879)
- **@dhruvrnaik** (2026-05-29 00:49 UTC): @a1zhang @ankit2119 @jxmnop IMO, the core idea from the blog + paper was making input context interactive. It was a great read and has definitely sparked a lot of subsequent thinking and work.  But supervisor-subagent architectures and increasingly dynamic variants have been around for quite a while. This  ·  [link](https://x.com/dhruvrnaik/status/2060161486404939850)
- **@willdepue** (2026-05-28 23:36 UTC): @a1zhang this shit is so annoying man. 'recursive language models' you mean putting your agent in a for loop. wow. incredible work man. truly groundbreaking. i'm sure you were the first person to think of this  ·  [link](https://x.com/willdepue/status/2060143163881201869)
- **@ankit2119** (2026-05-28 22:54 UTC): @a1zhang @jxmnop &gt; "first instance of a frontier model seriously trained to be an rlm"  you are probably aware of motte and bailey fallacy. when you do post, you overclaim things. then when someone pushes back, you say none of it was original but the composition was. read the full implementation,  ·  [link](https://x.com/ankit2119/status/2060132573859414506)
- **@b_shrir** (2026-05-28 22:35 UTC): @a1zhang @redtachyon One reason you are getting such reactions is that it seems fairly natural to go from the standard tool-using Dec 2025 Claude Code to RLM simply by increasing the flexibility of the agent in various ways, and one can easily imagine going further than RLM.  ·  [link](https://x.com/b_shrir/status/2060127810820206927)
- **@stochasticchasm** (2026-05-28 21:59 UTC): @a1zhang would you really consider it an RLM? there's no repl, and they don't dynamically query the prompt as far as i can see. it's prompt -&gt; script -&gt; call subagents on each prompt, so feels rather different  ·  [link](https://x.com/stochasticchasm/status/2060118871735234703)
- **@rasdani_** (2026-05-28 21:27 UTC): anthropic renaming RLM to Dynamic Workflows is like apple calling AI Apple Intelligence https://t.co/nIdwMJXPlQ  ·  [link](https://x.com/rasdani_/status/2060110776078094680)
- **@NoahZiems** (2026-05-28 20:32 UTC): Anthropic valuation before deploying RLMs: $380B  Anthropic valuation after deploying RLMs: $965B  Use RLMs and you too can add $500B to your valuation  ·  [link](https://x.com/NoahZiems/status/2060096973567561819)
- **@NoahZiems** (2026-05-28 20:46 UTC): @a1zhang The real value is the friends you made along the way 🫶🫶  ·  [link](https://x.com/NoahZiems/status/2060100325068210608)
