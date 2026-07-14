# Instructions mode

**Input:** cards where Ray typed a note into `ai_instructions`. **Output:** the note honoured,
and the field cleared.

> "The explanation is too hard to understand."
> "The explanation audio seems to be something else?"
> "No explanation audio here. Fix it. And also add a . to the picture part."

Those are real instructions, taken off real cards. Ray writes them **while reviewing in Anki**,
in the moment he notices something wrong — which is the only moment he'll ever notice it. This
mode is what makes that worth doing.

**Everything except SOURCE and WRITE is [the shared pipeline](pipeline.md).**

## Why this mode exists

`ai_instructions` used to be read by exactly two things: `replace_search.py`, which only sees
cards Ray has **flagged**, and `audiobook_scan.py`, which only sees the **audiobook batch** he
happens to be processing. A note left on a plain video- or bank-mode card was read by nothing,
ever.

In July 2026 a sweep of the collection turned up four outstanding instructions. Two of them —
including a genuine bug where one card was reading out another card's explanation — had been
sitting there unread because the cards were neither flagged nor audiobook. Ray had typed a
message to a reader that did not exist.

This mode is that reader. It selects on **the field**, not on the defect, so it catches every
card regardless of how it was made.

## Triggers

- "check my ai_instructions" · "act on the notes I left" · "what did I flag for you"
- Any mention of instructions/notes written on cards
- **Proactively**: the scan is one cheap query. Offer it at the top of any session where cards
  come up, even if Ray launched the skill for something else.

---

## 1 · SOURCE

```bash
python3 <skill-dir>/scripts/instructions_scan.py
```

Sweeps the whole note type for a non-empty `ai_instructions` and writes
`<work>/instructions.draft.json`. Per card it reports Ray's note verbatim, plus **`facts[]`** —
objectively checkable things about the card's current state (`explanation_audio_missing`,
`picture_blank`, `explanation_not_house_style`, `foreign_fields:definition`,
`explanation_audio_shared_with:…`).

**`facts` is not a reading of the instruction — it's a second opinion on it.** Ray writes these
notes from memory, mid-review, and he is sometimes wrong about the details. When his note says
the picture is missing and `facts` doesn't list `picture_blank`, believe `facts` and ask him
what he actually meant. When his note says the audio "sounds like something else" and `facts`
says `explanation_audio_shared_with:浸る`, he was right and you now know exactly why.

## 2 · CURATE — read the note, decide the action

Fill in `action` on each entry (comma-separated; one card can do several):

| `action` | Use when                                                                 |
|----------|--------------------------------------------------------------------------|
| `retts`  | The explanation needs re-rendering. Put a rewrite in `new_explanation` if the *text* is the problem; leave it empty to re-speak the existing text (the fix for a bad or crossed audio file). |
| `fields` | Housekeeping the scan found objectively: `。` into a blank picture, strip leftover foreign fields. |
| `route`  | The note asks for a deck move. Set `route` to `main` or `deferred`.        |
| `none`   | The note needs no change to the card, or you can't act on it safely.       |

**A note asking for a better sentence is a replace-mode job.** Don't reimplement it here — run
`replace_search.py --note-ids <id>` and `replace_apply.py`, which archive the old sentence to
`previous_versions` and rehabilitate the card. Come back and mark the entry `none`, then clear
it with `--clear-anyway`.

**If an instruction is ambiguous, don't guess.** Mark it `none`, leave the field alone, and tell
Ray what it said. A misread instruction is worse than an unread one: it silently rewrites a card
he was trying to protect.

## 5 · WRITE — and clear the note

```bash
python3 <skill-dir>/scripts/instructions_apply.py --draft <work>/instructions.draft.json
```

Applies each action, then **blanks `ai_instructions`**. This is the point of the mode, not a
tidy-up afterthought: an instruction that survives the pass that honoured it re-fires on every
future run, and Ray gets asked about a card he already fixed. Clearing is what makes the field a
queue rather than a pile.

Explanation audio is written to `sm_explain_<noteId>.mp3` — **keyed on the note, never on the
source sentence.** The old bank-mode scheme keyed it on the source, so two words mined from one
sentence (自己犠牲 and 浸る, from 「自己犠牲に浸るバカな青鬼と」) collided on a single file and one
card read out the other's explanation. That's the bug Ray caught by ear. Don't reintroduce it.

`--dry-run` prints the plan without writing. `--only <noteIds>` applies a subset.

### Two things it deliberately won't clear

- **A standing preference.** "*Always* keep this card's sentence short" is meant to outlive the
  pass that read it. The scan flags these (`looks_standing`) and apply leaves them in place.
- **An entry actioned `none`.** An instruction you didn't act on is not one you've honoured, so
  it stays put. `--clear-anyway` overrides, for the case where you handled it out-of-band (a
  replace-mode run) and just need the note retired.

Then **[Step 7 · QUEUE](pipeline.md#7--queue--offer-this-every-mode-every-time)**.

### Summary shape

```
Instructions mode

  照準
    said : The explanation is too hard to understand
    did  : explanation rewritten; explanation audio regenerated
    note : cleared

  自己犠牲
    said : The explanation audio seems to be something else?
    did  : explanation audio regenerated
    note : cleared

2 card(s) handled ✓   0 instruction(s) still outstanding in the collection.
```

## Gotchas

- **Ray's notes are dictated or typed one-handed mid-review.** Expect typos ("seems t obe"),
  `&nbsp;` from Anki's editor, and shorthand. Read for intent. The scan strips HTML and
  non-breaking spaces for you.
- **"Add a . to the picture" means the `。` filler**, not a literal ASCII period — though either
  works. A *blank* picture field makes the Back template replay the sentence audio on
  AnkiMobile/AnkiDroid, so the field just needs to be non-empty. See
  [pipeline.md §MEDIA](pipeline.md#4--media).
- **Don't batch a rewrite you haven't read.** `retts` with an empty `new_explanation` re-speaks
  whatever text is already on the card. If the text is the thing Ray complained about, that
  regenerates the same problem with a new filename.
