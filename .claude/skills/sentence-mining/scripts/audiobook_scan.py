#!/usr/bin/env python3
"""audiobook_scan.py — audiobook mode, step 1.

Cards mined with the external audiobook-viewer arrive in Anki already carrying a
sentence and its audiobook audio, but they are NOT house standard: the explanation
opens cold on the definition instead of naming the word, there's no explanation TTS,
the picture field is blank, and the tool leaves its own fields (definition,
pitch_accent, frequency_*) behind. Worse, nothing checks them against Ray's known
words, so a word he learned years ago (僕) and a sentence far above i+1 (天真爛漫)
land in the main deck next to genuinely useful cards.

This script does the *diagnosis*. Two jobs:

  --groups   Discovery. Buckets audiobook cards by book and reports how many in each
             still need work. Claude uses this to QUIZ Ray on which batch to run —
             the mode never guesses which book he meant.

  --query Q  Scan. For every card matching Q, emit an audiobook-draft JSON with:

               defects[]  what's off-standard (drives the fixes in audiobook_apply)
               route      main | rescue | deferred   (the auto-routing decision)
               i_level    unknowns in the sentence, counting the target word itself

Routing reuses analyze.py's known-word diff verbatim, so "known" means what it means
everywhere else in the skill: some card carrying that lemma has an interval >=
config.known_words.interval_threshold.

There is deliberately NO `retire` route here. The diff decides SEQUENCING (see it later),
never WORTH — Ray mined these words on purpose while reading, so an already-known lemma
goes to `deferred`, not to a suspend. The diff is also wrong sometimes (it wanted to bin
突っ伏す because 突 appears in 突然): a needless deferral is one click to undo, a needless
suspend is a word he chose vanishing silently.

  main     -> clean i+1: the target is the only thing Ray doesn't know.
  rescue   -> the sentence has unknowns BEYOND the target, so it's above i+1. Send the word
              back through the cascade for an easier sentence; keep the card either way.
  deferred -> above i+1 with no easier sentence anywhere, or the lemma already matured on
              another card. Later, not never.

This script deliberately decides nothing about the explanation TEXT. Claude writes those
inline in house style, because that needs Japanese fluency a script doesn't have.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _config import load_config, deck_main, deck_deferred  # noqa: E402
from _anki import anki_request  # noqa: E402
from analyze import (  # noqa: E402  — the SAME known-word diff video mode uses
    KNOWN_INTERVAL_THRESHOLD,
    extract_kanji_stem,
    get_known_intervals,
    is_card_worthy,
    is_content_word,
    is_proper_noun,
    kata_to_hira,
    load_mature_kanji_stems,
    strip_furigana,
    strip_html,
    strip_speaker_labels,
    tokenize,
)

AUDIOBOOK_TAG = "audiobook"  # set by Ray's audiobook-viewer, not by us
# Tags that say nothing about which book a card came from, so they'd be noise as groups.
BORING_TAGS = {AUDIOBOOK_TAG, "claude-sentence-mining", "claude-sentence-bank",
               "leech", "marked", *(f"i{n}" for n in range(1, 10)), "i?"}

# There is deliberately NO "this card is done" tag. A card is done when its FIELDS say so —
# house-style explanation, explanation audio, non-blank picture, no leftover foreign fields —
# which is exactly what scan_note() already computes. A processed-marker tag would be a second
# source of truth that can drift from the first (and Ray's audiobook-viewer rewrites tags on
# re-sync, so it drifted immediately). Re-running the scan over already-finished cards is
# free: they come back with zero defects and apply skips them.


from _style import KANJI as _KANJI, leads_with_word, norm_word as _norm_word  # noqa: E402


def word_in_sentence(word: str, sentence: str) -> bool:
    """Is the card's word actually IN its own sentence? The audiobook tool sometimes clips
    the line so the mined word falls off (あれ, July 2026). An exact substring check alone
    is too strict — the sentence often carries an INFLECTED form (悔しい appears as
    悔しそうに) — so also accept the word minus its final kana (the inflection stem), and
    fall back to the word's kanji appearing in order (same tolerance as leads_with_word).
    This flags gross clipping for a human look; it doesn't need to be a perfect parser."""
    s = sentence.replace(" ", "").replace("　", "")
    if not word or word in s:
        return True
    if len(word) >= 3 and word[:-1] in s:
        return True
    kanji = _KANJI.findall(word)
    if not kanji:
        return False
    pos = -1
    for k in kanji:
        pos = s.find(k, pos + 1)
        if pos < 0:
            return False
    return True


