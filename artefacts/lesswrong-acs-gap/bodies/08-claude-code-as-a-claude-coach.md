# Claude Code as a Claude Coach

- URL: https://www.lesswrong.com/posts/J7brEsreXSrHpHH3v/claude-code-as-a-claude-coach
- Author: Brendan Long
- Date: 2026-07-06
- Karma: 40  Comments: 2  Words: 918
- Band: A  Tier: 1  Score: 102.0  Density: 25.6
- Anchors: claude code, claude\.md, coding agents?

---

Exercise is hard but it's even harder if you have to use your brain and muscles at the same time. I wish a personal trainer would just teleport into my house whenever I work out, tell me exactly what to do, and then record my progress (and complaints) to improve the program going forward. Apps are too rigid or too complicated; personal trainers are expensive and require scheduling; but using Claude Code[^wyqfuh3eplg] as a personal trainer has worked out well for me.

![A stacked bar chart of training sessions per week from mid-March to early July 2026, colored by type (strength, cardio, yoga, dodgeball, crossfit). Most weeks have 2–4 sessions with strength (blue) as the backbone, hitting or exceeding the 2–3 strength-sessions-per-week target band nearly every week. Total: 45 sessions, averaging 2.8 per week.](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783377518/lexical_client_uploads/dclds7sw961tfd3kpbs0.png)

I'm still inconsistent, but more consistent than I used to be! My weekly workouts of any type averaged ~1 per week before this. Note that this graph starts when I started using Claude Coach, because it was too annoying to track this before.

  

A Typical Day
-------------

I drag myself out of bed, drink some coffee and electrolytes (separately, I'm not a monster), and then walk down to the gym in the basement. I open the Claude Code tab in the Claude Android app, select the `brendanlong/claude-coach` repo, and ask:

> What should I do today?

Claude reads the repo's instructions and logs and asks about:

*   Location (home, commercial gym, hotel)
*   Time and energy levels (short or full session)

I tell it I'm at home and have minimal energy, so it proposes that we deal with the two most out-of-date workouts (Romanian deadlift and squats), and then gives me a program:

%%% llm-output model="Claude Opus 4.8"

> A short lower-posterior day built around the hinge test.
> 
> *   RDL - test 55 lb DBs, 3x5. Last time 50 was RPE 6/6/7 (clearly easy, trigger met). If 55 moves at RPE ≤ 8 with a clean back, that's your new working weight.
> *   Squat (DBs at sides) - 3x8 @ 2x30, owning that new variant clean (goal is control, not load).

%%% /llm-output

I grudgingly agree, working through sets, telling Claude what I did and how hard it was ("First of 8 at 30 lbs, RPE 8"). At the end, it logs everything, and makes a PR. I merge it and then collapse into a chair for the next 8 hours.

![A grid of six line charts showing dumbbell working weight climbing over roughly three months (April–June 2026) for each lift: Bench Press +80% (25→45 lb per hand), Overhead Press +25% (20→25 lb), Row +33% (30→40 lb), RDL +25% (40→50 lb per hand), Goblet Squat +83% (30→55 lb), and Tricep Extension +25% (20→25 lb). Each line is a staircase that steps up over time and never drops.](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783377681/lexical_client_uploads/ezclzocxvxdfufvhdkwm.png)

Progress is ridiculously easy if you start out weak and work out with any consistency at all.

Exception Handling
------------------

The day above went smoothly, but sometimes I want changes. I've told Claude that certain exercises are harder than it expects or painful, and switched them to alternates (update the repo instructions). I also sometimes tell it I don't feel like doing the proposed exercise and do something else. Or sometimes the stars will align and I'll have *more* energy and I can ask for extra workouts.

I also have it add workouts as needed to help with my goals. For example, I had trouble with leg balance exercises in yoga, and it added lunges and calf raises to make that easier going forward.

No matter what comes up, I don't have to look anything up or think about it[^mi6kq8budqi], I just tell Claude what I do/don't feel like doing and the program gets updated.

The Setup
---------

Since LLMs are stateless but a workout program needs to keep track of things, I used a git repo with Claude Code (via the Android app). I told Claude I wanted to use it as a personal trainer, and it walked me through the setup. Some of the early decisions didn't work very well (Claude wanted a very rigid program that didn't match my ~~laziness~~ schedule; and it really wanted to use heart rate zones from my fitness band, which [don't seem to be accurate for me](https://www.secondnature.io/us/guides/weight-loss-medications/retatrutide-side-effects#heart-rate)), but since everything is code, I just told it what I wanted and had it update CLAUDE.md.

My current program tracks all of the equipment in my home gym (including adjustable dumbbell increments), the exercises in the program and when I last did them (plus a script to find the oldest ones), and logs for every session in case we need them. I also have a script to check the weather (for running) and some validation to keep data in a consistent format.

Your Setup
----------

If this sounds helpful, you could just create a git repo and ask Claude to set it up, but to save time, I also created [a bootstrapping skill](https://gist.github.com/brendanlong/1d86d44963327bc00fb5d845f04770ab) to help avoid the problems I had originally.

Just create a git repo, open it in Claude Code, and tell it:

> Run this skill: [https://gist.github.com/brendanlong/1d86d44963327bc00fb5d845f04770ab](https://gist.github.com/brendanlong/1d86d44963327bc00fb5d845f04770ab)

It should interview you and then set everything up. After that, just open the app whenever you ~~want to~~ can tolerate working out and ask it what to do. And if you don't want to do what it proposes, tell it you want to do something else. It's your repo, customize it for you!

[^wyqfuh3eplg]: I assume this whole setup would work with non-Claude AIs as well, as long as you have a way to run the coding agent mode from your phone, but my only experience using this is with Claude. 

[^mi6kq8budqi]: I know, I know, we're not supposed to outsource all of our thinking to AI, but I hate exercise and the options are "don't think about it and don't do it" or "don't think about it but do what Claude says".