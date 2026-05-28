# Real Estate Property Management Improvement Backlog

## Current Domain Evidence Used

- PBC key in scope: `real_estate_property_management`.
- Manifest evidence shows the package owns property, tenant, lease, rent charge, maintenance request, inspection, and security deposit records, plus policy, runtime parameter, schema extension, control assertion, and governed model tables.
- Current APIs already expose `POST /propertys`, `POST /tenants`, `POST /leases`, `POST /rent-charges`, `POST /maintenance-requests`, and `GET /real-estate-property-management-workbench`.
- Current UI fragments already named in the package are `RealEstatePropertyManagementWorkbench`, `RealEstatePropertyManagementDetail`, and `RealEstatePropertyManagementAssistantPanel`.
- Current domain operations in `domain_depth.py` include `create_property`, `record_tenant`, `review_lease`, `approve_rent_charge`, `simulate_maintenance_request`, `create_inspection`, and `record_security_deposit`.
- Current AppGen-X event surfaces in `events.py` emit `RealEstatePropertyManagementCreated`, `RealEstatePropertyManagementUpdated`, `RealEstatePropertyManagementApproved`, and `RealEstatePropertyManagementExceptionOpened`, and consume `PolicyChanged`, `CustomerUpdated`, and `SupplierQualified`.
- Current assistant and governed CRUD surfaces in `agent.py` already expose `agent_skill_manifest()`, `chatbot_interface_contract()`, `document_instruction_plan()`, and `datastore_crud_plan()`.
- Current release and verification surfaces already exist in `release_evidence.py`, `runtime.py`, `RELEASE_EVIDENCE.md`, `SPECIFICATION.md`, and `tests/test_contract.py`.

### 1. Portfolio and building hierarchy
**Justification:** The current owned `property` record is too flat for operators who manage portfolios, buildings, phases, and mixed-use sites with different ownership and reporting boundaries.
**Improvement:** Add an explicit portfolio hierarchy model that links portfolio, property, building, floor, and rentable area so one workbench can answer who owns the asset, who manages it, which leases belong to it, and which compliance obligations apply.
**Acceptance evidence:** `SPECIFICATION.md` describes the hierarchy, `migrations/001_initial.sql` is superseded by owned follow-on migrations for portfolio and building tables, and `RealEstatePropertyManagementWorkbench` can filter by portfolio, property, and building without raw SQL.

### 2. Unit inventory and availability ledger
**Justification:** Real estate operations break down when units are implied inside free-form payloads instead of being first-class records with status, marketability, and rent-ready dates.
**Improvement:** Introduce owned unit records tied to property and building entities, with fields for unit type, bedroom/bath mix, square footage, occupancy status, market rent, notice status, and make-ready target date.
**Acceptance evidence:** Unit inventory appears as a dedicated board in the workbench, availability counts reconcile to the rent roll, and contract tests prove unit creation and updates stay inside `real_estate_property_management_*` tables.

### 3. Property attribute completeness rules
**Justification:** Leasing, compliance, and maintenance decisions depend on property facts such as address, jurisdiction, utility responsibility, and amenity set being complete and trustworthy.
**Improvement:** Add property-level completeness scoring and blocking rules so a property cannot become leaseable until required regulatory, operational, and marketing attributes are present and validated.
**Acceptance evidence:** Rule definitions for property completeness are surfaced through the rule editor contracts, failed properties show blocking reasons in `RealEstatePropertyManagementDetail`, and release evidence includes completeness-rule pass rates.

### 4. Lease abstract and clause capture
**Justification:** Teams need structured lease abstracts for rent, deposit, renewal, notice, and maintenance obligations rather than storing those terms only inside attached PDFs.
**Improvement:** Expand the lease model to capture start and end dates, renewal options, break clauses, notice windows, rent steps, deposit rules, pet clauses, service obligations, and special concessions as discrete fields.
**Acceptance evidence:** `document_instruction_plan()` can preview extraction targets for lease clauses, lease detail screens show a structured abstract next to the source document, and test fixtures cover fixed-term, month-to-month, and early-termination leases.

