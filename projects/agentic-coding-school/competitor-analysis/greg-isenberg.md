---
source: "Claude Code Clearly Explained (and how to use it)"
channel: Greg Isenberg
video_id: zxMjOqM7DFs
date: 2026-01-19
---

## Gaps Not Covered in Master Claude Code

- **[HIGH] "Ask User Question" tool for deep planning interviews** — Ross Mike demonstrates using the `ask_user_question` tool explicitly in prompts to force Claude into an exhaustive interview mode before building. The prompt pattern is: "Read this plan file. Interview me in detail using the ask user question tool about literally anything. Technical implementation, UI, UX concerns, and trade-offs." This creates rounds of increasingly granular questions about workflow, cost handling, database choices, UI aesthetics, avatar types, storage options, etc. Quote: "When you use this ask user question tool, the questions become more granular... the first plan had two sets of questions and it was ready to build. But with this, it's asking me, do I want basic avatars, custom avatars, multi-scene videos?" Ray covers "Interactive Questions" and "Clarifying Questions" but not this specific technique of explicitly invoking the ask_user_question tool for exhaustive multi-round planning interviews.

- **[HIGH] "Don't use Ralph if you haven't shipped anything yet" philosophy** — Ross argues strongly that beginners should NOT use Ralph loops until they've manually built and deployed at least one project. Quote: "If you haven't built anything, deployed anything, there isn't a URL that I myself or Greg can click on that you've built, you have no business using Ralph." The reasoning: building manually develops "vibe QA testing" intuition and product sense that automation bypasses. This is a strong pedagogical stance that Ray could adopt or counter.

- **[MEDIUM] Ross's custom Ralph loop with built-in test + lint verification** — Ross shows his own Ralph setup that goes beyond basic iteration: after each feature is built, it writes a test, runs the test, and lints. If the test fails, the loop goes back to fix that feature before proceeding. Quote: "Every feature it builds, it then writes a test and it then lints... there's no point on working on feature two if feature one doesn't work." Ray covers Ralph Loop but not this specific test-then-lint-per-feature variation.

- **[MEDIUM] 50% context usage rule of thumb** — Ross recommends starting a new session when context hits 50% (not waiting for 85-95% auto-compact). Quote: "The moment you see 50% or even 40% I would start a new session." This is more aggressive than most advice and is a specific actionable tip. Ray covers compacting vs clearing but not this specific threshold recommendation.

- **[MEDIUM] "Think in features, not products" planning framework** — Ross frames the core planning mistake as describing a product instead of decomposing it into individual features with tests per feature. Quote: "A lot of times people will describe a product, not describe features, and will be frustrated with AI." This is a specific mindset shift for planning that Ray could cover more explicitly.

- **[MEDIUM] Using a separate chatbot to answer Claude's technical questions during planning** — Ross demonstrates copying Claude's planning questions (e.g., "What database and hosting approach do you want to use?") and pasting them into ChatGPT to get answers when you don't know the technical details. This "chatbot relay" workflow is a practical beginner tip.

- **[LOW] Using Ghostty terminal** — Brief mention of terminal preference. Ross uses Ghostty rather than the Mac terminal, Warp, or iTerm. Minor but could be worth noting as an alternative.

- **[LOW] "Audacity" as a product-building principle** — The emphasis on taste, design thinking, and scroll-stopping software. Quote: "Software development is starting to become easy, but software engineering is very very hard... to create great UX UI, to have great taste." More philosophical than tactical but could inspire a video on taste-driven AI coding.
