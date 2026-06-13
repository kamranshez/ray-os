#!/usr/bin/env python3
"""Tokenize, diff against AnkiMorphs DB, dedupe via AnkiConnect, rank by JPDB priority.

Input: AssemblyAI transcript JSON (from transcribe.py, post Step 2.5 splitting).
Output: candidate cards JSON per source.

Single-call mode lets multiple videos share one mecab + jamdict + AnkiConnect load.

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
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _config import load_config, deck_main, deck_deferred

CAP = 50

CONTENT_POS_PREFIXES = ("名詞", "動詞", "形容詞", "副詞", "連体詞", "感動詞", "形状詞")
SKIP_POS_PREFIXES = ("助詞", "助動詞", "補助記号", "記号", "接尾辞", "接頭辞", "代名詞", "フィラー")

PURE_DIGITS = re.compile(r"^[0-9０-９]+$")
PURE_ASCII = re.compile(r"^[A-Za-z]+$")
PUNCT_ONLY = re.compile(r"^[!?！？。、,\.…\-—~〜]+$")
SINGLE_KANA = re.compile(r"^[぀-ゟ゠-ヿー]$")
KANA_ONLY_SHORT = re.compile(r"^[぀-ゟ゠-ヿー]{1,2}$")
HAS_KANJI = re.compile(r"[一-鿿]")
KANJI_RE = re.compile(r"[一-鿿々]+")

HTML_TAG_RE = re.compile(r"<[^>]+>")
FURIGANA_RE = re.compile(r"([一-龯々]+)\[([ぁ-ゖァ-ヺー]+)\]")

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
    # Anki furigana lives as `漢字[かんじ]`; drop the reading so mecab sees clean text.
    return FURIGANA_RE.sub(r"\1", s)


def mecab_tokenize(text):
    p = subprocess.run(
        ["mecab"], input=text, capture_output=True, text=True, check=True
    )
    tokens = []
    for line in p.stdout.splitlines():
        if line == "EOS" or not line.strip() or "\t" not in line:
            continue
        surface, features = line.split("\t", 1)
        parts = features.split(",")
        pos = parts[0] if parts else ""
        if len(parts) >= 7 and parts[6] not in ("*", ""):
            lemma = parts[6]
        else:
            lemma = surface
        reading = parts[7] if len(parts) >= 8 and parts[7] != "*" else ""
        tokens.append((surface, lemma, reading, pos))
    return tokens


def is_content_word(pos):
    if any(pos.startswith(p) for p in SKIP_POS_PREFIXES):
        return False
    return any(pos.startswith(p) for p in CONTENT_POS_PREFIXES)


def is_card_worthy(lemma):
    if not lemma:
        return False
    if PURE_DIGITS.match(lemma) or PURE_ASCII.match(lemma) or PUNCT_ONLY.match(lemma):
        return False
    if SINGLE_KANA.match(lemma):
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
    read the field, mecab-tokenize it, and record every content lemma's HIGHEST
    card interval — exactly the `highest_lemma_learning_interval` idea AnkiMorphs
    stores, but computed live through AnkiConnect so the skill needs no AnkiMorphs
    install and no ankimorphs.db. Using the same mecab tokenizer here and on the
    mined sentences guarantees lemmas line up (no cross-tokenizer false unknowns).

    Returns {lemma: highest_interval_in_days}. New/learning cards report interval
    <= 0 (or seconds), so they naturally fall below the >= 21 known threshold.
    """
    intervals = {}
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
                for surface, lemma, reading, pos in mecab_tokenize(text):
                    if not is_content_word(pos) or not is_card_worthy(lemma):
                        continue
                    if ivl > intervals.get(lemma, -(10**9)):
                        intervals[lemma] = ivl
        if not seen_field:
            print(
                f"  WARNING: field {field!r} not found on cards for {query!r} "
                f"(check field name in config.known_words)",
                file=sys.stderr,
            )
    return intervals


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
                    and age_h < cache_hours):
                print(f"  known-set: cache hit ({age_h:.1f}h old, "
                      f"{len(cached['intervals'])} lemmas)", file=sys.stderr)
                return cached["intervals"]
        except Exception:  # noqa: BLE001 — corrupt cache → just rescan
            pass

    intervals = load_known_intervals(sources)
    if cache_hours:
        try:
            os.makedirs(work_dir, exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump({
                    "sources_key": key,
                    "threshold": KNOWN_INTERVAL_THRESHOLD,
                    "ts": time.time(),
                    "intervals": intervals,
                }, f, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            pass
    return intervals


def load_mature_kanji_stems(intervals):
    stems = set()
    for lemma, interval in intervals.items():
        if interval >= KNOWN_INTERVAL_THRESHOLD:
            stem = extract_kanji_stem(lemma)
            if stem:
                stems.add(stem)
    return stems


_jam = None


def _jamdict():
    global _jam
    if _jam is None:
        from jamdict import Jamdict
        _jam = Jamdict()
    return _jam


def jmdict_alt_forms(lemma):
    try:
        result = _jamdict().lookup(lemma)
    except Exception:
        return set()
    forms = set()
    for entry in result.entries:
        for k in entry.kanji_forms:
            forms.add(k.text)
        for k in entry.kana_forms:
            forms.add(k.text)
    return forms


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


def analyze_one(transcript, source_id, source_url, intervals, mature_stems, priority, existing):
    annotated_sentences = []
    for idx, sent in enumerate(transcript["sentences"]):
        tokens = mecab_tokenize(sent["text"])
        content = [(s, l, r, p) for (s, l, r, p) in tokens if is_content_word(p)]
        unknown = []
        for surface, lemma, reading, pos in content:
            if not is_card_worthy(lemma):
                continue
            if intervals.get(lemma, 0) >= KNOWN_INTERVAL_THRESHOLD:
                continue
            alt_forms = jmdict_alt_forms(lemma)
            if any(intervals.get(f, 0) >= KNOWN_INTERVAL_THRESHOLD for f in alt_forms):
                continue
            stem = extract_kanji_stem(lemma)
            if stem and stem in mature_stems:
                continue
            unknown.append({
                "surface": surface,
                "lemma": lemma,
                "reading_kata": reading,
                "reading_hira": kata_to_hira(reading),
                "pos": pos,
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
    intervals = get_known_intervals(cfg, force_refresh=args.refresh_known)
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
                intervals, mature_stems, priority, existing,
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
            intervals, mature_stems, priority, existing,
        )
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
