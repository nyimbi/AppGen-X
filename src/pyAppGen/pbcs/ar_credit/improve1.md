# Accounts Receivable and Credit PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `ar_credit`. The items are specific to accounts receivable and customer credit operations: customer credit governance, invoice issuance, tax evidence, revenue schedules, cash receipts, remittance parsing, cash application, deductions, disputes, collections, dunning, refunds, write-offs, statements, and agent-assisted AR work.

## Current Domain Evidence Used

- Domain purpose: quote-to-cash financial boundary after customer identity and fulfillment signals, including credit, invoices, receivable subledger, cash receipts, remittance interpretation, cash application, disputes, credit memos, refunds, write-offs, aging, dunning, statements, revenue schedules, credit decisions, e-invoice evidence, cross-border receivables, invoice finance, controls, rules, parameters, governed models, and workbench evidence.
- Owned boundary: customers, sites, customer graph, credit profiles, payment terms, risk signals, invoices, invoice lines, invoice tax, performance obligations, delivery confirmations, cash receipts, remittance advice, cash applications, unapplied cash, credit memos, write-offs, refunds, dispute cases, collection actions, dunning notices, statements, revenue schedules, cash pools, credit decisions, e-invoice submissions, cross-border receivables, invoice finance programs, rules, parameters, schema extensions, controls, governed models, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: customers, invoices, deliveries, remittance parsing, cash application, unapplied cash, credit memos, write-offs, refunds, disputes, collections, e-invoices, aging, statements, revenue schedules, runtime configuration, rules, parameters, and workbench views.
- Existing events and dependencies: emits customer, invoice, delivery, payment, unapplied cash, credit memo, write-off, refund, and collection events; consumes order, tax, treasury, identity, workflow, audit, and gateway signals only through APIs, AppGen-X events, and projections.

## 50 Better-Than-World-Class Improvements

### 1. Customer credit onboarding evidence pack

**Justification:** Credit exposure begins before the first invoice. A customer record without verified identity, payment terms, risk grade, credit authority, and related-party context cannot support controlled receivables growth.

**Improvement:** Add an onboarding evidence pack with customer identity projection, beneficial-owner graph, site validation, credit application, references, payment terms, tax profile, approved limit, reviewer, and activation decision. Block credit-enabled status until mandatory evidence is complete.

### 2. Credit limit lifecycle governance

**Justification:** Credit limits change with risk, payment behavior, order volume, seasonality, disputes, and macro conditions. A static limit field is not enough.

**Improvement:** Model credit limit requests, temporary limits, permanent limits, expiries, review cadence, approver authority, customer exposure, and override reasons. Store every credit decision with risk score, policy version, and expected exposure impact.

### 3. Customer exposure aggregation

**Justification:** Credit decisions need exposure across open invoices, unapplied cash, orders pending invoice, disputed amounts, credit memos, refunds, and related entities.

**Improvement:** Add exposure views by customer, parent, site, currency, aging bucket, disputed/open/secured amount, and pending order projection. Credit checks should use exposure snapshots with freshness evidence.

### 4. Related-party and parent-child credit graph

**Justification:** Customers may operate through subsidiaries, buying groups, franchised sites, or shared beneficial owners that concentrate credit risk.

**Improvement:** Expand customer graph records with parent hierarchy, guarantees, shared owners, shared payment instruments, site relationships, and risk propagation. Support group credit limits and local sublimits with explainable allocation.

### 5. Payment terms optimization

**Justification:** Terms affect DSO, bad debt, sales conversion, discount behavior, and working capital.

**Improvement:** Add term recommendation logic based on credit grade, historical payment behavior, margin, customer segment, country, dispute history, and treasury liquidity. Store counterfactual DSO and revenue impact for proposed term changes.

### 6. Invoice issuance completeness gate

**Justification:** Invoices should not be issued without required customer, delivery, tax, contract, performance obligation, and account evidence.

**Improvement:** Add an invoice readiness gate that checks customer status, credit hold, bill-to site, tax quote, delivery confirmation where required, line totals, revenue obligation mapping, and e-invoice jurisdiction rules before `InvoiceIssued`.

### 7. Invoice correction and cancellation lifecycle

**Justification:** Invoice mistakes require controlled cancellation, rebilling, credit memo, and audit linkage.

**Improvement:** Add correction records linking original invoice, correction reason, cancellation state, replacement invoice, credit memo, tax impact, revenue impact, and customer communication. Corrections should preserve immutable invoice history.

### 8. Performance obligation allocation

**Justification:** AR invoices may include bundled obligations whose revenue schedule differs from billing and cash timing.