### 5. Tenant household and occupant registry
**Justification:** Collections, compliance, and move-out disputes require more than a single tenant row; operators need the household, guarantor, and authorized occupant context.
**Improvement:** Model primary tenant, co-tenant, guarantor, occupant, and emergency contact roles with move-in and move-out dates, identity verification state, and communication preferences.
**Acceptance evidence:** Tenant records show household composition in the detail view, assistant read flows summarize the full household rather than one person, and policy tests prevent unauthorized exposure of guarantor-only fields.

### 6. Rent roll snapshots with drill-through
**Justification:** Asset managers need a true rent roll by property, unit, lease, and tenant, not a list of rent charge rows that require manual reconciliation.
**Improvement:** Build daily and month-end rent roll projections that show occupied and vacant units, contracted rent, concessions, arrears, deposits held, lease end dates, and upcoming notices.
**Acceptance evidence:** `GET /real-estate-property-management-workbench` returns rent-roll filters and summary totals, month-end snapshots are replayable from AppGen-X events, and `RELEASE_EVIDENCE.md` includes sample rent-roll reconciliation output.

### 7. Charge schedule and proration engine
**Justification:** Mid-month move-ins, transfers, and renewals create proration rules that are easy to get wrong if rent charges are created one line at a time.
**Improvement:** Add a charge scheduler that generates recurring base rent, one-time fees, utility pass-throughs, parking charges, and proration entries from the lease abstract and unit occupancy dates.
**Acceptance evidence:** `approve_rent_charge` scenarios cover full-month, prorated, free-rent, and mid-cycle amendment cases, generated charges link back to the source lease version, and the workbench can explain each proration formula.

### 8. Arrears aging and collections waterfall
**Justification:** Property teams need arrears control by bucket, promise-to-pay status, and escalation stage, not just a boolean “past due.”
**Improvement:** Create a collections ledger with aging buckets, collector assignment, payment-plan state, dispute flag, late-fee policy, and next action date at tenant, lease, unit, and property level.
**Acceptance evidence:** Arrears queues display 1-30, 31-60, 61-90, and 90+ buckets, exception events are emitted when arrears cross configured thresholds, and tests verify the same unpaid charge does not double-age after event replay.

### 9. Security deposit lifecycle
**Justification:** Deposits are a regulated trust obligation with distinct states from collection through refund or claim.
**Improvement:** Expand `security_deposit` handling to cover deposit invoice, receipt, trust account allocation, interest accrual where required, holdback for damages, refund approval, and dispute resolution.
**Acceptance evidence:** `record_security_deposit` operations show deposit state transitions, control assertions confirm segregation between deposit receipt and refund approval, and release evidence includes a refund-versus-held balance report.

### 10. Move-in checklist and condition capture
**Justification:** Move-in evidence is the baseline for later deposit claims and maintenance accountability.
**Improvement:** Add move-in workflows with checklist templates, signed resident acknowledgments, meter reads, key inventory, appliance serial capture, and photo/video condition evidence tied to the unit and lease.
**Acceptance evidence:** `create_inspection` supports move-in inspection type, `RealEstatePropertyManagementAssistantPanel` can summarize missing move-in evidence, and package tests cover signed versus unsigned move-in packets.

### 11. Move-out reconciliation and disposition accounting
**Justification:** Deposit disputes usually come from weak move-out accounting, not from the original deposit collection.
**Improvement:** Build a move-out reconciliation workflow that compares move-in and move-out condition, outstanding rent, utilities, damage charges, cleaning, and forwarding-address status before calculating deposit return or claim.
**Acceptance evidence:** Move-out detail screens show a side-by-side condition comparison, refund and chargeback decisions produce immutable event history, and `RELEASE_EVIDENCE.md` includes a sample disposition package.

