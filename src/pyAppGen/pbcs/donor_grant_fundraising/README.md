# Donor Grant Fundraising PBC

`donor_grant_fundraising` is a standalone AppGen-X Packaged Business Capability for advancement, fundraising, grants, restrictions, stewardship, and impact operations.

When selected as the only PBC, it now exposes a package-local standalone operating shell with owned schema, migrations, models, services, API routes, AppGen-X events, handlers, UI workbench surfaces, governed assistant skills, default rules and parameters, demo seed data, and focused package tests.

## Owned Boundary

The PBC owns only `donor_grant_fundraising_*` tables. It covers donors, campaigns, pledges, gifts, restrictions, grant applications, stewardship touchpoints, donor relationships, proposal workspaces, acknowledgements, briefing packets, opportunity scores, review chains, budget validations, governance records, and AppGen-X inbox/outbox/dead-letter events.

Ordinary database backends are limited to PostgreSQL, MySQL, and MariaDB. Eventing uses the AppGen-X event contract with no user-facing stream-engine picker.

## Executable Capabilities

- Register donor profiles for individual, household, corporate, and foundation donors.
- Advance prospects through researched, qualified, assigned, cultivated, solicitation-ready, and converted stages with evidence gates.
- Model campaign hierarchies, objectives, goals, donor segments, windows, and gift-counting rules.
- Create pledges with installment schedules, reminder dates, amendments, balance tracking, and lifecycle states.
- Post gifts against donors, campaigns, pledges, appeals, restrictions, receipt status, and posting dates.
- Enforce restriction type, purpose, geography, time window, approval, and release rules.
- Manage grant opportunities through qualification, proposal readiness, review, submission, award setup, and post-award stewardship.
- Operate proposal workspaces, acknowledgement queues, relationship maps, executive briefing packets, opportunity scoring, review chains, and grant budget validation.
- Build portfolio, pledge exposure, acknowledgement, proposal readiness, grant risk, review blocker, stewardship, campaign performance, and exception queues.

## Standalone App Shell

`standalone.py` provides `DonorGrantFundraisingStandaloneApplication`, which bootstraps defaults, seeds demo donor/campaign/restriction data, runs package-local command flows, exposes document intake and CRUD preview helpers, and renders a one-PBC workbench without touching shared generator code.

## UI and Assistant

The PBC exposes forms for donor profiles, prospect stages, campaigns, pledges, gifts, restrictions, grant applications, stewardship touchpoints, donor relationships, proposal workspaces, acknowledgements, review chains, and budget validations.

It exposes guided wizards for donor conversion, major gifts, restriction setup, grant submission, post-award setup, executive briefings, and first-run single-PBC launch.

The assistant contributes PBC-scoped proposal-support, stewardship-drafting, mutation-preview, and operator-guidance skills. It routes donor letters, gift documents, pledge instructions, restrictions, campaign appeals, stewardship notes, board packets, and grant guidelines into stable mutation previews with citations required, AppGen-X event evidence, and human confirmation before datastore changes.

## Release Evidence

Release evidence covers schema, migrations, models, services, API routes, events, handlers, UI, forms, wizards, controls, assistant skills, governance, retry/dead-letter behavior, the executable standalone shell, and the single-PBC app smoke tests.

Run package checks with:

```bash
python3 -m py_compile src/pyAppGen/pbcs/donor_grant_fundraising/*.py src/pyAppGen/pbcs/donor_grant_fundraising/tests/*.py
./.venv/bin/pytest -q src/pyAppGen/pbcs/donor_grant_fundraising/tests
PYTHONPATH=src python3 - <<'PY'
from pyAppGen.pbcs.donor_grant_fundraising.standalone import standalone_smoke_test
print(standalone_smoke_test()["ok"])
PY
```
