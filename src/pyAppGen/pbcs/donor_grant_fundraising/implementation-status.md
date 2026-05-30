# Donor Grant Fundraising Implementation Status

## Status

Implemented for the standalone PBC pass.

## Completed

- Added a package-local `standalone.py` shell with configuration bootstrap, default rules and parameters, demo seed data, governed document intake, CRUD previews, workbench rendering, and standalone smoke coverage.
- Expanded `fundraising_app.py` so the owned relationship, proposal workspace, acknowledgement, briefing packet, opportunity score, review chain, and budget validation tables are executable domain surfaces instead of inert declarations.
- Aligned runtime, domain-depth, service, route, schema, and migration contracts around the same owned table names and public routes.
- Added public route coverage for grant applications and stewardship touchpoints.
- Strengthened assistant skill metadata, workbench queues, release evidence, and package metadata so they reflect the actual standalone shell.
- Added focused tests for schema and route alignment, richer fundraising domain flows, and the standalone application shell.

## Verification

- `python3 -m py_compile src/pyAppGen/pbcs/donor_grant_fundraising/*.py src/pyAppGen/pbcs/donor_grant_fundraising/tests/*.py`
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/donor_grant_fundraising/tests`
- `PYTHONPATH=src python3 - <<'PY' ... standalone_smoke_test() ... PY`

## Remaining Risks

- The package proves standalone behavior in-process; it does not launch a browser or generated app shell.
- The route layer remains package-local and synthetic; a future pass could bind these contracts into the higher-level HTTP generator once shared-generator work is allowed.
- The migration is contract-aligned and domain-specific, but not yet exercised against a live database engine in this isolated PBC-only pass.

## 2026-05-30 improve1 Fundraising-Control Execution Slice

- Added `fundraising_control.py` as the side-effect-free executable proof layer for all 50 donor grant fundraising improve1 backlog items.
- Bound each feature to owned donor, campaign, pledge, gift, restriction, grant, stewardship, proposal, acknowledgement, review, budget, policy, control, event, and model tables plus UI fragments, service/API routes, permissions, agent skills, configuration guardrails, retry/dead-letter evidence, and release evidence.
- Wired fundraising controls into runtime capabilities, runtime smoke, release evidence, UI contracts, traceability artifacts, and focused package tests.
