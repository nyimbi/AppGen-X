# Asset Lifecycle PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `asset_lifecycle`. The items are specific to fixed asset operations: acquisition, capitalization, componentization, book assignment, placed-in-service control, depreciation, transfers, revaluation, impairment, maintenance-life adjustment, insurance, warranty, physical verification, retirement, disposal, audit proof, and agent-assisted asset accounting work.

## Current Domain Evidence Used

- Domain purpose: fixed asset operations from acquisition intent through capitalization, componentization, book assignment, placed-in-service control, depreciation, transfer, revaluation, impairment, maintenance-life adjustment, insurance, warranty, physical verification, retirement, disposal proceeds, audit proof, federation, identity evidence, controls, rules, parameters, configuration, workbench fragments, and release evidence.
- Owned boundary: fixed assets, components, component history, books, book assignments, acquisitions, capitalization, right-of-use assets, depreciation schedules/lines/runs/journals, transfers, valuation adjustments, impairment indicators, maintenance adjustments, insurance/warranty, claims, retirement, disposal proceeds, physical verification, location/custodian/cost-center history, policy screening, audit proofs, federation, identity credentials, carbon utilization, portfolio optimization, allocation mechanisms, anomaly signals, risk models, seed data, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: asset registration, placed-in-service, depreciation schedules, depreciation runs, transfers, revaluations, impairments, maintenance adjustments, retirements, event inbox, asset search, asset risk, rules, parameters, schema extensions, configuration, and workbench views.
- Existing events and dependencies: emits `AssetRegistered`, `AssetPlacedInService`, `DepreciationCalculated`, `AssetTransferred`, `AssetRevalued`, `AssetImpaired`, `MaintenanceAdjustedAssetLife`, and `AssetRetired`; consumes purchase receipt, maintenance, insurance, tax book, and access-policy events through AppGen-X projections and declared APIs only.

## 50 Better-Than-World-Class Improvements

### 1. Acquisition-to-asset traceability

**Justification:** Fixed asset accuracy begins before capitalization. Purchase receipts, invoices, projects, construction-in-progress, and acquisition approvals must be traceable to the resulting asset.

**Improvement:** Add acquisition trace records linking purchase receipt projections, supplier invoice references, project/CIP references, acquisition amount, intended category, capitalization decision, and final fixed asset. The workbench should show unresolved acquisition candidates and duplicate capitalization risks.

### 2. Capitalization policy compiler

**Justification:** Capitalization depends on threshold, asset class, useful life, entity policy, tax book, project status, and expense-versus-capital judgment.

**Improvement:** Compile capitalization rules with thresholds, asset categories, component rules, expense exceptions, approval levels, and effective dates. Every capitalization should store the rule version, failed tests, and human override reason.

### 3. Asset identity and tag governance

**Justification:** Assets need stable physical and digital identities across labels, serials, IoT tags, locations, custodians, and external registers.

**Improvement:** Add identity profiles with asset tag, serial, manufacturer, model, digital credential, physical label status, duplicate tag detection, and identity proof. Block service placement when identity evidence is incomplete for controlled asset classes.

### 4. Componentization decision engine

**Justification:** Major assets often contain components with different useful lives, depreciation methods, maintenance patterns, and retirement paths.

**Improvement:** Add componentization rules that split cost by component, useful life, book, location, and replacement policy. Store parent-child topology, capitalization basis, and component history for partial retirement and replacement.

### 5. Multi-book asset accounting

**Justification:** Assets commonly require corporate, statutory, tax, management, grant, and regulatory books with different methods and calendars.

**Improvement:** Expand book assignment with book purpose, currency, calendar, depreciation method, convention, useful life, residual value, tax class, and effective dates. Workbench views should compare book values and exceptions across books.

### 6. Placed-in-service control

**Justification:** Depreciation and capitalization should not begin until an asset is available for intended use and required evidence is complete.

**Improvement:** Add service-readiness checks for acquisition evidence, location, custodian, book assignment, cost center, insurance requirement, verification tag, and approval. Emit `AssetPlacedInService` only after checks pass or an approved exception exists.

### 7. Depreciation method library

**Justification:** Straight-line alone is insufficient; asset accounting needs declining balance, units-of-production, sum-of-years, tax methods, and custom schedules.

**Improvement:** Add method descriptors with formula, convention, rounding, partial-period policy, residual value handling, useful-life rule, and book eligibility. Generate tests for every method and schedule line.

### 8. Depreciation schedule versioning

**Justification:** Changes to cost, life, residual value, method, service date, or impairment require schedule revision without erasing history.

