# Cross Border Trade PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `cross_border_trade`. The items are specific to cross-border trade execution: HS classification, landed-cost quoting, denied-party screening, export-control checks, customs declarations, document packets, broker handoffs, carrier handoffs, compliance holds, country restrictions, duties and taxes, Incoterms, audit evidence, rules, parameters, configuration, AppGen-X event reliability, UI workbenches, and agent-assisted trade compliance operations.

## Current Domain Evidence Used

- Domain purpose: `cross_border_trade` owns cross-border trade execution, including HS classification, landed-cost calculation, denied-party and export-control screening, customs document evidence, duties and taxes, broker and carrier handoffs, declarations, compliance holds, and audit-proof release evidence.
- Owned boundary: HS classifications, landed-cost quotes, export-control checks, customs declarations, denied-party screenings, trade document packets, broker handoffs, carrier handoffs, compliance holds, country restriction policies, rules, parameters, configuration, schema extensions, audit evidence, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: runtime configuration, parameters, rules, schema extensions, event receiving, product classification, landed-cost quoting, export-control screening, customs declaration filing and release, denied-party screening, document packet preparation, broker/carrier handoffs, compliance hold open/resolution, country restriction policy registration, control tests, workbench, schema/service/release evidence, permissions, UI binding, and boundary verification.
- Existing events and dependencies: consumes `OrderPlaced`, `InventoryReserved`, `PaymentCaptured`, and `ShipmentDispatched`; emits `HSClassified`, `LandedCostQuoted`, `ExportControlCleared`, `CustomsDeclarationFiled`, `DeniedPartyScreened`, `TradeDocumentPacketPrepared`, `BrokerHandoffQueued`, `CarrierHandoffPrepared`, `TradeComplianceHoldOpened`, `TradeComplianceHoldResolved`, `CountryRestrictionPolicyRegistered`, and `CustomsDeclarationReleased`; integrates with order, inventory, payment, shipment, broker, carrier, customer, and audit only through declared APIs/events/projections.

## 50 Better-Than-World-Class Improvements

### 1. HS classification readiness gate

**Justification:** HS classification is unsafe when product description, materials, origin, destination, end use, and supporting evidence are incomplete.

**Improvement:** Add readiness checks for item identity, description, composition, country of origin, destination, end use, customer/channel context, prior classifications, keyword evidence, confidence, reviewer threshold, and effective date before publishing `HSClassified`.

### 2. HS classification lifecycle governance

**Justification:** Classifications need draft, reviewed, approved, superseded, disputed, expired, and blocked states to support audit and reclassification.

**Improvement:** Implement state transitions with classifier, reviewer, confidence, legal basis, ruling reference, reason, effective window, supersession lineage, idempotency key, and invalid-transition explanations.

### 3. Classification evidence graph

**Justification:** Trade specialists need to trace why a classification was selected and what evidence supported it.

**Improvement:** Link product attributes, materials, keywords, images/documents, prior rulings, country rules, reviewer notes, confidence factors, and audit hashes into a package-local classification graph.

### 4. Multi-jurisdiction classification variance

**Justification:** HS interpretation and duty treatment can vary by destination country, trade agreement, and local tariff schedule.

**Improvement:** Store jurisdiction-specific classification variants with destination, local code extension, tariff source, effective date, confidence, reviewer, and country restriction implications.

### 5. Landed-cost quote completeness

**Justification:** Landed cost must include goods value, freight, insurance, duty, tax, fees, Incoterms, currency, and assumptions.

**Improvement:** Validate quote inputs for item value, quantity, origin, destination, currency, Incoterms, shipping cost, insurance, broker fees, duty rates, tax rates, de minimis rules, and quote expiry.

### 6. Duty and tax calculation trace

**Justification:** Auditors and customers need to understand how duties and taxes were calculated.

**Improvement:** Record calculation lines for customs value, duty basis, rate source, duty amount, tax basis, tax rate, tax amount, fee amount, currency conversion, rounding, and excluded/assumed components.

### 7. Incoterm obligation model

**Justification:** Incoterms determine who owns customs clearance, risk transfer, cost responsibility, and document obligations.

**Improvement:** Add Incoterm rules for cost allocation, duty payer, tax payer, risk transfer point, document obligations, broker responsibility, carrier handoff requirements, and customer-facing disclosure.

### 8. De minimis and threshold handling

