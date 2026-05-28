# Procurement and Strategic Sourcing PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `procurement_sourcing`. The items are specific to source-to-order operations: requisitions, approvals, budget checks, category strategy, supplier qualification, RFQs, bids, scoring, awards, contracts, purchase orders, change orders, supplier risk, compliance, savings, carbon-aware sourcing, supply exposure, event reliability, UI workbenches, and agent-assisted procurement work.

## Current Domain Evidence Used

- Domain purpose: source-to-order execution for purchase requisitions, RFQs, supplier qualification, supplier scoring, contract awards, purchase orders, approvals, compliance, vendor performance, and supply-risk governance.
- Owned boundary: purchase requisitions and lines, requisition approvals, budget checks, category strategies and policies, supplier profiles, identities, sites, qualifications, risk signals, preferred supplier policies, RFQs and lines, invitations, supplier bids and bid lines, bid normalization, supplier scorecards, awards, split awards, vendor contracts, clauses, compliance obligations, renewals, purchase orders and lines, change orders, tolerance checks, payment terms, material-shortage projections, vendor-performance projections, budget projections, supplier-risk projections, contract-compliance projections, access-policy projections, policy screenings, PO routes, supplier compliance proofs, audit traces, federation projections, carbon sourcing selections, award optimization, RFQ allocation, bid anomaly signals, supply exposure models, price/lead-time forecasts, strategy simulations, parsed documents, rules, parameters, configuration, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: requisition creation and approval, RFQ creation, bid capture, supplier scoring, supplier award, contract creation, PO issuance, event inbox handling, workbench, rules, parameters, schema extensions, runtime configuration, boundary checks, and release evidence.
- Existing events and dependencies: emits `PurchaseRequisitionCreated`, `PurchaseRequisitionApproved`, `RfqCreated`, `SupplierBidCaptured`, `SupplierSelected`, `VendorContractCreated`, and `PurchaseOrderIssued`; consumes material shortage, vendor performance, budget, supplier risk, contract compliance, and access-policy events through declared APIs/projections only.

## 50 Better-Than-World-Class Improvements

### 1. Requisition intake completeness gate

**Justification:** Poor requisitions create downstream sourcing delays, approval rework, budget leakage, wrong supplier selection, and purchase order errors.

**Improvement:** Add requisition readiness checks for legal entity, requester, category, item/service description, quantity, UOM, needed-by date, delivery location, cost center/project, budget projection, preferred supplier, contract reference, risk class, and attachment evidence. Incomplete requisitions should remain draft with actionable remediation.

### 2. Requisition line semantic enrichment

**Justification:** Free-text request lines hide category, specification, quality, compliance, and supplier constraints that determine the correct sourcing route.

**Improvement:** Use semantic parsing and rules to classify line type, commodity/category, service scope, technical specification, substitutes, recurring spend, hazardous/restricted flags, and required evidence. Store confidence and require human correction for ambiguous lines.

### 3. Dynamic approval matrix

**Justification:** Procurement approvals depend on spend amount, category, entity, project, supplier risk, urgency, budget, contract coverage, and restricted goods.

**Improvement:** Implement an approval engine with threshold bands, delegation, out-of-office routing, segregation-of-duties checks, emergency overrides, escalation timers, and full approval evidence. Every approval decision should cite the active rule and projection versions used.

### 4. Budget commitment projection governance

**Justification:** Procurement decisions commit future spend before invoices arrive, so stale or weak budget checks create financial surprises.

**Improvement:** Add budget projection freshness, commitment reservations, soft/hard budget controls, tolerance thresholds, pre-encumbrance release, and budget-change event replay. Requisitions and POs should show budget impact and residual risk before approval.

### 5. Category strategy operating model

**Justification:** Category strategy is the bridge between policy and buying execution; without it, sourcing becomes transactional and inconsistent.

**Improvement:** Add category playbooks for source method, preferred supplier policy, RFQ threshold, negotiation method, contract requirement, sustainability weighting, diversity objectives, risk appetite, market index, and renewal strategy. Requisition routing should inherit category strategy by default.

### 6. Preferred supplier policy engine

