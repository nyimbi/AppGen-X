# Reinsurance Management PBC Manual Improvement Backlog

## Purpose

This hand-crafted backlog replaces generic roadmap text for `reinsurance_management` with reinsurance-specific improvements for treaties, facultative placements, cessions, bordereaux, recoverables, claim recoveries, exposure layers, counterparties, settlements, workbench operations, and governed agent assistance.

## Current Domain Evidence Used

- Stable PBC key: `reinsurance_management`.
- Domain purpose: treaties, facultative placements, cessions, recoverables, bordereaux, claims recoveries, and exposure.
- Owned records include `reinsurance_treaty`, `facultative_placement`, `cession`, `bordereau`, `recoverable`, `claim_recovery`, `exposure_layer`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Public APIs include `POST /reinsurance-treatys`, `POST /facultative-placements`, `POST /cessions`, `POST /bordereaus`, `POST /recoverables`, and `GET /reinsurance-management-workbench`.
- Workbench surfaces include `ReinsuranceManagementWorkbench`, `ReinsuranceManagementDetail`, and `ReinsuranceManagementAssistantPanel`.
- AppGen-X events include `ReinsuranceManagementCreated`, `ReinsuranceManagementUpdated`, `ReinsuranceManagementApproved`, and `ReinsuranceManagementExceptionOpened`.

## 50 High-Impact Improvements

### 1. Treaty structure model

**Justification:** Reinsurance treaties differ by quota share, surplus, excess of loss, aggregate stop loss, catastrophe, per-risk, and facultative-obligatory structures.

**Improvement:** Expand `reinsurance_treaty` with treaty type, covered book, lines of business, attachment basis, limits, shares, reinstatements, exclusions, effective period, and wording reference.

**Acceptance evidence:** Tests must validate treaty structures and reject cessions against unsupported treaty types.

### 2. Treaty lifecycle state machine

**Justification:** Treaty management requires draft, quoted, signed, active, suspended, commuted, expired, run-off, cancelled, and archived states.

**Improvement:** Add explicit treaty states with transition reason, evidence, approvals, allowed commands, and AppGen-X event emission.

**Acceptance evidence:** Invalid transition tests must fail and `ReinsuranceManagementWorkbench` must show next allowed actions by treaty state.

### 3. Counterparty and broker boundary

**Justification:** Reinsurers, brokers, cedants, pools, and retrocessionaires must be referenced without becoming master-party ownership.

**Improvement:** Store counterparty projections with role, participation, credit rating, domicile, contact constraints, and freshness.

**Acceptance evidence:** Boundary tests must prove counterparty data is consumed as projection evidence and no external party table is mutated.

### 4. Treaty participation ledger

**Justification:** Multi-participant placements need precise signed shares, order, security, slip references, and capacity changes.

**Improvement:** Add participation lines with reinsurer, broker, signed line, written line, authorization, effective date, and change history.

**Acceptance evidence:** Tests must sum signed shares, detect over-placement, and preserve historical participation.

### 5. Facultative placement workflow

**Justification:** Large or unusual risks require facultative capacity, quotes, subjectivities, signed lines, and placement evidence.

**Improvement:** Expand `facultative_placement` with submission package, market list, quote terms, capacity, subjectivities, bind status, and declinations.

**Acceptance evidence:** Tests must block bind evidence until required signed lines and subjectivities are complete.

### 6. Placement document intake

**Justification:** Slips, cover notes, treaty wording, bordereaux, and claim advice often arrive as documents.

**Improvement:** Add document extraction for limits, shares, effective dates, exclusions, premiums, claims clauses, and settlement terms with confidence and reviewer approval.

**Acceptance evidence:** Tests must require human confirmation before document-derived values update owned records.

### 7. Cession eligibility rules

**Justification:** A policy, exposure, premium, or loss must satisfy treaty scope before being ceded.

