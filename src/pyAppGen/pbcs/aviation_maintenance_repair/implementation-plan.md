# Implementation Plan

## Selected Slice

Implement a standalone `aviation_maintenance_repair` release-planning slice that
stays fully package-local and makes one end-to-end maintenance release workflow
executable inside the PBC.

The slice covers:

- aircraft, component, work-card, deferred-defect, and AD record intake;
- release-to-service assessment with human certifier guardrails;
- package-local workflow contracts, forms, wizards, and controls;
- governed document-instruction planning for CRUD previews;
- AppGen-X event/handler, permissions, and release-evidence coverage.

## File-Level Plan

1. Replace generic model/schema placeholders with domain-specific model
   contracts for aircraft, components, work cards, deferred defects,
   airworthiness directives, compliance releases, and package governance
   records.
2. Implement package-local workflow contracts for `release_to_service` and
   `document_instruction_planning`, then wire them through runtime, services,
   routes, UI, and assistant contracts.
3. Harden release evaluation so work-card closeout, duplicate inspection,
   authorization, tooling, consumables, deferred defects, component
   airworthiness, and human certifier checks all produce deterministic blocker
   evidence.
4. Expose focused standalone route and workbench metadata without touching
   shared generator, DSL, or cross-PBC ledgers.
5. Add focused package tests plus compile/smoke verification and refresh the
   package docs with concrete evidence.

## Acceptance Targets

- `aviation_maintenance_repair_runtime_smoke()` produces a release-ready pack
  for a valid local scenario.
- Blocked scenarios return explicit blocker codes and emit
  `AviationMaintenanceRepairExceptionOpened`.
- UI contracts expose forms, wizards, and controls for the standalone slice.
- Assistant planning previews CRUD mutations, stays inside owned tables, and
  never claims certifier authority.
- Release evidence reports schema, services, routes, workflows, UI, assistant,
  permissions, handlers, and governance readiness from inside the package.
