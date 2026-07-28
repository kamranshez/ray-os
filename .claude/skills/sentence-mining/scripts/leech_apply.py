#!/usr/bin/env python3
"""leech_apply.py — leech mode, stages 4-7. Apply a reviewed leech-draft to Anki.

Deliberately thin: every mechanism here already existed and was already debugged in
replace_apply.py, so this imports them rather than reimplementing them (media staging,
the explanation TTS, the previous_versions archive, rehabilitation, i+1 routing). What
is genuinely new in leech mode is the DISPOSITION of cards the cascade couldn't help,
and that's all that lives in this file.

Four things happen, in this order:

  1. RECOVERED — cards whose interval says they're fine now: strip the `leech` tag and
     touch NOTHING else. No forgetCards, no deck move, no field write. The whole point
     is that a card carrying a 338-day interval keeps it.

  2. SWAPS — new sentence + media + explanation TTS, old sentence archived, blank
     picture filled, i+1 retag and routing, then full rehabilitation (reps and lapses
     zeroed, front of the queue) with --due-now by default. Ray's main deck runs at
     new/day = 0, so a rehabilitated card that ISN'T made due today is invisible; the
     accepted trade-off is that it skips the learning steps.

  3. DELETES — misses (no usable sentence in any corpus) and the losing half of an
     interference twin. These are NOT suspended and NOT tagged not-worth-learning: Ray
     asked for deletion, after seeing the batch. So deletion needs --confirm-delete,
     which is meant to be passed only after the --dry-run table has been read by a
     human. Anki logs deleted notes' fields to deleted.txt, so the TEXT survives; the
     scheduling history and note id do not.

  4. TWIN SURVIVORS — the half of a merged pair that lives loses its `leech` tag too
     (its competitor is gone, which was the remedy) but keeps its scheduling. It gets no
     sentence swap: it was never diagnosed as having a bad sentence.

Every card this script touches loses the `leech` tag. That is what makes re-running it
safe — there's no ex-leech marker, so the tag itself is the queue, and Anki re-tags on
further lapses if a fix didn't hold.
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import analyze                       # noqa: E402 — strip_html
import generate_media_bank as gmb    # noqa: E402 — TTS concurrency knob
import replace_apply as ra           # noqa: E402 — THE shared apply machinery
from _anki import anki_request       # noqa: E402
from _config import load_config, deck_main, deck_deferred  # noqa: E402
from _env import load_skill_env, require_healthy_gemini_key  # noqa: E402
from _style import refuse_if_bad_explanations  # noqa: E402

LEECH_TAG = "leech"


def untag(note_ids):
    """Drop the leech tag. Anki re-adds it on further lapses, so this is not a
    suppression — it's handing the tag back its meaning as a live signal."""
    if note_ids:
        anki_request("removeTags", notes=list(note_ids), tags=LEECH_TAG)


DEFER_QUEUE_POSITION = 1_000_000  # back of the new queue — deferred means "after everything"


def apply_skipped(entry, cfg, fm, index):
    """A struggling leech that is NOT getting a new sentence.

    Two dispositions, both keeping the card's existing sentence:

      defer_rare      the word is rarer than config.leech.rare_rank_cutoff. Reset and
                      send to the DEFERRED deck at the BACK of the new queue. Rare +
                      failing means the card is costing more than it returns today; it
                      is not worth deleting, it's worth postponing.
      keep_sentence   the current sentence is BETTER than anything the cascade offered
                      (屈託's 屈託ない collocation, 2026-07-28). Clean slate in place:
                      same deck, front of the queue, due today.

    Both fill a genuinely blank picture (checked against the RAW field — an <img> tag
    strips to "" and must not be mistaken for empty) and both drop the leech tag."""
    nid = entry["note_id"]
    defer = entry.get("disposition") == "defer_rare"

    snapshot = entry.get("old_fields_snapshot") or {}
    pic_field = fm.get("picture", "")
    if pic_field and not snapshot.get(pic_field, "").strip():
        # Blank picture makes the Back template re-render sentence_audio → the card
        # double-plays its audio on mobile. "。" keeps {{#picture}} truthy.
        anki_request("updateNoteFields", note={"id": nid, "fields": {pic_field: "。"}})

    cards = ra.rehabilitate(nid,
                            position=DEFER_QUEUE_POSITION + index if defer else index,
                            due_now=not defer)
    if defer and cards:
        target, main, deferred = deck_deferred(cfg), deck_main(cfg), deck_deferred(cfg)
        try:
            info = anki_request("cardsInfo", cards=cards)
            current = {c.get("deckName", "") for c in info}
            # Same guard as replace_apply.apply_route: never yank a card out of a deck
            # it was deliberately filed in outside the mining pair.
            if current <= {main, deferred} and current != {target}:
                anki_request("changeDeck", cards=cards, deck=target)
        except Exception as e:  # noqa: BLE001
            print(f"  · {entry['word']}: deck move failed ({str(e)[:60]})", file=sys.stderr)
    return cards


