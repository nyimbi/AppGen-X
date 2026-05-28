# General Ledger Core PBC Improvement Backlog

## Purpose

This backlog identifies 50 high-impact, high-value improvements for `gl_core`. The items are specific to general ledger operations: immutable posting, accounting invariants, chart governance, allocations, accruals, revaluation, consolidation, continuous close, regulatory reporting, audit proof, and agent-assisted finance work.

## Current Domain Evidence Used

- Domain purpose: financial-accounting truth, balanced journal activity, immutable ledger events, derived projections, continuous close, posting policy, audit proofs, and AppGen-X subledger synchronization.
- Owned boundary: ledger event log, journal events, journal entries, journal lines, ledger accounts, accounting periods, ledger/account projections, consensus replicas, tenant partitions, probabilistic postings, close snapshots, causal scenarios, reconciliation cases, semantic source documents, regulatory rules, policy decisions, controls, federation links, identity credentials, resilience drills, crypto epochs, carbon execution windows, financial models, inbox/outbox, and dead-letter evidence.
- Existing command/query surface: journal posting/validation, projections, trial balance, close snapshots, reconciliation, policy rules, audit proofs, configuration, schema extension, event inbox, rules, parameters, and workbench views.
- Existing events and dependencies: emits `JournalPosted`, `CloseSnapshotCreated`, `ReconciliationSuggested`, `PostingPolicyChanged`, and `LedgerProjectionBuilt`; consumes invoice, payment, payroll, asset, and tax events through AppGen-X without shared tables.

## 50 Better-Than-World-Class Improvements

### 1. Double-entry invariant proof engine

**Justification:** The core promise of a GL is that every posted entry balances by entity, currency, ledger, and accounting basis. A ledger that merely stores debit and credit lines is incomplete without proof that posting invariants cannot be bypassed.

**Improvement:** Add an invariant engine that proves journal balance, account validity, period admissibility, entity isolation, currency consistency, source-document lineage, and immutable event append before a `JournalPosted` event is emitted. Store invariant proof hashes with each journal event and expose failed invariant reasons in the workbench.

### 2. Chart of accounts governance lifecycle

**Justification:** Chart changes affect postings, statements, consolidations, budgets, tax reporting, allocations, and integrations. Account records need controlled lifecycle, not generic create/update behavior.

**Improvement:** Model account lifecycle states such as proposed, active, posting-blocked, deprecated, mapped-only, and retired. Add hierarchy validation, normal-balance checks, effective dating, statement mapping, consolidation mapping, and impact preview for open journals and downstream reports.

### 3. Multi-ledger and accounting-basis support

**Justification:** Enterprises maintain operational, statutory, management, tax, and adjustment ledgers with different accounting bases and reporting rules.

**Improvement:** Add ledger-set descriptors with ledger type, accounting basis, permitted posting sources, reporting currency, adjustment policy, consolidation participation, and close calendar. Journal validation should ensure lines post to the correct ledger set and basis.

### 4. Bitemporal accounting queries

**Justification:** Finance teams need to answer what was booked, what was valid, what was processed, and what was visible at a historical time.

**Improvement:** Extend projections and queries with transaction time, valid time, processing time, and close-snapshot time. Trial balance, account detail, and statement queries should support as-of reconstruction with source event counts and projection freshness evidence.

### 5. Journal source lineage graph

**Justification:** Auditors and controllers need to trace a journal from subledger event, source document, approval, transformation, posting, reversal, and report impact.

**Improvement:** Build a lineage graph linking consumed AppGen-X events, semantic source documents, journal headers, journal lines, policy decisions, outbox events, audit proofs, and projections. UI drilldowns should show lineage without reading foreign PBC tables.

### 6. Journal lifecycle with draft, approval, posting, and correction

**Justification:** Manual and automated journals require different states, approvals, reversals, attachments, and correction patterns.

**Improvement:** Add explicit journal states for draft, validated, pending approval, rejected, posted, reversed, correcting, and superseded. Corrections must create new immutable events linked to the original, never update sealed postings.

### 7. Reversal and recurring journal engine

**Justification:** Standard GL operations rely on recurring journals, auto-reversals, recurring accruals, and scheduled postings.

**Improvement:** Add recurring journal templates with schedule, end condition, approval policy, auto-reversal date, holiday handling, and idempotency key. Generate future-dated draft entries with previewable amounts and release evidence.

### 8. Accrual and deferral schedule management

**Justification:** Revenue, expenses, prepaids, and liabilities often need systematic recognition across periods.

**Improvement:** Add owned accrual/deferral schedule records with source, basis, start/end dates, recognition method, account mapping, remaining balance, and generated journal linkage. Workbench users should see schedule rollforwards and exceptions.

