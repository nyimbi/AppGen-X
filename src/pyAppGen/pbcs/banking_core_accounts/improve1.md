# Banking Core Accounts Improvement Backlog

## Current Domain Evidence Used

- Exact PBC key in the manifest: `banking_core_accounts`.
- Manifest description: deposit accounts, balances, holds, interest, fees, statements, customer account servicing, and account controls.
- Owned tables: `deposit_account`, `account_balance`, `account_hold`, `interest_accrual`, `fee_assessment`, `statement_cycle`, `account_service_case`, `banking_core_accounts_policy_rule`, `banking_core_accounts_runtime_parameter`, `banking_core_accounts_schema_extension`, `banking_core_accounts_control_assertion`, `banking_core_accounts_governed_model`.
- Published APIs today: `POST /deposit-accounts`, `POST /account-balances`, `POST /account-holds`, `POST /interest-accruals`, `POST /fee-assessments`, `GET /banking-core-accounts-workbench`.
- Emitted events today: `BankingCoreAccountsCreated`, `BankingCoreAccountsUpdated`, `BankingCoreAccountsApproved`, `BankingCoreAccountsExceptionOpened`.
- Consumed events today: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- UI fragments already declared: `BankingCoreAccountsWorkbench`, `BankingCoreAccountsDetail`, `BankingCoreAccountsAssistantPanel`.
- Docs already declared: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Canonical deposit account lifecycle
**Justification:** Deposit accounts need a regulator-defensible lifecycle, not an open-ended status field. Opening, activation, suspension, dormancy, closure, and reopening each carry different controls for balances, fees, statements, and customer servicing.
**Improvement:** Define a state machine on `deposit_account` with effective-dated transitions for pending, approved, active, restricted, dormant, closed, and reopened. Require maker-checker approval where policy demands it, and surface current state plus next allowed actions in `BankingCoreAccountsDetail`.
**Acceptance evidence:** Transition rules are documented in `SPECIFICATION.md`, invalid transitions are rejected by tests, and `RELEASE_EVIDENCE.md` shows lifecycle screenshots plus event traces for create, approve, suspend, close, and reopen flows.

### 2. Customer-to-account servicing projection
**Justification:** Account operators need a fast view of all deposit accounts, holds, restrictions, service cases, and statement status for a customer relationship without copying customer master data into this PBC. Today the manifest exposes workbench surfaces but no explicit customer/account projection.
**Improvement:** Build a read model that projects customer identifiers, linked `deposit_account` records, current `account_balance` positions, active `account_hold` records, latest `statement_cycle` status, and open `account_service_case` items. Keep it projection-only so ownership of customer golden data remains outside `banking_core_accounts`.
**Acceptance evidence:** The workbench can open a customer/account summary from `GET /banking-core-accounts-workbench`, projection freshness is measured, and release evidence includes examples for single-account, joint-account, and restricted-account customers.

### 3. Product parameter inheritance for deposit accounts
**Justification:** Savings, current, youth, salary, and escrow accounts do not share the same interest, fee, hold, and overdraft rules. Without product inheritance, runtime parameters drift into record-by-record exceptions that are hard to audit.
**Improvement:** Layer `banking_core_accounts_runtime_parameter` so account product defaults flow into `deposit_account`, with controlled local overrides for branch, tenant, or regulatory reason. Show the inherited value, the override source, and the approval reason in the detail view.
**Acceptance evidence:** Tests prove product defaults apply consistently, override reasons are stored and queryable, and release evidence shows a product comparison with different fee, interest, and overdraft settings.

### 4. Ledger, available, and withdrawable balance decomposition
**Justification:** A single balance number is not enough for deposit operations. Core banking users need ledger balance, available balance, withdrawable balance, uncleared funds, and held funds separated to explain customer-facing and operational outcomes.
**Improvement:** Expand `account_balance` into a projection model that keeps ledger, available, withdrawable, held, uncleared, and accrued-interest components with value date and posting date. Make the workbench explain why available funds differ from the ledger figure.
**Acceptance evidence:** Balance calculation tests cover cash deposit, cheque hold, fee posting, interest accrual, and overdraft draw scenarios, and the detail page exposes a component-by-component balance explanation.

