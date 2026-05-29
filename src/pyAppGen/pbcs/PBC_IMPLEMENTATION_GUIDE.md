# AppGen-X PBC Implementation Guide

This guide is the working standard for fleshing out an AppGen-X Packaged Business Capability (PBC). It is written for an engineer assigned one directory under `src/pyAppGen/pbcs/<pbc_key>` who must turn that package into a standalone, composable business capability.

A complete PBC is not a catalog row, documentation stub, or generated placeholder. It is a package-local business application capability with owned schema, migrations, models, services, APIs, events, handlers, UI fragments, wizards, controls, configuration, rules, parameters, permissions, seed data, AI-agent skills, tests, release evidence, and side-effect-free registration. If an application is generated with only one PBC, that application must still be functional for the PBC's domain.

## 1. Work Scope

Work in a dedicated git worktree and branch for one PBC unless the lead explicitly assigns a different isolation model.

Use branch names like:

```text
pbc/<pbc-key>-standalone
```

Only edit files under:

```text
src/pyAppGen/pbcs/<pbc_key>
```

Do not edit global generators, global catalogs, shared docs, unrelated tests, or another PBC's directory. If a release gate fails because of global verifier behavior, record the blocker in `implementation-status.md` and report it upward rather than changing global code.

Every commit must use the repository Lore commit protocol. The commit should explain why the PBC was changed, which constraints shaped the implementation, rejected alternatives, verification performed, and known gaps.

## 2. Required Inputs

Before implementation, read the package-local materials:

```text
src/pyAppGen/pbcs/<pbc_key>/improve1.md
src/pyAppGen/pbcs/<pbc_key>/SPECIFICATION.md
src/pyAppGen/pbcs/<pbc_key>/manifest.py
src/pyAppGen/pbcs/<pbc_key>/runtime.py
src/pyAppGen/pbcs/<pbc_key>/models.py
src/pyAppGen/pbcs/<pbc_key>/services.py
src/pyAppGen/pbcs/<pbc_key>/routes.py
src/pyAppGen/pbcs/<pbc_key>/ui.py
src/pyAppGen/pbcs/<pbc_key>/agent.py
src/pyAppGen/pbcs/<pbc_key>/tests/test_contract.py
```

Then write `implementation-plan.md` in the PBC directory. The plan must be hand-curated and domain-specific. It must not be a generic checklist pasted across PBCs.

The plan should cover:

- The domain scope and non-scope.
- The personas and operating context.
- Table-stakes capabilities.
- Advanced capabilities.
- Owned data model.
- Workflows and exception flows.
- UI workbench, forms, wizards, and controls.
- Agent/chatbot skills.
- Configuration, parameters, and rule model.
- AppGen-X eventing.
- Release evidence and tests.

## 3. Required Package Shape

A complete PBC should contain these files unless it already has equivalent working files:

```text
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
```

Optional package-local files are encouraged when they reduce complexity: `blueprint.py`, `domain_depth.py`, `standalone.py`, `workflows.py`, `rules.py`, `analytics.py`, and focused test modules such as `tests/test_standalone.py`.

## 4. Package Root Interface

`__init__.py` must expose a side-effect-free interface. Imports must not create tables, mutate the global catalog, write files, open network connections, or start services.

Required functions:

```python
def implementation_contract() -> dict: ...
def register_pbc() -> dict: ...
def registration_plan(existing_catalog: dict | None = None) -> dict: ...
def package_metadata_manifest() -> dict: ...
def validate_package_metadata() -> dict: ...
def package_discovery_plan(existing_catalog: dict | None = None) -> dict: ...
def smoke_test() -> dict: ...
```

`implementation_contract()` should include:

```python
{
    "pbc": "<pbc_key>",
    "implementation_directory": "src/pyAppGen/pbcs/<pbc_key>",
    "owns_code": True,
    "side_effect_free": True,
    "standard_features": (...),
    "advanced_runtime": <runtime_capabilities>,
    "ui_contract": <ui_contract>,
    "api_contract": <api_contract>,
    "schema_contract": <schema_contract>,
    "service_contract": <service_contract>,
    "release_evidence_contract": <release_evidence>,
    "permissions_contract": <permissions_contract>,
    "owned_tables": (...),
    "runtime_tables": (...),
    "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
}
```