**Justification:** Low-value shipments may qualify for simplified clearance, duty relief, or special tax treatment.

**Improvement:** Model de minimis thresholds by country, currency, product category, shipment value, customer type, excluded goods, evidence requirements, and quote/declaration effects.

### 9. Denied-party screening lifecycle

**Justification:** Restricted-party screening must be auditable across counterparty, ship-to, bill-to, payer, consignee, broker, and carrier identities.

**Improvement:** Add screening states, parties screened, list sources, match strength, aliases, address matching, risk decision, reviewer, expiry, hold linkage, and `DeniedPartyScreened` event evidence.

### 10. Fuzzy match resolution controls

**Justification:** Screening creates false positives and false negatives that require controlled adjudication.

**Improvement:** Add match adjudication with candidate list, similarity factors, identity evidence, reviewer outcome, override reason, expiration, rescreen trigger, and audit proof.

### 11. Export-control check readiness

**Justification:** Export-control decisions need item, destination, end use, end user, license, classification, and order context.

**Improvement:** Validate classification, controlled item flags, destination restrictions, end-use statement, end-user screening, license requirement, exception eligibility, and review threshold before clearance.

### 12. License requirement detection

**Justification:** Some goods, destinations, customers, and end uses require export licenses or deny shipment.

**Improvement:** Add license trigger rules with jurisdiction, item class, HS/export code, destination, end use, party risk, exception code, license id, expiry, and hold/release effect.

### 13. Country restriction policy governance

**Justification:** Restricted countries, embargoes, sanctions, product bans, and local import rules change frequently.

**Improvement:** Register policies with country, region, product scope, party scope, restriction type, severity, effective dates, source reference, reviewer, and compiled policy hash.

### 14. Compliance hold lifecycle

**Justification:** Holds must prevent shipment or release until missing evidence, screening, licensing, or documents are resolved.

**Improvement:** Implement hold states open, assigned, evidence_pending, reviewed, resolved, released, expired, escalated, and blocked with source, severity, owner, SLA, release conditions, and emitted events.

### 15. Document packet completeness

**Justification:** Customs declarations require commercial invoice, packing list, certificate, license, origin evidence, and carrier/broker-specific documents.

**Improvement:** Add document packet rules by country, Incoterm, product, value, carrier, broker, and declaration type, with required documents, hashes, missing evidence, expiry, and completeness score.

### 16. Semantic trade document parsing

**Justification:** Trade documents contain classification, origin, value, party, license, and shipment facts that should be extracted safely.

**Improvement:** Parse invoices, packing lists, certificates, licenses, and broker forms into candidate facts with confidence, evidence links, field gaps, policy checks, and side-effect-free previews.

### 17. Customs declaration lifecycle

**Justification:** Declarations move through draft, documents_ready, broker_queued, filed, accepted, rejected, amended, released, closed, and cancelled.

**Improvement:** Implement declaration state transitions with filing data, broker handoff, carrier handoff, duties/taxes, holds, document packet, idempotency key, and release gates.

### 18. Declaration release gate

**Justification:** Customs declarations should not be released while holds, missing documents, denied-party risk, or export-control blocks remain.

**Improvement:** Enforce release checks for approved HS classification, landed-cost quote, denied-party clearance, export-control clearance, document completeness, broker status, carrier readiness, duties/taxes, and hold resolution.

### 19. Broker handoff orchestration

**Justification:** Broker handoffs require payload completeness, filing readiness, retry handling, and response tracking.

**Improvement:** Track broker route, payload hash, filing method, submission state, response codes, correction requests, retry policy, broker SLA, and declaration linkage.

### 20. Carrier handoff readiness

**Justification:** Carriers require customs references, documents, labels, commercial invoices, and shipment constraints before cross-border movement.

**Improvement:** Validate carrier service, route, documents, customs reference, Incoterm obligations, restricted goods, handoff payload, carrier acknowledgement, and shipment-dispatch linkage.

### 21. Broker and carrier performance scoring

**Justification:** Broker and carrier choices affect clearance speed, cost, compliance risk, and customer experience.

**Improvement:** Score providers by acceptance rate, correction rate, clearance time, fee, delay, compliance exceptions, carbon profile, country coverage, and claim/escalation history.

### 22. Carbon-aware broker routing

**Justification:** Trade routing can reduce emissions through broker/carrier choice and consolidation when deadlines allow.

