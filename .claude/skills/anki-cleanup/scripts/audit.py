#!/usr/bin/env python3
"""Multi-angle audit of an Anki deck via AnkiConnect.

This script does the *gathering*, not the *thinking*. It pulls the deck apart from
several independent angles (lapses, leeches, ease distribution, maturity, spinning
cards, card format) and dumps the raw material so the model can spot high-level
patterns across the worst cards — semantic clusters, structural issues, format
mismatches, false positives. Stats come from cheap findCards COUNT queries; only
the worst offenders get a full cardsInfo pull.

Usage:
    python3 audit.py                         # list decks + card counts, then stop
    python3 audit.py --deck "My Deck"        # full multi-angle audit
    python3 audit.py --deck "My Deck" --lapse-floor 5 --max-detail 300 \
                     --output ~/Downloads/anki-cleanup/audit.json

Field detection: reuses the sentence-mining skill's config.json (field_map / decks)
when present, so "sentence" / "word" / "frequency" map correctly. Falls back to
heuristics (longest text field = sentence; a field named *freq*/*priority*/*rank* or
mostly-numeric = frequency) for arbitrary note types.
"""
import argparse, json, os, re, sys, urllib.request
from collections import Counter

ANKI_URL = "http://localhost:8765"


def anki(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    try:
        r = urllib.request.urlopen(ANKI_URL, body, timeout=60)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"AnkiConnect unreachable at {ANKI_URL} ({e}). Is Anki running with "
                 f"the AnkiConnect add-on? (sentence-mining/scripts/ensure_anki.sh launches it.)")
    out = json.load(r)
    if out.get("error"):
        sys.exit(f"AnkiConnect error on {action}: {out['error']}")
    return out["result"]


def load_sm_config():
    """Best-effort: read the sibling sentence-mining skill's config for field map + decks."""
    here = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(here, "..", "..", "sentence-mining", "config.json")
    try:
        with open(cfg_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {}


def strip_html(h):
    h = h or ""
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h).strip()


def count(query):
    return len(anki("findCards", query=query))


def deck_clause(deck):
    return f'deck:"{deck}"'


def pick_fields(sample, sm_fields):
    """Decide which fields hold the sentence / word / frequency, config first."""
    keys = list(sample["fields"].keys())
    sent = sm_fields.get("sentence") if sm_fields.get("sentence") in keys else None
    word = sm_fields.get("word") if sm_fields.get("word") in keys else None
    # Heuristic fallback for sentence: longest average text field across the sample.
    if not sent:
        sent = max(keys, key=lambda k: len(strip_html(sample["fields"][k]["value"])), default=None)
    if not word:
        word = keys[0] if keys else None
    # Frequency: a field named freq/priority/rank, else a mostly-numeric field.
    freq_fields = [k for k in keys if re.search(r"freq|priority|rank", k, re.I)]
    return word, sent, freq_fields


