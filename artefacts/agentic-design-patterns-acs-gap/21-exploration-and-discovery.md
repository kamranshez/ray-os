---
title: "Ch 21: Exploration and Discovery -> ACS content-gap"
source: "Agentic Design Patterns - Antonio Gulli (Google)"
chapter: "21"
pattern: "Exploration and Discovery"
status: posted
date: 2026-07-03
tags: [acs-gap, agentic-design-patterns, book]
---

**Agentic Design Patterns, Ch 21: Exploration and Discovery** - Antonio Gulli

> Two buildable videos: a net-new Loopy-AI "co-scientist for your codebase" discovery loop that hunts unknown-unknowns, and a complement to "Multi Subagents for Hard Problems" that adds Elo-tournament ranking + evolution of the survivors. The tripartite-reviewer idea is already covered by "Automatic Plan Reviewing with Subagents".

## The one idea worth a video

- **An agent earns its keep when it proactively hunts for "unknown unknowns" instead of optimizing a goal you already handed it.** This is the chapter's highest-altitude claim; every example (Co-Scientist, Agent Laboratory) is just a machine for generating problems you did not think to ask. VERDICT: ❌ net-new video available (Loopy AI discovery loop).
- **The mechanism that makes open-ended discovery work is a generate -> debate -> Elo-tournament-rank -> evolve loop, not a single best-of-N pick.** Ranking survivors and *evolving* them across rounds is the part ACS has not filmed. VERDICT: 🔗 next-step video available (complements "Multi Subagents for Hard Problems").
- **A panel of distinct-persona reviewers approximates human judgement better than one scorer.** Real but already covered. VERDICT: ✅ already covered (kept for context).

## Summary + counts

Exploration and Discovery agents proactively seek novel information and unknown unknowns via multi-agent generate-debate-evolve loops, exemplified by Google Co-Scientist and Agent Laboratory.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 1 covered

## 🔬 Deep dive

### Spine 1 - Proactive discovery of unknown unknowns
THE CLAIM: a truly agentic system does not just optimize inside a predefined solution space, it "proactively ventures into unfamiliar territories" to surface information and sub-goals no human specified. WHY IT'S NON-OBVIOUS: the default mental model of a coding agent is reactive - you file a ticket, it implements the ticket. Gulli argues the higher-value mode is the agent "independently setting sub-goals to uncover novel information." WHY IT'S TRUE / MECHANISM: (1) in open-ended domains "static, pre-programmed information is insufficient" so the agent must generate its own hypotheses; (2) the Co-Scientist proves this concretely - it proposed KIRA6 for AML with "no prior preclinical evidence," a candidate a human optimizing known drugs would never reach. The value came from exploring, not optimizing. WHAT IT GENERALIZES TO: your codebase. Instead of "fix this bug," you run a standing agent that proactively probes for latent security flaws, dead abstractions, and risky coupling you never asked about - the chapter literally lists "Security Vulnerability Discovery" as a use case. HOW IT GOES WRONG: unbounded exploration hallucinates or chases low-value tangents; the chapter's own guardrail is a "scientist-in-the-loop" review and safety screening of goals, which the coding version needs too (a ranked shortlist, not auto-merge).

### Spine 2 - Generate, debate, Elo-tournament-rank, then evolve
THE CLAIM: the engine of discovery is a multi-agent cycle that generates many candidates, has them compete in "simulated scientific debates," ranks them with "an Elo-based tournament," and then *evolves* the top-ranked ones. WHY IT'S NON-OBVIOUS: most people stop at best-of-N - generate five options, pick one. Gulli's system does two extra things: pairwise tournament ranking (an Elo rating "concordant with the accuracy of its results," 78.4% on GPQA diamond) and an Evolution agent that "continuously refines top-ranked hypotheses by simplifying concepts, synthesizing ideas, and exploring unconventional reasoning." WHY IT'S TRUE / MECHANISM: (1) pairwise comparison is more reliable than absolute scoring because the judge only has to say which of two is better; (2) evolving winners compounds quality across rounds - "scaling test-time compute consistently improves the quality of hypotheses." WHAT IT GENERALIZES TO: hard coding problems. Generate N candidate fixes/designs, run a pairwise tournament to rank them, then hand the top two back to an evolution pass that merges their best parts - rather than implementing the majority answer once. HOW IT GOES WRONG: tournament and evolution multiply token cost fast; without a stop rule you burn budget refining a marginal winner.

