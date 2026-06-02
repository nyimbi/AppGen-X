PBC Completion Standard

  A complete AppGen-X PBC is a standalone business application package, not a catalog entry. If an app is generated with only one PBC, it must still provide useful domain functionality: owned
  database schema, migrations, models, services, API routes, events, handlers, forms, wizards, controls, workflows, rules, parameters, configuration, permissions, seed data, release evidence, tests,
  and an AI agent/chatbot surface.

  Required Package Shape

  Each PBC directory should contain:

  README.md
  SPECIFICATION.md
  implementation-plan.md
  implementation-status.md
  RELEASE_EVIDENCE.md
  __init__.py
  manifest.py
  runtime.py
  models.py
  schema_contract.py
  service_contract.py
  services.py
  routes.py
  events.py
  handlers.py
  ui.py
  agent.py
  config.py
  permissions.py
  seed_data.py
  release_evidence.py
  capability_assurance.py
  migrations/001_initial.sql
  tests/__init__.py
  tests/test_contract.py

  Optional but useful: blueprint.py, domain_depth.py, standalone.py, workflows.py, rules.py, analytics.py, and focused tests such as tests/test_standalone.py.

  Implementation Rules

  Work in a dedicated worktree and branch per PBC:

  pbc/<pbc-key>-standalone

  Only edit:

  src/pyAppGen/pbcs/<pbc_key>

  Read improve1.md first, then write a hand-curated implementation-plan.md. Do not mechanically copy another PBC. The plan must define the domain surface, table-stakes capabilities, advanced
  capabilities, owned data model, workflows, UI, agent skills, events, release gates, and tests.

  Core Interfaces

  __init__.py must expose side-effect-free package functions:

  def implementation_contract() -> dict: ...
  def register_pbc() -> dict: ...
  def registration_plan(existing_catalog: dict | None = None) -> dict: ...
  def package_metadata_manifest() -> dict: ...
  def validate_package_metadata() -> dict: ...
  def package_discovery_plan(existing_catalog: dict | None = None) -> dict: ...
  def smoke_test() -> dict: ...

  The package must not mutate global state, create tables, write files, start servers, or open network connections at import time.

  Domain Depth

  For the assigned domain, implement the real professional operating surface:

  - Master data and transaction data.
  - Main lifecycle states.
  - Normal workflows.
  - Exception workflows.
  - Approval, reversal, cancellation, correction, and reopening flows.
  - Rules, parameters, configuration, and policy enforcement.
  - Audit and release evidence.
  - Analytics and operational dashboards.
  - Domain-specific edge cases.
  - Credible advanced capabilities.

  “World-class” means the PBC covers the domain deeply with executable behavior and testable contracts, not exaggerated claims.

  Database Boundary

  All owned tables must be prefixed:

  <pbc_key>_<logical_table>

  A PBC may depend on other PBCs only through APIs, AppGen-X events, or owned projections. It must not read or write another PBC’s tables.

  Allowed ordinary backends remain:

  postgresql
  mysql
  mariadb

  Runtime

  runtime.py should provide deterministic executable behavior:

  def <pbc_key>_empty_state() -> dict: ...
  def <pbc_key>_configure_runtime(state: dict, config: dict) -> dict: ...
  def <pbc_key>_set_parameter(state: dict, name: str, value: object) -> dict: ...
  def <pbc_key>_register_rule(state: dict, rule: dict) -> dict: ...
  def <pbc_key>_receive_event(state: dict, event: dict) -> dict: ...
  def <pbc_key>_build_workbench_view(state: dict | None = None, ...) -> dict: ...
  def <pbc_key>_build_schema_contract() -> dict: ...
  def <pbc_key>_build_service_contract() -> dict: ...
  def <pbc_key>_build_api_contract() -> dict: ...
  def <pbc_key>_build_release_evidence() -> dict: ...
  def <pbc_key>_runtime_smoke() -> dict: ...
  def <pbc_key>_runtime_capabilities() -> dict: ...

  Prefer a package-local standalone facade, for example:

  class DomainStandaloneApp:
      def configure_runtime(self, config: dict) -> dict: ...
      def execute(self, operation: str, payload: dict | None = None) -> dict: ...
      def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict: ...
      def render_workbench(self, ...) -> dict: ...

  UI And Agent

  Every PBC must have UI and agent surfaces.

  ui.py must expose forms, wizards, controls, navigation, workbench panels, action permissions, configuration/rule/parameter editors, event surfaces, and release evidence.

  agent.py must expose:

  def agent_skill_manifest() -> dict: ...
  def chatbot_interface_contract() -> dict: ...
  def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict: ...
  def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict: ...
  def composed_agent_contribution() -> dict: ...
  def smoke_test() -> dict: ...

  The agent must reject foreign tables, require confirmation for mutations, map instructions to forms/wizards/services, and contribute skills to the composed application’s single agent.

  Events

  Use only the AppGen-X event contract. Do not expose stream-engine selection.

  Each PBC needs outbox, inbox, dead-letter, typed emitted events, typed consumed events, retry policy, idempotency keys, and idempotent handlers.

  Tests And Gates

  At minimum, package tests should prove:

  - Schema, models, migrations align.
  - Services and routes execute.
  - Event contracts validate.
  - Handlers are idempotent/retryable.
  - UI has forms/wizards/controls.
  - Agent document and CRUD planning works.
  - Rules, parameters, config work.
  - Seed data and permissions work.
  - A realistic one-PBC lifecycle runs.

  Run:

  python3 -m py_compile src/pyAppGen/pbcs/<pbc_key>/*.py src/pyAppGen/pbcs/<pbc_key>/tests/*.py
  ./.venv/bin/pytest -q src/pyAppGen/pbcs/<pbc_key>/tests

  Then verify:

  pbc_specification_contract(key)["ok"]
  pbc_source_artifact_contract(key)["ok"]
  pbc_implementation_release_audit((key,))["ok"]
  pbc_generation_smoke_audit((key,))["ok"]

  Definition Of Done

  A PBC is ready when it has a domain-specific plan, implementation, README, status file, owned schema/models/migrations, services/routes, events/handlers, UI, agent, config/rules/parameters,
  permissions, seed data, release evidence, and tests proving a standalone one-PBC application lifecycle.