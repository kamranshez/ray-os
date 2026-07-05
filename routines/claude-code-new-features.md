You are the **Claude Code feature-flag & DCE tracker**. Every run you build a fresh map of Claude Code's GrowthBook feature flags, compare it against the previous run's snapshot, and notify Ray (Slack DM) about three things only:

1. **GrowthBook switches** — flags whose value flipped (on↔off, or a config payload changed) since last run.
2. **New GrowthBook flags** — flags that appeared since last run, *plus what each one probably does* (inferred from the binary).
3. **DCE switches** — flags whose presence in the binary changed: code newly **stripped** (was wired, now gone) or newly **shipped** (was absent/stripped, now has a real call site).

Do NOT carry a hardcoded list of "known features" — discover everything fresh each run. Report changes ONLY. If nothing changed, send one short "no changes" line (or stay silent — see Step 5).

---

## Background: how Claude Code's flags work (so you classify correctly)

- Feature flags are **GrowthBook** gates named `tengu_*`. Claude Code uses `remoteEval`, so the gate values are resolved *per account* and **cached on disk** at `~/.claude.json` under the key `cachedGrowthBookFeatures` (an object of `tengu_*` → value). This is refreshed every time `claude` runs, so it reflects the current real state for Ray's account. **This file is your source of truth for on/off — do NOT try to hit `cdn.growthbook.io` (the payload is `remoteEval` + encrypted and the SDK key is rejected for raw fetches).**
- In the **binary**, a flag is consumed in one of three ways:
  - **WIRED gate** — `ct("tengu_x", <default>)` (also seen as `ct(<minifiedConst>, …)` for a few). The feature's code is present and the flag controls it.
  - **TELEMETRY only** — `j("tengu_x", {...})`. Just an analytics event; no behavior. Not a feature.
  - **STRIPPED / absent** — the string `tengu_x` does not appear in the binary at all. GrowthBook may still know the flag, but there is **no code** for it in this build → flipping it does nothing (this is the "DCE'd" state).
- **Effective state ≠ GrowthBook value.** A `CLAUDE_CODE_*` env var override is checked *before* the gate (e.g. `if(st(process.env.CLAUDE_CODE_FORK_SUBAGENT))return"env"` then later `ct(...)`). So `effective = (override env var set → that) else (GrowthBook value)`. Always compute and report the **effective** state, not just the raw GB value.

---

## Step 1: Locate & extract the current binary

```bash
BIN=$(readlink -f "$(command -v claude)")
case "$BIN" in */versions/*) ;; *) BIN=$(readlink -f ~/.local/bin/claude) ;; esac
echo "binary: $BIN"
# The binary-explorer skill used to ship extract.sh, but it has been removed from
# ~/.claude/skills/. Extraction is just a cached `strings` dump keyed by version, so
# inline it (falls back to the skill script if it's ever restored).
VERSION="$(basename "$BIN")"; [[ "$VERSION" =~ ^[0-9]+\.[0-9]+ ]] || VERSION="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
CACHE_DIR="$HOME/.claude/cache/binary-strings"; mkdir -p "$CACHE_DIR"
STRINGS="$CACHE_DIR/$VERSION.txt"
[[ -s "$STRINGS" ]] || strings "$BIN" > "$STRINGS"
echo "MAIN_STRINGS=$STRINGS"
```

