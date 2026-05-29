## Objective

Make `src/pyAppGen/pbcs/eam` function as a standalone one-PBC Enterprise Asset Management app package with internally consistent runtime, schema, services, routes, UI, events, permissions, seed data, agent planning, release evidence, and focused tests.

## Scope

- Stay package-local to `src/pyAppGen/pbcs/eam`.
- Prefer tightening existing executable contracts over adding new framework layers.
- Keep the runtime side-effect-free and evidence-driven.

## Gaps Found

1. Runtime, events, permissions, handlers, and release evidence disagree on topics, tables, permissions, and supported handlers.
2. Configuration and rule/parameter manifests are generic rather than EAM-specific.
3. Seed data is too thin to prove standalone EAM setup.
4. UI contract lacks explicit forms, wizards, cockpit controls, and agent/document planning evidence expected by the backlog.
5. Tests validate modules in isolation but do not prove a focused standalone EAM lifecycle.

## Implementation Steps

1. Align package contracts to the runtime source of truth.
   - Make permissions, event metadata, handlers, configuration, and release evidence derive from `runtime.py`.
   - Preserve AppGen-X inbox/outbox/dead-letter guarantees and owned-boundary enforcement.

2. Strengthen standalone EAM evidence.
   - Expand EAM-specific parameters, rules, permissions, seed descriptors, UI surfaces, and release checks.
   - Add agent/chatbot/document/CRUD planning evidence tied to owned tables and runtime operations.

3. Prove the package end-to-end.
   - Add focused tests for cross-module consistency and a standalone maintenance lifecycle scenario.
   - Run compile/test gates for the package and record outcomes in `implementation-status.md`.

4. Finish package documentation.
   - Write `README.md` for package usage and exported evidence.
   - Write `implementation-status.md` with completed work, verification, and remaining limits.

## Verification Plan

- Python compile gate for `src/pyAppGen/pbcs/eam`.
- Focused pytest run for `src/pyAppGen/pbcs/eam/tests/test_contract.py`.
- Review changed contracts for accidental cross-PBC references or stale constants.
