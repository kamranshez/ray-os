---
tags: [script, claude-cowork, video-8]
status: draft
---

## Video 8 — Skills

**Goal**: Viewer understands what skills are, installs one, creates one from scratch, and turns a repeated workflow into a reusable one-command skill.

---

### HOOK (0:00–0:30)

> "Every time you ask CoWork to do the same thing, you're typing the same instructions, waiting for it to figure out the same plan, burning the same credits. Skills fix that. A skill is a reusable set of instructions that you trigger with one command. Type /morning-brief and CoWork knows exactly what to do — no explaining required. In this video, I'll show you how to find skills, install them, and build your own from scratch."

---

### SECTION 1: What is a Skill? (0:30–2:30)

**On screen**: CoWork Customize → Skills panel.

> "A skill is a markdown file with instructions that teach CoWork how to do a specific job. Think of it like a recipe card."

**Analogy**:
> "Imagine you hire someone new and every day you explain the same task from scratch: go check my email, sort by priority, draft replies to the urgent ones, save a summary. That's exhausting. Instead, you write a playbook. Here's how you do email triage. Now every day, you just say 'do email triage' and they follow the playbook. That's a skill."

**What a skill file looks like** — show a simple example:

```markdown
# Morning Brief

Generate a morning briefing report:

1. Check Gmail for urgent unread emails
2. Check Google Calendar for today's schedule
3. Check Slack for messages that mention me
4. Compile everything into a formatted report
5. Save as YYYY-MM-DD-morning-brief.md in the /outputs folder

Format the report with these sections:
- Urgent Emails (need action today)
- Calendar (today's meetings and prep needed)
- Slack Highlights (anything I need to respond to)
- Top 3 Priorities for Today
```

> "It's just a markdown file. Instructions for how to complete a specific task. When you trigger the skill, CoWork reads this file and follows it."

**Reference from competitors**: Brock explains skills as "small files that teach Claude specific jobs. We can type a command and it knows exactly how to do it with no explaining required." Bart says "a skill is a way to build a repeatable AI workflow."

---

### SECTION 2: Finding and Installing Skills (2:30–5:00)

**On screen**: Skills panel in CoWork.

**Step 1: Navigate to Skills**
- Click Customize in the left sidebar
- Click Skills
- Show the skills panel

**Step 2: Browse existing skills**
- Show any pre-installed or recommended skills
- > "Anthropic includes some starter skills, and there are community skills you can browse."

**Step 3: Install a skill from a file**
- Click "Add" or "Upload a skill"
- Drag in a markdown file
- Show it appearing in the skills list

> "That's it. Drag a markdown file in and it becomes a skill. You can also share skills with other people — just send them the markdown file."

**Step 4: Install from the plugins/marketplace**
- Show the Plugins section
- Browse available plugins (collections of skills + connectors)
- > "A plugin is just a bundle of related skills. Like an 'Apollo' plugin that includes skills for lead enrichment, prospecting, and email sequences."

**Reference from competitors**: Brock offers his skills as free downloads from a Google Drive link. Jack Roberts shows the plugins marketplace with Apollo as an example. Bart shows "copy to your skills" after CoWork creates one.

---

### SECTION 3: Using a Skill (5:00–6:30)

**On screen**: CoWork task input.

> "Once a skill is installed, using it is dead simple."

**Demo: Trigger a skill**

Type into CoWork:
```
/morning-brief
```

Or just type naturally:
```
Run my morning briefing skill
```

- Show CoWork recognizing the skill
- Show it executing the steps from the skill file
- Show the output

> "One command. It knew exactly what to do because the skill file had all the instructions. I didn't have to explain anything."

**Show the difference**:
- Without skill: type 10 lines of instructions, wait for CoWork to plan
- With skill: type 1 command, CoWork already knows the plan
- > "Same result, fraction of the effort. And it'll be consistent every time because it's following the same instructions."

---

### SECTION 4: Creating a Skill from Scratch (6:30–12:00)

**On screen**: Building a skill live.

> "Now let's build a skill from scratch. I'm going to create an invoice processing skill."

**The scenario**:
> "Every week, I get a batch of invoices in a folder. I need to sort them by category, extract the totals, and create a summary spreadsheet. I've been asking CoWork to do this manually each time. Let's turn it into a skill."

**Step 1: Do the task manually first**

