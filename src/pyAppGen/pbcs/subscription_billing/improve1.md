# Subscription Billing PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `subscription_billing`. The items are specific to recurring revenue and subscription operations: plan catalog, rate schedules, trials, subscription lifecycle, phases, add-ons, change orders, cancellations, usage metering, billing schedules, invoices, invoice lines, credit memos, payment application, entitlements, revenue schedules, renewals, dunning, exceptions, rules, parameters, configuration, AppGen-X event reliability, UI workbenches, and agent-assisted billing operations.

## Current Domain Evidence Used

- Domain purpose: `subscription_billing` owns recurring revenue, usage rating, invoice approval, renewals, dunning, entitlement handoff, revenue recognition handoff, payment and price event handling, rules, parameters, configuration, and release evidence.
- Owned boundary: plan catalog, subscriptions, subscription phases, trial periods, add-ons, change orders, usage meters, billing schedules, invoices, invoice lines, credit memos, payment applications, entitlement grants, revenue schedules, billing exceptions, dunning notices, configuration, schema extensions, rules, parameters, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: runtime configuration, parameters, rules, schema extensions, plan registration, trial start, subscription creation, plan changes, cancellation, add-ons, usage recording, invoice generation, credit memos, payment application, entitlement grants, revenue recognition, renewal, billing exceptions, dunning notices, event receiving, control tests, proration simulation, revenue exposure scoring, workbench, schema/service/release evidence, permissions, UI binding, and boundary verification.
- Existing events and dependencies: emits `SubscriptionActivated`, `SubscriptionRenewed`, `UsageRated`, `SubscriptionChanged`, `SubscriptionCancelled`, `InvoiceApproved`, `InvoiceApprovalRequested`, `CreditMemoIssued`, `PaymentApplied`, `EntitlementGranted`, `RevenueRecognized`, and `DunningNoticeCreated`; consumes `PaymentCaptured` and `PriceOptimized`; integrates with payment, pricing, tax, ledger, entitlement, and customer projections only through declared APIs/events/projections.

## 50 Better-Than-World-Class Improvements

### 1. Plan catalog readiness gate

**Justification:** Subscription billing breaks when plans lack currencies, regions, periods, prices, included units, usage rates, tax treatment, or entitlement mappings.

**Improvement:** Add readiness checks for plan family, lifecycle status, supported currencies, supported regions, billing periods, base prices, included units, usage rates, add-on compatibility, tax marker, revenue treatment, entitlement mapping, and approval evidence.

### 2. Rate schedule versioning

**Justification:** Subscription invoices must prove which rates were effective for each period, phase, usage event, and plan change.

**Improvement:** Version rate schedules with effective dates, currency, region, plan family, price source event, discount guardrails, usage tiers, archived versions, migration notes, and invoice-line lineage.

### 3. Trial lifecycle governance

**Justification:** Trials affect conversion, entitlement access, billing start, renewal forecast, and abuse controls.

**Improvement:** Model trial states for offered, started, extended, converted, expired, cancelled, and abused with eligibility checks, trial length, extension approvals, entitlement scope, conversion score, and event evidence.

### 4. Subscription lifecycle state machine

**Justification:** Subscriptions move through draft, trial, active, paused, changed, renewal_review, renewed, past_due, suspended, cancelled, expired, and reactivated states.

**Improvement:** Implement transitions with actor, reason, effective date, idempotency key, billing schedule effect, entitlement effect, MRR effect, emitted events, and invalid-transition explanations.

### 5. Subscription phase governance

**Justification:** Phased contracts include ramps, discounts, trials, promotional terms, fixed-term periods, and renewal phases.

**Improvement:** Add phase definitions with sequence, effective window, price rules, discount rules, included units, minimum commitment, entitlement changes, renewal behavior, and invoice generation rules.

### 6. Add-on lifecycle management

**Justification:** Add-ons can be recurring, one-time, usage-based, seat-based, trialed, prorated, or coterminated.

**Improvement:** Model add-on states, compatibility, quantity, billing cadence, proration behavior, entitlement scope, start/end dates, cancellation rules, and MRR/ARR impact.

### 7. Change order controls

**Justification:** Upgrades, downgrades, seat changes, add-on changes, pauses, and cancellations need governed effective dating and proration.

**Improvement:** Add change-order types, requested date, effective date, current/target plan, delta quantity, approval rule, proration quote, customer notice, entitlement effect, and audit proof.

### 8. Cancellation and pause policy

