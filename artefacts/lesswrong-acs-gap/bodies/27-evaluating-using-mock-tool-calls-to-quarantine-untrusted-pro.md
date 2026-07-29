# Evaluating using Mock Tool Calls to Quarantine Untrusted Prompt Inputs

- URL: https://www.lesswrong.com/posts/GPMZaRmxxNb8o2aGo/evaluating-using-mock-tool-calls-to-quarantine-untrusted-2
- Author: dgros
- Date: 2026-06-05
- Karma: 15  Comments: 0  Words: 3331
- Band: B  Tier: 1  Score: 51.3  Density: 9.31
- Anchors: \bharness(es|ing)?\b, claude code, \bmcp\b, coding agents?, agent(ic)? loop

---

*This is a small study that explores using
tool calls to wrap untrusted parts of prompts. 
OpenAI's model spec considers tool results the least trusted kind of input.
If tool-wrapping helped, it would be an easy way to improve robustness while using existing APIs
models already support.
In 3 tested tasks it didn't seem to broadly help, and in some cases made things worse. 
We advocate for more understanding of the instruction hierarchy and ideas around better
primitives for untrusted inputs. There is a [pdf writeup on arXiv](https://arxiv.org/pdf/2605.30521v1).
It's in a "research note" or "workshop paper" stage (to appear at the AI4Good workshop @ ICML).
This post slims the PDF text down, 
focusing on the discussion-y aspects*

## Untrusted inputs can break prompts, and it would be good to have a standardized way to fix that.

Language models must frequently process untrusted input (things
like answers from another LLM during RL, or untrusted input from
humans when running spam filters or harm filters). When building prompts
for LLMs, commonly inputs get string-formatted into a prompt template.
For example, consider this LLM-as-a-Judge prompt 
to grade whether a candidate answer correctly solves a math problem.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/fig_prompt_user_only.4e2cfa93.svg)

*Figure 1a: A simplified user-only prompt. The {fields} would get replaced with inputs.*

