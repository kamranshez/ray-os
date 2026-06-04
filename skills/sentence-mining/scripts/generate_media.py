#!/usr/bin/env python3
"""For each candidate: clip sentence audio, grab middle frame, generate explanation TTS.

Input: a candidates JSON file where each candidate already has an `explanation` field
       filled in by Claude.
Output: a draft.json with `sentenceAudio`, `picture`, and `explanationAudio` filenames
        added to each candidate. Media is written into Anki's collection.media folder.
"""
import argparse
import asyncio
import json
import os
import subprocess
import sys
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _env import load_skill_env

ANKI_MEDIA = os.path.expanduser(
    "~/Library/Application Support/Anki2/User 1/collection.media"
)

GEMINI_MODEL = "gemini-3.1-flash-tts-preview"
GEMINI_VOICE = "Puck"
TTS_CONCURRENCY = 5


def clip_audio(video_path, start_ms, end_ms, out_path):
    """Extract sentence audio as mp3 with a small lead-in/out pad."""
    pad = 150
    start_s = max(0, (start_ms - pad)) / 1000
    duration_s = (end_ms - start_ms + 2 * pad) / 1000
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{start_s:.3f}",
            "-i", video_path,
            "-t", f"{duration_s:.3f}",
            "-vn", "-acodec", "libmp3lame", "-q:a", "4",
            out_path,
        ],
        check=True,
    )


def grab_screenshot(video_path, start_ms, end_ms, out_path):
    middle_s = ((start_ms + end_ms) / 2) / 1000
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", f"{middle_s:.3f}",
            "-i", video_path,
            "-vframes", "1",
            "-vf", "scale='min(720,iw)':-2",
            "-q:v", "3",
            out_path,
        ],
        check=True,
    )


async def gemini_tts(text, out_path, semaphore):
    """Generate Japanese explanation audio with Gemini 3.1 Flash TTS. Writes mp3."""
    from google import genai
    from google.genai import types

    client = genai.Client()
    async with semaphore:
        resp = await client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=GEMINI_VOICE)
                    )
                ),
            ),
        )
    pcm = resp.candidates[0].content.parts[0].inline_data.data

    # Gemini returns raw 24kHz s16le mono PCM. Wrap as WAV, then transcode to mp3
    # so Anki media size stays small.
    wav_path = out_path + ".tmp.wav"
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
         "-codec:a", "libmp3lame", "-q:a", "4", out_path],
        check=True,
    )
    os.remove(wav_path)


async def process_one(video_path, source_id, idx, candidate, semaphore):
    sent_audio = f"sm_{source_id}_{idx:03d}.mp3"
    screenshot = f"sm_{source_id}_{idx:03d}.jpg"
    explain_audio = f"sm_explain_{source_id}_{idx:03d}.mp3"

    sent_path = os.path.join(ANKI_MEDIA, sent_audio)
    shot_path = os.path.join(ANKI_MEDIA, screenshot)
    exp_path = os.path.join(ANKI_MEDIA, explain_audio)

    # ffmpeg work is CPU/IO bound; run in default executor.
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(None, clip_audio, video_path,
                             candidate["sentence_start_ms"], candidate["sentence_end_ms"], sent_path),
        loop.run_in_executor(None, grab_screenshot, video_path,
                             candidate["sentence_start_ms"], candidate["sentence_end_ms"], shot_path),
        gemini_tts(candidate["explanation"], exp_path, semaphore),
    )

    candidate["sentenceAudio_file"] = sent_audio
    candidate["picture_file"] = screenshot
    candidate["explanationAudio_file"] = explain_audio
    return candidate


async def main_async(args):
    load_skill_env()
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit(
            "GEMINI_API_KEY not set. Add it to <skill-dir>/.env "
            "(copy .env.example to .env) or export it in your shell."
        )

    with open(args.candidates, encoding="utf-8") as f:
        data = json.load(f)

    sem = asyncio.Semaphore(TTS_CONCURRENCY)
    tasks = [
        process_one(args.video, args.source_id, i, c, sem)
        for i, c in enumerate(data["candidates"])
        if c.get("explanation", "").strip()
    ]
    processed = await asyncio.gather(*tasks)

    data["candidates"] = processed
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--source-id", required=True)
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
