export const meta = {
  name: 'loopy-ai-class-review',
  description: 'Teacher/learner/researcher review of the loopy-ai class for pedagogical coherence',
  phases: [
    { title: 'Order', detail: 'teacher reads all lessons and proposes canonical order' },
    { title: 'Teach-Learn', detail: 'per concept: teacher explains, learner attacks (no file access)' },
    { title: 'Research', detail: 'researcher resolves gaps the teacher escalates with source-grounded evidence' },
    { title: 'Synthesis', detail: 'final coherence report and seamless-journey arc' },
  ],
}

const VAULT_PATH = '/Users/ray/Desktop/ray-os/projects/agentic-coding-school/to-film/loopy-ai'

const LEARNER_PERSONA = `You are a smart student in Ray's "Loopy AI" class. You do NOT read the source lesson files — your job is to interrogate the teacher's explanation directly. If you find yourself tempted to read the vault, STOP. You only know what the teacher has told you.

What you CAN do:
- You've built throwaway Claude Code workflows for personal projects (config tweaks, small scripts, scratchpad agents, the occasional custom command).
- You understand the core agent loop: model gets a prompt, calls tools, sees results, loops until done.
- You're comfortable with the mental model of "tools as functions the LLM calls" and "context window as working memory."
- You've used subagents / the Task tool a couple of times but only ad-hoc — never designed a deliberate multi-agent system.
- You have intermediate Python/JS, can read code fluently, know what unit tests and CI are.
- You vaguely know the words "eval" and "verifier" but couldn't design either from scratch.

What you CAN'T do yet:
- You have NEVER designed a verifier, an evaluator, or a loop with an outer success criterion.
- You do NOT know what "ralph loops", "ACE three-role split", "borrowed verifiers", "echo chamber", "mission command", "L1/L4/L5", "governance primitives", "autoresearch", or any of Ray's specific terminology means until the teacher defines it for you in this very lesson.
- You've never deliberately separated planner / executor / reviewer roles.
- You don't know what "closing the loop" means in this curriculum.
- You've never thought about agent discovery, workers as a layer, or governance as a design primitive.

How you behave:
- You are sharp, not naive. DO NOT ask "what is an agent?" — you know.
- You restate concepts back in your own words to expose what you actually understood vs. what slid past you.
- You explicitly compare each new concept to what was established earlier in this class — if the teacher hasn't bridged it, you call that out by name.
- You flag every term the teacher used that they did not define in this lesson.
- You are skeptical of unsupported claims ("loops are better because X" — prove it).
- You ask exactly ONE closing question — the one that would unblock you most.

You are the kind of student a teacher hopes for: engaged, paying attention, demanding rigor, building a real mental model.`

const ORDER_SCHEMA = {
  type: 'object',
  required: ['order', 'flagged_issues', 'foundational_pick'],
  properties: {
    order: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'role', 'depends_on', 'one_line_justification'],
        properties: {
          file: { type: 'string', description: 'filename relative to loopy-ai/ — e.g. "intro.md"' },
          role: { type: 'string', enum: ['foundational', 'core', 'advanced', 'supporting'] },
          depends_on: { type: 'array', items: { type: 'string' }, description: 'filenames of prior lessons this depends on' },
          one_line_justification: { type: 'string' },
        },
      },
    },
    flagged_issues: {
      type: 'array',
      items: {
        type: 'object',
        required: ['issue_type', 'detail'],
        properties: {
          issue_type: { type: 'string', enum: ['missing_prereq', 'duplicate_coverage', 'unclear_role', 'orphan', 'order_ambiguity'] },
          detail: { type: 'string' },
        },
      },
    },
    foundational_pick: {
      type: 'array',
      items: { type: 'string' },
      description: 'Filenames in teaching order representing the canonical foundational+core+advanced spine to drill into. Include EVERY lesson that is a real teaching beat — exclude only pure reference/supporting files (role=supporting) unless they introduce new concepts.',
    },
  },
}

