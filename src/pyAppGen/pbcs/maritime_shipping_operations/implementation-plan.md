# Maritime Shipping Operations Implementation Plan

## Intent

Make `maritime_shipping_operations` viable as a one-PBC maritime operating system for voyages, bookings, port calls, charters, claims, bunkers, compliance, and assistant-guided operations.

## Plan

1. Add maritime forms for voyages, vessel readiness, cargo bookings, charter clauses, port calls, stowage/special cargo, demurrage, bunkers/carbon, and compliance.
2. Add guided wizards for voyage publishing, booking-to-bill, port-call execution, laytime/demurrage, bunker/carbon, compliance, and schedule recovery.
3. Add controls that block unsafe voyage, booking, stowage, port-call, claim, bunker, and compliance actions until evidence exists.
4. Implement a standalone app that exercises vessel readiness, voyage delay propagation, bookings, bills, stowage, charter/laytime, statement of facts, demurrage, bunker/carbon, obligations, simulations, and assistant previews.
5. Wire standalone UI and release evidence into package-local contracts.
6. Add tests and record validation evidence.

## Boundary

All changes stay inside `src/pyAppGen/pbcs/maritime_shipping_operations`, reference only owned `maritime_shipping_operations_*` tables, and use AppGen-X event contracts.
