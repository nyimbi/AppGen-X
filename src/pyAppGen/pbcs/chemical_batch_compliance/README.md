# Chemical Batch Compliance

`chemical_batch_compliance` now implements one executable chemical manufacturing
compliance slice inside its own PBC directory.

## Implemented Slice

- controlled formula revisions with release gates
- SDS and hazardous-material qualification needed before release
- batch execution records with step, dispense, and parameter evidence
- quality-test driven compliance holds
- regulatory dossier assembly from owned records
- governed document-instruction CRUD previews for the assistant
- package-local workbench forms, wizards, controls, RBAC, and release evidence

## Main Runtime Entry Points

- `chemical_batch_compliance_create_formula_revision`
- `chemical_batch_compliance_release_formula_revision`
- `chemical_batch_compliance_record_batch`
- `chemical_batch_compliance_record_quality_test`
- `chemical_batch_compliance_create_regulatory_submission`
- `chemical_batch_compliance_create_document_instruction`
- `chemical_batch_compliance_query_workbench`
- `chemical_batch_compliance_build_workbench_view`

## Validation

- `python -m compileall src/pyAppGen/pbcs/chemical_batch_compliance`
- `python -m pytest src/pyAppGen/pbcs/chemical_batch_compliance/tests -q`
- runtime smoke through `chemical_batch_compliance_runtime_smoke()`

See `implementation-status.md` for exact execution outcomes and remaining risks.
