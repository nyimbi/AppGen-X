# Checkout Processing PBC

`checkout_processing` is a self-contained AppGen-X checkout slice for cart orchestration, pricing and tax handoffs, inventory and payment finalization, risk screening, workbench operations, and governed assistant support.

## What This Package Owns

- Checkout-owned models and migrations for carts, lines, checkout sessions, promotion redemptions, pricing/tax/inventory/payment handoffs, risk screens, address validation, rules, parameters, configuration, inbox, outbox, and dead letters.
- Executable runtime behavior for a full checkout scenario, including AppGen-X outbox/inbox handling and completion gating.
- Package-local app surfaces: services, routes, workbench UI, forms, wizards, controls, RBAC, configuration contracts, and assistant CRUD previews.

## Domain Shape

This PBC is optimized for headless commerce operations teams who need to:

- open and price carts,
- validate shipping and checkout readiness,
- confirm inventory before completion,
- authorize and capture payment in-sequence,
- investigate risk or dead-letter issues,
- review rules, parameters, and release readiness,
- use an assistant to turn uploaded checkout notes or instructions into bounded CRUD previews.

## Key Entry Points

- Runtime: [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/runtime.py)
- Services: [services.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/services.py)
- Routes: [routes.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/routes.py)
- Workbench UI: [ui.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/ui.py)
- Forms: [forms.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/forms.py)
- Wizards: [wizards.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/wizards.py)
- Controls: [controls.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/controls.py)
- Assistant support: [agent.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/agent.py)
- Release evidence: [release_evidence.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/release_evidence.py)

## One-PBC App Surface

The package now exposes:

- checkout intake, pricing, payment, and exception-handling forms,
- guided wizards for first checkout, exception recovery, release readiness, and assistant-assisted updates,
- package-local control dashboards for release readiness, completion gating, tenant boundary proof, and assistant guardrails,
- workbench metadata that binds panels, forms, wizards, and controls to checkout-owned data,
- agent/chatbot previews that classify documents and instructions into safe, permissioned CRUD plans.

## Verification

Primary verification lives in package-local tests under [tests](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/tests) and in the executable runtime smoke path inside [runtime.py](/Volumes/Media/src/pjs/appgen/src/pyAppGen/pbcs/checkout_processing/runtime.py).
