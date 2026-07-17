"""Load KEY=VALUE pairs from the skill's .env into os.environ.

Real env vars win — .env is a fallback so the skill works without polluting ~/.zshrc.
No external dependency (avoids needing python-dotenv).
"""
import os
import sys
from pathlib import Path


def load_skill_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def warn_if_ephemeral_gemini_key():
    """A permanent Gemini API key looks like `AIza…`. Anything else (e.g. an OAuth
    access token `AQ.…`/`ya29.…`) expires in ~1h and will 401 mid-run. Warn so the
    user swaps in a permanent key for unattended use. Returns True if the key is set."""
    k = os.environ.get("GEMINI_API_KEY", "")
    if not k:
        return False
    if not k.startswith("AIza"):
        print("  ⚠ GEMINI_API_KEY looks like a temporary OAuth token (expires ~1h), not a\n"
              "    permanent API key. TTS will 401 once it expires. Get a permanent key at\n"
              "    https://aistudio.google.com/apikey (looks like 'AIzaSy…').", file=sys.stderr)
    return True


def require_healthy_gemini_key():
    """Hard pre-flight for any script about to WRITE explanation TTS onto cards.

    An ephemeral OAuth token (`AQ.…`/`ya29.…`) predictably dies within ~1h, and the
    fix modes' best-effort TTS then half-fixes a whole batch: the explanation TEXT
    lands, the audio silently doesn't, and nothing surfaces it until Ray studies the
    cards. (July 2026: this is exactly how a batch ran with a token instead of a key.)
    So refuse up front, before anything is written — a 2-second failure beats a
    silently audio-less batch. Best-effort still covers genuinely mid-run failures.

    `SM_ALLOW_EPHEMERAL_GEMINI_KEY=1` overrides for a deliberate short run on a
    fresh token."""
    k = os.environ.get("GEMINI_API_KEY", "")
    if k.startswith("AIza"):
        return
    if k and os.environ.get("SM_ALLOW_EPHEMERAL_GEMINI_KEY") == "1":
        print("  ⚠ Running on an ephemeral GEMINI_API_KEY (SM_ALLOW_EPHEMERAL_GEMINI_KEY=1)."
              " It can expire mid-run; check the summary for missing audio.", file=sys.stderr)
        return
    if not k:
        sys.exit("GEMINI_API_KEY is not set. Add it to <skill-dir>/.env — get a key at "
                 "https://aistudio.google.com/apikey (looks like 'AIzaSy…').")
    sys.exit("GEMINI_API_KEY looks like a temporary OAuth token (expires ~1h), not a "
             "permanent API key.\nRefusing to start: TTS would die mid-run and leave cards "
             "with explanation text but NO audio, silently.\nGet a permanent key at "
             "https://aistudio.google.com/apikey (looks like 'AIzaSy…') and put it in "
             "<skill-dir>/.env.\n(Override for a deliberate short run: "
             "SM_ALLOW_EPHEMERAL_GEMINI_KEY=1.)")
