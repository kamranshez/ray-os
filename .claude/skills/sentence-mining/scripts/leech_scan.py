#!/usr/bin/env python3
"""leech_scan.py — leech mode, step 1 (SOURCE + diagnosis).

Anki tags a card `leech` at `leechFails` lapses and NEVER removes it, so `tag:leech`
answers "did this card give me trouble at some point", not "is this card a problem
now". On Ray's collection in July 2026 that gap was the whole story: 78 tagged cards,
43 of which had since recovered to intervals of 21-338 days. Running the replace-mode
rehabilitation over all of them would have called forgetCards on cards carrying most
of a year of scheduling.

So this script splits the tag two ways on CURRENT interval:

  struggling  interval < config.leech.struggling_interval (default 21d) — work on these
  recovered   interval >= that — the tag is a scar, not a diagnosis. Strip it and leave
              the scheduling completely alone. Anki re-tags on further lapses, so the
              tag goes back to being a live signal instead of a permanent mark.

For every struggling card it emits `defects[]` — what's off about the card — and then
pulls a fresh sentence through the SAME cascade replace mode uses (`_sources.py`).
The defects drive the REPORT and the twin branch; they do not gate the swap. Ray's
call, July 2026: 21 of the 35 struggling cards had a perfectly good sentence and were
still failing, and re-running the scheduler over unchanged material just fails again.
The old sentence is archived to `previous_versions` by the apply step, so a swap costs
nothing that isn't recoverable.

RARE WORDS ARE NOT RE-MINED. A struggling leech whose JPDB lemma rank is worse than
`config.leech.rare_rank_cutoff` (20,000) is deferred instead of being given a new
sentence — checked BEFORE the cascade, so a rare word costs no API call either. Fighting
a word that barely appears is the expensive kind of failure: 穏当 sits at rank 39,096 and
had cost 19 lapses across 87 reps by the time this mode first ran. Deferred, never
deleted — rare means "later", not "not worth learning".

Two defects do NOT lead to a swap:

  interference_twin   a second card in the collection tests the same word. A new
                      sentence cannot fix two cards competing with each other, so the
                      pair is emitted as a merge PROPOSAL (healthier card survives,
                      weaker one goes through the apply step's delete gate).
  word_not_in_sentence / word_only_in_compound  are swapped like anything else, but
                      they're called out because they mean the card has been actively
                      mis-teaching. 穏当 (19 lapses, 87 reps) carried the sentence
                      不穏当な発言は慎んだ方がよろしいかと — the target appears only inside
                      the word that means its OPPOSITE.

Modes:
  --summary   launch check. Cheap: one cardsInfo over tag:leech, no known-word scan.
  (default)   full diagnosis + cascade → leech-draft JSON for Claude to fill
              explanations into, then leech_apply.py.
"""
import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _sources                     # noqa: E402 — THE sentence engine (shared)
from _anki import anki_request      # noqa: E402
from _config import (  # noqa: E402
    load_config, deck_main, deck_deferred, leech_interval, leech_rare_cutoff,
)
from _env import load_skill_env     # noqa: E402
from _style import leads_with_word, norm_word  # noqa: E402
from analyze import (               # noqa: E402 — the same known-word diff everything uses
    KNOWN_INTERVAL_THRESHOLD,
    extract_kanji_stem,
    get_known_intervals,
    load_jpdb_priority,
    is_card_worthy,
    is_content_word,
    is_proper_noun,
    load_mature_kanji_stems,
    strip_html,
    strip_speaker_labels,
    tokenize,
)
from audiobook_scan import word_in_sentence  # noqa: E402 — one clipping check, not two

LEECH_TAG = "leech"
SHORT_SENTENCE = 15  # below this a sentence is a fragment, not a context


def deck_clause(cfg):
    return f'(deck:"{deck_main(cfg)}" OR deck:"{deck_deferred(cfg)}")'


def in_scope_query(cfg):
    """Leeches this skill owns: its note type, inside its own decks. A leech sitting in
    an unrelated deck is someone else's problem and must not be swept into a run."""
    return f'note:"{cfg["note_type"]}" tag:{LEECH_TAG} {deck_clause(cfg)}'


def split_by_health(cfg, max_interval):
    """Return (struggling, recovered, out_of_scope_count) as lists of cardsInfo dicts.

    Health is the card's CURRENT interval, not its lapse count: a card with 10 lapses
    and a 338-day interval has recovered, whatever its history says."""
    cards = anki_request("findCards", query=in_scope_query(cfg))
    info = anki_request("cardsInfo", cards=cards) if cards else []
    all_tagged = anki_request("findCards", query=f"tag:{LEECH_TAG}")
    out_of_scope = len(all_tagged) - len(cards)
    struggling = [c for c in info if c.get("interval", 0) < max_interval]
    recovered = [c for c in info if c.get("interval", 0) >= max_interval]
    return struggling, recovered, out_of_scope


