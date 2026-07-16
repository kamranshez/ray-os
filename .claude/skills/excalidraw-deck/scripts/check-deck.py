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

    headlines = re.findall(r"headline:\s*'((?:[^'\\]|\\.)*)'", body)
    headlines += re.findall(r'headline:\s*"((?:[^"\\]|\\.)*)"', body)
    print(f"slides: {len(headlines)}")
    for i, h in enumerate(headlines, 1):
        print(f"  {i:>2}. {h}")

if __name__ == "__main__":
    main()
