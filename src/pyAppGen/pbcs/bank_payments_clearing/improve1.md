# Bank Payments Clearing PBC Manual Improvement Backlog

## Purpose

This strict backlog replaces scaffold-derived roadmap material for `bank_payments_clearing` with a hand-curated payments operations roadmap. The PBC owns payment instructions, clearing batches, settlement files, return items, exception cases, bank reconciliation, participant banks, governed rules, agent assistance, and release evidence without owning customer accounts, sanctions master data, fraud case management, or general ledger tables.

## Current Domain Evidence Used

- Stable PBC key: `bank_payments_clearing`.
- Domain purpose: ACH, wire, real-time payment, card settlement, clearing files, exceptions, and bank reconciliation.
- Owned domain tables: `payment_instruction`, `clearing_batch`, `settlement_file`, `return_item`, `exception_case`, `bank_reconciliation`, `participant_bank`, `bank_payments_clearing_policy_rule`, `bank_payments_clearing_runtime_parameter`, `bank_payments_clearing_schema_extension`, `bank_payments_clearing_control_assertion`, `bank_payments_clearing_governed_model`.
- Public APIs: `POST /payment-instructions`, `POST /clearing-batchs`, `POST /settlement-files`, `POST /return-items`, `POST /exception-cases`, `GET /bank-payments-clearing-workbench`.
- Emitted AppGen-X events: `BankPaymentsClearingCreated`, `BankPaymentsClearingUpdated`, `BankPaymentsClearingApproved`, `BankPaymentsClearingExceptionOpened`.
- Consumed AppGen-X events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.

## 50 High-Impact Improvements

### 1. Payment Instruction State Machine

**Justification:** Payment instructions move through validation, screening, release, clearing, settlement, return, cancellation, repair, and reconciliation states.

**Improvement:** Add explicit states for drafted, validated, screened, approved, released, batched, cleared, settled, returned, repaired, canceled, reversed, reconciled, and archived.

**Acceptance evidence:** Tests must reject invalid transitions and preserve every material state change as AppGen-X evidence.

### 2. Payment Rail Classification

**Justification:** Domestic batch, same-day batch, wire, instant, card settlement, internal transfer, and cross-border rails have different cutoffs, message fields, risk, and settlement behavior.

**Improvement:** Add rail type, scheme profile, cutoff calendar, settlement basis, message format, value limits, supported currency, and repair rules to `payment_instruction`.

**Acceptance evidence:** Tests must evaluate the same payment facts differently by rail and show the applied rail profile.

### 3. Participant Bank Registry

**Justification:** Routing, settlement, returns, and exception handling depend on participant bank status and capabilities.

**Improvement:** Expand `participant_bank` with routing identifier, settlement account projection, active windows, supported rails, return contact, cutoffs, and suspension state.

**Acceptance evidence:** Tests must block payments to inactive or unsupported participant banks while preserving historical transactions.

### 4. Beneficiary and Originator Validation

**Justification:** Payment quality depends on names, account identifiers, routing identifiers, address, purpose, and originator authority.

**Improvement:** Add validation profiles for required parties, account format, routing checksum, purpose code, originator authorization, and beneficiary repair state.

**Acceptance evidence:** Tests must reject malformed instructions and route repairable party-data issues to exception queues.

### 5. Limits and Velocity Controls

**Justification:** Payments need configurable controls by rail, participant, value, currency, originator type, and risk.

**Improvement:** Add limit definitions, daily/transaction caps, velocity window, approval tier, override reason, and breach exception.

**Acceptance evidence:** Tests must enforce limits and require elevated approval for overrides.

### 6. Payment Screening Boundary

**Justification:** Sanctions, AML, and fraud systems may own screening, while clearing must store decision evidence and freshness.

**Improvement:** Represent screening result, score, match reason, projection freshness, hold/release decision, and override evidence as declared dependencies.

**Acceptance evidence:** Boundary tests must fail on direct sanctions or fraud table access and pass on declared event/API projections.

### 7. Clearing Batch Assembly

