---
video_id: YcT7gjzj2TU
title: "The No-Rework Workflow for AI Coding Assistants"
url: https://www.youtube.com/watch?v=YcT7gjzj2TU
channel: BoundaryML
---

### SUMMARY
Bipal and Dexter livestream building a message-queueing feature in Riptide, demonstrating their no-vibes design-first workflow with Claude Code SDK.

### IDEAS
- Baking assumptions into design upfront raises probability that downstream implementation will be technically correct.
- Less context used signals smart zone; higher percentages mean less efficient question answering, not done.
- Harder problems demand optimizing work into the smart part of context window deliberately.
- Learning tests prove how opaque SDKs actually behave before writing implementation code against them.
- Pattern recognition lets models replicate existing learning-test harnesses without inventing new approaches each time.
- Research from code, web, and proofs are three flavors of building pre-implementation knowledge.
- Great leaders being right a lot means moving faster because they avoid backtracking through mistakes.
- Architectural mistakes detected days later compound into more mistakes built atop the original.
- Decisions take little time but have huge impact; execution wastes time without good decisions.
- Codebases regress toward the mode of patterns, amplifying both your best and worst examples.
- Bad generations reinforce themselves; the model learns recent patterns are acceptable next time.
- Plan files and research docs should be throwaway artifacts, never checked into the repo permanently.
- Code becomes the source of truth the moment a feature ships into production.
- Reading the design doc meticulously catches missing requirements before implementation amplifies them everywhere.
- Junior engineers will mess up your design doc because of unwritten baked-in senior assumptions.
- Keep frontends dumb so backends own state and business logic in one consolidated place.
- Dumb frontends make backends usable by even the dumbest agents without protocol mistakes.
- Building all options in parallel costs evaluation time; build one feature plus another instead.
- Storybook lets you carve off UI decisions early without waiting for end-to-end implementation.
- Vertical planning slices through database, API, and frontend per phase rather than horizontally per layer.
- Models default to horizontal planning because layered thinking feels natural but delays testability significantly.
- Iterating on what is inconsistent or missing produces dramatically more complete structure outlines through repetition.
- Auto-advance through research and design phases because manual loops on research are pointless.
- Forking learning tests early lets you compare approaches cheaply before committing to thousand-line PRs.
- Prune your team's skill collection to a small minimum that everyone actively uses and improves.
- Treat skills like products; kill features only ten percent of your team uses.
- The compounding return on tooling comes from everyone iterating on the same shared things.
- Bad GPs in research systems poison decisions; one wrong inference cascades through the whole plan.
- The dumber your UI, the easier eventual agent-friendly backend migration becomes for everyone downstream.
- Boolean flags beat enums when the underlying intent is preference, not strict mode selection.
- Race conditions resolve cleanly when backend reinterprets stale frontend preferences as their actual current meaning.
- Pre-implementation surgery on a model's understanding is cheaper than mid-implementation course correction.
- Design discussions force humans into the high-stakes architecture decisions agents cannot reliably make alone.
- The sweet spot of plan time balances backtrack probability against diminishing returns from over-specification.
- Sending design docs to senior reviewers before implementation prevents wasted polishing on rejected approaches.

### INSIGHTS
- Move every decision as early as possible because backtracking compounds expensively across every later phase.
- The design doc's purpose is preventing mistakes, not preserving knowledge for future readers later.
- Dumb clients with smart servers create the cleanest path toward agent-driven backend interfaces eventually.
- Plans converge to your codebase's mode, so explicit pattern guidance matters more than generic prompts.
- Verifying critical design decisions in docs is faster than verifying them inside generated implementation code.
- Vertical slicing surfaces architectural surprises early when single layers cannot yet be tested independently.
- Skill sprawl destroys compounding returns; focused tooling adoption beats broad tooling distribution every time.
- Models replicate patterns rather than innovate, so investing in clean reference patterns pays back enormously.
- Cheap iteration on design beats expensive iteration on implementation because tokens cost less than context.
- Code rabbit and other CI tools compensate for the impossibility of reviewing every generated line yourself.
- Read the plan, not the code, because the plan is shorter and decisions live there.
- Confidence in oneshot implementation comes from rigorous research and design, not from clever prompting alone.

### QUOTES
- "The more assumptions that you can bake in ahead of time, the more correct your design is." - Bipal
- "Once you start hitting like 40 50 70 80 90 percent, you're just being less efficient." - Dexter
- "Great leaders are right a lot." - Bipal
- "When you're right, you move so much faster than any other competition." - Bipal
- "Decisions take not a lot of time and have a lot of impact." - Dexter
- "Your codebase will always regress to the average of the best pattern and the worst pattern." - Bipal
- "Plan files are throwaway. Research files are throwaway. They're task specific." - Dexter
- "If you want to know the truth read the code." - Bipal
- "You want to do brain surgery on the model and update the patterns it's going to follow." - Dexter
- "Keep your front end dumb. Keep your front end as dumb as possible." - Bipal
- "You want to optimize for finding surprises and finding incorrect things as early as possible." - Dexter
- "The dumber your UI the easier it is for you to consolidate state and business logic." - Bipal
- "Cut scope, iterate, focus on a small number of skills." - Bipal
- "Bring people in earlier into the fold. That's the magic." - Bipal
- "Focus on your product, not on your engineering workflow." - Bipal
- "You basically want to make decisions with the least amount of information possible." - Dexter
- "Design docs are purely an execution concept." - Dexter
- "Spend more and more time earlier on the fold making good decisions." - Bipal

