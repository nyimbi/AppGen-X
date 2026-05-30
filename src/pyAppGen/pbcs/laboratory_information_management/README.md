# Laboratory Information Management PBC

`laboratory_information_management` now includes a package-local standalone one-PBC application surface for sample accessioning, custody, testing, batch execution, QC, OOS handling, stability studies, CoA generation, audit evidence, and assistant-guided CRUD previews.

## What This Package Owns

- Package-local executable contracts for the existing runtime, services, routes, UI, events, handlers, permissions, and release evidence.
- A standalone app shell in `standalone.py` that runs core LIMS workflows without touching shared generator code.
- Package-local `forms.py`, `wizards.py`, and `controls.py` for the workbench surface.
- Focused standalone tests in `tests/test_standalone.py`.

## Domain Coverage

The standalone slice covers:

- sample accessioning with duplicate-prevention and identity-confidence checks,
- chain-of-custody capture with exception gating,
- test ordering and method/SOP registration,
- instrument readiness, calibration, QC lots, reagent inventory, and analyst competency,
- batch runs, result import, technical review, release gating, and OOS/CAPA handling,
- stability-study scheduling and completion,
- certificate-of-analysis generation and e-signature evidence,
- tamper-evident audit hash chains and assistant CRUD previews with citations.

## Key Entry Points

- Runtime contracts: `runtime.py`
- Standalone app: `standalone.py`
- UI contract and rendering: `ui.py`
- Release evidence: `release_evidence.py`

## Verification

Primary verification lives in:

- `tests/test_contract.py`
- `tests/test_standalone.py`
- `standalone.standalone_smoke_test()`
- `release_evidence.validate_release_evidence()`
