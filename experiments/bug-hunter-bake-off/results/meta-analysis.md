---
tags: [bug-hunt, evaluation, meta-analysis]
date: 2026-07-29
model: opus-5
---

## What this is

Ten independently designed bug-hunting skills were run against the same codebase, at the
same time, under the same rules, each spawning its own nested subagents. This document
scores them against each other and names a best and a worst.

The question being answered is *not* "what bugs does HyperWhisper have." It is "which
hunting strategy, given a codebase and no diff to anchor on, actually finds real defects."
The bugs are the measuring instrument, not the product.

## Why a pinned arena

The comparison is only meaningful if scope, effort, and report shape are identical across
all ten. Otherwise the winner is whoever happened to be pointed at the richest directory.
So every hunter got the same brief (`00-shared-brief.md`), the same 210-file arena
(`scope-files.txt`), the same deep-effort instruction, the same mandate to fan out to
subagents, and the same report template.

The arena was the TypeScript surface of the monorepo — `nextjs/` and `hyperwhisper-cloud/`,
210 files, ~31,000 lines — deliberately excluding the Swift, C#, and Rust clients. Two
reasons. First, it is the only slice with a working test/typecheck/lint loop, which the
oracle-driven and execution-driven strategies structurally require; without it they would
have degraded into plain reading and the comparison would have measured nothing. Second,
it carries the real risk surface: auth, billing, quota accounting, provider fallbacks,
webhooks.

## The verification bar

Every hunter was held to an inverted ladder: **the default verdict is REFUTED.** A finding
is CONFIRMED only when there is a concrete trigger path from a real entry point — named
file, named line, named caller, and an input or sequence that reaches it. Anything that
survives scrutiny but whose chain has an unproven link is PLAUSIBLE, and must say which
link.

This is the opposite of how diff review works, and deliberately so. On a diff, biasing
toward PLAUSIBLE is correct: the change is small, the reviewer's time is bounded, and a
false positive costs one comment. Off-diff, that bias is poison — an unbounded codebase
will generate unbounded plausible-looking findings, and a report of 200 maybes is
indistinguishable from noise.

## How the scoring works

Raw CONFIRMED counts are not the score, because the strategies do not have equal access to
proof. A hunter that can run the test suite clears "CONFIRMED" more cheaply than one that
reasons from reading, and would win on volume while telling you less. So four axes:

1. **Confirmed findings, weighted by repro.** A finding backed by something executable —
   a failing test, a `curl`, a node one-liner, an observed typecheck error — counts for
   substantially more than one backed by argument alone.
2. **Unique findings.** A defect that only one strategy surfaced is the clearest evidence
   that strategy sees something the others structurally cannot. This is the axis that most
   separates the field.
3. **Independent rediscovery.** When several hunters using unrelated methods land on the
   same file and line, that finding is almost certainly real. Convergence validates the
   *finding*; it does not credit the hunter much, since the defect was evidently findable
   by many routes.
4. **Honesty of the coverage ledger.** A hunter that examined 15 files and says so plainly
   is more useful than one that examined 15 files and implies the codebase is clean. Not a
   tiebreaker — load-bearing, because the entire failure mode of whole-codebase hunting is
   a report that reads as exhaustive when it was a sample.

## An important caveat about the data

Eight of ten hunters wrote their own reports. Two — **entry-point-tracer** and
**invariant-hunter** — were stopped before they synthesised theirs when the run was paused.
Their nested subagents had, however, returned essentially all of their analysis, and those
returns are preserved under `raw-subagent-output/`.

(oracle-hunter was initially counted among the unfinished, because it died on a session
limit. It turned out to have written its report first, so its row below is its own
self-reported scorecard: 8 confirmed / 7 plausible / 5 with repro / ~95 files / 10
subagents. That is higher than the reconstruction I had estimated from its subagent returns,
which is a useful calibration note on how much the synthesis pass adds.)