**Improvement:** Expand `cession` with source projection, treaty match, inclusion/exclusion rules, attachment test, limit test, territory, line, and effective-date validation.

**Acceptance evidence:** Tests must approve eligible cessions and reject out-of-scope risks with cited rule versions.

### 8. Cession calculation trace

**Justification:** Ceded premium and loss amounts must be reproducible from treaty terms and source amounts.

**Improvement:** Add calculation lines for gross amount, retention, share, layer, reinstatement, commission, tax, and rounding.

**Acceptance evidence:** Tests must reconstruct cession amounts and flag unsupported manual overrides.

### 9. Exposure layer accumulation

**Justification:** Reinsurance protects layers of exposure by peril, geography, line, event, and portfolio.

**Improvement:** Expand `exposure_layer` with attachment, exhaustion, peril, territory, portfolio, aggregation basis, event definition, and utilization.

**Acceptance evidence:** Tests must update layer utilization from cessions and show remaining capacity.

### 10. Catastrophe event tracking

**Justification:** Cat events drive accumulation, notice, recoverables, reinstatements, and aggregate exhaustion.

**Improvement:** Add event projections with event id, peril, occurrence window, affected treaties, gross loss estimate, ceded estimate, and reporting status.

**Acceptance evidence:** Tests must group claims into event windows and calculate affected layers.

### 11. Bordereau schema governance

**Justification:** Premium, loss, exposure, and claims bordereaux need consistent columns, validations, and reconciliation evidence.

**Improvement:** Expand `bordereau` with type, period, schema version, source file, row counts, validation failures, approval, and submission status.

**Acceptance evidence:** Tests must validate bordereau rows and block submission with unresolved rejects.

### 12. Bordereau ingestion quality controls

**Justification:** Bordereaux commonly contain duplicates, missing risk ids, currency mismatches, stale periods, and treaty mismatches.

**Improvement:** Add duplicate detection, period checks, currency validation, treaty mapping, source reconciliation, and reject queues.

**Acceptance evidence:** Tests must isolate bad rows while preserving accepted rows and source evidence.

### 13. Premium bordereau reconciliation

**Justification:** Ceded premium must reconcile to policy and billing projections before settlement.

**Improvement:** Add reconciliation against policy premium projections, billing status, ceded commission, taxes, and prior adjustments.

**Acceptance evidence:** Tests must flag variances and prevent settlement certification until resolved or approved.

### 14. Loss bordereau reconciliation

**Justification:** Ceded losses and expenses must reconcile to claims projections and treaty terms.

**Improvement:** Add loss bordereau checks for claim status, paid, case reserve, allocated expenses, event coding, layer, and deductible treatment.

**Acceptance evidence:** Tests must reject loss lines that exceed treaty scope or stale claims projections.

### 15. Recoverable lifecycle

**Justification:** Recoverables move from estimated to billed, disputed, collected, aged, impaired, written off, or closed.

**Improvement:** Expand `recoverable` with source cession, claim recovery link, amount, currency, due date, counterparty, status, aging, and impairment evidence.

**Acceptance evidence:** Tests must classify recoverables by status and aging bucket.

### 16. Claim recovery workflow

**Justification:** Reinsurance claim recovery requires notices, supporting documents, treaty clauses, reinsurer responses, and cash collection.

**Improvement:** Expand `claim_recovery` with claim projection, notice date, required documentation, submission package, response, dispute, collection, and closure.

**Acceptance evidence:** Tests must block recovery billing without required claim and treaty evidence.

### 17. Reinstatement premium calculation

**Justification:** Excess-of-loss treaties may require reinstatement premium after loss events.

**Improvement:** Add reinstatement records with exhausted limit, reinstatement number, pro-rata factor, premium due, approval, and settlement linkage.

**Acceptance evidence:** Tests must calculate reinstatement premiums from treaty terms and loss utilization.

### 18. Sliding-scale and profit commission