**Justification:** Batch rails require grouping by rail, participant, cutoff, effective date, currency, priority, and settlement window.

**Improvement:** Expand `clearing_batch` with batch profile, inclusion rules, totals, item count, hash total, cutoff, release approval, and finalization lock.

**Acceptance evidence:** Tests must assemble batches idempotently and reject additions after finalization.

### 8. Cutoff and Calendar Management

**Justification:** Payment timing depends on bank holidays, rail windows, participant cutoffs, daylight saving, and emergency closures.

**Improvement:** Add calendars with jurisdiction, rail, participant override, cutoff time, extension approval, and missed-window behavior.

**Acceptance evidence:** Tests must calculate next eligible clearing window and explain missed-cutoff rerouting.

### 9. Settlement File Generation

**Justification:** Settlement files require exact totals, sequence numbers, control records, encryption/signature evidence, and transmission status.

**Improvement:** Expand `settlement_file` with file sequence, rail profile, control total, item hash, generated checksum, signature, transmission channel, and acknowledgement.

**Acceptance evidence:** Tests must generate files with reproducible totals and detect altered file content.

### 10. Settlement Acknowledgement Handling

**Justification:** Clearing is incomplete until acknowledgement, acceptance, rejection, or partial processing is reconciled.

**Improvement:** Add acknowledgement type, received time, accepted count, rejected count, reason, linked batch, and repair/resubmit path.

**Acceptance evidence:** Tests must handle accepted, rejected, duplicate acknowledgement, and partial acceptance scenarios.

### 11. Return Item Lifecycle

**Justification:** Returned payments require reason code, effective date, time limit, original instruction, customer impact, and repair/reversal options.

**Improvement:** Expand `return_item` with return reason, original item link, return deadline, financial impact, repair eligibility, representment state, and notification requirement.

**Acceptance evidence:** Tests must process administrative, insufficient funds, unauthorized, closed account, and late return cases.

### 12. Exception Case Taxonomy

**Justification:** Payment exceptions vary by validation, screening, liquidity, participant, file, acknowledgement, return, reconciliation, and operational outage.

**Improvement:** Expand `exception_case` with type, severity, owner, deadline, financial exposure, blocked items, remediation action, and closure evidence.

**Acceptance evidence:** Tests must route each exception type to the correct queue and prevent closure without evidence.

### 13. Repair Queue Workflow

**Justification:** Many payment issues can be repaired without cancellation if authorized and auditable.

**Improvement:** Add repairable fields, maker/checker approval, original value, corrected value, reason, customer notification, and rescreening requirement.

**Acceptance evidence:** Tests must require dual approval for material repairs and preserve original values.

### 14. Cancellation and Recall Handling

**Justification:** Payment cancellation and recall feasibility depends on rail status, cutoff, settlement stage, participant response, and legal constraints.

**Improvement:** Add cancellation request, eligibility, deadline, recall message, participant response, final outcome, and customer communication.

**Acceptance evidence:** Tests must distinguish cancellable, recall-only, too-late, and participant-rejected outcomes.

### 15. Liquidity and Settlement Funding Checks

**Justification:** Released batches can fail if settlement funding is insufficient or liquidity buffers are breached.

**Improvement:** Add liquidity projection, prefunding requirement, settlement account balance evidence, buffer threshold, and release hold.

**Acceptance evidence:** Tests must block or warn on releases when liquidity projections are stale or below threshold.

### 16. Bank Reconciliation Matching

**Justification:** Payment clearing must reconcile instructions, batches, settlement files, acknowledgements, bank statements, fees, and returns.

**Improvement:** Expand `bank_reconciliation` with match type, matched records, tolerance, unmatched amount, aging, break reason, and resolution action.

**Acceptance evidence:** Tests must match one-to-one, many-to-one, fee, return, and unmatched statement scenarios.

### 17. Nostro and Internal Account Boundary

**Justification:** Clearing uses account balances and statements but should not own account ledgers or GL postings.

