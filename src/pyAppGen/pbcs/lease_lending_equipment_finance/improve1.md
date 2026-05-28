# Lease Lending and Equipment Finance Improvement Backlog

## Current Domain Evidence Used

- Manifest key: `lease_lending_equipment_finance`.
- Label: Lease Lending and Equipment Finance.
- Manifest description: equipment leases, assets, schedules, residuals, buyouts, repossession, and finance servicing.
- Declared APIs: `POST /equipment-leases`, `POST /leased-assets`, `POST /payment-schedules`, `POST /residual-values`, `POST /buyout-quotes`, `GET /lease-lending-equipment-finance-workbench`.
- Owned tables: `equipment_lease`, `leased_asset`, `payment_schedule`, `residual_value`, `buyout_quote`, `repo_case`, `lease_servicing_event`, policy rules, runtime parameters, schema extensions, control assertions, and governed models.
- Emitted events: `LeaseLendingEquipmentFinanceCreated`, `LeaseLendingEquipmentFinanceUpdated`, `LeaseLendingEquipmentFinanceApproved`, `LeaseLendingEquipmentFinanceExceptionOpened`.
- Consumed events: `PolicyChanged`, `AuditEventSealed`, `OperationalKpiChanged`.
- Declared UI fragments: `LeaseLendingEquipmentFinanceWorkbench`, `LeaseLendingEquipmentFinanceDetail`, `LeaseLendingEquipmentFinanceAssistantPanel`.
- Declared workflows: create equipment lease and record leased asset.
- Release artifacts already expected by the package: `SPECIFICATION.md` and `RELEASE_EVIDENCE.md`.

### 1. Canonical product structure model

**Justification:** Equipment finance teams book leases, loans, TRAC leases, finance leases, operating leases, fair market value deals, $1 buyout contracts, and rentals with purchase options. If those structures are flattened into one generic record, pricing, accrual, tax treatment, end-of-term processing, and default handling all become unreliable.

**Improvement:** Expand `equipment_lease` into a product structure model with explicit contract family, booking basis, purchase-option type, expected title transfer path, residual-bearing flag, usage billing flag, and servicing playbook selection. Include structure-specific validation for municipal leases, construction progress funding, vendor-originated paper, and refinance or sale-leaseback transactions.

**Acceptance evidence:** Sample deals for each structure book successfully, invalid combinations fail with precise reasons, workbench filters distinguish structure families, and release evidence includes screenshots plus test fixtures proving structure-specific behavior.

### 2. Full deal intake from application to booking

**Justification:** In equipment finance, the operational breakpoints start before booking: application, credit package, vendor quote, approval conditions, and funding instructions shape the final contract. A backlog that starts only at booked leases leaves the riskiest transitions uncontrolled.

**Improvement:** Add an intake pipeline that captures opportunity source, borrower request, equipment quote, dealer invoice, guarantor details, credit approval conditions, and booking prerequisites before creating the final `equipment_lease`. Persist an explicit pre-book status ladder such as application received, underwriting, approved with conditions, docs pending, ready to fund, and booked.

**Acceptance evidence:** A single workbench timeline shows every pre-book milestone, missing conditions prevent booking, assistant summaries cite the intake data they used, and release evidence contains a full application-to-book scenario trace.

### 3. Party and role hierarchy for obligors and support parties

**Justification:** Equipment transactions often involve borrower, co-borrower, guarantor, dealer, broker, supplier, insurer, service provider, and remarketing partner roles. Mis-modeling those parties causes approval, notice, collateral, and collections actions to target the wrong counterparty.

**Improvement:** Add party-role modeling around `equipment_lease` and `leased_asset` with effective dates, notice roles, funding roles, beneficial-owner relationships, cross-default links, and guarantor liability scope. Support borrower groups and master agreements that cover multiple schedules or assets.

**Acceptance evidence:** Test data covers single-obligor, multi-obligor, and guarantor-backed deals, notices route to the correct party roles, and the detail UI renders role cards with effective dates and liabilities.

### 4. Equipment asset identity and collateral traceability

**Justification:** Serial-numbered assets are the spine of equipment finance collateral control. If the platform cannot distinguish chassis, VIN, engine, aircraft tail, trailer, or heavy-equipment fleet identities, collateral perfection and recovery become weak.

