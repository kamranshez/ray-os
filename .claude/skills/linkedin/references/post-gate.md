# The pre-post gate

The single checklist every LinkedIn draft passes before it is shown to Ray or posted to Slack. Both the writing flow (`write-post.md`) and the source scout (`source-scout.md`, run daily by the cloud and on demand by Ray) run THIS file. Do not keep a second copy anywhere.

The skeleton it enforces lives in `references/viral-playbook.md`. Read that first; this file only checks the output.

Run every item on every draft, whether you generated one post or ten.

1. Hook line ends in a colon AND contains a digit. No digit, no post. Rewrite the hook. A hook like "Wild:" is an automatic discard.
2. Element order is exactly 1-8 from the skeleton. Nothing else goes in the body. No sub-headings ("Why this matters:"), no extra paragraphs between the spec block and the link line, no second closer. The closer comes AFTER the link line, never before it.
3. Spec block has both tiers. Every arrow bullet must contain an Arabic numeral; if it does not, move it to the hyphen tier. Hyphen bullets carry named features. All-arrow blocks fail. No `•`.
4. Why-it-matters is ONE paragraph, 2-4 sentences. Count them.
5. Link line present, followed by a real url starting with http, copied from the source and never reconstructed from memory. This is a BLOCKING fail: do not output the draft with a bad url and a note about it. Placeholders fail even when you flag them. Known tells: `dQw4w9WgXcQ`, `example.com`, `EXAMPLE`, Reddit ids like `1abc234`, any id you did not read from the source. If the source has no verifiable url, stop and ask Ray (interactive) or drop the pick (unattended). This applies to personal-story posts too.
6. 150-250 words including the P.S. Aim for 170-220; drafts that run to 245 are always the ones that sprawled structurally.
7. P.S. present and byte-identical to the canonical line in `viral-playbook.md` (single ASCII hyphen, bare domain), or a topic-matched Agentic Coding School pointer in the same shape.
8. Every factual claim in the post, numeric or not, traces to the source. That covers prose as well as the spec block. Do not invent product facts ("no waitlist"), durations, trends ("keeps falling"), audience behaviour ("most teams"), or superlatives ("fastest"). Do not derive new numbers by arithmetic from sourced ones. Do not restate a range's ceiling as a point fact.
   - **The scene-setting lines are factual claims, not colour.** Every noun in elements 2 and 3 must appear in the source. "One camera. No LiDAR." only works if the source says so. If you cannot fill three scene lines from source facts, write two. This is where fabrication hides, because it reads as rhythm rather than as a claim.
   - **Paraphrase is allowed; added detail is not.** You may restate a source quote in Ray's words. You may not attach a setting ("on stage"), a role or title ("a mathematician at Anthropic"), a proportion of credit ("did the heavy lifting"), or a history ("mathematicians had attacked it for 87 years") that the source did not state. If you would have to look it up to be sure, it is not in the source.
   - **No inferred facts either**, including implied time cadence, ordering, or audience behaviour. If the source states X, you may not state a consequence of X as a fact ("$2,300/month" does not license "$11,700 a month saved"; "it funds his full-time work" does not license "the school is still running").
9. House rules: no em or en dashes, sentence case, authors credited by handle, no DM keyword CTAs, feature-first framing. Same skeleton, Ray's voice, never copy Stanislav's actual sentences.
10. Would Ray say this at a dinner with smart people? Is it true to his actual experience?

Cut and redraft anything that fails. Report the check as a one-line result per draft so the gate leaves evidence.

## Glyphs

The writing flow drafts with the unicode arrow `→`. The scout drafts with ASCII `-> ` so the text survives Slack and copy-paste, whichever caller ran it. Both are valid arrow bullets for item 3. Feature bullets are always a plain hyphen `- `.
