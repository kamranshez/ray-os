#!/usr/bin/env python3
"""WRITE stage for instructions mode: act on Ray's note, then CLEAR it.

Takes the draft from instructions_scan.py with Claude's `action` filled in per entry, applies
it, and then blanks `ai_instructions` — because an instruction that survives the pass that
honoured it re-fires on every future run, and Ray ends up being asked about a card he already
fixed. Clearing is not a courtesy here; it is what makes the field a queue rather than a pile.

The one exception is a STANDING preference ("always keep this card's sentence short"), which
is meant to outlive the pass that read it. The scan flags those; this script leaves them.

`action` is a comma-separated list, so one card can do several things:

  retts   regenerate the explanation audio. Writes `new_explanation` first if Claude supplied
          one. The media filename is keyed on the NOTE ID — never on the source sentence,
          which is what let two words mined from one bank sentence collide on a single audio
          file and read each other's explanations out loud.
  fields  the housekeeping fixes the scan found objectively: `。` into a blank picture (a blank
          one makes the back template replay the sentence audio on mobile), and strip the
          foreign fields an external tool left behind (English `definition`, pitch, frequency).
  route   move the card between the main and deferred decks. A deck move and only a deck move —
          nothing here suspends a card or tags it not-worth-learning. Ray mined these words on
          purpose; the diff decides SEQUENCING, never WORTH.
  none    the instruction needed no change to the card (or Claude couldn't act on it safely).
          With `none` the instruction is left in place unless --clear-anyway is passed — an
          instruction you didn't act on is not an instruction you've honoured.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _anki import anki_request, store_media  # noqa: E402
from _config import deck_deferred, deck_main, load_config  # noqa: E402
from _style import refuse_if_bad_explanations  # noqa: E402
from _env import load_skill_env, require_healthy_gemini_key  # noqa: E402
from generate_media_bank import gemini_tts  # noqa: E402

PICTURE_FILLER = "。"
VALID = {"retts", "fields", "route", "none"}


async def retts_one(entry, workdir, sem):
    """Render the explanation to a note-id-keyed file. Returns the stored name, or None."""
    text = entry.get("new_explanation", "").strip() or entry.get("explanation", "").strip()
    if not text:
        print(f"  ⚠ {entry['word']} — retts asked for but there's no explanation text to speak",
              file=sys.stderr)
        return None
    local = workdir / f"sm_explain_{entry['noteId']}.mp3"
    try:
        await gemini_tts(text, local, sem)
        # store_media may CORRECT the extension — always use what it hands back.
        return store_media(local, f"sm_explain_{entry['noteId']}.mp3")
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ {entry['word']} — TTS failed: {e}", file=sys.stderr)
        return None


def apply_one(entry, cfg, fm, audio_filename, dry_run):
    actions = {a.strip() for a in entry["action"].split(",") if a.strip()}
    f, did = {}, []

    if "retts" in actions:
        if entry.get("new_explanation", "").strip():
            f[fm["explanation"]] = entry["new_explanation"].strip()
            did.append("explanation rewritten")
        if audio_filename:
            f[fm["explanation_audio"]] = f"[sound:{audio_filename}]"
            did.append("explanation audio regenerated")

    if "fields" in actions:
        for fact in entry["facts"]:
            if fact == "picture_blank" and fm.get("picture"):
                f[fm["picture"]] = PICTURE_FILLER
                did.append("picture filler")
            elif fact.startswith("foreign_fields:"):
                for name in fact.split(":", 1)[1].split(","):
                    f[name] = ""
                did.append("foreign fields cleared")

    if f and not dry_run:
        anki_request("updateNoteFields", note={"id": entry["noteId"], "fields": f})

    if "route" in actions and entry.get("route"):
        deck = deck_deferred(cfg) if entry["route"] == "deferred" else deck_main(cfg)
        if not dry_run:
            anki_request("changeDeck", cards=entry["cards"], deck=deck)
        did.append(f"→ {deck}")

    return did, actions


def clear_instruction(entry, fm, actions, clear_anyway, dry_run):
    """Blank the field so a one-shot note can't re-fire. Standing preferences survive."""
    if entry.get("looks_standing"):
        return "kept (standing preference)"
    if "none" in actions and not clear_anyway:
        return "kept (no action taken — pass --clear-anyway to drop it)"
    if not dry_run:
        anki_request("updateNoteFields",
                     note={"id": entry["noteId"], "fields": {fm["ai_instructions"]: ""}})
    return "cleared"


