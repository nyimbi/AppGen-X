# Cross Border Trade Implementation Status

## Status

Implemented the standalone one-PBC application surface for `cross_border_trade`.

## Delivered

- Added `app_surface.py` for forms, wizards, controls, document-instruction CRUD previews, and single-PBC app evidence.
- Extended runtime capabilities and smoke audits with the single-PBC app gate.
- Extended UI contracts and rendered workbench output with forms, wizards, controls, and standalone app metadata.
- Extended the assistant document-instruction plan with trade-specific target operations and owned-table mutation previews.
- Extended release evidence to include forms, wizards, controls, and single-PBC app readiness.
- Added focused tests proving the one-PBC app surface and its runtime/UI/agent/release integration.
- Added README and implementation plan/status documentation.

## Review Findings Resolved

- The PBC no longer relies only on a deep runtime smoke audit; it now declares the actual generated app controls a user needs to operate the domain.
- Document instructions now map to trade-specific commands such as `prepare_trade_document_packet`, `screen_export_control`, and `file_customs_declaration`.
- Workbench rendering now exposes forms, wizards, and release controls instead of only cards and fragments.
- Release readiness now carries explicit single-PBC app evidence.

## Validation

Validation commands for this slice:

- `python3 -m py_compile src/pyAppGen/pbcs/cross_border_trade/app_surface.py src/pyAppGen/pbcs/cross_border_trade/runtime.py src/pyAppGen/pbcs/cross_border_trade/ui.py src/pyAppGen/pbcs/cross_border_trade/agent.py src/pyAppGen/pbcs/cross_border_trade/release_evidence.py src/pyAppGen/pbcs/cross_border_trade/tests/test_app_surface.py`
- `./.venv/bin/pytest -q src/pyAppGen/pbcs/cross_border_trade/tests`
- `pbc_implementation_release_audit(("cross_border_trade",))`
- `pbc_generation_smoke_audit(("cross_border_trade",))`

## Remaining Risks

The runtime and app contracts are executable and side-effect-free, but this slice does not add a live HTTP server, browser-rendered frontend, or external customs/broker/carrier adapters. Those should remain later integration layers over this owned PBC surface.