**Improvement:** Version schedules with reason, source event, old/new assumptions, recalculation policy, affected periods, catch-up amount, and approval. Preserve prior schedule lines for audit.

### 9. Depreciation run idempotency and proof

**Justification:** Depreciation runs can create material duplicate journals if retried unsafely.

**Improvement:** Add run-level idempotency keys, included books, included assets, excluded assets, calculated totals, journal handoff proof, retry state, and reversal handling. Duplicate runs should return prior evidence rather than recalculating.

### 10. Depreciation journal reconciliation

**Justification:** Asset subledger depreciation must reconcile to GL postings by book, entity, cost center, and period.

**Improvement:** Add reconciliation records comparing depreciation schedule totals, run totals, journal events, and GL projection acknowledgements. Surface unreconciled depreciation as close blockers.

### 11. Asset transfer lifecycle

**Justification:** Transfers affect location, custodian, cost center, entity, depreciation responsibility, insurance, and sometimes tax.

**Improvement:** Add transfer workflows with requested/current/future location, custodian, cost center, entity, effective date, approval, physical movement evidence, book impact, and intercompany implications.

### 12. Custodian accountability controls

**Justification:** Asset custodianship determines physical accountability, verification, loss reporting, and handover.

**Improvement:** Add custodian assignment history with acceptance, delegation, handover, lost/stolen report, and overdue acknowledgement. The workbench should expose assets with stale or missing custodian confirmation.

### 13. Location hierarchy and geofence evidence

**Justification:** Asset location matters for insurance, tax, maintenance, verification, and impairment.

**Improvement:** Model location hierarchy, allowed asset classes, geofence proof, movement rules, and verification cadence. Transfers to restricted or unverified locations should require approval.

### 14. Cost center and project assignment rules

**Justification:** Depreciation expense and asset responsibility depend on valid cost center/project assignments.

**Improvement:** Add account-combination rules for asset category, book, cost center, project, entity, and period. Validate assignments before service, transfer, depreciation, and retirement.

### 15. Lease right-of-use asset depth

**Justification:** Right-of-use assets need lease term, liability, reassessment, modification, impairment, and disclosure evidence.

**Improvement:** Add lease component records with commencement date, term, discount rate, liability link, payment schedule, reassessment triggers, modification history, and depreciation treatment by book.

### 16. Construction-in-progress conversion

**Justification:** CIP assets accumulate cost over time and convert into one or many fixed assets when ready.

**Improvement:** Add CIP work-in-progress records, accumulated cost, project milestones, capitalization candidate assets, split rules, placed-in-service evidence, and residual CIP reconciliation.

### 17. Maintenance-driven useful-life adjustment

**Justification:** Major maintenance, overhaul, refurbishment, or damage changes useful life, residual value, and impairment risk.

**Improvement:** Link maintenance completion projections to useful-life assessment, component replacement, capitalizable maintenance, impairment indicator, schedule revision, and audit explanation. Require approval for material life changes.

### 18. Repair-versus-capitalize decision support

**Justification:** Maintenance spend can be expense, capitalize, component replacement, impairment, or life-extension depending on facts and policy.

**Improvement:** Add decision records using maintenance description, cost, asset class, component affected, expected benefit, policy rule, and accounting recommendation. The agent should draft evidence-backed decisions for review.

### 19. Revaluation model governance

**Justification:** Revaluation affects carrying amount, reserves, depreciation, impairment, and financial statements.

**Improvement:** Add revaluation basis, valuation source, appraiser evidence, fair-value hierarchy, book eligibility, reserve impact, depreciation reset, approval, and disclosure proof. Store rejected valuation alternatives.

### 20. Impairment indicator lifecycle

**Justification:** Market, usage, damage, obsolescence, regulation, and performance signals can trigger impairment review.

**Improvement:** Add impairment indicators with source, severity, affected cash-generating unit, recoverable amount evidence, value-in-use/fair-value basis, recommended adjustment, and closure state.

### 21. Impairment testing workbench

**Justification:** Impairment testing requires assumptions, recoverable amount, carrying amount, sensitivities, approvals, and journal evidence.

**Improvement:** Add testing records with asset group, carrying value, cash-flow assumptions, discount rate, fair-value estimate, impairment amount, reversal eligibility, and disclosure notes.

### 22. Insurance coverage adequacy

**Justification:** Assets may be uninsured, underinsured, overinsured, excluded, or outside policy location.