**Justification:** Cancellation and pause decisions affect revenue, entitlements, dunning, renewals, and customer commitments.

**Improvement:** Add cancellation/pause policy checks for term commitment, notice period, refund/credit eligibility, entitlement termination, dunning status, renewal state, and final invoice behavior.

### 9. Billing schedule engine

**Justification:** Recurring billing requires precise invoice dates, period boundaries, timezone handling, holidays, retries, and renewal timing.

**Improvement:** Add schedule generation by billing calendar, anchor date, period, timezone, holiday behavior, next invoice date, renewal date, retry date, catch-up runs, and schedule-state proof.

### 10. Usage metering ingestion controls

**Justification:** Usage billing is vulnerable to duplicate events, late events, unit mismatches, and unbillable quantities.

**Improvement:** Validate usage by subscription, meter key, event id, quantity, unit, timestamp, billing period, lateness policy, duplicate idempotency, included units, and billable status.

### 11. Usage rating engine

**Justification:** Usage charges need tiering, included units, overage, minimums, rounding, currency, and effective rate evidence.

**Improvement:** Add rating traces with included-unit calculation, tier selection, effective rate, rounding precision, discounts, tax marker, rated amount, currency, and `UsageRated` event evidence.

### 12. Late usage adjustment workflow

**Justification:** Late-arriving usage can affect closed invoices, revenue schedules, customer trust, and auditability.

**Improvement:** Add late usage states, cutoff rules, adjustment invoice, credit memo, next-cycle carryforward, approval thresholds, customer notice, and revenue impact evidence.

### 13. Invoice generation readiness

**Justification:** Invoices should not be generated when schedules, usage, plan rates, tax, payment, or entitlement markers are incomplete.

**Improvement:** Validate subscription state, billing period, plan version, usage completeness, payment status, tax marker, credit balance, entitlement status, approval threshold, and dependency freshness before invoice generation.

### 14. Invoice lifecycle state machine

**Justification:** Invoices require controlled states from draft to approved, posted, paid, partially paid, disputed, credited, voided, written off, and closed.

**Improvement:** Implement invoice transitions with amount validation, approvals, payment applications, credit memo effects, revenue schedule effects, emitted events, and audit proof.

### 15. Invoice line traceability

**Justification:** Customers and auditors need every invoice line tied to plan, phase, add-on, usage, credit, tax marker, or adjustment source.

**Improvement:** Add line provenance, source record, rate version, quantity, unit, period, proration ratio, discount, rounding, tax class, revenue treatment, and entitlement linkage.

### 16. Invoice approval workflow

**Justification:** High-value or anomalous invoices need human review before approval.

**Improvement:** Add approval thresholds, anomaly triggers, approver role, review queue, approval/denial reason, expiry, escalation, and `InvoiceApproved` or `InvoiceApprovalRequested` event evidence.

### 17. Credit memo lifecycle

**Justification:** Credits affect invoices, revenue, payment balance, customer trust, and audit trails.

**Improvement:** Model credit memo states, source invoice, amount ceiling, reason, approval, tax/revenue effect, application target, customer notice, and `CreditMemoIssued` evidence.

### 18. Payment application governance

**Justification:** Payment events must be applied idempotently and accurately to invoices and balances.

**Improvement:** Add application states, payment event id, amount, currency, invoice match, partial payment, overpayment, unapplied balance, duplicate suppression, and `PaymentApplied` event output.

### 19. Dunning strategy engine

**Justification:** Collections should balance recovery, customer value, risk, and compliance.

**Improvement:** Add dunning strategies by customer segment, invoice age, amount, payment history, risk score, region, payment method, notice cadence, suspension policy, and escalation path.

### 20. Dunning notice lifecycle

**Justification:** Dunning notices need controlled creation, delivery, retry, suppression, escalation, and closure.

**Improvement:** Model notice states, reason, invoice/subscription link, risk score, retry policy, delivery channel, suppression reason, dead-letter target, customer response, and closure proof.

### 21. Renewal confidence scoring

**Justification:** Renewal actions should be prioritized by confidence, churn risk, usage, payment history, support risk, and customer value.

**Improvement:** Score renewal confidence using subscription health, usage trend, payment delays, dunning history, plan fit, discount exposure, support/customer signals, and renewal history.

### 22. Renewal approval workflow

**Justification:** Low-confidence or high-value renewals require review before automatic renewal.

**Improvement:** Add renewal review states, confidence threshold, churn reason, approver, negotiation notes, renewal terms, event evidence, and schedule updates.

