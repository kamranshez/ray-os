#!/usr/bin/env python3
"""Tokenize, diff against AnkiMorphs DB, dedupe via AnkiConnect, rank by JPDB priority.

Input: AssemblyAI transcript JSON (from transcribe.py, post Step 2.5 splitting).
Output: candidate cards JSON per source.

Single-call mode lets multiple videos share one SudachiPy + AnkiConnect load.

Single-file (stdout):
    analyze.py --transcript T.json --source-id ID --source-url URL > cands.json

Manifest (multi-video, batched):
    analyze.py --manifest manifest.json --output-dir DIR
    # manifest.json is [{"transcript": "path", "source_id": "id", "source_url": "url"}, ...]
    # writes DIR/<source-id>.candidates.json per entry
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load_config, deck_main, deck_deferred

CAP = 50

# SudachiPy top-level POS categories (part_of_speech()[0]). na-adjectives are 名詞
# in Sudachi (no 形状詞 category — that's UniDic), so they're caught by 名詞.
CONTENT_POS_PREFIXES = ("名詞", "動詞", "形容詞", "副詞", "連体詞", "感動詞")
SKIP_POS_PREFIXES = ("助詞", "助動詞", "補助記号", "記号", "空白", "接尾辞", "接頭辞", "代名詞", "フィラー")

PURE_DIGITS = re.compile(r"^[0-9０-９]+$")
PURE_ASCII = re.compile(r"^[A-Za-z]+$")
PUNCT_ONLY = re.compile(r"^[!?！？。、,\.…\-—~〜]+$")
SINGLE_KANA = re.compile(r"^[぀-ゟ゠-ヿー]$")
KANA_ONLY_SHORT = re.compile(r"^[぀-ゟ゠-ヿー]{1,2}$")
HAS_KANJI = re.compile(r"[一-鿿]")
HAS_KANA = re.compile(r"[぀-ゟ゠-ヿ]")
KANJI_RE = re.compile(r"[一-鿿々]+")

HTML_TAG_RE = re.compile(r"<[^>]+>")
FURIGANA_RE = re.compile(r"([一-龯々]+)\[([ぁ-ゖァ-ヺー]+)\]")

# A leading Netflix-style speaker or sound label: （幾島）本日は… / ［幾島］本日は…
# Capped at 20 inner chars and allows no nested bracket, so a genuine parenthetical
# aside can't be mistaken for a label.
SPEAKER_LABEL_RE = re.compile(r"^[（(［\[][^）)］\]（(［\[]{0,20}[）)］\]]")

# Runtime config — populated by main() from config.json so the rest of the
# module reads plain module globals (no threading config through every call).
ANKICONNECT = "http://localhost:8765"
MAIN_DECK = ""
DEFERRED_DECK = ""
DEDUPE_DECKS_QUERY = ""
ANKI_NOTE_FIELD = "wordForm"
KNOWN_INTERVAL_THRESHOLD = 21


def strip_html(s):
    s = HTML_TAG_RE.sub("", s.replace("<br>", "\n").replace("<br/>", "\n"))
    return s.replace("　", " ").replace("\xa0", " ").strip()


def strip_furigana(s):
    # Anki furigana lives as `漢字[かんじ]`; drop the reading so the tokenizer sees clean text.
    return FURIGANA_RE.sub(r"\1", s)


def strip_speaker_labels(s):
    """Drop leading subtitle speaker/sound labels — `（幾島）本日は…` → `本日は…`.

    Netflix JP subtitles prefix lines with the speaker in full-width parens, and Ray
    mines Netflix. Left in, the label tokenizes as a real word and lands in the diff as
    a bogus extra unknown (幾島 counted against 伝統's sentence, July 2026).

    Feed this to the TOKENIZER only, never to the sentence written onto the card — the
    label is part of the source line and the card should keep it verbatim.
    """
    out = (s or "").lstrip()
    while True:
        m = SPEAKER_LABEL_RE.match(out)
        if not m:
            return out
        rest = out[m.end():].lstrip()
        if not rest:
            return out  # the whole line was bracketed — not a label, leave it alone
        out = rest


_sudachi_tokenizer = None
_sudachi_split = None


def _sudachi():
    """Lazily build a single SudachiPy tokenizer (SplitMode C) shared across calls."""
    global _sudachi_tokenizer, _sudachi_split
    if _sudachi_tokenizer is None:
        from sudachipy import dictionary, tokenizer
        _sudachi_tokenizer = dictionary.Dictionary(dict="core").create()
        _sudachi_split = tokenizer.Tokenizer.SplitMode.C  # longest units — best for vocab
    return _sudachi_tokenizer, _sudachi_split


def tokenize(text):
    """Tokenize with SudachiPy (SplitMode C — keeps meaningful compounds whole, e.g.
    警察官/被写体 as single words rather than 警察+官).

    Returns (surface, lemma, normalized, reading, pos) per token:
      lemma      = dictionary_form()   (走った→走る; keeps surface orthography, kana stays kana)
      normalized = normalized_form()   (collapses spelling variants: こもる/籠る→籠もる)
      reading    = reading_form()      (katakana)
      pos        = ",".join(part_of_speech())  — the FULL tag, e.g. 名詞,固有名詞,人名,一般,*,*

    `pos` used to be `part_of_speech()[0]` (the top-level category alone). It carries the
    whole tag now so callers can see the sub-categories — specifically 固有名詞, which is
    how the diff tells a proper noun (幾島, a subtitle speaker label) from vocabulary. The
    change is backward compatible by construction: every consumer tests `pos` with
    `startswith`, and the full tag begins with the top-level category, so
    `"名詞,固有名詞,人名".startswith("名詞")` still holds. The only places that need the
    bare category are the ones that WRITE pos into candidate JSON — they take
    `pos.split(",")[0]`, keeping references/transcript-schema.md accurate.

    The normalized form drives variant-aware known-word matching, replacing the
    old jamdict alt-form lookup. Using one in-process tokenizer for both the
    known-set and the mined sentences keeps lemmas aligned (no cross-tokenizer
    false unknowns) and is ~180x faster than spawning mecab per sentence.
    """
    tok, mode = _sudachi()
    out = []
    for m in tok.tokenize(text, mode):
        out.append((
            m.surface(),
            m.dictionary_form(),
            m.normalized_form(),
            m.reading_form(),
            ",".join(m.part_of_speech()),
        ))
    return out


def is_content_word(pos):
    if any(pos.startswith(p) for p in SKIP_POS_PREFIXES):
        return False
    return any(pos.startswith(p) for p in CONTENT_POS_PREFIXES)


def is_proper_noun(pos):
    """Names of people, places and works — context in a sentence, never vocabulary.

    Deliberately NOT folded into `is_content_word()`: that function also drives video
    mode's card *generation*, and dropping proper nouns there would quietly change what
    video mode proposes. This is applied only at the two extra-unknown COUNTING sites
    (audiobook_scan / _sources), where a name inflates the reported i-level and can
    push an otherwise-clean sentence out of i+1.
    """
    return "固有名詞" in pos


def is_card_worthy(lemma):
    if not lemma:
        return False
    if PURE_DIGITS.match(lemma) or PURE_ASCII.match(lemma) or PUNCT_ONLY.match(lemma):
        return False
    if SINGLE_KANA.match(lemma):
        return False
    # No Japanese script at all → an emoji or stray symbol, not a word. Sudachi tags an
    # unknown symbol as 名詞,普通名詞,サ変可能 (☺︎ did exactly that, July 2026), so POS
    # can't catch it and this check has to. Safe globally: nothing scriptless is a card.
    if not HAS_KANJI.search(lemma) and not HAS_KANA.search(lemma):
        return False
    if not HAS_KANJI.search(lemma) and KANA_ONLY_SHORT.match(lemma):
        return False
    return True


def kata_to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def extract_kanji_stem(lemma):
    m = KANJI_RE.match(lemma)
    return m.group(0) if m else ""


def load_known_intervals(sources):
    """Self-contained re-implementation of AnkiMorphs' known-lemma map.

    For each configured source (an Anki search + a note field), pull the cards,
    read the field, tokenize it (SudachiPy), and record every content lemma's
    HIGHEST card interval — exactly the `highest_lemma_learning_interval` idea
    AnkiMorphs stores, but computed live through AnkiConnect so the skill needs no
    AnkiMorphs install and no ankimorphs.db. Using the same tokenizer here and on
    the mined sentences guarantees lemmas line up (no cross-tokenizer false
    unknowns).

    Returns (intervals, norm_intervals):
      intervals       {dictionary_form: highest_interval_in_days}
      norm_intervals  {normalized_form: highest_interval_in_days}
    The second map powers variant-aware known matching (こもる counts as known if
    籠る is known, since both normalize to 籠もる) — replacing the jamdict hack.
    New/learning cards report interval <= 0, so they fall below the known threshold.
    """
    intervals = {}
    norm_intervals = {}
    for src in sources or []:
        query = (src.get("query") or "").strip()
        field = (src.get("field") or "").strip()
        if not query or not field:
            continue
        card_ids = anki_request("findCards", query=query)
        if not card_ids:
            print(f"  known-source matched 0 cards: {query!r}", file=sys.stderr)
            continue
        seen_field = False
        for i in range(0, len(card_ids), 500):
            chunk = anki_request("cardsInfo", cards=card_ids[i : i + 500])
            for c in chunk:
                ivl = c.get("interval", 0) or 0
                fobj = c.get("fields", {}).get(field)
                if fobj is None:
                    continue
                seen_field = True
                text = strip_html(strip_furigana(fobj.get("value", "")))
                if not text:
                    continue
                for surface, lemma, normalized, reading, pos in tokenize(text):
                    if not is_content_word(pos) or not is_card_worthy(lemma):
                        continue
                    if ivl > intervals.get(lemma, -(10**9)):
                        intervals[lemma] = ivl
                    if normalized and ivl > norm_intervals.get(normalized, -(10**9)):
                        norm_intervals[normalized] = ivl
        if not seen_field:
            print(
                f"  WARNING: field {field!r} not found on cards for {query!r} "
                f"(check field name in config.known_words)",
                file=sys.stderr,
            )
    return intervals, norm_intervals


def _sources_key(sources):
    import hashlib
    blob = json.dumps(sources, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def get_known_intervals(cfg, force_refresh=False):
    """load_known_intervals with an optional on-disk cache.

    Scanning ~13k cards + tokenizing takes ~100s, so re-running it for every
    single-video mine is wasteful. Cache the lemma->interval map under work_dir,
    keyed on the exact sources list (so editing config auto-invalidates) and the
    threshold. TTL is config.known_words.cache_hours (default 6; 0 disables).
    Pass --refresh-known to force a rescan after a big review session.

    Returns (intervals, norm_intervals) — see load_known_intervals.
    """
    kw = cfg["known_words"]
    sources = kw.get("sources", [])
    cache_hours = kw.get("cache_hours", 6)
    work_dir = os.path.expanduser(cfg.get("work_dir") or "~/Downloads/sentence-mining")
    cache_path = os.path.join(work_dir, ".known_cache.json")
    key = _sources_key(sources)

    if not force_refresh and cache_hours and os.path.exists(cache_path):
        try:
            with open(cache_path, encoding="utf-8") as f:
                cached = json.load(f)
            age_h = (time.time() - cached.get("ts", 0)) / 3600
            if (cached.get("sources_key") == key
                    and cached.get("threshold") == KNOWN_INTERVAL_THRESHOLD
                    and "norm_intervals" in cached  # skip pre-Sudachi cache shape
                    and age_h < cache_hours):
                print(f"  known-set: cache hit ({age_h:.1f}h old, "
                      f"{len(cached['intervals'])} lemmas)", file=sys.stderr)
                return cached["intervals"], cached["norm_intervals"]
        except Exception:  # noqa: BLE001 — corrupt cache → just rescan
            pass

    intervals, norm_intervals = load_known_intervals(sources)
    if cache_hours:
        try:
            os.makedirs(work_dir, exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({
                    "sources_key": key,
                    "threshold": KNOWN_INTERVAL_THRESHOLD,
                    "ts": time.time(),
                    "intervals": intervals,
                    "norm_intervals": norm_intervals,
                }, f, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            pass
    return intervals, norm_intervals


def load_mature_kanji_stems(intervals):
    stems = set()
    for lemma, interval in intervals.items():
        if interval >= KNOWN_INTERVAL_THRESHOLD:
            stem = extract_kanji_stem(lemma)
            if stem:
                stems.add(stem)
    return stems


def load_jpdb_priority(path):
    """Optional frequency ranking. Missing/empty path → empty map (ranking then
    falls back to source order, which is fine)."""
    priority = {}
    if not path or not os.path.exists(path):
        if path:
            print(f"  JPDB priority CSV not found at {path} — ranking by source order.",
                  file=sys.stderr)
        return priority
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            lemma = line.strip()
            if lemma and lemma not in priority:
                priority[lemma] = i
    return priority


def anki_request(action, **params):
    """AnkiConnect call with retry-with-backoff. AnkiConnect can return transient
    socket errors under burst load (parallel-9 jobs hitting it has produced
    'Operation timed out'); we retry up to 3 times with 1s/2s/4s backoff."""
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    last_exc = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                ANKICONNECT,
                data=body,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                resp = json.loads(r.read())
            if resp.get("error"):
                raise RuntimeError(f"AnkiConnect: {resp['error']}")
            return resp["result"]
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last_exc = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"AnkiConnect failed after 3 attempts: {last_exc}")


def existing_wordforms_in_deck():
    if not DEDUPE_DECKS_QUERY:  # no decks configured — skip dedupe rather than match all
        return set()
    note_ids = anki_request("findNotes", query=DEDUPE_DECKS_QUERY)
    if not note_ids:
        return set()
    forms = set()
    for i in range(0, len(note_ids), 1000):
        chunk = anki_request("notesInfo", notes=note_ids[i : i + 1000])
        for n in chunk:
            wf = n["fields"].get(ANKI_NOTE_FIELD, {}).get("value", "").strip()
            if wf:
                forms.add(wf)
    return forms


def _dominant_speaker(sent):
    """Best-effort speaker label for a sentence. Prefers an explicit `speaker`
    field set in Step 2.5; otherwise picks the most-frequent speaker across
    the sentence's words."""
    if sent.get("speaker"):
        return sent["speaker"]
    counts = {}
    for w in sent.get("words", []):
        sp = w.get("speaker")
        if sp:
            counts[sp] = counts.get(sp, 0) + 1
    if not counts:
        return None
    return max(counts.items(), key=lambda kv: kv[1])[0]


def analyze_one(transcript, source_id, source_url, intervals, norm_intervals, mature_stems, priority, existing):
    annotated_sentences = []
    for idx, sent in enumerate(transcript["sentences"]):
        tokens = tokenize(sent["text"])
        content = [(s, l, n, r, p) for (s, l, n, r, p) in tokens if is_content_word(p)]
        unknown = []
        for surface, lemma, normalized, reading, pos in content:
            if not is_card_worthy(lemma):
                continue
            if intervals.get(lemma, 0) >= KNOWN_INTERVAL_THRESHOLD:
                continue
            # Variant-aware: known if any spelling variant (same normalized form)
            # is known — e.g. candidate こもる is skipped when 籠る is known.
            if normalized and norm_intervals.get(normalized, 0) >= KNOWN_INTERVAL_THRESHOLD:
                continue
            stem = extract_kanji_stem(lemma)
            if stem and stem in mature_stems:
                continue
            unknown.append({
                "surface": surface,
                "lemma": lemma,
                "reading_kata": reading,
                "reading_hira": kata_to_hira(reading),
                # Bare top-level category — tokenize() returns the full tag now, but
                # references/transcript-schema.md documents `pos` as 名詞/動詞/….
                "pos": pos.split(",")[0],
            })
        annotated_sentences.append({
            "idx": idx,
            "text": sent["text"],
            "start_ms": sent["start_ms"],
            "end_ms": sent["end_ms"],
            "speaker": _dominant_speaker(sent),
            "words": sent["words"],
            "unknown_lemmas": unknown,
        })

    best_sentence_for_lemma = {}
    for sent in annotated_sentences:
        for u in sent["unknown_lemmas"]:
            lemma = u["lemma"]
            current = best_sentence_for_lemma.get(lemma)
            score = (len(sent["unknown_lemmas"]), sent["idx"])
            if current is None or score < current["score"]:
                best_sentence_for_lemma[lemma] = {
                    "score": score,
                    "sentence": sent,
                    "unknown_info": u,
                }

    candidates = []
    skipped_dupes = 0
    for lemma, picked in best_sentence_for_lemma.items():
        if lemma in existing:
            skipped_dupes += 1
            continue
        sent = picked["sentence"]
        info = picked["unknown_info"]
        unknown_count = len(sent["unknown_lemmas"])
        deck = MAIN_DECK if unknown_count == 1 else DEFERRED_DECK
        i_level = f"i{min(unknown_count, 9)}"

        target_start_ms = sent["start_ms"]
        for w in sent["words"]:
            if info["surface"] in w["text"] or w["text"] in info["surface"]:
                target_start_ms = w["start_ms"]
                break

        candidates.append({
            "lemma": lemma,
            "reading": info["reading_hira"],
            "surface": info["surface"],
            "pos": info["pos"],
            "sentence": sent["text"],
            "sentence_idx": sent["idx"],
            "sentence_start_ms": sent["start_ms"],
            "sentence_end_ms": sent["end_ms"],
            "speaker": sent["speaker"],
            "target_word_start_ms": target_start_ms,
            "unknown_count_in_sentence": unknown_count,
            "deck": deck,
            "i_level": i_level,
            "jpdb_rank": priority.get(lemma, 10**9),
        })

    candidates.sort(key=lambda c: (c["jpdb_rank"], c["sentence_idx"]))
    capped = candidates[:CAP]
    return {
        "source_id": source_id,
        "source_url": source_url,
        "stats": {
            "total_sentences": len(annotated_sentences),
            "unknown_lemmas_found": len(best_sentence_for_lemma),
            "skipped_duplicates": skipped_dupes,
            "candidates_after_cap": len(capped),
        },
        "candidates": capped,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript")
    ap.add_argument("--source-id")
    ap.add_argument("--source-url", default="")
    ap.add_argument("--manifest", help="JSON array of {transcript, source_id, source_url}.")
    ap.add_argument("--output-dir", help="Directory to write per-source candidate JSON when --manifest is used.")
    ap.add_argument("--refresh-known", action="store_true",
                    help="Force a rescan of the known-word set, ignoring the cache.")
    args = ap.parse_args()

    if not args.manifest and not args.transcript:
        ap.error("either --transcript or --manifest is required")

    # Pull per-user setup and publish it to the module globals the helpers read.
    global ANKICONNECT, MAIN_DECK, DEFERRED_DECK, DEDUPE_DECKS_QUERY
    global ANKI_NOTE_FIELD, KNOWN_INTERVAL_THRESHOLD
    cfg = load_config()
    ANKICONNECT = cfg["anki_connect_url"]
    MAIN_DECK = deck_main(cfg)
    DEFERRED_DECK = deck_deferred(cfg)
    ANKI_NOTE_FIELD = cfg["field_map"].get("word") or "wordForm"
    KNOWN_INTERVAL_THRESHOLD = cfg["known_words"].get("interval_threshold", 21)
    dedupe_decks = sorted({MAIN_DECK, DEFERRED_DECK} - {""})
    DEDUPE_DECKS_QUERY = (
        "(" + " OR ".join(f'deck:"{d}"' for d in dedupe_decks) + ")"
        if dedupe_decks else ""
    )

    # Load shared state once.
    intervals, norm_intervals = get_known_intervals(cfg, force_refresh=args.refresh_known)
    print(f"  known lemmas (interval >= {KNOWN_INTERVAL_THRESHOLD}): "
          f"{sum(1 for v in intervals.values() if v >= KNOWN_INTERVAL_THRESHOLD)} "
          f"of {len(intervals)} seen", file=sys.stderr)
    mature_stems = load_mature_kanji_stems(intervals)
    priority = load_jpdb_priority(cfg.get("jpdb_priority_csv"))
    existing = existing_wordforms_in_deck()

    if args.manifest:
        if not args.output_dir:
            ap.error("--output-dir is required with --manifest")
        os.makedirs(args.output_dir, exist_ok=True)
        with open(args.manifest, encoding="utf-8") as f:
            entries = json.load(f)
        summary = []
        for e in entries:
            with open(e["transcript"], encoding="utf-8") as tf:
                transcript = json.load(tf)
            out = analyze_one(
                transcript, e["source_id"], e.get("source_url", ""),
                intervals, norm_intervals, mature_stems, priority, existing,
            )
            out_path = os.path.join(args.output_dir, f"{e['source_id']}.candidates.json")
            with open(out_path, "w", encoding="utf-8") as of:
                json.dump(out, of, ensure_ascii=False, indent=2)
            summary.append({
                "source_id": e["source_id"],
                "output": out_path,
                "candidates": out["stats"]["candidates_after_cap"],
                "duplicates_skipped": out["stats"]["skipped_duplicates"],
            })
        print(json.dumps({"results": summary}, ensure_ascii=False, indent=2))
    else:
        with open(args.transcript, encoding="utf-8") as f:
            transcript = json.load(f)
        out = analyze_one(
            transcript, args.source_id, args.source_url,
            intervals, norm_intervals, mature_stems, priority, existing,
        )
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