`register_pbc()` returns the manifest only. `registration_plan()` returns a side-effect-free plan to register the package.

## 5. Manifest Standard

`manifest.py` must define a stable `PBC_MANIFEST`. The manifest is used for prompt selection, generation, composition, and release audits.

Minimum fields:

```python
PBC_MANIFEST = {
    "pbc": "<pbc_key>",
    "label": "...",
    "mesh": "...",
    "description": "...",
    "datastore_backend": "postgresql",
    "tables": (...),
    "apis": (...),
    "emits": (...),
    "consumes": (...),
    "ui_fragments": (...),
    "permissions": (...),
    "configuration": (...),
    "capabilities": (...),
    "standard_features": (...),
    "advanced_capabilities": (...),
    "workflows": (...),
    "analytics": (...),
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": (...),
}
```

Use AppGen-X terminology only. Do not introduce banned legacy product or framework names. Ordinary PBC database backends must remain PostgreSQL, MySQL, or MariaDB. Do not expose stream-engine pickers to users.

## 6. Domain Depth Standard

The PBC must fully cover the domain it claims. This requires hand-crafted domain thinking.

Define:

- Primary personas.
- Master data.
- Transaction data.
- Lifecycle states.
- Normal workflows.
- Exception workflows.
- Approval flows.
- Reversal, correction, cancellation, and reopen behavior.
- Audit evidence.
- Configuration rules and parameters.
- Analytics.
- Edge cases.
- Credible advanced capabilities.

Examples:

- Enterprise asset management should cover asset registry, hierarchy, work orders, maintenance strategy, inspections, reliability, shutdowns, permits, spares, warranties, calibration, safety, compliance, downtime, and lifecycle cost.
- Enterprise search/vector should cover connectors, crawling, ACL trimming, indexes, embeddings, vector drift, relevance tuning, synonyms, freshness, query analytics, source governance, retrieval evaluation, and answer grounding.
- Expense management should cover reports, receipt evidence, card feeds, policies, violations, approvals, reimbursements, advances, mileage, per diem, duplicates, fraud signals, audit sampling, and spend intelligence.

World-class means the package demonstrates a complete professional operating surface with executable behavior and testable contracts. It does not mean claiming impossible capabilities without evidence.

## 7. Owned Data Boundary

Every owned table must be prefixed with the PBC key:

```text
<pbc_key>_<logical_table>
```

A PBC may depend on another PBC only through:

- Declared API dependencies.
- AppGen-X events.
- Owned projections populated from consumed events.
- Stable external identifiers copied into owned tables.

Do not read or write another PBC's tables.

`models.py` should expose:

```python
def model_registry() -> dict: ...
def database_model_contract() -> dict: ...
def model_manifest() -> dict: ...
def instantiate_model(table_name: str, values: dict | None = None) -> dict: ...
def smoke_test() -> dict: ...
```

`schema_contract.py` should expose:

```python
def build_schema_contract() -> dict: ...
def validate_schema_contract() -> dict: ...
def smoke_test() -> dict: ...
```

The schema contract must include tables, fields, primary keys, indexes, relationships, migrations, models, dependencies, and `shared_table_access: False` evidence.

`migrations/001_initial.sql` must contain real DDL for owned domain tables plus AppGen-X outbox, inbox, and dead-letter tables.

## 8. Runtime Standard

`runtime.py` is the executable core. It should be deterministic and side-effect-free unless a method explicitly returns a database plan or uses a package-local in-memory harness for tests.

Required runtime surfaces:

```python
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
def <pbc_key>_permissions_contract() -> dict: ...
def <pbc_key>_verify_owned_table_boundary(references: tuple | list) -> dict: ...
def <pbc_key>_runtime_smoke() -> dict: ...
def <pbc_key>_runtime_capabilities() -> dict: ...
```

