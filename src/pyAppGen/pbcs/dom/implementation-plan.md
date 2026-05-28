# DOM Standalone Implementation Plan

## Goal

Make `src/pyAppGen/pbcs/dom` usable as a standalone one-PBC application without touching shared generator code or other PBCs.

## Scope

- Package-owned runtime and standalone application state.
- Order intake, validation, promise/ATP hinting, allocation, routing, planning, shipment confirmation.
- Holds, releases, backorders, substitutions, cancellations, exceptions, and audit evidence.
- Package-local UI forms, wizards, controls, and workbench rendering.
- Agent document intake and CRUD mutation planning.
- Package-local service methods, route execution, release evidence, and audit coverage.
- Package-local tests only under `src/pyAppGen/pbcs/dom/tests`.

## Delivery slices

1. Add standalone application shell and service wrapper.
2. Wire UI contract to executable forms, wizards, controls, and richer workbench queues.
3. Upgrade agent planning to extract order facts from documents and propose governed mutations.
4. Align event, service, route, permission, seed, manifest, and release evidence modules with the standalone surface.
5. Add package-local tests and audit execution.
