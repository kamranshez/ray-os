# Task-type playbooks

Concrete sequences for the recurring session types, distilled from the veteran. Cross-references: the two checklists live in `README.md`; danger tripwires in `danger-and-gotchas.md`.

Skill names below are verified present in this environment unless flagged. Reference `AGENT-INSTRUCTIONS.md` §Secrets / §Credit System / §Service Layer rather than re-reading them here.

---

## 1. "Implement the following plan: …" (most common)

**First moves, before any code:**
1. **Read the plan against current main, not memory.** Grep every symbol/path the plan cites — plans are often written a session or more before you run them and main has moved. If the plan says "fix X at `lib/ai-models.ts`" and that path doesn't exist (it's `lib/ai/models.ts` now; services moved to `lib/api/services/*.ts`), the plan is stale, not you.
2. **Spawn `general-purpose` explorer subagents to confirm blast radius** (NOT `Explore`-type — those go idle in teams). Ask them "where is X actually called from / does this column exist / what's the current signature." Keep exploration in subagents so your context stays clean.
3. **Create an isolated worktree off fresh origin/main** (mechanics below). Never work in the main checkout.
4. **Decide the schema question now:** if the plan edits `nextjs/src/db/schema/`, pre-commit to `pnpm db:generate` + committing the SQL.
5. **Identify the verify surface:** new user-facing flow (→ browser/GIF later), pure backend, or schema (→ auto-migrates). This shapes the whole session.

**Worktree mechanics (verified — worktrees live at `.claude/worktrees/<name>/`):**
```
git worktree add .claude/worktrees/<name> -b worktree-<slug> origin/main
```
Branch naming in practice: `worktree-<slug>`, or `feat/<slug>` / `fix/<slug>`.
- **node_modules trap:** a fresh worktree's `nextjs/node_modules` sometimes comes up EMPTY (pnpm decides "already up to date" but doesn't populate). Symptom: build/typecheck explode on missing modules in a worktree that looks fine. Fix: `pnpm install` in the worktree, or symlink its `nextjs/node_modules` to the main repo's populated one. **Never `npm install`.**
- `nextjs/.npmrc` keeps `shamefully-hoist=true` (verified) — if a build dies with `ERR_MODULE_NOT_FOUND` on a package nothing imports (picocolors, js-yaml, unist-util-visit, estree-util-value-to-estree), it's the fumadocs generated-config hoisting issue, not your code.
- Teardown after merge: `git worktree remove .claude/worktrees/<name>` (or `git worktree prune`). Stale entries accumulate; clean up.
- **Don't `git stash` to get a clean branch when main is dirty** — Ray keeps editing and `stash pop` can 3-way-merge in a way that looks like data loss. Use a worktree; it touches nothing in his tree.

**Build / verify before PR:**
- `cd nextjs && SKIP_ENV_VALIDATION=1 pnpm build` — the signal that matters. Run it **incrementally** as you go.
- **Do NOT trust the Vercel PR preview check** — fails by design (no preview secrets).
- `tsc --noEmit` was once a 13-min / OOM-at-8GB monster (hotspot `nextjs/src/lib/mcp/tools/sources.ts`, zod/MCP-SDK inference). Two PRs attacked it. **Current cost unmeasured — treat as an open question**; prefer `pnpm build`'s typecheck over a standalone `tsc --noEmit` unless you need isolated type errors, and expect it may still want a large heap.
- Never list "run migration against prod" as a step — `vercel-build` runs `drizzle-kit migrate` before `next build` automatically (verified). Committing the SQL is enough.

**Reflexive mid-implementation checks** (things plans never warn about) — these are the PRE-COMMIT checklist in `README.md`. The big ones: schema edit → `db:generate`; new gated page → outer/inner `DashboardLayout` pattern; catch block → `console.error`; new env var → REQUIRED not optional; balance mutation → audit row; chat route → Edge-safe.

**`/implement-feature`** is the heavy L3 loop that does all of this end-to-end (plan → worktree → adversarial review/fix loop → localhost Chrome verify with per-flow GIFs → PR → auto-merge small/escalate big → monitor prod 1h + auto-hotfix). Reach for it when Ray hands a finished spec and says "ship it end to end." (⚠️ `/implement-task`, the lighter scoped-build variant, is referenced in older sessions but is NOT in the current skill list — confirm it still exists before relying on it; `/implement-feature` is the confirmed one.)

