#!/usr/bin/env python3
"""queue_cards.py — make finished cards actually SHOW UP for study.

The last mile every mode was missing. A card can be perfectly built — sentence, audio,
house-style explanation, i+1 verified — and still never appear, because the deck's
`new/day` limit is 0 (Ray's main deck is, so *every* card the skill made today was
invisible until this script existed). "Pushed 12 cards" is a lie if none of them surface.

Only ever queues the **main deck** — the i+1 cards. Deferred cards are deferred on
purpose (they're above i+1); dragging them into today's queue defeats the whole point of
routing them there, so this script refuses to touch that deck.

  --due-now         THE DEFAULT. setDueDate 0 on just these cards, so they come up today
                    regardless of the deck's new-card limit. Ray keeps main at new/day = 0
                    deliberately — he controls his intake by hand rather than letting Anki
                    meter it — so the right move is to surface *this batch* and leave the
                    limit alone, not to open the floodgates on a 9000-card deck.

  --raise-limit N   Bump the deck's new/day to at least N instead. Cards stay NEW and go
                    through the normal learning steps, but it changes the deck config for
                    EVERYTHING, not just this batch. Only use it if Ray explicitly asks —
                    a new/day of 0 is usually a choice, not an accident.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _config import load_config, deck_main  # noqa: E402
from _anki import anki_request  # noqa: E402


def resolve(args, cfg):
    """Note ids from a draft, an explicit list, or a query — then keep only the cards that
    actually live in the main deck."""
    if args.draft:
        d = json.loads(Path(args.draft).read_text())
        ids = [e.get("noteId") or e.get("note_id") for e in d["entries"]]
        ids = [i for i in ids if i]
    elif args.note_ids:
        ids = [int(x) for x in args.note_ids.split(",")]
    else:
        ids = anki_request("findNotes", query=args.query)
    if not ids:
        return []

    main = deck_main(cfg)
    notes = anki_request("notesInfo", notes=ids)
    card_ids = [c for n in notes for c in n["cards"]]
    if not card_ids:
        return []
    info = anki_request("cardsInfo", cards=card_ids)
    # Deferred (and anything else) is excluded by design — see the module docstring.
    # Suspended cards are excluded too: audiobook mode suspends the cards it RETIRES
    # (already-known words), and queueing one would drag a card Ray deliberately killed
    # back into his reviews.
    return [c for c in info if c["deckName"] == main and c["queue"] != -1]


def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--draft", help="A draft JSON — queue the cards it touched")
    src.add_argument("--note-ids", help="Comma-separated note ids")
    src.add_argument("--query", help="Anki query")
    how = ap.add_mutually_exclusive_group()
    how.add_argument("--raise-limit", type=int, metavar="N",
                     help="Raise the main deck's new/day to at least N (cards stay new)")
    how.add_argument("--due-now", action="store_true",
                     help="Make just these cards due today (skips learning steps)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    main_deck = deck_main(cfg)
    cards = resolve(args, cfg)
    if not cards:
        print(f"Nothing to queue in \"{main_deck}\" — no matching cards there "
              "(deferred cards are excluded on purpose).")
        return

    new_cards = [c for c in cards if c["type"] == 0]
    ids = [c["cardId"] for c in cards]
    words = [c["fields"].get(cfg["field_map"]["word"], {}).get("value", "?") for c in cards]

    conf = anki_request("getDeckConfig", deck=main_deck)
    per_day = conf["new"]["perDay"]

    if args.dry_run:
        print(f"{len(cards)} card(s) in \"{main_deck}\" (new/day = {per_day}):")
        print("  " + "、".join(words))
        return

    if args.raise_limit:
        if per_day < args.raise_limit:
            conf["new"]["perDay"] = args.raise_limit
            anki_request("saveDeckConfig", config=conf)
            print(f'Raised new/day on "{main_deck}": {per_day} → {args.raise_limit}')
        else:
            print(f'"{main_deck}" already allows {per_day} new/day — no change needed.')
        print(f"{len(new_cards)} new card(s) will come up in the normal learning steps:")
    elif args.due_now:
        anki_request("setDueDate", cards=ids, days="0")
        print(f"{len(cards)} card(s) set due today (they skip the learning steps):")
    else:
        # No mechanism chosen — just report, and say what's actually blocking them.
        print(f'"{main_deck}": new/day = {per_day}, {len(new_cards)} new card(s) waiting.')
        if per_day == 0:
            print("  ⚠ new/day is 0 — these will NOT appear on their own.")
            print("    Re-run with --due-now to surface just this batch (keeps the limit at 0).")
        return

    print("  " + "、".join(words))


if __name__ == "__main__":
    main()
