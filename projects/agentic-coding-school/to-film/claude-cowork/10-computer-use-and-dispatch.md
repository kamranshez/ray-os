---
tags: [script, claude-cowork, video-10]
status: draft
---

## Video 10 — Computer Use & Dispatch

**Goal**: Viewer enables Computer Use so CoWork can control desktop apps, and sets up Dispatch to trigger tasks from their phone.

---

### HOOK (0:00–0:30)

> "So far, CoWork has been working inside its own bubble — files, connectors, browser. But what if it could control your actual desktop apps? Open Notion, click through Canva, navigate settings in any application? And what if you could trigger all of this from your phone while you're away from your desk? That's Computer Use and Dispatch. Let me show you both."

---

### SECTION 1: What is Computer Use? (0:30–2:00)

**On screen**: CoWork about to interact with a desktop app.

> "Computer Use gives CoWork the ability to see your screen and interact with it — clicking buttons, typing into fields, scrolling through apps. It's like giving CoWork a pair of eyes and hands on your desktop."

**How it works**:
- CoWork takes screenshots of your screen
- It identifies UI elements (buttons, text fields, menus)
- It can click, type, scroll, and navigate
- It works with ANY app — not just ones with connectors

> "This is different from connectors. A connector talks to an app through an API — fast, reliable, structured. Computer Use literally looks at your screen and clicks things like a human would. It's slower and less precise, but it works with everything."

**When to use Computer Use vs Connectors**:
- App has a connector → use the connector (faster, more reliable)
- App has NO connector → use Computer Use
- Need to do something visual (design tools, complex UIs) → Computer Use

---

### SECTION 2: Enabling Computer Use (2:00–3:30)

**On screen**: Settings screen.

**Step 1: Open Settings**
- Click your avatar → Settings
- Go to General

**Step 2: Enable Computer Use**
- Find "Computer Use" toggle
- Turn it on
- Also enable "Unhide apps when Claude finishes" (optional — brings apps to foreground)

> "That's it. Two toggles. Now CoWork can see and interact with your desktop."

**Reference from competitors**: Jack Roberts shows this exact setup: "come down to settings, general, make sure you've enabled Computer Use and unhide apps when Claude finishes."

---

### SECTION 3: Demo 1 — Navigating a Desktop App (3:30–7:00)

**On screen**: CoWork + a desktop app (e.g., Notion, Notes, or any app the viewer would recognize).

> "Let's start simple. I'm going to ask CoWork to do something inside a desktop app."

**Demo: Find something in a desktop app**

Type into CoWork:
```
Open Notion on my computer and find my "Weekly Tasks" page. 
Tell me what tasks are listed there.
```

- Show CoWork activating Computer Use
- Show it taking control of the screen
- Show Notion opening (or switching to it)
- Show CoWork navigating through the sidebar
- Show it finding the page and reading the content

> "Watch my screen — I'm not touching anything. CoWork just opened Notion, navigated to the right page, and read my tasks. It's seeing my screen and clicking through the UI."

**Demo: Interact with a design tool**

Type into CoWork:
```
Open Canva and find my most recent design. 
Take a screenshot of it and save it to my project folder.
```

- Show CoWork opening Canva
- Navigating to recent designs
- Screenshotting and saving

> "This is huge for non-technical users. You don't need APIs or connectors. If you can see it on your screen, CoWork can interact with it."

**Reference from competitors**: Jack Roberts does a Granola demo: "go to my app Granola and find a section where I can extend my free trial." Also a Canva demo where CoWork finds a specific design, exports it, and emails it.

---

### SECTION 4: Demo 2 — Form Filling (7:00–9:00)

**On screen**: A form in a desktop app or web browser.

> "One of the most practical uses: filling out forms."

Type into CoWork:
```
I need to fill out a supplier onboarding form. The form is open in my browser.
Here are the details:
- Company: [Your Company]
- Contact: [Your Name]
- Email: [Your Email]
- Phone: [Your Phone]
- Address: [Your Address]
Fill in all the fields and stop before submitting — I want to review first.
```

- Show CoWork tabbing through form fields
- Filling in each field
- Stopping at the submit button

> "It filled every field and stopped before submitting — exactly as I asked. Government forms, insurance applications, vendor onboarding — any form you hate filling out, CoWork can do it."

---

### SECTION 5: Computer Use Limitations (9:00–10:00)

**On screen**: Bullet points.

> "Computer Use is impressive, but it's not magic. Here are the limitations."