const ATTACK_SCHEMA = {
  type: 'object',
  required: ['restatement', 'bridge_check', 'undefined_terms', 'gaps', 'closing_question', 'escalate_to_research'],
  properties: {
    restatement: { type: 'string', description: 'The concept in the learner\'s own words — exposes what was actually understood.' },
    bridge_check: { type: 'string', description: 'Did this concept anchor cleanly to what was established earlier? If not, where did the bridge fail?' },
    undefined_terms: { type: 'array', items: { type: 'string' } },
    gaps: {
      type: 'array',
      items: {
        type: 'object',
        required: ['gap', 'severity'],
        properties: {
          gap: { type: 'string' },
          severity: { type: 'string', enum: ['blocker', 'serious', 'minor'] },
        },
      },
    },
    closing_question: { type: 'string', description: 'The ONE question that would unblock the learner the most.' },
    escalate_to_research: { type: 'boolean' },
    research_question: { type: 'string', description: 'Empty string if not escalating; otherwise the exact question for the researcher.' },
  },
}

const RESEARCH_SCHEMA = {
  type: 'object',
  required: ['findings', 'confidence'],
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['excerpt', 'source', 'relevance'],
        properties: {
          excerpt: { type: 'string', description: 'Exact quote — not a paraphrase.' },
          source: { type: 'string', description: 'File path or URL.' },
          relevance: { type: 'string', description: 'Why this excerpt addresses the gap.' },
        },
      },
    },
    confidence: { type: 'string', enum: ['high', 'medium', 'low', 'no_evidence_found'] },
    note: { type: 'string' },
  },
}

phase('Order')
const ordering = await agent(
  `You are the teacher for Ray's "Loopy AI" class. List every .md file in ${VAULT_PATH} (ignore _inbox/ and images/) and read them all. They are draft lesson scripts.

Your task: propose the canonical lesson order for teaching this class to a student matching this persona:

---
${LEARNER_PERSONA}
---

Return structured output following the schema. Specifically:
- "order" — every lesson file, with role classification, dependencies, and one-line justification.
- "flagged_issues" — concepts referenced without a prerequisite lesson, duplicate coverage, orphan files, etc.
- "foundational_pick" — up to 7 filenames in teaching order that form the foundational+core spine. These will be drilled into by the learner agent. Choose the ones whose pedagogical soundness most determines whether the class works.`,
  { label: 'propose-order', phase: 'Order', schema: ORDER_SCHEMA }
)

const limit = (args && typeof args.limit === 'number') ? args.limit : ordering.foundational_pick.length
const toDrill = ordering.foundational_pick.slice(0, limit)
log(`Ordering complete. Drilling into ${toDrill.length} of ${ordering.foundational_pick.length} concepts: ${toDrill.join(', ')}`)

const established = []
const results = []

