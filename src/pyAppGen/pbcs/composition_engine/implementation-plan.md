# Composition Engine Implementation Plan

## Goal

Turn `composition_engine` into a usable one-PBC composition/orchestration app without leaving the package boundary.

## Selected Backlog Themes

- PBC selection impact preview
- Document-driven composition intake
- Agent competency catalog and routing policy
- Guided operator forms, wizards, and controls
- Generated smoke-plan synthesis
- Release rehearsal and release-note drafting
- Documentation matrix and security review panel
- Release evidence alignment across runtime, UI, assistant, and tests

## Execution Steps

1. Align runtime, permissions, configuration, schema, service, and release evidence so the package exposes one coherent owned boundary.
2. Add package-local forms, wizards, and controls for workspace intake, selection, layout binding, governance, assistant preview, and release gating.
3. Extend runtime with selection-impact preview, smoke-plan synthesis, artifact lineage, documentation coverage, security review, release rehearsal, release notes, and assistant CRUD previews.
4. Wire those surfaces into the UI contract, assistant/chatbot contract, manifest, exports, and release evidence.
5. Add focused package-local tests for orchestration flow, assistant guardrails, and the new UI/control surfaces.
6. Record verification evidence and remaining risks in `implementation-status.md`.
