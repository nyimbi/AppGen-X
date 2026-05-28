# Clinical Trials Management Implementation Plan

## Goal

Turn `clinical_trials_management` into a coherent one-PBC clinical operations app surface that remains fully package-local. The slice must represent protocol governance, site activation, subject enrollment, consent, visits, safety, monitoring, assistant previews, and release evidence without touching the central generator or other PBCs.

## Scope

- Keep all edits under `src/pyAppGen/pbcs/clinical_trials_management`.
- Preserve the owned-table boundary and AppGen-X event contract.
- Replace scaffold drift with domain-specific contracts and executable previews.

## Work Items

1. Tighten domain contracts
   - Replace generic service, route, UI, event, handler, RBAC, and governance placeholders with clinical-trials-specific surfaces.
   - Align schema and model metadata with protocol, site, subject, consent, visit, safety, monitoring, and release-audit concerns.

2. Add one-PBC app surfaces
   - Add package-local `forms.py`, `wizards.py`, and `controls.py`.
   - Bind those surfaces into the workbench UI, services, routes, and release evidence.

3. Improve governed assistant behavior
   - Infer domain entities from protocol amendments, consent memos, monitoring notes, and safety instructions.
   - Return preview-only CRUD plans with owned-table boundary proof, permission hints, and citation requirements for regulatory-facing text.

4. Strengthen release evidence
   - Ensure release evidence covers schema, services, routes, UI, controls, assistant previews, docs presence, and package-local smoke paths.
   - Add package-local `README.md` and `implementation-status.md`.

5. Add focused tests
   - Cover enrollment gating, consent/version matching, site activation, adverse-event SLA handling, lock readiness, forms/wizards/controls catalogs, assistant preview behavior, route contracts, and release evidence.

## Non-Goals

- No edits to the AppGen-X central generator, DSL, or shared framework.
- No cross-PBC schema, docs, or runtime changes.
- No new third-party dependencies.

## Verification Plan

- Run package-local `pytest` for `src/pyAppGen/pbcs/clinical_trials_management/tests`.
- Run Python compilation checks on modified modules.
- Use runtime smoke plus focused new tests as the primary evidence.