**Improvement:** Add allocation controls for obligation identification, standalone selling price, satisfaction pattern, deferred revenue, recognized revenue, and schedule updates. Link invoice lines to revenue schedule lines with proof.

### 9. Delivery and acceptance evidence policy

**Justification:** Some invoices require shipment, service completion, milestone acceptance, or customer signoff before billing or revenue treatment.

**Improvement:** Add delivery evidence rules by product/service, contract, customer, and jurisdiction. Store delivery proof hash, acceptance status, exception reason, and invoice/revenue impact.

### 10. Tax and e-invoice clearance gate

**Justification:** AR invoices can be legally invalid if tax or electronic clearance rules are incomplete.

**Improvement:** Add jurisdiction-specific clearance checks for invoice fields, tax rates, invoice numbering, digital signatures, submission response, cancellation rules, and archival proof. Block dispatch where required clearance has not been accepted.

### 11. Invoice numbering and statutory sequence control

**Justification:** Many jurisdictions require strict invoice number sequences, gap handling, cancellation proof, and legal entity separation.

**Improvement:** Add sequence policies by entity, country, invoice type, and fiscal period. Track reserved, issued, cancelled, voided, and gap-explained numbers with release audit checks.

### 12. Receivable subledger to GL reconciliation

**Justification:** AR open balances, revenue, tax, cash, write-offs, refunds, and discounts must reconcile to GL without shared tables.

**Improvement:** Add reconciliation records comparing AR subledger balances and emitted GL handoff events, with variance classification, source invoice/cash/write-off links, and close-blocking status.

### 13. Cash receipt intake normalization

**Justification:** Receipts arrive from bank statements, lockboxes, cards, wallets, bank transfers, and payment processors with inconsistent references.

**Improvement:** Normalize all receipts into a canonical cash receipt record with source, bank reference, payer identity, currency, value date, fees, chargeback risk, and duplicate-detection evidence.

### 14. Semantic remittance parsing

**Justification:** Customers often send unstructured remittance text that references multiple invoices, deductions, credits, or disputes.

**Improvement:** Parse remittances into candidate invoice references, amounts, deductions, reason codes, confidence, source spans, and unresolved fragments. The agent should show citations and request review for low-confidence allocations.

### 15. Probabilistic cash application workbench

**Justification:** Automatic cash application must be explainable because wrong application damages customer balances and collections.

**Improvement:** Store candidate invoices, scores, tolerance rules, partial-payment treatment, currency match, remittance evidence, and final application decision. UI should support accept, split, reassign, park as unapplied, or open dispute.

### 16. Short-pay and deduction management

**Justification:** Customers frequently short-pay for claims, promotions, returns, taxes, service credits, or disputes.

**Improvement:** Add deduction records with reason, linked invoice lines, customer claim, supporting documents, approval path, expected recovery, write-off eligibility, and customer communication status.

### 17. Unapplied cash triage lifecycle

**Justification:** Unapplied cash distorts aging, customer statements, cash forecasts, and collections.

**Improvement:** Add triage categories for missing remittance, unknown payer, duplicate receipt, overpayment, refund candidate, customer credit, and bank error. Track owner, SLA, evidence, resolution action, and aging.

### 18. Credit memo governance

**Justification:** Credit memos reduce receivables and revenue and can be abused without policy controls.

**Improvement:** Add credit memo request, reason taxonomy, invoice linkage, tax impact, revenue impact, approval threshold, customer communication, and application policy. Require SoD approval for high-risk or manual credits.

### 19. Refund approval and payment handoff

**Justification:** Customer refunds require eligibility, bank/payment method verification, fraud controls, treasury funding, and GL handoff.

**Improvement:** Add refund lifecycle states with source credit/unapplied cash, customer verification, payment route, approval, idempotency, remittance, and settlement evidence. Integrate through declared treasury APIs/events.

### 20. Write-off policy and recovery controls

**Justification:** Write-offs affect bad debt, revenue quality, collections, and audit controls.

**Improvement:** Add write-off policies by amount, age, customer risk, dispute status, recovery exhaustion, and approver authority. Store recovery history, tax impact, GL handoff, and post-write-off monitoring.

### 21. Dispute case management

**Justification:** Disputes are multi-step cases involving reasons, documents, customer communication, internal owners, deductions, and resolution.

**Improvement:** Expand dispute cases with root cause, disputed lines, evidence, owner, customer contact, SLA, promised action, resolution decision, credit/write-off/refund linkage, and recurrence classification.

### 22. Collections strategy orchestration

