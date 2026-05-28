# Cross Border Trade Implementation Plan

## Intent

Make `cross_border_trade` usable as a complete one-PBC trade operations app. The existing runtime already contains deep trade lifecycle behavior; this pass adds explicit generated-application evidence for forms, wizards, controls, UI surfacing, release evidence, and agent-assisted document CRUD planning.

## Domain Slice

This pass focuses on the operator surface required for a single-PBC application:

- HS classification readiness and jurisdiction-aware approval.
- Landed-cost quote capture with duty, tax, fee, Incoterm, currency, and scenario trace.
- Denied-party screening with fuzzy-match resolution and override evidence.
- Export-control checks with license requirement and end-use evidence.
- Customs declaration filing and release readiness.
- Trade document packet completeness.
- Broker and carrier handoff readiness.
- Compliance hold opening, ownership, SLA, and resolution evidence.
- Country restriction policy change impact.
- Assistant document intake for invoices, packing lists, certificates, end-use statements, declarations, denied-party evidence, broker requests, and carrier handoffs.

## Executable Design

`app_surface.py` is the package-local one-PBC app surface. It defines deterministic, side-effect-free contracts for forms, wizards, controls, document-instruction mutation plans, and a standalone app contract. Runtime capabilities, UI contracts, agent plans, and release evidence now expose that surface directly.

The existing runtime remains the executable trade engine for state transitions, AppGen-X inbox/outbox, rules, parameters, customs release gates, broker/carrier handoffs, document packets, analytics, and release smoke audits.

## UI And Controls

The app exposes six forms, five wizards, and eight controls. These are intentionally operator-facing rather than generic catalog metadata: each form binds to an owned table and command; each wizard names a domain workflow; each control names a blocking release condition.

The workbench now returns forms, wizards, controls, and `single_pbc_app` metadata with its rendered cards so generated apps can render a standalone trade workspace.

## Validation Plan

Focused tests prove:

- A single-PBC trade app is database-backed and includes forms, wizards, controls, and AppGen-X eventing.
- Forms, wizards, and controls cover the customs release flow.
- Document instructions map to trade-specific CRUD previews.
- UI and runtime capabilities expose the standalone app surface.
- Runtime smoke includes the single-PBC app gate.

Validation commands:

- `python3 -m py_compile` on touched modules.
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/cross_border_trade/tests`
- `pbc_implementation_release_audit(("cross_border_trade",))`
- `pbc_generation_smoke_audit(("cross_border_trade",))`

## Remaining Expansion

Future passes should deepen actual persistence adapters, live HTTP binding, broker API adapters, tariff-source refresh, formal country policy compilation, and richer document parsing. This pass makes the generated one-PBC application contract explicit and executable.
