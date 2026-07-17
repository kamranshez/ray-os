#!/usr/bin/env python3
"""Bank-mode MEDIA stage — stage each candidate's clip/screenshot and TTS its explanation.

Input is `find_sentences.py`'s candidates JSON (explanations filled in by Claude). Each
candidate carries `sound_url` / `image_url` from the sentence cascade, which are:
  - URLs        for the web tiers (Immersion Kit, Nadeshiko, sentencesearch, kotu)
  - local paths for the bank tier (the indexed .apkg media)
Both are handled by the same `_stage` helper, so the tier a sentence came from stops
mattering the moment it has been chosen.

Per candidate:
  - stage + register the sentence audio (falls back to Gemini TTS only if the source
    clip is missing — every cascade tier requires native audio, so that's rare)
  - stage + register the image if the tier shipped one; leave `picture_file` empty
    otherwise and let push.py write the "。" filler
  - always Gemini-TTS the `explanation`

All writes go through `_anki.store_media()`, which sniffs the real bytes and corrects a
mismatched extension before registering — so use its RETURN value, never the name you
passed it. See _anki.py.

Output: a draft.json shaped exactly like generate_media.py's, so push.py works unchanged.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import wave
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _env import load_skill_env, require_healthy_gemini_key  # noqa: E402
from _anki import store_media  # noqa: E402
from _style import refuse_if_bad_explanations  # noqa: E402

GEMINI_MODEL = "gemini-3.1-flash-tts-preview"
GEMINI_VOICE = "Puck"
TTS_CONCURRENCY = int(os.environ.get("SM_TTS_CONCURRENCY", "2"))


def _slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", s).strip("_") or "x"


async def gemini_tts(text: str, out_path: Path, semaphore: asyncio.Semaphore) -> None:
    """Render `text` as Japanese speech and write mp3 to `out_path`."""
    from google import genai
    from google.genai import types
    from google.genai import errors as genai_errors

    client = genai.Client()
    async with semaphore:
        for attempt in range(5):
            try:
                resp = await client.aio.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=text,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=GEMINI_VOICE
                                )
                            )
                        ),
                    ),
                )
                # Empty/blocked responses come back with no candidate audio — treat
                # as retryable rather than crashing the whole asyncio.gather.
                cand = (resp.candidates or [None])[0]
                parts = getattr(getattr(cand, "content", None), "parts", None)
                if not parts or getattr(getattr(parts[0], "inline_data", None), "data", None) is None:
                    if attempt < 4:
                        await asyncio.sleep(3 * (attempt + 1))
                        continue
                    raise RuntimeError("Gemini TTS returned no audio after retries")
                break
            except genai_errors.ClientError as e:
                if getattr(e, "code", None) == 429 and attempt < 4:
                    await asyncio.sleep(10 * (attempt + 1))
                    continue
                raise
    pcm = resp.candidates[0].content.parts[0].inline_data.data
    wav_path = out_path.with_suffix(out_path.suffix + ".tmp.wav")
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        wf.writeframes(pcm)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav_path),
         "-codec:a", "libmp3lame", "-q:a", "4", str(out_path)],
        check=True,
    )
    wav_path.unlink()


def _is_url(src: str) -> bool:
    return src.startswith("http://") or src.startswith("https://")


def _ext_of(src: str, default: str) -> str:
    """Extension guessed from the URL/path. Only a guess — store_media() sniffs the real
    bytes and corrects the name if the source lied (kotu.io serves M4A from a .mp3-looking
    URL; one bank shipped MP3 bytes in a .wav). Always use store_media's RETURN value."""
    tail = src.split("?")[0].rsplit(".", 1)
    return tail[1].lower() if len(tail) == 2 and 1 <= len(tail[1]) <= 4 else default


