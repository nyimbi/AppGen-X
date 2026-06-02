# Release Evidence - Building Information Modeling Operations

This package ships release evidence for the implemented federation-governance standalone slice at `src/pyAppGen/pbcs/building_information_modeling_ops`.

## Evidence Produced

- Database-backed owned schema and model metadata for the PBC-owned BIM tables.
- AppGen-X-only event contract with owned outbox, inbox, and dead-letter tables.
- Forms for coordinate baselines, model package registration, and federation assembly.
- Wizards for federation setup and release readiness.
- Controls for coordinate alignment, issue-purpose publish gates, approval lineage, and owned-table boundary enforcement.
- Standalone app bootstrap and demo workbench rendering through `standalone.py`.
- Assistant document-instruction and datastore CRUD planning before governed mutation.
- Release evidence bundles that include contributor checksums, approval states, coordinate basis, and lineage hash.

## Validation Summary

- Package-local tests pass: `16/16`.
- Package compile pass succeeds.
- Standalone smoke confirms `active_federations = 1`, `doc_plan_ok = True`, and `crud_plan_ok = True`.
- Package-local audit pass succeeds across 12 smoke contracts: package, agent, capability, config, events, handlers, permissions, release, routes, runtime, standalone, and UI.
