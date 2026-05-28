# Donor Grant Fundraising Implementation Status

## Status

Implemented for the current pass.

## Completed

- Added `fundraising_app.py` with executable donor, campaign, pledge, gift, restriction, grant, stewardship, workbench, assistant-routing, and single-PBC app logic.
- Added forms, wizards, controls, workbench queues, stable document mutation plans, and AppGen-X event outbox evidence.
- Wired the service layer to execute stateful app commands and workbench queries.
- Extended runtime capabilities and release evidence with the single-PBC app surface.
- Expanded the owned-table contract to include relationship, proposal, acknowledgement, briefing, opportunity score, review chain, and budget validation records.
- Added package-local tests for the standalone app surface, prospect pipeline, gift/pledge/campaign matching, restriction and grant controls, stewardship queues, assistant routing, service state, and smoke flow.

## Verification

- `python3 -m py_compile src/pyAppGen/pbcs/donor_grant_fundraising/*.py src/pyAppGen/pbcs/donor_grant_fundraising/tests/*.py`
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/donor_grant_fundraising/tests`

## Remaining Risks

- Package tests prove deterministic business behavior, but do not open a browser against a generated app.
- Future passes should add richer donor household graph operations, proposal document rendering, tax receipting rules by jurisdiction, and external payment/import projections through API/event contracts.
