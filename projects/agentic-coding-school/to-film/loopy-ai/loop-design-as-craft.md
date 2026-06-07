---
duration: "10-14 min"
batch: 5
order: 2
batch_name: "Closing"
class: "loopy-ai"
chapter: "Where Taste Went"
---

Boris said product taste is the alpha today, but it's going to go away too.

He's half right. Taste doesn't go away. It moves.

This segment is where it went, why most people will miss the move, and what to do about it.

This is the closing argument of the class. Watch this one even if you skipped the middle.

Source: Boris Cherny on Acquired Unplugged, June 2026.

---

## The claim

Old taste lived in single judgments. New taste lives in criteria, thresholds, and rubrics. The standing rules a loop applies thousands of times.

That's a different cognitive skill.

Some people who had great craft taste will be bad at rubric taste. Because rubric taste requires articulating what was previously intuitive. And most senior people would rather make a hundred individual judgments than write down the one rule that captures the same taste.

[IMAGE: split panel. Left side a single person at a desk making one decision. Right side the same person, but their judgment encoded as a rubric on a screen that's running across hundreds of items in parallel]

![[images/loop-design-as-craft/old-vs-new-taste.png]]

---

## Three pairs that show the shift

### Anki cards

**Old taste.** You write one great Anki card. You know this sentence is the right length. You know this gloss is the right depth. You know this audio cue is the right cut point.

You can't fully explain why. You just know.

**New taste.** You decide what makes a card *worth your future attention*.

Which sources count. A Tokyo Ghoul rewatch, yes. A random Shorts compilation, no.

Daily cap. Twenty new cards is energising. Eighty is depressing.

Which i plus one sentences are *worth* learning, versus just technically i plus one. A sentence with three rare loanwords passes the filter but isn't useful.

The first taste is craft. The second is policy.

### Thumbnail picking

**Old taste.** Which thumbnail to pick from the three the designer sent.

**New taste.** Which *lessons* from yesterday's A/B test should shape tomorrow's hypothesis space.

Was the winner winning because of contrast? Or because the topic itself was hot? Opposite next moves. Get this wrong and the next ten thumbnails iterate on the wrong axis.

### Code review

**Old taste.** Spotting the bug in this PR.

**New taste.** Setting the threshold at which the review agent posts a finding. And the feedback signal it uses to self tune that threshold over the next hundred PRs.

[IMAGE: three side by side panels, each showing old taste on top and new taste below, with the same person in both]

![[images/loop-design-as-craft/three-pairs.png]]

---

## Why the move is hard

Articulating a rubric forces you to do the thing every senior person hates. Write down the implicit knowledge that made you senior in the first place.

This is the same reason senior engineers struggle to write good documentation. The intuitions feel obvious. They feel like they don't need to be said. Until you try to encode them, and you realise half of your "obvious" intuitions are actually wrong, and the other half have hidden criteria you've never made explicit.

So there's a sorting function happening here.

People who can compress their taste into rubrics will scale by a hundred times. Their judgment runs across hundreds of loops, applied thousands of times a day.

People who can't will keep doing one times work at a higher abstraction layer, and wonder why they feel slower.

The painful part is that this isn't a fairness issue. The people with the most refined taste are often the ones least able to articulate it. They got to where they are by trusting their gut, not by writing down rules.

The class can teach the skill. But it can't make people willing to learn it.

---

## Three drills to practise

These are the exercises that build rubric taste. Do them on something you actually care about. They don't work as toy problems.

**Drill one. Articulate one current intuition as a rubric.**

Pick something you "just know" in your domain. Write it as three to five criteria with thresholds.

Test it. Take ten recent cases where you applied this intuition. Run the rubric over them on paper. Does it reproduce your judgment eighty percent of the time?

If not, the rubric is wrong. Or the intuition is wrong. Or there are hidden criteria you haven't surfaced yet.

You don't know which one until you write it down.

**Drill two. Find the false negative.**

Every rubric has a class of cases where it fails silently. Find one.

Add a fallback. Or an escalation path. Or a manual override for that class.

This is the loop equivalent of a property based test. You're not testing the rubric against examples. You're testing it against the *class of examples* you know it will get wrong.

**Drill three. Watch a loop run for a week. Read every action.**

Not a summary. Every action.

Update the rubric.

This is the new code review. The artifact is not the prompt. It's the action log.

If you can't bring yourself to read the action log, you don't trust the loop. And you shouldn't. Loops you don't read drift, and you only notice when something has been wrong for a month.

[IMAGE: three drill cards stacked vertically, each with a title and a one line outcome]

![[images/loop-design-as-craft/three-drills.png]]

---

## The terminal role

Boris said the role becomes "builder." Not engineer, not PM, not designer. Just builder.

He's directionally right. He's missing one rung.

The terminal role is **loop curator** for a specific domain.

Loop curator for SEO.

Loop curator for invoice reconciliation.

Loop curator for L4 oncall.

Loop curator for a YouTube channel.

Each curator owns the rubrics, the kill switches, the token budgets, the escalation paths, the integration surface, the action log review cadence.

Specialisation always returns once a new abstraction matures. Right now everyone is a generalist builder because the abstraction is new. In two years there will be people whose entire job is curating the loops that run a specific function of a specific kind of company.

That's not a worse role. That's a deeper role.

The "member of technical staff" title is a transitional artifact. Don't tie your identity to it.

---

## What this class is really teaching

Not how to write loops. That's the surface.

What it's teaching is how to compress intuition into rules a fleet can run without you in the room.

Whether you stay close to your craft and use loops to scale it, or whether you get out of your craft entirely and use loops to do it for you, that's a values question, not a skill question.

Be honest with yourself about which one you want. The skill works either way. The life is different.

---

## Lines to take with you

Pull any of these out as a tweet. They're the through line of the class.

> The prompt is the easy part. The control surface is the work.

> Old taste was in single judgments. New taste is in rubrics.

> Loops are the unit of production. Rubrics are the unit of taste.

> If you can't articulate your taste, the fleet can't apply it. You're capped at one times.

> The next moat isn't a better model. It's the cleanest pipe into your decision surface.

> Token budget allocation is the new headcount allocation.

> Status meetings die before standups do.

---

## Demo

Open one of your existing loops on screen. Show its rubric, plainly written, in a markdown file or in the system prompt.

Read it out loud, slowly. Acknowledge how unromantic it is. A few lines of criteria with thresholds. No magic.

Then show the action log for the past week. Scroll through it on screen. Point at one item the rubric got wrong. Edit the rubric live on camera to add the missing criterion. Save. Show the next iteration of the loop picking up the new rubric and applying it.

Close the demo: "That's the work. That's where taste lives now."

Total demo: three minutes. The slowness is the point. People need to see how unglamorous and how powerful this actually is.

---

## Key Insight

> Old taste lived in single judgments. New taste lives in rubrics. The people who can move their taste from one to the other will scale by a hundred times. The rest will stay at one times and wonder why.

---

## Closing

You came into this class thinking a loop was one thing.

You're leaving knowing there are eight levels. You know which level you're at. You know which level you want to reach. You have the vocabulary to argue about loop design with someone who actually thinks about it. And you've built one running loop on your own work that's still going when you close your laptop.

That's the class.

The harder work starts now. Take one of the drills above and run it this week. Pick something you "just know" and try to write it down. See what breaks.

That's where the next ten times of your career hides. Go find it.