---

## 2. PR lifecycle + multi-round review-fix loop (2nd most common)

**Worktree-done → merged:**
1. Commit (message ends with the mandated `Co-Authored-By` + `Claude-Session` trailers — harness supplies them).
2. `git push -u origin <branch>`.
3. `gh pr create --base main --title "<type(scope): summary>" --body "..."` — conventional-commit title (`feat(email): …`, `fix(security): …`); body ends with the `🤖 Generated with Claude Code` trailer.
4. **Ignore the red Vercel preview check.** Real gates = review bots + local `pnpm build`.
5. Merge is **squash**. Small/low-risk → you merge (`gh pr merge <n> --squash`). Big/risky → escalate; Ray often merges himself ("move to main" / "merge to main" = his hand-off signal).

**Merge traps:**
- **Stacked PR + `--delete-branch` = auto-closed child** (GitHub closes, doesn't retarget). Merge the base WITHOUT `--delete-branch`, or rebase the child onto main first. Recovery: cherry-pick the child's commit onto a fresh branch, new PR.
- **A follow-up fix can strand on a deleted branch** (happened #448/BUG-087 — sanitization commit landed after squash-merge, so main shipped raw PII in `console.error`). After a loop pushes commits, re-check the PR isn't already merged.

**Review bots + triage:** Codex (chatgpt-codex-connector), Greptile, CodeRabbit, plus your own `/code-review`.
- **Verify every finding against the code before acting.** Classify **CONFIRMED** / **PLAUSIBLE** / **FALSE-POSITIVE** by reading the cited lines on the current branch. Bots false-positive regularly — never fix what you didn't re-derive.
- **Codex is the highest-signal automated reviewer here** (strong prior; Ray leans on it — many "fix Codex P1/P2 findings on PR #N" sessions). CodeRabbit skews to style/nit volume. ⚠️ Ray asked for a formal Greptile-vs-Codex comparison on 2026-06-30; the written conclusion was NOT persisted to memory — if he asks again, re-run the comparison rather than quoting a verdict.

**`/code-review` effort levels:** low/medium (routine PR, default — medium is most-used) → high/max (big/risky: voice, billing, security, rewrites; "find as many bugs as you can then verify" — expect uncertain findings needing your confirmation) → **ultra** (deep multi-agent cloud review, billed, **user-triggered only — you cannot launch it**). `/pr-review-loop` = babysit-a-PR-to-merge (fix bot findings, re-request, merge on a quiet window; e.g. `/pr-review-loop pr 616`). `/deep-bug-hunt` = whole-repo/subsystem hunt, not a single diff (heavy: millions of tokens, optionally files deduped GitHub issues). `/backlog-burndown` = convert a batch of open issues into reviewed PRs, one lane each.

**Keeping the fix-loop from spiraling** (voice PR #508 went 3 rounds where each round's fixes were themselves buggy):
- **Each round reviews the FIX COMMIT, not the original diff** — state which commit is under review.
- **Triage by introduced-by-this-work vs pre-existing.** Most max-effort findings on a hardening PR are pre-existing/plan-deferred — split those into separate follow-ups; don't fix them in the same branch. This stops the fractal expansion.
- **Convergence:** stop when new findings are only pre-existing, nits, or low-blast-radius plausibles — i.e. no NEW confirmed correctness/security regression from your own fixes. Three rounds is the most that's ever been needed; on round 4 still finding real regressions in your fixes → the approach is wrong, redesign.

**Deploy-and-monitor ritual (do it every push to main, don't ask first):**
- Use the **vercel-monitor skill** for status. Do NOT spawn a subagent ("Prompt is too long") and do NOT use the Vercel MCP `list_deployments` (dumps 20 objects/poll). `vercel ls` puts its status table on **stderr**. Scope is `theramjad`.
- **Ready ≠ healthy** — runtime errors only surface under traffic. When it flips to Ready, arm the 1h error tail (script in global CLAUDE.md: dedup'd `vercel logs --level error --since 2m` loop, Monitor `timeout_ms: 3600000`). On an error line, `vercel logs --level error --since 1h --expand`. Silent hour = healthy.
- **No prod deploy ~10 min after merge → dropped webhook** → push an empty commit (`git commit --allow-empty -m "chore: re-trigger prod deploy"`). Never `vercel --prod` from the monorepo root (tars node_modules/.next/.git → 7.6GB EPIPE).

---

## 3. Verification campaigns ⚠️ (machinery REFACTORED — verified 2026-07-05)

The old scheme (`verification/GOAL.md`, `verification/INDEX.md`, single `status:` field) is **gone**. Ignore `project_verify_*` memories describing it. Current layout (verified):
- **Source of truth: `verification/AGENTS.md`** — read it first, every time (invariants, data model, golden rules, procedures). Also present: `REGISTRY.md` (generated view), `CLAUDE.md`, `ENVIRONMENT.md`, `flows/`, `issues/`, `scripts/`, `evidence/`, `archives/`.
- **Two driving skills:** **`reconcile-flows`** (run AFTER shipping code — flags drift via line-edges, discovers gaps, reconciles merged fixes, updates the queue; does NOT run flows) → then **`verify-flows`** (the executor — sets up env, runs each flow in its own subagent, records a GIF, stamps result; does NOT decide staleness). Also `seed` (fixtures) and `discover-user-paths` (find new flows).
- **Unit = a flow file** `verification/flows/<scope>/<ID>-<slug>.md`: YAML frontmatter + `## Spec` + an **accumulating** `## Run history` table + dated `## Run <date>` sections. Runs accumulate, never overwrite.
- **Two orthogonal axes:** `result:` (untested|passing|partial|failing = last run) and `stale:` (true|false = code drifted, retest) — the old single status conflated these. Plus `needs_data:` (seed a fixture) and `wont_run:` (intentionally skipped). **Runnability is COMPUTED by `scripts/build_registry.py`, never stored** → 🟢 runnable-now / ♻️ needs-retest / 🔒 blocked-capability / 🔧 needs-data.

**The loop:** one flow per subagent, **strictly sequential for browser flows** (see below). Typical: `reconcile-flows` → `verify-flows` (drain 🟢 runnable-now).

**Hard gotchas:**
- **ONE shared Chrome + ONE Playwright.** Two browser subagents at once collide on the same tab/session — clicks land in the wrong flow. Browser flows run **one at a time**. A flow's `surface:` field says browser vs REST; REST/curl flows parallelize freely (run them alongside a single browser flow, never two browsers). Never run a role-mutating flow (promote/transfer) concurrently with a member-side flow.
- **Subagents fight your stamps:** they revert `verified_commit` to git HEAD (bake "verified_commit MUST be <X>, do NOT run git rev-parse" into the prompt), use non-canonical status values, and botch new-flow IDs (created an ACT-96 file with `id: ACT-62`). Verify/fix stamps on disk after each run.
- **Batched-subagent edit-loss:** a subagent running several flows sometimes doesn't persist its `.md` frontmatter/run edits (GIFs + gh issues persisted, the file didn't). Prefer one flow per subagent; if batched, grep `^## Run <date>` + the result field afterward and re-stamp.
- **Tell parallel subagents NOT to run `build_registry.py`** — concurrent runs race the registry file. Regenerate ONCE after the batch.
- **Worktree `ENVIRONMENT.md` is untracked** — exists only in the main repo, not the verify worktree. If missing, `build_registry.py` defaults to env-unknown/free and shows almost nothing runnable. `cp` it in, then rebuild.
- **Trust on-disk frontmatter, not task-notification text** — a finished subagent gets re-woken by a sibling's completion and re-reports.

**GIF vs snapshot:** a GIF is required for a `verify-flows` run (the evidence artifact; the `collect-gif.sh` Downloads/TCC move is mandatory — see AGENT-INSTRUCTIONS.md §GIFs). A **snapshot** (browser a11y tree, inline) suffices for ad-hoc investigation/bug-repro evidence — don't do the full GIF ritual for a debug check. ⚠️ **Background-tab trap:** the Claude-in-Chrome tab is backgrounded, so rAF animations (framer mount/whileInView, count-ups) freeze at frame 0 — a "blank" screenshot may be a fine page. Check `document.visibilityState`/computed opacity; inject force-reveal CSS to screenshot reveal-animated content.

**Know when to stop:** the discover loop returns MORE new flows each wave (+44/+87/+99) — convergence to "nothing new" is unreachable. Practical done = "the agent-runnable, externally-observable surface is exhausted," i.e. new yield is fixture-blocked or unit-test-territory. Write the hand-off; don't loop forever because a halt-gate says so.

---

## 4. Seeding test-org (skill: `seed`)

`test-org` (see README day-one for ids) is your only sandbox. The `seed` skill drives `/api/v1/seed/*` Hono routes (`nextjs/src/lib/api/hono/routes/seed/`: agent, billing, email, inbox, oauth, scenario, echo). Manufacture: zero-credit org, subscription past_due, two-actor inbox (customer reply on a ticket assigned to you), verified email domains, backdated agent `pendingDeleteAt`, expired OAuth, soft-deleted agents — without a second human actor or raw SQL.
- **Guardrail (verified):** every seed route hard-asserts `org.slug === "test-org"` (`SEED_ORG_SLUG`, `assertSeedOrg` in `seed/shared.ts`) → returns `SEED_ORG_FORBIDDEN` otherwise. It **cannot** touch `ray-amjad-ltd`. Still never touch that org manually.
- **Teardown:** each seed call returns a `previous`/snapshot — capture it and call restore when done. Run the seed-set-and-capture AND the restore **in subagents** (keeps orchestrator context clean).
- ⚠️ Email opt-out is now in `contacts.opted_out_at` — the old "reset Contacts→Status to New" teardown trick is OBSOLETE (that was BUG-102, fixed). Re-enable a STOP'd sender by clearing that column via DB; there's no UI path by design.

---

## 5. Live prod debugging playbooks

For each: how to get logs, the recurring signatures, fix-or-escalate.

### Voice / LiveKit
- **Architecture:** separate app in `agent/` — `main.ts` (entry, greeting, connect), `agent.ts` (tools, timers, 60s warning), `providers.ts` (realtime S2S model factory). Backend dispatches server-side via `AgentDispatchClient.createDispatch(room, "agentstack-voice-agent", {metadata})`.
- **Deploy:** separate from Vercel. `.github/workflows/deploy-voice-agent.yml` auto-redeploys on push to main touching `agent/**` (built from `agent/Dockerfile` via `lk agent deploy`). LiveKit projects: `agentstack-prod` and `agentstack-preview`.
- **Logs:** `lk agent logs --id <id> --project agentstack-prod` STREAMS NEW logs only → start the tail FIRST, then trigger a real call. `lk agent status --id <id> --project agentstack-prod` (needs `--id`) — but "Running / 100% uptime" can still mean every job crashes in entry(). Reproduce headlessly: `lk dispatch create --room R --agent-name agentstack-voice-agent --metadata '{...}'` — ⚠️ but a dispatch with NO participant ALWAYS throws region-info (OpenAI's socket connects lazily, empty room has no media region), so test with a real participant.
- **Classic silent-call causes:** (a) **fictional model IDs** not mapped to real provider ids → `code 1008 model-not-found` (e.g. `gemini-3.1-flash-live`; `gpt-realtime-1.5-mini` isn't real — real: `gpt-realtime-1.5`, `gpt-realtime-mini`, `gpt-realtime`, `gpt-realtime-2`). (b) **Gemini 3.1 silently ignores `generateReply()`/`updateInstructions()`** — greeting + warning use generateReply, so 3.1 = silent, no error; use `gemini-2.5-flash-native-audio-preview-12-2025`. (c) **missing CA certs in the Docker image** — `node:22-slim` ships without ca-certificates → `@livekit/rtc-node` TLS handshake to the region endpoint fails → `ConnectError: failed to retrieve region info` → silent (worker still REGISTERS fine over Node TLS). Fix: `apt-get install -y ca-certificates openssl` in the runtime stage. (d) **connect ordering:** `await ctx.connect()` BEFORE `session.start()` (start's auto-connect runs under `Promise.allSettled` which swallows failures). (e) **call-lock not released on startup throw** → "already has an active voice call"; register disconnect handlers (POST `/api/voice/end` → `finalizeVoiceCall`) before any throwing await.
- ⚠️ Model ids and SDK versions **drift fast** — re-check real provider ids before trusting these. Turn-detection is known-fragile (Turn Detector v1 integrated 2026-06-21, reverted 2026-06-22 after it "fucked up the turn system"). Test real end-to-end calls; don't trust code-only.
- **Fix-or-escalate:** model-mapping / Dockerfile / ordering → fix. SDK bumps → verify a real call before merge.

### Inbound/outbound email + SendGrid
- ⚠️ **Addresses are now FLAT** (verified `nextjs/src/lib/api/services/channels.ts:262`): `${baseLocalPart}-${nanoid(8)}@${AGENTSTACK_EMAIL_DOMAIN}`, lowercased. A flat localpart matches the single configured SendGrid Parse host `agentstack.email` → inbound WORKS (verified end-to-end 2026-06-27). The old `{slug}-{nanoid}@{orgId8}.agentstack.email` subdomain scheme (Parse dropped it silently — exact-host match, no wildcard) is gone.
- **Handlers:** inbound webhook `nextjs/src/app/api/webhooks/sendgrid/inbound/route.ts` (Basic Auth `SENDGRID_INBOUND_AUTH_USER/PASS`, timing-safe; matches on `emailAddresses.fullAddress` exact-equality). Processing in Trigger task `nextjs/src/trigger/handle-inbound-email.ts`.
- **Trace a missing email:** (a) recipient scheme flat vs legacy-subdomain (legacy = Parse drops silently); (b) MX resolves (NXDOMAIN = DNS — the `agentstack.email` Cloudflare zone needs a wildcard `* MX 10 mx.sendgrid.net`); (c) SendGrid Activity Feed / Parse settings for the drop; (d) the Trigger run for `handle-inbound-email`; (e) outbound → SendGrid activity + credit/rate-limit gate.
- **Test rig:** Gmail `fantasiesandfailures@gmail.com` (`mail.google.com/mail/u/3/`) ↔ `zz-fixtures-onfl@agentstack.email` (test-org). ⚠️ that sender is currently OPTED-OUT on zz-fixtures — clear `contacts.opted_out_at` via DB before re-running inbound from it. Round-trip ~30–60s.
- **Recurring bugs:** the **inverted per-agent rate limiter** (hourly limit passed as the Upstash token → raising the limit makes it STRICTER; default ≈1 email/hour, silently dropping the rest) — check if "agent only replies to some emails." Reply-loop guards (drop `Auto-Submitted` / `Precedence: bulk` inbound). Attachment filename collisions overwriting in R2.
- **Fix-or-escalate:** address-scheme / rate-limiter / loop-guard → fix. SendGrid account config (Parse hosts, domain auth) → Ray.

### Slack
- **Handler runs in Trigger:** `nextjs/src/trigger/handle-slack-message.ts`. Inbound webhook (signature-verified) enqueues the task; thread cache in Upstash Redis (7d TTL). Outbound = OAuth token + `chat.postMessage`.
- **Silent-bot debug:** (a) **OAuth SCOPES** (most common) — bot only replies to @mentions/DMs/threads it's in; missing `app_mentions:read` / `channels:history` / `groups:history` → silent. The inbound toggle disables with a "Reconnect Slack" CTA when scopes are missing. (Least-privilege work dropped `chat:write.public`.) (b) the Trigger run for `handle-slack-message`. (c) signature verification failing → webhook rejected before the task. (d) DM routing is one-agent-per-org (`handleDms`, atomic swap).
- **OAuth install "fails silently":** used to land on `/org/resolve?oauth_error=...` which dropped the param — now surfaced on the integrations page; check the callback + `oauth_error` handling.
- **Fix-or-escalate:** scope/routing/error-surfacing → fix. Re-connecting the workspace grant → Ray.

### Trigger.dev
- **Own deploy**, separate from Vercel (`mcp__trigger__deploy` / Trigger CLI). Does NOT auto-deploy with the Next app.
- ⚠️ **Env now syncs from Infisical, not Vercel** (verified `nextjs/trigger.config.ts` uses `syncEnvVars` + `InfisicalSDK`). It USED to use `syncVercelEnvVars()` which broke a deploy with `Invalid environment variables … NOTION_CLIENT_ID: Required` (2026-06-03). If a Trigger deploy fails env validation, the var is missing in **Infisical**, not Vercel.
- **Find/read a failed run:** Trigger MCP — `mcp__trigger__list_runs` (filter by task/status), `mcp__trigger__get_run_details` / `get_span_details` for the trace. Dashboard Observability → Runs (tasks: `handle-inbound-email`, `handle-slack-message`, `retrain-agent`, `analyze-session`). Failed deploys under Deployments → "Build failed."
- **Fix-or-escalate:** task logic → fix + redeploy. Env-validation → set the var in Infisical (you may write prod/staging) + redeploy.

### Vercel triage order
- **Build failure** (`Command "pnpm run vercel-build" exited with 1`): read the build log. Common: `ERR_MODULE_NOT_FOUND` (fumadocs hoist), un-runnable migration, type error, missing build-time env var. Load the **vercel-logs skill** before any ad-hoc `vercel logs` (non-obvious flag interactions hang) — but for the standard post-deploy tail use the pre-vetted script in global CLAUDE.md, don't load the skill.
- **Runtime 500** (Ready but errors under traffic): the "Ready ≠ healthy" case. `vercel logs --level error --since 2m`, then `--expand`. Classic: "column does not exist" (missing migration — the fce53d2 class), swallowed error with no `console.error`, Edge-runtime violation in the chat route.
- **Slow build** (crept to ~7 min): investigate on the dashboard's build-step timings, but it's NOT a correctness issue — don't block a merge on it (monorepo size + tsc cost).

---

## 6. Design variations + image-paste fixes (very common)

- **"Give me N variations on an HTML file/artifact"** (usually 5 or 10): produce a **single self-contained HTML artifact** (open in Chrome) with the distinct variations laid out for side-by-side eyeballing, all on the existing **light theme / design system**, and **mark your recommended option** (he asks for "your rec"). The `artifact-planner` and `frontend-design` skills help.
- **The "double down" pattern:** once he picks one, "generate 10 more like it" → a second artifact narrowing on the chosen one, then a third if needed. **Only then** "integrate into the main app." Don't jump to integration before he's picked.
- **When he wants to DECIDE, give him something clickable** (multiple-choice HTML he can copy answers back from, or `/spec-developer-v2`). When he wants to SEE, give variations. When he wants it BUILT, integrate the chosen one.
- **Image-paste "fix this":** read the image, find the exact component, fix the specific defect — **and check sibling pages/components for the same defect** (he usually means "fix it everywhere," even pointing at one instance).

---

## 7. Specs + the plans/ folder

- **Lifecycle dirs (verified):** `plans/draft/` → `plans/active/` → `plans/completed/` (42 completed), plus `plans/blocked-on-approval/` (parked pending Ray's go — NOT "next"), `plans/_lib/`, `plans/decisions/` (auto-spec decision HTML goes HERE, not `plans/`). Each plan is a numbered folder `NN-slug/` with `plan.md`. ⚠️ Memory says `plans/ready/` — that's now `plans/active/`.
- **"What's the next task / what plan is next?"** (a common Ray question): read `plans/active/` + `plans/draft/` **against reality**, not memory. Numeric order is file order, NOT strict priority. `blocked-on-approval/` items are not next. Give him what's genuinely actionable.
- **Spec authoring:** `/auto-spec <file-or-brief>` = autonomous two-agent interview + external-API research + codebase-grounded planning, using Ray's "digital twin" decision profile (answers as he would) → a ready-to-implement plan. `/spec-developer-v2` (and `/spec-developer`) interview HIM with sharp questions when he wants to drive the decisions. Both feed a plan file.

---

## 8. Codex tooling

- **`/codex-consult`** — three modes: `codex review` (independent diff review, pass/fail gate), `challenge` (adversarial, tries to break your code), `consult` (ask anything, session continuity). The "200-IQ second opinion" — reach for it on security/billing/correctness-sensitive changes, or when you and `/code-review` disagree and want a tiebreak. E.g. `/codex-consult xhigh <PR-url>`.
- **`/codex-app-control`** — drive Codex sessions/threads programmatically (list threads, send prompts, steer, interrupt, fork, approve). Use when ORCHESTRATING Codex as a worker, NOT for a one-shot consult.
- **The "grill an engineer about a proposed fix" pattern** (~80 sessions, 2026-05-28): Ray's adversarial-verification loop for a batch of review findings. For each proposed fix (a GitHub issue), an agent role-plays a skeptical senior — Reads/Greps the cited files to ask sharper questions, pressure-testing whether the fix is real and complete BEFORE it's implemented (catches the fix-loop spiral early). If handed a "grill this proposed fix" prompt, be genuinely adversarial and code-grounded — don't rubber-stamp.
