# Composition Engine Implementation Plan

## Goal

Turn `composition_engine` into a usable standalone composition/orchestration PBC that can run database-backed forms, workflows, controls, and assistant skills without leaving the package boundary.

## Selected Work

- Add a package-local SQLite repository that applies owned migrations and persists the runtime snapshot.
- Add a standalone app wrapper that bootstraps the slice, executes real forms and wizards, renders the workbench, and exposes assistant/control-center flows.
- Tighten forms and wizards so each step maps to an executable operation instead of placeholder metadata.
- Extend release evidence and implementation exports to include repository and standalone-app contracts.
- Add focused repository and standalone tests alongside the existing runtime/contract coverage.
- Refresh documentation and status evidence for the standalone path.

## Execution Steps

1. Add runtime-backed repository persistence and include runtime event tables in the migration.
2. Implement `CompositionEngineStandaloneApp` with bootstrap, form submission, wizard execution, route dispatch, assistant preview, and workbench rendering.
3. Align forms and wizards with executable preview, rehearsal, control-center, and release-note operations.
4. Export repository and standalone contracts from the package and fold them into release evidence.
5. Add focused tests for repository sync, standalone workflows, and database-backed workbench usage.
6. Re-run compile, package-local tests, and the relevant `pyAppGen.pbc` composition-engine contract test, then record the evidence.
