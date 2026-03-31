# Video-to-Action Pipeline

## What This Video Covers

Teaching AI agents to learn from YouTube videos instead of text alone. The pipeline: feed a YouTube URL → Claude sends the video to the Gemini API → Gemini processes at 1 frame per second and extracts step-by-step instructions → structured steps return to Claude → Claude executes each step using browser/MCP tools. The agent replicates exactly what the video tutorial teaches.

## Why This Matters

Most human learning happens through video — YouTube tutorials, screen recordings, walkthroughs. But agents have historically only been able to learn from text documentation. This bridges that gap.

You can now point an agent at ANY tutorial video and have it replicate the entire workflow: building N8N flows, Blender 3D models, Figma designs, Notion setups, Excel dashboards — anything that can be taught via screencast.

This also solves the "no documentation" problem — many tools have great YouTube tutorials but terrible or nonexistent text docs.

## The Pipeline

```
YouTube URL
    ↓
Download video
    ↓
Send to Gemini API (1fps tokenization)
    ↓
Gemini extracts hyperdetailed step-by-step instructions
    ↓
Steps saved to markdown file
    ↓
Claude reads the steps file
    ↓
Claude executes each step using Chrome DevTools MCP
    ↓
Result: workflow/app/design replicated from the video
```

## How the Competitor Teaches It

- Creates a skill called "video-to-action" with the full pipeline
- References Spencer Sterling's viral post about teaching an agent the Blender donut tutorial by watching YouTube
- Feeds in a 21-minute N8N lead scraping tutorial URL
- Gemini extracts every step with timestamps ("at 17 seconds, navigate to this element")
- Claude reads the extracted steps and builds the entire N8N flow
- Uses Chrome DevTools MCP to click buttons, configure nodes, map fields
- Even tests the workflow by executing it
- The extraction includes visual cues (button colors, element positions, UI layout)

## Key Concepts to Cover

- Why video learning matters (most knowledge is video, not text docs)
- The pipeline architecture: YouTube → download → Gemini → extraction → Claude → execution
- Gemini's 1fps tokenization rate for video (how video gets converted to text tokens)
- How to write the extraction prompt for maximum detail (include visual cues, colors, positions)
- The markdown output format (timestamped steps with visual descriptions)
- Combining with Chrome DevTools MCP for browser-based execution
- Spencer Sterling's Blender donut tutorial as inspiration/proof of concept
- Limitations: works best for procedural tutorials, struggles with creative/conceptual content
- Cost considerations: video processing consumes significant Gemini tokens

## Demo Plan

1. Find a YouTube tutorial for a workflow tool (N8N, Make.com, Notion, etc.)
2. Feed the URL into the video-to-action skill
3. Show Gemini processing the video and extracting steps
4. Open the extracted steps file — show the hyperdetailed instructions
5. Have Claude execute the steps using Chrome DevTools MCP
6. Show the replicated workflow running
7. Discuss what works well and what doesn't

## Suggested Class Placement

Techniques — Advanced Techniques