### 12. Renewal pipeline and rate decisioning
**Justification:** Renewals drive occupancy and revenue; they need pipeline visibility well before a lease expires.
**Improvement:** Add renewal stages for upcoming, offer drafted, offer sent, resident negotiating, accepted, declined, and expired, with renewal pricing guidance tied to unit availability and arrears status.
**Acceptance evidence:** Upcoming renewals are visible 30, 60, and 90 days out, operators can filter by acceptance probability, and tests verify a renewed lease rolls future rent charges without duplicating the old lease term.

### 13. Notice management and statutory deadlines
**Justification:** Renewal notices, pay-or-quit notices, entry notices, and non-renewal letters all have different timing and jurisdictional rules.
**Improvement:** Introduce a notice registry that stores notice type, required lead time, service method, proof of service, cure period, and jurisdictional basis for each property and lease.
**Acceptance evidence:** Notice due dates are generated from lease and jurisdiction settings, proof-of-service artifacts are linked in the detail screen, and policy rules block eviction-stage actions when required notices are missing or late.

### 14. Service request triage
**Justification:** Maintenance and resident experience depend on routing service requests correctly the first time by urgency, trade, and habitability impact.
**Improvement:** Extend `maintenance_request` into a service-request intake queue with category, severity, affected asset, resident-access constraints, after-hours flag, and auto-triage rules for habitability and safety issues.
**Acceptance evidence:** `simulate_maintenance_request` previews routing before mutation, urgent habitability issues jump to the top of the edge-case queue, and contract tests cover duplicate resident submissions with one resulting work order.

### 15. Work order execution and vendor dispatch
**Justification:** A service request is not enough; operations need the downstream work order, assignment, vendor dispatch, and completion evidence.
**Improvement:** Split intake from execution by introducing work-order records with assignment, scheduled window, labor and material estimates, vendor acceptance, on-site notes, and completion sign-off.
**Acceptance evidence:** Service requests can spawn one or more work orders, `SupplierQualified` consumption affects vendor eligibility, and workbench drill-through shows request-to-work-order conversion and close-out timing.

### 16. Preventive maintenance calendars
**Justification:** Fire safety checks, HVAC service, lift inspections, and common-area upkeep should be planned work, not only reactive tickets.
**Improvement:** Add preventive maintenance schedules by property, building system, and unit type with recurring cadence, next due date, vendor template, and completion proof requirements.
**Acceptance evidence:** Preventive tasks appear in forecast boards, missed cycles emit `RealEstatePropertyManagementExceptionOpened`, and release evidence includes a completed-versus-overdue preventive maintenance report.

### 17. Inspection program expansion
**Justification:** Real estate teams run move-in, move-out, annual, lender, insurance, and health-and-safety inspections that need different templates and consequence rules.
**Improvement:** Expand `inspection` to support inspection type, checklist template, failed-item severity, remediation requirement, reinspection scheduling, and linkages to service requests and notices.
**Acceptance evidence:** Inspection templates are selectable in the UI, failed items can generate maintenance requests and notices, and tests cover failed inspection items reopening until reinspection passes.

### 18. Compliance obligations by jurisdiction
**Justification:** Compliance is property-specific and jurisdiction-specific; a single generic compliance flag does not protect operators or residents.
**Improvement:** Create a compliance library for licensing, occupancy permits, lead-based paint disclosures, safety certificates, fair-housing postings, entry rules, and local notice standards by property jurisdiction.
**Acceptance evidence:** Each property detail screen shows active compliance obligations, overdue obligations raise exception records, and `PolicyChanged` events can update obligations without rewriting historical compliance evidence.

### 19. Contractor qualification and insurance tracking
**Justification:** Maintenance dispatch should not assign uninsured or unapproved vendors to occupied units.
**Improvement:** Add vendor qualification checks for insurance expiry, trade license, resident-access approval, and property-specific restrictions before a work order can be assigned.
**Acceptance evidence:** `SupplierQualified` inbox events update assignment eligibility, blocked vendors are explained in the dispatch UI, and control assertions verify no completed work order references an ineligible vendor.

