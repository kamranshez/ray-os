# Newsletter Survey Check-up Routine

A weekly (Monday) or on-demand routine for a newsletter survey analyst. The analyst pulls PostHog data, computes metrics, generates insights, and sends Ray a Telegram report — but only if there's data worth reporting. If zero responses, exit silently.

**Step 1 — Query PostHog** (via `query-run`), past 7 days:
- **Query A:** `newsletter_survey_answer` events grouped by `step`, `question_id`, `answer`
- **Query B:** `newsletter_survey_completed` events grouped by `using_ai_to_code`, `preferred_harness`, `current_role`, `learning_goals`
- **Query C:** count of `newsletter_browse_free_classes_clicked`

If Query A has zero rows → stop, send nothing.

**Step 2 — Compute metrics:** total starts (step=1 rows), completions, completion rate, per-step drop-off, Browse Free Classes CTR, answer distributions.

**Step 3 — Analyze:** Generate 3-5 concrete recommendations by cross-referencing:
- Q1 (AI coding) × Q3 (role) → audience stage
- Q2 (harness) distribution → comparison/migration posts if non-Claude-Code tool >15%
- Q3 (role) → pricing/tone signals (student discount if Student >25%, ROI content if Founder/CTO >20%)
- Q4 (learning goals) → cluster into themes, flag 3+ mentions without a matching ACS class
- Funnel health → simplify questions if completion <60%, fix CTA if CTR <30%, fix any step with >20% drop-off
- Week-over-week shifts >15%

**Step 4 — Decide:** Proceed only if Step 1 had data.

**Step 5 — Send two Telegram messages** via `curl` to `api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage` with `chat_id=${TELEGRAM_USER_ID}`, `parse_mode=Markdown`:
- **Message A — Metrics:** funnel, CTR, worst drop-off, Q1-Q4 distributions
- **Message B — Insights & Recs:** Audience, Content Gaps, Funnel Fixes, Pricing Signal sections

Don't truncate. Write every insight in full.

**Error handling:** On any failure, send a ⚠️ Telegram alert with step name and error message.

**PostHog events reference:**
- `newsletter_survey_answer` — props: `question_id`, `question`, `answer`, `step`, `total_steps`
- `newsletter_survey_completed` — props: `using_ai_to_code`, `preferred_harness`, `current_role`, `learning_goals`
- `newsletter_browse_free_classes_clicked` — no props

**Environment:** `TELEGRAM_BOT_TOKEN`, `TELEGRAM_USER_ID` available in shell.