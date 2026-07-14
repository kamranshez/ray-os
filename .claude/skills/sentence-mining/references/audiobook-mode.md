# Audiobook mode

**Input:** cards an *external* tool built. **Output:** the same cards, at house standard.

Ray mines Japanese audiobooks with `audiobook-viewer`, which pushes cards straight into Anki
tagged `audiobook` plus a book tag (`ryu`, `君の膵臓をたべたい`). Those cards arrive **half-built**:
a real sentence and real audiobook audio, but they never went through this skill, so nothing
enforced the house standard and nothing checked them against Ray's known words.

Audiobook mode adopts them. It does **not** create cards or re-mine the audiobook — the mining
already happened. This is the finishing pass.

**Everything except SOURCE and WRITE is [the shared pipeline](pipeline.md).**

## The expected defect set

All of these showed up on all 11 cards of the first batch (2026-07-14). Treat them as the norm,
not as edge cases:

| Defect                        | Why it matters |
|-------------------------------|----------------|
| `explanation_not_house_style` | The explanation opens cold on the definition (`首の後ろ側、…`) or on `ここでは、…`. **The #1 tell.** Ray's 9000+ cards all open by naming the word, and otherwise the TTS never says the headword. See [pipeline.md §EXPLAIN](pipeline.md#3--explain). |
| `explanation_audio_missing`   | No TTS on the explanation at all. |
| `picture_blank`               | Makes the card autoplay its sentence audio on **both** sides on mobile. Fill with `。`. See [pipeline.md §MEDIA](pipeline.md#4--media). |
| `foreign_fields:…`            | The tool leaves its own fields behind (`definition` with an English gloss, `pitch_accent`, `frequency_*`). Ray doesn't want English on these cards. |
| *(unchecked i+1)*             | Nothing diffed the card against Ray's known words, so words he learned years ago (僕) and sentences far above i+1 (天真爛漫's original) land in the main deck next to good cards. |

---

## 1 · SOURCE

### Pick the batch — ask, don't guess

```bash
python3 <skill-dir>/scripts/audiobook_scan.py --groups
```

Buckets the audiobook cards by book with how many in each still need work. **Show Ray the
buckets and let him choose** — he's usually mid-book and means "the ones I just added", not the
whole backlog. Offer the obvious candidates (a specific book, everything that needs work, or
`added:1` for today's).

### Scan

```bash
python3 <skill-dir>/scripts/audiobook_scan.py --query '<the chosen Anki query>'
```

Writes `<work>/audiobook.draft.json`: one entry per card with its `defects[]`, its `i_level`,
and a **route**. Routing reuses `analyze.py`'s known-word diff verbatim, so "known" means what
it means everywhere else in the skill.

| Route      | Meaning                                                          | What happens |
|------------|------------------------------------------------------------------|--------------|
| `main`     | Clean i+1 — the target is the only unknown in the sentence        | Stays in the main deck |
| `rescue`   | The sentence has unknowns *beyond* the target (above i+1)         | → rescue, below |
| `deferred` | Above i+1 with no easier sentence, **or** the lemma already matured on another card | Moved to the deferred deck |

> ### Never suspend. Never tag `not-worth-learning`.
>
> There is deliberately **no `retire` route here.** Ray mined these words on purpose, minutes
> ago, while reading — a card that exists is a card he wants, and the skill doesn't get to
> overrule that. The known-word diff is a hint about **sequencing** (show it to him later),
> never a verdict on worth. It is also *wrong sometimes*: it wanted to bin 突っ伏す because 突
> appears in 突然. A card sent to deferred that didn't need to be is one click to undo; a card
> suspended on a bad diff result is a word he chose vanishing silently. Ray was explicit in
> July 2026 — **"everything is worth learning at some point."**

Read each entry's `ai_instructions` before acting on it and obey it — see
[pipeline.md §CURATE](pipeline.md#2--curate).

### Rescue the too-hard cards — this is the good part

A `rescue` card is not a bad card. The **word** is still worth learning; it's the audiobook's
*sentence* that's too dense, which is just what novel prose is like. So don't exile it to the
deferred deck. Send it back through **[the cascade](pipeline.md#the-sentence-cascade)** for an
easier sentence for the same word:

```bash
python3 <skill-dir>/scripts/replace_search.py --note-ids <the rescue noteIds> --output <work>/rescue.json
python3 <skill-dir>/scripts/replace_apply.py --draft <work>/rescue.json
```

This routinely turns an i+3 card into a clean i+1. Real example from the first batch — 天真爛漫,
whose audiobook sentence carried two extra unknowns (襟足, ちょん切る):

```
audiobook:  私は天真爛漫で心配事といえば生活指導部に自慢の襟足をちょん切られることくらいだった。   (i3)
cascade:    母の死を乗り越えた明るく天真爛漫なアイドルを                                    (i1) ✓
```

Cards the cascade **misses** (no easier sentence anywhere) keep their dense sentence and fall
through to the deferred deck at apply time. That's the honest fallback, not the default.

**Expect a lot of rescue.** Novel prose is dense — 7 of the first 11 cards were above i+1.
That's the corpus being honest, not the diff being broken. Rescue them; don't loosen the
threshold.

---

## 5 · WRITE

```bash
python3 <skill-dir>/scripts/audiobook_apply.py --draft <work>/audiobook.draft.json
```

Per card: Gemini TTS on your house-style explanation → `store_media()` → overwrite
`explanation` + `explanation_audio` → clear the tool's foreign fields → `。` into a blank
picture → retag the i-level → route (deferred / leave in main).

**No approval gate** (Ray, July 2026) — nothing here is destructive: a deck move is a deck move,
and the script never suspends. Routing is applied automatically and reported afterwards.

`--dry-run` prints the plan without writing. `--only <noteIds>` applies a subset.

Then **[Step 7 · QUEUE](pipeline.md#7--queue--offer-this-every-mode-every-time)**.

---

## 6 · Audit the media — don't skip this

```bash
python3 <skill-dir>/scripts/audit_media.py --fix
```

Audiobook audio was written by an **external tool**, so it never passed through
`_anki.store_media()` and its extension was never checked against its actual bytes. A `.mp3`
that's really M4A plays fine on desktop Anki (which decodes by content) and is **silently mute
on AnkiMobile/AnkiDroid** (which trust the extension). This is exactly how two earlier batches
of bad audio got in. The audit is cheap; run it every time. See
[pipeline.md §MEDIA](pipeline.md#4--media).

---

## Gotchas

- **There is no "already processed" tag, on purpose.** Done-ness lives in the *fields* — a card
  with a house-style explanation, explanation audio, a non-blank picture and no foreign fields
  is done, which is exactly what the scan's defect check computes. An earlier version stamped a
  `claude-audiobook` marker tag and it was wrong twice over: it duplicated a check that already
  existed, and Ray's audiobook-viewer **rewrites tags on re-sync**, so finished cards lost the
  marker and reappeared anyway. Re-scanning a finished card is free — it reports zero defects.
  **Don't add a marker tag back.**
- **The scan is idempotent.** It re-reads cards every run, so it's safe over a book you've
  partly done.
- **Don't reuse `analyze.py`'s mature-kanji-stem heuristic to decide whether the target word is
  known.** Here a false "known" **buries a card Ray wants**, and it misfires constantly:
  突っ伏す shares the stem 突 with 突然. `audiobook_scan.py` deliberately requires an exact lemma
  (or spelling-variant) match. Don't "optimize" that back. Full reasoning in
  [pipeline.md §ROUTE](pipeline.md#6--route).
