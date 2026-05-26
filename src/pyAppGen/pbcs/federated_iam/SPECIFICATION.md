# Federated Identity and Access Management

Package-local implementation contract for the Federated IAM PBC. The package owns tenant identity, principal registry, provider federation, credential verification, role and policy control, token/session grants, privileged access, AppGen-X event evidence, rules, parameters, configuration, UI fragments, and release validation for platform-wide identity and authorization.

## Stable Identity

- PBC key: `federated_iam`.
- Mesh: platform fabric.
- Implementation directory: `src/pyAppGen/pbcs/federated_iam`.
- Runtime module: `runtime.py`.
- UI module: `ui.py`.
- Test module: `tests/test_pbc_federated_iam_runtime.py`.
- Event topic: `appgen.identity.events`.
- Event contract: AppGen-X.
- Supported relational backends: PostgreSQL, MySQL, and MariaDB.
- User-facing stream-engine selection is not exposed.

## Owned Boundary

Owned tables and generated model artifacts:

- `tenant`
- `principal`
- `identity_provider`
- `principal_identity`
- `role_assignment`
- `access_policy`
- `policy_decision`
- `token_grant`
- `session`
- `credential_verification`
- `privileged_access_request`
- `iam_rule`
- `iam_parameter`
- `iam_configuration`
- `federated_iam_appgen_outbox_event`
- `federated_iam_appgen_inbox_event`
- `federated_iam_dead_letter_event`

The PBC does not share customer, workforce, service-account, gateway, schema registry, audit, or business-domain tables. Cross-PBC integration is represented only by declared APIs, events, or projections:

- Consumed events: `RoleChanged`, `TenantLifecycleChanged`, `CustomerUpdated`, `EmployeeProvisioned`, and `ServiceAccountRequested`.
- API dependencies: `GET /schemas/identity-events`, `POST /audit/access-events`, and `POST /gateway/token-projections`.
- Projections and handoffs: `gateway_token_projection`, `audit_access_projection`, `principal_session_projection`, `tenant_lifecycle_projection`, `customer_identity_projection`, `employee_identity_projection`, and `service_account_request_projection`.
- Emitted events: `TenantProvisioned`, `PrincipalVerified`, `AccessPolicyChanged`, `PolicyDecisionRecorded`, `TokenGranted`, and `PrivilegedAccessApproved`.

## Standard Capabilities

- Tenant registry with lifecycle, region, compliance boundary, isolation, and active/blocked status.
- Principal registry for users, service accounts, devices, external workforce identities, customer identities, and agents.
- Identity-provider registry for OIDC, SAML, SCIM, DID/verifiable credential issuers, passkeys, and device-trust sources.
- Federated identity linking with claim mapping, subject binding, trust scores, and required-claim enforcement.
- Credential verification with issuer validation, confidence scoring, and credential-status evidence.
- Role assignments with scoped resources, allowed-role policy, status, and active role analytics.
- RBAC, ABAC, relationship policy, deny override, segregation-of-duties, and dynamic policy decisioning.
- Token grants with grant-type validation, audience, scopes, TTL, token hash evidence, and gateway/audit/session handoffs.
- Session governance, revocation route descriptors, step-up thresholds, and risk-based grant controls.
- Privileged access approval with risk gating, TTL, approver evidence, and break-glass audit trail.
- AppGen-X outbox/inbox idempotency, retry evidence, and dead-letter evidence.
- Tenant, role, customer, employee, and service-account projections from declared AppGen-X events.
- Identity and access analytics for principals, providers, identities, roles, decisions, tokens, and privileged access.
- Multi-tenant isolation through tenant-scoped state, configuration, rules, parameters, and workbench views.
- RBAC descriptors for tenant, principal, policy, token, privileged access, event, configuration, and audit actions.
- Package-local workbench UI for tenant registry, principal registry, providers, credentials, roles, policy decisions, tokens, privileged access, audit, rules, parameters, configuration, and event evidence.

## Advanced Capabilities

