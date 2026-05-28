# Trade Finance Operations Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `trade_finance_operations`.
- Manifest description: letters of credit, guarantees, documentary collections, sanctions checks, shipment documents, and trade settlement.
- Current APIs: `POST /letter-of-credits`, `POST /bank-guarantees`, `POST /documentary-collections`, `POST /trade-documents`, `POST /sanctions-checks`, `GET /trade-finance-operations-workbench`.
- Current owned tables: `letter_of_credit`, `bank_guarantee`, `documentary_collection`, `trade_document`, `sanctions_check`, `shipment_evidence`, `trade_settlement`, `trade_finance_operations_policy_rule`, `trade_finance_operations_runtime_parameter`, `trade_finance_operations_schema_extension`, `trade_finance_operations_control_assertion`, `trade_finance_operations_governed_model`.
- Current emitted events: `TradeFinanceOperationsCreated`, `TradeFinanceOperationsUpdated`, `TradeFinanceOperationsApproved`, `TradeFinanceOperationsExceptionOpened`.
- Current consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Current workflow surfaces: `trade_finance_operations_create_letter_of_credit_workflow`, `trade_finance_operations_record_bank_guarantee_workflow`, `letter_of_credit_management`, `agentic_document_instruction_intake`, `ai_agent_task_assistance`, `continuous_release_assurance`, `trade_finance_operations_event_sourced_operational_history`, `trade_finance_operations_predictive_risk_scoring`, `trade_finance_operations_continuous_control_testing`.
- Current UI surfaces: `TradeFinanceOperationsWorkbench`, `TradeFinanceOperationsDetail`, `TradeFinanceOperationsAssistantPanel`.
- Current documentation targets: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Canonical letter of credit taxonomy
**Justification:** The current PBC names a letter-of-credit capability, but the domain model is still too shallow unless it distinguishes import, export, standby, confirmed, transferable, revolving, sight, and usance instruments with explicit semantics.
**Improvement:** Add a canonical instrument taxonomy on `letter_of_credit` that captures credit type, availability method, confirmation status, tolerance rules, revolving terms, transferable flags, and linked governing rules so downstream examination and settlement logic stops relying on free text.
**Acceptance evidence:** Schema fields and fixtures for each instrument type, API validation that rejects invalid combinations, and workbench filters that segment cases by credit subtype.

### 2. Trade finance party-role graph
**Justification:** Letters of credit, guarantees, and collections fail in practice when applicant, beneficiary, issuing bank, advising bank, confirming bank, reimbursing bank, presenter, and collecting bank roles are not modeled explicitly.
**Improvement:** Introduce a role graph that binds every trade instrument to its obligated and informational parties, role effective dates, branch identifiers, contact points, and authority evidence, with support for party changes driven by amendments.
**Acceptance evidence:** Relationship tests for core party permutations, UI role cards on the detail page, and event payloads that preserve party-role lineage over time.

### 3. Amount, tenor, and availability controls
**Justification:** Trade finance exposure turns on amount ceilings, sight versus deferred availability, mixed payment terms, and tolerance usage, not just a nominal amount field.
**Improvement:** Expand the core model to capture available amount, amount utilized, drawing schedule, tenor basis, deferred-payment maturity logic, acceptance dates, tolerance percentages, and auto-close rules when balances are exhausted.
**Acceptance evidence:** Calculation tests for sight and usance cases, maturity-date scenarios with weekends and holidays, and settlement views that show outstanding versus available exposure.

### 4. Amendment chain governance
**Justification:** Amendments are central to trade finance operations and must be versioned as legally meaningful changes rather than flat updates that erase prior obligations.
**Improvement:** Build an amendment chain model that records proposed clause changes, party acceptances, effective timestamps, beneficiary consent status, superseded terms, and amendment-specific discrepancy impacts across credits and guarantees.
**Acceptance evidence:** Version timeline rendering in the detail view, regression tests proving historical terms remain reconstructable, and release evidence that shows amendment replay accuracy.