**Justification:** Preferred supplier use must balance price, quality, lead time, risk, contract obligations, diversity, sustainability, and operational urgency.

**Improvement:** Compile preferred supplier rules with eligibility, ranking, exceptions, effective dates, site coverage, contract linkage, restricted supplier checks, and override approval. Workbench explanations should show why a supplier was preferred or rejected.

### 7. Supplier onboarding and qualification lifecycle

**Justification:** Supplier qualification determines whether bids, contracts, and POs are valid and safe.

**Improvement:** Model supplier lifecycle from prospect to invited, qualified, conditional, restricted, suspended, inactive, and archived. Store identity checks, tax/compliance evidence, banking readiness references, insurance, certifications, capacity, site coverage, diversity status, and renewal dates.

### 8. Supplier identity and site verification

**Justification:** Fraud, duplicate suppliers, wrong supplier sites, and stale site capabilities undermine procurement controls.

**Improvement:** Add supplier identity matching, duplicate detection, site-level address/contact/capability validation, decentralized credential support, evidence expiry, risk flags, and approval gates. PO issuance should require an eligible supplier site, not only a supplier header.

### 9. Supplier risk signal fusion

**Justification:** Supplier risk changes from performance, financial stress, geopolitical events, compliance breaches, shortages, and access-policy changes.

**Improvement:** Fuse declared risk projections and internal signals into a supplier risk timeline with source, severity, confidence, affected categories/sites, expiry, mitigation, and decision impact. RFQ, award, contract, and PO actions should surface current risk.

### 10. RFQ strategy selection

**Justification:** Not all sourcing events should use the same RFQ structure; auctions, sealed bids, negotiated events, and emergency sourcing have different controls.

**Improvement:** Add RFQ strategy selection based on category, spend, supplier market, urgency, risk, bid count, confidentiality, and negotiation intent. The system should generate the correct RFQ timeline, invitation rules, scoring model, and communication controls.

### 11. RFQ line specification governance

**Justification:** Ambiguous line requirements cause incomparable bids, disputes, substitutions, and poor award decisions.

**Improvement:** Add RFQ line requirement templates for goods, services, capital equipment, subscriptions, logistics, and professional services. Require technical specs, acceptance criteria, delivery terms, service levels, alternatives, and mandatory compliance evidence where applicable.

### 12. Supplier invitation fairness controls

**Justification:** Sourcing integrity depends on fair, defensible supplier invitation and communication.

**Improvement:** Add invitation eligibility, conflict-of-interest screening, incumbent challenger balance, diversity goals, restricted supplier exclusion, communication blackout windows, supplier Q&A logs, late invite handling, and invitation audit evidence.

### 13. Bid capture and sealed-bid integrity

**Justification:** Bid tampering, premature visibility, late submissions, and incomplete responses damage trust and legal defensibility.

**Improvement:** Add sealed-bid vault behavior with submission timestamps, completeness checks, late-bid policy, amendment tracking, supplier acknowledgements, cryptographic hashes, and role-gated bid opening. Bid revisions should preserve full history.

### 14. Bid normalization workbench

**Justification:** Suppliers quote different units, currencies, incoterms, lead times, freight assumptions, discounts, tiers, and alternates.

**Improvement:** Normalize bids to comparable landed cost, UOM, currency, tax/duty assumptions, delivery point, payment terms, volume tiers, warranty, service levels, and risk adjustments. Keep original bid values and show every transformation.

### 15. Multi-factor supplier scorecard

**Justification:** Supplier selection should not collapse to price when lead time, quality, risk, capacity, sustainability, diversity, compliance, and contract fit matter.

**Improvement:** Build weighted scorecards with mandatory gates, category-specific weights, normalized metrics, confidence intervals, projection freshness, explainability, and sensitivity analysis. Scorecards should show how rank changes if weights or risk assumptions change.

### 16. Award recommendation with tradeoff analysis

**Justification:** Procurement teams need defensible award decisions that explain value, risk, savings, compliance, and service impact.

**Improvement:** Generate award recommendations with total cost, savings baseline, supplier risk, lead-time confidence, capacity fit, contract coverage, carbon impact, diversity contribution, and compliance obligations. Require approval when recommendation differs from lowest compliant bid.

