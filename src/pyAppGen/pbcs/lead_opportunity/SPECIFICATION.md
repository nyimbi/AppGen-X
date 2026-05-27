# Lead Opportunity PBC

`lead_opportunity` is the AppGen-X packaged business capability for revenue
pipeline intake, lead scoring, qualification, account hierarchy management,
opportunity execution, sales activity evidence, revenue forecasting, and
customer-update publication. It is a complete package-local implementation with
owned schema, runtime services, API descriptors, AppGen-X events, idempotent
handlers, rules, parameters, configuration, UI fragments, package metadata,
tests, and release evidence.

## Stable Identity

- PBC key: `lead_opportunity`.
- Mesh: relationship.
- Package directory: `src/pyAppGen/pbcs/lead_opportunity`.
- Runtime entrypoint: `lead_opportunity_runtime_capabilities()`.
- UI entrypoint: `lead_opportunity_ui_contract()`.
- Source registration entrypoint: `implementation_contract()`.
- Allowed database backends: PostgreSQL, MySQL, and MariaDB.
- Eventing standard: fixed AppGen-X event contract on
  `appgen.lead_opportunity.events`.
- User-facing stream-engine selector: forbidden and hidden.

## Owned Datastore Boundary

The package owns exactly these operational tables:

- `lead`: tenant, account, customer, contact data, source, region, currency,
  engagement score, estimated value, qualification score, assigned owner,
  status, and audit proof.
- `lead_enrichment_snapshot`, `lead_dedup_case`, `lead_score_snapshot`, and
  `lead_assignment`: enrichment, duplicate review, scoring, assignment, and
  qualification evidence for captured leads.
- `qualification_decision`: deterministic threshold, score, and decision
  evidence for lead qualification.
- `opportunity`: tenant, lead, account, name, amount, currency, stage, close
  date, win probability, forecast amount, risk score, status, and audit proof.
- `opportunity_stage_history`, `pipeline_forecast_snapshot`,
  `quote_proposal_handoff`, and `opportunity_outcome`: stage transitions,
  forecast rollups, quote/proposal handoffs, and win/loss evidence.
- `account_hierarchy`: tenant, account identity, parent account, customer
  projection key, region, owner, status, and audit proof.
- `sales_activity`: tenant, opportunity, activity type, subject, sentiment,
  timestamp, owner, next-best action, and immutable activity proof.
- `sales_coaching_insight`, `lead_opportunity_audit_event`,
  `lead_opportunity_rule`, `lead_opportunity_parameter`,
  `lead_opportunity_configuration`, `lead_opportunity_governed_model`, and
  `lead_opportunity_seed_data`: coaching, audit, governance, configuration,
  parameter, rule, and seed-data evidence owned by the package.

No customer, segment, billing, territory, marketing, product, or finance tables
are shared or directly accessed. External context arrives through declared
AppGen-X events and API projections only:

- Consumed event: `CustomerSegmentUpdated`.
- API projections: `customer_segment_projection`, `customer_projection`,
  `billing_projection`, and `territory_projection`.
- Runtime event tables are PBC-local:
  `lead_opportunity_appgen_outbox_event`,
  `lead_opportunity_appgen_inbox_event`, and
  `lead_opportunity_dead_letter_event`.

The boundary verifier accepts only owned tables, declared APIs/events,
declared projections, and PBC-local event tables. It rejects direct foreign
references such as `customer`.

## Standard Table-Stakes Capabilities

The implementation covers the ordinary revenue-pipeline capabilities expected
from a production relationship package:

- Account hierarchy creation with parent-child account structure, owner,
  customer projection key, region validation, status, and audit proof.
- Lead capture with source, contact, region, currency, engagement, estimated
  value, duplicate detection by tenant/email, assignment owner, and score.
- Executable lead enrichment snapshots, dedupe case resolution, score
  snapshots, owner assignment records, and qualification-decision evidence.
- Runtime configuration for database backend, event topic, retry limit,
  default currency, supported currencies, supported regions, pipeline stages,
  timezone, assignment mode, and workbench limit.
