# Actuarial Pricing and Reserving PBC

This PBC owns actuarial pricing, assumption governance, experience studies,
loss triangles, reserve estimation, rollforwards, and release evidence for an
insurance or risk-bearing business line. It is implemented as a composable
AppGen-X package with its own datastore boundary, AppGen-X event contract,
runtime contracts, workbench UI fragments, governed agent surface, and focused
actuarial calculation engine.

## Owned Business Surface

- Rating model version governance, approval gating, active model selection, and
  effective-date control.
- Rating factor libraries with required inputs, allowed values, relativities,
  defaults, minimum premium handling, additive adjustments, and override
  evidence.
- Premium calculation traces that reconstruct every factor step for audit,
  agent review, and user-facing workbench inspection.
- Actuarial assumption registry selection by assumption type, active state,
  approval evidence, and effective date.
- Assumption change impact analysis across exposure bases with materiality
  detection and approval routing evidence.
- Experience study validation across cohort, exposure basis, period basis, data
  vintage, completeness, timeliness, and quality score floors.
- Loss development triangle governance, missing-cell detection, negative-cell
  rejection, volume-weighted development factor calculation, chain-ladder
  reserve estimation, expected-loss reserve estimation, and reserve rollforward
  variance checks.

## Runtime and Composition

The generated runtime exposes owned tables, migrations, models, service
contracts, route contracts, event outbox/inbox/dead-letter contracts,
permissions, workbench descriptors, document-instruction parsing, and release
evidence. Ordinary datastore backends remain limited to PostgreSQL, MySQL, and
MariaDB. Ordinary eventing uses the AppGen-X event contract and does not expose
stream-engine choices to users.

The executable actuarial engine in `actuarial_engine.py` is side-effect-free.
It returns evidence dictionaries that can be composed into generated services,
UI panels, agent previews, and release audits without mutating policy, claims,
ledger, investment, reinsurance, or external analytics systems.

## Agent and UI Behavior

The PBC contributes an assistant panel and workbench descriptors for guided
pricing, assumption, experience study, and reserving workflows. Agent actions
must preview the governed operation, show calculation evidence, require
authorization where approval or materiality rules apply, and write only through
this PBC's service layer and owned tables.

## Verification

Focused implementation tests cover rating model activation and selection,
premium trace calculation, invalid factor rejection, assumption selection,
assumption impact analysis, experience study quality checks, loss triangle
governance, development factors, chain-ladder reserving, expected-loss
reserving, and reserve rollforward evidence.

