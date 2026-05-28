# Construction Contracts and Commercials PBC

`construction_contracts_commercials` is a package-local AppGen-X slice for construction commercial controls. It owns contract commercial state, pay application intake and certification, retainage, variation orders, commercial claims, lien waivers, subcontract compliance, governance artifacts, AppGen-X event tables, workbench views, and assistant previews without reaching into scheduling, procurement, finance, tax, or document-storage source-of-truth tables.

## Implemented Behavior

- Contract creation with pricing basis, jurisdiction, guarantees, obligations, and a reconciled schedule of values.
- Lifecycle progression with explicit allowed transitions and closeout blocker checks.
- Pay application intake with attachment/evidence validation and overclaim protection against schedule-of-values balances.
- Waiver-gated certification and retainage hold/release workflows.
- Variation approval that affects contract value only when approved.
- Commercial claim notice timeliness assessment and risk surfacing.
- Subcontract package compliance holds for missing insurance or bonds.
- Workbench queues for certification, waivers, guarantees, claims, retainage, and final account blockers.
- Governed agent/chatbot document-instruction parsing and CRUD previews with citations/human approval requirements.

## Key Entrypoints

- Runtime: `construction_contracts_commercials_runtime_capabilities()`
- Services: `ConstructionContractsCommercialsService`
- Routes: `dispatch_route(...)`
- UI: `construction_contracts_commercials_build_workbench_view(...)`
- Agent: `document_instruction_plan(...)`, `datastore_crud_plan(...)`
- Release evidence: `build_release_evidence()`

## Package-Local Development

- Tests:
  - `pytest src/pyAppGen/pbcs/construction_contracts_commercials/tests/test_contract.py`
- Syntax smoke:
  - `python -m compileall src/pyAppGen/pbcs/construction_contracts_commercials`

## Boundaries

- Only `construction_contracts_commercials_*` business tables and its AppGen-X event tables are owned here.
- Cross-PBC collaboration must use declared APIs, projections, or AppGen-X events.
- The package does not write schedule, cost, tax, finance, legal-matter, vendor-master, or document-storage source tables.