**Justification:** Collection actions should adapt to customer risk, amount, relationship value, dispute status, geography, and communication preferences.

**Improvement:** Add strategy records with action sequence, channel, tone, timing, owner, escalation, legal handoff threshold, and pause rules. Use counterfactual simulations to compare DSO impact and customer-risk cost.

### 23. Dunning policy compiler

**Justification:** Dunning levels and messages vary by country, customer segment, dispute status, and legal requirements.

**Improvement:** Compile dunning rules with grace days, aging bucket, excluded invoices, required language, channel, notice content, and escalation behavior. Store proof of sent notices and customer responses.

### 24. Promise-to-pay management

**Justification:** Collections depends on tracking customer commitments and following up when promises are missed.

**Improvement:** Add promise records with promised amount, date, invoices, collector, customer contact, confidence, reminder schedule, kept/broken status, and effect on collection strategy.

### 25. Customer statement generation and proof

**Justification:** Statements must be accurate, explainable, and reconcilable to invoices, receipts, credits, disputes, and unapplied cash.

**Improvement:** Add statement generation with as-of date, included transactions, excluded disputes, balance hash, delivery channel, customer acknowledgement, and dispute initiation link.

### 26. Aging analytics with explainable buckets

**Justification:** Aging reports drive collections, reserves, covenants, and management reporting, so bucket assignment must be defensible.

**Improvement:** Store aging snapshots by invoice, due date, payment terms, dispute/hold status, customer, currency, and entity. Show why each item is in a bucket and how credits/unapplied cash affect exposure.

### 27. Bad-debt reserve recommendations

**Justification:** Credit losses require forward-looking assessment using aging, customer risk, disputes, macro signals, and payment behavior.

**Improvement:** Add reserve recommendation records with expected loss, model version, scenario, customer risk factors, manual overlay, approval, and GL handoff. Keep model governance and deterministic fallback.

### 28. Customer default prediction governance

**Justification:** Default scores influence credit holds and collections, so they need explainability and controls.

**Improvement:** Govern default models with feature lineage, drift, protected-feature exclusion evidence, override reason, review cadence, and confidence. Surface risk contributors in customer credit views.

### 29. Credit hold and release lifecycle

**Justification:** Credit holds affect order release, customer relationships, and revenue timing.

**Improvement:** Add hold records with cause, exposure, customer group, affected orders/invoices, release conditions, approver, expiry, and communication evidence. Emit AppGen-X events for downstream order gating.

### 30. Credit insurance and collateral tracking

**Justification:** Receivable risk can be mitigated by insurance, guarantees, deposits, letters of credit, and collateral.

**Improvement:** Add risk mitigation records with coverage amount, expiry, insured customer, deductible, claim process, collateral value, and credit-limit effect. Include coverage in exposure calculations.

### 31. Cross-border receivables controls

**Justification:** International receivables involve currency, local invoicing, withholding, collection laws, settlement timing, and banking restrictions.

**Improvement:** Add cross-border requirements by country/currency, including e-invoice, tax, payment method, FX exposure, local collection constraints, and settlement proof. Flag invoices with incomplete cross-border evidence.

### 32. FX exposure and realized gain/loss handoff

**Justification:** Foreign-currency invoices and receipts create exposure and realized/unrealized gains or losses.

**Improvement:** Track invoice currency, functional currency, rates, revaluation exposure, receipt rate, realized gain/loss, and GL handoff evidence. Connect exposure to treasury projections through declared contracts.

### 33. Invoice finance program lifecycle

**Justification:** Receivables can be financed, sold, pledged, or factored, changing cash, risk, and customer communication.

**Improvement:** Add finance program records with eligible invoices, advance rate, counterparty, recourse/non-recourse status, fees, assignment notice, settlement, and accounting handoff.

### 34. Chargeback and payment reversal management

**Justification:** Card, wallet, and bank payments can be reversed or charged back after cash application.

**Improvement:** Add reversal lifecycle with original receipt, reason, dispute evidence, response deadline, provisional status, recovered/lost outcome, and invoice reopening logic.

### 35. Lockbox and bank file reconciliation

**Justification:** High-volume AR depends on reconciling bank/lockbox files, receipt batches, and remittance details.

**Improvement:** Add file ingestion evidence, batch totals, line totals, duplicate files, rejected lines, correction workflow, and proof that bank totals equal created receipts.

### 36. Customer communication workspace

**Justification:** Collections, disputes, statements, refunds, and credit holds need controlled communication history.

