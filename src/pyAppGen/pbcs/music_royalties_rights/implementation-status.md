# music_royalties_rights implementation status

## Improve1 executable controls

- Status: implemented for 50 of 50 improve1 backlog features.
- Control module: `royalties_rights_control.py`.
- Runtime wiring: `music_royalties_rights_runtime_capabilities()` exposes `royalties_rights_control` and `evaluate_royalties_rights_control`.
- UI wiring: `music_royalties_rights_ui_contract()` and `music_royalties_rights_render_workbench()` expose 50 royalties-specific control panels, service actions, and agent tools.
- Release evidence: `validate_release_evidence()` includes the royalties control contract and blocks on any failed improve1 control.
- Tests: `tests/test_domain_behavior.py` validates ownership, AppGen-X eventing, database backend allowlist, projection-only dependencies, human approval gates, agent preview gates, non-mutating simulations, and domain proof gates.

## Domain surface covered

The controls cover repertoire identity, contributor and publisher chains, split versioning, recording linkage, neighboring rights, PRO/CMO affiliation, licensing, usage ingestion, statement calculation, recoupment, reserves, deductions, beneficiary controls, tax withholding, disputes, restatements, catalog administration, registrations, evidence packages, event replay, repertoire UI, statement explainers, dispute cockpit, agent skills, leakage scoring, seeded release scenarios, schema expansion, policy packs, audit proofs, and go-live scorecards.

## Boundary assertions

- Database backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X on `pbc.music_royalties_rights.events`.
- No stream-engine picker is exposed.
- Cross-PBC facts are represented through declared APIs, events, or projections, not shared table mutation.
- All control evaluations are side-effect free and return release evidence.