def delete_targets(data, only=None):
    """[(note_id, word, why, detail)] — every note the draft proposes to delete."""
    out = []
    for m in data.get("misses", []):
        if only and m["note_id"] not in only:
            continue
        out.append((m["note_id"], m["word"], "no usable sentence in any corpus",
                    f"{m.get('lapses', 0)} lapses / {m.get('interval', 0)}d · "
                    f"tried {', '.join(m.get('forms_tried', []))} · "
                    f"«{m.get('old_sentence', '')[:44]}»"))
    for t in data.get("twins", []):
        lose_id = t["proposed_delete"]
        if only and lose_id not in only:
            continue
        lose = next((c for c in t["cards"] if c["note_id"] == lose_id), {})
        out.append((lose_id, t["word"], "loses the interference merge",
                    f"{t['reason']} · «{lose.get('sentence', '')[:44]}»"))
    return out


def print_delete_table(targets):
    print(f"\n{'─' * 92}\nDELETE GATE — {len(targets)} note(s) proposed for deletion")
    print("Anki logs the fields to deleted.txt; scheduling history and note id are gone.")
    print("─" * 92)
    for nid, word, why, detail in targets:
        print(f"  {word:<12} nid:{nid}  ({why})")
        print(f"  {'':<12} {detail}")
    print("─" * 92)


def print_dry_run(data, entries, cfg):
    main, deferred = deck_main(cfg), deck_deferred(cfg)
    rec = data.get("recovered", [])
    if rec:
        print(f"\nRECOVERED — {len(rec)} card(s): strip the '{LEECH_TAG}' tag, "
              f"change nothing else")
        head = ", ".join(f"{r['word']}({r['interval']}d/{r['lapses']}L)" for r in rec[:10])
        print(f"  {head}{' …' if len(rec) > 10 else ''}")
        print(f"  interval range: {min(r['interval'] for r in rec)}-"
              f"{max(r['interval'] for r in rec)}d — scheduling untouched")

    if entries:
        print(f"\nSWAPS — {len(entries)} card(s)")
        print(f"\n{'WORD':<10} {'L/ivl':<8} {'iLvl':<4}  OLD  →  NEW")
        print("─" * 92)
        for e in entries:
            dest = main if ra.route_for(e) == "main" else deferred
            print(f"{e['word']:<10} {str(e.get('lapses', 0)) + '/' + str(e.get('interval', 0)) + 'd':<8} "
                  f"{e.get('i_level', '?'):<4}  {analyze.strip_html(e['old_sentence'])[:38]}")
            print(f"{'':<25}→ {e['new_sentence']}   « {e.get('translation', '')[:34]} »")
            print(f"{'':<25}  ⇒ {dest}   defects: {', '.join(e.get('defects', [])) or '—'}")
        n_main = sum(1 for e in entries if ra.route_for(e) == "main")
        print(f"\nRouting: → {main} (i+1): {n_main}   → {deferred}: {len(entries) - n_main}")

    skipped = data.get("skipped", [])
    if skipped:
        print(f"\nNO SWAP — {len(skipped)} card(s) keep their current sentence")
        for s in skipped:
            if s.get("disposition") == "defer_rare":
                dest, why = deferred, f"rare — {s.get('skip_reason', '')}"
            else:
                dest, why = "stays put", s.get("skip_reason", "current sentence is better")
            print(f"  {s['word']:<10} {s.get('lapses', 0)}/{s.get('interval', 0)}d  "
                  f"⇒ {dest}   ({why})")
            print(f"{'':<12} «{s.get('old_sentence', '')[:60]}»")

    targets = delete_targets(data)
    if targets:
        print_delete_table(targets)
    for t in data.get("twins", []):
        keep = next((c for c in t["cards"] if c["note_id"] == t["proposed_survivor"]), {})
        print(f"\nTWIN {t['word']} — proposing to KEEP nid:{keep.get('note_id')} "
              f"({keep.get('interval', 0)}d / {keep.get('lapses', 0)} lapses)")
        print(f"    «{keep.get('sentence', '')}»")
        print("    (survivor keeps its scheduling; it just loses the leech tag)")

    print(f"\n[dry-run] {len(data.get('recovered', []))} de-tag, {len(entries)} swap, "
          f"{len(data.get('skipped', []))} no-swap, {len(targets)} delete "
          f"(needs --confirm-delete). Nothing written.")


