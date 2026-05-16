---
status: stub
acs:
  - class: claude-code
    title: "Different Orderings"
mapping: mapped-partial
day: 2
block: deep-cut
---
He’ll then take that bushel of vulnerability reports and cram them back through Claude Code, one run at a time. “I got an inbound vulnerability report; it’s in ${FILE}.vuln.md. Verify for me that this is actually exploitable”. The success rate of that pipeline: almost 100%.

Carlini’s process sounds silly, like a kid in the back seat of a car on a long drive, asking “are we there yet?”, over and over. But it’s deceptively interesting. Looping over source files iterates the process. LLMs are stochastic. He gets lots of pulls on the slot machine. Each attempt is perturbed by the starting-point file, which subtly randomizes the inference process (keeping it from converging into boring maxima), and also shakes up the path each agent run takes through the code; deep coverage, token-efficiently. You could write these scripts in 15 minutes.
- https://sockpuppet.org/blog/2026/03/30/vulnerability-research-is-cooked/