The runtime capabilities contract must list operations for configuration, parameters, rules, event ingestion, workbench rendering, schema contract, service contract, release evidence, domain commands, and advanced capabilities.

A package-local app facade is strongly recommended:

```python
class DomainStandaloneApp:
    def __init__(self, state: dict | None = None): ...
    def configure_runtime(self, config: dict) -> dict: ...
    def execute(self, operation: str, payload: dict | None = None) -> dict: ...
    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict: ...
    def render_workbench(self, ...) -> dict: ...
```

Tests should prove a realistic lifecycle can run through this facade.

## 9. Service And Route Standard

`services.py` should expose command/query behavior around the runtime. Commands mutate only owned state and append AppGen-X outbox events. Queries are read-only.

Required surfaces:

```python
def service_operation_contracts() -> dict: ...
def operation_plan(operation_name: str, payload: dict | None = None) -> dict: ...
def service_operation_manifest() -> dict: ...
class <PbcService>: ...
def smoke_test() -> dict: ...
```

Operation contracts should include:

```python
{
    "operation": "...",
    "operation_kind": "command" | "query",
    "method": "POST" | "GET" | "PATCH" | "DELETE",
    "path": "/api/pbc/<pbc_key>/...",
    "permission": "<pbc_key>....",
    "owned_tables": (...),
    "read_tables": (...),
    "emitted_event": "...",
    "transaction_boundary": "owned_datastore_plus_outbox",
    "event_contract": "AppGen-X",
    "idempotency_key": "...",
}
```

`routes.py` should expose:

```python
def api_route_contracts() -> dict: ...
def validate_api_route_contracts() -> dict: ...
def dispatch_route(method: str, path: str, payload: dict | None = None, service=None) -> dict: ...
def smoke_test() -> dict: ...
```

Do not list routes that cannot execute.

## 10. Event And Handler Standard

Every ordinary PBC uses the AppGen-X event contract. Do not expose broker or stream-engine choices to users.

`events.py` should expose:

```python
def event_contract_manifest() -> dict: ...
def validate_event_contract() -> dict: ...
def build_event_envelope(event_type: str, payload: dict, ...) -> dict: ...
def event_dispatch_plan(event: dict) -> dict: ...
def smoke_test() -> dict: ...
```

The event manifest must include topic names, outbox/inbox/dead-letter table names, typed emitted events, typed consumed events, payload fields, retry policy, idempotency evidence, and `stream_engine_picker_visible: False`.

`handlers.py` should expose:

```python
def handler_manifest() -> dict: ...
def dispatch_event(event: dict, state: dict | None = None) -> dict: ...
def smoke_test() -> dict: ...
```

Handlers must be idempotent. Unknown events should produce dead-letter evidence and retry metadata without mutating domain state.

## 11. Configuration, Parameters, And Rules

Every PBC must understand and implement configuration, rules, and parameters.

`config.py` should expose:

```python
def configuration_manifest() -> dict: ...
def validate_configuration(config: dict) -> dict: ...
def parameter_manifest() -> dict: ...
def set_parameter(name: str, value: object, ...) -> dict: ...
def rule_manifest() -> dict: ...
def compile_rule(rule: dict) -> dict: ...
def evaluate_rule(compiled_rule: dict, context: dict) -> dict: ...
def governance_smoke_test() -> dict: ...
def smoke_test() -> dict: ...
```

Parameters must be typed and bounded. Rules must be declarative and explainable enough for both UI editors and the PBC agent.

## 12. UI Standard

Every PBC must have UI. The package may define generated UI contracts rather than hand-written frontend components, but those contracts must be complete enough for a generated standalone app.

`ui.py` should expose:

```python
def <pbc_key>_ui_contract() -> dict: ...
def <pbc_key>_render_workbench(state: dict | None = None, ...) -> dict: ...
def <pbc_key>_standalone_app_contract() -> dict: ...
def smoke_test() -> dict: ...
```

The UI contract must include:

- Workbench route.
- Navigation sections.
- Forms.
- Wizards.
- Controls.
- Panels and cards.
- Action permissions.
- Configuration editor.
- Rule editor.
- Parameter editor.
- Event inbox, outbox, and dead-letter surfaces.
- Release evidence panel.
- Agent/chatbot panel.

Forms must map to commands. Wizards must represent real multi-step domain workflows. Controls must be useful domain controls, not decorative metadata.

## 13. Agent And Skill Standard

AI agents are first-class citizens of composed AppGen-X applications. Each PBC contributes skills to the single composed application agent.

`agent.py` should expose:

```python
def agent_skill_manifest() -> dict: ...
def chatbot_interface_contract() -> dict: ...
def document_instruction_plan(document: str, instruction: str, context: dict | None = None) -> dict: ...
def datastore_crud_plan(action: str, table: str | None = None, payload: dict | None = None) -> dict: ...
def composed_agent_contribution() -> dict: ...
def smoke_test() -> dict: ...
```

The agent must:

- Explain how to accomplish domain tasks.
- Accept documents/instructions and produce safe mutation plans.
- Map instructions to forms, wizards, service commands, and owned tables.
- Reject foreign tables.
- Require human confirmation for mutations.
- Use AppGen-X event contracts.
- Expose a `single_agent_skill_namespace`.
- Be expressible in the generated DSL.

The agent should not silently mutate state from free-form text. It should return a plan with impacted records, required permissions, event previews, idempotency keys, and validation warnings.

## 14. Permissions And Seed Data

`permissions.py` should expose:

```python
def permission_manifest() -> dict: ...
def authorize(actor: str, permission: str, context: dict | None = None) -> dict: ...
def smoke_test() -> dict: ...
```

Permissions should cover read, create, update, approve, administer, and domain-sensitive actions.

`seed_data.py` should expose:

```python
def seed_plan() -> dict: ...
def validate_seed_data() -> dict: ...
def smoke_test() -> dict: ...
```

Seed data should be useful: default rules, sample records, reference statuses, thresholds, roles, or starter catalogs. It must target owned tables only.

## 15. Release Evidence

`release_evidence.py` should expose:

```python
def pbc_source_artifact_contract() -> dict: ...
def build_release_evidence() -> dict: ...
def release_readiness_manifest() -> dict: ...
def validate_release_evidence() -> dict: ...
def pbc_implementation_release_audit() -> dict: ...
def pbc_generation_smoke_audit() -> dict: ...
def smoke_test() -> dict: ...
```

Release evidence must prove required files exist; schema, models, and migrations align; services and routes execute; events use AppGen-X; handlers are idempotent and retryable; UI includes forms, wizards, and controls; the agent exposes document and CRUD planning; configuration/rules/parameters work; permissions and seed data are valid; owned-table boundaries are respected; and tests/smoke gates passed.

`RELEASE_EVIDENCE.md` should summarize the same evidence for humans and list exact commands run.

## 16. Capability Assurance

`capability_assurance.py` should prove table-stakes and advanced coverage.

Required surfaces:

```python
def table_stakes_capability_manifest() -> dict: ...
def validate_table_stakes_capability_coverage() -> dict: ...
def smoke_test() -> dict: ...
```

The manifest should map every standard feature to concrete operations, routes, UI panels, tests, and tables. It should prove AppGen-X eventing, no stream picker, no invalid backend, and no foreign table mutation.

## 17. Tests

Package-local tests must be meaningful. `tests/test_contract.py` should include tests equivalent to:

```python
def test_generated_schema_service_and_release_evidence(): ...
def test_manifest_and_event_contract(): ...
def test_registration_plan_is_side_effect_free(): ...
def test_service_and_route_surface_are_executable(): ...
def test_configuration_permissions_and_seed_hooks_are_executable(): ...
def test_event_handlers_are_idempotent_and_retryable(): ...
def test_agent_chatbot_skills_and_governed_crud_are_executable(): ...
def test_runtime_smoke_and_domain_lifecycle_are_executable(): ...
def test_pbc_source_artifact_contract(): ...
def test_pbc_implementation_release_audit(): ...
def test_pbc_generation_smoke_audit(): ...
```

