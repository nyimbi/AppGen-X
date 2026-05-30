# Facility Energy Management PBC

`facility_energy_management` is a standalone AppGen-X PBC for campus and portfolio energy operations. It owns meter and submeter topology, interval load profiles, tariffs, HVAC and equipment schedules, demand response, optimization handoffs, weather-normalized baselines, anomaly investigation, comfort and safety controls, and governed assistant support.

## Owned Scope

- Tables for meters, interval profiles, equipment schedules, demand response events, optimization plans, tariff signals, energy baselines, policy rules, runtime parameters, schema extensions, control assertions, governed models, outbox, inbox, and dead letters.
- PostgreSQL, MySQL, and MariaDB datastore targets only.
- AppGen-X event contract only; no stream-engine picker is exposed.
- Cross-PBC dependencies are represented through events and APIs, never shared tables.

## Standalone Application Surface

`FacilityEnergyManagementStandaloneApp` proves the PBC can run as the only package in an application. The demo flow configures runtime parameters and rules, commissions main/floor/tenant/life-safety meters, records interval reads, creates tariff signals and HVAC schedules, approves weather-normalized baselines, blocks unsafe critical-load curtailment, dispatches and settles demand response, produces approval-gated optimization recommendations, opens anomaly case packs, and generates assistant CRUD previews that require confirmation.

## UI, Wizards, and Controls

The PBC exposes domain-specific forms for meter topology, interval imports, tariffs, HVAC schedules, demand response, baselines, and guardrails. Guided wizards cover meter commissioning, interval correction, tariff comparison, demand response dispatch/settlement, anomaly investigation, and baseline versioning. Continuous controls cover meter health, rollup residuals, interval quality, tariff calendars, schedule conflicts, critical loads, comfort/safety guardrails, baseline overlap, demand-response state, and agent mutation governance.

## Agent Skills

The PBC contributes `facility_energy_management_skills` to the composed application agent. The assistant can explain energy workflows, interpret utility bills or tenant comfort instructions, preview bounded CRUD changes, and reject foreign-table mutations.

## Verification

- `PYTHONPATH=src python3 -m compileall -q src/pyAppGen/pbcs/facility_energy_management`
- `PYTHONPATH=src ./.venv/bin/pytest -q src/pyAppGen/pbcs/facility_energy_management/tests`
- `standalone_smoke_test()` and `validate_release_evidence()`
- focused PBC source, package-local, specification, agent, implementation, capability, and generation audits where available
