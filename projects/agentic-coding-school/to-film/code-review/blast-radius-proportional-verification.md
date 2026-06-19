---
class: "code-review"
status: "scripted"
aliases: [blast-radius-proportional-verification]
---

# Blast Radius: Verification Proportional to Risk

## What This Video Covers

The shift from asking "did someone review this code?" to asking "what is the blast radius if this code is wrong, and is our verification proportional to that risk?" Code review as a universal practice is getting unbundled. In its place: a risk-management discipline where you tier code by business blast radius (internal tools, external-facing services, safety-critical systems) and match your verification investment to actual exposure.

This video introduces blast radius as the new core engineering discipline in an AI-assisted world, and shows how to apply it to your own workflow inside Claude Code.

## Why This Matters

The old model assumed a human read every line. That assumption is breaking: agents produce code faster than anyone can hand-review, and insisting on universal line-by-line review just collapses into rubber-stamping.

The replacement is not less rigor, it is proportional rigor. A throwaway bash script does not deserve the same verification as a production migration. A one-off internal dashboard does not deserve the same verification as a payment webhook. Treating them the same is not caution, it is waste.

From the retreat:

> "One practitioner framed this as the new core engineering discipline: instead of asking 'did someone review this code?' organizations need to ask 'what is the blast radius if this code is wrong, and is our verification proportional to that risk?'"

> "This moves engineering from a craft model (every line is hand-reviewed) to a risk management model (verification investment matches exposure)."

## The Three Tiers

A starter taxonomy viewers can apply to their own work:

1. **Internal / throwaway**: scripts, one-off analyses, prototypes. Blast radius is you. Verification: run it, does it work, ship it.
2. **External-facing**: customer features, API endpoints, content that goes out. Blast radius is users and reputation. Verification: tests, staging, typecheck, sometimes human review of the sensitive parts.
3. **Safety-critical / irreversible**: migrations, payments, auth, infra, anything with a blast radius that can't be rolled back cheaply. Verification: specs, tests, staging, canary, human sign-off, feature flags, planned rollback.

The discipline is not "always do tier 3." It is: be honest about which tier you are in, and match the verification.

## Blast Radius of Agent Permissions

Not just code has blast radius. Agent permissions do too. The retreat's clearest example:

> "Granting an agent email access enables password resets and account takeovers. Full machine access for development tools means full machine access for anything the agent decides to do."

Techniques to cover in Claude Code:
- Tool allowlists per project (what the agent can and can't touch)
- Hooks that gate destructive operations (force push, DB migrations, external sends)
- Using plan mode as a verification step before irreversible actions
- The "reversibility ladder": local edits → commits → pushes → merges → deploys → external effects. Further down the ladder, more verification.

## Why Most Teams Get This Wrong

Two failure modes:
- **Uniform paranoia**: every change gets the full treatment, so nothing ships, and the actual high-blast-radius changes hide in the noise.
- **Uniform laxity**: "Claude did it, looks fine," applied equally to a README fix and a schema migration. Eventually the blast lands.

Proportional verification is a forcing function. You can only apply it if you are willing to decide, explicitly, that the internal script is not worth testing and the payment code is non-negotiable.

## Key Concepts to Cover

- The quote: "did someone review this code?" is the wrong question now
- Blast radius as a property of code AND of agent permissions
- The three-tier taxonomy (internal / external / safety-critical)
- The reversibility ladder (local → committed → pushed → merged → deployed → external)
- Craft model vs risk management model
- Why uniform verification is wasteful AND unsafe (real risk hides in the noise)
- Practical Claude Code setup: tool allowlists, hooks, plan mode for irreversible ops
- Connection to feature flags, canaries, rollback as first-line mitigation (not code review)
- The discipline of being explicit about tier ("this is tier 1, I am not going to test it")

## Demo Plan

1. Walk through a real repo and classify three files into the three tiers
2. Show a throwaway script being shipped with zero verification (tier 1, appropriate)
3. Show a prod-adjacent change being gated by tests + plan mode (tier 2)
4. Show a migration being gated by staging + backup + hook (tier 3)
5. Show a bad example: someone treating tier 3 code like tier 1 and the blast
6. Show a bad example: someone treating tier 1 code like tier 3 and the waste

## Suggested Class Placement

Techniques — Fundamental Techniques (pairs well with core-agent-loop and subagent-verification-loops as a foundational mental model)
