# Electronic Health Records Core Implementation Plan

## Scope

Implement `electronic_health_records_core` as a package-local, executable one-PBC EHR slice without changing shared AppGen-X infrastructure or any files outside this directory.

## Constraints

- Only modify files under `src/pyAppGen/pbcs/electronic_health_records_core`.
- Keep package entrypoints stable so existing imports and discovery continue to work.
- Use only owned tables, AppGen-X events, and declared APIs; no foreign table access.
- Replace generic scaffold behavior with a coherent in-memory reference implementation that is testable and side-effect-free.

## Domain Slice

This pass turns the package into a usable EHR core focused on the owned chart:

- longitudinal patient chart creation with duplicate-candidate review rather than unsafe auto-merge
- encounter intake with care-setting semantics and documentation checklist
- clinical order lifecycle with allergy-aware safety warnings and invalid-transition guards
- observation capture with unit/reference-range evidence and critical-result acknowledgement workflow
- allergy specificity with duplicate detection and order warning support
- medication-list reconciliation with discrepancy tracking and unresolved counts
- care-note authorship, attestation, co-signature, and amendment lineage
- permission-aware patient summary assembly and segment redaction
- queue-oriented workbench, forms, wizards, controls, and governed assistant flows

## Delivery Plan

1. Add a package-local executable module for the EHR slice:
   - in-memory owned-table state
   - command/query functions for chart, encounter, order, observation, allergy, medication reconciliation, note, and summary workflows
   - AppGen-X outbox evidence, idempotency guards, and control assertions
   - forms, wizards, controls, workbench queues, and one-PBC app contract
2. Rebuild package adapters around that executable core:
   - runtime/schema/model/service contracts
   - routes, UI metadata, agent/chatbot mutation planning
   - rules, parameters, configuration, permissions, handlers, and seed data
   - release evidence, manifest, README, status, and migration DDL
3. Add focused tests that prove:
   - duplicate chart review is flagged without auto-merge
   - encounter completeness and note attestation controls work
   - unsafe order transitions and unacknowledged critical results are blocked
   - medication reconciliation and summary redaction are executable
   - services, routes, UI, agent flows, and release evidence are coherent
4. Validate with compile checks, focused package tests, and PBC release/smoke gates if they run in the current environment.

## Intended Outcome

The PBC should function as a standalone electronic health records core reference slice with meaningful domain behavior, not just generic generated metadata.
