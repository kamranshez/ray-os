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

# Re-splitting parameters. AssemblyAI's Japanese sentence segmentation often returns
# 20-30s "sentences" that are really paragraphs. We split them on silence gaps,
# punctuation, Japanese clause endings, and length caps so each card has a
# digestible 3-8s clip with a clean meaning boundary.
SILENCE_GAP_MS = 300        # split when a word-to-word silence exceeds this
MAX_CHUNK_MS = 10000        # hard force-split duration ceiling (rare in clause-rich speech)
MAX_CHUNK_CHARS = 55        # hard force-split char ceiling
SOFT_CHUNK_MS = 3000        # above this, clause-ending tokens are eligible split points
SOFT_CHUNK_CHARS = 22       # above this, clause-ending tokens are eligible split points
MIN_CHUNK_MS = 1200         # try not to emit chunks shorter than this

# Japanese clause-ending tokens we accept as split points once a chunk is "long enough".
# Includes hard punctuation, common discourse markers, and conversational sentence-end forms.
CLAUSE_END_SUFFIXES = (
    # hard punctuation
    "。", "！", "？", "!", "?", "、",
    # conjunctive clause enders (note: we intentionally exclude bare "んだ" / "んです" —
    # they fuse with following けど/よね/から into compound markers, and splitting after
    # them strands those particles at the start of the next chunk)
    "けど", "けれど", "けれども",
    "よね",
    "から", "ので", "のに",
    "だよ", "だね", "だな", "だわ", "だっけ",
    "ます", "ません", "でした", "ました",
)
HARD_PUNCT = ("。", "！", "？", "!", "?")


def _chunk_text(words):
    return "".join(w["text"] for w in words).strip()


def _ends_with_clause_boundary(text):
    text = text.rstrip()
    return any(text.endswith(suffix) for suffix in CLAUSE_END_SUFFIXES)


def _ends_with_hard_punct(text):
    text = text.rstrip()
    return any(text.endswith(p) for p in HARD_PUNCT)


def resplit_sentences(sentences):
    """Re-split AssemblyAI sentences into shorter chunks at meaning boundaries.

    Walk through each word. After appending, decide whether to close the chunk.
    Three tiers of split signals, strongest first:

      HARD: just appended a word ending in 。 ！ ？ ! ? — split immediately.
      MEDIUM: chunk is ≥ SOFT_* thresholds AND ends with a clause-ending token
              (、, けど, よね, から, ます, etc.) OR the gap to the next word is
              ≥ SILENCE_GAP_MS. These are the natural breath points.
      HARD CAP: chunk has hit MAX_CHUNK_MS / MAX_CHUNK_CHARS — force-split even
                if we're mid-thought, so cards never exceed ~8s/40ch.

    MIN_CHUNK_MS at the end merges stragglers forward.
    """
    out = []
    for sent in sentences:
        words = sent.get("words", [])
        if not words:
            out.append(sent)
            continue

        chunks = []
        current = [words[0]]
        for i, w in enumerate(words[:-1], start=1):
            # `w` is already in `current`. We're now deciding whether to close the chunk
            # before appending words[i] (the next word). Re-anchor: append happens below.
            next_w = words[i]
            text_so_far = _chunk_text(current)
            chunk_dur = current[-1]["end_ms"] - current[0]["start_ms"]
            chunk_chars = len(text_so_far)
            gap_to_next = next_w["start_ms"] - current[-1]["end_ms"]

            hit_hard_cap = chunk_dur >= MAX_CHUNK_MS or chunk_chars >= MAX_CHUNK_CHARS
            is_long_enough = chunk_dur >= SOFT_CHUNK_MS or chunk_chars >= SOFT_CHUNK_CHARS
            big_silence = gap_to_next >= SILENCE_GAP_MS
            ends_at_clause = _ends_with_clause_boundary(text_so_far)
            ends_at_hard_punct = _ends_with_hard_punct(text_so_far)

            should_split = (
                ends_at_hard_punct
                or hit_hard_cap
                or (is_long_enough and (big_silence or ends_at_clause))
            )

            if should_split:
                chunks.append(current)
                current = [next_w]
            else:
                current.append(next_w)
        chunks.append(current)

        # Merge any chunk shorter than MIN_CHUNK_MS forward into the next (or back
        # into the previous if it's the last one). Prevents stray 1-word fragments.
        merged = []
        for c in chunks:
            dur = c[-1]["end_ms"] - c[0]["start_ms"]
            if merged and dur < MIN_CHUNK_MS:
                merged[-1].extend(c)
            else:
                merged.append(c)
        if len(merged) >= 2:
            last_dur = merged[-1][-1]["end_ms"] - merged[-1][0]["start_ms"]
            if last_dur < MIN_CHUNK_MS:
                tail = merged.pop()
                merged[-1].extend(tail)

        for c in merged:
            text = "".join(x["text"] for x in c).strip()
            if not text:
                continue
            out.append({
                "text": text,
                "start_ms": c[0]["start_ms"],
                "end_ms": c[-1]["end_ms"],
                "words": c,
            })
    return out


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

    job = _req("POST", "/transcript", {**headers, "content-type": "application/json"}, data={
        "audio_url": audio_url,
        "language_code": "ja",
        "speech_model": "universal",  # routes to the latest Universal (currently Universal-3 Pro, best multilingual accuracy as of 2026)
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

    sentences_resp = _req("GET", f"/transcript/{job_id}/sentences", headers)
    sentences = sentences_resp.get("sentences", [])

    raw_sentences = [
        {
            "text": s["text"],
            "start_ms": s["start"],
            "end_ms": s["end"],
            "words": [
                {"text": w["text"], "start_ms": w["start"], "end_ms": w["end"]}
                for w in s.get("words", [])
            ],
        }
        for s in sentences
    ]
    out = {
        "transcript_id": job_id,
        "language": status.get("language_code", "ja"),
        "audio_duration_ms": int((status.get("audio_duration") or 0) * 1000),
        "sentences": resplit_sentences(raw_sentences),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: transcribe.py <video-path>")
    main(sys.argv[1])
