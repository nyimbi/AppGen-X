# Composable PBC Applications

AppGen-X supports composable enterprise applications through a catalog of
Packaged Business Capabilities (PBCs). A PBC is a selectable business slice with
its own datastore boundary, business API, event contracts, generated tables,
and deployment unit. Users should be able to choose individual PBCs or starter
stacks, then generate a working application shell from the composition.

## Design Rules

- Each PBC owns its datastore. Cross-PBC reads use APIs, projections, or event
  subscriptions instead of shared tables.
- Each ordinary PBC declares an approved open-source relational datastore
  backend: PostgreSQL, MySQL, or MariaDB. Built-in PBCs default to PostgreSQL.
- Each PBC declares command APIs and emitted/consumed events.
- Ordinary PBCs do not choose a stream processor. They have one visible
  developer choice: use the generated AppGen-X event contract. They omit
  `stream_processor`, generate the platform outbox/inbox and event-handler
  contracts, and let validation normalize the runtime profile behind the
  adapter. `quix_streams` is allowed only for telemetry, time-series, large
  ingestion, or windowed metrics with `stream_exception_evidence`; `bytewax` is
  allowed only for complex parallel dataflow or CPU-heavy transformations with
  the same evidence. Generated business logic should use the platform adapter,
  not profile-specific client code. The canonical policy is exposed by
  `acp_stream_processing_policy()` and documented in
  [Opinionated Event Processing Guidance](kafka-alternatives.md).
- Composition is event-first: dependencies are explicit event contracts, with
  unresolved external events recorded as integration obligations.
- Generated applications include one implementation directory per selected PBC:
  `app/pbcs/<pbc_key>/`. Each directory contains the PBC manifest, owned model
  metadata, migration SQL, service commands, API routes, event contracts,
  idempotent handlers, UI/workbench metadata, permissions, configuration,
  seed data, contract tests, and release evidence.
- Each generated PBC also carries an executable domain-depth contract. The
  contract proves capability modules, workflow implementations, policy controls,
  automation loops, analytics, integration contracts, workbench actions, and
  release gates for the selected domain. This is the AppGen-X bar for replacing
  broad enterprise-suite footprints with composable, owned capabilities.
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
- `load_pbc_package()` and `discover_pbc_packages()` for loading package
  entrypoints from local source directories or importable modules.
- `pbc_package_index_schema()` and `discover_pbc_package_index()` for loading
  reusable package catalogs without mutating the built-in catalog.
- `pbc_selection_from_prompt()` for natural-language PBC selection.
- `pbc_composition_plan()` for datastore, API, event, and dependency evidence.
- `pbc_composition_dsl()` for a generated AppGen DSL starter.
- Generated `pbc_runtime.py` in produced apps for catalog, selected-service,
  self-registration, composition workbench, and stream-policy smoke evidence.
- `pbc_implementation_contract()` and `pbc_implementation_release_audit()` for
  concrete per-PBC implementation evidence and ownership checks.
- `pbc_release_audit()` for package-level readiness evidence.

The aggregate package goal audit includes the PBC release audit, so composable
applications remain part of the platform's verified surface.

For third-party or agent-built PBCs, follow the detailed
[PBC Specification](pbc-specification.md). A usable PBC package must expose a
`register_pbc()` entrypoint, pass manifest validation, and include docs/tests
before it is published as reusable catalog content.