### 5. Value-dated balance replay
**Justification:** Deposit disputes often hinge on what the balance looked like on a prior value date, not only on the current day. Reconstructing those positions from mutable rows is slow and fragile.
**Improvement:** Use the event-sourced operational history capability to replay `account_balance` as-of any posting date or value date. Surface as-of balance replay from the workbench for dispute handling and reconciliation.
**Acceptance evidence:** Replay tests match stored projections for historical dates, event ordering is deterministic, and release evidence shows a statement dispute resolved from balance replay rather than manual reconstruction.

### 6. Hold taxonomy and priority model
**Justification:** Not all holds are equivalent. Legal, fraud, cheque, card authorization, compliance, deceased-customer, and internal-review holds each need different release rules and different customer communication.
**Improvement:** Add typed `account_hold` categories with priority, effect on available funds, expiry logic, renewal rules, and release authority. Show each hold with reason code, amount, expiry, owning queue, and whether it blocks debit, credit, closure, or statement generation.
**Acceptance evidence:** Tests cover overlapping hold categories, hold priority ordering, partial releases, and the workbench displays the impact of each active hold on withdrawable funds.

### 7. Hold release waterfall
**Justification:** When funds are released or reversed, the order in which holds fall away affects available balance and possible overdraft usage. Ad hoc release logic creates customer harm and reconciliation noise.
**Improvement:** Implement a configurable waterfall for releasing `account_hold` records by business priority, age, and legal precedence. Record why a hold was released automatically, manually, or because a source event expired.
**Acceptance evidence:** Simulation tests prove available balance changes correctly across competing holds, audit history captures release rationale, and release evidence shows manual and timed expiry releases.

### 8. Overdraft facility and grace-period controls
**Justification:** Overdraft behavior is central to transaction accounts and must align with product, risk, and customer servicing rules. It is not enough to post a negative balance and infer meaning later.
**Improvement:** Add overdraft limit, grace days, excess handling, and overdraft block rules to `deposit_account` and `account_balance` projections. Distinguish arranged overdraft, unarranged overdraft, and unauthorized excess with separate customer and operator treatments.
**Acceptance evidence:** Tests cover entering overdraft, curing within grace, exceeding limit, and blocking new debits, and the workbench shows current overdraft status with next fee or cure milestone.

### 9. Overdraft fee and interest reversal flows
**Justification:** Customers frequently challenge overdraft charges after same-day credits, technical outages, or bank-side errors. Reversal logic must explain which fee or interest entry is being unwound and why.
**Improvement:** Add reversal linkage from `fee_assessment` and `interest_accrual` back to the originating overdraft condition, including waiver reason, approving role, and customer-impact notes. Show the net financial impact before the reversal is committed.
**Acceptance evidence:** Reversal scenarios are covered by tests, waived and reversed items are visibly linked in the detail view, and release evidence includes a recovered overdraft case with before-and-after balances.

### 10. Interest rate tiering and accrual calendars
**Justification:** Deposit interest depends on product tiers, minimum balances, step rates, day-count conventions, and posting calendars. A generic accrual record is too shallow for real savings and term-based products.
**Improvement:** Enrich `interest_accrual` with tier tables, balance bands, day-count basis, holiday handling, and posting cadence. Distinguish accrual amount from capitalization amount so month-end, quarter-end, and maturity rules stay explicit.
**Acceptance evidence:** Tests cover daily accrual, step-tier transitions, month-end posting, and leap-year handling, and the workbench can explain the rate tier used for a given accrual period.

### 11. Interest capitalization versus payout handling
**Justification:** Some deposit products capitalize interest into principal, others pay it to a settlement account, and others suspend payout under restriction. Those paths affect statements, withholding, and reconciliation differently.
**Improvement:** Extend `interest_accrual` and `deposit_account` rules to support capitalization, payout-to-linked-account, tax withholding placeholder fields, and restricted-account suspense handling. Make the posting outcome visible before approval.
**Acceptance evidence:** Tests cover capitalization, external payout, restricted payout suspension, and statement presentation, and release evidence includes the journal-style breakdown used to support customer enquiries.