- Parameter engine for qualification threshold, win probability threshold,
  stale activity days, forecast confidence floor, deal slippage threshold, lead
  source weight, segment fit weight, engagement weight, max open opportunities,
  and workbench limit.
- Rule engine for tenant, scope, allowed regions, allowed currencies, allowed
  segments, qualification policy, assignment policy, status, compiled hash, and
  policy-engine evidence.
- Schema extension for owned revenue tables only, with versioned migration
  evidence.
- Idempotent AppGen-X handler for `CustomerSegmentUpdated`.
- Lead qualification that compares scored leads to configured thresholds and
  emits `LeadQualified` when accepted.
- Opportunity creation from qualified leads with stage validation, open
  opportunity limits, win probability, forecast amount, and slippage risk.
- Opportunity stage history, forecast snapshots, quote/proposal handoff
  execution, win/loss outcome evidence, audit events, and coaching insight
  generation.
- Sales activity timeline with sentiment, owner, timestamp, next-best action,
  and activity proof.
- Opportunity stage advancement and won-opportunity capture.
- `OpportunityWon` and `CustomerUpdated` AppGen-X outbox emissions.
- Retry/dead-letter evidence for failed consumed-event handling.
- Workbench views for leads, qualified leads, opportunities, won deals,
  accounts, activities, pipeline value, forecast amount, rules, parameters,
  configuration, outbox, and dead letters.
- UI fragments for lead inbox, account hierarchy map, qualification board,
  opportunity pipeline, sales activity timeline, forecast rollup,
  next-best-action panel, customer segment projection, rule studio, parameter
  console, configuration, outbox, and dead letters.
- Permission/RBAC descriptors for lead, opportunity, activity, event,
  configuration, and audit actions.
- Seed data for lead sources and pipeline stages.

## Advanced Capabilities

The executable runtime proves the advanced capabilities needed for a modern
revenue PBC:

- Event-sourced revenue lifecycle with immutable state-event hashes.
- Owned revenue schema boundary enforcement with explicit violation evidence.
- Multi-tenant pipeline isolation across leads, opportunities, accounts,
  activities, and UI views.
- Schema-evolution-safe opportunity extensions.
- Probabilistic win likelihood, deal slippage, and forecast confidence
  evidence.
- Counterfactual deal-velocity support through deterministic scoring,
  probability, and forecast recomputation.
- Temporal pipeline forecasting through stage, close-date, stale-activity, and
  forecast parameters.
- Autonomous next-best-action generation from activity sentiment and type.
- Semantic interaction understanding evidence through activity subject,
  sentiment, and next-best action.
- Dynamic sales policy screening through compiled rules and parameters.
- Automated revenue control testing via smoke checks and release audits.
- Self-healing assignment evidence through rule-driven default owners.
- Cryptographic pipeline proofs for accounts, leads, opportunities,
  activities, and outbox events.
- Immutable pipeline audit trail.
- Cross-system customer, segment, billing, and territory federation through
  declared APIs/events only.
- AppGen-X outbox/inbox eventing with idempotent handlers.
- Retry/dead-letter evidence.
- Permissions governance evidence.
- Configuration, rule, parameter, seed-data, and workbench evidence.
- Governed model evidence through schema extensions and scoring parameters.

## Commands And Services

The service layer exposes these package-local commands:

- `configure_runtime(configuration)`.
- `set_parameter(name, value)`.
- `register_rule(rule)`.
- `register_schema_extension(table, fields)`.
- `receive_event(event, simulate_failure=False)`.
- `create_account_hierarchy(command)`.
- `create_lead(command)`.
- `enrich_lead(lead_id, enrichment)`.
- `qualify_lead(lead_id)`.
- `create_opportunity(command)`.
- `record_sales_activity(command)`.
- `advance_opportunity(opportunity_id, stage)`.
- `create_quote_proposal_handoff(command)`.
- `win_opportunity(opportunity_id)`.
- `lose_opportunity(command)`.
- `build_api_contract()`.
- `build_schema_contract()`.
- `build_service_contract()`.
- `build_release_evidence()`.
- `permissions_contract()`.
- `build_workbench_view(tenant=...)`.
- `verify_owned_table_boundary(references=...)`.

