# Tax Localization

`tax_localization` is a standalone AppGen-X packaged business capability for indirect tax determination, jurisdiction setup, product taxability, exemption governance, invoice tax recording, filing preparation, remittance control, and authority-facing audit evidence.

## Standalone Scope

This package is designed to run as a one-PBC domain app without shared-table writes. The standalone surface includes:

- a package-local SQLite repository used for deterministic persistence smoke tests;
- forms for jurisdiction intake, rule authoring, quote calculation, invoice tax recording, filing preparation, and assistant-guided document intake;
- guided wizards for jurisdiction onboarding, quote-to-invoice tax flow, filing close, and authority notice response;
- executable controls for release readiness, filing gating, exemption evidence, boundary proof, and assistant mutation guardrails;
- an AppGen-X event contract with owned outbox, inbox, and dead-letter tables;
- an assistant surface that previews CRUD plans before any mutation path is considered.

## Package Layout

- `runtime.py` contains the package-owned tax behaviors, workbench projection logic, and capability smoke checks.
- `repository.py` provides a local database-backed persistence contract for standalone validation.
- `forms.py`, `wizards.py`, and `controls.py` define the operator-facing standalone app surface.
- `app_surface.py` proves the slice can operate alone with database-backed forms, workflows, controls, and assistant previews.
- `agent.py` exposes governed tax-document intake and bounded mutation previews.
- `release_evidence.py` aggregates schema, service, UI, assistant, repository, and documentation readiness.

## Validation

Typical focused validation for this package:

```bash
python3 -m py_compile src/pyAppGen/pbcs/tax_localization/*.py
python3 -m pytest src/pyAppGen/pbcs/tax_localization/tests/test_contract.py src/pyAppGen/pbcs/tax_localization/tests/test_app_surface.py
python3 -c "import sys; sys.path.insert(0, 'src'); from pyAppGen.pbc import pbc_implementation_contract, pbc_implementation_release_audit, pbc_implemented_capability_audit; print({'contract': pbc_implementation_contract('tax_localization')['pbc'], 'release_ok': pbc_implementation_release_audit(('tax_localization',))['ok'], 'capability_ok': pbc_implemented_capability_audit(('tax_localization',))['ok']})"
```

## Operating Notes

- All writes stay inside the package-owned boundary.
- The assistant is preview-only for mutation requests and always requires confirmation for non-read actions.
- The standalone repository exists for local validation evidence; the package contract still declares PostgreSQL/MySQL/MariaDB as supported runtime backends.