Run:

```text
python3 -m py_compile src/pyAppGen/pbcs/<pbc_key>/*.py src/pyAppGen/pbcs/<pbc_key>/tests/*.py
./.venv/bin/pytest -q src/pyAppGen/pbcs/<pbc_key>/tests
```

Run repository PBC gates:

```python
from pyAppGen.pbc import (
    pbc_specification_contract,
    pbc_source_artifact_contract,
    pbc_implementation_release_audit,
    pbc_generation_smoke_audit,
)

key = "<pbc_key>"
assert pbc_specification_contract(key)["ok"]
assert pbc_source_artifact_contract(key)["ok"]
assert pbc_implementation_release_audit((key,))["ok"]
assert pbc_generation_smoke_audit((key,))["ok"]
```

If a gate fails because it expects traceable materialization, add real assertions/functions/contracts in the PBC package. Do not weaken global verifiers from a PBC branch.

## 18. README Standard

`README.md` must help a developer and product owner understand and operate the package.

Include:

- What the PBC does.
- Domain scope and non-scope.
- Personas.
- Owned tables and boundaries.
- Main workflows.
- UI surfaces.
- Agent skills.
- Configuration, rules, and parameters.
- Events emitted and consumed.
- Test and smoke commands.
- One-PBC app composition notes.
- Known limitations and next extension points.

Avoid vague marketing copy.

## 19. Implementation Status Standard

`implementation-status.md` is the handoff artifact. Include:

- Date and branch.
- Summary of implemented capabilities.
- Files changed.
- Domain capabilities covered.
- Advanced capabilities covered.
- Verification commands and results.
- Review findings and fixes.
- Known gaps.
- Merge notes.

Be honest. Do not claim completion if global gates fail, tests are narrow, or important domain behavior is metadata-only.

## 20. Code Review Checklist

Before committing, verify:

- Imports are side-effect-free.
- All changes are inside `src/pyAppGen/pbcs/<pbc_key>`.
- Manifest key matches directory name.
- All owned tables are prefixed with the PBC key.
- Database backends are limited to PostgreSQL, MySQL, and MariaDB.
- AppGen-X event contracts are used everywhere.
- No user-facing stream-engine picker exists.
- Commands are backed by real runtime/service methods.
- Routes dispatch to real commands/queries.
- Handlers prove idempotency, retry, and dead-letter behavior.
- Forms map to commands.
- Wizards cover realistic domain workflows.
- Controls expose meaningful domain operation/configuration.
- Agent rejects foreign tables and requires confirmation for mutations.
- Rules, parameters, and configuration execute.
- Seed data targets owned tables.
- Release evidence includes named gate results.
- Tests prove a one-PBC lifecycle.
- `implementation-status.md` honestly lists verification and gaps.

## 21. Commit And Push Workflow

```text
git status -sb
git add src/pyAppGen/pbcs/<pbc_key>
git diff --cached --name-only
git commit ...
git diff --check HEAD~1..HEAD -- src/pyAppGen/pbcs/<pbc_key>
git push -u origin pbc/<pbc-key>-standalone
```

Do not push directly to `main` for isolated PBC work. Branches are reviewed and merged later.

## 22. Definition Of Done

A PBC is ready for merge when:

- `implementation-plan.md`, `implementation-status.md`, and `README.md` exist and are domain-specific.
- The package imports without side effects.
- It can execute a realistic domain lifecycle using package-local code.
- It has owned schema, migrations, models, services, routes, events, handlers, UI, agent, config, permissions, seed data, release evidence, and tests.
- Package tests pass.
- Source artifact, release audit, and generation smoke gates pass for that PBC.
- The branch commit touches only the assigned PBC directory.
- The Lore commit explains constraints, rejected alternatives, verification, and known gaps.

If any item is missing, the PBC is not complete. Continue implementing.