Type into CoWork:
```
I have several invoices in the /invoices folder. Can you:
1. Read each invoice
2. Sort them into subfolders by category (software, services, hardware, other)
3. Create a spreadsheet with columns: vendor, category, date, subtotal, tax, total
4. Add a summary row at the bottom with totals per category
5. Save the spreadsheet as invoice-summary.xlsx
```

- Show CoWork executing this
- Show the result
- > "Great, it works. Now let's capture this as a skill so I never have to type these instructions again."

**Step 2: Ask CoWork to create the skill**

Type:
```
Turn what you just did into a reusable skill. I want to be able to trigger it 
with /process-invoices. The skill should:
- Look in the /invoices folder for any new/unprocessed invoices
- Sort them into category subfolders
- Create or update the invoice-summary.xlsx spreadsheet
- Give me a summary of what was processed
```

- Show CoWork generating the skill markdown file
- Show the skill file content

> "CoWork just wrote the skill file for me based on the work it already did. This is the best way to create skills — do the task once, then have CoWork turn it into a reusable skill."

**Reference from competitors**: Bart does exactly this pattern — processes invoices manually, then says "turn this process into a reusable skill using your skill creator tool." This is the proven workflow.

**Step 3: Review and edit the skill**

- Open the skill file
- Walk through what it contains
- Make any adjustments

> "Always review the skill before you trust it. Check that the steps are in the right order, the file paths are correct, and it matches what you actually want."

**Step 4: Install and test**

- Save the skill to the skills folder
- Open a new task
- Type: `/process-invoices`
- Show it running from the skill

> "There we go. One command, and it processes all the invoices exactly the way I want. Same result every time."

---

### SECTION 5: Creating a Skill Manually (12:00–14:00)

**On screen**: Text editor with a skill file.

> "You can also write skills from scratch if you know exactly what you want."

**Demo: Create a content research skill**

Create the file manually:

```markdown
# Competitor Video Research

Research competitor YouTube videos on a given topic.

## Inputs
- Topic: the user will specify what to research

## Steps
1. Search YouTube for the topic
2. Find the top 10 videos by view count
3. For each video, note:
   - Title
   - Channel name
   - View count
   - Upload date
   - Duration
4. Identify common themes and patterns in the titles
5. Identify gaps — what's NOT being covered?
6. Save results as /research/YYYY-MM-DD-[topic]-competitor-research.md

## Output Format
Use a markdown table for the video list.
Below the table, write:
- **Common Themes**: 3-5 patterns you noticed
- **Content Gaps**: 3-5 topics nobody is covering well
- **Recommendations**: 3 video ideas based on the gaps
```

- Save the file
- Add it to skills
- Test it: "Research competitor videos on Claude CoWork"

> "This time I wrote the skill by hand instead of asking CoWork to generate it. Either approach works — use whichever feels more natural."

---

### SECTION 6: Skill Tips (14:00–15:30)

**On screen**: Tips list.

> "A few things I've learned about building good skills."

**Tip 1: Be specific about outputs**
- > "Tell the skill exactly what file to create, what format to use, and where to save it. Vague output instructions get inconsistent results."

**Tip 2: Include a section for inputs**
- > "If the skill needs information from you (like a topic or a client name), make that explicit. The skill should prompt you for anything it needs."

**Tip 3: One skill, one job**
- > "Don't create a skill that does 15 things. Make focused skills that do one thing well. You can chain them together later."

**Tip 4: Iterate**
- > "Your first version won't be perfect. Run the skill, see what it gets wrong, edit the markdown file, and run it again. After 3-4 iterations, it'll be solid."

**Tip 5: Skills save tokens**
- > "Here's something nobody talks about. A well-written skill can actually save you credits because CoWork doesn't need to plan from scratch — it already has the plan. Less thinking time means fewer tokens."

**Reference from competitors**: Bart mentions "skills in recent weeks actually evaluate that process against a set of criteria" and "get you involved so you can optimize before deploying." Jack Roberts emphasizes "avoid creating too many overlapping skills."

---

### OUTRO (15:30–16:00)

> "You now have reusable skills that turn complex workflows into one-command automations. In the next video, we're going to make these skills run on autopilot with scheduled tasks — so CoWork can work while you sleep."

---

### NOTES FOR FILMING

- The "do it manually then convert to skill" workflow is the hero demo — make it seamless
- Show the skill markdown file on screen long enough for viewers to understand the format
- Have invoices pre-loaded in the demo folder (use realistic ChatGPT-generated ones)
- The before/after comparison (manual typing vs one command) should be dramatic
- Target length: ~16 minutes
