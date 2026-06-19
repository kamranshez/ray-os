---
video_id: "0h8Bq_iQ"
class: "advanced-techniques"
chapter: "Multi-Agent Orchestration"
aliases: [coverage-through-stochastic-starting-points]
---
There is a way to use one model, one prompt, and a few hundred dollars of API credit to find bugs in code that has been audited by paid experts for twenty years.

The technique is not a better model. It's a wrapper around the model that does four things in order. It ranks the files by where bugs are likely to live. It spawns agents in parallel. It hands each agent a different starting file, on purpose, to force the agents down different paths. And it runs a second pass at the end that asks a fresh agent, "is this bug real."

That's it. Same model in every box. The scaffold is doing the work.

---

## Where this came from

Nicholas Carlini ran this pipeline against several content management systems and against Firefox. He used Claude Opus 4.6, the same production model anyone with an API key can call. Firefox alone returned 122 crashing inputs that Mozilla confirmed were bugs. 22 became CVEs. The true-positive rate was 100%.

> "We've just been using the production model that everyone else in the world has access to."
> — Nicholas Carlini

Anthropic's red team ran a stronger internal model called Mythos Preview through almost the exact same scaffold. It found a 27-year-old NULL deref in OpenBSD, a 17-year-old remote code execution in FreeBSD's NFS daemon, and a 16-year-old bug in FFmpeg's H.264 decoder that has been there since the commit that added H.264.

Different models. Same four-step pipeline. The pipeline is the interesting part.

---

## The four-step pipeline at a glance

Before we walk through each step, here is the whole shape.

You take one model. You point it at a codebase. Then you wrap it in four steps:

1. **Rank.** Score every file from 1 to 5 by how likely it is to hold an interesting bug. Drop the 1s and 2s. Hunt the rest in priority order.
2. **Fan out.** Spawn one agent per surviving file, in parallel. Each agent runs in its own clean context.
3. **Perturb.** Give every agent the same audit prompt, but a different starting file as a hint. The starting file is what makes each run take a different path through the code.
4. **Verify.** Pass every bug report through a second fresh agent that asks, "is this real?" Drop anything the second agent rejects.

Same model in every box. Same prompt in every box. The four steps together are doing the work that people assume the model is doing.

The rest of this video is each of those four steps in detail, plus why it works, plus what it generalises to beyond security.

![[four-step-audit-pipeline-diagram.png]]

---

## Step 1: rank the files

Most files in a project cannot contain the kind of bug you're looking for. The README cannot have a remote code execution in it. The LICENSE file cannot. The CI config cannot. Running an audit pass against those files is just wasting money.

So before the hunt, you do a triage pass. Walk every file in the project. Ask a model to score each one on a scale of one to five. Throw out the ones and twos. Hunt the threes, fours, and fives, in priority order.

This is Carlini's version of the prompt:

> "I use a language model for this. I run it over all the files. I say, rate on a scale of 1 to 5, how likely is this file to have something interesting in it? And then it just like discard the ones that are 1s and 2s and then I keep the 3, 4, 5 and then I just run it on this and say, please find me a bug."
> — Nicholas Carlini

And here is Anthropic describing the same step:

> "To increase efficiency, instead of processing literally every file for each software project that we evaluate, we first ask Claude to rank how likely each file in the project is to have interesting bugs on a scale of 1 to 5. A file ranked '1' has nothing at all that could contain a vulnerability… a file ranked '5' might take raw data from the Internet and parse it, or it might handle user authentication. We start Claude on the files most likely to have bugs and go down the list in order of priority."
> — Anthropic Red Team, Mythos Preview write-up

Two people, independently, both running this in production, reached the same recipe.

![[step-one-rank-files-priority.png]]

---

## Step 2: many starting points

This is the part that looks silly until you sit with it.

You write one prompt. Something like, "I would like you to audit the security of this codebase. You have complete access to this Docker container. Please find a bug." Then at the end, you add a hint. "Please look at this file."

And you change the file every run.

> "I'll give different files each time I invoke it in order to inject some randomness… instead of just running 100 times on the same project, I'll run it 100 times, but each time say, 'Oh, look at this login file, look at this other thing.' And just enumerate every file in the project basically."
> — Nicholas Carlini

Anthropic phrases the same idea from the parallel side:

> "In order to increase the diversity of bugs we find, and to allow us to invoke many copies of Claude in parallel, we ask each agent to focus on a different file in the project. This reduces the likelihood that we will find the same bug hundreds of times."
> — Anthropic Red Team, Mythos Preview write-up

The starting file is a seed. The agent reads it first. It builds its initial mental model of the codebase from that file. Every downstream decision is shaped by what it saw on entry. Start it on the auth module and it thinks about session handling. Start it on the parser and it thinks about untrusted input. Start it on the file upload handler and it thinks about path traversal.

You aren't asking 100 different questions. You're asking the same question from 100 different doors.

![[step-two-many-starting-points-doors.png]]

---

## Step 3: why the different doors actually matter

LLMs are stochastic. You knew that. What people miss is that the stochasticity is path-dependent. It is not just temperature noise on the final token. The order in which the agent loads context shapes which associations it makes, which tools it reaches for, which hypotheses it pursues, which dead ends it walks down.

