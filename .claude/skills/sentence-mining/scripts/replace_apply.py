#!/usr/bin/env python3
"""Replace mode — apply a reviewed replace-draft to Anki, in place.

For each entry (with `explanation` filled by Claude):
  - download the Immersion Kit image + audio (Linode CDN) and register them in
    Anki's media via storeMediaFile
  - Gemini-TTS the new explanation
  - ARCHIVE the current sentence (+ its old audio/image refs) into the
    `previous_versions` field, newest block first, so every prior version is
    recoverable and the old media never becomes "unused"
  - overwrite sentence / sentence_audio / picture / explanation / explanation_audio
  - retag the i-level (i1/i2/… reflecting how many other words are new for Ray)
  - rehabilitate the card (de-leech, unsuspend, reset scheduling to NEW at the
    FRONT of the new queue — or due today with --due-now)
  - clear the input flag:1 (default) so the redone card just rejoins the study
    queue. --done-flag N flags it instead. If the deck's new/day limit is 0, the
    reset cards can't surface — the script detects this and warns (fix: raise the
    limit, Custom Study, or --due-now).

Unfixable misses (no usable replacement in any corpus) are retired instead: tagged
`not-worth-learning`, suspended, and cleared off flag:1 (--keep-misses to skip).

`--dry-run` prints the old→new table and touches nothing (no downloads, no TTS,
no Anki writes) — use it for the review gate / summary.
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze  # strip_html
import generate_media_bank as gmb  # reuse gemini_tts + GEMINI_* config
from _env import load_skill_env, require_healthy_gemini_key
from _anki import anki_request, store_media
from _config import load_config, deck_main, deck_deferred
from _style import refuse_if_bad_explanations


def _norm(s):
    """Comparable form: strip html + spaces + trailing punctuation (for dedupe checks)."""
    return re.sub(r"[\s　。、！？…\.\!\?]+", "", analyze.strip_html(s))

I_TAGS = " ".join(f"i{n}" for n in range(0, 10)) + " i?"  # i0..i9 + i? — clear all, add one
RETIRE_TAG = "not-worth-learning"  # disposition for unfixable misses


# Media staging (URL download or local-file copy) and extension guessing are shared with
# the bank/new-card path — one implementation, so a fix to either applies to both.
_ext = gmb._ext_of
_stage = gmb._stage


async def process_one(entry, workdir: Path, sem):
    nid = entry["note_id"]
    base = f"sm_replace_{nid}"

    # An EMPTY picture field makes the note type's Back template re-render the
    # sentence audio (its {{^picture}} branch), so on mobile the sentence audio
    # autoplays on the back too. When the source ships no image, write "。" instead
    # of leaving it blank so {{#picture}} stays truthy and the back stays silent.
    if entry.get("image_url"):
        img_ext = _ext(entry["image_url"], "jpg")
        img_name = f"{base}_img.{img_ext}"
        _stage(entry["image_url"], workdir / img_name)
        img_name = store_media(workdir / img_name, img_name)
        entry["picture_field"] = f'<img src="{img_name}">'
    else:
        entry["picture_field"] = "。"

    # Extension is guessed from the URL, not the bytes -- an external source (IK /
    # Nadeshiko / web sentence sites) can serve content that doesn't match its own
    # URL's apparent extension. store_media() sniffs the real bytes and corrects
    # the filename before it's registered, so use its returned name below.
    snd_ext = _ext(entry["sound_url"], "mp3")
    snd_name = f"{base}_audio.{snd_ext}"
    _stage(entry["sound_url"], workdir / snd_name)
    snd_name = store_media(workdir / snd_name, snd_name)
    entry["sentence_audio_field"] = f"[sound:{snd_name}]"

    # Explanation TTS is best-effort: a dead/expired GEMINI key must NOT block the
    # card's sentence/audio/image update. On failure leave explanation_audio empty
    # (the explanation TEXT still lands; audio can be regenerated later).
    exp_name = f"{base}_explain.mp3"
    try:
        await gmb.gemini_tts(entry["explanation"], workdir / exp_name, sem)
        exp_name = store_media(workdir / exp_name, exp_name)
        entry["explanation_audio_field"] = f"[sound:{exp_name}]"
    except Exception as e:  # noqa: BLE001
        entry["explanation_audio_field"] = ""
        entry["tts_failed"] = True
        print(f"    · {entry['word']}: explanation TTS skipped ({str(e)[:60]})", file=sys.stderr)
    return entry


def archive_block(fm, old_snapshot, today):
    """Build the previous_versions block from the card's CURRENT sentence — TEXT ONLY
    (no audio/image; those stay on the live card and would just bloat the archive)."""
    old_text = analyze.strip_html(old_snapshot.get(fm["sentence"], "")).replace("\n", " ").strip()
    return f'<div class="sm-prev" data-archived="{today}">{old_text}</div>'


def set_flag(nid, flag):
    """Set the card's flag: 0 = remove the flag (default — a redone card just rejoins
    the study queue), 1-7 = a colored flag, None = leave the flag untouched. Anki flags
    are mutually exclusive, so setting one clears whatever the card was on (e.g. flag:1)."""
    if flag is None:
        return
    for c in anki_request("findCards", query=f"nid:{nid}"):
        anki_request("setSpecificValueOfCard", card=c, keys=["flags"],
                     newValues=[flag], warning_check=True)


def _miss_items(misses, fm):
    """Normalize the draft's `misses` to [(word, note_id)]. New drafts carry
    {word, note_id}; older drafts stored bare words — resolve those by the word field."""
    items = []
    for m in misses:
        if isinstance(m, dict):
            items.append((m.get("word", ""), m.get("note_id")))
        else:  # legacy: bare word string — look its card up
            hits = anki_request("findNotes", query=f'"{fm["word"]}:{m}" {deck_clause(load_config())}')
            items.append((m, hits[0] if hits else None))
    return items


def retire_note(nid):
    """An unfixable miss (no usable replacement in IK / Nadeshiko / bank) is retired:
    tag it `not-worth-learning`, suspend its cards, and clear the input flag so it
    leaves the fix queue and stops being re-picked by `replace_search --flag`."""
    if not nid:
        return []
    cards = anki_request("findCards", query=f"nid:{nid}")
    anki_request("addTags", notes=[nid], tags=RETIRE_TAG)
    if cards:
        try:
            anki_request("suspend", cards=cards)
        except Exception:  # noqa: BLE001
            pass
        for c in cards:
            anki_request("setSpecificValueOfCard", card=c, keys=["flags"],
                         newValues=[0], warning_check=True)
    return cards


def rehabilitate(nid, position=0, due_now=False):
    """A struggled-with card getting a fresh sentence should be re-learned cleanly:
    drop the leech tag, unsuspend (leeches are often auto-suspended), and reset the
    scheduling to new so it comes due again. Returns the card ids touched.

    `position` is the card's new-queue slot: forgetCards keeps the card's ORIGINAL
    due position, which for an old card can be a million deep — behind every unseen
    new card in the deck. Without repositioning, "rehabilitated" means "buried".

    `due_now=True` additionally runs setDueDate 0, which converts the new card into
    a review card due TODAY — the only way it surfaces when the deck's new/day is 0.
    Trade-off: it skips the learning steps."""
    cards = anki_request("findCards", query=f"nid:{nid}")
    if not cards:
        return []
    anki_request("removeTags", notes=[nid], tags="leech")
    try:
        anki_request("unsuspend", cards=cards)        # no-op if not suspended
    except Exception:  # noqa: BLE001
        pass
    anki_request("forgetCards", cards=cards)          # reset scheduling → new
    # forgetCards resets scheduling but leaves the rep/lapse COUNTERS intact, so a
    # "rehabilitated" card keeps its lapse history and re-leeches far too soon. Zero
    # them, and set `due` to the front of the new queue in the same per-card call.
    # setSpecificValueOfCard needs warning_check + integer values, and is per-card.
    for cid in cards:
        try:
            anki_request("setSpecificValueOfCard", card=cid,
                         keys=["reps", "lapses", "due"],
                         newValues=[0, 0, position], warning_check=True)
        except Exception:  # noqa: BLE001 — counter/position reset is best-effort
            pass
    if due_now:
        try:
            anki_request("setDueDate", cards=cards, days="0")
        except Exception as e:  # noqa: BLE001
            print(f"  · setDueDate failed for nid {nid}: {str(e)[:60]}", file=sys.stderr)
    return cards


def warn_zero_new_limit(card_ids):
    """Rehabilitated cards are NEW cards, so they only ever surface through their
    deck's new/day limit. Ray parks decks with new/day = 0 — on such a deck the old
    'reset to due — queued up next' claim was a lie: the cards sat invisible forever.
    Detect that per deck and say so instead. Returns the blocked (deck, count) list."""
    if not card_ids:
        return []
    per_deck = {}
    for ci in anki_request("cardsInfo", cards=card_ids):
        per_deck[ci["deckName"]] = per_deck.get(ci["deckName"], 0) + 1
    blocked = []
    for deck, n in sorted(per_deck.items()):
        try:
            per_day = anki_request("getDeckConfig", deck=deck).get("new", {}).get("perDay")
        except Exception:  # noqa: BLE001
            continue
        if per_day == 0:
            blocked.append((deck, n))
            print(f'  ⚠ "{deck}" has new/day = 0 — its {n} rehabilitated card(s) are at '
                  f"the FRONT of the new queue but will not appear until you raise the "
                  f"limit, use Custom Study → \"Increase today's new card limit\", or "
                  f"re-run with --due-now.", file=sys.stderr)
    return blocked


def apply_entry(entry, fm, today, done_flag=0, position=0, due_now=False):
    nid = entry["note_id"]
    old = entry["old_fields_snapshot"]
    existing_prev = old.get(fm.get("previous_versions", ""), "")
    new_prev = archive_block(fm, old, today) + existing_prev  # newest first

    fields = {
        fm["sentence"]: entry["new_sentence"],
        fm["sentence_audio"]: entry["sentence_audio_field"],
        fm["picture"]: entry["picture_field"],
        fm["explanation"]: entry["explanation"],
        fm["explanation_audio"]: entry["explanation_audio_field"],
    }
    # Archive only if the note type has a previous_versions field (optional, replace-only).
    if fm.get("previous_versions"):
        fields[fm["previous_versions"]] = new_prev
    anki_request("updateNoteFields", note={"id": nid, "fields": fields})
    # Retag i-level; leave the flag and the kind tag (claude-sentence-*) untouched.
    anki_request("removeTags", notes=[nid], tags=I_TAGS)
    anki_request("addTags", notes=[nid], tags=entry["i_level"])
    # Fresh sentence on a struggled-with card → de-leech + reset scheduling, front of queue.
    cards = rehabilitate(nid, position=position, due_now=due_now)
    # Clear the input flag (default) so the redone card just rejoins the study queue.
    # (--done-flag N to flag instead.)
    set_flag(nid, done_flag)
    return cards


def print_table(entries, misses):
    print(f"\n{'WORD':<10} {'iLvl':<4}  OLD  →  NEW")
    print("─" * 90)
    for e in entries:
        print(f"{e['word']:<10} {e['i_level']:<4}  {analyze.strip_html(e['old_sentence'])[:32]}")
        print(f"{'':<16}→ {e['new_sentence']}   « {e.get('translation','')[:40]} » [{e.get('title','')}]")
    if misses:
        words = [m["word"] if isinstance(m, dict) else m for m in misses]
        print(f"\nMISSES (unfixable → will be tagged '{RETIRE_TAG}' + suspended): "
              f"{', '.join(words)}")


def deck_clause(cfg):
    return f'(deck:"{deck_main(cfg)}" OR deck:"{deck_deferred(cfg)}")'


async def main_async(args):
    cfg = load_config()
    fm = cfg["field_map"]

    if args.rehab_flag is not None:  # de-leech + reset a whole flagged set
        nids = anki_request("findNotes", query=f"flag:{args.rehab_flag} {deck_clause(cfg)}")
        touched = []
        for i, nid in enumerate(nids):
            touched += rehabilitate(nid, position=i, due_now=args.due_now)
        print(f"Rehabilitated {len(nids)} card(s) flagged {args.rehab_flag} "
              f"(leech tag removed, unsuspended, reset to new at the front of the queue"
              f"{', made due today' if args.due_now else ''}).")
        if not args.due_now:
            warn_zero_new_limit(touched)
        return

    data = json.loads(Path(args.draft).expanduser().read_text())
    entries = data.get("entries", [])
    misses = data.get("misses", [])

    # House-style gate — runs for --dry-run too, so offenders are caught before the
    # old→new table ever reaches Ray. Drop an unwanted entry by DELETING it from the
    # draft, never by blanking its explanation.
    refuse_if_bad_explanations(
        [(e["word"], e.get("explanation", "")) for e in entries], "replace_apply.py")
    ready = entries

    if args.dry_run:
        print_table(ready, misses)
        retire_note_n = 0 if args.keep_misses else len(misses)
        print(f"\n[dry-run] {len(ready)} card(s) would be replaced, "
              f"{retire_note_n} unfixable miss(es) would be retired. Nothing written.")
        return

    # Idempotency guard: skip cards whose live sentence already equals the draft's new
    # one (re-running the same draft must NOT re-archive / double-apply).
    if ready:
        live = anki_request("notesInfo", notes=[e["note_id"] for e in ready])
        cur = {n["noteId"]: _norm(n["fields"].get(fm["sentence"], {}).get("value", "")) for n in live}
        already = [e for e in ready if cur.get(e["note_id"]) == _norm(e["new_sentence"])]
        if already:
            print(f"Skipping {len(already)} already-applied card(s): "
                  f"{', '.join(e['word'] for e in already)}", file=sys.stderr)
        ready = [e for e in ready if cur.get(e["note_id"]) != _norm(e["new_sentence"])]

    load_skill_env()
    # Hard pre-flight: refuse a missing/ephemeral key BEFORE any card is written.
    # Best-effort TTS only covers mid-run failures, not a key that predictably dies.
    require_healthy_gemini_key()

    today = datetime.date.today().isoformat()
    sem = asyncio.Semaphore(gmb.TTS_CONCURRENCY)
    with tempfile.TemporaryDirectory(prefix="sm_replace_") as tmp:
        workdir = Path(tmp)
        # Media download + TTS run concurrently (TTS gated to TTS_CONCURRENCY for the
        # Gemini RPM cap); Anki writes are serialized afterward to avoid write races.
        results = await asyncio.gather(
            *(process_one(e, workdir, sem) for e in ready), return_exceptions=True)
        done, touched = [], []
        for e, r in zip(ready, results):
            if isinstance(r, Exception):
                print(f"  ✗ {e['word']} — {r}", file=sys.stderr)
                continue
            df = None if args.done_flag < 0 else args.done_flag
            touched += apply_entry(e, fm, today, done_flag=df,
                                   position=len(done), due_now=args.due_now)
            done.append(e)
            print(f"  ✓ {e['word']} → {e['new_sentence'][:48]}", file=sys.stderr)

    sched_note = ("reset + made due today" if args.due_now
                  else "reset to new at the front of the queue")
    if args.done_flag < 0:
        flag_note = f"input flag left untouched, {sched_note}"
    elif args.done_flag == 0:
        flag_note = f"flag cleared, {sched_note}"
    else:
        flag_note = f"moved to flag {args.done_flag}, {sched_note}"
    print(f"\nReplaced {len(done)}/{len(ready)} cards in place ({flag_note}).")
    if not args.due_now:
        warn_zero_new_limit(touched)

    # Retire unfixable misses: tag not-worth-learning, suspend, clear the input flag so
    # they leave the fix queue. --keep-misses leaves them on the flag for a later pass.
    if misses:
        if args.keep_misses:
            words = [m["word"] if isinstance(m, dict) else m for m in misses]
            print(f"Misses (left on input flag): {', '.join(words)}")
        else:
            retired = []
            for word, nid in _miss_items(misses, fm):
                if retire_note(nid):
                    retired.append(word)
                else:
                    print(f"  · {word} — no card found to retire", file=sys.stderr)
            print(f"Retired {len(retired)} unfixable miss(es) "
                  f"(tagged '{RETIRE_TAG}', suspended): {', '.join(retired)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", help="Replace-draft JSON with explanations filled")
    ap.add_argument("--dry-run", action="store_true", help="Print old→new table; write nothing")
    ap.add_argument("--rehab-flag", type=int, default=None,
                    help="De-leech + unsuspend + reset-to-due every card flagged N "
                         "(no field changes). Use to rehabilitate an already-replaced batch.")
    ap.add_argument("--done-flag", type=int, default=0,
                    help="What to do with each redone card's flag. Default 0 = clear the "
                         "flag so it just rejoins the study queue (it's already reset to "
                         "due). 1-7 = set that colored flag instead. Negative = leave the "
                         "input flag untouched. Input is flag:1.")
    ap.add_argument("--due-now", action="store_true",
                    help="After the reset, setDueDate 0 so each redone card becomes a "
                         "review card due TODAY. Use when the deck's new/day limit is 0 "
                         "(otherwise a reset-to-new card never surfaces). Trade-off: "
                         "skips the learning steps.")
    ap.add_argument("--keep-misses", action="store_true",
                    help="Leave unfixable misses on the input flag. Default retires them: "
                         f"tag '{RETIRE_TAG}', suspend, clear the flag.")
    args = ap.parse_args()
    if not args.draft and args.rehab_flag is None:
        ap.error("pass --draft <file> (optionally --dry-run) or --rehab-flag N")
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
