#!/usr/bin/env python3
"""Tokenize, diff against AnkiMorphs DB, dedupe via AnkiConnect, rank by JPDB priority.

Input: AssemblyAI transcript JSON (from transcribe.py).
Output: candidate cards JSON.

Why a single script: every step depends on the previous (tokenize → classify → dedupe → rank),
and bundling avoids 4 separate JSON files on disk.
"""
import argparse
import json
import os
import sqlite3
import subprocess
import sys
import urllib.request

ANKIMORPHS_DB = os.path.expanduser(
    "~/Library/Application Support/Anki2/User 1/ankimorphs.db"
)
JPDB_CSV = os.path.expanduser(
    "~/Library/Application Support/Anki2/User 1/priority-files/ja-JPDBv2.2-lemma-priority.csv"
)
ANKICONNECT = "http://localhost:8765"
# Two-deck routing: clean i+1 cards land in Ray's main study deck so they enter
# normal daily review. Cards with more unknowns land in the Deferred deck — they
# stay unsuspended (no separate review schedule), but the deck split lets Ray
# quickly find/clean them out later if context turns out to be too messy.
MAIN_DECK = "Ray's Sentence Cards"
DEFERRED_DECK = "Ray's Sentence Mining Deferred"
DEDUPE_DECKS_QUERY = f'(deck:"{MAIN_DECK}" OR deck:"{DEFERRED_DECK}")'
ANKI_NOTE_FIELD = "wordForm"

KNOWN_INTERVAL_THRESHOLD = 21  # AnkiMorphs default; matches Ray's profile
CAP = 50

# MeCab POS tags we treat as content words (skip particles, aux verbs, symbols, etc.)
CONTENT_POS_PREFIXES = ("名詞", "動詞", "形容詞", "副詞", "連体詞", "感動詞", "形状詞")
SKIP_POS_PREFIXES = ("助詞", "助動詞", "補助記号", "記号", "接尾辞", "接頭辞", "代名詞", "フィラー")

import re

# Patterns for lemmas we should never make cards from. Catches numeric noise from
# transcription, ASCII junk (km, AI, etc.), punctuation tokens, and single-kana
# fragments (ワー, ね, あ) that are usually mecab segmentation errors rather than
# real vocabulary worth a card.
PURE_DIGITS = re.compile(r"^[0-9０-９]+$")
PURE_ASCII = re.compile(r"^[A-Za-z]+$")
PUNCT_ONLY = re.compile(r"^[!?！？。、,\.…\-—~〜]+$")
SINGLE_KANA = re.compile(r"^[぀-ゟ゠-ヿー]$")
KANA_ONLY_SHORT = re.compile(r"^[぀-ゟ゠-ヿー]{1,2}$")
HAS_KANJI = re.compile(r"[一-鿿]")


def mecab_tokenize(text):
    """Return list of (surface, lemma, reading, pos) tuples. Uses system mecab.

    Mecab's default IPA dict output format:
      surface\tpos,...,base_form,reading,pronunciation
    """
    p = subprocess.run(
        ["mecab"], input=text, capture_output=True, text=True, check=True
    )
    tokens = []
    for line in p.stdout.splitlines():
        if line == "EOS" or not line.strip():
            continue
        if "\t" not in line:
            continue
        surface, features = line.split("\t", 1)
        parts = features.split(",")
        # IPA dict: pos,subpos1,subpos2,subpos3,inflection_type,inflection_form,base,reading,pron
        # UniDic varies — handle both. Fall back to surface if base form missing/"*".
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
    """Reject lemmas that are almost certainly noise rather than real vocabulary."""
    if not lemma:
        return False
    if PURE_DIGITS.match(lemma) or PURE_ASCII.match(lemma) or PUNCT_ONLY.match(lemma):
        return False
    if SINGLE_KANA.match(lemma):
        return False
    # Short kana-only words (1-2 chars) without kanji are almost always fillers
    # (ワー, あの, ねえ) or mecab segmentation errors. Real common kana words like
    # する, ある, いる are already mature in Ray's deck and won't reach here.
    if not HAS_KANJI.search(lemma) and KANA_ONLY_SHORT.match(lemma):
        return False
    return True


