# Check Post Performance

## Steps

1. Read all files in `references/post-history/` to see which posts need updating
2. Use Chrome browser automation to navigate to Ray's activity page:
   `https://www.linkedin.com/in/rayamjad/recent-activity/all/`
3. Extract engagement data using `get_page_text` — look for reaction counts, comments, reposts, and impressions next to each post
4. For posts with direct URLs, navigate to them individually for precise numbers using:
   ```javascript
   const buttons = [...document.querySelectorAll('button, span')];
   const reactions = buttons.find(b => b.getAttribute('aria-label')?.match(/reaction/i))?.getAttribute('aria-label');
   const comments = buttons.find(b => b.innerText.match(/\d+\s*comment/i))?.innerText;
   const reposts = buttons.find(b => b.innerText.match(/\d+\s*repost/i))?.innerText;
   const impressions = document.body.innerText.match(/(\d[\d,]*)\s*impression/gi);
   ```
5. Update each post file's frontmatter with the new engagement numbers
6. Check for any posts on LinkedIn that aren't tracked in `post-history/` — offer to add them
7. Present a summary table to the user showing all posts and their current metrics
8. Note any patterns (e.g., which archetypes get more impressions, what hooks drive comments)

## Also Check

- Posts with status `draft` — ask "Did you end up posting [hook]?"
  - If yes → update to `posted`
  - If no → update to `skipped`