### 12. Fee schedule engine for deposit servicing
**Justification:** Maintenance fees, excess withdrawal fees, dormancy fees, stop-payment fees, paper statement fees, and account closure fees follow different triggers. Treating all charges as generic `fee_assessment` rows loses the trigger semantics needed for control and dispute handling.
**Improvement:** Introduce typed fee schedules with trigger condition, waiver policy, customer notice requirement, tax flag, and reversal rules. Link each `fee_assessment` to the rule version that produced it.
**Acceptance evidence:** Tests prove different fee triggers fire only under the right conditions, operators can trace a posted fee to its rule version, and release evidence shows maintenance, dormancy, and stop-payment fee examples.

### 13. Fee waiver governance
**Justification:** Fee waivers are common in branch and contact-center servicing, but uncontrolled waivers distort revenue and create fairness issues. Waiver evidence must be visible to supervisors and auditors.
**Improvement:** Add waiver reason codes, approval tiers, customer-impact notes, and repeat-waiver analytics to `fee_assessment`. Expose a waiver workbench queue for review of high-value or repeated discretionary waivers.
**Acceptance evidence:** Tests cover waiver approval thresholds and denial paths, the workbench shows repeat-waiver patterns by account and operator, and `RELEASE_EVIDENCE.md` includes a supervisor approval trail.

### 14. Statement cycle calendar and cutover controls
**Justification:** Statement generation is a domain event with strict cutoffs, not a background convenience feature. Cutover mistakes create wrong opening balances, duplicate charges, and customer complaints.
**Improvement:** Enhance `statement_cycle` to track cycle definition, cutoff timestamp, posting freeze window, rerun reason, and exception status. Make statement cutover visible on the workbench with warnings for pending holds, late fees, or unresolved balance anomalies.
**Acceptance evidence:** Tests cover standard cycle, rerun cycle, and cutoff-after-late-posting scenarios, and release evidence includes a statement cycle dashboard with pre-close and post-close evidence.

### 15. Statement line composition and balance-forward proof
**Justification:** A statement must explain how the opening balance became the closing balance through deposits, withdrawals, fees, interest, holds, and reversals. If the balance-forward proof is weak, both customer service and audit suffer.
**Improvement:** Build statement composition logic that groups entries by posting rules, preserves reversals, and proves opening balance plus net activity equals closing balance. Surface line-level provenance from `account_balance`, `interest_accrual`, `fee_assessment`, and `account_hold`.
**Acceptance evidence:** Statement proof tests pass across normal and corrected cycles, detail screens show provenance for each line item, and release evidence includes a redacted statement with balance-forward reconciliation.

### 16. Signatory and mandate registry
**Justification:** Many deposit accounts are joint, trustee, guardian, or business accounts with specific signing rules. Without explicit mandate modeling, servicing actions can be approved by the wrong party.
**Improvement:** Extend `deposit_account` and `account_service_case` to capture mandate type, signatory set, signing rule, effective dates, and evidence references. Project mandate status into account detail so staff can tell whether one signer, two signers, or all signers are required.
**Acceptance evidence:** Tests cover single-sign, joint-sign, guardian, and expired-mandate scenarios, and release evidence shows a mandate-driven service request approval path.

### 17. Effective-dated mandate changes
**Justification:** Signatory changes often overlap with address changes, account restrictions, and pending instructions. Core banking needs forward-dated mandate changes so service teams can schedule updates without losing current authority rules.
**Improvement:** Add pending, active, superseded, and revoked mandate versions with effective dates and approval status. Block sensitive servicing actions when a mandate change is incomplete or conflicting.
**Acceptance evidence:** Tests cover future-dated mandate activation and revocation overlap, the workbench warns about in-flight mandate changes, and release evidence includes a before/after signatory timeline.

### 18. Compliance restriction boundary model
**Justification:** AML review, sanctions concern, fraud investigation, and court order restrictions have different operational boundaries. Operators need to know exactly whether debit, credit, closure, statement delivery, or profile maintenance is blocked.
**Improvement:** Represent compliance boundaries on `deposit_account` and `account_hold` as structured capabilities blocked or allowed. Expose the restriction source, review owner, expiry, and escalation route without leaking external compliance-system internals into this PBC.
**Acceptance evidence:** Tests verify debit-only, full-freeze, and closure-block scenarios, and release evidence shows a restricted account view with action-level controls correctly disabled.