All commands are deterministic and side-effect-free: they accept explicit state
and return new state plus evidence payloads suitable for generated apps and
release smoke audits.

## APIs

The package-local API contract exposes route descriptors:

- `POST /accounts` runs `create_account_hierarchy`, writes
  `account_hierarchy`, requires `lead_opportunity.lead.write`, and is
  idempotent by `account_id`.
- `POST /leads` runs `create_lead`, writes `lead`, requires
  `lead_opportunity.lead.write`, and is idempotent by `lead_id`.
- `POST /lead-qualifications` runs `qualify_lead`, updates `lead`, requires
  `lead_opportunity.lead.write`, emits `LeadQualified`, and is idempotent by
  `lead_id`.
- `POST /opportunities` runs `create_opportunity`, writes `opportunity`,
  requires `lead_opportunity.opportunity.write`, and is idempotent by
  `opportunity_id`.
- `POST /sales-activities` runs `record_sales_activity`, writes
  `sales_activity`, requires `lead_opportunity.activity.write`, and is
  idempotent by `activity_id`.
- `POST /opportunity-stage` runs `advance_opportunity`, updates
  `opportunity`, requires `lead_opportunity.opportunity.write`, and is
  idempotent by `opportunity_id:stage`.
- `POST /quote-proposal-handoffs` runs `create_quote_proposal_handoff`, writes
  `quote_proposal_handoff`, emits `QuoteProposalRequested`, requires
  `lead_opportunity.opportunity.write`, and is idempotent by `handoff_id`.
- `POST /opportunity-wins` runs `win_opportunity`, updates `opportunity`,
  requires `lead_opportunity.opportunity.write`, emits `OpportunityWon` and
  `CustomerUpdated`, and is idempotent by `opportunity_id`.
- `POST /opportunity-losses` runs `lose_opportunity`, writes
  `opportunity_outcome` and `pipeline_forecast_snapshot`, emits
  `OpportunityLost`, requires `lead_opportunity.opportunity.write`, and is
  idempotent by `opportunity_id:reason`.
- `POST /lead-opportunity/events/inbox` runs `receive_event`, consumes
  declared AppGen-X events, requires `lead_opportunity.event.consume`, and is
  idempotent by `event_id`.
- `GET /pipeline` queries `build_workbench_view`, reads only owned Lead
  Opportunity state, and requires `lead_opportunity.audit`.
- `GET /lead-opportunity/schema-contract` queries
  `build_schema_contract`, reads only owned metadata, and requires
  `lead_opportunity.audit`.
- `GET /lead-opportunity/service-contract` queries
  `build_service_contract`, reads only owned metadata, and requires
  `lead_opportunity.audit`.
- `GET /lead-opportunity/release-evidence` queries
  `build_release_evidence`, reads only owned metadata/evidence, and requires
  `lead_opportunity.audit`.

The catalog-facing route set remains `POST /leads`, `POST /opportunities`, and
`GET /pipeline`.

## Events And Handlers

Consumed event:

- `CustomerSegmentUpdated`.

Emitted events:

- `LeadQualified`.
- `OpportunityWon`.
- `OpportunityLost`.
- `CustomerUpdated`.
- `QuoteProposalRequested`.

Handlers require event IDs, deduplicate already handled events, record inbox
evidence, store customer-segment projections in package-local state, and send
simulated failures to the dead-letter evidence queue. Users never choose a
stream engine.

## UI And Workbench

The UI contract exposes:

- Lead inbox.
- Lead enrichment board.
- Dedupe resolution queue.
- Qualification decision ledger.
- Account hierarchy map.
- Qualification board.
- Opportunity pipeline.
- Sales activity timeline.
- Forecast rollup.
- Quote proposal handoff panel.
- Win/loss outcome board.
- Sales coaching panel.
- Next-best-action panel.
- Customer segment projection panel.
- Revenue rule studio.
- Revenue parameter console.
- Revenue configuration panel.
- Revenue event outbox.
- Revenue dead-letter queue.

