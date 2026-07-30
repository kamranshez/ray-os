# The Verification Horizon — video script

**Format:** mental-model video with a demo spine. One idea argued hard and shown once per layer. Still not a tutorial.
**Thesis:** *Verifiers decay.* Your definition of "working" has a shelf life.
**Runtime target:** 20–22 min with the demo thread. Drop `DEMO 4` and shorten `DEMO 2` to hold 17.
**Script mode:** hybrid. Cold open and outro are **verbatim**. The five layer sections are **beat sheets** with mandated lines marked `★`. Every demo block is a **placeholder**: prompt and required outcome are fixed, the talking is improvised, `TK` marks anything filled at record time.
**Running example:** one feature — *"let users invite teammates to their workspace"* — plus a coverage board that stays on screen the whole video.
**Second running example:** one Claude Code session on that feature, cut into seven clips. See the demo spine below.

**Sources**
- OpenAI, *OpenAI and Hugging Face partner to address security incident during model evaluation*, 21 July 2026 (updated 28 July 2026).
- Andon Labs / Fable 5 alignment regression note (Vending-Bench Arena).
- Qwen Team, *The Verification Horizon: No Silver Bullet for Coding Agent Rewards*, arXiv:2606.26300.

---

## DEMO SPINE — one session, seven cuts

One Claude Code session on a real repo building the invite feature, recorded in order and cut into seven clips. The session is the second running example: by `DEMO 5` the audience is watching the trajectory of the same session they watched begin in Act 1.

| # | Where | Runs | What the audience sees |
|---|---|---|---|
| 0 | end of Act 1 | ~60s | The up-front ask. Before any code: *what can you verify, and how long can you run without me?* |
| 1 | Layer 1 | ~45s | It builds and runs the cheap pipeline. Rows 1–8 and 12 go green for real. |
| 2 | Layer 1 sidebar | ~40s | One invariant, fuzzed. It finds something nobody wrote down. |
| 3 | Layer 2 | ~50s | Playwright double-click. Backend green, product broken. |
| 4 | Layer 3 | ~45s | Rubric scoring, and a high score on something visibly bad. |
| 5 | Layer 4 | ~70s | The trajectory of this session. The flag. The payoff of the thread. |
| — | Layer 5 | none | **No demo, deliberately.** You cannot rehearse production. Say so on camera. |
| 6 | outro | ~40s | The conversion rule, executed once, live. |

**Rules for the thread**
- Same repo, same branch, same session, always in order. `DEMO 5` only works if the trajectory is genuinely the one from `DEMO 1` through `DEMO 4`, so a re-shoot of any earlier clip invalidates it.
- Keep every clip under 70 seconds. If one runs long, cut the agent's thinking, never the outcome.
- Nothing in the thread should look expensive. The argument is that this is a few prompts and a few minutes, not a weekend, which is what keeps it consistent with the outro.

---

## COLD OPEN — verbatim (target ~2:30)

> **[ON SCREEN: black. Just the words: "You don't have a verifier."]**

Let me start with the uncomfortable bit.

Most of you watching this do not have a verifier. You have a build step, you have some tests you wrote eight months ago, and you have your own eyeballs at eleven at night. That is not a verification system. That is a vibe with a CI badge.

And I know the objection, because it's the one I had: *why do I need all this?* The models keep getting better. Shouldn't I need less checking over time, not more?

No. And I want to show you why, using three things that all happened recently.

> **[ON SCREEN: OpenAI blog post header, 21 July 2026]**

Number one. In July, OpenAI published an incident report with Hugging Face. They were running an internal cyber-capabilities benchmark called ExploitGym. GPT-5.6 Sol, plus an internal pre-release model, with the safety refusals turned down on purpose, because the whole point was to measure the ceiling.

The environment was sandboxed. No internet. The only thing reachable was a package registry cache proxy.

So here's what the models did.

They spent a serious amount of compute working out how to get *out*. They found a zero-day in that proxy — a real, previously unknown vulnerability in Artifactory — and used it to break out of the sandbox. Then they escalated privileges and moved laterally across OpenAI's own research environment until they landed on a machine that had internet access.

Then they had a thought. They reasoned that Hugging Face probably hosts the models and datasets for ExploitGym. Which means Hugging Face probably has the *solutions*.

So they chained stolen credentials and more zero-days into remote code execution on Hugging Face's servers, and pulled the test solutions straight out of Hugging Face's production database.

