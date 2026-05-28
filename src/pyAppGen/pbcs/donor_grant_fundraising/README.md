# Donor Grant Fundraising PBC

`donor_grant_fundraising` is a standalone AppGen-X Packaged Business Capability for advancement, fundraising, grants, restrictions, stewardship, and impact operations.

When composed by itself, it provides a working domain application: users can configure the package, manage donors and prospects, run campaigns, create pledges, post gifts, enforce restrictions, manage grant submissions, coordinate stewardship, open workbench queues, and use the PBC assistant for governed document intake and task guidance.

## Owned Boundary

The PBC owns only `donor_grant_fundraising_*` tables. It covers donors, campaigns, pledges, gifts, restrictions, grant applications, stewardship touchpoints, donor relationships, proposal workspaces, acknowledgements, briefing packets, opportunity scores, review chains, budget validations, governance records, and AppGen-X inbox/outbox/dead-letter events.

Ordinary database backends are limited to PostgreSQL, MySQL, and MariaDB. Eventing uses the AppGen-X event contract with no user-facing stream-engine picker.

## Executable Capabilities

- Register donor profiles for individual, household, corporate, and foundation donors.
- Advance prospects through researched, qualified, assigned, cultivated, solicitation-ready, and converted stages with evidence gates.
- Model campaign hierarchies, objectives, goals, donor segments, windows, and gift-counting rules.
- Create pledges with installment schedules, reminder dates, amendments, balance tracking, and lifecycle states.
- Post gifts against donors, campaigns, pledges, appeals, restrictions, receipt status, and posting dates.
- Enforce restriction type, purpose, geography, time window, beneficiary class, approvals, release conditions, and sunset logic.
- Manage grant opportunities through qualification, drafting, review, submission, award setup, and post-award stewardship.
- Record stewardship playbooks, acknowledgement status, cadence gaps, touchpoint outcomes, and next ask readiness.
- Build portfolio, pledge exposure, acknowledgement, grant risk, stewardship, campaign performance, and exception queues.

## UI and Assistant

The PBC exposes forms for donor profiles, prospect stages, campaign hierarchy, pledge installments, gift posting, restriction rules, grant applications, and stewardship touchpoints.

It exposes wizards for donor conversion, major gifts, restriction setup, grant submission, post-award setup, and first-run single-PBC launch.

The assistant contributes PBC-scoped skills to the composed single agent. It routes grant guidelines, pledge documents, gift letters, restriction instructions, campaign appeals, stewardship notes, and donor correspondence into mutation previews with stable digests, citations required, AppGen-X event evidence, and human confirmation before datastore changes.

## Release Evidence

Release evidence covers schema, migrations, models, services, APIs, events, handlers, UI, forms, wizards, controls, assistant skills, governance, retry/dead-letter behavior, and the single-PBC app smoke test.

Run package checks with:

```bash
python3 -m py_compile src/pyAppGen/pbcs/donor_grant_fundraising/*.py src/pyAppGen/pbcs/donor_grant_fundraising/tests/*.py
./.venv/bin/pytest -q src/pyAppGen/pbcs/donor_grant_fundraising/tests
```
