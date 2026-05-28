# Actuarial Pricing and Reserving Implementation Plan

## Scope

This plan implements the first executable slice from `improve1.md` for `actuarial_pricing_reserving`. The slice focuses on high-value actuarial behavior that can be proven in package-local code without depending on external policy, claims, reinsurance, investment, or ledger tables.

## Implemented Domain Surface

1. Rating model version governance
   - Add explicit model states and activation rules.
   - Prevent retired, suspended, or unapproved models from being activated.
   - Select the correct model version for a product, jurisdiction, segment, and effective date.

2. Rating factor library and premium trace
   - Define factor schemas with allowed values, missing-value behavior, and optional relativities.
   - Validate rating inputs against factor definitions.
   - Reconstruct premiums from base rate, factor sequence, additive adjustments, minimum premium, rounding, and overrides.

3. Actuarial assumption registry and impact analysis
   - Track assumption type, selected value, effective period, approval, and retirement state.
   - Require active approved assumptions for pricing and reserving runs.
   - Produce side-effect-free impact analysis for proposed assumption changes.

4. Experience study and loss triangle governance
   - Validate study cohorts, exposure basis, period basis, and data quality thresholds.
   - Validate triangle shape by origin period and development age.
   - Calculate link ratios and selected development factors with rationale.

5. Reserving methods and rollforward evidence
   - Calculate chain-ladder and expected-loss reserve estimates.
   - Preserve method-level ultimate, unpaid, and IBNR evidence.
   - Reconcile reserve rollforwards with explicit movement components.

## Code Changes

- Add `actuarial_engine.py` with pure functions and immutable-style return payloads.
- Export the engine from the package `__init__.py`.
- Add package-focused tests proving core actuarial behavior and boundary safety.

## Review Checklist

- No shared table mutation.
- No stream-engine picker.
- Only AppGen-X event vocabulary appears in evidence.
- Functions are deterministic and side-effect-free.
- Tests cover positive, negative, and edge cases.

## Deferred Work

The remaining backlog items should be implemented in later slices: filing packets, stochastic reserve distributions, capital scenarios, catastrophe accumulation, reinsurance projections, validation plans, close workbench flows, and expanded UI components.
