"""House-style checks, shared by every path that writes an explanation.

The rules here are ENFORCED, not advised: push.py, both generate_media scripts, and
every *_apply.py call refuse_if_bad_explanations() before doing any work, so a card
whose explanation is empty or doesn't open by naming the word cannot reach Anki. The
TTS must say the headword — that's the point of the explanation audio — and cards
violating this shipped for months while the rule lived only in pipeline.md prose.

leads_with_word() moved here verbatim from audiobook_scan.py (which still uses it for
its defect scan); the gate helpers below wrap it for the write paths.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import strip_furigana, strip_html  # noqa: E402  (SudachiPy loads lazily)

KANJI = re.compile(r"[一-鿿]")


_DUP_COUNTER = re.compile(r"\s*[（(]\d+[)）]\s*$")


def norm_word(w: str) -> str:
    # Some word fields carry an Anki duplicate counter — `わけには行かない (2)` — which is
    # not part of the word and breaks exact matching against a correct opener.
    return _DUP_COUNTER.sub("", strip_furigana(strip_html(w)).strip())


def leads_with_word(explanation: str, word: str) -> bool:
    """House style: the explanation opens by NAMING the word, so the TTS actually says the
    headword and the card reads like Ray's other 9000. We look in the opening clause (before
    the first 、or 。), which is where the canonical `X は、…` opener always puts it.

    An exact substring match is too strict, because a card's word is often an INFLECTED form
    (突っ伏した, 猟奇的な) while the correct explanation opens with the dictionary form
    (突っ伏す, 猟奇的). Those are naming the headword, not dodging it. So we fall back to the
    word's kanji skeleton — 突っ伏した → 突伏 — and accept the opener if those kanji all show
    up, in order, in the head. That tolerates okurigana drift without matching an unrelated
    word that merely shares one kanji.

    Both fallbacks are ANCHORED near the start of the opener (unlike the exact match):
    they're lossy, and unanchored they accept the word's kanji merely OCCURRING
    mid-clause — pipeline.md's own ❌ example (`やろうと…途中で残して…` for やり残す)
    passed the original check through the 残 of 残して, 14 chars in. A correct opener
    names the word at the start (at most behind a 「 or a quote), so the anchor is
    "where this char sits inside the word itself, plus 2" — which keeps ひっくり返す
    (first kanji 4 chars in) passing while rejecting the mid-clause accident. Verified
    against all 7,546 explanations in Ray's live collection (2026-07-17): the anchor
    re-flags nothing the old check passed except one reading-opener (長期間 explained
    as ちょうきかんは…), which is a genuine style miss in writing even if the TTS says
    the right sound."""
    exp = strip_html(explanation).strip()
    w = norm_word(word)
    if not exp or not w:
        return False
    head = re.split(r"[、。\n]", exp, maxsplit=1)[0]
    if w in head:
        return True
    SLACK = 2  # room for an opening 「 or quote before the word
    kanji = KANJI.findall(w)
    if not kanji:
        # Kana-only word with no exact hit. An inflected kana word (なびかせて,
        # ほのめかしとくから) never exact-matches an opener that correctly names the
        # dictionary form (なびかせる, ほのめかす), and there's no kanji skeleton to
        # fall back on — so accept a shared kana stem instead: the word's first 4 kana
        # (or all of it, if shorter) opening the clause is the headword being named,
        # not an accident. Without this the check can NEVER pass such a card, so it
        # re-flags — and re-TTSes — a correct explanation on every run.
        need = min(len(w), 4)
        pos = head.find(w[:need])
        return 0 <= pos <= SLACK
    pos = head.find(kanji[0])
    if pos < 0 or pos > w.find(kanji[0]) + SLACK:
        return False
    for k in kanji[1:]:
        pos = head.find(k, pos + 1)
        if pos < 0:
            return False
    return True


def explanation_offenders(pairs, allow_empty=False):
    """[(word, explanation)] → [(word, reason)] for entries that must not be written.

    allow_empty=True skips the empty check, for callers with their own semantics for an
    empty explanation (audiobook_apply --allow-missing-explanations does field-only fixes;
    instructions_apply retts warns per-entry). A NON-empty explanation that fails
    leads_with_word is never waivable — there is no legitimate use for one."""
    out = []
    for word, exp in pairs:
        exp = (exp or "").strip()
        if not exp:
            if not allow_empty:
                out.append((word, "explanation is empty"))
        elif not leads_with_word(exp, word):
            out.append((word, "explanation does not open by naming the word"))
    return out


def refuse_if_bad_explanations(pairs, context, allow_empty=False):
    """Hard gate: exit(1) listing every offender. Call BEFORE any TTS/media/write work,
    so nothing is spent or half-written when the draft needs fixing."""
    offenders = explanation_offenders(pairs, allow_empty=allow_empty)
    if not offenders:
        return
    print(f"\n⛔ {context}: {len(offenders)} explanation(s) violate house style — "
          "nothing was written.", file=sys.stderr)
    for word, reason in offenders:
        print(f"   · {word}: {reason}", file=sys.stderr)
    print("Every explanation must open by NAMING the word (「やり残すは、…」 — dictionary "
          "form of an inflected word is fine) so the TTS says the headword.\n"
          "Fix these entries in the draft (or delete them from it), then re-run.",
          file=sys.stderr)
    sys.exit(1)