**Improvement:** Compare asset value, class, location, and risk to insurance policy projections. Flag coverage gaps, expired policies, excluded assets, deductibles, and required claim documentation.

### 23. Warranty tracking and claim triggers

**Justification:** Warranty recovery is lost when coverage, failure events, and claim deadlines are not tracked.

**Improvement:** Add warranty terms, covered components, expiry, claim threshold, maintenance/failure linkage, vendor evidence, and claim deadline alerts. Agent workflows should draft warranty claim packets.

### 24. Insurance claim lifecycle

**Justification:** Asset losses and damage require claim preparation, insurer communication, proceeds, repair, impairment, or retirement decisions.

**Improvement:** Add claim records with incident, asset/component, policy, estimated loss, claim amount, documents, adjuster status, proceeds, deductible, accounting treatment, and closure proof.

### 25. Physical verification planning

**Justification:** Physical counts must be risk-based and planned by asset class, location, custodian, materiality, and prior exceptions.

**Improvement:** Add verification plans with scope, sampling method, scan method, due dates, assigned teams, expected assets, and risk weighting. Generate count sheets and mobile scan tasks.

### 26. Physical verification exception management

**Justification:** Missing, extra, moved, damaged, duplicate-tagged, or custodian-mismatched assets require structured resolution.

**Improvement:** Add exception categories, evidence, owner, proposed resolution, financial impact, insurance impact, approval, and follow-up verification. unresolved material exceptions should block close where policy requires.

### 27. Asset retirement decision governance

**Justification:** Retirement can result from sale, scrap, loss, theft, donation, exchange, obsolescence, or destruction, each with different accounting.

**Improvement:** Add retirement reason, method, approval, final book value, accumulated depreciation, impairment, proceeds expectation, tax treatment, and required disposal evidence before retirement posting.

### 28. Disposal proceeds and gain/loss proof

**Justification:** Disposal gain or loss must reconcile proceeds, carrying value, costs, tax, and GL handoff.

**Improvement:** Add proceeds records with receipt, buyer, amount, currency, sale costs, tax, settlement date, carrying value, gain/loss calculation, and journal proof.

### 29. Partial retirement and component replacement

**Justification:** Components may be replaced while the parent asset remains in service.

**Improvement:** Add partial retirement logic for component cost, accumulated depreciation, replacement capitalization, gain/loss, and updated component topology. Preserve parent asset continuity.

### 30. Asset impairment and retirement fraud controls

**Justification:** Asset write-downs, retirements, and disposals can hide theft, unauthorized sale, or manipulation.

**Improvement:** Add anomaly signals for unusual retirements, repeated location exceptions, low proceeds, rapid impairment after acquisition, custodian conflicts, and duplicate tags. Route findings to control assertions and approvals.

### 31. Carbon utilization and sustainability evidence

**Justification:** Assets increasingly require utilization, energy, emissions, and sustainability reporting.

**Improvement:** Add carbon utilization records with asset class, usage window, energy source, intensity, operating schedule, and reporting allocation. Link high-emission assets to replacement/optimization scenarios.

### 32. Portfolio optimization for repair, replace, retain

**Justification:** Asset strategy depends on value, maintenance cost, downtime, energy, risk, residual value, and replacement alternatives.

**Improvement:** Add optimization scenarios comparing repair, replace, retain, sell, lease, or retire options with NPV, risk, downtime, carbon, tax, and accounting impacts.

### 33. Shared asset allocation mechanism

**Justification:** Shared assets must allocate usage, cost, depreciation, and capacity across departments or entities.

**Improvement:** Add allocation rules using usage meters, bookings, capacity, cost center bids, entity shares, and clearing accounts. Store allocation evidence and disputes.

### 34. Asset risk model governance

**Justification:** Useful-life, impairment, failure, and portfolio models affect accounting and operations.

**Improvement:** Govern models with feature lineage, training data class, drift, explainability, fallback rules, materiality, and review state. Require human approval for material accounting recommendations.

### 35. Asset audit proof bundles

**Justification:** Auditors need proof of existence, ownership, valuation, depreciation, transfer, and retirement without full operational data exposure.

**Improvement:** Generate disclosure-minimized proof bundles for asset existence, book value, depreciation run, physical verification, impairment, and retirement. Include verifier instructions and proof expiry.

### 36. Asset federation contracts

**Justification:** Asset data may exist in procurement, maintenance, insurance, tax, and external registers, but this PBC must not share tables.

**Improvement:** Add federation contracts with source, projection freshness, trust level, allowed use, reconciliation method, and stale-data behavior. Workbench should flag stale or conflicting projections.