### 20. Vacancy turn and rent-ready workflow
**Justification:** Vacancy loss is driven by days-turn, missed handoffs, and unclear readiness ownership.
**Improvement:** Introduce a vacancy-turn workflow from notice received through move-out, inspection, make-ready, marketing ready, and lease-ready, with target dates and blocker reasons at each stage.
**Acceptance evidence:** Unit boards show a turn timeline and blocker owner, days-vacant metrics appear in workbench analytics, and release evidence includes median turn-time by property.

### 21. Make-ready budgeting and cost capture
**Justification:** Property teams need to distinguish routine make-ready cost from capital improvement and damage recovery.
**Improvement:** Record make-ready scope, budget, approvals, actual labor, actual materials, and recoverable tenant damage amounts as part of the vacancy-turn process.
**Acceptance evidence:** Work orders and move-out charges reconcile to make-ready budgets, approval thresholds are enforced through runtime parameters, and reports distinguish recoverable versus non-recoverable turn costs.

### 22. Utility responsibility and recovery
**Justification:** Many lease disputes come from unclear utility responsibility, meter reads, and shared-area recovery rules.
**Improvement:** Add utility responsibility fields at property, unit, and lease level, along with meter-read capture, move-in/move-out read events, and configurable pass-through charge generation.
**Acceptance evidence:** Move-in and move-out workflows require utility reads when configured, rent charges can show utility pass-through source data, and tests cover shared utilities, resident-direct bills, and vacant-unit owner responsibility.

### 23. Payment exception handling
**Justification:** Returned payments, partial payments, and unapplied cash distort arrears reporting if they are absorbed into manual notes.
**Improvement:** Add explicit exception types for NSF, chargeback, underpayment, overpayment, unapplied credit, and disputed payment, with reversal logic and collector follow-up states.
**Acceptance evidence:** Collections queues identify payment exception type separately from arrears age, emitted events preserve the before-and-after tenant balance, and release readiness checks include payment-exception replay scenarios.

### 24. Concessions, credits, and write-off controls
**Justification:** Revenue leakage often comes from informal credits and concessions that bypass approval policy.
**Improvement:** Model free-rent periods, lease-up concessions, courtesy credits, bad-debt write-offs, and deposit offsets with approval paths based on amount, reason code, and lease stage.
**Acceptance evidence:** Runtime parameters define approval thresholds, denied actions are visible in the UI for unauthorized users, and control assertions prove no write-off posts without the required approver role.

### 25. Lease amendments and transfer history
**Justification:** Unit transfers, roommate changes, rent changes, and parking additions should not overwrite the original lease story.
**Improvement:** Add amendment records with effective dates, superseded terms, resident acknowledgments, and downstream impacts on rent charges, notices, and deposits.
**Acceptance evidence:** Lease detail screens show an amendment timeline, assistant summaries distinguish original versus amended terms, and tests verify historical rent roll snapshots stay stable after later amendments.

### 26. Occupancy and availability board
**Justification:** Site teams need one operational board for occupied, notice given, vacant, make-ready, model, and down units.
**Improvement:** Expand `RealEstatePropertyManagementWorkbench` with an occupancy board that groups units by status, next milestone, days in status, and whether a lease or notice is attached.
**Acceptance evidence:** Occupancy counts reconcile to unit inventory and rent roll totals, filters support property and building views, and UI contract smoke tests include the new board surface.

### 27. Ancillary asset assignments
**Justification:** Parking bays, storage lockers, and amenity rentals create revenue and conflict when they are not tied cleanly to lease terms.
**Improvement:** Add ancillary asset records and assignment history so parking, storage, and amenity usage can be leased, billed, renewed, and reclaimed alongside the main unit.
**Acceptance evidence:** Lease detail shows assigned ancillary assets, rent charge generation includes optional ancillary fees, and move-out workflows reclaim ancillary assets automatically.

### 28. Operator-first detail UI
**Justification:** The current three-fragment UI contract is too generic for day-to-day property operations that depend on fast triage and timeline context.
**Improvement:** Redesign `RealEstatePropertyManagementDetail` to center the entity timeline, related unit and lease links, arrears panel, open service requests, inspection results, notices, and pending approvals on one screen.
**Acceptance evidence:** `real_estate_property_management_ui_contract()` declares the new detail sections, operators can reach related records in one click, and release evidence includes before-and-after time-to-answer measurements for common questions.

