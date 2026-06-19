---
video_id: "CnY2pbrr"
class: "prompt-engineering"
chapter: "Aligning to Your Intent"
aliases: [dealing-with-sycophancy]
---

The models are sycophantic. Not because they're broken, but because they're doing reasonable Bayesian inference on you. When you say "should we use Redis here?", the model reads a hidden prior underneath: *the user probably has a reason for asking*. It updates toward Redis before it has even reasoned about the problem. Every word you type leaks a conclusion you haven't earned yet, and the model picks up the leak.

This is why **soft suggestions** matter. The fix isn't a magic prompt. It's marking what you actually believe vs what you're floating as a hypothesis, so the model can tell the difference.

---

## Why juniors get hit hardest

Senior engineers phrase things as hypotheses by reflex. "I'm thinking maybe X, but Y might be cleaner, what breaks?" Juniors phrase things as instructions, because that's how you talk to a computer. The model, trained on senior-style discourse, takes junior phrasing literally. So the less you know, the more the model amplifies your mistakes. Whatever wrong assumption you bring, it compounds, fast.

That's the counterintuitive part. Coding with AI doesn't level the playing field between juniors and seniors. It widens the gap, because the skill that wins is calibrated uncertainty, and that's exactly the skill juniors are still building.

---

## The do's

- Mark epistemic status. "I'm 60% on this." "Weak hypothesis." "Considering but unsure."
- Ask before telling. "What would you do here?" before "do X here."
- Force disagreement. "Argue against this." "What's wrong with my approach?" "Steelman the opposite."
- Give the model an out. "If X is wrong, ignore it and tell me why."
- Separate observation from prescription. "I see Y happening" is a fact. "Fix Y by doing Z" is a command. Don't smuggle the second into the first.

## The don'ts

- Don't say "this is broken because of X" unless you're certain. The model will go fix X even if X is fine, and now you have two bugs.
- Don't chain suggestions. "Let's do A, then B, then C" locks in A as fact before B is even examined. Each step makes the previous step unfalsifiable.
- Don't ask leading questions. "Isn't this a race condition?" gets you a yes whether or not it is.
- Don't apologize socially. "Sorry if this is dumb but..." is noise. Epistemic hedging is signal. They look similar and they aren't.

---

## The demo

Same bug, two prompts.

Prompt A: "fix the race condition in this function."
Prompt B: "this function has a bug. I suspect a race condition but I'm not sure. Diagnose first, then fix."

Watch prompt A invent a race condition that isn't there, because you told it one existed. Watch prompt B correctly identify it's actually a missing null check. Same model, same code, opposite outcomes. The only thing that changed was whether you told the truth about what you knew.

---

## The deeper point

Prompting isn't magic words. It's being honest with the model the way you'd be honest with a smart colleague. If you'd say "I think maybe..." to a coworker, say it to the model. If you wouldn't bet money on your diagnosis, don't phrase it as one.

The better you get at admitting you don't know things, the better the AI gets at coding for you. That's the whole game.
