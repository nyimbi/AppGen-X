# Treasury and Cash Management PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `treasury_cash`. The items are specific to treasury operations: bank account governance, bank connectivity, statement ingestion, cash positioning, forecasting, liquidity optimization, sweeps, concentration, intercompany netting, in-house banking, payment funding, debt, investments, FX exposure, covenants, counterparty risk, and agent-assisted treasury work.

## Current Domain Evidence Used

- Domain purpose: enterprise cash visibility, bank connectivity, statement ingestion, reconciliation, cash positioning, forecasting, liquidity planning, payment funding, payment-rail routing, cash sweeping, concentration, intercompany netting, in-house banking, FX exposure, hedge recommendations, debt facilities, investments, bank fees, counterparty risk, covenant evidence, working-capital finance, cross-border liquidity, controls, rules, parameters, configuration, governed models, and treasury workbench evidence.
- Owned boundary: bank accounts, signatories, bank counterparties, bank topology, balances, intraday balances, statements, statement lines, reconciliation matches/exceptions, cash positions, forecasts, liquidity pools/plans, sweep instructions, concentration runs, intercompany netting, in-house bank accounts, payment funding, payment rail routes, FX exposure, hedge recommendations, capital actions, debt facilities/draws, investments, bank fees, covenant proofs, cross-border liquidity, working-capital finance, risk signals, rules, parameters, configuration, schema extensions, controls, governed models, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: bank accounts, balances, statements, reconciliation, cash position, forecasts, liquidity optimization, payment-rail routing, investments, debt draws, FX hedge recommendations, AppGen-X inbox handling, configuration, rules, parameters, and workbench views.
- Existing events and dependencies: emits `BankAccountRegistered`, `BankBalanceCaptured`, `BankStatementIngested`, `CashPositionBuilt`, `PaymentFunded`, `InvestmentPlaced`, and `DebtFacilityDrawn`; consumes payment funding, receivable forecast, payable payment, payroll funding, tax payment, FX rate, and access policy events through declared APIs/projections.

## 50 Better-Than-World-Class Improvements

### 1. Bank account opening and closing governance

**Justification:** Bank accounts are high-risk treasury assets with signatories, mandates, fees, currencies, legal entities, and regulatory exposure. A generic account record cannot prove control over opening, activation, suspension, and closure.

**Improvement:** Add bank account lifecycle workflows for requested, due-diligence, mandate-approved, open, active, restricted, suspended, closing, and closed states. Store legal entity, purpose, currency, bank mandate, signatory approval, KYC evidence, fee schedule, closure proof, and audit events.

### 2. Bank mandate and signatory authority controls

**Justification:** Treasury signatory authority determines who can move cash and approve funding, sweeps, investments, and debt draws.

**Improvement:** Add mandate records with signer role, approval limits, dual-approval requirements, validity dates, jurisdiction, bank confirmation, emergency signer rules, and deactivation evidence. Payment funding should validate active mandate authority before release.

### 3. Bank counterparty exposure aggregation

**Justification:** Cash concentration at one bank or country creates counterparty and sovereign risk.

**Improvement:** Aggregate exposure by bank, country, rating, currency, legal entity, account type, deposit tenor, investment instrument, and committed facility. Show limit utilization and breach risk in the counterparty risk view.

### 4. Bank topology graph and failure impact

**Justification:** Treasury needs to know how accounts, signatories, pools, sweeps, rails, banks, and entities depend on one another during bank outages or sanctions.

**Improvement:** Build a bank topology graph with accounts, counterparties, signatories, rails, pools, sweeps, in-house bank links, and risk propagation. Simulate bank outage or country restriction impact on funding and liquidity.

### 5. Bank connectivity channel registry

**Justification:** Statement and payment connectivity differs by host-to-host, API, file upload, bank portal, lockbox, and payment network.

**Improvement:** Add connectivity channel descriptors with bank, protocol class, file format, schedule, credential/mandate evidence, encryption policy, expected latency, and fallback channel. Statement ingestion should cite the channel used.

### 6. Statement ingestion completeness proof

**Justification:** Cash visibility fails if bank statement files are missing, duplicated, truncated, or out of order.

**Improvement:** Add statement control totals, sequence checks, opening/closing balance continuity, duplicate file detection, missing-date alerts, line hash chains, and source channel proof. Block cash-position finalization when critical statements are incomplete.

### 7. Intraday balance freshness scoring

**Justification:** Intraday liquidity decisions depend on freshness and reliability of bank balances.

**Improvement:** Score balances by source, timestamp, bank SLA, expected update cadence, account criticality, and reconciliation state. Cash position views should display freshness and degrade confidence when balances are stale.

### 8. Value-date cash positioning

**Justification:** Treasury makes decisions by value date, not merely accounting date or posting timestamp.

