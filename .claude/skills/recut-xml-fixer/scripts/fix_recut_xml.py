#!/usr/bin/env python3
"""
Fix a Recut / AutoEdit-style FCP7 XML so it imports cleanly into Premiere with
the user's pristine audio track linked to the video, with no leftover source
audio track and no orphan clips.

Typical input shape (what apps like Recut, AutoEdit, Vika export):

  V1: source video, N clips (silence-cut)
  A1: pristine external audio (e.g. Audio.wav), often offset by 1 clip
  A2: source video's own audio, N clips, aligned with V1

What this script produces:

  V1: source video, M clips (orphans dropped)
  A1: pristine external audio, M clips, vertically aligned with V1, linked
      so selecting a video clip in Premiere also selects its audio clip.
  (A2 deleted entirely.)

Usage:
  python fix_recut_xml.py INPUT.xml [--output OUTPUT.xml] [--keep-audio SUBSTR]

By default it writes alongside the input as INPUT.fixed.xml and a backup as
INPUT.backup.xml.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


TRACK_RE = re.compile(r"(?m)^        <track[ >].*?\n        </track>", re.DOTALL)
CLIPITEM_ID_RE = re.compile(r'<clipitem id="([^"]+)"')
LINK_RE = re.compile(
    r"<link>\s*<linkclipref>([^<]+)</linkclipref>"
    r"\s*<mediatype>([^<]+)</mediatype>"
    r"\s*<trackindex>(\d+)</trackindex>"
    r"\s*<clipindex>(\d+)</clipindex>\s*</link>"
)


def find_track_spans(text: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in TRACK_RE.finditer(text)]


def clip_starts_ends(region: str) -> list[tuple[str, int, int]]:
    out = []
    for m in re.finditer(r'<clipitem id="([^"]+)"[^>]*>(.*?)</clipitem>', region, re.DOTALL):
        cid, body = m.group(1), m.group(2)
        s = re.search(r"<start>(-?\d+)</start>", body)
        e = re.search(r"<end>(-?\d+)</end>", body)
        if s and e:
            out.append((cid, int(s.group(1)), int(e.group(1))))
    return out


def first_clip_name(region: str) -> str:
    m = re.search(r"<clipitem [^>]*>\s*<name>([^<]+)</name>", region)
    return m.group(1) if m else ""


def remove_clip_by_se(region: str, start: int, end: int) -> tuple[str, int]:
    pat = re.compile(
        r"\n?\s*<clipitem [^>]*>(?:(?!</clipitem>).)*?<start>"
        + str(start)
        + r"</start>\s*<end>"
        + str(end)
        + r"</end>(?:(?!</clipitem>).)*?</clipitem>",
        re.DOTALL,
    )
    return pat.subn("", region, count=1)


def remove_track_block(text: str, span: tuple[int, int]) -> str:
    s, e = span
    if e < len(text) and text[e] == "\n":
        e += 1
    return text[:s] + text[e:]


def auto_pick_keep_audio(
    video_clip_name: str,
    audio_track_names: list[str],
    audio_track_clip_counts: list[int] | None = None,
) -> int:
    """Choose the audio track whose first clip name differs from the video clip name.

    The redundant audio track is the one that came in linked to the video and
    therefore shares its filename. The pristine track is the other one.

    Empty tracks (no clipitems) are skipped — Premiere XMLs sometimes include a
    placeholder audio track with no clips that would otherwise win the
    "name differs from video" check.
    """
    video_stem = Path(video_clip_name).stem
    counts = audio_track_clip_counts or [1] * len(audio_track_names)
    # Prefer a non-empty track whose name differs from video.
    for i, name in enumerate(audio_track_names):
        if counts[i] > 0 and Path(name).stem != video_stem:
            return i
    # Otherwise, any non-empty track.
    for i, count in enumerate(counts):
        if count > 0:
            return i
    return 0


def make_link(ref: str, mediatype: str, trackindex: int, clipindex: int) -> str:
    return (
        f"            <link>\n"
        f"              <linkclipref>{ref}</linkclipref>\n"
        f"              <mediatype>{mediatype}</mediatype>\n"
        f"              <trackindex>{trackindex}</trackindex>\n"
        f"              <clipindex>{clipindex}</clipindex>\n"
        f"            </link>\n"
    )


def fix_xml(text: str, keep_audio_substr: str | None = None, log=print) -> str:
    spans = find_track_spans(text)
    if len(spans) < 2:
        raise SystemExit(f"Expected at least 2 top-level tracks (V1 + audio), found {len(spans)}")
    v_span = spans[0]
    audio_spans = spans[1:]

    v_region = text[v_span[0] : v_span[1]]
    v_name = first_clip_name(v_region)
    audio_names = [first_clip_name(text[s:e]) for s, e in audio_spans]
    audio_clip_counts = [
        len(clip_starts_ends(text[s:e])) for s, e in audio_spans
    ]
    log(f"Video track first clip: {v_name!r}")
    log(f"Audio tracks first clips: {audio_names}")
    log(f"Audio tracks clip counts: {audio_clip_counts}")

    # Decide which audio track to keep
    if keep_audio_substr:
        keep_idx = next(
            (i for i, n in enumerate(audio_names) if keep_audio_substr.lower() in n.lower()),
            None,
        )
        if keep_idx is None:
            raise SystemExit(
                f"--keep-audio {keep_audio_substr!r} did not match any of {audio_names}"
            )
    else:
        keep_idx = auto_pick_keep_audio(v_name, audio_names, audio_clip_counts)
    log(f"Keeping audio track {keep_idx} ({audio_names[keep_idx]!r})")

    # Capture EVERY full <file> def before deleting clips. In FCP7 XML, a file's
    # full <file> (path, duration, dimensions) lives on the first clipitem that
    # uses it; later clips use a short <file id="..." /> ref. A single track can
    # reference multiple source files (e.g. two recording sessions concatenated:
    # Loom Recording.mp4 then Loom Recording 2.mp4). If orphan removal deletes the
    # clip that carried any file's full def, that def is lost and Premiere fails
    # the import. So we stash all full defs now and re-inject any that go missing.
    all_full_defs = {
        m.group(1): m.group(0)
        for m in re.finditer(r'<file id="([^"]+)">.*?</file>', text, re.DOTALL)
    }

    # 1) Delete every audio track except the kept one.
    drop_indices = [i for i in range(len(audio_spans)) if i != keep_idx]
    new_text = text
    # Delete from highest offset to lowest so earlier offsets stay valid.
    for i in sorted(drop_indices, reverse=True):
        new_text = remove_track_block(new_text, audio_spans[i])

    # 2) Find orphans between V1 and kept audio, then drop them.
    spans2 = find_track_spans(new_text)
    if len(spans2) != 2:
        raise SystemExit(f"Expected 2 tracks after pruning audio, got {len(spans2)}")
    v_span2, a_span2 = spans2

    v_clips = clip_starts_ends(new_text[v_span2[0] : v_span2[1]])
    a_clips = clip_starts_ends(new_text[a_span2[0] : a_span2[1]])
    v_set = {(s, e) for _, s, e in v_clips}
    a_set = {(s, e) for _, s, e in a_clips}
    v_orphans = sorted(v_set - a_set)
    a_orphans = sorted(a_set - v_set)
    log(f"V1 orphans (no audio counterpart): {len(v_orphans)} {v_orphans[:3]}")
    log(f"A1 orphans (no video counterpart): {len(a_orphans)} {a_orphans[:3]}")

    v_region = new_text[v_span2[0] : v_span2[1]]
    a_region = new_text[a_span2[0] : a_span2[1]]
    for s, e in v_orphans:
        v_region, _ = remove_clip_by_se(v_region, s, e)
    for s, e in a_orphans:
        a_region, _ = remove_clip_by_se(a_region, s, e)

    new_text = (
        new_text[: v_span2[0]] + v_region + new_text[v_span2[1] : a_span2[0]] + a_region + new_text[a_span2[1] :]
    )

    # 3) Re-inject any full <file> definition that orphan removal stripped out.
    # For every source file the surviving clips still reference, ensure its full
    # def is present; if only short refs remain, promote the first one back to the
    # full def. This covers tracks with multiple source files, not just the first.
    referenced_ids = set(re.findall(r'<file id="([^"]+)"', new_text))
    for file_id, full_def in all_full_defs.items():
        if file_id not in referenced_ids:
            continue  # file no longer used (e.g. dropped audio track) — skip
        if re.search(r'<file id="' + re.escape(file_id) + r'">', new_text):
            continue  # full def still present
        short = f'<file id="{file_id}" />'
        if short in new_text:
            new_text = new_text.replace(short, full_def, 1)

    # 4) Rewrite all <link> blocks: each clip on V1 links to itself + matching
    # A1 clip; each A1 clip links to itself + matching V1 clip. Stale clipindex
    # values are what cause Premiere's "import failed" error.
    spans3 = find_track_spans(new_text)
    v_ids = CLIPITEM_ID_RE.findall(new_text[spans3[0][0] : spans3[0][1]])
    a_ids = CLIPITEM_ID_RE.findall(new_text[spans3[1][0] : spans3[1][1]])
    if len(v_ids) != len(a_ids):
        raise SystemExit(f"V1 and A1 clip counts differ after orphan removal: {len(v_ids)} vs {len(a_ids)}")
    log(f"Final clip count per track: {len(v_ids)}")

    pair_v_to_a = dict(zip(v_ids, a_ids))
    pair_a_to_v = dict(zip(a_ids, v_ids))
    v_index = {cid: i + 1 for i, cid in enumerate(v_ids)}
    a_index = {cid: i + 1 for i, cid in enumerate(a_ids)}
    v_set_ids = set(v_ids)
    a_set_ids = set(a_ids)

    links_block_re = re.compile(r"(?:[ \t]*<link>.*?</link>\s*)+", re.DOTALL)
    clip_re = re.compile(r'<clipitem id="([^"]+)"[^>]*>.*?</clipitem>', re.DOTALL)

    def rewrite_clip(m: re.Match) -> str:
        body = m.group(0)
        cid = m.group(1)
        if cid in v_set_ids:
            idx = v_index[cid]
            partner = pair_v_to_a[cid]
            new_block = make_link(cid, "video", 1, idx) + make_link(partner, "audio", 1, idx)
        elif cid in a_set_ids:
            idx = a_index[cid]
            partner = pair_a_to_v[cid]
            new_block = make_link(partner, "video", 1, idx) + make_link(cid, "audio", 1, idx)
        else:
            return body
        new_body, n = links_block_re.subn(new_block, body, count=1)
        if n == 0:
            new_body = body.replace("</clipitem>", new_block + "          </clipitem>")
        return new_body

    new_text = clip_re.sub(rewrite_clip, new_text)

    # Sanity: validate as XML and check no dangling references.
    ET.fromstring(new_text)
    refs = set(re.findall(r"<linkclipref>([^<]+)</linkclipref>", new_text))
    ids = set(CLIPITEM_ID_RE.findall(new_text))
    dangling = refs - ids
    if dangling:
        raise SystemExit(f"Dangling linkclipref after fix: {len(dangling)} ({list(dangling)[:3]})")

    return new_text


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fix a Recut/AutoEdit FCP7 XML for Premiere import.")
    p.add_argument("input", type=Path, help="Path to the source .xml")
    p.add_argument("--output", type=Path, default=None, help="Output path (default: <input>.fixed.xml)")
    p.add_argument(
        "--keep-audio",
        default=None,
        help="Substring of the audio track filename to keep (e.g. 'Audio.wav'). "
        "If omitted, picks the audio track whose name differs from the video track.",
    )
    p.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite the input file (a .backup.xml is always written first).",
    )
    args = p.parse_args(argv)

    src: Path = args.input
    if not src.exists():
        print(f"input not found: {src}", file=sys.stderr)
        return 2

    backup = src.with_suffix(src.suffix + ".backup")
    if not backup.exists():
        shutil.copy2(src, backup)
        print(f"Backup: {backup}")

    text = src.read_text()
    fixed = fix_xml(text, keep_audio_substr=args.keep_audio)

    out = args.output or (src if args.in_place else src.with_name(src.stem + ".fixed" + src.suffix))
    out.write_text(fixed)
    print(f"Wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
