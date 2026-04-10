# Writing LinkedIn Posts

The goal every time is to write **10 different posts** using emotional psychology principles. Each post should use a different combination of emotional triggers so the user can pick the one that hits hardest.

## Before Writing

1. Read all files in `references/post-history/` to understand Ray's voice and what's worked
2. Read `references/viral-playbook.md` — this is the core framework, not optional guidance
3. If the user gives a topic, think about it through the lens of the 6 emotional triggers before writing anything

## The Writing Process

For each of the 10 posts:

### Step 1: Choose the Emotional Architecture

Before writing a single word, decide:
- **Primary trigger** (the hook — what makes them stop scrolling)
- **Secondary trigger** (the body — what makes them engage)

Use a different primary trigger for each of the 10 posts. This gives the user real variety, not 10 versions of the same angle. With 6 triggers and a Belief Disruption structure, you have more than enough combinations to make each post feel distinct.

Example trigger pairings:
- Curiosity Gap + Aspiration — "The setup that..." + show what's possible
- Productive Discomfort + Identity Validation — Challenge a belief + "it's not your fault, here's why"
- Tribal Belonging + Status Signaling — "Two types of developers..." + make sharing signal sophistication
- Identity Validation + Productive Discomfort — "You've felt this but never said it" + "here's what to do about it"
- Belief Disruption + Aspiration — Shatter a common assumption + show the better path
- Aspiration + Curiosity Gap — Paint the outcome + tease the method
- Status Signaling + Tribal Belonging — Make sharing signal expertise + define the in-group
- Productive Discomfort + Curiosity Gap — Call out the problem + hint at the fix
- Identity Validation + Aspiration — "You've been here" + "here's where you could be"
- Belief Disruption + Tribal Belonging — Break the assumption + show who already gets it

### Step 2: Write for Feeling, Not Information

Ask yourself: "What will the reader *feel* after reading this?" If the answer is "informed," rewrite it. The answer should be one of: seen, challenged, curious, aspirational, tribal, uncomfortable-in-a-good-way.

The same fact can be repackaged for any trigger:

**Fact:** Anthropic shipped scheduled tasks for Claude Code.

- **Productive Discomfort:** "You're still waking up to the same bugs you went to sleep with. Some developers wake up to PRs that fixed themselves overnight. Same tool. Different setup."
- **Tribal Belonging:** "There are developers learning Claude Code features one by one, and developers who've turned it into an autonomous pipeline. The second group isn't smarter — they just stopped thinking of AI as an assistant."
- **Identity Validation:** "If you've ever felt guilty for not being 'technical enough' to use AI properly — the developers shipping fastest right now aren't writing code at all. They're writing prompts on their phones."

### Step 3: Run the Authenticity Filter

Before including each post, check:
1. Is this true based on Ray's actual experience?
2. Would Ray say this at a dinner with smart people?
3. Is the emotional intensity proportional to the claim?
4. Does it serve the reader, not just engagement?

If it fails any test, rewrite or cut it.

## Writing Rules

### Voice
- Ray's voice: casual, opinionated, grounded in real experience
- Sentence-case capitalization always
- Short sentences that stack. Conversational rhythm.
- The reader should feel like a smart friend is telling them something they need to hear

### Output Format

After writing all 10 posts, generate an HTML preview so the user can see them styled as real LinkedIn posts with copy buttons.

1. Write a JSON file to `/tmp/linkedin-posts.json`:

```json
{
    "posts": [
        {
            "number": 1,
            "triggers": "Productive Discomfort + Aspiration",
            "body": "The full post text here..."
        }
    ]
}
```

2. Run the preview script:
```bash
python scripts/preview-posts.py /tmp/linkedin-posts.json --output /tmp/linkedin-preview.html --open
```

This opens an HTML page styled like LinkedIn's feed with all 10 variations and a copy button on each. The user picks the one they want to use.

Do NOT also output the raw post text in the conversation — the HTML preview is the deliverable.

## After the User Picks

1. Save their chosen post(s) to `references/post-history/YYYY-MM-DD_slug.md`:

```yaml
---
date: YYYY-MM-DD
hook: "First line of the post"
triggers:
  primary: productive discomfort
  secondary: aspiration
media: text only
status: draft
engagement:
  reactions: null
  comments: null
  reposts: null
  impressions: null
url: null
notes: null
---

The full post text here...
```

3. Ask: "Want me to post this, or are you posting yourself? Or save as a draft to come back to later?"
   - If Claude posts → see `references/browser-navigation.md`, then update status to `posted` once confirmed
   - If the user is posting themselves → update status to `posted` once they confirm it's live
   - If saving as a draft → keep status as `draft` and add a todo to `todos.yaml` (see below) so it surfaces on the next skill invocation
4. Update `todos.yaml` in the skill root (NOT any global todos file):
   - For posted posts → add an entry to check engagement in 3 days (`due: <today + 3>`)
   - For drafts → add an entry to finalize and post the draft, with `related_post` pointing to the post-history file
   - When a todo is completed, flip `status: done` or remove it — don't let completed entries accumulate