**Improvement:** Store statement and balance projection evidence with freshness, account identifier, source, and reconciliation result.

**Acceptance evidence:** Boundary tests must fail on direct ledger table writes and pass on emitted reconciliation/settlement events.

### 18. Fee and Charge Evidence

**Justification:** Payment fees, correspondent charges, scheme charges, and participant fees affect reconciliation and customer billing.

**Improvement:** Add fee type, amount, currency, payer, waiver, statement evidence, and downstream billing event.

**Acceptance evidence:** Tests must reconcile explicit and deducted fees without mutating billing tables.

### 19. Operational Risk Controls

**Justification:** Payment operations require controls over dual approval, segregation, limits, file integrity, exception aging, and reconciliation breaks.

**Improvement:** Add control assertions with population, threshold, failing items, owner, remediation, recurrence, and closure evidence.

**Acceptance evidence:** Tests must open control failures and require remediation proof.

### 20. Maker-Checker Authorization

**Justification:** High-risk payment changes require separation between creator, approver, releaser, and repairer.

**Improvement:** Add role constraints, approval tiers, conflict checks, delegation, and emergency override evidence.

**Acceptance evidence:** Tests must reject self-approval and unauthorized release.

### 21. Payment Message Validation

**Justification:** Rail messages have required fields, conditional rules, code lists, and semantic constraints.

**Improvement:** Add message schema profiles, field rules, conditional validation, code-list versions, and canonical-to-rail mapping evidence.

**Acceptance evidence:** Tests must validate complete, malformed, conditionally invalid, and backward-compatible message versions.

### 22. Duplicate Payment Prevention

**Justification:** Duplicate release can create financial loss and customer harm.

**Improvement:** Add duplicate scoring across originator, beneficiary, amount, currency, value date, purpose, reference, and source idempotency key.

**Acceptance evidence:** Tests must block exact duplicates and route near duplicates to review.

### 23. Real-Time Payment Finality

**Justification:** Instant rails often have irreversible or near-final settlement semantics.

**Improvement:** Add finality state, timeout handling, uncertain outcome queue, participant status polling, and customer messaging.

**Acceptance evidence:** Tests must handle success, reject, timeout-unknown, late confirmation, and duplicate retry safely.

### 24. Card Settlement Batch Support

**Justification:** Card settlement includes presentments, chargebacks, interchange, fees, and settlement files distinct from account-to-account rails.

**Improvement:** Add card settlement cycle, merchant batch projection, presentment totals, chargeback link, fee evidence, and settlement variance.

**Acceptance evidence:** Tests must reconcile card settlement totals and route chargeback-linked variances.

### 25. Cross-Border Payment Controls

**Justification:** Cross-border payments require currency, correspondent routing, purpose, regulatory reporting, fees, and sanctions evidence.

**Improvement:** Add correspondent chain, FX projection, purpose code, regulatory report flag, charge bearer, and country-specific validation.

**Acceptance evidence:** Tests must evaluate cross-border instructions by jurisdiction and currency without owning FX or compliance tables.

### 26. FX Rate Boundary

**Justification:** Payments may need FX rates while treasury or markets systems own rates.

**Improvement:** Store FX quote projection, rate timestamp, spread, expiry, source, and stale-rate behavior as declared dependency evidence.

**Acceptance evidence:** Tests must block stale FX payments and emit FX-used evidence without writing rate tables.

### 27. Customer Notification Events

**Justification:** Payment acceptance, rejection, return, repair, cancellation, and settlement need customer communication.

**Improvement:** Emit notification events with template, recipient projection, channel preference, deadline, and source evidence.

**Acceptance evidence:** Contract tests must prove notifications are emitted through AppGen-X and no notification tables are directly modified.

### 28. Payment Operations Workbench

**Justification:** Operators need queues by risk and next action, not raw payment lists.

**Improvement:** Add workbench views for validation fails, screening holds, pending approvals, cutoff risk, batch release, file acknowledgements, returns, reconciliation breaks, and stale dependencies.

**Acceptance evidence:** UI tests must prove each queue maps to owned data or declared projections with permission-aware actions.

