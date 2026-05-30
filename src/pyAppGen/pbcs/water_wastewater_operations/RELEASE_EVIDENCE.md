# Water and Wastewater Operations Release Evidence

## Package-local release gates

This package now provides executable release evidence for the focused audit surfaces used for standalone PBC completion:

- `pbc_source_artifact_release_audit`
- `pbc_specification_release_audit`
- `pbc_agent_capability_release_audit`
- `pbc_implementation_release_audit`
- `pbc_implemented_capability_audit`
- `pbc_generation_smoke_audit`

## Evidence Summary

- Owned tables are package-local and every mutable record remains under the `water_wastewater_operations_` prefix.
- Eventing remains AppGen-X only with explicit outbox, inbox, retry, idempotency, and dead-letter evidence.
- Runtime contracts expose schema, service, API, release, workbench, governed document parsing, and advanced assessment entrypoints.
- UI evidence includes package-local forms, wizards, controls, and command-center sections.
- Agent evidence proves `governed_datastore_crud`, confirmation-gated skills, and mutation-preview workflows.
- Release smoke scenarios execute treatment plant, process unit, sample, pump, incident, isolation, SCADA, permit, and lab compliance paths.

## Suggested Validation Commands

```bash
/Volumes/Media/src/pjs/appgen/.venv/bin/python -m py_compile   src/pyAppGen/pbcs/water_wastewater_operations/*.py   src/pyAppGen/pbcs/water_wastewater_operations/tests/*.py

PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest   src/pyAppGen/pbcs/water_wastewater_operations/tests/test_contract.py   src/pyAppGen/pbcs/water_wastewater_operations/tests/test_runtime_capabilities.py   src/pyAppGen/pbcs/water_wastewater_operations/tests/test_operational_slice.py   tests/test_pbc_water_wastewater_operations_runtime.py -q
```
