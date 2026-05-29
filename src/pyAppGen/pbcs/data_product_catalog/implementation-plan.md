# Implementation Plan

## Objective

Turn `data_product_catalog` into a coherent one-PBC package where models, schema, services, routes, UI, agent tooling, eventing, and release evidence all describe the same owned capability.

## Package-Local Constraints

- Stay entirely inside `src/pyAppGen/pbcs/data_product_catalog`.
- Preserve the PBC’s owned-table boundary.
- Keep AppGen-X as the only event contract.
- Favor deterministic, executable metadata and smokeable runtime behavior over placeholder text.

## Plan

1. Establish one canonical blueprint.
   Create a package-local source of truth for owned tables, fields, operations, routes, events, rules, parameters, forms, wizards, and controls.

2. Align executable contracts around that blueprint.
   Refactor manifest, domain depth, models, schema contract, service contract, routes, UI, agent, capability assurance, release evidence, and runtime/service execution to import the same contract data.

3. Strengthen the standalone runtime path.
   Provide a deterministic in-memory `DataProductCatalogApp` that exercises configuration, domain operations, AppGen-X outbox/inbox handling, workbench queries, and smoke checks without relying on external state.

4. Improve owned database evidence.
   Replace the drifted migration with a clean package-local migration that covers the owned business tables and AppGen-X event tables declared by the blueprint.

5. Add release-facing documentation.
   Provide `README.md`, `implementation-status.md`, and updated `RELEASE_EVIDENCE.md` so the package exposes its scope, validation path, and release gates from within the directory.

6. Expand focused tests.
   Verify deep schema/service counts, domain-depth coverage, standalone runtime execution, agent CRUD/document planning, and the named release gates:
   `pbc_source_artifact_contract`
   `pbc_implementation_release_audit`
   `pbc_generation_smoke_audit`

## Acceptance Criteria

- At least 20 owned tables and at least 15 executable domain operations are exposed consistently.
- Services, routes, UI surfaces, and agent planning resolve from one package-local contract.
- The migration matches the owned-table shape materially enough for audit evidence.
- The named release gates execute successfully from package-local code.
- Focused package tests and syntax validation pass.