def kata_to_hira(s):
    return "".join(
        chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s
    )


def load_morph_intervals():
    """Return dict[lemma] = highest_lemma_learning_interval. Missing lemma → treat as 0."""
    con = sqlite3.connect(ANKIMORPHS_DB)
    cur = con.cursor()
    cur.execute("SELECT lemma, MAX(highest_lemma_learning_interval) FROM Morphs GROUP BY lemma")
    intervals = {row[0]: (row[1] or 0) for row in cur.fetchall()}
    con.close()
    return intervals


def load_jpdb_priority():
    """Return dict[lemma] = rank (line number, lower = more frequent). Missing → rank=∞."""
    priority = {}
    with open(JPDB_CSV, encoding="utf-8") as f:
        # First line is header "Morph-Lemma"
        for i, line in enumerate(f):
            if i == 0:
                continue
            lemma = line.strip()
            if lemma and lemma not in priority:
                priority[lemma] = i
    return priority


def anki_request(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(
        ANKICONNECT, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
    if resp.get("error"):
        raise RuntimeError(f"AnkiConnect: {resp['error']}")
    return resp["result"]


def existing_wordforms_in_deck():
    """Return wordForm values already in Ray's Sentence Cards or in the Claude mining deck."""
    note_ids = anki_request("findNotes", query=DEDUPE_DECKS_QUERY)
    if not note_ids:
        return set()
    # Batch — notesInfo handles thousands at once but we chunk to be polite.
    forms = set()
    for i in range(0, len(note_ids), 1000):
        chunk = anki_request("notesInfo", notes=note_ids[i : i + 1000])
        for n in chunk:
            wf = n["fields"].get(ANKI_NOTE_FIELD, {}).get("value", "").strip()
            if wf:
                forms.add(wf)
    return forms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", required=True)
    ap.add_argument("--source-id", required=True)
    ap.add_argument("--source-url", default="")
    args = ap.parse_args()

    with open(args.transcript, encoding="utf-8") as f:
        transcript = json.load(f)

    intervals = load_morph_intervals()
    priority = load_jpdb_priority()
    existing = existing_wordforms_in_deck()

    # For each sentence, count unknown lemmas and remember which they are.
    annotated_sentences = []
    for idx, sent in enumerate(transcript["sentences"]):
        tokens = mecab_tokenize(sent["text"])
        content = [(s, l, r, p) for (s, l, r, p) in tokens if is_content_word(p)]
        unknown = []
        for surface, lemma, reading, pos in content:
            if not is_card_worthy(lemma):
                continue
            if intervals.get(lemma, 0) < KNOWN_INTERVAL_THRESHOLD:
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
            "words": sent["words"],
            "unknown_lemmas": unknown,
        })

    # For each unknown lemma, pick the best sentence (fewest unknowns; first appearance as tiebreak).
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

    # Dedupe against existing Anki cards.
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
        i_level = f"i{min(unknown_count, 9)}"  # i1, i2, i3, ... — tag for filtering

        # Find timing of the target word within the sentence.
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
            "target_word_start_ms": target_start_ms,
            "unknown_count_in_sentence": unknown_count,
            "deck": deck,
            "i_level": i_level,
            "jpdb_rank": priority.get(lemma, 10**9),
        })

    # Rank by JPDB priority (lower rank = more frequent = study first).
    candidates.sort(key=lambda c: (c["jpdb_rank"], c["sentence_idx"]))
    capped = candidates[:CAP]

    out = {
        "source_id": args.source_id,
        "source_url": args.source_url,
        "stats": {
            "total_sentences": len(annotated_sentences),
            "unknown_lemmas_found": len(best_sentence_for_lemma),
            "skipped_duplicates": skipped_dupes,
            "candidates_after_cap": len(capped),
        },
        "candidates": capped,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
