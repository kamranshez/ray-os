---
title: Building a Practical AI Assembly Line
videoId: adpUOpW85ns
url: https://www.youtube.com/watch?v=adpUOpW85ns
date: 2026-07-01
status: posted
---

# Building a Practical AI Assembly Line

## The one idea worth a video

**Spine 1 - Give the coding agent an isolated render harness (Storybook) so it iterates on a single component's props instead of booting the whole app: visual unit testing.** The bottleneck in agentic UI work is feedback latency, not code generation, and isolating the component collapses the loop.
VERDICT: 🔗 next-step video available (complements "closing-the-loop").

**Spine 2 - Split every component into a pure display half (props to render) and a wired half (state, hooks, fetching) so the agent has a deterministic, side-effect-free surface to work on.** This is the architecture prerequisite that makes Spine 1 possible, and it generalizes to functional-core / imperative-shell for any agent-worked code.
VERDICT: ❌ net-new video available.

## Summary

Dex and Vibhav of AI That Works show how Storybook renders isolated pure components as visual unit tests, giving agents a fast UI iteration loop.

🔴 1 net-new · 🔗 1 complement · 🟡 0 partial · ✅ 0 covered

## 🔬 Deep dive

### Spine 1 - The isolated render harness as a visual unit test

The claim: when a coding agent works on UI, the bottleneck is the feedback loop, not code generation, so build an isolated render harness and let the agent iterate on one component's props rather than the whole app. Non-obvious because the default move is to vibe-code against the running app: boot the server, click through to the broken state, screenshot, repeat. People treat UI as inherently un-unit-testable. Why it is true: a pure component is just props to render, so you can reproduce any state by handing it a JSON of props; because you skip the server, data, and navigation, loop time drops from minutes to seconds; therefore you can sweep twenty states in the time one full-app reproduction used to take. Dex frames it exactly: "it's unit testing for visual stuff." It generalizes to Vibhav's BAML playground, where today you must run the full LLM call to see how each output renders; isolate the render and the same loop collapses, and a screenshot-to-PNG CLI hook lets the agent converge autonomously. How it goes wrong: interactive components do not truly work in isolation (buttons render but do nothing), snapshot testing is only as good as its dataset, and Claude tends to duplicate rather than import the component.

### Spine 2 - Pure versus wired: architecting code so agents can work

The claim: separate each component into a pure display half (props to render, no side effects) and a wired half (hooks, state, API fetching) that pushes props down into the pure half. Non-obvious because most components mix display and business logic, and people conclude "all my components have state," so isolation feels impossible. Why it is true: because the pure half has no side effects, it is deterministic on its inputs; because it is deterministic, both a test harness and an agent can drive it with arbitrary props and trust the result; therefore the wired half becomes a thin, swappable shell (cloud and local can fetch from different APIs behind the same pure core). This is functional-core / imperative-shell applied to make code legible to agents. It generalizes well beyond frontend: any code that isolates side effects (I/O, network, DB) behind a pure core hands agents a deterministic surface, the same reason backend logic is easier to test than a wired endpoint. Store the pure components in a shared packages/ui folder imported identically across apps. How it goes wrong: the pattern is "not super baked in the training set," so you must prompt it explicitly; Claude often writes the component into both Storybook and the app instead of importing one source; naive wrappers can trigger re-render performance issues.

## 🎬 Proposed ACS videos

### 1. Unit Test Your UI: The Fastest Feedback Loop for Coding Agents

- HOOK: Your agent is not slow at writing UI code; it is slow because it reboots the whole app just to see one screen.
- THE PROMISE: For anyone building UI with Claude Code, set up an isolated render harness so the agent fixes a component in seconds, not minutes.
- THE SHAPE:
  1. The pain: booting the app and clicking through to reproduce one visual state.
  2. Bootstrap Storybook and add a couple of hello-world stories.
  3. Render a pure component and edit its props to sweep every state.
  4. Reproduce a real reported bug as a story and fix it in isolation.
  5. Add a screenshot-to-PNG CLI hook so the agent loops autonomously until it converges.
