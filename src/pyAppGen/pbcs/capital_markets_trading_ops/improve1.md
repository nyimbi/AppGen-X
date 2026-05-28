# Capital Markets Trading Operations Improvement Backlog

This backlog is a hand-curated improvement set for the `capital_markets_trading_ops` package. It stays inside the actual trading operations boundary described by the manifest: order capture, execution intake, allocations, confirmations, settlement instructions, trade breaks, position evidence, controls, event/API contracts, operator workbenches, and release assurance.

## Current Domain Evidence Used

- PBC key: `capital_markets_trading_ops`.
- Manifest label: `Capital Markets Trading Operations`.
- Domain description: trade orders, executions, allocations, confirmations, settlement, breaks, positions, and trading operations controls.
- Owned tables in scope: `trade_order`, `execution`, `allocation`, `confirmation`, `settlement_instruction`, `trade_break`, `position_snapshot`, `capital_markets_trading_ops_policy_rule`, `capital_markets_trading_ops_runtime_parameter`, `capital_markets_trading_ops_schema_extension`, `capital_markets_trading_ops_control_assertion`, `capital_markets_trading_ops_governed_model`.
- Workflows in scope: `capital_markets_trading_ops_create_trade_order_workflow` and `capital_markets_trading_ops_record_execution_workflow`.
- Public APIs in scope: `POST /trade-orders`, `POST /executions`, `POST /allocations`, `POST /confirmations`, `POST /settlement-instructions`, and `GET /capital-markets-trading-ops-workbench`.
- UI fragments in scope: `CapitalMarketsTradingOpsWorkbench`, `CapitalMarketsTradingOpsDetail`, and `CapitalMarketsTradingOpsAssistantPanel`.
- Event contracts in scope: emits `CapitalMarketsTradingOpsCreated`, `CapitalMarketsTradingOpsUpdated`, `CapitalMarketsTradingOpsApproved`, `CapitalMarketsTradingOpsExceptionOpened`; consumes `PolicyChanged`, `AuditEventSealed`, and `OperationalKpiChanged`.
- Advanced capability signals in scope: event-sourced operational history, anomaly detection, semantic document intake, predictive risk scoring, counterfactual simulation, cryptographic audit proofs, continuous control testing, cross-PBC event federation, and governed AI agent execution.
- Release surfaces in scope: `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`, `tests/test_contract.py`, and the initial migration.

### 1. Canonical trade order lifecycle
**Justification:** Trading ops teams need an exact lifecycle for an order from draft through release, hold, cancel, replace, completion, and archive or every downstream queue becomes interpretation-heavy.
**Improvement:** Define state and transition rules for `trade_order` that distinguish draft, validated, risk-passed, routed, partially-filled, fully-filled, cancelled, replaced, rejected, and operationally-closed outcomes, with explicit actors and timestamps.
**Acceptance evidence:** Lifecycle transition matrix, invalid-transition tests, workbench status badges, and event emission evidence showing which state changes produce `CapitalMarketsTradingOpsCreated`, `CapitalMarketsTradingOpsUpdated`, or `CapitalMarketsTradingOpsApproved`.

### 2. Order versioning and cancel-replace lineage
**Justification:** Capital markets order flow routinely creates superseded instructions, and operations cannot resolve breaks if cancel-replace chains are flattened into one mutable row.
**Improvement:** Add first-class lineage between original orders, amendments, and replacements so the package can show what changed in quantity, side, limit, destination, account, or trader instruction.
**Acceptance evidence:** Version-chain query examples, cancel-replace fixtures, audit views in `CapitalMarketsTradingOpsDetail`, and release evidence proving downstream executions keep the correct parent order reference.

### 3. Pre-trade reference-data completeness checks
**Justification:** A large share of execution failures begin before the first fill because instrument, account, broker, venue, or settlement standing data is incomplete or stale.
**Improvement:** Validate that every order has resolved instrument identity, trading account, desk, trader, broker or venue target, settlement model, and regulatory classification before it can be routed.
**Acceptance evidence:** Rejection fixtures for missing reference data, operator exception reasons, and evidence that incomplete orders remain visible in the workbench with actionable remediation fields.

### 4. Pre-trade operational risk gates
**Justification:** Operational controls in trading ops are not limited to market risk; they also include fat-finger tolerances, restricted books, blocked counterparties, and incomplete approvals.
**Improvement:** Introduce configurable pre-trade checks for notional thresholds, quantity tolerances, duplicate instruction windows, restricted lists, account funding prerequisites, and missing four-eyes approval.
**Acceptance evidence:** Policy rule examples, blocked-order test scenarios, approval override records, and workbench views that show which specific risk gate stopped release.

