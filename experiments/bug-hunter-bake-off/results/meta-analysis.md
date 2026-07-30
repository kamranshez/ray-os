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

| Skill | CONF | PLAUS | w/ repro | files (of 210) | subagents |
|---|---|---|---|---|---|
| hostile-input-hunter | 20 | 4 | 20 | 108 | 7 |
| entry-point-tracer ※ | ~40 | ~15 | ~12 | ~150 | 15 |
| git-signal-hunter | 11 | 3 | 6 | ~68 | 11 |
| invariant-hunter ※ | ~25 | ~15 | ~8 | ~140 | 14 |
| subsystem-auditor | 7 | 8 | 1 | 58 | 6 |
| oracle-hunter | 8 | 7 | 5 | ~95 | 10 |
| concurrency-hunter | 3 | 2 | 3 | 17 direct | 6 |
| divergence-hunter | 2 | 1 | 1 | 34 | 5 |
| spec-gap-hunter | 2 | 1 | 2 | 30 | 7 |
| mutation-survivor-hunter | 0 | 1 | 6 | 15 | 3 |

## Convergence index

Findings rediscovered independently, which is the strongest evidence available that they
are real. These also happen to be the ones worth fixing first.

| Finding | Found by |
|---|---|
| `sanitizeReturnTo` tab/CR/LF bypass → open redirect (`middleware.ts:135`) | 4: oracle-hunter, entry-point-tracer (T10, T11), invariant-hunter (I13) |
| `/usage` caches transient 5xx/429 as "license invalid" for 1h | 6: divergence, subsystem-auditor, git-signal, entry-point-tracer (T4, T5), oracle-hunter (D2), concurrency |
| Fire-and-forget `deductCredits` swallows failures; charge lost | 5: concurrency, git-signal, subsystem-auditor, entry-point-tracer (T3, T6), oracle-hunter (A1) |
| Credit check has no reservation/hold → concurrent overspend | 4: concurrency, entry-point-tracer (T3, T6), hostile-input, oracle-hunter (A1) |
| SIGTERM drain misses streaming sessions (billed to nobody) | 3: entry-point-tracer (T3, T4), invariant-hunter (I11), concurrency |
| Admin grant is the only writer not normalising email | 2: entry-point-tracer (T9, T12) |
| `/api/internal/models` ungated unlike its three siblings | 3: entry-point-tracer (T9), invariant-hunter (I9), oracle-hunter |

That the top item was found four times by four unrelated strategies, each verifying it by
*running* the WHATWG parser rather than reasoning about it, is the single most reassuring
result in the run.

---

## Best: entry-point-tracer

**It found the most, it found the most severe, and its structure is the one that
generalises.**

The strategy is simple to state: enumerate every entry point into the system (it found 88),
then trace each one hop by hop through every layer it touches, and look specifically at the
*joints* between layers rather than inside them. That framing is why it won. Its own
closing line on the transcribe path names the thesis better than I could: every individual
layer is defensively written, and all the failures are at the joints — the reservation and
the charge use different units of duration, the balance check and the deduction share no
state, the deduction's failure signal has nowhere to go, and the fail-closed duration
backstop was applied to four adapters and not the other four.

It produced the two most severe findings in the entire run, neither of which any other
hunter reached:

- **Login CSRF** (T10). A plain link with the *attacker's* license key silently signs the
  victim into the attacker's account — no POST, no form, no JS on the attacker's side.
  It traced why both of better-auth's CSRF defences structurally miss, and followed through
  to the consequence: the victim then buys credits into the attacker's wallet while
  `/api/customer/profile` hands them the attacker's key in plaintext.
- **Unrecoverable redirect-loop lockout** (T11). Middleware admits on cookie *presence*;
  the page checks session *validity* and bounces back; neither clears the cookie. Rotating
  `BETTER_AUTH_SECRET` puts every logged-in user into it at once, and they cannot reach
  sign-in or sign out to escape.

Its unique-finding count is the highest by a wide margin: the Stripe-customer binding by
unverified email match, the "Refund Only" button that revokes anyway via the webhook it
fires, the migrations that commit before two build steps that can fail, the admin-grant
email normalisation gap, the `23505` detection made dead by a drizzle upgrade, the missing
`return` in sign-out. Several of these are cross-*system* seams — code and Stripe, code and
Vercel's deploy ordering — that a strategy confined to reading files cannot see by
construction.

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
executable repros**, 108 files. It is the only entrant with a 100% repro rate, and that is
not an accident of scoring — its whole method is to construct an input and run it, so a
finding either reproduces or it does not survive. If you want findings a skeptic cannot
argue with, this is the strategy.

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

**git-signal-hunter** (11/3/6). Mines history — churn, reverts, bug-fix commits, comment
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

**concurrency-hunter** (3/2/3). Hunts races, TOCTOU, and ordering bugs. Low volume, but its
verification discipline was the best in the field — its verifiers confirmed, downgraded,
*and refuted* candidates with equal willingness, and corrected its own parent's framing
more than once. *Con:* only 17 files directly examined; a narrow thesis that this codebase
rewarded only in the billing path.

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

**0 confirmed. 15 files. The most expensive setup of any entrant.**

The thesis is respectable: mutate the code, run the tests, and every mutation that survives
marks a behaviour nothing pins. Surviving mutants are test gaps, and test gaps are where
bugs live. It needed its own git worktree and a `node_modules` symlink to run safely, which
it did correctly and cleaned up after — no complaints about execution.

It fails because **the thesis presupposes a test suite, and this codebase does not have one
in the places that matter.** You cannot learn anything from a surviving mutant in code that
has no tests at all: every mutant survives, and the signal is uniformly zero. Repeatedly,
the finding it would have made was already available more cheaply by just reading the file
and noticing there was no test. Its reach was the narrowest in the run — 15 of 210 files —
because running the suite per mutation is slow, and that cost bought nothing here.

To its considerable credit, it said so. Its scorecard reads "came up dry: yes (on test
gaps) / no (on live bugs)" — it reported honestly that its actual strategy produced nothing
and that its 6 repros came from bugs it stumbled into while mutating, which is not the same
achievement. That honesty is worth more than a padded scorecard, and it is why I rank it
last on *fit* rather than on *conduct*.

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