**Justification:** Treaty economics may include ceding commission, profit commission, sliding-scale rates, or no-claims bonuses.

**Improvement:** Add commission terms with basis, formula, loss ratio bands, period, adjustments, and settlement calculation trace.

**Acceptance evidence:** Tests must calculate commissions and preserve formula versions.

### 19. Deposit premium and minimum premium

**Justification:** Treaty settlement may involve deposit, minimum, adjustable, and earned premium calculations.

**Improvement:** Add premium term records with deposit amount, adjustment basis, minimum, reporting frequency, due dates, and true-up handling.

**Acceptance evidence:** Tests must calculate true-ups and flag missed reporting periods.

### 20. Currency and FX governance

**Justification:** Reinsurance programs often span currencies and require agreed exchange dates and rates.

**Improvement:** Add currency rules for treaty currency, source currency, settlement currency, FX source projection, conversion date, and rounding.

**Acceptance evidence:** Tests must reproduce converted ceded amounts and reject missing FX evidence.

### 21. Settlement statement generation

**Justification:** Reinsurance settlements need clear premium, commission, loss, recoverable, cash, and balance-forward lines.

**Improvement:** Add statement records with period, counterparty, treaty, balance, line items, approvals, delivery, and receipt status.

**Acceptance evidence:** Tests must generate statements from accepted bordereaux and recoverables.

### 22. Cash matching boundary

**Justification:** Reinsurance operations need cash collection status but should not own treasury or bank reconciliation.

**Improvement:** Store cash receipt projections, matched statement ids, unmatched differences, and freshness from declared APIs/events.

**Acceptance evidence:** Boundary tests must prove cash data is projected and no treasury table is mutated.

### 23. Collateral and funds-withheld tracking

**Justification:** Some treaties require letters of credit, trusts, funds withheld, or collateral thresholds.

**Improvement:** Add collateral records with type, amount, beneficiary, expiry, threshold, deficiency, renewal, and release conditions.

**Acceptance evidence:** Tests must flag collateral shortfalls and expiring instruments.

### 24. Credit risk monitoring

**Justification:** Reinsurer credit quality affects recoverability, collateral, impairment, and placement decisions.

**Improvement:** Store credit rating projections, watchlist status, exposure by counterparty, recoverable aging, and concentration metrics.

**Acceptance evidence:** Tests must produce counterparty risk alerts when thresholds are breached.

### 25. Commutation workflow

**Justification:** Treaty commutations settle future obligations and require actuarial estimates, negotiation, approval, and accounting handoff.

**Improvement:** Add commutation cases with affected treaties, estimated liabilities, offer terms, approval, settlement status, and release evidence.

**Acceptance evidence:** Tests must close affected recoverables only after approved commutation settlement.

### 26. Treaty wording clause library

**Justification:** Claims and cessions turn on clauses such as hours, exclusions, reporting deadlines, follow-the-fortunes, and loss-occurrence definitions.

**Improvement:** Add clause references with clause type, wording version, applicability, extracted obligations, and linked validations.

**Acceptance evidence:** Tests must cite clause versions in cession and claim-recovery decisions.

### 27. Notice and reporting calendar

**Justification:** Treaties impose notice deadlines, bordereau due dates, cash calls, renewal dates, and termination windows.

**Improvement:** Add calendar obligations with due date, owner, source clause, status, escalation, and proof of submission.

**Acceptance evidence:** Tests must open exceptions for overdue obligations and show them in the workbench.

### 28. Treaty renewal and placement pipeline

**Justification:** Renewals require exposure packs, loss experience, market submissions, quotes, signed lines, and bind evidence.

**Improvement:** Add renewal pipeline with required data, market list, quote comparison, terms changed, signed line status, and handoff to active treaty.

**Acceptance evidence:** Tests must create renewal packages and preserve prior treaty terms.

### 29. Retrocession support

**Justification:** Reinsurers may cede assumed risk onward through retrocession arrangements.

