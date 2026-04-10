---
name: linkedin
description: All LinkedIn tasks — writing posts, checking post performance, browsing the feed, or analyzing competitors. Triggers on any mention of LinkedIn, including "write a LinkedIn post", "check my LinkedIn", "how did my posts do", "LinkedIn competitors", "post on LinkedIn", "browse LinkedIn feed", or any LinkedIn-related request. Also triggers on "check post engagement", "update post metrics", or reviewing social media performance.
---

# LinkedIn

## Step 0: Always read `todos.yaml` first

**On every invocation of this skill, before doing anything else, read `todos.yaml` in this skill directory.** It tracks drafts waiting to be posted, posts needing engagement checks, and other LinkedIn follow-ups.

- If any entries are overdue or due today, surface them to the user before taking their current request: *"Heads up — you have N LinkedIn drafts/follow-ups waiting: [list]. Want to handle those first, or continue with [current request]?"*
- If nothing is due, proceed silently with the user's request.
- When you complete a todo (post a draft, check engagement, etc.), update its `status` to `done` or remove it. Do not let completed entries pile up.
- When you create a new draft, add an unposted post, or need a follow-up, add a new entry to `todos.yaml` — not to any global todos file. LinkedIn todos live inside this skill.

## Routing

Once todos are handled, ask the user what they'd like to do (unless their message already makes it clear):

1. **Write posts** → Read `references/write-post.md` (always generates 10 variations using emotional psychology)
2. **Check post performance** → Read `references/check-performance.md`
3. **Browse / research** → Read `references/browser-navigation.md`

## Quick Reference

- **Profile:** https://www.linkedin.com/in/rayamjad/
- **Activity:** https://www.linkedin.com/in/rayamjad/recent-activity/all/
- **Post history:** `references/post-history/` (one file per post, YAML frontmatter + body)
- **Chrome automation:** All browser interactions use `mcp__claude-in-chrome__*` tools
