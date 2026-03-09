---
duration: "1-4 min"
batch: 1
order: 21
batch_name: "Quick Wins"
class: "claude-code"
chapter: "Advanced"
---

# Generate Diagrams On Demand

Pairs with: [[delete-your-readme]]

## The problem

Architecture diagrams are READMEs with pictures. They go stale the moment you commit them, and when an agent reads a stale diagram (or the Mermaid source checked into the repo), it treats that outdated structure as ground truth. Worse, nobody updates them because updating a diagram is annoying — you have to understand what changed, open a diagramming tool, redraw it, re-export it.

## The fix

Delete the static diagram. Generate it fresh from the actual code whenever you need it.

The mermaid-diagram-generator skill does this in one step: it spawns Explore subagents that read your actual source files with `Read`, `Grep`, and `Glob`, traces the real data flow / component hierarchy / API sequence, then generates a standalone interactive HTML file with the Mermaid diagram plus a "Key Points" section documenting what it found — phase breakdowns, file paths referenced, architectural decisions, trade-offs.

It supports 10 diagram types — sequence diagrams for API flows, flowcharts for decision logic, ER diagrams for database schemas, class diagrams for component architecture, state diagrams for workflows, and more. It picks the right type based on what you're trying to understand.

## Why this beats static diagrams

1. **Always accurate.** The diagram is generated from the code that exists right now, not the code that existed when someone last bothered to update the wiki.
2. **Zero maintenance.** There's nothing to keep in sync because there's nothing stored. Generate, use, discard.
3. **Interactive.** The output is a self-contained HTML file you can open in any browser — responsive, dark mode, print-friendly. Not a dead PNG.
4. **Verification tool.** After an agent builds something, generate a diagram of what it actually built and compare it against the original plan. Gaps show up immediately — this is the "closing the loop" technique applied to architecture.

## Demo idea

Clone a repo you've never seen before. Run the mermaid-diagram-generator skill pointed at it. In 30 seconds you have an accurate architecture diagram — without reading a single line of code yourself. Then show the reverse: generate a diagram of something the agent just built, compare it against the spec, catch a missing edge case.
