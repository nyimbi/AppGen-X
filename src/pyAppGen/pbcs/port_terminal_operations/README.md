# Port Terminal Operations Standalone PBC

This package now ships a standalone one-PBC application surface for port terminal operations.

The standalone app stays inside the owned datastore boundary and exposes package-local forms, wizards, controls, workbench rendering, document-intake planning, and release-readiness evidence for:

- vessel arrival and berth nomination
- container, yard, and gate flow exceptions
- equipment fallback dispatch
- customs handoff and hold resolution
- control assertions and governed model evidence

Entrypoints:

- `port_terminal_operations_standalone_app_contract()`
- `port_terminal_operations_bootstrap_standalone_app()`
- `dispatch_standalone_route()`
- `port_terminal_operations_render_standalone_workbench()`