So those two are scored on *what their subagents demonstrably produced*, not on a
finished self-assessment. This cuts both ways and I want to be explicit about it: it
denies them the synthesis step where a hunter deduplicates, re-verifies, and drops its own
weak items — which is exactly where spec-gap-hunter, for instance, initially failed. It
also means their file counts and finding counts are reconstructed rather than self-reported.
Their placement below is defensible on the evidence, but it is not measured identically to
the other eight, and a rerun that let them finish could shift the ordering.

## Scorecard

Self-reported for the eight that finished; reconstructed for the two marked ※.

Every row below was re-checked on 2026-07-30 against the `## Scorecard` block the hunter
wrote at the top of its own report. Three rows were wrong on first publication and have been
corrected; see *Corrections* below.

| Skill | CONF | PLAUS | w/ repro | files (of 210) | subagents |
|---|---|---|---|---|---|
| entry-point-tracer ※ | ~40 | ~15 | ~12 | ~150 | 15 |
| invariant-hunter ※ | ~25 | ~15 | ~8 | ~140 | ≥19 |
| hostile-input-hunter | 20 | 4 | 20 | 108 | 7 |
| concurrency-hunter | 12 | 3 | 4 | ~150 | 6 |
| git-signal-hunter | 11 | 3 | 5 | ~68 | 11 |
| oracle-hunter | 8 | 7 | 5 | ~95 | 10 |
| subsystem-auditor | 7 | 8 | 1 | 58 | 6 |
| divergence-hunter | 2 | 1 | 1 | 34 | 5 |
| spec-gap-hunter | 2 | 1 | 2 | 30 | 7 |
| mutation-survivor-hunter | 0 | 3 | 7 | 20 | 4 |

### Corrections

**`concurrency-hunter` was scored 3/2/3/17 and is actually 12/3/4/~150.** This is the one
material error. Its coverage ledger explains how it happened: a transport failure swallowed
all six of its lens agents' completion notifications, so it first wrote a report from its own
direct reading alone, then re-requested the agents' results and published a merged version
with 12 numbered CONFIRMED findings (`reports/concurrency-hunter.md:103-524`). The scorecard
was taken from the partial version. The giveaway is the `17`, which is the count of files the
hunter read *directly itself*, never its coverage.

The error moves it from 7th to 4th, and the direction matters more than the position: the run
penalised a hunter for harness flakiness rather than for anything about its strategy. Any
conclusion drawn from "concurrency bugs were rare here" was an artifact. They were not rare.
Its 12 findings are the densest single cluster in the run, all on money-state transitions.

**`mutation-survivor-hunter` was scored 0/1/6/15/3 and is actually 0/3/7/20/4.** Does not
change its last-place ranking on confirmed bugs.

**`git-signal-hunter`'s repro count was 6 and is actually 5.** No ranking effect.

**Retracted: there is no invariant-hunter attribution error.** An earlier version of this
section claimed the CONFIRMED findings in `raw-subagent-output/verifiers/` were tagged with
invariants belonging to other hunters. That was wrong, and it was my error rather than the
run's. I1-I8 *are* invariant-hunter's own first eight sweeps, in the same numbering scheme as
the I09-I14 transcripts, and every candidate block carries an explicit `Invariant: I2`-style
ownership tag. What looked like misattribution was convergence: I2's candidates
(`credits.ts:74`, `transcribe.ts:678`) are the same *defects* several other hunters found,
because six hunters converged there. Same bug, independently discovered, correctly attributed.

**`invariant-hunter`'s subagent count is wrong: at least 19, published as 14.** Its run was
8 own sweeps (I1-I8) + 6 more (I09-I14) + 5 verifiers. This one still stands as an error.

One known-soft number remains, and it is the one that picks the winner:

- `entry-point-tracer`'s `~40` is unverified. It is the largest number in the table, an
  attempt to re-extract it from `raw-subagent-output/` failed, and it was assigned by a third
  party (me) to prose that was never graded on the shared ladder at all — none of its 13
  subagent prompts contain the words REFUTED, PLAUSIBLE, or "default verdict", and the string
  `PLAUSIBLE` appears nowhere in its transcripts, which instead self-grade `confidence: high`.
  So its count is not commensurable with the nine rows beneath it. Treat the top spot as
  unranked pending a rerun, not merely provisional.

## Does the scoreboard measure strategy, or compute?

Mostly compute, on the confirmed-count axis. Correlations across all ten rows, corrected
figures, n=10, critical |r| for p<.05 = 0.632:

| Relationship | Pearson | Spearman |
|---|---|---|
| confirmed ~ files read | **+0.82** | **+0.93** |
| confirmed ~ subagents | **+0.82** | **+0.78** |
| confirmed + plausible ~ subagents | **+0.85** | +0.69 |
| repro ~ subagents | +0.31 | +0.53 |
| repro ~ files read | +0.47 | +0.48 |
| files read ~ subagents | +0.65 | +0.62 |

Dropping the two reconstructed rows (n=8): confirmed~files +0.79, confirmed~subagents +0.41.

**The gap between the top two rows and the two repro rows is the finding.** Both numbers come
from the same self-reports, so the difference is not a reporting artifact: *fanning out more
agents buys more claims, not more proofs.* Confirmed-count is largely a compute proxy.
Repro-count is not, and does not reach significance against either compute axis.

That makes proof rate the only volume metric in this table worth ranking on, and it is why
`hostile-input-hunter`'s clean sweep is the most robust result in the run — it is measured on
the axis that compute cannot inflate.

**`concurrency-hunter` is the informative residual.** It reached ~150 files on 6 subagents,
matching the 15-agent entrant's coverage; correcting its row is what dropped files~subagents
from +0.87 to +0.65. Its ledger shows the mechanism: *one* broad mapping agent opened 120 files,
then five narrow lenses swept them. So fan-out **shape** beats fan-out **count**, and coverage
is not simply bought with agents. Compute explains most of the variance, and the residual points
at something more useful than the confound does.

## The subagent cap makes ranks 5-10 a race outcome

The `subagents` column is not a strategy property. All ten hunters competed for one shared
20-slot pool, and the four largest fan-outs alone demanded roughly 55 slots. The hunters that
grabbed slots early starved the ones that asked later, and five of them say so in their own
ledgers:

- `oracle-hunter` lost its **entire** verification wave: *"That phase did not run."*
- `subsystem-auditor` lost Angle D and all but one verifier.
- `mutation-survivor-hunter` got 4 agents where its deep tier wants 10-12, with 3 spawns
  rejected outright.
- `spec-gap-hunter` received zero subagent output — *"transcript files stayed at 130 bytes"* —
  which is the real cause of the synthesis failure I attributed to it below.
- `concurrency-hunter` had two lenses relaunched twice, on top of the transport failure that
  cost it eight places.

So the bottom half of the table is partly a record of which hunters lost a resource race, and
the fix is a dedicated equal budget per entrant rather than a shared pool. Ranks 5-10 should be
read as one-directionally understated.

## Convergence index

Findings rediscovered independently, which is the strongest evidence available that they
are real. These also happen to be the ones worth fixing first.

**Two limits on this table, both found after publication.** First, convergence measures agreement
in *noticing*, not agreement in *verdict*: the withdrawn `/api/internal/models` row was noticed by
three hunters and then independently **refuted** by two, so counting noticings had it exactly
backwards. Second, there is a selection bias in using convergence as proof — the findings that
converge are by construction the ones *many* strategies can reach, so this table partly measures
how cheap a finding was to find. The six-way `/usage` item sits in two functions about twenty lines
apart in a single file. It is still the right triage order, because cheap-to-find and real are
correlated here. But the axis that actually discriminates between *strategies* is unique findings,
and that is the axis this run measured worst.

