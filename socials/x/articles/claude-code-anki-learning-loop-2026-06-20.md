---
tags: [x-article, distribution]
date: 2026-06-20
source: "YouTube (Ray Amjad / @RAmjad) — Anki + Claude Code"
---

# I wired Claude Code into Anki. It builds my flashcards and fixes the ones I keep failing.

Anki got me into Cambridge to study physics. Claude Code now runs most of my day. A month ago I wired the two together, and it's the best learning setup I've ever had.

Quick context on each. Anki is the open-source flashcard app built on spaced repetition and active recall, and I've leaned on it for over 10 years. Claude Code is the AI agent I operate my whole life around. It lives on my machine, reads and writes my files, runs commands, and connects to the other tools I use, so it's the thing I reach for first for almost any task now.

So I wondered what would happen if I put them in the same room. Turns out you can hand Claude Code the keys to your entire learning loop. Not just making cards. The whole thing.

## The bridge is one add-on

There's exactly one piece of setup. In Anki, open `Tools > Add-ons > Get Add-ons` and paste the code for **AnkiConnect**. Restart Anki. That's it. AnkiConnect lets other programs on your machine talk to Anki, and Claude Code is one of them.

To check it worked, I ask Claude Code "can you see Anki on my device using AnkiConnect?" Once it says yes, it can read my decks, write new cards, edit existing ones, and reschedule anything.

## Point it at any video and walk away

The first thing I do is generate cards from whatever I'm learning. I watched Andrej Karpathy's intro to Transformers, then pasted the URL into Claude Code: make flashcards on a new note type, pull relevant diagrams and screenshots from the video, download it with `yt-dlp`, grab the transcript, order the cards beginner to advanced, and add a card anywhere there's a gap.

A couple of minutes later the deck is done. Each card has a one-sentence answer, slides it pulled straight from the lecture, and a timestamp linking back to the exact moment in the video. Where no good diagram existed, it drew one using **Nano Banana** running locally. I've done the same with chess openings, and with a stack of B2B sales videos merged into a single deck with references back to each source.

I've done the same with learning Japanese too. Every day Claude Code pulls the words I didn't know from the videos I watched and builds sentence cards, each with a screenshot from the clip, the sentence audio, and a text-to-speech explanation. That means I can review on a walk with a controller and Bluetooth headphones instead of staring at my phone.

## The point is to stop making cards by hand

Here's why I like this. Watching videos is still one of the best ways to learn, and the watching itself is where the real work happens. It's your chance to actually wrap your head around an idea. When I put on a 3Blue1Brown video, I want to give it my full attention, scribble on some paper, and follow the reasoning all the way through. Stopping every minute to write flashcards wrecks that.

So I let Claude Code handle the recall. I give it the URL, tell it to extract the screenshots and equations and draw the diagrams, and I teach it the card style I like by correcting it once or twice. Now my attention goes to understanding the material while I watch, and the spaced repetition gets handled for me afterwards.

## The real unlock is closing the loop

Making cards is the boring half. The interesting half is everything that comes after. Most people never touch their cards once they're made. I get Claude Code to work on mine using my actual pass and fail data from Anki.

A few things it does for me:

- **Leech surgery.** I asked it to look at my Japanese sentence deck and find words I keep failing. It went through 58 struggling cards and found patterns I'd never have spotted on my own: under-contextualized sentences, synonyms clashing with each other, a few malformed cards, some false leeches, and rare literary vocabulary that isn't worth my time right now.
- **Laddering.** When you keep failing a card, there's usually a missing concept sitting between what you know and what the card asks. Claude Code builds the in-between cards, with diagrams and linked videos, to fill the gap.
- **Confusable pairs.** It detects cards I mix up, because I fail them together or the answers look alike, and writes a new card that makes the distinction explicit.
- **Reprioritizing.** I told it to push my AI-related Japanese vocabulary to the front of the queue because I want to make AI videos in Japanese. Done in one prompt.
- **Atomic refactoring.** Cards that are walls of text get split into the smallest pieces possible, following the minimum information principle: memory works best when knowledge is broken into atomic chunks.

## It can check whether you actually use what you learn

This is the part I didn't expect. I made a deck of B2B sales techniques. Going through them every day is one thing. Knowing if I actually apply them on calls is another.

So I connect Claude Code to **Granola**, my meeting recorder, through its MCP server. It reads my recorded calls and checks whether I'm using the techniques I've been drilling. Then it reprioritizes or rewrites cards based on what I'm missing. The same idea works for presenting, or anything where the real test is daily life rather than a quiz.

## The pattern that stuck with me

Every day or two, Claude Code reads my Anki history, uses how I actually performed on each card to decide what to do next, and asks me one question to steer it. Make new cards, fix broken ones, reprioritize, ladder, delete.

The card making was never the hard part. Letting an agent run the loop off your real performance data is the thing nobody's doing yet. When it comes to Claude Code and Anki, your imagination is the limit, and I have a feeling this is just the beginning.

The full walkthrough, with every prompt and live demos, is in the video.

---
**Source**: YouTube (Ray Amjad / @RAmjad) — Anki + Claude Code
**Word count**: ~950