**Improvement:** Enrich `leased_asset` with manufacturer, model, serial set, asset class, mobility status, location, installation date, in-service date, title identifier, registration identifier, and replacement or substitution lineage. Support pools, schedules, and parent-child assemblies so a financed machine with attachments remains traceable.

**Acceptance evidence:** Asset-level validation rejects duplicate serials within the tenant, substitution history is visible, collateral schedules export correctly, and evidence includes examples for mobile, titled, and stationary equipment.

### 5. Vendor, invoice, and disbursement controls

**Justification:** Funding risk in equipment finance is often vendor-driven: duplicate invoices, unsupported soft costs, partial deliveries, and invoice manipulation can create immediate loss exposure. The PBC needs stronger funding controls than a simple approved amount field.

**Improvement:** Add supplier and invoice controls that distinguish equipment, freight, installation, training, taxes, and ineligible soft costs; require delivery or acceptance evidence; and support split disbursements, progress payments, and holdbacks. Link every funding line to the asset or schedule it supports.

**Acceptance evidence:** Funding cannot proceed when invoice totals, asset lines, or acceptance prerequisites do not reconcile, disbursement packs show source documents and reviewer sign-off, and release evidence includes a multi-draw construction-equipment example.

### 6. Credit memo and approval-condition tracking

**Justification:** Credit decisions in equipment finance are rarely binary. Approvals often include insurance binders, lien searches, GPS devices, guaranty delivery, field inspection, or extra equity requirements that must be tracked through booking and servicing.

**Improvement:** Add approval-condition records linked to `equipment_lease`, with owner, due date, waiver authority, fulfillment evidence, and breach severity. Separate pricing conditions from documentation conditions and post-close trailing conditions so operations can govern them differently.

**Acceptance evidence:** Deals cannot move to funded or active when blocking conditions remain open, waived conditions record the approving authority, and the workbench shows condition aging with escalation rules.

### 7. Pricing engine for lease and loan structures

**Justification:** Equipment finance pricing is sensitive to structure, advance rate, residual assumptions, collateral mobility, borrower risk, syndication appetite, and funding source. Flat rate entry hides margin leakage and makes exceptions hard to defend.

**Improvement:** Add a pricing engine that models yield, implicit rate, money factor, base curve, spread, fees, dealer reserve, documentation fees, subsidies, and minimum return floors. Support separate pricing paths for amortizing loans, level-pay leases, step-up schedules, and balloon structures.

**Acceptance evidence:** Pricing worksheets reconcile to booked cash flows, exception pricing requires explicit approval, scenario comparisons show margin impact, and release evidence contains worked examples for loan, FMV lease, and balloon structures.

### 8. Tax, accounting, and booking classification controls

**Justification:** The same equipment contract can be handled differently for tax, accounting, and operations depending on jurisdiction and structure. The platform needs explicit classification fields so teams do not infer treatment from notes or naming conventions.

**Improvement:** Capture contract classification, tax owner, property-tax billing method, depreciation beneficiary, maintenance-of-title expectation, and revenue or accrual treatment flags as governed attributes. Add policy rules that prevent incompatible combinations and expose the rationale to reviewers.

**Acceptance evidence:** Classification conflicts are blocked before approval, classification rationale is visible in the detail panel, and release evidence includes decision tables and test scenarios across common structure types.

### 9. Commencement and acceptance governance

**Justification:** A finance contract often should not commence until equipment is delivered, installed, accepted, or ready for beneficial use. Premature commencement creates billing disputes and audit issues.

**Improvement:** Add commencement logic that can anchor to ship date, delivery date, acceptance date, installation completion, or scheduled commencement with waiver approval. Support delayed funding, interim rent, and pre-commencement milestones for staged deliveries.

**Acceptance evidence:** Schedules generate only after the correct commencement trigger, interim rent rules apply when configured, and evidence includes acceptance-document capture with date-driven schedule calculations.

### 10. Payment schedule engine beyond simple level-pay

**Justification:** Equipment finance schedules routinely include stubs, advance rent, arrears billing, seasonal patterns, construction-period interest, balloon payments, and end-of-term purchase options. A simple installment table is not enough.

**Improvement:** Rebuild `payment_schedule` generation to support advance versus arrears timing, odd first periods, daily accrual, step payments, seasonal skips, balloon or bullet maturity, and rent streams tied to acceptance or usage milestones. Allow regenerated schedules only through controlled correction paths.

