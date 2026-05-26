# Schema Registry And Contract Validation

Package-local implementation contract for the Schema Registry PBC. The package owns subject catalogs, schema versions, compatibility rules, consumer bindings, validation runs, contract violations, contract projections, AppGen-X event evidence, rules, parameters, configuration, UI fragments, and release validation for API, event, projection, document, and package contracts across an AppGen-X composition.

## Stable Identity

- PBC key: `schema_registry`.
- Mesh: platform fabric.
- Implementation directory: `src/pyAppGen/pbcs/schema_registry`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_schema_registry_runtime.py`.
- Event topic: `appgen.schema.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `schema_subject`
- `schema_subject_alias`
- `schema_namespace`
- `schema_version`
- `schema_field`
- `schema_fingerprint`
- `schema_semantic_tag`
- `schema_diff`
- `schema_evolution_plan`
- `compatibility_rule`
- `compatibility_matrix`
- `compatibility_exception`
- `consumer_binding`
- `consumer_impact`
- `producer_binding`
- `validation_run`
- `payload_validation_sample`
- `payload_validation_error`
- `contract_violation`
- `contract_remediation`
- `contract_projection`
- `gateway_contract_projection`
- `audit_contract_projection`
- `composition_contract_projection`
- `workflow_contract_projection`
- `route_contract_projection`
- `access_policy_projection`
- `package_registration_projection`
- `pbc_deployment_projection`
- `schema_acceptance_proof`
- `schema_policy_screening`
- `schema_federation_view`
- `schema_resilience_drill`
- `schema_crypto_epoch`
- `carbon_validation_window`
- `schema_diff_optimization`
- `consumer_review_allocation`
- `validation_anomaly_signal`
- `contract_exposure_forecast`
- `schema_identity_attestation`
- `schema_governed_model`
- `schema_seed_data`
- `schema_control_assertion`
- `schema_registry_extension`
- `schema_rule`
- `schema_parameter`
- `schema_configuration`
- `schema_registry_appgen_outbox_event`
- `schema_registry_appgen_inbox_event`
- `schema_registry_dead_letter_event`

The PBC does not share gateway, identity, audit, workflow, composition, package-index, producer, consumer, or business-domain tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed events: `PbcDeployed`, `EventContractProposed`, `RoutePublished`, `AccessPolicyChanged`, and `PackageRegistrationRequested`.
- API dependencies: `GET /gateway/routes`, `GET /identity/policies`, `POST /audit/contract-events`, and `POST /composition/contracts`.
- Projections and handoffs: `gateway_contract_projection`, `audit_contract_projection`, `composition_contract_projection`, `workflow_contract_projection`, `pbc_deployment_projection`, `route_contract_projection`, `access_policy_projection`, and `package_registration_projection`.
- Emitted events: `SchemaSubjectRegistered`, `SchemaAccepted`, `BreakingSchemaBlocked`, `PayloadValidated`, `ContractViolationRecorded`, and `ContractProjectionPublished`.

## Standard Capabilities

- Subject catalog for API, event, projection, document, package, command, and query contracts.
- Subject ownership by tenant, owner PBC, namespace, channel, format, lifecycle status, and tags.
- Schema versioning with semantic version, immutable fingerprint, version number, compatibility decision, and risk evidence.
- Backward, forward, full, transitive, additive-only, semantic, and policy-aware compatibility checks.
- Required-field, type, enum, range, semantic tag, PII classification, namespace, and payload-shape validation.
- Compatibility rules at global, tenant, subject, channel, consumer, and package-registration scope.
- Consumer bindings for APIs, handlers, projections, workflows, package consumers, release gates, and minimum versions.
- Impact analysis for producer/consumer compatibility and release blocking.
- Breaking-change blocking with risk scores, blocked decisions, and remediation hints.
- Payload validation for generated events, API requests, projection documents, and package metadata.
- Contract violation lifecycle with producer PBC, consumer PBC, severity, reason, status, SLA, and release-blocking evidence.
- Contract projection publishing for gateway, audit, composition, workflow, and package discovery.
- AppGen-X outbox/inbox idempotency, retry evidence, and dead-letter evidence.
- Multi-tenant contract isolation through tenant-scoped subjects, rules, parameters, configuration, and workbench views.
- RBAC descriptors for read, register, approve, validate, triage, publish, event, configuration, and audit actions.
- Package-local workbench UI for subjects, versions, compatibility, consumers, validation, violations, projections, rules, parameters, configuration, and event evidence.