def find_twins(cfg, bare_word, self_note_id):
    """Other notes in the mining decks whose word field normalizes to the same word.

    Anki's dupe suffix means the pair is spelled differently in the field — 主張 and
    「主張 (2)」 — so a prefix search plus a normalized compare is what actually finds
    them. Returns [] for the overwhelmingly common single-card case."""
    wf = cfg["field_map"]["word"]
    try:
        ids = anki_request("findNotes", query=f'"{wf}:{bare_word}*" {deck_clause(cfg)}')
    except Exception:  # noqa: BLE001 — a word with query-hostile characters isn't fatal
        return []
    ids = [i for i in ids if i != self_note_id]
    if not ids:
        return []
    out = []
    for n in anki_request("notesInfo", notes=ids):
        val = n["fields"].get(wf, {}).get("value", "")
        if norm_word(strip_html(val)) != bare_word:
            continue  # 主張する matched the prefix but isn't the same card's word
        cards = anki_request("cardsInfo", cards=n["cards"]) if n.get("cards") else []
        best = max(cards, key=lambda c: c.get("interval", 0), default={})
        out.append({
            "note_id": n["noteId"],
            "word": strip_html(val),
            "sentence": strip_html(n["fields"].get(cfg["field_map"]["sentence"], {})
                                   .get("value", "")),
            "interval": best.get("interval", 0),
            "lapses": best.get("lapses", 0),
            "reps": best.get("reps", 0),
        })
    return out


def survivor_of(a, b):
    """Which of two competing cards should live. Higher current interval wins — it's the
    card that's actually working — then fewer lapses, then the sentence closest to the
    cascade's own sweet spot. Returned as (winner, loser, reason) so the apply step can
    print the reasoning and Ray can flip it."""
    def key(c):
        length_penalty = abs(_sources.jp_len(c.get("sentence", "")) - _sources.LEN_SWEET)
        return (c.get("interval", 0), -c.get("lapses", 0), -length_penalty)

    win, lose = (a, b) if key(a) >= key(b) else (b, a)
    return win, lose, (f"interval {win['interval']}d vs {lose['interval']}d, "
                       f"lapses {win['lapses']} vs {lose['lapses']}")


def diagnose(note, card, cfg, known, twins):
    """defects[] for one struggling leech. Descriptive only — see the module docstring
    for why the swap is unconditional."""
    fm = cfg["field_map"]
    intervals, norm_intervals, mature_stems, threshold = known
    # RAW vs stripped matters. `picture` holds an <img> tag and `sentence_audio` holds a
    # [sound:…] ref — running strip_html over the picture field reduces a perfectly good
    # <img src="…"> to "", so every card with an image reported `picture_blank`. That's
    # exactly what happened on the first run: all 35 struggling cards were reported blank
    # and none of them was. audiobook_scan.scan_note() reads raw for the same reason.
    raw = lambda k: note["fields"].get(fm.get(k, ""), {}).get("value", "")  # noqa: E731
    g = lambda k: strip_html(raw(k))                                        # noqa: E731

    word = norm_word(g("word"))
    sentence = g("sentence")
    defects = []

    if not word_in_sentence(word, sentence):
        defects.append("word_not_in_sentence")
    elif _sources.looks_misleading(sentence, word):
        # Every occurrence is glued into a compound / reads as a name / is a blocklisted
        # idiom. This is the 穏当 → 不穏当 case: the card teaches the wrong word.
        defects.append("word_only_in_compound")
    if _sources.jp_len(sentence) < SHORT_SENTENCE:
        defects.append("sentence_short")
    if not raw("picture").strip():
        # Blank picture makes the Back template re-render sentence_audio, so the card
        # autoplays its audio on BOTH sides on mobile.
        defects.append("picture_blank")
    if not g("explanation").strip():
        defects.append("explanation_missing")
    elif not leads_with_word(g("explanation"), word):
        defects.append("explanation_not_house_style")
    if not raw("sentence_audio").strip():
        defects.append("sentence_audio_missing")
    if twins:
        defects.append(f"interference_twin(x{len(twins) + 1})")

    def is_known(lemma, normalized):
        if intervals.get(lemma, 0) >= threshold:
            return True
        if normalized and norm_intervals.get(normalized, 0) >= threshold:
            return True
        stem = extract_kanji_stem(lemma)
        return bool(stem) and stem in mature_stems

    seen, extras = set(), []
    for surface, lemma, normalized, _reading, pos in tokenize(strip_speaker_labels(sentence)):
        if not is_content_word(pos) or not is_card_worthy(lemma) or lemma in seen:
            continue
        if is_proper_noun(pos) or is_known(lemma, normalized):
            continue
        seen.add(lemma)
        if lemma not in word and surface not in word:
            extras.append(surface)
    if extras:
        defects.append(f"above_i+1({len(extras)}:{'、'.join(extras[:4])})")

    # The lemma has matured on some OTHER card while this one keeps failing. Not a
    # verdict on worth — the same "sequencing, never worth" rule the rest of the skill
    # follows — but it's the strongest hint that the card itself is what's broken.
    if any(is_content_word(pos)
           and (intervals.get(lemma, 0) >= threshold
                or (normalized and norm_intervals.get(normalized, 0) >= threshold))
           for _s, lemma, normalized, _r, pos in tokenize(word)):
        defects.append("target_already_known")

    return word, sentence, defects