**Acceptance evidence:** Generated schedules match test vectors for stub periods, seasonal schedules, and balloon maturities, corrections retain lineage to prior versions, and the UI shows schedule version comparisons.

### 11. Day-count, grace, delinquency, and fee logic

**Justification:** Collections accuracy depends on exact timing rules. Different products use different day-count conventions, late-fee rules, grace periods, and delinquency escalation points.

**Improvement:** Introduce policy-driven timing logic for actual/360, 30/360, actual/365, payment grace windows, late-charge caps, default interest, and cure periods. Store which rule set governed each posted schedule and delinquency event.

**Acceptance evidence:** Test fixtures prove timing and fee calculations across conventions, servicing events show the governing policy version, and release evidence includes examples of cured and uncured delinquency paths.

### 12. Usage and meter-based billing support

**Justification:** Many equipment contracts include base rent plus overage by hours, miles, cycles, prints, or production units. If the PBC ignores usage, it cannot support common copier, fleet, and industrial-equipment deals.

**Improvement:** Add usage contracts to `equipment_lease` and `payment_schedule`, with included allowance, overage rate, meter source, estimated billing, true-up cadence, and disputed-usage workflow. Support manual meter entry, telematics feeds, and locked billing snapshots.

**Acceptance evidence:** Usage-driven invoices reconcile to the underlying meter records, disputed readings pause only the disputed component, and workbench evidence shows allowance consumption and true-up history.

### 13. Maintenance reserve and escrow administration

**Justification:** Aviation, transportation, and specialty assets often require reserves or escrow balances for maintenance and end-of-term obligations. These balances affect payoff, transfer, and default outcomes.

**Improvement:** Add reserve ledgers for `equipment_lease` covering collection basis, draw rules, approval thresholds, expiration, and unused-balance disposition. Link each reserve movement to the underlying asset, event, or maintenance approval.

**Acceptance evidence:** Reserve balances recalculate correctly through billing and draw events, unauthorized draws are blocked, and release evidence includes a reserve-funded maintenance reimbursement flow.

### 14. Residual setting and review workflow

**Justification:** Residual assumptions drive pricing, structuring, and investor appetite. A weak residual process creates losses at end of term and masks concentration risk in certain equipment classes.

**Improvement:** Expand `residual_value` into a governed workflow with origination assumptions, supporting market comps, appraisal source, residual curve version, review cadence, and downgrade triggers. Distinguish booked residual, current estimated residual, and stressed residual.

**Acceptance evidence:** Residual reviews are due according to policy, downgrades create pricing or risk alerts where appropriate, and the detail UI shows original versus current versus stressed values with supporting evidence.

### 15. Residual remarketing and realized-value feedback loop

**Justification:** Residual risk management improves only when actual sale or re-lease outcomes feed back into future pricing and review decisions. Otherwise the platform keeps repeating the same assumption errors.

**Improvement:** Link `residual_value`, `repo_case`, and end-of-term disposition events so realized proceeds, selling costs, downtime, and asset condition scores update residual analytics. Add concentration reporting by equipment class, manufacturer, age band, and geography.

**Acceptance evidence:** Actual remarketing outcomes update residual performance dashboards, realized-versus-booked variances are measurable by cohort, and release evidence includes at least one repossessed and one voluntary return feedback example.

### 16. Buyout quote engine with date-sensitive economics

**Justification:** Buyout requests are common and often contentious. Quotes must reflect payoff date, unearned income treatment, taxes, residual, unpaid fees, stipulations, and whether the contract allows partial or early buyout.

**Improvement:** Enrich `buyout_quote` to calculate scheduled payoff, accelerated payoff, FMV quote, fixed purchase option, casualty payoff, and sectioned quote components such as principal, accrued rent, fees, taxes, reserve adjustments, and title charges. Preserve the assumptions used to generate each quote.

**Acceptance evidence:** Quotes reproduce consistently for the same effective date and policy version, expired quotes are clearly marked, and workbench detail shows a line-by-line payoff explanation suitable for customer service and audit review.

### 17. End-of-term decision management

**Justification:** The contract does not end when the last rent posts. Equipment finance teams must manage renewals, returns, purchases, extensions, holds, and month-to-month rent without losing control of asset location or obligation status.

**Improvement:** Add end-of-term workflows for purchase, return, renewal, extension, evergreen rent, and holdover review. Track notice deadlines, asset-inspection requirements, quote expirations, and approval rules for concessionary extensions.

