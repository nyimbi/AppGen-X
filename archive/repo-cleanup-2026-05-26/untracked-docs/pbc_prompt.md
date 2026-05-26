  You are working in the AppGen-X codebase. Your task is to fully implement the Packaged Business Capability system, not merely document or catalog it.

  Start by reading:
  - AGENTS.md
  - README.md
  - docs/composable-pbc-apps.md
  - docs/pbc-specification.md
  - docs/apc-components.md
  - docs/kafka-alternatives.md
  - docs/active-goal-progress.md
  - src/pyAppGen/pbc.py
  - src/pyAppGen/gen.py
  - tests/test_main.py

  Important constraints:
  - Treat the current worktree as authoritative.
  - Do not overwrite unrelated dirty files.
  - Do not introduce banned legacy product/framework names; use AppGen-X terminology already present in the repo.
  - Backends for ordinary PBCs must remain limited to PostgreSQL, MySQL, or MariaDB.
  - Ordinary PBC eventing must use the AppGen-X event contract. Do not expose stream-engine pickers to users.
  - Commit regularly using the repository’s Lore commit protocol.
  - Keep docs/active-goal-progress.md updated with concrete progress and commit hashes.

  Goal:
  Turn the existing PBC catalog into a complete, usable PBC implementation system. A PBC must be a real composable business package with owned schema, migrations, models, services, APIs, events,
  handlers, UI fragments, generated DSL, tests, package metadata, self-registration, and release evidence.

  Current executable source of truth:
  - src/pyAppGen/pbc.py contains the PBC catalog, manifests, validation, registration, package loading, prompt selection, composition plans, DSL generation, release audits, and generation smoke
  audits.
  - src/pyAppGen/gen.py generates application code and app-local pbc_runtime.py.
  - tests/test_main.py already verifies catalog, manifests, selection, composition, generated runtime, and release audit behavior.

  Implement in slices. For each slice:
  1. Inspect existing implementation and tests.
  2. Add missing real implementation, not just placeholder evidence.
  3. Add focused tests proving the behavior.
  4. Run focused tests and relevant smoke audits.
  5. Update docs/active-goal-progress.md.
  6. Commit and push.

  Definition of “complete PBC”:
  Each built-in PBC must have:
  - Stable `pbc` key and manifest.
  - Mesh assignment.
  - Owned datastore boundary.
  - Tables with fields and relationships.
  - Generated migrations/schema artifacts.
  - Generated models.
  - Service layer with command methods.
  - API route definitions.
  - Event outbox/inbox contracts.
  - Typed emitted and consumed events.
  - Idempotent handlers.
  - Retry/dead-letter evidence.
  - UI fragments or workbench views where applicable.
  - Permissions/RBAC descriptors.
  - Configuration schema.
  - Seed data where useful.
  - Package registration metadata.
  - Release-audit evidence.
  - Unit tests and generation smoke tests.

  Start with the 46 PBCs currently in `PBC_CATALOG`:
  - gl_core
  - ap_automation
  - ar_credit
  - treasury_cash
  - asset_lifecycle
  - tax_localization
  - inventory_positioning
  - wms_core
  - procurement_sourcing
  - transportation_management
  - personnel_identity
  - time_labor
  - payroll_engine
  - talent_onboarding
  - mrp_engine
  - production_control
  - quality_assurance
  - eam
  - dom
  - product_catalog_pim
  - customer_360
  - federated_iam
  - api_gateway_mesh
  - schema_registry
  - workflow_orchestration
  - audit_ledger
  - composition_engine
  - global_inventory_visibility
  - order_routing_optimization
  - checkout_processing
  - payment_orchestration
  - subscription_billing
  - returns_reverse_logistics
  - cross_border_trade
  - enterprise_pim
  - dam_core
  - price_promotion_engine
  - lead_opportunity
  - service_ticketing
  - notifications
  - cdp_segmentation
  - loyalty_rewards
  - streaming_analytics
  - enterprise_search_vector
  - predictive_demand
  - fraud_anomaly_detection

  Prioritize implementation order:
  1. Platform fabric PBCs: identity, gateway, schema registry, workflow, audit ledger, composition engine.
  2. Financial core: GL, AP, AR, treasury, tax, asset lifecycle.
  3. Supply chain/order flow: inventory, WMS, procurement, transportation, DOM.
  4. HCM and payroll.
  5. Manufacturing.
  6. Commerce, content, relationship, and intelligence PBCs.
  7. Package/index/discovery flow for external PBCs.

  Acceptance criteria:
  - `pbc_release_audit()` passes.
  - A generation smoke audit passes for every built-in PBC, not just a sample.
  - Generated apps include working `app/pbc_runtime.py`.
  - Generated apps include PBC-owned models, services, routes, event contracts, and UI/workbench artifacts.
  - Self-registering PBC packages validate and produce side-effect-free registration plans.
  - Cross-PBC dependencies are represented through APIs/events/projections, not shared tables.
  - Natural-language prompts can select relevant PBCs and generate a valid composition DSL.
  - Tests prove that each generated PBC references only its own owned tables plus declared API/event dependencies.
  - Docs explain how to build, test, package, register, and compose PBCs.

  Do not stop after adding catalog entries or documentation. The end state is a working Application Composition Platform where users can select PBCs and generate functioning applications from them.