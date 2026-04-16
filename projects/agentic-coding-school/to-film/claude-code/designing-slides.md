## The 5-step process

1. Write a script (word for word, or structured outline with bullets)
2. Create a Claude Project so it's reusable
3. Generate + iterate 1 to 2 times inside the Claude chat
4. Download the HTML, iterate locally in Cursor or Claude Code
5. Present, or share via GitHub Pages

## Why code (not PowerPoint or Google Slides)

- Truly unique output. Animated visualizations, diagrams, charts. PPT and Slides are boxed in by the tools.
- Code is AI's superpower right now. Lean into it.
- If the format has to match a corporate template, that's the one case to use a Claude Skill with PPT/Google Slides instead. Point to the "I fixed AI document formatting with one Claude feature" video.

## Step 1: Script

- The AI needs something to build visuals from.
- Word for word works. Structured outline with bullets and sub-bullets also works.
- This is the foundation. Skipping it gives you generic output.

## Step 2: Claude Project

- Why a project: reusable. Drop in a new transcript, get a consistent, high-quality deck every time.
- Create it: claude.ai sidebar, Projects, New project, name it (e.g. "slides creator v2").
- The project screen has 3 things that matter: title, chat, instructions (system prompt on the right).

### System prompt

- Don't write it from scratch. Draft a base prompt, then run it through the prompt improver at console.anthropic.com.
- Sign in, click Generate Prompt, check the "enable thinking" box, paste your base prompt, generate. It injects Anthropic's prompt engineering best practices.
- Key requirements to bake into the prompt:
    - Single HTML file (emphasize this multiple times; otherwise you get a multi-file mess)
    - Minimal text per slide
    - Maximum visual impact per slide
    - Prioritize charts, diagrams, visuals over text
    - High contrast (dark background, light foreground)
    - Single accent color per slide for focal point
    - Modern, minimalistic look
    - Navigational structure
- The prompt improver adds a scratchpad section. Keep it. That's the model thinking before generating.

## Step 3: Generate + iterate in chat

- Model: Opus 4.5 with extended thinking on.
- Tested Gemini 3 Pro, GPT 5.2 extended thinking, Opus 4.5 over the last 3 weeks. Opus 4.5 wins consistently. Revisit every few months.
- First message: paste the script below a line break. Above the line break, add any dictated reminders (minimalism, high contrast, single accent color, modern minimalist look). Optional, since it's in the system prompt, but helps lock behavior.
- First generation takes 2 to 5 minutes.

### Iteration rule: max 1 to 2 rounds in chat

- Every turn fills the context window. Full context = dumber model.
- After 2 iterations, move to local.

### Apple Notes dictation trick for batching edits

- Open an Apple note. Walk through the deck slide by slide.
- Dictate every change you want ("delete slides 1 and 2", "change the accent on slide 5", etc.) into the note.
- When done, paste the full batch into Claude in one message. Don't ask for one change at a time.

## Step 4: Iterate locally

- Download the HTML from Claude (dropdown on the artifact, Download).
- Put the file in its own folder on your desktop.
- Tool options:
    - **Cursor**: recommended default. cursor.com, download for your OS, $20/mo beginner plan gets you extended access to high-end models. Free works with limits.
    - **Claude Code**: more technical (terminal-based). Better for advanced users.

### Match the model to the task

- Small tweaks (fonts, colors, rounded corners): Cursor's Composer model. Fast + cheap.
- Big structural changes (redesign a diagram, rethink a visual): Opus 4.5.
- Multiple changes in one shot (5 to 10 at once): Opus 4.5. Higher shot at one-try success.

### Cursor setup walkthrough

- Open Cursor, open the folder that has the HTML.
- Layout: left = file explorer, center = code, right = AI chat.
- Turn off "Auto" model toggle to expose model picker.
- Open the Browser tab (globe icon). Paste the file path URL from your local browser into Cursor's browser. You'll get an error on first load. Screenshot it, copy the error details, drop both into the chat, ask it to fix so the presentation renders inside Cursor. 10 seconds.

### Select element feature (top right, mouse-in-a-box icon)

- Click it, hover, click the element you want to change.
- It auto-inserts a reference to that specific code section into the chat.
- Focuses the AI's attention on exactly what to change. Higher one-shot success.

### Embedding images

- Images must live in the same folder as index.html.
- In the chat, @mention each image to put it in context.
- Dictate what you want: "add both images to slide 8, place them in the correct boxes, size them proportionally."

## Step 5: Share via GitHub Pages

- Create a GitHub account.
- Profile > Repositories > New. Name it, make it public, create.
- Upload existing files > select your HTML + any images > Commit changes.
- Critical constraints:
    - Files must be at repo root, no nested folders
    - The HTML file must be named `index.html`
- Settings > Pages > Branch dropdown from None to Main > Save.
- Wait 2 to 5 minutes, refresh. URL appears at the top of the Pages settings.
- That's a shareable public link.

## Recap

- Script first. Claude Project for reusability. Opus 4.5 extended thinking. Max 2 iterations in chat. Download, go local with Cursor. Match model to task. Select element + @-mentioned images for precision. GitHub Pages to share.

## Outro hook (for the video)

- Slides are one format. The same reverse-engineering approach works for SOPs, proposals, contracts, any company template. Point to the Claude Skills formatting video.
