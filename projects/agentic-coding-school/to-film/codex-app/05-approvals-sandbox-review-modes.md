---
duration: "6-8 min"
order: 5
class: "codex-app"
chapter: "Codex App"
status: "to-film"
tags: [course, script, codex, codex-app, review-modes, approvals, sandboxing]
lesson: "Approvals, Sandbox & Review Modes"
---

Every time you run Codex, you are turning a dial. On one end, Codex is a careful assistant that asks before it touches anything. On the other end, Codex is a coworker that just goes, edits files, runs commands, and hands you a diff at the end.

This video is about that dial. The official name for it is approvals, sandbox, and review modes. The mental model is simpler. **How much trust am I giving Codex before it produces a diff?**

[IMAGE: a dial with three positions labeled read-only, auto, full-access, with a hand turning it]

![[images/05-approvals-sandbox-review-modes/the-trust-dial.png]]

---

## The Three Areas

There are three settings, not one. They are related, but they answer different questions.

| Area | What it controls | Question it answers |
| ---- | ---------------- | ------------------- |
| Review modes | The workflow style. How Codex proposes, runs, and waits. | How do I want to work with Codex? |
| Approvals | The moments where Codex must stop and ask you. | When does Codex pause? |
| Sandbox | The boundary around files, commands, and network. | What is Codex physically allowed to touch? |

If approvals are the doorbell, the sandbox is the door itself. Approvals decide when Codex rings before walking in. The sandbox decides which rooms exist at all.

---

## The Sandbox Modes

These are the exact names from the codex repo. Learn them, because the labels in the app map directly to these.

**read-only.** Codex can read files and answer questions. It cannot edit, run commands, or hit the network. This is the safest setting. Use it when you are exploring an unfamiliar repo or asking Codex to plan before it touches anything.

**workspace-write.** This is the default. Codex can read files, edit files, and run commands inside your current workspace. Network access is off unless you explicitly turn it on. Anything outside the workspace requires approval.

**danger-full-access.** Also known as `--yolo`. No sandbox, no approvals. Codex can do whatever it wants on your machine. The name is a warning. Do not run untrusted code or unfamiliar agents in this mode.

[IMAGE: three concentric circles labeled read-only, workspace-write, danger-full-access, with a tiny lock icon shrinking from outer to inner]

![[images/05-approvals-sandbox-review-modes/sandbox-rings.png]]

---

## The Approval Policies

These are independent of the sandbox. They decide when Codex stops to ask.

**untrusted.** Codex runs safe reads on its own, but asks before any command that mutates state or executes externally. The most cautious setting.

**on-request.** Codex works inside the sandbox without bothering you, but pauses when it wants to escalate. Editing outside the workspace, hitting the network, running a destructive command. This is the default for version-controlled folders.

**on-failure.** Codex runs autonomously and only asks when something fails or gets blocked. Good for long agent runs you do not want to babysit.

**never.** No prompts at all. Codex operates entirely within the sandbox boundary you set, no matter what.

The app combines these into presets. The **Auto** preset is `workspace-write` plus `on-request`. That is the setting you will spend most of your time in.

---

## Behind The Scenes: How The Sandbox Is Actually Enforced

The sandbox is not a vibe. It is the operating system saying no.

**On macOS, Codex uses `sandbox-exec`.** This is Apple's built-in sandboxing tool, the same primitive that locks down apps from the App Store. Codex generates a Scheme profile that whitelists reads from your workspace, blocks writes outside it, and denies network sockets. When Codex spawns a shell command, that command runs inside the profile. If it tries to `rm -rf ~/`, the kernel refuses.

**On Linux, Codex uses bubblewrap with seccomp.** Inside `codex-rs/linux-sandbox`, you'll find the actual implementation. Bubblewrap creates a new mount and network namespace for the command. Codex calls it with `--unshare-net`, which means the command runs with no network at all. On top of that, Codex applies `PR_SET_NO_NEW_PRIVS` and a seccomp filter that blocks raw socket creation. Landlock is still in the codebase as a legacy fallback path, but the modern default is bubblewrap.

