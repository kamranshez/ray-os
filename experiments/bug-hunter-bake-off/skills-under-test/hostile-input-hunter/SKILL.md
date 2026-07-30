---
name: hostile-input-hunter
description: Hunt bugs in EXISTING code by attacking its input surfaces with a systematic catalog of hostile and boundary values — the red-team, input-driven complement to reading code structurally. Enumerates every surface that accepts outside data (API params, form fields, file uploads, CLI args, env/config, webhook payloads, parsed file formats, query strings, anything deserialized), then walks a fixed catalog of adversarial inputs through each code path and runs the ones that are cheap to run. Use this whenever the user wants to know what inputs break their code: "bug hunt", "fuzz this", "what inputs break it", "red-team my API", "edge case hunt", "find the input that crashes this", "what happens if someone sends garbage", "test this against bad data", "is this endpoint safe", "find validation holes", "what did I forget to validate", "hunt for injection/IDOR/authz bugs", or any request to audit an existing codebase from the attacker's side rather than the author's. Reach for it even when the user does not say "fuzz" — if they are asking what could go wrong with the data coming in, this is the skill. NOT for reviewing a diff, branch, or pull request (that is /code-review, which is diff-scoped by design); this hunts code that already shipped. Intended for the user's own codebases and authorized security testing.
---

# Hostile Input Hunter

Developers test the inputs they imagined. Bugs live in the inputs they did not.

That asymmetry is the whole thesis of this skill. A team writes validation against the shape of data they pictured while writing the feature, and their tests reuse the same imagination. Everything outside that picture reaches production untested. So instead of reading the code and asking "does this look right?", you start from a fixed catalog of hostile values and ask "what does this code do when it meets *this*?" A catalog beats inspiration because it is exhaustive exactly where intuition is spotty — nobody spontaneously remembers zero-width joiners, `-0`, or February 29th, but a checklist does, every time, on every surface.

Two rules keep this from degenerating into a list of theoretical complaints:

**The interesting inputs are the ones that pass the first check.** An input rejected at the edge with a 400 is the system working. The bug is the input that satisfies the validator and then violates an assumption three layers down — a string that passes a length check and then blows a database column, an ID that passes a format check and belongs to another user, a number that passes `isFinite` and then overflows a JSON serializer. Hunt the survivors, not the casualties.

**Run it when you can.** Prediction lies; execution does not. Any pure function, parser, validator, formatter, or serializer can be called from a scratch script in under a minute. A finding you executed is worth ten you reasoned about, and it arrives with its own repro attached. Reasoning is the fallback for code you cannot cheaply invoke, not the default.

## Effort

The user picks, or you infer from how they asked. Default to `quick` unless they say "thorough", "deep", "exhaustive", "everything", or name a small enough target that depth is free.

| | Surfaces | Catalog | Verify | Prove |
|---|---|---|---|---|
| **quick** | top 3 by blast radius | highlighted rows per surface type | 1 verifier per finding | repro for CONFIRMED where a script is cheap |
| **deep** | every surface enumerated | every applicable category, per surface | 1 verifier per finding + intent check | runnable repro required for every CONFIRMED |

Announce the mode and the surface count before you start fanning out, so the user can redirect you before you spend the tokens.

---

## Phase 1 — Surface enumeration

Spawn **one** agent to map the attack surface. This is a single agent, not a fan-out, because the point is one coherent inventory with no double-counting.

```
Map every input surface in this codebase — every place data from outside the
process enters it. Work from the code, not from documentation.

Search for and enumerate:
- HTTP handlers: route params, query strings, JSON/form bodies, headers,
  cookies, content-type negotiation
- File uploads and any parser fed by them (images, CSV, XML, YAML, zip, PDF)
- CLI arguments and stdin
- Environment variables and config files read at startup or runtime
- Webhook receivers and third-party callbacks
- Message queue / job payloads
- Anything deserialized: JSON.parse, pickle, YAML.load, protobuf, msgpack
- Database rows written by another system or an older version of this code
- Inter-service RPC boundaries

For each surface return:
  id           short slug, e.g. "api-user-update"
  entry        file:line of the handler or parse call
  inputs       each named field/param with its declared or inferred type
  validation   the FIRST validation layer it passes through (file:line), or
               "none found"
  reaches      what it ultimately touches — DB write, filesystem, shell,
               external HTTP, template render, another user's data
  blast        HIGH if it writes data / touches auth / crosses a trust
               boundary; MED if it reads sensitive data; LOW if it is
               read-only public data
  runnable     YES if the parsing/validation logic can be invoked directly
               from a script (name the function), NO if it needs a live
               server or DB

Group surfaces into CLUSTERS of 3-6 that share a validation layer or code
path, so one hunter can attack them together without redundant reading.

Also report: how you searched, and any area you could not map (generated
code, vendored deps, a framework whose routing you could not resolve). The
coverage ledger depends on you being honest about the gaps.
```

