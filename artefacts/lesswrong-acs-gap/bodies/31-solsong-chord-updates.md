# Solsong Chord Updates

- URL: https://www.lesswrong.com/posts/FtFdzhbtmxAekNqBA/solsong-chord-updates
- Author: jefftk
- Date: 2026-06-10
- Karma: 10  Comments: 0  Words: 262
- Band: B  Tier: 2  Score: 47.7  Density: 13.33
- Anchors: claude code

---

A [couple years ago](https://www.jefftk.com/p/making-a-secular-solstice-songbook) I put together a [Secular Solstice Songbook](https://www.jefftk.com/solsong/), a compilation of all the songs we've sung at [Boston Solstice](https://www.jefftk.com/p/boston-solstice-2025-retrospective). Anna Tchetchetkine and I led a session of group singing at [LessOnline](https://less.online/), following up from an informal one the year before, and I noticed several annoying things with its chord handling:

*   Despite being digital, it didn't support transposition.
    
*   Some songs didn't repeat the chord if they were unchanged, which meant that when scrolling new lyrics into view you'd lose the chords.
    
*   This is minor, but I like to align the chords in a grid and the repeat sign was very slightly to narrow, throwing off the grid.
    

In asked Claude Code to fix these, and it did almost all of it. The exception was a few cases where it wasn't obvious which chords to use and I needed to make some manual edits.

My favorite part is that it preserves the grid even when the addition of accidentals changes widths. For example, here are the chords I have for [haMephorash](https://www.jefftk.com/solsong/#hamephorash):

C Am C  Am
F G  C  G
C FG Am F
G E  Am /

If for some reason I wanted to play it in `E` instead of `C`, I could bring it up four semitones:

E C#m E   C#m
A B   E   B
E AB  C#m A
B Ab  C#m /

Note that because `C#m` is wider the columns containing it are now slightly wider to make room, accross the board.

I'm pretty happy with it, though I haven't tried using it for real yet.