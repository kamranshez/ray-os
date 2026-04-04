---
tags: [script, claude-cowork, video-7]
status: draft
---

## Video 7 — Browser Automation (Claude in Chrome)

**Goal**: Viewer sets up the Chrome extension, pairs it with CoWork, and watches CoWork navigate the web, extract data, and interact with pages.

---

### HOOK (0:00–0:30)

> "What if Claude CoWork could use your browser? Open tabs, navigate to websites, read pages, click buttons, fill out forms — all on its own. That's exactly what Claude in Chrome does. And in this video, I'm going to set it up and show you real examples of CoWork browsing the web like a human."

---

### SECTION 1: What is Claude in Chrome? (0:30–2:00)

**On screen**: Chrome with the Claude extension visible.

> "Claude in Chrome is a Chrome extension that lets CoWork control your browser. Not in a vague 'it can search the web' way — it can literally open tabs, navigate to URLs, scroll through pages, click on elements, and read what's on screen."

**What it can do**:
- Open new tabs and navigate to any URL
- Read the content of any webpage
- Click buttons, links, and interactive elements
- Fill out forms
- Scroll through pages
- Take screenshots of what it sees
- Extract data from pages (tables, text, prices, etc.)

**What it can't do**:
- It won't work if your browser is closed
- It operates in your actual Chrome — not a hidden background browser
- It can be slow if pages are heavy or require lots of scrolling

> "The key thing to understand: when CoWork uses your browser, you can watch it happening in real time. You'll see tabs opening, pages loading, cursors moving. It's using your browser as if it was sitting at your desk."

**Reference from competitors**: Tim demos YouTube research — CoWork opens YouTube, reads recommendations, clicks into videos, extracts stats and comment sentiment. Jack Roberts uses it to navigate Granola app, find a trial extension button.

---

### SECTION 2: Setting Up Chrome Extension (2:00–4:00)

**On screen**: Full screen recording.

**Step 1: Install the extension** (if not done in Video 1)
- Open Chrome
- Go to Chrome Web Store
- Search "Claude for Chrome" or "Claude"
- Click "Add to Chrome"
- Confirm the installation

**Step 2: Enable in CoWork settings**
- Open Claude Desktop app
- Go to Settings → Claude in Chrome
- Toggle it on
- > "This tells CoWork that it's allowed to use the Chrome extension."

**Step 3: Pair the extension with CoWork**
- Click the Claude extension icon in Chrome toolbar
- It should show "Connected" or prompt you to pair
- > "The extension needs to be paired with your desktop app. Usually this happens automatically, but if not, click the extension icon and follow the pairing prompt."

**Step 4: Verify connection**
- Go back to CoWork
- Start a new task
- Check that "Claude in Chrome" appears in your connectors/context
- > "You should see Claude in Chrome listed as an available connector. If it's there, you're good to go."

**Reference from competitors**: Tim shows the full setup: "install the Claude Chrome extension, enable it from settings, pair it, and then it shows up in your connectors." Good to follow the same steps.

---

### SECTION 3: Demo 1 — Web Research (4:00–7:30)

**On screen**: Split screen — CoWork on left, Chrome on right.

> "Let's start with the most common use case: getting CoWork to research something on the web."

Type into CoWork:
```
I want you to research the top 5 AI writing tools right now. 
For each one:
1. Go to their website
2. Find their pricing
3. Note their key features
4. Check if they have a free tier

Save everything as a comparison table in ai-writing-tools.md
```

**Walk through what happens**:
- CoWork opens Chrome
- Navigates to the first tool's website
- Reads the pricing page
- Extracts features
- Moves to the next tool
- Repeat for all 5
- Show it might run some in parallel (multiple tabs)

> "Watch Chrome on the right — see it opening tabs, navigating to each site, reading the content. This isn't CoWork making stuff up from memory. It's going to each website right now and reading the actual current pricing."

- Show the final markdown file with the comparison table

> "Five tools compared with current pricing, features, and free tier status. All from actual website visits, not training data from months ago."

**Key point**:
> "This is especially important for anything time-sensitive — pricing changes, product launches, current events. Chat would use its training data which might be months old. CoWork with Chrome gets you real-time information."

---

### SECTION 4: Demo 2 — YouTube Research (7:30–10:00)

**On screen**: CoWork about to research YouTube.

