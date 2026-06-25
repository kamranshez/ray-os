#!/usr/bin/env python3
"""
Transcribe an audio or video file with AssemblyAI -> plain .txt + .srt.

The input is always re-encoded to a small mono 64k MP3 before upload, so a
multi-hundred-MB WAV/MP4 becomes a few MB on the wire.

Usage:
  python transcribe.py <input.(wav|mp3|mp4|mov|...)> [--out /path/basename] [--keyterms keyterms.txt]

Outputs:
  <basename>.txt   plain transcript (YouTube auto-syncs it to timing)
  <basename>.srt   timestamped subtitles

If --out is omitted, outputs go to this skill's outputs/<input-stem>.
If --keyterms is omitted, only the built-in base terms are boosted.
"""

import sys
import os
import argparse
import subprocess
import tempfile
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = "https://api.assemblyai.com/v2"

# Always-on key terms. Per-video terms (from extract_keyterms.py) are added on top.
BASE_KEYTERMS = ["Claude Code", "Anthropic", "Claude"]


def to_mp3(src: str, dst: str) -> str:
    """Re-encode any audio/video to mono 64k MP3 to minimize the upload."""
    print(f"Encoding {src} -> mono 64k MP3...")
    subprocess.run(
        ["ffmpeg", "-y", "-i", src,
         "-vn", "-acodec", "libmp3lame", "-ar", "44100", "-ac", "1", "-b:a", "64k",
         dst],
        check=True, capture_output=True,
    )
    src_mb = os.path.getsize(src) / 1024 / 1024
    dst_mb = os.path.getsize(dst) / 1024 / 1024
    print(f"MP3 ready: {dst_mb:.1f} MB (from {src_mb:.0f} MB source)")
    return dst


def upload(audio: str, api_key: str) -> str:
    print(f"Uploading audio ({os.path.getsize(audio)/1024/1024:.1f} MB)...")
    with open(audio, "rb") as f:
        r = requests.post(f"{BASE_URL}/upload", headers={"authorization": api_key}, data=f)
    r.raise_for_status()
    print("Upload complete.")
    return r.json()["upload_url"]


def transcribe(upload_url: str, api_key: str, keyterms: list[str]) -> tuple[str, str]:
    """Returns (transcript_id, plain_text)."""
    print(f"Creating transcript job ({len(keyterms)} key terms)...")
    r = requests.post(
        f"{BASE_URL}/transcript",
        headers={"authorization": api_key, "content-type": "application/json"},
        json={
            "audio_url": upload_url,
            "speech_models": ["universal-3-pro"],
            "language_detection": True,
            "keyterms_prompt": keyterms,
        },
    )
    if not r.ok:
        print(f"Error {r.status_code}: {r.text}")
        r.raise_for_status()
    tid = r.json()["id"]
    print(f"Transcript ID: {tid}")

    while True:
        res = requests.get(f"{BASE_URL}/transcript/{tid}", headers={"authorization": api_key}).json()
        st = res["status"]
        if st == "completed":
            print(f"Done! {res.get('audio_duration',0)/60:.1f} min, "
                  f"confidence {res.get('confidence',0)*100:.1f}%, "
                  f"{len(res.get('words',[]))} words")
            return tid, res["text"]
        if st == "error":
            raise RuntimeError(res.get("error", "unknown error"))
        print(f"  {st}...")
        time.sleep(3)


def fetch_srt(tid: str, api_key: str) -> str:
    r = requests.get(f"{BASE_URL}/transcript/{tid}/srt", headers={"authorization": api_key})
    r.raise_for_status()
    return r.text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", help="output basename (no extension)")
    ap.add_argument("--keyterms", help="newline-delimited key terms file")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: file not found: {args.input}")
        sys.exit(1)

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set in .env")
        sys.exit(1)

    keyterms = list(BASE_KEYTERMS)
    if args.keyterms:
        extra = [l.strip() for l in open(args.keyterms) if l.strip()]
        # de-dupe, preserve order, base terms first
        seen = {k.lower() for k in keyterms}
        for k in extra:
            if k.lower() not in seen:
                keyterms.append(k); seen.add(k.lower())

    if args.out:
        out_base = args.out
    else:
        out_dir = Path(__file__).resolve().parent.parent / "outputs"
        out_dir.mkdir(exist_ok=True)
        out_base = str(out_dir / Path(args.input).stem)

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()
    try:
        to_mp3(args.input, tmp.name)
        upload_url = upload(tmp.name, api_key)
        tid, text = transcribe(upload_url, api_key, keyterms)
        srt = fetch_srt(tid, api_key)
    finally:
        os.unlink(tmp.name)

    Path(out_base).parent.mkdir(parents=True, exist_ok=True)
    Path(f"{out_base}.txt").write_text(text)
    Path(f"{out_base}.srt").write_text(srt)
    print(f"\nSaved {out_base}.txt")
    print(f"Saved {out_base}.srt")


if __name__ == "__main__":
    main()
