# Release Evidence - Building Information Modeling Operations

This package now ships release evidence for the implemented federation-governance slice at `src/pyAppGen/pbcs/building_information_modeling_ops`.

## Evidence Produced

- Database-backed owned schema and model metadata for the PBC-owned BIM tables.
- AppGen-X-only event contract with owned outbox, inbox, and dead-letter tables.
- Forms for coordinate baselines, model package registration, and federation assembly.
- Wizards for federation setup and release readiness.
- Controls for coordinate alignment, issue-purpose publish gates, approval lineage, and owned-table boundary enforcement.
- Workbench views for federation operations, blocked package triage, and release evidence review.
- Release evidence bundles that include contributor checksums, approval states, coordinate basis, and lineage hash.

## Validation Summary

- Package-local tests pass: `13/13`.
- Package compile pass succeeds.
- Single-PBC app smoke confirms:
  - `usable_as_one_pbc_app = True`
  - `forms = 3`
  - `wizards = 2`
  - `controls = 4`
  - `smoke_ok = True`
