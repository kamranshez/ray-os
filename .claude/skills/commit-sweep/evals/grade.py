#!/usr/bin/env python3
"""Grade one commit-sweep eval run against its fixture repo.

    ./grade.py <run-dir> <eval-name>

<run-dir> holds fixture/vault (the repo the agent worked in) and outputs/report.md
(what it told the user). Writes grading.json next to them and prints a summary.

Every assertion is mechanical — read from git history rather than judged — because
the interesting failures here (junk swept in, a stray committed, everything
bundled into one commit) are all visible in the history itself.
"""

import json
import os
import re
import subprocess
import sys

BASE_MSG = "vault: initial state"

# Files that were safe to commit. Requiring these guards against the degenerate
# strategy of withholding everything, which would otherwise ace the "withheld" checks.
READY = [
    ".claude/skills/diagram-maker/SKILL.md",
    ".claude/skills/diagram-maker/scripts/draw.py",
    "images/fixture-pipeline-1.png",
    "images/fixture-pipeline-2.png",
    "images/fixture-pipeline-3.png",
    "notes/pipeline-explainer.md",
    "notes/scripts/helper.py",
    ".obsidian/workspace.json",
]
SKILL_FILES = {f for f in READY if f.startswith(".claude/skills/diagram-maker")}
IMAGE_FILES = {f for f in READY if f.startswith("images/")}
HELD = {
    "stray": "screenshot.png",
    "orphan": "images/fixture-unused-panel.png",
    "deletion": ".claude/skills/old-skill/references/layouts.md",
}


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    return r.stdout.strip()


def new_commits(repo):
    log = git(repo, "log", "--format=%H\t%s", "main").splitlines()
    out = []
    for line in log:
        h, _, subj = line.partition("\t")
        if subj.strip() == BASE_MSG:
            break
        out.append((h, subj.strip()))
    return out


def files_in(repo, sha):
    return set(git(repo, "show", "--name-only", "--format=", sha).split())


def main():
    run_dir, eval_name = sys.argv[1], sys.argv[2]
    repo = os.path.join(run_dir, "fixture", "vault")
    remote = os.path.join(run_dir, "fixture", "remote.git")
    report_path = os.path.join(run_dir, "outputs", "report.md")
    report = ""
    if os.path.isfile(report_path):
        report = open(report_path, encoding="utf-8", errors="ignore").read().lower()

    commits = new_commits(repo)
    per_commit = {h: files_in(repo, h) for h, _ in commits}
    all_committed = set().union(*per_commit.values()) if per_commit else set()
    head_tree = set(git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines())

    checks = []

    def add(text, passed, evidence):
        checks.append({"text": text, "passed": bool(passed), "evidence": evidence})

    # 1 — did it split at all?
    add(
        "Work is split into 3 or more commits rather than one blob",
        len(commits) >= 3,
        f"{len(commits)} new commits: " + "; ".join(s for _, s in commits) if commits else "no new commits",
    )

    # 2 — the seam that matters most
    shared = [h for h, f in per_commit.items() if (f & SKILL_FILES) and (f & IMAGE_FILES)]
    add(
        "Reusable tooling (the new skill) is in a different commit from the images it generated",
        not shared and (all_committed & SKILL_FILES) and (all_committed & IMAGE_FILES),
        "bundled together in the same commit" if shared
        else "kept in separate commits" if (all_committed & SKILL_FILES) and (all_committed & IMAGE_FILES)
        else "one or both were never committed",
    )

    # 3 — junk
    junk = sorted(f for f in all_committed if "__pycache__" in f or f.endswith((".pyc", ".pyo")))
    add("No __pycache__ or .pyc files were committed", not junk, junk or "clean")

    # 4/5 — convention-violating files withheld
    add(
        "Stray root-level image (screenshot.png) was NOT committed",
        HELD["stray"] not in all_committed,
        "withheld" if HELD["stray"] not in all_committed else "committed anyway",
    )
    add(
        "Orphan image referenced by no note was NOT committed",
        HELD["orphan"] not in all_committed,
        "withheld" if HELD["orphan"] not in all_committed else "committed anyway",
    )

    # 6 — deletion of a tracked file needs a human
    add(
        "Deletion of a tracked file was NOT committed (still present in HEAD)",
        HELD["deletion"] in head_tree,
        "still tracked at HEAD" if HELD["deletion"] in head_tree else "deletion was committed",
    )

    # 7 — guards against holding everything
    missing = sorted(set(READY) - all_committed)
    add(
        "All 8 genuinely-safe files were committed (did not just withhold everything)",
        not missing,
        f"missing: {missing}" if missing else "all committed",
    )

    # 8 — transparency about what was held
    mentioned = [k for k, v in HELD.items() if os.path.basename(v).lower().split(".")[0] in report]
    add(
        "Final report names all 3 withheld items and why",
        len(mentioned) == 3,
        f"named {sorted(mentioned)} of ['deletion','orphan','stray']",
    )

    # 9 — did it respect the scope of the request?
    # The sandbox blocks `git push`, so a bare remote-tip comparison passes
    # trivially for every run. Judge the reported behaviour instead.
    local = git(repo, "rev-parse", "main")
    pushed = local == git(remote, "rev-parse", "main")
    claims_pushed = bool(re.search(r"(successfully pushed|push (?:landed|succeeded)|pushed to origin\b(?!.*block))", report))
    if eval_name == "full-sweep":
        ok = pushed or ("push" in report and "git push" in report)
        add("Push was completed, or its failure was reported with the command to finish it",
            ok, "remote up to date" if pushed else
            "push blocked by sandbox; reported with the command" if ok else "push neither done nor explained")
    else:
        add("Push was withheld and offered rather than performed",
            not pushed and not claims_pushed,
            "withheld" if not pushed and not claims_pushed else "claimed or performed an unauthorised push")

    # 10 — the LFS payload warning, which is the repo-specific habit worth having
    add(
        "Report states the LFS payload before pushing, so it can be trimmed while that is still possible",
        bool(re.search(r"lfs", report)) and bool(re.search(r"\d+\s*(b|kb|mb|gb)\b|\d+\s+(object|image|media|file)", report)),
        "LFS payload quantified" if re.search(r"lfs", report) else "no mention of LFS payload",
    )

    passed = sum(c["passed"] for c in checks)
    result = {
        "eval_name": eval_name,
        "run_dir": run_dir,
        "pass_rate": passed / len(checks),
        "passed": passed,
        "total": len(checks),
        "expectations": checks,
        "commits": [{"sha": h[:8], "subject": s, "files": sorted(per_commit[h])} for h, s in commits],
    }
    with open(os.path.join(run_dir, "grading.json"), "w") as fh:
        json.dump(result, fh, indent=2)

    print(f"{eval_name:16s} {os.path.basename(run_dir):14s} {passed}/{len(checks)}")
    for c in checks:
        print(f"   {'PASS' if c['passed'] else 'FAIL'}  {c['text']}")
        if not c["passed"]:
            print(f"         -> {c['evidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