### 19. Compliance review servicing cases
**Justification:** Restriction decisions are never just balance events; they create open work that must be tracked until resolution. Without typed service cases, restrictions linger without ownership and customer communication degrades.
**Improvement:** Add `account_service_case` templates for sanctions review, source-of-funds request, suspicious-activity follow-up, deceased-customer hold, and documentation deficiency. Make case status, SLA, and required evidence visible beside the impacted account.
**Acceptance evidence:** Tests cover case opening from restriction events and case closure after evidence review, and the workbench can filter cases by compliance type, queue, and ageing bucket.

### 20. Dormancy, inactivity, and reactivation controls
**Justification:** Dormancy changes what transactions are allowed, what fees apply, and what customer identification is required before reactivation. It should be a first-class lifecycle branch, not an afterthought.
**Improvement:** Use `deposit_account`, `statement_cycle`, and `fee_assessment` to track inactivity counters, dormancy threshold, dormancy notices, reactivation evidence, and escheat readiness. Distinguish dormant status from compliance restriction and from ordinary low activity.
**Acceptance evidence:** Tests cover inactivity ageing, dormancy conversion, reactivation, and fee treatment, and release evidence includes a dormant account reactivation path with required checks.

### 21. Account closure with residual balance handling
**Justification:** Closing a deposit account requires more than flipping a status. Residual balances, accrued interest, pending fees, holds, and statement obligations must be cleared or transferred in a controlled order.
**Improvement:** Build a closure checklist that verifies zero or transferred balance, cleared holds, final interest treatment, pending fee disposition, final statement generation, and customer communication completion. Refuse closure when any required step is incomplete.
**Acceptance evidence:** Closure tests cover zero-balance closure, transfer-out closure, and blocked closure due to unresolved hold or statement cycle, and the detail page exposes the closure checklist state.

### 22. Controlled account reopening
**Justification:** Reopening closed accounts is operationally sensitive because prior number, mandate, and fee history may still matter. Reopening must distinguish true reinstatement from opening a fresh account for the same customer.
**Improvement:** Add reopening rules that preserve lineage to the closed `deposit_account`, require reason codes, and re-evaluate mandates, holds, and product parameters before activation. Show whether the reopened account inherits prior restrictions or starts clean.
**Acceptance evidence:** Tests cover allowable and disallowed reopen paths, lineage is queryable in projections, and release evidence includes a reopened account with preserved historical statement access.

### 23. Internal transfer and linked-account relationships
**Justification:** Deposit products often depend on linked settlement, sweep, or charges accounts. Those relationships shape overdraft cure, fee collection, and interest payout behavior.
**Improvement:** Model linked account relationships and transfer permissions as part of `deposit_account` servicing context, while keeping actual transfer execution outside this PBC's ownership. Use the relationship projection to inform fee debit fallback and interest payout routing.
**Acceptance evidence:** Tests cover permitted and blocked linked-account usage, projections show active relationships, and release evidence includes interest payout routed to a linked settlement account.

### 24. Subledger-to-balance reconciliation
**Justification:** Core banking operations need daily proof that account-level projections agree with the authoritative posting stream that fed them. Without structured reconciliation, balance defects surface only after customer impact.
**Improvement:** Introduce reconciliation runs that compare `account_balance` projections, statement totals, fee postings, and interest postings against imported posting evidence. Open `account_service_case` items automatically for unreconciled differences.
**Acceptance evidence:** Reconciliation tests classify matched, timing, and broken cases, the workbench exposes break counts and materiality, and `RELEASE_EVIDENCE.md` includes a sample reconciliation report.

### 25. Intraday versus end-of-day posting boundary
**Justification:** Some balances must react intraday while other controls and customer artifacts are end-of-day. If the boundary is vague, operators cannot explain why a fee is visible but not yet statemented, or why a hold reduced available funds before formal posting.
**Improvement:** Make every `account_balance`, `interest_accrual`, `fee_assessment`, and `statement_cycle` update declare whether it is intraday, end-of-day, or backdated correction. Present the posting boundary in operator and auditor views.
**Acceptance evidence:** Tests cover intraday visibility, overnight roll, and backdated corrections, and release evidence shows the same account across intraday and end-of-day snapshots.

