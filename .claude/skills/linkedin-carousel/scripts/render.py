#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.45"]
# ///
"""
Render a LinkedIn carousel from a JSON spec into PNG slides.

Spec schema:
  {
    "title": "skill-system-upgrade",          # used for output dir slug
    "size": [1080, 1350],                       # optional; default 1080x1350 (4:5)
    "name": "Ray Amjad",                        # optional; default "Ray Amjad"
    "handle": "@rayamjad",                      # optional; default "@rayamjad"
    "slides": [
      {"type": "cover",   "headline": "..."},
      {"type": "content", "headline": "...", "subtitle": "..."},
      {"type": "cta",     "headline": "Follow for more...", "subtitle": "...", "button": "Follow @rayamjad"}
    ]
  }

Usage:
  uv run scripts/render.py path/to/spec.json [--out /tmp/linkedin-carousel-<slug>]
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = SKILL_DIR / "assets" / "profile.png"

# Twitter-style verified blue checkmark.
VERIFIED_SVG = """<svg viewBox="0 0 22 22" aria-label="Verified" role="img">
  <g><path fill="#1D9BF0" d="M20.396 11c-.018-.646-.215-1.275-.57-1.816-.354-.54-.852-.972-1.438-1.246.223-.607.27-1.264.14-1.897-.131-.634-.437-1.218-.882-1.687-.47-.445-1.053-.75-1.687-.882-.633-.13-1.29-.083-1.897.14-.273-.587-.704-1.086-1.245-1.44S11.647 1.62 11 1.604c-.646.017-1.273.213-1.813.568s-.969.854-1.24 1.44c-.608-.223-1.267-.272-1.902-.14-.635.13-1.22.436-1.69.882-.445.47-.749 1.055-.878 1.688-.13.633-.08 1.29.144 1.896-.587.274-1.087.705-1.443 1.245-.356.54-.555 1.17-.574 1.817.02.647.218 1.276.574 1.817.356.54.856.972 1.443 1.245-.224.606-.274 1.263-.144 1.896.13.634.433 1.218.877 1.688.47.443 1.054.747 1.687.878.633.132 1.29.084 1.897-.136.274.586.705 1.084 1.246 1.439.54.354 1.17.551 1.816.569.647-.016 1.276-.213 1.817-.567s.972-.854 1.245-1.44c.604.239 1.266.296 1.903.164.636-.132 1.22-.447 1.68-.907.46-.46.776-1.044.908-1.681s.075-1.299-.165-1.903c.586-.274 1.084-.705 1.439-1.246.354-.54.551-1.17.569-1.816zM9.662 14.85l-3.429-3.428 1.293-1.302 2.072 2.072 4.4-4.794 1.347 1.246z"/></g>
