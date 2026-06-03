---
class: "prompt-engineering"
chapter: "Core Techniques"
---
Interview-style prompting flips the dynamic: instead of you trying to anticipate what the model needs to know, you tell the model the goal and let it ask YOU the questions. This is the single most underrated technique in prompt engineering because it solves the hardest problem — you don't know what you don't know.

### The Information Asymmetry Problem

Every prompt has an information gap. You know things the model doesn't (your specific context, constraints, preferences). But the model also knows things you don't — specifically, *what information it needs* to give a good answer.

When you write a prompt, you're guessing which details matter. You include some, forget others, and assume the model shares your context. The result: you get a plausible-sounding output that's subtly wrong because it filled the gaps with training-data defaults instead of your actual situation.

Interview-style prompting closes this gap by making the model surface what it needs before attempting the task.

### The Pattern

```
I need [goal]. Before you start, interview me. Ask me one question at a time
about anything you need to know — audience, constraints, format, context,
examples, things to avoid. When you have enough information, say
"I have enough" and produce the output.
```

That's it. The model then becomes the interviewer, and you become the subject matter expert who just answers questions naturally.

### Why It Produces Better Results Than Any Single Prompt

1. **It surfaces your blind spots** — the model asks about things you'd never think to include. "What's the reading level of your audience?" "Is there a word limit?" "Should I include a CTA?" You have answers to all of these — you just wouldn't have included them unprompted.

2. **It matches how humans actually communicate** — nobody gives a perfect brief on the first try. Conversations are how we transfer context. Interview-style prompting embraces this instead of fighting it.

3. **It builds context incrementally** — each answer narrows the output distribution further. By the time the model starts generating, it has 10-15 data points about your preferences, constraints, and context. That's the equivalent of a very detailed prompt, assembled through conversation rather than upfront planning.

4. **It's faster for complex tasks** — writing a perfect 500-word prompt takes planning and iteration. Answering 8 questions takes 3 minutes of natural speech (especially with voice dictation).

### Controlling the Interview

The basic pattern works, but you can tune it:

**Scope the questions**: "Interview me, but only ask about tone, audience, and format — don't ask about content, I'll handle that."

**Limit the depth**: "Ask me no more than 5 questions."

**Batch the questions**: "Ask me 3 questions at a time instead of one at a time." (Faster but slightly less precise — each batch can't build on previous answers.)

**Direct the interview**: "I need a LinkedIn post. Interview me, focusing on what would make this resonate with CTOs specifically."

### The Auto-Spec Connection

This technique is the foundation of the auto-spec workflow used in software development. When you're building a feature, instead of writing a perfect Product Requirements Document upfront, you tell the model:

"I want to build [feature]. Interview me about every decision you'd need to make — data model, edge cases, error handling, UI behavior, permissions. One question at a time."

The model asks 15-30 targeted questions. Your answers become the spec. This is faster and more thorough than writing the spec from scratch because:
- The model knows what engineering decisions exist (from training data)
- You know what your specific constraints are (from your domain knowledge)
- The interview surfaces the intersection

### Interview-Style for Taste Extraction

Connecting to the Scaling Taste concept: interview-style prompting is also how you *extract* your taste for compression into skills and archetypes.

Instead of trying to introspect and write down your preferences, let the model interview you:

"I want to build a writing style guide based on how I actually write. Interview me about my preferences — sentence length, vocabulary, what I hate in writing, what I admire, how formal I am in different contexts. One question at a time."

Your answers become the raw data for a taste-activated skill. The interview surfaces preferences you didn't know you had — "Actually, now that you ask, I never use semicolons" — which are exactly the details that make a compressed identity accurate.

### The Context.json Pattern: Persistent Interview Context

Interview-style prompting is powerful for a single session. But what about projects that span weeks or months? Every new conversation starts from zero — the model doesn't remember what you told it last time.

The fix is simple: after the interview, ask the model to compile everything you said into a structured file — call it `context.json` or `project-context.md`. Upload it to a Claude Project, GPT Project, or Gemini Gem. Now every future conversation in that project starts with the full context from your interview, without you repeating anything.

The workflow:
1. Start a new project in your AI tool
2. Tell the model: "Interview me about this project — goals, constraints, audience, anything relevant"
3. Answer 8-15 questions naturally
4. When done: "Compile everything I told you into a structured context file I can reuse"
5. Save the file and upload it to the project

The key step most people skip: at the end of each subsequent conversation, ask the model to update the context file with any new decisions or information that came up. Replace the old file. Your context grows incrementally — each session adds signal without you writing documentation.

This bridges interview-style prompting (a single-session technique) with context engineering (a persistent system). The interview extracts your knowledge; the context file preserves it across sessions.

### When NOT to Use Interview Style

- **Simple tasks** — if you can describe what you want in one sentence, just describe it. The interview adds overhead.
- **Time-critical work** — the back-and-forth takes 3-5 minutes. For quick outputs, a direct prompt with constraints is faster.
- **Highly technical tasks** — if you're an expert and know exactly what you want, the interview will ask questions you've already answered internally. Just write the detailed prompt.
- **Batch/automated workflows** — interview style requires a human in the loop. For agent-to-agent communication, use structured output instead.

### Demo

1. Ask for a blog post directly — show the generic output that assumes a default audience, tone, and structure
2. Same task with interview style — answer 6-8 questions naturally
3. Compare the two outputs side by side — the interview version captures nuances that the direct prompt missed entirely
4. Show a software spec interview — the model asks about edge cases you hadn't considered
5. Show interview style for taste extraction — model surfaces writing preferences you didn't know you had

### Key Insight

> The best prompt is often the one you don't write yourself. Interview-style prompting solves the fundamental problem of prompt engineering: you can't include context you don't realize is relevant. By letting the model surface what it needs, you get a prompt's worth of context assembled through natural conversation — and the result is better than any prompt you'd write in one shot, because it closes gaps you didn't know existed.
