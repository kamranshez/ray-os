---
type: note-type-definition
tags: [deck, note-type, meta]
aliases: [Deck Note Type, About Decks]
date: 2026-06-20
---

## What a "deck" is

A **deck** is a brand new note type in this vault. It is a curated synthesis that pulls one topic out of several sources (videos, articles, books, interviews) and lays it out as a set of **technique cards** grouped into sections, with a closing **situational playbook** that tells you which cards to reach for in which situation.

A deck is not a summary and not a transcript. A summary compresses one source. A deck *combines* sources, attributes every idea back to where it came from, and is built to be used at the moment of action, not just read once.

Think of each card as something you could pull out mid task and apply on its own.

## When to make a deck

- You have watched or read 2+ sources on the same skill and want them merged into one reference.
- The topic is a **practice** (sales, negotiation, prompting, hiring, editing) where the payoff is knowing *which move fits which moment*.
- You want attribution preserved so you can trace a tactic back to its origin and re-watch it.

For a single source, use a normal note or [[extract-wisdom]] style breakdown instead.

## Frontmatter schema

```yaml
---
type: deck
tags: [deck, <topic>, ...]
aliases: [<Display Name> Deck]
date: YYYY-MM-DD
sources: <count and one-line description>
---
```

The `type: deck` property is what marks the note as this type, so all decks can be queried together later (Dataview / Bases).

## Structure of a deck

1. **Header / the voices** - who the sources are and the one sentence each one adds.
2. **Sections** - thematic chapters. Each section holds several technique cards.
3. **Technique cards** - the atomic unit. Every card has:
   - a short bold **name**
   - the **idea** in a few sentences
   - a **source tag** in brackets (e.g. `[AH]`) keyed to the Sources list
   - a **"Use when"** line: the situation that should make you reach for it
4. **Situational playbook** - a table or list mapping real situations to the cards that apply. This is the part that combines the concepts.
5. **Sources** - full attribution with links, keyed to the bracket tags used in the cards.

## Conventions

- Source tags are short initials in square brackets (`[KS]`, `[AH]`) and resolve in the Sources list at the bottom.
- Keep cards short enough to act on. If a card needs a page, it is really a section.
- Cross link related decks and notes with `[[wikilinks]]`.

First deck built on this type: [[b2b-sales-techniques]].