## Advanced Capabilities

- Event-sourced schema lifecycle with immutable hash-chain audit trail.
- Graph-relational contract topology across subjects, versions, consumers, producers, payloads, violations, and projections.
- Multi-tenant contract isolation and schema-on-read owned-table extension.
- Probabilistic breaking-change, consumer-impact, payload, and governance risk scoring.
- Real-time contract analytics for version count, validation count, consumer bindings, violations, and release blockers.
- Counterfactual schema-evolution simulation.
- Temporal compatibility-health forecasting.
- Autonomous remediation recommendations for required-field removal, type changes, and consumer breaks.
- Semantic schema intent parsing for natural-language registration requests.
- Predictive contract risk scoring and self-healing validation route selection.
- Zero-knowledge schema acceptance proof generation.
- Dynamic contract policy screening by classification and active rule state.
- Automated controls for configuration, database, rules, versions, outbox, dead-letter, and hash-chain integrity.
- Universal descriptor API and AppGen-X event contracts.
- Cross-system schema federation through gateway, audit, composition, workflow, route, access policy, package, and deployment projections.
- Decentralized producer and consumer identity verification through DID-like evidence.
- Chaos-engineered contract validation tolerance and replay from the schema outbox.
- Quantum-resistant schema signing simulation through crypto-agile epoch rotation.
- Carbon-aware validation windows for heavy compatibility sweeps.
- Algebraic schema-diff minimization for breaking-change reduction.
- Mechanism-design consumer impact allocation for review capacity.
- Information-theoretic validation anomaly detection.
- Temporal contract exposure stochastic modeling.
- Governed contract-risk model registration with feature lineage, drift, and monitoring evidence.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X event topic, retry limit, allowed schema formats, default compatibility, namespace policy, timezone, workbench limit, and stream-picker absence.
- `set_parameter` accepts only supported schema registry parameters.
- `register_rule` validates rule identity, tenant, scope, mode, classification, severity, and status.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles PBC deployment, event-contract proposal, route publication, access-policy, and package-registration events; records inbox evidence; schedules retries; and dead-letters exhausted failures.
- `register_subject` owns subject catalog state and emits subject registration evidence.
- `define_compatibility_rule` owns compatibility policy state.
- `register_consumer_binding` owns consumer dependency state without sharing consumer tables.
- `submit_schema_version` owns schema version state, fingerprints, compatibility decisioning, accepted events, and blocked-change events.
- `run_compatibility_check` owns validation-run state for proposed schemas.
- `validate_payload` owns payload validation runs and emits payload validation evidence.
- `record_contract_violation` owns violation state and release-blocking evidence.
- `publish_contract_projection` owns projection state and downstream handoffs.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, dependency, and owned-table evidence.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /schemas/subjects` maps to `register_subject`.
- `POST /schemas/versions` maps to `submit_schema_version`.
- `POST /schemas/compatibility-rules` maps to `define_compatibility_rule`.
- `POST /schemas/consumer-bindings` maps to `register_consumer_binding`.
- `POST /schemas/compatibility-checks` maps to `run_compatibility_check`.
- `POST /schemas/payload-validations` maps to `validate_payload`.
- `POST /schemas/violations` maps to `record_contract_violation`.
- `POST /schemas/projections` maps to `publish_contract_projection`.
- `POST /schemas/events/inbox` maps to `receive_event`.
- `GET /schemas/subjects` maps to `build_workbench_view`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, fixed AppGen-X eventing evidence, and dependency evidence.

## Events And Handlers

Emitted events:

- `SchemaSubjectRegistered`
- `SchemaAccepted`
- `BreakingSchemaBlocked`
- `PayloadValidated`
- `ContractViolationRecorded`
- `ContractProjectionPublished`

Consumed events:

- `PbcDeployed`
- `EventContractProposed`
- `RoutePublished`
- `AccessPolicyChanged`
- `PackageRegistrationRequested`

Handlers are idempotent by idempotency key or event type and event id. Duplicate processed events do not create duplicate state changes. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules cover compatibility, classification, payload validation, consumer impact, projection publication, release gates, namespace policy, schema format, default compatibility, severity, and status.

Parameters include:

- `compatibility_threshold`
- `max_schema_fields`
- `semantic_similarity_floor`
- `violation_risk_threshold`
- `review_sla_hours`
- `retention_days`
- `breaking_change_weight`
- `consumer_impact_weight`
- `payload_validation_sample_rate`
- `workbench_limit`

Configuration includes database backend, event topic, retry limit, allowed formats, default compatibility mode, namespace policy, default timezone, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, allowed relational backends, hidden stream-engine picker evidence, non-selectable event-contract evidence, and owned tables.

## UI And Workbench

UI fragments:

- `SchemaRegistryWorkbench`
- `SubjectCatalog`
- `SchemaVersionEditor`
- `CompatibilityStudio`
- `ConsumerImpactMap`
- `PayloadValidationConsole`
- `ContractViolationBoard`
- `ContractProjectionPublisher`
- `SchemaAuditEvidenceView`
- `SchemaRuleStudio`
- `SchemaParameterConsole`
- `SchemaConfigurationPanel`

The workbench exposes subject, version, validation, violation, consumer-binding, release-blocking, inbox, outbox, dead-letter, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by read, register, approve, validate, triage, publish, event, configuration, and audit permissions.

## Generated Schema, Services, And Release Evidence

`schema_registry_build_schema_contract` emits generation-ready descriptors for every owned table, including table fields, relationships, migration paths under `pbcs/schema_registry/migrations/{sequence}_{table}.sql`, model descriptors under `pbcs/schema_registry/models/{table}.py`, backend allowlist evidence, and `shared_table_access: False`.

`schema_registry_build_service_contract` publishes the command and query surface used by generated applications: runtime configuration, parameters, rules, owned schema extensions, AppGen-X inbox intake, subject registration, compatibility rules, consumer binding, schema submission, compatibility checks, payload validation, violation recording, contract projection publication, route failover, selective proof generation, policy screening, federation, identity checks, resilience drills, crypto epoch rotation, carbon-aware validation, schema diff optimization, consumer impact allocation, control testing, governed model registration, and boundary verification.

`schema_registry_build_release_evidence` is the package-local release gate. It proves owned schema depth, one migration descriptor per owned table, service command depth, AppGen-X-only API/eventing, permission coverage for core commands, backend allowlist compliance, and no shared table access.

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, fixed AppGen-X eventing, descriptor APIs, and action-level RBAC.
- Configuration, parameters, rules, schema extensions, event handling, subject registration, compatibility rules, consumer binding, schema versions, compatibility checks, payload validation, violations, projections, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, stream-picker configuration, unsupported parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.

<!-- APPGEN-X:PBC-MANIFEST-TRACEABILITY:START -->

## Manifest Traceability Appendix

This appendix is generated from the package manifest and is release-gated so the specification stays aligned with the implemented PBC surface.

- PBC key: `schema_registry`
- Mesh: `platform`
- Datastore backend: `None`

### Owned Tables

- `schema_subject`
- `schema_version`
- `compatibility_rule`
- `contract_violation`

### API Routes

- `POST /schemas`
- `POST /compatibility-checks`
- `GET /subjects`

### Emitted Events

- `SchemaAccepted`
- `BreakingSchemaBlocked`

### Consumed Events

- `PbcDeployed`
- `EventContractProposed`

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
