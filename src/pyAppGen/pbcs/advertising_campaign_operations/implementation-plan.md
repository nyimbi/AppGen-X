# Advertising Campaign Operations Standalone Implementation Plan

## Scope

Implement one executable, package-local PBC app surface inside
`src/pyAppGen/pbcs/advertising_campaign_operations` only.

The slice is grounded in `improve1.md` and focuses on:

1. Canonical campaign brief modeling.
2. Launch-readiness review and launch attempt handling.
3. Package-local standalone app wiring for routes, services, UI, assistant planning, permissions, workflows, and release evidence.

## Constraints

- Do not edit shared generator, DSL, or progress-ledger files.
- Keep all behavior and verification inside this package.
- Preserve the declared AppGen-X event contract and owned-table boundary.
- Prefer the smallest viable diff that produces an executable one-PBC surface.

## Planned Changes

### 1. Tighten executable contracts

- Replace thin wrappers in `models.py`, `schema_contract.py`, and `service_contract.py` with contracts that describe the implemented slice.
- Keep schema ownership and service operations aligned with package-local runtime behavior.

### 2. Build the standalone surface

- Add a package-local `standalone.py`.
- Upgrade `services.py` to own in-memory runtime state and expose command/query operations through one consistent contract.
- Upgrade `routes.py` to method/path route dispatch instead of string-only placeholders.

### 3. Make the UI package-local and usable

- Add standalone app metadata, navigation, forms, wizards, and controls in `ui.py`.
- Render a workbench shell that surfaces launch queue, blockers, actions, and release evidence affordances.

### 4. Complete assistant and workflow support

- Expand `agent.py` for campaign-brief preview, launch-readiness preview, and document-instruction CRUD planning.
- Add package-local workflows for brief-to-plan, launch gate review, and assistant document planning.

### 5. Tighten governance and release evidence

- Expand `permissions.py`, `config.py`, `handlers.py`, and `release_evidence.py` so they reflect the same executable slice.
- Update `README.md`, `implementation-status.md`, and `RELEASE_EVIDENCE.md` to describe only package-local evidence.

### 6. Add focused package tests

- Keep tests under `src/pyAppGen/pbcs/advertising_campaign_operations/tests`.
- Cover standalone app bootstrapping, route dispatch, assistant planning, UI shell contracts, and release evidence.

## Acceptance Targets

- A standalone app can bootstrap package-local state, create a campaign plan, attempt launch, and render the workbench.
- Routes and service contracts agree on methods, paths, permissions, and owned-table scope.
- UI contract exposes forms, wizards, and controls for the slice.
- Assistant document planning returns a governed CRUD preview with required confirmation.
- Release evidence is package-local and references only focused package verification.

## Verification Plan

- Run `py_compile` on modified package modules.
- Run focused pytest for `src/pyAppGen/pbcs/advertising_campaign_operations/tests`.
- Run package-local smoke and audit entry points that exist for this PBC.

## Non-Goals

- No edits outside this package.
- No new dependencies.
- No shared framework refactors.
- No attempt to implement the full backlog from `improve1.md`; only the standalone slice foundation.
