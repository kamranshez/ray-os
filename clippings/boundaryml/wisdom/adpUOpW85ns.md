---
video_id: adpUOpW85ns
title: "Building a Practical AI Assembly Line"
url: https://www.youtube.com/watch?v=adpUOpW85ns
channel: BoundaryML
---

### SUMMARY
Dex from HumanLayer and Vibhav from BoundaryML demonstrate how Storybook accelerates agentic UI development by isolating pure components, enabling fast iteration loops without rebuilding apps.

### IDEAS
- Storybook acts like learning tests for UI, letting agents iterate visually without reloading entire app state.
- Front-end planning fails because markdown specs cannot reveal whether final rendered output will look acceptable.
- Pure components take props and render; wired components handle state, fetching, and business logic separately.
- Vibe coding back-and-forth with models works, but waiting until implementation reveals visual problems too late.
- Figma loses to Storybook because agents excel at writing React but struggle interacting with WYSIWYG editors.
- Every coding agent output type deserves its own Storybook story for fast renderer iteration cycles.
- User-reported bugs become Storybook stories instantly, capturing edge cases as permanent regression tests.
- Mono repos enable better agentic coding because state and shared components stay accessible across packages.
- Designers using AI to code start hating Figma because code-based design eliminates translation steps entirely.
- Iteration speed is undervalued; small loop improvements compound dramatically across long development sessions.
- Plan mode catches version mistakes like outdated Storybook 8 before agents commit hours of work.
- Snapshot testing breaks brittle and only works as well as the dataset of states you build.
- Custom React renderers per data type beat plain JSON output for visualizing complex agent traces beautifully.
- Pre-purifying components before plan-and-implement workflows lets you decide before building anything full.
- Web search loops in default Claude waste tokens; researcher subagents fetch latest docs more reliably.
- Component preview tools matter more than the specific Storybook implementation; vibe-code your own version.
- Architecture wins when wrapper components push hooks-derived props into pure renderers that never fetch data.
- Reviewing storybook stories during PR review replaces clicking through entire applications to verify components.
- Automation gives wins and losses simultaneously; faster systems break harder when interconnected pieces fail.
- New programming languages may be required before lights-off agentic software factories become genuinely viable.
- WASM components and web workers create lifetime state issues that pure UI rendering can sidestep nicely.
- Charting libraries get baked in Storybook first; once components work, they propagate everywhere effortlessly.
- The frame and stage controls let you preview components inside fake VS Code panes for realism.
- Empty arrays and array-of-objects need different visual treatments; Storybook reveals these gaps quickly.
- Designers can review pure components directly, eliminating the Figma-to-React translation friction completely.
- Models default to outdated library versions unless explicitly told to research the latest releases.
- Bootstrapping Storybook incrementally beats full migration; add hello world, then split components individually.
- Stateful components belong outside Storybook entirely; mixing API calls there defeats the isolation purpose.
- Custom render registries by type let users plug visual components into agent traces and prompt outputs.
- Front-end engineers shift from translating designs to wiring data layers into already-approved pure components.

### INSIGHTS
- Visual unit tests for components compress feedback loops the same way logic unit tests compress backend iteration.
- Separating pure rendering from data fetching is older than React itself but newly critical for agents.
- Code-based design systems beat WYSIWYG because models live in distribution for React but not Figma.
- The bottleneck in agentic UI work is reproducing application state, not generating component code itself.
- Plan mode's value lies in catching outdated assumptions before agents commit hours to wrong implementations.
- Bug triage transforms when every reported issue becomes a permanent state in your component library.
- Iteration speed compounds; tools shaving seconds per cycle outperform tools optimizing single execution paths.
- Mono repo migration is the prerequisite filter separating teams ready for agentic coding from those unready.
- The new SDLC pushes design earlier into production-ready code, eliminating handoff friction completely.
- Customizable type-based renderers turn raw agent output into actionable, debuggable visual artifacts naturally.
- Automation always trades stability for speed; the question is how much disruption your team accepts.
- Architecture patterns popularized in 2014 quietly became the foundation for modern AI-native development workflows.

### QUOTES
- "I can just come up with all these edge cases and just decide exactly how we want to render it." — Vibhav
- "As soon as a user comes up with an issue, you just paste it into Claude." — Dex
- "There is no podcast with worst SEO than AI that works." — Dex
- "You need a totally different paradigm of software development." — Vibhav
- "Lean is not a good programming language. It's unusable." — Dex
- "We will as a team review just the storybook stuff." — Dex
- "Figma is just a WYSIWYG editor that agents are not that good at interacting with." — Dex
- "It's not running React. It is full React." — Dex
- "Storybook won't help if your designer is Claude." — Dex
- "Our designer started using AI to code, and he hates Figma now." — Audience member
- "If you're not willing to migrate to a mono repo, then we are not going to work with you." — Dex
- "I think iteration speed is undervalued." — Vibhav
- "It is not about the tool we're using here." — Dex
- "I'm a clicky boy. I like clicks." — Vibhav
- "We only show code that we are proud of showing and tools that we like actually using." — Vibhav
- "We can have multiple different wrapper components for different APIs." — Dex
- "You generally don't want to have your stateful components that are making API calls in storybook." — Dex
- "The teams I'm seeing moving the fastest are getting folks to adopt AI." — Dex