- **It's slow** — taking screenshots, analyzing UI, clicking. Much slower than API connectors.
- **It can misclick** — complex UIs with lots of small buttons can trip it up.
- **Screen resolution matters** — if elements are tiny, CoWork might not identify them correctly.
- **It can't type passwords** — for security, it won't enter credentials.
- **Your screen is shared** — while CoWork is using Computer Use, you'll see it happening on your screen. Don't start clicking around or you'll confuse it.

> "My rule: if a connector exists, use the connector. Computer Use is the fallback for everything else."

**Reference from competitors**: Jack Roberts ranks this: "MCPs first, files second, desktop intelligence as a last resort." Good hierarchy to reinforce.

---

### SECTION 6: What is Dispatch? (10:00–11:30)

**On screen**: Phone showing Claude app.

> "Now let's talk about Dispatch. This is how you control CoWork from your phone."

**What is Dispatch?**
- A feature in the Claude mobile app
- You send a task from your phone
- It runs on your desktop (which must be on and running Claude)
- You get the result back on your phone

> "You're at a coffee shop. You remember you need a report compiled. You open Claude on your phone, dispatch the task, and your desktop CoWork handles it. You get the result on your phone 5 minutes later."

**Requirements**:
- Claude mobile app installed (iOS or Android)
- Same account on phone and desktop
- Desktop must be on with Claude open
- Dispatch enabled in settings

---

### SECTION 7: Setting Up Dispatch (11:30–13:00)

**On screen**: Settings on desktop, then phone.

**Step 1: Enable Dispatch on desktop**
- Settings → CoWork → Enable Dispatch
- Toggle it on

**Step 2: Connect your phone**
- Open Claude app on your phone
- Sign in with the same account
- The phone and desktop should pair automatically
- > "Once they're on the same account, they find each other. You should see a Dispatch option appear in the mobile app."

**Step 3: Test it**
- On your phone, open Claude
- Look for the Dispatch option
- Type a simple task: "What files are in my Desktop folder?"
- Show it executing on the desktop
- Show the result coming back to your phone

> "I just asked my phone what's on my desktop, and the desktop CoWork read the folder and sent the answer back to my phone. The phone is just the remote control — the work happens on your computer."

**Reference from competitors**: Tim mentions "you can use CoWork from mobile — if your computer is open and you go on your phone, you can trigger CoWork to do something." Jack Roberts demos it with the Canva example — he's "at a coffee shop" and triggers CoWork to grab a design and email it.

---

### SECTION 8: Demo — Dispatch in Action (13:00–15:00)

**On screen**: Phone on one side, desktop on the other (picture-in-picture or split screen).

> "Let me show you a real use case."

**Scenario**: You're away from your desk and remember you need to send a file to someone.

On your phone, dispatch:
```
Go into my project folder, find the latest client report PDF, 
and draft an email to [client@email.com] with the report attached. 
Subject: "Monthly Report — April 2026". 
Don't send it — just create the draft.
```

- Show the task appearing on the desktop
- Show CoWork finding the file
- Show it drafting the email in Gmail
- Show the confirmation coming back to the phone

> "I was away from my desk, triggered the task from my phone, and CoWork found the file, drafted the email, and it's sitting in my Gmail drafts ready to review when I get back."

**More Dispatch ideas**:
- "Check my calendar and tell me when my next meeting is"
- "Run my morning briefing skill"
- "Create a new document in my project folder with these notes: [dictate notes]"
- "What unread emails do I have from [client name]?"

---

### SECTION 9: Tips for Computer Use & Dispatch (15:00–16:00)

**On screen**: Tips list.

**Computer Use tips**:
- Close unnecessary apps to reduce screen clutter
- Keep the app you want CoWork to use in the foreground
- Don't touch your mouse/keyboard while CoWork is using the screen
- Use simple, specific instructions — "click the blue button that says Submit" is better than "submit the form"

**Dispatch tips**:
- Keep tasks self-contained — Dispatch works best when CoWork doesn't need to ask you questions
- Use skills with Dispatch — "Run /morning-brief" is a perfect Dispatch task
- Remember: your computer must be on — if your laptop is in your bag closed, Dispatch won't work

---

### OUTRO (16:00–16:30)

> "CoWork can now control your desktop apps, fill out forms, and you can trigger it all from your phone. In the final video of this course, I'm going to put everything together — projects, instructions, connectors, skills, scheduled tasks, and Dispatch — into one complete automated workflow. That's where CoWork truly becomes your AI employee."

---

### NOTES FOR FILMING

- Computer Use demos need a clean desktop — close all unnecessary apps
- Film the phone demos with the phone visible on screen (picture-in-picture or camera angle showing phone)
- The Canva/Notion demos are visually compelling — viewers can see CoWork clicking through real apps
- Dispatch needs dual-screen recording — phone AND desktop simultaneously
- Target length: ~16 minutes