### 29. Assistant skills for leasing, collections, and maintenance
**Justification:** The current assistant surface exposes generic create and update tools, but property teams need domain-specific guided actions.
**Improvement:** Extend `agent_skill_manifest()` with skills for draft renewal offer, arrears follow-up summary, move-out disposition checklist, inspection follow-up generation, and maintenance triage recommendation.
**Acceptance evidence:** Assistant manifests list the new skills under the `real_estate_property_management_skills` namespace, each mutation path still requires human confirmation, and tests prove foreign-table mutations remain rejected.

### 30. Document instruction intake for real estate packets
**Justification:** Leases, notices, inspection forms, vendor invoices, and resident letters arrive as documents first and data second.
**Improvement:** Improve `document_instruction_plan()` so it can classify incoming lease packets, notice scans, inspection PDFs, and deposit letters, then map them to property, unit, lease, tenant, or service-request targets with ambiguity warnings.
**Acceptance evidence:** Document previews show candidate tables beyond the current first three defaults, human review screens flag uncertain unit or tenant matches, and release evidence includes representative lease and notice extraction samples.

### 31. Domain-specific emitted events
**Justification:** Four generic emitted event names are not enough for downstream consumers that need leasing, collections, inspection, and maintenance signals.
**Improvement:** Introduce richer event types such as lease_renewal_offered, notice_served, arrears_escalated, service_request_triaged, work_order_completed, inspection_failed, deposit_disposition_completed, and unit_ready_for_leasing while preserving AppGen-X envelope rules.
**Acceptance evidence:** `event_contract_manifest()` lists the expanded domain events, `build_event_envelope()` validates them, and downstream replay tests show the richer event stream can rebuild rent-roll and operations projections.

### 32. Inbox, idempotency, and dead-letter playbooks
**Justification:** Property operations need to understand what to do with duplicate events, invalid supplier updates, and policy changes that cannot be applied cleanly.
**Improvement:** Build operator playbooks and UI actions for inbox replay, duplicate suppression, dead-letter quarantine, fix-and-retry, and permanent closure with domain reason codes.
**Acceptance evidence:** `real_estate_property_management_appgen_dead_letter_event` entries are visible in the workbench, `dispatch_event()` negative cases link to remediation guidance, and tests prove retries do not duplicate rent charges or notices.

### 33. Cross-entity timeline and dossier view
**Justification:** Teams repeatedly need the whole story of a unit or resident across lease, charges, maintenance, inspections, and notices.
**Improvement:** Create a dossier view that merges AppGen-X events and record milestones into one chronological timeline for each property, unit, lease, and tenant.
**Acceptance evidence:** Operators can open a tenant or unit dossier from the workbench, timeline entries link to the originating record and event, and audit reviewers can export a redacted dossier without direct table access.

### 34. Owner statement and asset performance reporting
**Justification:** Property managers need owner-facing reporting, not only internal operational queues.
**Improvement:** Add owner statement outputs covering rent billed, rent collected, concessions, arrears, maintenance spend, make-ready cost, occupancy, and outstanding compliance actions by property and reporting period.
**Acceptance evidence:** Reports reconcile to rent-roll and work-order totals, statement snapshots are versioned for month-end close, and release evidence includes a sample owner statement lineage summary.

### 35. Budget versus actual operations view
**Justification:** Site leaders must see whether maintenance, vacancy, and concession spend is trending against plan.
**Improvement:** Introduce budget lines at property and category level with variance tracking for maintenance, turn cost, concession spend, utility recovery shortfall, and bad debt.
**Acceptance evidence:** Variance indicators appear in analytics panels, exception events fire when thresholds are breached, and tests verify variance calculations survive historical event replay and late adjustments.

