---
video_id: OpM-G3WNH4g
title: "Git Worktrees + Agents:🦄 #35"
url: https://www.youtube.com/watch?v=OpM-G3WNH4g
channel: BoundaryML
---

### SUMMARY
Vibhor and Dexter from BoundaryML and HumanLayer demonstrate git worktrees, parallel coding agents, tmux orchestration, and workflows for managing multiple concurrent Claude sessions productively.

### IDEAS
- Worktrees share a single git object database while exposing different branches as separate working directories on disk simultaneously.
- Cloning a repo multiple times wastes disk space and forces juggling numbered folders with no semantic meaning attached.
- Running two coding agents in the same directory causes them to step on each other's lockfiles constantly.
- Cargo build can only run once per project at a time, making parallel agents inside one repo unworkable for Rust.
- Worktree directories let you name branches semantically, eliminating the cognitive overhead of remembering what folder-2 contained.
- The same branch cannot be checked out in two worktrees simultaneously, preventing race conditions on file writes.
- Setup scripts like make-setup must exist or worktree adoption fails because gitignored files don't transfer automatically.
- Settings.local.json and credentials must be copied into each new worktree because they are intentionally not version controlled.
- A watcher agent running in a loop can auto-merge feature branches into main, resolving conflicts via Claude.
- Pre-commit hooks requiring tests to pass become viable in agentic worktrees because slowness matters less than stability guarantees.
- Tmux can programmatically capture another pane's output, letting one Claude monitor another Claude's terminal.
- Recursive worktrees from worktrees enable fanning out subtasks while keeping branch lineage intact through the object database.
- Parallel agents work best when checkpoints are homogeneous, like research documents, rather than heterogeneous mid-task states.
- Standardizing your workflow shape lets you spawn multiple agents and evaluate them against the same comparable rubric.
- Git is like Vegas slot machines — more automation means more potential output if luck holds.
- Naming worktrees by ticket, model, or three-word description beats UUIDs because humans need semantic anchors for context recall.
- Few-shot worktree naming from three manual examples could replace deterministic templates and feel more personal.
- Markdown plans should live outside git working trees to avoid merge conflicts on non-conflict-sensitive collaborative documents.
- Doing research and planning from main, then spawning worktrees only at implementation, prevents chaotic markdown branching everywhere.
- Worktrees plus parallel models let four agents tackle the same problem in different styles for design exploration.
- Cross-model parallelism reveals design elements no single model produces, beating any single-prompt optimization Ray attempted previously.
- Time-boxing a workflow change to two weeks prevents permanent commitment while still allowing meaningful productivity comparison.
- Branch naming conventions like person/feature plus optional date prefixes help teams disambiguate complex feature work history quickly.
- The future of collaborative documents lies between Git and Google Docs — version history without distributed merging chaos.
- GitHub issues lose to dedicated doc sites because navigation, prettiness, and real-time editing dominate complex content consumption.
- Worktree prune removes already-merged branches but cannot intelligently distinguish active work-in-progress from abandoned exploration.
- Semantic branch naming through coding agents can outperform timestamps because three-word descriptions encode purpose, not chronology.
- Spec Kit pioneered the question-answer markdown format for describing new language syntax inside enhancement proposals systematically.
- Forcing yourself to stage changes after every meaningful checkpoint enables fast diff-based recovery to known-good states.
- Coding interview standardization parallels agent workflow standardization — comparable inputs yield comparable outputs across many candidates.

### INSIGHTS
- Parallelism's real value isn't six agents at once but spatial separation letting work pause cleanly until tomorrow.
- Worktrees are branches with file-system views — the mental model only clicks after weeks of practical foot-gun encounters.
- Automation tradeoff: more delegation means higher output ceiling but greater drift from your actual intent unchecked.
- Make-setup scripts are the prerequisite for worktree adoption, not nice-to-haves — without them parallel workflows collapse immediately.
- Standardized convergence shapes (plans, research docs) reduce the cognitive cost of reviewing parallel agent outputs dramatically.
- Hide complexity through wrapper scripts the team shares so individual mental models matter less than shared opinions.
- Power users want raw git access while non-engineers want UI abstraction — tools must choose their target audience deliberately.
- Run experiments time-boxed because workflow changes feel permanent but should always remain reversible after evaluation periods.
- Parallel design exploration across models surfaces variation impossible to reach through any single prompt-engineering optimization loop.
- Diff-staging discipline lets you let agents rip aggressively while maintaining cheap rollback points to recent semantic checkpoints.

### QUOTES
- "It's really just git worktree add -b branch name followed by directory name." — Dexter
- "The anxiety I had about learning git worktrees just went away because it's just one command." — Vibhor
- "More you automate and the less you look into it, the more likely it might deviate." — Dexter
- "It's kind of like walking around the Vegas casino and putting a coin in slot." — Vibhor
- "If you don't have a single script to run to set up your worktree, you will fail." — Dexter
- "Most things with Git feel completely terrifying and arcane and you don't want to learn it." — Dexter
- "Worktrees are branches. They're just a view of a branch in a file system." — Dexter
- "If you don't need this, you probably shouldn't use it." — Dexter
- "It's almost like git stash on steroids." — Dexter
- "You can prompt Claude to monitor the terminal of another Claude session." — Dexter
- "Don't try to create worktrees for each step of the workflow." — Dexter
- "I'm scared I'm going to type the wrong command and screw myself." — Vibhor
- "We treat those documents as most people aren't modifying them, you're unlikely to have merge conflicts." — Dexter
- "Spend five minutes thinking about how you want to organize it and then iterate on that." — Dexter
- "The future of this is going to look a lot more like somewhere between git and Google docs." — Dexter

