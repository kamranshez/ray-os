#!/usr/bin/env python3
"""Bank mode, SOURCE stage — turn a WORD LIST into new-card candidates.

    "I keep forgetting 同期, give me a card."

For each word: skip it if a card already exists or the word is already known, then ask
the shared sentence engine (`_sources.best_for_word` — Immersion Kit → Nadeshiko →
sentencesearch → kotu → local bank, re-ranked by this collection's i+1) for the best
example sentence, and stage it as a new-card candidate.

This REPLACES the old `search_banks.py --words` entry point, which searched only the
local .apkg banks (the cascade's LAST tier) with its own scoring table and no
known-word check — so the same word produced a measurably worse card here than replace
mode produced for it. `search_banks.py` still exists and still does the within-bank
ranking, but it is now reached only as tier 5 *of the cascade*, never as the whole
search. See SKILL.md §Sourcing.

Output — a candidates JSON that Claude curates + explains, then generate_media_bank.py
and push.py consume unchanged:

    {"source": "bank-search",
     "candidates": [{lemma, reading, sentence, deck, i_level, explanation: "",
                     sound_url, image_url, translation, title, source,
                     extra_unknowns, bare_token, runner_ups}],
     "misses":  [{word, reason}]}
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze
import _sources
from _config import load_config, deck_main, deck_deferred
from _anki import anki_request
from _env import load_skill_env


def read_words(args):
    """Words come from --words (comma-separated) or --words-file (one per line, extra
    columns ignored — pasting a leech export straight in should just work)."""
    raw = []
    if args.words:
        raw = [w.strip() for w in args.words.split(",")]
    elif args.words_file:
        for line in open(os.path.expanduser(args.words_file), encoding="utf-8"):
            first = line.strip().split("\t")[0].split(",")[0].strip()
            if first:
                raw.append(first)
    seen, out = set(), []
    for w in raw:  # dedupe, preserve order
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def reading_for(word):
    """SudachiPy's reading for the word in isolation (katakana). push.py mirrors the
    word itself for all-katakana loanwords, so a blank here is survivable — but a real
    reading is better, and we already have the tokenizer loaded."""
    try:
        toks = analyze.tokenize(word)
        if len(toks) == 1:
            return toks[0][3] or ""
        return "".join(t[3] or "" for t in toks)
    except Exception:  # noqa: BLE001
        return ""


def already_known(word, known):
    """True only on an EXACT lemma / normalized-form match at or above the maturity
    threshold. Deliberately does NOT use analyze's mature-kanji-stem heuristic: that
    heuristic exists to skip possible unknowns *inside* a sentence, where a false
    'known' merely costs a candidate. Here a false 'known' would refuse to build a card
    the user explicitly asked for — 突っ伏す shares the stem 突 with 突然, so one matured
    kanji would bin the whole word. Same rule audiobook_scan.py follows.

    NOTE this is only a WARNING by default, not a veto (see main). Ray typed the word on
    purpose: "the known-word diff is a hint about sequencing, never a verdict on worth."
    """
    intervals, norm_intervals, _stems, threshold = known
    if intervals.get(word, 0) >= threshold:
        return True
    try:
        toks = analyze.tokenize(word)
        if len(toks) == 1:
            _s, lemma, normalized, _r, _p = toks[0]
            if intervals.get(lemma, 0) >= threshold:
                return True
            if normalized and norm_intervals.get(normalized, 0) >= threshold:
                return True
    except Exception:  # noqa: BLE001
        pass
    return False


def existing_card(word, cfg):
    """The word already has a card in the mining decks → nothing to mine. (push.py sets
    allowDuplicate: False so it would be rejected at the end anyway; catching it here
    means we don't burn a cascade lookup and a TTS call on it first.)"""
    fm, main, deferred = cfg["field_map"], deck_main(cfg), deck_deferred(cfg)
    q = f'"{fm["word"]}:{word}" (deck:"{main}" OR deck:"{deferred}")'
    try:
        return bool(anki_request("findNotes", query=q))
    except Exception:  # noqa: BLE001
        return False


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--words", help="Comma-separated target words")
    g.add_argument("--words-file", help="File with one word per line (first column)")
    ap.add_argument("--output", required=True, help="Write the candidates JSON here")
    ap.add_argument("--top", type=int, default=3, help="Runner-ups to keep per word")
    ap.add_argument("--refresh-known", action="store_true",
                    help="Rescan the known-word set instead of using the cache")
    ap.add_argument("--skip-known", action="store_true",
                    help="Refuse to build a card for a word already at/above the maturity "
                         "threshold. Default is to BUILD it and just warn: Ray typed the "
                         "word on purpose, and the known-word diff is a hint about "
                         "sequencing, not a verdict on worth (and it is wrong sometimes).")
    ap.add_argument("--defer-above-i1", action="store_true", default=True,
                    help="Route i2+ candidates to the deferred deck (default)")
    args = ap.parse_args()

    cfg = load_config()
    load_skill_env()
    words = read_words(args)
    if not words:
        sys.exit("No words given.")
    print(f"{len(words)} word(s) requested", file=sys.stderr)

    sources = _sources.Sources.load(cfg, refresh_known=args.refresh_known)
    main_deck, deferred_deck = deck_main(cfg), deck_deferred(cfg)

    candidates, misses = [], []
    searched = 0
    for word in words:
        # Cheap rejections first — no point hitting five corpora for a word we won't card.
        if existing_card(word, cfg):
            misses.append({"word": word, "reason": "already has a card"})
            print(f"  · {word} — already has a card", file=sys.stderr)
            continue
        # The known-word diff gets a VOICE here, not a veto. Ray typed this word on
        # purpose; refusing to build it because the diff thinks he knows it is the exact
        # failure mode he called out in July 2026 ("everything is worth learning at some
        # point"). So warn loudly, build the card anyway, and let --skip-known opt out.
        known_word = already_known(word, sources.known)
        if known_word:
            if args.skip_known:
                misses.append({"word": word, "reason": "already known (--skip-known)"})
                print(f"  · {word} — skipped, already known", file=sys.stderr)
                continue
            print(f"  ⚠ {word} — the diff says you already know this "
                  f"(building it anyway; --skip-known to refuse)", file=sys.stderr)

        if searched:
            time.sleep(_sources.REQUEST_DELAY)  # space requests so IK apiv2 doesn't 429
        searched += 1
        picks = _sources.best_for_word(word, sources, top=args.top)
        if not picks:
            misses.append({"word": word, "reason": "no usable sentence in any tier"})
            print(f"  ✗ {word} — no usable sentence in any tier", file=sys.stderr)
            continue

        best = picks[0]
        # i+1 is the clean case (the target is the only unknown). Anything denser goes to
        # the deferred deck rather than sitting next to good cards in the main one — same
        # routing rule video mode uses. See SKILL.md §ROUTE.
        deck = main_deck if best["i_level"] == "i1" else deferred_deck
        if not args.defer_above_i1:
            deck = main_deck

        src = "" if best["source"] == "immersionkit" else f" «{best['source']}»"
        media = ("🔊🖼" if best["image_url"] else "🔊")
        print(f"  ✓ {word} [{best['i_level']}]{src} {media} {best['new_sentence'][:44]}",
              file=sys.stderr)

        candidates.append({
            "lemma": word,
            "reading": reading_for(word),
            "sentence": best["new_sentence"],
            "sentence_with_furigana": best["sentence_with_furigana"],
            "translation": best["translation"],
            "sound_url": best["sound_url"],     # URL (IK/Nadeshiko/web) or local path (bank)
            "image_url": best["image_url"],     # may be "" — audio-only tiers ship no image
            "title": best["title"],
            "source": best["source"],
            "i_level": best["i_level"],
            "extra_unknowns": best["extra_unknowns"],
            "bare_token": best["bare_token"],
            "deck": deck,
            "already_known": known_word,        # surfaced to Claude; not a veto
            "explanation": "",                  # Claude fills this inline (SKILL.md §EXPLAIN)
            "runner_ups": picks[1:],
        })

    payload = {"source": "bank-search", "candidates": candidates, "misses": misses}
    os.makedirs(os.path.dirname(os.path.expanduser(args.output)) or ".", exist_ok=True)
    with open(os.path.expanduser(args.output), "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    n_main = sum(1 for c in candidates if c["deck"] == main_deck)
    print(f"\nWrote {len(candidates)} candidate(s) — {n_main} i+1 → main, "
          f"{len(candidates) - n_main} → deferred; {len(misses)} miss(es) → {args.output}",
          file=sys.stderr)
    for m in misses:
        print(f"  miss: {m['word']} ({m['reason']})", file=sys.stderr)


if __name__ == "__main__":
    main()
