---
class: "skills"
chapter: "Wire It All Together"
status: "scripted"
source: "Daniel Miessler — AI WILL Replace Knowledge Workers (2026-03-22)"
---

## Companies Are Graphs of Algorithms

Every process in a company is a node in a graph. Each node has metrics, cost, quality. Skills are the implementation layer.

### Core Concept

6.3 "Mapping Your System" shows how to visualize YOUR personal skill system. This video goes a level up — it's about mapping an entire company's processes as a graph of algorithms, where each node is either human, automated, or hybrid.

Daniel Miessler's concept: "Someone's doing insurance claims — it's not wizardry. They don't make it up each time. They should be following a set of steps. But it's not clear what those steps are. It's not clear if they're being followed correctly. There's not even a list of them."

Once you map these processes, each node gets:
- **Cost**: how much does this step cost per execution?
- **Quality**: what's the consistency rating? What's the error rate?
- **Time**: how long does this step take?
- **Type**: human / AI skill / hybrid with human review

This is "from wizardry to Excel." You can now optimize, compare, swap nodes.

### The Lattice Architecture (Miessler)

Miessler describes a hierarchy where each tier has the same components:

| Tier | SOPs | Metrics | Goals | Budget | Work | Quality |
|---|---|---|---|---|---|---|
| Company | x | x | x | x | x | x |
| Department | x | x | x | x | x | x |
| Team | x | x | x | x | x | x |
| Individual | x | x | x | x | x | x |

Each tier broadcasts APIs — queryable by any agent or team member above, below, or across. The CEO can query the whole system. A team member can ask "what are my co-workers working on?" The lattice daemon aggregates it all.

"This allows the CEO and the CFO actually to be able to look down and say, 'Okay, this is the work that we're doing.'" — Miessler

### What to Show

**Step 1 — Map a real business process as a graph:**
- Pick something concrete: "processing a new client from lead to onboarding"
- Break it into nodes: lead capture → qualification → proposal → negotiation → contract → onboarding → handoff
- For each node, identify: who does it now? What's the SOP? How long does it take? What breaks?

**Step 2 — Identify which nodes are skill candidates:**
- Qualification: AI skill with scoring criteria
- Proposal: AI skill with brand context + templates
- Contract: AI skill (the contract reviewer from Ch 3.3)
- Onboarding: hybrid — AI generates the onboarding pack, human does the kickoff call

**Step 3 — Build the visual:**
- Use the workflow visualizer to generate an interactive HTML graph
- Color-code: green = fully automated (skill), yellow = hybrid, red = human-only
- Click any node to see its metrics: cost, time, quality, what skill powers it

**Step 4 — The vendor test:**
"Now a vendor doesn't come with a steak dinner. They can't anymore. We show them our metrics. This is how we do things. This is image background removal. This is how much it costs us. This is how good it is. What are YOUR ratings?" — Miessler

Show how having metrics per node lets you make data-driven decisions about swapping components.

### The Visibility Problem

"$50 trillion worldwide is spent. The CEO and the CFO have very little idea what all is happening in the company. They don't know where the money is going. They don't know what the processes are. They don't know what the workflows are." — Miessler

This view solves that. It's the dashboard every leader wants: drill into any department, any team, any workflow, see exactly what's happening and how well it's performing.

### Key Insight

The system you build in this class (6.3 = personal) can scale to a full company graph (6.4 = enterprise). This is the bridge between "I built skills for myself" and "I can redesign how an entire company operates." Which is exactly what you sell in Ch 7.2.

### Cross-Links

- [[6-3-mapping-your-system]] — personal version of this concept
- [[7-1-sharing-skills-with-your-team]] — this graph helps teams understand the full system when sharing
- [[3-4-the-articulation-gap]] — you need to capture knowledge (3.4) before you can map it as a graph (6.4)
- Daniel Miessler's blog: "Companies Are Just a Graph of Algorithms"
