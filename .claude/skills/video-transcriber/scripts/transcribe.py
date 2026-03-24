#!/usr/bin/env python3
"""
Step 1: Transcribe an MP4 video using AssemblyAI.

Usage: python transcribe.py <video.mp4>
Output: <video-name>-raw.txt in the current working directory
"""

import sys
import os
import subprocess
import tempfile
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load .env from the skill directory (one level up from scripts/)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

ASSEMBLYAI_BASE_URL = "https://api.assemblyai.com/v2"


def extract_audio(video_path: str, output_path: str) -> str:
    """Extract mono MP3 audio from video using FFmpeg."""
    print(f"Extracting audio from {video_path}...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-acodec", "libmp3lame",
            "-ar", "44100", "-ac", "1", "-b:a", "64k",
            output_path,
        ],
        check=True,
        capture_output=True,
    )
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Audio extracted ({size_mb:.1f} MB): {output_path}")
    return output_path


def upload_to_assemblyai(audio_path: str, api_key: str) -> str:
    """Upload audio file to AssemblyAI and return the upload URL."""
    size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"Uploading audio to AssemblyAI ({size_mb:.1f} MB)...")
    with open(audio_path, "rb") as f:
        response = requests.post(
            f"{ASSEMBLYAI_BASE_URL}/upload",
            headers={"authorization": api_key},
            data=f,
        )
    response.raise_for_status()
    upload_url = response.json()["upload_url"]
    print(f"Upload complete.")
    return upload_url


def transcribe(upload_url: str, api_key: str) -> str:
    """Create a transcription job, poll until complete, return plain text."""
    print("Creating transcription job...")
    headers = {"authorization": api_key, "content-type": "application/json"}
    response = requests.post(
        f"{ASSEMBLYAI_BASE_URL}/transcript",
        headers=headers,
        json={
            "audio_url": upload_url,
            "speech_models": ["universal-3-pro"],
            "language_detection": True,
            "word_boost": [
                "Claude Code",
                "Anthropic",
                "Claude",
            ],
            "boost_param": "high",
        },
    )
    response.raise_for_status()
    transcript_id = response.json()["id"]
    print(f"Transcript ID: {transcript_id}")

    print("Waiting for transcription to complete...")
    while True:
        result = requests.get(
            f"{ASSEMBLYAI_BASE_URL}/transcript/{transcript_id}",
            headers={"authorization": api_key},
        ).json()

        status = result["status"]
        if status == "completed":
            duration_min = result.get("audio_duration", 0) / 60
            confidence = result.get("confidence", 0) * 100
            word_count = len(result.get("words", []))
            print(
                f"Transcription complete! "
                f"Duration: {duration_min:.1f} min, "
                f"Confidence: {confidence:.1f}%, "
                f"Words: {word_count}"
            )
            return result["text"]
        elif status == "error":
            raise RuntimeError(
                f"Transcription failed: {result.get('error', 'Unknown error')}"
            )

        print(f"  Status: {status}...")
        time.sleep(3)


def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <video.mp4>")
        sys.exit(1)

    video_path = sys.argv[1]
    if not os.path.exists(video_path):
        print(f"Error: File not found: {video_path}")
        sys.exit(1)

    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        print("Error: ASSEMBLYAI_API_KEY not set. Add it to the .env file.")
        sys.exit(1)

    # Extract audio to a temp file
    tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_audio.close()

    try:
        extract_audio(video_path, tmp_audio.name)
        upload_url = upload_to_assemblyai(tmp_audio.name, api_key)
        transcript_text = transcribe(upload_url, api_key)
    finally:
        os.unlink(tmp_audio.name)

    # Save raw transcript next to the video
    video_stem = Path(video_path).stem
    output_path = f"{video_stem}-raw.txt"
    with open(output_path, "w") as f:
        f.write(transcript_text)

    print(f"\nRaw transcript saved to: {output_path}")
    print(f"Next step: python correct.py {video_path} {output_path}")


if __name__ == "__main__":
    main()