### 5. Expiry, presentation period, and calendar handling
**Justification:** Presentation validity depends on expiry place, presentation period, banking days, and cut-off calendars; generic date fields are not sufficient.
**Improvement:** Add banking-calendar-aware logic for expiry date, last presentation day, shipment cut-off, grace handling, and place-of-expiry controls, including local non-business day roll rules where applicable.
**Acceptance evidence:** Calendar fixture coverage for weekend and holiday edge cases, UI warnings before expiry breaches, and discrepancy generation when late presentation occurs.

### 6. Presentation package document matrix
**Justification:** Trade transactions are decided on document packages, not isolated files, so the system needs a first-class document requirement matrix per instrument.
**Improvement:** Model required, optional, conditional, and waived document lines for each case, with quantities, originals versus copies, issuer constraints, wording constraints, and cross-document dependencies.
**Acceptance evidence:** A persisted document matrix tied to `trade_document`, API responses that expose requirement status, and test packs that fail when conditional documents are missing.

### 7. Document examination workbench
**Justification:** Document examination is the operational heart of letters of credit and collections, and it requires a structured compare-and-decide workspace rather than generic attachment review.
**Improvement:** Create an examination workspace that compares document facts to credit terms line by line, highlights mismatches, records examiner findings, tracks examination deadlines, and preserves an audit-grade examiner narrative.
**Acceptance evidence:** UI screenshots or story states for the examination panel, scenario tests for compliant and discrepant presentations, and event history showing who examined what and when.

### 8. Discrepancy codebook and severity model
**Justification:** Without a controlled discrepancy taxonomy, the PBC cannot support consistent refusal notices, waiver requests, or analytics on recurring trade document defects.
**Improvement:** Add a discrepancy catalog covering data mismatch, late presentation, missing document, stale transport date, unsigned certificate, prohibited transshipment, excess amount, inconsistent consignee, and sanctions-triggered hold, each with severity and allowed remediation paths.
**Acceptance evidence:** A discrepancy reference table, tests proving only approved discrepancy codes can be applied, and workbench reports that group backlog by discrepancy type and severity.

### 9. Discrepancy waiver and response workflow
**Justification:** Trade operations need a full post-examination path that distinguishes refusal, applicant waiver request, beneficiary resubmission, and accepted-under-reserve decisions.
**Improvement:** Implement a discrepancy workflow with timer-backed applicant waiver requests, beneficiary resubmission handling, partial acceptance logic, refusal notice generation, and settlement release conditions tied to final discrepancy disposition.
**Acceptance evidence:** Lifecycle tests from discrepancy opening to resolution, event traces for waiver requests and decisions, and UI states showing whether payment is blocked, released, or pending waiver.

### 10. Sight, deferred payment, acceptance, and negotiation flows
**Justification:** The PBC should not treat every drawing as immediate payment because trade finance settlement differs materially across sight, deferred-payment, acceptance, and negotiation structures.
**Improvement:** Add separate operational paths for sight reimbursement, deferred-payment undertakings, draft acceptance with maturity tracking, and negotiation with recourse or without recourse where supported by policy.
**Acceptance evidence:** Settlement scenario coverage for each availability type, maturity aging queues, and accounting-ready settlement evidence that identifies the exact obligation type.

### 11. Transferable and back-to-back credit support
**Justification:** Transferable credits and back-to-back arrangements introduce beneficiary substitution, amount reduction, and shipment timing controls that a basic LC model will miss.
**Improvement:** Extend `letter_of_credit` to support first and second beneficiary roles, transferred amount and quantity limits, clause inheritance rules, substituted document handling, and linked-credit relationships for back-to-back structures.
**Acceptance evidence:** Multi-beneficiary test cases, relationship views that show parent and child credits, and control assertions that prevent unauthorized term expansion in transferred credits.

### 12. Standby letter of credit handling under ISP rules
**Justification:** Standby credits operate differently from commercial credits, especially around demand wording, statement requirements, and governing practice under ISP rather than shipment-led document sets.
**Improvement:** Add a standby-specific workflow with demand package templates, beneficiary statement validation, drawing windows, automatic reduction logic, and rule selection between commercial-credit handling and standby handling.
**Acceptance evidence:** Case fixtures for standby financial and performance credits, rule-engine outputs that cite ISP logic, and detail views that show demand-package completeness before honor.