### 26. Typed domain events for lifecycle and servicing
**Justification:** The current emitted events are too coarse to explain the actual business action. Consumers need to differentiate account activation from hold release, statement closure, fee waiver, and overdraft breach without unpacking opaque payloads.
**Improvement:** Add typed events for deposit account opened, activated, restricted, dormant, reactivated, closed, hold applied, hold released, fee waived, interest capitalized, statement closed, and reconciliation break opened. Keep the existing manifest events as compatibility envelopes if needed.
**Acceptance evidence:** Event schemas are versioned, sample payloads are documented, compatibility tests pass, and release evidence shows downstream consumers reacting to typed events without custom parsing.

### 27. Idempotent command keys for external requests
**Justification:** Balance, hold, interest, and fee requests can arrive more than once from channels or batch sources. Deposit operations cannot tolerate duplicate holds or duplicate fee postings because a caller retried.
**Improvement:** Require idempotency keys and source-system references on `POST /account-balances`, `POST /account-holds`, `POST /interest-accruals`, and `POST /fee-assessments`. Expose duplicate detection results to the operator instead of silently dropping or replaying commands.
**Acceptance evidence:** Tests prove duplicate requests do not double-post domain effects, stored idempotency evidence is queryable, and release evidence includes a retry sequence with a single business outcome.

### 28. Dead-letter recovery workbench
**Justification:** Retry and dead-letter evidence is already declared in the manifest, but operators need a domain-aware recovery lane, not just infrastructure counters. Failures should point to the impacted account, balance, or statement cycle immediately.
**Improvement:** Build a workbench view that groups failed commands and events by affected `deposit_account`, `account_balance`, `account_hold`, or `statement_cycle`, with retry eligibility, poison-message hints, and linked service cases. Allow replay only through governed actions.
**Acceptance evidence:** Failed-message scenarios are reproducible in tests, the workbench shows domain grouping and replay decisions, and release evidence includes recovery of a failed hold event without manual datastore edits.

### 29. Query APIs for operational retrieval
**Justification:** The manifest lists command-heavy APIs, but servicing teams also need query surfaces for account detail, hold detail, fee history, statement history, and lifecycle evidence. Workbench screens should not depend on private query hacks.
**Improvement:** Add read APIs for account summary, balance components, active holds, interest history, fee history, statement cycle history, and open service cases. Keep filters aligned to branch, product, state, restriction, and ageing use cases.
**Acceptance evidence:** API contracts are documented, permission tests protect sensitive retrieval, and release evidence shows the workbench using supported query endpoints rather than undeclared data paths.

### 30. Operations workbench by role
**Justification:** Branch staff, central operations, contact-center agents, supervisors, and auditors do not need the same controls. A single generic workbench makes high-volume servicing slower and increases the chance of acting on the wrong evidence.
**Improvement:** Split `BankingCoreAccountsWorkbench` into role-focused views: opening and maintenance queue, restrictions queue, statement operations, fee and interest review, reconciliation breaks, and audit evidence. Keep one underlying domain model while changing only what each role sees and can do.
**Acceptance evidence:** Permission-aware UI tests pass, each role sees only its relevant actions, and release evidence includes screenshots for branch operator, supervisor, and auditor personas.

### 31. Account detail timeline
**Justification:** Service teams need a time-ordered story of what happened to an account across lifecycle, balances, holds, fees, interest, statements, and service cases. Jumping across separate tabs slows resolution and obscures causal chains.
**Improvement:** Build a unified timeline in `BankingCoreAccountsDetail` that merges typed events, balance changes, hold changes, statement milestones, fee activity, interest activity, and case actions. Allow filtering by event family and date range.
**Acceptance evidence:** Timeline ordering tests pass across mixed event types, the detail page can filter to disputes or compliance history, and release evidence shows a customer complaint resolved from one consolidated timeline.

