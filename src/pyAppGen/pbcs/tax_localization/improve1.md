# Tax Localization PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `tax_localization`. The items are specific to tax compliance and localization operations: jurisdiction topology, nexus, product taxability, indirect tax calculation, invoice tax evidence, exemptions, reverse charge, withholding, cross-border duties, environmental levies, digital tax documents, filings, remittance, authority notices, reconciliation, audit proof, and agent-assisted tax work.

## Current Domain Evidence Used

- Domain purpose: tax compliance, localization, indirect tax calculation, jurisdiction topology, authority connectivity, nexus profiles, product taxability, counterparty tax profiles, exemption evidence, invoice tax, cross-border duties, reverse charge, withholding, environmental levies, filings, remittance, payment evidence, refunds, notices, digital tax documents, audit proofs, rules, parameters, configuration, UI fragments, and release evidence.
- Owned boundary: jurisdictions, topology, authority channels/submissions, filing calendars, nexus profiles, tax rules/versions/impact analyses, product taxability, counterparty tax profiles, exemption reviews/certificates, calculations/lines, invoice tax records, reverse charge, withholding, environmental levies, cross-border duties, duty classifications, landed-cost components, filings/lines, reconciliations, remittance batches, payment evidence, refund claims, adjustments, notices, digital tax documents, document parses, liability forecasts, policy simulations, federation, identity credentials, audit proofs, allocations, anomaly signals, model registries, rules, parameters, configuration, controls, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: jurisdictions, rules, quotes, invoice tax records, filings, AppGen-X inbox, tax workbench, configuration, parameters, governance rules, tax rules, schema extensions, and release evidence.
- Existing events and dependencies: emits `TaxJurisdictionRegistered`, `TaxRuleActivated`, `TaxCalculated`, `InvoiceTaxRecorded`, and `TaxFilingPrepared`; consumes product, invoice, order, payment, and access-policy events through AppGen-X projections and declared APIs only.

## 50 Better-Than-World-Class Improvements

### 1. Jurisdiction topology lifecycle

**Justification:** Tax jurisdiction is not a flat country code. Rates, authorities, filing calendars, local taxes, home-rule cities, and parent-child relationships change over time.

**Improvement:** Add jurisdiction topology lifecycle records with country, region, locality, authority, parent jurisdiction, effective dates, currency, tax types, risk level, and retirement state. Calculation and filing should always reference the topology version used.

### 2. Authority channel certification

**Justification:** Digital tax and filing submissions depend on authority endpoints, credentials, formats, service levels, maintenance windows, and acknowledgements.

**Improvement:** Add authority-channel certification with endpoint type, credential evidence, supported document types, retry policy, SLA, sandbox/prod status, certificate expiry, and fallback route. Block production submission through uncertified channels.

### 3. Filing calendar intelligence

**Justification:** Filing due dates depend on frequency, holidays, weekends, local rules, fiscal calendars, extensions, and authority downtime.

**Improvement:** Add filing-calendar generation with period rules, due-day logic, holiday adjustment, extension evidence, authority blackout windows, and alert thresholds. The workbench should show upcoming filings and late-risk reasons.

### 4. Nexus threshold monitoring

**Justification:** Tax obligations begin or change when sales, transaction count, payroll, inventory, marketplace activity, or physical presence crosses thresholds.

**Improvement:** Add nexus threshold monitors by jurisdiction and entity, including threshold basis, measurement period, projected crossing date, supporting transaction projections, and registration workflow trigger.

### 5. Registration and deregistration workflow

**Justification:** Tax compliance requires controlled registration with authorities and deregistration when obligations end.

**Improvement:** Add registration lifecycle records with jurisdiction, tax type, registration number, effective date, evidence, authority acknowledgement, responsible owner, and deregistration conditions. Link active registration to calculation and filing eligibility.

### 6. Tax rule effective-date compiler

**Justification:** Tax rules change frequently and must be applied by transaction date, invoice date, ship date, service date, or payment date depending on jurisdiction.

**Improvement:** Compile rule versions with effective/expiry dates, trigger date basis, precedence, product class, counterparty class, rate, exemptions, and reverse-charge behavior. Store compiled hashes and rule fixtures.

### 7. Tax rule impact simulation

**Justification:** Rate and rule changes affect open quotes, invoices, filings, remittances, and customer pricing.

**Improvement:** Simulate proposed rule changes against historical and open transaction projections, showing tax delta, affected jurisdictions, products, customers, invoices, filing lines, and release blockers.

### 8. Product taxability evidence workflow