### 13. Guarantee issuance and lifecycle controls
**Justification:** Guarantees involve issuance, amendments, reductions, extensions, claims, expiries, and releases; treating them as flat records prevents safe operational control.
**Improvement:** Build a guarantee lifecycle on `bank_guarantee` that covers issuance approval, effective date, reduction schedule, auto-expiry, extension requests, claim receipt, claim decision, and final discharge evidence.
**Acceptance evidence:** State-machine tests for guarantee lifecycle edges, detail-page milestone rendering, and release evidence that proves claims and expiries were handled according to policy.

### 14. Counter-guarantee and indirect guarantee chains
**Justification:** Cross-border guarantee structures often include local issuing banks backed by counter-guarantees, and the chain of obligation must be visible to operations and control teams.
**Improvement:** Add linked-instrument support for guarantee hierarchies, counter-guarantee exposures, message dependencies, local-law overrides, and claim propagation rules across the chain.
**Acceptance evidence:** Hierarchy diagrams in the UI, scenario tests for downstream claims bubbling to upstream obligations, and event lineage that ties each claim to its guarantee chain.

### 15. Documentary collections for D/P and D/A
**Justification:** Documentary collections are operationally distinct from credits because banks handle documents and instructions without the same independent payment undertaking.
**Improvement:** Expand `documentary_collection` to model documents against payment, documents against acceptance, collecting-bank instructions, release conditions, drawee actions, maturity tracking, and non-payment or non-acceptance handling.
**Acceptance evidence:** Workflow tests for D/P and D/A paths, UI indicators for document release status, and analytics that separate unpaid, unaccepted, and matured collection items.

### 16. Collection instruction and release conditions
**Justification:** Collection operations depend on precise release wording, protest instructions, storage instructions, and charges allocation, which are usually hidden in free-text cover letters.
**Improvement:** Convert collection instructions into typed fields with protest flags, partial-payment rules, storage or warehousing instructions, contact escalation paths, and charge-bearer settings that drive operational decisions.
**Acceptance evidence:** Parsed instruction fixtures, API validation against unsupported instruction combinations, and generated release notices that draw only from typed instruction fields.

### 17. Trade loan linkage to trade instruments
**Justification:** Trade loans are not isolated credit products; they are often secured by, or timed against, letters of credit, guarantees, shipment evidence, or collection proceeds.
**Improvement:** Introduce explicit trade-loan records linked to the underlying credit, collection, shipment, or receivable so the PBC can track loan purpose, collateral basis, repayment source, and documentary prerequisites before drawdown.
**Acceptance evidence:** Linked-case views showing instrument-to-loan relationships, tests that block loan utilization when documentary prerequisites are unmet, and event payloads that expose linked obligations.

### 18. Pre-shipment and post-shipment loan utilization
**Justification:** Pre-shipment finance, packing credit, and post-shipment finance have different eligibility and aging logic, which should be operationally distinct.
**Improvement:** Add loan stages for pre-shipment, post-shipment, discounting, and collection-backed finance with utilization ceilings, rollover rules, due-date logic, and repayment waterfalls tied to export proceeds or accepted drafts.
**Acceptance evidence:** Utilization and repayment calculation tests, delinquency queues for overdue trade loans, and dashboard slices showing finance exposure by stage.

### 19. Sanctions and AML boundary orchestration
**Justification:** The PBC should own the trade decision boundary around sanctions and AML relevance without pretending to be the system of record for all customer due diligence.
**Improvement:** Define a boundary model in which `sanctions_check` stores trade-case screening requests, hits, adjudications, and release blocks while external KYC or customer-risk systems remain referenced by evidence links rather than duplicated profiles.
**Acceptance evidence:** Boundary contract documentation, tests proving only trade-relevant screening attributes are persisted locally, and operator screens showing when an external AML decision is required before release.

### 20. Rescreening triggers and watchlist evidence
**Justification:** A clean sanctions result at issuance is not enough when amendments, new shipment documents, vessel data, or beneficiary changes can alter risk.
**Improvement:** Add rescreen triggers for party changes, amendment terms, vessel updates, country changes, drawing requests, and elapsed time since last screen, with stored watchlist snapshots and adjudication notes.
**Acceptance evidence:** Event-driven rescreen tests, stale-screen alerts in the workbench, and evidence bundles showing what list version and matching rationale supported each decision.

