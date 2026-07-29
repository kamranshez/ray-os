# Guardian Angels: LLM Personalization for Productivity and Security

- URL: https://www.lesswrong.com/posts/siWqHqCSybdhtWGud/guardian-angels-llm-personalization-for-productivity-and
- Author: gwern
- Date: 2026-06-17
- Karma: 169  Comments: 38  Words: 464
- Band: C  Tier: 2  Score: 27.5  Density: 5.0
- Anchors: \bharness(es|ing)?\b

---

Powerful LLMs will be deployed at global scale in the next few years, and will dominate the Internet, and increasingly, ordinary life.
As of mid-2026, there is no coherent vision for how knowledge professionals, or ordinary people, will be able to harness these LLMs for large productivity increases, or how they will handle cybersecurity and cognitive security.

I propose a goal of creating **Guardian Angels** (**GA**): digital twin LLMs which are personalized with the goal of providing not the stereotypical "assistant chatbot agent" persona, but *emulating a single user's* personality, values, and preferences.

This weakly solves the principal-agent problem by unifying the principal and agent as much as possible.
In a GA future, the focus of the "principal" user is on defining what is *worth* doing by the GA (agent) users, and not on *what* or *how* to do things, functioning as the CEO or 'board' of an 'AI corporation'.
This allows them to deploy numerous agents to achieve desirable things and to handle security, like screening all messages for advanced attacks (like interlocking ecosystems of synthetic media for propaganda or spearphishing).
They cannot solve larger AI alignment problems, but they can help individual humans as part of a society-wide defense-in-depth strategy.

A GA persona is productive because it learns to emulate the principal's outputs but with higher quality.
It is trustworthy because it is, by definition, allied with its principal and shares its values and goals.
And it is secure in part by hardwiring a single, unique, situated user (for whom following a prompt attack would be absurd), avoiding 'confused deputy' problems, while periodic upgrades of the underlying model and the defenders' advantage allow GAs to keep up with attackers.

Standard techniques like prompt programming of in-context-learning for "frozen" models will not create useful GAs due to the limitations of post-training, context windows and self-attention with frozen weights in compute-efficient-but-under-parameterized models, low-compute outputs, and the status quo of passive offline data collection---which are collectively responsible for chatbots' disappointing results in knowledge worker amplification and creative writing and fatal errors in agentic settings.

We can try to create GAs by a combination of techniques: online learning (via dynamic evaluation) to update LLMs in realtime to avoid ignorance and fatal errors while remaining competitive with frozen frontier models, sample efficiency from pretrained preference-oriented large models and active Learning by querying the principal for corrections and preference data (obtaining low regret from DAgger-style bounds), and a local CLI-first logging-oriented UI/UX paradigm.

GAs could be done as an open-source community effort, but given the need for high security in deployment and the rising challenge of APTs equipped with Mythos-scale attackers, it probably makes more sense as a startup, catering initially to power-users and knowledge workers such as CEOs or researchers, and moving downwards as it is refined.