**Justification:** Product taxability is one of the highest-error areas in indirect tax and depends on product attributes, use, jurisdiction, and authority guidance.

**Improvement:** Add taxability decisions with product class, jurisdiction, evidence source, confidence, reviewer, effective dates, and uncertain classification state. Route low-confidence or high-risk classes to specialist review.

### 9. Taxability model governance

**Justification:** AI-assisted product classification affects legal obligations and must be explainable.

**Improvement:** Govern taxability models with feature lineage, training data class, drift, excluded features, deterministic fallback, confidence thresholds, and human override evidence. Release audit should fail if high-risk classifications lack review.

### 10. Counterparty tax profile completeness

**Justification:** Customer/vendor tax treatment depends on registrations, exemptions, use type, residency, reverse-charge status, and withholding eligibility.

**Improvement:** Add counterparty profile completeness gates with registration IDs, tax residency, exemption status, certificate links, use codes, treaty eligibility, and expiry warnings. Tax quotes should show missing profile evidence.

### 11. Exemption certificate lifecycle

**Justification:** Exemptions must be valid for jurisdiction, customer, product, date, and transaction purpose, and certificates expire or are revoked.

**Improvement:** Add certificate intake, parsing, validation, jurisdiction scope, product/use restrictions, expiry, renewal reminders, revocation, and audit proof. Block exempt treatment when evidence is stale or out of scope.

### 12. Exemption review queue

**Justification:** Tax specialists need to review questionable or ambiguous exemption evidence before invoices are finalized.

**Improvement:** Add review tasks with certificate extract, transaction impact, missing fields, confidence, due date, reviewer, decision, and customer communication evidence.

### 13. Quote-time tax calculation trace

**Justification:** Tax quotes must be fast and explainable, especially when rates, exemptions, nexus, and product taxability interact.

**Improvement:** Store calculation traces with jurisdiction path, rule versions, taxable basis, exemptions, sourcing decision, rounding, currency, and confidence. Return user-readable reasons for every tax line.

### 14. Invoice tax recording lock

**Justification:** Invoice tax should be immutable once issued except through controlled adjustments or credit/rebill flows.

**Improvement:** Add invoice tax state transitions for quoted, recorded, adjusted, reversed, credited, and reported. Adjustments must link to original calculation, reason, approval, and filing impact.

### 15. Tax rounding and precision policy

**Justification:** Rounding rules differ by jurisdiction, document type, currency, line/header level, and filing return.

**Improvement:** Add rounding policies with precision, mode, line/header basis, currency minor unit, and reconciliation tolerance. Tax calculations and filing lines should cite the rounding policy used.

### 16. Sourcing rule engine

**Justification:** Tax jurisdiction often depends on ship-from, ship-to, bill-to, service location, origin, destination, marketplace, and digital delivery rules.

**Improvement:** Add sourcing rules with precedence, address evidence, digital goods treatment, service situs, marketplace facilitator behavior, and fallback decision. Tax quotes should surface sourcing uncertainty.

### 17. Marketplace facilitator handling

**Justification:** Marketplace transactions can shift collection/remittance obligation from seller to marketplace.

**Improvement:** Add facilitator rules with marketplace identity, jurisdiction registration, transaction type, collection party, reporting party, and proof. Filing reconciliation should separate seller-collected and marketplace-collected tax.

### 18. Reverse-charge determination

**Justification:** Reverse charge depends on counterparty registration, cross-border rules, service/goods type, and document wording.

**Improvement:** Add reverse-charge decision records with registration validation, jurisdiction rule, product/service class, invoice disclosure text, and reporting box mapping.

### 19. Withholding tax determination

**Justification:** Withholding depends on income type, treaty, residency, certificate, payment date, and gross-up rules.

**Improvement:** Add withholding decisions with income type, treaty article, rate, base, certificate evidence, gross-up method, payment link, and remittance obligation. Integrate AP/AR through projections only.

### 20. Environmental levy and fee engine

**Justification:** Product taxes increasingly include battery, packaging, carbon, recycling, plastic, and other levies.

**Improvement:** Add levy rules with product attributes, unit basis, weight/volume, jurisdiction, exemptions, rates, and filing mapping. Calculation lines should distinguish tax, duty, levy, and fee.

### 21. Cross-border duty classification

**Justification:** Duties depend on HS classification, origin, destination, value, Incoterms, preference programs, and documentation.

**Improvement:** Add duty classification records with HS code, confidence, origin rule, preference eligibility, document evidence, landed-cost basis, and reviewer approval for uncertain classifications.

### 22. Landed cost calculation

**Justification:** Cross-border pricing and inventory valuation need duties, taxes, freight, insurance, brokerage, and fees.