### 9. Allocation and apportionment engine

**Justification:** Cost centers, departments, projects, and entities require repeatable allocation rules with transparent basis and reversibility.

**Improvement:** Add allocation rules with source pool, target basis, driver data projection, rounding policy, intercompany handling, effective dates, and simulation. Generated journals should include allocation proof and rejected alternatives.

### 10. Intercompany accounting and settlement

**Justification:** Cross-entity transactions require due-to/due-from balancing, eliminations, dispute handling, and settlement workflows.

**Improvement:** Add intercompany pair rules, reciprocal account mappings, counterparty entity validation, imbalance detection, settlement status, elimination eligibility, and dispute cases. Emit reconciliation suggestions and close blockers for unresolved imbalances.

### 11. Multi-currency translation and revaluation

**Justification:** GLs must manage transaction currency, functional currency, reporting currency, FX rates, revaluation, realized/unrealized gains, and translation adjustments.

**Improvement:** Add FX rate set projections, rate source evidence, revaluation runs, translation runs, rounding policy, CTA account mapping, and journal linkage. Trial balances should expose currency layers and revaluation proof.

### 12. Period close control framework

**Justification:** Closing a period is a controlled assurance process, not a date flag.

**Improvement:** Add close tasks, dependencies, approvals, reconciliations, lock rules, late-posting policy, reopen policy, and materiality thresholds. Continuous close snapshots should summarize open blockers and proof status by ledger, entity, and period.

### 13. Soft close and hard close distinction

**Justification:** Finance teams often run preliminary close, management close, statutory close, and final locked close with different permissions and tolerance.

**Improvement:** Model close phases with allowed posting types, adjustment windows, required controls, reporting visibility, and reopen governance. Journal validation should enforce phase-specific constraints.

### 14. Close snapshot reproducibility

**Justification:** A close snapshot must be reproducible from immutable events, not just stored as a balance copy.

**Improvement:** Store snapshot recipe, event sequence range, projection version, control assertions, rule versions, and source counts. Add a verifier that rebuilds the snapshot and compares proof hashes.

### 15. Financial statement mapping engine

**Justification:** Trial balances become statements through mappings, subtotals, eliminations, currency translation, and disclosure rules.

**Improvement:** Add statement line mappings for balance sheet, income statement, cash flow, equity, and custom statutory reports. Include effective dates, account ranges, dimension filters, sign convention, and validation tests.

### 16. Segment and management reporting dimensions

**Justification:** Finance teams report by entity, cost center, product, project, region, channel, and custom dimensions.

**Improvement:** Add dimension schema governance with mandatory/optional dimensions by account, allowed combinations, effective dating, and hierarchy mapping. Journal validation should reject invalid dimension combinations before posting.

### 17. Retained earnings and opening balance rollforward

**Justification:** Year-end close requires profit/loss transfer, balance carryforward, and opening-balance proof.

**Improvement:** Add retained-earnings rules, year-end close jobs, opening balance records, carryforward exceptions, and proof linking prior-year closing balances to new-year opening balances.

### 18. Consolidation and elimination support

**Justification:** Group reporting requires ownership percentages, currency translation, intercompany eliminations, minority interest, and consolidation adjustments.

**Improvement:** Add consolidation scopes, ownership structures, consolidation methods, elimination rules, group currency translation, and adjustment journals. Keep external ledgers as projections/federation links rather than shared tables.

### 19. Budgetary control at posting time

**Justification:** GL postings can violate budget, grant, project, or fund controls if not checked pre-posting.

**Improvement:** Add budget-control projections, encumbrance links, tolerance rules, override approvals, and budget impact simulation. Posting validation should produce an explainable pass/block/override decision.

### 20. Fund and grant accounting primitives

**Justification:** Public sector, nonprofit, and grant-funded organizations require restrictions, funds, grants, allowable costs, and reporting constraints.

**Improvement:** Add fund/grant dimension controls, restriction status, allowable account combinations, sponsor reporting tags, matching requirements, and close controls for restricted balances.

### 21. Source-document semantic account derivation

**Justification:** Automated journal creation must explain how source text, invoice lines, contracts, or events mapped to accounts and dimensions.

**Improvement:** Store semantic derivation candidates, confidence, source spans, rule hits, model version, human override, and final account decision. The agent should show evidence and require confirmation for low-confidence mappings.

### 22. Agent-safe journal creation

**Justification:** GL agents must help create journals from instructions and documents without silently posting material entries.

