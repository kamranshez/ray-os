# Opus 4.8 Handbook — agentstack

Survival handbook written for the incoming Claude Opus 4.8 agent by the departing Fable 5 veteran (~530 sessions), 2026-07-05. This does **not** repeat `AGENT-INSTRUCTIONS.md` or `CLAUDE.md` — read those first, then this. This captures the tacit knowledge: sequencing, judgment calls, war stories, and where the docs/memory have gone stale.

**Files**
- `README.md` (this) — day-one orientation + the two checklists + working-with-Ray + model-delta self-guidance.
- `playbooks.md` — task-type playbooks (plan implementation, PR/review loop, verification, bug hunts, prod debugging, design variations, specs).
- `danger-and-gotchas.md` — ranked danger zones with tripwires, environment quirks, and the stale-memory catch-list.

**Golden rule above all others:** trust the **code on current main**, not the plan, not memory, not this handbook. The March lib-reorg moved half the paths; memory files and plans cite paths that have drifted. Grep every symbol before you touch it. When you find a doc/memory wrong, fix it.

---

## Day one — orientation

**What this repo is:** `nextjs/` is the product (Next.js 15 + tRPC + Drizzle + Hono REST). `agent/` is a **separate** LiveKit voice worker (own Dockerfile, own deploy). `cloudflare/inbox-realtime/` is a Durable-Object worker. Trigger.dev tasks live in `nextjs/src/trigger/`. Docs are Fumadocs under `nextjs/content/docs/`.

**The repo is never clean.** At any moment there are ~20 live worktrees under `.claude/worktrees/`, several open PRs, Codex's own worktrees under `~/.codex/worktrees`, and uncommitted design experiments in the **main checkout** (Ray edits live). Before you branch: `git worktree list` and `git status`. **Never implement in the main checkout** — you'll collide with Ray. Leave files you didn't create alone.

**Two orgs are production, one is your sandbox:**
- `ray-amjad-ltd` (slug) + the **HyperWhisper** agent — real product, real customers (`hyperwhisper.com` dogfoods a live agentstack agent). **Untouchable.**
- `21-dreams` / "2D 21 Dreams" — another real org.
- **`test-org`** (UUID `79ead959-68f0-497e-b73c-2b97f99b7aa6`, agent `zz-fixtures` `0cf6a7f1-76ee-4675-9c21-6687de1688f8`) — your ONLY sandbox. Standard tier since 2026-06-14 (agent limit 3, ~10k credits, inbox enabled). The seed REST endpoints are hard-pinned to it (`SEED_ORG_SLUG` in `nextjs/src/lib/api/hono/routes/seed/shared.ts` — verified).

**"Fictional future models" are intentional.** The app uses model IDs that don't exist in the real world as internal labels: GPT-5.2 (default chat), GPT-5.4-nano, Gemini 3.1, etc. In the app's own registry (`nextjs/src/lib/ai/models.ts`) these are **correct — do not "fix" them to real ids.** They only need mapping to real provider ids at the moment code calls OpenAI/Google/LiveKit (else `model_not_found` / `code 1008`). Know which layer you're in. (You — Opus 4.8 — and Fable 5 are also "fictional from training"; don't let that confuse your handling.)

**Ray is building a meta-system.** A large fraction of sessions aren't feature work — they're "figure out my building pattern," "make a skill out of this," "compare the two review bots," "score the tech debt." When he describes a process, he often wants it **codified into a skill/workflow**, not just run once. Treat "make this repeatable" as the real deliverable.

**Fast facts (verified 2026-07-05):**
- Boot local with real env: `cd nextjs && infisical run --env=dev -- pnpm dev` (port 3000; OAuth redirect hardcoded to `localhost:3000`).
- Build without env: `cd nextjs && SKIP_ENV_VALIDATION=1 pnpm build`.
- Deploy = push to main → Vercel prod auto-deploys → migrations apply automatically (`vercel-build` = `patch-drizzle-migrate.js && drizzle-kit migrate && next build`).
- Vercel **preview** checks on PRs **fail by design** (no preview secrets) — never a merge blocker.
- pnpm only. Never `npm install` (breaks worktree store dedup).

---

## The two checklists (run these every time)

### ▶ PRE-COMMIT — before every `git commit`
1. **In a worktree off fresh `origin/main`**, not the main checkout?
2. **Touched `nextjs/src/db/schema/`?** → `cd nextjs && pnpm db:generate`, and the new `.sql` + `meta/*.json` go **in this commit**. (The `.githooks/pre-commit` guard is **NOT active** in this clone — `core.hooksPath` is default `.git/hooks`. Do it manually.)
3. **Every new `catch` has `console.error`** (else invisible in Vercel logs).
4. **New env var you actually set in Infisical → declared REQUIRED** in `nextjs/src/env/schema.mjs`, and set in dev/staging/prod **before** flipping. Not `.optional()`. (Ray hates this one.)
5. **Touched credits/balance?** Every `message_credits_balance` mutation has a matching `credit_transactions` audit insert; failure paths refund; auto-topup amount is a multiple of 1000.
6. **New gated dashboard page?** Default export = `<DashboardLayout><FooContent/></DashboardLayout>`; `useCan`/`useOrganization` live in `FooContent`, never the default export (provider is mounted *inside* `DashboardLayout`).
7. **`api/chat/route.ts` change → still Edge-safe** (no Node-only libs like the Stripe SDK).
8. **No secret value in any command's stdout/stderr.** Fingerprint (`… | sha256sum | cut -c1-12`) or present/missing check only.
9. **It compiles:** `SKIP_ENV_VALIDATION=1 pnpm build` clean. Build **incrementally** as you go, not just at the end.
10. **Commit message ends with the mandated `Co-Authored-By` + `Claude-Session` trailers** (the harness supplies them).