### HABITS
- Pause between research and implementation to build Storybook stories as part of pre-building research.
- Always read the plan rather than vibing through plan mode to catch incorrect assumptions early.
- Pull down PR branches and review storybook stories visually as part of code review process.
- Create separate apps and packages folders in turbo monorepos to isolate building blocks cleanly.
- Run agent browser tools to capture PNGs and feed visual feedback into automated convergence loops.
- Rotate API keys immediately after accidentally exposing them on stream rather than worrying about cleanup.
- Use research subagents to verify latest library versions before letting agents commit to dependencies.
- Build learning tests during planning to surface unknowns before reaching implementation phases.
- Import shared components from packages directories rather than letting Claude duplicate inline implementations.
- Use Whisper Flow or Super Whisper for voice input while pair-coding with agents on screen.
- Test components by editing JSON props directly instead of running full applications repeatedly.
- Skip Figma entirely; jump straight from research to building pure React components in code.
- Maintain a registry mapping data types to custom render components for agent trace visualization.
- Reproduce user-reported bugs as Storybook stories before attempting to fix the underlying issue.
- Split terminal panes via View menu in Ghosty rather than trying to memorize keyboard shortcuts.

### FACTS
- Storybook has existed for over ten years, since approximately the beginning of React's adoption.
- The pure-versus-wired component pattern dates back to roughly 2014 in React community practices.
- Storybook supports accessibility plugins that audit contrast levels against WCAG compliance guidelines.
- Storybook collects anonymous analytics by default unless users explicitly opt out of telemetry.
- Turbo monorepos organize code into apps folders for runnable code and packages folders for libraries.
- Shadcn and Radix UI handle accessibility concerns automatically without requiring custom implementation work.
- COVID-era supply chains broke because automation ties downstream systems too tightly to upstream availability.
- Farmers pre-sell wheat and corn through futures markets to provide stability against demand variation.
- Apple pre-buys chip shipments months ahead rather than relying on last-minute supplier availability.
- Salsa is a Rust crate used for building compilers with caching for performance optimization.
- BAML works as a LangChain, Pydantic, or Vercel AI SDK replacement with structured output support.
- Storybook 10 was the latest version at recording time, while models defaulted to suggesting version 8.
- Promptfiddle.com hosts the BAML playground used for live prompt iteration during the demonstration.
- Riptide ships separate UI and Cloud apps using shared component libraries from the same packages directory.
- HumanLayer focuses on helping people build products with coding agents inside large complex codebases.

### REFERENCES
- Storybook (component development tool)
- Figma (design tool, contrasted unfavorably)
- Stitch (mentioned as alternative platform)
- Stately AI (mentioned as alternative platform)
- ChatGPT (mentioned as design tool by some)
- Whisper Flow / Super Whisper (voice input tools)
- Riptide (coding agent product by HumanLayer)
- BAML (BoundaryML's programming language for LLMs)
- Promptfiddle.com (BAML playground)
- Crispy / RPI (HumanLayer's planning workflows)
- Shadcn (component library)
- Radix UI (accessibility primitives)
- Tailwind / flexbox (styling primitives)
- Mermaid (diagram renderer)
- Storybook Snapshot Testing
- Playwright (browser automation)
- Agent Browser skill (from Vercel)
- Tan Stack / G Stack (referenced in passing)
- Salsa (Rust crate for compilers)
- Jeff Huntley (lights-off software factory)
- Garry Tan (joke about fundraising)
- Kyle (HumanLayer team member integrating charts)
- Ghosty (terminal emulator)
- tmux (terminal multiplexer)
- VS Code (frame customization in Storybook)
- WCAG (Web Content Accessibility Guidelines)
- Vercel AI SDK / LangChain / Pydantic (BAML alternatives)

### ONE-SENTENCE TAKEAWAY
Build pure components first in Storybook so agents iterate visually without ever rebuilding entire applications.

### RECOMMENDATIONS
- Adopt Storybook to give your coding agents a fast visual iteration loop on UI components.
- Split every component into pure rendering plus a wired wrapper that handles state and fetching.
- Bootstrap Storybook incrementally; start with hello world stories, then migrate components one by one.
- When users report bugs, recreate the bad state as a Storybook story before attempting fixes.
- Use plan mode to catch outdated library version assumptions before agents commit hours of work.
- Migrate to a mono repo before expecting serious agentic coding productivity gains in your team.
- Build a custom type-to-component registry so agent outputs render visually rather than as JSON.
- Skip Figma for new design work; vibe code pure React components and review them directly.
- Run the agent browser skill or Playwright to capture screenshots inside automated convergence iteration loops.
- Tell agents explicitly to research latest library versions, since defaults often pull outdated training data.
- Review Storybook stories during PR review instead of clicking through full application user flows.
- Keep stateful components with API calls completely out of Storybook to maintain isolation properties.
- Build learning tests during planning to surface unknown assumptions before implementation reveals problems.
- Vibe code your own component preview tool if Storybook feels too heavy for your specific needs.
- Customize Storybook's frame and stage to preview components inside realistic VS Code panes when relevant.
- Use research subagents for documentation lookups instead of letting agents waste tokens on web searches.
- Move design earlier in the SDLC by approving pure React components instead of Figma mockups.
- Verify imported shared components persist after agent runs rather than getting duplicated inline accidentally.
- Test array, empty, and edge-case states explicitly in Storybook stories to surface visual gaps quickly.
- Pause between research and implementation phases to build Storybook stories as research artifacts.
