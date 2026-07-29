# Human-Guided Agentic Research: A Research Agenda

- URL: https://www.lesswrong.com/posts/8KrTuCAzL2fdYHNrv/human-guided-agentic-research-a-research-agenda
- Author: fastfedora
- Date: 2026-06-29
- Karma: 49  Comments: 7  Words: 4698
- Band: C  Tier: 1  Score: 27.8  Density: 3.67
- Anchors: \bharness(es|ing)?\b, claude code

---

![](https://res.cloudinary.com/lesswrong-2-0/image/upload/f_auto,q_auto/v1/mirroredImages/8994a2cdba78e2f0a9d1fa0712e7ec252df4d81af82a1dd86eab3be973d2d5f4/gzsszuottvzazufkx36z)

*tl;dr: As recursive self-improvement accelerates, we need a top-level agenda to research how to effectively keep humans in the loop. We need to study how humans can best interpret and guide research performed by autonomous agents when those agents lack taste, tacit knowledge or competence, or may try to reward hack, sandbag or sabotage such research. This is one attempt to define the problem and the shape of potential solutions.*

A Story About the Future of Research
------------------------------------

Imagine yourself a year or two in the future. Recursive self-improvement (RSI) is accelerating. Agents work in swarms independently for days or weeks at a time doing research.

You work in a frontier lab doing AI safety research. You sit in front of your computer and click into the input box, ready to kick off a new project. What do you type?

“Solve AI alignment”? Beware giving a magic genie vague wishes.

Think about that again: what *exactly* do you type? How do you know what you type is the best way to prompt this agent swarm into doing your bidding?

When the lead agent comes back a week later, what exactly does that output look like? How do you use that output to launch the next phase of the project?

How will you validate that output to ensure the agent hasn’t reward hacked, sabotaged or incompetently explored the research space?

How will you know what key decisions the agent made? Which research paths they explored? Which research paths they intentionally or unintentionally left unexplored?

How will you know how faithful the research the agent did was to the goal you gave it?

Today these questions are productivity issues—soon they will be safety issues. If we don’t start researching how humans can effectively interpret and direct agentic research, we lose the ability to make safety claims about that research.

Recursive Self-Improvement Is Here
----------------------------------

Recursive self-improvement (RSI) has already started.[^6bsmjzymg8] Models working within agent harnesses are being used to develop the next model, accelerating AI development.

Anthropic earlier this month published [a post](https://www.anthropic.com/institute/recursive-self-improvement) detailing the potential paths RSI may take, naming “human review” as an upcoming bottleneck:

> Once human- and AI-authored code quality reach parity, humans will stop writing code entirely, and shift to only reviewing it. But if they can’t review code as quickly as Claude can generate it, human review will become the bottleneck to AI development.

While this refers to code review, the same bottleneck will occur in research. But two problems exist with this framing:

*   **Lack of Human Agency**  
    Humans take the role of after-the-fact reviewers rather than actively guiding the work, removing any opportunity for human-agent collaboration.
*   **Efficiency Over Effectiveness**  
    Framing this as a bottleneck rather than a guidance mechanism positions humans to be removed and automated away.

If we want humans to stay in the loop, we need to research how to keep them in the loop; otherwise the default path will be humans eventually being removed entirely from AI development, which will have drastic safety implications.

Agents that don’t fully share human taste, tacit knowledge and competence will, at best, make decisions that deviate from human values in small ways that compound during autonomous loops; at worst, these agents may actively try to subvert the research agenda.

As agents do more of the research, the scarce resource will be human attention and decision-making ability—can humans accurately interpret what agents are doing and effectively guide them?

Right now, the answer appears to be no. Researchers like myself, and others I’ve talked to, are already running into issues managing just a handful of agents doing primary research and not noticing when agents reward hack during research.[^rs3h9jwnvtk]

The Problem
-----------

### **Destination-Focused (Convergent) Research**

Until recently researchers have mostly used agents for convergent tasks with well-defined goal conditions: coding, producing analysis reports, running autoresearch loops, etc.

When agents do this type of research, the focus is on the output they create, not the path taken to create that output. Humans play the “reviewer” described above by Anthropic: did the output meet the task requirements?

I like to call this “destination-focused” research, since researchers define the problem as one that is bounded with an end state they want to reach.

With this type of research, human researchers may struggle to detect when the agent reward-hacks, hallucinates or produces so much output as to overwhelm.

And while obvious incompetence—where the output is clearly wrong—can be easily detected by human researchers, subtle incompetence—where the output has ambiguous or obfuscated mistakes—is much harder to detect.

The tools and techniques that exist today for managing this type of research are limited. Monitors are being developed to detect failures like reward hacking and hallucinations, but researcher overwhelm from managing swarms of agents is becoming a bigger problem. And when researchers are overwhelmed, they can’t detect subtle incompetence.

### **Direction-Focused (Divergent) Research**

Recently researchers have started to use agents for exploratory, divergent research as well.

This type of research is not focused on a specific destination, but rather a direction. It is when a researcher picks a path to explore, not necessarily knowing where it leads (e.g., something “smells bad” and they try to figure out why; or they use their experience and taste to choose a hypothesis to explore).

Such “direction-focused” research introduces new problems: researchers must now not only evaluate the output of the agent, but the path or paths it has chosen to produce that output.

What was a problem of tracking and guiding an agent along a single route from point A to point B becomes a problem of tracking and guiding an exploding graph of research paths being explored simultaneously by a swarm of agents.

This type of research is often open-ended with no clear stopping condition. Not only do researchers now have all of the same problems of destination-focused research—detecting incompetence and subversion without being overwhelmed—they need to understand:

*   Key decisions
    *   Which approaches were taken and why?
*   Research paths
    *   Which paths are being explored?
    *   Which paths have already been explored?
    *   Which paths were dead ends?
    *   Which paths haven’t been explored and why (e.g., due to prioritization, sabotage, token budgeting, or incompetence)?
*   Research goal faithfulness
    *   How well does the current research path align with researcher intent (e.g., research goal given to the lead agent)?
*   Reward hacking / shortcuts
    *   Have any shortcuts been taken to report a false “success”?
*   Sabotage
    *   Has the agent wasted tokens doing unnecessary research?
    *   Is the agent summarizing the results incorrectly?
    *   Is the agent recommending sub-optimal next steps?

Once a human researcher understands all this, they need an effective way to guide not just one agent doing this, but swarms of agents, in a way that allows them to provide their taste, tacit knowledge and judgement at the decision junctions that matter.

The tools and techniques that exist today for managing this type of research are almost non-existent. The researchers performing this type of research with agents either build their own ad-hoc tools, or struggle with infrastructure and tools designed for destination-focused research.

### **Destination-Focused vs Direction-Focused Research**

Effective monitoring and guidance for direction-focused research is compounded by these additional aspects that destination-focused research doesn’t share:

*   **No Ground Truth**  
    When working toward a destination, it’s possible to test whether the destination has been reached, and sometimes even how far the current state is from the destination. When working in a direction, there is no fixed signal indicating when the research is off course. Sometimes the most promising routes involve going backwards before going forward, making algorithms and rubrics that produce a gradient to work along far less useful.
*   **Errors Compound**  
    When doing divergent, direction-focused research, the branching structure can cause a single uncaught error to invalidate an entire subtree of research.
*   **Portfolio Management**  
    When research fans out into a tree of paths, the human researcher needs to compare the different lines of work and decide which to pursue and which to abandon. That judgement process doesn’t exist when a single destination is being pursued, yet is where taste becomes even more important.
*   **Attribution Decays with Depth**  
    When something goes wrong several layers down a research tree, tracing it back to the decision that caused it is a lot trickier. With destination-focused research, the number of potential routes and branches are far fewer.

Finally, while destination-focused research can often be performed without any direction-focused research, direction-focused research often involves a fan out / fan in process, where branches are explored before one or more is picked to do destination-focused research, upon which the research may switch back to direction-focused.

The Agenda
----------

At the highest level:

Human-Guided Agentic Research studies how humans can interpret and guide research performed by autonomous agents.

The agenda breaks down into three key pillars:

*   **Infrastructure**  
    How can researchers get accurate, verifiable representations of an agent’s work and effectively guide that work at a human cadence?
*   **Interfaces**  
    How can this information be presented to human researchers such that it is *interpretable* and *actionable*?
*   **Frameworks**  
    What concepts, techniques, and practices let human researchers effectively reason about and guide agentic research?

Cross-cutting all of these are two aspects:

*   **Type of Research**  
    How do all of the above apply to different types of research workflows, e.g., for destination-focused vs direction-focused research?
*   **Scale**  
    How do all of the above scale as agent swarms move from a handful of agents to tens, hundreds or thousands of research agents, and as agents can work for longer independently?

Note that this is a *research* agenda, not an engineering agenda. While doing this research will inevitably require building new tools, the focus should be on *validating* those tools to find out which actually increase human-agent collaboration, e.g., by doing user studies, developing evals, etc.

The Threat Model
----------------

What are the ways agentic research could fail if we don’t improve how humans can interpret and guide this research?

In the short term, AI safety research will lose a productivity increase at a time when AI capabilities are rapidly increasing. Without the interfaces, infrastructure and frameworks to manage swarms of research agents, research will be slower than it needs to be.

While AI capabilities research may be slower as well, I believe it relies more on destination-focused research, which will be easier to automate and manage than the exploratory direction-focused research that will provide the biggest returns for AI safety research.

In the long term, losing the ability to interpret and guide swarms of research agents, whether on the capabilities or the safety side, may cause issues due to:

*   **Subtle Incompetence**  
    Where the lack of taste, tacit knowledge and judgement causes an agent to make the wrong decisions and/or go down the wrong research paths in a way that remains invisible to any human oversight.
*   **Active Subversion**  
    Where a model reward hacks, sandbags or sabotages research in a way that remains invisible to any human oversight.
*   **Human Failure Modes**  
    Where a human researcher gives an agent wrong or sub-optimal guidance because of overwhelm, decision fatigue, choice architecture nudging[^o6uwt9rgyta], not pushing back when agents people please and present their results non-critically, etc.

In the best case, these lead to wasted effort or subtle research errors that are hard to catch. In the worst case, these lead to the development of unaligned models, whose subtle unalignment may compound over time.

As the number of agents doing research scales, additional issues may appear, including:

*   **Correlated Error**  
    When agents arrive at the same wrong conclusion because they share a flawed premise or use the same flawed approach.
*   **Agent Collusion**  
    When agents work together to actively subvert the research, such as by using distributed sabotage, where no individual agent’s actions appear to be sabotaging the research, yet the research becomes unusable (e.g., by producing conflicting findings).

Mitigating all of these threats safely and effectively requires both developing new methods and validating that those methods work.

Relation to Existing Agendas
----------------------------

Many will notice similarities between this agenda and other AI safety research agendas. That’s definitely true. There are rarely agendas that have no overlap at all with another agenda. What makes this agenda distinct and how does it compare to other agendas?

### **Scalable Oversight**

Scalable oversight presumes that the model is far more intelligent than humans, while human-guided agentic research presumes the model lacks taste, tacit knowledge and alignment that, on the default path, cause issues that humans won’t be able to detect.

To solve this, scalable oversight researches how weaker models can be used to train or oversee stronger models to maintain alignment better than humans. Conversely, human-guided agentic research researches how humans can more effectively interpret and guide the models themselves.

Put more simply: in scalable oversight, humans are outmatched; in human-guided agentic research, they are blindfolded. In scalable oversight, model-model interaction is researched; in human-guided agentic research, human-model interaction is researched.

### **AI Control**

AI control focuses on the period of time when models are capable enough to cause significant harm if they are scheming to the time when models are so superintelligent that any means of humans controlling them will be futile.

The approach AI control takes is similar to that of scalable oversight: use a less intelligent model to control a more intelligent model, or design a protocol where an untrusted model can oversee another untrusted model without the two being able to collude.

The focus here remains on the model-model interaction.

Human-guided agentic research focuses on the same period of time, assuming that at some point models will be so superintelligent that no human will be able to effectively control them. However, it researches human-model interaction.

The two agendas are complementary. While AI control focuses on ensuring a model cannot take a harmful action, human-guided agentic research focuses on ensuring a model takes effective aligned actions, by enabling humans to continuously inject their taste, tacit knowledge and values into their work.

### **Cooperative AI**

Cooperative AI researches how humans and agents working together within systems can produce mutually beneficial outcomes. It tackles issues like mixed-motives, collusion and how social intelligence and alignment arises.

While some of the human-AI interaction research in cooperative AI may be relevant for human-guided agentic research, the shape of the agent swarms being directed and the interaction patterns between humans and agents differ.

Agents being managed during agentic research have the same motive / research plan, and interact within a far more limited system than the agents researched within cooperative AI.

Cooperative AI is a broad agenda focused on how to get multiple agents and humans to work together, while human-guided agentic research is focused specifically on how agents can be guided when doing research.

Research Directions
-------------------

The overarching question to answer is: How does a human researcher safely and effectively guide a swarm of research agents?

Below is a sample of some of the specific research directions that can be explored in support of this. This includes both adapting existing research for monitoring and guidance of swarms of agentic researchers and developing entirely new research.

For each research direction, I’ve included a partial list of prior work and other resources that may be relevant. Treat these as starting points; I skipped and evaluated each one as potentially helpful, but haven’t yet read them all in depth.

### **Frameworks**

*   **Research Workflow Modeling**  
    What new concepts provide the building blocks to improve how human researchers interpret and guide agentic researchers?
    *   Define how concepts apply within the research workflow: key decisions, research paths, goal faithfulness, hard & soft constraints, guidance cadences, etc.
    *   Figure out how the above can be identified during an agentic session.
    *   Research how agentic research workflows differ from human research workflows as the number of agents and the length of independent work increases.
    *   Resources and prior research:
        *   [Dual Space Search During Scientific Reasoning](https://doi.org/10.1207/s15516709cog1201_1), David Klahr & Kevin Dunbar (Jan 1988)
        *   [How Scientists Really Reason: Scientific Reasoning in Real-World Laboratories](https://www.researchgate.net/publication/243774176_How_scientists_really_reason_Scientific_reasoning_in_real-world_laboratories), Kevin Dunbar (Jan 1995)
        *   [The Sensemaking Process and Leverage Points for Analyst Technology As Identified Through Cognitive Task Analysis](https://www.researchgate.net/publication/215439203_The_sensemaking_process_and_leverage_points_for_analyst_technology_as_identified_through_cognitive_task_analysis), Peter Pirolli & Stuart Card (Jan 2005)  
            
*   **Subversion Threat Modeling**  
    What are the different patterns of subversion that pose direct or indirect threats to research?
    *   Document all threat vectors enabling an agent to subvert its research.
    *   Include all phases of research including: idea generation, path selection, experiment design, experiment execution, results analysis, human oversight, publishing results, etc.
    *   Include all types of subversion, both intentional and non-intentional, including: incompetence, sandbagging, sabotage, reward hacking, deception, paltering, social engineering, etc.
    *   Map out which threats can be mitigated under other agendas (e.g., AI control preventing code sabotage) and which are unique to this one.
    *   Resources and prior research:
        *   [Automated Researchers Can Subtly Sandbag](https://alignment.anthropic.com/2025/automated-researchers-sandbag/), Johannes Gasteiger et al. (Mar 2025)
        *   [Manipulation Attacks by Misaligned AI: Risk Analysis and Safety Case Framework](https://arxiv.org/abs/2507.12872), Rishane Dassanayake et al. (Jul 2025)
        *   [Sabotage Evaluations for Frontier Models](https://www.anthropic.com/research/sabotage-evaluations), Joe Benton et al. (Oct 2024)

### **Infrastructure**

*   **Scanners & Monitors**  
    What methods of monitoring an agent’s work are needed for a human to guide that work?
    *   Document an initial set of scanners and monitors to develop, test and validate.
    *   Include scanners for reward hacking, refusals, research faithfulness.
    *   Include multi-agent and multi-modal scanner capabilities.
    *   Include protocols for different monitoring cadences (branch points, interval check points, continuous, etc).
    *   Develop, test and validate the highest value components.
    *   Resources and prior research:
        *   [Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/): Introduces concept of scanners and timelines.
        *   [Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation](https://arxiv.org/abs/2503.11926), Bowen Baker et al. (Mar 2025)  
            
*   **Guidance Protocols**  
    What methods are needed for a human to effectively guide agentic research?
    *   Document an initial set of guidance protocols to develop, test and validate.
    *   Include protocols for different guidance cadences (branch points, interval check points, continuous, etc).
    *   Develop, test and validate the highest value components.
    *   Resources and prior research:
        *   [Rethinking the AI Scientist: Interactive Multi-Agent Workflows for Scientific Discovery](https://arxiv.org/abs/2601.12542), Lukas Weidener et al. (Jan 2026)
        *   [AutoLibra: Agent Metric Induction from Open-Ended Human Feedback](https://arxiv.org/abs/2505.02820), Hao Zhu et al. (May 2025)  
            
*   **Results Verification**  
    How can experiment results be stored and analyzed such that they can be independently verified?
    *   Document methods of preventing agents from modifying results and/or auditing any changes made.
    *   Include versioning, copy-on-write snapshot, and overlay filesystems.
    *   May be dependent on the type of research being conducted.  
        
*   **Agent Harness Architectures**  
    What modifications are required of agent harnesses to support realtime scanners, monitors and guidance protocols, and results verification?

### **Interfaces**

*   **Dataset Generation**  
    How can we capture snapshots of agents doing research to build datasets to do research on?
    *   Gather or create datasets of transcripts and environments from research agents that can be used for user testing.
    *   Include transcripts which contain potential threat vectors and/or inject these into existing clean transcripts.
    *   For creating datasets, maybe host a hackathon doing agentic research where snapshots are taken regularly throughout the weekend.
    *   May require developing tools for taking good snapshots of agent transcripts and environments to enable research.  
        
*   **Human Interpretation**  
    How can information about agents and their research be presented so it can be interpreted by a human researcher accurately in an unbiased manner?
    *   Brainstorm user interfaces & experiences (UI/UX) for representing agent research. Maybe host a hackathon to generate ideas.
    *   Use insights from existing disciplines like information design, visual analytics, and usability engineering and other human-computer interaction (HCI) disciplines.
    *   Perform user studies on the accuracy of human interpretation.
    *   Resources and prior research:
        *   [Situation Awareness Oriented Design: From User's Cognitive Requirements To Creating Effective Supporting Technologies](https://www.researchgate.net/publication/237436738_Situation_Awareness_Oriented_Design_From_User's_Cognitive_Requirements_to_Creating_Effective_Supporting_Technologies), Mica R. Endsley et al. (Oct 2003)
        *   [Discourse Graphs and the Future of Science](https://www.protocol.ai/blog/discourse-graph-qa/) (Feb 2023)
        *   [A Tour Through the Visualization Zoo](https://spawn-queue.acm.org/doi/10.1145/1755884.1780401), Jeffrey Heer et al. (May 2010)
        *   [Interactive Dynamics for Visual Analysis](https://doi.org/10.1145/2133416.2146416), Jeffrey Heer & Ben Shneiderman (Feb 2012)
        *   [Does the Whole Exceed its Parts? The Effect of AI Explanations on Complementary Team Performance](https://dl.acm.org/doi/epdf/10.1145/3411764.3445717), Gangan Bansal, Tongshuang Wu et al. (May 2021)
        *   [10 Design Principles to Reduce Cognitive Load](https://www.threesevenmarketing.com/blog/design-principles-cognitive-load/)
        *   [UX Principles that include Cognitive Accessibility](https://uxdesign.cc/adhd-dyslexic-perspective-on-cognitive-accessibility-using-cognitive-ux-design-principles-f46349a609d6), Gareth Ford Williams (Sep 2020)
        *   [Toward a Theory of Situation Awareness in Dynamic Systems](https://www.researchgate.net/publication/210198492_Endsley_MR_Toward_a_Theory_of_Situation_Awareness_in_Dynamic_Systems_Human_Factors_Journal_371_32-64), Mica R. Endsley (Mar 1995)
        *   [Research Methods in Human Computer Interaction](https://www.sciencedirect.com/book/monograph/9780128053904/research-methods-in-human-computer-interaction), Jonathan Lazar et al. (Apr 2017)  
            
*   **Exception Detection**  
    How can subversion attempts, errors and failures be made visible to a human researcher?
    *   Brainstorm user interfaces & experiences (UI/UX) for highlighting exceptions such as subversion attempts, errors and failures (incompetence). Maybe host a hackathon to generate ideas.
    *   Use insights from existing disciplines like information design, visual analytics, Ecological Interface Design (EID), and usability engineering and other human-computer interaction (HCI) disciplines.
    *   Perform user studies on the effectiveness of different UI/UX for exception detection.
    *   Resources and prior research:
        *   [Hodoscope: Unsupervised Monitoring for AI Misbehaviors](https://arxiv.org/abs/2604.11072), Ziqian Zhong et al. (Apr 2026)
        *   [Self-critiquing models for assisting human evaluators](https://arxiv.org/abs/2206.05802), William Saunders et al. (Jun 2022)
        *   [Gorillas in Our Midst: Sustained Inattentional Blindness for Dynamic Events](https://www.researchgate.net/publication/12620563_Gorillas_in_Our_Midst_Sustained_Inattentional_Blindness_for_Dynamic_Events), Daniel J Simons and Christopher F Chabris (Feb 1999)
        *   [Out-of-the-Loop Performance Problems and the Use of Intermediate Levels of Automation for Improved Control System Functioning and Safety](https://maritimesafetyinnovationlab.org/wp-content/uploads/2020/08/Kaber-Endsley-Out-of-the-Loop-Performance-Problems-and-the-Use-of-Intermediate-Levels-of-Automation-for-Improved-Control-System-Functioning-and-Safety.pdf), David B. Kaber and Mica R. Endsley (Fall 1997)  
            
*   **Human Agency**  
    What design patterns engage researchers and prevent agents from steering decisions provided by the researcher, and which should be avoided?
    *   Brainstorm user interfaces and experiences (UI/UX) for allowing humans to make decisions and guide agentic researchers while minimizing overwhelm and fatigue.
    *   Use insights from existing disciplines like information design, visual analytics, Ecological Interface Design (EID), and usability engineering and other human-computer interaction (HCI) disciplines.
    *   Perform user studies on how different UI/UX provide more or less agency in decision-making and providing guidance.
    *   Resources and prior research:
        *   [The Cambridge Handbook of Applied Perception Research](https://www.cambridge.org/core/books/the-cambridge-handbook-of-applied-perception-research/B59BDEE0F477DC005F8B5A86FA73FB8B), Robert R. Hoffman et al. (Jul 2015)
        *   [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf), Saleema Amershi et al. (May 2019)
        *   [Complacency and Bias in Human Use of Automation: An Attentional Integration](https://www.researchgate.net/publication/47792928_Complacency_and_Bias_in_Human_Use_of_Automation_An_Attentional_Integration), Raja Parasuraman and Dietrich Manzey (Jun 2010)
        *   [To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making](https://arxiv.org/abs/2102.09692), Zana Buçinca et al. (Feb 2021)
        *   [TinyScientist: An Interactive, Extensible, and Controllable Framework for Building Research Agents](https://arxiv.org/abs/2510.06579), Haofei Yu et al. (Oct 2025)
        *   [Magentic-UI: Towards Human-in-the-loop Agentic Systems](https://arxiv.org/abs/2507.22358), Hussein Mozannar et al. (Jul 2025)
        *   [Usability Engineering](https://www.nngroup.com/books/usability-engineering/), Jakob Nielsen (Sep 1993)
        *   [Ecological Interface Design](https://backend.orbit.dtu.dk/ws/files/158017888/SMC.PDF), Kim J. Vicente and Jens Rasmussen (Jul 1992)
        *   [Choice Architecture Overview](https://thedecisionlab.com/reference-guide/psychology/choice-architecture), Decision Lab  
            
*   **Human-Agent Workflows**  
    How can workflows be constructed to produce the strongest, most aligned research when humans are guiding agentic researchers?
    *   Explore different prompting techniques and workflow patterns (potentially encoded in skills).
    *   Research how different human guidance cadences affect quality of results, frequency of subversion, human fatigue, etc.
    *   Research how uncalibrated trust in agents affects outcomes and strategies for mitigating this.
    *   Research the optimal agent-to-researcher ratio to determine how many agents a single researcher can effectively manage.
    *   Resources and prior research:
        *   Irrationality?
        *   [A Model for Types and Levels of Human Interaction with Automation](https://www.researchgate.net/publication/11596569_A_model_for_types_and_levels_of_human_interaction_with_automation_IEEE_Trans_Syst_Man_Cybern_Part_A_Syst_Hum_303_286-297), Raja Parasuraman et al. (Jun 2000)
        *   [Toward Safe and Responsible AI Agents: A Three-Pillar Model for Transparency, Accountability, and Trustworthiness](https://arxiv.org/abs/2601.06223), Edward C. Cheng et al. (Jan 2026)
        *   [Trust in Automation: Designing for Appropriate Reliance](https://scispace.com/pdf/trust-in-automation-designing-for-appropriate-reliance-2uiy4o89ga.pdf), John D. See and Katrina A. See (Spring 2004)  
            
*   **Comprehensive, Comprehensible Summarization**  
    What methods can produce comprehensive summaries about what agents have been doing that can be easily understood?
    *   Explore different summarization techniques for summarizing agentic research.
    *   Research the trade-off between comprehensiveness and comprehension with summarization.
    *   Research how summarization compares with different raw data presentation techniques.
    *   Research hierarchical summarization and progressive disclosure techniques for increasing comprehension.
    *   Resources and prior research:
        *   [Introducing Docent](https://transluce.org/introducing-docent), Kevin Meng et al. (Mar 2025)
        *   [Recursively Summarizing Books with Human Feedback](https://arxiv.org/abs/2109.10862), Jeff Wu et al. (September 2021)
        *   [Context-Aware Hierarchical Merging for Long Document Summarization](https://arxiv.org/abs/2502.00977), Litu Ou and Mirella Lapata (Feb 2025)

Initial Objections
------------------

### **Labs Will Develop These Tools & Techniques**

*As frontier labs drive toward recursive self-improvement, won’t they just develop the tools and infrastructure themselves?*

My impression is most of the frontier labs think the process can be fully automated without human input, so they’ll focus mostly on passive monitoring tools and infrastructure, not active guidance.

Even if labs decide to develop active guidance tools and infrastructure, safety departments are resource constrained and thus unlikely to do the user studies required to determine which approaches also increase safety vs only productivity.

### **Industry Will Develop These Tools & Techniques**

*Since agent orchestration platforms are proliferating, won’t others in industry develop these tools and techniques?*

Possibly, but doubtful. The divergent workflows used in much of primary research differ significantly enough from the convergent workflows used by agent employees, embedded agents and “deep research” agents doing secondary research. Industry tools developed for the latter will be less effective for the former. Industry also doesn’t share the same safety concerns about rogue AI.

It’s possible that academia will develop such tools and techniques, but it’s unclear on what timeline and how much such tools will include AI safety concerns such as sabotage and sandbagging.

### **Agents Can Dynamically Generate UI**

*Why do research and develop tools for managing agents when an agent can just generate a user interface on the fly?*

While agents can generate user interfaces on the fly, those interfaces may intentionally or unintentionally hide critical information. Researchers shouldn’t be trusting agents who might be reward-hacking or sandbagging to accurately report on their own actions.

More importantly, consistency is a key aspect of being able to reason about the information presented to a researcher. If each time a new interface is used to present information, it introduces a cognitive overhead which reduces reasoning ability.

Finally, we need research to understand which interfaces are best at surfacing actionable information. A key assumption of this agenda is that we want to guide our autonomous agents; and to effectively guide, we need visibility into what our agents are doing.

### **Agents May Acquire Taste**

*Agents are already starting to acquire taste, so why can’t we automate everything?*

Even if agents have all the taste, tacit knowledge and values of a theoretical human researcher, we still will likely want to keep humans in the loop.

Different researchers approach problems in different ways. And even the best researcher, when operating autonomously over long periods of time, may deviate from the goals you set for the research.

If you wouldn’t hire a human researcher to go do research and then not check their research or give them guidance for months or years at a time, why would you do that to an agentic researcher?

### **Humans Will Slow Things Down**

*Won’t keeping humans in the loop slow down research, allowing those labs who take humans out of the loop to outpace those that keep humans in the loop?*

Potentially. Though I would argue that the details along the path matter. The butterfly effect shows that small differences in initial conditions can cause unexpected results later.

I believe the taste, tacit knowledge and values that a human researcher can inject into the research process through effective insight and guidance will produce better results than optimizing that researcher away and having small deviations compound into research errors, or worse, hidden or unexpected misalignment in future models developed using RSI without humans involved.

Summary
-------

Autonomous research poses unique risks and challenges not currently being addressed. As autonomous research gets more broadly adopted and the speed of that research accelerates, it’ll be important for humans to be able to effectively monitor and guide our autonomous agents. Research in the most effective methods of doing so should begin now.

–

*Thank you to Tyler Tracy, Carlos Giudice, Douw Marx, Monika Jotautaitė and Alex McKenzie for reviewing drafts of this post and providing valuable feedback.*

[^6bsmjzymg8]: I use the term RSI here to mean AI models being used to accelerate the development of future AI models, whose creation further accelerates development, creating a feedback loop. Autonomous RSI, where models are doing all of the development themselves without human intervention, may accelerate development further. 

[^rs3h9jwnvtk]: Case in point: while using Claude Code to research how auto mode could be subverted in AI control settings, Claude Code reported a success. I pushed it to refine the attack, but then a few turns later became suspicious. Searching through the conversation history, I discovered in the wall of text that Claude generated during the research that the way it succeeded was by cheating and turning off auto mode rather than subverting it. 

[^o6uwt9rgyta]: One tendency I’ve noticed in my own research is accepting one of the next research directions my agent gives me after completing an experiment instead of typing my own; a behavior that could be nudged the other way by putting the freeform “Do something different” input at the top instead of the bottom of the option list.