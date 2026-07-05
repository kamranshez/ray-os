# Danger zones + gotcha index

Ranked by real damage caused. For each: what happened, and the exact tripwire to check BEFORE the action. Then environment landmines and the stale-memory catch-list. Cross-ref the two checklists in `README.md`.

Secret-handling rules are in `AGENT-INSTRUCTIONS.md` §Secrets — read there; this only adds the incident context and the judgment.

---

## Danger zones (ranked)

### #1 — Prod DB writes / destructive SQL (highest)
The seed endpoints self-protect (hard-pinned to `test-org`), but **raw psql / PlanetScale-MCP writes do NOT.** Ray sometimes hands you live PlanetScale creds for a one-off (e.g. "delete this blog article directly from the DB") — that's authorization for **that action only**, not standing permission, and the creds are now in the transcript (flag that he may want to rotate).
**Tripwire before any DB write:** (a) am I on `test-org` or a real org? (b) is it reversible? (c) inspect the target row first, never batch, prefer a seed endpoint or a code fix over raw SQL. Prod DB reads this era used the **PlanetScale MCP** (`mcp__claude_ai_PlanetScale__planetscale_execute_read_query`, org `ray-amjad-ltd` / db `agentstack` / branch `main`). ⚠️ The MCP write token was **read-only (403 on writes)** as of late June — don't assume you can write via it. See "PlanetScale/psql" below for the read path.

