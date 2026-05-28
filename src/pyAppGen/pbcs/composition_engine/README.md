# Composition Engine PBC

`composition_engine` is a self-contained one-PBC composition/orchestration slice for AppGen-X. It owns workspace setup, PBC selection, component and fragment registration, layout binding, validation, side-effect-free package registration planning, release rehearsal, release evidence, assistant document previews, and package-local workbench surfaces.

## What It Exposes

- Owned runtime state and schema descriptors for composition workspaces, fragments, bindings, DSL artifacts, validation runs, package plans, release evidence, rules, parameters, configuration, and AppGen-X inbox/outbox/dead-letter tables.
- Composition-specific forms, guided wizards, and operational controls under [`forms.py`](./forms.py), [`wizards.py`](./wizards.py), and [`controls.py`](./controls.py).
- A richer assistant surface under [`agent.py`](./agent.py) for document-driven intake, intent routing, competency catalog publication, and CRUD previews that stay inside composition-owned tables.
- Workbench UI metadata and render helpers under [`ui.py`](./ui.py) for the composition console, assistant preview workbench, release rehearsal panel, documentation matrix, and security review panel.
- Package-local release evidence in [`runtime.py`](./runtime.py) and [`release_evidence.py`](./release_evidence.py), including smoke-plan synthesis, artifact lineage, documentation coverage, assistant guardrails, and security review.

## Key Runtime Entry Points

- `composition_engine_runtime_smoke()`
- `composition_engine_release_rehearsal(state, workspace_id)`
- `composition_engine_assistant_document_preview(document_text, instructions, ...)`
- `composition_engine_build_control_center(state, workspace_id=...)`
- `composition_engine_build_release_evidence()`

## Verification

- `./.venv/bin/pytest src/pyAppGen/pbcs/composition_engine/tests -q`
- `python3 -m compileall src/pyAppGen/pbcs/composition_engine`
- `./.venv/bin/python - <<'PY' ... runtime/ui/agent/control smoke checks ... PY`

See [`implementation-status.md`](./implementation-status.md) for the latest recorded evidence.