**Improvement:** Add carbon scoring for broker/carrier options with service deadline, clearance confidence, shipment urgency, cost, route emissions, consolidation, and override evidence.

### 23. Counterfactual landed-cost simulation

**Justification:** Trade teams need to compare origin, destination, Incoterm, carrier, broker, and duty scenarios before committing.

**Improvement:** Simulate alternate origins, destinations, Incoterms, declared values, carriers, brokers, trade programs, and duty treatments with total landed cost and compliance risk.

### 24. Duty and tax exposure forecasting

**Justification:** Cross-border margin and customer pricing need forward-looking duty, tax, FX, and policy exposure.

**Improvement:** Forecast duty/tax exposure by country, product, HS classification, trade lane, value band, exchange rate, policy change, and seasonality.

### 25. Trade program eligibility

**Justification:** Free trade agreements, preferential duties, bonded programs, and drawback can materially affect landed cost.

**Improvement:** Model trade program eligibility with origin rules, documentation, value thresholds, product scope, certification evidence, expiry, reviewer approval, and quote/declaration effects.

### 26. Country-of-origin evidence

**Justification:** Origin drives duties, restrictions, marking, and trade-program eligibility.

**Improvement:** Track origin source, supplier evidence, manufacturing country, substantial transformation rationale, certificate references, confidence, expiry, and declaration linkage.

### 27. Customs valuation controls

**Justification:** Incorrect customs values create duty underpayment, overpayment, penalties, and broker rejection.

**Improvement:** Add valuation checks for transaction value, assists, royalties, freight, insurance, discounts, related-party flag, currency conversion, and variance threshold.

### 28. Trade exception workflow

**Justification:** Exceptions arise from classification uncertainty, denied-party matches, missing documents, broker rejections, carrier blocks, and duty variances.

**Improvement:** Add exception cases with category, severity, affected declaration/quote, root cause, owner, SLA, recommended actions, evidence required, and closure proof.

### 29. Autonomous exception recommendation

**Justification:** Trade specialists need fast but controlled recommendations for complex compliance exceptions.

**Improvement:** Recommend next actions for missing document, classification review, license check, denied-party false positive, broker rejection, carrier hold, and duty variance with rationale and approval requirements.

### 30. Trade anomaly detection

**Justification:** Abnormal patterns can indicate misclassification, evasion risk, broker issues, fraud, or integration failures.

**Improvement:** Detect anomalies in HS code changes, duty variance, denied-party matches, document gaps, broker rejections, carrier handoff failures, declaration amendments, and dead-letter spikes.

### 31. Stochastic trade exposure model

**Justification:** Trade exposure spans duties, taxes, fines, holds, delays, rejected declarations, customer churn, and margin loss.

**Improvement:** Model exposure distributions by shipment, country, product, broker, carrier, value, party risk, classification confidence, and document completeness with mitigation.

### 32. Governed trade model evidence

**Justification:** Classification, risk, cost, and routing models affect compliance and financial outcomes.

**Improvement:** Track model purpose, training window, feature lineage, validation metrics, drift, false-clear/false-hold impact, approval status, rollback, and explainability evidence.

### 33. Cryptographic trade proof

**Justification:** Auditors, brokers, and counterparties may need proof of clearance, classification, or policy screening without full data exposure.

**Improvement:** Generate selective-disclosure proofs for classification, screening, declaration release, document completeness, landed-cost quote, and hold resolution with verifier and expiry.

### 34. Immutable trade audit trail

**Justification:** Customs audits require reconstruction of decisions, documents, filings, holds, and releases.

**Improvement:** Hash-chain classifications, quotes, screens, documents, broker handoffs, carrier handoffs, declarations, holds, releases, and AppGen-X event deliveries.

### 35. Dynamic trade policy screening

**Justification:** Trade policy varies by country, item, party, value, Incoterm, license, document status, and shipment route.

**Improvement:** Compile deterministic screening policies for classification, landed cost, denied parties, export control, documents, broker handoff, carrier handoff, holds, and declaration release.

### 36. AppGen-X inbox reliability

**Justification:** Order, inventory, payment, and shipment events are foundational inputs to trade execution.

**Improvement:** Add inbox schema validation, idempotency, duplicate suppression, retry evidence, unsupported-event rejection, dead-letter promotion, projection rebuild, and replay/quarantine controls.

### 37. AppGen-X outbox delivery assurance

