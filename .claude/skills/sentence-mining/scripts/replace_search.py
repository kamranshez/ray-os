#!/usr/bin/env python3
"""Replace mode, SOURCE stage — find a BETTER example sentence for an EXISTING card.

The search itself lives in `_sources.py` (the canonical 5-tier cascade, re-ranked by
this collection's own i+1). This script is only the replace-mode wrapper around it:

    resolve which cards to fix  →  _sources.best_for_word(word, exclude=current sentence)
                                →  write a replace-draft for Claude to curate

The one replace-specific rule: a candidate IDENTICAL to the card's current sentence is
excluded, since that's not an improvement. So a word whose only hit is already on the
card is reported as a genuine miss rather than a no-op "replacement".

Input — which cards to fix (one of):
    --flag N            every card flagged N in the mining decks (Ray's input queue: flag:1)
    --note-ids a,b,c    explicit Anki note ids (audiobook mode's rescue set comes in here)
    --words 同期,西暦   resolve the existing card for each word

Output — replace-draft JSON (proposals; no media downloaded, no explanation yet):
    {"entries": [{note_id, word, reading, old_sentence, old_fields_snapshot,
                  ai_instructions, new_sentence, translation, image_url, sound_url,
                  title, source, i_level, extra_unknowns, bare_token, query_form,
                  word_form_differs, runner_ups}],
     "misses":  [{word, note_id, forms_tried, ai_instructions}]}

`query_form` is the spelling that actually found the sentence — the cascade retries a
word field's inflected forms (爽快だ → 爽快), so a hit may come from a form the card
doesn't carry. `word_form_differs` flags exactly that case for the curate step.

Claude then fills `explanation` per entry and runs replace_apply.py.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze                      # strip_html
import _sources                     # THE sentence engine (shared with find_sentences.py)
from _config import load_config, deck_main, deck_deferred, flag_ignored, flag_meaning
from _anki import anki_request
from _env import load_skill_env


def refuse_ignored_flag(cfg, flag, force, option):
    """Stop before touching a flag the user has marked off-limits.

    Ray's flag:7 is his tutoring-lesson record — 8 cards that are there to be looked at,
    not mined. Nothing recorded that, so a `--flag 7` run would have rewritten all of
    them. Name the recorded meaning so the refusal explains itself."""
    if flag is None or force or not flag_ignored(cfg, flag):
        return
    sys.exit(
        f"Refusing {option} {flag}: config.flags[\"{flag}\"] is marked ignore — "
        f"{flag_meaning(cfg, flag) or 'no meaning recorded'}.\n"
        f"These cards are not for mining. Pass --force-ignored-flag if you really "
        f"mean to include them."
    )


def resolve_notes(args, cfg):
    """Return [{note_id, word, reading, old_sentence, ai_instructions, old_fields_snapshot}]."""
    fm = cfg["field_map"]
    wf, rf, sf = fm["word"], fm.get("reading", "reading"), fm["sentence"]
    # Free-text field where Ray leaves per-card notes for the next AI pass
    # ("I already know this word", "use a shorter sentence", "wrong reading").
    # Surfaced on every entry so Claude reads it BEFORE curating that card.
    aif = fm.get("ai_instructions", "ai_instructions")
    main, deferred = deck_main(cfg), deck_deferred(cfg)
    deck_clause = f'(deck:"{main}" OR deck:"{deferred}")'

    note_ids = []
    if args.note_ids:
        note_ids = [int(x) for x in args.note_ids.split(",") if x.strip()]
    elif args.flag is not None:
        note_ids = anki_request("findNotes", query=f"flag:{args.flag} {deck_clause}")
    elif args.words:
        for w in [x.strip() for x in args.words.split(",") if x.strip()]:
            hits = anki_request("findNotes", query=f'"{wf}:{w}" {deck_clause}')
            if hits:
                note_ids.append(hits[0])
            else:
                print(f"  ✗ {w} — no existing card in mining decks "
                      f"(new word? use find_sentences.py)", file=sys.stderr)
    if not note_ids:
        sys.exit("No target notes. Pass --flag N, --note-ids, or --words.")

    info = anki_request("notesInfo", notes=note_ids)
    notes = []
    for n in info:
        f = n["fields"]
        notes.append({
            "note_id": n["noteId"],
            "word": f.get(wf, {}).get("value", ""),
            "reading": analyze.strip_html(f.get(rf, {}).get("value", "")),
            "old_sentence": analyze.strip_html(f.get(sf, {}).get("value", "")),
            "ai_instructions": analyze.strip_html(f.get(aif, {}).get("value", "")).strip(),
            "old_fields_snapshot": {k: v.get("value", "") for k, v in f.items()},
        })
    return notes


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--flag", type=int, help="Operate on every card flagged N in mining decks")
    g.add_argument("--note-ids", help="Comma-separated Anki note ids")
    g.add_argument("--words", help="Comma-separated words (resolve their existing card)")
    ap.add_argument("--output", required=True, help="Write replace-draft JSON here")
    ap.add_argument("--refresh-known", action="store_true",
                    help="Rescan the known-word set instead of using the cache")
    ap.add_argument("--top", type=int, default=3, help="Runner-ups to keep per word")
    ap.add_argument("--force-ignored-flag", action="store_true",
                    help="Proceed even when --flag N names a flag config.flags marks "
                         "`ignore` (cards that are a record, not a mining queue).")
    args = ap.parse_args()

    cfg = load_config()
    refuse_ignored_flag(cfg, args.flag, args.force_ignored_flag, "--flag")
    load_skill_env()
    notes = resolve_notes(args, cfg)
    print(f"Resolved {len(notes)} target notes", file=sys.stderr)

    sources = _sources.Sources.load(cfg, refresh_known=args.refresh_known)

    out, misses = [], []
    for i, note in enumerate(notes):
        if i:
            time.sleep(_sources.REQUEST_DELAY)  # space requests so apiv2 doesn't 429
        word = note["word"]
        # Loud on stderr: a card carrying instructions must not be auto-curated like the
        # others — Claude has to read and honor these first (SKILL.md §CURATE).
        if note.get("ai_instructions"):
            print(f"  ⚠ {word} — ai_instructions: {note['ai_instructions']}", file=sys.stderr)

        picks = _sources.best_for_word(word, sources,
                                       exclude_sentence=note["old_sentence"], top=args.top)
        if not picks:
            # Say which spellings were actually searched. A miss on a word field that
            # carries a copula used to be a dead end; naming the ladder turns it into a
            # one-line manual probe (the kana→kanji jump — おかど違い → お門違い — is the
            # class the tokenizer can't reach on its own).
            forms = _sources.query_forms(word)
            # Carry the note_id so replace_apply can retire the card (no usable
            # replacement in any corpus → tag not-worth-learning + suspend).
            misses.append({"word": word, "note_id": note["note_id"],
                           "forms_tried": forms,
                           "ai_instructions": note.get("ai_instructions", "")})
            print(f"  ✗ {word} — no usable replacement in any tier "
                  f"— tried {', '.join(forms)}", file=sys.stderr)
            continue

        best = picks[0]
        flag = "·bare" if best["bare_token"] else "·partial"
        src = "" if best["source"] == "immersionkit" else f" «{best['source']}»"
        print(f"  ✓ {word} [{best['i_level']}{flag}]{src} {best['new_sentence'][:48]}",
              file=sys.stderr)
        entry = dict(note)
        entry.update({k: best[k] for k in (
            "new_sentence", "sentence_with_furigana", "translation", "image_url",
            "sound_url", "title", "ik_id", "source", "i_level", "extra_unknowns",
            "bare_token", "query_form")})
        # The hit came from a DIFFERENT spelling than the card carries (おかど違いだ found
        # via おかど違い). That's a decision for Claude/Ray — the word field probably wants
        # renaming — so surface it rather than leaving it to be noticed.
        entry["word_form_differs"] = best.get("query_form", word) != word
        if entry["word_form_differs"]:
            print(f"      ↳ matched on «{best['query_form']}» — the card's word field is "
                  f"«{word}»; consider renaming it", file=sys.stderr)
        entry["explanation"] = ""        # Claude fills this inline (SKILL.md §EXPLAIN)
        entry["runner_ups"] = picks[1:]  # kept for "try a different sentence"
        out.append(entry)

    payload = {"source": "replace", "misses": misses, "entries": out}
    os.makedirs(os.path.dirname(os.path.expanduser(args.output)) or ".", exist_ok=True)
    with open(os.path.expanduser(args.output), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\nWrote {len(out)} proposals ({len(misses)} misses) to {args.output}",
          file=sys.stderr)
    if misses:
        print(f"  misses: {', '.join(m['word'] for m in misses)}", file=sys.stderr)


if __name__ == "__main__":
    main()
