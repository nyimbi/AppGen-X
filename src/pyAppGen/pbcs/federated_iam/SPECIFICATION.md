# Federated Identity and Access Management PBC Specification

## Scope

`federated_iam` owns platform identity, tenant access, trust federation, policy
decisioning, token issuance, credential verification, role and attribute
assignment, session governance, privileged access, audit evidence, rules,
parameters, configuration, and UI workbench fragments for AppGen-X composable
applications.

The PBC composes with all business PBCs through APIs, AppGen-X events, and
read-model projections. It owns identity and authorization records; consuming
PBCs reference principals, tenants, scopes, and policy decisions through
contracts instead of shared tables.

## Owned Boundary

Owned tables:

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
- `iam_outbox`
- `iam_inbox`
- `iam_dead_letter`

Allowed datastore backends are PostgreSQL, MySQL, and MariaDB. Ordinary eventing
uses the AppGen-X outbox/inbox event contract.

## Standard Capabilities

- Tenant registry, tenant lifecycle, isolation policy, encryption key metadata,
  and region/compliance boundary descriptors.
- Principal registry for users, service accounts, devices, agents, and external
  workforce or customer identities.
- Identity-provider registration for OIDC, SAML, LDAP, SCIM, passkeys, device
  trust, and verifiable credential issuers.
- Federated identity link, claim mapping, credential verification, risk scoring,
  and trust-strength evidence.
- RBAC, ABAC, relationship-based access, policy-as-code evaluation, scoped
  grants, deny overrides, segregation-of-duties checks, and context-aware
  decisions.
- Token grants, refresh sessions, revocation, step-up authentication,
  privileged access workflows, just-in-time access, and break-glass evidence.
- Audit trail, outbox/inbox handlers, retry/dead-letter evidence, rules,
  parameters, configuration schema, permissions, seed data, and workbench UI.

## Advanced Capabilities

- Event-sourced identity lifecycle with immutable hash-chained events.
- Graph-relational trust topology spanning tenants, principals, providers,
  credentials, roles, policies, sessions, tokens, and grants.
- Multi-tenant access isolation with independent configuration, rule sets,
  parameters, and crypto epochs.
- Schema evolution through governed claim and credential extension registration.
- Probabilistic identity-risk, session-risk, trust-strength, and policy-risk
  scoring.
- Real-time access analytics over principals, roles, grants, decisions,
  sessions, step-up requests, and privileged access.
- Counterfactual policy simulation and blast-radius analysis.
- Temporal access risk, stale-role, and privilege-exposure forecasting.
- Autonomous identity exception recommendation with auditable rationale.
- Semantic access request parsing for support, operations, and agent workflows.
- Predictive access risk scoring and self-healing authorization route selection.
- Cryptographic policy-decision proofs, immutable audit trails, dynamic policy
  screening, and continuous control testing.
- Universal API and AppGen-X event contracts, federation views, decentralized
  identity verification, resilience drills, crypto agility, carbon-aware access
  processing, mathematical role optimization, privileged-access allocation,
  anomaly detection, stochastic access exposure modeling, and governed identity
  risk models.

## APIs

- `POST /tenants`
- `POST /principals`
- `POST /identity-providers`
- `POST /identity-links`
- `POST /credential-verifications`
- `POST /role-assignments`
- `POST /policy-decisions`
- `POST /token-grants`
- `POST /sessions/revoke`
- `POST /privileged-access-requests`
- `POST /iam-rules`
- `POST /iam-parameters`
- `POST /iam-configuration`

## Events

Emitted:

- `TenantProvisioned`
- `PrincipalVerified`
- `AccessPolicyChanged`
- `PolicyDecisionRecorded`
- `TokenGranted`
- `PrivilegedAccessApproved`

Consumed:

- `RoleChanged`
- `TenantProvisioned`
- `CustomerUpdated`
- `EmployeeProvisioned`
- `ServiceAccountRequested`

Handlers are idempotent through `federated_iam:<EventType>:<event_id>` keys,
retry through the AppGen-X outbox adapter, and route exhausted failures to
`federated_iam.dead_letter`.

## UI

The package exports a workbench UI contract with fragments for tenant registry,
principal registry, identity providers, credential verification, role
assignments, policy decisions, token grants, privileged access, audit controls,
rules, parameters, and configuration.
