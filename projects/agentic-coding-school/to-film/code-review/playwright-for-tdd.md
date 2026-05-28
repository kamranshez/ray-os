Pairs with [[Red-Green-Refactor]]. RGR tells you to write the failing test first — Playwright is the answer to *what kind of test*. End-to-end, behavioural, against the real running system.

From Marlene's talk (Microsoft/GitHub Core AI): the whole reason DHH's 2014 critique still lands in 2026 is that AI tools make the original failure mode worse. Agents love writing self-affirming unit tests — coverage is green, behaviour is untested, nothing actually works. Playwright sidesteps that by testing the system, not the implementation.

## Why Playwright fits the agentic loop

- **Behavioural by default.** The test drives a real browser, clicks real buttons, reads real pixels. Renaming an internal method doesn't break it.
- **Survives refactors.** Tests are pinned to the contract (the UI, the URL, the visible behaviour), not to the function names underneath.
- **AI can't fake it.** A passing Playwright test means the feature actually works end-to-end. There's no "looks right" loophole.
- **Screenshots for free.** Every run produces visual evidence. Drop it in the PR.

## The flow with an agent

1. **Red** — agent writes a failing Playwright test from the feature description. No app code yet.
2. **Green** — agent writes the minimum implementation to make the test pass. Speed over elegance.
3. **Refactor** — *this is where the human spends most of their time.* The agent's first-pass code usually needs cleanup. The tests stay green throughout.

Marlene's framing: with AI, Red and Green collapse to minutes. Refactor becomes the biggest block of human time — which is the inverse of how TDD used to feel.

## Wiring it up

Three options, in roughly increasing power:

- **Playwright MCP server** — drop-in for any coding agent (Claude Code, Copilot CLI). The agent gets browser-control tools natively.
- **Playwright CLI** — agent shells out, runs tests, parses results. Fine for simple cases.
- **Playwright agents** — `npx playwright init-agents` installs three `.md` files into your agents directory:
	- **Planner** — decides which tests to write for a feature
	- **Generator** — writes the actual test code
	- **Healer** — fixes broken tests after legitimate code changes

The healer is the interesting one. It's the agent that knows the difference between "the test is wrong now" and "the code is broken now."

## Practical rules

- **One test per feature.** Don't bundle. When something breaks you want to know exactly what.
- **Commit before letting the agent fix anything.** Agents lose context across sessions; the commit is your rollback point.
- **Headless mode in CI, headed mode when debugging.** Watching the browser do the thing is the best sanity check there is.
- **Attach screenshots to PRs.** Reviewers see the actual user-facing outcome without running the suite themselves.
- **Trigger the test from a feature request, not from a new method.** This is the mental shift — tests describe behaviour the user cares about, not internal structure.

## Where it doesn't fit

- **Pure backend / no UI** — test the API directly. Playwright has `request` for this, but plain HTTP assertions are often simpler.
- **Native mobile / desktop** — Playwright is browser-only today. For Mac/iOS apps you need something else (XCUITest, Appium).
- **Heavy state machines** — Playwright agents have specialised instructions for this; vanilla Playwright struggles. Use the `init-agents` flow.

## How this sits next to the reviewers

Day 7 is mostly about post-hoc trust (reviewers, adversarial agents, Codex second opinions). Playwright TDD is the *upstream* version of the same goal. Reviewers cover taste, architecture, subtle correctness. Playwright covers "does the feature actually work when a user clicks the button." Both layers, not either/or.

## Sources

- Marlene (Microsoft/GitHub Core AI) — conference talk on Playwright + agentic TDD
- Playwright docs: https://playwright.dev
- `npx playwright init-agents` — installs planner/generator/healer
