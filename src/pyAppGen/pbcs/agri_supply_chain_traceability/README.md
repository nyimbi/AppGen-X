# Agri Supply Chain Traceability

This AppGen-X PBC owns package-local traceability records for farm lots, certifications, storage events, transport legs, recall links, provenance proof, and release-readiness decisions.

## Executable Slice

This implementation delivers a real pre-shipment release gate from the backlog. The slice records traceability evidence into package-local runtime state and computes an explainable release verdict.

### Release Gate Checks

- active source farm lot
- provenance proof linking the release candidate to the source lot
- certification coverage for lot, site, commodity, and shipment date
- no unresolved storage or cold-chain exceptions
- no unresolved transport, seal-integrity, or receiving-confirmation issues
- no active recall link
- no pending hazards, lab results, or corrective actions on the candidate

### Main Runtime Entry Points

- `agri_supply_chain_traceability_command_farm_lot`
- `agri_supply_chain_traceability_record_certification`
- `agri_supply_chain_traceability_record_storage_event`
- `agri_supply_chain_traceability_record_transport_leg`
- `agri_supply_chain_traceability_record_recall_link`
- `agri_supply_chain_traceability_record_provenance_proof`
- `agri_supply_chain_traceability_assess_release_readiness`
- `agri_supply_chain_traceability_query_workbench`

### Contracts Updated

- Runtime capabilities advertise `assess_release_readiness`.
- Service contracts expose release-gate and evidence-recording commands.
- UI metadata exposes a release-gate panel in the workbench surface.
- Agent metadata exposes release-readiness guidance and release-gate preview hints.
- Release evidence includes the release-gate artifact and required evidence classes.

### Validation

Run:

```bash
./.venv/bin/python -m pytest -q \
  src/pyAppGen/pbcs/agri_supply_chain_traceability/tests/test_contract.py \
  tests/test_pbc_agri_supply_chain_traceability_implementation.py \
  tests/test_pbc_agri_supply_chain_traceability_runtime.py
```

Expected result for this slice: all tests pass.
