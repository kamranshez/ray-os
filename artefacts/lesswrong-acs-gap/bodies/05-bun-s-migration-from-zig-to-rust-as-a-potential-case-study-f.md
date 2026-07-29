# Bun's Migration from Zig to Rust as a Potential Case Study for Gradual Disempowerment

- URL: https://www.lesswrong.com/posts/qEbqPitYhWHthwFNu/bun-s-migration-from-zig-to-rust-as-a-potential-case-study
- Author: Sayhan Yalvaçer
- Date: 2026-06-08
- Karma: 97  Comments: 8  Words: 847
- Band: A  Tier: 1  Score: 146.8  Density: 41.32
- Anchors: claude code, agentic (coding|engineering|software|development|programming), \bcodex\b

---

TL;DR:
======

Bun is a very large and very influential open-source project. It is being migrated from the easier-to-read Zig programming language to harder-to-read but memory-safe Rust. This is done almost entirely by the AI tool Claude Code. The migration may become one of the earliest major case studies of human control over a significant software project becoming increasingly indirect--both due to the nature of the programming language itself and LLM-generated code being quite convoluted.

What happened?
==============

On May 14 2026, a Rust version of Bun was merged to the "main" branch of the Bun repository[^lv102mdvkfc].

Bun was originally written in Zig, by humans. Then they started to use AI coding tools, likely with an increased intensity after their acquisition by Anthropic in December 2025[^wxd6dcxkzrg].