### 23. MRR and ARR movement ledger

**Justification:** Recurring revenue reporting needs explainable movements for new, expansion, contraction, churn, reactivation, and FX changes.

**Improvement:** Add movement records with source event, prior MRR/ARR, new MRR/ARR, movement type, plan/add-on linkage, effective date, currency, FX note, and audit proof.

### 24. Revenue schedule governance

**Justification:** Approved invoices must produce revenue recognition schedules with correct periodization and evidence.

**Improvement:** Generate schedules by invoice line, service period, recognition method, deferred amount, recognized amount, period, ledger handoff marker, and `RevenueRecognized` evidence.

### 25. Entitlement grant governance

**Justification:** Subscription state must drive entitlements accurately without sharing entitlement tables.

**Improvement:** Create entitlement grants with subscription, plan, phase, add-on, scope, start/end dates, status, revocation reason, projection freshness, and `EntitlementGranted` event evidence.

### 26. Billing exception management

**Justification:** Usage spikes, payment delays, tax mismatches, entitlement mismatches, and revenue variances require structured resolution.

**Improvement:** Add exception type, severity, affected subscription/invoice, root cause, recommended action, owner, SLA, resolution proof, retry/dead-letter linkage, and workbench triage.

### 27. Tax quote handoff marker

**Justification:** Billing needs tax readiness without directly owning tax calculation.

**Improvement:** Record tax quote references, jurisdiction, quote expiry, taxable basis, invoice linkage, mismatch state, recalculation need, and declared API/projection lineage.

### 28. Ledger handoff marker

**Justification:** Billing must prove what should be posted without writing directly to ledger tables.

**Improvement:** Add ledger handoff markers for invoice approval, credit memo, payment application, revenue recognition, write-off, and adjustment with idempotency and delivery evidence.

### 29. Pricing event guardrails

**Justification:** Optimized prices can change subscription rates and discounts but must respect contracts and discount guardrails.

**Improvement:** Consume `PriceOptimized` with contract eligibility, effective date, discount cap, current phase, renewal-only flag, override approval, and rate schedule versioning.

### 30. Payment captured handler controls

**Justification:** Payment events must update invoice state exactly once and handle partials, overpayments, and unknown invoices.

**Improvement:** Add idempotent `PaymentCaptured` handling with invoice match, amount validation, currency validation, partial/overpayment routing, unknown invoice exception, retry evidence, and dead-letter evidence.

### 31. AppGen-X outbox delivery assurance

**Justification:** Subscription, usage, invoice, credit, payment, entitlement, revenue, and dunning events drive downstream capabilities.

**Improvement:** Add outbox states, ordering group, payload hash, retry attempts, next retry, delivery proof, dead-letter linkage, and replay controls for every emitted billing event.

### 32. Cross-PBC boundary proof

**Justification:** Subscription Billing must not directly read payment, pricing, tax, ledger, entitlement, customer, or analytics tables.

**Improvement:** Add release evidence scanning schema descriptors, services, routes, DSL, workbench bindings, and agent plans for foreign table access, proving dependencies are APIs, events, or package-local projections only.

### 33. Multi-tenant and customer isolation

**Justification:** Billing records contain sensitive pricing, payment, usage, and contract information.

**Improvement:** Add tenant/customer isolation evidence for subscriptions, invoices, usage, dunning, rules, parameters, configuration, events, workbench views, exports, and agent plans.

### 34. Proration quote simulator

**Justification:** Plan changes and seat changes need accurate proration previews before customer commitments.

**Improvement:** Simulate proration by effective date, remaining ratio, current plan, target plan, add-ons, usage, discounts, taxes marker, credits, and next invoice effect.

### 35. Counterfactual plan simulation

**Justification:** Commercial teams need to compare plan, discount, add-on, and usage alternatives against revenue and churn.

**Improvement:** Simulate plan changes, usage tiers, discounts, commitments, renewal terms, add-ons, and billing cadence with effects on MRR, ARR, churn risk, revenue schedule, and customer cost.

### 36. Revenue exposure forecasting

**Justification:** Billing teams need forward-looking exposure across churn, payment failure, dunning, usage volatility, and revenue timing.

**Improvement:** Forecast MRR, ARR, invoices, payments, dunning risk, renewal probability, revenue recognition, credit exposure, and usage variance by plan, cohort, tenant, and period.

### 37. Billing anomaly detection

**Justification:** Abnormal billing patterns can reveal metering defects, pricing errors, payment problems, entitlement mismatches, or revenue leakage.

