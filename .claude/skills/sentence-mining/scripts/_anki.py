"""Tiny AnkiConnect helpers shared across the skill's scripts.

Why route media writes through AnkiConnect's `storeMediaFile` instead of
shutil.copy directly into `collection.media`: add-ons that hook media events
(notably AJT Media Converter) treat externally-written files as "stale" and
may remove them. Going through Anki's media manager registers the file so
hooks see it as a legitimate add.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    from _config import load_config
except ImportError:  # when imported as a package
    from ._config import load_config


def _connect_url() -> str:
    cfg = load_config(required=False)
    if cfg and cfg.get("anki_connect_url"):
        return cfg["anki_connect_url"]
    return "http://localhost:8765"


def anki_request(action: str, **params):
    """Call AnkiConnect. Retries up to 3 times with backoff on transient errors."""
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    url = _connect_url()
    last_exc = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
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


def _sniff_audio_container(path: Path) -> str | None:
    """Identify a file's ACTUAL audio container from its bytes, ignoring its
    extension. Returns 'wav-pcm', 'mp3', 'm4a', 'ogg', 'flac', 'webm', or None
    (not a recognized audio container -- e.g. an image).

    Why this exists: AnkiMobile/AnkiDroid trust the file extension and pick a
    decoder from it, so a payload that doesn't match its own extension is
    silently unplayable on mobile even though desktop Anki's bundled player
    decodes by content and never notices. Found two independent instances of
    this in July 2026: an old import batch with MP3 bytes wrapped in a
    RIFF/WAVE container named .wav (9 cards), and a kotu.io sentence-audio
    download that was actually M4A/AAC saved as .mp3 (1 card)."""
    try:
        with open(path, "rb") as f:
            head = f.read(64)
    except OSError:
        return None
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        idx = head.find(b"fmt ")
        if idx != -1 and len(head) >= idx + 10:
            fmt_tag = int.from_bytes(head[idx + 8:idx + 10], "little")
            return "wav-pcm" if fmt_tag in (1, 3) else "mp3"  # else e.g. 0x55 = MP3-in-RIFF
        return "wav-pcm"
    if head[4:8] == b"ftyp":
        return "m4a"
    if head[:3] == b"ID3":
        return "mp3"
    for i in range(min(8, len(head) - 1)):
        if head[i] == 0xFF and (head[i + 1] & 0xE0) == 0xE0:  # MPEG frame sync
            return "mp3"
    if head[:4] == b"OggS":
        return "ogg"
    if head[:4] == b"fLaC":
        return "flac"
    if head[:4] == b"\x1a\x45\xdf\xa3":
        return "webm"
    return None


# Containers that only need a rename to become correctly labeled (no re-encode:
# the bytes are already valid content for the corrected extension).
_RENAME_ONLY = {"wav-pcm": "wav", "mp3": "mp3"}


def _transcode_to_mp3(path: Path) -> Path:
    """Re-encode a non-swappable container (m4a/ogg/flac/webm) to a real mp3
    alongside it. Used when a bare rename wouldn't produce valid content for
    the corrected extension (unlike wav<->mp3, which are both already-valid
    payloads that just need their label fixed)."""
    out = path.with_suffix(".mp3") if path.suffix.lower() != ".mp3" else path.with_name(path.stem + ".fixed.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
         "-codec:a", "libmp3lame", "-q:a", "4", str(out)],
        check=True,
    )
    return out


def store_media(local_path: Path | str, target_filename: str) -> str:
    """Register `local_path` in Anki's media folder as `target_filename`.

    For .wav/.mp3 targets, sniffs the actual bytes first and corrects a
    mismatch before registering (see `_sniff_audio_container`): a simple
    rename when the payload is already valid for the corrected extension
    (wav<->mp3), or a real ffmpeg transcode to mp3 when it isn't (m4a/ogg/
    flac/webm content). Returns the filename actually registered -- callers
    MUST use this return value (not their original target_filename) when
    building a [sound:...] field, since it may differ from what was passed in.
    """
    path = Path(local_path).expanduser().resolve()
    suffix = Path(target_filename).suffix.lower()
    if suffix in (".wav", ".mp3"):
        actual = _sniff_audio_container(path)
        if actual and _RENAME_ONLY.get(actual) != suffix.lstrip("."):
            if actual in _RENAME_ONLY:
                corrected = str(Path(target_filename).with_suffix(f".{_RENAME_ONLY[actual]}"))
                print(f"  ! media mismatch: {target_filename} is actually {actual} "
                      f"-- registering as {corrected} instead", file=sys.stderr)
                target_filename = corrected
            else:
                fixed_path = _transcode_to_mp3(path)
                corrected = str(Path(target_filename).with_suffix(".mp3"))
                print(f"  ! media mismatch: {target_filename} is actually {actual} "
                      f"-- transcoded to mp3 and registering as {corrected} instead",
                      file=sys.stderr)
                path = fixed_path
                target_filename = corrected
    anki_request("storeMediaFile", filename=target_filename, path=str(path))
    return target_filename
