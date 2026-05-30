# Sustainability ESG Reporting PBC

## Purpose

`sustainability_esg_reporting` is a standalone AppGen-X packaged business capability for sustainability and ESG reporting. It owns ESG metric definitions, double materiality, facility and activity data, emissions factors, Scope 1/2/3 calculations, renewable instruments, water and waste metrics, social and governance metrics, supplier ESG inputs, assurance controls and audit evidence, restatements, targets, climate scenarios, board packs, regulator filings, and governed AI document or instruction previews.

The package is deliberately implemented as a real one-PBC functional slice rather than a thin catalog stub. It exposes executable runtime contracts, owned schema and migrations, services, routes, eventing, UI workbench surfaces, governed AI previews, release audits, and focused tests.

## Owned Boundary

The package owns the following operational tables under the `sustainability_esg_reporting_` prefix:

- `esg_metric`
- `materiality_assessment`
- `reporting_framework_mapping`
- `facility_profile`
- `activity_data_record`
- `emissions_factor`
- `emissions_calculation`
- `scope_boundary`
- `renewable_instrument`
- `water_metric_record`
- `waste_metric_record`
- `social_metric_record`
- `governance_metric_record`
- `supplier_esg_input`
- `assurance_control`
- `assurance_evidence`
- `assurance_exception`
- `restatement_record`
- `sustainability_target`
- `target_progress`
- `climate_scenario`
- `data_quality_check`
- `disclosure_packet`
- `board_pack`
- `regulator_filing`
- `governed_document`
- `governed_instruction`
- `policy_rule`
- `runtime_parameter`
- `schema_extension`
- `control_assertion`
- `governed_model`
- `appgen_outbox_event`
- `appgen_inbox_event`
- `appgen_dead_letter_event`

No operation mutates foreign tables. Cross-PBC integration is limited to API dependencies, read-only projections, or consumed AppGen-X events.

## Database and Event Contract

- Database backends: PostgreSQL, MySQL, and MariaDB only.
- Event contract: AppGen-X only.
- Stream engine picker: not surfaced anywhere in runtime, configuration, routes, UI, or agent flows.
- Event transport: package-local outbox, inbox, and dead-letter tables with idempotent handlers and retry metadata.

## Core Domain Operations

The slice exposes executable operations for:

- defining ESG metrics
- approving materiality assessments
- registering facilities
- capturing activity data
- registering emissions factors
- calculating Scope 1/2/3 emissions
- recording renewable instruments
- recording water, waste, social, and governance metrics
- ingesting supplier ESG inputs
- defining scope boundaries
- creating targets and measuring target progress
- mapping reporting frameworks
- building disclosure packets
- attaching assurance evidence and running controls
- opening assurance exceptions
- recording restatements
- simulating climate scenarios
- preparing board packs
- filing regulator submissions
- compiling ESG rules
- previewing governed AI document and instruction changes

## Rules and Parameters

Rules are first-class executable artifacts:

- `materiality_policy`
- `emissions_factor_policy`
- `scope_boundary_policy`
- `renewable_claim_policy`
- `assurance_policy`
- `target_tracking_policy`
- `disclosure_policy`
- `data_quality_policy`

Bounded runtime parameters are exposed in configuration, controls, UI, and agent guidance:

- `quality_score_floor`
- `target_warning_percent`
- `factor_expiry_days`
- `assurance_sample_rate`
- `materiality_threshold`
- `workbench_limit`
- `certificate_vintage_window_days`
- `scenario_shock_limit`

## UI and Workbench

The workbench includes forms, wizards, and controls for:

- metric and materiality intake
- facility and activity capture
- emissions and renewable claim workflows
- water, waste, social, and governance metric review
- supplier ESG review
- assurance evidence and control testing
- restatement triage
- disclosure packet assembly
- board packs and regulator filings
- governed AI preview-only document and instruction flows

## Agent and Governed AI

The package contributes `sustainability_esg_reporting_skills` to the composed assistant. The agent can:

- explain domain tasks and workbench actions
- propose document and instruction change plans
- preview CRUD mutations against owned tables only
- require human confirmation for mutations
- refuse foreign-table writes
- keep AppGen-X event planning explicit

## Release and Audit Requirements

Release readiness requires the following focused audits to pass:

- source audit
- package audit
- spec audit
- agent audit
- implementation audit
- capability audit
- generation smoke audit

Focused tests assert:

- owned-table depth is at least 24 runtime tables
- domain operations are at least 20
- forms, wizards, and controls are all present
- AppGen-X is the only event contract
- stream engine picker visibility stays false
- board packs, regulator filings, Scope 1/2/3 calculations, renewable governance, water/waste/social/governance metrics, and governed AI previews are executable surfaces