**Improvement:** Detect anomalies in usage spikes, invoice totals, discounts, credits, payment applications, dunning notices, renewal confidence, entitlement grants, revenue schedules, and dead letters.

### 38. Governed billing model evidence

**Justification:** Churn, revenue, pricing, and dunning models influence customer treatment and revenue decisions.

**Improvement:** Track model purpose, training window, feature lineage, validation metrics, drift, false-positive/negative impact, approval status, rollback, and explainability evidence.

### 39. Semantic billing instruction parsing

**Justification:** Billing operators express actions such as pause this subscription, credit usage, or quote an upgrade in natural language.

**Improvement:** Parse instructions into safe query or command previews with target subscription, action, amount, effective date, policy checks, missing evidence, confidence, and no mutation until confirmed.

### 40. Agent-safe billing plans

**Justification:** The billing chatbot must not silently change subscriptions, issue credits, apply payments, or recognize revenue.

**Improvement:** Require side-effect-free plans naming command, permission, owned tables, idempotency key, expected event, financial impact, rollback limits, and human confirmation for all billing mutations.

### 41. Billing workbench coverage

**Justification:** Operators need a full recurring-revenue command center, not isolated subscription tables.

**Improvement:** Expand workbench surfaces for plans, subscriptions, trials, phases, add-ons, change orders, usage, schedules, invoices, credits, payments, entitlements, revenue, renewals, dunning, exceptions, events, rules, parameters, configuration, and release evidence.

### 42. Invoice approval cockpit

**Justification:** High-risk invoices need fast review with line-level evidence and recommended actions.

**Improvement:** Add queues by approval threshold, anomaly, customer risk, usage spike, tax mismatch, credit impact, revenue impact, payment delay, and event failure with drilldowns.

### 43. Renewal console

**Justification:** Renewal management needs contract, usage, payment, dunning, churn, and entitlement context.

**Improvement:** Add renewal views with confidence score, churn drivers, MRR/ARR, term dates, usage trend, dunning state, payment history, proposed terms, and approval actions.

### 44. Dunning board

**Justification:** Collections teams need prioritized, explainable, and compliant dunning queues.

**Improvement:** Add board views for notices, aging, risk score, amount due, customer value, suppression, retry status, delivery failures, escalation, entitlement suspension, and recovery actions.

### 45. Runtime parameter governance

**Justification:** Renewal confidence, churn risk, dunning risk, precision, retry limits, discount guardrails, and approval thresholds materially affect revenue.

**Improvement:** Add parameter bounds, impact simulation, approval workflow, effective dating, tenant/plan overrides, rollback, and release evidence for billing parameters.

### 46. Schema extension governance

**Justification:** Subscription businesses need custom contract attributes while preserving owned boundaries.

**Improvement:** Allow extensions only on owned billing tables with field validation, sensitivity classification, migration preview, UI binding preview, API exposure review, and release-audit evidence.

### 47. Continuous billing control testing

**Justification:** Billing controls should be proven continuously across subscriptions, usage, invoices, payments, entitlements, revenue, and events.

**Improvement:** Add assertions for invoice without active subscription, usage without meter, payment over-application, credit above invoice, entitlement without subscription, revenue without approved invoice, foreign-table access, dead-letter aging, and agent-preview bypass.

### 48. Billing resilience drills

**Justification:** Recurring revenue operations must degrade safely through duplicate events, payment delays, pricing lag, and invoice failures.

**Improvement:** Add drills for duplicate payment, price event delay, usage spike, invoice approval failure, dunning dead letter, entitlement handoff outage, revenue handoff failure, and workbench degraded mode.

### 49. Subscription Billing readiness score

**Justification:** Users need an evidence-backed view of whether `subscription_billing` is ready for live recurring revenue operations.

**Improvement:** Compute readiness from plan catalog, subscription lifecycle, usage rating, schedules, invoices, payments, entitlements, revenue schedules, renewals, dunning, events, UI coverage, model governance, controls, boundary proof, and agent safety.

### 50. End-to-end recurring revenue proof

**Justification:** A complete Subscription Billing PBC must prove it can execute the full lifecycle from plan setup through revenue evidence.

**Improvement:** Add an executable proof scenario covering plan registration, trial, subscription activation, add-on, usage rating, invoice generation and approval, payment application, entitlement grant, revenue recognition, renewal, dunning branch, emitted events, UI evidence, boundary proof, controls, and agent explanation.