### 36. Fraud and anomaly detection
**Justification:** Deposit refunds, repeated credits, suspicious vendor billing, and charge reversals are fraud-prone areas in property operations.
**Improvement:** Use the existing anomaly and predictive-risk capability hooks to score unusual deposit refunds, repeated maintenance requests on the same unit, rapid write-offs, and vendor concentration anomalies.
**Acceptance evidence:** Risk explanations show the exact features used, suspicious records route to review queues instead of auto-approval, and release evidence includes precision and false-positive review for sample anomaly cases.

### 37. Multi-tenant operating isolation
**Justification:** One management platform often serves multiple owners, portfolios, or operating companies with different rules and visibility.
**Improvement:** Tighten tenant isolation so owner A cannot see owner B units, notices, deposits, or vendors, while still allowing central corporate oversight with explicit cross-tenant privileges.
**Acceptance evidence:** Isolation tests cover UI filters, CRUD plans, assistant responses, and event projections, and `verify_owned_table_boundary` plus permission tests show no cross-tenant leakage path.

### 38. Approval matrix and segregation of duties
**Justification:** The package already exposes coarse permissions, but property operations need action-specific approvals for concessions, write-offs, refunds, notice issuance, and policy changes.
**Improvement:** Add an approval matrix keyed by action type, amount, risk, and property assignment so one user cannot both initiate and approve high-impact financial or compliance actions.
**Acceptance evidence:** `real_estate_property_management_permissions_contract()` expands beyond operator/approver/auditor with action-level policy rules, denied actions are visible in the UI, and control assertions log segregation breaches.

### 39. Historical conversion and bulk onboarding
**Justification:** New portfolios are usually onboarded in bulk, with existing tenants, lease abstracts, deposits, arrears, and open service requests that must be migrated safely.
**Improvement:** Add a staged conversion workflow for property, unit, tenant, lease, deposit, arrears, and maintenance data with import validation, source-to-target mapping, error buckets, and resumable batches.
**Acceptance evidence:** Bulk import jobs provide row-level outcomes, converted balances reconcile to opening snapshots, and `RELEASE_EVIDENCE.md` contains a cutover checklist and sample conversion evidence.

### 40. Search and entity resolution
**Justification:** Operators often search by resident name, unit number, phone, lease code, notice number, or vendor ticket, and duplicate entities are common.
**Improvement:** Add search indices and merge-candidate detection for properties, units, tenants, leases, service requests, and inspections, with governed merge workflows and survivor rules.
**Acceptance evidence:** Search results can pivot across entity types, duplicate candidates are scored and reviewed before merge, and tests cover same-name tenants in different properties without accidental merge.

### 41. Release evidence tied to domain outcomes
**Justification:** Current release evidence is structural; it needs to prove the package works for leasing, maintenance, collections, and compliance scenarios.
**Improvement:** Expand `real_estate_property_management_build_release_evidence()` so it emits domain scenario evidence for move-in, renewal, arrears escalation, service-request close-out, inspection failure, and deposit disposition.
**Acceptance evidence:** `release_readiness_manifest()` lists domain scenario sections, `validate_release_evidence()` fails when a required scenario artifact is missing, and `RELEASE_EVIDENCE.md` shows scenario IDs linked to code paths and test names.

### 42. Contract tests for real estate workflows
**Justification:** `tests/test_contract.py` currently proves package structure, not end-to-end domain behavior.
**Improvement:** Add workflow tests for property onboarding, unit availability changes, lease creation, rent-roll generation, notice issuance, arrears aging, service-request triage, inspection failure, and deposit refund.
**Acceptance evidence:** `tests/test_contract.py` or adjacent package-local tests exercise those workflows without external dependencies, failures identify the exact domain stage that broke, and test evidence is included in release readiness output.

### 43. API route normalization and backward compatibility
**Justification:** The existing `POST /propertys` route is awkward and risks client drift once unit, notice, renewal, and work-order APIs are added.
**Improvement:** Introduce canonical routes for properties, units, leases, notices, renewals, arrears actions, and work orders while preserving compatibility aliases for current clients until deprecation is complete.
**Acceptance evidence:** `api_route_contracts()` lists canonical and legacy routes, compatibility tests prove old clients still work, and the workbench only advertises canonical endpoints in generated docs.