- Event-sourced identity lifecycle with immutable hash-chain audit trail.
- Graph-relational trust topology across tenants, principals, providers, identities, credentials, roles, policies, sessions, tokens, and privileged access.
- Multi-tenant access isolation and owned-table schema evolution.
- Probabilistic identity, session, policy, and privilege risk scoring.
- Real-time access analytics across policy decisions, token grants, privileged access, and event streams.
- Counterfactual policy simulation and privilege-delta analysis.
- Temporal access-risk and exposure forecasting.
- Autonomous identity exception resolution for stale roles, risky sessions, and provider outages.
- Semantic access request parsing for operational and agent-driven workflows.
- Predictive access risk scoring and self-healing authorization route selection.
- Zero-knowledge policy-decision proof generation.
- Dynamic access-policy screening by restricted action and decision state.
- Automated controls for configuration, rules, parameters, privileged-access review, and hash-chain integrity.
- Universal descriptor API and AppGen-X event contracts.
- Cross-system identity federation through workforce, customer, service-account, gateway, session, and audit projections.
- Decentralized principal identity verification through DID-like evidence.
- Chaos-engineered identity tolerance for policy API and provider discovery failures.
- Quantum-resistant token authorization simulation through crypto-agile epoch rotation.
- Carbon-aware access processing windows.
- Algebraic least-privilege role optimization.
- Mechanism-design privileged-access allocation.
- Information-theoretic access anomaly detection.
- Temporal access exposure stochastic modeling.
- Governed identity-risk model registration with feature lineage, drift, and explainability controls.

## Runtime Services

- `configure_runtime` validates backend, exact AppGen-X event topic, retry limit, regions, provider types, principal types, grant types, timezone, workbench limit, and stream-picker absence.
- `set_parameter` accepts only supported identity and access parameters.
- `register_rule` validates rule identity, tenant, status, and access scope, then stores deterministic compiled evidence.
- `register_schema_extension` accepts only owned-table schema extensions.
- `receive_event` idempotently handles role, tenant lifecycle, customer, employee, and service-account events; records inbox evidence; schedules retries; and dead-letters exhausted failures.
- `provision_tenant` owns tenant lifecycle state and emits tenant provisioning evidence.
- `register_principal` owns principal state and graph topology evidence.
- `register_identity_provider` owns provider registry state.
- `link_identity` owns federated identity state, claim compliance, and trust-score enforcement.
- `verify_credential` owns credential verification state and issuer/confidence checks.
- `assign_role` owns role assignment and access policy change evidence.
- `evaluate_policy` owns policy decisions, deny override, risk scoring, and decision events.
- `grant_token` owns token grants, token hashes, TTL, and gateway/audit/session handoffs.
- `approve_privileged_access` owns privileged access state, risk thresholding, TTL, and approval evidence.
- `build_api_contract` emits descriptor-level route, permission, idempotency, event, dependency, and owned-table evidence.
- `build_schema_contract` emits package-local owned-table, runtime-table, migration, relationship, and backend evidence.
- `build_service_contract` emits command/query boundaries, AppGen-X eventing rules, rules/parameters/configuration support, idempotent handler evidence, and no-shared-table dependencies.
- `build_release_evidence` emits package-local release checks for schema depth, runtime-table evidence, AppGen-X-only eventing, backend allowlist, permissions, UI/workbench bindings, and owned-boundary validation.
- `permissions_contract` maps runtime commands to RBAC permissions.
- `verify_owned_table_boundary` accepts owned tables and declared API/event/projection dependencies, then reports direct foreign-table violations.
- `build_workbench_view` exposes operational and release evidence.

## API Contract

- `POST /tenants` maps to `provision_tenant`.
- `POST /principals` maps to `register_principal`.
- `POST /identity-providers` maps to `register_identity_provider`.
- `POST /identity-links` maps to `link_identity`.
- `POST /credential-verifications` maps to `verify_credential`.
- `POST /role-assignments` maps to `assign_role`.
- `POST /policy-decisions` maps to `evaluate_policy`.
- `POST /token-grants` maps to `grant_token`.
- `POST /privileged-access-requests` maps to `approve_privileged_access`.
- `PUT /iam/configuration` maps to `configure_runtime`.
- `POST /iam/parameters` maps to `set_parameter`.
- `POST /iam/rules` maps to `register_rule`.
- `POST /iam/events/inbox` maps to `receive_event`.
- `GET /iam-workbench` maps to `build_workbench_view`.
- `GET /iam/schema-contract` maps to `build_schema_contract`.
- `GET /iam/service-contract` maps to `build_service_contract`.
- `GET /iam/release-evidence` maps to `build_release_evidence`.