async def main_async(args):
    cfg = load_config()
    fm = cfg["field_map"]
    draft = json.loads(Path(args.draft).read_text())
    entries = draft["entries"]
    if args.only:
        want = {int(x) for x in args.only.split(",")}
        entries = [e for e in entries if e["noteId"] in want]

    blank = [e["word"] for e in entries if not e.get("action", "").strip()]
    if blank:
        sys.exit(f"These entries have no `action` — Claude must decide what the instruction is "
                 f"asking for first:\n  {', '.join(blank)}")
    bad = [f'{e["word"]}: {a}' for e in entries
           for a in e["action"].split(",") if a.strip() and a.strip() not in VALID]
    if bad:
        sys.exit(f"Unknown action(s): {', '.join(bad)}\nValid: {', '.join(sorted(VALID))}")

    # House-style gate on whatever text retts would speak — a rewrite that doesn't open
    # by naming the word, OR an existing explanation that never did, would re-record the
    # exact defect Ray's note is complaining about. Empty text keeps its own per-entry
    # warn in retts_one (it means "no text to speak", not a style violation). Runs for
    # --dry-run too, so the plan is honest.
    refuse_if_bad_explanations(
        [(e["word"], e.get("new_explanation", "").strip() or e.get("explanation", ""))
         for e in entries if "retts" in e["action"]],
        "instructions_apply.py (retts)", allow_empty=True)

    audio = {}
    needs = [e for e in entries if "retts" in e["action"]]
    if needs:
        load_skill_env()
        if not args.dry_run:
            # Hard pre-flight: a retts on a missing/ephemeral key would silently strand
            # the card without audio — the exact defect retts exists to fix.
            require_healthy_gemini_key()
        workdir = Path(cfg["work_dir"]) / "instructions-tts"
        workdir.mkdir(parents=True, exist_ok=True)
        sem = asyncio.Semaphore(3)  # Gemini free tier is 10 RPM.
        if not args.dry_run:
            audio = dict(zip((e["noteId"] for e in needs),
                             await asyncio.gather(*(retts_one(e, workdir, sem) for e in needs))))

    print(f"{'DRY RUN — nothing written' if args.dry_run else 'Instructions mode'}\n")
    for e in entries:
        did, actions = apply_one(e, cfg, fm, audio.get(e["noteId"]), args.dry_run)
        state = clear_instruction(e, fm, actions, args.clear_anyway, args.dry_run)
        print(f'  {e["word"]}')
        print(f'    said : {e["ai_instructions"]}')
        print(f'    did  : {"; ".join(did) or "nothing"}')
        print(f'    note : {state}')
        print()

    if not args.dry_run:
        left = anki_request("findNotes",
                            query=f'note:"{cfg["note_type"]}" "{fm["ai_instructions"]}:_*"')
        print(f"{len(entries)} card(s) handled ✓   "
              f"{len(left)} instruction(s) still outstanding in the collection.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft", required=True, help="instructions.draft.json with `action` filled")
    ap.add_argument("--only", help="Comma-separated noteIds — apply a subset")
    ap.add_argument("--dry-run", action="store_true", help="Print the plan, write nothing")
    ap.add_argument("--clear-anyway", action="store_true",
                    help="Clear the instruction even on entries actioned `none`")
    asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    main()
