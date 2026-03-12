---
duration: "10-15 min"
batch: 1
order: 1
batch_name: "Seed Thinking"
class: "prompt-engineering"
chapter: "Seed Thinking"
---
## Infusing Life Experience Into Your Prompts

AI is optimized to *continue* thought, not *generate* new thought. The creativity is in the seed — your seed. Your lived experience is the most valuable input you can give a model, and most people skip it entirely.

### The Core Idea

This comes from a concept explored in "The AI Paradox" by Jared Henderson:

> "A large language model is optimized to continue thought, not generate new thought. The creativity is in the seed thought and its continuation — the human input. AI has no inbuilt curiosity or preferences."

> "In a world where the cost of answers is dropping to zero, the value of the question becomes everything."

> "The input is the work. The input is the value."

Research confirms AI is weaker than humans at divergent thinking (generating truly novel starting points) but highly effective at convergent thinking (refining and executing once you give it direction). So the prompt — the seed — is where *your* value lives.

![[images/core-idea/excalidraw_9.png]]
### The Evidence: What Happens When You Skip the Seed

**The MIT writing study (2025)** — ["Your Brain on ChatGPT: Accumulation of Cognitive Debt when Using an AI Assistant for Essay Writing Task"](https://arxiv.org/abs/2506.08872) (Kosmyna et al., MIT Media Lab). Students wrote essays under three conditions: brain-only, Google-assisted, and ChatGPT-assisted. Researchers monitored brain activity with EEG while they worked. The findings:

- Minutes after finishing, when asked to recall a single sentence from their own essay, **83% of the ChatGPT group couldn't recall any specific text**. The few who thought they could? 100% of them got it wrong.
- The ChatGPT group showed significantly lower neural connectivity — their brains appeared to *dim* while working.
- When evaluators read the essays, the AI-assisted ones were technically proficient, grammatically correct, structurally sound — but consistently described as **"hollow" or "soulless."** They were remarkably similar to each other.

But here's the most interesting result: they tested one final group — **human first, then AI access**. Students who outlined their own thinking first and then used ChatGPT showed *higher* brain connectivity than even the human-only group. The difference was the starting point. Human first, or AI first.

![[images/mit-writing-study/excalidraw_7.png]]

**The story similarity study (2024)** — ["Generative AI enhances individual creativity but reduces the collective diversity of novel content"](https://www.science.org/doi/10.1126/sciadv.adn5290) (Doshi & Hauser, *Science Advances*). ~300 people wrote stories, some with AI assistants to seed their ideas, some without. When they analyzed all the stories together, the AI-assisted stories were **significantly more similar to each other**. Our collective thought narrows when everyone uses the same tool.

**The personas experiment** — ["Using Generative AI Personas Increases Collective Diversity in Human Ideation"](https://arxiv.org/abs/2504.13868) (Wan & Kalman, 2025). Researchers wondered if diversity could be restored. They gave writers 10 wildly different AI personas — a Latin American magic realist, a dystopian hard sci-fi writer, etc. It worked: the pool of stories became diverse again. But the catch was that the diversity only came from the human-designed personas in the first place. Within each persona, internal similarity was 0.92 — near-identical outputs. **The AI doesn't generate new diversity. It remixes what humans feed it.**

**The echoes study** — ["Echoes in AI: Quantifying lack of plot diversity in LLM outputs"](https://www.pnas.org/doi/10.1073/pnas.2504966122) (Xu et al., Microsoft Research, *PNAS* 2025). Examined GPT-4 and LLaMA-3 on story generation and found LLM outputs consist of "echoed" plot elements — the same combinations repeating across generations. One output looks novel. Many reveal they're all banal echoes of the same thing.

![[images/story-similarity-echoes/excalidraw_3.png]]

### Why This Happens: The Weighted Dice

Think of all possible thoughts as a massive tree, infinite in size. Each thought is a pathway — each step is a word. Your mind only ever explores a tiny sliver of this tree. But that's *your* sliver. The pathways you choose are like a fingerprint.

AI's dice are weighted, heavily biased towards what's been said before in its training data. That's why the paths make sense but always cluster and echo each other. You can't escape the weighted dice.

Human thought is different. Your dice are weighted by your unique life experience and what matters to you. And this weighting is always changing. You wander into territory nobody else has been and the AI couldn't reach.

![[images/weighted-dice/excalidraw_10.png]]

### What This Means for Prompt Engineering

Most people prompt AI like a search engine: "give me ideas for X." That's asking the model to diverge — the thing it's worst at. The output will be generic, clustered, and echoey.

The better approach: **seed it with your lived experience, then let it converge.**

Your unique experiences, observations, and half-formed ideas are the starting point. The model's job is to extend, refine, and explore the territory *around* your seed — not to invent the seed for you. This is the difference between asking "what should I make a video about?" and saying "I noticed X happening in my business this week, and it connects to Y — explore that."

![[images/prompt-engineering-implication/excalidraw_4.png]]

### The Practical Technique

One of the most powerful things you can do is take something you found genuinely interesting — a video, a podcast, an article, a conversation — and feed that into Claude alongside your own business context.

**Example workflow:**
1. Watch a video or read an article that sparks something for you
2. Copy the transcript or paste the article into Claude
3. Add your own business context: what you're working on, what your audience cares about, what problems you're solving
4. Ask Claude to explore the intersection — "given this idea and my business context, what are the implications? Where does this connect to what I'm building?"

The transcript or article acts as the seed — it puts the model into the right region of idea space. Your business context acts as a filter — it steers the exploration toward territory that's relevant to *you*. Together, they invoke a part of the model that a generic prompt ("give me content ideas") would never reach.

**This is prompt engineering meeting context engineering.** The prompt is the seed (the direction), the context is the soil (the constraints and relevance). Both matter.

![[images/practical-technique/excalidraw_3.png]]
### Demo

1. Take a real transcript from a video I found interesting (show the copy-paste workflow)
2. Add my business context alongside it
3. Show what Claude produces when seeded this way vs. a generic "give me ideas" prompt
4. The seeded version will be dramatically more specific, more connected to my actual work, and more likely to contain ideas I wouldn't have reached on my own — because I aimed the model at a specific region of thought space instead of asking it to wander generically

### The Fingerprint Metaphor

From The AI Paradox:

> "Out of the infinite possibilities, I'll only find a handful of these paths. Those paths have my fingerprint. An AI generating a random script or video based on my past work will be a distant echo, a very blurry fingerprint, because the chance of it finding all my next thoughts is zero."

> "Generative AI is all about small inputs and large outputs. When you have small inputs and large outputs, there is simply no way for you to put all of your intention to specify all the things that need to be specified when making art."

The takeaway: the more of *your* thought you put into the input, the more the output reflects you. Small generic inputs produce large generic outputs. Rich, experience-laden inputs produce outputs that actually extend your thinking.

![[images/fingerprint-metaphor/excalidraw_9.png]]
### Key Insight

> "Asking common questions to AI constantly will lead to atrophy. Like using GPS every day in your own neighborhood, you'll lose the map in your head. But asking rare questions you've never asked before to an AI — the ones specific to your experiences, the connections only you could make — that's different. Finding the question itself is the work."

Source: [The AI Paradox — Jared Henderson](https://www.youtube.com/watch?v=fPFoTx-fXGw)

![[images/key-insight/excalidraw_5.png]]