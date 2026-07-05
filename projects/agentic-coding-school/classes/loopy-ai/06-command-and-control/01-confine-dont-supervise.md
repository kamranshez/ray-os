---
video_id: "QbY_v6zs"
duration: "12-16 min"
batch: 5
order: 14
batch_name: "Command & Control"
class: "loopy-ai"
chapter: "Command & Control"
aliases: [confine-dont-supervise, the-autonomy-dial]
---
The safest unattended coding agent in the world runs with full permissions and never asks you for anything. No confirmation prompts. No "are you sure." It just runs.

That should sound reckless. It isn't. And the reason it isn't is the whole point of this video.

You do not make a loop safe by watching it more carefully. You make it safe by putting it somewhere it cannot do damage. **Confine it, don't supervise it.**

[IMAGE: dark canvas, two ways to make a loop safe side by side. Left, a tired human eye watching an agent, labeled "supervise: watch it harder", the agent still able to reach dangerous objects around it. Right, the same agent dropped inside a sealed box labeled "confine: put it where it cannot do damage", running wide open while the dangerous objects sit outside the wall. Caption: "confine it, don't supervise it".]
![[loopy-confine-dont-supervise-intro-v1-1.png]]
![[loopy-confine-dont-supervise-intro-v1-2.png]]
![[loopy-confine-dont-supervise-intro-v1-3.png]]
![[loopy-confine-dont-supervise-intro-v1-4.png]]
![[loopy-confine-dont-supervise-intro-v1-5.png]]

---

## The thing everyone does wrong

Watch what happens the first time you let a loop off the leash.

You start cautious. You make it ask before every action. Reformat a file? Confirm. Move a draft? Confirm. You sit there approving the obvious, and the autonomy you built was a lie. You're babysitting.

So you loosen it. You pass the skip-permissions flag, you walk away, you let it run. And one morning the loop has force-pushed the branch, or emailed the client, or spent real money, and now you're not babysitting, you're explaining yourself.

Here's the mistake underneath both. You're trying to control the loop by controlling its *judgment*. Asking it nicely, in a policy or a prompt, to please not do the dangerous thing. That's supervision, and supervision has two failure modes that are really one: you either supervise too much and babysit, or too little and get burned.

And it gets worse, because of *where* the loop is running.

[IMAGE: dark canvas, a laptop in the center labeled "your machine", an agent inside it with tentacles reaching out to grab labeled objects around it: SSH keys, prod credentials, a logged-in browser session, ~/.aws, a production database. The point is one agent touching everything you care about.]
![[loopy-confine-dont-supervise-laptop-blast-radius-1.png]]
![[loopy-confine-dont-supervise-laptop-blast-radius-2.png]]
![[loopy-confine-dont-supervise-laptop-blast-radius-3.png]]
![[loopy-confine-dont-supervise-laptop-blast-radius-4.png]]
![[loopy-confine-dont-supervise-laptop-blast-radius-5.png]]

Your laptop is the single worst place to run an unattended loop. It's the one machine that has your SSH keys, your production credentials, your logged-in browser, your cloud tokens, all in reach. You gave the loop full permissions to save yourself the prompts, and full permissions on *that* machine means the blast radius is your entire digital life.

So you go back to supervising. And the cycle repeats.x

---

## Soft control versus hard control

There are two completely different ways to stop a loop from doing something.

The first is to ask it not to. Write a rule in the intent doc. "Don't send email. Don't push to main." The loop reads the rule, and you trust it to obey. That's **soft control**. It depends on the model's judgment, and the model's judgment fails in three predictable ways. It misreads what's reversible. It gets prompt-injected by something it reads on the internet. Or it just decides, plausibly and confidently, that this particular email is fine to send.

The second way is to make the dangerous thing impossible. The loop cannot send email because it has no email tool. It cannot reach production because the machine it runs on has no network path to production. That's **hard control**. There is no judgment to trust, because there is no capability to misuse.