### 32. Assistant skill for governed servicing instructions
**Justification:** The manifest declares AI agent task assistance and document instruction intake, but account servicing needs domain-bounded skills. An assistant should prepare a safe deposit-account action plan, not improvise unrestricted data changes.
**Improvement:** Add an assistant skill in `BankingCoreAccountsAssistantPanel` that can interpret a servicing request, identify the affected account, summarize mandates and restrictions, draft the next governed command, and ask for approval when policy requires it. The assistant must reference only supported APIs, events, and projections inside `banking_core_accounts`.
**Acceptance evidence:** Skill tests cover address-change support, hold enquiry, fee waiver request, and closure request scenarios, and release evidence shows previewed actions with explicit approvals and audit traces.

### 33. Assistant skill for statement and fee explanations
**Justification:** A large share of contact-center traffic comes from customers asking why a balance moved, why a fee posted, or why a statement looks different. Those explanations require a domain-aware synthesis across balances, fees, interest, and holds.
**Improvement:** Add a read-only assistant skill that explains statement lines, fee triggers, interest computation, and hold impact using `account_balance`, `fee_assessment`, `interest_accrual`, and `statement_cycle` evidence. Return explanation cards that can be copied into a service case note.
**Acceptance evidence:** Prompt-and-response evaluations cover common customer questions, cited source spans link back to domain records, and release evidence shows an operator using the assistant without creating unauthorized changes.

### 34. Exception taxonomy and ageing
**Justification:** Not every exception is the same. Missing mandate evidence, failed reconciliation, stuck statement close, invalid balance component, and unresolved compliance block each need different queues, SLAs, and escalation paths.
**Improvement:** Add a typed exception model within `account_service_case` and supporting projections, with severity, materiality, ageing bucket, owner, blocked capability, and resolution evidence. Link every emitted exception to the domain object it prevents from progressing.
**Acceptance evidence:** Tests cover creation and ageing of multiple exception classes, the workbench can filter by blocked capability and severity, and release evidence includes an ageing dashboard tied to real case states.

### 35. Policy rule versioning with effective dating
**Justification:** Changes to hold rules, fee triggers, dormancy thresholds, or overdraft settings must be explainable after the fact. Current and prior account outcomes need to remain traceable to the rule version that governed them.
**Improvement:** Extend `banking_core_accounts_policy_rule` with effective-from, effective-to, superseded-by, approval evidence, and targeted account-product scope. Make rules queryable from impacted account, fee, hold, and statement records.
**Acceptance evidence:** Tests prove future-dated and superseded policies evaluate correctly, the workbench can trace a domain outcome to a rule version, and release evidence includes a policy change timeline plus impacted-account sample.

### 36. Runtime parameter scoping and drift detection
**Justification:** Parameters are useful only if operators know where they apply and whether they drifted away from approved values. Product teams need to see if a branch or tenant quietly diverged from the intended operating model.
**Improvement:** Add scope metadata to `banking_core_accounts_runtime_parameter` for tenant, product, branch, segment, and emergency override, plus drift detection against approved baselines. Show active scope resolution in the workbench before a parameter affects live accounts.
**Acceptance evidence:** Tests cover scope precedence and emergency override expiry, drift alerts appear in the workbench, and release evidence includes a resolved parameter conflict across product and branch layers.

### 37. Continuous control assertions for maker-checker and segregation of duties
**Justification:** Deposit account opening, overdraft changes, fee waivers, and mandate changes often require separation of duties. Control failures should be detected as the work happens, not only after an audit sample.
**Improvement:** Use `banking_core_accounts_control_assertion` to continuously test maker-checker presence, role separation, approval materiality thresholds, and restricted-action overrides. Raise visible exceptions when controls fail or are bypassed.
**Acceptance evidence:** Tests trigger control failures for self-approval and missing second checker, the workbench surfaces failed control assertions, and `RELEASE_EVIDENCE.md` includes control-pass and control-fail examples.