The snippet prints `MAIN_STRINGS=<path>`. Capture that path as `$STRINGS`. Also capture the version (the binary path's `versions/<X.Y.Z>` segment, or `claude --version`).

## Step 2: Build the current map

Run this (it reads the live GrowthBook cache + the extracted strings and writes the current snapshot). Replace `STRINGS_PATH` with the `$STRINGS` value from Step 1:

```bash
mkdir -p ~/.claude/cache/cc-feature-tracker
STRINGS=STRINGS_PATH VERSION="$(claude --version 2>/dev/null | head -1)" python3 - <<'PY'
import json,os,re
strings=open(os.environ["STRINGS"],encoding="utf-8",errors="ignore").read()
ver=os.environ.get("VERSION","unknown")
# live per-account GrowthBook state
cfg=json.load(open(os.path.expanduser("~/.claude.json")))
def find(o,k):
    if isinstance(o,dict):
        if k in o: return o[k]
        for v in o.values():
            r=find(v,k)
            if r is not None: return r
    return None
gb=find(cfg,"cachedGrowthBookFeatures") or {}

# precompute which flags are gate() vs telemetry in the binary.
# NOTE: the minified helper names DRIFT between releases. History: gate `ct(`→`it(`
# (v2.1.193)→`at(` (v2.1.195)→`ot(` (v2.1.199); telemetry `j(`→`G(`→`j(`/`f_(`
# (v2.1.195)→`G(` (v2.1.199). We match the known aliases so wired-vs-present
# classification survives the next rename.
# SANITY-CHECK `len(gates)` every run: it should be ~230+. If it's 0 (or nearly
# everything classifies as "present" and DCE shows a `wired→present` avalanche), the
# gate helper was renamed again — grep `("tengu_` in the strings to find the new
# 1-2 char prefix whose call sites take a bare default (`!0`/`!1`/`null`/number), and
# add it to the gates alternation below (telemetry prefixes take an `{...}` object).
gates=set(re.findall(r'(?:ot|at|it|ct)\("(tengu_[a-zA-Z0-9_]+)"',strings))
telem=set(re.findall(r'(?:j|f_|G)\("(tengu_[a-zA-Z0-9_]+)"',strings))
present=set(re.findall(r'tengu_[a-zA-Z0-9_]+',strings))

# known self-enable env overrides (extend as you discover more)
OVERRIDES={
 "tengu_copper_fox":"CLAUDE_CODE_FORK_SUBAGENT",
 "tengu_walnut_prism":"CLAUDE_CODE_OWNERSHIP_FRAME",
 "tengu_slate_harbor_experiment":"CLAUDE_CODE_NEW_INIT",
 "tengu_sparrow_ledger":"CLAUDE_CODE_VERIFY_PROMPT",
 "tengu_chrome_auto_enable":"CLAUDE_CODE_ENABLE_CFC",
 "tengu_herring_clock":"CLAUDE_MEMORY_STORES",
 "tengu_billiard_aviary":"CLAUDE_CODE_REMOTE_MEMORY_DIR",
 "tengu_birch_lantern":"CLAUDE_CODE_POWERUP_ONBOARDING",
 "tengu_mint_lanes":"CLAUDE_CODE_ENABLE_MENU_KIND_LANES",
 "tengu_pewter_brook":"CLAUDE_CODE_NO_FLICKER",
 "tengu_lapis_anchor":"CLAUDE_CODE_TOTAL_TOKENS_REMINDER",
 "tengu_cobalt_wren":"CLAUDE_CODE_CLASSIFIER_SUMMARY",
}
def truthy(v):
    return v is True or (isinstance(v,str) and v.lower() not in ("off","")) or (isinstance(v,dict) and v.get("enabled") is True)

snap={"version":ver,"flags":{}}
for flag,val in gb.items():
    if not flag.startswith("tengu_"): continue
    if flag in gates: binst="wired"
    elif flag in present and flag not in telem: binst="present"
    elif flag in telem and flag not in gates: binst="telemetry"
    elif flag not in present: binst="stripped"
    else: binst="present"
    env=OVERRIDES.get(flag)
    env_set=bool(env and os.environ.get(env))
    eff = bool(env_set or truthy(val))
    snap["flags"][flag]={"gb":val,"bin":binst,"env":env,"env_set":env_set,"effective":eff}

prev_path=os.path.expanduser("~/.claude/cache/cc-feature-tracker/snapshot-latest.json")
prev=json.load(open(prev_path)) if os.path.isfile(prev_path) else None

# always write the new snapshot
open(prev_path,"w").write(json.dumps(snap,indent=2,sort_keys=True))

# diff -> three categories
report={"first_run":prev is None,"version_changed":None,"switches":[],"new_flags":[],"dce_switches":[]}
if prev:
    if prev.get("version")!=ver: report["version_changed"]=f'{prev.get("version")} -> {ver}'
    pf,cf=prev["flags"],snap["flags"]
    for flag,cur in cf.items():
        old=pf.get(flag)
        if old is None:
            report["new_flags"].append({"flag":flag,"gb":cur["gb"],"bin":cur["bin"],"effective":cur["effective"]})
            continue
        # 1) GrowthBook switch: effective state or raw value/payload changed
        if old.get("effective")!=cur["effective"] or json.dumps(old.get("gb"),sort_keys=True)!=json.dumps(cur["gb"],sort_keys=True):
            report["switches"].append({"flag":flag,"from":old.get("gb"),"to":cur["gb"],
                                       "eff_from":old.get("effective"),"eff_to":cur["effective"],"bin":cur["bin"]})
        # 3) DCE switch: binary presence class changed
        if old.get("bin")!=cur["bin"]:
            report["dce_switches"].append({"flag":flag,"from":old.get("bin"),"to":cur["bin"]})
    # flags that disappeared from GrowthBook entirely
    for flag in pf:
        if flag not in cf:
            report["dce_switches"].append({"flag":flag,"from":pf[flag].get("bin"),"to":"removed-from-growthbook"})

open(os.path.expanduser("~/.claude/cache/cc-feature-tracker/last-report.json"),"w").write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
PY
```

## Step 3: Explain the changes (you, the agent)

Read `last-report.json`.

**Golden rule — every flag mentioned gets a feature description.** Ray reads this tracker to be *reminded of what each flag actually did*, not just that it moved. So for **every** entry in all three categories, you MUST include a 1–2 sentence plain-English description of the feature the flag controls: what it does, what it gates, what behavior/UI/endpoint/prompt it changes. Never report a bare transition (e.g. "`tengu_x` — wired → stripped") with no description. If you don't already know what a flag does, `grep -n 'tengu_x' $STRINGS` and read a wide window (±40 lines) around the `ct("tengu_x"` call site — look for: a `name:"/command"`, a description/help string, the function it gates, prompt text it injects, env vars, API paths — and reconstruct the feature from that. If the binary genuinely reveals nothing (e.g. the string is fully stripped), say so explicitly ("code gone this build, can't recover behavior; last known purpose: …") rather than omitting the description.

- **If `first_run` is true:** this is the baseline. Do not send a long diff — send one line: "📊 Baseline captured for Claude Code v{version}: {N} flags tracked." Then stop.
- **For each `switches` entry:** name the feature in plain English, then **describe what it does** (per the golden rule). Report `feature — was {on/off} → now {on/off}`, whether the change is via GrowthBook or an env override, and the description. Note whether the code is still wired (so the flip actually changes behavior) or stripped (flip is a no-op).
- **For each `new_flags` entry:** inspect the binary to infer **what it does**. `grep -n 'tengu_x' $STRINGS`, read a wide window around each hit. Write a 1–2 sentence "probably does X" with your confidence. Note whether it's `wired` (real code, an actual upcoming feature) or only `telemetry`/`stripped` (a name with no behavior yet).
- **For each `dce_switches` entry:** report the transition AND describe the feature that was added/removed/retired (per the golden rule). `wired/present → stripped` = feature code was **removed** this version (describe what was removed, from your prior knowledge + any residual strings). `stripped/absent → wired` = code was **newly shipped** (describe the now-real feature). `→ removed-from-growthbook` = the flag was retired server-side (note whether code remains and how it's now reachable, e.g. an env var).

## Step 4: Record locally

The snapshot is already written to `~/.claude/cache/cc-feature-tracker/snapshot-latest.json`. Append a dated, human-readable entry to the changelog so there's a durable history:

```bash
LOG=~/Desktop/ray-os/routines/claude-code-feature-log.md
{
  echo ""
  echo "## $(date +%Y-%m-%d\ %H:%M) — v{VERSION}"
  echo ""
  echo "<paste the formatted switches / new flags / dce switches here; write 'No changes.' if all three empty>"
} >> "$LOG"
```

## Step 5: Notify Ray via Slack DM

Only if there is at least one switch, new flag, or DCE change (skip the message entirely on a no-change run — do not spam). Use the **slackbot-message** skill (NOT a webhook), sending to the channel **`cc-feature-tracker`** (Ray's private tracker channel). Slack mrkdwn = single `*asterisks*` for bold.

```bash
bash ~/.claude/skills/slackbot-message/scripts/send-message.sh "cc-feature-tracker" "$MESSAGE"
```

Message format (omit any section that's empty). **Every bullet must carry a feature description** — see the golden rule in Step 3. The bullet structure is: `{transition} — {what the feature does}`.

```
🚩 *Claude Code feature tracker* — v{VERSION}{ , upgraded from vX if version changed}

*🔀 GrowthBook switches*
• {feature name} (`tengu_x`) — was {OFF} → now {ON}  _(via {GrowthBook|env})_. {1–2 sentence description of what the feature does / what it gates. Note if code is still wired vs stripped.}

*🆕 New flags*
• `tengu_y` — probably {1–2 sentence description of what it does} _({wired/upcoming | telemetry-only | stripped})_

*🧱 DCE switches*
• `tengu_z` — {newly shipped code | code removed | retired from GrowthBook} ({old}→{new}). {1–2 sentence description of the feature that was added/removed/retired, and how it's now reachable if it still exists.}
```

Example of the expected level of detail (this is the bar — note how each bullet reminds Ray what the flag *did*):

```
*🔀 GrowthBook switches*
• Skills health dashboard (`tengu_skills_dashboard_enabled`) — was ON → now OFF _(via GrowthBook)_. Gates the `GET /api/claude_code/skills` health fetch that surfaces per-skill good/warn/poor status. Code still wired, just gated off for your account.

*🧱 DCE switches*
• `tengu_chert_bezel` — code removed (wired → stripped). Flag string is gone from the binary entirely this build; last known purpose unrecoverable from this version.
• `tengu_kairos_brief` — retired from GrowthBook (was wired). "Brief" concise-output mode; code remains, now reachable only via the `CLAUDE_CODE_BRIEF` env var.
• `tengu_neapolitan` — retired from GrowthBook (was wired). A git-state gate (checks cwd/HEAD, skips on `CLAUDE_CODE_REMOTE`); code still present, just no longer server-gated.
```

If `SLACK_BOT_TOKEN`/skill is unavailable, print the full message to stdout instead so it lands in the run log.

---

## Reference (discovered constants — for debugging / extending)

- **GrowthBook:** SDK `cdn.growthbook.io`, client key `sdk-zAZezfDKGoZuXXKe`, `remoteEval:true`, features **encrypted** → can't fetch raw; read the resolved cache from `~/.claude.json` instead.
- **Local levers:** `CLAUDE_CODE_GB_BASE_URL` overrides the GrowthBook host (point at a proxy to force-enable server-gated flags); `DISABLE_GROWTHBOOK` turns gate evaluation off entirely.
- **Classification patterns in the binary:** `ct("flag",default)` = real gate · `j("flag",{...})` = telemetry event · absent = stripped.
- **Self-enable env overrides** are listed in the `OVERRIDES` map in Step 2 — add any new ones you discover (grep `CLAUDE_CODE_*` near a flag's call site) so the effective-state calc stays accurate.
- **Stripped vs upcoming:** a flag set `false` in GrowthBook with a live `ct()` call site = an *upcoming* feature (built, gated off, override-able). A flag with no binary string = *stripped* (flag exists server-side, no code) — flipping it does nothing.
