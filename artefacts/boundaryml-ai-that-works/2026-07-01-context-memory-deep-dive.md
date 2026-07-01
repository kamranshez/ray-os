---
title: "Context Engineering and memory deep dive #13"
videoId: -doV02eh8XI
url: https://www.youtube.com/watch?v=-doV02eh8XI
date: 2026-07-01
status: posted
---

## The one idea worth a video

**Spine 1 (❌ net-new): Decaying Resolution Memory.** You never make an agent remember everything; you make it remember what matters by summarizing at falling resolution as time recedes, so memory cost scales sublinearly instead of exploding.
VERDICT: ❌ net-new video available.

**Spine 2 (❌ net-new): Stateful tools as surrogate memory.** Stop stuffing everything into memory; give the agent scoped tools (an inbox, a calendar, a notepad) that ARE its memory, each hardcoded to one tenant so the model never touches IDs and cannot leak across customers.
VERDICT: ❌ net-new video available.

**Spine 3 (🟡 partial): It is all tokens in, tokens out.** RAG, memory, state, history and prompt engineering are one function (retrieve, then render into context); the render is the only context-engineering part.
VERDICT: 🟡 partial, the mindset is covered by the Context Engineering class; kept as a load-bearing deep dive, no pitch.

## Summary

BoundaryML's "AI That Works" episode 13: hosts Vaibhav (BAML) and Dexter (12-factor agents) plus guest Brian (Orin tutor) dissect context engineering and building agent memory.

🔴 2 net-new · 🔗 0 complement · 🟡 1 partial · ✅ 0 covered

---

## 🔬 Deep dive

### Spine 1: Decaying Resolution Memory (DRM)

The claim: you cannot make an agent recall everything, so you architect deliberate, time-keyed forgetting. Brian keeps today's interactions raw, rolls last week into daily summaries, older weeks into weekly summaries, and everything beyond into monthly summaries. Why it is non-obvious: the default reflex is to hoard, either replaying the full history or vector-searching all past conversations, both of which scale linearly and eventually blow the window or drown the model in noise. Why it is true: because most detail from a year ago is genuinely irrelevant to today, controlled information loss is a feature, not a bug. Each older tier compresses harder, so token count grows sublinearly and actually tapers, roughly 60 summaries of about 100 words each covers a five-year relationship. Their bet is that context windows grow faster than the memory ever will. What it generalizes to: Claude Code's own /compact does exactly this, building a smaller relevant subset once the window fills, as do log rotation and tiered storage (hot Redis versus cold archive). How it goes wrong: the memory is only as good as the summarizer, so each tier becomes its own evaluable LLM problem, and you must feed the summarizer ALL prior memory or it silently drops facts flagged important earlier. As Vaibhav put it, "how do I get this thing to remember everything... the answer is you don't."

### Spine 2: Stateful tools as surrogate memory (scoped IDs)

The claim: do not persist everything into a memory blob; give the agent stateful tools (email inbox, calendar, contact book, a notepad) that act as its memory, each hardcoded to exactly one customer. It argues against two defaults. First, people bolt on a "search your own memory" tool, but Brian says agents have poor intuition about what memory to fetch, so that "smells" wrong; build surrogate memory that makes semantic sense instead. Second, people make the model emit a database or user ID as a tool argument, forcing it to regurgitate an injected value. Why it is true: framing a tool as an "email inbox" activates deep in-sample training about how inboxes behave, so the model uses it human-like without instruction, while hardcoding the tenant ID sandboxes the agent so that only one family exists from its perspective. That makes cross-tenant leakage structurally impossible rather than merely prompted against, which matters enormously for children's data. It pairs with 12-factor agents' factor 13: inject always-needed context deterministically, silo the rest behind a stateful tool. Generalizes to any multi-tenant SaaS agent, and to a coding agent handed a CLI scoped to one repo. How it goes wrong: you sometimes still need a real ID (which parent's email), so scope shrinks the option set rather than eliminating it, and if a tool does not match an in-sample framing the model reverts to its bias (Brian's agent kept trying to send Zoom links).

### Spine 3: It is all tokens in, tokens out (retrieve, then render)

The claim: RAG, memory, state, history and prompt engineering are not separate disciplines but one pattern. An LLM is a stateless function whose only quality lever is the tokens fed in, so everything reduces to getting the right tokens in. Why it is non-obvious: the industry sells each as a distinct black-box tool with its own SDK. The reframe: RAG is retrieve(query) then render(data) into the prompt; memory is RAG against past conversations; state and history are RAG against the current thread. The retrieval query can be far richer than the user message (user id plus a date range). Because retrieval and rendering are orthogonal, structured outputs "live on a bridge": your context must know the schema, and so must your parser, and sometimes the model itself via constrained generation or tool calling. Dexter's framing: "it is all just strings going into models and tokens in and tokens out." Generalizes to database selection (Redis versus cold storage) and to model affinities (Anthropic guidance prefers user messages, OpenAI trains system-message obedience). How it goes wrong: it is a mindset, not a recipe, "no right answer," only trade-offs, so you need evals and observability to know which rendering actually wins. GAP: the ACS Context Engineering class already teaches this mindset for coding agents (context-is-everything, the-prompt-isnt-the-problem, signal-to-noise), so this spine is 🟡 partial and produces no pitch; the only missing angle is the AI-app-builder framing of one shared function signature.

