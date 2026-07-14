#!/usr/bin/env python3
"""SOURCE stage for instructions mode: find every card Ray left a note on.

`ai_instructions` is the field Ray types into while reviewing in Anki — a free-text note to
the next AI pass on that specific card ("the explanation is too hard", "the audio is wrong").

Until this script existed the field was only ever read by replace_search.py (which sees only
FLAGGED cards) and audiobook_scan.py (which sees only the audiobook batch you happen to be
processing). A note left on a plain video- or bank-mode card was read by nothing, ever: two
of them sat unnoticed in the collection for weeks. This script is the entry point that makes
the field actually mean something — it sweeps the whole note type, regardless of how the card
was made, whether it's flagged, or what deck it's in.

It decides NOTHING. It reports each card's instruction alongside enough of its current state
(explanation, audio, picture, foreign fields, i-level) for Claude to work out what the
instruction is asking for, then hands over to instructions_apply.py — which is also the thing
that CLEARS the instruction, so a one-shot note can't re-fire on the next run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import analyze  # noqa: E402
from _anki import anki_request  # noqa: E402
from _config import load_config  # noqa: E402

# A standing preference is meant to survive; a one-shot instruction is meant to be consumed.
# We can't tell them apart mechanically, so flag the likely standing ones for Claude to leave.
STANDING_HINTS = ("always", "from now on", "in future", "every time", "never ")


def looks_standing(text: str) -> bool:
    return any(h in text.lower() for h in STANDING_HINTS)


def diagnose(fields: dict, fm: dict) -> list[str]:
    """Objective, checkable facts about the card — NOT a reading of the instruction.

    Claude reads the instruction; this just saves it a round-trip to Anki to find out whether
    the card actually is missing audio / has a blank picture / still carries foreign fields.
    """
    def val(role):
        return fields.get(fm.get(role, ""), {}).get("value", "")

    facts = []
    if not val("explanation").strip():
        facts.append("explanation_empty")
    if not val("explanation_audio").strip():
        facts.append("explanation_audio_missing")
    if not val("picture").strip():
        facts.append("picture_blank")

    word = analyze.strip_html(val("word")).strip()
    exp = analyze.strip_html(val("explanation")).strip()
    # The house style: every explanation opens by naming the word. The TTS is the whole point —
    # an explanation that dives into the definition cold never says the headword out loud.
    if exp and word and word not in exp[: len(word) + 8]:
        facts.append("explanation_not_house_style")

    foreign = [f for f in ("definition", "pitch_accent", "frequency_yomitan", "frequency_addon")
               if fields.get(f, {}).get("value", "").strip()]
    if foreign:
        facts.append("foreign_fields:" + ",".join(foreign))

    # The bug that started all this: two words mined from one source sentence shared a single
    # explanation-audio FILE, so one card read out the other's explanation. Cheap to check.
    return facts


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", help="Override the Anki query (default: every note of the "
                                    "configured type with a non-empty ai_instructions)")
    ap.add_argument("--output", help="Draft path (default: <work_dir>/instructions.draft.json)")
    args = ap.parse_args()

    cfg = load_config()
    fm = cfg["field_map"]
    aif = fm.get("ai_instructions")
    if not aif:
        sys.exit("No `ai_instructions` role in config.field_map — nothing to scan. "
                 "Map it in config.json (see references/note-type.md).")

    query = args.query or f'note:"{cfg["note_type"]}" "{aif}:_*"'
    note_ids = anki_request("findNotes", query=query)
    if not note_ids:
        print(f"No cards carry an ai_instruction. ✓  (query: {query})")
        return

    # Shared explanation-audio files: the collision that made 自己犠牲 play 浸る's explanation.
    all_notes = anki_request("notesInfo", notes=anki_request(
        "findNotes", query=f'note:"{cfg["note_type"]}"'))
    audio_users: dict[str, list[str]] = {}
    for n in all_notes:
        ea = n["fields"].get(fm.get("explanation_audio", ""), {}).get("value", "")
        for m in re.findall(r"\[sound:(.*?)\]", ea):
            audio_users.setdefault(m, []).append(
                analyze.strip_html(n["fields"].get(fm["word"], {}).get("value", "")).strip())

    entries = []
    for n in anki_request("notesInfo", notes=note_ids):
        f = n["fields"]
        instruction = analyze.strip_html(f[aif]["value"]).replace("\xa0", " ").strip()
        facts = diagnose(f, fm)

        ea = f.get(fm.get("explanation_audio", ""), {}).get("value", "")
        for m in re.findall(r"\[sound:(.*?)\]", ea):
            shared = [w for w in audio_users.get(m, []) if w]
            if len(shared) > 1:
                facts.append(f"explanation_audio_shared_with:{'、'.join(x for x in shared if x)}")

        entries.append({
            "noteId": n["noteId"],
            "cards": n["cards"],
            "word": analyze.strip_html(f[fm["word"]]["value"]).strip(),
            "sentence": analyze.strip_html(f[fm["sentence"]]["value"]).strip(),
            "explanation": analyze.strip_html(f.get(fm.get("explanation", ""), {})
                                              .get("value", "")).strip(),
            "explanation_audio": ea,
            "picture": f.get(fm.get("picture", ""), {}).get("value", ""),
            "tags": n["tags"],
            "ai_instructions": instruction,
            "looks_standing": looks_standing(instruction),
            "facts": facts,
            # Claude fills these in:
            "action": "",          # retts | fields | route | none
            "new_explanation": "",  # only when the instruction asks for a rewrite
            "route": "",           # main | deferred — only when the instruction asks for a move
        })

    out = Path(args.output or Path(cfg["work_dir"]) / "instructions.draft.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"source": "instructions", "entries": entries},
                              ensure_ascii=False, indent=2))

    print(f"{len(entries)} card(s) carry an ai_instruction:\n")
    for e in entries:
        standing = "  [reads as a STANDING preference — honour it, but do NOT clear it]" \
            if e["looks_standing"] else ""
        print(f'  {e["word"]}  ({e["noteId"]}){standing}')
        print(f'    says  : {e["ai_instructions"]}')
        print(f'    facts : {", ".join(e["facts"]) or "none — nothing objectively wrong"}')
        print(f'    sent  : {e["sentence"][:60]}')
        print()
    print(f"Draft: {out}\n")
    print("Now: read each instruction, decide what it's asking for, fill `action` "
          "(+ `new_explanation` / `route`), then run instructions_apply.py — which applies "
          "the change AND clears the instruction so it can't re-fire.")


if __name__ == "__main__":
    main()
