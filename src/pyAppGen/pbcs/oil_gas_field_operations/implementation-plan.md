# Oil and Gas Field Operations Implementation Plan

## Goal

Turn `oil_gas_field_operations` into a coherent standalone one-PBC field-operations app surface while staying entirely inside `src/pyAppGen/pbcs/oil_gas_field_operations`.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/oil_gas_field_operations`.
- Preserve the owned-table boundary and AppGen-X event contract.
- Add a domain-deep standalone app surface instead of relying on shared generator changes.

## Work Items

1. Align package-local exports with field-operations reality
   - Keep runtime, routes, services, UI, release evidence, and metadata aligned on wells, production, tickets, workovers, and HSE.

2. Add standalone app surfaces
   - Add package-local `forms.py`, `wizards.py`, `controls.py`, and `standalone.py`.
   - Surface those contracts through UI, services, routes, and package metadata.

3. Improve assistant and operator workflows
   - Make document/instruction preview domain-specific for morning review, workover readiness, and bounded CRUD planning.
   - Keep assistant actions preview-only and confirmation-gated for mutations.

4. Strengthen release evidence and documentation
   - Ensure release evidence checks forms, wizards, controls, standalone smoke, and docs presence.
   - Add package-local `README.md` and implementation status.

5. Add focused tests
   - Cover forms, wizards, controls, assistant preview, routes, services, release evidence, and the standalone app journey.

## Non-Goals

- No edits to shared AppGen-X generators, DSL, language files, or ledgers.
- No cross-PBC schema, docs, or runtime changes.
- No new third-party dependencies.

## Verification Plan

- Run package-local `pytest` for `src/pyAppGen/pbcs/oil_gas_field_operations/tests`.
- Run Python compilation checks on modified modules.
- Use standalone smoke, control-center evidence, and route/service tests as the primary acceptance proof.
