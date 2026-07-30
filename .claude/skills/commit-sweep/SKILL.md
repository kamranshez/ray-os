---
name: commit-sweep
description: Turn an accumulated, messy ray-os working tree into a set of clean separately-revertable commits and push them — additions, renames and removals alike — while holding back the files a human should decide on. Use this whenever the user wants to commit or push work that has piled up — "commit all this", "push everything that's waiting", "split up the commits", "clean up my git status", "let's get this committed", "sync the vault" — and any time you finish a chunk of work in ray-os and the user asks you to save or ship it. Also use it when git status has grown long and mixed and you need to figure out what is safe to commit. Prefer this over a bare `git add -A && git commit` in this repo, because ray-os has LFS media, vault-convention checks, and usually a mix of your work and Ray's sitting side by side.
---

## Why this exists

A ray-os working tree is rarely one clean change. It accumulates: images the last skill generated, notes Ray wrote days ago, a skill you edited an hour ago, Obsidian UI churn, and a couple of files nobody meant to leave lying around. A blanket `git add -A` bundles all of that into one commit that can never be partially undone, and quietly ships an 80 MB LFS payload and a stray `__pycache__` along with it.

The job is to sort that pile into commits that each mean one thing, and to notice the handful of files that need Ray's judgment rather than yours.

## The workflow

### 1. Triage

Run the bundled script from the repo root. It classifies everything in the working tree and does the repo-specific checks that are easy to forget:

```bash
.claude/skills/commit-sweep/scripts/triage.py
```

It reports **junk** (never commit), **renames** (moves it paired up by content), **hold** (needs a human decision), **ready** (grouped by area), a **deletions** count, and the **LFS payload** you would be pushing. Read its output before deciding anything — it exists so you don't re-derive the same checks by hand every time.

Trust its rename pairing over your own reading of `git status`. It hashes every deleted path from the index and every untracked file from disk, so it catches a file that moved *and* was renamed, which eyeballing basenames does not.

### 2. Separate your work from what was already there

Claude Code puts a git status snapshot in your context at session start. Anything dirty in that snapshot predates you: it is Ray's work, not yours.

This matters for the commit messages. For your own work you know the intent and should say it. For his, describe **what changed** factually and skip the narrative — inventing a rationale for someone else's half-finished work puts words in their mouth, and a wrong "why" in a commit message is worse than no "why" at all.

If the snapshot isn't available (compacted away, resumed session), `git log -1 --format=%cd` against a path and the file mtimes will usually tell you.

### 3. Investigate anything you didn't create

Before committing a change you didn't make, spend the ten seconds to understand it. Deletions especially:

```bash
git ls-files <path>              # what was actually tracked
git log --oneline -2 -- <path>   # when it landed, and why
ls -d <path>                     # does it still exist on disk?
```

A skill directory that's gone from disk with three tracked files showing as deleted is an intentional removal, and step 5 says to commit it. The reason to look anyway is that the same status output covers a very different case: a file that moved. `ls -d` on the old path plus a search for the basename elsewhere tells you which one you have in about ten seconds, and that distinction changes what you stage.

### 4. Group into commits

The seam that matters most in this repo is **reusable tooling vs the content it produced**. A skill and the images it generated are two different things with two different lifetimes: bundle them and Ray can't throw away a batch of images without also losing the skill that makes more. Split them, always.

Beyond that, group so each commit is independently revertable and independently describable. Useful seams:

- one skill's changes = one commit (skills are self-contained units)
- one video's or note's content = one commit
- generated media + the note that embeds them = one commit (they're meaningless apart)
- `.obsidian/workspace.json` = its own `chore(obsidian): sync vault UI state`

Don't over-split. Three files that only make sense together are one commit, not three.

Message style follows the existing log — `area: what changed`, or `area(scope): what changed`. Run `git log --oneline -15` to match the prevailing shape. Append the trailers the Bash tool documents (`Co-Authored-By`, `Claude-Session`). Ray does not use em or en dashes in his writing; commit messages are his repo, so avoid them there too.

### 5. Sweep all three kinds of change

A working tree holds additions, renames and removals, and the sweep commits all three. None of them is an exception.

**Additions and modifications** are the easy case: group them by area per step 4 and commit.

**Renames** must be staged as renames. Take the pairs from the triage RENAMES section and stage the old and the new path *in the same commit* — `git add -- <old> <new>` — then confirm with `git diff --cached --find-renames --stat`, which should show `{old => new}` and zero content change. Staged apart, git records a delete plus an unrelated add, and the file's history stops at the old path. A pair flagged `content CHANGED` needs your eyes: same basename is suggestive, not proof, so compare them before deciding it is one file rather than two.

**Removals** get committed too. If a tracked file is gone from disk, Ray removed it, and leaving the removal uncommitted parks it in limbo: absent from the vault, still recorded in HEAD, and guaranteed to resurface in the next sweep. Group them by area, own commits, so one area can be reverted without the others.

That does not conflict with CLAUDE.md's "never delete files without explicit user permission." That rule governs *you* deleting things. Recording a removal Ray already made is the opposite: it happened before you arrived, and committing it is bookkeeping. The content also stays in history — `git show <sha>:<path>` recovers any of it — so this is reversible in a way an actual deletion is not.

Then say plainly in the report what was removed. A large batch deserves a sentence naming the directories that vanished, so Ray can spot a script that overreached.

**Calibrate the alarm.** Ray prunes this vault in bulk, routinely. Two hundred deletions in one sweep is a Tuesday, not an incident. Name the directories in a sentence and move on. Do not build a case around it: no byte-counts "at risk", no forensic hunt through `~/.Trash` and the wider filesystem, no treating a terse or auto-generated commit message on an earlier deletion as evidence of a runaway process. Content in HEAD is not "at risk" — it is in git. Escalate only if a deletion contradicts something Ray said in *this* conversation, and even then commit the rest first.

Still hold these:

- **Files that violate a vault convention** — an image outside `images/`, a generic name like `sheet1.png`, an image no note references. These are usually accidents, and committing an accident makes it permanent.
- **Anything you genuinely can't classify.**

The important part: hold them *without* blocking the rest. Commit everything else in full, then report each held item in a line or two — what it is, why you held it, and what the options are. Stopping the whole sweep over one ambiguous file wastes the run; silently committing it is worse.

### 6. Report the LFS payload before pushing

Every image type in this repo is LFS-tracked (see `.gitattributes`). LFS bandwidth is spent on every future clone, not just this push, so an 80 MB batch of candidate images is a permanent cost for something Ray may only keep a fraction of.

Tell him the payload size *before* pushing and offer to trim, because trimming is cheap now and effectively impossible once the objects are on the remote. Then let him decide — he often does want all the candidates.

### 7. Push only as far as you were authorised

Committing and pushing are two different permissions, and the gap between them is where this task goes wrong. A local commit is yours to undo; a push is outward-facing and effectively isn't. So read what the request actually licensed:

- *"commit everything and push it"* — push.
- *"get this committed"*, *"don't push yet"* — commit, stop, and say the push is ready when they are.
- *"recommend how you'd push it"*, *"what would you push?"* — that asks for a recommendation, not a push. Make the commits, describe the push you would run and why, and offer to run it.

That last one is easy to misread, because you've just done the work and pushing feels like finishing it. It isn't. Answering a question with an irreversible action is the failure mode. When the wording is ambiguous, commit and offer — the commits are the valuable, reversible part, and the push can happen one message later at no cost.

When you are pushing, push to `main` directly. Every commit in this repo's history is on `main`, it's a single-user vault, and there is no reviewer, so a branch and PR would be ceremony with no one on the other end. This is the one place to override the general "branch before committing on the default branch" habit.

```bash
git push origin main
```

Then verify it actually landed, since an LFS push can partially fail in ways that look fine:

```bash
git fetch -q origin && git rev-list --left-right --count 'origin/main...HEAD'   # want 0  0
git lfs fsck                                                                     # want "Git LFS fsck OK"
```

Not a Vercel project, so there's no deploy to watch afterwards.

## Repo-specific checks worth knowing

These are the ones that have actually caught something:

- **`__pycache__` is not in `.gitignore`.** It shows up as untracked under `artefacts/*/scripts/` and will get swept in by `git add -A` on a directory. Exclude it, or offer to add the ignore rule.
- **Images live flat in vault-root `images/`**, kebab-case and globally unique, and every one should be referenced by some note. An unreferenced image is an orphan and the convention says it shouldn't be kept.
- **Root-level files** are nearly always strays. Real content lives under `artefacts/`, `socials/`, `slides/`, `projects/`, `images/`.
- **`scratchpad/` is gitignored** — driver scripts and working files there are meant to stay out, so don't try to rescue them into a commit.
- **Other Claude sessions are often live in this same working tree.** Ray runs several at once. Expect the tree to move under you mid-sweep: the deletion count climbing, a file you just held deleting itself, a directory you committed ten minutes ago getting renamed by someone else. Check with `lsof -a -p <pid> -d cwd -Fn` over the pids from `ps -Ao pid,lstart,command | grep 'bin/claude'` if you want to confirm.

  This is a fact to work around, not a reason to stop. Re-snapshot `git status --porcelain` immediately before you stage each group rather than trusting the triage output from five minutes ago, stage explicit paths instead of `git add -A`, and finish the sweep. Another session pushing while you work is also normal — re-check `origin/main` before reporting what is unpushed, because some of your commits may already be on the remote. Never `git reset` or rewrite history to tidy up after a concurrent session; you would be pulling the rug out from under a running agent.

## Reporting back

Close with a table of the commits you made (one row each: message and what's in it), then the held items, then the push verification. Lead with the seam you chose and why if it wasn't obvious — the grouping is the actual judgment in this task, and it's the part worth a sentence of explanation.

Say how many additions, renames and removals went in. Renames especially: "4 of those 220 deletions were a move" is the kind of thing Ray wants to know, because it means the count he saw in `git status` was overstating what actually went away.

If you told Ray something earlier in the session that the triage proved wrong (a file you thought was modified and wasn't), correct it in one line. Don't dwell on it.