### 17. Split-award optimization

**Justification:** Splitting awards can reduce risk, improve capacity, meet diversity targets, and preserve competition, but it adds complexity.

**Improvement:** Add split-award optimization for capacity, lot sizes, geography, lead time, risk diversification, price breaks, minimum commitments, and supplier development goals. Show operational consequences and contract/PO complexity before approval.

### 18. Negotiation scenario planner

**Justification:** Negotiation outcomes improve when buyers can compare concessions, terms, volumes, and timing before engaging suppliers.

**Improvement:** Add negotiation scenario planning for price, rebates, payment terms, delivery windows, service levels, penalties, volume commitments, indexation, and renewal options. Link accepted terms to award and contract evidence.

### 19. Contract authoring readiness

**Justification:** Awards do not become executable supply until contract terms, clauses, obligations, and evidence are complete.

**Improvement:** Add contract readiness checks for supplier, category, pricing, effective dates, renewal horizon, termination rights, service levels, delivery terms, compliance obligations, data/security clauses, insurance, and approval evidence.

### 20. Clause library and obligation model

**Justification:** Contracts need structured clauses and obligations that can drive downstream monitoring instead of static documents.

**Improvement:** Build clause templates with jurisdiction, category, risk, fallback language, required approvals, obligation extraction, owner, due date, evidence type, breach severity, and renewal impact. Obligations should feed compliance projections and workbench queues.

### 21. Contract compliance monitoring

**Justification:** Procurement value erodes when contracted prices, terms, service levels, and obligations are not monitored.

**Improvement:** Add compliance checks for price adherence, service levels, insurance/certification expiry, volume commitments, rebates, sustainability reporting, diversity spend, and renewal milestones. Surface exceptions before PO issuance or renewal.

### 22. Renewal and expiry governance

**Justification:** Missed renewals create price leakage, service interruption, unmanaged auto-renewals, and weak negotiation leverage.

**Improvement:** Add renewal horizon parameters, notice windows, termination deadlines, renewal strategy, incumbent performance review, market benchmark refresh, and sourcing recommendation. Workbench should rank renewals by risk and opportunity.

### 23. Purchase order type coverage

**Justification:** Procurement requires different PO behaviors for standard, blanket, planned, emergency, service, capital, direct, indirect, and subcontracted spend.

**Improvement:** Add PO type-specific fields, rules, tolerances, approval paths, receiving/acceptance expectations, contract binding, payment terms, and AppGen-X event evidence. The UI should guide users through each PO type without generic forms.

### 24. PO line validation and tolerance controls

**Justification:** PO errors drive receipt, invoice, and supplier disputes.

**Improvement:** Validate item/service description, quantity, UOM, price, currency, tax assumptions, delivery schedule, location, contract price, supplier site, tolerance, and receiving requirements. Store rejected-line reasons and allowed override evidence.

### 25. Change order lifecycle

**Justification:** PO changes affect budget, supplier commitments, delivery, contract compliance, and downstream AP matching.

**Improvement:** Add change order versioning, reason codes, delta analysis, reapproval rules, supplier acknowledgement, budget recheck, contract compliance recheck, and emitted evidence. Users should see before/after values and downstream impact.

### 26. Emergency procurement controls

**Justification:** Urgent buying is necessary but can bypass controls, increase price, and introduce supplier risk.

**Improvement:** Add emergency sourcing mode with reason, time limit, premium tolerance, restricted supplier screening, post-facto review, mandatory remediation, and management evidence. Emergency POs should expire or require conversion to normal governance.

### 27. Material shortage-driven sourcing

**Justification:** Material shortages require rapid sourcing decisions while preserving risk and budget controls.

**Improvement:** Use `MaterialShortageDetected` projections to create sourcing demand with shortage severity, required date, substitute possibilities, production impact, supplier options, and expedited-cost scenarios. Keep inventory/manufacturing data as projections only.

### 28. Supplier performance feedback loop

**Justification:** Supplier selection must learn from actual delivery, quality, responsiveness, and compliance performance.

