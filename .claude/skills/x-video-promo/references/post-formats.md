# The video-tweet formula

How to write the short post that sits above an embedded video so people press
play. Reverse-engineered from the X posts that actually earned the watch; the
evidence and numbers behind every rule here live in `benchmarks.md`. Read this
file when writing; read that one when grading.

## The formula (3 parts + the close)

Every top video post is built the same way:

1. **Line one: a bold, concrete, first-person claim.** A strong noun and
   ownership. No throat-clearing, no "in this video". The reader's own world is
   on screen by the end of line one.
2. **A one-line twist: a reversal, a number, or the stakes.** This is the reason
   to keep reading past line one.
   - Reversal: "/grill-me is my most popular skill ever. But I've stopped using it for code."
   - Number: "slashes AFK usage limits by ~5-20X."
   - Contrarian: "AI helps you move faster, but it just accelerates software entropy."
3. **The close: a colon handoff by default.** A short final line ending in a
   colon ("Here's how it works:"), with the video right under it. The colon is
   an open loop the brain has to close, and the only way to close it is to press
   play. **Valid alternative:** a one-line personal reaction close ("This is
   just what I needed!") for the plain-announcement format below. It works as a
   credibility close that implies "and I'll show you why." Ray prefers it for
   feature-news posts; performance still unproven vs the colon handoff, so let
   the check-back log arbitrate.

The thing that ties it together: **the payoff is gated.** The post tells you a
thing exists and that it matters. It does not tell you how. The "how" is the
video. A caption that explains the whole workflow in bullets has removed its own
reason to be watched.

### Shared traits across every winner
- **Short.** Default under ~50 words total. If a draft needs a fourth idea, cut
  one instead of adding a line. Ray consistently trims drafts to roughly half
  the "complete" version; start there.
- Heavy whitespace, one idea per line, blank lines between. Never a wall.
- First person, personal ownership ("my", "I built", "a skill I made").
- Everything is named (a feature, a skill, a project). Names are clickable.
- No hashtags, no emoji clutter (one trailing arrow at most), no link in the body.
- No marketing voice. The winners sell nothing in the post.
- Capitalized and clean, not lowercase-casual. (The guinnesschen wave skewed
  lowercase; Matt Pocock, the stronger video-post benchmark, is clean caps.)
- For Ray specifically: no em dashes or en dashes, ever. Colons and line breaks
  do that work, which is the native style anyway.

## The formats worth copying

Give Ray a slate, each on a different one of these.

### A. The reveal (Matt Pocock's #1, the Sandcastle shape)
A named thing you made/found, then the colon handoff. Highest ceiling when the
artifact is genuinely yours.
```
I built <named thing>. <one line on what it is or why it's wild>.

<optional one-line twist>

Here's how it works:
```

### B. The number (the Anthropic-credit shape)
Open on a hard, arresting stat that is true. His audience reliably stops for a
number.
```
<striking true number, stated flat>.

<one line of context that makes the number land>.

Here's the setup:
```

### C. The reversal (the /grill-me shape)
Praise a thing, then subvert it. The pattern-interrupt earns the read.
```
<thing> was my whole approach to <X>.

I've stopped.

<what changed>. Here's what I switched to:
```

### D. The listicle (the "things people get wrong" shape)
A tight list of mistakes or news items, then the breakdown. Bullets are allowed
here because the list *is* the hook, but the resolution still lives in the video.
```
Things people get wrong with <X>:

- ...
- ...
- ...

Here's the breakdown:
```

### E. The plain announcement (Ray's preferred shape for feature news)
Feature stated flat, one line of contrast explaining what's actually different,
one-line personal reaction. Three short blocks, no hype, no colon handoff. Fits
third-party feature news where the video rides a wave rather than announces
Ray's own artifact. Performance unproven vs the colon-handoff formats; grade it
via the log.
```
<Vendor> just <shipped/added> <named feature> in <product>.

Unlike <the old way>, <one line on what is different and why it matters>.

This is just what I needed!
```

## Anti-patterns (the ways these die)
- **Giving away the payoff.** Bulleting the full workflow in the caption. Now
  there is nothing to watch for.
- **No close at all.** The post just trails off with neither a colon handoff
  nor a reaction line. No open loop, no pull to the video.
- **Stacking the sale.** Course/newsletter pitch in the caption suppresses the
  watch. Keep it in the video body and a pinned reply.
- **A wall of text.** No whitespace reads as effort and gets scrolled.
- **Abstraction in line one.** "In this video I discuss..." has no claim, no
  ownership, no reason to care.
- **Em/en dashes** in Ray's copy. Hard no.