### 5. Market data boundary snapshots on order release
**Justification:** Trading ops should consume prices and reference values without mutating or owning the market data domain, but it still needs a frozen view of the data used for decisions.
**Improvement:** Persist a market data snapshot reference on `trade_order` capturing the quote time, source, currency, and tolerance context used for checks and downstream confirmation of expected value.
**Acceptance evidence:** Snapshot linkage tests, stale-quote exception cases, and operator evidence showing when an order was validated against current versus stale market data.

### 6. Partial-fill execution capture
**Justification:** Real execution flow arrives in slices, and the package must distinguish fill-by-fill capture from the parent order’s aggregate status.
**Improvement:** Model `execution` as a sequence of partial and final fills with execution identifiers, venue time, broker time, price, quantity, fees, and source channel so cumulative fill math is explicit.
**Acceptance evidence:** Multi-fill fixtures, cumulative quantity checks, average-price calculations, and workbench drill-down from one order to all linked executions.

### 7. Execution cancel and correction handling
**Justification:** Late broker corrections and exchange cancels create the most dangerous hidden discrepancies because gross activity and net activity diverge.
**Improvement:** Add correction types for busts, price corrections, quantity corrections, and duplicate suppression so each `execution` retains the original record and the corrective event rather than overwriting history.
**Acceptance evidence:** Correct-and-bust test cases, net-versus-gross position proofs, and event history views that show the chain of corrections without ambiguity.

### 8. Allocation eligibility validation
**Justification:** Allocation quality is central to post-trade control because the wrong fund, sleeve, or legal entity assignment turns a good execution into a settlement or compliance problem.
**Improvement:** Validate `allocation` instructions against account eligibility, mandate restrictions, soft and hard limits, settlement model compatibility, and residual allocation policy.
**Acceptance evidence:** Allocation rejection scenarios, account-eligibility fixtures, and supervisor review screens that expose why an allocation cannot proceed.

### 9. Residual and rounding allocation policy
**Justification:** Multi-account fills often create residual shares or cash fragments, and those leftovers need governed handling rather than ad hoc operator judgment.
**Improvement:** Support explicit residual handling rules for `allocation`, including pro-rata, designated account, cash-in-lieu, and round-lot preference policies, with desk-level overrides where justified.
**Acceptance evidence:** Residual-allocation simulations, policy-rule records, and test evidence that rounding decisions remain reproducible across reruns.

### 10. Block trade split auditability
**Justification:** When one block execution is later split across funds or books, the package must preserve the commercial block and the operational distribution as separate but linked facts.
**Improvement:** Add linkage from parent block execution to child `allocation` records with timestamps, allocator identity, reason codes, and post-allocation balance checks.
**Acceptance evidence:** Block-to-child lineage reports, over-allocation prevention tests, and detail views proving every child allocation sums back to the block parent.

### 11. Confirmation channel normalization
**Justification:** Broker and counterparty confirmations arrive through different channels and formats, and the operational queue should normalize them before analysts compare economics.
**Improvement:** Standardize `confirmation` intake from API payloads, files, and document extraction into a consistent structure for economics, parties, settlement dates, commission, and status.
**Acceptance evidence:** Channel-specific parsing fixtures, normalized confirmation samples, and queue evidence showing mixed-source confirmations in one comparable analyst worklist.

### 12. Economic affirmation and mismatch handling
**Justification:** The core confirmation problem is whether economics actually match the booked execution and allocation picture, not whether a message merely arrived.
**Improvement:** Add comparison logic for price, quantity, side, account, settlement date, commission, tax, and counterparty details, with mismatch classes for material and immaterial differences.
**Acceptance evidence:** Match and mismatch test packs, analyst exception queues, and evidence that immaterial differences can be dispositioned without suppressing true breaks.

### 13. Settlement instruction golden-source governance
**Justification:** Settlement instructions are safety-critical data; any ambiguity about which SSI was active for a given market or account drives fails and manual repairs.
**Improvement:** Treat `settlement_instruction` as an effective-dated governed record with activation, expiry, approval, and supersession semantics across account, market, currency, and counterparty dimensions.
**Acceptance evidence:** Effective-date tests, duplicate-active-SSI prevention checks, and workbench evidence that a trade references the exact instruction in force at booking time.

