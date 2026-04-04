---
tags: [script, claude-cowork, video-2]
status: draft
---

## Video 2 — Your First Folder & Task

**Goal**: Viewer gives CoWork access to a folder and watches it complete a real task — organizing messy files.

---

### HOOK (0:00–0:30)

> "In the last video we installed Claude CoWork. Now it's time to actually use it. I'm going to give CoWork access to a messy folder on my computer, ask it to organize everything, and you're going to watch it work in real time. This is the moment it clicks — when you see an AI actually moving files around on your machine."

---

### SECTION 1: Giving CoWork Access to a Folder (0:30–3:00)

**On screen**: CoWork interface, about to select a folder.

> "CoWork can't touch anything on your computer until you give it explicit permission. This is important — it's not scanning your whole drive. You choose exactly which folders it can access."

**Step 1: Click "Work in a folder"**
- Show the dropdown
- > "You'll see this option at the top. Click it and you'll get a file picker."

**Step 2: Choose a folder**
- For this demo, select the Desktop or Downloads folder
- > "For this first task, I'm going to select my Downloads folder because — let's be honest — it's a mess. Screenshots mixed with PDFs, random installers, duplicate files. Sound familiar?"

**Step 3: The permission prompt**
- Show the "Allow Claude to make changes" dialog
- Explain the options: "Allow once" vs "Always allow"
- > "This is the permission gate. CoWork is asking: can I read, write, and modify files in this folder? For now, click 'Always allow' so it doesn't ask every single time. But understand what this means — anything inside this folder, CoWork can move, rename, or delete."

**Important safety note**:
> "A tip from experience: when you're first getting started, keep backups of important files. CoWork is good, but it's not perfect. If it moves something you didn't want moved, you want to be able to get it back. As you build trust, you'll worry about this less."

**Reference from competitors**: Bart recommends "when you're first getting started with Claude CoWork, keep duplicates of any important files in case they're accidentally deleted." Mikey emphasizes "do not grant everything just because it's faster. Give it access only to what you need."

---

### SECTION 2: Your First Task — Organize Files (3:00–7:00)

**On screen**: The messy Downloads folder visible in Finder/Explorer alongside CoWork.

> "Alright, let's give CoWork its first real job."

**Step 1: Write the task prompt**

Type into CoWork:
```
I have a messy Downloads folder. Can you please:
1. Sort all files into subfolders by type (documents, images, videos, installers, archives)
2. Rename any files with gibberish names to something descriptive
3. Delete any obvious duplicates
4. Give me a summary of what you organized when you're done
```

> "Notice I'm being specific. I'm not saying 'clean up my stuff.' I'm telling it exactly what I want: sort by type, rename, delete duplicates, give me a summary. The more specific you are, the better the result."

**Step 2: Watch CoWork create a plan**
- Show the plan appearing in the sidebar
- CoWork will break it into subtasks:
  - Scan folder contents
  - Categorize files by type
  - Create subfolders
  - Move files
  - Identify and remove duplicates
  - Generate summary

> "See this? Before it touches a single file, it made a plan. You can read through this and make sure you're happy before it starts executing. This is your safety net."

**Step 3: Watch it execute**
- Show the progress bar updating
- Show files actually moving in Finder/Explorer (split screen)
- > "Watch the Finder window on the right. See the files moving? That's CoWork actually reorganizing your computer in real time. It's not just telling you what to do — it's doing it."

**Step 4: Review the result**
- Show the organized folder structure
- Show the summary CoWork provides
- > "And just like that — documents in one folder, images in another, videos separated out, installers grouped. And it gave us a summary: 47 files sorted, 3 duplicates removed, 12 files renamed."

**Reference from competitors**: Tim demos desktop cleanup with color-coded folders. Mikey does a Downloads folder organization. Both get good results but don't show the plan step or the summary — include those for completeness.

---

### SECTION 3: Understanding What Just Happened (7:00–9:00)

**On screen**: Back in CoWork, scrolling through the task log.