### Spine 3 - Multi-persona reviewer panel (covered, for context)
Agent Laboratory's "tripartite agentic judgment mechanism" runs three reviewers with distinct lenses - "harsh but fair" on experimental rigour, one hunting "impactful in the field," one seeking "novel ideas that have not been proposed before" - each emitting a strict JSON rubric (Originality, Soundness, Overall, Decision). The insight is real: diverse evaluative personas approximate the "multi-faceted nature of human judgment" better than one scorer. But ACS already films this exact move in "Automatic Plan Reviewing with Subagents" (security, architecture, accessibility, performance reviewers folded into one plan). No distinct B to add, so no pitch.

## 🎬 Proposed ACS videos

### 1. A Co-Scientist Loop for Your Codebase (Finding the Bugs Nobody Filed)
- **HOOK:** Your agent waits for tickets. What if it went looking for the problems you don't even know you have?
- **THE PROMISE:** For devs running unattended loops - build a standing agent that proactively generates, ranks, and shortlists risks/improvements in your repo, surfacing unknown-unknowns instead of only doing what you asked.
- **THE SHAPE:** (1) Frame proactive discovery vs reactive execution using the chapter. (2) Build a loop: a Generation agent proposes hypotheses ("this auth middleware likely leaks X", "this module is dead") by exploring the codebase. (3) A Ranking pass scores each by severity x confidence. (4) The loop writes a ranked shortlist to a report, human triages - "scientist-in-the-loop", no auto-merge. (5) Schedule it nightly.
- **SPINE:** Spine 1.
- **SLOT:** Loopy AI, new chapter or under an existing autonomous-loop chapter ("discovery loop").
- **RELATIONSHIP:** ❌ net-new. ACS discovery videos ("Improving Explore Subagent", "Reducing Agent Confusion in Growing Projects") explore the codebase to *serve a plan you gave*; none run a standing agent that invents its own sub-goals and surfaces problems you never filed.
- **PROOF TO REUSE:** Co-Scientist proposing KIRA6 with "no prior preclinical evidence"; the "unknown unknowns" framing; "Security Vulnerability Discovery" listed as a use case; the "scientist-in-the-loop" guardrail as the human-triage step.

### 2. Tournament of Fixes: Rank and Evolve, Don't Just Pick One
- **HOOK:** Generating five solutions and picking one leaves quality on the table. Make them fight, then breed the winners.
- **THE PROMISE:** For devs stuck on a hard bug/design - run candidates through a pairwise tournament and an evolution round so the final answer is better than any single generation.
- **THE SHAPE:** (1) Generate N candidate approaches with parallel subagents. (2) Pairwise "debate" - a judge compares two at a time, Elo-style, to produce a ranking (more reliable than absolute scoring). (3) Take the top two, run an Evolution pass that merges/simplifies their best parts. (4) Implement the evolved winner. (5) Add a stop rule so token cost stays bounded.
- **SPINE:** Spine 2.
- **RELATIONSHIP:** 🔗 complements "Multi Subagents for Hard Problems" by being its next step. That video already has read-only strategy-analyzer subagents try distinct strategies and then implements the majority/convergent fix once. This adds the two moves it stops short of: pairwise tournament ranking instead of majority vote, and an evolution round that refines the survivors across iterations.
- **PROOF TO REUSE:** "Elo-based tournament to compare, rank, and prioritize hypotheses"; Elo rating "concordant with the accuracy of its results" (78.4% GPQA diamond); the Evolution agent that "refines top-ranked hypotheses by simplifying concepts, synthesizing ideas"; "scaling test-time compute consistently improves the quality of hypotheses".

## 📚 Full wisdom (reference)

**SUMMARY (25 words):** Exploration and Discovery agents proactively seek novel information and unknown unknowns via multi-agent generate-debate-evolve loops with tournament ranking, exemplified by Google Co-Scientist and Agent Laboratory.

