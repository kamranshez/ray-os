---
name: wise-transfer-verify
description: >
  Verify whether a Wise transfer actually went through before re-sending it.
  Use this skill whenever Ray gets an email or message claiming a payment
  "didn't arrive", "wasn't transferred", "expired", "was cancelled", "got
  bounced back", or "please re-send" — especially affiliate payouts, vendor
  payments, or transfers Ray sent via Wise. Also trigger when Ray says "check
  if X got paid", "did this go through", "look up that transfer", "verify
  before I resend", or pastes a Wise reference like RW20260523 and wants its
  status. Talks to the live Wise API across every profile (personal, Ray
  Amjad Ltd, Project Solve Labs CIC, Intentional AI Ltd), not just the CSV
  statement, so it catches the real outcome (sent / refunded / cancelled /
  waiting). Always run this BEFORE sending a replacement payment so Ray
  doesn't double-pay someone who already got their money or who already has
  a pending re-send queued up.
---

# Wise Transfer Verify

Verifies the live status of a Wise transfer so Ray can decide whether to
re-send a payment. The big risk we are protecting against is double-paying:
someone emails saying "I never got it", Ray feels bad and re-sends, but the
original payment actually went through, OR a re-send is already queued.

## When to run

Run BEFORE initiating any replacement Wise payment. Typical triggers:

- An email like "I was too slow accepting the Wise transfer, can you re-send?"
- "Did my affiliate payout for May go out?"
- "This vendor says they never received the payment"
- Ray pastes a Wise reference code (e.g. `RW20260523`)

## How to use it

There is one script: `scripts/check_transfer.py`. It reads `WISE_API_KEY`
from the repo-root `.env` (which is `.gitignore`d) and searches recent
transfers across every Wise profile on the account.

Filter by whatever signal you have. Combine flags freely.

```bash
# By Wise reference code (most precise)
python3 .claude/skills/wise-transfer-verify/scripts/check_transfer.py \
  --reference RW20260523

# By recipient email (triggers recipient lookup, slower)
python3 .claude/skills/wise-transfer-verify/scripts/check_transfer.py \
  --email carsten@360onlinemarketing.dk

# By recipient name
python3 .claude/skills/wise-transfer-verify/scripts/check_transfer.py \
  --name "360 Online Marketing"

# By amount (matches source OR target within 5 cents)
python3 .claude/skills/wise-transfer-verify/scripts/check_transfer.py \
  --amount 113.43

# Widen the search window (default is 60 days)
python3 .claude/skills/wise-transfer-verify/scripts/check_transfer.py \
  --email someone@example.com --days 180
```

If you only have a vague description from the email (e.g. "the payment I
sent last Tuesday for around $100 to Carsten"), start with the most unique
signal — usually the email address or the reference code if they quoted one.

## Interpreting the status

Wise transfer statuses you'll see in the output:

- **`outgoing_payment_sent`** — Wise has sent the money. Do NOT re-send.
- **`funds_converted`**, **`processing`** — In flight. Wait, don't re-send.
- **`waiting_recipient_input_to_proceed`** — Email-claim transfer is
  sitting in the recipient's inbox waiting to be accepted. A re-send is
  effectively already queued; tell the recipient to click the Wise email
  link. Do NOT initiate another transfer.
- **`funds_refunded`** — Recipient never claimed the email-claim transfer
  in time. Money is back in Ray's Wise balance. Safe to re-send (ideally
  to a real bank account this time, not an email-claim).
- **`cancelled`** — Transfer never funded. Safe to re-send.
- **`bounced_back`** — Bank rejected it. Check the recipient's account
  details before re-sending.

## Reporting back to Ray

After running the script, give Ray a clear verdict, not a JSON dump.
Structure:

1. **Verdict in one line** — "Yes it went through" / "No, it was refunded,
   safe to re-send" / "A re-send is already pending — tell them to check
   their email".
2. **The matching transfer(s)** — date, amount, recipient, reference,
   status.
3. **Anything else worth flagging** — e.g. a separate pending transfer to
   the same recipient, or another recent refund pattern that suggests a
   systemic issue (multiple email-claim payouts failing because recipients
   don't click in time).

## API key handling

The script reads `WISE_API_KEY` from `<repo-root>/.env`. That file is in
`.gitignore` (it's the very first line). Never paste the key into a commit,
a comment, a log line, or a message to Ray — he already has it in `.env`.

If `.env` is missing the key, the script exits with a clear error. Don't
silently fall back to environment variables in a way that could mask a
missing key.

## Why a script and not inline curl

The Wise account has four profiles (personal + three businesses) and
affiliate payouts go through `Ray Amjad Ltd`, not the personal profile.
Doing this with raw curl forgets one of the profiles half the time, which
is exactly how you end up wrongly telling Ray "I don't see that transfer,
must not have happened" and triggering a double-payment. The script
guarantees every profile is checked.