- SPINE: Spine 1.
- SLOT: Techniques class (sits beside closing-the-loop) or the Claude Code workflow chapter.
- RELATIONSHIP: 🔗 complements "closing-the-loop". That video teaches giving the agent a verifiable feedback signal to iterate against; this adds the concrete harness for the hardest case, visual UI you cannot easily assert on, by rendering pure components in isolation with hand-fed props.
- PROOF TO REUSE: Dex's "it's unit testing for visual stuff"; the BAML playground pain (must run the full LLM call to see how an output renders); "iteration speed is undervalued"; the paste-the-bad-state-and-have-Claude-add-a-story bug workflow; testing an "array of HTTP requests" state you cannot even produce in the app yet.

### 2. Pure vs Wired: Architecting Your Codebase So Agents Can Actually Work

- HOOK: "All my components have state" is exactly why your agent keeps breaking your UI.
- THE PROMISE: For engineers in real codebases, learn to split display from side effects so both agents and tests get a deterministic surface to iterate on.
- THE SHAPE:
  1. Why mixed display-plus-logic components block agents and tests alike.
  2. The pure versus wired split: props to render vs hooks, state, and fetching.
  3. Refactor one stateful component into pure plus wired, live.
  4. Move pure components into a shared packages/ui folder imported across apps.
  5. Prompt Claude explicitly so it does not duplicate or re-mix the concerns.
- SPINE: Spine 2.
- SLOT: Context Engineering class (codebase architecture for agents), or Techniques adjacent to the backlog brief "designing-interfaces".
- RELATIONSHIP: ❌ net-new. No ACS video teaches structuring code as a pure core plus wired shell so agents work on a side-effect-free surface; the closest, "designing-interfaces," is still backlog and broader in scope.
- PROOF TO REUSE: "It's not super baked in the training set, but if you prompt it properly you can get there"; the cloud-versus-local wrapper example (same pure component, different APIs); Claude's duplicate-instead-of-import failure mode; the monorepo packages/ui pattern where the exact same button component is imported in both Riptide and Cloud.

## 📚 Full wisdom (reference)

**SUMMARY** - Dex and Vibhav of AI That Works show how Storybook renders isolated pure components as visual unit tests, giving agents a fast UI iteration loop.

**IDEAS**
- Storybook renders individual UI components in isolation so you iterate without booting the entire application state.
- Treat component stories as visual unit tests: reproduce a bad state with props, then fix it.
- Split components into pure display logic and wired wrappers holding all state, hooks, and API fetching.
- Pure components only take props and render; wired wrappers push those props down from business logic.
- Agents write React code well but interact poorly with Figma's WYSIWYG editor, so design in code.
- Mockups become the actual React components, eliminating the Figma-to-code translation step and the designer sign-off loop.
- Build Storybook stories during research to resolve how-will-it-look unknowns before implementation instead of discovering them afterward.
- This mirrors proof-based development: write learning tests early so wrong assumptions surface in planning, not implementation.
- Add a CLI screenshot-to-PNG hook so an agent loops autonomously, converging until the component looks right.
- Vibhav's BAML playground currently must run the full LLM call to inspect how each output renders.
- A coding agent emits countless output shapes; render each raw data type as an isolated story.
- Migrate incrementally: bootstrap Storybook, add hello-world stories, then purify and add one real component each pass.
- Claude often duplicates a component into Storybook and the app instead of importing one shared source.
- Pure-versus-wired is weak in the model's training, so you must prompt the concept explicitly to succeed.
- Store pure components in a shared packages/ui folder, imported identically across every app in the monorepo.
- Test states you cannot even produce in the app yet, like an array of HTTP requests.
- Storybook audits color-contrast levels against accessibility guidelines, replacing inspection tasks people assume only Figma can handle.
- Plan mode caught the model installing Storybook 8 when Storybook 10 was actually the latest release.

**INSIGHTS**
- The bottleneck in agentic UI work is feedback latency; isolate the component and the loop collapses.
- Visual correctness resists assertions, so a fast human-in-the-loop render harness beats trying to automate the judgment.
- Architecture makes agents effective: isolating side effects hands them a deterministic surface they can safely iterate.
- Meet the model where it is strong: React code sits in-distribution, WYSIWYG design tools do not.
- Proof-based development is really about moving unknowns earlier, whether the unknown concerns logic or visual appearance.
- Removing a translation handoff, not adding a tool, is where the real workflow speedup comes from.
- Automation trades speed for fragility; add only as much QA automation as your recovery tolerance allows.
- You do not need the tool; you need to see one component under many prop combinations.
- Reviewable code artifacts democratize design contribution: more people can shape visuals when mockups are just components.

