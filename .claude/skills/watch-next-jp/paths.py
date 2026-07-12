"""Resolve external binaries (yt-dlp) from PATH.

This package shells out to yt-dlp for `search` + the speech gate; install it
from the system (`brew install yt-dlp`, `pipx install yt-dlp`, or your package
manager). `_NOWWIN` is kept so callers can spread `**_NOWWIN` into
subprocess.run unconditionally — it suppresses the console window on Windows
and is a no-op elsewhere.
"""

import shutil
import subprocess
import sys
from functools import lru_cache

_NOWWIN: dict = (
    {"creationflags": subprocess.CREATE_NO_WINDOW}
    if sys.platform == "win32"
    else {}
)


@lru_cache(maxsize=None)
def _resolve(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    raise FileNotFoundError(
        f"'{name}' not found on PATH — install it (e.g. brew install {name})"
    )


def ytdlp_path() -> str:
    return _resolve("yt-dlp")


def ytdlp_extra_args() -> list:
    """Extra args prepended to every yt-dlp call (none for system installs)."""
    return []
