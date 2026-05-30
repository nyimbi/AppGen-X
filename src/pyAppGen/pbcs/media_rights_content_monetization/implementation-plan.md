# Media Rights and Content Monetization Implementation Plan

## Goal

Deepen `src/pyAppGen/pbcs/media_rights_content_monetization` into a credible standalone one-PBC app without touching shared generators, language assets, or other PBC packages.

## Constraints

- Stay entirely inside `src/pyAppGen/pbcs/media_rights_content_monetization`.
- Preserve the owned-table boundary and AppGen-X event contract already declared by the package.
- Keep the standalone surface executable with package-local Python state rather than introducing new dependencies.
- Reflect real media-rights concerns: chain-of-title readiness, inbound vs outbound licensing scope, window amendments, territory carve-outs, platform entitlements, holdbacks, exclusivity conflicts, and royalty waterfall previews.

## Workstreams

1. Standalone domain app
   Add `standalone.py` with an executable one-PBC application class that can configure defaults, register rules and parameters, intake rights assets and licenses, amend windows, record territory restrictions, approve usage only when rights are eligible, simulate royalty statements, and expose workbench and assistant-preview surfaces.

2. Operator-facing workbench depth
   Add explicit `forms.py`, `wizards.py`, and `controls.py` so the package has concrete intake, guided operations, and release/control-center workflows rather than only abstract fragments.

3. UI and package exports
   Update `ui.py`, `__init__.py`, and `manifest.py` so the new standalone/forms/wizards/controls surface is discoverable through package-local contracts and source registration metadata.

4. Release evidence
   Expand `release_evidence.py` and `RELEASE_EVIDENCE.md` so readiness now covers the standalone app, workbench catalogs, and package-local documentation presence.

5. Focused verification
   Add targeted tests for the standalone slice and keep validation local to this PBC through compile checks, focused pytest runs, and package-scoped audits where available.

## Validation Plan

- `python3 -m compileall src/pyAppGen/pbcs/media_rights_content_monetization`
- `pytest src/pyAppGen/pbcs/media_rights_content_monetization/tests`
- Focused package audit from the new worktree when the repo exposes one without widening scope
