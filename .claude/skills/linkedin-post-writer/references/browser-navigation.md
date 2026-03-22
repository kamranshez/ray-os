# LinkedIn Browser Navigation Reference

How to navigate and interact with LinkedIn using Chrome browser automation (`mcp__claude-in-chrome__*`).

## Prerequisites

- Chrome browser automation tools must be available
- Get tab context first with `tabs_context_mcp`, then create or reuse a tab

## Ray's Profile

- **Profile URL:** https://www.linkedin.com/in/rayamjad/
- **Activity URL:** https://www.linkedin.com/in/rayamjad/recent-activity/all/

## Feed

Navigate to `https://www.linkedin.com/feed/` to load the main feed.

LinkedIn uses heavily obfuscated CSS class names (CSS modules). Standard DOM selectors like `.feed-shared-update-v2` or `[data-urn]` return 0 results. Use these approaches instead:

- **Reading posts:** Use `get_page_text` for bulk text extraction, or `read_page` for accessibility tree
- **Expanding posts:** Click "...more" buttons via JavaScript:
  ```javascript
  document.querySelectorAll('button').forEach(btn => {
    const text = btn.textContent.trim().toLowerCase();
    if (text.includes('more') && (text.includes('…') || text.includes('...'))) btn.click();
  });
  ```
- **Scrolling:** Use incremental scrolling (`window.scrollBy(0, 1500)`) not `scrollTo(0, document.body.scrollHeight)` — LinkedIn virtualizes the feed and unloads off-screen posts
- **Extracting engagement data:** Use regex on page text: `/(\d[\d,]*)\s+others?\s+reacted/gi`

## Profiles

Navigate to `https://www.linkedin.com/in/{username}/` for profiles.

## Posting

Navigate to `https://www.linkedin.com/feed/` and use `find` to locate the post composer ("Start a post" button).

**Composing a post:**

1. Click "Start a post" to open the composer modal
2. Use `find` to locate the text input area
3. Use `form_input` or `computer` type action to enter text
4. For line breaks in posts, use Shift+Enter (plain Enter may submit or close)
5. To add media, click the image/document/video icons in the composer toolbar
6. Click "Post" when ready (requires explicit user permission per security rules)
