"""Load KEY=VALUE pairs from the skill's .env into os.environ.

Real env vars win — .env is a fallback so the skill works without polluting ~/.zshrc.
No external dependency (avoids needing python-dotenv).
"""
import os
import sys
from pathlib import Path

# Gemini API key formats that are PERMANENT (as opposed to a `ya29.…` OAuth access
# token, which expires in ~1h and must never be used for a batch TTS run):
#   AQ.…     authorization key, 53 chars, bound to a service account. What AI Studio
#            issues for every new key now — this is the format to prefer.
#   AIzaSy…  legacy standard key. Still works, but the Gemini API stops accepting
#            standard keys in September 2026.
PERMANENT_KEY_PREFIXES = ("AQ.", "AIza")


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
    if not k.startswith(PERMANENT_KEY_PREFIXES):
        print("  ⚠ GEMINI_API_KEY doesn't look like a permanent Gemini API key (expected\n"
              "    'AQ.…' or 'AIzaSy…'). If it's an OAuth access token it will 401 once it\n"
              "    expires. Get a key at https://aistudio.google.com/apikey.", file=sys.stderr)
    return True


def require_healthy_gemini_key():
    """Hard pre-flight for any script about to WRITE explanation TTS onto cards.

    A genuinely ephemeral OAuth access token (`ya29.…`) dies within ~1h, and the fix
    modes' best-effort TTS then half-fixes a whole batch: the explanation TEXT lands,
    the audio silently doesn't, and nothing surfaces it until Ray studies the cards.
    (July 2026: this is exactly how a batch ran with a token instead of a key.) So
    refuse up front, before anything is written — a 2-second failure beats a silently
    audio-less batch. Best-effort still covers genuinely mid-run failures.

    **`AQ.` keys are PERMANENT.** This check used to reject them as ephemeral and that
    was wrong — it blocked a whole leech run on 2026-07-28 over a key that had been
    sitting unchanged in .env since 16 June and still worked. `AQ.` is Google's newer
    *authorization key* format (53 chars, bound to a service account), and AI Studio
    now issues ONLY `AQ.` keys for new keys. The old `AIzaSy` "standard" keys are the
    ones being retired: the Gemini API stops accepting them in September 2026. So the
    guard was refusing the modern format and recommending the doomed one.
    https://ai.google.dev/gemini-api/docs/api-key
    """
    k = os.environ.get("GEMINI_API_KEY", "")
    if k.startswith(PERMANENT_KEY_PREFIXES):
        return
    if k and os.environ.get("SM_ALLOW_EPHEMERAL_GEMINI_KEY") == "1":
        print("  ⚠ Running on an ephemeral GEMINI_API_KEY (SM_ALLOW_EPHEMERAL_GEMINI_KEY=1)."
              " It can expire mid-run; check the summary for missing audio.", file=sys.stderr)
        return
    if not k:
        sys.exit("GEMINI_API_KEY is not set. Add it to <skill-dir>/.env — get a key at "
                 "https://aistudio.google.com/apikey (a new key looks like 'AQ.…').")
    sys.exit("GEMINI_API_KEY isn't a recognised permanent Gemini API key (expected an "
             "'AQ.…' auth key, or a legacy 'AIzaSy…' standard key).\nRefusing to start: if "
             "this is an OAuth access token, TTS would die mid-run and leave cards with "
             "explanation text but NO audio, silently.\nGet a key at "
             "https://aistudio.google.com/apikey.\n(Override for a deliberate short run: "
             "SM_ALLOW_EPHEMERAL_GEMINI_KEY=1.)")
