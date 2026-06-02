# personnel_identity PBC

`personnel_identity` is the standalone workforce directory, identity, lifecycle, and access-governance packaged business capability. It owns department, employee, lifecycle, role, identity assurance, provisioning, privacy, policy, audit, and AppGen-X event artifacts.

## Standalone Domain Coverage

- Configure PostgreSQL/MySQL/MariaDB personnel identity boundaries and the fixed AppGen-X people event topic.
- Register departments and maintain employee identities, manager relationships, lifecycle status, contacts, documents, roles, and identity attributes.
- Enforce worker eligibility, segregation of duties, role limits, identity assurance thresholds, privacy/residency metadata, and policy screening.
- Consume provisioning, access-policy, org-unit, and role-review events into owned projections.
- Generate eligibility proofs, route provisioning with failover evidence, and surface controls through forms, wizards, workbench views, and agent skills.

## Executable Surfaces

- `runtime.py` contains side-effect-free personnel identity commands and advanced proof/risk/resilience functions.
- `repository.py` backs organization, employee, access, identity, and governance read models.
- `standalone.py` executes a complete department-to-active-employee identity workflow.
- `ui.py` exposes forms, wizards, controls, workbench cards, and standalone navigation.
- `seed_data.py` provides deterministic demo personnel data.
- `release_evidence.py` validates runtime, repository, UI, agent, model, event, API, service, schema, and artifact evidence.
