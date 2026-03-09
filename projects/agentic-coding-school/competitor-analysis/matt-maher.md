---
source: "I Went Deep on Claude Code—These Are My Top 13 Tricks"
channel: Matt Maher
video_id: T_IYHx-9VGU
date: 2025-07-07
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] Raycast scripts that invoke Claude Code CLI as a utility** — Matt builds Raycast scripts that call `claude` headlessly from outside the terminal. His "clipboard to downloads" script takes clipboard content, sends it to Claude to determine file type and name, then saves it as a properly named file in Downloads and puts it back on clipboard. He says: "this is just us using claude as a utility at the command line or within another script essentially to give us data back and use intelligence inside of what otherwise would have just been a plain script." Ray covers headless mode but not this pattern of integrating Claude CLI into system-level automation tools like Raycast/Alfred.

- **[HIGH] Per-project sound effects using stop hooks with 11 Labs voices** — Matt creates unique audio notifications per project using hooks. He generates custom voice lines with 11 Labs (e.g., "stats up, bro") and assigns them to each project's stop hook. He says: "I don't know which one made the sound. So now I have them telling me what happened, who finished." The combination of global + project-level stop hooks playing simultaneously is a creative pattern. Ray covers hooks and the speak-to-you hook but not this multi-project notification system or the 11 Labs custom voice angle.

- **[MEDIUM] /ide slash command for Cursor/VS Code integration** — Matt shows the `/ide` command that enables Claude Code to gain reference to files open in the IDE. He says: "files that you have and things that you select will show up down below or inside of the terminal version of claude." Ray covers using Cursor + Claude Code but may not cover this specific `/ide` integration command.

- **[MEDIUM] Cmd+Escape to open Claude Code as a tab in Cursor** — Matt demonstrates using Cmd+Escape to open Claude Code as a tab rather than a parked terminal window: "it works more like a tab than it does that parked terminal window." This specific keyboard shortcut / workflow tip may not be in Ray's course.

- **[MEDIUM] Control+V (not Cmd+V) for pasting images in terminal Claude Code on Mac** — Matt highlights that image pasting in the terminal requires Control+V, not Cmd+V. He says: "weirdly in this terminal application of clawed code. If you use controlV, it'll just paste right in." This specific gotcha is useful for Mac users.

- **[MEDIUM] Design iteration slash command with parallel subagents** — Matt's `/design-iterate` command launches N concurrent subtasks, each creating a different design variant of a UI from a screenshot input. He generates 5 wildly different calculator designs (minimalist, neon cyberpunk, retro 80s, 3D isometric, emoji chaos) as standalone HTML files. While Ray covers subagents, this specific "parallel creative exploration" pattern for design iteration is a distinct workflow.

- **[LOW] Colorizing VS Code/Cursor workspaces per project using Claude Code** — Matt has a `/project-settings` global command that auto-generates VS Code settings.json to color-code each project's workspace differently. This is a small quality-of-life automation.

- **[LOW] Clipboard manager workflow for sending content to Claude Code** — Matt uses a clipboard utility (Paste) alongside Claude Code, showing how clipboard history can be dragged into prompts or screenshots can be pasted. While Ray covers screenshots, the clipboard manager integration is a workflow detail.
