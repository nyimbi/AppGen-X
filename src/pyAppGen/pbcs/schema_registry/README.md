# Schema Registry Standalone PBC

`schema_registry` is a standalone AppGen-X platform slice for governed schema evolution, compatibility enforcement, payload validation, consumer blast-radius review, and contract projection publication.

## What Is Included

- Executable runtime proofs in `runtime.py` for subject registration, schema versioning, compatibility checks, payload validation, release evidence, and owned-table boundary enforcement.
- A stateful standalone repository in `repository.py` that persists only inside the `schema_registry` boundary.
- Command/query adapters in `services.py` and `routes.py` that expose one-PBC operations suitable for embedding in a local app shell.
- A workbench surface in `ui.py` with database-backed forms, guided wizards, controls, and standalone navigation.
- Assistant skills in `agent.py` for document intake, governed CRUD planning, policy explanation, and workbench guidance.
- Seed, event, handler, and release evidence modules that keep runtime, UI, and audit surfaces aligned with the AppGen-X contract.

## Standalone Entry Points

- `standalone.py:SchemaRegistryStandaloneApp` boots the PBC as a package-local one-PBC app.
- `standalone.py:smoke_test()` exercises the end-to-end bootstrap path.
- `tests/test_standalone.py` validates the standalone app, repository, forms, and wizards.

## Primary Workflows

- Subject onboarding: configure runtime, register a subject, publish the first schema version, bind consumers, and publish projections.
- Breaking change review: run compatibility analysis, inspect blast radius, record violations, and route remediation through the assistant.
- Release gate readiness: replay payload validation, publish projections, and inspect release evidence before rollout.

## Validation Commands

```bash
python -m compileall src/pyAppGen/pbcs/schema_registry
pytest src/pyAppGen/pbcs/schema_registry/tests tests/test_pbc_schema_registry_runtime.py
```

## Scope Guard

All code and docs for this slice live under `src/pyAppGen/pbcs/schema_registry`. The standalone app does not rely on shared table writes outside the PBC boundary.