def parse_freq(val):
    t = strip_html(val)
    m = re.search(r"\d[\d,]*", t)
    return int(m.group(0).replace(",", "")) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", help="deck name to audit; omit to list decks")
    ap.add_argument("--lapse-floor", type=int, default=5,
                    help="min lapses for the detailed worst-offender pull (default 5)")
    ap.add_argument("--max-detail", type=int, default=300,
                    help="cap on cards pulled in full detail (default 300)")
    ap.add_argument("--output", default="~/Downloads/anki-cleanup/audit.json")
    args = ap.parse_args()

    sm = load_sm_config()
    global ANKI_URL
    ANKI_URL = sm.get("anki_connect_url", ANKI_URL)
    sm_fields = (sm.get("field_map") or {})

    if not args.deck:
        names = anki("deckNames")
        print("Decks (card counts):")
        rows = sorted(((n, count(deck_clause(n))) for n in names), key=lambda x: -x[1])
        for n, c in rows:
            print(f"  {c:>7}  {n}")
        print("\nRe-run with --deck \"<name>\" to audit one.")
        return

    d = deck_clause(args.deck)
    total = count(d)
    if total == 0:
        sys.exit(f'No cards in deck "{args.deck}". Check the name (run with no --deck to list).')

    # --- Angle 1: aggregate struggle signals (cheap count queries) ---
    reviewed = count(f"{d} -is:new")
    stats = {
        "total": total,
        "reviewed": reviewed,
        "new": count(f"{d} is:new"),
        "suspended": count(f"{d} is:suspended"),
        "leech_tagged": count(f"{d} tag:leech"),
        "lapses>=3": count(f"{d} prop:lapses>=3"),
        "lapses>=5": count(f"{d} prop:lapses>=5"),
        "lapses>=8": count(f"{d} prop:lapses>=8"),
        "at_ease_floor": count(f"{d} prop:ease<1.31"),
        "mature_but_lapsing(ivl>=100,lap>=4)": count(f"{d} prop:ivl>=100 prop:lapses>=4"),
        "spinning(reps>=15,ivl<14)": count(f"{d} prop:reps>=15 prop:ivl<14"),
        "due": count(f"{d} is:due"),
    }
    # Ease-floor red herring: if a big chunk of reviewed cards sit at the min ease,
    # ease/factor is a deck-settings artifact, not a struggle signal — flag it so the
    # model doesn't mistake "low ease" for "hard card".
    floor_frac = (stats["at_ease_floor"] / reviewed) if reviewed else 0
    ease_floor_artifact = floor_frac > 0.25

    # --- Angle 2: detailed pull of the worst offenders ---
    ids = anki("findCards", query=f"{d} prop:lapses>={args.lapse_floor}")
    truncated = len(ids) > args.max_detail
    ids = ids[: args.max_detail]
    info = anki("cardsInfo", cards=ids) if ids else []

    model_names = Counter()
    cards = []
    word_f = sent_f = None
    freq_fs = []
    for c in info:
        if word_f is None:
            word_f, sent_f, freq_fs = pick_fields(c, sm_fields)
        model_names[c["modelName"]] += 1
        f = c["fields"]
        sentence = strip_html(f.get(sent_f, {}).get("value", "")) if sent_f else ""
        word = strip_html(f.get(word_f, {}).get("value", "")) if word_f else ""
        freq = None
        for ff in freq_fs:
            freq = parse_freq(f.get(ff, {}).get("value", ""))
            if freq:
                break
        cards.append({
            "note_id": c["note"],
            "card_id": c["cardId"],
            "word": word,
            "sentence": sentence,
            "sentence_len": len(sentence),
            "freq_rank": freq,
            "lapses": c["lapses"],
            "reps": c["reps"],
            "interval": c["interval"],
            "ease": c["factor"],
            "suspended": c["queue"] == -1,
            "model": c["modelName"],
        })

    # One rendered FRONT so the model can see what the card actually TESTS (this is how
    # "days of the week leeching" gets explained — the front may not test what you think).
    front_sample = strip_html(info[0]["question"])[:300] if info else ""

    cards.sort(key=lambda x: -x["lapses"])
    report = {
        "deck": args.deck,
        "stats": stats,
        "ease_floor_artifact": ease_floor_artifact,
        "ease_floor_fraction": round(floor_frac, 3),
        "detail_field_map": {"word": word_f, "sentence": sent_f, "frequency": freq_fs},
        "note_types_in_struggle_set": dict(model_names),
        "front_sample": front_sample,
        "detail_lapse_floor": args.lapse_floor,
        "detail_truncated": truncated,
        "cards": cards,
    }

    out = os.path.expanduser(args.output)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # --- Human-readable multi-angle summary to stdout ---
    print(f'AUDIT: "{args.deck}"  ({total} cards, {reviewed} reviewed)\n')
    print("Aggregate signals:")
    for k, v in stats.items():
        print(f"  {k:<38} {v}")
    if ease_floor_artifact:
        print(f"\n  ⚠ {floor_frac:.0%} of reviewed cards sit at the minimum ease — this is an "
              f"ease-floor artifact of the deck settings, NOT a struggle signal. Discount "
              f"ease/factor; trust lapses + leeches instead.")
    print(f"\nDetailed pull: {len(cards)} cards with >={args.lapse_floor} lapses"
          f"{' (TRUNCATED — raise --max-detail)' if truncated else ''}")
    print(f"Note types in struggle set: {dict(model_names)}")
    print(f"Front of worst card (what it actually tests): {front_sample[:120]}")
    print(f"\nFull detail written to {out}")
    print("Next: read that JSON and look across the cards for HIGH-LEVEL PATTERNS "
          "(see SKILL.md → Audit angles).")


if __name__ == "__main__":
    main()
