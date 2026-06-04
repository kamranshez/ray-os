#!/usr/bin/env python3
"""Transcribe a video/audio file with AssemblyAI (Japanese), output sentence-segmented JSON.

Usage: transcribe.py <video-path>
Stdout: JSON with {sentences: [{text, start_ms, end_ms, words: [{text, start_ms, end_ms}]}]}
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _env import load_skill_env

API = "https://api.assemblyai.com/v2"


def _req(method, path, headers, data=None):
    req = urllib.request.Request(API + path, method=method, headers=headers)
    if data is not None:
        req.data = data if isinstance(data, (bytes, bytearray)) else json.dumps(data).encode()
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def main(video_path):
    load_skill_env()
    key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        sys.exit(
            "ASSEMBLYAI_API_KEY not set. Add it to <skill-dir>/.env "
            "(copy .env.example to .env) or export it in your shell."
        )

    headers = {"authorization": key}

    with open(video_path, "rb") as f:
        upload = _req("POST", "/upload", headers, data=f.read())
    audio_url = upload["upload_url"]

    # `speech_models` (plural) is the current AssemblyAI parameter. The list is a
    # preference order with automatic fallback — Universal-3 Pro is the newest and
    # most accurate (≤10% WER on Japanese), Universal-2 is the safety net in case
    # Pro can't process this specific audio.
    job = _req("POST", "/transcript", {**headers, "content-type": "application/json"}, data={
        "audio_url": audio_url,
        "language_code": "ja",
        "speech_models": ["universal-3-pro", "universal-2"],
        "punctuate": True,
        "format_text": True,
    })
    job_id = job["id"]

    while True:
        status = _req("GET", f"/transcript/{job_id}", headers)
        if status["status"] == "completed":
            break
        if status["status"] == "error":
            sys.exit(f"AssemblyAI error: {status.get('error')}")
        time.sleep(2)

    # Flat word stream with timings. AssemblyAI's sentence segmentation is unreliable
    # for fast/casual Japanese speech, so we don't use it — Claude does sentence
    # splitting + correction with full context in the next step (see SKILL.md).
    raw_words = [
        {"text": w["text"], "start_ms": w["start"], "end_ms": w["end"]}
        for w in (status.get("words") or [])
    ]
    full_text = (status.get("text") or "").strip()
    out = {
        "transcript_id": job_id,
        "language": status.get("language_code", "ja"),
        "audio_duration_ms": int((status.get("audio_duration") or 0) * 1000),
        "full_text": full_text,
        "words": raw_words,
        # `sentences` is intentionally absent — Claude fills it in step 2.5 of
        # SKILL.md by reading `words` + `full_text` and emitting corrected,
        # well-split chunks with preserved timing.
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: transcribe.py <video-path>")
    main(sys.argv[1])
