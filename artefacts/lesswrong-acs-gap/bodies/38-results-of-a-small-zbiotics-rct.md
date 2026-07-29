# Results of a small ZBiotics RCT

- URL: https://www.lesswrong.com/posts/kw33A6uYPGRtvD43s/results-of-a-small-zbiotics-rct
- Author: Nikola Jurkovic
- Date: 2026-07-05
- Karma: 64  Comments: 2  Words: 389
- Band: B  Tier: 2  Score: 39.0  Density: 10.28
- Anchors: claude code

---

I ran a small single-blind ZBiotics RCT at a party I hosted recently. I prepared 30 cups, 21 of which contained a placebo and 9 of which contained a shot of [ZBiotics Pre-Alcohol](https://zbiotics.com/products/zbiotics). People took these as they entered the party. The day after, 28[^7purvpqg5ka] of them filled out a form asking how hungover they felt using a standard Acute Hangover Scale (AHS).[^fzzydtu23rk]

At N=28 and only 9 people receiving the real treatment, the study is only able to detect large effects on symptom severity. I did a pretty quick analysis using Opus 4.8 in Claude Code.[^z7ox6dybquo]

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783213886/lexical_client_uploads/er4dofqa8bq2ewiy51sj.png)

**The results are inconclusive.** The people who took ZBiotics had slightly worse hangover symptoms on average (but slightly better ones at the median), but the N is too small to conclude much.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783213725/lexical_client_uploads/vdctw1owdewjfvurbu4f.png)

It seems that out of the three main variables I committed to analyze, the only one that showed a detectable relationship with hangover severity is the number of drinks people drank during the party.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783213732/lexical_client_uploads/ucf5ghcghuu0nljteon1.png)

The scatter plots for AHS score vs number of drinks look pretty similar between the two groups. The lines are forced to have the same slope on this graph because they come from a single regression where membership in the placebo group is treated as a constant shift in AHS.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783213740/lexical_client_uploads/w9l8ndcu6nxgatatmlfq.png)

I also asked for people's number of hours slept, how they feel compared to mornings after similar parties, and how much they snacked at the party.

I've put the anonymized raw data in [this Google Sheet](https://docs.google.com/spreadsheets/d/1ziIrvMgI6otcwzRLtHy93J9pIYQuISXNw7vKDRKNDDw/edit?usp=sharing) in case people wish to analyze it. I removed people's names, heights, rounded their weights, and removed a free response field for more information.

Limitations:

*   I wish I got people's responses much earlier the morning after, ideally as soon as they woke up. I should have gotten them to commit to do this before participating.
*   I'm not sure if my placebo concoction was good enough. 5/8 people who got the real ZBiotics (and marked a guess) guessed correctly right after drinking that they got the real one, and 12 out of the 19 placebo group guessed correctly, both somewhat above chance.

I look forward to seeing more people run more studies on this, especially ones with many more participants, or ones where people switch groups on different nights.

[^7purvpqg5ka]: People varied in timing, but most forms were filled out between 11AM and 2PM. The last two people filled it out at 2:01PM and at 4:26PM. I discarded one response in the placebo group sent in around 6PM because I'd already done my analysis by then (they would have increased N to 29). One person in the placebo group never responded to the form. 

[^fzzydtu23rk]: The question I used for AHS is "Rate how you feel RIGHT NOW on each item. 0 = none, 1 = mild, 4 = moderate, 7 = incapacitating. Use the in-between numbers for in-between amounts.", with a 0-7 linear scale for each of [Hangover,Thirsty,Tired,Headache,Dizziness or faintness,Loss of appetite,Stomach ache,Nausea,Heart racing]. 

[^z7ox6dybquo]: I committed to publishing the results on LessWrong no matter what, and I preregistered that I would primarily analyze the effect on average AHS score as predicted by the arm people were randomly placed in, the number of drinks they had, and their weight.