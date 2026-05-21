#!/usr/bin/env python3
"""
sync-and-cut — align separately-recorded audio to screen recordings, combine
each pair into one file, optionally silence-cut with recut, and export a
single Adobe Premiere Pro XML.

Pipeline, per recording pair:
  1. Measure the time offset between the screen recording's own audio and the
     clean external audio, by cross-correlating their speech-energy envelopes.
  2. Mux the video with the offset-corrected clean audio into one .mov — video
     copied losslessly, the screen recording's own scratch audio dropped.
  3. (unless --sync-only) Run recut on the combined files to remove silence.
  4. Write one Premiere XML referencing the combined files.

Combining BEFORE recut is the key idea: recut then sees a single file per
recording, so it cuts video and audio as one locked unit — no multi-track
drift, no sync offset to reconcile afterwards.

Requires: ffmpeg, ffprobe, recut, and python3 with numpy.
"""
from __future__ import annotations
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import wave
import xml.etree.ElementTree as ET

try:
    import numpy as np
except ImportError:
    sys.exit("error: numpy is required  ->  pip3 install numpy")

VIDEO_EXTS = ('.mp4', '.mov', '.mkv', '.m4v', '.avi', '.webm')
AUDIO_EXTS = ('.wav', '.m4a', '.mp3', '.aiff', '.aif', '.flac', '.aac')
SYNCED_SUFFIX = ' (synced).mov'   # combined files get this suffix; skipped when pairing


