# Restaurant Operations PBC

`restaurant_operations` is a standalone AppGen-X packaged business capability for restaurant operators. It covers the operational surface needed to run a restaurant concept without depending on a second PBC for core workflows: menu and recipe management, floor plans, reservations and waitlists, prep and par planning, kitchen display execution, check settlement, food safety, incidents, loyalty recovery notes, and governed AI-assisted operational changes.

## Owned Domain

The PBC owns restaurant-specific execution records such as menu items, recipes, kitchen tickets, reservations, prep plans, waste/safety evidence, labor shift execution, floor plans, check settlements, vendor receipt evidence, guest incidents, loyalty notes, and governed preview records. Inventory, payroll, accounting, and customer master data remain adjacent domain truths; this PBC emits or consumes evidence instead of writing those tables directly.

## Standalone Application Surface

A composed application with only this PBC can bootstrap `RestaurantOperationsStandaloneService` through `restaurant_operations_bootstrap_standalone_app()`. The route dispatcher supports menu creation, recipe registration, floor plan design, reservation intake, shift readiness, prep planning, order creation, KDS state advancement, check settlement, vendor receipts, safety logs, incidents, loyalty notes, governed previews, and read models for the restaurant workbench, revenue, kitchen display, and governed AI preview queues.

## UI and Agent

The UI contract includes a restaurant workbench, dining room floor board, kitchen display board, safety/incident board, revenue and service analytics, reservation and waitlist forms, floor-plan design, safety logging, loyalty note capture, and guided workflows for reservation flow, service launch, and dining room recovery. The agent surface can ingest document/instruction context and produce confirmation-gated CRUD previews for PBC-owned tables only.

## Verification

The standalone smoke path seeds a representative restaurant day: menu and recipe setup, floor plan, reservation, staffing, prep, order flow, KDS advancement, settlement with comps/voids, receiving evidence, safety checks, incident capture, loyalty recovery, governed AI preview, workbench rendering, and revenue reporting. See `implementation-status.md` for exact command evidence.