async def main_async(args):
    cfg = load_config()
    fm = cfg["field_map"]
    data = json.loads(Path(args.draft).expanduser().read_text(encoding="utf-8"))
    only = {int(x) for x in args.only.split(",") if x.strip()} if args.only else None

    entries = data.get("entries", [])
    if only:
        entries = [e for e in entries if e["note_id"] in only]

    # House-style gate — runs for --dry-run too, so offenders never reach the table.
    refuse_if_bad_explanations(
        [(e["word"], e.get("explanation", "")) for e in entries], "leech_apply.py")

    if args.dry_run:
        print_dry_run(data, entries, cfg)
        return

    # ---- 1. recovered: de-tag only ----
    rec_ids = [r["note_id"] for r in data.get("recovered", [])
               if not only or r["note_id"] in only]
    if rec_ids and not args.skip_recovered:
        untag(rec_ids)
        print(f"Recovered: stripped '{LEECH_TAG}' from {len(rec_ids)} card(s) — "
              f"no scheduling touched.")

    # ---- 2. swaps ----
    done = []
    if entries:
        live = anki_request("notesInfo", notes=[e["note_id"] for e in entries])
        cur = {n["noteId"]: ra._norm(n["fields"].get(fm["sentence"], {}).get("value", ""))
               for n in live}
        already = [e for e in entries if cur.get(e["note_id"]) == ra._norm(e["new_sentence"])]
        if already:
            print(f"Skipping {len(already)} already-applied card(s): "
                  f"{', '.join(e['word'] for e in already)}", file=sys.stderr)
        entries = [e for e in entries if cur.get(e["note_id"]) != ra._norm(e["new_sentence"])]

    if entries:
        load_skill_env()
        require_healthy_gemini_key()
        today = datetime.date.today().isoformat()
        sem = asyncio.Semaphore(gmb.TTS_CONCURRENCY)
        routed = {"main": [], "deferred": [], "kept": []}
        import tempfile
        with tempfile.TemporaryDirectory(prefix="sm_leech_") as tmp:
            workdir = Path(tmp)
            results = await asyncio.gather(
                *(ra.process_one(e, workdir, sem) for e in entries), return_exceptions=True)
            touched = []
            for e, r in zip(entries, results):
                if isinstance(r, Exception):
                    print(f"  ✗ {e['word']} — {r}", file=sys.stderr)
                    continue
                # done_flag=None: leech cards weren't selected by a flag, so whatever
                # flag Ray put on one is his and must survive the run.
                cards, route = ra.apply_entry(e, fm, today, cfg, done_flag=None,
                                              position=len(done), due_now=not args.no_due_now)
                touched += cards
                routed[route].append(e["word"])
                done.append(e)
                print(f"  ✓ {e['word']} → {e['new_sentence'][:44]}", file=sys.stderr)

        print(f"\nSwapped {len(done)}/{len(entries)} card(s) "
              f"(rehabilitated: reps/lapses zeroed, leech tag dropped"
              f"{', due today' if not args.no_due_now else ''}).")
        for key, label in (("main", deck_main(cfg)), ("deferred", deck_deferred(cfg)),
                           ("kept", "left in place (outside the mining decks)")):
            if routed[key]:
                print(f"  → {label}: {len(routed[key])}")
                print(f"      {'、'.join(routed[key])}")
        if args.no_due_now:
            ra.warn_zero_new_limit(touched)

    # ---- 2b. no-swap cards: keep the sentence, fix the picture, re-file ----
    skipped = [s for s in data.get("skipped", []) if not only or s["note_id"] in only]
    if skipped:
        moved, held = [], []
        for i, s in enumerate(skipped):
            apply_skipped(s, cfg, fm, i)
            (moved if s.get("disposition") == "defer_rare" else held).append(s["word"])
        if moved:
            print(f"\nDeferred {len(moved)} rare word(s) → {deck_deferred(cfg)} "
                  f"(sentence kept, back of the new queue): "
                  f"{'、'.join(moved)}")
        if held:
            print(f"Kept the existing sentence on {len(held)} card(s), reset and due today: "
                  f"{'、'.join(held)}")

    # ---- 3. deletes (misses + twin losers) ----
    targets = delete_targets(data, only)
    if targets:
        if not args.confirm_delete:
            print_delete_table(targets)
            print("NOT deleted — re-run with --confirm-delete once this list is approved.")
            print("Until then these keep their leech tag and will reappear next scan.")
        else:
            ids = [nid for nid, *_ in targets]
            anki_request("deleteNotes", notes=ids)
            print(f"\nDeleted {len(ids)} note(s): "
                  f"{', '.join(w for _n, w, *_ in targets)}")
            print("  (fields logged to deleted.txt in the Anki collection folder)")

    # ---- 4. twin survivors keep their scheduling, lose the tag ----
    if args.confirm_delete:
        keep_ids = [t["proposed_survivor"] for t in data.get("twins", [])
                    if not only or t["proposed_survivor"] in only]
        if keep_ids:
            untag(keep_ids)
            print(f"Twin survivors: stripped '{LEECH_TAG}' from {len(keep_ids)} card(s) "
                  f"(competitor removed; scheduling untouched).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True, help="leech-draft JSON with explanations filled")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the de-tag / swap / delete tables; write nothing")
    ap.add_argument("--confirm-delete", action="store_true",
                    help="Actually delete the misses and twin losers listed by --dry-run. "
                         "Without this they are left untouched and keep their leech tag.")
    ap.add_argument("--no-due-now", action="store_true",
                    help="Rehabilitate to NEW without setDueDate 0. Restores the learning "
                         "steps, but on a deck with new/day = 0 the cards stay invisible "
                         "until you raise the limit (see queue_cards.py).")
    ap.add_argument("--skip-recovered", action="store_true",
                    help="Don't strip the tag from recovered cards this run")
    ap.add_argument("--only", help="Comma-separated note ids to act on")
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
