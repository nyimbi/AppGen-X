# Enterprise PIM PBC

The `enterprise_pim` package owns enterprise product-information governance for taxonomies, attributes, localized content, validation workflow, dependency intake, and publication evidence. It is implemented as a side-effect-free AppGen-X PBC package under `src/pyAppGen/pbcs/enterprise_pim`.

## Owned Boundary

Owned tables:

- `product_taxonomy`
- `product_attribute`
- `localized_content`
- `validation_workflow`

The PBC does not share tables with catalog, commerce, content, pricing, tax, or inventory PBCs. It consumes declared AppGen-X events and dependency schemas into package-owned inbox/projection state, then emits its own outbox events.

Allowed database backends are PostgreSQL, MySQL, and MariaDB. Eventing is fixed to the AppGen-X event contract on `appgen.enterprise-pim.events`; the runtime rejects stream-engine picker fields.

## Standard Capabilities

- Enterprise taxonomy creation and graph lineage.
- Product attribute definition, typed validation, inheritance, localized overrides, and schema evolution evidence.
- Multilingual localized content with locale fallback and quality scoring.
- Validation workflow start, approval, rejection, SLA, and control evidence.
- Schema-accepted dependency handling for media, pricing, tax, inventory, search, and catalog projection events.
- Configuration schema, bounded parameter engine, compiled rule engine, seed data, RBAC descriptors, API surfaces, and workbench UI fragments.
- AppGen-X outbox/inbox, idempotent handlers, retry and dead-letter records.

## Advanced Capabilities

- Event-sourced PIM mutations with immutable hash-chain evidence.
- Graph-relational taxonomy and attribute inheritance topology.
- Probabilistic completeness, localization, compliance, and workflow risk scoring.
- Counterfactual taxonomy/locale publication simulation.
- Temporal enrichment readiness forecasting.
- Autonomous enrichment exception recommendation.
- Semantic enrichment instruction parsing.
- Self-healing dependency route selection.
- Cryptographic master-data proof generation and crypto-agile epoch rotation.
- Dynamic policy screening, automated control tests, stochastic exposure modeling, anomaly detection, and governed model metadata.

## UI

The package exports `enterprise_pim_ui_contract()` and `enterprise_pim_render_workbench()`. The workbench exposes taxonomy, attribute, localization, workflow, dependency, event, rule, parameter, configuration, and audit panels with RBAC-bound visible actions.
