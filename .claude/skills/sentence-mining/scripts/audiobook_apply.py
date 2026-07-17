#!/usr/bin/env python3
"""audiobook_apply.py — audiobook mode, step 3. Commits the draft that audiobook_scan.py
produced and Claude filled in.

Per card, in order:

  1. Gemini TTS on the (Claude-written, house-style) explanation → store via
     _anki.store_media(), which sniffs the real container. This matters more here than
     anywhere else in the skill: audiobook cards were created by an EXTERNAL tool, so
     their sentence audio never went through store_media() and can be a .mp3 that is
     really M4A — silently unplayable on AnkiMobile. Run audit_media.py --fix alongside.
  2. Overwrite explanation + explanation_audio.
  3. Normalize fields: clear the tool's leftovers (definition, pitch_accent, frequency_*)
     and write `。` into a blank picture. A blank picture makes the Back template
     re-render sentence_audio, so the card autoplays its audio on BOTH sides on mobile.
  4. Route: deferred (above i+1 with no rescue, or the lemma already matured elsewhere)
     / leave in main. Retag with the i-level.

Routing is automatic and reported after the fact — Ray's call in July 2026. Nothing here
is destructive: a deck move is a deck move, and this script NEVER suspends a card or tags
one `not-worth-learning`. Anki's review queue is the real gate. (See the comment below on
why the known-word diff only sequences these cards and never vetoes them.)
"""
import argparse
import asyncio
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _env import load_skill_env, require_healthy_gemini_key  # noqa: E402
load_skill_env()

from _config import load_config, deck_main, deck_deferred  # noqa: E402
from _anki import anki_request, store_media  # noqa: E402
from _style import refuse_if_bad_explanations  # noqa: E402
from generate_media_bank import gemini_tts  # noqa: E402

I_TAGS = {f"i{n}" for n in range(1, 10)} | {"i?"}
PICTURE_FILLER = "。"

# This script never suspends a card and never tags one `not-worth-learning`. Ray mines these
# words on purpose while reading, so a card that exists is a card he wants; the i+1 diff gets
# to influence WHEN he sees it (main vs deferred), never WHETHER. A deck move he can undo in
# one click; a suspend on a bad diff result is a word he chose vanishing without a trace.
#
# There's also no "processed" tag. Done-ness lives in the fields (audiobook_scan.py's defect
# check), not in a marker tag that can drift — and Ray's audiobook-viewer rewrites tags on
# re-sync, so a marker tag drifts immediately.


async def tts_one(entry, workdir, sem):
    """Render the explanation. Returns the stored media filename, or None on failure —
    a card with no explanation audio is still worth its field fixes, so we don't abort."""
    local = workdir / f"audiobook_exp_{entry['noteId']}.mp3"
    try:
        if not local.exists():
            await gemini_tts(entry["explanation"], local, sem)
        # store_media may CORRECT the extension; always use what it hands back.
        return store_media(local, f"audiobook_exp_{entry['noteId']}.mp3")
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ TTS failed for {entry['word']}: {e}", file=sys.stderr)
        return None


def apply_one(entry, cfg, fm, audio_filename):
    f = {}
    if entry.get("explanation", "").strip():
        f[fm["explanation"]] = entry["explanation"]
    if audio_filename:
        f[fm["explanation_audio"]] = f"[sound:{audio_filename}]"

    # Blank picture => back template replays sentence audio (double audio on mobile).
    for d in entry["defects"]:
        if d == "picture_blank":
            f[fm["picture"]] = PICTURE_FILLER
        elif d.startswith("foreign_fields:"):
            for name in d.split(":", 1)[1].split(","):
                f[name] = ""

    if f:
        anki_request("updateNoteFields", note={"id": entry["noteId"], "fields": f})

    # Refresh the i-level tag so Ray can still filter by complexity in Anki.
    stale = [t for t in entry["tags"] if t in I_TAGS]
    if stale:
        anki_request("removeTags", notes=[entry["noteId"]], tags=" ".join(stale))
    anki_request("addTags", notes=[entry["noteId"]], tags=entry["i_level"])

    # Route — a deck move, and only a deck move.
    if entry["route"] in ("deferred", "rescue"):
        # `rescue` reaching this script means replace mode found nothing easier, so the dense
        # sentence stands — park it in deferred rather than drilling it at i+3. Same for a
        # word whose lemma already matured elsewhere: later, not never.
        anki_request("changeDeck", cards=entry["cards"], deck=deck_deferred(cfg))
        return "deferred"
    return "main"