def summary(cfg, max_interval):
    struggling, recovered, out_of_scope = split_by_health(cfg, max_interval)
    print(json.dumps({
        "total": len(struggling) + len(recovered),
        "struggling": len(struggling),
        "recovered": len(recovered),
        "threshold_days": max_interval,
        "out_of_scope": out_of_scope,
        "query": in_scope_query(cfg),
    }, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", action="store_true",
                    help="Launch check: counts only, no known-word scan, no cascade")
    ap.add_argument("--max-interval", type=int, default=None,
                    help="Struggling/recovered cut in days (default config.leech."
                         "struggling_interval, else the known-word threshold)")
    ap.add_argument("--out", help="Write the leech-draft JSON here")
    ap.add_argument("--limit", type=int, help="Only scan the N worst (lowest interval) cards")
    ap.add_argument("--no-search", action="store_true",
                    help="Diagnose only — skip the cascade (no API calls, no proposals)")
    ap.add_argument("--top", type=int, default=3, help="Runner-ups to keep per word")
    ap.add_argument("--refresh-known", action="store_true",
                    help="Rescan the known-word set instead of using the cache")
    args = ap.parse_args()

    cfg = load_config()
    max_interval = args.max_interval or leech_interval(cfg)

    if args.summary:
        summary(cfg, max_interval)
        return

    load_skill_env()
    struggling, recovered, out_of_scope = split_by_health(cfg, max_interval)
    if out_of_scope:
        print(f"({out_of_scope} card(s) tagged {LEECH_TAG} outside this skill's note type "
              f"/ decks — left alone)", file=sys.stderr)
    struggling.sort(key=lambda c: (c.get("interval", 0), -c.get("lapses", 0)))
    if args.limit:
        struggling = struggling[:args.limit]

    rec_notes = sorted({c["note"] for c in recovered})
    rec_out = []
    if rec_notes:
        best = {}
        for c in recovered:
            cur = best.get(c["note"])
            if not cur or c.get("interval", 0) > cur.get("interval", 0):
                best[c["note"]] = c
        fm = cfg["field_map"]
        for n in anki_request("notesInfo", notes=rec_notes):
            c = best[n["noteId"]]
            rec_out.append({
                "note_id": n["noteId"],
                "word": strip_html(n["fields"].get(fm["word"], {}).get("value", "")),
                "interval": c.get("interval", 0),
                "lapses": c.get("lapses", 0),
            })
        rec_out.sort(key=lambda r: -r["interval"])

    print(f"{len(struggling)} struggling (interval < {max_interval}d), "
          f"{len(rec_out)} recovered (tag will be stripped)", file=sys.stderr)
    if not struggling:
        entries, twins, misses, skipped = [], [], [], []
    else:
        notes = {n["noteId"]: n
                 for n in anki_request("notesInfo", notes=sorted({c["note"] for c in struggling}))}
        intervals, norm_intervals = get_known_intervals(cfg, force_refresh=args.refresh_known)
        known = (intervals, norm_intervals, load_mature_kanji_stems(intervals),
                 cfg["known_words"].get("interval_threshold", KNOWN_INTERVAL_THRESHOLD))

        sources = None
        if not args.no_search:
            sources = _sources.Sources.load(cfg, refresh_known=False)

        fm = cfg["field_map"]
        rare_cutoff = leech_rare_cutoff(cfg)
        priority = load_jpdb_priority(cfg.get("jpdb_priority_csv")) if rare_cutoff else {}
        if rare_cutoff and not priority:
            print("  ⚠ rare_rank_cutoff is set but no JPDB priority list loaded — "
                  "the rare-word skip is OFF for this run", file=sys.stderr)
        entries, twins, misses, skipped, searched = [], [], [], [], 0
        for card in struggling:
            note = notes.get(card["note"])
            if not note:
                continue
            twin_cards = find_twins(cfg, norm_word(strip_html(
                note["fields"].get(fm["word"], {}).get("value", ""))), note["noteId"])
            word, sentence, defects = diagnose(note, card, cfg, known, twin_cards)
            base = {
                "note_id": note["noteId"],
                "word": word,
                "reading": strip_html(note["fields"].get(fm.get("reading", ""), {})
                                      .get("value", "")),
                "old_sentence": sentence,
                "old_fields_snapshot": {k: v.get("value", "")
                                        for k, v in note["fields"].items()},
                "ai_instructions": strip_html(
                    note["fields"].get(fm.get("ai_instructions", ""), {}).get("value", "")).strip(),
                "lapses": card.get("lapses", 0),
                "interval": card.get("interval", 0),
                "reps": card.get("reps", 0),
                "defects": defects,
            }
            if base["ai_instructions"]:
                print(f"  ⚠ {word} — ai_instructions: {base['ai_instructions']}", file=sys.stderr)

            if twin_cards:
                # No swap. A fresh sentence can't fix two cards competing for the same
                # word — emit the pair for the merge gate instead.
                mine = {"note_id": note["noteId"], "word": word, "sentence": sentence,
                        "interval": card.get("interval", 0), "lapses": card.get("lapses", 0),
                        "reps": card.get("reps", 0)}
                win, lose, why = survivor_of(mine, twin_cards[0])
                twins.append({"word": word, "cards": [mine] + twin_cards,
                              "proposed_survivor": win["note_id"],
                              "proposed_delete": lose["note_id"],
                              "reason": why, "defects": defects})
                print(f"  ⇄ {word} — interference twin; proposing to keep "
                      f"nid:{win['note_id']} ({why})", file=sys.stderr)
                continue

            # Rare words are deferred, not re-mined. Fighting a word that barely appears
            # is the expensive kind of failure: 穏当 sits at JPDB rank 39,096 and had cost
            # 19 lapses across 87 reps by the time leech mode first ran. Skipping happens
            # BEFORE the cascade, so a rare word costs no API call either.
            rank = priority.get(word, 10 ** 9)
            base["jpdb_rank"] = None if rank >= 10 ** 9 else rank
            if rare_cutoff and rank > rare_cutoff:
                base["disposition"] = "defer_rare"
                base["skip_reason"] = (f"JPDB rank {base['jpdb_rank'] or 'absent'} > "
                                       f"{rare_cutoff}")
                skipped.append(base)
                print(f"  ⤵ {word} — rare ({base['skip_reason']}); deferring, no swap",
                      file=sys.stderr)
                continue

            if args.no_search:
                entries.append(base)
                continue

            if searched:
                time.sleep(_sources.REQUEST_DELAY)  # space IK requests — apiv2 429s
            searched += 1
            picks = _sources.best_for_word(word, sources,
                                           exclude_sentence=sentence, top=args.top)
            if not picks:
                base["forms_tried"] = _sources.query_forms(word)
                misses.append(base)
                print(f"  ✗ {word} — no usable replacement in any tier "
                      f"— tried {', '.join(base['forms_tried'])}", file=sys.stderr)
                continue
            best_pick = picks[0]
            entry = dict(base)
            entry.update({k: best_pick[k] for k in (
                "new_sentence", "sentence_with_furigana", "translation", "image_url",
                "sound_url", "title", "ik_id", "source", "i_level", "extra_unknowns",
                "bare_token", "query_form")})
            entry["word_form_differs"] = best_pick.get("query_form", word) != word
            entry["explanation"] = ""     # <- Claude fills this in, in house style
            entry["runner_ups"] = picks[1:]
            entries.append(entry)
            src = "" if best_pick["source"] == "immersionkit" else f" «{best_pick['source']}»"
            print(f"  ✓ {word} [{best_pick['i_level']}]{src} "
                  f"{best_pick['new_sentence'][:44]}", file=sys.stderr)

    out = Path(args.out).expanduser() if args.out else Path(cfg["work_dir"]) / "leech.draft.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "source": "leech",
        "threshold_days": max_interval,
        "decks": {"main": deck_main(cfg), "deferred": deck_deferred(cfg)},
        "recovered": rec_out,
        "entries": entries,
        "skipped": skipped,
        "twins": twins,
        "misses": misses,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    defect_counts = Counter()
    for e in entries + misses + twins + skipped:
        for d in e.get("defects", []):
            defect_counts[re.sub(r"\(.*", "", d)] += 1
    print(f"\nScanned {len(struggling)} struggling leech(es)")
    print(f"  defects: {dict(defect_counts.most_common())}")
    print(f"  proposals: {len(entries)}   skipped: {len(skipped)}   "
          f"twins: {len(twins)}   misses: {len(misses)}")
    print(f"  recovered (de-tag only): {len(rec_out)}")
    print(f"\nDraft: {out}")
    print("\nNext: Claude fills each entry's `explanation` (house style — LEAD WITH THE "
          "WORD), then leech_apply.py --dry-run for the gate.")


if __name__ == "__main__":
    main()