**QUOTES**
- "It's kind of like how you would do unit testing, right? But it's unit testing for visual stuff." - Dex
- "Now I can see how your iteration loop is much faster both for you and the agent because you don't have to run the whole app." - Vibhav
- "The mockups are just the React components... there is no translate the Figma into React. It's just already there implemented with your design system in code." - Dex
- "Our designer started using AI to code, and he hates Figma now." - Dex
- "If you're not willing to migrate to a mono repo, then we are not going to work with you." - Dex
- "You don't have to go spin up the whole web app and click around and create the state that reproduces the bug." - Dex
- "I think iteration speed is undervalued." - Dex
- "It's not hard to build a component that renders other components with random props. You could probably vibe code a version of Storybook." - Dex
- "It's not super baked in the training set, but if you prompt it properly, you can get there." - Dex
- "You may not even be able to produce that state in the app today, but you can test it this way." - Dex

**HABITS**
- They review only the Storybook components as a team during pull-request review instead of the app.
- When a user reports a bug, they paste the bad state and Claude adds a story.
- Dex always reads the plan before executing, refusing to blindly vibe changes he has opinions about.
- They prototype any new charting library inside Storybook first, then use it everywhere once it's baked.
- They run plan mode specifically to catch stale dependency versions the model otherwise installs by default.
- They scope migrations narrowly, converting one known-pure component rather than asking the agent to migrate everything.
- They only demo tools and code they are proud of, refusing sponsorships to keep content unbiased.
- They immediately rotate an API key the moment it leaks on stream instead of deleting footage.

**FACTS**
- Storybook has existed for over ten years, roughly since React's earliest days circa the year 2014.
- Storybook 10 is the latest major version; the model defaulted to installing the older Storybook 8.
- React's props-versus-state distinction and the pure-versus-wired split trace back to established component patterns from around 2014.
- During COVID, automated supply chains amplified shocks: delayed chips made cars far more expensive for buyers.
- Farmers pre-sell wheat and corn on futures markets because participants value long-term stability in automated systems.
- Storybook is open source but collects anonymous analytics by default unless you explicitly turn that off.
- Shadcn and Radix UI handle accessibility concerns like WCAG automatically, so you need not implement manually.
- WCAG stands for Web Content Accessibility Guidelines, the standard Storybook can audit contrast levels against automatically.

**REFERENCES** - Storybook (v8, v10); React; BAML / BoundaryML; HumanLayer; Riptide (Riptide UI, Riptide Cloud); Crispy and RPI (research-plan-implement) workflows; structure outline skill; promptfiddle.com; Figma, Figma Make, Google Stitch, Stately AI, Canva; ChatGPT; Shadcn; Radix UI; Whisper Flow / SuperWhisper; Vercel agent-browser skill; G stack (gstack); Playwright; computer use; Turbo monorepo; WASM / web workers; Salsa (Rust crate); Lean; cursed lang and Jeff Huntley's "lights off software factory"; Garry Tan; Ghostty terminal; tmux; Pydantic; LangChain; Vercel AI SDK; Protobuf; learning tests / proof-based development; snapshot testing; WCAG.

**ONE-SENTENCE TAKEAWAY** - Isolate UI into pure components so agents iterate on props, not the whole running app.

**RECOMMENDATIONS**
- Adopt Storybook to render pure components in isolation and give your coding agent a fast loop.
- Refactor mixed components into a pure display half and a wired half holding state and fetching.
- Explicitly prompt Claude with the pure-versus-wired concept, since it is not well-baked into its training data.
- Build component stories during planning so you resolve visual unknowns before committing to a full implementation.
- Reproduce reported UI bugs as a Storybook story with props, then iterate the fix in isolation.
- Add a screenshot-to-PNG CLI hook so the agent autonomously loops until the component converges on correct.
- Store shared pure components in a packages/ui folder so every app imports the identical building blocks.
- Verify the agent imports your shared component rather than duplicating markup that never affects the app.
- Run plan mode to force the model onto the latest library versions instead of stale defaults.