**Improvement:** Add retrocession flagging, assumed/ceded relationship, inward/outward treaty links, and net exposure calculations.

**Acceptance evidence:** Tests must calculate gross, ceded, assumed, and net exposure without shared table access.

### 30. Assumed reinsurance boundary

**Justification:** The PBC may need assumed treaty context while preserving separate policy and claims ownership.

**Improvement:** Add assumed portfolio projections with cedant, period, exposure, premium, loss, and bordereau mapping.

**Acceptance evidence:** Boundary tests must show assumed data enters via declared projection or event contracts.

### 31. Dispute and query management

**Justification:** Reinsurers dispute bordereau rows, recoverables, claims support, wording interpretation, and settlement balances.

**Improvement:** Add dispute records with category, disputed amount, source row, counterparty response, evidence request, owner, and resolution.

**Acceptance evidence:** Tests must hold disputed amounts from settlement certification until resolved.

### 32. Audit-ready treaty file

**Justification:** Reinsurance reviews require treaty wording, slips, signatures, bordereaux, calculations, notices, recoveries, and settlements.

**Improvement:** Add treaty file packet with required document checklist, missing evidence, hash, approval, and export manifest.

**Acceptance evidence:** Tests must generate a treaty file packet and detect missing evidence.

### 33. Exposure bordereau drilldown UI

**Justification:** Analysts need to see why an exposure is attached to a treaty, layer, peril, and counterparty.

**Improvement:** Add workbench drilldowns from exposure layer to cession, source projection, treaty clause, and accumulation bucket.

**Acceptance evidence:** UI tests must expose layer drilldown and stale-projection warnings.

### 34. Recoverable aging workbench

**Justification:** Collections teams need prioritized views of overdue, disputed, impaired, and high-value recoverables.

**Improvement:** Add recoverable queues by counterparty, treaty, age, currency, dispute status, and cash projection.

**Acceptance evidence:** UI tests must show aging buckets and collection actions without raw datastore access.

### 35. Treaty rule and parameter workbench

**Justification:** Reinsurance rules vary by program, treaty, counterparty, period, line, and jurisdiction.

**Improvement:** Add governed editors for treaty matching, bordereau validation, notice deadlines, recoverable aging, collateral thresholds, and approval limits.

**Acceptance evidence:** Tests must validate parameter bounds, approval history, rollback, and runtime effect.

### 36. Agent-assisted treaty extraction

**Justification:** Treaty wording and slips are dense documents with clauses, limits, shares, and obligations.

**Improvement:** Add assistant skills that extract treaty terms, clause obligations, participant shares, and reporting deadlines into governed previews.

**Acceptance evidence:** Tests must require human confirmation and retain source-page evidence for each accepted extraction.

### 37. Agent-assisted bordereau triage

**Justification:** Analysts need help explaining rejects, duplicates, variances, and treaty mismatches.

**Improvement:** Add assistant analysis for failed rows, likely mappings, missing source facts, and recommended remediation tasks.

**Acceptance evidence:** Tests must show assistant recommendations without mutating rows until approved.

### 38. Agent safety restrictions

**Justification:** AI must not silently approve treaties, release recoverables, settle statements, or alter cessions.

**Improvement:** Require agent proposals to declare command, affected records, financial impact, evidence, confidence, approval role, and irreversible-impact flag.

**Acceptance evidence:** Tests must block high-impact agent commands without explicit approval.

### 39. AppGen-X event specialization

**Justification:** Reinsurance composes with policy, claims, accounting, treasury, documents, and risk through events.

**Improvement:** Define typed events for treaty activated, facultative bound, cession accepted, bordereau certified, recoverable billed, recovery collected, and dispute opened.

**Acceptance evidence:** Event tests must verify idempotency keys, retry behavior, dead-letter evidence, and declared dependency usage.

### 40. Point-in-time reinsurance reconstruction