def run(cmd):
    """Run a command, raising a readable error on failure."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("command failed: " + ' '.join(str(c) for c in cmd)
                           + "\n" + r.stderr.strip())
    return r.stdout


def missing_tools():
    for tool in ('ffmpeg', 'ffprobe', 'recut'):
        if subprocess.run(['which', tool], capture_output=True).returncode != 0:
            yield tool


def ffprobe_info(path):
    out = run(['ffprobe', '-v', 'error', '-show_entries',
               'format=duration:stream=codec_type,sample_rate,r_frame_rate',
               '-of', 'json', path])
    d = json.loads(out)
    info = {'duration': float(d.get('format', {}).get('duration', 0.0)),
            'has_video': False, 'has_audio': False, 'fps': 30.0, 'sample_rate': 48000}
    for s in d.get('streams', []):
        if s.get('codec_type') == 'video' and not info['has_video']:
            info['has_video'] = True
            num, _, den = s.get('r_frame_rate', '30/1').partition('/')
            try:
                info['fps'] = float(num) / float(den) if float(den) else 30.0
            except (ValueError, ZeroDivisionError):
                info['fps'] = 30.0
        if s.get('codec_type') == 'audio' and not info['has_audio']:
            info['has_audio'] = True
            info['sample_rate'] = int(s.get('sample_rate', 48000))
    return info


def load_envelope(path, tmp, tag, fs=8000, env_rate=1000):
    """Extract mono audio and return a smoothed speech-energy envelope.

    The envelope (rectified, smoothed amplitude) is what makes alignment robust:
    two different mics in the same room have very different timbre, but the
    *energy over time* of the speech tracks together almost perfectly.
    """
    wav = os.path.join(tmp, tag + '.wav')
    run(['ffmpeg', '-y', '-v', 'error', '-i', path, '-vn',
         '-ac', '1', '-ar', str(fs), '-c:a', 'pcm_s16le', wav])
    w = wave.open(wav, 'rb')
    raw = w.readframes(w.getnframes())
    w.close()
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    if data.size == 0:
        raise RuntimeError("no audio samples in " + os.path.basename(path))
    x = np.abs(data)
    win = max(1, fs // 100)                       # 10 ms smoothing window
    c = np.cumsum(np.insert(x, 0, 0.0))
    x = (c[win:] - c[:-win]) / win
    step = max(1, fs // env_rate)
    return x[::step], fs // step


def find_offset(video, audio, tmp):
    """Return (offset_seconds, correlation_r, peak_clarity).

    offset > 0 means the external audio's content starts that many seconds into
    the video — i.e. the external recorder was started after the screen capture.
    offset < 0 means the external recorder was started first.
    """
    ve, fe = load_envelope(video, tmp, 'vid')
    ae, _ = load_envelope(audio, tmp, 'aud')
    v = ve - ve.mean()
    a = ae - ae.mean()
    nfft = 1 << ((len(v) + len(a) - 1).bit_length())
    cc = np.fft.irfft(np.fft.rfft(v, nfft) * np.conj(np.fft.rfft(a, nfft)), nfft)
    neg = cc[nfft - (len(a) - 1):] if len(a) > 1 else np.empty(0)
    full = np.concatenate((neg, cc[:len(v)]))
    lags = np.arange(-(len(a) - 1), len(v))
    k = int(np.argmax(full))
    lag_s = lags[k] / fe
    # peak clarity: how far the winning lag beats the next-best lag >0.5s away
    guard = full.copy()
    guard[max(0, k - fe // 2):k + fe // 2] = -np.inf
    clarity = float(full[k] / max(np.max(guard), 1e-9))
    # verified correlation of the two envelopes once shifted to the chosen offset
    d = int(round(lag_s * fe))
    if d >= 0:
        x, y = ve[d:], ae[:len(ve) - d]
    else:
        x, y = ve[:len(ae) + d], ae[-d:]
    m = min(len(x), len(y))
    r = float(np.corrcoef(x[:m], y[:m])[0, 1]) if m > 10 else 0.0
    return lag_s, r, clarity


def combine(video, audio, offset_s, out_path, codec):
    """Mux video + offset-corrected audio into one file, dropping the video's
    own scratch audio. Video is stream-copied (lossless, instant)."""
    sr = ffprobe_info(audio)['sample_rate']
    samples = int(round(abs(offset_s) * sr))
    if offset_s >= 0:                              # external audio started late: pad its front
        af = "[1:a]adelay=%dS:all=1[a]" % samples
    else:                                          # external audio started early: trim its front
        af = "[1:a]atrim=start_sample=%d,asetpts=N/SR/TB[a]" % samples
    run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-i', audio,
         '-filter_complex', af, '-map', '0:v', '-map', '[a]',
         '-c:v', 'copy', '-c:a', codec, '-shortest', out_path])


def verify(xml_path):
    """Print a sanity summary of the recut XML so the result can be trusted
    without opening Premiere."""
    seq = ET.parse(xml_path).getroot().find('sequence')
    if seq is None:
        print("  (could not read sequence from XML)")
        return
    fps = 30.0
    rate = seq.find('rate/timebase')
    if rate is not None and rate.text:
        fps = float(rate.text)
    vt = seq.find('media/video/track')
    at = seq.find('media/audio/track')
    if vt is None or at is None:
        print("  (XML has no video/audio track to verify)")
        return

    def spans(track):
        return [(int(c.find('start').text), int(c.find('end').text),
                 c.find('name').text) for c in track.findall('clipitem')]

    v, a = spans(vt), spans(at)
    mism = sum(1 for x, y in zip(v, a) if x[:2] != y[:2])
    lens = sorted(e - s for s, e, _ in v)
    med = lens[len(lens) // 2] if lens else 0
    tiny = sum(1 for l in lens if l < 8)           # < ~0.25s at 30fps
    total = int(seq.find('duration').text)
    print("  clips: %d video / %d audio   video/audio mismatches: %d"
          % (len(v), len(a), mism))
    print("  median clip %.2fs   choppy (<0.25s): %d%%"
          % (med / fps, (100 * tiny / len(lens)) if lens else 0))
    print("  timeline: %d:%02d min" % (total / fps // 60, total / fps % 60))
    prev = None
    for s, e, nm in v:
        if prev and nm != prev:
            print("  '%s' ends -> '%s' starts at %d:%02d"
                  % (prev, nm, s / fps // 60, s / fps % 60))
        prev = nm
    if lens and tiny / len(lens) > 0.10:
        print("  ! looks choppy — re-run with a larger --min-silence (e.g. 0.8)")
    if mism:
        print("  ! video/audio clip mismatch — unexpected; inspect the XML")


def trailing_int(path):
    nums = re.findall(r'\d+', os.path.splitext(os.path.basename(path))[0])
    return int(nums[-1]) if nums else None


def discover_pairs(directory):
    """Find video+audio pairs in a folder. Pair by trailing number when the
    filenames carry one (Loom Recording 1 <-> Audio 1); otherwise by sorted
    order. Audacity .aup3 projects are ignored — they aren't playable media."""
    files = sorted(glob.glob(os.path.join(directory, '*')))
    vids = [f for f in files if f.lower().endswith(VIDEO_EXTS)
            and not f.endswith(SYNCED_SUFFIX)]
    auds = [f for f in files if f.lower().endswith(AUDIO_EXTS)]
    if not vids or not auds:
        sys.exit("error: need at least one video and one audio file in %s\n"
                 "  videos: %d   audio: %d\n"
                 "  (Audacity .aup3 projects are ignored — export a .wav first)"
                 % (directory, len(vids), len(auds)))
    if len(vids) != len(auds):
        sys.exit("error: %d video(s) but %d audio file(s) — can't auto-pair.\n"
                 "  Use --pair VIDEO AUDIO for each pair instead."
                 % (len(vids), len(auds)))
    vmap = {trailing_int(v): v for v in vids}
    amap = {trailing_int(a): a for a in auds}
    if None not in vmap and None not in amap and set(vmap) == set(amap):
        return [(vmap[n], amap[n]) for n in sorted(vmap)]
    return list(zip(vids, auds))                   # fall back to sorted order