### 21. Vessel, port, route, and jurisdiction risk checks
**Justification:** Shipment risk is not limited to named parties; vessel ownership, sanctioned ports, unusual routing, and high-risk jurisdictions can materially change trade compliance outcomes.
**Improvement:** Extend `shipment_evidence` and `sanctions_check` to capture vessel identifiers, ports of loading and discharge, transshipment nodes, carrier data, and jurisdiction tags that feed policy checks and exception routing.
**Acceptance evidence:** Policy-rule fixtures for prohibited ports and routes, UI badges for route-risk findings, and event evidence linking shipment facts to the compliance decision.

### 22. Canonical shipment document registry
**Justification:** Shipment evidence is broader than a file attachment list and should preserve document identity, issuer, version, and business meaning across amendments and presentations.
**Improvement:** Build a shipment-document registry that normalizes bill of lading, airway bill, road consignment note, commercial invoice, packing list, certificate of origin, insurance certificate, inspection certificate, and beneficiary certificate records under `trade_document`.
**Acceptance evidence:** Typed document records with version history, search filters by document class, and tests that prevent duplicate or conflicting document identity within a single presentation.

### 23. Bill of lading rule pack
**Justification:** Bills of lading carry high documentary risk around shipment date, on-board notation, consignee, notify party, freight terms, and clean-versus-clause status.
**Improvement:** Add a bill-of-lading rule pack that checks transport mode, on-board date, clean notation, consignee wording, notify party, freight prepaid or collect status, original-count requirements, and transshipment consistency against instrument terms.
**Acceptance evidence:** Examination fixtures for compliant and discrepant bills, UI diff views that highlight clause mismatches, and refusal notices that cite the exact transport discrepancy detected.

### 24. Invoice, packing list, origin, and inspection consistency checks
**Justification:** Trade presentations often fail because values, quantities, marks, country of origin, and goods descriptions disagree across documents even when each document looks individually plausible.
**Improvement:** Implement cross-document consistency checks over invoice values, packing-list quantities, goods descriptions, origin declarations, inspection findings, beneficiary names, and buyer references, with tolerance policies where allowed.
**Acceptance evidence:** Multi-document scenario tests, discrepancy generation tied to specific conflicting fields, and a document matrix view that shows reconciled versus conflicting facts.

### 25. Insurance and transport document adequacy
**Justification:** Insurance certificates and transport evidence have clause-level adequacy rules that affect whether a presentation can be honored.
**Improvement:** Add checks for insured amount, covered risks, currency alignment, claims payable location, endorsement status, policy date, and transport-document cross-references, with separate handling for marine, air, and multimodal shipments.
**Acceptance evidence:** Rule tests for under-insurance and misdated coverage, UI warnings on insufficient coverage, and audit trails showing who overrode any document adequacy issue.

### 26. Partial shipment, transshipment, and split-presentation rules
**Justification:** Operations teams need explicit control over whether partial shipment and transshipment are allowed because those terms drive documentary acceptance and discrepancy outcomes.
**Improvement:** Add term-level controls and rule evaluation for partial shipment, transshipment, split drawings, multiple presentations, and staged shipment schedules, with document-level checks against those permissions.
**Acceptance evidence:** Policy tests for allowed and prohibited combinations, workbench alerts when a presentation breaches shipment terms, and amendment-impact evidence when these permissions change mid-case.

### 27. Drawing and claim package assembly
**Justification:** Drawings on credits, guarantees, and standbys should be assembled as governed packages with required statements and supporting documents, not ad hoc file uploads.
**Improvement:** Build a drawing package model that captures draw amount, demand basis, supporting statement templates, required document set, beneficiary certifications, partial-drawing history, and rule-based completeness checks before submission.
**Acceptance evidence:** Package completeness tests, UI package checklists, and event emissions that distinguish draft drawing, submitted drawing, examined drawing, and honored or refused drawing.

