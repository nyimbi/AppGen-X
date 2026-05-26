# Time Attendance and Labor Tracking PBC Specification

`time_labor` is the AppGen-X packaged business capability for workforce time,
attendance, schedules, absences, overtime, geo-fenced clock events, labor
allocation, approvals, and payroll-ready labor summaries. The implementation is
owned under `src/pyAppGen/pbcs/time_labor/`.

## Owned Boundary

- **PBC key:** `time_labor`
- **Mesh:** `hcm`
- **Owned tables:** `shift`, `shift_pattern`, `shift_assignment`,
  `shift_swap_request`, `schedule_bid`, `labor_demand_forecast`,
  `clock_event`, `clock_device`, `clock_source_route`, `clock_exception`,
  `time_entry`, `time_entry_line`, `break_deduction`, `overtime_bucket`,
  `premium_calculation`, `holiday_calendar`, `absence`, `absence_balance`,
  `absence_entitlement`, `absence_approval`, `labor_summary`,
  `labor_summary_line`, `labor_cost_allocation`, `labor_distribution`,
  `approval_workflow`, `approval_task`, `employee_projection`,
  `role_projection`, `payroll_labor_projection`,
  `warehouse_site_projection`, `manufacturing_shift_projection`,
  `project_cost_projection`, `time_policy_screening`, `time_audit_trace`,
  `time_hours_proof`, `time_federation_projection`,
  `time_carbon_schedule_window`, `time_schedule_optimization`,
  `time_shift_allocation`, `time_anomaly_signal`, `time_labor_risk_model`,
  `time_labor_risk_forecast`, `time_parsed_event`, `time_seed_data`,
  `time_schema_extension`, `time_control_assertion`,
  `time_governed_model`, `time_rule`, `time_parameter`,
  `time_configuration`, `time_labor_appgen_outbox_event`,
  `time_labor_appgen_inbox_event`, `time_labor_dead_letter_event`
- **Allowed datastores:** PostgreSQL, MySQL, MariaDB
- **Event contract:** AppGen-X outbox/inbox event contract only on fixed topic
  `appgen.time.events`
- **Emits:** `ShiftCreated`, `ClockEventRecorded`, `TimeEntryCalculated`,
  `LaborHoursApproved`, `AbsenceRecorded`
- **Consumes:** `EmployeeCreated`, `RoleChanged`
- **Primary APIs:** `POST /shifts`, `POST /shift-patterns`,
  `POST /shift-swaps`, `POST /clock-events`,
  `POST /time-entries/calculate`, `POST /absences`,
  `POST /labor-summaries/{id}/approve`, `POST /time/events/inbox`,
  `POST /time/rules`, `POST /time/parameters`,
  `POST /time/configuration`, `GET /labor-summaries`,
  `GET /time-workbench`
- **UI artifacts:** time workbench, schedule board, clock event queue, overtime
  review, absence calendar, approval queue, policy editor

The PBC owns time and labor facts. Personnel, payroll, project, manufacturing,
warehouse, and finance packages consume approved labor facts through APIs,
events, and projections rather than shared time tables. Runtime event
infrastructure is owned by `time_labor_appgen_outbox_event`,
`time_labor_appgen_inbox_event`, and `time_labor_dead_letter_event`; these are
package-local implementation tables, not cross-PBC shared integration storage.

## Rules, Parameters, and Configuration

The runtime must execute time and labor rules, parameters, and configuration:

- **Rules:** shift eligibility, clock-in/out sequence, geofence enforcement,
  break requirements, overtime calculation, premium eligibility, absence
  entitlement, approval routing, role-based labor costing, holiday rules,
  rounding policy, and payroll-ready cutoff gates.
- **Parameters:** standard daily hours, weekly overtime threshold, break minutes,
  rounding interval, geofence radius, absence entitlement, approval threshold,
  exception age limit, premium multiplier, and payroll cutoff hour.
- **Configuration:** datastore backend, event topic, retry limit, default
  timezone, allowed clock sources, allowed absence types, workweek start,
  holiday calendar, labor precision, and workbench limits.

The runtime exposes operations to configure the package, set parameters,
register rules, and apply them during shift creation, clock events, absence
recording, overtime calculation, approval, and payroll-ready summary generation.
Configuration is intentionally narrow. `database_backend` must be one of
`postgresql`, `mysql`, or `mariadb`. `event_topic` must be
`appgen.time.events`. The configuration contract marks `event_contract` as
`AppGen-X`, hides the stream-engine picker, and disallows user-selectable
event transports. Any configuration field that attempts to expose stream
engine selection is rejected before runtime state is changed.