**Acceptance evidence:** Upcoming maturities appear in dedicated workbench queues, missed notice deadlines raise exceptions, and release evidence includes one exercised purchase option and one returned-asset path.

### 18. Renewal, restructure, and modification controls

**Justification:** Borrowers regularly request maturity extensions, payment relief, collateral substitutions, and restructures. Those actions change economics and risk and need more than a free-text servicing note.

**Improvement:** Add formal modification cases linked to `equipment_lease` with reason code, effective date, pre- and post-change economics, consent requirements, and whether the change is a true modification, refinance, or replacement booking. Preserve the original schedule and the approved replacement schedule.

**Acceptance evidence:** Modification packages show before-and-after cash flows, unauthorized material changes are blocked, and servicing history displays a clear chain of restructures and their approvals.

### 19. Collateral package and perfection tracking

**Justification:** Collateral control is central to equipment lending and leasing. Teams need to know what secures the obligation, where liens were filed, when they expire, and what perfection defects remain open.

**Improvement:** Add collateral package records that capture primary asset collateral, additional collateral, cross-collateralization, filing jurisdiction, filing number, continuation deadlines, title status, and possession or control requirements. Link deficiencies directly to booking and default workflows.

**Acceptance evidence:** Perfection gaps block funding or raise tracked exceptions according to policy, upcoming continuation deadlines appear in operational queues, and evidence includes lien and title status examples for titled and non-titled assets.

### 20. Insurance and collateral-protection monitoring

**Justification:** Lapses in insurance or loss-payee coverage materially change recovery risk. Equipment portfolios also rely on GPS, service obligations, or location restrictions that need ongoing monitoring.

**Improvement:** Add insurance and collateral-protection controls for policy type, coverage amount, named insured, additional insured or loss-payee status, expiration, tracking-device requirement, and field-inspection cadence. Generate servicing events when required protections lapse.

**Acceptance evidence:** Coverage expirations and missing endorsements surface as timed alerts, proof-of-insurance documents are linked to the lease and asset, and release evidence includes lapse, cure, and escalation scenarios.

### 21. Delinquency, collections, and workout segmentation

**Justification:** Collections strategies differ by product, collateral recoverability, customer type, and promise-to-pay quality. A single generic collections status does not support equipment finance operations.

**Improvement:** Add collections segmentation for soft delinquency, hard delinquency, workout, litigation hold, bankruptcy hold, and charge-off preparation. Track promises to pay, dispute flags, cure deadlines, deferment approvals, and collector strategy notes in structured form.

**Acceptance evidence:** Collection queues segment correctly by delinquency and strategy, promise-to-pay breaches create timed follow-up tasks, and release evidence shows the journey from first missed payment to either cure or workout escalation.

### 22. Hardship, deferral, and covenant-waiver controls

**Justification:** Temporary payment relief and covenant waivers are common in stressed portfolios, but they can quietly distort portfolio metrics if they are not modeled explicitly. Operations needs to distinguish approved relief from uncontrolled delinquency.

**Improvement:** Add formal relief programs with reason, term, payment treatment, accrued-interest handling, reporting classification, and expiration rules. Require dual approval for covenant waivers, payment holidays, or principal-only periods above a configurable materiality threshold.

**Acceptance evidence:** Relief-modified schedules are reproducible, waiver approvals are visible in the case history, and release evidence includes side-by-side reporting for normal, deferred, and re-aged accounts.

### 23. Repossession case management

**Justification:** Repossession is a high-risk, high-visibility domain process involving notices, third parties, field actions, asset condition, and legal restrictions. The current `repo_case` surface should become a full operational case.

**Improvement:** Expand `repo_case` with notice generation, assignment to repossession vendors, legal hold flags, cure-period countdowns, voluntary surrender path, asset-location updates, condition grading, and chain-of-custody evidence. Support state-specific or country-specific workflow differences through policy rules.

**Acceptance evidence:** Repo timelines are complete and auditable, mandatory notices cannot be skipped, vendor actions are time-stamped, and release evidence contains a full cure-versus-recover scenario.

### 24. Disposition, remarketing, and loss allocation

**Justification:** After recovery, teams need to manage refurbishment, storage, transport, sale channel, proceeds, and deficiency calculations. Without structured disposition data, recovery performance stays opaque.

**Improvement:** Add post-recovery workflows covering inspection, repair authorization, auction or negotiated sale, re-lease, storage costs, transport costs, net proceeds, and deficiency or surplus allocation. Feed realized disposition economics back to residual and loss reporting.