Every route descriptor includes owned tables, command or query binding, idempotency key where applicable, required permission, emitted events, consumed events, fixed AppGen-X eventing evidence, and dependency evidence.

## Events And Handlers

Emitted events:

- `TenantProvisioned`
- `PrincipalVerified`
- `AccessPolicyChanged`
- `PolicyDecisionRecorded`
- `TokenGranted`
- `PrivilegedAccessApproved`

Consumed events:

- `RoleChanged`
- `TenantLifecycleChanged`
- `CustomerUpdated`
- `EmployeeProvisioned`
- `ServiceAccountRequested`

Handlers are idempotent by idempotency key or event type and event id. Duplicate processed events do not create duplicate state changes. Failed events record retry evidence until the configured retry limit and then produce dead-letter records.

## Rules, Parameters, And Configuration

Rules cover access policy, tenant boundaries, identity-provider eligibility, required claims, allowed regions, allowed roles, denied actions, privileged actions, segregation-of-duties checks, session controls, token policy, revocation policy, and status.

Parameters include:

- `minimum_trust_score`
- `session_risk_threshold`
- `token_ttl_minutes`
- `privileged_access_ttl_minutes`
- `step_up_threshold`
- `retention_days`
- `maximum_failed_policy_checks`
- `privileged_access_approval_count`
- `credential_confidence_threshold`
- `workbench_limit`

Configuration includes database backend, event topic, retry limit, allowed regions, allowed provider types, allowed principal types, allowed grant types, default timezone, and workbench limit. Runtime configuration records `event_contract: AppGen-X`, allowed relational backends, hidden stream-engine picker evidence, non-selectable event-contract evidence, and owned tables.

## UI And Workbench

UI fragments:

- `FederatedIamWorkbench`
- `TenantRegistry`
- `PrincipalRegistry`
- `IdentityProviderConsole`
- `CredentialVerificationPanel`
- `RoleAssignmentBoard`
- `PolicyDecisionWorkbench`
- `TokenGrantConsole`
- `PrivilegedAccessReview`
- `IdentityAuditDashboard`
- `IamRuleStudio`
- `IamParameterConsole`
- `IamConfigurationPanel`

The workbench exposes principal, provider, identity, active role, policy-decision, allowed-decision, token, privileged-access, inbox, outbox, dead-letter, configuration, rule, parameter, and owned-boundary evidence. Visible actions are RBAC-filtered by tenant, principal, policy, token, privileged access, event, configuration, and audit permissions.

UI and workbench binding evidence must include:

- owned tables plus runtime tables for outbox, inbox, and dead-letter evidence
- fixed AppGen-X event contract and required event topic
- rule, parameter, and configuration fragments
- RBAC mapping for runtime actions

## Release Evidence

The focused test suite proves:

- Runtime smoke covers every declared standard and advanced capability key.
- The package declares owned tables, allowed relational backends, fixed AppGen-X eventing, descriptor APIs, and action-level RBAC.
- The package-local `implementation_contract()` exposes `schema_contract`, `service_contract`, `release_evidence_contract`, runtime tables, required event topic, emitted events, and consumed events.
- Configuration, parameters, rules, schema extensions, event handling, tenant provisioning, principal/provider registration, identity linking, credential verification, role assignment, policy decisions, token grants, privileged access, UI, and workbench evidence execute.
- Boundary validation accepts owned tables and declared API/event/projection dependencies, then rejects direct foreign-table references.
- Invalid backend, stream-picker configuration, unsupported parameters, non-owned schema extensions, idempotent duplicates, retries, and dead letters are verified.

## Seed And Release Evidence

Release evidence includes package-local seed data for default tenant policies,
identity assurance levels, provider trust classes, role templates, and privileged
access review states. The seed descriptors are generated with the package and
validated alongside schema, migration, model, service, route, event, handler,
UI, RBAC, configuration, and release contracts.