### 28. Settlement orchestration and release conditions
**Justification:** Settlement should occur only when documentary, compliance, and approval conditions are satisfied, and those dependencies must be transparent to operators.
**Improvement:** Expand `trade_settlement` to include release conditions, blocked reason, value date, reimbursement path, beneficiary payment instructions, partial settlement handling, returned funds, and post-settlement proof artifacts.
**Acceptance evidence:** End-to-end settlement tests from compliant presentation to release, blocked-settlement dashboard states, and release evidence that ties settlement authorization to documentary and sanctions outcomes.

### 29. Charges, commissions, interest, and fee accruals
**Justification:** Trade finance revenue and customer communication depend on correctly assigning issuance fees, advising fees, confirmation commissions, handling charges, discrepancy fees, and usance interest.
**Improvement:** Add typed fee schedules with charge bearer, accrual basis, waiver flags, tax handling, and reversal logic for amendments, cancellations, and returned collections.
**Acceptance evidence:** Fee calculation fixtures, UI fee breakdowns by case, and settlement outputs that reconcile net proceeds after charges and commissions.

### 30. Foreign exchange and amount-mismatch controls
**Justification:** Trade instruments often operate across invoice currency, credit currency, settlement currency, and financing currency, which creates preventable amount and exposure errors.
**Improvement:** Add FX-aware validation for amount tolerances, financed amount versus available amount, currency conversion snapshots, and mismatch handling when presented values differ from expected instrument or shipment values.
**Acceptance evidence:** Multi-currency scenario tests, detail views showing conversion basis and tolerance usage, and risk alerts when a case exceeds allowed FX or amount mismatch thresholds.

### 31. UCP 600 rule-engine coverage
**Justification:** Commercial letters of credit need rule execution grounded in UCP 600 concepts rather than generic validation slogans.
**Improvement:** Build a rule pack that evaluates presentation timing, document consistency, originals and copies, transport-document requirements, stale shipment dates, and refusal timing with clause references traceable to the governing practice configuration.
**Acceptance evidence:** Rule-engine fixtures keyed to UCP-style scenarios, examiner screens that show rule citations behind findings, and release evidence listing which rule set governed each decision.

### 32. ISP98 rule-engine coverage
**Justification:** Standby credits and demand instruments need a separate rules surface because demand wording, statement conditions, and honor timing differ from shipment-led commercial credits.
**Improvement:** Add an ISP-focused rule set for documentary or statement conditions, drawing windows, extension clauses, automatic reduction, and demand-package sufficiency, selectable at the instrument level.
**Acceptance evidence:** Standby-specific rule outputs, scenario tests for demand-package sufficiency, and UI labels that make the governing practice visible to examiners and approvers.

### 33. Documentary collection rules under collection practice
**Justification:** Collections should not be forced into LC logic because release conditions, presentation decisions, and bank obligations differ materially.
**Improvement:** Add a collection-rule layer for release against payment, release against acceptance, protest instructions, partial-payment rules, return-of-documents handling, and drawer notification obligations.
**Acceptance evidence:** Collection scenario coverage, event histories showing release or return decisions, and workbench views that distinguish collection outcomes from credit outcomes.

### 34. Exception prioritization and service-level timers
**Justification:** Exceptions only become manageable when the queue is ordered by exposure, expiry risk, compliance severity, and customer-impact timers rather than creation time alone.
**Improvement:** Introduce SLA timers and prioritization logic that ranks examination exceptions, sanctions holds, expired waivers, overdue maturities, unclaimed guarantees, and stalled collections by operational urgency.
**Acceptance evidence:** Prioritized queue views, timer breach events, and analytics proving exception aging can be segmented by root cause and severity.

### 35. Four-eyes control and override justification
**Justification:** Honor, refusal, sanctions release, guarantee claim handling, and fee waivers are high-impact actions that need clear segregation of duties and override discipline.
**Improvement:** Add approval matrices requiring dual control for critical actions, including mandatory override reason codes, linked evidence, and policy-rule references whenever an operator bypasses a warning or soft block.
**Acceptance evidence:** Permission tests for maker-checker separation, UI prompts that require reason capture, and control-assertion records showing override frequency and approver identity.