### 14. Market-specific settlement enrichment
**Justification:** Settlement fields vary materially across depositories, custodians, and market models, so a generic SSI structure leaves operators to improvise critical details.
**Improvement:** Add market-aware enrichment for place of settlement, custodian or agent bank, local market account, depository code, payment model, and standing narrative fields where required.
**Acceptance evidence:** Market-specific fixtures, missing-field exception cases, and release evidence showing the package can reject incomplete instructions before they create settlement breaks.

### 15. Fails, penalties, and buy-in workflow
**Justification:** Settlement is not complete when an instruction is sent; the package should continue through failed settlement outcomes and their operational consequences.
**Improvement:** Track settlement status progression from instructed to matched, settled, failed, re-instructed, and resolved, including penalty exposure, buy-in triggers, and accountable owner.
**Acceptance evidence:** Failed-settlement scenarios, aging dashboards, and operator evidence that penalties and escalations remain attached to the original trade context.

### 16. Trade break taxonomy
**Justification:** Break management becomes unmanageable when all discrepancies are stored as one undifferentiated exception type.
**Improvement:** Classify `trade_break` records into booking, allocation, confirmation, settlement, position, cash, fee, corporate action, and external reference-data discrepancies with severity and root-cause fields.
**Acceptance evidence:** Taxonomy definitions, break classification tests, and workbench filters that let analysts separate economic breaks from static-data or workflow breaks.

### 17. Break lineage across lifecycle events
**Justification:** A break should point back to the lifecycle event that caused it or operators cannot tell whether to fix the order, the execution, the allocation, or the settlement instruction.
**Improvement:** Link each `trade_break` to the exact upstream order, execution, allocation, confirmation, or settlement event that introduced the discrepancy and to the remediation action that closed it.
**Acceptance evidence:** End-to-end break lineage fixtures, closure audit trails, and drill-through views from a break to the originating lifecycle event.

### 18. Position snapshot provenance
**Justification:** Position evidence is only useful if operations can explain whether a snapshot was derived from executions, allocations, settlement status, or manual repair.
**Improvement:** Add provenance attributes to `position_snapshot` for source cut, valuation time, data completeness, correction status, and whether the view is intraday provisional or end-of-day affirmed.
**Acceptance evidence:** Snapshot provenance tests, provisional-versus-final examples, and detail screens showing the chain from executions and allocations into position evidence.

### 19. Corporate actions boundary protection
**Justification:** Trading ops must recognize corporate actions impact without swallowing the corporate actions domain and creating duplicated business logic.
**Improvement:** Define explicit boundaries where stock splits, symbol changes, spin-offs, rights issues, and cash dividends can create or explain breaks, but require those events to enter through governed external contracts.
**Acceptance evidence:** Boundary notes in the specification, simulated corporate-action impact cases, and proof that adjustments are traceable to an external event rather than silently recomputed locally.

### 20. Trading calendar and timezone normalization
**Justification:** Cross-market operations fail quietly when trade dates, settlement dates, and cutoff times are interpreted in inconsistent local and venue timezones.
**Improvement:** Normalize order, execution, confirmation, and settlement timestamps against venue timezone, desk timezone, and legal-entity business calendar, including holiday and half-day logic.
**Acceptance evidence:** Calendar fixtures across multiple markets, cutoff-edge test cases, and visible timezone context in detail and workbench views.

### 21. Asset-class-sensitive booking rules
**Justification:** Even within one PBC, equities, fixed income, FX, and listed derivatives carry different operational fields and validation rules.
**Improvement:** Introduce booking profiles that apply different required fields, lifecycle events, and exception tolerances by product type while keeping the package’s surface coherent.
**Acceptance evidence:** Product-specific validation cases, profile configuration evidence, and workbench forms that adapt required fields by product type without collapsing into generic blobs.

### 22. Fee, tax, and commission transparency
**Justification:** Economic agreement is incomplete if analysts cannot see how commissions, fees, taxes, or local charges were expected and then confirmed.
**Improvement:** Capture expected versus confirmed charges on `execution` and `confirmation` records, with break logic for materially different commissions, levies, and stamp duties.
**Acceptance evidence:** Charge comparison fixtures, materiality threshold rules, and analytics showing break rates attributable to fees and taxes rather than core economics.

