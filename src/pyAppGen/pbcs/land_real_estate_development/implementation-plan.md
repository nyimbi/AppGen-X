# Land Real Estate Development Implementation Plan

## Selected Slice

Implement a standalone land-development operating slice inside this package,
covering:

- land acquisition and control thresholds,
- zoning and entitlement sequencing,
- parcel constraints and environmental blockers,
- feasibility and pro forma residual land value,
- utility availability and permit readiness,
- site planning and approval registers,
- construction readiness plus sales and lease handoff,
- assistant document and CRUD mutation previews.

## Why This Slice

- It turns a contract-heavy package into executable domain behavior.
- It stays fully inside the owned PBC boundary.
- It addresses the strongest domain gaps called out in `improve1.md` without editing shared generators.
- It supports standalone verification with package-local routes, services, and tests.

## Planned Changes

- Add a standalone in-memory store and service for project, parcel, acquisition, zoning, entitlement, permit, site-plan, feasibility, approval, and handoff flows.
- Add package-local forms, wizards, and controls that map to the standalone flow.
- Extend local manifest, UI, and release evidence to advertise the new standalone surface.
- Add focused standalone tests and package-local documentation.

## Constraints

- Work only inside `src/pyAppGen/pbcs/land_real_estate_development`.
- Do not modify shared generator, language, or progress-ledger files.
- Keep AppGen-X eventing only.
- Keep `stream_engine_picker_visible` false.
- Keep `shared_table_access` false.

## Validation Plan

- Run `py_compile` on modified package files.
- Run focused pytest on `tests/test_standalone.py` and existing package tests.
- Run direct standalone and release evidence smoke calls.
- Record evidence in `implementation-status.md`.