> "Let me show you something more specific. I want to research what's working on YouTube in my niche."

Type into CoWork:
```
Go to YouTube and search for "Claude CoWork tutorial". 
For the top 5 results:
1. Note the title, channel name, and view count
2. Click into each video
3. Read the comments — what are people asking about? What do they like?
4. Give me a summary of what topics are covered and what gaps you see

Save as youtube-competitor-research.md
```

- Show CoWork opening YouTube
- Searching for the term
- Clicking into videos
- Scrolling through comments
- Coming back with results

> "It just analyzed 5 competitor videos, read their comments, and told me what topics are saturated and where the gaps are. That's an hour of research done in 5 minutes."

**Reference from competitors**: Tim does this exact YouTube demo — "open up my browser, go to YouTube and tell me two of the recommended videos on my home screen" then "click into both those videos and give me all the stats."

---

### SECTION 5: Demo 3 — Form Filling & Data Extraction (10:00–12:30)

**On screen**: A website with a form or data table.

> "CoWork can also interact with pages — not just read them."

**Demo: Extract data from a page**

Type into CoWork:
```
Go to [a public data source - e.g., a product comparison site or stats page].
Extract all the data from the main table on the page.
Clean it up and save it as a CSV file.
```

- Show CoWork navigating to the page
- Reading the table data
- Creating a clean CSV

> "It navigated to the page, found the data table, extracted every row, and saved it as a clean CSV. No copy-pasting, no manual cleanup."

**Demo: Fill out a form** (optional, use a test form)

> "CoWork can also fill out forms. Insurance applications, government portals, onboarding forms — anything with fields it can see. Obviously use this carefully, but it works."

**Reference from competitors**: Jack Roberts demos "fill in forms — insurance, onboarding, government portals. All that annoying admin gone." Mikey mentions "CoWork can organize your folders, check your Gmail, manage your calendar — it operates strictly within the world of what you grant access to."

---

### SECTION 6: Demo 4 — Price Monitoring (12:30–14:00)

**On screen**: CoWork running a flight search.

> "Here's a practical one. I want CoWork to search for flights."

Type into CoWork:
```
Search Google Flights for direct flights from London to Dubai 
in the next 3 months in economy class.
Find the cheapest options and give me the top 5 
with dates, airlines, and prices.
```

- Show CoWork navigating Google Flights
- Entering search criteria
- Reading results
- Compiling the top options

> "It just searched real flight prices on Google Flights. You could set this up as a scheduled task — check flights every day and alert you when prices drop."

**Reference from competitors**: Tim does a flight search demo — "search Google Flights, find direct flights from Miami to Dubai in the next six months in business class under $3,000." Good visual, viewers relate to it.

---

### SECTION 7: Tips & Limitations (14:00–15:00)

**On screen**: Bullet points.

> "A few things to know about browser automation."

**Tips**:
- CoWork works best on simple, well-structured pages
- If a page requires login, you need to be already logged in — CoWork uses your existing Chrome session
- Heavy JavaScript apps (like complex dashboards) can be tricky
- Running things in parallel (multiple tabs) is faster but uses more credits

**Limitations**:
- Your computer must be on and Chrome must be open
- CoWork can't bypass CAPTCHAs or bot-detection
- Some pages block automated browsing
- It's slower than API-based connectors — if an app has a native connector, use that instead

> "Browser automation is your last resort for getting data. If there's a connector or an API, use that — it's faster and more reliable. Browser automation is for when there's no other way in."

**Reference from competitors**: Jack Roberts ranks it: "Number one, MCPs. If it's connected via an API, it'll be a lot faster. Second, files on your computer. Only as a last resort do we want to use desktop intelligence."

---

### OUTRO (15:00–15:30)

> "CoWork can now browse the web, extract data, fill forms, and research on your behalf. Combined with connectors, it has access to your email, calendar, files, and now the entire internet. In the next video, we're going to learn about Skills — reusable workflows that turn all of this into one-click automations."

---

### NOTES FOR FILMING

- Split screen is essential for this video — viewers need to see both CoWork and Chrome simultaneously
- Pick research examples that are visually interesting (YouTube, flights, product comparisons)
- The YouTube research demo will resonate with the audience since they're watching YouTube
- Have a backup plan if a website blocks the automation — show the failure gracefully
- Target length: ~15 minutes