### 23. Broker, venue, and counterparty boundary modeling
**Justification:** Trading ops works across brokers, venues, and custodians, and each boundary creates separate statuses, acknowledgements, and failure modes.
**Improvement:** Model external party roles explicitly so the package can distinguish executing broker, venue, clearing broker, custodian, and settlement agent responsibilities through the lifecycle.
**Acceptance evidence:** Party-role examples, multi-party workflow tests, and detail views that show which party owns the next operational action.

### 24. Compliance holds and restricted-list workflow
**Justification:** Post-trade operations still needs compliance-sensitive controls because a trade may be captured operationally before all downstream restrictions are cleared.
**Improvement:** Support restricted-list, sanctions, and mandate-breach holds that prevent allocation, confirmation release, or settlement progression until the hold is approved, lifted, or escalated.
**Acceptance evidence:** Hold scenarios, policy-rule records, and workbench queues separating compliance-hold items from ordinary operational backlog.

### 25. Best-execution evidence attachment
**Justification:** Trading operations frequently has to support best-execution review even when the decision occurred earlier on the desk or in another system.
**Improvement:** Add evidence slots for venue choice rationale, quote context, routing notes, and external review references so each order and execution can carry its own best-execution support pack.
**Acceptance evidence:** Evidence attachment tests, immutable evidence references after approval, and release evidence showing best-execution artifacts can be exported for audit.

### 26. Surveillance handoff boundaries
**Justification:** The package should raise suspicious patterns but must not pretend to own the entire surveillance domain.
**Improvement:** Emit explicit event contracts and exception records when wash-trade-like patterns, duplicate offsets, unusual timing, or restricted-account activity require surveillance review outside this PBC.
**Acceptance evidence:** Handoff event schemas, suspicious-pattern fixtures, and boundary proof that the package opens a governed exception rather than embedding a parallel surveillance engine.

### 27. Event vocabulary for lifecycle changes
**Justification:** Generic create and update events are too weak for real integration because downstream consumers need to know whether the change was an approval, correction, hold, or closure.
**Improvement:** Expand event payload semantics around order release, execution correction, allocation approval, confirmation mismatch, settlement fail, and break resolution while preserving the manifest’s top-level emitted contract family.
**Acceptance evidence:** Event examples, schema compatibility notes, and tests proving downstream consumers can differentiate operational meaning without inspecting raw row diffs.

### 28. Idempotent intake at every external edge
**Justification:** Duplicate executions, repeated confirmations, and replayed settlement acknowledgements are common operational facts and must not create duplicate records or false breaks.
**Improvement:** Apply idempotency keys and source-fingerprint logic across all inbound order, execution, allocation, confirmation, and settlement instruction channels.
**Acceptance evidence:** Duplicate-message fixtures, replay tests, and operator evidence showing suppressed duplicates remain visible with reason codes instead of disappearing.

### 29. Bulk operations workbench for high-volume days
**Justification:** Month-end, rebalance, and index event days create workload spikes that cannot be handled one record at a time.
**Improvement:** Extend `CapitalMarketsTradingOpsWorkbench` with bulk validate, bulk approve, bulk assign, bulk retry, and bulk export actions, each constrained by role and exception type.
**Acceptance evidence:** Bulk-action permission tests, partial-success result displays, and workbench evidence for high-volume queue handling without losing row-level traceability.

### 30. Supervisor approval cockpit
**Justification:** Supervisors need a different surface from analysts because they focus on materiality, aging, concentrated risk, and override governance.
**Improvement:** Add supervisor views that group pending approvals by desk, legal entity, notional size, settlement urgency, and repeated operator override patterns.
**Acceptance evidence:** Role-based UI tests, approval-aging metrics, and screenshots or snapshots in release evidence showing materiality-ranked queues.

### 31. Governed agent skills for trading ops tasks
**Justification:** The assistant should accelerate operations, but only as a constrained operator that drafts actions, explains reasoning, and respects permissions.
**Improvement:** Expand `CapitalMarketsTradingOpsAssistantPanel` with skills for triaging breaks, preparing allocation suggestions, summarizing mismatches, drafting SSI changes, and assembling release evidence packs without directly bypassing approval controls.
**Acceptance evidence:** Skill manifest examples, blocked-action tests, human-confirmation checkpoints, and audit entries for every accepted assistant proposal.

### 32. Semantic document intake for broker confirms and SSIs
**Justification:** Many post-trade facts still arrive as documents, and analysts waste time rekeying details that a governed extractor could stage safely.
**Improvement:** Use the manifest’s document-intake capability to parse broker confirmations, custodian settlement instructions, and exception notices into reviewable structured drafts linked back to source spans.
**Acceptance evidence:** Extraction quality fixtures, confidence thresholds, redaction handling, and operator review evidence showing source text next to proposed structured fields.

