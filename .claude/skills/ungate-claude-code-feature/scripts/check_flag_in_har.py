#!/usr/bin/env python3
"""Check whether a GrowthBook flag is present in a Proxyman HAR export of the
Claude Code /api/eval/sdk-* flow, and print its forced value.

Usage:
    python3 check_flag_in_har.py <export.har> <flag-name>

Proxyman HAR exports store the response body base64-encoded; the decoded payload
may also be gzip/deflate compressed. This script handles all of that, then
locates the flag inside the GrowthBook `features` map and reports whether the
value looks injected (source "force" + ruleId null) or is the real server value.

Exit code 0 = flag found, 1 = flag absent / no eval flow, 2 = bad usage.
"""
import sys
import json
import base64
import gzip
import zlib


def decode_body(content):
    """Return the response body as text, handling base64 + gzip/deflate."""
    text = content.get("text", "")
    if not text:
        return ""
    raw = base64.b64decode(text) if content.get("encoding") == "base64" else text.encode()
    for fn in (
        lambda d: gzip.decompress(d),
        lambda d: zlib.decompress(d),
        lambda d: zlib.decompress(d, -zlib.MAX_WBITS),
        lambda d: d,
    ):
        try:
            return fn(raw).decode("utf-8", "replace")
        except Exception:
            continue
    return ""


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    har_path, flag = sys.argv[1], sys.argv[2]

    with open(har_path) as fh:
        har = json.load(fh)

    entries = har.get("log", {}).get("entries", [])
    eval_entries = [e for e in entries if "/api/eval/" in e["request"]["url"]]
    if not eval_entries:
        print("NO /api/eval/ FLOW in this HAR.")
        print("Capture a Claude Code session running through the proxy first.")
        sys.exit(1)

    found = False
    for e in eval_entries:
        url = e["request"]["url"]
        body = decode_body(e["response"]["content"])
        try:
            data = json.loads(body)
        except Exception:
            print(f"  could not parse response body for {url}")
            continue
        feats = data.get("features", {})
        if flag in feats:
            found = True
            f = feats[flag]
            val = f.get("value", f.get("defaultValue"))
            injected = f.get("source") == "force" and f.get("ruleId") is None
            print(f"FOUND  {flag}")
            print(f"  value   = {json.dumps(val)}")
            print(f"  on/off  = {f.get('on')}/{f.get('off')}")
            print(f"  source  = {f.get('source')}   ruleId = {f.get('ruleId')}")
            print(f"  injected by Proxyman rule: "
                  f"{'YES' if injected else 'NO (this is the real server value)'}")
        else:
            print(f"ABSENT {flag}  (not in features map of {url})")

    sys.exit(0 if found else 1)


if __name__ == "__main__":
    main()
