# personnel_identity Implementation Plan

## Scope

Make Personnel Identity usable as a one-PBC application with owned schema, services, APIs, events, handlers, repository/read models, forms, wizards, controls, assistant skills, seed data, tests, and release evidence.

## Delivered Architecture

1. Runtime owns department, employee, role, identity attribute, lifecycle, policy, proof, and provisioning behavior.
2. Repository contracts expose PBC-owned read models without shared-table access.
3. UI contracts surface hire-to-identity, role review, assurance, offboarding, and governance workflows.
4. Standalone smoke exercises configuration, parameters, rules, schema extension, event projections, department setup, employee creation, status transition, role assignment, identity attributes, proof generation, provisioning route, and control tests.
5. Release evidence validates executable package surfaces.

## Guardrails

- No user-facing stream-engine picker.
- Ordinary backends remain PostgreSQL, MySQL, or MariaDB.
- Cross-PBC context enters through declared APIs, AppGen-X events, or owned projections.
