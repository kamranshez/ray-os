---
tags: [strategy, revenue, agentic-coding-school, actions]
date: 2026-04-08
---

## Revenue Actions — Direct Money Moves

Filtered for ideas that generate revenue, not "improve quality" or "increase retention." Each one either brings in new customers, extracts more from existing ones, or opens a new revenue line.

---

### 1. Team Pricing Push

Already built. Undermarketed. The infrastructure exists — tiered volume discounts (30% off at 5 seats, 40% at 10, 50% at 20+) with self-serve checkout at `/for-teams`.

**Why this is money left on the table:** Tyler McGinnis built his company around team plans. Total TypeScript found that "adding the React module is often a no-brainer for folks buying for their teams." Kyle Shevlin called team licenses "an obvious way to increase revenue and distribution." Companies have training budgets — $1,000-5,000 on a team license is pocket change compared to a single day of consulting.

**Moves:**
- Email your 3,151 students: "Does your team use Claude Code? Get them up to speed — team licenses start at 30% off." One email, direct link to `/for-teams`.
- Add a "Buy for your team" upsell on the post-purchase / member dashboard page. Catch people right after they've validated the product for themselves.
- Collect company names from student signups (you already show company logos on the marquee). Reach out to companies with 2+ individual buyers — they're already paying retail for something they could get at volume discount.
- Add a Slack/LinkedIn outreach template students can send to their manager: "Hey, I found this Claude Code training. Here's the team pricing page." Remove the friction of the internal sell.
- The $1,000/hr consulting rate on the team page is a strong anchor — it makes the per-seat license feel like nothing.

**Expected range:** A single 10-seat team deal at ~$150/seat = $1,500. Five of those = $7,500. One enterprise deal at 50+ seats could be $5-10K alone.

---

### 2. Publish Course Lessons as SEO Blog Posts

Josh Comeau published 5-6 actual course lessons as blog posts. His blog was his **#1 conversion driver** — higher than email, higher than Twitter. The posts had full interactivity, embedded widgets, and a CTA at the bottom: "This was a lesson from the course."

**Why this works:** Every blog post is a permanent, indexed sales page. Someone Googles "how to use Claude Code subagents" → finds your lesson → sees it's from a 213-lesson course → checks out. This compounds over time with zero ongoing cost.

**Moves:**
- Pick 5-10 lessons that stand alone as complete, valuable tutorials. Good candidates: anything people frequently Google about Claude Code (MCP setup, subagents, hooks, CLAUDE.md, context engineering basics).
- Publish at `/blog/[slug]` with the video embedded (use the `is_free` flag), a written summary with code snippets, and a CTA: "This is 1 of 213 lessons in Master Claude Code."
- Optimize titles for search: "How to Set Up MCP Servers in Claude Code (Complete Guide)" not "Lesson 47: MCP Servers."
- Interlink between published lessons — each one should reference 2-3 others with "want to go deeper?" links that point back to the course.
- Add email capture to each post for people who aren't ready to buy: "Get the Claude Code cheat sheet" or "Weekly tips from Ray."

**Expected range:** Comeau had 50-60K monthly visits from blog content at course launch. Even 5-10K monthly organic visits at a 1-2% conversion rate = 50-200 new customers/year from a one-time effort.

---

### 3. Demand Survey Before Building the Next Class

Matt D. Smith asked his list "which of these 4 ideas?" — constrained choice, not open-ended. Mark Shust found that topics free followers wanted were **completely different** from what paying customers wanted. Jorge Vergara: don't ask "what do you want me to build?" — ask "which of these are you struggling with?"

**Why this is a revenue move:** Building the wrong class first means months of recording time with a smaller launch. Building the right one maximizes day-one revenue. If Skills has 3x the demand of CoWork, you want to know that before committing.

**Moves:**
- One email to 3,151 students. Subject: "What should I build next?"
- Body: "I'm recording the next class. Which would you take first?" with 4 options: (1) Claude Skills — build and chain custom skills for business automation (2) Claude Chat — master the Claude.ai interface (3) Claude CoWork — desktop CoWork mode for non-developers (4) DevBoxes — running Claude in sandboxed environments.
- Add a text field: "What's the #1 thing you wish the course covered that it doesn't?"
- Send to paying customers only — not YouTube subscribers, not free trial users. Paying customers tell you what people will actually pay for.
- Secondary signal: which option gets the most replies (not just votes) has the most emotional energy behind it.

**Expected range:** This doesn't generate revenue directly — it prevents you from wasting 2-3 months building the wrong thing. The opportunity cost of building CoWork when students wanted Skills could be $20-50K+ in launch revenue difference.

---

### 4. Announce a Price Increase (Then Do It)

Marie Poulin raised her price by $100 and saw **zero change in signups**. Then raised again. Joel Hooks: "The programming course market is grossly undercharging by an order of magnitude relative to career value."

**Why this is direct revenue:** A price increase announcement is the single strongest urgency mechanism that isn't manufactured. "Price goes up on May 1" converts fence-sitters immediately. And after the increase, every future sale is worth more.

**Moves:**
- Announce lifetime going from current price to $449 (or $499) in 3 weeks.
- Email sequence: announcement → reminder at 1 week → final reminder at 48 hours.
- Show the countdown on the landing page pricing cards.
- After the increase: if conversion doesn't drop, it was underpriced. If it drops slightly, total revenue likely still increases because the higher price more than compensates.
- Matt Pocock priced at $490 specifically to stay under the $500 corporate card threshold — that's your ceiling for self-serve.