### HABITS
- Stage every change after each meaningful checkpoint, never commit, then let the agent rip again.
- Run the same prompt across five different coding models in parallel for design comparison work.
- Maintain a make-setup script in every repo so worktree creation can install dependencies automatically every time.
- Commit settings.local.json copying logic into the create-worktree script for personal Claude allowances always.
- Use tmux multiplexing to manage multiple shell windows instead of overwhelming yourself with single-window terminal sessions.
- Name branches as person-name slash feature-name to make team collaboration on shared branches easier.
- Add date prefixes when naming complex features that spawn many related branches across the work cycle.
- Place all worktrees under a tilde-slash-worktree-slash-repo-name-slash-branch-name directory convention for consistent organization.
- Do research and planning from main branch only, spawning worktrees only when implementation begins seriously.
- Run code review agents on your own outputs before merging to catch quality issues automatically.
- Time-box every new workflow experiment to two weeks before deciding whether to keep or abandon it.
- Cap parallel coding agents at two maximum to prevent context-switching overhead from destroying overall productivity.
- Delete worktrees immediately after PR merge to avoid accumulating orphaned directories cluttering your filesystem.
- Use git aliases extensively to compress common multi-flag commands into memorable two-letter shortcuts daily.
- Generate parallel markdown design docs in different styles to discover the best framing through comparison.

### FACTS
- Subversion was invented by someone who was at the University of Chicago for a period.
- Mercurial was a viable Git competitor used at small companies as recently as several years ago.
- Open Code is an open-source coding agent project explored by the BoundaryML and HumanLayer teams.
- Cargo build can only execute once per project at any given moment due to lock-file constraints.
- Git worktrees share a single object database across all linked working directories on the same machine.
- The same branch cannot be checked out in two worktrees simultaneously due to race-condition prevention.
- Git worktree prune automatically removes worktrees whose branches have been merged into the current branch.
- BAML is BoundaryML's domain-specific language with roughly 300,000 lines of code plus extensive test fixtures.
- Settings.local.json in Claude Code is git-ignored to keep personal permissions separate from team-shared configurations.
- Pre-commit hooks can mandate test passage before allowing commits to land on watcher branches.
- Vibe Conductor and Conductor are existing tools that abstract worktree management into UI-driven product experiences.
- Theo published a video showcasing his AI coding workflow including the worktree setup step explicitly.
- Jeff Huber founded Chroma DB, the vector database company widely used in retrieval-augmented generation systems.
- BAML Enhancement Proposals (BEPs) follow a question-answer format for describing new language syntax features.
- The HumanLayer codebase contains many remotes, requiring scripts to manage them programmatically.

### REFERENCES
- BAML (Boundary Markup Language) by BoundaryML
- HumanLayer
- Open Code (open-source coding agent)
- Code Layer (Dexter's tool)
- Multicloud (Dexter's open-source orchestration tool from May)
- Tmux terminal multiplexer
- Mercurial version control system
- Subversion version control system
- Theo's AI coding workflow video
- Vibe Conductor (worktree management tool)
- Conductor (worktree management tool)
- Claude Desktop UI's worktree management
- Spec Kit (specification framework)
- Chroma DB and Jeff Huber interview
- JJ (Jujutsu) version control system
- CRDT-based collaborative editing concepts
- Cursor IDE
- Anti-gravity diff view
- VS Code terminal
- GitHub Issues for collaborative documentation

### ONE-SENTENCE TAKEAWAY
Worktrees unlock parallel agentic coding without disk waste — but only with disciplined naming and setup scripts.

### RECOMMENDATIONS
- Try git worktree add -b branch-name directory-name once today to demystify the entire feature instantly.
- Write a create-worktree shell script that runs make-setup and copies your local Claude settings automatically.
- Time-box switching from clones to worktrees for two weeks before deciding whether to keep the workflow.
- Pick a worktree directory convention like tilde-worktree-repo-branch and stick with it across all projects.
- Cap parallel coding agents at two simultaneously to preserve mental bandwidth and reviewing capacity effectively.
- Run a watcher agent in a loop that auto-merges feature branches resolving conflicts via Claude calls.
- Add pre-commit hooks requiring tests to pass on watcher-merged worktree branches for stability guarantees daily.
- Stage changes constantly without committing so you can diff against last known-good state cheaply throughout sessions.
- Generate four parallel design variations using different models when no single model gets design right.
- Adopt person/feature branch naming so teammates instantly recognize ownership when scanning the branch list together.
- Keep markdown research and planning documents outside the git working tree to avoid pointless merge conflicts.
- Use tmux capture-pane to let one Claude session programmatically observe another Claude's progress in real time.
- Run npm-install or equivalent setup automatically inside create-worktree so dependencies exist before agent invocation begins.
- Delete worktrees immediately after PR merge using a cleanup script that removes orphaned directories systematically.
- Few-shot your worktree naming convention by manually naming three then letting tools infer subsequent names automatically.
- Avoid creating worktrees for research or planning steps because non-code documents rarely have meaningful merge conflicts.
- Tell Claude Code to run git worktree commands for you rather than memorizing every possible flag combination.
- Standardize your agent workflow into research-plan-implement so convergence checkpoints look the same across spawned parallel agents.
- Build wrapper scripts encoding team opinions about worktree organization rather than expecting individuals to reinvent conventions.
- Treat worktrees as temporary workspaces tied to features, deleting them aggressively once their purpose has been served.