### #2 — Schema edit without a generated migration (the fce53d2 incident)
**What happened:** schema TS was edited (2 cols on `subscriptions`, indexes, tz conversions) but `db:generate` was never run → zero `.sql` files. `vercel-build` runs `drizzle-kit migrate`, which replays only `.sql` files → **applied nothing** → `next build` compiled code referencing columns absent in prod → every page selecting `subscriptions` (analytics, API keys, billing) threw "column does not exist" **two days later** when a user hit it.
**Exact guard:** the instant you edit anything under `nextjs/src/db/schema/`, `cd nextjs && pnpm db:generate`, and the new `.sql` + `meta/*.json` are part of that commit. **The `.githooks/pre-commit` guard is NOT active** in this clone (`core.hooksPath` = default `.git/hooks`, verified) — do it manually. Also watch migration ORDERING on stacked/merged schema PRs — a reorder can strand a "never-runs" migration and block the whole deploy (PR #775 deploy-blocker).

### #3 — Secret leak (the 4-transcript purge + rotation incident)
A secret leaks the instant its VALUE reaches stdout/stderr (Bash captures all output into the session `.jsonl`). A real incident leaked LiveKit secret + PlanetScale password + `ENCRYPTION_KEY` + `BETTER_AUTH_SECRET` across four transcripts → required purging every `~/.claude` artifact for those session ids AND rotating the secrets.
**Tripwires:** never run a command whose stdout IS a secret (banned: bare `infisical secrets get KEY --plain`, bare `infisical secrets` table). Feed secrets only via pipe into the consumer, `2>/dev/null` the producer, end with a non-secret confirmation (fingerprint `… | sha256sum | cut -c1-12`, or present/missing). You MAY now WRITE prod/staging secrets (`infisical secrets set/delete`) but reading non-dev VALUES still needs Ray via the `!` prefix. Note `infisical secrets set` echoes the value in its confirm table — for a real secret, feed via `$(...)` / `--silent` / the `!` prefix so it never lands in the transcript.

### #4 — Deleting/overwriting things you didn't create
Before deleting or overwriting, **look at the target** — if what you find contradicts how it was described (or you didn't create it), surface that instead of proceeding. The main checkout is full of Ray's live edits and stray artifact dirs (`logo-concepts/`, `security-audit/`, `widget-concepts/`). The stacked-PR `--delete-branch` auto-close is a version of this.

### #5 — Migrations auto-apply on deploy
A bad migration doesn't just fail your PR — it blocks the **whole prod deploy** (`vercel-build` runs `drizzle-kit migrate` before `next build`). Verify the SQL locally before merging a schema PR.

### Email / credits / money — blast-radius checks
- **Email now works end-to-end** (since 2026-06-27) — a test send can reach a REAL inbox. Use the dedicated test rig (`fantasiesandfailures@gmail.com` ↔ `zz-fixtures-onfl@agentstack.email`), never a real customer address. Before touching email-send code: does it fan out to many recipients? does it loop (Auto-Submitted/Precedence guards)? is there a rate limit and is it the RIGHT direction (the inverted-limiter bug throttled to ~1/hour)?
- **Credits = real money** (1 credit = $0.02; a drop below threshold triggers a real Stripe auto-topup charge). Before any billing change: (a) does every balance mutation also write a `credit_transactions` audit row? (`deductCredits` does NOT auto-write it — it's hand-written in ≥4 call sites; `refundCredits` does); (b) can it deduct twice on retry (Slack task `maxAttempts:3` can multi-charge)? (c) does the failure path refund (chat/email/voice all must; voice pre-auths and must compensate on setup failure with atomic finalization so concurrent end-signals can't double-refund)? (d) is the auto-topup amount a multiple of 1000? test-org's ~10k credits won't accidentally trigger topups, but a real-org test would.

---

## Environment landmines (which are live)

- **Local dev with real env:** `cd nextjs && infisical run --env=dev -- pnpm dev` (injection, never extraction). Port **3000** (Google OAuth redirect hardcoded to `localhost:3000`). `.infisical.json` workspace `fbad2ff5-…`, `defaultEnvironment` empty → always pass `--env`. Needs a one-time interactive `infisical login`. First-boot failures: empty `node_modules` in a fresh worktree; env-validation throw if a required var isn't in Infisical dev.
- **PlanetScale/psql:** `~/.config/agentstack/dbq.sh` exists but needs **psql 17** (`/opt/homebrew/opt/postgresql@17/bin`) — psql 14 can't parse `sslrootcert=system` and fails. **This psql17 gotcha is LIVE.** Safe read path: try the **PlanetScale MCP read tool** first, fall back to `dbq.sh` + psql17. ⚠️ dbq.sh's embedded cred was auth-failing late June — state unconfirmed; the MCP write token was read-only. Treat ALL prod DB writes as danger-zone #1.
- **Cloudflare worker** (`cloudflare/inbox-realtime/`): does NOT auto-sync from Infisical (unlike Vercel/Trigger). Set worker secrets manually by PIPING (`infisical secrets get KEY --env=ENV --plain 2>/dev/null | wrangler secret put NAME --env <production|preview>`, never printing). `wrangler` needs `export CLOUDFLARE_ACCOUNT_ID=f2821033c1667dab67b5f3f891dc6123` or it fails non-interactively (multi-account OAuth). Setting a secret auto-redeploys the worker.
- **Browser-MCP background tab** — LIVE and permanent (Chrome throttles hidden tabs). rAF animations freeze at frame 0; a "blank" screenshot may be a fine page. Always relevant to browser verification.
- **VS Code vs Xcode file-opening** — a one-off macOS default-app fix on Ray's machine, not a repo landmine. Ignore unless he raises it.

---

## Stale-memory catch-list (verified wrong as of 2026-07-05)

The inherited memory files are a mix of durable truth and archaeology. **Trust current `nextjs/src` over any memory/plan.** Confirmed-stale items (fixed here, but expect more):
- `verification/GOAL.md` and `verification/INDEX.md` **no longer exist**; the single `status:` field is gone. Source of truth is `verification/AGENTS.md` + the computed `REGISTRY.md` (two-axis `result:`/`stale:` model). — verified
- Trigger env-sync moved **Vercel → Infisical** (`trigger.config.ts` uses `syncEnvVars` + `InfisicalSDK`, not `syncVercelEnvVars`). — verified
- Inbound-email addresses are now **flat** (`…-nanoid@agentstack.email`), not orgId-subdomain — inbound works. (`lib/api/services/channels.ts:262`) — verified
- The `.githooks/pre-commit` schema guard is **NOT wired** (`core.hooksPath` is default `.git/hooks`). — verified
- `plans/ready/` is now **`plans/active/`**. — verified
- Service files moved to `lib/api/services/*.ts`; `lib/ai-models.ts` → `lib/ai/models.ts` (the March lib-reorg). Grep before trusting any path.

**When you find a memory wrong, UPDATE it** (memory dir: `/Users/ray/.claude/projects/-Users-ray-Desktop-agentstack/memory/`, one fact per file + a line in `MEMORY.md`). That's how the system stays alive. Treat memories as leads for WHY/incident-history, not as facts about current paths/columns/flags.

---

## Could-not-verify / open questions (hand-off)

- **tsc --noEmit current cost** — was 13-min/OOM-at-8GB in April; two PRs attacked the `mcp/tools/sources.ts` hotspot; not re-measured. Prefer `pnpm build`'s typecheck.
- **Greptile-vs-Codex verdict** — Ray commissioned the comparison 2026-06-30 but the conclusion wasn't persisted. Strong lived prior: Codex is highest-signal. Re-run if he asks.
- **`/implement-task`** — referenced in older sessions but NOT in the current skill list; `/implement-feature` is the confirmed L3 loop. Confirm `/implement-task` exists before relying on it.
- **dbq.sh cred auth state + PlanetScale MCP write-token state** — both were failing/read-only late June; unconfirmed now. Assume you cannot write prod DB via automation without checking.
- **Voice model ids / LiveKit SDK versions** — drift fast; re-check real provider ids against `agent/src/providers.ts` before trusting the list in `playbooks.md`.