async def main_async(args):
    cfg = load_config()
    fm = cfg["field_map"]
    draft = json.loads(Path(args.draft).read_text())
    entries = draft["entries"]

    if args.only:
        keep = {int(x) for x in args.only.split(",")}
        entries = [e for e in entries if e["noteId"] in keep]

    missing = [e["word"] for e in entries if not e.get("explanation", "").strip()]
    if missing and not args.allow_missing_explanations:
        print("These entries have no explanation — Claude must write them first "
              f"(or pass --allow-missing-explanations to fix fields only):\n  {', '.join(missing)}",
              file=sys.stderr)
        sys.exit(1)

    # House-style gate on the non-empty explanations — NOT waivable: a written
    # explanation that doesn't open by naming the word is the #1 defect this very
    # mode exists to fix, so writing one back would be self-defeating.
    refuse_if_bad_explanations(
        [(e["word"], e["explanation"]) for e in entries if e.get("explanation", "").strip()],
        "audiobook_apply.py")

    if args.dry_run:
        for e in entries:
            print(f"{e['word']:8} {e['i_level']:3} → {e['route']:8} | {e['route_reason']}")
            print(f"         fixes: {', '.join(e['defects']) or 'none'}")
        return

    # Hard pre-flight: refuse a missing/ephemeral GEMINI_API_KEY BEFORE any card is
    # written. Best-effort TTS below only covers genuinely mid-run failures — a key
    # that predictably dies would half-fix the whole batch (text lands, audio silently
    # doesn't), which is exactly how 41 cards shipped without audio in July 2026.
    if any(e.get("explanation", "").strip() for e in entries):
        require_healthy_gemini_key()

    workdir = Path(cfg["work_dir"]) / "audiobook-tts"
    workdir.mkdir(parents=True, exist_ok=True)

    sem = asyncio.Semaphore(int(os.environ.get("SM_TTS_CONCURRENCY", "2")))
    needs_tts = [e for e in entries if e.get("explanation", "").strip()]
    audio = dict(zip(
        (e["noteId"] for e in needs_tts),
        await asyncio.gather(*(tts_one(e, workdir, sem) for e in needs_tts)),
    ))

    results = defaultdict(list)
    for e in entries:
        results[apply_one(e, cfg, fm, audio.get(e["noteId"]))].append(e["word"])

    # ---- post-write verify: report what's actually ON the cards, never what we meant ----
    # An earlier version printed "brought to house standard ✓" unconditionally, so a run
    # whose TTS silently failed still claimed success — and nobody noticed the missing
    # audio until review time. Re-read every note and let the fields do the talking.
    mapped = set(fm.values())
    live = {n["noteId"]: n["fields"]
            for n in anki_request("notesInfo", notes=[e["noteId"] for e in entries])}
    incomplete = []
    for e in entries:
        f = live.get(e["noteId"], {})
        get = lambda key: f.get(fm.get(key, ""), {}).get("value", "").strip()  # noqa: E731
        probs = [msg for cond, msg in (
            (not get("explanation"), "no explanation"),
            (not get("explanation_audio"), "NO EXPLANATION AUDIO"),
            (not get("picture"), "blank picture"),
            (any(k not in mapped and v.get("value", "").strip() for k, v in f.items()),
             "foreign fields left"),
        ) if cond]
        if probs:
            incomplete.append((e["word"], probs))

    done = len(entries) - len(incomplete)
    if incomplete:
        print(f"\nAudiobook mode: {done}/{len(entries)} card(s) verified at house standard — "
              f"{len(incomplete)} NOT done:")
        for w, probs in incomplete:
            print(f"  ⚠ {w}: {', '.join(probs)}")
        print("  Re-run this draft once the cause is fixed (already-clean fields are skipped).")
    else:
        print(f"\nAudiobook mode: {len(entries)} card(s) at house standard — "
              "verified on the cards ✓")
    print()
    if results["main"]:
        print(f"  → {deck_main(cfg)} (i+1): {len(results['main'])}")
        print(f"      {'、'.join(results['main'])}")
    if results["deferred"]:
        print(f"  → {deck_deferred(cfg)} (above i+1, or lemma already matured — "
              f"learn later, nothing dropped): {len(results['deferred'])}")
        print(f"      {'、'.join(results['deferred'])}")
    print("\nNow run:  python3 scripts/audit_media.py --fix")
    print("  (audiobook audio was made by an external tool, so it never passed through")
    print("   store_media() — a .mp3 that's really M4A is silently mute on AnkiMobile.)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True, help="audiobook.draft.json with explanations filled")
    ap.add_argument("--only", help="Comma-separated noteIds — apply just these")
    ap.add_argument("--dry-run", action="store_true", help="Print the plan; write nothing")
    ap.add_argument("--allow-missing-explanations", action="store_true",
                    help="Fix fields/routing even where Claude left the explanation empty")
    asyncio.run(main_async(ap.parse_args()))


if __name__ == "__main__":
    main()