def scan_note(note, fm, intervals, norm_intervals, mature_stems):
    f = note["fields"]
    get = lambda key: f.get(fm.get(key, ""), {}).get("value", "")  # noqa: E731

    word = _norm_word(get("word"))
    sentence = strip_html(get("sentence"))
    explanation = get("explanation")

    # ---- defects: how does this card differ from what the skill would have built? ----
    defects = []
    if not word_in_sentence(word, sentence):
        # The tool clipped the line and the card's word isn't in its own sentence
        # (あれ, July 2026: the leading interjection was cut off). Don't write an
        # explanation against a sentence that doesn't contain the word — send the
        # card through replace mode for a real sentence instead.
        defects.append("word_not_in_sentence")
    if not explanation.strip():
        defects.append("explanation_missing")
    elif not leads_with_word(explanation, word):
        defects.append("explanation_not_house_style")
    if not get("explanation_audio").strip():
        defects.append("explanation_audio_missing")
    if not get("picture").strip():
        # A blank picture makes the Back template re-render sentence_audio, so the card
        # autoplays its sentence audio on BOTH sides on AnkiMobile/AnkiDroid.
        defects.append("picture_blank")
    if not get("sentence_audio").strip():
        defects.append("sentence_audio_missing")

    # Fields the audiobook tool populated that this note type doesn't own.
    mapped = set(fm.values())
    foreign = sorted(k for k, v in f.items() if k not in mapped and v.get("value", "").strip())
    if foreign:
        defects.append("foreign_fields:" + ",".join(foreign))

    # ---- known-word diff (identical logic to analyze.py) ----
    def is_known(lemma, normalized):
        if intervals.get(lemma, 0) >= KNOWN_INTERVAL_THRESHOLD:
            return True
        if normalized and norm_intervals.get(normalized, 0) >= KNOWN_INTERVAL_THRESHOLD:
            return True
        stem = extract_kanji_stem(lemma)
        return bool(stem) and stem in mature_stems

    # Deliberately does NOT use the mature-kanji-stem heuristic that is_known() applies.
    # That heuristic is tuned for the opposite job — skipping possible unknowns inside a
    # sentence, where a false "known" only costs a missed candidate. Here a false "known"
    # RETIRES a card Ray actually wants, and it fires constantly: 突っ伏す shares the stem
    # 突 with 突然, so a single mature kanji would bin the whole word. Retiring is only
    # justified by an exact lemma (or spelling-variant) match on a matured card.
    target_known = any(
        is_content_word(pos)
        and (intervals.get(lemma, 0) >= KNOWN_INTERVAL_THRESHOLD
             or (normalized and norm_intervals.get(normalized, 0) >= KNOWN_INTERVAL_THRESHOLD))
        for _s, lemma, normalized, _r, pos in tokenize(word)
    )

    # Tokenize with any leading subtitle speaker label stripped — （幾島） is a name tag,
    # not vocabulary, and it was being charged against the sentence's i-level. The card
    # keeps the sentence verbatim; only the DIFF sees the stripped text.
    unknowns, seen = [], set()
    for surface, lemma, normalized, reading, pos in tokenize(strip_speaker_labels(sentence)):
        if not is_content_word(pos) or not is_card_worthy(lemma) or lemma in seen:
            continue
        if is_proper_noun(pos):
            continue  # a name is context, not a word to learn — don't charge it as load
        if is_known(lemma, normalized):
            continue
        seen.add(lemma)
        unknowns.append({"lemma": lemma, "surface": surface,
                         "reading_hira": kata_to_hira(reading)})

    # The target is itself an unknown — that's the point of the card. Anything ELSE
    # unknown in the sentence is extra load stacked on top of it.
    extras = [u for u in unknowns if u["lemma"] not in word and u["surface"] not in word]
    i_level = f"i{min(len(extras) + 1, 9)}"

    # NOTHING here retires or suspends a card. Ray mined these words minutes ago, on purpose,
    # while reading — a card he deliberately made is by definition worth learning, and the
    # skill has no business overruling that. The known-word diff is a hint about SEQUENCING
    # (learn it later), never a verdict on worth. Suspending on a diff result also hides the
    # card, so when the diff is wrong — and it is: it wanted to bin 突っ伏す because 突 appears
    # in 突然 — Ray would never see it to disagree. Worst case a card goes to deferred and he
    # pulls it back. Worst case of a suspend is a word he chose silently disappearing.
    if extras:
        # Above i+1. Don't exile it to `deferred` yet — the word is still worth learning,
        # it's the audiobook's SENTENCE that's too dense (novel prose usually is). Hand it
        # to replace mode, which pulls an easier sentence for the same word from Immersion
        # Kit / Nadeshiko / the corpora and re-ranks by this same i+1 diff. Deferring is the
        # fallback for when even those corpora have nothing simpler.
        route, why = "rescue", (f"{len(extras)} unknown beyond the target: "
                                + "、".join(u["surface"] for u in extras[:6]))
    elif target_known:
        route, why = "deferred", (f"lemma already matured elsewhere (≥ {KNOWN_INTERVAL_THRESHOLD}d)"
                                  " — sequence it later, don't drop it")
    else:
        route, why = "main", "clean i+1"

    return {
        "noteId": note["noteId"],
        "cards": note["cards"],
        "word": word,
        "reading": strip_html(get("reading")),
        "sentence": sentence,
        "explanation_old": strip_html(explanation),
        "tags": note["tags"],
        "defects": defects,
        "extras": extras,
        "i_level": i_level,
        "route": route,
        "route_reason": why,
        "ai_instructions": get("ai_instructions").strip(),
        "explanation": "",  # <- Claude fills this in, in house style
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", help="Anki query selecting the audiobook cards to fix")
    ap.add_argument("--groups", action="store_true",
                    help="Bucket audiobook cards by book and print JSON (for the quiz)")
    ap.add_argument("--out", help="Write the audiobook-draft JSON here")
    ap.add_argument("--refresh-known", action="store_true",
                    help="Rescan known words instead of using the cache")
    args = ap.parse_args()

    cfg = load_config()
    fm = cfg["field_map"]
    nt = cfg["note_type"]

    if args.groups:
        ids = anki_request("findNotes", query=f'note:"{nt}" tag:{AUDIOBOOK_TAG}')
        if not ids:
            print(json.dumps({"total": 0, "groups": []}, ensure_ascii=False, indent=2))
            return
        notes = anki_request("notesInfo", notes=ids)

        # "Needs work" is a cheap field check — no known-word scan, so the quiz is fast.
        def needs_work(n):
            g = lambda k: n["fields"].get(fm.get(k, ""), {}).get("value", "")  # noqa: E731
            mapped = set(fm.values())
            word = _norm_word(g("word"))
            return bool(
                not g("explanation_audio").strip()
                or not g("picture").strip()
                or not leads_with_word(g("explanation"), word)
                or not word_in_sentence(word, strip_html(g("sentence")))
                or any(k not in mapped and v.get("value", "").strip()
                       for k, v in n["fields"].items())
            )

        by_book = defaultdict(lambda: {"total": 0, "needs_work": 0})
        for n in notes:
            books = [t for t in n["tags"] if t not in BORING_TAGS] or ["(untagged)"]
            for b in books:
                by_book[b]["total"] += 1
                by_book[b]["needs_work"] += needs_work(n)

        groups = [
            {"book": b, "query": f'note:"{nt}" tag:{AUDIOBOOK_TAG} tag:{b}'
                                 if b != "(untagged)" else f'note:"{nt}" tag:{AUDIOBOOK_TAG}',
             "total": v["total"], "needs_work": v["needs_work"]}
            for b, v in sorted(by_book.items(), key=lambda kv: -kv[1]["needs_work"])
        ]
        print(json.dumps({
            "total": len(ids),
            "needs_work": sum(needs_work(n) for n in notes),
            "all_query": f'note:"{nt}" tag:{AUDIOBOOK_TAG}',
            "groups": groups,
        }, ensure_ascii=False, indent=2))
        return

    if not args.query:
        ap.error("--query is required (or --groups to discover which books are minable)")

    ids = anki_request("findNotes", query=args.query)
    if not ids:
        print(f"No notes match: {args.query}", file=sys.stderr)
        sys.exit(1)
    notes = anki_request("notesInfo", notes=ids)

    # get_known_intervals returns BOTH maps: lemma->interval and normalized->interval
    # (the latter makes the diff variant-aware, e.g. こもる counts as known when 籠る is).
    intervals, norm_intervals = get_known_intervals(cfg, force_refresh=args.refresh_known)
    mature_stems = load_mature_kanji_stems(intervals)

    entries = [scan_note(n, fm, intervals, norm_intervals, mature_stems) for n in notes]

    for e in entries:
        if e["ai_instructions"]:
            print(f"⚠ {e['word']} — ai_instructions: {e['ai_instructions']}", file=sys.stderr)

    out = Path(args.out) if args.out else Path(cfg["work_dir"]) / "audiobook.draft.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "source": "audiobook",
        "query": args.query,
        "decks": {"main": deck_main(cfg), "deferred": deck_deferred(cfg)},
        "entries": entries,
    }, ensure_ascii=False, indent=2))

    counts, clean = defaultdict(int), 0
    for e in entries:
        counts[e["route"]] += 1
        clean += not e["defects"]
    print(f"Scanned {len(entries)} audiobook card(s): {args.query}")
    print(f"  route  → main: {counts['main']}   rescue: {counts['rescue']}   "
          f"deferred: {counts['deferred']}")
    print(f"  {len(entries) - clean} need fixing, {clean} already house standard")
    print(f"\nDraft: {out}")
    if counts["rescue"]:
        ids = ",".join(str(e["noteId"]) for e in entries if e["route"] == "rescue")
        print(f"\nRescue ({counts['rescue']} above i+1) — get them an easier sentence first:")
        print(f"  python3 scripts/replace_search.py --note-ids {ids} --output <work>/rescue.json")
        print("  (then replace_apply.py; anything it MISSES falls back to the deferred deck)")
    print("\nThen: Claude fills each entry's `explanation` (house style) → audiobook_apply.py")


if __name__ == "__main__":
    main()