[Jared Sumner](https://jarredsumner.com/), Bun's creator, posted that the Zig version will be discontinued in favor of the Rust version.

![Screenshot 2026-05-18 at 16-49-43 (1) Jarred Sumner on X Bun v1.3.14 releases tomorrow. If we do merge the Rust rewrite this would be the last version in Zig _ X.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779112428/lexical_client_uploads/h61xpfhlojpbfb1cuahn.png)

Why is this a big deal?
=======================

As far as I'm aware, this is the first example of a hand-written large open-source software project entirely transitioning to LLM-written code.

![Screenshot of an X thread where Jarred Sumner says Bun’s code has largely been maintained via Claude Code for months.](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779111246/lexical_client_uploads/l7hworkeixc6mzahul7h.png)

According to what Jarred Sumner says on X, they haven't been typing code themselves, even before the acquisition--in other words, Claude was already Bun's *de facto* primary coder.

An explosion of complexity
--------------------------

> "An idiot admires complexity, a genius admires simplicity."
> 
> — Terry A. Davis

An initial bad sign about the viability of human maintenance is the increased codebase size. After the migration, the code size increased to over 1 million lines of Rust, compared to ~600,000 lines of the previous Zig code. This is especially surprising given that Rust is usually the more concise of the two: Zig is more verbose and will usually require more LoC than Rust for the same high-level task. This implies that this explosion of complexity is largely a result of Claude use.

To put things into scale, let's compare this with some other important OSS projects:

*   **JavaScriptCore:** ~810k lines (this is the JavaScript compiler Bun is wrapping!!)
*   **SQLite:** ~400k lines
*   **cURL / libcurl:** ~500k lines
*   **Redis:** ~270k lines
*   **nginx:** ~185k lines
*   **OpenSSH:** ~180k lines
*   **React:** ~625k lines
*   **Bash:** ~425k lines[^zdtelnzrlfa]

Why should you care?
====================

A great gamble
--------------

In the short term, this is a gamble for both Anthropic and the rest of the AI industry.

If the Bun team successfully continues to maintain the Rust code by using Claude Code, that would be strong evidence that current frontier AI models are advanced enough to handle at least some large-scale software migration and maintenance with little human oversight. Importantly, this would still be a narrower win than an AI system independently building a major greenfield software system *de novo* since the existing Bun codebase already supplies much of the architecture and desired behavior.

If the migration fails, it will be a fiasco for the AI industry, or at least for the strong near-term claims about agentic coding workflows.

Bun is in a uniquely favorable position for an attempt like this since they are owned by Anthropic: they don't have to care about Claude Code quotas or API cost, they might have access to [Claude Mythos Preview](https://www.lesswrong.com/posts/ssg9ZA4KmH4oJGYAN/claude-mythos-preview-analysis-of-anthropic-s-public) (which is not released publicly yet![^5g9vack9rk8]), and they have top-tier human developers. Despite all these favorable conditions, if the project still visibly fails, other companies might be more skeptical of aggressive agentic-AI workflows.[^k679y2k92qe]

If this project is going to fail, the easiest-to-spot early sign will be an explosion of complexity i.e. the codebase size increasing at an unreasonable and compounding rate. In this scenario, the size won't stay at 1 million lines of code[^xyx0lip5wej].

How gradual disempowerment comes into the picture
-------------------------------------------------

To put it concisely, [gradual disempowerment](https://www.lesswrong.com/posts/pZhEQieM9otKXhxmd/gradual-disempowerment-systemic-existential-risks-from) is a family of AI-catastrophe scenarios where we see a gradual and non-belligerent loss of power to AI systems, instead of a dramatic, confrontational takeover by a superintelligence[^60rbm98e3dt].

I think Bun's transition is a good toy model of gradual disempowerment.

In the good old days, Bun developers used to write the Zig code themselves. They had a line-by-line understanding of the code. Then they started to delegate coding to AI agents but they were still familiar with the language and the hidden assumptions behind it.

The Rust migration changed this. Claude agents generated the code entirely by themselves with minimal human supervision--which is indicated by the fact that the migration was done within a mere 6 days. Even the supervision work is done indirectly now: it's delegated to a symbiotic loop of tests/audits and AI.

Bun is upstream of many software projects[^l7z75qceg1p], which are in turn upstream of many other systems. So, I think it's reasonable to expect that the consequences of this decision won't remain isolated.

Appendix: Why did this happen?
==============================

*If you're convinced that this is indeed something you should care about, then I expect that you will benefit from reading this section.*

*If you aren't convinced, it's probably low ROI for you to read it as it doesn't contain any cruxes.*

* * *

There are several likely semi-overlapping reasons:

Memory Safety and Debugging Cost
--------------------------------

The main advantage of Rust over Zig (or C) is memory safety. Unlike those languages, Rust shifts the responsibility for memory cleanup from the coder to the compiler and thus automates this process.

This is also the stated reason for the Rust rewrite:

> why: I am so tired of worrying about & spending lots of time fixing memory leaks and crashes and stability issues. it would be so nice if the language provided more powerful tools for preventing these things.
> 
> — [Jarred Sumner on Twitter](https://x.com/jarredsumner/status/2053058171338682875) ([Archive](https://archive.is/5ou4w))

The Rust re-write has over 13,000 instances of unsafe calls[^574c7gasn8s]. This is an astronomical number, even for a large-scale project like Bun. For example, uv (which is *sort of*[^zqhmoh1uuz] the Python counterpart of Bun), has only 73 unsafe calls:

![Tweet by Theo (@theo) comparing Rust codebases: uv has 350k lines with 73 `unsafe` calls, while Bun’s Rust port has 681k lines with over 13,000, shown via side-by-side VS Code search results.](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1779378178/lexical_client_uploads/fsuf1e2y2n5zw9crz1ny.png)

This might seem like a bad thing at first. But it is actually an improvement over the Zig version: the unsafe blocks were already unsafe, but now they're at least annotated. This makes things much easier to fix: if you notice a memory leak and you know the function where the memory leak originates from, you can simply instruct Claude to fix it.

So, the Rust version has *de novo* beneficial feedback loops that can make it easier to have an AI debug the code.

"AI-native" Development Workflow
--------------------------------

Bun's developer team has been bullish on LLM usage for quite some time. This is a quote from their [acquisition post](https://web.archive.org/web/20251202182536/https://bun.com/blog/bun-joins-anthropic):

> Over the last several months, the GitHub username with the most merged PRs in Bun's repo is now a Claude Code bot. We have it set up in our internal Discord and we mostly use it to help fix bugs. It opens PRs with tests that fail in the earlier system-installed version of Bun before the fix and pass in the fixed debug build of Bun. It responds to review comments. It does the whole thing.

This arguably reduced the perceived cost of migrating from a language they were somewhat familiar with to another language since their heavy AI use had already distanced them from the code. Their devs weren't operating at the level of code to begin with.

This relates strongly to the next point.

Zig's Anti-LLM Policy
---------------------

Zig's policy barred developers from using AI for their PRs and this created operational and cultural mismatches between the Zig and Bun teams. For example, [~~the Bun team couldn't upstream their contributions to Zig~~](https://news.ycombinator.com/item?id=48017510) ~~because of this constraint.~~

*Edit, Jun 13: As* [*Viliam points out below*](https://www.lesswrong.com/posts/qEbqPitYhWHthwFNu/bun-s-migration-from-zig-to-rust-as-a-potential-case-study?commentId=aGXG6XzdL8zEdu9mE), the block was overdetermined: the Zig devs wouldn't want the changes even if the code weren't LLM-generated, although it's true that Zig has a no-LLM policy.

Anthropic's Influence
---------------------

This is the most speculative one (so take it with a larger grain of salt) but I think this migration is a tour de force for Anthropic: it is intended as a showcase for how powerful SOTA agentic coding tools are.

* * *

*Shout-out to* [*@JustisMills*](https://www.lesswrong.com/users/justismills?mention=user) *for detailed and extremely helpful feedback on the draft.*

[^lv102mdvkfc]: Bun PR #30412: https://github.com/oven-sh/bun/pull/30412 

[^wxd6dcxkzrg]: Bun is joining Anthropic | Bun Blog: https://web.archive.org/web/20251202182536/https://bun.com/blog/bun-joins-anthropic 

[^zdtelnzrlfa]: I had OpenAI's Codex calculate these using cloc. 

[^5g9vack9rk8]: Claude Mythos #2: Cybersecurity and Project Glasswing | The Zvi 

[^k679y2k92qe]: I don't want to put much weight on predicting broader public, VC, or executive reactions because those reactions are noisy and may depend more on other factors like salience or marketing. 

[^xyx0lip5wej]: I don't think that the failure of this project will bring about the end of the race towards AGI or will show that LLM-driven automatization of software development is not possible. Because, the only condition required for this failure mode is the inability of agentic-AI-based coding tools to keep up with the increase in code complexity. It could, however, burst the AI bubble if it causes a mass disillusionment event that cuts off the VC money. I'm not exactly sure that an AI bubble burst would straightforwardly reduce existential risk. E.g. it might knock out smaller competitors while benefiting leading labs like Anthropic, and any slowdown from reduced investment could be partly offset if compute becomes cheaper for the companies remaining in the race. 

[^60rbm98e3dt]: For a brief introduction to this concept, check @Jan_Kulveit's post Gradual Disempowerment, Shell Games and Flinches. 

[^l7z75qceg1p]: Including Claude Code itself, which ships as a Bun executable. 

[^574c7gasn8s]: An "unsafe block" in Rust basically tells the compiler to allow the operation even if it's not proven memory safe. An example: let slice = unsafe {    std::slice::from_raw_parts(ptr, len)}; 

[^zqhmoh1uuz]: This is a simplification. Bun actually does more than what uv does: uv is mainly a Python package manager. Bun has a JavaScript package manager and runtime.