| Finding | Found by |
|---|---|
| `sanitizeReturnTo` tab/CR/LF bypass → open redirect (`middleware.ts:135`) | 4: oracle-hunter, entry-point-tracer (T10, T11), invariant-hunter (I13) |
| `/usage` caches transient 5xx/429 as "license invalid" for 1h | 6: divergence, subsystem-auditor, git-signal, entry-point-tracer (T4, T5), oracle-hunter (D2), concurrency |
| Fire-and-forget `deductCredits` swallows failures; charge lost | 5: concurrency, git-signal, subsystem-auditor, entry-point-tracer (T3, T6), oracle-hunter (A1) |
| Credit check has no reservation/hold → concurrent overspend | 4: concurrency, entry-point-tracer (T3, T6), hostile-input, oracle-hunter (A1) |
| SIGTERM drain misses streaming sessions (billed to nobody) | 3: entry-point-tracer (T3, T4), invariant-hunter (I11), concurrency |
| Admin grant is the only writer not normalising email | 3: git-signal (`:476-502`), subsystem-auditor (`:191-208`), entry-point-tracer (T9-B1, T12-BUG1, T13-BUG2). Previously listed as "2: entry-point-tracer (T9, T12)", which counted one hunter's two traces as two hunters — the opposite error to the one below. |
| ~~`/api/internal/models` ungated unlike its three siblings~~ **withdrawn** | 3 noticed it, and 2 independently refuted it: `hostile-input-hunter.md:531-533` (public by design, with an explicit anonymous-traffic comment and `Cache-Control: public, s-maxage=3600`) and `verifiers/verify-credits-api-auth-ratelimit.md` (byte-identical to the deliberately public `/models`, no confidentiality delta). |

That the top item was found four times by four unrelated strategies, each verifying it by
*running* the WHATWG parser rather than reasoning about it, is the single most reassuring
result in the run.

---

## Best: entry-point-tracer — *claim withdrawn, see below*

> **This section overstated its case and the heading no longer holds.** Three of its load-bearing
> claims did not survive checking: "it found the most" rests on an unaudited count graded on a
> different scale from every other row, "neither of which any other hunter reached" is false for
> one of the two headline findings, and "the highest unique-finding count" is tabulated nowhere.
> What does survive is narrower and still worth having: *entry-point tracing reached a class of
> cross-system seam defect that no other strategy in this run reached at all.* The rest of the
> section is left as written, with the failures marked, because the way an unverified number
> acquired a crown is the most instructive thing in this document.

**It found the most, it found the most severe, and its structure is the one that
generalises.** ← two of these three are not supported.

The strategy is simple to state: enumerate every entry point into the system (it found 88),
then trace each one hop by hop through every layer it touches, and look specifically at the
*joints* between layers rather than inside them. That framing is why it won. Its own
closing line on the transcribe path names the thesis better than I could: every individual
layer is defensively written, and all the failures are at the joints — the reservation and
the charge use different units of duration, the balance check and the deduction share no
state, the deduction's failure signal has nowhere to go, and the fail-closed duration
backstop was applied to four adapters and not the other four.

It produced the two most severe findings in the entire run. Only the first was unique to it;
the claim that neither was reached by another hunter is **false**:

- **Login CSRF** (T10). A plain link with the *attacker's* license key silently signs the
  victim into the attacker's account — no POST, no form, no JS on the attacker's side.
  It traced why both of better-auth's CSRF defences structurally miss, and followed through
  to the consequence: the victim then buys credits into the attacker's wallet while
  `/api/customer/profile` hands them the attacker's key in plaintext.
