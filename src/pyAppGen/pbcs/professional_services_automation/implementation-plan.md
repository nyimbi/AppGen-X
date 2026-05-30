# Professional Services Automation Standalone Implementation Plan

## Goal

Implement one package-local standalone AppGen-X slice for `professional_services_automation` without touching shared generators, language files, or the progress ledger.

## Scope

- Add package-local `forms.py`, `wizards.py`, `controls.py`, and `standalone.py`.
- Wire standalone metadata into `ui.py`, `release_evidence.py`, `manifest.py`, and `__init__.py`.
- Add package-local documentation and focused standalone tests.

## Constraints

- Stay inside `src/pyAppGen/pbcs/professional_services_automation`.
- Preserve existing runtime/domain-depth contracts that already satisfy repo-wide audits.
- Keep the standalone surface deterministic and side-effect-free in tests.

## Verification Plan

- Compile modified package files with `python3 -m py_compile`.
- Run package-local tests plus `tests/test_pbc_professional_services_automation_runtime.py`.
- Run focused PBC release and capability audits through `pyAppGen.pbc` if import-time conditions allow.
