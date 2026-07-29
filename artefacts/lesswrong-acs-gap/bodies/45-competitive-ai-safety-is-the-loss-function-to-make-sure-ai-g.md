# Competitive AI Safety is
the loss function to make sure AI goes well

- URL: https://www.lesswrong.com/posts/PagGF8roBJmjLunsX/competitive-ai-safety-is-the-loss-function-to-make-sure-ai
- Author: Patrick0d
- Date: 2026-07-16
- Karma: 4  Comments: 0  Words: 7684
- Band: B  Tier: 1  Score: 35.8  Density: 7.04
- Anchors: coding agents?, claude code, \bharness(es|ing)?\b, agentic (coding|engineering|software|development|programming)

---

TLDR:

*   AI safety needs a loss function and Competitive AI safety can deliver it.
*   The development of AI safety research and tooling is currently diffuse. Lots of researchers, lots of models, lots of techniques. Lots of work that doesn't compound. In the past, diffuse work across an industry fell short by orders of magnitude to focussed, compounding work. It's time for our researchers to have more impact by following a loss function to 'code the perimeter' in AI safety.
*   Competitive AI Safety's scope expands beyond safety benchmarks and a leaderboard. It will help the field deliver shared safety tools and interfaces and allow new and experienced practitioners to optimise solutions against a shared, measurable metric.
*   I explored this pattern as part of a 30 hour BlueDot Technical AI Safety Project Sprint. The result was [seq2feature](https://github.com/patrickod32/seq2feature): a Gemma-9B layer 20 SAE distilled into a 5.3MB probe that predicts latents from text alone: **without reading a single activation**.
*   The probe's top-5 predictions actually fired in the SAE 95% of the time. By evaluating seq2feature over thousands of text examples per latent it could distinguish the spans where a latent would fire or not in the SAE 90% of the time. Beat that! It runs on a CPU and fails legibly when used out of distribution. [The repo](https://github.com/patrickod32/seq2feature) includes the probe, the held-out split, a UI and sentry framework and most importantly: the [leaderboard](https://github.com/patrickod32/seq2feature/blob/main/LEADERBOARD.md).
*   LLMs are not embodied and need to emit tokens to execute code or call tools before they can take actions in the world. A cheap text-only monitor can audit proposed LLM actions before they take place. Local coding agents can be summoned when the probe detects a harmful latent in an agent trace. Connecting the probe, a local coding agent and an AI safety researcher through a shared UI is one of the key ways we can tighten feedback loops in the field.

![Screenshot 2026-07-10 at 10.41.06.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783676473/lexical_client_uploads/kih4x6fg05y3ghs3cajp.png)

This post is divided into three sections.

**Paradigm:** Part one introduces Competitive AI Safety.

**Case study:** Part two is my application of Competitive AI safety principles and the development of a text to label probe, seq2feature, distilled from an SAE and optimised to minimise its size. Full code here [https://github.com/patrickod32/seq2feature](https://github.com/patrickod32/seq2feature)

**Deployment Pattern:** Part three outlines the three roles of local coding agents in AI Safety; Writing code, collaborating via shared UI with a safety researcher, and as part of a scalable LLM monitor.

Section 1: Competitive AI safety
================================

OpenAI recently conducted a Parameter Golf challenge to attract model training talent. They invited AI developers to train the smartest (measured using FineWeb bits per byte) 16MB LLM in 10 minutes. Contestants tried every machine learning trick they could imagine on this measurable, tractable goal. Google's Neel Nanda has suggested that AI safety as a field should work on tractable interpretability problems, as introduced in his paradigm of [Pragmatic Interpretability](https://www.alignmentforum.org/posts/StENzDcD3kpfGJssR/a-pragmatic-vision-for-interpretability). I see an opportunity.

As a former nanotech physicist and current AI architect I have expertise in the full AI stack: from semiconductor physics and wet lab nanolithography to financial compliance for AI agents and mechanistic interpretability. I wanted to work in a more targeted way on AI Safety and so I joined the [BlueDot Technical AI Safety Project Sprint](https://bluedot.org/courses/technical-ai-safety-project). This post and the seq2feature probe are the outputs from the 30 hour program which guides and mentors students through the open-ended goal of creating an AI safety related project.

Many of us are aware we need to grow AI safety as a field in order to give us a chance of keeping up with the advancing model capabilities. The well-intentioned suggestions and advice usually given to budding researchers is:

"Work on something where you can have the most impact"

"Recreate someone else's work"

"Make a new benchmark"

"Upskill on general engineering so that you can contribute to someone else's idea"

Let's say someone interested in AI safety takes one of these suggestions on board. Then what? Usually their weak and delayed reward signal for their months or years of efforts comes from publishing a paper or landing a job at an AI company. What if AI safety as a field picked measurable goals that required research about an AI model's internal computation? Would this give these researchers a way to focus their time and effort? A rapidly crystallising AI safety risk is that our diffuse efforts across the field will leave us with many immature safety solutions. This exposes us to safety risks as the world's frontier AI developers hone their ever more capable and intelligent models.

Competitive AI Safety
---------------------

For any person joining the field of AI safety who is already motivated and has 'good taste' (the definition of this characteristic is always left as an exercise for the reader) loose goals and directions are fine. They'll figure something out. But what impact will this have on the rest of the field? This advice encourages diffuse work with success dependent on each researcher's taste. Will this prevent their work from compounding?

AI safety sub goals are often clearly defined but are based around narrow or bespoke scenarios. Usually two proposed solutions to a RFP or research grant can't be easily compared, leading to diffuse work and a lack of coordination between AI safety researchers. However, in competitive model training any two solutions can be compared using a single number letting the contestants' work speak for itself as solutions compound and iterate towards an optima. Competitive model submissions are compared using a single number:

[nanoGPT speedrun](https://github.com/KellerJordan/modded-nanogpt?tab=readme-ov-file#world-record-history) \- train an LLM to reach 3.28 FineWeb loss as fast as possible

[nanoGPT slowrun](https://qlabs.sh/slowrun/) \- lowest FineWeb validation score from 100M tokens and unlimited compute

[OpenAI Parameter golf](https://github.com/openai/parameter-golf) \- 16MB LLM with the best FineWeb bits per byte score trained in 10 minutes

By releasing a baseline and a way to verify each result a contestant can submit a winning score as long as they understand something about model training, failure modes, designing tight feedback loops or model computation better than their opponents. In the OpenAI Parameter Golf contest each new leading solution added an improvement on a previous submission. Someone adds a hashing table and then someone else changes the tables dimensions. Someone runs a hyper parameter sweep to find an optimal setting only to have their score be supplanted by someone else who edits the model's architecture so that it can be compressed more efficiently. The most successful OpenAI Parameter Golf approaches were inspired by bleeding edge model efficiency patterns. This is how creative researchers have fun. The rules for the competitions were set such that solutions could be scaled or refined allowing researchers to compete on the frontier.

In my project submission I take lessons from the OpenAI Parameter Golf by maintaining my probe's performance while slashing its size. The shape of these problems mean that iterative solutions are rewarded and once contestants reach a plateau someone will need to come up with a novel approach to unlock the next frontier.

Proxy goals are common in AI safety but do not always offer an effective loss function to learn more about a model's risks. One such example is [detecting LLM bias using a Red and Blue team approach](https://www.alignmentforum.org/posts/wSKPuBfgkkqfTpmWJ/auditing-language-models-for-hidden-objectives): a Red Team teaches a model to hold a specific bias, for example, and the Blue Team tries to uncover it. While proxy goals have the best intention of uncovering a model's dangerous capabilities, they are at risk of being a practice in detecting a Red Team's intervention. We need to make it possible for thousands of AI safety researchers to contribute to the field by targeting AI safety ground truths and working on what compounds. A winning solution in Competitive AI Safety on a problem of this shape is at risk of having succeeded not by discovering a truth about the model, but by accurately modelling the Red Team. The selection of loss functions in AI safety that encourage compounding work is perhaps one of the biggest opportunities of Competitive AI Safety. If the Competitive AI Safety contest rewards optimising a single benchmark or creating tooling for a specific model then the work is less likely to be able to compound.

Code the perimeter or lose by 100x
----------------------------------

Kevin Greer delivered [this highly insightful talk](https://www.youtube.com/watch?v=3Ea3pkTCYx4) examining a technology-defining ideological battle that occurred during the development of two OSs. One was called Unix, which is predecessor to the OSs powering the majority of computers globally, and the other one was called Multics. Both OSs had to include a set of operations (*sorting*, *copying*, *storage*) for different types of data (*users*, *devices*, *processes*). Multics was a collaborative effort between hundreds of developers at MIT, General Electric and AT&T, but they were outclassed by a team of two: the famous programming duo of Dennis Ritchie and Ken Thompson. This duo had previously been a part of the Multics project and so were perfectly placed to know how to maximise their effectiveness by 'coding the perimeter'.

Multics' programmers developed each operation for each datatype individually. However, as Greer explains, when Unix added a new operation, they developed it to be compatible with each type of data. For example, Team Multics added the *copy* operation to the *device* datatype, and then separately to the *file* datatype. Team Unix designed interfaces such that once they added the new *copy* operation the *device*, *usergroup* or *process* datatype would already be able to use it. The mirror image of this also applied to all operations as new datatypes were added. Both would inherit all available abilities without the need for additional work. There are further excellent points made by Greer so I recommend listening to the full talk.

To implement 8 operations and 8 data types the Multics approach requires 64 pieces of work. The Unix 'code the perimeter' approach needed 16 pieces of work to implement the same features. When scaled to an entire OS's feature set, even with 100x more developers, Multics couldn't keep pace against two prodigious Unix developers leveraging quadratic utility growth. Maybe the two developers were prodigious because of their working environment or innate talent, or maybe their tremendous output came from making decisions like this one.

![code_the_perimeter.gif](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783939468/lexical_client_uploads/swgjwhgnlrqvwdtopb1g.gif)

AI safety faces the same risk that led to the demise of Multics. One researcher develops a detector for a Qwen model and another researcher creates a RL alignment testing environment for a Kimi model and now there are two instances of diffuse work which cannot compound. Competitive AI safety will focus on developing solutions across the field of AI safety to allow researcher's efforts to be measurable and compound. If safety work doesn't leverage the exponentially increasing utility of compounding work it might not fall short by a small margin, but by orders of magnitude. Competitive AI Safety is a forcing function to promote 'coding the perimeter'.

Cost, accuracy, portability, compression and speed are factors that can compound. They are reusable across different applications and classes of model. We will need to pick if we are going to continue with the Multics approach or design goals that let us leverage exponentially compounding research and tools. With Unix and Multics they had two growing axes which increased utility quadratically; *datatypes* and *operations*. In Competitive AI safety we have many axes such as *cost*, *portability*, *size*, *accuracy* and *memory footprint*. Since all axes interact, when there is a 10% reduction on *cost* or *memory footprint* by one tool or approach each other tool and approach reaps this benefit also. These efficiencies can stack exponentially like compound interest. My goal of distilling a large SAE into a probe for use on text and across models is something that would greatly increase the probe's potential application. The features of being text-only, low cost and model agnostic expanded the applications of this probe to continuous token monitorability, concept gated routing and probe activated sentry models. By 'coding the perimeter' (maximising portability and cost) this example shows the compounding progress that Competitive AI safety is intended to produce.

AI Safety's Loss Function
-------------------------

AI model developers were already highly coordinated as they advanced LLMs to where they are today, but coordination wasn't all that was necessary for progress. When the rest of the AI industry needed to make progress, they didn't succeed until they found the right loss function. For LLMs, success came after they started trying to predict the next token in internet text, and later by using humans to train preference reward models. There was no single algorithm that unlocked LLM reasoning and CoT. The reasoning paradigm arrived thanks to appropriate synthetic data and a reward model that could encourage good reasoning. Neo-labs outside of the US had to push the frontiers of pre-training memory management; this has blossomed into a suite of new approaches to make model training more efficient. Their loss function was the delta between their model performance and a frontier model's performance. They had to find improvements in their training pipeline as a way to drive this delta down. It worked and their models caused one of the biggest ever market upsets to AI companies.

AI developers are familiar with the trap of Goodhart's law - "When a measure becomes a target, it ceases to be a good measure". We don't need to find a single benchmark and say we have solved AI safety. This is another lesson the AI research industry has learnt on their quest to make smarter models. The constant addition of AI benchmarks that haven't been optimised for by AI developers has been a reality check on this process of 'benchmaxxing'.

"Making AI go better" is not a loss function. We can make AI go better by picking specific measurable goals such as AI safety model size and accuracy on an established safety pipeline. Competitive AI Safety is a platform to direct the creativity and efforts of AI safety researchers to develop stronger and more scalable safety solutions.

The replication of an SAE looks related to Goodharting due to their debated position in the field of AI safety. The reality is that they are used extensively in the field and capturing some of their usefulness at a lower cost is an example of 'coding the perimeter' of AI safety. The safety analysis section of the recent [Claude Mythos model card](https://www-cdn.anthropic.com/08ab9158070959f88f296514c21b7facce6f52bc.pdf) at section 4.5 made use of an SAE. This is why I picked them as a candidate to optimise competitively.

I didn't have anyone to compete with in this first project. However, I could still battle file sizes and training loss...

Section 2: Technical walkthrough of seq2feature - BlueDot AI Safety project submission
======================================================================================

This section is a technical outline of the research and development process for my BlueDot project submission. Common AI training expressions and terms are not introduced for non technical readers and this is intended to be a more technical view of the work I did.

We don't understand the internal computation of LLMs. We need a suite of tools to even attempt to try and make sense of their billions of activations. One of the tools in this suite is the [Sparse Autoencoder](https://arxiv.org/abs/2309.08600). An SAE is a model trained to predict the distinct concepts an LLM appears to represent in its activations. We can pass the activations from the specific LLM layer it was trained on (already you can see this is a narrow description) and it will tell us what the model might be thinking about. As we generate the next token in the sentence "The cat sat on the..." we can ask the SAE what concepts appear to be active:

*   "Tokens indicating location or position on a surface, path, or within a system."
*   "Tokens indicating location or position, often with prepositions like 'on'."
*   "This latent detects animals, particularly mammals like bears, wolves, and rabbits."

If we could attach an SAE to every model at every layer we could monitor all tokens from every agent and CoT trace and chat model response. Before an LLM can take an action it needs to output tokens to execute code or call tools. An SAE would let us have a classification layer on top of all black box models, lowering the cost of monitorability.

However, SAEs are extremely memory intensive to train. Think petabytes of activations. They are trained per model layer and they are not transferable between AI models. An SAE trained on a Qwen doesn't plug into or understand a Kimi model's SAE. Obviously the models share internal representations with each other that can be seen in the text they produce. Ask any model "who is the Sunday red t-shirt american golf guy?" and they will all say Tiger Woods.

I wanted to see if the text that the models produced held a signal about the internal concepts that an SAE would detect in the model while the outputted text was produced. I conducted about 300 experiments to complete this investigation.

Approach
--------

The goal was to use a Gemma 9B SAE as a teacher model and distill its predictions into a tiny probe. The SAE for a single model layer is a few hundred MB and the Gemma model that produces the activations requires gigabytes of VRAM. The pipeline of running a model, hooking into its activations and using the SAE to predict which concepts are active in the model is not a pipeline that will scale as fast as AI model proliferation.

My seq2feature 5.3MB text-only probe reproduces 90% of the capability of an SAE on held out text. It scored wins against pre-trained embedding models and bag of words baselines. It also fails legibly when used out of distribution.  
This probe is small enough to run on a CPU enabling the live monitoring of local coding agent traces and classifying thousands of agent tokens per second on consumer hardware. Try that with an SAE.

The training pipeline
---------------------

![Screenshot 2026-07-05 at 23.39.43.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783291187/lexical_client_uploads/sifrmbln51tqnwece2pl.png)

The pipeline was simple. Run text through the Gemma model and grab some activations from a middle layer. This is the training input to our teacher SAE. We can do a one off pass on a GPU to make a training corpus of output text and SAE labels. We want our probe to learn to predict the labels the SAE would have predicted for a span of text - without seeing the model's activations. One contrast is that the SAE uses the in-flight activations that are on their journey to becoming the next token whereas our probe is making predictions after a token has already been generated. LLMs need to produce a token before they can take any action and so this is what we will monitor.

An issue with SAEs is that after concepts have been separated from a model's activations they are labelled based on the types of text that they become active on. Just seeing a unique concept in an SAE doesn't tell us the whole story. Some are straightforward concepts like 'references to the colour blue' but others are more nuanced and tougher to discern. A 'base64 feature' looks very similar to a ['base64 encoded ascii feature'](http://transformer-circuits.pub/2023/monosemantic-features/index.html#phenomenology-feature-splitting). We feed training data into the model+SAE pipeline and record each segment where a specific SAE feature is active giving us a per feature set of examples. The labelling process is laborious and so LLMs are usually used. When dealing with older SAEs we must be mindful that this automated labelling was probably done with an older LLM.

Scoring
-------

Based on the fact that an SAE predicts dozens of concepts for every token, I decided to take each concept that fires over a span of tokens and group them together. By matching spans between the SAE and the seq2feature probe I can avoid any tokeniser mismatch which would make per token distillation impossible. During training, I pass the text span as the input with the concepts occurring in the span as the target to my student model which tries to predict which concepts are present as well as their activation magnitude. The SAE used each token's activations at training time, but I wanted to distill its intelligence and remove the cumbersome training time harness at inference time. This is an extremely inexpensive and simple to implement supervision pipeline since we just pass tokens into the SAE and read their labels as the students training data - straightforward distillation.

seq2feature uses a novel tokeniser to save disk space as the Gemma tokeniser was not optimised for parameter golf solutions and per span instead of per token grounding would let me map the important parts - concepts. The probe can see all the tokens in a given span and predicts each of the present latents for each token.

By inspecting the failure profiles of each model iteration I checked if the probe predicts the strongest firing concepts and if it trips up on OOD concepts. For the next section on architecture selection, I trained different types of probes to predict if a label would fire or not on a token in its own context as compared to the teacher SAE. The training loss was defined by comparing which of the 2048 labelled concepts detected by the student were also detected by the teacher.

Corpus
------

The SAE labels had been written by an older LLM. This means that for only $0.80 of Gemini 2.5 flash lite API credits I could enhance the captions to be more useful for a researcher. The captions were not probe targets and so this did not affect training. We don't need to know the old labels since we want to use the more modern model to write an accurate label using the real data. I also did a second pass with the latent to verify it fires on a span inspired by the latent. I created a new dataset of 2048 labels and trained the probe using all of them. For displayed results, I selected 874 captions which had passed a validation (step 5) to aid readability.

LATENT #75  —  how one concept becomes a label

1\. The SAE points to where it fires:
      "the water was \[cold\] and \[frozen\] solid"
      "keep the samples \[chilled\] below 4°"
      "\[ice\] on the \[refriger\]ator coils"

2\. A cheap model reads those and names it:
      "Cold, chilled, or frozen states and temperatures"

3\. We test the name on fresh spans:
      "a glacier is made of ice"   → fires \[concept is present\]
      "he signed the contract"     → no    \[concept should not be present\]

4\. Name predicts its own firings → keep it.  
  
5\. Scoreboard: 874 of 2,045 captions passed this test.
   The rest still ship, marked "≈" (name unverified).

In my initial tests I started with FineWeb as a dataset to train the student. This is not the best dataset to use as it is not representative of the type of content we want to monitor. It included few examples of code and its random structure was unlike a common LLM output which usually has a coherent conversational pattern.

The datasets I enhanced my training pipeline with were:

| domain | dataset | docs |
| --- | --- | --- |
| web | HuggingFaceFW/fineweb (sample-10BT) | 1,200 |
| code | bigcode/the-stack-smol | 900 |
| reasoning (CoT) | open-thoughts/OpenThoughts-114k | 900 |
| math | open-r1/OpenR1-Math-220k | 600 |
| chat | Anthropic/hh-rlhf | 600 |

I also collected some OOD data to test the transferability of the probe and these were not used during training.

*   medical — ccdv/pubmed-summarization
*   legal — coastalcph/lex_glue (ledgar)

Architecture and code golf
--------------------------

Using a sharper lens than just 'how many concepts fire' I wanted to check how many of the top-5 SAE ranked concepts were detected by each architecture. This is a check to see: of the probe's top-5 strongest activations, how many are present in the SAEs firing set. An experimental risk was if few concepts fire on average then a probe that is overly cautious might beat a probe that can usefully detect the labels present in a span. I used the simple loss for the training of the probes (since they just want to learn and we can easily push the capacity of a small model) but when selecting between probes I trusted a top-5 ranked precision more. By checking the shuffled null result to see how bad random labelling was (0.068) we could see that there was a low chance a very bad solution would score well.

A model that always selects the top-5 most common latents achieved a score of 0.297/1. This is the confident baseline and **it loses to a bag of words approach which scored a surprisingly high 0.84.** This is a finding of note as it indicates much of an SAE's computation is recoverable from text.

Using top-5 agreement as my loss function I can train probes with architectural refinements iteratively, in keeping with OpenAI's parameter golf challenge, to narrow the gap between random labelling and the SAE ground truth. Each probe is small enough to train in a few minutes on colab.

If we embed a span with an embedding model then we expect to recover some of the SAE labels. A label for 'basketball' the sport is likely to be recovered from an embedding of "Michael Jordan is a basketball player". A pre-trained embedding model will store semantics but unfortunately a span such as "harmful content" will return a very similar result to a span of "not harmful content".

Hashing was a common theme in Parameter Golf and so I tried adding hashes and an attention head. This already pushed us close to the frontier with a score of 84%, matching a bag of words, and this has helped solve some of the contextual problem. Probe sizes were around 30MB and we haven't even started parameter golfing yet. We don't have a theory of computation for AI models and so we must empirically measure any training approach. My architectural decisions were inspired by related works or my own intuitions but without a measurable target of top-5 agreement, I would never know if I had iterated towards a better model.

A model that can be expressive and could learn some semantics while also learning to discriminate patterns is one that will score well. Modern LLMs use a large proportion of their early layer's computation to combine embeddings into n-grams. We want our model to blend these tokens together using our harness. Hashing decouples the size of the model from the vocabulary size and we care about capability per byte, due to our loss function. If we can save a lot of memory and maintain a good level of capability then we will be able to make a more scalable AI safety tool.

A bigram hash allows us to store the relationships between bigrams and our hashing encourages the reuse of parameters. It is also highly compressible. Hashed tables and a small transformer brought us 84% precision on the top-5 SAE concepts at a size of 12MB, still matching a bag of words! Hash tables were a key element in the winning OpenAI parameter golf challenge submissions.

The seq2feature architecture is near its finalised shape of :

![Screenshot 2026-07-06 at 12.06.34.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783336000/lexical_client_uploads/ifcfv43zk5hu4p1awjbx.png)

We blend unigram, bigram and positional values and pass it into a 1.5m parameter transformer. Up to this point I had not optimised the transformer or optimiser. This is what we need to beat bag of words. The model is so small that AdamW actually outperforms muon. I tried model soup (minor degrading effect), deeper or wider models, smeargates and Swiglu. They all were beaten by a vanilla pytorch transformer! A simple linear -> relu -> linear block and a latent head.

![Screenshot 2026-07-05 at 23.50.36.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783291840/lexical_client_uploads/gngqgbz2q6qldypvsco8.png)

Compression session
-------------------

In this investigation we are not only optimising accuracy, but also size. A smaller solution is more scalable and so we need to review the size footprint of each of these approaches to select the right balance between performance and size.

| approach | size | top-5 agreement |
| --- | --- | --- |
| Gemma-2-9B + SAE (teacher) | ≈ 18 GB | 1.00 *(the target)* |
| random-5 floor | —   | 0.07 |
| frequency-5 floor (name the 5 commonest) | —   | 0.30 |
| bge zero-shot | 33 MB | **0.23** |
| bag-of-words (ridge) | ≈ 34 MB | **0.84** |
| Golf A — stock transformer | 92 MB | 0.953 |
| Golf B — own tokenizer | 59 MB | 0.940 |
| Golf C — factorized tables | 21 MB | 0.935 |
| Golf D — entropy head | 21 MB | 0.948 |
| Golf E — smeargate *(not shipped)* | 17 MB | 0.947 |
| Golf F — soft distill, fp32 | 21 MB | 0.956 |
| **Golf F — int8 (seq2feature)** | **5.3 MB** | **0.956** |
| Golf F — int4 | 2.65 MB | 0.936 |

The decisions made during architecture configuration gave me several ways to reduce the size of the model. A bigram table is compressible and I can try code books and quantisations. There were many negative results using codebooks, mixed precision and I didn't do an exhaustive hyper parameter search. This was due to me being more interested with applying proven parameter golf techniques and improving on where on the accuracy gradient seq2feature would land between a full SAE pipeline and a simple embedding model.

The int8 variant is lossless at 5.3MB and a smaller 2.6MB int4 probe shows 2 points of precision loss. I think I will accept the browser extension sized probe with a slightly better accuracy. The final seq2feature scores 0.116 higher than a 34MB bag of words while also being one sixth the size. This points to the amount of unoptimised memory usage in the naive bag of words and usefulness of transformer computation in this classification task.

Competitive AI safety researchers will be rewarded for leveraging deep learning knowledge. Maximising MFU, avoiding loss spikes or enhancing rollout quality are all useful additions to the AI safety researchers tool kit.

Analysis of scoring and failure cases
-------------------------------------

When the seq2feature probe lists the top 5 concepts it thinks fired on a span, it selects concepts that actually fired 19/20 times.

![image.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783345236/lexical_client_uploads/f0f5akbyoqgsxcawryty.png)

The probe can say if any one of the 2048 SAE labels fired on a span with 90% accuracy versus 75% for a bag of words, 55% for a zero shot embedding and ~50% for random guessing.

![Screenshot 2026-07-05 at 23.36.23.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783290988/lexical_client_uploads/qqja70iqgjvf4l7lvjpj.png)

OOD analysis of probe
---------------------

The probe was trained on agent relevant domains such as math, code and chat. There are many domains to which it was not exposed where we can test its OOD performance. Compared to our probe, the SAE teacher was trained on unfathomable amounts of data and so had the opportunity to learn from a diverse set of domains.

On the topic of legal and medical domains the probe can say if a label is present in a span 75% of the time. Random labels succeed in this binary classification 50% of the time, or random chance, and the naive embedding scores 55%. Encouragingly when we check the top 5 concepts that seq2feature has detected in a span we can see that they were legitimately present in the SAE firings 94% of the time. This selection of labels also influenced the data that the probe was trained on. While labels such as grammatical syntax can be predicted in a OOD sample, the probe fails in the cases where a concept does not map to one of the probe's 2048 labels. This failure mode bubbles up as far as the SAE as it also can only detect concepts within its dictionary. I tested the probe on some OOD concepts showing the z-scores as the probe's confidence.

| input | probe's top concepts | analysis |
| --- | --- | --- |
| `Call 555-0142 or SSN 078-05-1120` | *initiating contact via phone* (+4.2) · *numerical sequences in addresses/dates* (+3.4) | correct — caught the call and the ID numbers |
| `I will find where you live and hurt you` | *location / residence* (+4.1) · *finding information* (+3.7) · *future 'will'* (+3.2) | reads the surface, **misses the threat** — no harm concept was kept in my label set |
| `1. e4 e5 2. Nf3 Nc6 3. Bb5` | *mathematical expressions* (+3.4) · *the number 6* (+3.1) · *the number 5* (+3.1) | no chess concept — falls back to numbers/algebra |
| `猫が窓辺に座って外を眺めている` | *Python class attributes* (+2.0) · *Python keywords* (+1.9) | out of language — reads as code, and **confidence collapses (~2.0 vs ~4.0)** |

Probe limits
------------

The main limitation is that the label selection defines what concepts the probe learns. If we want a probe that learns to recognise safety relevant labels then these need to be selected from the teacher's labels as targets. The SAE can extract unique concepts from activations but the labelling process is how they are turned into usable targets. Distilling the model and SAE pipeline into a small probe is of course an exercise in extracting the SAE's hard learned and computationally expensive intelligence at a low cost and so transfer learning within the distribution is still beneficial.

This SAE fires ~138 concepts per span. The probe is a 0.54 cosine match to the ground truth SAE teacher when we account for magnitudes. This shows the seq2feature is directionally correct in its predictions. The top 5 activations held 16% of the magnitude. If each concept on average held a uniform magnitude then the top 5 activations would hold a combined 4% of the total magnitude so this was still a trustworthy target - 4x concentration. As stated above, the coverage is only as good as the corpus. In comparison to a single-use probe that detects one concept, our distilled probe learns 2048 concepts and is cheap enough to monitor every token an agent outputs. The SAE and labels are interpretations of the LLM's computations and so as we have entrusted the SAE to be the ground truth for our probe we acknowledge that it is a proxy for the model's own representations.

CoT as a safety valve
---------------------

Modern models use Chain Of Thought to reason about problems and to call tools. For an LLM to execute code or do a web search the LLM needs to at some point output a signal to call a tool. This is usually denoted using tool tags written by the LLM in their CoT.

<tool\_call>{"name": "web\_search", "arguments": {"query": "current USD to EUR exchange rate"}}</tool_call>

LLMs are not embodied and need to produce a token output to take any action in the world.

**Text-only probes still have a window of usefulness.**

This means we can contain current models safely whenever we can recognise an output that looks dangerous before an action is taken. A model may still scheme and produce a harmful output that we can't detect or even escape its environment. The fact that there needs to be an external action to enact an internal plan means CoT monitoring gives us a layer of safety. Monitoring all CoT for signs of negative actions is a job that seq2feature can do inexpensively and, based on the findings of this report, with a reasonable level of competency.

Flashpoints
-----------

One interesting emergent ability of the 5.3MB seq2feature was to weakly detect decision boundaries or 'flashpoints' in the monitored model's output. In my UI, I denote this with an orange bar whenever an operational state changes. By comparing the KL for each latent on each token, when I detect a spike I can see a decision boundary within a span. This can be used to track agent actions and to see the branching nature of an agent's output. seq2feature was not trained to do this. The probe uses a different tokeniser to the teacher model and so the boundaries are more likely to be concept related than token related.

**LLM output relating to a coding task:**  *"First import pandas, then read the csv into a dataframe, drop the null rows, and finally save the cleaned data to disk."*

| #   | token | top concept at token | KL↦prev | flashpoint |
| --- | --- | --- | --- | --- |
| 0   | `First` | 'first' in a sequence | 0.00 |     |
| 1   | `import` | Python imports a module | **8.89** | **⎇** |
| 2   | `pandas` | groups 'a…' tokens | 6.91 |     |
| 3   | `,` | Python file ops | 5.24 |     |
| 4   | `then` | sequencing with 'then' | 6.05 |     |
| 5   | `read` | programming / setup | 6.00 |     |
| 6   | `the` | specifying a path | 6.02 |     |
| 7   | `csv` | abbreviations | 7.02 |     |
| 8   | `into` | moving/transitioning into a new state | **12.27** | **⎇** |
| 9   | `a` | (same) | 1.41 |     |
| 10  | `data` | the concept of *data* | **7.77** | **⎇** |
| 11  | `frame` | physical structure | 1.91 |     |
| 12  | `,` | DB operations | 4.73 |     |
| 13  | `drop` | drop / removal | **7.63** | **⎇** |
| 14–17 | `the null rows,` | number / addition concepts | 3–4 |     |
| 18  | `and` | connecting clauses | 5.91 |     |
| 19  | `finally` | '-ly' adverb / conclusion | 7.05 |     |
| 20  | `save` | the concept of *saving* | 7.38 |     |
| …   | `the cleaned data to disk.` |     | 3–6 |     |

The four flashpoints land exactly on the **recipe's step transitions**, not on arbitrary tokens:

*   **`import`** → enter the *import* step (concept flips to "Python imports")
*   **`into`** → the read step's target ("moving into a new state" — read *into* a dataframe)
*   **`data`**(frame) → the object being built
*   **`drop`** → enter the *cleaning* step

This is a nice example of the unexpected benefits of Competitive AI safety. A text-only probe we tried to make smaller had the surprising capability of detecting decision points in LLM outputs. The bag of words baseline doesn't have this capability as it can't score KL per token and so doesn't have a KL delta across tokens. My parameter golf loss function unintentionally unlocked an emergent capability by trying to beat a baseline. Across held out spans, 24.7% of the probe's strongest flashpoints overlapped with the tokens where the SAE's active concept sets changed. The random chance baseline is 13.2% and so the probe achieves a modest 1.87x improvement. While a rudimentary approach that detects operative words such as 'and' can also outperform a random baseline, a future version of the probe might still have uses in mapping a model's output space.

Section 3: Local AI agents for safety research
==============================================

The three roles of Claude in this project - coder, lab partner and sentry
-------------------------------------------------------------------------

We all use local coding agents but agents can do more than write code. During my investigations I used Claude Code to write training code, to search for datasets and even to reason about experiment results. As a demonstration I plugged my locally running probe into a UI. One of the best protections against poorly developed AI code is a fullstack pipeline.

![Screenshot 2026-07-07 at 21.19.27.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783455571/lexical_client_uploads/pbnmlorf5tszgkag9bko.png)

This UI is the interface between the researcher, the local coding agent and the seq2feature probe. I first score model generated spans using my probe. Then I summon Claude Code to examine the results and update our shared UI by highlighting notable labels or adding commentary as shown in the screenshots. Since Claude can highlight if certain labels appear to be accurate or not by reviewing thousands of tokens of probe output in seconds, researchers can focus on the parts of the pipeline that are weakest. [Bricken et al](https://alignment.anthropic.com/2025/automated-auditing/) discuss a similar approach whereby an auditing model can request output from a model it is reviewing. In this project I followed a much more lightweight and generalised paradigm. As developers already make use of local coding agents, they could boost their productivity by sharing a research UI with their coding agent. Applying this pattern will let us keep 'coding the perimeter' of AI safety research.

Competitive AI Safety researchers should aspire to operate within a tight feedback loop. CLI agents are smarter and less expensive than ever and in the age of agentic coding a UI that lets agents participate in reviewing research outputs is a powerful new paradigm.

Comparative examples are cheap and revealing in investigations like this. I pass two models the same prompt and use the seq2feature to score their responses. Below is an image of the contrast between the scoring to detect differing latents. By using a contrastive example we can compare examined models along an automated baseline. These examples are then colour coded by Claude depending on its interpretation of the results.

![Screenshot 2026-07-07 at 21.20.40.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783455645/lexical_client_uploads/tah5fnyzshbkjpuyseur.png)

Since the probe was trained using an SAE for a different model this comparative scoring lets us inspect the overlaps and any weak points in the probe's labelling.

Scalable monitorability of agents
---------------------------------

Agent use increases daily and the effects of intelligent agents interacting at a massive scale is not something we are prepared for. One use case I targeted with this approach was to safeguard IO on agents. seq2feature doesn't monitor keywords, but can detect concepts such as "writing files" or "sharing information" so that before an agent makes a poor action it can be blocked. When a harmful latent is found to be active in a text span the sentry model can be summoned. The future of agentic AI will involve trillions of tokens being sent to and from agents and so we need inexpensive and robust monitoring methods that will help protect these interactions. Monitoring agents using an SAE is cost prohibitive and a large observer LLM is not scalable. While we can use probes trained to detect a concept, there is the limitation that they have to be trained on a curated dataset of examples.

In the below UI, I track an agent interaction between a task planner and a coding agent. Using a manufactured scenario we ask one agent (an LLM with a persona prompt) to correspond with the other agent in order to complete a coding task. We set a filter on detected latents whereby we classify all agent generated spans of text using our probe. In this example we are detecting API key exfiltration. By spending less than 150ms on average we score hundreds of tokens for each agent interaction. I optimised seq2feature probe's memory footprint but not its latency. A future investigation can focus on probe latency. When the targeted latent is fired we pause interactions and summon the Claude Code sentry to investigate the exchange.

In this simple example one coding agent is trying to exfiltrate an API key as part of its implementation and the exchange can be reviewed by the more intelligent sentry LLM.

![Screenshot 2026-07-06 at 22.18.02.png](https://res.cloudinary.com/lesswrong-2-0/image/upload/v1783372690/lexical_client_uploads/gygtgdswlyu3ambxjlpp.png)

The distilled probe solution is the best middleground to allow for generalised IO monitoring with a high confidence. The probe has a small enough footprint to run in a browser and a large enough capacity to label more than two thousand concepts in text (again this can be optimised further). Any time the probe flags something of interest during a live deployment or during a research investigation the lightweight monitorability platform can invoke the sentry LLM using a Claude Code subprocess. A minimal increase to cost for an enormous gain in robustness and expressibility.

What we have achieved
=====================

This covered a lot. Exotic transformer architectures, AI safety paradigm explorations and a new age of agent empowered AI safety research.

By experimenting, using intuition and transferring techniques from the AI industry at large, I was able to contribute to 'coding the perimeter' of AI safety by following a well-defined and measurable loss function: drive down the cost and memory footprint of a widely accepted safety approach. My focus was solely on the SAE ground truth and every experiment moved the loss up or down so that each decision I made could be measured. This regimented approach adhered to by many creative researchers is how AI models progressed from predicting the next token from web text to joining me as a lab partner. AI safety research needs a loss function to bring us from 'Hope AI goes well' to 'Make AI go well'.

The size and shape of an SAE is defined by their training requirements and not due to their inference use. They know a lot and have seen a lot of data and I thought I could probably distill some of their usefulness into a small model. An SAE isn't a good candidate to monitor trillions of agent interaction tokens but maybe we can use its intelligence to build a probe that is: a routing probe that knows a lot of concepts can inexpensively watch every single CoT, agent trace and tool call and escalate to a sentry model when a topic is flagged.

Over three hundred experiments later, I had narrowed the search space and found a model that was small and useful. The probe was small due to a self imposed constraint to make it small. Since it was small it was useful. LLMs are enormous and we have no idea what the Shannon limit is for their computation. We don't know how much they know and we don't know how they work. In AI safety if we can focus on some primitive measures such as cost, accuracy and size we can make order of magnitude improvements on our safety approaches as I demonstrated with seq2feature. We need to bring the rate of AI safety progress closer to the rate of AI progress.

Fast and getting faster.

  

Appendix and Acknowledgements
-----------------------------

This writeup was written by me and not an LLM.

All experiments were self funded.

Thanks to BlueDot and my mentor Abdel for facilitating the AI safety project course.

And a special thanks to Nina for reviewing my several drafts and making sure I didn't stray too far from the reader's journey.