---

## 🎬 Proposed ACS videos

### 1. Decaying Resolution Memory: Teach Your Agent To Forget On Purpose

- TITLE: Decaying Resolution Memory: Teach Your Agent To Forget On Purpose
- HOOK: You cannot make an agent remember two years of history, and you should stop trying.
- THE PROMISE: For anyone building a long-running product agent, you will leave able to build a memory that spans years while staying nearly flat in token cost.
- THE SHAPE: (1) Show the naive "replay everything" approach blowing the context window. (2) Reframe: remember what matters, not everything. (3) Build the tiers, raw today, daily this week, weekly recently, monthly forever. (4) Show it scaling sublinearly (about 60 summaries for five years). (5) Write one eval per tier and feed prior memory back into each summarizer.
- SPINE: Spine 1.
- SLOT: Context Engineering class, new "Agent Memory" chapter (or for-business, building agents).
- RELATIONSHIP: ❌ net-new. The existing Context Engineering class covers structuring context for coding agents on a codebase and Claude Code auto-memory, but nothing builds a product agent's long-term, time-decayed memory architecture.
- PROOF TO REUSE: "the answer is you don't"; the 60 summaries of about 100 words over five years figure; feeding all prior memory into every summarization prompt so notable absences still get recorded; using o3 for summaries.

### 2. Stateful Tools Are Your Agent's Memory (And Its Security Boundary)

- TITLE: Stateful Tools Are Your Agent's Memory (And Its Security Boundary)
- HOOK: Do not give your agent a tool to search its own memory; give it an inbox.
- THE PROMISE: For anyone shipping a multi-tenant agent, you will leave able to offload memory into scoped tools that make leakage structurally impossible.
- THE SHAPE: (1) The failure: an agent regurgitating a database ID it was handed. (2) Build a stateful email-inbox tool hardcoded to one tenant so only one user exists from the model's view. (3) Show why "inbox" framing beats a custom tool (in-sample knowledge). (4) Layer factor 13: inject always-needed context, silo the rest. (5) Prove cross-tenant leakage is impossible by construction.
- SPINE: Spine 2.
- SLOT: Context Engineering class (tool design) or for-business, building agents.
- RELATIONSHIP: ❌ net-new. ACS teaches MCP and tool basics, but nothing frames tools as surrogate memory, nor scoping tool instances to one tenant as the security boundary.
- PROOF TO REUSE: "sandboxed into only being able to operate within the scope of this one family"; the Zoom-link bias showing models prefer in-sample tools; the "just use Fathom" advice; the notepad-of-meeting-recordings analogy.

---

## 📚 Full wisdom (reference)

### SUMMARY
BoundaryML's "AI That Works" episode 13: hosts Vaibhav (BAML) and Dexter (12-factor agents) plus guest Brian (Orin tutor) dissect context engineering and building agent memory.

### IDEAS
- LLMs are stateless functions; the only lever on output quality is the tokens you feed in.
- RAG, memory, state, and history are the same pattern: retrieve data, then render it into context.
- Decaying resolution memory keeps today raw, then compresses older interactions into daily, weekly, then monthly summaries.
- Because summaries compress harder with age, memory token cost scales sublinearly and eventually tapers nearly flat.
- Five years of a tutoring relationship becomes roughly sixty summaries, each about a hundred words long.
- Stateful tools act as surrogate memory: the agent checks an inbox instead of storing every message.
- Each tool instance is hardcoded to one family's ID, so the model cannot leak across tenants.
- Framing a tool as an email inbox triggers rich in-sample training about how to use it.
- Never give agents tools to search their own memory; build surrogate memory tools making semantic sense.
- Structured outputs live on a bridge: context, model, and parser must all agree on the schema.
- XML seems better than JSON mainly because its parsing tolerates escape tokens like real newlines gracefully.
- Anthropic guidance prefers user messages; OpenAI trains models to obey system messages and resist prompt injections.
- The request-more-information pattern returns either a result or a structured request; your code decides next steps.
- Whether a step needs more information is a function; using a model is an implementation detail.
- Proactivity, an agent waking on its own schedule to text you, is the real wow factor.
- Letting the agent schedule itself forces you back into time zones, which models handle notoriously badly.
- Feed the summarizer all prior memory or it drops facts previously flagged as important long-term context.

### INSIGHTS
- Defining success criteria first, what to remember versus ignore, is the prerequisite to any memory design.
- Reframing 'remember everything' as 'remember what matters' converts an impossible task into an evaluable summarization problem.
- Memory, RAG, and state differ only by convention: factual data, personal history, or current conversation respectively.
- Context engineering resembles a system design interview: no right answer, only trade-offs you must actively measure.
- Sandboxing a tool to one tenant beats prompting against leaks because it removes the capability entirely.
- Models gravitate toward in-sample tools, so matching real-world tool framings beats inventing novel custom tool interfaces.
- Deterministically injecting always-needed data beats waiting for the agent to request it via a tool call.
- Time-keyed compression suits relationship agents, but a coding session stays wholly relevant and should never decay.
- Few-shot examples that describe only outputs teach structure without prescribing how to summarize each specific input.
- Proactivity delivers the wow moment, but only after understanding which problem your users actually need solved.