### 29. Agent-Assisted Payment Investigation

**Justification:** Payment staff need concise explanations of payment status, exceptions, returns, and reconciliation breaks.

**Improvement:** Add agent skills for payment status summary, return explanation, repair recommendation, reconciliation break analysis, and cutoff impact summary with citations.

**Acceptance evidence:** Tests must require evidence citations and confirmation before any payment mutation.

### 30. Governed Agent CRUD Commands

**Justification:** The chatbot should help operate payment records without silently moving money.

**Improvement:** Add command previews for approve payment, hold payment, release batch, repair instruction, open exception, close reconciliation break, and initiate recall.

**Acceptance evidence:** Intent tests must require payment identity, action, evidence, preview, confirmation, authority, and audit trail.

### 31. Participant Bank Health Monitoring

**Justification:** Participant outages, rejects, or delayed acknowledgements affect clearing risk.

**Improvement:** Add participant health metrics, acknowledgement latency, reject rate, outage state, fallback rule, and escalation owner.

**Acceptance evidence:** Tests must route payments according to participant status and show health reasons.

### 32. Clearing Window Forecast

**Justification:** Operations teams need early warning of missed cutoffs, liquidity shortages, or batch congestion.

**Improvement:** Add forecast metrics from pending items, approval backlog, screening holds, participant status, liquidity, and calendar windows.

**Acceptance evidence:** Tests must produce explainable cutoff risk forecasts.

### 33. Payment Volume and Risk Analytics

**Justification:** Payments leaders need visibility into volume, value, exceptions, returns, rejects, SLA, and reconciliation breaks.

**Improvement:** Add analytics by rail, participant, currency, originator type, exception type, return reason, cutoff miss, and settlement variance.

**Acceptance evidence:** Tests must generate tenant-scoped metrics with source drilldowns.

### 34. Return Reason Trend Analysis

**Justification:** Repeated returns indicate data-quality, customer, participant, or fraud issues.

**Improvement:** Add trend projections for return reason, originator, beneficiary bank, rail, amount band, and recurrence.

**Acceptance evidence:** Tests must open prevention tasks for recurring preventable returns.

### 35. Reconciliation Break Aging

**Justification:** Aging breaks can hide operational loss or settlement issues.

**Improvement:** Add aging buckets, financial exposure, owner, escalation, write-off recommendation, and closure evidence.

**Acceptance evidence:** Tests must escalate aged high-value breaks and reject closure without match or approved write-off evidence.

### 36. Payment File Security Controls

**Justification:** Settlement files require confidentiality, integrity, signing, encryption, and secure transmission evidence.

**Improvement:** Add file encryption status, signature, key version reference, transmission endpoint, checksum, and access log evidence.

**Acceptance evidence:** Tests must block transmission when required security evidence is missing.

### 37. Cyber and Fraud Incident Boundary

**Justification:** Suspicious payment activity may open fraud or cyber cases owned elsewhere.

**Improvement:** Emit investigation events with payment evidence, risk indicators, hold state, and case reference projection.

**Acceptance evidence:** Boundary tests must prove fraud/cyber tables are not directly mutated.

### 38. Regulatory Reporting Triggers

**Justification:** Some payment activity requires operational or regulatory reporting by rail, value, country, purpose, or incident.

**Improvement:** Add report trigger, jurisdiction, report type, deadline, required fields, submission status, and correction history.

**Acceptance evidence:** Tests must create report candidates and track submission evidence.

### 39. Exception Root Cause Analytics

**Justification:** High exception rates should drive process fixes.

**Improvement:** Add root cause categories for customer data, participant outage, rail rule, screening dependency, liquidity, file error, and operator action.

**Acceptance evidence:** Tests must trend root causes and open remediation tasks.

### 40. Replay-Safe Idempotency

**Justification:** Payment event replay must never duplicate movement, files, returns, or notifications.

**Improvement:** Add idempotency keys across instruction intake, batch assembly, file generation, acknowledgement, return processing, and reconciliation.

