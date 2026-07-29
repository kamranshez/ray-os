# The consequences of locking intelligence away: an introduction to Claude relays in China

- URL: https://www.lesswrong.com/posts/YrgeED3nWD4EjcqLd/the-consequences-of-locking-intelligence-away-an
- Author: CMLKevin
- Date: 2026-06-30
- Karma: 112  Comments: 6  Words: 508
- Band: C  Tier: 2  Score: 28.7  Density: 7.87
- Anchors: agentic (coding|engineering|software|development|programming)

---

There has been recent discourse floating around on Hacker News about Chinese API relay stations that use every Western VC-subsidized channel of cheap tokens (think Claude/ChatGPT subscriptions, AWS/Azure credits, Kiro, Google Antigravity, etc.) to resell as APIs to the domestic Chinese market.  
  
This is true, as a Chinese citizen that has been seeing an uptick of this trend since mid 2024, but especially since 2025. When I go on Taobao (China's Amazon) and search for keywords, there would be dozens of relay services selling for around 1/5th to 1/10th the price of official western APIs.

Indeed, many of these relays may have cheaper models disguised as genuine western ones, so the Chinese tech community has entire forums such as [linux.do](https://linux.do/c/welfare/36/l/hot) that serves primarily as a way for people to discuss and rate relay services based on their price, quality, and availability, as well as websites such as [hvoy.ai](https://www.hvoy.ai/en) that uses a variety of automated testing suites to benchmark the quality of relay providers. There are even free relays that exists primarily as a gentleman's handshake data collection method between relay operators and users - some in China have speculated that one of the most popular ones is operated by Zhipu, which might explain their model's apparent claude-ness.  
  
This is also why Chinese LLMs are far cheaper on average: they both have to compete with each other, but also with grey market relays serving foreign models at aggressively subsidized rates in the domestic market. Even GLM-5.2's $4.2/million out price is having a hard time competing with Opus 4.8 at a $7.5/million out price in the most reputable API relay services.  
  
In retrospect, this is the natural endgame of current era China AI bans.  
  
When people in the West hear about Anthropic accusing Chinese firms of distilling their models, they map them onto the typical cases of corporate espionage: innovative U.S. companies create the frontier of intelligence, then the Chinese copy them in massive government-subsidized campaigns. However, it's far from the case. There simply is sufficient market incentive for both tech enterprises as well as individual developers to onboard third-party relays selling Claude Opus 4.8 in 1/10th the price.  
  
I note my conflict of interest: I'm naturally frustrated at how I'm unable to access Anthropic's services legitimately as they have been cracking down on users with VPNs, so this channel is the lifeline I get to interacting with SOTA models. however, I'm also highly aware of the numerous data risks that surrounds this grey market (which is what caused relays to be named in Chinese state media as an area for concern - interestingly, China has always been lax to programmers and STEM students in terms of the GFW, so "foreign models tells that Taiwan is a country" and such are not named).  
  
Perhaps post-Mythos and post-GPT-5.6 era KYC would reduce this phenomenon, but there has already been workarounds brewing (examples being reverse engineering the APIs of third party agentic coding services), so we'll have to see about their efficacy.  
  
I'll be happy to take questions from the comment section.