# nonprofit_program_impact implementation status

## Improve1 executable controls

- Status: implemented for 50 of 50 improve1 backlog features.
- Control module: `impact_control.py`.
- Runtime wiring: `nonprofit_program_impact_runtime_capabilities()` exposes `impact_control` and `evaluate_impact_control`.
- UI wiring: `nonprofit_program_impact_ui_contract()` and `nonprofit_program_impact_render_workbench()` expose 50 nonprofit-impact control panels, service actions, and agent tools.
- Release evidence: `validate_release_evidence()` includes the impact control contract and blocks on failed improve1 controls.
- Tests: `tests/test_domain_behavior.py` validates ownership, AppGen-X eventing, database backend allowlist, projection-only dependencies, human approval gates, agent preview gates, non-mutating simulations, and sensitive impact evidence gates.

## Domain surface covered

The controls cover theory of change, results chains, beneficiary and cohort modeling, eligibility, intervention taxonomy, dosage and fidelity, outputs, outcomes, indicators, baselines and targets, surveys, sampling, consent, safeguarding, referrals, qualitative evidence, partner delivery, grant restrictions, donor attribution and freeze controls, equity disaggregation, longitudinal follow-up, negative outcomes, comparison groups, geography, dashboards, program and beneficiary UI, donor review, assistant skills, domain events, lineage, consumed-event effects, partner scorecards, release evidence, exception taxonomy, retention, access control, predictive risk, simulations, offline sync, localization, accessibility, fixtures, and go-live gates.

## Boundary assertions

- Database backends remain limited to PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X on `pbc.nonprofit_program_impact.events`.
- No stream-engine picker is exposed.
- Cross-PBC facts are represented through declared APIs, events, or projections, not shared table mutation.
- All control evaluations are side-effect free and return release evidence.
