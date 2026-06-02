# Master Data Governance Release Evidence

This package now contains a package-local standalone one-PBC app for master data governance in `standalone.py`. The executable slice is scoped entirely to `src/pyAppGen/pbcs/master_data_governance` and owns its own forms, wizards, controls, UI/workbench wiring, SQLite-backed owned tables, route dispatch, seed bundle, agent planning surface, and focused tests.

## Evidence

- Owned persistence is package-local and restricted to `master_data_governance_` tables plus package outbox/inbox/dead-letter tables.
- The standalone route surface covers domain registry, source intake, dedupe match candidates, merge decisions, survivorship rules, golden records, quality rules, remediation queue, hierarchy nodes, reference data, lineage links, policy approvals, audit proofs, agent planning, and workbench queries.
- UI/workbench wiring is grounded in standalone forms, wizards, controls, and navigation contracts instead of generator-only placeholders.
- AI agent planning is executable through document/instruction and CRUD preview functions that only target owned tables and always require confirmation for mutation paths.
- Seed bundle execution creates a realistic MDM slice spanning domain setup, source intake, match/merge, survivorship, golden record publication, stewardship, quality, hierarchy, reference data, lineage, policy approval, and audit proof.
- Release readiness is executable through `release_evidence.py`, standalone smoke functions, and focused package tests under `tests/test_contract.py` and `tests/test_standalone_app.py`.