**Improvement:** Use `VendorPerformanceUpdated` projections to update scorecards, preferred supplier policy, RFQ eligibility, award confidence, and renewal strategy. Show which performance events changed a supplier decision.

### 29. Savings and value realization tracking

**Justification:** Procurement value includes hard savings, cost avoidance, rebates, working-capital benefits, risk reduction, and service improvements.

**Improvement:** Track baseline, negotiated price, award price, realized PO price, rebate terms, payment-term value, risk-adjusted savings, and leakage. Require methodology evidence for claimed savings.

### 30. Spend analytics convergence

**Justification:** Buyers need real-time visibility into requisitions, RFQs, awards, contracts, and POs without separate analytical pipelines.

**Improvement:** Add operational spend analytics by category, supplier, entity, project, contract, PO type, risk class, carbon impact, diversity, savings, cycle time, and exception rate. Dashboards should cite source records and projection freshness.

### 31. Supply exposure modeling

**Justification:** Procurement risk is concentrated across suppliers, categories, countries, sites, logistics lanes, and contract dependencies.

**Improvement:** Model stochastic supply exposure with supplier concentration, site dependency, geopolitical risk, material scarcity, contract expiry, lead-time variance, and performance volatility. Provide mitigation options and confidence.

### 32. Price and lead-time forecasting

**Justification:** Sourcing strategy and award timing improve when buyers understand probable price and lead-time movements.

**Improvement:** Add forecasts by category, supplier, commodity, region, volume band, contract term, and urgency. Show forecast confidence, feature lineage, drift, and impact on requisition routing, RFQ timing, and award strategy.

### 33. Carbon-aware sourcing selection

**Justification:** Sourcing decisions affect freight emissions, supplier operations, packaging, regional production, and sustainability commitments.

**Improvement:** Include carbon scoring in bid normalization and award recommendations using supplier site, delivery terms, transport projection, packaging, production method, and renewable evidence. Show cost-service-carbon tradeoffs explicitly.

### 34. Supplier diversity and resilience goals

**Justification:** Supplier networks should support diversity, resilience, local sourcing, and strategic supplier development without tokenistic scoring.

**Improvement:** Add measurable goals, eligibility evidence, spend targets, category applicability, development programs, anti-fraud checks, and tradeoff analysis. Awards should show how they affect supplier diversity and resilience.

### 35. Restricted supplier and compliance screening

**Justification:** Procurement must prevent buying from restricted, sanctioned, noncompliant, or policy-blocked suppliers.

**Improvement:** Add screening before RFQ invitation, bid acceptance, award, contract, and PO issuance with policy version, attributes evaluated, decision, override path, and AppGen-X audit evidence. Block high-severity violations by default.

### 36. Zero-knowledge supplier compliance proof

**Justification:** Internal teams or external parties may need proof of supplier eligibility without exposing sensitive supplier documents.

**Improvement:** Generate cryptographic compliance proofs for qualification, insurance, certification, restricted-list screening, and contract obligations. Verification APIs should prove status and timestamp while redacting confidential evidence.

### 37. Immutable procurement audit trace

**Justification:** Source-to-order decisions are high-control activities requiring complete, tamper-evident reconstruction.

**Improvement:** Hash-chain requisition, approval, RFQ, bid, scoring, award, contract, PO, change order, policy screening, event handling, and agent-preview evidence. UI timelines should show every material decision and event.

### 38. AppGen-X event reliability cockpit

**Justification:** Procurement depends on budget, supplier risk, material shortage, compliance, and access-policy events; stale or failed projections change decisions.

**Improvement:** Add inbox/outbox panels for idempotency, duplicates, retries, dead letters, projection freshness, payload lineage, handler version, replay eligibility, and downstream emitted events. Decisions should warn when projections are stale.

### 39. Supplier network federation

**Justification:** Enterprises coordinate with AP, inventory, manufacturing, logistics, supplier systems, and risk providers without sharing tables.

**Improvement:** Add federation projections for supplier capability, supply demand, PO route status, payment readiness, material need, performance, and compliance. Boundary tests should reject direct reads of AP, inventory, manufacturing, or supplier-system tables.

### 40. Sourcing strategy simulation