- **Unrecoverable redirect-loop lockout** (T11). Middleware admits on cookie *presence*;
  the page checks session *validity* and bounces back; neither clears the cookie. Rotating
  `BETTER_AUTH_SECRET` puts every logged-in user into it at once, and they cannot reach
  sign-in or sign out to escape.
  **Not unique.** `invariant-hunter` found this independently in its I8 sweep — same file, same
  line (`nextjs/middleware.ts:133`), same trigger, same blast radius, down to naming the secret
  rotation: *"A secret rotation does this to every signed-in customer simultaneously."* See
  `raw-subagent-output/invariant-hunter/own-sweeps-I1-I8/i08-auth-gate-agreement.md`. The same
  sweep also independently found the missing `return` in sign-out, which is likewise counted
  below as one of this hunter's unique findings.

The login CSRF does appear genuinely unique: no CSRF or forced-login candidate exists in any of
I1-I8, and a case-insensitive search for `csrf` across all eight finished reports returns
nothing. That is a real result and it is the strongest single point in this hunter's favour.

~~Its unique-finding count is the highest by a wide margin~~ — **this was never tabulated, by me
or anyone.** The list that followed it (Stripe-customer binding by unverified email match, the
"Refund Only" button that revokes anyway via the webhook it fires, the migrations that commit
before two failable build steps, the admin-grant email normalisation gap, the `23505` detection
made dead by a drizzle upgrade, the missing `return` in sign-out) was never checked against the
other hunters' candidate lists, and spot-checking has now found two items in it that were not
unique. Read it as "findings this hunter reached", not as "findings only this hunter reached".

The genuinely distinctive part is the *class*, not the count: several of these are cross-*system*
seams — code and Stripe, code and Vercel's deploy ordering — that a strategy confined to reading
files cannot see by construction. That claim needs no count to stand, and it is what I would keep
this strategy for.

**Pros.** Highest yield and highest severity. Systematically complete in a way the
file-oriented strategies are not — it enumerated entry points first, so its coverage claim
is checkable. Naturally finds cross-boundary defects. Its traces are directly actionable:
every finding arrives with a named hop sequence a developer can walk.

**Cons.** By far the most expensive — 15 subagents, the longest wall-clock, and the largest
token spend in the run. Coverage is entry-point-shaped, so code reachable only through
unusual paths gets thinner treatment. It generated real duplication across traces (the
`/usage` cache poisoning surfaced in both T4 and T5, the deduction swallow in both T3 and
T6), which a synthesis pass would have collapsed — and, as noted above, it never got that
pass. Its lower repro rate relative to hostile-input reflects that tracing produces
arguments more readily than it produces executable proofs.

---

## Runner-up: hostile-input-hunter

Worth naming because on the pure numbers it looks like the winner: 20 confirmed, **20 with
executable repros**, 108 files. Every single confirmed finding carried a repro, the only clean
sweep in the field, and that is not an accident of scoring — its whole method is to construct
an input and run it, so a finding either reproduces or it does not survive. If you want
findings a skeptic cannot argue with, this is the strategy.

(On the comparison page the same hunter reads 83% rather than 100%, because that column divides
repros by confirmed *plus* plausible. Both numbers are correct and they answer different
questions: 20 of 20 confirmed findings were proven, and 20 of its 24 total claims were.)

It loses the top spot on severity and reach. Its findings are overwhelmingly
input-validation-shaped: unbounded fields, missing type guards, oversized payloads,
malformed values reaching parsers. Real, cheap to fix, but none of them are the login CSRF.
The defects that cost the most here are architectural mismatches between layers, and you
cannot fuzz your way to "the reservation and the charge disagree about what a minute is."

**Pros.** Unmatched proof quality; every finding is executable. Broad file coverage.
Findings are unambiguous and fast to triage — no judgment call about whether it's real.
**Cons.** Ceiling on severity: finds *malformed input* bugs, not *design seam* bugs. Blind
to anything requiring multi-step state or cross-service reasoning. Produces volume that can
crowd out the few items that actually matter.

---

## The rest, ranked

