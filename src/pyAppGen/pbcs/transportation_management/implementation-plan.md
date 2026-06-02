# transportation_management Implementation Plan

## Scope

Make Transportation Management usable as a one-PBC application with owned schema, runtime services, APIs, events, handlers, repository/read models, forms, wizards, controls, assistant skills, seed data, tests, and release evidence.

## Delivered Architecture

1. Runtime owns the shipment lifecycle from carrier registration through delivery proof.
2. Repository contracts expose package-local read models without introducing shared-table access.
3. UI contracts surface shipment, carrier, route, tracking, delivery, exception, and governance workflows.
4. Standalone smoke executes configuration, rules, parameters, schema extension, event projection, shipment creation, carrier selection, route planning, dispatch, tracking, arrival, delivery, and control testing.
5. Release evidence validates artifacts and executable surfaces.

## Guardrails

- No user-facing stream-engine picker.
- Ordinary backends remain PostgreSQL, MySQL, or MariaDB.
- Cross-PBC context enters through declared APIs, AppGen-X events, or owned projections.
