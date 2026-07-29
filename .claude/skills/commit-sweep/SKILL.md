---
name: commit-sweep
description: Turn an accumulated, messy ray-os working tree into a set of clean separately-revertable commits and push them, while holding back the files a human should decide on. Use this whenever the user wants to commit or push work that has piled up — "commit all this", "push everything that's waiting", "split up the commits", "clean up my git status", "let's get this committed", "sync the vault" — and any time you finish a chunk of work in ray-os and the user asks you to save or ship it. Also use it when git status has grown long and mixed and you need to figure out what is safe to commit. Prefer this over a bare `git add -A && git commit` in this repo, because ray-os has LFS media, vault-convention checks, and usually a mix of your work and Ray's sitting side by side.
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

It reports four groups: **junk** (never commit), **hold** (needs a human decision), **ready** (grouped by area), and the **LFS payload** you would be pushing. Read its output before deciding anything — it exists so you don't re-derive the same checks by hand every time.

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

A skill directory that's gone from disk with three tracked files showing as deleted is probably an intentional removal — but "probably" is the reason to ask rather than assume.

### 4. Group into commits

The seam that matters most in this repo is **reusable tooling vs the content it produced**. A skill and the images it generated are two different things with two different lifetimes: bundle them and Ray can't throw away a batch of images without also losing the skill that makes more. Split them, always.

Beyond that, group so each commit is independently revertable and independently describable. Useful seams:

- one skill's changes = one commit (skills are self-contained units)
- one video's or note's content = one commit
- generated media + the note that embeds them = one commit (they're meaningless apart)
- `.obsidian/workspace.json` = its own `chore(obsidian): sync vault UI state`

Don't over-split. Three files that only make sense together are one commit, not three.

Message style follows the existing log — `area: what changed`, or `area(scope): what changed`. Run `git log --oneline -15` to match the prevailing shape. Append the trailers the Bash tool documents (`Co-Authored-By`, `Claude-Session`). Ray does not use em or en dashes in his writing; commit messages are his repo, so avoid them there too.

### 5. Hold back the judgment calls

Some things should not be committed on your own initiative:

- **Deletions of tracked files.** Committing a deletion propagates it. That's a decision, and CLAUDE.md is explicit that files don't get deleted without Ray saying so.
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

## Reporting back

Close with a table of the commits you made (one row each: message and what's in it), then the held items, then the push verification. Lead with the seam you chose and why if it wasn't obvious — the grouping is the actual judgment in this task, and it's the part worth a sentence of explanation.

If you told Ray something earlier in the session that the triage proved wrong (a file you thought was modified and wasn't), correct it in one line. Don't dwell on it.
