# WMS Core Release Evidence

Package path: `src/pyAppGen/pbcs/wms_core`

## Summary

`wms_core` now ships as a standalone warehouse-execution PBC with package-local repository bindings, forms/wizards/controls, a one-PBC standalone app, and focused smoke coverage for bootstrap, workflow execution, release evidence, and read-model projection.

## Package evidence

- `repository.py` binds operational forms to WMS-owned tables only.
- `standalone.py` bootstraps configuration, parameters, rules, warehouse masters, inbound events, and one inbound-to-ship workflow.
- `ui.py` exposes domain-specific forms, wizards, controls, navigation, and assistant namespace wiring.
- `release_evidence.py` now verifies artifacts, agent surface, repository surface, UI composition, and standalone smoke in addition to the runtime release checks.

## Verification intent

- Compile package-local Python modules for `wms_core`.
- Run focused package tests including standalone coverage.
- Run relevant `pyAppGen.pbc` audits for `wms_core`.
