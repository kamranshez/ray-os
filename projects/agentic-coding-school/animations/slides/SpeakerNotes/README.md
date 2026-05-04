# SpeakerNotes

A macOS SwiftUI speaker-notes app that's invisible to screen recorders. Reads
and writes the shared `notes.json` next to it, and runs a tiny HTTP server on
`localhost:7878` so the slide deck (`goal-vs-ralph-slides.html`) stays in sync.

## Build & run

```bash
cd projects/agentic-coding-school/animations/slides/SpeakerNotes
swift build -c release
# run from the slides/ folder so notes.json resolves
cd ..
./SpeakerNotes/.build/release/SpeakerNotes
```

If you'd rather use Xcode, open `Package.swift` directly:

```bash
open Package.swift
```

(Make sure the working directory contains `notes.json` — the binary searches
`./notes.json`, `../notes.json`, then `../../notes.json`. Override with
`SPEAKER_NOTES_PATH=/abs/path/to/notes.json`.)

## How "invisible" works

`NSWindow.sharingType = .none` excludes the window from screen captures.
Both ScreenCaptureKit (the modern macOS framework used by QuickTime, Loom,
Screen Studio, Riverside, OBS via the `SCKit` source on macOS 12.3+) and
the legacy `CGWindowListCopyWindowInfo`-based capture path respect this.
Recordings will see the slide deck behind it but not the notes window.

## Verify it's invisible

1. Launch the app: `./SpeakerNotes/.build/release/SpeakerNotes`
2. Start a screen recording in QuickTime (File → New Screen Recording).
3. Wave the SpeakerNotes window around. The recorded video will show
   only the desktop / slide deck behind it, not the notes window.
4. Same with OBS using "macOS Screen Capture" (the SCKit backend).

If you see the window in the recording, double-check you launched the
release build (debug builds occasionally inherit different entitlements
under sandboxing). On macOS 14+ you may also need to grant Screen
Recording permission to the recorder app once.

## Sync with the slide deck

The slide deck polls `notes.json` every second (relative URL — works
under `file://` for content, but you'll want to serve it over HTTP for
the POST sync to work without CORS issues):

```bash
cd projects/agentic-coding-school/animations/slides
python3 -m http.server 8080
# open http://localhost:8080/goal-vs-ralph-slides.html
```

Arrow-key navigation in the deck POSTs to `http://localhost:7878/current`
which the SpeakerNotes app handles and writes back to `notes.json`.
Cmd+← and Cmd+→ in SpeakerNotes do the same in reverse — the file change
is picked up by the deck on the next 1s poll.

## Endpoints

- `GET  http://localhost:7878/current` → `{"current": N}`
- `POST http://localhost:7878/current` body `{"current": N}` → `{"ok": true}`