### 38. Release evidence pack for core banking operations
**Justification:** This PBC already declares `RELEASE_EVIDENCE.md`, but release proof should cover domain correctness, not only deployment success. Account lifecycle, balance integrity, statement accuracy, and control evidence all need to be demonstrable.
**Improvement:** Define a release pack that includes lifecycle walkthroughs, balance component proofs, hold behavior, overdraft edge cases, interest and fee samples, statement cutover evidence, reconciliation summaries, and control assertion results. Keep the evidence organized by domain scenario rather than by internal component.
**Acceptance evidence:** `RELEASE_EVIDENCE.md` contains repeatable scenario evidence across the main deposit-account flows, release reviewers can trace each scenario to tests and screenshots, and the pack is complete before a release is marked ready.

### 39. Tenant isolation and jurisdiction boundary checks
**Justification:** The manifest includes multi-tenant policy isolation, and deposit-account controls can vary by tenant and jurisdiction. Leakage across tenant or jurisdiction boundaries is a severe operational and regulatory risk.
**Improvement:** Enforce tenant-scoped records, parameter resolution, workbench filters, and emitted event context across `deposit_account`, `account_balance`, `fee_assessment`, and `account_service_case`. Prevent an operator from applying the wrong jurisdictional rule set to an account.
**Acceptance evidence:** Tests prove tenant and jurisdiction isolation, UI filters never cross tenant context, and release evidence includes negative tests for cross-tenant and cross-jurisdiction access attempts.

### 40. Schema extension registry for product-specific account fields
**Justification:** Deposit products evolve and often need controlled extra attributes such as notice period, passbook flag, payroll anchor, or trustee reference. Those additions should not become uncontrolled JSON clutter that breaks servicing and evidence.
**Improvement:** Use `banking_core_accounts_schema_extension` to register product-specific fields with owner, validation rule, display rule, and migration plan. Surface approved extensions in detail and workbench views without weakening core field discipline.
**Acceptance evidence:** Tests cover extension validation and rendering, incompatible extensions are rejected before release, and release evidence includes one approved extension flowing through API, UI, and event payloads.

### 41. Product and branch analytics for deposit behavior
**Justification:** The manifest exposes analytics, but account teams need domain measures that matter operationally. Hold spikes, overdraft penetration, dormancy growth, fee waiver concentration, and statement reruns all indicate real servicing issues.
**Improvement:** Create analytics projections for product, branch, and tenant that summarize active accounts, balance composition, hold ratios, overdraft usage, fee waivers, interest cost, dormant accounts, and reconciliation breaks. Make each metric drill into the affected accounts.
**Acceptance evidence:** Metric definitions are documented, projections update from domain events, and release evidence shows product and branch drill-downs tied to actual account records.

### 42. Cryptographic sealing of account evidence
**Justification:** AuditEventSealed is already consumed, so the PBC should make high-value account evidence tamper-evident. Statements, approvals, mandate changes, and reconciliation reports benefit from integrity proofing.
**Improvement:** Hash and seal approved statement artifacts, mandate evidence, major fee waivers, overdraft-limit changes, and reconciliation reports. Record seal references on the relevant domain objects for later verification.
**Acceptance evidence:** Verification tests prove sealed evidence can be re-validated, the detail page displays seal status for high-value artifacts, and release evidence includes a successful seal verification run.

### 43. Counterfactual simulation for fee, rate, and policy changes
**Justification:** Banking operations need to understand customer and revenue impact before changing fee schedules, overdraft policy, or interest rules. Simulation is especially valuable when multiple products and branches are affected.
**Improvement:** Add non-mutating simulations that project how a proposed `banking_core_accounts_policy_rule` or runtime parameter change would affect fees, interest expense, overdraft incidents, dormant-account revenue, and exception queues. Expose simulation outputs through the workbench before approval.
**Acceptance evidence:** Simulations can be run against historical snapshots, results are reproducible, and release evidence includes a sample policy change showing forecast impact and approval notes.

### 44. Anomaly detection for balance and fee behavior
**Justification:** The manifest includes autonomous anomaly detection, but the highest-value anomalies are domain-specific. Unexpected fee bursts, repeated hold-reapply cycles, same-day overdraft cures, and statement reruns should raise targeted concern.
**Improvement:** Train anomaly features on `account_balance`, `fee_assessment`, `account_hold`, and `statement_cycle` patterns relevant to deposit operations. Route flagged anomalies into the appropriate service or control queue with an explanation of the unusual pattern.
**Acceptance evidence:** Detection tests cover known anomalous scenarios, anomaly cards cite the responsible domain signals, and release evidence shows operator review of flagged balance and fee anomalies.