</svg>"""


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "carousel"


def build_html(slide: dict, *, idx: int, total: int, name: str, handle: str,
               profile_data_url: str, width: int, height: int) -> str:
    stype = slide.get("type", "content")
    headline = slide.get("headline", "")
    subtitle = slide.get("subtitle", "")
    button = slide.get("button", f"Follow {handle}")
    counter = f"{idx} / {total}"

    profile_chip = f"""
      <div class="chip">
        <img class="chip-avatar" src="{profile_data_url}" alt="" />
        <div class="chip-text">
          <div class="chip-name">{name}<span class="chip-check">{VERIFIED_SVG}</span></div>
          <div class="chip-handle">{handle}</div>
        </div>
      </div>
    """

    if stype == "cover":
        body = f"""
        <header class="row">
          <div></div>
          <div class="counter">{counter}</div>
        </header>
        <main class="cover-main">
          <h1 class="headline cover-headline">{headline}</h1>
          <div class="accent"></div>
          {profile_chip}
        </main>
        <footer class="row">
          <div class="footer-handle">{handle}</div>
          <div class="swipe">Swipe →</div>
        </footer>
        """
    elif stype == "cta":
        body = f"""
        <header class="row">
          <div></div>
          <div class="counter">{counter}</div>
        </header>
        <main class="cta-main">
          <img class="cta-avatar" src="{profile_data_url}" alt="" />
          <div class="cta-name">{name}<span class="chip-check">{VERIFIED_SVG}</span></div>
          <div class="cta-handle">{handle}</div>
          <div class="cta-divider"></div>
          <h1 class="headline cta-headline">{headline}</h1>
          {f'<p class="subtitle cta-subtitle">{subtitle}</p>' if subtitle else ''}
          <button class="cta-button">{button}</button>
        </main>
        <footer class="row">
          <div class="footer-handle">{handle}</div>
          <div></div>
        </footer>
        """
    else:  # content
        body = f"""
        <header class="row">
          {profile_chip}
          <div class="counter">{counter}</div>
        </header>
        <main class="content-main">
          <h1 class="headline">{headline}</h1>
          {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
        </main>
        <footer class="row">
          <div class="footer-handle">{handle}</div>
          <div></div>
        </footer>
        """

    return f"""<!doctype html>
<html><head><meta charset="utf-8" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --ink: #0F1419;
    --muted: #536471;
    --line: #EFF3F4;
    --blue: #1D9BF0;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; }}
  body {{
    width: {width}px; height: {height}px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #fff; color: var(--ink);
    -webkit-font-smoothing: antialiased;
    text-rendering: geometricPrecision;
  }}
  .slide {{
    width: 100%; height: 100%;
    padding: 56px 64px;
    display: flex; flex-direction: column;
  }}
  .row {{ display: flex; justify-content: space-between; align-items: center; }}
  .counter {{ color: var(--muted); font-size: 22px; font-weight: 500; }}
  .footer-handle {{ color: var(--muted); font-size: 22px; font-weight: 500; }}
  .swipe {{ color: var(--blue); font-size: 22px; font-weight: 600; }}

  /* Profile chip */
  .chip {{ display: flex; align-items: center; gap: 14px; }}
  .chip-avatar {{ width: 60px; height: 60px; border-radius: 50%; }}
  .chip-text {{ display: flex; flex-direction: column; line-height: 1.15; }}
  .chip-name {{ font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 6px; }}
  .chip-handle {{ font-size: 20px; color: var(--muted); font-weight: 500; }}
  .chip-check {{ display: inline-flex; width: 22px; height: 22px; }}
  .chip-check svg {{ width: 100%; height: 100%; }}

  /* Headlines */
  .headline {{
    font-weight: 800; letter-spacing: -0.02em; line-height: 1.05;
    color: var(--ink); margin: 0;
  }}
  .subtitle {{
    color: var(--muted); font-weight: 500; line-height: 1.35;
    margin: 24px 0 0 0;
  }}

  /* Cover */
  .cover-main {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
  .cover-headline {{ font-size: 96px; font-weight: 900; }}
  .accent {{ width: 80px; height: 6px; background: var(--blue); border-radius: 3px; margin: 36px 0 48px; }}

  /* Content */
  .content-main {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
  .content-main .headline {{ font-size: 80px; }}
  .content-main .subtitle {{ font-size: 36px; }}

  /* CTA */
  .cta-main {{
    flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center;
  }}
  .cta-avatar {{ width: 140px; height: 140px; border-radius: 50%; }}
  .cta-name {{ font-size: 36px; font-weight: 700; margin-top: 20px; display: flex; align-items: center; gap: 8px; }}
  .cta-handle {{ font-size: 28px; color: var(--muted); font-weight: 500; margin-top: 4px; }}
  .cta-divider {{ width: 80px; height: 1px; background: var(--line); margin: 36px 0; }}
  .cta-headline {{ font-size: 64px; max-width: 820px; }}
  .cta-subtitle {{ font-size: 30px; max-width: 760px; }}
  .cta-button {{
    margin-top: 48px; padding: 22px 48px; font-size: 28px; font-weight: 700;
    background: var(--ink); color: #fff; border: none; border-radius: 999px;
    font-family: inherit; cursor: default;
  }}
</style></head>
<body><div class="slide">{body}</div></body></html>
"""


def png_to_data_url(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def ensure_chromium() -> None:
    """Install Playwright's chromium if missing. Idempotent and quiet on success."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                b = p.chromium.launch()
                b.close()
                return
            except Exception:
                pass
    except Exception:
        pass
    print("Installing Playwright chromium (one-time)...", file=sys.stderr)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def render(spec_path: Path, out_dir: Path | None) -> Path:
    spec = json.loads(spec_path.read_text())
    title = spec.get("title") or spec_path.stem
    width, height = spec.get("size", [1080, 1350])
    name = spec.get("name", "Ray Amjad")
    handle = spec.get("handle", "@rayamjad")
    profile_path = Path(spec.get("profile", DEFAULT_PROFILE)).expanduser()
    if not profile_path.exists():
        raise SystemExit(
            f"profile image missing: {profile_path}\n"
            f"run: uv run {SKILL_DIR}/scripts/prep_profile.py"
        )

    slides = spec.get("slides", [])
    if not slides:
        raise SystemExit("spec has no slides")

    if out_dir is None:
        out_dir = Path(f"/tmp/linkedin-carousel-{slugify(title)}")
    out_dir.mkdir(parents=True, exist_ok=True)

    profile_data_url = png_to_data_url(profile_path)

    ensure_chromium()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2,  # crisp text
        )
        page = context.new_page()
        for i, slide in enumerate(slides, start=1):
            html = build_html(
                slide, idx=i, total=len(slides), name=name, handle=handle,
                profile_data_url=profile_data_url, width=width, height=height,
            )
            page.set_content(html, wait_until="networkidle")
            # Let webfonts settle.
            page.wait_for_timeout(200)
            out_path = out_dir / f"slide-{i}.png"
            page.screenshot(path=str(out_path), full_page=False, omit_background=False,
                            clip={"x": 0, "y": 0, "width": width, "height": height})
            print(f"wrote {out_path}")
        browser.close()
    return out_dir


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", type=Path, help="path to spec.json")
    ap.add_argument("--out", type=Path, default=None, help="output dir (default /tmp/linkedin-carousel-<slug>)")
    args = ap.parse_args()
    out = render(args.spec, args.out)
    print(f"\ncarousel -> {out}")


if __name__ == "__main__":
    main()