**Justification:** Trade events must reliably reach order, shipment, carrier, broker, audit, customer, and finance flows.

**Improvement:** Add outbox state, ordering group, payload hash, retry attempts, next retry, delivery proof, dead-letter linkage, and replay controls for emitted trade events.

### 38. Cross-PBC boundary proof

**Justification:** Cross Border Trade must not directly read or write order, inventory, payment, shipment, broker, carrier, customer, or audit tables.

**Improvement:** Add release evidence scanning schema descriptors, services, routes, DSL, workbench bindings, and agent plans for foreign table access, proving dependencies are APIs, events, or projections only.

### 39. Runtime parameter governance

**Justification:** Classification thresholds, duty variance tolerance, denied-party thresholds, de minimis values, and routing weights change compliance outcomes.

**Improvement:** Add parameter bounds, impact simulation, approval workflow, effective dating, tenant/country overrides, rollback, and release evidence before parameter changes activate.

### 40. Schema extension governance

**Justification:** Trade operations need custom country, product, broker, carrier, and document fields while preserving owned boundaries.

**Improvement:** Allow extensions only on owned trade tables with field validation, sensitivity classification, migration preview, UI binding preview, API exposure review, and release-audit evidence.

### 41. Trade workbench coverage

**Justification:** Specialists need a complete compliance command center, not scattered classification and declaration tables.

**Improvement:** Expand workbench surfaces for classifications, landed cost, screening, documents, broker handoffs, carrier handoffs, declarations, holds, policies, events, rules, parameters, configuration, and release evidence.

### 42. Classification review console

**Justification:** Low-confidence HS classifications need expert review with evidence and alternatives.

**Improvement:** Add review queues with confidence, candidate codes, evidence snippets, prior decisions, duty impact, restriction impact, reviewer notes, and approval actions.

### 43. Declaration operations cockpit

**Justification:** Operators need real-time visibility into declaration readiness, broker response, carrier readiness, holds, and release status.

**Improvement:** Add cockpit views for declaration state, document packet, broker handoff, carrier handoff, duty/tax, holds, errors, release gates, and customer/shipment impact.

### 44. Denied-party screening panel

**Justification:** Screening teams need controlled match adjudication and audit-ready decisions.

**Improvement:** Add panels with party roles, match candidates, similarity factors, source lists, reviewer decisions, rescreen dates, hold linkage, and release evidence.

### 45. Continuous trade control testing

**Justification:** Trade compliance controls must run continuously, not just during release checks.

**Improvement:** Add assertions for declaration without classification, release with open hold, missing documents, stale screening, blocked country, unsupported Incoterm, foreign-table access, dead-letter aging, and agent-preview bypass.

### 46. Trade resilience drills

**Justification:** Cross-border execution must degrade safely through broker outages, carrier failures, duplicate events, and missing documents.

**Improvement:** Add drills for duplicate order event, inventory delay, payment delay, shipment dispatch replay, broker rejection, carrier acknowledgement failure, dead-letter recovery, and workbench degraded mode.

### 47. Crypto-agile trade authorization

**Justification:** Trade proofs and audit evidence need durable signatures and future key rotation.

**Improvement:** Add crypto epoch, signing profile, key rotation evidence, proof compatibility, revocation, and migration readiness across trade proofs and audit traces.

### 48. Agent-safe trade plans

**Justification:** The trade chatbot must not silently release declarations, override holds, or change classification and screening rules.

**Improvement:** Require side-effect-free plans naming command, permission, owned tables, idempotency key, expected event, compliance impact, financial impact, rollback limits, and human confirmation.

### 49. Cross Border Trade readiness score

**Justification:** Users need an evidence-backed view of whether `cross_border_trade` is ready for live customs and compliance execution.

**Improvement:** Compute readiness from classification, landed-cost quoting, screening, document packets, broker/carrier handoffs, declarations, holds, duties/taxes, event reliability, UI coverage, model governance, controls, boundary proof, and agent safety.

### 50. End-to-end customs release proof

**Justification:** A complete Cross Border Trade PBC must prove it can execute the full lifecycle from order event to customs release.

**Improvement:** Add an executable proof scenario covering order/inventory/payment/shipment event intake, HS classification, landed-cost quote, denied-party screening, export-control clearance, document packet, broker and carrier handoffs, declaration filing, hold resolution if needed, declaration release, emitted events, UI evidence, boundary proof, controls, and agent explanation.