**Improvement:** Add value-date position logic that combines opening balances, intraday balances, forecast flows, settlements, bank cutoffs, sweeps, and restricted cash. Provide as-of and projected positions by entity, bank, account, and currency.

### 9. Restricted cash and trapped cash classification

**Justification:** Not all cash is available for liquidity; restrictions, local controls, debt covenants, taxes, and repatriation barriers matter.

**Improvement:** Add restricted/trapped cash records with reason, jurisdiction, expiry, release condition, covenant link, and repatriation feasibility. Liquidity plans should distinguish available, restricted, trapped, and pledged cash.

### 10. Bank statement narrative intelligence

**Justification:** Statement narratives drive reconciliation, cash application, fees, fraud detection, and forecast variance analysis.

**Improvement:** Parse narratives into payer/payee, reference, charge type, payment rail, bank fee, counterparty, confidence, and source span. Store semantic evidence and route ambiguous lines to reconciliation exceptions.

### 11. Autonomous bank reconciliation with explainability

**Justification:** Automated reconciliation must explain why a statement line matched a funding request, AP payment, AR receipt, payroll run, tax payment, fee, or sweep.

**Improvement:** Store match candidates, confidence, matching features, tolerance rules, timing differences, currency conversion, and final decision. UI should allow accept, split, reject, defer, or open exception with audit proof.

### 12. Reconciliation exception lifecycle

**Justification:** Unmatched bank lines can represent fraud, bank error, missing AP/AR records, fee surprises, or timing gaps.

**Improvement:** Expand exceptions with category, owner, SLA, suspected source, bank contact, required evidence, resolution action, GL/AR/AP handoff, and recurrence flag. The agent should summarize exceptions and propose safe next steps.

### 13. Cash forecast contributor model

**Justification:** Forecast quality depends on AP, AR, payroll, tax, debt, investment, FX, manual adjustments, and confidence bands.

**Improvement:** Model each forecast line with source projection, confidence, scenario, value date, currency, committed/probable/manual status, and forecast owner. Forecast workbench should show contributor freshness and variance.

### 14. Forecast variance and learning loop

**Justification:** Treasury forecasts improve only when actual cash movements are compared to expected flows.

**Improvement:** Add variance records comparing forecast lines to bank statements and settlements by source, value date, amount, currency, and reason. Feed variance into governed forecast model monitoring.

### 15. Scenario-based liquidity planning

**Justification:** Treasurers need to model downside collections, accelerated payables, bank outage, FX shock, facility draw, and trapped-cash scenarios.

**Improvement:** Add liquidity scenarios with assumptions, affected flows, confidence, stress severity, funding options, covenant impact, and management recommendation. Preserve baseline versus scenario deltas.

### 16. Minimum liquidity buffer governance

**Justification:** Liquidity buffers are policy decisions varying by entity, currency, region, risk, and covenant requirements.

**Improvement:** Add buffer policies with target, floor, warning threshold, currency, entity, effective dates, and breach actions. Cash position and funding plans should flag projected breaches and recommended mitigations.

### 17. Liquidity pool optimization

**Justification:** Cash pools need target balances, sweep thresholds, bank fees, FX impact, legal constraints, and counterparty risk.

**Improvement:** Optimize pools across target balances, entity constraints, restricted cash, bank limits, sweep cost, FX exposure, and concentration risk. Store rejected alternatives and reason codes.

### 18. Sweep instruction lifecycle

**Justification:** Sweeps move cash and can violate mandates, cutoffs, restrictions, or liquidity needs if uncontrolled.

**Improvement:** Add sweep states from proposed to approved, transmitted, settled, failed, reversed, and cancelled. Include source/target validation, cutoff windows, mandate authority, rail, fee, and settlement proof.

### 19. Cash concentration run controls

**Justification:** Concentration runs aggregate many sweeps and can create large counterparty exposure.

**Improvement:** Add run-level controls for included accounts, excluded accounts, target pool, total swept, failed sweeps, exposure after run, approval, and reconciliation proof. UI should show before/after cash topology.

### 20. Intercompany netting engine

**Justification:** Intercompany netting reduces cash movement and FX cost but requires entity rules, tax/legal constraints, and settlement proof.

**Improvement:** Add netting cycles, participants, receivable/payable projections, net amounts, currency conversion, dispute handling, approvals, settlement instruction, and GL handoff evidence.

### 21. In-house banking subledger

**Justification:** In-house banking creates internal accounts, interest, settlements, and entity-level balances.

**Improvement:** Add internal account statements, interest calculation, entity balances, internal transfers, overdraft limits, and reconciliation to external bank accounts. Keep all state treasury-owned with declared GL handoff events.

### 22. Payment funding reservation

