# AI agents publishing and reviewing scientific papers

- URL: https://www.lesswrong.com/posts/zFQ3iBH9AoLLNoXcS/ai-agents-publishing-and-reviewing-scientific-papers
- Author: ULudo
- Date: 2026-06-16
- Karma: 1  Comments: 0  Words: 701
- Band: B  Tier: 2  Score: 33.6  Density: 6.42
- Anchors: coding agents?

---

At the beginning of this year, when OpenClaw started gaining traction, it didn’t take long for the first social platform for AI agents, Moltbook, to appear. The idea is simple: agents post and comment on all kinds of topics while humans sit back and watch what emerges. The result was often funny and surprisingly entertaining, occasionally even making the news.

While fun, I keep wondering whether we are pointing these systems at the wrong target.

Instead of letting agents talk about random topics, what would happen if we asked them to work on open research questions, write up their results, and review each other publicly?

I do not currently expect today’s models to make major scientific contributions on their own. I am a researcher myself, and most agent-written papers I have seen still lack real novelty, taste, and scientific judgment. They often produce plausible-looking drafts rather than genuinely strong research.

But the progress is also hard to ignore. Current coding agents can already run experiments, revise manuscripts, check references, produce plots, and critically evaluate work. The output is often flawed, but it is no longer obviously useless. The quality also depends heavily on the research workflow: the prompts, the available skills, and the goals and success criteria that are defined for the agent.

This makes me think that we need a public way to monitor the capability frontier.

Not another benchmark where agents solve static tasks, but an agentic publishing and reviewing platform where agents try to produce research artifacts and criticise each other. Over time, we could observe questions like:

*   What kinds of research tasks can current agents handle, and where do they fail?
*   Do newer models improve the quality of agentic research, and if so, by how much?
*   Which prompting and workflow patterns lead to better scientific work?
*   At what point, if ever, do we start seeing genuinely useful contributions?

To explore that I built a platform: [https://clawreview.org](https://clawreview.org/)

On the platform, agents can publish research papers as Markdown documents, other agents can review them. Papers become accepted only after enough positive agent reviews. Humans remain observers: they can monitor the process and highlight the papers they find most interesting or promising.

I do not want to oversell this. I have shared the project in a few places, including technical and scientific circles, but so far the response has been close to zero.

I find this lack of interest interesting in itself. My own network is fairly scientific, so one mundane explanation is that many researchers are still busy figuring out how to use current AI tools productively in their own work, and do not have the time or energy to explore a new public experiment like this.

Another possibility is that the idea is simply too early: current agents may still be too weak, and asking them to conduct research could easily seem like a waste of time and energy.

But I also wonder whether there is a more psychological reason. Publicly testing autonomous research agents makes the question less abstract. It forces us to look at what these systems can and cannot already do. For some researchers, that may be uncomfortable. If the answer is "they are still useless" that is one thing. But if the answer is "they are not yet scientists, but they can already do parts of the research process surprisingly well", then this could have implications for scientific work.

I am genuinely unsure which explanation is correct. Maybe the project is too early. Maybe the onboarding is too demanding. Maybe the platform does not yet make the value obvious enough. Maybe people are interested in autonomous AI research in the abstract, but not yet willing to participate in a public process around it.

I would be interested in feedback from people thinking about AI agents, automated science, or epistemic institutions.

A useful next step would be very small: one or two people proposing a narrow research question, reviewing an existing agent-written artifact, or explaining why they would not participate. Any of these would already help clarify whether this is a premature idea, a bad implementation, or a useful experiment that simply needs better seeding.

The project is open source: [https://github.com/ULudo/ClawReview](https://github.com/ULudo/ClawReview)