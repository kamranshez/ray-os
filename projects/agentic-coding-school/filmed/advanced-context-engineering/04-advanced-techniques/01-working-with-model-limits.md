---
status: to-film
---

I think you should not make this video and move some things here into the Techniques class.

### Force a Constraint Restatement Before Code

Many failures come from the model silently dropping constraints. It's not lying — it genuinely "forgot" by the time it started generating code.

**Analogy:** A pilot's pre-flight checklist isn't because pilots are forgetful. It's because the cost of missing something is too high to rely on memory. The checklist forces explicit confirmation.

**Add a tiny step:**
> "Before coding, list the requirements you will satisfy (max 6 bullets). Then implement."

This surfaces missing constraints early and reduces "oops I forgot."

**Why it works:** The restatement happens right before generation, when attention is highest. Constraints that would have decayed over a long context get refreshed.

---

### Use Instruction Hierarchy Explicitly

Conflicts cause unpredictable behavior; models don't reliably resolve them. When two instructions contradict, the model picks one — and you won't know which until you see the output.

**Analogy:** Traffic laws have hierarchy. "Stop at red lights" beats "maintain traffic flow." Without explicit hierarchy, every intersection becomes a judgment call.

**Give a priority order:**
1. Must pass tests
2. Must preserve public API
3. Must follow repo style
4. Nice-to-have: performance

This reduces conflict ambiguity and improves follow-through.

**Connection to the layer:** This is why [[01 - Anatomy of a Node#Set Clear Boundaries|boundaries]] matter in your CLAUDE.md. "Never do X" instructions are high-priority constraints that should be explicit and few.

---

### Use Two-Pass Agents for Reliability

Single-pass generation drops constraints; a second pass catches misses. This isn't a sign of model weakness — it's using the tool correctly.

**Analogy:** Code review exists because authors miss things in their own code. Fresh eyes catch what tired eyes skip. A second-pass agent is automated code review for instruction compliance.

**Make it useful:**
- Pass 1: Generate solution
- Pass 2: A "compliance checker" prompt: "Check against requirements; list violations; patch."

This is basically unit tests for instruction following.

**Connection to the layer:** This pattern maps to [[02 - The Context Layer#Hooks|hooks]]. A post-edit hook can run validation automatically — you don't have to remember to invoke the second pass.