**Justification:** AP, payroll, tax, and other payment runs need funding certainty without double-reserving the same cash.

**Improvement:** Add funding reservations with source request, value date, account, amount, currency, expiry, priority, approval, and release/cancel state. Cash positions should show reserved versus free liquidity.

### 23. Payment rail route governance

**Justification:** Payment route selection affects cost, speed, cutoffs, bank risk, sanctions, and resiliency.

**Improvement:** Score rails by account availability, mandate, cutoff, currency, country, cost, latency, risk, outage state, and fallback. Store route decision evidence and require approval for high-value failover.

### 24. Treasury payment idempotency ledger

**Justification:** Duplicate funding or payment routing decisions can cause duplicate cash movements.

**Improvement:** Add idempotency records for funding request, route selection, bank transmission, acknowledgement, settlement, and reversal. Duplicate requests should return prior state rather than create new funding movements.

### 25. Investment policy and placement controls

**Justification:** Treasury investments must obey counterparty, tenor, instrument, yield, liquidity, and concentration policies.

**Improvement:** Add investment policy checks for eligible instruments, maturity ladder, issuer limits, currency, yield, liquidity needs, and approval limits. Store rejected investments and projected liquidity impact.

### 26. Investment maturity ladder

**Justification:** Maturity timing affects liquidity, reinvestment risk, interest income, and covenant compliance.

**Improvement:** Add maturity ladder views with expected principal, interest, counterparty, currency, reinvestment assumption, and cash forecast linkage. Alert on liquidity gaps caused by maturity concentration.

### 27. Debt facility covenant and draw governance

**Justification:** Debt draws affect liquidity, covenants, interest, fees, and lender exposure.

**Improvement:** Add facility lifecycle, borrowing base, availability, draw request, rate basis, fees, approvals, covenant impact, repayment schedule, and GL handoff evidence. Block draws that breach policy or mandate authority.

### 28. Interest and fee accrual forecasting

**Justification:** Treasury must forecast interest income, debt interest, commitment fees, bank charges, and facility fees.

**Improvement:** Add accrual forecasts by instrument, facility, bank account, fee type, rate index, day-count convention, and value date. Reconcile expected fees to statement lines and raise anomalies.

### 29. Bank fee anomaly management

**Justification:** Bank fees often leak value through incorrect pricing, duplicate charges, or unapproved services.

**Improvement:** Compare statement fees to bank fee schedules, expected volumes, account terms, and historical patterns. Open recovery cases with bank contact, disputed amount, expected credit, and resolution state.

### 30. FX exposure capture by cash flow

**Justification:** FX risk comes from forecast flows, AR, AP, debt, investments, and bank balances, not only posted accounting entries.

**Improvement:** Add FX exposure records by source, currency pair, value date, amount, confidence, natural offset, hedge status, and accounting designation. Keep source records as projections/contracts.

### 31. Hedge recommendation and designation evidence

**Justification:** Hedges need purpose, exposure linkage, instrument, ratio, effectiveness, approval, and accounting evidence.

**Improvement:** Add hedge recommendations with exposure bundle, instrument type, hedge ratio, counterparty, tenor, cost, effectiveness expectation, designation intent, and approval workflow.

### 32. Hedge effectiveness monitoring

**Justification:** Hedge programs require ongoing testing and evidence that strategy remains aligned with exposure.

**Improvement:** Track effectiveness metrics, exposure changes, market rates, hedge fair value, ineffectiveness amount, and rebalancing recommendations. Store model governance and accounting handoff evidence.

### 33. Covenant proof generation

**Justification:** Lenders and boards require evidence that liquidity, leverage, coverage, and restricted cash covenants are met.

**Improvement:** Generate covenant proofs from cash positions, debt facilities, investments, forecasts, and restricted cash. Include formula version, source evidence, threshold, result, reviewer, and disclosure-minimized proof bundle.

### 34. Working-capital finance program management

**Justification:** Supplier finance, receivables finance, and inventory finance affect liquidity, counterparty risk, and accounting treatment.

**Improvement:** Add program records with eligibility, counterparty, advance amount, fee, recourse, maturity, participant limits, accounting handoff, and forecast impact. Simulate liquidity benefit versus risk.

### 35. Cross-border liquidity controls

**Justification:** Cross-border cash movement faces tax, FX, trapped-cash, sanctions, local banking, and documentation constraints.

**Improvement:** Add cross-border liquidity requirements by country, currency, entity, purpose, document, tax implication, settlement rail, and approval. Block movements missing required evidence.

### 36. Counterparty risk signal governance

**Justification:** Counterparty ratings, CDS spreads, bank news, country risk, and internal limits affect investment, deposit, and payment decisions.

**Improvement:** Add risk signal records with source, score, freshness, affected counterparties, policy impact, and override workflow. Surface limit breaches and concentration warnings.