**Acceptance evidence:** Tests must replay duplicate events with unchanged financial outcomes.

### 41. Dead-Letter and Retry Operations

**Justification:** Payment files, acknowledgements, screening responses, participant updates, and reconciliation inputs can fail.

**Improvement:** Add dead-letter reason, risk, retry count, replay checkpoint, remediation action, and manual release gate.

**Acceptance evidence:** Tests must replay failed events without duplicate payment effects.

### 42. Cryptographic Payment Evidence

**Justification:** Payment disputes and audits need tamper-evident proof of instruction, approval, file, acknowledgement, return, and reconciliation events.

**Improvement:** Add hash chains for payment instructions, approvals, batches, settlement files, acknowledgements, returns, exceptions, and reconciliation outcomes.

**Acceptance evidence:** Tests must verify proof chains and detect altered payloads or reordered events.

### 43. Privacy and Minimum Necessary Views

**Justification:** Payment records include sensitive account, party, and compliance evidence.

**Improvement:** Add redaction profiles for operator, approver, investigator, auditor, participant view, and customer-service view.

**Acceptance evidence:** Permission tests must prove sensitive party, screening, and account data are hidden when not needed.

### 44. Configuration Impact Simulation

**Justification:** Changing limits, cutoffs, screening hold policies, participant status, or repair rules can disrupt payments.

**Improvement:** Add side-effect-free simulations over recent instructions, batches, exceptions, returns, and reconciliation breaks.

**Acceptance evidence:** Tests must produce impact reports before activating high-risk configuration.

### 45. Seeded Payments Scenario Library

**Justification:** Release audits need realistic payments stories.

**Improvement:** Add seeds for clean batch payment, wire approval, instant payment timeout, screening hold, return item, file reject, reconciliation break, recall, and stale liquidity projection.

**Acceptance evidence:** Scenario tests must load side-effect-free and create expected queues, events, and evidence packets.

### 46. Role-Based Permission Model

**Justification:** Payment operators, approvers, release managers, investigators, reconciliation users, liquidity users, and auditors need different authority.

**Improvement:** Add permissions for create, repair, approve, release, cancel, recall, process return, close exception, transmit file, and close reconciliation break.

**Acceptance evidence:** Permission tests must block unauthorized commands and show disabled UI actions.

### 47. Settlement Close and Finance Handoff

**Justification:** Clearing outputs feed finance and treasury but should not own accounting ledgers.

**Improvement:** Emit settlement, fee, return, reconciliation, and unresolved-break events with idempotency keys and evidence references.

**Acceptance evidence:** Contract tests must prove finance handoff events are complete and replay-safe.

### 48. Full Payments Release Simulation

**Justification:** A complete PBC must prove instruction-to-reconciliation behavior end to end.

**Improvement:** Add a simulation where instructions validate, screen, approve, batch, generate settlement files, receive acknowledgements, process returns, reconcile statements, and emit finance handoff events.

**Acceptance evidence:** The simulation must validate owned schema, APIs, services, AppGen-X events, handlers, workbench views, agent skills, permissions, and release evidence.

### 49. Package Overlap Guardrails

**Justification:** This PBC must not duplicate core accounts, fraud, treasury, notification, regulatory reporting, or general ledger ownership.

**Improvement:** Add overlap checks and declared dependency contracts for account balances, screening, FX, liquidity, customer notifications, finance postings, and audit events.

**Acceptance evidence:** Tests must fail on undeclared external table references and pass on declared AppGen-X dependency usage.

### 50. Composition DSL and Unified Agent Exposure

**Justification:** Generated applications must expose payment clearing capabilities through DSL, UI, APIs, and the composed application agent.

**Improvement:** Extend composition metadata for payment instructions, batches, files, returns, exceptions, reconciliations, participant banks, controls, workbench fragments, and agent skills.

**Acceptance evidence:** DSL tests must prove generated apps include payments models, routes, services, event contracts, UI artifacts, and assistant skills without stream-engine picker exposure.