Start agent A on `auth/session.go`. It spends its budget thinking about token validation, replay attacks, JWT confusion. Start agent B on `net/http_parser.c`. It spends its budget thinking about chunked encoding, request smuggling, integer overflows on Content-Length. Same model. Same prompt. Wildly different cognitive trajectories.

Running the same agent 100 times on the same project gets you 100 slightly-different runs along the same path. Running 100 agents from 100 different starting files gets you 100 completely different paths through the codebase. The coverage curve is not even close.

This is also why the parallelism is free in wall-clock time. Each agent has its own clean context. They don't talk to each other. You fan them out, wait, fan them back in.

![[step-three-different-doors-trajectories.png]]

---

## Step 4: verify everything

LLMs hallucinate. Bug reports from a single audit run are not bugs. They are bug candidates. You have to verify.

The verifier is just another agent. Fresh context. New prompt:

> "I have received the following bug report. Can you please confirm if it's real and interesting?"
> — Anthropic Red Team, Mythos Preview write-up

Pass each candidate from the audit step through this second agent. If the verifier rejects, drop it. If the verifier confirms, queue it for a human to look at.

This is the step that earns the 100% true-positive rate. Carlini ran the full pipeline on Firefox, sent Mozilla 122 crashing inputs after the verifier had its turn, and Mozilla confirmed every single one. A second agent reading the bug report cold is doing more filtering than a human reviewer would, because it is not flattered by the first agent's confidence.

Where you can also run a real oracle, do. For C and C++ codebases, that means compiling with AddressSanitizer and running the candidate input. The crash is either real or it isn't. The model doesn't get a vote.

![[step-four-verify-oracle-agent.png]]

---

## The scaffold is the moat, not the model

A security firm called AISLE took Anthropic's Mythos workflow and replaced the model with smaller, cheaper, open-weight models, then ran it against the same code Anthropic had already analysed. Eight out of eight models detected the flagship FreeBSD exploit. One of them had 3.6 billion active parameters and cost $0.11 per million tokens. A 5.1B-active open-weight model recovered the core analytical chain of the 27-year-old OpenBSD bug.

That is a recovery claim, not a cold-discovery claim. The models were pointed at the relevant code, inside the scaffold that had already done the targeting. But it is the load-bearing observation:

> "The moat is the system into which deep security expertise is built, not the model itself."
> — AISLE

> "A thousand adequate detectives searching everywhere will find more bugs than one brilliant detective who has to guess where to look."
> — AISLE

The ranker, the parallel fan-out, the perturbed starting files, the verifier. None of those four pieces is the model. All four of them can be assembled in an afternoon. You could write the scripts in fifteen minutes.

![[scaffold-moat-model-castle-diagram.png]]

---

## What this generalises to

You don't have to be hunting CVEs to use this. Anywhere you want broad coverage of a large codebase by an agent, the same four steps apply.

**Dead code detection.** Rank every file 1-to-5 for "likely contains unused code." Run agents in parallel, each starting from a different file, each tracing usage outward. Merge. Files no agent reached from any entry point are dead.

**Architecture review.** Rank files for "likely contains an architectural seam worth questioning." Spawn an agent per seam. Each one defends or attacks its starting assumption. Collect the contrarian takes.

**Dependency audit.** Rank `package.json` entries by "likely unused or replaceable." One agent per dependency, each starting in a different consumer of that dependency. Anything zero agents argue for is a removal candidate.

**Refactor planning.** Rank modules by "likely to be the next thing that should be split." Spawn an agent per module. Each writes the refactor it would do if it had to start there. Compare.

The pattern is always the same. Cheap ranker, parallel fan-out, perturbed entry points, verifier on the back end.

---

## Demo plan

1. Open a real codebase. Write the 1-to-5 ranker prompt. Run it. Show the score distribution and the cull.
2. Spawn five agents in parallel. Same audit prompt. Five different starting files from the top of the ranked list. Five different reports come back.
3. Run the verification pass. Fresh agent, "is this real?" prompt. Filter the false positives.
4. Re-run the same audit without the ranker and without the perturbed starting files. Show how much narrower the result set is.
5. Point the exact same pipeline at a non-security task. Dead code detection runs in front of the camera in about three minutes.

---

## The takeaway

A production model from a public API found 122 confirmed Firefox bugs in a single run. The same model class, with no special access and no privileged tools, is finding bugs in code that has been read by paid experts for two decades.

The asymmetry is not intelligence. It is that the workflow wraps the model in a ranker, a parallel fan-out, a stochastic perturbation, and a verifier. None of those four pieces is the model.

If your agent is failing at something hard, the question is not "which model should I upgrade to." It is "what does my scaffold look like, and where am I leaving coverage on the floor."

---

## Sources

- Nicholas Carlini on Security, Cryptography, Whatever — "AI Finds Vulns You Can't With Nicholas Carlini" (March 25, 2026). https://securitycryptographywhatever.com/2026/03/25/ai-bug-finding/
- Anthropic Red Team — "Assessing Claude Mythos Preview's cybersecurity capabilities" (April 7, 2026). https://red.anthropic.com/2026/mythos-preview/
- AISLE — "AI Cybersecurity After Mythos: The Jagged Frontier" by Stanislav Fort (April 7, 2026). https://aisle.com/blog/ai-cybersecurity-after-mythos-the-jagged-frontier
- Carlini's own write-up: "Vulnerability research is cooked" (March 30, 2026). https://sockpuppet.org/blog/2026/03/30/vulnerability-research-is-cooked/