**Improvement:** Add landed-cost component calculations linked to order/shipments projections, with duty, import VAT/GST, brokerage, freight allocation, currency conversion, and proof.

### 23. Digital tax document lifecycle

**Justification:** Many jurisdictions require digital invoice clearance, QR codes, fiscal signatures, cancellation, or buyer acknowledgement.

**Improvement:** Add digital document states for draft, submitted, accepted, rejected, cancelled, corrected, archived, and expired. Store authority acknowledgement, signature, QR/hash, validation errors, and retry evidence.

### 24. Authority acknowledgement reconciliation

**Justification:** Submissions are incomplete until authority acknowledgement is matched, interpreted, and reflected in tax state.

**Improvement:** Add acknowledgement matching by submission id, document id, authority status, timestamp, rejection reason, retry eligibility, and affected invoices/filings. Surface stale pending acknowledgements as operational risk.

### 25. Filing preparation workbench

**Justification:** Tax filings require aggregation, exclusions, adjustments, credits, exemptions, remittances, and approvals.

**Improvement:** Add filing prep workbench with source calculation lines, filing boxes, jurisdiction totals, adjustments, prior-period corrections, reconciliation status, approval state, and submit readiness.

### 26. Filing line provenance

**Justification:** Every filing number should trace to calculation lines, invoice tax records, adjustments, and payments.

**Improvement:** Store filing-line provenance with source record ids, tax types, jurisdiction, period, calculation hash, and inclusion/exclusion reason. Auditors should drill from filing total to transaction evidence.

### 27. Filing amendment and correction workflow

**Justification:** Tax filings often require amendments due to late invoices, corrections, authority notices, or exemption changes.

**Improvement:** Add amendment records with original filing, corrected lines, reason, authority procedure, payment/refund delta, approval, and audit proof. Preserve original submitted filing evidence.

### 28. Tax remittance batch controls

**Justification:** Remittance batches move cash and must reconcile to filings, liabilities, payment evidence, and bank settlement.

**Improvement:** Add remittance controls for jurisdiction, period, due date, amount, payment route, approval, bank reference, authority acknowledgement, and under/overpayment handling.

### 29. Tax payment evidence reconciliation

**Justification:** Payment evidence must reconcile to filing liability and treasury settlement.

**Improvement:** Add reconciliation between filing liability, remittance batch, tax payment evidence, bank statement projection, and authority acknowledgement. Flag variances and stale payment proofs.

### 30. Tax refund claim management

**Justification:** Refunds need eligibility, documentation, authority submission, expected cash timing, and dispute handling.

**Improvement:** Add refund claim lifecycle with source overpayment/credit, jurisdiction, filing period, documents, claim amount, submission, expected receipt, received amount, and appeal state.

### 31. Authority notice case management

**Justification:** Notices, audits, penalties, and inquiries require structured case handling and evidence.

**Improvement:** Add notice cases with authority, jurisdiction, period, issue type, due date, penalty exposure, assigned owner, response documents, resolution, and follow-up control.

### 32. Tax reconciliation control framework

**Justification:** Collected, accrued, reported, remitted, refunded, and adjusted tax must reconcile by jurisdiction and period.

**Improvement:** Add reconciliation controls comparing calculation totals, invoice tax records, filing lines, remittance evidence, refunds, and GL handoff events. Open variances should block filing or close where policy requires.

### 33. Tax liability forecasting

**Justification:** Treasury and finance need expected tax cash outflows and tail risk before filing deadlines.

**Improvement:** Forecast liabilities by jurisdiction, entity, tax type, period, confidence, open transaction volume, rule changes, and refund/notice exposure. Publish projection freshness and assumptions.

### 34. Counterfactual policy simulation

**Justification:** Tax teams need to evaluate rate changes, nexus expansion, product reclassification, exemption expiry, and filing frequency changes before they hit operations.

**Improvement:** Add policy simulations with scenario assumptions, affected tax quotes, invoices, filings, remittance cash, customer pricing, and compliance workload.

### 35. Tax anomaly detection

**Justification:** Tax errors often appear as unusual rate usage, exempt spikes, jurisdiction gaps, filing variances, or authority rejections.

**Improvement:** Add anomaly signals by jurisdiction, product class, counterparty, exemption, rate, filing box, and submission channel. Each anomaly should have an explanation and suggested investigation path.

### 36. Audit proof and disclosure minimization

**Justification:** Tax audits need detailed evidence, but not every reviewer should see all commercial transaction details.

