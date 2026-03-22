# Writing a LinkedIn Post

## Before Writing

1. Read all files in `references/post-history/` to understand what's worked before
2. Read `references/viral-playbook.md` for hook formulas, archetypes, and formatting rules
3. If the user has 5+ posts with engagement data, note which archetypes and hooks performed best — prioritize proven patterns over general best practices

## Writing Rules

### Capitalization
Always use proper sentence-case capitalization. The casual tone comes from word choice and sentence structure, not from dropping capitals. Every sentence starts with a capital letter.

### Output Format
Always output the post as plain text — no markdown blockquote `>` prefixes, no code fences. The user will copy-paste it directly into LinkedIn, so it must be clean, ready-to-paste text.

### Style
Apply patterns from `references/viral-playbook.md` — hook formulas, formatting, 8 archetypes, media ranking. Keep it opinion-driven and concise. News + Insight archetype has historically performed best for this user.

## After Writing

1. Save the post as a new file in `references/post-history/YYYY-MM-DD_slug.md` with this format:

```yaml
---
date: YYYY-MM-DD
hook: "First line of the post"
archetype: The News + Insight
media: text only
status: draft
engagement:
  reactions: null
  comments: null
  reposts: null
  impressions: null
url: null
notes: null
---

The full post text here...
```

2. Ask: "Want me to post this, or are you posting yourself?"
   - If Claude posts → see `references/browser-navigation.md` for how
   - Update status to `posted` once confirmed
3. Add a todo to `todos.yaml` to check engagement in 3 days:
   ```yaml
   - task: "Check LinkedIn engagement for '[hook]' post"
     due: YYYY-MM-DD
     context: "Posted on [date]. Check reactions/comments/reposts and update post-history file."
   ```
