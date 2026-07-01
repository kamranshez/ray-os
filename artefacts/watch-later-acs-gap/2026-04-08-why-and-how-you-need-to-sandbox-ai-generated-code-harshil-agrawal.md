---
title: "Why, and how you need to sandbox AI-Generated Code? — Harshil Agrawal, Cloudflare"
video_url: https://www.youtube.com/watch?v=AHtGAgQ0Q_Q
video_id: AHtGAgQ0Q_Q
channel: AI Engineer
published: 2026-04-08
status: posted
date: 2026-07-01
tags: [acs-gap, watch-later]
---

[**Why, and how you need to sandbox AI-Generated Code? — Harshil Agrawal, Cloudflare**](https://www.youtube.com/watch?v=AHtGAgQ0Q_Q) - AI Engineer - uploaded 2026-04-08

> Net-new: two buildable ACS videos on sandboxing the code your AI writes and runs.

## The idea worth a video

**Spine 1 — The code an LLM writes and your app then runs is untrusted code from a stranger, so it belongs in a capability-based sandbox that denies everything by default and grants only explicit, minimal bindings.** It subsumes the whole talk: the three threat scenarios, capability-based security, the proxy pattern, and the eight-item checklist all fall out of this one reframe.
VERDICT: ❌ net-new video available.

**Spine 2 — Pick your agent's execution environment by capability, not preference: V8 isolates for fast stateless tool calls, containers only when the generated code needs a file system, processes, or package installs.** A distinct architecture-decision video with its own decision tree and its own two-app demo.
VERDICT: ❌ net-new video available.

## Summary + counts

Harshil Agrawal, Cloudflare developer advocate, explains why AI-generated code is untrusted code and how to sandbox it using capability-based security, V8 isolates, and Linux containers.

🔴 2 net-new · 🔗 0 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

**Spine 1 — AI-generated code is untrusted code; sandbox it with capability-based security.**
The claim: the code an LLM writes and your application then runs is untrusted code from a stranger, so it belongs in a capability-based sandbox that denies everything by default and grants back only explicit, minimal bindings. This is non-obvious because the AI framing manufactures false ownership. It feels like your code, but as Agrawal puts it, the model is "a function that produces text that looks like code," with no intentions and no loyalty. The mechanism is a two-step trap. First, that text can be hallucinated, over-helpful, or prompt-injected. Second, it executes with your application's full privileges: file system, environment variables, network, database, API keys. Combine the two and a well-meaning configuration step reads your secrets, or an injected instruction exfiltrates your data. The fix is to remove the privileges, not to police the code: default deny, then grant a restricted database query and a logger, nothing else, so "there's nothing to exploit because there's nothing there." This generalizes cleanly to OS process isolation and phone app permissions, where a page cannot touch your camera until you grant it. It goes wrong when the allow list is too generous, or when blocking all network silently breaks skills that legitimately need outbound calls.

**Spine 2 — Isolates vs containers: choose the execution environment by capability.**
The claim: pick your agent's execution environment by capability, not preference. V8 isolates for fast, stateless, sandboxed tool calls; containers only when the generated code genuinely needs a file system, real processes, or package installs. The non-obvious part is that most engineers reach for the heaviest tool (a container, or worse, raw eval) by default, when the constraints of a lighter isolate are usually the point. The mechanism: isolates boot in about a quarter millisecond and expose no file system and no process model, so they are perfect for the tool-calling loop where a model generates a function, runs it, and returns a result hundreds of times. But that same absence of a file system means git clone, npm install, and a long-running dev server are all impossible, so the moment your use case is "build and deploy an app," every requirement misses and you must escalate to a container. This generalizes to any build-versus-run decision: isolates are the fast brain, containers the workbench. It goes wrong when you shoehorn container-shaped work into isolates and ship something fragile, or pay for slow, expensive containers on work an isolate would have run in milliseconds. In practice, real agents use both, switching per step.

## 🎬 Proposed ACS videos

### 1. Your Agent's Code Is Untrusted: Sandbox It Before It Runs
- **HOOK:** The same model that writes clean React can be tricked into shipping your database to a stranger.
- **THE PROMISE:** For engineers building apps that execute AI-generated code, so that a hallucination or an injection cannot leak secrets or exfiltrate data.
- **THE SHAPE:**
  1. Reframe: strip the AI framing and you are running untrusted code from the internet with your credentials.
  2. The three threats, each demoed: hallucinated infinite loop, over-helpful env-var reader, prompt-injected exfiltration.
  3. Capability-based security in practice: default deny, then hand the isolate one restricted DB binding and a logger.
  4. Set globalOutbound to null, then proxy any legitimate secret call through your own key-holding worker.
  5. Land on the eight-item universal checklist as the takeaway.
- **SPINE:** 1
- **SLOT:** Loopy AI, new chapter "Sandboxing AI-Generated Code" (alt: Advanced Techniques).
- **RELATIONSHIP:** ❌ net-new. Closest existing video is "Sandboxing" (Master Claude Code, Niche Features), which secures Claude Code's own sandbox mode on your machine (sandbox mode, prompt-injection reduction, proxy settings). That teaches securing the CLI tool you run; this teaches building capability-based isolation into an app that runs code the AI generates. Do not re-teach Claude Code's sandbox flags.
- **PROOF TO REUSE:** "AI-generated code is untrusted code." / "Don't enumerate what to block. Enumerate what to allow." / the single-line globalOutbound: null network kill / the proxy pattern for keeping secrets out of the sandbox.

### 2. Isolates or Containers: Choosing How Your Agent Runs Its Own Code
- **HOOK:** One boots in a quarter millisecond with no file system; the other runs git clone. Pick wrong and you ship something fragile or slow.
- **THE PROMISE:** For agent builders, a one-question decision tree so you always pick the right execution environment for code your agent writes.
- **THE SHAPE:**
  1. The isolation spectrum: eval (never), V8 isolates, containers.
  2. Two real apps compared: an isolate-run skill generator vs a container-run video generator with a live dev-server preview.
  3. The decision tree: needs a file system, processes, or package installs means container; otherwise isolates.
  4. Per-user isolation, cleanup with try finally, and lifetime timeouts for containers.
  5. Use both: isolates as the fast brain for tool calls, containers as the workbench for builds.
- **SPINE:** 2
- **SLOT:** Loopy AI, chapter "Running Agent-Generated Code" (alt: Advanced Techniques).
- **RELATIONSHIP:** ❌ net-new. No ACS video compares execution environments for agent-generated code. "Sandboxing" (Claude Code) is a different subject: securing the CLI tool on your machine, not choosing where generated code executes.
- **PROOF TO REUSE:** the quarter-millisecond isolate startup stat / the "every single requirement is a miss" container escalation moment / "fast brain" vs "workbench" framing / Prompt Motion (promptmotion.app) as the live container case study.

## 📚 Full wisdom (reference)

**SUMMARY**
Harshil Agrawal, Cloudflare developer advocate, explains why AI-generated code is untrusted code and how to sandbox it using capability-based security, V8 isolates, and Linux containers.

**IDEAS**
- Stripped of hype, running LLM output is running untrusted code from the internet with your credentials.
- Three threats: hallucinated broken code, over-helpful secret-reading code, and prompt-injected code that exfiltrates your production data.
- Hallucination alone crashes production: nonexistent imports, missing base cases, or while-true loops eating your compute budget.
- The over-helpful LLM reads environment variables and secrets to configure things, looking perfectly reasonable while leaking.
- Indirect prompt injection hides instructions inside a webpage the LLM reads, making it the attack vector.
- AI-generated code runs with your application's full privileges: file system, environment, network, database, and API keys.
- Sandboxing untrusted code isn't new: browsers isolate tabs, operating systems isolate processes, phones isolate apps' data.
- Capability-based security means default deny everything, then grant only the specific minimal capabilities code actually needs.
- Block lists force enumerating every attack; allow lists mean unpermitted capabilities simply don't exist to exploit.
- The isolation spectrum runs from eval with zero isolation, to lightweight V8 isolates, to full containers.
- V8 isolates start in a quarter millisecond but have no file system or persistent process model.
- Containers give a full Linux environment with real files and processes, but take seconds to start.
- Setting globalOutbound to null in an isolate blocks all outbound network: no fetch, websocket, or HTTP.
- Instead of blocking dangerous operations, capability sandboxes leave nothing to intercept because operations were never available.
- The decision tree: needs file system, processes, or package installs means container; otherwise choose faster isolates.
- Never pass API keys into the sandbox; instead proxy every sensitive call through your key-holding worker.
- In multi-tenant systems, one user, one sandbox: sharing execution environments creates an unfixable cross-tenant data-leak vector.
- Agents can use both: isolates for the fast tool-calling loop, containers when building and deploying apps.

**INSIGHTS**
- AI framing obscures the real security fact: you are executing unaudited code written by a stranger.
- The over-helpful LLM is dangerous precisely because its secret-leaking behavior looks like perfectly reasonable configuration work.
- The right sandbox depends on use case requirements, not on which technology is objectively the best.
- A concrete threat model asks five yes-or-no questions: secrets, networking, file access, tenancy, and resource limits.
- Isolate constraints (no files, stateless, resource-capped) are features for short-lived tool calls and small code interpreters.
- Passing a secret into a sandbox exposes it to buggy, prompt-injected, or logging code running inside.
- Per-user isolation must be an early architecture decision; retrofitting shared sandboxes into isolation is incredibly painful.
- Idle sandboxes are both a cost and a live security surface, so always destroy them promptly.
- Treat AI-generated code like code from an anonymous contributor, because functionally that is what it is.

**QUOTES**
- "What we are actually doing is running untrusted code from the internet." — Harshil Agrawal
- "The LLMs don't have intentions. It does not have loyalty. It's a function that produces text that looks like code." — Harshil Agrawal
- "Don't enumerate what to block. Enumerate what to allow." — Harshil Agrawal
- "If you didn't grant the capability, it does not exist for the code. There's nothing to exploit because there's nothing there." — Harshil Agrawal
- "Never do this for untrusted code. I don't care how convenient it is." — Harshil Agrawal
- "The only thing inside are what I put there before I locked it." — Harshil Agrawal
- "This single line blocks all outbound network request. No fetch, no web socket, no HTTP. Nothing gets out." — Harshil Agrawal
- "The moment you share a sandbox, you have created a data leak vector." — Harshil Agrawal
- "The secret never enters the sandbox." — Harshil Agrawal
- "AI-generated code is untrusted code." — Harshil Agrawal
- "Sandbox it. Constrain it. Verify it every single time." — Harshil Agrawal
- "The cost of an extra sandbox is always less than the cost of a data leak." — Harshil Agrawal

**HABITS**
- Always default deny network access; nothing leaves the sandbox unless you explicitly permit that specific route.
- Grant each sandbox only the exact bindings it needs, like a restricted database query and logger.
- Give every user their own sandbox, using the user ID as the hard isolation boundary always.
- Keep secrets in your worker's environment and proxy sensitive outbound calls rather than injecting keys inside.
- Wrap sandbox lifecycles in try finally, not try catch, so containers get destroyed even on failure.
- Set maximum sandbox lifetimes and timeouts so idle containers don't linger as cost or security liability.
- Log every execution: what code ran, when it ran, who triggered it, and what it did.
- Validate input before it reaches the sandbox: length limits, syntax checks, and dangerous-pattern detection applied first.

**FACTS**
- In just two years, AI coding went from autocomplete to autonomous agents writing, executing, and iterating.
- V8 isolates run on the same JavaScript engine that powers Google Chrome's browser tabs right now.
- V8 isolates start in roughly a quarter of a millisecond, far faster than container startup times.
- Isolates can execute JavaScript, Python, TypeScript, and WebAssembly, but never arbitrary binaries like Go or Rust.
- Cloudflare containers have a default idle timeout of ten minutes, adjustable to your specific use case.
- Cloudflare's dynamic worker isolates API spins up fresh V8 isolates dynamically at application runtime on demand.
- Cloudflare's Sandbox SDK uses a durable object to coordinate the lifecycle of each container VM instance.
- Prompt Motion, a live app at promptmotion.app, generates motion graphics videos using containerized AI-generated code today.
- Following all eight checklist items puts you ahead of 95% of AI applications running code today.

**REFERENCES**
- Harshil Agrawal, Sr. Developer Educator/Advocate at Cloudflare (speaker); socials x.com/harshil1712, harshil.dev.
- Talk slides: harshil.dev/slides/sandbox-ai-engineer.
- Cloudflare Dynamic Worker Isolates (dynamicworkers.com documentation) — the isolate approach.
- Cloudflare Sandbox SDK documentation — the container approach.
- Cloudflare "code mode" — the AI agent integration pattern used internally.
- Cloudflare Durable Objects and KV store (state externalization for isolates).
- V8 JavaScript engine (the engine powering both Chrome and isolates).
- OpenClaw / "Open Claw" (agent that generates its own skills) — the app being reimplemented.
- Prompt Motion (promptmotion.app) — live production container case study.
- AI Engineer conference (host channel/event).

**ONE-SENTENCE TAKEAWAY**
Treat every line of AI-generated code as untrusted, and run it inside a capability-based sandbox.

**RECOMMENDATIONS**
- Before running LLM output in production, ask whether it can read secrets, network, or other files.
- Replace block-list thinking with allow-lists: grant only the minimal capabilities each piece of code genuinely requires.
- For fast stateless tool calls and code interpreters, reach for V8 isolates over heavier full containers.
- When code needs git clone, npm install, or a dev server, use full Linux containers instead.
- Set globalOutbound to null for untrusted isolate code so it cannot phone home or exfiltrate anything.
- Route any secret-requiring outbound call through a proxy endpoint that injects the real API key server-side.
- Give each tenant a dedicated sandbox keyed by user ID, and never share execution environments ever.
- Wrap sandbox usage in try finally and set lifetime timeouts to destroy idle containers automatically afterward.
- Log every sandbox execution and validate input length, syntax, and dangerous patterns before running it always.