### 36. Domain event taxonomy expansion
**Justification:** Generic created or updated events are not enough for downstream consumers to understand trade operations state changes.
**Improvement:** Extend emitted events to include amendment requested, amendment accepted, presentation received, discrepancy raised, waiver requested, screening blocked, drawing honored, collection released, guarantee claimed, settlement completed, and loan utilized.
**Acceptance evidence:** Event-schema definitions with examples, compatibility tests for consumers, and release evidence showing emitted-event coverage for each major workflow branch.

### 37. Outbox, inbox, idempotency, and replay evidence
**Justification:** Trade operations cannot afford duplicate honors, duplicate claim handling, or lost screening updates when event delivery is retried.
**Improvement:** Tighten outbox and inbox behavior with case-scoped idempotency keys, replay-safe handlers, duplicate detection on external callbacks, and operator tooling to inspect message status and retry reasons.
**Acceptance evidence:** Retry and duplicate-delivery tests, dead-letter scenarios with recovery steps, and UI evidence that shows message lineage from command to emitted event to projection update.

### 38. Trade finance workbench queue design
**Justification:** The current workbench surface should behave like an operations cockpit for credits, guarantees, collections, screenings, and settlements rather than a generic list page.
**Improvement:** Redesign `TradeFinanceOperationsWorkbench` into domain queues for instruments awaiting issuance, amended cases, presented documents, discrepancies, sanctions holds, pending drawings, due settlements, overdue maturities, and release-evidence gaps.
**Acceptance evidence:** Queue definitions mapped to real case states, navigation tests for every queue, and operator evidence showing one-click access from queue row to the exact pending action.

### 39. Detail page timeline and obligation view
**Justification:** Operators need a single narrative that combines amendments, document receipts, screenings, examination decisions, claims, settlements, and loan actions in time order.
**Improvement:** Expand `TradeFinanceOperationsDetail` into a timeline-plus-obligation view with instrument terms, outstanding obligations, documentary status, compliance status, fee status, and next required action grouped by lifecycle stage.
**Acceptance evidence:** Detail-page state stories for LC, guarantee, collection, and trade-loan linked cases, plus event-replay tests that recreate the same timeline from stored history.

### 40. Document viewer and discrepancy comparison UI
**Justification:** Examiners lose time when they have to jump between attachments and manually compare clause wording, shipment dates, quantities, and amounts.
**Improvement:** Build a document viewer that aligns extracted facts beside governing terms, highlights differing text spans, tracks examiner comments per field, and supports side-by-side comparison across invoice, bill of lading, insurance, and certificate documents.
**Acceptance evidence:** UI component states for compare mode, examiner annotation persistence tests, and usability evidence that discrepancies can be opened directly from a highlighted mismatch.

### 41. Agent skill for clause extraction and draft setup
**Justification:** Agent assistance is most useful when it prepares accurate drafts from applications or instrument text instead of producing generic summaries.
**Improvement:** Add an assistant skill that extracts clauses, parties, amounts, dates, shipment terms, and required documents from applications or incoming instrument text and converts them into governed draft records for operator review.
**Acceptance evidence:** Prompt-to-draft test fixtures, operator approval flows that show every extracted field before commit, and release evidence proving the assistant never bypasses governed mutation paths.

### 42. Agent skill for document examination support
**Justification:** Examination work is repetitive and detail-heavy, making it a strong fit for constrained AI support if findings remain explainable and reviewable.
**Improvement:** Add an assistant skill that pre-checks presentation packages against governing terms, suggests discrepancy codes, cites the triggering clause or field mismatch, and drafts refusal or waiver-request text without sending it automatically.
**Acceptance evidence:** Evaluation sets comparing assistant suggestions to human examiner outcomes, UI controls for accept or reject per suggested discrepancy, and audit logs for all assistant-generated examination content.

### 43. Agent skill for sanctions and AML boundary guidance
**Justification:** Screening escalations need consistent operator guidance that respects the boundary between trade-case screening and wider AML decisioning.
**Improvement:** Add an assistant skill that explains why a trade case was screened, what shipment or party facts triggered escalation, what evidence is still missing, and when the operator must wait for an external AML or compliance decision before proceeding.
**Acceptance evidence:** Guided-case fixtures for clear, false-positive, and escalation-required outcomes, detail-page assistant panels that surface missing evidence, and control tests proving the skill cannot clear a blocked case on its own.