**git-signal-hunter** (11/3/5). Mines history — churn, reverts, bug-fix commits, comment
drift — to find where the codebase has repeatedly hurt. Strong yield and 11 subagents. Its
distinctive move was reading commit messages as intent evidence, which let it separate
deliberate tradeoffs from oversights better than any other entrant. *Con:* this repo is a
squashed vendoring commit for large stretches, which blinded it exactly where it most
wanted to look; it says so honestly.

**invariant-hunter** ※ (~25/~15). Picks a property that should hold codebase-wide
(every outbound fetch has a timeout; every secret comparison is constant-time) and sweeps
all 210 files for violations. Excellent *completeness* per invariant and the best
refuted-to-confirmed ratio in the run — I9 came back nearly clean and said so, which is a
genuinely useful result. Found that seven of eight LLM adapters call `fetch` with no
timeout signal. *Con:* it only ever finds what its invariant list anticipates. Choosing the
invariants *is* the strategy, and a defect nobody thought to name as a property is invisible.

**subsystem-auditor** (7/8/1). Divides the codebase into subsystems and audits each in
depth. Reasonable yield, 58 files. *Con:* only 1 of 15 findings had a repro — it reasons
rather than proves, so its output needs the most downstream verification. Its
PLAUSIBLE count exceeding its CONFIRMED count is the signature of that.

**oracle-hunter** (8/7/5). Runs the tools — typechecker, linter, dead-code analysis —
and chases each signal to a verdict. Notable for the *highest refutation rate in the run*:
it killed most of its own leads, correctly. It established that the Stripe `as any`
suppressions were narrowing noise rather than a version mismatch, that a "dead" validator
was actually called, and that a NaN hazard was unreachable. *Pro:* nearly everything it
confirms is backed by observed tool output. *Con:* strictly bounded by what the tools can
see, and this codebase typechecks clean, so its ceiling was low from the start. Its best
findings came from chasing a signal *sideways* into adjacent code rather than from the
signal itself.

**concurrency-hunter** (12/3/4). Hunts races, TOCTOU, and ordering bugs. Fourth on volume and
first on verification discipline: its verifiers confirmed, downgraded, *and refuted*
candidates with equal willingness, and corrected its own parent's framing more than once. Its
12 findings are the tightest thematic cluster in the run — every one sits on a money-state
transition (admission, cache write, deduction, refund, grant, shutdown) rather than on data
corruption, because the storage layer's unique-index defenses genuinely held and every
survivor lives either upstream of storage or on a dedupe key chosen so an existing constraint
could never fire. *Pro:* the only strategy that reached defects requiring two things to happen
at once, which is a class no amount of careful file-reading finds. *Con:* only 4 of 12 carry
executable repros, and that is inherent rather than laziness — true cross-process races across
17 Fly machines and many Vercel lambdas cannot be driven in-process, so its best findings are
argued rather than demonstrated. It also survived the run's worst harness failure (see
*Corrections*), which cost it eight places in the original table.

**divergence-hunter** (2/1/1) and **spec-gap-hunter** (2/1/2). Both landed 2 confirmed.
Divergence looks for two implementations of one operation that disagree — a good thesis
that found the `/usage` versus `auth.ts` cache-poisoning split, which six hunters ultimately
converged on. Spec-gap compares documented behaviour to actual, and correctly bucketed
stale-doc items separately rather than inflating its count. Both are sound strategies that
this codebase simply did not reward much. Spec-gap also required intervention: its first
report badly under-reported what its own subagents had returned, a synthesis failure rather
than a hunting failure.

---

## Worst: mutation-survivor-hunter

**0 confirmed. 20 files. The most expensive setup of any entrant.**

The thesis is respectable: mutate the code, run the tests, and every mutation that survives
marks a behaviour nothing pins. Surviving mutants are test gaps, and test gaps are where
bugs live. It needed its own git worktree and a `node_modules` symlink to run safely, which
it did correctly and cleaned up after — no complaints about execution.

