#!/usr/bin/env python3
"""The sentence engine — ONE canonical way to answer "what's the best example
sentence for this word, for THIS learner?"

Canonical source order (SKILL.md §Sourcing):

    1. Immersion Kit          apiv2.immersionkit.com   image + audio, anime-skewed
    2. Nadeshiko              api.nadeshiko.co         image + audio, drama-heavy
    3. sentencesearch         cached static corpus     audio only, ~45k sentences
    4. kotu.io                live API                 audio only, TV/news/audiobook
    5. local sentence bank    indexed .apkg files      image + audio, indexed subset only

Each tier is tried only if the previous ones yield nothing usable *for this learner*.
None of these corpora know what the learner knows, so we graft that back on: every
candidate from every tier is tokenized with the same SudachiPy + known-word machinery
`analyze.py` uses, and ranked by how few OTHER content words are unknown — a true i+1
for this collection, not a generic JLPT level.

Why this module exists: both `replace_search.py` (fix an existing card's sentence) and
`find_sentences.py` (mine a new card from a word list) need exactly this. They used to
have two different engines — replace had the 5-tier cascade, bank mode searched only
tier 5 with its own scoring table and no known-word check, so the same word produced a
*worse* card via bank mode than via replace mode. Both now call `best_for_word()` here.

The ONLY difference between the two callers is what they do with the result:
  replace_search  → update an existing note (and drops a candidate identical to the
                    card's current sentence, since that's not an improvement)
  find_sentences  → add a new note
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze  # tokenizer + known-word diff (importing does NOT run its main())

IK_SEARCH = "https://apiv2.immersionkit.com/search"
NADESHIKO_SEARCH = "https://api.nadeshiko.co/v1/search"
SENTENCESEARCH_DATA_URL = "https://sentencesearch.neocities.org/data/all_v11.json"
SENTENCESEARCH_AUDIO_BASE = "https://receptomanijalogi.web.app/audio/"
SENTENCESEARCH_CACHE_DAYS = 30   # re-download the static corpus at most monthly
KOTU_SEARCH = "https://api.kotu.io/v2/media/anki/subtitles"
KOTU_AUDIO_BASE = "https://api.kotu.io/v2/media/audio/external/"  # + externalFile.id

LEN_MIN = 10          # below this, hits are usually fragments
LEN_MAX = 45          # above this, the clip becomes a wall of text
LEN_SWEET = 22        # ideal length; ranking prefers candidates near this
FETCH_LIMIT = 30      # candidates to pull per word before filtering
REQUEST_DELAY = 1.2   # seconds between IK requests — apiv2 429s on bursts


def norm(s):
    """Collapse to comparable form: strip html, spaces, and trailing ellipsis/punct."""
    return re.sub(r"[\s　。、！？…\.\!\?]+", "", analyze.strip_html(s))


def jp_len(s):
    return len(analyze.strip_html(s))


# ─────────────────────────────── tier 1: Immersion Kit ───────────────────────────────

def ik_search(word, limit=FETCH_LIMIT):
    """Query Immersion Kit /search. Returns examples[] (with full media URLs).

    The documented api.immersionkit.com is a dead PythonAnywhere placeholder — apiv2 is
    the live host. apiv2 throttles bursts aggressively (HTTP 429 / 'No route to host'),
    so retry with exponential backoff. Callers also space requests via REQUEST_DELAY."""
    qs = urllib.parse.urlencode({
        "q": word,
        "exactMatch": "true",
        "sort": "sentence_length:asc",
        "showUrlInMedia": "true",
        "limit": str(limit),
    })
    url = f"{IK_SEARCH}?{qs}"
    last = None
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ray-sentence-mining/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read()).get("examples", [])
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(5 * (attempt + 1))  # back off on rate limit
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            time.sleep(3 * (attempt + 1))       # transient (throttle drops the route)
    raise RuntimeError(f"IK unreachable after retries: {last}")


# ──────────────────────────────── tier 2: Nadeshiko ──────────────────────────────────

def nadeshiko_search(word, key, limit=FETCH_LIMIT):
    """POST /v1/search, normalized to the same `ex` shape ik_search returns so the
    scorer and filters work unchanged. Nadeshiko's drama-heavy corpus covers formal /
    abstract words IK's anime-skewed corpus misses. `take` max is 50 (60 → HTTP 400)."""
    body = json.dumps({
        "query": {"search": word, "exactMatch": True},
        "take": limit,
        "sort": {"mode": "ASC"},                       # shortest first
        "filters": {"category": ["ANIME", "JDRAMA"]},
    }).encode()
    url, last = NADESHIKO_SEARCH, None
    for attempt in range(5):
        try:
            req = urllib.request.Request(
                url, data=body, method="POST",
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json",
                         "User-Agent": "ray-sentence-mining/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(5 * (attempt + 1)); continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            time.sleep(3 * (attempt + 1))
    else:
        raise RuntimeError(f"Nadeshiko unreachable after retries: {last}")

    out = []
    for s in data.get("segments", []):
        tj = s.get("textJa") or {}
        urls = s.get("urls") or {}
        toks = tj.get("tokens") or []
        wl = [t.get("surface") or t.get("text") or "" for t in toks] if isinstance(toks, list) else []
        out.append({
            "sentence": tj.get("content", ""),
            "word_list": wl,
            "translation": (s.get("textEn") or {}).get("content", ""),
            "image": urls.get("imageUrl", ""),
            "sound": urls.get("audioUrl", ""),
            "title": s.get("mediaPublicId", "nadeshiko"),
            "id": s.get("publicId", ""),
            "sentence_with_furigana": "",
        })
    return out


# ─────────────────────────── tier 3: sentencesearch (cached) ─────────────────────────

def load_sentencesearch(cfg):
    """Download (and cache) the sentencesearch.neocities static corpus, return its
    records. The site searches all ~45k sentences client-side from one JSON, so we
    mirror that file into work_dir/cache and substring-search it locally — no per-word
    HTTP, no rate limit. Returns [] if it can't be fetched (the tier is then skipped)."""
    work = os.path.expanduser((cfg.get("work_dir") or "~/Documents/sentence-mining"))
    cache = Path(work) / "cache" / "sentencesearch_all_v11.json"
    fresh = cache.exists() and (
        time.time() - cache.stat().st_mtime) < SENTENCESEARCH_CACHE_DAYS * 86400
    if not fresh:
        try:
            cache.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(
                SENTENCESEARCH_DATA_URL, headers={"User-Agent": "ray-sentence-mining/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                cache.write_bytes(r.read())
        except Exception as e:  # noqa: BLE001
            if not cache.exists():
                print(f"  · sentencesearch corpus unavailable: {e}", file=sys.stderr)
                return []
            # stale-but-present cache is better than nothing — fall through and use it
    try:
        return json.loads(cache.read_text())
    except Exception:  # noqa: BLE001
        return []


def sentencesearch_examples(word, data):
    """Substring-match the cached sentencesearch corpus. Audio-only (no image); each
    record is {source, audio_jap, jap, eng} and the clip lives at AUDIO_BASE+audio_jap."""
    out = []
    for rec in data:
        jap = rec.get("jap", "")
        if word and word in jap:
            out.append({
                "sentence": jap,
                "word_list": [],                          # not tokenized → never bare-flagged
                "translation": rec.get("eng", ""),
                "image": "",
                "sound": SENTENCESEARCH_AUDIO_BASE + rec.get("audio_jap", ""),
                "title": rec.get("source", "sentencesearch"),
                "id": rec.get("audio_jap", ""),
                "sentence_with_furigana": "",
            })
            if len(out) >= FETCH_LIMIT:
                break
    return out


# ──────────────────────────────── tier 4: kotu.io ────────────────────────────────────

def kotu_search(word, limit=FETCH_LIMIT):
    """Query kotu.io's media-example API (TV/anime/news/audiobook, native audio per
    subtitle). Audio-only: the clip is at KOTU_AUDIO_BASE + externalFile.id; there is no
    screenshot. Substring (not exact) match, so `looks_misleading` earns its keep here
    dropping compound hits like 鉱山-inside-住友金属鉱山."""
    qs = urllib.parse.urlencode(
        {"q": word, "limit": str(limit), "order": "descending", "sort": "default"})
    url = f"{KOTU_SEARCH}?{qs}"
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ray-sentence-mining/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                items = json.loads(r.read()).get("items", [])
            break
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(3 * (attempt + 1)); continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = e
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"kotu unreachable after retries: {last}")

    out = []
    for it in items:
        fid = (it.get("externalFile") or {}).get("id", "")
        if not fid:
            continue
        out.append({
            "sentence": it.get("text", ""),
            "word_list": [],
            "translation": "",                            # media endpoint ships no gloss
            "image": "",
            "sound": KOTU_AUDIO_BASE + fid,
            "title": (it.get("video") or {}).get("title", "kotu"),
            "id": it.get("id", ""),
            "sentence_with_furigana": "",
        })
    return out


# ─────────────────────────── tier 5: local sentence bank ─────────────────────────────

def bank_examples(word, banks, require_media=True):
    """Normalize local sentence-bank hits into the same `ex` shape the scorer uses.
    Media are local file paths (not URLs); the apply step stores them directly.

    `search_banks.search_word` still does the within-bank ranking (audio/image present,
    exact target-word field, length sweet spot), but that ranking is only a pre-order —
    the CASCADE's `score_candidate` below is what actually decides, so bank hits compete
    on the same i+1 terms as every other tier."""
    from search_banks import search_word
    out = []
    for h in search_word(word, banks, FETCH_LIMIT):
        if require_media and not (h.get("existing_audio") and h.get("existing_image")):
            continue  # a replacement card wants BOTH native audio and a screenshot
        if not h.get("existing_audio"):
            continue  # a card with no audio at all is not usable
        out.append({
            "sentence": h["sentence"],
            "word_list": [],                      # banks don't tokenize → not bare-flagged
            "translation": h.get("bank_meaning", ""),
            "image": h.get("existing_image", ""),  # local path
            "sound": h["existing_audio"],          # local path
            "title": h.get("bank_id", "bank"),
            "id": str(h.get("note_id", "")),
            "sentence_with_furigana": "",
        })
    return out


# ──────────────────────────── filtering + i+1 scoring ────────────────────────────────

def _is_kanji(c):
    return "一" <= c <= "鿿" or c == "々"


# Honorifics that turn a noun into a proper name (紅葉くん = "Momiji", not "autumn leaves").
NAME_MARKERS = ("くん", "ちゃん", "さん", "様", "氏", "先輩", "君")
# A candidate that trails off on one of these reads broken and its clip cuts mid-thought:
# a comma, or a bare case/topic particle with no verb after it (…彼女が, …文芸書、 — both
# ranked #1 in July 2026 before this check existed; CURATE caught them only by eye).
# Deliberately NOT here: sentence-final particles that end real utterances (よ ね か な
# さ わ ぞ の), and て/で — a bare te-form is a complete casual request (死なないで).
FRAGMENT_TAILS = set("、,がをはにとへも")
# Idioms where the target carries a non-literal meaning that mis-teaches the word.
IDIOM_BLOCKLIST = {"呆れる": ("聞いて呆れる",)}


def looks_misleading(sentence, target_word):
    """True if every occurrence of the target is glued into a kanji compound
    (攻撃抑制 for 抑制, 戦略級 for 戦略), reads as a name (紅葉くん), or sits inside a
    blocklisted idiom — i.e. the sentence would mis-teach the word."""
    s = sentence.replace(" ", "").replace("　", "")
    for idiom in IDIOM_BLOCKLIST.get(target_word, ()):  # idiom check on raw text
        if idiom.replace(" ", "") in s:
            return True
    clean_occurrence = False
    i = s.find(target_word)
    while i != -1:
        after_pos = i + len(target_word)
        before = s[i - 1] if i > 0 else ""
        after = s[after_pos] if after_pos < len(s) else ""
        # Compound-glue only counts when the kanji of the TARGET butts against another
        # kanji: 攻撃|抑制 (kanji before a kanji-initial target) or 戦略|級 (kanji-final
        # target before a kanji). A kana-ending verb followed by a kanji word —
        # 和らげる|為, 整える|事 — is normal grammar, NOT a compound.
        prefix_glue = _is_kanji(before) and _is_kanji(target_word[0])
        suffix_glue = _is_kanji(target_word[-1]) and _is_kanji(after)
        named = any(s[after_pos:].startswith(m) for m in NAME_MARKERS)
        if not prefix_glue and not suffix_glue and not named:
            clean_occurrence = True
            break
        i = s.find(target_word, i + 1)
    return not clean_occurrence


def score_candidate(ex, target_word, known, require_image=True):
    """Return (rank_tuple, extra_unknowns, bare_token, i_level) for an example,
    or None if the candidate should be dropped outright.

    `known` is (intervals, norm_intervals, mature_stems, threshold). `require_image`
    is True for the screenshot-bearing sources (IK / Nadeshiko / local bank) and False
    for the audio-only web corpora (sentencesearch / kotu), which legitimately ship a
    clip but no image — the apply step writes the picture's "。" filler in that case."""
    intervals, norm_intervals, mature_stems, threshold = known
    sentence = ex.get("sentence", "")
    n = jp_len(sentence)
    if not (LEN_MIN <= n <= LEN_MAX):
        return None
    tail = sentence.rstrip(" 　…‥.")
    if tail and tail[-1] in FRAGMENT_TAILS:
        return None  # trails off mid-clause — the docs' fragment rule, enforced
    if not ex.get("sound"):
        return None  # every card needs at least native audio
    if require_image and not ex.get("image"):
        return None  # image-bearing sources must ship a screenshot
    if target_word not in sentence:
        return None
    if looks_misleading(sentence, target_word):
        return None  # compound-glued, a proper name, or a mis-teaching idiom

    word_list = ex.get("word_list", [])
    bare_token = target_word in word_list  # standalone, not glued into a compound

    # Count content words OTHER than the target that the learner doesn't yet know.
    extra_unknowns = []
    for surface, lemma, normalized, reading, pos in analyze.tokenize(sentence):
        if not analyze.is_content_word(pos):
            continue
        if not analyze.is_card_worthy(lemma):
            continue
        if target_word in (lemma, surface, normalized):
            continue
        if intervals.get(lemma, 0) >= threshold:
            continue
        if normalized and norm_intervals.get(normalized, 0) >= threshold:
            continue
        stem = analyze.extract_kanji_stem(lemma)
        if stem and stem in mature_stems:
            continue
        extra_unknowns.append(lemma)

    n_extra = len(extra_unknowns)
    i_level = f"i{min(n_extra + 1, 9)}"  # target is the +1 by definition
    # Rank: fewest other-unknowns first, then bare token, then closest to sweet length.
    rank = (n_extra, 0 if bare_token else 1, abs(n - LEN_SWEET))
    return rank, extra_unknowns, bare_token, i_level


def score_examples(examples, word, known, exclude_norm, source, require_image=True):
    """Score + sort a tier's raw examples. `exclude_norm` drops a candidate identical to
    a sentence we already have (replace mode passes the card's current sentence — an
    identical hit is not an improvement, so the word is reported as a genuine miss)."""
    scored = []
    for ex in examples:
        if exclude_norm and norm(ex.get("sentence", "")) == exclude_norm:
            continue
        res = score_candidate(ex, word, known, require_image=require_image)
        if res is None:
            continue
        rank, extra, bare, i_level = res
        scored.append({
            "rank": rank,
            "new_sentence": ex["sentence"],
            "sentence_with_furigana": ex.get("sentence_with_furigana", ""),
            "translation": ex.get("translation", ""),
            "image_url": ex.get("image", ""),
            "sound_url": ex.get("sound", ""),
            "title": ex.get("title", ""),
            "ik_id": ex.get("id", ""),
            "source": source,
            "i_level": i_level,
            "extra_unknowns": extra,
            "bare_token": bare,
        })
    scored.sort(key=lambda c: c["rank"])
    return scored


# ───────────────────────────────── the cascade ───────────────────────────────────────

class Sources:
    """Everything the cascade needs, loaded once and reused across a whole word list:
    the known-word set, the Nadeshiko key, the indexed banks, the sentencesearch corpus.

    Build it with `load(cfg)`. Both replace_search and find_sentences do this once at
    startup so a 40-word run doesn't rescan the collection or re-download a corpus 40x."""

    def __init__(self, known, nadeshiko_key, banks, ss_data):
        self.known = known
        self.nadeshiko_key = nadeshiko_key
        self.banks = banks
        self.ss_data = ss_data

    @classmethod
    def load(cls, cfg, refresh_known=False, verbose=True):
        analyze.KNOWN_INTERVAL_THRESHOLD = cfg["known_words"].get("interval_threshold", 21)

        def say(msg):
            if verbose:
                print(msg, file=sys.stderr)

        nadeshiko_key = os.environ.get("NADESHIKO_API_KEY") or ""
        say("Nadeshiko: enabled" if nadeshiko_key else "Nadeshiko: off (no NADESHIKO_API_KEY)")

        say("Loading known-word set (cached)…")
        intervals, norm_intervals = analyze.get_known_intervals(cfg, force_refresh=refresh_known)
        mature_stems = analyze.load_mature_kanji_stems(intervals)
        known = (intervals, norm_intervals, mature_stems, analyze.KNOWN_INTERVAL_THRESHOLD)

        banks = None
        idx = os.path.expanduser((cfg.get("banks") or {}).get("index_dir") or "")
        if idx and os.path.isdir(idx):
            try:
                from search_banks import load_indexes
                banks = load_indexes(Path(idx))
                say(f"Local banks: {len(banks)} indexed")
            except (Exception, SystemExit) as e:  # noqa: BLE001
                # load_indexes raises SystemExit (not Exception) when the index dir
                # exists but holds no *.notes.json — banks are an optional tier, so
                # treat that as "no banks" rather than aborting the whole run.
                banks = None
                say(f"Local banks: unavailable ({e})")
        else:
            say("Local banks: off (none indexed)")

        say("Loading sentencesearch corpus (cached)…")
        ss_data = load_sentencesearch(cfg)
        say(f"sentencesearch: {len(ss_data)} sentences" if ss_data
            else "sentencesearch: unavailable")
        say("kotu.io: enabled (live API)")
        return cls(known, nadeshiko_key, banks, ss_data)


def best_for_word(word, sources: Sources, exclude_sentence="", top=3):
    """THE sentence engine. Walk the canonical source order, stopping at the first tier
    that yields something usable for this learner, and return the top-N ranked picks.

    `exclude_sentence` is dropped from the results (replace mode passes the card's
    current sentence; new-card mining passes nothing). Empty list = a genuine miss —
    no corpus has a clean, i+1-appropriate sentence for this word."""
    ex_norm = norm(exclude_sentence)
    known = sources.known
    scored = []

    def tier(name, fetch, require_image=True):
        nonlocal scored
        if scored:
            return
        try:
            scored = score_examples(fetch(), word, known, ex_norm, name,
                                    require_image=require_image)
        except Exception as e:  # noqa: BLE001 — a dead tier must not kill the cascade
            print(f"  · {word} — {name} error: {e}", file=sys.stderr)

    tier("immersionkit", lambda: ik_search(word))
    if sources.nadeshiko_key:
        tier("nadeshiko", lambda: nadeshiko_search(word, sources.nadeshiko_key))
    if sources.ss_data:
        tier("sentencesearch",
             lambda: sentencesearch_examples(word, sources.ss_data), require_image=False)
    tier("kotu", lambda: kotu_search(word), require_image=False)
    if sources.banks:
        tier("bank", lambda: bank_examples(word, sources.banks))

    return scored[:top]