### 37. Asset identity credential lifecycle

**Justification:** High-value assets need verifiable identity and ownership claims across internal and external systems.

**Improvement:** Add asset credentials with issuer, subject, claim type, validity, revocation status, and verification evidence. Link credentials to acquisition, transfer, insurance, and disposal workflows.

### 38. Tax book alignment

**Justification:** Tax books and corporate books often differ in methods, lives, bonus depreciation, and recapture rules.

**Improvement:** Consume tax book projections and compare tax/corporate book assignments, depreciation, retirements, and revaluations. Flag mismatches and required tax disclosures.

### 39. Asset close cockpit

**Justification:** Period close requires depreciation, transfers, impairments, retirements, physical verification, and GL handoff visibility.

**Improvement:** Add a close cockpit with depreciation run status, unposted journals, new assets not in service, pending transfers, impairment reviews, retirement approvals, verification exceptions, and reconciliation status.

### 40. Depreciation forecast and budget view

**Justification:** Finance needs future depreciation expense by book, entity, cost center, project, and asset class.

**Improvement:** Add forecast projections from schedules, planned acquisitions, retirements, impairments, and life changes. Include confidence and scenario assumptions.

### 41. Asset bulk import and migration controls

**Justification:** Asset registers are often migrated or corrected in bulk, creating high risk of duplicate, invalid, or unbalanced records.

**Improvement:** Add staged import batches with validation, duplicate detection, capitalization policy checks, book assignment checks, sampling approval, partial failure handling, and rollback/correction events.

### 42. Asset rules and parameter simulation

**Justification:** Capitalization thresholds, impairment thresholds, verification intervals, batch sizes, and retirement limits materially change operations.

**Improvement:** Simulate rule/parameter changes against historical and open assets, showing changed capitalization, depreciation, impairment reviews, verification workload, retirement approvals, and close blockers.

### 43. Agent-safe capitalization assistance

**Justification:** The asset chatbot can help classify acquisitions, but capitalization decisions affect financial statements.

**Improvement:** Require agent previews with source receipt, suggested asset category, capitalization rule, component split, useful life, book assignments, policy exceptions, and approval route. Agent actions should create drafts only.

### 44. Agent-safe depreciation and valuation actions

**Justification:** Depreciation, revaluation, and impairment actions are financially material and must be controlled.

**Improvement:** Define agent competencies for depreciation explanation, schedule simulation, impairment recommendation, and revaluation review. Require human approval for postings or carrying-value changes.

### 45. Agent-safe physical verification support

**Justification:** Agents can assist verification planning and exception triage but should not silently resolve existence exceptions.

**Improvement:** Add agent workflows for count-plan drafting, scan evidence summarization, exception grouping, custodian outreach, and remediation proposals with confirmation gates for financial changes.

### 46. Workbench coverage for all asset operations

**Justification:** Asset specialists need direct UI access to lifecycle operations, not hidden backend records.

**Improvement:** Expand UI into acquisition queue, capitalization workbench, asset register, component topology, book/depreciation console, transfer board, valuation/impairment panel, maintenance-life view, insurance/warranty, verification, retirement/disposal, close cockpit, risk, and agent panels.

### 47. Continuous asset controls

**Justification:** Asset controls should run continuously for existence, completeness, depreciation, valuation, and authorization.

**Improvement:** Add control assertions for untagged assets, assets not placed in service, depreciation omissions, stale useful life, expired insurance, overdue verification, missing custodian, unusual retirement, and GL reconciliation.

### 48. Boundary proof for asset-only ownership

**Justification:** Asset lifecycle must integrate with procurement, maintenance, insurance, tax, GL, identity, and audit without reading their tables.

**Improvement:** Add static/runtime checks proving every command uses only asset-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 49. Asset release readiness score

**Justification:** Users need a concise measure of whether asset lifecycle is complete enough for production fixed asset accounting.

**Improvement:** Compute readiness from acquisition traceability, capitalization controls, book coverage, depreciation proof, transfer governance, valuation controls, verification status, retirement controls, GL/tax/insurance handoffs, UI coverage, boundary proof, and agent safety.

### 50. End-to-end asset lifecycle trace

**Justification:** Asset accounting excellence requires tracing each asset from acquisition through service, depreciation, transfers, maintenance, verification, valuation, insurance, and retirement.

**Improvement:** Build an end-to-end trace view using asset-owned records and declared projections. The agent should answer asset status, book value, depreciation, location, custodian, and disposal questions from this trace with source evidence.
