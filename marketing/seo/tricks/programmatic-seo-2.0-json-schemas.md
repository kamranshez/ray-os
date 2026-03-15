---
source:
  - https://x.com/jakezward/status/2031701565434732917
  - https://x.com/hridoyreh/status/2032048973872013697
author: Jake Ward (@jakezward)
date: 2026-03-14
---

## Programmatic SEO 2.0 — JSON Schema-Driven Pages at Scale

13,000+ pages built in 3 hours, +466% organic traffic in 60 days.

### Core Concept

Never ask AI to write freeform content. Ask it to fill a **strict JSON schema**.

- AI generates structured data (JSON)
- React components handle presentation
- These two layers never mix

This prevents inconsistent structure, unpredictable quality, and unvalidatable pages.

### The System

1. **Niche taxonomy** (309 niches) — audience, pain points, monetisation, content formats, subtopics
2. **Gemini Flash** fills strict JSON schemas with niche-aware content
3. **Validated JSON** → 13,000+ type-safe content files
4. **20+ specialised React renderers** per content type

### 6 Content Categories

- Resource pages (34 content types × 309 niches = 7,600+ pages) — idea lists, checklists, calendars, guides, templates
- Free tools (actual working tools with niche-specific examples)
- Comparison pages (smallest category, only 1%)
- Blog name ideas
- AI content guides
- Tool alternative pages

### Why It Works (Not Spam)

- Pages are structured and functional (filtering, checkboxes, copy-to-clipboard, real tools)
- Every content type has its own purpose-built React component with proper UX, schema markup, breadcrumbs, FAQ schema
- Test: "Would this still be useful if search engines didn't exist?"

### Key Technical Details

- **Titles are NOT AI-generated** — deterministic templates like "100 Blog Post Ideas for Travel Bloggers in 2026"
- **100 concurrent workers** — bottleneck is API rate limits, not model speed
- **Niche context injection** — same schema produces completely different substance per niche (health checklist focuses on E-E-A-T/YMYL, travel checklist focuses on seasonal keywords)
- **Content and design are separate** — can redesign the site without regenerating any content

### Example Schema (Simplified)

```json
interface ResourceArticle {
  meta: { content_type, niche },
  seo: { title (templated), description, keywords[] },
  content: {
    intro,
    sections: [{
      heading,
      items (15-20 per section): [{
        title, description,
        difficulty: beginner|intermediate|advanced,
        potential: high|medium|standard
      }]
    }],
    pro_tips (exactly 5)
  }
}
```

### Results (60 Days)

- 971 → 5,500 weekly clicks (+466%)
- ~50% pages indexed (still growing)
- No negative signals from Google's helpful content updates
- Resource pages drove most traffic
- Free tools had highest engagement

### Lessons

- Spend ~60% of time on niche taxonomy — it's the foundation
- Resource pages and tools beat comparison pages
- Ship in batches for progressive rollout
- Use native JSON output (Gemini Flash) to eliminate parsing issues
- Invest in the frontend — purpose-built components make pages actually useful
- The feedback loop matters more than page count: learn which niches/content types perform, feed data back into taxonomy

> "AI content should be built, not written."
