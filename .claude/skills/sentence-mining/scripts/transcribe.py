#!/usr/bin/env python3
"""Transcribe a video/audio file with AssemblyAI (Japanese), output sentence-segmented JSON.

Usage: transcribe.py <video-path>
Stdout: JSON with {sentences: [{text, start_ms, end_ms, words: [{text, start_ms, end_ms}]}]}
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
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


def _extract_audio(video_path):
    """Transcode to mono 16kHz WAV in a temp file so we upload ~audio-only bytes
    instead of the whole video container. AssemblyAI strips video server-side
    anyway, so shipping the full file just wastes upload time (a 14-min 1080p mp4
    is ~150MB; its 16kHz mono audio is ~25MB). WAV (PCM s16le) is the most
    universally accepted ASR input and needs no decode step server-side. Returns
    (audio_path, is_temp); falls back to the original file if ffmpeg is missing or
    the transcode fails."""
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found; uploading the full file (slower).", file=sys.stderr)
        return video_path, False
    fd, audio_path = tempfile.mkstemp(suffix=".wav", prefix="sm_audio_")
    os.close(fd)
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000",
             "-c:a", "pcm_s16le", audio_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        return audio_path, True
    except (subprocess.CalledProcessError, OSError) as e:
        os.path.exists(audio_path) and os.remove(audio_path)
        print(f"audio extraction failed ({e}); uploading the full file.", file=sys.stderr)
        return video_path, False


def main(video_path):
    load_skill_env()
    key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        sys.exit(
            "ASSEMBLYAI_API_KEY not set. Add it to <skill-dir>/.env "
            "(copy .env.example to .env) or export it in your shell."
        )

    headers = {"authorization": key}

    audio_path, is_temp = _extract_audio(video_path)
    try:
        with open(audio_path, "rb") as f:
            upload = _req("POST", "/upload", headers, data=f.read())
    finally:
        if is_temp:
            os.path.exists(audio_path) and os.remove(audio_path)
    audio_url = upload["upload_url"]

    # `speech_models` (plural) is the current AssemblyAI parameter. The list is a
    # preference order with automatic fallback — Universal-3 Pro is the newest and
    # most accurate (≤10% WER on Japanese), Universal-2 is the safety net in case
    # Pro can't process this specific audio.
    # `speaker_labels` adds diarization (A/B/...). We deliberately don't pass
    # `speakers_expected` — videos may have 1, 2, or N speakers and we want
    # auto-detection.
    job = _req("POST", "/transcript", {**headers, "content-type": "application/json"}, data={
        "audio_url": audio_url,
        "language_code": "ja",
        "speech_models": ["universal-3-pro", "universal-2"],
        "punctuate": True,
        "format_text": True,
        "speaker_labels": True,
    })
    job_id = job["id"]

    while True:
        status = _req("GET", f"/transcript/{job_id}", headers)
        if status["status"] == "completed":
            break
        if status["status"] == "error":
            sys.exit(f"AssemblyAI error: {status.get('error')}")
        time.sleep(1)

    # Build a word-id → speaker map from the utterances array (utterance.words[].speaker).
    # Match by start_ms since AssemblyAI doesn't carry word ids across the two arrays.
    speaker_by_start = {}
    for utt in (status.get("utterances") or []):
        for w in (utt.get("words") or []):
            speaker_by_start[w["start"]] = utt.get("speaker") or w.get("speaker")

    raw_words = [
        {
            "text": w["text"],
            "start_ms": w["start"],
            "end_ms": w["end"],
            "speaker": speaker_by_start.get(w["start"]),
        }
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
        # well-split chunks with preserved timing + speaker labels.
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: transcribe.py <video-path>")
    main(sys.argv[1])
