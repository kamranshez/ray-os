---
class: "skills"
chapter: "Build Your AI Employees"
status: "new"
tags: [course, script, skills]
lesson: "4.3 The Operations Manager"
---

## The Operations Manager

In the last video we built a content director — a creative employee. This video is the opposite. We're building the boring employee. The one that handles receipts, invoices, and expense tracking. The stuff nobody wants to do but everybody needs done.

I'll be honest — I'd rather build five apps than spend 30 minutes looking at a spreadsheet. So I built skills that handle the spreadsheets for me.

### The Receipt Scanner (0:00–3:30)

Here's the scenario. You've got a folder on your desktop where you dump receipts. Photos from your phone, PDFs from email, screenshots of online purchases. They pile up all week.

> [SCREEN: a folder on desktop with ~10 receipt images/PDFs]

Right now, organizing these is a manual job. Open each one, type the amount into a spreadsheet, categorize it. Maybe an hour every week if you're disciplined about it. Most people just... don't do it. Then tax time comes and it's a nightmare.

So we build a skill.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build a receipt scanner skill. Given a folder of receipt images and PDFs, read every receipt, extract the vendor name, date, amount, tax, and category. Generate two outputs: a spreadsheet with all the data, and an HTML expense dashboard with total spend, average per receipt, total tax paid, and a breakdown by category."]

Skill Creator asks a few questions. "What categories do you want? How should it handle unclear receipts? Do you want it to flag anything suspicious?" I tell it my categories — software, meals, travel, office supplies, miscellaneous. Flag anything over $500 for review.

> [SHOW: the skill being built]

Now I point it at my receipts folder.

> [TYPE: "Scan all receipts in ~/Desktop/receipts/"]

> [SHOW: Claude processing — reading each receipt, extracting data]

It's reading every receipt. Using vision to parse the images, reading the PDFs directly. Extracting vendor, date, amount, tax, assigning categories.

> [SHOW: the two outputs — spreadsheet and HTML dashboard]

Two outputs. A spreadsheet with every receipt as a row — vendor, date, amount, tax, category. All sorted by date. And an HTML dashboard.

> [SHOW: the dashboard in a browser — total spend, tax paid, category breakdown with a chart]

Total spend this week. Total tax paid. Average per receipt. Category breakdown — most of it's software subscriptions and meals. This would've taken me an hour manually. The skill did it in about 30 seconds.

And the best part — we'll turn this into a scheduled task in Chapter 6 so it runs every Friday at 5pm automatically. Drop receipts in the folder all week, forget about them, get a dashboard every Friday.

### The Invoice Generator (3:30–6:00)

Now the other side of finances — getting paid.

I used to dread invoicing. Open the invoicing software, find the template, fill in the client details, line-item everything, export as PDF, email it. Fifteen minutes minimum per invoice. And I'd always procrastinate on it.

So I built an invoice skill.

> [SCREEN: Claude terminal]

> [TYPE: /skill-creator]

> [TYPE: "Build an invoice generator skill. Given a client name, project description, and amount, generate a professional PDF invoice. Pre-fill my business name, address, bank details, and logo from brand-context/. Auto-generate an invoice number. Include payment terms — net 30."]

The key here is that the skill pulls from the brand context folder we set up in Chapter 3. My logo, my colors, my business details — all pre-loaded. I never type them again.

> [SHOW: the skill — skill.md with the process, references pointing to brand-context/]

Now let me generate an invoice.

> [TYPE: "Generate an invoice for Acme Corp. AI consulting project — 40 hours at $200/hour. Due in 30 days."]

> [SHOW: Claude generating the invoice]

One sentence. That's my entire input.

> [SHOW: the PDF invoice — logo, colors, business details, line items, total, payment terms]

Professional PDF. My logo in the top right. My brand colors. Business name, address, bank details — all pulled from brand context. Invoice number auto-generated. Line items broken out. Total with tax. Payment terms: net 30.

That used to be 15 minutes of software I didn't enjoy using. Now it's one sentence.

### The Financial Reporting Angle (6:00–7:30)

Now if you combine the receipt scanner and the invoice generator, you've got both sides of your finances covered. Money in, money out. And you can build on top of that.

A financial reporting skill that takes your expense data and your invoice data and produces a monthly P&L. A budget planner that shows you projected savings based on your current income and spending patterns — interactive, where you can adjust the numbers and see how it changes.

I'm not going to build those live in this video — but the pattern is the same as everything we've done. Skill Creator, describe what you want, iterate.

The honest assessment: this isn't replacing your accountant. When tax time comes, you still need a professional. But it does something your accountant can't do — it keeps things organized in real time, every week, without you thinking about it. And that's the difference between showing up to your accountant with a box of receipts and showing up with a clean spreadsheet and monthly dashboards.

For a one-person business, that's the difference between financial chaos and financial awareness. And it costs you nothing beyond the skills you've already learned to build.

### What's Next

We've got content and operations covered. In the next video, we're building the marketing director — LinkedIn posts, email drafts, SEO content, all pulling from your brand context and running with your positioning baked in.
