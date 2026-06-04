#!/usr/bin/env python3
"""Push staged draft cards to Anki via AnkiConnect. Suspend Deferred cards.

Reports per-card success/failure but never aborts the batch — a late-detected
duplicate shouldn't stop the other 19 cards from landing.
"""
import argparse
import datetime as dt
import json
import sys
import urllib.request

ANKICONNECT = "http://localhost:8765"
MODEL = "Ray's Sentence Mining"


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


PERMANENT_TAG = "claude-sentence-mining"


def build_note(candidate, source_url, date_tag, source_tag):
    return {
        "deckName": candidate["deck"],
        "modelName": MODEL,
        "fields": {
            "wordForm": candidate["lemma"],
            "reading": candidate.get("reading", ""),
            "sentence": candidate["sentence"],
            "sentenceAudio": f"[sound:{candidate['sentenceAudio_file']}]",
            "picture": f'<img src="{candidate["picture_file"]}">',
            "explanation": candidate.get("explanation", ""),
            "explanationAudio": f"[sound:{candidate['explanationAudio_file']}]",
            "definition": "",
            "wordAudio": "",
            "pitchAccent": "",
            "frequency_yomitan": "",
            "frequency_addon": "",
            "source_url": source_url,
        },
        "tags": [PERMANENT_TAG, date_tag, source_tag, candidate.get("i_level", "")],
        "options": {"allowDuplicate": False},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    args = ap.parse_args()

    with open(args.draft, encoding="utf-8") as f:
        data = json.load(f)

    date_tag = f"auto-mined:{dt.date.today().isoformat()}"
    source_tag = f"source:{data['source_id']}"

    # Make sure both decks exist (createDeck is idempotent).
    decks_needed = {c["deck"] for c in data["candidates"]}
    for d in decks_needed:
        anki_request("createDeck", deck=d)

    notes = [
        build_note(c, data.get("source_url", ""), date_tag, source_tag)
        for c in data["candidates"]
    ]

    # addNotes returns a list of new note IDs (or None for failures, in order).
    note_ids = anki_request("addNotes", notes=notes)

    added = 0
    failed = []
    for candidate, note_id in zip(data["candidates"], note_ids):
        if note_id is None:
            failed.append(candidate["lemma"])
            continue
        added += 1

    print(json.dumps({
        "added": added,
        "failed": failed,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