[IMAGE: dark canvas, two panels. Left panel "Soft control": a sticky note that says "please don't send email" taped to an agent, a dotted line to an email action that's still clearly reachable. Right panel "Hard control": the same agent in a sealed box with no email tool at all, the email action physically outside the wall. Contrast between asking and removing.]
![[loopy-confine-dont-supervise-soft-vs-hard-1.png]]
![[loopy-confine-dont-supervise-soft-vs-hard-2.png]]
![[loopy-confine-dont-supervise-soft-vs-hard-3.png]]
![[loopy-confine-dont-supervise-soft-vs-hard-4.png]]
![[loopy-confine-dont-supervise-soft-vs-hard-5.png]]

This is the whole reframe. Stop writing rules that ask the loop to behave. Start building boxes the loop cannot behave badly *in*. The most autonomous loop is the most confined one, because confinement is the only thing that lets you genuinely stop watching.

---

## Stripe runs 1,300 agents a week this way

This isn't theory. It's how Stripe ships code.

Stripe runs homegrown unattended coding agents they call minions. Over 1,300 pull requests merged every week are fully minion-produced, human-reviewed, but containing no human-written code. A company moving more than a trillion dollars a year lets agents write its code start to finish.

Source: https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents

And here's the line that matters, in their own words:

> The quarantined devbox environment means that the agent doesn't need confirmation prompts. Any mistakes an agent might make are confined to the limited blast radius of one devbox, so we can safely run the agent with full permissions and skip confirmation prompts.

Read that again. Full permissions. No confirmation prompts. *Safely.* Stripe does the exact opposite of supervising their agents. They don't sit over the loop's shoulder approving actions. They drop it into a sealed box and let it run wide open.

[IMAGE: dark canvas, an agent running wide open inside a sealed box labeled "devbox", happily using full permissions inside. The walls of the box are solid and labeled "no production access" and "no internet egress". Outside the box, greyed out and unreachable: prod database, real user data, the open internet.]
![[loopy-confine-dont-supervise-sealed-box-1.png]]
![[loopy-confine-dont-supervise-sealed-box-2.png]]
![[loopy-confine-dont-supervise-sealed-box-3.png]]
![[loopy-confine-dont-supervise-sealed-box-4.png]]
![[loopy-confine-dont-supervise-sealed-box-5.png]]

The box is a fresh developer machine, isolated from production and from the open internet, with no real user data on it. The agent has full power *inside* the box, and the box can't touch anything that matters. The worst thing a minion can do is mess up its own throwaway machine, which Stripe deletes anyway.

That's the trade. You give up supervision, and in return you get a hard wall around the blast radius. Wide-open autonomy, zero risk to production, because the two were never actually connected.

---

## You already have a sealed box. It's an SSH connection.

You might be thinking this is Stripe-scale infrastructure you'll never build. You don't need it.

The accessible version is one command. Spin up a cheap cloud machine, a throwaway VPS or a fresh container, and SSH into it. Run your loop *there*, not on your laptop. That's it. That's the box.

[IMAGE: dark canvas, flow left to right. Your laptop on the left (with its SSH keys and prod creds drawn small and protected behind it), an SSH arrow crossing a gap to a remote cloud box on the right where the agent actually runs. The agent is clearly on the far side of the gap, nowhere near the laptop's secrets.]
![[loopy-confine-dont-supervise-ssh-devbox-1.png]]
![[loopy-confine-dont-supervise-ssh-devbox-2.png]]
![[loopy-confine-dont-supervise-ssh-devbox-3.png]]
![[loopy-confine-dont-supervise-ssh-devbox-4.png]]
![[loopy-confine-dont-supervise-ssh-devbox-5.png]]

The moment the loop runs on a remote box you SSH into, the math changes. It's not on the machine with your credentials. It only has the tools and keys you deliberately put on *that* box, which is nothing by default. If it goes haywire, you close the connection and destroy the machine. Nothing it did can reach you, because there was never a path home.

This is why "just SSH into a devbox" is the single most practical safety move in this whole class. It costs you a few dollars and a few minutes, and it converts "I have to watch this loop" into "I can let this loop run." Run the same task lifecycle from [[task-lifecycle-loop]] inside that box instead of on your machine, and the lifecycle didn't change at all. Only its blast radius did.

---

## The three walls of the box

Confinement isn't one move. It's three, stacked, from strongest to softest.

**Wall one, the environment.** This is the big one. The machine itself has no path to anything dangerous. No production access. No real data. No arbitrary network egress, just an allowlist of the specific domains the task actually needs. Stripe's minions run in their QA environment for exactly this reason. The loop can't email your investors because the box can't reach a mail server, full stop.

**Wall two, the tools.** Give the loop the minimum set of tools the job requires, and nothing else. Stripe built a central tool server with nearly 500 tools, and then hands each agent a deliberately small subset. Their words: agents perform best when given a smaller box with a tastefully curated set of tools. Default to read-only tools wherever you possibly can. A loop that can only read is almost unconditionally safe to run unattended.

**Wall three, the output.** When the loop must produce something that changes the world, it doesn't change the world. It produces a *proposal*. A minion's only output is a pull request a human opens. The dangerous action, merging code that ships to production, never lives inside the loop at all. It lives at one human gate, outside the box.

[IMAGE: dark canvas, three concentric walls around an agent at the center. Inner wall labeled "tools: minimum, read-only first", middle wall labeled "environment: no prod, no egress", and the output crossing the outer boundary as a single "PR" arrow passing through a gate labeled "human opens it". Nesting from agent outward.]
![[loopy-confine-dont-supervise-three-walls-1.png]]
![[loopy-confine-dont-supervise-three-walls-2.png]]
![[loopy-confine-dont-supervise-three-walls-3.png]]
![[loopy-confine-dont-supervise-three-walls-4.png]]
![[loopy-confine-dont-supervise-three-walls-5.png]]

Notice what these three have in common. None of them ask the loop to behave. The environment removes the path. The toolset removes the capability. The output split removes the authority. You're not trusting the model's judgment at any point. You're removing the need for it.

---

## This is the proposer and applier split

Wall three deserves its own beat, because it's the move that makes confinement practical.

A fully sealed, read-only loop is perfectly safe and also can't ship anything. So you split the work in two. A **proposer** runs wide open inside the box, reads everything, reasons freely, and produces a candidate: a diff, a draft, a plan. Then a separate, narrow **applier** is the only thing that can act on the proposal, and that applier is either a human clicking merge or a tightly scoped step you trust.

[IMAGE: dark canvas, flow. A wide, busy "proposer" agent inside a sealed box on the left, full permissions, lots of activity, output is a single artifact labeled "PR / draft". An arrow carries the artifact out through a narrow gate labeled "applier (human or scoped step)" to the protected world on the right (prod, send, deploy). The proposer is big and free, the applier is small and guarded.]
![[loopy-confine-dont-supervise-proposer-applier-1.png]]
![[loopy-confine-dont-supervise-proposer-applier-2.png]]
![[loopy-confine-dont-supervise-proposer-applier-3.png]]
![[loopy-confine-dont-supervise-proposer-applier-4.png]]
![[loopy-confine-dont-supervise-proposer-applier-5.png]]

All the dangerous capability collects at one small, watched place. The loop gets to be as autonomous as you like, because the part of it that could hurt you was lifted out and handed to the gate. This is the practical shape of almost every safe unattended loop you'll build. Wide-open proposer, narrow applier.

---

## Don't confuse the box with the brake

Two things in this class sound like they do the same job, and they don't.

[[governance-primitives]] gave you a brake. A kill switch that stops a misbehaving loop after it's already running and already going wrong. That's reactive. You, or a monitor, notice the problem and pull the cord.

The box is different. The box is preventive. It stops the harm before the loop ever acts, because the harmful action was never possible inside the box. You don't have to notice anything. You don't have to react in time.

You want both, and they work at different altitudes. The brake stops the fleet when something slips through. The box makes sure almost nothing can slip through in the first place. Confine first, so the brake is a backstop you rarely need, not a thing you're standing on all day.

And keep this separate from the autonomy *ladder* from [[l1-essentials]], because the words blur together. The ladder is about *how long* a loop runs unattended. Duration. The box is about *what a loop can touch* while it runs. Capability. A loop that runs for a month inside a tight box is safe. A loop that runs for ten minutes on your laptop with full access can still email your investors in those ten minutes. High on the ladder isn't the scary part. No box is the scary part.

[IMAGE: dark canvas, two panels. Left "the brake (reactive)": a loop already running and going wrong, a hand pulling a kill-switch cord after the fact, labeled "stops it after it acts". Right "the box (preventive)": the same loop sealed in a box, the harmful action greyed out and unreachable, labeled "harm was never possible". A small note underneath both: "confine first, the brake is the backstop you rarely need". Caption: "the box prevents, the brake reacts".]
![[loopy-confine-dont-supervise-don-t-confuse-the-box-with-the-brake-v1-1.png]]
![[loopy-confine-dont-supervise-don-t-confuse-the-box-with-the-brake-v1-2.png]]
![[loopy-confine-dont-supervise-don-t-confuse-the-box-with-the-brake-v1-3.png]]
![[loopy-confine-dont-supervise-don-t-confuse-the-box-with-the-brake-v1-4.png]]
![[loopy-confine-dont-supervise-don-t-confuse-the-box-with-the-brake-v1-5.png]]

---

## How you tune it

You don't set the box once. You widen it as trust accrues, and you widen the *box*, never the supervision.

Start a new loop as tight as it can possibly be and still do the job. Read-only tools. Sealed environment. Output is a proposal you review. Watch it work. As the proposals come back good, run after run, you earn the right to widen a wall. Let it write inside the box without asking. Add the one extra tool it kept needing. Eventually, for the cheap reversible stuff, let a narrow applier act without you.

[IMAGE: dark canvas, a ratchet or a box growing outward in labeled steps over time: "read-only + review every output" to "write inside box" to "+ one more tool" to "narrow auto-apply for reversible work". Arrow of time underneath, only ever widening, with a small note "the box widens, supervision never returns".]
![[loopy-confine-dont-supervise-trust-ratchet-1.png]]
![[loopy-confine-dont-supervise-trust-ratchet-2.png]]
![[loopy-confine-dont-supervise-trust-ratchet-3.png]]
![[loopy-confine-dont-supervise-trust-ratchet-4.png]]
![[loopy-confine-dont-supervise-trust-ratchet-5.png]]

The direction only ever goes one way. You're trading a wall of the box for a piece of trust you've actually earned with evidence. You are never trading it back for sitting and watching. The day you find yourself supervising again is the day to ask which wall you should have built instead.

---

## Failure modes

Five ways people get this wrong, and you'll recognise most of them from the cycle we opened with.

**Running it on your laptop.** The original sin. The one machine with all your secrets is the one machine the loop should never run on. Move it to a box you SSH into.

**Granting full tools "to be safe."** Backwards. Every tool you add is a wall you removed. Minimum set, read-only first, widen later.

**Trusting the model to refuse.** Writing "don't push to main" in a prompt and walking away. That's soft control, and the model will eventually, confidently, push to main. If it must never happen, remove the capability, don't request restraint.

**A box with a door to production.** A confined machine that still has prod credentials sitting on it, or open network egress, isn't confined. The wall has to actually be a wall. No real data, no prod path, allowlist the egress.

**No applier gate.** Letting the proposer also be the thing that merges and deploys. The whole point was to lift the dangerous action out to one watched place. If the loop can ship straight to prod, you built a fast way to break prod.

[IMAGE: dark canvas, five failure cards in a row, each a small wrong sketch with a red X and a green "fix" arrow beneath it: "runs on your laptop -> move to an SSH box", "full tools to be safe -> minimum set, read-only first", "trusting the model to refuse -> remove the capability", "a box with a door to prod -> no creds, no egress", "no applier gate -> proposer cannot merge". Caption: "every failure here is a wall someone skipped".]
![[loopy-confine-dont-supervise-failure-modes-v1-1.png]]
![[loopy-confine-dont-supervise-failure-modes-v1-2.png]]
![[loopy-confine-dont-supervise-failure-modes-v1-3.png]]
![[loopy-confine-dont-supervise-failure-modes-v1-4.png]]
![[loopy-confine-dont-supervise-failure-modes-v1-5.png]]

---

## Demo

Open a terminal. The whole demo is one loop, run somewhere it can't hurt you.

1. **Spin up the box.** Start a fresh cloud VM or container and SSH into it. Show that it's empty: no production credentials, no real data, nothing on it but the repo and the agent.

2. **Scope the walls.** Hand the loop a deliberately small toolset, read-only over the codebase plus the one or two tools the task needs. Set the network so it can reach the package registry and nothing else. Say out loud: it physically cannot reach production from here.

3. **Run it wide open.** Give the task and pass full permissions, no confirmation prompts, exactly like Stripe. Let it work start to finish with you not touching anything. Point out that you are not approving a single action, and that's correct, because of where it's running.

4. **Prove the wall.** Ask the loop, or just try it yourself on the box, to hit the production database or send an external request to a non-allowlisted domain. Watch it fail. The wall is real. This is the moment the whole idea lands on camera.

5. **Collect the proposal.** The loop finishes by pushing a branch and opening a pull request. The dangerous step, merging, is yours. You review the diff and you decide. Then close the connection and destroy the box.

6. **Now do it five times.** Kick off five of these in five separate boxes at once. Five loops running wide open in parallel, five PRs waiting for you, zero risk to anything you care about. That's what confinement buys: not one careful loop you babysit, but a fleet you don't have to.

---

## Key Insight

> You don't make a loop safe by supervising it harder. You make it safe by putting it where it cannot do harm, and then letting it run wide open. The most autonomous loop is the most confined one.

---

## Where we go next

The box decides what a loop *can* touch. The next video is where the confined fleet reports, learns, and coordinates: [[slack-as-your-command-center]]. One channel per routine, where the loop posts its decisions as something you can correct in one tap, where that single reaction is the only signal it needs, and where the next run reads everything that happened while you were away. No approve buttons, because a confined loop never has to ask.

And it pairs with the brake from [[governance-primitives]] and the comms pipe from [[keeping-you-in-the-loop]]. The box prevents harm, the brake stops what slips through, and the pipe carries what's left to you. Build the box first. Everything else gets easier once the loop has nowhere dangerous to stand. See you in the next one.
