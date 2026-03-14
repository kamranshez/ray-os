---
duration: "8-12 min"
batch: 2
order: 1
batch_name: "Claude Code Lab"
class: "claude-code"
chapter: "Workflows"
---

## Concept

Give Claude Code a **laboratory** — a sandbox where it can build its own benchmarking system and iterate through dozens of hypotheses to find the optimal solution to a fuzzy engineering problem.

Inspired by Brian Lovin's tweet: https://x.com/brian_lovin/status/1899442991415128182

## Key Examples from Brian

### 1. Email Newsletter → Markdown Extraction
- Problem: Emails are messy (junk headers/footers, tracking pixels, redirect links, forward chains)
- Approach: Told Claude to build a lab to find the best combo of tools and processing steps
- Claude built its own benchmarking system, tested dozens of combinations of HTML parsing libraries, pixel tracking detection, header/footer removal
- Also tested where in the pipeline an LLM step helped most (different prompts and models)
- Built an evaluation system to grade output quality
- Result: Fast, simple pipeline. Adding a cheap LLM as the final step had the most impact.

### 2. Audio Transcription Cost Reduction
- Problem: Speech-to-text models charge per minute of audio
- Approach: Build an audio lab to find the optimal way to reduce audio length without losing transcription quality
- Tested: silence trimming (varying intensity), audio compression, playback speed adjustment, and all combinations
- Evaluated accuracy against a predefined benchmark of the original transcript
- Finding: Trimming silence almost never works — clips edges of words, accuracy plummets
- Result: 1.75x speedup was the sweet spot. 47% cost reduction.

## What to Demonstrate

Pick a real problem and replicate this pattern live:
1. Define a fuzzy optimisation problem
2. Tell Claude to build itself a benchmarking/evaluation system
3. Let Claude iterate through hypotheses autonomously
4. Show it converging on an optimal solution

## Script Angle

- The insight: instead of YOU figuring out the optimal approach, give Claude a lab and let IT run experiments
- Claude is better than you at systematically testing combinations
- The key ingredients: a clear evaluation metric + freedom to iterate
- This is a workflow pattern, not a one-off trick