**Justification:** Auditors and disputes require historical treaty, cession, exposure, and recoverable state.

**Improvement:** Add event replay to reconstruct treaty participation, cessions, bordereaux, recoverables, and settlements at a date.

**Acceptance evidence:** Tests must replay owned events and reproduce historical snapshots.

### 41. Cryptographic reinsurance evidence packet

**Justification:** Counterparties, auditors, and regulators may challenge calculations and settlements.

**Improvement:** Add hash-linked packets for treaty terms, cession calculations, bordereau certification, recoverable billing, and settlement statements.

**Acceptance evidence:** Tests must detect altered packet contents and verify packet generation from owned records.

### 42. Large-loss alerting

**Justification:** Large losses can trigger notices, cash calls, reinstatements, collateral, and reserve review.

**Improvement:** Add large-loss thresholds by treaty and counterparty with claim projection intake, alert routing, and required action checklist.

**Acceptance evidence:** Tests must open large-loss tasks when projected losses breach thresholds.

### 43. Aggregate exhaustion monitoring

**Justification:** Aggregate covers and stop-loss treaties require careful erosion tracking.

**Improvement:** Add aggregate exhaustion calculations by period, event, line, and treaty with remaining protection and breach warnings.

**Acceptance evidence:** Tests must update aggregate usage after accepted loss cessions.

### 44. Operational risk scoring

**Justification:** Reinsurance operations need early warning for stale bordereaux, unpaid recoverables, credit risk, missed notices, and exposure concentration.

**Improvement:** Add risk scores with factor explanations, trend, threshold, owner, and workbench queue placement.

**Acceptance evidence:** Tests must calculate scores and expose factor explanations.

### 45. Multi-currency settlement dashboard

**Justification:** Reinsurance settlements span currencies, exchange rates, counterparty balances, and aging.

**Improvement:** Add dashboard views by currency, converted value, FX source, settlement status, and unmatched cash.

**Acceptance evidence:** UI tests must show original and converted amounts with FX evidence.

### 46. Regulatory and statutory reporting support

**Justification:** Reinsurance affects solvency, statutory schedules, concentration, credit-for-reinsurance, and recoverable aging reports.

**Improvement:** Add reporting packages with report type, period, included treaties, recoverables, collateral, certification, and submission evidence.

**Acceptance evidence:** Tests must generate report packages from owned records and projections.

### 47. Release smoke scenarios

**Justification:** Generated apps need evidence that realistic reinsurance workflows execute after composition.

**Improvement:** Add smoke scenarios for treaty setup, facultative placement, cession calculation, bordereau certification, recoverable billing, claim recovery, and settlement.

**Acceptance evidence:** Release evidence must show owned records, AppGen-X events, UI artifacts, and boundary checks for each scenario.

### 48. Cross-PBC boundary proof

**Justification:** Reinsurance touches policy, claims, accounting, treasury, documents, risk, and counterparty domains without owning them.

**Improvement:** Add automated proof that generated models, services, routes, handlers, projections, and agent commands use only owned tables plus declared APIs/events.

**Acceptance evidence:** Tests must fail on undeclared table references and pass for declared projection or event dependency references.

### 49. Treaty profitability analytics

**Justification:** Reinsurance teams need view of ceded premium, losses, commissions, expenses, recoverables, and net benefit.

**Improvement:** Add profitability views by treaty, layer, counterparty, line, period, event, and portfolio.

**Acceptance evidence:** Tests must calculate profitability metrics from accepted cessions, recoveries, and settlement data.

### 50. Treaty command center

**Justification:** Users need one surface for treaty status, obligations, cessions, bordereaux, recoverables, disputes, exposure, and agent guidance.

**Improvement:** Add command center with treaty summary, next obligations, exposure utilization, recoverable aging, disputes, settlement status, and assistant panel.

**Acceptance evidence:** UI tests must expose treaty command context and governed actions without raw datastore access.
