---
duration: "5-9 min"
batch: 5
order: 2
batch_name: "Subagents & Models"
class: "claude-code"
chapter: "Subagents"
---

# Model Differences

### Aparajita

Key Practical Differences

1. Error Recovery & Debugging
- Opus: When something breaks during implementation, better at diagnosing root causes across multiple files and backtracking to fix the approach
- Sonnet: Good at fixing individual issues, but may need you to help identify when the overall approach needs revision

2. Scope Changes During Implementation
- Opus: Better at recognizing mid-phase when a dependency is more complex than expected, and re-assessing the whole approach
- Sonnet: Works from the plan more literally; if scope creeps, may push forward rather than pause to reconsider

3. Multi-File Coordination
- Opus: Naturally sees all moving parts and maintains consistency across files
- Sonnet: Good but benefits from explicit guidance

4. Trade-off Analysis
- Opus: Proactively flags and weighs trade-offs
- Sonnet: Implements what you ask for, may not surface subtler design choices

5. Edge Cases & Anticipation
- Opus: Better at anticipating downstream effects
- Sonnet: May encounter and fix issues reactively

6. Speed
- Opus: Slower (more deliberation before coding)
- Sonnet: Faster execution
