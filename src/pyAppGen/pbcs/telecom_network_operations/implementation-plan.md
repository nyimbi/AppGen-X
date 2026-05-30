# Telecom Network Operations Implementation Plan

## Intent

Turn `telecom_network_operations` from a generated package contract into a standalone, one-PBC network operations application. The implementation must let a composed app run this PBC by itself for NOC inventory, alarm, outage, assurance, capacity, maintenance, SLA, and assistant workflows while preserving AppGen-X composition boundaries.

## Domain Scope From `improve1.md`

The improvement backlog calls for deep coverage across site hierarchy, radio identity, circuit and fiber topology, alarm normalization, root-cause correlation, owned trouble tickets, planned work, outage lifecycle, SLA clocks, capacity and KPI baselines, NOC workbench queues, topology UI, field evidence, typed events, replay safety, and AI assistant skills. This slice implements an executable representative surface for those requirements using the current owned tables as the package boundary.

## Implementation Steps

1. Add package-local `forms.py`, `wizards.py`, and `controls.py` for site, cell, circuit/fiber, alarm, outage, SLA, capacity, maintenance, field evidence, and assistant workflows.
2. Add `standalone.py` with `TelecomNetworkOperationsStandaloneApp`, side-effect-free state, domain command methods, scenario simulation, and a `single_pbc_app_contract()`.
3. Wire the standalone app into `__init__.py`, `manifest.py`, and `release_evidence.py` without modifying shared generator or language files.
4. Add focused tests in `tests/test_standalone.py` proving guarded workflows, UI/forms/wizards/controls, database/event policies, and assistant confirmation behavior.
5. Write `README.md` explaining how the PBC works, its boundary, UI, APIs, events, assistant skills, and verification.
6. Perform code review after implementation, resolve emergent issues, and record evidence in `implementation-status.md`.

## Acceptance Gates

- Compile succeeds for `src/pyAppGen/pbcs/telecom_network_operations`.
- PBC-local tests pass.
- `git diff --check` is clean for the PBC directory.
- Focused source/package/spec/agent/implementation/capability/generation audits pass for `telecom_network_operations`.
- No stream-engine picker is exposed; ordinary database backends remain PostgreSQL, MySQL, and MariaDB.