Schema evolution is also bounded. `register_schema_extension` may extend only
Time Labor owned tables and accepts only lower-case snake-case field names.
This gives regions, unions, device providers, and local labor agreements room
for extension without allowing a time package to mutate personnel, payroll,
warehouse, manufacturing, finance, or project tables.

## Standard Table-Stakes Capabilities

1. Shift creation with employee, role, date, planned start/end, site, cost
   center, job, and schedule status.
2. Shift pattern, shift assignment, schedule bid, and shift-swap request
   management.
3. Labor demand forecasts for site, date, required hours, and confidence.
4. Clock-in and clock-out events from kiosk, mobile, web, badge, or integration
   sources.
5. Clock-device registry, source routing, and self-healing route evidence.
6. Clock exception queues for missed punches, geofence breaks, and sequence
   gaps.
7. Geo-fence, source, and sequence validation for clock actions.
8. Time-entry calculation with rounded hours, break deduction, premium,
   exception flags, and audit evidence.
9. Time-entry lines for earning codes, rates, premiums, and adjustment
   evidence.
10. Overtime, double-time, holiday, shift differential, and premium
    calculation.
11. Absence recording, balance, entitlement check, approval status, and event
    emission.
12. Labor summary generation by employee, date, cost center, role, project, and
   payroll period.
13. Labor summary lines, cost allocation, and labor distribution.
14. Approval workflow and approval tasks for overtime, exceptions, absences,
   and payroll-ready
   hours.
15. Employee and role projection handling from personnel identity events.
16. Payroll, warehouse, manufacturing, project, and audit projections as local
    read models instead of shared tables.
17. Payroll-ready labor event emission with idempotency evidence.
18. Multi-tenant and multi-entity time isolation.
19. AppGen-X outbox/inbox, retry, dead-letter, and idempotent consumed-event
    handling.
20. Time policy screening, audit trace, hours-proof, and control assertion
    evidence.
21. Carbon schedule windows, schedule optimization, and shift-allocation
    records.
22. Labor risk models, risk forecasts, anomaly signals, parsed event evidence,
    governed-model metadata, seed data, and schema extensions.
23. Time workbench views for open shifts, exceptions, overtime, absences,
    approvals, and payroll-ready summaries.
24. Permissions and ABAC descriptors for schedule, clock, approve, absence,
    summarize, configure, and audit operations.
25. Configuration schema and seed data for clock sources, absence types,
    premium codes, approval levels, and default parameters.
26. Release-audit evidence for package ownership, manifests, schema, migrations,
    models, services, routes, events, handlers, UI, permissions, configuration,
    tests, registration metadata, and generation smoke.

## Generated Schema, Services, and Release Evidence

`build_schema_contract` emits table fields, relationships, migration artifact
paths under `pbcs/time_labor/migrations/`, generated model names, backend
allowlists, and `shared_table_access: false` for every owned table. The schema
contract covers scheduling, clocking, entries, breaks, overtime, premiums,
holidays, absence, summaries, labor costing, approvals, projections, policy
screening, audit, proof, federation, carbon scheduling, optimization,
allocation, anomaly, risk, parsed event, seed, extension, control, governed
model, rules, parameters, configuration, outbox, inbox, and dead-letter
evidence.

`build_service_contract` declares the transaction boundary as the Time Labor
owned datastore plus the AppGen-X outbox. Commands configure runtime state, set
parameters, register rules and schema extensions, receive events, maintain
employee projections, create shifts, record clock events, calculate entries,
record absences, approve labor summaries, route clock sources, generate hours
proofs, screen policies, federate labor views, verify employee identities, run
resilience drills, rotate crypto epochs, schedule carbon-aware shifts, optimize
schedules, allocate shifts, run controls, and register governed models. Query
methods cover workbench views, counterfactual schedule policy simulation,
overtime forecasting, semantic clock parsing, labor-risk scoring, anomaly
detection, stochastic labor exposure, and generated API/schema/release
contracts.

`build_release_evidence` combines schema, service, API, and permissions checks:
owned schema depth, per-table migration coverage, command depth, fixed
AppGen-X event contract, key command permission coverage, backend allowlist,
and no shared-table access. A release is valid only when every check passes and
`blocking_gaps` is empty.

## Event Handling and Projections

`receive_event` is the only package-local consumed-event handler. It accepts
`EmployeeCreated` and `RoleChanged` events through the AppGen-X inbox contract.
Each event is keyed by `idempotency_key` or by `event_type:event_id`, written to
the inbox evidence stream, and recorded in `handled_events` after successful
processing. Replays of processed events return a duplicate response and leave
state unchanged. `EmployeeCreated` maintains the employee projection used by
shift eligibility, clock validation, absence entitlement, and approval
workflows. `RoleChanged` updates the employee role projection and records a
role projection record for audit and workbench visibility.