### 33. Dead-letter triage with domain explanations
**Justification:** Operational staff can only recover failed handlers if the retry queue explains the business impact rather than exposing a generic integration error.
**Improvement:** Present dead-lettered events in business terms such as duplicate execution, unknown account, stale policy version, or missing settlement instruction, with replay and quarantine actions.
**Acceptance evidence:** Dead-letter queue scenarios, replay safety tests, and workbench evidence that operators can resolve a business cause without reading infrastructure internals.

### 34. Replay-safe projection rebuilds
**Justification:** Trading ops needs trustworthy projections for positions, breaks, and workload analytics, and those views must be recoverable after code or schema changes.
**Improvement:** Add controlled rebuild and backfill procedures for projections derived from event-sourced operational history, with checkpointing and reconciliation against current read models.
**Acceptance evidence:** Projection rebuild tests, checksum comparisons, and release evidence proving rebuilds preserve operational counts and balances.

### 35. Continuous control assertions
**Justification:** Controls should fail loudly when segregation of duties, missing approvals, or stale exceptions appear, not only during periodic review.
**Improvement:** Populate `capital_markets_trading_ops_control_assertion` with continuous checks for self-approval, unresolved aged breaks, inactive SSIs on live trades, and unmatched confirmations past SLA.
**Acceptance evidence:** Failing-control fixtures, dashboard summaries, and event evidence that control breaches create explicit operational exceptions.

### 36. Tenant and legal-entity isolation
**Justification:** A single deployment may support multiple funds, books, or legal entities, and trading operations data leakage between them is unacceptable.
**Improvement:** Apply tenant isolation to orders, executions, allocations, confirmations, and position evidence, including policy rules and runtime parameters that can differ by tenant or legal entity.
**Acceptance evidence:** Cross-tenant negative tests, tenant-specific policy examples, and workbench proof that filters and permissions never cross entity boundaries.

### 37. Release evidence pack for operational readiness
**Justification:** The package manifest already points to `RELEASE_EVIDENCE.md`, so the backlog should make release proof concrete rather than aspirational.
**Improvement:** Define a release evidence pack that captures contract tests, lifecycle coverage, break-resolution scenarios, permission proofs, projection rebuild results, and representative workbench snapshots for trading ops flows.
**Acceptance evidence:** A documented release checklist, evidence artifact index, and package-level proof that every critical lifecycle stage has at least one regression artifact.

### 38. Workbench metrics that matter to operations
**Justification:** Generic counts do not help desk support or middle-office leads decide where to intervene first.
**Improvement:** Expand analytics to surface backlog aging, confirmation mismatch rate, settlement fail rate, repeat-break recurrence, stale market-data usage, and manual override frequency by desk and product.
**Acceptance evidence:** Metric definitions, projection tests, and workbench screens showing drill-through from KPI to the underlying queue.

### 39. Counterfactual simulation for disruption scenarios
**Justification:** Trading ops leaders need to test the effect of market holidays, settlement agent outages, cutoff changes, or policy tightening before those changes hit live flow.
**Improvement:** Use the simulation capability to model how order release, confirmation throughput, settlement timeliness, and break backlog would change under alternate policies or market disruptions.
**Acceptance evidence:** Scenario comparison outputs, non-mutating simulation logs, and release evidence demonstrating at least one settlement disruption and one policy-change simulation.

### 40. Carbon and sustainability annotations at the boundary
**Justification:** The manifest includes sustainability awareness, but in trading ops this should remain evidence-aware and not distort core booking logic.
**Improvement:** Add optional sustainability annotations such as venue or counterparty sustainability tags and downstream reporting references while keeping them outside the core economic validation path.
**Acceptance evidence:** Optional-field tests, UI evidence that sustainability data is visible but non-blocking unless policy requires it, and boundary notes in the specification.

### 41. Cross-PBC event federation contracts
**Justification:** Trading ops sits between trading, treasury, custody, accounting, and compliance domains, so event boundaries must be explicit to prevent hidden data coupling.
**Improvement:** Document and test which lifecycle facts are emitted for downstream consumers and which external events are accepted for policy, audit, and KPI context, including freshness and ownership expectations.
**Acceptance evidence:** Event contract tables, federation tests, and proof that no downstream workflow depends on direct table reads outside this PBC.

