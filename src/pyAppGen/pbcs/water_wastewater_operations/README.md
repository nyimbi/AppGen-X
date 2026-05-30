# Water and Wastewater Operations PBC

This package now implements an executable water and wastewater operations slice inside `src/pyAppGen/pbcs/water_wastewater_operations`. The slice keeps all behavior inside the PBC boundary while covering treatment plants, process units, source water, production, distribution zones, pressure and quality samples, pump and valve work, sewer collection, lift stations, wastewater treatment, discharge permits, lab compliance, incidents, flushing, hydrants, asset isolation, SCADA projections, governed agent assistance, AppGen-X events, and release smoke evidence.

## Implemented Slice

- Treatment plant registration with explicit operating-state evidence.
- Process-unit configuration for treatment stages and critical control points.
- Source-water observation capture with anomaly scoring and operator review flags.
- Production-run evidence with district-loss indicators for non-revenue-water monitoring.
- Distribution-zone registration for hydraulic and critical-customer projections.
- Pressure and quality sampling with disinfectant, turbidity, chain-of-custody, and holding-time gates.
- Pump operations, valve operations, sewer collection, and lift-station overflow-risk monitoring.
- Wastewater treatment batch tracking against permit-risk thresholds.
- Discharge permit and lab compliance case handling with governed approval gates.
- Incident response, flushing programs, hydrant inspections, asset isolation plans, and SCADA projections.
- Workbench command center with forms, wizards, controls, and release evidence sections.
- Governed AI surfaces for sample interpretation, incident narration, isolation planning, and SCADA projection review.

## Runtime and Policy

The runtime remains on PostgreSQL, MySQL, and MariaDB only. Eventing remains AppGen-X only. There is no stream-engine picker, runtime-profile selector, broker chooser, or foreign-table mutation path. External systems such as GIS, SCADA historians, field crews, and labs are modeled only as projections or declared dependencies in release evidence.

## UI and Agent Surfaces

The workbench exposes command-center sections for treatment, pressure and quality, pump/valve operations, sewer and lift-station risk, incidents, flushing and hydrants, asset isolation, SCADA projection health, and release evidence. The UI contract now declares package-local forms, wizards, and controls, and the agent contract keeps all skills confirmation-gated while exposing `governed_datastore_crud` in the chatbot surface.

## Verification

Validated with:

- `/Volumes/Media/src/pjs/appgen/.venv/bin/python -m py_compile src/pyAppGen/pbcs/water_wastewater_operations/*.py src/pyAppGen/pbcs/water_wastewater_operations/tests/*.py`
- `PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/pytest src/pyAppGen/pbcs/water_wastewater_operations/tests/test_contract.py src/pyAppGen/pbcs/water_wastewater_operations/tests/test_runtime_capabilities.py src/pyAppGen/pbcs/water_wastewater_operations/tests/test_operational_slice.py tests/test_pbc_water_wastewater_operations_runtime.py -q`
- `PYTHONPATH=src /Volumes/Media/src/pjs/appgen/.venv/bin/python - <<'PY' ... focused audit calls ... PY`