Unsupported or failed consumed events never mutate domain facts. The handler
records retry evidence, increments attempts, and moves the event to
`time_labor_dead_letter_event` when the configured retry limit is reached.
Dead-letter records include event identity, tenant, attempt count, and reason.
This proves retry and dead-letter behavior without exposing an event-transport
picker to users.

## API, Permissions, and Workbench Contract

The package exposes descriptor-level routes rather than opaque strings. The API
contract maps `POST /shifts` to `create_shift`, `POST /clock-events` to
`record_clock_event`, `POST /time-entries/calculate` to
`calculate_time_entry`, `POST /absences` to `record_absence`,
`POST /labor-summaries/{id}/approve` to `approve_labor_summary`,
`POST /time/events/inbox` to `receive_event`, and read routes to the
workbench/query surface. Each descriptor declares owned tables touched,
emitted or consumed events, idempotency key, and required permission. The
contract also declares `shared_table_access: false`, the allowed database
backends, fixed AppGen-X eventing, emitted and consumed event types, and owned
tables.

Permissions are action-level descriptors:

- `time_labor.schedule` creates shifts.
- `time_labor.clock` records clock events.
- `time_labor.summarize` calculates time entries.
- `time_labor.absence` records absences.
- `time_labor.approve` approves labor summaries.
- `time_labor.event` receives consumed events.
- `time_labor.configure` changes rules, parameters, configuration, and schema
  extensions.
- `time_labor.audit` opens audit and workbench evidence.

The UI contract binds panels to owned tables, configuration, rules,
parameters, AppGen-X outbox/inbox/dead-letter evidence, and RBAC descriptors.
The workbench render includes visible and locked actions based on permissions,
owned-table binding evidence, outbox count, inbox count, dead-letter count, and
the fixed configuration metadata. Users can operate schedules, clock events,
absence review, approvals, rules, parameters, and configuration from the
workbench without selecting a stream engine or crossing package data
boundaries.

## Boundary Verification

`verify_owned_table_boundary` proves that generated or hand-authored Time Labor
artifacts reference only owned tables, package runtime tables, declared
consumed event types, declared API calls, declared projections, or
`time_labor_` implementation objects. Explicitly allowed dependencies include
personnel identity projections, payroll labor projections, warehouse site
projections, manufacturing shift projections, project cost projections, audit
ledger projections, `GET /employees`, `GET /roles`,
`POST /payroll-labor-hours`, and `POST /labor-cost-projections`. References to
foreign tables such as payroll runs, employee master, inventory tables, or
ledger tables are violations and must be represented through APIs, events, or
projections instead.

## Advanced Capabilities

1. Event-sourced labor lifecycle.
2. Graph-relational employee, shift, entry, absence, role, site, and approval
   topology.
3. Multi-tenant time isolation.
4. Schema-on-read time extensibility for region, union, project, and device
   attributes.
5. Probabilistic time fraud and exception scoring.
6. Real-time labor execution and analytics convergence.
7. Counterfactual schedule and overtime simulation.
8. Temporal labor demand and overtime forecasting.
9. Autonomous time exception resolution recommendations.
10. Semantic clock and absence event parsing.
11. Predictive burnout, absence, and compliance risk scoring.
12. Self-healing clock-source route selection.
13. Zero-knowledge payroll-ready hours proof.
14. Immutable labor audit trail.
15. Dynamic labor policy screening.
16. Automated time-control testing.
17. Universal API and async event contracts.
18. Cross-system labor federation with personnel, payroll, warehouse,
    manufacturing, project, and finance packages.
19. Workforce device integration evidence.
20. Decentralized employee time identity verification.
21. Chaos-engineered clock and approval tolerance.
22. Crypto-agile time authorization.
23. Carbon-aware schedule planning.
24. Algebraic schedule and labor optimization.
25. Mechanism-design shift allocation.
26. Information-theoretic time anomaly detection.
27. Stochastic labor exposure modeling.
28. Distributed systems engineering for idempotent handlers.
29. Probabilistic ML labor-risk governance.
30. Cryptographic engineering for proofs and hash chains.
31. Mathematical optimization for schedule, overtime, and staffing decisions.
32. Labor MLOps governance with feature lineage, drift, and explainability.

## Runtime Completeness Contract

The runtime must prove that rules, parameters, and configuration execute and
influence clock, absence, overtime, and approval decisions; that time-owned state
stays inside the package boundary; that AppGen-X outbox events are idempotent;
that backend configuration rejects anything outside PostgreSQL, MySQL, or
MariaDB; that eventing remains bound to the AppGen-X event contract without
user-facing stream-engine selection; that package-local UI fragments expose
shift planning, clock exceptions, absences, labor approvals, rule, parameter,
and configuration workbench surfaces; and that all standard and advanced
capability claims have testable release evidence.