Keep the returned inventory verbatim. It is both the work list for Phase 2 and the coverage ledger for Phase 5 — you cannot report what you did not cover unless you first wrote down what existed.

---

## The input catalog

This is the payload every hunter carries. Do not improvise a replacement; the value here is that it is fixed and complete. Skip rows that cannot apply to a surface's types, and say in the report which categories you skipped and why.

**Strings**
- empty `""`, whitespace-only `"   "`, `"\n"`, `"\t"`
- very long: 10KB, 1MB, 10MB (does it hit a column limit, a body limit, a memory ceiling, a regex backtracking cliff?)
- unicode: emoji, combining characters, RTL marks `‮`, zero-width `​`, homoglyphs, astral-plane chars that break naive length/slicing
- null bytes `"a\x00b"` (truncation in C-backed libs, filesystem calls)
- path traversal `"../../etc/passwd"`, absolute paths, Windows `..\\`, URL-encoded `%2e%2e%2f`
- format-string `"%s %n"`, template-injection `"{{7*7}}"`, `"${jndi:...}"`
- HTML/JS `"<script>"`, SQL `"' OR 1=1--"`, shell `"; rm -rf /"`, regex metachars `".*"`, `"("`
- case variants where comparison matters; leading/trailing whitespace where identity matters
- valid-looking-but-wrong: `"0"`, `"false"`, `"null"`, `"undefined"`, `"NaN"`, `"-"`, `"e"` — strings that a loose parse turns into something surprising

**Numbers**
- `0` (and every falsy-zero check that treats it as absent)
- `-1`, negatives where only positives were imagined
- type MIN/MAX, `MAX_SAFE_INTEGER + 1`, 2^53, 2^63
- `NaN`, `Infinity`, `-Infinity`, `-0`
- floats where money or counts live; `0.1 + 0.2`; a value that survives arithmetic but fails equality
- integer-as-string `"42"` and string-as-integer coercion in the other direction
- precision loss at serialization boundaries (a 64-bit ID through JSON becomes a lossy double)
- units: cents vs dollars, ms vs s, bytes vs KB — a correct number in the wrong unit

**Collections**
- empty list/map (does an aggregate divide by length? does a `[0]` index?)
- exactly one element (off-by-one in join/pagination/"and" formatting)
- duplicates where uniqueness is assumed
- deeply nested (recursion depth, stack overflow in a validator)
- self-referential / circular where the code serializes
- 100k elements (N+1 queries, unbounded memory, a timeout that half-commits)
- heterogeneous types inside a list the code assumes is uniform
- `null` as a member rather than as the collection

**Time**
- epoch `0`, negative timestamps, year 1970 vs 1900 defaults
- far future (2099), and the 2038 signed-32-bit boundary
- Feb 29 on a leap year, Dec 31 / Jan 1 across a year boundary
- DST transitions: the hour that does not exist, and the hour that happens twice
- timezone-naive values mixed with aware ones; UTC assumed where local was sent
- client clock skew: an "expires_at" in the past on arrival, a token issued "in the future"
- durations that are zero or negative; end before start

**Identity and state**
- the same request twice (idempotency — does it double-charge, double-send, double-insert?)
- IDs that do not exist, IDs that are malformed, IDs of the wrong entity type
- **IDs belonging to another user** — this is the IDOR check and it is the single highest-value row in the catalog; test it on every surface that takes an ID
- soft-deleted or archived records treated as live
- stale references: an ID valid when the page rendered, deleted before submit
- an actor whose permissions changed mid-session; a revoked token still cached
- a record in a state the transition does not allow (refund an unpaid order)