for (let i = 0; i < toDrill.length; i++) {
  const file = toDrill[i]
  const priorContext = established.length === 0
    ? '(This is the FIRST lesson — no prior concepts established yet.)'
    : established.map((e, idx) => `${idx + 1}. ${e.concept}\n   Learner's understanding: ${e.summary}`).join('\n\n')

  phase('Teach-Learn')

  const teaching = await agent(
    `You are teaching Ray's "Loopy AI" class. Your student matches this persona — internalize it:

---
${LEARNER_PERSONA}
---

Concepts already established earlier in this class (from the learner's own restatements):

${priorContext}

Now teach the concept from this file:
${VAULT_PATH}/${file}

Read the file thoroughly first. Then explain the concept to the student. Your explanation MUST:
1. Open with an explicit learning objective: "By the end of this lesson the student will be able to [verb] [concept]."
2. Anchor to prior concepts BY NAME when relevant. If this is lesson 1, anchor instead to what the persona says they already know.
3. Define every Ray-specific term you introduce — assume the student has only heard the words listed in the persona before this lesson.
4. Use exactly one concrete worked example.
5. State a single takeaway sentence at the end.

Return ONLY the lesson explanation as the student would experience it. No meta-commentary, no "here is my explanation", no markdown headers labeling sections. Just the teaching.`,
    { label: `teach:${file}`, phase: 'Teach-Learn' }
  )

  const attack = await agent(
    `${LEARNER_PERSONA}

Concepts established so far in this class (your own prior restatements):

${priorContext}

The teacher just delivered this lesson to you:

---
${teaching}
---

Do your job per the schema:
- "restatement" — your understanding in your OWN words. If the teacher said something you can't actually restate, expose that.
- "bridge_check" — did this lesson anchor cleanly to what was established earlier? Be specific about WHERE the bridge held or failed.
- "undefined_terms" — every term the teacher used that you don't have a working definition for from THIS lesson plus the persona's baseline.
- "gaps" — places the explanation didn't earn its conclusion, with severity.
- "closing_question" — the ONE question that would unblock you the most.
- "escalate_to_research" — true if there's a factual / external claim, a comparison to outside work, or a gap that the teacher's own materials can't close. Set "research_question" to the exact question you'd want the researcher to answer.`,
    { label: `learn:${file}`, phase: 'Teach-Learn', schema: ATTACK_SCHEMA }
  )

  let research = null
  if (attack.escalate_to_research && attack.research_question) {
    phase('Research')
    research = await agent(
      `You are the researcher for Ray's "Loopy AI" class. The teacher has escalated a gap from a student. Your output must be SOURCE-GROUNDED — excerpts and citations, NOT summaries or paraphrases.

The gap: ${attack.research_question}

Context: this came up while teaching "${file}". Concepts established so far:
${priorContext}

Where to search:
1. The loopy-ai vault: ${VAULT_PATH} (other lessons may already address it).
2. Ray's broader vault: /Users/ray/Desktop/ray-os/ (skills, scripts, prior writing).
3. External sources via the Exa MCP tool (load mcp__claude_ai_Exa_Advanced__web_search_exa via ToolSearch if needed). Use it for academic papers, blog posts, open-source patterns.

Each finding MUST include:
- "excerpt" — the EXACT quote (not paraphrased).
- "source" — vault-relative path or full URL.
- "relevance" — one sentence on why this addresses the gap.

If you cannot find evidence, set confidence to "no_evidence_found" and explain in "note". Do not fabricate.`,
      { label: `research:${file}`, phase: 'Research', schema: RESEARCH_SCHEMA }
    )
  }

  established.push({ concept: file, summary: attack.restatement })
  results.push({ file, teaching, attack, research })
  log(`Lesson ${i + 1}/${ordering.foundational_pick.length} done: ${file} — ${attack.gaps.length} gaps (${attack.gaps.filter(g => g.severity === 'blocker').length} blockers)${research ? ', researcher called' : ''}`)
}

phase('Synthesis')
const synthesis = await agent(
  `You are synthesizing a teacher / learner / researcher review of Ray's "Loopy AI" class into a coherence report Ray will use to teach.

Big-picture goal Ray stated: "meet the learner where they are and feel like a seamless journey from the beginning of the class to the end."

The learner persona used throughout:
---
${LEARNER_PERSONA}
---

Lesson order proposed by the teacher:
${JSON.stringify(ordering, null, 2)}

Per-lesson teach → learn → research results:
${JSON.stringify(results.map(r => ({
  file: r.file,
  teaching_excerpt: r.teaching.slice(0, 800),
  learner_restatement: r.attack.restatement,
  bridge_check: r.attack.bridge_check,
  undefined_terms: r.attack.undefined_terms,
  gaps: r.attack.gaps,
  closing_question: r.attack.closing_question,
  research_findings_count: r.research?.findings?.length ?? 0,
  research_confidence: r.research?.confidence ?? null,
  research_excerpts: r.research?.findings?.map(f => ({ source: f.source, excerpt: f.excerpt.slice(0, 200) })) ?? [],
})), null, 2)}

Produce a markdown report with these sections, in this order:

# Loopy AI — Class Coherence Review

## 1. Recommended Canonical Order
Full ordered list with one-line rationale per lesson. Call out where the teacher's order should be reshuffled and why.

## 2. The Seamless Journey
One paragraph: the throughline arc from lesson 1 to the closing argument. What story does this class tell?

## 3. Cross-Cutting Gaps
The 5 most important gaps that span lessons (terms introduced before defined, missing bridges, repeated confusion). Each with: the gap, where it surfaces, the fix.

## 4. Per-Lesson Verdicts
For each foundational/core lesson drilled: a 2-3 sentence verdict (what works, what to add, severity).

## 5. Lessons That Need Rework Now
Top 3 lessons that most jeopardize the seamless-journey goal. Specific guidance per lesson: what to cut, what to add, what to define earlier.

## 6. Open Research Questions
Anything the researcher flagged as low confidence or no evidence found — Ray should resolve these before teaching.

Be direct and specific. Cite filenames. No throat-clearing.`,
  { label: 'synthesis', phase: 'Synthesis' }
)

return { ordering, results, synthesis }