**Justification:** Buyers should understand consequences before changing sourcing method, bid count, weightings, split-award rules, or emergency premium.

**Improvement:** Simulate sourcing strategies against historical and active events, showing supplier participation, cycle time, savings, risk, service, carbon, diversity, budget, and compliance outcomes. Keep simulations side-effect-free.

### 41. Mechanism-design RFQ and auction allocation

**Justification:** RFQ design affects supplier behavior, price discovery, fairness, and long-term supplier health.

**Improvement:** Add RFQ mechanism options such as sealed bid, multi-round negotiation, reverse auction, capacity auction, and score-weighted allocation. Provide anti-collusion controls, participation safeguards, and buyer explanations.

### 42. Bid anomaly and collusion detection

**Justification:** Unusual bid patterns can indicate collusion, supplier distress, specification ambiguity, or data errors.

**Improvement:** Detect bid anomalies across price, lead time, identical language, timing, IP/device metadata where available, alternates, exclusions, and historical patterns. Route high-risk events to review without automatically accusing suppliers.

### 43. Procurement MLOps governance

**Justification:** ML-assisted supplier ranking, risk scoring, price forecasting, and anomaly detection influence spend and supplier fairness.

**Improvement:** Add model registry, feature lineage, training windows, approval status, explainability, drift monitoring, fairness checks, rollback, and release evidence for every procurement model used in decisions.

### 44. Rule and parameter simulation

**Justification:** Approval thresholds, score weights, supplier risk limits, bid count, renewal horizon, and tolerance values materially alter procurement behavior.

**Improvement:** Simulate rule and parameter changes against historical and active procurement work, showing approval load, cycle time, supplier eligibility, award outcomes, budget failures, compliance blocks, and dead-letter volume before activation.

### 45. Workbench coverage for all procurement capabilities

**Justification:** Buyers, approvers, contract managers, and auditors need direct access to the full source-to-order surface.

**Improvement:** Expand UI into requisition intake, approval queue, budget policy, category strategy, supplier qualification, RFQ monitor, bid normalization, scorecard, award board, contract console, renewal queue, PO console, change orders, risk cockpit, spend analytics, controls, rules, parameters, configuration, event reliability, and agent panels.

### 46. Agent-safe procurement document intake

**Justification:** The procurement chatbot should read requisitions, quotes, contracts, supplier documents, and instructions without unsafe writes.

**Improvement:** Add document intake skills that extract candidate facts, map them to owned procurement tables, validate permissions and rules, reject foreign-table mutations, and produce side-effect-free previews with confidence, risk, required confirmations, and expected AppGen-X events.

### 47. Agent-safe sourcing and award guidance

**Justification:** AI recommendations can bias supplier outcomes if they are not explainable, bounded, and reviewable.

**Improvement:** Require the agent to present sourcing options, score drivers, supplier risks, conflicts, budget impact, contract implications, carbon/diversity tradeoffs, and approval requirements. The agent should not create awards or POs without explicit human confirmation.

### 48. Continuous procurement control testing

**Justification:** Procurement controls should run continuously across approvals, supplier eligibility, bid integrity, contracts, POs, and event handling.

**Improvement:** Add assertions for unauthorized approvals, split approvals, restricted suppliers, insufficient bid count, missing contract linkage, expired qualification, PO tolerance breach, stale budget projection, duplicate supplier, dead-letter aging, and agent-preview bypass.

### 49. Procurement readiness score

**Justification:** Users need an evidence-backed view of whether the PBC is ready for production procurement operations.

**Improvement:** Compute readiness from category setup, supplier qualification, approval matrix, budget projection freshness, RFQ strategy, contract templates, PO rules, event reliability, UI coverage, control assertions, boundary proof, model governance, and agent safety.

### 50. End-to-end source-to-order proof

**Justification:** A complete procurement PBC must prove the full lifecycle from demand signal to governed purchase order.

**Improvement:** Add an executable proof scenario covering material shortage projection, requisition creation, approval, RFQ, supplier invitation, sealed bid, bid normalization, scorecard, award, contract, PO issuance, emitted `PurchaseOrderIssued`, audit trace, UI evidence, event reliability, controls, and agent explanation.
