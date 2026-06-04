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
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request

ANKIMORPHS_DB = os.path.expanduser(
    "~/Library/Application Support/Anki2/User 1/ankimorphs.db"
)
JPDB_CSV = os.path.expanduser(
    "~/Library/Application Support/Anki2/User 1/priority-files/ja-JPDBv2.2-lemma-priority.csv"
)
ANKICONNECT = "http://localhost:8765"
MAIN_DECK = "Ray's Sentence Cards"
DEFERRED_DECK = "Ray's Sentence Mining Deferred"
DEDUPE_DECKS_QUERY = f'(deck:"{MAIN_DECK}" OR deck:"{DEFERRED_DECK}")'
ANKI_NOTE_FIELD = "wordForm"

KNOWN_INTERVAL_THRESHOLD = 21
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


def load_morph_intervals():
    con = sqlite3.connect(ANKIMORPHS_DB)
    cur = con.cursor()
    cur.execute(
        "SELECT lemma, MAX(highest_lemma_learning_interval) FROM Morphs GROUP BY lemma"
    )
    intervals = {row[0]: (row[1] or 0) for row in cur.fetchall()}
    con.close()
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


def load_jpdb_priority():
    priority = {}
    with open(JPDB_CSV, encoding="utf-8") as f:
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
    args = ap.parse_args()

    if not args.manifest and not args.transcript:
        ap.error("either --transcript or --manifest is required")

    # Load shared state once.
    intervals = load_morph_intervals()
    mature_stems = load_mature_kanji_stems(intervals)
    priority = load_jpdb_priority()
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
