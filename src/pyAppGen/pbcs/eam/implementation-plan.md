# EAM Improve1 Implementation Plan

## Intent

This plan implements the `improve1.md` backlog as a package-local Enterprise Asset Management application surface. The goal is not to add another catalog entry; the EAM PBC must be usable by itself as a controlled maintenance application with owned data, forms, wizards, controls, routes, event evidence, AI assistance, release gates, and explanatory documentation.

## Backlog Reading Summary

The backlog asks EAM to cover the real operating surface of enterprise asset management: equipment readiness, asset hierarchy integrity, locations and criticality, warranty recovery, preventive and predictive strategies, meter and condition triggers, work request triage, work-order lifecycle, planning packages, scheduling, mobile execution, skills and tools, safety permits and isolation, spares, downtime, failure analysis, root cause, reliability analytics, forecasting, vendor work, external event projections, AppGen-X reliability, UI coverage, AI-safe planning, semantic maintenance instructions, anomaly detection, governed models, decentralized equipment identity, resilience drills, continuous controls, readiness scoring, and an end-to-end proof.

The existing implementation already provides a deep runtime for equipment registration, maintenance plans, readings, safety permits, work orders, scheduling, spares, completion, reliability analytics, policy screening, compliance proof, model governance, AppGen-X inbox/outbox/dead-letter handling, and workbench rendering. The missing package-local deliverables are the explicit improvement plan, standalone app contract, richer app-surface tests, README, implementation status, and release evidence that proves the improve1 work is mounted for a one-PBC generated application.

## Implementation Steps

1. Add `app_surface.py` as the standalone application contract for EAM.
   - Expose forms for equipment readiness, hierarchy, work requests, work packages, safety permits, spares, mobile completion, vendor service, reliability analytics, controls, and configuration.
   - Expose wizards for equipment-to-maintenance readiness, work-order planning, safety/isolation, mobile execution, reliability improvement, vendor dispatch, and resilience drills.
   - Expose controls for hierarchy integrity, permit readiness, skill/tool matching, spare governance, AppGen-X replay, foreign-table boundary proof, model governance, and continuous control assertions.
   - Provide an end-to-end maintenance proof summary bound to the existing runtime smoke scenario.

2. Wire the app surface into package entrypoints.
   - Include standalone app evidence in `implementation_contract()` and `smoke_test()`.
   - Include standalone route contracts in route evidence.
   - Include standalone app evidence in UI and composed agent contribution.
   - Include standalone checks in release evidence.

3. Add focused tests.
   - Verify single-PBC app readiness, forms/wizards/controls coverage, AI document planning boundaries, route/UI/agent/release integration, and package smoke exposure.
   - Keep tests side-effect-free and package-local.

4. Write the README.
   - Explain the EAM domain, owned boundary, standard capabilities, advanced capabilities, data model, runtime, UI, agent, configuration, events, and verification.
   - Make it useful for a new engineer completing or reviewing this PBC.

5. Write implementation status.
   - Record what was implemented, how improve1 items map to code, validation commands, review findings, known residual risks, and next merge notes.

## Review Checklist

- No file outside `src/pyAppGen/pbcs/eam` is changed.
- Ordinary data backends remain PostgreSQL, MySQL, and MariaDB.
- Eventing remains AppGen-X; no stream-engine picker is exposed.
- Agent plans are side-effect-free and require human confirmation for mutations.
- Generated app evidence references owned EAM tables only, plus declared API/event/projection dependencies.
- Release evidence and tests prove forms, wizards, controls, UI, routes, agent, and end-to-end proof are available to a one-PBC app.
