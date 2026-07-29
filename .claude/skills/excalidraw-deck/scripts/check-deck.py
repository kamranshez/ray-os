#!/usr/bin/env python3
"""Sanity-check an excalidraw-deck HTML file.

Extracts the inline <script> that drives the deck, runs `node --check` on it,
and lists each slide's headline so you can eyeball the narrative order without
opening a browser. Run this after every edit, before declaring a deck done.

Usage:
    python3 check-deck.py path/to/deck.html
"""
import re, subprocess, sys, tempfile, os

def main():
    if len(sys.argv) != 2:
        print("usage: check-deck.py <deck.html>"); sys.exit(2)
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()

    # The deck logic lives in the LAST <script> block (the IIFE). The earlier
    # ones load rough.js from a CDN and have no inline body to check.
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    body = next((s for s in reversed(scripts) if "slides" in s), None)
    if not body:
        print("no inline deck script found (expected a <script> mentioning `slides`)")
        sys.exit(1)

    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(body); tmp = f.name
    try:
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode != 0:
            print("JS SYNTAX ERROR:\n" + (r.stderr or r.stdout)); sys.exit(1)
    finally:
        os.unlink(tmp)
    print("node --check: ok")

    # --- picker deck: V('1A', 'headline', ...) grouped by slide number ---
    variations = re.findall(r"V\(\s*'(\d+[A-Z])'\s*,\s*'((?:[^'\\]|\\.)*)'", body)
    if variations:
        groups = {}
        for tag, hl in variations:
            groups.setdefault(int(re.match(r"\d+", tag).group()), []).append((tag, hl))
        m = re.search(r"const TITLES\s*=\s*\[(.*?)\n\s*\];", body, re.S)
        titles = re.findall(r"'((?:[^'\\]|\\.)*)'", m.group(1)) if m else []
        print(f"picker: {len(variations)} variations across {len(groups)} slides")
        if titles and len(titles) != len(groups):
            print(f"  WARNING: TITLES has {len(titles)} entries but tags cover {len(groups)} slides")
        thin = [g for g, v in groups.items() if len(v) < 3]
        if thin:
            print(f"  WARNING: slides with fewer than 3 variations: {thin}")
        for g in sorted(groups):
            name = titles[g-1] if g <= len(titles) else "(no TITLES entry)"
            print(f"  {g:>2}. {name}  [{len(groups[g])} variations]")
            for tag, hl in groups[g]:
                print(f"       {tag}  {hl}")
        return

    # --- plain linear deck: slides.push({ headline: '...' }) ---
    headlines = re.findall(r"headline:\s*'((?:[^'\\]|\\.)*)'", body)
    headlines += re.findall(r'headline:\s*"((?:[^"\\]|\\.)*)"', body)
    print(f"slides: {len(headlines)}")
    for i, h in enumerate(headlines, 1):
        print(f"  {i:>2}. {h}")

if __name__ == "__main__":
    main()