### 42. API surface completion beyond create endpoints
**Justification:** The listed APIs cover core creates, but operations also needs validate-only, search, exception, and evidence endpoints to function at scale.
**Improvement:** Extend the package API design to include queue retrieval, lifecycle search, validate-only order intake, break disposition, simulation access, and evidence export endpoints aligned to the existing route family.
**Acceptance evidence:** API contract examples, route authorization tests, and release evidence showing operators can complete full post-trade workflows without resorting to ad hoc data access.

### 43. Permission model by desk, role, and action
**Justification:** Read, create, update, approve, and admin are necessary but not sufficient for real separation of duties in trading operations.
**Improvement:** Define action-level permissions for releasing orders, approving allocations, changing SSIs, closing breaks, replaying dead letters, and accepting agent proposals, all scoped by desk or legal entity.
**Acceptance evidence:** Permission matrix, denial test cases, and UI proof that unavailable actions are absent or explicitly disabled with reason text.

### 44. Retention, masking, and evidentiary redaction
**Justification:** Trading ops records contain sensitive identifiers and commercial details, but audit and release evidence still need exportable artifacts.
**Improvement:** Apply field-level masking and retention rules to confirmations, SSIs, and evidence attachments so exported packs reveal enough for review without leaking sensitive settlement or client data.
**Acceptance evidence:** Redaction fixtures, retention policy examples, and release evidence exports that demonstrate masked but still verifiable artifacts.

### 45. FX and price tolerance management
**Justification:** Cross-currency trades and manually entered prices create frequent false breaks unless tolerances are explicit and product-aware.
**Improvement:** Add runtime-parameter support for price, FX, and accrued-value tolerances by asset class, market, and settlement currency, with separate thresholds for auto-match and analyst review.
**Acceptance evidence:** Tolerance policy records, match-threshold test cases, and workbench examples showing why one difference auto-matched while another opened a break.

### 46. Custodian and settlement-agent communication status
**Justification:** Operators need to know whether a settlement problem is internal, at the custodian, or with a counterparty before escalating.
**Improvement:** Track acknowledgement and status milestones from custodian, settlement agent, or depository interactions on `settlement_instruction` and related post-trade records.
**Acceptance evidence:** External-status fixtures, escalation routing tests, and workbench history that shows each external acknowledgement in sequence.

### 47. Cutoff-aware escalation logic
**Justification:** A break opened at 09:00 and one opened ten minutes before market cutoff do not have the same operational urgency.
**Improvement:** Make SLA and escalation rules aware of market cutoff windows, value date, and local holiday schedules so urgent items rise automatically and with the right severity.
**Acceptance evidence:** Cutoff-edge scenarios, escalation timer tests, and dashboard evidence that near-cutoff exceptions are highlighted separately from ordinary backlog.

### 48. Manual override governance
**Justification:** A resilient trading ops package must allow rare manual intervention without turning every hard case into an untraceable exception.
**Improvement:** Require reason codes, approver identity, expiration rules, and post-override review for any manual change to allocations, confirmations, settlement instructions, or break closures.
**Acceptance evidence:** Override fixtures, approval audit records, and analytics showing override rates by team and process stage.

### 49. Realistic seed data and operator runbooks
**Justification:** Trading ops quality is hard to judge from toy examples because the real domain depends on partial fills, crossed timezones, broken confirmations, and failed settlement chains.
**Improvement:** Expand seed and example data to include realistic lifecycle stories across order entry, execution capture, allocation, confirmation mismatch, settlement fail, and break resolution, paired with concise operator runbooks.
**Acceptance evidence:** Seed data scenarios, runbook references in package docs, and release evidence demonstrating that the sample stories exercise the main operational queues.

### 50. Continuous release assurance for the full trade lifecycle
**Justification:** The package claims continuous release assurance, so the final standard should prove the entire trading ops chain keeps working as changes land.
**Improvement:** Gate releases on contract tests, lifecycle scenario tests, permission checks, event-contract validation, projection rebuild verification, and curated UI evidence across `CapitalMarketsTradingOpsWorkbench`, `CapitalMarketsTradingOpsDetail`, and `CapitalMarketsTradingOpsAssistantPanel`.
**Acceptance evidence:** Passing package contract tests, release checklist completion, updated `RELEASE_EVIDENCE.md` expectations, and proof that the full order-to-break-to-resolution lifecycle remains covered.