### 44. Release evidence pack automation
**Justification:** The manifest already calls for `RELEASE_EVIDENCE.md`, so the backlog should make release evidence a first-class operational deliverable rather than a manual afterthought.
**Improvement:** Generate a release-evidence pack that bundles executed workflow tests, rule-pack coverage, event-contract verification, screening boundary tests, UI state evidence, unresolved-risk lists, and migration or backfill status for the trade finance package.
**Acceptance evidence:** A reproducible release-evidence checklist, generated artifacts tied to build outputs, and proofs that each critical trade workflow has current evidence attached to the release candidate.

### 45. Synthetic trade-document corpus and edge-case fixtures
**Justification:** Domain-deep quality depends on a representative test corpus of shipment documents, amendments, guarantees, demands, and collections rather than shallow happy-path examples.
**Improvement:** Build a synthetic corpus that covers compliant and discrepant document sets, forged-looking but structurally valid inputs, late shipments, partial drawings, split bills of lading, vessel changes, expired guarantees, and loan-linked trade cases.
**Acceptance evidence:** Versioned fixtures stored with clear scenario labels, automated tests that consume the corpus across parsing and examination flows, and release evidence that reports corpus coverage by product type.

### 46. Counterfactual simulation for amendments, drawings, and delays
**Justification:** Trade operations teams need to know the downstream impact of a proposed amendment, delayed vessel, changed shipment quantity, or partial drawing before they commit the change.
**Improvement:** Add non-mutating simulation flows that show how a candidate amendment or operational delay would affect document requirements, sanctions rescreening, settlement timing, guarantee exposure, and linked trade-loan repayment assumptions.
**Acceptance evidence:** Simulation result views with before-and-after comparisons, tests proving no live state is mutated during simulation, and operator exports that can be attached to approval decisions.

### 47. Operational analytics and KPI definitions
**Justification:** A trade finance workbench should expose domain KPIs such as examination turnaround, discrepancy rate, waiver aging, claim frequency, settlement timeliness, and screened-case conversion.
**Improvement:** Define metrics and projections for issuance cycle time, amendment volume, first-pass clean presentation rate, discrepancy recurrence, sanctions hold duration, maturity punctuality, collection release rate, and trade-loan utilization versus settlement outcome.
**Acceptance evidence:** Metric definitions with exact formulas, projection tests, dashboard cards wired to owned read models, and release evidence that shows KPI calculations were validated on known fixtures.

### 48. Multi-entity, branch, and correspondent operating model
**Justification:** Trade finance frequently spans branches, regional operations centers, and correspondent-bank handoffs, which must be modeled without cross-tenant leakage or blurred accountability.
**Improvement:** Extend the PBC to capture booking branch, operating branch, advising location, correspondent role, branch-specific calendars, and local-policy overrides while preserving tenant isolation and action auditability.
**Acceptance evidence:** Multi-entity access tests, branch-scoped queue views, and control assertions that prevent users from one branch or tenant acting on another entity's restricted cases.

### 49. API and query completeness for trade operations
**Justification:** The current API list is command-heavy and needs richer query and correction surfaces for real operational use.
**Improvement:** Expand the API surface with search, detail retrieval, examination save or submit, discrepancy response, amendment preview, drawing submission, settlement release, rescreen request, trade-loan linkage, and release-evidence export endpoints, all with explicit idempotency and pagination rules.
**Acceptance evidence:** Contract tests for new command and query routes, pagination and filter fixtures on the workbench feeds, and event-to-API traceability proving every critical UI action is backed by a governed endpoint.

### 50. Go-live control gates and release readiness
**Justification:** A domain-heavy package should not ship on feature count alone; it should ship only when trade-specific controls, evidence, and operational playbooks are complete.
**Improvement:** Define release gates that require passing rule-pack tests, document-examination regression suites, sanctions-boundary verification, event replay checks, UI critical-path validation, unresolved-exception review, and signed-off operational runbooks for credits, guarantees, collections, loans, and settlements.
**Acceptance evidence:** A go-live checklist tied to `RELEASE_EVIDENCE.md`, explicit pass or fail criteria for each control gate, and a release summary that names any remaining risks rather than hiding them.