**Sequencing**
- multi-step flows executed out of order, or with a step skipped
- back-button replay, double-submit, two tabs racing the same form
- session expiring between step 2 and step 3
- webhook arriving before the record it references exists (ordering is not guaranteed)
- retry after a partial failure — what did step 1 leave behind?
- cancel / abort mid-operation

---

## Phase 2 — Fuzz

One hunter subagent per cluster, all spawned in parallel. Pass each hunter its cluster's inventory rows verbatim plus the full catalog.

```
You are attacking input surfaces from the outside. Your cluster:

<the surface rows for this cluster, verbatim>

Method, per surface, per applicable catalog row:

1. Trace the input from the entry point inward. At each hop ask: is it
   REJECTED, SANITIZED/COERCED, or does it FLOW THROUGH unchanged?
2. Ignore what is rejected at the edge — that is the system working. Your
   targets are inputs that PASS the first validation layer and then violate
   a deeper assumption. A string that passes a length check and overflows a
   DB column, an ID that passes a UUID regex and belongs to another tenant,
   a number that passes isFinite and loses precision in JSON — these are
   the findings.
3. Where the surface is marked runnable=YES, WRITE A SCRATCH SCRIPT AND
   ACTUALLY CALL IT with the hostile value. Do not predict what a parser
   does; invoke it. Put scratch files in a temp dir, not the repo.
4. Note explicitly which catalog categories you skipped for a surface and
   why (e.g. "no time inputs on this endpoint").

For each candidate return:
  surface       the surface id
  input         the EXACT value, copy-pasteable, not a description
  path          entry → hop → hop → where it detonates, with file:line
  detonation    the user-visible consequence
  class         authz-bypass | injection | corruption | crash | resource |
                error-quality
  executed      YES (with the observed output) or NO (reasoned only)

Severity honesty matters more than volume: an input that produces an ugly
500 instead of a clean 400 is error-quality — real, but LOW. Do not dress
it up as a crash. A pile of inflated findings makes the whole report
untrustworthy and the genuine authz bug gets lost in it.

Return an empty list if the cluster is genuinely well-guarded. That is a
legitimate and useful result.
```

---

## Phase 3 — Verify, with the ladder inverted

Spawn one verifier per candidate, in parallel, each blind to the others.

Diff review can afford to be generous — flag anything plausible and the author checks it in thirty seconds. Off-diff hunting has no author standing by. Every false positive costs someone a full investigation from cold, and a report where half the entries dissolve on inspection gets ignored entirely, including the true half. So the default verdict is REFUTED and the finding must earn its way up.

```
Adversarially verify one claimed input bug. Assume it is WRONG and try to
prove that. Read the actual code; do not take the claim's word for the
control flow.

Candidate: <input, path, detonation, class, executed>

Verdicts:

CONFIRMED — requires ALL of:
  (a) the exact input value, reproducible as written
  (b) the actual code path it travels, quoting the lines that fail to stop it
  (c) a user-visible detonation you can name concretely
  A finding whose "executed" evidence you can reproduce goes straight here.

PLAUSIBLE — the mechanism is real and the path is right, but the trigger
  depends on runtime state you cannot pin (a config value, a specific DB
  row, a race). Say precisely what would confirm it.

REFUTED — the default. Choose it when: a guard the hunter missed catches
  the input (quote it), the framework coerces or rejects it upstream
  (quote it), the type system makes the value unconstructible, the path
  described does not exist, or the "bug" is cosmetic with no observable
  effect.

Then the intent check — off-diff code has no PR description, so
deliberate decisions look identical to mistakes:
  - `git log -L <line>,<line>:<file>` or `git blame` on the relevant lines
  - read surrounding comments and any test that covers this input
  - if a test asserts the current behavior, or a comment explains it, the
    behavior is INTENTIONAL — say so, and downgrade unless you can argue
    the intent itself is wrong

Return: verdict, evidence (quoting lines), intent (INTENTIONAL /
UNINTENTIONAL / UNCLEAR + what you based it on), and a corrected severity
if the hunter's class was inflated.
```