**Improvement:** Add communication records linked to customer, invoice, dispute, collection action, statement, or promise-to-pay with channel, template, send proof, response summary, and next action.

### 37. AR close cockpit

**Justification:** AR close requires visibility into unissued invoices, unapplied cash, disputes, write-offs, revenue schedules, tax exceptions, and GL reconciliation.

**Improvement:** Add close dashboards by entity/period showing open blockers, subledger-to-GL reconciliation, aging snapshots, reserve recommendations, e-invoice failures, and revenue schedule exceptions.

### 38. Revenue-to-cash forecasting

**Justification:** AR is a core input to liquidity and revenue planning.

**Improvement:** Forecast collections by customer, invoice, due date, payment behavior, dispute state, collection strategy, and macro risk. Publish forecast projections with confidence intervals and freshness evidence.

### 39. Collection effectiveness analytics

**Justification:** Teams need to know which strategies improve DSO, reduce bad debt, and preserve customer relationships.

**Improvement:** Track action-to-outcome metrics by collector, channel, customer segment, aging bucket, dispute type, and promise-to-pay behavior. Recommend strategy improvements with evidence.

### 40. Customer portal AR task queue

**Justification:** Customers can resolve remittance gaps, disputes, statement questions, and payment promises faster through structured tasks.

**Improvement:** Add customer-facing task descriptors for missing remittance, dispute documentation, statement acknowledgement, payment promise, refund information, and credit application updates. Keep mutations behind AR-owned review workflows.

### 41. Agent-safe cash application

**Justification:** The AR chatbot should help apply cash, but incorrect application is financially damaging.

**Improvement:** Define agent previews for cash application with receipt, candidate invoices, confidence, unapplied impact, customer statement impact, and reversal path. Require human confirmation below confidence or above materiality thresholds.

### 42. Agent-safe collections assistance

**Justification:** Collection messages affect customer relationships and legal posture.

**Improvement:** Give the agent skills to draft collection actions, dispute summaries, statement explanations, and promise follow-ups from owned evidence. Require policy checks for tone, jurisdiction, disputed invoices, and contact permissions before sending.

### 43. Agent-safe credit decisions

**Justification:** Credit changes can block orders or increase bad-debt exposure.

**Improvement:** Require credit decision previews showing exposure, limit, risk factors, payment history, open disputes, mitigation, model confidence, and approval route. Agent actions should draft recommendations, not directly change limits without authority.

### 44. Rules and parameter simulation

**Justification:** Cash thresholds, credit buffers, dunning grace days, write-off limits, and collection risk thresholds materially change AR outcomes.

**Improvement:** Simulate rule/parameter changes against historical and open receivables. Show impact on auto-application rate, unapplied cash, collection workload, write-offs, credit holds, DSO, and release blockers.

### 45. Continuous AR controls

**Justification:** AR controls should run continuously, not only at month end.

**Improvement:** Add control assertions for open amount integrity, receipt application, write-off approval, refund approval, credit-limit breach, aging completeness, e-invoice acceptance, and subledger reconciliation.

### 46. Boundary proof for AR-only ownership

**Justification:** AR must integrate with order, tax, treasury, GL, workflow, identity, and audit without direct table access.

**Improvement:** Add static/runtime checks proving every command uses only AR-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 47. Workbench surface for all AR capabilities

**Justification:** AR specialists need operational surfaces for every major workflow, not hidden backend commands.

**Improvement:** Expand UI into credit cockpit, invoice issuance, cash application, unapplied cash, dispute board, collections planner, dunning console, statement generator, refunds/write-offs, revenue schedule view, close cockpit, analytics, and agent assistant.

### 48. Customer-facing explanation packets

**Justification:** Customers often need understandable explanations for balances, disputes, credits, dunning, and statements.

**Improvement:** Generate explanation packets from invoices, receipts, credits, disputes, promises, and statements with redaction and approved wording. Store delivery proof and customer acknowledgement.

### 49. AR release readiness score

**Justification:** Users need a defensible measure of whether AR is complete enough for production finance operations.

**Improvement:** Compute readiness from customer evidence, credit governance, invoice readiness, cash application accuracy, dispute aging, collection controls, refund/write-off approvals, revenue schedules, GL/treasury/tax handoffs, UI coverage, and agent safety.

### 50. End-to-end order-to-cash trace

**Justification:** AR excellence depends on tracing customer obligation from order/delivery through invoice, tax, revenue, receipt, application, dispute, collection, GL, and statement.

**Improvement:** Build an order-to-cash trace view using AR-owned records and declared projections. The agent should answer status and balance questions from this trace with source evidence and confidence.
