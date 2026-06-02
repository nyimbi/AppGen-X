# Workflow Orchestration

`workflow_orchestration` is a standalone AppGen-X packaged business capability
for long-running workflow execution, saga coordination, timers, human tasks,
policy controls, and governed operator assistance.

## What This Package Provides

- A package-local runtime with owned workflow tables, configuration,
  parameters, rules, inbox/outbox/dead-letter behavior, and workbench views.
- Runtime-driven schema, model, repository, service, route, permission, seed,
  and release contracts so generated artifacts stay aligned with executable
  behavior.
- A standalone one-PBC app surface in `standalone.py` that bootstraps workflow
  definitions, versions, policies, signals, tasks, compensations, and release
  evidence entirely inside this package.
- UI contracts for workbench fragments plus explicit forms, wizards, and
  controls for workflow authoring, signal admission, timer management,
  exception recovery, and release readiness.
- Agent/document-planning helpers that extract workflow structure from text and
  return governed CRUD or action previews with routes, permissions,
  idempotency keys, and AppGen-X event expectations.

## Key Entrypoints

- Runtime: `runtime.py`
- Repository: `repository.py`
- Models: `models.py`
- Services: `services.py`
- Routes: `routes.py`
- UI/workbench: `ui.py`
- Standalone app: `standalone.py`
- Agent planning: `agent.py`
- Release audit: `release_evidence.py`

## Validation

Focused package-local validation is captured in `tests/test_contract.py`,
`tests/test_standalone.py`, `implementation-status.md`, and
`RELEASE_EVIDENCE.md`.
