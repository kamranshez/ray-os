#!/usr/bin/env python3
"""
Step 2: Correct a raw transcript using Gemini with the actual video as context.

Uploads the entire video to Gemini's File API so it can cross-reference
audio with on-screen text (slides, code, terminal output, names, lower-thirds)
to fix transcription errors.

Usage: python correct.py <video.mp4> <raw-transcript.txt>
Output: <video-name>.txt in the current working directory
"""

import sys
import os
import time
from pathlib import Path

from google import genai
from dotenv import load_dotenv

# Load .env from the skill directory (one level up from scripts/)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CORRECTION_PROMPT = """You are given a video and its raw transcript from a speech-to-text engine.

Your task:
1. Watch and listen to the entire video carefully
2. Compare the audio to the provided transcript
3. Fix any transcription errors:
   - Misspelled names, numbers, and technical terms
   - Words that were misheard or garbled
   - Missing or incorrect punctuation
   - Run-on sentences that should be separate
4. Use on-screen text (slides, code, terminal output, lower-thirds, URLs) to verify correct spelling of names, tools, and terms

Key terms to watch for (these are commonly misheard by speech-to-text):
- "Claude Code" (not "cloud code", "clawed code", etc.)
- "Anthropic" (not "anthropomorphic", etc.)
- "MCP" (Model Context Protocol)
- "LLM" / "large language model"
- "Gemini", "AssemblyAI"
- "FFmpeg"

Rules:
- Output ONLY the corrected plain text — no timestamps, no formatting markers
- Preserve natural paragraph breaks (split on topic changes or pauses)
- If something is genuinely unclear, write [inaudible]
- Do NOT add anything that wasn't said — no summaries, headers, or commentary
- No code fences or markdown formatting in the output

Raw transcript:

{transcript}"""

GEMINI_MODEL = "gemini-3-flash"


def upload_video(client, video_path: str):
    """Upload video to Gemini File API and wait until it's ready."""
    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    print(f"Uploading video to Gemini ({size_mb:.1f} MB)...")
    video_file = client.files.upload(file=video_path)
    print("Upload complete. Waiting for processing...")

    while True:
        file_info = client.files.get(name=video_file.name)
        if file_info.state.name == "ACTIVE":
            print("Video processed and ready.")
            return video_file
        elif file_info.state.name == "FAILED":
            raise RuntimeError("Gemini failed to process the video file.")
        time.sleep(2)


def correct_transcript(client, video_file, raw_transcript: str) -> str:
    """Send video + raw transcript to Gemini for correction."""
    print(f"Sending to Gemini ({GEMINI_MODEL}) for correction...")

    prompt = CORRECTION_PROMPT.replace("{transcript}", raw_transcript)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[video_file, prompt],
    )

    corrected = response.text.strip()

    # Strip code fences if Gemini wrapped the output
    if corrected.startswith("```"):
        first_newline = corrected.find("\n")
        if first_newline != -1:
            corrected = corrected[first_newline + 1:]
        else:
            corrected = corrected[3:]
        if corrected.endswith("```"):
            corrected = corrected[:-3]
        corrected = corrected.strip()

    return corrected


def main():
    if len(sys.argv) != 3:
        print("Usage: python correct.py <video.mp4> <raw-transcript.txt>")
        sys.exit(1)

    video_path = sys.argv[1]
    transcript_path = sys.argv[2]

    for p in [video_path, transcript_path]:
        if not os.path.exists(p):
            print(f"Error: File not found: {p}")
            sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Add it to the .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    with open(transcript_path, "r") as f:
        raw_transcript = f.read()

    if not raw_transcript.strip():
        print("Error: Transcript file is empty.")
        sys.exit(1)

    # Upload video and correct
    video_file = upload_video(client, video_path)

    try:
        corrected = correct_transcript(client, video_file, raw_transcript)
    finally:
        # Clean up the uploaded file from Gemini
        try:
            client.files.delete(name=video_file.name)
            print("Cleaned up video from Gemini.")
        except Exception:
            pass

    # Save corrected transcript to skill outputs folder
    skill_dir = Path(__file__).resolve().parent.parent
    outputs_dir = skill_dir / "outputs"
    outputs_dir.mkdir(exist_ok=True)

    video_stem = Path(video_path).stem
    output_path = outputs_dir / f"{video_stem}.txt"
    with open(output_path, "w") as f:
        f.write(corrected)

    print(f"\nCorrected transcript saved to: {output_path}")
    print("Ready to upload to YouTube!")


if __name__ == "__main__":
    main()