### HABITS
- Run learning tests against opaque SDKs before assuming documented behaviors match actual runtime behavior.
- Iterate on structured outlines repeatedly with what is inconsistent or missing prompts every time.
- Delete research and design docs after merging because the code becomes the source of truth.
- Send complex design discussions to your senior reviewer before committing to implementation work.
- Send simple ones through autonomously without bothering anyone, trusting your own judgment for low stakes.
- Use auto-advance through every design discussion phase rather than manually loop through research repeatedly.
- Read every design doc meticulously despite it slowing you down during the planning phase.
- Slice features vertically by phase rather than horizontally by architectural layer when planning.
- Test the database after the API endpoint exists, before wiring complete frontend behavior.
- Use Storybook for UI decisions that AI cannot reliably back-pressure with good design taste.
- Spawn parallel sessions running rip grep across node modules to extract minified types and interfaces.
- Prefer building one new feature over building seven variants of the same architectural option.
- Trust developers to recognize when complexity warrants pulling additional reviewers into the design fold.
- Verify critical decisions made it into design docs by reading them rather than implementations later.
- Prune team skill collections aggressively, keeping only the small set everyone actively uses well.

### FACTS
- Cloud Code SDK ships partially open source with closed-source binary, requiring node modules type exploration.
- Riptide is the working title for Human Layer's IDE harness sitting on top of Cloud Code.
- Riverside is not open source but offers a waitlist for early access to interested users.
- BAML is a programming language built specifically for constructing AI pipelines and prompt orchestration.
- Amazon's leadership principles include the often-memed but useful tenet that great leaders are right.
- Google engineers wrote design docs constantly but rarely referenced them after implementation shipped successfully.
- The protobuf migration discussed touched seventeen thousand added lines and thirteen thousand removed lines.
- The protobuf refactor was completed across roughly eighteen commits over a two-week period.
- Cloud Code's binary contains minified code where types remain explorable through node modules type definitions.
- Conversation events tables can power streaming displays merging user input with backend SDK event data.
- BAML's type system migration created entirely new top-level packages rather than evolving existing types.
- Code Rabbit functions as the team's CI validation tool catching bugs before merging completes.
- Cloud Agent SDK supports streaming input modes that accept queued messages during active session execution.

### REFERENCES
- BAML programming language for building AI pipelines
- Human Layer for context engineering tooling
- Riptide / Code Layer IDE for Cloud Code workflows
- Cloud Code CLI and Cloud Agent SDK from Anthropic
- Code Rabbit CI review tool
- Storybook for component-level UI development
- Amazon Leadership Principles
- Linear for issue and ticket tracking
- Google internal design doc culture
- Previous AI That Works episode on interruptible agents
- Ralph Wiggum iteration meme used to describe loop prompting
- Ripgrep used for SDK source exploration

### ONE-SENTENCE TAKEAWAY
Front-load decisions into research and design so implementation oneshots, eliminating costly mid-execution rework and backtracking.

### RECOMMENDATIONS
- Build learning tests for any opaque dependency before designing features that rely on its behavior.
- Read every design doc meticulously and update assumptions before letting agents start writing implementation code.
- Slice work vertically through database, API, and frontend per phase rather than horizontally per layer.
- Prune your team skill catalog to fewer than ten well-adopted skills with active maintenance.
- Treat all research and plan files as throwaway artifacts deleted after merge.
- Send complex design discussions to a senior reviewer before any implementation tokens get spent.
- Use autoadvance through research phases since manual loops on early-stage research provide no value.
- Iterate structure outlines using what is inconsistent or missing prompts until output stabilizes completely.
- Keep frontends dumb so backends own state, simplifying eventual agent-driven API consumers later.
- Prefer boolean flags over enums when the underlying field expresses preference rather than strict mode.
- Default to single endpoint receiving intent rather than multiple endpoints split by current state.
- Spend more time on design discussions than plans, more on plans than code.
- Stop trying to build all architectural options in parallel; pick one and ship something else parallel.
- Use Storybook to carve off UI decisions agents cannot back-pressure well with taste alone.
- Verify the design doc captured your critical preferences explicitly before letting implementation begin.
- Recognize when complexity warrants pulling another reviewer into the fold rather than deciding solo.
- Prompt for V2 patterns explicitly during research, then verify research output reflects that preference.
- Unify continue, queue, and interrupt endpoints into one message endpoint with intent boolean parameter.
- Reduce probability of backtracking by spending five extra minutes ensuring the design is correct.
- Treat your engineering workflow tooling as products with usage metrics driving feature pruning decisions.