def main():
    ap = argparse.ArgumentParser(
        description="Sync external audio to screen recordings, combine, "
                    "silence-cut, and export one Premiere XML.")
    ap.add_argument('directory', nargs='?',
                    help="folder containing the video + audio pairs")
    ap.add_argument('--pair', nargs=2, action='append', metavar=('VIDEO', 'AUDIO'),
                    help="an explicit video+audio pair (repeatable)")
    ap.add_argument('-o', '--output', help="output XML path")
    ap.add_argument('-n', '--name', default='Sync and Cut',
                    help="Premiere sequence name")
    ap.add_argument('--sync-only', action='store_true',
                    help="stop after combining — skip silence removal")
    ap.add_argument('--min-silence', type=float, default=0.6,
                    help="recut: shortest pause to cut, in seconds (default 0.6)")
    ap.add_argument('--padding', type=float, default=0.15,
                    help="recut: breathing room kept around speech (default 0.15)")
    ap.add_argument('--audio-codec', default='pcm_s24le',
                    help="codec for the combined file's audio (default pcm_s24le)")
    ap.add_argument('--work-dir',
                    help="where to write combined .mov + XML (default: source folder)")
    args = ap.parse_args()

    miss = list(missing_tools())
    if miss:
        sys.exit("error: missing required tool(s): " + ', '.join(miss))

    if args.pair:
        pairs = [(os.path.abspath(v), os.path.abspath(a)) for v, a in args.pair]
        base = os.path.dirname(pairs[0][0])
    elif args.directory:
        base = os.path.abspath(args.directory)
        pairs = discover_pairs(base)
    else:
        sys.exit("error: give a directory, or one or more --pair VIDEO AUDIO")

    work_dir = os.path.abspath(args.work_dir) if args.work_dir else base
    os.makedirs(work_dir, exist_ok=True)

    print("Found %d recording pair(s).\n" % len(pairs))
    combined = []
    for i, (video, audio) in enumerate(pairs, 1):
        vname, aname = os.path.basename(video), os.path.basename(audio)
        print("[%d/%d] %s  +  %s" % (i, len(pairs), vname, aname))
        if not ffprobe_info(video)['has_audio']:
            sys.exit("  error: %s has no audio track to sync against" % vname)
        with tempfile.TemporaryDirectory() as tmp:
            offset, r, clarity = find_offset(video, audio, tmp)
        flag = "" if r >= 0.5 else "   <-- LOW CONFIDENCE, check this pair"
        print("  offset %+.3fs   confidence r=%.3f   clarity %.1fx%s"
              % (offset, r, clarity, flag))
        out_mov = os.path.join(work_dir, os.path.splitext(vname)[0] + SYNCED_SUFFIX)
        combine(video, audio, offset, out_mov, args.audio_codec)
        print("  -> %s\n" % os.path.basename(out_mov))
        combined.append(out_mov)

    if args.sync_only:
        print("Sync-only: combined file(s) written. Import the .mov file(s) "
              "straight into Premiere — video and clean audio are already locked.")
        return

    out_xml = os.path.abspath(args.output) if args.output \
        else os.path.join(work_dir, 'sync-and-cut.xml')
    print("Silence-cutting with recut (min-silence %.2fs, padding %.2fs)..."
          % (args.min_silence, args.padding))
    # recut options are stateful and must precede the files they apply to.
    run(['recut', '--min-silence', str(args.min_silence),
         '--padding', str(args.padding)] + combined
        + ['-n', args.name, '-o', out_xml])
    print("\nWrote %s\n" % out_xml)
    verify(out_xml)
    print("\nImport %s into Premiere (File -> Import). Keep the (synced).mov "
          "files where they are — the XML points at them."
          % os.path.basename(out_xml))


if __name__ == '__main__':
    main()