**Improvement:** Generate proof bundles for calculations, exemptions, filings, remittances, and digital documents with minimized claims, hashes, disclosed fields, verifier instructions, and expiry.

### 37. Tax identity credential lifecycle

**Justification:** Authority and counterparty tax identities must be verified and revocation-aware.

**Improvement:** Add credentials for tax authorities, taxpayers, counterparties, representatives, and submission channels with issuer, validity, revocation, assurance level, and use scope.

### 38. Localized invoice disclosure text

**Justification:** Jurisdictions require specific invoice wording for exemptions, reverse charge, withholding, fiscalization, and customer rights.

**Improvement:** Add localized disclosure text rules with language, tax type, condition, effective date, and required placement. Invoice tax records should cite the disclosure rule used.

### 39. Multi-language authority document parsing

**Justification:** Certificates, notices, and authority responses arrive in many languages and formats.

**Improvement:** Add document parsing with language detection, field extraction, confidence, source spans, translation evidence, and human review for low-confidence tax facts.

### 40. Tax agent safe calculation assistance

**Justification:** The tax chatbot can help calculate and explain tax, but incorrect tax output has regulatory impact.

**Improvement:** Require agent calculation previews with jurisdiction, sourcing, rule versions, taxability, exemptions, rates, basis, confidence, and caveats. Low-confidence outputs should be marked draft and routed to review.

### 41. Agent-safe filing preparation

**Justification:** Filing submissions are legally significant and should not be autonomously filed from a chat instruction.

**Improvement:** Define agent competencies for filing prep, variance explanation, notice summarization, and evidence gathering. Filing submission should require explicit authorized human approval with previewed totals and proof.

### 42. Agent-safe tax document ingestion

**Justification:** AI can extract certificates, notices, and authority acknowledgements, but extracted facts must be traceable and reviewable.

**Improvement:** Add ingestion previews with extracted fields, confidence, source citations, affected records, validation errors, and required approvals before creating certificate, notice, or submission records.

### 43. Tax rules and parameter simulation

**Justification:** Precision, reconciliation tolerance, retry limits, exemption warning days, and nexus thresholds materially change compliance outcomes.

**Improvement:** Simulate rule/parameter changes against historical and open tax records, showing changes in tax quotes, filing variances, authority retries, exemption warnings, nexus triggers, and workload.

### 44. Cross-PBC tax boundary proof

**Justification:** Tax must integrate with products, invoices, orders, payments, identity, and audit without sharing their operational tables.

**Improvement:** Add static/runtime checks proving every command uses only tax-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 45. Tax authority resilience drills

**Justification:** Authority channels fail or reject submissions during deadlines, and the PBC must degrade safely.

**Improvement:** Add drills for authority outage, credential expiry, duplicate submission, rejected digital document, delayed acknowledgement, and dead-letter replay. Store recovery path and filing-risk evidence.

### 46. Continuous tax controls

**Justification:** Compliance needs continuous controls, not just filing-time review.

**Improvement:** Add control assertions for expired exemptions, missing nexus review, inactive tax rules, filing-calendar gaps, unreconciled tax, unaccepted digital documents, overdue notices, and boundary violations.

### 47. Tax workbench coverage for all capabilities

**Justification:** Tax specialists need end-to-end surfaces for jurisdiction, rules, calculation, filing, remittance, notices, and evidence.

**Improvement:** Expand UI into jurisdiction topology, authority channels, nexus monitor, rule editor, taxability workbench, exemption queue, quote trace, invoice tax, cross-border duty, filing cockpit, remittance, notices, audit proof, model governance, and agent panels.

### 48. Tax release readiness score

**Justification:** Users need a concise measure of whether tax localization is complete enough for production compliance.

**Improvement:** Compute readiness from jurisdiction coverage, active rules, nexus profiles, taxability confidence, exemption validity, calculation traceability, filing readiness, remittance reconciliation, authority channel health, UI coverage, boundary proof, and agent safety.

### 49. End-to-end tax obligation trace

**Justification:** Tax compliance requires tracing obligation from product/order/invoice/payment through calculation, document, filing, remittance, notice, and audit proof.

**Improvement:** Build an obligation trace view using tax-owned records and declared projections. The agent should answer why tax was charged, exempted, reversed, withheld, filed, or remitted from this trace.

### 50. Tax localization pack governance

**Justification:** Complete localization depends on curated jurisdiction packs containing rates, rules, forms, authority channels, text, calendars, and tests.

**Improvement:** Add localization pack metadata with jurisdiction, version, included rules, forms, document text, filing calendars, authority channels, fixtures, effective dates, and release evidence. Packages should be tested before activation.