**Improvement:** Add agent journal plans with proposed header, lines, accounts, dimensions, tax/currency assumptions, balance proof, policy results, risk score, required approvals, and rollback/correction limits. Agent-generated entries should remain drafts until approved.

### 23. Materiality-aware posting validation

**Justification:** Controls and approvals depend on materiality by entity, account, period, currency, and close phase.

**Improvement:** Add materiality profiles and route validation through amount thresholds, volatility, account sensitivity, close status, and actor authority. Store the materiality decision trace with each journal.

### 24. Segregation-of-duties enforcement

**Justification:** Journal preparation, approval, posting, reversal, close approval, and rule modification must be separated for high-risk activities.

**Improvement:** Consume identity policy projections to enforce SoD constraints, emergency overrides, and reviewer independence. Workbench actions should hide or block conflicted approvals and record denial reasons.

### 25. Dynamic approval policy compiler

**Justification:** Approval thresholds vary by account, entity, amount, currency, source, close phase, and risk.

**Improvement:** Compile approval rules into versioned predicates with fixtures, effective dates, and simulation against historical journals. Store compiled evidence and impact analysis before activating rule changes.

### 26. Autonomous reconciliation workbench

**Justification:** Reconciliation cases need evidence, matching candidates, explanations, disputes, and closure proof.

**Improvement:** Expand reconciliation with bank/subledger/intercompany/clearing types, matched items, unmatched aging, confidence, suggested action, human decision, supporting proof, and close blocker status. The agent should recommend matches with explainable evidence.

### 27. Clearing account governance

**Justification:** Suspense and clearing accounts accumulate risk when aged balances are not resolved.

**Improvement:** Add clearing-account aging, expected clearing source, auto-clear rules, exception thresholds, owner assignment, and close blockers. Dashboards should show unresolved balances by account, entity, and age bucket.

### 28. Probabilistic accounting with disclosure controls

**Justification:** Uncertain postings are useful only if finance can report confidence, exposure, and disclosure treatment.

**Improvement:** Extend probabilistic postings with scenario distribution, confidence interval, expected value, materiality impact, statement line propagation, disclosure note, and conversion path to deterministic posting.

### 29. Causal scenario analysis for finance decisions

**Justification:** Controllers and CFOs need counterfactual analysis such as rate changes, reclassification, delayed close, or intercompany settlement impact.

**Improvement:** Add scenario templates that replay ledger projections under changed FX rates, allocation drivers, account mappings, or posting timing. Persist assumptions, affected statement lines, and confidence.

### 30. Ledger projection rebuild governance

**Justification:** Rebuilding projections can change reported balances if event ordering, rules, or schema changed.

**Improvement:** Add rebuild plans with event ranges, projection version, rule version, expected balance deltas, validation checks, and approval for material differences. Store before/after hashes and explanations.

### 31. Real-time trial balance with freshness evidence

**Justification:** Real-time balances are only trustworthy when users know projection lag and included event ranges.

**Improvement:** Add trial balance freshness indicators, last event sequence, projection lag, stale dimension warnings, and confidence for incomplete subledger feeds. UI should show why a balance is preliminary or final.

### 32. Regulatory rule versioning and impact analysis

**Justification:** Changes in accounting standards, local rules, or statutory reporting mappings can materially alter postings and statements.

**Improvement:** Add regulatory rule versions with effective dates, impacted accounts, impacted statement lines, historical simulation, and adoption status. Release evidence should prove rule changes were tested before activation.

### 33. Electronic audit file generation

**Justification:** Many jurisdictions require standardized audit exports with chart, journals, tax, source, and balances.

**Improvement:** Add audit-file descriptors by jurisdiction, required fields, mapping rules, validation checks, disclosure limits, and export proof. Generated files should be reproducible from event sequences and close snapshots.

### 34. Disclosure-minimized audit proof channels

**Justification:** Regulators or external reviewers may need proof of integrity without full journal-line disclosure.

**Improvement:** Add proof bundles for balance existence, journal inclusion, period completeness, and control pass/fail with minimized claims, verifier instructions, and revocation/expiry metadata.

### 35. Immutable event-chain anomaly detection

**Justification:** Ledger integrity can be weakened by sequence gaps, unusual posting bursts, duplicate source hashes, or entropy shifts.

**Improvement:** Add anomaly detection over ledger event cadence, actor/action patterns, account usage, source hashes, and sequence behavior. Each anomaly should create an explainable control assertion or reconciliation case.

### 36. Consensus and geo-resilience drill evidence

**Justification:** Distributed ledger claims require operational proof of quorum behavior, failover, and recovery.

**Improvement:** Add resilience drills for node failure, region partition, stale replica, duplicate commit, and recovery replay. Store quorum state, committed index, data-loss exposure, and release readiness evidence.

