# Release Evidence - Laboratory Information Management

Package directory: `pbcs/laboratory_information_management`.

## Evidence Surface

- Generated runtime/schema/service/event/handler contracts remain package-local and side-effect free.
- Standalone executable surface exists in `standalone.py` and is checked by `standalone.standalone_smoke_test()`.
- Package-local workbench forms, wizards, and controls exist in `forms.py`, `wizards.py`, and `controls.py`.
- Dynamic release validation exists in `release_evidence.py` and includes standalone and documentation checks.
- Focused tests exist in `tests/test_contract.py` and `tests/test_standalone.py`.

## Release Gates

- Owned datastore boundary remains `laboratory_information_management_*` only.
- AppGen-X event contract remains fixed and stream-engine picker exposure stays hidden.
- Result release requires reviewed batch evidence, passed QC, intact custody, and e-signature capture.
- Assistant CRUD paths remain preview-only until confirmation and citation-backed evidence is present.
