---
duration: "7-10 min"
order: 18
class: "skills"
chapter: "Quality Control"
status: "new"
---

## A/B Testing Reference Files

Not all reference files improve quality. Some just cost tokens. Test them.

### Core Concept

"What this starts to tell me is: can we take away some of the reference files without actually compromising the quality of the output? And that is where we'd run the A/B test to see exactly which files are improving quality and which files don't even matter." (7 Levels)

### What to Show

Take a skill with multiple reference files (e.g., the AI SEO skill with 4 reference files):

1. **Baseline**: Run 5 tests with ALL reference files. Record pass rate, time, tokens.
2. **Remove one file**: Take out content-type-optimization.md
3. **Run 5 tests without it**: Compare pass rate, time, tokens
4. **Interpret results**:
   - Same 93% pass rate but significantly fewer tokens → remove it, it's dead weight
   - Pass rate drops from 93% to 70% → keep it, it's load-bearing

"I could do that for every single reference file and therefore have a really good evaluation of whether my reference files are actually benefiting my skill or just costing me token usage." (7 Levels)

### The A/B Testing Feature

"The evals feature also has a great other feature: A/B testing. I could A/B test by taking out the content type optimization reference file and saying run this same task five times, once with and once without — which performs better?" (7 Levels)

It returns a thorough review: before and after, quality comparison, token cost comparison.

### Why This Matters

Every reference file has a cost (tokens, loading time) and a benefit (quality improvement). Without A/B testing, you're guessing which files earn their keep.

The lean skill (fewer files, same quality) will:
- Activate faster
- Leave more context window for your conversation
- Be more reliable in complex workflows where multiple skills chain together
