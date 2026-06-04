#!/usr/bin/env python3
"""Push staged draft cards to Anki via AnkiConnect.

Reports per-card success/failure but never aborts the batch — a late-detected
duplicate shouldn't stop the other 19 cards from landing.
"""
import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request

ANKICONNECT = "http://localhost:8765"
MODEL = "Ray's Sentence Mining"


def anki_request(action, **params):
    """Retry up to 3 times with 1s/2s/4s backoff on transient socket errors."""
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


PERMANENT_TAG_VIDEO = "claude-sentence-mining"
PERMANENT_TAG_BANK = "claude-sentence-bank"


def build_note(candidate, source_url, date_tag, permanent_tag):
    speaker = candidate.get("speaker")
    speaker_tag = f"speaker:{speaker}" if speaker else None
    # Prepend a small speaker prefix to the sentence so the card shows who's
    # talking. Skip if no diarization data — keep older drafts working.
    sentence_text = candidate["sentence"]
    if speaker:
        sentence_text = f"<b>{speaker}:</b> {sentence_text}"

    tags = [permanent_tag, date_tag, candidate.get("i_level", "")]
    if speaker_tag:
        tags.append(speaker_tag)
    bank_id = candidate.get("bank_id")
    if bank_id:
        tags.append(f"bank:{bank_id}")
    tags = [t for t in tags if t]

    sentence_audio_file = candidate.get("sentenceAudio_file", "")
    picture_file = candidate.get("picture_file", "")
    explanation_audio_file = candidate.get("explanationAudio_file", "")

    return {
        "deckName": candidate["deck"],
        "modelName": MODEL,
        "fields": {
            "wordForm": candidate["lemma"],
            "reading": candidate.get("reading", ""),
            "sentence": sentence_text,
            "sentenceAudio": f"[sound:{sentence_audio_file}]" if sentence_audio_file else "",
            "picture": f'<img src="{picture_file}">' if picture_file else "",
            "explanation": candidate.get("explanation", ""),
            "explanationAudio": f"[sound:{explanation_audio_file}]" if explanation_audio_file else "",
            "definition": "",
            "wordAudio": "",
            "pitchAccent": "",
            "frequency_yomitan": "",
            "frequency_addon": "",
            "source_url": source_url,
        },
        "tags": tags,
        "options": {"allowDuplicate": False},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    args = ap.parse_args()

    with open(args.draft, encoding="utf-8") as f:
        data = json.load(f)

    date_tag = f"auto-mined:{dt.date.today().isoformat()}"
    permanent_tag = PERMANENT_TAG_BANK if data.get("source") == "bank-search" else PERMANENT_TAG_VIDEO

    # Make sure both decks exist (createDeck is idempotent).
    decks_needed = {c["deck"] for c in data["candidates"]}
    for d in decks_needed:
        anki_request("createDeck", deck=d)

    notes = [
        build_note(c, data.get("source_url", ""), date_tag, permanent_tag)
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