### 44. Schema evolution for units, notices, and renewals
**Justification:** The current owned schema does not explicitly represent units, notices, renewals, work orders, or occupancy snapshots, yet those are core operating records.
**Improvement:** Register new owned tables through the schema-extension pathway with compatibility checks, projection backfills, and migration sequencing that keeps existing property, tenant, and lease data intact.
**Acceptance evidence:** `real_estate_property_management_register_schema_extension()` accepts the new owned tables, schema contracts show them as owned by the PBC, and migration dry runs prove replay-safe backfills.

### 45. Queue-centered workbench navigation
**Justification:** Property teams work queues first: expiring leases, notices due, arrears escalations, overdue turns, overdue inspections, and aging service requests.
**Improvement:** Reframe `RealEstatePropertyManagementWorkbench` around queue widgets and KPI cards for expiring renewals, notice deadlines, occupancy loss, overdue work orders, open inspection failures, and blocked deposit refunds.
**Acceptance evidence:** `real_estate_property_management_render_workbench()` exposes queue-oriented sections, navigation includes direct entry into edge-case triage, and UI smoke tests confirm queue cards load without side effects.

### 46. Mobile inspection and field maintenance support
**Justification:** Inspectors and technicians work on phones and tablets, often offline or in basements with poor connectivity.
**Improvement:** Add mobile-friendly inspection and work-order flows with cached checklist steps, photo capture, signature collection, and later synchronization through the AppGen-X event contract.
**Acceptance evidence:** Offline-created inspection events replay cleanly into the inbox and outbox flow, detail screens show upload status for photos and signatures, and release evidence includes a field-use smoke scenario.

### 47. Resident communication log
**Justification:** Collections, notices, maintenance coordination, and renewal outreach all depend on knowing what was said, when, and through which channel.
**Improvement:** Add a communication log linked to tenant, lease, unit, and service request records with channel, template used, delivery state, and response summary for calls, email, SMS, and portal messages.
**Acceptance evidence:** Operators can see communication history from the tenant and lease detail views, notices link to their delivery proof, and assistant summaries cite the latest resident contact before suggesting a next action.

### 48. Audit proofs and replayability
**Justification:** Disputes over rent, notices, inspections, or deposit claims require tamper-evident history and reliable replay.
**Improvement:** Extend the existing cryptographic-audit and event-sourced hooks so key domain decisions are hash-linked and every operational projection can be rebuilt from event history plus schema version metadata.
**Acceptance evidence:** Audit proof exports verify successfully against stored hashes, replay checks rebuild rent-roll and arrears views without drift, and `validate_release_evidence()` includes replay-integrity checks as blocking evidence.

### 49. Governed AI recommendations
**Justification:** AI assistance is useful for draft notices, maintenance routing, and renewal summaries, but property teams need explainability and strict human confirmation on every mutation.
**Improvement:** Add governed recommendation flows for renewal pricing rationale, likely notice requirement, service-request severity, and deposit disposition draft, all with explanation text, confidence, and approval capture.
**Acceptance evidence:** `chatbot_interface_contract()` lists the recommendation surfaces, `datastore_crud_plan()` still marks mutations as confirmation-required, and control evidence shows who accepted or rejected each AI suggestion.

### 50. Go-live evidence pack for the PBC
**Justification:** A domain-deep backlog is only useful if the package can prove readiness for a managed release into real property operations.
**Improvement:** Define a release gate that requires passing evidence for portfolio hierarchy, units, leases, tenants, rent rolls, service requests, inspections, maintenance, deposits, arrears, notices, renewals, move-in, move-out, compliance, UI, agent skills, events, and replay-safe release evidence before version promotion.
**Acceptance evidence:** The final go-live pack references `SPECIFICATION.md`, `RELEASE_EVIDENCE.md`, `release_readiness_manifest()`, `validate_release_evidence()`, `event_contract_manifest()`, and the expanded contract tests, and it fails closed if any required domain evidence section is missing.
