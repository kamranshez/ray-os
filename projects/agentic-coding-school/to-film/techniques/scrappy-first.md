---
duration: "5-7 min"
batch: 3
order: 2
batch_name: "Techniques"
class: "techniques"
chapter: "Advanced Techniques"
---
Integrate this comment
>For reasons which it would take a while to unpack, if is often the case that the best (or sometimes only) way to find out what programming actually needs to be done, is to program something that's not it, and then replace it. This may need to be done multiple times. Programming is only occasionally the final product, it is much more often the means of working through what it is that is actually needed. This is very difficult for the people who ask for the software, to understand, and it is quite often very difficult for the people doing the programming to understand.

>Most of what is being done, during programming, is working through the problem space in a way which will make it more obvious what your mistakes are, in your understanding of the problem and what a solution would look like. Once you have arrived at that understanding, then there are a variety of ways to make what you need, but that is not the rate-limiting step.

- https://news.ycombinator.com/item?id=47752970
# Scrappy-First

Every new feature should get built twice. The first build is fake, fast, and isolated. The second build is real, integrated, and the one you ship. The trick is committing up front to throwing the first one away, because that's the only thing that lets you cut the corners that make it fast, and that's the only thing that lets v1 actually teach you what v2 should be.

This sounds wasteful until you remember that the second build is basically free now. An agent can regenerate a clean version from a good spec in minutes. So the question isn't "can I afford to build it twice." The question is "can I afford *not* to."

---

## The proper-first trap

Here's the old instinct. A feature request lands. You think hard, write a spec, pick the abstractions, and start building the real version. Three days in you have something clean and well-tested. You show it to a user. They use it for five minutes and say "actually I wanted it to do this other thing."

Now the investment is working against you. The abstractions are load-bearing, the tests encode the old assumption, and you can't pivot without unwinding three days of work. And the worst part is you couldn't have known any of this on day one, because the information that would have made the spec correct only shows up *after* the user touches the thing.

Proper-first is really just "guess the product, then invest heavily in the guess." When the guess is wrong, the investment is wasted.

---

## Two builds, one product

The alternative is simple: decide up front that you're building it twice.

**Build one is the research instrument.** Its only job is to exist well enough that a user can click it. Fake the auth. Mock the database. Hard-coded API response. Happy path only, no error handling, no edge cases. Standalone file or standalone route, zero integration with the rest of the codebase. One user flow, one screen, one taste of the feature.

You're not shipping this. You're not even keeping it. You're building it so you can put it in someone's hands and watch what happens.

**Then you feel it.** Click the buttons. Try to break it. The real requirements show up here, the ones you could not have guessed from reading the feature request. You're not looking for bugs. You're looking for *surprises*.

**Then you write the spec.** Now you know the shape of the problem because you've held it. The spec practically writes itself because it's informed by a real thing instead of your imagination of a real thing.

**Then you build it for real.** Throw the prototype away. Regenerate the proper version from the new spec, this time with the real integrations, the real edge cases, and the real scope. With an agent this is fast, and it's the cleanest codebase you're ever going to get, because the model is doing the thing it's strongest at: generating fresh code from clear intent.

The key move is the *throwing away*. The prototype is not a draft of the product. Its only deliverable is the spec.

---

## Why the second build is free

Here's the part that makes this economically obvious. Agents are dramatically better at *generating fresh code from a clean spec* than they are at *refactoring crusty code with inherited assumptions*.

Refactoring forces the model into its worst mode. It has to read the existing code, figure out which assumptions are load-bearing, and change things without breaking the parts it hasn't fully understood. Every dead branch and half-finished migration is a trap.

Regenerating from a spec skips all of that. Clean slate, one consistent pattern, no inherited assumptions. The model is only generating, not decoding, and generation is the thing it's best at.

So keeping the old code doesn't just cost you nothing. It actively pushes your agent into its weakest mode. "Don't throw code away" isn't just outdated advice, it's now backwards.

---

## The scrappy prompt

With an agent in the loop, the prompt is trivial. When a feature request lands, you hand the agent the request and say something like:

> Build a scrappy prototype of this feature. Thinnest possible vertical slice. Fake the auth, mock the database, hard-code the API response, happy path only, standalone route. I want to click something and feel the shape of it. Also tell me the foot-guns you hit along the way.

The important phrase is *foot-guns*. You're not asking the agent to ship the feature. You're asking it to expose what will go wrong. The ideal output is a working ugly thing plus a list of surprises: "the existing event bus can't carry this payload," "the auth layer assumes single-tenant," "the database needs a new column." That list is the beginning of your real spec, and you could not have written it without the prototype.

---

## Half the time, v1 is what you ship

Here's the side effect nobody expects. You build the scrappy version as throwaway research, fully intending to rebuild it. You put it in front of users. And a surprising amount of the time, they just use it. It's enough. It does the job. The fancy version you had planned turns out to be robustness for a problem that never existed.

So you polish the ugly version a little, and you ship it.

This is the best possible outcome, and you can only reach it by starting scrappy. If you had started with the long spec, you would have built the fancy version regardless, because that's what the spec told you to do. Scrappy-first is the only path that lets v1 accidentally become the product.

---

## When to use it, when to skip it

This isn't always the right move. Use it when the domain is new and you genuinely don't know what the user wants. Use it when the feel matters more than anything you could write on paper, so you need to hold the thing before you can describe it. Those are the cases where the prototype pays for itself, because the information it surfaces is information you literally cannot get any other way.

Skip it when the work is well-trodden. CRUD, standard integrations, the same dashboard you've built ten times. The spec is already in your head, and the scrappy step is just extra work.

Rule of thumb: the more uncertain the requirements, the more the prototype pays for itself.

---

## The shift in instinct

Plan to build it twice and the first build gets way better, because you stop trying to make it survive. Plan to build it once and you'll keep polishing the guess long after you should have thrown it out.

Build scrappy v1, ugly and fast. Put it in hands, find the foot-guns. Write the informed spec from the real shape, not the guess. Regenerate cleanly, or ship v1 if it turned out to be enough.

The best plan is a prototype. Not because prototypes are clever, but because the second build is free now, and anything that isn't a prototype is a guess dressed up as a document.