**Expected range:** The announcement itself drives a surge (Total TypeScript's pre-release urgency drove $415K). Even without a surge, raising lifetime from ~$294 to $449 on 80%+ of sales is ~$155 more per buyer permanently.

---

### 5. Black Friday / Seasonal Sale

Marcy Sutton ran a Black Friday sale for **one full week** (to allow time for company approval processes). Result: 110 purchases during the week — a spike event on an existing product with no new content.

**Moves:**
- Plan a sale for a natural moment: Black Friday, New Year ("level up in 2027"), or tied to a Claude Code major release.
- Run it for a full week, not 24 hours — Marcy's insight is that companies need procurement time.
- Discount the annual plan (not lifetime — you want recurring revenue). 30-40% off annual for one week.
- Email the full list including lapsed subscribers and non-buyers from your email capture.

**Expected range:** 50-150 purchases at discounted annual rate during the sale week. Even at 30% off $199 = $139 x 100 = $13,900 in a week, with those customers renewing at full price next year.

---

### 6. Affiliate Program Activation

Rewardful is already integrated. Affiliates can sign up from the member dashboard. But having the infrastructure isn't the same as activating it.

**Moves:**
- Email your top students (most active, most engaged) directly: "Want to earn money recommending the course? Here's your affiliate link." Personal outreach converts better than a self-serve signup page.
- Reach out to Claude Code YouTubers, newsletter writers, and Twitter/X accounts in the AI coding space. Offer them a meaningful commission (30-40%) — it costs you nothing unless they sell.
- Create a simple affiliate resource kit: a paragraph of copy they can paste, a few social images, and their tracking link. Remove friction.
- Wes Bos and Scott Tolinski use "shameless plugs" at the end of every Syntax FM episode. If you appear on podcasts or other creators' channels, always drop the affiliate-friendly URL.

**Expected range:** Even 10 active affiliates each driving 2-3 sales/month = 20-30 additional sales/month. At $199 annual, that's $4-6K/month in new revenue you didn't have to market for.

---

### 7. Corporate Expensing Frictionless Path

The landing page playbook mentions this in the FAQ section, but it deserves its own push. Matt Pocock priced at $490 specifically for the corporate card threshold. You already have an `/expense` page.

**Moves:**
- Make the `/expense` page do the work: pre-written email template the student can send to their manager, with ROI framing ("if this saves me 2 hours/week, that's $5,200/year at $50/hr — the course costs $199").
- Add "Company name" and "Company address" to the checkout flow for invoice generation — some companies require a proper invoice, not just a Stripe receipt.
- Surface the expensing option prominently on the pricing cards: "Most developers can expense this without manager approval" next to the annual price.
- Add a "Need a quote for your manager?" button that generates a PDF with course details, ROI calculation, and company logos of current students.

**Expected range:** This doesn't create new demand — it converts people who want to buy but need their company to pay. Even converting 10% more of your "scrolled to pricing but didn't buy" visitors (265 per month) = 26 additional purchases/month.

---

### 8. In-Course Upsell When New Classes Ship

Brennan Dunn built his platform specifically to support in-course product promotion: attach a product to a specific lesson, show grayed-out premium content to lower-tier buyers, surface related products based on what a learner is studying.

**Moves:**
- When Skills class ships, add a banner/card inside relevant Claude Code lessons: "Want to go deeper on skills? The new Skills class covers building, chaining, and selling custom skills." Direct link to checkout.
- For lifetime buyers (who got the core class): show them a discounted upgrade path, not the full price. They already trust you — the conversion rate will be high.
- Cross-reference between classes: a student watching the hooks lesson in Claude Code should see "Related: the hooks-with-skills lesson in the Skills class."

**Expected range:** Brennan's in-course upsells converted at significantly higher rates than cold traffic because the buyer is already engaged and trusting. Even a 5-10% conversion rate on your 3,151 existing students for a $99-149 add-on = $15-47K per new class launch.

---

### 9. Newsletter Sponsorships

Wes Bos's Syntax FM earns independent sponsor revenue alongside course promotion. Tyler McGinnis's Bytes newsletter is a top company priority partly because it's a standalone revenue line.

**Moves:**
- Once your newsletter has 2,000+ subscribers (developer audience, AI/Claude Code niche), approach relevant sponsors: AI tool companies, dev tool startups, hosting providers.
- Even a modest $200-500/issue sponsorship on a weekly newsletter = $10-25K/year for content you're already producing.
- This is revenue that doesn't cannibalize course sales — it's additive.

**Expected range:** Small at first ($200-500/issue), growing with list size. The real value is that it makes the newsletter self-sustaining, which keeps your email list (your #1 launch asset) growing.

---

## Priority Sequence

**This week (1-2 hours each):**
1. Send the demand survey (#3) — takes 30 minutes, informs everything else
2. Send the team pricing email (#1) — one email to existing students
3. Activate 10 affiliates (#6) — personal outreach to engaged students

**This month:**
4. Announce price increase (#4) — 3-week countdown, then raise lifetime
5. Publish first 5 blog posts (#2) — pick lessons, optimize for SEO
6. Improve the `/expense` page (#7) — manager email template, quote generator

**Next quarter:**
7. Plan a seasonal sale (#5) — tied to a natural moment
8. Build in-course upsell infrastructure (#8) — ready for when Skills ships
9. Launch paid beta for Skills class — 100 seats
10. Newsletter sponsorships (#9) — once list hits 2,000+
