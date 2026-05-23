# Composable PBC Applications

AppGen-X supports composable enterprise applications through a catalog of
Packaged Business Capabilities (PBCs). A PBC is a selectable business slice with
its own datastore boundary, business API, event contracts, generated tables,
and deployment unit. Users should be able to choose individual PBCs or starter
stacks, then generate a working application shell from the composition.

## Design Rules

- Each PBC owns its datastore. Cross-PBC reads use APIs, projections, or event
  subscriptions instead of shared tables.
- Each PBC declares an approved open-source datastore backend. Built-in PBCs
  default to PostgreSQL; third-party PBCs may use PostgreSQL, MySQL, MariaDB,
  SQLite, DuckDB, ClickHouse, MongoDB, or OpenSearch.
- Each PBC declares command APIs and emitted/consumed events.
- Event-heavy PBCs declare one Python-native stream processor profile. The
  default is `faust_streaming`. Use `quix_streams` only for high-throughput
  event/time-series workloads, and use `bytewax` only for complex parallel
  dataflow transformations. The canonical policy is exposed by
  `acp_stream_processing_policy()` and documented in
  [Opinionated Event Processing Guidance](kafka-alternatives.md).
- Composition is event-first: dependencies are explicit event contracts, with
  unresolved external events recorded as integration obligations.
- Generated applications include service folders, outbox tables, workbench
  views, target selection, and release-audit evidence.
- Natural-language requests can resolve to PBC selections before generation.

## Meshes

The catalog is grouped into five enterprise meshes:

- Financial Operations: ledger, payable, receivable, treasury, assets, and tax.
- Supply Chain and Logistics: inventory state, warehouse, procurement, and
  transportation.
- Human Capital Management: personnel, time, payroll, and onboarding.
- Operations and Manufacturing: planning, production, quality, and assets.
- Commerce and Customer Experience: order management, product information, and
  customer engagement.

## User Flow

1. Select PBCs from the IDE catalog or choose a recommended stack.
2. Review each selected PBC's owned datastore, APIs, events, and tables.
3. Review dependency links and external event obligations.
4. Generate DSL, app code, target packages, and release evidence.
5. Iterate through natural language, DSL editing, or visual composition.

## Runtime Contract

The executable catalog lives in `src/pyAppGen/pbc.py` and exposes:

- `pbc_mesh_catalog()` for the five domain groups.
- `pbc_catalog()` for selectable bounded contexts.
- `pbc_starter_stacks()` for reusable enterprise starter compositions.
- `pbc_manifest_schema()` for the self-registering PBC manifest contract.
- `validate_pbc_manifest()` for package validation before registration.
- `register_pbc_manifest()` for a side-effect-free registration plan.
- `pbc_package_contract()` for installable package metadata.
- `pbc_selection_from_prompt()` for natural-language PBC selection.
- `pbc_composition_plan()` for datastore, API, event, and dependency evidence.
- `pbc_composition_dsl()` for a generated AppGen DSL starter.
- Generated `pbc_runtime.py` in produced apps for catalog, selected-service,
  self-registration, composition workbench, and stream-policy smoke evidence.
- `pbc_release_audit()` for package-level readiness evidence.

The aggregate package goal audit includes the PBC release audit, so composable
applications remain part of the platform's verified surface.

For third-party or agent-built PBCs, follow the detailed
[PBC Specification](pbc-specification.md). A usable PBC package must expose a
`register_pbc()` entrypoint, pass manifest validation, and include docs/tests
before it is published as reusable catalog content.