**Acceptance evidence:** Net recovery waterfalls reconcile from gross proceeds to final gain or loss, disposition cycle times are measurable, and evidence includes one auction disposition and one re-lease example.

### 25. Syndication and participation allocations

**Justification:** Many equipment finance originators syndicate or sell participations in booked deals. The platform needs to know which investors own which slices so cash, risk, and servicing responsibilities remain accurate.

**Improvement:** Add investor allocation records to `equipment_lease` for lead-owned, syndicated, participated, or warehouse-funded positions, including effective dates, retained strip, servicing fee basis, and consent requirements for modifications or defaults. Support post-book assignment changes.

**Acceptance evidence:** Investor shares reconcile to 100 percent of the tracked exposure, cash distributions reflect retained and sold interests, and release evidence includes one pre-funding syndication and one post-book participation transfer.

### 26. Investor reporting and remittance waterfalls

**Justification:** Syndicated equipment deals require transparent remittance reporting. If investor waterfalls are opaque, accounting disputes and servicing breaches follow quickly.

**Improvement:** Build remittance logic for billed rent, collected cash, fees, recoveries, losses, reserve balances, and servicing compensation across multiple investor positions. Distinguish booked cash, allocated cash, and remitted cash with exception handling for shortfalls and reversals.

**Acceptance evidence:** Investor statements reconcile to servicing events and cash movements, remittance exceptions create work queues, and release evidence includes waterfall reports with supporting calculations.

### 27. Portfolio concentration and exposure analytics

**Justification:** Equipment finance risk accumulates by collateral type, manufacturer, geography, industry, obligor group, residual profile, and syndication channel. Operational teams need concentration views inside the workbench, not only in external reporting.

**Improvement:** Add portfolio analytics that segment exposure by equipment category, mobility, vintage, residual-bearing status, investor channel, dealer, and covenant profile. Include stressed exposure views for delinquent, uninsured, under-collateralized, and high-residual cohorts.

**Acceptance evidence:** Analytics drill from portfolio view to deal and asset detail, thresholds trigger policy-driven alerts, and release evidence includes concentration packs with threshold breaches and operator responses.

### 28. Exception taxonomy tuned for equipment finance

**Justification:** Domain exceptions are not interchangeable. A missing serial number, a stale UCC continuation, a disputed meter reading, and an expired insurance binder require different queues, owners, and SLA rules.

**Improvement:** Replace generic exception handling with a controlled taxonomy covering origination, documentation, funding, schedule, usage, collateral, insurance, collections, repo, remarketing, investor, and release-readiness exceptions. Track severity, customer impact, recovery impact, and regulatory or legal sensitivity separately.

**Acceptance evidence:** Every exception opens in a typed queue with the correct owner and SLA, dashboards show aging by taxonomy, and evidence includes representative resolution narratives for at least five distinct exception classes.

### 29. Manual override governance

**Justification:** Equipment finance operations needs overrides, but ungoverned overrides destroy consistency and auditability. The platform should make exceptions visible without preventing legitimate business judgment.

**Improvement:** Require structured justification, approving authority, expiration, and compensating control for overrides affecting pricing, collateral, residual, schedule regeneration, buyout concessions, or repossession holds. Separate temporary operational overrides from permanent policy exceptions.

**Acceptance evidence:** Overrides are searchable by type and approver, expired overrides trigger follow-up actions, and release evidence includes both an approved override and a blocked override attempt.

### 30. Document intake and semantic extraction for finance packs

**Justification:** Equipment finance files contain quotes, invoices, purchase orders, master lease agreements, schedules, guaranties, insurance certificates, titles, UCC searches, and payoff letters. Agents can help only if they extract the right fields and expose confidence clearly.

**Improvement:** Extend assistant intake to classify document type, extract finance-relevant fields, and map them to safe draft updates for `equipment_lease`, `leased_asset`, `buyout_quote`, and `repo_case`. Require citation spans for extracted purchase option language, serials, payoff terms, and notice clauses.

**Acceptance evidence:** Extraction tests cover agreements, invoices, insurance certificates, and payoff letters, low-confidence fields require human confirmation, and UI previews show the source text for every suggested mutation.

### 31. Agent skill for structuring and pricing assistance

