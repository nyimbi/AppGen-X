# Water and Wastewater Operations Implementation Plan

## Scope

Implement a package-local, executable standalone slice that replaces the previous scaffold behavior with real water and wastewater operations logic. The slice stays entirely inside `src/pyAppGen/pbcs/water_wastewater_operations` and does not touch shared generator, language, documentation, or ledger files.

## Why This Slice

The current package already satisfies structural audits but not domain depth. `improve1.md` calls for treatment-state handling, sampling governance, permit and incident flows, pump and valve evidence, sewer and lift-station monitoring, hydrant and flushing work, asset isolation, SCADA projections, governed AI assistance, and realistic release smoke evidence. This slice implements those behaviors with deterministic functions that can be proven through package-local tests.

## Planned Changes

1. Add a package-local operational engine.
   - Model treatment plants, process units, source water, production, distribution zones, samples, pumps, valves, sewer collection, lift stations, wastewater treatment batches, permits, lab cases, incidents, flushing programs, hydrants, isolation plans, and SCADA projections.
   - Keep all persistence evidence inside owned tables and AppGen-X outbox/inbox/dead-letter tables.

2. Rewire runtime, services, routes, UI, and agent surfaces.
   - Expose advanced runtime operations for schema, service, release, workbench, and governed document/CRUD flows.
   - Add forms, wizards, controls, and command-center sections to the UI contract.
   - Keep all agent skills confirmation-gated and aligned to `governed_datastore_crud`.

3. Refresh package-local documentation and release evidence.
   - Hand-craft `README.md`, `implementation-status.md`, and this plan.
   - Refresh `SPECIFICATION.md` traceability so manifest tables, APIs, features, permissions, and configuration remain auditable.
   - Expand `RELEASE_EVIDENCE.md` to describe smoke scenarios and control evidence.

4. Add package-local tests.
   - Preserve the exact required contract-test function names.
   - Add runtime-capability and operational-slice tests for samples, incidents, permits, hydrants, isolation, SCADA projections, and release smoke.

## Acceptance Targets

- Water/wastewater operations execute through deterministic package-local functions and service entrypoints.
- The workbench exposes forms, wizards, controls, and command-center summaries.
- All agent skills require confirmation and surface `governed_datastore_crud`.
- AppGen-X remains the only event contract and PostgreSQL/MySQL/MariaDB remain the only backends.
- Package-local tests and focused audits pass after the implementation.

## Verification Plan

- Run Python compilation over the modified package.
- Run package-local tests plus the focused root runtime test for this PBC.
- Run `git diff --check`.
- Run focused source, spec, agent, implementation, capability, and generation audit entrypoints for `water_wastewater_operations`.

## Non-Goals

- No edits outside this PBC package.
- No new dependencies.
- No stream-engine selection surface.
- No foreign-table ownership or direct mutation of GIS, SCADA, crew, lab, or customer systems.
