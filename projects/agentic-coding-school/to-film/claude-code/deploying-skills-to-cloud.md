# Deploying Skills to the Cloud (Modal / Netlify)

## What This Video Covers

Taking locally-built skills, websites, and tools and deploying them to the internet so they run independently — accessible from any device, triggerable by webhooks, and shareable with clients. Modal for serverless functions (API endpoints, scheduled tasks). Netlify for static sites. Claude sets everything up from a one-line prompt.

## Why This Matters

Everything built locally on your computer is only useful while you're sitting at that computer. Deployment makes your skills accessible:
- From your phone
- By other people (clients, team members)
- By other tools (N8N, Make.com, Zapier) via webhooks
- On a schedule (cron jobs running your skills automatically)

Modal costs pennies (starts with $5 free credits — the competitor has spent $0.50 after months of use). Netlify is free for static sites.

## How the Competitor Teaches It

**Modal (serverless functions):**
1. Signs up to Modal (free $5 credits)
2. Creates an API token
3. Pastes the token into Claude Code — it installs everything
4. Deploys a simple birthday-check endpoint: visit the URL in browser → see a message
5. Then deploys the lead scraping skill as a web form: fill out "dentist / United States / 100 results" → get a CSV download
6. Shows the URL is publicly accessible from any browser

**Netlify (static sites):**
1. Deploys the proposal generator app built earlier
2. Pushes to Netlify with environment variables (Supabase, Stripe, Anthropic keys)
3. Shows the app live on a public URL with working auth, payments, and e-signatures

## Key Concepts to Cover

- Why deploy: accessibility, sharing, webhook triggers, scheduling
- **Modal:**
  - Sign up process ($5 free credits)
  - Creating an API token
  - Having Claude install and configure Modal
  - Deploying a simple endpoint (hello world / birthday check)
  - Deploying a skill as a web form (scrape leads, get CSV)
  - Cost reality: pennies per month for light usage
- **Netlify:**
  - Static site deployment for websites/apps
  - Adding environment variables in production
  - Custom domains
- Integration with no-code tools (N8N, Make.com) via webhooks
- Security considerations for public endpoints (don't expose API keys, add auth if needed)
- The workflow: build locally → test → deploy → share URL

## Demo Plan

1. Sign up to Modal, get API token
2. Give token to Claude — it sets up everything
3. Deploy a simple endpoint, visit in browser
4. Deploy a real skill (lead scraper) as a web form
5. Fill out the form, get CSV results
6. Show Netlify deployment for a website/app
7. Discuss webhook integration with N8N/Make.com

## Suggested Class Placement

Claude Code — Advanced, or Business class
