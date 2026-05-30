# Construction Contracts and Commercials PBC

`construction_contracts_commercials` is a package-local AppGen-X slice for construction commercial controls. It owns contract commercial state, pay application intake and certification, retainage, variation orders, commercial claims, lien waivers, subcontract compliance, governance artifacts, AppGen-X event tables, workbench views, assistant previews, and a standalone one-PBC app surface without reaching into scheduling, procurement, finance, tax, or document-storage source-of-truth tables.

## Implemented Behavior

- Contract creation with pricing basis, jurisdiction, guarantees, obligations, and a reconciled schedule of values.
- Lifecycle progression with explicit allowed transitions and closeout blocker checks.
- Pay application intake with attachment/evidence validation and overclaim protection against schedule-of-values balances.
- Waiver-gated certification and retainage hold/release workflows.
- Variation approval that affects contract value only when approved.
- Commercial claim notice timeliness assessment and risk surfacing.
- Subcontract package compliance holds for missing insurance or bonds.
- Workbench queues for certification, waivers, guarantees, claims, retainage, and final account blockers.
- Governed agent/chatbot document-instruction parsing and CRUD previews with citations and human approval requirements.
- Standalone package-local store, service, route, UI, and app bootstrap entrypoints for local one-PBC execution.

## Key Entrypoints

- Runtime: `construction_contracts_commercials_runtime_capabilities()`
- Services: `ConstructionContractsCommercialsService`
- Standalone services: `ConstructionContractsCommercialsStandaloneService`
- Routes: `dispatch_route(...)`
- Standalone routes: `dispatch_standalone_route(...)`
- UI: `construction_contracts_commercials_build_workbench_view(...)`
- Standalone UI: `construction_contracts_commercials_render_standalone_workbench(...)`
- Agent: `document_instruction_plan(...)`, `datastore_crud_plan(...)`
- Standalone app: `construction_contracts_commercials_standalone_app_contract()`
- Release evidence: `build_release_evidence()`

## Package-Local Development

- Tests:
  - `pytest src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_contract.py src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_standalone.py`
- Syntax smoke:
  - `python3 -m compileall src/pyAppGen/pbcs/construction_contracts_commercials`
- Standalone smoke:
  - `PYTHONPATH=src python3 -c "from pyAppGen.pbcs.construction_contracts_commercials.standalone import construction_contracts_commercials_standalone_app_smoke; print(construction_contracts_commercials_standalone_app_smoke()['ok'])"`

## Boundaries

- Only `construction_contracts_commercials_*` business tables and its AppGen-X event tables are owned here.
- Cross-PBC collaboration must use declared APIs, projections, or AppGen-X events.
- The package does not write schedule, cost, tax, finance, legal-matter, vendor-master, or document-storage source tables.