**Justification:** Deal teams need guided help assembling a viable structure, not a generic assistant that only restates inputs. The assistant should reason about equipment finance choices while staying inside policy boundaries.

**Improvement:** Add a structuring skill in `LeaseLendingEquipmentFinanceAssistantPanel` that proposes lease versus loan alternatives, highlights collateral or residual implications, suggests schedule patterns, and explains likely approval conditions. Limit the skill to draft outputs and policy-aware recommendations until a human confirms the structure.

**Acceptance evidence:** Prompt-to-draft runs are reproducible, recommendations cite the inputs and policy rules used, and blocked recommendations appear when the assistant tries to exceed approved authority.

### 32. Agent skill for servicing and customer-ops assistance

**Justification:** Servicing teams field payoff, extension, usage dispute, and default-status requests continuously. A domain-trained assistant can reduce cycle time if it summarizes the account state accurately and safely.

**Improvement:** Add a servicing skill that assembles account snapshots, explains delinquency and payoff composition, drafts customer-ready summaries, and prepares structured servicing actions such as quote generation or modification requests. Require permission-aware redaction of sensitive party or investor data.

**Acceptance evidence:** Assistant responses match the current governed record state, sensitive data is hidden for unauthorized roles, and release evidence includes audited examples of quote, extension, and collections support flows.

### 33. Agent skill for exception triage and next-best action

**Justification:** High-value operations gains come from clearing exceptions faster. The assistant should help sort the queue by severity, recoverability, due date, and missing evidence rather than answering free-form questions only.

**Improvement:** Add a triage skill that groups equipment finance exceptions, suggests next-best actions, drafts follow-up tasks, and identifies stale blockers such as missing titles, stale insurance, incomplete repo notices, or unresolved investor approvals. Require every suggestion to reference the underlying lease, asset, or case records.

**Acceptance evidence:** Triage suggestions reduce queue-aging in test scenarios, every suggestion links to record evidence, and reviewers can accept, edit, or reject recommendations with feedback logged for future tuning.

### 34. Workbench landing page for origination and servicing queues

**Justification:** Equipment finance users need to enter the system through operational queues, not static summary cards. The landing page should immediately show what requires underwriting action, funding action, collections action, or end-of-term action.

**Improvement:** Redesign `LeaseLendingEquipmentFinanceWorkbench` around queue-first panels: ready to fund, conditions due, schedule exceptions, insurance lapses, maturities within window, delinquent accounts, repossession cases, and investor remittance breaks. Include saved views for originations, servicing, collateral, and recovery personas.

**Acceptance evidence:** Queue counts reconcile to underlying records, persona-specific default layouts load correctly, and release evidence includes screenshots and interaction traces for each major persona.

### 35. Deal detail UI with economics, collateral, and history together

**Justification:** Operators lose time when contract economics, collateral facts, schedule history, and exception state sit on separate disconnected pages. A deal detail view should tell the whole story of a financed asset set.

**Improvement:** Expand `LeaseLendingEquipmentFinanceDetail` into a tabbed or sectional view that combines contract summary, cash-flow profile, assets, collateral status, conditions, servicing history, investor allocations, and end-of-term outlook. Make history version-aware so users can compare the current state to prior approved states.

**Acceptance evidence:** The detail UI shows a coherent record history without hidden joins, users can compare schedule versions and modification states, and evidence includes role-based view differences for operations, credit, and collections users.

### 36. Asset and collateral workspace

**Justification:** Asset-level issues often drive the real risk: missing serials, mismatched locations, title defects, inactive insurance, or pending substitutions. Those issues deserve a dedicated workspace rather than scattered fields.

**Improvement:** Add an asset and collateral workspace that groups `leased_asset`, perfection records, insurance status, inspections, condition scores, telematics data, and substitution history. Let users pivot from one asset to every lease, schedule, exception, and repo case tied to it.

**Acceptance evidence:** Asset searches find records by serial, title, registration, or location, asset-centric exception counts reconcile correctly, and release evidence includes an asset substitution and collateral-cure example.

### 37. Collections, repo, and recovery workspace

**Justification:** Once a deal is troubled, teams need one place to manage cure notices, field actions, promises to pay, repo assignments, asset recovery, and disposition economics. Fragmented tooling slows recovery and increases legal risk.

**Improvement:** Build a recovery workspace centered on `lease_servicing_event` and `repo_case` with configurable case boards, countdown timers, vendor assignments, cure payment tracking, recovered-asset milestones, and net recovery waterfalls. Expose legal-hold and bankruptcy flags prominently.

