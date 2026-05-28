## Implementation Plan

### Scope

Implement a real executable slice for backlog item 49: a pre-shipment release gate that evaluates whether an agricultural shipment candidate can be released using package-local traceability evidence.

### Why This Slice

- It is directly listed in `improve1.md`.
- It fits the current owned record set: `farm_lot`, `certification`, `storage_event`, `transport_leg`, `recall_link`, and `provenance_proof`.
- It can be expressed through the existing AppGen-X runtime/service/UI/agent surfaces without widening into new infrastructure or foreign-table coupling.

### Current Gaps

- Domain execution is mostly placeholder metadata.
- There is no executable release decision that combines lineage, certificate coverage, storage or transport exceptions, recall state, and explainable blockers.
- The workbench and assistant surfaces do not advertise a concrete release-readiness workflow.

### Planned Slice

1. Add package-local release-gate logic that:
   - requires an active farm lot
   - requires provenance evidence linking the release candidate back to the source lot
   - validates certification validity and scope on a shipment date
   - blocks on unresolved storage exceptions
   - blocks on unresolved transport exceptions or broken seal evidence
   - blocks on active recall links
   - blocks on pending hazards, lab results, or corrective actions declared on the candidate
   - returns an explainable verdict with passed checks and blockers
2. Wire the slice into runtime/service contracts as a supported command/query surface.
3. Extend UI and agent contracts so the release gate is visible as a supported operational capability.
4. Add focused tests for:
   - a release-ready scenario
   - blocked release due to certificate and cold-chain/custody issues
   - service and UI exposure for the new slice

### Files To Change

- `src/pyAppGen/pbcs/agri_supply_chain_traceability/runtime.py`
- `src/pyAppGen/pbcs/agri_supply_chain_traceability/services.py`
- `src/pyAppGen/pbcs/agri_supply_chain_traceability/ui.py`
- `src/pyAppGen/pbcs/agri_supply_chain_traceability/agent.py`
- `tests/test_pbc_agri_supply_chain_traceability_implementation.py`
- `src/pyAppGen/pbcs/agri_supply_chain_traceability/implementation-status.md`
- `src/pyAppGen/pbcs/agri_supply_chain_traceability/README.md`

### Constraints

- Keep AppGen-X terminology.
- Stay inside package-local logic and the assigned test file.
- Do not add new dependencies.
- Keep datastore assumptions to PostgreSQL, MySQL, or MariaDB only.
- Preserve owned-table boundaries and avoid foreign-table mutation.

### Verification Plan

- Run targeted pytest for the assigned implementation test file.
- Run the existing agri supply chain runtime test to ensure the slice does not regress current contracts.
- Review modified code for accidental scope expansion or debug leftovers.