**IDEAS**
- Exploration differs from optimization: it ventures into unfamiliar territory rather than searching a predefined solution space.
- The goal is uncovering "unknown unknowns," not merely optimizing a known process.
- A truly agentic system independently sets its own sub-goals to uncover novel information.
- Multi-agent frameworks let specialized LLMs emulate the scientific method collaboratively.
- Co-Scientist uses Generation, Reflection, Ranking, Evolution, Proximity, and Meta-review agents.
- A supervisor agent coordinates specialized agents in an asynchronous, scalable task framework.
- An Elo-based tournament compares and ranks hypotheses through simulated scientific debates.
- The Evolution agent refines top hypotheses by simplifying, synthesizing, and exploring unconventional reasoning.
- Test-time compute scaling allocates more compute to iteratively reason and improve outputs.
- The system follows an iterative "generate, debate, and evolve" cycle mirroring the scientific method.
- Agent Laboratory structures research into literature review, experimentation, report writing, and knowledge sharing.
- Agent Laboratory mimics an academic hierarchy: Professor, PostDoc, Reviewer, ML Engineer, SW Engineer agents.
- A tripartite reviewer panel uses three distinct personas to approximate human judgement.
- Reviewer prompts emulate human evaluation criteria: relevance, coherence, factual accuracy, quality.
- AgentRxiv is a decentralized repository letting agents share and build on findings.
- The design philosophy is augmentation, "scientist-in-the-loop," not full automation.
- Safety screening reviews both research goals and generated hypotheses before proceeding.

**INSIGHTS**
- Discovery value comes from candidates a pure optimizer would never reach (e.g. KIRA6).
- Pairwise tournament ranking is more reliable than assigning absolute quality scores.
- Evolving the winners compounds quality; best-of-N leaves improvement on the table.
- Proactive sub-goal generation is what separates an agent from a reactive tool.
- Multiple evaluative personas capture qualitative richness a single metric misses.
- Human-in-the-loop triage is the guardrail that keeps open-ended exploration safe and useful.
- Test-time compute is a dial: more reasoning rounds reliably improve hypothesis quality.
- Open-access-only knowledge is a real blind spot; paywalled and negative results are missed.

**QUOTES**
- "focus on agents proactively venturing into unfamiliar territories, experimenting with new approaches, and generating new knowledge." (Gulli)
- "Employs an Elo-based tournament to compare, rank, and prioritize hypotheses through simulated scientific debates." (Gulli)
- "Continuously refines top-ranked hypotheses by simplifying concepts, synthesizing ideas, and exploring unconventional reasoning." (Gulli)
- "scaling test-time compute consistently improves the quality of hypotheses, as measured by the Elo rating." (Gulli)
- "This pattern is essential when the objective is to uncover 'unknown unknowns' rather than merely optimizing a known process." (Gulli)
- "the very essence of a truly agentic system... move beyond passive instruction-following to proactively explore its environment." (Gulli)

**HABITS / PRACTICES**
- Structure discovery as generate -> debate -> rank -> evolve rather than a single pass.
- Rank candidates by pairwise comparison (Elo) instead of absolute scores.
- Evaluate outputs with a panel of distinct-persona reviewers.
- Keep a human in the loop to guide and triage exploratory output.
- Screen goals and generated outputs for safety before acting.

**FACTS**
- Co-Scientist runs on Google's Gemini LLM.
- It achieved 78.4% top-1 accuracy on the GPQA "diamond set".
- Analysis spanned over 200 research goals; a curated 15-problem set beat human "best guess" solutions.
- KIRA6 was a novel AML drug suggestion with no prior preclinical evidence; validated in vitro.
- It identified novel epigenetic targets for liver fibrosis, validated in human hepatic organoids.
- It recapitulated an unpublished cf-PICI/phage-tail finding in two days that took a lab over a decade.
- A safety eval with 1,200 adversarial goals showed robust rejection of dangerous inputs.
- Drug-repurposing proposals were rated high-quality by a panel of six expert oncologists.
- Agent Laboratory is by Samuel Schmidgall under the MIT License; reviewers used gpt-4o-mini.

**REFERENCES**
- Google Co-Scientist (Google Research); Gemini LLM.
- Agent Laboratory (Samuel Schmidgall, MIT License); AgentRxiv repository.
- AlphaGo (cited as game-playing exploration example).
- GPQA benchmark; Elo rating system.
- arXiv, Hugging Face, Python, LaTeX (Agent Laboratory tooling).
- Exploration-Exploitation Dilemma (Wikipedia); NIH Specific Aims format.

**ONE-SENTENCE TAKEAWAY:** Build multi-agent loops that generate, rank, and evolve hypotheses to discover what you didn't know to ask.

**RECOMMENDATIONS**
- Add a pairwise-tournament ranking step to any best-of-N generation workflow.
- Run a standing discovery agent that surfaces risks/improvements you never filed.
- Give hard problems an evolution round that merges the top two candidates.
- Use a multi-persona reviewer panel for subjective quality calls.
- Always keep human triage on the output of open-ended exploration.
- Explore Samuel Schmidgall's Agent Laboratory repo to study the agent hierarchy.