---

## Phase 4 — Prove

This variant has a structural advantage over every other way of hunting bugs: **the finding is already an input.** There is no gap between "I believe this is broken" and "here is the thing that breaks it." Close it.

For each CONFIRMED finding, produce a runnable repro — a failing test in the project's own framework where one fits, otherwise a standalone script or a `curl` command. In `deep` mode this is required; in `quick` mode, do it wherever a script is cheap.

Then take the result seriously in both directions. A repro that works turns a claim into a fix-ready ticket, which is the entire point of hunting off-diff: a finding with no owner and no proof rots in a backlog, a finding with a failing test gets fixed. And a CONFIRMED finding you *cannot* reproduce is telling you something — an input bug that will not detonate on demand was probably not confirmed. Downgrade it to PLAUSIBLE and say the repro failed. Reporting that honestly is worth more than the finding was.

Never commit repro scripts or leave them in the repo unless the user asks. Temp dir, then reference the path.

---

## Phase 5 — Report

Rank by what actually hurts, not by how clever the finding is: authorization bypass and IDOR first (someone reads or writes another user's data), then injection, then silent corruption (wrong data persisted — worse than a crash because nobody notices), then crashes and resource exhaustion, then error-quality. Within a tier, repro-backed above CONFIRMED above PLAUSIBLE.

Use this structure exactly:

```markdown
# Hostile input hunt — <target>

**Mode:** quick | deep
**Surfaces enumerated:** N — **fuzzed:** M
**Candidates:** C → **confirmed:** X, **plausible:** Y, **refuted:** Z
**Repros produced:** R

## Summary
Two or three sentences: the worst thing found, and the pattern behind it if
there is one (e.g. "validation is thorough at the API edge and absent on
the webhook path").

## Findings

### 1. <one-line claim> — CONFIRMED · authz-bypass
**Surface:** api-user-update (`routes/user.ts:41`)
**Input:**
```
{"id": "<another user's uuid>", "email": "attacker@example.com"}
```
**Path:** `routes/user.ts:41` accepts `id` from the body → `validateUser`
(`lib/validate.ts:12`) checks UUID format only → `db.users.update`
(`db/users.ts:88`) writes without an owner predicate.
**Detonation:** Any authenticated user can change any other user's email,
which the password-reset flow then trusts. Full account takeover.
**Intent:** UNINTENTIONAL — no test covers cross-user ids; `git blame`
shows the owner check was in the handler until `a3f9c21` moved routing.
**Repro:** `/tmp/hunt/idor-user-update.sh` (executed: 200 OK, row changed)
**Fix direction:** scope the update by `session.userId`, not the body id.

### 2. ...

## Refuted
One line each, with the guard that saved it — so the same candidate is not
re-raised next hunt.

## Coverage
| Surface | Blast | Fuzzed | Categories applied | Skipped (why) |
|---|---|---|---|---|
| api-user-update | HIGH | yes | strings, numbers, identity, sequencing | time (no date inputs) |
| upload-avatar | HIGH | no | — | out of scope for quick mode |

**Not examined:** <surfaces enumerated but not fuzzed, and anything Phase 1
could not map>

This section is not boilerplate. "No findings" in an area you never opened
reads as "that area is clean" and the next person trusts it. Say what you
did not touch.
```

---

## Staying honest

A few failure modes worth naming, because each one quietly destroys the value of the whole hunt:

**Padding.** Ten low-severity findings do not add up to one real one; they bury it. If the honest answer is "one IDOR and the rest is well-guarded", report that.

**Describing instead of instantiating.** "A very long string could overflow" is not a finding. `"A" * 10485760` at `routes/x.ts:14` producing a 30-second hang is.

**Fuzzing the validator instead of the system.** If every catalog row you tried died at the edge, you found a good validator, and the right move is to go deeper into the surfaces the validator passes — not to write up the rejections.

**Silent scope collapse.** Fanning out over three surfaces and reporting as if you covered the codebase is the most damaging thing this skill can do. The coverage table is the antidote; fill it in truthfully even when it is unflattering.