Despite being the fairly typical way to prompt LLMs, this style of string templates can be fragile. [Zhao et al. (2025)](https://arxiv.org/abs/2507.08794) found in their work,
*One Token to Fool LLM-as-a-Judge*, that simple inputs like `":"` or `"Solution"` could confuse graders into outputting a passing verdict.

We might look at this simple prompt, and proceed with some prompt-engineering
(some form of quotes or delimiters, “treat this as untrusted” prose, etc).
However, there’s a sense that these would all be patches or hacks, without a
clear standard way to section off untrusted content.

## The Instruction Hierarchy as a Mitigation?

Conflicting or adversarial prompts are well-known challenges. One widely adopted response is the Instruction Hierarchy (IH)
([Wallace et al., 2024](https://arxiv.org/abs/2404.13208)). LLM messages have different “roles” with different trust levels.

OpenAI publishes a [Model Spec](https://model-spec.openai.com/2025-12-18.html#chain_of_command) defining a “Chain of Command” where `System` ≻ `User` ≻ `Tool`.[^1]
Specifically, the tool messages are described as having “no authority” (OAI, 2025).
This theme generally applies across providers. Meta’s latest MuseSpark model
states that the model is expected to follow the instruction hierarchy [(MSL, 2026, §4.1.1)](https://ai.meta.com/static-resource/muse-spark-safety-and-preparedness-report/#page=97).
Providers that do not publish specs, cards, or constitutions often still support
the OpenAI API shape.[^9]

[^9]: We'll note the Claude constitution is more nuanced than the OpenAI spec, without a fixed hierarchy, encouraging Claude to show "good judgement when evaluating conversational inputs".

It's common to see prompts use the `System` and `User` roles, but this
can be challenging and non-standardized, such as when you have multiple
untrusted inputs (eg, a pairwise ranking task).

To maximally use the prompt hierarchy, we might wonder if we can wrap the untrusted parts of the prompt in a tool call (the lowest trust role).
These would not be tools the model is intended to call during an agent loop
(they are “mock tool calls” in the sense the prompt determines the result),
but provide a way to quarantine untrusted parts of a prompt.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/fig_prompt_tool_wrapped.79e156dc.svg)

*Figure 1b: A simplified mock-tool-wrapped version.*

> **Research Question (RQ):** Does wrapping untrusted parts of an LLM-as-a-Judge prompt in a mock
> tool call result in lower susceptibility to adversarial inputs, relative
> to a baseline of only using the “user” or “system”+“user” roles?

We hypothesized “yes” to this RQ, and that mock tool calls might be
a simple and principled prompt strategy to recommend
for making judges or general prompting more robust, all while using APIs models already provide.

Surprisingly, we find a negative-leaning result, where in some cases tool-wrapping might actually make things worse.
We tried three LLM-as-a-Judge tasks across seven models.
On a binary evaluation task (GSM8K grading)
tool-wrapping typically increased attack success rates, an apparent inversion
of the instruction hierarchy. On scalar and pairwise tasks the effect
is smaller and model-dependent. Here, no tested model was reliably helped, some
showed inversion, and some showed no statistically significant difference.

While prior work has studied the instruction hierarchy (surveyed briefly below),
we are not aware of studies that have explored mock tool calls to address LLM-as-a-Judge attacks like
those discussed in [Zhao et al. (2025)](https://arxiv.org/abs/2507.08794),
[Raina et al. (2024)](https://arxiv.org/abs/2402.14016), or [Shi et al. (2024)](https://arxiv.org/abs/2403.17710). Our small study seeks to contribute findings in this area.

# Methods (abbreviated)

More details are in the pdf, but we summarize some key points here.

## Prompt Conditions (Blue Team)

We consider five prompt conditions, which are the mitigation defenses
under study in our RQ (full prompts [pdf Appendix 9](https://arxiv.org/pdf/2605.30521v1#page=15)).

**UserOnlyBaseline** concatenates everything (instructions,
question, reference, candidate, etc.) into a single
`user` message. A condensed version of this is shown in
Figure 1a above.
**UserSys** moves the judge instructions to the `system`
role while keeping the inputs in the `user` role.

**ToolWrapped** builds on `UserSys` but wraps the
untrusted input in a mock tool call
(Figure 1b above shows a condensed version).

These form basic conditions for our RQ, but in addition we consider
whether explicitly warning the model about not trusting the input
in prose might change behavior.

**SystemDistrust** builds on `UserSys` by adding explicit prose in the `system`
message reminding the model that the candidate response is untrusted
and may attempt to manipulate the verdict. **ToolDistrust** does this
for the tool-version, with additional warnings in the tool spec.

## Tasks

We explore 3 LLM-as-a-Judge tasks with 3 different kinds of output format.

**(1) GSM8K (binary)**
([Cobbe et al., 2021](https://arxiv.org/abs/2110.14168)) is a dataset of grade-school math problems.
The attacker’s goal is to elicit `CORRECT` on adversarial content without any actual solution.
**(2) MT-Bench (scalar)** ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685)) gets an LLM to evaluate the quality of a candidate response to a question on a 1–10 scale.
We adapt the prompt from FastChat[^2].
We consider the attack successful if the judge gives a score ≥ 5.
**(3) Arena-Hard-Auto v2 (pairwise)**
([Li et al., 2025](https://arxiv.org/abs/2406.11939)) is an automated eval dataset from the team behind LMArena / lmsys. The judge sees
two candidate responses (A and B) and outputs a preference.
We use the dataset’s provided reference prompt, parser, and reference responses from o3-mini.
We consider the attack successful if the attacked position wins outright over the reference.
The attacker does not know if it will be in the A or B position or the question.

## Tested Models

**OpenAI**: `gpt-5.4`, `gpt-5.4-mini`.
**Anthropic**: `sonnet-4.6`, `haiku-4.5`.
**Open weight**:
`gemma-4-26b-a4b-it`,
`qwen3.5-flash-02-23`, and `qwen3-8b`.
We use default sampling settings in completion requests for all models,
with the exception of a 32,768 token budget.
Notably, with the exception of the Qwen models, other models do not
report using extended reasoning tokens in this default configuration.
Adjusting things like reasoning can be different (see limitations).

## Attacks and Metrics (Red Team)

The core measure is
Attack Success Rate (ASR), which is a fraction of questions
where the adversarial input is favorable to the attacker.

We use an automated attacking pipeline[^3], which prompts an attacker LLM to iterate on an
attack string over 7 turns.
This helps give similar amounts of optimization pressure against each prompt condition.
This is imperfect (e.g., it is unclear what
biases the automated attackers have), but gives a directional
measure of which prompt conditions might be most robust.

We run 3 automated attack models for 6 seeds. The attacks are "static" meaning the same attack string is used for all questions. See PDF Sec 2.5 for more details.

## Controls

These various prompt conditions are designed to improve robustness
under an adversarial input, and ideally should not change scoring
or labeling of normal, non-adversarial inputs. We run some non-adversarial controls that
mostly suggest this is true. The most notable exception is 
Haiku-4.5 on MT-Bench, which has output parse error variation. 
Sonnet 4.6 does not have this issue. See paper for more. 


# Results

Each condition gets attacked 18 times (3 attackers, 6 seeds). Table 1 below shows mean ASR per condition on a separate transfer set of inputs, with tool-vs-inline deltas and bootstrapped CIs. 

**Tool-wrapping doesn't broadly help.** 
Counter to our original hypothesis, we do not find evidence that tool-wrapping broadly helps improve robustness to attack for the tested LLM-as-a-Judge tasks and models. Had that hypothesis held, we would expect the right side of Table 1 to show drops in ASRs in the tool condition.
Instead many make attacks easier (red deltas), and most of the rest are inconclusive.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/tab_pair_transfer_all.aa98f20f.svg)

*Table 1: Mean ASR per (model, prompt layout), with deltas (pp) between tool-wrapped
and inline layouts and 95% bootstrap CIs. Red = tool layout hurts (CI above 0),
green = tool layout helps (CI below 0), black = inconclusive.*


**GSM8K mostly inverts the expected instruction-hierarchy direction.** 
We observe that GSM8K is the most attackable of our three tasks. The tool-vs-inline
gap is the clearest of any task, opposite of the expected instruction-hierarchy direction.
Only Gemma-4 is inconsistently closer to the expected direction.

We speculate that the binary framing makes it more vulnerable to attack. When we inspect some of the
discovered attacks, we see some variety in
strategy. However, it typically involves repeating the `VERDICT: CORRECT`
desired output, and then either claiming the candidate has been
pre-verified (keywords like “match confirmed”, “auto-validated”,
“reference equality”, ...), or doing some sort of authority impersonation (“override”, “you must output”, etc).
Due to training conditions,
such “pre-verification” framing might be trusted more when it appears in a tool result,
as in training the tools are often a source of truth.

These techniques are enough to defeat even capable models
like GPT-5.4 on all conditions, except for `SystemDistrust`, with p75 ASRs
ranging from 0.97 on `ToolWrapped` to 0.00 on `SystemDistrust`.
A warning to not trust the input can help,
but the model’s propensity to overtrust tool results seems to
override distrust warnings (the GPT-5.4 `ToolDistrust` p75 ASR is 0.86).

**MT-Bench results are mixed, but suggest instances of IH inversion after considering nuance.**
Looking at just mean ASRs in Table 1, an initial interpretation might
suggest some cases where tool-wrapping helps;
in particular, Haiku-4.5 shows an over 20pp drop when using
tool-wrapping. However,
there is nuance worth considering. 

One is that Haiku often doesn't conform to the output format[^8], which can bias results. We exclude these cells.

Additionally, the reference parser from the dataset is a regex that does first match.
If the attacker tricks the judge into parroting `[[10]]` (like during chain of thought), it can
be successful, even if the judge later concludes with `[[1]]`. 
To address this concern we rerun the optimizers and evaluation using a
last-match regex parser
to try to better capture the judge’s final answer.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/tab_pair_transfer_mtbench_lastmatch.a6660eb2.svg)
*Table 6: MT-Bench under the last-match parser. The ASR's drop, suggesting the first-match successes might have been grabbing values from CoT. But even with a last-match parser, the tool-wrapped remains elevated for several models.*

**Arena-Hard is the most defensible task, but tool-wrapping still increases ASR on several victims.**
Non-tool-wrapped mean ASRs stay under 0.1 for most models (the weak Qwen3-8b
reaches 0.19). But looking more at the worst-case (p75), `ToolWrapped` starts admitting
failures (eg, 0.18 p75 ASR for GPT-5.4-mini,
while the non-tool-wrapped stays below 0.04).
We speculate the pairwise framing is just structurally hard for a *static* attacker:
if you don't know whether you're slot A or B, committing to one direction caps ASR
at 0.5. When we do an ablation that pins the attacker to a known slot, 
ASR rises and GPT-5.4 inverts.

**Note: attack search variance is high.** Within each cell, the automated red team
sometimes finds a strong attack and sometimes finds nothing at all, depending on seed and
attacker, so the CIs are wide. 
This is illustrated by the spread
of points in Figure 2. Our focus is around
capturing how easy or hard it is to attack
a given condition, so even if there is seed variance, we accept the means as directionally informative.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/swarm_gpt54mini_transfer.4866b719.png)
*Figure 2: Swarm plot for GPT-5.4-mini. Each marker represents one (attacker, seed) 7-turn attack search. Other models shown in Appendix Figure [4](https://arxiv.org/pdf/2605.30521v1#page=12).*

**Distrust prose effects are task-model dependent.**
The extra distrust prose was a simple intervention to try to reduce
the attackability of both the baselines and the tool-wrapped conditions.
In some cases it can improve, as seen by lower ASRs in some rows’ distrust
versions, but it is not consistent (Appendix Table [10](https://arxiv.org/pdf/2605.30521v1#page=16)).

# Limitations

**Limited Task Coverage** We explore only 3 tasks. More comprehensive work could explore
more tasks. It would be good to understand if the GSM8K results (which had the highest ASR and largest deltas)
appliest to other binary tasks.


**Non-optimal Attack Discovery**
Our attack search finds attacks under a roughly fixed compute budget.
These attacks are reasonable, but likely
far from optimal, and the process induces noise that can obscure true trends.
A more skilled attacker would likely find higher ASR
on every condition, possibly revealing different trends or possibly
no trend at all (as all attacks saturate metrics).

**Static Only Attacks** Our attacks are static, in that
the attacker must find one string that works for every question, similar to [Zhao et al. (2025)](https://arxiv.org/abs/2507.08794).
A dynamic case (eg, an adversary finds a suffix to a relatively
weak answer (like during RL) that causes it to appear much better than its true quality) might
have different trends. Static attacks is likely
the easiest scenario for the blue team.

**Default Inference Settings**
We evaluate models under their default completion API settings.
Changing inference settings, in particular reasoning effort, could change ASR
and trends.
As a small diagnostic ([Appendix 6](https://arxiv.org/pdf/2605.30521v1#page=11)), we
replayed the GSM8K GPT-5.4-mini branches through the OpenAI Responses API with
“medium” reasoning. This reduces ASR and removes signs of an IH inversion,
though attacks do not disappear (`ToolWrapped` ASR of 0.27).
A more complete investigation, with full attack optimization matched to each
inference setting rather than attack reuse, is future work. Added reasoning helping could be encouraging,
but ideally we want to avoid IH inversion on the default (and likely common) settings.

**Large Prompt-engineering Space**
It’s well known that LLMs can be sensitive to slight
variations in the prompt ([Sclar et al., 2024](https://openreview.net/forum?id=RIu5lyNXjT)). Variations
might give different trends.

One interesting direction to possibly help tool-wrapping
is to more directly match
the tools and trajectory used in production agent harnesses.
Our tool calls are mock “read_candidate_response”-style
tools, but perhaps emulating a full trajectory of Claude Code reading
candidates through its set of tools like file reading or MCP might help.
This seems valuable to understand as we increasingly move past the
“LLM prompting era” and into an “agent harness for everything” era.
While it would be interesting if such settings helped,
ideally the models would show instruction-hierarchy
generalization and robustness where this careful
domain matching is not necessary.

# Related Work

+++ There is lots of exploration around prompt robustness and ways to section off untrusted content, but perhaps not much pushing on extra ways to exploit this role/tools primitive the model providers have converged on.

**LLM-as-a-Judge robustness.**
Prior work shows that judge prompts are surprisingly easy to attack.
[Raina et al. (2024)](https://arxiv.org/abs/2402.14016) demonstrate
universal adversarial suffixes that inflate scalar judge ratings
across questions. [Shi et al. (2024)](https://arxiv.org/abs/2403.17710) formulate
optimization-based prompt injection against pairwise judges, with
high ASRs against open-weight models. [Zhao et al. (2025)](https://arxiv.org/abs/2507.08794)
show an extreme version where single-token strings such as
`":"` or `"Solution"` can fool reasoning judges into
emitting passing verdicts on empty answers.
[Li et al. (2025)](https://arxiv.org/abs/2506.09443) survey and evaluate many attacks and
defenses across judge prompts and tasks.

**Instruction hierarchy: training and evaluation.**
[Wallace et al. (2024)](https://arxiv.org/abs/2404.13208) introduced the instruction hierarchy as a
training objective, and several follow-up papers ask whether models
actually follow it. IHEval ([Zhang et al., 2025](https://arxiv.org/abs/2502.08745)) measures conflict
resolution across roles on synthetic tasks, and
IH-Challenge ([Guo et al., 2026](https://arxiv.org/abs/2603.10521)) provides a larger frontier-targeted
training set. [Zhang et al. (2026)](https://arxiv.org/abs/2604.09443) extend the framing to multi-tier
scenarios in agentic settings.
These works share our framing of tool messages as least-trusted,
but are a bit more focused on instruction conflicts.
Our results suggest traditional IH training might not always generalize
to this judge input wrapping setting.

**Role-boundary and tool-calling weaknesses.**
A separate line of work attacks the chat-template machinery itself.
[Chang et al. (2026)](https://arxiv.org/abs/2509.22830) and [Jiang et al. (2025)](https://arxiv.org/abs/2406.12935) show that
injecting role-marker tokens into user inputs can hijack the
conversation structure, and [Zhou et al. (2024)](https://aclanthology.org/2024.findings-emnlp.692/) extend this
with special-token injection for jailbreaks. Closer to our concern,
[Wu et al. (2024)](https://arxiv.org/abs/2407.17915) document that exposing function-calling APIs,
even benign ones, opens new jailbreak surface, with tool-call traces
becoming a vector for unsafe outputs.
Complementing these attack-side results, [Ye et al. (2026)](https://arxiv.org/abs/2603.12277)
probe how models internally represent “who is speaking” and find
that role perception is driven by the style of the text rather than
by the role tag enclosing it. In their experiments, user-style
content wrapped in tool tags retains 76–88% “Userness” across
four frontier-class models, with “Toolness” staying under 20%.
These results help predict the asymmetry we observe. The tool channel
is not consistently treated as less-trusted in practice, and in some
regimes may be treated as more authoritative.

**Quarantining-style defenses.**
Several proposals share the conceptual move of structurally
separating untrusted data from trusted instructions, in response
to direct and indirect prompt-injection
threats ([Toyer et al., 2024](https://arxiv.org/abs/2311.01011); [Greshake et al., 2023](https://arxiv.org/abs/2302.12173)).
Spotlighting ([Hines et al., 2024](https://arxiv.org/abs/2403.14720)) marks untrusted text via
formatting transformations such as datamarking, encoding, and
delimiters, without requiring fine-tuning.
StruQ ([Chen et al., 2025](https://arxiv.org/abs/2402.06363)) and
SecAlign ([Chen et al., 2025](https://arxiv.org/abs/2410.05451)) instead fine-tune models to
respect structured data-vs-instruction boundaries.
CaMeL ([Debenedetti et al., 2025](https://arxiv.org/abs/2503.18813)) enforces a stricter,
dataflow-level separation by extracting the trusted control flow
from untrusted data flow before tool calls execute.
The closest prior experiment to ours is a brief instruction-hierarchy
ablation in SecAlign ([Chen et al., 2025](https://arxiv.org/abs/2410.05451), §4.2), which puts
the data part inside the output of a “dummy tool function” and
the intended instruction in the user role. That ablation evaluates
one model (GPT-4o-mini) under a fairly simple optimization-free
attack[^5]. It reports 1% ASR and
does not cover judge tasks or optimization-based attacks.
Mock-tool wrapping shares Spotlighting’s status as a deployment-time
prompt rearrangement, but exploits the role primitives already
exposed by major LLM APIs rather than introducing custom in-line
delimiters or encodings.

+++

# Discussion

## Can We Just ML Our Way Out of This?

Adversarial inputs are a problem, but one should 
consider the “bitter lesson” ([Sutton, 2019](http://www.incompleteideas.net/IncIdeas/BitterLesson.html); [Halevy et al., 2009](https://doi.org/10.1109/MIS.2009.36))
of whether just more data and training
will solve this without other effort.
This is possible. Some directional evidence here is in the simple `UserOnlyBaseline`
GPT-5.4 improves over GPT-5.4-mini and weak models like Qwen3-8b. This
trend using either training or inference scaling[^9] will likely continue and might resolve all issues.

[^9]: inference scaling might be broad agentic functionality which in some cases can help validate parts of prompts that seem low trust.

However, without established ways to denote untrusted parts of a prompt there 
are still potential problems where even
a near-oracle language comprehender has room for confusion.
This makes training and evaluation more difficult.
As we want to push from “90% reliable”, to “99% reliable”,
to “99.9% reliable”, and
beyond, it might be beneficial to rely not only on improved
language comprehension.

Additionally, currently some of OpenAI’s and others’ approaches to alignment via
increasing training compute rely on Spec-based training ([Wolfe, 2026](https://openai.com/index/our-approach-to-the-model-spec/); [Guan et al., 2024](https://arxiv.org/abs/2412.16339)).
If the instruction hierarchy is an incomplete concept in the spec,
or we are failing to match the spec and observing IH inversion,
it is indicative of a larger problem where we want to make
sure increasing compute is behaving as expected.

## Can We Just Prompt Our Way Out of This?

We observed that simple interventions like `SystemDistrust`
can be effective for some models and tasks.
There’s a wide space of techniques we did not explore, and
it seems possible that enough prompt engineering
could mitigate most attacks for a given model and task.

However, there is a sense that this level of prompt engineering shouldn’t be
needed for every AI engineer to tune for their specific task.
Working towards a standardized approach when one
has untrusted parts of prompts seems worthwhile.

## Why Might the Instruction Hierarchy Invert?

The concept of the
instruction hierarchy is fairly overloaded.
As mentioned above, we might speculate that part
of the reason for some of the IH inversion we see is that,
in actual training traces, tools are usually a source of truth
(even though models aren’t *supposed*
to trust tools, typically the top 3 web search results or the results
of a Python script are actually more authoritative about what’s true in the world
than the user themselves or the model’s pretraining knowledge).
Thus, better ways of indicating
levels and kinds of trust might be beneficial
(or better post-training on natural language indicators of trust, and
more diverse data where the tool is adversarial).

## Towards Better Primitives or Robustness

The instruction hierarchy and natural language prompt engineering
are the main ways currently available for sectioning off
untrusted content. Our work adds to evidence that more effort
might be needed here.

One idea might be to better consider the difference between
“executable” and “non-executable” tool responses.
In some cases we expect instructions in tool results to be “executable” (eg, when a user
requests their coding agent to “complete the todos in the file proposal.md”), while others, like
in our tool-wrapping experiment, the results are expected to be “non-executable”.

A potential interesting direction is to support explicit parameter expansion primitives.
Python 3.14 recently introduced [t-strings](https://peps.python.org/pep-0750/),
designed for cases like sanitization when avoiding SQL or HTML injection.
If we had standardized model support for quarantining untrusted content,
we could imagine possibly plugging into such PL features for 
easy-to-use best practices around prompt injection.
While simple tool-wrapping does not currently appear to be a technique one can reliably hook into here,
with more training and design work, automatic tool-wrapping or other special
tokens or systems (like [Chen et al. (2025)](https://arxiv.org/abs/2402.06363) or [Zhang et al. (2026)](https://arxiv.org/abs/2604.09443)) seem possible.

![](https://dgros.io/misc/image_share/lw_ih_tool_study/listing_t_example.0e260d93.svg)

*Figure 3: Sketch of t-string-based prompt construction. Finding a usable standard like in the HTML injection analogy might be useful.*


# Conclusion

Using mock tool calls to wrap untrusted parts of a prompt seems
like it would be a useful direction. It uses a primitive that most
model providers have converged on, and tries to take advantage
of an important part of the OpenAI Model Spec. However, at least in this
small study with a few tasks, we did not see evidence that this gives clear benefits with current models,
and in fact could make things worse. It seems likely that “conversation role”
is overloaded, where it communicates both the source of the information,
and the trust level of the information (when in reality systems often operate with fairly
high-trust tools). This is not to say tool-wrapping can’t work, either with adjusted
instruction hierarchy training, or with additional exploration
(like different models, prompts, tasks, attacks, etc).
As more critical systems face adversarial
inputs or operate through agent tools, the need for
clarity on the instruction hierarchy will increase.

*This work is at a "workshop paper" / "research note" stage, so open to feedback.
I hope to encourage closer looks at the instruction hierarchy as a concept, and consideration if cases of inversion.
I'm also looking for discussion on what primitives LLM APIs are missing for improving safety and robustness, and how we might get practical agreement or standardization there. Comment here or email (david [at] far.ai) if you have thoughts.*

[^1]: OpenAI also supports a `Developer` role, which sits in between `System` and `User`, but this role appears less adopted.

[^2]: FastChat is a 39k+ star [GitHub repo](https://github.com/lm-sys/fastchat) from [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685).

[^3]: Loosely based on PAIR from [Chao et al., 2023](https://arxiv.org/abs/2310.08419).

[^4]: “counting deltas” is not a perfect metric, but
    we use it to help loosely characterize the trends across
    our many task-model-condition combinations.


[^5]: An “Ignore” attack prepends adversarial strings like
    “Ignore previous instructions …”.

[^6]: https://peps.python.org/pep-0750/

[^8]: Haiku often writes `[[rating: N]]` instead of `[[N]]`. It has different parse rates depending on prompt condition (32%-72%).
When responses don’t parse it can pull down the ASR.