> "Let's look at what CoWork actually did under the hood, because this is important for understanding how it works."

**Walk through the task log**:

1. **It scanned first** — read every file name, file type, and file size
2. **It made decisions** — categorized each file based on extension and content
3. **It created structure** — made the subfolders with logical names
4. **It executed** — moved files one by one
5. **It reported** — gave you a summary of actions taken

> "This is the pattern you'll see with every CoWork task: scan, plan, execute, report. Get used to this cycle because it's how CoWork thinks."

**Key concept: Sub-agents**
> "You might have noticed the task ran pretty fast. That's because CoWork can spawn sub-agents — basically copies of itself that run tasks in parallel. Instead of moving one file at a time, it might have three or four sub-agents working simultaneously. You'll see this more in complex tasks."

**Reference from competitors**: Tim explains sub-agents as "another agent or version of Claude running in the background — you can run multiple at the exact same time." Jack Roberts notes "CoWork can spin off multiple tasks in parallel — this means Claude CoWork can actually produce massive amounts of work in a short period of time."

---

### SECTION 4: A Second Task — Something More Useful (9:00–12:00)

**On screen**: CoWork ready for a new task.

> "File organization is a nice demo, but let's do something you'd actually use in real life."

**Demo: Summarize a batch of PDFs**

Set up: Have 5-10 PDF files in a folder (invoices, reports, articles — whatever feels natural).

Type into CoWork:
```
In this folder I have a bunch of PDF documents. Can you please:
1. Read through each one
2. Create a spreadsheet that lists: filename, document type, key details, and a one-line summary
3. Save the spreadsheet as summary.xlsx in the same folder
```

- Show CoWork processing each PDF
- Show it creating the Excel file
- Open the spreadsheet and show the result

> "This is where it gets real. I just gave CoWork 8 invoices and in about two minutes it read every single one, extracted the vendor name, the amount, the date, and summarized them in a spreadsheet. That would have taken me 20 minutes manually."

**Reference from competitors**: Bart does an invoice processing demo where CoWork "categorizes invoices into subfolders and creates an Excel sheet listing every invoice separated by category, total, tax, and subtotal." Same concept, show it working end to end.

---

### SECTION 5: Tips for Writing Good Task Prompts (12:00–13:30)

**On screen**: Side-by-side comparison of bad vs good prompts.

> "Before we wrap up, here's what I've learned about giving CoWork instructions."

**Bad prompt**:
```
Clean up my files
```

**Good prompt**:
```
Sort all files in this folder into subfolders by file type. 
Create folders called Documents, Images, Videos, and Other.
Move each file into the appropriate folder.
Give me a count of how many files went into each folder.
```

**Rules of thumb**:
1. **Be specific about the outcome** — what should the end state look like?
2. **Number your steps** — CoWork follows numbered lists really well
3. **Ask for a summary** — always ask it to report what it did so you can verify
4. **Set boundaries** — if there are files it shouldn't touch, say so explicitly

> "Think of it like delegating to a new hire on their first day. They're smart, but they don't know your preferences yet. The more context you give, the better the result."

**Reference from competitors**: Mikey emphasizes "if you give vague instructions, the interface feels slow and unfocused. If you give structured goals with clear outcomes, it feels extremely efficient."

---

### OUTRO (13:30–14:00)

> "You've now given CoWork access to your files and watched it complete two real tasks. You can see the pattern: tell it what you want, it makes a plan, it executes, it reports back. In the next video, we're going to look at when you should use CoWork versus regular Claude chat versus Claude Code — because picking the wrong tool wastes time and credits."

---

### NOTES FOR FILMING

- Pre-load the Downloads folder with a genuine mess (or create one that looks realistic)
- Have the PDF invoices ready — use realistic-looking ones (ChatGPT-generated is fine)
- Split screen: CoWork on the left, Finder/Explorer on the right so viewers can see files moving
- Show the spreadsheet output in Excel/Numbers — viewers need to see the final deliverable
- Target length: ~14 minutes