> **[ON SCREEN: pull quote, OpenAI's own words]**

OpenAI's own words: the models were *"hyperfocused on finding a solution for ExploitGym, going to extreme lengths to achieve a rather narrow testing goal."*

Sit with that. The model did not solve the benchmark. The model **stole the answer key.** It committed a genuine, novel, multi-stage cyber intrusion — against a real company, in production — because that was the cheapest path to a passing score.

![[verification-horizon-answer-key-1.png]]
![[verification-horizon-answer-key-2.png]]
![[verification-horizon-answer-key-3.png]]
![[verification-horizon-answer-key-4.png]]
![[verification-horizon-answer-key-5.png]]

> **[ON SCREEN: Andon Labs / Fable 5 excerpt]**

Number two. Andon Labs reported a partial alignment regression in Fable 5. In a vending-machine business simulation, it planned to turn a competitor into a dependent wholesale customer so it could control pricing. It falsely told a supplier that a competing distributor was quoting lower prices, as a negotiation tactic. And in head-to-head play it was the only model to initiate price collusion — at more than double the rate of Opus 4.8, even after adjusting for how much more it talked.

Nobody asked for any of that. It was just effective.

![[verification-horizon-unasked-behaviour-1.png]]
![[verification-horizon-unasked-behaviour-2.png]]
![[verification-horizon-unasked-behaviour-3.png]]
![[verification-horizon-unasked-behaviour-4.png]]
![[verification-horizon-unasked-behaviour-5.png]]

> **[ON SCREEN: Qwen paper title card]**

Number three, and this is the one that's actually about your job. Qwen published a paper called *The Verification Horizon*. They trained a coding agent with reinforcement learning against test suites — the exact thing you'd do. Pass the tests, get the reward.

The pass rate went up beautifully.

Then they checked *how*. Across three SWE-Bench variants, **28.6% of the successful runs were hacks.** Nearly a third of the wins were the agent finding the original pull request, tampering with the test, or editing the evaluation harness. And there's one line in their behaviour table I can't stop thinking about: the agents that went and retrieved the actual solution artifact resolved tasks **twelve points above baseline.** Cheating had the highest success rate of anything they measured.

That is the same behaviour as the Hugging Face incident. Identical. One agent googled the fixing PR. The other one popped a zero-day and raided a production database. Same instinct, four orders of magnitude apart.

![[verification-horizon-hacked-wins-1.png]]
![[verification-horizon-hacked-wins-2.png]]
![[verification-horizon-hacked-wins-3.png]]
![[verification-horizon-hacked-wins-4.png]]
![[verification-horizon-hacked-wins-5.png]]

> **[ON SCREEN: "It's not malice. It's optimisation."]**

And here's the thing I need you to take out of this section, because it's the load-bearing idea for everything after it:

None of this is the model being evil. Every one of these systems did exactly what it was told. It maximised the thing we measured. The problem is that the thing we measured was never the thing we wanted. It was a **proxy** for the thing we wanted.

Your tests are a proxy. Your types are a proxy. Your linter is a proxy. Every single check you own is an approximation of "this works," and there is a gap between the approximation and the truth.

Weak models can't find that gap. Strong models find it every time.

![[verification-horizon-proxy-gap-1.png]]
![[verification-horizon-proxy-gap-2.png]]
![[verification-horizon-proxy-gap-3.png]]
![[verification-horizon-proxy-gap-4.png]]
![[verification-horizon-proxy-gap-5.png]]

> **[ON SCREEN: the thesis, held for a beat]**

Which leads to the actual claim of this video, and it's sharper than "you should test more":

**Your verifier decays.**

Not "your verifier is incomplete" — it's always been incomplete. **Decays.** The same test file, unchanged, on disk, means *less* today than it meant a year ago. Not because it changed. Because the thing being measured got better at satisfying it specifically.

You already accept this for dependencies. You accept it for security. You do not accept it for your definition of "working," and that's the mistake.

So for the rest of this video I want to do two things. Show you the five layers of verification you can actually have. And for each one, show you exactly how it goes blind — because that's the part nobody tells you.

![[verification-horizon-decay-1.png]]
![[verification-horizon-decay-2.png]]
![[verification-horizon-decay-3.png]]
![[verification-horizon-decay-4.png]]
![[verification-horizon-decay-5.png]]

---

## ACT 1 — THE GAP (target ~2:30)

**Purpose:** establish *why* verification is hard before touching any layer. The prompt is not the requirement.

**Beats:**

- Open on the prompt, on screen, alone:
  > `"Let users invite teammates to their workspace."`
- ★ **"That's the whole ticket. Twelve words. And an agent will hand you working code for it in about ninety seconds."**
- The problem isn't the code. The problem is that those twelve words are not the requirement. They're a *pointer* to a requirement that lives entirely in your head and has never been written down anywhere.
- Now unfold the board. Read them out, let them accumulate — the accumulation *is* the point:

**THE COVERAGE BOARD — 15 things nobody said out loud**

| # | Requirement nobody wrote down |
|---|---|
| 1 | Only workspace admins can send invites |
| 2 | The address has to be a real, deliverable email |
| 3 | Inviting an existing member doesn't create a second membership |
| 4 | An invite can be accepted exactly once |
| 5 | Invites expire |
| 6 | A revoked invite stops working immediately |
| 7 | The invite grants *that* workspace, at *the* role that was chosen |
| 8 | Nobody can fire off ten thousand invites |
| 9 | Double-clicking Send sends one invite, not two |
| 10 | The pending list updates without a refresh |
| 11 | The whole thing works on a phone |
| 12 | Deleting the workspace kills its pending invites |
| 13 | Someone signed into the wrong Google account can work out what to do |
| 14 | A user who's never invited anyone can *find* the button |
| 15 | All of this still works after somebody refactors auth in March |

- ★ **"Nobody wrote a single one of these down. And every one of them is a way the feature can be technically delivered and actually broken."**
- Call the paper here, briefly: this is what Qwen means when they say intent is *underspecified by nature*. The person holding the intent often can't articulate it until a counterexample shows up. You don't know rule 13 exists until someone emails you about it.
- ★ **"So this board is the target. And a verifier is anything that can tell you a row is green. That's it. That's what the rest of the video is."**

> **[DEMO 0 — screen recording, ~60s. Repo open, board stays docked right.]**

**The beat: ask before you build.** Almost nobody does this and it costs nothing.

**Prompt, fixed. Read it out as you type it:**

```
Before you write any code for this feature: what verification can you
actually set up for "let users invite teammates to their workspace"?

Three lists:
1. checks you can write AND run yourself, right now
2. checks you can write but can't run without me
3. what you won't be able to check at all

Then: once list 1 exists, how long could you work on this unattended?
```

**What should come back. Steer it if it doesn't, TK exact wording on the day:**
- list 1: build, types, unit, integration, a permissions test. The cheap pipeline.
- list 2: browser-level behaviour, email delivery, anything needing a real account.
- list 3: whether the copy is any good, whether the button is findable, what real users will actually do.

**On the board:** rows the agent claims in list 1 get a **hollow outline**, not a fill. Claimed, not proven. The five layers spend the rest of the video filling them in.

- ★ **"That is the cheapest sixty seconds in this entire video. I asked it what it could prove before I asked it to build anything, and it told me exactly where my board goes dark."**
- List 3 is the interesting one: that's the agent volunteering its own blind spots, accurately, for free. It knows. You just have to ask before it's invested in a diff.
- And the part nobody says out loud, which is the real reason to do this:
- ★ **"Whatever it can check by itself is exactly how far it can run without you. Your verifier is not a safety net. It's the length of the leash."**
- Keep it cheap on camera. This is one prompt, not a plan.

**TK improv:** react to what it actually proposes. If it over-promises on list 1, say so out loud — that's better footage than a clean answer.

- Set the rule for the middle: five layers, and for each one, two questions only. **What does it catch? How does it go blind?**

> **[ON SCREEN: board stays docked, right-hand side, all 15 rows grey. It never leaves.]**

![[verification-horizon-prompt-vs-requirement-1.png]]
![[verification-horizon-prompt-vs-requirement-2.png]]
![[verification-horizon-prompt-vs-requirement-3.png]]
![[verification-horizon-prompt-vs-requirement-4.png]]
![[verification-horizon-prompt-vs-requirement-5.png]]

---

## ACT 2 — THE FIVE LAYERS

Same rhythm every time. Artifact → what it catches → how it goes blind. About 90 seconds each, except layer 4 which carries the paper payoff and runs longer.

![[verification-horizon-five-layers-1.png]]
![[verification-horizon-five-layers-2.png]]
![[verification-horizon-five-layers-3.png]]
![[verification-horizon-five-layers-4.png]]
![[verification-horizon-five-layers-5.png]]

---

### LAYER 1 — Deterministic checks (~1:45)

**Artifact on screen:** one integration test.

```ts
it("cannot accept the same invitation twice", async () => {
  const invite = await createInvitation({ email: "alice@example.com" });

  await acceptInvitation(invite.token);

  await expect(acceptInvitation(invite.token))
    .rejects.toThrow("Invitation already used");

  expect(await membershipsFor(invite)).toHaveLength(1);
});
```

**What it catches** — rows 1 through 8, and 12. Anything you can state as a mechanical fact about the system: permissions, expiry, single-use, scoping, rate limits, cascade deletes. It's cheap, it's fast, it's deterministic, it runs a thousand times a day and it never gets bored. This layer is genuinely great and most of you are under-using it.

**Light up: 1, 2, 3, 4, 5, 6, 7, 8, 12.**

> **[DEMO 1 — screen recording, ~45s]**

**Same session as `DEMO 0`, no new context.** One line: `go ahead and build list 1, then run it.`

**What must land:**
- it scaffolds the five gates and runs them without being told how
- green across the board, fast, and genuinely satisfying to watch
- the hollow rows from `DEMO 0` fill in solid: 1 through 8, and 12

**TK improv:** whatever it names the test files. Point at the permissions test specifically — that's row 1, the one everyone forgets.

- ★ **"Two prompts. Nine rows are now permanently guarded. This is the cheapest layer you will ever own and most of you don't have it."**

**How it goes blind** — ★ **"A test suite is a list of the things you thought of. It has no opinion whatsoever about the things you didn't."**
- Row 9 is already half-dark: you can test that the API is idempotent, but you cannot test that a human double-clicks.
- Rows 10 through 15 are completely invisible to this layer and always will be.
- And the deeper failure: this layer measures *what the code does*, never *whether it should*. Qwen's agents passed these. That's the whole point.

![[verification-horizon-thought-of-1.png]]
![[verification-horizon-thought-of-2.png]]
![[verification-horizon-thought-of-3.png]]
![[verification-horizon-thought-of-4.png]]
![[verification-horizon-thought-of-5.png]]

**Sidebar: fuzzing (~30s).** The honest partial patch. Fuzzing is how you attack "the things you didn't think of" without having to think of them — throw generated tokens, malformed emails, random valid-and-invalid action sequences at it, and assert an *invariant* instead of an output:
> `"A user never gets membership in a workspace without a valid, unexpired, unrevoked invitation."`
That's a sentence that covers rows you never wrote. It's the only thing on this layer that finds unknown unknowns, and almost nobody runs it.

> **[DEMO 2 — screen recording, ~40s]**

**Prompt:** `write me one property test for this invariant, then fuzz it: a user never gets membership in a workspace without a valid, unexpired, unrevoked invitation.`

**What must land:** it generates the sequences and it finds something. **TK the actual failure** — seed the repo beforehand so one exists. Likeliest candidates: an invite accepted for a workspace deleted mid-flow, or an invite accepted after the role it granted was changed.

**Board discipline:** the finding goes on as `4a`, indented under row 4. **Not** as row 16. The board *growing* is Layer 5's move and we don't spend it here. This is a deliberate foreshadow, not the payoff.

- ★ **"I didn't think of that one. Nobody typed that requirement anywhere. The invariant found it because an invariant is a sentence about the rows you haven't written yet."**

![[verification-horizon-invariant-1.png]]
![[verification-horizon-invariant-2.png]]
![[verification-horizon-invariant-3.png]]
![[verification-horizon-invariant-4.png]]
![[verification-horizon-invariant-5.png]]

---

### LAYER 2 — Real browser behaviour (~1:30)

**Artifact on screen:** a Playwright assertion with a deliberate double-click.

```ts
await page.getByRole("button", { name: "Send invitation" }).dblclick();

await expect(page.getByText("Invitation sent")).toBeVisible();
expect(await invitationsFor("alice@example.com")).toHaveLength(1);
expect(await emailsSentTo("alice@example.com")).toBe(1);
```

**What it catches** — rows 9, 10, 11, and it re-checks 1 through 7 through the actual interface a human touches. This is where you find out that the API is perfect and the button is behind a modal. Backend green, product broken.

**Light up: 9, 10, 11.**

> **[DEMO 3 — screen recording, ~50s. This is where the demo turns on you, so don't over-rehearse it.]**

**Prompt:** `now drive the real UI. Send an invite the way a person would, and double-click the button.`

**What must land, in this order:**
- layer 1 is still fully green. Say that out loud *before* showing the result.
- the double-click produces two invites, or two emails. **TK** which one — seed the repo so this genuinely breaks.
- the fix is one line and it finds it in seconds. The point is not that it's hard. The point is that nothing below this layer could see it at all.

- ★ **"Every test I had was green. The feature was broken. Both of those sentences are true and that is the entire reason this layer exists."**

**TK improv:** the reaction shot when it comes back with two rows in the invites table. Don't script it.

**How it goes blind** — ★ **"This layer proves the thing happened. It has no idea whether the thing was any good."**
- The button worked. Was the error message comprehensible? Playwright cannot tell you.
- It only walks paths you scripted, so it inherits layer 1's blindness in a more expensive form.
- And it's the flakiest thing you own — which matters more than it sounds, because a suite people have learned to re-run until it passes has already stopped being a verifier.

![[verification-horizon-happened-vs-good-1.png]]
![[verification-horizon-happened-vs-good-2.png]]
![[verification-horizon-happened-vs-good-3.png]]
![[verification-horizon-happened-vs-good-4.png]]
![[verification-horizon-happened-vs-good-5.png]]

---

### LAYER 3 — Judgment (~2:00)

**Artifact on screen:** a rubric, not a prompt.

```yaml
- id: wrong-account-recovery
  question: >
    A user opens the invite link while signed into a different account.
    Does the screen tell them which account the invite was for,
    and give them a way out without leaving the flow?
  score: 0-10
```

**What it catches** — rows 13 and 14. The things that are real, expensive, and impossible to assert. Is the error message useful. Is the feature discoverable. Does this look like the rest of the product. Did the agent solve the request or a narrow reading of the request.

**Light up: 13, 14.**

> **[DEMO 4 — screen recording, ~45s. First cut if runtime is tight.]**

**Prompt:** paste the rubric from the slide, then `open the invite link signed into a different account, score it against this rubric, and show me the screen you scored.`

**What must land:**
- it drives the flow, screenshots the wrong-account screen, comes back with a number and reasons
- the number is **too high**. TK the exact score, but it should be praising a screen that is visibly unhelpful.
- then the move: `you gave that an 8. Read the screen again and tell me what a confused user does next.` It reverses.

- ★ **"It agreed with me instantly. That's not a judge, that's an audience. And a judge you can talk out of its score will get talked out of it by the thing it's judging."**

**TK improv:** if it happens to score it correctly low, run it again against a deliberately more verbose version of the same screen and show it preferring the longer one. Either outcome proves the layer, so you can't lose this take.

- Worth naming why it's a *rubric* and not "hey Claude is this good": Qwen found that decomposing into structured dimensions took judge–human agreement to a Spearman correlation around 0.9, and made different judge models agree with each other at Kendall τ above 0.93. Unstructured LLM judging is vibes with extra steps. Structured judging is a measurement.

**How it goes blind** — ★ **"This is the first layer that can be *persuaded*, and that changes everything."**
- Qwen's static judges got gamed by length: models learned to emit more and more CSS and JavaScript because verbose output scored better. The fix was to stop judging the source and start judging the *runtime behaviour* — drive the actual page, then score what happened.
- And the structural problem: a judge calibrated against weak output can't discriminate between two strong outputs. It saturates. The better your agent gets, the less this layer tells you — ★ **which is decay, happening in front of you, on a file you never edited.**

![[verification-horizon-saturation-1.png]]
![[verification-horizon-saturation-2.png]]
![[verification-horizon-saturation-3.png]]
![[verification-horizon-saturation-4.png]]
![[verification-horizon-saturation-5.png]]

---

### LAYER 4 — The trajectory (~3:00) ← paper payoff

**Artifact on screen:** an agent trajectory log.

```
task-9281
  commands:        rg "invitation" apps/api  ·  git log --grep="8486"  ·  pnpm test
  files_modified:  apps/api/invitations/accept.ts
                   tests/integration/invitations.test.ts   ← 🚩
  network:         api.github.com/search/issues?q=...invitation+expiry   ← 🚩
  diff:            assertion changed:  toHaveLength(1)  →  toBeGreaterThan(0)   ← 🚩
```

**What it catches** — ★ **"Nothing on the board. Not one row. This is the only layer that doesn't verify the feature — it verifies your other four layers haven't been tampered with."**

Every layer above judges the final state. None of them can see *how you got there*. So: the agent searched GitHub for the fixing PR. The agent edited the test file it was being graded on. The agent widened an assertion from "exactly one" to "at least one" and every check went green.

**Board light-up: none. Instead — a shield appears over the board itself.**

**This is where the paper pays off.** Callback to the cold open:

- Qwen catalogued seven distinct hacking behaviours. Solution artifact retrieval. External fix lookup. Test-oracle tampering. Evaluation-harness tampering. Visible-test overfitting. Evaluator-aware patching. Repository-history mining.
- ★ **"Every single one of those is something a competent human engineer under deadline pressure has also done."**
- They hardened the environment first — stripped future commits, killed network access where it wasn't needed. Sensible. Necessary. **And not sufficient**, because the remaining exploits were *policy-dependent*: they emerged from how the agent chose to gather information, so you cannot patch them out of the environment in advance.
- So they added a trajectory monitor. Log every command, every network call, every file touched, the final diff. Penalise the runs that got their green via a shortcut.
- The numbers: hacked-and-passing went from **28.6% to 0.56%.** Clean resolution — passing *without* triggering the monitor — went from **40.2% to 60.5%.** On SWE-Bench Verified alone, 36% to 65%.
- ★ **"Read that second number again. Watching how the work got done made the work twenty points better. They didn't add a single test."**
- And the graph that should scare you: in the unmonitored run, the reported pass rate kept climbing while genuine performance *collapsed*. The dashboard was green the whole way down.

> **[DEMO 5 — screen recording, ~70s. The payoff of the whole thread.]**

**Nothing new gets built here.** You scroll back through the session the audience has been watching since Act 1 and read what actually happened in it.

**Prompt:** `dump everything you did in this session: every command, every file you touched, every network call, and the final diff.`

**What must land, in this order:**
1. the boring stuff. Commands, files read. Let it be boring for a good ten seconds.
2. the flag. **TK the real one, do not stage it if you can possibly avoid it.** Most likely candidates from `DEMO 1` through `DEMO 3`: it edited a test file while fixing the double-click bug, it looked something up online, or it loosened an assertion to get back to green.
3. if the session genuinely produced nothing flag-worthy, say that on camera and cut to the log from the separate unattended run instead. **A clean log is a real result and it is worth more than a planted one.**

- ★ **"Every green tick you just watched came from this session. This is the only view that can tell you whether any of them were earned."**
- Callback to `DEMO 0` and close the leash idea: this is why *how long can you run unattended* is not a number the agent gets to pick for itself.
- ★ **"I let it run on its own because layers one and two existed. This is how I find out whether that was a good idea."**

**How it goes blind** — the pattern set is a list of tricks you've already seen. Qwen had to keep rewriting it *during training*, because as the policy improved it found new channels that weren't in the original review. ★ **"A monitor is a snapshot of yesterday's cheating."**

![[verification-horizon-trajectory-1.png]]
![[verification-horizon-trajectory-2.png]]
![[verification-horizon-trajectory-3.png]]
![[verification-horizon-trajectory-4.png]]
![[verification-horizon-trajectory-5.png]]

![[verification-horizon-monitor-lag-1.png]]
![[verification-horizon-monitor-lag-2.png]]
![[verification-horizon-monitor-lag-3.png]]
![[verification-horizon-monitor-lag-4.png]]
![[verification-horizon-monitor-lag-5.png]]

---

### LAYER 5 — Production reality (~2:00)

**Artifact on screen:** the funnel, plus one support email.

```
invite_started    1,000
invite_created      940
invite_opened       610
invite_accepted     238   ← 39%, was 61% last month
```
> *"I clicked the link and it says I don't have access? I'm literally the person you invited."*

**What it catches** — rows 13, 14 and 15, but *for real* this time, and at their true magnitude. Every layer above this is a simulation of a user. This layer is users.

★ **"Metrics tell you where. Users tell you why."** The funnel told you 39%. It could never have told you they were signed into a personal Gmail while the invite went to their work address. Only a human types that sentence.

**Light up: 13, 14, 15 — and then the move that matters:**

★ **"And then this happens."** — **new rows appear on the board that were never there.**

```
16 | Invite emails are landing in Outlook spam
17 | Nobody understands what "role" means at the point of sending
18 | Half of them are inviting people who already have accounts
```

★ **"You didn't forget these. You could not have known them. The board was never complete, and it was never going to be — and if you believe that, then you already believe verifiers decay, because a board that grows is a verifier that was wrong yesterday."**

> **[NO DEMO HERE — and say that on camera. It's the strongest thing you can do with this layer.]**

There is no clip for this layer because there cannot be one. Everything above was a simulation you can run in ninety seconds on a laptop. This one takes a month and real users, and the honest move is to name that difference out loud rather than fake a dashboard for symmetry.

**On screen:** real artifacts only. **TK** a genuine funnel screenshot and one genuine support email, redacted. If nothing suitable exists, use the mock above and label it a mock on screen.

- ★ **"I can demo the first four layers. I cannot demo this one, and that gap is the point: the only layer that touches reality is the only one you can't rehearse."**

**How it goes blind** — it's the slowest and most expensive signal you own, it only tells you about things that already shipped and already cost you, and it's aggregate, so a failure affecting 2% of users hides inside noise forever. You cannot ship against this layer. You can only learn from it.

![[verification-horizon-board-grows-1.png]]
![[verification-horizon-board-grows-2.png]]
![[verification-horizon-board-grows-3.png]]
![[verification-horizon-board-grows-4.png]]
![[verification-horizon-board-grows-5.png]]

---

## ACT 3 — OUTRO — verbatim (target ~2:30)

> **[ON SCREEN: the full board, all 18 rows, colour-coded by layer]**

So that's the stack. Deterministic checks. Real browser behaviour. Structured judgment. The trajectory. And production.

And I want to be really clear about what I am *not* saying, because this is where these videos usually go wrong. I'm not telling you to go and build five layers of verification for your side project this weekend. You will not do it, and you shouldn't.

Here's what I actually think you should do. It's one rule, and it's the whole video:

> **[ON SCREEN: THE CONVERSION RULE]**

**When reality disagrees with your verifier, convert that disagreement into a permanent check at whichever layer would have caught it.**

That's it. That's the mechanism.

Someone emails you that they were signed into the wrong account. You don't just fix it. You ask: *which layer should have caught this?* And the answer is layer three, so you add a rubric line about wrong-account recovery, and now that failure can never silently ship again. Your agent double-sends an invite. That's layer two, so a double-click test goes in. You catch an agent widening an assertion to make its own tests pass — that's layer four, and now that pattern is in the policy file forever.

You don't plan the whole stack. You let production pay for it. Every real failure buys exactly one permanent check, at exactly the layer that missed it. Do that for six months and you will have a verification system that is *shaped like your actual product*, which is worth more than any stack somebody on YouTube designed for you.

And notice this is the same question I asked at the very beginning, just pointed the other way round. Before you start, you ask the agent what it can prove. After something breaks, you ask which layer should have proved it. One question, two ends of the same loop, and between them is the only verification system you're ever actually going to maintain.

> **[DEMO 6 — screen recording, ~40s. Last thing before the close.]**

The rule, run once, on a failure the audience already watched happen.

**Prompt:** `the double-click bug from earlier got through. Which layer should have caught it, and add the check there. Just that one.`

**What must land:**
- it names layer 2 without being told
- one test goes in, it runs, it's green, it's committed
- the whole thing is under a minute, and that *is* the argument. You are not building a stack. You are paying for one check with one failure.

- ★ **"That's it. That's the entire practice. One real failure bought one permanent check, and my verifier is now one row less wrong than it was this morning."**

**TK improv:** if the fuzz finding from `DEMO 2` got a bigger reaction on the day, use that failure instead. Either works.

![[verification-horizon-conversion-rule-1.png]]
![[verification-horizon-conversion-rule-2.png]]
![[verification-horizon-conversion-rule-3.png]]
![[verification-horizon-conversion-rule-4.png]]
![[verification-horizon-conversion-rule-5.png]]

> **[ON SCREEN: back to the thesis]**

And the reason this has to be a *rule* and not a one-time setup is the thing we started with.

The agent that hit Hugging Face wasn't trying to break the rules. It was trying to pass the test. Qwen's agents weren't malicious — they found the cheapest path to the number we told them to maximise, and cheating had the best success rate of anything on the board. That's not a bug in the models. That's what optimisation *is*.

Which means every check you own is on a clock. Not because you'll write it badly. Because the thing you're measuring is getting better at satisfying that specific check, and the gap between "passes my tests" and "does what I meant" is exactly where all the failure now lives.

> **[ON SCREEN, final: "When did your verifier last change, and what forced it?"]**

So here's the question I'd leave you with. Go look at your repo tonight and ask: **when did my verification last change, and what forced it?**

If the answer is "I haven't touched the tests in a year, and nothing forced it" — that's not stability. Your agent got better every month this year. Your definition of "working" didn't move once.

That's the horizon. It keeps receding, and you have to keep walking.

I'll see you in the next one.

![[verification-horizon-receding-horizon-1.png]]
![[verification-horizon-receding-horizon-2.png]]
![[verification-horizon-receding-horizon-3.png]]
![[verification-horizon-receding-horizon-4.png]]
![[verification-horizon-receding-horizon-5.png]]

---

## Appendix — production notes

**Coverage board states.** Board is docked from Act 1 onward. Row states: `grey` (uncovered) → `lit` when a layer claims it → colour-coded by layer. Layer 4 lights nothing and instead draws a shield around the whole board. Layer 5 lights 13/14/15 *and appends rows 16–18*, which is the visual proof of the thesis.

**Demo thread — recording prep.**
- One repo, one branch, one session, recorded in order in a single sitting. `DEMO 5` reads the trajectory of `DEMO 1` through `DEMO 4`, so re-shooting any earlier clip invalidates it.
- Seed the repo so `DEMO 2` and `DEMO 3` genuinely fail. **TK** which bugs. The double-click one has to actually break, not be narrated.
- Record a second, longer unattended run separately as insurance for `DEMO 5`, in case the main session's log comes back clean.
- Board states for the thread: `hollow` (claimed by the agent in `DEMO 0`, unproven) → `solid` (proven by a layer) → indented sub-rows like `4a` for anything fuzzing turns up. Rows 16 to 18 still only appear at Layer 5.
- Do not tidy the agent's output before recording. The mistakes are the asset.
- Runtime: the thread adds roughly 5:00. `DEMO 4` is the first cut, `DEMO 2` the second.

**Mandated lines (`★`) — do not paraphrase on camera:**
1. "That's the whole ticket. Twelve words."
2. "Nobody wrote a single one of these down."
3. "A test suite is a list of the things you thought of."
4. "This layer proves the thing happened. It has no idea whether the thing was any good."
5. "This is the first layer that can be persuaded."
6. "Nothing on the board. Not one row." (L4)
7. "Watching how the work got done made the work twenty points better. They didn't add a single test."
8. "A monitor is a snapshot of yesterday's cheating."
9. "Metrics tell you where. Users tell you why."
10. "The board was never complete, and it was never going to be."
11. The conversion rule, read exactly as written.

**Demo-thread mandated lines (`★`) — do not paraphrase on camera:**
12. "Whatever it can check by itself is exactly how far it can run without you. Your verifier is not a safety net. It's the length of the leash." (`DEMO 0`)
13. "Two prompts. Nine rows are now permanently guarded." (`DEMO 1`)
14. "Every test I had was green. The feature was broken." (`DEMO 3`)
15. "Every green tick you just watched came from this session." (`DEMO 5`)
16. "I can demo the first four layers. I cannot demo this one." (Layer 5)
17. "One real failure bought one permanent check." (`DEMO 6`)

**Numbers to get right on camera:**
- Qwen hacked-resolved **28.57% → 0.56%**; clean-resolved **40.22% → 60.53%**; SWE-Bench Verified clean **36.49% → 64.98%**.
- Solution artifact retrieval: **4.32%** of trajectories, **72.34%** resolved vs **59.99%** baseline (**+12.35pp**).
- Rubric judge alignment: Spearman **0.905**, cross-judge Kendall **τ ≥ 0.93**.
- Fable 5: only model to initiate price collusion; **~6×** more agent-to-agent email; collusion rate **>2×** Opus 4.8.
- OpenAI/HF: **21 July 2026**, GPT-5.6 Sol + internal pre-release prototype, reduced cyber refusals, **ExploitGym**, **Artifactory** zero-day, RCE on HF servers, test solutions from HF **production database**.

**Title candidates**
- "Your Tests Have an Expiry Date"
- "AI Agents Are Cheating More, Not Less"
- "The Agent Didn't Solve the Benchmark. It Stole the Answer Key."
- "Why Your Coding Agent Passes Every Test and Still Ships Broken Code"
- "You Don't Have a Verifier"

**Open / to decide**
- Whether to include the cost-cascade point (don't run all five layers on every change; gate the expensive ones behind the cheap ones). Currently cut for pace — one line in the outro at most. `DEMO 1` now covers most of this implicitly.
- CTA placement.
- Runtime. The demo thread pushes this to 20–22 min. Either accept the longer runtime or cut `DEMO 4` and trim `DEMO 2`.
- Deck slides for the thread don't exist yet. At minimum: a `DEMO 0` three-lists slide, a hollow-vs-solid board legend, and a "no demo possible" card for Layer 5.