### 45. Account number, alias, and external reference integrity
**Justification:** Deposit operations rely on stable account identifiers, but customers and channels may also use aliases, masked numbers, and external references. Identifier confusion causes posting errors and servicing mistakes.
**Improvement:** Standardize identifier handling on `deposit_account` with canonical account number, masked display number, product alias, and channel reference mappings. Ensure APIs and workbench views display the right identifier for the right audience.
**Acceptance evidence:** Tests cover duplicate prevention, masked display rules, and external reference lookups, and release evidence includes branch, customer-service, and audit views using different safe identifier formats.

### 46. Negative-balance cure and collections handoff boundary
**Justification:** When unarranged overdrafts are not cured, the account eventually crosses from ordinary servicing into recovery or collections workflows. That boundary must be explicit so this PBC stops at the right point and emits the right evidence.
**Improvement:** Add cure milestones, customer notification stages, and handoff-ready evidence to `account_service_case` for prolonged negative balances. Emit a specific handoff event when the case leaves ordinary deposit-account servicing.
**Acceptance evidence:** Tests cover cure, non-cure, and handoff thresholds, the workbench shows countdown to handoff, and release evidence includes a negative-balance case that cleanly transitions out of this PBC's operating scope.

### 47. Operational calendar and holiday-aware servicing
**Justification:** Interest posting, statement closure, and fee assessment depend on business days, weekends, and local holidays. Without explicit calendars, operators cannot explain why one account posted today and another waits until the next business day.
**Improvement:** Add calendar awareness to `interest_accrual`, `fee_assessment`, and `statement_cycle`, including business-day adjustment rules and holiday overrides. Show the next scheduled action date and the rule that produced it.
**Acceptance evidence:** Tests cover weekend, holiday, and month-end adjustment scenarios, the workbench shows scheduled dates with adjustment reasons, and release evidence includes a holiday-shifted posting example.

### 48. Correction and restatement workflow
**Justification:** Core banking operations occasionally need to restate balances, fees, or statements after a discovered defect or late posting. Corrections must preserve the original event trail rather than pretending the first version never existed.
**Improvement:** Add controlled correction flows for `account_balance`, `fee_assessment`, `interest_accrual`, and `statement_cycle`, with original-versus-corrected linkage, reason code, approval evidence, and customer-impact notes. Distinguish operational correction from fraud or compliance intervention.
**Acceptance evidence:** Tests cover corrected statement lines and corrected fee entries, timelines preserve both original and corrected versions, and release evidence includes a restated statement with linked correction evidence.

### 49. End-to-end event and API boundary map
**Justification:** This PBC already declares APIs and emitted and consumed events, but boundary ownership needs to be explicit for future extensions. Account servicing breaks when teams cannot tell whether a change belongs in an API, an event, a projection, or another PBC.
**Improvement:** Document the command, query, and event boundary for opening accounts, updating balances, applying holds, posting interest, assessing fees, closing statements, and opening service cases. Make the map visible in `SPECIFICATION.md` and use it to reject undeclared coupling.
**Acceptance evidence:** Boundary documentation references every current API and event, contract tests assert the documented interfaces, and release evidence includes a trace from one API command through emitted events to refreshed projections.

### 50. Structural release gate for this backlog's domain scope
**Justification:** A backlog is useful only if it drives verifiable implementation and release discipline. The final gate should prove that `banking_core_accounts` handles the promised deposit-account domain with testable evidence across API, UI, event, and control surfaces.
**Improvement:** Convert this backlog into a release-readiness checklist that groups work under lifecycle, balances, holds, overdraft, interest, fees, statements, mandates, compliance boundaries, reconciliation, assistant skills, workbench UX, and evidence sealing. Require each group to point to tests, projections, UI flows, and `RELEASE_EVIDENCE.md` artifacts before calling the PBC production-ready.
**Acceptance evidence:** The checklist exists beside the release evidence, every group has linked proof, unresolved gaps are visible, and a reviewer can verify end-to-end readiness for `banking_core_accounts` without searching outside the package.