**Acceptance evidence:** Collections-to-repo-to-disposition handoffs are visible without leaving the package, overdue case steps are highlighted, and release evidence includes full lifecycle screenshots plus event logs.

### 38. Event model and immutable servicing history

**Justification:** Disputes over funding, delinquency, quote timing, and repossession notices often turn on sequence and timing. The platform needs a reliable event stream, not a mutable notes table.

**Improvement:** Expand `lease_servicing_event` into an immutable event ledger that captures who did what, on which record, under which policy version, with before-and-after economic summaries where applicable. Separate user actions, system calculations, assistant suggestions, and inbound dependency events.

**Acceptance evidence:** Event replay reconstructs the current state for representative deals, event ordering is deterministic, and evidence includes redacted event timelines for origination, modification, default, and payoff scenarios.

### 39. API surface for search, simulation, correction, and exports

**Justification:** The current manifest exposes create-oriented APIs, but equipment finance operations also needs search, quote recalculation, exception management, and evidence exports. Without those surfaces, UI and automation stay thin.

**Improvement:** Add governed APIs for deal search, asset search, schedule simulation, residual review, buyout recalculation, modification drafting, exception acknowledgement, repo progression, investor remittance export, and release-evidence export. Require idempotency keys for any mutating endpoint that may be retried.

**Acceptance evidence:** API contracts cover both command and query use cases, idempotent retries do not duplicate actions, and release evidence includes request and response examples for the new critical routes.

### 40. Data model expansion for economic and legal subrecords

**Justification:** The manifest tables are a solid start, but equipment finance needs richer subrecords than the current top-level list implies. Economic components, legal documents, perfection details, and investor allocations should be explicit entities.

**Improvement:** Add owned child records for fee components, tax components, approval conditions, collateral filings, insurance coverage, reserve balances, usage snapshots, investor allocations, remittance runs, modification cases, and disposition outcomes. Keep these owned by the PBC rather than spreading finance logic into adjacent packages.

**Acceptance evidence:** Schema migrations create the new owned records, relational tests prove referential behavior, and release evidence lists each new entity with its operating purpose.

### 41. Policy-rule and parameter governance

**Justification:** Product behavior in equipment finance changes through policy: maximum advance rates, residual caps, dual-approval thresholds, grace windows, and repo escalation timing. Those controls need transparent governance and versioning.

**Improvement:** Use the existing policy-rule and runtime-parameter surfaces to version origination, servicing, collateral, residual, and recovery policies with effective dates, tenant scope, and approval history. Add simulation before activation so teams can see which active leases or open cases would be affected.

**Acceptance evidence:** Policy diffs are visible, future-dated changes can be simulated without mutating production records, and release evidence includes activation records plus regression tests for retired and current policy versions.

### 42. Release evidence pack tied to domain workflows

**Justification:** A package that handles financing, collateral, and recovery must prove more than unit-test coverage. Release readiness should show that the major business flows are demonstrably supported end to end.

**Improvement:** Turn `RELEASE_EVIDENCE.md` into a structured pack containing origination, funding, schedule generation, usage billing, residual review, buyout, modification, delinquency, repossession, recovery, and syndication scenarios. Include role screenshots, API examples, event traces, and assistant transcripts where relevant.

**Acceptance evidence:** Every major workflow listed above appears in the release pack with a dated trace, evidence references are reproducible, and missing evidence blocks release approval until the gap is resolved.

### 43. Scenario library and regression matrix

**Justification:** Equipment finance behavior breaks at the edges: odd first periods, partial deliveries, serial substitutions, partial payoffs, quote expirations, investor transfers, and disputed usage. Those edge cases need explicit regression scenarios.

**Improvement:** Build a scenario library covering product structures, funding patterns, payment shapes, asset substitutions, residual downgrades, buyout concessions, hardship modifications, repossession outcomes, and syndication events. Tie scenarios directly to package tests and release evidence references.

**Acceptance evidence:** The regression matrix maps scenarios to tests and evidence artifacts, new defects add new scenarios, and release evidence identifies which scenario IDs passed for the build.

### 44. Migration and backfill evidence for existing portfolios

**Justification:** Real-world rollout often starts with an existing booked portfolio. Migration quality is critical because bad imported schedules, collateral facts, or investor allocations can undermine trust immediately.