def _stage(src: str, dest: Path) -> None:
    """Put a remote URL or a local file path at `dest` so it can be handed to store_media."""
    if _is_url(src):
        req = urllib.request.Request(src, headers={"User-Agent": "ray-sentence-mining/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
            f.write(r.read())
    else:
        shutil.copyfile(src, dest)


def _media_src(candidate: dict, *keys: str) -> str:
    """First non-empty of the given keys that actually resolves.

    Candidates carry `sound_url` / `image_url` from the sentence cascade — these are
    URLs for the web tiers (Immersion Kit, Nadeshiko, sentencesearch, kotu) and local
    file paths for the bank tier. `existing_audio` / `existing_image` are the legacy
    keys the old bank-only search wrote; still honored so an old draft on disk applies."""
    for k in keys:
        src = (candidate.get(k) or "").strip()
        if not src:
            continue
        if _is_url(src) or Path(src).exists():
            return src
    return ""


async def process_one(idx: int, candidate: dict, workdir: Path, sem: asyncio.Semaphore) -> dict:
    base = f"sm_word_{_slug(candidate.get('lemma', str(idx)))}_{idx}"

    # Sentence audio: stage the cascade's clip (URL or bank file). Every tier of the
    # cascade requires native audio, so the TTS fallback below should be rare — it only
    # fires for a legacy draft or a candidate hand-edited to have no source clip.
    sent_audio_field = ""
    src_audio = _media_src(candidate, "sound_url", "existing_audio")
    if src_audio:
        target = f"{base}_sentence.{_ext_of(src_audio, 'mp3')}"
        try:
            _stage(src_audio, workdir / target)
            sent_audio_field = store_media(workdir / target, target)
        except Exception as e:  # noqa: BLE001
            print(f"  sentence audio failed for {candidate.get('lemma')!r}: {e}", file=sys.stderr)
            src_audio = ""
    if not sent_audio_field:
        target = f"{base}_sentence_tts.mp3"
        local = workdir / target
        try:
            await gemini_tts(candidate["sentence"], local, sem)
            sent_audio_field = store_media(local, target)
        except Exception as e:  # noqa: BLE001
            print(f"  sentence TTS failed for {candidate.get('lemma')!r}: {e}", file=sys.stderr)

    # Image: the audio-only tiers (sentencesearch, kotu) legitimately ship none. Leave
    # picture_file empty and let push.py write the "。" filler — a BLANK picture field
    # makes the Back template replay the sentence audio on mobile. See SKILL.md §MEDIA.
    pic_field = ""
    src_img = _media_src(candidate, "image_url", "existing_image")
    if src_img:
        target_img = f"{base}_image.{_ext_of(src_img, 'jpg')}"
        try:
            _stage(src_img, workdir / target_img)
            pic_field = store_media(workdir / target_img, target_img)
        except Exception as e:  # noqa: BLE001
            print(f"  image failed for {candidate.get('lemma')!r}: {e}", file=sys.stderr)

    # Explanation TTS — always.
    exp_target = f"sm_explain_{_slug(candidate.get('lemma', str(idx)))}_{idx}.mp3"
    exp_local = workdir / exp_target
    try:
        await gemini_tts(candidate["explanation"], exp_local, sem)
        exp_target = store_media(exp_local, exp_target)
    except Exception as e:  # noqa: BLE001
        print(f"  explanation TTS failed for {candidate.get('lemma')!r}: {e}", file=sys.stderr)
        exp_target = ""

    candidate["sentenceAudio_file"] = sent_audio_field
    candidate["picture_file"] = pic_field
    candidate["explanationAudio_file"] = exp_target
    return candidate


async def main_async(args):
    load_skill_env()
    require_healthy_gemini_key()  # covers missing AND ephemeral (would die mid-run)

    data = json.loads(Path(args.candidates).expanduser().read_text())

    # House-style gate: refuse before ANY download/TTS spend — a bad or empty
    # explanation means the draft needs rewriting, not media. (Curation drops an
    # unwanted candidate by DELETING its entry, never by blanking the explanation.)
    refuse_if_bad_explanations(
        [(c["lemma"], c.get("explanation", "")) for c in data["candidates"]],
        "generate_media_bank.py")
    keep = data["candidates"]

    sem = asyncio.Semaphore(TTS_CONCURRENCY)
    with tempfile.TemporaryDirectory(prefix="sm_bank_media_") as tmp:
        workdir = Path(tmp)
        tasks = [process_one(i, c, workdir, sem) for i, c in enumerate(keep)]
        processed = await asyncio.gather(*tasks)

    data["candidates"] = processed
    out = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).expanduser().write_text(out)
        print(f"Wrote {len(processed)} draft cards to {args.output}", file=sys.stderr)
    else:
        print(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True, help="Candidates JSON with explanation field filled.")
    ap.add_argument("--output", default=None, help="Where to write draft.json (default stdout).")
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