### QUOTES
(Near-verbatim from auto-generated captions.)
- Dexter: "LMS are completely stateless functions... the only thing that affects the quality of your AI application is the quality of the tokens."
- Dexter: "At the end of the day it's all just strings going into models and tokens in and tokens out."
- Vaibhav: "How do I get this thing to remember everything I've done over the last two years? And the answer is you don't."
- Vaibhav: "Once you reframe that problem and say, how do I get to remember the most important things? Now you have a separate task."
- Brian: "We ended up building what we call decaying resolution memory... as memories get older, it clumps them into lower resolution summarized chunks."
- Brian: "Even if we're working with a family for five years, you're still only at a max of like maybe call it 60 summaries."
- Brian: "I don't think that the paradigm of giving the agent tools to access its own memory is a very good paradigm."
- Brian: "The model itself is like sandboxed into only being able to operate within the scope of this one family."
- Brian: "If you can just use Fathom, do that man... it will have insample data about what Fathom is and how to use it."
- Brian: "It feels less like a tool and more like a service because it has this temporal memory. It can be proactive."
- Vaibhav: "These are all just fundamentally data structures and algorithms problems... Leak code is just about to get a whole lot harder."
- Dexter: "Don't try to solve time zones in a prompt."

### HABITS
- The team labels AI-written Notion docs with an upfront collapsible note so readers know the source.
- Brian's team uses o3 for all summaries, trusting it to surface what genuinely deserves longer retention.
- They plug existing condensed memory into every summarization prompt to avoid dropping previously flagged important facts.
- Daily summaries flag notes worth keeping weekly, which the weekly summarization prompt then picks them up.
- They isolate each agent's email inbox, calendar, and contacts to a single paying customer family unit.
- The agent runs a while loop calling tools until it invokes an explicit sleep tool call.
- Vaibhav yells at GPT in all caps because, he jokes, it seems to work pretty well.
- They refuse to share evals but happily share prompts, treating evals as the real secret sauce.
- Tool descriptions go in the system message even when schemas also appear in structured-output tool fields.

### FACTS
- The stateless-function context diagram originates in the 12-factor agents document, which was first published in April.
- The term context engineering popped off around June, boosted by Toby Lutke's and Andrej Karpathy's tweets.
- A Cognition blog post around June 12th helped the context-engineering term gain broad, widespread industry traction.
- Anthropic requires at least one user message before it will accept any system message in requests.
- Anthropic models recognize MCP as a distinct primitive, supporting resources that Cursor and Windsurf do not.
- Constrained generation strikes invalid tokens from the sampler but it generally hurts overall output quality somewhat.
- Orin, Brian's tutoring agent, can wake up ten to twenty times every single day fully autonomously.
- Orin serves middle schoolers, aiming to feel like a long-term partner across many months and years.
- YAML is whitespace-sensitive and JSON forbids most whitespace, while XML tolerates escape characters far more forgivingly.

### REFERENCES
- BoundaryML / BAML (structured output tooling and format).
- 12-factor agents document (Dexter, HumanLayer), notably factor 13.
- HumanLayer (Dexter's company); Orin (Brian's proactive AI tutor product).
- Brian's blog post on proactive agents plus short-term versus long-term memory.
- Toby Lutke tweet; Andrej Karpathy; Cognition blog post on context engineering.
- Claude Code /compact and CLAUDE.md rules; auto-memory.
- o3 (used for summaries); ChatGPT memory feature.
- Fathom, Granola (meeting recorders); Pipedrive (CRM); Plaid; Zoom.
- Neo4j, OWL-Time and Allen's interval algebra (13 temporal relations), raised by audience.
- MCP list-tools and resources primitive; Gemini, Cursor, Windsurf.
- AI Engineer Summit (Dexter's context engineering talk); Redis (database example).

### ONE-SENTENCE TAKEAWAY
Memory is not total recall; engineer lossy, time-decayed summaries and scoped tools around your problem.

### RECOMMENDATIONS
- Define explicitly what your agent must remember versus ignore before designing any memory system at all.
- Build decaying resolution memory: raw today, daily this week, weekly recently, monthly for everything much older.
- Write a separate eval for each summary tier, since good monthly summaries are highly use-case specific.
- Pass all prior condensed memory into summarization prompts so that notable absences still get recorded correctly.
- Scope every agent tool to one tenant with a hardcoded ID instead of model-supplied database identifiers.
- Give agents surrogate memory tools like inboxes and notepads rather than giving direct memory-search access tools.
- Frame tools using real-world names like inbox or calendar to leverage the model's in-sample training knowledge.
- Inject always-needed context deterministically instead of hoping the agent requests it via a separate tool call.
- Write few-shot examples that show only good outputs, teaching structure without prescribing each exact summarization step.
- Normalize and augment context for time zones separately; never try solving them inside the raw prompt.
