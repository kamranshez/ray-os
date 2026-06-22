---
duration: "8-12 min"
batch: 9
order: 35
batch_name: "Loops In The Wild"
class: "loopy-ai"
chapter: "Write Loops, Not Code"
status: "scripted"
aliases: [write-loops-not-code]
---

The last two loops ran while you were at the keyboard. This one runs while you are asleep.

This is the loop that started the whole conversation, in the words of the man who built Claude Code. He does not write code anymore. He writes loops, and the loops write the code while he sleeps. A widely shared version of the claim puts a number on it: roughly 30 percent of his code is now fully written by loops.
Source: https://x.com/0xMovez

This is a routine from the command and control chapter. While I am gone, not while I am here.

---

## The problem it kills

Your pull requests rot overnight, and you spend your morning unrotting them.

The build went red after a dependency moved. A reviewer left three comments you have not answered. A branch went stale against main while you slept. None of it is hard. All of it is the boring tax you pay before you can do real work, and you pay it every single morning with your freshest hours.

A routine pays that tax for you, on a schedule, in the dark.

---

## The loop

The shape is a scheduled routine pointed at your open PRs, the kind of overnight worker that wakes you to finished work instead of a chore list.

```
/schedule every night, watch my open PRs. Auto-fix build failures, answer review comments in a fresh worktree, and rebase what is stale. Leave anything ambiguous for me. State in git so a crash loses nothing.
```

Three verbs, and the difference between them is the whole toolbox. `/goal` runs until an outcome is true, then stops. `/loop` repeats while your session is open, while you are here. `/schedule` runs while your laptop is closed, while you are gone. This command is the third one, and "while you are gone" is precisely why it is worth building.

[IMAGE: dark canvas, a sleeping human icon on the left, a moon and a clock showing night, a routine box in the middle reading "watch open PRs", three small worker arrows coming out labeled "fix build", "answer comments", "rebase", and a stack of green PRs waiting on the right under a rising sun]

![[loopy-litw-write-loops-not-code.png]]

---

## Why it works: the worktree and the state line

Two clauses in that command are what separate a routine you can trust from one that wrecks your repo at 3am.

"In a fresh worktree" is isolation. The routine does its overnight work on its own checkout, not on top of whatever you left in your working tree. So it can answer comments and fix builds across several PRs at once without any of them stepping on each other or on you.

"State in git so a crash loses nothing" is the part nobody thinks about until it bites them. An unattended loop will eventually die mid-run, on a timeout, a rate limit, a power blip. If its progress lives only in memory, a crash at 4am means you wake to nothing. If its progress is committed as it goes, a crash just means it picks up from the last commit. Durable state is what makes "while you are gone" safe.

---

## The leash: leave the ambiguous for me

"Leave anything ambiguous for me" is the autonomy dial, set deliberately.

This routine is allowed to act on the unambiguous: a red build, a stale branch, a review comment with one obvious answer. The moment it hits something that needs a judgment call, it stops and queues it for you instead of guessing. That is the line between a routine that compounds and one that quietly ships bad decisions all night.

You wake up to two piles. A pile of finished work it was safe to finish, and a short pile of decisions only you can make. The second pile is where your morning actually starts, and it is a fraction of what it used to be.

---

## Demo

Run the routine on a real set of open PRs.

1. Show the schedule. The routine is set to fire overnight. Same scheduled-task primitive from the command and control chapter, pointed at your PR list.

2. Show one PR with a red build. The routine spins a fresh worktree, reproduces the failure, fixes it, pushes. Point at the worktree: your actual checkout never moved.

3. Show one PR with review comments. The routine answers the straightforward ones in the worktree and pushes the replies. Then show it hit an ambiguous comment, stop, and file it to your morning queue instead of guessing.

4. Kill it mid-run on purpose. Stop the process halfway, then restart it. Show it resume from the last commit, not from zero. That is the state-in-git clause earning its place.

5. Cut to morning. One Slack summary: PRs it cleared overnight, and the short list of decisions waiting for you.

Total demo: four minutes. The point is that the boring tax got paid while you slept, and you woke up to choices, not chores.

---

## Key Insight

> Stop being the thing in the loop. Write the routine, give it isolation and durable state, and wake up to finished work instead of a morning of chores.

---

## Where we go next

So far every loop in this chapter has been well behaved. The next one is about the loops that are not, the ones that spin forever, burn money, and never notice they are stuck.