Rendered workbench output includes tenant-filtered lead, qualified-lead,
opportunity, won-deal, account, activity, forecast amount, inbox, outbox, and
dead-letter counts; visible and locked actions from RBAC permissions;
configuration/rule/parameter state; runtime-table bindings; and owned-table
binding evidence.

## Release Evidence

Focused tests prove:

- Runtime capability and smoke checks cover every advanced capability key.
- Configuration, rule, parameter, schema-extension, customer-segment event
  handling, account hierarchy, lead capture, qualification, opportunity
  creation, sales activity, stage advancement, win capture, outbox emission, UI
  rendering, API descriptors, RBAC descriptors, and workbench evidence execute.
- AppGen-X eventing is fixed and stream-engine picker exposure is false.
- Backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Boundary validation accepts owned tables and declared dependencies and
  rejects direct foreign table references.
- Invalid database backends, invalid parameters, non-owned schema extensions,
  and simulated handler failures are rejected or dead-lettered.
- `implementation_contract()` exposes package-local schema, service, release,
  permissions, event-topic, emitted/consumed-event, runtime-table, and
  boundary evidence without relying on shared-file edits.
- The package participates in all-PBC implementation release and generation
  smoke audits.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `lead_opportunity`
- Mesh: `relationship`
- Datastore backend: `None`

### Owned Tables

- `lead`
- `opportunity`
- `account_hierarchy`
- `sales_activity`

### API Routes

- `POST /leads`
- `POST /opportunities`
- `GET /pipeline`

### Emitted Events

- `OpportunityWon`
- `CustomerUpdated`

### Consumed Events

- `CustomerSegmentUpdated`

### UI Fragments

- None declared

### Permissions

- None declared

### Configuration Keys

- None declared

### Standard Features

- None declared

### Advanced Capabilities

- None declared

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:END -->

## Agent, Chatbot Skills, And Self-Registration Contract

The `lead_opportunity` package exposes a first-class PBC agent and chatbot interface through `agent.py`. The composed application imports these capabilities under the `lead_opportunity_skills` namespace so a single application assistant can route help, task guidance, document instruction intake, governed datastore CRUD planning, workbench navigation, and policy explanation back to the owning PBC instead of inventing cross-package mutations. The agent contract is scoped to the `Enterprise Lead and Opportunity Management` boundary and must name the command, permission, owned tables, idempotency key, expected AppGen-X event, and human confirmation requirement before any create, update, or delete plan is eligible to execute.

Document and instruction intake is explicit release evidence. The chatbot can accept uploaded documents, operational notes, or user instructions, extract candidate facts for owned tables such as `lead_opportunity_lead`, `lead_opportunity_opportunity`, `lead_opportunity_account_hierarchy`, `lead_opportunity_sales_activity`, validate those facts against package rules, parameters, configuration, and permissions, and return a side-effect-free mutation preview. The preview is not a write. It is a governed plan that references service operations such as , uses AppGen-X event expectations such as `OpportunityWon`, `CustomerUpdated`, rejects foreign tables, and records whether a read-only query or a confirmed command is required. This keeps AI assistance professional, auditable, and bounded to the PBC datastore.

Self-registration is also part of the specification. `registration_plan()`, `package_metadata_manifest()`, `validate_package_metadata()`, and `package_discovery_plan()` must produce a side-effect-free discovery and registration plan for `lead_opportunity`. Registration metadata identifies the source package directory, required artifacts, owned datastore, AppGen-X event contract, UI fragments, RBAC descriptors, configuration schema, seed data, tests, and release evidence without mutating the global catalog during discovery. Composition tooling may then register the PBC, merge the `lead_opportunity_skills` contribution into the single composed assistant, and expose the workbench UI while preserving owned-table boundaries and declared API/event/projection dependencies.

