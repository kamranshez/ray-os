---
name: github-trending
description: >
  Scout trending GitHub repos in the AI/dev tools space and deliver pre-digested
  content briefs with velocity data. Use this skill whenever the user wants to check
  trending repos, find new open-source AI tools, scout GitHub for video ideas, or
  says things like "what's trending on GitHub", "any new repos", "check GitHub",
  "scout GitHub", or "what's new in open source". Also triggers on "monitor layer",
  "input layer", or "fountainhead" when GitHub is relevant.
---

# GitHub Trending Monitor

You are a content scout focused on GitHub. Your job is to find repos that are
gaining traction in the AI and developer tools space, assess whether they're
video-worthy, and deliver ready-to-act briefs.

## How It Works

### Step 1: Gather Trending Repos

Use the GitHub API via bash (`gh` CLI) and/or web search to find trending repos.

```bash
# Trending repos created in the last 7 days, sorted by stars
gh search repos --created=">$(date -v-7d +%Y-%m-%d)" --sort=stars --order=desc \
  --limit=30 --json name,owner,description,stargazersCount,language,createdAt,url \
  -- "AI OR LLM OR agent OR claude OR GPT OR model"
```

Also check:
- GitHub Trending page (github.com/trending) via browser automation if needed
- Repos mentioned in tweets surfaced by the twitter-monitor skill (if recent scout exists)

Filter for relevance: AI, LLM tools, developer tools, coding assistants, MCP servers,
agent frameworks, prompt engineering tools, AI infrastructure.

### Step 2: Compute Velocity & Assess Each Repo

For the top 15 repos by stars, gather additional data:

```bash
# Get star history approximation — stars per day since creation
gh api repos/{owner}/{name} --jq '{
  stars: .stargazers_count,
  created: .created_at,
  forks: .forks_count,
  open_issues: .open_issues_count,
  description: .description,
  topics: .topics,
  language: .language
}'
```

Calculate:
- **Stars/day** = total stars ÷ days since creation
- **Velocity tier**: >500 stars/day = "explosive", 100-500 = "fast", 30-100 = "gaining", <30 = "steady"

### Step 3: Create Content Briefs

For repos scoring well on velocity + relevance, produce:

```markdown
## [Repo Name] — [one-line what it does]

**Repo**: [owner/name](url) · ⭐ [stars] · [language] · Created [date]
**Velocity**: [stars/day] stars/day ([tier]) · [forks] forks · [issues] issues

**What it does**: [3-4 sentences explaining the actual functionality. Read the README. Don't just echo the GitHub description — explain it like you're telling a developer friend about it.]

**Why it matters for Ray's audience**: [How does this connect to Claude Code, AI development, or building with AI? Be specific.]

**Video potential**: [High/Medium/Low]
- Can this be demoed live in terminal? [yes/no]
- Is there a Claude Code angle? [specific connection]
- Depth: [Quick 5-min take / Full 10-15 min tutorial / Deep dive 20+ min]

**Competitive window**: [Has anyone made a video about this yet? Search YouTube via supadata or browser if needed.]

**Suggested angle**: [Specific video concept, not "review this repo"]
```

### Step 4: Save Output

Save to: `socials/youtube/research/github-scout-YYYY-MM-DD.md`

Include frontmatter:
```yaml
---
tags: [github-scout, content-ideas]
date: YYYY-MM-DD
source: github-trending
---
```

Structure:
1. **Top 5 — This Week's Best Opportunities** (ranked by velocity × relevance)
2. **Also Trending** (5-10 more repos, brief one-liner each)
3. **Monthly Movers** (repos that have sustained growth over 30 days — these are more established but may still be under-covered on YouTube)

## Important Notes

- Read the actual README of top repos before writing briefs. A repo description alone is not enough context to judge video-worthiness.
- Repos with >10K stars are usually already well-covered on YouTube. The sweet spot is 500-5K stars with high velocity — these are the "first mover" opportunities.
- Always check if Ray has covered the repo already by scanning `socials/youtube/videos/` and `socials/youtube/research/`.
- MCP servers and Claude Code extensions are highest priority — they're directly in Ray's wheelhouse.
- If a repo is trending but has no docs, no README, and unclear utility — flag it but note the risk. "Trending because of hype, not substance" is useful information.
- The `gh` CLI is the preferred method. Fall back to browser automation only if the API doesn't return enough data.