It fails because **the thesis presupposes a test suite, and this codebase does not have one
in the places that matter.** You cannot learn anything from a surviving mutant in code that
has no tests at all: a surviving mutant carries no information there, so the signal collapses.
Precisely: of the 10 mutations it executed, 7 survived and 3 were killed, and the 3 kills all
came from `hyperwhisper-cloud`, which does have a suite (138 passing tests). "Every mutant
survives" is true of `nextjs/` and false of the cloud service. Repeatedly,
the finding it would have made was already available more cheaply by just reading the file
and noticing there was no test. Its reach was the narrowest in the run — 20 of 210 files —
because running the suite per mutation is slow, and that cost bought nothing here.

To its considerable credit, it said so. Its scorecard reads "came up dry: yes (on test
gaps) / no (on live bugs)" — it reported honestly that its actual strategy produced nothing
and that its 7 executed mutations came from bugs it stumbled into while mutating, which is
not the same achievement. That honesty is worth more than a padded scorecard, and it is why
I rank it last on *fit* rather than on *conduct*.

**The one result from this run that most deserves to escape the scorecard is its.** All 7
surviving mutants are the same kind of thing: a money-charging or authorization enforcement
point in `hyperwhisper-cloud/src/middleware/` that the suite *executes* — giving respectable
coverage percentages — but never *asserts on*. It deleted the only line that charges anyone
(`credits.ts:144`), turned the paywall gate into `balance < 0` (`credits.ts:47`), removed the
revoked-license rejection (`auth.ts:113-115`), deleted the license-required gate
(`auth.ts:102-105`), removed the SIGTERM deduction drain (`credits.ts:114`), and moved
Deepgram's rate by 80% (`cost-calculator.ts:16`). The suite stayed green for every one. All
three of `validateAuth`'s rejection paths are independently removable.

So the entrant that scored zero on the metric being measured produced the most alarming
sentence in the run: *the arithmetic is defended, the gates that call the arithmetic are not.*
That is a finding about the codebase's safety margin rather than about a bug in it, which is
exactly why a confirmed-bug scoreboard cannot see it. Worth remembering when reading its last
place: the ranking measures fit to this task, not value delivered.

**Pros.** When it does fire, its evidence is the strongest possible — an executable
demonstration that a behaviour is unpinned. Rigorous and self-aware. Correctly isolated its
mutations so no other entrant was affected.
**Cons.** Requires mature test coverage to produce any signal at all; on a thinly-tested
codebase it degrades to zero. Slowest per file by a wide margin. Narrowest coverage.
Highest operational complexity — the only entrant needing write access and isolation.

---

## What I'd actually take from this

**Two strategies are worth keeping as a pair.** entry-point-tracer for reach and severity,
hostile-input-hunter for proof. They fail in opposite directions — one produces arguments
about architecture, the other produces executable demonstrations about inputs — and running
both gets you the severe findings *and* the incontestable ones. Their overlap was low.

**The inverted ladder worked.** Across the run, verifiers refuted a large share of what
finders proposed, and several refutations overturned findings that read as compelling: a
"dead" validator that was live, a Stripe version mismatch that was a typing artifact, a
credit-reservation bug whose exposure turned out to be bounded and self-correcting. Under
diff-review defaults every one of those ships as a PLAUSIBLE comment. Off-diff, that is the
difference between a report and noise.

**Coverage honesty was the sleeper axis.** The strategies I trust most are not the ones
with the biggest numbers; they are the ones whose refuted lists are longer than their
candidate lists. invariant-hunter's I9 sweep, oracle-hunter's chases, and the concurrency
verifiers all spent most of their effort proving things *weren't* bugs, and that is what
makes their remaining claims worth acting on.

**One caveat on the ranking.** Two hunters never got their synthesis pass. entry-point-tracer
wins comfortably enough that I doubt finishing would change the top spot, but the middle of
the table — invariant-hunter, oracle-hunter, subsystem-auditor — is close enough that a
clean rerun could reorder it.
