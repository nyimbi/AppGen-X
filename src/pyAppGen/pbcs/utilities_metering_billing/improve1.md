# Utilities Metering and Billing Improvement Backlog

## Current Domain Evidence Used

- Stable PBC key: `utilities_metering_billing`.
- Manifest and specification scope the package around meter reads, usage validation, tariffs, service orders, utility bills, billing adjustments, collections interactions, and customer utility billing.
- Owned lifecycle entities already exist for `meter_read`, `usage_interval`, `tariff`, `service_order`, `utility_bill`, `billing_adjustment`, and `customer_meter_account`.
- Public APIs already exposed are `POST /meter-reads`, `POST /usage-intervals`, `POST /tariffs`, `POST /service-orders`, `POST /utility-bills`, and `GET /utilities-metering-billing-workbench`.
- Existing executable domain operations include `create_meter_read`, `record_usage_interval`, `review_tariff`, `approve_service_order`, `simulate_utility_bill`, `create_billing_adjustment`, and `record_customer_meter_account`.
- Existing UI fragments are `UtilitiesMeteringBillingWorkbench`, `UtilitiesMeteringBillingDetail`, and `UtilitiesMeteringBillingAssistantPanel`.
- Existing emitted events are `UtilitiesMeteringBillingCreated`, `UtilitiesMeteringBillingUpdated`, `UtilitiesMeteringBillingApproved`, and `UtilitiesMeteringBillingExceptionOpened`; consumed events are `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- `SPECIFICATION.md` and `RELEASE_EVIDENCE.md` already set expectations for owned-boundary behavior, AppGen-X eventing, governed agent execution, and release assurance.

### 1. Service point master identity
**Justification:** Billing accuracy depends on a stable service point identity that survives account changes, meter swaps, and tariff revisions without conflating premise, meter, and customer concepts.
**Improvement:** Add an explicit service point model under the `customer_meter_account` boundary with premise identifier, commodity, voltage/pressure class, feeder or zone, geocode, lifecycle status, and effective-dated links to active customer, active meter set, and active tariff assignment.
**Acceptance evidence:** Tests prove one active billable relationship per service point and date, `UtilitiesMeteringBillingDetail` shows service point lineage, and release evidence includes occupied, vacant, disconnected, and reconnected service point scenarios.

### 2. Service point energization and service-order boundary
**Justification:** Connect, disconnect, suspend, and reconnect actions affect when billing can legally start, stop, or resume.
**Improvement:** Make energization state changes first-class outcomes of `service_order` approval, with explicit statuses for pending connection, live, disconnected for non-payment, disconnected on request, and safety lockout, plus effective timestamps used by billing logic.
**Acceptance evidence:** Scenario tests prove service orders change service point state only through approved transitions, workbench queues highlight pending energization actions, and event history shows who authorized each state change.

### 3. Meter asset registry and installation metadata
**Justification:** A bill cannot be defended if the system cannot show which physical or virtual meter was installed, where it was installed, and how it was configured.
**Improvement:** Extend meter ownership to capture serial number, manufacturer, model, multiplier, firmware, communication type, seal status, install date, removal date, service point placement, and register inventory for each meter instance.
**Acceptance evidence:** Migration and contract tests cover meter create, install, remove, and reassign flows; the detail view renders current and prior installed meters; and release evidence includes a meter-history audit export.

### 4. Meter exchange, rollover, and final-initial read chaining
**Justification:** Meter replacement and register rollover are common sources of revenue leakage and dispute when final and initial reads are not linked.
**Improvement:** Add a meter exchange workflow that records outgoing final reads, incoming initial reads, rollover flags, multiplier differences, and continuity rules so consumption is stitched cleanly across removed and installed meters.
**Acceptance evidence:** End-to-end tests prove no gap or double-counted usage across exchanges, bill simulations explain rollover math, and exception evidence captures unresolved exchange mismatches.

### 5. Register and channel model for complex metering
**Justification:** Electricity, water, and gas billing often depends on multiple registers or channels, not one scalar reading.
**Improvement:** Model meter registers and interval channels explicitly for import, export, reactive energy, demand, pressure, and flow, with unit-of-measure validation and tariff mapping per register or channel.
**Acceptance evidence:** Sample fixtures cover single-register, time-of-use, demand, and net-export meters, rating tests bind channels to the right tariff determinants, and the UI shows per-register contribution to billed quantities.

### 6. Read capture provenance across AMI, handheld, and manual entry
**Justification:** Read trustworthiness depends on source provenance, not just the captured value.
**Improvement:** Store read source, collector identity, device session, acquisition time, geotag where relevant, photo evidence where relevant, and whether the read arrived from AMI, field handheld, customer self-service, or office entry.
**Acceptance evidence:** API tests on `POST /meter-reads` require provenance fields, detail pages show origin and evidence, and release evidence includes both AMI and field-read examples.

### 7. Meter health, drift, and certification schedule
**Justification:** Unhealthy meters produce bad reads long before they fail completely.
**Improvement:** Add meter health indicators for stale telemetry, repeated communication failure, certification expiry, drift suspicion, and repeated estimate substitution so operations can intervene before billing is compromised.
**Acceptance evidence:** Analytics tests flag overdue certification and unhealthy meters, workbench cards surface health badges and aging, and scenario evidence includes automatic creation of follow-up service orders.

### 8. Read validation ladder
**Justification:** Utilities need deterministic validation layers before a read becomes billable.
**Improvement:** Implement a validation ladder covering presence, monotonicity where applicable, rollover handling, multiplier application, historical tolerance bands, service point status, duplicate detection, date-window validity, and prior-final-read consistency.
**Acceptance evidence:** Validation fixtures prove accepted, warned, blocked, and exceptioned outcomes, rule traces show which step fired, and assistant previews explain why a read was or was not promoted.

### 9. Interval completeness and gap stitching
**Justification:** Usage analytics and interval-based tariffs fail when gaps, overlaps, or timezone drift remain unresolved.
**Improvement:** Add completeness checks for `usage_interval` by interval length, timezone, daylight-saving shift, overlap, missing window, and derived total consistency, with governed repair paths for interpolation or backfill.
**Acceptance evidence:** Interval test packs cover missing half-hour and hourly windows, backfill projections show before-after completeness, and the workbench exposes unresolved interval gaps by service point.

### 10. Estimate hierarchy and substitution policy
**Justification:** Estimated consumption is unavoidable, but the basis must be ranked and auditable.
**Improvement:** Define an estimate hierarchy that prefers adjacent actual reads, aligned season history, occupancy-adjusted profiles, weather-normalized patterns, and engineering fallback, while storing confidence, reason code, and expiry criteria on every estimate.
**Acceptance evidence:** Rating tests show which estimate strategy was selected, estimate records include confidence and reason codes, and release evidence includes prolonged access-denied, communication-outage, and new-service estimates.

### 11. Estimate replacement and frozen-bill rules
**Justification:** When an actual read arrives after an estimate, rebilling rules must be predictable and compliant.
**Improvement:** Add replacement logic that marks superseded estimates, decides whether to rebill immediately or carry correction forward, freezes periods already under dispute or regulatory hold, and records customer-impact deltas.
**Acceptance evidence:** Simulation tests show actual-read replacement outcomes, bills trace which estimated quantities were reversed, and audit history captures the freeze reason for protected periods.

### 12. Read and estimate exception taxonomy
**Justification:** Operators need more precision than a generic failed status when triaging meter and billing exceptions.
**Improvement:** Introduce explicit exception codes for inaccessible meter, suspect read, repeated estimate, reverse flow, meter mismatch, stale interval feed, tariff missing, service point inactive, and move boundary conflict, each with severity, owner, SLA, and next action.
**Acceptance evidence:** Exception tables contain typed codes and SLAs, workbench filters slice by exception family, and release evidence includes one full remediation trail for each critical exception class.

### 13. Suspicious consumption and tamper analytics
**Justification:** Revenue assurance depends on identifying usage patterns that do not match the physical or customer context.
**Improvement:** Add anomaly scoring for sudden drop, sudden spike, flatline, impossible negative import, reverse-flow anomaly, bypass suspicion, and neighborhood outlier behavior, with distinct outcomes for inspection, hold, or informational watch.
**Acceptance evidence:** Analytics tests show expected flags on crafted tamper scenarios, the assistant panel summarizes drivers of the anomaly score, and event evidence records when inspection recommendations were accepted or rejected.

### 14. Field re-read and investigation orchestration
**Justification:** Some validation failures need a field action, not a back-office override.
**Improvement:** Tie selected exception types to `service_order` creation for re-read, inspection, meter test, or disconnect visit, while preserving a clear owned boundary between billing decisions and operational field execution.
**Acceptance evidence:** Tests prove qualifying exceptions spawn governed service orders, workbench links exceptions to field actions and outcomes, and release evidence shows closed-loop resolution from suspect read to corrected bill.

### 15. Read-to-bill validation explainability
**Justification:** Billing teams and regulators need to understand how raw reads turned into billed quantities.
**Improvement:** Store a read-to-bill trace that links source reads, interval repairs, estimate substitutions, validation results, tariff determinants, and final billed components for each bill segment.
**Acceptance evidence:** `UtilitiesMeteringBillingDetail` renders a drill-down from bill line to originating reads, test snapshots verify deterministic trace output, and audit exports can be produced without querying foreign tables.

### 16. Tariff versioning with effective-dated determinants
**Justification:** Tariffs change frequently, and rating defects usually come from bad effective dating rather than bad arithmetic.
**Improvement:** Make `tariff` versioning explicit with approval state, jurisdiction, commodity, customer class, service point class, effective start and end, supersession rules, and non-overlap validation for determinant sets.
**Acceptance evidence:** Contract tests reject overlapping active versions, the tariff board shows pending and active versions clearly, and release evidence includes a regulator-driven tariff replacement scenario.

### 17. Rating engine for blocks, time-of-use, demand, and net export
**Justification:** Utilities billing often combines several charging methods on one account.
**Improvement:** Extend bill simulation to support inclining and declining blocks, time-of-use windows, demand ratchets, power factor penalties, fixed charges, minimum charges, and net-export credit treatment within one reproducible rating trace.
**Acceptance evidence:** Bill simulation fixtures cover flat, TOU, demand, and net-metering accounts, each line item shows its determinant set and formula basis, and result snapshots are stable across reruns.

### 18. Tariff eligibility, riders, subsidies, and exemptions
**Justification:** Social tariffs, public-lighting rules, lifeline blocks, and rider eligibility materially change customer outcome.
**Improvement:** Add eligibility rules that attach riders, subsidies, exemptions, and special handling based on service point class, customer program enrollment, regulator directives, or protected-customer status, with clear precedence over default tariff logic.
**Acceptance evidence:** Rule tests prove rider and subsidy assignment order, workbench details show why an account qualified or did not qualify, and release evidence includes a protected-customer billing example.

### 19. Bill-cycle calendar and segment generation
**Justification:** Bills must align to cycle calendars even when operational events happen mid-cycle.
**Improvement:** Introduce a bill-cycle calendar with route, zone, or service-point grouping and generate bill segments whenever meter changes, tariff changes, move events, or service state changes occur inside the cycle.
**Acceptance evidence:** Cycle-generation tests show correct segment splits, workbench views display pending and completed cycle runs, and release evidence includes a cycle with multiple mid-period events.

### 20. Proration across tariff, meter, and occupancy changes
**Justification:** Mid-cycle changes create some of the hardest billing disputes because usage and fixed charges must be allocated fairly.
**Improvement:** Add explicit proration rules for fixed charges, demand windows, minimum charges, and consumption blocks when the service point changes tariff, meter, occupancy, or energization state during a cycle.
**Acceptance evidence:** Scenario packs prove proration math for move, reconnect, tariff update, and meter exchange cases, bill details show the proration basis, and rule traces expose day-count and usage-allocation methods.

### 21. Reproducible bill calculation and line-level traceability
**Justification:** Finance, customer care, and auditors need to rerun a bill and get the same answer from the same evidence set.
**Improvement:** Persist bill-calculation inputs, rule versions, parameter versions, read set hashes, and deterministic line-item traces so `simulate_utility_bill` can reproduce the original output exactly.
**Acceptance evidence:** Rerun tests match original bill outputs byte-for-byte on stable fixtures, release evidence stores calculation hashes, and detail pages expose calculation version metadata.

### 22. Taxes, levies, fuel clauses, and regulatory riders
**Justification:** Many bills are legally dominated by non-energy or non-volume components that change independently from the core tariff.
**Improvement:** Treat taxes, levies, universal service charges, fuel or power cost adjustments, municipal surcharges, and regulator-mandated riders as separately versioned components with their own effective dates and precedence rules.
**Acceptance evidence:** Fixture bills show statutory and tariff-based charges separately, rating traces identify the source rule for each rider, and release evidence includes a period where only the regulatory rider changed.

### 23. Adjustment governance with typed debit and credit reasons
**Justification:** Adjustments are unavoidable, but uncontrolled adjustments create audit and revenue risk.
**Improvement:** Require `billing_adjustment` records to carry typed reason codes, reference bill segments, materiality bands, maker-checker approval paths, customer-communication requirements, and reversal linkage for every debit or credit.
**Acceptance evidence:** Permission and workflow tests enforce maker-checker rules, the adjustment board filters by reason and approval state, and release evidence includes reversal of an incorrectly posted adjustment.

### 24. Backbilling and rebilling workflow
**Justification:** Correcting historic billing periods is operationally and legally sensitive.
**Improvement:** Add a governed backbilling and rebilling flow that computes corrected historic periods, customer impact, carry-forward treatment, and notice obligations, while preventing silent mutation of already-issued bills.
**Acceptance evidence:** Scenario tests show multi-period rebill outputs and customer deltas, event history records replaced bill relationships, and release evidence includes a regulator-capped backbill example.

### 25. Payment boundary event model
**Justification:** This PBC needs payment facts for billing status, but it should not own payment instrument storage or settlement ledgers.
**Improvement:** Define explicit inbound and outbound payment-boundary events for bill issued, payment posted, reversal posted, unpaid threshold reached, promise-to-pay registered, and write-off approved, while keeping receivables and settlement ownership outside this package.
**Acceptance evidence:** Boundary tests prove billing status changes only from declared payment events, interface contracts document fields and idempotency keys, and no payment-card or bank-account tables appear under this PBC.

### 26. Allocation rules for partial payments, credits, and write-offs
**Justification:** Customer balance narratives become inconsistent when payment allocation logic lives outside the bill narrative.
**Improvement:** Store allocation views that explain how partial payments, overpayments, prepayments, refunds, credits, and write-offs were applied across bill segments without turning this PBC into the system of record for cash settlement.
**Acceptance evidence:** Detail views show open, paid, credited, and written-off amounts per bill segment, integration tests replay payment events in different orders safely, and release evidence includes partial-payment and reversal examples.

### 27. Customer move-in boundary orchestration
**Justification:** The move-in boundary decides when a customer starts paying and which opening quantities belong to them.
**Improvement:** Add a move-in workflow that validates service point vacancy or transfer eligibility, captures opening read or opening estimate, applies deposits or connection fees where configured, and starts billing only from the effective occupancy timestamp.
**Acceptance evidence:** Tests prove no pre-move usage is billed to the incoming customer, workbench flows show move-in readiness and blockers, and release evidence includes same-day transfer and vacant-premise move-in cases.

### 28. Customer move-out boundary orchestration
**Justification:** The move-out boundary determines final liability, final read handling, and the handoff to vacant or successor occupancy.
**Improvement:** Add a move-out workflow that captures final read or approved estimate, final bill generation, disconnection or leave-live decision, forwarding contact capture, and successor-account handoff rules for the same service point.
**Acceptance evidence:** Scenario tests show correct final bill timing and successor-account separation, event traces record final-read completion, and release evidence includes disputed move-out and access-denied final-read cases.

### 29. Vacant premise and landlord continuity rules
**Justification:** Many utilities need a defined billing posture between occupants instead of treating the service point as ownerless.
**Improvement:** Support vacant-premise, landlord, or house-account modes with effective-dated responsibility rules, reduced service-state options, and clear separation from standard retail customer billing.
**Acceptance evidence:** Tests prove usage during vacant intervals is attributed according to configured policy, detail pages show the responsible party per date range, and release evidence includes vacancy-to-occupancy transition scenarios.

### 30. Deposits, connection fees, and arrears carry-forward
**Justification:** Customer onboarding and account transfer often involve non-consumption balances that still influence billing.
**Improvement:** Add controlled handling for deposit assessment, deposit refund eligibility, connection and reconnection fees, installment plans, and arrears carry-forward so these amounts appear in the billing narrative without breaking the payment boundary.
**Acceptance evidence:** Bill fixtures show deposit and fee presentation distinctly from usage charges, workflow tests handle deposit refund triggers on move-out, and release evidence includes arrears transfer and installment-plan cases.

### 31. Usage analytics cockpit
**Justification:** Billing teams need operating insight into how customers and service points are consuming, not just whether a bill was produced.
**Improvement:** Build analytics for daily, monthly, and seasonal usage, normalized consumption by customer class and service point class, read success rate, estimate rate, and billed-to-actual variance by meter cohort and route.
**Acceptance evidence:** `GET /utilities-metering-billing-workbench` returns usage KPI summaries, dashboard snapshots prove route-level drill-down works, and test fixtures validate the metric definitions.

### 32. Forecasting, budget billing, and leak alerts
**Justification:** Proactive customer care depends on spotting likely overconsumption before the next bill lands.
**Improvement:** Add forecast models for expected end-of-cycle consumption and bill amount, plus leak or continuous-flow alerts for water and abnormal base-load alerts for electricity or gas, with optional budget-billing plan suggestions.
**Acceptance evidence:** Forecast tests compare expected and actual outcomes on fixed fixtures, alert queues show explainable drivers, and release evidence includes alert-to-customer-outreach examples.

### 33. Exception workbench with SLA and ownership
**Justification:** Revenue protection and customer service both degrade when unresolved exceptions disappear into general queues.
**Improvement:** Rework `UtilitiesMeteringBillingWorkbench` to provide explicit exception inboxes by read issue, interval issue, tariff issue, bill issue, move boundary issue, and payment-boundary issue, with owner, due date, severity, and escalation path.
**Acceptance evidence:** UI tests verify queue filters, aging badges, and bulk assignment, event evidence records escalation actions, and release evidence includes SLA breach reporting.

### 34. Billing dispute and complaint handling
**Justification:** A regulated utility needs a defensible dispute workflow that pauses only the right actions and preserves evidence.
**Improvement:** Add dispute cases linked to bill segments, reads, adjustments, and service orders, with dispute reason codes, evidence attachments, hold rules, decision outcomes, and customer-notice checkpoints.
**Acceptance evidence:** Workflow tests prove disputes freeze only configured actions, detail views show dispute lineage end to end, and release evidence includes upheld, partial-upheld, and rejected dispute examples.

### 35. Regulatory billing rule packs by jurisdiction
**Justification:** Billing rules are often jurisdiction-specific and change on regulator notice rather than engineering cadence.
**Improvement:** Organize policy rules into effective-dated regulatory packs that can govern estimated bill caps, notice windows, social tariff eligibility, meter-testing obligations, and rebill limits per jurisdiction or tenant.
**Acceptance evidence:** Rule-pack tests show jurisdiction-specific outcomes on the same base scenario, the assistant panel identifies the active regulatory pack, and release evidence includes a mid-year regulator-rule change.

### 36. Consumer-protection, disconnection, and moratorium rules
**Justification:** The PBC must know when billing or service actions are legally constrained by protected-customer or seasonal rules.
**Improvement:** Add rule support for disconnection notice periods, cold- or heat-season moratoriums, protected medical accounts, minimum payment thresholds before disconnection, and maximum estimated-bill streaks before mandatory field action.
**Acceptance evidence:** Compliance fixtures verify illegal actions are blocked, workbench banners show why an account is protected, and release evidence includes a moratorium-period non-payment case.

### 37. Workbench queue design around operator jobs
**Justification:** Domain users work by job type, not by table name.
**Improvement:** Reshape `UtilitiesMeteringBillingWorkbench` into queues for read review, estimate review, tariff activation, bill-run approval, adjustment approval, move processing, dispute handling, and exception clearance, each with mass-action and evidence drill-down support.
**Acceptance evidence:** UI navigation tests cover every queue, operators can complete core jobs without raw table access, and release evidence includes screenshot packs for each queue state.

### 38. Service point, meter, and bill detail UX
**Justification:** Investigations slow down when users must jump between unrelated screens to understand one account.
**Improvement:** Expand `UtilitiesMeteringBillingDetail` into a unified timeline that shows service point status, meter installations, read history, interval quality, tariff timeline, bill segments, adjustments, disputes, and payment-boundary status on one page.
**Acceptance evidence:** Detail-view tests confirm all major lifecycle artifacts are visible, screenshots show linked drill-down panels, and release evidence includes a complex account timeline with exchange, estimate, rebill, and payment reversal.

### 39. Approval, override, and exception UX safeguards
**Justification:** Billing overrides are high-risk and should feel deliberate in the UI.
**Improvement:** Require structured override reason capture, before-after value display, impacted-customer counts, regulator-rule warnings, and second-approver prompts in approval flows for tariffs, adjustments, rebills, and protected exceptions.
**Acceptance evidence:** UI tests block submission when override evidence is incomplete, approval history shows captured justification fields, and release evidence includes screenshots of guarded override flows.

### 40. Agent skill for read and exception review
**Justification:** Operators spend significant time classifying suspect reads and assembling the same evidence repeatedly.
**Improvement:** Add an agent skill that summarizes read provenance, prior history, validation failures, anomaly drivers, and recommended next actions, but requires human confirmation before any write to `meter_read`, `usage_interval`, `service_order`, or `utility_bill`.
**Acceptance evidence:** Assistant transcripts show evidence-backed recommendations, policy tests block unconfirmed mutations, and release evidence includes side-by-side human-versus-agent review outcomes.

### 41. Agent skill for tariff and regulatory notice intake
**Justification:** Tariff updates and regulator notices often arrive as semi-structured documents that are expensive to hand-key.
**Improvement:** Add an intake skill that parses tariff schedules, rider notices, and regulator directives into draft `tariff` changes or policy-rule updates, highlights ambiguous clauses, and links every extracted field to source snippets.
**Acceptance evidence:** Document-ingestion fixtures cover clean and noisy notices, the assistant panel shows extraction confidence and source mapping, and approval workflows preserve draft-versus-approved separation.

### 42. Agent skill for adjustment drafting and bill explanation
**Justification:** Customer care and back-office teams need fast, consistent explanations for why a bill changed.
**Improvement:** Add an agent skill that drafts adjustment proposals, customer-facing bill explanations, and dispute summaries using bill traces, read traces, and rule outcomes, while keeping approval and final mutation under existing permissions.
**Acceptance evidence:** Draft-generation tests verify required evidence links are present, UI previews show human-editable outputs, and audit history records who accepted or rejected each assistant draft.

### 43. Expanded domain event model
**Justification:** Current coarse events are not enough to reconstruct important service-point, meter, and billing lifecycle transitions.
**Improvement:** Add granular AppGen-X events for service point activated, service point disconnected, meter installed, meter removed, read validated, estimate created, estimate replaced, bill simulated, bill issued, adjustment approved, and dispute opened, mapped back to the existing package eventing model.
**Acceptance evidence:** Event-contract tests validate payloads and naming, projections rebuild lifecycle timelines from events alone, and release evidence includes an event-sequence trace for a full billing cycle.

### 44. Outbox, inbox, and dead-letter recovery evidence
**Justification:** Billing operations must survive duplicate messages, delayed events, and partial downstream failures.
**Improvement:** Strengthen AppGen-X handling with deterministic idempotency keys per domain action, replay-safe consumers, dead-letter classification by failure cause, and operator tools to retry or suppress events with audit evidence.
**Acceptance evidence:** Retry tests prove duplicates do not create duplicate bills or adjustments, dead-letter views show root cause and remediation status, and release evidence includes a successful replay after simulated downstream failure.

### 45. Cross-boundary event contracts for policy, payment, and KPIs
**Justification:** This PBC depends on upstream policy and downstream payment facts, but those interactions must stay explicit and narrow.
**Improvement:** Formalize consumed-event handling for `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`, plus declared integration contracts for payment-status facts and analytics export, without direct mutation of non-owned tables.
**Acceptance evidence:** Boundary tests prove consumed events alter only owned projections and statuses, contract docs enumerate required fields and idempotency behavior, and release evidence shows policy-change re-evaluation on affected bills.

### 46. Release evidence scenario matrix
**Justification:** Release evidence is only credible if it covers the billing situations that actually trigger defects and regulatory complaints.
**Improvement:** Expand `RELEASE_EVIDENCE.md` expectations into a scenario matrix covering normal actual reads, repeated estimates, meter exchange, move-in, move-out, tariff change, rebill, protected-customer moratorium, payment reversal, dispute, and batch bill-run completion.
**Acceptance evidence:** A maintained scenario checklist ties each case to tests, UI screenshots, event traces, and calculation evidence, and no release is marked ready without complete coverage for the matrix.

### 47. Realistic seed data and reference data packs
**Justification:** Billing defects hide when development data does not resemble real service-point, tariff, and meter diversity.
**Improvement:** Provide seed data for residential, commercial, industrial, prepaid-like boundary cases, multi-register meters, vacant premises, protected customers, and mixed tariff zones, plus reference calendars, units, and reason-code dictionaries.
**Acceptance evidence:** Seed-data tests confirm the package can bootstrap representative tenants, workbench screenshots show varied operating states, and release evidence identifies which scenario uses which seed bundle.

### 48. Batch billing, close-window, and SLA evidence
**Justification:** Utilities run billing in cycles and need proof that batch performance holds under operational load.
**Improvement:** Add performance evidence for mass read ingestion, interval validation, bill simulation, bill issuance, rebill reruns, and queue refreshes, with explicit SLAs for cycle close and exception backlog clearance.
**Acceptance evidence:** Performance test reports capture throughput and latency for batch workloads, workbench metrics expose SLA attainment, and release evidence includes a representative billing-cycle close run.

### 49. Multi-tenant, jurisdiction, and audit-proof evidence
**Justification:** Billing data is sensitive and often segregated by utility, municipality, or regulator.
**Improvement:** Strengthen evidence that tenant isolation, jurisdiction-specific rule packs, audit hashes, and permission boundaries all hold when similar service points and accounts exist in parallel tenants.
**Acceptance evidence:** Isolation tests prove no cross-tenant leakage in APIs, UI, or events, audit-proof manifests seal calculation and approval traces, and release evidence includes side-by-side tenant scenarios with different rule packs.

### 50. Go-live cutover and hypercare evidence
**Justification:** Billing programs fail at launch when migration, reconciliation, and first-cycle support are under-specified.
**Improvement:** Add a production-readiness checklist for legacy account and meter migration, opening balance reconciliation, first-bill comparison, exception war-room queues, operator training on the workbench, and hypercare exit criteria after the first successful cycle.
**Acceptance evidence:** Cutover rehearsal outputs reconcile legacy and new bill totals within agreed thresholds, first-cycle dashboards show open exception volume and aging, and release evidence includes signed-off go-live and hypercare completion artifacts.