**Network egress is blocked at the namespace level.** When workspace-write is on without network, Codex isn't politely declining HTTP calls. The network namespace literally has no route to the outside world. `curl` fails because there is no internet from inside the sandbox. If you flip on the network toggle, Codex either drops the `--unshare-net` flag or routes traffic through a managed proxy bridge that only reaches configured endpoints.

This is why the trust dial is real. **read-only** isn't a polite request. It is a kernel-level box.

[IMAGE: split diagram, left side macOS with sandbox-exec wrapping a shell command, right side Linux with bubblewrap + seccomp wrapping a shell command, both with a red X over a network arrow]

![[images/05-approvals-sandbox-review-modes/enforcement-os-level.png]]

---

## When To Tighten The Dial

Default to stricter settings when:

- You're in an unfamiliar repo and you don't know what scripts exist.
- The task could touch many files at once.
- A command in the chain might delete, migrate, deploy, or publish something.
- The work involves credentials, secrets, or external systems.
- You haven't reviewed the agent's plan yet.

Stricter settings cost you speed. They buy you the ability to catch a bad plan before it runs.

---

## When To Loosen The Dial

Reach for `on-failure` or `never` when:

- You're working in a worktree, so the blast radius is contained.
- The task is well-scoped and you've seen Codex do this kind of thing before.
- You want Codex to run tests in a loop without asking you every iteration.
- You're heading to lunch and you want a long agent run to keep moving.

A worktree plus `workspace-write` plus `on-failure` is a great setup for trusted, repetitive work. Codex can edit, run tests, fix, and try again without ever interrupting you.

[IMAGE: a slider with low-trust on the left, high-trust on the right, with example tasks labeled at each end]

![[images/05-approvals-sandbox-review-modes/when-to-tighten-loosen.png]]

---

## The Pitfall

`danger-full-access` exists because sometimes you genuinely need it. A migration script that has to touch system paths. An install step that hits the network. A repo that lives outside your workspace.

It is named "danger" on purpose. The moment you flip it on, you have removed every guardrail. A typo in a prompt, a bad tool call, an injected instruction in some file Codex reads, and there is nothing between the model and your filesystem.

The rule of thumb. **Never run an agent in danger-full-access on a machine that has anything you care about.** If you must, do it in a VM, a fresh devbox, or a container you can throw away. The sandbox exists for a reason. The reason is that models do unexpected things, and the kernel is the only thing that can say no with certainty.

---

## Demo

Open the Codex app on a real repo and walk through this:

1. Start a new thread in **read-only** mode. Ask Codex to plan a feature. Watch it read files, draw a plan, and stop. Try to make it run a shell command. Watch it refuse.
2. Switch to **workspace-write** with **on-request** approval. Ask Codex to add a small function and run the tests. Notice it edits and runs tests on its own. Now ask it to `curl` something. Watch it pause and ask for approval to escalate.
3. Open the settings panel and find the approval policy dropdown. Show the four options: `untrusted`, `on-request`, `on-failure`, `never`. Show the sandbox dropdown with `read-only`, `workspace-write`, `danger-full-access`.
4. Open a terminal in the worktree and run `codex sandbox macos -- curl https://example.com` (or `codex sandbox linux` on Linux). Show the command failing because the sandbox blocked the network call. This is the exact box your agent runs in.
5. Flip the workspace-write network toggle on. Re-run the same curl. Watch it succeed. Show the viewer that this is one switch, not a vague setting.

[IMAGE: screenshot mockup of the Codex app settings panel showing sandbox and approval dropdowns side by side]

![[images/05-approvals-sandbox-review-modes/settings-panel.png]]

---

## Key Insight

> The trust dial isn't a preference. It's a kernel-level box. read-only means the operating system will refuse, not that Codex will politely decline.

---

## Up Next

You've decided how much freedom Codex has before it produces a diff. The next video is what happens after the diff exists, how you review it, comment on it, and accept or send it back.

That's [[04-reviewing-changes-pr-review]].
