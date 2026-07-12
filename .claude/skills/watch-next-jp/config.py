"""Config + data-dir resolution for the standalone recommender.

Everything is optional. With no config.json at all, the tool stores its
discovery database and reads your taste file from `./data/` next to this
package. Override the location three ways (first wins):

    1. --config path/to/config.json   (a JSON file with {"data_dir": "..."})
    2. HARVEST_DATA_DIR env var
    3. the built-in default: <package>/data

config.json may also carry a `discover` block to tune the format blocklist:

    {
      "data_dir": "~/recommender-data",
      "discover": {
        "format_blocklist": ["ゆっくり解説", "voiceroid", ...],
        "channel_blocklist": ["UCxxxx", ...]
      }
    }

Leave `format_blocklist` out to keep the built-in synthetic-TTS default in
harvest.py; set it to `[]` to disable format filtering entirely.
"""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_config(path=None):
    cfg_path = Path(path) if path else ROOT / "config.json"
    cfg = {}
    if cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)

    data_dir = (os.environ.get("HARVEST_DATA_DIR")
                or cfg.get("data_dir")
                or str(ROOT / "data"))
    cfg["data_dir"] = str(Path(data_dir).expanduser())
    cfg.setdefault("taste_file", str(Path(cfg["data_dir"]) / "taste.json"))
    cfg["taste_file"] = str(Path(cfg["taste_file"]).expanduser())
    return cfg
