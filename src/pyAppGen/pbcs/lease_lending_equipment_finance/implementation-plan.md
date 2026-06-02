# Lease Lending and Equipment Finance Implementation Plan

## Intent

Turn the equipment finance package into a self-contained PBC that can originate, book, service, collect, recover, and report a transaction without relying on shared tables or placeholder evidence.

## Plan

1. Add forms for deal intake, product structure, parties, assets, funding, pricing/schedules, residuals, buyouts, and repo/disposition.
2. Add wizards for application-to-booking, structuring/pricing, funding, usage/reserves, end-of-term, collections/repo, and investor remittance.
3. Add controls for booking prerequisites, product compatibility, serial uniqueness, disbursement reconciliation, schedule lineage, collateral protection, repo notices, and investor waterfalls.
4. Implement a standalone app that exercises application intake, condition clearance, asset registration, funding reconciliation, schedule generation, usage billing, residual review, buyout quotes, booking, collections, repo, disposition, investor allocation, remittance, and assistant finance-pack previews.
5. Wire standalone UI and release evidence into the local package contracts.
6. Add focused tests and validation evidence.

## Boundary

All executable behavior stays inside `src/pyAppGen/pbcs/lease_lending_equipment_finance`, references only `lease_lending_equipment_finance_*` tables, and uses AppGen-X eventing.
