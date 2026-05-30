# Nonprofit Program Impact Implementation Plan

## Goal

Turn `nonprofit_program_impact` into a coherent standalone one-PBC app surface that remains fully package-local. The existing runtime already advertises nonprofit program, beneficiary, service, outcome, grant, evidence, and donor-report concepts. This slice focuses on making that runtime consumable through domain-specific standalone app surfaces and release evidence.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/nonprofit_program_impact`.
- Preserve the owned-table boundary and AppGen-X event contract.
- Improve domain coherence instead of broadening scope into central generators or sibling PBCs.

## Work Items

1. Add package-local standalone app surfaces
   - Introduce `standalone.py` with an executable in-memory nonprofit impact service.
   - Cover program setup, beneficiary enrollment, service capture, outcomes, evidence, donor reporting, and timelines.

2. Add workbench forms, wizards, and controls
   - Add `forms.py`, `wizards.py`, and `controls.py` with nonprofit-specific workflows.
   - Keep assistant previews bounded to the owned table set.

3. Wire exports through package metadata
   - Update `ui.py`, `release_evidence.py`, `manifest.py`, and `__init__.py`.
   - Surface forms, wizards, controls, docs, and standalone release readiness in package contracts.

4. Add focused docs and tests
   - Add package-local `README.md`, `implementation-status.md`, and targeted standalone tests.
   - Validate compile and package-local pytest coverage where available.

## Non-Goals

- No edits to shared AppGen-X generator, DSL, or framework files.
- No cross-PBC schema, docs, or runtime changes.
- No new third-party dependencies.

## Verification Plan

- Run package-local `pytest` for `src/pyAppGen/pbcs/nonprofit_program_impact/tests`.
- Run Python compilation checks on the modified package.
- Use standalone smoke plus release evidence validation as the primary evidence.