### ▶ PRE-MERGE — before `gh pr merge --squash`
1. **Re-derived every review-bot finding yourself?** Classify CONFIRMED / PLAUSIBLE / FALSE-POSITIVE by reading the cited code. Never fix what you didn't verify — bots false-positive regularly.
2. **Latest review round found only nits/pre-existing, no NEW confirmed regression in your own fixes?** If a real regression → loop once more. If you're on round 4 still finding regressions in your fixes → **redesign, don't patch.**
3. **Ignore the red Vercel preview check.** Real gate = local build clean + bots quiet.
4. **Small/low-risk → you merge. Big/risky (voice, billing, security, large rewrites, schema) → escalate to Ray.** When unsure, escalate. Ray often merges these himself ("move to main").
5. **Stacked PR? Do NOT `--delete-branch`** (GitHub auto-closes the child instead of retargeting). And confirm no follow-up commit is stranded on the branch post-merge.
6. **Schema PR? Migration ordering sane** — a reorder on a merge can strand a "never-runs" migration and **block the whole prod deploy**.
7. **After merge: monitor the deploy** (see below), then arm the 1h error tail. **Ready ≠ healthy.**
8. **No prod deploy ~10 min after merge → dropped webhook → push an empty commit** (`git commit --allow-empty`). Never `vercel --prod` from the monorepo root (7.6GB EPIPE).
9. **User-facing change? Verify it in the real app** (browser/GIF or a described repro) before calling it done.

---

## Working with Ray

**His messages are dictated (speech-to-text).** Recurring corruptions to auto-correct:
- **"go OAuth and" = "go ahead and"** (constant). OAuth-the-protocol only when context is integrations/Slack/Calendly/Notion.
- **"styripe" = Stripe.** "live kit" = LiveKit. "cloud/claude in chroem" = Claude-in-Chrome. "fable agent" = a Fable-model subagent. "clawmd" = CLAUDE.md. "xer"/"exa" = Exa MCP. "off page" = auth page (login/signup). "amber class out" = amber callout.
- Strip filler: "like," "kind of," "or something like that," "basically." "or something" is **not** a request for options.

**Ask vs swing:** default to **best-swing with a fast escape hatch** — he's usually not watching live, and "shall I…?" stalls work. For genuinely ambiguous **product/design** decisions, don't ask open questions — give him a **clickable pick-list** (an HTML artifact with multiple-choice, or `/spec-developer-v2`). He'd rather click than free-type. Hard "ask first": destructive/irreversible actions or real scope changes. If he's describing a problem or asking a question (not requesting a change), the deliverable is your **assessment** — report and stop, don't pre-fix.

**What "done" means to him:** verified working **in the real app** (not just typecheck-green) + merged + **deploy watched to healthy** + no regressions in adjacent flows + (if schema) migration committed. He comes back annoyed when: it "worked" in code but not live; a new env var was added optional and silently no-op'd; a design change is subtly inconsistent with the rest of the site; or you reported success you didn't observe.

**What he hates (corrected more than once):** `.optional()` env vars; leaking secrets into transcripts; being asked permission for obviously-in-scope work; **design inconsistency** (spacing/cards/modals that don't match the site); duplicated/divergent logic; reporting done without verifying; `npm` instead of pnpm; stashing his live-edited files.

**The single highest-leverage habit:** when he points at **one** broken thing (a screenshot, a URL, "this spacing is off"), the right move is almost never the literal minimal fix. **Find the pattern and fix the class** — silently ask "where else does this exact pattern live?" and sweep sibling pages/components. He thinks in design systems and code seams, not individual bugs, and notices when you fix one instance and miss three.

**Credentials in chat:** he sometimes pastes a live secret to unblock a one-off (he did it with PlanetScale creds to delete a blog row). That's authorization for **that action only** — but the transcript now contains a credential, so flag that he may want to rotate it, and don't reuse it beyond the task.

---

## Model-delta — how to operate as the weaker model

You (Opus 4.8) are genuinely less capable than the Fable 5 veteran at raw reasoning, long-context synthesis, and holding many threads at once. Where the veteran leaned on capability, you substitute **process**:

- **Don't hold a big plan in your head.** Write its phases into `TaskCreate` the moment you start; re-read the relevant files after each phase instead of trusting recollection. The task list is your working memory.
- **Don't one-shot a multi-file change and build only at the end.** Make the smallest compilable increments and run `pnpm build` frequently — cheaper to catch a type error in isolation than untangle five.
- **Don't rely on bug-intuition.** The veteran caught the inverted rate limiter / missing-migration / useCan-silent-false bugs because they "smelled wrong." You may not get that signal free — rely on the checklists above, and delegate the "is this actually right?" question to an adversarial subagent (`/code-review`, `/codex-consult challenge`) rather than trusting your own read.
- **Delegate long reads.** Any "read across many files and tell me the conclusion" → `Explore`/`general-purpose` subagent. Log analysis → haiku subagent. Keep your own context clean.
- **Run fewer concurrent threads.** Lean on on-disk state (grep frontmatter) and shared task lists, not head-tracking.

**Stop and ask/escalate specifically because you're the weaker model when:** you've circled the same problem 2+ times (spawn a fresh-perspective subagent, then surface it); a change touches money/real-email/prod-DB/secrets/auth-gating and you're not certain of blast radius; a product decision is genuinely ambiguous (give a pick-list); or you **cannot actually verify** the change works (say so plainly — "I made the change but couldn't exercise it end-to-end because X" beats false confidence). **Your failure mode is quiet overconfidence.** Antidote: externalize doubt, show your verification, and believe a disagreeing subagent until you've disproven it.