### 37. Sanctions and account freeze screening

**Justification:** Treasury movements may be blocked by sanctions, frozen accounts, or restricted counterparties.

**Improvement:** Add screening evidence for bank counterparties, payment beneficiaries, countries, and account restrictions using declared identity/compliance projections. Record clear/block decisions and escalation.

### 38. Treasury close and proof cockpit

**Justification:** Treasury close requires bank reconciliation, cash positions, FX, debt, investments, fees, and covenant evidence.

**Improvement:** Add a close cockpit with statement completeness, unreconciled lines, cash position finalization, FX exposure review, investment/debt rollforwards, fee anomalies, covenant proofs, and GL handoff status.

### 39. Cash movement audit trail

**Justification:** Every treasury cash movement needs traceability from source request through approval, route, bank acknowledgement, settlement, reconciliation, and GL handoff.

**Improvement:** Build cash movement trace views linking funding requests, sweeps, investments, debt draws, netting, bank statements, events, controls, and audit proofs.

### 40. Treasury rules and parameter simulation

**Justification:** Liquidity buffers, risk thresholds, approval limits, hedge triggers, investment limits, and forecast confidence floors materially change decisions.

**Improvement:** Simulate rule/parameter changes against historical and open treasury data, showing changed funding decisions, buffer breaches, investment eligibility, hedges, exceptions, and approval workload.

### 41. Resilience drills for bank and rail outages

**Justification:** Treasury must know how it will fund obligations when a bank, rail, API, or region is unavailable.

**Improvement:** Add drills for bank outage, delayed statements, payment rail failure, stale FX rates, missing forecasts, and dead-letter replay. Store degraded-mode decisions and recovery evidence.

### 42. Crypto-agile treasury authorization

**Justification:** High-value treasury instructions need signing policies that can rotate without breaking evidence.

**Improvement:** Add authorization signature epochs for payment funding, sweeps, investments, debt draws, and bank transmissions. Store signer, algorithm, key epoch, and verification evidence.

### 43. Carbon-aware treasury workload scheduling

**Justification:** Some treasury workloads, such as forecast refreshes and analytics, can be scheduled flexibly; funding and cutoff-sensitive work cannot.

**Improvement:** Classify workloads by urgency and schedule only deferrable jobs into carbon-aware windows. Record why a job was deferred or executed immediately.

### 44. Treasury model governance

**Justification:** Forecasting, reconciliation, risk, hedge, and liquidity optimization models influence financial decisions.

**Improvement:** Add model governance with feature lineage, training data class, drift, fallback, explainability, approval status, and materiality thresholds. Require human review for high-impact recommendations.

### 45. Agent-safe liquidity planning

**Justification:** A treasury chatbot can help optimize cash, but it must not move money or alter funding policy without approval.

**Improvement:** Define agent previews for liquidity plans with cash positions, reserves, forecast assumptions, proposed sweeps/funding, counterparty risk, covenant impact, and approval requirements. Agent mutations should remain draft until confirmed.

### 46. Agent-safe bank reconciliation

**Justification:** The agent can accelerate reconciliation but wrong matches distort cash and downstream ledgers.

**Improvement:** Require match previews with candidate sources, confidence, amount/date differences, narrative evidence, and reversal path. The agent should only auto-accept matches above policy thresholds and route others to review.

### 47. Agent-safe capital action recommendations

**Justification:** Investments, debt draws, hedges, and working-capital finance are financially material actions.

**Improvement:** Publish agent competencies for drafting investment, debt, hedge, and finance recommendations with risk, liquidity, covenant, accounting, and approval evidence. Execution must require authorized human approval.

### 48. UI surface for all treasury capabilities

**Justification:** Treasury specialists need operational command surfaces, not hidden backend commands.

**Improvement:** Expand the workbench into bank account governance, signatory mandates, statements, reconciliation, cash position, forecast, liquidity optimization, sweeps, netting, in-house bank, funding, investments, debt, FX/hedges, covenants, fees, risk, close, and agent panels.

### 49. Boundary proof for treasury-only ownership

**Justification:** Treasury integrates with AP, AR, payroll, tax, GL, identity, audit, schema, and gateway but must not read their tables directly.

**Improvement:** Add static/runtime checks proving every treasury command uses only treasury-owned tables plus declared APIs/events/projections. Include failing fixtures for direct foreign-table references.

### 50. Treasury readiness score

**Justification:** Users need a concise view of whether treasury is complete enough for production cash control.

**Improvement:** Compute readiness from bank account governance, statement completeness, reconciliation aging, cash-position freshness, forecast accuracy, liquidity buffers, funding controls, investments/debt/FX coverage, covenant proofs, counterparty risk, UI coverage, boundary proof, and agent safety.