### 37. Tenant ledger partition isolation tests

**Justification:** A GL must prevent cross-tenant journal visibility, key reuse, sequence leakage, and reporting contamination.

**Improvement:** Add tenant isolation tests for journal posting, projections, trial balance, close snapshots, audit proofs, agent responses, and dead-letter handling. Release audit should fail on any cross-tenant leakage.

### 38. Privacy-preserving consolidation proof

**Justification:** Group reporting may need consolidation evidence across legal entities without exposing all transaction detail.

**Improvement:** Add private consolidation commitments for entity balances, eliminations, ownership, and group totals. Store proof inputs and limitations so reviewers can verify group numbers with minimized detail.

### 39. Ledger federation contract governance

**Justification:** External ledgers and subledgers must join through explicit contracts rather than shared databases.

**Improvement:** Add federation contracts with source system, trust level, API/event schema, freshness, reconciliation method, and allowed reporting use. Flag stale or untrusted federation links before reporting.

### 40. Carbon-aware non-urgent ledger workloads

**Justification:** Heavy projection rebuilds, audit-file generation, and analytics can often be scheduled outside urgent close windows.

**Improvement:** Add workload urgency classification and carbon windows for deferrable ledger tasks. Record why work ran immediately or was deferred, and ensure close-critical work is never delayed blindly.

### 41. Financial model governance for automation

**Justification:** ML-assisted account derivation, reconciliation, anomaly detection, and risk scoring affect financial statements and controls.

**Improvement:** Add model approval workflows with feature lineage, training data class, drift metrics, explainability, fallback rules, materiality gate, and human override evidence.

### 42. Journal import and bulk correction controls

**Justification:** Large imports and corrections are high-risk because they can bypass normal UI controls.

**Improvement:** Add staged import batches with template validation, duplicate detection, balance proof, sample approval, partial failure handling, and correction-event generation. The agent should explain rejected rows and draft remediation.

### 43. Account combination rule engine

**Justification:** Invalid account/dimension combinations create reporting and control defects.

**Improvement:** Add account-combination rules by account type, entity, cost center, project, product, fund, and period. Compile rules with fixtures and enforce them in journal validation and allocation generation.

### 44. Close cockpit UI coverage

**Justification:** Close, reconciliation, controls, approvals, snapshots, and reporting need an integrated finance workbench.

**Improvement:** Expand UI into close cockpit, journal workspace, account explorer, reconciliation board, allocation console, FX/revaluation panel, consolidation view, audit proof viewer, and agent assistant panel with permission-aware actions.

### 45. Ledger agent competency catalog

**Justification:** In composed apps, the single agent must know GL-specific finance skills and their safety limits.

**Improvement:** Publish competencies for journal drafting, account lookup, trial balance explanation, reconciliation suggestion, close blocker triage, audit proof explanation, regulatory impact analysis, and document-to-journal extraction. Declare permissions, safe reads, mutation previews, and approval requirements.

### 46. Natural-language financial query explanations

**Justification:** Finance users ask why balances changed, why close is blocked, or why an entry failed in natural language.

**Improvement:** Add query explanation plans that translate user questions into safe ledger queries, projection checks, lineage drilldowns, and answer evidence. The agent should cite journal events, controls, and projections rather than inventing explanations.

### 47. Statement-level variance analysis

**Justification:** Controllers need to explain movement between periods, versions, close snapshots, and forecasts.

**Improvement:** Add variance records by statement line, account, dimension, source event class, allocation, FX, and one-time posting. Workbench drilldowns should reconcile variance to journal events.

### 48. Release audit for GL-specific completeness

**Justification:** Generic PBC evidence can pass while missing essential ledger controls.

**Improvement:** Add GL release gates for double-entry proof, chart governance, period close controls, journal lifecycle, reversals, accruals, allocations, FX, intercompany, consolidation, audit proofs, SoD, tenant isolation, and agent safety tests.

### 49. Formal accounting invariant specification

**Justification:** Core financial invariants are precise enough to be specified and tested beyond unit examples.

**Improvement:** Add machine-readable invariant descriptors for balance equality, period lock, account normal balance, retained-earnings rollforward, currency layers, intercompany reciprocity, and event-chain append-only behavior. Generate tests from these descriptors.

### 50. End-to-end financial truth readiness score

**Justification:** Users need one defensible view of whether the GL is ready for real financial truth.

**Improvement:** Compute readiness from journal invariants, projection freshness, account governance, close controls, reconciliation aging, control assertions, audit proof health, model governance, tenant isolation, UI coverage, and agent competency coverage. Show blockers and next best remediation actions.