**Improvement:** Add migration and backfill plans for booked leases, open schedules, residual assumptions, buyout quotes in flight, active repo cases, and existing servicing history. Validate imported data against the new policy and asset-traceability rules before activation.

**Acceptance evidence:** Migration dry runs produce reconciliation reports, unmapped or invalid records are quarantined with reasons, and release evidence includes import validation for at least one active and one distressed portfolio segment.

### 45. Operational SLA and cycle-time instrumentation

**Justification:** Teams need to know how long origination, funding, quote issuance, exception resolution, repo progression, and investor remittance take in practice. Without timing evidence, backlog improvements cannot be prioritized rationally.

**Improvement:** Instrument the package to measure time-to-approve, time-to-fund, schedule-generation latency, quote-turnaround time, exception-aging, recovery-cycle time, and remittance completion time. Distinguish policy pauses from operational delays.

**Acceptance evidence:** SLA dashboards show current and breached items, timers pause and resume according to configured rules, and release evidence includes baseline and target cycle times for the core workflows.

### 46. Risk scoring and anomaly detection grounded in finance signals

**Justification:** The manifest already declares predictive risk and anomaly capabilities, but they need equipment-finance features rather than generic activity signals. Residual stress, serial anomalies, insurance lapses, and collateral perfection defects matter more than generic volume spikes.

**Improvement:** Train risk and anomaly models using domain signals such as residual volatility, unusual usage trends, funding-before-acceptance patterns, concentration build-up, repeat dealer exceptions, delinquency cures followed by repeat default, and mismatched title or insurance data. Expose model explanations in business language.

**Acceptance evidence:** Scores and anomalies cite the finance features that drove them, reviewers can compare recommended action to actual outcomes, and release evidence includes calibration and false-positive summaries.

### 47. Security, privacy, and authority boundaries for agent-assisted actions

**Justification:** Finance servicing and recovery data is sensitive, and assistant actions can become a hidden control bypass if they are not tightly bounded. The package needs clear authority boundaries for people and agents.

**Improvement:** Enforce action-level permissions for quote generation, modification drafting, condition waiver, repo progression, investor export, and release-evidence publication. Require assistant actions to generate proposed commands, visible diffs, and actor attribution before execution.

**Acceptance evidence:** Unauthorized agent actions are blocked with auditable reasons, every assistant-issued command is attributable and reviewable, and release evidence includes permission matrices plus denial-path tests.

### 48. Continuous control testing for financing and collateral controls

**Justification:** Control assertions are most useful when they run continuously against live operations. Equipment finance needs automated checks for segregation of duties, missing approvals, stale collateral filings, expired insurance, and unreconciled investor balances.

**Improvement:** Use `lease_lending_equipment_finance_control_assertion` to schedule recurring control tests over funding approvals, residual changes, buyout concessions, repo notices, remittance allocation, and release-evidence completeness. Publish failures directly into typed exception queues.

**Acceptance evidence:** Control failures are reproducible from source data, exceptions link back to the failed control and affected deals, and release evidence includes current control-pass and control-fail examples with remediation.

### 49. Go-live readiness by phased operating scope

**Justification:** Equipment finance rollouts usually land in phases: basic origination first, then servicing, then recovery, then investor operations. The backlog should explicitly support staged deployment instead of assuming one big-bang launch.

**Improvement:** Define readiness gates for phase 1 origination and booking, phase 2 servicing and end-of-term, phase 3 collections and repossession, and phase 4 syndication and investor remittance. Map required evidence, training, data quality, and fallback plans to each phase.

**Acceptance evidence:** Each phase has a signed checklist, missing capabilities block only the relevant phase, and release evidence shows which phase scope was approved for the current version.

### 50. Final acceptance rubric for the package

**Justification:** A domain-deep backlog needs a clear finish line. Without a package-specific rubric, teams will declare success based on code completion instead of operational readiness and finance correctness.

**Improvement:** Add a final acceptance rubric for `lease_lending_equipment_finance` covering contract structures, asset and collateral traceability, schedule accuracy, usage billing, residual governance, buyout correctness, repossession workflow, syndication support, typed exceptions, persona UI coverage, agent-skill safety, and release evidence completeness. Require the rubric to be reviewed on every material release.

**Acceptance evidence:** The rubric is stored with the package docs, every release marks pass, partial, or fail for each acceptance area, and the current release evidence contains the completed rubric with named reviewers and dated sign-off.
